#!/usr/bin/env python3
"""
Recompute every headline number in the paper from the committed raw data.

    python verify_paper_numbers.py

Requires: scipy, numpy.  Reads only files in this repository — no GPU, no dataset,
no model weights.  Each check prints the value recomputed from raw data next to the
value printed in the manuscript, and PASS/FAIL.

This exists so a reviewer can confirm the paper's arithmetic in under a minute.
"""
import json
import math
import os
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "benchmark2-proof", "results")
STA = os.path.join(HERE, "statistics")

try:
    import numpy as np
    from scipy import stats
except ImportError:
    sys.exit("needs numpy and scipy:  pip install numpy scipy")

results = []


def check(label, got, want, tol=0.02, note=""):
    ok = abs(got - want) <= tol
    results.append(ok)
    flag = "PASS" if ok else "FAIL"
    print(f"  [{flag}] {label:<52} recomputed={got:>9.4f}   paper={want:<9} {note}")


def load(path):
    with open(path) as fh:
        return json.load(fh)


# ---------------------------------------------------------------- leakage artifact
print("\n=== 1. THE LEAKAGE ARTIFACT (naive file-level split, 21 architectures) ===")
leaky = load(os.path.join(STA, "benchmark0_LEAKY_21arch_naive_split.json"))
d = [r["delta_pp"] for r in leaky["per_architecture"]]
check("masking benefit under the leaky split (pp)", sum(d) / len(d), 3.06)
check("architectures that appeared to improve", sum(1 for x in d if x > 0), 20, tol=0)
print("         (these accuracies are inflated by leakage and are NOT results)")

# ---------------------------------------------------------------- masking null
print("\n=== 2. THE MASKING NULL ON THE LEAK-FREE SPLIT ===")
s42 = load(os.path.join(STA, "benchmark1_11arch_4cond_seed42.json"))
by42 = defaultdict(dict)
for e in s42:
    by42[e["arch"]][e["cond"]] = e["acc"]
d42 = [v["masked"] - v["unmasked"] for v in by42.values() if "masked" in v and "unmasked" in v]
check("seed-42 masking effect, 11 architectures (pp)", float(np.mean(d42)), 1.5, tol=0.06)

TRANSFORMERS = {"SWIN-Tiny", "SWIN-Small", "SWIN-Base", "SWIN-Large", "ViT-Base"}
t42 = [by42[a]["masked"] - by42[a]["unmasked"] for a in by42 if a in TRANSFORMERS]
check("seed-42 effect, transformers only (pp)", float(np.mean(t42)), 3.1, tol=0.06)
check("transformers that improved at seed 42", sum(1 for x in t42 if x > 0), 5, tol=0)

conf = load(os.path.join(STA, "benchmark1_masking_seeds01_confirmation.json"))
byc = defaultdict(dict)
for e in conf:
    byc[(e["arch"], e["seed"])][e["cond"]] = e["acc"]
archs8 = sorted({a for (a, _) in byc})
pooled, tr, cv = [], [], []
for a in archs8:
    for s in (0, 1):
        v = byc.get((a, s), {})
        if "masked" in v and "unmasked" in v:
            x = v["masked"] - v["unmasked"]
            pooled.append(x)
            (tr if a in TRANSFORMERS else cv).append(x)
    if "masked" in by42[a] and "unmasked" in by42[a]:
        x = by42[a]["masked"] - by42[a]["unmasked"]
        pooled.append(x)
        (tr if a in TRANSFORMERS else cv).append(x)

check("pooled effect over seeds 0, 1, 42 (pp)", float(np.mean(pooled)), 0.55)
check("architecture-seed pairs pooled", len(pooled), 24, tol=0)
check("pairs that improved", sum(1 for x in pooled if x > 0), 13, tol=0)
check("Wilcoxon signed-rank p", float(stats.wilcoxon(pooled, zero_method="pratt").pvalue), 0.32)
mw1 = float(stats.mannwhitneyu(tr, cv, alternative="greater").pvalue)
mw2 = float(stats.mannwhitneyu(tr, cv).pvalue)
check("Mann-Whitney transformer vs conv (ONE-sided)", mw1, 0.33)
print(f"         note: the two-sided value is {mw2:.4f}; the manuscript reports the one-sided figure")
print("         and should state the sidedness explicitly. Both are null, so no conclusion changes.")

# ---------------------------------------------------------------- head to head
print("\n=== 3. HEAD-TO-HEAD (multi-seed, seeds 0, 1, 2) ===")
ms = load(os.path.join(RES, "multiseed_results.json"))
for key, want_mean, want_sd, name in [
    ("clf_int", 82.6, 0.6, "classifier, internal"),
    ("pipe_int", 78.9, 0.8, "pipeline,   internal"),
    ("clf_ext", 76.6, 1.3, "classifier, external"),
    ("pipe_ext", 73.4, 2.0, "pipeline,   external"),
]:
    check(f"{name} mean (%)", ms[key]["mean"], want_mean, tol=0.06)
    check(f"{name} SD", ms[key]["sd"], want_sd, tol=0.06)

wins = sum(
    1 for i in range(3)
    if ms["clf_int"]["seeds"][i] > ms["pipe_int"]["seeds"][i]
    and ms["clf_ext"]["seeds"][i] > ms["pipe_ext"]["seeds"][i]
)
check("seeds where the classifier wins BOTH sets", wins, 3, tol=0)

# ---------------------------------------------------------------- paired tests
print("\n=== 4. PAIRED SIGNIFICANCE, RECOMPUTED FROM PER-IMAGE PREDICTIONS ===")


def mcnemar_exact(rows):
    b = sum(1 for r in rows if r["clf"] == r["true"] and r["pipe"] != r["true"])
    c = sum(1 for r in rows if r["clf"] != r["true"] and r["pipe"] == r["true"])
    n = b + c
    if n == 0:
        return b, c, 1.0
    p = 2 * sum(math.comb(n, k) for k in range(min(b, c) + 1)) / 2 ** n
    return b, c, min(p, 1.0)


for fn, name, wb, wc, wp in [
    ("preds_internal.json", "internal", 20, 18, 0.87),
    ("preds_external.json", "external", 54, 40, 0.18),
]:
    rows = load(os.path.join(RES, fn))
    b, c, p = mcnemar_exact(rows)
    check(f"McNemar {name}: classifier-only correct", b, wb, tol=0)
    check(f"McNemar {name}: pipeline-only correct", c, wc, tol=0)
    check(f"McNemar {name}: exact p", p, wp, tol=0.005)

# ---------------------------------------------------------------- segmentation etc
print("\n=== 5. SEGMENTATION, ORACLE, PIPELINE VARIANTS, TIMING ===")
b2 = load(os.path.join(RES, "benchmark2_results.json"))
check("1-class localiser test mask mAP50", b2["1class"]["test_mask_map50"], 0.726, tol=0.001)
check("3-class standalone test mask mAP50", b2["3class"]["test_mask_map50"], 0.603, tol=0.001)

clf = load(os.path.join(RES, "classifier_results.json"))
check("oracle Swin-Tiny on ground-truth masks (%)", clf["swin_tiny_masked"]["test_acc"], 83.9, tol=0.06)

rob = load(os.path.join(RES, "robust_pipeline_results.json"))
check("robust pipeline, internal, seed 42 (%)", rob["internal"]["robust_pipeline_acc"], 81.5, tol=0.06)
check("robust pipeline, external, seed 42 (%)", rob["external"]["robust_pipeline_acc"], 69.9, tol=0.06)

strict = load(os.path.join(RES, "true_pipeline_results.json"))
check("strict pipeline, internal (%)", strict["true_pipeline_test_acc"], 79.0, tol=0.06)

tim = load(os.path.join(RES, "timing_results.json"))
check("full pipeline latency (ms)", tim["Full pipeline (loc->mask->Swin)"], 42.3, tol=0.06)
check("ConvNeXt-Large latency (ms)", tim["ConvNeXt-L classifier"], 25.8, tol=0.06)

# ---------------------------------------------------------------- confusion matrices
print("\n=== 6. CONFUSION MATRICES (Figure 3) SUM TO N ===")
for fn, n, name in [("preds_internal.json", 205, "internal"), ("preds_external.json", 319, "external")]:
    rows = load(os.path.join(RES, fn))
    check(f"{name} confusion matrix total", len(rows), n, tol=0)

# ---------------------------------------------------------------- external clinical
print("\n=== 7. BIP_US CLINICAL EXTERNAL VALIDATION ===")
bip = load(os.path.join(STA, "external_validation_BIPUS.json"))
rowsb = bip["rows"]
check("BIP_US images", len(rowsb), 94, tol=0)
per = defaultdict(lambda: [0, 0])
for r in rowsb:
    gt = "Second" if r["depth"] == "Superficial dermal" else ("Second" if r["depth"] == "Deep dermal" else "Third")
    per[gt][1] += 1
    if r["pred_pipeline"] == gt:
        per[gt][0] += 1
bal = 100 * sum(c / n for c, n in per.values()) / len(per)
check("balanced accuracy, deep-dermal->2nd (%)", bal, 30.5, tol=0.2)


# ---------------------------------------------------------------- v2 additions
print("\n=== 8. STATISTICS ADDED IN THE REVISED MANUSCRIPT (v2) ===")
ms2 = load(os.path.join(RES, "multiseed_results.json"))
for key, name in [("clf_int", "classifier internal"), ("pipe_int", "pipeline internal"),
                  ("clf_ext", "classifier external"), ("pipe_ext", "pipeline external")]:
    v = np.array(ms2[key]["seeds"])
    print(f"         {name:<22} sample SD (n-1) = {v.std(ddof=1):.2f}   "
          f"[the archived JSON stores the population SD {v.std(ddof=0):.2f}]")
print("         v2 reports the sample SD; the originally submitted version reported the population SD.")

for a, b, nm, wm, wlo, whi in [
    ("clf_int", "pipe_int", "internal", 3.74, 3.04, 4.44),
    ("clf_ext", "pipe_ext", "external", 3.24, -3.83, 10.31),
]:
    d = np.array(ms2[a]["seeds"]) - np.array(ms2[b]["seeds"])
    ci = stats.t.interval(0.95, len(d) - 1, loc=d.mean(), scale=stats.sem(d))
    check(f"paired classifier-minus-pipeline, {nm} (pp)", float(d.mean()), wm, tol=0.02)
    check(f"  its 95% CI lower bound, {nm}", float(ci[0]), wlo, tol=0.02)
    check(f"  its 95% CI upper bound, {nm}", float(ci[1]), whi, tol=0.02)

pooled = [r["delta_pp"] for r in load(os.path.join(STA, "benchmark1_masking_pooled_analysis.json"))["per_run"]]
ci = stats.t.interval(0.95, len(pooled) - 1, loc=np.mean(pooled), scale=stats.sem(pooled))
check("masking effect 95% CI lower bound (pp)", float(ci[0]), -0.37, tol=0.02)
check("masking effect 95% CI upper bound (pp)", float(ci[1]), 1.47, tol=0.02)

print("\n=== 9. CLASS-CONDITIONED GRADING BIAS (v2 Section 4.7) ===")
for fn, nm, wu, wo in [("preds_internal.json", "internal", 19.3, 10.1),
                       ("preds_external.json", "external", 28.3, 15.2)]:
    rows = load(os.path.join(RES, fn))
    ug = sum(1 for r in rows if r["true"] > 0)
    og = sum(1 for r in rows if r["true"] < 2)
    u = 100 * sum(1 for r in rows if r["pipe"] < r["true"]) / ug
    o = 100 * sum(1 for r in rows if r["pipe"] > r["true"]) / og
    check(f"{nm}: under-graded, of images that could be (%)", u, wu, tol=0.1)
    check(f"{nm}: over-graded, of images that could be (%)", o, wo, tol=0.1)


print("\n=== 10. SEED-VARIANCE REPLICATION (v2 Section 4.9 / Table 7) ===")
sv = load(os.path.join(STA, "seed_variance_7seed_replication.json"))
import itertools
for key, wsd, wmin, wmax in [
    ("convnext_large|unmasked", 1.40, 0.28, 2.25),
    ("swin_tiny_patch4_window7_224|masked", 0.79, 0.00, 1.13),
]:
    g = sv["groups"][key]
    a = np.array(g["acc"])
    check(f"{key.split('|')[0][:20]}: seeds run", g["n_seeds"], 7, tol=0)
    check(f"{key.split('|')[0][:20]}: sample SD over 7 seeds", float(a.std(ddof=1)), wsd, tol=0.02)
    sub = [float(np.array(c).std(ddof=1)) for c in itertools.combinations(a, 3)]
    check(f"{key.split('|')[0][:20]}: min SD from any 3 seeds", min(sub), wmin, tol=0.02)
    check(f"{key.split('|')[0][:20]}: max SD from any 3 seeds", max(sub), wmax, tol=0.02)
print("         The paper reports 0.75 from three seeds; the seven-seed value is 1.40.")
print("         This is the basis for the claim that a three-seed SD is uninformative.")


print("\n=== 11. TEN-SEED PAIRED HEAD-TO-HEAD (v2 Section 4.5 / Table 8) ===")
h = load(os.path.join(STA, "h2h_10seed_paired.json"))
A = {x["seed"]: x for x in h if x["arm"] == "A_classifier"}
B = {x["seed"]: x for x in h if x["arm"] == "B_pipeline"}
common = sorted(set(A) & set(B))
check("paired seeds completed", len(common), 10, tol=0)
for nm, k, wd, wlo, whi, wp, wins in [
    ("internal", "int_acc", 2.63, 0.29, 4.98, 0.0316, 7),
    ("external", "ext_acc", 2.79, 1.09, 4.49, 0.0048, 9),
]:
    a = np.array([A[s][k] for s in common]); b = np.array([B[s][k] for s in common]); d = a - b
    ci = stats.t.interval(0.95, len(d) - 1, loc=d.mean(), scale=stats.sem(d))
    check(f"{nm}: paired difference (pp)", float(d.mean()), wd, tol=0.02)
    check(f"{nm}: CI lower", float(ci[0]), wlo, tol=0.02)
    check(f"{nm}: CI upper", float(ci[1]), whi, tol=0.02)
    check(f"{nm}: paired t p", float(stats.ttest_rel(a, b).pvalue), wp, tol=0.002)
    check(f"{nm}: seeds the classifier wins", int((d > 0).sum()), wins, tol=0)

print("\n=== 12. SEED VARIANCE OVER TEN SEEDS (v2 Section 4.9 / Table 7) ===")
import itertools
for arm, nm, wsd, wmin, wmax in [("A_classifier", "classifier", 1.74, 0.00, 3.25),
                                 ("B_pipeline", "pipeline", 2.22, 0.28, 3.69)]:
    a = np.array([x["int_acc"] for x in sorted([y for y in h if y["arm"] == arm], key=lambda z: z["seed"])])
    sub = [float(np.array(c).std(ddof=1)) for c in itertools.combinations(a, 3)]
    check(f"{nm}: sample SD over 10 seeds", float(a.std(ddof=1)), wsd, tol=0.02)
    check(f"{nm}: min SD from any 3 seeds", min(sub), wmin, tol=0.02)
    check(f"{nm}: max SD from any 3 seeds", max(sub), wmax, tol=0.02)
print("         Three seeds reported 0.75 and 1.02. Ten seeds give 1.74 and 2.22.")
print("         Some three-seed subsets give exactly zero, purely by chance.")

# ---------------------------------------------------------------- summary
print("\n" + "=" * 78)
n_ok, n = sum(results), len(results)
print(f"  {n_ok}/{n} checks passed")
print("=" * 78)
sys.exit(0 if n_ok == n else 1)
