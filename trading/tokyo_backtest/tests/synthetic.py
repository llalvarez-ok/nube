"""Generador de datos SINTÉTICOS para probar el software.

NO son datos de mercado y NUNCA deben usarse para sacar conclusiones de trading.
Sirven para: (1) comprobar que el pipeline corre de punta a punta, (2) tests de
look-ahead (un random walk no debe mostrar ventaja; si la muestra, hay un bug).
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def random_walk_m1(start="2019-01-01", end="2022-12-31", price=110.0, daily_vol=0.006, seed=1,
                   server_shift_ny=7) -> pd.DataFrame:
    """Random walk M1 en formato export MT5 (precios bid, hora servidor NY+7), 24x5."""
    rng = np.random.default_rng(seed)
    idx_utc = pd.date_range(start, end, freq="1min")
    ny = idx_utc.tz_localize("UTC").tz_convert("America/New_York")
    # mercado abierto de domingo 17:00 NY a viernes 17:00 NY
    wd, hr = ny.dayofweek, ny.hour
    open_ = ~((wd == 5) | ((wd == 4) & (hr >= 17)) | ((wd == 6) & (hr < 17)))
    idx_utc = idx_utc[open_]
    n = len(idx_utc)
    # volatilidad intradía con forma de U simple + ruido de régimen
    hours = idx_utc.hour.values
    prof = 0.6 + 0.8 * np.isin(hours, [0, 1, 7, 8, 12, 13, 14]).astype(float)
    regime = np.repeat(rng.lognormal(0, 0.3, size=n // 1440 + 2), 1440)[:n]
    sig = daily_vol / np.sqrt(1440) * prof * regime
    rets = rng.standard_normal(n) * sig
    close = price * np.exp(np.cumsum(rets))
    open_px = np.concatenate([[price], close[:-1]])
    wick = np.abs(rng.standard_normal((n, 2))) * sig[:, None] * close[:, None] * 0.5
    high = np.maximum(open_px, close) + wick[:, 0]
    low = np.minimum(open_px, close) - wick[:, 1]
    vol = rng.integers(5, 200, n) * (1 + prof)
    server = (idx_utc.tz_localize("UTC").tz_convert("America/New_York").tz_localize(None)
              + pd.Timedelta(hours=server_shift_ny))
    return pd.DataFrame({"<DATE>": server.strftime("%Y.%m.%d"), "<TIME>": server.strftime("%H:%M:%S"),
                         "<OPEN>": open_px.round(3), "<HIGH>": high.round(3), "<LOW>": low.round(3),
                         "<CLOSE>": close.round(3), "<TICKVOL>": vol.astype(int), "<VOL>": 0, "<SPREAD>": 8})
