"""Mapa de costo contra movimiento a partir de los ticks grabados.

Responde la pregunta de la Etapa 0: para cada plazo de operación (5 s, 15 s,
30 s, ...) y cada hora del día, ¿cuánto cuesta entrar y salir comparado con
cuánto se mueve el precio?

    CVR(h) = costo de ida y vuelta / desvío estándar del movimiento del mid en h

Uso:
    python -m research.ticks.analizar_costos --raiz "<...>/Common/Files/ATS" \
        --simbolo XAUUSDc --salida reporte_costos.md

El costo incluye el spread observado en la entrada y en la salida. El slippage
y la comisión NO se pueden observar en los ticks: se pasan como supuestos
(--slippage, --comision) y el reporte lo aclara. Se reemplazan por valores
medidos cuando haya ejecución real.
"""
import argparse
import csv
from pathlib import Path

import numpy as np

from research.ticks.formato import leer_simbolo

HORIZONTES_DEFAULT = (5, 15, 30, 60, 120, 300)


def limpiar(ticks):
    """Descarta ticks imposibles (precios no positivos o ask < bid)."""
    ok = (ticks["bid"] > 0) & (ticks["ask"] > 0) & (ticks["ask"] >= ticks["bid"])
    return ticks[ok], int((~ok).sum())


def grilla(ticks, paso_ms=1000, max_edad_ms=30_000):
    """Muestrea el último precio conocido cada `paso_ms`.

    Un punto es válido si el último tick tiene menos de `max_edad_ms` de
    antigüedad (fuera de eso el mercado está cerrado o el feed se cortó).
    """
    t_ticks = ticks["time_msc"]
    inicio = (t_ticks[0] // paso_ms + 1) * paso_ms
    t = np.arange(inicio, t_ticks[-1] + 1, paso_ms, dtype=np.int64)
    idx = np.searchsorted(t_ticks, t, side="right") - 1
    valido = (idx >= 0) & ((t - t_ticks[np.clip(idx, 0, None)]) <= max_edad_ms)
    idx = np.clip(idx, 0, None)
    bid = ticks["bid"][idx]
    ask = ticks["ask"][idx]
    return {
        "t": t,
        "mid": (bid + ask) / 2.0,
        "spread": ask - bid,
        "valido": valido,
        "paso_ms": paso_ms,
    }


def hora_del_dia(t_ms):
    return (t_ms // 1000 % 86400) // 3600


def _metricas(dm, costo):
    if len(dm) < 30:
        return None
    sigma = float(np.std(dm))
    c = float(np.mean(costo))
    return {
        "n": int(len(dm)),
        "sigma": sigma,
        "mov_abs_medio": float(np.mean(np.abs(dm))),
        "costo": c,
        "cvr": c / sigma if sigma > 0 else float("inf"),
        "p_empate": (sigma + c) / (2 * sigma) if sigma > 0 else float("inf"),
    }


def costo_vs_movimiento(g, horizontes, slippage_por_lado=0.0, comision_rt=0.0):
    """Devuelve {h: {"total": métricas, "por_hora": {hora: métricas}}}."""
    paso_s = g["paso_ms"] / 1000.0
    horas = hora_del_dia(g["t"])
    resultado = {}
    for h in horizontes:
        k = int(round(h / paso_s))
        if k <= 0 or k >= len(g["t"]):
            continue
        ok = g["valido"][:-k] & g["valido"][k:]
        dm = (g["mid"][k:] - g["mid"][:-k])[ok]
        # Comprar al ask y vender al bid cuesta medio spread en cada punta.
        costo = ((g["spread"][:-k] + g["spread"][k:]) / 2.0)[ok]
        costo = costo + 2.0 * slippage_por_lado + comision_rt
        horas_ok = horas[:-k][ok]
        por_hora = {}
        for hora in range(24):
            sel = horas_ok == hora
            m = _metricas(dm[sel], costo[sel])
            if m:
                por_hora[hora] = m
        resultado[h] = {"total": _metricas(dm, costo), "por_hora": por_hora}
    return resultado


def spread_por_hora(g, ticks):
    """Percentiles del spread (ponderados por tiempo) y actividad por hora."""
    horas = hora_del_dia(g["t"])
    horas_ticks = hora_del_dia(ticks["time_msc"])
    salida = {}
    for hora in range(24):
        sel = g["valido"] & (horas == hora)
        if sel.sum() < 30:
            continue
        s = g["spread"][sel]
        segundos = sel.sum() * g["paso_ms"] / 1000.0
        salida[hora] = {
            "p50": float(np.percentile(s, 50)),
            "p90": float(np.percentile(s, 90)),
            "p99": float(np.percentile(s, 99)),
            "max": float(np.max(s)),
            "ticks_por_seg": float((horas_ticks == hora).sum() / segundos),
        }
    return salida


def leer_specs(raiz, simbolo):
    """Lee el archivo de especificaciones más reciente del símbolo, si existe."""
    archivos = sorted((Path(raiz) / "specs").glob(f"{simbolo}_*.csv"))
    if not archivos:
        return {}
    with open(archivos[-1], encoding="latin-1") as f:
        return {fila["key"]: fila["value"] for fila in csv.DictReader(f, delimiter=";")}


def _lectura_cvr(cvr):
    if cvr > 1:
        return "costo > movimiento: descartar"
    if cvr > 0.5:
        return "muy difícil"
    if cvr > 0.2:
        return "difícil, investigable"
    return "costo manejable"


def _pct(p):
    return "imposible" if p >= 1 else f"{p * 100:.1f} %"


def reporte(simbolo, ticks, descartados, g, resultado, spreads, specs,
            slippage_por_lado, comision_rt):
    dias = sorted({str(np.datetime64(int(t), "ms").astype("datetime64[D]")) for t in ticks["time_msc"][:: max(1, len(ticks) // 1000)]})
    horas_validas = g["valido"].sum() * g["paso_ms"] / 3_600_000
    lineas = [
        f"# Costo contra movimiento — {simbolo}",
        "",
        f"- Ticks: {len(ticks):,} (descartados por inválidos: {descartados})",
        f"- Período: {dias[0]} a {dias[-1]} · horas con mercado activo: {horas_validas:.1f}",
        "- Horas del día en **hora del servidor del broker**.",
        "- Costo = spread observado (medio en la entrada + medio en la salida)"
        f" + slippage supuesto {slippage_por_lado:g} por lado + comisión supuesta {comision_rt:g} ida y vuelta.",
        "- **El slippage y la comisión son supuestos hasta medir ejecución real.**",
        "",
    ]
    if specs:
        lineas += [
            f"Cuenta: {specs.get('account_company', '?')} · moneda {specs.get('account_currency', '?')} · "
            f"contrato {specs.get('contract_size', '?')} · volumen mínimo {specs.get('volume_min', '?')} · "
            f"stops level {specs.get('stops_level', '?')} puntos",
            "",
        ]

    lineas += [
        "## Resumen por plazo",
        "",
        "| Plazo | n | Movimiento típico (σ) | Costo medio | CVR | Aciertos para empatar con TP=SL=σ | Lectura |",
        "|---|---|---|---|---|---|---|",
    ]
    for h, r in resultado.items():
        m = r["total"]
        if not m:
            continue
        lineas.append(
            f"| {h} s | {m['n']:,} | {m['sigma']:.3f} | {m['costo']:.3f} | {m['cvr']:.2f} | "
            f"{_pct(m['p_empate'])} | {_lectura_cvr(m['cvr'])} |"
        )

    lineas += ["", "## CVR por hora del día", "",
               "| Hora | " + " | ".join(f"{h} s" for h in resultado) + " |",
               "|---|" + "---|" * len(resultado)]
    for hora in range(24):
        celdas = []
        for h, r in resultado.items():
            m = r["por_hora"].get(hora)
            celdas.append(f"{m['cvr']:.2f}" if m else "—")
        if any(c != "—" for c in celdas):
            lineas.append(f"| {hora:02d} | " + " | ".join(celdas) + " |")

    lineas += ["", "## Spread por hora del día (unidades de precio)", "",
               "| Hora | P50 | P90 | P99 | Máximo | Ticks/s |", "|---|---|---|---|---|---|"]
    for hora, s in spreads.items():
        lineas.append(
            f"| {hora:02d} | {s['p50']:.3f} | {s['p90']:.3f} | {s['p99']:.3f} | {s['max']:.3f} | {s['ticks_por_seg']:.1f} |"
        )

    lineas += [
        "",
        "## Cómo leerlo",
        "",
        "- **CVR > 1:** el costo supera el movimiento típico; operar en ese plazo exige aciertos irreales.",
        "- **0,5–1:** muy difícil. **0,2–0,5:** difícil pero investigable. **< 0,2:** el costo es manejable.",
        "- La columna de aciertos para empatar supone objetivo y stop iguales al movimiento típico del plazo.",
        "- Esto mide si hay *espacio* para una ventaja, no que exista: eso lo dice la investigación de estrategias.",
    ]
    return "\n".join(lineas) + "\n"


def valores_por_simbolo(texto, simbolos):
    """Interpreta "0.05" (vale para todos) o "XAUUSDc=0.05,BTCUSDc=5" (por símbolo)."""
    texto = (texto or "0").strip()
    if "=" not in texto:
        return {s: float(texto) for s in simbolos}
    valores = {s: 0.0 for s in simbolos}
    for parte in texto.split(","):
        if parte.strip():
            simbolo, valor = parte.split("=")
            valores[simbolo.strip()] = float(valor)
    return valores


def comparativo(analisis, horizontes, h_referencia=60):
    """Tabla con un renglón por activo. El CVR no tiene unidades: se compara entre activos."""
    lineas = [
        "# Comparación entre activos",
        "",
        "CVR = costo de ida y vuelta / movimiento típico en el plazo. Más bajo es mejor.",
        "",
        "| Activo | " + " | ".join(f"CVR {h} s" for h in horizontes)
        + f" | Mejor hora (CVR {h_referencia} s) | Spread P50 | Horas activas |",
        "|---|" + "---|" * (len(horizontes) + 3),
    ]
    for simbolo, a in analisis.items():
        celdas = []
        for h in horizontes:
            m = a["resultado"].get(h, {}).get("total")
            celdas.append(f"{m['cvr']:.2f}" if m else "—")
        por_hora = a["resultado"].get(h_referencia, {}).get("por_hora", {})
        if por_hora:
            hora, m = min(por_hora.items(), key=lambda kv: kv[1]["cvr"])
            mejor = f"{hora:02d} h ({m['cvr']:.2f})"
        else:
            mejor = "—"
        g = a["grilla"]
        spread_p50 = float(np.percentile(g["spread"][g["valido"]], 50))
        horas = g["valido"].sum() * g["paso_ms"] / 3_600_000
        lineas.append(f"| {simbolo} | " + " | ".join(celdas) + f" | {mejor} | {spread_p50:.3f} | {horas:.0f} |")
    lineas += [
        "",
        "- Las horas son del servidor del broker y mezclan todos los días; en cripto incluyen fines de semana.",
        "- Los índices (US30, US100, US500) se mueven casi juntos, igual que BTC y ETH: "
        "un buen CVR en los tres índices no son tres oportunidades independientes.",
        "",
    ]
    return "\n".join(lineas)


def analizar(raiz, simbolo, horizontes, slippage, comision, desde=None, hasta=None):
    ticks, descartados = limpiar(leer_simbolo(raiz, simbolo, desde, hasta))
    if len(ticks) < 100:
        raise ValueError(f"{simbolo}: hay muy pocos ticks válidos para analizar")
    g = grilla(ticks)
    resultado = costo_vs_movimiento(g, horizontes, slippage, comision)
    texto = reporte(simbolo, ticks, descartados, g, resultado, spread_por_hora(g, ticks),
                    leer_specs(raiz, simbolo), slippage, comision)
    return {"grilla": g, "resultado": resultado, "texto": texto}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--raiz", required=True, help="carpeta ATS dentro de Common\\Files")
    p.add_argument("--simbolo", required=True, help="uno o varios separados por coma")
    p.add_argument("--desde", help="AAAAMMDD")
    p.add_argument("--hasta", help="AAAAMMDD")
    p.add_argument("--horizontes", default=",".join(map(str, HORIZONTES_DEFAULT)),
                   help="plazos en segundos separados por coma")
    p.add_argument("--slippage", default="0",
                   help="slippage supuesto por lado en unidades de precio: un valor, o SIMBOLO=valor,...")
    p.add_argument("--comision", default="0",
                   help="comisión supuesta ida y vuelta en unidades de precio: un valor, o SIMBOLO=valor,...")
    p.add_argument("--salida", default="reporte_costos.md")
    a = p.parse_args(argv)

    simbolos = [s.strip() for s in a.simbolo.split(",") if s.strip()]
    horizontes = [int(x) for x in a.horizontes.split(",") if x.strip()]
    slippage = valores_por_simbolo(a.slippage, simbolos)
    comision = valores_por_simbolo(a.comision, simbolos)

    analisis, faltantes = {}, []
    for simbolo in simbolos:
        try:
            analisis[simbolo] = analizar(a.raiz, simbolo, horizontes, slippage[simbolo],
                                         comision[simbolo], a.desde, a.hasta)
        except (FileNotFoundError, ValueError) as e:
            faltantes.append(f"- {simbolo}: {e}")
    if not analisis:
        raise SystemExit("No hay datos para ningún símbolo:\n" + "\n".join(faltantes))

    partes = []
    if len(simbolos) > 1:
        partes.append(comparativo(analisis, horizontes))
        if faltantes:
            partes.append("Sin datos:\n" + "\n".join(faltantes) + "\n")
    partes += [a_["texto"] for a_ in analisis.values()]
    texto = "\n---\n\n".join(partes)
    Path(a.salida).write_text(texto, encoding="utf-8")
    print(texto)


if __name__ == "__main__":
    main()
