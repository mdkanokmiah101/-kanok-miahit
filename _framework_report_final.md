# Content Framework Enforcement Report — kanokmiah.com.bd

**Generated:** 2026-07-24 14:18 BST  
**Changes detected:** 49 modified posts in `src/app/blog/data.js`  
**Change type:** Auto-formatting (blank lines, markdown fixes) + new intro headings on 7 posts  

---

## Changes Overview

The 3 cron commits in the last 48h were "auto-fix: blog heading/HTML tags cleanup" — primarily:
- Added blank lines before `##` headings for readability
- Fixed bold markdown syntax (`**text**, **text**` → `text, **text**`)
- Added **7 new intro headings**: `## What is [Topic]?` on affiliate-seo-bangladesh, b2b-lead-generation-seo-bangladesh, seo-for-fitness-gyms-bangladesh, seo-healthcare-medical-clinics-bangladesh, seo-educational-institutions-bangladesh, seo-travel-tourism-bangladesh, recovering-google-penalties-bangladesh-guide
- Added pillar links on ~20 posts that were missing them
- Added related-resource sections on several posts

---

## Overall Result: ⚠️ 48/49 posts need attention (framework gaps)

| Check | ✅ Pass | ❌ Fail | Status |
|-------|--------|--------|--------|
| Schema Ready | 49 | 0 | ✅ |
| TF-IDF Keyword Coverage | 29 | 20 | ❌ |
| Internal Linking (≥3) | 40 | 9 | ❌ |
| Pillar Link | 19 | 30 | ❌ |
| Entity Coverage | 3 | 46 | ❌ |
| AEO/GEO Question Headings (≥2) | 13 | 36 | ❌ |

---

## ⚠️ NOTE: Some failures are expected

- **Entity Coverage**: The check flags absence of "search engine optimization" even when "SEO" is used. This is a soft concern — Google understands both. The more important missing entities are location names and industry-specific terms.
- **TF-IDF**: Some keyword extraction is imprecise (e.g. "mobile optimize" not found as a bigram in mobile-seo content). Manual review recommended before acting on these.
- **AEO/GEO (Bengali posts)**: 36 posts flagged, but many are Bengali-language where question patterns use Bengali words (কী, কিভাবে, কেন) — the English-word regex misses these. True count of posts lacking questions is lower.

---

## Posts with Actual Content Issues (worth fixing)

### 🔴 HIGH PRIORITY — Missing Pillar Link (30 posts)
These posts do NOT link back to `/blog/complete-seo-guide-bangladesh-businesses-2026`:

```
google-search-console-performance-guide      seo-event-management-companies-bangladesh
google-tag-manager-seo-bd                     seo-faq-schema-bangladesh
how-to-track-measure-seo-roi-bangladesh       seo-howto-schema-bangladesh
mobile-seo-bangladesh-ranking-strategy        seo-hreflang-guide-bangladesh
recovering-google-penalties-bangladesh-guide  seo-json-ld-schema-bangladesh
seo-canonical-url-guide-bd                    seo-landing-page-optimization-bd
seo-educational-institutions-bangladesh       seo-real-estate-agents-property-developers-bangladesh
seo-for-law-firms-bangladesh                  seo-referral-traffic-bangladesh
seo-for-podcast-bangladesh                    seo-robots-txt-guide-bangladesh
seo-for-startups-bangladesh                   seo-services-cost-bangladesh-pricing-guide
seo-google-analytics-4-bangladesh             seo-structured-data-guide-bd
seo-healthcare-medical-clinics-bangladesh     seo-travel-tourism-bangladesh
seo-vs-google-ads-bangladesh-business         seo-website-migration-guide-bd
seo-vs-ppc-advertising-bangladesh             seo-xml-sitemap-guide-bd
voice-search-seo-bengali-bangladesh           youtube-seo-bangladesh-ranking-tips
```
**Fix:** Add a contextual link to the pillar page in the conclusion or "Related Resources" section.

### 🟡 MEDIUM — Low Internal Links (9 posts)
These posts have fewer than 3 internal links:

| Post | Links | Issue |
|------|-------|-------|
| seo-faq-schema-bangladesh | 0 | Purely technical FAQ — no blog/service/location links |
| seo-howto-schema-bangladesh | 0 | Same |
| seo-hreflang-guide-bangladesh | 0 | Same |
| seo-json-ld-schema-bangladesh | 0 | Same |
| seo-robots-txt-guide-bangladesh | 0 | Same |
| seo-structured-data-guide-bd | 0 | Same |
| seo-xml-sitemap-guide-bd | 0 | Same |
| seo-canonical-url-guide-bd | 1 | Only 1 link |
| google-tag-manager-seo-bd | 2 | Only 2 links |

**Fix:** Add links to related services (/services/technical-seo) and location pages (/locations/dhaka) in these technical schema/SEO posts.

### 🟢 LOW — Schema Ready ✅ (All 49 posts have title, excerpt, date)
All posts have the fields needed for ArticleSchema — no action needed.

---

## Posts That Passed All Checks ✅

Only **1 post** passed every framework check:

| Post | Title |
|------|-------|
| affiliate-seo-bangladesh | অ্যাফিলিয়েট মার্কেটিং SEO: বাংলাদেশি মার্কেটে সফল হওয়ার কৌশল |

---

## Action Items Summary

1. **Add pillar link** to 30 posts (see 🔴 list above) — add `/blog/complete-seo-guide-bangladesh-businesses-2026` in a concluding or "Related" section
2. **Add internal links** to 9 technical schema posts — reference /services/technical-seo and location pages
3. **Add Bengali question headings** to Bengali posts that lack them — use কী, কেন, কিভাবে, কখন, কোথায় patterns
4. **Review entity coverage** — specifically ensure all industry posts mention Dhaka, Chittagong, Sylhet, and their primary service domain at least once

**Next check:** Framework re-audit in 48 hours after fixes are applied.
