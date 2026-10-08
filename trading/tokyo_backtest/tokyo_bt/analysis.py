"""Monte Carlo, MAE/MFE, análisis por hora/día/volatilidad y correlaciones."""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats

from .metrics import r_metrics

DOW = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}


# ----------------------------------------------------------------------------
# Monte Carlo
# ----------------------------------------------------------------------------

def monte_carlo(R: np.ndarray, risk_pct: float, n_sims: int, ruin_dd_pct: float, seed: int) -> dict:
    """Dos variantes:
      * permutation: reordena las MISMAS operaciones (riesgo de secuencia: DD, rachas).
        El retorno final es idéntico en todas (la capitalización es conmutativa).
      * bootstrap: remuestrea con reposición (distribución del retorno esperado).
    Riesgo fijo % sobre equity actual => factor por operación (1 + risk * R).
    """
    R = np.asarray(R, float)
    n = len(R)
    if n < 10:
        return {"n_trades": n}
    rng = np.random.default_rng(seed)
    f = risk_pct / 100
    out = {"n_trades": n, "risk_pct": risk_pct, "n_sims": n_sims}
    for kind in ("permutation", "bootstrap"):
        if kind == "permutation":
            idx = np.argsort(rng.random((n_sims, n)), axis=1)
        else:
            idx = rng.integers(0, n, size=(n_sims, n))
        sims = R[idx]
        eq = np.cumprod(1 + f * sims, axis=1)
        eq = np.concatenate([np.ones((n_sims, 1)), eq], axis=1)
        peak = np.maximum.accumulate(eq, axis=1)
        dd = ((peak - eq) / peak).max(axis=1) * 100
        losing = sims < 0
        # racha perdedora máxima por simulación
        streak = np.zeros(n_sims, int)
        cur = np.zeros(n_sims, int)
        for j in range(n):
            cur = np.where(losing[:, j], cur + 1, 0)
            streak = np.maximum(streak, cur)
        ret = (eq[:, -1] - 1) * 100
        out[kind] = {
            "max_dd_median_pct": float(np.median(dd)), "max_dd_p95_pct": float(np.percentile(dd, 95)),
            "max_dd_p99_pct": float(np.percentile(dd, 99)), "max_dd_worst_pct": float(dd.max()),
            "worst_losing_streak": int(streak.max()), "losing_streak_p95": float(np.percentile(streak, 95)),
            "prob_ruin": float((dd >= ruin_dd_pct).mean()),
            "return_p05_pct": float(np.percentile(ret, 5)), "return_median_pct": float(np.median(ret)),
            "return_p95_pct": float(np.percentile(ret, 95)), "prob_loss": float((ret < 0).mean()),
            "_dd": dd, "_ret": ret}
    return out


# ----------------------------------------------------------------------------
# Agrupaciones
# ----------------------------------------------------------------------------

def _boot_ci(x, n=2000, seed=0):
    if len(x) < 5:
        return (np.nan, np.nan)
    rng = np.random.default_rng(seed)
    m = rng.choice(x, size=(n, len(x)), replace=True).mean(axis=1)
    return float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))


def by_group(t: pd.DataFrame, col: str, order=None) -> pd.DataFrame:
    rows = []
    keys = order if order is not None else sorted(t[col].dropna().unique())
    for k in keys:
        r = t.loc[t[col] == k, "R"].values
        m = r_metrics(r)
        lo, hi = _boot_ci(r)
        rows.append({col: k, "trades": len(r), "win_rate": m.get("win_rate", np.nan),
                     "expectancy_R": m.get("expectancy_R", np.nan), "ci95_lo": lo, "ci95_hi": hi,
                     "profit_factor": m.get("profit_factor", np.nan), "average_R": m.get("expectancy_R", np.nan),
                     "max_dd_R": m.get("max_dd_R", np.nan), "net_R": m.get("net_R", 0.0)})
    df = pd.DataFrame(rows)
    groups = [t.loc[t[col] == k, "R"].values for k in keys]
    groups = [g for g in groups if len(g) >= 5]
    p = stats.kruskal(*groups).pvalue if len(groups) >= 2 else np.nan
    df.attrs["kruskal_p"] = float(p)
    return df


def hour_table(t):
    return by_group(t, "hour_utc", order=list(range(0, 9)))


def dow_table(t):
    tt = t.assign(day=t["dow"].map(DOW))
    return by_group(tt, "day", order=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])


def vol_table(t):
    return by_group(t, "vol_regime", order=["low", "medium", "high", "unclassified"])


# ----------------------------------------------------------------------------
# MAE / MFE
# ----------------------------------------------------------------------------

def mae_mfe(t: pd.DataFrame) -> dict:
    w, l = t[t["R"] > 0], t[t["R"] <= 0]
    out = {
        "mae_R_winners_mean": float(w["mae_R"].mean()), "mae_R_losers_mean": float(l["mae_R"].mean()),
        "mfe_R_mean": float(t["mfe_R"].mean()), "mfe_R_winners_mean": float(w["mfe_R"].mean()),
        "mfe_R_losers_mean": float(l["mfe_R"].mean()),
        "mfe_R_pctiles": {p: float(np.nanpercentile(t["mfe_R"], p)) for p in (25, 50, 75, 90)},
        "winners_mae_gt_0.8R_share": float((w["mae_R"] > 0.8).mean()) if len(w) else np.nan,
        "losers_mfe_ge_1R_share": float((l["mfe_R"] >= 1).mean()) if len(l) else np.nan,
        "losers_mfe_ge_0.5R_share": float((l["mfe_R"] >= 0.5).mean()) if len(l) else np.nan,
    }
    # diagnóstico
    notes = []
    if out["winners_mae_gt_0.8R_share"] > 0.25:
        notes.append("Más del 25% de las ganadoras llegó cerca del stop (MAE>0.8R): el SL es ajustado; "
                     "un SL algo más amplio podría evitar stops prematuros (validar, no asumir).")
    if out["losers_mfe_ge_1R_share"] > 0.3:
        notes.append("Más del 30% de las perdedoras llegó a +1R antes de perder: TP o gestión (BE/parcial) "
                     "podrían capturar ese movimiento.")
    med = out["mfe_R_pctiles"][50]
    notes.append(f"La mediana de MFE es {med:.2f}R: targets muy por encima de ~{out['mfe_R_pctiles'][75]:.2f}R "
                 "(p75) se alcanzan pocas veces.")
    out["notes"] = notes
    return out


def mfe_by(t, col):
    return t.groupby(col)["mfe_R"].agg(["count", "mean", "median"]).rename(columns={"count": "trades"})


# ----------------------------------------------------------------------------
# Correlaciones entre símbolos
# ----------------------------------------------------------------------------

def correlation(frozen_trades: pd.DataFrame, mid_session_returns: pd.DataFrame) -> dict:
    """frozen_trades: operaciones de las configuraciones congeladas (todas las estrategias).
    mid_session_returns: retorno mid de la sesión de Tokio por fecha (columnas = símbolos).

    Devuelve correlación de resultados diarios en R por estrategia, coincidencia de señales
    y número efectivo de apuestas independientes (por autovalores)."""
    out = {}
    if not mid_session_returns.empty:
        c = mid_session_returns.corr()
        out["session_return_corr"] = c
        out["session_return_n_eff"] = _n_eff(c)
    for strat, g in frozen_trades.groupby("strategy"):
        daily = g.pivot_table(index="date", columns="symbol", values="R", aggfunc="sum")
        if daily.shape[1] < 2:
            continue
        corr = daily.corr(min_periods=30)
        sig = g.assign(s=np.sign(g["direction"])).pivot_table(index="date", columns="symbol", values="s",
                                                              aggfunc="first")
        co = {}
        syms = list(sig.columns)
        for i, a in enumerate(syms):
            for b in syms[i + 1:]:
                both = sig[[a, b]].dropna()
                either = sig[[a, b]].notna().any(axis=1).sum()
                co[f"{a}~{b}"] = {"same_day_share": len(both) / either if either else np.nan,
                                  "same_direction_share": float((both[a] == both[b]).mean()) if len(both) else np.nan}
        out[strat] = {"daily_R_corr": corr, "cooccurrence": co,
                      "n_eff": _n_eff(corr.fillna(0).where(~np.eye(len(corr), dtype=bool), 1.0)),
                      "n_symbols": daily.shape[1]}
    return out


def _n_eff(c: pd.DataFrame) -> float:
    ev = np.linalg.eigvalsh(np.nan_to_num(c.values))
    ev = ev[ev > 0]
    return float(ev.sum() ** 2 / (ev ** 2).sum()) if len(ev) else np.nan
