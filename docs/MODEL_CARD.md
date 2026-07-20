# Model Card — Burn Segmentation & Classification

> ⚠️ **Correction (2026-07-20):** the masked classifier below was trained on a dataset with ~80% train/test leakage, so its **93.05% is inflated**; its honest accuracy on never-seen images is ~82% (below the unmasked model's ~89%). The `swin-small_masked` checkpoint is retained for transparency but **superseded** by the leak-free re-run (`../05_code/training/build_clean_split.py` + Kaggle `burn-clean-benchmark`). See [`../01_paper/statistics/DATA_LEAKAGE_FINDING.md`](../01_paper/statistics/DATA_LEAKAGE_FINDING.md).

## Production models (`production/`) — the deployed pipeline
| File | Arch | Role | Size | Reported metric |
|---|---|---|---|---|
| `yolov8x-seg_1class__best.pt` | YOLOv8x-seg | Stage 1: segment burn (1 class) | 137 MB | mask mAP50 ≈ 69% (val) |
| `swin-small_masked__best_cnn_mask.pth` | Swin-Small (timm `swin_small_patch4_window7_224`) | Stage 2: classify masked burn | 186 MB | ⚠️ 93.05% reported but **leakage-inflated** (~82% honest) |
| `swin-small_fp16_deploy.pth` | Swin-Small, FP16 | Deployment copy (apps/Flask) | 93 MB | same weights, half precision |

**Pipeline:** `photo → YOLO seg → binary mask (thr 0.1) → mask×image → Resize256/CenterCrop224/ImageNet-norm → Swin → {First, Second, Third}`. End-to-end **91.41%**, ~718 ms/image (Swin is ~95% of the time). Canonical code: `../05_code/pipeline/integrated_pipeline__yolov8seg_swin.py`; deployment: `../06_apps/flutter-and-flask/burin_ai2/flask_server/app2.0.py`.

## Benchmark checkpoints (`benchmark-checkpoints/`)
| File | Arch | Role |
|---|---|---|
| `swin-small_unmasked__best_cnn_full.pth` | Swin-Small | Ablation control (unmasked), 88.81% test |
| `yolov8x-seg_3class__best.pt` | YOLOv8x-seg | 3-class segmentation benchmark (mask mAP50 57.6%) |

The other 20 benchmarked architectures were trained on Kaggle (notebooks `MasksCNN` / `NoMasksCNN`, reused per model). Their checkpoints are **not** all preserved locally — see reproducibility note below.

## Archive (`archive/`)
Old-Way detection-era models (VGG16, ResNet50, MobileNet `.keras`/`.pth`, YOLO-detect `best.pt`) currently remain inside `../03_datasets/archive/Old-Way-detection/` with their datasets. Superseded; kept for the record.

## ⚠️ Reproducibility notes
- Training notebooks were **reused across models** ("change the version to another model"), so the currently-saved `MasksCNN` version shows 89.19% (a *different* architecture), while the **93.05% Swin-masked** result is in an **earlier version** of that notebook. Pin each benchmark number to its notebook version before publishing.
- Missing for full reproduction: random seeds, `requirements.txt` for training, exact Roboflow dataset version. To be added.
- Recommended for release: publish `production/` checkpoints to **Zenodo** (free DOI) + Hugging Face; update the paper's Data Availability from "upon request" to real links.

## App-bundled copies (duplication is intentional)
The Flutter app and Flask server bundle their own copies of `best.pt` + `cnn_compressed_fp16.pth` under `../06_apps/flutter-and-flask/burin_ai2/.../assets/models/` and `.../flask_server/models/`. These are byte-identical to `production/` and must ship with the app to run offline.
