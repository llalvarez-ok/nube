#!/usr/bin/env python3
"""Arma produccion/video02/guion.json. Los valores de la planilla se calculan aquí, de forma independiente."""
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


# ---------------------------------------------------------------- HOOK
esc("excel", {"archivo": ARCH, "hoja": "Resumen", "anchos": RES_ANCHOS, "solo_video": True, "seleccion_inicial": "B1",
              "celdas": resumen(OCT, True, True, True, "01/10/2026")}, [
    b("Esta planilla se completa sola: precios, vencimientos, cobranza y el resumen del lunes.",
      [dict(GRAF, x=1222, y=262, ancho=310, retraso=0), {"tipo": "resaltar", "rango": "B9", "color": "#ffd400", "etiqueta": "PAGADO", "retraso": 1.4}]),
    b("Diez fórmulas que le pedí a una IA gratis, en minutos. A mano me llevaban unas cuatro horas; es una estimación mía.",
      {"tipo": "resaltar", "rango": "D2:F5", "color": "#107c41", "hasta": 3.5},
      tts="Diez fórmulas que le pedí a una IA gratis, en minutos. A mano me llevaban unas cuatro horas; es una estimación mía."),
    b("Ojo con ese sello: una fórmula casi le cobra dos veces a un cliente que ya había pagado. Te muestro cuál, y cómo la atrapé.",
      {"tipo": "zoom", "rango": "A7:B12", "escala": 1.5}),
    b("Uso un prompt de tres partes. Casi nadie usa la tercera, y es la que encontró el error.",
      {"tipo": "zoom_fuera"}),
], transicion="corte", entrada=0.1)

esc("lista", {"titulo": "Lo que necesitas", "items": [
    {"texto": "Excel para la web *gratis*", "detalle": "o Microsoft 365 · no sirve Excel 2016 ni 2019", "icono": "sheet"},
    {"texto": "Una IA gratis", "detalle": "uso Claude · el mismo prompt va en ChatGPT o Copilot", "icono": "sparkles"},
    {"texto": "Datos *ficticios*", "detalle": "la distribuidora es inventada", "icono": "file-spreadsheet"}]}, [
    b("Lo que necesitas: Excel para la web, que es gratis, o Microsoft 365. Varias de estas fórmulas no existen en Excel 2016 ni 2019."),
    b("Una IA gratis. Yo uso Claude; el mismo prompt funciona en ChatGPT o en Copilot gratis."),
    b("Y la empresa es inventada: los datos son ficticios. Al final vas a poder pedir tus fórmulas y comprobarlas antes de confiar en ellas."),
])

# ---------------------------------------------------------------- PLANILLA SUCIA
esc("excel", {"archivo": ARCH, "hoja": "Pedidos", "seleccion_inicial": "A1",
              "anchos": [175, 340, 250, 230, 190, 140, 100, 120, 100, 140, 150, 100, 130],
              "celdas": pedidos(set(), filas_cod)}, [
    b("Esta es Distribuidora Sur. Así exporta su sistema los pedidos: nombres con espacios y mayúsculas mezcladas.",
      {"tipo": "resaltar", "rango": "B2:B13", "color": "#e5484d", "etiqueta": "nombres sucios", "retraso": 0.3}),
    b("El vendedor viene pegado a su código. Y las columnas vacías las va a llenar cada fórmula, una detrás de otra: cada una usa el resultado de la anterior.",
      [{"tipo": "resaltar", "rango": "D2:D13", "color": "#e5484d", "retraso": 0.1}, {"tipo": "seleccionar", "rango": "C2:C13", "retraso": 1.6}]),
])

# ---------------------------------------------------------------- F1 BUSCARX
esc("capitulo", {"numero": 1, "total": 10, "titulo": "BUSCARX: el precio del catálogo"},
    [b("Fórmula uno: traer el precio de cada pedido.")], capitulo="1. BUSCARX: traer precios del catálogo")

M1 = ("Excel para la web en español, separador punto y coma. Hoja Pedidos, filas 2 a 13: A Fecha, B Cliente, C Cliente limpio, "
      "D Vendedor, E Vendedor limpio, F Código, G Cantidad, H Precio, I Descuento, J Neto, K Vence, L Pagado (Sí/No), M Estado. "
      "Catálogo en la hoja Productos: A Código, C Precio. Fecha de corte en Resumen!B1. "
      "En H2 quiero el precio de cada código; si no existe, que diga \"Código no existe\". Una fórmula para copiar hacia abajo.")
esc("chat", {"app": "Claude", "modelo": "versión gratuita"}, [
    b("Primero, el mapa: qué hay en cada columna, y que mi Excel está en español con punto y coma. Después, la meta, en palabras.",
      {"tipo": "prompt", "texto": M1, "duracion": 3.5}),
    b("Y la respuesta: una fórmula, buscar equis, lista para pegar. Hasta aquí, dos partes del método.",
      {"tipo": "respuesta", "texto": "Escribe esto en H2 y cópialo hasta H13. El último argumento es lo que muestra si no encuentra el código, así que no verás #N/A:",
       "formula": "=BUSCARX(F2;Productos!A:A;Productos!C:C;\"Código no existe\")"},
      tts="Y la respuesta: una fórmula, buscar equis, lista para pegar. Hasta aquí, dos partes del método."),
])

esc("excel", {"archivo": ARCH, "hoja": "Productos", "anchos": [190, 320, 170], "seleccion_inicial": "A1",
              "celdas": [["Código", "Producto", "Precio"]] + [[c, p, n(v)] for c, p, v in PRODUCTOS]}, [
    b("El catálogo vive en otra hoja: el código en la columna A y el precio en la C. Por eso el mapa lo dice.",
      [{"tipo": "resaltar", "rango": "A2:A8", "color": "#3b6fd8", "etiqueta": "busca aquí", "retraso": 0.2},
       {"tipo": "resaltar", "rango": "C2:C8", "color": "#107c41", "etiqueta": "devuelve esto", "retraso": 1.6}]),
])

VIS_V1 = {"B": 330, "F": 170, "G": 120, "H": 300}
V1 = anchos(VIS_V1)
esc("excel", {"archivo": ARCH, "hoja": "Pedidos", "anchos": V1, "seleccion_inicial": "H2", "celdas": ocultar(pedidos(set(), filas_cod), VIS_V1)}, [
    b("Buscar equis es la versión nueva de buscar uve: no se rompe si agregas columnas.",
      {"tipo": "zoom", "rango": "F1:H4", "escala": 1.5}, tts="Buscar equis es la versión nueva de buscar uve: no se rompe si agregas columnas."),
    b("La pego en la primera fila.",
      {"tipo": "escribir", "celda": "H2", "texto": "=BUSCARX(F2;Productos!A:A;Productos!C:C;\"Código no existe\")", "duracion": 2.6}),
    b("Dos mil cuatrocientos: el precio del cloro.", {"tipo": "calcular", "celda": "H2", "valor": "2.400"}),
    b("¿Tu Excel usa coma en vez de punto y coma? Mira cualquier fórmula que ya tengas. En México suele ser coma: dilo en el mapa.",
      [{"tipo": "mover", "celda": "B4"}, {"tipo": "nota", "celda": "H2", "texto": "¿*;* o *,*? Mira una fórmula que ya tengas", "retraso": 0.4}]),
    b("Ahora la arrastro hacia abajo.",
      [{"tipo": "quitar_nota"}, {"tipo": "zoom_fuera", "duracion": 0.8},
       {"tipo": "rellenar", "rango": "H2:H13", "valores": [("Código no existe" if r["F"] == "PAP-201" else n(r["H"])) for r in filas_cod], "retraso": 0.6}]),
    b("Pero fíjate en la fila doce. No es un error, es un aviso: el código PAP-201 no existe.",
      [{"tipo": "resaltar", "rango": "F12:H12", "color": "#e5484d", "etiqueta": "aviso, no error"}],
      tts="Pero fíjate en la fila doce. No es un error, es un aviso: el código pe, a, pe, dos, cero, uno, no existe."),
    b("Era PAP-210. Lo corrijo, y el precio aparece solo.",
      [{"tipo": "escribir", "celda": "F12", "texto": "PAP-210", "duracion": 1.0}, {"tipo": "calcular", "celda": "H12", "valor": "6.200", "retraso": 2.2}],
      tts="Era pe, a, pe, dos, uno, cero. Lo corrijo, y el precio aparece solo."),
])

# ---------------------------------------------------------------- F2 NOMPROPIO + ESPACIOS
esc("capitulo", {"numero": 2, "total": 10, "titulo": "NOMPROPIO + ESPACIOS: nombres prolijos"},
    [b("Fórmula dos: limpiar los nombres.")], capitulo="2. NOMPROPIO y ESPACIOS: limpiar nombres")
VIS_V2 = {"B": 360, "C": 360, "F": 150, "G": 100, "H": 140}
V2 = anchos(VIS_V2)
esc("excel", {"archivo": ARCH, "hoja": "Pedidos", "anchos": V2, "seleccion_inicial": "C2", "celdas": ocultar(pedidos({"H"}), VIS_V2)}, [
    b("Con el mapa ya enviado, le pido solo la meta: el nombre prolijo, sin espacios de más y con mayúscula inicial.",
      {"tipo": "zoom", "rango": "B1:C5", "escala": 1.45}),
    b("Me da dos funciones, una dentro de otra: espacios quita los espacios sobrantes; nompropio arregla las mayúsculas.",
      {"tipo": "escribir", "celda": "C2", "texto": "=NOMPROPIO(ESPACIOS(B2))", "duracion": 1.8},
      tts="Me da dos funciones, una dentro de otra: espacios quita los espacios sobrantes; nom propio arregla las mayúsculas."),
    b("Ferretería El Tornillo. La copio, y las doce filas quedan prolijas.",
      [{"tipo": "calcular", "celda": "C2", "valor": filas[0]["C"], "derecha": False},
       {"tipo": "zoom_fuera", "retraso": 1.0, "duracion": 0.8},
       {"tipo": "rellenar", "rango": "C2:C13", "valores": col("C", "C"), "retraso": 1.6}]),
    b("Veredicto honesto: la sigla SRL quedó en minúsculas. La propia IA me lo advirtió; las siglas, revísalas a mano.",
      [{"tipo": "resaltar", "rango": "C3", "color": "#e5484d", "etiqueta": "Srl", "retraso": 0.3}],
      tts="Veredicto honesto: la sigla ese, erre, ele, quedó en minúsculas. La propia IA me lo advirtió; las siglas, revísalas a mano."),
])

# ---------------------------------------------------------------- F3 TEXTODESPUES
esc("capitulo", {"numero": 3, "total": 10, "titulo": "TEXTODESPUES: separar el vendedor"},
    [b("Fórmula tres: separar al vendedor de su código.")], capitulo="3. TEXTODESPUES: separar texto pegado")
VIS_V3 = {"C": 330, "D": 300, "E": 250, "F": 150, "G": 100, "H": 140}
V3 = anchos(VIS_V3)
esc("excel", {"archivo": ARCH, "hoja": "Pedidos", "anchos": V3, "seleccion_inicial": "E2", "celdas": ocultar(pedidos({"H", "C"}), VIS_V3)}, [
    b("Viene así: código, una barra y el nombre.",
      [{"tipo": "zoom", "rango": "C1:E5", "escala": 1.45}, {"tipo": "resaltar", "rango": "D2", "color": "#3b6fd8", "retraso": 1.0, "hasta": 3}]),
    b("La IA conoce una función de 2022 que casi nadie usa: texto después. Todo lo que viene después de la barra.",
      {"tipo": "escribir", "celda": "E2", "texto": "=TEXTODESPUES(D2;\"| \")", "duracion": 1.6},
      tts="La IA conoce una función de dos mil veintidós que casi nadie usa: texto después. Todo lo que viene después de la barra."),
    b("Diego Paz. Su gemela, texto antes, te da el código.",
      [{"tipo": "calcular", "celda": "E2", "valor": "Diego Paz", "derecha": False},
       {"tipo": "nota", "celda": "E2", "texto": "TEXTOANTES(D2;\" |\") → *V01*", "retraso": 0.8}]),
    b("Copio hacia abajo. ¿Y sin la IA? Habría terminado con extrae y hallar, o separando a mano.",
      [{"tipo": "quitar_nota"}, {"tipo": "zoom_fuera", "duracion": 0.8},
       {"tipo": "rellenar", "rango": "E2:E13", "valores": col("E", "E"), "retraso": 0.5}],
      tts="Copio hacia abajo. ¿Y sin la IA? Habría terminado con extrae y hallar, o separando a mano."),
])

esc("titular", {"etiqueta": "Plantilla gratis", "icono": "file-spreadsheet",
                "lineas": ["Los 10 prompts,", {"texto": "con *qué revisar*", "beat": 0}],
                "sub": "Hoja «Prompts» · enlace en la descripción", "sub_beat": 1}, [
    b("Las diez consignas completas están en la plantilla gratis, en la hoja Prompts, con una columna de qué revisar."),
    b("Y en un rato vas a ver la fórmula que le cobraba dos veces a un cliente, y cómo la atrapé con una sola pregunta."),
])

# ---------------------------------------------------------------- F4 SI.CONJUNTO
esc("capitulo", {"numero": 4, "total": 10, "titulo": "SI.CONJUNTO: descuentos por tramos"},
    [b("Fórmula cuatro: descuentos por tramos.")], capitulo="4. SI.CONJUNTO: descuentos por tramos")
esc("chat", {"app": "Claude", "modelo": "versión gratuita"}, [
    b("La política de descuentos, escrita como la diría mi jefe: diez por ciento desde cien mil, cinco desde cuarenta mil.",
      {"tipo": "prompt", "texto": "En I2 quiero el descuento según el total de la compra (G2*H2): 10 % si llega a 100.000; 5 % si llega a 40.000; si no, 0 %."}),
    b("Ojo con el orden: la IA pone los tramos de mayor a menor, y cierra con verdadero, que significa en cualquier otro caso.",
      {"tipo": "respuesta", "texto": "Las condiciones se evalúan en orden, por eso va primero el tramo más alto. El VERDADERO del final funciona como \"en cualquier otro caso\". Dale formato de porcentaje a la columna I:",
       "formula": "=SI.CONJUNTO(G2*H2>=100000;10%;G2*H2>=40000;5%;VERDADERO;0)"}),
])
VIS_V4 = {"C": 330, "F": 150, "G": 100, "H": 140, "I": 130, "J": 190}
V4 = anchos(VIS_V4)
esc("excel", {"archivo": ARCH, "hoja": "Pedidos", "anchos": V4, "seleccion_inicial": "I2", "celdas": ocultar(pedidos({"H", "C", "E"}), VIS_V4)}, [
    b("La pego en la columna del descuento.",
      [{"tipo": "zoom", "rango": "F1:J4", "escala": 1.4},
       {"tipo": "escribir", "celda": "I2", "texto": "=SI.CONJUNTO(G2*H2>=100000;10%;G2*H2>=40000;5%;VERDADERO;0)", "duracion": 2.4, "retraso": 1.0}],
      tts="La pego en la columna del descuento."),
    b("Cuarenta bidones de cloro suman noventa y seis mil: cinco por ciento.", {"tipo": "calcular", "celda": "I2", "valor": "5 %"}),
    b("Abajo, cada pedido cae en su tramo.",
      {"tipo": "rellenar", "rango": "I2:I13", "valores": col("I", "I", pct)}),
    b("El neto es una multiplicación simple. Esa no cuenta entre las diez.",
      {"tipo": "escribir", "celda": "J2", "texto": "=G2*H2*(1-I2)", "duracion": 1.2}),
    b("Noventa y un mil doscientos, y toda la columna lista.",
      [{"tipo": "calcular", "celda": "J2", "valor": n(filas[0]["J"])}, {"tipo": "zoom_fuera", "retraso": 0.5, "duracion": 0.8},
       {"tipo": "rellenar", "rango": "J2:J13", "valores": col("J", "J", n), "retraso": 1.0}]),
])

# ---------------------------------------------------------------- F5 FIN.MES
esc("capitulo", {"numero": 5, "total": 10, "titulo": "FIN.MES: vencimientos sin errores de calendario"},
    [b("Fórmula cinco: el vencimiento.")], capitulo="5. FIN.MES: fechas de vencimiento")
VIS_V5 = {"A": 170, "C": 330, "J": 170, "K": 190}
V5 = anchos(VIS_V5)
esc("excel", {"archivo": ARCH, "hoja": "Pedidos", "anchos": V5, "seleccion_inicial": "K2", "celdas": ocultar(pedidos({"H", "C", "E", "I", "J"}), VIS_V5)}, [
    b("La condición de pago es a fin del mes siguiente. Casi todos suman treinta días, y fallan con los meses de treinta y uno.",
      {"tipo": "zoom", "rango": "A1:K4", "escala": 1.4}),
    b("Se lo dije así a la IA, y me dio fin punto mes.",
      {"tipo": "escribir", "celda": "K2", "texto": "=FIN.MES(A2;1)", "duracion": 1.2}, tts="Se lo dije así a la IA, y me dio fin punto mes."),
    b("Pedido del 4 de agosto: vence el 30 de septiembre.", {"tipo": "calcular", "celda": "K2", "valor": f(filas[0]["K"])},
      tts="Pedido del cuatro de agosto: vence el treinta de septiembre."),
    b("Ojo: si ves un número como 46.295, a la celda le falta formato de fecha.",
      [{"tipo": "mover", "celda": "C6"}, {"tipo": "nota", "celda": "K2", "texto": "¿Ves *46295*? Dale formato de fecha", "retraso": 0.4}],
      tts="Ojo: si ves un número como cuarenta y seis mil doscientos noventa y cinco, a la celda le falta formato de fecha."),
    b("La copio hacia abajo, y cada pedido tiene su vencimiento.",
      [{"tipo": "quitar_nota"}, {"tipo": "zoom_fuera", "duracion": 0.8},
       {"tipo": "rellenar", "rango": "K2:K13", "valores": [f(r["K"]) for r in filas], "retraso": 0.5}]),
])

esc("titular", {"etiqueta": "Lo que viene", "icono": "triangle-alert",
                "lineas": ["Una fórmula *perfecta*", "que cobraba dos veces"],
                "sub": "Si te sirve, suscríbete: una planilla resuelta con IA cada semana", "sub_beat": 1}, [
    b("Lo que viene es lo que más me sirvió: una fórmula que escribí yo, que parecía perfecta, y la parte del método que la atrapó."),
    b("Si te está sirviendo, suscríbete: cada semana resuelvo una planilla nueva con IA."),
])

# ---------------------------------------------------------------- F6 SUMAR.SI.CONJUNTO
esc("capitulo", {"numero": 6, "total": 10, "titulo": "SUMAR.SI.CONJUNTO: ventas por vendedor"},
    [b("Fórmula seis: ventas por vendedor y por mes.")], capitulo="6. SUMAR.SI.CONJUNTO: ventas por vendedor y mes")
F6 = "=SUMAR.SI.CONJUNTO(Pedidos!J:J;Pedidos!E:E;A3;Pedidos!A:A;\">=\"&$B$2;Pedidos!A:A;\"<=\"&FIN.MES($B$2;0))"
esc("chat", {"app": "Claude", "modelo": "versión gratuita"}, [
    b("Para la reunión de ventas: cuánto vendió cada vendedor en el mes que elijo.",
      {"tipo": "prompt", "texto": "En Resumen tengo los vendedores en A3:A5 y en B2 el primer día del mes que quiero ver. En B3 quiero el neto vendido por ese vendedor en ese mes. Una fórmula para copiar hacia abajo."}),
    b("Aquí todos se traban: el criterio de fechas y los signos de dólar. La IA los pone, y explica por qué.",
      {"tipo": "respuesta", "texto": "Suma el neto (J) donde el vendedor (E) es el de A3 y la fecha (A) está entre el primer y el último día del mes de B2. Los $ dejan fija B2 al copiar; A3 sí cambia.",
       "formula": F6}),
])
esc("excel", {"archivo": ARCH, "hoja": "Resumen", "anchos": RES_ANCHOS, "seleccion_inicial": "B3", "celdas": resumen()}, [
    b("En la hoja Resumen, el mes va arriba: septiembre.",
      [{"tipo": "zoom", "rango": "A1:B5", "escala": 1.35}, {"tipo": "resaltar", "rango": "B2", "color": "#3b6fd8", "retraso": 0.9, "hasta": 2.6}]),
    b("Pego la fórmula en el primer vendedor.", {"tipo": "escribir", "celda": "B3", "texto": F6, "duracion": 3.2}),
    b("Diego Paz vendió 581.040 en septiembre.", {"tipo": "calcular", "celda": "B3", "valor": n(SEP[0])},
      tts="Diego Paz vendió quinientos ochenta y un mil cuarenta en septiembre."),
    b("La copio: Carla Ruiz, un millón doscientos quince mil.",
      {"tipo": "rellenar", "rango": "B3:B5", "valores": [n(v) for v in SEP]}),
    b("¿Y si cambio el mes a octubre? La tabla se recalcula sola.",
      [{"tipo": "escribir", "celda": "B2", "texto": "01/10/2026", "duracion": 1.0}]
      + [{"tipo": "calcular", "celda": f"B{3 + i}", "valor": n(v), "retraso": 2.0 + 0.15 * i} for i, v in enumerate(OCT)]),
    b("Fíjate en una pieza: fin punto mes, otra vez. Aquí marca el último día del mes elegido, así que suma del primero al treinta y uno.",
      [{"tipo": "mover", "celda": "A10"}, {"tipo": "nota", "celda": "B4", "texto": "FIN.MES($B$2;0) → *31/10/2026*", "lado": "abajo", "retraso": 0.3}]),
])

# ---------------------------------------------------------------- F7 EL GIRO
esc("capitulo", {"numero": 7, "total": 10, "titulo": "La IA como *revisora* de tus fórmulas"},
    [b("Fórmula siete: la IA como revisora.")], capitulo="7. La IA como revisora de tus fórmulas")
VIS_V7 = {"C": 330, "J": 170, "K": 180, "L": 120, "M": 200}
V7 = anchos(VIS_V7)
NAIVE = "=SI(K2<Resumen!$B$1;\"Vencido\";\"Al día\")"
GOOD = "=SI(L2=\"Sí\";\"Cobrado\";SI(K2<Resumen!$B$1;\"Vencido\";\"Al día\"))"
esc("excel", {"archivo": ARCH, "hoja": "Pedidos", "anchos": V7, "seleccion_inicial": "M2", "celdas": ocultar(pedidos({"H", "C", "E", "I", "J", "K"}), VIS_V7)}, [
    b("El estado de cada factura. Esta es corta, así que la escribí yo.", {"tipo": "zoom", "rango": "J1:M4", "escala": 1.4}),
    b("Si vence antes de la fecha de corte, vencido; si no, al día.",
      [{"tipo": "escribir", "celda": "M2", "texto": NAIVE, "duracion": 2.2},
       {"tipo": "nota", "celda": "K3", "texto": "Escrita *a mano*, como la escribe casi todo el mundo", "lado": "abajo", "retraso": 2.6}]),
    b("No da error.", {"tipo": "calcular", "celda": "M2", "valor": "Vencido", "derecha": False}),
    b("La copio, y la cobranza sale sola: ocho facturas vencidas, dos millones cuatrocientos cuarenta y seis mil por cobrar.",
      [{"tipo": "quitar_nota"}, {"tipo": "zoom_fuera", "duracion": 0.8},
       {"tipo": "rellenar", "rango": "M2:M13", "valores": [r["M0"] for r in filas], "retraso": 0.5},
       {"tipo": "resaltar", "rango": "M2:M9", "color": "#e5484d", "etiqueta": "8 vencidas · 2.446.165", "retraso": 2.2}]),
    b("Parece perfecta, ¿no? Ahora viene la tercera parte del método.",
      {"tipo": "formato", "rango": "M2:M9", "fondo": "#ffd6d6"}),
])

esc("lista", {"titulo": "El prompt de 3 partes", "items": [
    {"texto": "*Mapa*", "detalle": "qué hay en cada columna y qué Excel usas", "icono": "map"},
    {"texto": "*Meta*", "detalle": "qué quieres, con la regla en palabras", "icono": "target"},
    {"texto": "*Prueba*", "detalle": "qué casos darían mal sin error, y qué debe dar en dos filas", "icono": "shield-check"}]}, [
    b("Mapa: dónde está cada dato."),
    b("Meta: qué quieres, en palabras."),
    b("Y la que casi nadie usa, la prueba: qué casos darían un resultado equivocado sin mostrar error, y qué debería dar en dos filas concretas."),
])

PRUEBA = ("Escribí esta fórmula para M2: =SI(K2<Resumen!$B$1;\"Vencido\";\"Al día\"). ¿Qué casos pueden hacer que dé un resultado equivocado "
          "sin mostrar error? ¿Qué debería dar la fila 2 (vence 30/09/2026, Pagado: Sí) y la fila 6 (vence 31/10/2026, Pagado: No), con corte 04/11/2026?")
esc("chat", {"app": "Claude", "modelo": "versión gratuita"}, [
    b("Pego mi fórmula en el chat, con la prueba.", {"tipo": "prompt", "texto": PRUEBA, "duracion": 3.5}),
    b("Y va directo al problema: mi fórmula no mira la columna Pagado. La fila dos ya estaba pagada, y dice vencido.",
      {"tipo": "respuesta", "texto": "1. Facturas pagadas: la fórmula no mira la columna L. Si ya se pagó pero su vencimiento pasó, dice \"Vencido\".<br>"
                                      "2. Si K está vacía, cuenta como 0 y también dice \"Vencido\".<br>"
                                      "Fila 2: da \"Vencido\", pero ya está pagada.<br>Fila 6: da \"Vencido\", y es correcto.<br>Fórmula corregida:",
       "formula": GOOD, "duracion": 5.5}),
])

esc("aviso", {"titulo": "3 clientes · 4 facturas *ya pagadas*", "nivel": "rojo", "icono": "phone-off",
              "texto": "Ferretería El Tornillo, Kiosco La Esquina y Librería San Martín figuraban como deudores."}, [
    b("El lunes habría llamado a tres clientes para cobrarles cuatro facturas que ya habían pagado."),
])
esc("cifra", {"valor": 610575, "etiqueta": "de más en la lista de cobranza", "fuente": "cálculo sobre la planilla ficticia del video"}, [
    b("610.575 de más en la lista de cobranza.", tts="Seiscientos diez mil quinientos setenta y cinco de más en la lista de cobranza."),
])

esc("excel", {"archivo": ARCH, "hoja": "Pedidos", "anchos": V7, "seleccion_inicial": "M2",
              "celdas": ocultar(pedidos({"H", "C", "E", "I", "J", "K", "M"}, m_ingenuo=True), VIS_V7)}, [
    b("Pego la corregida: primero mira si está pagada.",
      [{"tipo": "zoom", "rango": "J1:M4", "escala": 1.4},
       {"tipo": "escribir", "celda": "M2", "texto": GOOD, "duracion": 2.6, "retraso": 0.9}]),
    b("La fila dos ahora dice cobrado.", {"tipo": "calcular", "celda": "M2", "valor": "Cobrado", "derecha": False}),
    b("La copio: cuatro vencidas de verdad, un millón ochocientos treinta y cinco mil quinientos noventa.",
      [{"tipo": "zoom_fuera", "duracion": 0.8},
       {"tipo": "rellenar", "rango": "M2:M13", "valores": [r["M"] for r in filas], "retraso": 0.4},
       {"tipo": "formato", "celdas": {f"M{i + 2}": ("#ffd6d6" if r["M"] == "Vencido" else "#ffffff") for i, r in enumerate(filas)}, "retraso": 1.8},
       {"tipo": "resaltar", "rango": "M3", "color": "#107c41", "etiqueta": "4 vencidas · 1.835.590", "retraso": 2.4}]),
])

esc("titular", {"etiqueta": "Hallazgo honesto", "icono": "search-check",
                "tamano": 88, "lineas": ["A veces la IA te avisa sola.", {"texto": "La Prueba hace que", "beat": 1}, {"texto": "te lo diga *sí o sí*.", "beat": 1}]}, [
    b("A veces la IA te avisa sola: cuando le pedí esta fórmula con el mapa completo, me habló de la columna Pagado. Por eso el mapa nombra todas las columnas."),
    b("Pero no siempre pasa. La prueba hace que te lo diga sí o sí, aunque la fórmula la hayas escrito tú."),
])
esc("titular", {"tamano": 92, "lineas": ["Un error que *se ve*, se arregla.", {"texto": "El peligroso es el *creíble*.", "beat": 1}]}, [
    b("Una fórmula que da error es fácil de arreglar."),
    b("La peligrosa es la que da un resultado creíble y equivocado."),
])

# ---------------------------------------------------------------- F8 FILTRAR
esc("capitulo", {"numero": 8, "total": 10, "titulo": "FILTRAR: la cobranza del lunes en una celda"},
    [b("Fórmula ocho: el reporte de cobranza del lunes.")], capitulo="8. FILTRAR: cobranza en Excel, el reporte del lunes")
P8 = ("Mapa: el de antes. Meta: en Resumen!D2, una lista que se actualice sola con Cliente (C), Vence (K) y Neto (J) de las facturas "
      "\"Vencido\", de mayor a menor neto. Prueba: antes de darme la fórmula, dime qué casos darían un resultado equivocado sin error y qué debería salir arriba.")
F8 = "=SI.ERROR(ORDENAR(FILTRAR(ELEGIRCOLS(Pedidos!A2:M13;3;11;10);Pedidos!M2:M13=\"Vencido\");3;-1);\"Sin vencidos\")"
esc("chat", {"app": "Claude", "modelo": "versión gratuita"}, [
    b("Desde ahora, el prompt va con las tres partes: mapa, meta y prueba.", {"tipo": "prompt", "texto": P8, "duracion": 3.5}),
    b("Mira lo que encuentra la prueba antes de darme nada: si no hay vencidas, la fórmula fallaría. Y lo cubre.",
      {"tipo": "respuesta", "texto": "1. Si no hay ninguna vencida, FILTRAR no tiene nada que devolver y ORDENAR daría error. Lo cubro con SI.ERROR.<br>"
                                      "2. Los pedidos debajo de la fila 13 quedan afuera: amplía los rangos.<br>"
                                      "Arriba debería salir la vencida con el neto más alto.",
       "formula": F8, "duracion": 5}),
])
esc("excel", {"archivo": ARCH, "hoja": "Resumen", "anchos": RES_ANCHOS, "seleccion_inicial": "D2",
              "celdas": resumen(OCT, mes_fecha="01/10/2026")}, [
    b("Lo pego en la hoja Resumen, en una sola celda.",
      [{"tipo": "zoom", "rango": "D1:F5", "escala": 1.3},
       {"tipo": "resaltar", "rango": "D1:F1", "color": "#107c41", "etiqueta": "Cobranza del lunes", "retraso": 0.9, "hasta": 2.6}]),
    b("Tres funciones, de adentro hacia afuera. Elegir columnas toma cliente, vencimiento y neto.",
      {"tipo": "escribir", "celda": "D2", "texto": F8, "duracion": 3.2}, tts="Tres funciones, de adentro hacia afuera. Elegir columnas toma cliente, vencimiento y neto."),
    b("Filtrar deja solo las vencidas, y ordenar pone la más grande arriba.",
      {"tipo": "nota", "celda": "D3", "texto": "ELEGIRCOLS → FILTRAR → ORDENAR", "lado": "abajo"}),
    b("Y la lista se desborda sola: cuatro facturas.",
      [{"tipo": "quitar_nota"}]
      + [{"tipo": "calcular", "celda": f"{c}{2 + i}", "valor": v, "derecha": c != "D", "retraso": 0.1 + 0.12 * (3 * i + j)}
         for i, fila in enumerate(cobranza) for j, (c, v) in enumerate(zip("DEF", [fila[0], f(fila[1]), n(fila[2])]))]),
    b("Un millón ochocientos treinta y cinco mil quinientos noventa. Ese es tu lunes: a quién llamar, y por cuánto.",
      {"tipo": "resaltar", "rango": "F2:F5", "color": "#ffd400", "etiqueta": "Total 1.835.590"}),
    b("Y no tienes que volver a armarla: el lunes que viene cambias la fecha de corte, y la lista se rehace sola.",
      [{"tipo": "zoom", "rango": "A1:B2", "escala": 1.4}, {"tipo": "resaltar", "rango": "B1", "color": "#3b6fd8", "etiqueta": "fecha de corte", "retraso": 1.0, "hasta": 4.0}]),
])

# ---------------------------------------------------------------- F9 y F10
esc("capitulo", {"numero": 9, "total": 10, "titulo": "UNICOS + CONTAR.SI.CONJUNTO: el tablero de clientes"},
    [b("Fórmulas nueve y diez: el tablero de clientes.")], capitulo="9 y 10. UNICOS y CONTAR.SI.CONJUNTO: clientes y deudas")
F9 = "=ORDENAR(UNICOS(Pedidos!C2:C13))"
F10 = "=CONTAR.SI.CONJUNTO(Pedidos!C:C;A8;Pedidos!M:M;\"Vencido\")"
esc("excel", {"archivo": ARCH, "hoja": "Resumen", "anchos": RES_ANCHOS, "seleccion_inicial": "A8",
              "celdas": resumen(OCT, True, mes_fecha="01/10/2026")}, [
    b("Primero, la lista de clientes sin repetidos: únicos, dentro de ordenar.",
      [{"tipo": "zoom", "rango": "A6:B12", "escala": 1.4},
       {"tipo": "escribir", "celda": "A8", "texto": F9, "duracion": 1.8, "retraso": 1.0}]),
    b("Cinco clientes. Con los nombres sucios del principio habrían salido diez, porque únicos distingue un espacio de más. Por eso valió la pena limpiarlos.",
      [{"tipo": "calcular", "celda": f"A{8 + i}", "valor": c, "derecha": False, "retraso": 0.12 * i} for i, c in enumerate(clientes)]),
    b("Fórmula diez: cuántas facturas vencidas tiene cada uno. Contar si conjunto, con dos condiciones.",
      {"tipo": "escribir", "celda": "B8", "texto": F10, "duracion": 2.6},
      tts="Fórmula diez: cuántas facturas vencidas tiene cada uno. Contar si punto conjunto, con dos condiciones."),
    b("Cuatro clientes deben una factura cada uno. La ferretería, ninguna: con la fórmula escrita a mano, le habría contado dos.",
      [{"tipo": "calcular", "celda": "B8", "valor": str(cuenta[0])},
       {"tipo": "rellenar", "rango": "B8:B12", "valores": [str(k) for k in cuenta], "retraso": 0.7},
       {"tipo": "resaltar", "rango": "A9:B9", "color": "#ffd400", "etiqueta": "pagó todo", "retraso": 2.0}]),
    b("Y con eso, la hoja Resumen queda completa, con su gráfico.",
      [{"tipo": "zoom_fuera", "duracion": 0.8}, dict(GRAF, x=1222, y=262, ancho=310, retraso=0.6)]),
])

# ---------------------------------------------------------------- cierre
esc("comparar", {"titulo": "¿Cuándo *no* pedírsela a la IA?", "columnas": ["Si…", "Entonces"],
                 "filas": [["La fórmula es más corta que el prompt", "Escríbela tú, y pásala por la *Prueba*"],
                           ["No sabes ni qué función existe", "Pídesela a la IA"],
                           ["Combina tres funciones o más", "Pídesela a la IA"],
                           ["Tienes datos reales de clientes", "No los pegues: el Mapa solo lleva *columnas*"]]}, [
    b("¿Cuándo no usar la IA? Si la fórmula es más corta que el prompt, escríbela tú, y pásala por la prueba."),
    b("Si no sabes ni qué función existe, pídesela."),
    b("Si combina tres funciones o más, también."),
    b("Y nunca pegues datos reales de clientes en un chat gratis: el mapa solo necesita los nombres de las columnas."),
])
esc("titular", {"etiqueta": "Gratis", "icono": "download",
                "lineas": ["Distribuidora Sur", "*10 fórmulas con IA*"], "sub": "Pedidos, Resumen, Prompts y una hoja para practicar", "sub_beat": 1}, [
    b("¿Usas ChatGPT o Copilot? El prompt de tres partes es el mismo. La planilla completa, con las diez fórmulas, está gratis en la descripción."),
    b("Trae la hoja Prompts con las tres partes de cada consigna, y una hoja para practicar sin fórmulas."),
])
esc("final", {"titulo": "Sigue con *este atajo*"}, [
    b("Y si en tu trabajo también te llegan informes largos en pe de efe, mira este video: cómo resumirlos con IA sin que invente datos."),
])

guion = {"titulo": "10 fórmulas de Excel con IA: tu planilla se llena sola", "duracion_objetivo_min": 10,
         "marca": {"nombre": "Atajos IA", "acento": "#ffd400"}, "subtitulos": False, "progreso": True,
         "fuentes": [{"dato": "610.575, 2.446.165, 1.835.590 y el resto de las cifras de la planilla",
                      "fuente": "Cálculo propio sobre la planilla ficticia «Distribuidora Sur» (produccion/video02/guion.json, verificado con plantilla_xlsx.py)",
                      "fecha": "2026-10"},
                     {"dato": "«Unas cuatro horas a mano» (estimación, pendiente de medir por el creador)",
                      "fuente": "Estimación propia; ver produccion/video02/idea.md", "fecha": "2026-10"}],
         "escenas": E}
json.dump(guion, open(f"{RAIZ}/produccion/video02/guion.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
pal = sum(len(x["voz"].split()) for e in E for x in e["beats"])
print("escenas", len(E), "palabras", pal)
