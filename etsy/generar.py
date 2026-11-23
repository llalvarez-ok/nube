#!/usr/bin/env python3
"""Genera los packs imprimibles a partir de etsy/contenido_<idioma>.py.

Por cada pack escribe en etsy/productos/<idioma>/<slug>/:
  <slug>-letter.pdf, <slug>-a4.pdf   -> lo que descarga el comprador
  publicacion-1..3.png               -> imágenes para la publicación de Etsy

Uso: python3 etsy/generar.py [idioma] [slug]
"""
import html
import importlib
import math
import random
import re
import subprocess
import sys
from pathlib import Path

from ilustraciones import ICONOS, guirnalda

AQUI = Path(__file__).resolve().parent
SALIDA = AQUI / "productos"
TAMANOS = {"letter": ("8.5in", "11in"), "a4": ("210mm", "297mm")}
FUENTES = ('<link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600;700&'
           'family=Nunito:wght@400;600;700;800&display=swap" rel="stylesheet">')

TEMAS = {
    "xmas": dict(ink="#26343d", c1="#d93a3a", c2="#1f9d63", c3="#f5b83d", t1="#fdeaea", t2="#e4f5ec", t3="#fff3d6",
                 fondo="#d93a3a", iconos=["tree", "gift", "santa", "ginger", "ornament", "cane", "snowman", "star"], luces=True),
    "nye": dict(ink="#1e2350", c1="#e0457b", c2="#22aaa8", c3="#f4b93a", t1="#fde6ee", t2="#def5f4", t3="#fff3d6",
                fondo="#1e2350", iconos=["partyhat", "glass", "clock", "firework", "balloon", "disco", "star", "popper"], luces=False),
    "office": dict(ink="#25323f", c1="#ee5d4d", c2="#128f8f", c3="#f3b23c", t1="#fde8e4", t2="#dcf2f1", t3="#fff2d8",
                   fondo="#128f8f", iconos=["mug", "gift", "popper", "trophy", "laptop", "balloon", "star", "tree"], luces=False),
}

CSS = """
@page { size: %(w)s %(h)s; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: Nunito, sans-serif; color: %(ink)s; -webkit-print-color-adjust: exact; }
.page { position: relative; width: %(w)s; height: %(h)s; padding: .46in; page-break-after: always; overflow: hidden; }
.confeti { position: absolute; inset: 0; width: 100%%; height: 100%%; }
.frame { position: relative; height: 100%%; border: 3pt solid %(c1)s; border-radius: 22pt; background: #fff;
         padding: 0 .42in .2in; display: flex; flex-direction: column; overflow: hidden; }
.guirnalda { margin: 0 -.42in; } .guirnalda svg { display: block; width: 100%%; }
.top { display: flex; justify-content: space-between; align-items: center; margin-top: 2pt; }
.pill { font: 600 8.5pt Fredoka, sans-serif; letter-spacing: .08em; text-transform: uppercase; color: #fff;
        background: %(c2)s; border-radius: 99pt; padding: 3pt 11pt; }
.name { font-size: 10pt; font-weight: 700; } .name i { display: inline-block; width: 1.9in; border-bottom: 1.2pt solid %(ink)s; }
.titulo { display: flex; align-items: center; justify-content: center; gap: 10pt; margin-top: 8pt; }
.titulo svg { flex: none; width: 50pt; height: 50pt; } .titulo svg:first-child { transform: rotate(-10deg); }
.titulo svg:last-child { transform: rotate(10deg); }
h1 { font-family: Fredoka, sans-serif; font-weight: 700; text-align: center; line-height: 1.02;
     text-shadow: 2.2pt 2.2pt 0 %(c3)s; }
.how { text-align: center; font-size: 10.3pt; font-weight: 600; line-height: 1.35; background: %(t3)s; border-radius: 12pt;
       padding: 6pt 16pt; margin: 8pt auto 0; max-width: 6.1in; }
.body { flex: 1; display: flex; flex-direction: column; justify-content: space-evenly; margin-top: 10pt; min-height: 0; }
.foot { display: flex; align-items: center; justify-content: center; gap: 6pt; font: 500 7.5pt Fredoka, sans-serif;
        letter-spacing: .1em; text-transform: uppercase; opacity: .75; margin-top: 6pt; }
.foot svg { width: 13pt; height: 13pt; }
.row { display: flex; align-items: flex-end; gap: 9pt; font-size: 11pt; font-weight: 600; line-height: 1.22; }
.n { flex: none; width: 21pt; height: 21pt; border-radius: 50%%; color: #fff; font: 700 10.5pt Fredoka, sans-serif;
     display: flex; align-items: center; justify-content: center; align-self: center; }
.k0 { background: %(c1)s; } .k1 { background: %(c2)s; } .k2 { background: %(c3)s; color: %(ink)s; }
.t { flex: 0 1 auto; max-width: 66%%; } .blank { flex: 1; min-width: 1.3in; border-bottom: 1.2pt solid %(ink)s; height: 14pt; }
.emoji .t { font-family: "Noto Color Emoji"; font-size: 19pt; letter-spacing: 2pt; }
.scramble .t { font: 600 14pt Fredoka, sans-serif; letter-spacing: .26em; }
.big .row { font-size: 14pt; align-items: center; background: %(t3)s; border-radius: 99pt; padding: 5pt 14pt 5pt 5pt; }
.big .row:nth-child(3n+1) { background: %(t1)s; } .big .row:nth-child(3n+2) { background: %(t2)s; }
.big .t { max-width: none; } .big .n { width: 31pt; height: 31pt; font-size: 16pt; }
.pair { display: flex; align-items: stretch; gap: 7pt; font-size: 10.5pt; font-weight: 600; line-height: 1.22; }
.pair div { flex: 1; border-radius: 10pt; padding: 6pt 11pt; display: flex; align-items: center; }
.pair div:first-child { background: %(t1)s; } .pair div:last-child { background: %(t2)s; }
.pair em { align-self: center; flex: none; min-width: 24pt; height: 24pt; padding: 0 5pt; border-radius: 99pt; background: %(c3)s;
           font: 600 9pt Fredoka, sans-serif; display: flex; align-items: center; justify-content: center; }
.pt { display: flex; align-items: center; gap: 9pt; font-size: 11pt; font-weight: 600; }
.box { flex: none; width: 13pt; height: 13pt; border: 1.5pt solid %(ink)s; border-radius: 4pt; }
.dots { flex: 1; border-bottom: 2pt dotted %(ink)s; opacity: .35; transform: translateY(3pt); }
.pt b { flex: none; width: 25pt; height: 25pt; border-radius: 50%%; color: #fff; font: 700 11pt Fredoka, sans-serif;
        display: flex; align-items: center; justify-content: center; }
.p5 { background: %(c2)s; } .p10 { background: %(c3)s; color: %(ink)s !important; } .p15 { background: %(c1)s; } .p20 { background: %(ink)s; }
.total { align-self: flex-end; font: 600 13pt Fredoka, sans-serif; background: %(t3)s; border-radius: 99pt; padding: 5pt 16pt; }
.total i { display: inline-block; width: .9in; border-bottom: 1.2pt solid %(ink)s; }
.grid { flex: 1; display: grid; grid-template-columns: repeat(4, 1fr); grid-template-rows: repeat(4, 1fr); gap: 6pt; margin-top: 10pt; }
.grid div { border: 1.5pt solid %(ink)s; border-radius: 11pt; padding: 8pt 7pt 8pt; font-size: 9.6pt; font-weight: 700; line-height: 1.2;
            text-align: center; display: flex; flex-direction: column; justify-content: space-between; background: %(t3)s; }
.grid div:nth-child(4n+1), .grid div:nth-child(4n+3) { background: %(t1)s; }
.grid div:nth-child(8n+2), .grid div:nth-child(8n+4), .grid div:nth-child(8n+5), .grid div:nth-child(8n+7) { background: %(t2)s; }
.grid i { border-bottom: 1.2pt solid %(ink)s; height: 12pt; }
.cards { flex: 1; display: grid; grid-template-columns: 1fr 1fr; grid-template-rows: repeat(4, 1fr); margin-top: 10pt; }
.cards div { position: relative; border: 1.5pt dashed %(ink)s; margin: -.75pt; padding: 9pt 12pt; font: 600 11.5pt Fredoka, sans-serif;
             display: flex; flex-direction: column; justify-content: space-between; }
.cards svg { position: absolute; right: 7pt; top: 6pt; width: 20pt; height: 20pt; }
.cards span { padding-right: 24pt; } .cards i { border-bottom: 1pt solid %(ink)s; height: 14pt; opacity: .6; }
.story { font-size: 12.5pt; line-height: 1.6; font-weight: 600; justify-content: center; } .story p { margin-bottom: 11pt; }
.story b { color: #fff; border-radius: 6pt; padding: 0 4pt; font-family: Fredoka, sans-serif; font-weight: 600; }
.story .w0 { background: %(c1)s; } .story .w1 { background: %(c2)s; }
.cover .frame { border: none; background: %(t3)s; border-radius: 0; padding: 0; justify-content: center; align-items: center; overflow: visible; }
.cover { padding: 0; } .cover .ic { position: absolute; }
.cover .card { position: relative; background: #fff; border: 3pt solid %(ink)s; border-radius: 30pt; box-shadow: 7pt 7pt 0 %(c1)s;
               width: 74%%; padding: 26pt 22pt 24pt; text-align: center; }
.cover h1 { margin: 12pt 0 0; text-shadow: 3pt 3pt 0 %(c3)s; } .cover .pill { display: inline-block; font-size: 10pt; }
.cover .tag { font-size: 13.5pt; font-weight: 700; margin-top: 12pt; }
.cover ul { list-style: none; margin-top: 16pt; display: flex; flex-wrap: wrap; gap: 6pt; justify-content: center; }
.cover li { font: 600 10.5pt Fredoka, sans-serif; border-radius: 99pt; padding: 4pt 12pt; }
.guide { font-size: 9.8pt; line-height: 1.33; font-weight: 600; }
.guide h3, .keys h3 { font: 600 12.5pt Fredoka, sans-serif; color: %(c1)s; } .guide div:nth-child(even) h3 { color: %(c2)s; }
.tips { background: %(t2)s; border-radius: 12pt; padding: 8pt 13pt; }
.keys { flex: 1; columns: 2; column-gap: 24pt; margin-top: 14pt; font-size: 9.6pt; font-weight: 600; line-height: 1.5; }
.keys section { break-inside: avoid; margin-bottom: 12pt; background: %(t3)s; border-radius: 12pt; padding: 8pt 12pt; }
.keys section:nth-child(even) { background: %(t2)s; } .keys ol { padding-left: 17pt; }
"""

e = html.escape


def icono(nombre, t):
    return ICONOS[nombre](t)


def confeti(rng, t, n=46):
    """Papel picado en la franja exterior de la hoja (fuera del marco)."""
    piezas = []
    for _ in range(n):
        lado = rng.choice("TBLR")
        a, b = rng.uniform(4, 96), rng.uniform(2.6, 4.0)
        x, y = {"T": (a, b), "B": (a, 100 - b), "L": (b * 1.25, a), "R": (100 - b * 1.25, a)}[lado]
        col = rng.choice([t["c1"], t["c2"], t["c3"]])
        r = rng.uniform(0, 360)
        forma = rng.choice(["c", "r", "s"])
        if forma == "c":
            piezas.append(f'<circle cx="{x:.1f}%" cy="{y:.1f}%" r="3" fill="{col}"/>')
        elif forma == "r":
            piezas.append(f'<svg x="{x:.1f}%" y="{y:.1f}%" overflow="visible"><rect x="-4.5" y="-2" width="9" height="4" rx="1" fill="{col}" transform="rotate({r:.0f})"/></svg>')
        else:
            piezas.append(f'<svg x="{x:.1f}%" y="{y:.1f}%" overflow="visible"><path d="M0-5 1.4-1.4 5 0 1.4 1.4 0 5-1.4 1.4-5 0-1.4-1.4Z" fill="{col}" transform="rotate({r:.0f})"/></svg>')
    return f'<svg class="confeti">{"".join(piezas)}</svg>'


def tam_titulo(texto, base=31):
    n = len(texto)
    return base if n <= 20 else base * .86 if n <= 26 else base * .74 if n <= 33 else base * .64


def tam_ancho(texto, base, ancho):
    """Reduce el tamaño si la palabra más larga no entra en el ancho disponible."""
    return min(base, ancho / (.62 * max(map(len, texto.split()))))


def hoja(pack, S, t, rng, idx, titulo, cuerpo, how="", nombre=True):
    ic = t["iconos"]
    a, b = ic[idx % len(ic)], ic[(idx + 3) % len(ic)]
    lado = f'<span class="name">{e(S["name"])} <i></i></span>' if nombre else "<span></span>"
    pie = icono(ic[(idx + 1) % len(ic)], t) + f'<span>{e(S["personal"])}</span>' + icono(ic[(idx + 5) % len(ic)], t)
    return (f'<div class="page">{confeti(rng, t)}<div class="frame"><div class="guirnalda">{guirnalda(t)}</div>'
            f'<div class="top"><span class="pill">{e(pack["title"])}</span>{lado}</div>'
            f'<div class="titulo">{icono(a, t)}<h1 style="font-size:{tam_titulo(titulo):.1f}pt">{e(titulo)}</h1>{icono(b, t)}</div>'
            + (f'<p class="how">{e(how)}</p>' if how else "") + cuerpo + f'<div class="foot">{pie}</div></div></div>')


def revolver(palabra, rng):
    letras = list(palabra)
    while "".join(letras) == palabra:
        rng.shuffle(letras)
    return "".join(letras)


def cuerpo_juego(j, S, t, rng):
    tipo = j["type"]
    if tipo == "lines":
        items = [i[0] if isinstance(i, tuple) else i for i in j["items"]]
        if j.get("scramble"):
            items = [revolver(p, rng) for p in items]
        n = len(items)
        nums = range(n, 0, -1) if j.get("numbered") == "down" else range(1, n + 1)
        blank = '<span class="blank"></span>' if j.get("blank") else ""
        cls = "emoji" if j.get("emoji") else "scramble" if j.get("scramble") else "" if j.get("blank") else "big"
        filas = "".join(f'<div class="row"><span class="n k{i % 3}">{k}</span><span class="t">{e(x)}</span>{blank}</div>'
                        for i, (k, x) in enumerate(zip(nums, items)))
        return f'<div class="body {cls}">{filas}</div>'
    if tipo == "pairs":
        return '<div class="body">' + "".join(
            f'<div class="pair"><div>{e(a)}</div><em>{e(S["or"])}</em><div>{e(b)}</div></div>' for a, b in j["items"]) + "</div>"
    if tipo == "points":
        filas = "".join(f'<div class="pt"><span class="box"></span><span>{e(x)}</span><span class="dots"></span><b class="p{p}">{p}</b></div>'
                        for x, p in j["items"])
        return f'<div class="body">{filas}<div class="total">{e(S["total"])}: <i></i></div></div>'
    if tipo == "grid":
        return '<div class="grid">' + "".join(f"<div><span>{e(x)}</span><i></i></div>" for x in j["items"]) + "</div>"
    if tipo == "cards":
        ic = t["iconos"]
        return '<div class="cards">' + "".join(
            f'<div>{icono(ic[k % len(ic)], t)}<span>{e(j["prompt"])}</span><i></i><i></i><i></i></div>' for k in range(8)) + "</div>"
    if tipo == "story":
        palabras = S["pass_words"]
        patron = re.compile(r"\b(" + "|".join(map(re.escape, palabras)) + r")\b")
        # La tercera palabra (p. ej. WRIGHT) suena igual que la segunda: mismo color.
        marca = lambda m: f'<b class="w{min(palabras.index(m.group(1)), 1)}">{m.group(1)}</b>'
        ps = "".join("<p>" + patron.sub(marca, e(p)) + "</p>" for p in j["text"])
        return f'<div class="body story">{ps}</div>'
    raise ValueError(tipo)


def respuestas(j):
    if j["type"] != "lines" or not j.get("blank"):
        return None
    if j.get("scramble"):
        return j["items"]
    if isinstance(j["items"][0], tuple):
        return [r for _, r in j["items"]]
    return None


def portada(pack, S, t, rng):
    ic = t["iconos"]
    piezas, k = [], 0
    for fila in range(7):
        for col in range(5):
            if 1 <= fila <= 5 and 1 <= col <= 3:
                continue
            x = 3 + col * 19.5 + rng.uniform(-2, 2)
            y = 3 + fila * 13.6 + rng.uniform(-1.5, 1.5)
            piezas.append(f'<div class="ic" style="left:{x:.1f}%;top:{y:.1f}%;width:13%;transform:rotate({rng.uniform(-18, 18):.0f}deg)">{icono(ic[k % len(ic)], t)}</div>')
            k += 1
    tintes = [t["t1"], t["t2"], t["t3"]]
    lista = "".join(f'<li style="background:{tintes[i % 3]}">{e(j["name"])}</li>' for i, j in enumerate(pack["games"]))
    return (f'<div class="page cover"><div class="frame">{"".join(piezas)}<div class="card"><span class="pill">{e(pack["kicker"])}</span>'
            f'<h1 style="font-size:{tam_ancho(pack["title"], tam_titulo(pack["title"], 52), 390):.1f}pt">{e(pack["title"])}</h1><p class="tag">{e(pack["tagline"])}</p>'
            f'<ul>{lista}</ul></div></div></div>')


def documento(pack, S, tam):
    rng = random.Random(pack["slug"])
    t = TEMAS[pack["theme"]]
    w, h = TAMANOS[tam]
    juegos = pack["games"]
    paginas = [portada(pack, S, t, rng)]
    guia = "".join(f'<div><h3>{e(j["name"])}</h3><p>{e(j["how"])} {e(j["host"])}</p></div>' for j in juegos)
    guia += f'<div class="tips"><b>{e(S["tips_title"])}</b> {e(S["tips"])}</div>'
    paginas.append(hoja(pack, S, t, rng, 0, S["how_to_play"], f'<div class="body guide">{guia}</div>', S["host_sub"], nombre=False))
    for k, j in enumerate(juegos, 1):
        paginas.append(hoja(pack, S, t, rng, k, j["name"], cuerpo_juego(j, S, t, rng), j["how"], nombre=j["type"] not in ("story", "cards")))
    claves = [(j["name"], respuestas(j)) for j in juegos if respuestas(j)]
    if claves:
        cuerpo = '<div class="keys">' + "".join(
            f"<section><h3>{e(n)}</h3><ol>" + "".join(f"<li>{e(r)}</li>" for r in rs) + "</ol></section>"
            for n, rs in claves) + "</div>"
        paginas.append(hoja(pack, S, t, rng, len(juegos) + 1, S["answer_key"], cuerpo, S["answer_sub"], nombre=False))
    css = CSS % dict(t, w=w, h=h)
    return f'<!doctype html><meta charset="utf-8">{FUENTES}<style>{css}</style>' + "".join(paginas), len(paginas)


def imagenes(pack, S, carpeta, n_pag):
    """Tres imágenes 2000x1500 para la publicación, a partir de las páginas reales del PDF."""
    t = TEMAS[pack["theme"]]
    rng = random.Random(pack["slug"] + "img")
    n_juegos = len(pack["games"])
    cuenta = dict(games=n_juegos, pages=n_pag)
    ic = t["iconos"]
    base = (f'<!doctype html><meta charset="utf-8">{FUENTES}<style>*{{box-sizing:border-box;margin:0}}'
            f'body{{position:relative;width:2000px;height:1500px;overflow:hidden;font-family:Nunito,sans-serif;font-weight:700;color:{t["ink"]}}}'
            f'h1,h2{{font-family:Fredoka,sans-serif;font-weight:700;line-height:1.02}}'
            f'img{{box-shadow:0 14px 40px rgba(0,0,0,.3);background:#fff;border-radius:10px}}'
            f'.ic{{position:absolute}} .ic svg{{width:100%;display:block}}'
            f'.pill{{display:inline-block;border-radius:99px;padding:14px 36px;font:600 38px Fredoka,sans-serif}}</style>')

    def sueltos(posiciones):
        return "".join(f'<div class="ic" style="left:{x}px;top:{y}px;width:{w}px;transform:rotate({rng.uniform(-18, 18):.0f}deg)">{icono(ic[k % len(ic)], t)}</div>'
                       for k, (x, y, w) in enumerate(posiciones))

    tam = 150 if len(pack["title"]) <= 18 else 124 if len(pack["title"]) <= 26 else 100
    tam = tam_ancho(pack["title"], tam, 850)
    uno = base + (
        f'<body style="background:{t["fondo"]};color:#fff">'
        + sueltos([(60, 50, 170), (330, 90, 120), (620, 40, 150), (70, 1270, 160), (380, 1300, 130), (690, 1250, 150), (1780, 40, 170), (1800, 1290, 160)])
        + f'<div style="position:absolute;left:110px;top:0;width:860px;height:1500px;display:flex;flex-direction:column;justify-content:center">'
        f'<div style="letter-spacing:.22em;font:600 28px Fredoka,sans-serif;color:{t["t3"]}">{e(S["img_kicker"])}</div>'
        f'<h1 style="font-size:{tam:.0f}px;margin:30px 0 40px;text-shadow:7px 7px 0 {t["ink"]}">{e(pack["title"])}</h1>'
        f'<div><span class="pill" style="background:{t["c3"]};color:{t["ink"]}">{e(S["img_count"].format(**cuenta))}</span></div>'
        f'<div style="font-size:34px;margin-top:34px;color:{t["t3"]}">{e(S["img_formats"])}</div></div>'
        + "".join(f'<img src="pag-{i:02d}.png" style="position:absolute;width:540px;left:{x}px;top:{y}px;transform:rotate({r}deg)">'
                  for i, x, y, r in [(5, 1000, 330, -9), (8, 1375, 300, 8), (3, 1190, 400, 0)])
        + "</body>")
    ancho = 1900 // 6 - 24
    dos = base + (
        f'<body style="background:{t["t3"]};padding:0 50px;text-align:center;display:flex;flex-direction:column;justify-content:center">'
        f'<h2 style="font-size:92px;text-shadow:5px 5px 0 {t["c3"]}">{e(S["img_all"])}</h2>'
        f'<p style="font-size:36px;margin:16px 0 44px">{e(S["img_all_sub"].format(**cuenta))}</p>'
        f'<div style="display:flex;flex-wrap:wrap;gap:24px;justify-content:center">'
        + "".join(f'<img src="pag-{i:02d}.png" style="width:{ancho}px">' for i in range(1, n_pag + 1))
        + "</div></body>")
    colores = [t["c1"], t["c2"], t["c3"]]
    tres = base + (
        f'<body style="background:{t["t2"]};padding:110px 120px">' + sueltos([(1700, 60, 180), (1490, 90, 130)])
        + f'<h2 style="font-size:104px;text-shadow:5px 5px 0 {t["c3"]}">{e(S["img_how"])}</h2>'
        f'<div style="display:flex;gap:44px;margin-top:70px">'
        + "".join(f'<div style="flex:1;background:#fff;border:5px solid {t["ink"]};border-radius:40px;box-shadow:10px 10px 0 {colores[n]};padding:50px 44px">'
                  f'<div style="width:116px;height:116px;border-radius:50%;background:{colores[n]};color:{"#fff" if n < 2 else t["ink"]};font:700 64px Fredoka,sans-serif;display:flex;align-items:center;justify-content:center">{n + 1}</div>'
                  f'<h2 style="font-size:60px;margin:34px 0 16px">{e(a)}</h2><p style="font-size:33px;line-height:1.38">{e(b)}</p></div>'
                  for n, (a, b) in enumerate(S["img_steps"]))
        + f'</div><p style="font-size:31px;line-height:1.5;margin-top:70px;max-width:1700px">{e(S["img_note"])}</p></body>')
    for k, doc in enumerate((uno, dos, tres), 1):
        f = carpeta / f"_img{k}.html"
        f.write_text(doc, encoding="utf-8")
        subprocess.run(["node", AQUI / "render.js", "png", f, carpeta / f"publicacion-{k}.png", "2000", "1500"], check=True)
        f.unlink()


def generar(pack, S):
    carpeta = SALIDA / S["lang"] / pack["slug"]
    carpeta.mkdir(parents=True, exist_ok=True)
    for tam, (w, h) in TAMANOS.items():
        doc, n_pag = documento(pack, S, tam)
        f = carpeta / f"_{tam}.html"
        f.write_text(doc, encoding="utf-8")
        subprocess.run(["node", AQUI / "render.js", "pdf", f, carpeta / f'{pack["slug"]}-{tam}.pdf', w, h], check=True)
        f.unlink()
    muestra = "letter" if S["lang"] == "en" else "a4"
    subprocess.run(["pdftoppm", "-png", "-r", "100", carpeta / f'{pack["slug"]}-{muestra}.pdf', carpeta / "pag"], check=True)
    imagenes(pack, S, carpeta, n_pag)
    for p in carpeta.glob("pag-*.png"):
        p.unlink()
    print(S["lang"], pack["slug"], n_pag, "páginas")


if __name__ == "__main__":
    sys.path.insert(0, str(AQUI))
    args = sys.argv[1:]
    for f in sorted(AQUI.glob("contenido_*.py")):
        lang = f.stem.split("_")[1]
        if args and args[0] != lang:
            continue
        mod = importlib.import_module(f.stem)
        for pack in mod.PACKS:
            if len(args) < 2 or args[1] == pack["slug"]:
                generar(pack, mod.STRINGS)
