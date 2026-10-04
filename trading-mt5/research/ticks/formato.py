"""Lectura de los archivos de ticks que escribe ATS_TickRecorder.mq5.

Cada archivo `ticks/<SIMBOLO>/<AAAAMMDD>.bin` es una secuencia de registros
de 52 bytes, little-endian, sin encabezado. Si se cambia el orden de los campos
en el servicio de MT5, hay que cambiarlo también acá.
"""
from pathlib import Path

import numpy as np

TICK_DTYPE = np.dtype([
    ("time_msc", "<i8"),     # hora del servidor del broker, ms desde 1970
    ("bid", "<f8"),
    ("ask", "<f8"),
    ("last", "<f8"),
    ("volume_real", "<f8"),
    ("flags", "<u4"),        # TICK_FLAG_* de MT5
    ("local_us", "<u8"),     # reloj monotónico local al leer el tick (µs)
])
assert TICK_DTYPE.itemsize == 52


def leer_archivo(path):
    """Lee un archivo .bin. Ignora un registro final incompleto (escritura cortada)."""
    datos = Path(path).read_bytes()
    completos = len(datos) // TICK_DTYPE.itemsize
    return np.frombuffer(datos[: completos * TICK_DTYPE.itemsize], dtype=TICK_DTYPE)


def leer_simbolo(raiz, simbolo, desde=None, hasta=None):
    """Lee todos los días grabados de un símbolo, ordenados por hora del servidor.

    `desde` y `hasta` son claves AAAAMMDD opcionales (inclusive).
    """
    carpeta = Path(raiz) / "ticks" / simbolo
    archivos = sorted(carpeta.glob("*.bin"))
    if desde:
        archivos = [a for a in archivos if a.stem >= desde]
    if hasta:
        archivos = [a for a in archivos if a.stem <= hasta]
    if not archivos:
        raise FileNotFoundError(f"No hay archivos de ticks en {carpeta}")
    ticks = np.concatenate([leer_archivo(a) for a in archivos])
    orden = np.argsort(ticks["time_msc"], kind="stable")
    return ticks[orden]


def escribir_archivo(path, ticks):
    """Escribe ticks en el mismo formato (para tests y datos sintéticos)."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    np.asarray(ticks, dtype=TICK_DTYPE).tofile(path)
