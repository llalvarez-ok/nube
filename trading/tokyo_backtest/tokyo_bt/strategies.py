"""Generación de señales de las estrategias A–E.

Reglas comunes (sin look-ahead):
  * El rango [start, end) se construye con barras M5 cuya apertura cae dentro de
    la ventana; recién se conoce en `end` (cierre de la última barra).
  * Sólo se evalúan velas M5 con apertura >= end. La señal ocurre al CIERRE de la
    vela de confirmación; la entrada se ejecuta en la apertura de la siguiente
    barra de ejecución (M1), que es el primer precio negociable posterior.
  * Precios de referencia: mid. Las ejecuciones usan bid/ask (ver engine.py).
  * Máximo una señal por breakout y por dirección en cada sesión.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from .config import hhmm_to_minutes
from .market import Market, Session


_ROW_COLS = ("mid_h", "mid_l", "mid_c", "ask_c", "bid_c", "vwap")


def _rows(mk: Market, start: pd.Timestamp, end: pd.Timestamp):
    """Itera (t, dict) sobre velas M5 con apertura en [start, end). Sin iterrows (lento)."""
    if not hasattr(mk, "_m5_np"):
        mk._m5_np = {c: mk.m5[c].to_numpy(dtype=float) for c in _ROW_COLS}
        mk._m5_t = mk.m5.index.to_numpy()
    t = mk._m5_t
    i0 = np.searchsorted(t, start.to_datetime64())
    i1 = np.searchsorted(t, end.to_datetime64())
    a = mk._m5_np
    for i in range(i0, i1):
        yield pd.Timestamp(t[i]), {c: a[c][i] for c in _ROW_COLS}


def _window(m5: pd.DataFrame, start: pd.Timestamp, end: pd.Timestamp):
    return m5.loc[start:end - pd.Timedelta(minutes=1)]


def _range(m5: pd.DataFrame, start, end, min_cov=0.9):
    w = _window(m5, start, end)
    n_exp = (end - start) / pd.Timedelta(minutes=5)
    if len(w) == 0 or len(w) < np.floor(n_exp * min_cov):
        return None
    hi, lo = float(w["mid_h"].max()), float(w["mid_l"].min())
    if hi <= lo:
        return None
    return {"hi": hi, "lo": lo, "rng": hi - lo, "mid": (hi + lo) / 2, "end": end}


def _base(mk: Market, sess: Session, strategy, direction, bar_t, row, rng, extra):
    sig_t = bar_t + pd.Timedelta(minutes=5)          # cierre de la vela de confirmación
    if sig_t > sess.last_entry:
        return None
    e = mk.bar_index_at(sig_t)
    if e >= sess.i1:
        return None
    exp_entry = float(row["ask_c"]) if direction > 0 else float(row["bid_c"])
    d = {"strategy": strategy, "symbol": mk.symbol, "date": sess.date, "direction": direction,
         "signal_time": sig_t, "entry_idx": e, "exit_idx": sess.i1, "exp_entry": exp_entry,
         "signal_close_mid": float(row["mid_c"]), "atr": sess.atr, "vol_regime": sess.vol_regime,
         "range_hi": rng["hi"], "range_lo": rng["lo"], "range": rng["rng"], "range_mid": rng["mid"],
         "range_atr": rng["rng"] / sess.atr, "vwap": float(row.get("vwap", np.nan)),
         "spread_at_signal": float(row["ask_c"] - row["bid_c"])}
    d.update(extra)
    return d


# ----------------------------------------------------------------------------
# Breakout (A, C, E)
# ----------------------------------------------------------------------------

def breakout_signals(mk: Market, sess: Session, rng: dict, buffer_atr: float, strategy: str,
                     vwap_filter: bool = False, vwap_lb: int = 6, extra=None) -> list[dict]:
    buf = buffer_atr * sess.atr
    out, done = [], {1: False, -1: False}
    vw = mk.m5["vwap"]
    for t, row in _rows(mk, rng["end"], sess.exit):
        c = row["mid_c"]
        for direction in (1, -1):
            if done[direction]:
                continue
            if direction > 0:
                broke = row["mid_h"] > rng["hi"] and c > rng["hi"] + buf
                dist = c - rng["hi"]
            else:
                broke = row["mid_l"] < rng["lo"] and c < rng["lo"] - buf
                dist = rng["lo"] - c
            if not broke:
                continue
            ex = {"buffer_atr": buffer_atr, "breakout_dist_atr": dist / sess.atr, "vwap_filter": vwap_filter}
            if vwap_filter:
                v_now = row["vwap"]
                prev_t = t - pd.Timedelta(minutes=5 * vwap_lb)
                v_prev = vw.asof(prev_t) if prev_t >= vw.index[0] else np.nan
                if np.isnan(v_now) or np.isnan(v_prev):
                    continue
                slope = v_now - v_prev
                ok = (c > v_now and slope > 0) if direction > 0 else (c < v_now and slope < 0)
                ex["vwap_slope_atr"] = slope / sess.atr
                if not ok:
                    continue   # se sigue buscando una confirmación posterior que cumpla VWAP
            s = _base(mk, sess, strategy, direction, t, row, rng, {**ex, **(extra or {})})
            done[direction] = True   # una única operación por breakout y dirección
            if s:
                out.append(s)
    return out


# ----------------------------------------------------------------------------
# Failed breakout / mean reversion (B, D)
# ----------------------------------------------------------------------------

def failed_breakout_signals(mk: Market, sess: Session, rng: dict, min_sweep_atr: float, strategy: str,
                            extra=None) -> list[dict]:
    """SHORT: el precio supera el high, se registra el máximo del sweep y una M5 vuelve a
    cerrar DENTRO del rango -> short al cierre. LONG: inverso sobre el low."""
    out = []
    state = {-1: None, 1: None}       # -1: sweep del high (short); +1: sweep del low (long)
    done = {-1: False, 1: False}
    for t, row in _rows(mk, rng["end"], sess.exit):
        h, l, c = row["mid_h"], row["mid_l"], row["mid_c"]
        for direction in (-1, 1):
            if done[direction]:
                continue
            st = state[direction]
            beyond = (h > rng["hi"]) if direction < 0 else (l < rng["lo"])
            if st is None and beyond:
                st = state[direction] = {"start": t, "ext": h if direction < 0 else l, "bars": 0}
            if st is None:
                continue
            st["ext"] = max(st["ext"], h) if direction < 0 else min(st["ext"], l)
            st["bars"] += 1
            inside = rng["lo"] < c < rng["hi"]
            if not inside:
                continue
            depth = (st["ext"] - rng["hi"]) if direction < 0 else (rng["lo"] - st["ext"])
            if depth / sess.atr < min_sweep_atr:
                state[direction] = None    # sweep insuficiente: se descarta y se espera otro
                continue
            ex = {"sweep_ext": st["ext"], "sweep_depth_atr": depth / sess.atr, "min_sweep_atr": min_sweep_atr,
                  "bars_outside": st["bars"],
                  "minutes_outside": (t + pd.Timedelta(minutes=5) - st["start"]).total_seconds() / 60,
                  "dist_to_mid_atr": abs(c - rng["mid"]) / sess.atr}
            s = _base(mk, sess, strategy, direction, t, row, rng, {**ex, **(extra or {})})
            done[direction] = True
            state[direction] = None
            if s:
                out.append(s)
    return out


# ----------------------------------------------------------------------------
# Generadores por estrategia: devuelven {clave_de_señal: [señales]}
# ----------------------------------------------------------------------------

def _t(sess, hhmm):
    return sess.date + pd.Timedelta(minutes=hhmm_to_minutes(hhmm))


def gen_A(mk, scfg):
    out = {}
    for b in scfg["grid"]["buffer_atr"]:
        sigs = []
        for s in mk.tradable_sessions():
            r = _range(mk.m5, _t(s, scfg["range_start_utc"]), _t(s, scfg["range_end_utc"]))
            if r:
                sigs += breakout_signals(mk, s, r, b, "A_asian_range_breakout")
        out[(("buffer_atr", b),)] = sigs
    return out


def gen_B(mk, scfg):
    out = {}
    for ms in scfg["grid"]["min_sweep_atr"]:
        sigs = []
        for s in mk.tradable_sessions():
            r = _range(mk.m5, _t(s, scfg["range_start_utc"]), _t(s, scfg["range_end_utc"]))
            if r:
                sigs += failed_breakout_signals(mk, s, r, ms, "B_asian_failed_breakout")
        out[(("min_sweep_atr", ms),)] = sigs
    return out


def gen_C(mk, scfg):
    out = {}
    for orm in scfg["grid"]["or_minutes"]:
        for b in scfg["grid"]["buffer_atr"]:
            sigs = []
            for s in mk.tradable_sessions():
                st = _t(s, scfg["or_start_utc"])
                r = _range(mk.m5, st, st + pd.Timedelta(minutes=orm))
                if r:
                    sigs += breakout_signals(mk, s, r, b, "C_tokyo_or_breakout", extra={"or_minutes": orm})
            out[(("or_minutes", orm), ("buffer_atr", b))] = sigs
    return out


def gen_D(mk, scfg):
    out = {}
    for orm in scfg["grid"]["or_minutes"]:
        for ms in scfg["grid"]["min_sweep_atr"]:
            sigs = []
            for s in mk.tradable_sessions():
                st = _t(s, scfg["or_start_utc"])
                r = _range(mk.m5, st, st + pd.Timedelta(minutes=orm))
                if r:
                    sigs += failed_breakout_signals(mk, s, r, ms, "D_tokyo_or_failed_breakout",
                                                    extra={"or_minutes": orm})
            out[(("or_minutes", orm), ("min_sweep_atr", ms))] = sigs
    return out


def gen_E(mk, scfg, vwap_lb):
    out = {}
    if not mk.has_volume:
        return out
    for vf in scfg["vwap_filter"]:
        for b in scfg["grid"]["buffer_atr"]:
            sigs = []
            for s in mk.tradable_sessions():
                r = _range(mk.m5, _t(s, scfg["range_start_utc"]), _t(s, scfg["range_end_utc"]))
                if r:
                    sigs += breakout_signals(mk, s, r, b, "E_tokyo_breakout_vwap", vwap_filter=vf, vwap_lb=vwap_lb)
            out[(("vwap_filter", vf), ("buffer_atr", b))] = sigs
    return out


def generate(mk: Market, strategy: str, scfg: dict, cfg: dict):
    if strategy.startswith("A_"):
        return gen_A(mk, scfg)
    if strategy.startswith("B_"):
        return gen_B(mk, scfg)
    if strategy.startswith("C_"):
        return gen_C(mk, scfg)
    if strategy.startswith("D_"):
        return gen_D(mk, scfg)
    if strategy.startswith("E_"):
        return gen_E(mk, scfg, cfg["indicators"]["vwap"]["slope_lookback_bars"])
    raise ValueError(strategy)
