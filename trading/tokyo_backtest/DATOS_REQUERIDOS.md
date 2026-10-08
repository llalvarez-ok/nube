# Datos requeridos para ejecutar el backtest

**Estado al 08/10/2026: NO hay datos históricos disponibles.** No se ejecutó ningún backtest
sobre datos de mercado y no se informa ningún resultado de rentabilidad.

Verificación hecha:

| Fuente | Resultado |
|---|---|
| Repositorio (`nube`) | Sin archivos de precios (sólo material del canal de YouTube) |
| Google Drive conectado | Sin archivos USDJPY / XAUUSD / JP225 / AUDJPY / Nikkei / M1 |
| Descarga directa (Dukascopy, HistData, Yahoo, Stooq) | Bloqueada por la política de red del entorno (403 del proxy) |

Para correr el estudio necesito los archivos en `trading/tokyo_backtest/data/raw/`.
Lo más simple es el camino de la sección 0.

## 0. Camino recomendado: exportar desde tu MetaTrader 5 (Exness)

Claude corre en un servidor en la nube y no puede entrar a tu PC, así que la exportación
la hace un script en tu computadora, con MT5 abierto:

1. **Instalar Python** (una sola vez): https://www.python.org/downloads/ → al instalar, tildar
   *"Add Python to PATH"*.
2. **En MT5**: Herramientas → Opciones → Gráficos → *Máx. barras en el gráfico* = **Unlimited**
   → Aceptar → cerrar y volver a abrir MT5 (logueado).
3. **Descargar el script** [`exportar_mt5.py`](exportar_mt5.py) (en GitHub: abrir el archivo →
   botón *Download raw file*) y guardarlo en una carpeta, por ejemplo `C:\backtest`.
4. **Abrir una terminal** en esa carpeta (en el Explorador, escribir `cmd` en la barra de
   dirección y Enter) y ejecutar:
   ```
   pip install MetaTrader5 pandas
   python exportar_mt5.py
   ```
   Tarda unos minutos. Crea la carpeta `datos_mt5` con un archivo por símbolo y año,
   `especificaciones.json` (contrato, punto, swap, moneda: así los costos dejan de ser supuestos)
   y `resumen.txt`. No guarda número de cuenta, saldo ni contraseña.
5. **Subir la carpeta a GitHub**: en el repo `nube`, elegir la rama
   `claude/confident-darwin-t42tpn`, entrar a `trading/tokyo_backtest/data/raw/` →
   *Add file* → *Upload files* → arrastrar **el contenido** de `datos_mt5` (las carpetas de cada
   símbolo y los dos archivos) → *Commit changes*.
6. Avisarle a Claude. Además conviene decirle **qué tipo de cuenta Exness usás** (Standard,
   Pro, Raw Spread, Zero), porque la comisión depende de eso.

El config ya está preparado para este formato (`format: mt5py`, servidor Exness en UTC; `check-data`
lo verifica). Si Exness no tiene M1 suficientemente antiguo para algún símbolo, el reporte de
calidad lo va a mostrar y se puede completar con Dukascopy (opción B).

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

### Opción A2: export manual de MetaTrader 5 (sin Python)

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
