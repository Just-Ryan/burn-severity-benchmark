# Does segmentation-based masking help automated burn severity classification? A leakage-corrected benchmark with external validation

Code and reproducibility materials for the paper of the same name. This repository
accompanies a study of deep learning for burn severity classification (first, second,
and third degree) from photographs, and its central result is a cautionary one.

## Summary

We asked whether restricting a classifier's input to the segmented burn region
("masking") improves accuracy, benchmarked 21 architectures, and built a
YOLOv8-segmentation → Swin-Small-classification pipeline.

- On a **naive file-level split** of the augmented dataset, masking appeared to help
  20 of 21 architectures (mean +3.06 pp; best 93.05%).
- **That benefit is a data-leakage artifact.** Because the source dataset augments each
  photograph into several near-duplicate copies, a file-level split placed copies of the
  same photograph in both training and test, leaking ~80% of the masked test set while
  the unmasked split leaked none.
- On a **leak-free split** grouped by the 1,370 unique source photographs (validation and
  test deduplicated to one image per source), the masking effect **vanishes**: mean
  0.0 pp, paired t-test p = 1.0. No architecture is statistically best; clean accuracies
  are 75–85%.
- The end-to-end pipeline **ties** a plain classifier on identical images (McNemar p = 1.0),
  and on an **independent clinical dataset** accuracy falls to 39% (below the majority-class
  baseline), with systematic under-grading of severity.

The contribution is a **leakage-corrected, uncertainty-aware benchmark** and a reproducible
account of a data-hygiene pitfall that is easy to make and hard to see.

## Repository structure

```
code/
  training/
    build_clean_split.py        # builds the leak-free, source-grouped split
    kaggle-notebooks/           # the training notebooks (seg + classifiers), as .py
  pipeline/
    train_yolov8_seg.py         # segmentation training
    train_cnn_classifier.py     # classifier training
  evaluation/
    external_validation_bipus.py# external (BIP_US) evaluation
    *__evaluate_models.py       # per-stage evaluation
statistics/                     # bootstrap CIs, McNemar, sign/Wilcoxon, power, raw JSON/CSV
docs/
  DATASET.md                    # datasheet + leakage correction
  MODEL_CARD.md                 # model card
```

## Reproducing the results

1. **Environment.** Python 3.10+, PyTorch, `timm`, `ultralytics`, `scikit-learn`, `scipy`.
   Training was run on Kaggle (NVIDIA Tesla P100). Note: on P100, pin
   `torch==2.5.1 torchvision==0.20.1` (cu121) — newer builds drop the P100 (sm_60) kernels.
2. **Data.** Download the primary dataset from Roboflow (link below) and the BIP_US external
   set from the University of Seville (research request).
3. **Build the leak-free split:** `python code/training/build_clean_split.py` — groups
   augmented copies by source photograph, keeps copies train-only, and deduplicates
   validation/test to one image per source (seed 42).
4. **Train** the segmenter and classifiers with the scripts in `code/`.
5. **Evaluate and run statistics** with the scripts in `code/evaluation/` and `statistics/`.

## Data availability

- **Primary dataset:** "skin burn wound classification" by Binus, Roboflow Universe,
  CC BY 4.0 — https://universe.roboflow.com/binus-if3z9/skin-burn-wound-classification
- **External validation:** BIP_US database, Biomedical Image Processing Group, University of
  Seville (available for research on request).

## Model availability

Trained checkpoints are hosted on Kaggle:

- 1-class YOLOv8x-seg (pipeline segmenter): `justryantl/yolo-seg1c_dt`
- 3-class YOLOv8x-seg (benchmark segmenter) and Swin-Small classifiers: see the project's
  Kaggle models under user `justryantl`.

## Citation

> DOI and full citation will be added upon publication.

## License

The code in this repository is released for research use. Note that it depends on
Ultralytics YOLOv8, which is licensed **AGPL-3.0**; trained YOLO checkpoints inherit that
license. Choose and add a top-level `LICENSE` consistent with that dependency before making
the repository public.

## Acknowledgment

We thank the Biomedical Image Processing Group of the University of Seville for the BIP_US
database, and the Kaggle platform for computational resources.
