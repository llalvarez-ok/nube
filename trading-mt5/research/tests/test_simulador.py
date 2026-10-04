import numpy as np
import pytest

from research.estrategias import aleatoria
from research.estrategias.base import Senales
from research.features.motor import calcular
from research.sim.metricas import resumen
from research.sim.simulador import ConfigCuenta, ConfigEjecucion, ConfigNoOperar, simular
from research.ticks.formato import TICK_DTYPE

T0 = 1_790_000_000_000


def serie(mids, spread=0.2, paso_ms=100):
    n = len(mids)
    t = np.zeros(n, dtype=TICK_DTYPE)
    t["time_msc"] = T0 + np.arange(n) * paso_ms
    t["bid"] = np.asarray(mids) - spread / 2
    t["ask"] = np.asarray(mids) + spread / 2
    return t


def una_senal(n, i, d, stop, objetivo=np.nan, hold_ms=np.nan):
    direccion = np.zeros(n, dtype=np.int8)
    direccion[i] = d
    return Senales(direccion, np.full(n, stop), np.full(n, objetivo), np.full(n, hold_ms), "TEST", "V1")


def correr(ticks, sen, **kw):
    ejec = kw.pop("ejecucion", ConfigEjecucion(latencia_ms=(0.0,)))
    cuenta = kw.pop("cuenta", ConfigCuenta(lotes_fijos=1.0, valor_por_precio=1.0))
    no_operar = kw.pop("no_operar", ConfigNoOperar(spread_rel_max=10))
    return simular(ticks, calcular(ticks), sen, "TEST", ejec, cuenta, no_operar)


def test_compra_que_llega_al_objetivo():
    mids = [100.0] * 20 + [100 + 0.1 * k for k in range(1, 40)]
    ticks = serie(mids)
    r = correr(ticks, una_senal(len(mids), 10, +1, stop=1.0, objetivo=2.0))
    op = r.operaciones.iloc[0]
    assert op["motivo_salida"] == "OBJETIVO"
    assert op["precio_entrada"] == pytest.approx(100.1)          # ask del tick de entrada
    assert op["precio_salida"] >= op["precio_objetivo"] - 1e-9  # se ejecuta al bid que lo tocó
    assert op["neto_precio"] == pytest.approx(op["bruto_precio"] - op["costo_entrada"] - op["costo_salida"])


def test_latencia_ejecuta_en_el_tick_posterior():
    mids = [100 + 0.01 * k for k in range(100)]
    ticks = serie(mids)
    r = correr(ticks, una_senal(100, 10, +1, stop=5, hold_ms=1000),
               ejecucion=ConfigEjecucion(latencia_ms=(250.0,)))
    op = r.operaciones.iloc[0]
    assert op["t_entrada"] == T0 + 1300          # señal en 1000 ms + 250 -> primer tick >= 1250
    assert op["deriva_entrada"] == pytest.approx(0.03)
    assert op["motivo_salida"] == "TIEMPO"
    assert op["t_salida"] == op["t_disparo_salida"] + 300   # la salida por tiempo también sufre latencia


def test_stop_gana_si_el_mismo_tick_toca_ambos():
    mids = [100.0] * 10 + [100.0, 105.0]
    ticks = serie(mids, spread=12.0)   # spread enorme: el tick toca stop y objetivo a la vez
    r = correr(ticks, una_senal(len(mids), 5, +1, stop=1.0, objetivo=1.0))
    assert r.operaciones.iloc[0]["motivo_salida"] == "STOP"


def test_venta_con_slippage_y_comision():
    mids = [100.0] * 10 + [100 - 0.1 * k for k in range(1, 30)]
    ticks = serie(mids)
    ejec = ConfigEjecucion(latencia_ms=(0.0,), slippage=(0.05,), comision_por_lote_rt=0.3)
    r = correr(ticks, una_senal(len(mids), 5, -1, stop=1.0, objetivo=1.0), ejecucion=ejec)
    op = r.operaciones.iloc[0]
    assert op["precio_entrada"] == pytest.approx(99.9 - 0.05)
    assert op["motivo_salida"] == "OBJETIVO"
    assert op["neto_dinero"] == pytest.approx(op["neto_precio"] - 0.3)
    assert op["neto_precio"] == pytest.approx(op["bruto_precio"] - op["costo_entrada"] - op["costo_salida"])


def test_no_redondea_hacia_arriba_al_volumen_minimo():
    ticks = serie([100.0] * 50)
    cuenta = ConfigCuenta(capital_inicial=10.0, riesgo_por_operacion=0.005, valor_por_precio=100.0,
                          volumen_min=0.01, volumen_paso=0.01)
    r = correr(ticks, una_senal(50, 10, +1, stop=1.0), cuenta=cuenta)
    assert len(r.operaciones) == 0 and r.no_operadas["TAMANO"] == 1


def test_rechazo_y_spread_excesivo():
    ticks = serie([100.0] * 50)
    r = correr(ticks, una_senal(50, 10, +1, stop=1.0),
               ejecucion=ConfigEjecucion(latencia_ms=(0.0,), prob_rechazo=1.0))
    assert r.no_operadas["RECHAZO"] == 1
    ticks["ask"][10] += 5.0
    r = correr(ticks, una_senal(50, 10, +1, stop=1.0), no_operar=ConfigNoOperar(spread_rel_max=2.0))
    assert r.no_operadas["SPREAD"] == 1


def test_una_posicion_a_la_vez_y_drawdown_detiene():
    rng = np.random.default_rng(0)
    mids = 100 + np.cumsum(rng.normal(0, 0.05, 20_000))
    ticks = serie(mids, spread=0.3)
    f = calcular(ticks)
    sen = aleatoria.senales(f, prob_por_segundo=0.5, stop_rango=0.5, max_hold_s=5, semilla=1)
    cuenta = ConfigCuenta(capital_inicial=1000, riesgo_por_operacion=0.02, valor_por_precio=100,
                          perdida_diaria_max=1.0, drawdown_max=0.10)
    r = simular(ticks, f, sen, "T", ConfigEjecucion(latencia_ms=(0.0,)), cuenta, ConfigNoOperar())
    ops = r.operaciones
    assert (ops["t_entrada"].to_numpy()[1:] > ops["t_salida"].to_numpy()[:-1]).all()
    assert r.detenido == "DRAWDOWN"
    assert r.capital_final <= 1000 * 0.9 + 1e-6
    assert r.capital_final > 1000 * 0.9 - 1000 * 0.02 * 3   # la última pérdida es acotada


def test_azar_en_paseo_aleatorio_pierde_el_costo():
    rng = np.random.default_rng(5)
    mids = 100 + np.cumsum(rng.normal(0, 0.05, 200_000))
    ticks = serie(mids, spread=0.1)
    f = calcular(ticks)
    sen = aleatoria.senales(f, prob_por_segundo=0.2, stop_rango=1.0, max_hold_s=30, semilla=2)
    cuenta = ConfigCuenta(lotes_fijos=1.0, valor_por_precio=1.0, perdida_diaria_max=1.0, drawdown_max=1.0)
    r = simular(ticks, f, sen, "T", ConfigEjecucion(latencia_ms=(0.0,)), cuenta, ConfigNoOperar())
    m = resumen(r.operaciones, cuenta.capital_inicial)
    assert m["n"] > 300
    # Sin ventaja, el bruto ronda cero y el neto es aproximadamente menos el costo
    err = 3 * r.operaciones["bruto_precio"].std() / np.sqrt(m["n"])
    assert abs(m["bruto_medio_precio"]) < err
    assert m["costo_medio_precio"] == pytest.approx(0.1, rel=0.05)
