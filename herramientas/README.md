# Conectar el canal a la API de YouTube

Hecho: cuenta `canal.atajoia@gmail.com`, canal, pantalla de consentimiento en producción y cliente OAuth de escritorio.

## 1. Activar las 2 APIs (Google Cloud Console, con la cuenta del canal)
1. Entrá en **APIs y servicios → Biblioteca**.
2. Buscá **YouTube Data API v3** y hacé clic en **Habilitar**.
3. Buscá **YouTube Analytics API** y hacé clic en **Habilitar**.

## 2. Descargar el JSON del cliente
En **APIs y servicios → Credenciales**, buscá tu cliente de escritorio y hacé clic en el ícono de descarga. Se baja un archivo `client_secret_XXXX.json`.

## 3. Correr el script en tu computadora
1. Si no tenés Python, instalalo desde https://www.python.org/downloads/. En Windows, marcá "Add Python to PATH" durante la instalación.
2. Descargá [`obtener_token.py`](obtener_token.py) en la misma carpeta que el JSON.
3. Abrí una terminal en esa carpeta y corré:
   ```
   python obtener_token.py client_secret_XXXX.json
   ```
4. En el navegador:
   - Elegí **canal.atajoia@gmail.com**.
   - Si te pregunta por un canal o una cuenta de marca, elegí **Atajo IA**.
   - Si aparece "Google no verificó esta app", hacé clic en **Configuración avanzada → Ir a … (no seguro)**. Es tu propia app.
   - Aceptá los permisos.
5. La terminal muestra **"Canal autorizado: …"** y las 3 variables.

## 4. Cargar las variables en la nube (no en el chat)
1. En la sesión de Claude, abrí el menú del entorno en la nube (en la barra del título) y hacé clic en **Edit**.
2. En las variables de entorno, pegá las tres líneas:
   ```
   YT_CLIENT_ID=...
   YT_CLIENT_SECRET=...
   YT_REFRESH_TOKEN=...
   ```
3. Guardá y abrí una sesión nueva. Las variables solo se leen al iniciar.

## 5. Verificación (la hace Claude)
```
python herramientas/yt.py canal
```

## Seguridad
- El *refresh token* da acceso al canal. **No lo compartas** y no lo subas al repo.
- Para revocar el acceso en cualquier momento, entrá con la cuenta del canal en https://myaccount.google.com/permissions y quitá la app.
