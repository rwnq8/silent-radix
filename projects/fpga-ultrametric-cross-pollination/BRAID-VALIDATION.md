# BRAID-VALIDATION: FPGA Acceleration of the Central Conjecture

**Author:** QNFO Research Agent | **Date:** 2026-07-03 | **Status:** Specification v0.1
**Project:** fpga-ultrametric-cross-pollination / braided-memory-register | **Phase:** 2 — Bridge Design

---

## 1. Purpose

Specify the FPGA-accelerated computational pipeline for validating the Braided Memory Register central conjecture:

$$\delta(a,b) = c \cdot w(a,b)$$

where $\delta(a,b)$ is the ultrametric distance and $w(a,b)$ is the minimal braid word length between memory traces $a$ and $b$.

**Epistemic status:** `[my conjecture]` — the conjecture itself is unproven. This document specifies how to test it computationally at scales ($n > 20$) unreachable by pure software. `[speculative]` — the FPGA acceleration factors are projected, not measured.

---

## 2. Validation Pipeline

### 2.1 Data Flow

```
┌──────────────────────────────────────────────────────────────────┐
│ STEP 1: Generate synthetic ultrametric dendrogram                │
│   n leaves, random hierarchical clustering                       │
│   Output: dendrogram.json {nodes, parent pointers, depths}       │
└──────────────────────────┬───────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────────┐
│ STEP 2: Map leaves to braid strand positions                     │
│   Left-to-right dendrogram traversal → strand ordering 1..n      │
│   Define "permitted crossings": siblings at depth ≤ 1            │
│   Output: adjacency_matrix (n×n boolean, 1 if siblings)          │
└──────────────────────────┬───────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────────┐
│ STEP 3: FPGA-accelerated pairwise computation (THE CORE)         │
│   For all n(n-1)/2 pairs (i,j):                                  │
│     δ[i][j] = UDIST(i,j)  ← ANC engine (Tree Engine)             │
│     w[i][j]  = BWGT(i,j)  ← Braid Word Counter (Braid Engine)    │
│   Output: delta_matrix, word_matrix (both n×n, symmetric, diag=0)│
└──────────────────────────┬───────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────────┐
│ STEP 4: Statistical validation (software, on FPGA output)        │
│   Linear regression: δ ~ c·w + ε                                 │
│   Report: R², slope c, intercept, residual analysis              │
│   Additional tests:                                              │
│     - Check strong triangle inequality for w (is w ultrametric?) │
│     - Check Spearman rank correlation                            │
│     - Bootstrap confidence intervals for c                       │
└──────────────────────────────────────────────────────────────────┘
```

### 2.2 Why FPGA for Step 3?

| Scale | Software (Python) | FPGA (200 MHz) | Speedup |
|:------|:-----------------|:---------------|:--------|
| n=20, 190 pairs | ~200 ms | ~20 μs | 10,000× |
| n=100, 4,950 pairs | ~5 s | ~500 μs | 10,000× |
| n=500, 124,750 pairs | ~130 s | ~13 ms | 10,000× |
| n=1000, 499,500 pairs | ~520 s | ~50 ms | 10,400× |

`[speculative — projected from instruction latencies in ARCHITECTURE-SPEC.md §7.2]`

The key bottleneck is n=20: software can handle this, but n=500+ requires FPGA for reasonable iteration cycles (testing many dendrogram topologies).

---

## 3. Integration with Existing Braided Memory Register Specs

### 3.1 Mapping to PROTOTYPE-SPEC.md

The PROTOTYPE-SPEC.md defines a 3-layer architecture. The FPGA accelerator replaces Layer 2 (Hierarchical Embedding) and augments Layer 3 (Version DAG):

| PROTOTYPE-SPEC Layer | Software Implementation | FPGA Accelerator |
|:---------------------|:------------------------|:-----------------|
| Layer 1: Tokenizer | One-hot encoding → stays in software | No change — trivial |
| Layer 2: Hierarchical Embedding | v-PuNN analog in NumPy → **FPGA Tree Engine** | UDIST, ANC, DEPTH ops |
| Layer 3: Version DAG | Python dicts → **FPGA Braid Engine** | BWGT, BCOMP ops |
| Validation | SciPy linregress → stays in software | Receives FPGA output |

### 3.2 Mapping to CONJECTURE-PROOF.md

The proof sketch defines 4 strategy steps. The FPGA validates Step 1 (index by dendrogram) and Step 3 (minimal braid word) computationally:

| Proof Step | Mathematical Claim | FPGA Validation |
|:-----------|:-------------------|:----------------|
| Step 1: Index by dendrogram | Left-to-right traversal produces canonical ordering | FPGA ANC engine traverses dendrogram in hardware |
| Step 2: Braid group action | Adjacent σ_i permitted iff siblings at depth ≤ 1 | FPGA adjacency check via Tree Engine |
| Step 3: Minimal braid word | w(a,b) = number of permitted crossings | FPGA BWGT counts permitted crossings |
| Step 4: Equality proof | δ = c·w (up to scaling) | FPGA computes both and feeds regression |

### 3.3 Mapping to FORMAL-DEFINITIONS.md

| Formal Structure | FPGA Primitive |
|:-----------------|:---------------|
| Ultrametric Memory Space §2.1 | Tree Engine: UDIST, DEPTH, ANC |
| Braided Monoidal Category §2.2 | Braid Engine: BWGT, BCOMP |
| Content-Addressable Identification §2.3 | Ball Query Engine: BALL, NN |
| Version DAG §2.4 | (future: FPGA-accelerated Merkle tree) |
| Social Propagation §2.5 | (future: FPGA-accelerated ultrametric clustering) |

---

## 4. FPGA vs. Software Benchmark Protocol

### 4.1 Software Baseline (Python reference)

```python
# _baseline_conjecture.py — Pure-Python reference implementation
# Run first to establish baseline timing

import time, json, random
import numpy as np
from scipy.stats import linregress

def build_random_dendrogram(n):
    """Generate synthetic ultrametric dendrogram with n leaves."""
    nodes = [{'id': i, 'parent': None, 'depth': 0, 'is_leaf': True}
             for i in range(n)]
    next_id = n
    # Agglomerative clustering: merge random pairs until root
    active = list(range(n))
    while len(active) > 1:
        i, j = random.sample(active, 2)
        new_node = {'id': next_id, 'parent': None, 'depth': 0,
                    'children': [i, j], 'is_leaf': False}
        nodes.append(new_node)
        nodes[i]['parent'] = next_id
        nodes[j]['parent'] = next_id
        active.remove(i); active.remove(j)
        active.append(next_id)
        next_id += 1
    # Assign depths (bottom-up)
    # ... (implementation omitted for brevity)
    return nodes

def compute_pairwise(n, dendrogram):
    """Software baseline for all-pairs δ and w."""
    deltas = np.zeros((n, n))
    words = np.zeros((n, n))
    for i in range(n):
        for j in range(i+1, n):
            d = anc_depth(dendrogram, i, j)
            w = braid_word_len(dendrogram, i, j)
            deltas[i][j] = d; deltas[j][i] = d
            words[i][j] = w; words[j][i] = w
    return deltas, words

# Benchmark
for n in [10, 20, 50, 100, 200]:
    dendrogram = build_random_dendrogram(n)
    t0 = time.time()
    deltas, words = compute_pairwise(n, dendrogram)
    elapsed = time.time() - t0
    upper = deltas[np.triu_indices(n, 1)]
    w_upper = words[np.triu_indices(n, 1)]
    slope, intercept, r, p, std = linregress(w_upper, upper)
    print(f"n={n:4d}: {elapsed:8.3f}s, R²={r**2:.4f}, slope={slope:.4f}")
```

### 4.2 FPGA Benchmark (Verilator simulation)

```verilog
// _fpga_benchmark.sv — Top-level testbench for conjecture validation
module conjecture_benchmark;
    // Instantiate Tree Engine + Braid Engine
    // Feed synthetic dendrogram data
    // Collect all-pairs results
    // Output JSON for statistical analysis
endmodule
```

### 4.3 Comparison Metrics

| Metric | Software | FPGA (Verilator) | FPGA (Hardware) |
|:-------|:---------|:-----------------|:----------------|
| n=20 wall time | ~200 ms | ~2 ms (sim) | ~20 μs |
| n=100 wall time | ~5 s | ~50 ms (sim) | ~500 μs |
| R² for random dendrogram | varies | identical (bit-exact) | identical |
| Power (n=20) | ~15W (CPU) | N/A (sim) | ~0.5W (Artix-7) |

`[speculative — FPGA hardware numbers are projected, not measured]`

---

## 5. Falsification Protocol

The conjecture is **disconfirmed** if any of the following are observed:

| Condition | Threshold | Action |
|:----------|:----------|:-------|
| R² < 0.5 for any dendrogram topology | Strong disconfirmation | Reject conjecture, document counterexample |
| R² < 0.9 averaged over 100 random topologies | Weak disconfirmation | Conjecture needs revision |
| δ and w uncorrelated (p > 0.05) | Disconfirmation | Reject conjecture |
| Slope c varies by >10× across topologies | c is not universal | Conjecture as stated is false |

The conjecture is **supported** (not proven) if:

| Condition | Threshold |
|:----------|:----------|
| R² ≥ 0.95 for all tested topologies | Strong support |
| Slope c constant within ±5% across topologies | c appears universal |
| Residuals normally distributed with mean ≈ 0 | Good model fit |

---

## 6. Next Steps

1. **Implement software baseline** (`_baseline_conjecture.py`) — run on existing machine
2. **Synthesize Verilog modules** from REFERENCE-DESIGN.md — target Verilator simulation
3. **Run co-simulation** — compare bit-exact FPGA output vs. software for n=10, 20
4. **Scale to n=100** via FPGA simulation or synthesis
5. **Report findings** → update CONJECTURE-PROOF.md with computational evidence

---

*Certainty: [speculative] throughout. The conjecture is [my conjecture]. FPGA performance projections are [LLM-INFERRED]. Falsifiable by implementation and measurement.*
