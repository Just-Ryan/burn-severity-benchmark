"""
External validation on the BIP_US database (Univ. of Seville, hospital burn photos, 2005).
94 images labeled by burn depth. Degree mapping:
  Superficial dermal -> Second (superficial partial thickness)
  Deep dermal        -> Second (deep partial thickness)   [also reported split out]
  Full-thickness     -> Third
No epidermal/1st-degree images -> this is a clean 2nd-vs-3rd OOD probe.
Runs the deployed pipeline (YOLOv8x-seg 1-class -> mask -> Swin-Small masked) and the
unmasked baseline, and reports predictions broken down by BIP_US depth subclass.
"""
import os, json, numpy as np, cv2, torch, timm
from PIL import Image
from torchvision import transforms
from ultralytics import YOLO
from sklearn.metrics import confusion_matrix, accuracy_score

ROOT = "/Volumes/RayTOSHIBA/مشروع تخرج ١"
BIP = "/private/tmp/claude-501/-Volumes-RayTOSHIBA-------------/ceac3eb8-5ae5-4670-a589-4829e125cc74/scratchpad/bipus_data/Burns_BIP_US_database"
CLASSES = ["First", "Second", "Third"]

# Ground-truth depth per image number (from README.pdf)
SUP = list(range(1,10))+[25,26,27,28,31,32,39,41,42,43,44,46,52,53,54,55,56,57,63,71,72,73,84,85,86,87,88,89,90,91,92,93,94]
DEEP= [10,11,12,13,14,22,23,24,29,30,34,35,36,37,38,48,49,50,51,65,66,67,68,69,70,77,78,79,80,81,82,83]
FULL= [15,16,17,18,19,20,21,33,40,45,47,58,59,60,61,62,64,74,75,76]
depth_of = {}
for n in SUP: depth_of[n]="Superficial dermal"
for n in DEEP: depth_of[n]="Deep dermal"
for n in FULL: depth_of[n]="Full-thickness"
# degree ground truth (deep dermal -> Second by default)
degree_of = {n:("Third" if depth_of[n]=="Full-thickness" else "Second") for n in depth_of}

TF = transforms.Compose([transforms.Resize(256), transforms.CenterCrop(224), transforms.ToTensor(),
                         transforms.Normalize([0.485,0.456,0.406],[0.229,0.224,0.225])])
def swin(ck):
    m=timm.create_model("swin_small_patch4_window7_224",pretrained=False,num_classes=3)
    m.load_state_dict(torch.load(ck,map_location="cpu",weights_only=False)); return m.eval()
yolo=YOLO(f"{ROOT}/04_models/production/yolov8x-seg_1class__best.pt")
mask_model=swin(f"{ROOT}/04_models/production/swin-small_masked__best_cnn_mask.pth")
full_model=swin(f"{ROOT}/04_models/benchmark-checkpoints/swin-small_unmasked__best_cnn_full.pth")
def ymask(bgr):
    r=yolo(bgr,imgsz=640,verbose=False)[0]
    if r.masks is None or len(r.boxes)==0: return None
    c=r.boxes.conf.cpu().numpy(); mk=r.masks.data[int(np.argmax(c))].cpu().numpy()
    rgb=cv2.cvtColor(bgr,cv2.COLOR_BGR2RGB); mk=cv2.resize(mk,(rgb.shape[1],rgb.shape[0]))
    return rgb*(mk>0.1).astype(np.uint8)[:,:,None]
@torch.no_grad()
def cls(m,rgb): return CLASSES[int(m(TF(Image.fromarray(rgb.astype(np.uint8))).unsqueeze(0)).argmax(1))]

# locate every image file 1..94
files={}
for sub in ["Training set","Testing set"]:
    d=os.path.join(BIP,sub)
    for fn in os.listdir(d):
        if fn.lower().endswith((".jpg",".bmp")):
            num=int(os.path.splitext(fn)[0])
            files[num]=os.path.join(d,fn)

rows=[]; segok=0
for n in sorted(files):
    bgr=cv2.imread(files[n])
    if bgr is None: continue
    rgb=cv2.cvtColor(bgr,cv2.COLOR_BGR2RGB)
    m=ymask(bgr); ok=m is not None
    if ok: segok+=1
    else: m=rgb
    rows.append({"num":n,"depth":depth_of[n],"degree_gt":degree_of[n],
                 "pred_pipeline":cls(mask_model,m),"pred_unmasked":cls(full_model,rgb),"seg_ok":ok})

def summarize(rows,key):
    # 2nd-vs-3rd accuracy (map any First prediction as wrong)
    yt=[r["degree_gt"] for r in rows]; yp=[r[key] for r in rows]
    acc=np.mean([a==b for a,b in zip(yt,yp)])
    lab=["First","Second","Third"]
    cm=confusion_matrix(yt,yp,labels=lab)
    print(f"\n== {key} ==  2nd-vs-3rd accuracy = {acc*100:.1f}%  (N={len(rows)})")
    print("   rows=GT(Second/Third), cols=pred(First/Second/Third):")
    for i,l in enumerate(lab):
        if l in yt: print(f"     {l:7s}: {cm[i].tolist()}")
    # per depth subclass: what does the model predict?
    for depth in ["Superficial dermal","Deep dermal","Full-thickness"]:
        sub=[r for r in rows if r["depth"]==depth]
        from collections import Counter
        c=Counter(r[key] for r in sub)
        print(f"     {depth:20s} (n={len(sub)}): {dict(c)}")
    return acc

print(f"BIP_US external validation — {len(rows)} images, seg success {segok}/{len(rows)} = {segok/len(rows)*100:.0f}%")
acc_pipe=summarize(rows,"pred_pipeline")
acc_base=summarize(rows,"pred_unmasked")

out={"dataset":"BIP_US (Univ. Seville, external clinical)","n":len(rows),
     "seg_success_rate":segok/len(rows),
     "note":"2nd-vs-3rd probe; no 1st-degree images; deep dermal mapped to Second",
     "acc_pipeline_2v3":float(acc_pipe),"acc_unmasked_2v3":float(acc_base),
     "rows":rows}
os.makedirs(f"{ROOT}/01_paper/statistics",exist_ok=True)
with open(f"{ROOT}/01_paper/statistics/external_validation_BIPUS.json","w") as f: json.dump(out,f,indent=2)
print("\nSaved -> 01_paper/statistics/external_validation_BIPUS.json")
