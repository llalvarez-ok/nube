"""MOMENTUM V0: esqueleto para probar la cadena completa. NO está validada.

Hipótesis económica: después de un impulso rápido y "limpio" (con poco ida y
vuelta), el flujo de órdenes que lo causó tiende a continuar unos segundos.
"""
import numpy as np

from research.estrategias.base import Senales, primer_tick_de_cada_segundo, vacias


def senales(features, ventana_s=5, umbral_rango=0.5, eficiencia_min=0.6,
            stop_rango=1.0, objetivo_r=1.0, max_hold_s=60.0):
    n = len(features)
    direccion, stop, objetivo, hold = vacias(n)
    ret = features[f"ret_{ventana_s}s"].to_numpy()
    rango = features["rango_120s"].to_numpy()
    efic = features["eficiencia_30s"].to_numpy()
    with np.errstate(invalid="ignore"):
        activa = (
            primer_tick_de_cada_segundo(features["time_msc"].to_numpy())
            & (rango > 0)
            & (np.abs(ret) >= umbral_rango * rango)
            & (efic >= eficiencia_min)
        )
    direccion[activa] = np.sign(ret[activa]).astype(np.int8)
    stop[:] = stop_rango * rango
    objetivo[:] = objetivo_r * stop
    hold[:] = max_hold_s * 1000.0
    return Senales(direccion, stop, objetivo, hold, "MOMENTUM", "V0",
                   dict(ventana_s=ventana_s, umbral_rango=umbral_rango, eficiencia_min=eficiencia_min,
                        stop_rango=stop_rango, objetivo_r=objetivo_r, max_hold_s=max_hold_s))
