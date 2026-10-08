"""Verificación de datos ANTES de cualquier backtest (regla 36).

Para cada símbolo comprueba: cobertura temporal, timeframe, timezone (por la hora
de apertura semanal), bid/ask, spreads, volumen, gaps, cobertura de la sesión de
Tokio, coherencia OHLC, outliers y si el rango de precios corresponde al activo.
Nada se corrige silenciosamente: los problemas se reportan.
"""
from __future__ import annotations

import json

import numpy as np
import pandas as pd

from .config import hhmm_to_minutes, resolve
from .data import TF_MINUTES, DataMissingError, load_cached

CRITICAL = "CRÍTICO"
WARN = "ADVERTENCIA"
OK = "OK"


def check_symbol(cfg: dict, symbol: str) -> dict:
    spec = cfg["instruments"][symbol]
    rep = {"symbol": symbol, "issues": []}

    def issue(level, msg):
        rep["issues"].append({"level": level, "msg": msg})

    try:
        df = load_cached(cfg, symbol)
    except DataMissingError as e:
        issue(CRITICAL, str(e))
        rep["status"] = CRITICAL
        return rep
    except Exception as e:  # formato ilegible
        issue(CRITICAL, f"No se pudo leer: {type(e).__name__}: {e}")
        rep["status"] = CRITICAL
        return rep

    pfx = "bid" if df.attrs.get("has_bid_ask") else "px"
    o, h, l, c = (df[f"{pfx}_{k}"] for k in "ohlc")
    idx = df.index
    tf = df.attrs["timeframe"]
    rep.update(rows=len(df), first=str(idx[0]), last=str(idx[-1]),
               years=round((idx[-1] - idx[0]).days / 365.25, 2), timeframe=tf,
               has_bid_ask=bool(df.attrs.get("has_bid_ask")), price_side=df.attrs.get("price_side"),
               has_volume=bool(df.attrs.get("has_volume")),
               spread_source=df.attrs.get("spread_source"))

    if df.attrs.get("dropped_coarse_bars"):
        rep["intraday_start"] = df.attrs["intraday_start"]
        rep["dropped_coarse_bars"] = df.attrs["dropped_coarse_bars"]
        issue(WARN, f"Se descartaron {df.attrs['dropped_coarse_bars']} velas no intradía (diarias) anteriores al "
                    f"{df.attrs['intraday_start']}: el historial M1 real empieza ahí.")
    if df.attrs.get("dropped_isolated_bars"):
        rep["dropped_isolated_bars"] = df.attrs["dropped_isolated_bars"]
        issue(WARN, f"Se descartaron {df.attrs['dropped_isolated_bars']} velas aisladas (restos de velas diarias).")
    if "spread_points" in df and not df.attrs.get("has_bid_ask"):
        z = (df["spread_points"].fillna(0) == 0).groupby(df.index.year).mean()
        rep["spread_zero_share_by_year"] = {int(k): round(float(v), 3) for k, v in z.items()}
        if (z > 0.5).any():
            fb = spec["spread_model"].get("zero_fallback")
            issue(WARN, f"Años sin dato de spread (columna en 0): {[int(k) for k in z[z > 0.5].index]}. "
                        + (f"Se usa el valor de reemplazo medido de {fb} pips." if fb is not None
                           else "Se usa el piso del modelo: configurar spread_model.zero_fallback."))
    if tf not in ("M1", "M5"):
        issue(CRITICAL, f"Timeframe inferido {tf}: se requiere M1 (preferido) o M5 para ejecutar.")
    elif tf == "M5":
        issue(WARN, "Sólo M5: la simulación intrabarra es menos precisa (SL primero en ambigüedad).")
    if rep["years"] < 5:
        issue(WARN, f"Sólo {rep['years']} años: split 60/20/20 y walk-forward 24/6 quedan con poca muestra.")

    # Coherencia OHLC
    bad = ((h < np.maximum(o, c) - 1e-12) | (l > np.minimum(o, c) + 1e-12) | (h < l)).sum()
    nonpos = ((o <= 0) | (c <= 0)).sum()
    rep["ohlc_inconsistent_rows"] = int(bad)
    rep["nonpositive_rows"] = int(nonpos)
    if bad or nonpos:
        issue(WARN if (bad + nonpos) < len(df) * 1e-4 else CRITICAL,
              f"{bad} barras OHLC incoherentes y {nonpos} precios <= 0.")

    # ¿El símbolo es el activo pedido? (rango de precios esperado)
    lo, hi = spec.get("expected_price_range", [None, None])
    rep["price_min"], rep["price_max"] = float(l.min()), float(h.max())
    if lo is not None and (rep["price_min"] < lo or rep["price_max"] > hi):
        issue(CRITICAL, f"Precios [{rep['price_min']}, {rep['price_max']}] fuera del rango esperado "
                        f"{[lo, hi]}: ¿símbolo equivocado, escala distinta (JP225 x10) o datos corruptos?")

    # Outliers de retorno
    r = np.log(c).diff()
    mad = (r - r.median()).abs().median() * 1.4826
    jumps = r.abs() > max(25 * mad, 1e-9)
    rep["return_outliers"] = int(jumps.sum())
    if jumps.sum():
        top = r[jumps].abs().sort_values(ascending=False).head(5)
        rep["return_outliers_top"] = {str(k): round(float(v), 5) for k, v in top.items()}
        issue(WARN, f"{int(jumps.sum())} saltos > 25 MAD (revisar ticks malos / rolls de futuros).")

    # Duplicados / orden ya limpiados en carga; gaps intrasemana
    step = pd.Timedelta(minutes=TF_MINUTES.get(tf, 1))
    gaps = pd.Series(idx[1:] - idx[:-1], index=idx[1:])
    weekend = (gaps > pd.Timedelta(hours=36))
    intraweek = gaps[(gaps > step * 30) & ~weekend]
    rep["intraweek_gaps_gt_30bars"] = int(len(intraweek))
    rep["largest_intraweek_gaps"] = {str(k): str(v) for k, v in intraweek.sort_values(ascending=False).head(10).items()}

    # Timezone: hora UTC de la primera barra de cada semana
    week_open = idx[1:][weekend.values]
    if len(week_open):
        hrs = pd.Series(week_open.hour + week_open.minute / 60)
        rep["weekly_open_hour_utc"] = {f"{k:g}": int(v) for k, v in hrs.value_counts().head(5).items()}
        # FX abre domingo 17:00 NY = 21:00 UTC (verano) / 22:00 UTC (invierno)
        ny = week_open.tz_localize("UTC").tz_convert("America/New_York")
        consistent = ((ny.hour >= 16) & (ny.hour <= 18)).mean()
        rep["weekly_open_consistent_with_17NY"] = round(float(consistent), 3)
        if spec.get("asset_class") == "fx" and consistent < 0.8:
            issue(CRITICAL, f"Sólo {consistent:.0%} de las aperturas semanales caen ~17:00 NY: "
                            f"timezone (source_tz={spec.get('source_tz')}) probablemente mal configurado.")

    # Cobertura de la sesión de Tokio por día
    s0, s1 = hhmm_to_minutes(cfg["session"]["start_utc"]), hhmm_to_minutes(cfg["session"]["end_utc"])
    mins = idx.hour * 60 + idx.minute
    in_sess = (mins >= s0) & (mins < s1)
    per_day = pd.Series(1, index=idx[in_sess]).groupby(idx[in_sess].normalize()).sum()
    expected = (s1 - s0) / TF_MINUTES.get(tf, 1)
    cov = per_day / expected
    weekdays = cov[cov.index.dayofweek < 5]
    rep["session_days"] = int(len(weekdays))
    rep["session_coverage_median"] = round(float(weekdays.median()), 3) if len(weekdays) else 0.0
    min_cov = cfg["session"]["min_session_coverage"]
    rep["session_days_below_min_coverage"] = int((weekdays < min_cov).sum())
    if len(weekdays) and (weekdays < min_cov).mean() > 0.1:
        issue(WARN, f"{(weekdays < min_cov).mean():.0%} de las sesiones con cobertura < {min_cov:.0%} "
                    "(feriados, pausas del CFD o huecos de datos). Esas sesiones se excluyen.")
    # Perfil por hora (detecta pausas diarias del CFD)
    by_hour = pd.Series(1, index=idx).groupby(idx.hour).sum()
    rep["bars_by_hour_utc"] = {int(k): int(v) for k, v in by_hour.items()}

    # Spread
    if df.attrs.get("has_bid_ask"):
        spr = (df["ask_o"] - df["bid_o"]) / spec["pip"]
        rep["spread_pips_by_hour_median"] = {int(k): round(float(v), 2) for k, v in spr.groupby(idx.hour).median().items()}
        if (spr < 0).any():
            issue(CRITICAL, f"{int((spr < 0).sum())} barras con ask < bid.")
    elif "spread_points" in df:
        spr = df["spread_points"] * spec["point"] / spec["pip"]
        rep["spread_pips_by_hour_median"] = {int(k): round(float(v), 2) for k, v in spr.groupby(idx.hour).median().items()}
        issue(WARN, "Sin bid/ask: se usa la columna de spread por barra (mínimo) combinada con el modelo del config.")
    else:
        issue(WARN, "Sin bid/ask ni spread por barra: se usa el MODELO de spread del config (SUPUESTO).")

    if not df.attrs.get("has_volume"):
        issue(WARN, "Sin volumen utilizable: VWAP (estrategia E) no disponible para este símbolo.")

    rep["status"] = CRITICAL if any(i["level"] == CRITICAL for i in rep["issues"]) else \
        (WARN if rep["issues"] else OK)
    return rep


def check_all(cfg: dict, symbols: list[str]) -> dict:
    reps = {s: check_symbol(cfg, s) for s in symbols}
    out = resolve(cfg, cfg["project"]["output_dir"])
    out.mkdir(parents=True, exist_ok=True)
    with open(out / "data_quality.json", "w", encoding="utf-8") as fh:
        json.dump(reps, fh, indent=2, ensure_ascii=False)
    lines = ["# Verificación de datos\n"]
    for s, r in reps.items():
        lines.append(f"## {s} — {r['status']}\n")
        for k in ("rows", "first", "last", "years", "timeframe", "has_bid_ask", "price_side", "has_volume",
                  "spread_source", "price_min", "price_max", "session_coverage_median",
                  "weekly_open_hour_utc", "weekly_open_consistent_with_17NY", "intraweek_gaps_gt_30bars"):
            if k in r:
                lines.append(f"- {k}: {r[k]}")
        for i in r["issues"]:
            lines.append(f"- **{i['level']}**: {i['msg']}")
        lines.append("")
    (out / "data_quality.md").write_text("\n".join(lines), encoding="utf-8")
    return reps
