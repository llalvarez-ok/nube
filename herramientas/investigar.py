#!/usr/bin/env python3
"""Investigación de mercado con datos reales de YouTube (gratis).

    python3 herramientas/investigar.py sugerencias "ia para"            # demanda: autocompletado de YouTube
    python3 herramientas/investigar.py outliers "resumir pdf con ia" --region MX --dias 180
    python3 herramientas/investigar.py nicho "ia para excel" "ia para contadores" --region MX
    python3 herramientas/investigar.py populares --region MX --categoria 27

Autenticación: usa YT_API_KEY si existe; si no, el OAuth del canal (YT_CLIENT_ID,
YT_CLIENT_SECRET, YT_REFRESH_TOKEN). Cuota diaria gratis: 10.000 unidades. Cada
"outliers" gasta ~102 (una búsqueda = 100), así que "nicho" admite hasta ~8 consultas.

Outlier = vistas / suscriptores del canal. Un video con 10x o más en un canal chico
prueba que el TEMA tiene demanda, no el canal: es la señal que usan los métodos tipo
IATube para elegir qué producir. Agrega --json para que lo lean los agentes.
"""

import datetime
import json
import os
import statistics
import sys
import urllib.error
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(__file__))
DATA = "https://www.googleapis.com/youtube/v3/"
CATEGORIAS = {"27": "Educación", "28": "Ciencia y tecnología", "22": "Personas y blogs", "26": "Instructivos y estilo"}


class Cliente:
    def __init__(self):
        self.clave = os.environ.get("YT_API_KEY")
        self.token = None
        if not self.clave:
            from yt import token_de_acceso
            self.token = token_de_acceso()

    def get(self, recurso, params):
        if self.clave:
            params = {**params, "key": self.clave}
        req = urllib.request.Request(DATA + recurso + "?" + urllib.parse.urlencode(params))
        if self.token:
            req.add_header("Authorization", f"Bearer {self.token}")
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            cuerpo = e.read().decode()[:300]
            if "quotaExceeded" in cuerpo:
                sys.exit("Cuota diaria de la API agotada (se renueva a medianoche, hora del Pacífico).")
            sys.exit(f"Error {e.code} en {recurso}: {cuerpo}")


def sugerencias(semilla, idioma="es"):
    """Autocompletado de YouTube para la semilla y la semilla + cada letra: lo que la gente escribe."""
    vistas, salida = set(), []
    for sufijo in [""] + [f" {c}" for c in "abcdefghijlmnopqrstuvz"]:
        q = urllib.parse.quote(semilla + sufijo)
        url = f"https://suggestqueries.google.com/complete/search?client=firefox&ds=yt&hl={idioma}&q={q}"
        try:
            with urllib.request.urlopen(url, timeout=15) as r:
                datos = json.loads(r.read().decode("utf-8", "replace"))
        except (urllib.error.URLError, ValueError) as e:
            sys.exit(f"No se pudo consultar el autocompletado: {e}")
        for s in datos[1]:
            if s not in vistas:
                vistas.add(s)
                salida.append(s)
    return salida


def outliers(cli, consulta, region="MX", dias=180, idioma="es", maximo=25):
    desde = (datetime.datetime.utcnow() - datetime.timedelta(days=dias)).strftime("%Y-%m-%dT%H:%M:%SZ")
    busq = cli.get("search", {"part": "snippet", "q": consulta, "type": "video", "order": "viewCount",
                              "regionCode": region, "relevanceLanguage": idioma, "publishedAfter": desde,
                              "maxResults": maximo})
    ids = [i["id"]["videoId"] for i in busq.get("items", [])]
    if not ids:
        return []
    vids = cli.get("videos", {"part": "snippet,statistics,contentDetails", "id": ",".join(ids)})["items"]
    canales = {c["id"]: c for c in cli.get("channels", {"part": "statistics,snippet",
                                                         "id": ",".join({v["snippet"]["channelId"] for v in vids})})["items"]}
    hoy = datetime.datetime.utcnow()
    filas = []
    for v in vids:
        c = canales.get(v["snippet"]["channelId"], {})
        subs = int(c.get("statistics", {}).get("subscriberCount", 0) or 0)
        vistas = int(v["statistics"].get("viewCount", 0))
        edad = max(1, (hoy - datetime.datetime.strptime(v["snippet"]["publishedAt"][:19], "%Y-%m-%dT%H:%M:%S")).days)
        filas.append({
            "titulo": v["snippet"]["title"], "canal": v["snippet"]["channelTitle"], "id": v["id"],
            "vistas": vistas, "suscriptores": subs, "dias": edad,
            "vistas_por_dia": round(vistas / edad), "outlier": round(vistas / max(subs, 1000), 1),
            "duracion": v["contentDetails"]["duration"],
            "comentarios": int(v["statistics"].get("commentCount", 0) or 0),
        })
    return sorted(filas, key=lambda f: -f["outlier"])


def resumen_nicho(filas):
    """Puntaje de oportunidad 0-100: demanda reciente + canales chicos que la capturan."""
    if not filas:
        return {"oportunidad": 0, "nota": "sin resultados"}
    vistas = [f["vistas"] for f in filas]
    chicos = [f for f in filas if f["suscriptores"] < 50_000 and f["vistas"] > 20_000]
    outl = [f for f in filas if f["outlier"] >= 3]
    vpd = statistics.median(f["vistas_por_dia"] for f in filas)
    demanda = min(40, vpd / 25)                    # 1.000 vistas/día mediana = 40 puntos
    hueco = min(35, len(chicos) * 7)               # canales chicos con éxito = hay lugar
    senal = min(25, len(outl) * 5)                 # videos outlier = tema caliente
    return {"oportunidad": round(demanda + hueco + senal), "mediana_vistas": int(statistics.median(vistas)),
            "mediana_vistas_por_dia": int(vpd), "canales_chicos_con_exito": len(chicos), "outliers_3x": len(outl)}


def populares(cli, region="MX", categoria=None):
    params = {"part": "snippet,statistics", "chart": "mostPopular", "regionCode": region, "maxResults": 50}
    if categoria:
        params["videoCategoryId"] = categoria
    return [{"titulo": v["snippet"]["title"], "canal": v["snippet"]["channelTitle"],
             "vistas": int(v["statistics"].get("viewCount", 0)), "id": v["id"]}
            for v in cli.get("videos", params).get("items", [])]


def opcion(nombre, defecto):
    if nombre in sys.argv:
        return sys.argv[sys.argv.index(nombre) + 1]
    return defecto


def posicionales(argv, con_valor):
    """Argumentos que no son opciones ni valores de opciones."""
    salida, saltar = [], False
    for a in argv:
        if saltar:
            saltar = False
        elif a in con_valor:
            saltar = True
        elif not a.startswith("--"):
            salida.append(a)
    return salida


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    cmd = sys.argv[1]
    args = posicionales(sys.argv[2:], {"--region", "--dias", "--categoria", "--idioma"})
    como_json = "--json" in sys.argv
    region, dias, idioma = opcion("--region", "MX"), int(opcion("--dias", 180)), opcion("--idioma", "es")

    if cmd == "sugerencias":
        res = {a: sugerencias(a, idioma) for a in args}
        if como_json:
            print(json.dumps(res, ensure_ascii=False, indent=2))
        else:
            for semilla, lista in res.items():
                print(f"\n## {semilla} ({len(lista)} búsquedas)")
                print("\n".join(f"- {s}" for s in lista))
        return

    cli = Cliente()
    if cmd == "outliers":
        filas = outliers(cli, " ".join(args), region, dias, idioma)
        if como_json:
            print(json.dumps(filas, ensure_ascii=False, indent=2))
            return
        print(f"| Outlier | Vistas | Vistas/día | Subs | Días | Título | Canal |\n|---|---|---|---|---|---|---|")
        for f in filas:
            print(f"| {f['outlier']}x | {f['vistas']:,} | {f['vistas_por_dia']:,} | {f['suscriptores']:,} | {f['dias']} | "
                  f"[{f['titulo'][:60]}](https://youtu.be/{f['id']}) | {f['canal']} |")
    elif cmd == "nicho":
        res = {}
        for consulta in args:
            filas = outliers(cli, consulta, region, dias, idioma)
            res[consulta] = {**resumen_nicho(filas), "top": filas[:3]}
        if como_json:
            print(json.dumps(res, ensure_ascii=False, indent=2))
            return
        print(f"Región {region} · últimos {dias} días\n")
        print("| Consulta | Oportunidad | Mediana vistas | Vistas/día | Canales chicos con éxito | Outliers 3x+ |\n|---|---|---|---|---|---|")
        for q, r in sorted(res.items(), key=lambda x: -x[1]["oportunidad"]):
            print(f"| {q} | **{r['oportunidad']}** | {r.get('mediana_vistas', 0):,} | {r.get('mediana_vistas_por_dia', 0):,} | "
                  f"{r.get('canales_chicos_con_exito', 0)} | {r.get('outliers_3x', 0)} |")
    elif cmd == "populares":
        filas = populares(cli, region, opcion("--categoria", None))
        if como_json:
            print(json.dumps(filas, ensure_ascii=False, indent=2))
            return
        for f in filas:
            print(f"{f['vistas']:>12,}  {f['titulo'][:80]}  · {f['canal']}")
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
