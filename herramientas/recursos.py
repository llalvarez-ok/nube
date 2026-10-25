#!/usr/bin/env python3
"""Busca y descarga imágenes de apoyo con licencia libre, y registra el crédito.

    python3 herramientas/recursos.py video02 "office laptop" --n 3
    python3 herramientas/recursos.py video02 "spreadsheet" --fuente pexels

Fuentes gratuitas:
    openverse (por defecto, sin clave): obras con licencia Creative Commons.
    pexels (PEXELS_API_KEY, gratis en pexels.com/api): fotos de uso libre.

Guarda en produccion/<video>/recursos/ y agrega cada archivo a creditos.json, que el
agente seo-empaquetador copia a la descripción. Se usan en escenas de tipo "imagen"
("imagen": "produccion/<video>/recursos/<archivo>", "credito": "...").
Solo se aceptan licencias que permiten uso comercial (CC0, PDM, BY, BY-SA).
"""

import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LICENCIAS_OK = {"cc0", "pdm", "by", "by-sa"}


def pedir(url, cabeceras=None):
    req = urllib.request.Request(url, headers={"User-Agent": "atajos-ia/1.0", **(cabeceras or {})})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def openverse(consulta, n):
    q = urllib.parse.urlencode({"q": consulta, "license": ",".join(LICENCIAS_OK), "page_size": n * 2,
                                "aspect_ratio": "wide", "size": "large", "mature": "false"})
    datos = json.loads(pedir(f"https://api.openverse.org/v1/images/?{q}"))
    for r in datos.get("results", []):
        if r.get("license") in LICENCIAS_OK:
            autor = r.get("creator") or "autor desconocido"
            yield r["url"], f"{r.get('title') or 'Imagen'} · {autor} · CC {r['license'].upper()} · {r.get('foreign_landing_url', '')}"


def pexels(consulta, n):
    clave = os.environ.get("PEXELS_API_KEY")
    if not clave:
        sys.exit("Falta PEXELS_API_KEY (gratis en https://www.pexels.com/api/). O usa --fuente openverse.")
    q = urllib.parse.urlencode({"query": consulta, "per_page": n, "orientation": "landscape"})
    datos = json.loads(pedir(f"https://api.pexels.com/v1/search?{q}", {"Authorization": clave}))
    for f in datos.get("photos", []):
        yield f["src"]["large2x"], f"Foto de {f['photographer']} en Pexels · {f['url']}"


def main():
    from investigar import posicionales
    args = posicionales(sys.argv[1:], {"--n", "--fuente"})
    n = int(sys.argv[sys.argv.index("--n") + 1]) if "--n" in sys.argv else 3
    fuente = sys.argv[sys.argv.index("--fuente") + 1] if "--fuente" in sys.argv else "openverse"
    if len(args) < 2:
        sys.exit(__doc__)
    video, consulta = args[0], " ".join(args[1:])
    destino = os.path.join(RAIZ, "produccion", video, "recursos")
    os.makedirs(destino, exist_ok=True)
    reg_path = os.path.join(destino, "creditos.json")
    registro = json.load(open(reg_path, encoding="utf-8")) if os.path.exists(reg_path) else {}
    buscador = pexels if fuente == "pexels" else openverse
    base = re.sub(r"[^a-z0-9]+", "-", consulta.lower()).strip("-")
    guardadas = 0
    try:
        for url, credito in buscador(consulta, n):
            if guardadas >= n:
                break
            ext = os.path.splitext(urllib.parse.urlparse(url).path)[1].lower()
            ext = ext if ext in (".jpg", ".jpeg", ".png", ".webp") else ".jpg"
            nombre = f"{base}-{len(registro) + 1}{ext}"
            try:
                datos = pedir(url)
            except urllib.error.URLError:
                continue
            with open(os.path.join(destino, nombre), "wb") as f:
                f.write(datos)
            registro[nombre] = credito
            guardadas += 1
            print(f"✔ recursos/{nombre} · {credito}")
    except urllib.error.URLError as e:
        sys.exit(f"No se pudo consultar {fuente}: {e}")
    with open(reg_path, "w", encoding="utf-8") as f:
        json.dump(registro, f, ensure_ascii=False, indent=2)
    if not guardadas:
        print("No se encontraron imágenes con licencia libre para esa búsqueda (prueba en inglés).")


if __name__ == "__main__":
    main()
