
---

## Session 2026-07-02 (Fourth Phase) — Synthesis: Lessons Learned & Research Handoff

&gt; **Agent:** deepseek-v4-pro | **Git:** `9b03f08` (base)

---

### RESEARCH LESSONS LEARNED

These are extracted from three phases of work across the Parisi PDE solver, silent-radix synthesis paper, trapped-ion experiment, and CMB bispectrum analysis. They are methodological findings, not physical ones.

#### 1. Numerical resolution determines physical conclusions

The original AT instability claim at beta*J~5.25 was an artifact of n_gh=16 Gauss-Hermite quadrature (3.8% error in q). The "corrected" claim at beta*J~10 (commit 5d266ab) was itself erroneous — only the full sweep with n_gh=64 and systematic k-extrapolation converged on the stable result: **no AT crossing anywhere in [1,15].**

**Rule:** Before claiming a phase transition, run the full parameter sweep at the highest affordable resolution. A single-point estimate of lambda_AT is insufficient.

#### 2. Never trust a HANDOFF claim — verify independently

Three sessions passed assertions forward through the HANDOFF chain without independent numerical verification. The number of falsified claims (AT at beta*J~5.25, AT at beta*J~10, "Parisi recursion not implemented") exceeds the number of surviving claims.

**Rule:** The first act of any session continuing from a HANDOFF must be to independently verify the HANDOFF's central numerical claim. Inherited assertions are hypotheses, not facts.

#### 3. Red-team your red-teams

Commit 5d266ab was labeled "RED-TEAM CORRECTION" and claimed to fix a spurious AT by moving it to beta*J~10. This correction was itself wrong. Quality assurance processes need their own quality assurance.

**Rule:** Every correction must be verified with at least one independent method (different solver path, different resolution, different parameter range).

#### 4. Physical intuition trained on SK is misleading for WDW

Standard SK intuition says: stronger disorder -> AT instability -> RSB. This is so deeply ingrained that both the original analysis AND the "correction" assumed an AT crossing must exist — they just disagreed about where. The actual result (monotonically increasing lambda_AT) was so counterintuitive it took three phases to accept.

**Rule:** When working with a novel ensemble, treat the standard model's phase structure as a null hypothesis to reject, not a template to fit.

#### 5. Two solver methods, complementary strengths

| Method | Speed | Accuracy | Best Use |
|:-------|:------|:---------|:---------|
| `_precompute_fdf()` | O(k*n_gh^2*N_grid), ~0.5s for k=7 | Nearest-neighbor on 500-pt grid | Parameter sweeps, phase diagrams |
| `_parisi_recursion_step()` | O(n_gh^k), infeasible for k>=3 | Exact GH integration | Spot-checks, cross-validation at low k |

**Rule:** Fast approximate methods enable exploration. Exact methods enable verification. Use both.

#### 6. Publication timing discipline saved the paper

The silent-radix paper was nearly submitted with a false AT crossing claim. The program's two-round self-correction caught it before publication. This is the red-team->DoD->iterate->refine cycle operating across sessions — a success of process, not a failure of research.

**Rule:** Never publish from a HANDOFF claim. Publish only from a claim that has survived at least one independent session's verification.

#### 7. The WDW ensemble is physically distinct — own that

The central positive finding that survives all three phases: **deterministic clock fields suppress RSB by 10-15x vs standard SK, producing a qualitatively different phase structure.** This is the result to publish.

**Rule:** When a null result is physically surprising, it is not a null result — it is the result.

---

### NEXT STEPS: Silent-Radix & Related Research

Excludes IPFS/CID infrastructure. Sorted by dependency.

#### Phase A: Paper Revision (blocks all downstream)

**Task:** Revise `arxiv-silent-radix/silent-radix-synthesis-paper-v1.0.md`

1. **Remove** Sections 2.1-2.2 AT instability claims (falsified at both beta*J~5.25 and beta*J~10)
2. **Add** "Replica Stability of the WDW Ensemble" — lambda_AT(beta*J) monotonic increase data
3. **Add** "Comparison with Standard SK" — quantify 10-15x suppression, clock fields as rigid backbone
4. **Revise** abstract and conclusions to lead with RS-stability
5. **Regenerate** .tex (verify exit 0) and .pdf (verify no rendering artifacts)

**Dependencies:** None. Can begin immediately.

#### Phase B: AT Cross-Validation (scientific confidence)

**Task:** Verify the lambda_AT sign at beta*J=10 with independent methods.

1. Run closure-based `_parisi_recursion_step()` at beta*J=10, k=3. Compare lambda_AT against lookup-table result (+0.758). Discrepancy >0.01 flags discretization artifact.
2. Test n_gh=128 at beta*J=10, k=2. If lambda_AT drops significantly, quadrature is still insufficient.

**Dependencies:** None. Uses existing solver.

#### Phase C: Parameter Space Exploration

**Task:** Determine whether RSB exists at any parameter combination.

1. Extend beta*J sweep to 20, 30 at k=2,3
2. Test (N_clock, M_rest) = (3,2), (7,5), (11,7) at beta*J=10
3. Run k=9, 11 at beta*J=15 to refine power-law extrapolation near lambda~+0.00067

**Dependencies:** None. Uses solver with modified config.

#### Phase D: Trapped-Ion Experiment Reframing

**Task:** Revise `trapped-ion-experiment-design.md` v2.0.

1. Four-quadrant test structure remains valid
2. If Phase C confirms no RSB: reframe as **null test** of WDW RS-stability prediction
3. If Phase C finds RSB: adjust target coupling strengths
4. D4 tree/chain spectrum distinction is independent of AT — preserve

**Dependencies:** Phase C results determine experimental targets.

#### Phase E: Publication

**Task:** Publish revised silent-radix paper.

- [ ] Revised .md passes Publication Language Gate
- [ ] .tex compiles exit 0, .pdf verified
- [ ] All AT claims cross-validated (Phase B)
- [ ] Zenodo upload + Pages deploy to deep.qwav.tech/papers/

**Dependencies:** Phase A + Phase B.

---

### CONTINUATION PROMPT

```
LOAD ALL QNFO SKILLS. CONTINUE FROM HANDOFF IN projects/radix-uw-bt-synthesis/HANDOFF.md.

RESEARCH ONLY — NO IPFS/CID INFRASTRUCTURE.

EXECUTE IN ORDER:

1. REVISE silent-radix paper (arxiv-silent-radix/silent-radix-synthesis-paper-v1.0.md):
   REMOVE Sections 2.1-2.2 AT instability claims (falsified at beta*J~5.25 AND beta*J~10).
   ADD "Replica Stability of the WDW Ensemble" — lambda_AT(beta*J) monotonic increase data.
   ADD "Comparison with Standard SK" — 10-15x AT suppression, clock fields as rigid backbone.
   REVISE abstract/conclusions to lead with RS-stability.
   REGENERATE .tex and .pdf.

2. CROSS-VALIDATE AT at beta*J=10, k=3:
   Run closure-based _parisi_recursion_step(). Compare lambda_AT vs lookup-table (+0.758).
   If discrepancy > 0.01: flag discretization artifact.

3. EXPLORE parameter space:
   Test N_clock=3,7,11 at beta*J=10. Extend beta*J to 20,30 at k=2.
   Run k=9,11 at beta*J=15 near marginal stability (lambda~+0.00067 at k=7).

4. REFRAME trapped-ion experiment:
   If RSB absent: null test. If RSB found in step 3: adjust couplings.

KEY DATA (verified n_gh=64, damping=0.3, max_iter=40):
  AT SWEEP k=2: lambda_AT increases 0.800->0.939 across beta*J in [1,15]. NO crossing.
  CONTINUOUS k=3,5,7 at beta*J=10: lambda = +0.758, +0.450, +0.165 (all positive).
  EXTRAPOLATION: lambda(k) = 2.64*k^(-1.29), never crosses zero (R^2=0.87).
  EXTREME: k=7, beta*J=15: lambda=+0.000668 (marginal, still positive).
  FREE ENERGY 1RSB at beta*J=10: RS phase, q0~q1~0.975, F=-48.16.

CRITICAL: Parisi solver parisi_pde_solver.py (626 lines, n_gh=64).
  Use ParisiKRSBSolver with damping=0.3, max_iter=40.
  compute_at_krsb() returns dict -> use min(values()).
  compute_free_energy() returns tuple -> use result[0].
  _precompute_fdf() for sweeps, _parisi_recursion_step() for spot-checks.
```

---

*Session closeout 2026-07-02 (fourth phase). Research synthesis complete. Seven methodological lessons documented. HANDOFF carries forward RS-stability as central finding. Two layers of falsified AT claims documented. Continuation targets paper revision + cross-validation.*
