# Framework Checks Report — Batch 2 (11 posts)

## Legend
| Check | Description | Pass threshold |
|-------|-------------|----------------|
| **A** (TF-IDF) | Primary keyword from title → occurrences in content | ≥ 5 |
| **B** (Entities) | Dhaka, Bangladesh, Google, SEO all appear | all 4 present |
| **C** (Pillar) | Links to /services/, /industries/, or /blog/ exist | ≥ 1 |
| **D** (AEO/GEO) | Question-based headings (How/What/Why/When/Where/Can/Do/Is/Are) | ≥ 2 |
| **E** (Internal Links) | Internal links to other posts/services/locations | ≥ 3 |
| **F** (Schema) | title, excerpt, date fields set | all 3 present |

## Summary Table

```
 #  Slug (truncated if >47 chars)                       A    B    C    D    E    F    🚩   Keyword (A)
--------------------------------------------------------------------------------------------------------------
 1  mobile-seo-optimization-bangladesh-mobile-first-era ✅   ✅   ✅   ✅   ✅   ✅   0    Mobile SEO
 2  content-marketing-strategy-bangladeshi-brands-seo   ✅   ✅   ✅   ✅   ✅   ✅   0    Content Marketing
 3  international-seo-bangladesh-exporters-global-buy.. ✅   ✅   ✅   ✅   ✅   ✅   0    International SEO
 4  seo-bangla-beginners-guide-google-ranking           ⚠️   ✅   ✅   ⚠️   ✅   ✅   2    সহজ ভাষায়
 5  local-seo-dhaka-google-maps-ranking                 ✅   ✅   ✅   ⚠️   ✅   ✅   1    স্থানীয় SEO
 6  seo-trends-2026-ai-geo-future                       ⚠️   ✅   ✅   ⚠️   ✅   ✅   2    ২০২৬ সালের
 7  technical-seo-core-web-vitals-optimization          ✅   ✅   ✅   ⚠️   ✅   ✅   1    টেকনিক্যাল SEO
 8  ecommerce-seo-daraz-shopify-guide                   ✅   ✅   ✅   ⚠️   ✅   ✅   1    ই-কমার্স SEO
 9  link-building-bangladesh-strategies                 ✅   ✅   ✅   ⚠️   ✅   ✅   1    লিংক বিল্ডিং
10  keyword-research-bangladesh-market                  ✅   ✅   ✅   ⚠️   ✅   ✅   1    কীওয়ার্ড রিসার্চ
11  content-marketing-seo-friendly-content-writing      ✅   ✅   ✅   ⚠️   ✅   ✅   1    কন্টেন্ট মার্কেটিং
--------------------------------------------------------------------------------------------------------------
```

**3 posts pass all 6 checks**  ✅  
**8 posts have issues** — most commonly Check D (no question-based headings → these posts use declarative Bangla headings instead of question-form)

---

## Per-Post Details

### ✅ #1 mobile-seo-optimization-bangladesh-mobile-first-era — **0/6 flags** ALL PASS
- Title: "Mobile SEO for Bangladesh: Optimize for the Mobile-First Era"
- A: "Mobile SEO" → 21x ✅
- B: Dhaka=16 Bangladesh=48 Google=22 SEO=55 ✅
- C: /services/=3 /industries/=3 /blog/=4 ✅
- D: 7 question headings ✅
- E: 11 internal links ✅
- F: all fields set ✅

### ✅ #2 content-marketing-strategy-bangladeshi-brands-seo — **0/6 flags** ALL PASS
- Title: "Content Marketing Strategy for Bangladeshi Brands: Drive SEO Growth"
- A: "Content Marketing" → 29x ✅
- B: Dhaka=14 Bangladesh=47 Google=16 SEO=30 ✅
- C: /services/=2 /industries/=0 /blog/=4 ✅
- D: 7 question headings ✅
- E: 7 internal links ✅
- F: all fields set ✅

### ✅ #3 international-seo-bangladesh-exporters-global-buyers — **0/6 flags** ALL PASS
- Title: "International SEO for Bangladesh Exporters: Attract Global Buyers"
- A: "International SEO" → 22x ✅
- B: Dhaka=8 Bangladesh=57 Google=17 SEO=46 ✅
- C: /services/=2 /industries/=1 /blog/=4 ✅
- D: 6 question headings ✅
- E: 8 internal links ✅
- F: all fields set ✅

### ⚠️ #4 seo-bangla-beginners-guide-google-ranking — **2/6 flags**
- Title: সহজ ভাষায় SEO: কীভাবে গুগলে প্রথম পেজে আসবেন (২০২৬ গাইড)
- A: "সহজ ভাষায়" → 1x ⚠️ (<5)
- B: Dhaka=5 Bangladesh=6 Google=4 SEO=87 ✅
- C: /services/=5 /industries/=0 /blog/=3 ✅
- D: 0 question headings ⚠️ (<2)
- E: 10 internal links ✅
- F: all fields set ✅

### ⚠️ #5 local-seo-dhaka-google-maps-ranking — **1/6 flags**
- Title: স্থানীয় SEO: ঢাকায় আপনার ব্যবসা কীভাবে গুগল ম্যাপে শীর্ষে দেখাবেন
- A: "স্থানীয় SEO" → 12x ✅
- B: Dhaka=6 Bangladesh=7 Google=8 SEO=55 ✅
- C: /services/=4 /industries/=0 /blog/=4 ✅
- D: 0 question headings ⚠️ (<2)
- E: 9 internal links ✅
- F: all fields set ✅

### ⚠️ #6 seo-trends-2026-ai-geo-future — **2/6 flags**
- Title: ২০২৬ সালের SEO ট্রেন্ডস: AI, GEO ও জিরো-ক্লিক সার্চের যুগে কীভাবে প্রস্তুত থাকবেন
- A: "২০২৬ সালের" → 1x ⚠️ (<5; "২০২৬ সালের" is a temporal modifier, not the core topic keyword)
- B: Dhaka=5 Bangladesh=5 Google=4 SEO=63 ✅
- C: /services/=5 /industries/=0 /blog/=3 ✅
- D: 0 question headings ⚠️ (<2)
- E: 9 internal links ✅
- F: all fields set ✅

### ⚠️ #7 technical-seo-core-web-vitals-optimization — **1/6 flags**
- Title: টেকনিক্যাল SEO: ওয়েবসাইট স্পিড ও কোর ওয়েব ভাইটালস অপটিমাইজেশন
- A: "টেকনিক্যাল SEO" → 20x ✅
- B: Dhaka=5 Bangladesh=5 Google=7 SEO=52 ✅
- C: /services/=5 /industries/=0 /blog/=2 ✅
- D: 0 question headings ⚠️ (<2)
- E: 8 internal links ✅
- F: all fields set ✅

### ⚠️ #8 ecommerce-seo-daraz-shopify-guide — **1/6 flags**
- Title: ই-কমার্স SEO: দারাজ ও শপিফাই স্টোরের জন্য সম্পূর্ণ গাইড
- A: "ই-কমার্স SEO" → 10x ✅
- B: Dhaka=5 Bangladesh=4 Google=4 SEO=74 ✅
- C: /services/=4 /industries/=1 /blog/=1 ✅
- D: 0 question headings ⚠️ (<2)
- E: 7 internal links ✅
- F: all fields set ✅

### ⚠️ #9 link-building-bangladesh-strategies — **1/6 flags**
- Title: লিংক বিল্ডিং: বাংলাদেশি ওয়েবসাইটের জন্য কার্যকরী কৌশল
- A: "লিংক বিল্ডিং" → 15x ✅
- B: Dhaka=5 Bangladesh=5 Google=4 SEO=38 ✅
- C: /services/=6 /industries/=0 /blog/=1 ✅
- D: 0 question headings ⚠️ (<2)
- E: 8 internal links ✅
- F: all fields set ✅

### ⚠️ #10 keyword-research-bangladesh-market — **1/6 flags**
- Title: কীওয়ার্ড রিসার্চ: বাংলাদেশি মার্কেটের জন্য সঠিক কীওয়ার্ড নির্বাচন
- A: "কীওয়ার্ড রিসার্চ" → 19x ✅
- B: Dhaka=6 Bangladesh=5 Google=7 SEO=50 ✅
- C: /services/=5 /industries/=0 /blog/=1 ✅
- D: 0 question headings ⚠️ (<2)
- E: 7 internal links ✅
- F: all fields set ✅

### ⚠️ #11 content-marketing-seo-friendly-content-writing — **1/6 flags**
- Title: কন্টেন্ট মার্কেটিং: SEO-ফ্রেন্ডলি কন্টেন্ট কীভাবে লিখবেন
- A: "কন্টেন্ট মার্কেটিং" → 5x ✅ (exactly at threshold)
- B: Dhaka=5 Bangladesh=7 Google=5 SEO=45 ✅
- C: /services/=5 /industries/=0 /blog/=2 ✅
- D: 0 question headings ⚠️ (<2)
- E: 8 internal links ✅
- F: all fields set ✅

---

## Entity Counts Matrix

```
 #  Slug                                     Dhaka    Bangladesh   Google   SEO
------------------------------------------------------------------------------
 1  mobile-seo-optimization...               16       48           22       55
 2  content-marketing-strategy...            14       47           16       30
 3  international-seo-exporters...            8       57           17       46
 4  seo-bangla-beginners-guide...             5        6            4       87
 5  local-seo-dhaka...                        6        7            8       55
 6  seo-trends-2026-ai-geo...                 5        5            4       63
 7  technical-seo-core-web-vitals...          5        5            7       52
 8  ecommerce-seo-daraz-shopify...            5        4            4       74
 9  link-building-bangladesh...               5        5            4       38
10  keyword-research-bangladesh...            6        5            7       50
11  content-marketing-seo-friendly...         5        7            5       45
```

**All 11 posts pass Check B** — all 4 entities (Dhaka, Bangladesh, Google, SEO) appear in every post.

---

## Internal & Pillar Link Counts

```
 #  Slug                                    Total      /services/   /industries/   /blog/
--------------------------------------------------------------------------------------------
 1  mobile-seo-optimization...               11         3            3              4
 2  content-marketing-strategy...             7         2            0              4
 3  international-seo-exporters...            8         2            1              4
 4  seo-bangla-beginners-guide...            10         5            0              3
 5  local-seo-dhaka...                        9         4            0              4
 6  seo-trends-2026-ai-geo...                 9         5            0              3
 7  technical-seo-core-web-vitals...          8         5            0              2
 8  ecommerce-seo-daraz-shopify...            7         4            1              1
 9  link-building-bangladesh...               8         6            0              1
10  keyword-research-bangladesh...            7         5            0              1
11  content-marketing-seo-friendly...         8         5            0              2
```

**All 11 posts pass Check C** (each has at least one pillar link) and **Check E** (each has at least 3 internal links).

---

## Key Findings

1. **All 11 posts have good entity coverage** (Check B) — Dhaka, Bangladesh, Google, and SEO all appear in every post.

2. **All 11 posts have sufficient internal/pillar linking** (Checks C & E) — every post links to /services/, /industries/, or /blog/, and has at least 3 total internal links.

3. **All 11 posts have complete schema fields** (Check F) — title, excerpt, and date are all present.

4. **3 English posts pass all 6 checks** with zero flags.

5. **Systemic Check D failure on Bangla posts:** 8 of 8 Bangla-language posts have 0 question-based headings. These posts use declarative Bangla headings (e.g., "টেকনিক্যাল SEO কী?" appears as content but not as a heading in ## format). The question words "কীভাবে" (how) appear frequently in titles and body text but never as the start of an `## Heading`. This is a style choice worth noting — adding question-form `## How do I...` / `## What is...` headings would improve AEO/GEO readiness.

6. **Minor Check A issues on 2 Bangla posts:**
   - Post 4: "সহজ ভাষায়" (literal: "easy language") → only 1x in content
   - Post 6: "২০২৬ সালের" ("2026's") → only 1x in content (it's a temporal modifier, not the core topic)
   These are false positives caused by taking the first 2 words of a Bangla title that aren't the actual core subject keyword.

---

**Files created:**
- `/root/kanok-miahit/check_blog_posts.py` — initial version
- `/root/kanok-miahit/check_blog_posts_v2.py` — improved with markdown link support
- `/root/kanok-miahit/check_blog_posts_v3.py` — final version with 2-word keyword extraction
