#!/usr/bin/env python3
"""CLI del framework.

  python run.py check-data                 # verificación de datos (regla 36) — SIEMPRE primero
  python run.py run                        # estudio completo
  python run.py run --symbols USDJPY JP225 --strategies A_asian_range_breakout
  python run.py run --config config/mi_config.yaml --workers 4
"""
from __future__ import annotations

import argparse
import sys

from tokyo_bt.config import load_config
from tokyo_bt.quality import CRITICAL, check_all


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["check-data", "run"])
    ap.add_argument("--config", default=None)
    ap.add_argument("--symbols", nargs="*")
    ap.add_argument("--strategies", nargs="*")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--skip-costs", action="store_true", help="omite la sensibilidad de costos (más rápido)")
    a = ap.parse_args(argv)
    cfg = load_config(a.config)
    syms = a.symbols or list(cfg["instruments"])

    if a.command == "check-data":
        reps = check_all(cfg, syms)
        for s, r in reps.items():
            print(f"{s:8s} {r['status']}")
            for i in r["issues"]:
                print(f"   - {i['level']}: {i['msg']}")
        print("\nDetalle: output/data_quality.md")
        return 1 if all(r["status"] == CRITICAL for r in reps.values()) else 0

    from tokyo_bt.pipeline import run
    run(cfg, syms, a.strategies, workers=a.workers, skip_costs=a.skip_costs)
    print("\nListo: output/REPORT.md, output/tables/, output/charts/, output/trade_log/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
