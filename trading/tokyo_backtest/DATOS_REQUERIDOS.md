# Datos requeridos para ejecutar el backtest

**Estado al 08/10/2026: NO hay datos históricos disponibles.** No se ejecutó ningún backtest
sobre datos de mercado y no se informa ningún resultado de rentabilidad.

Verificación hecha:

| Fuente | Resultado |
|---|---|
| Repositorio (`nube`) | Sin archivos de precios (sólo material del canal de YouTube) |
| Google Drive conectado | Sin archivos USDJPY / XAUUSD / JP225 / AUDJPY / Nikkei / M1 |
| Descarga directa (Dukascopy, HistData, Yahoo, Stooq) | Bloqueada por la política de red del entorno (403 del proxy) |

Para correr el estudio necesito que me pases los archivos (subidos al repo en
`trading/tokyo_backtest/data/raw/`, a Drive, o habilitando un dominio de descarga).

## 1. Qué archivos

Un archivo por símbolo, **M1** (preferido) o M5 si no existe M1:

| Símbolo | Archivo esperado | Notas |
|---|---|---|
| USDJPY | `USDJPY_M1.csv` | **Obligatorio**: también convierte JPY a USD para AUDJPY, EURJPY y JP225 |
| AUDJPY | `AUDJPY_M1.csv` | |
| AUDUSD | `AUDUSD_M1.csv` | |
| NZDUSD | `NZDUSD_M1.csv` | |
| EURJPY | `EURJPY_M1.csv` | |
| JP225 | `JP225_M1.csv` | Indicar si el CFD es contado o futuro, la moneda (JPY/USD) y el valor del punto |
| XAUUSD | `XAUUSD_M1.csv` | |

Mínimo útil: **5 años**; ideal: **8–10 años** (p. ej. 2015–2026). Con menos, el split
60/20/20 y el walk-forward 24/6 quedan con muestras demasiado chicas.

Todos los símbolos deberían cubrir el mismo período (para correlaciones y portafolio).

## 2. Formatos aceptados

### Opción A (la más simple): export de MetaTrader 5 de tu broker

En MT5: `Ver > Símbolos > Barras` → elegir símbolo, período M1, rango de fechas →
`Solicitar` → `Exportar barras`. Genera:

```
<DATE>	<TIME>	<OPEN>	<HIGH>	<LOW>	<CLOSE>	<TICKVOL>	<VOL>	<SPREAD>
2024.01.02	00:00:00	140.951	140.968	140.940	140.955	57	0	12
```

- Precios **BID**, hora del **servidor del broker**. En `config/default.yaml`, `source_tz`
  por defecto es `"NY+7"` (GMT+2 invierno / GMT+3 verano, lo más común). **Decime el
  nombre del broker y el horario del servidor**; `check-data` igual lo verifica contra la
  apertura semanal (domingo 17:00 Nueva York).
- La columna `<SPREAD>` (en puntos) se usa como cota inferior del spread.
- Ventaja: son exactamente los precios y símbolos que vas a operar.
- Ojo: muchos brokers sólo guardan pocos años de M1. Si el historial es corto, combinar con B.

### Opción B (la mejor calidad): Dukascopy con BID y ASK separados

Desde dukascopy.com → Historical Data Feed (o la herramienta `dukascopy-node`):
un CSV **BID** y uno **ASK** por símbolo, M1, horario **UTC**:

```
Gmt time,Open,High,Low,Close,Volume
02.01.2024 00:00:00.000,140.951,140.968,140.940,140.955,123.45
```

Configurar `files: {bid: USDJPY_BID_M1.csv, ask: USDJPY_ASK_M1.csv}`, `format: dukascopy`,
`source_tz: UTC`. Con bid/ask el spread es real y no hace falta el modelo.

Si preferís que lo descargue yo, habilitá `datafeed.dukascopy.com` en la red del
entorno (configuración del entorno → Network access → Allowed domains).

### Opción C: CSV genérico

Cualquier CSV con timestamp y OHLC: se mapea con `format: generic` y `columns:` en el config.

## 3. Especificaciones del broker (para que los costos sean reales)

Por cada símbolo, en `config/default.yaml`. Los valores actuales dicen `# SUPUESTO`:

- Spread típico por hora UTC (sobre todo 21:00–01:00 UTC, que es el rollover)
- Comisión por lote ida y vuelta (USD)
- Tamaño de contrato, lote mínimo y paso de lote
- JP225: moneda, valor del punto, contrato contado vs futuro
- Swap long/short (sólo influye si se extiende el cierre más allá de la sesión)
- Moneda de la cuenta (por defecto USD)

## 4. Opcional

- **Calendario económico** (`data/news/calendar.csv`): `datetime_utc,currency,impact,event`
  (por ejemplo, export de ForexFactory o Investing). Sin él, la comparación con/sin
  noticias no se hace (no se asume que el filtro mejore nada).
- Volumen: los exports de MT5 traen tick volume (sirve para VWAP en FX/CFD).
  Sin volumen, la estrategia E se marca "NO DISPONIBLE".
