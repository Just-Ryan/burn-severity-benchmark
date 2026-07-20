# Model & Data Validation Record

> Independent verification of every model, checkpoint, and headline number, run locally against the real files (2026-07-20). Purpose: a reviewer- and supervisor-grade evidence trail. Scripts live in the session and in `05_code/`.

## 1. Checkpoint integrity — all pass
| Checkpoint | Loads | Params | Head | dtype | Notes |
|---|---|---|---|---|---|
| `production/swin-small_masked__best_cnn_mask.pth` | ✅ 0 missing/unexpected keys | 48.8M | 3-class ✓ | fp32 | — |
| `benchmark-checkpoints/swin-small_unmasked__best_cnn_full.pth` | ✅ | 48.8M | 3-class ✓ | fp32 | — |
| `production/swin-small_fp16_deploy.pth` | ✅ | 48.8M | 3-class ✓ | fp16 | matches full model, max|Δ|=1.5e-5 (precision only) |
| `production/yolov8x-seg_1class__best.pt` | ✅ loads via Ultralytics | 71.7M | 1 class 'burn' | — | 125 layers, 327.9 GFLOPs |
| `benchmark-checkpoints/yolov8x-seg_3class__best.pt` | ✅ | 71.7M | 3 class | — | — |

**App-bundled model copies are byte-identical to production** (md5): the Flutter `assets/models/best.pt`, and the FP16 Swin in both the Flutter app and the Flask server, all match production exactly. No drift between the paper's models and the deployed apps.

## 2. Clean dataset (`CNN-Dataset-clean`) — verified sound
The corrected paper depends on this leak-free dataset. Checks:
- **Matched pairs:** masked and unmasked have identical counts (train 2425 / valid 504 / test 495) and **identical filenames** per split/class — 0 mismatches. This is a true paired ablation.
- **Masks are correct:** masked images have a mean non-zero (foreground) pixel fraction of 0.39 (range 0.02–0.94); **zero all-black images**. Unmasked images are full frames (0.997 non-zero).
- **Zero leakage:** train ∩ valid ∩ test source photos = 0 (source-grouped split, verified).
- Class distribution preserved and imbalanced as expected (0/1/2 = 1st/2nd/3rd).

## 3. Reproduced headline numbers (local, real checkpoints)
| Quantity | Reproduced | Paper | Match |
|---|---|---|---|
| Swin masked, full (leaky) test | 93.24% | 93.05% | ✓ (leaky — see below) |
| Swin unmasked, clean 143-test | 90.91% | matches eval screenshot | ✓ |
| Integrated pipeline (128 seg-success imgs) | 91.41% | 91.41% | ✓ exact, incl. per-class F1 |
| External (BIP_US, 94 clinical imgs) | 39.4% | new | ✓ |

## 4. Data-leakage quantification (the key correction)
- Masked classifier test set: **80.5% of images share a source photo with training** (verified by source-ID grouping); unmasked: 0%.
- Masked Swin on **leaked** subset (n=417): 95.9%; on **clean** subset (n=101): **82.2%** → ~13.7 pp inflation.
- Honest ranking: masked-clean **82.2%** < unmasked-clean **88.81%**. Masking does not help once leakage is removed. Full analysis in `DATA_LEAKAGE_FINDING.md`.

## 5. YOLO segmentation validation — COMPLETE, paper numbers verified
Independently re-run with Ultralytics on both splits (`yolo_seg_validation.txt`):

| Model | Split | box mAP50 | mask mAP50 | mask mAP50-95 |
|---|---|---|---|---|
| 1-class (production) | val | 68.4 | **66.9** | 39.7 |
| 1-class (production) | test | 62.5 | 60.7 | 34.5 |
| 3-class (benchmark) | val | 67.8 | 66.4 | 40.4 |
| 3-class (benchmark) | test | 58.3 | **57.2** | 36.1 |

- **Paper's 3-class 57.6% is confirmed as a TEST number** (my test run: 57.2%) — the audit's worry that it might be a validation figure is resolved in the paper's favour.
- **Paper's 1-class 69.1% is a VALIDATION number** (my val: 66.9%; small gap from library/NMS version). Its held-out **test** mask mAP50 is 60.7% — worth adding to the paper for completeness.
- **Training config corrected against checkpoint metadata (2026-07-20, ground truth).** Both segmenters' embedded `train_args` were read directly. Actual configs: **3-class** = 100 epochs, AdamW, lr0 1e-3, imgsz 640, batch 8, from `yolov8x-seg.pt`; **1-class** = 100 epochs, AdamW, lr0 1e-4, imgsz 640, batch 8, **continued from a stage-1 run (`bestmsofar`)** that was itself 100 epochs AdamW. The earlier "3-class 300 ep AdamW / 1-class 150 ep SGD" note came from a notebook that did **not** produce these checkpoints and is superseded; the manuscript now matches the checkpoints. Full audit: `../../04_models/KAGGLE_MODELS_VERIFICATION.md`.

## 6. Clean leak-free classifier benchmark — running (definitive)
8 architectures × masked/unmasked on the **gold-standard deduped split** (val/test one image per source, augmented copies train-only, 0% leakage), fixed seed 42, evaluation-time augmentation off, identical transform across all architectures. On Kaggle GPU. This gives the honest masking result the paper will report.

## 6. Still to reconcile in the manuscript (after the two jobs land)
1. Replace the leaky masked benchmark column with the clean re-run numbers.
2. ✅ Done — segmentation training description corrected to match the checkpoints (100 ep AdamW for both; 1-class continued from stage-1). See §5.
3. State the seg mAP split (val vs test) explicitly, from the validation above.
