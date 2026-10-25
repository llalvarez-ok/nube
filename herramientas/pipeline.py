#!/usr/bin/env python3
"""Estado y compuertas de calidad de cada video (protocolo de debate entre agentes).

    python3 herramientas/pipeline.py nuevo video02 "Cómo hacer X con IA" [--canal atajos-ia]
    python3 herramientas/pipeline.py estado                 # todos los videos
    python3 herramientas/pipeline.py estado video02         # detalle e historial
    python3 herramientas/pipeline.py siguiente video02      # qué etapa toca y qué agentes llamar
    python3 herramientas/pipeline.py evaluar video02 guion ronda.json
    python3 herramientas/pipeline.py marcar video02 render            # etapas sin debate
    python3 herramientas/pipeline.py forzar video02 guion "motivo"   # decisión humana

ronda.json (lo arma el orquestador con las respuestas de los críticos):
    {"evaluaciones": [
        {"agente": "critico-retencion", "puntajes": {"hook": 8, "ritmo": 7},
         "objeciones": ["El hook tarda 20 s en mostrar el resultado"]},
        ...]}

Reglas (sistema/rubricas.json): por criterio se promedian los críticos que lo puntuaron;
la nota de la etapa es el promedio ponderado. Se aprueba si la nota >= umbral, ningún
criterio queda bajo su mínimo y ningún criterio con veto queda bajo su mínimo en NINGÚN
crítico. Si no se aprueba tras max_rondas, la etapa se escala al creador.
"""

import datetime
import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRODUCCION = os.path.join(RAIZ, "produccion")
RUBRICAS = json.load(open(os.path.join(RAIZ, "sistema", "rubricas.json"), encoding="utf-8"))
ETAPAS = ["idea", "guion", "visual", "render", "qc", "empaque", "listo", "publicado"]
CON_DEBATE = set(RUBRICAS["etapas"])
AGENTES_SIN_DEBATE = {
    "render": "productor (python3 herramientas/motor.py <video> --alta)",
    "listo": "seo-empaquetador escribe publicacion.md; el creador sube el MP4",
    "publicado": "analista a los 2, 7 y 28 días",
}


def ahora():
    return datetime.datetime.now().isoformat(timespec="seconds")


def ruta_estado(video):
    return os.path.join(PRODUCCION, video, "estado.json")


def cargar(video):
    r = ruta_estado(video)
    if not os.path.exists(r):
        sys.exit(f"{video} no tiene estado.json (créalo con: pipeline.py nuevo {video} \"tema\")")
    return json.load(open(r, encoding="utf-8"))


def guardar(video, estado):
    with open(ruta_estado(video), "w", encoding="utf-8") as f:
        json.dump(estado, f, ensure_ascii=False, indent=2)
        f.write("\n")


def avanzar(estado, etapa):
    i = ETAPAS.index(etapa)
    if ETAPAS.index(estado["etapa"]) <= i and i + 1 < len(ETAPAS):
        estado["etapa"] = ETAPAS[i + 1]


def calificar(etapa, evaluaciones):
    """Devuelve (nota, por_criterio, motivos_de_rechazo)."""
    rub = RUBRICAS["etapas"][etapa]
    criterios = rub["criterios"]
    por_criterio, motivos = {}, []
    for nombre, c in criterios.items():
        notas = [e["puntajes"][nombre] for e in evaluaciones if nombre in e.get("puntajes", {})]
        if not notas:
            motivos.append(f"nadie puntuó «{nombre}»")
            continue
        prom = sum(notas) / len(notas)
        por_criterio[nombre] = round(prom, 2)
        if prom < c["minimo"]:
            motivos.append(f"«{nombre}» {prom:.1f} < mínimo {c['minimo']}")
        if c.get("veto"):
            for e in evaluaciones:
                n = e.get("puntajes", {}).get(nombre)
                if n is not None and n < c["minimo"]:
                    motivos.append(f"veto de {e['agente']} en «{nombre}» ({n})")
    peso = sum(criterios[n]["peso"] for n in por_criterio) or 1
    nota = sum(por_criterio[n] * criterios[n]["peso"] for n in por_criterio) / peso
    if nota < rub["umbral"]:
        motivos.append(f"nota {nota:.2f} < umbral {rub['umbral']}")
    return round(nota, 2), por_criterio, motivos


def cmd_nuevo(video, tema, canal="atajos-ia"):
    base = os.path.join(PRODUCCION, video)
    if os.path.exists(ruta_estado(video)):
        sys.exit(f"{video} ya existe")
    os.makedirs(base, exist_ok=True)
    if not os.path.exists(os.path.join(RAIZ, "canales", canal, "ficha.md")):
        sys.exit(f"No existe canales/{canal}/ficha.md (créalo con /nuevo-canal)")
    guardar(video, {"video": video, "canal": canal, "tema": tema, "creado": ahora(), "etapa": "idea", "historial": []})
    print(f"✔ {video} creado en produccion/{video}/ · canal: {canal} · etapa: idea")


def cmd_estado(video=None):
    if video:
        e = cargar(video)
        print(f"{e['video']} · {e.get('canal', 'atajos-ia')} · {e['tema']} · etapa actual: {e['etapa']}")
        for h in e["historial"]:
            linea = f"  {h['fecha']}  {h['etapa']:<8} ronda {h.get('ronda', '-')}  {h['resultado']:<9}"
            if "nota" in h:
                linea += f" nota {h['nota']}"
            print(linea)
            for m in h.get("motivos", []):
                print(f"      · {m}")
        return
    filas = []
    for d in sorted(os.listdir(PRODUCCION)):
        if os.path.exists(ruta_estado(d)):
            e = cargar(d)
            filas.append(f"  {d:<10} {e['etapa']:<10} {e['tema']}")
    print("\n".join(filas) if filas else "No hay videos con estado.json")


def cmd_siguiente(video):
    e = cargar(video)
    etapa = e["etapa"]
    if etapa in CON_DEBATE:
        rub = RUBRICAS["etapas"][etapa]
        rondas = sum(1 for h in e["historial"] if h["etapa"] == etapa and h["resultado"] != "forzado")
        print(f"Etapa: {etapa} (ronda {rondas + 1} de {RUBRICAS['max_rondas']})")
        print(f"  Autor:    {rub['autor']} → produccion/{video}/{rub['artefacto']}")
        print(f"  Críticos: {', '.join(rub['criticos'])} (en paralelo, sin ver las notas de los otros)")
        if "objetivo" in rub:
            print(f"  Antes:    {rub['objetivo']}")
        print(f"  Umbral:   {rub['umbral']} · criterios: {', '.join(rub['criterios'])}")
        previas = [h for h in e["historial"] if h["etapa"] == etapa and h["resultado"] == "revisar"]
        if previas:
            print("  Objeciones a resolver de la ronda anterior:")
            for o in previas[-1].get("objeciones", []):
                print(f"    · {o}")
    else:
        print(f"Etapa: {etapa} · {AGENTES_SIN_DEBATE.get(etapa, '-')}")


def cmd_evaluar(video, etapa, archivo):
    if etapa not in CON_DEBATE:
        sys.exit(f"La etapa {etapa} no tiene debate. Etapas con debate: {', '.join(sorted(CON_DEBATE))}")
    e = cargar(video)
    ronda = json.load(open(archivo, encoding="utf-8"))
    evaluaciones = ronda["evaluaciones"]
    nota, por_criterio, motivos = calificar(etapa, evaluaciones)
    n = sum(1 for h in e["historial"] if h["etapa"] == etapa and h["resultado"] != "forzado") + 1
    if not motivos:
        resultado = "aprobado"
        avanzar(e, etapa)
    elif n >= RUBRICAS["max_rondas"]:
        resultado = "escalado"
    else:
        resultado = "revisar"
    objeciones = [f"[{ev['agente']}] {o}" for ev in evaluaciones for o in ev.get("objeciones", [])]
    e["historial"].append({"fecha": ahora(), "etapa": etapa, "ronda": n, "resultado": resultado, "nota": nota,
                           "criterios": por_criterio, "motivos": motivos, "objeciones": objeciones})
    guardar(video, e)
    print(f"{etapa} · ronda {n} · nota {nota} · {resultado.upper()}")
    for k, v in por_criterio.items():
        print(f"  {k:<14} {v}")
    for m in motivos:
        print(f"  ✗ {m}")
    if resultado == "escalado":
        print(f"  → {RUBRICAS['max_rondas']} rondas sin aprobar: decide el creador (pipeline.py forzar ...) o se descarta.")
    return resultado


def cmd_forzar(video, etapa, motivo):
    e = cargar(video)
    e["historial"].append({"fecha": ahora(), "etapa": etapa, "resultado": "forzado", "motivos": [motivo]})
    avanzar(e, etapa)
    guardar(video, e)
    print(f"✔ {etapa} aprobado a mano · etapa actual: {e['etapa']}")


def cmd_marcar(video, etapa):
    """Para etapas sin debate (render, listo, publicado)."""
    e = cargar(video)
    e["historial"].append({"fecha": ahora(), "etapa": etapa, "resultado": "hecho"})
    avanzar(e, etapa)
    guardar(video, e)
    print(f"✔ {etapa} hecho · etapa actual: {e['etapa']}")


def main():
    a = sys.argv[1:]
    canal = "atajos-ia"
    if "--canal" in a:
        i = a.index("--canal")
        canal = a[i + 1]
        del a[i:i + 2]
    if not a:
        sys.exit(__doc__)
    c = a[0]
    if c == "nuevo" and len(a) == 3:
        cmd_nuevo(a[1], a[2], canal)
    elif c == "estado":
        cmd_estado(a[1] if len(a) > 1 else None)
    elif c == "siguiente" and len(a) == 2:
        cmd_siguiente(a[1])
    elif c == "evaluar" and len(a) == 4:
        cmd_evaluar(a[1], a[2], a[3])
    elif c == "forzar" and len(a) == 4:
        cmd_forzar(a[1], a[2], a[3])
    elif c == "marcar" and len(a) == 3:
        cmd_marcar(a[1], a[2])
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
