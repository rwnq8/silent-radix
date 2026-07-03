# FALSIFICATION REPORT: Central Conjecture δ = c · w

**Author:** QNFO Research Agent | **Date:** 2026-07-03 | **Status:** CONJECTURE DISCONFIRMED
**Project:** fpga-ultrametric-cross-pollination / braided-memory-register

---

## 1. Result

The central conjecture — that ultrametric depth δ equals braid word length w (up to a universal scaling constant c) — is **disconfirmed** by computational testing on random ultrametric dendrograms.

| n | Topologies | R² (mean ± std) | Slope c (mean ± std) | Verdict |
|:--|:-----------|:----------------|:---------------------|:--------|
| 10 | 20 | 0.0114 ± 0.0165 | 0.08 ± 0.12 | **DISCONFIRMED** |
| 20 | 20 | 0.0046 ± 0.0054 | 0.13 ± 0.09 | **DISCONFIRMED** |
| 50 | 20 | 0.0033 ± 0.0047 | -0.22 ± 0.09 | **DISCONFIRMED** |

**All 60 topologies produced R² < 0.09.** The highest single-topology R² was 0.0821 (n=10). There is no linear relationship between δ and w under the permitted-crossings model.

---

## 2. Why the Conjecture Fails

### 2.1 The "Permitted Crossings" Model is Too Sparse

The braid word length w(a,b) counts only adjacent transpositions where the two strands are **siblings** in the dendrogram. For random dendrograms:

- Most adjacent leaf pairs in the left-to-right ordering are NOT siblings
- Therefore w=0 for the vast majority of pairs
- δ varies broadly (0 to max_depth) but w stays near 0 for most pairs → zero correlation

Example from n=10, seed=42:
```
δ distribution: [0, 1, 2, 3] (uniform-ish)
w distribution:  [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, ...] (mostly 0)
```

The permitted-crossings restriction is too strong — it doesn't capture the hierarchical structure that the conjecture needs.

### 2.2 The "Permission" Condition is Arbitrary

The conjecture assumed crossings are permitted only for siblings at depth ≤ 1. But the dendrogram's hierarchical structure is richer than that — any two leaves at distance δ share a common ancestor at depth δ, which may involve many intermediate clusters. The restriction to direct siblings ignores this multi-level structure.

---

## 3. What Survives

The falsification does NOT invalidate the Braided Memory Register project. It only falsifies the **specific formulation** δ = c·w under the permitted-crossings model. The broader hypothesis — that ultrametric structure and braided structure are related — remains viable.

### 3.1 Alternative Formulations (from CONJECTURE-PROOF.md §4)

These weaker conjectures should be tested next:

| Conjecture | Statement | Status |
|:-----------|:----------|:-------|
| **C1** (strong, original) | δ = c·w for permitted crossings | ❌ DISCONFIRMED |
| **C2** (rank preservation) | δ(a,b) < δ(c,d) ⇔ w(a,b) < w(c,d) | Untested |
| **C3** (monotonic) | w non-decreasing with δ (but not necessarily linear) | Untested |
| **C4** (unrestricted crossings) | δ = c·w where w counts ALL adjacent transpositions (not just permitted) | Untested |
| **C5** (minimum dendrogram distance) | w(a,b) equals number of dendrogram edges on shortest path | Untested |

### 3.2 What to Try Next

1. **Test C4:** Remove the permitted-crossings restriction. Count ALL adjacent transpositions to swap positions a and b. This should correlate with leaf ordering distance, which may correlate with dendrogram depth.
2. **Test C5:** Use dendrogram edge-count distance (shortest path in the dendrogram graph) instead of depth.
3. **Test C2:** Use Spearman rank correlation (already computed; check if ρ > 0 even if R² ≈ 0).

---

## 4. Impact on FPGA Acceleration

The FPGA accelerator designs remain valid — they compute δ and w as defined. The falsification just means:
- The specific validation target (δ = c·w) is not worth building hardware for
- If C4 or C5 is confirmed, the FPGA designs can be adapted to count unrestricted crossings or edge distances
- The P-ADIC ALU and TREE ENGINE modules are still useful for other QNFO projects (number-theory-ultrametric-deep, radix-uw-bt-synthesis)

---

## 5. What This Means for the Braided Memory Register

**The falsification is a feature, not a bug.** The project's CONJECTURE-PROOF.md explicitly listed falsification conditions. The computational result provides empirical evidence that sharpens the conjecture. The project should:

1. **Revise the conjecture** to one of the alternative formulations (C4 or C5 most promising)
2. **Re-run validation** with the revised definition of w
3. **Update the proof sketch** to reflect which relationship is actually supported

**The Braided Memory Register project is NOT invalidated.** Only one specific mathematical formulation of the ultrametric-braid connection has been falsified. The broader consilience program — connecting ultrametric topology, braided categories, content-addressable memory, DAG versioning, and social propagation — remains viable.

---

## 6. Evidence

- **Script:** `_baseline_conjecture.py` — run to reproduce
- **Results:** `_conjecture_results.json` — full per-topology data
- **p-adic tests:** `_padic_arithmetic.py` — 20/20 PASS (ultrametric triangle inequality verified independently)

---

*Certainty: [CODE-EXECUTED] — results produced by Python execution on 2026-07-03. Reproducible by re-running `_baseline_conjecture.py`.*
