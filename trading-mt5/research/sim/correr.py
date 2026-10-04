"""Corre una estrategia sobre ticks grabados y la compara con entradas al azar.

Uso:
    python -m research.sim.correr --raiz <carpeta ATS> --simbolo XAUUSDc \
        --estrategia momentum --params '{"umbral_rango": 0.5}' --salida reporte_sim.md

La línea base usa las mismas salidas, el mismo horario y una frecuencia de
entrada parecida, con dirección y momento al azar. Se corre con varias
semillas: si la estrategia no queda claramente por encima de la mayoría, su
señal no aporta nada.

La latencia y el slippage son SUPUESTOS hasta medir ejecución real. Con
`--latencia-ms status` se usan los pings grabados por el servicio (es un
mínimo optimista: el broker suma su propio tiempo de proceso).
"""
import argparse
import csv
import json
from pathlib import Path

import numpy as np

from research.estrategias import aleatoria, momentum
from research.features.motor import calcular
from research.sim.metricas import resumen, tabla
from research.sim.simulador import ConfigCuenta, ConfigEjecucion, ConfigNoOperar, simular
from research.ticks.analizar_costos import leer_specs, limpiar
from research.ticks.formato import leer_simbolo

ESTRATEGIAS = {"momentum": momentum.senales, "aleatoria": aleatoria.senales}


def pings_grabados(raiz, simbolo):
    """Pings (ms) que registró el servicio para ese símbolo, si los hay."""
    valores = []
    for archivo in sorted((Path(raiz) / "status").glob("*.csv")):
        with open(archivo, encoding="latin-1") as f:
            for fila in csv.DictReader(f, delimiter=";"):
                if fila.get("symbol") == simbolo and fila.get("connected") == "1":
                    ping = float(fila.get("ping_us") or 0) / 1000.0
                    if ping > 0:
                        valores.append(ping)
    return tuple(valores)


def cuenta_desde_specs(specs, capital, riesgo, lotes_fijos):
    cuenta = ConfigCuenta(capital_inicial=capital, riesgo_por_operacion=riesgo, lotes_fijos=lotes_fijos)
    try:
        tick_value = float(specs["tick_value"])
        tick_size = float(specs["tick_size"])
        if tick_value > 0 and tick_size > 0:
            cuenta.valor_por_precio = tick_value / tick_size
        cuenta.volumen_min = float(specs["volume_min"])
        cuenta.volumen_max = float(specs["volume_max"])
        cuenta.volumen_paso = float(specs["volume_step"])
    except (KeyError, ValueError):
        pass
    return cuenta


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--raiz", required=True)
    p.add_argument("--simbolo", required=True)
    p.add_argument("--desde")
    p.add_argument("--hasta")
    p.add_argument("--estrategia", choices=sorted(ESTRATEGIAS), default="momentum")
    p.add_argument("--params", default="{}", help="parámetros de la estrategia en JSON")
    p.add_argument("--latencia-ms", default="200", help='valor fijo en ms, o "status" para usar los pings grabados')
    p.add_argument("--slippage", type=float, default=0.0, help="slippage supuesto por lado (unidades de precio)")
    p.add_argument("--comision", type=float, default=0.0, help="comisión por lote ida y vuelta (moneda de la cuenta)")
    p.add_argument("--capital", type=float, default=1000.0)
    p.add_argument("--riesgo", type=float, default=0.005)
    p.add_argument("--lotes-fijos", type=float)
    p.add_argument("--semillas-base", type=int, default=10)
    p.add_argument("--salida", default="reporte_sim.md")
    p.add_argument("--operaciones-csv", help="si se indica, guarda ahí las operaciones de la estrategia")
    a = p.parse_args(argv)

    ticks, _ = limpiar(leer_simbolo(a.raiz, a.simbolo, a.desde, a.hasta))
    features = calcular(ticks)
    specs = leer_specs(a.raiz, a.simbolo)
    cuenta = cuenta_desde_specs(specs, a.capital, a.riesgo, a.lotes_fijos)
    if a.latencia_ms == "status":
        latencias = pings_grabados(a.raiz, a.simbolo)
        if not latencias:
            raise SystemExit("No hay pings grabados para ese símbolo.")
    else:
        latencias = (float(a.latencia_ms),)
    stops_level = float(specs.get("stops_level", 0) or 0) * float(specs.get("point", 0) or 0)

    def ejecucion(semilla):
        return ConfigEjecucion(latencia_ms=latencias, slippage=(a.slippage,), comision_por_lote_rt=a.comision,
                               stops_level=stops_level, semilla=semilla)

    params = json.loads(a.params)
    sen = ESTRATEGIAS[a.estrategia](features, **params)
    res = simular(ticks, features, sen, a.simbolo, ejecucion(0), cuenta, ConfigNoOperar())
    m = resumen(res.operaciones, cuenta.capital_inicial)

    segundos = max(1, len(np.unique(features["time_msc"].to_numpy() // 1000)))
    prob = sen.cantidad() / segundos
    salida_params = {k: params[k] for k in ("stop_rango", "objetivo_r", "max_hold_s") if k in params}
    bases = []
    for semilla in range(a.semillas_base):
        sb = aleatoria.senales(features, prob_por_segundo=prob, semilla=semilla, **salida_params)
        rb = simular(ticks, features, sb, a.simbolo, ejecucion(semilla), cuenta, ConfigNoOperar())
        bases.append(resumen(rb.operaciones, cuenta.capital_inicial))
    exp_bases = [b["expectativa_R"] for b in bases if b.get("n", 0) > 0]
    supera = sum(1 for e in exp_bases if m.get("n", 0) and m["expectativa_R"] > e)

    lineas = [
        f"# Simulación — {a.simbolo} — {sen.ref}",
        "",
        "**Resultado de simulación, no de operación real.** Latencia y slippage son supuestos "
        f"(latencia: {'pings grabados' if a.latencia_ms == 'status' else a.latencia_ms + ' ms'}; "
        f"slippage {a.slippage:g} por lado; comisión {a.comision:g} por lote).",
        "",
        f"- Ticks: {len(ticks):,} · señales: {sen.cantidad():,} · parámetros: `{json.dumps(sen.parametros)}`",
        f"- Capital inicial {cuenta.capital_inicial:g}, riesgo {cuenta.riesgo_por_operacion * 100:g} % por operación"
        + (f", lotes fijos {cuenta.lotes_fijos:g}" if cuenta.lotes_fijos else "")
        + f", valor por 1,0 de precio y lote: {cuenta.valor_por_precio:g}",
        f"- No operadas: {dict(res.no_operadas)}" + (f" · **detenida por {res.detenido}**" if res.detenido else ""),
        "",
        tabla([(sen.ref, m)] + [(f"Azar (semilla {s})", b) for s, b in enumerate(bases)]),
        "",
        f"**La estrategia supera a {supera} de {len(exp_bases)} corridas al azar en expectativa.** "
        "Para tomarla en serio tiene que superar a casi todas, con cota inferior positiva, y repetirlo fuera de muestra.",
        "",
    ]
    if m.get("n", 0):
        lineas += [
            "## De dónde sale el costo (promedio por operación, unidades de precio)",
            "",
            f"- Medio spread entrada + salida: {m['medio_spread_medio']:.4f}",
            f"- Slippage: {m['slippage_medio']:.4f}",
            f"- Deriva por latencia: {m['deriva_media']:+.4f}",
            f"- Salidas: {m['salidas']}",
            "",
        ]
    texto = "\n".join(lineas)
    Path(a.salida).write_text(texto, encoding="utf-8")
    if a.operaciones_csv:
        res.operaciones.to_csv(a.operaciones_csv, index=False)
    print(texto)


if __name__ == "__main__":
    main()
