# Content Framework Enforcement Report
**Date:** 2026-07-29 | **Project:** kanokmiah.com.bd  
**Commit:** 089949f — auto-fix: blog heading/HTML tags cleanup [cron]

---

## Changes Detected

Git log shows **4 posts modified** in the last 48 hours under `src/app/blog/data.js`:

| Post Slug | Change Type |
|-----------|------------|
| `link-building-strategies-bangladesh-market` | Heading formatting (bold → ###) |
| `seo-garments-textile-industry-b2b-lead-generation` | Heading formatting (bold → ###) |
| `google-business-profile-optimization-guide-bangladesh` | Heading formatting (bold → ###) |
| `mobile-seo-optimization-bangladesh-mobile-first-era` | **New metadata added** (metaTitle, metaDescription, dateModified) |

The first 3 posts had purely cosmetic heading fixes from a cron job. The Mobile SEO post received substantive content improvements.

---

## Post: `mobile-seo-optimization-bangladesh-mobile-first-era`
**Title:** Mobile SEO for Bangladesh: Optimize for the Mobile-First Era

| Check | Status | Details |
|-------|--------|---------|
| **TF-IDF: "Mobile SEO"** | ✅ | 25 occurrences — strong keyword coverage |
| **Entities** | ✅ | Dhaka (15), Bangladesh (54), Chittagong (3), Sylhet (2), e-commerce (7), Core Web Vitals (8), voice search (14) — all key entities present |
| **Pillar Link** | ⚠️ | No dedicated `/services/mobile-seo` pillar page exists. Post links to related services (`/on-page-seo`, `/technical-seo`, `/local-seo`) but lacks a central Mobile SEO pillar to anchor the cluster. |
| **AEO/GEO** | ✅ | 9 question-based headings — excellent for voice/AI search |
| **Internal Links** | ✅ | 20 internal links: 8 blog, 5 services, 3 locations, 3 industries, 1 about |
| **Schema Ready** | ✅ | title, excerpt, date, author, metaTitle, metaDescription, dateModified all set |

### Additional Issues Found

**🔴 Unicode Punctuation Inconsistency (Conclusion Section)**
Lines 2463–2467 in the post conclusion contain Bengali text: `আরও জানতে দেখুন` followed by punctuation. Two lines correctly use Bengali Danda (`।` U+0964), but the third uses CJK Full Stop (`。` U+3002):

```
✅ [on-page SEO services](/services/on-page-seo) — আরও জানতে দেখুন।
✅ [mobile SEO ranking strategies](/blog/mobile-seo-bangladesh-ranking-strategy) — আরও জানতে দেখুন।
❌ [technical SEO checklist](/blog/technical-seo-checklist-bangladeshi-websites) — আরও জানতে দেখুন。
```

**Fix:** Replace `。` (U+3002) with `।` (U+0964) on line 2467.

---

## Post: `link-building-strategies-bangladesh-market`
**Change:** 2 heading fixes (cosmetic only — no content changed)

| Check | Status | Details |
|-------|--------|---------|
| **TF-IDF: "Link Building"** | ✅ | 40 occurrences |
| **Entities** | ✅ | All key entities present |
| **Pillar Link** | ✅ | Links to `/services/link-building` (dedicated service page) |
| **AEO/GEO** | ✅ | 10 question headings |
| **Internal Links** | ✅ | 22 internal links |
| **Schema Ready** | ✅ | All fields present |

No additional issues. Framework compliant.

---

## Post: `seo-garments-textile-industry-b2b-lead-generation`
**Change:** 1 heading fix (cosmetic only — no content changed)

| Check | Status | Details |
|-------|--------|---------|
| **TF-IDF: "Garments & Textile SEO"** | ✅ | 46 "garment" root occurrences, 6 "textile industry", 6 "RMG" — strong topical depth |
| **Entities** | ✅ | Dhaka, Bangladesh, Chittagong, factory, B2B, RMG all present |
| **Pillar Link** | ✅ | Links to `/industries/garments-textile` and `/services/link-building` |
| **AEO/GEO** | ✅ | 9 question headings |
| **Internal Links** | ✅ | 19 internal links |
| **Schema Ready** | ✅ | All fields present |

No additional issues. Framework compliant.

---

## Post: `google-business-profile-optimization-guide-bangladesh`
**Change:** 2 heading fixes (cosmetic only — no content changed)

| Check | Status | Details |
|-------|--------|---------|
| **TF-IDF: "Google Business Profile"** | ✅ | 9 occurrences |
| **Entities** | ✅ | Dhaka, Bangladesh, verification, Google Maps, review all present |
| **Pillar Link** | ✅ | Links to `/services/local-seo` (dedicated service page) |
| **AEO/GEO** | ✅ | 13 question headings |
| **Internal Links** | ✅ | 14 internal links |
| **Schema Ready** | ✅ | All fields present |

No additional issues. Framework compliant.

---

## Summary

| Metric | ✅ Pass | ⚠️ Flagged | ❌ Fail |
|--------|--------|------------|--------|
| TF-IDF Coverage | 4/4 | 0 | 0 |
| Entity Coverage | 4/4 | 0 | 0 |
| Pillar Link | 3/4 | 1 (Mobile SEO — no pillar page exists) | 0 |
| AEO/GEO | 4/4 | 0 | 0 |
| Internal Links | 4/4 | 0 | 0 |
| Schema Ready | 4/4 | 0 | 0 |

### Action Items

1. **🔴 [High] Fix Unicode punctuation** in `mobile-seo-optimization-bangladesh-mobile-first-era` — replace CJK full stop `。` (U+3002) with Bengali Danda `।` (U+0964) on the third Bengali link in the Conclusion section. This affects content quality signals and may influence Bengali-language user trust.

2. **🟡 [Medium] Create Mobile SEO pillar page** — The `mobile-seo` post belongs to the "Mobile SEO" topic cluster but no dedicated pillar page (`/services/mobile-seo` or `/mobile-seo`) exists. Creating one and linking this post to it would strengthen pillar-cluster structure and topical authority signals.

3. **✅ Good** — The new metaTitle, metaDescription, and dateModified fields on the Mobile SEO post are properly set and improve Schema/rich result readiness.
