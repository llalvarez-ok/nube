"""Prepara todo lo que necesita la simulación de un símbolo en un escenario de costos.

Todas las series auxiliares (ATR, VWAP, swings) se alinean a la hora de CIERRE
de cada barra de ejecución mediante `asof`, por lo que un valor sólo se usa
cuando ya habría sido observable en tiempo real.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from .config import hhmm_to_minutes
from .costs import build_bid_ask, slippage_px
from .data import TF_MINUTES, daily_bars, resample
from .indicators import (asof, atr_available, confirmed_swings, daily_atr_for_sessions,
                         rolling_vwap, session_vwap, volatility_regime)


@dataclass
class Session:
    date: pd.Timestamp
    start: pd.Timestamp
    last_entry: pd.Timestamp
    exit: pd.Timestamp
    i0: int            # primera barra de ejecución de la sesión
    i1: int            # primera barra con apertura >= exit (excluida)
    atr: float
    vol_regime: str
    coverage: float


@dataclass
class Market:
    symbol: str
    spec: dict
    cfg: dict
    bars: pd.DataFrame
    m5: pd.DataFrame
    tf_min: int
    slip: float
    sessions: list = field(default_factory=list)
    arr: dict = field(default_factory=dict)
    has_volume: bool = False
    spread_source: str = ""

    # ------------------------------------------------------------------
    @classmethod
    def build(cls, raw: pd.DataFrame, symbol: str, cfg: dict, spread_mult=1.0, slip_mult=1.0):
        spec = cfg["instruments"][symbol]
        bars = build_bid_ask(raw, spec, cfg, spread_mult)
        tf = raw.attrs.get("timeframe", "M1")
        tf_min = TF_MINUTES[tf]
        m5 = resample(bars, "M5", prefixes=("bid", "ask", "mid")) if tf_min < 5 else bars.copy()
        mk = cls(symbol, spec, cfg, bars, m5, tf_min, slippage_px(spec, slip_mult))
        mk.has_volume = bool(raw.attrs.get("has_volume"))
        mk.spread_source = bars.attrs.get("spread_source", "")
        mk._indicators()
        mk._sessions()
        return mk

    # ------------------------------------------------------------------
    def _indicators(self):
        cfg, ind = self.cfg, self.cfg["indicators"]
        sess = cfg["session"]
        bnd = hhmm_to_minutes(sess["daily_boundary_utc"])
        d1 = daily_bars(self.bars, bnd, sess["min_daily_hours"], price="mid")
        self.atr_d1 = daily_atr_for_sessions(d1, ind["atr"]["period"], bnd)

        close_t = self.bars.index + pd.Timedelta(minutes=self.tf_min)
        self.arr["close_t"] = close_t.values
        for p in ("bid", "ask", "mid"):
            for k in "ohlc":
                self.arr[f"{p}_{k}"] = self.bars[f"{p}_{k}"].values.astype(float)
        self.arr["spread"] = self.bars["spread_px"].values.astype(float)

        ta = ind["trail_atr"]
        if ta["timeframe"] == "D1":
            self.arr["trail_atr"] = asof(self.atr_d1, close_t)
        else:
            tfm = TF_MINUTES[ta["timeframe"]]
            b = resample(self.bars, ta["timeframe"], prefixes=("mid",)) if tfm > self.tf_min else self.bars
            self.arr["trail_atr"] = asof(atr_available(b, tfm, ta["period"]), close_t)

        if self.has_volume:
            if ind["vwap"].get("mode", "session") == "rolling":
                vw = rolling_vwap(self.bars, self.tf_min, int(ind["vwap"]["rolling_minutes"]))
            else:
                vw = session_vwap(self.bars, self.tf_min, hhmm_to_minutes(ind["vwap"]["anchor_utc"]))
            self.arr["vwap"] = vw.values
            m5_close = self.m5.index + pd.Timedelta(minutes=5)
            self.m5["vwap"] = asof(vw, m5_close)
        else:
            self.arr["vwap"] = np.full(len(self.bars), np.nan)
            self.m5["vwap"] = np.nan

        sw = ind["swing"]
        lows, highs = confirmed_swings(self.m5, sw["left"], sw["right"])
        self.arr["swing_low"] = asof(lows, close_t)
        self.arr["swing_high"] = asof(highs, close_t)

    # ------------------------------------------------------------------
    def _sessions(self):
        s = self.cfg["session"]
        s0, le, ex = (hhmm_to_minutes(s[k]) for k in ("start_utc", "last_entry_utc", "exit_time_utc"))
        e0 = hhmm_to_minutes(s["end_utc"])
        idx = self.bars.index
        t = idx.values
        days = pd.DatetimeIndex(np.unique(idx.normalize()))
        days = days[days.dayofweek.isin(s["trading_days"])]
        start_t = days + pd.Timedelta(minutes=s0)
        atr = asof(self.atr_d1, start_t)
        regime = volatility_regime(pd.Series(atr, index=days), **{
            "lookback": self.cfg["indicators"]["volatility_regime"]["lookback_days"],
            "low_pct": self.cfg["indicators"]["volatility_regime"]["low_pct"],
            "high_pct": self.cfg["indicators"]["volatility_regime"]["high_pct"]})
        expected = (e0 - s0) / self.tf_min
        for k, d in enumerate(days):
            st = d + pd.Timedelta(minutes=s0)
            en = d + pd.Timedelta(minutes=e0)
            i0 = int(np.searchsorted(t, st.to_datetime64()))
            i1 = int(np.searchsorted(t, (d + pd.Timedelta(minutes=ex)).to_datetime64()))
            ie = int(np.searchsorted(t, en.to_datetime64()))
            cov = (ie - i0) / expected
            if np.isnan(atr[k]) or atr[k] <= 0 or i1 <= i0:
                continue
            self.sessions.append(Session(d, st, d + pd.Timedelta(minutes=le), d + pd.Timedelta(minutes=ex),
                                         i0, i1, float(atr[k]), regime.iloc[k], float(cov)))
        self.min_cov = s["min_session_coverage"]

    def tradable_sessions(self):
        return [x for x in self.sessions if x.coverage >= self.min_cov]

    def m5_session(self, sess: Session) -> pd.DataFrame:
        return self.m5.loc[sess.start:sess.exit - pd.Timedelta(minutes=5)]

    def bar_index_at(self, t: pd.Timestamp) -> int:
        """Índice de la primera barra de ejecución con apertura >= t."""
        return int(np.searchsorted(self.arr_t, t.to_datetime64()))

    @property
    def arr_t(self):
        if "t" not in self.arr:
            self.arr["t"] = self.bars.index.values
        return self.arr["t"]
