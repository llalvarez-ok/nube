import numpy as np
import pandas as pd

from research.features.motor import COLUMNAS, calcular, calcular_referencia
from research.ticks.formato import TICK_DTYPE


def ticks_irregulares(n=600, semilla=3):
    rng = np.random.default_rng(semilla)
    t = np.zeros(n, dtype=TICK_DTYPE)
    # intervalos irregulares, con ticks repetidos en el mismo ms y huecos largos
    pasos = rng.choice([0, 1, 50, 300, 900, 2500, 40_000], size=n, p=[.05, .1, .3, .3, .15, .08, .02])
    t["time_msc"] = 1_790_000_000_000 + np.cumsum(pasos)
    mid = 4400 + np.cumsum(rng.choice([-0.01, 0, 0.01, 0.02], size=n))
    spread = rng.choice([0.1, 0.12, 0.2, 0.5], size=n)
    t["bid"] = mid - spread / 2
    t["ask"] = mid + spread / 2
    return t


def test_vectorizada_igual_a_referencia():
    ticks = ticks_irregulares()
    rapido = calcular(ticks)
    lento = calcular_referencia(ticks)
    assert list(rapido.columns) == COLUMNAS
    for col in COLUMNAS:
        a = rapido[col].to_numpy(dtype=float)
        b = lento[col].to_numpy(dtype=float)
        assert np.array_equal(np.isnan(a), np.isnan(b)), col
        ok = ~np.isnan(a)
        assert np.allclose(a[ok], b[ok], rtol=1e-9, atol=1e-9), col


def test_features_causales():
    ticks = ticks_irregulares()
    completo = calcular(ticks)
    parcial = calcular(ticks[:300])
    pd.testing.assert_frame_equal(completo.iloc[:300].reset_index(drop=True), parcial, check_exact=False)


def test_eficiencia_de_un_movimiento_recto_es_uno():
    n = 400   # 40 s: hace falta historia de más de 30 s para ret_30s
    t = np.zeros(n, dtype=TICK_DTYPE)
    t["time_msc"] = 1_790_000_000_000 + np.arange(n) * 100
    t["bid"] = 100 + np.arange(n) * 0.01
    t["ask"] = t["bid"] + 0.02
    f = calcular(t)
    assert np.allclose(f["eficiencia_30s"].iloc[-1], 1.0)
    assert f["desequilibrio_30s"].iloc[-1] == 1.0
