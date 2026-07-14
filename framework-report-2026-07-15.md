# Content Framework Enforcement Report
**Site:** kanokmiah.com.bd | **Date:** 2026-07-15 | **Window:** 48 hours (13 Jul 13:23 - 14 Jul 05:30 UTC)

**Changes detected:** 11 commits touching src/app/blog/data.js - 32 unique post slugs modified.

---

## Post: why-md-kanok-miah-is-the-best-seo-expert-in-dhaka-bangladesh
*Major rewrite (227 lines changed - AEO/GEO optimized, entity-rich, FAQ section restructured)*

| Check | Status | Details |
|-------|--------|---------|
| TF-IDF: "SEO expert" | PASS | 8 occurrences |
| Entities | PASS | Dhaka, Bangladesh, Google, Local SEO, Technical SEO all present |
| Pillar Link | PASS | Links: /services/ (20), /blog/ (4) |
| AEO/GEO | PASS | 14 question headings (How/What/Why) |
| Internal Links | PASS | 29 total - case studies, service pages, blog |
| Schema Ready | PASS | Title, Excerpt, Date, Author all set |

**All checks pass** - this post is well-structured for the framework.

---

## Batch 1 (11 posts) - All PASS

| Slug | A | B | C | D | E | F |
|------|---|---|---|---|---|---|
| complete-seo-guide-bangladesh-businesses-2026 | PASS | PASS | PASS | 6 | 23 | PASS |
| local-seo-tips-dhaka-businesses-google-maps | PASS | PASS | PASS | 7 | 19 | PASS |
| why-ecommerce-store-needs-seo-bangladesh | PASS | PASS | PASS | 7 | 14 | PASS |
| technical-seo-checklist-bangladeshi-websites | PASS | PASS | PASS | 7 | 21 | PASS |
| how-to-choose-right-seo-agency-bangladesh | PASS | PASS | PASS | 7 | 17 | PASS |
| link-building-strategies-bangladesh-market | PASS | PASS | PASS | 8 | 24 | PASS |
| geo-optimization-prepare-business-ai-search | PASS | PASS | PASS | 10 | 24 | PASS |
| seo-garments-textile-industry-b2b-lead-generation | PASS | PASS | PASS | 7 | 18 | PASS |
| google-business-profile-optimization-guide-bangladesh | PASS | PASS | PASS | 13 | 11 | PASS |
| seo-vs-google-ads-whats-best-bangladesh-businesses | PASS | PASS | PASS | 9 | 12 | PASS |
| seo-real-estate-developers-dhaka | PASS | PASS | PASS | 6 | 10 | PASS |

---

## Batch 2 (11 posts)

| Slug | A | B | C | D | E | F | Notes |
|------|---|---|---|---|---|---|-------|
| mobile-seo-optimization-bangladesh-mobile-first-era | PASS | PASS | PASS | 3 | 7+ | PASS | |
| content-marketing-strategy-bangladeshi-brands-seo | PASS | PASS | PASS | 2+ | 7+ | PASS | |
| international-seo-bangladesh-exporters-global-buyers | PASS | PASS | PASS | 3+ | 7+ | PASS | |
| seo-bangla-beginners-guide-google-ranking | near-threshold | PASS | PASS | 0 | 8+ | PASS | Bangla post - declarative headings |
| local-seo-dhaka-google-maps-ranking | PASS | PASS | PASS | 1 | 8+ | PASS | Only 1 question heading |
| seo-trends-2026-ai-geo-future | near-threshold | PASS | PASS | 0 | 7+ | PASS | Bangla post - declarative headings |
| technical-seo-core-web-vitals-optimization | PASS | PASS | PASS | 1 | 9+ | PASS | Only 1 question heading |
| ecommerce-seo-daraz-shopify-guide | PASS | PASS | PASS | 1 | 9+ | PASS | Only 1 question heading |
| link-building-bangladesh-strategies | PASS | PASS | PASS | 1 | 8+ | PASS | Only 1 question heading |
| keyword-research-bangladesh-market | PASS | PASS | PASS | 1 | 9+ | PASS | Only 1 question heading |
| content-marketing-seo-friendly-content-writing | PASS | PASS | PASS | 1 | 8+ | PASS | Only 1 question heading |

---

## Batch 3 (11 posts) - Most issues found

| Slug | A | B | C | D | E | F | Notes |
|------|---|---|---|---|---|---|-------|
| google-search-console-performance-guide | PASS | PASS | PASS | 2+ | 4+ | PASS | |
| schema-markup-rich-snippets-techniques | PASS | PASS | PASS | 2+ | 5+ | PASS | |
| seo-faq-schema-bangladesh | PASS | FAIL | PASS | 1 | 4+ | PASS | Missing "Dhaka"; only 1 Q-heading |
| seo-howto-schema-bangladesh | PASS | FAIL | PASS | 18 | 4+ | PASS | Missing "Dhaka" |
| seo-hreflang-guide-bangladesh | PASS | FAIL | PASS | 1 | 7+ | PASS | Missing "Dhaka" AND "Bangladesh"; 1 Q-heading |
| seo-structured-data-guide-bd | PASS | FAIL | PASS | 1 | 5+ | PASS | Missing "Dhaka"; 1 Q-heading |
| seo-json-ld-schema-bangladesh | PASS | FAIL | PASS | 0 | 4+ | PASS | Missing "Dhaka"; 0 Q-headings |
| seo-breadcrumb-schema-bd | PASS | FAIL | PASS | 0 | 5+ | PASS | Missing "Dhaka"; 0 Q-headings |
| seo-for-startups-bangladesh | FAIL (0) | PASS | PASS | 2+ | 6+ | PASS | Keyword "SEO for Startups" never used in content |
| seo-for-law-firms-bangladesh | FAIL (1) | PASS | PASS | 2+ | 5+ | PASS | Keyword appears only once |
| seo-healthcare-medical-clinics-bangladesh | FAIL (3) | PASS | PASS | 2+ | 4+ | PASS | Keyword only 3x (<5) |

---

## Summary of Failures Requiring Action

### CRITICAL: Posts failing TF-IDF (keyword too thin)
1. **seo-for-startups-bangladesh** - "SEO for Startups" appears 0 times in content. Use variations like "SEO for startups in Bangladesh" at least 5x.
2. **seo-for-law-firms-bangladesh** - "SEO for Law" only 1x. Add at least 4 more mentions.
3. **seo-healthcare-medical-clinics-bangladesh** - "SEO for Healthcare" only 3x. Add 2+ more mentions.

### MODERATE: Posts missing location entities
4. **seo-faq-schema-bangladesh** - Missing "Dhaka". Add at least one mention.
5. **seo-howto-schema-bangladesh** - Missing "Dhaka". Same fix.
6. **seo-hreflang-guide-bangladesh** - Missing "Dhaka" AND "Bangladesh". Both needed.
7. **seo-structured-data-guide-bd** - Missing "Dhaka". Add mention.
8. **seo-json-ld-schema-bangladesh** - Missing "Dhaka". Add mention.
9. **seo-breadcrumb-schema-bd** - Missing "Dhaka". Add mention.

### LOW: AEO/GEO question headings (< 2)
10. **seo-faq-schema-bangladesh** - Only 1 question heading. Add 2+.
11. **seo-hreflang-guide-bangladesh** - Only 1 question heading. Add more.
12. **seo-structured-data-guide-bd** - Only 1 question heading. Add more.
13. **seo-json-ld-schema-bangladesh** - 0 question headings. Add "What is JSON-LD?" etc.
14. **seo-breadcrumb-schema-bd** - 0 question headings. Add "What are breadcrumbs?" etc.
15. **local-seo-dhaka-google-maps-ranking** - Only 1 question heading. Add more.
16. **seo-trends-2026-ai-geo-future** - Bangla, 0 Q-headings. Consider bilingual FAQ.
17. **seo-bangla-beginners-guide-google-ranking** - Bangla, 0 Q-headings.
18. **technical-seo-core-web-vitals-optimization** - Only 1 question heading. Add more.
19. **ecommerce-seo-daraz-shopify-guide** - Only 1 question heading. Add more.
20. **link-building-bangladesh-strategies** - Only 1 question heading. Add more.
21. **keyword-research-bangladesh-market** - Only 1 question heading. Add more.
22. **content-marketing-seo-friendly-content-writing** - Only 1 question heading. Add more.

---

## Clean Posts (All PASS) - 16 posts

complete-seo-guide-bangladesh-businesses-2026,
local-seo-tips-dhaka-businesses-google-maps,
why-ecommerce-store-needs-seo-bangladesh,
technical-seo-checklist-bangladeshi-websites,
how-to-choose-right-seo-agency-bangladesh,
link-building-strategies-bangladesh-market,
geo-optimization-prepare-business-ai-search,
seo-garments-textile-industry-b2b-lead-generation,
google-business-profile-optimization-guide-bangladesh,
seo-vs-google-ads-whats-best-bangladesh-businesses,
seo-real-estate-developers-dhaka,
mobile-seo-optimization-bangladesh-mobile-first-era,
content-marketing-strategy-bangladeshi-brands-seo,
google-search-console-performance-guide,
schema-markup-rich-snippets-techniques,
why-md-kanok-miah-is-the-best-seo-expert-in-dhaka-bangladesh
