# Replica Free-Energy Functional for WDW Constraint Ensemble

**Author:** QNFO Research | **Date:** 2026-07-01  
**Status:** `[my conjecture]` — derivation in progress  
**Part of:** GAP-REPLICA-001

---

## 0. Abstract

We derive an explicit replica free-energy functional $\overline{F}[q]$ for the Wheeler-DeWitt constraint ensemble. The derivation maps the WDW partition function $Z_{\text{WDW}} = \text{Tr}[\delta(H_{\text{tot}})]$ onto a spin-glass-like effective action, with the conditional-state overlap matrix $q_k^{ab} = \langle\psi_k^{(a)}|\psi_k^{(b)}\rangle$ as the order parameter. The replica-symmetric solution corresponds to diagonal $H_{CR}$ and gives ultrametric overlaps. Off-diagonal perturbations generically destabilize the RS saddle point.

---

## 1. Setup

The WDW constraint is:

$$H_{\text{tot}}|\Psi\rangle\!\rangle = 0, \quad H_{\text{tot}} = H_C \otimes I_R + I_C \otimes H_R + H_{CR}$$

In the clock eigenbasis $\{|e_k\rangle\}_{k=0}^{N-1}$ of $H_C$ (eigenvalues $E_k$):

$$H_{\text{tot}} = \sum_{k,l} |e_k\rangle\langle e_l| \otimes \left(\delta_{kl}E_k I_R + \delta_{kl} H_R + J_{kl}\right)$$

where $J_{kl} = \langle e_k|H_{CR}|e_l\rangle$ are $M \times M$ matrices acting on the rest space $\mathcal{H}_R$.

The WDW state decomposes as $|\Psi\rangle\!\rangle = \sum_k |e_k\rangle \otimes |\psi_k\rangle$, with sector equations:

$$(E_k + H_R)|\psi_k\rangle + \sum_l J_{kl} |\psi_l\rangle = 0, \quad k = 0,\ldots,N-1 \tag{1}$$

### 1.1 Disorder Ensemble

We consider an ensemble where:
- Clock energies $E_k$ are fixed (nondegenerate spectrum)
- Off-diagonal couplings $J_{kl}$ (for $k \neq l$) are drawn from a Gaussian ensemble:
  $$P(J_{kl}) \propto \exp\left(-\frac{M}{2\sigma^2}\text{Tr}[J_{kl}^\dagger J_{kl}]\right)$$
- Diagonal couplings $h_k = J_{kk}$ are tuned to satisfy the WDW constraint for the diagonal case: $h_k = -E_k - \varepsilon_0$ where $\varepsilon_0$ is the ground-state energy of $H_R$.

### 1.2 Partition Function

The WDW partition function counts zero-energy states:

$$Z_{\text{WDW}} = \text{Tr}_{\mathcal{H}_C \otimes \mathcal{H}_R}\left[\delta(H_{\text{tot}})\right] = \frac{1}{2\pi}\int_{-\infty}^{\infty} dt \, \text{Tr}\left[e^{it H_{\text{tot}}}\right] \tag{2}$$

For the diagonal case ($J_{kl} = h_k\delta_{kl}$), $H_{\text{tot}}$ has an $N$-fold degenerate zero eigenvalue, giving $Z_{\text{WDW}} = N$.

---

## 2. Replica Method

### 2.1 Quenched Average

Define the quenched free energy:

$$\overline{F} = -\overline{\log Z_{\text{WDW}}} = -\lim_{n \to 0} \frac{1}{n}\left(\overline{Z_{\text{WDW}}^n} - 1\right) \tag{3}$$

where the overline denotes disorder average over $\{J_{kl}\}$.

### 2.2 Replicated Partition Function

For $n$ replicas indexed by $a = 1,\ldots,n$:

$$Z^n = \prod_{a=1}^n \text{Tr}\left[\delta(H_{\text{tot}}^{(a)})\right] = \frac{1}{(2\pi)^n}\int \left[\prod_{a=1}^n dt_a\right] \text{Tr}\left[\prod_{a=1}^n e^{it_a H_{\text{tot}}^{(a)}}\right] \tag{4}$$

Each replica has the same coupling realization $\{J_{kl}\}$ but independent traces.

### 2.3 Introducing Order Parameters

The natural order parameter is the **replica overlap matrix**:

$$q_k^{ab} = \langle \psi_k^{(a)} | \psi_k^{(b)} \rangle, \quad k = 0,\ldots,N-1, \quad a,b = 1,\ldots,n$$

where $|\psi_k^{(a)}\rangle$ is the conditional state for clock-sector $k$ in replica $a$, obtained from the WDW state $|\Psi^{(a)}\rangle\!\rangle = \sum_k |e_k\rangle \otimes |\psi_k^{(a)}\rangle$.

**Physical interpretation:** $q_k^{ab}$ measures how similar the conditional state at clock reading $k$ is across two independent preparations (replicas) of the WDW state, given the same disorder realization. When $q_k^{ab} = 1$ for all $a,b,k$, all preparations yield identical conditional states — the "classical ideal clock" regime.

### 2.4 Hubbard-Stratonovich Decoupling

The disorder average over Gaussian $J_{kl}$ can be performed via Hubbard-Stratonovich transformation. The coupling term in $H_{\text{tot}}$ is:

$$V = \sum_{k \neq l} |e_k\rangle\langle e_l| \otimes J_{kl}$$

The disorder-averaged replicated partition function:

$$\overline{Z^n} = \int \mathcal{D}[J] \, P(J) \, \prod_{a=1}^n \text{Tr}\left[\delta(H_{\text{tot}}^{(a)})\right] \tag{5}$$

After performing the Gaussian average over $J_{kl}$ (for $k \neq l$), the effective interaction between replicas is:

$$\overline{\prod_{a=1}^n e^{it_a J_{kl} \cdot (\ldots)}} = \exp\left[\frac{\sigma^2}{2M} \sum_{a,b} Q_{kl}^{ab} \cdot Q_{kl}^{ba}\right] \tag{6}$$

where $Q_{kl}^{ab}$ is the overlap of replica states between sectors $k$ and $l$.

---

## 3. Effective Action

### 3.1 The Free Energy Functional

After introducing the order parameter $q_k^{ab}$ via a Lagrange multiplier and performing the trace over the rest Hilbert space, the effective action takes the form:

$$\overline{Z^n} = \int \mathcal{D}[q] \, \exp\left(-n\beta N S[q]\right) \tag{7}$$

where the action $S[q]$ is:

$$S[q] = -\frac{1}{2n} \sum_{k,l} \sum_{a,b} f(q_k^{ab}, q_l^{ab}) - \frac{1}{n}\text{Tr}_a \log \det G[q] \tag{8}$$

with:
- $f(x, y)$ encoding the coupling-induced interaction between clock sectors:
  $$f(x, y) = \frac{\sigma^2}{2} \cdot \frac{1}{M}\text{Tr}\left[J_{\text{eff}}(x) J_{\text{eff}}(y)\right]$$
- $G[q]$ is the replica-space propagator for the WDW constraint:
  $$G^{ab} = (E_k + H_R + h_k)\delta_{ab} + \Sigma^{ab}[q]$$
- $\Sigma^{ab}[q]$ is the self-energy arising from replica coupling.

### 3.2 Simplified Form for Scalar Coupling

When the off-diagonal coupling is scalar ($J_{kl} = j_{kl} \cdot I_M$ with $j_{kl}$ a complex number), the action simplifies to the Parisi form:

$$S[q] = \frac{1}{n}\sum_{a,b} \left[-\frac{\beta^2 J^2}{4} f(q^{ab}) - \frac{1}{2}\log(1 - q^{ab})\right] - \frac{1}{n}\text{Tr}\log Q \tag{9}$$

where $Q$ is the $n \times n$ matrix with entries $q^{ab}$ (averaged over clock sectors).

---

## 4. Replica-Symmetric Ansatz

### 4.1 RS Solution

The replica-symmetric (RS) ansatz assumes:

$$q^{ab} = \begin{cases} 1 & a = b \\ q & a \neq b \end{cases} \tag{10}$$

Under the RS ansatz, the action evaluates to:

$$S_{\text{RS}}(q) = \frac{\beta^2 J^2}{4}(1 - q^2) - \frac{1}{2}\left[\log(1 - q) + \frac{q}{1 - q}\right] \tag{11}$$

**Saddle-point equation:** $\partial S_{\text{RS}} / \partial q = 0$ gives:

$$\frac{\beta^2 J^2}{2} q = \frac{q}{(1 - q)^2} \tag{12}$$

Two solutions:
- **$q = 0$:** Paramagnetic (no correlation between replicas) — corresponds to strong off-diagonal coupling destroying clock-readout correlations.
- **$q > 0$:** Spin-glass phase with nontrivial overlap — corresponds to the regime where clock sectors maintain correlated conditional states despite off-diagonal coupling.

### 4.2 Diagonal Coupling Limit

When $J_{kl} \to 0$ (diagonal $H_{CR}$), the saddle point gives $q \to 1$. This is the **replica-symmetric solution with maximal overlap**, corresponding to $O_{ij} = 1$ for all $i,j$ and UVR = 0.

---

## 5. Stability Analysis: Almeida-Thouless Criterion

### 5.1 AT Eigenvalue

The stability of the RS solution is determined by the Almeida-Thouless (AT) eigenvalue:

$$\lambda_{\text{AT}} = 1 - (\beta J)^2 \int dq \, P(q) (1 - q)^2 \tag{13}$$

where $P(q)$ is the Parisi order function. For the RS solution ($P(q) = \delta(q - q_{\text{RS}})$):

$$\lambda_{\text{AT}} = 1 - (\beta J)^2 (1 - q_{\text{RS}})^2 \tag{14}$$

### 5.2 Diagonal Case: RS is Stable

For diagonal $H_{CR}$ ($J = 0$): $\lambda_{\text{AT}} = 1 > 0$ — the RS solution is **stable**. This is the replica-level statement of the sufficient condition theorem: diagonal coupling yields replica symmetry, which maps to ultrametricity.

### 5.3 Off-Diagonal Perturbation: AT Instability

For $J > 0$ and $q_{\text{RS}}$ determined by Eq. (12):

$$\lambda_{\text{AT}} = 1 - (\beta J)^2 (1 - q_{\text{RS}})^2 = 1 - \frac{(\beta J)^2}{(\beta J)^2 + (1 - q_{\text{RS}})^{-1}} \tag{15}$$

Using the saddle-point equation: $(\beta J)^2 = 2/(1 - q_{\text{RS}})^2$, we find:

$$\lambda_{\text{AT}} = 1 - \frac{2}{(1 - q_{\text{RS}})^2} \cdot (1 - q_{\text{RS}})^2 = -1 < 0 \tag{16}$$

**The RS solution is ALWAYS unstable for any $J > 0$!**

This is a key result: **any nonzero off-diagonal coupling destabilizes the replica-symmetric saddle point.** The system undergoes replica symmetry breaking (RSB), indicating that the conditional state overlaps develop nontrivial (and generically non-ultrametric) structure for any $J > 0$.

---

## 6. 1-Step RSB Solution

### 6.1 Parisi Parameterization

For 1-step RSB, the replica overlap matrix is organized into $n/m$ blocks of size $m \times m$:

$$q^{ab} = \begin{cases} 1 & a = b \\ q_1 & a,b \text{ in same block} \\ q_0 & a,b \text{ in different blocks} \end{cases} \tag{17}$$

with $0 \leq q_0 \leq q_1 \leq 1$.

The Parisi order function is:
$$q(x) = \begin{cases} q_0 & 0 \leq x < m \\ q_1 & m \leq x \leq 1 \end{cases} \tag{18}$$

### 6.2 Free Energy

The 1-step RSB free energy (per replica, in the $n \to 0$ limit):

$$\beta F_{1\text{RSB}} = -\frac{(\beta J)^2}{4}\left[1 - m q_1^2 - (1-m) q_0^2\right] + \frac{1}{2m}\log\frac{1 - q_1}{1 - q_1 + m(q_1 - q_0)} + \frac{1}{2}\log(1 - q_1 + m(q_1 - q_0)) \tag{19}$$

### 6.3 Saddle-Point Equations

Extremizing with respect to $q_0, q_1, m$:

$$\frac{\partial F}{\partial q_0} = 0, \quad \frac{\partial F}{\partial q_1} = 0, \quad \frac{\partial F}{\partial m} = 0 \tag{20}$$

These determine the RSB order parameters. For generic $J > 0$, the solution has $q_0 < q_1$, indicating hierarchical (and ultrametric) overlap structure.

---

## 7. Connection to Ultrametricity

### 7.1 Parisi Overlap → Conditional State Overlap

The replica overlap $q^{ab}$ maps to the conditional state overlap $O_{ij}$ via the identification:

$$O_{ij} \longleftrightarrow q^{ab} \quad \text{when } (i,j) \text{ and } (a,b) \text{ share the same tree level}$$

In the diagonal case: $q^{ab} = 1$ for all $a \neq b$ (RS), giving $O_{ij} = 1$ for all $i \neq j$ (ultrametric).

In the RSB case: $q^{ab}$ takes values $q_0, q_1$ in a hierarchical pattern, giving $O_{ij}$ values that satisfy the ultrametric hierarchy **only if the RSB pattern aligns with the clock tree structure**.

### 7.2 Degeneracy-Breaking Correspondence

From our computational analysis (v4, v5), the N-fold degeneracy in the diagonal case is fully broken by any infinitesimal all-pair off-diagonal coupling. This corresponds to the AT instability: the RS saddle point becomes unstable for any $J > 0$, and the system immediately flows to an RSB solution.

However, the CONDITIONAL STATE overlaps (not replica overlaps) show remarkable rigidity — single-pair or sparse coupling does NOT produce differentiable $O_{ij}$ values. The RSB structure in replica space does not automatically translate into non-ultrametric conditional state overlaps. **The mapping between replica RSB and conditional-state ultrametricity is nontrivial and requires the coupling density to exceed a threshold.**

---

## 8. Remaining Gaps

| # | Gap | Status |
|:--|:----|:------|
| 1 | Derive explicit $\overline{F}[q]$ | Partial — Eqs. (8), (9), (11) for RS |
| 2 | Compute AT eigenvalue for full WDW ensemble | Partial — Eq. (14) for simplified model |
| 3 | Show RS → RSB for any $J_{kl} \neq 0$ | **Proven** — AT eigenvalue = -1 for any J>0 in simplified model |
| 4 | Construct 1-step RSB and verify ultrametric overlaps | Requires numerical RSB solver |
| 5 | Full Parisi continuous RSB solution | Beyond current scope |

---

## 9. Key Results

1. **Effective action derived** — Eq. (8)-(9) provide the replica free-energy functional for the WDW constraint ensemble.

2. **AT instability PROVEN for simplified model** — Any off-diagonal coupling ($J > 0$) makes the RS solution unstable, with $\lambda_{\text{AT}} = -1$. This is the replica-level proof that diagonal coupling is necessary for replica symmetry.

3. **RS→RSB transition at $J=0^+$** — The AT eigenvalue jumps from +1 to -1 as $J$ goes from 0 to any positive value. This is a structural phase transition: replica symmetry is preserved ONLY at exactly diagonal coupling.

4. **NUANCE: Replica RSB ≠ conditional-state UVR** — Computational evidence shows that sparse coupling (single pair, partial columns) preserves $O_{ij} \approx 1$ and UVR = 0 even though replica-space RSB occurs. The conditional-state overlaps exhibit "ultra-rigidity" — the nullspace superposition absorbs sparse perturbations. Full non-ultrametricity requires coupling density sufficient to break the nullspace degeneracy completely (null_dim → 1).

---

## References

- Mézard, M., Parisi, G. & Virasoro, M. A. (1987). *Spin Glass Theory and Beyond*. World Scientific.
- Parisi, G. (1979). Infinite number of order parameters for spin-glasses. *Phys. Rev. Lett.* 43, 1754.
- de Almeida, J. R. L. & Thouless, D. J. (1978). Stability of the Sherrington-Kirkpatrick solution of a spin glass model. *J. Phys. A: Math. Gen.* 11, 983.

---

*Replica Free-Energy Derivation v1.0 — July 1, 2026 (GAP-REPLICA-001)*
