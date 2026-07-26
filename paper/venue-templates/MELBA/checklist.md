# MELBA — pre-submission checklist

Verified 2026-07-25 against melba-journal.org, the melba-journal/submission repo, Scholastica, DOAJ, OpenAlex, NLM Catalog and the ISSN Portal. Re-verify before submitting.

## Gate 0 — allowed to submit, and is it worth it?

- [ ] TÜBİTAK has **rejected** the paper, or it is **formally withdrawn with written confirmation**. MELBA forbids simultaneous submission explicitly.
- [ ] **I have asked my faculty whether a publication in a journal that is NOT in DOAJ, and whose Scopus/WoS status I could not confirm, satisfies my degree / scholarship / CV requirement.** (See README §2. This is the single most important box on this page — tick it before doing any work.)
- [ ] I re-checked indexing myself in a browser: https://www.scopus.com/sources and https://mjl.clarivate.com for "Journal of Machine Learning for Biomedical Imaging" / ISSN 2766-905X.
- [ ] I checked https://github.com/melba-journal/submission#special-issues for an open special issue (evaluation / fairness / uncertainty would fit) with a stated deadline.

## Gate 1 — the template (desk-reject risk)

- [ ] Cloned https://github.com/melba-journal/submission and used the LaTeX files in `latex/`.
- [ ] Using **`\documentclass{melba}` with `melba.cls`** — *not* `melba.sty`, which does not exist despite the README linking it.
- [ ] **The class file is unmodified.** "using any other template will result in a desk reject."
- [ ] Default (submission) class option — line numbers on.
- [ ] Bibliography converted to the template's mandated style.
- [ ] Compiles cleanly against `melba-sample.tex` as a reference.

## Gate 2 — un-blinding (MELBA is SINGLE-blind)

- [ ] Author names, affiliations and ORCIDs are **ON** the manuscript PDF via `\author{}` / `\affiliations{}` / `\orcid{}`.
- [ ] The acknowledgement of **Dr. Hani Sayaf Almoamari** is restored (he consented in writing).
- [ ] The repo link is in the manuscript — and the repo is public and clean (see Gate 5).
- [ ] I have *not* accidentally left "Anonymised for double-blind review" anywhere.

## Gate 3 — mandatory statements (MELBA's differ from other venues)

- [ ] **Data Availability Statement** — present. Mandatory. Contains an actual repository link/DOI, or a well-justified explanation for withholding. **Not** a promise to release "upon acceptance."
- [ ] **Ethics statement** — present, using MELBA's own second branch: "a statement of why such approval was not required."
- [ ] **Conflict of interest** — declared in the manuscript, **and** the online declaration completed by **every** author in Scholastica.
- [ ] **Editors named** — "Authors must name all editors that have recently collaborated with the authors." Checked the current board; none apply (or listed those that do).
- [ ] **Funding / acknowledgements** — funding sources acknowledged (none, in this case — state it).
- [ ] **GenAI disclosure in the Acknowledgement section** of the manuscript.
- [ ] **GenAI disclosure in the cover letter** — separate hard requirement.
- [ ] The GenAI wording addresses MELBA's "not for unsupervised, de novo content creation" clause honestly — describing supervised drafting from author-supplied results with author verification. **Not** shortened to look compliant (README §4).
- [ ] CRediT is **not** required here, but ORCIDs supplied anyway.

## Gate 4 — the manuscript

- [ ] Length around **20 pages** — material cut for TÜBİTAK's 15-page cap has been added back.
- [ ] Clinical/epidemiological framing shortened to ~2 paragraphs.
- [ ] `fig_leakage.pdf` prominent; the within-model leakage evidence (95.9% leaked vs 82.2% clean) promoted to a **primary** result.
- [ ] Statistics section expanded: power statement (80% McNemar power near 8.5–9 pp), ddof = 1, exploratory-subgroup admission, per-source sensitivity at N = 175.
- [ ] Considered adding the **ITA skin-tone fairness probe** — this community runs a FAIMI special issue and actively cares.
- [ ] All open items in `../../SUBMISSION_PLAYBOOK.md` §1.5 fixed.
- [ ] `../../SUBMISSION_PLAYBOOK.md` §2 universal checklist worked through.

## Gate 5 — repo release (safe here, single-blind)

- [ ] `standalone_yolo_thresholds.json` regenerated and committed; notebook cell 26 saved **with outputs**.
- [ ] `benchmark1_masking_pooled_analysis.json` recomputed — its p-values currently contradict the manuscript.
- [ ] Stale "not yet exported" passage removed from `statistics/BENCHMARK2_AND_HEADTOHEAD.md`.
- [ ] `statistics/CLEAN_BENCHMARK_RESULTS.md` marked **SUPERSEDED**.
- [ ] 205-filename test manifest shipped; globs `sorted()`.
- [ ] `ci` field relabelled `ci_bootstrap` (it is not Wilson).
- [ ] The "56 of 199 sources … all were removed" claim reconciled with a released set containing 175 of 199 sources.
- [ ] Repo made **public**, Zenodo DOI minted, both links in the Data Availability Statement.

## Gate 6 — preprint

- [ ] arXiv preprint posted **under a CC BY licence** (MELBA expects this and encourages arXiv posting).
- [ ] The preprint uses the `arxiv` class option.
- [ ] The preprint declaration in the cover letter names the arXiv ID (or the sentence is deleted if there is none).

## Gate 7 — Scholastica submission

- [ ] Scholastica account created (free).
- [ ] Went to `http://app.scholasticahq.com/submissions/melba/new` or found MELBA from https://melba.scholasticahq.com/.
- [ ] **Metadata** step: title, abstract, **keywords** (explicitly on MELBA's checklist).
- [ ] **Authors** step: all three entered in the Scholastica system, with emails, affiliations and ORCIDs.
- [ ] **Files** step: manuscript PDF, plus the cover letter as an additional file with the descriptor **"Cover Letter"**.
- [ ] Online **conflict-of-interest declaration** completed by every author.
- [ ] Ready to pay the **USD 10** Scholastica submission charge (platform fee, not a journal APC — the only money in this playbook).
- [ ] **Everything checked before the final click:** "You cannot make any changes to your submission once you click Submit manuscript."

## Gate 8 — after submitting

- [ ] Diarised. No official turnaround is published; chase after **3 months**, not before.
- [ ] On **Major Revisions**: prepare the required **"response to reviewer comments"** file (on MELBA's checklist), following `../../SUBMISSION_PLAYBOOK.md` §6 and leading with the self-identified corrections in §6.4.
- [ ] On **acceptance**: switch to the `accepted` class option; complete the **Ethical Standards and Conflicts of Interest sections at the end of the paper**; set the arXiv record to CC BY 4.0 with the specified comment / journal-ref.
