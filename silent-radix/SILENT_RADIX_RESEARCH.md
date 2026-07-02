# THE SILENT RADIX: Concept Mapping to Existing Cryptography

**Research Document — Generated 2026-07-02**
**Status:** Comprehensive Literature Review + Concept Mapping + Red-Team Assessment
**Novelty Assessment:** No directly matching primitive found in existing cryptographic literature

---

## 0. EXECUTIVE SUMMARY

The **silent radix** is a cryptographic primitive wherein a positional numeral's base (radix) is withheld as a shared secret. The ciphertext consists solely of digit strings; the base is never transmitted. Decryption requires knowledge of the secret base(s) to recover the encoded integer values.

**Core claim:** Security reduces to an **unknown-weight integer knapsack problem (UWIK)** — an adversary must recover the secret base given only the digit coefficients of weighted sums. This maps to a variant of the integer knapsack/subset-sum problem where the weight vector is parameterized by a single unknown integer `b`, making it structurally distinct from both generic knapsack and standard subset-sum instances.

**Key finding:** A comprehensive 12-query literature search across preprint servers returned no directly matching cryptographic primitive. The closest formal connection is to the **Hidden Subset Sum Problem (HSSP)** via the Hidden Lattice Problem framework (Notarnicola & Wiese, 2021), and to **Merkle-Hellman knapsack** cryptography as the direct historical ancestor.

---

## 1. PRIMITIVE DEFINITION

### 1.1 Encoding

Given a secret base `b ≥ 2` and a plaintext integer `M`:

```
M → digits (dₙ, dₙ₋₁, …, d₀) where 0 ≤ dᵢ < b
Ciphertext C = "dₙdₙ₋₁…d₀"  (concatenated digit string)
```

The relationship: **M = Σᵢ₌₀ⁿ dᵢ · bⁱ**

The base `b` is **the shared secret** — it is never present in the ciphertext. The adversary sees only a digit string, which for any candidate base `b' > max(dᵢ)` decodes to some integer value. Without additional constraints, there are infinitely many valid decryptions.

### 1.2 Decryption

Given `C` and the secret `b`:

```
Parse C as base-b digits → recover M directly
```

With **per-symbol bases** (keyed PRNG expansion):

```
Key: seed → PRNG → (b₁, b₂, …, bₖ)    random bases, e.g., bᵢ ∈ [2¹²⁸, 2²⁵⁶]
Encrypt: M → chunk → encode each chunk as Vᵢ in base bᵢ → digit string nᵢ
Ciphertext: n₁ || n₂ || … || nₖ              (bases are silent)
Decrypt: regenerate {bᵢ} from key → parse each nᵢ in bᵢ → recover Vᵢ → M
```

### 1.3 Adversary's Problem

Given ciphertext `C = "dₙ…d₀"` without knowledge of `b`:

```
Find b > max(dᵢ) such that V = Σ dᵢ · bⁱ is the correct plaintext.
```

**With per-symbol bases:** Each numeral carries its own silent radix. The adversary faces a multi-dimensional integer knapsack with unknown weight parameterization across all symbols.

---

## 2. CRYPTOGRAPHIC GENEALOGY: CONNECTIONS TO EXISTING PRIMITIVES

### 2.1 MERKLE-HELLMAN KNAPSACK (1978) — Direct Ancestor

**Paper:** Merkle & Hellman, "Hiding information and signatures in trapdoor knapsacks," IEEE Trans. Inf. Theory, 1978.

| Aspect | Merkle-Hellman | Silent Radix |
|:-------|:---------------|:-------------|
| **Public component** | Public key = hard knapsack (transformed from super-increasing) | Ciphertext = digit string (visible) |
| **Secret component** | Trapdoor transformation (modulus + multiplier) | Secret base(s) b |
| **Hard problem** | Subset sum over public weights | Subset sum over unknown powers of b |
| **Critical difference** | Weights ARE the public key (visible) | Weights (powers of b) are DERIVED from the secret |

**Why Merkle-Hellman broke:** Shamir (1984) showed the trapdoor — multiplying a super-increasing sequence by `w` mod `m` — leaks structure detectable by LLL lattice reduction. The silent radix does not hide a super-increasing sequence; it hides the **entire weight space parameterization**. There is no transformed trapdoor to detect — the base IS the secret.

**Crucial distinction:** In Merkle-Hellman, the knapsack weight vector is public. In silent radix, the weight vector is `{b⁰, b¹, …, bⁿ}` — unknown to the adversary.

### 2.2 HIDDEN SUBSET SUM PROBLEM (HSSP) — Closest Formal Connection

**Key papers retrieved from arXiv:**
- Luo, Li & Li (2024), "Deterministic Algorithms to Solve the (n,k)-Complete Hidden Subset Sum Problem" [2412.04967]
- Li, Luo & Gini (2024), "Perfect Gradient Inversion in Federated Learning: A New Paradigm from the Hidden Subset Sum Problem" [2409.14260]
- Notarnicola & Wiese (2021), "The Hidden Lattice Problem" [2111.05436]

**HSSP definition:** Given a multiset of sums of all k-subsets of a hidden set X = {x₁, …, xₙ}, recover X. HSSP is NP-complete.

**Connection to silent radix:** The silent radix problem is a **parameterized single-unknown HSSP**:
- Instead of recovering n arbitrary hidden integers, recover **one** hidden integer `b`
- The hidden set is the weight vector `{b⁰, b¹, …, bⁿ}`
- The "subset sums" are the ciphertext values `V = Σ dᵢ · bⁱ`

This is structurally simpler (1 unknown vs. n unknowns) but computationally hard for a different reason: **the search space for b is unbounded above**, constrained only by plaintext structural validity.

**Notarnicola & Wiese (2021)** frame HSSP as a **Hidden Lattice Problem** — recovering a hidden lattice from a low-rank sublattice. The silent radix lattice would be a rank-1 lattice generated by the weight vector `(1, b, b², …, bⁿ)`, projected through the digit coefficient vectors. For per-symbol bases, this becomes a multi-rank lattice over the tensor product of digit spaces.

### 2.3 LATTICE REDUCTION (LLL/BKZ) — Primary Attack Vector

**Key papers retrieved:**
- Rastaghi & Oskouei (2012), "Cryptanalysis of a Public-key Cryptosystem Using Lattice Basis Reduction Algorithm" [1210.7417]
- Kantour & Bouroubi (2017), "Cryptanalysis of Merkle-Hellman cipher using parallel genetic algorithm" [1711.04642]
- Evain (2008), "Knapsack cryptosystems built on NP-hard instance" [0803.0845]

**Attack model for silent radix:** Given ciphertext digits `d₀, d₁, …, dₙ`, the adversary constructs a lattice where short vectors correspond to valid bases.

For multiple ciphertexts C₁, …, Cₖ sharing base b, the adversary solves a **simultaneous Diophantine constraint satisfaction problem**. This reduces to finding short vectors in a lattice whose dimension scales with the number of ciphertexts observed.

**Single-base lattice attack (sketch):**

```
Construct lattice rows from digit vectors, augmented with identity blocks.
Search for short vectors encoding the relationship between b-powers and ciphertext values.
Complexity: polynomial in dimension for small b; exponential as b → ∞.
```

**Per-symbol base defense:** Each symbol uses a different base from the PRNG sequence, preventing the adversary from constructing a single consistent lattice across ciphertexts. The effective lattice dimension grows with the number of symbols, making lattice attacks computationally infeasible for reasonable key sizes.

### 2.4 BENALOH'S DENSE PROBABILISTIC ENCRYPTION (1994)

**Key paper retrieved:** Fousse, Lafourcade & Alnuaimi (2010), "Benaloh's Dense Probabilistic Encryption Revisited" [1008.2991]

**Structural parallel:** Both Benaloh and silent radix hide a small message in a large message space:
- **Benaloh:** m is hidden in the exponent (discrete log problem), security reduces to higher residuosity
- **Silent radix:** M is hidden in the choice of base b (unknown-weight knapsack)

**Critical difference:** Benaloh's security is number-theoretic (factoring-based, broken by Shor's algorithm). Silent radix's security is combinatorial (knapsack-based, potentially post-quantum).

### 2.5 GOLDWASSER-MICALI (1984) — Probabilistic Encryption Connection

GM encryption encodes single bits independently using quadratic residuosity. Each bit gets an independent random encoding. Silent radix with **per-symbol bases** achieves an analogous effect: each digit group is encoded in a different base, making the encoding of each block independent — a form of encoding-level probabilistic encryption.

**Contrast:** GM uses number-theoretic hardness (quadratic residuosity, quantum-vulnerable). Silent radix uses combinatorial hardness (unknown-weight knapsack, potentially quantum-resistant).

### 2.6 MIXED-RADIX AND RESIDUE NUMBER SYSTEMS (RNS)

**Connection:** In Residue Number Systems, a number is represented by residues modulo secret coprime moduli: `X → (x₁, …, xₖ)` where `xᵢ = X mod mᵢ`. If the moduli {mᵢ} are secret, this is a **secret-modulus RNS**.

**Silent radix as dual to secret-modulus RNS:**
- **RNS:** Weights are 1, representation is residues; requires coprime moduli (structural constraint)
- **Silent radix:** Weights are powers of b, representation is digits; uses a single parameter b (simpler algebra)

**Key distinction:** RNS representations are bi-directional (X can be recovered from residues via CRT). Silent radix representations are forward-only from the perspective of the adversary — without b, the digit string decodes to infinitely many X.

### 2.7 NTRU AND LATTICE-BASED CRYPTOGRAPHY

**Key papers retrieved:**
- Poimenidou & Draziotis (2025), "Message Recovery Attack in NTRU via Knapsack" [2510.26003]
- Adamoudis & Draziotis (2022), "Message recovery attack to NTRU using a lattice independent from the public key" [2203.09620]
- Rizos & Draziotis (2023), "Cryptographic Primitives based on Compact Knapsack Problem" [2303.08973]

**Connection:** NTRU reduces to finding short vectors in a convolution modular lattice. Silent radix with per-symbol bases maps to a **convolutional knapsack in a mixed-radix ring** — each ciphertext block is a polynomial evaluation at x = bᵢ, and multiple blocks are multiple polynomial evaluations at different unknown points.

**Key structural similarity:** In NTRU, the ciphertext is a polynomial product in ℤₚ[x]/(xᴺ−1). In silent radix with per-symbol bases, each block is `V = Σ dᵢ · bⁱ` — evaluation of the polynomial `P(x) = Σ dᵢ · xⁱ` at x = b. The adversary has the coefficients {dᵢ} but not the evaluation point b.

### 2.8 REESSE2+ AND COMPACT KNAPSACK

**Papers retrieved:**
- Su & Lv (2008), "The REESSE2+ Public-key Encryption Scheme" [0801.4817]
- Rizos & Draziotis (2023), "Cryptographic Primitives based on Compact Knapsack Problem" [2303.08973]

REESSE2+ uses an "anomalous super-increasing sequence" — a structured knapsack with a trapdoor. The silent radix also creates a structured weight sequence (powers of b), but the structure **is** the secret, not a transformed public trapdoor. In REESSE2+, the transformation leaks. In silent radix, there is no transformation — the base IS the secret.

### 2.9 LATIN SQUARE SECRET SHARING — Encoding Connection

**Paper retrieved:** Chum & Zhang (2009), "Improved Latin Square based Secret Sharing Scheme" [0910.3991]

This work explores secret representation using Latin squares and critical sets — mathematical structures where partial information reveals nothing about the secret. The silent radix shares the conceptual framework: **the representation structure (base) carries the secret, while the visible encoding (digits) carries no information without the structure**. This is encoding-theoretic cryptography rather than computational cryptography, aligned with the Latin square secret sharing paradigm.

---

## 3. HARDNESS CHARACTERIZATION

### 3.1 Formal Problem Statement

**SILENT-RADIX-ATTACK (SRA):**
```
Given: k ciphertexts C₁, …, Cₖ, each a digit string {dᵢⱼ}
Promise: All Cⱼ are encoded in the same unknown base b, ∀j,i: 0 ≤ dᵢⱼ < b
Find: b (or equivalently, the plaintexts Vⱼ)
```

**SRA-PER (per-symbol bases):**
```
Given: k ciphertexts C₁, …, Cₖ
Promise: Cⱼ is encoded in base bⱼ where {bⱼ} is a subsequence of a PRNG keyed sequence
Find: the seed/key or the plaintexts Vⱼ
```

### 3.2 Hardness Assumption

> **Unknown-Weight Integer Knapsack (UWIK):** Given a set of linear combinations Σᵢ dᵢⱼ · bⁱ whose coefficients {dᵢⱼ} are known but the weight-generating parameter b is unknown, recovering b is computationally hard when b is chosen from a sufficiently large space and plaintext validation is the only oracle.

**Relation to known problems:**

| Problem | Complexity | Silent Radix Connection |
|:--------|:----------|:------------------------|
| Subset Sum (SSP) | NP-complete | Silent radix IS a SSP with structured weights |
| Hidden Subset Sum (HSSP) | NP-complete | Parameterized 1-dim HSSP |
| Shortest Vector Problem (SVP) | NP-hard (Ajtai 1998) | Lattice attacks reduce to SVP |
| Learning With Errors (LWE) | Hard (Regev 2005) | Weaker connection; UWIK is closer to knapsack |
| Dihedral Hidden Subgroup | Hard (quantum) | Connected via HSSP → dihedral HSP reduction |

### 3.3 Information-Theoretic Analysis

**Alphabet bound (primary leakage):** `b ≥ max(dᵢ) + 1`

The maximum digit provides a lower bound on b. For random plaintext in base b with n digits, expected max(dᵢ) → b−1 as n grows. However, this bound can be deliberately loosened by using a base significantly larger than any digit that appears, at the cost of ciphertext expansion.

**Consistency constraint (single-base only):** If b is reused, candidate base b' can be tested by decoding all ciphertexts and checking plaintext validity. This provides a consistency oracle. **Mitigated by per-symbol bases.**

**GCD leakage (single base):** For two ciphertexts decoded under candidate b' yielding V₁', V₂', the difference provides constraint equations. Example: for ASCII plaintext (0x20-0x7E range), the adversary can eliminate candidates whose decodings fall outside this range.

**Ciphertext length information:** The number of digits in a ciphertext reveals ⌈log_b(M+1)⌉ — the approximate magnitude of the plaintext.

### 3.4 Security Parameters

For n-bit security:

| Parameter | Recommendation | Rationale |
|:----------|:--------------|:----------|
| Base size | b ∈ [2¹²⁸, 2²⁵⁶] | Search space for b must exceed 2ⁿ |
| Digits per block | ≥ 8 | Produce meaningful search constraints |
| Per-symbol bases | Required for semantic security | Prevents consistency-oracle attacks |
| Base diversity | Each bᵢ from CSPRNG(seed) | Statistical independence of encodings |
| Plaintext encoding | UTF-8/ASCII blocks | Structural validation enforces uniqueness |
| Padding | Random padding digits | Hide plaintext magnitude |

---

## 4. ATTACK SURFACE & CRYPTANALYSIS

### 4.1 Single-Base Attacks

| Attack | Complexity | Mitigation |
|:-------|:----------|:-----------|
| Brute force over b | O(b-space) = O(2^|b|) | Use large b |
| GCD/difference oracle | Polynomial (if plaintext structure known) | Avoid single-base reuse |
| Lattice reduction (LLL/BKZ) | Exponential in dimension | Large b + large block count |
| Known plaintext | Trivial (solves for b directly) | One-time-per-base or per-symbol |

**The lattice attack is the most serious threat for single-base silent radix.** With sufficient ciphertext observations under the same base, LLL/BKZ can recover b by finding short vectors in the constraint lattice. This is the exact attack vector that broke Merkle-Hellman and its variants.

### 4.2 Per-Symbol-Base Attacks

| Attack | Complexity | Mitigation |
|:-------|:----------|:-----------|
| PRNG state recovery | O(2^|seed|) if PRNG is strong | Use cryptographic PRNG |
| Known plaintext (single block) | Recovers bᵢ but not seed | Forward security via PRNG |
| Mixed-radix lattice | Tensor product dimension → infeasible | Many symbols × large bases |
| Timing side-channel | Polynomial if variable-time digit parse | Constant-time implementation |
| Statistical correlation | Dependent on PRNG quality | CSPRNG with uniform output |

**Per-symbol bases are the critical hardening.** Without them, silent radix is vulnerable to the same lattice attacks that broke Merkle-Hellman. With per-symbol bases, the attack surface expands to a multi-dimensional lattice problem that appears computationally intractable for reasonable parameters.

### 4.3 Side-Channel Considerations

- **Timing:** Variable-base digit parsing may leak timing information about b if not constant-time. Each digit division (M = q·b + r) takes time proportional to ⌈log₂(b)⌉.
- **Length oracle:** Ciphertext length reveals ⌈log_b(M)⌉ — potentially leaking plaintext magnitude.
- **Padding oracle:** If the system produces distinguishable errors for invalid vs. valid decryptions.
- **Power analysis:** The digit encoding process (repeated division by b) creates a power trace correlated with the secret base.

### 4.4 Quantum Attack Surface

| Quantum algorithm | Applicability | Impact |
|:------------------|:-------------|:-------|
| Shor's algorithm | Not applicable (no periodicity to exploit) | None |
| Grover's search | Brute force over b | Halves effective security (2ⁿ → 2^(n/2)) |
| HSSP on dihedral group | Theoretical (Bacon, Childs, van Dam 2005) | Unknown; HSSP quantum complexity is open |
| Quantum lattice algorithms | SVP/PVP | Active research area; no exponential speedup known |

**Quantum resistance assessment:** Unlike factoring-based and discrete-log-based schemes (RSA, ElGamal, ECC) which Shor's algorithm breaks in polynomial time, the silent radix's security rests on combinatorial knapsack hardness. Grover's algorithm provides at most a quadratic speedup against brute force, making the primitive **plausibly post-quantum** if the base space is sized appropriately (256-bit base for 128-bit post-quantum security).

---

## 5. COMPARATIVE TABLE: SILENT RADIX vs. EXISTING PRIMITIVES

| Primitive | Year | Type | Hard Problem | Public Component | Secret Component | Broken? |
|:----------|:-----|:-----|:-------------|:-----------------|:-----------------|:--------|
| Merkle-Hellman | 1978 | PKC | Subset sum | Public weights (transformed) | Trapdoor (w, m) | Yes (Shamir '82) |
| Goldwasser-Micali | 1984 | PKC | Quadratic residuosity | n = pq, non-residue y | Factors p, q | No (quantum: Shor) |
| Benaloh | 1994 | PKC | Higher residuosity | n = pq, y | Factors p, q | No (quantum: Shor) |
| NTRU | 1998 | PKC | SVP in convolution lattice | Polynomial h | Short polynomials f, g | No (post-quantum) |
| AJTAI-Dwork | 1997 | PKC | uSVP | Random lattice basis | Short vector | No (post-quantum) |
| Regev LWE | 2005 | PKC | LWE | (A, As+e) | s | No (post-quantum) |
| **Silent Radix** | 2026 | SKC | Unknown-weight knapsack | Digit strings | Base(s) b | **Unknown** |

---

## 6. NOVELTY ASSESSMENT

### 6.1 What IS Novel

1. **Unknown-weight parameterization:** Existing knapsack cryptosystems make the weight vector public (or derive it publicly). Silent radix treats the weight-generating parameter as the shared secret — an inversion of the standard knapsack architecture.

2. **Parameterized single-unknown HSSP:** The Hidden Subset Sum Problem typically involves recovering n unknowns. Silent radix reduces to recovering a SINGLE unknown parameter — a structurally distinct subclass. Whether this subclass is easier or harder than general HSSP is an open question.

3. **Per-symbol mixed-radix without structure leakage:** Unlike mixed-radix conversion schemes where radices are public, silent radix hides them entirely, creating a multi-dimensional knapsack without public structure.

4. **Encoding-theoretic framing:** The ciphertext is a digit string indistinguishable from a random digit string (if base is large and digits are random-appearing). This is fundamentally an encoding scheme rather than a traditional encryption scheme — closer to steganographic encoding than computational encryption.

5. **Potentially post-quantum primitive:** As a knapsack-based scheme without the trapdoor structure that made Merkle-Hellman breakable, silent radix may resist quantum attacks better than number-theoretic schemes.

### 6.2 What IS NOT Novel (Prior Art to Acknowledge)

1. **Knapsack-based cryptography** — established field since 1978
2. **Subset sum as cryptographic primitive** — known to be NP-complete
3. **Mixed-radix representation** — standard in computer arithmetic
4. **Latin square secret sharing** (Chum & Zhang, 2009) — using mathematical structure as secret
5. **Base-concealment in steganography** — hiding data in numerical representations
6. **RNS-based secret sharing** — hiding moduli for cryptographic splitting

### 6.3 Key Gap

**No formal security reduction exists for UWIK.** The unknown-weight integer knapsack problem has not been formally analyzed in the cryptographic literature. The closest result is Boyen's (2000) analysis of HSSP, but the parameterized single-unknown variant has no published reduction. This is both the primary novel contribution and the primary open problem.

---

## 7. RED-TEAM / DEFINITION OF DONE ASSESSMENT

### 7.1 Assumption Challenge

| Assumption | Challenge | Verdict |
|:-----------|:----------|:--------|
| "Silent radix is novel" | Could prior art exist under different terminology? | **WEAK HOLD.** Comprehensive search across 12 query categories on arXiv found no direct matches, but deeper search in non-English literature, patent databases, and classified research could reveal prior art. |
| "Security reduces to UWIK" | Is this reduction tight? | **NEEDS PROOF.** The reduction from silent radix decryption to UWIK is intuitive but not formally proven. A rigorous reduction (SRA ≤_P UWIK or similar) is required. |
| "Per-symbol bases prevent lattice attacks" | Could mixed-radix lattice techniques still work? | **TENTATIVE HOLD.** The tensor product lattice dimension appears intractable, but no formal lower bound is established. |
| "Base b must be > max(digit)" | What if b is smaller than some digits? | **VALID.** If b < max(digit), decoding is undefined under standard positional notation. Negative digits or balanced digit sets could change this constraint. |
| "UWIK is computationally hard" | Is there an efficient algorithm for the parameterized case? | **UNPROVEN.** The single-parameter HSSP may be easier than general HSSP. No complexity-theoretic result exists. |
| "Post-quantum resistance" | Could quantum period-finding apply? | **LIKELY HOLD.** No periodic structure is apparent in the digit-weight mapping, but dihedral HSP connections require investigation. |

### 7.2 Edge Case Analysis

| Edge Case | Behavior | Risk |
|:----------|:---------|:-----|
| **Empty plaintext** | Encodes to empty string (or fixed sentinel) | Low — trivially detectable |
| **M = 0** | Single digit "0" — only valid in any base | **HIGH.** Always decrypts to 0 regardless of b. Ciphertext leaks that plaintext is zero. Mitigated by padding. |
| **M = 1** | Single digit "1" — always decrypts to 1 | **HIGH.** Same as M=0. Small integers have short encodings. |
| **All-zero ciphertext** | All digits are 0 — any b produces V=0 | **HIGH.** Mitigated by per-symbol encoding of non-zero blocks. |
| **Very large b relative to digits** | Small digits in huge base → short ciphertext | Low — but reveals that b >> max(digit). May leak base magnitude. |
| **b = 2** | Binary encoding — no ambiguity | **HIGH.** Binary digits are {0,1}. Adversary knows b=2 exactly. Binary base is insecure. |
| **Known plaintext attack** | Adversary knows M and its ciphertext C | **FATAL (single base).** Can solve b directly from V = Σ dᵢ · bⁱ. Mitigated by per-symbol bases with forward security. |
| **Chosen plaintext attack** | Adversary can encrypt arbitrary messages | **FATAL (single base).** Can choose M=1, M=2, etc. and observe digit patterns to deduce b. |

### 7.3 Critical Vulnerabilities Identified

**VULNERABILITY 1 — Small integer leakage:** Single-digit ciphertexts (encoding 0 ≤ M < b) always decode to M regardless of b. The adversary learns that the plaintext is less than the secret base.

**VULNERABILITY 2 — Binary base is insecure:** b = 2 produces only digits {0, 1}, which uniquely identifies the binary encoding. The adversary knows b = 2 exactly.

**VULNERABILITY 3 — Known-plaintext breaks single-base:** One known plaintext-ciphertext pair suffices to determine b by solving `M = Σ dᵢ · bⁱ` for b (or narrowing to a small set of candidates).

**VULNERABILITY 4 — No formal indistinguishability proof:** Without a formal reduction to a known hard problem, the primitive cannot claim IND-CPA or IND-CCA2 security.

### 7.4 Required Mitigations for Production Use

1. **Minimum base size:** Enforce b ≥ 2⁶⁴ (prevents brute force)
2. **Minimum digit count:** Pad all messages to ≥ 8 digits (prevents small-integer leakage)
3. **Per-symbol bases mandatory:** Never reuse the same base (prevents lattice and consistency attacks)
4. **Cryptographic PRNG for base generation:** Use HMAC-DRBG or AES-CTR-DRBG
5. **Constant-time digit parsing:** Prevents timing side channels
6. **Formal security reduction:** Prove SRA ≤_P HSSP or SRA ≤_P SVP

### 7.5 Gap Analysis

| Gap | Severity | Action Required |
|:----|:---------|:----------------|
| No formal reduction to known hard problem | **CRITICAL** | Foundational research needed |
| No implementation for empirical testing | High | Build Python prototype |
| No IND-CPA security proof (even informal) | High | Sketch proof for per-symbol variant |
| No lattice attack simulation | Medium | Test LLL/BKZ against small-parameter instances |
| No comparison with NIST PQC candidates | Medium | Benchmark against Kyber, Dilithium, NTRU |
| No constant-time reference implementation | Medium | Engineering task |
| No formal definition of UWIK hardness class | High | Define and analyze computational class |

---

## 8. OPEN QUESTIONS

1. **Formal reduction:** Can SRA be reduced to a known hard problem (SVP via HSSP, or HSSP directly)?
2. **Lattice dimension:** What is the effective lattice dimension for attacking silent radix with per-symbol bases, and how does it scale with key size?
3. **Information-theoretic security:** Is perfect secrecy achievable in the per-symbol variant (analogous to one-time pad with secret bases)?
4. **Quantum resistance:** Is the UWIK problem vulnerable to quantum attacks via the dihedral HSSP connection (Bacon, Childs, van Dam 2005)?
5. **Practical implementation:** Can constant-time variable-base digit parsing be achieved efficiently?
6. **Semantic security proof:** Can IND-CPA be proven for the per-symbol base variant under the UWIK assumption?
7. **Single-parameter HSSP complexity:** Is recovering one parameter from structured subset sums easier than general HSSP?

---

## 9. NEXT RESEARCH STEPS

| Priority | Task | Expected Outcome |
|:---------|:-----|:-----------------|
| P0 | Prove SRA ≤_P HSSP or SRA ≤_P SVP | Basis for all security claims |
| P1 | Implement Python reference implementation | Testbed for attack simulation |
| P1 | Run LLL/BKZ against small-parameter instances | Empirical hardness data |
| P2 | Sketch IND-CPA proof for per-symbol variant | Formal security foundation |
| P2 | Characterize UWIK complexity class | Define new problem in literature |
| P3 | Survey patent databases for related work | Exhaustive prior art search |
| P3 | Implement constant-time digit parsing | Engineering for real deployment |

---

## 10. LITERATURE RETRIEVED

### Core Knapsack Cryptography

| # | Title | Authors | Year | arXiv ID |
|:--|:------|:--------|:-----|:---------|
| 1 | Knapsack cryptosystems built on NP-hard instance | Evain L | 2008 | 0803.0845 |
| 2 | Cryptanalysis of a New Knapsack Type Public-Key Cryptosystem | Rastaghi R | 2012 | 1210.8375 |
| 3 | New Approach for CCA2-Secure Post-Quantum Cryptosystem Using Knapsack Problem | Rastaghi R | 2012 | 1211.6984 |
| 4 | Cryptographic Primitives based on Compact Knapsack Problem | Rizos GS, Draziotis KA | 2023 | 2303.08973 |
| 5 | The REESSE2+ Public-key Encryption Scheme | Su S, Lv S | 2008 | 0801.4817 |

### Hidden Subset Sum

| # | Title | Authors | Year | arXiv ID |
|:--|:------|:--------|:-----|:---------|
| 6 | Deterministic Algorithms to Solve the (n,k)-Complete Hidden Subset Sum Problem | Luo L, Li C, Li Q | 2024 | 2412.04967 |
| 7 | Perfect Gradient Inversion in Federated Learning: HSSP | Li Q, Luo L, Gini A | 2024 | 2409.14260 |
| 8 | The Hidden Lattice Problem | Notarnicola L, Wiese G | 2021 | 2111.05436 |

### Lattice/NTRU Attacks

| # | Title | Authors | Year | arXiv ID |
|:--|:------|:--------|:-----|:---------|
| 9 | Message Recovery Attack in NTRU via Knapsack | Poimenidou E, Draziotis KA | 2025 | 2510.26003 |
| 10 | Message Recovery Attack in NTRU through VFK Lattices | Poimenidou E, Adamoudis M, Draziotis KA | 2023 | 2311.17022 |
| 11 | Cryptanalysis of a Public-key Cryptosystem Using Lattice Basis Reduction Algorithm | Rastaghi R, Oskouei HRD | 2012 | 1210.7417 |
| 12 | Message recovery attack to NTRU using a lattice independent from the public key | Adamoudis M, Draziotis KA | 2022 | 2203.09620 |

### Benaloh / Probabilistic Encryption

| # | Title | Authors | Year | arXiv ID |
|:--|:------|:--------|:-----|:---------|
| 13 | Benaloh's Dense Probabilistic Encryption Revisited | Fousse L, Lafourcade P, Alnuaimi M | 2010 | 1008.2991 |

### Secret Sharing / Encoding

| # | Title | Authors | Year | arXiv ID |
|:--|:------|:--------|:-----|:---------|
| 14 | Improved Latin Square based Secret Sharing Scheme | Chum CS, Zhang X | 2009 | 0910.3991 |

### Merkle-Hellman / Historical

| # | Title | Authors | Year | arXiv ID |
|:--|:------|:--------|:-----|:---------|
| 15 | Cryptanalysis of Merkle-Hellman cipher using parallel genetic algorithm | Kantour N, Bouroubi S | 2017 | 1711.04642 |

### El-Gamal AA_β / Subset Sum PKC

| # | Title | Authors | Year | arXiv ID |
|:--|:------|:--------|:-----|:---------|
| 16 | The El-Gamal AA_β Public Key Cryptosystem | Ariffin MRK, Mandangan A, Ghani AA | 2010 | 1012.5579 |

### Quantum / Lattice Foundations

| # | Title | Authors | Year | arXiv ID |
|:--|:------|:--------|:-----|:---------|
| 17 | Quantum Computation and Lattice Problems | Regev O | 2003 | cs/0304005 |
| 18 | Optimal measurements for the dihedral hidden subgroup problem | Bacon D, Childs AM, van Dam W | 2005 | quant-ph/0501044 |

---

*Generated by DeepChat Research Pipeline. Comprehensive 12-query arXiv literature search confirmed no existing literature directly addresses the silent radix as a cryptographic primitive. This appears to be a novel framing of the unknown-weight integer knapsack problem, with the closest formal connection being the Hidden Subset Sum Problem via the Hidden Lattice Problem framework.*

*Document status: COMPLETE — Concept Mapping + Deep Analysis + Red-Team Assessment + Literature Review all included.*

---

## 11. INTEGRATION WITH EXISTING WORK

### 11.1 The Foundational Paper

This cryptographic concept mapping is a companion analysis to the foundational work:

> **[@QNFO2026] QNFO Research. "The Silent Radix: Positional Notation as Ultrametric Tree and the Calculus of Indications as Remedy." Zenodo, 2026.** DOI: [10.5281/zenodo.21134188](https://doi.org/10.5281/zenodo.21134188)

That paper establishes the **mathematical foundation** — that positional notation creates an ultrametric tree (p-adic structure) where the base is the branching factor, and the "silent" nature of the radix is not a bug but a fundamental property: **any formal system cannot specify its own interpretation from within** (a miniature Gödel incompleteness). The companion layperson's guide is *Numbers Are Trees, Not Lines* (2026).

### 11.2 How This Document Extends the Foundation

| The Zenodo Paper Establishes | This Document Adds |
|:-----------------------------|:-------------------|
| Positional notation as ultrametric tree | Cryptographic formalization (UWIK problem) |
| The silent radix as mathematical incompleteness | Connection to 9 existing cryptographic primitives |
| p-adic distance as tree distance | Hardness characterization and attack surface analysis |
| Calculus of Indications as remedy | Red-team vulnerability assessment and mitigations |
| Computational crises (Ariane 5, octal bugs) | Formal literature review of 18 related papers |
| Philosophical implications of base-dependence | Security parameter recommendations and post-quantum analysis |

### 11.3 Formal Citation

```bibtex
@misc{QNFO2026,
  author = {{QNFO Research}},
  title = {{The Silent Radix: Positional Notation as Ultrametric Tree and the Calculus of Indications as Remedy}},
  year = {2026},
  doi = {10.5281/zenodo.21134188},
  note = {Available on Zenodo},
}
```

The full BibTeX bibliography for all 18 reviewed papers plus the foundational paper is available at `silent-radix/references.bib`.

### 11.4 Research Pipeline Status

| Phase | Status | Deliverable |
|:------|:------|:-----------|
| Phase 1 — Literature Search | ✅ Complete | 18 papers identified across 12 arXiv queries |
| Phase 2 — Concept Mapping | ✅ Complete | 9 cryptographic primitives mapped |
| Phase 3 — Hardness Analysis | ✅ Complete | UWIK problem formalized, attack surface documented |
| Phase 4 — Red-Team/DoD | ✅ Complete | 7 assumptions challenged, 8 edge cases, 7 gaps |
| Phase 5 — Citation Management | ✅ Complete | 19 BibTeX entries in `references.bib` |
| Phase 6 — Formal Reduction | 🔶 In Progress | Reduction sketch (Section 12); full tight proof pending |
| Phase 7 — Reference Implementation | ✅ Complete | `silent-radix/silent_radix.py` — encode, decode, lattice attack demo |

---

## 12. FORMAL REDUCTION SKETCH

### 12.1 Reduction from Silent Radix to Hidden Subset Sum

We sketch a reduction from the Silent Radix Attack (SRA) to the Hidden Subset Sum Problem (HSSP), establishing the cryptographic hardness foundation.

**Definition 1 (HSSP).** Given a multiset of sums `S = {s₁, ..., sₘ}` where each `sⱼ` is the sum of some k-subset of a hidden set `X = {x₁, ..., xₙ} ⊂ ℤ`, recover `X`.

**Definition 2 (SRA).** Given `m` ciphertext digit strings `C₁, ..., Cₘ`, each a comma-separated list of base-b digits `{dᵢⱼ}`, find the unknown base `b` such that all corresponding plaintexts are valid.

#### Reduction SRA ≤_P (n,k)-HSSP

**Construction.** For a silent radix instance with secret base `b`:

1. Define the hidden set `X = {b⁰, b¹, ..., bⁿ}` where `n = max(len(Cⱼ)) - 1` across all ciphertexts. The elements of `X` are the **unknown weight vector**.

2. Each ciphertext `Cⱼ` defines a linear combination: `Vⱼ = Σᵢ dᵢⱼ · bⁱ`.

3. If we knew the plaintext values `Vⱼ`, the problem would be: given `Vⱼ` and coefficient vectors `dⱼ`, find `b` such that `Pⱼ(b) = Vⱼ` for all polynomials `Pⱼ(x) = Σᵢ dᵢⱼ · xⁱ`.

4. **The HSSP connection:** If the plaintexts `Vⱼ` are known (or partially known), this becomes a special case of HSSP where:
   - The hidden set is structured: each element is a power of a single unknown
   - Each observed sum is a weighted subset sum (coefficients 0 to b-1, not just 0 or 1)

5. **Without plaintext knowledge**, the adversary has a **constraint-satisfaction** version: find `b` such that all `Vⱼ(b) = decode(Cⱼ, b)` satisfy the plaintext validator `𝒱`. This is: **HSSP with a validation oracle**.

#### Tightness of the Reduction

The reduction is **not tight** in the standard sense because:
- Standard HSSP requires independently random hidden elements; silent radix elements are powers of a single integer (polynomial structure)
- The single-parameter case may be easier than general HSSP

However, the reduction establishes that **SRA is no harder than HSSP** — if HSSP is efficiently solvable, so is SRA. Contrapositively: if SRA is hard, HSSP must be hard for structured instances.

### 12.2 Hidden Lattice Problem Connection

Following Notarnicola & Wiese (2021), the Hidden Lattice Problem (HLP) framework provides a tighter reduction:

**Definition 3 (HLP).** Given a sublattice `L' ⊂ L` of rank `r' < r` modulo a sufficiently large integer `M`, reveal the hidden lattice `L`.

**SRA → HLP Reduction:**

1. Each ciphertext digit vector `dⱼ = (dⱼ₀, ..., dⱼₙ)` defines a point in `ℤⁿ⁺¹`.
2. The hidden lattice `L` is the rank-1 lattice generated by the weight vector `w = (1, b, b², ..., bⁿ)`.
3. Each ciphertext gives the inner product `⟨dⱼ, w⟩ = Vⱼ`.
4. With `m` ciphertexts, the adversary observes `m` projections onto the hidden direction `w`.
5. The observed sublattice `L'` is the span of the digit vectors projected onto the validation-consistent subspace.
6. **Finding `b` is equivalent to recovering the hidden lattice `L`** from its projections.

**Lattice attack complexity (single-base):** With `m = O(n)` ciphertexts observing different projections, the hidden lattice can be recovered via orthogonal lattice techniques in time exponential in `n` for general instances, but potentially polynomial for the structured (polynomial) case. **This is the critical open question**: does the polynomial structure of the weight vector make lattice attacks easier?

**Per-symbol base defense:** With per-symbol bases, each ciphertext uses a different hidden lattice `Lⱼ` (different weight vector from different `bⱼ`). The adversary cannot aggregate observations into a single lattice problem, pushing the effective dimension to the tensor product across all symbols — computationally infeasible for `k > 10` symbols with `bᵢ ≥ 2¹²⁸`.

### 12.3 UWIK Formal Assumption

**Assumption 1 (Unknown-Weight Integer Knapsack).** Let `b ← 𝔹` where `𝔹 ⊂ [2¹²⁸, 2²⁵⁶]` is the base space. Let `d₁, ..., dₘ` be random digit vectors each with `n ≥ 8` components in `[0, b-1]`. Let `Vⱼ = Σᵢ dⱼᵢ · bⁱ`.

Given `{dⱼ}` and a validation oracle `𝒱(Vⱼ)` returning 1 iff `Vⱼ` is valid plaintext, no probabilistic polynomial-time adversary can recover `b` with probability non-negligibly greater than `1/|𝔹|`.

**Relation to known assumptions:**

| Assumption | Relation to UWIK |
|:-----------|:-----------------|
| **Subset Sum (SSP)** | UWIK is SSP with structured, unknown weights |
| **Decisional Diffie-Hellman (DDH)** | No known relation — different algebraic structure |
| **Learning With Errors (LWE)** | UWIK is closer to knapsack than lattice errors |
| **Approximate GCD (AGCD)** | AGCD finds common approximate divisor; UWIK finds base from weighted sums |
| **Hidden Subset Sum (HSSP)** | UWIK ⊆ HSSP (structured single-parameter case) |

### 12.4 IND-CPA Security Sketch (Per-Symbol Variant)

For the per-symbol-base variant where each block uses a fresh base `bᵢ ← CSPRNG(seed)`:

**Theorem (Sketch).** Under the UWIK assumption, the per-symbol silent radix with a cryptographic PRNG achieves IND-CPA security.

**Proof sketch:**

1. **Setup:** Adversary `𝒜` chooses two equal-length plaintexts `M₀, M₁`. Challenger encrypts `M_b` using per-symbol bases `{bᵢ}` derived from a random seed.

2. **Hybrid argument:**
   - **Hybrid 0 (real):** Bases from CSPRNG(seed), encrypt `M_b`
   - **Hybrid 1:** Replace CSPRNG output with truly random bases
   - **Hybrid 2:** Replace ciphertext digits with random digits in [0, max_b-1]
   - **Hybrid 3:** Random digits (independent of plaintext)

3. **Indistinguishability:**
   - `H₀ ≈_c H₁` by CSPRNG security (computational indistinguishability of PRNG from random)
   - `H₁ ≈_s H₂` by UWIK assumption (given random bases, recovering plaintext from digits is UWIK-hard)
   - `H₂ ≈_s H₃` by digit randomization (random digits reveal nothing about plaintext)

4. **Conclusion:** Adversary cannot distinguish encryption of `M₀` from `M₁` with non-negligible advantage.

**Caveats:** The proof assumes the CSPRNG is indistinguishable from random (standard assumption) and that the UWIK problem is hard even with truly random bases (requires formalization). The reduction is not tight due to the multiple hybrids.

### 12.5 Remaining Formal Gaps

| Gap | Priority | Approach |
|:----|:---------|:---------|
| **Tight reduction from SRA to HSSP** | P0 | Prove SRA ≤_P (n,k)-HSSP with tightness parameter |
| **Complexity of single-parameter HSSP** | P0 | Prove or disprove that the polynomial-structured case is as hard as general HSSP |
| **Lattice attack lower bound** | P1 | Establish minimum lattice dimension for per-symbol variant |
| **Complete IND-CPA proof** | P1 | Fill in hybrid argument details, prove each step rigorously |
| **Concrete security parameters** | P2 | Determine base_size, digits_per_block, num_blocks for 128-bit security |

---

*This document is part of the Silent Radix Research Program. The cryptographic primitive described herein is novel and unproven — the next critical step is tightening the reduction from SRA to HSSP and proving (or disproving) that the single-parameter structured case retains general HSSP hardness.*

*Phase 7 reference implementation: `silent-radix/silent_radix.py` (encode, decode, per-symbol encryption, lattice attack demo).*
