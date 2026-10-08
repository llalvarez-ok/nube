"""Gráficos PNG (matplotlib). Paleta: instancia de referencia validada (categórica en
orden fijo, divergente azul<->rojo con punto medio gris para expectancy +/-)."""
from __future__ import annotations

import textwrap
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm  # noqa: E402

SURFACE = "#fcfcfb"
INK, INK2, GRID = "#0b0b0b", "#52514e", "#e4e3df"
SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#4a3aa7", "#e34948"]
POS, NEG = "#2a78d6", "#e34948"
DIVERGING = LinearSegmentedColormap.from_list("div", ["#e34948", "#f0efec", "#2a78d6"])

plt.rcParams.update({
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
    "axes.edgecolor": GRID, "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
    "text.color": INK, "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6,
    "axes.spines.top": False, "axes.spines.right": False, "font.size": 9, "axes.titlesize": 11,
    "axes.titleweight": "bold", "lines.linewidth": 2, "figure.dpi": 110,
})


def _save(fig, path: Path, synthetic: bool):
    if synthetic:
        fig.text(0.5, 0.5, "DATOS SINTÉTICOS — PRUEBA DE SOFTWARE", ha="center", va="center",
                 fontsize=22, color="#e34948", alpha=0.25, rotation=20)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def equity_drawdown(eq: pd.Series, title: str, path: Path, synthetic=False, seg_bounds=None):
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True, gridspec_kw={"height_ratios": [3, 1.3]})
    a1.plot(eq.index, eq.values, color=SERIES[0])
    a1.set_title(f"{title} — equity")
    a1.set_ylabel("USD")
    peak = eq.cummax()
    dd = (eq - peak) / peak * 100
    a2.fill_between(dd.index, dd.values, 0, color=NEG, alpha=0.35, linewidth=0)
    a2.plot(dd.index, dd.values, color=NEG, linewidth=1)
    a2.set_title("Drawdown")
    a2.set_ylabel("%")
    if seg_bounds:
        for ax in (a1, a2):
            for lbl, x in seg_bounds.items():
                ax.axvline(x, color=INK2, linewidth=1, linestyle="--")
        for lbl, x in seg_bounds.items():
            a1.annotate(lbl, (x, 1), xycoords=("data", "axes fraction"), color=INK2, fontsize=8,
                        xytext=(3, -12), textcoords="offset points")
    _save(fig, path, synthetic)


def bar_by_period(values: pd.Series, title: str, ylabel: str, path: Path, synthetic=False):
    fig, ax = plt.subplots(figsize=(max(6, len(values) * 0.25 + 2), 4))
    colors = [POS if v >= 0 else NEG for v in values.values]
    ax.bar([str(i) for i in values.index], values.values, color=colors, width=0.8)
    ax.axhline(0, color=INK2, linewidth=1)
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    if len(values) > 24:
        for lbl in ax.get_xticklabels():
            lbl.set_rotation(90)
            lbl.set_fontsize(6)
    _save(fig, path, synthetic)


def histogram(x, title: str, xlabel: str, path: Path, synthetic=False, vlines=None, color=None):
    fig, ax = plt.subplots(figsize=(7, 4))
    x = np.asarray(x, float)
    x = x[np.isfinite(x)]
    ax.hist(x, bins=60, color=color or SERIES[0], edgecolor=SURFACE, linewidth=0.5)
    for lbl, v in (vlines or {}).items():
        ax.axvline(v, color=INK2, linestyle="--", linewidth=1)
        ax.annotate(lbl, (v, 1), xycoords=("data", "axes fraction"), xytext=(3, -12),
                    textcoords="offset points", fontsize=8, color=INK2)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("operaciones" if "R" in xlabel else "simulaciones")
    _save(fig, path, synthetic)


def heatmap(mat: pd.DataFrame, title: str, path: Path, synthetic=False, fmt="{:.2f}", counts=None,
            min_count=None, cbar_label="expectancy (R)"):
    fig, ax = plt.subplots(figsize=(max(7, mat.shape[1] * 0.9 + 2.5), max(3.5, mat.shape[0] * 0.45 + 2)))
    v = mat.values.astype(float)
    if counts is not None and min_count:
        v = np.where(counts.reindex_like(mat).values >= min_count, v, np.nan)
    lim = np.nanmax(np.abs(v)) if np.isfinite(v).any() else 1.0
    lim = lim if lim > 0 else 1.0
    im = ax.imshow(v, cmap=DIVERGING, norm=TwoSlopeNorm(0, -lim, lim), aspect="auto")
    ax.set_xticks(range(mat.shape[1]), [str(c) for c in mat.columns], rotation=45, ha="right")
    ax.set_yticks(range(mat.shape[0]), [str(i) for i in mat.index])
    ax.grid(False)
    for i in range(v.shape[0]):
        for j in range(v.shape[1]):
            txt = "—" if not np.isfinite(v[i, j]) else fmt.format(v[i, j])
            ax.text(j, i, txt, ha="center", va="center", fontsize=7, color=INK)
    cb = fig.colorbar(im, ax=ax, shrink=0.8)
    cb.set_label(cbar_label)
    ax.set_title("\n".join(textwrap.wrap(title, 60)))
    _save(fig, path, synthetic)


def hbar(values: pd.Series, title: str, xlabel: str, path: Path, synthetic=False):
    values = values.sort_values()
    fig, ax = plt.subplots(figsize=(8, max(3, len(values) * 0.35 + 1)))
    ax.barh([str(i) for i in values.index], values.values,
            color=[POS if v >= 0 else NEG for v in values.values], height=0.7)
    ax.axvline(0, color=INK2, linewidth=1)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    for y, v in enumerate(values.values):
        ax.annotate(f"{v:.3f}", (v, y), xytext=(4 if v >= 0 else -4, 0), textcoords="offset points",
                    ha="left" if v >= 0 else "right", va="center", fontsize=7, color=INK2)
    _save(fig, path, synthetic)


def walk_forward_chart(wf: pd.DataFrame, title: str, path: Path, synthetic=False):
    if wf.empty:
        return
    fig, ax = plt.subplots(figsize=(9, 4))
    x = np.arange(len(wf))
    w = 0.38
    ax.bar(x - w / 2, wf["wf_test_expectancy_R"].fillna(0), width=w, color=SERIES[0],
           label="config. elegida en cada ventana de train")
    ax.bar(x + w / 2, wf["final_test_expectancy_R"].fillna(0), width=w, color=SERIES[1],
           label="config. congelada final")
    ax.axhline(0, color=INK2, linewidth=1)
    ax.set_xticks(x, [str(d) for d in wf["test_start"]], rotation=45, ha="right")
    ax.set_ylabel("expectancy test (R)")
    ax.set_title(title)
    ax.legend(frameon=False, fontsize=8)
    _save(fig, path, synthetic)
