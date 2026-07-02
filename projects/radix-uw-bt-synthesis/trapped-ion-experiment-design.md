# Trapped-Ion Page-Wootters Experiment: Testing Ultrametricity with Tree vs. Chain Clock Spectra

> **Author:** QNFO Research | **Date:** 2026-07-02 (rebuilt v2.0) | **Part of:** Radix→BT Synthesis — GAP-EXPT-001
> **Correction:** Incorporates D4 sufficient condition refinement (tree vs. chain spectrum distinction, §5.2 of silent-radix v1.2)

---

## Abstract

We propose an updated protocol for the trapped-ion Page-Wootters experiment, incorporating the D4 sufficient-condition refinement: diagonal clock-rest coupling $\hat{H}_{CR}$ produces exact ultrametric conditional state overlaps ($\text{UVR}=0\%$) **only when combined with a tree-structured clock spectrum** (pairwise-clustered energy levels). A chain spectrum (e.g., $E_k \propto 3^{-k}$) with diagonal coupling produces a specific counterexample $Q_{13} < \min(Q_{12}, Q_{23})$ — a finite UVR despite diagonality. Nondiagonal coupling produces the universal $\sim 32\%$ violation rate regardless of spectrum type. The experiment is redesigned with **two distinct clock spectrum configurations** — tree-structured and chain — enabling a decisive four-quadrant test of the corrected theory.

---

## 1. Physical Implementation

### 1.1 System

| Component | Physical Realization | Parameters (Yb$^+$) |
|:----------|:---------------------|:---------------------|
| Clock system $\hat{H}_C$ | $N$ hyperfine/Zeeman sublevels | $N = 6$, $E_k$ tunable via Zeeman splitting |
| Rest system $\hat{H}_R$ | $M$ motional Fock states | $M = 4$, $\omega_z \approx 2\pi \times 1\,\text{MHz}$ |
| Coupling $\hat{H}_{CR}$ | Laser-driven carrier/sideband transitions | Rabi frequency $\Omega_{k,n} \to \Omega_{k,n'}$ tunable |

### 1.2 Hamiltonian

The total Page-Wootters Hamiltonian for the clock+rest system:

$$\hat{H} = \hat{H}_C \otimes \mathbb{I}_R + \mathbb{I}_C \otimes \hat{H}_R + \hat{H}_{CR}$$

with:
- $\hat{H}_C = \sum_{k=0}^{N-1} E_k |k\rangle\langle k|$ (clock spectrum — **the key design parameter**)
- $\hat{H}_R = \sum_{n=0}^{M-1} n\omega_z |n\rangle\langle n|$ (motional ladder)
- $\hat{H}_{CR}$ engineered via laser interactions (see §1.3)

The WDW constraint $\hat{H}|\Psi\rangle = 0$ defines the physical Hilbert space. We implement this by post-selecting on total energy $E_{\text{tot}} = 0$ via an auxiliary verification qubit.

### 1.3 Clock-Rest Interaction Engineering

| Coupling Type | Laser Configuration | $\hat{H}_{CR}$ Form | Matrix Structure |
|:-------------|:-------------------|:-------------------|:-----------------|
| **Diagonal** | Carrier (no motional change) | $\sum_{k,n} g_{k,n} |k,n\rangle\langle k,n|$ | Block-diagonal in $|k\rangle$ |
| **Nondiagonal** | 1st-order red/blue sideband | $\sum_{k,\ell,n} g_{k\ell,n} |k,n\rangle\langle \ell,n\pm 1|$ | Off-diagonal in $|k\rangle$, $|n\rangle$ |

The diagonal configuration uses only carrier transitions that preserve the motional state. The nondiagonal configuration adds sideband transitions that couple different clock states through motional exchange — the source of replica symmetry breaking.

**Tunability:** By adjusting laser detunings and powers, the strength of off-diagonal coupling $\epsilon = ||\hat{H}_{CR}^{\text{off-diag}}|| / ||\hat{H}_{CR}^{\text{diag}}||$ is continuously tuned from $\epsilon = 0$ (pure diagonal) to $\epsilon \approx 0.3$ (strong nondiagonal).

---

## 2. Clock Spectrum Engineering: Tree vs. Chain

**This is the central design update reflecting the D4 correction (silent-radix v1.2, §5.2).**

### 2.1 Tree-Structured Spectrum (UVR → 0 prediction)

The tree spectrum encodes hierarchical clustering: states with a *recent* common ancestor in the tree have close energies. For $N = 6 = 2 \times 3$, a depth-2 tree:

**Configuration A — p-adic tree ($p=2$, depth $d=2$):**

| Level | States | Energies $E_k$ | Commentary |
|:------|:-------|:---------------|:-----------|
| $q_0$ (base) | $\{0,1,2,3,4,5\}$ | $\{0, 0+\delta, \Delta, \Delta+\delta, 2\Delta, 2\Delta+\delta\}$ | Pairwise clustering |
| $q_1$ (pairs) | $\{0,1\}$, $\{2,3\}$, $\{4,5\}$ | pairs separated by $\Delta$ | Three branches at depth 1 |
| $q_2$ (all) | $\{0,\ldots,5\}$ | all states | Root at depth 2 |

**Example parameters (Hz):**
$$\{E_0, E_1, E_2, E_3, E_4, E_5\} = \{0, 50, 500, 550, 1000, 1050\}$$

where $\delta = 50$ Hz (intra-pair splitting) and $\Delta = 500$ Hz (inter-pair splitting).

**Experimental implementation:** Use two Zeeman sublevel manifolds: adjacent $m_F$ states within the same $F$ manifold have small splitting ($\delta$); states in different $F$ manifolds have large splitting ($\Delta$). The tree structure emerges from the $|F, m_F\rangle$ hyperfine structure.

**Prediction:** Tree spectrum + diagonal $\hat{H}_{CR}$ → $\text{UVR} = 0\%$ (exact ultrametricity, within tomography precision).

### 2.2 Chain Spectrum (UVR > 0 prediction — D4 counterexample)

The chain spectrum has no hierarchical clustering. Energy differences are proportional to index separation, producing the specific non-ultrametric configuration $Q_{13} < \min(Q_{12}, Q_{23})$.

**Configuration B — Exponential chain ($E_k \propto 3^{-k}$):**

$$\{E_0, E_1, E_2, E_3, E_4, E_5\} = E_{\max} \times \{1, 3^{-1}, 3^{-2}, 3^{-3}, 3^{-4}, 3^{-5}\}$$

**Example parameters (Hz, $E_{\max} = 1200$ Hz):**
$$\{E_0, E_1, E_2, E_3, E_4, E_5\} \approx \{1200, 400, 133, 44, 15, 5\}$$

Note: $E_k$ decreases with increasing $k$, so the zero-energy reference is applied to the constraint $\hat{H}|\Psi\rangle = 0$ via appropriate laser detunings.

**Experimental implementation:** Use a single Zeeman manifold with equal spacing, scaled to produce the $3^{-k}$ pattern. Energies are set by the magnetic field gradient: $E_k = g_k \mu_B B(z_k)$ where $z_k$ is the ion position in the trap's harmonic potential (which naturally produces approximately exponential energy sequences at large displacements).

**Prediction:** Chain spectrum + diagonal $\hat{H}_{CR}$ → $\text{UVR} > 0\%$ (specifically: $Q_{13} < \min(Q_{12}, Q_{23})$ is measured).

### 2.3 Why This Distinction Matters

| Configuration | $\hat{H}_{CR}$ Type | Predicted UVR | Mechanism |
|:-------------|:-------------------|:--------------|:----------|
| Tree + diagonal | Carrier only | $0\%$ | Diagonal + tree spectrum → exact ultrametricity |
| **Chain + diagonal** | **Carrier only** | **$> 0\%$** | **D4 counterexample: spectral structure breaks UVR even with diagonal coupling** |
| Tree + nondiagonal | Sideband added | $\sim 32\%$ | Off-diagonal coupling introduces RSB |
| Chain + nondiagonal | Sideband added | $\sim 32\%$ | Off-diagonal coupling dominates spectral effect |

**The critical test:** If Row 2 (chain + diagonal) shows UVR > 0 while Row 1 shows UVR = 0, the D4 refinement is experimentally validated. If both rows show UVR = 0, the original (unrefined) theorem holds and the D4 counterexample is not physically realized.

---

## 3. WDW State Preparation

### 3.1 The Constraint

The physical state must satisfy:
$$\hat{H}|\Psi\rangle = (\hat{H}_C + \hat{H}_R + \hat{H}_{CR})|\Psi\rangle = 0$$

For the WDW ensemble, the physically allowed states are superpositions of configurations with zero total energy. We prepare:
$$|\Psi\rangle = \frac{1}{\sqrt{Z}} \sum_{k=0}^{N-1} \sum_{n=0}^{M-1} \psi_{kn} |k\rangle \otimes |n\rangle \quad \text{with} \quad \hat{H}|\Psi\rangle = 0$$

where $\psi_{kn}$ is nonzero only when $E_k + n\omega_z + g_{k,n} \approx 0$ (to within the laser linewidth).

### 3.2 Preparation Protocol

1. **Cool** to motional ground state $|n=0\rangle$ via resolved sideband cooling
2. **Prepare clock superposition:** Microwave/optical pumping to $\frac{1}{\sqrt{N}} \sum_k |k\rangle$
3. **Apply constraint:** Laser pulses at each $\omega_{k,n} = E_k + n\omega_z$ to transfer population between $|k,n\rangle$ and auxiliary states
4. **Post-select:** Measure auxiliary qubit; keep trials where constraint is satisfied
5. **Verify:** $\langle \hat{H} \rangle < \epsilon_{\text{tol}} E_{\text{tot}}$

### 3.3 Validation

Before proceeding to ultrametricity tests, verify:
- Constraint satisfaction: $|\langle \Psi | \hat{H} | \Psi \rangle| < 10^{-2} \times ||\hat{H}||$
- State purity: $\text{Tr}(\rho^2) > 0.95$ (via randomized benchmarking)
- Clock population uniformity: $|p_k - 1/N| < 0.05$ for all $k$

---

## 4. Conditional State Measurement

### 4.1 Conceptual Protocol

For each clock reading $\tau$, the conditional rest state is:
$$|\psi_R(\tau)\rangle = \frac{1}{\sqrt{p(\tau)}} \langle \tau | \Psi \rangle$$

where $|\tau\rangle = \frac{1}{\sqrt{N}} \sum_k e^{-iE_k\tau} |k\rangle$ is the Page-Wootters "clock time" state. The overlap between conditional states at clock readings $\tau_i$ and $\tau_j$:

$$Q_{ij} = |\langle \psi_R(\tau_i) | \psi_R(\tau_j) \rangle|^2$$

This $N_{\tau} \times N_{\tau}$ overlap matrix is the primary observable.

### 4.2 Experimental Sequence

For each clock reading $\tau_i$ ($i = 1, \ldots, N_{\tau}$ with $N_{\tau} \geq 6$):

1. **Evolve clock:** Apply $\hat{U}_C(t) = e^{-i\hat{H}_C t}$ for time $t = \tau_i$ (implemented via phase advances on microwave carriers)
2. **Project clock:** Read out clock state via state-dependent fluorescence
3. **Tomography motional state:** For the post-selected clock projection, perform full motional state tomography (see §4.3)
4. **Reconstruct** $|\psi_R(\tau_i)\rangle$ from tomographic data
5. **Compute overlaps** $Q_{ij} = |\langle \psi_R(\tau_i) | \psi_R(\tau_j) \rangle|^2$

Repeat entire sequence $R \approx 10^4$ times per $\tau_i$ for statistical convergence.

### 4.3 Motional State Tomography

Full reconstruction of the $M$-dimensional motional density matrix $\rho_{\text{mot}}^{(i)}$ at each $\tau_i$:

1. **Displacement operations:** Apply $D(\alpha)$ for $\alpha \in \{\alpha_1, \ldots, \alpha_K\}$ on a discrete grid
2. **Motional parity measurement:** $\hat{\Pi} = \sum_n (-1)^n |n\rangle\langle n|$ via red/blue sideband comparison
3. **Maximum likelihood estimation:** Reconstruct $\rho_{\text{mot}}^{(i)}$ from parity data
4. **Extract $|\psi_R(\tau_i)\rangle$:** Take the dominant eigenvector (constraint enforces near-purity)

With $M = 4$ motional states, $K \approx 16$ displacement points suffice for $>99\%$ fidelity reconstruction.

---

## 5. Ultrametricity Test

### 5.1 Overlap Matrix Construction

From the $N_{\tau}$ conditional states, construct:
$$Q_{ij} = |\langle \psi_R(\tau_i) | \psi_R(\tau_j) \rangle|^2, \quad i,j = 1,\ldots,N_{\tau}$$

The overlap matrix is symmetric ($Q_{ij} = Q_{ji}$), has unit diagonal ($Q_{ii} = 1$), and values in $[0, 1]$.

### 5.2 Parisi Ultrametricity Violation Rate (UVR)

For each triple $(i, j, k)$, the strong triangle inequality requires:
$$Q_{ij} \geq \min(Q_{ik}, Q_{jk})$$

A violation occurs when $Q_{ij} < \min(Q_{ik}, Q_{jk})$. The UVR is:

$$\text{UVR} = \frac{\text{number of violating triples}}{\binom{N_{\tau}}{3}} \times 100\%$$

**Error estimation:** With $N_{\tau} = 6$ ($\binom{6}{3} = 20$ triples) and measurement uncertainty $\sigma_Q$ on each overlap:
$$\sigma_{\text{UVR}} \approx \frac{\sqrt{\text{UVR} \cdot (1 - \text{UVR})}}{\sqrt{20}}$$

For UVR $\approx 0$, we use Poisson statistics: an observation of 0 violations in 20 triples gives a 95% confidence upper bound of UVR $\leq 13.9\%$. With $N_{\tau} = 8$ (56 triples), the bound tightens to UVR $\leq 5.3\%$.

### 5.3 Predicted Outcomes — Four-Quadrant Test

**The hallmark of the D4 refinement: switching from zero to non-zero UVR purely by changing the clock spectrum.**

#### Quadrant I: Tree Spectrum + Diagonal $\hat{H}_{CR}$

| Quantity | Predicted Value |
|:---------|:----------------|
| UVR | $0\%$ (within statistical error) |
| Statistics | $0/20$ violations expected for $N_{\tau}=6$ |
| $\chi^2$ per degree of freedom | $\sim 0$ (consistent with exact ultrametricity) |

#### Quadrant II: Chain Spectrum + Diagonal $\hat{H}_{CR}$ — THE CRITICAL TEST

| Quantity | Predicted Value |
|:---------|:----------------|
| UVR | $> 0\%$ (specific: $Q_{13} < \min(Q_{12}, Q_{23})$ expected) |
| Specific violation | $Q_{13} < \min(Q_{12}, Q_{23})$ for chain $E_k \propto 3^{-k}$ |
| Physics | Spectral anti-clustering breaks ultrametricity even with diagonal coupling |
| Statistical significance target | $\geq 3\sigma$ separation from zero-violation null hypothesis |

**If UVR = 0 is observed in Quadrant II, the D4 counterexample is falsified — diagonal coupling alone IS sufficient for ultrametricity with this experimental configuration.**

#### Quadrant III: Tree Spectrum + Nondiagonal $\hat{H}_{CR}$

| Quantity | Predicted Value |
|:---------|:----------------|
| UVR | $32 \pm 3\%$ (universal violation rate from off-diagonal coupling) |
| Mechanism | Replica symmetry breaking from motional-state exchange |

#### Quadrant IV: Chain Spectrum + Nondiagonal $\hat{H}_{CR}$

| Quantity | Predicted Value |
|:---------|:----------------|
| UVR | $32 \pm 3\%$ (dominated by off-diagonal coupling, spectrum effect subdominant) |
| Mechanism | Off-diagonal RSB dominates spectral anti-clustering effect |

### 5.4 Statistical Power Analysis

For the critical Quadrant I vs. Quadrant II comparison:

| Parameter | Value | Rationale |
|:----------|:------|:----------|
| Null hypothesis $H_0$ | $\text{UVR} = 0$ in BOTH quadrants | Original (unrefined) theorem |
| Alternative $H_1$ | $\text{UVR} > 0$ in Quadrant II | D4 refinement |
| Test statistic | Observed violation count in Quadrant II | Binomial test |
| $N_{\tau}$ required for $5\sigma$ | $\geq 8$ ($56$ triples) | $p < 3 \times 10^{-7}$ for false positive |
| Tomography precision required | $\sigma_Q < 0.02$ | Must resolve $Q$ differences $> 2\sigma_Q$ |

---

## 6. Experimental Requirements

### 6.1 Required Capabilities

| Requirement | Value | Status |
|:------------|:------|:------|
| Single ion trapping (Yb$^+$ or Ca$^+$) | Standard Paul trap | Established [established] |
| $N \geq 6$ resolvable clock states | Hyperfine/Zeeman + tunable B-field | Established [established] |
| $M \geq 4$ motional Fock states | Near ground-state cooling | Established [established] |
| State-dependent fluorescence readout | Standard technique | Established [established] |
| Arbitrary laser pulse sequences | AOM + arbitrary waveform generator | Established [established] |
| Motional parity measurement | Red/blue sideband comparison | Established [established] |
| **Tunable clock spectrum (tree vs. chain)** | **B-field gradient + Zeeman tuning** | **Requires custom trap design (see §7)** |
| Constraint post-selection | Auxiliary ion/qubit | Requires 2-ion trap (established) |

### 6.2 Clock Spectrum Engineering — Experimental Implementation

**Tree spectrum realization:**
1. Use $^{171}$Yb$^+$ hyperfine structure: $F=0$ and $F=1$ manifolds in $^2S_{1/2}$
2. Within $F=1$: three $m_F$ sublevels split by $\delta = g_F \mu_B B$
3. Between $F=0$ and $F=1$: hyperfine splitting $\Delta_{\text{HFS}} = 12.6$ GHz
4. Map: $\{F=0\}$ → states $\{0,1,2\}$ with small intra-manifold Zeeman splitting; $\{F=1\}$ → states $\{3,4,5\}$ with large inter-manifold splitting
5. Fine-tune $\delta$ and $\Delta$ via magnetic field and AC Stark shifts

**Chain spectrum realization:**
1. Use a single $F=1$ manifold ($^2S_{1/2}$ in $^{171}$Yb$^+$)
2. Apply a magnetic field gradient $\partial B/\partial z$ along the trap axis
3. Position the ion at different $z$ via DC electrode voltages to sample the gradient
4. Alternatively: use AC Stark shifts from a focused laser to program $E_k$ values
5. The $3^{-k}$ sequence is programmed via individual laser detunings for each state

---

## 7. Noise Analysis and Error Budget

### 7.1 Sources of Systematic Error

| Error Source | Magnitude | Mitigation |
|:-------------|:----------|:-----------|
| Motional heating ($\bar{n} \to \bar{n}+1$) | $\sim 1$ quanta/s | Cryogenic trap ($T < 10$ K), suppress by $10^3 \times$ |
| Laser phase noise | $\Delta\phi \sim 10^{-3}$ rad/pulse | Phase-locked lasers, feed-forward |
| Magnetic field drift | $\Delta B/B \sim 10^{-6}$/hr | $\mu$-metal shielding, active compensation |
| State preparation fidelity | $> 99\%$ with composite pulses | BB1 or CORPSE sequences |
| Readout fidelity | $> 99.5\%$ per shot | Shelving technique |
| Tomography reconstruction bias | $\Delta Q < 0.01$ | Maximum likelihood + bootstrapped uncertainties |

### 7.2 Statistical Error

With $R = 10^4$ repetitions per $\tau_i$ and $N_{\tau} = 8$ clock readings:
- Overlap precision: $\sigma_Q \approx 1/\sqrt{R} \approx 0.01$
- UVR precision: $\sigma_{\text{UVR}} \approx \sqrt{\text{UVR}/56} \approx 0.04$ for UVR $\approx 5\%$
- Total experiment time: $N_{\tau} \times R \times (\text{sequence time}) \approx 8 \times 10^4 \times 10\,\text{ms} \approx 800$ s per configuration

### 7.3 Distinguishing Diagonal from Nondiagonal — Leakage Test

A critical systematic: imperfect laser polarization can introduce residual off-diagonal coupling in the "diagonal" configuration. To quantify this:

1. Measure $\epsilon_{\text{residual}} = ||\hat{H}_{CR}^{\text{off-diag}}|| / ||\hat{H}_{CR}^{\text{diag}}||$ via coherent population trapping
2. Require $\epsilon_{\text{residual}} < 0.01$ for the diagonal configuration to be valid
3. If $\epsilon_{\text{residual}} > 0.01$, the UVR in Quadrant I will be diluted toward $\sim 32\% \times (\epsilon_{\text{residual}}/0.3)^2$

---

## 8. Connection to CMB and Bruhat-Tits

### 8.1 CMB Interpretation

The non-ultrametric CMB temperature-temperature angular correlation overlaps ($C_\ell$ bispectrum analysis at large $\ell$) are consistent with either:
1. Nondiagonal coupling in the primordial Hamiltonian, OR
2. **Diagonal coupling + chain-structured primordial spectrum** (the D4 correction)

The present experiment distinguishes these mechanisms. A chain spectrum with diagonal coupling in the ion trap produces non-ultrametric overlaps — if the CMB shows identical non-ultrametric structure, the primordial Hamiltonian may be diagonal with a `natural' chain spectrum rather than a fine-tuned tree.

### 8.2 Bruhat-Tits Spectrum

The $p$-adic Bruhat-Tits tree at prime $p$ corresponds to a clock spectrum with exact self-similarity: $E_k \propto p^{-v_p(k)}$ where $v_p(k)$ is the $p$-adic valuation. This represents an idealized tree spectrum. The ion-trap clock spectrum in Configuration A approximates this for $p=2$ with depth $d=2$. Higher depths require more clock states ($N = p^d$). An alternative approach uses $N = p$ clock states with a single depth and tests the $p \to \infty$ (Archimedean, chain-like) limit by increasing $N$.

---

## 9. Timeline and Resource Estimate

| Phase | Duration | Description |
|:------|:---------|:------------|
| 1: Trap design | 2 months | Custom trap with magnetic field gradient for spectrum engineering |
| 2: Calibration | 1 month | Characterize tree and chain spectra, measure $\epsilon_{\text{residual}}$ |
| 3: Data (4 quadrants) | 2 weeks | $\sim 800$ s per quadrant, with cross-checks |
| 4: Analysis | 1 month | Full tomographic reconstruction, UVR calculation, systematic error budget |
| **Total** | **4.5 months** | First-generation experiment |

---

## References

1. Page, D. N. & Wootters, W. K. (1983). Evolution without evolution. *Physical Review D*, 27(12), 2885.
2. Moreva, E. et al. (2014). Time from quantum entanglement. *Physical Review A*, 89(5), 052122.
3. Parisi, G. (1979). Infinite number of order parameters for spin-glasses. *Physical Review Letters*, 43(23), 1754.
4. Almeida, J. R. L. & Thouless, D. J. (1978). Stability of the Sherrington-Kirkpatrick solution. *Journal of Physics A*, 11(5), 983.
5. QNFO Research (2026). The Silent Radix: Convergent Synthesis (v1.2). DOI: [10.5281/zenodo.21129799](https://doi.org/10.5281/zenodo.21129799).
6. QNFO Research (2026). Necessity Proof: Diagonal Sufficient Condition for Ultrametricity. DOI: [10.5281/zenodo.21122238](https://doi.org/10.5281/zenodo.21122238).

---

*Rebuilt 2026-07-02 with D4 correction. The four-quadrant test is the decisive experimental protocol for the silent-radix synthesis.*
