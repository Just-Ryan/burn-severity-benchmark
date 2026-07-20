# External-Dataset Validation Report (BIP_US)

> Real out-of-distribution test run locally on 2026-07-20. Script: `scratchpad/eval_bipus.py`; raw output: `external_validation_BIPUS.json`. This is the external validation the paper was missing (Practical Task 2 / reviewer point D3). **The result is important and unfavorable — and reporting it honestly is what makes the paper trustworthy.**

## The dataset (why it's a fair external test)
- **BIP_US** — Biomedical Image Processing Group, University of Seville + Virgen del Rocío Hospital. 94 **clinical** burn photographs, captured ~2005.
- **Genuinely independent:** hospital-sourced, predates the web-scraped Roboflow/Kaggle burn-image ecosystem our model trained on — it **cannot** overlap the training data (the contamination risk that plagues web-scraped burn datasets does not apply here).
- **License:** free for research use with attribution to the BIP Group, Univ. of Seville.
- **Labels:** burn **depth** — Superficial dermal (42), Deep dermal (32), Full-thickness (20). Degree mapping: superficial + deep dermal → 2nd degree; full-thickness → 3rd degree. No epidermal/1st-degree images, so this is a **2nd-vs-3rd** probe.

## Result: the model does not generalize
| Metric | Full pipeline | Unmasked classifier |
|---|---|---|
| 2nd-vs-3rd accuracy (deep→2nd) | **39.4%** | 35.1% |
| 2nd-vs-3rd accuracy (deep→3rd) | 31.9% | 25.5% |
| **Majority-class baseline (always "2nd")** | **78.7%** | 78.7% |
| Segmentation success rate | 82/94 = 87% | — |

**The model performs far below the trivial majority-class baseline (39% vs 79%)**, under every reasonable label mapping.

### It systematically UNDER-grades severity (the clinically dangerous direction)
- **59%** of images were assigned a *lower* severity than truth; only **2%** higher.
- Per depth subclass (pipeline predictions):
  - Superficial dermal (n=42, true 2nd): 27 → 2nd (64% ok), 13 → **1st**, 2 → 3rd.
  - Deep dermal (n=32, true 2nd): **25 → 1st (78%!)**, 7 → 2nd.
  - Full-thickness (n=20, true 3rd): only **3 → 3rd (15%)**, 7 → 2nd, **10 → 1st (50%)**.

Half of the full-thickness (3rd-degree) burns — the most severe, graft-requiring injuries — were labeled **first-degree** by the model. In a clinical setting that is the most harmful error class.

## Honest caveats (state these in the paper, don't hide behind them)
1. **Label-protocol difference.** BIP_US uses depth-for-grafting terminology; "deep dermal" sits on the 2nd/3rd boundary. Some disagreement is expected. But the *direction and magnitude* (below-baseline, 59% under-graded, 50% of full-thickness called 1st-degree) far exceed what protocol mismatch explains.
2. **Domain shift.** 2005 clinical photographs (different cameras, lighting, surgical context) vs web-scraped training images. This shift is exactly what real deployment would face — which is the point of external validation.
3. **Small N (94), 2nd/3rd only.** Directional, not a precise generalization estimate.

## What this means for the paper
- **Delete/replace the current "generalization" claim** (the 3 cherry-picked internet images in §4.6 that were "all correct"). Replace with this quantitative external test.
- **Add a headline limitation:** the system is validated **in-distribution only**; on independent clinical data it does not currently generalize and tends to under-grade severity. Future work = domain adaptation, clinically-labeled multi-source training data, and calibration.
- This **reframes the contribution** accurately: a controlled benchmark + masking ablation on one dataset, **not** a deployable clinical tool. That honesty is a strength — it pre-empts the exact rejection a reviewer would issue, and it is the truthful scientific story.
- It composes with the in-distribution findings: the pipeline ties a plain classifier end-to-end (p=1.0), and the whole system does not transfer to external clinical images. Together these make a modest but **fully honest** paper. *(Correction, 2026-07-20: an earlier version of this line said "masking helps classification given clean in-distribution masks." The subsequent leak-free re-run showed masking has no effect even with clean annotation-derived masks — mean 0.0 pp, p=1.0. The masking claim is retracted; see `CLEAN_BENCHMARK_RESULTS.md`. The external result below stands unchanged.)*
