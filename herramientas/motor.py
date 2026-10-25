#!/usr/bin/env python3
"""Motor v2: produce un video animado (motion graphics) a partir de produccion/<video>/guion.json.

    python3 herramientas/motor.py video02                  # video final con voz (Google TTS)
    python3 herramientas/motor.py video02 --sin-voz        # vista previa: tiempos estimados, con efectos de sonido
    python3 herramientas/motor.py video02 --borrador       # 960x540, rápido, para revisar ritmo
    python3 herramientas/motor.py video02 --alta           # 2560x1440 (YouTube asigna mejor códec y bitrate)
    python3 herramientas/motor.py video02 --cuadros 3,12.5,40   # solo capturas PNG en esos segundos (revisión visual)
    python3 herramientas/motor.py video02 --desde 30 --hasta 60 # solo un tramo

guion.json:
    {"titulo": "...", "marca": {"nombre": "Atajos IA", "acento": "#ffd400"}, "musica": "produccion/musica/x.mp3",
     "subtitulos": false, "escenas": [
        {"plantilla": "titular|cifra|antes_despues|lista|capitulo|aviso|comparar|excel|chat|final",
         "capitulo": "Título del capítulo (opcional)", "transicion": "empuje|zoom|barrido|fundido|corte",
         "datos": {...}, "beats": [{"voz": "Una o dos frases.", "voz_tts": "(opcional, pronunciación)", "accion": {...}}]}]}

Cada beat se sintetiza por separado, así las animaciones caen justo cuando la voz las nombra.
Ver sistema/motor-v2.md para el catálogo de plantillas y acciones.
"""

import array
import hashlib
import json
import math
import os
import random
import re
import shutil
import subprocess
import sys
import wave

sys.path.insert(0, os.path.dirname(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RENDER = os.path.join(RAIZ, "produccion", "render")
MOTOR = os.path.join(RENDER, "motor")
SR = 48000
PALABRAS_POR_SEG = 2.6
ICONOS_BASE = ["sheet", "sparkles", "clipboard-paste", "bold", "italic", "underline", "align-left", "align-center", "percent",
               "dollar-sign", "sigma", "funnel", "chart-column", "table", "paint-bucket", "triangle-alert"]


# ---------------------------------------------------------------- efectos de sonido (sintetizados, sin licencias)
def _env(n, ataque, caida):
    a, c = max(1, int(ataque * SR)), max(1, int(caida * SR))
    return [min(1, i / a) * (math.exp(-max(0, i - a) / c)) for i in range(n)]


def _ruido_filtrado(n, corte_ini, corte_fin, semilla):
    rnd = random.Random(semilla)
    y, out = 0.0, []
    for i in range(n):
        fc = corte_ini + (corte_fin - corte_ini) * (i / n)
        k = 1 - math.exp(-2 * math.pi * fc / SR)
        y += k * (rnd.uniform(-1, 1) - y)
        out.append(y)
    pico = max(abs(v) for v in out) or 1
    return [v / pico for v in out]


def _tono(n, f0, f1, decaimiento, armonicos=(1,)):
    out, fase = [], 0.0
    for i in range(n):
        f = f0 + (f1 - f0) * (i / n)
        fase += 2 * math.pi * f / SR
        v = sum(math.sin(fase * h) / (j + 1) for j, h in enumerate(armonicos))
        out.append(v * math.exp(-i / (decaimiento * SR)))
    return out


def sintetizar_sfx(destino):
    os.makedirs(destino, exist_ok=True)

    def guardar(nombre, muestras, gan=0.8):
        pico = max(abs(v) for v in muestras) or 1
        with wave.open(os.path.join(destino, nombre + ".wav"), "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
            w.writeframes(array.array("h", (int(v / pico * gan * 32000) for v in muestras)).tobytes())

    def whoosh(dur, c0, c1, sem, pico_en=0.45):
        n = int(dur * SR)
        r = _ruido_filtrado(n, c0, c1, sem)

        def env(x):
            return math.sin(math.pi / 2 * x / pico_en) ** 2 if x < pico_en else math.cos(math.pi / 2 * (x - pico_en) / (1 - pico_en)) ** 2
        return [r[i] * env(i / n) for i in range(n)]

    guardar("whoosh", whoosh(0.55, 400, 5000, 1), 0.7)
    guardar("whoosh_suave", whoosh(0.45, 300, 2500, 2), 0.45)
    guardar("zoom", whoosh(0.9, 200, 3500, 3, 0.6), 0.5)
    n = int(0.035 * SR)
    clic = _ruido_filtrado(n, 6000, 3000, 4)
    guardar("clic", [clic[i] * math.exp(-i / (0.006 * SR)) + 0.4 * math.sin(2 * math.pi * 1800 * i / SR) * math.exp(-i / (0.004 * SR)) for i in range(n)], 0.55)
    guardar("pop", _tono(int(0.12 * SR), 520, 980, 0.035, (1, 2)), 0.5)
    guardar("ding", [a + b for a, b in zip(_tono(int(0.9 * SR), 1318, 1318, 0.25), _tono(int(0.9 * SR), 1975, 1975, 0.18))], 0.4)
    guardar("subida", [v * min(1, i / (0.1 * SR)) for i, v in enumerate(_tono(int(0.8 * SR), 280, 840, 0.6, (1, 2, 3)))], 0.3)
    alerta = _tono(int(0.16 * SR), 880, 880, 0.08) + [0] * int(0.05 * SR) + _tono(int(0.22 * SR), 660, 660, 0.1)
    guardar("alerta", alerta, 0.45)
    guardar("enviar", _tono(int(0.18 * SR), 600, 1200, 0.06), 0.35)
    notas = []
    for f in (880, 1108, 1318):
        notas += _tono(int(0.11 * SR), f, f, 0.08)
    guardar("respuesta", notas, 0.25)
    guardar("brillo", [sum(math.sin(2 * math.pi * f * i / SR) for f in (2093, 2637, 3136)) * math.exp(-i / (0.25 * SR)) for i in range(int(0.7 * SR))], 0.22)
    rnd = random.Random(9)
    arr = _ruido_filtrado(int(1.2 * SR), 800, 1600, 5)
    guardar("arrastre", [v * 0.6 * (0.6 + 0.4 * math.sin(i / SR * 40)) for i, v in enumerate(arr)], 0.25)
    # tecleo y tictac: pistas largas que se recortan a la duración del evento
    tec = [0.0] * int(6 * SR)
    t = 0.02
    while t < 5.9:
        i0 = int(t * SR)
        golpe = _ruido_filtrado(int(0.03 * SR), 5000, 2500, rnd.randint(0, 9999))
        amp = rnd.uniform(0.5, 1)
        for j, v in enumerate(golpe):
            tec[i0 + j] += v * amp * math.exp(-j / (0.005 * SR))
        t += rnd.uniform(0.055, 0.12)
    guardar("tecleo", tec, 0.35)
    tic = [0.0] * int(4 * SR)
    for k in range(int(4 / 0.12)):
        i0 = int(k * 0.12 * SR)
        for j, v in enumerate(_tono(int(0.02 * SR), 3000 if k % 2 else 2400, 2400, 0.004)):
            tic[i0 + j] += v
    guardar("tic", tic, 0.3)


# ---------------------------------------------------------------- audio
def leer_wav(ruta):
    with wave.open(ruta, "rb") as w:
        if w.getframerate() != SR or w.getnchannels() != 1 or w.getsampwidth() != 2:
            tmp = ruta + ".48k.wav"
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", ruta, "-ac", "1", "-ar", str(SR), "-sample_fmt", "s16", tmp], check=True)
            return leer_wav(tmp)
        return array.array("h", w.readframes(w.getnframes()))


def escribir_wav(ruta, muestras_f):
    with wave.open(ruta, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(array.array("h", (max(-32767, min(32767, int(v))) for v in muestras_f)).tobytes())


def mezclar_en(pista, muestras, t, gan=1.0, dur=None):
    i0 = int(t * SR)
    n = len(muestras) if dur is None else min(len(muestras), int(dur * SR))
    fade = int(0.03 * SR)
    for j in range(n):
        k = i0 + j
        if k >= len(pista):
            break
        g = gan * (min(1, (n - j) / fade) if dur is not None else 1)
        pista[k] += muestras[j] * g


# ---------------------------------------------------------------- tiempos
def palabras(t):
    return len(re.findall(r"\w+", t))


def armar_tiempos(guion, duraciones):
    t = 0.0
    for es in guion["escenas"]:
        es["inicio"] = round(t, 3)
        cursor = t + es.get("entrada", 0.45 if es["plantilla"] not in ("capitulo",) else 0.35)
        for b in es["beats"]:
            d = duraciones[id(b)]
            b["t"] = round(cursor - t, 3)
            b["d"] = round(d, 3)
            texto = b.get("voz", "")
            trozos, acum = [], 0
            ws = texto.split()
            grupos = [" ".join(ws[i:i + 6]) for i in range(0, len(ws), 6)]
            total = sum(len(g) for g in grupos) or 1
            for g in grupos:
                trozos.append({"t": round(b["t"] + d * acum / total, 3), "texto": g})
                acum += len(g)
            b["trozos"] = trozos
            cursor += d + b.get("pausa", 0.3)
        fin = cursor + es.get("cola", 0.35) + es.get("extra", 0)
        if es["plantilla"] == "final":
            fin = max(fin, t + es.get("minimo", 20))
        if es["plantilla"] == "capitulo":
            fin = max(fin, t + 2.2)
        es["dur"] = round(fin - t, 3)
        t = fin
    guion["duracion"] = round(t, 3)


def recolectar_iconos(obj, salida):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "icono" and isinstance(v, str):
                salida.add(v)
            else:
                recolectar_iconos(v, salida)
    elif isinstance(obj, list):
        for v in obj:
            recolectar_iconos(v, salida)


def cargar_iconos(nombres):
    carpeta = os.path.join(RENDER, "node_modules", "lucide-static", "icons")
    out = {}
    for n in nombres:
        p = os.path.join(carpeta, n + ".svg")
        if os.path.exists(p):
            out[n] = re.sub(r"<!--.*?-->", "", open(p, encoding="utf-8").read(), flags=re.S).strip()
        else:
            print(f"⚠ ícono desconocido: {n}")
    return out


def pagina(build, guion):
    fuentes = os.path.join(RENDER, "fonts")
    ff = "".join(f"@font-face{{font-family:Inter;font-weight:{w};src:url(file://{fuentes}/inter-latin-{w}-normal.woff2)}}"
                 f"@font-face{{font-family:Inter;font-weight:{w};src:url(file://{fuentes}/inter-latin-ext-{w}-normal.woff2);unicode-range:U+0100-024F}}"
                 for w in (400, 600, 800, 900))
    with open(os.path.join(build, "datos.js"), "w", encoding="utf-8") as f:
        f.write("window.GUION = " + json.dumps(guion, ensure_ascii=False) + ";")
    gs = os.path.join(RENDER, "node_modules", "gsap", "dist")
    html = f"""<!doctype html><html><head><meta charset="utf-8"><style>{ff}</style>
<link rel="stylesheet" href="file://{MOTOR}/estilos.css"></head><body>
<div id="fondo"><div class="mancha m1"></div><div class="mancha m2"></div><div class="mancha m3"></div><div id="reticula"></div><div id="grano"></div><div id="vineta"></div></div>
<div id="escenas"></div><div id="barridos"></div><div id="marca"></div><div id="subtitulos"></div><div id="progreso"><div class="barra"></div></div>
<script src="file://{gs}/gsap.min.js"></script><script src="file://{gs}/TextPlugin.min.js"></script>
<script src="file://{build}/datos.js"></script><script src="file://{MOTOR}/motor.js"></script></body></html>"""
    ruta = os.path.join(build, "motor.html")
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(html)
    return ruta


def tiempo_srt(s):
    h, s = divmod(s, 3600)
    m, s = divmod(s, 60)
    return f"{int(h):02}:{int(m):02}:{int(s):02},{int((s % 1) * 1000):03}"


def opcion(n, d=None):
    return sys.argv[sys.argv.index(n) + 1] if n in sys.argv else d


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    valores = {opcion(o) for o in ("--cuadros", "--desde", "--hasta", "--workers")}
    args = [a for a in args if a not in valores]
    if not args:
        sys.exit(__doc__)
    nombre = args[0]
    sin_voz = "--sin-voz" in sys.argv
    base = os.path.join(RAIZ, "produccion", nombre)
    build = os.path.join(base, "build")
    os.makedirs(os.path.join(build, "voz"), exist_ok=True)
    guion = json.load(open(os.path.join(base, "guion.json"), encoding="utf-8"))
    if not os.path.isdir(os.path.join(RENDER, "node_modules", "gsap")):
        subprocess.run(["npm", "ci", "--silent"], cwd=RENDER, check=True)

    # 1) voz por beat (o duración estimada)
    clave = os.environ.get("GOOGLE_TTS_API_KEY")
    cuadros = opcion("--cuadros")
    if not sin_voz and not clave and not cuadros:
        sys.exit("Falta GOOGLE_TTS_API_KEY (o usa --sin-voz para una vista previa con tiempos estimados).")
    voz = None
    if clave and not sin_voz:
        from producir_video import elegir_voz, sintetizar
        voz = elegir_voz(clave)
        print(f"✔ Voz: {voz}")
    duraciones, wavs = {}, {}
    for es in guion["escenas"]:
        for b in es["beats"]:
            texto = b.get("voz_tts") or b.get("voz", "")
            if not texto.strip():
                duraciones[id(b)] = b.get("duracion", 1.2)
                continue
            if voz:
                h = hashlib.sha1(f"{voz}|{texto}".encode()).hexdigest()[:16]
                ruta = os.path.join(build, "voz", h + ".wav")
                if not os.path.exists(ruta):
                    sintetizar(texto, voz, clave, ruta)
                wavs[id(b)] = ruta
                with wave.open(ruta, "rb") as w:
                    duraciones[id(b)] = w.getnframes() / w.getframerate()
            else:
                duraciones[id(b)] = max(1.0, palabras(b.get("voz", "")) / PALABRAS_POR_SEG)
    armar_tiempos(guion, duraciones)
    iconos = set(ICONOS_BASE)
    recolectar_iconos(guion, iconos)
    guion["iconos"] = cargar_iconos(sorted(iconos))
    html = pagina(build, guion)
    print(f"✔ {len(guion['escenas'])} escenas · {guion['duracion'] / 60:.1f} min")

    escala = "0.5" if "--borrador" in sys.argv else ("1.3333" if "--alta" in sys.argv else "1")
    grabar = os.path.join(RENDER, "grabar.js")
    if cuadros:
        destino = os.path.join(build, "cuadros")
        os.makedirs(destino, exist_ok=True)
        subprocess.run(["node", os.path.join(RENDER, "capturar.js"), html, destino, cuadros, "--escala", escala], check=True)
        return

    # 2) video
    video_mudo = os.path.join(build, "video-mudo.mp4")
    cmd = ["node", grabar, html, video_mudo, "--escala", escala, "--workers", opcion("--workers", "3")]
    for o in ("--desde", "--hasta"):
        if opcion(o):
            cmd += [o, opcion(o)]
    subprocess.run(cmd, check=True)
    desde = float(opcion("--desde", 0))
    sfx = json.load(open(video_mudo + ".sfx.json"))

    # 3) audio: voz + efectos (+ música con ducking)
    dur = guion["duracion"]
    voz_pista = array.array("f", bytes(4 * int(dur * SR + SR)))
    for es in guion["escenas"]:
        for b in es["beats"]:
            if id(b) in wavs:
                mezclar_en(voz_pista, leer_wav(wavs[id(b)]), es["inicio"] + b["t"])
    sfx_dir = os.path.join(RENDER, "sfx")
    if not os.path.exists(os.path.join(sfx_dir, "tic.wav")):
        sintetizar_sfx(sfx_dir)
    cache = {}
    ganancias = guion.get("sfx_ganancia", {})
    sfx_pista = array.array("f", bytes(4 * int(dur * SR + SR)))
    for ev in sfx:
        if ev["n"] not in cache:
            p = os.path.join(sfx_dir, ev["n"] + ".wav")
            cache[ev["n"]] = leer_wav(p) if os.path.exists(p) else array.array("h")
        mezclar_en(sfx_pista, cache[ev["n"]], ev["t"], ganancias.get(ev["n"], 1.0), ev.get("dur"))
    voz_wav, sfx_wav = os.path.join(build, "voz.wav"), os.path.join(build, "sfx.wav")
    escribir_wav(voz_wav, voz_pista)
    escribir_wav(sfx_wav, sfx_pista)
    salida = os.path.join(base, f"{nombre}{'-preview' if sin_voz else ''}.mp4")
    musica = guion.get("musica")
    entradas = ["-i", video_mudo, "-ss", str(desde), "-i", voz_wav, "-ss", str(desde), "-i", sfx_wav]
    nivel_sfx = guion.get("nivel_sfx", 0.55)
    if musica and os.path.exists(os.path.join(RAIZ, musica)):
        entradas += ["-stream_loop", "-1", "-i", os.path.join(RAIZ, musica)]
        filtro = (f"[1:a]asplit=2[v][guia];[2:a]volume={nivel_sfx}[s];[3:a]volume={guion.get('nivel_musica', 0.16)},afade=t=in:d=2[m];"
                  "[m][guia]sidechaincompress=threshold=0.02:ratio=8:attack=20:release=500[md];"
                  "[v][s][md]amix=inputs=3:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]")
    else:
        if musica:
            print(f"⚠ No existe {musica}: sale sin música")
        filtro = f"[2:a]volume={nivel_sfx}[s];[1:a][s]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *entradas, "-filter_complex", filtro, "-map", "0:v", "-map", "[a]",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", salida], check=True)

    # 4) subtítulos y capítulos (la vista previa los deja en build/)
    destino = build if sin_voz else base
    with open(os.path.join(destino, f"{nombre}.srt"), "w", encoding="utf-8") as f:
        n = 0
        for es in guion["escenas"]:
            for b in es["beats"]:
                oraciones = [o.strip() for o in re.split(r"(?<=[.!?])\s+", b.get("voz", "")) if o.strip()]
                total = sum(len(o) for o in oraciones) or 1
                ti = es["inicio"] + b["t"]
                for o in oraciones:
                    to = ti + b["d"] * len(o) / total
                    n += 1
                    f.write(f"{n}\n{tiempo_srt(ti)} --> {tiempo_srt(to)}\n{o}\n\n")
                    ti = to
    caps = [(es["inicio"], es["capitulo"]) for es in guion["escenas"] if es.get("capitulo")]
    with open(os.path.join(destino, "capitulos.txt"), "w", encoding="utf-8") as f:
        if not caps or caps[0][0] > 0:
            f.write("0:00 Introducción\n")
        for s, c in caps:
            f.write(f"{int(s // 60)}:{int(s % 60):02} {c}\n")
    print(f"✔ Video: {os.path.relpath(salida, RAIZ)} ({dur / 60:.1f} min)")


if __name__ == "__main__":
    main()
