# Proyecto: canal de YouTube "Atajo IA"

Canal en español sobre IA práctica para el trabajo. Nombre real del canal: **Atajos IA** (los documentos dicen "Atajo IA"; usar "Atajos IA" en el contenido nuevo). ID: UC53Js7WmP8wd5OxJz8KxKJA, handle: @AtajosIAoficial, creado el 03/10/2026. Cuenta: canal.atajoia@gmail.com. El usuario habla español rioplatense (voseo); el contenido del canal usa español neutro con "tú".

- El plan completo está en `youtube/` (índice en `README.md`). Plan de ejecución: `youtube/09-plan-90-dias.md`.
- API de YouTube: `python herramientas/yt.py canal|videos|analitica N`, que lee `YT_CLIENT_ID`, `YT_CLIENT_SECRET` y `YT_REFRESH_TOKEN` del entorno. Nunca imprimas, guardes ni subas esos valores.
- El proyecto de API no está auditado: los videos subidos por API quedan bloqueados como privados. Hasta la auditoría, Claude deja los videos listos (metadatos, miniatura, horario) y el usuario los sube.
- Formato decidido el 04/10/2026: videos explicativos animados producidos por Claude (`herramientas/producir_video.py`, escenas en `produccion/<video>/escenas.json`), voz sintética de Google Cloud TTS (`GOOGLE_TTS_API_KEY`), demos con documentos de ejemplo ficticios y respuestas de Claude (siempre aclarado en el video y la descripción).
- Flujo de publicación: el usuario sube el MP4 a mano (privado), Claude completa título, descripción, miniatura, subtítulos y playlists con `herramientas/completar_video.py <video>`, y el usuario publica o programa.
- Los guiones van en `youtube/guiones/` y las revisiones en `youtube/revisiones/AAAA-MM-DD.md`.

## Estado
- API conectada y verificada el 03/10/2026 (Data API y Analytics responden).
- Rutina semanal de los lunes creada (sesión nueva en cada disparo).
- Pendiente: auditoría de la API de YouTube (guía en `herramientas/auditoria-api.md`).
