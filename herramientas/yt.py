#!/usr/bin/env python3
"""Cliente mínimo de la API de YouTube para Atajo IA (solo librería estándar).

Lee YT_CLIENT_ID, YT_CLIENT_SECRET y YT_REFRESH_TOKEN del entorno.

    python herramientas/yt.py canal          # datos y estadísticas del canal
    python herramientas/yt.py videos         # últimos videos con estadísticas
    python herramientas/yt.py analitica 28   # métricas de los últimos N días (por video)
"""

import datetime
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

DATA = "https://www.googleapis.com/youtube/v3/"
ANALYTICS = "https://youtubeanalytics.googleapis.com/v2/reports"


def token_de_acceso():
    faltan = [v for v in ("YT_CLIENT_ID", "YT_CLIENT_SECRET", "YT_REFRESH_TOKEN") if not os.environ.get(v)]
    if faltan:
        sys.exit(f"Faltan variables de entorno: {', '.join(faltan)}")
    cuerpo = urllib.parse.urlencode({
        "client_id": os.environ["YT_CLIENT_ID"],
        "client_secret": os.environ["YT_CLIENT_SECRET"],
        "refresh_token": os.environ["YT_REFRESH_TOKEN"],
        "grant_type": "refresh_token",
    }).encode()
    try:
        with urllib.request.urlopen(urllib.request.Request("https://oauth2.googleapis.com/token", data=cuerpo)) as r:
            return json.load(r)["access_token"]
    except urllib.error.HTTPError as e:
        sys.exit(f"No se pudo renovar el token ({e.code}): {e.read().decode()}")


def get(url, params, token):
    req = urllib.request.Request(url + "?" + urllib.parse.urlencode(params), headers={"Authorization": f"Bearer {token}"})
    try:
        with urllib.request.urlopen(req) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"Error {e.code} en {url}: {e.read().decode()}")


def canal(token):
    return get(DATA + "channels", {"part": "snippet,statistics,contentDetails,status", "mine": "true"}, token)


def videos(token, maximo=25):
    uploads = canal(token)["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    lista = get(DATA + "playlistItems", {"part": "contentDetails", "playlistId": uploads, "maxResults": maximo}, token)
    ids = [i["contentDetails"]["videoId"] for i in lista.get("items", [])]
    if not ids:
        return {"items": []}
    return get(DATA + "videos", {"part": "snippet,statistics,contentDetails,status", "id": ",".join(ids)}, token)


def analitica(token, dias=28):
    fin = datetime.date.today()
    inicio = fin - datetime.timedelta(days=dias)
    return get(ANALYTICS, {
        "ids": "channel==MINE",
        "startDate": inicio.isoformat(),
        "endDate": fin.isoformat(),
        "dimensions": "video",
        "metrics": "views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,subscribersGained,likes,comments",
        "sort": "-views",
        "maxResults": 50,
    }, token)


def main():
    comando = sys.argv[1] if len(sys.argv) > 1 else "canal"
    token = token_de_acceso()
    if comando == "canal":
        resultado = canal(token)
    elif comando == "videos":
        resultado = videos(token)
    elif comando == "analitica":
        resultado = analitica(token, int(sys.argv[2]) if len(sys.argv) > 2 else 28)
    else:
        sys.exit(__doc__)
    print(json.dumps(resultado, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
