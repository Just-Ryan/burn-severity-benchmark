# Critical finding: data leakage in the masked benchmark

> Found by the code-fairness audit (2026-07-20) and verified locally against the real checkpoints and datasets. **This invalidates the paper's main positive claim as currently measured and must be fixed before submission.**

## What happened
The Roboflow export produces several augmented copies of each source photo, named `<source>_jpg.rf.<hash>...jpg`. The two classifier datasets were split differently:

| Dataset | split ratio | test images whose **source photo is also in train** |
|---|---|---|
| **CNN-DatasetM (masked)** | 2400 / 513 / 518 (70/15/15) | **417 / 518 = 80.5%** (validation also 82% contaminated) |
| **CNN-DatasetNM (unmasked)** | 3081 / 200 / 143 (90/6/4) | **0 / 143 = 0.0%** (clean Roboflow split) |

The masked set was re-split *after* the augmented copies were flattened, scattering copies of the same photo across train and test. The unmasked set kept Roboflow's leak-free split.

## Impact (measured on the real `best_cnn_mask.pth`)
| Masked Swin-Small evaluated on | n | accuracy |
|---|---|---|
| Full test set (the reported number) | 518 | 93.24% |
| Leaked subset (source seen in training) | 417 | 95.9% |
| **Clean subset (source never in training)** | 101 | **82.2%** |

Leakage inflated this model by **~13.7 points**. The honest masked accuracy is ~82%, not 93%.

## Consequence for the paper's claims
- The **unmasked** clean accuracy is **88.81%**; the **masked** clean accuracy is **82.2%**. So on leak-free evaluation, **masking does not improve classification — it is worse.**
- The headline "segmentation-masking improves classification for 20 of 21 architectures (+3.06 pp mean)" is an artifact of the 80%-vs-0% leakage asymmetry, not a real effect.
- This is consistent with the earlier paired McNemar test (pipeline vs plain classifier on identical images, p = 1.0) and with the external-validation failure: **no independent evidence that masking helps survives once confounds are removed.**

## Required fix (one of):
1. **Re-run properly (recommended, uses GPU):** build ONE leak-free, source-grouped split (all augmented copies of a source confined to a single split); derive matched masked and unmasked datasets from that same split; retrain the classifier(s) on each; report the honest, paired masking comparison. This definitively answers "does masking help?" with clean data.
2. **Reframe honestly without re-running:** report the leakage discovery as the finding — apparent masking benefit was a data-hygiene artifact that disappears (masked 82% < unmasked 89%) on clean evaluation — and drop/retract the "masking helps" claim. A cautionary reproducibility contribution.

Either way, the current masked column of the benchmark table and the "masking helps" narrative cannot be submitted as-is.

## Other code issues found (see the full audit)
- Test-time augmentation applied to the test set (flips/rotation/brightness/CoarseDropout) → reported numbers are stochastic, not reproducible.
- No random seeds set.
- Class weights hardcoded to `[100,50,30]  # Example counts`, not the true class frequencies.
- YOLO segmentation training in the paper (100 epochs, AdamW) does not match the code (3-class: 300 epochs AdamW; 1-class: 150 epochs SGD); 3-class mAP may be a validation, not test, number.
- Cosmetic: notebook loads `densenet201` while a comment says "DenseNet-121"; `Degree1/2/3` vs `First/Second/Third` folder naming.
