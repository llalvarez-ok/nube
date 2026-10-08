# Tokyo Session Backtest — reporte


Selección congelada: `selection.json` (hash `76ecd438aa06d05a`). El OOS se midió después de congelarla y no se usó para elegir ningún parámetro.

## 0. Datos verificados

| symbol | status | first | last | years | tf | bid_ask | volume | spread |
|---|---|---|---|---|---|---|---|---|
| USDJPY | ADVERTENCIA | 2021-07-16 00:00:00 | 2026-10-08 21:33:00 | 5.230 | M1 | False | True | bar_spread_column+model |
| AUDJPY | ADVERTENCIA | 2021-07-16 00:00:00 | 2026-10-08 21:34:00 | 5.230 | M1 | False | True | bar_spread_column+model |
| AUDUSD | ADVERTENCIA | 2021-07-16 00:00:00 | 2026-10-08 21:35:00 | 5.230 | M1 | False | True | bar_spread_column+model |
| NZDUSD | ADVERTENCIA | 2021-07-16 00:00:00 | 2026-10-08 21:37:00 | 5.230 | M1 | False | True | bar_spread_column+model |
| EURJPY | ADVERTENCIA | 2021-07-16 00:00:00 | 2026-10-08 20:59:00 | 5.230 | M1 | False | True | bar_spread_column+model |
| JP225 | ADVERTENCIA | 2021-07-16 00:00:00 | 2026-10-08 20:59:00 | 5.230 | M1 | False | True | bar_spread_column+model |
| XAUUSD | ADVERTENCIA | 2017-04-27 00:00:00 | 2026-10-08 20:57:00 | 9.450 | M1 | False | True | bar_spread_column+model |

Detalle completo en `data_quality.md`.

## 1. Tabla final (configuración congelada por estrategia + activo)

Orden: rango compuesto de (1) expectancy pre-OOS, (2) profit factor VAL, (3) max DD, (4) robustez de vecindario, (5) expectancy OOS. No se ordena por beneficio neto.

| Strategy | Asset | Timeframe | Trades (OOS) | Win Rate (OOS) | PF (OOS) | Expectancy R (OOS) | Expectancy R (pre-OOS) | Net Return % (todo, 0.5%) | Max DD % (todo) | Sharpe | Sortino | Average R | Best parameter region | Worst parameter region | Veredicto | Flags |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A_asian_range_breakout | JP225 | M1 ejecución / M5 señal | 53 | 0.415 | 0.946 | -0.012 | 0.035 | 3.299 | 3.869 | 0.302 | 0.490 | 0.025 | buffer_atr=0.1, sl=atr_1.25, tp=r_2.0, rf=btw_0.50_1.50 | buffer_atr=0.025, sl=range_0.50, tp=r_0.5, rf=none | SIN VENTAJA: se degrada fuera de muestra |  |
| A_asian_range_breakout | EURJPY | M1 ejecución / M5 señal | 151 | 0.430 | 0.902 | -0.033 | 0.038 | 6.125 | 6.854 | 0.274 | 0.426 | 0.022 | buffer_atr=0.1, sl=atr_0.50, tp=r_3.0, rf=gt_0.25 | buffer_atr=0.0, sl=range_0.50, tp=r_0.5, rf=none | SIN VENTAJA: se degrada fuera de muestra | FRÁGIL: sólo 50% de ventanas WF positivas |
| C_tokyo_or_breakout | USDJPY | M1 ejecución / M5 señal | 269 | 0.494 | 0.898 | -0.016 | 0.007 | 0.751 | 4.591 | 0.066 | 0.097 | 0.002 | buffer_atr=0.0, or_minutes=5, sl=atr_1.00, tp=r_2.0 | buffer_atr=0.1, or_minutes=30, sl=or_opposite, tp=r_1.0 | SIN VENTAJA: se degrada fuera de muestra | FRÁGIL: 84% del beneficio pre-OOS en un solo año; sólo 50% de ventanas WF positivas |
| E_tokyo_breakout_vwap | USDJPY | M1 ejecución / M5 señal | 184 | 0.500 | 0.863 | -0.033 | 0.033 | 8.557 | 8.375 | 0.411 | 0.661 | 0.019 | buffer_atr=0.05, sl=range_opposite, tp=r_2.0, vwap_filter=False | buffer_atr=0.0, sl=atr_1.00, tp=r_1.0, vwap_filter=True | SIN VENTAJA: se degrada fuera de muestra | FRÁGIL: 59% del beneficio pre-OOS en un solo año; sólo 50% de ventanas WF positivas |
| E_tokyo_breakout_vwap | JP225 | M1 ejecución / M5 señal | 63 | 0.444 | 0.989 | -0.001 | 0.003 | 0.309 | 2.258 | 0.053 | 0.082 | 0.002 | buffer_atr=0.05, sl=atr_1.00, tp=trail_atr_1.0, vwap_filter=True, rf=gt_0.50 | buffer_atr=0.0, sl=range_opposite, tp=r_1.0, vwap_filter=False, rf=none | SIN VENTAJA: se degrada fuera de muestra | FRÁGIL: 65% del beneficio pre-OOS en un solo año; sólo 25% de ventanas WF positivas NO ROBUSTA: expectancy <= 0 con spread x1.5/slip x1, spread x1/slip x2 |
| A_asian_range_breakout | USDJPY | M1 ejecución / M5 señal | 162 | 0.531 | 0.879 | -0.053 | 0.047 | 9.693 | 12.554 | 0.318 | 0.486 | 0.026 | buffer_atr=0.05, sl=atr_1.00, tp=r_3.0, rf=gt_0.25 | buffer_atr=0.1, sl=range_0.50, tp=r_0.5, rf=none | SIN VENTAJA: se degrada fuera de muestra | FRÁGIL: sólo 50% de ventanas WF positivas |
| D_tokyo_or_failed_breakout | USDJPY | M1 ejecución / M5 señal | 69 | 0.652 | 0.549 | -0.130 | 0.008 | -3.287 | 6.030 | -0.323 | -0.378 | -0.021 | exit=tp2_opposite, min_sweep_atr=0.2, or_minutes=15, stop_buffer_atr=0.1 | exit=split_mid_opposite, min_sweep_atr=0.0, or_minutes=60, stop_buffer_atr=0.0 | SIN VENTAJA: se degrada fuera de muestra | FRÁGIL: 58% del beneficio pre-OOS en un solo año; sólo 50% de ventanas WF positivas; menos de la mitad de los vecinos de parámetros son positivos NO ROBUSTA: expectancy <= 0 con spread x1.5/slip x1, spread x1/slip x2 |
| E_tokyo_breakout_vwap | AUDJPY | M1 ejecución / M5 señal | 40 | 0.300 | 0.539 | -0.084 | 0.039 | 1.251 | 3.774 | 0.214 | 0.330 | 0.014 | buffer_atr=0.0, sl=atr_0.75, tp=r_2.0, vwap_filter=False, rf=gt_0.50 | buffer_atr=0.05, sl=atr_1.00, tp=r_1.0, vwap_filter=True, rf=none | SIN VENTAJA: se degrada fuera de muestra | FRÁGIL: 53% del beneficio pre-OOS en un solo año; sólo 50% de ventanas WF positivas |
| A_asian_range_breakout | AUDJPY | M1 ejecución / M5 señal | 41 | 0.293 | 0.693 | -0.085 | 0.054 | 2.428 | 7.640 | 0.217 | 0.350 | 0.026 | buffer_atr=0.0, sl=atr_0.75, tp=r_3.0, rf=gt_0.50 | buffer_atr=0.1, sl=range_0.50, tp=r_0.5, rf=none | SIN VENTAJA: se degrada fuera de muestra | FRÁGIL: 65% del beneficio pre-OOS en un solo año; sólo 50% de ventanas WF positivas |
| A_asian_range_breakout | NZDUSD | M1 ejecución / M5 señal | 170 | 0.406 | 0.618 | -0.038 | -0.011 | -6.456 | 7.734 | -1.012 | -1.344 | -0.017 | buffer_atr=0.0, sl=atr_1.25, tp=trail_atr_1.0, rf=gt_0.25 | buffer_atr=0.1, sl=range_0.50, tp=r_1.5, rf=none | FRÁGIL | FRÁGIL: 95% del beneficio pre-OOS en un solo año; sólo 0% de ventanas WF positivas; menos de la mitad de los vecinos de parámetros son positivos NO ROBUSTA: expectancy <= 0 con spread x1.5/slip x1, spread x1/slip x2 |
| A_asian_range_breakout | XAUUSD | M1 ejecución / M5 señal | 386 | 0.508 | 1.183 | 0.012 | -0.015 | -8.877 | 9.445 | -1.065 | -1.423 | -0.014 | buffer_atr=0.0, sl=atr_1.25, tp=r_0.5, rf=none | buffer_atr=0.025, sl=range_0.50, tp=r_3.0, rf=gt_0.25 | FRÁGIL | FRÁGIL: sólo 27% de ventanas WF positivas; menos de la mitad de los vecinos de parámetros son positivos NO ROBUSTA: expectancy <= 0 con spread x1.5/slip x1, spread x1/slip x2 |
| C_tokyo_or_breakout | XAUUSD | M1 ejecución / M5 señal | 485 | 0.532 | 1.015 | 0.002 | -0.016 | -9.771 | 11.323 | -0.567 | -0.789 | -0.014 | buffer_atr=0.0, or_minutes=5, sl=atr_1.00, tp=r_1.0 | buffer_atr=0.1, or_minutes=30, sl=or_opposite, tp=r_3.0 | FRÁGIL | FRÁGIL: 100% del beneficio pre-OOS en un solo año; sólo 9% de ventanas WF positivas; menos de la mitad de los vecinos de parámetros son positivos NO ROBUSTA: expectancy <= 0 con spread x1.5/slip x1, spread x1/slip x2 |
| A_asian_range_breakout | AUDUSD | M1 ejecución / M5 señal | 177 | 0.407 | 0.606 | -0.041 | -0.013 | -7.336 | 8.230 | -1.060 | -1.436 | -0.018 | buffer_atr=0.0, sl=atr_1.25, tp=r_3.0, rf=gt_0.25 | buffer_atr=0.1, sl=range_0.50, tp=r_0.5, rf=none | FRÁGIL | FRÁGIL: 100% del beneficio pre-OOS en un solo año; sólo 0% de ventanas WF positivas; menos de la mitad de los vecinos de parámetros son positivos NO ROBUSTA: expectancy <= 0 con spread x1.5/slip x1, spread x1/slip x2 |
| D_tokyo_or_failed_breakout | AUDJPY | M1 ejecución / M5 señal | 59 | 0.695 | 0.820 | -0.045 | -0.024 | -4.689 | 7.857 | -0.420 | -0.498 | -0.028 | exit=tp2_opposite, min_sweep_atr=0.2, or_minutes=5, stop_buffer_atr=0.1 | exit=split_mid_opposite, min_sweep_atr=0.0, or_minutes=15, stop_buffer_atr=0.0 | FRÁGIL | FRÁGIL: 51% del beneficio pre-OOS en un solo año; sólo 0% de ventanas WF positivas; menos de la mitad de los vecinos de parámetros son positivos NO ROBUSTA: expectancy <= 0 con spread x1.5/slip x1, spread x1/slip x2 |
| D_tokyo_or_failed_breakout | JP225 | M1 ejecución / M5 señal | 43 | 0.512 | 0.737 | -0.072 | -0.026 | -4.149 | 6.397 | -0.482 | -0.581 | -0.034 | exit=tp1_mid, min_sweep_atr=0.2, or_minutes=15, stop_buffer_atr=0.1 | exit=tp2_opposite, min_sweep_atr=0.0, or_minutes=30, stop_buffer_atr=0.0 | FRÁGIL | FRÁGIL: 100% del beneficio pre-OOS en un solo año; sólo 0% de ventanas WF positivas; menos de la mitad de los vecinos de parámetros son positivos NO ROBUSTA: expectancy <= 0 con spread x1.5/slip x1, spread x1/slip x2 |
| C_tokyo_or_breakout | JP225 | M1 ejecución / M5 señal | 236 | 0.462 | 0.726 | -0.061 | -0.003 | -8.512 | 14.194 | -0.404 | -0.585 | -0.014 | buffer_atr=0.1, or_minutes=30, sl=atr_1.00, tp=r_2.0 | buffer_atr=0.0, or_minutes=5, sl=or_opposite, tp=r_1.0 | SIN VENTAJA: se degrada fuera de muestra | FRÁGIL: sólo 50% de ventanas WF positivas NO ROBUSTA: expectancy <= 0 con spread x1.5/slip x1, spread x1/slip x2 |
| D_tokyo_or_failed_breakout | XAUUSD | M1 ejecución / M5 señal | 85 | 0.459 | 0.577 | -0.120 | -0.022 | -5.797 | 7.280 | -0.491 | -0.587 | -0.035 | exit=tp2_opposite, min_sweep_atr=0.2, or_minutes=60, stop_buffer_atr=0.1 | exit=split_mid_opposite, min_sweep_atr=0.0, or_minutes=5, stop_buffer_atr=0.0 | FRÁGIL | FRÁGIL: sólo 27% de ventanas WF positivas; menos de la mitad de los vecinos de parámetros son positivos NO ROBUSTA: expectancy <= 0 con spread x1.5/slip x1, spread x1/slip x2 |
| C_tokyo_or_breakout | AUDJPY | M1 ejecución / M5 señal | 228 | 0.469 | 0.718 | -0.044 | -0.013 | -10.075 | 10.957 | -0.758 | -1.070 | -0.019 | buffer_atr=0.1, or_minutes=60, sl=atr_1.00, tp=r_2.0 | buffer_atr=0.025, or_minutes=5, sl=or_opposite, tp=r_1.0 | SIN VENTAJA: se degrada fuera de muestra | FRÁGIL: 100% del beneficio pre-OOS en un solo año; sólo 25% de ventanas WF positivas NO ROBUSTA: expectancy <= 0 con spread x1.5/slip x1, spread x1/slip x2 |
| B_asian_failed_breakout | AUDUSD | M1 ejecución / M5 señal | 76 | 0.421 | 0.921 | -0.025 | -0.059 | -10.549 | 14.584 | -0.664 | -0.935 | -0.053 | exit=tp2_opposite, min_sweep_atr=0.1, stop_buffer_atr=0.1, rf=none | exit=split_mid_opposite, min_sweep_atr=0.0, stop_buffer_atr=0.0, rf=gt_0.25 | FRÁGIL | FRÁGIL: 60% del beneficio pre-OOS en un solo año; sólo 0% de ventanas WF positivas; menos de la mitad de los vecinos de parámetros son positivos NO ROBUSTA: expectancy <= 0 con spread x1.5/slip x1, spread x1/slip x2 |
| B_asian_failed_breakout | EURJPY | M1 ejecución / M5 señal | 71 | 0.380 | 0.586 | -0.235 | -0.049 | -12.760 | 15.407 | -0.746 | -1.059 | -0.097 | exit=tp1_mid, min_sweep_atr=0.1, stop_buffer_atr=0.1, rf=none | exit=split_mid_opposite, min_sweep_atr=0.0, stop_buffer_atr=0.0, rf=gt_0.25 | FRÁGIL | FRÁGIL: 57% del beneficio pre-OOS en un solo año; sólo 25% de ventanas WF positivas; menos de la mitad de los vecinos de parámetros son positivos NO ROBUSTA: expectancy <= 0 con spread x1.5/slip x1, spread x1/slip x2 |
| B_asian_failed_breakout | XAUUSD | M1 ejecución / M5 señal | 97 | 0.402 | 0.555 | -0.138 | -0.085 | -14.132 | 15.058 | -0.828 | -1.108 | -0.096 | exit=tp2_opposite, min_sweep_atr=0.1, stop_buffer_atr=0.1, rf=gt_0.25 | exit=tp1_mid, min_sweep_atr=0.0, stop_buffer_atr=0.0, rf=none | FRÁGIL | FRÁGIL: 100% del beneficio pre-OOS en un solo año; sólo 18% de ventanas WF positivas; menos de la mitad de los vecinos de parámetros son positivos NO ROBUSTA: expectancy <= 0 con spread x1.5/slip x1, spread x1/slip x2 |
| B_asian_failed_breakout | JP225 | M1 ejecución / M5 señal | 92 | 0.489 | 0.877 | -0.049 | -0.121 | -23.861 | 24.246 | -1.283 | -1.678 | -0.108 | exit=tp1_mid, min_sweep_atr=0.1, stop_buffer_atr=0.1, rf=none | exit=tp2_opposite, min_sweep_atr=0.0, stop_buffer_atr=0.0, rf=gt_0.50 | FRÁGIL | FRÁGIL: sólo 50% de ventanas WF positivas; menos de la mitad de los vecinos de parámetros son positivos NO ROBUSTA: expectancy <= 0 con spread x1.5/slip x1, spread x1/slip x2 |
| B_asian_failed_breakout | AUDJPY | M1 ejecución / M5 señal | 77 | 0.494 | 0.659 | -0.116 | -0.127 | -22.784 | 23.382 | -1.735 | -2.063 | -0.125 | exit=tp1_mid, min_sweep_atr=0.1, stop_buffer_atr=0.1, rf=none | exit=tp2_opposite, min_sweep_atr=0.0, stop_buffer_atr=0.0, rf=gt_0.50 | FRÁGIL | FRÁGIL: sólo 25% de ventanas WF positivas; menos de la mitad de los vecinos de parámetros son positivos NO ROBUSTA: expectancy <= 0 con spread x1.5/slip x1, spread x1/slip x2 |
| B_asian_failed_breakout | USDJPY | M1 ejecución / M5 señal | 144 | 0.458 | 0.593 | -0.200 | -0.107 | -35.205 | 36.408 | -1.532 | -2.083 | -0.127 | exit=tp1_mid, min_sweep_atr=0.1, stop_buffer_atr=0.05, rf=none | exit=split_mid_opposite, min_sweep_atr=0.0, stop_buffer_atr=0.0, rf=gt_0.25 | FRÁGIL | FRÁGIL: sólo 0% de ventanas WF positivas; menos de la mitad de los vecinos de parámetros son positivos NO ROBUSTA: expectancy <= 0 con spread x1.5/slip x1, spread x1/slip x2 |
| B_asian_failed_breakout | NZDUSD | M1 ejecución / M5 señal | 65 | 0.354 | 0.502 | -0.208 | -0.172 | -24.883 | 25.113 | -1.986 | -2.424 | -0.180 | exit=tp2_opposite, min_sweep_atr=0.1, stop_buffer_atr=0.1, rf=none | exit=tp1_mid, min_sweep_atr=0.0, stop_buffer_atr=0.0, rf=gt_0.25 | FRÁGIL | FRÁGIL: sólo 0% de ventanas WF positivas; menos de la mitad de los vecinos de parámetros son positivos NO ROBUSTA: expectancy <= 0 con spread x1.5/slip x1, spread x1/slip x2 |

## 2. Ranking por estrategia
| strategy | pairs | oos_exp_mean | oos_positive | val_exp_mean | robust |
|---|---|---|---|---|---|
| C_tokyo_or_breakout | 4 | -0.030 | 1 | -0.029 | 0 |
| A_asian_range_breakout | 7 | -0.036 | 1 | -0.027 | 0 |
| E_tokyo_breakout_vwap | 3 | -0.039 | 0 | -0.040 | 0 |
| D_tokyo_or_failed_breakout | 4 | -0.092 | 0 | -0.000 | 0 |
| B_asian_failed_breakout | 7 | -0.139 | 0 | -0.074 | 0 |

## 3. Ranking por activo
| symbol | strategies | oos_exp_mean | oos_positive | val_exp_mean |
|---|---|---|---|---|
| AUDUSD | 2 | -0.033 | 0 | -0.051 |
| JP225 | 5 | -0.039 | 0 | -0.044 |
| XAUUSD | 4 | -0.061 | 2 | -0.004 |
| AUDJPY | 5 | -0.075 | 0 | -0.095 |
| USDJPY | 5 | -0.087 | 0 | 0.008 |
| NZDUSD | 2 | -0.123 | 0 | -0.097 |
| EURJPY | 2 | -0.134 | 0 | 0.014 |

## 4. Ranking estrategia + activo
| strategy | symbol | composite_rank | pre_oos_expectancy_R | VAL_profit_factor | ALL_max_dd_pct | robust_expectancy_R | OOS_expectancy_R | verdict |
|---|---|---|---|---|---|---|---|---|
| A_asian_range_breakout | JP225 | 3.400 | 0.035 | 1.183 | 3.869 | 0.033 | -0.012 | SIN VENTAJA: se degrada fuera de muestra |
| A_asian_range_breakout | EURJPY | 6 | 0.038 | 0.991 | 6.854 | 0.057 | -0.033 | SIN VENTAJA: se degrada fuera de muestra |
| C_tokyo_or_breakout | USDJPY | 6.400 | 0.007 | 1.053 | 4.591 | 0.007 | -0.016 | SIN VENTAJA: se degrada fuera de muestra |
| E_tokyo_breakout_vwap | USDJPY | 7.400 | 0.033 | 1.085 | 8.375 | 0.029 | -0.033 | SIN VENTAJA: se degrada fuera de muestra |
| E_tokyo_breakout_vwap | JP225 | 7.800 | 0.003 | 0.777 | 2.258 | 0.012 | -0.001 | SIN VENTAJA: se degrada fuera de muestra |
| A_asian_range_breakout | USDJPY | 8 | 0.047 | 1.161 | 12.554 | 0.032 | -0.053 | SIN VENTAJA: se degrada fuera de muestra |
| D_tokyo_or_failed_breakout | USDJPY | 9.400 | 0.008 | 1.150 | 6.030 | -0.001 | -0.130 | SIN VENTAJA: se degrada fuera de muestra |
| E_tokyo_breakout_vwap | AUDJPY | 9.600 | 0.039 | 0.411 | 3.774 | 0.080 | -0.084 | SIN VENTAJA: se degrada fuera de muestra |
| A_asian_range_breakout | AUDJPY | 10.800 | 0.054 | 0.385 | 7.640 | 0.129 | -0.085 | SIN VENTAJA: se degrada fuera de muestra |
| A_asian_range_breakout | NZDUSD | 11.200 | -0.011 | 0.886 | 7.734 | -0.013 | -0.038 | FRÁGIL |
| A_asian_range_breakout | XAUUSD | 11.800 | -0.015 | 0.792 | 9.445 | -0.016 | 0.012 | FRÁGIL |
| C_tokyo_or_breakout | XAUUSD | 12 | -0.016 | 0.896 | 11.323 | -0.018 | 0.002 | FRÁGIL |
| A_asian_range_breakout | AUDUSD | 12.800 | -0.013 | 0.778 | 8.230 | -0.011 | -0.041 | FRÁGIL |
| D_tokyo_or_failed_breakout | AUDJPY | 13.400 | -0.024 | 0.918 | 7.857 | -0.022 | -0.045 | FRÁGIL |
| D_tokyo_or_failed_breakout | JP225 | 13.600 | -0.026 | 0.951 | 6.397 | -0.040 | -0.072 | FRÁGIL |
| C_tokyo_or_breakout | JP225 | 13.800 | -0.003 | 0.753 | 14.194 | 0.014 | -0.061 | SIN VENTAJA: se degrada fuera de muestra |
| D_tokyo_or_failed_breakout | XAUUSD | 13.800 | -0.022 | 1.000 | 7.280 | -0.029 | -0.120 | FRÁGIL |
| C_tokyo_or_breakout | AUDJPY | 14 | -0.013 | 0.597 | 10.957 | 0.002 | -0.044 | SIN VENTAJA: se degrada fuera de muestra |
| B_asian_failed_breakout | AUDUSD | 16.800 | -0.059 | 0.732 | 14.584 | -0.076 | -0.025 | FRÁGIL |
| B_asian_failed_breakout | EURJPY | 18 | -0.049 | 1.078 | 15.407 | -0.081 | -0.235 | FRÁGIL |
| B_asian_failed_breakout | XAUUSD | 18.600 | -0.085 | 1.050 | 15.058 | -0.129 | -0.138 | FRÁGIL |
| B_asian_failed_breakout | JP225 | 20.200 | -0.121 | 0.639 | 24.246 | -0.111 | -0.049 | FRÁGIL |
| B_asian_failed_breakout | AUDJPY | 20.800 | -0.127 | 0.817 | 23.382 | -0.148 | -0.116 | FRÁGIL |
| B_asian_failed_breakout | USDJPY | 21.200 | -0.107 | 0.830 | 36.408 | -0.125 | -0.200 | FRÁGIL |
| B_asian_failed_breakout | NZDUSD | 24.200 | -0.172 | 0.473 | 25.113 | -0.175 | -0.208 | FRÁGIL |

## 5. Parámetros robustos y TOP 10 por categoría

| strategy | symbol | cid | robust_expectancy_R | neighbor_positive_share | n_configs_tested | bh_significant_is | dsr_is |
|---|---|---|---|---|---|---|---|
| A_asian_range_breakout | JP225 | buffer_atr=0.1/sl=atr_0.50/tp=trail_atr_1.0/rf=btw_0.50_1.50 | 0.033 | 1 | 1536 | 0 | 0.016 |
| A_asian_range_breakout | EURJPY | buffer_atr=0.05/sl=range_1.00/tp=r_2.0/rf=gt_0.25 | 0.057 | 1 | 1536 | 0 | 0.000 |
| C_tokyo_or_breakout | USDJPY | buffer_atr=0.0/or_minutes=15/sl=atr_1.00/tp=r_2.0/rf=none | 0.007 | 1 | 320 | 0 | 0.114 |
| E_tokyo_breakout_vwap | USDJPY | buffer_atr=0.05/sl=range_opposite/tp=r_2.0/vwap_filter=True/rf=none | 0.029 | 0.667 | 48 | 0 | 0.472 |
| E_tokyo_breakout_vwap | JP225 | buffer_atr=0.05/sl=atr_1.00/tp=trail_atr_1.0/vwap_filter=True/rf=gt_0.50 | 0.012 | 0.667 | 48 | 0 | 0.182 |
| A_asian_range_breakout | USDJPY | buffer_atr=0.0/sl=range_0.50/tp=trail_swing/rf=gt_0.25 | 0.032 | 0.750 | 1536 | 0 | 0.000 |
| D_tokyo_or_failed_breakout | USDJPY | exit=tp2_opposite/min_sweep_atr=0.2/or_minutes=5/stop_buffer_atr=0.0/rf=none | -0.001 | 0.333 | 192 | 0 | 0.000 |
| E_tokyo_breakout_vwap | AUDJPY | buffer_atr=0.0/sl=atr_1.00/tp=r_1.0/vwap_filter=True/rf=gt_0.50 | 0.080 | 1 | 48 | 0 | 0.582 |
| A_asian_range_breakout | AUDJPY | buffer_atr=0.0/sl=atr_0.50/tp=r_2.0/rf=btw_0.50_1.50 | 0.129 | 1 | 1536 | 0 | 0.122 |
| A_asian_range_breakout | NZDUSD | buffer_atr=0.025/sl=atr_1.25/tp=trail_atr_0.5/rf=gt_0.25 | -0.013 | 0.000 | 1536 | 0 | 0.000 |
| A_asian_range_breakout | XAUUSD | buffer_atr=0.0/sl=atr_1.25/tp=r_0.5/rf=none | -0.016 | 0.000 | 1536 | 0 | 0.000 |
| C_tokyo_or_breakout | XAUUSD | buffer_atr=0.0/or_minutes=15/sl=atr_1.00/tp=r_1.5/rf=none | -0.018 | 0.000 | 320 | 0 | 0.000 |
| A_asian_range_breakout | AUDUSD | buffer_atr=0.0/sl=atr_1.25/tp=r_1.5/rf=gt_0.25 | -0.011 | 0.167 | 1536 | 0 | 0.000 |
| D_tokyo_or_failed_breakout | AUDJPY | exit=tp2_opposite/min_sweep_atr=0.2/or_minutes=15/stop_buffer_atr=0.0/rf=none | -0.022 | 0.250 | 192 | 0 | 0.000 |
| D_tokyo_or_failed_breakout | JP225 | exit=tp1_mid/min_sweep_atr=0.2/or_minutes=60/stop_buffer_atr=0.1/rf=none | -0.040 | 0.000 | 192 | 0 | 0.000 |
| C_tokyo_or_breakout | JP225 | buffer_atr=0.0/or_minutes=30/sl=atr_0.75/tp=r_2.0/rf=none | 0.014 | 0.714 | 320 | 0 | 0.042 |
| D_tokyo_or_failed_breakout | XAUUSD | exit=tp2_opposite/min_sweep_atr=0.2/or_minutes=60/stop_buffer_atr=0.1/rf=none | -0.029 | 0.000 | 192 | 0 | 0.000 |
| C_tokyo_or_breakout | AUDJPY | buffer_atr=0.1/or_minutes=60/sl=atr_1.00/tp=r_1.5/rf=none | 0.002 | 0.600 | 320 | 0 | 0.002 |
| B_asian_failed_breakout | AUDUSD | exit=tp2_opposite/min_sweep_atr=0.1/stop_buffer_atr=0.1/rf=none | -0.076 | 0.250 | 288 | 0 | 0.000 |
| B_asian_failed_breakout | EURJPY | exit=tp2_opposite/min_sweep_atr=0.1/stop_buffer_atr=0.025/rf=gt_0.25 | -0.081 | 0.167 | 288 | 0 | 0.000 |
| B_asian_failed_breakout | XAUUSD | exit=tp2_opposite/min_sweep_atr=0.1/stop_buffer_atr=0.1/rf=gt_0.25 | -0.129 | 0.000 | 288 | 0 | 0.000 |
| B_asian_failed_breakout | JP225 | exit=tp1_mid/min_sweep_atr=0.05/stop_buffer_atr=0.1/rf=gt_0.25 | -0.111 | 0.000 | 264 | 0 | 0.000 |
| B_asian_failed_breakout | AUDJPY | exit=tp1_mid/min_sweep_atr=0.1/stop_buffer_atr=0.1/rf=none | -0.148 | 0.000 | 264 | 0 | 0.000 |
| B_asian_failed_breakout | USDJPY | exit=tp1_mid/min_sweep_atr=0.05/stop_buffer_atr=0.025/rf=none | -0.125 | 0.000 | 288 | 0 | 0.000 |
| B_asian_failed_breakout | NZDUSD | exit=tp2_opposite/min_sweep_atr=0.1/stop_buffer_atr=0.1/rf=gt_0.25 | -0.175 | 0.000 | 288 | 0 | 0.000 |

`bh_significant_is` = configuraciones de la grilla con expectancy > 0 significativa tras Benjamini-Hochberg (q=0.05). `dsr_is` = Deflated Sharpe Ratio de la elegida (prob. de Sharpe real > 0 corrigiendo por la cantidad de pruebas).

### A_best_IS
| strategy | symbol | cid | is_trades | is_expectancy_R | is_robust_expectancy_R | is_profit_factor | val_expectancy_R | oos_expectancy_R |
|---|---|---|---|---|---|---|---|---|
| A_asian_range_breakout | AUDJPY | buffer_atr=0.0/sl=range_0.50/tp=r_2.0/rf=gt_0.50 | 126 | 0.222 | 0.155 | 1.698 | -0.405 | -0.135 |
| A_asian_range_breakout | AUDJPY | buffer_atr=0.0/sl=range_0.50/tp=r_2.0/rf=btw_0.50_1.50 | 124 | 0.214 | 0.144 | 1.669 | -0.405 | -0.135 |
| A_asian_range_breakout | AUDJPY | buffer_atr=0.0/sl=range_0.50/tp=r_3.0/rf=gt_0.50 | 126 | 0.188 | 0.137 | 1.592 | -0.378 | -0.188 |
| A_asian_range_breakout | AUDJPY | buffer_atr=0.0/sl=range_0.50/tp=r_3.0/rf=btw_0.50_1.50 | 124 | 0.186 | 0.141 | 1.583 | -0.378 | -0.188 |
| A_asian_range_breakout | AUDJPY | buffer_atr=0.0/sl=range_0.50/tp=trail_atr_1.0/rf=gt_0.50 | 126 | 0.161 | 0.124 | 1.549 | -0.401 | -0.170 |
| A_asian_range_breakout | AUDJPY | buffer_atr=0.0/sl=range_0.50/tp=trail_atr_1.0/rf=btw_0.50_1.50 | 124 | 0.161 | 0.124 | 1.547 | -0.401 | -0.170 |
| A_asian_range_breakout | AUDJPY | buffer_atr=0.0/sl=range_0.50/tp=r_1.5/rf=gt_0.50 | 126 | 0.155 | 0.121 | 1.486 | -0.415 | -0.161 |
| A_asian_range_breakout | AUDJPY | buffer_atr=0.0/sl=range_0.50/tp=trail_swing/rf=btw_0.50_1.50 | 124 | 0.151 | 0.116 | 1.511 | -0.393 | -0.183 |
| A_asian_range_breakout | AUDJPY | buffer_atr=0.0/sl=range_0.50/tp=trail_swing/rf=gt_0.50 | 126 | 0.150 | 0.111 | 1.510 | -0.393 | -0.183 |
| A_asian_range_breakout | AUDJPY | buffer_atr=0.0/sl=range_0.50/tp=r_1.5/rf=btw_0.50_1.50 | 124 | 0.149 | 0.130 | 1.467 | -0.415 | -0.161 |

### B_best_VALIDATION
| strategy | symbol | cid | is_trades | is_expectancy_R | is_robust_expectancy_R | is_profit_factor | val_expectancy_R | oos_expectancy_R |
|---|---|---|---|---|---|---|---|---|
| A_asian_range_breakout | USDJPY | buffer_atr=0.1/sl=range_0.50/tp=r_3.0/rf=gt_0.25 | 282 | -0.010 | -0.022 | 0.980 | 0.169 | -0.226 |
| A_asian_range_breakout | USDJPY | buffer_atr=0.1/sl=range_0.75/tp=r_0.5/rf=gt_0.25 | 282 | -0.013 | -0.013 | 0.953 | 0.141 | -0.062 |
| A_asian_range_breakout | USDJPY | buffer_atr=0.1/sl=range_0.50/tp=r_2.0/rf=gt_0.25 | 282 | -0.039 | -0.039 | 0.919 | 0.141 | -0.142 |
| A_asian_range_breakout | USDJPY | buffer_atr=0.1/sl=range_0.50/tp=trail_swing/rf=gt_0.25 | 282 | -0.001 | -0.019 | 0.998 | 0.132 | -0.202 |
| A_asian_range_breakout | USDJPY | buffer_atr=0.1/sl=range_0.50/tp=r_1.0/rf=gt_0.25 | 282 | -0.054 | -0.048 | 0.876 | 0.131 | -0.192 |
| A_asian_range_breakout | USDJPY | buffer_atr=0.1/sl=range_0.50/tp=r_3.0/rf=none | 400 | -0.034 | -0.020 | 0.937 | 0.129 | -0.240 |
| A_asian_range_breakout | USDJPY | buffer_atr=0.1/sl=range_0.50/tp=r_0.5/rf=gt_0.25 | 282 | -0.001 | -0.009 | 0.996 | 0.125 | -0.091 |
| A_asian_range_breakout | USDJPY | buffer_atr=0.05/sl=range_0.50/tp=r_1.0/rf=gt_0.25 | 356 | 0.010 | -0.016 | 1.024 | 0.125 | -0.074 |
| A_asian_range_breakout | USDJPY | buffer_atr=0.1/sl=range_0.50/tp=trail_atr_1.0/rf=gt_0.25 | 282 | -0.037 | -0.040 | 0.914 | 0.122 | -0.178 |
| A_asian_range_breakout | USDJPY | buffer_atr=0.1/sl=range_0.50/tp=trail_atr_0.5/rf=gt_0.25 | 282 | -0.054 | -0.043 | 0.877 | 0.119 | -0.188 |

### C_best_OOS_solo_informativo
| strategy | symbol | cid | is_trades | is_expectancy_R | is_robust_expectancy_R | is_profit_factor | val_expectancy_R | oos_expectancy_R |
|---|---|---|---|---|---|---|---|---|
| B_asian_failed_breakout | JP225 | exit=tp2_opposite/min_sweep_atr=0.05/stop_buffer_atr=0.0/rf=gt_0.25 | 305 | -0.326 | -0.326 | 0.506 | -0.341 | 0.194 |
| B_asian_failed_breakout | JP225 | exit=split_mid_opposite/min_sweep_atr=0.05/stop_buffer_atr=0.0/rf=gt_0.25 | 305 | -0.275 | -0.276 | 0.553 | -0.351 | 0.190 |
| B_asian_failed_breakout | JP225 | exit=split_mid_opposite/min_sweep_atr=0.05/stop_buffer_atr=0.0/rf=none | 315 | -0.276 | -0.275 | 0.553 | -0.358 | 0.172 |
| B_asian_failed_breakout | JP225 | exit=tp2_opposite/min_sweep_atr=0.05/stop_buffer_atr=0.0/rf=none | 315 | -0.326 | -0.326 | 0.509 | -0.348 | 0.171 |
| B_asian_failed_breakout | JP225 | exit=tp1_mid/min_sweep_atr=0.05/stop_buffer_atr=0.0/rf=gt_0.25 | 305 | -0.250 | -0.252 | 0.593 | -0.316 | 0.160 |
| C_tokyo_or_breakout | XAUUSD | buffer_atr=0.0/or_minutes=30/sl=or_opposite/tp=r_3.0/rf=none | 2283 | -0.185 | -0.169 | 0.744 | -0.121 | 0.153 |
| A_asian_range_breakout | JP225 | buffer_atr=0.05/sl=range_0.50/tp=r_1.0/rf=gt_0.25 | 405 | -0.100 | -0.099 | 0.762 | -0.115 | 0.153 |
| A_asian_range_breakout | JP225 | buffer_atr=0.05/sl=range_0.50/tp=r_1.0/rf=none | 422 | -0.095 | -0.100 | 0.773 | -0.094 | 0.150 |
| A_asian_range_breakout | JP225 | buffer_atr=0.05/sl=range_0.50/tp=r_3.0/rf=gt_0.25 | 405 | -0.111 | -0.109 | 0.755 | -0.139 | 0.150 |
| C_tokyo_or_breakout | XAUUSD | buffer_atr=0.025/or_minutes=15/sl=or_opposite/tp=r_3.0/rf=none | 2157 | -0.172 | -0.166 | 0.760 | -0.117 | 0.148 |

### D_best_ROBUSTA
| strategy | symbol | cid | is_trades | is_expectancy_R | is_robust_expectancy_R | is_profit_factor | val_expectancy_R | oos_expectancy_R |
|---|---|---|---|---|---|---|---|---|
| A_asian_range_breakout | EURJPY | buffer_atr=0.025/sl=range_0.75/tp=r_3.0/rf=gt_0.25 | 417 | 0.068 | 0.053 | 1.170 | 0.018 | 0.012 |
| A_asian_range_breakout | EURJPY | buffer_atr=0.025/sl=range_1.00/tp=r_3.0/rf=gt_0.25 | 417 | 0.051 | 0.051 | 1.162 | 0.004 | -0.017 |
| A_asian_range_breakout | EURJPY | buffer_atr=0.025/sl=range_1.00/tp=r_2.0/rf=gt_0.25 | 417 | 0.043 | 0.047 | 1.137 | 0.005 | -0.032 |
| A_asian_range_breakout | EURJPY | buffer_atr=0.025/sl=range_0.75/tp=r_2.0/rf=gt_0.25 | 417 | 0.056 | 0.043 | 1.140 | 0.009 | 0.015 |
| A_asian_range_breakout | JP225 | buffer_atr=0.1/sl=atr_0.50/tp=trail_atr_1.0/rf=btw_0.50_1.50 | 164 | 0.034 | 0.033 | 1.156 | 0.037 | -0.012 |
| A_asian_range_breakout | USDJPY | buffer_atr=0.0/sl=range_0.50/tp=trail_swing/rf=gt_0.25 | 438 | 0.039 | 0.032 | 1.092 | 0.064 | -0.053 |
| A_asian_range_breakout | USDJPY | buffer_atr=0.05/sl=range_1.00/tp=r_3.0/rf=gt_0.25 | 356 | 0.042 | 0.031 | 1.163 | 0.028 | -0.094 |
| A_asian_range_breakout | USDJPY | buffer_atr=0.0/sl=range_1.00/tp=r_3.0/rf=gt_0.25 | 438 | 0.039 | 0.030 | 1.151 | 0.045 | -0.023 |
| A_asian_range_breakout | USDJPY | buffer_atr=0.025/sl=range_1.00/tp=r_3.0/rf=gt_0.25 | 401 | 0.030 | 0.030 | 1.114 | 0.039 | -0.063 |
| A_asian_range_breakout | JP225 | buffer_atr=0.1/sl=atr_0.50/tp=trail_swing/rf=btw_0.50_1.50 | 164 | 0.031 | 0.030 | 1.141 | 0.040 | -0.004 |

### E_best_riesgo_retorno
| strategy | symbol | cid | is_trades | is_expectancy_R | is_robust_expectancy_R | is_profit_factor | val_expectancy_R | oos_expectancy_R |
|---|---|---|---|---|---|---|---|---|
| A_asian_range_breakout | USDJPY | buffer_atr=0.05/sl=atr_0.50/tp=r_1.5/rf=none | 522 | 0.022 | 0.017 | 1.121 | 0.029 | -0.038 |
| A_asian_range_breakout | USDJPY | buffer_atr=0.025/sl=atr_1.00/tp=r_3.0/rf=none | 595 | 0.013 | 0.014 | 1.140 | 0.007 | -0.031 |
| A_asian_range_breakout | USDJPY | buffer_atr=0.025/sl=atr_1.25/tp=r_2.0/rf=none | 594 | 0.013 | 0.012 | 1.173 | 0.002 | -0.026 |
| A_asian_range_breakout | USDJPY | buffer_atr=0.05/sl=atr_0.50/tp=r_2.0/rf=none | 522 | 0.027 | 0.022 | 1.146 | 0.017 | -0.030 |
| A_asian_range_breakout | USDJPY | buffer_atr=0.025/sl=atr_1.25/tp=r_3.0/rf=none | 594 | 0.012 | 0.013 | 1.165 | 0.002 | -0.026 |
| A_asian_range_breakout | USDJPY | buffer_atr=0.025/sl=atr_1.25/tp=r_1.5/rf=none | 594 | 0.012 | 0.012 | 1.164 | 0.002 | -0.029 |
| A_asian_range_breakout | USDJPY | buffer_atr=0.025/sl=atr_0.50/tp=r_2.0/rf=none | 597 | 0.017 | 0.017 | 1.093 | 0.029 | -0.042 |
| A_asian_range_breakout | USDJPY | buffer_atr=0.025/sl=atr_0.50/tp=r_1.5/rf=none | 597 | 0.014 | 0.015 | 1.077 | 0.039 | -0.049 |
| A_asian_range_breakout | USDJPY | buffer_atr=0.025/sl=atr_0.50/tp=r_3.0/rf=none | 597 | 0.017 | 0.018 | 1.088 | 0.029 | -0.027 |
| A_asian_range_breakout | USDJPY | buffer_atr=0.025/sl=atr_1.00/tp=r_2.0/rf=none | 595 | 0.012 | 0.013 | 1.126 | 0.007 | -0.033 |

### F_best_ejecucion_automatica
| strategy | symbol | cid | is_trades | is_expectancy_R | is_robust_expectancy_R | is_profit_factor | val_expectancy_R | oos_expectancy_R |
|---|---|---|---|---|---|---|---|---|
| A_asian_range_breakout | EURJPY | buffer_atr=0.025/sl=range_0.75/tp=r_3.0/rf=gt_0.25 | 417 | 0.068 | 0.053 | 1.170 | 0.018 | 0.012 |
| A_asian_range_breakout | EURJPY | buffer_atr=0.025/sl=range_1.00/tp=r_3.0/rf=gt_0.25 | 417 | 0.051 | 0.051 | 1.162 | 0.004 | -0.017 |
| A_asian_range_breakout | EURJPY | buffer_atr=0.025/sl=range_1.00/tp=r_2.0/rf=gt_0.25 | 417 | 0.043 | 0.047 | 1.137 | 0.005 | -0.032 |
| A_asian_range_breakout | EURJPY | buffer_atr=0.025/sl=range_0.75/tp=r_2.0/rf=gt_0.25 | 417 | 0.056 | 0.043 | 1.140 | 0.009 | 0.015 |
| E_tokyo_breakout_vwap | USDJPY | buffer_atr=0.05/sl=range_opposite/tp=r_2.0/vwap_filter=True/rf=none | 530 | 0.037 | 0.029 | 1.172 | 0.019 | -0.033 |
| E_tokyo_breakout_vwap | USDJPY | buffer_atr=0.05/sl=range_opposite/tp=r_2.0/vwap_filter=False/rf=none | 530 | 0.037 | 0.029 | 1.171 | 0.019 | -0.033 |
| A_asian_range_breakout | USDJPY | buffer_atr=0.05/sl=range_1.00/tp=r_3.0/rf=none | 530 | 0.041 | 0.028 | 1.143 | 0.022 | -0.059 |
| A_asian_range_breakout | USDJPY | buffer_atr=0.0/sl=range_1.00/tp=r_3.0/rf=gt_0.25 | 438 | 0.039 | 0.030 | 1.151 | 0.045 | -0.023 |
| A_asian_range_breakout | USDJPY | buffer_atr=0.025/sl=range_1.00/tp=r_3.0/rf=gt_0.25 | 401 | 0.030 | 0.030 | 1.114 | 0.039 | -0.063 |
| A_asian_range_breakout | USDJPY | buffer_atr=0.05/sl=range_opposite/tp=r_3.0/rf=none | 530 | 0.039 | 0.026 | 1.178 | 0.003 | -0.025 |

Si A (mejor IS) no coincide con D (mejor robusta) y su OOS es peor, eso es evidencia directa de sobreoptimización. C es sólo informativo: elegir por C sería look-ahead.

## 6. Resultados OUT-OF-SAMPLE de la selección congelada

| strategy | symbol | IS_trades | IS_expectancy_R | VAL_trades | VAL_expectancy_R | OOS_trades | OOS_win_rate | OOS_expectancy_R | OOS_profit_factor | OOS_net_return_pct | OOS_max_dd_pct | OOS_sharpe |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A_asian_range_breakout | JP225 | 164 | 0.034 | 47 | 0.037 | 53 | 0.415 | -0.012 | 0.946 | -0.347 | 2.640 | -0.406 |
| A_asian_range_breakout | EURJPY | 370 | 0.053 | 139 | -0.003 | 151 | 0.430 | -0.033 | 0.902 | -2.500 | 6.240 | -0.464 |
| C_tokyo_or_breakout | USDJPY | 803 | 0.007 | 268 | 0.007 | 269 | 0.494 | -0.016 | 0.898 | -1.998 | 3.493 | -0.574 |
| E_tokyo_breakout_vwap | USDJPY | 530 | 0.037 | 195 | 0.019 | 184 | 0.500 | -0.033 | 0.863 | -2.969 | 8.344 | -0.716 |
| E_tokyo_breakout_vwap | JP225 | 197 | 0.013 | 62 | -0.030 | 63 | 0.444 | -0.001 | 0.989 | -0.048 | 1.231 | -0.243 |
| A_asian_range_breakout | USDJPY | 438 | 0.039 | 188 | 0.064 | 162 | 0.531 | -0.053 | 0.879 | -4.353 | 12.496 | -0.685 |
| D_tokyo_or_failed_breakout | USDJPY | 189 | 0.002 | 72 | 0.026 | 69 | 0.652 | -0.130 | 0.549 | -4.313 | 5.481 | -1.834 |
| E_tokyo_breakout_vwap | AUDJPY | 125 | 0.082 | 36 | -0.110 | 40 | 0.300 | -0.084 | 0.539 | -1.600 | 2.005 | -1.218 |
| A_asian_range_breakout | AUDJPY | 124 | 0.142 | 37 | -0.240 | 41 | 0.293 | -0.085 | 0.693 | -1.723 | 3.017 | -0.803 |
| A_asian_range_breakout | NZDUSD | 494 | -0.012 | 170 | -0.009 | 170 | 0.406 | -0.038 | 0.618 | -3.010 | 3.778 | -2.179 |
| A_asian_range_breakout | XAUUSD | 1248 | -0.014 | 419 | -0.016 | 386 | 0.508 | 0.012 | 1.183 | -0.236 | 0.949 | -0.299 |
| C_tokyo_or_breakout | XAUUSD | 1450 | -0.018 | 483 | -0.012 | 485 | 0.532 | 0.002 | 1.015 | 0.538 | 1.730 | 0.120 |
| A_asian_range_breakout | AUDUSD | 544 | -0.011 | 179 | -0.020 | 177 | 0.407 | -0.041 | 0.606 | -3.367 | 3.577 | -2.467 |
| D_tokyo_or_failed_breakout | AUDJPY | 214 | -0.027 | 77 | -0.017 | 59 | 0.695 | -0.045 | 0.820 | -1.302 | 3.419 | -0.433 |
| D_tokyo_or_failed_breakout | JP225 | 156 | -0.031 | 43 | -0.011 | 43 | 0.512 | -0.072 | 0.737 | -1.546 | 2.585 | -1.021 |
| C_tokyo_or_breakout | JP225 | 708 | 0.014 | 236 | -0.053 | 236 | 0.462 | -0.061 | 0.726 | -7.035 | 8.026 | -1.779 |
| D_tokyo_or_failed_breakout | XAUUSD | 209 | -0.029 | 68 | -0.000 | 85 | 0.459 | -0.120 | 0.577 | -2.457 | 3.013 | -0.966 |
| C_tokyo_or_breakout | AUDJPY | 697 | 0.003 | 230 | -0.058 | 228 | 0.469 | -0.044 | 0.718 | -4.723 | 5.155 | -1.702 |
| B_asian_failed_breakout | AUDUSD | 254 | -0.051 | 90 | -0.082 | 76 | 0.421 | -0.025 | 0.921 | -1.098 | 3.807 | -0.293 |
| B_asian_failed_breakout | EURJPY | 150 | -0.076 | 53 | 0.030 | 71 | 0.380 | -0.235 | 0.586 | -7.956 | 10.144 | -1.973 |
| B_asian_failed_breakout | XAUUSD | 197 | -0.111 | 52 | 0.013 | 97 | 0.402 | -0.138 | 0.555 | -4.598 | 5.621 | -1.303 |
| B_asian_failed_breakout | JP225 | 305 | -0.107 | 101 | -0.164 | 92 | 0.489 | -0.049 | 0.877 | -2.294 | 4.001 | -0.565 |
| B_asian_failed_breakout | AUDJPY | 255 | -0.152 | 84 | -0.051 | 77 | 0.494 | -0.116 | 0.659 | -4.362 | 5.729 | -1.594 |
| B_asian_failed_breakout | USDJPY | 397 | -0.117 | 143 | -0.078 | 144 | 0.458 | -0.200 | 0.593 | -13.381 | 13.381 | -2.707 |
| B_asian_failed_breakout | NZDUSD | 193 | -0.168 | 65 | -0.185 | 65 | 0.354 | -0.208 | 0.502 | -6.552 | 7.679 | -2.170 |

## 7. Walk-forward (sólo período pre-OOS)

| strategy | symbol | windows | wf_positive | wf_net_R | final_net_R | distinct_cfgs |
|---|---|---|---|---|---|---|
| A_asian_range_breakout | AUDJPY | 4 | 0.500 | 0.355 | -0.286 | 3 |
| A_asian_range_breakout | AUDUSD | 4 | 0.000 | -48.313 | -10.354 | 4 |
| A_asian_range_breakout | EURJPY | 4 | 0.500 | 5.495 | 6.002 | 3 |
| A_asian_range_breakout | JP225 | 4 | 0.750 | 0.392 | 4.497 | 3 |
| A_asian_range_breakout | NZDUSD | 4 | 0.000 | -15.038 | -6.982 | 4 |
| A_asian_range_breakout | USDJPY | 4 | 0.500 | 12.054 | 29.025 | 3 |
| A_asian_range_breakout | XAUUSD | 11 | 0.273 | -17.968 | -15.695 | 9 |
| B_asian_failed_breakout | AUDJPY | 4 | 0.250 | -22.753 | -16.392 | 3 |
| B_asian_failed_breakout | AUDUSD | 4 | 0.000 | -30.159 | -11.577 | 3 |
| B_asian_failed_breakout | EURJPY | 4 | 0.250 | -13.330 | 0.959 | 4 |
| B_asian_failed_breakout | JP225 | 4 | 0.500 | -5.179 | -16.317 | 1 |
| B_asian_failed_breakout | NZDUSD | 4 | 0.000 | -37.770 | -25.398 | 3 |
| B_asian_failed_breakout | USDJPY | 4 | 0.000 | -65.496 | -50.765 | 3 |
| B_asian_failed_breakout | XAUUSD | 11 | 0.182 | -57.147 | -13.880 | 9 |
| C_tokyo_or_breakout | AUDJPY | 4 | 0.250 | -38.346 | -9.742 | 4 |
| C_tokyo_or_breakout | JP225 | 4 | 0.500 | -23.577 | -8.062 | 4 |
| C_tokyo_or_breakout | USDJPY | 4 | 0.500 | -5.035 | 6.845 | 3 |
| C_tokyo_or_breakout | XAUUSD | 11 | 0.091 | -30.314 | -25.073 | 7 |
| D_tokyo_or_failed_breakout | AUDJPY | 4 | 0.000 | -8.042 | -5.148 | 3 |
| D_tokyo_or_failed_breakout | JP225 | 4 | 0.000 | -10.003 | -7.080 | 4 |
| D_tokyo_or_failed_breakout | USDJPY | 4 | 0.500 | -0.798 | 0.839 | 3 |
| D_tokyo_or_failed_breakout | XAUUSD | 11 | 0.273 | -20.568 | -5.123 | 9 |
| E_tokyo_breakout_vwap | AUDJPY | 4 | 0.500 | 1.434 | 1.742 | 3 |
| E_tokyo_breakout_vwap | JP225 | 4 | 0.250 | -3.312 | -1.112 | 4 |
| E_tokyo_breakout_vwap | USDJPY | 4 | 0.500 | 6.566 | 17.486 | 4 |

`distinct_cfgs` alto = la configuración óptima cambia de ventana en ventana (inestable).

## 8. Monte Carlo (10.000 simulaciones) y drawdown

| strategy | symbol | risk_pct | trades | maxDD_median | maxDD_p95 | maxDD_p99 | worst_losing_streak | prob_ruin | boot_prob_ruin | return_p05 | return_median | return_p95 | prob_loss |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A_asian_range_breakout | JP225 | 0.250 | 264 | 1.939 | 3.024 | 3.615 | 22 | 0.000 | 0.000 | -2.295 | 1.662 | 5.773 | 0.249 |
| A_asian_range_breakout | JP225 | 0.500 | 264 | 3.852 | 5.973 | 7.120 | 22 | 0.000 | 0.000 | -4.589 | 3.294 | 11.808 | 0.252 |
| A_asian_range_breakout | JP225 | 1 | 264 | 7.602 | 11.647 | 13.810 | 22 | 0.000 | 0.000 | -9.159 | 6.447 | 24.711 | 0.260 |
| A_asian_range_breakout | EURJPY | 0.250 | 660 | 4.430 | 6.796 | 7.976 | 24 | 0.000 | 0.000 | -4.963 | 3.470 | 13.103 | 0.253 |
| A_asian_range_breakout | EURJPY | 0.500 | 660 | 8.729 | 13.204 | 15.433 | 24 | 0.000 | 0.000 | -9.907 | 6.762 | 27.541 | 0.263 |
| A_asian_range_breakout | EURJPY | 1 | 660 | 16.924 | 24.966 | 28.750 | 24 | 0.000 | 0.000 | -19.678 | 12.730 | 60.797 | 0.282 |
| C_tokyo_or_breakout | USDJPY | 0.250 | 1340 | 3.536 | 5.353 | 6.317 | 34 | 0.000 | 0.000 | -5.149 | 0.685 | 6.822 | 0.421 |
| C_tokyo_or_breakout | USDJPY | 0.500 | 1340 | 6.982 | 10.472 | 12.304 | 34 | 0.000 | 0.000 | -10.149 | 1.246 | 13.967 | 0.429 |
| C_tokyo_or_breakout | USDJPY | 1 | 1340 | 13.622 | 20.011 | 23.282 | 34 | 0.000 | 0.000 | -19.678 | 1.985 | 29.227 | 0.443 |
| E_tokyo_breakout_vwap | USDJPY | 0.250 | 909 | 3.717 | 5.737 | 6.708 | 21 | 0.000 | 0.000 | -3.497 | 4.418 | 12.966 | 0.180 |
| E_tokyo_breakout_vwap | USDJPY | 0.500 | 909 | 7.339 | 11.195 | 13.026 | 21 | 0.000 | 0.000 | -7.075 | 8.782 | 27.301 | 0.186 |
| E_tokyo_breakout_vwap | USDJPY | 1 | 909 | 14.298 | 21.333 | 24.565 | 21 | 0.000 | 0.000 | -14.416 | 17.278 | 60.599 | 0.200 |
| E_tokyo_breakout_vwap | JP225 | 0.250 | 322 | 1.427 | 2.131 | 2.496 | 21 | 0.000 | 0.000 | -2.140 | 0.144 | 2.618 | 0.460 |
| E_tokyo_breakout_vwap | JP225 | 0.500 | 322 | 2.840 | 4.224 | 4.938 | 21 | 0.000 | 0.000 | -4.251 | 0.267 | 5.282 | 0.463 |
| E_tokyo_breakout_vwap | JP225 | 1 | 322 | 5.625 | 8.298 | 9.667 | 21 | 0.000 | 0.000 | -8.398 | 0.456 | 10.750 | 0.468 |
| A_asian_range_breakout | USDJPY | 0.250 | 788 | 5.822 | 8.833 | 10.308 | 21 | 0.000 | 0.000 | -6.704 | 5.017 | 18.057 | 0.247 |
| A_asian_range_breakout | USDJPY | 0.500 | 788 | 11.406 | 17.041 | 19.692 | 21 | 0.000 | 0.000 | -13.349 | 9.748 | 38.668 | 0.257 |
| A_asian_range_breakout | USDJPY | 1 | 788 | 21.870 | 31.613 | 36.036 | 21 | 0.000 | 0.005 | -26.328 | 18.149 | 88.202 | 0.279 |
| D_tokyo_or_failed_breakout | USDJPY | 0.250 | 330 | 3.143 | 4.337 | 4.861 | 11 | 0.000 | 0.000 | -5.282 | -1.669 | 1.934 | 0.778 |
| D_tokyo_or_failed_breakout | USDJPY | 0.500 | 330 | 6.221 | 8.514 | 9.512 | 11 | 0.000 | 0.000 | -10.332 | -3.360 | 3.856 | 0.781 |
| D_tokyo_or_failed_breakout | USDJPY | 1 | 330 | 12.175 | 16.415 | 18.213 | 11 | 0.000 | 0.000 | -19.769 | -6.793 | 7.655 | 0.787 |
| E_tokyo_breakout_vwap | AUDJPY | 0.250 | 201 | 1.166 | 1.813 | 2.145 | 19 | 0.000 | 0.000 | -1.531 | 0.678 | 3.020 | 0.307 |
| E_tokyo_breakout_vwap | AUDJPY | 0.500 | 201 | 2.324 | 3.599 | 4.248 | 19 | 0.000 | 0.000 | -3.054 | 1.341 | 6.106 | 0.310 |
| E_tokyo_breakout_vwap | AUDJPY | 1 | 201 | 4.613 | 7.093 | 8.340 | 19 | 0.000 | 0.000 | -6.076 | 2.624 | 12.497 | 0.316 |
| A_asian_range_breakout | AUDJPY | 0.250 | 202 | 2.163 | 3.371 | 3.918 | 21 | 0.000 | 0.000 | -2.876 | 1.248 | 5.718 | 0.309 |
| A_asian_range_breakout | AUDJPY | 0.500 | 202 | 4.299 | 6.643 | 7.701 | 21 | 0.000 | 0.000 | -5.723 | 2.450 | 11.682 | 0.314 |
| A_asian_range_breakout | AUDJPY | 1 | 202 | 8.468 | 12.906 | 14.878 | 21 | 0.000 | 0.000 | -11.318 | 4.691 | 24.359 | 0.323 |
| A_asian_range_breakout | NZDUSD | 0.250 | 834 | 3.919 | 4.588 | 4.931 | 28 | 0.000 | 0.000 | -5.955 | -3.455 | -1.050 | 0.992 |
| A_asian_range_breakout | NZDUSD | 0.500 | 834 | 7.703 | 8.983 | 9.634 | 28 | 0.000 | 0.000 | -11.575 | -6.812 | -2.115 | 0.992 |
| A_asian_range_breakout | NZDUSD | 1 | 834 | 14.884 | 17.222 | 18.399 | 28 | 0.000 | 0.000 | -21.882 | -13.241 | -4.284 | 0.992 |

Permutación: mismas operaciones reordenadas (riesgo de secuencia). Bootstrap: remuestreo con reposición (distribución del retorno). Ruina = drawdown >= 50%.

### Gestión de capital (todo el período)

| strategy | symbol | sizing | trades | net_return_pct | cagr_pct | max_dd_pct | avg_dd_pct | sharpe | sortino | calmar | recovery_factor | profit_factor | max_consec_losses | skipped_unsizable |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A_asian_range_breakout | JP225 | riesgo 0.25% | 264 | 1.665 | 0.320 | 1.947 | 1.010 | 0.302 | 0.490 | 0.164 | 0.849 | 1.115 | 9 | 0 |
| A_asian_range_breakout | JP225 | riesgo 0.5% | 264 | 3.299 | 0.629 | 3.869 | 2.010 | 0.302 | 0.490 | 0.163 | 0.840 | 1.113 | 9 | 0 |
| A_asian_range_breakout | JP225 | riesgo 1.0% | 264 | 6.461 | 1.217 | 7.634 | 3.978 | 0.302 | 0.490 | 0.159 | 0.821 | 1.109 | 9 | 0 |
| A_asian_range_breakout | JP225 | lote fijo 0.1 | 264 | 0.008 | 0.002 | 0.029 | 0.012 | 0.127 | 0.196 | 0.056 | 0.291 | 1.054 | 9 | 0 |
| A_asian_range_breakout | EURJPY | riesgo 0.25% | 660 | 2.994 | 0.572 | 3.560 | 0.705 | 0.268 | 0.416 | 0.161 | 0.797 | 1.060 | 10 | 0 |
| A_asian_range_breakout | EURJPY | riesgo 0.5% | 660 | 6.125 | 1.156 | 6.854 | 1.680 | 0.274 | 0.426 | 0.169 | 0.805 | 1.057 | 10 | 0 |
| A_asian_range_breakout | EURJPY | riesgo 1.0% | 660 | 12.322 | 2.271 | 13.544 | 3.359 | 0.287 | 0.446 | 0.168 | 0.738 | 1.054 | 10 | 0 |
| A_asian_range_breakout | EURJPY | lote fijo 0.1 | 660 | 5.368 | 1.016 | 4.325 | 1.011 | 0.316 | 0.502 | 0.235 | 1.148 | 1.076 | 10 | 0 |
| C_tokyo_or_breakout | USDJPY | riesgo 0.25% | 1340 | 0.080 | 0.015 | 2.212 | 0.431 | 0.021 | 0.030 | 0.007 | 0.035 | 1.002 | 13 | 0 |
| C_tokyo_or_breakout | USDJPY | riesgo 0.5% | 1340 | 0.751 | 0.145 | 4.591 | 0.964 | 0.066 | 0.097 | 0.032 | 0.156 | 1.009 | 13 | 0 |
| C_tokyo_or_breakout | USDJPY | riesgo 1.0% | 1340 | 1.624 | 0.312 | 8.873 | 2.026 | 0.083 | 0.122 | 0.035 | 0.168 | 1.009 | 13 | 0 |
| C_tokyo_or_breakout | USDJPY | lote fijo 0.1 | 1340 | 2.560 | 0.490 | 10.077 | 2.002 | 0.116 | 0.171 | 0.049 | 0.245 | 1.016 | 13 | 0 |
| E_tokyo_breakout_vwap | USDJPY | riesgo 0.25% | 909 | 4.386 | 0.833 | 4.197 | 0.580 | 0.433 | 0.697 | 0.198 | 0.971 | 1.090 | 8 | 0 |
| E_tokyo_breakout_vwap | USDJPY | riesgo 0.5% | 909 | 8.557 | 1.599 | 8.375 | 1.203 | 0.411 | 0.661 | 0.191 | 0.884 | 1.082 | 8 | 0 |
| E_tokyo_breakout_vwap | USDJPY | riesgo 1.0% | 909 | 16.523 | 2.999 | 16.383 | 2.532 | 0.398 | 0.639 | 0.183 | 0.762 | 1.074 | 8 | 0 |
| E_tokyo_breakout_vwap | USDJPY | lote fijo 0.1 | 909 | 6.316 | 1.191 | 5.136 | 1.057 | 0.365 | 0.584 | 0.232 | 1.121 | 1.083 | 8 | 0 |
| E_tokyo_breakout_vwap | JP225 | riesgo 0.25% | 283 | 0.351 | 0.068 | 1.104 | 0.462 | 0.115 | 0.184 | 0.061 | 0.316 | 1.043 | 8 | 0 |
| E_tokyo_breakout_vwap | JP225 | riesgo 0.5% | 322 | 0.309 | 0.060 | 2.258 | 0.943 | 0.053 | 0.082 | 0.026 | 0.134 | 1.016 | 9 | 0 |
| E_tokyo_breakout_vwap | JP225 | riesgo 1.0% | 322 | 0.536 | 0.103 | 4.492 | 1.875 | 0.053 | 0.082 | 0.023 | 0.115 | 1.014 | 9 | 0 |
| E_tokyo_breakout_vwap | JP225 | lote fijo 0.1 | 322 | 0.005 | 0.001 | 0.032 | 0.011 | 0.061 | 0.097 | 0.030 | 0.158 | 1.025 | 9 | 0 |
| A_asian_range_breakout | USDJPY | riesgo 0.25% | 788 | 4.895 | 0.928 | 6.280 | 0.901 | 0.318 | 0.486 | 0.148 | 0.716 | 1.060 | 9 | 0 |
| A_asian_range_breakout | USDJPY | riesgo 0.5% | 788 | 9.693 | 1.804 | 12.554 | 1.908 | 0.318 | 0.486 | 0.144 | 0.651 | 1.056 | 9 | 0 |
| A_asian_range_breakout | USDJPY | riesgo 1.0% | 788 | 18.249 | 3.292 | 23.866 | 3.752 | 0.319 | 0.488 | 0.138 | 0.551 | 1.050 | 9 | 0 |
| A_asian_range_breakout | USDJPY | lote fijo 0.1 | 788 | 2.566 | 0.491 | 3.745 | 0.745 | 0.214 | 0.314 | 0.131 | 0.676 | 1.043 | 9 | 0 |
| D_tokyo_or_failed_breakout | USDJPY | riesgo 0.25% | 330 | -1.577 | -0.307 | 2.928 | 0.751 | -0.321 | -0.376 | -0.105 | -0.532 | 0.901 | 4 | 0 |
| D_tokyo_or_failed_breakout | USDJPY | riesgo 0.5% | 330 | -3.287 | -0.644 | 6.030 | 1.536 | -0.323 | -0.378 | -0.107 | -0.531 | 0.900 | 4 | 0 |
| D_tokyo_or_failed_breakout | USDJPY | riesgo 1.0% | 330 | -6.889 | -1.370 | 12.122 | 3.104 | -0.330 | -0.387 | -0.113 | -0.539 | 0.897 | 4 | 0 |
| D_tokyo_or_failed_breakout | USDJPY | lote fijo 0.1 | 330 | -1.272 | -0.247 | 3.396 | 0.722 | -0.221 | -0.260 | -0.073 | -0.368 | 0.929 | 4 | 0 |
| E_tokyo_breakout_vwap | AUDJPY | riesgo 0.25% | 201 | 0.442 | 0.085 | 1.873 | 0.205 | 0.162 | 0.246 | 0.046 | 0.231 | 1.076 | 8 | 0 |
| E_tokyo_breakout_vwap | AUDJPY | riesgo 0.5% | 201 | 1.251 | 0.241 | 3.774 | 0.404 | 0.214 | 0.330 | 0.064 | 0.317 | 1.099 | 8 | 0 |
| E_tokyo_breakout_vwap | AUDJPY | riesgo 1.0% | 201 | 2.601 | 0.498 | 7.703 | 0.821 | 0.221 | 0.341 | 0.065 | 0.306 | 1.097 | 8 | 0 |
| E_tokyo_breakout_vwap | AUDJPY | lote fijo 0.1 | 201 | 2.186 | 0.419 | 4.764 | 0.550 | 0.254 | 0.410 | 0.088 | 0.429 | 1.121 | 8 | 0 |
| A_asian_range_breakout | AUDJPY | riesgo 0.25% | 202 | 1.078 | 0.208 | 3.816 | 0.463 | 0.197 | 0.315 | 0.054 | 0.271 | 1.088 | 8 | 0 |
| A_asian_range_breakout | AUDJPY | riesgo 0.5% | 202 | 2.428 | 0.465 | 7.640 | 0.870 | 0.217 | 0.350 | 0.061 | 0.290 | 1.094 | 8 | 0 |
| A_asian_range_breakout | AUDJPY | riesgo 1.0% | 202 | 4.724 | 0.896 | 14.920 | 1.770 | 0.217 | 0.351 | 0.060 | 0.264 | 1.086 | 8 | 0 |
| A_asian_range_breakout | AUDJPY | lote fijo 0.1 | 202 | 1.397 | 0.268 | 5.377 | 0.630 | 0.166 | 0.265 | 0.050 | 0.244 | 1.076 | 8 | 0 |
| A_asian_range_breakout | NZDUSD | riesgo 0.25% | 834 | -2.960 | -0.579 | 3.590 | 0.671 | -0.992 | -1.323 | -0.161 | -0.821 | 0.806 | 11 | 0 |
| A_asian_range_breakout | NZDUSD | riesgo 0.5% | 834 | -6.456 | -1.282 | 7.734 | 1.430 | -1.012 | -1.344 | -0.166 | -0.828 | 0.804 | 11 | 0 |
| A_asian_range_breakout | NZDUSD | riesgo 1.0% | 834 | -12.956 | -2.646 | 15.470 | 2.866 | -1.003 | -1.334 | -0.171 | -0.822 | 0.806 | 11 | 0 |
| A_asian_range_breakout | NZDUSD | lote fijo 0.1 | 834 | -9.621 | -1.936 | 11.479 | 1.858 | -0.906 | -1.204 | -0.169 | -0.826 | 0.820 | 11 | 0 |
| A_asian_range_breakout | XAUUSD | riesgo 0.25% | 640 | -2.461 | -0.265 | 2.569 | 1.350 | -1.002 | -1.312 | -0.103 | -0.957 | 0.717 | 11 | 0 |
| A_asian_range_breakout | XAUUSD | riesgo 0.5% | 1602 | -8.877 | -0.984 | 9.445 | 4.919 | -1.065 | -1.423 | -0.104 | -0.938 | 0.800 | 11 | 0 |
| A_asian_range_breakout | XAUUSD | riesgo 1.0% | 1832 | -17.788 | -2.063 | 19.171 | 9.981 | -0.956 | -1.297 | -0.108 | -0.924 | 0.828 | 11 | 0 |
| A_asian_range_breakout | XAUUSD | lote fijo 0.1 | 2053 | 4.421 | 0.461 | 66.231 | 10.615 | 0.129 | 0.202 | 0.007 | 0.066 | 1.007 | 11 | 0 |
| C_tokyo_or_breakout | XAUUSD | riesgo 0.25% | 1218 | -1.927 | -0.207 | 3.091 | 1.562 | -0.261 | -0.372 | -0.067 | -0.623 | 0.937 | 8 | 0 |
| C_tokyo_or_breakout | XAUUSD | riesgo 0.5% | 2044 | -9.771 | -1.088 | 11.323 | 11.323 | -0.567 | -0.789 | -0.096 | -0.863 | 0.896 | 8 | 0 |
| C_tokyo_or_breakout | XAUUSD | riesgo 1.0% | 2165 | -22.746 | -2.709 | 27.094 | 27.094 | -0.640 | -0.876 | -0.100 | -0.840 | 0.884 | 8 | 0 |
| C_tokyo_or_breakout | XAUUSD | lote fijo 0.1 | 2418 | -112.783 | -100 | 143.346 | 71.754 | 0.068 | 0.090 | -0.698 | -0.787 | 0.903 | 8 | 0 |
| A_asian_range_breakout | AUDUSD | riesgo 0.25% | 900 | -3.647 | -0.715 | 4.096 | 0.865 | -1.101 | -1.487 | -0.175 | -0.887 | 0.791 | 9 | 0 |
| A_asian_range_breakout | AUDUSD | riesgo 0.5% | 900 | -7.336 | -1.462 | 8.230 | 1.812 | -1.060 | -1.436 | -0.178 | -0.884 | 0.801 | 9 | 0 |
| A_asian_range_breakout | AUDUSD | riesgo 1.0% | 900 | -15.073 | -3.108 | 16.991 | 3.218 | -1.078 | -1.451 | -0.183 | -0.869 | 0.800 | 9 | 0 |
| A_asian_range_breakout | AUDUSD | lote fijo 0.1 | 900 | -11.828 | -2.403 | 13.892 | 2.723 | -0.917 | -1.249 | -0.173 | -0.833 | 0.822 | 9 | 0 |
| D_tokyo_or_failed_breakout | AUDJPY | riesgo 0.25% | 350 | -2.199 | -0.429 | 3.813 | 0.858 | -0.403 | -0.479 | -0.112 | -0.573 | 0.881 | 4 | 0 |
| D_tokyo_or_failed_breakout | AUDJPY | riesgo 0.5% | 350 | -4.689 | -0.924 | 7.857 | 1.766 | -0.420 | -0.498 | -0.118 | -0.590 | 0.875 | 4 | 0 |
| D_tokyo_or_failed_breakout | AUDJPY | riesgo 1.0% | 350 | -9.459 | -1.902 | 15.421 | 3.481 | -0.419 | -0.497 | -0.123 | -0.599 | 0.873 | 4 | 0 |
| D_tokyo_or_failed_breakout | AUDJPY | lote fijo 0.1 | 350 | -2.821 | -0.552 | 4.075 | 0.989 | -0.485 | -0.561 | -0.135 | -0.689 | 0.847 | 4 | 0 |
| D_tokyo_or_failed_breakout | JP225 | riesgo 0.25% | 240 | -1.874 | -0.365 | 3.035 | 0.720 | -0.435 | -0.525 | -0.120 | -0.612 | 0.849 | 6 | 0 |
| D_tokyo_or_failed_breakout | JP225 | riesgo 0.5% | 242 | -4.149 | -0.816 | 6.397 | 1.493 | -0.482 | -0.581 | -0.128 | -0.637 | 0.834 | 6 | 0 |
| D_tokyo_or_failed_breakout | JP225 | riesgo 1.0% | 242 | -8.254 | -1.651 | 12.476 | 2.933 | -0.482 | -0.581 | -0.132 | -0.639 | 0.833 | 6 | 0 |
| D_tokyo_or_failed_breakout | JP225 | lote fijo 0.1 | 242 | -0.023 | -0.004 | 0.032 | 0.008 | -0.466 | -0.559 | -0.136 | -0.705 | 0.821 | 6 | 0 |

## 9. MAE / MFE (en R)

| mae_R_winners_mean | mae_R_losers_mean | mfe_R_mean | mfe_R_winners_mean | mfe_R_losers_mean | winners_mae_gt_0.8R_share | losers_mfe_ge_1R_share | losers_mfe_ge_0.5R_share |
|---|---|---|---|---|---|---|---|
| 0.209 | 0.534 | 0.346 | 0.549 | 0.154 | 0.021 | 0.009 | 0.067 |

- La mediana de MFE es 0.21R: targets muy por encima de ~0.44R (p75) se alcanzan pocas veces.

| strategy | symbol | mae_R_winners_mean | mae_R_losers_mean | mfe_R_mean | mfe_R_winners_mean | mfe_R_losers_mean | winners_mae_gt_0.8R_share | losers_mfe_ge_1R_share | losers_mfe_ge_0.5R_share | mfe_p50 | mfe_p75 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A_asian_range_breakout | AUDJPY | 0.286 | 0.673 | 0.519 | 0.883 | 0.215 | 0.011 | 0.018 | 0.091 | 0.355 | 0.738 |
| A_asian_range_breakout | AUDUSD | 0.092 | 0.259 | 0.154 | 0.246 | 0.076 | 0.000 | 0.000 | 0.002 | 0.121 | 0.212 |
| A_asian_range_breakout | EURJPY | 0.326 | 0.796 | 0.605 | 0.958 | 0.283 | 0.025 | 0.041 | 0.194 | 0.439 | 0.892 |
| A_asian_range_breakout | JP225 | 0.267 | 0.572 | 0.484 | 0.816 | 0.198 | 0.025 | 0.000 | 0.099 | 0.366 | 0.629 |
| A_asian_range_breakout | NZDUSD | 0.099 | 0.242 | 0.141 | 0.236 | 0.063 | 0.000 | 0.000 | 0.000 | 0.110 | 0.210 |
| A_asian_range_breakout | USDJPY | 0.418 | 1.030 | 0.981 | 1.614 | 0.301 | 0.108 | 0.000 | 0.226 | 0.695 | 1.305 |
| A_asian_range_breakout | XAUUSD | 0.076 | 0.215 | 0.136 | 0.219 | 0.062 | 0.000 | 0.000 | 0.000 | 0.104 | 0.194 |
| B_asian_failed_breakout | AUDJPY | 0.308 | 0.827 | 0.346 | 0.512 | 0.177 | 0.048 | 0.015 | 0.078 | 0.295 | 0.523 |
| B_asian_failed_breakout | AUDUSD | 0.335 | 0.782 | 0.459 | 0.729 | 0.229 | 0.031 | 0.009 | 0.159 | 0.392 | 0.676 |
| B_asian_failed_breakout | EURJPY | 0.404 | 1.021 | 0.723 | 1.204 | 0.365 | 0.103 | 0.070 | 0.306 | 0.581 | 1.098 |
| B_asian_failed_breakout | JP225 | 0.384 | 0.908 | 0.502 | 0.806 | 0.230 | 0.077 | 0.015 | 0.156 | 0.394 | 0.753 |
| B_asian_failed_breakout | NZDUSD | 0.348 | 0.791 | 0.412 | 0.792 | 0.178 | 0.041 | 0.005 | 0.100 | 0.328 | 0.694 |
| B_asian_failed_breakout | USDJPY | 0.396 | 1.030 | 0.613 | 0.943 | 0.330 | 0.082 | 0.076 | 0.250 | 0.475 | 0.926 |
| B_asian_failed_breakout | XAUUSD | 0.344 | 0.773 | 0.458 | 0.769 | 0.212 | 0.065 | 0.016 | 0.119 | 0.352 | 0.617 |
| C_tokyo_or_breakout | AUDJPY | 0.140 | 0.389 | 0.247 | 0.410 | 0.106 | 0.002 | 0.003 | 0.018 | 0.170 | 0.336 |
| C_tokyo_or_breakout | JP225 | 0.210 | 0.542 | 0.386 | 0.632 | 0.173 | 0.005 | 0.003 | 0.060 | 0.289 | 0.537 |
| C_tokyo_or_breakout | USDJPY | 0.142 | 0.417 | 0.282 | 0.439 | 0.129 | 0.005 | 0.001 | 0.021 | 0.202 | 0.371 |
| C_tokyo_or_breakout | XAUUSD | 0.137 | 0.377 | 0.241 | 0.376 | 0.111 | 0.001 | 0.001 | 0.016 | 0.189 | 0.341 |
| D_tokyo_or_failed_breakout | AUDJPY | 0.285 | 0.876 | 0.271 | 0.340 | 0.116 | 0.029 | 0.000 | 0.028 | 0.246 | 0.370 |
| D_tokyo_or_failed_breakout | JP225 | 0.255 | 0.682 | 0.256 | 0.360 | 0.108 | 0.035 | 0.000 | 0.010 | 0.231 | 0.389 |
| D_tokyo_or_failed_breakout | USDJPY | 0.251 | 0.890 | 0.261 | 0.323 | 0.095 | 0.054 | 0.000 | 0.000 | 0.224 | 0.335 |
| D_tokyo_or_failed_breakout | XAUUSD | 0.240 | 0.643 | 0.262 | 0.367 | 0.128 | 0.010 | 0.000 | 0.019 | 0.226 | 0.344 |
| E_tokyo_breakout_vwap | AUDJPY | 0.149 | 0.383 | 0.266 | 0.448 | 0.109 | 0.000 | 0.000 | 0.019 | 0.182 | 0.374 |
| E_tokyo_breakout_vwap | JP225 | 0.142 | 0.310 | 0.242 | 0.397 | 0.103 | 0.000 | 0.000 | 0.012 | 0.160 | 0.326 |
| E_tokyo_breakout_vwap | USDJPY | 0.256 | 0.650 | 0.485 | 0.751 | 0.228 | 0.009 | 0.015 | 0.108 | 0.356 | 0.662 |

## 9b. Hora UTC, día y volatilidad

### by_hour (Kruskal-Wallis p = 0.0012)
| hour_utc | trades | win_rate | expectancy_R | ci95_lo | ci95_hi | profit_factor | average_R | max_dd_R | net_R |
|---|---|---|---|---|---|---|---|---|---|
| 0.000 | 3856 | 0.492 | -0.006 | -0.019 | 0.007 | 0.962 | -0.006 | 37.665 | -21.610 |
| 1 | 1392 | 0.484 | -0.029 | -0.053 | -0.007 | 0.835 | -0.029 | 43.416 | -40.861 |
| 2 | 529 | 0.558 | -0.006 | -0.045 | 0.032 | 0.963 | -0.006 | 13.466 | -3.414 |
| 3 | 3076 | 0.481 | -0.008 | -0.030 | 0.013 | 0.959 | -0.008 | 58.718 | -25.714 |
| 4 | 2114 | 0.502 | -0.004 | -0.032 | 0.024 | 0.984 | -0.004 | 27.252 | -8.167 |
| 5 | 1961 | 0.473 | -0.048 | -0.075 | -0.021 | 0.803 | -0.048 | 104.796 | -94.571 |
| 6 | 2254 | 0.485 | -0.047 | -0.072 | -0.021 | 0.808 | -0.047 | 113.580 | -105.062 |
| 7 | 2131 | 0.470 | -0.050 | -0.073 | -0.026 | 0.771 | -0.050 | 107.043 | -106.553 |
| 8 | 158 | 0.380 | -0.109 | -0.176 | -0.045 | 0.476 | -0.109 | 18.998 | -17.187 |

### by_day (Kruskal-Wallis p = 0.4325)
| day | trades | win_rate | expectancy_R | ci95_lo | ci95_hi | profit_factor | average_R | max_dd_R | net_R |
|---|---|---|---|---|---|---|---|---|---|
| Monday | 3346 | 0.491 | -0.008 | -0.026 | 0.010 | 0.958 | -0.008 | 46.929 | -26.965 |
| Tuesday | 3596 | 0.489 | -0.020 | -0.037 | -0.003 | 0.902 | -0.020 | 76.534 | -72.949 |
| Wednesday | 3515 | 0.481 | -0.028 | -0.046 | -0.010 | 0.861 | -0.028 | 99.668 | -98.486 |
| Thursday | 3595 | 0.490 | -0.026 | -0.043 | -0.008 | 0.876 | -0.026 | 93.931 | -92.628 |
| Friday | 3419 | 0.479 | -0.039 | -0.057 | -0.021 | 0.818 | -0.039 | 138.867 | -132.112 |

### by_volatility (Kruskal-Wallis p = 0.2320)
| vol_regime | trades | win_rate | expectancy_R | ci95_lo | ci95_hi | profit_factor | average_R | max_dd_R | net_R |
|---|---|---|---|---|---|---|---|---|---|
| low | 5361 | 0.481 | -0.034 | -0.048 | -0.020 | 0.837 | -0.034 | 193.166 | -180.594 |
| medium | 4242 | 0.483 | -0.034 | -0.050 | -0.018 | 0.831 | -0.034 | 143.905 | -142.667 |
| high | 7142 | 0.491 | -0.012 | -0.024 | 0.001 | 0.942 | -0.012 | 101.387 | -84.554 |
| unclassified | 726 | 0.492 | -0.021 | -0.062 | 0.020 | 0.904 | -0.021 | 19.140 | -15.324 |

p > 0.05 => no hay evidencia de que la hora/día/régimen cambie el resultado; no filtrar por eso.

## 10. Sensibilidad a costos

| strategy | symbol | sp1/sl1 | sp1/sl2 | sp1/sl3 | sp1.5/sl1 | sp1.5/sl2 | sp1.5/sl3 | sp2/sl1 | sp2/sl2 | sp2/sl3 |
|---|---|---|---|---|---|---|---|---|---|---|
| A_asian_range_breakout | AUDJPY | 0.054 | 0.037 | 0.020 | 0.032 | 0.015 | -0.002 | 0.009 | -0.008 | -0.025 |
| A_asian_range_breakout | AUDUSD | -0.013 | -0.020 | -0.028 | -0.019 | -0.027 | -0.034 | -0.026 | -0.034 | -0.041 |
| A_asian_range_breakout | EURJPY | 0.038 | 0.020 | 0.002 | 0.010 | -0.008 | -0.025 | -0.009 | -0.027 | -0.045 |
| A_asian_range_breakout | JP225 | 0.035 | 0.014 | -0.007 | 0.003 | -0.018 | -0.039 | -0.022 | -0.043 | -0.064 |
| A_asian_range_breakout | NZDUSD | -0.011 | -0.022 | -0.033 | -0.021 | -0.032 | -0.042 | -0.031 | -0.041 | -0.052 |
| A_asian_range_breakout | USDJPY | 0.047 | 0.022 | -0.003 | 0.021 | -0.003 | -0.028 | 0.003 | -0.021 | -0.050 |
| A_asian_range_breakout | XAUUSD | -0.015 | -0.023 | -0.031 | -0.020 | -0.028 | -0.036 | -0.025 | -0.033 | -0.041 |
| B_asian_failed_breakout | AUDJPY | -0.127 | -0.150 | -0.174 | -0.154 | -0.177 | -0.200 | -0.174 | -0.196 | -0.219 |
| B_asian_failed_breakout | AUDUSD | -0.059 | -0.088 | -0.118 | -0.096 | -0.125 | -0.154 | -0.117 | -0.145 | -0.174 |
| B_asian_failed_breakout | EURJPY | -0.049 | -0.077 | -0.105 | -0.078 | -0.106 | -0.133 | -0.124 | -0.151 | -0.178 |
| B_asian_failed_breakout | JP225 | -0.121 | -0.159 | -0.197 | -0.177 | -0.215 | -0.252 | -0.222 | -0.258 | -0.295 |
| B_asian_failed_breakout | NZDUSD | -0.172 | -0.215 | -0.257 | -0.201 | -0.243 | -0.285 | -0.219 | -0.260 | -0.300 |
| B_asian_failed_breakout | USDJPY | -0.107 | -0.136 | -0.165 | -0.146 | -0.175 | -0.204 | -0.172 | -0.200 | -0.229 |
| B_asian_failed_breakout | XAUUSD | -0.085 | -0.121 | -0.158 | -0.111 | -0.147 | -0.183 | -0.130 | -0.166 | -0.201 |
| C_tokyo_or_breakout | AUDJPY | -0.013 | -0.021 | -0.029 | -0.025 | -0.033 | -0.042 | -0.035 | -0.044 | -0.052 |
| C_tokyo_or_breakout | JP225 | -0.003 | -0.016 | -0.030 | -0.020 | -0.033 | -0.047 | -0.036 | -0.049 | -0.063 |
| C_tokyo_or_breakout | USDJPY | 0.007 | 0.002 | -0.003 | 0.002 | -0.003 | -0.009 | -0.003 | -0.008 | -0.013 |
| C_tokyo_or_breakout | XAUUSD | -0.016 | -0.027 | -0.038 | -0.023 | -0.033 | -0.044 | -0.029 | -0.040 | -0.050 |
| D_tokyo_or_failed_breakout | AUDJPY | -0.024 | -0.042 | -0.060 | -0.054 | -0.072 | -0.090 | -0.081 | -0.098 | -0.116 |
| D_tokyo_or_failed_breakout | JP225 | -0.026 | -0.045 | -0.064 | -0.054 | -0.073 | -0.091 | -0.084 | -0.102 | -0.120 |
| D_tokyo_or_failed_breakout | USDJPY | 0.008 | -0.002 | -0.013 | -0.002 | -0.013 | -0.024 | -0.005 | -0.016 | -0.026 |
| D_tokyo_or_failed_breakout | XAUUSD | -0.022 | -0.041 | -0.060 | -0.039 | -0.058 | -0.077 | -0.050 | -0.069 | -0.088 |
| E_tokyo_breakout_vwap | AUDJPY | 0.039 | 0.030 | 0.022 | 0.028 | 0.020 | 0.011 | 0.016 | 0.007 | -0.001 |
| E_tokyo_breakout_vwap | JP225 | 0.003 | -0.008 | -0.018 | -0.013 | -0.023 | -0.034 | -0.025 | -0.035 | -0.046 |
| E_tokyo_breakout_vwap | USDJPY | 0.033 | 0.019 | 0.005 | 0.022 | 0.008 | -0.005 | 0.012 | -0.001 | -0.015 |

Expectancy (R) pre-OOS por multiplicador de spread / slippage. Si se vuelve <= 0 con spread x1.5 o slippage x2 la estrategia se marca NO ROBUSTA.

## 10b. Restricciones operativas (portafolio por estrategia, todos los activos)

| strategy | mode | trades | win_rate | expectancy_R | profit_factor | max_dd_R | net_R |
|---|---|---|---|---|---|---|---|
| A_asian_range_breakout | per_signal | 2347 | 0.465 | -0.011 | 0.915 | 31.319 | -25.812 |
| A_asian_range_breakout | one_per_session | 2256 | 0.465 | -0.011 | 0.913 | 30.496 | -24.989 |
| A_asian_range_breakout | two_per_session | 2345 | 0.465 | -0.011 | 0.915 | 31.275 | -25.768 |
| B_asian_failed_breakout | per_signal | 1706 | 0.460 | -0.114 | 0.724 | 194.709 | -193.707 |
| B_asian_failed_breakout | one_per_session | 1317 | 0.459 | -0.113 | 0.733 | 149.663 | -149.317 |
| B_asian_failed_breakout | two_per_session | 1659 | 0.459 | -0.115 | 0.723 | 191.531 | -190.529 |
| C_tokyo_or_breakout | per_signal | 2430 | 0.484 | -0.011 | 0.920 | 28.333 | -26.470 |
| C_tokyo_or_breakout | one_per_session | 2422 | 0.483 | -0.011 | 0.919 | 28.564 | -26.444 |
| C_tokyo_or_breakout | two_per_session | 2430 | 0.484 | -0.011 | 0.920 | 28.333 | -26.470 |
| D_tokyo_or_failed_breakout | per_signal | 1099 | 0.653 | -0.022 | 0.895 | 30.093 | -23.697 |
| D_tokyo_or_failed_breakout | one_per_session | 908 | 0.646 | -0.029 | 0.866 | 33.241 | -26.325 |
| D_tokyo_or_failed_breakout | two_per_session | 1081 | 0.652 | -0.024 | 0.886 | 32.103 | -25.707 |
| E_tokyo_breakout_vwap | per_signal | 1044 | 0.485 | 0.015 | 1.073 | 20.712 | 15.157 |
| E_tokyo_breakout_vwap | one_per_session | 1022 | 0.481 | 0.010 | 1.050 | 22.154 | 10.297 |
| E_tokyo_breakout_vwap | two_per_session | 1043 | 0.484 | 0.014 | 1.072 | 20.712 | 15.020 |

## 10c. Filtro de noticias

No se proporcionó calendario (`data/news/calendar.csv`): comparación NO realizada. No se asume que el filtro mejore el sistema.

## 10d. ¿VWAP mejora el expectancy? (estrategia E)

| symbol | segment | pares | delta_expectancy_media | share_mejora | wilcoxon_p |
|---|---|---|---|---|---|
| AUDJPY | IS | 48 | -0.001 | 0.000 | 0.000 |
| AUDJPY | VAL | 48 | -0.000 | 0.000 | 0.002 |
| AUDJPY | OOS | 48 | -0.000 | 0.042 | 0.116 |
| JP225 | IS | 48 | 0.000 | 0.417 | 0.030 |
| JP225 | VAL | 48 | 0.000 | 0.000 |  |
| JP225 | OOS | 48 | 0.000 | 0.000 |  |
| USDJPY | IS | 48 | 0.000 | 0.104 | 0.108 |
| USDJPY | VAL | 48 | 0.000 | 0.000 |  |
| USDJPY | OOS | 48 | 0.000 | 0.000 |  |

delta = expectancy con VWAP - sin VWAP para la misma configuración. Sólo se considera que VWAP mejora si el delta es positivo en IS **y** VAL **y** OOS y p < 0.05.

## 11. Correlación e independencia de señales

Correlación de retornos de la sesión de Tokio (N efectivo = 3.29 de 7 activos):

| index | USDJPY | AUDJPY | AUDUSD | NZDUSD | EURJPY | JP225 | XAUUSD |
|---|---|---|---|---|---|---|---|
| USDJPY | 1 | 0.635 | -0.212 | -0.283 | 0.794 | 0.340 | -0.217 |
| AUDJPY | 0.635 | 1 | 0.620 | 0.420 | 0.757 | 0.485 | 0.120 |
| AUDUSD | -0.212 | 0.620 | 1 | 0.819 | 0.151 | 0.277 | 0.373 |
| NZDUSD | -0.283 | 0.420 | 0.819 | 1 | 0.100 | 0.196 | 0.335 |
| EURJPY | 0.794 | 0.757 | 0.151 | 0.100 | 1 | 0.388 | -0.017 |
| JP225 | 0.340 | 0.485 | 0.277 | 0.196 | 0.388 | 1 | 0.168 |
| XAUUSD | -0.217 | 0.120 | 0.373 | 0.335 | -0.017 | 0.168 | 1 |

### A_asian_range_breakout: N efectivo de apuestas = 4.46 de 7 activos

| par | same_day_share | same_direction_share |
|---|---|---|
| AUDJPY~AUDUSD | 0.171 | 0.931 |
| AUDJPY~EURJPY | 0.195 | 0.874 |
| AUDJPY~JP225 | 0.141 | 0.825 |
| AUDJPY~NZDUSD | 0.148 | 0.805 |
| AUDJPY~USDJPY | 0.172 | 0.816 |
| AUDJPY~XAUUSD | 0.077 | 0.537 |
| AUDUSD~EURJPY | 0.418 | 0.576 |
| AUDUSD~JP225 | 0.200 | 0.711 |
| AUDUSD~NZDUSD | 0.621 | 0.880 |
| AUDUSD~USDJPY | 0.481 | 0.450 |
| AUDUSD~XAUUSD | 0.345 | 0.658 |
| EURJPY~JP225 | 0.213 | 0.726 |
| EURJPY~NZDUSD | 0.405 | 0.557 |
| EURJPY~USDJPY | 0.548 | 0.876 |
| EURJPY~XAUUSD | 0.245 | 0.506 |
| JP225~NZDUSD | 0.196 | 0.628 |
| JP225~USDJPY | 0.189 | 0.706 |
| JP225~XAUUSD | 0.108 | 0.558 |
| NZDUSD~USDJPY | 0.466 | 0.381 |
| NZDUSD~XAUUSD | 0.332 | 0.656 |
| USDJPY~XAUUSD | 0.297 | 0.408 |

### B_asian_failed_breakout: N efectivo de apuestas = 5.58 de 7 activos

| par | same_day_share | same_direction_share |
|---|---|---|
| AUDJPY~AUDUSD | 0.299 | 0.825 |
| AUDJPY~EURJPY | 0.229 | 0.921 |
| AUDJPY~JP225 | 0.237 | 0.717 |
| AUDJPY~NZDUSD | 0.227 | 0.704 |
| AUDJPY~USDJPY | 0.274 | 0.759 |
| AUDJPY~XAUUSD | 0.107 | 0.658 |
| AUDUSD~EURJPY | 0.158 | 0.602 |
| AUDUSD~JP225 | 0.203 | 0.579 |
| AUDUSD~NZDUSD | 0.278 | 0.906 |
| AUDUSD~USDJPY | 0.258 | 0.452 |
| AUDUSD~XAUUSD | 0.105 | 0.694 |
| EURJPY~JP225 | 0.189 | 0.702 |
| EURJPY~NZDUSD | 0.157 | 0.550 |
| EURJPY~USDJPY | 0.248 | 0.876 |
| EURJPY~XAUUSD | 0.087 | 0.551 |
| JP225~NZDUSD | 0.187 | 0.562 |
| JP225~USDJPY | 0.268 | 0.649 |
| JP225~XAUUSD | 0.087 | 0.687 |
| NZDUSD~USDJPY | 0.223 | 0.406 |
| NZDUSD~XAUUSD | 0.085 | 0.615 |
| USDJPY~XAUUSD | 0.118 | 0.430 |

### C_tokyo_or_breakout: N efectivo de apuestas = 3.87 de 4 activos

| par | same_day_share | same_direction_share |
|---|---|---|
| AUDJPY~JP225 | 0.774 | 0.616 |
| AUDJPY~USDJPY | 0.857 | 0.571 |
| AUDJPY~XAUUSD | 0.474 | 0.476 |
| JP225~USDJPY | 0.873 | 0.578 |
| JP225~XAUUSD | 0.483 | 0.486 |
| USDJPY~XAUUSD | 0.550 | 0.387 |

### D_tokyo_or_failed_breakout: N efectivo de apuestas = 3.72 de 4 activos

| par | same_day_share | same_direction_share |
|---|---|---|
| AUDJPY~JP225 | 0.152 | 0.645 |
| AUDJPY~USDJPY | 0.203 | 0.773 |
| AUDJPY~XAUUSD | 0.105 | 0.545 |
| JP225~USDJPY | 0.141 | 0.529 |
| JP225~XAUUSD | 0.072 | 0.450 |
| USDJPY~XAUUSD | 0.096 | 0.373 |

### E_tokyo_breakout_vwap: N efectivo de apuestas = 2.49 de 3 activos

| par | same_day_share | same_direction_share |
|---|---|---|
| AUDJPY~JP225 | 0.168 | 0.853 |
| AUDJPY~USDJPY | 0.153 | 0.766 |
| JP225~USDJPY | 0.228 | 0.689 |

Señales del mismo día y misma dirección en pares JPY correlacionados NO son oportunidades independientes: el tamaño de muestra efectivo es el N efectivo, no la suma de operaciones.

## 12. Conclusión objetiva

**Ninguna combinación estrategia + activo mostró una ventaja estadística robusta** con los criterios definidos. No se recomienda operar ninguna con dinero real.

| strategy | symbol | verdict |
|---|---|---|
| A_asian_range_breakout | JP225 | SIN VENTAJA: se degrada fuera de muestra |
| A_asian_range_breakout | EURJPY | SIN VENTAJA: se degrada fuera de muestra |
| C_tokyo_or_breakout | USDJPY | SIN VENTAJA: se degrada fuera de muestra |
| E_tokyo_breakout_vwap | USDJPY | SIN VENTAJA: se degrada fuera de muestra |
| E_tokyo_breakout_vwap | JP225 | SIN VENTAJA: se degrada fuera de muestra |
| A_asian_range_breakout | USDJPY | SIN VENTAJA: se degrada fuera de muestra |
| D_tokyo_or_failed_breakout | USDJPY | SIN VENTAJA: se degrada fuera de muestra |
| E_tokyo_breakout_vwap | AUDJPY | SIN VENTAJA: se degrada fuera de muestra |
| A_asian_range_breakout | AUDJPY | SIN VENTAJA: se degrada fuera de muestra |
| A_asian_range_breakout | NZDUSD | FRÁGIL |
| A_asian_range_breakout | XAUUSD | FRÁGIL |
| C_tokyo_or_breakout | XAUUSD | FRÁGIL |
| A_asian_range_breakout | AUDUSD | FRÁGIL |
| D_tokyo_or_failed_breakout | AUDJPY | FRÁGIL |
| D_tokyo_or_failed_breakout | JP225 | FRÁGIL |
| C_tokyo_or_breakout | JP225 | SIN VENTAJA: se degrada fuera de muestra |
| D_tokyo_or_failed_breakout | XAUUSD | FRÁGIL |
| C_tokyo_or_breakout | AUDJPY | SIN VENTAJA: se degrada fuera de muestra |
| B_asian_failed_breakout | AUDUSD | FRÁGIL |
| B_asian_failed_breakout | EURJPY | FRÁGIL |
| B_asian_failed_breakout | XAUUSD | FRÁGIL |
| B_asian_failed_breakout | JP225 | FRÁGIL |
| B_asian_failed_breakout | AUDJPY | FRÁGIL |
| B_asian_failed_breakout | USDJPY | FRÁGIL |
| B_asian_failed_breakout | NZDUSD | FRÁGIL |


### Sesgos revisados
- Look-ahead: rangos y ATR sólo con barras cerradas; entrada en la barra siguiente; trailing aplica desde la barra siguiente; régimen de volatilidad con percentiles del pasado.
- Data mining / selección: se reporta la cantidad de configuraciones probadas, BH-FDR y Deflated Sharpe; la elección usa vecindarios, no el máximo.
- Overfitting / sensibilidad: heatmaps de parámetros (mediana sobre el resto) y vecinos positivos.
- Régimen: % del beneficio en un año y ventanas WF positivas (marca FRÁGIL).
- Survivorship: los símbolos se fijaron a priori (no se eligieron por desempeño). Un CFD de índice basado en futuros puede tener saltos de roll: ver outliers en data_quality.md.
- Intrabarra: SL primero ante ambigüedad; resultados con M5 son menos precisos que con M1.
