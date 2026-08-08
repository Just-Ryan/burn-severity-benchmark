# Submitting to MELBA — do this in order

*Current as of 7 August 2026, manuscript state `ad4e9db`. This file replaces
`1_WITHDRAW_FROM_TUBITAK_FIRST.md` and `2_SUBMIT_TO_MELBA.md`, both of which are stale.*

**There is no TÜBİTAK step.** They declined the paper at editorial screening on 4 August 2026,
without external review. Nothing to withdraw. The cover letter already discloses this, which is the
correct handling — you are not hiding a prior submission, you are stating it.

---

## 0. One blocker before you submit

Your Data Availability Statement sends reviewers to the GitHub repository. Twelve Ultralytics
validation mosaics containing identifiable patient faces were removed from the repo and purged from
its Git history on 7 August, and the current tree and tag are clean. **But GitHub still serves those
objects by direct commit SHA** until it garbage-collects them:

```
https://raw.githubusercontent.com/Just-Ryan/burn-severity-benchmark/4de60be/benchmark2-proof/figures/yolo_1class_test/val_batch0_labels.jpg
```

Ask GitHub Support to garbage-collect unreachable objects on the repository, citing removal of
identifiable patient photographs, and reference commits `4de60be` and `cbc8fc5`. There are **zero
forks** and **zero release-asset downloads**, so nothing else needs chasing.

Re-check when they confirm — the URL above should return 404:

```bash
curl -s -o /dev/null -w "%{http_code}\n" -L "https://raw.githubusercontent.com/Just-Ryan/burn-severity-benchmark/4de60be/benchmark2-proof/figures/yolo_1class_test/val_batch0_labels.jpg"
```

---

## 1. What you upload

| File | Notes |
|---|---|
| `manuscript.pdf` | **32 pages.** Compiled with default class options, line numbers on |
| `cover_letter.pdf` | Upload with the descriptor **"Cover Letter"** |

Everything else in this folder is source, not submission material.

Rebuild the PDF if you change anything:

```bash
tectonic -X compile manuscript.tex
```

---

## 2. Metadata to paste into the portal

**Title**

> When Leakage Changes the Conclusion: A Methodological Evaluation of Segmentation-Guided Burn
> Severity Classification

**Authors** — all three, with emails, affiliations and ORCIDs. MELBA asks explicitly.

| Author | ORCID |
|---|---|
| Ryan Altayeb (corresponding, altayeb.ray@gmail.com) | 0009-0006-0031-9531 |
| Abdulrahman Alraddadi | 0009-0000-2325-5063 |
| Mohannad Alrehaili | 0009-0008-2491-185X |

Affiliation for all three: Faculty of Computer and Information Systems, Islamic University of
Madinah, Madinah, Saudi Arabia.

**Abstract** — copy from the PDF, not from `manuscript.tex` (the source contains LaTeX markup).

**Keywords** — Burn severity assessment, deep learning, data leakage, external validation, image
segmentation, reproducibility.

---

## 3. The portal

Scholastica, at `melba.scholasticahq.com`. Type the domain yourself rather than following a link.

1. Create a Scholastica account. Free; the **USD 10** is a per-submission platform charge, not a
   MELBA fee.
2. Find MELBA → **Metadata** → title, abstract, keywords (§2 above).
3. **Authors** → all three with ORCIDs.
4. **Files** → `manuscript.pdf`, then `cover_letter.pdf` tagged **"Cover Letter"**.
5. **Conflict-of-interest declaration** — required from *every* author. You have none, and none of
   you has recently collaborated with a MELBA editor.
6. Pay the USD 10.
7. **Read everything before the final click.** Scholastica: *"You cannot make any changes to your
   submission once you click Submit manuscript."*

### Worth putting in the submission comments

`melba.cls` defines `\doi{}` as a setter for the paper's own DOI header field
(`\def\doi#1{\gdef\@doi{#1}}` — stores the argument, prints nothing), but `plainnat.bst` emits
`\doi{...}` for every reference. Without a workaround every reference DOI is silently swallowed,
and the *last* reference's DOI overwrites `\@doi`, so an accepted paper prints someone else's DOI
in its own header and Crossmark link. `manuscript.tex` patches this immediately before
`\bibliography`. This is a template bug affecting every MELBA paper that cites DOIs, and the
editors will probably want to know.

---

## 4. Optional, and genuinely optional

**arXiv preprint.** MELBA encourages it and expects a CC-BY copy at acceptance. Compile with
`\documentclass[arxiv]{melba}` (disables line numbers). Category **eess.IV** primary, **cs.CV**
cross-list, licence **CC BY 4.0**. First submission in a category needs an endorsement, which is
the slow part — start early if you want it. If you post one, add a sentence to the cover letter
saying so. **Do not claim it in advance.**

**Zenodo DOI.** Connect the repo to Zenodo and cut a release; Zenodo mints the DOI. Then add it to
the Data Availability Statement. *Do not write a DOI into the paper before Zenodo has issued it.*

Neither of these blocks submission.

---

## 5. When reviews come back

Expect **major revision** rather than acceptance. That is the normal good outcome. MELBA requires a
**response-to-reviewers** file on resubmission.

**Lead with the corrections you found yourselves.** This paper argues that routine shortcuts
manufacture findings, and you caught eight in your own work — the leakage artifact, the residual
perceptual-duplicate pair, the three-seed variance failure, the skin-tone non-replication, the
un-propagated segmentation split, the metric dependence, the test-selected comparison arm, and the
test-selected *regime* that cost you the external parity claim on the last day. Volunteering those
before a referee finds them is the strongest move available and it is consistent with the paper's
thesis rather than an apology for it.

The four questions most likely to come back, and the honest answers:

| Likely reviewer question | Answer |
|---|---|
| The dataset is small | Yes. The methodological claims generalise; the burn results do not. Say so. |
| The labels are not clinician-confirmed | Correct, and it limits clinical interpretation of any absolute accuracy. The methodological comparison is still informative within the benchmark. **Do not offer to re-label** — that is a different study. |
| Does this generalise beyond burns? | It is demonstrated in one benchmark. Broader claims need replication. Do not overreach. |
| Why 32 pages? | Offer to move Tables 7, 9 and 10 to supplementary material. Do not cut them pre-emptively. |

---

## 6. State at freeze

| | |
|---|---|
| Manuscript | 32 pages, 0 overfull boxes, 0 undefined references |
| Bibliography | 67 entries, all cited, all 47 DOIs valid |
| Cross-references | 43, all resolve |
| Figures | 6, all present, all placed before the references |
| Reproducibility | `verify_paper_numbers.py` — **220/220** |
| Repository | Public, MIT + CC BY 4.0, no secrets, no source photographs |
| Release | `v1.0-melba`, 5 weight files, retagged on cleaned history |

Rerun the checks any time:

```bash
python verify_paper_numbers.py
```

---

## 7. After you submit

Diarise a chase at **three months**. MELBA publishes no turnaround figure for regular submissions;
the 4–6 week number that circulates comes from 2023 special-issue blog posts and is not current
general policy.

Then leave it alone. The next person who should tell you what is wrong with this paper is a MELBA
reviewer.
