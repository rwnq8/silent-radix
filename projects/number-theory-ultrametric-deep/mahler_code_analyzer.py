#!/usr/bin/env python3
"""
Mahler Code Analyzer — Phase 2 Prototype v2 (fixed model)
==========================================================
Tests Conjecture 7.3: p-adic Mahler coefficient structure correlates with code distance.

For a stabilizer code family parameterized by n (code length):
  f(n) = distance d_n
  Mahler expansion: f(n) = sum a_k * binom(n, k)
  Decay: alpha = growth rate of v_p(a_k) with k

Key insight: v_p(a_k) — the p-adic VALUATION — is the proper metric.
Larger v_p(a_k) means faster p-adic decay, which should correlate with
larger code distance (more sophisticated p-adic structure).

Author: QNFO Research Agent | Date: 2026-07-03
"""

import math
from typing import List, Dict

# ==============================================================================
# p-adic Arithmetic
# ==============================================================================

def v_p(n: int, p: int) -> float:
    """p-adic valuation of integer n."""
    if n == 0:
        return float('inf')
    n = abs(n)
    v = 0
    while n > 0 and n % p == 0:
        n //= p
        v += 1
    return v

def binom(n: int, k: int) -> int:
    """Standard binomial coefficient."""
    if k < 0 or k > n:
        return 0
    k = min(k, n - k)
    result = 1
    for i in range(1, k + 1):
        result = result * (n - i + 1) // i
    return result

# ==============================================================================
# Mahler Transform
# ==============================================================================

def mahler_coefficients(f_values: List[int], p: int, max_n: int = 15) -> List[Dict]:
    """
    Compute Mahler coefficients a_n for a function f: Z_p -> Z.
    
    Mahler transform: a_n = sum_{k=0..n} (-1)^{n-k} binom(n,k) f(k)
    
    Returns list of dicts with {value, v_p, abs_p}
    """
    results = []
    for n in range(max_n + 1):
        s = 0
        for k in range(n + 1):
            sign = -1 if (n - k) % 2 == 1 else 1
            s += sign * binom(n, k) * f_values[k]
        
        vp = v_p(s, p) if s != 0 else float('inf')
        abs_p_val = p ** (-vp) if vp != float('inf') else 0.0
        
        results.append({
            "n": n,
            "value": s,
            "v_p": vp if vp != float('inf') else "inf",
            "abs_p": abs_p_val
        })
    
    return results

def mahler_decay_rate(coeffs: List[Dict], p: int) -> float:
    """
    Compute Mahler decay rate alpha = average slope of v_p(a_n) vs n.
    
    alpha = average (v_p(a_n) - v_p(a_{n-1})) for n >= 5 (asymptotic region)
    """
    valid = [(c["n"], c["v_p"]) for c in coeffs if isinstance(c["v_p"], (int, float)) and c["n"] >= 5]
    if len(valid) < 3:
        return 0.0
    
    # Average the increments
    increments = []
    for i in range(1, len(valid)):
        dn = valid[i][0] - valid[i-1][0]
        dv = valid[i][1] - valid[i-1][1]
        if dn > 0:
            increments.append(dv / dn)
    
    return sum(increments) / len(increments) if increments else 0.0

# ==============================================================================
# Code Characteristic Functions — Realistic Distances
# ==============================================================================

def surface_code_distances(max_n: int = 20) -> List[int]:
    """
    Toric/surface code distances: d(L) = L for [[2L^2, 2, L]].
    Parameterized by code length n = 2L^2.
    For n = 2, 8, 18, 32, 50, 72, 98, 128, 162, 200, ...
       d = 1, 2,  3,  4,  5,  6,  7,   8,   9,  10, ...
    """
    vals = []
    for n in range(max_n + 1):
        L = int(math.sqrt(n / 2)) if n >= 2 else 0
        d = min(L, max_n)  # distance = lattice size
        vals.append(max(d, 1))  # minimum distance 1
    return vals

def css_code_distances(max_n: int = 20) -> List[int]:
    """
    CSS code distances: d ~ floor(sqrt(n)) for random CSS codes.
    """
    vals = []
    for n in range(max_n + 1):
        d = max(1, int(math.floor(math.sqrt(n))))
        vals.append(d)
    return vals

def optimal_code_distances(max_n: int = 20) -> List[int]:
    """
    Optimal code distances: d ~ n (Singleton bound d <= n/2 + 1).
    For [[n, k, d]] with k=1, d <= floor(n/2)+1.
    """
    vals = []
    for n in range(max_n + 1):
        d = max(1, n // 2 + 1) if n >= 1 else 1
        vals.append(min(d, n + 1))
    return vals

def random_code_distances(max_n: int = 20) -> List[int]:
    """
    Random stabilizer codes: d ~ 3 (constant, no meaningful growth).
    """
    vals = []
    for n in range(max_n + 1):
        d = 3 if n >= 2 else (n + 1)  # d=3 for n>=2, d=1 for n=0, d=2 for n=1
        vals.append(d)
    return vals

# ==============================================================================
# Analysis
# ==============================================================================

def analyze_code(name: str, f_vals: List[int], p: int = 2):
    """Run Mahler analysis on a code family."""
    print(f"\n{'='*60}")
    print(f"CODE FAMILY: {name} (p={p})")
    print(f"Distances: f(0..{len(f_vals)-1}) = {f_vals[:8]}{'...' if len(f_vals) > 8 else ''}")
    print(f"{'='*60}")
    
    coeffs = mahler_coefficients(f_vals, p, max_n=min(15, len(f_vals)-1))
    alpha = mahler_decay_rate(coeffs, p)
    
    # Report Mahler spectrum
    print(f"\n  Mahler Spectrum (p={p}):")
    print(f"  {'n':>3} {'a_n':>8} {'v_p(a_n)':>10} {'|a_n|_p':>10}")
    print(f"  {'-'*3} {'-'*8} {'-'*10} {'-'*10}")
    for c in coeffs[:12]:
        n = c["n"]
        val = c["value"]
        vp = str(c["v_p"])
        ap = f"{c['abs_p']:.6f}" if isinstance(c['abs_p'], float) else "0.0"
        print(f"  {n:3d} {val:8d} {vp:>10} {ap:>10}")
    
    # Key metrics
    actual_d = f_vals[-1]
    
    # v_p growth
    vp_vals = [c["v_p"] for c in coeffs if isinstance(c["v_p"], (int, float))]
    vp_start = vp_vals[1] if len(vp_vals) > 1 else 0
    vp_end = vp_vals[-1] if vp_vals else 0
    vp_growth = vp_end - vp_start
    
    print(f"\n  Decay rate alpha = {alpha:.4f}")
    print(f"  v_p(a_1) = {vp_start}, v_p(a_N) = {vp_end}, growth = {vp_growth}")
    print(f"  Actual distance d = {actual_d}")
    
    return {
        "name": name,
        "alpha": alpha,
        "vp_growth": vp_growth,
        "actual_d": actual_d,
        "coeffs": coeffs
    }

def test_conjecture_7_3(results: List[Dict]):
    """Test Conjecture 7.3."""
    print(f"\n{'='*60}")
    print(f"TEST: Conjecture 7.3 — Mahler Decay ∝ Code Distance")
    print(f"{'='*60}\n")
    
    print(f"{'Code Family':<22} {'Alpha':<8} {'v_p growth':<10} {'Distance':<10} {'Alpha×d':<10}")
    print("-" * 65)
    
    for r in results:
        name = r["name"][:20]
        alpha = r["alpha"]
        vpg = r["vp_growth"]
        d = r["actual_d"]
        product = alpha * d
        print(f"{name:<22} {alpha:<8.4f} {vpg:<10.1f} {d:<10d} {product:<10.4f}")
    
    # Check: does higher alpha correlate with higher distance?
    sorted_by_d = sorted(results, key=lambda r: r["actual_d"])
    sorted_by_alpha = sorted(results, key=lambda r: r["alpha"])
    
    d_order = [r["name"] for r in sorted_by_d]
    alpha_order = [r["name"] for r in sorted_by_alpha]
    
    # Kendall tau (simplified)
    pairs = 0
    concordant = 0
    n = len(results)
    for i in range(n):
        for j in range(i+1, n):
            pairs += 1
            ri, rj = results[i], results[j]
            # Check if alpha and d have same ordering
            if (ri["alpha"] <= rj["alpha"] and ri["actual_d"] <= rj["actual_d"]) or \
               (ri["alpha"] >= rj["alpha"] and ri["actual_d"] >= rj["actual_d"]):
                concordant += 1
    
    tau = 2*concordant/pairs - 1 if pairs > 0 else 0
    
    print(f"\n  Kendall tau (alpha vs distance): {tau:.3f}")
    print(f"  Concordant pairs: {concordant}/{pairs}")
    
    if tau > 0.5:
        print("  [SUPPORTED] Conjecture 7.3: alpha correlates with distance")
    elif tau > 0:
        print("  [WEAK SUPPORT] Positive correlation but weak")
    elif tau == 0:
        print("  [INCONCLUSIVE] No detectable correlation")
    else:
        print("  [REFUTED] Negative correlation — alpha does NOT track distance")

# ==============================================================================
# Main
# ==============================================================================

def main():
    p = 2
    print("=" * 60)
    print("MAHLER CODE ANALYZER — Phase 2 Prototype v2")
    print("Testing Conjecture 7.3: v_p(a_k) growth ∝ Code Distance")
    print("=" * 60)
    
    families = [
        ("Surface Codes", surface_code_distances),
        ("CSS Codes", css_code_distances),
        ("Optimal Codes", optimal_code_distances),
        ("Random Codes", random_code_distances),
    ]
    
    results = []
    for name, func in families:
        f_vals = func(20)
        r = analyze_code(name, f_vals, p)
        results.append(r)
    
    test_conjecture_7_3(results)
    
    # p=3 test
    print(f"\n\n{'='*60}")
    print(f"CROSS-PRIME CHECK: p=3")
    print(f"{'='*60}")
    results3 = []
    for name, func in families:
        f_vals = func(20)
        r = analyze_code(f"{name} (p=3)", f_vals, p=3)
        results3.append(r)
    test_conjecture_7_3(results3)
    
    return results

if __name__ == "__main__":
    main()
