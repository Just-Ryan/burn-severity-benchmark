# Burns — pre-submission checklist

Verified 2026-07-25 against the live Guide for Authors, Open Access Options and Insights pages. Re-verify before submitting.

## Gate 0 — allowed to submit?

- [ ] TÜBİTAK has **rejected** the paper, or it is **formally withdrawn with written confirmation**.
- [ ] The paper is under consideration nowhere else.
- [ ] Journal verification protocol run (`../../SUBMISSION_PLAYBOOK.md` §7.3) — I typed `sciencedirect.com` myself rather than following an email link.

## Gate 1 — the rewrite (§6 of README)

- [ ] Lead result is now the **clinical safety finding** (55 of 94 under-graded; half of full-thickness burns called first degree), not the classifier-vs-pipeline comparison.
- [ ] Architecture benchmarking compressed to one table and one paragraph; the rest moved to supplementary.
- [ ] Clinical depth vocabulary added alongside degree terms (superficial / superficial-partial / deep-partial / full thickness).
- [ ] "Under-graded" reframed as **under-triage** with a stated clinical consequence (delayed referral to a burn centre).
- [ ] Discussion leads with clinical implications, not methodology.
- [ ] Efficiency table cut or moved to supplementary.
- [ ] **Skin-tone / pigmentation limitation stated prominently.** Every reviewer will raise it.
- [ ] "Data leakage" explained in one plain sentence at first use; jargon removed ("oracle upper bound", "architecture-seed pairs", "MDE").
- [ ] Fu's five-year systematic review of burn CNN papers is used as the bridge to this readership.

## Gate 2 — hard formatting rules

- [ ] **Abstract ≤ 250 words, unstructured.** (Current draft is 321 — must be cut.)
- [ ] Keywords: **1 to 6**.
- [ ] References: numeric, **square brackets**, in order of appearance, **abbreviated** journal names (LTWA) — *opposite of TÜBİTAK's full-name rule*. >6 authors → first 6 + "et al." Shortened last page numbers. DOIs included.
- [ ] Source file is **.doc/.docx or .tex** — **a PDF is not an acceptable source file**.
- [ ] Word file is **single-column** (double-column is permitted only for LaTeX).
- [ ] Title is **not all capitals**.
- [ ] Manuscript is **NOT anonymised** — review is single-anonymised.
- [ ] Length: no published limit — checked against 2–3 recent *Burns* research articles for a sane target.

## Gate 3 — the mandatory files

- [ ] **Disclosures form completed and uploaded** — https://legacyfileshare.elsevier.com/gfa/journal-specific/burns-declarations.docx — **"This is mandatory for the submission process."** All six sections filled, inapplicable ones marked "Not applicable":
  - [ ] Funding — none
  - [ ] Clinical Trial Number — not applicable
  - [ ] Ethics Approval — public de-identified images + independent public research database; no new human-subjects data; IRB approval not required
  - [ ] Use of Generative AI — completed
  - [ ] Informed Consent — not applicable
  - [ ] CRediT Author Statement — matches `../../SUBMISSION/SUBMISSION_METADATA.md` exactly
- [ ] **Highlights file** — 3–5 bullets, **each ≤85 characters including spaces** (count them), separate editable file with `highlights` in the filename.
- [ ] **Title page** — title, all author names and full addresses, corresponding author's full postal address, email and telephone.
- [ ] Figures as separate files (EPS/PDF for vector; TIFF ≥300 dpi for raster; ≥500 dpi for combination art).
- [ ] Optional: graphical abstract, 531 × 1328 px (h × w) or proportionally larger, readable at 5 × 13 cm.
- [ ] Cover letter (`cover_letter.md`) — bracketed placeholders replaced, editor name checked against the live editorial board page.

## Gate 4 — the GenAI declaration

- [ ] Moved **into the manuscript**, in a new section **immediately before the reference list**.
- [ ] Section titled exactly: **"Declaration of generative AI and AI-assisted technologies in the manuscript preparation process."**
- [ ] Follows Elsevier's template and **ends with** "…reviewed and edited the content as needed and take(s) full responsibility for the content of the published article."
- [ ] **Not shortened.** Under-declaring is far worse than declaring a lot.
- [ ] Covers writing/analysis assistance only — the segmentation and classification models are research method and are correctly excluded ("This policy does not prevent the use of AI tools in formal research design or research methods").
- [ ] Also completed in the **"Use of Generative AI" field on the disclosures form** — both are required.
- [ ] No AI-generated figures; if any figure were model-drawn, disclosed in its caption too.

## Gate 5 — universal items

- [ ] `../../SUBMISSION_PLAYBOOK.md` §2 worked through in full (ORCIDs, CRediT, declarations, figures, integrity).
- [ ] All open items in §1.5 fixed (ddof = 1, the "all three seeds" claim, the 226-vs-118 chain, Table 3's "not tested", chance-level wording, fixed-localiser caveat, seed-42 caption).
- [ ] iThenticate similarity checked via the university library.
- [ ] BIP_US usage permission confirmed in writing — **especially** if any figure reproduces a BIP_US image.
- [ ] Preprint declaration accurate (see `../../SUBMISSION_PLAYBOOK.md` §0.2).

## Gate 6 — submitting

- [ ] Went to **https://www.editorialmanager.com/jbur** by typing it, not by clicking a link.
- [ ] Article type chosen: "Original Paper" or "Original Research".
- [ ] Files uploaded: manuscript · title page · **disclosures form** · **highlights** · figures · cover letter · optional graphical abstract.
- [ ] Declarations tool completed in the wizard (competing interests → "I have nothing to declare"; funding → none).
- [ ] **Built PDF reviewed before approving** — approval is irreversible.
- [ ] Manuscript number recorded.
- [ ] Diarised: do not chase before 3 months ("submission to decision after review" is 63 days, which excludes desk rejections).

## Gate 7 — on decision

- [ ] Revision returned **within three months**.
- [ ] Response letter follows `../../SUBMISSION_PLAYBOOK.md` §6, leading with the self-identified corrections in §6.4.
- [ ] **On acceptance: DECLINE gold open access.** Choose the subscription route. The APC is USD 3,570 and is entirely optional. If a screen asks for payment details, stop.
- [ ] Proof returned within two days.
- [ ] After the 12-month embargo, accepted manuscript self-archived for free green OA.
