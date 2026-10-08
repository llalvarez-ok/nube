"""Motor de simulación de operaciones barra a barra (M1 preferido).

Supuestos de ejecución (documentados y conservadores):
  * Entrada: apertura de la barra siguiente al cierre de la vela de confirmación,
    al ASK (long) o BID (short), más slippage adverso.
  * Stop: se dispara cuando el BID (long) / ASK (short) toca el nivel. Se llena al
    peor entre el nivel y la apertura de la barra (gaps), más slippage adverso.
  * Take profit: orden límite, se llena exactamente en el nivel (sin mejora por gap).
  * Si en una misma barra se tocan stop y target, se asume SIEMPRE el stop primero.
  * Tras un TP parcial, el nuevo stop (breakeven) se evalúa desde esa misma barra
    (conservador). El trailing se recalcula al cierre de cada barra y aplica desde la
    siguiente.
  * Cierre forzado a `exit_time_utc` al cierre de la última barra de la sesión.
  * R = distancia planificada entre el precio esperado de entrada (ask/bid al cierre de
    la vela de señal) y el stop. El slippage y el spread hacen que una pérdida completa
    sea algo mayor que 1R: es intencional.

Los shorts se simulan en "espacio espejado" (precios negados) para usar el mismo código.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from .market import Market

EXIT_SL, EXIT_TP, EXIT_TIME, EXIT_TRAIL, EXIT_BE = 0, 1, 2, 3, 4
EXIT_NAMES = {EXIT_SL: "stop_loss", EXIT_TP: "take_profit", EXIT_TIME: "time_exit",
              EXIT_TRAIL: "trailing_stop", EXIT_BE: "breakeven"}


# ----------------------------------------------------------------------------
# Plan de salida
# ----------------------------------------------------------------------------

def exit_grid(strategy: str, scfg: dict) -> list[dict]:
    g = scfg["grid"]
    out = []
    if strategy[0] in "ACE":
        for sl in g["sl"]:
            for tp in g["tp"]:
                out.append({"sl": sl, "tp": tp})
    else:
        for b in g["buffer_atr"]:
            for ex in g["exit"]:
                out.append({"stop_buffer_atr": b, "exit": ex})
    return out


def plan(sig: dict, ex: dict, scfg: dict):
    """Devuelve (stop, legs[(fracción, tp|None)], be_after_first, trail) en precios reales o None."""
    d, e, atr = sig["direction"], sig["exp_entry"], sig["atr"]
    if "sl" in ex:
        kind, _, val = ex["sl"].partition("_")
        if ex["sl"] in ("range_opposite", "or_opposite"):
            stop = sig["range_lo"] if d > 0 else sig["range_hi"]
        elif kind == "range":
            stop = e - d * float(val) * sig["range"]
        elif kind == "atr":
            stop = e - d * float(val) * atr
        else:
            raise ValueError(ex["sl"])
        rdist = (e - stop) * d
        if not rdist > 0:
            return None
        tp = ex["tp"]
        if tp.startswith("r_"):
            return stop, [(1.0, e + d * float(tp[2:]) * rdist)], False, None, rdist
        tp1 = e + d * scfg.get("trail_tp1_r", 1.0) * rdist
        f = scfg.get("trail_partial_fraction", 0.5)
        trail = ("swing", None) if tp == "trail_swing" else ("atr", float(tp.split("_")[-1]))
        # con f = 0 el primer tramo (fracción 0) sólo actúa como disparador de BE + trailing
        legs = [(f, tp1), (1 - f, None)]
        return stop, legs, True, (trail, tp1), rdist
    # failed breakout
    stop = sig["sweep_ext"] + d * -1 * ex["stop_buffer_atr"] * atr
    rdist = (e - stop) * d
    mid, opp = sig["range_mid"], (sig["range_hi"] if d > 0 else sig["range_lo"])
    if not rdist > 0 or (mid - e) * d <= 0:      # midpoint ya superado: geometría inválida
        return None
    if ex["exit"] == "tp1_mid":
        legs = [(1.0, mid)]
    elif ex["exit"] == "tp2_opposite":
        legs = [(1.0, opp)]
    else:
        legs = [(0.5, mid), (0.5, opp)]
    return stop, legs, bool(scfg.get("split_move_to_be", True)) and len(legs) > 1, None, rdist


# ----------------------------------------------------------------------------
# Simulación de una operación
# ----------------------------------------------------------------------------

def _first(mask: np.ndarray) -> int:
    i = int(np.argmax(mask)) if len(mask) else 0
    return i if len(mask) and mask[i] else -1


def simulate(mk: Market, sig: dict, stop, legs, be_after_first, trail, rdist) -> dict | None:
    a = mk.arr
    e, i1, d = sig["entry_idx"], sig["exit_idx"], sig["direction"]
    if e >= i1:
        return None
    slip = mk.slip
    if d > 0:
        hi, lo, op, cl = a["bid_h"][e:i1], a["bid_l"][e:i1], a["bid_o"][e:i1], a["bid_c"][e:i1]
        entry = a["ask_o"][e] + slip
        sw = a["swing_low"][e:i1]
        s = stop
        tps = [tp for _, tp in legs]
    else:   # espacio espejado
        hi, lo, op, cl = -a["ask_l"][e:i1], -a["ask_h"][e:i1], -a["ask_o"][e:i1], -a["ask_c"][e:i1]
        entry = -(a["bid_o"][e] - slip)
        sw = -a["swing_high"][e:i1]
        s = -stop
        tps = [None if tp is None else -tp for _, tp in legs]
    n = len(hi)
    tatr = a["trail_atr"][e:i1]

    remaining = [(f, tp) for (f, _), tp in zip(legs, tps)]
    fills = []                       # (fracción, precio, barra, motivo)
    k0 = 0
    cur_stop = s
    stop_reason = EXIT_SL
    trailing_from = None
    while remaining and k0 < n:
        f_next, tp_next = remaining[0]
        # stop vigente por barra
        if trailing_from is None:
            stop_arr = np.full(n - k0, cur_stop)
        else:
            j = trailing_from
            mode, mult = trail[0]
            if mode == "atr":
                cand = np.maximum.accumulate(hi[j:]) - mult * np.nan_to_num(tatr[j:], nan=np.inf)
            else:
                cand = np.nan_to_num(sw[j:], nan=-np.inf)
            dyn = np.maximum.accumulate(np.maximum(cand, cur_stop))
            st = np.empty(n - j)
            st[0] = cur_stop
            st[1:] = dyn[:-1]                       # el trailing calculado al cierre aplica desde la barra siguiente
            stop_arr = st[k0 - j:]
        ks = _first(lo[k0:] <= stop_arr)
        kt = _first(hi[k0:] >= tp_next) if tp_next is not None else -1
        if ks >= 0 and (kt < 0 or ks <= kt):       # stop primero (incluye empate)
            k = k0 + ks
            lvl = stop_arr[ks]
            px = min(lvl, op[k]) - slip
            reason = stop_reason if trailing_from is None or lvl <= cur_stop + 1e-12 else EXIT_TRAIL
            for f, _ in remaining:
                fills.append((f, px, k, reason))
            remaining = []
            break
        if kt >= 0:
            k = k0 + kt
            fills.append((f_next, tp_next, k, EXIT_TP))
            remaining = remaining[1:]
            if be_after_first and len(fills) == 1:
                cur_stop = max(cur_stop, entry)     # breakeven sobre el precio de entrada
                stop_reason = EXIT_BE
                if trail is not None:
                    trailing_from = k
            k0 = k                                  # el nuevo stop se evalúa desde esta misma barra
            if trailing_from is None and not be_after_first:
                k0 = k + 1
            continue
        break
    if remaining:                                   # cierre por tiempo
        k = n - 1
        px = cl[k] - slip
        for f, _ in remaining:
            fills.append((f, px, k, EXIT_TIME))
    last_k = max(f[2] for f in fills)
    pnl = sum(f * (px - entry) for f, px, _, _ in fills)
    exit_px = sum(f * px for f, px, _, _ in fills)
    mfe = np.max(hi[:last_k + 1]) - entry
    mae = entry - np.min(lo[:last_k + 1])
    final_reason = fills[-1][3] if len(fills) == 1 else max(fills, key=lambda x: x[2])[3]
    return {"entry_fill": entry * d, "exit_fill": exit_px * d, "pnl_px": pnl, "exit_bar": e + last_k,
            "exit_reason": final_reason, "tp1_hit": any(r == EXIT_TP for *_, r in fills),
            "mae_px": mae, "mfe_px": mfe, "stop": stop, "rdist": rdist,
            "tp": legs[0][1] if legs[0][1] is not None else np.nan,
            "tp2": legs[1][1] if len(legs) > 1 and legs[1][1] is not None else np.nan}


# ----------------------------------------------------------------------------
# Grilla completa de un símbolo/estrategia
# ----------------------------------------------------------------------------

def run_signal_sets(mk: Market, strategy: str, scfg: dict, signal_sets: dict, exits: list[dict] | None = None):
    """Simula cada conjunto de señales bajo cada plan de salida.

    Devuelve (signals_df, trades_df). trades_df es compacto: sig_id + params + resultados.
    """
    exits = exits if exits is not None else exit_grid(strategy, scfg)
    sig_rows, trade_rows = [], []
    sid = 0
    for sig_key, sigs in signal_sets.items():
        for sig in sigs:
            sig = dict(sig)
            sig["sig_id"] = sid
            for k, v in sig_key:
                sig[k] = v
            sig_rows.append(sig)
            for ex in exits:
                p = plan(sig, ex, scfg)
                if p is None:
                    continue
                r = simulate(mk, sig, *p)
                if r is None:
                    continue
                row = {"sig_id": sid, **{f"p_{k}": v for k, v in sig_key}, **{f"p_{k}": v for k, v in ex.items()}}
                row.update(r)
                trade_rows.append(row)
            sid += 1
    sdf = pd.DataFrame(sig_rows)
    tdf = pd.DataFrame(trade_rows)
    if len(tdf):
        t = mk.arr_t
        tdf["entry_time"] = pd.to_datetime(t[sdf.set_index("sig_id").loc[tdf["sig_id"], "entry_idx"].values])
        tdf["exit_time"] = pd.to_datetime(mk.arr["close_t"][tdf["exit_bar"].values])
        tdf["mae_R"] = tdf["mae_px"] / tdf["rdist"]
        tdf["mfe_R"] = tdf["mfe_px"] / tdf["rdist"]
    return sdf, tdf
