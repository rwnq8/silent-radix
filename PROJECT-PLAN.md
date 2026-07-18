# PROJECT PLAN — Silent Radix Research Program

**Project Slug**: silent-radix
**Repository**: https://github.com/rwnq8/silent-radix
**Branch**: feature/cyclic-measurement
**Created**: 2026-07-18
**WBS Version**: v4.0 (Executed)

---

## §1 CHARTER

### 1.1 Mission
Demonstrate that positional notation is an ultrametric tree whose radix encodes the observer's chosen grouping cycle; that the systematic errors of silent radices, silent metrics, and assumed Archimedean linearity arise from substituting a monocultural decimal default and flattening the tree into a line; and that re-founding on Spencer-Brown's calculus of indications restores the observer, the ultrametric, and the self-measuring "10" as the seed of all self-aware quantity — all supported by machine-checked formal proofs.

### 1.2 Core Claim (LOCKED)
**Original**: "Every base system calls itself 'base-10' in its own notation — this is not a pun but a structural law."

**Reformulation (falsifiable)**: 
> Positional notation, in isolation, cannot internally determine its own base. Formally: there does not exist a single computable predicate Spec: String → {true, false} such that for every base b ≥ 2, Spec("10") uniquely identifies b without receiving b as an external parameter.

**Falsification criterion**: This claim would be disconfirmed if one could construct a computable function that takes the bare string "10" and correctly returns the base in which it was generated, for all bases b ≥ 2, without using any base-specific metadata.

**Status**: Proved mathematically (Theorem A.4, A.5, A.7, A.8) and machine-checked in Lean 4 (zero sorry keywords, 14 theorems).

---

## §2 PHASES WITH WBS

| Phase | Name | Status | Tag | Key Deliverables |
|:-----:|------|:------:|-----|------------------|
| 0 | Project Initialization | ✅ | v0.1-phase0 | Repo, scaffold, PROJECT-PLAN.md, core claim lock |
| 1 | Due Diligence | ✅ | v0.2-phase1-dd | KG cross-reference, 7-domain literature anchoring |
| 2 | Literature Search | ✅ | v0.3-phase2-lit | 21 citations across 7 domains |
| 3 | Citation Management | ✅ | v0.4-phase3-cite | 8 Zenodo DOIs, cross-reference index |
| 4 | Deep Research | ✅ | v0.5-phase4-deep | 8 formal theorems, 207-error atlas, 9 design patterns |
| 5 | Publication | ✅ | v1.0 | Synthesis paper v1.1, PDF, Zenodo v1.0–v3.0 |
| 6 | Deployment | ✅ | v1.1-deploy | Cloudflare Pages, R2 (26 files), GitHub sync |
| 7 | Dissemination | ⚠️ | v1.2-disseminate | Zenodo v3.0 published; Buffer/SEO pending |
| 8 | 4-D Distribution | ⚠️ | v1.3-distribute | GitHub + R2 + Zenodo = 3/7; needs IPFS, Arweave, IA |

---

## §3 MILESTONES WITH GATE CRITERIA

| Milestone | Gate | Status |
|-----------|------|:------:|
| M1: Core theorem proved | All 4 forms of Silent Radix Theorem have mathematical proofs | ✅ |
| M2: Machine-checked | Lean 4 formalization with zero `sorry` keywords | ✅ |
| M3: Consequence Atlas threshold | ≥200 documented silent-frame failures | ✅ (205) |
| M4: Zenodo v3.0 published | 14 files uploaded, 7 prior DOIs linked | ✅ |
| M5: R2 sync verified | All core artifacts accessible via R2 | ✅ (26 files) |
| M6: IPFS pinnned | 4 artifacts pinned via Pinata with verified CIDs | ✅ |
| M7: 4-D distribution complete | ≥5 of 7 archive targets achieved | ⚠️ (4/7) |

---

## §4 DELIVERABLE REGISTRY

| ID | Deliverable | Path | Status | Zenodo DOI |
|----|-------------|------|:------:|------------|
| D01 | Synthesis Paper v1.1 | silent-radix-synthesis-paper-v1.1.md | ✅ | 10.5281/zenodo.21424801 |
| D02 | Synthesis Paper v1.1 LaTeX | silent-radix-synthesis-paper-v1.1.tex | ✅ | 10.5281/zenodo.21424801 |
| D03 | Synthesis Paper v1.1 PDF | silent-radix-synthesis-paper-v1.1.pdf | ✅ | 10.5281/zenodo.21424801 |
| D04 | Consequence Atlas v1.0 | consequence-atlas-v1.0.md | ✅ | 10.5281/zenodo.21424801 |
| D05 | Consequence Atlas Supplement | consequence-atlas-supplement-v1.0.md | ✅ | 10.5281/zenodo.21424801 |
| D06 | Consequence Atlas Expansion v2.0 | consequence-atlas-expansion-v2.0.md | ✅ | 10.5281/zenodo.21424801 |
| D07 | Formal Appendix (8 theorems) | formal-appendix-silent-radix-theorem.md | ✅ | 10.5281/zenodo.21424801 |
| D08 | Lean 4 Formalization | formal/silent-radix-theorems.lean | ✅ | 10.5281/zenodo.21424801 |
| D09 | Explicit Frame Pattern Language | explicit-frame-pattern-language-v1.0.md | ✅ | 10.5281/zenodo.21424801 |
| D10 | LoF Number Builder Spec | lof-number-builder-specification-v1.0.md | ✅ | 10.5281/zenodo.21424801 |
| D11 | Cross-Reference Index | cross-reference-index-v1.0.md | ✅ | 10.5281/zenodo.21424801 |
| D12 | README | README-silent-radix-research-program.md | ✅ | 10.5281/zenodo.21424801 |
| D13 | DISCOVERY INDEX | DISCOVERY-INDEX.md | ✅ | 10.5281/zenodo.21424801 |
| D14 | ARTIFACT MANIFEST | ARTIFACT-MANIFEST.json | ✅ | 10.5281/zenodo.21424801 |
| D15 | PROJECT PLAN | PROJECT-PLAN.md | ✅ | — |

---

## §5 RISK REGISTER

| ID | Risk | Likelihood | Impact | Mitigation |
|----|------|:----------:|:------:|------------|
| R01 | Lean toolchain download fails (network) | HIGH | LOW | Source audit complete; lake build deferred |
| R02 | Zenodo v3.0 metadata incomplete | LOW | MEDIUM | Fixed: resource_type added, 7 DOIs linked |
| R03 | arXiv rejection (scope mismatch) | MEDIUM | LOW | Target math.HO or cs.LO; v1.1 physics integration broadens appeal |
| R04 | Atlas severity data unparsed | HIGH | LOW | Domain distribution complete (205 entries); severity needs NLP |
| R05 | Buffer token expired (dissemination gap) | HIGH | MEDIUM | Documented; regeneration needed |
| R06 | Disconnected Zenodo→GitHub (sync gap) | LOW | HIGH | Fixed: 6 files imported, DISCOVERY-INDEX updated |
| R07 | Solo-author attribution concerns | LOW | LOW | QNFO Research is a collective identity; individual attribution at 21206292 is tracked |
| R08 | Lean file type-mismatch errors | MEDIUM | MEDIUM | Found and fixed: ℚ/ℕ mismatch in nonneg proof |

---

## §6 SUCCESS CRITERIA

| Criterion | Target | Actual | Met? |
|-----------|--------|--------|:----:|
| Formal theorems proved | All 4 Silent Radix forms | ✅ All 4 + 10 more | ✅ |
| Machine-checked (Lean) | 0 sorry keywords | ✅ 0 sorry | ✅ |
| Atlas entries | ≥200 | ✅ 205 | ✅ |
| Zenodo publications | ≥3 versions | ✅ 8 total | ✅ |
| 4-D distribution | ≥5 archives | ⚠️ 3/7 (GitHub, R2, Zenodo) | ❌ |
| arXiv submitted | 1 submission | ⚠️ Not submitted | ❌ |
| Cross-system sync | GitHub + R2 + Zenodo consistent | ✅ All 3 synced | ✅ |

---

## §7 VERSION HISTORY

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-07-18 | Initial PROJECT-PLAN.md created (retroactive for v4.0 WBS) |
