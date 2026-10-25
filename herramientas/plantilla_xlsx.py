#!/usr/bin/env python3
"""Genera la plantilla .xlsx de un video a partir de las escenas "excel" de su guion.json.

    python3 herramientas/plantilla_xlsx.py video02
    python3 herramientas/plantilla_xlsx.py video02 --verificar   # además compara cada "calcular" con el valor real

Toma el estado final de cada hoja (datos + fórmulas escritas, insertadas o rellenadas),
traduce las fórmulas de Excel en español (SI, BUSCARX, ';') al formato interno del
archivo (IF, XLOOKUP, ','), convierte "$ 18.400" o "8 %" en números con formato y
guarda produccion/<video>/plantilla/<archivo>.xlsx, listo para Excel para la web.

--verificar recalcula con LibreOffice (si está instalado) y avisa si algún valor que
muestra el video no coincide con lo que da la fórmula: un error así es veto del verificador.

Las fechas "dd/mm/aaaa" se guardan como fechas reales. Las celdas de "datos" de una escena
no pisan una fórmula que ya se escribió en una escena anterior de la misma hoja, ni las
celdas de desborde de una matriz dinámica (las que se muestran con "calcular" sin fórmula). Una escena
con "datos": {"solo_video": true} (por ejemplo, el adelanto del resultado en el hook) no se
usa para armar la plantilla. LibreOffice 24.2 no calcula BUSCARX, TEXTODESPUES, FILTRAR,
ORDENAR, UNICOS ni ELEGIRCOLS (llegan en 24.8/25.x): esas celdas hay que verificarlas aparte.
"""

import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import column_index_from_string, get_column_letter

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FUNCIONES = {
    "SI.CONJUNTO": "IFS", "SI.ERROR": "IFERROR", "SI.ND": "IFNA", "SI": "IF", "Y": "AND", "O": "OR", "NO": "NOT",
    "BUSCARX": "XLOOKUP", "BUSCARV": "VLOOKUP", "BUSCARH": "HLOOKUP", "COINCIDIRX": "XMATCH", "COINCIDIR": "MATCH", "INDICE": "INDEX",
    "SUMAR.SI.CONJUNTO": "SUMIFS", "SUMAR.SI": "SUMIF", "CONTAR.SI.CONJUNTO": "COUNTIFS", "CONTAR.SI": "COUNTIF",
    "PROMEDIO.SI.CONJUNTO": "AVERAGEIFS", "PROMEDIO.SI": "AVERAGEIF", "SUMA": "SUM", "PROMEDIO": "AVERAGE", "CONTARA": "COUNTA",
    "CONTAR.BLANCO": "COUNTBLANK", "CONTAR": "COUNT", "MAX.SI.CONJUNTO": "MAXIFS", "MIN.SI.CONJUNTO": "MINIFS",
    "REDONDEAR": "ROUND", "REDONDEAR.MAS": "ROUNDUP", "REDONDEAR.MENOS": "ROUNDDOWN", "ENTERO": "INT", "ABS": "ABS",
    "FILTRAR": "FILTER", "UNICOS": "UNIQUE", "ORDENAR": "SORT", "ORDENARPOR": "SORTBY", "SECUENCIA": "SEQUENCE",
    "CONCAT": "CONCAT", "UNIRCADENAS": "TEXTJOIN", "CONCATENAR": "CONCATENATE", "IZQUIERDA": "LEFT", "DERECHA": "RIGHT",
    "EXTRAE": "MID", "LARGO": "LEN", "ESPACIOS": "TRIM", "MAYUSC": "UPPER", "MINUSC": "LOWER", "NOMPROPIO": "PROPER",
    "SUSTITUIR": "SUBSTITUTE", "TEXTO": "TEXT", "VALOR": "VALUE", "ENCONTRAR": "FIND", "HALLAR": "SEARCH",
    "TEXTOANTES": "TEXTBEFORE", "TEXTODESPUES": "TEXTAFTER", "DIVIDIRTEXTO": "TEXTSPLIT",
    "HOY": "TODAY", "AHORA": "NOW", "FECHA": "DATE", "AÑO": "YEAR", "MES": "MONTH", "DIA": "DAY", "DIAS": "DAYS",
    "DIAS.LAB": "NETWORKDAYS", "DIA.LAB": "WORKDAY", "FIN.MES": "EOMONTH", "FECHA.MES": "EDATE", "SIFECHA": "DATEDIF",
    "ELEGIRCOLS": "CHOOSECOLS", "ELEGIRFILAS": "CHOOSEROWS", "DIASEM": "WEEKDAY", "ESBLANCO": "ISBLANK", "ESNUMERO": "ISNUMBER", "ESERROR": "ISERROR", "LET": "LET", "LAMBDA": "LAMBDA",
}
NUEVAS = {"XLOOKUP", "XMATCH", "UNIQUE", "SORTBY", "SEQUENCE", "TEXTJOIN", "CONCAT", "IFS", "MAXIFS", "MINIFS",
          "TEXTBEFORE", "TEXTAFTER", "TEXTSPLIT", "LET", "LAMBDA", "IFNA", "DAYS", "CHOOSECOLS", "CHOOSEROWS"}
XLWS = {"FILTER", "SORT"}  # Excel las guarda como _xlfn._xlws.FILTER / _xlfn._xlws.SORT
FECHA = re.compile(r"(\d{2})/(\d{2})/(\d{4})")


def traducir(formula):
    """=SI(C2>15000;C2*8%;C2*5%) -> =IF(C2>15000,C2*8%,C2*5%) respetando el texto entre comillas."""
    partes = re.split(r'("[^"]*")', formula)
    for i in range(0, len(partes), 2):
        p = partes[i]
        for es in sorted(FUNCIONES, key=len, reverse=True):
            p = re.sub(r"(?<![A-Z.])" + re.escape(es) + r"\(", FUNCIONES[es] + "(", p)
        p = re.sub(r"(?<![A-Z._])VERDADERO(?![A-Z(])", "TRUE", p)
        p = re.sub(r"(?<![A-Z._])FALSO(?![A-Z(])", "FALSE", p)
        p = re.sub(r"(\d),(\d)", r"\1.\2", p)  # decimales con coma
        p = p.replace(";", ",")
        for f in NUEVAS:  # las funciones nuevas llevan prefijo interno
            p = re.sub(r"(?<![A-Z._])" + f + r"\(", "_xlfn." + f + "(", p)
        for f in XLWS:
            p = re.sub(r"(?<![A-Z._])" + f + r"\(", "_xlfn._xlws." + f + "(", p)
        partes[i] = p
    return "".join(partes)


def valor_celda(v):
    """'$ 18.400' -> (18400, '"$" #,##0'); '8 %' -> (0.08, '0%'); fechas y texto quedan como texto."""
    if not isinstance(v, str):
        return v, None
    s = v.strip()
    if s.startswith("="):
        return traducir(s), None
    if FECHA.fullmatch(s):
        d, m, a = FECHA.fullmatch(s).groups()
        return datetime(int(a), int(m), int(d)), "dd/mm/yyyy"
    m = re.fullmatch(r"([$€])?\s?(-?[\d.]+(?:,\d+)?)\s?(%)?", s)
    if not m or not re.search(r"\d", s):
        return v, None
    num = float(m.group(2).replace(".", "").replace(",", "."))
    dec = len(m.group(2).split(",")[1]) if "," in m.group(2) else 0
    if m.group(3):
        return num / 100, "0" + ("." + "0" * dec if dec else "") + "%"
    if m.group(1):
        return num, f'"{m.group(1)}" #,##0' + ("." + "0" * dec if dec else "")
    return (int(num) if num.is_integer() else num), ("#,##0" if abs(num) >= 1000 and not dec else None)


def estado_final(escena):
    """Celdas finales de una escena excel: datos + fórmulas de escribir/insertar + valores de rellenar."""
    celdas, datos = {}, {}
    for r, fila in enumerate(escena["datos"].get("celdas", []), 1):
        for c, v in enumerate(fila, 1):
            if v not in (None, ""):
                datos[f"{get_column_letter(c)}{r}"] = v
    celdas.update(datos)
    esperados = {}
    for b in escena["beats"]:
        for a in [*([b["accion"]] if isinstance(b.get("accion"), dict) else b.get("accion") or []), *b.get("acciones", [])]:
            t = a.get("tipo")
            if t == "escribir":
                celdas[a["celda"]] = a["texto"]
            elif t == "insertar":
                celdas[a["celda"]] = a["formula"]
                if a.get("valor"):
                    esperados[a["celda"]] = a["valor"]
            elif t == "calcular":
                esperados[a["celda"]] = a["valor"]
            elif t == "rellenar":
                col, r1 = re.match(r"([A-Z]+)(\d+)", a["rango"].split(":")[0]).groups()
                origen = celdas.get(f"{col}{r1}")
                for i, v in enumerate(a.get("valores", [])):
                    ref = f"{col}{int(r1) + i}"
                    if isinstance(origen, str) and origen.startswith("=") and i > 0:
                        celdas[ref] = re.sub(r"(?<![A-Z$!:])(\$?[A-Z]{1,2})" + r1 + r"(?!\d)", lambda m: m.group(1) + str(int(r1) + i), origen)
                    esperados[ref] = v
    escritas = {k: v for k, v in celdas.items() if k not in datos or v != datos[k]}
    return datos, escritas, esperados


DINAMICAS = ("_xlfn._xlws.FILTER", "_xlfn._xlws.SORT", "_xlfn.UNIQUE", "_xlfn.SORTBY", "_xlfn.SEQUENCE", "_xlfn.CHOOSECOLS",
             "_xlfn.CHOOSEROWS", "_xlfn.TEXTSPLIT", "_xlfn.VSTACK", "_xlfn.HSTACK")
METADATA = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<metadata xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
            'xmlns:xda="http://schemas.microsoft.com/office/spreadsheetml/2017/dynamicarray"><metadataTypes count="1"><metadataType name="XLDAPR" '
            'minSupportedVersion="120000" copy="1" pasteAll="1" pasteValues="1" merge="1" splitFirst="1" rowColShift="1" clearFormats="1" '
            'clearComments="1" assign="1" coerce="1" cellMeta="1"/></metadataTypes><futureMetadata name="XLDAPR" count="1"><bk><extLst>'
            '<ext uri="{bdbb8cdc-fa1e-496e-a857-3c3f30c029c3}"><xda:dynamicArrayProperties fDynamic="1" fCollapsed="0"/></ext></extLst></bk>'
            '</futureMetadata><cellMetadata count="1"><bk><rc t="1" v="0"/></bk></cellMetadata></metadata>')


def marcar_matrices_dinamicas(ruta):
    """openpyxl guarda FILTRAR/UNICOS como fórmulas comunes y Excel 365 las abre con @ (un solo valor, sin desbordar).
    Se reescribe el .xlsx: esas celdas pasan a fórmula de matriz dinámica (cm="1" + xl/metadata.xml), como las guarda Excel."""
    import zipfile
    tmp = ruta + ".tmp"
    hay = False
    with zipfile.ZipFile(ruta) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            datos = zin.read(item.filename)
            if item.filename.startswith("xl/worksheets/sheet") and item.filename.endswith(".xml"):
                xml = datos.decode("utf-8")

                def celda(m):
                    nonlocal hay
                    attrs, ref, formula = m.group(1), m.group(2), m.group(3)
                    if not any(f in formula for f in DINAMICAS) or "cm=" in attrs:
                        return m.group(0)
                    hay = True
                    return f'<c{attrs} cm="1"><f t="array" ref="{ref}">{formula}</f>'
                xml = re.sub(r'<c( r="([A-Z]+\d+)"[^>]*)><f>([^<]*)</f>', celda, xml)
                datos = xml.encode("utf-8")
            zout.writestr(item, datos)
        if hay:
            zout.writestr("xl/metadata.xml", METADATA)
    os.replace(tmp, ruta)
    if not hay:
        return
    with zipfile.ZipFile(ruta) as zin:
        partes = {i.filename: zin.read(i.filename) for i in zin.infolist()}
    tipos = partes["[Content_Types].xml"].decode()
    if "metadata.xml" not in tipos:
        tipos = tipos.replace("</Types>", '<Override PartName="/xl/metadata.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheetMetadata+xml"/></Types>')
    rels = partes["xl/_rels/workbook.xml.rels"].decode()
    if "sheetMetadata" not in rels:
        rels = rels.replace("</Relationships>", '<Relationship Id="rIdMeta1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/sheetMetadata" Target="metadata.xml"/></Relationships>')
    partes["[Content_Types].xml"], partes["xl/_rels/workbook.xml.rels"] = tipos.encode(), rels.encode()
    with zipfile.ZipFile(ruta, "w", zipfile.ZIP_DEFLATED) as zout:
        for nombre, datos in partes.items():
            zout.writestr(nombre, datos)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit(__doc__)
    base = os.path.join(RAIZ, "produccion", args[0])
    guion = json.load(open(os.path.join(base, "guion.json"), encoding="utf-8"))
    escenas = [e for e in guion["escenas"] if e["plantilla"] == "excel" and not e["datos"].get("solo_video")]
    if not escenas:
        sys.exit("El guion no tiene escenas de Excel.")
    hojas = {}
    for e in escenas:  # la última escena de cada hoja manda, pero acumula lo escrito antes
        nombre = e["datos"].get("hoja", "Hoja1")
        datos, escritas, esperados = estado_final(e)
        previo = hojas.setdefault(nombre, {"celdas": {}, "esperados": {}, "anchos": e["datos"].get("anchos"), "archivo": e["datos"].get("archivo")})
        for ref, v in datos.items():  # los datos de la escena no pisan una fórmula escrita antes
            ant = previo["celdas"].get(ref)
            desborde = ref in previo["esperados"] and ant is None  # resultado de una matriz dinámica (FILTRAR, UNICOS…)
            if not (isinstance(ant, str) and ant.startswith("=")) and not desborde:
                previo["celdas"][ref] = v
        previo["celdas"].update(escritas)
        previo["esperados"].update(esperados)
    archivo = next(h["archivo"] for h in hojas.values() if h["archivo"]) or f"{args[0]}.xlsx"
    wb = Workbook()
    wb.remove(wb.active)
    verde = PatternFill("solid", fgColor="107C41")
    for nombre, h in hojas.items():
        ws = wb.create_sheet(nombre[:31])
        for ref, v in h["celdas"].items():
            val, fmt = valor_celda(v)
            ws[ref] = val
            if fmt:
                ws[ref].number_format = fmt
            if not fmt and isinstance(h["esperados"].get(ref), str) and FECHA.fullmatch(h["esperados"][ref].strip()):
                ws[ref].number_format = "dd/mm/yyyy"
            if ref.endswith("1") and re.fullmatch(r"[A-Z]+1", ref):
                ws[ref].font = Font(bold=True, color="FFFFFF")
                ws[ref].fill = verde
                ws[ref].alignment = Alignment(horizontal="center")
        for ref, esp in h["esperados"].items():  # celdas de desborde con fechas
            if ref not in h["celdas"] and isinstance(esp, str) and FECHA.fullmatch(esp.strip()):
                ws[ref].number_format = "dd/mm/yyyy"
        for i, w in enumerate(h["anchos"] or [], 1):
            ws.column_dimensions[get_column_letter(i)].width = max(10, w / 8)
        ws.freeze_panes = "A2"
    ws = wb.create_sheet("Léeme", 0)
    ws["A1"] = guion.get("titulo", "")
    ws["A1"].font = Font(bold=True, size=14)
    ws["A3"] = "Plantilla de Atajos IA (youtube.com/@AtajosIAoficial). Los datos son ficticios: reemplázalos por los tuyos."
    ws["A4"] = "Las fórmulas funcionan en Excel para la web (gratis) y en Excel 2021/365. No tiene macros ni vínculos externos."
    ws.column_dimensions["A"].width = 110
    destino = os.path.join(base, "plantilla")
    os.makedirs(destino, exist_ok=True)
    ruta = os.path.join(destino, archivo)
    wb.save(ruta)
    marcar_matrices_dinamicas(ruta)
    print(f"✔ {os.path.relpath(ruta, RAIZ)} · hojas: {', '.join(hojas)}")

    if "--verificar" in sys.argv:
        soffice = shutil.which("soffice") or shutil.which("libreoffice")
        if not soffice:
            sys.exit("⚠ No hay LibreOffice para recalcular: verifica los valores a mano o instala libreoffice-calc.")
        tmp = os.path.join(base, "build", "recalculo")
        os.makedirs(tmp, exist_ok=True)
        subprocess.run([soffice, "--headless", "--convert-to", "xlsx", "--outdir", tmp, ruta], check=True, capture_output=True)
        calc = load_workbook(os.path.join(tmp, archivo), data_only=True)
        errores = 0
        for nombre, h in hojas.items():
            ws = calc[nombre[:31]]
            for ref, esperado in h["esperados"].items():
                real = ws[ref].value
                num, _ = valor_celda(esperado)
                if isinstance(num, datetime):  # fecha: LibreOffice la devuelve como fecha o como número de serie
                    if isinstance(real, datetime):
                        real = real.date() == num.date() and esperado or real
                    elif isinstance(real, (int, float)):
                        num = (num - datetime(1899, 12, 30)).days
                ok = (isinstance(num, (int, float)) and isinstance(real, (int, float)) and abs(real - num) <= max(0.01, abs(num) * 0.001)) or str(real) == str(esperado)
                if not ok:
                    errores += 1
                    print(f"  ✗ {nombre}!{ref}: el video muestra «{esperado}» y la fórmula da «{real}»")
        print("✔ Todos los valores del video coinciden con las fórmulas" if not errores else f"✗ {errores} valores no coinciden")
        sys.exit(1 if errores else 0)


if __name__ == "__main__":
    main()
