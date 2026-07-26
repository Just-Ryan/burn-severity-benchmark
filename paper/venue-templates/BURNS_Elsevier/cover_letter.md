# Burns — cover letter

> **Note:** *Burns* does not document a cover-letter requirement (UNVERIFIED as of 2026-07-25), but Editorial Manager exposes the field and a good letter is never wasted. Paste this into the "Comments" / cover letter box, or upload as a PDF.
> **Update the bracketed items before sending.** Replace `[DATE]` and check the editor's name on https://www.sciencedirect.com/journal/burns/about/editorial-board — do not guess it.

---

[DATE]

The Editors
*Burns* — Journal of the International Society for Burn Injuries
Elsevier

Dear Editors,

We submit for your consideration our manuscript, **"A comparative study of deep learning approaches for automated burn injury segmentation and severity classification,"** as an Original Paper.

**Why we are sending this to a burn journal rather than an engineering one.** The paper's most important result is a patient-safety result. We built a smartphone burn-severity assessment tool of the kind increasingly proposed for settings without a burn specialist, and we then tested it honestly. On our own held-out data it scores 82.6% accuracy — comfortably in the range that the burn deep-learning literature routinely reports. On an independent clinical database of 94 photographs from the Biomedical Image Processing Group at the University of Seville, the same system **under-estimated burn depth in 55 of 94 images against 2 over-estimates, and classified roughly half of the full-thickness burns as first degree.** Balanced accuracy fell to 30.5–35.0% on a two-class probe.

We think that finding belongs in front of burn clinicians, because the direction of the failure is the dangerous one. A tool that over-calls severity wastes a referral. A tool that under-calls it sends a deep dermal or full-thickness burn toward conservative management and delays specialist assessment. Our system does the second, and it does so while looking accurate on internal metrics.

**Why the internal number was misleading, and why that matters to your readers.** Investigating our own results, we found that our original favourable finding was an artifact of how the dataset had been split. The public dataset we used, like many hosted image collections, ships pre-augmented: each source photograph exists as roughly 2.5 near-duplicate files. Splitting those files at random — the ordinary, obvious thing to do — placed copies of the same photograph in both training and test. In one of our experimental arms this leaked **80.5% of the test set**, and it manufactured an apparent 3.06-percentage-point benefit for our segmentation-first design across 20 of 21 network architectures. When we rebuilt the split so that all copies of a photograph stay in one fold, the benefit collapsed to 0.55 points with a confidence interval spanning zero. The cleanest evidence is within a single model on a single test set: it scored 95.9% on the test images whose source photograph had appeared in training and 82.2% on those whose had not.

We report this because we believe it is a live problem in the burn imaging literature specifically. A recent five-year systematic review of CNN work on burn photographs found that most studies report strong single-dataset accuracies, very few evaluate on an independent source, and dataset handling is often under-described. Our paper offers your readership a quantified, mechanistically explained example of how such a number can be produced without anyone doing anything dishonest — and a simple procedural rule that prevents it: **partition by source photograph, not by file.**

**What else the paper reports.** A fair multi-seed head-to-head showing that a plain classifier is more accurate than our own segmentation-first pipeline, so segmentation is justified here by localisation and interpretability rather than by accuracy; an ablation using ground-truth masks, which establishes that no better segmenter could have rescued the result; and a second, web-sourced external set, cleaned by perceptual hashing, on which the decline is milder than on the clinical images — consistent with clinical photography being the larger distribution shift.

**What we are careful not to claim.** This is not a clinically validated device and we say so repeatedly in the manuscript. There is no new architecture and we claim no methodological novelty. The study uses a single web-sourced training collection with community-provided labels, an internal test set of 205 images, and no analysis of performance across skin tones — a limitation we state prominently, because pigmentation directly confounds erythema-based depth assessment and we do not want a reader to assume otherwise.

**Declarations.** This manuscript is original, is not under consideration elsewhere, and has not been published previously. It [has not been posted to a preprint server / is available as a preprint at arXiv:XXXXX — **delete whichever does not apply**]. The study used only publicly available, de-identified burn photographs (Roboflow Universe, CC BY 4.0) and an independent public research database provided for research by the University of Seville; no new human-subjects data were collected and institutional review board approval was therefore not required. The authors declare no conflict of interest and received no funding. Generative AI assistance in preparing the manuscript is declared in full in the section before the reference list, and the completed journal disclosures form accompanies this submission. All authors have read and approved the submission.

Thank you for considering our work.

Sincerely,

**Ryan Altayeb**, on behalf of all authors
Corresponding author — altayeb.ray@gmail.com — ORCID 0009-0006-0031-9531
Faculty of Computer and Information Systems, Islamic University of Madinah, Madinah, Saudi Arabia

Co-authors: Abdulrahman Alraddadi (ORCID 0009-0000-2325-5063), Mohannad Alrehaili (ORCID 0009-0008-2491-185X)
