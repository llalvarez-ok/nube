#!/usr/bin/env python3
"""Produce un video de Atajos IA a partir de produccion/<video>/escenas.json.

    python3 herramientas/producir_video.py video01            # con voz (Google TTS)
    python3 herramientas/producir_video.py video01 --sin-voz  # vista previa muda

Pipeline: escenas HTML -> PNG (Chromium) · voz por paso (Google Cloud TTS) ·
segmentos con zoom suave y revelado progresivo de listas (ffmpeg) · música con
ducking opcional · video final normalizado a -14 LUFS · subtítulos .srt · capítulos.

Opciones de escenas.json (además de "titulo" y "pasos"):
    "total_pasos": 4                      la etiqueta "Paso N de 4"
    "marca": {"nombre": "Atajos IA", "acento": "#ffd400"}
    "musica": "produccion/musica/tema.mp3"  (Biblioteca de audio de YouTube; va a -26 dB bajo la voz)

Variables de entorno:
    GOOGLE_TTS_API_KEY   clave de API con Cloud Text-to-Speech habilitada
    TTS_VOZ              opcional, p. ej. es-US-Chirp3-HD-Charon
"""

import base64
import html
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FUENTES = os.path.join(RAIZ, "produccion", "render", "fonts")
FPS = 30
PAUSA = 0.35  # silencio al final de cada paso
XFADE = 0.25  # fundido entre cuadros del revelado progresivo
VOZ_PREFERIDA = ["es-US-Chirp3-HD-Charon", "es-US-Chirp3-HD-Orus", "es-US-Chirp3-HD-Puck"]

CSS = f"""
@font-face{{font-family:Inter;font-weight:400;src:url(file://{FUENTES}/inter-latin-400-normal.woff2)}}
@font-face{{font-family:Inter;font-weight:600;src:url(file://{FUENTES}/inter-latin-600-normal.woff2)}}
@font-face{{font-family:Inter;font-weight:800;src:url(file://{FUENTES}/inter-latin-800-normal.woff2)}}
@font-face{{font-family:Inter;font-weight:900;src:url(file://{FUENTES}/inter-latin-900-normal.woff2)}}
*{{box-sizing:border-box}}
html,body{{margin:0;width:1920px;height:1080px;overflow:hidden;background:#0f0f10;color:#fff;font-family:Inter,sans-serif}}
.grid{{position:absolute;inset:0;background-image:linear-gradient(#ffffff07 1px,transparent 1px),linear-gradient(90deg,#ffffff07 1px,transparent 1px);background-size:60px 60px}}
.marca{{position:absolute;left:64px;top:48px;display:flex;align-items:center;gap:14px;font-weight:800;font-size:30px}}
.marca svg{{width:44px;height:44px}}
.paso{{position:absolute;right:64px;top:48px;padding:10px 24px;border-radius:999px;background:#ffd400;color:#0f0f10;font-weight:800;font-size:28px}}
.centro{{position:absolute;inset:140px 120px 100px;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center}}
.grande{{font-weight:900;font-size:110px;letter-spacing:-3px;line-height:1.05}}
.chico{{margin-top:34px;font-size:46px;color:#cfcfcf;font-weight:600;line-height:1.3;white-space:pre-line}}
.amarillo{{color:#ffd400}}
.oculto{{opacity:0!important}}
.cifra{{font-weight:900;font-size:300px;letter-spacing:-10px;line-height:1;color:#ffd400}}
.mitad{{position:absolute;top:150px;bottom:100px;width:820px;display:flex;flex-direction:column;justify-content:center}}
.tarjeta{{background:#1a1a1d;border:2px solid #2c2c31;border-radius:28px;padding:48px 56px;text-align:left}}
.etiqueta{{font-size:26px;font-weight:800;color:#9a9aa3;text-transform:uppercase;letter-spacing:2px;margin-bottom:22px}}
.pag{{display:inline-block;background:#ffd400;color:#0f0f10;font-weight:800;border-radius:10px;padding:0 12px;font-size:.8em;margin-left:6px}}
ul,ol{{margin:0;padding-left:1.1em}} li{{margin:0 0 22px}}
table{{border-collapse:collapse;width:100%;font-size:38px}}
td,th{{padding:18px 22px;border-bottom:2px solid #2c2c31;text-align:left}} th{{color:#9a9aa3;font-size:26px;text-transform:uppercase;letter-spacing:2px}}
"""

ICONO = '<svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="48" fill="#ffd400"/><path d="M28 30 L50 50 L28 70 Z M50 30 L72 50 L50 70 Z" fill="#0f0f10"/></svg>'


def pags(texto):
    """Escapa y convierte '(pág. 5)' / '(págs. 2 y 5)' en etiquetas amarillas."""
    t = html.escape(texto)
    return re.sub(r"\((págs?\. [^)]+)\)", r'<span class="pag">\1</span>', t)


LISTAS = {"herramientas": "items", "respuesta": "items", "lista": "items", "tabla": "filas", "comparar": "filas"}
MARCA = {"nombre": "Atajos IA", "acento": "#ffd400"}
TOTAL_PASOS = 4


def estados(p):
    """Cuántos cuadros tiene la escena: las listas se revelan de a un elemento."""
    clave = LISTAS.get(p["tipo"])
    if clave and p.get("revelar", True) and len(p[clave]) > 1:
        return len(p[clave])
    return 1


def escena_html(p, build, revelar=None):
    tipo = p["tipo"]
    g, c = p.get("grande", ""), p.get("chico", "")

    def oc(i):  # clase para los elementos todavía no revelados
        return " oculto" if revelar is not None and i >= revelar else ""

    cab = f'<div class="grid"></div><div class="marca">{ICONO}{html.escape(MARCA["nombre"])}</div>'
    if p.get("paso"):
        cab += f'<div class="paso">Paso {p["paso"]} de {TOTAL_PASOS}</div>'

    def centro(interior):
        return f'<div class="centro">{interior}</div>'

    if tipo in ("titulo", "cta", "plantilla", "respuesta_mini"):
        extra = ""
        if tipo == "cta":
            extra = '<div style="margin-top:60px;background:#ff2d2d;color:#fff;font-weight:800;font-size:48px;padding:22px 60px;border-radius:999px">SUSCRIBIRSE</div>'
        if tipo == "plantilla":
            extra = '<div style="margin-top:60px;font-size:120px">📄⬇</div>'
        if tipo == "respuesta_mini":
            extra = ('<div class="tarjeta" style="margin-top:50px;font-size:36px;width:1300px">'
                     '<div class="etiqueta">Resumen</div>Ventas Q3: $ 1.240 M, +8 % <span class="pag">pág. 2</span><br>'
                     'Costo logístico: 11,2 % <span class="pag">pág. 5</span></div>')
        cuerpo = centro(f'<div class="grande">{html.escape(g)}</div><div class="chico">{html.escape(c)}</div>{extra}')
    elif tipo == "problema":
        cuerpo = centro(f'<div class="grande" style="text-decoration:line-through;text-decoration-color:#ff3b3b;text-decoration-thickness:12px">{html.escape(g)}</div><div class="chico">{html.escape(c)}</div>')
    elif tipo == "paginas":
        imgs = "".join(
            f'<img src="file://{build}/pag-{n}.png" style="position:absolute;height:760px;left:{980 + i * 230}px;top:{190 + i * 30}px;transform:rotate({(i - 1) * 4}deg);box-shadow:0 30px 60px #000a;border-radius:8px">'
            for i, n in enumerate(p["paginas"]))
        cuerpo = (imgs + f'<div style="position:absolute;left:120px;top:330px;width:820px"><div class="grande">{html.escape(g)}</div>'
                  f'<div class="chico" style="text-align:left">{html.escape(c)}</div></div>')
    elif tipo == "herramientas":
        chips = "".join(f'<div class="tarjeta{oc(i)}" style="font-size:56px;font-weight:800;text-align:center">{html.escape(x)}</div>' for i, x in enumerate(p["items"]))
        cuerpo = centro(f'<div class="grande" style="font-size:84px">{html.escape(g)}</div>'
                        f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:34px;margin-top:60px;width:1300px">{chips}</div>')
    elif tipo == "aviso":
        color = "#ff3b3b" if p.get("rojo") else "#ffd400"
        cuerpo = centro(f'<div class="tarjeta" style="border-color:{color};width:1500px;text-align:center">'
                        f'<div style="font-size:110px">⚠</div><div class="grande" style="font-size:76px;color:{color}">{html.escape(g)}</div>'
                        f'<div class="chico" style="font-size:40px">{html.escape(c)}</div></div>')
    elif tipo == "prompt":
        borde = "#ffd400" if p.get("destacar") else "#2c2c31"
        cuerpo = centro(f'<div class="tarjeta" style="width:1560px;border-color:{borde}"><div class="etiqueta">Tu prompt</div>'
                        f'<div style="font-size:42px;line-height:1.45;white-space:pre-line">{html.escape(p["texto"])}</div></div>')
    elif tipo == "respuesta":
        color = "#ffb020" if p.get("ambar") else "#ffd400"
        items = "".join(f'<li class="{oc(i)}">{pags(x)}</li>' for i, x in enumerate(p["items"]))
        cuerpo = centro(f'<div class="tarjeta" style="width:1560px;border-left:10px solid {color}"><div class="etiqueta">Respuesta de Claude · {html.escape(p["titulo"])}</div>'
                        f'<ul style="font-size:44px;line-height:1.35">{items}</ul></div>')
    elif tipo == "tabla":
        filas = "".join(f'<tr class="{oc(i)}"><td>{html.escape(a)}</td><td style="font-weight:800">{html.escape(b)}</td><td><span class="pag">pág. {html.escape(n)}</span></td></tr>' for i, (a, b, n) in enumerate(p["filas"]))
        cuerpo = centro(f'<div class="tarjeta" style="width:1500px"><div class="etiqueta">Respuesta de Claude · {html.escape(p["titulo"])}</div>'
                        f'<table><tr><th>Dato</th><th>Valor</th><th>Página</th></tr>{filas}</table></div>')
    elif tipo == "verificar":
        cuerpo = (f'<img src="file://{build}/pag-{p["pagina"]}.png" style="position:absolute;left:150px;top:150px;height:860px;border-radius:8px;outline:10px solid #ffd400">'
                  f'<div style="position:absolute;left:900px;top:300px;width:900px"><div class="etiqueta">La IA dijo</div>'
                  f'<div class="grande" style="font-size:96px">{html.escape(p["dato"])} <span class="pag" style="font-size:48px">pág. {p["pagina"]}</span></div>'
                  f'<div class="grande amarillo" style="font-size:90px;margin-top:60px">✔ Verificado</div></div>')
    elif tipo == "lista":
        items = "".join(f'<li class="{oc(i)}">{html.escape(x)}</li>' for i, x in enumerate(p["items"]))
        cuerpo = centro(f'<div class="tarjeta" style="width:1560px"><div class="etiqueta">{html.escape(p["titulo"])}</div>'
                        f'<ol style="font-size:50px;line-height:1.35">{items}</ol></div>')
    elif tipo == "comparar":
        filas = "".join(f'<tr class="{oc(i)}"><td>{html.escape(a)}</td><td class="amarillo" style="font-weight:800">{html.escape(b)}</td></tr>' for i, (a, b) in enumerate(p["filas"]))
        cuerpo = centro(f'<div class="grande" style="font-size:84px;margin-bottom:40px">{html.escape(g)}</div>'
                        f'<div class="tarjeta" style="width:1600px"><table><tr><th>Si tienes…</th><th>Usa</th></tr>{filas}</table></div>')
    elif tipo == "final":
        cuerpo = ('<div style="position:absolute;left:150px;top:330px;width:900px;height:506px;border:4px dashed #3a3a40;border-radius:20px;display:flex;align-items:center;justify-content:center;color:#55555c;font-size:34px"></div>'
                  '<div style="position:absolute;left:1250px;top:380px;width:400px;height:400px;border:4px dashed #3a3a40;border-radius:50%"></div>'
                  f'<div style="position:absolute;left:150px;top:160px" class="grande">{html.escape(g)}</div>')
    elif tipo == "cifra":  # un número enorme con su contexto: "40 %" / "de los correos se pueden automatizar"
        cuerpo = centro(f'<div class="cifra">{html.escape(g)}</div><div class="chico" style="font-size:58px;color:#fff">{html.escape(c)}</div>'
                        + (f'<div class="chico" style="font-size:30px;color:#77777f">Fuente: {html.escape(p["fuente"])}</div>' if p.get("fuente") else ""))
    elif tipo == "antes_despues":  # {"antes": {"titulo","texto"}, "despues": {...}}
        a, d = p["antes"], p["despues"]
        cuerpo = (f'<div class="mitad" style="left:120px"><div class="etiqueta" style="color:#ff3b3b">Antes</div>'
                  f'<div class="grande" style="font-size:96px;color:#8a8a93;text-decoration:line-through;text-decoration-color:#ff3b3b">{html.escape(a["titulo"])}</div>'
                  f'<div class="chico" style="text-align:left">{html.escape(a.get("texto", ""))}</div></div>'
                  f'<div style="position:absolute;left:958px;top:200px;bottom:150px;width:4px;background:#2c2c31"></div>'
                  f'<div class="mitad" style="left:1000px"><div class="etiqueta amarillo">Después</div>'
                  f'<div class="grande amarillo" style="font-size:96px">{html.escape(d["titulo"])}</div>'
                  f'<div class="chico" style="text-align:left">{html.escape(d.get("texto", ""))}</div></div>')
    elif tipo == "cita":
        cuerpo = centro(f'<div style="font-size:200px;line-height:.6;color:#ffd400;font-weight:900">“</div>'
                        f'<div class="grande" style="font-size:76px;font-weight:800;max-width:1500px">{html.escape(g)}</div>'
                        f'<div class="chico" style="font-size:36px">— {html.escape(c)}</div>')
    elif tipo == "imagen":  # imagen de apoyo a pantalla completa (ruta relativa a la raíz del repo), con leyenda y crédito
        src = os.path.join(RAIZ, p["imagen"])
        cuerpo = (f'<img src="file://{src}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover">'
                  '<div style="position:absolute;inset:0;background:linear-gradient(transparent 45%,#0f0f10ee)"></div>'
                  f'<div style="position:absolute;left:120px;right:120px;bottom:110px"><div class="grande" style="font-size:90px">{html.escape(g)}</div>'
                  f'<div class="chico" style="text-align:left;margin-top:16px">{html.escape(c)}</div></div>'
                  + (f'<div style="position:absolute;right:24px;bottom:16px;font-size:20px;color:#ffffff99">{html.escape(p["credito"])}</div>' if p.get("credito") else ""))
    else:
        raise ValueError(f"tipo de escena desconocido: {tipo}")
    pagina = f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{cab}{cuerpo}</body></html>'
    return pagina.replace("#ffd400", MARCA["acento"])


def ejecutar(cmd):
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def duracion(archivo):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", archivo],
                       capture_output=True, text=True, check=True)
    return float(r.stdout.strip())


def elegir_voz(clave):
    if os.environ.get("TTS_VOZ"):
        return os.environ["TTS_VOZ"]
    with urllib.request.urlopen(f"https://texttospeech.googleapis.com/v1/voices?languageCode=es-US&key={clave}") as r:
        nombres = [v["name"] for v in json.load(r).get("voices", [])]
    for v in VOZ_PREFERIDA:
        if v in nombres:
            return v
    for familia in ("Chirp3-HD", "Studio", "Neural2", "Wavenet"):
        candidatas = [n for n in nombres if familia in n]
        if candidatas:
            return candidatas[0]
    return nombres[0]


def sintetizar(texto, voz, clave, salida):
    cuerpo = json.dumps({
        "input": {"text": texto},
        "voice": {"languageCode": "es-US", "name": voz},
        "audioConfig": {"audioEncoding": "LINEAR16", "sampleRateHertz": 48000},
    }).encode()
    req = urllib.request.Request(f"https://texttospeech.googleapis.com/v1/text:synthesize?key={clave}", data=cuerpo,
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as r:
            audio = base64.b64decode(json.load(r)["audioContent"])
    except urllib.error.HTTPError as e:
        sys.exit(f"Error de Text-to-Speech ({e.code}): {e.read().decode()[:400]}")
    with open(salida, "wb") as f:
        f.write(audio)


def tiempo_srt(s):
    h, s = divmod(s, 3600)
    m, s = divmod(s, 60)
    return f"{int(h):02}:{int(m):02}:{int(s):02},{int((s % 1) * 1000):03}"


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    nombre = sys.argv[1]
    sin_voz = "--sin-voz" in sys.argv
    base = os.path.join(RAIZ, "produccion", nombre)
    build = os.path.join(base, "build")
    os.makedirs(build, exist_ok=True)
    spec = json.load(open(os.path.join(base, "escenas.json"), encoding="utf-8"))
    pasos = spec["pasos"]
    global TOTAL_PASOS
    MARCA.update(spec.get("marca", {}))
    TOTAL_PASOS = spec.get("total_pasos", TOTAL_PASOS)

    pdf = os.path.join(base, "documento", "informe.pdf")
    if os.path.exists(pdf):
        ejecutar(["pdftoppm", "-r", "110", "-png", pdf, os.path.join(build, "pag")])
        for f in os.listdir(build):  # pdftoppm nombra pag-01.png; normalizar a pag-1.png
            m = re.fullmatch(r"pag-0*(\d+)\.png", f)
            if m and f != f"pag-{m.group(1)}.png":
                os.replace(os.path.join(build, f), os.path.join(build, f"pag-{m.group(1)}.png"))

    trabajos, cuadros = [], []
    for i, p in enumerate(pasos):
        n = estados(p)
        cuadros.append([])
        for k in range(1, n + 1):
            sufijo = f"-{k}" if n > 1 else ""
            h = os.path.join(build, f"escena-{i:02}{sufijo}.html")
            with open(h, "w", encoding="utf-8") as f:
                f.write(escena_html(p, build, k if n > 1 else None))
            png = os.path.join(build, f"escena-{i:02}{sufijo}.png")
            trabajos.append({"html": h, "out": png, "w": 1920, "h": 1080})
            cuadros[i].append(png)
    with open(os.path.join(build, "trabajos.json"), "w") as f:
        json.dump(trabajos, f)
    render = os.path.join(RAIZ, "produccion", "render")
    if not os.path.isdir(os.path.join(render, "node_modules")):
        subprocess.run(["npm", "ci", "--silent"], cwd=render, check=True)
    ejecutar(["node", os.path.join(render, "render.js"), os.path.join(build, "trabajos.json")])
    print(f"✔ {len(pasos)} escenas renderizadas")

    clave = os.environ.get("GOOGLE_TTS_API_KEY")
    if not sin_voz and not clave:
        sys.exit("Falta GOOGLE_TTS_API_KEY (o usa --sin-voz para una vista previa muda).")
    voz = None if sin_voz else elegir_voz(clave)
    if voz:
        print(f"✔ Voz: {voz}")

    segmentos, srt, capitulos, t = [], [], [], 0.0
    for i, p in enumerate(pasos):
        wav = os.path.join(build, f"voz-{i:02}.wav")
        if sin_voz:
            seg = max(2.5, len(p["voz"].split()) / 2.6)
            ejecutar(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=mono", "-t", f"{seg:.2f}", wav])
        else:
            sintetizar(p["voz"], voz, clave, wav)
        d = duracion(wav) + PAUSA
        frames = int(round(d * FPS))
        mp4 = os.path.join(build, f"seg-{i:02}.mp4")
        # revelado progresivo: los elementos aparecen repartidos en el primer 80 % de la locución
        imgs = cuadros[i]
        marcas = [k * 0.8 * (d - PAUSA) / len(imgs) for k in range(len(imgs))] + [frames / FPS]
        tramos = [marcas[k + 1] - marcas[k] for k in range(len(imgs))]
        entradas, filtros, previo = [], [], "[c0]"
        for k, img in enumerate(imgs):
            largo = tramos[k] + (XFADE if k < len(imgs) - 1 else 0)
            entradas += ["-loop", "1", "-framerate", str(FPS), "-t", f"{largo:.3f}", "-i", img]
            filtros.append(f"[{k}:v]format=yuv420p,setsar=1[c{k}]")
        for k in range(1, len(imgs)):
            filtros.append(f"{previo}[c{k}]xfade=transition=fade:duration={XFADE}:offset={marcas[k]:.3f}[x{k}]")
            previo = f"[x{k}]"
        zoom = f"zoompan=z='min(1+0.00025*on,1.04)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1920x1080:fps={FPS}"
        filtros.append(f"{previo}scale=3840:-1,{zoom},fade=t=in:st=0:d=0.2,format=yuv420p[v]")
        filtros.append(f"[{len(imgs)}:a]apad=pad_dur={PAUSA}[a]")
        ejecutar(["ffmpeg", "-y", *entradas, "-i", wav, "-filter_complex", ";".join(filtros),
                  "-map", "[v]", "-map", "[a]", "-t", f"{frames / FPS:.3f}", "-c:v", "libx264", "-preset", "medium",
                  "-crf", "18", "-c:a", "pcm_s16le", "-ar", "48000", mp4])
        segmentos.append(mp4)
        # subtítulos: una línea por oración, repartida según su largo
        oraciones = [o.strip() for o in re.split(r"(?<=[.!?])\s+", p["voz"]) if o.strip()]
        total = sum(len(o) for o in oraciones)
        ti = t
        for o in oraciones:
            to = ti + (d - PAUSA) * len(o) / total
            srt.append((ti, to, o))
            ti = to
        if p.get("paso") and not any(c[1] == p["paso"] for c in capitulos):
            capitulos.append((t, p["paso"]))
        t += frames / FPS
        print(f"  · paso {i + 1}/{len(pasos)} ({d:.1f} s)")

    lista = os.path.join(build, "segmentos.txt")
    with open(lista, "w") as f:
        f.writelines(f"file '{s}'\n" for s in segmentos)
    salida = os.path.join(base, f"{nombre}{'-preview' if sin_voz else ''}.mp4")
    musica = spec.get("musica")
    if musica and os.path.exists(os.path.join(RAIZ, musica)):
        # la música baja sola cuando habla la voz (sidechain) y queda ~-26 dB por debajo
        mezcla = ("[0:a]asplit=2[voz][guia];[1:a]volume=0.18,afade=t=in:d=2[m];"
                  "[m][guia]sidechaincompress=threshold=0.03:ratio=10:attack=15:release=450[mduck];"
                  f"[voz][mduck]amix=inputs=2:duration=first:normalize=0,afade=t=out:st={max(0, t - 2.5):.2f}:d=2.5,"
                  "loudnorm=I=-14:TP=-1.5:LRA=11[a]")
        ejecutar(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", lista, "-stream_loop", "-1", "-i", os.path.join(RAIZ, musica),
                  "-filter_complex", mezcla, "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                  "-shortest", "-movflags", "+faststart", salida])
        print(f"✔ Música: {musica}")
    else:
        if musica:
            print(f"⚠ No existe {musica}: el video sale sin música")
        ejecutar(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", lista, "-c:v", "copy",
                  "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", salida])

    # la vista previa muda tiene tiempos estimados: no pisa los subtítulos ni capítulos reales
    destino = build if sin_voz else base
    with open(os.path.join(destino, f"{nombre}.srt"), "w", encoding="utf-8") as f:
        for n, (a, b, o) in enumerate(srt, 1):
            f.write(f"{n}\n{tiempo_srt(a)} --> {tiempo_srt(b)}\n{o}\n\n")
    with open(os.path.join(destino, "capitulos.txt"), "w", encoding="utf-8") as f:
        f.write("0:00 Introducción\n")
        for s, n in capitulos:
            f.write(f"{int(s // 60)}:{int(s % 60):02} Paso {n}\n")
    print(f"✔ Video: {salida} ({t / 60:.1f} min)")


if __name__ == "__main__":
    main()
