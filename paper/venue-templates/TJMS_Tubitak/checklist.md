# Turkish Journal of Medical Sciences — pre-submission checklist

Verified 2026-07-25 against journals.tubitak.gov.tr and the 2026 Word templates downloaded from the site. Re-verify before submitting.

## Gate 0 — allowed to submit?

- [ ] TJEECS has **rejected** the paper, or it is **formally withdrawn with written confirmation from the editorial office**. TJEECS and TJMS are sister journals under the same publisher — a parallel submission would be visible and unforgivable.
- [ ] Under consideration nowhere else.
- [ ] I typed `journals.tubitak.gov.tr` myself rather than following a link in an email (hijacked-journal defence — Turkish journals are disproportionately targeted).
- [ ] Article type is **Research Article**. *(Reviews are by invitation only — do not propose one.)*

## Gate 1 — the rebuild (this is not a reformat)

- [ ] Downloaded https://journals.tubitak.gov.tr/medical/Medical-Sciences-Templates-2026.rar and extracted both `.docx` files.
- [ ] Manuscript rebuilt **in `Medical Sciences Manuscript New Template_2026.docx`** — **"Manuscripts that are not prepared using the template will not be considered for publication."**
- [ ] **MS Word format. LaTeX is not accepted here.**
- [ ] Double-spaced, 3-cm margins, Times New Roman 12.
- [ ] **Page numbers AND line numbers** on.
- [ ] Length ≤ **30 pages** double-spaced, including references, figures and tables.
- [ ] Figures + tables ≤ **10 combined**. *(Currently 4 + 6 = 10 — exactly at the cap. Adding anything means removing something.)*
- [ ] References ≤ **60**. *(Currently 51.)*

## Gate 2 — abstract and keywords

- [ ] Abstract ≤ **300 words**. *(Current draft is 321 — must be cut.)*
- [ ] Abstract is **STRUCTURED** under four separate headings:
  - [ ] Background / Aim
  - [ ] Materials and methods
  - [ ] Results
  - [ ] Conclusion
- [ ] Keywords: **3 to 6**, no acronyms, **MeSH terms used where possible** (e.g. Burns; Deep Learning; Diagnosis, Computer-Assisted).

## Gate 3 — references (opposite rules to Elsevier and to TJEECS)

- [ ] CSE style (*Scientific Style and Format*, 7th ed.).
- [ ] Numbered in **square brackets**, in order of first appearance.
- [ ] Combined as `[2,6]`, **not** `[2],[6]`.
- [ ] **Journal titles spelled out IN FULL** — *not* abbreviated. (TJEECS requires Web-of-Science abbreviations; Elsevier requires LTWA abbreviations; TJMS requires full names. Do not carry one over.)
- [ ] ≤5 authors listed in full; 6 or more → first 5 + "et al."
- [ ] DOIs as full `https://doi.org/10.xxxx/xxxxx` URLs with **no "doi:" prefix**.

## Gate 4 — double-blind

- [ ] **Title page is a SEPARATE `.docx`**, built from `Medical Sciences Title page New Template_2026.docx`.
- [ ] Manuscript file contains **no author names and no affiliations** — TJMS states this explicitly: "Do not include author names or affiliations here."
- [ ] No acknowledgement of the supervisor in the manuscript file (it belongs on the title page).
- [ ] No repo URL, no institution name, no first-person self-citation in the manuscript file.
- [ ] **Word/PDF document metadata checked** — no author name or machine username.

## Gate 5 — declarations

**On the TITLE PAGE file:**
- [ ] Acknowledgment / disclaimers — **matching the CRediT roles entered in Editorial Manager exactly**.
- [ ] **Pre-print server / online repository** field — accurate (see `../../SUBMISSION_PLAYBOOK.md` §0.2). If a preprint exists, name it and give the link.
- [ ] Conflict of interest.

**In the MANUSCRIPT file:**
- [ ] **Data availability statement** (TÜBİTAK's APERTA repository, https://aperta.ulakbim.gov.tr/, is encouraged).
- [ ] **"Declaration of Generative AI and AI-assisted technologies"** — including the **model name and version** and the **exact prompt(s)**, the purpose, and which sections it was applied to. Not shortened.
- [ ] Funding (none — state it).
- [ ] Informed consent (not applicable — state why).

**In Editorial Manager:**
- [ ] **ORCID for all three authors** — "All authors are required to provide their ORCID iD during the submission process."
- [ ] CRediT roles entered, matching the title page word for word.

## Gate 6 — ethics (the sharpest edge at a medical journal)

- [ ] Ethics statement written: no human-subject involvement; secondary analysis of publicly available de-identified photographs; ethics committee approval not required.
- [ ] Dataset provenance and licences cited (Roboflow CC BY 4.0; BIP_US provided for research by the University of Seville).
- [ ] **Letter from the faculty ethics committee obtained** stating approval was not required. *(Not written into TJMS policy — there is no published exemption for public de-identified datasets — but worth the weeks it takes at a medical journal. Request it early.)*
- [ ] If uncertain, **emailed medsci@tubitak.gov.tr before submitting** to ask how they want a public-dataset AI study handled.
- [ ] BIP_US usage permission confirmed in writing, especially if any figure reproduces a BIP_US image.

## Gate 7 — the clinical reframe

- [ ] Leads with the **safety finding** (55 of 94 clinical images under-graded; half of full-thickness burns called first degree), not with the architecture comparison.
- [ ] Architecture benchmarking compressed — the scope caveat warns that papers "focusing on the technical details of a given medical subspeciality may not be evaluated."
- [ ] The 60–80% inter-rater agreement discussion expanded.
- [ ] Clinical depth vocabulary (superficial / superficial-partial / deep-partial / full thickness) used alongside degree terms.
- [ ] "Data leakage" explained in plain language at first use.
- [ ] Skin-tone / pigmentation limitation stated prominently.
- [ ] Extra length used to add back the expanded statistics and per-class results that TJEECS's 15-page cap forced out.

## Gate 8 — figures

- [ ] Re-exported from PDF into Word-compatible high-resolution raster formats (jpeg/tiff). *(TJEECS is PDF-only; TJMS is not.)*
- [ ] Embedded in the manuscript per the template's instructions.
- [ ] Readable in greyscale and by colour-blind readers.
- [ ] Any figure produced with a non-generative ML tool is disclosed **in its caption** (TÜBİTAK policy).

## Gate 9 — universal

- [ ] `../../SUBMISSION_PLAYBOOK.md` §2 worked through in full.
- [ ] All open items in §1.5 fixed.
- [ ] iThenticate similarity **under 25%** (>25% is "generally returned"; ≥50% may trigger a ban).

## Gate 10 — submitting

- [ ] Went to **https://www2.cloud.editorialmanager.com/turkjmedsci/default2.aspx** by typing it.
- [ ] Article type: **Research Article**.
- [ ] Uploaded: blinded manuscript (.docx) · **separate** title page (.docx) · figures · cover letter.
- [ ] Metadata entered: title, structured abstract, MeSH keywords, all three authors with ORCIDs and emails, CRediT roles, **preprint disclosure field**.
- [ ] **PDF proof built and read before approving.** Approval is the only irreversible step.
- [ ] Manuscript number recorded.
- [ ] Diarised — no published turnaround; the journal is bi-monthly. Chase after **3 months**, not before.

## Gate 11 — on decision

- [ ] Response letter follows `../../SUBMISSION_PLAYBOOK.md` §6, leading with the self-identified corrections in §6.4.
- [ ] **On acceptance:** diamond OA — nothing to pay, nothing to decline. Make the repo public, mint the Zenodo DOI, update the Data Availability statement, and confirm the supervisor's acknowledgement survives into the proof.
