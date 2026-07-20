# Statistical Validation Report

> ⚠️ **PARTIALLY SUPERSEDED (2026-07-20, later same day).** This report was written on the *leaky* masked split (N=518) before the gold-standard leak-free re-run. Its Section 4 recommendation to "lead with the input-level masking ablation" is **no longer valid**: on the leak-free split (grouped by the 1,370 source photos), masking has **no effect** (mean 0.0 pp; paired-t p=1.0), even with clean annotation-derived masks. The reproduced 93.05% and the "masking helps with clean masks" framing were data-leakage artifacts. The McNemar pipeline result (§2, p=1.0), the transform-sensitivity note (§3), and the no-single-architecture-winner finding (§5) remain valid. **Definitive result: `CLEAN_BENCHMARK_RESULTS.md`; leakage analysis: `DATA_LEAKAGE_FINDING.md`.**

> Real experiments run locally (CPU) on 2026-07-20 using the repository's own checkpoints and test sets. Reproduces the paper's headline numbers, adds the 95% confidence intervals and significance tests the paper was missing (Practical Task 6), and surfaces one important, honest caveat about the central claim. Scripts: `scratchpad/eval_swin.py`, `scratchpad/paired_mcnemar.py`. Raw outputs: `swin_eval_results.json`, `swin_predictions.json`, `paired_mcnemar_results.json`.

## 1. Headline accuracies reproduced (with bootstrap 95% CIs)

| Configuration | Test set | Accuracy | **95% CI** (10k bootstrap) | Paper says |
|---|---|---|---|---|
| Swin-Small **masked** | CNN-DatasetM/test (518) | **93.24%** | **[91.12, 95.37]** | 93.05% ✓ |
| Swin-Small **unmasked** | CNN-DatasetNM/test (143) | **90.91%** | **[86.01, 95.10]** | (matches the standalone eval screenshot exactly) |

Per-class (masked, N=518): First P96.2/R93.6/F94.9 · Second P87.5/R92.5/F89.9 · Third P95.7/R93.7/F94.7.
The masked run reproduces the paper's 93.05% to within 0.2 pp — **the headline classification result is real and reproducible.**

## 2. The paired significance test on the central claim (the important part)

The benchmark's masking ablation (93.05% masked vs 88.81% unmasked) was measured on **two independently-split datasets** — the masked and unmasked test sets share only 19 of 143 images, so that comparison is **not paired**. To test the claim rigorously, I built a properly paired experiment on **the same 143 images**:

- **Unmasked model** classifies the raw image.
- **Masked model** classifies the **YOLO-segmented (real pipeline)** version of the *same* image.
- Both use the deployed pipeline transform (Resize256 / CenterCrop224).

| Comparison (same images) | Unmasked-on-raw | Masked-pipeline | McNemar p |
|---|---|---|---|
| Seg-success subset (N=128) | **91.41%** | **91.41%** | **1.0000** |
| Full set incl. seg failures (N=143) | 90.91% | 88.81% | 0.6900 |

**Finding:** on identical images, the end-to-end segmentation-first pipeline and a plain unmasked classifier are **statistically indistinguishable** (91.41% vs 91.41%, McNemar p = 1.0; 10 images helped, 10 hurt). The pipeline **matches but does not beat** the simpler classifier here.

**Why this differs from the benchmark's +4 pp masking gain:** the benchmark used *clean, ground-truth-derived* masks; the real pipeline uses *YOLO-predicted* masks, which are imperfect (segmentation failed outright on 15/143 ≈ 10%). Segmentation error erodes the theoretical benefit of masking. This **quantifies the paper's own stated limitation** ("segmentation quality directly impacts the pipeline").

**Caveats:** N is small (128–143) so McNemar has limited power — "not significant" ≠ "proven equal." The point estimates being identical (91.41 = 91.41) is nonetheless striking. The masked model was trained on GT masks, so feeding it YOLO masks is a mild train/test shift.

## 3. A reproducibility landmine found: transform sensitivity

The masked model's accuracy on YOLO-masked images swings **5.5 pp** purely from preprocessing:

| Eval transform | Masked model, seg-success (N=128) |
|---|---|
| `Resize((224,224))` (standalone-eval style) | 85.94% |
| `Resize(256)+CenterCrop(224)` (pipeline style) | **91.41%** |

The exact eval transform **must be pinned** in the paper and code, or the headline pipeline number is not reproducible.

## 4. What this means for publication

1. **Keep and lead with the input-level ablation** — "segmentation-masking improves classification given good masks" is real, reproduced, and defensible (that is the benchmark's masked-vs-unmasked result with clean masks).
2. **Reframe the pipeline claim honestly** — the *end-to-end* segmentation-first pipeline, evaluated on identical images with real predicted masks, is **on par with**, not superior to, a strong unmasked classifier. Say so. This is more trustworthy and pre-empts the exact objection a sharp reviewer would raise.
3. **This strengthens the "future work" narrative** — better segmentation is the lever that would convert the clean-mask advantage into a real end-to-end gain.
4. **Add these numbers to the paper:** the 95% CIs (§1), the paired McNemar (§2), and the transform note (§3) directly complete Practical Task 6 and answer the #1 reviewer risk.

## 5. Architecture-comparison significance — "SWIN-Small is best" is NOT statistically supported

Using Wilson 95% score intervals at the confirmed masked test size (N = 518), and pairwise two-proportion tests (`architecture_wilson_CIs.csv`):

| Architecture | Masked acc | 95% CI |
|---|---|---|
| **SWIN-Small** | 93.05% | [90.53, 94.94] |
| ConvNeXt-Large | 91.70% | [89.00, 93.78] |
| ConvNeXt-XLarge | 91.12% | [88.36, 93.28] |
| SWIN-Tiny | 90.15% | [87.29, 92.43] |
| … (top ~10 all overlap) | | |

- At ~91% accuracy with N = 518, the 95% CI half-width is **±2.5 pp** — so any accuracy gap **smaller than ~5 pp is within noise.**
- **Pairwise tests vs the "winner":** SWIN-Small vs ConvNeXt-Large **p = 0.41**; vs ConvNeXt-XLarge **p = 0.25**; vs SWIN-Tiny **p = 0.09**. **None are significant.**

**Implication for the paper:** the statement that SWIN-Small "achieved the highest accuracy, outperforming all other architectures" must be softened to *"achieved the numerically highest accuracy; its advantage over the leading CNNs (ConvNeXt-Large/XLarge) and smaller SWIN variants was within the 95% CI and not statistically significant at this test-set size."* Reporting this **strengthens** the paper — it reframes the contribution as an honest benchmark with proper uncertainty rather than an overclaimed winner. Many identical accuracies in the original table (e.g. four models at 85.31%) are consistent with this: the test set simply cannot resolve sub-5-pp differences.

## 6. Still outstanding (needs Kaggle / more compute)
- **Definitive paired McNemar between top architectures**: the Wilson-CI/z-test above already shows non-significance; a paired McNemar would confirm it but needs ConvNeXt-Large predictions (checkpoint not saved → retrain on Kaggle). Lower priority now that the CI overlap is established.
- **External-dataset validation**: run the frozen pipeline on a genuinely external public burn set (not this Roboflow source). *(In progress — teammate sourcing a dataset.)*
- **Reconcile the two test sets** (143 vs 518) so every reported number maps to one clearly-named split.
