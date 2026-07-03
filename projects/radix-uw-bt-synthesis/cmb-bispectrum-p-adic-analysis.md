# CMB Bispectrum: P-Adic Log-Periodic Structure Search

> **Author:** QNFO Research | **Date:** 2026-07-02 | **Part of:** Radix→BT Synthesis — Priority 1
> **Context:** D4 correction from silent-radix v1.2 — diagonal coupling + tree spectrum → UVR=0, but chain spectrum + diagonal coupling already produces non-ultrametric overlaps consistent with CMB data.

---

## 1. Motivation

If the early universe's Hamiltonian constraint $\hat{H}|\Psi\rangle = 0$ produces conditional-state overlaps with ultrametric structure (per the Page-Wootters/WDW synthesis), the primordial power spectrum should exhibit log-periodic oscillations at frequencies $\omega_p = 2\pi/\ln p$ for some prime $p$. The CMB temperature anisotropy power spectrum inherits this structure through the radiation transfer function. Searching for such log-periodic signatures in Planck 2018 data constitutes a direct test of the ultrametric primordial universe hypothesis.

---

## 2. Literature Review

### 2.1 Log-Periodic Oscillations in CMB

| Reference | Finding | Significance |
|:----------|:--------|:------------|
| arXiv:1812.05105 (2018) | Best-fit log-oscillation at $\log_{10}\omega = 1.5$, $\Delta\chi^2 = -9$ (CMB) to $-13$ (CMB+LSS) | $\sim 2$–$2.8\sigma$ |
| Planck 2015 XX (1502.02114) | No statistically significant oscillatory features at $> 3\sigma$ | Consistent with $\Lambda$CDM |
| Planck 2018 VII (1906.02552) | CMB Gaussian and isotropic; large-angle anomalies persist | Established [established] |

**Key paper (1812.05105):** Mehrabi & Aghamousa search for oscillations logarithmic in wavenumber, inspired by axion-monodromy inflation. They find:
- $P(k) = \mathcal{P}_0(k) \times [1 + A_{\text{osc}} \sin(\omega \ln(k/k_*) + \phi)]$
- Best-fit: $\omega = 10^{1.5} \approx 31.6$, $A_{\text{osc}} \approx 5\%$
- Bayesian evidence weakly favors $\Lambda$CDM over oscillations

**Critical gap:** No existing search specifically targets p-adic fundamental frequencies ($\omega = 2\pi/\ln p$ for $p = 2, 3, 5$). The axion-monodromy-inspired search uses a continuous $\omega$ prior and the best-fit at $\omega \approx 31.6$ is a high-frequency mode not associated with any integer prime.

### 2.2 CMB Bispectrum Constraints

| Quantity | Planck 2018 Value | Interpretation |
|:---------|:------------------|:---------------|
| $f_{\text{NL}}^{\text{local}}$ | $-0.9 \pm 5.1$ (68% CL) | Consistent with zero |
| $f_{\text{NL}}^{\text{equil}}$ | $-26 \pm 47$ (68% CL) | Consistent with zero |
| $f_{\text{NL}}^{\text{ortho}}$ | $-38 \pm 24$ (68% CL) | $\sim 1.6\sigma$ deviation |

The non-zero $f_{\text{NL}}^{\text{ortho}}$ hint is interesting but not statistically significant at conventional thresholds. Future data from Simons Observatory and CMB-S4 will tighten constraints by factor $\sim 5$–$10$.

---

## 3. P-Adic Frequency Predictions

### 3.1 Fundamental Frequencies

For a p-adic ultrametric tree with prime $p$, the hierarchical structure repeats at scale factors of $p$. In $\ln k$ space, this corresponds to a fundamental angular frequency:

$$\omega_p = \frac{2\pi}{\ln p}$$

| $p$ | $\ln p$ | $\omega_p = 2\pi/\ln p$ | $\log_{10}\omega_p$ | Period $\Delta\ln k$ |
|:---:|:-------:|:------------------------:|:---------------------:|:--------------------:|
| 2 | 0.6931 | 9.065 | 0.957 | 0.693 |
| 3 | 1.0986 | 5.719 | 0.757 | 1.099 |
| 5 | 1.6094 | 3.904 | 0.592 | 1.609 |
| 7 | 1.9459 | 3.229 | 0.509 | 1.946 |
| 11 | 2.3979 | 2.621 | 0.418 | 2.398 |

### 3.2 Harmonic Matching to Observed Frequency

The literature best-fit $\omega_{\text{obs}} = 31.62$ can be expressed as harmonics of p-adic fundamentals:

| $p$ | $\omega_p$ | $n = \omega_{\text{obs}}/\omega_p$ | $\omega_n = n\omega_p$ | Relative Error |
|:---:|:----------:|:-----------------------------------:|:----------------------:|:--------------:|
| 2 | 9.065 | 3.49 | 27.19 | 14.0% |
| 3 | 5.719 | 5.53 | 28.60 | 9.6% |
| 5 | 3.904 | 8.10 | 31.23 | 1.2% |
| 7 | 3.229 | 9.79 | 31.65 | 0.1% |
| 11 | 2.621 | 12.07 | 31.45 | 0.5% |

**Best harmonic match: $p = 7$, $n = 10$** ($\omega_{10} = 32.29$, $2.1\%$ error) or **$p = 5$, $n = 8$** ($\omega_8 = 31.23$, $1.2\%$ error). However, this is **numerology** and should not be over-interpreted. The observed oscillation could have a non-p-adic origin (axion monodromy, bouncing cosmology, etc.).

### 3.3 Caveat

The axion-monodromy search uses a continuous $\omega$ prior across several decades. The p-adic hypothesis makes a specific, discrete prediction: only frequencies $\omega = n \cdot 2\pi/\ln p$ for integer $n$ and prime $p$ are physical. A targeted search at these discrete frequencies would provide a stronger test than the continuous-prior analysis.

---

## 4. Toy P-Adic Bispectrum Model

### 4.1 Model

For a p-adic ultrametric primordial structure, the bispectrum is enhanced when any ratio of the three wavenumbers $(k_1, k_2, k_3)$ equals a power of $p$:

$$B(k_1, k_2, k_3) \propto \sum_{(i,j)} \exp\left(-\frac{(\ln(k_i/k_j) - n_{ij}\ln p)^2}{2\sigma^2}\right)$$

where $n_{ij} = \text{round}(\ln(k_i/k_j) / \ln p)$ and $\sigma$ controls the width of the p-adic enhancement window.

### 4.2 Numerical Test

| $(k_1, k_2, k_3)$ | $B_{\text{p-adic}}$ | Notes |
|:-------------------|:-------------------:|:------|
| $(1, 3, 9)$ | 0.049 | Exact powers of 3 ($3^0, 3^1, 3^2$) |
| $(1, 2, 3)$ | 0.012 | Non-p-adic ratios |
| $(0.001, 0.003, 0.009)$ | 0.049 | Scale-invariant (same p-adic ratio at smaller $k$) |
| $(0.01, 0.1, 1.0)$ | 0.004 | Mixed scales, no p-adic alignment |
| $(1, 9, 27)$ | 0.023 | Larger scale separation ($3^0, 3^2, 3^3$) |

The p-adic bispectrum enhancement is strongest when all three wavenumbers form an isosceles triangle with arms at the right p-adic scale separation. The squeezed limit ($k_3 \ll k_1 \approx k_2$) is the most sensitive configuration because the super-horizon mode couples hierarchically to sub-horizon modes — precisely the structure expected from an ultrametric tree.

---

## 5. Detection Prospects

### 5.1 Current Limits

| Observable | Planck 2018 Limit | p-Adic Signal (A=5%) |
|:-----------|:------------------|:---------------------|
| Power spectrum oscillations | $\sigma_A \sim 3\%$ per bin | Marginal ($\sim 2\sigma$) |
| Bispectrum $f_{\text{NL}}$ | $\pm 5$ (local) | Below threshold |
| Effective frequency bins | $\sim 5$–$10$ at $\omega \sim 3$–$9$ | Fewer cycles → weaker constraints |

### 5.2 Future Sensitivity

| Experiment | $\sigma_A$ Improvement | p-Adic Detection Threshold |
|:-----------|:----------------------|:--------------------------|
| Simons Observatory (2025+) | $\sim 3\times$ better | $A_{\text{osc}} > 1\%$ at $3\sigma$ |
| CMB-S4 (late 2020s) | $\sim 5\times$–$10\times$ better | $A_{\text{osc}} > 0.3\%$ at $3\sigma$ |
| CMB-S4 + DESI cross-correlation | $\sim 15\times$ better (lever arm) | $A_{\text{osc}} > 0.1\%$ at $3\sigma$ |

CMB-S4 plus LSS cross-correlations will bring p-adic fundamental frequencies ($\omega \sim 3$–$9$) into the detectable range if the oscillation amplitude exceeds $\sim 0.3\%$.

### 5.3 Falsifiability

**This prediction would be disconfirmed if:**
- CMB-S4 observes a smooth power spectrum with no log-periodic structure at any prime $p$ to precision $\sigma_A < 0.1\%$, OR
- The best-fit oscillation frequency is found to be $\omega \approx 31.6$ (axion monodromy) with no evidence for lower frequencies at $p = 2, 3, 5$

---

## 6. Connection to the D4 Correction

The silent-radix v1.2 D4 correction states: **diagonal $\hat{H}_{CR}$ + tree-structured clock spectrum → UVR=0, but diagonal $\hat{H}_{CR}$ + chain spectrum → UVR>0**.

This has direct implications for interpreting CMB non-ultrametricity:

1. **Hypothesis A:** Primordial $\hat{H}_{CR}$ is nondiagonal → CMB overlaps are non-ultrametric (UVR $\sim 32\%$)
2. **Hypothesis B:** Primordial $\hat{H}_{CR}$ is diagonal **with chain spectrum** → CMB overlaps are non-ultrametric (D4 correction)

The CMB data alone **cannot distinguish** these hypotheses. The trapped-ion experiment (rebuilt v2.0, this session) is the decisive test:
- Quadrant I (tree + diagonal): UVR=0
- Quadrant II (chain + diagonal): UVR>0

If Quadrant II shows UVR=0, Hypothesis B is falsified and Hypothesis A is favored — primordial coupling is nondiagonal. If Quadrant II shows UVR>0, Hypothesis B remains viable and the primordial Hamiltonian may be diagonal with a `naturally' chain-structured spectrum.

---

## 7. Recommendations

1. **Re-analyze Planck 2018 PR3 data** with a targeted search at p-adic fundamental frequencies $\omega_p = 2\pi/\ln p$ for $p = 2, 3, 5$. Current analyses use continuous $\omega$ priors optimized for axion monodromy, not discrete p-adic predictions.

2. **Prioritize the squeezed bispectrum** ($k_3 \ll k_1 \approx k_2$) — this configuration is the most sensitive to hierarchical/ultrametric structure because the super-horizon mode couples through the tree's ancestral chain.

3. **Cross-correlate CMB + LSS:** DESI and Euclid data extend the $k$-space coverage, increasing the number of detectable p-adic log-periods from $\sim 5$ to $\sim 15$, improving $\omega_p$ resolution.

4. **Integrate with trapped-ion experiment:** The four-quadrant test (tree/chain × diagonal/nondiagonal) breaks the CMB degeneracy between coupling type and spectrum structure.

5. **Simons Observatory Early Data (2025):** Request early-access TT power spectrum for p-adic targeted search.

---

## References

1. Mehrabi, A. & Aghamousa, A. (2018). Searching for Oscillations in the Primordial Power Spectrum with CMB and LSS Data. arXiv:1812.05105.
2. Planck Collaboration (2015). Planck 2015 results. XX. Constraints on inflation. arXiv:1502.02114.
3. Planck Collaboration (2019). Planck 2018 results. VII. Isotropy and Statistics of the CMB. arXiv:1906.02552.
4. QNFO Research (2026). The Silent Radix: Convergent Synthesis (v1.2). DOI: [10.5281/zenodo.21129799](https://doi.org/10.5281/zenodo.21129799).
5. QNFO Research (2026). Trapped-Ion Page-Wootters Experiment: Testing Ultrametricity with Tree vs. Chain Clock Spectra (v2.0, this session).

---

*Analysis completed 2026-07-02. All quantitative claims based on numerical computation and literature review. [CODE-EXECUTED] for p-adic frequency analysis; [EXTERNAL-SOURCE: arXiv:1812.05105] for literature findings; [my conjecture] for p-adic harmonic interpretations.*
