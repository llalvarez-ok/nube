# Proyecto: canal de YouTube "Atajo IA"

Canal en español sobre IA práctica para el trabajo. Cuenta del canal: canal.atajoia@gmail.com. El usuario habla español rioplatense (voseo); el contenido del canal usa español neutro con "tú".

- El plan completo está en `youtube/` (índice en `README.md`). Plan de ejecución: `youtube/09-plan-90-dias.md`.
- API de YouTube: `python herramientas/yt.py canal|videos|analitica N`, que lee `YT_CLIENT_ID`, `YT_CLIENT_SECRET` y `YT_REFRESH_TOKEN` del entorno. Nunca imprimas, guardes ni subas esos valores.
- El proyecto de API no está auditado: los videos subidos por API quedan bloqueados como privados. Hasta la auditoría, Claude deja los videos listos (metadatos, miniatura, horario) y el usuario los sube.
- Lo que hace el usuario: grabar las demos y la voz, y publicar. Lo que hace Claude: guiones, empaque, revisiones semanales y mensuales (`youtube/08-analitica.md`) y lead magnets.
- Los guiones van en `youtube/guiones/` y las revisiones en `youtube/revisiones/AAAA-MM-DD.md`.

## Pendiente al conectar la API
1. Verificar el canal con `yt.py canal`.
2. Crear una rutina semanal (lunes): métricas, revisión semanal y guiones de la semana, con commit.
3. Guiar al usuario para pedir la auditoría de la API de YouTube.
