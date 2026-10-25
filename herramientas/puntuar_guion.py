#!/usr/bin/env python3
"""Control objetivo de retención de un guion (produccion/<video>/escenas.json).

    python3 herramientas/puntuar_guion.py video02          # informe legible
    python3 herramientas/puntuar_guion.py video02 --json   # para los agentes

No reemplaza a los críticos: detecta lo medible (hook, ritmo, escenas largas, frases
largas, relleno, CTA temprano, promesa del título) para que el debate se concentre en
lo que no se puede medir. Nota de 0 a 100; el guion pasa a los críticos con >= 80.
"""

import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PALABRAS_POR_SEG = 2.6  # ritmo medido de la voz Chirp 3 HD en español (~156 ppm)
SALUDOS = r"\b(hola|bienvenid[oa]s?|en este video|en el video de hoy|qué tal|antes de empezar)\b"
BUCLES = r"(al final|en el paso \w+|más adelante|enseguida|truco|secreto|casi nadie|te muestro|vas a ver|ya verás|pero hay|sorpresa)"
REENGANCHES = r"(\?|pero |ahora viene|y aquí|atención|ojo|lo importante|el truco|esto cambia|fíjate|mira )"
RELLENO = r"\b(básicamente|literalmente|realmente|simplemente|obviamente|digamos|o sea|en fin|bueno,)\b"
VACIAS = set("a al como con cualquier de del el en es la las lo los más mi para por que qué se sin su tu un una y o con ia".split())


def oraciones(t):
    return [o.strip() for o in re.split(r"(?<=[.!?])\s+", t) if o.strip()]


def palabras(t):
    return re.findall(r"[\wáéíóúñü%$]+", t.lower())


def analizar(spec):
    pasos = spec["pasos"]
    problemas = []  # (penalización, mensaje)
    t, tiempos = 0.0, []
    for i, p in enumerate(pasos):
        d = len(palabras(p.get("voz", ""))) / PALABRAS_POR_SEG + 0.35
        tiempos.append((t, d))
        t += d
    total = t

    def at(seg):
        return f"{int(seg // 60)}:{int(seg % 60):02}"

    # Hook: primeros 15 y 30 segundos
    hook15 = " ".join(p.get("voz", "") for p, (ti, _) in zip(pasos, tiempos) if ti < 15)
    hook30 = " ".join(p.get("voz", "") for p, (ti, _) in zip(pasos, tiempos) if ti < 30)
    if re.search(SALUDOS, hook15, re.I):
        problemas.append((15, "Hook: hay saludo o 'en este video' en los primeros 15 s. Empieza por el resultado."))
    primera = oraciones(pasos[0].get("voz", ""))[:1]
    if primera and len(palabras(primera[0])) > 22:
        problemas.append((8, f"Hook: la primera frase tiene {len(palabras(primera[0]))} palabras (ideal <= 22)."))
    if not re.search(BUCLES, hook30, re.I):
        problemas.append((10, "Hook: no hay bucle abierto en los primeros 30 s ('en el paso 3…', 'al final…', 'un truco…')."))

    # Promesa del título en el hook
    titulo = spec.get("titulo", "")
    clave = [w for w in palabras(titulo) if w not in VACIAS and len(w) >= 3]
    if clave:
        raices = {w[:5] for w in palabras(hook30)}
        vistas = [w for w in clave if w[:5] in raices]
        if len(vistas) < max(1, len(clave) // 3):
            problemas.append((8, f"Promesa: el hook casi no menciona el tema del título ({', '.join(clave)})."))

    # Escenas largas y tipos repetidos
    largas_escenas = 0
    for i, (p, (ti, d)) in enumerate(zip(pasos, tiempos)):
        if d > 14:
            largas_escenas += 1
            problemas.append((3 if largas_escenas <= 4 else 0, f"Escena {i + 1} ({at(ti)}): {d:.0f} s sin cambio visual (ideal <= 12 s). Divídela."))
    racha = 1
    for i in range(1, len(pasos)):
        racha = racha + 1 if pasos[i]["tipo"] == pasos[i - 1]["tipo"] else 1
        if racha == 3:
            problemas.append((3, f"Escenas {i - 1}-{i + 1}: 3 escenas seguidas de tipo «{pasos[i]['tipo']}»."))

    # Reenganches: al menos uno cada 90 s
    ventana = 90
    for inicio in range(0, int(total), ventana):
        texto = " ".join(p.get("voz", "") for p, (ti, _) in zip(pasos, tiempos) if inicio <= ti < inicio + ventana)
        if texto and not re.search(REENGANCHES, texto, re.I):
            problemas.append((5, f"Ritmo: entre {at(inicio)} y {at(inicio + ventana)} no hay ningún reenganche (pregunta, 'pero', 'ojo'…)."))

    # Frases largas y relleno
    todas = [o for p in pasos for o in oraciones(p.get("voz", ""))]
    largas = [o for o in todas if len(palabras(o)) > 30]
    for o in largas[:5]:
        problemas.append((2, f"Frase larga ({len(palabras(o))} palabras): «{o[:70]}…»"))
    prom = sum(len(palabras(o)) for o in todas) / max(1, len(todas))
    if prom > 18:
        problemas.append((5, f"Claridad: {prom:.1f} palabras por frase en promedio (ideal <= 18)."))
    relleno = re.findall(RELLENO, " ".join(p.get("voz", "") for p in pasos), re.I)
    if len(relleno) > total / 60:
        problemas.append((4, f"Relleno: {len(relleno)} muletillas ({', '.join(sorted(set(r.lower() for r in relleno)))})."))

    # CTA de suscripción temprano y cierre
    for p, (ti, _) in zip(pasos, tiempos):
        if re.search(r"suscr", p.get("voz", ""), re.I) and ti < total * 0.35:
            problemas.append((6, f"CTA: pide suscripción en {at(ti)} (antes del 35 % del video). Primero entrega valor."))
            break
    if not re.search(r"(siguiente video|este video|próximo video|en pantalla)", pasos[-1].get("voz", ""), re.I):
        problemas.append((4, "Cierre: el final no lleva a otro video (pantalla final). Es la mayor fuente de sesión."))

    # Duración
    objetivo = spec.get("duracion_objetivo_min")
    if objetivo and total / 60 > objetivo * 1.25:
        problemas.append((6, f"Duración: {total / 60:.1f} min contra {objetivo} min objetivo (+25 %). Recorta."))

    nota = max(0, 100 - sum(p for p, _ in problemas))
    return {"nota": nota, "duracion_min": round(total / 60, 1), "escenas": len(pasos),
            "palabras_por_frase": round(prom, 1),
            "problemas": [{"penalizacion": p, "detalle": m} for p, m in sorted(problemas, key=lambda x: -x[0])]}


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit(__doc__)
    ruta = args[0] if args[0].endswith(".json") else os.path.join(RAIZ, "produccion", args[0], "escenas.json")
    r = analizar(json.load(open(ruta, encoding="utf-8")))
    if "--json" in sys.argv:
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return
    estado = "PASA a los críticos" if r["nota"] >= 80 else "NO PASA: corrige antes del debate"
    print(f"Nota {r['nota']}/100 · {estado}")
    print(f"{r['duracion_min']} min estimados · {r['escenas']} escenas · {r['palabras_por_frase']} palabras por frase")
    for p in r["problemas"]:
        print(f"  -{p['penalizacion']:<3} {p['detalle']}")


if __name__ == "__main__":
    main()
