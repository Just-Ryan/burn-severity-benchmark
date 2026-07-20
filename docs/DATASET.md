# Dataset Datasheet — Burn Injury Images

> Single source of truth for the data behind this project. Fill the ⚠️ items before publication (needed for the Data Availability statement).

## Source & license
- **Origin:** Roboflow Universe — "skin burn wound classification" by **Binus**, exported as `BIAC.v31i.coco-segmentation` (version 31). URL: https://universe.roboflow.com/binus-if3z9/skin-burn-wound-classification
- **License:** Creative Commons Attribution 4.0 (CC BY 4.0). 3 classes labelled numerically 0/1/2 → mapped to 1st/2nd/3rd degree.
- **⚠️ Image-count reconciliation (a reviewer will ask):** the Roboflow project page currently shows **3,695** images; the v31 COCO-segmentation export used here contains **3,424 images that carry a valid burn polygon** (images without an annotation are dropped). Critically, these 3,424 are **Roboflow-augmented copies of only 1,370 unique source photographs** (~2.5 copies per source, up to 3×). The paper's earlier "≈3,440" refers to the augmented image count. All splits in this project are done **by the 1,370 source photos**, never by the 3,424 files — that is the fix for the leakage described below.
- **Labeling:** public Roboflow annotations. **NOT independently re-verified by a clinician** — the paper does not claim clinical verification.

## ⚠️ DATA-LEAKAGE CORRECTION (2026-07-20) — read first
The original **masked** classifier dataset (`CNN-DatasetM`, now `CNN-DatasetM-DEPRECATED-LEAKY`) was re-split *after* Roboflow augmentation copies were flattened, so **81.8% of its test images shared a source photo with training** (verified). The unmasked set (`CNN-DatasetNM`) kept Roboflow's leak-free split (0%). This inflated the masked classifier's accuracy from an honest ~82% to 93.05% and produced the (now-retracted) "masking helps" result. **The canonical replacement is `CNN-Dataset-clean/`** (below), built leak-free by `../05_code/training/build_clean_split.py`. Full analysis: `../01_paper/statistics/DATA_LEAKAGE_FINDING.md`.

## Contents (current "New-Way" era)
Total ≈ **3,440** burn images, 3 severity classes. Natural class imbalance:

| Class | Images | Share |
|---|---|---|
| 1st degree | ~1,444 | 42.0% |
| 2nd degree | ~1,055 | 30.7% |
| 3rd degree | ~941 | 27.4% |

Split ≈ 70 / 15 / 15 (train / val / test).

## Dataset variants (`New-Way/`)
| Variant | Path | Split (tr/va/te) | Leakage | Status |
|---|---|---|---|---|
| **YOLO 3-class seg** | `Seqmentation-Dataset/BIAC.v31i.yolov8_3Class/` | 3081/200/143 | 0% | current (seg benchmark + source for clean rebuild) |
| **YOLO 1-class seg** | `Seqmentation-Dataset/BIAC.v31i.yolov8_1Class/` | 3081/200/143 | 0% | current (pipeline stage 1) |
| **CNN clean (masked + unmasked)** | `CNN-Dataset-clean/{masked,unmasked}/` | 2425/206/205 | **0% (source-grouped, val/test deduped to 1 image/source)** | ✅ **canonical** — matched pair for the honest masking ablation |
| **CNN unmasked (legacy)** | `CNN-DatasetNM/` | 3081/200/143 | 0% | kept (clean Roboflow split; matches the paper's legacy unmasked eval) |
| **CNN masked (LEAKY)** | `CNN-DatasetM-DEPRECATED-LEAKY/` | 2400/513/518 | **81.8%** | ❌ deprecated — do not use; retained for transparency (see its `LEAKAGE.md`) |

`CNN-Dataset-clean` classes are `0/1/2` = 1st/2nd/3rd degree; the split is grouped by source photo (all augmented copies confined to one split), verified train∩valid∩test = 0 sources.

## Dataset generation
- **Clean split (canonical):** `../05_code/training/build_clean_split.py` reads the 3-class YOLO polygons, groups augmented copies by source id (`<src>_jpg.rf.<hash>`), does a stratified 70/15/15 **group** split by source (seed 42), keeps all augmented copies **only in the training fold**, and **deduplicates validation and test to one image per source** (206 and 205 images, exactly one per unseen source). Writes matched masked + unmasked copies. Verified train ∩ valid ∩ test sources = 0.
- **Legacy masked (deprecated):** `../05_code/training/newway-seqcode/extractMasks.py` — the original per-degree flat mask extraction that led to the leaky re-split.

## Archived data (superseded)
- `archive/Old-Way-detection/` — the detection-era datasets (~19k images across Yolo_Dataset, CNN_Dataset, Yolo&CNN_Dataset). Kept as evidence for the paper's "why we switched to segmentation" argument.
- `archive/Dataset-tool-yolo-detection/` — exploratory YOLO-detection fine-tuning runs.

## Kaggle mirror
Datasets also live on Kaggle (`JustRyanTL`), cleaned 2026-07-20 to 5 current sets: `burn-clean-split` (new canonical, masked+unmasked), `CNN-NMask_DT`, `YOLO-Seg1C_DT`, `YOLO-Seg3C_DT`, and `cnn-mask-dt` (deprecated/leaky, kept for transparency). ~18 superseded detection-era datasets were deleted (preserved locally in `archive/`).
