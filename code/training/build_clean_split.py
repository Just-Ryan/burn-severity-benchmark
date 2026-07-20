import os, glob, cv2, numpy as np
from collections import Counter, defaultdict
SEG="/Volumes/RayTOSHIBA/مشروع تخرج ١/03_datasets/New-Way/Seqmentation-Dataset/BIAC.v31i.yolov8_3Class"
OUT="clean_ds2"; rng=np.random.default_rng(42)
def sid(name): return name.split("_jpg.rf.")[0] if "_jpg.rf." in name else name.split(".rf.")[0]
items=[]
for sp in ["train","valid","test"]:
    for img in glob.glob(f"{SEG}/{sp}/images/*"):
        base=os.path.splitext(os.path.basename(img))[0]; lab=f"{SEG}/{sp}/labels/{base}.txt"
        if not os.path.exists(lab): continue
        cls=[int(l.split()[0]) for l in open(lab) if l.split()]
        if not cls: continue
        items.append((img,lab,sid(base),Counter(cls).most_common(1)[0][0]))
src_imgs=defaultdict(list)
for it in items: src_imgs[it[2]].append(it)
src_deg={s:Counter(x[3] for x in v).most_common(1)[0][0] for s,v in src_imgs.items()}
by=defaultdict(list)
for s,d in src_deg.items(): by[d].append(s)
split_of={}
for d,srcs in by.items():
    srcs=list(srcs); rng.shuffle(srcs); n=len(srcs); ntr=int(round(n*.70)); nva=int(round(n*.15))
    for i,s in enumerate(srcs): split_of[s]="train" if i<ntr else ("valid" if i<ntr+nva else "test")
def pmask(lp,w,h):
    m=np.zeros((h,w),np.uint8)
    for l in open(lp):
        p=l.split()
        if len(p)<7: continue
        pts=np.array([[float(p[i])*w,float(p[i+1])*h] for i in range(1,len(p)-1,2)],np.int32); cv2.fillPoly(m,[pts],1)
    return m
for v in ["masked","unmasked"]:
    for sp in ["train","valid","test"]:
        for d in [0,1,2]: os.makedirs(f"{OUT}/{v}/{sp}/{d}",exist_ok=True)
counts=defaultdict(lambda:defaultdict(int)); used=defaultdict(set)
for img,lab,s,deg in sorted(items,key=lambda x:x[0]):
    sp=split_of[s]
    if sp in ("valid","test"):
        if s in used[sp]: continue
        used[sp].add(s)
    bgr=cv2.imread(img)
    if bgr is None: continue
    base=os.path.splitext(os.path.basename(img))[0]
    cv2.imwrite(f"{OUT}/unmasked/{sp}/{deg}/{base}.jpg",bgr)
    h,w=bgr.shape[:2]; cv2.imwrite(f"{OUT}/masked/{sp}/{deg}/{base}.jpg", bgr*pmask(lab,w,h)[:,:,None])
    counts[sp][deg]+=1
for sp in ["train","valid","test"]:
    print(f"{sp}: {dict(counts[sp])} total {sum(counts[sp].values())}")
def ss(sp):
    s=set()
    for d in[0,1,2]:
        for fn in os.listdir(f"{OUT}/masked/{sp}/{d}"): s.add(sid(os.path.splitext(fn)[0]))
    return s
tr,va,te=ss("train"),ss("valid"),ss("test")
print(f"LEAKAGE: tr_te={len(tr&te)} tr_va={len(tr&va)} va_te={len(va&te)} | val 1-per-source: {sum(counts['valid'].values())==len(va)} test 1-per-source: {sum(counts['test'].values())==len(te)}")
