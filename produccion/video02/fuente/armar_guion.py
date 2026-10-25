#!/usr/bin/env python3
"""Arma produccion/video02/guion.json (ronda 2). Los valores de la planilla se calculan aquí, de forma independiente.

    python3 produccion/video02/fuente/armar_guion.py && python3 herramientas/plantilla_xlsx.py video02
"""
import json
from datetime import date, timedelta
import calendar

RAIZ = "/home/user/nube"
ARCH = "Distribuidora Sur.xlsx"
CORTE = date(2026, 11, 4)

PRODUCTOS = [("LIM-010", "Cloro 5 L", 2400), ("LIM-020", "Detergente 5 L", 3100), ("LIM-030", "Desinfectante 1 L", 1150),
             ("LIM-040", "Papel higiénico x48", 9800), ("PAP-200", "Resma A4", 4500), ("PAP-210", "Cuadernos x10", 6200),
             ("PAP-220", "Bolígrafos x50", 3900)]
PRECIO = {c: p for c, _, p in PRODUCTOS}
RAW = [  # fecha, cliente sistema, vendedor sistema, código, cantidad, pagado
    (date(2026, 8, 4), "  ferretería el TORNILLO ", "V01 | Diego Paz", "LIM-010", 40, "Sí"),
    (date(2026, 8, 12), "LIBRERÍA SAN MARTÍN SRL", "V02 | Carla Ruiz", "PAP-200", 120, "No"),
    (date(2026, 8, 21), "kiosco la esquina", "V03 | Tomás Gil", "LIM-020", 15, "Sí"),
    (date(2026, 9, 2), "ferretería el tornillo  ", "V01 | Diego Paz", "PAP-210", 60, "Sí"),
    (date(2026, 9, 9), "  Colegio Nuevo Horizonte", "V02 | Carla Ruiz", "PAP-200", 300, "No"),
    (date(2026, 9, 15), "KIOSCO LA ESQUINA", "V03 | Tomás Gil", "LIM-030", 25, "No"),
    (date(2026, 9, 23), "librería san martín srl ", "V01 | Diego Paz", "PAP-220", 40, "Sí"),
    (date(2026, 9, 30), "Hotel  Mirador", "V01 | Diego Paz", "LIM-040", 12, "No"),
    (date(2026, 10, 6), "colegio nuevo horizonte", "V02 | Carla Ruiz", "PAP-220", 150, "No"),
    (date(2026, 10, 14), "hotel mirador ", "V03 | Tomás Gil", "LIM-040", 30, "No"),
    (date(2026, 10, 22), "Kiosco La Esquina", "V01 | Diego Paz", "PAP-210", 10, "No"),  # en el sistema viene PAP-201
    (date(2026, 10, 28), "Ferretería El Tornillo", "V02 | Carla Ruiz", "LIM-020", 50, "Sí"),
]


def f(d): return d.strftime("%d/%m/%Y")
def n(x): return f"{x:,.0f}".replace(",", ".")
def pct(x): return f"{round(x * 100)} %"
def proper(s):
    out, ini = [], True
    for ch in s:
        out.append(ch.upper() if ini else ch.lower())
        ini = not ch.isalpha()
    return "".join(out)
def trim(s): return " ".join(s.split())
def fin_mes(d, k):
    m = d.month - 1 + k
    a, m = d.year + m // 12, m % 12 + 1
    return date(a, m, calendar.monthrange(a, m)[1])


filas = []
for fe, cli, ven, cod, cant, pag in RAW:
    h = PRECIO[cod]
    bruto = cant * h
    desc = 0.10 if bruto >= 100000 else 0.05 if bruto >= 40000 else 0
    neto = round(bruto * (1 - desc))
    k = fin_mes(fe, 1)
    ingenuo = "Vencido" if k < CORTE else "Al día"
    estado = "Cobrado" if pag == "Sí" else ingenuo
    filas.append(dict(A=f(fe), fecha=fe, B=cli, C=proper(trim(cli)), D=ven, E=ven.split("| ", 1)[1], F=cod, G=cant, H=h,
                      I=desc, J=neto, K=k, L=pag, M0=ingenuo, M=estado))
filas_cod = [dict(r) for r in filas]
filas_cod[10]["F"] = "PAP-201"

# comprobaciones de las cifras del guion
venc0 = [r for r in filas if r["M0"] == "Vencido"]
venc = [r for r in filas if r["M"] == "Vencido"]
assert len(venc0) == 8 and sum(r["J"] for r in venc0) == 2446165
assert len(venc) == 4 and sum(r["J"] for r in venc) == 1835590
assert sum(r["J"] for r in venc0) - sum(r["J"] for r in venc) == 610575
VEND = ["Diego Paz", "Carla Ruiz", "Tomás Gil"]
def ventas(mes):
    ini, fin = date(2026, mes, 1), fin_mes(date(2026, mes, 1), 0)
    return [sum(r["J"] for r in filas if r["E"] == v and ini <= r["fecha"] <= fin) for v in VEND]
SEP, OCT = ventas(9), ventas(10)
clientes = sorted(set(r["C"] for r in filas))
sucios = {}
for r in filas:
    sucios.setdefault(r["B"].lower(), 1)
assert len(clientes) == 5 and len(sucios) == 10
cuenta = [sum(1 for r in filas if r["C"] == c and r["M"] == "Vencido") for c in clientes]
cobranza = sorted([(r["C"], r["K"], r["J"]) for r in venc], key=lambda x: -x[2])
print("SEP", SEP, "OCT", OCT, "clientes", clientes, cuenta, "cobranza", cobranza)

ENC = ["Fecha", "Cliente (sistema)", "Cliente", "Vendedor (sistema)", "Vendedor", "Código", "Cant.", "Precio", "Desc.", "Neto",
       "Vence", "Pagado", "Estado"]


def pedidos(hasta, rows=filas, m_ingenuo=False):
    """Celdas de Pedidos con las columnas calculadas hasta la etapa indicada (conjunto de letras ya completadas)."""
    out = [ENC]
    for r in rows:
        fila = [r["A"], r["B"], "", r["D"], "", r["F"], str(r["G"]), "", "", "", "", r["L"], ""]
        if "C" in hasta: fila[2] = r["C"]
        if "E" in hasta: fila[4] = r["E"]
        if "H" in hasta: fila[7] = n(r["H"])
        if "I" in hasta: fila[8] = pct(r["I"])
        if "J" in hasta: fila[9] = n(r["J"])
        if "K" in hasta: fila[10] = f(r["K"])
        if "M" in hasta: fila[12] = r["M0"] if m_ingenuo else r["M"]
        out.append(fila)
    return out


def ocultar(celdas, vis):
    """Vacía las celdas de las columnas ocultas (los datos completos ya están en la escena de la planilla sucia)."""
    idx = [i for i, c in enumerate("ABCDEFGHIJKLM") if c not in vis]
    return [[("" if i in idx else v) for i, v in enumerate(fila)] for fila in celdas]


def anchos(vis):
    """vis: {letra: px}; las demás columnas quedan ocultas (2 px), como columnas ocultas de Excel."""
    return [vis.get(c, 2) for c in "ABCDEFGHIJKLM"]


def col(letra, campo, fmt=str, rows=filas):
    return [fmt(r[campo]) for r in rows]


def resumen(mes=None, cobro=False, clientes_ok=False, conteo=False, mes_fecha="01/09/2026"):
    c = [["Fecha de corte", f(CORTE), "", "Cliente", "Vence", "Neto"],
         ["Ventas del mes", mes_fecha, "", "", "", ""],
         [VEND[0], "", "", "", "", ""], [VEND[1], "", "", "", "", ""], [VEND[2], "", "", "", "", ""],
         ["", "", "", "", "", ""],
         ["Cliente", "Vencidas", "", "", "", ""],
         ["", "", "", "", "", ""], ["", "", "", "", "", ""], ["", "", "", "", "", ""], ["", "", "", "", "", ""], ["", "", "", "", "", ""]]
    if mes:
        for i, v in enumerate(mes): c[2 + i][1] = n(v)
    if cobro:
        for i, (cl, k, j) in enumerate(cobranza):
            c[1 + i][3], c[1 + i][4], c[1 + i][5] = cl, f(k), n(j)
    if clientes_ok:
        for i, cl in enumerate(clientes): c[7 + i][0] = cl
    if conteo:
        for i, k in enumerate(cuenta): c[7 + i][1] = str(k)
    return c


RES_ANCHOS = [310, 180, 30, 310, 160, 160]
GRAF = {"tipo": "grafico", "titulo": "Ventas · octubre", "etiquetas": VEND, "valores": OCT,
        "textos": [n(v) for v in OCT], "destacar": 1}

E = []  # escenas


def esc(plantilla, datos, beats, **kw):
    e = {"plantilla": plantilla, "datos": datos, "beats": beats}
    e.update(kw)
    E.append(e)
    return e


def b(voz, accion=None, tts=None, **kw):
    x = {"voz": voz}
    if tts: x["voz_tts"] = tts
    if isinstance(accion, list): x["acciones"] = accion
    elif accion: x["accion"] = accion
    x.update(kw)
    return x




# ================================================================ RONDA 2
CLAUDE = {"app": "Claude"}  # sin "modelo": las respuestas no salieron de claude.ai gratis (decisión del orquestador)
Z = 1.65  # zoom mínimo antes de escribir, calcular o mostrar una nota
NAIVE = "=SI(K2<Resumen!$B$1;\"Vencido\";\"Al día\")"
GOOD = "=SI(L2=\"Sí\";\"Cobrado\";SI(K2<Resumen!$B$1;\"Vencido\";\"Al día\"))"
PEDIDOS_COMPLETOS = pedidos(set(), filas_cod)  # datos crudos de Pedidos para la plantilla (columnas ocultas en pantalla)

# ---------------------------------------------------------------- HOOK (solo video)
VIS_H = {"C": 330, "H": 140, "J": 170, "K": 180, "L": 120, "M": 180}
assert filas[0]["L"] == "Sí" and filas[0]["M0"] == "Vencido" and filas[0]["C"] == "Ferretería El Tornillo"  # fila del sello PAGADO
esc("excel", {"archivo": ARCH, "hoja": "Pedidos", "solo_video": True, "anchos": anchos(VIS_H), "seleccion_inicial": "H2",
              "celdas": ocultar(pedidos({"C"}), VIS_H)}, [
    b("Esta planilla se completa sola, con diez fórmulas. Nueve se las pedí a una IA.",
      [{"tipo": "rellenar", "rango": "H2:H13", "valores": col("H", "H", n), "duracion": 0.45, "retraso": 0},
       {"tipo": "rellenar", "rango": "J2:J13", "valores": col("J", "J", n), "duracion": 0.45, "retraso": 0.75},
       {"tipo": "rellenar", "rango": "K2:K13", "valores": [f(r["K"]) for r in filas], "duracion": 0.45, "retraso": 1.5},
       {"tipo": "rellenar", "rango": "M2:M13", "valores": [r["M0"] for r in filas], "duracion": 0.45, "retraso": 2.25}]),
    b("Y una la escribí yo. Ojo con ese sello: marcaba vencida una factura de Ferretería El Tornillo que ya estaba pagada.",
      [{"tipo": "zoom", "rango": "K1:M3", "escala": 1.8, "duracion": 0.9},
       {"tipo": "formato", "celdas": {"M2": "#ffd6d6"}, "retraso": 0.6},
       {"tipo": "resaltar", "rango": "L2:M2", "color": "#ffd400", "etiqueta": "PAGADO", "retraso": 0.8}]),
    b("Casi le cobro dos veces. Te muestro cómo la atrapé.",
      {"tipo": "zoom", "rango": "C1:M7", "escala": 1.2}),
    b("Solo necesitas Excel para la web, que es gratis, y una IA: yo uso Claude. La empresa es inventada.",
      [{"tipo": "zoom_fuera"},
       {"tipo": "rotulo", "texto": "Excel web *gratis* o 365", "sub": "en 2021 fallan 2 de las 10 · 2016/2019 no · datos ficticios", "hasta": 4.6, "retraso": 0.3}]),
], transicion="corte", entrada=0.1)

# ---------------------------------------------------------------- F1 BUSCARX
M1 = ("Excel para la web en español, separador punto y coma. Hoja Pedidos, filas 2 a 13: A Fecha, B Cliente, C Cliente limpio, "
      "D Vendedor, E Vendedor limpio, F Código, G Cantidad, H Precio, I Descuento, J Neto, K Vence, L Pagado (Sí/No), M Estado. "
      "Catálogo en la hoja Productos: A Código, C Precio. Fecha de corte en Resumen!B1. "
      "En H2 quiero el precio de cada código; si no existe, que diga \"Código no existe\". Una fórmula para copiar hacia abajo.")
esc("chat", CLAUDE, [
    b("Fórmula uno: el precio. Le digo qué hay en cada columna, eso es el mapa, y qué quiero, la meta.",
      [{"tipo": "rotulo", "numero": "01", "texto": "BUSCARX", "sub": "el mapa completo está en la hoja Prompts", "hasta": 3.0},
       {"tipo": "prompt", "texto": M1, "duracion": 1.2, "retraso": 0.3}]),
    b("Y me da buscar equis.",
      {"tipo": "respuesta", "texto": "Escribe esto en H2 y cópialo hasta H13. El último argumento es lo que muestra si no encuentra el código, así que no verás #N/A:",
       "formula": "=BUSCARX(F2;Productos!A:A;Productos!C:C;\"Código no existe\")", "duracion": 1.6},
      tts="Y me da buscar equis."),
], capitulo="1. BUSCARX: traer precios del catálogo")

VIS_V1 = {"B": 340, "F": 170, "G": 120, "H": 300}
esc("excel", {"archivo": ARCH, "hoja": "Pedidos", "anchos": anchos(VIS_V1), "seleccion_inicial": "H2",
              "celdas": ocultar(pedidos(set(), filas_cod), VIS_V1), "celdas_plantilla": PEDIDOS_COMPLETOS}, [
    b("Buscar equis es la versión nueva de buscar uve. La pego en la columna Precio.",
      [{"tipo": "zoom", "rango": "F1:H4", "escala": 1.7},
       {"tipo": "escribir", "celda": "H2", "texto": "=BUSCARX(F2;Productos!A:A;Productos!C:C;\"Código no existe\")", "duracion": 2.2, "retraso": 1.1}],
      tts="Buscar equis es la versión nueva de buscar uve. La pego en la columna Precio."),
    b("Dos mil cuatrocientos: el precio del cloro.",
      [{"tipo": "calcular", "celda": "H2", "valor": "2.400"}, {"tipo": "mover", "celda": "B4", "retraso": 0.3}]),
    b("Primero, el código que busca. Después, dónde buscarlo, de dónde traer el precio, y qué decir si no lo encuentra.",
      [{"tipo": "nota", "celda": "H2", "texto": "BUSCARX(*qué*; *dónde*; *qué traer*; *si no está*)", "retraso": 0.2},
       {"tipo": "nota", "celda": "H2", "texto": "¿Tu Excel usa *coma*? Dilo en el mapa", "retraso": 5.6}], pausa=1.8),
    b("La copio hacia abajo.",
      [{"tipo": "quitar_nota"}, {"tipo": "zoom_fuera", "duracion": 0.7},
       {"tipo": "rellenar", "rango": "H2:H13", "valores": [("Código no existe" if r["F"] == "PAP-201" else n(r["H"])) for r in filas_cod], "retraso": 0.4}]),
    b("PAP-201 no existe: era PAP-210. Lo corrijo, y el precio aparece.",
      [{"tipo": "zoom", "rango": "F5:H9", "escala": 1.6, "duracion": 0.8},
       {"tipo": "resaltar", "rango": "F12:H12", "color": "#e5484d", "etiqueta": "aviso, no error", "retraso": 0.5, "hasta": 2.4},
       {"tipo": "escribir", "celda": "F12", "texto": "PAP-210", "duracion": 0.8, "retraso": 1.2},
       {"tipo": "calcular", "celda": "H12", "valor": "6.200", "retraso": 2.9}],
      tts="Pe, a, pe, dos, cero, uno, no existe: era pe, a, pe, dos, uno, cero. Lo corrijo, y el precio aparece.", pausa=0.8),
])

# ---------------------------------------------------------------- F2 NOMPROPIO + ESPACIOS
esc("capitulo", {"numero": 2, "total": 10, "titulo": "NOMPROPIO + ESPACIOS: nombres prolijos"},
    [b("Fórmula dos: limpiar los nombres.")], capitulo="2. NOMPROPIO y ESPACIOS: limpiar nombres")
VIS_V2 = {"B": 370, "C": 370, "F": 150, "G": 100, "H": 140}
esc("excel", {"archivo": ARCH, "hoja": "Pedidos", "anchos": anchos(VIS_V2), "seleccion_inicial": "C2", "celdas": ocultar(pedidos({"H"}), VIS_V2)}, [
    b("El sistema escribe al mismo kiosco de tres formas: en minúsculas, en mayúsculas y bien.",
      [{"tipo": "resaltar", "rango": "B4", "color": "#e5484d", "etiqueta": "1", "retraso": 0.3, "hasta": 4.5},
       {"tipo": "resaltar", "rango": "B7", "color": "#e5484d", "etiqueta": "2", "retraso": 1.6, "hasta": 3.2},
       {"tipo": "resaltar", "rango": "B12", "color": "#107c41", "etiqueta": "3 · bien", "retraso": 2.9, "hasta": 1.9}]),
    b("Y a otros les sobran espacios: para una lista, eso ya es otro cliente.",
      {"tipo": "resaltar", "rango": "B5", "color": "#e5484d", "etiqueta": "espacios de más", "retraso": 0.2, "hasta": 3.0}),
    b("En la misma conversación, así no repito el mapa, le pido solo la meta: el nombre prolijo.",
      [{"tipo": "zoom", "rango": "B1:C5", "escala": 1.6},
       {"tipo": "rotulo", "numero": "02", "texto": "Se la pedí a Claude", "sub": "el prompt está en la hoja Prompts", "retraso": 0.4}]),
    b("Dos funciones, una dentro de otra: espacios quita los sobrantes y nompropio arregla las mayúsculas.",
      {"tipo": "escribir", "celda": "C2", "texto": "=NOMPROPIO(ESPACIOS(B2))", "duracion": 1.6},
      tts="Dos funciones, una dentro de otra: espacios quita los sobrantes y nom propio arregla las mayúsculas."),
    b("La copio, y el kiosco queda igual en las tres filas: Kiosco La Esquina.",
      [{"tipo": "calcular", "celda": "C2", "valor": filas[0]["C"], "derecha": False},
       {"tipo": "zoom_fuera", "duracion": 0.6, "retraso": 0.6},
       {"tipo": "rellenar", "rango": "C2:C13", "valores": col("C", "C"), "retraso": 1.0},
       {"tipo": "resaltar", "rango": "C4", "color": "#107c41", "retraso": 2.4, "hasta": 3.4},
       {"tipo": "resaltar", "rango": "C7", "color": "#107c41", "retraso": 2.6, "hasta": 3.2},
       {"tipo": "resaltar", "rango": "C12", "color": "#107c41", "etiqueta": "las 3, iguales", "retraso": 2.8, "hasta": 3.0}]),
    b("Y me avisó de algo: la sigla SRL queda en minúsculas. Esas, a mano.",
      [{"tipo": "resaltar", "rango": "C3", "color": "#e5484d", "retraso": 0.2},
       {"tipo": "rotulo", "texto": "Claude: «las siglas también cambian: SRL queda Srl»", "sub": "respuesta real (prompt 2 de la hoja Prompts)", "retraso": 0.3, "hasta": 4.0}],
      tts="Y me avisó de algo: la sigla ese, erre, ele, queda en minúsculas. Esas, a mano.", pausa=1.2),
])
esc("antes_despues", {"antes": {"valor": 10, "sufijo": "", "texto": "«clientes» con los nombres *sucios*"},
                      "despues": {"valor": 5, "sufijo": "", "texto": "clientes con los nombres *limpios*"}}, [
    b("Con los nombres sucios, una lista sin repetidos daba diez clientes."),
    b("Limpios, son cinco."),
])

# ---------------------------------------------------------------- F3 TEXTODESPUES
VIS_V3 = {"C": 330, "D": 310, "E": 250, "F": 150, "G": 100, "H": 140}
esc("excel", {"archivo": ARCH, "hoja": "Pedidos", "anchos": anchos(VIS_V3), "seleccion_inicial": "E2", "celdas": ocultar(pedidos({"H", "C"}), VIS_V3)}, [
    b("Fórmula tres: el vendedor viene pegado a su código, con una barra.",
      [{"tipo": "zoom", "rango": "C1:E4", "escala": 1.6},
       {"tipo": "rotulo", "numero": "03", "texto": "TEXTODESPUES", "sub": "se la pedí a Claude · prompt en la hoja Prompts", "retraso": 0.3},
       {"tipo": "resaltar", "rango": "D2", "color": "#3b6fd8", "retraso": 1.0, "hasta": 3}]),
    b("La IA me dio texto después: todo lo que viene después de la barra.",
      {"tipo": "escribir", "celda": "E2", "texto": "=TEXTODESPUES(D2;\"| \")", "duracion": 1.5}),
    b("Diego Paz. Su gemela, texto antes, te da el código.",
      [{"tipo": "calcular", "celda": "E2", "valor": "Diego Paz", "derecha": False},
       {"tipo": "mover", "celda": "C4", "retraso": 0.3},
       {"tipo": "nota", "celda": "E2", "texto": "TEXTOANTES(D2;\" |\") → *V01*", "retraso": 0.7}], pausa=0.8),
    b("Y abajo, todos los vendedores separados.",
      [{"tipo": "quitar_nota"}, {"tipo": "zoom_fuera", "duracion": 0.7},
       {"tipo": "rellenar", "rango": "E2:E13", "valores": col("E", "E"), "retraso": 0.4}]),
], capitulo="3. TEXTODESPUES: separar texto pegado")

esc("titular", {"etiqueta": "Lo que viene", "icono": "triangle-alert", "tamano": 84,
                "lineas": ["Fórmula 7: el error", "que casi me *cuesta caro*", {"texto": "Prompts gratis: hoja *Prompts*", "beat": 1}],
                "sub": "enlace en la descripción", "sub_beat": 1}, [
    b("En la fórmula siete, la que escribí yo, viene el error que casi me cuesta caro."),
    b("Los diez prompts están gratis en la plantilla: hoja Prompts."),
])

# ---------------------------------------------------------------- F4 SI.CONJUNTO
esc("capitulo", {"numero": 4, "total": 10, "titulo": "SI.CONJUNTO: descuentos por tramos"},
    [b("Fórmula cuatro: descuentos por tramos.")], capitulo="4. SI.CONJUNTO: descuentos por tramos")
esc("chat", CLAUDE, [
    b("Los descuentos, como los diría mi jefe.",
      {"tipo": "prompt", "texto": "En I2 quiero el descuento según el total de la compra (G2*H2): 10 % si llega a 100.000; 5 % si llega a 40.000; si no, 0 %.", "duracion": 1.2}),
    b("Ojo: tramos de mayor a menor, y verdadero al final, que significa en cualquier otro caso.",
      {"tipo": "respuesta", "texto": "Las condiciones se evalúan en orden, por eso va primero el tramo más alto. El VERDADERO del final funciona como \"en cualquier otro caso\".",
       "formula": "=SI.CONJUNTO(G2*H2>=100000;10%;G2*H2>=40000;5%;VERDADERO;0)", "duracion": 2.6}),
])
VIS_V4 = {"C": 330, "F": 150, "G": 100, "H": 140, "I": 130, "J": 190}
esc("excel", {"archivo": ARCH, "hoja": "Pedidos", "anchos": anchos(VIS_V4), "seleccion_inicial": "I2", "celdas": ocultar(pedidos({"H", "C", "E"}), VIS_V4)}, [
    b("La pego en la columna del descuento.",
      [{"tipo": "zoom", "rango": "G1:J4", "escala": 1.7},
       {"tipo": "escribir", "celda": "I2", "texto": "=SI.CONJUNTO(G2*H2>=100000;10%;G2*H2>=40000;5%;VERDADERO;0)", "duracion": 2.2, "retraso": 1.0}], pausa=0.9),
    b("Cuarenta bidones de cloro suman noventa y seis mil: cinco por ciento.", {"tipo": "calcular", "celda": "I2", "valor": "5 %"}),
    b("Y si no llega a cuarenta mil, como los veinticinco desinfectantes del kiosco, cero.",
      [{"tipo": "zoom", "rango": "G4:J8", "escala": 1.6, "duracion": 0.7}, {"tipo": "mover", "celda": "C10"},
       {"tipo": "nota", "celda": "I7", "texto": "25 × 1.150 = 28.750 → *0 %*", "lado": "abajo", "retraso": 0.8}], pausa=0.6),
    b("Cada pedido cae en su tramo. El neto es una multiplicación simple, que no cuenta entre las diez.",
      [{"tipo": "quitar_nota"}, {"tipo": "rellenar", "rango": "I2:I13", "valores": col("I", "I", pct)},
       {"tipo": "escribir", "celda": "J2", "texto": "=G2*H2*(1-I2)", "duracion": 1.1, "retraso": 2.4}]),
    b("Noventa y un mil doscientos, y la columna completa.",
      [{"tipo": "calcular", "celda": "J2", "valor": n(filas[0]["J"])}, {"tipo": "zoom_fuera", "retraso": 0.7, "duracion": 0.7},
       {"tipo": "rellenar", "rango": "J2:J13", "valores": col("J", "J", n), "retraso": 1.2}]),
])

# ---------------------------------------------------------------- F5 FIN.MES
esc("antes_despues", {"antes": {"valor": 3, "sufijo": " sep.", "texto": "*+30 días* desde el 4 de agosto ✗"},
                      "despues": {"valor": 30, "sufijo": " sep.", "texto": "*FIN.MES*: fin del mes siguiente ✓"}}, [
    b("Fórmula cinco: vence a fin del mes siguiente. ¿Y si sumas treinta días? Del 4 de agosto llegas al 3 de septiembre.",
      tts="Fórmula cinco: vence a fin del mes siguiente. ¿Y si sumas treinta días? Del cuatro de agosto llegas al tres de septiembre."),
    b("Lo correcto es el 30 de septiembre.", tts="Lo correcto es el treinta de septiembre."),
], capitulo="5. FIN.MES: fechas de vencimiento")
VIS_V5 = {"A": 175, "C": 330, "J": 170, "K": 190}
esc("excel", {"archivo": ARCH, "hoja": "Pedidos", "anchos": anchos(VIS_V5), "seleccion_inicial": "K2", "celdas": ocultar(pedidos({"H", "C", "E", "I", "J"}), VIS_V5)}, [
    b("Se lo pedí a la IA, y me dio fin punto mes.",
      [{"tipo": "zoom", "rango": "A1:K4", "escala": 1.6},
       {"tipo": "rotulo", "numero": "05", "texto": "FIN.MES", "sub": "se la pedí a Claude · prompt en la hoja Prompts", "retraso": 0.3},
       {"tipo": "escribir", "celda": "K2", "texto": "=FIN.MES(A2;1)", "duracion": 1.1, "retraso": 1.2}], pausa=0.6),
    b("Treinta de septiembre. El uno es el mes siguiente; con cero, sería el fin de este mes.",
      [{"tipo": "calcular", "celda": "K2", "valor": f(filas[0]["K"])},
       {"tipo": "mover", "celda": "C4", "retraso": 0.3},
       {"tipo": "nota", "celda": "C3", "lado": "abajo", "texto": "FIN.MES(A2;*1*): fin del mes siguiente · con *0*, fin de este mes", "retraso": 0.5}]),
    b("Si ves un número raro, a la celda le falta formato de fecha.",
      {"tipo": "nota", "celda": "C3", "lado": "abajo", "texto": "¿Ves *46295*? Inicio › Formato de número › Fecha corta"}),
    b("Y cada pedido, con su vencimiento.",
      [{"tipo": "quitar_nota"}, {"tipo": "zoom_fuera", "duracion": 0.7},
       {"tipo": "rellenar", "rango": "K2:K13", "valores": [f(r["K"]) for r in filas], "retraso": 0.4}]),
])

esc("titular", {"etiqueta": "Lo que viene", "icono": "triangle-alert",
                "lineas": ["La fórmula que", "*cobraba dos veces*"], "sub": "Si te sirve, suscríbete: una planilla resuelta con IA cada semana", "sub_beat": 1}, [
    b("Después viene la fórmula que casi le cobra dos veces a un cliente."),
    b("Si te está sirviendo, suscríbete."),
])

# ---------------------------------------------------------------- F6 SUMAR.SI.CONJUNTO
esc("capitulo", {"numero": 6, "total": 10, "titulo": "SUMAR.SI.CONJUNTO: ventas por vendedor"},
    [b("Fórmula seis: ventas por vendedor.")], capitulo="6. SUMAR.SI.CONJUNTO: ventas por vendedor y mes")
F6 = "=SUMAR.SI.CONJUNTO(Pedidos!J:J;Pedidos!E:E;A3;Pedidos!A:A;\">=\"&$B$2;Pedidos!A:A;\"<=\"&FIN.MES($B$2;0))"
esc("chat", CLAUDE, [
    b("Para la reunión de ventas: cuánto vendió cada uno en el mes que elijo.",
      {"tipo": "prompt", "texto": "En Resumen tengo los vendedores en A3:A5 y en B2 el primer día del mes que quiero ver. En B3 quiero el neto vendido por ese vendedor en ese mes. Una fórmula para copiar hacia abajo.", "duracion": 1.2}),
    b("Ojo: arma el criterio de fechas con fin punto mes, otra vez.",
      {"tipo": "respuesta", "texto": "Suma el neto (J) donde el vendedor (E) es el de A3 y la fecha (A) está entre el primer y el último día del mes de B2. Los $ dejan fija B2 al copiar.",
       "formula": F6, "duracion": 2.4}),
])
esc("excel", {"archivo": ARCH, "hoja": "Resumen", "anchos": RES_ANCHOS, "seleccion_inicial": "B3", "celdas": resumen()}, [
    b("En la hoja Resumen, el mes va en B2: septiembre.",
      [{"tipo": "zoom", "rango": "A1:B5", "escala": 1.6},
       {"tipo": "rotulo", "numero": "06", "texto": "Ventas del mes", "sub": "una sola fórmula para toda la columna", "retraso": 0.3},
       {"tipo": "resaltar", "rango": "B2", "color": "#3b6fd8", "retraso": 1.0, "hasta": 2.6}]),
    b("Pego la fórmula. El signo de dólar deja fija la celda del mes al copiar.",
      {"tipo": "escribir", "celda": "B3", "texto": F6, "duracion": 3.0}),
    b("Diego Paz: 581.040 en septiembre.", {"tipo": "calcular", "celda": "B3", "valor": n(SEP[0])},
      tts="Diego Paz: quinientos ochenta y un mil cuarenta en septiembre."),
    b("Suma el neto cuando el vendedor coincide y la fecha cae entre el primero y el último día del mes.",
      [{"tipo": "mover", "celda": "A9"}, {"tipo": "nota", "celda": "B4", "texto": "\">=\"&$B$2 y \"<=\"&FIN.MES($B$2;0)", "lado": "abajo", "retraso": 0.3}]),
    b("Carla Ruiz, un millón doscientos quince mil.",
      [{"tipo": "quitar_nota"}, {"tipo": "rellenar", "rango": "B3:B5", "valores": [n(v) for v in SEP]}]),
    b("Cambio a octubre, y se recalcula sola.",
      [{"tipo": "escribir", "celda": "B2", "texto": "01/10/2026", "duracion": 0.9}]
      + [{"tipo": "calcular", "celda": f"B{3 + i}", "valor": n(v), "retraso": 1.8 + 0.15 * i} for i, v in enumerate(OCT)], pausa=0.8),
])

# ---------------------------------------------------------------- F7 EL GIRO
esc("capitulo", {"numero": 7, "total": 10, "titulo": "SI: el estado de cada factura"},
    [b("Fórmula siete: el estado de cada factura.")], capitulo="7. SI: el estado de cada factura")
VIS_V7 = {"C": 330, "J": 170, "K": 180, "L": 120, "M": 200}
esc("excel", {"archivo": ARCH, "hoja": "Pedidos", "anchos": anchos(VIS_V7), "seleccion_inicial": "M2", "celdas": ocultar(pedidos({"H", "C", "E", "I", "J", "K"}), VIS_V7)}, [
    b("Esta es corta: la escribí yo. Compara el vencimiento con la fecha de corte, en Resumen B1.",
      [{"tipo": "zoom", "rango": "J1:M4", "escala": 1.6},
       {"tipo": "rotulo", "numero": "07", "texto": "La IA como revisora", "sub": "esta la escribí yo", "retraso": 0.3}]),
    b("En tu planilla, pon igual a hoy en B1. Aquí la dejo fija, para que veas los mismos números.",
      [{"tipo": "mover", "celda": "C4"}, {"tipo": "nota", "celda": "K2", "texto": "Fecha de corte: Resumen!B1 · en tu planilla, *=HOY()*", "retraso": 0.3}],
      tts="En tu planilla, pon igual a hoy en be uno. Aquí la dejo fija, para que veas los mismos números."),
    b("Si vence antes del corte, vencido; si no, al día.",
      [{"tipo": "quitar_nota"}, {"tipo": "escribir", "celda": "M2", "texto": NAIVE, "duracion": 2.0, "retraso": 0.2},
       {"tipo": "nota", "celda": "K3", "texto": "Escrita *a mano*, como la escribe casi todo el mundo", "lado": "abajo", "retraso": 2.6}], pausa=1.2),
    b("No da error.", {"tipo": "calcular", "celda": "M2", "valor": "Vencido", "derecha": False}),
    b("La copio: ocho facturas vencidas, dos millones cuatrocientos cuarenta y seis mil por cobrar.",
      [{"tipo": "quitar_nota"}, {"tipo": "zoom_fuera", "duracion": 0.7},
       {"tipo": "rellenar", "rango": "M2:M13", "valores": [r["M0"] for r in filas], "retraso": 0.4},
       {"tipo": "formato", "rango": "M2:M9", "fondo": "#ffd6d6", "retraso": 1.6},
       {"tipo": "resaltar", "rango": "M2:M9", "color": "#e5484d", "etiqueta": "8 vencidas · 2.446.165", "retraso": 2.0}]),
    b("Parece perfecta, ¿no? Ahora, la tercera parte del método.",
      {"tipo": "zoom", "rango": "J1:M5", "escala": 1.3}),
])

esc("lista", {"titulo": "El prompt de 3 partes", "items": [
    {"texto": "*Mapa*", "detalle": "qué hay en cada columna · nunca datos reales de clientes", "icono": "map"},
    {"texto": "*Meta*", "detalle": "qué quieres, con la regla en palabras", "icono": "target"},
    {"texto": "*Prueba*", "detalle": "qué casos darían mal sin error, y qué debe dar en dos filas", "icono": "shield-check"}]}, [
    b("Mapa: dónde está cada dato. Solo nombres de columnas: nunca pegues datos reales de clientes."),
    b("Meta: qué quieres, en palabras."),
    b("Y la prueba, la que casi nadie usa: qué casos darían mal sin mostrar error, y qué debería dar en dos filas."),
])

PRUEBA = ("Escribí esta fórmula para M2: =SI(K2<Resumen!$B$1;\"Vencido\";\"Al día\"). ¿Qué casos pueden hacer que dé un resultado equivocado "
          "sin mostrar error? ¿Qué debería dar la fila 2 (vence 30/09/2026, Pagado: Sí) y la fila 6 (vence 31/10/2026, Pagado: No), con corte 04/11/2026?")
esc("chat", CLAUDE, [
    b("Pego mi fórmula, con la prueba.", {"tipo": "prompt", "texto": PRUEBA, "duracion": 1.2}),
    b("Y va directo al problema: mi fórmula no mira la columna Pagado. La fila dos ya estaba pagada, y dice vencido.",
      {"tipo": "respuesta", "texto": "1. Facturas pagadas: la fórmula no mira la columna L. Si ya se pagó pero su vencimiento pasó, dice \"Vencido\".<br>"
                                      "2. Si K está vacía, cuenta como 0 y también dice \"Vencido\". (y 2 casos más)<br>"
                                      "Fila 2: da \"Vencido\", pero ya está pagada.<br>Fila 6: da \"Vencido\", y es correcto.<br>Fórmula corregida:",
       "formula": GOOD, "duracion": 4.5}, pausa=1.2),
])
esc("aviso", {"titulo": "3 clientes · 4 facturas *ya pagadas*", "nivel": "rojo", "icono": "phone-off",
              "texto": "Ferretería El Tornillo, Kiosco La Esquina y Librería San Martín figuraban como deudores."}, [
    b("Esta semana habría llamado a tres clientes para cobrarles cuatro facturas que ya habían pagado."),
])
esc("cifra", {"valor": 610575, "etiqueta": "de más en la lista de cobranza", "fuente": "cálculo sobre la planilla ficticia del video"}, [
    b("610.575 de más en la lista de cobranza.", tts="Seiscientos diez mil quinientos setenta y cinco de más en la lista de cobranza."),
])
esc("excel", {"archivo": ARCH, "hoja": "Pedidos", "anchos": anchos(VIS_V7), "seleccion_inicial": "M2",
              "celdas": ocultar(pedidos({"H", "C", "E", "I", "J", "K", "M"}, m_ingenuo=True), VIS_V7)}, [
    b("Pego la corregida: primero mira si está pagada.",
      [{"tipo": "zoom", "rango": "J1:M4", "escala": 1.6},
       {"tipo": "escribir", "celda": "M2", "texto": GOOD, "duracion": 2.4, "retraso": 0.9}], pausa=1.0),
    b("La fila dos ahora dice cobrado.", {"tipo": "calcular", "celda": "M2", "valor": "Cobrado", "derecha": False}),
    b("Y abajo, la ferretería, el kiosco y la librería pasan a cobrado.",
      [{"tipo": "zoom_fuera", "duracion": 0.7},
       {"tipo": "rellenar", "rango": "M2:M13", "valores": [r["M"] for r in filas], "retraso": 0.4},
       {"tipo": "formato", "celdas": {f"M{i + 2}": ("#ffd6d6" if r["M"] == "Vencido" else "#ffffff") for i, r in enumerate(filas)}, "retraso": 1.6}]),
    b("Y compruebo lo que la prueba dijo de la fila seis: vencida y sin pagar. Coincide.",
      [{"tipo": "zoom", "rango": "J5:M7", "escala": 1.7}, {"tipo": "resaltar", "rango": "K6:M6", "color": "#107c41", "etiqueta": "lo que dijo la Prueba ✓", "retraso": 0.9}]),
])
esc("antes_despues", {"antes": {"valor": 8, "texto": "vencidas con la fórmula *escrita a mano*"},
                      "despues": {"valor": 4, "texto": "vencidas *de verdad* · 1.835.590"}}, [
    b("Ocho vencidas con la fórmula escrita a mano."),
    b("Cuatro de verdad: un millón ochocientos treinta y cinco mil quinientos noventa."),
])
esc("titular", {"etiqueta": "Hallazgo honesto", "icono": "search-check", "tamano": 92,
                "lineas": ["A veces la IA avisa sola.", "La Prueba, *siempre*."]}, [
    b("A veces la IA te avisa sola, pero no siempre: la prueba hace que te lo diga. Y en la fórmula ocho me salvó otra vez."),
])

# ---------------------------------------------------------------- F8 FILTRAR
esc("capitulo", {"numero": 8, "total": 10, "titulo": "FILTRAR: la cobranza de la semana en una celda"},
    [b("Fórmula ocho: el reporte de cobranza de la semana.")], capitulo="8. FILTRAR: cobranza en Excel, el reporte de la semana")
P8 = ("Mapa: el de antes. Meta: en Resumen!D2, una lista que se actualice sola con Cliente (C), Vence (K) y Neto (J) de las facturas "
      "\"Vencido\", de mayor a menor neto. Prueba: antes de darme la fórmula, dime qué casos darían un resultado equivocado sin error y qué debería salir arriba.")
F8 = "=SI.ERROR(ORDENAR(FILTRAR(ELEGIRCOLS(Pedidos!A2:M13;3;11;10);Pedidos!M2:M13=\"Vencido\");3;-1);\"Sin vencidos\")"
esc("chat", CLAUDE, [
    b("Ahora el prompt va completo: mapa, meta y prueba.", {"tipo": "prompt", "texto": P8, "duracion": 1.2}),
    b("La prueba encuentra un caso. Lo cubre: si no hay vencidas, muestra un mensaje en vez de un error.",
      {"tipo": "respuesta", "texto": "1. Si no hay ninguna vencida, FILTRAR no tiene nada que devolver y ORDENAR daría error. Lo cubro con SI.ERROR.<br>"
                                      "2. Los pedidos debajo de la fila 13 quedan afuera: amplía los rangos.<br>(y 2 casos más)<br>"
                                      "Arriba debería salir la vencida con el neto más alto.",
       "formula": F8, "duracion": 3.6}, pausa=0.8),
])
esc("excel", {"archivo": ARCH, "hoja": "Resumen", "anchos": RES_ANCHOS, "seleccion_inicial": "D2",
              "celdas": resumen(OCT, mes_fecha="01/10/2026")}, [
    b("La pego en Resumen, en una sola celda.",
      [{"tipo": "zoom", "rango": "D1:F5", "escala": 1.6},
       {"tipo": "rotulo", "numero": "08", "texto": "Cobranza de la semana", "sub": "ELEGIRCOLS → FILTRAR → ORDENAR", "retraso": 0.3}]),
    b("De adentro hacia afuera: elegir columnas toma cliente, vencimiento y neto.",
      {"tipo": "escribir", "celda": "D2", "texto": F8, "duracion": 3.0}),
    b("Filtrar deja las vencidas, y ordenar pone la más grande arriba.",
      [{"tipo": "mover", "celda": "B10"}, {"tipo": "nota", "celda": "D3", "texto": "ELEGIRCOLS → FILTRAR → ORDENAR", "lado": "abajo", "retraso": 0.2}]),
    b("El resultado ocupa las celdas de abajo: déjalas vacías.",
      [{"tipo": "quitar_nota"}]
      + [{"tipo": "calcular", "celda": f"{c}{2 + i}", "valor": v, "derecha": c != "D", "retraso": 0.1 + 0.1 * (3 * i + j)}
         for i, fila in enumerate(cobranza) for j, (c, v) in enumerate(zip("DEF", [fila[0], f(fila[1]), n(fila[2])]))]),
    b("Un millón ochocientos treinta y cinco mil quinientos noventa: a quién llamar esta semana, y por cuánto.",
      {"tipo": "resaltar", "rango": "F2:F5", "color": "#ffd400", "etiqueta": "Total 1.835.590"}),
    b("Si alguien paga, cambias su Pagado a sí en Pedidos, y sale de esta lista.",
      [{"tipo": "zoom", "rango": "D1:F5", "escala": 1.6},
       {"tipo": "nota", "celda": "D3", "lado": "abajo", "texto": "Pedidos › Pagado = *Sí* → sale de la lista", "retraso": 0.4}]),
    b("Y si cambias la fecha de corte, la lista se rehace sola.",
      [{"tipo": "quitar_nota"}, {"tipo": "zoom", "rango": "A1:B2", "escala": 1.6},
       {"tipo": "resaltar", "rango": "B1", "color": "#3b6fd8", "etiqueta": "fecha de corte", "retraso": 0.9, "hasta": 3.4}]),
])

# ---------------------------------------------------------------- F9 y F10
esc("capitulo", {"numero": 9, "total": 10, "titulo": "UNICOS + CONTAR.SI.CONJUNTO: el tablero de clientes"},
    [b("Fórmulas nueve y diez: el tablero de clientes.")], capitulo="9 y 10. UNICOS y CONTAR.SI.CONJUNTO: clientes y deudas")
F9 = "=ORDENAR(UNICOS(Pedidos!C2:C13))"
F10 = "=CONTAR.SI.CONJUNTO(Pedidos!C:C;A8;Pedidos!M:M;\"Vencido\")"
esc("excel", {"archivo": ARCH, "hoja": "Resumen", "anchos": RES_ANCHOS, "seleccion_inicial": "A8",
              "celdas": resumen(OCT, True, mes_fecha="01/10/2026")}, [
    b("La lista de clientes sin repetidos: únicos, dentro de ordenar.",
      [{"tipo": "zoom", "rango": "A6:B12", "escala": 1.6},
       {"tipo": "rotulo", "numero": "09", "texto": "UNICOS + ORDENAR", "sub": "prompt con las 3 partes en la hoja Prompts", "retraso": 0.3},
       {"tipo": "escribir", "celda": "A8", "texto": F9, "duracion": 1.6, "retraso": 1.0}]),
    b("Cinco clientes, gracias a la limpieza de la fórmula dos.",
      [{"tipo": "calcular", "celda": f"A{8 + i}", "valor": c, "derecha": False, "retraso": 0.12 * i} for i, c in enumerate(clientes)]),
])
esc("antes_despues", {"antes": {"valor": 2, "sufijo": " vencidas", "texto": "Ferretería, con la fórmula *a mano* ✗"},
                      "despues": {"valor": 0, "sufijo": " vencidas", "texto": "Ferretería, *con la prueba* ✓"}}, [
    b("A mano, la ferretería tenía dos vencidas."),
    b("Con la prueba, cero."),
])
esc("excel", {"archivo": ARCH, "hoja": "Resumen", "anchos": RES_ANCHOS, "seleccion_inicial": "B8",
              "celdas": resumen(OCT, True, clientes_ok=True, mes_fecha="01/10/2026")}, [
    b("Fórmula diez: cuántas vencidas tiene cada uno. Contar si conjunto, con dos condiciones.",
      [{"tipo": "zoom", "rango": "A6:B12", "escala": 1.6}, {"tipo": "rotulo", "numero": "10", "texto": "CONTAR.SI.CONJUNTO", "sub": "dos condiciones: cliente y «Vencido»", "retraso": 0.3},
       {"tipo": "escribir", "celda": "B8", "texto": F10, "duracion": 2.4, "retraso": 0.4}],
      tts="Fórmula diez: cuántas vencidas tiene cada uno. Contar si punto conjunto, con dos condiciones.", pausa=0.6),
    b("Cuatro clientes deben una factura. La ferretería, ninguna.",
      [{"tipo": "calcular", "celda": "B8", "valor": str(cuenta[0])},
       {"tipo": "rellenar", "rango": "B8:B12", "valores": [str(k) for k in cuenta], "retraso": 0.7},
       {"tipo": "resaltar", "rango": "A9:B9", "color": "#ffd400", "etiqueta": "pagó todo", "retraso": 2.0}]),
    b("Y la hoja Resumen queda completa, con su gráfico.",
      [{"tipo": "zoom_fuera", "duracion": 0.8}, dict(GRAF, x=1222, y=262, ancho=310, retraso=0.6)]),
])

# ---------------------------------------------------------------- cierre
esc("comparar", {"titulo": "¿Cuándo *no* pedírsela a la IA?", "columnas": ["Si…", "Entonces"],
                 "filas": [["La fórmula es más corta que el prompt", "Escríbela tú, y pásala por la *Prueba*"],
                           ["No sabes qué función existe", "Pídesela a la IA"],
                           ["Combina tres funciones o más", "Pídesela a la IA"],
                           ["Usas ChatGPT o Copilot", "Mismo prompt · la respuesta puede cambiar: *Prueba*"]], "beats_filas": [1, 2, 3, 4]}, [
    b("¿Y cuándo conviene no pedírsela a la IA?"),
    b("Si la fórmula es más corta que el prompt: escríbela tú, y pásala por la prueba."),
    b("Si no sabes qué función existe, pídesela."),
    b("Si combina tres o más, también."),
    b("Y puedes pegar el mismo prompt en ChatGPT o Copilot. La respuesta puede cambiar, y por eso existe la prueba."),
])
esc("titular", {"etiqueta": "Gratis", "icono": "download",
                "lineas": ["Distribuidora Sur", "*10 fórmulas con IA*"], "sub": "Pedidos, Resumen, Prompts y Práctica · en la descripción"}, [
    b("La planilla, con las diez fórmulas y la hoja Prompts, está gratis en la descripción. Y si te llegan informes en pe de efe, mira este video."),
])
esc("final", {"titulo": "Sigue con *este atajo*"}, [
    b("Te lo dejo en pantalla."),
])

# ---------------------------------------------------------------- hojas extra de la plantilla
QUE_REVISAR = {
    "1": "Que el último argumento cubra los códigos mal escritos; si tu Excel no tiene BUSCARX, pide BUSCARV.",
    "2": "Siglas (SRL queda Srl) y tildes que faltan: NOMPROPIO no las arregla.",
    "3": "Filas sin la barra devuelven #N/A: usa el sexto argumento para dejar el texto original.",
    "4": "El orden de los tramos (de mayor a menor) y que un precio con error da #¡VALOR!.",
    "5": "Formato de fecha en la columna (si no, ves 46295); con 0 es fin de este mes.",
    "6": "Fechas guardadas como texto no se suman y no avisan: compruébalo con un filtro.",
    "7": "Que mire la columna Pagado; vencimientos vacíos; vence el mismo día del corte.",
    "8": "Sin vencidas, SI.ERROR; pedidos debajo de la fila 13; deja libres las celdas de abajo.",
    "9": "Usa la columna limpia: un espacio de más duplica un cliente.",
    "10": "Un espacio de más en el estado o en el nombre cuenta 0 sin avisar.",
}


def prompts_reales():
    """Lee respuestas-ia.md: número, prompt y primera fórmula de cada respuesta."""
    import re as _re
    txt = open(f"{RAIZ}/produccion/video02/respuestas-ia.md", encoding="utf-8").read()
    filas_p = []
    for bloque in _re.split(r"\n## ", txt)[1:]:
        cab = bloque.splitlines()[0]
        num = cab.split(" ")[0]
        prompt = _re.search(r"\*\*Prompt\*\*\n\n((?:> .*\n?)+)", bloque).group(1)
        prompt = " ".join(l[2:].strip() for l in prompt.strip().splitlines())
        resp = bloque.split("**Respuesta**", 1)[1]
        formulas = _re.findall(r"`(=[^`]+)`", resp)
        formula = formulas[-1] if num.startswith("7b") else formulas[0]
        filas_p.append([num, cab.split("·")[1].strip() if "·" in cab else cab, prompt, formula,
                        QUE_REVISAR.get(num.rstrip("ab"), "Es la versión sin Prueba: compárala con la 7b.") if num != "7a" else
                        "Es la versión sin Prueba: compárala con la 7b."])
    return filas_p


PLANTILLA_EXTRA = {
    "leeme": ("Funciona en Excel para la web (gratis) y en Microsoft 365. En Excel 2021 fallan TEXTODESPUES (fórmula 3) y ELEGIRCOLS (fórmula 8); "
              "en 2016/2019, varias más. La fecha de corte de Resumen!B1 está fija (04/11/2026) para que veas los números del video: "
              "en tu planilla, escribe =HOY(). Sin macros ni vínculos externos. Respuestas generadas con Claude el 25/10/2026."),
    "hojas": [
        {"nombre": "Productos", "anchos": [190, 320, 170],
         "celdas": [["Código", "Producto", "Precio"]] + [[c, p, n(v)] for c, p, v in PRODUCTOS]},
        {"nombre": "Prompts", "formulas": False, "anchos": [60, 260, 900, 700, 520],
         "celdas": [["#", "Fórmula", "Prompt (Mapa · Meta · Prueba)", "Fórmula que dio Claude", "Qué revisar"]] + prompts_reales()},
        {"nombre": "Práctica", "anchos": [175, 340, 250, 230, 190, 140, 100, 120, 100, 140, 150, 100, 130],
         "celdas": pedidos(set(), filas_cod)},
    ]}

guion = {"titulo": "10 fórmulas de Excel con IA: tu planilla se llena sola", "duracion_objetivo_min": 10,
         "marca": {"nombre": "Atajos IA", "acento": "#ffd400"}, "subtitulos": False, "progreso": True,
         "descripcion_avisos": ("Respuestas generadas con Claude el 25/10/2026. Documentos y empresa de ejemplo ficticios. "
                                "Voz sintética: la primera persona del guion es un recurso narrativo. Plantilla gratis, sin registro. "
                                "Funciona en Excel para la web (gratis) y Microsoft 365; en Excel 2021 fallan TEXTODESPUES (fórmula 3) y ELEGIRCOLS (fórmula 8); "
                                "en 2016/2019, varias más."),
         "fuentes": [
             {"dato": "610.575, 2.446.165, 1.835.590 y el resto de las cifras de la planilla",
              "fuente": "Cálculo propio sobre la planilla ficticia «Distribuidora Sur» (produccion/video02/fuente/verificar_lo242.py)", "fecha": "2026-10"},
             {"dato": "BUSCARX existe en Excel 2021, 2024 y Microsoft 365; no en Excel 2016 ni 2019",
              "fuente": "https://support.microsoft.com/es-ES/Excel/functions/xlookup-function", "fecha": "2026-10"},
             {"dato": "TEXTODESPUES: Microsoft 365 y Excel 2024 (no Excel 2021)",
              "fuente": "https://support.microsoft.com/es-ES/Excel/functions/textafter-function", "fecha": "2026-10"},
             {"dato": "ELEGIRCOLS: Microsoft 365 y Excel para la web; Excel 2024 PENDIENTE de confirmar (no se afirma en el video)",
              "fuente": "https://support.microsoft.com/office/choosecols-function-bf117976-2722-4466-9b9a-1c01ed9aebff", "fecha": "2026-10"},
             {"dato": "Excel para la web, gratis con cuenta Microsoft (página oficial de Office gratis en la web)",
              "fuente": "https://www.microsoft.com/microsoft-365/free-office-online-for-the-web", "fecha": "2026-10"},
             {"dato": "ELEGIRCOLS no está en Excel 2021 (llegó con las funciones de 2024)",
              "fuente": "https://exceljet.net/functions · https://www.bettersolutions.com/excel/functions/updates-2024-new-functions.htm", "fecha": "2026-10"},
             {"dato": "Separador de listas (coma o punto y coma) según la configuración regional: PENDIENTE de URL oficial; el video solo dice «¿tu Excel usa coma? dilo en el mapa»",
              "fuente": "pendiente", "fecha": "2026-10"}],
         "plantilla_extra": PLANTILLA_EXTRA,
         "escenas": E}
json.dump(guion, open(f"{RAIZ}/produccion/video02/guion.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
pal = sum(len(x["voz"].split()) for e in E for x in e["beats"])
print("escenas", len(E), "palabras", pal)
