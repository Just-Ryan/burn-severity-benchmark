#!/usr/bin/env python3
"""
Exploratory skin-tone probe for the burn-severity benchmark.

Estimates apparent skin tone from *perilesional* (non-burn) skin pixels using the
Individual Typology Angle (ITA), then crosses it with per-image correctness of the
standalone classifier and the two-stage pipeline.

    python skin_tone_probe.py

WHAT THIS IS NOT
----------------
ITA computed from uncontrolled web photographs is a proxy for *apparent skin tone in
the image*, not a measurement of a patient's constitutive skin phototype. White
balance, illumination, camera processing and perilesional erythema all shift it, and
this dataset carries no ground-truth skin-type labels. Treat every number here as
exploratory and hypothesis-generating, never as a fairness audit of a deployed system.

METHOD
------
1. Burn region excluded per image:
     internal  - from the ground-truth masked/unmasked image pair
     external  - by rasterising the YOLO polygon annotations
   The exclusion is dilated so the burn margin does not contaminate the skin sample.
2. Skin pixels selected from the remaining region by a conjunction of the standard
   RGB and YCbCr skin rules (Kovac et al.; Chai and Ngan).
3. sRGB -> CIE L*a*b* (D65), ITA = arctan((L* - 50) / b*) * 180/pi, median over skin
   pixels. Images with fewer than MIN_SKIN_PX skin pixels are reported as
   indeterminate and excluded from the ITA analysis rather than guessed at.
4. Accuracy per ITA bin with Wilson 95% intervals; association tested on the
   continuous ITA (Mann-Whitney, correct vs incorrect) so the result does not depend
   on where the bin edges fall.
"""
import json
import os
import sys
from collections import defaultdict

import numpy as np
from PIL import Image, ImageDraw
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))

INT_UNMASKED = os.path.join(ROOT, "03_datasets/New-Way/CNN-Dataset-clean/unmasked/test")
INT_MASKED = os.path.join(ROOT, "03_datasets/New-Way/CNN-Dataset-clean/masked/test")
EXT_IMAGES = os.path.join(ROOT, "03_datasets/external-test-clean/images")
EXT_LABELS = os.path.join(ROOT, "03_datasets/external-test-clean/labels")
RESULTS = os.path.join(ROOT, "01_paper/benchmark2-proof/results")
OUT = os.path.join(ROOT, "01_paper/statistics/skin_tone_ITA_probe.json")

MIN_SKIN_PX = 500      # below this the ITA median is too noisy to use
DILATE_ITER = 6        # burn-margin exclusion, in pixels
MAX_SIDE = 512         # downscale for speed; ITA is a colour statistic, not a spatial one

# Standard ITA bands (Chardon et al. 1991; as used in the dermatology literature)
BANDS = [
    ("very light", 55, 1e9),
    ("light", 41, 55),
    ("intermediate", 28, 41),
    ("tan", 10, 28),
    ("brown", -30, 10),
    ("dark", -1e9, -30),
]


# ------------------------------------------------------------------ colour
def srgb_to_lab(rgb):
    """rgb: float array in [0,1], shape (...,3) -> CIE L*a*b* under D65."""
    m = rgb <= 0.04045
    lin = np.where(m, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)
    mat = np.array([[0.4124564, 0.3575761, 0.1804375],
                    [0.2126729, 0.7151522, 0.0721750],
                    [0.0193339, 0.1191920, 0.9503041]])
    xyz = lin @ mat.T
    white = np.array([0.95047, 1.00000, 1.08883])
    t = xyz / white
    d = 6.0 / 29.0
    f = np.where(t > d ** 3, np.cbrt(t), t / (3 * d * d) + 4.0 / 29.0)
    L = 116 * f[..., 1] - 16
    a = 500 * (f[..., 0] - f[..., 1])
    b = 200 * (f[..., 1] - f[..., 2])
    return L, a, b


def skin_mask(arr8):
    """Conjunction of the RGB (Kovac) and YCbCr (Chai & Ngan) skin rules."""
    R = arr8[..., 0].astype(np.int16)
    G = arr8[..., 1].astype(np.int16)
    B = arr8[..., 2].astype(np.int16)
    mx = np.maximum(np.maximum(R, G), B)
    mn = np.minimum(np.minimum(R, G), B)
    rgb_rule = ((R > 95) & (G > 40) & (B > 20) & ((mx - mn) > 15)
                & (np.abs(R - G) > 15) & (R > G) & (R > B))
    Cb = 128 - 0.168736 * R - 0.331264 * G + 0.5 * B
    Cr = 128 + 0.5 * R - 0.418688 * G - 0.081312 * B
    ycc_rule = (Cb >= 77) & (Cb <= 127) & (Cr >= 133) & (Cr <= 173)
    return rgb_rule & ycc_rule


def dilate(mask, iters):
    """Binary dilation by repeated 4-neighbour OR. No scipy.ndimage dependency."""
    m = mask.copy()
    for _ in range(iters):
        p = np.zeros_like(m)
        p[1:, :] |= m[:-1, :]
        p[:-1, :] |= m[1:, :]
        p[:, 1:] |= m[:, :-1]
        p[:, :-1] |= m[:, 1:]
        m = m | p
    return m


def load_rgb(path):
    im = Image.open(path).convert("RGB")
    if max(im.size) > MAX_SIDE:
        s = MAX_SIDE / max(im.size)
        im = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.BILINEAR)
    return np.asarray(im)


def ita_for(arr8, burn):
    """Median ITA over non-burn skin pixels. Returns (ita, n_skin)."""
    region = ~dilate(burn, DILATE_ITER) if burn is not None else np.ones(arr8.shape[:2], bool)
    sel = skin_mask(arr8) & region
    n = int(sel.sum())
    if n < MIN_SKIN_PX:
        return None, n
    px = arr8[sel].astype(np.float64) / 255.0
    L, _, b = srgb_to_lab(px)
    ok = np.abs(b) > 1e-6
    if ok.sum() < MIN_SKIN_PX:
        return None, n
    ita = np.arctan((L[ok] - 50.0) / b[ok]) * 180.0 / np.pi
    return float(np.median(ita)), n


# ------------------------------------------------------------------ masks
def burn_from_pair(unmasked_path, masked_path, shape):
    """Internal set: the masked copy zeroes non-burn pixels, so burn = non-black."""
    m = Image.open(masked_path).convert("RGB")
    m = m.resize((shape[1], shape[0]), Image.NEAREST)
    a = np.asarray(m)
    return a.sum(axis=2) > 12


def burn_from_yolo(label_path, shape):
    """External set: rasterise the normalised YOLO polygons."""
    h, w = shape
    img = Image.new("1", (w, h), 0)
    d = ImageDraw.Draw(img)
    drew = False
    with open(label_path) as fh:
        for line in fh:
            p = line.split()
            if len(p) < 7:
                continue
            c = [float(x) for x in p[1:]]
            pts = [(c[i] * w, c[i + 1] * h) for i in range(0, len(c) - 1, 2)]
            if len(pts) >= 3:
                d.polygon(pts, fill=1)
                drew = True
    return np.asarray(img, bool) if drew else None


# ------------------------------------------------------------------ stats
def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (100 * max(0.0, c - h), 100 * min(1.0, c + h))


def band_of(ita):
    for name, lo, hi in BANDS:
        if lo <= ita < hi:
            return name
    return "unclassified"


def index_images(root):
    """filename -> path, walking class subfolders."""
    out = {}
    for dirpath, _, files in os.walk(root):
        for f in files:
            if f.lower().endswith((".jpg", ".jpeg", ".png")):
                out[f] = os.path.join(dirpath, f)
    return out


def run(name, preds, img_index, mask_fn):
    rows, missing, indet = [], 0, 0
    for i, r in enumerate(preds):
        path = img_index.get(r["img"])
        if path is None:
            missing += 1
            continue
        arr = load_rgb(path)
        burn = mask_fn(r["img"], path, arr.shape[:2])
        ita, nskin = ita_for(arr, burn)
        if ita is None:
            indet += 1
            continue
        rows.append({
            "img": r["img"], "ita": ita, "band": band_of(ita), "n_skin": nskin,
            "true": r["true"], "clf": r["clf"], "pipe": r["pipe"],
            "clf_ok": int(r["clf"] == r["true"]), "pipe_ok": int(r["pipe"] == r["true"]),
            # a burn can only be under-graded if it is not already the mildest class
            "could_under": int(r["true"] > 0),
            "pipe_under": int(r["true"] > 0 and r["pipe"] < r["true"]),
        })
        if (i + 1) % 50 == 0:
            print(f"    {name}: {i + 1}/{len(preds)}", file=sys.stderr)

    print(f"\n=== {name}: {len(rows)} images with a usable ITA "
          f"({indet} indeterminate, {missing} not found) ===")

    out = {"set": name, "n_used": len(rows), "n_indeterminate": indet,
           "n_missing": missing, "bands": {}, "rows": rows}

    for band, _, _ in BANDS:
        sub = [r for r in rows if r["band"] == band]
        if not sub:
            continue
        n = len(sub)
        kc = sum(r["clf_ok"] for r in sub)
        kp = sum(r["pipe_ok"] for r in sub)
        cu = sum(r["could_under"] for r in sub)
        pu = sum(r["pipe_under"] for r in sub)
        ci_c, ci_p = wilson(kc, n), wilson(kp, n)
        out["bands"][band] = {
            "n": n,
            "clf_acc": 100 * kc / n, "clf_ci": ci_c,
            "pipe_acc": 100 * kp / n, "pipe_ci": ci_p,
            "under_rate": (100 * pu / cu) if cu else None, "n_could_under": cu,
        }
        print(f"  {band:<13} n={n:>4}  clf {100*kc/n:5.1f}% [{ci_c[0]:.1f},{ci_c[1]:.1f}]"
              f"   pipe {100*kp/n:5.1f}% [{ci_p[0]:.1f},{ci_p[1]:.1f}]"
              + (f"   under {100*pu/cu:5.1f}% (n={cu})" if cu else ""))

    # Association on the continuous ITA, so nothing hinges on the bin edges.
    for arm in ("clf", "pipe"):
        a = [r["ita"] for r in rows if r[f"{arm}_ok"] == 1]
        b = [r["ita"] for r in rows if r[f"{arm}_ok"] == 0]
        if len(a) > 2 and len(b) > 2:
            u = stats.mannwhitneyu(a, b, alternative="two-sided")
            rb = 1 - 2 * u.statistic / (len(a) * len(b))   # rank-biserial correlation
            out[f"{arm}_ita_correct_median"] = float(np.median(a))
            out[f"{arm}_ita_wrong_median"] = float(np.median(b))
            out[f"{arm}_mannwhitney_p"] = float(u.pvalue)
            out[f"{arm}_rank_biserial"] = float(rb)
            print(f"  {arm}: median ITA correct {np.median(a):.1f} vs wrong {np.median(b):.1f}"
                  f"  Mann-Whitney p={u.pvalue:.3f}  rank-biserial r={rb:+.3f}")

    ita_all = [r["ita"] for r in rows]
    out["ita_median"] = float(np.median(ita_all))
    out["ita_iqr"] = [float(np.percentile(ita_all, 25)), float(np.percentile(ita_all, 75))]
    print(f"  ITA overall: median {np.median(ita_all):.1f}, "
          f"IQR [{np.percentile(ita_all,25):.1f}, {np.percentile(ita_all,75):.1f}]")
    return out


def main():
    results = {}

    print("Indexing images...", file=sys.stderr)
    int_un = index_images(INT_UNMASKED)
    int_ma = index_images(INT_MASKED)
    ext_im = index_images(EXT_IMAGES)

    preds_int = json.load(open(os.path.join(RESULTS, "preds_internal.json")))
    preds_ext = json.load(open(os.path.join(RESULTS, "preds_external.json")))

    def int_mask(fname, path, shape):
        mp = int_ma.get(fname)
        return burn_from_pair(path, mp, shape) if mp else None

    def ext_mask(fname, path, shape):
        lp = os.path.join(EXT_LABELS, os.path.splitext(fname)[0] + ".txt")
        return burn_from_yolo(lp, shape) if os.path.exists(lp) else None

    results["internal"] = run("internal", preds_int, int_un, int_mask)
    results["external"] = run("external", preds_ext, ext_im, ext_mask)

    results["method"] = {
        "ita": "arctan((L*-50)/b*) * 180/pi, median over non-burn skin pixels",
        "skin_rule": "conjunction of RGB (Kovac) and YCbCr (Chai & Ngan) rules",
        "burn_excluded": "internal: ground-truth masked/unmasked pair; "
                         "external: rasterised YOLO polygons; both dilated 6 px",
        "min_skin_px": MIN_SKIN_PX,
        "max_side": MAX_SIDE,
        "caveat": "ITA from uncontrolled web photographs is a proxy for apparent skin "
                  "tone in the image, not a measurement of constitutive phototype. "
                  "No ground-truth skin-type labels exist for this dataset. "
                  "Exploratory only.",
    }

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(results, fh, indent=1)
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    main()
