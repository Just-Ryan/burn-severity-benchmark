# Clean (leak-free) benchmark — definitive results

> The gold-standard re-run that determines the paper's conclusion. Raw data: `clean_benchmark_results.json`. Kaggle: `justryantl/burn-clean-benchmark` on `justryantl/burn-clean-split` (v2, deduped).

## Setup (all fixes applied)
- **Split:** by the 1,370 unique source photographs, stratified 70/15/15; augmented copies **only in training**; validation and test **deduplicated to one image per source** (val 206, test 205); **0% source leakage** (verified).
- **Training:** fixed seed 42; AdamW (lr 1e-4, wd 1e-2); cosine over 30 epochs; early stopping patience 5; batch 16; class-weighted cross-entropy with **true inverse-frequency weights**; robust `num_classes=3` head.
- **Evaluation:** augmentation **off**; identical transform (Resize 224, ImageNet norm) for every architecture; test accuracy from the best-validation checkpoint. Bootstrap 95% CI per number.

## Results (test N = 205, one image per unseen source)
| Architecture | Unmasked % (95% CI) | Masked % (95% CI) | Masking Δ (pp) |
|---|---|---|---|
| SWIN-Small | 84.9 (80–89) | 81.0 (76–86) | −3.9 |
| DenseNet201 | 82.4 (77–88) | 82.0 (77–87) | −0.5 |
| ConvNeXt-Large | 81.5 (76–87) | 79.5 (74–85) | −2.0 |
| ViT-Base | 81.5 (76–86) | 81.0 (75–86) | −0.5 |
| SWIN-Tiny | 80.0 (75–85) | 82.4 (77–87) | +2.4 |
| EfficientNet-B0 | 78.5 (73–84) | 75.1 (69–81) | −3.4 |
| ResNet50 | 76.1 (70–82) | 79.0 (73–84) | +2.9 |
| MobileNetV3-Large | 75.1 (69–81) | 80.0 (74–85) | +4.9 |

## Findings
1. **Masking has no effect on clean data.** Mean Δ = **0.00 pp** (sd 3.15; 3 of 8 positive). Not significant: sign test p = 0.73, paired t-test p = 1.00, Wilcoxon p = 0.95. **The original "+3.06 pp, 20/21 architectures" was entirely a data-leakage artifact** (masked split leaked 80% of its test set; unmasked leaked none).
2. **No architecture is significantly best.** Clean accuracies span 75–85%; every 95% CI (±~5 pp at N=205) overlaps the others. SWIN-Small is numerically highest unmasked (84.9%) but tied within CI.
3. **Clean accuracies are 4–12 pp below the leaky numbers** (e.g., SWIN-Small 84.9% clean vs 93.05% leaky), quantifying the inflation.

## Honest paper conclusion
Segmentation-based masking does **not** improve burn severity classification once data leakage is removed; no single architecture dominates; the end-to-end pipeline ties a plain classifier; and the model does not generalise to external clinical data. The contribution is a **leakage-corrected benchmark and a quantified cautionary lesson** on how augmentation-before-splitting inflates results in medical-imaging benchmarks.

## Caveat (per reviewer)
Test N=205 gives wide CIs (±~5 pp); differences under ~6–7 pp are not resolvable. This is reported honestly on every number. The paper frames the benchmark as: 21 architectures compared, no statistically significant winner, on a gold-standard split.

## Post-hoc power (masking effect, paired t-test)
Computed from the eight full-precision masking deltas (mean 0.0000 pp, **SD 3.1506 pp**,
ddof=1), one-sample/paired t-test, alpha=0.05 two-sided, via noncentral-t (statsmodels
`TTestPower`):

| Quantity | Value |
|---|---|
| 80%-power minimum detectable effect (exact noncentral-t) | **3.64 pp** (Cohen d 1.156) |
| z-approximation MDE (anti-conservative for n=8) | 3.12 pp |
| Power at the naive split's apparent 3.1 pp effect | **0.667** |

The manuscript reports the exact noncentral-t figure (3.6 pp) and the two-thirds power at
3.1 pp; a reviewer must use the t-based (not z-based) calculation to reproduce 3.6 pp.
The observed effect is exactly 0.0 pp (three architectures up, five down), so the result
is a clean null, not an attenuated positive.
