"""Evaluación de la grilla, robustez de parámetros, selección congelada y walk-forward.

Reglas anti-sobreoptimización implementadas:
  * Se elige por EXPECTANCY ROBUSTA (mediana de la configuración y sus vecinos en la
    grilla), no por beneficio neto ni por el máximo absoluto.
  * IN-SAMPLE elige candidatas, VALIDATION confirma, OUT-OF-SAMPLE sólo se mide
    DESPUÉS de congelar la selección en disco (selection.json con hash).
  * Walk-forward sólo usa el período previo al OOS (el OOS queda fuera de toda optimización).
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone

import numpy as np
import pandas as pd

from .config import config_hash
from .metrics import benjamini_hochberg, deflated_sharpe, fast_group_metrics
from .postprocess import position_mask, range_filter_mask

_NUM = re.compile(r"^-?\d+(\.\d+)?$")


def kept_by_filter(t: pd.DataFrame, range_filters: list[str], mode: dict) -> dict[str, pd.DataFrame]:
    """Para cada filtro de rango devuelve las operaciones aceptadas (modo de posición aplicado)."""
    out = {}
    cols = ["cfg", "date", "entry_time", "exit_time", "R", "segment", "mae_R", "mfe_R"]
    for rf in range_filters:
        sub = t.loc[range_filter_mask(t["range_atr"], rf), cols]
        keep = position_mask(sub, ["cfg"], mode["max_per_session"], mode["single_position"])
        k = sub.loc[keep].copy()
        k["rf"] = rf
        k["cid"] = k["cfg"] + "|rf=" + rf
        out[rf] = k
    return out


def grid_metrics(kept: dict[str, pd.DataFrame], mask_fn) -> pd.DataFrame:
    parts = []
    for rf, k in kept.items():
        sub = k[mask_fn(k)]
        if len(sub):
            parts.append(fast_group_metrics(sub, "cid"))
    return pd.concat(parts) if parts else pd.DataFrame()


# ----------------------------------------------------------------------------
# Robustez: vecindario en la grilla
# ----------------------------------------------------------------------------

def _axis_code(v):
    """(familia, valor ordinal) de un valor de parámetro."""
    s = str(v)
    if s in ("True", "False"):
        return ("bool", float(s == "True"))
    if _NUM.match(s):
        return ("num", float(s))
    if s == "none":
        return ("gt", 0.0)
    m = re.match(r"^(.*?)_(-?\d+(?:\.\d+)?)(?:_(-?\d+(?:\.\d+)?))?$", s)
    if m:
        fam = m.group(1) + ("_btw" if m.group(3) else "")
        return (fam, float(m.group(2)) + (float(m.group(3)) / 1000 if m.group(3) else 0))
    return (s, 0.0)


def parse_cid(cid: str) -> dict:
    out = {}
    for part in cid.split("|"):
        if "=" in part:
            k, v = part.split("=", 1)
            out[k] = v
    return out


def robustness(table: pd.DataFrame, value_col="expectancy_R") -> pd.DataFrame:
    """Agrega a cada configuración: mediana de expectancy en su vecindario (+-1 paso por eje),
    fracción de vecinos con expectancy > 0 y PF mínimo del vecindario."""
    if table.empty:
        return table
    params = {cid: parse_cid(cid) for cid in table.index}
    axes = sorted({k for p in params.values() for k in p})
    # posiciones ordinales por eje y familia
    pos = {}
    for ax in axes:
        codes = {}
        for p in params.values():
            codes.setdefault(_axis_code(p[ax])[0], set()).add(_axis_code(p[ax])[1])
        pos[ax] = {fam: sorted(vals) for fam, vals in codes.items()}
    key_of = {}
    for cid, p in params.items():
        key_of[cid] = tuple((ax, _axis_code(p[ax])[0], pos[ax][_axis_code(p[ax])[0]].index(_axis_code(p[ax])[1]))
                            for ax in axes)
    by_key = {v: k for k, v in key_of.items()}
    med, stab, minpf, nn = [], [], [], []
    for cid in table.index:
        key = key_of[cid]
        neigh = []
        for i, (ax, fam, ix) in enumerate(key):
            for step in (-1, 1):
                j = ix + step
                if 0 <= j < len(pos[ax][fam]):
                    k2 = list(key)
                    k2[i] = (ax, fam, j)
                    c2 = by_key.get(tuple(k2))
                    if c2 is not None:
                        neigh.append(c2)
        vals = table.loc[[cid] + neigh, value_col].values
        med.append(np.nanmedian(vals))
        nv = table.loc[neigh, value_col].values if neigh else np.array([])
        stab.append(float((nv > 0).mean()) if len(nv) else np.nan)
        minpf.append(float(table.loc[[cid] + neigh, "profit_factor"].min()))
        nn.append(len(neigh))
    out = table.copy()
    out["robust_expectancy_R"] = med
    out["neighbor_positive_share"] = stab
    out["neighbor_min_pf"] = minpf
    out["n_neighbors"] = nn
    return out


def rank_table(tab: pd.DataFrame, min_trades: int) -> pd.DataFrame:
    """Orden: expectancy robusta, profit factor, menor DD (en R), estabilidad."""
    t = tab[tab["trades"] >= min_trades].copy()
    return t.sort_values(["robust_expectancy_R", "profit_factor", "max_dd_R", "neighbor_positive_share"],
                         ascending=[False, False, True, False])


def marginal_regions(tab: pd.DataFrame, min_trades: int) -> tuple[str, str]:
    """Mejor y peor región de parámetros: por eje, el valor con mayor/menor mediana de expectancy."""
    t = tab[tab["trades"] >= min_trades]
    if t.empty:
        return "n/d", "n/d"
    p = pd.DataFrame([parse_cid(c) for c in t.index], index=t.index)
    best, worst = [], []
    for ax in p.columns:
        if p[ax].nunique() < 2:
            continue
        m = t["expectancy_R"].groupby(p[ax]).median()
        best.append(f"{ax}={m.idxmax()}")
        worst.append(f"{ax}={m.idxmin()}")
    return ", ".join(best), ", ".join(worst)


# ----------------------------------------------------------------------------
# Selección congelada
# ----------------------------------------------------------------------------

def select(kept: dict, cfg: dict, n_candidates: int = 10) -> dict:
    """Usa sólo IS y VAL. Devuelve la selección y tablas IS/VAL."""
    min_tr = cfg["selection"]["min_trades_is"]
    is_tab = robustness(grid_metrics(kept, lambda k: k["segment"].values == "IS"))
    val_tab = grid_metrics(kept, lambda k: k["segment"].values == "VAL")
    if is_tab.empty:
        return {"chosen": None, "is_tab": is_tab, "val_tab": val_tab}
    ranked = rank_table(is_tab, min_tr)
    cands = ranked.head(n_candidates).copy()
    cands["val_expectancy_R"] = val_tab["expectancy_R"].reindex(cands.index)
    cands["val_trades"] = val_tab["trades"].reindex(cands.index)
    cands["val_profit_factor"] = val_tab["profit_factor"].reindex(cands.index)
    cands["combined"] = np.minimum(cands["robust_expectancy_R"], cands["val_expectancy_R"].fillna(-np.inf))
    chosen = cands.sort_values("combined", ascending=False).index[0] if len(cands) else None
    # sesgo de minería: DSR y Benjamini-Hochberg sobre toda la grilla IS
    is_full = is_tab[is_tab["trades"] >= 10]
    sr_trials = (is_full["expectancy_R"] / is_full["sd_R"]).values
    bh = benjamini_hochberg(is_full["p_value"].fillna(1).values) if len(is_full) else np.array([])
    return {"chosen": chosen, "candidates": cands, "is_tab": is_tab, "val_tab": val_tab,
            "n_configs_tested": int(len(is_tab)), "sr_trials": sr_trials,
            "bh_significant_is": int(bh.sum()), "min_trades": min_tr}


def freeze(selections: dict, path) -> str:
    payload = {"frozen_at_utc": datetime.now(timezone.utc).isoformat(), "selections": selections}
    payload["hash"] = config_hash(selections)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, default=str)
    return payload["hash"]


def deflated(kept: dict, chosen: str, sr_trials) -> dict:
    rf = parse_cid(chosen)["rf"]
    k = kept[rf]
    r = k.loc[(k["cid"] == chosen) & (k["segment"] == "IS"), "R"].values
    return deflated_sharpe(r, np.asarray(sr_trials))


# ----------------------------------------------------------------------------
# Walk-forward (sólo pre-OOS)
# ----------------------------------------------------------------------------

def walk_forward(kept: dict, bounds: dict, cfg: dict, final_cid: str | None) -> pd.DataFrame:
    wf = cfg["walk_forward"]
    start, stop = bounds["start"], bounds["val_end"]
    is_years = (bounds["is_end"] - bounds["start"]).days / 365.25
    min_tr = max(30, int(cfg["selection"]["min_trades_is"] * wf["train_months"] / 12 / max(is_years, 1e-9)))
    rows = []
    ts = start
    while True:
        te = ts + pd.DateOffset(months=wf["train_months"])
        tt = te + pd.DateOffset(months=wf["test_months"])
        if tt > stop:
            break
        train = robustness(grid_metrics(kept, lambda k: (k["date"].values >= ts.to_datetime64()) &
                                                       (k["date"].values < te.to_datetime64())))
        test = grid_metrics(kept, lambda k: (k["date"].values >= te.to_datetime64()) &
                                            (k["date"].values < tt.to_datetime64()))
        ranked = rank_table(train, min_tr) if not train.empty else train
        pick = ranked.index[0] if len(ranked) else None
        row = {"train_start": ts.date(), "train_end": te.date(), "test_start": te.date(), "test_end": tt.date(),
               "selected_cfg": pick, "train_expectancy_R": ranked["expectancy_R"].iloc[0] if pick else np.nan,
               "train_trades": ranked["trades"].iloc[0] if pick else 0}
        for lbl, cid in (("wf", pick), ("final", final_cid)):
            if cid is not None and cid in test.index:
                row[f"{lbl}_test_trades"] = test.loc[cid, "trades"]
                row[f"{lbl}_test_expectancy_R"] = test.loc[cid, "expectancy_R"]
                row[f"{lbl}_test_net_R"] = test.loc[cid, "net_R"]
                row[f"{lbl}_test_pf"] = test.loc[cid, "profit_factor"]
            else:
                row[f"{lbl}_test_trades"] = 0
                row[f"{lbl}_test_expectancy_R"] = np.nan
                row[f"{lbl}_test_net_R"] = 0.0
                row[f"{lbl}_test_pf"] = np.nan
        rows.append(row)
        ts = ts + pd.DateOffset(months=wf["step_months"])
    return pd.DataFrame(rows)
