#!/usr/bin/env python3
"""Control de calidad técnico de un video renderizado.

    python3 herramientas/qc_video.py video02            # produccion/video02/video02.mp4
    python3 herramientas/qc_video.py ruta/al/video.mp4 --json

Revisa resolución, fps, códecs, sonoridad integrada (-14 LUFS ±1) y pico real,
silencios de más de 2 s, tramos negros o congelados y que los subtítulos cubran el
video. Además genera produccion/<video>/build/hoja-de-contactos.png (1 cuadro cada
N segundos) para que el agente editor-qc la mire y juzgue lo que no se puede medir.
"""

import json
import os
import re
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def correr(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def probe(archivo):
    r = correr(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", archivo])
    if r.returncode:
        sys.exit(f"ffprobe no pudo leer {archivo}: {r.stderr[:300]}")
    return json.loads(r.stdout)


def analizar(archivo, srt=None, hoja=None):
    errores, avisos = [], []
    info = probe(archivo)
    dur = float(info["format"]["duration"])
    v = next((s for s in info["streams"] if s["codec_type"] == "video"), None)
    a = next((s for s in info["streams"] if s["codec_type"] == "audio"), None)
    if not v:
        return {"errores": ["No hay pista de video"], "avisos": [], "duracion_s": dur}
    if (v["width"], v["height"]) not in ((1920, 1080), (3840, 2160), (1080, 1920)):
        errores.append(f"Resolución {v['width']}x{v['height']} (se espera 1920x1080 o 1080x1920 para Shorts)")
    num, den = map(int, v["r_frame_rate"].split("/"))
    fps = num / den
    if abs(fps - 30) > 0.5 and abs(fps - 60) > 0.5:
        avisos.append(f"{fps:.2f} fps (se recomienda 30 o 60)")
    if v["codec_name"] != "h264":
        avisos.append(f"Códec de video {v['codec_name']} (h264 es el más seguro)")
    if not a:
        errores.append("No hay pista de audio")
    elif a["codec_name"] != "aac":
        avisos.append(f"Códec de audio {a['codec_name']} (se recomienda aac)")

    # Sonoridad, silencios, negro y congelado en una sola pasada
    filtros_a = "ebur128=peak=true,silencedetect=n=-45dB:d=2"
    filtros_v = "blackdetect=d=0.5:pix_th=0.08,freezedetect=n=0.003:d=6"
    r = correr(["ffmpeg", "-hide_banner", "-nostats", "-i", archivo, "-af", filtros_a, "-vf", filtros_v, "-f", "null", "-"])
    log = r.stderr
    lufs = re.findall(r"I:\s+(-?[\d.]+) LUFS", log)
    pico = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", log)
    integrada = float(lufs[-1]) if lufs else None
    pico_real = float(pico[-1]) if pico else None
    if integrada is not None and archivo.endswith("-preview.mp4"):
        avisos.append(f"Vista previa sin voz: sonoridad {integrada} LUFS no se controla")
    elif integrada is not None and abs(integrada + 14) > 1:
        errores.append(f"Sonoridad {integrada} LUFS (objetivo -14 ±1)")
    if pico_real is not None and pico_real > -1.0:
        avisos.append(f"Pico real {pico_real} dBFS (ideal <= -1)")
    for ini, fin in zip(re.findall(r"silence_start: ([\d.]+)", log), re.findall(r"silence_end: ([\d.]+)", log)):
        if float(ini) > 1 and float(fin) < dur - 3:
            (avisos if archivo.endswith("-preview.mp4") else errores).append(f"Silencio de {float(fin) - float(ini):.1f} s en {fmt(float(ini))}")
    for ini, d in re.findall(r"black_start:([\d.]+) black_end:[\d.]+ black_duration:([\d.]+)", log):
        errores.append(f"Pantalla negra de {float(d):.1f} s en {fmt(float(ini))}")
    for ini in re.findall(r"freeze_start: ([\d.]+)", log):
        avisos.append(f"Imagen casi quieta más de 6 s desde {fmt(float(ini))} (¿falta movimiento o cambio de escena?)")

    # Subtítulos
    if srt and os.path.exists(srt):
        tiempos = re.findall(r"(\d+):(\d+):(\d+),(\d+) --> (\d+):(\d+):(\d+),(\d+)", open(srt, encoding="utf-8").read())
        if tiempos:
            h, m, s, ms = map(int, tiempos[-1][4:])
            fin = h * 3600 + m * 60 + s + ms / 1000
            if fin > dur + 0.5:
                errores.append(f"Los subtítulos terminan en {fmt(fin)}, después del video ({fmt(dur)})")
            elif fin < dur - 15:
                avisos.append(f"Los subtítulos terminan en {fmt(fin)} y el video dura {fmt(dur)}")
    elif srt:
        avisos.append("No hay archivo de subtítulos .srt")

    # Hoja de contactos para revisión visual
    if hoja:
        paso = max(5, dur / 24)
        os.makedirs(os.path.dirname(hoja), exist_ok=True)
        correr(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", archivo, "-vf",
                f"fps=1/{paso:.2f},scale=480:-1,drawtext=text='%{{pts\\:hms}}':x=8:y=8:fontsize=22:fontcolor=white:box=1:boxcolor=black@0.6,tile=4x6",
                "-frames:v", "1", hoja])

    return {"archivo": archivo, "duracion_s": round(dur, 1), "resolucion": f"{v['width']}x{v['height']}",
            "fps": round(fps, 2), "lufs": integrada, "pico_real_dbfs": pico_real,
            "errores": errores, "avisos": avisos, "hoja_de_contactos": hoja if hoja and os.path.exists(hoja) else None,
            "aprobado": not errores}


def fmt(s):
    return f"{int(s // 60)}:{int(s % 60):02}"


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit(__doc__)
    if args[0].endswith(".mp4"):
        archivo, srt, hoja = args[0], None, None
    else:
        base = os.path.join(RAIZ, "produccion", args[0])
        archivo = os.path.join(base, f"{args[0]}.mp4")
        srt = os.path.join(base, f"{args[0]}.srt")
        if not os.path.exists(archivo):  # vista previa muda: sus subtítulos estimados quedan en build/
            archivo = os.path.join(base, f"{args[0]}-preview.mp4")
            srt = os.path.join(base, "build", f"{args[0]}.srt")
        hoja = os.path.join(base, "build", "hoja-de-contactos.png")
    if not os.path.exists(archivo):
        sys.exit(f"No existe {archivo}. Renderízalo con producir_video.py.")
    r = analizar(archivo, srt, hoja)
    if "--json" in sys.argv:
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return
    print(f"{'✔ APROBADO' if r['aprobado'] else '✗ RECHAZADO'} · {r['resolucion']} · {r['fps']} fps · "
          f"{fmt(r['duracion_s'])} · {r['lufs']} LUFS · pico {r['pico_real_dbfs']} dBFS")
    for e in r["errores"]:
        print(f"  ✗ {e}")
    for a in r["avisos"]:
        print(f"  · {a}")
    if r["hoja_de_contactos"]:
        print(f"  Hoja de contactos: {os.path.relpath(r['hoja_de_contactos'], RAIZ)}")


if __name__ == "__main__":
    main()
