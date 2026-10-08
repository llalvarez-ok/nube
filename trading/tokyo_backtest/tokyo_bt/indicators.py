"""Indicadores calculados exclusivamente con barras cerradas.

Convención: cada serie devuelta está indexada por su HORA DE DISPONIBILIDAD
(cierre de la barra que la produce). Para consultarla en un instante t se usa
`asof(series, t)`, que toma el último valor disponible en t o antes.
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def wilder_atr(h: pd.Series, l: pd.Series, c: pd.Series, period: int) -> pd.Series:
    prev_c = c.shift(1)
    tr = pd.concat([h - l, (h - prev_c).abs(), (l - prev_c).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / period, adjust=False, min_periods=period).mean()


def atr_available(bars: pd.DataFrame, tf_minutes: int, period: int, prefix="mid") -> pd.Series:
    """ATR de las barras dadas, indexado por la hora de cierre de cada barra."""
    a = wilder_atr(bars[f"{prefix}_h"], bars[f"{prefix}_l"], bars[f"{prefix}_c"], period)
    a.index = bars.index + pd.Timedelta(minutes=tf_minutes)
    return a.dropna()


def daily_atr_for_sessions(d1: pd.DataFrame, period: int, boundary_minutes: int) -> pd.Series:
    """ATR diario utilizable al INICIO de cada día: sólo días completamente cerrados.

    d1 indexado por la fecha del día (ya desplazado por el corte). El valor para la
    sesión del día D es el ATR calculado hasta el día D-1 inclusive.
    """
    a = wilder_atr(d1["h"], d1["l"], d1["c"], period)
    # disponible al cierre del día => desde el inicio del siguiente día de datos
    avail = pd.Series(a.values, index=d1.index + pd.Timedelta(days=1) + pd.Timedelta(minutes=boundary_minutes))
    return avail.dropna()


def asof(series: pd.Series, times: pd.DatetimeIndex | np.ndarray) -> np.ndarray:
    """Último valor de 'series' disponible en cada instante de 'times' (o NaN)."""
    if len(series) == 0:
        return np.full(len(times), np.nan)
    st = series.index.values
    pos = np.searchsorted(st, np.asarray(times, dtype="datetime64[ns]"), side="right") - 1
    vals = series.values
    out = np.where(pos >= 0, vals[np.clip(pos, 0, None)], np.nan)
    return out.astype(float)


def session_vwap(bars: pd.DataFrame, tf_minutes: int, anchor_minutes: int) -> pd.Series:
    """VWAP anclado diariamente a 'anchor_minutes' UTC, valor al CIERRE de cada barra."""
    tp = (bars["mid_h"] + bars["mid_l"] + bars["mid_c"]) / 3
    v = bars["volume"].astype(float).fillna(0)
    day = (bars.index - pd.Timedelta(minutes=anchor_minutes)).normalize()
    pv = (tp * v).groupby(day).cumsum()
    vv = v.groupby(day).cumsum()
    vwap = (pv / vv.replace(0, np.nan))
    vwap.index = bars.index + pd.Timedelta(minutes=tf_minutes)
    return vwap


def rolling_vwap(bars: pd.DataFrame, tf_minutes: int, window_minutes: int) -> pd.Series:
    """VWAP de las últimas 'window_minutes' (ventana móvil), valor al CIERRE de cada barra."""
    tp = (bars["mid_h"] + bars["mid_l"] + bars["mid_c"]) / 3
    v = bars["volume"].astype(float).fillna(0)
    w = f"{window_minutes}min"
    vwap = (tp * v).rolling(w).sum() / v.rolling(w).sum().replace(0, np.nan)
    vwap.index = bars.index + pd.Timedelta(minutes=tf_minutes)
    return vwap


def confirmed_swings(m5: pd.DataFrame, left: int, right: int, tf_minutes: int = 5):
    """Swings M5 (fractales). Un swing en la barra i se confirma al cierre de la barra i+right.

    Devuelve (swing_lows, swing_highs) indexados por hora de CONFIRMACIÓN.
    """
    from numpy.lib.stride_tricks import sliding_window_view as swv
    lo, hi = m5["mid_l"].values, m5["mid_h"].values
    w = left + right + 1
    sl_idx = sh_idx = np.array([], dtype=int)
    if len(m5) >= w:
        wl, wh = swv(lo, w), swv(hi, w)
        c_lo, c_hi = lo[left:len(lo) - right], hi[left:len(hi) - right]
        # mínimo/máximo estricto (único) de la ventana centrada
        is_low = (c_lo == wl.min(axis=1)) & ((wl == c_lo[:, None]).sum(axis=1) == 1)
        is_high = (c_hi == wh.max(axis=1)) & ((wh == c_hi[:, None]).sum(axis=1) == 1)
        sl_idx = np.nonzero(is_low)[0] + left
        sh_idx = np.nonzero(is_high)[0] + left
    conf_t = m5.index + pd.Timedelta(minutes=tf_minutes * (right + 1))
    lows = pd.Series(lo[sl_idx], index=conf_t[sl_idx])
    highs = pd.Series(hi[sh_idx], index=conf_t[sh_idx])
    return lows, highs


def volatility_regime(atr_by_session: pd.Series, lookback: int, low_pct: float, high_pct: float,
                      min_history: int = 60) -> pd.Series:
    """Clasifica cada sesión por el percentil de su ATR contra las 'lookback' sesiones ANTERIORES."""
    vals = atr_by_session.values
    out = []
    for i in range(len(vals)):
        past = vals[max(0, i - lookback):i]
        past = past[~np.isnan(past)]
        if len(past) < min_history or np.isnan(vals[i]):
            out.append("unclassified")
            continue
        pct = (past < vals[i]).mean() * 100
        out.append("low" if pct < low_pct else ("high" if pct > high_pct else "medium"))
    return pd.Series(out, index=atr_by_session.index)
