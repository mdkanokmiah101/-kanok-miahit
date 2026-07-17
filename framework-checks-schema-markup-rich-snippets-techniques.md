# Framework Checks Report: `schema-markup-rich-snippets-techniques`

**Post:** Schema Markup & Rich Snippets Techniques  
**Slug:** `schema-markup-rich-snippets-techniques`  
**Line:** 5014 in `/src/app/blog/data.js`  
**Date:** 2026-07-08  
**Author:** মোঃ কনক মিঞা  
**Tags:** স্কিমা মার্কআপ, Schema Markup, Rich Snippets, Structured Data, Bangladesh SEO  

---

## A. TF-IDF Coverage

| Check | Result |
|-------|--------|
| **Primary keyword extracted from title** | `স্কিমা মার্কআপ` (first meaningful noun phrase in "স্কিমা মার্কআপ: সার্চ রেজাল্টে রিচ স্নিপেট পাওয়ার কৌশল") |
| **Occurrences in content** | **13** (lines 5023×1, 5025×2, 5027×1, 5066×1, 5068×1, 5096×1, 5098×1, 5127×1, 5129×1, 5160×1, 5172×1, 5225×1) |
| **Threshold** | ≥ 5 required |
| **Verdict** | ✅ **PASS** — 13 occurrences, well above threshold |

---

## B. Semantic Entity Coverage

| Entity | Expected | Found? | Evidence |
|--------|----------|--------|----------|
| **Location: Dhaka** | Present at least once | ✅ Yes | Lines 5029, 5041, 5186, 5204, 5206 — "ঢাকা" mentioned multiple times |
| **Location: Bangladesh** | Present at least once | ✅ Yes | Lines 5027, 5033, 5110, 5150, 5204 etc. — "বাংলাদেশ"/"Bangladesh" throughout |
| **Service type** | Present at least once | ✅ Yes | "technical SEO services with schema implementation" (5131), "SEO সার্ভিস", "লোকাল SEO", "ই-কমার্স SEO", "কন্টেন্ট মার্কেটিং" (5206) |
| **Industry** | Present at least once | ✅ Yes | "রিয়েল এস্টেট, ই-কমার্স, হোটেল, রেস্টুরেন্ট, এনজিও, আইন সংস্থা" (5190) |
| **Schema markup** | Present (main topic) | ✅ Yes | Core subject of entire post |

**Verdict:** ✅ **PASS** — All required semantic entities present.

---

## C. Pillar-Cluster Alignment

| Check | Result |
|-------|--------|
| **Tags indicate pillar topic** | Schema / Structured Data / Technical SEO |
| **Links to pillar page or relevant service page** | ✅ Yes — Links to `/services/technical-seo` (lines 5131, 5218) — a relevant technical SEO service page |
| **Links to cluster content** | ✅ Yes — Links to `/blog/technical-seo-checklist-bangladeshi-websites` (5133), `/blog/seo-json-ld-schema-bangladesh` (5217), `/blog/technical-seo-core-web-vitals-optimization` (5186), `/blog/seo-semantic-search-bangla` (5135) |

The schema cluster includes sibling posts: `seo-json-ld-schema-bangladesh`, `seo-breadcrumb-schema-bd`, `seo-faq-schema-bangladesh`, `seo-howto-schema-bangladesh`. This post links to 2 of them directly.

**Verdict:** ✅ **PASS** — Pillar link to `/services/technical-seo` present; multiple cluster links included.

---

## D. AEO/GEO Optimization — Question-Based Headings

| # | Heading | Line | Question word |
|---|---------|------|---------------|
| 1 | `### Bangladesh-এ GEO কেন গুরুত্বপূর্ণ?` | 5150 | কেন (why) + `?` |
| 2 | `### কীভাবে AEO আপনার স্কিমা মার্কআপ কে সাহায্য করবে?` | 5160 | কীভাবে (how) + `?` |
| 3 | `### স্কিমা মার্কআপ এর জন্য সঠিক কৌশল কী?` | 5172 | কী (what) + `?` |
| 4 | `### AI সার্চ ইঞ্জিনের জন্য কীভাবে কন্টেন্ট অপটিমাইজ করবেন?` | 5175 | কীভাবে (how) + `?` |
| 5 | `## কেন বিশ্বাস করবেন মোঃ কনক মিঞাকে?` | 5202 | কেন (why) + `?` |
| 6 | `## আরও জানতে চান? বিশেষজ্ঞ পরামর্শ নিন` | 5210 | চান? (want?) + `?` |
| 7 | `### বাংলাদেশি ব্যবসার জন্য কোন স্কিমা টাইপ সবচেয়ে গুরুত্বপূর্ণ?` | 5227 | কোন (which) + `?` |

| Check | Result |
|-------|--------|
| **Count of question-based headings** | **7** |
| **Threshold** | ≥ 2 required |
| **Verdict** | ✅ **PASS** — Well above minimum |

---

## E. Internal Linking

### Links by type

| Link type | Paths found | Count |
|-----------|-------------|-------|
| `/blog/...` | `/blog/google-search-console-performance-guide` (5102), `/blog/technical-seo-checklist-bangladeshi-websites` (5133), `/blog/seo-semantic-search-bangla` (5135), `/blog/technical-seo-core-web-vitals-optimization` (5186), `/blog/seo-json-ld-schema-bangladesh` (5217) | **5** |
| `/services/...` | `/services/technical-seo` (5131, 5218), `/services/local-seo` (5206, 5219), `/services/ecommerce-seo` (5206, 5220), `/services/semantic-seo` (5206, 5221) | **8** (5 unique) |
| `/industries/...` | (none) | **0** |
| `/locations/...` | (none) | **0** |
| **Total** | | **13** |

| Check | Result |
|-------|--------|
| **Total internal links** (to /blog/, /services/, /industries/, /locations/) | **13** |
| **Threshold** | ≥ 3 required |
| **Verdict** | ✅ **PASS** — 13 links, well above threshold |

---

## F. Post Schema / Metadata

| Field | Present? | Value |
|-------|----------|-------|
| **title** | ✅ Yes | "স্কিমা মার্কআপ: সার্চ রেজাল্টে রিচ স্নিপেট পাওয়ার কৌশল" (line 5015) |
| **excerpt** | ✅ Yes | Detailed excerpt describing schema markup types and benefits (line 5018) |
| **date** | ✅ Yes | "2026-07-08" (line 5016) |
| **author** | ✅ Yes | "মোঃ কনক মিঞা" (line 5017) |
| **tags** | ✅ Yes | 5 tags covering স্কিমা মার্কআপ, Schema Markup, Rich Snippets, Structured Data, Bangladesh SEO (line 5020) |

**Verdict:** ✅ **PASS** — All 5 metadata fields are present.

---

## Summary

| Check | Result | Details |
|-------|--------|---------|
| **A. TF-IDF Coverage** | ✅ PASS | "স্কিমা মার্কআপ" appears 13 times (threshold: 5) |
| **B. Semantic Entity Coverage** | ✅ PASS | Dhaka, Bangladesh, service types, industries, and schema markup all present |
| **C. Pillar-Cluster Alignment** | ✅ PASS | Links to `/services/technical-seo` (pillar service page) and 4 related cluster posts |
| **D. AEO/GEO Optimization** | ✅ PASS | 7 question-based headings (threshold: 2) |
| **E. Internal Linking** | ✅ PASS | 13 internal links to /blog/ and /services/ (threshold: 3) |
| **F. Post Schema/Metadata** | ✅ PASS | All 5 fields (title, excerpt, date, author, tags) present |

### Overall: ✅ ALL CHECKS PASS — No issues flagged.
