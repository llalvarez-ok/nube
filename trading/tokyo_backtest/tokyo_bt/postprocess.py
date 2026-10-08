"""Pasos posteriores a la simulación: costos en R, filtros, modos de posición, noticias, split."""
from __future__ import annotations

import numpy as np
import pandas as pd

from .config import resolve
from .costs import Converter, swap_nights
from .engine import EXIT_NAMES

SIG_COLS = ["sig_id", "strategy", "symbol", "date", "direction", "signal_time", "exp_entry", "atr",
            "vol_regime", "range_hi", "range_lo", "range", "range_mid", "range_atr", "vwap",
            "spread_at_signal", "breakout_dist_atr", "sweep_ext", "sweep_depth_atr", "bars_outside",
            "minutes_outside", "dist_to_mid_atr", "or_minutes", "vwap_slope_atr"]


MIN_COLS = ["sig_id", "strategy", "symbol", "date", "direction", "signal_time", "range_atr"]


def enrich(tdf: pd.DataFrame, sdf: pd.DataFrame, spec: dict, conv: Converter, slip_px: float,
           full: bool = False) -> pd.DataFrame:
    """Calcula R neto (comisión y swap incluidos). full=True agrega todos los campos de la señal."""
    cols = [c for c in (SIG_COLS if full else MIN_COLS) if c in sdf.columns]
    t = tdf.merge(sdf[cols], on="sig_id", how="left")
    t["conv"] = conv.rate(spec["quote_ccy"], pd.DatetimeIndex(t["signal_time"]))
    unit_usd = spec["contract_size"] * t["conv"]
    t["comm_px"] = spec.get("commission_per_lot_rt", 0.0) / unit_usd
    if (t["exit_time"].dt.normalize() != t["entry_time"].dt.normalize()).any() or \
            (t["exit_time"].dt.hour >= 21).any():
        nights = np.array([swap_nights(a, b) for a, b in zip(t["entry_time"], t["exit_time"])])
    else:
        nights = np.zeros(len(t))
    sw = np.where(t["direction"] > 0, spec.get("swap_long_points", 0.0), spec.get("swap_short_points", 0.0))
    t["swap_px"] = nights * sw * spec["point"]
    t["R"] = (t["pnl_px"] + t["swap_px"] - t["comm_px"]) / t["rdist"]
    t["slippage_px"] = slip_px
    t["exit_reason_name"] = t["exit_reason"].map(EXIT_NAMES)
    t["hour_utc"] = t["entry_time"].dt.hour
    t["dow"] = t["entry_time"].dt.dayofweek
    pcols = sorted(c for c in t.columns if c.startswith("p_"))
    t["cfg"] = (t[pcols].astype(str).radd([f"{c[2:]}=" for c in pcols]).agg("|".join, axis=1)
                if pcols else "base")
    return t.sort_values("entry_time").reset_index(drop=True)


# ----------------------------------------------------------------------------

def range_filter_mask(range_atr: pd.Series, name: str) -> np.ndarray:
    if name == "none":
        return np.ones(len(range_atr), bool)
    parts = name.split("_")
    if parts[0] == "gt":
        return (range_atr > float(parts[1])).values
    if parts[0] == "btw":
        return ((range_atr >= float(parts[1])) & (range_atr <= float(parts[2]))).values
    raise ValueError(name)


def position_mask(df: pd.DataFrame, group_cols: list[str], max_per_session, single_position: bool) -> np.ndarray:
    """Acepta operaciones en orden de entrada respetando single-position y el tope por sesión.
    df debe estar ordenado por entry_time."""
    keep = np.zeros(len(df), bool)
    gkey = df[group_cols].astype(str).agg("|".join, axis=1).values if len(group_cols) > 1 \
        else df[group_cols[0]].astype(str).values
    sess = df["date"].values
    entry = df["entry_time"].values
    exit_ = df["exit_time"].values
    state = {}     # gkey -> (date, count, last_exit)
    for i in range(len(df)):
        g = gkey[i]
        d, cnt, last_exit = state.get(g, (None, 0, None))
        if d != sess[i]:
            cnt = 0
        if max_per_session is not None and cnt >= max_per_session:
            state[g] = (sess[i], cnt, last_exit)
            continue
        if single_position and last_exit is not None and entry[i] < last_exit:
            state[g] = (sess[i], cnt, last_exit)
            continue
        keep[i] = True
        state[g] = (sess[i], cnt + 1, exit_[i] if last_exit is None or exit_[i] > last_exit else last_exit)
    return keep


# ----------------------------------------------------------------------------
# Noticias
# ----------------------------------------------------------------------------

def load_news(cfg: dict) -> pd.DataFrame | None:
    n = cfg.get("news", {})
    if not n.get("enabled"):
        return None
    p = resolve(cfg, n["file"])
    if not p.exists():
        return None
    df = pd.read_csv(p)
    df["datetime_utc"] = pd.to_datetime(df["datetime_utc"], utc=True).dt.tz_localize(None)
    df = df[df["impact"].str.lower().isin([x.lower() for x in n["impact_levels"]])]
    return df


def news_mask(t: pd.DataFrame, news: pd.DataFrame, cfg: dict) -> np.ndarray:
    """True si la operación se ABRE dentro de la ventana de un evento de alto impacto
    de alguna de las monedas del símbolo. El calendario es conocido de antemano (no es look-ahead)."""
    n = cfg["news"]
    before, after = pd.Timedelta(minutes=n["window_before_min"]), pd.Timedelta(minutes=n["window_after_min"])
    out = np.zeros(len(t), bool)
    for sym, idx in t.groupby("symbol").groups.items():
        ccys = n["currency_map"].get(sym, [])
        ev = np.sort(news.loc[news["currency"].isin(ccys), "datetime_utc"].values)
        if len(ev) == 0:
            continue
        et = t.loc[idx, "entry_time"].values
        # evento más cercano posterior a (entry - after) debe ser <= entry + before
        pos = np.searchsorted(ev, et - after.to_timedelta64())
        nxt = ev[np.clip(pos, 0, len(ev) - 1)]
        hit = (pos < len(ev)) & (nxt <= et + before.to_timedelta64())
        out[np.asarray([t.index.get_loc(i) for i in idx])] = hit
    return out


# ----------------------------------------------------------------------------
# Split temporal 60/20/20
# ----------------------------------------------------------------------------

def split_bounds(dates: pd.Series | pd.DatetimeIndex, cfg: dict) -> dict:
    d = pd.DatetimeIndex(sorted(pd.unique(pd.DatetimeIndex(dates))))
    s = cfg["split"]
    n = len(d)
    i_is = int(n * s["in_sample"])
    i_val = int(n * (s["in_sample"] + s["validation"]))
    return {"start": d[0], "is_end": d[i_is], "val_end": d[i_val], "end": d[-1] + pd.Timedelta(days=1)}


def segment(dates: pd.Series, b: dict) -> np.ndarray:
    d = pd.DatetimeIndex(dates)
    return np.where(d < b["is_end"], "IS", np.where(d < b["val_end"], "VAL", "OOS"))
