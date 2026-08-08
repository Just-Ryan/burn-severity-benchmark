# Segmentation-Guided Burn Severity Classification
## A complete technical account of the project, from idea to submitted manuscript

**Authors:** Ryan Altayeb, Abdulrahman Alraddadi, Mohannad Alrehaili
**Origin:** Undergraduate graduation project, Faculty of Computer and Information Systems, Islamic University of Madinah
**Status at time of writing:** manuscript prepared for the *Journal of Machine Learning for Biomedical Imaging* (MELBA)
**Repository:** https://github.com/Just-Ryan/burn-severity-benchmark (public, MIT / CC BY 4.0)
**Verification:** `verify_paper_numbers.py` — 205 published quantities recomputed from raw data, all passing

---

# 0. How to read this document

This is the full record of a project that began as an undergraduate capstone and ended as a methodological study. It is written for a reader who wants to judge the work rather than be sold it: every claim below is accompanied by the number that supports it, and where a number changed during the project the document says what it was, what it became, and why.

The account is deliberately structured around a single narrative arc, because that arc *is* the scientific content. We set out to show that a two-stage segmentation-guided pipeline beats a plain image classifier at grading burn severity. The first answer we obtained was that it did, by a comfortable margin. That answer was wrong. Establishing why it was wrong, and what the true answer is, consumed the majority of the project's effort and produced its most transferable findings.

The short version of the conclusion, stated up front so nothing below reads as a reveal:

> Segmentation-guided classification reaches **internal parity at best** with a plain classifier, never advantage. Its apparent early superiority was an artifact of data leakage. Its apparent later inferiority was substantially an artifact of testing it in a configuration it was never trained for. Corrected on both counts, the internal difference is no longer resolvable — but the **external** claim does not survive: the configuration that made the two look equal externally was itself selected on the test sets, and against the configuration validation would have chosen the plain classifier is still ahead externally (+2.57 pp, *p* = 0.008). The pipeline runs two models to reach internal parity.

Sections 1–6 cover the idea, the system, and the data. Sections 7–14 cover every experiment in the order it was run. Section 15 covers the methodological findings, which are the part of this work most likely to matter to people outside burn imaging. Sections 16–19 cover reproducibility, the publication process, and an honest post-mortem.

---

# 1. Origin and motivation

## 1.1 The clinical problem

Burns are common and consequential. Roughly 11 million people require medical attention for burns each year, and the World Health Organization estimates about 180,000 annual deaths, concentrated in low- and middle-income countries where specialist burn care is scarce. Survivors frequently face long hospital stays, scarring and permanent disability.

Treatment decisions turn first on **burn depth**, which separates injuries that will heal with conservative management from those requiring surgical intervention. The conventional grading is:

| Grade | Depth | Clinical implication |
|---|---|---|
| First degree | Epidermis only | Heals spontaneously, days |
| Second degree | Partial thickness, into dermis | May heal or may need grafting |
| Third degree | Full thickness | Requires surgical management |

The difficulty is that depth assessment is genuinely hard even for experts. Jaskille et al. report that experienced burn surgeons assess depth **accurately only 64 to 76 percent of the time**. Assessment is affected by lighting, the evolution of the wound over hours, blistering, and skin pigmentation. Instrumented alternatives such as infrared thermography reach higher accuracy but require equipment that is expensive and rarely available at the point of care.

That gap — a decision that matters, made unreliably, with no cheap instrument to help — is what motivates automated assessment from ordinary photographs.

## 1.2 Why we thought segmentation would help

This is the intellectual core of the project and deserves stating carefully, because the whole study is a test of it.

A photograph of a burn contains the wound and a great deal else: unburned skin, dressings, bedding, clothing, a clinician's gloved hand, furniture, the room. A convolutional network or vision transformer trained on whole images is free to use any of that signal. Nothing in the training objective tells it to look at the injury.

In a **web-sourced** dataset this freedom is actively dangerous. Background correlates with severity for reasons that have nothing to do with tissue pathology:

- Severe burns are photographed in hospitals — surgical drapes, monitors, gloves in frame.
- Minor burns are photographed at home — kitchen counters, domestic lighting.
- Image provenance itself correlates: clinical case reports use different cameras and framing than consumer photographs.

A model that learns "surgical drape ⇒ third degree" will score well on a held-out split of the same collection and fail immediately in any setting where that correlation does not hold. This is precisely the failure mode documented by Zech et al. in chest radiography, where a pneumonia network scoring 0.931 AUC internally fell to 0.815 at an external hospital and was shown to be exploiting site-specific artifacts.

The remedy is direct: **remove everything that is not the wound**. Segment the burn region, multiply the binary mask into the image so that all non-burn pixels are zero, and pass only the isolated lesion to the classifier. The classifier then has access only to the properties clinicians actually use — the colour, texture, blanching and moisture of injured tissue — because nothing else survives.

This design is not novel in medical imaging generally. Dual-stage frameworks that localise a region of interest before classifying it are established in breast ultrasound and dermoscopy. What was missing was any evaluation of the design **for burns, against the simpler alternative it is meant to improve on**. The published burn literature either classifies whole images or segments them; where the two are combined, the combination is not tested against a plain classifier under one protocol. Whether isolating the burn actually helps a burn-severity classifier was, when we began, an open question with an assumed answer.

We built the system to find out.

---

# 2. The system

## 2.1 Architecture

The deployed pipeline has two stages:

```
photograph
    ↓
[Stage 1]  YOLOv8x-seg, single class ("burn")
    ↓      predicts a segmentation mask
binary mask × image  →  background set to zero
    ↓
[Stage 2]  Swin transformer classifier
    ↓
first / second / third degree
```

**Stage 1 — localiser.** YOLOv8x-seg, the largest segmentation variant in the YOLOv8 family (~71M parameters), trained as a *single-class* detector. It answers "where is the burn?" and deliberately not "what grade is it?", on the reasoning that separating localisation from grading lets each stage specialise. Training: 100 epochs, 640×640 input, batch size 8, AdamW at an initial learning rate of 10⁻³, seed 42, early stopping with patience 20, initialised from public `yolov8x-seg.pt` weights.

**Stage 2 — classifier.** A Swin transformer (Swin-Tiny in the benchmarked configuration), ImageNet-pretrained via the `timm` library, classification head resized to three outputs. Training: AdamW, class-weighted cross-entropy using inverse class frequencies, cosine schedule with early stopping, mixed precision, input resized to 224×224. Training-time augmentation was horizontal flip, colour jitter and small rotation; evaluation-time augmentation was disabled. The identical transform was used for every architecture so that differences reflect the network rather than the setup.

**Inference behaviour.** The deployed system runs the localiser at a low confidence threshold of 0.05 and falls back to classifying the full frame when no region is returned. We call this the **robust pipeline**. We also report a **strict pipeline** (confidence 0.25, no-detection counted as an error) as a sensitivity check, because the difference between the two is entirely a matter of how you handle detection failures and it turns out to matter a great deal on external data.

## 2.2 Deployment

The system was fielded as a mobile application:

- **Backend:** Flask server hosting both models, exposing an inference endpoint.
- **Frontend:** Flutter mobile application — capture or upload a photograph, receive a grade and the localised region.
- **Secondary artifact:** a separate iOS SwiftUI application with on-device LibTorch inference.

An important disclosure that appears throughout the manuscript: **the shipped demonstration application runs a Swin-Small classifier, whereas every pipeline number in the paper uses the benchmarked Swin-Tiny weights.** The application is a research and demonstration artifact, not a clinically validated device, and the external results reported below show it is not ready for any clinical role.

## 2.3 Efficiency

Measured on an NVIDIA A100, 640×640 input, batch size 1:

| Component | ms/image | images/s |
|---|---|---|
| YOLO localiser (1-class) | 15.4 | 65 |
| Standalone YOLOv8-seg (3-class) | 15.1 | 66 |
| Swin-Tiny classifier | 23.7 | 42 |
| ConvNeXt-Large classifier | 25.8 | 39 |
| **Full pipeline** (localiser → mask → Swin) | **42.3** | **24** |

The pipeline costs about **1.6×** the latency of a standalone classifier because it runs two models. This figure is a datacentre measurement and is explicitly *not* a mobile latency budget; on-device inference time was never measured, which the manuscript states.

---

# 3. Data

## 3.1 Primary dataset

The **"skin burn wound classification"** collection on Roboflow Universe (version 31), released under CC BY 4.0, exported in COCO segmentation format.

| Property | Value |
|---|---|
| Unique source photographs | **1,370** |
| Augmented annotated files | ≈ 3,424 (about 2.5 copies per source) |
| Classes | first / second / third degree |
| Approximate class shares | 42% / 31% / 27% |
| Label provenance | Community-provided, **not** clinically verified |

The augmentation factor is the single most consequential property of this dataset and it caused the project's central error. The collection ships each photograph as roughly 2.5 augmented copies **with distinct file names**. A naive file-level split therefore scatters copies of one photograph across training and test folds. More on this in Section 7.

From the split we derive:

- a **segmentation** dataset (polygon annotations, either single-class "burn" or three severity classes), and
- a **classification** dataset in four input forms: *unmasked* full images; *masked*, where the ground-truth polygon is rasterised to a binary mask and multiplied into the image; *cropped* to the annotation bounding box; and *masked and cropped*.

A critical caveat, stated in the manuscript wherever the masked condition appears: **the masked form uses ground-truth annotations, not predicted masks**. Any benchmark result on it is therefore an *oracle upper bound* — the most a perfect segmenter could contribute.

## 3.2 The leak-free split

After discovering the leakage (Section 7), we rebuilt the split from scratch:

- Partition the **1,370 source photographs** 70/15/15, stratified by class, seeded at 42.
- Keep all augmented copies **only** in the training fold.
- Deduplicate validation and test to **one image per source**.

| Fold | Images | Sources |
|---|---|---|
| Train | 2,425 | 1,829 |
| Validation | 206 | 206 |
| Test | 205 | 205 |

Internal test class distribution: **86 first / 63 second / 56 third degree**.

**We then audited our own correction.** Applying the same perceptual-hash procedure used for external decontamination, we found that **2 of the 205 test images (1.0 percent) are perceptually identical to a training image carrying a different source identifier** — the same photograph contributed to the collection twice under different names. One of the two pairs additionally carries *conflicting labels* between the folds.

We report this rather than suppress it. The effect is bounded — each reported accuracy moves by at most 1.0 percentage point — but the more important point is what it demonstrates: **grouping by identifier is a heuristic, not a proof of independence**. Identifiers describe provenance only as well as the upstream collection was curated. Any source-grouped split should be verified with a content-based check.

## 3.3 External validation sets

Two independent sets, chosen to probe different kinds of distribution shift.

**BIP_US (clinical).** The Biomedical Image Processing Group database, University of Seville — **94 photographs**, predating and independent of the web-sourced training data. Depth is labelled as *superficial dermal* (42), *deep dermal* (32) or *full thickness* (20). The mapping onto our three classes is not exact, so we report both plausible mappings of deep dermal (to second degree and to third), giving a second-versus-third-degree probe with **no first-degree cases**. No BIP_US image is redistributed in our repository.

**Clean web-sourced external set.** Built from a second public Roboflow burn collection by removing everything overlapping our training data. The screening used perceptual hashing — pHash and dHash computed with the `imagehash` library, compared by Hamming distance against all primary training images, made horizontal-flip-aware. An image was treated as a duplicate when either hash matched a training image **exactly (Hamming distance 0)** in any flip orientation; after removal we verified no retained image lay within a Hamming distance of 10 of any training hash.

| Stage | Count |
|---|---|
| Original collection | 1,371 images from 199 sources |
| Removed as perceptual-hash identical to training | **118** |
| Sources contributing a removed image | 56 of 199 (28%) |
| Sources eliminated entirely | 24 |
| Retained after also dropping fourth-degree and remapping | **319 images from 175 sources** |
| Class distribution | 139 / 157 / 23 |

Note the arithmetic explicitly, because a careful reader will check it: 199 − 56 ≠ 175. Removal was at the **image** level, not the source level, so a source contributing one contaminated image could retain its other copies. It is the verified Hamming-distance-10 margin, not source-level exclusion, that rules out residual contamination among retained images.

Because 319 images derive from only 175 sources, an interval computed on N = 319 is too narrow. We therefore report **source-clustered bootstrap intervals** (20,000 resamples over the 175 source photographs) alongside Wilson intervals. Clustering widens the external accuracy intervals by roughly a fifth — from 9.6 to 11.7 percentage points for the classifier and 10.0 to 11.9 for the pipeline.

---

# 4. Literature review

The review positions the work along four axes.

## 4.1 Automated burn assessment, and the high single-dataset pattern

Computer-aided burn assessment predates deep learning: early systems on the Seville BIP_US database combined hand-crafted colour and texture features with classical classifiers. Deep learning has since become dominant, typically applied to the two coupled subproblems of delineating the burn and grading its severity.

Recent work spans convolutional classifiers, attention-augmented residual networks, YOLO-family detectors adapted to burn severity, and transformer frameworks performing segmentation and severity assessment jointly. Several report high single-dataset accuracy — 95.6 percent with a transfer-learning classifier is representative, and a recent five-year systematic review collates studies reporting **80 to 98 percent**.

That review is also the strongest evidence for our framing. It judges **six of fourteen studies to carry a high risk of bias**, faults the reliance on public datasets that do not represent the target population, and reports dataset details as frequently unstated.

One qualitative point deserves care, because we initially got it wrong. An earlier draft claimed that partial-thickness (second-degree) burns are "the hardest class" and cited two works in support. Checking those sources revealed that **one reports the opposite** — second degree is among its best-performing classes, with its weakest classes attributed to under-representation. The manuscript now states the disagreement rather than manufacturing a consensus: second degree is consistently hardest in *our* results, and the literature does not settle the question.

## 4.2 Comparative studies on a single split

Comparative burn studies exist, but they evaluate several backbones on a single split and rarely report confidence intervals, significance tests, or external evaluation. Without these, apparent improvements may not be reliable and out-of-distribution behaviour is unknown. This is the gap our benchmark targets directly.

## 4.3 Segment-then-classify, and whether masking helps

Cascading segmentation into a downstream classifier is well established: dual-stage frameworks localise then classify in breast ultrasound and dermoscopy, and the cascade appears in burns for wound measurement and surface-area estimation. This grounds our design as a standard template rather than a novelty.

The evidence that masking *helps*, however, is mixed. Sourget et al. show that models trained on full images can match or exceed models restricted to the region of interest, precisely because networks exploit background and spurious cues — so masking is not universally beneficial preprocessing. Our central result is consistent with that finding.

## 4.4 Data leakage and external validation

Leakage — information about the test set contaminating training — is a long-recognised cause of inflated, irreproducible results, and has been identified as a systemic driver of the reproducibility crisis across machine-learning-based science. In medical imaging, a systematic review that screened 2,212 COVID-19 studies and adjudicated 62 found **none of clinical use**, with leakage, biased curation and inadequate reporting among the leading causes.

Quantified leakage case studies exist and report inflations **larger than ours**:

| Study | Domain | Reported inflation |
|---|---|---|
| Yagis et al. 2021 | Brain MRI | 29–55% across four cohorts (slice- vs subject-level splitting) |
| Tampu et al. 2022 | Retinal and breast OCT | 5–30% accuracy |
| Rosenblatt et al. 2024 | Connectome prediction | Varies by mechanism; some forms *decrease* performance |

In all of these, leakage inflates the absolute score of a single model. **Our case differs structurally**, and this is the narrow novelty claim the paper makes: the leak rate was *confounded with the condition under comparison* — 80.5 percent in one arm, zero in the other — so leakage did not inflate a number, it manufactured a *comparative conclusion* and a design recommendation.

The nearest precedent is confound-leakage (Hamdan et al. 2023), where a corrective preprocessing step introduces leakage into one arm of a comparison. We scope our claim explicitly against it rather than claiming priority. We are careful about the mechanism too: masking itself creates no leakage. What differed between our arms was the *split protocol* — one arm re-partitioned at file level, the other left on the collection's own partition.

## 4.5 How many training runs a conclusion needs

That benchmark results depend on more than the reported point estimate is established. Bouthillier et al. show that comparing two methods from single runs produces high rates of both false positives and false negatives, and — importantly, in the direction our own results reproduce — that variance from perturbing the **data split** exceeds variance from weight initialisation alone. Picard shows that even where the overall spread across seeds is modest, individual outlier seeds are easy to find. In medical imaging specifically, evaluation noise has been shown to exceed the gap between the winning model and the best 10 percent of entries in five of eight challenges examined, and biomedical image analysis rankings are unstable to methodological choices.

What we add is not the observation that seeds matter, which belongs to this literature, but a **measured instance in which the conventional three-run protocol changed which of two conclusions the evidence supported, in both directions at once**.

---

# 5. Benchmark design

Two benchmarks answer two distinct questions.

**Benchmark 1 — does masking help the classifier?** Eleven ImageNet-pretrained architectures (ConvNeXt-Tiny, ConvNeXt-Large, DenseNet201, EfficientNet-B0, MobileNetV3-Large, ResNet50, Swin-Tiny, Swin-Small, Swin-Base, Swin-Large, ViT-Base) trained on the leak-free split. Coverage is stated explicitly and is **not uniform**: all 11 architectures under unmasked and masked conditions; only 8 of 11 under the two cropping conditions (ConvNeXt-Tiny, Swin-Base and Swin-Large omitted for compute). Because the masked condition uses ground-truth masks, its result is an **oracle upper bound**.

**Benchmark 2 — does the pipeline help end to end?** A head-to-head on the shared 205-image internal test set and the external sets, comparing the standalone classifier, the all-in-one YOLOv8-seg model, and the two-stage pipeline.

We state one asymmetry rather than claiming fairness: the standalone classifier is evaluated in its best Benchmark 1 condition, whereas the pipeline arm is fixed to the *deployed* configuration. This favours the classifier, and Section 15.7 reports how much.

**Statistical protocol.** Two distinct questions require two distinct tests and we keep them separate throughout:

- Whether one system beats another **on a particular test set** is an image-level question, answered by paired exact McNemar on per-image predictions.
- Whether one system beats another **on average across training runs** is a run-level question, answered by a paired test over per-seed accuracies.

Overlapping error bars are never used as evidence of absence, because the comparisons are paired.

---

# 6. The first answer — and why it was wrong

The original experiment trained **21 architectures** under masked and unmasked conditions on a naive file-level split. The result looked decisive:

> Masking improved accuracy for **20 of 21 architectures**, by a mean of **+3.06 percentage points**.

Twenty-one architectures agreeing is exactly the kind of consistency that reads as robustness. It was the opposite.

---

# 7. The leakage discovery

## 7.1 What we found

Auditing the split revealed that the two arms of the comparison had not been constructed the same way:

| Arm | Split | Test fold | Leak rate |
|---|---|---|---|
| Masked (CNN-DatasetM) | Re-split 70/15/15 after flattening | 518 images | **417 / 518 = 80.5%** |
| Unmasked (CNN-DatasetNM) | Retained the collection's own 90/6/4 | 143 images | **0 / 143 = 0%** |

Because the source collection augments each photograph into ~2.5 near-duplicate copies with distinct file names, re-splitting at the file level scattered copies of one photograph across training and test. The masked arm was re-split and leaked catastrophically; the unmasked arm was never re-split and leaked nothing.

The two arms differed in **split ratio, test-set size and leak rate simultaneously**. The "+3.06 pp masking benefit" was not a property of masking. It was a property of one arm being scored partly on images it had memorised.

## 7.2 Why cross-architecture consistency was misleading

This is the finding we consider most transferable. The 20-of-21 consistency felt like strong evidence. It was in fact evidence *for the confound*: every architecture was subject to the same asymmetric leak, so every architecture benefited. **When a leak rate differs between the arms being compared, consistency across architectures is evidence for the confound rather than against it.**

## 7.3 The matched contrast

A subtlety we later caught in our own reporting: the "before" figure (3.06 pp) came from 21 architectures while the "after" figure came from 8. Restricting the naive-split analysis to the **same eight architectures** that enter the corrected estimate:

| Architecture pool | Naive file-level split | Leak-free, pooled |
|---|---|---|
| All 21 originally trained | +3.06 pp, 20/21 positive | — |
| Same 11 as Benchmark 1 | +2.89 pp, 10/11 | — |
| **Same 8 as the pooled analysis** | **+2.07 pp, 7/8** | **+0.55 pp, 13/24 pairs** |

The matched contrast is **2.07 → 0.55**, not 3.06 → 0.55. The paper reports the smaller, matched figure as the one it relies on, and gives the 21-architecture number only because it is what the original experiment produced.

---

# 8. Benchmark 1 — does masking help?

On the leak-free split, with ground-truth (oracle) masks:

**Seed 42 alone.** Masking raised accuracy by **+1.5 percentage points** overall, concentrated in transformers (+3.1, in five of five) with roughly no change for convolutional networks (+0.2).

**Pooled over seeds 0, 1 and 42** (24 architecture-seed pairs across 8 architectures):

> **+0.55 percentage points, 95% CI −0.37 to +1.47** (Wilcoxon signed-rank *p* = 0.32; 13 of 24 pairs improved)

The interval is the informative quantity. It is consistent with no effect, and it **rules out any benefit larger than about 1.5 percentage points**. The apparent transformer advantage did not replicate (one-sided Mann-Whitney *p* = 0.33; two-sided *p* = 0.66), with transformers at +0.77 and convolutional networks at +0.33 pooled.

Cropping to the burn produced essentially no change at seed 42, as did masking with cropping; both were run on 8 of 11 architectures and not repeated across seeds, so they are treated as a weaker single-seed check.

**The strongest form of this result:** because the ablation used *ground-truth* masks, poor segmentation cannot be blamed for the null. A better segmenter could not rescue a masking gain that is absent even with perfect masks. This is an upper bound, and it is small.

**Best-of-condition, seed 42.** Worth recording because it is the most favourable honest view of masking:

| Condition | Best architecture | Accuracy |
|---|---|---|
| Masked | Swin-Tiny | **85.37** |
| Unmasked | ConvNeXt-Large | 84.88 |

With perfect masks, the best masked configuration does edge the best unmasked one. The effect simply does not survive pooling across architectures and seeds.

---

# 9. Segmentation quality

On the held-out test set:

| Model | Classes | Test mask mAP50 | mAP50-95 |
|---|---|---|---|
| Single-class localiser (pipeline front-end) | 1 | **0.726** | 0.417 |
| Standalone YOLOv8-seg | 3 | **0.603** | 0.349 |

The single-class model scores higher because it need not separate severity classes. Second degree is the hardest class to segment, consistent with the classifiers' weakest per-class performance on partial-thickness burns.

Segmentation is therefore **moderate, not excellent** — a fact that matters for interpreting the pipeline.

After the segmentation-split correction (Section 15.5), the retrained models reach mask mAP50 of **0.695** (1-class) and **0.566** (3-class) on the leak-free test fold.

---

# 10. Benchmark 2 — the head-to-head

## 10.1 As originally run (three seeds)

| System | Internal (N=205) | External (N=319) |
|---|---|---|
| Standalone classifier (ConvNeXt-Large) | 82.6 ± 0.7 | 76.6 ± 1.6 (bal. 80.1) |
| Robust pipeline (localiser → Swin-Tiny) | 78.9 ± 1.0 | 73.4 ± 2.5 (bal. 77.9) |
| Standalone YOLOv8-seg (single seed) | 78.0 (bal. 77.7) | 66.8 (bal. 67.0) |
| *Oracle Swin-Tiny (ground-truth masks)* | *83.9* | *n/a* |
| *Strict pipeline (conf 0.25, no-detection = error)* | *79.0* | *54.2* |
| *Robust pipeline, seed 42* | *81.5* | *69.9* |

Two observations that shaped everything after:

**The oracle/real gap.** Swin-Tiny on ground-truth masks reached 83.9 percent; the robust pipeline with real predicted masks reached 81.5 at the same seed. At matched seeds, imperfect segmentation appeared to cost about two points.

**The threshold matters enormously at the tail.** Strict versus robust moves external accuracy from 54.2 to 69.9 percent — a 15.7-point swing driven by how detection failures are handled, not by model quality.

## 10.2 Threshold provenance

Because "you chose 0.05 on the test set" is the obvious attack on a paper about protocol hygiene, we checked it. Sweeping the localiser confidence on the **206-image validation fold**:

| conf | val acc | test acc |
|---|---|---|
| 0.001 | 79.61 | **79.51** ← test optimum |
| **0.005** | **82.04** ← val optimum | 77.07 |
| 0.05 | 81.07 | 78.05 ← reported |
| 0.25 | 80.10 | 75.12 |
| 0.50 | 72.82 | 69.76 |

The reported operating point of 0.05 is **neither the validation optimum nor the test optimum**. It was inherited from the deployed system, not tuned. The whole sweep spans about two percentage points until the threshold rises past 0.25 and detections start being lost.

---

# 11. The seed investigation

## 11.1 Three seeds against ten

The original protocol used three seeds, which is entirely conventional. We repeated the full head-to-head over **ten** seeds, training both arms under a fixed recipe.

| | Classifier | Pipeline | Paired difference | *p* |
|---|---|---|---|---|
| **Internal, three seeds** | 82.6 ± 0.7 | 78.9 ± 1.0 | +3.74 [+3.04, +4.44] | 0.002 |
| **Internal, ten seeds** | 83.61 ± 1.74 | 80.98 ± 2.22 | +2.63 [+0.29, +4.98] | 0.032 |
| **External, three seeds** | 76.6 ± 1.6 | 73.4 ± 2.5 | +3.24 [−3.83, +10.31] | 0.19 |
| **External, ten seeds** | 77.81 ± 2.29 | 75.02 ± 1.32 | **+2.79 [+1.09, +4.49]** | **0.005** |

The contrast is the point, and it runs in **both directions at once**:

- Three seeds put the internal difference at +3.74 with an interval **three times narrower** than ten seeds support (1.40 vs 4.69 pp wide), around an effect whose true magnitude is smaller.
- The same three seeds put the external difference at +3.24 with an interval spanning zero, licensing no claim at all — when that effect is in fact **the most reliable in the study**.

A three-seed protocol thus **overstated the weaker result and concealed the stronger one simultaneously**.

## 11.2 Seed variance measured directly

Over ten seeds on the internal test set:

| System | Mean | Sample SD | Range | SD from any 3 of these 10 |
|---|---|---|---|---|
| Standalone classifier | 83.61 | **1.74** | 5.85 | **0.00 to 3.25** |
| Two-stage pipeline | 80.98 | **2.22** | 6.83 | 0.28 to 3.69 |

The three-seed protocol had reported 0.75 and 1.02 — roughly **half** the ten-seed values.

Across all $\binom{10}{3} = 120$ three-seed subsets, the estimated standard deviation for the classifier ranges from **0.00 to 3.25** percentage points. A three-seed standard deviation is therefore not a noisy estimate of the right quantity; it is very nearly uninformative, and **it can be arbitrarily small purely by chance**.

## 11.3 Removing the recipe confound

The three-versus-ten comparison also involved a training-recipe change, so it confounded seed count with recipe. We removed that by enumerating all 120 three-seed subsets **of the same ten runs**:

| Quantity (external; ten seeds give +2.79, *p* = 0.005) | Across 120 subsets |
|---|---|
| Point estimate | +0.21 to +5.22 pp |
| *p*-value | 0.0005 to 0.86 |
| CI half-width | 0.45 to 10.63 pp (>20-fold spread) |
| Subsets reaching *p* < 0.05 | **15 of 120** |

Internally the spread is wider: estimates run from **−0.98 to +6.67**, so some three-seed subsets place the *pipeline* ahead, and only 6 of 120 reach *p* < 0.05. Because every subset comes from the same ten runs under one recipe, this analysis carries no confound and isolates seed count as the cause.

## 11.4 Pooling honesty

Seeds 0–6 used batch 16 at lr 10⁻⁴; seeds 7–9 used batch 32 at 2×10⁻⁴. The paired differences from the two groups are similar (internal +2.44 vs +3.09; external +2.87 vs +2.61; Welch *p* = 0.84 and 0.92) and we pool on that basis — but we state it as an **assumption rather than as something a test established**, because with seven runs against three the Welch test has almost no power, and by the standard this paper applies elsewhere a non-significant result is not evidence of equivalence. Every per-seed value is printed so a reader can inspect the groups directly.

---

# 12. External validation

## 12.1 The clean web-sourced set

On 319 pHash-cleaned images, the classifier was the most robust approach with no undetected images, while segmentation-dependent approaches degraded more.

**Under-grading, quantified conditionally.** Raw error counts are confounded by class balance — a first-degree burn cannot be under-graded and a third-degree burn cannot be over-graded — so we condition on eligibility:

| | Under-graded | Over-graded |
|---|---|---|
| Internal | 19.3% (23/119) | 10.1% (15/149) |
| External | **28.3% (51/180)** | 15.2% (45/296) |

The bias toward lower severity is present on both sets and numerically higher externally. An earlier draft described the external rate as "markedly stronger"; **testing it rather than asserting it gives *z* = 1.77, *p* = 0.08** — and that figure ignores source clustering, so it is optimistic. The corrected statement is that under-grading is substantial on both sets, numerically higher externally, and **not established as different between them** at this sample size.

Under-grading is the clinically dangerous direction: it routes a severe burn toward conservative care.

## 12.2 BIP_US — and a correction to our own interpretation

On the 94 clinical images, the pipeline graded about 55 of 94 below their true severity and classified about half of the full-thickness burns as first degree. Balanced accuracy was **30.5 percent** (deep-dermal→second) and **35.0 percent** (deep-dermal→third), against a chance level of 50 percent for a two-class probe.

Below-chance performance invites a mechanical explanation, and we tested one rather than leaving it to a reader. **The BIP_US reference contains no first-degree category, yet the pipeline assigns first degree to 48 of the 94 images — 51 percent — a class that cannot be correct under either mapping.** That alone drives balanced accuracy beneath chance.

| Treatment | Deep dermal → Second | Deep dermal → Third |
|---|---|---|
| As reported | 30.5% | 35.0% |
| Excluding impossible-class calls (n=46) | **62.2%** | **55.4%** |
| Collapsing first → second | 56.1% | 50.5% |

The correct reading is therefore **not** that the model cannot rank burn depth, but that it applies a severity scale **systematically offset** from clinical depth staging — and offset in the dangerous direction. Assigning the mildest available grade to half of a set containing no mild burns is under-grading in its most extreme form. The transfer failure is real; what the below-chance figure measures is the offset, not an inability to discriminate.

---

# 13. The fairness probe

Because any imaging aid intended for clinical use should be checked for systematic dependence on skin tone, we added an exploratory probe.

**Method.** No ground-truth phototype labels exist, so we estimated *apparent* skin tone from the images using the **Individual Typology Angle**, ITA = arctan((L\* − 50)/b\*) × 180/π, computed in CIE L\*a\*b\* under D65 and binned into the six conventional bands of Chardon et al. ITA must be measured on **unburned** skin, so the burn region was excluded from every image — from ground-truth masks internally, from rasterised polygons externally — and both exclusions dilated by 6 pixels. Skin pixels were selected by the conjunction of the standard RGB and YCbCr skin rules; images yielding fewer than 500 skin pixels were recorded as indeterminate (11 of 205 internal, 0 external).

**Headline result: a null.** Accuracy does not order monotonically with ITA on either test set, and the band strongest internally (very light, 97.6%) is among the weakest externally (65.1%).

**The subgroup finding we could have published as positive.** Restricting the internal set to first-degree burns, the classifier's errors fell on markedly darker-appearing skin than its correct predictions:

> median ITA **19.2** for the 21 errors against **38.4** for the 60 correct predictions — a 19-point gap crossing a band boundary, Mann-Whitney ***p* = 0.0025**, rank-biserial −0.45, **surviving Bonferroni correction** across all 15 tests in the probe (threshold 0.05/15 = 0.0033).

That is a large effect, in the direction the fairness literature predicts and worries about. Reported alone, it would read as clear evidence of bias.

**It does not replicate.** The identical test on the external set, same arm, same class, gives ***p* = 0.35 with the effect in the opposite direction** (rank-biserial +0.10). This is not a power failure: the external cell contains **139** images against the internal cell's 81, so the replication attempt was the **better-powered** of the two.

**Nor is it stable across training runs.** Repeating the test on each of the ten classifier seeds:

| | Result |
|---|---|
| Seeds reaching *p* < 0.05 | **3 of 10** |
| *p*-value range | 0.025 to 0.72 (median 0.20) |
| Seeds with the effect in the same direction | **10 of 10** |

Whether the effect is "significant" is a property of the seed. The *direction*, however, is consistent in all ten. We deliberately do **not** convert that into a sign test, because ten classifiers trained on the same images and scored on the same 205 photographs produce heavily correlated errors and the runs are not independent draws.

**Our conclusion is conservative:** this study provides no usable evidence about skin-tone fairness in either direction. We report the subgroup signal in full rather than deleting it, because suppressing it would be exactly the selective reporting the paper criticises — and because a bias result is one a reader wants to believe and a reviewer is unlikely to challenge, which makes it the most seductive of our false positives. Establishing whether these models are equitable requires data with recorded phototype and a pre-registered analysis.

**Limits, stated plainly:** ITA from uncontrolled web photographs is a proxy for *apparent skin tone in the image*, not constitutive phototype. White balance, illumination, camera processing and perilesional erythema all shift it. The darkest bands contain 9 and 5 images. This is exploratory and is not a fairness audit.

---

# 14. Giving the pipeline its best configuration

This is the project's final and, we think, most useful experiment.

## 14.1 The flaw we found in our own test

The pipeline's classifier is trained on **ground-truth** masks, because that is what the classification dataset provides. But at inference it receives masks **predicted** by the localiser. Those distributions are not the same: predicted masks are ragged, sometimes miss part of the lesion, and occasionally cover the whole frame. A classifier trained only on perfect masks has never seen that.

Attributing the pipeline's deficit to *segmentation quality*, as our earlier analysis did, presumes the answer. The deficit could equally be a **train/test distribution mismatch** — and nobody had tested it.

## 14.2 The experiment

Three configurations, **ten seeds each**, against the same standalone classifier:

- **A** — trained on ground-truth masks, tested on predicted *(the published configuration)*
- **B** — trained *and* tested on predicted masks *(matched)*
- **C** — matched, plus mask dilated by 12 px to retain a rim of peri-lesional skin

| Configuration | Internal | Paired diff | External | Paired diff |
|---|---|---|---|---|
| Standalone classifier | 83.61 ± 1.74 | — | 77.81 ± 2.29 | — |
| A: GT-trained, predicted-tested | 81.27 ± 1.74 | −2.34, ***p* = 0.025** | 76.33 ± 1.23 | −1.47, *p* = 0.085 |
| **B: mask source matched** | **83.32 ± 1.50** | **−0.29, *p* = 0.65** | 76.02 ± 1.82 | −1.79, *p* = 0.11 |
| C: matched and dilated | 83.27 ± 2.41 | −0.34, *p* = 0.67 | 75.24 ± 2.45 | −2.57, *p* = 0.008 |

## 14.3 What it means

**Matching the mask source is worth +2.05 percentage points internally** (95% CI +0.11 to +3.99, *p* = 0.041) — most of the gap the published configuration showed. Dilation adds nothing beyond that internally and costs on the external set.

The consequence for the head-to-head is substantial:

> Against the **published** configuration, the classifier leads internally by 2.34 points (*p* = 0.025).
> Against the pipeline's best-**on-test** configuration (regime B), the two systems are not statistically distinguishable — internally −0.29 (*p* = 0.65), externally −1.79 (*p* = 0.11).
>
> **But regime B was selected on test.** Validation ranks C first (84.37 vs 83.45 vs 83.35), and against regime C the external difference **is** resolved: +2.57 pp, 95% CI [+0.87, +4.27], *p* = 0.008. The external half of the parity claim is therefore withdrawn. Internal parity holds under either regime (*p* = 0.65 / 0.67).

The conservative reading is the one the evidence now supports: **a tie is not a win, and externally it is not even a tie.** Internally the pipeline reaches parity while running two models at 1.6× the latency, which does not justify the cost on accuracy grounds. Externally, once the configuration is chosen on validation rather than on test, the plain classifier is simply ahead.

Both readings agree on the fact: the published configuration understated the design by about two points, and no configuration we tried beats the simpler alternative.

## 14.4 A three-seed pilot that lied

A three-seed pilot of this experiment put regime C at **83.90 percent** against the classifier's 83.61, and appeared to win. At ten seeds it is **83.27 with an SD of 2.41**, and it loses.

That is the eighth time in this project a three-seed result did not survive ten — and on this occasion, the result it offered was the one we wanted. It is in the paper for exactly that reason.

---

# 15. The methodological findings

These are the transferable outputs, independent of burns. Each was discovered while building the benchmark; each changed an answer we had already obtained.

## 15.1 Splitting augmented files at random

Manufactured a masking benefit of +2.07 pp (matched pool) that falls to +0.55 [−0.37, +1.47] once grouped by source photograph. **Lesson:** datasets augmented before splitting must be partitioned by source image.

## 15.2 Trusting identifier-based grouping

The standard correction still left 2 of 205 test images perceptually identical to a training image under a different identifier, one pair with conflicting labels. **Lesson:** identifier grouping is a heuristic, not a proof; verify with a content-based check.

## 15.3 Using three training seeds

Overstated the internal margin, narrowed its interval threefold, and concealed the external margin entirely. Of 120 three-seed subsets of ten runs, only 15 detect the external effect. **Lesson:** three seeds neither estimate a variance nor support an interval.

## 15.4 Testing a subgroup on one dataset

A large, Bonferroni-surviving skin-tone association reversed and vanished on a better-powered external cell, and was significant in only 3 of 10 seeds. **Lesson:** a single-dataset subgroup finding — a fairness finding included — is subject to the same replication failure as a single-dataset accuracy claim.

## 15.5 Correcting the split for one stage only

Our source-grouped split was built for the classifiers and never propagated to the segmentation models, which kept the collection's original split. **179 of 205 internal test images (87.3 percent)** sat in their training or validation folds — 145 in training, 34 in validation, leaving only 26 the models had never seen.

We retrained both segmentation models on the source-grouped split under the original recipe, changing nothing but the partition:

| | Internal | External |
|---|---|---|
| Contaminated | 90.7% | 48.9% |
| Leak-free | **78.0%** | **66.8%** |

The internal drop is **12.7 pp** (exact McNemar, 33 vs 7 discordant, *p* = 4×10⁻⁵). But we then disclose a confound in our own headline: **the corrected partition also leaves 21 percent less training data** (2,425 vs 3,081 images). On the 26 test images *neither* model saw, the contaminated model still leads by 7.7 pp — which cannot be leakage. The leak-attributable excess is about 5.7 pp, but with n=26 the bootstrap interval runs 0.0 to 19.2 and cannot separate the mechanisms cleanly.

The internal-to-external drop tells the cleaner story: **41.8 points for the contaminated model against 11.2 for the leak-free one**. That excess is the leakage signature.

**We then closed the question for the pipeline**, retraining its ten Swin-Tiny classifiers and re-scoring on the corrected localiser. We expected the pipeline to be inflated. It was not:

> Pipeline: 80.98 ± 2.22 → **80.88 ± 1.50**. Margin: +2.63 → +2.73.

A leak worth 12.7 points to the standalone model was worth **0.10 points** to the pipeline, because in the pipeline the grading is done by a classifier that was never contaminated and the localiser contributes only a mask.

**Lesson:** a correction applied to one stage of a pipeline must be propagated to every stage and re-audited — and **contamination does not propagate uniformly**; where it lands depends on which stage the metric actually depends on.

## 15.6 Choosing the summary metric

The internal margin holds on plain accuracy (+2.63, *p* = 0.032) but **not** on balanced accuracy (+1.45, 95% CI −0.74 to +3.65, *p* = 0.17, ahead in only 6 of 10). The external margin survives both (+1.96, *p* = 0.028). **Lesson:** which of two standard summaries you report can decide whether a comparison is established at all.

## 15.7 Selecting the comparison arm on test

The paper described the classifier arm as "the best Benchmark 1 condition, ConvNeXt-Large." Best **on test**. Ranked by *validation*, Swin-Tiny wins (85.44 vs 84.47) and scores 82.44 on test against ConvNeXt-Large's 84.88.

| Against the seed-42 pipeline (81.46%) | Margin |
|---|---|
| Test-selected arm (what we used) | +3.41 pp |
| Validation-selected arm | **+0.98 pp** |

**Honest selection removes 71 percent of the internal margin.** We selected a model from a pool of eleven on the set we then scored it on. **Lesson:** a comparison arm chosen on the test set inherits a selection effect that can exceed the difference under study.

The consequence, stated in the manuscript's Limitations: **the internal head-to-head is not reported as an effect estimate.**

---

# 16. Reproducibility infrastructure

Everything above is checkable, and we built the infrastructure to make checking cheap.

## 16.1 The verification script

`verify_paper_numbers.py` recomputes **205 published quantities** from committed raw data — no GPU, no dataset download, no model weights, under a minute:

```bash
pip install numpy scipy
python verify_paper_numbers.py
```

It covers the leakage artifact and matched pools, the masking null with its Wilcoxon and Mann-Whitney tests, three- and ten-seed head-to-head means and paired intervals, all 120 three-seed subsets, exact McNemar tests recomputed from per-image predictions, segmentation mAP, the oracle-mask bound, both pipeline variants, timing, BIP_US balanced accuracy, the ITA probe and its non-replication, source-clustered bootstraps, the segmentation-split leak, the architecture-selection effect, threshold selection, and the three mask regimes.

**Several checks exist specifically to catch us overstating our own results** — for example, confirming that the matched-pool leakage contrast is the smaller 2.07 → 0.55 rather than 3.06 → 0.55, and that the internal interval-narrowing factor is 3.35 rather than the "four times" an earlier draft claimed.

## 16.2 Released artifacts

| Artifact | Location |
|---|---|
| Code, split builder, analysis scripts | Repository |
| Kaggle notebooks, exactly as executed | `code/kaggle-notebooks/` |
| Per-image predictions behind every table and figure | `benchmark2-proof/results/` |
| Raw result JSON for every analysis | `statistics/` |
| Trained weights (5 checkpoints, 734 MB) | `v1.0-melba` release |
| Manuscript source, bibliography, cover letter | `paper/` |

**Both the contaminated and the corrected segmentation models are published deliberately**, so the leak can be reproduced as readily as its correction.

The split builder (`build_seg_split_leakfree.py`) verifies its own output and **refuses to emit a dataset in which any source photograph appears in two folds**. The training notebooks re-verify the same property inside the Kaggle kernel before spending a single GPU-hour.

## 16.3 Licensing

Code under **MIT**; data, figures, predictions and weights under **CC BY 4.0**, matching the licence of the primary source data. The project originally used AGPL-3.0, which was changed because network copyleft is a poor fit for an artifact whose purpose is to be reused.

---

# 17. Publication process

## 17.1 First submission

Submitted to the **Turkish Journal of Electrical Engineering & Computer Sciences** (TJEECS), manuscript TURKJELECENGCOMPSCI-S-26-02236. Returned at editorial screening without external review.

The form letter lists five criteria. Assessing honestly which we failed:

| Criterion | Assessment |
|---|---|
| Technical standard, reproducible methods | Met, strongly |
| Conclusions justified, speculation labelled | Met |
| Novelty emphasised via recent literature | **Partly failed** — the Introduction cited nothing from 2024+ |
| "A significant breakthrough of general interest" | **Failed, by design** — the paper explicitly disclaims being a breakthrough |
| Clear language | Met |

The fourth criterion is the diagnosis. TJEECS screens for breakthroughs; this paper reports a careful negative-to-neutral result. That is a **venue mismatch**, not a defect in the work.

## 17.2 Redirection to MELBA

The *Journal of Machine Learning for Biomedical Imaging* fits substantially better:

- Its stated scope explicitly includes **"empirical comparisons."**
- Its reviewer form explicitly scores **"Reproducibility: is the code and/or data shared?"** — a criterion this paper is built to win.
- It is free to publish (USD 10 platform submission fee), CC BY 4.0, single-blind.

Single-blind review also means the repository can be public at submission, which it now is.

## 17.3 Manuscript preparation

The manuscript was ported to `melba.cls` — a substantial job, since MELBA uses two-column layout, author-year citations and BibTeX. Along the way we found and patched a bug in MELBA's own class file: `melba.cls` defines `\doi{}` as a *setter* for the paper's DOI header (`\def\doi#1{\gdef\@doi{#1}}`), which collides with the `\doi{}` that `plainnat.bst` emits for every reference. Unpatched, every reference DOI vanishes **and** the last reference's DOI overwrites the paper's own header and Crossmark link.

The manuscript was also restructured to lead with the method rather than with the sequence of self-corrections. The corrections remain — every number and caveat intact — but they appear where methodological controls belong, and the sensitivity analysis is a table in Results rather than the paper's opening frame.

---

# 18. Post-mortem: what we would do differently

An honest list, because it is the most useful thing a reader can take from this.

1. **Build the split first, and audit it before training anything.** Every downstream problem traces to a split built after augmentation. The audit costs an afternoon; the error cost months.

2. **Audit the split with content, not identifiers.** Perceptual hashing found duplicates that filename grouping could not. It should be the default, not a follow-up.

3. **Propagate corrections to every stage, then re-audit.** We fixed the classifier split and assumed the pipeline was clean. It was not, for 87.3 percent of the test set.

4. **Budget for ten seeds from the start.** Three seeds cost us more analysis time than ten seeds would have cost in compute. Eight separate three-seed results in this project failed to replicate at ten.

5. **Match your training distribution to your test distribution.** The single largest correction to the pipeline's measured performance — +2.05 pp — came from training the classifier on the kind of masks it would actually receive.

6. **Select models on validation, always.** Choosing the comparison arm on test accounted for 71 percent of an internal margin.

7. **Pre-specify metrics.** Plain and balanced accuracy disagreed about whether the internal comparison held.

8. **Archive every checkpoint.** The original Swin-Tiny weights were lost, which forced a full retrain to answer a question that should have taken ten minutes of inference.

9. **Write the verification script early.** Building it late meant reconstructing provenance for numbers already in a manuscript — and revealed that one published row (79.5 / 68.7 / 74.6 for the standalone YOLO) had no archived provenance at all and reproduced under no aggregation rule.

---

# 19. Summary of final results

**The scientific question.** Does isolating the burn improve severity classification?

| Finding | Evidence |
|---|---|
| Masking helps **only** with perfect masks, and only slightly | +0.55 pp, 95% CI [−0.37, +1.47], oracle upper bound |
| The published pipeline configuration **understated** the design | Matching mask source: **+2.05 pp**, *p* = 0.041 |
| Corrected, the two are indistinguishable **internally** | Internal −0.29 (*p* = 0.65 for B, 0.67 for C) |
| Externally the classifier is **ahead** once the regime is chosen on validation | +2.57 pp, 95% CI [+0.87, +4.27], *p* = 0.008 (regime C) |
| The pipeline costs 1.6× latency for that parity | 42.3 ms vs 25.8 ms |
| Segmentation quality is the binding constraint | Localiser mask mAP50 0.695 |
| The model **does not transfer** to clinical images | Severity scale offset; 51% of BIP_US images graded first degree |
| Under-grading is the dangerous direction, present on both sets | 19.3% internal, 28.3% external (*z* = 1.77, *p* = 0.08) |
| No usable evidence on skin-tone fairness in either direction | Internal *p* = 0.0025 → external *p* = 0.35, reversed |

**Conclusion.** Segmentation-guided classification attains **internal parity at best** with a plain classifier, never advantage, and externally the classifier remains ahead under honest configuration selection. Its value is localisation and interpretability — the system returns *where* the burn is, and a clean region a clinician can inspect — but that is not the property the design was adopted for, and it is not free.

**The methodological contribution**, which we consider the more transferable output: seven conventional evaluation choices, each of which changed an answer we had already obtained, each measured against its corrected baseline on the same data. None is specific to burns.

---

# Appendix D — Chronology

The order matters, because several findings are only intelligible as consequences of earlier ones.

**Phase 1 — Build (graduation project).** Dataset acquired from Roboflow. YOLOv8x-seg localiser and Swin classifier trained. Flask backend and Flutter application built and deployed. A separate iOS SwiftUI application with on-device LibTorch inference produced as a secondary artifact. At this stage the system worked end to end and the team had a demonstrable product.

**Phase 2 — First benchmark.** Twenty-one architectures trained under masked and unmasked conditions. Masking appeared to help 20 of 21 by a mean of +3.06 pp. This was written up as the project's headline finding. It was wrong.

**Phase 3 — The leakage audit.** An audit of the split procedure found that the masked arm had been re-split 70/15/15 after flattening while the unmasked arm retained the collection's own 90/6/4 partition. Leak rates: 80.5 percent against zero. The headline finding dissolved.

**Phase 4 — Rebuild.** Source-grouped split constructed over 1,370 source photographs. Benchmark 1 re-run on 11 architectures across four input conditions. The masking benefit fell to +0.55 pp with an interval spanning zero. Benchmark 2 head-to-head established on three seeds.

**Phase 5 — External validation.** BIP_US clinical database evaluated. Second Roboflow collection decontaminated by perceptual hashing, 118 images removed, 319 retained from 175 sources. Transfer failure documented in both.

**Phase 6 — Statistical hardening.** Ten-seed replication of the head-to-head. The three-versus-ten contrast revealed that the conventional protocol had overstated one margin and concealed the other. The 120-subset analysis isolated seed count from the recipe change.

**Phase 7 — First submission and desk rejection.** Submitted to TJEECS; returned at editorial screening without review. Diagnosed as a venue mismatch on the "significant breakthrough" criterion, with a fair secondary criticism about recent-literature positioning.

**Phase 8 — Redirection and audit.** Redirected to MELBA. A systematic audit of the manuscript against its own raw data followed, producing the fairness probe, the segmentation-split discovery, the metric-choice finding, the architecture-selection finding, and corrections to seven mischaracterised citations and thirty-one incorrect author names.

**Phase 9 — Closing the open questions.** Segmentation models retrained leak-free. Pipeline arm re-scored on the corrected localiser. Mask-regime experiment run at ten seeds, establishing that the published configuration had understated the pipeline by about two points and that corrected, the two systems are indistinguishable.

**Phase 10 — Preparation.** Manuscript restructured to lead with the method. Repository made public under MIT with CC BY 4.0 data. Verification extended to 200 checks.

**Phase 11 — Repositioning after external review.** The paper was retitled from *Segmentation-guided burn severity classification* to *When Leakage Changes the Conclusion: A Methodological Evaluation of Segmentation-Guided Burn Severity Classification*, because the methodological result is the transferable one. Four figure changes followed. Figure 3 was rebuilt on ten seeds — it had been plotting three-seed error bars, the very protocol Section 4.9 argues against, and its caption still carried the discredited +3.74 internal margin. A new Figure 4 plots the published pipeline against its best configuration. Figure 1 was extended upward to show the data and training path, so the source-grouped split now appears in a figure. Figure 5's example images were replaced: the third-degree panel had been an identifiable facial burn and the second-degree panel carried case-report annotation letters. Three new sections were added — *Why segmentation did not win* (the mechanism behind the null), *What this generalises to*, and *What we learned* — plus an expanded *Future work*. Verification grew to 205 checks: four pin claims that only a figure makes, and one checks the ten-seed regime JSON against the archived stdout of the Kaggle run that produced it, seed by seed. One false statement was caught and removed in the process: the Data Availability statement still said the pipeline arm could not be re-evaluated because the Swin-Tiny weights were unarchived, which Phase 9 had already made untrue.

---

# Appendix E — Statistical methods

Stated compactly, because the choices are load-bearing.

**Accuracy intervals.** Wilson score intervals for proportions, which behave correctly at the sample sizes here (N = 205 and N = 319) where the normal approximation does not.

**Source-clustered intervals.** For the external set, a cluster bootstrap resampling the **175 source photographs** with replacement, 20,000 resamples, percentile method. Because 319 images derive from 175 sources, an interval on N = 319 is too narrow; clustering widens it by roughly a fifth. The clustered interval is the one relied upon.

**Image-level comparison.** Paired exact McNemar on discordant pairs. Used when the question is whether one system beats another *on a particular test set*.

**Run-level comparison.** Paired *t* on per-seed accuracy differences, with the Wilcoxon signed-rank as a distribution-free companion. Used when the question is whether one system beats another *on average across training runs*. These two estimands are never conflated.

**Masking ablation.** Wilcoxon signed-rank over architecture-seed pairs, with the effect reported as a point estimate and confidence interval rather than against a detectability threshold. An earlier version of the analysis reported a minimum detectable effect; this was withdrawn because the interval is the more informative and less misleading summary.

**Subgroup analysis.** Mann-Whitney on the continuous ITA rather than on binned categories, so that no conclusion depends on where band edges fall. Bonferroni correction over the 15 tests actually reported in the probe.

**Standard deviations.** Sample standard deviation, denominator *n* − 1. An early version of the results file stored population standard deviations, which understated the spread by about 18 percent at *n* = 3; all reported figures were corrected.

**Pooling.** Where two training recipes were pooled, the pooling is stated as an assumption rather than as something a significance test established, on the grounds that a Welch test with seven runs against three has almost no power and that a non-significant result is not evidence of equivalence.

**What we did not do.** No multiple-comparison correction is applied across the paper as a whole, because the analyses answer distinct pre-specified questions rather than searching one hypothesis space; where a search *was* performed — the skin-tone probe — Bonferroni is applied and stated.

# Appendix A — Model inventory

| Model | Role | Key metric |
|---|---|---|
| `yolov8x-seg_1class_LEAKFREE.pt` | Localiser, source-grouped split | Test mask mAP50 **0.695** |
| `yolov8x-seg_3class_LEAKFREE.pt` | Standalone segmenter, source-grouped | mAP50 0.566; 78.0% internal / 66.8% external |
| `yolov8x-seg_1class__best.pt` | Original localiser — **contaminated** | mask mAP50 0.726 |
| `yolov8x-seg_3class__best.pt` | Original standalone — **contaminated** | 90.7% internal / 48.9% external |
| `swin-small_masked__best_cnn_mask.pth` | Classifier in the mobile demonstration | — |

Not archived, and its absence is disclosed: the benchmark's original Swin-Tiny checkpoints.

# Appendix B — Experiment inventory

| # | Experiment | Scale | Output |
|---|---|---|---|
| 0 | Naive-split masking ablation | 21 architectures | +3.06 pp — **leakage artifact** |
| 1 | Leak-free masking ablation | 11 arch × 4 conditions, seeds 0/1/42 | +0.55 pp [−0.37, +1.47] |
| 2 | Head-to-head, original | 3 seeds | +3.74 internal / +3.24 external |
| 3 | Head-to-head, ten-seed replication | 10 seeds, both arms | +2.63 / +2.79 |
| 4 | 120 three-seed subsets | Re-analysis, 0 GPU | 15/120 detect the external effect |
| 5 | External validation | 319 + 94 images | Transfer failure, under-grading |
| 6 | Perceptual-hash decontamination | 1,371 → 319 images | 118 removed |
| 7 | Skin-tone ITA probe | 194 + 319 images, 10 seeds | Non-replicating null |
| 8 | Segmentation-split leak audit | 205 test images | 87.3% contaminated |
| 9 | Segmentation retraining | 2 × YOLOv8x-seg, 100 epochs | 12.7 pp leak measured |
| 10 | Pipeline arm re-score | 10 × Swin-Tiny | Leak worth 0.10 pp |
| 11 | Mask-regime experiment | 3 regimes × 10 seeds | **+2.05 pp; internal parity only** |
| 12 | Threshold sweep on validation | 10 thresholds | 0.05 not tuned on test |
| 13 | Architecture-selection audit | 11 architectures | 71% of margin |

# Appendix C — Verification

```
$ python verify_paper_numbers.py
...
  205/205 checks passed
```

Every quantity in this document and in the manuscript is recomputed from raw data committed to the repository. Any reader can run it in under a minute, and any reader who finds a discrepancy has found a real error.
