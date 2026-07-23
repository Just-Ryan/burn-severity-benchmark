# Training code and notebooks

## Start here: `colab-benchmark2.ipynb`

**This is the main experimental record**, and it is committed **with its execution outputs
intact** (14 of 15 code cells). Everything the article reports as Benchmark 2 was produced by
this one notebook on a Google Colab **A100**:

| § | What it does |
|---|---|
| 1–2 | Setup; mount and unzip the leak-free dataset |
| 3 | Train **Model 1** — single-class YOLOv8x-seg localiser (the pipeline front-end) |
| 4 | Train **Model 2** — three-class standalone YOLOv8x-seg |
| 5 | Evaluate segmentation; export results |
| 6–7 | Classifier data + **retrain and save** the two winning classifiers |
| 8 | **True end-to-end pipeline** (real localiser → predicted mask → Swin) |
| 9 | Head-to-head chart + YOLO figures |
| 10 | **External generalisation** on the clean 319-image set |
| 11 | **Robust pipeline** — low threshold + full-frame fallback |
| 12 | **Multi-seed robustness** (3 seeds) — the key comparison |
| 13 | Efficiency / timing table (per stage, A100) |
| 14 | Paired **McNemar** significance + export proof |
| 15 | Fairness fix — standalone YOLO at the same low threshold |

Sections 3 and 4 are **idempotent**: they skip training if a checkpoint already exists, so a
disconnected runtime can simply be re-run.

## Where the rest of the results live

**The notebooks in `kaggle-notebooks/` contain source only — no stored cell outputs.** They
were retrieved with the Kaggle API (`kaggle kernels pull`), which returns the kernel source
without its execution outputs. Rather than re-run them and paste in outputs that would not
correspond to any archived artifact, every number in the paper is recorded as machine-readable
evidence instead:

| What you want | Where it is |
|---|---|
| Every number reported in the article | [`../../benchmark2-proof/results/*.json`](../../benchmark2-proof/results) |
| Masking ablation, 11 architectures × 4 conditions, seed 42 | [`../../statistics/benchmark1_11arch_4cond_seed42.json`](../../statistics) |
| Segmentation curves, confusion matrices, head-to-head chart | [`../../benchmark2-proof/figures/`](../../benchmark2-proof/figures) |
| Per-image predictions (internal & external) | `../../benchmark2-proof/results/preds_internal.json`, `preds_external.json` |

Those JSON files *are* the outputs. They are the artifacts the paper's tables were computed
from, and they let anyone recompute a reported statistic without a GPU.

> ⚠️ **Provenance warning.** Several notebooks under `kaggle-notebooks/` predate the
> data-leakage correction and were run on the **naive file-level split**. Their accuracies are
> inflated and are retained only to document how the artifact arose. See
> [`../../statistics/DATA_LEAKAGE_FINDING.md`](../../statistics/DATA_LEAKAGE_FINDING.md).
> **Do not quote numbers from those notebooks as results.**

---

## Layout

```
training/
├── colab-benchmark2.ipynb      # ⭐ Benchmark 2, WITH outputs (A100) — see table above
├── build_clean_split.py        # first source-grouped, leak-free split
├── build_clean_split_v2.py     # split used for the final benchmarks (4 input conditions)
├── build_clean_yolo_seg.py     # builds the leak-free YOLO segmentation dataset
├── kaggle-notebooks/           # kernels pulled from Kaggle (source only, see above)
│   ├── yolo-seg1class/         # single-class localiser (pipeline front-end)
│   ├── yolo-seg3class/         # three-class standalone segmenter
│   ├── maskscnn/ nomaskscnn/   # masked vs unmasked classifier runs
│   ├── classificationskinburncnn/ skinburncnnonly/
│   └── detectionskinburnyolo/ skinburnyoloonly/   # Old-Way (detection→crop), superseded
└── newway-seqcode/             # segmentation/masking preprocessing
    ├── dtSplit.py  extractMasks.py  imageCNN.py  oneClassSeg.py
```

## The one file that matters most

`build_clean_split_v2.py` is the heart of the correction. It groups the ~3,424 augmented files
by their **1,370 source photographs**, keeps all augmented copies **train-only**, and
deduplicates validation and test to **one image per source** (seed 42, stratified by class).
Running it reproduces the exact split behind every leak-free number in the paper.

```bash
python build_clean_split_v2.py
```

## Running the Colab notebook yourself

Open `colab-benchmark2.ipynb` in Google Colab and select an **A100** runtime (Runtime →
Change runtime type → GPU). Two operational notes, learned the hard way:

- **Mount Drive by running the Setup cell yourself.** `drive.mount` opens an authorisation
  pop-up that has to be clicked; it cannot complete headlessly.
- **Keep the Colab tab in the foreground while training.** Colab disconnects backgrounded
  tabs, which killed one YOLO run at epoch 12. Because sections 3–4 are idempotent, a
  re-run resumes rather than retraining from scratch.

The dataset is read from Drive, so no Kaggle credentials are needed inside the notebook.

## Compute environments

| Stage | Hardware | Pin |
|---|---|---|
| Benchmark 1 (masking ablation) | Kaggle NVIDIA **P100** | `torch==2.5.1 torchvision==0.20.1` (cu121) — newer builds drop the `sm_60` kernels the P100 needs |
| Benchmark 2 (segmentation, head-to-head, external, timing) | Google Colab **A100** | PyTorch 2.11, CUDA 12.8 |

This environment difference likely accounts for the retrained classifier accuracies sitting
about two percentage points below the earlier seed-42 Kaggle run.
