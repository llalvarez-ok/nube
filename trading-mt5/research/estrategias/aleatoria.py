"""Línea base: entradas al azar con la misma lógica de salida que la estrategia
a evaluar. Si una estrategia no le gana a esto, su señal no aporta nada."""
import numpy as np

from research.estrategias.base import Senales, primer_tick_de_cada_segundo, vacias


def senales(features, prob_por_segundo=0.01, stop_rango=1.0, objetivo_r=1.0,
            max_hold_s=60.0, semilla=0):
    n = len(features)
    direccion, stop, objetivo, hold = vacias(n)
    rng = np.random.default_rng(semilla)
    candidatos = np.flatnonzero(primer_tick_de_cada_segundo(features["time_msc"].to_numpy()))
    elegidos = candidatos[rng.random(len(candidatos)) < prob_por_segundo]
    direccion[elegidos] = rng.choice(np.array([-1, 1], dtype=np.int8), size=len(elegidos))
    stop[:] = stop_rango * features["rango_120s"].to_numpy()
    objetivo[:] = objetivo_r * stop
    hold[:] = max_hold_s * 1000.0
    return Senales(direccion, stop, objetivo, hold, "ALEATORIA", "V1",
                   dict(prob_por_segundo=prob_por_segundo, stop_rango=stop_rango,
                        objetivo_r=objetivo_r, max_hold_s=max_hold_s, semilla=semilla))
