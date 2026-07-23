"""
Build the leak-free, source-grouped split in FOUR matched input conditions, so the
"does focusing on the burn help?" hypothesis gets a fair, complete test:

  unmasked      : full image (baseline)
  masked        : image x polygon mask (background -> black); the deployed pipeline
  cropped       : full image cropped tightly to the burn bounding box (zoom in, keeps local context)
  maskedcrop    : masked image cropped to the burn bounding box (both)

All four are derived from the SAME source-grouped 70/15/15 split (seed 42) with
validation/test deduplicated to one image per source, so every condition sees the
identical images and the comparison is matched and leak-free.
"""
import os, glob, cv2, numpy as np
from collections import Counter, defaultdict

SEG = "/Volumes/RayTOSHIBA/مشروع تخرج ١/03_datasets/New-Way/Seqmentation-Dataset/BIAC.v31i.yolov8_3Class"
OUT = os.environ.get("OUT_DIR", "/private/tmp/claude-501/-Volumes-RayTOSHIBA-------------/ceac3eb8-5ae5-4670-a589-4829e125cc74/scratchpad/clean_ds4")
PAD = 0.15  # bbox padding fraction
VARIANTS = ["unmasked", "masked", "cropped", "maskedcrop"]
rng = np.random.default_rng(42)

def sid(name):
    return name.split("_jpg.rf.")[0] if "_jpg.rf." in name else name.split(".rf.")[0]

# --- gather items (image, label, source-id, majority-degree) ---
items = []
for sp in ["train", "valid", "test"]:
    for img in glob.glob(f"{SEG}/{sp}/images/*"):
        base = os.path.splitext(os.path.basename(img))[0]
        lab = f"{SEG}/{sp}/labels/{base}.txt"
        if not os.path.exists(lab):
            continue
        cls = [int(l.split()[0]) for l in open(lab) if l.split()]
        if not cls:
            continue
        items.append((img, lab, sid(base), Counter(cls).most_common(1)[0][0]))

# --- source-grouped stratified 70/15/15 split (seed 42), identical to v1 ---
src_imgs = defaultdict(list)
for it in items:
    src_imgs[it[2]].append(it)
src_deg = {s: Counter(x[3] for x in v).most_common(1)[0][0] for s, v in src_imgs.items()}
by = defaultdict(list)
for s, d in src_deg.items():
    by[d].append(s)
split_of = {}
for d, srcs in by.items():
    srcs = list(srcs); rng.shuffle(srcs)
    n = len(srcs); ntr = int(round(n*.70)); nva = int(round(n*.15))
    for i, s in enumerate(srcs):
        split_of[s] = "train" if i < ntr else ("valid" if i < ntr+nva else "test")

def polys(lp, w, h):
    out = []
    for l in open(lp):
        p = l.split()
        if len(p) < 7:
            continue
        pts = np.array([[float(p[i])*w, float(p[i+1])*h] for i in range(1, len(p)-1, 2)], np.int32)
        out.append(pts)
    return out

def mask_of(pl, w, h):
    m = np.zeros((h, w), np.uint8)
    for pts in pl:
        cv2.fillPoly(m, [pts], 1)
    return m

def bbox_of(pl, w, h):
    allpts = np.vstack(pl)
    x0, y0 = allpts[:, 0].min(), allpts[:, 1].min()
    x1, y1 = allpts[:, 0].max(), allpts[:, 1].max()
    bw, bh = x1-x0, y1-y0
    x0 = int(max(0, x0 - PAD*bw)); y0 = int(max(0, y0 - PAD*bh))
    x1 = int(min(w, x1 + PAD*bw)); y1 = int(min(h, y1 + PAD*bh))
    if x1-x0 < 8 or y1-y0 < 8:   # guard tiny boxes
        return 0, 0, w, h
    return x0, y0, x1, y1

for v in VARIANTS:
    for sp in ["train", "valid", "test"]:
        for d in [0, 1, 2]:
            os.makedirs(f"{OUT}/{v}/{sp}/{d}", exist_ok=True)

counts = defaultdict(lambda: defaultdict(int)); used = defaultdict(set)
for img, lab, s, deg in sorted(items, key=lambda x: x[0]):
    sp = split_of[s]
    if sp in ("valid", "test"):
        if s in used[sp]:
            continue
        used[sp].add(s)
    bgr = cv2.imread(img)
    if bgr is None:
        continue
    base = os.path.splitext(os.path.basename(img))[0]
    h, w = bgr.shape[:2]
    pl = polys(lab, w, h)
    if not pl:
        continue
    m = mask_of(pl, w, h)
    masked = bgr * m[:, :, None]
    x0, y0, x1, y1 = bbox_of(pl, w, h)
    cv2.imwrite(f"{OUT}/unmasked/{sp}/{deg}/{base}.jpg", bgr)
    cv2.imwrite(f"{OUT}/masked/{sp}/{deg}/{base}.jpg", masked)
    cv2.imwrite(f"{OUT}/cropped/{sp}/{deg}/{base}.jpg", bgr[y0:y1, x0:x1])
    cv2.imwrite(f"{OUT}/maskedcrop/{sp}/{deg}/{base}.jpg", masked[y0:y1, x0:x1])
    counts[sp][deg] += 1

for sp in ["train", "valid", "test"]:
    print(f"{sp}: {dict(counts[sp])} total {sum(counts[sp].values())}")

def ss(sp, v="masked"):
    s = set()
    for d in [0, 1, 2]:
        for fn in os.listdir(f"{OUT}/{v}/{sp}/{d}"):
            s.add(sid(os.path.splitext(fn)[0]))
    return s
tr, va, te = ss("train"), ss("valid"), ss("test")
print(f"LEAKAGE: tr_te={len(tr&te)} tr_va={len(tr&va)} va_te={len(va&te)} | "
      f"val 1-per-source={sum(counts['valid'].values())==len(va)} test 1-per-source={sum(counts['test'].values())==len(te)}")
# verify all four variants have identical filenames per split/class
import filecmp
ok = True
for sp in ["train", "valid", "test"]:
    for d in [0, 1, 2]:
        ref = set(os.listdir(f"{OUT}/unmasked/{sp}/{d}"))
        for v in VARIANTS[1:]:
            if set(os.listdir(f"{OUT}/{v}/{sp}/{d}")) != ref:
                ok = False
print("all four variants have identical filename sets per split/class:", ok)
