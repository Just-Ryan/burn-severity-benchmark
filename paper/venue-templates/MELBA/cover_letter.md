# MELBA — cover letter

> **Upload this as an additional file in Scholastica with the descriptor "Cover Letter".** It is on MELBA's own submission checklist.
> **The GenAI paragraph below is MANDATORY, not optional:** "Authors are required to state in the cover letter if and how GenAI or LLMs were used" (https://www.melba-journal.org/for_authors.html, verified 2026-07-25). Do not delete or shorten it.
> Replace `[DATE]` before sending. Check the current Editors-in-Chief at https://www.melba-journal.org/about.html — do not guess names.

---

[DATE]

The Editors
*Journal of Machine Learning for Biomedical Imaging* (MELBA)

Dear Editors,

We submit for your consideration our manuscript, **"A comparative study of deep learning approaches for automated burn injury segmentation and severity classification."**

**What the paper is.** It is an empirical evaluation study built around a deployed burn-severity system, and its central finding is a negative one that we did not expect and did not want. We report it because we think it generalises well beyond burns.

We built a two-stage system — a YOLOv8x-seg localiser feeding a masked Swin transformer classifier, served through a smartphone application — on the premise that masking the classifier's input to the segmented burn region improves severity grading. Our own early experiments supported that premise: masking improved accuracy by 3.06 percentage points across 20 of 21 architectures, with a Wilcoxon p-value of 7 × 10⁻⁵.

The premise was wrong, and the reason is a data-handling failure that we believe is widespread. The public dataset we used, like many hosted image collections, is distributed pre-augmented: each source photograph exists as roughly 2.5 near-duplicate files under distinct names. Splitting those files at random scattered copies of the same photograph across training and test. In the masked arm this leaked **80.5% of the test set**; the separately partitioned unmasked arm leaked none, and the asymmetry manufactured the entire effect. The cleanest evidence is within a single model on a single test set, with no confounds at all: the masked classifier scored **95.9% on the 417 test images whose source photograph had appeared in training and 82.2% on the 101 whose had not** — a 13.7-point gap attributable only to memorisation.

We rebuilt the split by source photograph and re-ran the comparison. Over 24 architecture–seed pairs the masking effect is **+0.55 percentage points, 95% CI −0.37 to +1.47** (Wilcoxon p = 0.32, 13 of 24 pairs improved). We report the interval rather than a significance verdict, so the claim is "no benefit larger than about 1.5 points," not "the effect is zero." Because the masking ablation used **ground-truth** polygons, it is an oracle upper bound: no better segmenter could have rescued a gain that is absent under perfect masks.

**What else the paper contributes.** A multi-seed head-to-head in which a plain classifier outperforms our own segmentation-first pipeline (paired per-seed difference +3.74 points, 95% CI +3.04 to +4.44, paired t p = 0.002), reported alongside the honest caveat that at N = 205 an image-level McNemar test reaches 80% power only near 8.5–9 points. And two independent external evaluations: on a clinical database from the University of Seville the model collapses to 30.5–35.0% balanced accuracy and under-grades 55 of 94 images against 2 over-grades, while on a perceptual-hash-cleaned web-sourced set the decline is far milder — consistent with clinical photography being the larger distribution shift.

**Why MELBA.** The paper is an empirical comparison in medical imaging with a data-quality finding at its centre, which is squarely within your stated scope, and it is the kind of work that mainstream venues decline for lack of methodological novelty. We claim no novelty: there is no new architecture, loss or algorithm here. What we offer is a matched before-and-after measurement of a leakage artifact on the same data with the same architectures, plus a within-model decomposition isolating memorisation, and an external evaluation that shows in-distribution ranking failing to predict clinical usefulness.

**Self-identified corrections.** During an internal re-audit we found and corrected several failures in our own reporting: we had promised Wilson confidence intervals and printed none; we had asserted categorically that no source photograph appeared in more than one fold, and a content-based check found 2 of 205 test images (1.0%) that violate it, one pair carrying conflicting labels; our external set of 319 images derives from only 175 distinct source photographs and is therefore not 319 independent observations; and one reported Mann-Whitney p-value was the one-sided value, unlabelled. All are now disclosed in the manuscript with quantified bounds. We mention this in the cover letter because the paper argues that the field under-scrutinises its own favourable results, and we would rather meet that standard than merely recommend it.

**Reproducibility.** Code, the exact source-grouped split recipe, the 205-filename test manifest, and the per-image predictions behind every reported statistic are publicly released, and the manuscript carries a Data Availability Statement.

**Use of generative AI and large language models.** As required by MELBA's author policy, we state here how such tools were used. We used Anthropic Claude (Claude Code) to organise the project materials, to reproduce and check our reported results against the raw output files, to run the statistical, benchmarking and external-validation analyses — including the leak-free re-runs and the perceptual-hash leakage check — and to draft and edit the manuscript text, tables and figure captions. All drafting was performed from author-supplied results, under author direction, and every claim was reviewed and verified by the authors against the source files; no content was generated de novo without author supervision. The research itself — system design, model training, dataset preparation and the mobile application — was conceived and carried out by the authors. No LLM is listed as an author, and the authors take full responsibility for the content of the manuscript. A corresponding disclosure appears in the Acknowledgement section of the manuscript.

**Declarations.** This manuscript is previously unpublished, is not under consideration at any other journal or conference, and is not an extension of a conference paper. It is available as a preprint at [arXiv:XXXXX — **complete or delete**]. The study used only publicly available, de-identified burn photographs (Roboflow Universe, CC BY 4.0) and an independent public research database provided for research by the Biomedical Image Processing Group of the University of Seville; no new human-subjects data were collected and institutional review board approval was therefore not required. The authors report no financial, organizational, commercial or personal conflicts of interest, have received no funding, and have not recently collaborated with any member of the MELBA editorial board.

Thank you for considering our work.

Sincerely,

**Ryan Altayeb**, on behalf of all authors
Corresponding author — altayeb.ray@gmail.com — ORCID 0009-0006-0031-9531
Faculty of Computer and Information Systems, Islamic University of Madinah, Madinah, Saudi Arabia

Co-authors: Abdulrahman Alraddadi (ORCID 0009-0000-2325-5063), Mohannad Alrehaili (ORCID 0009-0008-2491-185X)
