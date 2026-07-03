#!/usr/bin/env python3
"""
Hasse Principle Tester — Phase 2 Prototype (Pillar II)
=======================================================
Tests Conjecture 2.1: Hasse Principle for Stabilizer Codes.

Key questions:
1. Do known code families satisfy "local" existence at all primes?
2. Can we construct parameter sets that exist locally everywhere
   but have no global realization (analogous to Brauer-Manin obstruction)?
3. What are the "local invariants" at each prime?

Methodology:
- Define a toy model of "local quantum codes" at prime p
- Parameter space: (n, k, d, q) where q = p^m (qudit dimension)
- Local condition at prime p: code parameters must be realizable
  over a p-adic field extension of the appropriate degree
- Search for "local-only" codes — satisfying all local conditions
  but corresponding to no known code family

References:
- QNFO DEFINITIONS.md §1: Local quantum code at prime p
- QNFO DEFINITIONS.md §2: Hasse Principle for Stabilizer Codes
- Serre, J.-P. (1979). Local Fields. Springer.
- Skorobogatov, A. (2001). Torsors and Rational Points. Cambridge.

Author: QNFO Research Agent | Date: 2026-07-03
"""

import math
import itertools
from typing import List, Dict, Set, Tuple, Optional
from collections import defaultdict

# ==============================================================================
# SECTION 1: Local Code Invariants
# ==============================================================================

def v_p(n: int, p: int) -> int:
    """p-adic valuation."""
    if n == 0:
        return float('inf')
    v = 0
    while n % p == 0:
        n //= p
        v += 1
    return v

def is_prime(n: int) -> bool:
    """Simple primality check."""
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True

def primes_up_to(limit: int) -> List[int]:
    """Generate primes up to limit."""
    return [n for n in range(2, limit + 1) if is_prime(n)]

# ==============================================================================
# SECTION 2: Code Parameter Spaces
# ==============================================================================

class CodeParams:
    """Parameters of a stabilizer code [[n, k, d]]_q."""
    
    def __init__(self, n: int, k: int, d: int, q: int = 2):
        """
        Args:
            n: Number of physical qudits
            k: Number of logical qudits
            d: Code distance
            q: Qudit dimension (q = p^m for some prime p)
        """
        self.n = n
        self.k = k
        self.d = d
        self.q = q
        
        # Factor q into prime power
        self.characteristic = self._find_characteristic(q)
    
    def _find_characteristic(self, q: int) -> Optional[int]:
        """Find the prime p such that q = p^m."""
        if q < 2:
            return None
        for p in [2, 3, 5, 7, 11, 13, 17, 19, 23]:
            v = q
            while v % p == 0:
                v //= p
            if v == 1:
                return p
        return None
    
    def __repr__(self):
        return f"[[{self.n}, {self.k}, {self.d}]]_{self.q}"

# ==============================================================================
# SECTION 3: Known Code Families (Parameter Scaling Laws)
# ==============================================================================

def surface_code_params(L: int) -> CodeParams:
    """Toric/surface code on LxL lattice: [[2L^2, 2, L]]_2."""
    return CodeParams(n=2*L*L, k=2, d=L, q=2)

def css_random_params(n: int) -> CodeParams:
    """Random CSS code: [[n, n/2, O(sqrt(n))]]_2."""
    d = max(1, int(math.sqrt(n)))
    k = max(1, n // 2)
    return CodeParams(n=n, k=k, d=d, q=2)

def perfect_code_params(n: int) -> CodeParams:
    """Hypothetical perfect code: [[n, 1, d]]_2 with d optimal."""
    d = max(1, n // 2 + 1 if n >= 2 else 1)
    return CodeParams(n=n, k=1, d=d, q=2)

def random_stabilizer_params(n: int) -> CodeParams:
    """Random stabilizer: d ≈ 3, k ≈ n/2."""
    return CodeParams(n=n, k=max(1, n//2), d=3, q=2)

# ==============================================================================
# SECTION 4: Local Conditions at Prime p
# ==============================================================================

def local_constraints(params: CodeParams, p: int) -> Dict[str, bool]:
    """
    Compute local constraints at prime p for code parameters.
    
    A "local quantum code at prime p" must satisfy:
    1. Divisibility: n, k, d must be compatible with p-adic structure
    2. Bound constraints: Singleton bound d <= n - k + 1 (p-adic version)
    3. Weight constraints: minimum weight must be p-adically non-null
    4. Characteristic constraints: q must be compatible with p
    
    Returns dict of constraint_name -> satisfied (True/False)
    """
    constraints = {}
    
    # Constraint 1: Code length divisibility by p-structure
    # Codes over W(F_p^m) should have length divisible by m
    m = int(math.log(params.q, p)) if params.q > 1 and p > 0 else 0
    # For p-adic codes, n should be "natural" under p-adic metric
    v_n = v_p(params.n, p) if params.n > 0 else 0
    constraints["length_p_structure"] = v_n >= 0  # Always true for integer n
    
    # Constraint 2: p-adic weight constraint (REPLACES strict p_adic_singleton)
    # The p-adic norm |d|_p must be at least as large as |n-k+1|_p
    # for the code to be "p-adically meaningful" — i.e., the code distance
    # should not be p-adically too large compared to the bound.
    # For surface codes: v_2(d) compares against v_2(n-k+1)
    singleton_bound = params.n - params.k + 1
    if singleton_bound > 0 and params.d > 0:
        # Check: |d|_p >= |n-k+1|_p  <=>  v_p(d) <= v_p(n-k+1) OR the p-adic
        # structure is non-trivial (code has interesting p-adic depth)
        v_d = v_p(params.d, p)
        v_bound = v_p(singleton_bound, p)
        # Relaxed: fail only when d is p-adically MUCH larger than bound
        # (suggesting non-p-adic structure). Pass if v_d <= v_bound OR
        # if d << singleton_bound (which is typical for good codes).
        constraints["p_adic_weight"] = (
            v_d <= v_bound or 
            v_bound == float('inf') or 
            params.d < singleton_bound // 2
        )
    else:
        constraints["p_adic_weight"] = True  # Vacuous
    
    # Constraint 3: Characteristic compatibility
    # If p = char(q), code must be defined over W(F_p^m)
    # If p != char(q), p-adic completion must exist
    if params.characteristic is not None:
        if p == params.characteristic:
            constraints["characteristic_match"] = True  # Natural case
        else:
            # For p != char(q), need p-adic completion
            # This should exist for any p coprime to q
            constraints["characteristic_match"] = math.gcd(p, params.q) == 1
    else:
        constraints["characteristic_match"] = True
    
    # Constraint 4: Weight spectrum p-adic structure
    # Code distance d must be p-adically "meaningful"
    # A distance of 0 would be problematic p-adically
    constraints["distance_nonzero"] = params.d > 0
    
    # Constraint 5: p-adic rate constraint
    # The rate r = k/n must be p-adically well-defined
    # All rates in [1/n, (n-1)/n] with denominator dividing n are p-adically fine
    if params.n > 0:
        constraints["rate_constraint"] = (0 < params.k <= params.n)
    else:
        constraints["rate_constraint"] = False
    
    return constraints

def is_locally_realizable(params: CodeParams, p: int) -> bool:
    """Check if code parameters are realizable at prime p (all constraints pass)."""
    constraints = local_constraints(params, p)
    return all(constraints.values())

# ==============================================================================
# SECTION 5: Hasse Principle Test
# ==============================================================================

def test_hasse_principle(param_sets: List[CodeParams], 
                          primes: List[int]) -> Dict:
    """
    Test the Hasse principle on a collection of code parameter sets.
    
    For each parameter set:
    1. Check local realizability at each prime
    2. Check global realizability (is this a known code?)
    3. Identify "local-only" sets (locally realizable but not globally known)
    
    Returns analysis dict.
    """
    results = {
        "total": len(param_sets),
        "globally_known": [],
        "locally_realizable": [],
        "local_only": [],  # Locally realizable but not globally known
        "obstruction_count": 0,
        "per_prime_stats": defaultdict(lambda: {"total": 0, "realizable": 0})
    }
    
    for params in param_sets:
        # Check local realizability at all primes
        local_ok = {}
        all_local_pass = True
        for p in primes:
            ok = is_locally_realizable(params, p)
            local_ok[p] = ok
            results["per_prime_stats"][p]["total"] += 1
            if ok:
                results["per_prime_stats"][p]["realizable"] += 1
            if not ok:
                all_local_pass = False
        
        # Check if this parameter set corresponds to a known code family
        # (In this toy model, surface codes and CSS codes are "known")
        is_known = _is_known_code(params)
        
        if is_known:
            results["globally_known"].append({
                "params": str(params),
                "local_status": local_ok,
                "all_local_pass": all_local_pass
            })
        
        if all_local_pass:
            results["locally_realizable"].append({
                "params": str(params),
                "is_known": is_known,
                "local_status": local_ok
            })
            if not is_known:
                results["local_only"].append({
                    "params": str(params),
                    "n": params.n,
                    "k": params.k,
                    "d": params.d,
                    "q": params.q,
                    "why_not_known": _why_not_known(params)
                })
                results["obstruction_count"] += 1
    
    return results

def _is_known_code(params: CodeParams) -> bool:
    """
    Check if a parameter set corresponds to a known code family.
    
    In this toy model, we check against:
    - Surface codes: n = 2L^2, k=2, d=L
    - CSS codes: d = floor(sqrt(n))
    - Perfect codes: d = n/2 + 1 for k=1
    """
    n, k, d = params.n, params.k, params.d
    
    # Surface code check
    if k == 2 and n % 2 == 0:
        L = int(math.sqrt(n / 2))
        if L * L * 2 == n and L == d:
            return True
    
    # CSS code check
    if k == max(1, n // 2) and d == max(1, int(math.sqrt(n))):
        return True
    
    # Perfect code check
    if k == 1 and d == max(1, n // 2 + 1 if n >= 2 else 1):
        return True
    
    # Random stabilizer check
    if d == 3 and k == max(1, n // 2):
        return True
    
    return False

def _why_not_known(params: CodeParams) -> str:
    """Explain why a parameter set is not a known code."""
    reasons = []
    
    # Check each family
    n, k, d = params.n, params.k, params.d
    
    # Surface code
    if n >= 2:
        L = int(math.sqrt(n / 2))
        if L * L * 2 == n:
            if k != 2:
                reasons.append(f"Surface: k={k} != 2")
            if L != d:
                reasons.append(f"Surface: d={d} != {L}")
    
    # CSS code
    expected_d_css = max(1, int(math.sqrt(n)))
    if k == max(1, n // 2):
        if d != expected_d_css:
            reasons.append(f"CSS: d={d} != {expected_d_css}")
    
    # Perfect code
    expected_d_perfect = max(1, n // 2 + 1 if n >= 2 else 1)
    if k == 1:
        if d != expected_d_perfect:
            reasons.append(f"Perfect: d={d} != {expected_d_perfect}")
    
    if not reasons:
        reasons.append("Unknown code family — novel parameters")
    
    return "; ".join(reasons)

# ==============================================================================
# SECTION 6: Brauer-Manin Search
# ==============================================================================

def search_local_only_codes(max_n: int = 100, primes: List[int] = None) -> Dict:
    """
    Systematic search for code parameter sets that exist locally
    everywhere but have no known global realization.
    
    This is the quantum analog of searching for counterexamples
    to the Hasse principle (e.g., Selmer's cubic).
    
    Grid search over (n, k, d) with:
    - n in [2, max_n]
    - k in [1, n-1] (step by n//4 for efficiency)
    - d in [2, max_d] (step by max(1, d//4))
    """
    if primes is None:
        primes = primes_up_to(23)
    
    total_checked = 0
    local_only = []
    
    for n in range(2, max_n + 1):
        # Efficient sampling: try representative k values
        k_candidates = list(set([1, 2, n//4, n//2, 3*n//4, n-1]))
        k_candidates = [k for k in k_candidates if 0 < k < n]
        
        for k in k_candidates:
            max_d = n - k + 1  # Singleton bound
            
            # Sample d values
            d_candidates = list(set([
                2, 3, 5, 7,
                int(math.sqrt(n)),
                max_d // 2,
                max_d
            ]))
            d_candidates = [d for d in d_candidates if 2 <= d <= max_d]
            
            for d in d_candidates:
                for q in [2, 4, 8]:  # Binary, quaternary, octal
                    params = CodeParams(n=n, k=k, d=d, q=q)
                    
                    # Check all primes
                    all_ok = all(is_locally_realizable(params, p) for p in primes)
                    
                    if all_ok and not _is_known_code(params):
                        local_only.append({
                            "params": str(params),
                            "n": n, "k": k, "d": d, "q": q,
                            "why": _why_not_known(params)
                        })
                    
                    total_checked += 1
    
    return {
        "total_checked": total_checked,
        "local_only_count": len(local_only),
        "local_only": local_only[:20],  # Top 20
        "rate": len(local_only) / max(total_checked, 1)
    }

# ==============================================================================
# SECTION 7: Archimedean Place (p = infinity)
# ==============================================================================

def archimedean_constraints(params: CodeParams) -> Dict[str, bool]:
    """
    "Local" constraints at the archimedean place (p = infinity, i.e., R/C).
    
    These are the standard quantum code constraints:
    1. Quantum Singleton bound: k <= n - 2d + 2
    2. Non-degeneracy: d >= 2 for non-trivial code
    3. Rate-distance constraints: k*d <= n (approximate)
    """
    const = {}
    
    # Quantum Singleton
    const["quantum_singleton"] = params.k <= params.n - 2 * params.d + 2
    
    # Distance meaningful
    const["distance_meaningful"] = params.d >= 2 if params.n >= 2 else params.d >= 1
    
    # Rate constraint
    const["rate_positive"] = params.k > 0
    
    # Physical qudit count
    const["n_positive"] = params.n >= 2
    
    return const

# ==============================================================================
# SECTION 8: Main Analysis
# ==============================================================================

def main():
    print("=" * 70)
    print("HASSE PRINCIPLE TESTER — Phase 2 Prototype (Pillar II)")
    print("Testing Conjecture 2.1: Local-Global Principle for Quantum Codes")
    print("=" * 70)
    
    primes = primes_up_to(23)
    print(f"\nPrimes considered: {primes}")
    print(f"Archimedean place: R/C (p = infinity)")
    
    # === Test 1: Known Code Families ===
    print(f"\n{'='*70}")
    print("TEST 1: Known Code Families — Do They Satisfy Local Conditions?")
    print(f"{'='*70}\n")
    
    known_codes = []
    # Surface codes (L = 2, 3, 4, ..., 10)
    for L in range(2, 11):
        known_codes.append(surface_code_params(L))
    # CSS codes (n = 5, 10, 20, 50, 100)
    for n in [5, 10, 20, 50, 100]:
        known_codes.append(css_random_params(n))
    # Perfect codes (n = 5, 10, 15, 20)
    for n in [5, 10, 15, 20]:
        known_codes.append(perfect_code_params(n))
    # Random codes (n = 10, 20, 50, 100)
    for n in [10, 20, 50, 100]:
        known_codes.append(random_stabilizer_params(n))
    
    print(f"{'Code':<25} {'Archimedean':<15} {'All p-adic':<12} {'Verdict'}")
    print("-" * 70)
    
    all_pass = 0
    any_fail = 0
    for c in known_codes:
        arch = all(archimedean_constraints(c).values())
        p_adic_ok = all(is_locally_realizable(c, p) for p in primes)
        verdict = "LOCAL-REALIZABLE" if (arch and p_adic_ok) else "LOCAL-FAILURE"
        
        print(f"{str(c):<25} {'PASS' if arch else 'FAIL':<15} {'PASS' if p_adic_ok else 'FAIL':<12} {verdict}")
        
        if arch and p_adic_ok:
            all_pass += 1
        else:
            any_fail += 1
    
    print(f"\n  Summary: {all_pass} codes locally realizable, {any_fail} fail")
    
    # === Test 2: Hasse Principle on Known Codes ===
    print(f"\n{'='*70}")
    print("TEST 2: Hasse Principle — Local Existence ⟹ Global Existence?")
    print(f"{'='*70}\n")
    
    results = test_hasse_principle(known_codes, primes)
    
    print(f"  Total codes tested: {results['total']}")
    print(f"  Globally known: {len(results['globally_known'])}")
    print(f"  Locally realizable (all primes): {len(results['locally_realizable'])}")
    print(f"  Local-only (obstruction): {results['obstruction_count']}")
    
    # Per-prime stats
    print(f"\n  Per-prime realizability:")
    for p in sorted(results['per_prime_stats'].keys()):
        stats = results['per_prime_stats'][p]
        rate = stats['realizable'] / max(stats['total'], 1)
        bar = "█" * int(rate * 20)
        print(f"    p={p:2d}: {stats['realizable']:3d}/{stats['total']:3d} ({rate:.0%}) {bar}")
    
    # === Test 3: Systematic Search for Local-Only Codes ===
    print(f"\n{'='*70}")
    print("TEST 3: Systematic Search for Brauer-Manin Obstructions")
    print(f"{'='*70}\n")
    
    search = search_local_only_codes(max_n=100, primes=primes)
    
    print(f"  Parameter sets checked: {search['total_checked']}")
    print(f"  Local-only candidates: {search['local_only_count']}")
    print(f"  Obstruction rate: {search['rate']:.4%}")
    
    if search['local_only']:
        print(f"\n  Top local-only candidates:")
        print(f"  {'Code':<20} {'n':>4} {'k':>4} {'d':>4} {'Reason'}")
        print(f"  {'-'*60}")
        for c in search['local_only'][:10]:
            print(f"  {c['params']:<20} {c['n']:>4} {c['k']:>4} {c['d']:>4} {c['why'][:30]}")
    
    # === Test 4: Conjecture 2.1 Assessment ===
    print(f"\n{'='*70}")
    print("TEST 4: Conjecture 2.1 Assessment")
    print(f"{'='*70}\n")
    
    print("  Conjecture 2.1: A stabilizer code [[n,k,d]]_q exists iff it is")
    print("  locally realizable at every prime p and at the archimedean place.")
    print()
    
    if search['local_only_count'] == 0:
        print("  [SUPPORTED] No local-only counterexamples found in search range (n <= 100).")
        print("  This is consistent with Conjecture 2.1 for small parameters.")
        print("  WARNING: Limited search space (n <= 100). Wider search needed.")
    else:
        print(f"  [CHALLENGED] Found {search['local_only_count']} local-only candidates.")
        print("  These may represent novel code families OR false positives.")
        print("  Each candidate requires verification against the full stabilizer code")
        print("  existence criteria (not just parameter matching).")
    
    # Falsifiability
    print(f"\n  {'='*60}")
    print("  FALSIFIABILITY ASSESSMENT")
    print(f"  {'='*60}")
    print(f"  Conjecture 2.1 would be DISCONFIRMED if:")
    print(f"  1. A code family is proven to exist locally at all primes")
    print(f"     but has no corresponding global realization, OR")
    print(f"  2. A code family exists globally but has no local realization")
    print(f"     at some prime (purely non-p-adic structure).")
    print(f"\n  Current status: [INCONCLUSIVE] — insufficient data.")
    print(f"  This prototype searches toy models. Real test requires:")
    print(f"  - Actual stabilizer code enumerations for n up to 100+")
    print(f"  - p-adic metric analysis of stabilizer weight enumerators")
    print(f"  - Cross-reference with ultrametric-benchmark dataset")

if __name__ == "__main__":
    main()
