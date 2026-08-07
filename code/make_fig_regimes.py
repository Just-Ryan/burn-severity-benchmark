#!/usr/bin/env python3
"""Figure — the pipeline as published against the pipeline given its best configuration.

The published pipeline trains its classifier on ground-truth masks and then, at test
time, feeds it masks predicted by the localiser. Those two distributions are not the
same. Regimes B and C repair that mismatch. This figure is the visual form of Table 5:
what the repair is worth, and what it is not worth.

Every value is read from ``pipeline_regimes_10seed.json`` and the ten classifier runs
in ``h2h_10seed_paired.json``; the paired differences are recomputed here rather than
copied from the table.

Usage
-----
    python make_fig_regimes.py
"""

from __future__ import annotations

import argparse
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

CLF = "#3B6EA8"
OLD = "#C4622D"
NEW = "#2E7D5B"

LABELS = [
    ("clf", "standalone\nclassifier", "", CLF),
    ("A", "A  published", "trained on GT masks,\ntested on predicted", OLD),
    ("B", "B  mask source\nmatched", "trained and tested\non predicted masks", NEW),
    ("C", "C  matched\n+ dilated", "as B, plus a 12 px rim\nof peri-lesional skin", NEW),
]



def _find(root: str, *candidates: str) -> str:
    """Resolve a data path under either layout.

    The working tree keeps results under ``01_paper/``; the public repository
    flattens them to the top level. The scripts ship in the repository, so they
    have to work there too.
    """
    for c in candidates:
        p = os.path.join(root, *c.split("/"))
        if os.path.exists(p):
            return p
    raise SystemExit("not found under %s: %s" % (root, " | ".join(candidates)))

def _out_default(root: str, name: str) -> str:
    """Write beside the manuscript in the working tree, into figures/ in the repo."""
    for rel in ("01_paper/melba", "figures"):
        d = os.path.join(root, *rel.split("/"))
        if os.path.isdir(d):
            return os.path.join(d, name)
    return os.path.join(root, name)



def panel(ax, series, clf_vals, title, subtitle):
    xs = np.arange(len(LABELS), dtype=float)
    rng = np.random.default_rng(7)
    lo_pad = []

    for i, (key, _, _, colour) in enumerate(LABELS):
        vals = np.asarray(clf_vals if key == "clf" else series[key], dtype=float)
        jit = rng.uniform(-0.11, 0.11, len(vals))
        ax.scatter(xs[i] + jit, vals, s=22, color=colour, alpha=0.75, zorder=3,
                   edgecolor="white", linewidth=0.5)
        ax.plot([xs[i] - 0.26, xs[i] + 0.26], [vals.mean()] * 2,
                color=colour, lw=2.6, zorder=4)
        ax.annotate(f"{vals.mean():.2f}", (xs[i] + 0.275, vals.mean()),
                    ha="left", va="center", fontsize=8.8,
                    fontweight="bold", color=colour)
        lo_pad.append(vals.min())

        if key != "clf":
            d = np.asarray(clf_vals, float) - vals
            p = stats.ttest_rel(np.asarray(clf_vals, float), vals).pvalue
            sign = "−" if d.mean() > 0 else "+"
            ax.annotate(f"{sign}{abs(d.mean()):.2f} pp\n$p={p:.3f}$",
                        (xs[i], 0.0), xycoords=("data", "axes fraction"),
                        xytext=(0, 9), textcoords="offset points",
                        ha="center", va="bottom", fontsize=8, color="#444444")

    ax.axhline(np.mean(clf_vals), color=CLF, lw=1.0, ls=(0, (5, 3)), alpha=0.55, zorder=1)
    ax.set_xlim(-0.55, len(LABELS) - 0.22)
    ax.set_xticks(xs)
    ax.set_xticklabels([l for _, l, _, _ in LABELS], fontsize=8.8)
    ax.set_title(title, fontsize=11, pad=16)
    ax.text(0.5, 1.012, subtitle, transform=ax.transAxes, ha="center", va="bottom",
            fontsize=8.5, color="#555555")
    ax.tick_params(axis="y", labelsize=9)
    ax.grid(axis="y", color="#e8e8e8", lw=0.7)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color("#999999")
    return min(lo_pad)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=os.path.join(os.path.dirname(__file__), "..", ".."))
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    root = os.path.abspath(args.repo_root)
    out = args.out or _out_default(root, "fig_regimes.pdf")

    reg = json.load(open(_find(root, "01_paper/statistics/pipeline_regimes_10seed.json",
                                     "statistics/pipeline_regimes_10seed.json")))["regimes"]
    keys = {"A": "A_gt_train_pred_test", "B": "B_matched_hard", "C": "C_matched_dilated"}

    h2h = json.load(open(_find(root, "01_paper/statistics/h2h_10seed_paired.json",
                                     "statistics/h2h_10seed_paired.json")))
    clf = sorted((r for r in h2h if "classifier" in r["arm"]), key=lambda r: r["seed"])
    clf_int = [r["int_acc"] for r in clf]
    clf_ext = [r["ext_acc"] for r in clf]

    fig, axes = plt.subplots(1, 2, figsize=(9.6, 4.7))
    mins = []
    for ax, field, cvals, title, sub in (
        (axes[0], "internal", clf_int, "Internal test set", "205 images"),
        (axes[1], "external", clf_ext, "Clean external set", "319 images"),
    ):
        series = {k: reg[v][field] for k, v in keys.items()}
        mins.append(panel(ax, series, cvals, title, sub))

    axes[0].set_ylabel("Accuracy (%)", fontsize=10)
    hi = max(max(clf_int), max(max(reg[v]["internal"]) for v in keys.values())) + 2.2
    for ax in axes:
        ax.set_ylim(min(mins) - 3.4, hi)

    fig.suptitle("Matching the mask source closes the internal gap. It does not close "
                 "the external one.", fontsize=11.5, y=0.985)
    fig.subplots_adjust(left=0.068, right=0.988, top=0.835, bottom=0.145, wspace=0.13)
    fig.savefig(out, format="pdf")
    fig.savefig(os.path.splitext(out)[0] + ".png", format="png", dpi=200)

    for k, v in keys.items():
        for field, cv in (("internal", clf_int), ("external", clf_ext)):
            a = np.asarray(cv, float)
            b = np.asarray(reg[v][field], float)
            print(f"{k} {field}: pipeline {b.mean():.2f}  diff {(a-b).mean():+.2f} "
                  f"p={stats.ttest_rel(a, b).pvalue:.3f}")
    print("wrote", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
