#!/usr/bin/env python3
"""Autoriza a Atajo IA a usar la API de YouTube y muestra las 3 credenciales.

Se corre UNA vez, en tu computadora (no en la nube), con Python 3.8+ y sin
instalar nada extra:

    python obtener_token.py   (busca solo el client_secret*.json de la carpeta)

El navegador se abre: elegí la cuenta canal.atajoia@gmail.com y, si te lo
pregunta, el canal "Atajo IA". Al terminar, el script imprime YT_CLIENT_ID,
YT_CLIENT_SECRET y YT_REFRESH_TOKEN para cargarlos en el entorno de la nube.
No los pegues en el chat.
"""

import base64
import glob
import hashlib
import http.server
import json
import os
import secrets
import sys
import urllib.error
import urllib.parse
import urllib.request
import webbrowser

SCOPES = [
    "https://www.googleapis.com/auth/youtube",  # subir, editar, playlists, miniaturas
    "https://www.googleapis.com/auth/youtube.force-ssl",  # comentarios
    "https://www.googleapis.com/auth/yt-analytics.readonly",  # estadísticas
]
AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"


def cargar_cliente(ruta):
    with open(ruta, encoding="utf-8") as f:
        datos = json.load(f)
    cliente = datos.get("installed") or datos.get("web")
    if not cliente:
        sys.exit("El JSON no parece un cliente OAuth de Google. Descargalo de nuevo desde Credenciales.")
    if "installed" not in datos:
        print("Aviso: el cliente no es de tipo 'App de escritorio'; puede fallar el redireccionamiento.")
    return cliente["client_id"], cliente["client_secret"]


def esperar_codigo(estado_esperado):
    resultado = {}

    class Manejador(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            if "code" not in params and "error" not in params:
                self.send_response(404)
                self.end_headers()
                return
            resultado.update({k: v[0] for k, v in params.items()})
            ok = "code" in params and params.get("state", [""])[0] == estado_esperado
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            mensaje = "Listo. Ya podés cerrar esta pestaña y volver a la terminal." if ok else "Algo falló. Mirá la terminal."
            self.wfile.write(f"<h2>{mensaje}</h2>".encode("utf-8"))

        def log_message(self, *args):
            pass

    servidor = http.server.HTTPServer(("127.0.0.1", 0), Manejador)
    return servidor, resultado


def main():
    ruta = sys.argv[1] if len(sys.argv) > 1 else ""
    if not os.path.isfile(ruta):
        candidatos = glob.glob("client_secret*.json")
        if len(candidatos) != 1:
            sys.exit(
                f"No encontré el archivo '{ruta}'. JSON en esta carpeta: {glob.glob('*.json') or 'ninguno'}\n"
                "Pasá el nombre exacto: python obtener_token.py NOMBRE.json"
            )
        ruta = candidatos[0]
        print(f"Usando {ruta}")
    client_id, client_secret = cargar_cliente(ruta)

    verificador = secrets.token_urlsafe(64)
    desafio = base64.urlsafe_b64encode(hashlib.sha256(verificador.encode()).digest()).rstrip(b"=").decode()
    estado = secrets.token_urlsafe(16)

    servidor, resultado = esperar_codigo(estado)
    redirect_uri = f"http://127.0.0.1:{servidor.server_port}/"
    url = AUTH_URL + "?" + urllib.parse.urlencode({
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": " ".join(SCOPES),
        "access_type": "offline",
        "prompt": "consent",
        "state": estado,
        "code_challenge": desafio,
        "code_challenge_method": "S256",
    })

    print("\nAbriendo el navegador. Si no se abre, copiá esta dirección:\n")
    print(url + "\n")
    print("Si aparece 'Google no verificó esta app': Configuración avanzada → Ir a ... (no seguro).")
    print("Es tu propia app; el aviso es normal.\n")
    webbrowser.open(url)

    while not resultado:
        servidor.handle_request()
    servidor.server_close()

    if "error" in resultado:
        sys.exit(f"Google devolvió un error: {resultado['error']}")
    if resultado.get("state") != estado:
        sys.exit("El parámetro 'state' no coincide; por seguridad se cancela. Volvé a correr el script.")

    cuerpo = urllib.parse.urlencode({
        "code": resultado["code"],
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
        "code_verifier": verificador,
    }).encode()
    try:
        with urllib.request.urlopen(urllib.request.Request(TOKEN_URL, data=cuerpo)) as r:
            tokens = json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"No se pudo obtener el token: {e.read().decode()}")

    refresh = tokens.get("refresh_token")
    if not refresh:
        sys.exit("Google no devolvió refresh_token. Quitá el acceso de la app en myaccount.google.com/permissions y repetí.")

    # Verificación: qué canal quedó autorizado.
    req = urllib.request.Request(
        "https://www.googleapis.com/youtube/v3/channels?part=snippet&mine=true",
        headers={"Authorization": f"Bearer {tokens['access_token']}"},
    )
    try:
        with urllib.request.urlopen(req) as r:
            items = json.load(r).get("items", [])
        canal = items[0]["snippet"]["title"] if items else "(ningún canal: ¿elegiste la cuenta correcta?)"
    except urllib.error.HTTPError as e:
        canal = f"(no se pudo verificar: {e.code}. ¿Activaste 'YouTube Data API v3' en el proyecto?)"

    print("=" * 70)
    print(f"Canal autorizado: {canal}")
    print("=" * 70)
    print("Cargá estas 3 variables en el entorno de la nube (NO en el chat):\n")
    print(f"YT_CLIENT_ID={client_id}")
    print(f"YT_CLIENT_SECRET={client_secret}")
    print(f"YT_REFRESH_TOKEN={refresh}")
    print("\nDespués cerrá esta terminal y borrá el JSON descargado si no lo vas a usar.")


if __name__ == "__main__":
    main()
