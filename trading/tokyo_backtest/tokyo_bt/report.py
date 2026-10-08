"""Tablas CSV, trade log, gráficos y REPORT.md."""
from __future__ import annotations

import json

import numpy as np
import pandas as pd
from scipy import stats

from . import analysis as an
from . import charts as ch
from .config import resolve
from .metrics import equity_metrics, equity_sim, r_metrics
from .postprocess import load_news, news_mask, position_mask
from .research import parse_cid

TRADE_LOG_COLS = {
    "date": "Date", "entry_time": "Time", "symbol": "Symbol", "strategy": "Strategy", "direction": "Direction",
    "entry_fill": "Entry", "stop": "SL", "tp": "TP", "exit_fill": "Exit", "exit_reason_name": "Exit reason",
    "pnl_usd": "Profit $", "R": "Profit R", "mae_R": "MAE (R)", "mfe_R": "MFE (R)",
    "spread_at_signal": "Spread", "slippage_px": "Slippage", "atr": "ATR", "asian_high": "Asian High",
    "asian_low": "Asian Low", "asian_range": "Asian Range", "or_high": "OR High", "or_low": "OR Low",
    "or_range": "OR Range", "vwap": "VWAP", "day": "Day of week", "hour_utc": "Hour UTC",
}

AXIS_PAIRS = {
    "A": [("sl", "tp"), ("buffer_atr", "rf")],
    "B": [("min_sweep_atr", "exit"), ("stop_buffer_atr", "rf")],
    "C": [("or_minutes", "buffer_atr"), ("sl", "tp")],
    "D": [("or_minutes", "min_sweep_atr"), ("stop_buffer_atr", "exit")],
    "E": [("vwap_filter", "tp"), ("sl", "tp"), ("buffer_atr", "rf")],
}


def md_table(df: pd.DataFrame, floatfmt="{:.3f}", max_rows=60) -> str:
    if df is None or len(df) == 0:
        return "_(sin datos)_\n"
    d = df.head(max_rows)
    cols = list(d.columns)
    out = ["| " + " | ".join(str(c) for c in cols) + " |", "|" + "---|" * len(cols)]
    for _, r in d.iterrows():
        cells = []
        for c in cols:
            v = r[c]
            if isinstance(v, (float, np.floating)):
                if pd.isna(v):
                    cells.append("")
                elif np.isinf(v):
                    cells.append("inf")
                elif float(v).is_integer() and abs(v) >= 1 and c not in ("expectancy_R",):
                    cells.append(str(int(v)))
                else:
                    cells.append(floatfmt.format(v))
            else:
                cells.append(str(v).replace("|", "/"))
        out.append("| " + " | ".join(cells) + " |")
    return "\n".join(out) + "\n"


def _trade_log(ft: pd.DataFrame) -> pd.DataFrame:
    t = ft.copy()
    t["direction"] = np.where(t["direction"] > 0, "LONG", "SHORT")
    is_or = t["strategy"].str[0].isin(["C", "D"])
    for a, b in (("asian_high", "range_hi"), ("asian_low", "range_lo"), ("asian_range", "range")):
        t[a] = np.where(~is_or, t[b], np.nan)
    for a, b in (("or_high", "range_hi"), ("or_low", "range_lo"), ("or_range", "range")):
        t[a] = np.where(is_or, t[b], np.nan)
    t["day"] = t["entry_time"].dt.day_name()
    t["date"] = t["entry_time"].dt.date
    t["entry_time"] = t["entry_time"].dt.strftime("%H:%M")
    cols = [c for c in TRADE_LOG_COLS if c in t.columns]
    out = t[cols].rename(columns=TRADE_LOG_COLS)
    extra = [c for c in ("cid", "segment", "vol_regime", "range_atr", "breakout_dist_atr", "sweep_depth_atr",
                         "minutes_outside", "dist_to_mid_atr", "or_minutes", "lots", "exit_time")
             if c in t.columns]
    return pd.concat([out, t[extra]], axis=1)


def build_report(cfg: dict, res: dict, synthetic: bool):
    out = resolve(cfg, cfg["project"]["output_dir"])
    tdir, cdir, ldir = out / "tables", out / "charts", out / "trade_log"
    for d in (tdir, cdir, ldir):
        d.mkdir(parents=True, exist_ok=True)
    initial = cfg["project"]["initial_equity"]
    specs = cfg["instruments"]
    summary, frozen, all_cfg = res["summary"], res["frozen"], res["all_cfg"]
    mm = cfg["money_management"]
    min_tr = cfg["selection"]["min_trades_is"]
    md = []
    banner = ("> **ADVERTENCIA: DATOS SINTÉTICOS.** Este reporte se generó con datos aleatorios para probar el "
              "software. Ninguna cifra es un resultado de mercado.\n\n" if synthetic else "")
    md.append("# Tokyo Session Backtest — reporte\n\n" + banner)
    md.append(f"Selección congelada: `selection.json` (hash `{res['sel_hash']}`). El OOS se midió después de "
              "congelarla y no se usó para elegir ningún parámetro.\n")

    # ------------------------------------------------------------------ datos
    md.append("## 0. Datos verificados\n")
    q = pd.DataFrame([{"symbol": s, "status": r["status"], "first": r.get("first"), "last": r.get("last"),
                       "years": r.get("years"), "tf": r.get("timeframe"), "bid_ask": r.get("has_bid_ask"),
                       "volume": r.get("has_volume"), "spread": r.get("spread_source")}
                      for s, r in res["quality"].items()])
    md.append(md_table(q))
    if res["excluded"]:
        md.append("**Símbolos excluidos:**\n" + "\n".join(f"- {s}: {'; '.join(m)}" for s, m in res["excluded"].items()) + "\n")
    md.append("Detalle completo en `data_quality.md`.\n")

    if len(frozen) == 0:
        (out / "REPORT.md").write_text("\n".join(md) + "\n\nNo hubo configuraciones elegibles.\n", encoding="utf-8")
        return

    # ------------------------------------------------------------------ capital (pnl $) para trade log
    frozen = frozen.copy()
    parts = []
    for cid, g in frozen.groupby("cid", sort=False):
        es = equity_sim(g, initial, "risk", 0.5, specs=specs)
        parts.append(es)
    frozen = pd.concat(parts, ignore_index=True).sort_values("entry_time").reset_index(drop=True)
    _trade_log(frozen).to_csv(ldir / "frozen_trades.csv", index=False)

    # ------------------------------------------------------------------ resumen y rankings
    summary.to_csv(tdir / "summary.csv", index=False)
    all_cfg.to_csv(tdir / "all_configurations.csv.gz", index=False, compression="gzip")
    ok = summary[summary["status"] == "OK"].copy()
    final = pd.DataFrame({
        "Strategy": ok["strategy"], "Asset": ok["symbol"], "Timeframe": ok["timeframe"],
        "Trades (OOS)": ok["OOS_trades"], "Win Rate (OOS)": ok["OOS_win_rate"],
        "PF (OOS)": ok["OOS_profit_factor"], "Expectancy R (OOS)": ok["OOS_expectancy_R"],
        "Expectancy R (pre-OOS)": ok["pre_oos_expectancy_R"],
        "Net Return % (todo, 0.5%)": ok["ALL_net_return_pct"], "Max DD % (todo)": ok["ALL_max_dd_pct"],
        "Sharpe": ok["ALL_sharpe"], "Sortino": ok["ALL_sortino"], "Average R": ok["ALL_average_R"],
        "Best parameter region": ok["best_region"], "Worst parameter region": ok["worst_region"],
        "Veredicto": ok["verdict"], "Flags": (ok["fragile"].fillna("") + " " + ok.get("cost_flag", "").fillna("")).str.strip()})
    final.to_csv(tdir / "final_table.csv", index=False)
    md.append("## 1. Tabla final (configuración congelada por estrategia + activo)\n")
    md.append("Orden: rango compuesto de (1) expectancy pre-OOS, (2) profit factor VAL, (3) max DD, "
              "(4) robustez de vecindario, (5) expectancy OOS. No se ordena por beneficio neto.\n")
    md.append(md_table(final))

    by_strat = ok.groupby("strategy").agg(pairs=("symbol", "count"), oos_exp_mean=("OOS_expectancy_R", "mean"),
                                          oos_positive=("OOS_expectancy_R", lambda x: int((x > 0).sum())),
                                          val_exp_mean=("VAL_expectancy_R", "mean"),
                                          robust=("verdict", lambda v: int(v.str.startswith("CANDIDATA").sum()))) \
        .sort_values("oos_exp_mean", ascending=False)
    by_asset = ok.groupby("symbol").agg(strategies=("strategy", "count"), oos_exp_mean=("OOS_expectancy_R", "mean"),
                                        oos_positive=("OOS_expectancy_R", lambda x: int((x > 0).sum())),
                                        val_exp_mean=("VAL_expectancy_R", "mean")) \
        .sort_values("oos_exp_mean", ascending=False)
    by_strat.to_csv(tdir / "ranking_strategy.csv")
    by_asset.to_csv(tdir / "ranking_asset.csv")
    md.append("## 2. Ranking por estrategia\n" + md_table(by_strat.reset_index()))
    md.append("## 3. Ranking por activo\n" + md_table(by_asset.reset_index()))
    combo = ok[["strategy", "symbol", "composite_rank", "pre_oos_expectancy_R", "VAL_profit_factor",
                "ALL_max_dd_pct", "robust_expectancy_R", "OOS_expectancy_R", "verdict"]]
    md.append("## 4. Ranking estrategia + activo\n" + md_table(combo))

    # ------------------------------------------------------------------ parámetros robustos / top10
    md.append("## 5. Parámetros robustos y TOP 10 por categoría\n")
    md.append(md_table(ok[["strategy", "symbol", "cid", "robust_expectancy_R", "neighbor_positive_share",
                           "n_configs_tested", "bh_significant_is", "dsr_is"]]))
    md.append("`bh_significant_is` = configuraciones de la grilla con expectancy > 0 significativa tras "
              "Benjamini-Hochberg (q=0.05). `dsr_is` = Deflated Sharpe Ratio de la elegida (prob. de Sharpe "
              "real > 0 corrigiendo por la cantidad de pruebas).\n")
    if len(all_cfg):
        ac = all_cfg.copy()
        ac["pre_net_R"] = ac["is_expectancy_R"] * ac["is_trades"] + ac["val_expectancy_R"].fillna(0) * ac["val_trades"].fillna(0)
        ac["pre_dd_R"] = np.maximum(ac["is_max_dd_R"], ac["val_max_dd_R"].fillna(0))
        ac["risk_return"] = ac["pre_net_R"] / ac["pre_dd_R"].replace(0, np.nan)
        elig = ac["is_trades"] >= min_tr
        cats = {
            "A_best_IS": ac[elig].sort_values("is_expectancy_R", ascending=False),
            "B_best_VALIDATION": ac[ac["val_trades"] >= min_tr / 3].sort_values("val_expectancy_R", ascending=False),
            "C_best_OOS_solo_informativo": ac[ac["oos_trades"] >= min_tr / 3].sort_values("oos_expectancy_R", ascending=False),
            "D_best_ROBUSTA": ac[elig & (ac["is_neighbor_positive_share"] >= 0.75) & (ac["val_expectancy_R"] > 0)]
            .sort_values("is_robust_expectancy_R", ascending=False),
            "E_best_riesgo_retorno": ac[elig & (ac["val_expectancy_R"] > 0)].sort_values("risk_return", ascending=False),
            "F_best_ejecucion_automatica": ac[elig & (ac["is_neighbor_positive_share"] >= 0.75) &
                                              (ac["val_expectancy_R"] > 0) & ~ac["cid"].str.contains("trail_swing")]
            .assign(score=lambda d: d["is_robust_expectancy_R"] * np.sqrt(d["is_trades"]))
            .sort_values("score", ascending=False),
        }
        show = ["strategy", "symbol", "cid", "is_trades", "is_expectancy_R", "is_robust_expectancy_R",
                "is_profit_factor", "val_expectancy_R", "oos_expectancy_R"]
        for name, d in cats.items():
            d.head(10)[show].to_csv(tdir / f"top10_{name}.csv", index=False)
            md.append(f"### {name}\n" + md_table(d.head(10)[show]))
        md.append("Si A (mejor IS) no coincide con D (mejor robusta) y su OOS es peor, eso es evidencia "
                  "directa de sobreoptimización. C es sólo informativo: elegir por C sería look-ahead.\n")

    # ------------------------------------------------------------------ OOS
    md.append("## 6. Resultados OUT-OF-SAMPLE de la selección congelada\n")
    md.append(md_table(ok[["strategy", "symbol", "IS_trades", "IS_expectancy_R", "VAL_trades", "VAL_expectancy_R",
                           "OOS_trades", "OOS_win_rate", "OOS_expectancy_R", "OOS_profit_factor",
                           "OOS_net_return_pct", "OOS_max_dd_pct", "OOS_sharpe"]]))

    # ------------------------------------------------------------------ walk-forward
    wf = res["wf"]
    wf.to_csv(tdir / "walk_forward.csv", index=False)
    md.append("## 7. Walk-forward (sólo período pre-OOS)\n")
    if len(wf):
        agg = wf.groupby(["strategy", "symbol"]).agg(
            windows=("test_start", "count"),
            wf_positive=("wf_test_net_R", lambda x: float((x > 0).mean())),
            wf_net_R=("wf_test_net_R", "sum"), final_net_R=("final_test_net_R", "sum"),
            distinct_cfgs=("selected_cfg", "nunique")).reset_index()
        md.append(md_table(agg))
        md.append("`distinct_cfgs` alto = la configuración óptima cambia de ventana en ventana (inestable).\n")
        for (s, y), g in wf.groupby(["strategy", "symbol"]):
            ch.walk_forward_chart(g, f"Walk-forward {s} {y}", cdir / f"wf_{s}_{y}.png", synthetic)

    # ------------------------------------------------------------------ Monte Carlo
    md.append("## 8. Monte Carlo (10.000 simulaciones) y drawdown\n")
    top = ok.sort_values("composite_rank").head(cfg["monte_carlo"]["top_n_configs"])
    mc_rows = []
    for r in top.itertuples():
        R = frozen.loc[frozen["cid"] == r.cid, "R"].values
        for risk in mm["risk_pct"]:
            res_mc = an.monte_carlo(R, risk, cfg["monte_carlo"]["n_sims"], mm["ruin_drawdown_pct"],
                                    cfg["project"]["seed"])
            if "permutation" not in res_mc:
                continue
            p, b = res_mc["permutation"], res_mc["bootstrap"]
            mc_rows.append({"strategy": r.strategy, "symbol": r.symbol, "risk_pct": risk, "trades": len(R),
                            "maxDD_median": p["max_dd_median_pct"], "maxDD_p95": p["max_dd_p95_pct"],
                            "maxDD_p99": p["max_dd_p99_pct"], "worst_losing_streak": p["worst_losing_streak"],
                            "prob_ruin": p["prob_ruin"], "boot_prob_ruin": b["prob_ruin"],
                            "return_p05": b["return_p05_pct"], "return_median": b["return_median_pct"],
                            "return_p95": b["return_p95_pct"], "prob_loss": b["prob_loss"]})
            if risk == 0.5 and r.Index in top.index[:3]:
                ch.histogram(p["_dd"], f"MC max drawdown {r.strategy} {r.symbol} (0.5%)", "max drawdown %",
                             cdir / f"mc_dd_{r.strategy}_{r.symbol}.png", synthetic,
                             {"p95": p["max_dd_p95_pct"], "p99": p["max_dd_p99_pct"]}, color=ch.NEG)
                ch.histogram(b["_ret"], f"MC retorno (bootstrap) {r.strategy} {r.symbol} (0.5%)", "retorno %",
                             cdir / f"mc_ret_{r.strategy}_{r.symbol}.png", synthetic,
                             {"p05": b["return_p05_pct"], "mediana": b["return_median_pct"]})
    mc = pd.DataFrame(mc_rows)
    mc.to_csv(tdir / "monte_carlo.csv", index=False)
    md.append(md_table(mc))
    md.append("Permutación: mismas operaciones reordenadas (riesgo de secuencia). Bootstrap: remuestreo con "
              "reposición (distribución del retorno). Ruina = drawdown >= "
              f"{mm['ruin_drawdown_pct']}%.\n")

    # gestión de capital y lotaje fijo
    mm_rows = []
    for r in ok.itertuples():
        g = frozen[frozen["cid"] == r.cid]
        bnd = res["by_sym"][r.symbol]["bounds"]
        for mode, lvl in [("risk", x) for x in mm["risk_pct"]] + [("fixed", mm["fixed_lot"])]:
            es = equity_sim(g, initial, mode, lvl if mode == "risk" else 0, fixed_lot=mm["fixed_lot"], specs=specs)
            em = equity_metrics(es, initial, bnd["start"], bnd["end"])
            mm_rows.append({"strategy": r.strategy, "symbol": r.symbol,
                            "sizing": f"riesgo {lvl}%" if mode == "risk" else f"lote fijo {lvl}", **em})
        es = equity_sim(g, initial, "risk", 0.5, specs=specs)
        eq = pd.Series(es["equity"].values, index=es["exit_time"])
        ch.equity_drawdown(eq, f"{r.strategy} {r.symbol} (riesgo 0.5%)",
                           cdir / f"equity_{r.strategy}_{r.symbol}.png", synthetic,
                           {"VAL": bnd["is_end"], "OOS": bnd["val_end"]})
        monthly = eq.resample("ME").last().ffill()
        mret = monthly.pct_change().fillna(monthly.iloc[0] / initial - 1) * 100 if len(monthly) else monthly
        yearly = eq.resample("YE").last().ffill()
        yret = yearly.pct_change().fillna(yearly.iloc[0] / initial - 1) * 100 if len(yearly) else yearly
        if r.Index in top.index[:3]:
            ch.bar_by_period(mret.rename(lambda d: d.strftime("%Y-%m")), f"Retorno mensual {r.strategy} {r.symbol}",
                             "%", cdir / f"monthly_{r.strategy}_{r.symbol}.png", synthetic)
            ch.bar_by_period(yret.rename(lambda d: d.year), f"Retorno anual {r.strategy} {r.symbol}", "%",
                             cdir / f"yearly_{r.strategy}_{r.symbol}.png", synthetic)
    mmdf = pd.DataFrame(mm_rows)
    mmdf.to_csv(tdir / "money_management.csv", index=False)
    md.append("### Gestión de capital (todo el período)\n")
    md.append(md_table(mmdf[["strategy", "symbol", "sizing", "trades", "net_return_pct", "cagr_pct", "max_dd_pct",
                             "avg_dd_pct", "sharpe", "sortino", "calmar", "recovery_factor", "profit_factor",
                             "max_consec_losses", "skipped_unsizable"]]))

    # ------------------------------------------------------------------ MAE / MFE
    md.append("## 9. MAE / MFE (en R)\n")
    mm_all = an.mae_mfe(frozen)
    json.dump({k: v for k, v in mm_all.items()}, open(tdir / "mae_mfe.json", "w"), indent=2, default=float)
    md.append(md_table(pd.DataFrame([{k: v for k, v in mm_all.items() if not isinstance(v, (dict, list))}])))
    md.append("\n".join(f"- {n}" for n in mm_all["notes"]) + "\n")
    per_pair = []
    for (s, y), g in frozen.groupby(["strategy", "symbol"]):
        d = an.mae_mfe(g)
        per_pair.append({"strategy": s, "symbol": y, **{k: v for k, v in d.items() if not isinstance(v, (dict, list))},
                         "mfe_p50": d["mfe_R_pctiles"][50], "mfe_p75": d["mfe_R_pctiles"][75]})
    md.append(md_table(pd.DataFrame(per_pair)))
    for col in ("symbol", "hour_utc", "strategy"):
        an.mfe_by(frozen, col).to_csv(tdir / f"mfe_by_{col}.csv")
    ch.histogram(frozen["R"], "Distribución de resultados (configs congeladas)", "R por operación",
                 cdir / "profit_distribution.png", synthetic, {"0": 0})
    ch.histogram(frozen["mae_R"], "Distribución MAE", "MAE (R)", cdir / "mae_distribution.png", synthetic,
                 {"1R": 1}, color=ch.NEG)
    ch.histogram(frozen["mfe_R"], "Distribución MFE", "MFE (R)", cdir / "mfe_distribution.png", synthetic, {"1R": 1})

    # ------------------------------------------------------------------ hora / día / volatilidad
    md.append("## 9b. Hora UTC, día y volatilidad\n")
    frozen["pair"] = frozen["strategy"].str[:1] + "·" + frozen["symbol"]
    h = an.hour_table(frozen)
    d = an.dow_table(frozen)
    v = an.vol_table(frozen)
    for name, tab in (("by_hour", h), ("by_day", d), ("by_volatility", v)):
        tab.to_csv(tdir / f"{name}.csv", index=False)
        md.append(f"### {name} (Kruskal-Wallis p = {tab.attrs.get('kruskal_p', np.nan):.4f})\n" + md_table(tab))
    md.append("p > 0.05 => no hay evidencia de que la hora/día/régimen cambie el resultado; no filtrar por eso.\n")
    hm = frozen.pivot_table(index="pair", columns="hour_utc", values="R", aggfunc="mean").reindex(columns=range(9))
    hc = frozen.pivot_table(index="pair", columns="hour_utc", values="R", aggfunc="count").reindex(columns=range(9))
    ch.heatmap(hm, "Expectancy por hora de entrada (UTC)", cdir / "heatmap_hour.png", synthetic, counts=hc, min_count=10)
    dm = frozen.assign(day=frozen["dow"].map(an.DOW)).pivot_table(index="pair", columns="day", values="R", aggfunc="mean")
    dm = dm.reindex(columns=[c for c in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"] if c in dm.columns])
    dc = frozen.assign(day=frozen["dow"].map(an.DOW)).pivot_table(index="pair", columns="day", values="R", aggfunc="count")
    ch.heatmap(dm, "Expectancy por día", cdir / "heatmap_day.png", synthetic, counts=dc, min_count=10)

    # ------------------------------------------------------------------ heatmaps de parámetros
    if len(all_cfg):
        for (s, y), g in all_cfg.groupby(["strategy", "symbol"]):
            p = pd.DataFrame([parse_cid(c) for c in g["cid"]], index=g.index)
            for ax1, ax2 in AXIS_PAIRS.get(s[0], []):
                if ax1 not in p or ax2 not in p or p[ax1].nunique() < 2 or p[ax2].nunique() < 2:
                    continue
                gg = g[g["is_trades"] >= min_tr / 2]
                if gg.empty:
                    continue
                piv = gg.assign(a=p[ax1], b=p[ax2]).pivot_table(index="a", columns="b", values="is_expectancy_R",
                                                                 aggfunc="median")
                ch.heatmap(piv, f"{s} {y}: expectancy IS (mediana sobre el resto) {ax1} x {ax2}",
                           cdir / f"param_{s}_{y}_{ax1}_x_{ax2}.png", synthetic)

    # performance por activo / estrategia
    ch.hbar(ok.groupby("symbol")["OOS_expectancy_R"].mean(), "Expectancy OOS media por activo (configs congeladas)",
            "R", cdir / "performance_by_asset.png", synthetic)
    ch.hbar(ok.groupby("strategy")["OOS_expectancy_R"].mean(), "Expectancy OOS media por estrategia",
            "R", cdir / "performance_by_strategy.png", synthetic)

    # ------------------------------------------------------------------ costos
    md.append("## 10. Sensibilidad a costos\n")
    ct = []
    for (s, y), tab in res["cost_tabs"].items():
        ct.append(tab.assign(strategy=s, symbol=y))
    if ct:
        ctd = pd.concat(ct, ignore_index=True)
        ctd.to_csv(tdir / "cost_sensitivity.csv", index=False)
        piv = ctd[ctd["segment"] == "pre_OOS"].pivot_table(index=["strategy", "symbol"],
                                                           columns=["spread_mult", "slippage_mult"],
                                                           values="expectancy_R")
        piv.columns = [f"sp{a:g}/sl{b:g}" for a, b in piv.columns]
        md.append(md_table(piv.reset_index()))
        md.append("Expectancy (R) pre-OOS por multiplicador de spread / slippage. "
                  "Si se vuelve <= 0 con spread x1.5 o slippage x2 la estrategia se marca NO ROBUSTA.\n")
    else:
        md.append("_(no ejecutada)_\n")

    # ------------------------------------------------------------------ modos de posición, noticias, VWAP
    md.append("## 10b. Restricciones operativas (portafolio por estrategia, todos los activos)\n")
    pm_rows = []
    for strat, g in frozen.groupby("strategy"):
        g = g.sort_values("entry_time")
        for m in cfg["position_modes"]:
            keep = position_mask(g.assign(pf="all"), ["pf"], m["max_per_session"], m["single_position"])
            r = r_metrics(g.loc[keep, "R"].values)
            pm_rows.append({"strategy": strat, "mode": m["name"], **{k: r.get(k) for k in
                            ("trades", "win_rate", "expectancy_R", "profit_factor", "max_dd_R", "net_R")}})
    pm = pd.DataFrame(pm_rows)
    pm.to_csv(tdir / "position_modes.csv", index=False)
    md.append(md_table(pm))

    md.append("## 10c. Filtro de noticias\n")
    news = load_news(cfg)
    if news is None:
        md.append("No se proporcionó calendario (`data/news/calendar.csv`): comparación NO realizada. "
                  "No se asume que el filtro mejore el sistema.\n")
    else:
        nm = news_mask(frozen, news, cfg)
        rows = []
        for (s, y), idx in frozen.groupby(["strategy", "symbol"]).groups.items():
            sub = frozen.loc[idx]
            msk = nm[frozen.index.get_indexer(idx)]
            a, b = r_metrics(sub["R"].values), r_metrics(sub.loc[~msk, "R"].values)
            rows.append({"strategy": s, "symbol": y, "trades_all": a.get("trades"), "exp_all": a.get("expectancy_R"),
                         "trades_sin_noticias": b.get("trades"), "exp_sin_noticias": b.get("expectancy_R"),
                         "trades_en_noticias": int(msk.sum()),
                         "exp_en_noticias": sub.loc[msk, "R"].mean() if msk.any() else np.nan})
        nd = pd.DataFrame(rows)
        nd.to_csv(tdir / "news_filter.csv", index=False)
        md.append(md_table(nd))

    md.append("## 10d. ¿VWAP mejora el expectancy? (estrategia E)\n")
    e = all_cfg[all_cfg["strategy"].str.startswith("E_")] if len(all_cfg) else pd.DataFrame()
    if len(e):
        e = e.assign(base=e["cid"].str.replace(r"vwap_filter=(True|False)\|?", "", regex=True),
                     vf=e["cid"].str.contains("vwap_filter=True"))
        rows = []
        for (sym), g in e.groupby("symbol"):
            w = g[g["vf"]].set_index("base")
            wo = g[~g["vf"]].set_index("base")
            common = w.index.intersection(wo.index)
            for seg in ("is", "val", "oos"):
                dlt = (w.loc[common, f"{seg}_expectancy_R"] - wo.loc[common, f"{seg}_expectancy_R"]).dropna()
                p = stats.wilcoxon(dlt).pvalue if len(dlt) >= 10 and (dlt != 0).any() else np.nan
                rows.append({"symbol": sym, "segment": seg.upper(), "pares": len(dlt),
                             "delta_expectancy_media": dlt.mean(), "share_mejora": (dlt > 0).mean(),
                             "wilcoxon_p": p})
        vd = pd.DataFrame(rows)
        vd.to_csv(tdir / "vwap_test.csv", index=False)
        md.append(md_table(vd))
        md.append("delta = expectancy con VWAP - sin VWAP para la misma configuración. Sólo se considera que VWAP "
                  "mejora si el delta es positivo en IS **y** VAL **y** OOS y p < 0.05.\n")
    else:
        md.append("Estrategia E no evaluada (sin volumen o deshabilitada).\n")

    # ------------------------------------------------------------------ correlación
    md.append("## 11. Correlación e independencia de señales\n")
    sret = pd.DataFrame({s: r["session_ret"] for s, r in res["by_sym"].items()})
    corr = an.correlation(frozen, sret)
    if "session_return_corr" in corr:
        corr["session_return_corr"].to_csv(tdir / "corr_session_returns.csv")
        md.append(f"Correlación de retornos de la sesión de Tokio (N efectivo = "
                  f"{corr['session_return_n_eff']:.2f} de {sret.shape[1]} activos):\n")
        md.append(md_table(corr["session_return_corr"].reset_index()))
        ch.heatmap(corr["session_return_corr"], "Correlación retornos sesión Tokio", cdir / "corr_session.png",
                   synthetic, cbar_label="correlación")
    for strat, c in corr.items():
        if strat.startswith("session"):
            continue
        c["daily_R_corr"].to_csv(tdir / f"corr_R_{strat}.csv")
        md.append(f"### {strat}: N efectivo de apuestas = {c['n_eff']:.2f} de {c['n_symbols']} activos\n")
        md.append(md_table(pd.DataFrame(c["cooccurrence"]).T.reset_index().rename(columns={"index": "par"})))
    md.append("Señales del mismo día y misma dirección en pares JPY correlacionados NO son oportunidades "
              "independientes: el tamaño de muestra efectivo es el N efectivo, no la suma de operaciones.\n")

    # ------------------------------------------------------------------ conclusión
    md.append("## 12. Conclusión objetiva\n")
    cands = ok[ok["verdict"].str.startswith("CANDIDATA")]
    if len(cands):
        md.append("Combinaciones que pasan TODOS los filtros (IS, VAL y OOS positivos, PF OOS > 1.1, no frágil, "
                  "robusta a costos, DSR > 0.95):\n")
        md.append(md_table(cands[["strategy", "symbol", "cid", "OOS_expectancy_R", "OOS_profit_factor",
                                  "ALL_max_dd_pct"]]))
        md.append("Aun así: el siguiente paso es forward test en demo con el broker real antes de arriesgar capital.\n")
    else:
        md.append("**Ninguna combinación estrategia + activo mostró una ventaja estadística robusta** con los "
                  "criterios definidos. No se recomienda operar ninguna con dinero real.\n")
    md.append(md_table(summary[["strategy", "symbol", "verdict"]]))
    md.append("\n### Sesgos revisados\n"
              "- Look-ahead: rangos y ATR sólo con barras cerradas; entrada en la barra siguiente; trailing aplica "
              "desde la barra siguiente; régimen de volatilidad con percentiles del pasado.\n"
              "- Data mining / selección: se reporta la cantidad de configuraciones probadas, BH-FDR y Deflated Sharpe; "
              "la elección usa vecindarios, no el máximo.\n"
              "- Overfitting / sensibilidad: heatmaps de parámetros (mediana sobre el resto) y vecinos positivos.\n"
              "- Régimen: % del beneficio en un año y ventanas WF positivas (marca FRÁGIL).\n"
              "- Survivorship: los símbolos se fijaron a priori (no se eligieron por desempeño). Un CFD de índice "
              "basado en futuros puede tener saltos de roll: ver outliers en data_quality.md.\n"
              "- Intrabarra: SL primero ante ambigüedad; resultados con M5 son menos precisos que con M1.\n")
    (out / "REPORT.md").write_text("\n".join(md), encoding="utf-8")
