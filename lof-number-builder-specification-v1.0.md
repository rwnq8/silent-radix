# LoF NUMBER BUILDER — Interactive Specification v1.0

**Part of the Silent Radix Research Program**
**Target:** Interactive web application demonstrating the construction of numbers as nested distinctions in the calculus of indications

---

## 1. Concept

The LoF Number Builder is an interactive web tool that allows users to construct numbers by drawing distinctions (marking spaces), choose a base (grouping of distinctions), and visualize the resulting numeral as a tree, a positional string, and an ultrametric space. It demonstrates that base, metric, and scale are visible parameters of the distinction process — not invisible add-ons.

---

## 2. Core Interaction Model

### 2.1 The Primitive Act: Drawing a Distinction

The user encounters an unmarked space (void, empty canvas). The single available action is: **draw a distinction** — click to create a mark, a boundary separating marked from unmarked.

Each mark represents one counted unit. Multiple marks accumulate. The user is counting, but the counting is spatial — each mark occupies a position in a tree structure determined by the chosen base.

### 2.2 The Base as Grouping Structure

The user selects a base $b$ (default: 2). The base determines the branching factor of the tree. When $b$ marks accumulate at one level, they "cross the boundary" — roll over — to become one mark at the next level up. This is exactly carrying in positional notation.

**Base selector:** A slider or dropdown for common bases: 2, 3, 5, 8, 10, 12, 16, 20, 60. Custom base entry allowed.

### 2.3 Positional Notation Display

As marks accumulate and roll over, a positional numeral appears:

- **Binary ($b=2$):** `1 → 10 → 11 → 100 → 101 → ...`
- **Decimal ($b=10$):** `1 → 2 → ... → 9 → 10 → 11 → ...`
- **Sexagesimal ($b=60$):** `1 → 2 → ... → 59 → 1-0 → 1-1 → ...`

The numeral is displayed with place-value columns labeled by power of base, and the radix is explicitly shown: $1011_2$, $11_{10}$.

### 2.4 The "10" Re-Entry — The Cycle Observes Itself

When the user accumulates exactly $b$ marks at the finest level, they witness the rollover: all $b$ marks vanish from the current level and one mark appears at the next level. The display shows the string "10."

At this moment, the interface highlights the re-entry: the column that just rolled over. A label appears: **"10 — the base observing its own completion."** This is the minimal act of self-aware measurement — the cycle counting its own period.

---

## 3. Visualization Modes

The user can toggle between three views of the same number:

### 3.1 Tree View (Primary)

The number is displayed as a rooted tree:

- The root is the unmarked state (zero, empty).
- Each level corresponds to a place-value column (base$^0$, base$^1$, base$^2$, ...).
- At each level, a node has up to $b$ children (the digits 0 through $b-1$).
- The active number is a path from the root to a leaf, with the count of marks at each level determining which child branch is taken.
- **Ultrametric visualization:** Two numbers are shown simultaneously, and the depth of their shared prefix (common ancestor in the tree) is highlighted. The ultrametric distance $b^{-k}$ where $k$ is the shared depth is displayed.

### 3.2 Positional String View

The number is displayed as a standard positional numeral with explicit radix markers, place-value labels, and the rollover logic animated.

### 3.3 Flattened Line View (Explicit Projection)

The number is mapped onto a Euclidean number line. The interface explicitly tags this as a **projection** — a secondary, derived view. A toggle allows switching between:

- **Linear spacing** (standard number line)
- **Logarithmic spacing** (Dehaene's log-compressed number sense)
- **$p$-adic clustering** (positions cluster by shared trailing digits)

The projection is labeled: `[LINEAR PROJECTION — Native structure is ultrametric tree]`

---

## 4. Metric Exploration

### 4.1 Distance Calculator

The user selects two numbers (by building them or typing them in multiple bases) and a metric:

| Metric | Computation | Visualization |
|:-------|:------------|:--------------|
| Euclidean | $|a - b|$ | Straight line segment |
| $b$-adic | $b^{-v_b(a-b)}$ | Depth of shared tree prefix |
| Log | $|\log(a) - \log(b)|$ | Compressed line |
| Discrete | $1$ if $a \neq b$, else $0$ | Binary same/different |

The distance is displayed alongside the tree, showing visually how "close" the numbers are under each metric.

### 4.2 p-adic Explorer

For prime $p$, the $p$-adic tree is rendered as a Cantor-set-like branching structure. The user can:

- Zoom into a $p$-adic ball (all numbers congruent mod $p^k$)
- See the ball subdivide into $p$ sub-balls
- Click a ball to see all numbers within it
- Switch between 2-adic, 3-adic, 5-adic, etc.

---

## 5. Mixed-Radix Mode

The user can define a mixed-radix system — a sequence of bases $[b_0, b_1, b_2, ...]$ for successive place-value columns. This models:

- **Time:** `[60, 60, 24]` — seconds, minutes, hours
- **Calendars:** `[31, 12]` — days, months
- **Custom hierarchies:** any nested grouping structure

The tree becomes irregular — each level has a different branching factor. The display shows the mixed-radix numeral (e.g., `14:05:00` for 2:05 PM) and the tree adapts accordingly.

---

## 6. LoF Formal View

An advanced panel shows the number as a formal expression in the calculus of indications:

- Cross symbols for distinctions: $\lrcorner$
- Nesting for place value: $\lrcorner \lrcorner \lrcorner$ represents three marks at the units level
- Empty space (void) for zero at any position
- The laws of calling and crossing are demonstrated interactively: two marks in the same space cancel; two nested marks cancel.

The user can manipulate the LoF expression directly and see the arithmetic consequences in the tree and numeral views.

---

## 7. The Silent Frame Detector (Integrated)

The Number Builder includes a "Naked Number" input: the user types a bare numeral like `10` or `010`, and the system:

1. Flags it as ambiguous: "This numeral has no radix — it could mean 2, 8, 10, or 16 depending on context."
2. Shows a split view: all four interpretations simultaneously in their respective trees.
3. Prompts: "Choose the intended base."
4. After selection, displays the number with an explicit radix marker.

This demonstrates the silent radix problem directly and interactively.

---

## 8. Educational Sequences

The tool supports guided sequences:

### 8.1 "What Is 10?" (Ages 8+)
1. Start with unmarked space.
2. Add one mark at a time — count to ten in base-10.
3. Switch to base-2 — count to ten again. "10" in binary equals two.
4. Switch to base-3 — "10" equals three.
5. Revelation: "In any base, '10' means the base itself."

### 8.2 "The Tree and the Line" (Ages 12+)
1. Build numbers in a chosen base, view the tree.
2. Switch to line view — see the flattening.
3. Compare distances in tree vs. line metrics.
4. Explore p-adic trees as alternative geometries.

### 8.3 "The Observer's Choice" (Undergraduate+)
1. Examine the "10" self-reference in the LoF formal view.
2. Explore re-entry: the cycle marking its own completion.
3. Discuss: "Who chose the base? Where is the observer in a decimal number?"
4. Construct a number with explicit frame — radix, metric, unit all visible.

---

## 9. Technical Architecture

### 9.1 Technology Stack
- **Frontend:** React + D3.js for tree visualization, Canvas for the unmarked space
- **State management:** Immutable tree structure representing the current number as a nested form
- **No backend required:** All computation client-side; LoF algebra is purely structural

### 9.2 Core Data Structure

```typescript
interface Distinction {
  content: Distinction[];  // contained marks (children at this level)
  depth: number;            // place-value level (0 = units, 1 = base^1, ...)
}

interface NumberForm {
  root: Distinction[];      // the number as nested distinctions
  base: number | number[];  // single base or mixed-radix sequence
  radixTag: string;         // explicit radix label (e.g., "10", "2", "3")
}
```

### 9.3 Key Operations
- `addMark(form, base)`: Add one mark; handle rollover/carrying
- `toPositional(form, base)`: Convert to string with radix marker
- `toTree(form)`: Convert to D3 hierarchy for tree visualization
- `ultrametricDistance(formA, formB, base)`: Compute shared nesting depth
- `toLoF(form)`: Convert to Spencer-Brown cross notation
- `reify(form)`: Apply calling/crossing laws to simplify

---

## 10. Deliverables

The full specification includes:

1. **Wireframes** for each view (Tree, Positional, Line, LoF, Mixed-Radix)
2. **Interaction flow diagrams** for "What Is 10?" educational sequence
3. **API specification** for the core LoF algebra in TypeScript
4. **Accessibility requirements:** screen-reader descriptions of tree structure, keyboard navigation for mark placement
5. **Test suite:** verify that the LoF algebra correctly implements calling and crossing laws; verify that positional output matches standard arithmetic for all bases

---

## 11. Relationship to the Research Program

This tool is the interactive demonstration of the thesis. It proves, in working code, that:

1. Numbers are constructed by acts of distinction.
2. The base is a visible choice of grouping — not a hidden parameter.
3. The ultrametric tree is the native geometry of positional notation.
4. The Euclidean line is a secondary projection.
5. The "10" loop is a stable re-entrant form — the tree observing its own branching.

The Number Builder makes the Silent Frame visible. It is the complement to the Consequence Atlas (which shows what happens when the frame is hidden) and the Explicit Frame Pattern Language (which provides design principles for keeping it visible).

---

*LoF Number Builder Specification v1.0 — Part of the Silent Radix Research Program. [EXECUTED]*
