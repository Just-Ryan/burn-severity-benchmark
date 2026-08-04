#!/usr/bin/env python3
"""
Rebuild the YOLO segmentation datasets on the SAME source-grouped split as the
classifiers, fixing the leak reported in Section 4.11 of the manuscript.

The original segmentation datasets used the collection's distribution-supplied
split. That split disagrees with the leak-free classifier split: 179 of the 205
internal classification test images (87.3 percent) sat in the segmentation
models' training or validation folds.

This script re-partitions the identical images and labels so that:
  - the segmentation TEST fold is exactly the 205-image classification test set,
  - the segmentation VAL fold is exactly the 206-image classification val set,
  - training keeps every augmented copy of every training-fold source, and
  - no source photograph appears in more than one fold.

It then verifies all of that and refuses to write a dataset that still leaks.

    python build_seg_split_leakfree.py
"""
import json
import os
import shutil
import sys
from collections import defaultdict

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
SEG = os.path.join(ROOT, "03_datasets/New-Way/Seqmentation-Dataset")
CLEAN = os.path.join(ROOT, "03_datasets/New-Way/CNN-Dataset-clean/unmasked")
OUT = os.path.join(ROOT, "03_datasets/seg-leakfree")

VARIANTS = {
    "1class": ("BIAC.v31i.yolov8_1Class", 1, ["burn"]),
    "3class": ("BIAC.v31i.yolov8_3Class", 3, ["first_degree", "second_degree", "third_degree"]),
}


def sid(name):
    """Roboflow encodes the source photograph before the _jpg.rf. marker."""
    return name.split("_jpg.rf.")[0] if "_jpg.rf." in name else name.rsplit(".", 1)[0]


def listing(root):
    out = {}
    for dp, _, fs in os.walk(root):
        for f in fs:
            if f.lower().endswith((".jpg", ".jpeg", ".png")):
                out[f] = os.path.join(dp, f)
    return out


def main():
    # --- the authoritative split, taken from the leak-free classifier folders ---
    fold_images = {sp: set(listing(os.path.join(CLEAN, sp))) for sp in ("train", "valid", "test")}
    fold_sources = {sp: {sid(f) for f in imgs} for sp, imgs in fold_images.items()}
    print("leak-free classifier split (the authority):")
    for sp in ("train", "valid", "test"):
        print(f"  {sp:6}: {len(fold_images[sp]):5} images, {len(fold_sources[sp]):4} sources")

    overlap = (fold_sources["train"] & fold_sources["valid"]) | \
              (fold_sources["train"] & fold_sources["test"]) | \
              (fold_sources["valid"] & fold_sources["test"])
    if overlap:
        sys.exit(f"FATAL: the classifier split itself shares {len(overlap)} sources between folds")
    print("  no source appears in two folds. OK\n")

    src_fold = {}
    for sp in ("train", "valid", "test"):
        for s in fold_sources[sp]:
            src_fold[s] = sp

    for key, (subdir, nc, names) in VARIANTS.items():
        src_root = os.path.join(SEG, subdir)
        dst_root = os.path.join(OUT, key)
        print(f"=== {key} ===")
        all_imgs = listing(src_root)
        print(f"  segmentation pool: {len(all_imgs)} images, "
              f"{len({sid(f) for f in all_imgs})} sources")

        counts = defaultdict(int)
        unassigned = 0
        for sp in ("train", "valid", "test"):
            os.makedirs(os.path.join(dst_root, sp, "images"), exist_ok=True)
            os.makedirs(os.path.join(dst_root, sp, "labels"), exist_ok=True)

        for fname, path in sorted(all_imgs.items()):
            fold = src_fold.get(sid(fname))
            if fold is None:
                unassigned += 1
                continue
            # val and test are deduplicated to exactly the classifier's images,
            # so the segmentation test fold IS the classification test fold.
            if fold in ("valid", "test") and fname not in fold_images[fold]:
                continue
            lbl = os.path.join(os.path.dirname(os.path.dirname(path)), "labels",
                               os.path.splitext(fname)[0] + ".txt")
            if not os.path.exists(lbl):
                continue
            shutil.copy2(path, os.path.join(dst_root, fold, "images", fname))
            shutil.copy2(lbl, os.path.join(dst_root, fold, "labels",
                                           os.path.splitext(fname)[0] + ".txt"))
            counts[fold] += 1

        for sp in ("train", "valid", "test"):
            print(f"  {sp:6}: {counts[sp]:5} images")
        if unassigned:
            print(f"  {unassigned} images had no fold assignment (not in the clean split); dropped")

        # ---- verify, and refuse to ship a leaking dataset ----
        got = {sp: set(os.listdir(os.path.join(dst_root, sp, "images"))) for sp in
               ("train", "valid", "test")}
        gsrc = {sp: {sid(f) for f in got[sp]} for sp in got}
        bad = (gsrc["train"] & gsrc["valid"]) | (gsrc["train"] & gsrc["test"]) | \
              (gsrc["valid"] & gsrc["test"])
        if bad:
            sys.exit(f"FATAL: rebuilt {key} still shares {len(bad)} sources across folds")
        missing = fold_images["test"] - got["test"]
        print(f"  source overlap between folds: 0  OK")
        print(f"  test fold == the 205 classification test images: "
              f"{len(got['test'])}/205 present, {len(missing)} missing")

        with open(os.path.join(dst_root, "data.yaml"), "w") as fh:
            fh.write("path: .\ntrain: train/images\nval: valid/images\ntest: test/images\n\n")
            fh.write(f"nc: {nc}\nnames: {names}\n")
        print(f"  wrote {dst_root}/data.yaml\n")

    print(f"done -> {OUT}")


if __name__ == "__main__":
    main()
