"""Base ficticia de Distribuidora Sur para video03 (dashboard).

Genera los pedidos del 01/01/2026 al 03/11/2026 (semilla fija) e incluye,
textuales, las 12 filas de video02 (agosto-octubre, con PAP-201 ya corregido
a PAP-210). Imprime los KPI que usa idea.md. Datos ficticios.
Uso: python3 produccion/video03/fuente/datos_base.py [--csv salida.csv]
"""
import calendar, csv, datetime as dt, random, sys

PRODUCTOS = {"LIM-010": 2400, "LIM-020": 3100, "LIM-030": 1150, "LIM-040": 9800,
             "PAP-200": 4500, "PAP-210": 6200, "PAP-220": 3900}
CLIENTES = ["Ferretería El Tornillo", "Librería San Martín Srl", "Kiosco La Esquina",
            "Colegio Nuevo Horizonte", "Hotel Mirador"]
VENDEDORES = ["Diego Paz", "Carla Ruiz", "Tomás Gil"]
CORTE = dt.date(2026, 11, 3)

V02 = [  # fecha, cliente, vendedor, código, cant, pagado (video02)
    ("2026-08-04", 0, 0, "LIM-010", 40, "Sí"), ("2026-08-12", 1, 1, "PAP-200", 120, "No"),
    ("2026-08-21", 2, 2, "LIM-020", 15, "Sí"), ("2026-09-02", 0, 0, "PAP-210", 60, "Sí"),
    ("2026-09-09", 3, 1, "PAP-200", 300, "No"), ("2026-09-15", 2, 2, "LIM-030", 25, "No"),
    ("2026-09-23", 1, 0, "PAP-220", 40, "Sí"), ("2026-09-30", 4, 0, "LIM-040", 12, "No"),
    ("2026-10-06", 3, 1, "PAP-220", 150, "No"), ("2026-10-14", 4, 2, "LIM-040", 30, "No"),
    ("2026-10-22", 2, 0, "PAP-210", 10, "No"), ("2026-10-28", 0, 1, "LIM-020", 50, "Sí")]


def desc(bruto):
    return 0.10 if bruto >= 100000 else 0.05 if bruto >= 40000 else 0.0


def fin_mes(f, n):
    y, m = f.year + (f.month - 1 + n) // 12, (f.month - 1 + n) % 12 + 1
    return dt.date(y, m, calendar.monthrange(y, m)[1])


def fila(f, c, v, cod, cant, pag):
    bruto = cant * PRODUCTOS[cod]
    return {"fecha": f, "cliente": CLIENTES[c], "vendedor": VENDEDORES[v], "codigo": cod,
            "cant": cant, "precio": PRODUCTOS[cod], "desc": desc(bruto),
            "neto": round(bruto * (1 - desc(bruto))), "vence": fin_mes(f, 1), "pagado": pag}


def generar():
    rnd = random.Random(1335)  # semilla elegida para una tendencia estable (+8 % oct. vs sep.)
    filas = [fila(dt.date.fromisoformat(f), c, v, cod, q, p) for f, c, v, cod, q, p in V02]
    d = dt.date(2026, 1, 2)
    while d <= CORTE:
        for _ in range(rnd.choice([0, 1, 1, 2]) if d.weekday() < 5 else 0):
            cod = rnd.choice(list(PRODUCTOS))
            q = rnd.choice([10, 12, 15, 20, 25, 30, 40, 50, 60, 80, 100, 120])
            v = fila(d, rnd.randrange(5), rnd.randrange(3), cod, q, "No")
            v["pagado"] = "Sí" if v["vence"] < dt.date(2026, 10, 1) and rnd.random() < 0.95 \
                else ("Sí" if rnd.random() < 0.4 and v["vence"] < CORTE else "No")
            filas.append(v)
        d += dt.timedelta(days=1)
    return sorted(filas, key=lambda r: r["fecha"])


def total(filas, desde, hasta):
    return sum(r["neto"] for r in filas if desde <= r["fecha"] <= hasta)


if __name__ == "__main__":
    filas = generar()
    if "--csv" in sys.argv:
        with open(sys.argv[sys.argv.index("--csv") + 1], "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=filas[0].keys()); w.writeheader(); w.writerows(filas)
    print("pedidos:", len(filas))
    for m in range(1, 12):
        a = dt.date(2026, m, 1); b = min(fin_mes(a, 0), CORTE)
        n = sum(1 for r in filas if a <= r["fecha"] <= b)
        print(f"2026-{m:02d}", n, total(filas, a, b))
    nov = total(filas, dt.date(2026, 11, 1), CORTE)
    octu = total(filas, dt.date(2026, 10, 1), dt.date(2026, 10, 31))
    sep = total(filas, dt.date(2026, 9, 1), dt.date(2026, 9, 30))
    oct3 = total(filas, dt.date(2026, 10, 1), dt.date(2026, 10, 3))
    print("ingenuo nov vs oct:", nov, octu, f"{nov/octu-1:+.1%}")
    print("mismo tramo 1-3 nov vs 1-3 oct:", nov, oct3, f"{(nov/oct3-1) if oct3 else float('nan'):+.1%}")
    print("último mes cerrado oct vs sep:", octu, sep, f"{octu/sep-1:+.1%}")
    ytd = total(filas, dt.date(2026, 1, 1), CORTE)
    print("acumulado año:", ytd)
    for v in VENDEDORES:
        print(v, sum(r["neto"] for r in filas if r["vendedor"] == v))
