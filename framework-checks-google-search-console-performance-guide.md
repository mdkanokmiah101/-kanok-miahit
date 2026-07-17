# Framework Checks Report: `google-search-console-performance-guide`

**Slug:** `google-search-console-performance-guide`  
**Title:** গুগল সার্চ কনসোল: আপনার ওয়েবসাইটের পারফরমেন্স বুঝুন  
**Location in data.js:** Line 4599  
**Date:** 2026-07-08  
**Author:** মোঃ কনক মিঞা  
**Tags:** গুগল সার্চ কনসোল, Google Search Console, SEO টুল, ওয়েবসাইট পারফরমেন্স, Bangladesh SEO  

---

## A. TF-IDF Coverage

- **Primary keyword extracted from title:** `গুগল সার্চ কনসোল` (first meaningful noun phrase)
- **Occurrences in content:** **9** (title, excerpt, tags, 2× H2 headings, 2× H3 headings, 2× body paragraphs, 1× concluding paragraph)
- **Threshold:** ≥ 5
- **Result:** ✅ **PASS** (9 occurrences — well above the 5 minimum)

---

## B. Semantic Entity Coverage

| Entity | Expected | Found? | Evidence |
|--------|----------|--------|----------|
| **Location: Bangladesh** | At least once | ✅ | "বাংলাদেশি" (lines 4612, 4650, 4667, 4671, 4699), "বাংলাদেশের" (lines 4671, 4718, 4722), "Bangladesh" (lines 4720, 4776) |
| **Location: Dhaka** | At least once | ✅ | "ঢাকা" / "dhaka" in lines 4714, 4746, 4756, 4764, 4774, 4776 |
| **Service type: SEO / Technical SEO** | At least once | ✅ | "SEO" appears throughout; "টেকনিক্যাল SEO" in headings and body; links to `/services/technical-seo` |
| **Industry: Web/Digital** | At least once | ✅ | "ডিজিটাল মার্কেটিং" (line 4756), various industry references |
| **Google Search Console** | At least once | ✅ | Primary subject of the entire post |

**Result:** ✅ **PASS** — All expected entities are present.

---

## C. Pillar-Cluster Alignment

- **Tags analysis:** The tags center on **Google Search Console / SEO Tools / Website Performance** — strongly aligning with a **Technical SEO** pillar.
- **Identified pillar page(s):**
  - `slug: "seo-pillar-content-strategy-bd"` — Pillar Content Strategy (general pillar methodology)
  - `slug: "technical-seo-checklist-bangladeshi-websites"` — Technical SEO checklist (cluster within technical SEO)
  - `/services/technical-seo` — Technical SEO service page (de facto pillar for technical SEO)
- **Links found in this post:**
  1. `[কোর ওয়েব ভাইটালস মনিটর링](/blog/technical-seo-core-web-vitals-optimization)` — cluster blog
  2. `[complete technical SEO checklist](/blog/technical-seo-checklist-bangladeshi-websites)` — cluster blog
  3. `[technical SEO services with Search Console setup](/services/technical-seo)` — **service pillar link**
  4. `[on-page SEO services for better rankings](/services/on-page-seo)` — service link
  5. `[জেনারেটিভ ইঞ্জিন অপটিমাইজেশন](/services/geo-ai-search)` — service link
  6. Multiple service links in the closing section: `[টেকনিক্যাল SEO](/services/technical-seo)`, `[লোকাল SEO](/services/local-seo)`, `[ই-কমার্স SEO](/services/ecommerce-seo)`, `[কন্টেন্ট মার্কেটিং](/services/semantic-seo)`
- **Pillar/topical authority link present:** ✅ Yes — links directly to `/services/technical-seo` (the technical SEO pillar) and to cluster blog posts within the technical SEO topic.

**Result:** ✅ **PASS** — Post links to a relevant pillar/service page and cluster content.

---

## D. AEO/GEO Optimization — Question-Based Headings

All headings in the post checked for starting with How, What, Why, When, Where, Can, Do, Is, Are (English) or কী, কেন, কীভাবে, কখন, কোথায়, পারে, কর, হয়, are (Bangla):

| Line | Heading | Starts with question word? |
|------|---------|--------------------------|
| 4608 | `## গুগল সার্চ কনসোল কী এবং কেন এটি দরকার` | ❌ (starts with "গুগল") |
| 4614 | `## গুগল সার্চ কনসোল সেটআপ করা` | ❌ |
| 4626 | `## পারফরমেন্স রিপোর্ট বোঝা` | ❌ |
| 4642 | `## কীওয়ার্ড পারফরমেন্স বিশ্লেষণ` | ❌ |
| 4652 | `## ইনডেক্সিং ইস্যু চেক করা` | ❌ |
| 4663 | `## কোর ওয়েব ভাইটালস রিপোর্ট` | ❌ |
| 4669 | `## মোবাইল ইউসাবিলিটি রিপোর্ট` | ❌ |
| 4678 | `## লিংক রিপোর্ট` | ❌ |
| 4686 | `## নিয়মিত GSC চেকলিস্ট` | ❌ |
| 4695 | `## উপসংহার` | ❌ |
| 4708 | `## জেনারেটিভ ইঞ্জিন অপটিমাইজেশন (GEO)` | ❌ |
| 4720 | `### Bangladesh-এ GEO কেন গুরুত্বপূর্ণ?` | ❌ (starts with "Bangladesh") |
| 4726 | `## AI সার্চ ও অ্যানসার ইঞ্জিন অপটিমাইজেশন` | ❌ |
| 4730 | `### কীভাবে AEO আপনার গুগল সার্চ কনসোল কে সাহায্য করবে?` | ✅ ("কীভাবে" = How) |
| 4740 | `### AEO প্রশ্ন-উত্তর` | ❌ |
| 4742 | `### গুগল সার্চ কনসোল এর জন্য সঠিক কৌশল কী?` | ❌ (starts with "গুগল") |
| 4745 | `### AI সার্চ ইঞ্জিনের জন্য কীভাবে কন্টেন্ট অপটিমাইজ করবেন?` | ❌ (starts with "AI") |
| 4750 | `## E-E-A-T: Google-এর গুণগত মানের মাপকাঠি` | ❌ |
| 4772 | `## কেন বিশ্বাস করবেন মোঃ কনক মিঞাকে?` | ✅ ("কেন" = Why) |

- **Question-based headings found:** **2** (lines 4730 and 4772)
- **Threshold:** ≥ 2
- **Result:** ✅ **PASS** (2 question headings — meets the minimum)

---

## E. Internal Linking

Links to `/blog/`, `/services/`, `/industries/`, `/locations/` in the post:

| # | Link | Type |
|---|------|------|
| 1 | `[কোর ওয়েব ভাইটালস মনিটরিং](/blog/technical-seo-core-web-vitals-optimization)` | `/blog/` |
| 2 | `[complete technical SEO checklist](/blog/technical-seo-checklist-bangladeshi-websites)` | `/blog/` |
| 3 | `[technical SEO services with Search Console setup](/services/technical-seo)` | `/services/` |
| 4 | `[on-page SEO services for better rankings](/services/on-page-seo)` | `/services/` |
| 5 | `[জেনারেটিভ ইঞ্জিন অপটিমাইজেশন](/services/geo-ai-search)` | `/services/` |
| 6 | `[ভয়েস সার্চ SEO](/blog/voice-search-seo-bangladesh)` | `/blog/` |
| 7 | `[টেকনিক্যাল SEO](/services/technical-seo)` | `/services/` |
| 8 | `[লোকাল SEO](/services/local-seo)` | `/services/` |
| 9 | `[ই-কমার্স SEO](/services/ecommerce-seo)` | `/services/` |
| 10 | `[কন্টেন্ট মার্কেটিং](/services/semantic-seo)` | `/services/` |

- **Total internal links found:** **10** (3× to `/blog/`, 7× to `/services/`)
- **Threshold:** ≥ 3
- **Result:** ✅ **PASS** (10 internal links)

---

## F. Schema / Metadata Fields

| Field | Present? | Value |
|-------|----------|-------|
| **slug** | ✅ | `google-search-console-performance-guide` |
| **title** | ✅ | গুগল সার্চ কনসোল: আপনার ওয়েবসাইটের পারফরমেন্স বুঝুন |
| **excerpt** | ✅ | গুগল সার্চ কনসোল ব্যবহার করে আপনার ওয়েবসাইটের... সম্পূর্ণ গাইড |
| **date** | ✅ | `2026-07-08` |
| **author** | ✅ | মোঃ কনক মিঞা |
| **tags** | ✅ | 5 tags: গুগল সার্চ কনসোল, Google Search Console, SEO টুল, ওয়েবসাইট পারফরমেন্স, Bangladesh SEO |

**Result:** ✅ **PASS** — All required schema/metadata fields are present.

---

## Overall Summary

| Check | Result | Notes |
|-------|--------|-------|
| A. TF-IDF Coverage | ✅ **PASS** | 9 occurrences of primary keyword "গুগল সার্চ কনসোল" |
| B. Semantic Entity Coverage | ✅ **PASS** | All entities (Bangladesh, Dhaka, SEO, GSC) covered |
| C. Pillar-Cluster Alignment | ✅ **PASS** | Links to `/services/technical-seo` (pillar) and cluster blogs |
| D. AEO/GEO Optimization | ✅ **PASS** | 2 question-based headings (lines 4730, 4772) |
| E. Internal Linking | ✅ **PASS** | 10 internal links (3 blog + 7 services) |
| F. Schema/Metadata | ✅ **PASS** | All 6 fields present |

**Final verdict: All 6 checks PASS.** The post is well-optimized across all framework dimensions.
