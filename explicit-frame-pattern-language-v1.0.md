# EXPLICIT FRAME PATTERN LANGUAGE v1.0

**A Design Guide for Self-Aware Numeric Communication**
**Part of the Silent Radix Research Program**

---

## Core Principle

> *No naked numbers. Every quantitative representation shall carry the interpretive frame needed to disambiguate its meaning — radix, metric, unit, scale type, and cyclic grounding.*

---

## The Nine Patterns

### Pattern 1: RADIX TAG

**Problem:** A numeral string like `10` has no intrinsic radix. It means ten in decimal, two in binary, eight in octal, sixteen in hex.

**Solution:** Every positional numeral shall carry a radix tag as an inseparable part of its representation.

| Instead of | Write | Meaning |
|:-----------|:------|:--------|
| `10` | `10_dec` or `0d10` | Ten (decimal) |
| `10` | `10_bin` or `0b10` | Two (binary) |
| `10` | `10_oct` or `0o10` | Eight (octal) |
| `10` | `10_hex` or `0x10` | Sixteen (hexadecimal) |
| `10` | `10_60` or `10_sex` | Sixty (sexagesimal) |

**Implementation:**
- Programming: `0b10`, `0o10`, `0d10`, `0x10` (Python 3, Rust)
- Data formats: `{"value": 10, "radix": "dec"}` or `"10_dec"`
- Documentation: subscript notation `10_{10}`

**Anti-pattern:** `int("010")` — radix guessing. Always specify: `int("010", 10)`.

---

### Pattern 2: METRIC DECLARATION

**Problem:** Numbers on a line have no intrinsic distance function. The Euclidean metric ($d(x,y) = |x-y|$) is a conventional default, not a logical necessity.

**Solution:** Every distance-sensitive numeric operation shall declare its metric.

| Metric | Declaration | Use Case |
|:-------|:------------|:---------|
| Euclidean | `metric=euclidean` | Continuous geometry, physics |
| $p$-adic | `metric=p_adic(2)` | Divisibility, tree clustering |
| Log | `metric=log10` | Magnitude perception, decibels |
| Discrete | `metric=discrete` | Counts, graph distance |
| Manhattan | `metric=manhattan` | Grid, L1 optimization |

**Implementation:**
```python
# Instead of: distance = abs(a - b)
distance = compute_distance(a, b, metric="euclidean")  # explicit

# p-adic distance
distance_2adic = p_adic_distance(a, b, p=2)
```

**Anti-pattern:** Computing a mean on ordinal data — the Euclidean distance between "agree" (4) and "strongly agree" (5) is assumed equal to the distance between "neutral" (3) and "agree" (4). The metric is silent and wrong.

---

### Pattern 3: UNIT GLUE

**Problem:** A measurement like `5.2` without units is meaningless. Is it meters? Seconds? Kilograms? Dimensionless?

**Solution:** Every physical quantity shall have its unit inseparably attached.

| Instead of | Write |
|:-----------|:------|
| `v = 5.2` | `v = 5.2_m` or `v = Quantity(5.2, "m")` |
| `mass = 100` | `mass = 100_kg` |
| `thrust = 4400` | `thrust = Quantity(4400, "N*s")` |

**Implementation:**
- Code: Use dimensional analysis libraries (`pint` for Python, `F#` units of measure, `Boost.Units` for C++)
- Data: `{"value": 5.2, "unit": "m"}` — never `{"distance": 5.2}`
- Variable naming: `distance_m`, `mass_kg`, `time_s`

**Anti-pattern:** The Mars Climate Orbiter — thruster data in `lbf·s` consumed by software expecting `N·s`. The unit was a silent parameter.

---

### Pattern 4: SCALE TYPE ANNOTATION

**Problem:** Numeric labels like `1, 2, 3, 4, 5` on a survey response carry no information about whether the numbers represent ordinal ranks, interval measures, or ratio quantities.

**Solution:** Every numeric variable in a statistical context shall declare its Stevens scale type.

| Scale Type | Declaration | Allowed Operations | Examples |
|:-----------|:------------|:-------------------|:---------|
| Nominal | `scale=nominal` | Mode, frequency | ZIP codes, IDs |
| Ordinal | `scale=ordinal` | Median, rank correlation | Likert, rankings |
| Interval | `scale=interval` | Mean (carefully), t-test | Celsius temperature |
| Ratio | `scale=ratio` | All arithmetic, geometric mean | Mass, length, counts |

**Implementation:**
- Data schema: `{"variable": "satisfaction", "scale": "ordinal", "values": [1,2,3,4,5]}`
- Linter rule: flag `mean()` or `t.test()` on ordinal variables
- Statistical software: `as.ordinal(x)` type cast with operation restrictions

**Anti-pattern:** Computing Z-scores on ranked education levels treated as interval.

---

### Pattern 5: CYCLIC GROUNDING

**Problem:** Numbers representing temporal or periodic phenomena lose their cyclic structure when flattened into pure decimal.

**Solution:** When a number counts cycles, declare the cycle hierarchy explicitly.

| Instead of | Write |
|:-----------|:------|
| `365` days | `1-0-0_{365}` (one year in a 365-day calendar) |
| `90` minutes | `1:30` (one hour thirty minutes, mixed radix 24:60) |
| `time = 50700` | `time = Duration(hours=14, minutes=5, seconds=0)` |

**Implementation:**
- Calendar: `YYYY-MM-DD` (ISO 8601) — makes the cyclic hierarchy explicit
- Mixed radix: `{cycles: [{unit: "hour", base: 24}, {unit: "minute", base: 60}, {unit: "second", base: 60}]}`
- Cyclic data: store the tree, not the flat count

**Anti-pattern:** Storing a duration as a bare integer of seconds and losing the calendar structure.

---

### Pattern 6: EPOCH DECLARATION

**Problem:** Timestamps like `2026-06-29 14:00:00` have hidden epoch offsets (time zone, fiscal year start, GPS week epoch) that determine their meaning.

**Solution:** Every temporal value shall carry its epoch information.

| Instead of | Write |
|:-----------|:------|
| `2026-06-29 14:00:00` | `2026-06-29T14:00:00+00:00` (ISO 8601 with UTC offset) |
| UNIX timestamp `1719604800` | `Timestamp(seconds=1719604800, epoch="1970-01-01T00:00:00Z", width=32)` |
| GPS week `2234` | `GPSWeek(week=2234, epoch="1980-01-06", rollover=1024, rollover_count=2)` |

**Implementation:**
- Always store UTC with time zone offset
- For embedded/legacy systems: include epoch, width, and rollover metadata
- Data schema: `{"timestamp": 1719604800, "epoch": "unix", "width": 32, "signed": true}`

**Anti-pattern:** Year 2038 — `time_t` is 32-bit signed, but the width and signedness are silent parameters of every POSIX timestamp.

---

### Pattern 7: PRECISION BOUNDS

**Problem:** Floating-point numbers like `3.141592653589793` carry no information about which digits are significant and which are artifacts of the representation.

**Solution:** Every computed or measured number shall carry precision bounds.

| Instead of | Write |
|:-----------|:------|
| `pi = 3.141592653589793` | `pi = 3.141592653589793 ± 1e-15` or `pi = Value(3.14159, precision=6)` |
| `result = 0.1 + 0.2` | `result = Decimal("0.3")` or `result = Fraction(1, 10) + Fraction(2, 10)` |

**Implementation:**
- Use decimal or rational types when precision matters
- Annotate significant figures: `3.14(16)` or `3.14 ± 0.01`
- In data: `{"value": 3.14159, "significant_digits": 6}`

**Anti-pattern:** `0.1 + 0.2 == 0.3` evaluates to `false` in IEEE 754 binary64. The precision limitation of the float representation is a silent parameter.

---

### Pattern 8: FRAME INHERITANCE

**Problem:** When numbers pass through system boundaries (API calls, file formats, databases), their frame is often stripped. JSON erases radix; CSV erases unit; SQL may coerce types silently.

**Solution:** Every data interchange format shall preserve frames across boundaries.

**Implementation:**
- API contracts: every numeric field has a schema with radix, unit, metric, scale
- File formats: use self-describing formats or explicit metadata blocks
- Database: use `CHECK` constraints, not silent coercion

```json
// Instead of
{"temperature": 23.5}

// Write
{
  "temperature": {
    "value": 23.5,
    "unit": "celsius",
    "scale": "interval",
    "precision": 1
  }
}
```

**Anti-pattern:** JSON — numbers are decimal-only, no hex, no octal, no unit. Information is destroyed at the format boundary.

---

### Pattern 9: THE WITNESS — Include the Observer

**Problem:** The act of measurement (the observer's choice of frame) is erased from the representation, making the frame invisible and error-prone.

**Solution:** Include a "witness" or "observer" marker — a minimal self-referential element that declares the frame was chosen.

**The "10" as witness:** The self-referential string "10" — the base naming itself — is the minimal observer. When a number carries its own frame, the "10" loop is stable and visible: the cycle marking its own completion.

**Implementation:**
- Every dataset: include a `_frame` section declaring observer choices
- Every measurement: include a `_by` field: who or what process chose the frame
- Interactive tools: show the frame choice and allow switching to see alternatives

```json
{
  "_frame": {
    "observer": "thermometer_model_T100",
    "chosen_radix": "dec",
    "chosen_metric": "euclidean",
    "chosen_unit": "celsius",
    "chosen_scale": "interval",
    "self_reference": "This frame declares itself in base-10 decimal."
  },
  "measurements": [...]
}
```

---

## Quick Reference Card

| If you see... | It's missing... | Add... |
|:--------------|:----------------|:-------|
| `10` | Radix | `10_dec` or `0d10` |
| `mean(survey)` | Scale type | `scale=ordinal` before `median()` |
| `distance = 5` | Unit | `5_m` or `Quantity(5, "m")` |
| `p < 0.001` | Effect size | `d = 0.3, CI [0.1, 0.5]` |
| `time = 90000` | Epoch + width | `Timestamp(90000, epoch="unix", width=32)` |
| `result = 0.30000000000000004` | Precision | `Decimal("0.3")` |
| `2026-06-29 14:00` | Time zone | `2026-06-29T14:00:00+00:00` |
| `010` in C | Radix (ambiguous) | `8` or `0o10` or `10` |
| `color: #10` | Radix (hex shorthand) | `#110000` or `rgb(17, 0, 0)` |
| `risk +50%` | Base of percentage | `from 2% to 3% (+1pp)` or `+50% relative to 2%` |

---

## Design Heuristics

1. **Default to explicit.** When in doubt, add the frame. Redundancy is cheaper than error.
2. **Frames travel with data.** Never strip frames at API boundaries, file formats, or database inserts.
3. **Frames are checkable.** Use linters, schema validators, and type systems to enforce frame presence.
4. **Frames are switchable.** Let the user change the frame and see how the interpretation changes.
5. **The observer is part of the system.** Don't erase who chose the frame or when.

---

*Explicit Frame Pattern Language v1.0 — Part of the Silent Radix Research Program. [EXECUTED]*
