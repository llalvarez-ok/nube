"""Indicadores (features) calculados a partir de ticks.

Todas las features son causales: en el tick i solo usan ticks con hora <= la
del tick i. Cada definición está escrita dos veces:

- `calcular`: versión vectorizada (rápida), la que usa la investigación.
- `calcular_referencia`: versión tick a tick, lenta y literal, que sirve de
  especificación. Los tests verifican que ambas den lo mismo, y el código MQL5
  del motor en vivo se va a verificar contra la misma referencia.

Si se cambia una definición, hay que cambiarla en las dos funciones.
"""
import numpy as np
import pandas as pd

VENTANAS_RETORNO_S = (1, 5, 30, 120)
VENTANAS_RANGO_S = (30, 120)
VENTANAS_ACTIVIDAD_S = (5, 60)
VENTANA_EFICIENCIA_S = 30
VENTANA_SPREAD_S = 600

COLUMNAS = (
    ["time_msc", "mid", "spread", "dt_prev_ms", "hora"]
    + [f"ret_{w}s" for w in VENTANAS_RETORNO_S]
    + [f"rango_{w}s" for w in VENTANAS_RANGO_S]
    + [f"ticks_por_s_{w}s" for w in VENTANAS_ACTIVIDAD_S]
    + [f"eficiencia_{VENTANA_EFICIENCIA_S}s", f"desequilibrio_{VENTANA_EFICIENCIA_S}s", "spread_rel"]
)


def calcular(ticks):
    """Devuelve un DataFrame con una fila por tick y las columnas de COLUMNAS.

    Definiciones (ventana de w segundos = ticks con hora en (T - w, T]):
    - ret_ws: mid actual menos el mid del último tick con hora <= T - w (NaN si no hay).
    - rango_ws: máximo menos mínimo del mid en la ventana.
    - ticks_por_s_ws: cantidad de ticks en la ventana / w.
    - eficiencia_30s: |ret_30s| / suma de |cambios del mid| en la ventana (0 a 1; NaN si no hubo movimiento).
    - desequilibrio_30s: (subas - bajas) / (subas + bajas) del mid en la ventana (NaN si no hubo cambios).
    - spread_rel: spread / promedio del spread en los últimos 600 s.
    - dt_prev_ms: ms desde el tick anterior (NaN en el primero).
    - hora: hora del día (hora del servidor) del tick.
    """
    t = np.asarray(ticks["time_msc"], dtype=np.int64)
    mid = (np.asarray(ticks["bid"], dtype=float) + np.asarray(ticks["ask"], dtype=float)) / 2.0
    spread = np.asarray(ticks["ask"], dtype=float) - np.asarray(ticks["bid"], dtype=float)
    n = len(t)

    salida = {"time_msc": t, "mid": mid, "spread": spread}
    dt_prev = np.full(n, np.nan)
    dt_prev[1:] = np.diff(t)
    salida["dt_prev_ms"] = dt_prev
    salida["hora"] = (t // 1000 % 86400) // 3600

    for w in VENTANAS_RETORNO_S:
        idx = np.searchsorted(t, t - w * 1000, side="right") - 1
        r = np.full(n, np.nan)
        ok = idx >= 0
        r[ok] = mid[ok] - mid[idx[ok]]
        salida[f"ret_{w}s"] = r

    indice = pd.to_datetime(t, unit="ms")
    s_mid = pd.Series(mid, index=indice)
    for w in VENTANAS_RANGO_S:
        ventana = s_mid.rolling(f"{w}s")
        salida[f"rango_{w}s"] = (ventana.max() - ventana.min()).to_numpy()
    for w in VENTANAS_ACTIVIDAD_S:
        salida[f"ticks_por_s_{w}s"] = s_mid.rolling(f"{w}s").count().to_numpy() / w

    delta = np.zeros(n)
    delta[1:] = np.diff(mid)
    w = VENTANA_EFICIENCIA_S
    camino = pd.Series(np.abs(delta), index=indice).rolling(f"{w}s").sum().to_numpy()
    signo = np.sign(delta)
    neto = pd.Series(signo, index=indice).rolling(f"{w}s").sum().to_numpy()
    cambios = pd.Series(np.abs(signo), index=indice).rolling(f"{w}s").sum().to_numpy()
    with np.errstate(invalid="ignore", divide="ignore"):
        efic = np.abs(salida[f"ret_{w}s"]) / camino
        deseq = neto / cambios
    efic[~(camino > 1e-12)] = np.nan
    deseq[~(cambios > 0.5)] = np.nan
    salida[f"eficiencia_{w}s"] = np.clip(efic, 0.0, 1.0)
    salida[f"desequilibrio_{w}s"] = deseq

    media_spread = pd.Series(spread, index=indice).rolling(f"{VENTANA_SPREAD_S}s").mean().to_numpy()
    with np.errstate(invalid="ignore", divide="ignore"):
        rel = spread / media_spread
    rel[~(media_spread > 0)] = np.nan
    salida["spread_rel"] = rel

    return pd.DataFrame(salida, columns=COLUMNAS)


def calcular_referencia(ticks):
    """Misma definición que `calcular`, tick a tick y sin atajos. Solo para tests."""
    t = [int(x) for x in ticks["time_msc"]]
    mid = [(float(b) + float(a)) / 2.0 for b, a in zip(ticks["bid"], ticks["ask"])]
    spread = [float(a) - float(b) for b, a in zip(ticks["bid"], ticks["ask"])]
    filas = []
    for i in range(len(t)):
        T = t[i]
        f = {"time_msc": T, "mid": mid[i], "spread": spread[i],
             "dt_prev_ms": float(T - t[i - 1]) if i > 0 else float("nan"),
             "hora": (T // 1000 % 86400) // 3600}

        def en_ventana(w):
            return [j for j in range(i + 1) if t[j] > T - w * 1000]

        for w in VENTANAS_RETORNO_S:
            previos = [j for j in range(i + 1) if t[j] <= T - w * 1000]
            f[f"ret_{w}s"] = mid[i] - mid[previos[-1]] if previos else float("nan")
        for w in VENTANAS_RANGO_S:
            v = [mid[j] for j in en_ventana(w)]
            f[f"rango_{w}s"] = max(v) - min(v)
        for w in VENTANAS_ACTIVIDAD_S:
            f[f"ticks_por_s_{w}s"] = len(en_ventana(w)) / w

        w = VENTANA_EFICIENCIA_S
        js = en_ventana(w)
        deltas = [mid[j] - mid[j - 1] if j > 0 else 0.0 for j in js]
        camino = sum(abs(d) for d in deltas)
        subas = sum(1 for d in deltas if d > 0)
        bajas = sum(1 for d in deltas if d < 0)
        ret = f[f"ret_{w}s"]
        f[f"eficiencia_{w}s"] = (min(1.0, abs(ret) / camino)
                                 if camino > 1e-12 and ret == ret else float("nan"))
        f[f"desequilibrio_{w}s"] = (subas - bajas) / (subas + bajas) if subas + bajas else float("nan")

        sp = [spread[j] for j in en_ventana(VENTANA_SPREAD_S)]
        media = sum(sp) / len(sp)
        f["spread_rel"] = spread[i] / media if media > 0 else float("nan")
        filas.append(f)
    return pd.DataFrame(filas, columns=COLUMNAS)
