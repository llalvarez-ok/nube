# Tokyo Session Backtest

Framework de investigación cuantitativa para estrategias de la **sesión asiática / Tokio**
(00:00–09:00 UTC = 21:00–06:00 ART). El objetivo no es encontrar lo que más ganó, sino
determinar **si existe una ventaja estadística robusta** y en qué condiciones.

> Estado: el framework está completo y probado con datos sintéticos (sólo como prueba de
> software). **No se corrió sobre datos reales porque no hay datos disponibles.** Ver
> [DATOS_REQUERIDOS.md](DATOS_REQUERIDOS.md).

## Cómo ejecutarlo

```bash
cd trading/tokyo_backtest
pip install -r requirements.txt
# 1) copiar los CSV a data/raw/ (ver DATOS_REQUERIDOS.md) y ajustar config/default.yaml
python run.py check-data          # SIEMPRE primero: calidad, timezone, gaps, bid/ask, símbolo correcto
python run.py run                 # estudio completo -> output/
python run.py run --symbols USDJPY JP225 --strategies C_tokyo_or_breakout D_tokyo_or_failed_breakout
python tests/test_lookahead.py    # tests de look-ahead y reglas de ejecución
python tests/run_smoke.py /tmp/smoke   # prueba de punta a punta con datos SINTÉTICOS
```

Salida en `output/`:

| Archivo | Contenido |
|---|---|
| `REPORT.md` | Reporte completo: rankings, OOS, WF, Monte Carlo, MAE/MFE, costos, correlación, conclusión |
| `data_quality.md` | Verificación de datos por símbolo |
| `selection.json` | Configuraciones elegidas con IS+VAL, **congeladas con hash antes de mirar el OOS** |
| `tables/*.csv` | Tabla final, todas las configuraciones (IS/VAL/OOS), top 10 por categoría, WF, MC, costos, hora, día, volatilidad, noticias, VWAP, correlación |
| `trade_log/frozen_trades.csv` | Cada operación de las configuraciones congeladas con todas las columnas pedidas |
| `charts/*.png` | Equity, drawdown, retornos mensuales/anuales, distribuciones, heatmaps, WF, Monte Carlo |

## Estructura

```
config/default.yaml     todos los parámetros (horarios, instrumentos, costos, grillas, validación)
run.py                  CLI
tokyo_bt/
  data.py               lectores MT5 / Dukascopy / genérico, conversión a UTC, remuestreo
  quality.py            verificación de datos (regla 36)
  costs.py              spread (bid/ask real > columna MT5 > modelo), slippage, comisión, swap, conversión a USD
  indicators.py         ATR, VWAP, swings, régimen de volatilidad — indexados por hora de disponibilidad
  market.py             prepara un símbolo: barras bid/ask, M5, indicadores alineados, sesiones
  strategies.py         señales A–E
  engine.py             simulación barra a barra (M1), SL/TP/BE/trailing/parciales, MAE/MFE
  postprocess.py        R neto, filtro de rango, modos de posición, noticias, split 60/20/20
  research.py           grilla, robustez por vecindario, selección congelada, walk-forward
  metrics.py            métricas en R y de cuenta, Deflated Sharpe, Benjamini-Hochberg
  analysis.py           Monte Carlo, MAE/MFE, hora/día/volatilidad, correlación
  charts.py, report.py  gráficos y reporte
tests/                  tests de look-ahead, generador sintético, prueba de humo
```

## Metodología

### Tiempo y datos
- Todo en UTC. La hora del archivo se convierte con `source_tz` (`UTC`, zona IANA o
  `NY+7` para servidores GMT+2/+3 que siguen el DST de Nueva York). Japón no usa DST, así que
  la sesión de Tokio es fija en UTC; el horario del broker no define ninguna regla.
- Una barra con índice `t` cubre `[t, t+tf)` y su información existe recién en `t+tf`.
- Sesiones con cobertura < 90% (feriados, pausas del CFD, huecos) se excluyen.

### Sin look-ahead
- Asian range 00:00–03:00 y Opening Range sólo con barras cerradas; se usan a partir del cierre.
- ATR diario (D1, 14) calculado con días **anteriores** completos. ATR del trailing (H1, 14) con
  barras H1 cerradas. VWAP anclado a 00:00 UTC, valor al cierre de cada barra.
- Swings M5 (fractal 2-2) confirmados recién 2 velas después.
- Régimen de volatilidad: percentil del ATR contra las 252 sesiones **anteriores**.
- Entrada en la apertura de la barra M1 siguiente al cierre de la vela M5 de confirmación.
- `tests/test_lookahead.py` verifica que truncar los datos no cambie ninguna señal previa.

### Ejecución y costos (conservador)
- Long entra al ASK y sale al BID; short al revés. Slippage adverso en entradas y stops.
- Stop con gap: se llena en la apertura (peor que el nivel). TP límite sin mejora.
- Si en la misma barra se tocan SL y TP: **SL primero**.
- Tras TP parcial, el stop en breakeven se evalúa en la misma barra (conservador).
- Spread: bid/ask real si existe; si no, `max(columna <SPREAD> de MT5, modelo por hora)`.
  El modelo del config está marcado `# SUPUESTO` y debe reemplazarse por valores del broker.
- R = distancia planificada entre la entrada esperada y el stop. Costos incluidos en R:
  una pérdida completa vale algo más de −1R.
- Sensibilidad: spread ×1/×1.5/×2 y slippage ×1/×2/×3. **NO ROBUSTA** si la expectancy pre-OOS
  pasa a ≤ 0 con spread ×1.5 o slippage ×2.

### Estrategias
| | Nombre | Grilla por defecto |
|---|---|---|
| A | Asian Range Breakout | buffer {0, .025, .05, .10} ATR × SL {extremo opuesto, 0.5/0.75/1.0 rango, 0.5/0.75/1.0/1.25 ATR} × TP {0.5,1,1.5,2,3 R; trailing 0.5 ATR, 1 ATR, swing M5} × filtro de rango {6} |
| B | Asian Failed Breakout | buffer SL × profundidad mínima del sweep {0…0.5 ATR} × salida {midpoint, extremo opuesto, 50/50 con BE} × filtro |
| C | Tokyo OR Breakout | OR {5, 15, 30, 60 min} × buffer × SL × TP |
| D | Tokyo OR Failed Breakout | OR × profundidad × buffer SL × salida |
| E | Breakout + VWAP | con VWAP vs **sin VWAP (control)** sobre la misma grilla; test pareado de Wilcoxon |

Una operación por breakout y por dirección. Trailing: TP1 = 1R (cierra 50% configurable) →
stop a breakeven → trailing por ATR o último swing M5. Cierre forzado a las 09:00 UTC.

### Selección (anti curve-fitting)
1. **IS (60%)**: métricas de toda la grilla. Para cada configuración se calcula la *expectancy
   robusta* = mediana de la configuración y sus vecinos (±1 paso en cada eje). Se rankea por
   expectancy robusta → PF → DD → estabilidad, exigiendo un mínimo de operaciones.
2. **VALIDATION (20%)**: las 10 mejores candidatas IS se confirman; se elige la de mejor
   `min(expectancy robusta IS, expectancy VAL)`.
3. Se **congela** la selección (`selection.json` + hash).
4. **OOS (20%)**: recién ahora se mide. Nunca vuelve a la selección.
5. **Walk-forward** 24/6/6 meses sólo sobre el período pre-OOS: en cada ventana se re-elige por
   el mismo criterio y se mide en el bloque siguiente.
6. Sesgo de minería: cantidad de configuraciones probadas, Benjamini-Hochberg y Deflated Sharpe.
7. **FRÁGIL** si más del 50% del beneficio pre-OOS viene de un año, si menos del 60% de las
   ventanas WF son positivas o si menos de la mitad de los vecinos de parámetros son positivos.

Veredicto: sólo es **CANDIDATA ROBUSTA** si IS, VAL y OOS son positivos, PF OOS > 1.1, no es
frágil, resiste costos y DSR > 0.95. Aun así, el siguiente paso es forward test en demo.

### Gestión de capital
Riesgo 0.25 / 0.5 / 1.0% sobre equity **actual** (PnL cerrado al momento de la entrada), lotes
redondeados al paso del broker; comparación con lote fijo. Monte Carlo de 10.000 simulaciones
(permutación para riesgo de secuencia, bootstrap para la distribución del retorno).

## Limitaciones conocidas
- Con datos M5 la simulación intrabarra es menos precisa (se aplica SL primero).
- El spread del modelo es un supuesto hasta que se carguen los valores del broker.
- El split usa el rango de fechas de cada símbolo; para comparar activos conviene que todos
  cubran el mismo período.
- La correlación se mide sobre resultados diarios en R y retornos de sesión; el N efectivo se
  estima por autovalores (aproximación).
