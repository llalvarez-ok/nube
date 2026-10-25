#!/usr/bin/env python3
"""Recorta un Short vertical (1080x1920) de un video largo ya renderizado.

    python3 herramientas/shorts.py video02 0:12 0:52 --titulo "El truco del paso 3"
    python3 herramientas/shorts.py video02 1:30 2:20 --titulo "..." --salida short2

Diseño: el cuadro 16:9 al centro, el mismo cuadro desenfocado de fondo, el título
arriba y los subtítulos del tramo quemados abajo (los Shorts se miran sin sonido).
Máximo 60 s para que entre en el estante de Shorts sin dudas. El agente
seo-empaquetador elige los tramos: un solo punto, que se entienda sin el video largo,
y que termine con una frase que mande al video completo.
"""

import os
import re
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FUENTES = ["/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]


def seg(t):
    partes = [float(x) for x in t.split(":")]
    s = 0.0
    for p in partes:
        s = s * 60 + p
    return s


def srt_tiempo(s):
    h, s = divmod(max(0, s), 3600)
    m, s = divmod(s, 60)
    return f"{int(h):02}:{int(m):02}:{int(s):02},{int((s % 1) * 1000):03}"


def recortar_srt(origen, desde, hasta, destino):
    bloques = open(origen, encoding="utf-8").read().strip().split("\n\n")
    salida = []
    for b in bloques:
        lineas = b.splitlines()
        m = re.match(r"(\S+) --> (\S+)", lineas[1]) if len(lineas) > 2 else None
        if not m:
            continue
        a, z = (seg(x.replace(",", ".")) for x in m.groups())
        if z <= desde or a >= hasta:
            continue
        salida.append(f"{len(salida) + 1}\n{srt_tiempo(max(a, desde) - desde)} --> {srt_tiempo(min(z, hasta) - desde)}\n" + "\n".join(lineas[2:]))
    with open(destino, "w", encoding="utf-8") as f:
        f.write("\n\n".join(salida) + "\n")
    return bool(salida)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    titulo = sys.argv[sys.argv.index("--titulo") + 1] if "--titulo" in sys.argv else ""
    nombre_salida = sys.argv[sys.argv.index("--salida") + 1] if "--salida" in sys.argv else None
    args = [a for a in args if a not in (titulo, nombre_salida)]
    if len(args) < 3:
        sys.exit(__doc__)
    video, desde, hasta = args[0], seg(args[1]), seg(args[2])
    if hasta - desde > 60:
        sys.exit(f"El tramo dura {hasta - desde:.0f} s: un Short debe durar 60 s o menos.")
    base = os.path.join(RAIZ, "produccion", video)
    origen = os.path.join(base, f"{video}.mp4")
    if not os.path.exists(origen):
        sys.exit(f"No existe {origen}")
    os.makedirs(os.path.join(base, "shorts"), exist_ok=True)
    nombre = nombre_salida or f"short-{int(desde)}-{int(hasta)}"
    salida = os.path.join(base, "shorts", f"{nombre}.mp4")
    fuente = next((f for f in FUENTES if os.path.exists(f)), None)

    filtro = ("[0:v]split[a][b];"
              "[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=40:4,eq=brightness=-0.25[fondo];"
              "[b]scale=1080:-2[frente];[fondo][frente]overlay=0:(H-h)/2-60")
    if titulo and fuente:
        texto = titulo.replace("\\", "\\\\").replace(":", "\\:").replace("'", "’")
        filtro += (f",drawtext=fontfile={fuente}:text='{texto}':fontsize=74:fontcolor=white:"
                   "x=(w-text_w)/2:y=330:box=1:boxcolor=black@0.55:boxborderw=28")
    srt = os.path.join(base, f"{video}.srt")
    tramo = os.path.join(base, "shorts", f"{nombre}.srt")
    if os.path.exists(srt) and recortar_srt(srt, desde, hasta, tramo):
        estilo = "FontName=Inter,Bold=1,Fontsize=13,PrimaryColour=&H0000D4FF,OutlineColour=&H00000000,Outline=3,Alignment=2,MarginV=55"
        filtro += f",subtitles={tramo}:force_style='{estilo}'"
    filtro += "[v]"
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{desde:.2f}", "-t", f"{hasta - desde:.2f}", "-i", origen,
           "-filter_complex", filtro, "-map", "[v]", "-map", "0:a", "-c:v", "libx264", "-crf", "19", "-preset", "medium",
           "-af", f"afade=t=out:st={max(0, hasta - desde - 0.6):.2f}:d=0.6,loudnorm=I=-14:TP=-1.5",
           "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", salida]
    subprocess.run(cmd, check=True)
    print(f"✔ {os.path.relpath(salida, RAIZ)} ({hasta - desde:.0f} s)")


if __name__ == "__main__":
    main()
