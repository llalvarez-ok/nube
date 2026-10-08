"""Métricas en R (para comparar configuraciones) y sobre equity (para gestión de capital)."""
from __future__ import annotations

import heapq
import math

import numpy as np
import pandas as pd
from scipy import stats


def streaks(x: np.ndarray):
    """(máx. ganadoras consecutivas, máx. perdedoras consecutivas)."""
    best_w = best_l = cw = cl = 0
    for v in x:
        if v > 0:
            cw, cl = cw + 1, 0
        elif v < 0:
            cl, cw = cl + 1, 0
        else:
            cw = cl = 0
        best_w, best_l = max(best_w, cw), max(best_l, cl)
    return best_w, best_l


def max_dd_R(r: np.ndarray) -> float:
    if len(r) == 0:
        return 0.0
    eq = np.concatenate([[0.0], np.cumsum(r)])
    return float(np.max(np.maximum.accumulate(eq) - eq))


def r_metrics(r: np.ndarray, dates=None) -> dict:
    """Métricas en unidades de R (independientes del tamaño de posición)."""
    r = np.asarray(r, float)
    n = len(r)
    if n == 0:
        return {"trades": 0}
    wins, losses = r[r > 0], r[r < 0]
    gp, gl = wins.sum(), -losses.sum()
    sd = r.std(ddof=1) if n > 1 else np.nan
    t = r.mean() / (sd / math.sqrt(n)) if n > 1 and sd > 0 else np.nan
    w, l = streaks(r)
    out = {"trades": n, "win_rate": len(wins) / n, "expectancy_R": r.mean(), "net_R": r.sum(),
           "gross_profit_R": gp, "gross_loss_R": gl, "profit_factor": gp / gl if gl > 0 else np.inf,
           "avg_winner_R": wins.mean() if len(wins) else 0.0, "avg_loser_R": losses.mean() if len(losses) else 0.0,
           "max_dd_R": max_dd_R(r), "max_consec_wins": w, "max_consec_losses": l,
           "sharpe_per_trade": r.mean() / sd if sd and sd > 0 else np.nan, "t_stat": t,
           "p_value": float(stats.t.sf(t, n - 1)) if not np.isnan(t) else np.nan}
    out["return_dd_R"] = out["net_R"] / out["max_dd_R"] if out["max_dd_R"] > 0 else np.inf
    return out


def fast_group_metrics(df: pd.DataFrame, key: str, rcol="R") -> pd.DataFrame:
    """Métricas en R por configuración (vectorizado). df ordenado por entry_time."""
    g = df.groupby(key, sort=False)[rcol]
    out = pd.DataFrame({"trades": g.size(), "expectancy_R": g.mean(), "net_R": g.sum(),
                        "sd_R": g.std(ddof=1)})
    pos = df[rcol].clip(lower=0).groupby(df[key]).sum()
    neg = (-df[rcol].clip(upper=0)).groupby(df[key]).sum()
    out["profit_factor"] = pos / neg.replace(0, np.nan)
    out["win_rate"] = (df[rcol] > 0).groupby(df[key]).mean()
    cum = g.cumsum()
    peak = cum.groupby(df[key]).cummax().clip(lower=0)
    out["max_dd_R"] = (peak - cum).groupby(df[key]).max()
    out["t_stat"] = out["expectancy_R"] / (out["sd_R"] / np.sqrt(out["trades"]))
    out["p_value"] = stats.t.sf(out["t_stat"].fillna(0), (out["trades"] - 1).clip(lower=1))
    out["return_dd_R"] = out["net_R"] / out["max_dd_R"].replace(0, np.nan)
    return out


# ----------------------------------------------------------------------------
# Simulación de equity
# ----------------------------------------------------------------------------

def equity_sim(trades: pd.DataFrame, initial: float, mode: str = "risk", risk_pct: float = 0.5,
               fixed_lot: float = 0.1, specs: dict | None = None) -> pd.DataFrame:
    """Simula la cuenta. mode='risk': riesgo % sobre equity ACTUAL (sólo PnL cerrado al
    momento de la entrada); mode='fixed': lotaje fijo.

    Requiere columnas: symbol, entry_time, exit_time, rdist, pnl_px, comm_px, swap_px, conv.
    """
    t = trades.sort_values("entry_time").reset_index(drop=True)
    eq_closed = initial
    pending = []          # heap (exit_time, idx, pnl)
    pnl_usd = np.zeros(len(t))
    lots_arr = np.zeros(len(t))
    eq_at_entry = np.zeros(len(t))
    for i, row in enumerate(t.itertuples(index=False)):
        while pending and pending[0][0] <= row.entry_time:
            _, _, p = heapq.heappop(pending)
            eq_closed += p
        spec = specs[row.symbol]
        unit_usd = spec["contract_size"] * row.conv          # USD por 1.0 de precio por lote
        if mode == "risk":
            raw = eq_closed * risk_pct / 100 / (row.rdist * unit_usd)
            lots = math.floor(raw / spec["lot_step"] + 1e-9) * spec["lot_step"]
            if lots < spec["min_lot"]:
                lots = 0.0                                  # no se puede dimensionar: se omite
        else:
            lots = fixed_lot
        p = lots * unit_usd * (row.pnl_px + row.swap_px - row.comm_px)
        pnl_usd[i], lots_arr[i], eq_at_entry[i] = p, lots, eq_closed
        heapq.heappush(pending, (row.exit_time, i, p))
    t["lots"], t["pnl_usd"], t["equity_at_entry"] = lots_arr, pnl_usd, eq_at_entry
    t = t.sort_values("exit_time").reset_index(drop=True)
    t["equity"] = initial + t["pnl_usd"].cumsum()
    return t


def equity_metrics(t: pd.DataFrame, initial: float, start: pd.Timestamp, end: pd.Timestamp) -> dict:
    """Métricas de cuenta a partir de la salida de equity_sim."""
    if len(t) == 0:
        return {"trades": 0}
    t = t[t["lots"] > 0]
    pnl = t["pnl_usd"].values
    eq = pd.Series(np.concatenate([[initial], initial + np.cumsum(pnl)]),
                   index=pd.DatetimeIndex([start]).append(pd.DatetimeIndex(t["exit_time"])))
    peak = eq.cummax()
    dd = (peak - eq) / peak
    # episodios de drawdown
    in_dd = dd > 0
    episodes = (in_dd != in_dd.shift()).cumsum()[in_dd]
    ep_depth = dd[in_dd].groupby(episodes).max() if in_dd.any() else pd.Series(dtype=float)
    daily = eq.groupby(eq.index.normalize()).last()
    bdays = pd.bdate_range(start.normalize(), end.normalize())
    daily = daily.reindex(bdays.union(daily.index)).ffill().fillna(initial)
    ret = daily.pct_change().dropna()
    years = max((end - start).days / 365.25, 1e-9)
    final = eq.iloc[-1]
    cagr = (final / initial) ** (1 / years) - 1 if final > 0 else -1.0
    max_dd = float(dd.max())
    downside = ret[ret < 0]
    wins, losses = pnl[pnl > 0], pnl[pnl < 0]
    w, l = streaks(pnl)
    return {
        "trades": int(len(t)), "win_rate": float((pnl > 0).mean()),
        "net_profit": float(final - initial), "net_return_pct": float((final / initial - 1) * 100),
        "gross_profit": float(wins.sum()), "gross_loss": float(-losses.sum()),
        "profit_factor": float(wins.sum() / -losses.sum()) if len(losses) else np.inf,
        "expectancy_usd": float(pnl.mean()), "average_trade": float(pnl.mean()),
        "average_winner": float(wins.mean()) if len(wins) else 0.0,
        "average_loser": float(losses.mean()) if len(losses) else 0.0,
        "average_R": float(t["R"].mean()) if "R" in t else np.nan,
        "max_dd_pct": max_dd * 100, "max_dd_usd": float((peak - eq).max()),
        "avg_dd_pct": float(ep_depth.mean() * 100) if len(ep_depth) else 0.0,
        "sharpe": float(ret.mean() / ret.std() * np.sqrt(252)) if ret.std() > 0 else np.nan,
        "sortino": float(ret.mean() / np.sqrt((downside ** 2).sum() / len(ret)) * np.sqrt(252))
        if len(downside) else np.nan,
        "recovery_factor": float((final - initial) / (peak - eq).max()) if (peak - eq).max() > 0 else np.inf,
        "max_consec_losses": l, "max_consec_wins": w,
        "cagr_pct": cagr * 100, "calmar": (cagr / max_dd) if max_dd > 0 else np.inf,
        "skipped_unsizable": int((t["lots"] == 0).sum()),
    }


# ----------------------------------------------------------------------------
# Sesgo de minería de datos
# ----------------------------------------------------------------------------

def deflated_sharpe(r: np.ndarray, sr_trials: np.ndarray) -> dict:
    """Deflated Sharpe Ratio (Bailey & López de Prado, 2014), Sharpe por operación.

    Devuelve la probabilidad de que el Sharpe verdadero sea > 0 tras corregir por
    el número de configuraciones probadas y la no normalidad.
    """
    r = np.asarray(r, float)
    n = len(r)
    sr_trials = sr_trials[np.isfinite(sr_trials)]
    if n < 10 or len(sr_trials) < 2 or r.std(ddof=1) == 0:
        return {"dsr": np.nan, "sr0": np.nan, "n_trials": len(sr_trials)}
    sr = r.mean() / r.std(ddof=1)
    N = len(sr_trials)
    var_sr = sr_trials.var(ddof=1)
    emc = 0.5772156649
    sr0 = math.sqrt(var_sr) * ((1 - emc) * stats.norm.ppf(1 - 1 / N) + emc * stats.norm.ppf(1 - 1 / (N * math.e)))
    sk, ku = stats.skew(r), stats.kurtosis(r, fisher=False)
    den = math.sqrt(max(1 - sk * sr + (ku - 1) / 4 * sr ** 2, 1e-12))
    z = (sr - sr0) * math.sqrt(n - 1) / den
    return {"dsr": float(stats.norm.cdf(z)), "sr": float(sr), "sr0": float(sr0), "n_trials": N}


def benjamini_hochberg(p: np.ndarray, q: float = 0.05) -> np.ndarray:
    p = np.asarray(p, float)
    n = len(p)
    order = np.argsort(p)
    thresh = q * (np.arange(1, n + 1) / n)
    passed = p[order] <= thresh
    k = np.max(np.where(passed)[0]) + 1 if passed.any() else 0
    out = np.zeros(n, bool)
    out[order[:k]] = True
    return out
