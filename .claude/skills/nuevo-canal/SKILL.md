---
name: nuevo-canal
description: Crea un canal de YouTube nuevo de punta a punta con los agentes (investigación de nicho, identidad, marca, ficha, ideas y checklist de lanzamiento). Úsalo cuando pidan crear o lanzar un canal nuevo o un segundo canal.
---
# Crear un canal nuevo

Argumento opcional: el nicho o la idea del creador. Sin argumento, el nicho sale de la investigación.

1. **Investigación (con debate).** Llama al `investigador-mercado` en modo "informe de nicho". Después pide al `critico-retencion` y al `verificador` que ataquen el informe: ¿los RPM tienen fuente? ¿el nicho choca con la política de contenido inauténtico? ¿el formato animado puede producirlo con calidad? El `showrunner` decide el nicho (o pide otra ronda, máximo 2).
2. **Confirmación del creador.** Presenta el nicho elegido, 2 alternativas y el porqué en 5 líneas. Espera su "sí" antes de seguir: crear un canal es una decisión del creador.
3. **Fundación.** Llama al `estratega-canal` con el slug y el nicho: ficha, aprendizajes, nombre y handle, identidad visual renderizada, descripción, playlists y `lanzamiento.md`.
4. **Ideas.** Llama al `ideador` para las 30 primeras ideas (`canales/<slug>/ideas.md`) y al `investigador-mercado` para puntuar las 10 primeras con `investigar.py nicho`.
5. **Lo que hace el creador.** La API de YouTube no puede crear canales ni subir la foto de perfil. Pásale el checklist de `lanzamiento.md`: crear la cuenta y el canal, verificar el teléfono, handle, foto. Para conectar la API, `herramientas/README.md`.
6. **Configuración por API** (cuando el creador cargue las credenciales del canal nuevo): `python3 herramientas/configurar_canal.py` con los archivos del canal.
7. Commit y resumen.
