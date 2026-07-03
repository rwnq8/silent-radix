# ARCHITECTURE SPECIFICATION: Ultrametric FPGA Primitives

**Author:** QNFO Research Agent | **Date:** 2026-07-03 | **Status:** Draft v0.1
**Project:** fpga-ultrametric-cross-pollination | **Phase:** 2 — Formalization

---

## 1. Purpose

Define the instruction set, pipeline architecture, and memory hierarchy for an FPGA optimized for ultrametric and p-adic operations. This specification serves as:
- A formal target for Verilog/VHDL reference implementations
- A benchmark framework for comparing hardware vs. software ultrametric performance
- An architectural reference for QNFO's existing software-based Ultrametric Engine (Cloudflare Workers)

**Epistemic status:** `[speculative]` — these primitives are defined from first principles. No prior FPGA implementation of ultrametric-specific instructions is known to exist `[LLM-INFERRED — needs Phase 1 lit search verification]`. This specification is a design target, not a report on existing hardware.

**Architecture Compliance Gate:** `[BLOCKED: Architecture Compliance — FPGA is not Cloudflare-native. This specification is research-only. No production deployment on QNFO infrastructure.]`

---

## 2. Instruction Set Architecture (ISA)

### 2.1 Core Data Types

| Type | Width | Description |
|:-----|:------|:------------|
| `pval<k>` | `k × ceil(log₂ p)` bits | p-adic integer truncated to k digits, base p |
| `dnode` | 64 bits | Dendrogram node: {parent_ptr[32], depth[16], child_count[8], flags[8]} |
| `uleaf` | 128 bits | Ultrametric leaf: {feature_vector[96], energy[16], label[16]} |
| `dist` | 32 bits | Ultrametric distance (fixed-point, 16.16) |

### 2.2 Instruction Set

```
┌─────────────────────┬──────────────────────────────────────────────────────┐
│ Mnemonic             │ Operation                                            │
├─────────────────────┼──────────────────────────────────────────────────────┤
│ PADD  rd, ra, rb    │ p-adic addition: rd ← ra + rb (digit-serial, base p) │
│ PMUL  rd, ra, rb    │ p-adic multiplication: rd ← ra × rb                  │
│ PVAL  rd, ra        │ Compute p-adic valuation: rd ← v_p(ra)               │
│ PDIST rd, ra, rb    │ p-adic distance: rd ← p^{-v_p(ra - rb)}              │
│ PNORM rd, ra        │ p-adic absolute value: rd ← |ra|_p                   │
├─────────────────────┼──────────────────────────────────────────────────────┤
│ UDIST rd, ra, rb    │ Ultrametric distance: rd ← d(leaf[ra], leaf[rb])     │
│ ANC   rd, ra, rb    │ Nearest common ancestor: rd ← LCA(leaf[ra], leaf[rb])│
│ DEPTH rd, ra        │ Dendrogram depth: rd ← depth(leaf[ra])               │
│ BALL  rd, ra, rb    │ Ball query: rd ← all leaves within distance rb of ra │
│ NN    rd, ra        │ Nearest neighbor: rd ← argmin d(leaf[ra], leaf[j])   │
├─────────────────────┼──────────────────────────────────────────────────────┤
│ BWGT  rd, ra, rb    │ Braid word length: rd ← minimal σ crossings swap(a,b)│
│ BCOMP rd, ra, rb,rc │ Braid composition: rd ← braid[ra] ∘ braid[rb]       │
│ BARTIN rd, ra       │ Artin word length: rd ← |word(ra)| in generators     │
├─────────────────────┼──────────────────────────────────────────────────────┤
│ HENC  rd, ra        │ Hensel lift one step: a_{n+1} ← a_n - f(a_n)/f'(a_n)│
│ WTADD rd, ra, rb    │ Witt vector addition (digit-serial over Z_p)         │
│ WTMUL rd, ra, rb    │ Witt vector multiplication                           │
└─────────────────────┴──────────────────────────────────────────────────────┘
```

### 2.3 Instruction Encoding (24-bit)

```
┌──────────┬──────────┬──────────┬──────────┬──────────┐
│  opcode   │    rd    │    ra    │    rb    │   flags  │
│  6 bits   │  5 bits  │  5 bits  │  5 bits  │  3 bits  │
└──────────┴──────────┴──────────┴──────────┴──────────┘

Opcode map:
  000000  NOP
  000001  PADD    000010  PMUL    000011  PVAL
  000100  PDIST   000101  PNORM
  010000  UDIST   010001  ANC     010010  DEPTH
  010011  BALL    010100  NN
  100000  BWGT    100001  BCOMP   100010  BARTIN
  110000  HENC    110001  WTADD   110010  WTMUL
```

---

## 3. Pipeline Architecture

### 3.1 Overall Pipeline (5 stages)

```
FETCH → DECODE → EXECUTE → MEMORY → WRITEBACK
  │        │         │         │          │
  │        │         │         │          └─ Write result to register file
  │        │         │         └─ Dendrogram RAM / Leaf memory access
  │        │         └─ P-ADIC ALU / TREE ENGINE / BRAID ENGINE
  │        └─ Instruction decode, register read, hazard detection
  └─ Instruction memory (BRAM), PC increment
```

### 3.2 Execution Units

```
                    ┌──────────────┐
    Issue Queue ───►│ P-ADIC ALU   │──► p-adic add/mul/val/dist/norm
    (in-order)      │ (digit-serial)│    Latency: k cycles (k = precision digits)
                    └──────────────┘
                    ┌──────────────┐
    Issue Queue ───►│ TREE ENGINE  │──► UDIST, ANC, DEPTH, BALL, NN
                    │ (pipelined)  │    Latency: log₂(n) cycles (n = leaves)
                    └──────────────┘
                    ┌──────────────┐
    Issue Queue ───►│ BRAID ENGINE │──► BWGT, BCOMP, BARTIN
                    │ (FSM-based)  │    Latency: O(w²) cycles (w = word length)
                    └──────────────┘
```

### 3.3 Pipeline Hazard Handling

| Hazard | Detection | Resolution |
|:-------|:----------|:-----------|
| RAW (read after write) | Compare rd(EX/MEM/WB) with ra,rb(DEC) | Stall decode stage until writeback |
| Structural (shared TREE ENGINE) | Check execution unit busy flag | Stall issue until unit free |
| BRAID ENGINE multi-cycle | In-order completion only | All braid ops block until done |

---

## 4. Memory Hierarchy

### 4.1 Memory Map

```
┌──────────────────────────────────────────────────────────┐
│ Address Range      │ Size    │ Content                    │
├────────────────────┼─────────┼────────────────────────────┤
│ 0x0000_0000        │  64 KB  │ Instruction Memory (BRAM)  │
│ 0x0001_0000        │ 128 KB  │ Dendrogram Node RAM        │
│ 0x0003_0000        │ 256 KB  │ Leaf Feature RAM           │
│ 0x0007_0000        │  32 KB  │ Braid Group Scratchpad     │
│ 0x0007_8000        │   4 KB  │ Register File (32 × 128b)  │
│ 0x0007_9000        │   4 KB  │ p-adic Constant ROM        │
│ 0x0008_0000        │   1 MB  │ External HBM (optional)    │
└────────────────────┴─────────┴────────────────────────────┘
```

### 4.2 Dendrogram Node RAM Layout

Each node: 64 bits (8 bytes). Capacity: 16,384 nodes (128 KB).

```
┌────────────┬──────────┬──────────┬──────────┐
│ parent_ptr │  depth   │ children │  flags   │
│  32 bits   │ 16 bits  │  8 bits  │  8 bits  │
└────────────┴──────────┴──────────┴──────────┘

parent_ptr: 0 = root (no parent); index into node RAM
depth:      ultrametric distance from root (fixed-point 8.8)
children:   number of direct children (max 255)
flags:      bit 0 = is_leaf; bit 1 = is_root; bits 2-7 reserved
```

### 4.3 Leaf Feature RAM Layout

Each leaf: 128 bits (16 bytes). Capacity: 16,384 leaves (256 KB).

```
┌────────────────────┬──────────┬──────────┐
│   feature_vector    │  energy  │  label   │
│      96 bits        │ 16 bits  │ 16 bits  │
└────────────────────┴──────────┴──────────┘

feature_vector: embedding or tag encoding
energy:         E(m) ∝ d(m, m₀) — activation energy for recall
label:          class/category identifier
```

---

## 5. P-adic Arithmetic Unit Design

### 5.1 p-adic Addition (digit-serial)

For p-adic integers truncated to k digits:

```
Algorithm PADD(a[0..k-1], b[0..k-1], base p):
  carry ← 0
  for i = 0 to k-1:
    sum ← a[i] + b[i] + carry
    result[i] ← sum mod p
    carry ← sum ÷ p          // integer division
  return result[0..k-1]
```

**Hardware implementation:**
- k pipeline stages (one per digit)
- Each stage: ⌈log₂ p⌉-bit adder + modulo-p reducer (LUT-based)
- Throughput: 1 result per cycle after pipeline fill
- Latency: k cycles
- Resource estimate: k × (2 LUTs per adder bit + ~16 LUTs for mod-p)

### 5.2 p-adic Distance Computation

```
PDIST(a, b) = p^{-v_p(a - b)}

Hardware:
  1. PSUB: compute diff = a - b (digit-serial, k cycles)
  2. Leading-zero detect: find first non-zero digit → valuation v_p(diff)
  3. Table lookup: distance = precomputed[p - v_p(diff)]
```

**Falsifiability condition:** This would be disconfirmed if p-adic distance computation on FPGA is slower than software for k < 256. `[speculative]`

---

## 6. Tree Engine Design

### 6.1 Nearest Common Ancestor (ANC)

```
Algorithm ANC(leaf_a, leaf_b):
  ptr_a ← leaf_to_node[leaf_a]
  ptr_b ← leaf_to_node[leaf_b]
  // Align depths
  while depth[ptr_a] > depth[ptr_b]: ptr_a ← parent[ptr_a]
  while depth[ptr_b] > depth[ptr_a]: ptr_b ← parent[ptr_b]
  // Walk up together
  while ptr_a ≠ ptr_b:
    ptr_a ← parent[ptr_a]
    ptr_b ← parent[ptr_b]
  return ptr_a

Hardware: FSM with 2 read ports on dendrogram RAM
Latency: ≤ 2 × max_depth cycles ≈ 2 × 16 = 32 cycles for 65K leaves
```

### 6.2 Ball Query (BALL)

```
Algorithm BALL(center, radius):
  result_list ← empty
  for each leaf i:
    if UDIST(center, i) ≤ radius:
      result_list.append(i)
  return result_list

Hardware: Pipelined with leaf RAM read + comparator
Throughput: 1 comparison per cycle
Full scan latency: N cycles (N = leaf count)
```

### 6.3 Ultrametric Distance via Dendrogram

```
UDIST(leaf_a, leaf_b) = depth[ANC(leaf_a, leaf_b)]

This is the key property of ultrametric spaces: distance equals
the depth of the deepest common ancestor. For a dendrogram,
depth is the ultrametric distance from root.
```

---

## 7. Braid Engine Design

### 7.1 Braid Word Length (BWGT)

For the Braided Memory Register central conjecture (δ = c·w):

```
Algorithm BWGT(leaf_a, leaf_b):
  // Compute number of σ_i crossings to swap positions a and b
  // in the braid group B_n with standard generators
  if a > b: swap(a, b)
  // Minimum crossings = b - a (adjacent transpositions)
  // But restricted to "permitted" crossings (siblings at depth ≤ 1)
  return permitted_crossings(a, b)

permitted_crossings(a, b):
  count ← 0
  pos ← a
  while pos < b:
    if is_sibling(pos, pos+1):  // share parent at depth ≤ 1
      count ← count + 1
    pos ← pos + 1
  return count
```

**Validation target:** For the Braided Memory Register conjecture, compute BWGT for all pairs in a synthetic dendrogram and correlate with UDIST. R² > 0.9 supports the conjecture. `[speculative]`

### 7.2 Resource Estimates

| Component | LUTs | BRAM (36 Kb) | DSP | Latency |
|:----------|:-----|:-------------|:----|:--------|
| P-ADIC ALU (k=64, p=2) | ~800 | 0 | 0 | 64 cycles |
| TREE ENGINE | ~1,200 | 4 (128 KB) | 0 | 32 cycles |
| BRAID ENGINE | ~600 | 1 (32 KB) | 0 | O(w²) |
| Pipeline control + regfile | ~400 | 1 (4 KB) | 0 | — |
| **Total (minimal)** | **~3,000** | **6** | **0** | — |

Fits in a small FPGA (e.g., Xilinx Artix-7 XC7A35T: 33,280 LUTs, 100 BRAM blocks). `[LLM-INFERRED]`

---

## 8. Validation Suite

### 8.1 Correctness Tests

| Test | Description | Expected |
|:-----|:------------|:---------|
| `test_padd_identity` | a + 0 = a for random p-adic values | Bit-exact match with software |
| `test_pdist_ultrametric` | max(d(x,z), d(z,y)) ≥ d(x,y) | Strong triangle inequality holds |
| `test_anc_identity` | ANC(x,x) = x | Self-ancestor is self |
| `test_udist_symmetry` | UDIST(a,b) = UDIST(b,a) | Always true for any metric |
| `test_ball_monotonic` | BALL(x, r₁) ⊆ BALL(x, r₂) for r₁ ≤ r₂ | Monotonic inclusion |
| `test_bwgt_triangle` | w(x,z) ≤ w(x,y) + w(y,z) | Triangle inequality for braid words |

### 8.2 Performance Benchmarks

| Benchmark | Software (Python) | FPGA (target) | Speedup |
|:----------|:-----------------|:--------------|:--------|
| p-adic add (k=64, 10⁶ ops) | ~50 ms | ~5 ms @ 200 MHz | 10× |
| ANC query (16K leaves, 10⁶ queries) | ~200 ms | ~16 ms | 12.5× |
| BALL query (16K leaves, r=5) | ~100 ms | ~0.08 ms | 1,250× |
| BWGT (n=20, all pairs) | ~200 ms | ~20 μs | 10,000× |

`[speculative — targets, not measurements. Falsifiable by implementation.]`

---

## 9. Integration Points with QNFO Projects

| QNFO Project | FPGA Primitive Used | Validation |
|:-------------|:-------------------|:-----------|
| braided-memory-register | BWGT, UDIST | Correlate δ and w for n=20 synthetic dendrograms |
| number-theory-ultrametric-deep | PADD, PMUL, HENC, WTADD | Benchmark p-adic arithmetic for Pillars 3–4 |
| radix-uw-bt-synthesis | ANC, DEPTH, BALL | Traverse BT(2) and BT(3) buildings |
| ultrametric-engine | UDIST, ANC, BALL | Architectural reference vs. Worker JavaScript |

---

*Certainty: [speculative] throughout — this is a design target, not a report on existing hardware. [LLM-INFERRED] for resource estimates and performance targets. Falsifiable by implementation and benchmarking.*
