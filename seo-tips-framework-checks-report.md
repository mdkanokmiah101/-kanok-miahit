# Framework Checks Report: `seo-tips-for-business-owners-bd`

**Post Slug:** `seo-tips-for-business-owners-bd`
**Title:** ব্যবসায়ীদের জন্য SEO টিপস: নিজেই SEO করুন
**File:** `/root/kanok-miahit/src/app/blog/data.js` (lines 5912–6179)
**Date:** 2026-07-08
**Author:** মোঃ কনক মিঞা
**Tags:** ব্যবসায়ীদের জন্য SEO, DIY SEO, বাংলাদেশ ব্যবসা, লোকাল SEO

---

## A. TF-IDF Coverage ❌ FLAGGED

- **Primary keyword extracted from title (first meaningful noun phrase):** `SEO টিপস` (SEO Tips)
- **Occurrences in content body:** **0**
- **Threshold:** ≥ 5
- **Status:** ❌ **FAIL** — Keyword `SEO টিপস` appears only in the title metadata (line 5913) but zero times in the actual content body (lines 5919–6179).

> **Note:** The broader term `SEO` appears very frequently throughout the content (~50+ occurrences), but the specific primary keyphrase `SEO টিপ스` as extracted from the title is never used in the body. Consider naturally weaving the primary keyphrase into headings and introductory paragraphs.

---

## B. Semantic Entity Coverage ✅ PASS

| Entity | Expected? | Found? | Evidence |
|--------|-----------|--------|----------|
| **Location: Dhaka (ঢাকা)** | ✅ | ✅ Yes | Lines 5924, 5928, 5932, 6081, 6094, 6119, 6122, 6132, 6140, 6150, 6152 |
| **Location: Bangladesh (বাংলাদেশ)** | ✅ | ✅ Yes | Lines 5922, 5976, 6079, 6094, 6096, 6098, 6132, 6136, 6140, 6150, 6152, 6162, 6171, 6175 |
| **Service type: SEO** | ✅ | ✅ Yes | Throughout entire content body |
| **Industry: Business (ব্যবসা/ব্যবসায়ী)** | ✅ | ✅ Yes | Throughout entire content body |

- **Status:** ✅ **PASS** — All key entities (Dhaka/Bangladesh, SEO, Business) are present and repeatedly referenced.

---

## C. Pillar-Cluster Alignment ✅ PASS

- **Tags:** `ব্যবসায়ীদের জন্য SEO`, `DIY SEO`, `বাংলাদেশ ব্যবসা`, `লোকাল SEO`
- **Likely pillar topic:** "SEO for Business" / "Local SEO for Bangladesh"
- **Pillar/service page links found:**
  - `/services/on-page-seo` (line 5968)
  - `/services/technical-seo` (lines 6071, 6152, 6164)
  - `/services/local-seo` (lines 6075, 6152, 6165)
  - `/services/ecommerce-seo` (lines 6152, 6166)
  - `/services/semantic-seo` (lines 6152, 6167)
  - `/blog/complete-seo-guide-bangladesh-businesses-2026` (line 6073 — likely pillar page)
- **Status:** ✅ **PASS** — Multiple relevant service pages and a likely pillar blog post are linked.

---

## D. AEO/GEO Optimization ✅ PASS

- **Question-based headings found (Bengali equivalents of How/What/Why/When/Where):**

| # | Heading | Line | Question Word |
|---|---------|------|---------------|
| 1 | `## ব্যবসায়ীদের জন্য SEO: কেন এটি গুরুত্বপূর্ণ?` | 5920 | কেন (Why) |
| 2 | `## SEO কী এবং কেন ব্যবসায়ীদের এটি জানা দরকার?` | 5926 | কী (What) + কেন (Why) |
| 3 | `## কখন প্রফেশনাল সাহায্য নেওয়া উচিত?` | 6059 | কখন (When) |
| 4 | `### Bangladesh-এ GEO কেন গুরুত্বপূর্ণ?` | 6096 | কেন (Why) |
| 5 | `### কীভাবে AEO আপনার ব্যবসার জন্য SEO কে সাহায্য করবে?` | 6106 | কীভাবে (How) |
| 6 | `### ব্যবসার জন্য SEO এর জন্য সঠিক কৌশল কী?` | 6118 | কী (What) |
| 7 | `### AI সার্চ ইঞ্জিনের জন্য কীভাবে কন্টেন্ট অপটিমাইজ করবেন?` | 6121 | কীভাবে (How) |
| 8 | `## কেন বিশ্বাস করবেন মোঃ কনক মিঞাকে?` | 6148 | কেন (Why) |
| 9 | `## আরও জানতে চান? বিশেষজ্ঞ পরামর্শ নিন` | 6156 | চান? (question) |

- **Total question-based headings:** **9**
- **Threshold:** ≥ 2
- **Status:** ✅ **PASS** — Well above the minimum of 2. Rich question-based content structure suitable for AEO/GEO.

---

## E. Internal Linking ✅ PASS

- **Internal links found in content body:**

| # | Link | Type | Line |
|---|------|------|------|
| 1 | `/blog/seo-bangla-blog-content-writing` | `/blog/` | 5989 |
| 2 | `/blog/content-marketing-strategy-bangladeshi-brands-seo` | `/blog/` | 5989 |
| 3 | `/blog/content-marketing-seo-friendly-content-writing` | `/blog/` | 5989 |
| 4 | `/blog/complete-seo-guide-bangladesh-businesses-2026` | `/blog/` | 6073 |
| 5 | `/blog/what-does-seo-expert-do-guide-business-owners` | `/blog/` | 6163 |
| 6 | `/services/on-page-seo` | `/services/` | 5968 |
| 7 | `/services/technical-seo` | `/services/` | 6071, 6152, 6164 |
| 8 | `/services/local-seo` | `/services/` | 6075, 6152, 6165 |
| 9 | `/services/ecommerce-seo` | `/services/` | 6152, 6166 |
| 10 | `/services/semantic-seo` | `/services/` | 6152, 6167 |
| 11 | `/about` | internal | 6150 |
| 12 | `/contact` | internal | 6162 |
| 13 | `/` (home) | internal | 6152 |

- **Total unique internal links:** **13+** (5 blog posts + 5 service types + about + contact + home)
- **Threshold:** ≥ 3
- **Status:** ✅ **PASS** — Excellent internal linking with plenty of blog and service page links.

---

## F. Schema / Required Fields ✅ PASS

| Field | Present? | Value |
|-------|----------|-------|
| **title** | ✅ Yes | ব্যবসায়ীদের জন্য SEO টিপস: নিজেই SEO করুন |
| **excerpt** | ✅ Yes | বাংলাদেশি ব্যবসায়ীদের জন্য সম্পূর্ণ DIY SEO গাইড — কীভাবে নিজেই আপনার বিজনেসের SEO করবেন... |
| **date** | ✅ Yes | 2026-07-08 |
| **author** | ✅ Yes | মোঃ কনক মিঞা |
| **tags** | ✅ Yes | ["ব্যবসায়ীদের জন্য SEO", "DIY SEO", "বাংলাদেশ ব্যবসা", "লোকাল SEO"] |

- **Status:** ✅ **PASS** — All five required schema fields are present.

---

## Overall Summary

| Check | Status |
|-------|--------|
| A. TF-IDF Coverage | ❌ **FAIL** — Primary keyphrase `SEO টিপস` not found in content body (0 occurrences) |
| B. Semantic Entity Coverage | ✅ PASS |
| C. Pillar-Cluster Alignment | ✅ PASS |
| D. AEO/GEO Optimization | ✅ PASS (9 question headings) |
| E. Internal Linking | ✅ PASS (13+ internal links) |
| F. Schema Fields | ✅ PASS |

**1 issue flagged:** The primary keyphrase `SEO টিপস` extracted from the title is never used in the actual content body. Recommend introducing it in at least one H2 heading or the introductory paragraph to improve topical relevance and TF-IDF signal.
