import re

path = r"projects/braided-memory-register/POSITION-PAPER.md"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

banned = [
    "Module N", "Task N", "SPRINT", "PROCEED", "RESUME",
    "PROJECT STATE", "0.N.py", "0.N.md", "cp1252",
    "ready for handoff", "new agent starting from cold"
]
violations = {t: text.count(t) for t in banned if t in text}
print("Language Gate:", "FAIL" if violations else "PASS", violations)

has_author = "**Author:**" in text
has_date = "**Date:**" in text
has_license = "**License:**" in text
print("Author block:", "PASS" if all([has_author, has_date, has_license]) else "FAIL")

bare = ["α", "β", "γ", "δ", "ε", "π", "σ", "∞", "∑", "∫", "√", "≤", "≥", "≠"]
bare_hits = [c for c in bare if c in text]
print("Math format:", "PASS" if not bare_hits else "FAIL", bare_hits)

citations = re.findall(r"\[@(\w+(?:[,;\s]+@\w+)*)\]", text)
print("Citations:", len(citations), "found")

overall = not violations and all([has_author, has_date, has_license]) and not bare_hits
print("Overall:", "PASS" if overall else "FAIL")
