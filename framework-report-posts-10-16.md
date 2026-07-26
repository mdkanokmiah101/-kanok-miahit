# Framework Report: Blog Posts 10-16 (Technical SEO Cluster)
**Generated:** 2026-07-19  
**Analyzed posts:** 7 posts in Bengali (Technical SEO pillar cluster)  
**Author:** মোঃ কনক মিঞা  
**Date:** All dated 2026-07-08

---

## 1. Overview

| # | Slug | Title (EN) | Word Count | Tags |
|---|------|-----------|-----------|------|
| 10 | seo-structured-data-guide-bd | Structured Data: Complete Schema.org Guide | ~1,772 | স্ট্রাকচারড ডাটা, Schema.org, স্কিমা মার্কআপ, রিচ রেজাল্ট, বাংলাদেশ |
| 11 | seo-hreflang-guide-bangladesh | Hreflang Tag: Guide for Multilingual Websites | ~1,814 | Hreflang ট্যাগ, মাল্টিলিঙ্গুয়াল SEO, আন্তর্জাতিক SEO, বাংলা ভাষা, বাংলাদেশ |
| 12 | seo-xml-sitemap-guide-bd | XML Sitemap Guide: Properly Submit Pages to Google | ~1,794 | XML সাইটম্যাপ, গুগল সার্চ কনসোল, সাইটম্যাপ সাবমিট, টেকনিকেল SEO, বাংলাদেশ |
| 13 | seo-robots-txt-guide-bangladesh | Robots.txt: Search Engine Crawl Control | ~1,912 | রোবটস.টেক্সট, ক্রল নিয়ন্ত্রণ, টেকনিকেল SEO, সার্চ ইঞ্জিন, বাংলাদেশ |
| 14 | seo-canonical-url-guide-bd | Canonical URL: Solving Duplicate Content Issues | ~1,849 | ক্যানোনিকাল ইউআরএল, ডুপ্লিকেট কন্টেন্ট, টেকনিকেল SEO, ক্যানোনিকাল ট্যাগ, বাংলাদেশ |
| 15 | seo-redirects-guide-bangladesh | Redirect Guide: 301, 302 & SEO Best Practices | ~2,290 | রিডাইরেক্ট, 301 রিডাইরেক্ট, 302 রিডাইরেক্ট, SEO বেস্ট প্র্যাকটিস, বাংলাদেশ |
| 16 | seo-google-penalty-recovery-bd | Google Penalty Recovery: Complete Guide for BD Sites | ~2,409 | গুগল পেনাল্টি, পেনাল্টি রিকভারি, SEO, গুগল অ্যালগরিদম, বাংলাদেশ |

---

## 2. CRITICAL ISSUES

### 2.1 Missing Excerpt/Meta Description — ALL 7 POSTS
Every single post has an **empty `excerpt` field**. This means:
- No meta description is set for SERP snippets
- Google will auto-generate snippets, potentially missing keyword-rich context
- Social sharing previews will lack proper descriptions

**Action Required:** Add Bengali meta descriptions (120-160 chars) summarizing each post with target keywords.

### 2.2 Missing `dateModified` — ALL 7 POSTS
All posts have `dateModified: ""`. For SEO freshness signals, this should at minimum mirror `date`.

**Action Required:** Set `dateModified` to same as `date` (2026-07-08) or leave empty if truly not modified.

### 2.3 Duplicate Sections Within Two Posts
**seo-redirects-guide-bangladesh** and **seo-google-penalty-recovery-bd** have severely **duplicated content sections** within the same post:

| Section | Redirects Post | Penalty Post |
|---------|---------------|-------------|
| GEO (Generative Engine Optimization) | Appears **2×** | Appears **2×** |
| EEAT (Experience, Expertise...) | Appears **2×** | Appears **2×** |
| AEO (Answer Engine Optimization) | Appears **2×** | Appears **2×** |
| FAQ | Appears **2×** | Appears **2×** |

This is a **critical quality issue** — duplicate content within the same page confuses readers and search engines. The repeated sections appear to be artifacts from template merging.

**Action Required:** Remove duplicate GEO/EEAT/AEO/FAQ sections from both posts.

### 2.4 Cross-Post Duplicate Boilerplate — ALL 7 POSTS
Three sections are **identical boilerplate text copied across all 7 posts**:

1. **AEO Section** — Exactly 481 chars, verbatim identical in every post:
   > "Answer Engine Optimization (AEO) হলো কন্টেন্ট অপটিমাইজ করার একটি কৌশল যা সরাসরি প্রশ্নের উত্তর প্রদানের উপর ফোকা..."

2. **EEAT Section** — Nearly identical (~727-800 chars) starting with:
   > "Google-এর EEAT ফ্রেমওয়ার্ক আপনার কন্টেন্টের বিশ্বাসযোগ্যতা নির্ধারণে গুরুত্বপূর..."

3. **GEO Section** — Same structure, same opening sentence template:
   > "২০২৬ সালে, Generative Engine Optimization (GEO) একটি গুরুত্বপূর্ণ SEO কৌশল হয়ে উঠেছে..."

**Recommendation:** While some template reuse is expected, these sections should be **at minimum 30-40% unique per post** with post-specific context. Otherwise they risk being flagged as thin/duplicate content.

---

## 3. POSITIVE FINDINGS

### 3.1 Strong AEO (Answer Engine Optimization) Implementation
All 7 posts effectively use Bengali question words (কী, কেন, কিভাবে, কি, কখন, কোথায়, কীভাবে) in H3 headings. Specifics:

| Post | AEO Question Words in Headings |
|------|-------------------------------|
| structured-data-guide-bd | কী (3), কেন (1), কি (1) |
| hreflang-guide-bangladesh | কী (3), কেন (1), কি (1), কোথায় (1) |
| xml-sitemap-guide-bd | কী (2), কেন (1), কখন (2) |
| robots-txt-guide-bangladesh | কী (3), কেন (1), কি (1), কোথায় (2), কীভাবে (1) |
| canonical-url-guide-bd | কী (3), কেন (1), কীভাবে (1), কি (1) |
| redirects-guide-bangladesh | কী (3), কেন (2), কি (1), কখন (1) |
| google-penalty-recovery-bd | কী (2), কেন (1), কি (1), কীভাবে (1) |

This is **excellent for answer engine optimization** — directly addressing user questions in heading structure.

### 3.2 FAQ Sections
All 7 posts include FAQ sections with question-answer pairs, further supporting AEO and featured snippet optimization.

### 3.3 Good Content Depth
Word counts range from ~1,772 to ~2,409 Bengali words, which is solid for comprehensive technical guides.

### 3.4 Pillar Topic Linking (Technical SEO)
5 out of 7 posts link to `/services/technical-seo`:
- seo-structured-data-guide-bd ✅
- seo-xml-sitemap-guide-bd ✅
- seo-robots-txt-guide-bangladesh ✅
- seo-redirects-guide-bangladesh ✅
- seo-google-penalty-recovery-bd ✅
- seo-hreflang-guide-bangladesh ❌ (links to /services/on-page-seo instead)
- seo-canonical-url-guide-bd ❌ (links to /services/on-page-seo instead)

### 3.5 Contact CTAs
All posts include contact/যোগাযোগ CTAs for conversion.

---

## 4. CROSS-LINKING ANALYSIS (Within Cluster)

| Post | Links TO this cluster | Links FROM this cluster | Rating |
|------|---------------------|----------------------|--------|
| structured-data-guide-bd | robots-txt, xml-sitemap | canonical-url-guide-bd | ⚠️ Partial |
| hreflang-guide-bangladesh | canonical-url, xml-sitemap | *(none)* | ⚠️ Partial |
| xml-sitemap-guide-bd | canonical-url, redirects, robots-txt | structured-data, hreflang, robots-txt | ✅ Good |
| robots-txt-guide-bangladesh | canonical-url, xml-sitemap | structured-data, xml-sitemap | ⚠️ Partial |
| canonical-url-guide-bd | redirects, structured-data | hreflang, xml-sitemap, robots-txt, redirects | ✅ Good |
| redirects-guide-bangladesh | canonical-url | xml-sitemap, canonical-url | ⚠️ Partial |
| google-penalty-recovery-bd | **NONE** | *(none)* | ❌ Isolated |

**seo-google-penalty-recovery-bd** is entirely isolated — it has no cross-links to/from any of the other 6 posts in this cluster. It also does not link to any other blog/seo-* post within the cluster.

---

## 5. STRUCTURAL OBSERVATIONS

### 5.1 Heading Hierarchy
- All posts have only **1 H2** (the post title) — all content is under H3 headings
- This flat structure is acceptable but unconventional; consider using more H2s for major sections

### 5.2 Images
- **Zero images across all 7 posts**
- No diagrams, screenshots, or infographics for highly visual technical SEO topics
- Missed opportunity for image search traffic and engagement

### 5.3 Breadcrumb Mention
- Only `seo-structured-data-guide-bd` mentions breadcrumb schema
- Other posts don't mention breadcrumbs despite being part of a structured content hierarchy

### 5.4 External Links
All posts link to 1-3 authoritative external sources (Google Search Central, Moz, etc.) — good for credibility.

---

## 6. SUMMARY OF ACTIONS REQUIRED

| Priority | Issue | Posts Affected |
|----------|-------|---------------|
| 🔴 **Critical** | Duplicate GEO/EEAT/AEO/FAQ sections within same post | seo-redirects-guide-bangladesh, seo-google-penalty-recovery-bd |
| 🔴 **Critical** | Empty excerpt (meta description) | All 7 posts |
| 🟡 **High** | Cross-post duplicate boilerplate (GEO/EEAT/AEO sections identical) | All 7 posts |
| 🟡 **High** | Isolated post with no cluster cross-linking | seo-google-penalty-recovery-bd |
| 🟡 **High** | Empty dateModified | All 7 posts |
| 🟢 **Medium** | No images across any post | All 7 posts |
| 🟢 **Medium** | Missing links to /services/technical-seo pillar from 2 posts | seo-hreflang-guide-bangladesh, seo-canonical-url-guide-bd |
| 🟢 **Medium** | Only single H2 per post (flat structure) | All 7 posts |

---

## 7. OVERALL ASSESSMENT

**Content Quality:** Generally strong — well-structured Bengali technical SEO guides with good depth (1,700-2,400 words each), excellent use of AEO question words, and proper FAQ sections.

**Technical Issues:** Two posts have severe duplicate content issues within themselves (redirects and penalty recovery). All posts lack meta descriptions, and the boilerplate GEO/EEAT/AEO sections across all posts reduce content originality.

**SEO Framework Health:** The cluster shows good internal linking overall with some gaps. The isolated `seo-google-penalty-recovery-bd` post needs integration. Pillar page linking is good but not universal.

**Overall Rating: 7/10** — Solid foundation with critical fixes needed on deduplication and metadata before going live.
