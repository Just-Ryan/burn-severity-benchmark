# CMPB — pre-submission checklist

Verified 2026-07-25 in a live browser session against the Guide for Authors, Aims and Scope, Open Access Options and Insights pages. Re-verify before submitting.

## Gate 0 — allowed to submit?

- [ ] TÜBİTAK has **rejected** the paper, or it is **formally withdrawn with written confirmation**.
- [ ] Under consideration nowhere else.
- [ ] Verification protocol run (`../../SUBMISSION_PLAYBOOK.md` §7.3) — I typed the URL rather than following an email link.
- [ ] **I am submitting to CMPB, not to "CMPB Update."** Update is fully gold OA with an unavoidable APC of USD 2,390 / 1,580 and has **no free route**.

## Gate 1 — the hard limits (this is where CMPB submissions die)

- [ ] Main text is **≤ 3,500 words**, excluding the abstract. *(Current draft ~4,800 — must be cut ~1,300.)*
- [ ] References **≤ 50**. *(Current 51 — cut at least one.)*
- [ ] Abstract is **≤ 350 words** and **STRUCTURED** with exactly these four headings:
  - [ ] Background and Objective
  - [ ] Methods
  - [ ] Results
  - [ ] Conclusions
- [ ] **The Results heading of the abstract reports precision, sensitivity and specificity values** — a hard journal-specific requirement the current paper does not satisfy. These have been computed and inserted.
- [ ] No references or abbreviations in the abstract.
- [ ] Keywords: **3 to 6**, none using "and"/"of".
- [ ] Sections are Introduction / Methods / Results / Discussion / Acknowledgements, numbered 1, 1.1, 1.1.1.

## Gate 2 — format

- [ ] Source file is **.doc/.docx or .tex** — **PDF is not an acceptable source file**.
- [ ] Word file is **single-column** (double-column permitted only for LaTeX).
- [ ] **Double-spaced with wide margins.**
- [ ] References numbered in **square brackets** in order of appearance. *(Formatting is free-form at submission; style is applied at proof.)*
- [ ] **Separate title page** prepared: title (**not all capitals**), all author names and full addresses, corresponding author's full postal address, email **and telephone**.
- [ ] Manuscript is **NOT anonymised** — review is single-anonymised.
- [ ] **Exactly one corresponding author** (Ryan Altayeb). "Submissions with multiple corresponding authors are no longer accepted."

## Gate 3 — the rewrite

- [ ] Framing leads with the **method and released software** (source-grouped splitting + perceptual-hash contamination screening), not with "we compared architectures."
- [ ] Deployed system compressed to a paragraph plus the figure.
- [ ] Efficiency results and the architecture list moved to supplementary.
- [ ] Related Work compressed from five thematic paragraphs to three.
- [ ] Discussion tightened — it currently restates the Results.
- [ ] **Statistics, leakage evidence and limitations NOT cut.** Those are the paper.
- [ ] All open items in `../../SUBMISSION_PLAYBOOK.md` §1.5 fixed.

## Gate 4 — declarations

- [ ] **CRediT statement** — mandatory. Matches `../../SUBMISSION/SUBMISSION_METADATA.md` word for word.
- [ ] **Competing interests** — declarations tool completed; "I have nothing to declare".
- [ ] **Funding** — "This research did not receive any specific grant from funding agencies in the public, commercial, or not-for-profit sectors."
- [ ] **Ethics — active confirmation prepared.** CMPB "requires authors to confirm at submission if their research needs an Ethics statement"; if not needed, "they must state why." My sentence is written and states why.
- [ ] **Data availability statement** — encouraged, not mandatory. Included anyway, with the real repository link and DOI.
- [ ] Declarations placed under "Acknowledgements including declarations".
- [ ] Declarations tool output saved as **.doc/.docx** for upload.

## Gate 5 — the GenAI declaration

- [ ] In a **new section immediately before the reference list**.
- [ ] Titled exactly: **"Declaration of generative AI and AI-assisted technologies in the manuscript preparation process."**
- [ ] Follows Elsevier's template and ends with "…take(s) full responsibility for the content of the published article."
- [ ] **Not shortened.**
- [ ] Covers manuscript preparation and analysis assistance only — the segmentation/classification models are research method and are correctly excluded ("This policy does not prevent the use of AI tools in formal research design or research methods").
- [ ] No AI-generated figures (or, if any, disclosed in the caption as well).

## Gate 6 — universal

- [ ] `../../SUBMISSION_PLAYBOOK.md` §2 worked through in full.
- [ ] Repo public and clean (single-anonymised review makes this safe) — release hygiene checklist in §1.3 step 4 done.
- [ ] Preprint declaration accurate.
- [ ] iThenticate similarity checked.
- [ ] BIP_US usage permission confirmed in writing.

## Gate 7 — submitting

- [ ] Went to **https://submit.elsevier.com/CMPB** by typing it.
- [ ] **Did NOT use editorialmanager.com/CMPB** — it currently reads "Site under development. Do not use for live manuscript submission."
- [ ] Clicked **"Start a submission"**.
- [ ] Have ready: submission files · all author and co-author details including emails and affiliations · funder details.
- [ ] Uploaded: manuscript · title page · declarations tool output (.doc/.docx) · figures · optional highlights (3–5 bullets, ≤85 chars) · **cover letter (mandatory)**.
- [ ] Cover letter states all four required things: why it suits CMPB · what is known · what the study adds · that it is unpublished.
- [ ] Reviewed the system-built single PDF before final submission.
- [ ] Manuscript number recorded; noted that post-submission management moves to Editorial Manager.

## Gate 8 — after

- [ ] Diarised **40 days** (Elsevier's published "submission to first decision"). Do not chase before ~10 weeks.
- [ ] Revision response follows `../../SUBMISSION_PLAYBOOK.md` §6, leading with the self-identified corrections in §6.4.
- [ ] Noted: **one appeal only, and the appeal decision is final.** Do not spend it lightly.
- [ ] **On acceptance: DECLINE gold open access.** Choose the subscription route. USD 3,180 is optional. If a screen asks for payment details, stop.
- [ ] After the 12-month embargo, accepted manuscript self-archived for free green OA.
