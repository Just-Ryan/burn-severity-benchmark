# MELBA — Journal of Machine Learning for Biomedical Imaging

**Fallback rank: 1** (of 5). Smallest rewrite, best topical fit, essentially free — **but read §2 before you commit, because the indexing situation is not what the project audit assumed.**

> **DO NOT SUBMIT WHILE THE TÜBİTAK MANUSCRIPT IS UNDER REVIEW.** MELBA is explicit: "simultaneous submission to other journals, conferences, or MELBA of the same or substantially similar articles is not permitted" (https://www.melba-journal.org/about.html, verified 2026-07-25).

**All facts below verified 2026-07-25** from melba-journal.org, the melba-journal/submission GitHub repo, the Scholastica portal, the DOAJ API, OpenAlex, the NLM Catalog and the ISSN Portal. Site was live and current (latest article 2026-07-22).

---

## 1. Why MELBA

Exact topical intersection: machine learning **and** biomedical imaging.

> "in the broad field that bridges machine learning and biomedical imaging"
> "invites the submission of previously unpublished journal-length papers"
> — https://www.melba-journal.org/about.html (verified 2026-07-25)

Listed in-scope topics include **"empirical comparisons"** and "new problem formulations / publicly available datasets with a baseline" — your paper is an empirical comparison with a leakage case study attached, so it sits squarely inside the stated scope without any reframing gymnastics.

Reviewers are explicitly asked to score reproducibility: *"Reproducibility: … Is the code and/or data shared?"* (https://www.melba-journal.org/for_reviewers.html). That is a rubric this paper scores well on.

Community-run, respected in the MICCAI/MIDL world, monthly issues, Crossref member (DOI prefix 10.59275).

## 2. ⚠️ The indexing problem — decide with your eyes open

**The project audit (`INDEPENDENT_AUDIT_2026-07.md` §9.1) states MELBA is in DOAJ. It is not.** Verified 2026-07-25:

| Index | Status | Evidence |
|---|---|---|
| **DOAJ** | **NOT listed** | DOAJ API returns `total: 0` for `issn:2766-905X` and for a title search (API confirmed working against a control journal). OpenAlex agrees: `is_in_doaj: false` |
| **PubMed** | **Selected citations only — NOT MEDLINE-indexed** | [NLM Catalog, NLM ID 9918400085306676](https://www.ncbi.nlm.nih.gov/nlmcatalog/490569): "In: PubMed: Selected citations only" and "Not currently indexed for MEDLINE. Citations are for articles where the manuscript was deposited in PubMed Central." Only **12** MELBA items are in PubMed, against 233 works in OpenAlex |
| **Scopus** | **UNVERIFIED** | Scopus source list, scopus.com and SCImago were all bot-blocked. No SCImago or Scopus record surfaced in searching. MELBA makes no Scopus claim |
| **Web of Science** | **UNVERIFIED** | Clarivate's Master Journal List is JS-gated. No ESCI/WoS record found. MELBA makes no WoS claim |
| **ISSN** | **2766-905X** (electronic), confirmed | [ISSN Portal](https://portal.issn.org/resource/ISSN/2766-905X), record type "Confirmed" |

**MELBA's own website makes no indexing claims at all** — every page was searched for "Scopus / DOAJ / Web of Science / PubMed / indexed / MEDLINE / Clarivate" and returned zero hits. That is honest of them, and it is also a signal.

**What to do with this:**

- MELBA is **not predatory**. It is community-run, transparent about its process, a Crossref member, hosts the MIDL and MICCAI-workshop special issues, and publishes work by identifiable researchers. It fails a mechanical DOAJ-plus-Scopus checklist while being obviously legitimate — which is precisely why `../../SUBMISSION_PLAYBOOK.md` §7.3 is a screening tool, not a verdict. **Use judgment, not just the checklist.**
- But **if your degree, scholarship, or CV requires a Scopus- or WoS-indexed publication, MELBA may not satisfy it.** Ask your faculty *before* you spend six weeks on a submission. This is a five-minute email that can save a year.
- **Before submitting, re-run the check yourself:** search https://www.scopus.com/sources for "Journal of Machine Learning for Biomedical Imaging" and 2766-905X, and https://mjl.clarivate.com for the same. Both are gated to automated tools but work fine in a browser. Indexing status changes; ours is a July 2026 snapshot with two genuine unknowns in it.

## 3. Facts table

| Item | Value | Verified |
|---|---|---|
| **Publication fee** | **None.** "There are no publication charges with MELBA: you wrote it, the community reviewed it, we publish it" | 2026-07-25 |
| **Submission fee** | **USD 10**, charged by Scholastica, not by MELBA: "The Scholastica submission system requires a $10 charge during initial submission." MELBA adds "However, we are actively working on removing this as well." Scholastica's own rate page confirms $10 per submission | 2026-07-25 |
| Licence | **CC BY 4.0**, authors retain copyright | 2026-07-25 |
| ISSN | 2766-905X (electronic) | 2026-07-25 |
| **Blinding** | **SINGLE-blind.** "the reviewers are anonymous, but the authors are known to the reviewers" · "The identity of reviewers will be hidden from authors." **Author names and affiliations go ON the submitted PDF.** Reviews are not published | 2026-07-25 |
| Review flow | EiC screen → Associate Editor → 3 reviewers. Decisions: Accept, Major Revisions, Reject | 2026-07-25 |
| **Format** | **LaTeX only, mandatory template.** "Submissions must be in LaTeX using the provided template." · **"using any other template will result in a desk reject"** | 2026-07-25 |
| Template | https://github.com/melba-journal/submission — LaTeX files at https://github.com/melba-journal/submission/tree/master/latex | 2026-07-25 |
| ⚠️ Template gotcha | It is a **class file, `melba.cls`** (`\documentclass{melba}`, v2.03, 2025/03/17), *not* a style file. The repo README says "requiring only the melba.sty style file" and links `latex/melba.sty` — **that file does not exist and the link is broken.** Use `melba.cls`. Raw: https://raw.githubusercontent.com/melba-journal/submission/master/latex/melba.cls | 2026-07-25 |
| Class options | default (= submission, line numbers on), `arxiv`, `accepted`, `specialissue`. "During submission, authors should not modify it." | 2026-07-25 |
| Word / .docx | **Not allowed by MELBA** (LaTeX is required), even though Scholastica's generic uploader accepts .docx/.pdf | 2026-07-25 |
| Length | "Regular research manuscripts are expected to be approximately **20 pages** long, though MELBA does not enforce a strict page limit." | 2026-07-25 |
| Word / figure / abstract limits | **None stated anywhere** — site, Scholastica page, README and `melba.cls` were all searched. Treat as "not specified", **not** "unlimited" | 2026-07-25 |
| Submission system | **Scholastica.** Link on the MELBA site (note plain http): `http://app.scholasticahq.com/submissions/melba/new`, which redirects to a login. Journal portal: https://melba.scholasticahq.com/ | 2026-07-25 |
| **Time to first decision** | **UNVERIFIED.** No turnaround figure is published for regular submissions. The only stated numbers ("4-6 weeks") are from 2023 **special-issue** blog posts and must not be quoted as current general policy | 2026-07-25 |
| Cadence | "MELBA publishes monthly issues as well as special issues." | 2026-07-25 |
| Preprints | **Explicitly allowed, and encouraged.** "Prior submissions of articles on arXiv are permitted." · "Preprints can be shared at any time." The Scholastica page says arXiv preprints are "encouraged" | 2026-07-25 |
| Simultaneous submission | **Forbidden** — see the warning at the top of this file | 2026-07-25 |
| Conference extensions | Allowed with "significant extensions", overlap **< 50%**, and must be declared in the cover letter | 2026-07-25 |

**Special issues** (see https://github.com/melba-journal/submission#special-issues): MIDL 2020, IPMI 2021, MICCAI workshops (UNSURE, DART, PIPPI, MLCN, iMIMIC, LNQ challenge), Generative Models, Image Registration, **FAIMI (fairness)**, MELBA–BVM 2025, UNSURE 2025. Check the current list for an open call — a special issue on evaluation, fairness or uncertainty would be a strong fit and typically has a stated deadline and faster turnaround.

There is also a separate **Resource track** for datasets and open-source tools, with its own prescribed structure (https://www.melba-journal.org/resource.html). Your paper is a regular research submission, not a Resource paper — but the released benchmark could be a *second*, later paper.

**MIDL journal-to-conference track:** "Authors of recently published papers at MELBA may be eligible to present their work at MIDL 2025." The banner still says MIDL 2025 and is likely stale; **current-year eligibility is UNVERIFIED.**

## 4. Required statements — MELBA's are unusual, read carefully

| Requirement | Status | Wording |
|---|---|---|
| **Data Availability Statement** | **MANDATORY** | "Authors submitting articles to MELBA are required to include a Data Availability Statement in their manuscripts." Sharing itself is voluntary — "we adopt a voluntary data sharing policy" — but non-sharers must give "a well-justified explanation" |
| **Ethics statement** | **MANDATORY** | "a statement confirming the approval by the appropriate institutional review boards **or a statement of why such approval was not required**" — the second clause is exactly your case, and MELBA writes it into the requirement |
| **Conflict of interest** | **MANDATORY, two layers** | "Authors must disclose any financial, organizational, commercial, or personal conflicts of interest"; "all authors are required to fill out an online conflict of interest declaration upon submission"; **plus** "Authors must name all editors that have recently collaborated with the authors" |
| **Funding / acknowledgements** | **MANDATORY** | "The authors must acknowledge any funding sources used for the conduct of the research" |
| **GenAI disclosure** | **MANDATORY, in two places** | "The use of computational tools such as large language models (LLMs) or generative AI (GenAI) in general needs to be disclosed in an **Acknowledgement section**"; and "Authors are required to state in the **cover letter** if and how GenAI or LLMs were used". "LLMs are not permitted as co-authors." Permitted "to help polish text or draft initial bullet-points, but not for unsupervised, de novo content creation" |
| **CRediT** | **NOT required** | The word "CRediT" appears nowhere. A narrative policy applies instead: "Authors listed on a MELBA submission are expected to have made a meaningful contribution" |
| **ORCID** | **NOT required** | Supported via `\orcid{}` in the template and an optional Scholastica field. Supply them anyway |
| Code sharing | **Encouraged, not required** | "MELBA encourages authors to share and support their code and data, with an emphasis on replicability." The cover-letter template marks the code line "[OPTIONAL, BUT ENCOURAGED]" |

⚠️ **The GenAI clause needs thought.** MELBA permits GenAI "to help polish text or draft initial bullet-points, **but not for unsupervised, de novo content creation.**" Your declaration says Claude was used to "draft and edit the manuscript." That is a broader claim than "polish text."

**Do not solve this by shrinking the declaration.** Solve it by describing accurately what happened: the AI drafted text *from author-supplied results, under author direction, and every claim was reviewed and verified against source files by the authors*, which is supervised drafting rather than unsupervised de novo creation. State that explicitly in both the Acknowledgement section and the cover letter. If an editor still judges it out of policy, you want to have found that out honestly, before publication rather than after. **Accuracy over convenience — this is the same standard the paper argues for.**

## 5. Two errors on MELBA's own site — know them before you get confused

1. **`melba.sty` vs `melba.cls`** — the README links a `.sty` that does not exist. Use `\documentclass{melba}` with `latex/melba.cls`.
2. **Post-acceptance hosting** — `for_authors.html` still says "the actual PDF of the manuscript will be hosted on arXiv", but the template repo says "Nowadays, MELBA publishes directly the papers (as opposed to initially being an arXiv-overlay)" and only *prefers* an arXiv copy. **The README reflects current practice; the website text is stale.** Note that `for_authors.html` also states "All manuscripts need to submitted on arXiv under the Creative Commons Attribution license" [sic] — treat an arXiv CC-BY copy as expected at acceptance, and confirm with the editors rather than assuming.

## 6. What to change in the manuscript for MELBA

**Budget 1–2 weeks. This is the smallest rewrite of the five venues.** The audience is ML-for-medical-imaging researchers — very close to the paper's natural readership.

| Element | Change |
|---|---|
| **Template** | Port to `\documentclass{melba}`. This is the main mechanical job. Do not modify the class |
| **Blinding** | **Un-blind it.** Put author names, affiliations and ORCIDs back on the manuscript via the template's `\author{}` / `\affiliations{}` / `\orcid{}` fields. Review is single-blind. Restore the acknowledgement of Dr. Almoamari |
| **Repo** | Because review is single-blind, **the repo may be made public** for this submission — and reviewers explicitly score whether code is shared. Do the release-hygiene checklist in `../../SUBMISSION_PLAYBOOK.md` §1.3 step 4 first |
| Length | Target ~20 pages. The current body (~4,800 words + 6 tables + 4 figures) will expand comfortably into that, so **add back** the material TÜBİTAK's 15-page cap forced out |
| Clinical framing | Keep, but shorten. Two paragraphs of burn-depth motivation, not two pages of epidemiology |
| Deployed system | Keep as a subsection — this audience is interested in deployment, and the "smartphone tools are under-validated" framing lands well here |
| Leakage story | Keep central. `fig_leakage.pdf` stays prominent. **Add** the within-model evidence (95.9% leaked vs 82.2% clean) as a primary result |
| Statistics | **Expand.** This readership reads statistics carefully. Add the power statement, the ddof = 1 correction, the exploratory-subgroup admission, and the per-source sensitivity analysis at N = 175 |
| Fairness | **Add the ITA skin-tone probe if you can.** MELBA runs a FAIMI (fairness) special issue; this community actively cares. Even a null with wide intervals is a contribution here |
| Data Availability | **Rewrite — it is mandatory and yours is currently a promise.** Give the actual repository link and DOI, or a well-justified explanation |
| References | The template mandates its own bibliography style. Convert from the TÜBİTAK numeric style |

## 7. Ordered submission steps

1. **[Can do today] Clone the template:** `git clone https://github.com/melba-journal/submission` — the LaTeX files are in `latex/`. Read `melba-sample.tex` and `melba-sample-in-submission.pdf`.
2. **[Can do today] Port the manuscript** to `\documentclass{melba}`. Do not modify the class file — "using any other template will result in a desk reject."
3. **[Can do today] Create a Scholastica account** at https://scholasticahq.com — free, and separate from the $10 per-submission charge.
4. **[Can do today] Confirm with your faculty** whether a non-DOAJ, possibly-non-Scopus venue satisfies your degree or CV requirements (§2).
5. **[After TÜBİTAK is clear] Rewrite** per §6. Un-blind. Restore the acknowledgement.
6. **[After TÜBİTAK is clear] Post the arXiv preprint** under a **CC BY** licence — MELBA expects it and it is explicitly encouraged.
7. **Release the repo** (single-blind review, so this is safe) after the hygiene checklist. Put the link in the Data Availability Statement.
8. **Write the cover letter** from `cover_letter.md`. **It must state if and how GenAI/LLMs were used** — this is a MELBA-specific hard requirement, not boilerplate.
9. **Go to** `http://app.scholasticahq.com/submissions/melba/new` (or find MELBA from https://melba.scholasticahq.com/) and log in.
10. **Work through Scholastica's six steps:** *Find the journal → Metadata → Authors → Files → Reviewers → Confirm and Submit.*
    - **Metadata:** title, abstract, **keywords** (MELBA's checklist names keywords explicitly).
    - **Authors:** "enter all authors in the scholastica system" — all three, with emails, affiliations and ORCIDs.
    - **Files:** the manuscript PDF, plus the cover letter uploaded as an additional file with the descriptor **"Cover Letter"**. Scholastica accepts `.docx` or `.pdf`.
    - Complete the **online conflict-of-interest declaration** — required from every author — and **name any editors you have recently collaborated with**.
11. **Pay the USD 10 Scholastica submission charge.** This is the only money in this entire playbook. It is charged by the platform, not the journal.
12. **Check everything before the final click:** "You cannot make any changes to your submission once you click Submit manuscript."
13. **Diarise.** No official turnaround exists; the 2023 special-issue figure was 4–6 weeks, so chase after **3 months**, not before.
14. **On Major Revisions:** MELBA's checklist requires a **"response to reviewer comments"** file on resubmission. Use `../../SUBMISSION_PLAYBOOK.md` §6, leading with the self-identified corrections in §6.4.
15. **On acceptance:** switch the class option to `accepted`, complete the **Ethical Standards and Conflicts of Interest sections at the end of the paper** (required post-acceptance per the template repo), and set the arXiv record's licence to CC BY 4.0 with the specified comment / journal-ref.

## 8. Files in this folder

- `cover_letter.md` — ready to send. **Contains the mandatory GenAI paragraph — do not delete it.**
- `checklist.md` — tick before submitting.
