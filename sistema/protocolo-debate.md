# Protocolo de debate entre agentes

> Ningún artefacto avanza porque su autor lo considere bueno. Avanza cuando **críticos independientes** lo puntúan por encima del umbral en una rúbrica medible, sin vetos, y un juez resolvió sus contradicciones.

## La ronda

```
  ┌──────────┐   artefacto    ┌────────────────────────────┐
  │  AUTOR   │ ─────────────▶ │ CONTROL OBJETIVO (scripts) │── no pasa ──┐
  └──────────┘                └────────────────────────────┘             │
       ▲                                  │ pasa                         │
       │                                  ▼                              │
       │            ┌────────────┬────────────┬────────────┐             │
       │            │ CRÍTICO 1  │ CRÍTICO 2  │ CRÍTICO 3  │ en paralelo,│
       │            │ (JSON)     │ (JSON)     │ (JSON)     │ a ciegas    │
       │            └────────────┴─────┬──────┴────────────┘             │
       │                               ▼                                 │
       │                 pipeline.py evaluar (rúbrica)                   │
       │            ┌──────────────────┼───────────────────┐             │
       │       APROBADO             REVISAR             ESCALADO         │
       │      (etapa sig.)             │            (ronda 3: decide     │
       │                               ▼              el creador)        │
       │                         ┌───────────┐                           │
       └──── brief de revisión ──│ SHOWRUNNER│◀──────────────────────────┘
             + réplicas          └───────────┘
```

1. **Autor:** produce el artefacto. Desde la ronda 2 responde **cada** objeción en `debate.md`: *aceptada* (qué cambió) o *rechazada* (con un argumento basado en datos, en la ficha o en los aprendizajes del canal).
2. **Control objetivo:** lo medible se mide con scripts antes de gastar críticos (`puntuar_guion.py` ≥ 80; `qc_video.py` sin errores).
3. **Críticos a ciegas y en paralelo:** cada uno puntúa solo sus criterios y no ve las notas de los demás, para evitar el efecto manada.
4. **Rúbrica:** `pipeline.py evaluar` promedia por criterio, pondera y aplica mínimos y vetos (`sistema/rubricas.json`).
5. **Showrunner:** si hay que revisar, resuelve contradicciones con esta prioridad: **veracidad y políticas > promesa cumplida > retención > estilo**. Decide las réplicas del autor y escribe un brief con 3-6 correcciones obligatorias y lo que no hay que tocar.
6. **Máximo 3 rondas.** Si no aprueba, se escala al creador con una recomendación: aprobar con pendientes documentados, rehacer desde la etapa anterior o descartar.

## Quién cuestiona a quién

| Etapa | Autor | Críticos (criterios) | Umbral |
|---|---|---|---|
| idea | ideador | investigador-mercado (demanda, rpm, diferenciación) · crítico-retención (empaque) · espectador (empaque, encaje) | 8,0 |
| guion | guionista | crítico-retención (hook, ritmo, promesa, claridad) · verificador (veracidad, **veto**) · espectador (claridad, promesa) | 8,5 |
| visual | director-visual | crítico-retención (variedad) · editor-qc (legibilidad, coherencia, marca, variedad) | 8,0 |
| qc | productor | editor-qc (técnico **veto**, sincronía, pronunciación) | 9,0 |
| empaque | seo-empaquetador | crítico-retención (ctr, búsqueda) · verificador (honestidad **veto**, completitud) · espectador (ctr) | 8,5 |

Por diseño, los críticos tiran en direcciones opuestas: el **crítico de retención** quiere ir más rápido y prometer más; el **verificador** quiere más precisión y menos promesa; el **espectador** quiere entender sin esfuerzo. La versión que sobrevive a los tres es mejor que la que cualquiera de ellos escribiría solo.

## El ciclo largo: aprendizaje

El **analista** mide cada video publicado (2, 7 y 28 días) y escribe una regla por video en `canales/<canal>/aprendizajes.md`. Todos los autores y críticos leen ese archivo antes de trabajar. Si un criterio de la rúbrica no predice el rendimiento real (por ejemplo, guiones con hook 9 que igual pierden el 50 % a los 30 s), el analista propone cambiar el peso o el mínimo en `rubricas.json`.

## Registro

Todo queda en `produccion/<video>/`: `estado.json` (etapa, notas, motivos), `rondas/*.json` (las críticas crudas) y `debate.md` (respuestas del autor y decisiones del showrunner). Así se puede auditar por qué un video salió como salió.
