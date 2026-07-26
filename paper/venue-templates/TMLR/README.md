# TMLR — Transactions on Machine Learning Research

**Fallback rank: 2** (of 5). Pick this if you are willing to rewrite the paper in a machine-learning register.

> **DO NOT SUBMIT WHILE THE TÜBİTAK MANUSCRIPT IS UNDER REVIEW.** See `../../SUBMISSION_PLAYBOOK.md` §0.1. TMLR's dual-submission clause is unusually explicit and would catch you (§6 below).

**All facts below verified 2026-07-25 from jmlr.org/tmlr, the live OpenReview API, DOAJ and the ISSN Portal. Policies change — re-verify before submitting.**

---

## 1. Why TMLR

TMLR's acceptance criteria are, on paper, the best match in existence for this manuscript. Acceptance turns on two questions and nothing else:

> "Are the claims made in the submission supported by accurate, convincing and clear evidence?"
> "Would at least some individuals in TMLR's audience be interested in knowing the findings of this paper?"
> — https://jmlr.org/tmlr/acceptance-criteria.html and https://jmlr.org/tmlr/reviewer-guide.html (verified 2026-07-25)

And it explicitly disarms the objection that would sink this paper elsewhere:

> "novelty of the studied method is not a necessary criteria for acceptance"
> "We explicitly avoid these terms ("significant", "impactful", "novel"), and focus instead on the notion of "interest"."
> "a reviewer that is unsure as to whether a submission satisfies this criterion should assume that it does"
> — https://jmlr.org/tmlr/acceptance-criteria.html (verified 2026-07-25)

> "Papers should be accepted if they meet the criteria, even if the contribution or significance of the work is modest."
> — https://jmlr.org/tmlr/editorial-policies.html (verified 2026-07-25)

**UNVERIFIED:** no TMLR page uses the phrase "negative results". The closest in-scope wording is "accounts of applications of existing techniques that shed light on the strengths and weaknesses of the methods" (editorial-policies.html, § Scope). Do not tell an editor that TMLR "explicitly welcomes negative results" — say instead that your claims are evidence-supported, which is the criterion that actually exists.

## 2. The three risks you must weigh before choosing TMLR

**(a) Rejection is permanent and public.**
> "All submitted papers, including those accepted, rejected, withdrawn, or retracted, are made publicly accessible on OpenReview. An exception is made for desk-rejected papers, which are never made public."
> — https://jmlr.org/tmlr/faq.html (verified 2026-07-25)

A rejected TMLR submission stays on the internet forever, with its reviews. Author names stay hidden unless you choose to reveal them, and revealing them "will preclude them from submitting a revised version of the manuscript to TMLR" (editorial-policies.html). This is a real cost that MELBA, *Burns*, CMPB and TJMS do not have. **If you are not confident, submit to MELBA first.**

**(b) Scope is narrow and ML-methods-oriented.**
> "TMLR's objective is to publish original papers that contribute to the understanding of the computational and mathematical principles that enable intelligence through learning, be it in brains or in machines."
> — https://jmlr.org/tmlr/editorial-policies.html (verified 2026-07-25)

Desk rejection "for reasons including (but not limited to): being out of scope" is an explicit option for the action editor. A paper that reads as a clinical burn-assessment study will be desk-rejected. A paper that reads as *"a case study in how augmentation-before-split manufactures effects, and what an evaluation looks like that does not"* will not. §5 tells you how to make it the second thing.

**(c) The authorship quota.**
> "Authors are restricted in the number of submissions they can make per year, according to the Generalized Harmonic Quota Rule, with parameters N_1 = 2 and N_9 = 9."
> "Budget is spent for all submissions by an author, including those which are desk rejected."
> — https://jmlr.org/tmlr/editorial-policies.html (verified 2026-07-25)

Not a problem for you — you have never submitted to TMLR — but note that a desk rejection *costs* budget. Get the scope framing right the first time.

## 3. Facts table

| Item | Value | Source (verified 2026-07-25) |
|---|---|---|
| **Fee** | **None.** "TMLR imposes no fees or payments to authors, reviewers, action editors, or editors-in-chief." | jmlr.org/tmlr/editorial-policies.html |
| Licence | CC BY 4.0, authors retain copyright | jmlr.org/tmlr/author-guide.html |
| ISSN | 2835-8856 (electronic) | jmlr.org/tmlr/ |
| Indexing | **DOAJ: yes** (added 2025-01-15). **Scopus: yes** (source ID 21101278441, confirmed via ISSN Portal). **DBLP: yes**. **Google Scholar: partial and unreliable — TMLR says so itself.** *PubMed: listed by the ISSN Portal but not independently confirmed on an NLM page — treat as UNVERIFIED.* Reported CiteScore/SJR figures could not be read first-hand — **UNVERIFIED** | doaj.org/toc/2835-8856, portal.issn.org, dblp.org/db/journals/tmlr/, jmlr.org/tmlr/faq.html |
| Format | **LaTeX only.** `tmlr.sty`. "Submissions must be PDF files generated using the TMLR LaTeX stylefile and template." No Word template exists. (An explicit *ban* on Word is UNVERIFIED; the rule is stated positively) | jmlr.org/tmlr/author-guide.html |
| Template | https://github.com/JmlrOrg/tmlr-style-file — zip: https://github.com/JmlrOrg/tmlr-style-file/archive/refs/heads/main.zip | GitHub |
| Page limit | **None**, but 12 pages of main content is the pivotal threshold: ≤12 pages → reviews due in 2 weeks; >12 pages → 4 weeks and "longer timescales" | jmlr.org/tmlr/faq.html, reviewer-guide.html |
| Appendix | Allowed, after the references, inside the same PDF. "Looking at the Appendix is at the discretion of the reviewers." | jmlr.org/tmlr/author-guide.html |
| Supplementary | ZIP/PDF up to 100 MB, must be anonymised, visible to reviewers and the public | live OpenReview submission form |
| Blinding | **Double-blind AND open.** "TMLR uses an open-reviewing, double-blind process." Submission becomes public once the AE assigns reviewers | jmlr.org/tmlr/editorial-policies.html |
| Submission system | OpenReview, venue id `TMLR` — https://openreview.net/group?id=TMLR | jmlr.org/tmlr/submissions.html |
| Decision time | "the rolling review process aims to deliver a final decision approximately 9 weeks after submission" — with no guarantee, and longer over 12 pages | jmlr.org/tmlr/faq.html |
| Dual submission | Strict. See §6 | jmlr.org/tmlr/editorial-policies.html |
| arXiv preprints | **Allowed at any time**, anonymously or not, provided you do not link the named version from the submission | jmlr.org/tmlr/author-guide.html |
| Reciprocal reviewing | **Not required.** No obligation exists; reviewing is opt-in | jmlr.org/tmlr/faq.html |
| Seasonal pause | TMLR has paused new submissions over the winter holidays in past years (2 Dec 2025 – 5 Jan 2026). Check the news box on jmlr.org/tmlr before submitting in December | jmlr.org/tmlr/ |

**Certifications** (awarded automatically on consideration, not applied for): Outstanding, Featured, **Reproducibility** — "papers whose primary purpose is reproduction of other published work. Beyond simple verification, the paper must contribute significant added value through additional baselines, analysis, ablations, or insights" — Survey, Expert, and the new J2C (Journal-to-Conference) certification routing to NeurIPS/ICML/ICLR journal tracks. The Reproducibility certification is the one plausibly in reach for this paper. You cannot request it; do not mention it in the cover letter.

## 4. Blocking prerequisite: OpenReview profiles for ALL THREE authors

> "All authors must be listed on OpenReview, with active OpenReview profiles, at the time of submission and throughout the review process. There are no exceptions to this policy."
> — https://jmlr.org/tmlr/editorial-policies.html (verified 2026-07-25)

**This will bite you.** All three author emails on file are gmail addresses, and:

> "It can take up to 2 weeks for profiles using public email services to be activated. To activate immediately, please sign up with an email address that uses an educational or employing institution domain."
> — https://docs.openreview.net/getting-started/creating-an-openreview-profile/signing-up-for-openreview (verified 2026-07-25)

**Action:** get all three authors an `@iu.edu.sa` (or whatever your university domain is) address and register OpenReview profiles with it **now** — this costs nothing, does not count as submitting anywhere, and removes a two-week delay from the critical path. Each profile also needs a valid homepage: "a website that shows your name, affiliation, and email that you used to register", plus affiliations, conflicts of interest and publication history.

## 5. What to change in the manuscript for TMLR

This is the **largest rewrite of the five venues** — budget 3–5 weeks. You are converting a clinical-systems paper into an ML evaluation paper.

**Retitle.** The current title foregrounds the clinical application, which is exactly what triggers a scope desk-rejection. Use something like:

> *When augmentation precedes the split: a leak-free re-analysis of segmentation-first classification on a medical image benchmark*

**Restructure the argument.** Lead with the leakage finding, not the deployed system.

| Section | Current paper | TMLR version |
|---|---|---|
| Abstract/intro | Burns are a clinical problem; here is a system | File-level splits of pre-augmented datasets manufacture effects; here is a quantified case with a controlled before/after |
| §1 lead | WHO burn statistics | The leakage/reproducibility literature (Kapoor & Narayanan, Roberts et al., REFORMS) |
| Deployed system (§2.3) | A full subsection with the Flutter/Flask app | **Two sentences**, or move to an appendix. TMLR does not care about your app |
| Clinical background (§1) | ~2 pages | ~4 sentences of motivation, no epidemiology |
| Related work | Burn-assessment literature first | Leakage/evaluation-methodology literature first; burn literature as the domain instance |
| Leakage result (§3.2) | One short subsection | **The centrepiece**, with `fig_leakage.pdf` as Figure 1 and the within-model evidence (95.9% on the 417 leaked test images vs 82.2% on the 101 clean ones — one model, one test set, no confounds) promoted to a primary result |
| Masking null (§3.3) | Reported | Keep, framed as an effect-size-with-interval result |
| External validation | Clinical safety framing | Keep, framed as an in-distribution-vs-OOD generalisation result. The BIP_US under-grading finding is still interesting to this audience as a distribution-shift failure mode |
| Statistics | Good | **Expand.** This audience will read the statistics closely. Include the power analysis (80% McNemar power near 8.5–9 pp), the ddof = 1 correction, the exploratory-subgroup admission |

**Terminology to switch:** "severity classification" → keep, but add "3-class classification"; "leak-free split" → "source-grouped (group-wise) split"; "minimum detectable effect" → delete entirely, use the CI; "pipeline" → "cascade" or "segment-then-classify cascade" reads more naturally to this audience.

**Length target:** aim for **≤12 pages of main content** to get the 2-week review clock rather than the 4-week one. Push the deployed-system description, the efficiency table, the full architecture list and the per-class breakdowns into the appendix. The current 4,800-word body will fit.

**Add, because this audience expects it:**
- A reproducibility statement with the exact split-reconstruction recipe and the 205-filename manifest.
- Anonymised code as supplementary material (ZIP, ≤100 MB) — TMLR's supplementary is public, so it must be **anonymised**: strip author names, ORCIDs, the GitHub remote, and any `.git` directory.
- Explicit statement that the transformer/convnet subgroup analysis was **exploratory**.

## 6. The dual-submission clause — read it before you plan anything

> "Unlike many other journals, TMLR only accepts original contributions that don't reuse the authors' own prior work. In particular, we do not accept submissions that are expanded versions of conference papers. There should not be any reuse of written text, figures or results between the submitted paper and any paper which has been published, accepted for publication, or **submitted in parallel** at another archival, peer-reviewed venue."
> — https://jmlr.org/tmlr/editorial-policies.html (verified 2026-07-25, emphasis added)

**What this means for you:**
- While TÜBİTAK holds the paper, a TMLR submission would be a direct policy violation. Not ambiguous.
- After a TÜBİTAK **rejection**, the paper is no longer "submitted in parallel" and has not been published, so TMLR is open to you.
- Your **graduation project report** is fine if it is non-archival: "It is acceptable for a submission to overlap with the author's previous work if it was shared at venues or tracks that are publicly declared, in writing, to be non-archival". A thesis is explicitly treated like a preprint. If your university publishes theses in an archival, peer-reviewed repository, check.
- **arXiv is fine and encouraged** — post the preprint after a TÜBİTAK rejection, using `\usepackage[preprint]{tmlr}`, then submit. Just do not link the named arXiv version from the OpenReview submission.

## 7. Ordered submission steps

Do these in order. Steps 1–3 can be done today; steps 4 onward only after TÜBİTAK is clear.

1. **[Do today] Register OpenReview profiles for all three authors** at https://openreview.net/signup, using institutional email addresses. Complete each profile: full name, affiliation (Faculty of Computer and Information Systems, Islamic University of Madinah), ORCID, homepage URL, publication history, conflicts of interest. Wait for activation.
2. **[Do today] Download the style files:** https://github.com/JmlrOrg/tmlr-style-file/archive/refs/heads/main.zip → you get `tmlr.sty`, `tmlr.bst`, `fancyhdr.sty`, `main.tex`, `math_commands.tex`.
3. **[Do today] Port the manuscript** to `\documentclass[10pt]{article}` + `\usepackage{tmlr}`. **Do not alter the stylefile:** "Any changes to the stylefile or template that alters the formatting, font, or layout of the manuscript may result in rejection without review." (submissions.html). Convert the bibliography to `tmlr.bst` (author–year, not the numeric TÜBİTAK style).
4. **[After TÜBİTAK is clear] Rewrite** per §5. Get the main body to ≤12 pages.
5. **[After TÜBİTAK is clear] Post the arXiv preprint** (`cs.CV`, cross-list `eess.IV`) using `\usepackage[preprint]{tmlr}`.
6. **Anonymise the PDF.** Author block blank (the stylefile handles this in submission mode), no acknowledgements, no repo URL, no self-identifying phrasing, and **check the PDF metadata** for your machine username.
7. **Build the anonymised supplementary ZIP** (code + the 205-filename manifest + the results JSONs). Strip `.git`, author names, ORCIDs, and the GitHub remote. ≤100 MB.
8. **Log in to https://openreview.net/group?id=TMLR** and start a new submission. The form asks for exactly these fields (confirmed live against the OpenReview API on 2026-07-25):
   - `title`
   - `abstract`
   - `authors` / `authorids` — all three, matched to their activated profiles
   - `pdf` — the anonymised manuscript
   - `submission_length` — a three-way radio. Choose **"Regular submission (no more than 12 pages of main content)"**
   - `competing_interests` — state "The authors declare no competing interests."
   - `human_subjects_reporting` — state that the study used only publicly available, de-identified images and an independent public research database, that no new human-subjects data were collected, and that IRB approval was therefore not required
   - `supplementary_material` (optional) — the anonymised ZIP
   - `previous_TMLR_submission_url` — leave blank (this is your first)
9. **Submit.** Then watch for the email asking you to **recommend potential action editors**: "You will receive an email once your submission has been made, asking you to recommend potential Action Editors that would be appropriate for your submission." (submissions.html). Suggest AEs who work on evaluation methodology, dataset quality, or medical imaging — not on burn care.
10. **Within ~1 week** an action editor is assigned. If they do not desk-reject, the paper becomes public and at least three reviewers are assigned.
11. **Respond to reviews within 2 weeks** of the third review landing (FAQ recommendation). Use the response structure in `../../SUBMISSION_PLAYBOOK.md` §6, and lead with the self-identified corrections in §6.4.
12. **On acceptance:** switch to `\usepackage[accepted]{tmlr}`, add the link to the review page, and submit the camera-ready. **Camera-ready is final** — "changes are not allowed" afterwards except at EiC discretion. Proof it carefully. Optionally add a video presentation or code link.

## 8. Timeline

| Stage | Stated duration |
|---|---|
| Action editor assigned | within 1 week |
| Reviews due | 2 weeks (≤12 pp) / 4 weeks (>12 pp) after assignment |
| Discussion phase | 2–4 weeks |
| Author response | recommended within 2 weeks of the 3rd review |
| Reviewer final recommendations | ≥2 weeks after all 3 reviews are public |
| **Total to decision** | **~9 weeks target, not guaranteed** |
| Publication | immediate on completion (continuous publication) |

## 9. Files in this folder

- `cover_letter.md` — TMLR has no cover-letter field in the submission form. Use this text as the basis for your **action-editor recommendation email** and as a note in `competing_interests`/correspondence if an AE asks about scope. Keep it; do not paste it into the abstract.
- `checklist.md` — tick before submitting.
