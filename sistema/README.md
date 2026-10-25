# Sistema de creación de contenido automatizado

> Un equipo de **13 agentes de IA** que investiga el mercado, crea el canal, idea, escribe, diseña, produce, verifica, empaqueta y aprende de los resultados. Los agentes **se cuestionan entre sí** con rúbricas medibles antes de que algo avance. Corre solo con una rutina programada y usa herramientas gratuitas. El creador hace solo lo que YouTube no deja automatizar: subir el MP4 y apretar "publicar".

- Qué es IATube, la narrativa del momento y los nichos que mejor pagan: [investigacion/2026-10-iatube-y-nichos.md](investigacion/2026-10-iatube-y-nichos.md)
- Cómo debaten los agentes: [protocolo-debate.md](protocolo-debate.md) · rúbricas: [rubricas.json](rubricas.json)

## 1. Cómo se usa

| Quieres… | Escribe en Claude Code |
|---|---|
| Producir el próximo video de punta a punta | `/producir-video video02 "Cómo usar IA en Excel"` |
| Retomar un video donde quedó | `/producir-video video02` |
| Saber qué nicho o qué temas convienen ahora | `/investigar-nicho` |
| Crear un canal nuevo | `/nuevo-canal` o `/nuevo-canal finanzas para autónomos` |
| Que el canal corra solo una semana | `/piloto-automatico` (o la rutina programada, sección 5) |
| Ver en qué etapa está cada video | `python3 herramientas/pipeline.py estado` |

## 2. El equipo

| Agente | Rol | Autor en | Critica en |
|---|---|---|---|
| `investigador-mercado` | Nichos, narrativa, outliers, demanda con datos de la API | informes | idea |
| `estratega-canal` | Funda canales: nicho, identidad, marca, ficha, lanzamiento | canal nuevo | — |
| `ideador` | Ideas con empaque (10 títulos, 3 miniaturas) y evidencia | idea | — |
| `guionista` | Guion de alta retención → `guion.json` (voz por beats + coreografía) | guion | — |
| `director-visual` | Variedad de escenas, imágenes libres, 3 miniaturas | visual | — |
| `productor` | Respuestas reales de IA, demo, voz, render, Shorts | render | — |
| `seo-empaquetador` | Títulos A/B, descripción, etiquetas, Shorts, publicación | empaque | — |
| `critico-retencion` | Abogado del diablo del CTR y la retención | — | idea, guion, visual, empaque |
| `verificador` | Datos, fuentes, políticas de YouTube (**veto**) | — | guion, empaque |
| `espectador` | Simula a la audiencia objetivo de la ficha | — | idea, guion, empaque |
| `editor-qc` | Revisa escenas, audio, subtítulos, pronunciación (**veto técnico**) | — | visual, qc |
| `showrunner` | Juez: resuelve contradicciones y escribe el brief de revisión | — | todas |
| `analista` | Mide lo publicado y escribe reglas nuevas | revisiones | (ajusta rúbricas) |

Las definiciones están en [`.claude/agents/`](../.claude/agents/) y los flujos en [`.claude/skills/`](../.claude/skills/).

## 3. El flujo de un video

```
 investigador ─▶ IDEA ─▶ GUION ─▶ VISUAL ─▶ RENDER ─▶ QC ─▶ EMPAQUE ─▶ LISTO ─▶ (creador sube) ─▶ PUBLICADO ─▶ analista
                  ▲  debate  ▲ debate  ▲ debate          ▲ debate ▲ debate                                       │
                  └──────────────────────────── aprendizajes.md ◀────────────────────────────────────────────────┘
```

| Etapa | Artefacto en `produccion/<video>/` | Control objetivo | Umbral |
|---|---|---|---|
| idea | `idea.md` | evidencia de `investigar.py` | 8,0 |
| guion | `guion.json` | `puntuar_guion.py` ≥ 80 | 8,5 |
| visual | `guion.json`, `miniatura*.html` | capturas `motor.py --cuadros` | 8,0 |
| render | `<video>.mp4`, `.srt`, `capitulos.txt` | — | — |
| qc | — | `qc_video.py` sin errores + hoja de contactos | 9,0 |
| empaque | `metadatos.json`, `miniatura.png`, `publicacion.md`, `shorts/` | — | 8,5 |

## 4. Herramientas (`herramientas/`)

| Script | Qué hace | Necesita |
|---|---|---|
| `pipeline.py` | Estado de cada video, rondas de debate, notas y escaladas | — |
| `investigar.py` | Autocompletado de YouTube, videos outlier, puntaje de oportunidad, populares por país | API de YouTube (OAuth del canal o `YT_API_KEY`) |
| `puntuar_guion.py` | Linter de retención: hook, bucle abierto, ritmo, escenas largas, frases largas, relleno, CTA, promesa | — |
| `motor.py` | **Motor v2**: motion graphics cuadro por cuadro (GSAP + Chromium): réplica animada de Excel con cursor, fórmulas que se escriben, cámara con zoom, panel y chat de IA, gráficos, transiciones, efectos de sonido sintetizados, voz por beat sincronizada, música con *ducking*, subtítulos y capítulos. Catálogo: [motor-v2.md](motor-v2.md) | `GOOGLE_TTS_API_KEY` |
| `producir_video.py` | Motor v1 (diapositivas con zoom), solo para video01 | `GOOGLE_TTS_API_KEY` |
| `qc_video.py` | Resolución, fps, −14 LUFS, pico, silencios, negro, imagen congelada, subtítulos, hoja de contactos | — |
| `shorts.py` | Short vertical 1080×1920 con fondo desenfocado, título y subtítulos quemados | — |
| `recursos.py` | Imágenes con licencia libre (Openverse sin clave, Pexels con clave gratis) y registro de créditos | — |
| `completar_video.py` | Carga título, descripción, miniatura, subtítulos y playlists de un video subido | OAuth del canal |
| `configurar_canal.py` | Banner, descripción, palabras clave, marca de agua y playlists del canal | OAuth del canal |

El motor v2 acepta `marca` (nombre y color de acento) y `musica` en `guion.json`, así que sirve para otros canales.

## 5. Automatización

**Rutina programada (sesión nueva en cada disparo):**

| Cuándo | Prompt de la rutina | Resultado |
|---|---|---|
| Lunes 8:00 | `/piloto-automatico` | Analítica + revisión semanal + banco de ideas + producción de los 2 videos de la semana |
| Jueves 8:00 | `/producir-video` | Retoma lo que quedó a medias (escaladas resueltas, renders pendientes) |
| Día 1 de cada mes | `/investigar-nicho` (informe mensual) | Narrativa y nichos actualizados en `sistema/investigacion/` |

Cada corrida termina con un commit y un `produccion/AAAA-MM-DD-resumen.md`, que es lo único que el creador necesita leer.

**Qué queda en manos del creador (y por qué):**

| Tarea | Por qué no se automatiza |
|---|---|
| Crear la cuenta de Google y el canal, verificar el teléfono, foto de perfil | La API de YouTube no lo permite |
| Subir el MP4 (como privado) y publicar o programar | El proyecto de API no está auditado: lo que se sube por API queda bloqueado como privado. Al aprobarse la auditoría (`herramientas/auditoria-api.md`), el productor puede subir y programar solo |
| Decidir en las escaladas (3 rondas sin aprobar) | Es una decisión editorial |
| Aprobar un canal o un cambio de estrategia | Es una decisión de negocio |

## 6. Variables de entorno

| Variable | Para qué | Costo |
|---|---|---|
| `YT_CLIENT_ID`, `YT_CLIENT_SECRET`, `YT_REFRESH_TOKEN` | API del canal (ya configuradas) | Gratis |
| `GOOGLE_TTS_API_KEY` | Voz Chirp 3 HD | Gratis hasta 1 M de caracteres/mes |
| `YT_API_KEY` (opcional) | Investigación sin gastar el OAuth del canal | Gratis |
| `PEXELS_API_KEY` (opcional) | Fotos de Pexels | Gratis |

**Red:** el entorno en la nube tiene que permitir `suggestqueries.google.com` (autocompletado) y `api.openverse.org` (imágenes libres), y `api.pexels.com` si se usa Pexels. Se agregan en el menú del entorno → **Edit** → *Network access* → *Allowed domains* ([guía](https://code.claude.com/docs/en/cloud-environments#network-access)).

## 7. Calidad: por qué estos videos no son "IA basura"

1. Cada idea tiene **evidencia de demanda** y un **ángulo propio** antes de escribirse.
2. Cada guion pasa un linter de retención y **3 críticos con incentivos opuestos**.
3. Cada dato real tiene **fuente verificada**; las demos son ficticias y se declara; las respuestas de IA en pantalla son reales.
4. Cada render pasa un **QC técnico** medible y una revisión visual.
5. Cada video publicado **enseña algo** al sistema (aprendizajes.md) y cambia cómo se hace el siguiente.
6. Formato de serie con guiones únicos: lo opuesto a la "producción en masa" que penaliza la política de contenido inauténtico.
