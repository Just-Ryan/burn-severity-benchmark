# Independent Audit — *A comparative study of deep learning approaches for automated burn injury segmentation and severity classification*

**Manuscript:** TURKJELECENGCOMPSCI-S-26-02236 (TÜBİTAK Turkish Journal of Electrical Engineering & Computer Sciences, diamond OA)
**Status at audit time:** submitted, under review
**Audit date:** 2026-07-25
**Auditor:** lead reviewer, synthesising seven independent dimension audits plus adversarial verification of every critical/major claim. Every number below was recomputed from raw files; refuted findings were dropped before this document was written.

**Source of truth:** `01_paper/benchmark2-proof/results/*.json`, `01_paper/statistics/*.json`, `05_code/`, `01_paper/SUBMISSION/manuscript.tex`.

---

## 1. Executive verdict

### Score: **7.0 / 10** as a piece of science. **5.5 / 10** as a submitted manuscript.

The gap between those two numbers is the whole story. The underlying work is better than the paper that describes it.

**Why 7.0 for the science.** I attempted to break this project and mostly failed. I independently rebuilt the source-grouped split from the raw Roboflow dataset and reproduced the *exact* 205 test filenames used in the paper. Every seed-42 headline number recomputes exactly from the shipped per-image predictions (internal classifier 82.439, pipeline 81.463; external 74.295 / 69.906; McNemar b/c = 20/18 and 54/40 with exact p = 0.8714 and 0.1797). Table 5's BIP_US matrix reproduces cell-for-cell and both balanced accuracies (30.47 → 30.5, 35.03 → 35.0) recompute from the 94 raw rows. The retracted leakage artifact reproduces exactly (+3.0571 pp, 20 of 21 architectures). The pooled masking null reproduces exactly (n = 24, +0.54878 pp, 13 positive, Wilcoxon p = 0.3238). No superseded pre-leakage number (93.05, 91.41, 88.81, 84.9, 39.4) leaks into the current manuscript. Masking is genuinely oracle — `build_clean_split_v2.py:54-68,101-102` fills ground-truth polygons, no model involved — so the null cannot be blamed on a weak segmenter. No test-time augmentation anywhere. No-detection images are counted as errors against a fixed denominator in every evaluation loop, which is why the paper is *allowed* to show a 54.2% external collapse for the strict pipeline instead of hiding it.

Most importantly: three undergraduates found a leakage artifact in their own favourable result, ran a pre-registered fresh-seed confirmation, watched a p = 0.041 effect evaporate, and reported the null. That behaviour is rare in this literature and it is the thing worth defending.

**Why only 5.5 for the manuscript.** The paper's selling point is reporting discipline, and it does not consistently meet its own standard:

1. It promises Wilson confidence intervals three times (`:58`, `:70`, `:119`), indicts prior work for omitting them, and then **prints not a single numeric interval anywhere.** It draws a conclusion — "The Wilson intervals overlap" — from intervals the reader never sees.
2. The 319-image "clean external set" contains only **175 unique source photographs**; 269 of 319 images (84%) are augmented copies of another image in the same set. The paper applied source-grouping to the internal set and not to the external set — the exact failure the paper exists to warn about, on the set carrying its most load-bearing claim.
3. The internal split still contains **residual source-level leakage**: 9 duplicate photograph clusters hide behind distinct filename source-ids, 5 straddle folds, and 2 training photographs sit in the 205-image test set. `manuscript.tex:90` says categorically "We verified that no source photograph appears in more than one fold." That statement is false, and the paper's own advertised pHash screen catches it at Hamming distance 0.
4. The minimum detectable effect of 3.64 pp — the yardstick for the paper's central negative result, invoked three times — is described as "at N = 205". It has nothing to do with N = 205. It is a one-sample t-test MDE over **n = 8 architectures**, using SD = 3.1506 pp from an eight-architecture run **the manuscript never mentions**. No referee can reproduce 3.64 from anything the paper reports.
5. Two figure/table captions infer "no difference" from **overlapping error bars** in a paired design — a textbook fallacy. The correct seed-paired test, never run, gives internal difference +3.74 pp, SD 0.28, t = 23.0, p = 0.0019. The paper under-claims from a position of not having looked, and internally its ±1 SD bars do not even overlap.
6. `manuscript.tex:155` and the Figure 3 caption claim an "external shift toward lower severity". The external confusion matrix says 51 under-graded vs 45 over-graded, mean predicted grade 1.639 vs true 1.636. The figure the sentence points to refutes the sentence. Meanwhile the *internal* panel — described only as "second-degree difficulty" — has the larger downward bias (23 under vs 15 over). The labels are effectively swapped.

None of these overturns the central thesis. All six are checkable by a competent referee in under an hour, and every one lands on the paper's own chosen high ground. That is what costs 1.5 points.

**Bottom line.** This is a genuinely good undergraduate research project with an important, publishable, honest negative result, wrapped in a manuscript that repeatedly asserts rigour it did not quite execute. Fixing the six items above costs perhaps 20 hours and converts the paper's largest vulnerabilities into further demonstrations of its own thesis.

---

## 2. Prioritized action table

Effort key: **S** ≤ 1 h · **M** 1–4 h · **L** 4–15 h · **XL** > 15 h or requires GPU re-runs.
Timing key: **NOW** = do before any decision arrives (repo/artifact hygiene, no manuscript change) · **REV** = revision-stage manuscript edit · **NOW+REV** = prepare now, land at revision.

| # | ID | Sev | Eff | When | Issue | Exact fix |
|---|----|-----|-----|------|-------|-----------|
| 1 | STAT-06 | **Major** | S | REV | Wilson CIs promised at `:58`, `:70`, `:119`; **zero printed**. | Replace `:147` "The Wilson intervals overlap." with the numbers: internal clf 82.4 [76.7, 87.0] vs pipe 81.5 [75.6, 86.2]; external 74.3 [69.2, 78.8] vs 69.9 [64.7, 74.7]. Add to the single-seed reference rows of Table 4 only (Wilson is undefined on a 3-seed mean). Do **not** add a Wilson column to the multi-seed rows. |
| 2 | SI-03 | **Major** | S | REV | "external shift toward lower severity" (`:155`, Fig-3 caption `:425`) contradicted by the matrix: 51 under vs 45 over, mean pred 1.639 vs true 1.636. | `:155` → "…with second degree the hardest class internally and, externally, errors concentrated between first and second degree in both directions with no net severity bias". `:425` → state 41 second→first against 28 first→second, mean predicted 1.64 vs true 1.64, and that the under-grading finding is **specific to BIP_US**. Add to Discussion: BIP_US under:over = 55:2 vs clean external 51:45 — evidence the failure is clinical-domain shift, not a generic model bias. This *strengthens* the paper. |
| 3 | STAT-07 | **Major** | S | REV | Error-bar / CI-overlap fallacy at `:147`, `:346`, `:408`; internally the ±1 SD bars do **not** overlap, so `:408` is factually false against its own figure. | Delete the overlap reasoning. Replace with the two-part correct statement: seed-paired differences 3.90 / 3.90 / 3.41 pp, paired t p = 0.002 (n = 3, initialisation variance only, localiser held fixed); McNemar on images p = 0.87 / 0.18, underpowered — 80% power near **8.5–9 pp** at the observed discordance. |
| 4 | SI-02 / STAT-02 / STAT-03 / SI-05 | **Major** | M | REV | MDE 3.64 pp labelled "at N = 205" three times (`:119`, `:137`, `:322`); it is n = 8 architectures, SD 3.1506 pp, from a run the paper never describes (`clean_benchmark_results.json`, mean delta exactly 0.00 pp, 3/8 positive). Recomputed for the design actually reported: n = 11 → 2.00 pp; n = 24 pooled → 1.30 pp. | Delete "at $N=205$" everywhere. **Preferred:** replace the MDE framing with a CI on the effect — pooled masking +0.55 pp, 95% CI **−0.37 to +1.47 pp** (n = 24, paired t p = 0.23), which says the same thing without the observed-power objection. Disclose the 8-architecture pilot in one sentence in §Res:mask. Soften "All effects are below the MDE" — under an n = 11 yardstick the seed-42 transformer +3.12 pp is *not* below it; rest that null on the failed replication, not the MDE. |
| 5 | SI-01 | **Major** | M | NOW+REV | External set is **not** source-grouped: 319 images / **175** sources; 84% sit in a multi-copy group. Wilson CIs and the external McNemar p = 0.18 are pseudo-replicated. | Do **not** rebuild (seeds 0 and 2 have no saved external predictions; the whole external column would need re-running). Disclose at `:121`: "the 319 images derive from 175 source photographs; unlike the internal test set the external set was not deduplicated to one image per source". Add a sensitivity line to the Table 4 note: per-source majority vote, N = 175 → clf **73.7**, pipeline **72.6**, McNemar b = 24 / c = 22, exact p = 0.88; over 5,000 random one-per-source draws the mean gap is 3.46 pp (95% range 0.0–7.4) and p < 0.05 in 0.4% of draws — **no dedup variant changes the conclusion.** Add one Limitations sentence naming the asymmetry. |
| 6 | CR-01 | **Major** | M | NOW+REV | Residual internal leakage: 9 duplicate photograph clusters across distinct source-ids; 5 straddle folds; **2 of 205 test images have a pixel-duplicate in training** (corr ≈ 1.000, mean abs diff < 1.3/255). One pair carries contradictory labels (class 0 vs class 1). Paper says categorically "no source photograph appears in more than one fold" (`:90`). | Do **not** rebuild the split — it would invalidate every CI, McNemar, and multi-seed mean to fix 0.98% of the test set. Replace `:90` with the true, threshold-qualified statement: grouping was by file name; applying the paper's own flip-aware pHash/dHash screen to the 1,370 sources finds a small residual (9 strict-threshold clusters, 5 straddling folds, 2 test images affected = 0.98%, one pair with contradictory ground truth); three orders of magnitude below the 80.5% naive leakage and far below the MDE. **Report it yourselves** — it converts the paper's weakest point into another instance of its thesis. |
| 7 | CR-03 / SI-04 / STAT-14 | **Major** | M | **NOW** | Table 4's standalone-YOLO row (79.5 / 68.7 / bal 74.6, `:142`, `:340`) traces to notebook cell 26, the **only** code cell with zero stored outputs; `standalone_yolo_thresholds.json` exists nowhere on disk or in the repo. Archived values are the *less* favourable conf-0.25 run (78.5 / 58.0). | Re-run cell 26 (inference only, deterministic, minutes on any GPU), commit `standalone_yolo_thresholds.json` into `benchmark2-proof/results/` **and** the repo, and save the notebook **with the cell's outputs retained**. If unrecoverable: footnote Table 4 that the conf-0.05 row is reported from the run log and give the archived conf-0.25 values alongside. Do not delete the row — that would make the head-to-head less fair. |
| 8 | STAT-01 | Minor | S | REV | All six printed ± values are **population** SDs (`np.std`, ddof = 0) over n = 3; sample SDs are 22.5% larger. Bug: `colab-benchmark2.ipynb` cell 20. | Recompute from the stored `seeds` arrays (no retraining). `:142` and `:338-339` → 82.6 ± 0.7, 76.6 ± 1.6 (bal 80.1 ± 1.8), 78.9 ± 1.0, 73.4 ± 2.5 (bal 77.9 ± 3.4); `:151` → 78.9 ± 1.0. Abstract `:48` prints no ± — **no change needed there**. Add "(n = 3, ddof = 1)" to §Statistics. Note Figure 2 has no generating script in the tree; if it cannot be regenerated, change the caption to "error bars show the spread across three seeds" or plot min–max. |
| 9 | STAT-05 | Minor | S | REV | "the classifier won on both sets in all three seeds" (`:48`, `:142`, `:331`) is false for **external balanced accuracy**: seed 1 gives pipeline 80.14 vs classifier 79.96. | `:142` → "had the higher accuracy on both sets in all three seeds; on external balanced accuracy it led in two of three". `:331` → "wins on accuracy on both sets in all three seeds, and on external balanced accuracy in two of three". `:48` → minimal two-word fix, "had the higher accuracy" (abstract is already ~297 words). Optionally disclose that the seed-1 external accuracy margin is 0.63 pp = 2 of 319 images. |
| 10 | SI-12 | Minor | S | REV | External cleaning under-reported: abstract says "removed 118 contaminated images"; 226 images were actually removed, and the released set retains 175 of 199 sources, contradicting "56 of 199 sources … all were removed" (`:121`). | State the full chain in §Mat:eval and Table 1: raw 1,371 images / 199 sources → 118 images perceptual-hash identical to training → 226 images removed in total (24 source groups removed wholesale = exactly 118 images; flagged images from surviving sources removed individually) → fourth degree dropped → 319 images / 175 sources, 139/157/23. **Resolve the 56-vs-24 source discrepancy before any repo release** — a referee running the released check will find 175 of 199 sources still present. |
| 11 | STAT-08 | Minor | S | REV | ± is cross-seed training noise on a fixed test set; Wilson widths are ~10 pp, 1.3–4.4× wider. Reader will read ±0.6 as precision. | One sentence at `:119`: "± values are the standard deviation across three random initialisations evaluated on a fixed test set; they quantify training reproducibility, not sampling uncertainty, which is given by the Wilson intervals (~10 pp wide at these sample sizes)." Pairs with item 1. |
| 12 | CR-12 | Minor | S | REV | Multi-seed varies only the classifier — `yolo1` is loaded once outside the seed loop (cell 20 line 9). Pipeline SD contains **no segmenter variance**. Also all figures and both McNemar tests use seed 42, which is the *worst* of four runs externally for both arms. | Add to §3: "the localiser was held fixed across seeds, so the pipeline's cross-seed SD reflects classifier variability only and understates the full pipeline's variance." State the seed in the Fig-3 caption. |
| 13 | SI-10 | Minor | S | REV | Fig-3 caption says "a representative seed"; it is seed 42, above all three multi-seed internal values (81.46 vs 78.05/78.54/80.00) and below all three external values (69.91 vs 70.53/74.29/75.24). The paper itself says at `:147` that seed 42 was the pipeline's most favourable run. | Caption → "on the seed-42 models (the same models used for the McNemar tests in Table 4); seed 42 is the pipeline's most favourable internal run and its least favourable external run — see Table 4 for multi-seed means." Also label the unlabelled seed-42 reference rows in Table 4. |
| 14 | SI-07 | Minor | S | REV | Methods promise sign and paired-t tests (`:119`); neither is reported. | Either report them (seed-42 sign test p = 0.065, paired t p = 0.041 — both *strengthen* the replication narrative) or delete them from the Methods sentence. |
| 15 | SI-08 | Minor | S | REV | Table 3 declares the two cropping conditions "not significant" although no test was run (the adjacent column correctly says "not run"). | Replace with "not tested (single seed)" or an em-dash. Exact means for the record: cropped +0.0000 pp (3/8 positive), masked+cropped +0.0610 pp (4/8). |
| 16 | CR-07 / STAT-09 | Minor | S | REV | "Mann-Whitney p = 0.33" (`:137`, `:322`) is the **one-sided** value; two-sided is 0.66. Separately, the Table 3 footnote attaches this pooled p to a seed-42 subgroup sentence where the actual value is p = 0.055. | Say "one-sided" explicitly, or give both. Rewrite the footnote to separate the two analyses: seed-42 transformer subgroup (+3.1, 5/5, paired t p = 0.04, MWU p = 0.05) → **did not survive** fresh seeds (pooled +0.55, Wilcoxon p = 0.32, MWU one-sided p = 0.33). The replication story lands much harder this way. |
| 17 | SI-13 | Minor | S | REV | The +3.06 pp artifact is attributed to leakage alone, but the two naive runs also differ in split ratio (70/15/15 vs 90/6/4) and test set (518 vs 143 images, sharing only 19). Meanwhile the **decisive within-model evidence is omitted**. | Add the clean evidence to §Res:leak: the *same* masked classifier scored **95.9%** on the 417 test images whose source appeared in training and **82.2%** on the 101 whose source did not — a 13.7 pp gap, one model, one test set, no confounds. Then concede in one clause that the naive pair also differed in split ratio and test set. The paper is currently weaker than its own data. |
| 18 | SI-14 | Minor | S | REV | BIP_US is reported for the pipeline only. `external_validation_BIPUS.json` also holds `pred_unmasked`: the plain classifier scores **25.9 / 28.1** balanced — worse than the pipeline's 30.5 / 35.0. The paper's headline winner loses on the only genuinely clinical set, and this is not reported. | Add one sentence or a Table 5 column. Both are below the 50% trivial baseline so it means little — which is exactly why omitting it is a needless selective-reporting exposure, and why including it *supports* the thesis that in-distribution ranking does not predict clinical usefulness. |
| 19 | STAT-12 | Minor | M | REV | External balanced accuracy is driven by a 23-image third-degree class: one image moves it 1.45 pp. Per-class Wilson widths 24–38 pp. Bootstrap on balanced accuracy: clf [73.2, 83.4], pipe [58.6, 74.0] — 3.5–5.5× the reported ±. | Report per-class recalls with n, plus the stratified-bootstrap intervals. Quantifying the fragility of your own headline metric is exactly the behaviour the paper argues the field is missing. |
| 20 | SI-11 | Minor | S | REV | Both head-to-head architectures were selected as best-of-11 on the **same 205-image test set** they are then evaluated on, and the selection is unstable (`clean_benchmark_results.json` puts Swin-Small on top instead). Never acknowledged. | One sentence in §Mat:bench stating the selection basis, plus one Limitations sentence on the resulting optimistic bias and that no architecture is separable within the intervals. Optionally report the mean over all 11 architectures as the unbiased comparator. |
| 21 | CR-02 | Minor | S | NOW+REV | BIP_US is evaluated through Resize(256)+CenterCrop(224) while training used Resize(224,224). **This is not a bug in the measurement** — it is the deployed app's own transform (`flask_server/app.py:48-53`), and Table 5 is captioned "the deployed pipeline". But it is undisclosed, and `:103` claims the robust pipeline "matches the deployed application", which is untrue at the transform level. | One Methods sentence: the BIP_US protocol runs the deployed inference path verbatim, including its resize+centre-crop, which differs from the square resize used in training; reported as an as-deployed evaluation. Soften `:103`. Optional sensitivity re-run with matched preprocessing — expect a few points, not a reversal (the unmasked branch over-predicts "first" *more*, 53/94 vs 48/94, and the 12 no-detection images behave the same, so the crop is not the driver). |
| 22 | CR-09 | Minor | S | REV | The timing benchmark measures Python/OpenCV overhead, not model cost: Swin-Tiny (~4.5 GFLOPs) 23.7 ms vs ConvNeXt-Large (~34.4 GFLOPs) 25.8 ms — a 7.6× compute ratio measured as 1.09×. Single run of 60 images, batch 1, warm-up images re-timed inside the loop, no dispersion. | Cheapest honest fix: relabel as end-to-end per-image latency including CPU preprocessing at batch size 1, and add one sentence that preprocessing dominates so these do not rank the networks by compute. (Or re-measure properly: hoist preprocessing, ≥3 repeats × ≥100 iterations, report median and IQR.) Also fix the stale "H100" in the notebook title cell — the run was an A100. |
| 23 | SI-16 / STAT-13 | Nitpick | S | REV | "against a chance level of 50 percent" mischaracterises the baseline: the model emits three labels, 51% of its BIP_US predictions are "first degree", a class absent from the ground truth. | "against 50 percent for a trivial constant predictor on this two-class probe". Add the bootstrap CI (30.5%, 95% CI 21.3–40.9), which contains 33.3% — i.e. indistinguishable from uniform three-way guessing. More damaging to the model, better for the paper. |
| 24 | SI-09 | Nitpick | S | REV | Table 3's footnote uses "8 architectures" for two different, non-overlapping subsets in adjacent sentences (cropping 8 = 3 transformers + 5 convnets; multi-seed 8 = 4 + 4). | Name the four transformers and four convnets used in the multi-seed confirmation, or write "a different subset of 8". |
| 25 | SI-17 | Nitpick | S | REV | Two claims asserted without their numbers: "second degree is the hardest class to segment" (no per-class metric in Table 2) and the strict-vs-robust threshold effect (no no-detection counts). | Add per-degree mask mAP50 ≈ 0.63 / 0.47 / 0.75 as a Table 2 footnote, and the no-detection counts: at conf 0.25 the localiser returned no region on 10 of 205 internal and 66 of 319 external, versus 0 and 1 fallbacks at 0.05. The 66 images are almost the entire 54.2% vs 69.9% external gap. |
| 26 | CR-08 | Minor | S | **NOW** | `statistics/benchmark1_masking_pooled_analysis.json` reports Wilcoxon p = 0.2336 and MWU 0.6014/0.3007 — **contradicting the manuscript's 0.32 / 0.33**, even though its per-run deltas are byte-identical to mine. My recomputation matches the manuscript (0.3150 / 0.6643 / 0.3321). | Recompute the file with the same scipy call and record the scipy version, the exact `alternative`, and the zero-handling method in the JSON. If it ships as-is, a referee finds three artifact p-values disagreeing with three paper p-values. |
| 27 | SI-04b | Minor | S | **NOW** | `statistics/BENCHMARK2_AND_HEADTOHEAD.md:229-237` still says the multi-seed masking results "are not yet exported" — they were exported on 25 Jul and sit in the same directory. This stale text ships in the release repo and misled one of my own auditors. | Delete or update the passage before release. |
| 28 | CR-11 | Minor | S | **NOW** | The split depends on unsorted `glob.glob()` ordering before `rng.shuffle`; the built-in check only asserts zero fold overlap, so a divergence would be silent. (Empirically it did not bite — sorted and unsorted both reproduce the exact 205.) | Wrap both globs in `sorted(...)`, sort the per-class source list before shuffling, and **ship the 205-filename test manifest as JSON** so anyone can assert an exact match instead of re-deriving it. Two lines plus one file. |
| 29 | CR-13 | Nitpick | S | **NOW** | Seeding is incomplete: no `random.seed`, no `cudnn.deterministic`, no DataLoader `generator`/`worker_init_fn`, plus AMP. "Seed 42" implies bitwise reproducibility the code does not deliver. | Add the missing seeds and determinism flags; state in Methods that runs reproduce to roughly ±0.5 pp rather than exactly. Also pass the true correct-count (169/205) to `wilson()` in cell 14 instead of reconstructing it from a rounded percentage. |
| 30 | CR-14 | Nitpick | S | **NOW** | `benchmark1_masking_seeds01_confirmation.json` contains 6 orphan **seed-2** unmasked-only runs despite its name; they form no pairs and are correctly excluded, but the file will confuse a referee. | Drop them or add a top-level note field explaining they come from an aborted third replication. |
| 31 | SI-05b | Minor | S | **NOW** | `statistics/CLEAN_BENCHMARK_RESULTS.md` opens "The gold-standard re-run that determines the paper's conclusion" and asserts "Mean Δ = 0.00 pp" — flatly contradicting the manuscript's +1.5/+0.55, in the package the Data Availability statement promises to publish. | Add a one-line SUPERSEDED header: it is the eight-architecture pilot, retained because the manuscript's MDE derives from its SD. |
| 32 | CR-10 | Minor | S | REV | `:90` reads as though validation/test contain original photographs. For ~71% of them the retained image is one arbitrary augmented rendering (all three Roboflow copies are augmented; pairwise mean abs diff 36–92 grey levels). | One clause: "because the public release stores only augmented renderings for most sources, the retained image is one augmented variant rather than the original photograph, identically for every condition and system." No bias — all systems see identical images — but it is a free honesty win. |

**Do NOW (repo/artifact only, no manuscript change, ~4–6 h total):** items 7, 26, 27, 28, 29, 30, 31, plus the disclosure prep for 5, 6, 10, 21.
**Everything else is revision-stage.** Do not contact the editor mid-review to volunteer corrections unless something is *wrong* in a reported number — nothing is. Prepare a self-identified-corrections section for the response letter.

---

## 3. The science

### 3.1 Is it sound? — Yes, in its core, with two disclosure failures at the edges.

**The central claim chain holds:**

1. *A file-level split of an augmented dataset leaks catastrophically.* Verified. `DATA_LEAKAGE_FINDING.md:10` — 417 of 518 masked test images (80.50%) shared a source with training; the separately partitioned unmasked set leaked none. The leakage-era code is archived and inspectable (`YoloAlone/DatasetSplit.py:52-58`, `newway-seqcode/dtSplit.py:44-49` — both `train_test_split` over file paths, no grouping).
2. *That leakage manufactured a masking benefit.* Verified: +3.0571 pp over 20 of 21 architectures, recomputed from the archived report table, and overwhelmingly "significant" in the leaky regime (Wilcoxon p = 6.9e-05). **The strongest thing in this paper is that the authors threw that away.**
3. *After a source-grouped split the benefit vanishes.* Verified: pooled +0.54878 pp over 24 architecture-seed pairs, 13 positive, Wilcoxon p = 0.3238, transformers +0.77 vs convnets +0.33 (MWU one-sided p = 0.332). Reproduces exactly from two released JSONs.
4. *A plain classifier is the most accurate single system.* Verified in direction and stability, though see §4 on how it should be argued.
5. *The model does not transfer to clinical images and under-grades.* Verified on BIP_US, cell-for-cell. 55 of 94 under-graded vs 2 over-graded — a 27.5:1 ratio. This is the paper's most important and most quotable finding, and it is solid.

**The oracle-mask design is the paper's best structural decision.** Because the masking ablation used ground-truth polygons, "a better segmenter could not have rescued a masking gain that is absent even with perfect masks" (`:169`) is a genuinely strong argument, and it is honestly maintained throughout — the 83.9% oracle number is quarantined below the rule in Table 4 and explicitly disowned at `:151`.

### 3.2 What is verified, exactly

- Source-grouped split rebuilt from raw data → train/valid/test = 2425/206/205, class counts 86/63/56, **zero** fold overlap by file-group, test filenames **identical 205/205** to `preds_internal.json`. Invariant to glob ordering.
- Every value in Tables 1, 2, 4, 5, 6 and every seed-42 delta in Table 3 recomputes from raw files.
- Both McNemar tests recompute to six decimals; the exact conditional binomial (not χ²) is the right choice at these discordant counts.
- Both Figure 3 confusion matrices recompute cell-for-cell from `preds_internal.json` / `preds_external.json` and the rendered PDFs carry the same cells.
- Table 3's architecture-coverage claim (11 masked/unmasked, 8 cropping, omitting exactly ConvNeXt-Tiny/Swin-Base/Swin-Large) is verified against a 38-row JSON.
- The seed sets {0,1,2} and {0,1,42} are correctly described and **never conflated** — and the paper says so defensively at `:105`.
- External decontamination is real: an independent flip-aware pHash+dHash check of all 319 external images against all 3,424 primary images finds **zero** within Hamming distance 10; closest match at 18 of 127 bits.

### 3.3 What is weak

| Weakness | Severity |
|---|---|
| External set not source-grouped (175 sources behind 319 images) — the paper's own rule applied unevenly | **The single highest-probability rejection trigger.** Not because it changes anything (it doesn't — see item 5), but because of *where* it lands. |
| Residual internal leakage falsifying a categorical verification claim | Major credibility, negligible numerically (0.98% of test set) |
| A ground-truth contradiction in the dataset (same photo labelled Degree 1 and Degree 2), plus a second such pair at a looser threshold | Independently interesting; the paper already flags community labelling as a limitation but has direct evidence it never uses |
| MDE unreproducible and mislabelled; source run undisclosed | Major, because it is the yardstick for the central negative result |
| Both head-to-head architectures chosen on the test set they are evaluated on | Classic winner's curse, unacknowledged; partly symmetric so it does not flip the ordering |
| N = 205 internal / 94 BIP_US / 23 third-degree external images | Structural. Nothing to be done except state it (the paper does, at `:177`) |
| Single web source, community labels, no fairness/skin-tone analysis | Correctly and fully disclosed at `:177`. Good. |

---

## 4. Statistics — the statistician's verdict

**Verdict: the arithmetic is honest; the statistical *reporting* is not yet defensible.** Every test that was run was run correctly. The problem is a set of promised-but-absent statistics, one mislabelled yardstick, and one invalid inference rule — in a paper that indicts the field for exactly these habits.

**What is done right:**
- Exact McNemar on paired discordant counts (not χ²) — the right test, right design, reproduces to six decimals.
- Wilcoxon signed-rank correctly two-sided; correct pooling across two Kaggle kernels (label vectors are byte-identical across all 38 seed-42 runs and the seeds-0/1 file, so the join is legitimate).
- The MDE, whatever its labelling problems, uses exact noncentral-t rather than the anti-conservative z-approximation, and `PROJECT_FULL_REPORT.md:435` explicitly says why. That is better practice than most papers manage.
- Fixed-denominator evaluation with no-detections counted as errors.
- A pre-registered replication that killed the authors' own p = 0.041 result.

**What must change:**

1. **Print the intervals.** Internal clf 82.4 [76.7, 87.0], pipe 81.5 [75.6, 86.2], oracle 83.9 [78.3, 88.3], strict pipe 79.0 [72.9, 84.0]; external clf 74.3 [69.2, 78.8], pipe 69.9 [64.7, 74.7], strict pipe 54.2 [48.7, 59.6]. Widths ≈ 10 pp. That number — 10 pp — is the single most useful thing the paper can give a reader, because it is what stops them over-reading ±0.6.
2. **Replace the MDE with a confidence interval on the effect.** Pooled masking +0.55 pp, 95% CI **−0.37 to +1.47** (n = 24, paired t p = 0.23). This says "no benefit found, and benefits larger than about 1.5 pp are excluded" without any observed-power objection, without depending on an undisclosed SD, and without the n-mismatch. It resolves items 4, 11 and half of 3 at once. **This is the highest-leverage statistical edit available.**
3. **Run the paired test you already have the data for.** Seed-paired internal difference +3.74 pp, SD 0.28, t = 23.0, p = 0.0019; external +3.24 pp, p = 0.19; external balanced +2.18 pp, p = 0.24. Then state the caveat honestly: n = 3, seeds are not the unit of clinical generalisation, and the localiser was held fixed so this understates pipeline variance. The correct framing — "highly stable across initialisations, not resolvable across images, because those are different questions" — is more interesting and more defensible than what is written.
4. **State the power of the comparison you actually care about.** At the observed discordance (38 of 205 internal, 94 of 319 external), exact McNemar reaches 80% power only near **8.5–9 pp**. The observed 3.7 pp gap is less than half that. Say so; it is the paper's strongest defence of "consistent rather than significant", and it is missing entirely (`grep -i power manuscript.tex` returns nothing).
5. **ddof = 1, and say so.** 82.6 ± 0.7 / 76.6 ± 1.6 / 78.9 ± 1.0 / 73.4 ± 2.5, balanced 80.1 ± 1.8 / 77.9 ± 3.4.
6. **Label every tail.** One-sided MWU reported as bare "p = 0.33".
7. **Name the exploratory subgroup as exploratory.** The transformer/convnet split was suggested by the seed-42 results, not pre-specified — which is precisely *why* it was subjected to a fresh-seed confirmation. Saying so converts a latent criticism into evidence of discipline. Multiplicity is a non-issue here because every surviving conclusion is a null (Holm on the four reported p-values leaves min adjusted p = 0.72), but the exploratory status should be stated.

**On the "consistent rather than significant" framing:** the intent is admirable and I would keep it. As executed, it is under-claiming from a position of not having looked, and it is justified by an invalid argument (marginal-interval overlap in a paired design). Fix the justification, keep the conclusion.

---

## 5. Code and reproducibility

**This is the strongest dimension of the project.** The Benchmark-2 code is better than most published medical-imaging code, and I say that having tried to break it.

**Verified correct:**
- The source-grouped split is exactly reproducible and produces the exact 205 test filenames used in the paper.
- Masking is oracle (ground-truth `fillPoly`), never model-derived.
- Fixed denominators, no silent drops, in all four evaluation loops (cells 9, 13, 16, 26). Balanced accuracy uses `np.where(pp<0, 99, pp)` so a no-detection can never be credited.
- No test-time augmentation anywhere; `augment=False` throughout.
- Multi-seed runs are genuine independent retrains (`timm.create_model(pretrained=True)` per seed), not cached; resumability keys on `_seeds_done`, not model files.
- Label mapping consistent end to end (`0/1/2` directories → ImageFolder indices → YOLO class ids). None of the classic remap bugs. No dropped class.
- Class weights computed from the actual training distribution only.
- Model selection on validation only; the test fold is touched once, at the end.
- YOLO training seeded (`seed=42, deterministic=True`) with identical hyperparameters for both variants, and `build_clean_yolo_seg.py:87-89` self-verifies that the two variants share identical images per split.
- The leakage mechanism is *archived*, not merely asserted — the original buggy split scripts are in the repo.

**Reproducibility gaps, in priority order:**

1. **`standalone_yolo_thresholds.json` does not exist** and its notebook cell has zero stored outputs. Two numbers in the main results table are uncheckable against anything the Data Availability statement promises. Fix before release (item 7). This is the one gap that genuinely contradicts the paper's stated contribution.
2. **Three p-values in a shipped analysis JSON contradict three p-values in the paper** (item 26).
3. **A stale doc in the release package tells readers the headline masking data is missing** when it is not (item 27).
4. **Unsorted glob ordering** determines the split, and the built-in check cannot detect a divergence (item 28). Ship the 205-filename manifest.
5. **Incomplete seeding** — `random.seed`, cuDNN determinism, DataLoader generator all missing, plus AMP. "Seed 42" over-promises (item 29).
6. **`ci` field in `benchmark1_11arch_4cond_seed42.json` is not Wilson.** Endpoints lie on the 1/205 grid and are asymmetric about `acc` — that is a percentile bootstrap. Relabel `ci_bootstrap`, or better, recompute as `ci_wilson` from the `preds`/`labels` arrays already stored in every row (which do allow full recomputation — a real mitigation).
7. **Train/serve preprocessing inconsistency across the artifact** (item 21): the deployed app and integrated pipeline crop; the training scripts and Benchmark-2 notebook do not. This is a real artifact defect even though it is *not* a measurement bug for Table 5. If you change the deployed transform, you must say the released code differs from the evaluated build.

**Release checklist before the repo goes public:**
- [ ] `standalone_yolo_thresholds.json` present, notebook cell 26 outputs retained
- [ ] `benchmark1_masking_pooled_analysis.json` recomputed, scipy version + tails recorded
- [ ] `BENCHMARK2_AND_HEADTOHEAD.md` stale passage removed
- [ ] `CLEAN_BENCHMARK_RESULTS.md` marked SUPERSEDED (it currently contradicts the paper)
- [ ] 205-filename test manifest shipped
- [ ] `ci` key relabelled or recomputed as Wilson
- [ ] The `:121` "56 of 199 sources … all were removed" claim reconciled with a released set containing 175 of 199 sources
- [ ] Orphan seed-2 records annotated or dropped
- [ ] Sorted globs, complete seeding

---

## 6. Figures

Currently: 3 figures, 6 tables. The figures are the least developed part of the paper.

### Fixes to existing figures

**Figure 1 (system architecture)** — fine. One improvement: annotate the two boxes with the *actual deployed* weights vs the *benchmarked* weights (Swin-Small vs Swin-Tiny), since the paper already discloses that difference in prose at `:94`. Making it visual pre-empts the question.

**Figure 2 (head-to-head)** — three problems.
- The caption's claim that "the differences fall within the cross-seed spread" is **false against the figure itself**: internal ±1 SD bars are [81.99, 83.21] vs [78.03, 79.69], a 2.3 pp gap with no overlap. Externally they overlap by 0.08 pp.
- Error bars are ddof = 0.
- No generating script exists in the tree — the only in-repo head-to-head plotting cell draws Wilson CIs, not seed SDs, so it is not the source of the submitted figure. **Reconstruct the script before claiming the figure was updated.**
- Best redesign: plot **both** uncertainties — a thick bar for the cross-seed spread (or min–max at n = 3, which is more honest and trivially reproducible) and a thin whisker for the Wilson interval, with a caption that names which is which. That single figure would visually make the paper's key statistical point: initialisation noise is tiny, sampling noise is ~10 pp.

**Figure 3 (confusion matrices)** — the matrices are correct; the caption is not (items 2 and 13). Fix "representative seed" → seed 42 with its position in the seed distribution stated, and fix the under-grading claim, which panel (b) refutes. Consider adding row-normalised percentages alongside counts.

### Missing figures — ranked by value

1. **The leakage figure (highest value, currently absent).** This is the paper's intellectual centre and it has *no figure*. Proposed: a two-panel schematic. Left, the mechanism — one source photograph → three augmented copies → a file-level split scattering them across train/test, versus a source-grouped split keeping them together. Right, the consequence, as a paired dot plot: the same masked classifier at **95.9%** on the 417 leaked test images vs **82.2%** on the 101 clean ones (13.7 pp, one model, one test set), and beside it the 21-architecture masked−unmasked deltas before (+3.06, 20/21 positive) and after (+0.55, 13/24) the fix. This is one figure that carries the entire paper. Build it.
2. **BIP_US error-direction figure.** A diverging bar chart of under- vs over-grading on the two external sets: BIP_US 55 vs 2, clean external 51 vs 45. It makes the safety finding immediate, and it makes the corrected version of item 2 into a positive result (domain-specific failure, not generic bias).
3. **Qualitative panel.** 6–9 example images with predicted mask overlay, true grade, predicted grade — including at least two BIP_US failures and one no-detection case. Cheap, and it is the figure clinical reviewers look for first. Also the natural place to *show* the duplicate-photograph pair with contradictory labels.
4. **Optional: per-class recall with intervals** on the external set, to make the 23-image third-degree fragility visible rather than buried in a note.

---

## 7. Writing — highest-value concrete edits

The prose is clear, well-organised, and unusually candid. The problems are precision, not style.

1. **Abstract — the "118 contaminated images" claim.** 226 were actually removed. Change to "removed every image from the 28 percent of source photographs that overlapped training". One phrase, removes a literal inaccuracy from the most-read sentence in the paper.
2. **Abstract — "won on both sets across all three seeds"** → "had the higher accuracy on both sets across all three seeds". Two words. (Abstract is ~297 words and likely over the limit; check the journal cap and trim elsewhere.)
3. **`:90` — the categorical verification claim.** Replace with the true, threshold-qualified version (item 6). This is the single most important sentence-level edit in the paper. Do not swap one over-confident absolute for another: name the screen, name the threshold, say the residual is threshold-dependent.
4. **`:155` and Fig-3 caption — the under-grading overclaim.** (Item 2.) Keep the claim where it is supported (BIP_US, overwhelming), remove it where it is not (clean external).
5. **`:119` — the statistics paragraph** is where four separate problems concentrate: promised-but-absent tests, the mislabelled MDE, the missing head-to-head power statement, and the undisclosed ddof. Rewrite the whole paragraph once, carefully, rather than patching.
6. **Add the within-model leakage evidence** to §Res:leak (item 17). The paper currently makes its central causal claim with the *weaker* of the two pieces of evidence it owns.
7. **Add the BIP_US classifier row** (item 18). Reporting that your headline winner loses on the clinical set is the most credible thing you can do in a paper about not over-trusting internal rankings.
8. **Tighten the "we never claim" register.** The manuscript hedges beautifully but occasionally hedges in the wrong place: it is very careful about the oracle number (good) and careless about "no source photograph appears in more than one fold" and "representative seed" (bad). A pass specifically hunting *categorical* words — "no", "all", "every", "verified", "representative" — would catch the remaining ones.
9. **The GenAI declaration is accurate and appropriately detailed.** Do not water it down. If anything, the listed prompt understates the scope slightly (the AI also drafted figure captions and tables); consider "…draft and edit the manuscript, including tables and figure captions". Accuracy here is worth more than a shorter declaration.
10. **Related Work sets a trap.** `:58` and `:70` indict prior work for not reporting confidence intervals. Until item 1 is fixed, a referee can quote your own sentence back at you in a single line. Fix the intervals *before* softening the indictment — the indictment is correct and worth keeping.

---

## 8. Contribution and acceptance odds

### What this paper is actually worth

Strip away the framing and there are three deliverables, in descending order of value:

1. **A quantified, mechanistically-explained leakage case study with the before/after both reported.** +3.06 pp across 20 of 21 architectures manufactured by a file-level split of an augmented dataset; +0.55 pp (ns) after source grouping; 95.9% vs 82.2% within one model split by memorisation. This is genuinely useful and I have not seen it done this cleanly in the burn literature. It is the paper's real contribution.
2. **A leak-free external evaluation showing a burn-severity model collapsing on clinical images in the dangerous direction.** 55 of 94 under-graded, half of full-thickness burns called first degree, balanced accuracy 30.5/35.0 against a 50% trivial baseline. Small N, but the direction is unambiguous and clinically meaningful.
3. **A negative result on segmentation-first pipelines.** Useful, honestly reported, and reinforced by the oracle-mask design. Weakest of the three because it is a null on 205 images with a ~9 pp detectable difference — but the paper says so.

**Who this helps:** anyone building a medical-image classifier from a Roboflow/Kaggle-style pre-augmented dataset — which is a very large population of MSc/BSc/early-PhD projects and a non-trivial share of published clinical-AI papers. The procedural lesson (partition by source, not by file) generalises far beyond burns. Secondarily, burn-AI reviewers now have a citable demonstration of why single-dataset accuracies in the 90s deserve suspicion.

**What it is not:** a methods contribution. There is no new architecture, loss, or algorithm, and the paper is admirably explicit about framing the contribution as the combination rather than novelty.

### Acceptance odds

**At TÜBİTAK TJEECS (current submission):**
- Accept without major revision: **~10%**
- Major revision then accept: **~45%**
- Minor revision then accept: **~15%**
- Reject: **~30%**

**Overall probability of acceptance somewhere reputable and fee-free within 12 months, given the fixes in §2 are made: ~85%.** This work will be published. The question is where and after how many rounds.

**What drives the odds:**
- *For:* the topic is a real clinical problem, the honesty is unusual and reviewers reward it, the leakage story is a genuine contribution, and TJEECS is a Q3–Q4 venue where the methodological bar this paper clears is above the typical submission.
- *Against:* no method novelty (some EE/CS reviewers reject purely on that); small N; a negative headline result; three student authors with no senior co-author, which affects perceived credibility even where it should not; and the six self-inflicted issues in §1, any of which a careful referee will find.
- *Wildcard:* if the referees include one statistician, items 1–4 of §2 will all be raised and the review will be harsh but fixable. If the referees are clinical or applied-CV, the small N and the lack of a fairness/skin-tone analysis will dominate instead.

**Advice on the supervisor question:** the supervisor is thanked, not a co-author. That is the authors' call and I will not second-guess the contribution question. But be aware it materially affects how referees read a paper making strong methodological claims. If the supervisor's contribution meets authorship criteria, including them is both correct and strategically helpful.

---

## 9. Alternative venues

**Constraint: no APCs, ever.** Two routes satisfy this — **diamond OA** (free to publish, free to read) and **hybrid/subscription journals via the non-OA route** (free to publish, paywalled to read). The second route is systematically overlooked and it opens far better journals than the first. Elsevier, Springer, Oxford and IEEE hybrid titles all publish subscription articles at **zero cost to the author**; the APC is only charged if you *choose* gold OA. You can then post the accepted manuscript to arXiv or an institutional repository, which achieves green OA for free.

**Statuses below were verified via web search in July 2026. Indexing and fee policies change — re-verify the specific title before submitting.** Where I could not verify something, I say so.

### 9.1 Tier A — best fit, free, and reputable

| Rank | Venue | Fee | Indexing | Fit | Notes |
|---|---|---|---|---|---|
| **A1** | **TMLR** — Transactions on Machine Learning Research | **None** (diamond, CC-BY) | DOAJ; reported Scopus-indexed (**verify**); DBLP, Google Scholar | **Excellent** | Acceptance criteria are literally *"are the claims supported by accurate, convincing and clear evidence"* and *"would some individuals be interested"* — with explicit policy that papers should be accepted **even if the contribution or significance is modest**, and explicit support for negative/null results. This paper is almost purpose-built for TMLR. Rolling submissions, fast turnaround, open review. Would need reframing from a clinical-journal register to an ML register, and the app/deployment material trimmed. |
| **A2** | **MELBA** — Journal of Machine Learning for Biomedical Imaging | **None** (diamond, CC-BY; ~$10 Scholastica submission fee) | DOAJ; Scopus status **unverified — check** | **Excellent** | Exactly the topical intersection: ML + biomedical imaging. Community-run, rigour-friendly, respected in the MICCAI/MIDL community. Single-blind review. Publishes methodological and evaluation papers that mainstream venues bounce for lack of novelty. |
| **A3** | ***Burns*** (Elsevier, ISBI journal) | **None via subscription route** (gold APC $3,190 is *optional*) | SCIE, Scopus, PubMed/MEDLINE, Q1 in burns | **Excellent clinical fit, moderate methods fit** | The flagship burn journal. The clinical-transfer failure and the under-grading finding are directly relevant to its readership. Would require heavy rewriting toward a clinical audience and away from architecture benchmarking. Highest prestige of any option here, and genuinely free if you decline gold OA. |
| **A4** | *Computer Methods and Programs in Biomedicine* (Elsevier) | **None via subscription route** (gold APC $3,180 optional) | SCIE, Scopus, PubMed, Q1 | **Very good** | Hybrid. Methodologically-oriented, welcomes evaluation and benchmarking work in medical computing. Avoid the *"…Update"* companion title — it is gold OA with a $1,500 APC. |
| **A5** | *Journal of Imaging Informatics in Medicine* (Springer, formerly *J. Digital Imaging*) | **None via subscription route** | SCIE, Scopus, PubMed | **Very good** | Hybrid. Publishes exactly this kind of applied-evaluation and data-quality work. Society-backed (SIIM). |

### 9.2 Tier B — free, decent, easier

| Rank | Venue | Fee | Indexing | Fit | Notes |
|---|---|---|---|---|---|
| B1 | **TÜBİTAK Turkish J. of Electrical Eng. & Computer Sciences** *(current)* | **None** (diamond) | SCIE, Scopus | Good | Already submitted. Bi-monthly, diamond, published by TÜBİTAK. Q3–Q4. |
| B2 | **TÜBİTAK Turkish Journal of Medical Sciences** | **None** (diamond) | SCIE, Scopus, PubMed | Good, if reframed clinically | Same publisher family — a natural lateral move if TJEECS rejects on "not enough EE/CS". |
| B3 | **Nordic Machine Intelligence** (Univ. of Oslo) | **None** (diamond) | Norwegian Level 1; Scopus **not confirmed — verify** | Good | Non-commercial, no APC, hosts the MedAI challenges. Friendly to medical-ML evaluation work. Lower visibility; check whether Scopus indexing matters for your degree/CV requirements. |
| B4 | **DMLR** — Journal of Data-centric Machine Learning Research | **None** (diamond) | DBLP, Google Scholar; Scopus unlikely — **verify** | Very good topically | Data-centric ML: dataset quality, leakage, benchmark construction. Your leakage story is squarely in scope. Young journal, so indexing is the risk. |
| B5 | **MIDL** (Medical Imaging with Deep Learning), PMLR proceedings | **No publication fee**; conference **registration** required | PMLR, DBLP, Google Scholar; not Scopus/SCIE | Very good | MIDL 2027 is in Porto. Free to publish, but registration + travel is a real cost. Strong community, and MIDL specifically values reproducibility work. Consider the short-paper track. |
| B6 | **ReScience C** | **None** (diamond) | Google Scholar; limited formal indexing | Good for the leakage component only | Reproducibility-focused. Would suit a companion paper narrowly about the leakage replication, not the whole study. |

### 9.3 Tier C — free but weaker, or with caveats

- **IEEE hybrid transactions via the subscription route** (e.g. *IEEE J. Biomedical and Health Informatics*, *IEEE Trans. Medical Imaging*): free to publish if you decline OA, excellent indexing, but the acceptance bar for a no-novelty evaluation paper is high. Realistic only after substantial strengthening (§10). **Avoid IEEE Access** — it is gold OA at ~$1,950.
- **arXiv (cs.CV / eess.IV)**: not a venue, but **do this immediately and unconditionally**. Free, timestamps the leakage finding, makes the work citable and discoverable, and is compatible with every venue above. TJEECS does not prohibit preprints; verify before posting if you want to be careful. Post the *pre-review* version now and update after acceptance.

### 9.4 Explicitly NOT recommended (all charge APCs you cannot avoid)

MDPI titles (*Diagnostics*, *Journal of Imaging*, *Sensors*, *Applied Sciences*, *Bioengineering* — CHF 1,800–2,900); Frontiers titles; PLOS ONE and PLOS Digital Health; *Scientific Reports*; *BMC Medical Imaging*; *PeerJ Computer Science*; *Burns & Trauma* (OUP, up to **$2,400**; LMIC waivers do not apply to Saudi Arabia); *Burns Open* (Elsevier gold OA); *Intelligence-Based Medicine*; *Machine Learning with Applications*; *Array*; *Heliyon*. All are legitimate — they are simply incompatible with a zero-fee constraint.

### 9.5 Predatory and problematic venues to avoid

You will receive solicitation emails within weeks of any submission or preprint. Rules:

- **Never respond to an unsolicited invitation to submit.** No reputable journal recruits by cold email with a promised 7-day review.
- **Red flags:** guaranteed or "rapid" acceptance; APC disclosed only after acceptance; an editorial board with no verifiable affiliations; "impact factor" from a fake metric provider (UIF, GIF, SJIF, Cosmos, ICV, "Index Copernicus Value"); a journal name near-identical to a famous one; a website with broken English or stock-photo editors.
- **Publisher families to avoid outright:** OMICS/Longdom, SCIRP, Bentham's low-tier open titles, Academic Journals (Nigeria), IJSER / IJARCCE / IJRASET / IJERT-style engineering mills, "World Scientific News"-type aggregators, and any journal listed on Beall's-descendant lists or absent from DOAJ.
- **Hijacked journals are the sharpest risk in this space.** Fake mirror sites impersonate legitimate Turkish and Iranian journals. **Always navigate to the journal from the publisher's own domain (`journals.tubitak.gov.tr`, `sciencedirect.com`, `academic.oup.com`, `link.springer.com`), never from a link in an email.**
- **Verification protocol before any submission:** the journal must be in **DOAJ** (if OA) **and** in Scopus or Web of Science Master Journal List, and the APC must be stated publicly *before* submission. If any of the three fails, do not submit.
- **Grey zone, not predatory:** MDPI and Frontiers special issues are legitimately indexed but carry reputational baggage in some committees, and are excluded here on cost anyway.

### 9.6 Concrete fallback plan

**Stay with TJEECS through the current round.** Do not withdraw. Prepare the §2 fixes so that a major-revision request can be answered comprehensively and quickly — a thorough, self-critical response letter that volunteers items 5, 6 and 10 before the referees find them is your single best lever on this decision.

- **If major/minor revision:** revise fully, volunteer the self-identified corrections explicitly, and this is very likely accepted.
- **If rejected → 1st choice: MELBA (A2).** Closest topical fit, no fees, and a community that specifically values the leakage/evaluation contribution. Reframe toward ML-for-imaging; keep the deployment story short.
- **→ 2nd choice: TMLR (A1).** Best acceptance-criteria match of any venue in existence for this paper. Rolling submission, so no waiting for a cycle. Requires the most rewriting (drop clinical framing, lead with the leakage methodology), which is why it is second despite the best fit on paper — do it first if you are willing to rewrite.
- **→ 3rd choice: *Burns* (A3), subscription route.** Highest prestige and the clinically most relevant audience, at zero cost. Requires the largest rewrite (clinical register, de-emphasise architecture benchmarking, lead with the under-grading safety finding). Also the slowest.
- **→ 4th: TÜBİTAK Turkish J. Medical Sciences (B2)** or **Computer Methods and Programs in Biomedicine (A4)**, depending on whether the rewrite went clinical or computational.
- **Throughout: arXiv preprint from today.** It costs nothing and protects priority on the leakage finding.

---

## 10. How to make this paper substantially stronger

Ranked by impact ÷ effort, and realistic for three undergraduates with Colab Pro. Items 1–4 are achievable inside a normal revision window.

| # | Work | Effort | Impact | Why it matters |
|---|---|---|---|---|
| **1** | **Rebuild the external set at one image per source (N = 175) and re-run all three seeds on it.** Three classifiers × three seeds is inference-only against saved checkpoints if the checkpoints exist; if only seed 42's predictions survive, re-run the three classifier seeds. | M–L (hours on Colab Pro if checkpoints exist; ~1 day if retraining) | **Very high** | Turns the paper's biggest vulnerability into its strongest demonstration. "We applied our own rule to our own external set and the conclusion held" is a far better sentence than any amount of disclosure. |
| **2** | **Add 2–3 more seeds (5 total) to the head-to-head.** | M (GPU-hours, not human-hours) | **High** | Three seeds is the bottom of what is publishable, and you already have direct evidence it under-covers (a fourth pipeline observation, seed 42 at 81.5%, sits 3.1 reported-SDs from the three-seed mean). Five seeds makes the entire "consistent across seeds" argument — which is the paper's substitute for significance — actually solid. Cheapest big win. |
| **3** | **Run the full pHash/dHash duplicate screen over the 1,370 primary sources, merge duplicate clusters, and rebuild the internal split as a robustness appendix.** Show the numbers are unchanged. | M–L | **High** | Closes the item-6 hole permanently, and does it in the strongest possible way: not "we disclosed a flaw" but "we re-ran it and the result holds". Also surfaces the label-contradiction finding as a real, citable observation about community-labelled burn datasets. |
| **4** | **Report the within-model leakage split (95.9% leaked vs 82.2% clean) as a primary result, and add the leakage figure (§6).** | S | **High** | You already have the data. It is the cleanest causal evidence in the entire project and it is currently unused. Highest impact-per-hour item on this list. |
| **5** | **Skin-tone / Fitzpatrick fairness probe.** Even a coarse ITA-based (individual typology angle) stratification of the test images into light/medium/dark and per-stratum accuracy with intervals. | M | **High** | Currently listed as a limitation with nothing behind it. For a burn-severity model — where pigmentation directly confounds erythema-based depth assessment — this is the single most-asked-for missing analysis, and reviewers in clinical AI now expect it. ITA can be computed from the images themselves; no new labels needed. Even a null with wide intervals is a contribution here. |
| **6** | **A second clinical external set, or a clinician re-read of BIP_US.** Ask one burn or plastic-surgery clinician (your institution has a medical school) to grade the 205 internal test images blind, and report human-vs-model agreement. | M–L (human, not compute) | **High** | Converts "the model gets 82.6%" into "the model gets 82.6% where a clinician gets X on the same images", which is the only comparison a clinical reader cares about. Also directly addresses the "60–80% inter-rater agreement" framing in your own Introduction, which currently goes unused. |
| **7** | **Calibration analysis.** Reliability diagram + ECE on internal and both external sets. | S–M | Medium-high | A model that under-grades dangerously *and* is over-confident is a much sharper safety finding than under-grading alone. You have the logits (or can get them in one inference pass). Cheap, and it is what a deployment-oriented referee will ask about. |
| **8** | **Report the mean over all 11 architectures alongside the best-of-11**, as the unbiased comparator. | S | Medium | Neutralises the winner's-curse objection (item 20) with data you already have. |
| **9** | **Proper efficiency measurement** (item 22), or on-device latency from the actual Flutter app. | S–M | Medium | The current table cannot distinguish a 4.5-GFLOP model from a 34-GFLOP one. On-device mobile latency would be genuinely novel content for this paper and directly supports the deployment framing. |
| **10** | **Test-time robustness sweep**: accuracy under JPEG compression, brightness/white-balance shift, and blur, on the internal set. | M | Medium | Cheap, entirely local, and it probes the *mechanism* of the clinical failure. If the model breaks under white-balance shift, that is a concrete, actionable explanation for the BIP_US collapse rather than the current hand-wave at "distribution shift". |
| **11** | **A small held-out "clinical-style" set** built by photographing burn images under clinical-like conditions, or by sourcing a third public clinical set. | L–XL | Medium | Only worth doing if items 1–7 are done. Two external sets is already better than most of the literature. |

**What I would explicitly NOT spend time on:** new architectures, hyperparameter search, a bigger backbone, or improving the segmenter. The paper's own oracle-mask argument proves a better segmenter cannot help, and adding architectures to a null result adds nothing. Every hour is better spent on evaluation rigour, which is what this paper is actually about.

---

## 11. What I would do next, in order

1. **Today — post to arXiv.** Free, protects priority on the leakage finding, makes the work citable while you wait. Verify TJEECS's preprint policy first (it is permissive, but check).
2. **This week — fix the repo, not the paper** (§2 items 7, 26, 27, 28, 29, 30, 31; ~4–6 hours). Re-run notebook cell 26 and commit `standalone_yolo_thresholds.json`; recompute the contradicting p-values; delete the stale "not yet exported" passage; mark `CLEAN_BENCHMARK_RESULTS.md` superseded; ship the 205-filename manifest; sort the globs. None of this touches the manuscript, all of it must be true before the repo goes public.
3. **This week — write the correction list.** Draft the exact replacement text for §2 items 1–6 and 8–10 now, while it is fresh. When the decision arrives you will have a revision ready in days instead of weeks.
4. **Next two weeks — do the cheap high-impact science:** the within-model leakage number promoted to a primary result (item 4 of §10, ~1 hour), and two more seeds queued on Colab Pro (item 2 of §10, GPU-time not human-time).
5. **Next month — the two structural fixes**: rebuild the external set at N = 175 (§10 item 1) and run the full duplicate screen with a rebuilt-split robustness appendix (§10 item 3). Both convert admissions into demonstrations.
6. **In parallel — the ITA skin-tone probe** (§10 item 5). It is the most-asked-for missing analysis, it needs no new data, and a null with wide intervals is still a contribution.
7. **When the decision arrives:**
   - *Revision* → answer everything, volunteer the self-identified corrections explicitly and early in the letter, and attach the strengthened analyses. Referees reward authors who find their own errors; you have already proven you will.
   - *Reject* → MELBA first, TMLR second (or TMLR first if you are willing to rewrite in an ML register), *Burns* third. Do not lower your standards to a paid venue, and do not answer a single solicitation email.
8. **Whatever happens — do not soften the honesty.** The leakage story, the failed replication, the clinical collapse, and the refusal to headline the oracle number are why this paper deserves to exist. The corrections in this audit exist to make the paper live up to that, not to trim it.

---

*Prepared 2026-07-25. Every quantitative claim in this document was recomputed from the raw files cited; where a claim could not be verified from a file, it is marked unverified.*
