"""Métricas de un conjunto de operaciones. Ninguna se informa sin su tamaño de muestra."""
import numpy as np

Z_95 = 1.96


def resumen(ops, capital_inicial):
    if ops is None or len(ops) == 0:
        return {"n": 0}
    r = ops["neto_R"].to_numpy(dtype=float)
    dinero = ops["neto_dinero"].to_numpy(dtype=float)
    ganadoras = dinero > 0
    n = len(r)
    desvio = float(np.std(r, ddof=1)) if n > 1 else float("nan")
    curva = np.concatenate([[capital_inicial], ops["capital_despues"].to_numpy(dtype=float)])
    maximos = np.maximum.accumulate(curva)
    perdidas_totales = -dinero[~ganadoras].sum()
    return {
        "n": n,
        "win_rate": float(ganadoras.mean()),
        "ganancia_media": float(dinero[ganadoras].mean()) if ganadoras.any() else 0.0,
        "perdida_media": float(dinero[~ganadoras].mean()) if (~ganadoras).any() else 0.0,
        "profit_factor": float(dinero[ganadoras].sum() / perdidas_totales) if perdidas_totales > 0 else float("inf"),
        "expectativa_R": float(r.mean()),
        "desvio_R": desvio,
        "lcb_R": float(r.mean() - Z_95 * desvio / np.sqrt(n)) if n > 1 else float("nan"),
        "neto_total": float(dinero.sum()),
        "drawdown_max": float(np.max((maximos - curva) / maximos)),
        "bruto_medio_precio": float(ops["bruto_precio"].mean()),
        "costo_medio_precio": float((ops["costo_entrada"] + ops["costo_salida"]).mean()),
        "medio_spread_medio": float((ops["medio_spread_entrada"] + ops["medio_spread_salida"]).mean()),
        "slippage_medio": float((ops["slippage_entrada"] + ops["slippage_salida"]).mean()),
        "deriva_media": float((ops["deriva_entrada"] + ops["deriva_salida"]).mean()),
        "duracion_media_s": float(ops["duracion_ms"].mean() / 1000.0),
        "salidas": ops["motivo_salida"].value_counts().to_dict(),
    }


def tabla(filas):
    """filas: lista de (nombre, resumen). Devuelve una tabla markdown."""
    enc = ("| | n | Aciertos | Expectativa (R) | Cota inferior 95 % (R) | Profit factor | Neto | "
           "Drawdown máx. | Costo medio | Bruto medio | Duración media |")
    lineas = [enc, "|---" * 11 + "|"]
    for nombre, m in filas:
        if m.get("n", 0) == 0:
            lineas.append(f"| {nombre} | 0 |" + " — |" * 9)
            continue
        lineas.append(
            f"| {nombre} | {m['n']} | {m['win_rate'] * 100:.1f} % | {m['expectativa_R']:+.3f} | "
            f"{m['lcb_R']:+.3f} | {m['profit_factor']:.2f} | {m['neto_total']:+.2f} | "
            f"{m['drawdown_max'] * 100:.1f} % | {m['costo_medio_precio']:.4f} | {m['bruto_medio_precio']:+.4f} | "
            f"{m['duracion_media_s']:.1f} s |"
        )
    return "\n".join(lineas)
