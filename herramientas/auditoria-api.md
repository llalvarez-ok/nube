# Pedir la auditoría de la API de YouTube

**Para qué sirve:** hoy, los videos que se suben por API desde tu proyecto quedan **privados y bloqueados**. No se pueden hacer públicos, ni por API ni desde YouTube Studio. Es una regla de Google para todo proyecto creado después del 28/07/2020 que no fue auditado.

Leer métricas, editar títulos y descripciones y responder comentarios **funciona igual**, sin auditoría. Lo único bloqueado es publicar lo que sube la API.

**Qué esperar:**
- Google puede tardar **varias semanas** en responder.
- A veces pide más información o un video que muestre cómo se usa la herramienta.
- Puede rechazarla. Si pasa eso, no se pierde nada: seguís subiendo vos los videos y yo dejo todo lo demás listo.

## Paso 1 · Datos que vas a necesitar
- **Número del proyecto:** en Google Cloud Console, entrá a la página principal del proyecto (*Panel*). Ahí figura el "Número de proyecto".
- **ID del canal:** `UC53Js7WmP8wd5OxJz8KxKJA`
- **Email de contacto:** canal.atajoia@gmail.com

## Paso 2 · Abrir el formulario
Con la cuenta del canal, entrá a:
https://support.google.com/youtube/contact/yt_api_form

Elegí la opción de **auditoría (Audit)**, no la de aumento de cuota.

## Paso 3 · Respuestas sugeridas
El formulario está en inglés. Podés copiar estos textos y ajustarlos si te piden algo distinto.

**Describe your use case / How does your API client use YouTube API Services?**
> Internal tool used only by the owner of a single YouTube channel ("Atajos IA", channel ID UC53Js7WmP8wd5OxJz8KxKJA) to manage their own content. It uploads the owner's own videos (videos.insert) with title, description, chapters, scheduled publish time and custom thumbnail (thumbnails.set); manages the channel's own playlists; reads the channel's own analytics (YouTube Analytics API) to prepare weekly performance reviews; and reads and replies to comments on the channel's own videos. The tool is not offered to any other user, does not access other channels' private data, and does not store data beyond the weekly reports kept in the owner's private repository.

**Who are your users?**
> Only the channel owner (1 user, authenticated with OAuth 2.0, desktop client).

**Which API services and endpoints?**
> YouTube Data API v3: videos.insert, videos.update, videos.list, thumbnails.set, playlists.*, playlistItems.*, channels.list, commentThreads.list, comments.insert. YouTube Analytics API: reports.query.

**Data storage / retention**
> Analytics aggregates are stored in the owner's private repository as weekly reports. No personal data of viewers is stored. OAuth tokens are stored as encrypted environment variables and can be revoked at any time from the Google account permissions page.

**Expected quota usage**
> Around 2–3 uploads per week plus daily read requests; well within the default 10,000 units/day.

## Paso 4 · Si te piden política de privacidad o un video
- **Política de privacidad:** avisame y armo una página simple en español e inglés para publicar.
- **Video (screencast):** avisame y te preparo un guion de 2 minutos para grabar la pantalla mostrando el flujo.

## Paso 5 · Cuando responda Google
Avisame qué respondieron. Si aprueban, actualizo la rutina para que yo suba y programe los videos.
