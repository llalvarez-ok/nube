#!/usr/bin/env python3
"""Aplica la configuración completa del canal Atajos IA por API (idempotente).

    python3 herramientas/configurar_canal.py            # aplica
    python3 herramientas/configurar_canal.py --simular  # solo muestra qué haría

Configura: descripción, palabras clave, país, idioma, banner, marca de agua
(botón de suscripción en los videos) y playlists por pilar. La foto de perfil
y el handle no se pueden cambiar por API.
"""

import json
import os
import sys
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(__file__))
from yt import DATA, canal, get, token_de_acceso  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD = "https://www.googleapis.com/upload/youtube/v3/"

DESCRIPCION = """Aprende a usar la inteligencia artificial para trabajar menos y mejor.

En Atajos IA te muestro flujos reales, paso a paso y con el cronómetro en pantalla, para que hagas en minutos lo que antes te llevaba horas: resumir documentos, armar presentaciones, responder correos, analizar datos en Excel y mucho más.

✔ Tutoriales paso a paso con ChatGPT, Gemini, Claude, NotebookLM y otras herramientas
✔ Comparativas honestas: qué IA sirve y cuál no
✔ IA para tu profesión: docentes, contadores, abogados, vendedores, pymes
✔ Plantillas y prompts gratis en cada video

Sin humo, sin tecnicismos. Nuevo atajo cada martes y viernes.

📩 Contacto: canal.atajoia@gmail.com"""

PALABRAS_CLAVE = (
    '"inteligencia artificial" IA ChatGPT "IA para el trabajo" productividad '
    '"herramientas de IA" "tutorial ChatGPT" Gemini Claude NotebookLM Excel '
    '"automatizar tareas" prompts "IA gratis" "IA en español" oficina emprendedores'
)

PLAYLISTS = [
    ("Empieza aquí: lo mejor de Atajos IA",
     "Los videos para empezar a usar la IA en tu trabajo desde cero. Si es tu primera vez en el canal, arranca por acá."),
    ("Flujos paso a paso con IA",
     "Tutoriales completos para hacer tareas de oficina con inteligencia artificial: PDFs, correos, presentaciones, Excel, informes y más."),
    ("Pruebas y comparativas de IA",
     "Probamos herramientas de inteligencia artificial con tareas reales y te decimos cuál conviene según tu caso. Comparativas honestas, sin patrocinio oculto."),
    ("IA para tu profesión",
     "Cómo usar la inteligencia artificial en tu trabajo: docentes, contadores, abogados, vendedores, recursos humanos, inmobiliarias, pymes y más."),
    ("Novedades de IA que sí sirven",
     "Lo nuevo en inteligencia artificial, probado y explicado: solo lo que te sirve para trabajar mejor."),
]


def enviar(metodo, url, token, cuerpo=None, tipo="application/json"):
    datos = json.dumps(cuerpo).encode() if isinstance(cuerpo, (dict, list)) else cuerpo
    req = urllib.request.Request(url, data=datos, method=metodo,
                                 headers={"Authorization": f"Bearer {token}", "Content-Type": tipo})
    try:
        with urllib.request.urlopen(req) as r:
            texto = r.read().decode()
            return json.loads(texto) if texto else {}
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"{e.code}: {e.read().decode()[:500]}") from None


def paso(nombre, funcion):
    try:
        print(f"✔ {nombre}: {funcion()}")
        return True
    except (Exception, SystemExit) as e:  # cada paso es independiente
        print(f"✘ {nombre}: {e}")
        return False


def main():
    simular = "--simular" in sys.argv
    token = token_de_acceso()
    c = canal(token)["items"][0]
    canal_id = c["id"]
    print(f"Canal: {c['snippet']['title']} ({canal_id})")

    def banner():
        with open(os.path.join(RAIZ, "marca", "banner.jpg"), "rb") as f:
            imagen = f.read()
        if simular:
            return f"subiría banner.jpg ({len(imagen) // 1024} KB)"
        r = enviar("POST", UPLOAD + "channelBanners/insert?uploadType=media", token, imagen, "image/jpeg")
        return r["url"]

    url_banner = {}

    def subir_banner():
        resultado = banner()
        url_banner["url"] = resultado
        return resultado if simular else "subido"

    def branding():
        actual = get(DATA + "channels", {"part": "brandingSettings", "id": canal_id}, token)["items"][0]
        bs = actual.get("brandingSettings", {})
        bs.setdefault("channel", {}).update({
            "description": DESCRIPCION,
            "keywords": PALABRAS_CLAVE,
            "country": "AR",
            "defaultLanguage": "es",
        })
        if url_banner.get("url", "").startswith("http"):
            bs.setdefault("image", {})["bannerExternalUrl"] = url_banner["url"]
        if simular:
            return json.dumps(bs["channel"], ensure_ascii=False)[:200] + "…"
        enviar("PUT", DATA + "channels?part=brandingSettings", token, {"id": canal_id, "brandingSettings": bs})
        return "descripción, palabras clave, país AR, idioma es" + (", banner" if "url" in url_banner else "")

    def marca_de_agua():
        with open(os.path.join(RAIZ, "marca", "marca-de-agua.png"), "rb") as f:
            imagen = f.read()
        if simular:
            return "subiría marca-de-agua.png"
        meta = json.dumps({"timing": {"type": "offsetFromStart", "offsetMs": 0},
                           "position": {"type": "corner", "cornerPosition": "topRight"}}).encode()
        limite = b"atajosia_limite"
        cuerpo = (b"--" + limite + b"\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n" + meta +
                  b"\r\n--" + limite + b"\r\nContent-Type: image/png\r\n\r\n" + imagen +
                  b"\r\n--" + limite + b"--")
        enviar("POST", UPLOAD + f"watermarks/set?channelId={canal_id}&uploadType=multipart", token,
               cuerpo, "multipart/related; boundary=" + limite.decode())
        return "botón de suscripción en todos los videos (arriba a la derecha)"

    def playlists():
        existentes = get(DATA + "playlists", {"part": "snippet", "mine": "true", "maxResults": 50}, token)
        titulos = {p["snippet"]["title"] for p in existentes.get("items", [])}
        creadas = []
        for titulo, descripcion in PLAYLISTS:
            if titulo in titulos:
                continue
            if not simular:
                enviar("POST", DATA + "playlists?part=snippet,status", token, {
                    "snippet": {"title": titulo, "description": descripcion, "defaultLanguage": "es"},
                    "status": {"privacyStatus": "public"},
                })
            creadas.append(titulo)
        return f"creadas {len(creadas)}: {creadas}" if creadas else "ya existían todas"

    resultados = [
        paso("Banner", subir_banner),
        paso("Descripción, palabras clave, país e idioma", branding),
        paso("Marca de agua", marca_de_agua),
        paso("Playlists", playlists),
    ]
    print(("Simulación" if simular else "Configuración") + f" terminada: {sum(resultados)}/{len(resultados)} pasos OK")


if __name__ == "__main__":
    main()
