"""Prueba de humo de punta a punta con datos SINTÉTICOS.

    python tests/run_smoke.py <dir_trabajo>

Genera (si faltan) dos random walks en formato MT5 y corre el pipeline completo con
grillas reducidas. El reporte queda marcado como SINTÉTICO. No produce resultados de trading.
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))

from synthetic import random_walk_m1  # noqa: E402
from tokyo_bt.config import load_config  # noqa: E402
from tokyo_bt.pipeline import run  # noqa: E402


def main(work: str):
    work = Path(work).resolve()
    raw = work / "raw"
    raw.mkdir(parents=True, exist_ok=True)
    for sym, seed, px in (("USDJPY", 1, 110.0), ("AUDJPY", 2, 80.0)):
        f = raw / f"{sym}_M1.csv"
        if not f.exists():
            random_walk_m1(seed=seed, price=px).to_csv(f, sep="\t", index=False)
    txt = (ROOT / "tests" / "smoke_config.yaml").read_text()
    txt = txt.replace("SYNTH_RAW", str(raw)).replace("SYNTH_CACHE", str(work / "cache")) \
             .replace("SYNTH_OUT", str(work / "output"))
    cfg = load_config(overrides=yaml.safe_load(txt))
    cfg["instruments"] = {k: v for k, v in cfg["instruments"].items() if k in ("USDJPY", "AUDJPY")}
    cfg["_synthetic"] = True
    run(cfg, ["USDJPY", "AUDJPY"], workers=int(sys.argv[2]) if len(sys.argv) > 2 else 2)
    print(f"Reporte SINTÉTICO en {work / 'output' / 'REPORT.md'}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "/tmp/tokyo_bt_smoke")
