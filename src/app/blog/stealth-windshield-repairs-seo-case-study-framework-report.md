# Content Framework Audit Report

**Post:** Stealth Windshield Repairs SEO: From 0 to 400+ Monthly Visitors in 6 Months
**Slug:** `stealth-windshield-repairs-seo-case-study`
**File:** `src/app/blog/data.js` (lines 25352–25419)
**Audit Date:** 2026-07-29

---

## Post: stealth-windshield-repairs-seo-case-study

| Check | Status | Details |
|-------|--------|---------|
| **TF-IDF: `windshield`** | ✅ PASS | 6 occurrences in post object (1 in title, 5 in content body). Threshold: ≥ 5. Related terms: `windscreen` (2), `auto glass` (4), `local SEO` (4). Strong keyword coverage for the core service topic. |
| **Entities** | ✅ PASS | All key entities present: **Location** — Edinburgh ✅, Glasgow ✅, Fife ✅; **Service type** — Auto Glass Repair ✅, Windshield Repair ✅ (2x), Windscreen Repair ✅ (2x), Chip Repair ✅; **SEO entities** — GBP/Local SEO ✅, Citations ✅ (30+), Reviews ✅ (38, 4.9★), Schema ✅, Page Speed ✅ (6.2→1.4s). No critical entity missing. |
| **Pillar Link** | ✅ PASS | Links to `/services/local-seo` (local SEO services pillar). Also links to `/blog/locksmith-dundee-seo-case-study` (related case study) and `/` (homepage). Good pillar-cluster alignment. |
| **AEO/GEO** | ❌ FAIL | **0 question headings found** (threshold: ≥ 2). No headings contain a question mark. The post uses declarative headings throughout (e.g., "The Challenge", "The Solution", "Key Takeaways", "Conclusion"). Adding question-based headings (e.g., "How Did Stealth Windshield Repairs Go From 0 to 400+ Visitors?" or "What Local SEO Strategies Worked for an Auto Glass Business?") would improve Answer Engine Optimization. |
| **Internal Links** | ✅ PASS | 3 internal links total: `/blog/locksmith-dundee-seo-case-study`, `/services/local-seo`, `/`. Threshold: ≥ 3. Meets minimum. |
| **Schema Ready** | ❌ FAIL | All standard fields present: slug ✅, title ✅, excerpt ✅, date ✅, author ✅, tags ✅, imagePlaceholder ✅. **Missing: `dateModified`** (only 5 of ~50+ posts include this field, but it's used for `Article.dateModified` schema markup and improves EEAT freshness signals). Also missing `image` field (falls back to default profile image). |

### Summary

| Check | Status |
|-------|--------|
| A. TF-IDF Coverage | ✅ PASS |
| B. Semantic Entity Coverage | ✅ PASS |
| C. Pillar-Cluster Alignment | ✅ PASS |
| D. AEO/GEO Optimization | ❌ FAIL |
| E. Internal Linking | ✅ PASS |
| F. Schema (Metadata) | ❌ FAIL |

### Fix Instructions

1. **AEO/GEO Optimization (Priority: High)**
   - Add at least **2 question-format headings**. Suggestions:
     - `### How Did Stealth Windshield Repairs Go From 0 to 400+ Monthly Visitors in 6 Months?`
     - `### What Local SEO Strategies Made the Biggest Impact for This Auto Glass Business?`
   - Consider adding a FAQ section with 3–5 Q&A pairs (e.g., "How long did it take to see results?", "What was the most effective tactic?", "Can other auto glass businesses replicate these results?"). This also enables FAQ schema markup.

2. **Schema Enhancement (Priority: Medium)**
   - Add `dateModified: "2026-06-18"` (matching `date` since post is newly published) to the post object. This explicitly populates `Article.dateModified` in JSON-LD schema, improving EEAT freshness signals.
   - Consider adding an `image` field with a post-specific image URL instead of relying on the default profile image.

3. **Content Enhancement Suggestions (Priority: Low)**
   - Add a dedicated GEO section explicitly explaining how the case study's approach aligns with Generative Engine Optimization (AI search readiness) — e.g., structured data, entity optimization, question answering.
