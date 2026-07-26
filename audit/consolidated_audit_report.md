# Content Cluster & E-E-A-T Audit — kanokmiah.com.bd
**Audit Date:** 2026-07-20 | **Site:** https://kanokmiah.com.bd | **Executor:** Hermes Agent (Cron Job)

---

## SECTION 1: EXECUTIVE SUMMARY

| Metric | Value |
|--------|-------|
| Total blog posts analyzed | 128 |
| Content pillars identified | 8 |
| Pillars with critical gaps (< 8 articles) | 2 (E-commerce SEO: 3, Link Building: 5) |
| Pillars needing expansion (< 12 articles) | 1 (Local SEO: 7) |
| Average E-E-A-T score | **7.5 / 10** |
| Posts with E-E-A-T score ≥ 8 | **61 posts (48%)** |
| Posts with E-E-A-T score < 6 | **1 post (#64 — has bug)** |
| Schema types implemented | **15/15** ✅ |
| Critical bugs found | **1** (Post #64 author field) |
| Improvement opportunities | **8** |

---

## SECTION 2: CONTENT CLUSTER MAP

### Pillar Distribution

| # | Pillar | Posts | Status | Recommended Size |
|---|--------|-------|--------|-----------------|
| 1 | **Local SEO & Google Maps** | 7 | 🔶 Needs expansion | 12+ |
| 2 | **Technical SEO & Core Web Vitals** | 29 | ✅ Strong | 15+ |
| 3 | **E-commerce SEO** | 3 | ❌ **Critical gap** | 12+ |
| 4 | **Content Marketing & SEO Strategy** | 40 | ✅ Excellent | 20+ |
| 5 | **GEO & AI Search** | 14 | ✅ Strong | 12+ |
| 6 | **Link Building & Off-Page SEO** | 5 | 🔶 Needs expansion | 10+ |
| 7 | **Industry-Specific SEO** | 19 | ✅ Good | 20+ |
| 8 | **Case Studies & Portfolio** | 11 | ✅ Good | 12+ |

### Critical Gaps

**E-commerce SEO (3 posts)** — For a $4B+ market, only 3 articles exist:
- `why-ecommerce-store-needs-seo-bangladesh` (EN)
- `ecommerce-seo-daraz-shopify-guide` (BN)
- `seo-for-facebook-marketplace` (BN)

**Link Building (5 posts)** — A core SEO service, only 5 articles:
- `link-building-strategies-bangladesh-market` (EN)
- `link-building-bangladesh-strategies` (BN)
- `seo-skyscraper-technique-bangladesh` (BN)
- `seo-domain-authority-bangladesh` (BN)
- `backlink-outreach-templates-strategies-bangladesh` (EN)

### Recommended New Cluster Topics

**1. Advanced E-commerce SEO for Bangladesh** — CRITICAL (6 posts)
- Daraz Seller Ranking Algorithm Deep-Dive
- Product Schema Implementation Guide
- E-commerce Category Page SEO
- Seasonal E-commerce SEO Calendar (Eid, Pohela Boishakh)
- Marketplace vs Independent Store SEO
- E-commerce Site Architecture & Crawl Budget

**2. Link Building & Digital PR Mastery** — HIGH (6 posts)
- Broken Link Building for BD Niches
- Digital PR for Bangladeshi Brands
- Competitor Backlink Gap Analysis
- Local Citation Authority Directory Strategy
- Link Reclamation: Unlinked Brand Mentions
- Guest Posting in Bangladesh

**3. Local SEO Deep-Dive & GBP Mastery** — MEDIUM (6 posts)
- GBP Products & Services Setup Guide
- Review Generation System for BD Businesses
- Hyperlocal SEO: Dhaka Neighborhoods
- 30-Day GBP Posts Content Calendar
- Service-Area Business Local SEO
- Seasonal Local SEO (Eid, Winter)

**4. SEO Analytics & ROI Measurement** — MEDIUM (5 posts)
- Building an SEO Dashboard (GSC + GA4 + Looker)
- SEO ROI Calculator for BD Businesses
- Advanced Google Search Console
- A/B Testing for SEO
- Monthly SEO Reporting Template

**5. EEAT & Brand Authority for BD** — LOW-MEDIUM (5 posts)
- Building EEAT for Bangladeshi Websites
- Getting into Google Knowledge Graph
- Author Authority Building
- YMYL SEO for Bangladesh
- Case Study-Based Authority Strategy

Full cluster map: `/root/kanok-miahit/audit/cluster_map.md` (476 lines, all 128 posts mapped)

---

## SECTION 3: E-E-A-T REVIEW

### Site-Level Schema Audit

| Schema Type | Status | Location |
|------------|--------|----------|
| OrganizationSchema | ✅ | layout.js (global) |
| LocalBusinessSchema | ✅ | layout.js (global) |
| WebSiteSchema | ✅ | layout.js (global) |
| PersonSchema | ✅ | layout.js (global) |
| ArticleSchema | ✅ | blog/[slug]/page.js |
| BreadcrumbSchema | ✅ | blog + blog/[slug] |
| FAQSchema | ✅ | blog + blog/[slug] |
| CollectionPageSchema | ✅ | blog/page.js |
| ServiceSchema | ✅ | Service pages |
| ContactPageSchema | ✅ | /contact |
| AboutPageSchema | ✅ | /about |
| AggregateRatingSchema | ✅ | 4.9/5, 108 reviews |
| ReviewSchema | ✅ | Schema.js |
| ProfessionalServiceSchema | ✅ | Schema.js |
| VideoObjectSchema | ✅ | Schema.js |

**All 15 schema types present and accounted for.** ✅

### Score Distribution

| Score | Count | Posts |
|-------|-------|-------|
| 9/10 | 9 | English guides with citations & credentials |
| 8/10 | 52 | English posts + Bangla posts with credentials |
| 7/10 | 66 | Bangla posts (no external citations) |
| 6/10 | 1 | Post #64 (author field bug) |
| **Average** | **7.5/10** | **Good — but room for improvement** |

### Critical Issues Found

**⚠️ BUG #1 — Author Field Markdown (Post #64)**
- **Post:** `seo-hubspot-vs-wordpress-bd`
- **Problem:** `author: "[মোঃ কনক মিঞা](/about)"` — contains markdown link syntax instead of plain text
- **Impact:** HIGH — Renders broken link syntax as author name
- **Fix:** Change to `author: "মোঃ কনক মিঞা"`
- **File:** `src/app/blog/data.js`

**⚠️ BUG #2 — Missing Author Bio on Blog Posts**
- **Problem:** No author photo, credentials badge, or bio section visible on any blog post page
- **Impact:** MEDIUM — Google's E-E-A-T guidelines recommend showing author expertise alongside content
- **Fix:** Add AuthorBio component below each post showing photo, credentials (Google Digital Garage, HubSpot, SEMrush), link to /about

**⚠️ BUG #3 — Inconsistent dateModified**
- **Problem:** Only some posts have `dateModified` field; others only have `date`
- **Impact:** LOW-MEDIUM — ArticleSchema handles fallback but update signals may be missed
- **Fix:** Add `dateModified` to all posts (set to last edit date)

Full E-E-A-T report: `/root/kanok-miahit/audit/eeat_report.md` (241 lines, all 128 posts scored)

---

## SECTION 4: IMPLEMENTATION TASKS CHECKLIST

### 🔴 Priority 1 — MUST FIX THIS WEEK

| # | Task | File | Effort | Impact |
|---|------|------|--------|--------|
| 1 | **Fix author field bug** in Post #64 — replace `"[মোঃ কনক মিঞা](/about)"` with `"মোঃ কনক মিঞা"` | `src/app/blog/data.js` | 2 min | HIGH — fixes broken author rendering |
| 2 | **Fix author field for Post #64 — same fix needed in data.js for the Bangla author to not have markdown** | `src/app/blog/data.js` (line ~5754 area) | 2 min | HIGH |
| 3 | **Add dateModified to all 128 posts** — audit which are missing and set to match `date` | `src/app/blog/data.js` | 30 min | MEDIUM — consistency fix |
| 4 | **Verify post #64 renders correctly** after fix (build or dev test) | `src/app/blog/data.js` | 5 min | HIGH — validation |

### 🟡 Priority 2 — FIX THIS MONTH

| # | Task | File | Effort | Impact |
|---|------|------|--------|--------|
| 5 | **Create AuthorBio component** — add photo, credentials badge (Google Digital Garage, HubSpot, SEMrush), bio, link to /about below each blog post | New: `src/components/AuthorBio.js` + modify `src/app/blog/[slug]/BlogPostClient.js` | 3-4 hours | HIGH — biggest E-E-A-T uplift |
| 6 | **Publish 3+ E-commerce SEO articles** — start with Daraz ranking deep-dive, Product Schema guide, Category Page SEO | New blog posts | 2-3 days | HIGH — fills critical cluster gap |
| 7 | **Publish 3+ Link Building articles** — start with Broken Link Building, Digital PR, Backlink Gap Analysis | New blog posts | 2-3 days | HIGH — fills critical cluster gap |
| 8 | **Add 3+ Local SEO articles** — GBP Products setup, Review Generation, Hyperlocal Dhaka neighborhoods | New blog posts | 2-3 days | MEDIUM — strengthens core pillar |
| 9 | **Add 2+ Bangladesh-specific case studies** — healthcare, restaurant, or education SEO results | New blog posts | 1-2 days | MEDIUM — more local proof |

### 🟢 Priority 3 — NICE TO HAVE

| # | Task | File | Effort | Impact |
|---|------|------|--------|--------|
| 10 | **Rebalance content strategy** — Content Marketing pillar (40 posts) is overbuilt vs. E-commerce (3) and Link Building (5). Shift publishing focus | Content calendar | Ongoing | HIGH — strategic alignment |
| 11 | **Add external citations to Bangla posts** — link to Google Search Central, DataReportal, or official docs where relevant | `src/app/blog/data.js` (post content) | 4-5 hours | MEDIUM — improves score from 7→8 |
| 12 | **Implement separate Author schema** with sameAs social profiles on blog posts | `src/app/blog/[slug]/page.js` | 1 hour | LOW — nice to have |
| 13 | **Add "Last Updated" dates** visible on blog post pages (not just in schema) | `src/app/blog/[slug]/BlogPostClient.js` | 1 hour | LOW — transparency signal |
| 14 | **Publish the remaining 4 recommended cluster topics** (Analytics, Industry, EEAT series) | New blog posts | 5-7 days | MEDIUM — long-term authority |
| 15 | **Add internal links** between related pillar and cluster posts for stronger topical authority | Across multiple posts | 2-3 hours | MEDIUM — strengthens SEO signals |

---

## SECTION 5: SUMMARY

**What's strong:**
- 128 posts is excellent content volume for a personal brand site
- 15 schema types implemented — comprehensive structured data foundation
- Bilingual content strategy (EN + BN) reaches broader audience
- Case studies include real metrics (traffic increases, rankings)
- All posts are fresh (2026) with proper ArticleSchema
- 11 real-world case studies with measurable results

**What needs immediate attention:**
1. **Author field bug** in Post #64 — quick fix, high impact
2. **Missing author bio** on all blog posts — biggest single E-E-A-T improvement available
3. **E-commerce SEO cluster** — severely underbuilt (3 posts) for a $4B+ market
4. **Link Building cluster** — underbuilt (5 posts) for a core service offering
5. **Inconsistent dateModified** — low effort to fix site-wide

**Recommendation:** Fix Priority 1 items this week (30 min total), then allocate 1-2 weeks for Priority 2 items (author bio component + 6-9 new articles in critical clusters). This will move the average E-E-A-T score from 7.5 → 8.5+ and significantly strengthen topical authority for the two most commercially valuable pillars.

---

*Full reports:*  
- `/root/kanok-miahit/audit/cluster_map.md` (476 lines)  
- `/root/kanok-miahit/audit/eeat_report.md` (241 lines)  
- `/root/kanok-miahit/audit/generate_eeat.py` (scoring script)
