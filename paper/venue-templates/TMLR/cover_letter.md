# TMLR — cover letter / action-editor note

> **How to use this.** TMLR's OpenReview submission form has **no cover-letter field**. Do not try to paste this into the abstract. Use it in three places instead:
> 1. As the body of the email you send when TMLR asks you to **recommend action editors** after submission.
> 2. As your prepared answer if an action editor queries **scope** before assigning reviewers.
> 3. As a private note to yourself: if you cannot write this letter honestly, the paper is not framed correctly for TMLR yet.
>
> **Anonymity:** while under review, do not send this from an identifying address to reviewers, and do not include the author block. The version below is the *post-submission, editor-facing* version; strip §"Authors" if you use it anywhere reviewers can see.

---

Subject: TMLR submission — action editor recommendations and scope note

Dear Editors,

Thank you for the opportunity to recommend action editors for our submission, **"When augmentation precedes the split: a leak-free re-analysis of segmentation-first classification on a medical image benchmark."**

**What the paper claims, and what supports each claim.** We have written this submission specifically against TMLR's first acceptance criterion, so we state the mapping directly:

1. *Partitioning a pre-augmented image dataset at the file level leaks catastrophically.* Evidence: 417 of 518 test images (80.5%) share a source photograph with training in one arm of a real, previously-run experiment, while a separately partitioned arm leaks none. The buggy split scripts are archived and released.
2. *That leakage manufactured a positive result.* Evidence: under the leaky split, background masking appears to improve accuracy by +3.06 percentage points in 20 of 21 architectures. The decisive within-model evidence has no confounds at all: the same masked classifier scores 95.9% on the 417 test images whose source appeared in training and 82.2% on the 101 whose source did not — one model, one test set, a 13.7-point gap attributable only to memorisation.
3. *After a source-grouped split, the effect is absent.* Evidence: +0.55 percentage points over 24 architecture-seed pairs, 95% CI −0.37 to +1.47, Wilcoxon p = 0.32, 13 of 24 pairs improved. We report the interval rather than a significance verdict, so the claim is "no benefit larger than about 1.5 points," not "the effect is zero." The masking ablation used **ground-truth** polygons, so it is an oracle upper bound: a better segmenter cannot rescue a gain that is absent under perfect masks.
4. *A plain classifier outperforms the segment-then-classify cascade.* Evidence: paired per-seed difference +3.74 points (95% CI +3.04 to +4.44, paired t p = 0.002), with the correct caveat that at N = 205 an image-level McNemar test reaches 80% power only near 8.5–9 points, so we do not claim an image-level difference.
5. *In-distribution accuracy does not predict out-of-distribution behaviour here.* Evidence: on an independent clinical database the model collapses to 30.5–35.0% balanced accuracy and fails asymmetrically, under-grading 55 of 94 images against 2 over-graded.

**Why we think some individuals in TMLR's audience would be interested.** The failure mode is not exotic. It is what happens when a practitioner downloads a dataset that has already been augmented by the hosting platform and calls `train_test_split` on the file list. We believe that describes a substantial fraction of applied machine-learning work, including a non-trivial share of published clinical-AI papers. What we can contribute that the existing leakage literature does not is a *matched before-and-after on the same data with the same architectures*, plus a within-model decomposition that isolates memorisation from every other difference between the two conditions.

**On novelty.** There is none, and we do not claim any. There is no new architecture, loss, or algorithm here. We note TMLR's stated position that novelty is not a necessary criterion and that papers meeting the criteria should be accepted even where the contribution is modest, and we have written the paper to be judged on its evidence rather than on its ambition.

**Self-identified corrections.** During an internal re-audit we found and fixed several problems in our own reporting before submitting: we had promised Wilson confidence intervals and printed none; we had asserted categorically that no source photograph appeared in more than one fold, and a content-based check found 2 of 205 test images (1.0%) that violate it, one pair with conflicting labels; our external set of 319 images derives from only 175 distinct source photographs, so it is not 319 independent observations; and one reported Mann-Whitney p-value was the one-sided value, unlabelled. All four are now disclosed in the manuscript, with bounds. We mention this because the paper argues that the field under-scrutinises its own favourable results, and we would rather be held to that standard by ourselves than by a reviewer.

**Reproducibility.** Anonymised code, the exact split-reconstruction recipe, and the 205-filename test manifest are included as supplementary material, so every number in the paper can be recomputed from the released artefacts.

**Suggested action editor expertise.** We would benefit most from an action editor working on evaluation methodology, dataset quality and leakage, or empirical rigour in applied deep learning — rather than on medical imaging as a clinical domain. The contribution is methodological; burns are the setting, not the subject.

**Declarations.** This work is not under consideration at any other archival, peer-reviewed venue, reuses no text, figures or results from any published or accepted work of ours, and has been posted only as an arXiv preprint. The study used exclusively publicly available, de-identified images and an independent public research database; no new human-subjects data were collected and no institutional review board approval was required. The authors declare no competing interests. All authors hold active OpenReview profiles.

Sincerely,

**Authors** *(strip this block from any reviewer-visible copy)*
Ryan Altayeb (corresponding), Abdulrahman Alraddadi, Mohannad Alrehaili
Faculty of Computer and Information Systems, Islamic University of Madinah, Madinah, Saudi Arabia
altayeb.ray@gmail.com · ORCID 0009-0006-0031-9531
