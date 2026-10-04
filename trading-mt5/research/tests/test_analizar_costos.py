import numpy as np

from research.ticks.analizar_costos import costo_vs_movimiento, grilla, leer_specs, limpiar, main
from research.ticks.formato import TICK_DTYPE, escribir_archivo, leer_archivo, leer_simbolo

T0 = 1_790_000_000_000  # ms, un día cualquiera de 2026


def ticks_sinteticos(n=200_000, paso_ms=200, sigma=0.05, spread=0.2, semilla=1):
    rng = np.random.default_rng(semilla)
    t = np.zeros(n, dtype=TICK_DTYPE)
    t["time_msc"] = T0 + np.arange(n) * paso_ms
    mid = 4400 + np.cumsum(rng.normal(0, sigma, n))
    t["bid"] = mid - spread / 2
    t["ask"] = mid + spread / 2
    return t


def test_formato_ida_y_vuelta_y_registro_cortado(tmp_path):
    t = ticks_sinteticos(n=10)
    f = tmp_path / "ticks" / "XAUUSDc" / "20260904.bin"
    escribir_archivo(f, t)
    with open(f, "ab") as h:
        h.write(b"\x00" * 20)  # escritura cortada a mitad de registro
    leidos = leer_archivo(f)
    assert len(leidos) == 10
    assert np.array_equal(leidos["bid"], t["bid"])
    assert len(leer_simbolo(tmp_path, "XAUUSDc")) == 10


def test_sigma_y_costo_de_un_paseo_aleatorio():
    t = ticks_sinteticos()
    g = grilla(t)
    r = costo_vs_movimiento(g, [5, 60], slippage_por_lado=0.05, comision_rt=0.1)
    for h in (5, 60):
        m = r[h]["total"]
        esperado = 0.05 * np.sqrt(h * 1000 / 200)
        assert abs(m["sigma"] / esperado - 1) < 0.1
        assert abs(m["costo"] - (0.2 + 0.1 + 0.1)) < 1e-9
        assert abs(m["cvr"] - m["costo"] / m["sigma"]) < 1e-9
    assert r[5]["total"]["cvr"] > r[60]["total"]["cvr"]


def test_mercado_cerrado_no_cuenta():
    t = ticks_sinteticos(n=20_000)
    t["time_msc"][10_000:] += 3_600_000  # una hora sin ticks en el medio
    g = grilla(t)
    assert (~g["valido"]).sum() > 3_000
    r = costo_vs_movimiento(g, [60])
    assert r[60]["total"]["n"] < len(g["t"]) - 3_000


def test_limpiar_descarta_ticks_imposibles():
    t = ticks_sinteticos(n=100)
    t["ask"][3] = t["bid"][3] - 1
    t["bid"][7] = 0
    limpios, descartados = limpiar(t)
    assert descartados == 2 and len(limpios) == 98


def test_reporte_completo(tmp_path):
    escribir_archivo(tmp_path / "ticks" / "XAUUSDc" / "20260904.bin", ticks_sinteticos())
    (tmp_path / "specs").mkdir()
    (tmp_path / "specs" / "XAUUSDc_20260904.csv").write_text(
        "key;value\naccount_company;Broker\ncontract_size;100.0000\nvolume_min;0.0100\n", encoding="latin-1")
    assert leer_specs(tmp_path, "XAUUSDc")["contract_size"] == "100.0000"
    salida = tmp_path / "r.md"
    main(["--raiz", str(tmp_path), "--simbolo", "XAUUSDc", "--salida", str(salida)])
    texto = salida.read_text(encoding="utf-8")
    assert "## Resumen por plazo" in texto and "| 300 s |" in texto


def test_varios_activos_y_supuestos_por_simbolo(tmp_path):
    from research.ticks.analizar_costos import valores_por_simbolo
    assert valores_por_simbolo("0.1", ["A", "B"]) == {"A": 0.1, "B": 0.1}
    assert valores_por_simbolo("A=2,B=0.5", ["A", "B", "C"]) == {"A": 2.0, "B": 0.5, "C": 0.0}

    escribir_archivo(tmp_path / "ticks" / "XAUUSDc" / "20260904.bin", ticks_sinteticos())
    escribir_archivo(tmp_path / "ticks" / "BTCUSDc" / "20260904.bin",
                     ticks_sinteticos(sigma=5.0, spread=10.0, semilla=2))
    salida = tmp_path / "r.md"
    main(["--raiz", str(tmp_path), "--simbolo", "XAUUSDc,BTCUSDc,US30c", "--salida", str(salida)])
    texto = salida.read_text(encoding="utf-8")
    assert "# Comparación entre activos" in texto
    assert "| XAUUSDc |" in texto and "| BTCUSDc |" in texto
    assert "US30c: No hay archivos" in texto
