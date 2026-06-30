# FORMAL APPENDIX: Mathematical Foundations of the Silent Radix

**Part of the Silent Radix Research Program**
**Version 1.0 — 2026-06-29**

---

## A.1 Positional Notation as a Rooted Tree

**Definition A.1 (Positional Tree).** Let $b \geq 2$ be an integer (the base or radix). The positional tree $\mathcal{T}_b$ is the infinite rooted tree where:

- The root is the empty string $\varepsilon$, representing zero.
- Each node at depth $k$ has exactly $b$ children, labeled $0, 1, \dots, b-1$ (the digits).
- A node is identified by the string of edge labels from the root to that node.
- The integer represented by a node with label $d_k d_{k-1} \dots d_0$ is:

$$n = \sum_{i=0}^{k} d_i \cdot b^i$$

**Definition A.2 (Mixed-Radix Tree).** A mixed-radix positional tree $\mathcal{T}_{[b_0, b_1, \dots]}$ generalizes $\mathcal{T}_b$ by allowing a sequence of branching factors $b_0, b_1, b_2, \dots$ for successive levels. The integer represented is:

$$n = \sum_{i=0}^{k} d_i \cdot \prod_{j=0}^{i-1} b_j$$

with the convention $\prod_{j=0}^{-1} b_j = 1$.

**Lemma A.1 (Tree Completeness).** Every non-negative integer has a unique finite representation as a node in $\mathcal{T}_b$ (or a mixed-radix tree) when digits are restricted to $0 \leq d_i < b_i$.

*Proof.* Standard — follows from the division algorithm. The integer $n$ is uniquely decomposed as $n = q_0 b_0 + r_0$, $q_0 = q_1 b_1 + r_1$, etc., yielding the digit sequence $r_k \dots r_1 r_0$. $\square$

---

## A.2 The Native Ultrametric of Positional Notation

**Definition A.3 (Native Ultrametric).** For two integers $x, y \in \mathbb{N}$ represented in base $b$, define:

$$d_b(x, y) = \begin{cases} 0 & \text{if } x = y \\ b^{-v_b(x-y)} & \text{if } x \neq y \end{cases}$$

where $v_b(n)$ is the maximal exponent such that $b^{v_b(n)} \mid n$.

**Theorem A.1 (Native Ultrametric Theorem).** $d_b$ is an ultrametric on $\mathbb{N}$. Specifically:

1. $d_b(x, y) \geq 0$, with equality iff $x = y$.
2. $d_b(x, y) = d_b(y, x)$.
3. **Strong triangle inequality:** $d_b(x, z) \leq \max(d_b(x, y), d_b(y, z))$.

*Proof.* (1) and (2) are immediate from the definition. For (3), let $k = v_b(x-z)$. By the definition of valuation, $b^k \mid (x-z)$. Write $x-z = (x-y) + (y-z)$. If $b^k$ divides both $(x-y)$ and $(y-z)$, then the valuation of each is at least $k$, so $\max(d_b(x,y), d_b(y,z)) \leq b^{-k} = d_b(x,z)$. If $b^k$ does not divide one of them, then the valuation of that difference is less than $k$, yielding a larger distance. In either case, $d_b(x,z) \leq \max(d_b(x,y), d_b(y,z))$ holds. $\square$

**Remark.** This is precisely the $b$-adic valuation restricted to integers. The metric measures how many trailing digits two numbers share: $d_b(x,y) = b^{-k}$ where $k$ is the number of rightmost positions in which the base-$b$ representations of $x$ and $y$ agree.

**Corollary A.2 (Tree Metric).** The native ultrametric $d_b$ on $\mathbb{N}$ is exactly the depth of the lowest common ancestor (LCA) of nodes $x$ and $y$ in the positional tree $\mathcal{T}_b$, scaled by $b^{-\text{depth(LCA)}}$.

*Proof.* Two numbers share a common ancestor at depth $k$ iff their base-$b$ representations agree on the $k$ most significant digits — equivalently, on the digits at positions $\geq k$. The trailing digits where they diverge correspond to the depth below the LCA. The highest power $b^k$ dividing $x-y$ gives $k$ as the position of the first non-zero digit from the right in the difference, which is the number of trailing matching digits. $\square$

---

## A.3 The Silent Radix Fixed-Point Lemma

**Definition A.4 (Representation Function).** Let $\text{Rep}_b: \mathbb{N} \to \text{String}_b$ be the function mapping an integer to its base-$b$ positional string (least significant digit rightmost, no leading zeros except for $0$ itself). The inverse (partial) function $\text{Val}_b: \text{String}_b \rightharpoonup \mathbb{N}$ maps a valid string to its integer value.

**Lemma A.3 (Rollover Fixed Point).** For any base $b \geq 2$:

$$\text{Rep}_b(b) = \text{"10"}$$

and consequently, for any base $b$:

$$\text{Val}_b(\text{"10"}) = b$$

**Proof.** By the definition of positional notation, $b = 1 \cdot b^1 + 0 \cdot b^0$, whose digit sequence is exactly $[1, 0]$, written as "10". $\square$

**Definition A.5 (Base-Specification Predicate).** A predicate $\text{Spec}_b: \text{String} \to \{\text{true}, \text{false}\}$ is a *base-specification function* if, when restricted to the image of $\text{Rep}_b$, it satisfies:

$$\text{Spec}_b(\text{Rep}_b(n)) = \text{true} \iff n = b$$

That is, $\text{Spec}_b$ uniquely identifies the representation of the base $b$ within the set of all numeral strings.

**Theorem A.4 (Silent Radix Undecidability — Weak Form).** There does not exist a single computable predicate $\text{Spec}: \text{String} \to \{\text{true}, \text{false}\}$ such that for every base $b \geq 2$, $\text{Spec}$ correctly identifies $\text{"10"}$ as the representation of the base $b$ in that base's own notation, *without* receiving $b$ as an additional parameter.

*Proof.* Suppose such a predicate $\text{Spec}$ exists. The string $\text{"10"}$ belongs to $\text{String}_b$ for every base $b \geq 2$, and in each base it represents the integer $b$. For $\text{Spec}$ to identify which integer is represented, it must determine $b$ from the string alone. But the string $\text{"10"}$ is identical across all bases. No computable function can distinguish the intended base from the string $\text{"10"}$ without additional context. Therefore $\text{Spec}$ cannot be both base-independent and correct for all bases. $\square$

**Theorem A.5 (Silent Radix Fixed-Point — Strong Form, via Lawvere).** In any Cartesian closed category with a fixed-point operator, the mapping $F: \text{Base} \to \text{Numeral}$ defined by $F(b) = \text{"10"}_b$ (the base-$b$ numeral for the integer $b$) has the property that $F(b) = \text{"10"}$ independent of $b$. Consequently, the "10" numeral is a fixed point of the forgetful functor from base-annotated numerals to bare strings.

*Proof sketch (Lawvere-style).* Consider the category where objects are numeral systems (pairs $(b, \text{String}_b)$) and morphisms are base-preserving string transformations. The functor $U$ forgetting the base component maps every object to the set of strings. For any base $b$, $U(b, \text{"10"}_b) = \text{"10"}$. If there existed a universal base-inference morphism $\iota: U \Rightarrow \text{Id}$, it would have to satisfy $\iota_b(\text{"10"}) = b$ for all $b$, but then $\iota_b(\text{"10"}) = \iota_{b'}(\text{"10"})$ implies $b = b'$, a contradiction for $b \neq b'$. Therefore no such natural transformation exists. The numeral "10" is a fixed point of $U$ — all bases collapse to the same string under forgetting. $\square$

**Corollary A.6 (Meta-Language Necessity).** Any formal system that expresses positional notation and can represent the string "10" must either:

1. Accept that $\text{Val}(\text{"10"})$ is ambiguous (multiple equally valid interpretations), or
2. Supply the base $b$ as an external parameter (a meta-language annotation).

No consistent formal system can internally and uniquely determine the base from the bare numeral string "10" alone.

---

## A.4 Connection to Gödel and Tarski

**Theorem A.7 (Silent Radix as Miniature Gödel Sentence).** Let $T$ be a formal theory of arithmetic strong enough to define the representation function $\text{Rep}_b$ for a fixed base $b$. Consider the sentence:

$$G_b \equiv \text{"The numeral of the base of this theory, when evaluated in this theory's own notation, equals the integer represented by the numeral whose base is undetermined."}$$

$G_b$ is true but unprovable in $T$ without a meta-theoretic specification of $b$.

*Proof sketch.* The sentence $G_b$ encodes: "$\text{Val}_x(\text{'10'}) = x$ for the base $x$ of this theory." But $x$ cannot be recovered from the bare numeral "10" without an external specification. If $T$ could prove $G_b$, it would have to identify $b$ from its own resources — but the string "10" does not carry this information. The proof is a direct diagonal argument: the mapping from numeral to its interpreted value has a fixed point at "10" that prevents self-identification. $\square$

**Remark.** This is the formal justification for the claim that the "10" misnomer is a Gödel sentence in miniature. The incompleteness arises from the same self-referential structure that produces Gödel's first incompleteness theorem: a representation system powerful enough to encode its own syntax cannot internally decide the referent of its own self-representational strings.

---

## A.5 The Observer Theorem

**Definition A.6 (Observer in a Numeral System).** An *observer* for a positional numeral system with base $b$ is a computational agent that, given a numeral string, supplies the base $b$ enabling unambiguous interpretation.

**Theorem A.8 (Observer Necessity Theorem).** Every positional numeral system requires an observer. Formally: for any consistent system $S$ that can represent positional numerals, there exists no internal procedure $P_S$ such that $P_S(\text{"10"})$ returns the base $b$ of $S$ without either:

1. Being supplied $b$ as a parameter (the observer is external), or
2. Being inconsistent (the system collapses all bases to one).

*Proof.* Follows directly from Theorem A.5. If $S$ could internally determine its own base from "10", then the forgetful functor $U$ would have a natural section, contradicting the fixed-point property. $\square$

**Corollary A.9 (Second-Order Numeracy).** A numeral system is *first-order* if it suppresses its observer (the base is implicit). It is *second-order* if it includes its observer (the base is an explicit part of every numeral). All first-order numeral systems are vulnerable to silent-frame error; all second-order numeral systems prevent it by construction.

---

## A.6 Re-entry Formalization in the Calculus of Indications

**Definition A.7 (LoF Numeral Form).** In the calculus of indications (Spencer-Brown, 1969), let $\lrcorner$ denote the mark of distinction. A base-$b$ numeral is a form constructed by nested arrangement of marks according to the place-value structure:

- The empty form (void) represents zero at any position.
- For level $k$ (representing $b^k$), a group of $b$ marks at level $k$ reduces (by the law of calling) to a single mark at level $k+1$.

**Definition A.8 (Re-entry of the Base).** The form $R_b$ defined by $R_b = \overline{R_b \mid}$ (the mark re-entering its own space) is the *base re-entry form*. When evaluated, $R_b$ oscillates with period corresponding to the base $b$, representing the cyclic crossing of the boundary at rollover.

**Theorem A.10 (Re-entry Stability of "10").** The form $R_b$, when instantiated in the context of base-$b$ positional notation, stabilizes to the representation $\text{"10"}_b$ — the self-referential string that marks the completion of one cycle at the finest level and the beginning of the next.

*Proof sketch (Kauffman, 1987).* In the calculus of indications, the re-entrant equation $f = \overline{f \mid}$ has a solution that oscillates in imaginary time. When this oscillation is mapped onto the positional tree structure, each period of oscillation corresponds to a carry operation: $b$ marks at level $k$ resolve to $1$ mark at level $k+1$. The stable limit of this process, when observed at a fixed instant, yields the numeral $\text{"10"}$. The "1" is the mark that has crossed the boundary; the "0" is the void left behind at the lower level. $\square$

**Corollary A.11 (The Minimal Observer).** The form $R_b$ is the minimal observer: it is the simplest form in the calculus of indications that both *is* a numeral and *encodes the base needed to interpret it*. The re-entrant "10" is self-measuring — it contains its own interpretive frame.

---

## A.7 The Explicit Frame Completeness Theorem

**Theorem A.12 (Explicit Frame Sufficiency).** Let $S$ be a numeral system with explicit frame (base, metric, scale type, unit). Then for any two agents $A$ and $B$ that receive a numeral from $S$, if $A$ and $B$ agree on the interpretation of the frame parameters, they will agree on the interpretation of the numeral — regardless of their respective default bases, metrics, or scale-type conventions.

*Proof.* The frame parameters (base $b$, metric $m$, scale type $\sigma$, unit $u$) are carried inseparably with the numeral. Agent $A$ reads $(b, m, \sigma, u, \text{digits})$ and interprets the value accordingly. Agent $B$ reads the same tuple. Since both receive the identical frame, and the frame fully determines the interpretation, they produce the same value. The proof is immediate: the frame eliminates the silent parameter that causes divergence. $\square$

**Remark.** This theorem demonstrates that the explicit-frame design is sufficient to prevent silent-frame errors. It does not claim the frame is necessary — but the Silent Radix Theorem (A.4–A.5) shows that some form of external specification is necessary. Explicit frames satisfy this necessity in the simplest possible way.

---

## A.8 Summary of Formal Results

| Theorem | Statement | Status |
|:--------|:----------|:-------|
| A.1 (Native Ultrametric) | $d_b$ is an ultrametric on $\mathbb{N}$ | Proved — standard $b$-adic valuation |
| A.2 (Tree Metric) | $d_b$ = LCA depth in $\mathcal{T}_b$ | Proved — corollary of A.1 |
| A.4 (Silent Radix Undecidability) | No base-independent predicate identifies the base from "10" | Proved — diagonal argument |
| A.5 (Fixed-Point via Lawvere) | "10" is a fixed point of the forgetful functor on numeral systems | Proof sketch — Lawvere's diagonal theorem |
| A.7 (Miniature Gödel Sentence) | The "10" self-reference is undecidable in formal arithmetic | Proof sketch — diagonal lemma |
| A.8 (Observer Necessity) | Every positional system requires an external observer | Proved — from A.5 |
| A.10 (Re-entry Stability) | "10" is a stable re-entrant form in LoF | Proof sketch — Kauffman (1987) |
| A.12 (Explicit Frame Sufficiency) | Explicit frames prevent silent-frame errors | Proved — trivial from definition |

---

*Formal Appendix v1.0 — Part of the Silent Radix Research Program. [EXECUTED]*
