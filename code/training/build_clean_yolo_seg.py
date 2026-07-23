"""
Build leak-free YOLOv8-seg datasets (1-class localiser + 3-class classifier) from the
SAME source-grouped split (seed 42) used for the classifier benchmark, so the pipeline
localiser, the standalone 3-class YOLO, and the classifiers all share identical folds and
test images. Val/test are deduplicated to one image per source (matching the classifiers).
  1class : all labels -> class 0 ('Burn')          (pipeline localiser)
  3class : original labels 0/1/2 (Degree1/2/3)      (standalone YOLO baseline)
"""
import os, glob, shutil
import numpy as np
from collections import Counter, defaultdict

SEG = "/Volumes/RayTOSHIBA/مشروع تخرج ١/03_datasets/New-Way/Seqmentation-Dataset/BIAC.v31i.yolov8_3Class"
OUT = os.environ.get("OUT_DIR", "/private/tmp/claude-501/-Volumes-RayTOSHIBA-------------/ceac3eb8-5ae5-4670-a589-4829e125cc74/scratchpad/yolo_seg_clean")
rng = np.random.default_rng(42)

def sid(name):
    return name.split("_jpg.rf.")[0] if "_jpg.rf." in name else name.split(".rf.")[0]

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

# identical source-grouped 70/15/15 split (seed 42)
src_deg = {}
for it in items:
    src_deg.setdefault(it[2], []).append(it[3])
src_deg = {s: Counter(v).most_common(1)[0][0] for s, v in src_deg.items()}
by = defaultdict(list)
for s, d in src_deg.items():
    by[d].append(s)
split_of = {}
for d, srcs in by.items():
    srcs = list(srcs); rng.shuffle(srcs)
    n = len(srcs); ntr = int(round(n*.70)); nva = int(round(n*.15))
    for i, s in enumerate(srcs):
        split_of[s] = "train" if i < ntr else ("valid" if i < ntr+nva else "test")

SPLITMAP = {"train": "train", "valid": "valid", "test": "test"}
for variant in ["1class", "3class"]:
    for sp in ["train", "valid", "test"]:
        os.makedirs(f"{OUT}/{variant}/{sp}/images", exist_ok=True)
        os.makedirs(f"{OUT}/{variant}/{sp}/labels", exist_ok=True)

counts = defaultdict(int); used = defaultdict(set)
for img, lab, s, deg in sorted(items, key=lambda x: x[0]):
    sp = split_of[s]
    if sp in ("valid", "test"):
        if s in used[sp]:
            continue
        used[sp].add(s)
    base = os.path.basename(img)
    labname = os.path.splitext(base)[0] + ".txt"
    lines = [l for l in open(lab) if l.split()]
    for variant in ["1class", "3class"]:
        shutil.copy(img, f"{OUT}/{variant}/{sp}/images/{base}")
        if variant == "1class":
            out = ["0 " + " ".join(l.split()[1:]) + "\n" for l in lines]
        else:
            out = [l if l.endswith("\n") else l+"\n" for l in lines]
        open(f"{OUT}/{variant}/{sp}/labels/{labname}", "w").writelines(out)
    counts[sp] += 1

# data.yaml for each (path filled at train time on Kaggle)
for variant, nc, names in [("1class", 1, ["Burn"]), ("3class", 3, ["Degree1", "Degree2", "Degree3"])]:
    with open(f"{OUT}/{variant}/data.yaml", "w") as f:
        f.write(f"path: .\ntrain: train/images\nval: valid/images\ntest: test/images\nnc: {nc}\nnames: {names}\n")

print("images per split:", dict(counts))
def srcs(sp, v="3class"):
    S = set()
    for fn in os.listdir(f"{OUT}/{v}/{sp}/images"):
        S.add(sid(os.path.splitext(fn)[0]))
    return S
tr, va, te = srcs("train"), srcs("valid"), srcs("test")
print(f"LEAKAGE tr_te={len(tr&te)} tr_va={len(tr&va)} va_te={len(va&te)} | "
      f"val 1/src={counts['valid']==len(va)} test 1/src={counts['test']==len(te)}")
# verify 1class and 3class share identical images per split
ok = all(set(os.listdir(f"{OUT}/1class/{sp}/images")) == set(os.listdir(f"{OUT}/3class/{sp}/images"))
         for sp in ["train", "valid", "test"])
print("1class and 3class share identical images per split:", ok)
