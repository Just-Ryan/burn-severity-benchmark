# How to submit to MELBA — the whole thing, in order

*Everything here was verified against melba-journal.org, the melba-journal/submission repo, and
Scholastica. Where something is unverified I say so rather than guessing.*

---

## Your two questions first

### 1. Do we make the repo public before or after acceptance?

**Before. Before you submit.** Three reasons, and none of them is close:

- **MELBA review is single-blind.** Reviewers know who you are. There is no anonymity to protect,
  so the usual reason for waiting does not apply to you.
- **MELBA reviewers are scored on it.** Their reviewer form asks, in as many words,
  *"Reproducibility: is the code and/or data shared?"* A private link is a lost point on a
  criterion this paper is otherwise built to win.
- **It is this paper's single strongest asset.** A reviewer who can run `verify_paper_numbers.py`
  and watch 136 checks pass will trust everything else you wrote. A reviewer who cannot has only
  your word for it. Your paper is about not taking authors at their word.

The usual counter-argument — *someone will scoop us* — does not apply. The work will be on arXiv
with a timestamp, and the contribution is an audit of your own protocol, not a method anyone can
lift.

**Do it in this order:** finish the release-hygiene checklist below → make public → mint the Zenodo
DOI → put the DOI in the paper → submit.

### 2. Zenodo — what is it for, and what about licensing?

Zenodo is a free, CERN-run archive that gives your artifact a **permanent DOI**. GitHub can be
deleted, renamed, or made private; a Zenodo deposit cannot. That is the entire point: a reviewer
in 2030 following your Data Availability link should still land on something.

**How to do it (15 minutes):**

1. Log in to <https://zenodo.org> with your GitHub account.
2. Go to the GitHub tab and flip the switch **on** for `burn-severity-benchmark`.
   *The switch only appears for public repositories — so make the repo public first.*
3. Back on GitHub, cut a release (you already have the `v1.0-melba` tag with the weights attached).
   Zenodo captures it automatically within a minute or two.
4. Zenodo issues **two** DOIs. Use the right one:
   - a **concept DOI** that always resolves to the newest version ← **cite this one in the paper**
   - a **version DOI** for that specific release
5. Edit the Zenodo record: add all three authors with ORCIDs, the paper title, and the description.

**On licensing — and you have a real problem here.**

Your repo is currently **AGPL-3.0**. That is a strong network-copyleft licence: anyone who runs a
modified version as a service must publish their source. It is a fine licence for an application.
It is a poor licence for a research artifact, because it discourages exactly the reuse this paper
is asking for — you are telling people to adopt your leak-checking procedure, and AGPL makes a
company's lawyer say no.

**My recommendation:**

| What | Licence | Why |
|---|---|---|
| Code | **MIT** or **Apache-2.0** | Standard for research code. Apache-2.0 adds a patent grant; MIT is shorter. Either is fine |
| Data, figures, per-image predictions | **CC BY 4.0** | Matches the Roboflow source data you built on, and matches what MELBA publishes under |
| Trained weights | **CC BY 4.0** | Treated as data, not code |

This is your decision, not mine — AGPL is a legitimate choice if you *want* to force derivatives
open. But be aware you are choosing it, rather than inheriting it from a template. If you switch,
do it **before** the Zenodo deposit, because the deposit records whatever licence is in the repo at
capture time.

Zenodo will ask you to pick a licence during setup. Pick the one that matches your `LICENSE` file.

---

## Before you make anything public — release hygiene

- [ ] **Re-run the secret scan.** You have committed many times since the last one:
      ```bash
      git log -p --all | grep -niE "37cfeeb|sk-or-|sk-ant-|gho_|ghp_|hf_[A-Za-z0-9]|AKIA|BEGIN PRIVATE KEY|kaggle\.json"
      ```
      Expect zero hits. This scans **history**, not just the working tree — a key deleted in a
      later commit is still public in an earlier one.
- [ ] **Decide the licence** (above). Update `LICENSE` and the README badge if you change it.
- [ ] **Confirm no BIP_US images are redistributed.** That database was provided for research use;
      you may report results on it, not republish it.
- [ ] `python verify_paper_numbers.py` → **136/136**.
- [ ] `CITATION.cff` names all three authors with ORCIDs.
- [ ] README's first screen states what the repo is, the licence, and how to cite.

---

## Then: arXiv

MELBA explicitly encourages a preprint, and the TÜBİTAK declaration no longer binds you — that
submission was declined, so nothing is under review anywhere.

- [ ] Compile with the arxiv class option: `\documentclass[arxiv]{melba}` (turns off line numbers).
- [ ] Categories: **eess.IV** primary, **cs.CV** cross-list.
- [ ] Licence: **CC BY 4.0** — MELBA expects this at acceptance, so choose it now.
- [ ] arXiv requires an **endorsement** for a first submission in a category. This is the only step
      with unpredictable lead time. Start it early; a gmail address is fine.
- [ ] Put the arXiv ID in the cover letter once you have it.

---

## Then: Scholastica

Reach it by typing the publisher domain yourself: <https://melba.scholasticahq.com/>

1. **Create a Scholastica account.** Free. The $10 is charged per submission by the platform, not
   by MELBA.
2. **Metadata** — title, abstract, keywords. MELBA's checklist names keywords explicitly.
3. **Authors** — enter *all three*, each with email, affiliation and ORCID. MELBA asks for this.
4. **Files**
   - `manuscript.pdf` — compiled with the **default** class options, line numbers on.
   - `cover_letter.pdf` — upload as an additional file with the descriptor **"Cover Letter"**.
5. **Conflict-of-interest declaration** — required from *every* author, online, and you must
   **name any editors you have recently collaborated with**. You have none.
6. **Pay the USD 10.**
7. **Check everything before the final click.** Scholastica: *"You cannot make any changes to your
   submission once you click Submit manuscript."*

Then diarise a chase for **three months**. MELBA publishes no turnaround figure for regular
submissions; the "4–6 weeks" that circulates online is from 2023 *special-issue* blog posts and is
not current general policy.

---

## Things MELBA requires that are easy to miss

| Requirement | Where it lives now |
|---|---|
| **Data Availability Statement** | Mandatory. `\data{}` in the manuscript ✓ |
| **Ethics statement** | Mandatory — and MELBA explicitly accepts *"a statement of why such approval was not required"*, which is your case. `\ethics{}` ✓ |
| **Conflict of interest** | Mandatory in the paper **and** as an online form per author. `\coi{}` ✓ |
| **Funding / acknowledgements** | Mandatory. In `\acks{}` ✓ |
| **GenAI disclosure** | Mandatory in **two** places: an Acknowledgement section **and** the cover letter. Both done ✓ — do not delete either |
| **LaTeX template** | Mandatory. *"using any other template will result in a desk reject."* Using `melba.cls` unmodified ✓ |
| CRediT | **Not** required by MELBA |
| ORCID | Not required, but supplied ✓ |

---

## If you get Major Revisions

That is the most likely non-rejection outcome and it is a good one. MELBA requires a **"response to
reviewer comments"** file on resubmission.

**Lead with the corrections you found yourself.** You have five, including one where you leaked
into your own pipeline and then measured the leak at 12.7 points. Volunteering those before a
referee finds them is the strongest move available, and it is consistent with the paper's thesis
rather than an apology for it.

---

## One thing to tell the editors

`melba.cls` defines `\doi{}` as a setter for the paper's own DOI header field
(`\def\doi#1{\gdef\@doi{#1}}` — it stores the argument and prints nothing), which collides with the
`\doi{}` that `plainnat.bst` emits for every reference. Unpatched, every reference DOI vanishes and
the *last* reference's DOI overwrites the paper's own header and Crossmark link. `manuscript.tex`
patches it immediately before `\bibliography`. Worth a line in your submission comments — it
affects every MELBA paper that cites DOIs.

---

## Order of operations, condensed

```
1. secret scan + licence decision
2. repo → public
3. Zenodo switch on → cut release → get concept DOI
4. paste DOI into manuscript Data Availability → recompile
5. arXiv (start endorsement early)
6. Scholastica: metadata → authors → files → COI → $10 → submit
7. diarise a chase at 3 months
```
