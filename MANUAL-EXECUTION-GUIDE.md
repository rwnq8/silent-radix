# MANUAL EXECUTION GUIDE — Silent Radix Research Program Publication

## Step 1: Sync Skills to R2

```powershell
# This uploads all skills (including the newly created publication-publisher) to Cloudflare R2
python "G:\My Drive\DeepChat\tools\bootstrap_skills.py" --sync
```

## Step 2: Restart DeepChat

```powershell
# REQUIRED — skills load at application startup
powershell -ExecutionPolicy Bypass -File "C:\Users\LENOVO\.deepchat\skills\skill-sync\scripts\restart_deepchat.ps1"
```

After restart, `skill_view('publication-publisher')` will be available.

## Step 3: Publish to Zenodo

```powershell
# Set Zenodo token (obtain at https://zenodo.org/account/settings/applications/)
$env:ZENODO_TOKEN = "your-token-here"

# Dry run — verify all artifacts present
python zenodo_upload_silent_radix.py --dry-run

# Actual upload
python zenodo_upload_silent_radix.py
```

This creates a Zenodo deposition, uploads all 8 artifacts, and publishes.

**Output:** A DOI like `10.5281/zenodo.XXXXX`. Also written to `SLT_RADIX_DOI.txt`.

## Step 4: Post to Social Media via Buffer

```powershell
# Set Buffer token (obtain at https://buffer.com/developers/api)
$env:BUFFER_ACCESS_TOKEN = "your-token-here"

# Use DOI from Step 3
$env:SLT_RADIX_DOI = "10.5281/zenodo.XXXXX"

# Preview posts without creating
python buffer_post_silent_radix.py --doi $env:SLT_RADIX_DOI --dry-run

# List configured Buffer profiles
python buffer_post_silent_radix.py --list

# Schedule 6 posts with staggered timing over 5 days
python buffer_post_silent_radix.py --doi $env:SLT_RADIX_DOI

# OR: Post immediately (no scheduling)
python buffer_post_silent_radix.py --doi $env:SLT_RADIX_DOI --now
```

Posts will appear at https://buffer.com/app. Schedule:
- Post 1 (Launch): T+0h — Twitter, LinkedIn, Bluesky
- Post 2 (Thesis): T+24h — Twitter, Bluesky
- Post 3 (Ultrametric): T+48h — Twitter, Bluesky
- Post 4 (Design): T+72h — Twitter
- Post 5 (Foundation): T+96h — LinkedIn
- Post 6 (Summary): T+120h — Twitter, Bluesky

## Step 5: (Optional) Submit Synthesis Paper to arXiv

Convert `silent-radix-synthesis-paper-v1.0.md` to LaTeX and submit via https://arxiv.org/submit
Suggested category: `math.HO` (History and Overview) or `cs.LO` (Logic in Computer Science)

---

## Files Ready for Publication

| # | File | Content |
|---|------|---------|
| 1 | `silent-radix-synthesis-paper-v1.0.md` | Core synthesis paper (9 sections, 21 refs) |
| 2 | `consequence-atlas-v1.0.md` | 50-entry error catalog |
| 3 | `consequence-atlas-supplement-v1.0.md` | 15 additional entries |
| 4 | `formal-appendix-silent-radix-theorem.md` | 8 formal theorems |
| 5 | `explicit-frame-pattern-language-v1.0.md` | 9 design patterns |
| 6 | `lof-number-builder-specification-v1.0.md` | Interactive tool spec |
| 7 | `cross-reference-index-v1.0.md` | Atlas↔Paper mapping |
| 8 | `README-silent-radix-research-program.md` | Master index |

## Publication Scripts

| # | File | Purpose |
|---|------|---------|
| 9 | `zenodo_upload_silent_radix.py` | Zenodo deposition + artifact upload |
| 10 | `zenodo-metadata.json` | Deposition metadata (backup) |
| 11 | `publication-manifest.json` | Artifact inventory (backup) |
| 12 | `buffer_post_silent_radix.py` | Buffer GraphQL API posting |

## Quick-Start Checklist

- [ ] Token files exist: `%USERPROFILE%\.zenodo_token` and `%USERPROFILE%\.buffer_token`
- [ ] All 8 artifacts present in `G:\My Drive\DeepChat\`
- [ ] `python zenodo_upload_silent_radix.py --dry-run` → all OK
- [ ] `python buffer_post_silent_radix.py --list` → profiles visible
- [ ] `python zenodo_upload_silent_radix.py` → DOI obtained
- [ ] `python buffer_post_silent_radix.py --doi 10.5281/zenodo.XXXXX` → posts scheduled
- [ ] Verify at https://zenodo.org and https://buffer.com/app

---

*Manual Execution Guide — Silent Radix Research Program v1.0. Updated with Python GraphQL scripts.*
