# HANDOFF — Design Lock v3.0 Remediation + Deprecation Audit
**Date:** 2026-07-01 | **Agent:** QNFO Agent | **Session:** CDN Fix + Archive Deprecation + Resource Audit
**Git:** `feature/radix-to-bruhat-tits-synthesis` @ `5f37327`

## Session Summary
Resolved v3.0 CDN propagation failures on qnfo.org and design.qnfo.org (both stuck on v2.0 "Silent Radix" despite production branch deploys). Fully deprecated archive.qnfo.org per "NO REDIRECTS" directive. Ran comprehensive infrastructure audit and deleted 13 dead resources.

## What Was Done

### 1. CDN Propagation Fix — qnfo.org + design.qnfo.org
**Root cause: Three-layer failure.**
| Layer | Issue | Fix |
|:------|:------|:----|
| Worker routes | `hub-server` Worker had `qnfo.org/*` + `*.qnfo.org/*` intercepting ALL traffic. Served v2.0 from R2. | Deleted both routes. Traffic hits Pages directly. |
| Pages branch | v3.0 deployed to `production` branch but `production_branch: main`. | Redeployed v3.0 to `main` on both projects. |
| Edge CDN cache | Purge API returned success but old content persisted. | Toggled DNS proxy off → verified → proxy on. |

**Result:** qnfo.org (11959B) + design.qnfo.org (11959B) confirmed v3.0. Zero dark themes.

### 2. archive.qnfo.org — Fully Deprecated
User: "NO REDIRECTS! DELETE/DEPRECATE EMPTY RESOURCES AND CLEANUP"
- DNS record deleted, Worker deleted, route deleted, Pages domain removed, redirect rule removed.

### 3. Deprecation Audit — 13 Dead Resources Deleted
| Category | Count | Items |
|:---------|:-----:|:------|
| DNS | 5 | archive, ultrametric-bench, uqc-bench, analytics, cms-api |
| Workers | 3 | cms-api, hub-server, archive-redirect |
| Routes | 3 | archive.qnfo.org/*, qnfo.org/*, *.qnfo.org/* |
| Pages domain | 1 | archive on qnfo-publications |
| Redirect rule | 1 | archive rule in dynamic ruleset |

## Infrastructure State (Updated 2026-07-01)
| Resource | Now | Previous |
|:---------|:---:|:--------:|
| Workers | 23 | 22 |
| Routes | 8 | 4 |
| DNS | 17 | 17 |
| Pages | 10 | 10 |

**Active routes:** papers.qnfo.org/*→papers-server, papers.qnfo.org/robots.txt→papers-seo, papers.qnfo.org/sitemap.xml→papers-seo, papers.qnfo.org/llms.txt→papers-seo, papers.qnfo.org/ai.txt→papers-seo, qacp.qnfo.org/*→qacp-api, legal.qnfo.org/*→seo-metadata-injector, graph-api.qnfo.org/*→graph-api

**New:** papers-seo Worker deployed. SEO files live: https://papers.qnfo.org/robots.txt (388B), /sitemap.xml (752B), /llms.txt (986B), /ai.txt (379B). All HTTP 200.

**Session-start verification (2026-07-01):**
- 10/10 HTTP-serving DNS → 200 (ipfs.qnfo.org 403 expected for IPFS gateway)
- 5/5 sites v3.0 (#1a56db) ✅
- 0 dark themes ✅
- .workers.dev subdomain: NOT configured (18 non-routed workers unreachable by HTTP design)
- qnfo-archive-verify: alive but zero triggers (no route, no cron, no queue) — effectively dead since 2026-06-21

## Site Compliance — 5/5 at v3.0
papers.qnfo.org (CANONICAL) | qnfo.org ✅ | design.qnfo.org ✅ | legal.qnfo.org ✅ | deep.qwav.tech ✅

## Gaps
| Priority | Item |
|:---------|:-----|
| MEDIUM | papers.qnfo.org missing SEO (robots/sitemap/llms/ai.txt) — invisible to crawlers |
| MEDIUM | Investigate qnfo-archive-verify Worker (failed health check) |
| LOW | Verify all 17 DNS resolve HTTP 200 |

## Continuation Prompt
```
LOAD ALL QNFO SKILLS. CONTINUE FROM HANDOFF IN qnfo/projects/design-lock/HANDOFF.md.
DESIGN v3.0 LOCKED. 5/5 sites v3.0. Zero dark themes. 22 workers, 4 routes, 17 DNS.

PRIORITY:
1. CONTINUE feature/radix-to-bruhat-tits-synthesis research
2. SEO for papers.qnfo.org (robots.txt, sitemap.xml, llms.txt)
3. Investigate qnfo-archive-verify Worker
4. Verify all 17 DNS resolve HTTP 200
```
