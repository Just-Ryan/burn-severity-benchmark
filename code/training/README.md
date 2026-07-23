# Training code and notebooks

## Where the results actually live

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
├── build_clean_split.py        # first source-grouped, leak-free split
├── build_clean_split_v2.py     # split used for the final benchmarks (4 input conditions)
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

## Google Colab (Benchmark 2)

Benchmark 2 — segmentation training, the classifier retraining, the true end-to-end pipeline,
the external evaluations, and the timing table — was run on a **Google Colab A100** in a single
notebook, and is not yet mirrored here. Its outputs *are* archived in
[`../../benchmark2-proof/`](../../benchmark2-proof). To add the notebook itself:
**Colab → File → Download → Download .ipynb**, then drop it in as `colab-benchmark2.ipynb`.

## Compute environments

| Stage | Hardware | Pin |
|---|---|---|
| Benchmark 1 (masking ablation) | Kaggle NVIDIA **P100** | `torch==2.5.1 torchvision==0.20.1` (cu121) — newer builds drop the `sm_60` kernels the P100 needs |
| Benchmark 2 (segmentation, head-to-head, external, timing) | Google Colab **A100** | PyTorch 2.11, CUDA 12.8 |

This environment difference likely accounts for the retrained classifier accuracies sitting
about two percentage points below the earlier seed-42 Kaggle run.
