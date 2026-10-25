#!/usr/bin/env python3
"""Mide las metas de ritmo del guion de video02 con los tiempos estimados del motor (sin voz).

    python3 produccion/video02/fuente/metas.py
"""
import json
import sys

sys.path.insert(0, "/home/user/nube/herramientas")
import motor  # noqa: E402

g = json.load(open("/home/user/nube/produccion/video02/guion.json", encoding="utf-8"))
dur = {id(b): max(1.0, motor.palabras(b.get("voz", "")) / motor.PALABRAS_POR_SEG) + b.get("pausa", 0) * 0
       for es in g["escenas"] for b in es["beats"]}
motor.armar_tiempos(g, dur)
total = g["duracion"]
fmt = lambda s: f"{int(s // 60)}:{int(s % 60):02}"

excel = sum(es["dur"] for es in g["escenas"] if es["plantilla"] == "excel")
larga = max((es["dur"], i) for i, es in enumerate(g["escenas"]) if es["plantilla"] == "excel")
fuertes = [es["inicio"] for es in g["escenas"] if es["plantilla"] in ("capitulo", "antes_despues", "cifra", "aviso")]
cortes = [0.0] + fuertes + [total]
hueco = max(b - a for a, b in zip(cortes, cortes[1:]))

# fórmula 1: momento en que aparece en pantalla (respuesta del chat 1 con la fórmula)
f1 = None
for es in g["escenas"]:
    for b in es["beats"]:
        for a in [*([b["accion"]] if isinstance(b.get("accion"), dict) else []), *b.get("acciones", [])]:
            if f1 is None and a.get("tipo") in ("respuesta", "escribir") and "BUSCARX" in (a.get("formula") or a.get("texto") or ""):
                f1 = es["inicio"] + b["t"] + a.get("retraso", 0)
# zoom en calcular y nota
malos = []
for i, es in enumerate(g["escenas"]):
    if es["plantilla"] != "excel":
        continue
    acc = []
    for b in es["beats"]:
        for a in [*([b["accion"]] if isinstance(b.get("accion"), dict) else []), *b.get("acciones", [])]:
            acc.append((b["t"] + a.get("retraso", 0), a))
    escala = 1.0
    for t, a in sorted(acc, key=lambda x: x[0]):
        if a["tipo"] == "zoom":
            escala = a.get("escala", 1.6)
        elif a["tipo"] == "zoom_fuera":
            escala = 1.0
        elif a["tipo"] in ("calcular", "nota") and escala < 1.6 and not es["datos"].get("solo_video"):
            malos.append(f"escena {i} {a['tipo']} {a.get('celda')} a {escala}x")
cierre = [es for es in g["escenas"] if es["plantilla"] == "titular"][-1]

print(f"Duración estimada: {fmt(total)} ({total:.0f} s)")
print(f"Fórmula 1 en pantalla: {fmt(f1)}")
print(f"Excel: {excel / total * 100:.0f} % del tiempo")
print(f"Escena excel más larga: {larga[0]:.0f} s (escena {larga[1]})")
print(f"Mayor hueco entre cambios fuertes: {hueco:.0f} s")
print(f"calcular/nota con zoom < 1,6x: {len(malos)} {malos}")
print(f"Cierre (titular antes de final): {cierre['dur']:.0f} s")
for i, es in enumerate(g["escenas"]):
    print(f"  {i:2} {fmt(es['inicio'])} {es['dur']:5.1f}s {es['plantilla']:13} {es.get('capitulo', '')[:45]}")
