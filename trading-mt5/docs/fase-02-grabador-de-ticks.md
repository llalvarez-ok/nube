# Fase 2 (Etapa 0) — Grabador de ticks y mapa de costos

**Fecha:** 04/10/2026 · **Estado:** código escrito, **sin compilar todavía** (falta compilarlo en MetaEditor).

## Qué hace

`mql5/Services/ATS_TickRecorder.mq5` es un **servicio** de MT5: corre en segundo plano, sin gráfico y **sin operar**. Graba:

| Archivo (en `...\Common\Files\ATS\`) | Contenido |
|---|---|
| `ticks\<SÍMBOLO>\<AAAAMMDD>.bin` | Cada tick recibido: hora del servidor (ms), bid, ask, last, volumen, flags y la hora local en que el terminal lo leyó |
| `status\<AAAAMMDD>.csv` | Cada 10 s: ping al servidor, conexión, bid/ask/spread, ticks grabados y errores |
| `specs\<SÍMBOLO>_<AAAAMMDD>.csv` | Especificaciones del símbolo y de la cuenta (contrato, volumen mínimo, stops level, modo de ejecución, apalancamiento…). **No guarda número de cuenta ni nombre.** |
| `events.csv` | Inicio, fin y errores del servicio |

Ocupa del orden de decenas de MB por día para el oro. Si el servicio se reinicia, sigue agregando al archivo del día.

`research/ticks/analizar_costos.py` lee esos archivos y produce el **mapa de costo contra movimiento** (CVR por plazo y por hora, §9.4 del documento de la Fase 1).

## Instalación (en tu PC)

1. Abrí MT5 con la cuenta cent de Exness.
2. En **Observación del mercado**, fijate el nombre exacto del oro en tu cuenta (en cuentas cent de Exness suele ser `XAUUSDc`).
3. Menú **Archivo → Abrir carpeta de datos**. Entrá a `MQL5\Services` y copiá ahí `ATS_TickRecorder.mq5`.
4. Abrí **MetaEditor** (tecla F4), abrí el archivo y compilalo (tecla F7). **Si aparece algún error o advertencia, mandame el texto completo** de la pestaña "Errores".
5. En MT5, panel **Navegador → Servicios**: clic derecho sobre `ATS_TickRecorder` → **Agregar servicio**. En los parámetros poné el nombre exacto del símbolo en `InpSymbols` (podés agregar más separados por coma, p. ej. `XAUUSDc,EURUSDc`). Aceptá; el servicio arranca.
6. Verificá en la pestaña **Diario** (abajo) que aparezca `ATS_TickRecorder: START`. Después de un minuto, en `C:\Users\<tu usuario>\AppData\Roaming\MetaQuotes\Terminal\Common\Files\ATS\ticks\` tiene que haber un archivo `.bin` creciendo.

### Para que la grabación sirva

- **Dejalo corriendo al menos 5 días hábiles seguidos** (idealmente 2 semanas), cubriendo las sesiones de Asia, Londres y Nueva York.
- **Configurá Windows para que no suspenda la PC** ni apague el disco. MT5 tiene que quedar abierto y conectado.
- Cortes de luz o internet no rompen nada: quedan como huecos y se ven en `status`. Anotá si hubo alguno largo.
- El servicio no envía órdenes, así que no hay riesgo para la cuenta.

## Análisis (lo corro yo)

```
pip install -r requirements.txt
python -m research.ticks.analizar_costos --raiz <carpeta ATS> --simbolo XAUUSDc --salida reporte_costos.md
```

- `--slippage` y `--comision` (en unidades de precio) son **supuestos** hasta tener ejecución real. En la cuenta Standard Cent la comisión es 0 y el costo está en el spread.
- Tests: `python -m pytest research/tests`.

## Formato del archivo de ticks

Registros de 52 bytes, little-endian, sin encabezado:

| Campo | Tipo | Bytes |
|---|---|---|
| time_msc | int64 | 8 |
| bid | float64 | 8 |
| ask | float64 | 8 |
| last | float64 | 8 |
| volume_real | float64 | 8 |
| flags | uint32 | 4 |
| local_us | uint64 | 8 |

`local_us` es el reloj monotónico local en el momento en que el servicio leyó el tick, un poco después de que llegó (consulta cada 10 ms). Sirve para medir la regularidad de llegada. Para relacionarlo con la hora real se usa `status`, que registra el mismo reloj junto a la hora del servidor, GMT y local.
