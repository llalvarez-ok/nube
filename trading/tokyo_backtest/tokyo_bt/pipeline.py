"""Orquestación del estudio completo.

Fase 0  verificación de datos (aborta símbolos con problemas CRÍTICOS)
Fase 1  simulación de toda la grilla + selección con IS/VAL + walk-forward (pre-OOS)
Fase 2  CONGELAR selección en selection.json  <- a partir de aquí no se elige nada
Fase 3  OOS, sensibilidad de costos, modos de posición, noticias, capital, Monte Carlo,
        MAE/MFE, hora/día/volatilidad, correlaciones, gráficos y reporte.
"""
from __future__ import annotations

import json
import pickle
import time
from concurrent.futures import ProcessPoolExecutor
from copy import deepcopy
from pathlib import Path

import numpy as np
import pandas as pd

from . import analysis as an
from . import charts as ch
from .config import resolve
from .costs import Converter
from .data import load_cached
from .engine import run_signal_sets
from .market import Market
from .metrics import equity_metrics, equity_sim, r_metrics
from .postprocess import (SIG_COLS, enrich, load_news, news_mask, position_mask, range_filter_mask, segment,
                          split_bounds)
from .quality import CRITICAL, check_all
from .research import (deflated, freeze, grid_metrics, kept_by_filter, marginal_regions, parse_cid,
                       select, walk_forward)
from .strategies import generate

PARAM_TO_GRID = {"stop_buffer_atr": "buffer_atr"}


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def _out(cfg, *parts) -> Path:
    p = resolve(cfg, cfg["project"]["output_dir"]).joinpath(*parts)
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def _default_mode(cfg):
    name = cfg["default_position_mode"]
    return next(m for m in cfg["position_modes"] if m["name"] == name)


def _conv_series(cfg, symbols_ok):
    """Cierres mid del símbolo de conversión indexados por hora de cierre."""
    series = {}
    for ccy, rule in cfg["conversion"].items():
        if rule and rule["symbol"] in symbols_ok and rule["symbol"] not in series:
            raw = load_cached(cfg, rule["symbol"])
            mk = Market.build(raw, rule["symbol"], cfg)
            series[rule["symbol"]] = pd.Series(mk.arr["mid_c"], index=pd.DatetimeIndex(mk.arr["close_t"]))
    return series


def narrow_scfg(scfg: dict, params: dict) -> dict:
    """Copia de la config de la estrategia con la grilla reducida a los parámetros dados."""
    s = deepcopy(scfg)
    for k, v in params.items():
        if k == "rf":
            s["grid"]["range_filter"] = [v]
            continue
        if k == "vwap_filter":
            s["vwap_filter"] = [v == "True"]
            continue
        gk = PARAM_TO_GRID.get(k, k)
        cur = s["grid"].get(gk, [])
        match = [x for x in cur if str(x) == v]
        s["grid"][gk] = match or [type(cur[0])(v) if cur else v]
    return s


def _exit_from_params(strategy, params):
    if strategy[0] in "ACE":
        return [{"sl": params["sl"], "tp": params["tp"]}]
    return [{"stop_buffer_atr": float(params["stop_buffer_atr"]), "exit": params["exit"]}]


# ----------------------------------------------------------------------------
# Fase 1 (por símbolo, en paralelo)
# ----------------------------------------------------------------------------

def phase1_symbol(cfg: dict, symbol: str, strategies: list[str], conv_series: dict) -> dict:
    t0 = time.time()
    raw = load_cached(cfg, symbol)
    mk = Market.build(raw, symbol, cfg)
    conv = Converter(cfg, conv_series)
    sessions = mk.tradable_sessions()
    dates = pd.DatetimeIndex([s.date for s in sessions])
    bounds = split_bounds(dates, cfg)
    res = {"symbol": symbol, "bounds": bounds, "timeframe": raw.attrs.get("timeframe"),
           "spread_source": mk.spread_source, "has_volume": mk.has_volume, "pairs": {},
           "n_sessions": len(sessions)}
    # retorno mid de la sesión (para correlaciones)
    a = mk.arr
    res["session_ret"] = pd.Series({s.date: a["mid_c"][s.i1 - 1] / a["mid_o"][s.i0] - 1 for s in sessions})
    mode = _default_mode(cfg)
    for strat in strategies:
        scfg = cfg["strategies"][strat]
        if symbol not in scfg["symbols"]:
            continue
        if strat.startswith("E_") and not mk.has_volume:
            res["pairs"][strat] = {"status": "NO DISPONIBLE: sin volumen no se puede calcular VWAP"}
            continue
        sets = generate(mk, strat, scfg, cfg)
        sdf, tdf = run_signal_sets(mk, strat, scfg, sets)
        if tdf.empty:
            res["pairs"][strat] = {"status": "SIN OPERACIONES"}
            continue
        t = enrich(tdf, sdf, mk.spec, conv, mk.slip)
        t["segment"] = segment(t["date"], bounds)
        kept = kept_by_filter(t, scfg["grid"].get("range_filter", ["none"]), mode)
        sel = select(kept, cfg)
        if strat.startswith("E_"):
            # la estrategia E es CON VWAP; la variante sin VWAP sólo es el grupo de control
            kept_v = {rf: k[k["cfg"].str.contains("vwap_filter=True")] for rf, k in kept.items()}
            sel_v = select(kept_v, cfg)
            sel_v["is_tab"], sel_v["val_tab"] = sel["is_tab"], sel["val_tab"]
            if sel_v.get("candidates") is not None and len(sel_v["candidates"]):
                sel_v["candidates"]["robust_expectancy_R"] = sel["is_tab"]["robust_expectancy_R"].reindex(
                sel_v["candidates"].index).fillna(sel_v["candidates"]["robust_expectancy_R"])
            sel = sel_v
        wf = walk_forward(kept, bounds, cfg, sel["chosen"])
        best_reg, worst_reg = marginal_regions(sel["is_tab"], sel.get("min_trades", 0))
        pth = _out(cfg, "trades", f"{strat}__{symbol}.pkl")
        with open(pth, "wb") as fh:
            pickle.dump({"t": t, "sdf": sdf, "kept": kept}, fh)
        res["pairs"][strat] = {
            "status": "OK", "chosen": sel["chosen"], "candidates": sel.get("candidates"),
            "is_tab": sel["is_tab"], "val_tab": sel["val_tab"], "n_configs": sel.get("n_configs_tested", 0),
            "bh_significant_is": sel.get("bh_significant_is", 0),
            "dsr": deflated(kept, sel["chosen"], sel["sr_trials"]) if sel["chosen"] else {},
            "wf": wf, "best_region": best_reg, "worst_region": worst_reg, "trades_path": str(pth),
            "n_signals": int(len(sdf))}
    log(f"{symbol}: fase 1 completa en {time.time() - t0:.0f}s")
    return res


# ----------------------------------------------------------------------------
# Fase 3 helpers
# ----------------------------------------------------------------------------

def frozen_trades(cfg, strat, symbol, chosen, mode=None, pair_pickle=None):
    """Operaciones completas de la configuración congelada (con todos los campos de la señal)."""
    with open(pair_pickle, "rb") as fh:
        d = pickle.load(fh)
    t, sdf = d["t"], d["sdf"]
    params = parse_cid(chosen)
    sub = t[t["cfg"] == chosen.rsplit("|rf=", 1)[0]]
    sub = sub[range_filter_mask(sub["range_atr"], params["rf"])]
    mode = mode or _default_mode(cfg)
    sub = sub[position_mask(sub, ["cfg"], mode["max_per_session"], mode["single_position"])]
    extra = ["sig_id"] + [c for c in SIG_COLS if c in sdf.columns and c not in sub.columns]
    ft = sub.merge(sdf[extra], on="sig_id", how="left").sort_values("entry_time").reset_index(drop=True)
    ft["cid"] = chosen
    return ft


def cost_sensitivity(cfg, strat, symbol, chosen, conv_series, bounds) -> pd.DataFrame:
    scfg = cfg["strategies"][strat]
    params = parse_cid(chosen)
    narrowed = narrow_scfg(scfg, {k: v for k, v in params.items() if k not in ("sl", "tp", "exit",
                                                                               "stop_buffer_atr")})
    exits = _exit_from_params(strat, params)
    raw = load_cached(cfg, symbol)
    conv = Converter(cfg, conv_series)
    rows = []
    for sm in cfg["sensitivity"]["spread_mult"]:
        for lm in cfg["sensitivity"]["slippage_mult"]:
            mk = Market.build(raw, symbol, cfg, spread_mult=sm, slip_mult=lm)
            sets = generate(mk, strat, narrowed, cfg)
            sdf, tdf = run_signal_sets(mk, strat, narrowed, sets, exits=exits)
            if tdf.empty:
                continue
            t = enrich(tdf, sdf, mk.spec, conv, mk.slip)
            t = t[range_filter_mask(t["range_atr"], params["rf"])]
            m = _default_mode(cfg)
            t = t[position_mask(t, ["cfg"], m["max_per_session"], m["single_position"])]
            seg = segment(t["date"], bounds)
            for lbl, mask in (("pre_OOS", seg != "OOS"), ("OOS", seg == "OOS")):
                r = r_metrics(t.loc[mask, "R"].values)
                rows.append({"spread_mult": sm, "slippage_mult": lm, "segment": lbl,
                             "trades": r.get("trades", 0), "expectancy_R": r.get("expectancy_R", np.nan),
                             "profit_factor": r.get("profit_factor", np.nan), "net_R": r.get("net_R", 0)})
    return pd.DataFrame(rows)


def _phase3_costs(args):
    cfg, strat, symbol, chosen, conv_series, bounds = args
    return (strat, symbol), cost_sensitivity(cfg, strat, symbol, chosen, conv_series, bounds)


# ----------------------------------------------------------------------------
# Orquestador
# ----------------------------------------------------------------------------

def run(cfg: dict, symbols: list[str] | None = None, strategies: list[str] | None = None,
        workers: int = 4, skip_costs: bool = False):
    synthetic = bool(cfg.get("_synthetic"))
    all_syms = symbols or list(cfg["instruments"])
    strategies = strategies or [s for s, c in cfg["strategies"].items() if c.get("enabled")]
    log("Fase 0: verificación de datos")
    quality = check_all(cfg, all_syms)
    ok = [s for s in all_syms if quality[s]["status"] != CRITICAL]
    bad = {s: [i["msg"] for i in quality[s]["issues"] if i["level"] == CRITICAL] for s in all_syms if s not in ok}
    for s, msgs in bad.items():
        log(f"  EXCLUIDO {s}: {' | '.join(msgs)}")
    # símbolos cotizados en una moneda sin serie de conversión
    for s in list(ok):
        rule = cfg["conversion"].get(cfg["instruments"][s]["quote_ccy"])
        if rule and rule["symbol"] not in ok:
            bad[s] = [f"sin datos de {rule['symbol']} para convertir {cfg['instruments'][s]['quote_ccy']} a USD"]
            ok.remove(s)
    if not ok:
        raise SystemExit("No hay ningún símbolo con datos válidos. Ver output/data_quality.md y DATOS_REQUERIDOS.md")
    conv_series = _conv_series(cfg, ok)

    log(f"Fase 1: simulación de la grilla ({len(ok)} símbolos, {len(strategies)} estrategias)")
    if workers > 1:
        with ProcessPoolExecutor(max_workers=workers) as ex:
            res = list(ex.map(phase1_symbol, [cfg] * len(ok), ok, [strategies] * len(ok), [conv_series] * len(ok)))
    else:
        res = [phase1_symbol(cfg, s, strategies, conv_series) for s in ok]
    by_sym = {r["symbol"]: r for r in res}

    log("Fase 2: congelando la selección (IS + VAL) antes de mirar el OOS")
    selections = {}
    for s, r in by_sym.items():
        for strat, p in r["pairs"].items():
            if p["status"] == "OK" and p["chosen"]:
                cand = p["candidates"].loc[p["chosen"]]
                selections[f"{strat}::{s}"] = {
                    "cid": p["chosen"], "is_expectancy_R": cand["expectancy_R"],
                    "is_robust_expectancy_R": cand["robust_expectancy_R"],
                    "val_expectancy_R": cand["val_expectancy_R"], "is_trades": cand["trades"],
                    "val_trades": cand["val_trades"],
                    "split": {k: str(v) for k, v in r["bounds"].items()}}
    sel_hash = freeze(selections, _out(cfg, "selection.json"))
    log(f"  selection.json congelado (hash {sel_hash}) con {len(selections)} configuraciones")

    log("Fase 3: OOS y análisis de la selección congelada")
    return phase3(cfg, by_sym, selections, sel_hash, conv_series, quality, bad, strategies, synthetic,
                  workers, skip_costs)


def phase3(cfg, by_sym, selections, sel_hash, conv_series, quality, bad, strategies, synthetic, workers,
           skip_costs):
    conv = Converter(cfg, conv_series)
    initial = cfg["project"]["initial_equity"]
    specs = cfg["instruments"]
    tables = {}
    rows_all_cfg = []
    frozen = []
    summary = []
    wf_all = []
    for s, r in by_sym.items():
        b = r["bounds"]
        for strat, p in r["pairs"].items():
            if p["status"] != "OK":
                summary.append({"strategy": strat, "symbol": s, "status": p["status"]})
                continue
            with open(p["trades_path"], "rb") as fh:
                kept = pickle.load(fh)["kept"]
            oos_tab = grid_metrics(kept, lambda k: k["segment"].values == "OOS")   # sólo para reporte
            ist, vt = p["is_tab"], p["val_tab"]
            big = ist.add_prefix("is_").join(vt[["trades", "expectancy_R", "profit_factor", "max_dd_R"]]
                                             .add_prefix("val_"), how="left") \
                .join(oos_tab[["trades", "expectancy_R", "profit_factor", "max_dd_R"]].add_prefix("oos_"), how="left")
            big["strategy"], big["symbol"] = strat, s
            rows_all_cfg.append(big.reset_index().rename(columns={"index": "cid", "cid": "cid"}))
            if not p["chosen"]:
                summary.append({"strategy": strat, "symbol": s, "status": "SIN CONFIGURACIÓN ELEGIBLE "
                                "(pocas operaciones IS)"})
                continue
            ft = frozen_trades(cfg, strat, s, p["chosen"], pair_pickle=p["trades_path"])
            ft["segment"] = segment(ft["date"], b)
            frozen.append(ft)
            wf = p["wf"].assign(strategy=strat, symbol=s)
            wf_all.append(wf)
            row = {"strategy": strat, "symbol": s, "status": "OK", "cid": p["chosen"],
                   "timeframe": f"{r['timeframe']} ejecución / M5 señal", "spread_source": r["spread_source"],
                   "n_configs_tested": p["n_configs"], "bh_significant_is": p["bh_significant_is"],
                   "dsr_is": p["dsr"].get("dsr", np.nan), "best_region": p["best_region"],
                   "worst_region": p["worst_region"]}
            cand = p["candidates"].loc[p["chosen"]]
            row.update(robust_expectancy_R=cand["robust_expectancy_R"],
                       neighbor_positive_share=cand["neighbor_positive_share"])
            for seg in ("IS", "VAL", "OOS"):
                m = r_metrics(ft.loc[ft["segment"] == seg, "R"].values)
                for k in ("trades", "win_rate", "expectancy_R", "profit_factor", "max_dd_R"):
                    row[f"{seg}_{k}"] = m.get(k, np.nan)
            # métricas de cuenta (riesgo 0.5% sobre equity actual) en todo el período y OOS
            for lbl, mask in (("ALL", np.ones(len(ft), bool)), ("OOS", ft["segment"].values == "OOS")):
                sub = ft[mask]
                if len(sub) == 0:
                    continue
                st = b["start"] if lbl == "ALL" else b["val_end"]
                es = equity_sim(sub, initial, "risk", 0.5, specs=specs)
                em = equity_metrics(es, initial, st, b["end"])
                for k in ("net_return_pct", "max_dd_pct", "sharpe", "sortino", "cagr_pct", "calmar",
                          "average_R", "recovery_factor", "avg_dd_pct"):
                    row[f"{lbl}_{k}"] = em.get(k, np.nan)
            # FRÁGIL
            pre = ft[ft["segment"] != "OOS"]
            yr = pre.groupby(pre["date"].dt.year)["R"].sum()
            pos_total = yr[yr > 0].sum()
            row["max_year_share"] = float(yr.max() / pos_total) if pos_total > 0 else np.nan
            wfv = wf["wf_test_net_R"]
            row["wf_windows"] = int(len(wf))
            row["wf_positive_share"] = float((wfv > 0).mean()) if len(wf) else np.nan
            sc = cfg["selection"]
            fragile = []
            if not np.isnan(row["max_year_share"]) and row["max_year_share"] > sc["fragile_max_year_share"]:
                fragile.append(f"{row['max_year_share']:.0%} del beneficio pre-OOS en un solo año")
            if len(wf) and row["wf_positive_share"] < sc["fragile_min_wf_positive"]:
                fragile.append(f"sólo {row['wf_positive_share']:.0%} de ventanas WF positivas")
            if row.get("neighbor_positive_share", 1) < 0.5:
                fragile.append("menos de la mitad de los vecinos de parámetros son positivos")
            row["fragile"] = "FRÁGIL: " + "; ".join(fragile) if fragile else ""
            summary.append(row)

    summary = pd.DataFrame(summary)
    ok_rows = summary[summary["status"] == "OK"] if "status" in summary else summary
    frozen_df = pd.concat(frozen, ignore_index=True) if frozen else pd.DataFrame()

    # ---- sensibilidad de costos ----
    cost_tabs = {}
    if not skip_costs and len(ok_rows):
        log("  sensibilidad de costos (spread x1/x1.5/x2, slippage x1/x2/x3)")
        jobs = [(cfg, r.strategy, r.symbol, r.cid, conv_series, by_sym[r.symbol]["bounds"])
                for r in ok_rows.itertuples()]
        if workers > 1:
            with ProcessPoolExecutor(max_workers=workers) as ex:
                for key, tab in ex.map(_phase3_costs, jobs):
                    cost_tabs[key] = tab
        else:
            for j in jobs:
                key, tab = _phase3_costs(j)
                cost_tabs[key] = tab
        flags = []
        for r in ok_rows.itertuples():
            tab = cost_tabs.get((r.strategy, r.symbol), pd.DataFrame())
            flag = ""
            if not tab.empty:
                pre = tab[tab["segment"] == "pre_OOS"].set_index(["spread_mult", "slippage_mult"])["expectancy_R"]
                bad_c = [f"spread x{k[0]:g}/slip x{k[1]:g}" for k in [(1.5, 1.0), (1.0, 2.0)]
                         if k in pre.index and not pre[k] > 0]
                if bad_c:
                    flag = "NO ROBUSTA: expectancy <= 0 con " + ", ".join(bad_c)
            flags.append(flag)
        summary.loc[ok_rows.index, "cost_flag"] = flags
        ok_rows = summary[summary["status"] == "OK"]

    # ---- veredicto ----
    def verdict(r):
        if r.get("status") != "OK":
            return r.get("status")
        conds = [r["IS_expectancy_R"] > 0, r["VAL_expectancy_R"] > 0, r["OOS_expectancy_R"] > 0,
                 (r["OOS_profit_factor"] or 0) > 1.1, not r.get("fragile"), not r.get("cost_flag")]
        if all(conds) and (r.get("dsr_is") or 0) > 0.95:
            return "CANDIDATA ROBUSTA (requiere forward test)"
        if r["IS_expectancy_R"] > 0 and (r["VAL_expectancy_R"] <= 0 or r["OOS_expectancy_R"] <= 0):
            return "SIN VENTAJA: se degrada fuera de muestra"
        if r.get("fragile"):
            return "FRÁGIL"
        if r.get("cost_flag"):
            return "NO ROBUSTA (costos)"
        if all(conds):
            return "POSITIVA PERO NO SIGNIFICATIVA tras corrección por minería (DSR <= 0.95)"
        return "SIN VENTAJA ESTADÍSTICA"
    if len(summary):
        summary["verdict"] = summary.apply(verdict, axis=1)

    # ranking compuesto (orden pedido: expectancy, PF, DD, robustez, OOS)
    if len(ok_rows):
        s2 = summary[summary["status"] == "OK"].copy()
        pre_exp = (s2["IS_expectancy_R"] * s2["IS_trades"] + s2["VAL_expectancy_R"] * s2["VAL_trades"]) / \
                  (s2["IS_trades"] + s2["VAL_trades"])
        s2["pre_oos_expectancy_R"] = pre_exp
        ranks = pd.concat([pre_exp.rank(ascending=False), s2["VAL_profit_factor"].rank(ascending=False),
                           s2["ALL_max_dd_pct"].rank(ascending=True),
                           s2["robust_expectancy_R"].rank(ascending=False),
                           s2["OOS_expectancy_R"].rank(ascending=False)], axis=1)
        s2["composite_rank"] = ranks.mean(axis=1)
        summary.loc[s2.index, "pre_oos_expectancy_R"] = s2["pre_oos_expectancy_R"]
        summary.loc[s2.index, "composite_rank"] = s2["composite_rank"]
        summary = summary.sort_values("composite_rank", na_position="last")

    out = {"summary": summary, "frozen": frozen_df, "cost_tabs": cost_tabs,
           "wf": pd.concat(wf_all, ignore_index=True) if wf_all else pd.DataFrame(),
           "all_cfg": pd.concat(rows_all_cfg, ignore_index=True) if rows_all_cfg else pd.DataFrame(),
           "quality": quality, "excluded": bad, "sel_hash": sel_hash, "by_sym": by_sym}
    from .report import build_report
    build_report(cfg, out, synthetic)
    return out
