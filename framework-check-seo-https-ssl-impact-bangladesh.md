# Content Framework Check Report
## Post: seo-https-ssl-impact-bangladesh
**Title:** HTTPS ও SSL: SEO-র উপর প্রভাব ও সেটআপ গাইড
**Slug:** seo-https-ssl-impact-bangladesh
**Language:** Bengali (BN)
**Author:** মোঃ কনক মিঞা
**Date:** 2026-07-08
**Tags:** HTTPS, SSL, ওয়েবসাইট সিকিউরিটি, SEO, বাংলাদেশ
**Content Length:** 14,030 chars
**Commit:** f4d9445 — "silo: added sibling links + contact CTA" (3 insertions, 3 deletions)
**Modifications Made:**
1. Line 16315: Added sibling link → `/blog/seo-redirects-guide-bangladesh` (anchor: "রিডাইরেক্ট বেস্ট প্র্যাকটিস গাইড")
2. Line 16319: Added sibling link → `/blog/seo-canonical-url-guide-bd` (anchor: "ক্যানোনিকাল ইউআরএল গাইড")
3. Line 16456: Added contact CTA → `/contact` (anchor: "যোগাযোগ")

---

| # | Category | Status | Detail |
|---|----------|--------|--------|
| **A** | **TF-IDF** | ⚠️ **BORDERLINE FAIL** | Primary keyword extracted: `"উপর"` — 3 occurrences (need ≥5). **This is a false negative:** The keyword extraction algorithm selected the Bengali preposition "উপর" (meaning "on/upon") as the primary keyword instead of the actual topic keywords. Real primary keywords: **HTTPS** ×62, **SSL** ×52, **SEO** ×32, **সেটআপ** ×8, **প্রভাব** ×5 — all well above threshold. The algorithm lacks Bengali stopword filtering. Framework-reported: ❌ FAIL |
| **B** | **Entities** | ✅ **PASS** | All 3 required entities present: `location_dhaka` (ঢাকা), `location_bangladesh` (বাংলাদেশ), `service_seo` (SEO/এসইও). No tag-triggered entities needed. All found in content. |
| **C** | **Pillar-Cluster** | ✅ **PASS** | **Direct pillar link found:** `/blog/schema-markup-rich-snippets-techniques` (schema pillar). Also links to `/services/technical-seo`. Sibling links added in commit link to other cluster posts: `/blog/seo-redirects-guide-bangladesh` (redirects), `/blog/seo-canonical-url-guide-bd` (canonical URLs), `/blog/google-search-console-performance-guide` (GSC), `/blog/seo-website-migration-guide-bd` (migration). The pillar link to schema-markup-rich-snippets is thematically appropriate — SSL/HTTPS is a technical SEO topic closely related to schema/structured data. |
| **D** | **AEO/GEO** | ✅ **PASS** | **20 total AEO elements** (12 question-based headings + 8 FAQ elements). Dedicated **GEO section** (line 16349-16357), **EEAT section** (line 16359-16368), **AEO section** (line 16370-16379), and **FAQ section** (line 16431-16440). All well above the ≥2 threshold. |
| **E** | **Internal Links** | ✅ **PASS** | **16 unique internal links** (need ≥3): 5 blog links, 1 service link, 8 location links, 2 other (contact/about). Blog links form a strong technical SEO cluster. Location links cover all 8 major Bangladeshi cities. Contact CTA added in commit. |
| **F** | **Schema** | ✅ **PASS** | All fields present: title ✓, excerpt ✓, date ✓, author ✓, content (14,030 chars) ✓. Schema.org/structured data explicitly mentioned in content. |

---

## Detailed Breakdown

### A: TF-IDF Keyword Coverage
```
Extracted keyword:    "উপর"    3 occurrences  ⚠️
HTTPS                        62 occurrences  ✅
SSL                          52 occurrences  ✅
SEO                          32 occurrences  ✅
সেটআপ (setup)                8 occurrences   ✅
প্রভাব (impact)               5 occurrences   ✅
মাইগ্রেশন (migration)        6 occurrences   ✅
সার্টিফিকেট (certificate)    10 occurrences  ✅
```
**Verdict:** Framework reports FAIL due to algorithmic limitation (Bengali stopword not filtered). Content is actually very well optimized — all topic keywords appear ≥5 times. Recommend adding `উপর` and similar Bengali stopwords to the exclusion list in `extract_primary_keyword()`.

### B: Entity Coverage
| Entity | Pattern | Found? |
|--------|---------|--------|
| location_dhaka | dhaka\|ঢাকা | ✅ |
| location_bangladesh | bangladesh\|বাংলাদেশ | ✅ |
| service_seo | SEO\|এসইও | ✅ |

No tag-triggered additional entities needed (tags: HTTPS, SSL, ওয়েবসাইট সিকিউরিটি, SEO, বাংলাদেশ — none match entity trigger lists for ecommerce, real estate, video, etc.).

### C: Pillar-Cluster Alignment
**Defined pillar pages checked:**
| Pillar | URL | Linked? |
|--------|-----|---------|
| SEO Guide | /blog/complete-seo-guide-bangladesh-businesses-2026 | ✗ |
| Local SEO | /blog/local-seo-tips-dhaka-businesses-google-maps | ✗ |
| Technical SEO | /blog/technical-seo-checklist-bangladeshi-websites | ✗ |
| Ecommerce | /blog/why-ecommerce-store-needs-seo-bangladesh | ✗ |
| Keyword | /blog/keyword-research-bangladesh-market | ✗ |
| Link Building | /blog/link-building-strategies-bangladesh-market | ✗ |
| GEO | /blog/geo-optimization-prepare-business-ai-search | ✗ |
| Content | /blog/content-marketing-seo-friendly-content-writing | ✗ |
| Mobile | /blog/mobile-seo-bangladesh-ranking-strategy | ✗ |
| **Schema** | **/blog/schema-markup-rich-snippets-techniques** | **✅** |

The post links to `/blog/schema-markup-rich-snippets-techniques`, which is the defined schema pillar. This is thematically appropriate — the conclusion paragraph mentions "আরও জানতে আমাদের স্কিমা মার্কআপ ও রিচ স্নিপেট গাইড দেখুন".

**Other blog links in content (sibling cluster posts):**
- `/blog/seo-redirects-guide-bangladesh` — sibling link (added in commit)
- `/blog/seo-canonical-url-guide-bd` — sibling link (added in commit)
- `/blog/google-search-console-performance-guide` — sibling link
- `/blog/seo-website-migration-guide-bd` — sibling link
- `/blog/schema-markup-rich-snippets-techniques` — **pillar link**

**Other internal links:**
- `/services/technical-seo` — service link
- `/locations/dhaka`, `/chittagong`, `/sylhet`, `/khulna`, `/rajshahi`, `/barisal`, `/rangpur`, `/mymensingh` — 8 location links (strong local SEO signal)
- `/contact` — contact CTA (added in commit)
- `/about` — about page

### D: AEO/GEO Optimization
**Question-based headings detected (12):**
The content has extensive question-format headings like "HTTPS এবং SSL কী?" (What are HTTPS and SSL), "কেন HTTPS SEO-র জন্য গুরুত্বপূর্ণ?" (Why is HTTPS important for SEO), etc. Also has dedicated sections:
- ✅ **GEO section** (line 16349): "GEO (Generative Engine Optimization) এবং HTTPS এবং SSL"
- ✅ **EEAT section** (line 16359): "EEAT (Experience, Expertise, Authoritativeness, Trustworthiness)"
- ✅ **AEO section** (line 16370): "AEO (Answer Engine Optimization)"
- ✅ **FAQ section** (line 16431): Standard FAQ with 3 Q&A pairs

### E: Internal Links Summary
| Type | Count | URLs |
|------|-------|------|
| Blog (sibling/pillar) | 5 | /blog/seo-redirects-guide-bangladesh, /blog/seo-canonical-url-guide-bd, /blog/google-search-console-performance-guide, /blog/schema-markup-rich-snippets-techniques, /blog/seo-website-migration-guide-bd |
| Services | 1 | /services/technical-seo |
| Locations | 8 | /locations/dhaka, /chittagong, /sylhet, /khulna, /rajshahi, /barisal, /rangpur, /mymensingh |
| Other (Contact/About) | 2 | /contact, /about |
| **Total** | **16** | |

### F: Schema Readiness
| Field | Value | Present? |
|-------|-------|----------|
| title | "HTTPS ও SSL: SEO-র উপর প্রভাব ও সেটআপ গাইড" | ✅ |
| excerpt | "HTTPS এবং SSL কীভাবে আপনার ওয়েবসাইটের SEO-কে প্রভাবিত করে..." | ✅ |
| date | "2026-07-08" | ✅ |
| author | "মোঃ কনক মিঞা" | ✅ |
| content | 14,030 chars | ✅ |
| schema.org mention | Content explicitly mentions "Schema.org ডকুমেন্টেশন" in learning resources and "স্ট্রাকচারড ডেটা (Schema.org)" in GEO section | ✅ |

---

## Modification Impact Assessment (commit f4d9445)

The 3 changes introduced in commit f4d9445:

| Change | Effect | Assessment |
|--------|--------|------------|
| 1. Sibling link to `/blog/seo-redirects-guide-bangladesh` (anchor: "রিডাইরেক্ট বেস্ট প্র্যাকটিস গাইড") | +1 internal blog link | ✅ Positive — strengthens cluster relevance (HTTPS migration → redirects) |
| 2. Sibling link to `/blog/seo-canonical-url-guide-bd` (anchor: "ক্যানোনিকাল ইউআরএল গাইড") | +1 internal blog link | ✅ Positive — strengthens cluster relevance (HTTPS migration → canonical URLs) |
| 3. Contact CTA `/contact` (anchor: "যোগাযোগ") | +1 contact link, replaces naked link | ✅ Positive — converts brand anchor to proper contact CTA |

**Net framework impact:** Internal Links count increased from 14 to 16. No other check metrics changed. All 3 changes are framework-compliant improvements.

---

## FINAL SUMMARY TABLE

| Check | Status | Score | Notes |
|-------|--------|-------|-------|
| **A: TF-IDF** | ⚠️ BORDERLINE | 3/5 (false negative) | Algorithmic limitation; real keywords (HTTPS, SSL, SEO) all well above threshold |
| **B: Entities** | ✅ PASS | 3/3 | All required entities present |
| **C: Pillar-Cluster** | ✅ PASS | 1 pillar + 4 sibling links | Linked to schema pillar page; strong cluster connectivity |
| **D: AEO/GEO** | ✅ PASS | 20 elements | Dedicated GEO, EEAT, AEO, and FAQ sections |
| **E: Internal Links** | ✅ PASS | 16 links | Blog + services + locations + contact; well distributed |
| **F: Schema** | ✅ PASS | 5/5 fields | All metadata fields complete; schema.org mentioned in content |

**Overall: 5/6 PASS, 1 BORDERLINE (TF-IDF false negative)**

**Recommended action:** The single failing check (TF-IDF) is a false negative caused by the keyword extraction algorithm selecting the Bengali stopword "উপর" instead of the actual topic keyword. If the framework is used for enforcement, consider one of:
- Add Bengali stopwords (`উপর`, `এবং`, `করে`, etc.) to the stopword list in `extract_primary_keyword()`
- Manually override the primary keyword for this post to "HTTPS" or "SSL"
- Accept the false negative — the content is genuinely well-optimized
