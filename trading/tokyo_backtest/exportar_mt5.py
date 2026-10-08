"""Exporta el historial M1 desde tu MetaTrader 5 (Exness u otro broker) para el backtest.

Se ejecuta EN TU PC (Windows), con MetaTrader 5 abierto y logueado:

    pip install MetaTrader5 pandas
    python exportar_mt5.py            # todos los símbolos
    python exportar_mt5.py XAUUSD     # sólo los indicados

Genera la carpeta `datos_mt5/` con:
  - <SIMBOLO>/<SIMBOLO>_<AÑO>.csv.gz   velas M1 (precio BID, hora del servidor, spread por vela)
  - especificaciones.json               contrato, punto, lote mínimo, swap, moneda de cada símbolo
  - resumen.txt                         qué se exportó y desde qué fecha

No lee ni guarda tu número de cuenta, saldo ni contraseña: sólo precios y
especificaciones públicas de los símbolos.
"""
from __future__ import annotations

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

try:
    import MetaTrader5 as mt5
    import pandas as pd
except ImportError:
    sys.exit("Falta instalar dependencias:  pip install MetaTrader5 pandas")

# Símbolos pedidos y nombres alternativos según el broker (Exness agrega sufijos como 'm' o 'c').
WANTED = {
    "USDJPY": ["USDJPY"],
    "AUDJPY": ["AUDJPY"],
    "AUDUSD": ["AUDUSD"],
    "NZDUSD": ["NZDUSD"],
    "EURJPY": ["EURJPY"],
    "JP225": ["JP225", "JPN225", "NIKKEI225", "NIKKEI", "JP225CASH"],
    "XAUUSD": ["XAUUSD", "GOLD"],
}
FIRST_YEAR = 2010
OUT = Path("datos_mt5")

SPEC_FIELDS = ["name", "description", "path", "digits", "point", "trade_contract_size", "volume_min",
               "volume_step", "volume_max", "currency_base", "currency_profit", "currency_margin",
               "spread", "spread_float", "swap_long", "swap_short", "swap_mode", "swap_rollover3days",
               "trade_calc_mode", "trade_tick_size", "trade_tick_value"]


def find_symbol(candidates: list[str]) -> str | None:
    names = [s.name for s in (mt5.symbols_get() or [])]
    upper = {n.upper(): n for n in names}
    for c in candidates:                       # nombre exacto
        if c in upper:
            return upper[c]
    for c in candidates:                       # con sufijo (USDJPYm, XAUUSDc, ...)
        # el más corto primero: XAUUSDm antes que XAUUSD247m (variante 24/7 de Exness)
        hits = sorted((n for n in names if n.upper().startswith(c) and len(n) <= len(c) + 2
                       and not n[len(c):].isdigit() and "247" not in n),
                      key=lambda n: (len(n), n))
        if hits:
            return hits[0]
    return None


def fetch_year(symbol: str, year: int) -> pd.DataFrame | None:
    start = datetime(year, 1, 1, tzinfo=timezone.utc)
    end = min(datetime(year + 1, 1, 1, tzinfo=timezone.utc), datetime.now(timezone.utc))
    rates = None
    for _ in range(3):                         # el terminal descarga el historial bajo demanda
        rates = mt5.copy_rates_range(symbol, mt5.TIMEFRAME_M1, start, end)
        if rates is not None and len(rates):
            break
        time.sleep(2)
    if rates is None or len(rates) == 0:
        return None
    df = pd.DataFrame(rates)
    df["time"] = pd.to_datetime(df["time"], unit="s")
    df = df[df["time"].dt.year == year]          # MT5 a veces devuelve velas fuera del rango pedido
    if df.empty:
        return None
    df["time"] = df["time"].dt.strftime("%Y-%m-%d %H:%M:%S")
    return df[["time", "open", "high", "low", "close", "tick_volume", "spread", "real_volume"]]


def main():
    if not mt5.initialize():
        sys.exit(f"No pude conectarme a MetaTrader 5 ({mt5.last_error()}). Abrí MT5, logueate y probá de nuevo.")
    acc, term = mt5.account_info(), mt5.terminal_info()
    only = [a.upper() for a in sys.argv[1:]]        # p. ej.: python exportar_mt5.py XAUUSD
    targets = {k: v for k, v in WANTED.items() if not only or k in only}
    if not targets:
        sys.exit(f"Símbolos válidos: {', '.join(WANTED)}")
    for t in targets:
        if (OUT / t).exists() and any((OUT / t).iterdir()):
            sys.exit(f"Ya existe {(OUT / t).resolve()} con datos. Borrala (o renombrala) y ejecutá de nuevo.")
    OUT.mkdir(exist_ok=True)
    spec_file = OUT / "especificaciones.json"
    old_specs = json.loads(spec_file.read_text(encoding="utf-8")) if spec_file.exists() else {}
    specs = {**old_specs, "_broker": {"company": getattr(acc, "company", None), "server": getattr(acc, "server", None),
                         "account_currency": getattr(acc, "currency", None),
                         "max_bars_setting": getattr(term, "maxbars", None),
                         "exported_at_utc": datetime.now(timezone.utc).isoformat()}}
    lines = [f"Broker: {specs['_broker']['company']} / {specs['_broker']['server']}"]
    if term is not None and term.maxbars < 10_000_000:
        mt5.shutdown()
        sys.exit(f"ALTO: 'Máx. barras en el gráfico' está en {term.maxbars:,}, así que MT5 sólo entrega unos meses "
                 "de M1.\nPoné 'Unlimited' en Herramientas > Opciones > Gráficos > 'Máx. barras en el gráfico', "
                 "cerrá MT5 por completo, volvé a abrirlo y ejecutá de nuevo este script.")
    for target, cands in targets.items():
        sym = find_symbol(cands)
        if sym is None:
            print(f"{target}: no encontrado en este broker")
            lines.append(f"{target}: NO ENCONTRADO")
            continue
        mt5.symbol_select(sym, True)
        info = mt5.symbol_info(sym)
        specs[target] = {k: getattr(info, k, None) for k in SPEC_FIELDS}
        d = OUT / target
        d.mkdir(exist_ok=True)
        years, rows = [], 0
        for y in range(FIRST_YEAR, datetime.now().year + 1):
            df = fetch_year(sym, y)
            if df is None:
                continue
            df.to_csv(d / f"{target}_{y}.csv.gz", index=False, compression="gzip")
            years.append(y)
            rows += len(df)
            print(f"{target} ({sym}) {y}: {len(df):,} velas")
        msg = (f"{target} -> {sym}: {rows:,} velas M1, años {years[0]}-{years[-1]}" if years
               else f"{target} -> {sym}: SIN HISTORIAL M1")
        print(msg)
        lines.append(msg)
    (OUT / "especificaciones.json").write_text(json.dumps(specs, indent=2, default=str), encoding="utf-8")
    res = OUT / "resumen.txt"
    prev = res.read_text(encoding="utf-8").splitlines()[1:] if res.exists() else []
    prev = [l for l in prev if l.split(" ")[0].rstrip(":") not in targets]
    res.write_text("\n".join(lines[:1] + prev + lines[1:]), encoding="utf-8")
    mt5.shutdown()
    print(f"\nListo. Carpeta: {OUT.resolve()}")


if __name__ == "__main__":
    main()
