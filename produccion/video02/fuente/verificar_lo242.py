#!/usr/bin/env python3
"""Verificación de video02 con LibreOffice 24.2, que no tiene BUSCARX, TEXTODESPUES, FILTRAR, ORDENAR, UNICOS ni ELEGIRCOLS.

1. Genera la plantilla con herramientas/plantilla_xlsx.py (misma lógica que --verificar).
2. Reemplaza, solo en una copia, cada función nueva por un equivalente clásico:
   BUSCARX(x;A;C;"no") -> SI.ERROR(INDICE(C;COINCIDIR(x;A;0));"no")
   TEXTODESPUES(D2;"| ") -> EXTRAE(D2;HALLAR("| ";D2)+2;999)
   Desborde de FILTRAR/ORDENAR (Resumen!D2:F5): fila i = i-ésimo neto vencido más grande (AGREGAR) y su cliente/vencimiento por SUMAPRODUCTO.
   Desborde de UNICOS/ORDENAR (Resumen!A8:A12): i-ésimo cliente distinto en orden alfabético, con CONTAR.SI sobre la columna C.
3. Recalcula con LibreOffice y compara con cada valor que muestra el video.
"""
import os, re, shutil, subprocess, sys
sys.path.insert(0, "/home/user/nube/herramientas")
import json
import plantilla_xlsx as P
from openpyxl import load_workbook
from datetime import datetime

BASE = "/home/user/nube/produccion/video02"
TMP = "/home/user/nube/produccion/video02/build/guion/lo242"
os.makedirs(TMP, exist_ok=True)

guion = json.load(open(BASE + "/guion.json", encoding="utf-8"))
hojas = {}
for e in [e for e in guion["escenas"] if e["plantilla"] == "excel" and not e["datos"].get("solo_video")]:
    datos, escritas, esperados = P.estado_final(e)
    h = hojas.setdefault(e["datos"]["hoja"], {"celdas": {}, "esperados": {}})
    for ref, v in datos.items():
        ant = h["celdas"].get(ref)
        if not (isinstance(ant, str) and ant.startswith("=")) and not (ref in h["esperados"] and ant is None):
            h["celdas"][ref] = v
    h["celdas"].update(escritas)
    h["esperados"].update(esperados)

subprocess.run([sys.executable, "/home/user/nube/herramientas/plantilla_xlsx.py", "video02"], check=True, capture_output=True)
origen = BASE + "/plantilla/Distribuidora Sur.xlsx"
wb = load_workbook(origen)
cambios = 0
for ws in wb.worksheets:
    for fila in ws.iter_rows():
        for c in fila:
            v = c.value
            if not isinstance(v, str) or not v.startswith("="):
                continue
            n = re.sub(r'_xlfn\.XLOOKUP\(([A-Z]+\d+),([^,]+),([^,]+),("[^"]*")\)', r'IFERROR(INDEX(\3,MATCH(\1,\2,0)),\4)', v)
            n = re.sub(r'_xlfn\.TEXTAFTER\(([A-Z]+\d+),"\| "\)', r'MID(\1,SEARCH("| ",\1)+2,999)', n)
            if n != v:
                c.value = n
                cambios += 1
R = wb["Resumen"]
V = 'Pedidos!$M$2:$M$13="Vencido"'
for i in range(4):
    r = 2 + i
    R[f"F{r}"] = f"=SUMPRODUCT(LARGE(({V})*Pedidos!$J$2:$J$13,{i + 1}))"
    fila = f"SUMPRODUCT((Pedidos!$J$2:$J$13=F{r})*({V})*ROW(Pedidos!$J$2:$J$13))"
    R[f"D{r}"] = f"=INDEX(Pedidos!$C:$C,{fila})"
    R[f"E{r}"] = f"=INDEX(Pedidos!$K:$K,{fila})"
# i-ésimo cliente distinto en orden alfabético: el que tiene exactamente i-1 clientes distintos menores que él
for i in range(5):
    R[f"A{8 + i}"] = ('=INDEX(Pedidos!$C$2:$C$13,MATCH(' + str(i) + ',INDEX(MMULT((Pedidos!$C$2:$C$13>TRANSPOSE(Pedidos!$C$2:$C$13))/'
                      'TRANSPOSE(COUNTIF(Pedidos!$C$2:$C$13,Pedidos!$C$2:$C$13)),ROW(Pedidos!$C$2:$C$13)^0),0),0))')
R["H1"] = "=SUMPRODUCT(1/COUNTIF(Pedidos!$C$2:$C$13,Pedidos!$C$2:$C$13))"  # clientes distintos (limpios)
R["H2"] = "=SUMPRODUCT(1/COUNTIF(Pedidos!$B$2:$B$13,Pedidos!$B$2:$B$13))"  # "clientes" con los nombres sucios
R["H3"] = '=SUMIF(Pedidos!$M$2:$M$13,"Vencido",Pedidos!$J$2:$J$13)'
R["H4"] = '=COUNTIF(Pedidos!$M$2:$M$13,"Vencido")'
R["H5"] = "=SUMPRODUCT((Pedidos!$K$2:$K$13<$B$1)*Pedidos!$J$2:$J$13)"  # la fórmula escrita a mano: total "vencido"
R["H6"] = "=SUMPRODUCT((Pedidos!$K$2:$K$13<$B$1)*1)"
copia = TMP + "/copia.xlsx"
wb.save(copia)
subprocess.run(["soffice", "--headless", "--convert-to", "xlsx", "--outdir", TMP + "/out", copia], check=True, capture_output=True)
calc = load_workbook(TMP + "/out/copia.xlsx", data_only=True)
err = 0
total = 0
for nombre, h in hojas.items():
    ws = calc[nombre]
    for ref, esperado in h["esperados"].items():
        total += 1
        real = ws[ref].value
        num, _ = P.valor_celda(esperado)
        if isinstance(num, datetime):
            if isinstance(real, datetime):
                real = esperado if real.date() == num.date() else real
            elif isinstance(real, (int, float)):
                num = (num - datetime(1899, 12, 30)).days
        ok = (isinstance(num, (int, float)) and isinstance(real, (int, float)) and abs(real - num) <= max(0.01, abs(num) * 0.001)) or str(real) == str(esperado)
        if not ok:
            err += 1
            print(f"  ✗ {nombre}!{ref}: video «{esperado}» · LibreOffice «{real}»")
print(f"Funciones reemplazadas en la copia: {cambios}")
print("Chequeos: clientes distintos limpios =", calc["Resumen"]["H1"].value, "· con nombres sucios =", calc["Resumen"]["H2"].value,
      "· total vencido =", calc["Resumen"]["H3"].value, "· facturas vencidas =", calc["Resumen"]["H4"].value,
      "· con la fórmula escrita a mano:", calc["Resumen"]["H6"].value, "facturas,", calc["Resumen"]["H5"].value)
print(f"{total - err}/{total} valores coinciden" + ("" if err else " ✔"))
