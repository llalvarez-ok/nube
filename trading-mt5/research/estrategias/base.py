"""Contrato común de las estrategias.

Una estrategia solo propone: dirección, distancia del stop, distancia del
objetivo y tiempo máximo. No decide el tamaño ni envía órdenes; eso lo hacen el
Risk Engine y el Execution Engine (en investigación, el simulador).
"""
from dataclasses import dataclass, field

import numpy as np


@dataclass
class Senales:
    direccion: np.ndarray      # int8 por tick: +1 compra, -1 venta, 0 nada
    stop: np.ndarray           # distancia al stop en unidades de precio
    objetivo: np.ndarray       # distancia al objetivo (NaN = sin objetivo)
    max_hold_ms: np.ndarray    # tiempo máximo en la operación (NaN = sin límite)
    estrategia: str
    version: str
    parametros: dict = field(default_factory=dict)

    @property
    def ref(self):
        return f"{self.estrategia}@{self.version}"

    def cantidad(self):
        return int(np.count_nonzero(self.direccion))


def primer_tick_de_cada_segundo(time_msc):
    """Las decisiones se toman como máximo una vez por segundo, en el primer tick
    de cada segundo. Así la frecuencia no depende de cuántos ticks manda el broker."""
    seg = np.asarray(time_msc) // 1000
    marca = np.ones(len(seg), dtype=bool)
    marca[1:] = seg[1:] != seg[:-1]
    return marca


def vacias(n):
    return (np.zeros(n, dtype=np.int8), np.full(n, np.nan), np.full(n, np.nan), np.full(n, np.nan))
