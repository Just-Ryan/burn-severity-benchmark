# Cover letter — MELBA

*Upload to Scholastica as an additional file with the descriptor **"Cover Letter"** (.pdf or .docx).*

> **Do not delete the GenAI paragraph.** MELBA requires the cover letter to state *if and how*
> GenAI/LLMs were used. This is a hard, MELBA-specific requirement, not boilerplate.

---

Dear Editors of the Journal of Machine Learning for Biomedical Imaging,

We submit for your consideration "Deep learning for burn severity assessment: five evaluation
choices that changed our conclusions."

The paper reports a deployed two-stage burn-severity system — a YOLOv8x-seg localiser feeding a
masked Swin classifier, served through a mobile application — together with a leak-free benchmark
built to test whether that segmentation-first design is justified. Our answer is that it is not, on
accuracy grounds. What we think makes the paper worth your reviewers' time is not that finding but
what we hit on the way to it: **five separate times, a conventional protocol and an independent
second look gave different answers, and in every case the conventional protocol was the one we ran
first.** Table 1 sets all five side by side. The fifth we found in our own pipeline, after every
other number was final.

**1. A leakage artifact whose structure differs from the published cases.** Our original result was
that masking the image to the burn improved accuracy by 3.06 percentage points across 20 of 21
architectures. It was an artifact: the dataset augments each photograph into about 2.5 copies with
distinct file names, and a file-level split placed copies of one photograph in both folds. In the
masked classification set, 80.5 percent of test images shared a source photograph with training;
the separately partitioned unmasked set leaked none. Source-grouped, the effect is +0.55 points
(95 percent CI −0.37 to +1.47). Restricted to the eight architectures common to both analyses the
matched contrast is 2.07 → 0.55 rather than 3.06 → 0.55, and we rely on the smaller figure.

What we believe is unusual here is not the magnitude, which is smaller than the published
quantified-leakage studies, but that **the leak rate was confounded with the condition under
comparison** — 80.5 percent in one arm, zero in the other. Leakage therefore did not inflate a
score; it manufactured a comparative conclusion and a design recommendation, consistently across 20
of 21 architectures. The nearest precedent we found is confound-leakage (Hamdan et al., 2023), and
we scope our claim against it explicitly rather than claiming priority.

**2. Direct evidence that a three-seed protocol is actively misleading, not merely imprecise.**
Three seeds put the internal head-to-head margin at +3.74 points, 95 percent CI [+3.04, +4.44],
p = 0.002 — an interval about three times narrower than the data support — around an effect whose
true magnitude is smaller. The same three seeds put the external margin at +3.24, CI
[−3.83, +10.31], p = 0.19, licensing no claim at all, when that effect is in fact the most reliable
in the study (ten seeds: +2.79, CI [+1.09, +4.49], p = 0.005, ahead in 9 of 10 runs). One protocol
overstated the weaker result and concealed the stronger one simultaneously.

Because that comparison also involved a recipe change, we removed the confound: across all 120
three-seed subsets **of the same ten runs**, only 15 detect the external effect, estimates range
from +0.21 to +5.22 externally and −0.98 to +6.67 internally — some subsets place the pipeline
ahead — and the estimated standard deviation ranges from 0.00 to 3.25 percentage points.

**3. External validation that fails, reported as such.** On the independent BIP_US clinical
database the system collapses toward chance and under-grades severity, the dangerous direction. On
a second external set of 319 images, screened by perceptual hashing that removed 118
training-identical images, it under-graded 28.3 percent of
the images that could be under-graded against 19.3 percent internally. Because those 319 images
come from 175 source photographs, we report source-clustered bootstrap intervals alongside the
Wilson intervals; they are about a fifth wider, and they are the ones we rely on.

**4. A fairness probe that we could have published as a positive finding.** An exploratory
skin-tone analysis gave a large internal subgroup effect — median ITA 19.2 for errors against 38.4
for correct predictions, p = 0.0025, surviving Bonferroni correction across all 15 tests, in the
direction the fairness literature would predict. It does not replicate: the same test on the
external set, better powered at 139 images against 81, gives p = 0.35 with the effect reversed. We
report it in full, as a null with the subgroup signal disclosed, because deleting it would be
exactly the selective reporting the paper argues against.

**5. A leak we found in our own pipeline, and did not quietly fix.** While packaging the code for
release we discovered that our source-grouped split had been built for the classifiers and never
propagated to the segmentation models, which kept the collection's original split. As a result
179 of the 205 internal test images — 87.3 percent — sit in the segmentation models' training or
validation folds. We could have retrained quietly and said nothing. Instead we quantified it: the
standalone segmentation model scored 90.7 percent internally against 48.9 externally, a 41.8-point
gap that is the signature of being scored on one's own training data. Then we measured the leak by
removing it: we rebuilt both segmentation datasets on the classifiers' source-grouped split and
retrained both models under the original recipe, changing nothing but the partition. On the same
205 images the standalone model falls from 90.7 to **78.0 percent** — the leak was worth 12.7
percentage points. We also established, rather than assumed, what it does and does not touch. Segmentation mAP is clean (that split has zero
source overlap with training), the external set is clean (zero overlap), and Benchmark 1 uses
ground-truth masks throughout. What it inflates is the internal pipeline arm — the arm that
loses — so our headline internal margin is a lower bound, not an overstatement. We report it as
the fifth audit because a paper arguing that leakage is easy to introduce and hard to see should
say plainly when it introduced some and could not see it.

We are aware that this paper offers no new architecture, and we do not claim one. We submit it to
MELBA because your stated scope includes empirical comparisons, because your reviewers are asked
explicitly to assess reproducibility, and because this readership is the one that can act on the
result.

Every number in the paper can be recomputed. The repository at
https://github.com/Just-Ryan/burn-severity-benchmark contains the code, the trained weights, the
split definition, the raw per-image predictions behind every table and figure, and
`verify_paper_numbers.py`, a self-contained script that recomputes **136 published quantities** from
the committed raw data without a GPU, a dataset download, or model weights; all 136 pass. Two of
those checks exist specifically to catch us overstating our own results.

**Use of generative AI.** As required by MELBA's policy, we state how GenAI was used. The authors
used Anthropic Claude (Claude Code; Opus 4.8 and Opus 5 models) to organise the project materials,
to reproduce and check the reported results, to run the statistical, benchmarking and
external-validation analyses — including the leak-free re-runs, the ten-seed replication, the
perceptual-hash leakage check and the skin-tone probe — and to draft and edit the manuscript text.
All drafting was performed from author-supplied results and under author direction; the authors
verified every quantitative claim against the underlying result files, and the verification script
named above exists so that a reviewer can do the same. No text was accepted without author review,
and the tool was not used for unsupervised, de novo content creation. The research itself — the
system design, model training, dataset preparation and the mobile application — was conceived and
carried out by the authors, who take full responsibility for the content. This disclosure also
appears in the Acknowledgements section of the manuscript. We would rather state this fully and let
you judge it against your policy than describe it narrowly.

This manuscript is not under consideration elsewhere. An earlier and substantially shorter version
was submitted to the Turkish Journal of Electrical Engineering and Computer Sciences and was
declined at editorial screening, without external review, on 4 August 2026; we mention it for
completeness and are happy to supply the correspondence. The present version adds the ten-seed
replication, the 120-subset analysis, the skin-tone probe, the matched-architecture leakage
contrast, the source-clustered intervals and the segmentation-split audit, none of which were in
that submission. The work has
not been published previously. All three authors have approved this submission, declare no
conflicts of interest, and have not recently collaborated with any member of the MELBA editorial
board.

Thank you for your consideration.

Sincerely,

Ryan Altayeb, on behalf of Abdulrahman Alraddadi and Mohannad Alrehaili
Faculty of Computer and Information Systems, Islamic University of Madinah, Madinah, Saudi Arabia
altayeb.ray@gmail.com · ORCID 0009-0006-0031-9531

---

## Before you send — check these

- [ ] Confirm the rejection date above (4 August 2026) matches the TJEECS email.
- [ ] If you post an arXiv preprint before submitting, add one sentence saying so. MELBA encourages
      it. If you have not, say nothing — do not claim it in advance.
- [ ] Confirm the repository is public before you cite it as available.
