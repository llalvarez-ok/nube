---
name: producir-video
description: Orquesta la producción completa de un video con el equipo de agentes y el protocolo de debate (idea → guion → visual → render → qc → empaque → listo). Úsalo cuando pidan producir, continuar o retomar un video, o "el próximo video".
---
# Producir un video con el equipo de agentes

Actúas como **orquestador**. No escribes el contenido tú: lo delegas a los agentes de `.claude/agents/` y haces cumplir el protocolo de `sistema/protocolo-debate.md`. Argumento: `<video> [tema]` (por ejemplo `video02 "Cómo usar IA en Excel"`). Sin argumento, continúa el video más avanzado que no esté `listo`, o toma la mejor idea aprobada.

## 0. Preparar
- `python3 herramientas/pipeline.py estado` para ver todos los videos.
- Si el video no existe: `python3 herramientas/pipeline.py nuevo <video> "<tema>"`.
- `python3 herramientas/pipeline.py siguiente <video>` te dice la etapa, el autor, los críticos y las objeciones pendientes.

## 1. Ciclo de cada etapa con debate (idea, guion, visual, qc, empaque)
1. **Autor.** Llama al agente autor con: video, etapa, ruta del artefacto y, desde la ronda 2, el brief del showrunner de `produccion/<video>/debate.md`. Pídele que responda cada objeción (aceptada/rechazada con argumento).
2. **Controles objetivos.** guion: `puntuar_guion.py` ≥ 80 y `plantilla_xlsx.py <video> --verificar` sin diferencias (si no, vuelve al autor sin gastar críticos). qc: `qc_video.py` sin errores.
3. **Críticos en paralelo** (un solo mensaje con varias llamadas al Agent tool). Cada uno recibe el artefacto y la rúbrica de la etapa, **no** ve las notas de los otros. Cada uno devuelve un JSON.
4. **Ronda.** Junta los JSON en `produccion/<video>/rondas/<etapa>-<n>.json` como `{"evaluaciones": [...]}` y corre `python3 herramientas/pipeline.py evaluar <video> <etapa> <archivo>`.
5. **Showrunner.** Si el resultado es REVISAR, llama al showrunner con las evaluaciones: resuelve contradicciones y escribe el brief en debate.md. Vuelve al paso 1.
   Si es APROBADO, pasa a la etapa siguiente. Si es ESCALADO, el showrunner deja su recomendación y te detienes: avisa al creador.

## 2. Etapas sin debate
- **render:** agente `productor` (respuestas reales pendientes, documento de demo, `producir_video.py`, luego `pipeline.py marcar <video> render`). Sin `GOOGLE_TTS_API_KEY`, renderiza `--sin-voz`, avisa y detente después del qc visual.
- **listo:** el `seo-empaquetador` dejó `publicacion.md`; el productor genera los 3 Shorts. `pipeline.py marcar <video> listo` solo cuando el creador confirme que lo subió.

## 3. Cierre
- Commit de los artefactos (idea.md, guion.json, debate.md, rondas/, metadatos.json, miniaturas, srt, capitulos.txt, publicacion.md, estado.json). Los MP4 no se suben.
- Resumen para el creador: etapa alcanzada, nota de cada etapa, decisiones importantes del showrunner y qué tiene que hacer él (subir el MP4, publicar).

## Reglas
- Máximo 3 rondas por etapa. No "aprobar por cansancio": si no pasa, escala.
- Nunca saltees al verificador. Nunca subas un video ni cambies su privacidad por API (proyecto no auditado: ver CLAUDE.md).
- Si un agente devuelve algo que no es JSON válido en una crítica, pídeselo de nuevo una vez; si vuelve a fallar, registra la crítica a mano con sus puntajes.
