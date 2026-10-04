# Sistema autónomo adaptativo de trading (MT5)

Proyecto independiente del canal de YouTube. Se trabaja por fases (BUILD → TEST → AUDIT → FIX → VALIDATE).

- Fase 1 — Arquitectura y viabilidad: [`docs/fase-01-documento-tecnico.md`](docs/fase-01-documento-tecnico.md) (decisiones del 04/10 en §26)
- Fase 2 / Etapa 0 — Grabador de ticks y mapa de costos: [`docs/fase-02-grabador-de-ticks.md`](docs/fase-02-grabador-de-ticks.md)
- Fase 3 (adelantada) — Features, simulador y línea base: [`docs/fase-03-features-y-simulador.md`](docs/fase-03-features-y-simulador.md)

Estructura:

- `mql5/` — código que corre dentro de MetaTrader 5 (se copia a la carpeta de datos del terminal).
- `research/` — investigación en Python (fuera de la ruta de ejecución). Tests: `python -m pytest research/tests`.

Principio rector: el sistema puede volverse más conservador por sí solo (reducir riesgo, pausar, detenerse), pero nunca más agresivo sin validación y aprobación humana.
