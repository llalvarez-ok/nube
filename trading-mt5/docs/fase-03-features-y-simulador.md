# Fase 3 (adelantada) — Features, simulador y línea base

**Fecha:** 04/10/2026 · **Estado:** probado con datos sintéticos (17 tests). Falta correrlo sobre la grabación real.

## Piezas

| Módulo | Qué hace |
|---|---|
| `research/features/motor.py` | 16 features por tick, todas causales (solo usan el pasado): retornos a 1/5/30/120 s, rango a 30/120 s, ticks por segundo, eficiencia del movimiento, desequilibrio de subas/bajas, spread relativo al promedio de 10 min, antigüedad del tick anterior y hora. |
| `research/estrategias/` | Contrato común (`Senales`): dirección, stop, objetivo y tiempo máximo. `aleatoria` (línea base) y `momentum` V0 (**esqueleto sin validar**). Las decisiones se evalúan como máximo una vez por segundo. |
| `research/sim/simulador.py` | Simula la ejecución tick a tick: filtros de no-operar, tamaño por riesgo (sin redondear hacia arriba), latencia, slippage, rechazos, stops level, stop y objetivo en el servidor, salida por tiempo con latencia, una posición por símbolo, límite de pérdida diaria y de drawdown. |
| `research/sim/metricas.py` | Expectativa en R con cota inferior al 95 %, profit factor, drawdown y desglose del costo. |
| `research/sim/correr.py` | Corre una estrategia sobre los ticks grabados y la compara con varias corridas al azar con las mismas salidas. |

## Decisiones de diseño

- **Dos implementaciones de cada feature:** una vectorizada (rápida) y una de referencia tick a tick (lenta y literal). Los tests verifican que coincidan. El motor en MQL5 se va a validar contra la misma referencia, así investigación y producción calculan exactamente lo mismo.
- **Costos medidos contra el mid del momento de decidir:** medio spread, slippage y deriva por latencia por separado, en la entrada y en la salida. Se verifica que neto = bruto − costos.
- **Supuestos conservadores:** si un tick toca el stop y el objetivo a la vez, se asume el stop. La salida por tiempo sufre latencia. La latencia por defecto es 200 ms (PC hogareña) hasta medirla; con `--latencia-ms status` se usan los pings grabados (mínimo optimista).
- **Siempre contra el azar:** el reporte de cada estrategia incluye corridas al azar con igual frecuencia y salidas.

## Prueba de cordura (datos sintéticos sin ningún patrón)

Sobre 1 millón de ticks de un paseo aleatorio, la estrategia de momentum dio un bruto medio de −0,010 con error estándar 0,023 en 649 operaciones: cero, como corresponde, y el neto negativo por el costo. En una corrida corta de 54 operaciones el bruto había dado −0,16: con muestras chicas, el ruido parece señal.

Velocidad: ~7 s por millón de ticks, incluidas 5 corridas al azar.

## Uso

```
python -m research.sim.correr --raiz <carpeta ATS> --simbolo XAUUSDc \
    --estrategia momentum --params '{"umbral_rango": 0.5, "max_hold_s": 60}' \
    --latencia-ms status --salida reporte_sim.md
```

## Pendiente

- Correr sobre la grabación real y ajustar los supuestos de costo con lo medido.
- Separar en muestra / fuera de muestra / walk-forward y Monte Carlo (Fase 15) antes de considerar cualquier resultado.
- Registro de hipótesis y contador de pruebas (§15.3 del documento de la Fase 1).
