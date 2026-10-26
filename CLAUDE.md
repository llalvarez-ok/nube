# Proyecto: canal de YouTube "Atajo IA"

Canal en español sobre IA práctica para el trabajo. Nombre real del canal: **Atajos IA** (los documentos dicen "Atajo IA"; usar "Atajos IA" en el contenido nuevo). ID: UC53Js7WmP8wd5OxJz8KxKJA, handle: @AtajosIAoficial, creado el 03/10/2026. Cuenta: canal.atajoia@gmail.com. El usuario habla español rioplatense (voseo); el contenido del canal usa español neutro con "tú".

- El plan completo está en `youtube/` (índice en `README.md`). Plan de ejecución: `youtube/09-plan-90-dias.md`.
- API de YouTube: `python herramientas/yt.py canal|videos|analitica N`, que lee `YT_CLIENT_ID`, `YT_CLIENT_SECRET` y `YT_REFRESH_TOKEN` del entorno. Nunca imprimas, guardes ni subas esos valores.
- El proyecto de API no está auditado: los videos subidos por API quedan bloqueados como privados. Hasta la auditoría, Claude deja los videos listos (metadatos, miniatura, horario) y el usuario los sube.
- Formato: videos de motion graphics producidos por código con el **motor v2** (`herramientas/motor.py`, guion en `produccion/<video>/guion.json`, catálogo en `sistema/motor-v2.md`). El motor v1 (`producir_video.py` + `escenas.json`) queda solo para video01. Nicho angostado el 25/10/2026 a **Excel + IA** (`canales/atajos-ia/ficha.md`, `ideas.md`, `productos.md`). Voz: voz sintética de Google Cloud TTS (`GOOGLE_TTS_API_KEY`), demos con documentos de ejemplo ficticios y respuestas de Claude (siempre aclarado en el video y la descripción).
- Flujo de publicación: el usuario sube el MP4 a mano (privado), Claude completa título, descripción, miniatura, subtítulos y playlists con `herramientas/completar_video.py <video>`, y el usuario publica o programa.
- Los guiones van en `youtube/guiones/` y las revisiones en `youtube/revisiones/AAAA-MM-DD.md`.

## Sistema de agentes (desde el 25/10/2026)
- Arquitectura y uso: `sistema/README.md`. Protocolo de debate: `sistema/protocolo-debate.md`; rúbricas: `sistema/rubricas.json`.
- 13 agentes en `.claude/agents/` y flujos en `.claude/skills/`: `/producir-video`, `/investigar-nicho`, `/nuevo-canal`, `/piloto-automatico`.
- Cada canal tiene `canales/<slug>/ficha.md` (fuente única para los agentes) y `aprendizajes.md` (memoria que escribe el analista).
- Estado de cada video: `python3 herramientas/pipeline.py estado`. Ninguna etapa avanza sin pasar la rúbrica (`pipeline.py evaluar`).

## Estado
- API conectada y verificada el 03/10/2026 (Data API y Analytics responden).
- Rutina semanal de los lunes creada (sesión nueva en cada disparo).
- Pendiente: auditoría de la API de YouTube (guía en `herramientas/auditoria-api.md`).
- video02 (primer video Excel + IA, motor v2): idea escalada (falta medir la demanda), guion aprobado en provisional (8,65), vista previa sin voz renderizada, metadatos, miniaturas y `publicacion.md` listos. Falta: `GOOGLE_TTS_API_KEY`, probar la plantilla en Excel para la web y la decisión del creador sobre la idea.
- video02 publicado el 26/10/2026 (https://youtu.be/drjrSlUxi78); Shorts programados 27, 29 y 31/10.
- video03 (dashboard en Excel con IA): idea y guion aprobados por el creador tras escalada, visual aprobado (8,0), empaque en borrador. Bloqueado hasta que el creador corra los prompts de `produccion/video03/respuestas-ia.md` en claude.ai gratis y pruebe la plantilla en Excel para la web (plazo 30/10); después: elegir ramas (`rama_elegida`), render con voz, qc, empaque final. Publicación prevista 03/11/2026 13:00 CDMX.
