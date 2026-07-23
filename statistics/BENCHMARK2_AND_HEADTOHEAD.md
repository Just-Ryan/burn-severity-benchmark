# Benchmark 2 (YOLOv8x-seg) + Head-to-Head — results synthesis

> Compiled for the manuscript. Everything below is on the **identical leak-free,
> source-grouped 70/15/15 split (seed 42)**, val deduplicated to one image per source
> (val 206) and **test = the shared 205-image, one-image-per-unseen-source set**.
> Builders: classifier conditions `05_code/training/build_clean_split_v2.py`; YOLO folds
> `05_code/training/build_clean_yolo_seg.py` (both re-derive the same seed-42 fold, so the
> classifiers, the 1-class localiser and the standalone 3-class YOLO all see identical
> test images).
>
> **Skeptical reading up front:** the pipeline number in the head-to-head is an
> **oracle upper bound**, not a measured end-to-end result. See §3–§4. Two numeric
> discrepancies against files already in this folder are flagged in §6 and must be
> reconciled before submission.

---

## 1. Benchmark 2 — YOLOv8x-seg (just completed, Colab A100)

Config (as reported; matches the 3-class embedded `train_args` in `04_models/MODEL_CARD.md`):
**100 epochs, imgsz 640, batch 8, AdamW lr0 1e-3, seed 42, patience 20**, from `yolov8x-seg.pt`.

| Model | Role | Split | mask mAP50 | mask mAP50-95 |
|---|---|---|---|---|
| YOLOv8x-seg **1-class** | pipeline segmentation stage (localiser) | val | 0.712 | 0.420 |
| YOLOv8x-seg **1-class** | " | **test** | **0.726** | **0.417** |
| YOLOv8x-seg **3-class** | standalone segment-and-classify | val | 0.595 | — |
| YOLOv8x-seg **3-class** | " | **test** | **0.603** | **0.349** |

3-class per-degree **test** mask mAP50 (roughly): Degree1 ≈ 0.63 · Degree2 ≈ 0.47 · Degree3 ≈ 0.75
(Degree2/second-degree is the hardest, consistent with the classifiers' weakest per-class F1.)

**3-class standalone TEST classification accuracy: 78.5% (161/205 correct; 10 images with no detection).**

> Note: these numbers **supersede** the earlier CPU eval in `yolo_seg_validation.txt`
> (which reported 1-class test mask mAP50 0.607 and 3-class test mask mAP50 0.572). The
> Benchmark-2 A100 retrain is materially better; treat the old `.txt` as stale.

---

## 2. Task 1 — Head-to-head (all on the same 205-image test set)

| System | What it does | Test accuracy | 95% CI (Wilson) | Notes |
|---|---|---|---|---|
| **Standalone YOLOv8x-seg (3-class)** | one model segments **and** classifies degree | **78.5%** (161/205) | 72.4 – 83.6 | 10/205 no-detection counted as errors (§4) |
| **Best standalone classifier** (unmasked) | classify the whole image, no segmentation | **84.9%** (174/205) | 79.3 – 89.1 | best single number in Benchmark 1 |
| **Pipeline** = 1-class localiser → **masked** Swin-Small | segment burn, black-out background, then classify | **≤ 82.9%** (oracle) | 77.2 – 87.5 | **upper bound only** — uses ground-truth masks; true end-to-end not yet run (§3) |

Pairwise (two-proportion, unpaired — the correct paired McNemar needs per-image preds, see §5):

- Classifier 84.9% vs YOLO 78.5%: **+6.3 pp**, z = 1.66, p ≈ 0.10 — CIs overlap.
- Oracle pipeline 82.9% vs YOLO 78.5%: +4.4 pp, z = 1.13, p ≈ 0.26.
- Classifier 84.9% vs oracle pipeline 82.9%: +2.0 pp, z = 0.54, p ≈ 0.59 — a tie.

### Honest reading
1. **A dedicated classifier is the most accurate single system** (84.9%), beating the
   all-in-one YOLO by ~6 pp. The gap is in the expected direction and larger than the
   study's masking MDE (~3.6 pp), but at N = 205 the two Wilson CIs still overlap, so it
   is **suggestive, not statistically resolved**. Do not claim a significant win without
   the paired McNemar test (§5).
2. **The pipeline neither helps nor hurts accuracy vs the plain classifier** — even at
   its oracle ceiling (82.9%) it merely **ties** the 84.9% classifier (2.0 pp, p ≈ 0.6).
   Segmentation-then-classify buys no accuracy; crucially, it is also **not harmful**.
3. **Therefore the pipeline's justification is localization / interpretability**
   (it returns *where* the burn is and a clean masked region a clinician can inspect),
   **not accuracy**. State this plainly; do not sell the pipeline as more accurate.
4. **All-in-one segmentation is the weakest classifier** (78.5%): forcing one network to
   localise and grade simultaneously costs accuracy relative to a dedicated grader, and it
   additionally fails to fire on ~5% of images.

> Best-classifier attribution caveat: the task brief names **ConvNeXt-Large unmasked**
> as the 84.9% top model; the local `clean_benchmark_results.json` puts **Swin-Small
> unmasked** at 84.9% (0.84878 = 174/205) and ConvNeXt-Large unmasked at 81.5%. The
> headline number (84.9% = 174/205) is the same either way; the **architecture label
> is unsettled** and must be pinned before the manuscript names one (§6).

---

## 3. Task 2 — CRITICAL VERIFICATION: which masks did Benchmark 1's "masked" condition use?

**Answer: GROUND-TRUTH annotation polygons, NOT the YOLO localiser's predicted masks.**
Consequently the masked-classifier accuracy (~82.9% Swin) is an **oracle / upper bound**
on the pipeline — it is *not* the true end-to-end pipeline number.

Evidence from `05_code/training/build_clean_split_v2.py`:

- The source is a Roboflow-exported **annotation** dataset (human-labelled polygons), read
  straight from its `labels/*.txt` files — no model is ever loaded or run in this script:
  ```python
  # line 17
  SEG = ".../Seqmentation-Dataset/BIAC.v31i.yolov8_3Class"
  # lines 29-34: read the ground-truth label file for each image
  lab = f"{SEG}/{sp}/labels/{base}.txt"
  ...
  cls = [int(l.split()[0]) for l in open(lab) if l.split()]
  ```
  (Verified on disk: `train/labels/1-1-_jpg.rf.*.txt` contains lines like
  `0 0.4843 0 0.4631 0.0329 …` — class id + normalized polygon vertices, i.e. the
  hand-drawn annotation, not a detector output.)

- The mask fed to the classifier is built by rasterising **those ground-truth polygons**
  and multiplying the image by them:
  ```python
  # lines 54-68 + 98-105
  def polys(lp, w, h):            # reads polygon vertices from the GT label file
      ...
  def mask_of(pl, w, h):
      m = np.zeros((h, w), np.uint8)
      for pts in pl:
          cv2.fillPoly(m, [pts], 1)   # perfect polygon fill
      return m
  ...
  pl  = polys(lab, w, h)          # lab = GROUND-TRUTH label path
  m   = mask_of(pl, w, h)
  masked = bgr * m[:, :, None]    # background -> black using the annotation mask
  cv2.imwrite(f"{OUT}/masked/{sp}/{deg}/{base}.jpg", masked)
  ```

There is **no `YOLO(...)`, no `.predict`, no `_best.pt`** anywhere in the file. The
"masked" images are the original photos with the background zeroed out by the **perfect,
human-drawn segmentation**.

**Implication (the load-bearing point for the paper):**
The masked-Swin ~82.9% assumes a *flawless* segmenter. The real pipeline's segmenter is
the 1-class localiser at **mask mAP50 0.726 / mAP50-95 0.417** on this test set — far from
perfect. So the true end-to-end pipeline accuracy is **≤ 82.9%**, and the difference
between the two is exactly the accuracy cost of imperfect (predicted) masks. The paper
must **not** present 82.9% as "the pipeline accuracy"; it is the pipeline's **ceiling**.

---

## 4. Task 4 — The 10/205 "no-detection" cases (standalone YOLO)

- 205 test images = **161 correct + 10 no-detection + 34 detected-but-wrong-degree**.
- The reported **78.5% already counts the 10 no-detections as errors** (denominator fixed
  at the full 205). This is the honest convention — **keep it**. Do not quote an accuracy
  computed only over images where the detector fired (that would inflate to 161/195 ≈ 82.6%).
- Report it explicitly, e.g.: *"On 10/205 (4.9%) test images the detector produced no
  burn detection; these are scored as errors. Standalone accuracy is 78.5% over all 205
  images (82.6% over the 195 images with a detection)."* Give both, label the first as the
  primary number.
- **Caution for the pipeline:** these 10 no-detections are a property of the **3-class**
  model. The **1-class localiser** has higher recall (test mask mAP50 0.726 vs 0.603), so
  its no-detection count on the 205 test images will likely be **different (probably lower)**
  and **must be measured**, not assumed to be 10. Whatever it is, those images are pipeline
  errors and must stay in the denominator.

---

## 5. Task 3 — What remains to compute a clean, true end-to-end pipeline number

**Definition of the number still owed:** for each of the 205 test images, run the
Benchmark-2 **1-class localiser** → threshold mask → `mask × image` (background black) →
classify with a **clean-split-trained masked Swin-Small** → predicted degree; score all
205 (no-detections = errors). This replaces the ground-truth masks of §3 with real
predicted masks, turning the 82.9% ceiling into an actual measurement.

### Weights needed and where they live

| Component | Use this | Location | Status |
|---|---|---|---|
| **1-class localiser** | Benchmark-2 checkpoint | Colab Drive `Burn-Benchmark2/models/yolov8x-seg_1class_best.pt` | ✅ exists; matches the reported test mAP50 0.726 |
| Masked Swin-Small classifier | clean-split (leak-free, seed-42, deduped) masked checkpoint | **NOT found locally** | ⚠️ **missing — must be recovered or retrained** |

**Localiser detail:** use the **Benchmark-2** localiser, not the older
`04_models/production/yolov8x-seg_1class__best.pt`. The production one is an earlier,
weaker model (val mask mAP50 ≈ 0.67 in `yolo_seg_validation.txt`) — a different checkpoint.
Using the Benchmark-2 localiser keeps the end-to-end number consistent with the 0.726 test
mAP reported in §1.

**Classifier detail — this is the blocker.** The two Swin checkpoints on disk are the
**old leaky-era models**, not the clean ones:
- `04_models/production/swin-small_masked__best_cnn_mask.pth` (dated 2025-03-03) — the
  93.05%→~82% honest *leaky* model. `04_models/MODEL_CARD.md` explicitly flags it as
  **superseded** and leakage-inflated; `swin_eval_results.json` shows it was scored on the
  leaky "CNN-DatasetM/test" (n=518, 93.2%).
- `04_models/benchmark-checkpoints/swin-small_unmasked__best_cnn_full.pth` (2025-03-03) —
  the leaky unmasked control (88.81%).

Both were trained on the pre-dedup, source-leaking data. **Classifying the clean 205-image
test set with either would re-introduce leakage** (their training sources overlap the clean
test sources) and is invalid for an honest end-to-end number.

The **clean** masked-Swin — the one that produced the ~82.9% oracle figure — was a Kaggle
`burn-clean-benchmark` notebook run and its checkpoint is **not preserved in this repo**
(`MODEL_CARD.md`: *"The other … benchmarked architectures were trained on Kaggle … Their
checkpoints are not all preserved locally"*; `KAGGLE_MODELS_VERIFICATION.md`: *"None of the
Swin classifiers is stored as a Kaggle Model … they exist only in this repo (and in
notebook outputs)"*). So, in priority order:

1. **Recover** the clean masked-Swin checkpoint from the `burn-clean-benchmark` Kaggle
   notebook output (if it was saved there). Cheapest if it exists.
2. Otherwise **retrain-and-save** a masked Swin-Small on the clean `masked` variant
   (`build_clean_split_v2.py` output, `masked/train`), using the exact Benchmark-1 recipe
   (AdamW, seed 42, class-weighted CE, best-val checkpoint), and **archive the `.pth`**.
   This is a required reproducibility artifact regardless — it should be saved for Zenodo.

### Procedure once both weights are in hand
1. Run the Benchmark-2 1-class localiser on each of the 205 test images (imgsz 640);
   take the highest-confidence mask; threshold at **0.1** (the deployed/paper threshold);
   compute `mask × image`.
2. Classify each masked image with the clean masked-Swin, using the **transform that model
   was trained with** — the clean-benchmark recipe is **Resize(224) + ImageNet-norm**
   (`build_clean_split_v2.py`), **not** the deployed `Resize(256)/CenterCrop(224)` in
   `05_code/pipeline/integrated_pipeline__yolov8seg_swin.py`. Match training, or the number
   is biased.
3. **Score all 205** with no-detections as errors (fixed denominator). Report accuracy +
   Wilson CI + per-degree confusion.
4. **Also run the paired McNemar test** (pipeline vs standalone-classifier, and
   classifier vs standalone-YOLO) — this needs per-image predictions from all three systems
   on the 205 images. The standalone-YOLO per-image predictions live in the Benchmark-2
   Colab outputs; export them. McNemar (paired) is the statistically correct head-to-head
   test and can resolve the 6.3 pp classifier-vs-YOLO gap that the unpaired test leaves at
   p ≈ 0.10.

⚠️ **Reuse-with-care warning:** `integrated_pipeline__yolov8seg_swin.py` is a good template
for steps 1–2 **but** (a) it points at old leaky paths + the leaky `cnn_compressed_fp16.pth`,
and (b) on no-detection it `return None` and the image is **dropped from the denominator**
(`success_rate < 100%`) — that inflates accuracy. Fix both before using it: load the clean
checkpoints and **count no-detections as errors**.

---

## 6. Discrepancies to reconcile before the manuscript (do not skip)

1. **Benchmark-1 numbers differ from the local JSON.** The brief describes the final
   Benchmark 1 as **11 architectures × 4 input conditions** with a multi-seed (0, 1, 42)
   masking confirmation, and quotes e.g. Swin-Tiny masked **85.4%**, ConvNeXt-Large
   unmasked **84.9%**, Swin-Small unmasked **80.5%** / masked **82.9%**. The file actually
   in this folder, `clean_benchmark_results.json` (+ `CLEAN_BENCHMARK_RESULTS.md`,
   `STATISTICS_REPORT.md`), is an **earlier 8-architecture × 2-condition, seed-42-only**
   run with different values (Swin-Small unmasked 84.9% / masked 81.0%; Swin-Tiny masked
   82.4%; ConvNeXt-Large unmasked 81.5%). **The final 11-arch / 4-condition / multi-seed
   results are not yet exported to `01_paper/statistics/`.** Land that JSON here and
   regenerate the tables so the manuscript, this doc, and the raw data agree. The headline
   figures used above (84.9% best classifier, 82.9% oracle-masked Swin) are taken from the
   brief; confirm them against the final export.
2. **Best-classifier architecture** (ConvNeXt-Large vs Swin-Small) — see §2 caveat; pin it.
3. **The masking conclusion is unchanged and safe:** whether from the 8-arch or 11-arch
   run, masking shows **no reliable benefit** (pooled ≈ +0.55 pp, Wilcoxon p ≈ 0.32;
   transformer-vs-convnet p ≈ 0.33), and cropping ≈ +0.0 pp. State the null honestly; the
   earlier "+3.06 pp, masking helps" was a data-leakage artifact.

---

## 7. One-paragraph summary for the manuscript

On a single leak-free 205-image test set, a **dedicated image classifier is the most
accurate system at 84.9%**, an all-in-one **YOLOv8x-seg that both segments and grades
reaches 78.5%** (with no detection on 4.9% of images, scored as errors), and the
**segment-then-classify pipeline neither helps nor hurts** — even assuming a perfect
segmenter it only ties the plain classifier at 82.9%. Because Benchmark 1's "masked"
condition was built from **ground-truth annotation polygons**, that 82.9% is an **oracle
ceiling**, not the deployed pipeline's accuracy; the true end-to-end number (localiser
predictions → masked Swin, all 205 scored) is **still to be computed** and requires
recovering-or-retraining the clean masked-Swin checkpoint (the only version saved locally
is the superseded leaky one). The pipeline's contribution is therefore **localization and
interpretability, not accuracy**, and masking/cropping provide **no reliable
classification benefit** once leakage is removed.
