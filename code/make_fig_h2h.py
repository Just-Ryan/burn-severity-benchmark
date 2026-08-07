#!/usr/bin/env python3
"""Figure 3 — the ten-seed head-to-head, on both test sets.

The earlier version of this figure plotted three-seed means with standard-deviation
bars. That is the protocol the paper spends Section 4.7 arguing against, so the figure
contradicted the argument around it. This one plots all ten runs individually and
joins each seed to itself across the two arms, because the comparison is paired and
what matters is the per-seed difference rather than the overlap of two error bars.

Everything drawn here is recomputed from ``h2h_10seed_paired.json``; no number is
typed in except the single-seed standalone segmentation reference, which is read from
``segmentation_retrained_leakfree.json``.

Usage
-----
    python make_fig_h2h.py
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

CLF = "#3B6EA8"   # standalone classifier
PIPE = "#C4622D"  # two-stage pipeline
SEG = "#6b6b6b"   # all-in-one segmentation model



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



def arms(records):
    """Per-seed accuracy for each arm, ordered by seed so the pairing is real."""
    out = {}
    for r in records:
        out.setdefault(r["arm"], []).append(r)
    return {k: sorted(v, key=lambda r: r["seed"]) for k, v in out.items()}


def paired_stats(a: np.ndarray, b: np.ndarray) -> dict:
    """Classifier minus pipeline, with the interval and test the paper reports."""
    d = a - b
    n = len(d)
    mean = d.mean()
    sem = d.std(ddof=1) / np.sqrt(n)
    half = stats.t.ppf(0.975, n - 1) * sem
    return dict(mean=mean, lo=mean - half, hi=mean + half,
                p_t=stats.ttest_rel(a, b).pvalue,
                p_w=stats.wilcoxon(a, b, zero_method="pratt").pvalue,
                ahead=int((d > 0).sum()), n=n)


def panel(ax, clf, pipe, seg, title, subtitle):
    x_clf, x_pipe = 0.0, 1.0
    rng = np.random.default_rng(42)          # jitter only; never touches the values
    jit = rng.uniform(-0.045, 0.045, len(clf))

    # one faint line per seed: the pairing made visible
    for i in range(len(clf)):
        ax.plot([x_clf + jit[i], x_pipe + jit[i]], [clf[i], pipe[i]],
                color="#b9b9b9", lw=0.8, zorder=1, solid_capstyle="round")
    ax.scatter(x_clf + jit, clf, s=26, color=CLF, zorder=3,
               edgecolor="white", linewidth=0.6)
    ax.scatter(x_pipe + jit, pipe, s=26, color=PIPE, zorder=3,
               edgecolor="white", linewidth=0.6)

    # means, drawn wide so they read as the summary rather than as another point
    for x, vals, col in ((x_clf, clf, CLF), (x_pipe, pipe, PIPE)):
        ax.plot([x - 0.20, x + 0.20], [vals.mean()] * 2, color=col, lw=2.6, zorder=4)
        ax.annotate(f"{vals.mean():.2f}", (x + 0.215, vals.mean()), fontsize=9.5,
                    color=col, fontweight="bold", va="center", ha="left")

    ax.axhline(seg, color=SEG, lw=1.1, ls=(0, (5, 3)), zorder=2)
    ax.annotate(f"all-in-one YOLOv8-seg, single seed  {seg:.1f}", (-0.385, seg),
                fontsize=8, color=SEG, va="bottom", ha="left",
                bbox=dict(boxstyle="square,pad=0.15", fc="white", ec="none"))

    st = paired_stats(clf, pipe)
    ax.set_title(title, fontsize=11, pad=18)
    ax.text(0.5, 1.012, subtitle, transform=ax.transAxes, ha="center", va="bottom",
            fontsize=8.5, color="#555555")

    # The summary sits below the axes rather than inside them: with ten points per
    # arm and a reference line there is no interior space that is free in both panels.
    box = (f"paired difference  $+{st['mean']:.2f}$ pp,   "
           f"95% CI  $[{st['lo']:+.2f}, {st['hi']:+.2f}]$\n"
           f"$p={st['p_t']:.3f}$ (paired $t$),  {st['p_w']:.3f} (Wilcoxon);   "
           f"classifier ahead in {st['ahead']} of {st['n']} seeds")
    ax.text(0.5, -0.255, box, transform=ax.transAxes, ha="center", va="top",
            fontsize=8.4, linespacing=1.5,
            bbox=dict(boxstyle="round,pad=0.45", fc="#f6f6f6", ec="#d3d3d3", lw=0.7))

    ax.set_xlim(-0.42, 1.62)
    ax.set_xticks([x_clf, x_pipe])
    ax.set_xticklabels(["standalone\nclassifier", "two-stage\npipeline"], fontsize=9.5)
    ax.tick_params(axis="y", labelsize=9)
    ax.grid(axis="y", color="#e8e8e8", lw=0.7)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color("#999999")
    return st


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=os.path.join(os.path.dirname(__file__), "..", ".."))
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    root = os.path.abspath(args.repo_root)
    out = args.out or _out_default(root, "head_to_head.pdf")

    recs = json.load(open(_find(root, "01_paper/statistics/h2h_10seed_paired.json",
                                     "statistics/h2h_10seed_paired.json")))
    a = arms(recs)
    clf_key = next(k for k in a if "classifier" in k)
    pipe_key = next(k for k in a if "pipeline" in k)

    seg_int = json.load(open(_find(root, "01_paper/benchmark2-proof/results/standalone_yolo_leakfree.json",
                                         "benchmark2-proof/results/standalone_yolo_leakfree.json")))["acc"]
    seg_ext = json.load(open(_find(root, "01_paper/benchmark2-proof/results/standalone_yolo_leakfree_external.json",
                                         "benchmark2-proof/results/standalone_yolo_leakfree_external.json")))["acc"]

    fig, axes = plt.subplots(1, 2, figsize=(9.3, 4.9))
    stats_out = {}
    for ax, key, sv, title, sub in (
        (axes[0], "int_acc", seg_int, "Internal test set", "205 images, source-grouped split"),
        (axes[1], "ext_acc", seg_ext, "Clean external set", "319 images, perceptual-hash screened"),
    ):
        clf = np.array([r[key] for r in a[clf_key]])
        pipe = np.array([r[key] for r in a[pipe_key]])
        stats_out[key] = panel(ax, clf, pipe, sv, title, sub)

    axes[0].set_ylabel("Accuracy (%)", fontsize=10)
    lo = min(seg_ext, min(r["ext_acc"] for r in recs)) - 3
    hi = max(r["int_acc"] for r in recs) + 2.5
    for ax in axes:
        ax.set_ylim(lo, hi)

    fig.suptitle("Ten training runs per arm, evaluated on both test sets",
                 fontsize=12, y=0.985)
    fig.subplots_adjust(left=0.070, right=0.985, top=0.860, bottom=0.305, wspace=0.14)
    fig.savefig(out, format="pdf")
    fig.savefig(os.path.splitext(out)[0] + ".png", format="png", dpi=200)

    for k, v in stats_out.items():
        print(f"{k}: +{v['mean']:.2f} [{v['lo']:+.2f},{v['hi']:+.2f}] "
              f"p_t={v['p_t']:.4f} p_w={v['p_w']:.4f} ahead {v['ahead']}/{v['n']}")
    print("wrote", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
