#!/usr/bin/env python3
"""Genera los packs imprimibles de etsy/contenido.py.

Por cada pack escribe en etsy/productos/<slug>/:
  <slug>-letter.pdf, <slug>-a4.pdf   -> lo que descarga el comprador
  publicacion-1..3.png               -> imágenes para la publicación de Etsy

Uso: python3 etsy/generar.py [slug]
"""
import html
import random
import re
import subprocess
import sys
from pathlib import Path

from contenido import PACKS

AQUI = Path(__file__).resolve().parent
SALIDA = AQUI / "productos"
TAMANOS = {"letter": ("8.5in", "11in"), "a4": ("210mm", "297mm")}
FUENTES = '<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,700&display=swap" rel="stylesheet">'

ICONOS = {
    "snow": '<svg viewBox="-12 -12 24 24"><g stroke="currentColor" stroke-width="1.6" stroke-linecap="round" fill="none">'
            + "".join(f'<g transform="rotate({a})"><path d="M0 0V-10M0 -6l-3 -3M0 -6l3 -3"/></g>' for a in range(0, 360, 60))
            + "</g></svg>",
    "star": '<svg viewBox="-12 -12 24 24"><path fill="currentColor" d="M0 -11Q1.5 -1.5 11 0Q1.5 1.5 0 11Q-1.5 1.5 -11 0Q-1.5 -1.5 0 -11Z"/></svg>',
    "spark": '<svg viewBox="-12 -12 24 24"><path fill="currentColor" d="M0 -11Q1.5 -1.5 11 0Q1.5 1.5 0 11Q-1.5 1.5 -11 0Q-1.5 -1.5 0 -11Z"/>'
             '<circle cx="8" cy="-8" r="1.6" fill="currentColor"/><circle cx="-8" cy="8" r="1.6" fill="currentColor"/></svg>',
}

CSS = """
@page { size: %(w)s %(h)s; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: Inter, sans-serif; color: %(ink)s; -webkit-print-color-adjust: exact; }
.page { width: %(w)s; height: %(h)s; padding: .45in; page-break-after: always; overflow: hidden; }
.frame { height: 100%%; border: 1.6pt solid %(ink)s; outline: .6pt solid %(accent)s; outline-offset: 3pt;
         padding: .38in .5in .3in; display: flex; flex-direction: column; }
.top { display: flex; justify-content: space-between; align-items: center; font-size: 8pt;
       letter-spacing: .16em; text-transform: uppercase; font-weight: 600; }
.top .name { letter-spacing: 0; text-transform: none; font-weight: 400; font-size: 10pt; }
.top .name i { display: inline-block; width: 1.9in; border-bottom: .8pt solid %(ink)s; }
.icons { display: flex; gap: 7pt; justify-content: center; color: %(accent)s; margin: 14pt 0 4pt; }
.icons svg { width: 15pt; height: 15pt; } .icons svg:nth-child(2) { width: 22pt; height: 22pt; margin-top: -4pt; }
h1 { font-family: Fraunces, Georgia, serif; font-weight: 700; font-size: 31pt; text-align: center; line-height: 1.05; }
.how { text-align: center; font-size: 10.5pt; line-height: 1.4; max-width: 5.6in; margin: 8pt auto 0; }
.body { flex: 1; display: flex; flex-direction: column; justify-content: space-evenly; margin-top: 14pt; min-height: 0; }
.foot { text-align: center; font-size: 7pt; letter-spacing: .14em; text-transform: uppercase; opacity: .6; margin-top: 8pt; }
.row { display: flex; align-items: flex-end; gap: 9pt; font-size: 11pt; line-height: 1.25; }
.n { flex: none; width: 19pt; height: 19pt; border-radius: 50%%; background: %(ink)s; color: #fff; font-size: 8.5pt;
     font-weight: 700; display: flex; align-items: center; justify-content: center; align-self: center; }
.t { flex: 0 1 auto; max-width: 66%%; } .blank { flex: 1; min-width: 1.4in; border-bottom: .8pt solid %(ink)s; height: 14pt; }
.emoji .t { font-family: "Noto Color Emoji"; font-size: 19pt; letter-spacing: 2pt; }
.scramble .t { font-weight: 700; letter-spacing: .28em; font-size: 12.5pt; }
.big .row { font-size: 14pt; align-items: center; } .big .t { max-width: none; }
.big .n { width: 30pt; height: 30pt; font-size: 14pt; background: %(accent)s; font-family: Fraunces, serif; }
.pair { display: flex; align-items: stretch; gap: 8pt; font-size: 10.5pt; line-height: 1.25; }
.pair div { flex: 1; background: %(soft)s; border-radius: 5pt; padding: 7pt 10pt; display: flex; align-items: center; }
.pair em { align-self: center; font-family: Fraunces, serif; font-style: italic; color: %(accent)s; font-size: 12pt; }
.pt { display: flex; align-items: center; gap: 9pt; font-size: 11pt; }
.box { flex: none; width: 12pt; height: 12pt; border: 1pt solid %(ink)s; border-radius: 2pt; }
.dots { flex: 1; border-bottom: 1pt dotted %(ink)s; opacity: .5; transform: translateY(3pt); }
.pt b { font-family: Fraunces, serif; font-size: 12.5pt; color: %(accent)s; width: 28pt; text-align: right; }
.total { align-self: flex-end; font-weight: 700; font-size: 12pt; } .total i { display: inline-block; width: 1in; border-bottom: 1pt solid %(ink)s; }
.grid { flex: 1; display: grid; grid-template-columns: repeat(4, 1fr); grid-template-rows: repeat(4, 1fr); gap: 6pt; margin-top: 14pt; }
.grid div { border: 1pt solid %(ink)s; border-radius: 5pt; padding: 8pt 7pt 7pt; font-size: 9.5pt; line-height: 1.25;
            text-align: center; display: flex; flex-direction: column; justify-content: space-between; }
.grid div:nth-child(odd) { background: %(soft)s; } .grid i { border-bottom: .8pt solid %(ink)s; height: 12pt; }
.cards { flex: 1; display: grid; grid-template-columns: 1fr 1fr; grid-template-rows: repeat(4, 1fr); gap: 0; margin-top: 14pt; }
.cards div { border: 1pt dashed %(ink)s; margin: -.5pt; padding: 10pt 12pt; font-family: Fraunces, serif; font-size: 11.5pt;
             display: flex; flex-direction: column; justify-content: space-between; }
.cards i { border-bottom: .8pt solid %(ink)s; height: 15pt; opacity: .7; }
.story { font-size: 12.5pt; line-height: 1.55; } .story p { margin-bottom: 10pt; } .story b { color: %(accent)s; }
.cover .frame { justify-content: center; text-align: center; background: %(soft)s; }
.cover h1 { font-size: 50pt; margin: 6pt 0.3in 0; } .cover .k { font-size: 10pt; letter-spacing: .3em; text-transform: uppercase; font-weight: 600; }
.cover .tag { font-family: Fraunces, serif; font-style: italic; font-size: 15pt; margin-top: 12pt; }
.cover ul { list-style: none; margin: 30pt auto 0; font-size: 12.5pt; line-height: 2; }
.cover .icons svg { width: 24pt; height: 24pt; } .cover .icons svg:nth-child(2) { width: 36pt; height: 36pt; }
.guide { font-size: 10pt; line-height: 1.4; } .guide h3 { font-family: Fraunces, serif; font-size: 12.5pt; color: %(accent)s; }
.tips { background: %(soft)s; border-radius: 6pt; padding: 9pt 12pt; font-size: 9.5pt; line-height: 1.45; }
.keys { flex: 1; columns: 2; column-gap: 26pt; margin-top: 16pt; font-size: 9.5pt; line-height: 1.5; }
.keys section { break-inside: avoid; margin-bottom: 14pt; } .keys h3 { font-family: Fraunces, serif; font-size: 12.5pt; color: %(accent)s; }
.keys ol { padding-left: 16pt; }
"""

e = html.escape


def revolver(palabra, rng):
    letras = list(palabra)
    while "".join(letras) == palabra:
        rng.shuffle(letras)
    return "".join(letras)


def iconos(tema):
    return f'<div class="icons">{ICONOS[tema["icon"]] * 3}</div>'


def hoja(pack, titulo, cuerpo, how="", nombre=True, clase=""):
    lado = '<span class="name">Name <i></i></span>' if nombre else "<span></span>"
    return (f'<div class="page {clase}"><div class="frame"><div class="top"><span>{e(pack["title"])}</span>{lado}</div>'
            f'{iconos(pack["theme"])}<h1>{e(titulo)}</h1>' + (f'<p class="how">{e(how)}</p>' if how else "")
            + cuerpo + '<div class="foot">For personal use only</div></div></div>')


def cuerpo_juego(j, rng):
    t = j["type"]
    if t == "lines":
        items = [i[0] if isinstance(i, tuple) else i for i in j["items"]]
        if j.get("scramble"):
            items = [revolver(p, rng) for p in items]
        n = len(items)
        nums = range(n, 0, -1) if j.get("numbered") == "down" else range(1, n + 1)
        blank = '<span class="blank"></span>' if j.get("blank") else ""
        cls = "emoji" if j.get("emoji") else "scramble" if j.get("scramble") else "" if j.get("blank") else "big"
        filas = "".join(f'<div class="row"><span class="n">{k}</span><span class="t">{e(x)}</span>{blank}</div>'
                        for k, x in zip(nums, items))
        return f'<div class="body {cls}">{filas}</div>'
    if t == "pairs":
        return '<div class="body">' + "".join(
            f'<div class="pair"><div>{e(a)}</div><em>or</em><div>{e(b)}</div></div>' for a, b in j["items"]) + "</div>"
    if t == "points":
        filas = "".join(f'<div class="pt"><span class="box"></span><span>{e(x)}</span><span class="dots"></span><b>{p}</b></div>'
                        for x, p in j["items"])
        return f'<div class="body">{filas}<div class="total">My total: <i></i></div></div>'
    if t == "grid":
        return '<div class="grid">' + "".join(f"<div><span>{e(x)}</span><i></i></div>" for x in j["items"]) + "</div>"
    if t == "cards":
        return '<div class="cards">' + f'<div><span>{e(j["prompt"])}</span><i></i><i></i><i></i></div>' * 8 + "</div>"
    if t == "story":
        ps = "".join("<p>" + re.sub(r"\b(LEFT|W?RIGHT)\b", r"<b>\1</b>", e(p)) + "</p>" for p in j["text"])
        return f'<div class="body story">{ps}</div>'
    raise ValueError(t)


def respuestas(j):
    if j["type"] != "lines" or not j.get("blank"):
        return None
    if j.get("scramble"):
        return j["items"]
    if isinstance(j["items"][0], tuple):
        return [r for _, r in j["items"]]
    return None


def documento(pack, tam):
    rng = random.Random(pack["slug"])
    w, h = TAMANOS[tam]
    juegos = pack["games"]
    paginas = [
        f'<div class="page cover"><div class="frame"><div class="k">{e(pack["kicker"])}</div>{iconos(pack["theme"])}'
        f'<h1>{e(pack["title"])}</h1><p class="tag">{e(pack["tagline"])}</p><ul>'
        + "".join(f"<li>{e(j['name'])}</li>" for j in juegos) + "</ul></div></div>"
    ]
    guia = "".join(f'<div><h3>{e(j["name"])}</h3><p>{e(j["how"])} {e(j["host"])}</p></div>' for j in juegos)
    guia += ('<div class="tips"><b>Printing tips.</b> Print at 100% scale on US Letter or A4 paper (use the matching file). '
             'Print one sheet per guest for the pen-and-paper games. Small prizes for the winners make everything more fun!</div>')
    paginas.append(hoja(pack, "How to Play", f'<div class="body guide">{guia}</div>', "A quick guide for the host.", nombre=False))
    for j in juegos:
        paginas.append(hoja(pack, j["name"], cuerpo_juego(j, rng), j["how"], nombre=j["type"] not in ("story", "cards")))
    claves = [(j["name"], respuestas(j)) for j in juegos if respuestas(j)]
    if claves:
        cuerpo = '<div class="keys">' + "".join(
            f"<section><h3>{e(n)}</h3><ol>" + "".join(f"<li>{e(r)}</li>" for r in rs) + "</ol></section>"
            for n, rs in claves) + "</div>"
        paginas.append(hoja(pack, "Answer Key", cuerpo, "For the host's eyes only!", nombre=False))
    css = CSS % dict(pack["theme"], w=w, h=h)
    return f'<!doctype html><meta charset="utf-8">{FUENTES}<style>{css}</style>' + "".join(paginas), len(paginas)


def imagenes(pack, carpeta, n_pag):
    """Tres imágenes 2000x1500 para la publicación, a partir de las páginas reales del PDF."""
    t = pack["theme"]
    n_juegos = len(pack["games"])
    pag = lambda i: f'<img src="pag-{i:02d}.png">'
    base = (f'<!doctype html><meta charset="utf-8">{FUENTES}<style>*{{box-sizing:border-box;margin:0}}'
            f'body{{width:2000px;height:1500px;overflow:hidden;font-family:Inter,sans-serif;color:{t["ink"]}}}'
            f'h1,h2{{font-family:Fraunces,serif;font-weight:700;line-height:1.02}}'
            f'img{{box-shadow:0 14px 40px rgba(0,0,0,.28);background:#fff}}'
            f'.pill{{display:inline-block;border-radius:99px;padding:14px 34px;font-weight:600;font-size:34px}}</style>')
    uno = base + (
        f'<body style="background:{t["bg"]};color:#fff;display:flex;align-items:center">'
        f'<div style="width:880px;padding-left:110px"><div style="letter-spacing:.3em;font-size:28px;font-weight:600;color:{t["soft"]}">PRINTABLE · INSTANT DOWNLOAD</div>'
        f'<h1 style="font-size:132px;margin:34px 0 40px">{e(pack["title"])}</h1>'
        f'<div class="pill" style="background:{t["accent"]}">{n_juegos} games · {n_pag} pages</div>'
        f'<div style="font-size:34px;margin-top:34px;color:{t["soft"]}">US Letter + A4 PDF · Answer keys included</div></div>'
        f'<div style="position:relative;flex:1;height:100%">'
        + "".join(f'<img src="pag-{i:02d}.png" style="position:absolute;width:560px;left:{x}px;top:{y}px;transform:rotate({r}deg)">'
                  for i, x, y, r in [(4, 40, 330, -9), (7, 470, 300, 8), (3, 255, 400, 0)])
        + "</div></body>")
    ancho = 1900 // 6 - 24
    dos = base + (
        f'<body style="background:{t["soft"]};padding:0 50px;text-align:center;display:flex;flex-direction:column;justify-content:center">'
        f'<h2 style="font-size:84px">Everything you get</h2>'
        f'<p style="font-size:34px;margin:14px 0 44px">{n_pag} pages · {n_juegos} games, host guide and answer key</p>'
        f'<div style="display:flex;flex-wrap:wrap;gap:24px;justify-content:center">'
        + "".join(f'<img src="pag-{i:02d}.png" style="width:{ancho}px">' for i in range(1, n_pag + 1))
        + "</div></body>")
    pasos = [("1", "Download", "Your PDF files are ready right after purchase."),
             ("2", "Print", "At home or at a print shop, on US Letter or A4."),
             ("3", "Play", "Hand out the sheets, grab some pens and have fun.")]
    tres = base + (
        f'<body style="background:{t["soft"]};padding:120px 130px"><h2 style="font-size:96px">How it works</h2>'
        f'<div style="display:flex;gap:50px;margin-top:80px">'
        + "".join(f'<div style="flex:1;background:#fff;border-radius:28px;padding:56px 48px">'
                  f'<div style="width:110px;height:110px;border-radius:50%;background:{t["accent"]};color:#fff;font:700 60px Fraunces,serif;display:flex;align-items:center;justify-content:center">{n}</div>'
                  f'<h2 style="font-size:64px;margin:36px 0 18px">{a}</h2><p style="font-size:33px;line-height:1.4">{b}</p></div>'
                  for n, a, b in pasos)
        + f'</div><p style="font-size:32px;line-height:1.5;margin-top:70px;max-width:1500px">This is a digital product — no physical item will be shipped. '
          f'For personal use only. Designed by the shop owner with the assistance of AI tools.</p></body>')
    for k, doc in enumerate((uno, dos, tres), 1):
        f = carpeta / f"_img{k}.html"
        f.write_text(doc, encoding="utf-8")
        subprocess.run(["node", AQUI / "render.js", "png", f, carpeta / f"publicacion-{k}.png", "2000", "1500"], check=True)
        f.unlink()


def generar(pack):
    carpeta = SALIDA / pack["slug"]
    carpeta.mkdir(parents=True, exist_ok=True)
    for tam, (w, h) in TAMANOS.items():
        doc, n_pag = documento(pack, tam)
        f = carpeta / f"_{tam}.html"
        f.write_text(doc, encoding="utf-8")
        subprocess.run(["node", AQUI / "render.js", "pdf", f, carpeta / f'{pack["slug"]}-{tam}.pdf', w, h], check=True)
        f.unlink()
    subprocess.run(["pdftoppm", "-png", "-r", "100", carpeta / f'{pack["slug"]}-letter.pdf', carpeta / "pag"], check=True)
    imagenes(pack, carpeta, n_pag)
    for p in carpeta.glob("pag-*.png"):
        p.unlink()
    print(pack["slug"], n_pag, "páginas")


if __name__ == "__main__":
    for pack in PACKS:
        if len(sys.argv) < 2 or sys.argv[1] == pack["slug"]:
            generar(pack)
