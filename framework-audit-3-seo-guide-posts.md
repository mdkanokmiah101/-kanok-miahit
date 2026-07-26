# Framework Audit Report — 3 SEO Guide Posts
**Date:** 2026-07-20 | **Auditor:** Hermes Agent

---

## Post 1: seo-expert-vs-seo-agency-dhaka-which-is-right
**Title:** SEO Expert vs SEO Agency in Dhaka: Which One is Right for Your Business?
**Date:** 2026-07-14 | **Tags:** SEO Expert Dhaka, SEO Agency Dhaka, SEO Services Bangladesh, Hire SEO
**Content:** 15,384 chars

| # | Check | Status | Detail |
|---|-------|--------|--------|
| A | TF-IDF | ✅ PASS | 'SEO Expert' appears 23x (min 5) |
| B | Entities | ✅ PASS | Dhaka ✓, Bangladesh ✓, SEO expert ✓, SEO agency ✓ |
| C | Pillar Link | ✅ PASS | Links to `/services` (broader services hub) |
| D | AEO/GEO | ✅ PASS | 4 question headings found |
| E | Internal Links | ✅ PASS | 6 total (1 blog + 2 services + 0 locations + 3 industries) |
| F | Schema | ✅ PASS | title ✓, excerpt ✓, date ✓ |

**Result: ✅ 0/6 FLAGS — PASS**

---

## Post 2: top-10-seo-mistakes-dhaka-businesses-fix
**Title:** Top 10 SEO Mistakes Dhaka Businesses Make (And How to Fix Them)
**Date:** 2026-07-14 | **Tags:** SEO Mistakes, Dhaka SEO, SEO Tips Bangladesh, SEO Expert Dhaka
**Content:** 27,914 chars

| # | Check | Status | Detail |
|---|-------|--------|--------|
| A | TF-IDF | ✅ PASS | 'SEO Mistakes' appears 8x (min 5) |
| B | Entities | ❌ FAIL | Missing: **SEO agency** (0 occurrences) |
| C | Pillar Link | ❌ FAIL | No link to `/services/seo`; services links go to sub-pages (local-seo, on-page-seo, technical-seo, ecommerce-seo) |
| D | AEO/GEO | ✅ PASS | 4 question headings found |
| E | Internal Links | ✅ PASS | 6 total (0 blog + 6 services + 0 locations + 0 industries) |
| F | Schema | ✅ PASS | title ✓, excerpt ✓, date ✓ |

**Result: ⚠️ 2/6 FLAGS**

**Fixes needed:**
- 🔴 Add mention of "SEO agency" in content (entity missing)
- 🔴 Add link to pillar page `/services/seo` or `/services`

---

## Post 3: hiring-seo-expert-dhaka-better-roi-than-paid-ads
**Title:** Why Hiring an SEO Expert in Dhaka Delivers Better ROI Than Paid Ads
**Date:** 2026-07-14 | **Tags:** SEO ROI, SEO vs Ads, Dhaka SEO Expert, Digital Marketing Bangladesh
**Content:** 25,445 chars

| # | Check | Status | Detail |
|---|-------|--------|--------|
| A | TF-IDF | ❌ FAIL | 'SEO Expert' appears **0x** (min 5) — body uses "SEO Consultant" (11x) instead |
| B | Entities | ❌ FAIL | Missing: **SEO expert** (0x), **SEO agency** (0x) — body says "SEO Consultant" |
| C | Pillar Link | ❌ FAIL | No link to `/services/seo`; only link is `/services/local-seo` |
| D | AEO/GEO | ✅ PASS | 13 question headings found |
| E | Internal Links | ❌ FAIL | Only **1 internal link** (min 3): `/services/local-seo` |
| F | Schema | ✅ PASS | title ✓, excerpt ✓, date ✓ |

**Result: ⚠️ 4/6 FLAGS**

**Fixes needed:**
- 🔴 Use "SEO Expert" in content body (currently uses "SEO Consultant" 11x) — mismatch with title
- 🔴 Add mention of "SEO agency" in content
- 🔴 Add link to pillar page `/services/seo`
- 🔴 Add 2+ more internal links to `/blog/`, `/services/`, `/locations/`, or `/industries/`

---

## Executive Summary

| # | Slug | Flags | Status |
|---|------|-------|--------|
| 1 | seo-expert-vs-seo-agency-dhaka-which-is-right | 0/6 | ✅ PASS |
| 2 | top-10-seo-mistakes-dhaka-businesses-fix | 2/6 | ⚠️ FAIL |
| 3 | hiring-seo-expert-dhaka-better-roi-than-paid-ads | 4/6 | ⚠️ FAIL |

**Total: 6 flags across 3 posts (12 of 18 checks passing)**

### Per-Check Summary

| Check | Post 1 | Post 2 | Post 3 |
|-------|--------|--------|--------|
| A. TF-IDF | ✅ 23x 'SEO Expert' | ✅ 8x 'SEO Mistakes' | ❌ 0x 'SEO Expert' |
| B. Entities | ✅ All present | ❌ 'SEO agency' missing | ❌ 'SEO expert','SEO agency' missing |
| C. Pillar Link | ✅ /services | ❌ No link | ❌ No link |
| D. AEO/GEO | ✅ 4 questions | ✅ 4 questions | ✅ 13 questions |
| E. Int Links | ✅ 6 links | ✅ 6 links | ❌ 1 link |
| F. Schema | ✅ All set | ✅ All set | ✅ All set |

### Key Findings

1. **Post 3 has title/body keyword mismatch**: Title says "SEO Expert" but body uses "SEO Consultant" (11x). Zero occurrences of the primary keyword in content.
2. **Post 2 and Post 3 lack pillar page links**: Neither links to `/services/seo` or `/services`.
3. **Post 3 needs more internal links**: Only 1 internal link found (min 3 required).
4. **Post 2 misses "SEO agency" entity**: Content covers SEO mistakes without mentioning agencies.
