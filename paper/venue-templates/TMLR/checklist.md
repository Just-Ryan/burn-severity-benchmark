# TMLR — pre-submission checklist

Verified against jmlr.org/tmlr and the live OpenReview API on **2026-07-25**. Re-verify before submitting.

## Gate 0 — am I allowed to submit at all?

- [ ] The TÜBİTAK manuscript has been **rejected**, or **formally withdrawn with written confirmation** from the editorial office.
- [ ] I have re-read TMLR's dual-submission clause: no reuse of text, figures or results from anything published, accepted, **or submitted in parallel** at another archival peer-reviewed venue.
- [ ] My graduation-project report is non-archival (or I have checked that my university's repository is not an archival peer-reviewed venue).
- [ ] I accept that **if TMLR rejects this paper, the submission and its reviews stay publicly readable on OpenReview forever** (only desk rejections are hidden).
- [ ] I have not submitted to TMLR twice already this year (Generalized Harmonic Quota Rule, N₁ = 2, N₉ = 9; desk rejections still spend budget).

## Gate 1 — OpenReview accounts (do this weeks in advance)

- [ ] Ryan Altayeb has an **activated** OpenReview profile.
- [ ] Abdulrahman Alraddadi has an **activated** OpenReview profile.
- [ ] Mohannad Alrehaili has an **activated** OpenReview profile.
- [ ] Each profile was created with an **institutional** email — gmail addresses take up to 2 weeks in moderation.
- [ ] Each profile has: full name, affiliation (Faculty of Computer and Information Systems, Islamic University of Madinah), ORCID, a **valid homepage showing name + affiliation + registration email**, publication history, conflicts of interest.

## Gate 2 — the manuscript

- [ ] Ported to `\documentclass[10pt]{article}` + `\usepackage{tmlr}` using the official style files from https://github.com/JmlrOrg/tmlr-style-file
- [ ] **The stylefile is unmodified.** Any change to formatting, font or layout "may result in rejection without review."
- [ ] Bibliography converted to `tmlr.bst` (author–year), not the TÜBİTAK numeric style.
- [ ] Main body is **≤ 12 pages** (this gets the 2-week review clock instead of 4 weeks).
- [ ] Appendix, if any, is placed **after the references** in the same PDF.
- [ ] Reframed per `README.md` §5: leakage is the centrepiece, the deployed app is ≤2 sentences, clinical epidemiology is cut, the leakage/evaluation literature leads the related work.
- [ ] Title no longer foregrounds the clinical application (scope desk-rejection risk).
- [ ] The within-model leakage evidence (95.9% leaked vs 82.2% clean, one model, one test set) is a **primary** result, not a footnote.
- [ ] `fig_leakage.pdf` is Figure 1.
- [ ] The power statement is present: 80% McNemar power near 8.5–9 pp at the observed discordance.
- [ ] The transformer-vs-convnet subgroup analysis is labelled **exploratory**.
- [ ] All open items from `../../SUBMISSION_PLAYBOOK.md` §1.5 are fixed: ddof = 1 SDs, the "won in all three seeds" claim corrected for external balanced accuracy, the 226-vs-118 cleaning chain, Table 3's "not tested (single seed)", the chance-level wording, the fixed-localiser caveat, the seed-42 figure caption.

## Gate 3 — anonymity

- [ ] Author block blank / stylefile in submission mode.
- [ ] No acknowledgements section (it names your supervisor).
- [ ] No GitHub URL, no Zenodo DOI, no institution name anywhere in the PDF.
- [ ] No self-citation phrased in the first person ("in our earlier work").
- [ ] **PDF metadata checked** — `pdfinfo manuscript.pdf` shows no author name or machine username.
- [ ] The arXiv preprint, if posted, is **not linked** from the submission.
- [ ] The supplementary ZIP is anonymised: no author names, no ORCIDs, no `.git` directory, no GitHub remote in `.git/config`, no absolute paths containing your username.

## Gate 4 — the submission form (fields confirmed live 2026-07-25)

- [ ] `title`
- [ ] `abstract` — trimmed from the current 321 words; rewritten in an ML register
- [ ] `authors` / `authorids` — all three, matched to activated profiles, in the agreed order
- [ ] `pdf` — anonymised
- [ ] `submission_length` — **"Regular submission (no more than 12 pages of main content)"**
- [ ] `competing_interests` — "The authors declare no competing interests."
- [ ] `human_subjects_reporting` — public de-identified images + an independent public research database; no new human-subjects data; no IRB approval required
- [ ] `supplementary_material` — anonymised ZIP, ≤ 100 MB (optional but strongly recommended here)
- [ ] `previous_TMLR_submission_url` — blank (first submission)

## Gate 5 — after clicking submit

- [ ] Watched for the email asking for **action editor recommendations**; replied within a few days using `cover_letter.md`.
- [ ] Recommended AEs working on evaluation methodology / dataset quality / empirical rigour — **not** clinical medical imaging.
- [ ] Diarised: AE assigned within ~1 week; reviews due 2 weeks after assignment; discussion 2–4 weeks; target decision ~9 weeks.
- [ ] Prepared to respond within **2 weeks of the third review** landing.
- [ ] The self-identified corrections block (`../../SUBMISSION_PLAYBOOK.md` §6.4) is ready to paste into the author response.

## Gate 6 — on acceptance

- [ ] Switched to `\usepackage[accepted]{tmlr}`.
- [ ] Added the link to the OpenReview review page in the camera-ready.
- [ ] **Proofread the camera-ready completely — it is final and changes are not allowed** afterwards except at Editors-in-Chief discretion.
- [ ] Repo made public, Zenodo DOI minted, links added.
- [ ] Optional: video presentation / code link added.
- [ ] arXiv version updated to the accepted text.
