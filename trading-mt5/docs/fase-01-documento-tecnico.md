# Fase 1 — Documento técnico de arquitectura y viabilidad

**Proyecto:** Adaptive Multi-Strategy Trading Engine (MT5)
**Versión del documento:** 1.0 — 04/10/2026
**Estado:** borrador para revisión. No hay código de producción todavía.

---

## Resumen ejecutivo (leé esto primero)

1. **El cuello de botella no es MQL5 ni la velocidad de cálculo. Son los costos y la calidad de ejecución del broker.** MQL5 calcula un vector de features en microsegundos; una orden de mercado tarda entre ~5 ms (VPS al lado del servidor del broker) y 200+ ms (PC hogareña), y a eso se le suma el procesamiento del broker.
2. **"Miles de operaciones por día" es técnicamente ejecutable en MT5, pero casi con seguridad no es económicamente viable** en Forex/CFDs retail con holding de segundos. El motivo es aritmético: en horizontes de segundos el movimiento esperado del precio es del mismo orden que el costo de ida y vuelta (spread + comisión + slippage). Con costo de 1 pip y TP=SL=2 pips, necesitás **75 % de aciertos** solo para empatar (ver §9).
3. **Hay edges de alta frecuencia que en MT5 retail directamente no existen para vos:** arbitraje de latencia, posición en la cola del libro, market making real. Varios brokers los prohíben en sus términos y anulan ganancias. La "Strategy J" del prompt debe reformularse (ver §12.4).
4. **Mi recomendación:** no empezar construyendo el sistema completo. Empezar por una **Fase 0 de medición** (dos a tres semanas): registrar ticks, spreads y ejecución real con órdenes de lote mínimo, y calcular el **ratio costo/volatilidad por horizonte** (§9.4). Ese número dice, antes de escribir una sola estrategia, en qué horizonte e instrumento hay alguna chance de operar. La frecuencia operativa sale de ese análisis; no es algo que se elige.
5. **Principio rector de la arquitectura — asimetría de autonomía:** el sistema puede volverse **más conservador** solo (reducir riesgo, pausar, bloquear, detenerse) pero **nunca más agresivo** solo (aumentar riesgo, activar estrategias, cambiar parámetros). Toda acción que aumenta riesgo pasa por validación y aprobación humana.

---

## Índice

1. [Viabilidad de cientos/miles de operaciones diarias en MT5](#1-viabilidad-de-cientosmiles-de-operaciones-diarias-en-mt5)
2. [Limitaciones de MT5/MQL5](#2-limitaciones-de-mt5mql5)
3. [Qué vive dentro de MT5](#3-qué-vive-dentro-de-mt5)
4. [Qué vive fuera de MT5](#4-qué-vive-fuera-de-mt5)
5. [Arquitectura completa](#5-arquitectura-completa)
6. [Flujo de datos](#6-flujo-de-datos)
7. [Flujo de decisión](#7-flujo-de-decisión)
8. [Flujo de ejecución](#8-flujo-de-ejecución)
9. [Modelo de costos](#9-modelo-de-costos)
10. [Modelo de expectativa neta](#10-modelo-de-expectativa-neta)
11. [Market Regime Engine](#11-market-regime-engine)
12. [Strategy Selector y biblioteca de estrategias](#12-strategy-selector-y-biblioteca-de-estrategias)
13. [Risk Engine](#13-risk-engine)
14. [Learning Engine](#14-learning-engine)
15. [Research Engine](#15-research-engine)
16. [Sistema de versionado](#16-sistema-de-versionado)
17. [Sistema de validación](#17-sistema-de-validación)
18. [Sistema de seguridad](#18-sistema-de-seguridad)
19. [Estructura de almacenamiento](#19-estructura-de-almacenamiento)
20. [MVP recomendado](#20-mvp-recomendado)
21. [Riesgos técnicos](#21-riesgos-técnicos)
22. [Riesgos financieros](#22-riesgos-financieros)
23. [Supuestos a comprobar experimentalmente](#23-supuestos-a-comprobar-experimentalmente)
24. [Datos necesarios antes de comenzar](#24-datos-necesarios-antes-de-comenzar)
25. [Preguntas que necesito que respondas](#25-preguntas-que-necesito-que-respondas)

---

## 1. Viabilidad de cientos/miles de operaciones diarias en MT5

Hay que separar tres preguntas que el prompt mezcla.

### 1.1 ¿Puede MT5 *enviar* cientos o miles de órdenes por día?

**Sí.** 1.000 operaciones en una sesión de 8 horas son ~1 operación cada 29 segundos (2 órdenes: apertura y cierre). Una orden de mercado con `OrderSend` tarda típicamente:

| Ubicación del terminal | Ping al servidor | Ida y vuelta de una orden de mercado (orden de magnitud) |
|---|---|---|
| VPS en el mismo datacenter que el servidor del broker (p. ej. LD4, NY4) | 0,5–3 ms | 5–50 ms |
| VPS en la misma región | 5–30 ms | 20–100 ms |
| PC hogareña en Argentina → servidor en Londres/NY | 150–250 ms | 200–500 ms+ |

Los números exactos dependen del broker y hay que medirlos (§23). Pero aun en el peor caso, la capacidad de envío alcanza para miles de órdenes por día. **El límite técnico no es la cantidad; es la latencia relativa a la duración de la oportunidad.**

### 1.2 ¿Puede MT5 *capturar oportunidades que duran segundos*?

**Depende de la naturaleza de la oportunidad:**

- **Oportunidades que duran < 1 segundo** (desequilibrios del libro, desfasajes entre feeds, reacción a un print): **no**. Ahí compiten firmas con colocation, FPGA y acceso directo al exchange. Con 200 ms de latencia desde Argentina llegás tarde siempre. Desde un VPS a 2 ms seguís llegando tarde respecto de quien opera a microsegundos, y además el feed de MT5 ya viene filtrado/agregado por el broker.
- **Oportunidades de 5 a 60 segundos** (micro-momentum, reversión de un spike): **técnicamente capturables desde un VPS cercano**, pero el costo de ejecución es grande relativo al movimiento (ver 1.3).
- **Oportunidades de 1 a 15 minutos**: la latencia deja de importar mucho; el problema pasa a ser exclusivamente si existe edge neto.

### 1.3 ¿Es *económicamente* viable?

Este es el punto crítico. Para un horizonte de holding *h*, la pregunta es cuánto se mueve el precio en *h* comparado con lo que cuesta entrar y salir:

```
Costo ida y vuelta (EURUSD, cuenta raw/ECN buena):
  spread medio 0,1–0,3 pips + comisión ~0,6–0,7 pips + slippage 0–0,3 pips
  ≈ 0,7 – 1,3 pips

Movimiento típico del mid de EURUSD (desvío estándar, a medir):
  en 10 s  → del orden de 0,3–1 pip
  en 60 s  → del orden de 1–2,5 pips
  en 5 min → del orden de 2,5–6 pips
```

(Los rangos de movimiento son órdenes de magnitud orientativos que cambian mucho por sesión y por día; la Fase 0 los mide con datos reales.)

**Conclusión:** a 10 segundos, el costo es igual o mayor que el movimiento típico. Para ganar ahí necesitás una capacidad predictiva que, en la práctica, los participantes retail no tienen sobre un feed de MT5. A 5 minutos, el costo pasa a ser una fracción manejable del movimiento.

### 1.4 Veredicto de viabilidad

| Objetivo | Veredicto |
|---|---|
| Miles de operaciones/día, holding de segundos, un instrumento FX retail | **No viable.** Premisa económicamente falsa salvo evidencia contraria medida. No diseño la arquitectura sobre esto. |
| Cientos/día, holding 10–60 s, varios instrumentos, VPS cercano | **Improbable pero testeable.** Solo en instrumentos con costo/volatilidad muy bajo y en franjas horarias específicas. Requiere la Fase 0. |
| Decenas a ~200/día, holding 30 s–10 min, varios instrumentos | **Plausible como hipótesis de investigación.** Es donde recomiendo centrar el MVP. |
| Frecuencia como consecuencia del edge (lo que pide el prompt) | **Correcto, y es lo que implementa la arquitectura.** No hay ningún objetivo de cantidad en el código. |

**Respuesta a la regla 49:** "¿Existe suficiente edge después de spread, comisión y slippage para hacer miles de operaciones?" — Hoy no hay evidencia de que exista, y la aritmética de costos sugiere que no en horizontes de segundos. La arquitectura soporta alta frecuencia si los datos la justifican, pero no la presupone.

### 1.5 Restricciones no técnicas que pueden matar el proyecto

- **Términos del broker.** Muchos brokers prohíben explícitamente: scalping de menos de N segundos/minutos, "tick scalping", arbitraje de latencia, explotación de precios desfasados. Pueden anular ganancias o cerrar la cuenta *después* de que ganaste. **Hay que leer los términos antes de elegir broker** (§24).
- **Broker market maker (B-book).** Si el broker es contraparte de tus operaciones, un scalper consistentemente ganador es un problema para él: puede introducir "virtual dealer" (retrasos y slippage asimétrico), mover a la cuenta a otro grupo de ejecución o limitar volumen. Preferir ejecución STP/ECN (A-book) y **medir la asimetría del slippage** (positivo vs. negativo) como indicador.
- **Cuentas demo.** Las demo suelen ejecutar idealmente (sin slippage real, sin rechazos). **Resultados en demo no validan la ejecución.**
- **Regulación/apalancamiento.** Según jurisdicción del broker, el apalancamiento retail está limitado (p. ej. 1:30 en majors bajo ESMA). Esto limita el tamaño con capital chico.

---

## 2. Limitaciones de MT5/MQL5

### 2.1 Recepción de ticks

| Limitación | Impacto | Mitigación |
|---|---|---|
| **El evento `NewTick` no se encola por tick.** Si `OnTick()` todavía está procesando, los ticks nuevos que llegan no generan eventos adicionales (solo puede haber un `NewTick` pendiente en la cola). | Si el procesamiento es lento, se "saltean" ticks. El tester, en cambio, llama a `OnTick` para cada tick: el backtest ve ticks que en vivo no habrías visto. | `OnTick` mínimo. Recuperar los ticks intermedios con `CopyTicks(symbol, ticks, COPY_TICKS_ALL, desde_ultimo_msc)` en cada llamada. Medir tiempo de `OnTick` con `GetMicrosecondCount()`. |
| **El feed lo produce el broker**, no el mercado. En FX/CFDs es un precio del broker, filtrado y/o agregado. | La "microestructura" disponible es la del feed del broker, no la del mercado interbancario. Patrones de tick pueden ser artefactos del broker. | Tratar todo patrón microestructural como específico del broker. Comparar con un segundo feed si es posible. |
| **`OnTick` se dispara solo para el símbolo del gráfico.** | Multi-símbolo no recibe eventos de los otros símbolos. | `OnTimer` (milisegundos) + `CopyTicks` por símbolo, o `OnBookEvent` si hay DOM, o un EA por símbolo coordinado. |
| **Timestamps:** `MqlTick.time_msc` está en milisegundos y en hora del servidor del broker. | No hay timestamp del exchange ni resolución sub-ms. La latencia "mercado → terminal" no se puede medir exactamente sin sincronizar relojes. | Medir llegada local con `GetMicrosecondCount()` y estimar offset/deriva respecto de `time_msc`. Usar `TERMINAL_PING_LAST` como referencia. |
| **`EventSetMillisecondTimer`** tiene resolución práctica de ~10–16 ms en Windows. | Timers no sirven para precisión sub-10 ms. | No depender de timers finos; la decisión se dispara por tick. |

### 2.2 Profundidad de mercado (DOM)

- `MarketBookAdd` / `OnBookEvent` / `MarketBookGet` existen, pero **en FX/CFDs la mayoría de los brokers no da libro, o da uno sintético** (agregación de cotizaciones de proveedores de liquidez, sin cola real ni ejecución garantizada a esos niveles).
- En instrumentos de **bolsa** accesibles por MT5 (según broker: algunos futuros, acciones) el DOM puede ser real, junto con `TICK_FLAG_BUY/SELL` y volumen real.
- **Decisión de diseño:** el DOM es un input *opcional*. El sistema debe funcionar sin él, y ninguna estrategia del MVP puede depender de él hasta verificar que es real en el broker elegido.

### 2.3 Ejecución

| Elemento | Detalle relevante |
|---|---|
| Modos de ejecución (`SYMBOL_TRADE_EXEMODE`) | Instant (con requotes), Request, Market (precio al momento de ejecutar, slippage), Exchange. Para scalping se quiere **Market** con broker STP/ECN. Instant genera requotes que destruyen estrategias de segundos. |
| Filling (`SYMBOL_FILLING_MODE`) | FOK / IOC / Return (y BOC en builds recientes para órdenes límite). Hay que elegir según lo que el símbolo admite; un filling inválido devuelve `TRADE_RETCODE_INVALID_FILL`. |
| `SYMBOL_TRADE_STOPS_LEVEL` | Distancia mínima de SL/TP al precio. Si es mayor que el stop que querés (frecuente en scalping), no podés poner el SL real en el servidor a esa distancia. |
| `SYMBOL_TRADE_FREEZE_LEVEL` | Cerca del precio no se pueden modificar/cerrar órdenes pendientes ni SL/TP. |
| Rechazos/requotes | `REQUOTE`, `PRICE_CHANGED`, `PRICE_OFF`, `REJECT`, `TOO_MANY_REQUESTS`, `TIMEOUT`, `CONNECTION`, etc. Cada uno requiere un manejo distinto (§8). |
| Límites de cuenta | `ACCOUNT_LIMIT_ORDERS`, `SYMBOL_VOLUME_LIMIT`, límites de frecuencia del servidor (no documentados, se descubren con `TOO_MANY_REQUESTS`). |
| `OrderSend` vs `OrderSendAsync` | Síncrono: bloquea hasta respuesta (simple, mide latencia directamente). Asíncrono: no bloquea; el resultado llega por `OnTradeTransaction`. Async agrega complejidad de estado; empezar síncrono, medir, y migrar solo si el bloqueo tiene costo medible. |
| Hedging vs netting (`ACCOUNT_MARGIN_MODE`) | Cambia cómo se gestionan posiciones (en netting una orden opuesta reduce la posición). El Position Manager debe soportar ambos o rechazar el que no soporta. |

### 2.4 Strategy Tester

El tester de MT5 es útil como **test de integración del EA**, pero **insuficiente como herramienta de validación para horizontes de segundos**:

- "Cada tick basado en ticks reales" usa la historia de ticks guardada por el broker, que puede diferir de lo que recibiste en vivo (filtrado distinto, huecos).
- Ejecuta al precio del tick (o con un retraso configurable fijo/aleatorio). **No modela slippage condicional a volatilidad, rechazos, requotes, ejecuciones parciales, ni liquidez finita.**
- No reproduce el salteo de ticks de `OnTick` en vivo.
- La optimización genética del tester invita al overfitting si no se controla el número de pruebas.

**Consecuencia:** la investigación se hace en un **simulador propio en Python** con modelos de costo/latencia **medidos** (§15), y el tester de MT5 se usa para verificar que el código MQL5 hace lo mismo que el simulador (paridad).

### 2.5 Lenguaje y entorno

- MQL5 es compilado y rápido; el cálculo de features no es cuello de botella si se usa estado incremental (buffers circulares, EWMA) y no recálculos completos.
- Un EA corre en **un solo hilo** por gráfico. Operaciones pesadas (escritura masiva a disco, cálculos grandes) bloquean la decisión. Mitigación: buffers en memoria, escritura por lotes en `OnTimer`, o tareas separadas en un **Service** de MT5.
- **SQLite nativo** (`DatabaseOpen`, `DatabasePrepare`, transacciones): permite registrar decisiones sin DLLs.
- **ONNX nativo** (`OnnxCreate`, `OnnxRun`): un modelo entrenado en Python puede ejecutarse **dentro** de MT5, sin dependencia externa en la ruta crítica.
- Sockets: MQL5 tiene sockets cliente (`SocketCreate`/`SocketConnect`), no servidor. ZeroMQ y similares requieren DLLs (habilitar DLLs amplía la superficie de riesgo).
- El paquete `MetaTrader5` de Python se comunica con un terminal local, solo en Windows. Útil para **bajar historia** en investigación; **no** para la ruta de ejecución.

---

## 3. Qué vive dentro de MT5

**Todo lo que participa en una decisión de trading en vivo, o en la protección del capital, vive dentro de MT5.** Nada de esto puede depender de un proceso externo.

| Componente | Motivo |
|---|---|
| Market Data Engine (ticks, spreads, specs de símbolo) | Fuente primaria; sin latencia adicional. |
| Tick Recorder (como Service separado) | Captura lo que efectivamente llegó al terminal, con timestamp local. |
| Feature Engine (incremental) | Ruta crítica. |
| Market Regime Engine (clasificación) | Ruta crítica; usa umbrales calibrados offline. |
| Strategies (lógica de señal de versiones `APPROVED`) | Ruta crítica. Modelos ML vía ONNX si los hay. |
| Cost Engine en vivo (spread actual, estimación de slippage/latencia con tablas calibradas) | Necesario para el filtro de edge neto. |
| Expectancy Engine en vivo (consulta de tablas de expectativa por estrategia/régimen) | Ruta crítica. |
| Strategy Selector | Ruta crítica. |
| No-Trade Engine | Debe tener autoridad absoluta, sin dependencias. |
| Risk Engine + Position Sizing | Protección del capital. |
| Execution Engine | Ruta crítica. |
| Position Manager + Time Exit | Ruta crítica. |
| Emergency Risk Controller | Debe funcionar aunque todo lo demás falle. |
| Decision Logger (escritura local) | Debe registrar aunque el exterior no exista. |
| Dashboard | Visualización local en el gráfico. |
| Config Loader (lee configuración aprobada, valida, nunca escribe estrategia) | Única puerta de entrada de cambios. |

## 4. Qué vive fuera de MT5

**Todo lo que es investigación, aprendizaje y validación vive fuera (Python), y solo produce artefactos que un humano aprueba.**

| Componente | Motivo |
|---|---|
| Ingesta y limpieza de datos (ticks, logs) → Parquet | Volumen y herramientas de análisis. |
| Simulador de tick-replay con modelo de costos/latencia/rechazos medido | El tester de MT5 no alcanza (§2.4). |
| Feature library espejo (misma definición que MQL5) + tests de paridad | Investigación sobre las mismas features que corren en vivo. |
| Calibración del Regime Engine (umbrales, percentiles por sesión) | Cálculo offline; resultado = parámetros versionados. |
| Learning Engine (estadísticas, detección de patrones) | No necesita tiempo real. |
| Hypothesis Engine + registro de experimentos | Trazabilidad y control de pruebas múltiples. |
| Backtest / OOS / Walk-forward / Monte Carlo / Stress | Cómputo pesado. |
| Entrenamiento de modelos ML (y export a ONNX) | Librerías de ML. |
| Strategy Registry (máquina de estados de versiones) | Gobierno de despliegue. |
| Reportes de validación y auditoría automática | Evidencia para aprobar o rechazar. |

### 4.1 Comunicación MT5 ↔ Python

```
MT5 ──(escribe)──► SQLite (WAL) + archivos binarios de ticks ──(lee, solo lectura)──► Python
Python ──(escribe)──► /candidates/*.json  (NUNCA leído por MT5)
Humano ──(aprueba)──► /approved/<strategy>@<version>.json + hash en registry
MT5 ──(lee al iniciar o por comando, solo si está flat)──► /approved/
```

Reglas:

1. **MT5 nunca espera a Python.** No hay llamadas síncronas, sockets ni pipes en la ruta crítica.
2. **Python nunca escribe en lo que MT5 lee automáticamente.** La promoción a `/approved/` es un acto humano explícito (en la práctica: un script de promoción que exige confirmación y registra quién/cuándo).
3. **El Config Loader valida todo:** esquema, rangos de parámetros dentro de límites duros compilados en el EA, hash coincidente con el registro, estado `APPROVED`. Si algo falla → mantiene la configuración anterior y registra el evento. Nunca arranca con config parcial.
4. **Recarga solo con el sistema sin posiciones** de la estrategia afectada.
5. **Fallback (§37 del prompt):** si Python no existe, MT5 sigue operando con la última configuración aprobada. Lo único que se pierde es la investigación.

---

## 5. Arquitectura completa

### 5.1 Vista de dos mundos

```
╔═══════════════════════════ LIVE (MT5) ════════════════════════════╗
║                                                                   ║
║  Market Data ─► Features ─► Regime ─► Strategies (señales)        ║
║                                          │                        ║
║                     Cost Engine ─► Expectancy ─► Selector         ║
║                                                     │             ║
║           Emergency ◄──► No-Trade Engine ◄──► Risk Engine         ║
║              │                                      │             ║
║              └────────► Execution ─► Position Mgr ─► Result       ║
║                                                     │             ║
║                                              Decision Logger      ║
╚════════════════════════════════════════════════│══════════════════╝
                                    (solo datos, unidireccional)
╔══════════════════════ RESEARCH (Python) ═══════▼══════════════════╗
║  Ingesta ─► Learning (estadística) ─► Hypothesis ─► Simulador     ║
║   ─► IS / OOS ─► Walk-forward ─► Monte Carlo ─► Stress            ║
║   ─► Auditoría automática ─► Candidate ─► Registry                ║
╚════════════════════════════════════════════════│══════════════════╝
                                                 ▼
                                   APROBACIÓN HUMANA (gate)
                                                 ▼
                          /approved  ─► Config Loader (MT5)
```

### 5.2 Módulos MQL5 (mapeo a la estructura de carpetas pedida)

```
MQL5/
├── Experts/ATS/ATS.mq5              # EA delgado: solo cablea módulos y eventos
├── Services/ATS_TickRecorder.mq5    # Service independiente: graba ticks
└── Include/ATS/
    ├── Core/        # tipos comunes, Clock, Result/Error, constantes, límites duros
    ├── Data/        # SymbolSpec (SymbolInfo*), sesiones, calendario económico
    ├── Ticks/       # TickBuffer circular, recuperación con CopyTicks, calidad de datos
    ├── Features/    # features incrementales (EWMA, ventanas temporales)
    ├── Regime/      # clasificador multi-eje + confianza + histéresis
    ├── Strategies/  # IStrategy + implementaciones (una clase por estrategia)
    ├── Signals/     # Signal (dirección, score, entrada/stop/target sugeridos)
    ├── Expectancy/  # tablas de expectativa neta por (estrategia, versión, celda de régimen)
    ├── Costs/       # SpreadEngine, SlippageModel, LatencyModel (en vivo)
    ├── Risk/        # RiskEngine, PositionSizer, NoTradeEngine, EmergencyController
    ├── Execution/   # OrderRouter, validaciones pre-trade, manejo de retcodes
    ├── Positions/   # PositionManager, TimeExit, trailing, MFE/MAE
    ├── Statistics/  # estadísticas en vivo (rolling), CUSUM de deterioro de edge
    ├── Logging/     # DecisionLogger (SQLite, buffer + batch)
    ├── Config/      # ConfigLoader + validación + hash
    ├── Dashboard/   # panel en el gráfico
    └── Testing/     # tests unitarios en script MQL5, fixtures de ticks
```

Las carpetas `/Learning`, `/Research` y `/Optimization` del prompt **no existen en MQL5 a propósito**: viven en Python. Que no haya código de aprendizaje en el EA es la garantía física de que el aprendizaje no puede modificar producción.

### 5.3 Proyecto Python

```
research/
├── ingest/        # lectura de SQLite/ticks de MT5 → Parquet particionado
├── features/      # espejo de Include/ATS/Features + tests de paridad
├── regime/        # calibración de umbrales/percentiles
├── costs/         # ajuste de distribuciones de spread/slippage/latencia
├── sim/           # simulador de tick-replay (latencia, slippage, rechazos, stops level)
├── strategies/    # prototipos de estrategias (misma lógica que MQL5)
├── validation/    # IS/OOS, walk-forward, Monte Carlo, stress, auditoría
├── learning/      # estadísticas por celda, detección de patrones
├── hypotheses/    # registro de hipótesis y experimentos (cada prueba cuenta)
├── registry/      # strategy registry + promoción con confirmación humana
└── reports/       # reportes de validación reproducibles
```

### 5.4 Interfaz de estrategia (contrato)

Cada estrategia implementa el mismo contrato, en MQL5 y en Python:

```
IStrategy
  id(), version(), params_hash()
  allowed_regimes(), forbidden_regimes()
  on_features(FeatureVector f, RegimeState r) -> Signal | NONE
  exit_rule(Position p, FeatureVector f, RegimeState r) -> ExitDecision | HOLD
  expected_holding_ms()
  max_holding_ms()
```

La estrategia **no** decide tamaño, **no** envía órdenes y **no** conoce el estado de la cuenta. Solo propone. Eso permite que el Risk Engine y el No-Trade Engine sean los mismos para todas.

---

## 6. Flujo de datos

```
Servidor broker
   │ ticks (bid, ask, last, volume, flags, time_msc)
   ▼
[TickRecorder Service] ── binario diario por símbolo ──► disco ──► Python (Parquet)
   │
[EA] OnTick / OnTimer
   │ CopyTicks desde último time_msc procesado (recupera ticks salteados)
   ▼
TickBuffer (circular, por símbolo) + chequeo de calidad:
   - tick duplicado / desordenado / bid>=ask / salto absurdo / feed congelado
   ▼
Feature Engine (incremental, ventanas por tiempo: 1s, 5s, 30s, 2m, 10m)
   ▼
FeatureVector (snapshot inmutable con id) ──► Regime ──► Strategies ...
   │
   └─► Decision Logger guarda el snapshot SOLO cuando hay una señal o un evento
       (no por cada tick: el detalle por tick ya está en el TickRecorder)
```

### 6.1 Features iniciales (todas calculables tick a tick)

| Grupo | Features |
|---|---|
| Precio | mid, retorno del mid en ventanas de 1/5/30/120 s |
| Spread | spread actual, percentil del spread vs. distribución de la misma sesión, z-score, tasa de cambio, tiempo desde último ensanchamiento |
| Actividad | ticks por segundo (EWMA), tiempo desde el último tick (detección de feed congelado) |
| Volatilidad | volatilidad realizada por ventana (muestreada por tiempo, no por tick, para reducir ruido de microestructura), rango de la ventana |
| Dirección | velocidad (Δmid/Δt), aceleración, desequilibrio de upticks/downticks, efficiency ratio (|movimiento neto| / longitud del camino) |
| Estructura | distancia al máximo/mínimo reciente, autocorrelación de retornos de corto plazo (negativa ⇒ rebote/reversión) |
| Exchange (si hay) | volumen real, agresor (`TICK_FLAG_BUY/SELL`), desequilibrio del libro |
| Contexto | sesión, minutos a/desde noticias (calendario nativo de MT5), ATR M1/M5, tendencia M15/H1 |
| Ejecución | ping actual, slippage reciente, tasa de rechazo reciente |

**Advertencia:** cada feature nueva aumenta el espacio de búsqueda y el riesgo de overfitting. El MVP debería arrancar con ~10–15 features.

---

## 7. Flujo de decisión

```
FeatureVector + RegimeState
        │
        ▼
[1] Emergency Controller: ¿estado NORMAL o DEGRADED? ── no ─► FIN (sin entradas nuevas)
        │
        ▼
[2] Data Quality: ¿feed sano, ticks recientes, spread válido? ── no ─► NO_TRADE(DATA)
        │
        ▼
[3] Regime: ¿confianza ≥ mínimo? ¿régimen operable? ── no ─► NO_TRADE(REGIME)
        │
        ▼
[4] Strategies: cada estrategia APPROVED y permitida en este régimen evalúa → señales
        │ (si no hay señales → FIN, se registra solo en estadísticas agregadas)
        ▼
[5] Cost Engine: costo esperado de ida y vuelta para cada señal (spread actual,
    slippage esperado condicional, comisión, costo por latencia)
        ▼
[6] Expectancy: E_net y su cota inferior (LCB) para cada señal
        ▼
[7] Selector: elige la mejor señal con LCB > umbral; "NO TRADE" siempre compite con E = 0
        │ (todas ≤ 0 → NO_TRADE(EDGE), se registra la señal rechazada)
        ▼
[8] Risk Engine: tamaño, límites de exposición/correlación/pérdida diaria
        │ (tamaño < volumen mínimo → NO_TRADE(SIZE): nunca redondear hacia arriba)
        ▼
[9] No-Trade Engine: veto final con todas las condiciones (§12.3) ── veto ─► NO_TRADE(motivo)
        ▼
[10] Execution Engine
```

**Punto clave:** las señales **rechazadas** se registran con su motivo y luego se les calcula el resultado contrafáctico en investigación. Sin eso no se puede saber si un filtro agrega valor o solo reduce la muestra. Es una de las fuentes de aprendizaje más valiosas y la más fácil de olvidar.

---

## 8. Flujo de ejecución

```
Decisión aprobada (con id de decisión)
   ▼
Validaciones pre-trade:
   - TERMINAL_TRADE_ALLOWED, MQL_TRADE_ALLOWED, ACCOUNT_TRADE_ALLOWED
   - SYMBOL_TRADE_MODE (full / close-only / disabled), sesión de trading abierta
   - volumen normalizado: múltiplo de SYMBOL_VOLUME_STEP, entre MIN y MAX, bajo LIMIT
   - precios normalizados a SYMBOL_TRADE_TICK_SIZE / digits
   - SL/TP respetan STOPS_LEVEL; si no, ver "stops virtuales" abajo
   - filling mode compatible con SYMBOL_FILLING_MODE
   - margen suficiente (OrderCalcMargin / OrderCheck)
   ▼
t0 = GetMicrosecondCount();  mid_decision = mid al momento de decidir
OrderSend(request, result)    (síncrono en el MVP)
t1 = GetMicrosecondCount()
   ▼
Manejo de retcode:
   DONE / DONE_PARTIAL ─► registrar fill (precio, volumen, deal), latencia t1-t0
   REQUOTE / PRICE_CHANGED / PRICE_OFF ─► recalcular E_net con precio nuevo;
        reintentar como máximo 1 vez SOLO si el edge sigue siendo positivo
   REJECT / TIMEOUT / CONNECTION / TOO_MANY_REQUESTS ─► no reintentar a ciegas;
        contador de errores → Emergency Controller
   INVALID_* / NO_MONEY / MARKET_CLOSED / TRADE_DISABLED ─► error de lógica o
        de estado: registrar, bloquear la estrategia/símbolo, alertar
   TIMEOUT con estado desconocido ─► reconciliar contra PositionsTotal/HistoryDeals
        ANTES de cualquier otra acción (nunca duplicar una orden por no saber si entró)
   ▼
Position Manager:
   - SL "de catástrofe" en el servidor SIEMPRE (protege si el terminal muere)
   - si el stop operativo es más chico que STOPS_LEVEL: stop virtual gestionado
     por el EA + SL de catástrofe más amplio en el servidor (documentar el riesgo)
   - Time Exit, trailing, salida por cambio de régimen o pérdida de momentum
   - registra MFE/MAE tick a tick mientras la posición vive
   ▼
Cierre: misma secuencia de validación, medición de latencia y slippage
   ▼
Resultado: HistoryDealGet* → comisión real, swap, precio real; reconciliación
```

### 8.1 Medición de latencia

```
t_tick_server   = tick.time_msc               (reloj del broker)
t_tick_local    = GetMicrosecondCount() al entrar a OnTick
t_decision      = al terminar de decidir
t_send / t_ack  = antes/después de OrderSend
t_deal_server   = DEAL_TIME_MSC del deal
```

- Latencia interna (local → decisión): medible exactamente.
- Latencia de orden (send → ack): medible exactamente.
- Latencia feed (servidor → local): solo estimable (ping/2 + offset de relojes con deriva). Se registra como estimación, no como dato.

### 8.2 Reconciliación

Cada N segundos y después de todo error: comparar el estado interno de posiciones con `PositionsTotal()`/`PositionGet*`. Cualquier discrepancia → `HALT_NEW` y alerta. Un sistema que no sabe qué posiciones tiene no puede seguir operando.

---

## 9. Modelo de costos

### 9.1 Definición: implementation shortfall respecto del mid

Todos los costos se miden contra el **mid en el momento de la decisión**, que es el precio "teórico" sobre el que la estrategia estimó su edge.

```
Para una compra:
  costo_entrada = (precio_fill_entrada − mid_decisión_entrada)
                = medio spread + slippage_entrada + deriva por latencia
  costo_salida  = (mid_decisión_salida − precio_fill_salida)
                = medio spread + slippage_salida + deriva por latencia

COSTO_TOTAL = costo_entrada + costo_salida + comisión_ida_y_vuelta + swap + otros

NET P&L = GROSS P&L(mid a mid) − COSTO_TOTAL
```

Separar "medio spread", "slippage" y "deriva por latencia" permite saber **qué** está matando una estrategia.

### 9.2 Componentes

| Componente | Cómo se estima en vivo | Cómo se calibra |
|---|---|---|
| Spread | Spread actual (conocido) para entrada; para salida, distribución esperada del spread en la ventana de holding | Distribución por símbolo × sesión × hora × régimen de volatilidad × cercanía a noticias/rollover |
| Comisión | Tabla del broker (por lote o por valor nocional) verificada contra `DEAL_COMMISSION` real | Comparación automática esperado vs. real en cada trade |
| Slippage | Cuantil del modelo condicional (P50 para expectativa, P90 para stress) | Distribución empírica por símbolo × estrategia × dirección × volatilidad × hora × tipo de salida (TP, SL, time exit) |
| Latencia | Ping actual + latencia de orden reciente | Distribución medida; se convierte a costo con la volatilidad de corto plazo (deriva esperada ≈ f(σ por ms × latencia)) |
| Stop-out | Slippage en stops es mayor que en entradas (los stops se disparan con movimiento en contra) | Se modela aparte; nunca se usa el slippage medio de entradas para los stops |

**Al inicio no hay datos de slippage propios.** Se arranca con supuestos conservadores (p. ej. 0,5 pip por lado en majors) marcados como `ASSUMED`, y se reemplazan por valores `MEASURED` a medida que llega la ejecución real. El sistema debe mostrar cuánto de su modelo de costos es todavía supuesto.

### 9.3 Movimiento mínimo rentable

```
MPM = spread_esperado_rt + comisión_rt + slippage_esperado_rt
      + costo_latencia + margen_estadístico

margen_estadístico = k · σ(costo)     (k ≈ 1–2: cubre la variabilidad del costo)
```

Si el movimiento esperado a favor (target × probabilidad, ver §10) no supera MPM → `NO_TRADE(COST)`.

### 9.4 Métrica de viabilidad por horizonte: ratio costo/volatilidad

```
CVR(h) = COSTO_TOTAL_rt / σ(Δmid en horizonte h)
```

Interpretación orientativa (a confirmar con datos):

| CVR(h) | Lectura |
|---|---|
| > 1 | El costo supera el movimiento típico. Operar a ese horizonte requiere una capacidad predictiva irreal. Descartar. |
| 0,5 – 1 | Muy difícil. Solo con señales excepcionales. |
| 0,2 – 0,5 | Difícil pero investigable. |
| < 0,2 | Los costos son una fracción manejable. Horizonte razonable para buscar edge. |

**Este es el primer entregable de la Fase 0.** Por símbolo, sesión y hora: CVR para h = 5 s, 15 s, 30 s, 60 s, 2 min, 5 min, 15 min. Ese mapa determina dónde tiene sentido buscar.

### 9.5 Ejemplo: por qué los segundos son tan difíciles

Con TP = SL = G (simétrico) y costo total C por operación:

```
ganancia neta = G − C       pérdida neta = G + C
win rate de empate p* = (G + C) / (2G)
```

| G (pips) | C = 1,0 pip | C = 0,6 pip |
|---|---|---|
| 1,5 | 83,3 % | 70,0 % |
| 2 | 75,0 % | 65,0 % |
| 3 | 66,7 % | 60,0 % |
| 5 | 60,0 % | 56,0 % |
| 10 | 55,0 % | 53,0 % |

En horizontes de segundos, G es necesariamente chico, y p* se va a valores que ninguna señal sobre un feed retail sostiene. **Respuesta a "quiero ganar centavos":** el problema no es que la ganancia sea chica; es que el costo es fijo por operación y no se achica con el target.

### 9.6 Costo en unidades de riesgo

Expresado en R (R = distancia al stop): `costo_en_R = C / distancia_stop`. Con stop de 3 pips y C = 0,9 pip, **cada operación cuesta 0,3 R antes de empezar**. Una expectativa bruta de +0,3 R por trade sería excepcional; acá es el umbral de empate.

Con frecuencia alta el efecto se acumula: 500 operaciones/día × 0,3 R = 150 R de costos diarios que la señal tiene que superar.

---

## 10. Modelo de expectativa neta

### 10.1 Definición

Por señal, en unidades de R:

```
E_net = p · W_net − (1 − p) · L_net − (costos no incluidos en W/L)

donde:
  p      = probabilidad calibrada de alcanzar el target antes del stop/time-exit
  W_net  = ganancia media neta cuando gana (ya descontados costos)
  L_net  = pérdida media neta cuando pierde (incluye slippage de stop)
```

Con time exit hay un tercer desenlace (salida por tiempo con resultado intermedio), así que en la práctica:

```
E_net = Σ_desenlaces P(desenlace) · resultado_neto_medio(desenlace)
```

### 10.2 De dónde salen los números

No se confía en la estimación puntual. Para cada combinación (estrategia, versión, celda de régimen) se mantiene:

- n (cantidad de trades, separando backtest, paper y live — **nunca se mezclan**)
- media y desvío de R neto
- **cota inferior de confianza (LCB)** de la media
- **shrinkage bayesiano** hacia la expectativa global de la estrategia (o hacia 0) cuando n es chico, para no creerle a una celda con 15 trades

```
E_shrunk = (n · media_celda + n0 · media_prior) / (n + n0)
LCB      = E_shrunk − z · σ / √(n + n0)
```

**La decisión usa LCB, no la media.** Una estrategia con E = +0,10 R y n = 30 no se opera porque su LCB es negativa.

### 10.3 Tamaño de muestra necesario (respuesta a "la estrategia ganó 80 %")

Para afirmar con 95 % de confianza que E > 0 cuando la expectativa real es E con desvío σ (en R ≈ 1):

```
n ≈ (z · σ / E)²
E = 0,10 R  →  n ≈ 384 trades
E = 0,05 R  →  n ≈ 1.537 trades
```

Y si se probaron 150 combinaciones (10 estrategias × 15 regímenes), la corrección por pruebas múltiples (Bonferroni, z ≈ 3,4) lleva esos números a ~1.150 y ~4.600 trades **por celda**. **Conclusión de diseño:** con 15 regímenes y 10 estrategias no hay datos suficientes para nada durante mucho tiempo. El MVP debe usar pocas celdas (§11, §20).

### 10.4 Calibración

Si un modelo dice p = 0,60, de cada 100 señales con p ≈ 0,60 deberían ganar ~60. Se verifica con curvas de calibración por bin en OOS y en vivo. Un modelo descalibrado invalida todo el cálculo de E_net aunque su "accuracy" parezca buena.

### 10.5 Métricas del Expectancy Engine

Win rate, ganancia neta media, pérdida neta media, profit factor neto, expectativa (R y moneda), costo medio por trade (absoluto y en R), retorno ajustado por riesgo (Sharpe/Sortino por trade y diario), MFE/MAE medias, duración media, **y todas con su intervalo de confianza y su n**. Ninguna métrica se muestra sin su tamaño de muestra.

---

## 11. Market Regime Engine

### 11.1 Crítica a la lista de regímenes del prompt

Los 15 regímenes propuestos **no son mutuamente excluyentes** (un mercado puede estar en "Trend Up", "High Volatility", "Momentum" y "Expansion" al mismo tiempo) y mezclan cosas de naturaleza distinta (dirección, volatilidad, liquidez, calidad de datos). Un clasificador de una sola etiqueta con 15 clases va a ser inestable y va a fragmentar la muestra.

### 11.2 Diseño propuesto: régimen multi-eje

| Eje | Estados | Base de cálculo |
|---|---|---|
| **Tendencia** | UP / DOWN / NONE | efficiency ratio + pendiente del mid en 2–10 min |
| **Volatilidad** | LOW / NORMAL / HIGH | percentil de la volatilidad realizada vs. la misma franja horaria de los últimos N días |
| **Fase de volatilidad** | EXPANDING / STABLE / CONTRACTING | ratio vol corta / vol larga |
| **Costo/liquidez** | NORMAL / WIDE_SPREAD / THIN | percentil del spread, tick rate, DOM si existe |
| **Integridad** (gate, no régimen) | OK / ANOMALY / UNKNOWN | calidad del feed, saltos, noticias en curso, rollover |

Conceptos del prompt como "Breakout", "Exhaustion", "Mean Reversion", "Momentum" **no son regímenes; son eventos o patrones** y pertenecen a las estrategias (detección de oportunidades). "Chaotic", "Abnormal Spread", "Poor Liquidity" y "Unknown" se mapean al eje de costo/liquidez y al gate de integridad, y son **condiciones de no-trade**.

**Para el MVP:** solo Volatilidad (3) × Tendencia (3) = 9 celdas, más el gate. Agregar ejes solo cuando la muestra lo permita.

### 11.3 REGIME_CONFIDENCE

```
confianza = mín(c_margen, c_acuerdo, c_persistencia, c_datos)

c_margen       = distancia normalizada del valor al umbral más cercano
c_acuerdo      = coincidencia entre ventana corta y media
c_persistencia = tiempo en el régimen actual vs. mínimo requerido
c_datos        = calidad del feed reciente
```

- **Histéresis:** para cambiar de estado, el indicador debe cruzar el umbral por un margen y sostenerse un tiempo mínimo. Evita que el régimen parpadee tick a tick.
- **Confianza < umbral** → el Risk Engine reduce tamaño; **< umbral mínimo** → `NO_TRADE(REGIME_UNCERTAIN)`.

### 11.4 Calibración y validación

- Umbrales y percentiles se calibran offline (Python), **por símbolo y por franja horaria**, y se versionan igual que una estrategia.
- Se valida que el régimen tenga **valor predictivo**: si la expectativa de las estrategias no difiere entre regímenes, el régimen no sirve y solo agrega complejidad.
- Arrancar con reglas deterministas e interpretables. Modelos como HMM o clustering quedan para después, y solo si superan a las reglas en OOS.

---

## 12. Strategy Selector y biblioteca de estrategias

### 12.1 Score de selección

```
score(señal) = LCB(E_net | estrategia, versión, celda de régimen, costo actual)
               × factor_confianza_régimen
               × factor_estabilidad (penaliza deterioro reciente detectado por CUSUM)
               − penalización_correlación (con posiciones abiertas)
               − penalización_drawdown_estrategia
```

- **"NO TRADE" siempre es un candidato con score 0.** Se elige una señal solo si su score es > 0 con margen.
- **Winner's curse:** elegir el máximo entre muchas señales sesga hacia arriba la expectativa de la elegida. El shrinkage y el uso de LCB lo mitigan; además, la expectativa realizada de "la mejor señal elegida" se mide por separado.
- En el MVP con 1–2 estrategias el selector es casi trivial. **No conviene construir un selector sofisticado antes de tener al menos dos estrategias validadas** por separado.

### 12.2 Ficha obligatoria por estrategia

Lógica de entrada, lógica de salida, lógica de riesgo (dónde va el stop y por qué), regímenes permitidos/prohibidos, holding esperado y máximo, costos esperados, expectativa histórica (IS/OOS/WF/live, separadas), sensibilidad a la ejecución (cuánto cae E por cada +0,1 pip de costo y por cada +50 ms de latencia), **y la hipótesis económica**: por qué debería funcionar y quién está del otro lado. Una estrategia sin hipótesis económica es candidata a overfitting.

### 12.3 No-Trade Engine

Autoridad de veto final. Condiciones (cada una con umbral configurable y versionado):

| Condición | Ejemplo de umbral inicial |
|---|---|
| Spread excesivo | spread > P90 de la franja horaria, o > máximo absoluto por símbolo |
| Slippage reciente excesivo | slippage medio de últimas N ejecuciones > P90 histórico |
| Latencia elevada | ping o latencia de orden > umbral por estrategia (de su sensibilidad medida) |
| Integridad ANOMALY/UNKNOWN | siempre bloquea |
| Régimen incierto | confianza < mínimo |
| Edge insuficiente | LCB(E_net) ≤ umbral |
| Movimiento esperado < MPM | siempre bloquea |
| Riesgo excesivo | cualquier límite del Risk Engine |
| Drawdown / pérdida diaria | límites del §13 |
| Ventana de noticias | ±N minutos de eventos de alto impacto (calendario MT5) |
| Rollover / apertura de sesión | franjas configurables |
| Demasiadas operaciones recientes | tope por minuto/hora como **protección contra bugs** (no como objetivo) |
| Correlación excesiva | exposición al mismo factor > límite |
| Ejecución degradada | tasa de rechazo/requote > umbral |
| Estrategia no `PRODUCTION` | siempre bloquea |

Cada veto se registra con el motivo exacto (para responder "¿por qué no entramos?").

### 12.4 Biblioteca: evaluación crítica de A–J

| Estrategia | Comentario | Prioridad |
|---|---|---|
| A. Momentum | Hipótesis clara (flujo de órdenes persistente tras impulso). Muy sensible a costo y latencia en horizontes cortos. | **MVP candidata** |
| B. Mean Reversion | En ticks, gran parte de la "reversión" es rebote bid-ask, que no se puede capturar porque es justamente el spread. Válida en horizontes de minutos tras spikes. | **MVP candidata** (horizonte ≥ 30 s) |
| C. Breakout | Alta tasa de falsos breakouts; depende de régimen de volatilidad. | Fase posterior |
| D. Breakout + Retest | Menos señales, mejor selección; útil para comparar con C. | Fase posterior |
| E. Liquidity Sweep | Sin DOM real, "liquidez" es inferida y el concepto se vuelve vago. Exige definición operativa precisa antes de testear. | Baja |
| F. Volatility Expansion | Más un filtro/régimen que una estrategia. | Como filtro |
| G. Volatility Compression | Ídem, precondición de F/C. | Como filtro |
| H. Exhaustion/Reversal | Difícil de definir sin sesgo retrospectivo. | Baja |
| I. Tick Momentum | Es A en escala de ticks; el feed del broker puede generar patrones artificiales. | Variante de A |
| J. Spread/Execution-based | **Reformular.** Si significa explotar precios desfasados del broker, es arbitraje de latencia: prohibido por la mayoría de los brokers, con anulación de ganancias. Lo legítimo es usar spread/ejecución como **filtro** ("operar solo cuando el costo es bajo"), no como fuente de alfa. | Solo como filtro |

**Línea base obligatoria:** toda estrategia se compara contra una **entrada aleatoria con la misma lógica de salida, mismo horario y mismo costo**. Si la estrategia no supera significativamente a la entrada aleatoria, la señal no aporta nada (lo que "funciona" es la salida o el período).

---

## 13. Risk Engine

### 13.1 Jerarquía de límites

```
Nivel cuenta     : drawdown máximo, pérdida diaria, pérdida semanal, exposición total
Nivel portfolio  : exposición por factor (p. ej. USD), correlación entre posiciones
Nivel estrategia : drawdown por estrategia, pérdidas consecutivas, deterioro de edge
Nivel símbolo    : exposición máxima, posiciones simultáneas
Nivel trade      : riesgo por operación, distancia de stop válida, costo en R máximo
```

Valores iniciales sugeridos (a ajustar con tu tolerancia real):

| Límite | Micro-live | Producción inicial |
|---|---|---|
| Riesgo por trade | volumen mínimo fijo | 0,25 % – 0,5 % |
| Pérdida diaria → stop del día | 1 % | 2 % |
| Pérdida semanal → stop de semana | 2 % | 4 % |
| Drawdown máximo → `HALT` + revisión humana | 5 % | 10 % |
| Posiciones simultáneas | 1 | 1 por símbolo, 3 total |
| Pérdidas consecutivas → enfriamiento | 5 | 6–8 (calibrado con Monte Carlo) |

### 13.2 Position sizing

```
riesgo_moneda   = equity × riesgo_% × multiplicadores
pérdida_por_lote = (distancia_stop + costo_esperado_rt + slippage_stop_P90)
                   × valor_por_unidad_de_precio_por_lote
lotes_brutos    = riesgo_moneda / pérdida_por_lote

multiplicadores ∈ [0, 1]:
  × confianza_régimen  × escalado_por_drawdown  × calidad_ejecución_reciente
  × calidad_señal (solo reduce, nunca > 1)

lotes = mín(lotes_brutos, tope_liquidez, tope_margen, tope_exposición, tope_estrategia)
lotes = floor(lotes / volume_step) × volume_step
si lotes < volume_min → NO_TRADE(SIZE)
```

- El valor por unidad de precio sale de `SYMBOL_TRADE_TICK_VALUE` / `SYMBOL_TRADE_TICK_SIZE`, con cuidado en símbolos cuya moneda de profit no es la de la cuenta (el tick value cambia con el tipo de cambio).
- **Nunca redondear hacia arriba al volumen mínimo.** Con capital chico, esta regla va a bloquear muchas operaciones de stop amplio. Es correcto: si el mínimo del broker excede tu presupuesto de riesgo, esa operación no es para tu cuenta.
- Todos los multiplicadores son ≤ 1. **No existe ningún camino en el código por el que una pérdida aumente el tamaño.**

### 13.3 Risk scaling down

```
escalado_por_drawdown = 1                    si DD < DD1
                      = lineal hasta 0,25    entre DD1 y DD2
                      = 0 (HALT)             si DD ≥ DD_max
```

### 13.4 Capital Scaling Engine

- El riesgo sube **por escalones** (p. ej. ×1,25), nunca se duplica.
- Para subir de escalón (todas obligatorias): n mínimo de trades **en vivo** en el escalón actual; LCB de E_net > 0 en vivo; desempeño en vivo consistente con OOS (sin degradación significativa); drawdown dentro del percentil esperado por Monte Carlo; ejecución estable; **aprobación humana**.
- Para bajar: **automático e inmediato** cuando se viola cualquier condición.
- Asimetría deliberada: subir es lento y requiere evidencia; bajar es rápido y automático.

### 13.5 Prohibiciones (compiladas como restricciones, no como configuración)

Martingala, grid sin límite, aumento de tamaño tras pérdidas, "recuperación" de pérdidas, mover el stop en contra, desactivar el stop de catástrofe. El código no tiene parámetros que permitan activar ninguna de estas cosas.

---

## 14. Learning Engine

### 14.1 Qué aprende y qué no

| Aprende (en Python, offline) | No hace |
|---|---|
| Expectativa por (estrategia, régimen, franja horaria, rango de spread, volatilidad, duración) | Modificar parámetros en vivo |
| Distribuciones reales de costo y su relación con las condiciones | Activar estrategias |
| Duración óptima por estrategia (curva de expectativa vs. tiempo) | Aumentar riesgo |
| Qué condiciones preceden a falsos positivos | Escribir en `/approved/` |
| Calibración de probabilidades | Borrar o filtrar datos negativos |
| Deterioro del edge en vivo | |

Su salida son **observaciones y estadísticas**, que alimentan al Hypothesis Engine.

### 14.2 Aprender de decisiones, no de resultados

Cada operación se clasifica en cuatro dimensiones independientes:

| Dimensión | Pregunta | Cómo se evalúa |
|---|---|---|
| **Calidad de decisión** | ¿Se respetaron todas las reglas y había edge esperado según el modelo vigente en ese momento? | Ex-ante: estrategia `PRODUCTION`, LCB(E_net) > umbral con la info de ese momento, todos los checks pasados. **No depende del resultado.** |
| **Calidad de ejecución** | ¿El costo real estuvo dentro de lo esperado? | Implementation shortfall vs. distribución esperada: ≤ P50 bueno, P50–P90 normal, > P90 malo. |
| **Comportamiento del mercado** | ¿El precio se comportó como predecía la señal? | Trayectoria del mid vs. banda esperada (MFE en tiempo esperado, etc.). |
| **Resultado financiero** | ¿Ganó o perdió neto? | Signo del P&L neto. |

Ejemplos del prompt:

```
Señal con edge + ejecución pésima → pérdida
  DECISION = GOOD, EXECUTION = BAD, MARKET = AS_EXPECTED, RESULT = LOSS

Entrada sin edge (bug o regla mal aplicada) → ganancia
  DECISION = BAD, RESULT = WIN   → se investiga como error, no como acierto
```

**Límite honesto:** en una sola operación no se puede saber si la *señal* era buena (el azar domina). La calidad de la señal y del modelo se evalúa **en agregado**: calibración, expectativa realizada vs. predicha por bin, en cientos de operaciones. La clasificación individual sirve para separar errores de proceso (decisión mala) y problemas de ejecución.

### 14.3 Detección de deterioro (PAUSE automático)

En vivo (dentro de MT5, porque es protección):

- **CUSUM** sobre (R_neto − E_esperado) por estrategia: si la suma acumulada de desvíos negativos supera un umbral → `PAUSED`.
- **Test secuencial (SPRT)** entre H0: "E = E_validado" y H1: "E = 0": si gana H1 → `PAUSED`.
- Pausar es una acción conservadora: el sistema la puede tomar solo. **Reactivar requiere investigación y aprobación.**

Esto implementa el §45 del prompt: "Esta estrategia funcionaba. Ahora dejó de funcionar." → `PAUSE`.

---

## 15. Research Engine

### 15.1 Simulador de tick-replay (pieza central)

```
Para cada tick histórico (grabado por el TickRecorder propio):
  1. actualizar features (misma lógica que MQL5)
  2. evaluar régimen, señales, costos, expectativa, riesgo, no-trade
  3. si hay orden: muestrear latencia L de la distribución medida
     → el fill ocurre al precio del primer tick en t + L
     → + slippage muestreado del modelo condicional
     → con probabilidad p_rechazo (medida) la orden se rechaza
     → respetar stops level, freeze level, volumen mínimo/step
  4. gestionar posición (stops, time exit) con la misma lógica
  5. registrar exactamente el mismo esquema de datos que el EA en vivo
```

Que el simulador y el EA produzcan **el mismo esquema de logs** permite comparar backtest vs. vivo trade a trade.

### 15.2 Paridad MQL5 ↔ Python

Riesgo serio y subestimado: que la feature "velocidad 5 s" se calcule distinto en MQL5 y en Python (training/serving skew). Mitigación: tests dorados — mismo archivo de ticks procesado por ambos, comparación de cada feature con tolerancia. Se ejecutan en cada cambio de cualquiera de los dos lados.

### 15.3 Hypothesis Engine

Formato estructurado (igual que el ejemplo del prompt), con dos agregados críticos:

```
ID: H-0007
OBSERVACIÓN: Momentum V1 pierde expectativa cuando spread > P75 (n=412, live+paper)
HIPÓTESIS: Filtrar spread > P75 mejora LCB(E_net)
PRE-REGISTRO: criterio de aceptación definido ANTES de testear:
              ΔE_net OOS > +0,03 R y LCB > 0, y no reduce n en más de 40 %
DATOS: IS 2026-01..2026-06 / OOS 2026-07..2026-09 (nunca vistos para esta hipótesis)
TESTS: backtest, OOS, walk-forward, stress spread ×2, slippage P90
RESULTADO: ACCEPT / REJECT
N_PRUEBAS_ACUMULADAS: 37   ← cuántas hipótesis se probaron sobre estos datos
```

- **Pre-registro:** el criterio de aceptación se escribe antes de ver el resultado. Evita racionalizar.
- **Contador de pruebas:** cada prueba sobre el mismo conjunto de datos "gasta" significancia. Con 37 pruebas, un resultado al 95 % es esperable por azar ~2 veces. Se usa para ajustar la significancia (deflated Sharpe, corrección por pruebas múltiples).
- **Datos OOS "quemados":** un período OOS usado para decidir una hipótesis deja de ser OOS para las siguientes. Se lleva registro.

### 15.4 Machine Learning: posición prudente

- Arrancar con estadística descriptiva y reglas simples. ML solo cuando haya una línea base sólida que superar.
- Modelos simples primero (regresión logística, gradient boosting con pocas features), con validación purgada (purged/embargoed CV) para no filtrar información entre ventanas solapadas.
- Si un modelo pasa todo, se exporta a **ONNX**, se versiona con hash y corre dentro de MT5. Nunca un modelo que se reentrena solo en vivo.

---

## 16. Sistema de versionado

### 16.1 Qué identifica unívocamente a una decisión

```
decision.strategy_ref = "MOMENTUM@V3"
  → strategy_id         MOMENTUM
  → version             V3
  → params_hash         sha256 del JSON de parámetros
  → code_ref            commit git + sha256 del .ex5 compilado
  → model_ref           sha256 del .onnx (si aplica)
  → regime_ref          REGIME@V2 (+ hash de umbrales)
  → cost_model_ref      COSTS@2026-10-01 (+ hash)
  → risk_config_ref     RISK@V1 (+ hash)
```

Con esto, cualquier operación se puede reproducir exactamente en el simulador.

### 16.2 Registro de estrategias

Por versión: id, versión, parámetros, fecha de creación, fecha de validación, métricas IS/OOS/WF/stress/paper/live (separadas), reporte de auditoría, estado, historial de transiciones (quién, cuándo, por qué).

**Inmutabilidad:** una versión publicada no se modifica jamás. Cualquier cambio de parámetro, por mínimo que sea, crea una versión nueva que recorre todo el pipeline. Nunca se reemplaza una versión silenciosamente.

### 16.3 Máquina de estados

```
RESEARCH → BACKTEST → OOS → WALK_FORWARD → PAPER → MICRO_LIVE → APPROVED → PRODUCTION
                                                                                │
cualquier estado ──(falla)──► RETIRED                     PRODUCTION ──► PAUSED ┘
                                                          PAUSED ──► RESEARCH (re-investigar)
                                                          PAUSED/PRODUCTION ──► RETIRED
```

| Transición | Quién puede hacerla |
|---|---|
| Avanzar hasta `MICRO_LIVE` (entrar) | Pipeline automático si pasa los gates **+ confirmación humana para entrar a micro-live** (usa dinero real) |
| `MICRO_LIVE → APPROVED` | **Solo humano**, con reporte |
| `APPROVED → PRODUCTION` | **Solo humano** |
| `PRODUCTION → PAUSED` | **Automático** (CUSUM/SPRT/emergencia) o humano |
| `PAUSED → PRODUCTION` | **Prohibido directo**: debe volver a investigación o, como mínimo, a micro-live |
| `* → RETIRED` | Automático por falla de gate, o humano |

El EA solo opera estrategias en `PRODUCTION` (y `MICRO_LIVE` con volumen mínimo forzado).

---

## 17. Sistema de validación

### 17.1 Pipeline y gates

| Gate | Criterio (orientativo, a fijar en Fase 12–15) | Falla crítica ⇒ |
|---|---|---|
| ASSUMPTION CHECK | Hipótesis económica escrita; sin look-ahead (auditoría de timestamps); costos `MEASURED` o explícitamente conservadores | REJECT |
| COST CHECK | E_net > 0 con costos medidos; sigue > 0 con spread ×1,5 | REJECT |
| IS | E_net > 0, n suficiente, mejor que línea base aleatoria con significancia | REJECT |
| OOS (cronológico, con embargo) | LCB(E_net) > 0; degradación vs. IS < 50 % | REJECT |
| WALK-FORWARD (rolling) | ≥ 70 % de ventanas con E_net > 0; sin dependencia de una sola ventana | REJECT |
| PARAMETER PERTURBATION | ±10–20 % en cada parámetro mantiene E_net > 0 (meseta, no pico) | REJECT |
| MONTE CARLO (block bootstrap) | P(DD > límite) < 5 %; P(ruina) < 1 % al riesgo propuesto | REJECT |
| STRESS | Spread ×2, slippage P90 en todos los fills, latencia +100 ms, win rate −5 pp: E_net no cae a < 0 en el escenario base de stress definido | REJECT |
| REGIME CHECK | Expectativa explicada por regímenes permitidos; no depende de un solo episodio | REJECT |
| OVERFITTING CHECK | Deflated Sharpe ajustado por N_PRUEBAS; cantidad de parámetros razonable vs. n | REJECT |
| EXECUTION CHECK | Sensibilidad a latencia compatible con la latencia medida real | REJECT |
| PAPER (shadow en cuenta real, sin órdenes) | Frecuencia y distribución de señales consistentes con el simulador | Volver a investigación |
| MICRO_LIVE | n mínimo; costos reales dentro de lo modelado; E_net en vivo consistente con OOS (test estadístico) | PAUSED / RETIRED |

"No racionalizar el resultado": los gates se evalúan con código, contra criterios pre-registrados. Si falla un gate crítico, el estado pasa a `RETIRED` automáticamente; para volver hay que crear una versión nueva con una hipótesis nueva.

### 17.2 Sobre "paper"

El paper trading en **cuenta demo** valida la lógica de señal pero **no** la ejecución (la demo suele ejecutar perfecto). Propuesta: "shadow mode" en el terminal de la cuenta real (el EA decide y registra sin enviar órdenes, con el feed real) y luego **micro-live** con volumen mínimo, que es el único test real de ejecución. El costo de micro-live es un **costo de investigación presupuestado**.

### 17.3 Monte Carlo

- **Block bootstrap** de la secuencia de R netos (preserva autocorrelación y rachas), no shuffle simple.
- Escenarios: reordenamiento, costos aumentados, win rate reducido, colas de pérdida más gordas, períodos sin edge insertados.
- Salidas: distribución de drawdown máximo, P(ruina) definida como caída a X % del capital, tiempo hasta recuperación, distribución de retorno a 1/3/6 meses (presentada como distribución, **nunca como proyección**).

---

## 18. Sistema de seguridad

### 18.1 Emergency Risk Controller — estados

```
NORMAL ──► DEGRADED ──► HALT_NEW ──► FLATTEN ──► STOPPED
  ▲            │            │
  └────────────┴────────────┘  (vuelta a NORMAL: solo humano desde HALT_NEW o peor)
```

| Estado | Efecto | Disparadores típicos |
|---|---|---|
| DEGRADED | Riesgo reducido, solo estrategias más robustas | latencia alta, slippage elevado, régimen incierto prolongado |
| HALT_NEW | Sin entradas nuevas; posiciones existentes se gestionan normalmente | pérdida diaria, errores repetidos, discrepancia de reconciliación, datos corruptos, desconexión breve |
| FLATTEN | Cierra todas las posiciones (con control de costos) y luego HALT | drawdown máximo, anomalía grave de ejecución, comportamiento inesperado |
| STOPPED | EA inactivo (`ExpertRemove()`), requiere reinicio manual | kill switch, fallas en cascada |

### 18.2 Kill switch inequívoco (varias vías, cualquiera alcanza)

1. Botón en el dashboard ("STOP") → FLATTEN + STOPPED.
2. Archivo `STOP` en la carpeta común → se lee en cada `OnTimer`.
3. Variable global del terminal `ATS_STOP = 1`.
4. Botón "Algo Trading" del terminal (MT5 bloquea `OrderSend` desde el propio terminal).
5. Desconexión: los **SL de catástrofe en el servidor** protegen las posiciones aunque el terminal/VPS muera.

### 18.3 Otras protecciones

- **Límites duros compilados** (riesgo por trade, volumen máximo absoluto, operaciones por minuto) que ninguna configuración puede superar.
- **Watchdog/heartbeat:** el EA escribe un latido; un monitor externo (opcional, fuera de la ruta crítica) alerta si se detiene.
- **Reconciliación periódica** (§8.2).
- **Detección de bucles:** muchas órdenes en poco tiempo, apertura/cierre repetido del mismo símbolo → HALT. Protege contra el bug más caro: el bucle de órdenes.
- **Datos corruptos:** bid ≥ ask, saltos > N desvíos sin confirmación, feed congelado > N s en horario activo → integridad ANOMALY.
- **Arranque seguro:** al iniciar, el EA reconcilia posiciones existentes, verifica config y arranca en HALT_NEW hasta que todos los chequeos pasen.
- **DLLs deshabilitadas** salvo necesidad justificada.

---

## 19. Estructura de almacenamiento

### 19.1 Dónde

| Dato | Escritor | Formato | Ubicación |
|---|---|---|---|
| Ticks crudos | TickRecorder (Service) | binario propio (struct `MqlTick` + timestamp local), un archivo por símbolo/día | `Common/Files/ATS/ticks/` |
| Decisiones, órdenes, ejecuciones, resultados, eventos | EA | SQLite (modo WAL, transacciones por lote) | `Common/Files/ATS/live.db` |
| Configuración aprobada | Humano (script de promoción) | JSON + hash | `Common/Files/ATS/approved/` |
| Candidatos | Python | JSON | `research/candidates/` (MT5 no lo lee) |
| Datos de investigación | Python | Parquet particionado (símbolo/fecha) | `research/data/` |
| Registro de estrategias, hipótesis, experimentos | Python | SQLite/JSON versionado en git | `research/registry/` |

### 19.2 Esquema lógico (tablas principales)

```
symbols_spec      (snapshot de SymbolInfo* por día: digits, point, tick_size, tick_value,
                   contract_size, volume_min/max/step, stops_level, freeze_level,
                   filling_mode, exemode, sesiones, comisión)

features_snapshot (snapshot_id, ts_server_msc, ts_local_us, symbol, feature_json, regime_ref)

regime_log        (ts, symbol, eje_tendencia, eje_vol, eje_fase, eje_costo, integridad,
                   confianza, regime_ref)

signals           (signal_id, snapshot_id, strategy_ref, direction, score, confidence,
                   entry_sugerido, stop, target, expected_gross_win, expected_gross_loss,
                   expected_cost_rt, e_net, e_net_lcb, mpm,
                   status: SELECTED | REJECTED, reject_reason)

decisions         (decision_id, signal_id, risk_pct, lots, lots_raw, multiplicadores_json,
                   reason_entry_text, emergency_state, config_refs_json)

orders            (order_id, decision_id, type, requested_price, requested_lots, filling,
                   t_send_us, t_ack_us, retcode, retcode_desc, retry_of)

executions        (deal_id, order_id, fill_price, fill_lots, deal_time_msc, commission,
                   swap, mid_at_decision, spread_at_send, slippage_points)

trades            (trade_id, decision_id, symbol, direction, open/close refs,
                   entry_req, entry_exec, exit_req, exit_exec, duration_ms,
                   mfe, mae, gross_pnl, spread_cost, commission_cost, slippage_cost,
                   latency_cost, net_pnl, net_r, reason_exit,
                   decision_quality, execution_quality, market_as_expected, result)

risk_events       (ts, level, rule, value, threshold, action)
system_events     (ts, type, detail)  -- errores, reconexiones, cambios de estado, config cargada
```

Esto cubre todos los campos obligatorios del §10 del prompt y permite responder las preguntas del §40 ("¿por qué entramos?", "¿por qué ese tamaño?", etc.) con una consulta.

### 19.3 Reglas de integridad

- **Append-only.** No se borra ni se modifica ningún registro. Las correcciones son registros nuevos que referencian al original.
- Trades perdedores, rechazados y errores se guardan igual que todo lo demás.
- Backups diarios; hash diario de la base para detectar alteraciones.
- Live, paper/shadow, micro-live y simulación llevan una columna `environment` y **nunca se mezclan en una métrica**.

### 19.4 Volumen estimado

Ticks: unos pocos MB a decenas de MB por símbolo y día (depende de la actividad del broker). Decisiones/trades: insignificante. Un año de 5 símbolos entra cómodo en un disco común; Parquet comprime mucho.

---

## 20. MVP recomendado

### 20.1 Reordenamiento de fases

Propongo cambiar el orden de las 18 fases del prompt: **medir costos y grabar datos antes de escribir estrategias.** Construir una estrategia antes de conocer el costo real es construir sobre un supuesto.

| Nueva etapa | Contenido (fases del prompt) | Gate para avanzar |
|---|---|---|
| **0. Medición** | 2 Market Data + TickRecorder, 10 Logging básico, 7 Cost Engine (solo medición), sonda de ejecución | Mapa CVR(h) por símbolo/hora; costos reales medidos; ToS del broker verificados |
| **1. Investigación** | 3 Features (Python + MQL5 con paridad), 4 Regime (calibración), 12 simulador, 5 primera estrategia + línea base aleatoria, 6 Expectancy | Una estrategia pasa IS/OOS/WF/stress en el simulador con costos medidos |
| **2. Esqueleto live** | 8 Risk, 9 Execution, No-Trade, Emergency, 11 Dashboard, 10 Logging completo | Tests unitarios + tester MT5 con paridad vs. simulador + 1–2 semanas de shadow mode |
| **3. Micro-live** | 16–17 | n mínimo con costos dentro de lo modelado y E_net consistente con OOS |
| **4. Expansión** | 13–15 Research/Learning/WF/MC automatizados, más estrategias, 18 Escalamiento | Cada estrategia nueva recorre todo el pipeline |

### 20.2 Alcance concreto del MVP

- **1 broker** con cuenta raw/ECN, ejecución Market, términos que permitan scalping, servidor conocido.
- **VPS** cerca del servidor del broker (Windows, porque MT5 es nativo en Windows).
- **2 símbolos** con costo bajo relativo a la volatilidad (candidatos a medir: EURUSD y un índice o el oro; elegir con el mapa CVR, no a priori).
- **Horizonte inicial 30 s – 5 min.** Experimento explícito para medir cómo cae el edge al acortar el horizonte. Si el edge sobrevive a horizontes más cortos, se acorta; no al revés.
- **1 estrategia** (momentum o reversión post-spike, la que sugiera la Fase 0) **+ línea base aleatoria**.
- **Régimen de 9 celdas** (volatilidad × tendencia) + gate de integridad.
- Risk Engine completo, No-Trade completo, Emergency completo **desde el día uno** (no son "features" que se agregan después).
- Selector trivial (una estrategia) pero con la interfaz ya definida.
- Sin ML, sin DOM, sin multi-estrategia.

### 20.3 Sonda de ejecución (Etapa 0)

Unas 150–300 operaciones de **volumen mínimo**, distribuidas en distintas horas y condiciones, con entrada aleatoria y salida a tiempo fijo, en la cuenta **real**. Objetivo: medir latencia, slippage (y su asimetría), rechazos, comisión real. Costo esperado: pequeño y acotado de antemano (estimable una vez elegido el broker). Es el único modo de obtener costos reales; ningún backtest los da.

---

## 21. Riesgos técnicos

| # | Riesgo | Severidad | Mitigación |
|---|---|---|---|
| T1 | Backtest optimista por ejecución ideal del tester | Crítica | Simulador propio con costos medidos; paridad backtest-vivo trade a trade |
| T2 | Diferencia entre ticks históricos del broker y ticks recibidos en vivo | Alta | TickRecorder propio; investigar sobre ticks propios |
| T3 | Training/serving skew (features distintas en MQL5 y Python) | Alta | Tests dorados de paridad |
| T4 | Look-ahead bias (usar información futura sin querer) | Crítica | Auditoría de timestamps; simulador estrictamente causal; tests con datos sintéticos que detectan look-ahead |
| T5 | Ticks salteados por `OnTick` lento | Media | `OnTick` mínimo, `CopyTicks` de recuperación, medición del tiempo de proceso |
| T6 | Bucle de órdenes por bug | Crítica | Límites duros compilados, detección de bucles, HALT |
| T7 | Estado desconocido tras timeout (posición duplicada) | Alta | Reconciliación obligatoria antes de reintentar |
| T8 | Caída de VPS/terminal con posiciones abiertas | Alta | SL de catástrofe en servidor; arranque seguro con reconciliación |
| T9 | Stops level > stop operativo deseado | Media | Stops virtuales + SL de catástrofe; documentar el riesgo de gap |
| T10 | Cambios del broker en specs (comisión, stops level, horario) sin aviso | Media | Snapshot diario de specs y alerta ante cambios |
| T11 | Bloqueo del hilo del EA por escritura a disco | Media | Buffer + escritura por lotes; logging pesado en Service |
| T12 | Clock drift entre servidor y local | Baja | Estimación continua de offset; latencia de feed marcada como estimada |
| T13 | Complejidad excesiva (17 motores antes de tener un edge) | Alta | MVP mínimo, construir solo lo que una estrategia validada necesita |
| T14 | Contaminación de producción por investigación | Crítica | Separación física (sin código de aprendizaje en el EA), config solo vía `/approved/` con hash |

## 22. Riesgos financieros

| # | Riesgo | Comentario |
|---|---|---|
| F1 | **No existe edge neto en el horizonte deseado** | El riesgo más probable. La Fase 0 está diseñada para detectarlo barato. Hay que aceptar que el resultado del proyecto puede ser "no viable". |
| F2 | Costos que consumen el edge | Con alta frecuencia el costo acumulado domina. Ver §9.6. |
| F3 | Overfitting / falsos descubrimientos | Con muchas estrategias × regímenes × parámetros, aparecen "edges" por azar. Pre-registro, contador de pruebas, OOS quemado. |
| F4 | Decaimiento del edge (dejó de funcionar) | CUSUM/SPRT → PAUSE automático. |
| F5 | Riesgo de contraparte del broker (B-book, anulación de ganancias, quiebra) | Elegir broker regulado, ejecución STP/ECN; leer términos; no dejar más capital del necesario en la cuenta. |
| F6 | Gaps y eventos extremos (noticias, flash crash, fin de semana) | No operar noticias; stops de catástrofe; sin posiciones en cierre de semana; tamaño que soporte slippage extremo. |
| F7 | Capital chico + volumen mínimo del broker | Puede hacer imposible respetar el riesgo por trade; la regla "no redondear hacia arriba" va a bloquear operaciones. |
| F8 | Riesgo de ruina por crecimiento agresivo | Ver abajo. |
| F9 | Sesgo psicológico del operador (apagar el sistema tras pérdidas normales, o encenderlo más agresivo tras ganancias) | Límites y escalado definidos de antemano; cambios solo por pipeline. |
| F10 | Costo de infraestructura (VPS, datos) vs. capital | Con capital muy chico, el VPS solo puede ser un porcentaje relevante del capital por mes. |

**Sobre "transformar poco capital en mucho" (respuesta a "quiero crecer rápido"):** el crecimiento compuesto depende de la expectativa logarítmica, no de la aritmética. Arriesgar más que una fracción de Kelly aumenta la varianza más rápido que el crecimiento y, por encima de ~2× Kelly, el crecimiento esperado se vuelve **negativo** aunque cada trade tenga expectativa positiva. Como la expectativa real nunca se conoce con precisión (solo un intervalo), lo prudente es fracciones chicas de Kelly calculadas sobre la **LCB**, no sobre la media. El sistema reportará P(ruina) y la distribución de drawdown para cada nivel de riesgo propuesto; no reportará proyecciones de crecimiento como metas.

---

## 23. Supuestos a comprobar experimentalmente

Cada uno con método y criterio de rechazo, a ejecutar en la Etapa 0–1.

| # | Supuesto | Método | Se rechaza si… |
|---|---|---|---|
| S1 | Existe algún horizonte/símbolo/franja con CVR < 0,3 | Mapa CVR(h) con ticks propios + costos medidos | Ningún símbolo tiene CVR < 0,5 en h ≤ 5 min |
| S2 | La latencia desde el VPS es estable y baja | Distribución de `t_ack − t_send` y ping, 2 semanas | P95 > 100 ms o alta variabilidad |
| S3 | El slippage es simétrico (sin manipulación del dealer) | Sonda de ejecución: distribución de slippage positivo vs. negativo, por dirección y volatilidad | Asimetría significativa en contra → cambiar de broker |
| S4 | El broker no rechaza/requotea en exceso | Tasa de rechazos/requotes en la sonda | > 2–3 % de órdenes |
| S5 | Los ticks históricos del broker ≈ ticks recibidos en vivo | Comparar TickRecorder vs. `CopyTicksRange` histórico del mismo día | Diferencias materiales en cantidad/precios |
| S6 | El DOM (si existe) es real y útil | Correlación entre desequilibrio de libro y movimiento futuro; verificar si cambia con ejecuciones | Libro estático/sintético |
| S7 | La estrategia candidata supera a la entrada aleatoria | Simulador, mismos costos, test estadístico | No supera significativamente |
| S8 | El régimen tiene valor predictivo | Expectativa de la estrategia por celda; test de diferencia | Sin diferencias significativas |
| S9 | El edge sobrevive al acortar el horizonte | Curva E_net(h) | E_net cae a ≤ 0 por debajo de cierto h → ese es el horizonte mínimo |
| S10 | Simulador ≈ ejecución real | Comparación trade a trade en micro-live | Desvío sistemático en costos o señales |
| S11 | Los términos del broker permiten la operativa | Lectura de ToS + consulta escrita al broker | Prohibición de holding corto o de la estrategia |
| S12 | La demo ejecuta distinto que la real | Mismas órdenes en ambas (sonda) | (Se espera que sí; confirma no usar demo para costos) |

## 24. Datos necesarios antes de comenzar

**Del broker (por cuenta y por símbolo):**
- Tipo de cuenta, modelo de ejecución (STP/ECN/market maker), regulador y jurisdicción.
- Términos y condiciones completos, en especial cláusulas sobre scalping, holding mínimo, arbitraje, "abuso".
- Comisión exacta (por lote/por millón, ida y vuelta), swaps.
- Specs de cada símbolo: digits, tick size, tick value, contract size, volumen min/max/step, stops level, freeze level, filling modes, modo de ejecución, horarios de sesión y de trading.
- Ubicación del servidor de trading (datacenter) para elegir VPS.
- Profundidad de historia de ticks disponible (`CopyTicksRange` hacia atrás).
- Si ofrece DOM y sobre qué símbolos.
- Límites de órdenes/posiciones y de frecuencia.

**Medidos por nosotros (Etapa 0):**
- 2–4 semanas de ticks propios por símbolo candidato (cubriendo sesiones de Asia, Londres, NY y días con noticias).
- Distribución de spread por símbolo × hora × día.
- Latencia (ping y orden) desde el VPS.
- Slippage, rechazos y comisión real desde la sonda de ejecución.
- Calendario económico histórico (nativo en MT5) para marcar ventanas de noticias.

**Tuyos:**
- Capital que vas a destinar (y cuánto de eso estás dispuesto a perder entero en investigación).
- Pérdida máxima tolerable (diaria, semanal, total) antes de detener el proyecto.
- Disponibilidad de Windows/VPS.
- Tiempo disponible para supervisar y aprobar cambios.

---

## 25. Preguntas que necesito que respondas

1. **¿Qué broker y tipo de cuenta tenés (o pensás usar)?** ¿Es ECN/raw o market maker? ¿Ya leíste sus términos sobre scalping?
2. **¿Con cuánto capital arrancarías?** Determina si el volumen mínimo del broker es compatible con el riesgo por trade.
3. **¿Qué instrumentos te interesan?** ¿Solo Forex, o también índices, oro, cripto? ¿Tenés acceso a algún instrumento de bolsa por MT5 (con volumen y libro reales)?
4. **¿Desde dónde correría el terminal?** ¿PC hogareña en Argentina o VPS? Para horizontes cortos, el VPS cerca del broker no es opcional.
5. **¿Cuál es la pérdida que, si ocurre, da por terminado el experimento?** Es el parámetro más importante del Risk Engine y tiene que estar definido antes de operar.
6. **¿Aceptás que la primera etapa (2–3 semanas) sea solo de medición, con un costo acotado de la sonda de ejecución, y que el resultado pueda ser "no hay edge en horizontes de segundos"?**
7. **Repositorio:** este documento quedó en el repo del canal de YouTube (`trading-mt5/`). Para el código conviene un repositorio aparte. ¿Lo creamos?

---

### Próximo paso propuesto

Con tus respuestas a §25: **Etapa 0 — FASE 2 (Market Data Engine + TickRecorder)** y **especificación de la sonda de ejecución**, con el ciclo BUILD → TEST → AUDIT → FIX → VALIDATE. No avanzo a estrategias hasta tener el mapa de costos reales.

---

## 26. Decisiones y ajustes (04/10/2026)

**Decisiones del usuario:**
- **Objetivo:** muchas operaciones rápidas. Se aclara que deben ser muchas *decisiones independientes*, cada una con riesgo chico, y no una posición grande partida en muchas órdenes iguales (como en el reel de referencia, donde ~40 posiciones al mismo precio eran una sola apuesta con apalancamiento de ~5.000 veces).
- **Instrumento principal:** oro (XAUUSD).
- **Brokers posibles:** Exness o BlackBull.
- **Pruebas:** cuenta **cent de Exness** con ~10 USD (1.000 USC).
- **Infraestructura:** PC hogareña que puede quedar prendida mucho tiempo.

**Consecuencias para el diseño:**

| Tema | Consecuencia |
|---|---|
| Cuenta cent | Buena para la sonda de ejecución y el micro-live: el volumen mínimo es diminuto en dólares, así que se puede respetar un riesgo de 0,25–0,5 % por operación incluso con 10 USD (verificar `contract_size` y `volume_min` en `specs`). |
| Cuenta cent | Sus costos (spread, ejecución) **no son los de una cuenta Raw/Zero ni los de BlackBull**. Lo que se mida en cent vale para cent; para otra cuenta hay que volver a medir. |
| 10 USD | Es presupuesto de investigación, no capital para hacer crecer. El objetivo de esta etapa es obtener datos, no ganancia. |
| Apalancamiento alto/ilimitado del broker | No cambia nada: el Risk Engine limita la exposición con sus propios topes, sin importar cuánto permita el broker. |
| PC hogareña en Argentina | Latencia probable de 150–300 ms al servidor: penaliza los plazos de segundos. Se mide con el ping que graba el servicio. Si el mapa de costos muestra espacio en plazos cortos pero la latencia lo come, se evalúa un VPS. |
| PC hogareña | Riesgo de cortes de luz/internet y suspensión: **SL de catástrofe en el servidor obligatorio** en toda operación (ya previsto en §8 y §18). |
| Exness / BlackBull | Leer los términos de ambos sobre scalping y plazos mínimos antes de operar en real. BlackBull (cuentas con comisión) puede servir para comparar costos con una cuenta demo. |

**Próximo entregable:** grabación de ticks del oro durante 1–2 semanas con `ATS_TickRecorder` (ver `fase-02-grabador-de-ticks.md`) y el mapa de costo contra movimiento por plazo y hora.
