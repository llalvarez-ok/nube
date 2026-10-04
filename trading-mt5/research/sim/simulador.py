"""Simulador de ejecución sobre ticks grabados.

Reproduce lo que pasaría en vivo con una sola posición por símbolo:

1. En el tick de la señal se aplican los filtros de no-operar y el tamaño.
2. La orden llega al broker después de una latencia sorteada: se ejecuta en el
   primer tick con hora >= señal + latencia, al ask (compra) o al bid (venta),
   más un slippage sorteado. Puede ser rechazada con cierta probabilidad.
3. El stop y el objetivo están en el servidor: se disparan en el primer tick que
   los toca y se ejecutan a ese precio más slippage. Si un mismo tick toca los
   dos, se asume el stop (supuesto conservador).
4. La salida por tiempo la manda el robot: sufre latencia y slippage.

Todos los costos se miden contra el mid del momento de cada decisión
(implementation shortfall), separados en medio spread, slippage y deriva por
latencia. Identidad que se verifica en los tests:

    neto = bruto (mid a mid) - costo de entrada - costo de salida
"""
from collections import Counter
from dataclasses import dataclass, field

import numpy as np
import pandas as pd

EPS = 1e-9


@dataclass
class ConfigEjecucion:
    latencia_ms: tuple = (200.0,)   # muestras (se sortea una por orden). SUPUESTO hasta medir
    slippage: tuple = (0.0,)        # muestras en unidades de precio; positivo = en contra
    prob_rechazo: float = 0.0
    comision_por_lote_rt: float = 0.0   # en moneda de la cuenta, ida y vuelta
    stops_level: float = 0.0            # distancia mínima del stop, en unidades de precio
    semilla: int = 0


@dataclass
class ConfigCuenta:
    capital_inicial: float = 1000.0
    valor_por_precio: float = 100.0     # dinero por 1,0 de movimiento del precio con 1 lote
    volumen_min: float = 0.01
    volumen_max: float = 100.0
    volumen_paso: float = 0.01
    riesgo_por_operacion: float = 0.005  # fracción del capital; ignorado si hay lotes_fijos
    lotes_fijos: float = None
    perdida_diaria_max: float = 0.02     # fracción del capital al inicio del día
    drawdown_max: float = 0.10           # desde el máximo; al superarlo se detiene todo


@dataclass
class ConfigNoOperar:
    spread_rel_max: float = 2.0          # spread / promedio de 10 min
    edad_tick_max_ms: float = 5000.0     # tick anterior demasiado viejo = datos dudosos
    horas_permitidas: frozenset = None   # None = todas (hora del servidor)


@dataclass
class Resultado:
    operaciones: pd.DataFrame
    no_operadas: Counter
    capital_final: float
    detenido: str = ""
    parametros: dict = field(default_factory=dict)


def _tamano(cuenta, capital, stop, costo_estimado):
    if cuenta.lotes_fijos:
        return cuenta.lotes_fijos
    perdida_por_lote = (stop + costo_estimado) * cuenta.valor_por_precio
    if perdida_por_lote <= 0:
        return 0.0
    lotes = capital * cuenta.riesgo_por_operacion / perdida_por_lote
    lotes = np.floor(lotes / cuenta.volumen_paso + EPS) * cuenta.volumen_paso
    return float(min(lotes, cuenta.volumen_max))


def _primer(cond):
    idx = np.flatnonzero(cond)
    return int(idx[0]) if len(idx) else -1


def simular(ticks, features, senales, simbolo="", ejecucion=None, cuenta=None, no_operar=None):
    ejecucion = ejecucion or ConfigEjecucion()
    cuenta = cuenta or ConfigCuenta()
    no_operar = no_operar or ConfigNoOperar()
    rng = np.random.default_rng(ejecucion.semilla)

    t = np.asarray(ticks["time_msc"], dtype=np.int64)
    bid = np.asarray(ticks["bid"], dtype=float)
    ask = np.asarray(ticks["ask"], dtype=float)
    mid = (bid + ask) / 2.0
    spread = ask - bid
    n = len(t)
    spread_rel = features["spread_rel"].to_numpy()
    dt_prev = features["dt_prev_ms"].to_numpy()
    hora = features["hora"].to_numpy()
    lat = np.asarray(ejecucion.latencia_ms, dtype=float)
    slip = np.asarray(ejecucion.slippage, dtype=float)
    costo_estimado_extra = 2.0 * float(np.mean(slip))

    capital = cuenta.capital_inicial
    maximo = capital
    dia_actual, capital_inicio_dia, detenido_dia = None, capital, False
    detenido = ""
    ops, no_op = [], Counter()
    fin_posicion = -1

    for i in np.flatnonzero(senales.direccion != 0):
        if i <= fin_posicion:
            no_op["POSICION_ABIERTA"] += 1
            continue
        if detenido:
            no_op["DETENIDO_" + detenido] += 1
            continue
        dia = t[i] // 86_400_000
        if dia != dia_actual:
            dia_actual, capital_inicio_dia, detenido_dia = dia, capital, False
        if detenido_dia:
            no_op["PERDIDA_DIARIA"] += 1
            continue
        if not (dt_prev[i] <= no_operar.edad_tick_max_ms):
            no_op["DATOS"] += 1
            continue
        if not (spread_rel[i] <= no_operar.spread_rel_max):
            no_op["SPREAD"] += 1
            continue
        if no_operar.horas_permitidas is not None and int(hora[i]) not in no_operar.horas_permitidas:
            no_op["HORARIO"] += 1
            continue

        d = int(senales.direccion[i])
        stop_d = float(senales.stop[i])
        if not (stop_d > 0):
            no_op["SIN_STOP"] += 1
            continue
        if stop_d < ejecucion.stops_level:
            no_op["STOPS_LEVEL"] += 1
            continue
        lotes = _tamano(cuenta, capital, stop_d, spread[i] + costo_estimado_extra)
        if lotes < cuenta.volumen_min - EPS:
            no_op["TAMANO"] += 1   # nunca se redondea hacia arriba al volumen mínimo
            continue
        if rng.random() < ejecucion.prob_rechazo:
            no_op["RECHAZO"] += 1
            continue

        # Entrada
        lat_in = float(rng.choice(lat))
        j = int(np.searchsorted(t, t[i] + lat_in, side="left"))
        if j >= n:
            no_op["FIN_DATOS"] += 1
            break
        slip_in = float(rng.choice(slip))
        precio_in = ask[j] + slip_in if d > 0 else bid[j] - slip_in
        precio_stop = precio_in - d * stop_d
        obj_d = float(senales.objetivo[i])
        precio_obj = precio_in + d * obj_d if obj_d > 0 else np.nan
        hold = float(senales.max_hold_ms[i])
        limite = t[j] + hold if hold > 0 else np.inf

        # Búsqueda del disparo de salida, vectorizada por tramos
        k, motivo = -1, None
        desde = j + 1
        while desde < n and motivo is None:
            if np.isinf(limite):
                hasta = min(n, desde + 50_000)
            else:
                # Incluye el primer tick con hora >= límite
                hasta = min(n, int(np.searchsorted(t, limite, side="left")) + 1)
            px_cierre = bid[desde:hasta] if d > 0 else ask[desde:hasta]
            toca_stop = (px_cierre <= precio_stop) if d > 0 else (px_cierre >= precio_stop)
            if obj_d > 0:
                toca_obj = (px_cierre >= precio_obj) if d > 0 else (px_cierre <= precio_obj)
            else:
                toca_obj = np.zeros(len(px_cierre), dtype=bool)
            vence = t[desde:hasta] >= limite
            primeros = [(_primer(c), m) for c, m in ((toca_stop, "STOP"), (toca_obj, "OBJETIVO"), (vence, "TIEMPO"))]
            primeros = [(x, m) for x, m in primeros if x >= 0]
            if primeros:
                # min toma el primer tick; en empate gana el orden STOP > OBJETIVO > TIEMPO
                pos, motivo = min(primeros, key=lambda xm: (xm[0], ["STOP", "OBJETIVO", "TIEMPO"].index(xm[1])))
                k = desde + pos
            if not np.isinf(limite):
                break
            desde = hasta
        if motivo is None:
            k, motivo = n - 1, "FIN_DATOS"

        if motivo == "TIEMPO":
            lat_out = float(rng.choice(lat))
            e = min(n - 1, int(np.searchsorted(t, t[k] + lat_out, side="left")))
        else:
            lat_out, e = 0.0, k
        slip_out = float(rng.choice(slip)) if motivo != "FIN_DATOS" else 0.0
        precio_out = bid[e] - slip_out if d > 0 else ask[e] + slip_out

        recorrido = (bid[j:e + 1] if d > 0 else ask[j:e + 1]) - precio_in
        mfe = float(np.max(d * recorrido)) if len(recorrido) else 0.0
        mae = float(np.min(d * recorrido)) if len(recorrido) else 0.0

        bruto = d * (mid[k] - mid[i])
        deriva_in = d * (mid[j] - mid[i])
        deriva_out = d * (mid[k] - mid[e])
        costo_in = deriva_in + spread[j] / 2.0 + slip_in
        costo_out = deriva_out + spread[e] / 2.0 + slip_out
        neto_precio = d * (precio_out - precio_in)
        comision = ejecucion.comision_por_lote_rt * lotes
        neto_dinero = neto_precio * cuenta.valor_por_precio * lotes - comision
        riesgo_dinero = stop_d * cuenta.valor_por_precio * lotes

        capital += neto_dinero
        maximo = max(maximo, capital)
        ops.append({
            "simbolo": simbolo, "estrategia": senales.ref,
            "t_senal": int(t[i]), "t_entrada": int(t[j]), "t_disparo_salida": int(t[k]), "t_salida": int(t[e]),
            "direccion": d, "lotes": lotes,
            "mid_senal": mid[i], "precio_entrada": precio_in, "precio_stop": precio_stop, "precio_objetivo": precio_obj,
            "motivo_salida": motivo, "mid_disparo_salida": mid[k], "precio_salida": precio_out,
            "latencia_entrada_ms": lat_in, "latencia_salida_ms": lat_out,
            "slippage_entrada": slip_in, "slippage_salida": slip_out,
            "medio_spread_entrada": spread[j] / 2.0, "medio_spread_salida": spread[e] / 2.0,
            "deriva_entrada": deriva_in, "deriva_salida": deriva_out,
            "bruto_precio": bruto, "costo_entrada": costo_in, "costo_salida": costo_out,
            "neto_precio": neto_precio, "comision": comision, "neto_dinero": neto_dinero,
            "neto_R": neto_dinero / riesgo_dinero if riesgo_dinero > 0 else np.nan,
            "mfe": mfe, "mae": mae, "duracion_ms": int(t[e] - t[j]), "capital_despues": capital,
        })
        fin_posicion = e

        if capital <= capital_inicio_dia * (1 - cuenta.perdida_diaria_max) + EPS:
            detenido_dia = True
        if capital <= maximo * (1 - cuenta.drawdown_max) + EPS:
            detenido = "DRAWDOWN"

    return Resultado(pd.DataFrame(ops), no_op, capital, detenido,
                     {"estrategia": senales.ref, **senales.parametros})
