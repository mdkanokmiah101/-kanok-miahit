# Content Framework Enforcement Report
**Site:** kanokmiah.com.bd | **Period:** Last 48 hours | **Date:** 2026-07-14

## Changes Detected
✅ 12 commits found modifying `src/app/blog/data.js` in the last 48 hours.

### Commits Summary
| Commit | Description | Scope |
|--------|------------|-------|
| `5f866ad` | auto-fix: blog heading/HTML tags cleanup [cron] | 1-line fix |
| `220d410` | fix: update title | "best SEO expert" post |
| `d8dd19d` | fix: shorten H1, fix milestones/case study links | "best SEO expert" post |
| `e06ed4b` | Replace intro: personal → market-data-driven | "best SEO expert" post |
| `f93ce87` | Story-style intro + workload metrics | "best SEO expert" post |
| `f9a8d35` | Full rewrite: AEO/GEO, entity-rich, FAQ | "best SEO expert" post |
| `0471a64` | Remove FAQ comment artifacts | "best SEO expert" post |
| `817fc84` | Remove 11 FAQ schema script blocks (visible text) | "best SEO expert" post |
| `9e54bda` | Remove FAQ comment artifact | "best SEO expert" post |
| `3578353` | Remove raw FAQ JSON from content | "best SEO expert" post |
| `33f46ec` | Fix 43 broken internal links + real-estate table | Many posts |
| `9a56389` | Align bio: "since 2019, 210+ projects" | Many posts |

**Substantively modified posts identified:**

1. `why-md-kanok-miah-is-the-best-seo-expert-in-dhaka-bangladesh`
2. `seo-real-estate-developers-dhaka`
3. `seo-real-estate-agents-property-developers-bangladesh`
4. ~12 other posts had mechanical link fixes + bio alignment (no content change)

---

## Post: `why-md-kanok-miah-is-the-best-seo-expert-in-dhaka-bangladesh`

| Check | Status | Details |
|-------|--------|---------|
| **TF-IDF: "SEO expert"** | ✅ | 8 occurrences (≥5 ✓) |
| **TF-IDF: "Dhaka"** | ✅ | 28 occurrences |
| **Entities — Dhaka** | ✅ | 28 occurrences |
| **Entities — Bangladesh** | ✅ | 27 occurrences |
| **Entities — Google** | ✅ | 47 occurrences |
| **Entities — SEO** | ✅ | 111 occurrences |
| **Entities — Khan IT** | ✅ | 6 occurrences |
| **Entities — CloudMatrix** | ✅ | 6 occurrences |
| **Entities — 210+ Projects** | ✅ | 12 occurrences |
| **Pillar Link** | ✅ | 26 pillar links (services, blog, contact) |
| **AEO/GEO** | ✅ | 15 question-based headings (threshold: 2) |
| **Internal Links** | ✅ | 29 total (4 blog + 20 services + 5 other) |
| **Schema Ready** | ✅ | Title: 61 chars, Excerpt: 227 chars, Date: 2026-07-09 |

**Verdict: ✅ ALL CHECKS PASSED**

Notable strengths:
- Heavy AEO/GEO optimization — 15 question headings (H2 + H3) including "How Did I Start...", "What Certifications...", "How Long Does It Take...", "What Is the Cost...", etc.
- Excellent internal linking: 4 case study links, all 7 service pages linked, contact CTA
- Strong entity coverage with location, employer, certification, and metric entities
- FAQ section with 6 detailed Q&A pairs

---

## Post: `seo-real-estate-developers-dhaka`

| Check | Status | Details |
|-------|--------|---------|
| **TF-IDF: "Real Estate SEO"** | ✅ | 5 occurrences |
| **TF-IDF: "real estate"** | ✅ | 45 occurrences |
| **TF-IDF: "Dhaka"** | ✅ | 38 occurrences |
| **Entities — Dhaka** | ✅ | 37 occurrences |
| **Entities — Bangladesh** | ✅ | 12 occurrences |
| **Entities — Google** | ✅ | 17 occurrences |
| **Entities — Real Estate/Property/Developer** | ✅ | 45/34/35 occurrences |
| **Pillar Link** | ✅ | 10 pillar links (services, blog, industries) |
| **AEO/GEO** | ✅ | 6 question headings (threshold: 2) |
| **Internal Links** | ✅ | 10 total (services + blog + industries) |
| **Schema Ready** | ✅ | Title: 69 chars, Excerpt: 183 chars, Date: 2026-06-27 |

**Verdict: ✅ ALL CHECKS PASSED**

Notes:
- Table separator fix was applied (raw `|--|` was visible as text — fixed to markdown-friendly format)
- Good diversity of internal links to service pages and related blog posts
- Question headings include "How long does real estate SEO take...", "What is the monthly cost...", etc.

---

## Post: `seo-real-estate-agents-property-developers-bangladesh`

| Check | Status | Details |
|-------|--------|---------|
| **TF-IDF: "Real Estate SEO"** | ✅ | 6 occurrences |
| **TF-IDF: "real estate"** | ✅ | 37 occurrences |
| **TF-IDF: "property"** | ✅ | 45 occurrences |
| **Entities — Dhaka** | ✅ | 24 occurrences |
| **Entities — Bangladesh** | ✅ | 20 occurrences |
| **Entities — Google** | ✅ | 15 occurrences |
| **Entities — Real Estate/Property/Developer/Agent** | ✅ | 37/50/18/11 occurrences |
| **Pillar Link** | ✅ | 4 pillar links (services, industries) |
| **AEO/GEO** | ✅ | 6 question-marked headings (1 English + 5 Bengali) |
| **Internal Links** | ✅ | 4 internal links (services + industries) |
| **Schema Ready** | ✅ | Title: 83 chars, Excerpt: 233 chars, Date: 2026-07-08 |

**Verdict: ✅ ALL CHECKS PASSED**

Notes:
- Bengali question headings properly serve the bilingual audience (e.g., "রিয়েল এস্টেট SEO কী?")
- Bio alignment commit updated "over a decade" → "7+ years" to match verified credentials

---

## Additional Posts (Link Fixes Only)

The commit `33f46ec` fixed **43 broken internal links** (missing `/blog/` prefix) across approximately 20+ posts. These were mechanical fixes — no content was changed beyond URL paths. Examples of affected posts include:

- Bengali schema guides (JSON-LD, FAQ, HowTo, Breadcrumb)
- Case studies (Landlord Certificates, SEO pricing guide)
- Industry pages references
- Wedding & event planners guide
- Enterprise SEO guides

**Status: ✅ All broken links resolved — no content issues.**

---

## Overall Summary

| Post | TF-IDF | Entities | Pillar | AEO/GEO | Links | Schema | **Result** |
|------|--------|----------|--------|---------|-------|--------|:----------:|
| best-seo-expert-dhaka | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | **✅ PASS** |
| real-estate-developers-dhaka | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | **✅ PASS** |
| real-estate-agents-bangladesh | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | **✅ PASS** |
| ~20 other posts (link fixes) | N/A | N/A | N/A | N/A | ✅ fixed | N/A | **✅ PASS** |

**FINAL VERDICT: ✅ All content framework checks pass. No fixes required.**
