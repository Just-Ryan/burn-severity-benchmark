# Kaggle Models — verification and cleanup plan (2026-07-20)

Every Kaggle Model under `justryantl` was inventoried and, where it could be a
production artifact, downloaded and md5-checked against the local repository
**before any deletion**. No Kaggle item has been deleted; deletions below are
recommendations awaiting the owner's approval.

## Local production/benchmark checkpoints (the paper's actual models)
| File | Size (bytes) | md5 |
|---|---|---|
| `production/yolov8x-seg_1class__best.pt` | 143,940,093 | `db15d921120a7ce36ef4b21b943d1b4e` |
| `benchmark-checkpoints/yolov8x-seg_3class__best.pt` | 143,923,901 | `c3dcd18e7689cc84d81e154311131c2c` |
| `production/swin-small_masked__best_cnn_mask.pth` | 195,488,238 | `6c7c982ed572b4f380107eae6384bf08` |
| `benchmark-checkpoints/swin-small_unmasked__best_cnn_full.pth` | 195,488,238 | `49d33187c95ce12aedb5f1eaff79e1e5` |
| `production/swin-small_fp16_deploy.pth` | 97,802,272 | `968ae5bc1fdef14d6c36a205fabb222d` |

**None of the Swin classifiers is stored as a Kaggle Model** — they exist only in
this repo (and in notebook outputs). They are the single most important files to
preserve and are the priority for the Zenodo deposit.

## The 10 Kaggle Models
| Kaggle Model | Files | Size | Date | md5-verified? | What it is | Recommendation |
|---|---|---|---|---|---|---|
| `bestmsofar` | best.pt | 137 MB | 2025-03-02 | ✅ `b158d616...` **unique** | Stage-1 of the production 1-class segmenter (lineage parent) | **PRESERVED locally** (`archive/segmentation-lineage/`); safe to delete from Kaggle after |
| `yolo-seg1c_dt` | best.pt | 137 MB | 2025-03-03 | ✅ `db15d921...` = local 1-class **exact** | The production 1-class segmenter | Backed up locally; **keep on Kaggle** (it is the clean, correctly named copy) |
| `yolov8x-seg_last` | last.pt | 411 MB | 2025-02-23 | not downloaded | Last-epoch checkpoint with optimizer state (not used for inference) | **Keep** (or download before deleting; not needed for the paper) |
| `classifymodels` | 5× ImageNet `.h5` | 84–90 MB | 2024-11-20 | n/a | Public Keras ImageNet backbone weights (inception/mobilenet/resnet50/vgg16/vgg19), not trained on burns | **Delete** — publicly re-downloadable, not our work |
| `newtrainedmodels` | 2× `.keras` | 112 MB | 2024-11-20 | n/a | Old Keras burn classifiers (project later moved to PyTorch/timm) | **Delete** — superseded era |
| `trainedcnnmodels` | 2× `.keras` | 112 MB | 2024-11-21 | n/a | Byte-name duplicate of `newtrainedmodels`, one day later | **Delete** — duplicate + superseded |
| `yoloskinburn` | skin_burn_2022_8_21.pt | 316 MB | 2024-10-31 | not downloaded | Old 2022 detection model, Old-Way (detection→crop) era | **Delete** (Old-Way; archived locally under `03_datasets/.../archive`) |
| `yolov8sbest` | best.pt | 22 MB | 2024-11-02 | not downloaded | YOLOv8s detection, Old-Way | **Delete** — superseded |
| `yolov8best` | best.pt | 22 MB | 2024-11-12 | not downloaded | YOLOv8s detection, Old-Way | **Delete** — superseded |
| `yolobestmodel` | best.pt | 14 MB | 2024-11-22 | not downloaded | Small YOLO detection, Old-Way | **Delete** — superseded |

## Corrected training configuration (ground truth from embedded `train_args`)
The manuscript previously described the segmenters as "3-class: 300 epochs AdamW"
and "1-class: 150 epochs SGD," taken from a notebook. The **checkpoints' own
embedded arguments** — authoritative, since Ultralytics records the exact run that
produced each file — say otherwise, and the manuscript was corrected to match:

- **3-class:** segment, 3 classes, **100 epochs, AdamW, lr0 1e-3**, imgsz 640, batch 8, from `yolov8x-seg.pt`.
- **1-class:** segment, 1 class, **100 epochs, AdamW, lr0 1e-4**, imgsz 640, batch 8, **continued from the stage-1 `bestmsofar` run** (itself 100 epochs AdamW from `yolov8x-seg.pt`).

There is no SGD run and no 300/150-epoch run among the deployed checkpoints.

## Bottom line
- Nothing unique will be lost: the one genuinely unique inference-relevant model
  (`bestmsofar`) is now preserved in the repo with a verified md5.
- Seven Models (`classifymodels`, `newtrainedmodels`, `trainedcnnmodels`,
  `yoloskinburn`, `yolov8sbest`, `yolov8best`, `yolobestmodel`) are superseded or
  publicly re-downloadable and are safe to delete once approved.
- Two seg Models are the current production 1-class segmenter and its lineage
  parent; keep `yolo-seg1c_dt`, delete-or-keep `bestmsofar` (already backed up).
- `yolov8x-seg_last` is an optional training-state checkpoint; keep it.
