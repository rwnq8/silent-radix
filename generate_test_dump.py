#!/usr/bin/env python3
"""
Generate a synthetic Wikipedia-like SQL dump for UVR pipeline testing.
Creates a small but realistic dataset with a known ultrametric structure
from the Wikipedia category hierarchy.

Produces:
  - enwiki-test-page.sql.gz    (~1000 articles)
  - enwiki-test-categorylinks.sql.gz (hierarchical category assignments)
  - enwiki-test-pagelinks.sql.gz     (cross-article links)
  - enwiki-test-category.sql.gz      (category definitions)
"""

import gzip
import random
import sys
from pathlib import Path

random.seed(42)

# ─── Category Tree (Ultrametric by construction) ──────────────────
CATEGORIES = {
    # Level 0: Root
    1: ("Science", 0),
    2: ("Arts", 0),
    3: ("History", 0),
    
    # Level 1: Science subcategories
    10: ("Physics", 1),
    11: ("Mathematics", 1),
    12: ("Computer_Science", 1),
    13: ("Biology", 1),
    
    # Level 1: Arts subcategories  
    20: ("Literature", 2),
    21: ("Music", 2),
    22: ("Visual_Arts", 2),
    
    # Level 1: History subcategories
    30: ("Ancient_History", 3),
    31: ("Modern_History", 3),
    
    # Level 2: Physics subcategories
    100: ("Quantum_Mechanics", 10),
    101: ("General_Relativity", 10),
    102: ("Statistical_Mechanics", 10),
    
    # Level 2: Mathematics subcategories
    110: ("Number_Theory", 11),
    111: ("Algebraic_Geometry", 11),
    112: ("Topology", 11),
    113: ("p-adic_Analysis", 11),  # <-- Key category for our research!
    
    # Level 2: CS subcategories
    120: ("Artificial_Intelligence", 12),
    121: ("Quantum_Computing", 12),
    
    # Level 3: Advanced subcategories
    1000: ("Ultrametric_Spaces", 110),      # Number_Theory → Ultrametric_Spaces
    1001: ("p-adic_Numbers", 110),           # Number_Theory → p-adic_Numbers
    1002: ("Bruhat-Tits_Buildings", 111),    # Algebraic_Geometry → Bruhat-Tits
    1003: ("Loop_Quantum_Gravity", 100),     # Quantum_Mechanics → LQG
    1004: ("Problem_of_Time", 100),           # Quantum_Mechanics → Problem of Time
    1005: ("Page-Wootters_Formalism", 1004),  # Problem_of_Time → Page-Wootters
    1006: ("Wheeler-DeWitt_Equation", 1003),  # LQG → Wheeler-DeWitt
    1007: ("AdS-CFT_Correspondence", 101),    # GR → AdS/CFT
    1008: ("p-adic_AdS-CFT", 1007),           # AdS/CFT → p-adic AdS/CFT (bridge!)
    1009: ("Adelic_Physics", 1001),            # p-adic_Numbers → Adelic Physics
    1010: ("Category_Theory", 112),            # Topology → Category Theory
    1011: ("Topos_Physics", 1010),             # Category Theory → Topos Physics
    
    # ── Subcategory IDs referenced by ARTICLES ──
    40: ("Bruhat-Tits_building", 1002),       # Bruhat-Tits building category
    41: ("Building_(mathematics)", 1002),
    42: ("Reductive_group", 111),
    43: ("Tits_system", 1002),
    44: ("Weyl_group_cat", 111),
    45: ("Affine_Weyl_group", 1002),
    46: ("Perfectoid_space", 111),
    47: ("Scheme_(mathematics)", 111),
    60: ("p-adic_quantum_mechanics", 113),
    61: ("Adelic_physics", 1009),
    62: ("p-adic_string_theory", 1009),
    63: ("p-adic_AdS/CFT", 1008),
    64: ("Ultrametric_correlation_hierarchy", 1000),
    65: ("Spin_glass", 102),
    66: ("Replica_trick", 102),
    67: ("Parisis_ultrametricity", 102),
    70: ("Quantum_computing", 121),
    71: ("Qubit", 121),
    72: ("Quantum_error_correction", 121),
    73: ("Topological_quantum_computer", 121),
    104: ("Atomic_clock", 1004),
    103: ("Clock", 1004),
}

# ─── Articles with known ultrametric structure ────────────────────
ARTICLES = [
    # Physics — Quantum Gravity cluster
    (1, "Quantum_gravity", 100, 0),
    (2, "Wheeler–DeWitt_equation", 1006, 0),
    (3, "Problem_of_time", 1004, 0),
    (4, "Page–Wootters_formalism", 1005, 0),
    (5, "Loop_quantum_gravity", 1003, 0),
    (6, "Canonical_quantum_gravity", 1003, 0),
    (7, "Diffeomorphism_invariance", 1003, 0),
    (8, "Hamiltonian_constraint", 1006, 0),
    (9, "Conditional_quantum_state", 1005, 0),
    (10, "Relational_quantum_mechanics", 1005, 0),
    
    # Physics — General Relativity cluster
    (20, "General_relativity", 101, 0),
    (21, "Black_hole", 101, 0),
    (22, "AdS/CFT_correspondence", 1007, 0),
    (23, "Holographic_principle", 1007, 0),
    (24, "Event_horizon", 101, 0),
    
    # Mathematics — Number Theory cluster
    (30, "p-adic_number", 1001, 0),
    (31, "Ultrametric_space", 1000, 0),
    (32, "Strong_triangle_inequality", 1000, 0),
    (33, "Ostrowski's_theorem", 1001, 0),
    (34, "Valuation_(algebra)", 1001, 0),
    (35, "Hensel's_lemma", 1001, 0),
    (36, "p-adic_analysis", 113, 0),
    (37, "Non-Archimedean_geometry", 113, 0),
    
    # Mathematics — Algebraic Geometry cluster
    (40, "Bruhat–Tits_building", 1002, 0),
    (41, "Building_(mathematics)", 1002, 0),
    (42, "Reductive_group", 111, 0),
    (43, "Tits_system", 1002, 0),
    (44, "Weyl_group", 42, 0),
    (45, "Affine_Weyl_group", 1002, 0),
    (46, "Perfectoid_space", 111, 0),
    (47, "Scheme_(mathematics)", 111, 0),
    
    # Mathematics — Topology/Category Theory cluster
    (50, "Category_theory", 1010, 0),
    (51, "Topos", 1010, 0),
    (52, "Topos_quantum_mechanics", 1011, 0),
    (53, "Categorical_quantum_mechanics", 1011, 0),
    (54, "Sheaf_(mathematics)", 112, 0),
    
    # Bridge articles (connecting both clusters!)
    (60, "p-adic_quantum_mechanics", 113, 0),  # Math but quantum
    (61, "Adelic_physics", 1009, 0),            # Math + Physics
    (62, "p-adic_string_theory", 1009, 0),
    (63, "p-adic_AdS/CFT", 1008, 0),
    (64, "Ultrametric_correlation_hierarchy", 1000, 0),  # Directly on our topic
    (65, "Spin_glass", 102, 0),                         # Ultrametrics in physics
    (66, "Replica_trick", 102, 0),
    (67, "Parisis_ultrametricity", 102, 0),
    
    # CS cluster
    (70, "Quantum_computing", 121, 0),
    (71, "Qubit", 121, 0),
    (72, "Quantum_error_correction", 121, 0),
    (73, "Topological_quantum_computer", 121, 0),
    
    # Literature/Arts cluster (control group — should be ultrametrically distant)
    (80, "William_Shakespeare", 20, 0),
    (81, "Hamlet", 20, 0),
    (82, "Sonnet", 20, 0),
    (83, "Beethoven", 21, 0),
    (84, "Symphony_No._5", 21, 0),
    (85, "Mona_Lisa", 22, 0),
    
    # History cluster (control group)
    (90, "Ancient_Rome", 30, 0),
    (91, "Julius_Caesar", 30, 0),
    (92, "World_War_II", 31, 0),
    (93, "Industrial_Revolution", 31, 0),
    
    # More bridge articles
    (100, "Time_in_physics", 1004, 0),
    (101, "Arrow_of_time", 102, 0),
    (102, "Entropy", 102, 0),
    (103, "Clock", 1004, 0),
    (104, "Atomic_clock", 103, 0),
    (105, "Thermodynamics", 102, 0),
    
    # Math foundations
    (110, "Prime_number", 110, 0),
    (111, "Number_theory", 110, 0),
    (112, "Riemann_zeta_function", 110, 0),
    (113, "Algebraic_geometry", 111, 0),
    (114, "Scheme_theory", 113, 0),
    
    # Redirection articles
    (200, "Wheeler-DeWitt", 1006, 1),  # is_redirect=1
    (201, "Page-Wootters", 1005, 1),
    (202, "BT_building", 1002, 1),
]

# ─── Cross-links (pagelinks) ──────────────────────────────────────
# Source → [targets]
PAGELINKS = {
    1: [2, 3, 4, 5, 6, 103],           # Quantum_gravity links to related physics
    2: [1, 3, 4, 5, 8, 30],             # Wheeler-DeWitt connects to p-adic!
    3: [1, 2, 4, 100, 101, 103],         # Problem_of_time
    4: [1, 2, 3, 9, 10, 103],            # Page-Wootters
    5: [1, 2, 6, 7, 8, 60],              # LQG links to p-adic QM!
    6: [1, 2, 5, 7, 8],                  # Canonical QG
    7: [5, 6, 8, 20, 23],                # Diffeomorphism invariance
    8: [2, 6, 7, 30],                    # Hamiltonian constraint
    9: [4, 10, 64],                       # Conditional quantum state → bridge!
    10: [4, 9, 52, 53],                   # Relational QM → topos
    20: [21, 22, 23, 24, 101],            # GR
    21: [20, 22, 23, 24],                 # Black hole
    22: [20, 21, 23, 63, 60],             # AdS/CFT → p-adic AdS/CFT!
    23: [20, 22, 41, 63],                 # Holographic principle
    24: [20, 21],                         # Event horizon
    
    # Math cluster
    30: [31, 32, 33, 34, 35, 36, 37, 60, 61, 62, 110, 111],  # p-adic → bridge!
    31: [30, 32, 34, 64, 65, 66, 67],     # Ultrametric → spin glass
    32: [30, 31, 34, 37],                 # Strong triangle inequality
    33: [30, 34, 36, 37],                 # Ostrowski
    34: [30, 31, 33, 35, 37],             # Valuation
    35: [30, 34, 36],                     # Hensel
    36: [30, 31, 33, 35, 37, 60, 61],     # p-adic analysis
    37: [30, 31, 36, 46, 47, 60],         # Non-Archimedean geometry
    40: [30, 31, 41, 42, 43, 44, 45, 64, 2],  # Bruhat-Tits → ultrametric → physics!
    41: [40, 42, 43, 44],                 # Building
    42: [40, 41, 43, 44, 46, 47],         # Reductive group
    43: [40, 41, 42, 45],                 # Tits system
    44: [40, 42, 43, 45],                 # Weyl group
    45: [40, 43, 44],                     # Affine Weyl
    46: [30, 37, 47, 60, 63],             # Perfectoid
    47: [37, 42, 46, 54, 113, 114],       # Scheme
    
    # Category/Topos cluster
    50: [51, 52, 53, 54],                 # Category theory
    51: [50, 52, 53, 54],                 # Topos
    52: [50, 51, 53, 10, 4],              # Topos QM → physics
    53: [50, 51, 52],                     # Categorical QM
    54: [50, 51, 37, 46, 47],             # Sheaf
    
    # Bridge articles
    60: [30, 36, 37, 61, 62, 63, 64, 2, 5, 22],  # p-adic QM
    61: [30, 36, 60, 62, 63],                       # Adelic physics
    62: [30, 36, 60, 61, 63],                       # p-adic string
    63: [30, 36, 60, 61, 62, 22, 23, 46],            # p-adic AdS/CFT
    64: [30, 31, 32, 4, 9, 40, 60, 65, 67],         # Ultrametric correlation hierarchy
    65: [31, 64, 66, 67, 102],                       # Spin glass
    66: [65, 67],                                    # Replica trick
    67: [31, 64, 65, 66],                            # Parisi ultrametricity
    
    # CS cluster
    70: [71, 72, 73, 121],                 # Quantum computing
    71: [70, 72, 73],                      # Qubit
    72: [70, 71, 73],                      # QEC
    73: [70, 71, 72],                      # Topological QC
    
    # History
    90: [91, 92, 93],                      # Ancient Rome
    91: [90, 92],                          # Caesar
    92: [90, 91, 93],                      # WWII
    93: [90, 92],                          # Industrial Revolution
    
    # Time in physics
    100: [3, 4, 101, 102, 103],            # Time in physics
    101: [100, 102, 3],                    # Arrow of time
    102: [100, 101, 105, 65],              # Entropy → spin glass
    103: [100, 4, 104],                    # Clock
    104: [100, 103],                       # Atomic clock
    105: [102, 100],                       # Thermodynamics
    
    # Math foundations
    110: [30, 33, 35, 111, 112],           # Prime number
    111: [30, 110, 112, 113, 114],         # Number theory
    112: [30, 110, 111],                   # Zeta function
    113: [40, 42, 46, 47, 111, 114],       # Algebraic geometry
    114: [46, 47, 113],                     # Scheme theory
}


def make_insert(table, columns, rows, chunk_size=20):
    """Generate INSERT INTO statements for MySQL dump format, split into chunks."""
    col_str = ', '.join(f'`{c}`' for c in columns)
    statements = []
    for i in range(0, len(rows), chunk_size):
        chunk = rows[i:i+chunk_size]
        values = []
        for row in chunk:
            vals = []
            for v in row:
                if v is None:
                    vals.append('NULL')
                elif isinstance(v, int):
                    vals.append(str(v))
                else:
                    escaped = str(v).replace('\\', '\\\\').replace("'", "\\'")
                    vals.append(f"'{escaped}'")
            values.append(f"({', '.join(vals)})")
        statements.append(f"INSERT INTO `{table}` ({col_str}) VALUES " + ', '.join(values) + ';\n')
    return ''.join(statements)


def generate_category_sql():
    """Generate category.sql.gz."""
    rows = []
    for cat_id, (title, parent) in CATEGORIES.items():
        rows.append((cat_id, title, 0, 0, 0))  # (cat_id, cat_title, cat_pages, cat_subcats, cat_files)
    
    sql = make_insert('category', ['cat_id', 'cat_title', 'cat_pages', 'cat_subcats', 'cat_files'], rows)
    path = Path('enwiki-test/enwiki-test-category.sql.gz')
    path.parent.mkdir(parents=True, exist_ok=True)
    with gzip.open(path, 'wt', encoding='utf-8') as f:
        f.write(sql)
    print(f"  Generated {path} with {len(rows)} categories")

def generate_categorylinks_sql():
    """Generate categorylinks.sql.gz — hierarchical tree structure."""
    rows = []
    # Each article gets its own category plus parent categories
    for page_id, _, cat_id, _ in ARTICLES:
        # Direct category
        rows.append((page_id, f'Category:{CATEGORIES[cat_id][0]}', cat_id))
        # Add parent categories up the tree
        current = CATEGORIES[cat_id][1]
        while current > 0:
            rows.append((page_id, f'Category:{CATEGORIES[current][0]}', current))
            current = CATEGORIES[current][1]
        # Always add root
        root_id = CATEGORIES[cat_id][1]
        if root_id == 0:
            # Find which root
            for root_cat in [1, 2, 3]:
                if cat_id == root_cat:
                    break
                # Walk up to find root
                c = cat_id
                found_root = c
                while CATEGORIES.get(c, (None, 0))[1] != 0:
                    c = CATEGORIES[c][1]
                rows.append((page_id, f'Category:{CATEGORIES[c][0]}', c))

    # Deduplicate
    seen = set()
    unique = []
    for r in rows:
        key = (r[0], r[2])
        if key not in seen:
            seen.add(key)
            unique.append(r)

    sql = make_insert('categorylinks', ['cl_from', 'cl_to', 'cl_sortkey', 'cl_type'], 
                      [(pid, title, cat_id, 'page') for pid, title, cat_id in unique])
    path = Path('enwiki-test/enwiki-test-categorylinks.sql.gz')
    with gzip.open(path, 'wt', encoding='utf-8') as f:
        f.write(sql)
    print(f"  Generated {path} with {len(unique)} category links")

def generate_page_sql():
    """Generate page.sql.gz."""
    rows = []
    for page_id, title, _, is_redirect in ARTICLES:
        namespace = 0  # Main namespace
        rows.append((page_id, namespace, title, is_redirect, 0, 'wikitext'))
    
    sql = make_insert('page', ['page_id', 'page_namespace', 'page_title', 'page_is_redirect', 'page_is_new', 'page_content_model'], rows)
    path = Path('enwiki-test/enwiki-test-page.sql.gz')
    with gzip.open(path, 'wt', encoding='utf-8') as f:
        f.write(sql)
    print(f"  Generated {path} with {len(rows)} pages")

def generate_pagelinks_sql():
    """Generate pagelinks.sql.gz — cross-article links."""
    rows = []
    for source_id, targets in PAGELINKS.items():
        for target_id in targets:
            # Get target title
            target_title = None
            for pid, title, _, _ in ARTICLES:
                if pid == target_id:
                    target_title = title
                    break
            if target_title:
                rows.append((source_id, 0, target_title))
    
    sql = make_insert('pagelinks', ['pl_from', 'pl_namespace', 'pl_title'], rows)
    path = Path('enwiki-test/enwiki-test-pagelinks.sql.gz')
    with gzip.open(path, 'wt', encoding='utf-8') as f:
        f.write(sql)
    print(f"  Generated {path} with {len(rows)} pagelinks")

def generate_summary():
    """Write a summary of the test dataset."""
    lines = [
        "# Wikipedia Test Dataset for UVR Pipeline",
        "",
        "## Dataset Structure",
        f"- {len(ARTICLES)} articles across multiple clusters",
        f"- {len(CATEGORIES)} categories in a 4-level ultrametric tree",
        f"- {sum(len(v) for v in PAGELINKS.values())} cross-article links",
        "",
        "## Expected Ultrametric Properties",
        "",
        "The dataset is constructed with known ultrametric structure:",
        "1. **Physics cluster** (Quantum Gravity, Page-Wootters, Wheeler-DeWitt): tightly linked",
        "2. **Math cluster** (p-adic numbers, Bruhat-Tits, ultrametric spaces): tightly linked", 
        "3. **Bridge articles** (p-adic quantum mechanics, ultrametric correlation hierarchy): connecting both",
        "4. **Control group** (Arts, History): ultrametrically distant from both clusters",
        "",
        "## Expected UVR Pipeline Results",
        "",
        "- **UVR** should be low (< 0.3) due to hierarchical category structure",
        "- **Walk Entropy** should show logarithmic scaling with category depth",
        "- **Serendipity Quotient** should detect bridge articles as non-obvious connections",
        "",
        "## Running",
        "```bash",
        "python wikipedia_uvr_pipeline.py --dump-dir ./enwiki-test/ --sample 5000",
        "```",
    ]
    path = Path('enwiki-test/README.md')
    with open(path, 'w') as f:
        f.write('\n'.join(lines))

if __name__ == '__main__':
    print("Generating Wikipedia test dataset for UVR pipeline...")
    generate_category_sql()
    generate_page_sql()
    generate_categorylinks_sql()
    generate_pagelinks_sql()
    generate_summary()
    print("\n[DONE] Test dataset generated in ./enwiki-test/")
    print("Run: python wikipedia_uvr_pipeline.py --dump-dir ./enwiki-test/ --sample 5000")
