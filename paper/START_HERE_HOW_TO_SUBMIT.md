# START HERE — what to do about publishing this paper

*Written 26 July 2026. This is the short, actionable version.
The long reference is `SUBMISSION_PLAYBOOK.md`; the per-journal folders are in `venue-templates/`.*

---

## 1. The question you asked: can I submit elsewhere while TÜBİTAK has it?

**Your friend is right that you can publish in other journals. He is right about formats too.
But the timing matters, and this is the one rule that can actually damage you.**

| | Allowed? |
|---|---|
| Submitting to journal B **while** journal A is still reviewing | ❌ **No** |
| **Withdrawing** from journal A, then submitting to journal B | ✅ **Yes — and it can be done today** |
| Submitting to journal B after journal A rejects | ✅ Yes |
| Different journals wanting Word vs LaTeX vs PDF | ✅ True, and irrelevant to the rule above |

This is not a TÜBİTAK quirk. It is the position of [COPE](https://publicationethics.org/guidance/cope-position/handling-concurrent-and-duplicate-submissions),
which essentially every reputable journal follows. The realistic downside of being caught is
not a lecture: it is rejection from both journals, and editors sometimes notify the authors'
institution. As an undergraduate publishing your first paper, that is a bad trade for a few
months.

**So you are not stuck for five or six months. You have a choice, and you can make it today.**

---

## 2. Your actual decision

### Option A — Wait for TÜBİTAK
- **Cost:** likely 2–5 months to a first decision.
- **Upside:** it is a real SCIE/Scopus-indexed journal, free, and your paper is already there and
  formatted for it. Realistic odds are roughly **45 % major-revision-then-accept**.
- Meanwhile: finish the revisions (already done in `v2-improved/`), keep the repo private, and
  prepare the response letter so a revision request can be answered in days.

### Option B — Withdraw and go straight to a better-fitting venue
- **Cost:** you give up a submission that has a decent chance.
- **Upside:** **MELBA** and **TMLR** fit this paper *better* than TÜBİTAK does, and TMLR in
  particular judges only whether claims are supported by evidence — it explicitly does **not**
  reject for lack of novelty, which is this paper's main vulnerability everywhere else.
- **How:** email the editorial office, one short paragraph, ask them to withdraw
  `TURKJELECENGCOMPSCI-S-26-02236`. Wait for written confirmation. Then submit elsewhere.

**My recommendation: Option A, with one exception.** Wait — unless your degree or graduation
has a deadline that five months would miss. The paper is already there, it costs nothing to
wait, and a major revision at TÜBİTAK is a good outcome. Use the waiting time to finish the
strengthening work.

> **Withdrawal email template**
>
> Subject: Withdrawal request — TURKJELECENGCOMPSCI-S-26-02236
>
> Dear Editor,
>
> I am writing to request the withdrawal of manuscript TURKJELECENGCOMPSCI-S-26-02236,
> "A comparative study of deep learning approaches for automated burn injury segmentation and
> severity classification," submitted on 23 July 2026.
>
> After further analysis we have substantially revised the study's statistical treatment and
> wish to submit the revised work to a venue whose scope is a closer fit. I apologise for the
> inconvenience and am grateful for the time the editorial office has already given us.
>
> Could you please confirm the withdrawal in writing.
>
> Sincerely,
> Ryan Altayeb (on behalf of all authors)

---

## 3. Two things you must NOT do right now

1. **Do not post to arXiv or any preprint server yet.** Your submitted title page states
   *"This manuscript has not been previously posted to any pre-print server or other online
   repository."* Posting now makes a submitted statement false. (TÜBİTAK itself permits
   preprints — the blocker is our own wording.) After a rejection or a confirmed withdrawal,
   post immediately.
2. **Do not make the GitHub repository public yet.** It contains your names and ORCIDs, and the
   review is double-blind.

---

## 4. Where to submit — ranked, all free

**"Free" here means free to publish.** Hybrid journals (Elsevier, Springer, IEEE) charge only
if you *choose* gold open access; if you decline it, publishing costs nothing and the article
sits behind a paywall. You may then post the accepted manuscript to arXiv for free ("green"
open access).

| # | Venue | Fee | Indexed | Fit | Format |
|---|---|---|---|---|---|
| **1** | **MELBA** — J. Machine Learning for Biomedical Imaging | Free (~$10 submission) | ⚠️ **not in DOAJ** — verify it counts for your degree | Best topical match | LaTeX |
| **2** | **TMLR** — Trans. on Machine Learning Research | Free | DOAJ, DBLP | Best *criteria* match — judges evidence, not novelty | LaTeX (OpenReview) |
| **3** | ***Burns*** (Elsevier) | Free via subscription route | SCIE, Scopus, PubMed, **Q1** | Best clinical audience, highest prestige | LaTeX or Word |
| **4** | *Comput. Methods Programs Biomed.* | Free via subscription | SCIE, Scopus, Q1 | Good | LaTeX or Word |
| **5** | TÜBİTAK Turkish J. Medical Sciences | Free | SCIE, Scopus, PubMed | Good if reframed clinically | **Word only** |

**Two time-sensitive notes:**
- **MELBA is not in DOAJ.** It is legitimate and respected in the MICCAI community, but if your
  university requires a DOAJ/Scopus-indexed venue, check **before** spending six weeks. One email
  to your faculty.
- **TMLR requires OpenReview accounts for all three authors, and gmail addresses can take up to
  two weeks to clear moderation.** If TMLR is anywhere in your plan, **create those accounts now** —
  it is the only item with a two-week lead time.

**Never submit to:** anything that emails you an invitation, promises fast acceptance, or hides
its fee until after acceptance. Verify every venue is in DOAJ (if open access) *and* Scopus or
Web of Science, and that the fee is stated publicly before you submit. Always reach a journal by
typing its publisher's domain yourself — hijacked mirror sites are common in this field.

---

## 5. Exactly what to do, in order

**Now (today):**
1. Decide Option A or B (§2).
2. If TMLR is a possibility, create OpenReview accounts for all three authors.
3. Email your faculty: *"Does a journal need to be in Scopus/DOAJ for my graduation
   requirement?"* — the answer changes the ranking above.
4. Do **not** preprint. Do **not** make the repo public.

**While waiting:**
5. The revised manuscript is ready in `01_paper/v2-improved/` — it fixes nine defects an
   independent audit found, including printing the confidence intervals the submitted version
   promised but never showed.
6. Read `venue-templates/<venue>/README.md` for whichever venue you would go to next.

**When TÜBİTAK replies:**
- **Accept** → celebrate, then make the repo public and mint the Zenodo DOI.
- **Minor/major revision** → answer with `v2-improved`, and *volunteer* the self-found
  corrections in the response letter. Doing that before the referees find them is the single
  strongest move available. Template in `SUBMISSION_PLAYBOOK.md` §6.
- **Reject** → post to arXiv the same day, then submit to MELBA (or TMLR). Cover letters are
  already written in `venue-templates/`.

---

## 6. What is already prepared for you

| File | What it is |
|---|---|
| `01_paper/SUBMISSION/` | **Frozen.** Exactly what went to TÜBİTAK — do not edit |
| `01_paper/v2-improved/` | The revised, stronger manuscript + two new figures |
| `01_paper/SUBMISSION_PLAYBOOK.md` | Full reference: checklists, per-venue steps, reviewer-response templates |
| `01_paper/venue-templates/*/` | Per-journal README, tailored cover letter, and checklist |
| `01_paper/INDEPENDENT_AUDIT_2026-07.md` | The full audit, 126 findings |
| GitHub `verify_paper_numbers.py` | Recomputes 49 published numbers from raw data; all pass |
