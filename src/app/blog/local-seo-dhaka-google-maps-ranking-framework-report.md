# Content Framework Check Report

**Post Slug:** `local-seo-dhaka-google-maps-ranking`
**File:** `/root/kanok-miahit/src/app/blog/data.js` (lines 3078–3322)
**Language:** Bengali (with some English terms)
**Review Date:** 2026-07-23

---

## Post Metadata

| Field | Value |
|-------|-------|
| **Title** | `স্থানীয় SEO: ঢাকায় আপনার ব্যবসা কীভাবে গুগল ম্যাপে শীর্ষে দেখাবেন` |
| **Slug** | `local-seo-dhaka-google-maps-ranking` |
| **Date** | `2026-07-08` |
| **Author** | `মোঃ কনক মিঞা` |
| **Excerpt** | `ঢাকায় আপনার ব্যবসাকে গুগল ম্যাপে শীর্ষে আনার জন্য সম্পূর্ণ স্থানীয় SEO গাইড। গুগল বিজনেস প্রোফাইল অপটিমাইজেশন, বাংলাদেশি ডিরেক্টরিতে সাইটেশন, গ্রাহক রিভিউ ব্যবস্থাপনা এবং লোকাল কীওয়ার্ড টার্গেটিং নিয়ে বিস্তারিত ব্যবহারিক কৌশল।` |
| **Tags** | `["Local SEO", "Dhaka", "Google Maps", "GBP Optimization", "Bangladesh Business"]` |
| **Content Length** | ~236 lines (template literal from line 3086 to 3321) |

---

## A. TF-IDF Coverage (Primary Keyword Density)

| Check | Detail |
|-------|--------|
| **Primary keyword extraction** | First meaningful noun phrase from title: **`স্থানীয় SEO`** (Local SEO) |
| **Count in content (exact match)** | `স্থানীয় SEO`: **14 occurrences** |
| **Count in content (variants)** | `লোকাল SEO`: **3**, `Local SEO`: **1** → **18 total** |
| **Threshold** | ≥ 5 |
| **Result** | ✅ **PASS** — 14 exact + 4 variants = 18 total occurrences (well above threshold) |

---

## B. Semantic Entity Coverage

| Entity | Check | Occurrences | Status |
|--------|-------|-------------|--------|
| **Location: Dhaka** | `ঢাকা` / `Dhaka` in content | **24** | ✅ Present |
| **Location: Bangladesh** | `বাংলাদেশ` / `Bangladesh` in content | **17** | ✅ Present |
| **Service type: Google Maps** | `গুগল ম্যাপ` / `Google Maps` / `Google Map` in content | **12** | ✅ Present |
| **Service type: GBP** | `গুগল বিজনেস প্রোফাইল` / `GBP` / `Google Business Profile` in content | **13** | ✅ Present |
| **Industry/Business verticals** | Examples: restaurant, dentist, salon, IT service, real estate, e-commerce, garments, hotel, NGO, law firm | **Multiple** | ✅ Present |

| **Overall Result** | ✅ **PASS** — All required key entities (Dhaka, Bangladesh, Google Maps, GBP, business verticals) are well-represented |

---

## C. Pillar-Cluster Alignment

| Check | Detail |
|-------|--------|
| **Tags analyzed** | `Local SEO`, `Dhaka`, `Google Maps`, `GBP Optimization`, `Bangladesh Business` |
| **Pillar topic identified** | **Local SEO** → mapped to `/services/local-seo` (the Local SEO service page, confirmed at `/root/kanok-miahit/src/app/services/data.js` slug: `local-seo`) |
| **Link to pillar page** | ✅ **Yes** — Line 3318: `[লোকাল SEO](/services/local-seo) — গুগল ম্যাপ ও স্থানীয় সার্চ` |
| **Other cluster cross-links** | `/services/technical-seo`, `/services/ecommerce-seo`, `/services/semantic-seo`, and 7 `/blog/...` posts in the Local SEO cluster |
| **Result** | ✅ **PASS** — Post explicitly links to the Local SEO pillar page (`/services/local-seo`) |

---

## D. AEO/GEO Optimization (Question-Based Headings)

| # | Heading | Line | Question Word | Type |
|---|---------|------|---------------|------|
| 1 | `### কীভাবে বেশি রিভিউ পাবেন` | 3123 | কীভাবে (How) | Bengali |
| 2 | `### কীভাবে AEO আপনার স্থানীয় SEO কে সাহায্য করবে?` | 3265 | কীভাবে (How) | Bengali |
| 3 | `## কেন বিশ্বাস করবেন মোঃ কনক মিঞাকে?` | 3303 | কেন (Why) | Bengali |

**Total question-based headings: 3**
**Threshold: ≥ 2**

| Result | ✅ **PASS** — 3 question-based headings found (above minimum of 2) |

Note: Several other headings contain question words but don't start with them (e.g., `## স্থানীয় SEO কী?`, `### গুগল ম্যাপে র‍্যাংকিংয়ের জন্য সবচেয়ে গুরুত্বপূর্ণ ফ্যাক্টর কী?`, `## বাংলাদেশ-এ GEO কেন গুরুত্বপূর্ণ?`) — these are not counted per the strict "starts with" rule but add to the AEO/GEO value.

---

## E. Internal Linking

### `/blog/` links (to other blog posts) — 7 found
1. `seo-bangla-beginners-guide-google-ranking` (line 3177)
2. `mobile-seo-optimization-bangladesh-mobile-first-era` (line 3183)
3. `technical-seo-checklist-bangladeshi-websites` (line 3184)
4. `seo-local-citations-bangladesh` (line 3229)
5. `google-business-profile-optimization-guide-bangladesh` (line 3231)
6. `complete-seo-guide-bangladesh-businesses-2026` (line 3235)
7. `seo-consultant-dhaka-bangladesh` (line 3237)

### `/services/` links — 4 found
1. `/services/technical-seo` (line 3317)
2. `/services/local-seo` (line 3318, pillar page)
3. `/services/ecommerce-seo` (line 3319)
4. `/services/semantic-seo` (line 3320)

### `/locations/` links — 3 found
1. `/locations/dhaka` (line 3289)
2. `/locations/chittagong` (line 3289)
3. `/locations/sylhet` (line 3289)

**Total internal links: 7 + 4 + 3 = 14**
**Threshold: ≥ 3**

| Result | ✅ **PASS** — 14 internal links (well above threshold of 3) |

---

## F. Schema (ArticleSchema Readiness)

| Field | Value | Status |
|-------|-------|--------|
| **title** | `স্থানীয় SEO: ঢাকায় আপনার ব্যবসা কীভাবে গুগল ম্যাপে শীর্ষে দেখাবেন` | ✅ Set |
| **slug** | `local-seo-dhaka-google-maps-ranking` | ✅ Set |
| **date** | `2026-07-08` | ✅ Set |
| **author** | `মোঃ কনক মিঞা` | ✅ Set |
| **excerpt** | `ঢাকায় আপনার ব্যবসাকে গুগল ম্যাপে শীর্ষে আনার জন্য...` | ✅ Set |
| **imagePlaceholder** | `📍` | ✅ Set |

| Result | ✅ **PASS** — All required ArticleSchema fields (title, slug, date, author, excerpt) are present and populated |

---

## Summary

| Check | Result | Score |
|-------|--------|-------|
| **A. TF-IDF Coverage** | ✅ **PASS** | 14 exact + 4 variant occurrences (threshold: 5) |
| **B. Semantic Entity Coverage** | ✅ **PASS** | Dhaka (24), Bangladesh (17), Google Maps (12), GBP (13) |
| **C. Pillar-Cluster Alignment** | ✅ **PASS** | Links to `/services/local-seo` pillar page |
| **D. AEO/GEO Optimization** | ✅ **PASS** | 3 question-based headings (threshold: 2) |
| **E. Internal Linking** | ✅ **PASS** | 14 internal links (threshold: 3) |
| **F. Schema** | ✅ **PASS** | All ArticleSchema fields present |
| **OVERALL** | ✅ **ALL CHECKS PASSED** | — |

### Notes & Recommendations
- The post is comprehensive and well-optimized for Local SEO in the Dhaka/Bangladesh context.
- It covers GBP optimization, local citations, review management, hyperlocal keyword targeting, GEO/AEO, and E-E-A-T.
- Strong internal linking structure with 7 blog cross-references, 4 service page links (including the pillar), and 3 location page links.
- 3 question-based headings help with AEO/GEO — could optionally add 1–2 more starting with `কখন` (When) or `কোথায়` (Where) for broader coverage.
- The excerpt, title, and all metadata are fully populated for ArticleSchema.
