#!/usr/bin/env python3
"""Figure 4 — qualitative behaviour of the deployed two-stage pipeline.

Three rows (input / predicted burn region / masked input to the classifier) by four
columns: one correctly graded example per severity class, plus one representative
failure. Every panel is a held-out internal test image; nothing here is cherry-picked
from training data.

The four columns are pinned by file name rather than re-selected on each run, so the
figure is reproducible from the committed weights. Their pipeline predictions are
asserted against ``preds_internal.json`` — the same per-image file that
``verify_paper_numbers.py`` reads — so the figure cannot silently drift from the
numbers in the tables.

Usage
-----
    python make_fig_qualitative.py --repo-root .. --out ../../01_paper/melba/fig_qualitative.pdf
"""

from __future__ import annotations

import argparse
import json
import os
import sys

import cv2
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from ultralytics import YOLO

# --- the four pinned examples -------------------------------------------------
# (file name, true class, predicted class, column heading)
CLASSES = ("1st", "2nd", "3rd")
COLUMNS = [
    ("1-176-_jpg.rf.9b0c205c71be2d6649216dc33407f007.jpg", 0, 0),
    ("2-142-_jpg.rf.b43af00635702afd10f6a8f2adb32815.jpg", 1, 1),
    ("3-326-_jpg.rf.1ba1389ec69751b31bc44b2fc2aa6e46.jpg", 2, 2),
    ("2-194-_jpg.rf.add2cc7746fafae15ccbdeb7c5e19705.jpg", 1, 0),  # under-graded
]

ROW_LABELS = ("Input", "Predicted burn region", "Masked input to classifier")
OK, BAD = "#1a7a3c", "#b3261e"
CONF = 0.05  # deployment threshold: the localiser is run exactly as it is served



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



def trim_and_crop(rgb: np.ndarray, mask: np.ndarray, aspect: float = 4 / 3):
    """Drop uniform letterbox borders, then centre-crop to a common aspect ratio.

    Several images in the collection are padded to square with flat white or black
    bars. Left in place those bars dominate the panel and, because the panels then
    differ in shape, the grid cannot be packed tightly. Image and mask are cropped
    identically so the overlay stays registered.
    """
    h, w = rgb.shape[:2]
    flat = rgb.reshape(h, w, 3)
    # a border row/column is uniform and either near-white or near-black
    def uniform(line: np.ndarray) -> bool:
        return line.std() < 4.0 and (line.mean() > 244 or line.mean() < 11)

    top, bot, left, right = 0, h, 0, w
    while top < bot - 8 and uniform(flat[top]):
        top += 1
    while bot > top + 8 and uniform(flat[bot - 1]):
        bot -= 1
    while left < right - 8 and uniform(flat[:, left]):
        left += 1
    while right > left + 8 and uniform(flat[:, right - 1]):
        right -= 1
    rgb, mask = rgb[top:bot, left:right], mask[top:bot, left:right]

    # Too wide: crop, anchored on the predicted region rather than the geometric
    # centre, so an off-centre lesion is not cut in half. Too tall: never crop — a
    # tall frame is usually a whole limb, and cropping it to shape would discard the
    # very context the panel is there to show. Those are letterboxed instead, by
    # pad_to_aspect, once each row has been rendered.
    h, w = rgb.shape[:2]
    if w / h > aspect:
        xs = np.nonzero(mask)[1]
        cx = int(xs.mean()) if xs.size else w // 2
        nw = int(round(h * aspect))
        x0 = int(np.clip(cx - nw // 2, 0, w - nw))
        rgb, mask = rgb[:, x0:x0 + nw], mask[:, x0:x0 + nw]
    return rgb, mask


def pad_to_aspect(img: np.ndarray, aspect: float, colour: int) -> np.ndarray:
    """Letterbox a too-tall panel to the grid's aspect ratio."""
    h, w = img.shape[:2]
    if w / h >= aspect:
        return img
    nw = int(round(h * aspect))
    pad = nw - w
    l, r = pad // 2, pad - pad // 2
    return np.pad(img, ((0, 0), (l, r), (0, 0)), constant_values=colour)


def load_mask(model: YOLO, path: str, shape: tuple[int, int]) -> np.ndarray:
    """Union of the localiser's predicted instances, at full image resolution.

    Mirrors the deployed robust pipeline: on no detection the whole frame is passed
    through rather than raising, so the classifier always receives an image.
    """
    h, w = shape
    res = model.predict(path, conf=CONF, verbose=False)[0]
    if res.masks is None or len(res.masks.data) == 0:
        return np.ones((h, w), np.uint8)
    m = res.masks.data.cpu().numpy().max(axis=0)
    return (cv2.resize(m, (w, h), interpolation=cv2.INTER_NEAREST) > 0.5).astype(np.uint8)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=os.path.join(os.path.dirname(__file__), "..", ".."))
    ap.add_argument("--weights", default=None, help="1-class localiser checkpoint")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    root = os.path.abspath(args.repo_root)
    weights = args.weights or os.path.join(root, "04_models", "production", "yolov8x-seg_1class__best.pt")
    out = args.out or _out_default(root, "fig_qualitative.pdf")
    preds_path = _find(root, "01_paper/benchmark2-proof/results/preds_internal.json",
                             "benchmark2-proof/results/preds_internal.json")
    test_root = os.path.join(root, "03_datasets", "New-Way", "CNN-Dataset-clean", "unmasked", "test")

    # index the held-out test images by file name
    index = {}
    for dirpath, _, files in os.walk(test_root):
        for f in files:
            if f.lower().endswith((".jpg", ".jpeg", ".png")):
                index[f] = os.path.join(dirpath, f)

    preds = {r["img"]: r for r in json.load(open(preds_path))}

    # every panel must agree with the per-image predictions behind the tables
    for name, true, pipe in COLUMNS:
        if name not in index:
            sys.exit(f"not in the internal test set: {name}")
        rec = preds[name]
        if (rec["true"], rec["pipe"]) != (true, pipe):
            sys.exit(f"{name}: figure claims true={true} pipe={pipe}, "
                     f"preds_internal.json has true={rec['true']} pipe={rec['pipe']}")

    model = YOLO(weights)

    fig, axes = plt.subplots(3, 4, figsize=(9.6, 6.0))
    fig.suptitle("Two-stage pipeline on held-out test images:  localise $\\rightarrow$ mask "
                 "$\\rightarrow$ classify", fontsize=11.5, y=0.985)

    for col, (name, true, pipe) in enumerate(COLUMNS):
        path = index[name]
        bgr = cv2.imread(path)
        rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
        mask = load_mask(model, path, rgb.shape[:2])
        rgb, mask = trim_and_crop(rgb, mask)

        # middle row: dim everything outside the prediction and outline the boundary,
        # so the predicted region is legible at print size rather than a near-copy
        # of the input.
        dim = (rgb * 0.30 + 255 * 0.06).astype(np.uint8)
        overlay = np.where(mask[..., None].astype(bool), rgb, dim)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        edge = max(2, int(round(0.004 * max(rgb.shape[:2]))))
        cv2.drawContours(overlay, contours, -1, (255, 214, 10), edge, lineType=cv2.LINE_AA)

        masked = rgb * mask[..., None]

        correct = true == pipe
        colour = OK if correct else BAD
        axes[0, col].set_title(
            f"true {CLASSES[true]}  $\\rightarrow$  predicted {CLASSES[pipe]}",
            fontsize=10, color=colour, fontweight="normal" if correct else "bold", pad=7)

        panels = (pad_to_aspect(rgb, 4 / 3, 255),
                  pad_to_aspect(overlay, 4 / 3, 255),
                  pad_to_aspect(masked, 4 / 3, 0))

        for row, img in enumerate(panels):
            ax = axes[row, col]
            ax.imshow(img)
            ax.set_xticks([]); ax.set_yticks([])
            for s in ax.spines.values():
                s.set_edgecolor(colour if not correct else "#cccccc")
                s.set_linewidth(1.6 if not correct else 0.6)
            if col == 0:
                ax.set_ylabel(ROW_LABELS[row], fontsize=9.5)

        if not correct:
            axes[0, col].text(0.5, 0.955, "UNDER-GRADED", transform=axes[0, col].transAxes,
                              ha="center", va="top", fontsize=8.5, color="white",
                              fontweight="bold",
                              bbox=dict(boxstyle="square,pad=0.32", fc=BAD, ec="none"))

    fig.subplots_adjust(left=0.042, right=0.996, top=0.895, bottom=0.006,
                        wspace=0.030, hspace=0.045)
    fig.savefig(out, format="pdf", dpi=300)
    png = os.path.splitext(out)[0] + ".png"
    fig.savefig(png, format="png", dpi=200)
    print("wrote", out)
    print("wrote", png)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
