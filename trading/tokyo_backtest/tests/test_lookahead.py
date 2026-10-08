"""Tests de integridad: sin look-ahead y reglas de ejecución conservadoras.

    python -m pytest tests/ -q        (o)   python tests/test_lookahead.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))

from synthetic import random_walk_m1  # noqa: E402
from tokyo_bt.config import load_config  # noqa: E402
from tokyo_bt.data import to_utc  # noqa: E402
from tokyo_bt.engine import EXIT_BE, EXIT_SL, EXIT_TIME, EXIT_TP, simulate  # noqa: E402
from tokyo_bt.market import Market  # noqa: E402
from tokyo_bt.strategies import generate  # noqa: E402


def _raw_from_synth(df: pd.DataFrame, symbol="USDJPY") -> pd.DataFrame:
    ts = pd.to_datetime(df["<DATE>"] + " " + df["<TIME>"], format="%Y.%m.%d %H:%M:%S")
    idx = to_utc(pd.DatetimeIndex(ts), "NY+7")
    raw = pd.DataFrame({"px_o": df["<OPEN>"].values, "px_h": df["<HIGH>"].values, "px_l": df["<LOW>"].values,
                        "px_c": df["<CLOSE>"].values, "volume": df["<TICKVOL>"].values.astype(float),
                        "spread_points": df["<SPREAD>"].values}, index=idx)
    raw.attrs.update(has_bid_ask=False, price_side="bid", has_volume=True, timeframe="M1", symbol=symbol)
    return raw


def _cfg():
    cfg = load_config()
    cfg["indicators"]["volatility_regime"]["lookback_days"] = 60
    return cfg


_RAW = None


def raw():
    global _RAW
    if _RAW is None:
        _RAW = _raw_from_synth(random_walk_m1("2021-01-01", "2021-08-31", seed=7))
    return _RAW


def test_timezone_ny_plus_7():
    # 2021-07-01 10:00 servidor (verano, GMT+3) = 07:00 UTC ; 2021-01-04 10:00 (invierno, GMT+2) = 08:00 UTC
    idx = pd.DatetimeIndex(["2021-07-01 10:00", "2021-01-04 10:00"])
    out = to_utc(idx, "NY+7")
    assert list(out) == [pd.Timestamp("2021-07-01 07:00"), pd.Timestamp("2021-01-04 08:00")]


def test_signals_invariant_to_future_data():
    """Truncar los datos en T no puede cambiar ninguna señal anterior a T (ni ATR, ni rangos)."""
    cfg = _cfg()
    full = raw()
    cut = pd.Timestamp("2021-06-15 05:17")
    trunc = full[full.index < cut].copy()
    trunc.attrs = full.attrs
    compared = 0
    for strat in ("A_asian_range_breakout", "B_asian_failed_breakout", "C_tokyo_or_breakout",
                  "D_tokyo_or_failed_breakout", "E_tokyo_breakout_vwap"):
        scfg = cfg["strategies"][strat]
        a = generate(Market.build(full, "USDJPY", cfg), strat, scfg, cfg)
        b = generate(Market.build(trunc, "USDJPY", cfg), strat, scfg, cfg)
        keys = ["date", "direction", "signal_time", "exp_entry", "atr", "range_hi", "range_lo", "vwap"]
        for k in a:
            sa = [tuple(s.get(x) for x in keys) for s in a[k] if s["signal_time"] < cut]
            sb = [tuple(s.get(x) for x in keys) for s in b[k] if s["signal_time"] < cut]
            # la sesión cortada puede perder señales por cobertura, nunca ganar ni cambiar
            sa = [s for s in sa if s[0] < cut.normalize()]
            sb = [s for s in sb if s[0] < cut.normalize()]
            assert len(sa) == len(sb), (strat, k, len(sa), len(sb))
            compared += len(sa)
            for x, y in zip(sa, sb):
                assert all((p == q) or (isinstance(p, float) and np.isnan(p) and np.isnan(q))
                           for p, q in zip(x, y)), (strat, k, x, y)
    assert compared > 100, compared     # el test no debe pasar en vacío


def test_range_ignores_bars_after_range_end():
    """Modificar el precio después de las 03:00 no cambia el Asian range."""
    cfg = _cfg()
    r = raw().copy()
    day = pd.Timestamp("2021-05-12")
    m = (r.index >= day + pd.Timedelta(hours=3)) & (r.index < day + pd.Timedelta(hours=9))
    r2 = r.copy()
    r2.loc[m, ["px_h"]] += 5.0
    r2.attrs = r.attrs
    scfg = cfg["strategies"]["A_asian_range_breakout"]
    s1 = [s for s in generate(Market.build(r, "USDJPY", cfg), "A_asian_range_breakout", scfg, cfg)[(("buffer_atr", 0.0),)]
          if s["date"] == day]
    s2 = [s for s in generate(Market.build(r2, "USDJPY", cfg), "A_asian_range_breakout", scfg, cfg)[(("buffer_atr", 0.0),)]
          if s["date"] == day]
    if s1 and s2:
        assert s1[0]["range_hi"] == s2[0]["range_hi"] and s1[0]["range_lo"] == s2[0]["range_lo"]


def test_entry_is_after_signal_close():
    cfg = _cfg()
    mk = Market.build(raw(), "USDJPY", cfg)
    sigs = generate(mk, "A_asian_range_breakout", cfg["strategies"]["A_asian_range_breakout"], cfg)
    for lst in sigs.values():
        for s in lst:
            assert mk.arr_t[s["entry_idx"]] >= s["signal_time"].to_datetime64()
            assert s["signal_time"] >= s["date"] + pd.Timedelta(hours=3, minutes=5)


# ----------------------------------------------------------------------------
# Motor: reglas conservadoras con barras construidas a mano
# ----------------------------------------------------------------------------

class _FakeMk:
    def __init__(self, bars, slip=0.0):
        n = len(bars)
        b = np.array(bars, float)  # columnas: o h l c (bid); ask = bid + 0.01
        self.arr = {"bid_o": b[:, 0], "bid_h": b[:, 1], "bid_l": b[:, 2], "bid_c": b[:, 3]}
        for k in "ohlc":
            self.arr[f"ask_{k}"] = self.arr[f"bid_{k}"] + 0.01
        self.arr["trail_atr"] = np.full(n, 1.0)
        self.arr["swing_low"] = np.full(n, np.nan)
        self.arr["swing_high"] = np.full(n, np.nan)
        self.slip = slip


def _sig(n):
    return {"entry_idx": 0, "exit_idx": n, "direction": 1}


def test_same_bar_sl_and_tp_is_stop():
    mk = _FakeMk([[100, 100.1, 99.9, 100], [100, 102, 98, 100], [100, 100, 100, 100]])
    r = simulate(mk, _sig(3), 99.0, [(1.0, 101.0)], False, None, 1.0)
    assert r["exit_reason"] == EXIT_SL and r["pnl_px"] < -1.0


def test_tp_then_time_exit_and_gap_stop():
    mk = _FakeMk([[100, 100.2, 99.9, 100.1], [100.1, 101.5, 100, 101.2]])
    r = simulate(mk, _sig(2), 99.0, [(1.0, 101.0)], False, None, 1.0)
    assert r["exit_reason"] == EXIT_TP and abs(r["exit_fill"] - 101.0) < 1e-9
    mk = _FakeMk([[100, 100.2, 99.9, 100.1], [100.1, 100.2, 100, 100.1]])
    r = simulate(mk, _sig(2), 99.0, [(1.0, 101.0)], False, None, 1.0)
    assert r["exit_reason"] == EXIT_TIME
    # gap por debajo del stop: se llena en la apertura (peor que el stop)
    mk = _FakeMk([[100, 100.2, 99.9, 100.1], [98.5, 98.6, 98.0, 98.2]])
    r = simulate(mk, _sig(2), 99.0, [(1.0, 101.0)], False, None, 1.0)
    assert r["exit_reason"] == EXIT_SL and abs(r["exit_fill"] - 98.5) < 1e-9


def test_breakeven_after_partial_and_short_mirror():
    mk = _FakeMk([[100, 100.2, 99.9, 100.1], [100.1, 101.2, 100.5, 101], [101, 101, 99.5, 99.6]])
    r = simulate(mk, _sig(3), 99.0, [(0.5, 101.0), (0.5, 103.0)], True, None, 1.0)
    assert r["exit_reason"] == EXIT_BE and r["tp1_hit"]
    # short: stop arriba, se dispara con el ASK
    mk = _FakeMk([[100, 100.2, 99.9, 100.1], [100.1, 100.995, 100, 100.5]])
    r = simulate(mk, {"entry_idx": 0, "exit_idx": 2, "direction": -1}, 101.0, [(1.0, 99.0)], False, None, 1.0)
    assert r["exit_reason"] == EXIT_SL      # ask_h = 101.005 >= 101


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("OK", name)
