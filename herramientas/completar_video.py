#!/usr/bin/env python3
"""Completa por API un video que el creador subió a mano (sin auditoría hace falta solo editar).

    python3 herramientas/completar_video.py video01              # usa el último video subido
    python3 herramientas/completar_video.py video01 VIDEO_ID
    python3 herramientas/completar_video.py video01 --simular

Aplica desde produccion/<video>/: título, descripción (con capítulos.txt), etiquetas,
categoría, idioma, miniatura.png, subtítulos <video>.srt y playlists de metadatos.json.
No cambia la privacidad: la publicación la decide el creador.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from configurar_canal import UPLOAD, enviar, paso  # noqa: E402
from yt import DATA, get, token_de_acceso, videos  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def multipart(meta, datos, tipo):
    limite = b"atajosia_limite"
    cuerpo = (b"--" + limite + b"\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n" +
              json.dumps(meta).encode() + b"\r\n--" + limite + b"\r\nContent-Type: " + tipo.encode() +
              b"\r\n\r\n" + datos + b"\r\n--" + limite + b"--")
    return cuerpo, "multipart/related; boundary=" + limite.decode()


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit(__doc__)
    nombre = args[0]
    simular = "--simular" in sys.argv
    base = os.path.join(RAIZ, "produccion", nombre)
    meta = json.load(open(os.path.join(base, "metadatos.json"), encoding="utf-8"))
    token = token_de_acceso()

    if len(args) > 1:
        video_id = args[1]
    else:
        subidos = videos(token, 5).get("items", [])
        if not subidos:
            sys.exit("No hay videos subidos en el canal.")
        subidos.sort(key=lambda v: v["snippet"]["publishedAt"], reverse=True)
        video_id = subidos[0]["id"]
    actual = get(DATA + "videos", {"part": "snippet,status", "id": video_id}, token)["items"][0]
    print(f"Video: {video_id} · subido como «{actual['snippet']['title']}» · {actual['status']['privacyStatus']}")

    capitulos = open(os.path.join(base, "capitulos.txt"), encoding="utf-8").read().strip()
    descripcion = meta["descripcion"].replace("{capitulos}", capitulos)

    def textos():
        snippet = {
            "title": meta["titulo"], "description": descripcion, "tags": meta["etiquetas"],
            "categoryId": meta["categoria"], "defaultLanguage": "es", "defaultAudioLanguage": "es",
        }
        status = dict(actual["status"])
        status.update({"selfDeclaredMadeForKids": False, "embeddable": True})
        for solo_lectura in ("uploadStatus", "failureReason", "rejectionReason", "madeForKids"):
            status.pop(solo_lectura, None)
        if simular:
            return f"«{meta['titulo']}», {len(meta['etiquetas'])} etiquetas, {capitulos.count(chr(10)) + 1} capítulos"
        enviar("PUT", DATA + "videos?part=snippet,status", token, {"id": video_id, "snippet": snippet, "status": status})
        return "título, descripción con capítulos, etiquetas, categoría e idioma"

    def miniatura():
        ruta = os.path.join(base, "miniatura.png")
        if simular:
            return f"subiría {ruta}"
        with open(ruta, "rb") as f:
            enviar("POST", UPLOAD + f"thumbnails/set?videoId={video_id}&uploadType=media", token, f.read(), "image/png")
        return "miniatura.png"

    def subtitulos():
        ruta = os.path.join(base, f"{nombre}.srt")
        if simular:
            return f"subiría {ruta}"
        existentes = get(DATA + "captions", {"part": "snippet", "videoId": video_id}, token).get("items", [])
        if any(c["snippet"]["language"] == "es" and c["snippet"].get("trackKind") != "asr" for c in existentes):
            return "ya había subtítulos en español"
        with open(ruta, "rb") as f:
            cuerpo, tipo = multipart({"snippet": {"videoId": video_id, "language": "es", "name": "Español", "isDraft": False}},
                                     f.read(), "application/octet-stream")
        enviar("POST", UPLOAD + "captions?part=snippet&uploadType=multipart", token, cuerpo, tipo)
        return "español"

    def playlists():
        todas = get(DATA + "playlists", {"part": "snippet", "mine": "true", "maxResults": 50}, token).get("items", [])
        por_titulo = {p["snippet"]["title"]: p["id"] for p in todas}
        hechas = []
        for titulo in meta["playlists"]:
            pid = por_titulo.get(titulo)
            if not pid:
                hechas.append(f"{titulo} (no existe)")
                continue
            items = get(DATA + "playlistItems", {"part": "contentDetails", "playlistId": pid, "maxResults": 50}, token)
            if any(i["contentDetails"]["videoId"] == video_id for i in items.get("items", [])):
                continue
            if not simular:
                enviar("POST", DATA + "playlistItems?part=snippet", token,
                       {"snippet": {"playlistId": pid, "resourceId": {"kind": "youtube#video", "videoId": video_id}}})
            hechas.append(titulo)
        return ", ".join(hechas) or "ya estaba en todas"

    ok = [paso("Textos", textos), paso("Miniatura", miniatura), paso("Subtítulos", subtitulos), paso("Playlists", playlists)]
    print(("Simulación" if simular else "Listo") + f": {sum(ok)}/{len(ok)} pasos OK. La privacidad no se modificó.")


if __name__ == "__main__":
    main()
