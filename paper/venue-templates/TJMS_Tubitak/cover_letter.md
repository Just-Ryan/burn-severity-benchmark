# Turkish Journal of Medical Sciences — cover letter

> Paste into the Editorial Manager "Comments" box, or upload as a separate file if a cover-letter slot exists.
> Replace `[DATE]`. Check the current Editor-in-Chief at https://journals.tubitak.gov.tr/medical/ — do not guess.
> **If TJEECS rejected this paper, say so.** Same publisher, same infrastructure; disclosing it voluntarily costs nothing and looks far better than being discovered. The paragraph is included below — delete it only if it does not apply.

---

[DATE]

To the Editor-in-Chief
*Turkish Journal of Medical Sciences*
TÜBİTAK ULAKBİM

Dear Editor,

We submit for your consideration our manuscript, **"A comparative study of deep learning approaches for automated burn injury segmentation and severity classification,"** as a Research Article.

**The clinical question.** Burn depth determines treatment: whether a wound heals with conservative care or requires surgical intervention and referral to a burn centre. Agreement between experienced burn surgeons on depth is only about 60 to 80 percent, and it is degraded by lighting, wound evolution, blistering and skin pigmentation. Automated assessment aids are therefore attractive, particularly where specialists are absent — and smartphone-based burn assessment tools are increasingly proposed for exactly those settings.

**What we found, and why we think it matters to your readership.** We built such a tool — a deep learning system that localises a burn in a photograph and grades its severity, served through a smartphone application — and then tested whether it is safe to use. It is not.

On our own held-out test data the system reached 82.6 percent accuracy, squarely within the range that published burn deep-learning studies routinely report. On an independent clinical database of 94 burn photographs from the Biomedical Image Processing Group at the University of Seville, **the same system under-estimated burn depth in 55 of 94 images against only 2 over-estimates, and classified approximately half of the full-thickness burns as first degree.** Balanced accuracy fell to 30.5–35.0 percent.

The direction of that failure is the clinically dangerous one. A tool that over-calls severity generates an unnecessary referral. A tool that under-calls it directs a deep dermal or full-thickness burn toward conservative management and delays specialist assessment. Ours does the second, while appearing accurate on the internal metrics that most published studies report.

**Why the internal number was misleading.** Auditing our own favourable results, we found that our original positive finding was an artifact of how the image dataset had been divided. The public collection we trained on, like many hosted image datasets, is distributed pre-augmented: each source photograph exists as roughly 2.5 near-duplicate files under different names. Dividing those files at random placed copies of the same photograph in both the training and the test set. In one arm of our experiment this affected 80.5 percent of test images, and it manufactured an apparent 3.06-percentage-point improvement across 20 of 21 network architectures. The clearest evidence involves a single model on a single test set: it scored 95.9 percent on the test images whose source photograph had appeared in training and 82.2 percent on those whose had not. After dividing the data by source photograph rather than by file, the apparent improvement fell to 0.55 percentage points with a confidence interval spanning zero.

We report this because we believe it is a live problem in the medical AI literature. A recent five-year systematic review of convolutional networks applied to burn photographs found that most studies report strong single-dataset accuracies, very few validate on an independent source, and dataset handling is often under-described. Our study offers a quantified, mechanistically explained example of how such a number is produced without anyone acting dishonestly, together with a simple procedural rule that prevents it.

**Fit with the journal.** The *Turkish Journal of Medical Sciences* accepts original manuscripts in all fields of medicine and related health sciences. Our submission is a clinical evaluation study: it asks whether an automated diagnostic aid performs adequately on real patient images, and it answers with a quantified safety finding. We have deliberately kept the technical machine-learning detail to the minimum needed for reproducibility, and placed the clinical implications and limitations at the centre of the Discussion.

**Ethics.** This study involved no human participants and collected no new patient data. It is a secondary analysis of publicly available, de-identified burn photographs released under a Creative Commons Attribution 4.0 licence, together with an independent research database provided for research use by the University of Seville. No experimental investigation was conducted with humans, and institutional review board approval was therefore not required. [**If you have obtained a letter from your faculty, add:** A letter from the ethics committee of the Faculty of Computer and Information Systems, Islamic University of Madinah, confirming that approval was not required, is available on request.]

**Self-identified corrections.** During an internal re-audit we identified and corrected several shortcomings in our own reporting: confidence intervals we had promised but not printed; a categorical claim about data independence that a content-based check falsified for 2 of 205 test images; an external validation set of 319 images that derives from only 175 distinct source photographs and is therefore not 319 independent observations; and an unlabelled one-sided p-value. All are now disclosed in the manuscript with quantified bounds. We mention this because a study arguing that the field under-scrutinises its own favourable results should first be held to that standard by its own authors.

[**DELETE IF NOT APPLICABLE:** In the interest of full transparency, we note that an earlier version of this manuscript was submitted to the *Turkish Journal of Electrical Engineering and Computer Sciences* and was not accepted. We have withdrawn it there, revised it substantially in response to the referees' comments, and reframed it for a clinical readership. No version is under consideration at any other journal.]

**Declarations.** This manuscript is original and is not under consideration elsewhere. It [has not been posted to a preprint server / is available as a preprint at arXiv:XXXXX — **delete whichever does not apply**]. The authors declare no conflict of interest and received no funding. All authors have provided ORCID iDs, have contributed according to the CRediT roles entered at submission, and have read and approved this submission. Our use of generative AI in preparing the manuscript is declared in full, including the model version and the exact prompt, in the dedicated section of the manuscript.

Thank you for considering our work.

Sincerely,

**Ryan Altayeb**, on behalf of all authors
Corresponding author — altayeb.ray@gmail.com — ORCID 0009-0006-0031-9531
Faculty of Computer and Information Systems, Islamic University of Madinah, Madinah, Saudi Arabia

Co-authors: Abdulrahman Alraddadi (ORCID 0009-0000-2325-5063), Mohannad Alrehaili (ORCID 0009-0008-2491-185X)
