"""Carga de datos históricos y normalización a UTC.

Formato canónico (DataFrame indexado por la hora de APERTURA de la barra, UTC):
    bid_o bid_h bid_l bid_c ask_o ask_h ask_l ask_c volume
    + atributos: df.attrs["has_bid_ask"], ["has_volume"], ["spread_source"], ["timeframe"]

Una barra con índice t cubre [t, t + timeframe) y su información recién está
disponible en t + timeframe. Ningún dato se inventa: si un archivo falta, se
lanza DataMissingError.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from .config import resolve

TF_MINUTES = {"M1": 1, "M5": 5, "M15": 15, "H1": 60, "D1": 1440}


class DataMissingError(RuntimeError):
    pass


# ----------------------------------------------------------------------------
# Lectores por formato
# ----------------------------------------------------------------------------

def _read_mt5(path: Path) -> pd.DataFrame:
    """Export de MetaTrader 5 (Symbols > Bars > Export). Precios BID, hora del servidor."""
    with open(path, encoding="utf-8", errors="replace") as fh:
        first = fh.readline()
    sep = "\t" if "\t" in first else ("," if "," in first else ";")
    df = pd.read_csv(path, sep=sep)
    df.columns = [c.strip("<>").lower() for c in df.columns]
    ts = pd.to_datetime(df["date"].astype(str) + " " + df["time"].astype(str), format="%Y.%m.%d %H:%M:%S")
    out = pd.DataFrame({"o": df["open"].values, "h": df["high"].values, "l": df["low"].values,
                        "c": df["close"].values}, index=ts)
    vol = df["tickvol"] if "tickvol" in df else df.get("vol")
    out["volume"] = vol.values if vol is not None else np.nan
    if "spread" in df:
        out["spread_points"] = df["spread"].values
    out.attrs["price_side"] = "bid"
    return out


def _read_mt5py(path: Path) -> pd.DataFrame:
    """CSV generado por exportar_mt5.py (API Python de MT5): precios BID, hora del servidor."""
    df = pd.read_csv(path)
    ts = pd.to_datetime(df["time"], format="%Y-%m-%d %H:%M:%S")
    out = pd.DataFrame({"o": df["open"].values, "h": df["high"].values, "l": df["low"].values,
                        "c": df["close"].values, "volume": df["tick_volume"].values,
                        "spread_points": df["spread"].values}, index=ts)
    out.attrs["price_side"] = "bid"
    return out


def _read_dukascopy(path: Path) -> pd.DataFrame:
    """CSV de Dukascopy (Historical Data Feed): 'Gmt time,Open,High,Low,Close,Volume' (UTC)."""
    df = pd.read_csv(path)
    tcol = [c for c in df.columns if "time" in c.lower()][0]
    ts = pd.to_datetime(df[tcol], format="%d.%m.%Y %H:%M:%S.%f")
    out = pd.DataFrame({"o": df["Open"].values, "h": df["High"].values, "l": df["Low"].values,
                        "c": df["Close"].values, "volume": df["Volume"].values}, index=ts)
    out.attrs["price_side"] = "file"
    return out


def _read_generic(path: Path, spec: dict) -> pd.DataFrame:
    """CSV genérico. spec['columns'] mapea timestamp/open/high/low/close/volume/spread_points."""
    cols = spec.get("columns", {})
    df = pd.read_csv(path)
    ts = pd.to_datetime(df[cols.get("timestamp", "timestamp")], format=spec.get("timestamp_format"))
    out = pd.DataFrame({k: df[cols.get(n, n)].values for k, n in
                        [("o", "open"), ("h", "high"), ("l", "low"), ("c", "close")]}, index=ts)
    out["volume"] = df[cols["volume"]].values if "volume" in cols else np.nan
    if "spread_points" in cols:
        out["spread_points"] = df[cols["spread_points"]].values
    out.attrs["price_side"] = spec.get("price_side", "mid")
    return out


def to_utc(idx: pd.DatetimeIndex, source_tz: str) -> pd.DatetimeIndex:
    """Convierte la hora del archivo a UTC (naive)."""
    if idx.tz is not None:
        return idx.tz_convert("UTC").tz_localize(None)
    if source_tz in ("UTC", "GMT", "Etc/UTC"):
        return idx
    if source_tz.upper().startswith("NY+"):
        # Servidor GMT+2/+3 que sigue el DST de Nueva York: server = NY + N horas.
        shift = int(source_tz[3:])
        ny = (idx - pd.Timedelta(hours=shift)).tz_localize(
            "America/New_York", ambiguous=False, nonexistent="shift_forward")
        return ny.tz_convert("UTC").tz_localize(None)
    return idx.tz_localize(source_tz, ambiguous=False, nonexistent="shift_forward") \
              .tz_convert("UTC").tz_localize(None)


# ----------------------------------------------------------------------------
# Carga de un instrumento
# ----------------------------------------------------------------------------

def _expand(raw_dir: Path, pattern: str) -> list[Path]:
    """Un archivo o un patrón glob (p. ej. 'USDJPY/USDJPY_*.csv.gz', un archivo por año)."""
    return sorted(raw_dir.glob(pattern)) if any(ch in pattern for ch in "*?[") else \
        ([raw_dir / pattern] if (raw_dir / pattern).exists() else [])


def _read_file(path, spec: dict) -> pd.DataFrame:
    if isinstance(path, list):
        parts = [_read_file(p, spec) for p in path]
        out = pd.concat(parts)
        out.attrs = parts[0].attrs
        return out
    fmt = spec.get("format", "mt5")
    if fmt == "mt5py":
        return _read_mt5py(path)
    if fmt == "mt5":
        return _read_mt5(path)
    if fmt == "dukascopy":
        return _read_dukascopy(path)
    return _read_generic(path, spec)


def load_raw(cfg: dict, symbol: str) -> pd.DataFrame:
    """Lee los archivos del símbolo y devuelve el DataFrame canónico SIN modelo de spread aplicado.

    Si hay archivos bid y ask separados se usan tal cual (spread real).
    Si sólo hay un archivo, se guarda como 'mid'/'bid' y el spread se aplica luego en costs.py.
    """
    spec = cfg["instruments"][symbol]
    raw_dir = resolve(cfg, cfg["data"]["raw_dir"])
    files = spec.get("files", {})
    missing = [f for f in files.values() if not _expand(raw_dir, f)]
    if not files or missing:
        raise DataMissingError(f"{symbol}: faltan archivos en {raw_dir}: {missing or 'ninguno configurado'}")

    def clean(df):
        attrs = dict(df.attrs)
        df.index = to_utc(pd.DatetimeIndex(df.index), spec.get("source_tz", "UTC"))
        df = df[~df.index.duplicated(keep="first")].sort_index()
        # MT5 entrega velas DIARIAS para los años sin M1: se descartan las que preceden al
        # primer día con historial intradía denso (> 100 velas). Se registra, no se oculta.
        per_day = df.index.normalize().value_counts().sort_index()
        dense = per_day[per_day > 100]
        if len(dense) and dense.index[0] > df.index[0]:
            dropped = int((df.index < dense.index[0]).sum())
            df = df[df.index >= dense.index[0]]
            attrs["dropped_coarse_bars"] = dropped
            attrs["intraday_start"] = str(dense.index[0].date())
        df.attrs = attrs
        return df

    if "bid" in files and "ask" in files:
        bid = clean(_read_file(_expand(raw_dir, files["bid"]), spec))
        ask = clean(_read_file(_expand(raw_dir, files["ask"]), spec))
        idx = bid.index.intersection(ask.index)
        bid, ask = bid.loc[idx], ask.loc[idx]
        out = pd.DataFrame(index=idx)
        for k in "ohlc":
            out[f"bid_{k}"] = bid[k].values
            out[f"ask_{k}"] = ask[k].values
        out["volume"] = bid["volume"].values
        out.attrs.update(has_bid_ask=True, price_side="bid_ask", spread_source="bid_ask_data")
    else:
        f = files.get("mid") or files.get("bid")
        d = clean(_read_file(_expand(raw_dir, f), spec))
        side = d.attrs.get("price_side", "mid")
        if "bid" in files and side == "file":
            side = "bid"
        out = pd.DataFrame(index=d.index)
        for k in "ohlc":
            out[f"px_{k}"] = d[k].values
        out["volume"] = d["volume"].values
        if "spread_points" in d:
            out["spread_points"] = d["spread_points"].values
        out.attrs.update({k: d.attrs[k] for k in ("dropped_coarse_bars", "intraday_start") if k in d.attrs})
        out.attrs.update(has_bid_ask=False, price_side=side,
                         spread_source="bar_spread_column+model" if "spread_points" in d else "model")
    out.index.name = "time_utc"
    vol = out["volume"]
    out.attrs["has_volume"] = bool(vol.notna().mean() > 0.95 and (vol.fillna(0) > 0).mean() > 0.5)
    out.attrs["timeframe"] = infer_timeframe(out.index)
    out.attrs["symbol"] = symbol
    return out


def infer_timeframe(idx: pd.DatetimeIndex) -> str:
    if len(idx) < 3:
        return "unknown"
    d = pd.Series(idx[1:] - idx[:-1]).dt.total_seconds().div(60)
    mode = d.mode().iloc[0]
    for name, m in TF_MINUTES.items():
        if abs(mode - m) < 1e-9:
            return name
    return f"{mode:g}min"


def load_cached(cfg: dict, symbol: str) -> pd.DataFrame:
    cache = resolve(cfg, cfg["data"]["cache_dir"])
    cache.mkdir(parents=True, exist_ok=True)
    spec = cfg["instruments"][symbol]
    raw_dir = resolve(cfg, cfg["data"]["raw_dir"])
    mtimes = [p.stat().st_mtime for f in spec.get("files", {}).values() for p in _expand(raw_dir, f)]
    key = f"{symbol}_{int(max(mtimes)) if mtimes else 0}_{spec.get('source_tz')}.pkl"
    p = cache / key
    if p.exists():
        df = pd.read_pickle(p)
        return df
    df = load_raw(cfg, symbol)
    df.to_pickle(p)
    return df


# ----------------------------------------------------------------------------
# Remuestreo sin look-ahead
# ----------------------------------------------------------------------------

def resample(df: pd.DataFrame, tf: str, prefixes=("bid", "ask", "px")) -> pd.DataFrame:
    """Agrega barras a 'tf'. Etiqueta = apertura; la barra sólo es usable en apertura + tf."""
    rule = {"M1": "1min", "M5": "5min", "M15": "15min", "H1": "1h", "D1": "1D"}[tf]
    agg = {}
    for p in prefixes:
        if f"{p}_o" in df:
            agg.update({f"{p}_o": "first", f"{p}_h": "max", f"{p}_l": "min", f"{p}_c": "last"})
    if "volume" in df:
        agg["volume"] = "sum"
    if "spread_points" in df:
        agg["spread_points"] = "min"
    if "spread_px" in df:
        agg["spread_px"] = "mean"
    out = df.resample(rule, label="left", closed="left").agg(agg)
    first = next(iter(agg))
    out = out[out[first].notna()]
    out["n_sub"] = df[first].resample(rule, label="left", closed="left").count().reindex(out.index)
    out.attrs = dict(df.attrs, timeframe=tf)
    return out


def daily_bars(df: pd.DataFrame, boundary_minutes: int, min_hours: float, price="mid") -> pd.DataFrame:
    """Barras D1 con corte en 'boundary_minutes' UTC. Descarta días con pocas horas (stub del domingo)."""
    shifted = df.copy()
    shifted.index = shifted.index - pd.Timedelta(minutes=boundary_minutes)
    h, l, c, o = (f"{price}_{k}" for k in "hlco")
    d = shifted.resample("1D").agg({o: "first", h: "max", l: "min", c: "last"})
    cnt = shifted[c].resample("1D").count()
    tf_min = TF_MINUTES.get(df.attrs.get("timeframe", "M1"), 1)
    d["hours"] = cnt * tf_min / 60
    d = d[(d["hours"] >= min_hours) & d[c].notna()]
    d.columns = ["o", "h", "l", "c", "hours"]
    return d
