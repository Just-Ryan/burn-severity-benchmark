# CMPB — cover letter

> **A cover letter is MANDATORY at CMPB**, and its content is prescribed. The submission portal requires it to state "why the submission is appropriate for publication in Computer Methods and Programs in Biomedicine", what is already known, what your study adds, and that the work is unpublished. The letter below covers all four — the headings are deliberate, keep them.
> Replace `[DATE]`. Check the current Editor-in-Chief at https://www.sciencedirect.com/journal/computer-methods-and-programs-in-biomedicine/about/editorial-board — do not guess.

---

[DATE]

The Editor-in-Chief
*Computer Methods and Programs in Biomedicine*
Elsevier Ireland Ltd

Dear Editor,

We submit for your consideration our manuscript, **"A comparative study of deep learning approaches for automated burn injury segmentation and severity classification,"** as an original research article.

### Why this submission is appropriate for *Computer Methods and Programs in Biomedicine*

The journal's stated aims include encouraging "the development of formal computing methods, and their application in biomedical research," reporting "new computer methodologies applied in biomedical areas," and "the eventual distribution of demonstrable software to avoid duplication of effort." Our submission addresses all three.

We contribute a **reproducible evaluation protocol for biomedical image classifiers built on pre-augmented public datasets**, together with the complete software that implements it: a source-grouped partitioning procedure that prevents augmented copies of one photograph from spanning folds, a flip-aware perceptual-hash screen (pHash and dHash) that detects contamination between a training set and a putatively independent external set, and a full benchmarking harness. Code, the exact split-reconstruction recipe, the test-set manifest and the per-image predictions behind every reported statistic are publicly released, so every number in the paper can be recomputed by a reader.

We demonstrate the protocol on a deployed clinical-imaging system — a YOLOv8x-seg localiser feeding a masked Swin transformer classifier, served through a smartphone application for burn-severity assessment — and the demonstration is what makes the case for the protocol.

### What is already known

Deep learning for burn depth assessment is an active area, and published studies routinely report single-dataset accuracies in the 90s. A recent five-year systematic review of convolutional networks applied to burn photographs found that most such studies evaluate on a single dataset, very few validate on an independent source, and dataset handling is frequently under-described. Separately, a broad literature establishes that data leakage is a systemic driver of irreproducible results in machine-learning-based science, and that in-distribution accuracy is a poor predictor of external performance in medical imaging.

What has been missing is a *matched, quantified demonstration* of how a specific, ordinary data-handling choice converts into a specific, publishable-looking effect — measured on the same data, with the same architectures, before and after the fix.

### What this study adds

1. **A quantified leakage case study with both arms measured.** The public dataset we used is distributed pre-augmented: each source photograph exists as roughly 2.5 near-duplicate files. Partitioning those files at random leaked **80.5% of one test set** while a separately partitioned arm leaked none, and the asymmetry manufactured an apparent 3.06-percentage-point benefit for masking across 20 of 21 architectures. The decisive evidence carries no confounds: the same model, on the same test set, scored **95.9% on the 417 images whose source photograph appeared in training and 82.2% on the 101 whose did not.**
2. **The corrected measurement.** After source-grouped partitioning, the masking effect is **+0.55 percentage points, 95% CI −0.37 to +1.47** (Wilcoxon p = 0.32). Because the ablation used ground-truth polygons, it is an oracle upper bound — no better segmenter could recover a gain absent under perfect masks.
3. **A fair multi-seed comparison** in which a plain classifier outperforms the segmentation-first pipeline (paired per-seed difference +3.74 points, 95% CI +3.04 to +4.44, p = 0.002), reported with the honest power caveat that image-level McNemar testing at N = 205 resolves only differences near 8.5–9 points.
4. **Two independent external evaluations**, one of them a genuinely clinical database, on which the system collapses to 30.5–35.0% balanced accuracy and under-estimates burn depth in 55 of 94 images against 2 over-estimates — a clinically dangerous asymmetry, and a direct demonstration that in-distribution ranking does not predict usefulness.
5. **Released, documented software** implementing the whole protocol.

### What we do not claim

We claim no methodological novelty in the modelling sense: there is no new architecture, loss or algorithm, and we say so explicitly in the manuscript. The system is a research and demonstration artifact, not a clinically validated device. The training data come from a single web source with community-provided labels, the internal test set is 205 images, and we have performed no analysis of performance across skin tones — a limitation we state prominently.

We also report, unprompted, several corrections we identified in our own reporting during an internal re-audit: confidence intervals we had promised and not printed; a categorical claim about fold independence that a content-based check falsified for 2 of 205 test images; an external set of 319 images that derives from only 175 source photographs and is therefore not 319 independent observations; and an unlabelled one-sided p-value. All are now disclosed with quantified bounds. We mention this because a paper arguing that the field under-scrutinises its own results should be held to that standard first by its authors.

### Declarations

This manuscript is original, has not been published previously, and is not under consideration by any other journal. It is available as a preprint at [arXiv:XXXXX — **complete or delete this clause**]; preprint posting does not constitute prior publication under the journal's policy. The study used only publicly available, de-identified burn photographs (Roboflow Universe, CC BY 4.0) and an independent public research database provided for research by the Biomedical Image Processing Group of the University of Seville. No new human-subjects data were collected, and institutional review board approval was therefore not required. The authors declare no competing interests and received no funding. Author contributions are given using CRediT roles, and the use of generative AI in preparing the manuscript is declared in full in the section immediately preceding the reference list. All authors have read and approved this submission. **Ryan Altayeb is the sole corresponding author.**

Thank you for considering our work.

Sincerely,

**Ryan Altayeb**, on behalf of all authors
Corresponding author — altayeb.ray@gmail.com — ORCID 0009-0006-0031-9531
Faculty of Computer and Information Systems, Islamic University of Madinah, Madinah, Saudi Arabia

Co-authors: Abdulrahman Alraddadi (ORCID 0009-0000-2325-5063), Mohannad Alrehaili (ORCID 0009-0008-2491-185X)
