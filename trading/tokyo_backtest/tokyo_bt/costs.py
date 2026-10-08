"""Modelo de costos: spread, slippage, comisión, swap y conversión a moneda de cuenta.

Prioridad para el spread:
  1. Datos bid/ask reales (si existen y costs.use_bid_ask_if_available).
  2. Columna de spread por barra (export MT5) — tratada como COTA INFERIOR:
     spread = max(columna, modelo) cuando costs.bar_spread_column_is_minimum.
  3. Modelo por hora UTC del archivo de configuración (SUPUESTO conservador).
Los multiplicadores de sensibilidad ensanchan el spread alrededor del precio medio.
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def model_spread_px(index: pd.DatetimeIndex, spec: dict) -> np.ndarray:
    m = spec["spread_model"]
    unit = spec["pip"] if m.get("unit", "pips") == "pips" else spec["point"]
    by_hour = {int(k): float(v) for k, v in (m.get("by_hour") or {}).items()}
    hours = index.hour.values
    vals = np.full(len(index), float(m["default"]))
    for hr, v in by_hour.items():
        vals[hours == hr] = v
    return vals * unit


def build_bid_ask(raw: pd.DataFrame, spec: dict, cfg: dict, spread_mult: float = 1.0) -> pd.DataFrame:
    """Devuelve DataFrame con bid_*/ask_*/mid_*/spread_px a partir del canónico."""
    out = pd.DataFrame(index=raw.index)
    if raw.attrs.get("has_bid_ask") and cfg["costs"].get("use_bid_ask_if_available", True):
        for k in "ohlc":
            b, a = raw[f"bid_{k}"].values, raw[f"ask_{k}"].values
            mid, half = (a + b) / 2, (a - b) / 2 * spread_mult
            out[f"bid_{k}"], out[f"ask_{k}"], out[f"mid_{k}"] = mid - half, mid + half, mid
        out["spread_px"] = (raw["ask_o"] - raw["bid_o"]).values * spread_mult
        source = "bid_ask_data"
    else:
        s = model_spread_px(raw.index, spec)
        source = "model"
        if "spread_points" in raw and raw["spread_points"].notna().any():
            col = raw["spread_points"].fillna(0).values * spec["point"]
            s = np.maximum(col, s) if cfg["costs"].get("bar_spread_column_is_minimum", True) else \
                np.where(col > 0, col, s)
            source = "bar_spread_column+model"
        s = s * spread_mult
        side = raw.attrs.get("price_side", "mid")
        for k in "ohlc":
            px = raw[f"px_{k}"].values
            if side == "bid":
                bid, ask = px, px + s
            elif side == "ask":
                bid, ask = px - s, px
            else:
                bid, ask = px - s / 2, px + s / 2
            out[f"bid_{k}"], out[f"ask_{k}"], out[f"mid_{k}"] = bid, ask, (bid + ask) / 2
        out["spread_px"] = s
    out["volume"] = raw["volume"].values
    out.attrs = dict(raw.attrs, spread_source=source, spread_mult=spread_mult)
    return out


def slippage_px(spec: dict, mult: float = 1.0) -> float:
    return float(spec.get("slippage_pips", 0.0)) * spec["pip"] * mult


class Converter:
    """Convierte importes en moneda de cotización a la moneda de cuenta usando
    el último cierre conocido del símbolo de conversión (sin look-ahead)."""

    def __init__(self, cfg: dict, series: dict[str, pd.Series]):
        self.cfg = cfg
        self.series = series  # símbolo -> serie de cierres mid indexada por hora de CIERRE

    def rate(self, quote_ccy: str, times: pd.DatetimeIndex) -> np.ndarray:
        rule = self.cfg["conversion"].get(quote_ccy)
        if rule is None:
            return np.ones(len(times))
        s = self.series.get(rule["symbol"])
        if s is None:
            raise RuntimeError(f"Para convertir {quote_ccy} a USD se necesitan datos de {rule['symbol']}")
        from .indicators import asof
        px = asof(s, times)
        return 1.0 / px if rule["op"] == "divide" else px


def swap_nights(entry: pd.Timestamp, exit_: pd.Timestamp, rollover_utc_hour: int = 21) -> int:
    """Cantidad de rollovers cruzados (miércoles cuenta triple)."""
    if exit_ <= entry:
        return 0
    n = 0
    t = entry.normalize() + pd.Timedelta(hours=rollover_utc_hour)
    if t <= entry:
        t += pd.Timedelta(days=1)
    while t <= exit_:
        n += 3 if t.dayofweek == 2 else 1
        t += pd.Timedelta(days=1)
    return n
