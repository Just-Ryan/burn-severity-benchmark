# Submission playbook

**Paper:** *A comparative study of deep learning approaches for automated burn injury segmentation and severity classification*
**Authors:** Ryan Altayeb (corresponding, altayeb.ray@gmail.com, ORCID 0009-0006-0031-9531) · Abdulrahman Alraddadi (0009-0000-2325-5063) · Mohannad Alrehaili (0009-0008-2491-185X). All: Faculty of Computer and Information Systems, Islamic University of Madinah, Madinah, Saudi Arabia.
**Not an author:** Dr. Hani Sayaf Almoamari (supervisor) — **acknowledged only**. Do not add him to any author list at any venue without a fresh, explicit decision; author lists cannot normally be changed after submission.
**Playbook written:** 2026-07-25. **Every fee, URL and limit in this document was verified on the date stated next to it and will drift. Re-verify before you click submit.**

---

## 0. STOP — read this before you do anything

### 0.1 The paper is under review. You may not submit it anywhere else.

The manuscript is **under review at TÜBİTAK Turkish Journal of Electrical Engineering & Computer Sciences**, manuscript number **TURKJELECENGCOMPSCI-S-26-02236**.

> **Simultaneous submission of the same manuscript to two journals is research misconduct.** It is not a grey area and it is not a shortcut. It wastes reviewers' unpaid time, and if both journals accept, you have a duplicate publication that has to be retracted — with your names on the retraction notice, permanently, at the start of your careers.

COPE (the Committee on Publication Ethics, the body whose flowcharts nearly every journal follows) treats concurrent submission as an integrity case and expects authors to **formally withdraw from journal A before submitting to journal B** ([COPE: Handling concurrent and duplicate submissions](https://publicationethics.org/guidance/cope-position/handling-concurrent-and-duplicate-submissions); [COPE flowchart: Concurrent submissions of a manuscript to multiple journals](https://publicationethics.org/guidance/flowchart/concurrent-submissions-manuscript-multiple-journals)).

**The rule for this project, with no exceptions:**

| You may do now, while TÜBİTAK holds the paper | You may NOT do until TÜBİTAK returns a decision or the paper is formally withdrawn |
|---|---|
| Prepare every fallback package in full (reformat, rewrite, draft cover letters) | Upload the manuscript to any other journal's submission system, even as a "draft" you don't approve |
| Fix the repo and the analysis artefacts | Post to arXiv / medRxiv / any preprint server (see §0.2) |
| Write the response-to-reviewers material | Post the manuscript PDF on a personal site, ResearchGate, Academia.edu, LinkedIn, or a public GitHub repo |
| Run additional experiments | Make the code repo public (see §0.3) |

Everything in the `venue-templates/` folders is a **loaded, safed weapon**. Preparation is free and ethical. Firing is not, until the barrel is clear.

### 0.2 Do NOT preprint — because of what YOU declared, not because of what TÜBİTAK forbids

The title page you submitted to TÜBİTAK contains this section:

> **Pre-print server/online repository** — "This manuscript has not been previously posted to any pre-print server or other online repository."
> (`01_paper/SUBMISSION/titlepage.tex`, line 60)

That is a **declaration you made to a journal**, in a field the journal specifically provides for it. Posting to arXiv or medRxiv today would make a statement sitting in your submission file untrue. That is worse than not preprinting: it converts a neutral fact into a misrepresentation on the record.

**Get the reason right, because the reason matters.** TÜBİTAK itself has no objection to preprints. Its publisher-wide policy is explicit:

> "TÜBİTAK Academic Journals permit authors to post their manuscripts as preprints on reputable and non-commercial preprint servers (e.g., arXiv, bioRxiv, medRxiv, SSRN, etc.) before or during the submission process."
> "Posting a preprint does not prevent submission to TÜBİTAK journals."
> "The Preprint archive will not be considered a duplicate publication."
> — https://journals.tubitak.gov.tr/elektrik/policies.html (verified 2026-07-25; identical text at `/medical/policies.html`)

So the blocker is **your own declaration**, not the journal's rules. The policy also requires that a preprint be **disclosed at submission in the dedicated field** — which is exactly the field you filled in with a negative.

**This means you have two lawful routes, not one:**

| Route | What you do | Risk |
|---|---|---|
| **A — Default. Wait.** (recommended, and the operative rule for this project) | Do not preprint until TÜBİTAK returns a decision or the paper is formally withdrawn | Zero. Costs you a few months of priority on the leakage finding |
| **B — Correct the record first** | Email `elektrik@tubitak.gov.tr` from the corresponding author's registered address, quoting TURKJELECENGCOMPSCI-S-26-02236, stating that you wish to post a preprint under the journal's preprint policy and asking them to update the "Pre-print server/online repository" field on the title page. **Post only after they confirm in writing.** Then supply the arXiv link for that field | Low but non-zero: it puts your manuscript in front of the editorial office mid-review for an administrative reason, and it is an extra thing to get wrong. Do not take this route unless someone is about to scoop the leakage finding |

**Do not** simply post and hope nobody checks. That is the one option that is actually dishonest.

Note that §9.3 and §11.1 of `INDEPENDENT_AUDIT_2026-07.md` advise posting to arXiv "immediately and unconditionally." **That advice is superseded here.** It was correct about TÜBİTAK's policy and wrong about your declaration; follow route A or route B, not the audit.

**If you do preprint (via route B, or after a decision):** TÜBİTAK asks you to protect the double-blind:

> "Where possible, authors may choose to post preprints without listing their full names or affiliations until after the peer review process"
> — https://journals.tubitak.gov.tr/elektrik/policies.html (verified 2026-07-25)

Post to arXiv `cs.CV` with cross-list `eess.IV`, consider omitting affiliations while review is live, and update the preprint with the final DOI after publication.

**Whatever happens, keep the declaration accurate.** Every venue in `venue-templates/` has a preprint field. The moment a preprint exists, the answer changes from "none" to "arXiv:XXXX.XXXXX" everywhere, forever. Put it on a checklist so you never send a stale negative again.

### 0.3 The GitHub repo stays PRIVATE.

`github.com/Just-Ryan/burn-severity-benchmark` is currently private. **Keep it private.**

- The repo contains author names and ORCIDs. TÜBİTAK review is **double-blind**. A referee who finds the repo de-anonymises you and can, in principle, report a blinding breach.
- Your Data Availability statement already says the repo will be released **upon acceptance** — which is the correct promise and buys you time to fix the artefacts (§1.3).
- Do not link it, do not mention the URL in any correspondence with the journal, and do not push the manuscript PDF to it.
- When you do release: strip nothing, but re-read §1.3 first. A repo whose files contradict the paper is worse than no repo.

### 0.4 Zero budget: what "free" actually means

You cannot pay an APC. Two routes satisfy that, and the second one is the one nobody tells undergraduates about:

1. **Diamond / platinum OA** — free to publish *and* free to read. The publisher is funded by a society, university, or government agency. Examples here: TÜBİTAK journals, TMLR, MELBA.
2. **Hybrid journals via the subscription route** — **this is the important one.** Elsevier, Springer Nature, Oxford University Press and IEEE hybrid titles publish your article at **zero cost to you** if you simply *decline* the optional gold open-access option at the licensing stage. The APC you see advertised ($3,000+) is a **choice**, not a bill. Choose "subscription" / "no open access", sign the standard publishing agreement, and you pay nothing. Your article is then paywalled, and you achieve free "green" open access separately by depositing the accepted manuscript in arXiv or your institutional repository after the publisher's embargo.

**What this rules out:** fully gold-OA journals, where there is no subscription route and the APC is unavoidable. That excludes MDPI titles (*Diagnostics*, *Journal of Imaging*, *Sensors*, *Bioengineering*), all Frontiers titles, PLOS ONE / PLOS Digital Health, *Scientific Reports*, *BMC Medical Imaging*, *PeerJ Computer Science*, *IEEE Access*, *Burns & Trauma* (OUP), *Burns Open*, *Heliyon*, *Intelligence-Based Medicine*, *Machine Learning with Applications*, and *Array*. All are legitimate journals. They are simply incompatible with a zero-fee constraint. Do not let a friendly editor talk you into one.

**The trap to watch for:** at the *acceptance* stage of a hybrid journal you will be shown a rights/licensing form that presents gold OA attractively and sometimes as the default. Read it slowly. Choose the subscription option. If any screen asks for a card, stop and re-read — you have taken a wrong turn.

---

## 1. Decision tree: what to do on each TÜBİTAK outcome

TÜBİTAK Editorial Manager will eventually change the manuscript status. There are four outcomes. Find yours and follow the branch. **Do not improvise.**

```
                        TURKJELECENGCOMPSCI-S-26-02236
                                    │
        ┌───────────────┬───────────┴────────┬──────────────────┐
        │               │                    │                  │
     ACCEPT       MINOR REVISION       MAJOR REVISION         REJECT
        │               │                    │                  │
      §1.1            §1.2                 §1.3               §1.4
```

### 1.1 ACCEPT (as-is, or accept-after-proof)

Rare on a first round (~10% here). If it happens:

1. **Do not celebrate by publishing anything yet.** Wait for the formal acceptance email with a manuscript ID and a proof stage.
2. **Make the repo public and mint a Zenodo DOI** — but only after working through the release checklist in §1.3, step 4. A public repo that contradicts the published paper is a correction waiting to happen.
3. **Update the Data Availability statement** in the camera-ready with the real GitHub URL and the Zenodo DOI.
4. **Add the acknowledgement of Dr. Almoamari back in** — it is currently only on the title page (blinded out of the main manuscript). Check it survives into the proof.
5. **Read the galley proof against `v2-improved/manuscript.tex` line by line**, especially every number in Tables 3–6. Typesetters introduce errors in tables more than anywhere else. You get one proof round.
6. **Then**, and only then, deposit the accepted version. TÜBİTAK is diamond OA so the published version is already free; a green deposit is optional.
7. Close out `venue-templates/` — you will not need it. Keep it; you will write another paper.

### 1.2 MINOR REVISION

The best realistic outcome. Turn it around **fast** — minor-revision deadlines are typically 2–4 weeks and a late return can be re-classified as a new submission.

1. Build the response letter using the template in §6.
2. Apply the reviewer's requests **and** the self-identified corrections listed in §6.4. Volunteer them; do not wait to be caught.
3. The improved manuscript at `v2-improved/manuscript.tex` **already contains most of those corrections** (§1.5). Diff it against `SUBMISSION/manuscript.tex` so your response letter describes changes accurately.
4. **Watch the page limit.** TÜBİTAK allows up to 20 pages *only after a revision request* (the initial cap is 15). A minor revision is your one chance to add the material the audit wants. Use it.
5. Re-check the abstract word count — `v2-improved` is currently **321 words** against a **300-word cap** (§2.2). Trim before resubmitting.
6. Upload as a **revision**, not a new submission. In Editorial Manager: *Submissions Needing Revision* → *Submit Revision*, never *Submit New Manuscript*.

### 1.3 MAJOR REVISION (most likely single outcome, ~45%)

Treat this as good news. A major revision means the editor wants the paper.

1. **Read every referee point twice before writing a word.** Sort them into: (a) things you will do, (b) things you will do differently and explain why, (c) things you will decline and justify. Never leave a point unanswered.
2. **Volunteer the self-identified corrections in §6.4 in the first section of the letter**, before answering any referee. Referees reward authors who find their own errors — and this paper's entire thesis is about finding your own errors. Doing it is *on-brand*, not embarrassing.
3. **Land the `v2-improved` changes.** They already answer six of the audit's major items. §1.5 lists exactly which, and which remain open.
4. **Do the repo work now** (it does not touch the manuscript, so it is safe during review). From `INDEPENDENT_AUDIT_2026-07.md` §5, before any public release:
   - `standalone_yolo_thresholds.json` regenerated and committed; notebook cell 26 saved **with outputs**.
   - `benchmark1_masking_pooled_analysis.json` recomputed — its p-values currently **contradict the manuscript** (0.2336 / 0.6014 / 0.3007 vs the paper's 0.32 / 0.66 / 0.33). Record the scipy version and the `alternative` argument in the JSON.
   - Delete the stale "not yet exported" passage in `statistics/BENCHMARK2_AND_HEADTOHEAD.md:229-237`.
   - Mark `statistics/CLEAN_BENCHMARK_RESULTS.md` **SUPERSEDED** — it currently asserts "Mean Δ = 0.00 pp", contradicting the paper's +0.55.
   - Ship the 205-filename test manifest as JSON; wrap the globs in `sorted(...)`.
   - Relabel the `ci` field in `benchmark1_11arch_4cond_seed42.json` as `ci_bootstrap` (it is not Wilson).
   - Reconcile the "56 of 199 sources … all were removed" claim with a released set that contains 175 of 199 sources.
5. **Consider the two cheap high-impact additions** if the referees give you an opening: two more seeds (5 total) in the head-to-head, and promoting the within-model leakage number (95.9% on leaked test images vs 82.2% on clean ones, same model, same test set) to a primary result. Both are hours, not weeks.
6. Deadline: typically 60–90 days. Ask for an extension **before** it expires if you need one; editors grant them routinely and refuse them retroactively.

### 1.4 REJECT

Not a disaster. ~30% probability and mostly driven by "no method novelty," which is a venue-fit problem, not a quality problem.

**Do these five things, in this order, in the first week:**

1. **Confirm the rejection is final.** Read the decision letter for the words "reject and resubmit" or "we would consider a substantially revised version" — that is *not* a rejection, it is a major revision wearing a costume, and you should take it (branch §1.3).
2. **Harvest the referee reports.** Even a rejecting referee gives you free peer review. Fix everything they raised *before* the next submission. The next venue's referees will raise the same points.
3. **NOW you may preprint.** Post to arXiv `cs.CV` with cross-list `eess.IV`. This timestamps the leakage finding and makes the work citable while you wait through another review cycle. Use the `v2-improved` version plus the referee-driven fixes. **Then update the preprint declaration** in every venue package from "has not been posted" to the arXiv ID (§0.2, last paragraph). MELBA additionally expects the arXiv copy to carry a **CC BY** licence.
4. **Now you may make the repo public** — after the §1.3 step-4 checklist. Add the GitHub and Zenodo links to the Data Availability statement of the next submission.
5. **Pick the next venue** using §3 and §4, then work through that venue's folder in `venue-templates/`.

**Order of fallback venues** (rationale in §4):

| Order | Venue | Pick it if… |
|---|---|---|
| 1 | **MELBA** | You want the smallest rewrite. Closest topical fit: ML for biomedical imaging, values evaluation/methodology work. |
| 2 | **TMLR** | You are willing to rewrite in an ML register. Its acceptance criteria are the best match in existence for a well-evidenced null result. |
| 3 | ***Burns*** (Elsevier) | You are willing to rewrite for a clinical audience and lead with the under-grading safety finding. Highest prestige; free via the subscription route; slowest. |
| 4 | **CMPB** (Elsevier) | The rewrite went computational rather than clinical. |
| 5 | **TJMS** (TÜBİTAK) | You want the closest thing to a lateral move: same publisher family, diamond OA, PubMed-indexed, clinical framing. |

**Do not** submit to two of these at once. Same rule as §0.1: one at a time, always.

### 1.5 Where `v2-improved` already stands

`v2-improved/manuscript.tex` is a **corrected** version of what was submitted. Diffing it against `SUBMISSION/manuscript.tex` shows it has already fixed:

| Audit item | Fixed in v2? | What changed |
|---|---|---|
| STAT-06 — Wilson CIs promised but never printed | **Yes** | Table 4 now prints seed-42 Wilson intervals: classifier [76.6, 87.0] internal / [69.2, 78.8] external; pipeline [75.6, 86.2] / [64.7, 74.7] |
| CR-01 — false claim "no source photograph appears in more than one fold" | **Yes** | The categorical sentence is deleted; a new paragraph in §Mat:leak discloses **2 of 205 test images (1.0%)** perceptually identical to a training image under a different source id, one pair with conflicting labels |
| SI-01 — external set not source-grouped | **Yes** | §Mat:eval now states the 319 images derive from **175 distinct sources** and that `N=319` intervals "should be read as optimistic" |
| CR-07 — bare "Mann-Whitney p = 0.33" was one-sided | **Yes** | Now "one-sided Mann-Whitney p=0.33; two-sided p=0.66" in both text and Table 3 note |
| STAT-07 — error-bar-overlap fallacy | **Yes** | Replaced with the correct paired test: **+3.74 pp internally, 95% CI +3.04 to +4.44, paired t p = 0.002**; Figure 2 caption rewritten |
| SI-02 / STAT-02 — unreproducible "MDE 3.64 pp at N=205" | **Yes** | Replaced throughout with the CI on the effect: **+0.55 pp, 95% CI −0.37 to +1.47** |
| SI-03 — "external shift toward lower severity" contradicted by the matrix | **Yes** | Replaced with conditional rates: under-graded 19.3% internally (23/119) and 28.3% externally (51/180); over-graded 10.1% / 15.2% |
| §6 item 1 — no leakage figure | **Yes** | New `fig_leakage.pdf` (Figure 1) |

**Still open in `v2-improved` — fix these before any resubmission or new submission:**

| Open item | Where | Fix |
|---|---|---|
| STAT-01 — `±` values are population SDs (ddof = 0), sample SDs are 22.5% larger | Table 4, §Res:h2h | Recompute from the stored seed arrays: 82.6 ± 0.7, 76.6 ± 1.6 (bal 80.1 ± 1.8), 78.9 ± 1.0, 73.4 ± 2.5 (bal 77.9 ± 3.4). Add "(n = 3, ddof = 1)" to the statistics paragraph |
| STAT-05 — "The classifier won on both sets in all three seeds" is false for external **balanced** accuracy (seed 1: pipeline 80.14 vs classifier 79.96) | §Res:h2h | "…had the higher accuracy on both sets in all three seeds; on external balanced accuracy it led in two of three" |
| SI-12 — abstract says "removed 118 contaminated images"; 226 were removed | Abstract, §Mat:eval, Table 1 | State the full chain: 1,371 images / 199 sources → 118 pHash-identical → 226 removed in total → 319 images / 175 sources |
| SI-08 — Table 3 declares the cropping conditions "not significant" although no test was run | Table 3 | "not tested (single seed)" |
| SI-16 — "against a chance level of 50 percent" mischaracterises the baseline | §Res:ext, Table 5 | "against 50 percent for a trivial constant predictor on this two-class probe" |
| Abstract length | Abstract | **321 words** — over the 300-word TÜBİTAK cap, over *Burns*' cap, and over most venues. Trim (§2.2) |
| CR-12 — the localiser was held fixed across seeds | §Mat:bench | One sentence: the pipeline's cross-seed SD reflects classifier variability only and understates full pipeline variance |
| SI-10 — Figure 4 caption still says "a representative seed" | Fig. `fig:cm` caption | Name seed 42 and state that it is the pipeline's most favourable internal run and least favourable external run |

---

## 2. Before you submit ANYWHERE: the universal checklist

Work through this **once**, then work through the venue-specific checklist in the relevant `venue-templates/*/checklist.md`. Nothing here is venue-specific; all of it is required almost everywhere.

### 2.1 Identity and credit

- [ ] **ORCID for all three authors, verified live.** Open each in a browser and confirm it resolves to the right person:
  - Ryan Altayeb — https://orcid.org/0009-0006-0031-9531
  - Abdulrahman Alraddadi — https://orcid.org/0009-0000-2325-5063
  - Mohannad Alrehaili — https://orcid.org/0009-0008-2491-185X
- [ ] Each ORCID record has the **Islamic University of Madinah affiliation** and a working email. Empty ORCID records look like a fabricated identity to a suspicious editor.
- [ ] **Author order fixed and agreed by all three, in writing (a WhatsApp message is fine).** Most systems will not let you change it after submission without an editor's intervention and a signed statement from every author.
- [ ] **Corresponding author = Ryan Altayeb, altayeb.ray@gmail.com.** Use the same address everywhere. Consider whether a university address is available — some editors distrust free webmail for corresponding authors, though none will reject on it.
- [ ] **CRediT statement** matches, word for word, between (a) the submission-system form, (b) the title page, and (c) any "Author contributions" section. The authoritative version is in `SUBMISSION/SUBMISSION_METADATA.md` §"Author contributions (CRediT)":
  - **Ryan Altayeb:** Conceptualization (lead); Data curation (lead); Software (lead); Supervision (lead); Validation (equal); Visualization (lead).
  - **Abdulrahman Alraddadi:** Conceptualization (equal); Formal analysis (supporting); Methodology (lead); Project administration (equal); Validation (equal); Writing – original draft (lead); Writing – review and editing (lead).
  - **Mohannad Alrehaili:** Formal analysis (lead); Investigation (lead); Project administration (equal); Resources (lead); Supervision (equal).
- [ ] **Dr. Hani Sayaf Almoamari appears in the Acknowledgements, not the author list.** Confirm he has *agreed in writing* to be acknowledged — most journals formally require named individuals to consent to acknowledgement.
- [ ] Sanity check on the authorship decision itself: if the supervisor's contribution meets the ICMJE/CRediT bar, excluding him is not "modest," it is a mis-attribution. This is your call and it is reversible only *before* submission. Decide once, deliberately, then stop revisiting it.

### 2.2 The manuscript itself

- [ ] **Abstract within the venue's cap.** `v2-improved` is **321 words**. Caps: TÜBİTAK 300, *Burns* and CMPB stricter still (§3). Trim by cutting the second sentence of the leakage description and the "Flutter and Flask" detail — not by cutting numbers.
- [ ] **Title in the venue's required case.** TÜBİTAK wants sentence case. Elsevier journals accept either but are consistent within a journal. Look at three recent articles in the target journal and copy their style.
- [ ] **Every number in the manuscript traces to a file in `benchmark2-proof/results/` or `statistics/`.** This was true at TÜBİTAK submission and must stay true. If you change one number, grep the whole `.tex` for it — several numbers appear in the abstract, the body, a table, and a figure caption.
- [ ] **The open items in §1.5 are fixed.** Do not send a manuscript you already know contains a false sentence.
- [ ] References: all cited, none orphaned, DOIs present, journal-name style matching the venue. `v2-improved` has **51 references**.
- [ ] Consistent spelling (British *or* American, not both). The manuscript currently uses British forms ("localiser", "anonymised") — keep them, but check the venue does not mandate American.
- [ ] Acronyms defined at first use. "pHash", "mAP50", "MDE", "ITA" are the risky ones.

### 2.3 Figures

- [ ] Four figures in `v2-improved/`: `fig_leakage.pdf`, `fig_system.pdf`, `head_to_head.pdf`, and the two-panel confusion-matrix figure (`cm_true_pipeline.pdf` + `ext_cm_pipe.pdf`).
- [ ] **Format matches the venue.** TÜBİTAK accepts **PDF only** and explicitly rejects PNG/JPEG/EPS/TIFF. Elsevier prefers EPS/PDF for vector and TIFF ≥300 dpi for raster. MELBA/TMLR take PDF inside the LaTeX build. Check before you export.
- [ ] Resolution and size within venue limits (TÜBİTAK: ≥118 px/cm at 16 cm width, ≤16×20 cm, ≥8 cm wide).
- [ ] **Figures uploaded both embedded in the manuscript and as separate files** where the venue requires it (TÜBİTAK does; Elsevier does; TMLR/MELBA do not).
- [ ] Every figure is referenced in the text in order, and the caption says what the reader should conclude, not just what is plotted.
- [ ] **Figure 2 (`head_to_head.pdf`) has no generating script in the tree.** Before you claim it was regenerated, reconstruct the script. If you cannot, do not change the caption's description of the error bars.
- [ ] Colour figures readable in greyscale and by colour-blind readers (the confusion matrices are the risk).

### 2.4 Declarations — every venue asks for all of these

Copy these from `SUBMISSION/SUBMISSION_METADATA.md`; they are already drafted and correct.

- [ ] **Funding:** "This research received no specific grant from any funding agency in the public, commercial, or not-for-profit sectors."
- [ ] **Conflict of interest:** "The authors declare no conflict of interest."
- [ ] **Ethics / IRB:** "This study used only publicly available, de-identified burn images (Roboflow, CC BY 4.0) and an independent public research database (BIP_US, University of Seville). No new human-subjects data were collected, so institutional review board approval was not required." — *Medical journals (Burns, TJMS) will scrutinise this hardest. Some require a formal letter from your institution's ethics committee stating that approval was not required. Ask your faculty for that letter now; it takes weeks and costs nothing.*
- [ ] **Informed consent:** not applicable — no new participants; images are public and de-identified.
- [ ] **Data availability:** currently "will be made available upon acceptance; links withheld to preserve double-blind review." After a rejection and repo release, replace with the actual GitHub + Zenodo DOI.
- [ ] **Preprint status:** currently "has not been previously posted to any pre-print server or other online repository." **This must be updated the moment you post a preprint (§0.2).** A stale declaration is a false declaration.
- [ ] **Generative AI declaration** — see §2.5. Do not shorten it.

### 2.5 The AI disclosure — keep it accurate, do not water it down

The declaration in `v2-improved/manuscript.tex` (§"Declaration of generative AI and AI-assisted technologies") is accurate and appropriately detailed. It states that Claude was used to organise materials, reproduce and check results, run the statistical/benchmarking/external-validation analyses, and **draft and edit the manuscript**, while the research itself — system design, model training, dataset preparation, mobile application — was conceived and carried out by the authors.

- [ ] **Do not trim it to look better.** Under-declaring AI use is a much more serious integrity problem than declaring a lot of it. Every major publisher's policy asks for disclosure of exactly this.
- [ ] **Consider strengthening it** — the audit notes the current wording slightly understates scope, since the AI also drafted figure captions and tables. "…draft and edit the manuscript, including tables and figure captions" is more accurate and costs you nothing.
- [ ] **AI is never an author.** Confirm no venue form lets you accidentally add it.
- [ ] **Placement varies by venue.** Elsevier requires the statement in a *declared section immediately before the reference list*; TÜBİTAK took it on the title page. Move it, do not delete it.
- [ ] The final sentence — "the authors reviewed and edited the content as needed and take full responsibility for the content of the publication" — is required by Elsevier's policy wording. Keep it verbatim.

### 2.6 Integrity checks

- [ ] **Similarity check.** TÜBİTAK returns manuscripts above ~25% iThenticate similarity and can ban above 50%. Ask your university library to run a Turnitin/iThenticate report before each submission — most Saudi universities provide this free to students. Self-plagiarism from your own graduation-project report counts.
- [ ] **No text recycled** from the graduation-project report without rewriting.
- [ ] **Image rights:** the Roboflow set is CC BY 4.0 — attribute it. BIP_US is provided for research by the University of Seville — confirm you have written permission for the use you are making, and that any figure reproducing a BIP_US image is permitted. **If in doubt, do not reproduce a BIP_US image in a figure.**
- [ ] **Nothing identifying you in the blinded manuscript**: no author names, no acknowledgements, no repo URL, no "our previous work [12]" self-citations phrased in the first person, and **no PDF metadata leaking your name** (check with `pdfinfo` or File → Properties; LaTeX often stamps the machine username).

---

## 3. The five fallback venues at a glance

**Everything in this table was verified on 2026-07-25** from the publishers' own sites. **Fees, metrics and indexing change. Re-verify before you submit** — the *Burns* APC alone moved from USD 3,190 to USD 3,570 between the project audit and this playbook.

| | **MELBA** | **TMLR** | ***Burns*** | **CMPB** | **TJMS** |
|---|---|---|---|---|---|
| **Full name** | J. of Machine Learning for Biomedical Imaging | Transactions on Machine Learning Research | Burns (ISBI journal) | Computer Methods and Programs in Biomedicine | Turkish J. of Medical Sciences |
| **Publisher** | Community / MELBA editors | JMLR | Elsevier | Elsevier Ireland | TÜBİTAK ULAKBİM |
| **Fee to you** | **USD 0** publication + **USD 10** Scholastica submission charge | **USD 0** | **USD 0** via subscription route (gold OA is USD 3,570 — decline it) | **USD 0** via subscription route (gold OA is USD 3,180 — decline it) | **USD 0** (diamond) |
| **Model** | Diamond OA, CC BY 4.0 | Diamond OA, CC BY 4.0 | Hybrid — go subscription, 12-mo green embargo | Hybrid — go subscription, 12-mo green embargo | Diamond OA, CC BY 4.0 |
| **Indexing** | ⚠️ **NOT in DOAJ.** PubMed "selected citations only", **not MEDLINE**. **Scopus & WoS UNVERIFIED.** ISSN 2766-905X | DOAJ ✓ · **Scopus ✓** · DBLP ✓ · Google Scholar patchy (TMLR says so itself) | **SCIE ✓ · Scopus ✓ · MEDLINE ✓** (NLM: "Currently indexed for MEDLINE") | **SCIE ✓ · Scopus ✓ · MEDLINE ✓** | **SCIE ✓ · Scopus ✓ (1994–) · PubMed ✓ · MEDLINE ✓** · DOAJ ✓ |
| **Metrics** | none published; makes no indexing claims at all | CiteScore/SJR **UNVERIFIED** (Scopus pages bot-blocked) | IF **2.6** · CiteScore 4.7 · SCImago Q1 | **IF 6.4** · CiteScore 11.9 · SCImago Q1 | IF **1.4** · **Q2** |
| **Format** | **LaTeX only**, `melba.cls`. Other templates = **desk reject** | **LaTeX only**, `tmlr.sty` | Word (.doc/.docx) **or** LaTeX (.tex). No PDF source | Word (.doc/.docx) **or** LaTeX (.tex). No PDF source | **Word only.** No LaTeX |
| **Template** | github.com/melba-journal/submission | github.com/JmlrOrg/tmlr-style-file | none journal-specific (`elsarticle` publisher-wide) | none linked (**UNVERIFIED**) | `Medical-Sciences-Templates-2026.rar` — mandatory |
| **Length** | ~20 pages, no hard limit | no limit; **≤12 pp main body** halves review time | **not published — UNVERIFIED** | **≤3,500 words**, **≤50 refs** ← tightest | ≤30 pp double-spaced, ≤60 refs, ≤10 figs+tables |
| **Abstract** | no stated limit | no stated limit | **≤250 w, unstructured** | **≤350 w, 4 headings**, must give precision/sensitivity/specificity | **≤300 w, 4 headings** |
| **Blinding** | **Single-blind** — names ON the PDF | **Double-blind AND public**; rejected papers stay online forever | **Single-anonymised** — do not anonymise | **Single-anonymised** — do not anonymise | **Double-blind**, separate title page |
| **Decision time** | **UNVERIFIED** (2023 special-issue figure was 4–6 wks) | ~**9 weeks** target, not guaranteed | 63 d "submission to decision after review" — *not* a first-decision median; true figure **UNVERIFIED** | **40 d** to first decision (published) | **UNVERIFIED** |
| **Submit at** | app.scholasticahq.com/submissions/melba/new | openreview.net/group?id=TMLR | editorialmanager.com/jbur | **submit.elsevier.com/CMPB** (*not* Editorial Manager) | www2.cloud.editorialmanager.com/turkjmedsci |
| **Biggest reframing needed** | **Almost none — un-blind it and expand it back to ~20 pages.** Smallest job of the five | **Strip the clinical framing entirely; lead with leakage as an ML methodology result.** Largest intellectual rewrite | **Invert to clinical: lead with under-triage safety, bury the architecture benchmarking.** Largest audience shift | **Cut 1,300 words and lead with the released software/protocol, not the null result** | **Rebuild in Word and convert to a clinical paper.** Largest mechanical rebuild |

### Three things this table should change in your thinking

1. **MELBA's indexing is worse than the project audit assumed.** `INDEPENDENT_AUDIT_2026-07.md` §9.1 says MELBA is in DOAJ. **It is not** — the DOAJ API returns zero results for ISSN 2766-905X, and OpenAlex agrees (`is_in_doaj: false`). PubMed carries only ~12 MELBA items, as "selected citations only", not MEDLINE indexing. Scopus and Web of Science could not be verified either way. MELBA is a legitimate, respected, community-run journal — but **if your degree, scholarship or CV needs a Scopus/WoS-indexed publication, ask your faculty before you spend six weeks on it.** That email is five minutes and can save a year.
2. **The best-indexed venues here are the Elsevier hybrids, and they are free.** *Burns* and CMPB both have SCIE + Scopus + MEDLINE and both cost nothing if you decline gold OA. CMPB has the strongest metrics of anything in this playbook (IF 6.4, Q1). The barrier is fit and word count, not money.
3. **TMLR's rejection is permanent and public.** Every other venue lets a rejection disappear. TMLR does not: "All submitted papers, including those accepted, rejected, withdrawn, or retracted, are made publicly accessible on OpenReview." Only desk rejections are hidden. Weigh that before choosing it over MELBA.

---

## 4. What to change in the manuscript, venue by venue

Full detail lives in each `venue-templates/*/README.md` §"What to change". This is the summary you use to *choose*.

### 4.1 Effort and risk

| Venue | Rewrite effort | Main risk | Best-case appeal |
|---|---|---|---|
| **MELBA** | **1–2 weeks** | Indexing may not satisfy your degree requirement | Reviewers explicitly score reproducibility, and yours is excellent |
| **TMLR** | 3–5 weeks | Scope desk-rejection; a permanent public rejection record | Acceptance criteria are "claims supported by evidence" + "would some individuals be interested" — nothing about novelty |
| ***Burns*** | 4–6 weeks | No methodological novelty; clinical reviewers want a clinician in the loop | The under-triage finding is directly actionable for its readership; highest prestige |
| **CMPB** | 3–4 weeks | 3,500 words is brutal; scope favours "formal computing methods" | Software papers are explicitly welcomed; IF 6.4 |
| **TJMS** | 2–3 weeks | Scope names no medical informatics; "technical details" caveat | Diamond OA + MEDLINE, and you know the publisher's systems |

### 4.2 The single reframing sentence for each

- **MELBA** — *"An empirical comparison in medical imaging whose central finding is a data-quality artifact, with everything released."* You barely change the paper; you un-blind it, add back the material TÜBİTAK's page cap forced out, and make the Data Availability Statement real (it is mandatory there and yours is currently a promise).
- **TMLR** — *"File-level splits of pre-augmented datasets manufacture effects; here is a matched before/after with a within-model decomposition."* Retitle away from burns. Cut the epidemiology and the app. Promote the 95.9%-vs-82.2% within-model evidence to a primary result. Get the main body under 12 pages.
- **Burns** — *"A burn-severity model that looks 82.6% accurate under-triages 55 of 94 clinical burns and calls half of full-thickness burns first degree."* Lead with patient harm. Compress the architecture tables to one. Add the clinical depth vocabulary. Address skin tone prominently — every reviewer will raise it.
- **CMPB** — *"A reproducible protocol and released software for source-grouped splitting and perceptual-hash contamination screening, demonstrated on a clinical imaging system."* Lead with the method and the software, because that is what the scope names. Then cut 1,300 words and compute precision/sensitivity/specificity, which the structured abstract demands and your paper does not currently report.
- **TJMS** — *"Is an AI burn-assessment tool safe to use on real patients? No, and here is the measurement."* Rebuild in Word from the mandatory template. Structured abstract. Full journal names in references. Compress the engineering.

### 4.3 The traps that differ per venue — do not carry a habit across

| Thing | MELBA | TMLR | Burns | CMPB | TJMS |
|---|---|---|---|---|---|
| Anonymise the manuscript? | **No** | **Yes** | **No** | **No** | **Yes** |
| Journal names in references | template style | `tmlr.bst` author–year | **abbreviated** (LTWA) | **abbreviated** (LTWA) | **spelled out in full** |
| CRediT required? | **No** (narrative instead) | not a form field | **Yes**, on the disclosures form | **Yes** | **Yes**, must match the title page |
| Where the GenAI statement goes | **Acknowledgements *and* the cover letter** | not a form field | **new section before the references** | **new section before the references** | dedicated section, **with model version and exact prompt** |
| Data availability statement | **Mandatory** | expected in practice | not required | encouraged | required section |
| Extra mandatory file | cover letter | — | **disclosures form + highlights** | **cover letter + declarations output** | **separate title page** |
| Can the repo be public? | **Yes** | **No** (anonymised ZIP only) | **Yes** | **Yes** | **No** |

### 4.4 What NOT to change, anywhere

- **The honesty.** The leakage story, the failed replication, the clinical collapse, and the refusal to headline the 83.9% oracle number are why this paper deserves to exist. Every venue rewards them; none requires you to soften them.
- **The AI declaration.** Move it, reformat it, expand it. Never shrink it (§2.5).
- **The limitations section.** Reviewers who see a candid limitations section trust the rest of the paper more, not less.
- **"We claim no methodological novelty."** Saying it first removes the reviewer's best weapon.

---

## 5. Exact submission steps

**Per-venue click-by-click instructions live in each venue folder's `README.md` §"Ordered submission steps".** They are too long and too venue-specific to duplicate here, and duplicating them means they drift.

| Venue | Steps | Note |
|---|---|---|
| MELBA | `venue-templates/MELBA/README.md` §7 | Scholastica's six steps; USD 10 charge; **submission is irreversible once clicked** |
| TMLR | `venue-templates/TMLR/README.md` §7 | OpenReview; **all three authors need activated profiles first — start this weeks early** |
| *Burns* | `venue-templates/BURNS_Elsevier/README.md` §7 | Editorial Manager `jbur`; **mandatory disclosures form + highlights file** |
| CMPB | `venue-templates/CMPB_Elsevier/README.md` §8 | **submit.elsevier.com/CMPB**, *not* Editorial Manager (which currently says "do not use for live manuscript submission") |
| TJMS | `venue-templates/TJMS_Tubitak/README.md` §6 | Editorial Manager `turkjmedsci`; **Word template is mandatory** |
| TJEECS (current) | `SUBMISSION/SUBMISSION_GUIDE.md` | The tab-by-tab walkthrough you already used |

### 5.1 The three steps that apply to every venue

**Step A — verify the venue is real (§7.3).** Fifteen minutes. Type the URL yourself.

**Step B — build the file set before you open the submission system.** Every system times out, and half of them lose your work when they do. Have every file finished on disk first.

**Step C — never approve without reading the built proof.** Every one of these systems assembles your uploads into a single PDF and shows it to you. **Approval is the only irreversible action in the whole process.** Read the proof: check that figures appear, that tables are not mangled, that no LaTeX error page has been inserted, and that a double-blind submission contains no author names. The TÜBİTAK submission failed its first build attempt for exactly this reason (see `SUBMISSION/SUBMISSION_GUIDE.md` §0).

### 5.2 If you need to withdraw from TÜBİTAK first

TÜBİTAK publishes a withdrawal *policy* but no withdrawal *procedure*. Verified 2026-07-25 at https://journals.tubitak.gov.tr/elektrik/policies.html:

> "withdrawal generally refers to a voluntary action taken by the author(s), usually prior to acceptance or publication"
> "A withdrawn article is not considered part of the journal's publication history."
> "Withdrawal requests are thoroughly reviewed by the Editor-in-Chief (EiC) and may be denied"
> **"Authors do not have an automatic right to withdraw a manuscript after peer review"**
> "The journal reserves the right to proceed with editorial evaluation or ethical review if the withdrawal request appears intended to circumvent editorial or ethical procedures."

**UNVERIFIED:** there is no published form, deadline, fee, named contact or step-by-step mechanism, and no stated penalty for a good-faith withdrawal.

**What to do, given that:**

1. Send a short, signed request **from Ryan's registered corresponding-author address** to **elektrik@tubitak.gov.tr**, quoting **TURKJELECENGCOMPSCI-S-26-02236** and the full title, stating the reason plainly, and CC'ing both co-authors. Alternatively use "Send E-mail" from the submission's Author Main Menu in Editorial Manager.
2. **Wait for written confirmation from the Editor-in-Chief.** Withdrawal is not effective until they confirm it. Note the policy explicitly says requests "may be denied."
3. **Do not submit anywhere else until that confirmation arrives in your inbox.** Not "probably fine", not "it's been two weeks" — in writing.
4. Note where the policy's teeth are aimed: withdrawals used to dodge authorship or ethics scrutiny. A straightforward "we wish to withdraw" before a decision is normal and low-risk.

**Do not withdraw merely because the review is slow.** It restarts your clock at zero and costs you a relationship with an editor who may referee your next paper.



## 6. Responding to reviewers

This section applies to a TÜBİTAK revision and to every future venue. It is the single highest-leverage document you will write on this project.

### 6.1 Rules

1. **Answer every point.** Number them exactly as the referee numbered them. An unanswered point is read as a concession.
2. **Never argue about tone.** If a referee is rude, respond as if they were polite. Editors read both documents.
3. **Quote the referee verbatim, then answer.** Editors skim; they must be able to see the point and your answer without opening the manuscript.
4. **Say where the change is.** "Revised, Section 3.2, page 7, lines 214–221" — with the line numbers of the *revised* file. Your manuscript already has `lineno` enabled, so use it.
5. **Include the new text.** Paste the actual replacement sentences into the letter. Do not make the editor hunt.
6. **Disagree at most twice, and with evidence.** A letter that concedes everything looks unserious; one that concedes nothing looks defensive. Pick your two hills.
7. **Provide a marked-up manuscript** (colour or `latexdiff`) alongside the clean one if the venue allows it. `latexdiff SUBMISSION/manuscript.tex v2-improved/manuscript.tex > diff.tex` gives you this in one command.

### 6.2 Structure of the response letter

```
[Date]
[Editor name], [Journal]
Re: Manuscript [ID] — "[Title]"

Dear [Editor],

  ¶1  Thank you. State the decision you are responding to, and that you
      have revised the manuscript accordingly.

  ¶2  ONE paragraph summarising the three or four biggest changes.

  ¶3  ── SELF-IDENTIFIED CORRECTIONS ──  (see §6.4 — put this BEFORE
      the referee responses, not buried at the end)

  Then, for each referee:

  ## Reviewer 1

  **Comment 1.1** — [verbatim quote of the referee's point]

  **Response.** [What you did. If you changed the manuscript, quote the
  new text and give section + line numbers. If you declined, give the
  reason in two sentences and offer an alternative.]

  **Change made.** Section X.Y, lines NN–MM: "[new text]"

  ... repeat ...

  Closing: thank the referees specifically for the points that improved
  the paper (name them), and state that all authors approved the revision.

Sincerely,
Ryan Altayeb, on behalf of all authors
```

### 6.3 A worked example of the register you want

> **Comment 2.3** — *"The claim that no source photograph appears in more than one fold is not verified anywhere in the manuscript."*
>
> **Response.** The referee is right, and the claim was in fact false. We removed it and replaced it with the result of an actual content-based audit, which found a small residual we had not previously detected. We would rather report this than let it stand. The effect is bounded at 1.0 percentage point and reverses no comparison in the paper, and we now use it to make a methodological point that strengthens the study's own thesis.
>
> **Change made.** Section 2.2, lines 92–98: "Source grouping removes leakage between augmented copies of the same file, but it cannot remove what the file names do not encode. […] we find 2 of the 205 test images (1.0 percent) are perceptually identical to a training image carrying a different source identifier […] One of the two pairs is additionally annotated with conflicting labels in the two folds."

Note what that does: it concedes fully, quantifies the damage, and converts the concession into evidence for the paper's argument. That is the move to repeat throughout.

### 6.4 The self-identified corrections — VOLUNTEER THESE

Put this block near the top of the response letter, before Reviewer 1. Suggested heading: **"Corrections identified by the authors during an internal re-audit."**

**Suggested opening paragraph:**

> Before responding to the referees, we wish to report five corrections that we identified ourselves during an internal re-audit conducted while the manuscript was under review. None of them changes any conclusion of the paper. We report them unprompted because this manuscript's central argument is that self-scrutiny of one's own favourable results is the thing the field under-does, and we would rather hold ourselves to that standard than be held to it.

Then, one short numbered item each:

**(1) Wilson confidence intervals are now printed.**
> The submitted manuscript promised Wilson intervals in three places and criticised prior work for omitting them, but printed no numeric interval. We have added them to the single-seed reference rows of Table 4: the standalone classifier 82.4% [76.6, 87.0] internally and 74.3% [69.2, 78.8] externally; the robust pipeline 81.5% [75.6, 86.2] and 69.9% [64.7, 74.7]. The intervals are approximately 10 percentage points wide, which is the most useful single fact about the precision of this study and which we had failed to give the reader. We have added a sentence stating that the ± values are cross-seed training variability, not sampling uncertainty.

**(2) Residual leakage in the internal split is now disclosed.**
> The submitted manuscript stated categorically that no source photograph appeared in more than one fold. Applying our own flip-aware pHash/dHash screen to the corrected split, we found that **2 of the 205 test images (1.0%)** are perceptually identical to a training image carrying a different source identifier, and that one of those two pairs carries conflicting ground-truth labels. We have replaced the categorical claim with a threshold-qualified statement of what was actually verified, quantified the bound (at most 1.0 pp, reversing no comparison), and drawn the methodological lesson: grouping by identifier must be verified with a content-based check. We did not rebuild the split, because doing so to correct 0.98% of the test set would invalidate every confidence interval, McNemar test and multi-seed mean in the paper.

**(3) The external set is 319 images from 175 source photographs.**
> We applied source-grouping to the internal test set but not to the external set — precisely the failure our paper exists to warn about. We now state in Section 2.6 that the 319 external images derive from **175 distinct source photographs** (mean 1.8 per source, maximum 4), that they are therefore not 319 independent observations, and that intervals computed on N = 319 should be read as optimistic. A per-source majority-vote sensitivity analysis at N = 175 gives 73.7% for the classifier and 72.6% for the pipeline (McNemar b/c = 24/22, exact p = 0.88); over 5,000 random one-image-per-source draws no dedup variant changes the conclusion.

**(4) The Mann-Whitney test's sidedness is now stated.**
> The submitted manuscript reported "Mann-Whitney p = 0.33" without stating that this is the **one-sided** value. We now state the tail explicitly and give both: one-sided p = 0.33, two-sided p = 0.66. We also now identify the transformer-versus-convolutional comparison as **exploratory** — it was suggested by the seed-42 results rather than pre-specified, which is exactly why we subjected it to a fresh-seed confirmation that it failed.

**(5) A paired test across seeds has been added, replacing an invalid inference.**
> The submitted manuscript inferred "no difference" from overlapping error bars in a paired design, which is not a valid inference — and in the internal panel the ±1 SD bars do not in fact overlap. We have removed that reasoning and run the correct test on data we already had. The paired per-seed difference is **+3.74 pp internally (95% CI +3.04 to +4.44, paired t, p = 0.002)** and **+3.24 pp externally (95% CI −3.83 to +10.31, p = 0.19)**. We now separate two questions that we had conflated: whether one system beats another *on these particular images* (McNemar; not resolved at N = 205, where 80% power requires roughly 8.5–9 pp) and whether it does so *on average across training runs* (paired t; clearly yes internally). We note that the localiser was held fixed across seeds, so the pipeline's cross-seed SD reflects classifier variability only.

**And, if you have also fixed them by then, add:**
> We have additionally replaced the minimum-detectable-effect framing with a confidence interval on the effect itself (+0.55 pp, 95% CI −0.37 to +1.47), corrected the description of external error direction to conditional under- and over-grading rates, recomputed all ± values with ddof = 1, and corrected the abstract's account of external-set cleaning (226 images were removed in total, of which 118 were perceptual-hash identical to training).

### 6.5 The two hills worth defending

If a referee pushes on these, hold your ground politely:

- **"There is no methodological novelty."** Correct, and stated in the paper. The contribution is a quantified leakage case study with the before-and-after both reported, plus a leak-free external evaluation showing a clinically dangerous failure mode. Point out that the paper explicitly frames its contribution as the combination rather than novelty, and that a null result reported honestly is exactly what the burn literature is short of.
- **"N = 205 is too small."** Correct, and stated in the paper. Answer with power, not apology: at the observed discordance, exact McNemar reaches 80% power only near 8.5–9 pp, and the paper says so rather than claiming a significant difference it cannot detect. Offer the additional seeds if they want more.

**Do not defend:** the residual leakage, the un-grouped external set, the missing intervals, or the ddof bug. Concede all of those immediately and completely — they are correct criticisms and the concession is what makes the rest of the letter credible.

---

## 7. Predatory venues: defence and verification protocol

Within weeks of any submission — and immediately after any preprint — you will start receiving flattering emails inviting you to submit to journals you have never heard of. Some will name your paper. They are automated and they are scraping the submission metadata.

### 7.1 Rules that never change

1. **Never respond to an unsolicited invitation to submit.** No reputable journal recruits by cold email. Delete.
2. **Never navigate to a journal from a link in an email.** Type the publisher's domain yourself: `journals.tubitak.gov.tr`, `sciencedirect.com`, `link.springer.com`, `academic.oup.com`, `jmlr.org`, `melba-journal.org`. This is the single most effective defence against **hijacked journals** — fake mirror sites that clone a real journal's name, ISSN and branding to take your money. The Retraction Watch Hijacked Journal Checker passed **400 entries** in December 2025 and grows by 70–80 a year ([Retraction Watch, 2025-12-26](https://retractionwatch.com/2025/12/26/retraction-watch-hijacked-journal-checker-now-has-400-entries)). Turkish and Iranian journals are disproportionately targeted, which is directly relevant to you.
3. **A fee that appears only after acceptance is a scam**, without exception. Legitimate journals publish their APC before submission.

### 7.2 Red flags

- Guaranteed acceptance, or a promised review turnaround of days.
- "Impact factor" from a fake metrics provider: Universal Impact Factor, Global Impact Factor, SJIF, Cosmos, Index Copernicus Value, ICV. **The only impact factor that exists is Clarivate's Journal Impact Factor in Journal Citation Reports.** Everything else is invented.
- An editorial board with no affiliations, or affiliations that don't check out when you search the person's university page.
- A journal name one word away from a famous one (*Journal of Machine Learning Research and Applications*, *International Burns Journal*).
- Broken English, stock-photo editors, a "call for papers" for a "special issue" you never heard of.
- Payment by personal bank transfer or to an individual.
- Publisher families to avoid outright: OMICS/Longdom, SCIRP, Academic Journals (Nigeria), IJSER / IJARCCE / IJRASET / IJERT-style engineering mills, "World Scientific News"-type aggregators.

### 7.3 The verification protocol — run this before EVERY submission

Do all five. It takes fifteen minutes and it is the cheapest insurance in your career.

| # | Check | Where | Pass condition |
|---|---|---|---|
| 1 | **Am I on the real site?** | Type the publisher domain manually | The journal lives on the publisher's own domain, with a valid HTTPS certificate issued to that publisher |
| 2 | **Is it hijacked?** | [Retraction Watch Hijacked Journal Checker](https://retractionwatch.com/the-retraction-watch-hijacked-journal-checker/) | The title/URL is **not** listed |
| 3 | **Is it in DOAJ?** (OA journals only) | https://doaj.org/search/journals | Listed, with the ISSN matching the site |
| 4 | **Is it indexed *today*?** | Scopus: https://www.scopus.com/sources · Web of Science: https://mjl.clarivate.com · PubMed: https://www.ncbi.nlm.nih.gov/nlmcatalog/journals | Listed as **currently** covered. A journal's own website claiming "Scopus indexed" is marketing; the Scopus Sources page is fact. Journals get de-listed and never update their own site |
| 5 | **Is the fee stated publicly, before submission?** | The journal's own author pages | An explicit fee (or explicit "no fee"), findable without an account |

Also run the [Think. Check. Submit.](https://thinkchecksubmit.org/journals/) checklist the first time you consider any new venue.

**If any of the five fails, stop and think.** For an unknown journal that emailed you, a failure means *do not submit* — no exceptions, no "but the deadline."

### 7.3.1 When the checklist and reality disagree

**MELBA fails check 3 (it is not in DOAJ) and check 4 is unverifiable (Scopus and Web of Science could not be confirmed). MELBA is not predatory.** It is community-run, transparent about its editorial process, a Crossref member with its own DOI prefix, hosts the MIDL and MICCAI-workshop special issues, and publishes identifiable researchers you can look up. It also makes **no indexing claims whatsoever** on its own site — which is the opposite of what a predatory journal does.

The lesson is worth internalising because you will face it again:

- **Predatory journals fail the checklist *and* claim they pass it.** Fake impact factors, invented index names, "Scopus indexed" banners that Scopus has never heard of. The lie is the signal, not the absence.
- **Young legitimate journals fail the checklist and say nothing.** Indexing takes years to obtain, and honest editors do not pretend otherwise.
- The checklist is a **screening tool that decides what to investigate**, not a verdict. Something that fails it needs a human look, not an automatic no.

**What a failure should trigger:** who are the editors, and do their university pages confirm the role? Who has published there, and would you cite them? Is the review process described in public? Is the fee stated up front? Does anyone in your field recognise the name?

**And the separate, practical question:** even a legitimate journal may not count for your degree, your scholarship, or a future job application. That is not an integrity question, it is an administrative one — and it is answered by asking your faculty, before you submit, not after.



### 7.4 The grey zone

MDPI and Frontiers are **not** predatory — they are legitimately indexed and widely cited — but they carry reputational baggage with some hiring and grant committees, and their special-issue solicitation emails are indistinguishable from predatory ones in tone. They are excluded here purely on cost (§0.4). If someone tells you your paper was rejected because you published in MDPI, that is a real phenomenon and not something you can control after the fact.

---

## 8. Timeline: what to expect and when

Times below are typical ranges. Nothing in academic publishing arrives on schedule.

```
2026
 Jul ██ SUBMITTED (TÜBİTAK, 2026-07-23)
     ░░ ← YOU ARE HERE (2026-07-25). Do the repo work. Draft everything.
 Aug ░░ editorial/technical check, referee assignment
 Sep ░░ referees reading
 Oct ▓▓ first decision plausible (TÜBİTAK typically ~2–4 months)
     │
     ├─ MINOR ─────► revise 2–4 wks ──► accept ~Dec 2026 ──► online early 2027
     │
     ├─ MAJOR ─────► revise 4–8 wks ──► 2nd round 6–10 wks ──► accept ~Feb–Apr 2027
     │
     └─ REJECT ────► 1 wk: harvest reports, preprint, release repo
                     │
                     ├─ MELBA  : reformat 1–2 wks → decision 2–4 months → accept mid-2027
                     ├─ TMLR   : rewrite 3–5 wks → decision ~2 months (rolling) → accept mid-2027
                     ├─ Burns  : rewrite 4–6 wks → decision 2–4 months → accept late 2027
                     ├─ CMPB   : rewrite 3–4 wks → decision 2–4 months → accept late 2027
                     └─ TJMS   : reformat 2–3 wks → decision 2–4 months → accept 2027
```

**Planning assumptions that are usually right:**

- **Budget 12 months from today to a published paper**, and be pleasantly surprised. The audit's estimate — ~85% probability of acceptance at a reputable, fee-free venue within 12 months, given the §1.5 fixes — is realistic.
- **Every rejection costs 3–5 months**, of which only 2–4 weeks is your own work. Which is exactly why the fallback packages are prepared *now*, in parallel, rather than after a rejection.
- **Silence is normal.** Do not email the editor before **3 months** of no status change. After 3 months, a single polite one-paragraph enquiry quoting the manuscript number is entirely acceptable and often works.
- **Do not withdraw a manuscript merely because it is slow.** Withdrawing to chase a faster venue restarts the clock at zero and burns a bridge with an editor who may be a referee for you later.

**What to do with the waiting time (in priority order):**

1. The repo fixes in §1.3 step 4 — ~4–6 hours, must be done before any public release.
2. Draft the exact replacement text for every open item in §1.5, so a revision takes days rather than weeks.
3. Two additional seeds (5 total) in the head-to-head — GPU time, not human time. This is the cheapest large improvement available.
4. Promote the within-model leakage evidence (95.9% on leaked test images vs 82.2% on clean ones — one model, one test set, no confounds) to a primary result. ~1 hour, and it is the strongest causal evidence in the project.
5. The ITA skin-tone fairness probe — computable from the images you already have, and it is the single most-requested missing analysis in clinical AI review.
6. Only then: prepare the venue packages in `venue-templates/`.

---

## 9. Quick reference

| I want to… | Go to |
|---|---|
| Know whether I'm allowed to submit somewhere | §0.1 |
| Know whether I can preprint | §0.2 |
| Know what to do about the TÜBİTAK decision | §1 |
| Know what's already fixed vs still broken in the manuscript | §1.5 |
| Prepare a submission to any venue | §2, then the venue folder |
| Compare the five fallback venues | §3 |
| Know what to rewrite for a specific venue | §4 |
| Write a response to reviewers | §6 |
| Check a journal is real | §7.3 |
| Know when to worry about silence | §8 |

**Venue folders:** `venue-templates/MELBA/` · `venue-templates/TMLR/` · `venue-templates/BURNS_Elsevier/` · `venue-templates/CMPB_Elsevier/` · `venue-templates/TJMS_Tubitak/`
Each contains `README.md` (facts and ordered steps), `cover_letter.md` (ready to send), and `checklist.md` (tick boxes).

**Key project files:**

| File | What it is |
|---|---|
| `v2-improved/manuscript.tex` | The corrected manuscript. **Use this one**, not the submitted version |
| `SUBMISSION/manuscript.tex` | Exactly what TÜBİTAK has. Do not edit; it is the record |
| `SUBMISSION/titlepage.tex` | Author names, ORCIDs, CRediT, declarations |
| `SUBMISSION/SUBMISSION_METADATA.md` | Copy-paste sheet for submission forms |
| `SUBMISSION/SUBMISSION_GUIDE.md` | The TÜBİTAK Editorial Manager walkthrough |
| `INDEPENDENT_AUDIT_2026-07.md` | The full audit. §2 is the action table; §9 is venues; §10 is how to strengthen the paper |
