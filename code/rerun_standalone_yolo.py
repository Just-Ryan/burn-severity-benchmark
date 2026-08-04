#!/usr/bin/env python3
"""
Re-run the three-class standalone YOLOv8-seg model at the fair confidence
threshold (0.05) on both test sets, and archive the per-image predictions.

The manuscript's head-to-head table reports this arm at conf 0.05, but the only
archived evaluation was at the ultralytics default of 0.25. This script produces
the missing evidence. Whatever it returns is what the paper will report.

Per-image label = the majority severity class over the model's detections,
weighted by predicted mask area, matching how the pipeline arm is scored.
Images with no detection are counted as errors in a fixed denominator.
"""
import json
import os
import sys

import numpy as np
from ultralytics import YOLO

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
WEIGHTS = os.path.join(ROOT, "04_models/benchmark-checkpoints/yolov8x-seg_3class__best.pt")
INT_DIR = os.path.join(ROOT, "03_datasets/New-Way/CNN-Dataset-clean/unmasked/test")
EXT_DIR = os.path.join(ROOT, "03_datasets/external-test-clean/images")
RES = os.path.join(ROOT, "01_paper/benchmark2-proof/results")
OUT = os.path.join(RES, "standalone_yolo_conf005.json")
CONF = 0.05


def index_images(root):
    out = {}
    for dp, _, fs in os.walk(root):
        for f in fs:
            if f.lower().endswith((".jpg", ".jpeg", ".png")):
                out[f] = os.path.join(dp, f)
    return out


def majority_degree(res):
    """Area-weighted majority class over detections. None if nothing detected."""
    if res.masks is None or res.boxes is None or len(res.boxes) == 0:
        return None
    cls = res.boxes.cls.cpu().numpy().astype(int)
    md = res.masks.data.cpu().numpy()          # (n, H, W) binary
    areas = md.reshape(len(md), -1).sum(axis=1)
    if len(cls) != len(areas) or areas.sum() == 0:
        return int(np.bincount(cls).argmax())
    tot = {}
    for c, a in zip(cls, areas):
        tot[c] = tot.get(c, 0.0) + float(a)
    return int(max(tot, key=tot.get))


def balanced_accuracy(rows):
    per = {}
    for r in rows:
        t = r["true"]
        per.setdefault(t, [0, 0])
        per[t][1] += 1
        if r["pred"] == t:
            per[t][0] += 1
    return 100.0 * float(np.mean([c / n for c, n in per.values()]))


def run(name, preds_file, img_dir, model):
    truth = json.load(open(os.path.join(RES, preds_file)))
    index = index_images(img_dir)
    rows, missing = [], 0
    for i, t in enumerate(truth):
        p = index.get(t["img"])
        if p is None:
            missing += 1
            continue
        res = model.predict(p, conf=CONF, verbose=False)[0]
        d = majority_degree(res)
        rows.append({"img": t["img"], "true": t["true"],
                     "pred": -1 if d is None else d, "no_detection": d is None})
        if (i + 1) % 50 == 0:
            print(f"  {name}: {i+1}/{len(truth)}", file=sys.stderr)

    n = len(rows)
    correct = sum(1 for r in rows if r["pred"] == r["true"])
    nodet = sum(1 for r in rows if r["no_detection"])
    acc = 100.0 * correct / n
    bal = balanced_accuracy(rows)
    print(f"\n=== {name} (conf {CONF}) ===")
    print(f"  n={n}  correct={correct}  accuracy={acc:.2f}%  balanced={bal:.2f}%  "
          f"no-detection={nodet}  (images not found: {missing})")
    return {"n": n, "correct": correct, "acc": acc, "balanced_acc": bal,
            "no_detection": nodet, "conf": CONF, "rows": rows}


def main():
    print(f"weights: {WEIGHTS}")
    model = YOLO(WEIGHTS)
    out = {
        "note": "Three-class standalone YOLOv8-seg re-evaluated at the fair "
                "confidence threshold 0.05. Per-image label is the area-weighted "
                "majority severity class; no-detection counted as an error.",
        "weights": os.path.relpath(WEIGHTS, ROOT),
        "internal": run("internal", "preds_internal.json", INT_DIR, model),
        "external": run("external", "preds_external.json", EXT_DIR, model),
    }
    with open(OUT, "w") as fh:
        json.dump(out, fh, indent=1)
    print(f"\nwrote {OUT}")
    print("\nManuscript currently reports 79.5 internal / 68.7 external (bal. 74.6).")
    print("Archived conf-0.25 run gave 78.54 / 57.99 (bal. 65.47).")


if __name__ == "__main__":
    main()
