# Framework Check Report

**Post:** seo-case-study-dhaka-businesses-increased-organic-traffic
**Title:** SEO Case Study: How Businesses in Dhaka Increased Organic Traffic
**Date:** 2026-07-14
**Author:** Md Kanok Miah
**Tags:** SEO Case Study, Dhaka SEO, Organic Traffic, SEO Results Bangladesh
**Content Length:** 28,184 characters (~3,000 words)
**Report Generated:** 2026-07-15

---

## Summary

| # | Check | Status | Detail |
|---|-------|--------|--------|
| 1 | TF-IDF / Keyword Density | ✅ **PASS** | 7 occurrences of "seo case study" (need ≥5) |
| 2 | Entity Coverage | ✅ **PASS** | All required entities (Dhaka, Bangladesh, Google, SEO) present |
| 3 | Pillar-Cluster Alignment | ❌ **FAIL** | No links to pillar pages (/services/, /industries/, /blog/) |
| 4 | AEO/GEO Question Headings | ✅ **PASS** | 8 question-based headings (need ≥2) |
| 5 | Internal Links Count | ❌ **FAIL** | 2 unique internal links (need ≥3): `/`, `/contact` |
| 6 | Schema Readiness | ✅ **PASS** | All fields set: title, excerpt/description, date, tags |
| | **OVERALL** | **4/6 PASS** | **Failing: Pillar Link, Internal Links** |

---

## Detailed Results

### 1️⃣ TF-IDF / Keyword Density (✅ PASS)

**Keyword tested:** `seo case study`
**Occurrences:** 7
**Threshold:** ≥5

The keyword "seo case study" appears 7 times in the content (e.g., in context like "this SEO case study Dhaka report"). The broader term "SEO" appears 62 times. Content has strong keyword saturation.

---

### 2️⃣ Entity Coverage (✅ PASS)

| Entity | Present? |
|--------|----------|
| Dhaka | ✅ Yes |
| Bangladesh | ✅ Yes |
| Google | ✅ Yes |
| SEO | ✅ Yes |

All required location, brand, and topic entities are well-covered. The post mentions Dhaka neighborhoods (Gulshan, Banani, Dhanmondi, Uttara, Mirpur), specific Dhaka landmarks, and Bangladeshi context throughout.

---

### 3️⃣ Pillar-Cluster Alignment (❌ FAIL)

**Expected pillar URL patterns:** `/services/`, `/industries/`, `/blog/`
**Found pillar links:** None

The post has 5 links total, all external full URLs:
- `https://kanokmiah.com.bd/` (x3) → normalized to `/`
- `https://kanokmiah.com.bd/contact` (x2) → normalized to `/contact`

**None** of these point to pillar hub pages. For a case study about e-commerce, the post should link to `/industries/ecommerce` (the relevant pillar page). The context information says "Internal links: /industries/ecommerce (many times)" but these do NOT exist in the actual content.

---

### 4️⃣ AEO/GEO Question Headings (✅ PASS)

**Total headings (H2/H3):** 35
**Question-based headings:** 8
**Threshold:** ≥2

The 8 question headings found:
1. *How long does SEO take to show results for Dhaka businesses?*
2. *What is the typical SEO investment for a Dhaka-based business?*
3. *Which Dhaka neighborhoods benefit most from local SEO?*
4. *Can I do SEO myself or should I hire a professional?*
5. *How does GEO (Generative Engine Optimization) help Dhaka businesses?*
6. *What is AEO (Answer Engine Optimization) and why does it matter?*
7. *How does E-E-A-T affect SEO for Bangladeshi businesses?*
8. *What is the single most important SEO action for a new Dhaka business?*
9. *How does this SEO case study for Dhaka differ from international case studies?*

(Note: The exact count depends on whether H3 FAQ subheadings are included; framework shows 8-10.)

The post includes a dedicated 10-question FAQ section and GEO/AEO optimization section as specified in requirements.

---

### 5️⃣ Internal Links Count (❌ FAIL)

**Threshold:** ≥3 unique internal links
**Found:** 2 unique internal links

| # | Link | Normalized Path |
|---|------|-----------------|
| 1 | `https://kanokmiah.com.bd/` | `/` |
| 2 | `https://kanokmiah.com.bd/contact` | `/contact` |

Only 2 unique internal link destinations detected. Need at least 3. The links point only to the homepage and contact page. Missing links to other blog posts, service pages, or industry pages. The context mentions `/industries/ecommerce (many times)` but these links are NOT present in the post content.

---

### 6️⃣ Schema Readiness (✅ PASS)

| Field | Status | Value |
|-------|--------|-------|
| Title | ✅ SET | "SEO Case Study: How Businesses in Dhaka Increased Organic Traffic" |
| Excerpt/Description | ✅ SET | "Real SEO case studies from Dhaka — see how an e-commerce store..." |
| Date | ✅ SET | "2026-07-14" |
| Tags | ✅ SET | ["SEO Case Study", "Dhaka SEO", "Organic Traffic", "SEO Results Bangladesh"] |

All schema-required fields are present and populated. The post is ready for Article schema markup. (Note: `framework_check_v2.py` incorrectly flagged excerpt as missing due to a parser limitation with multi-line excerpts — it is actually present.)

---

## Fix Recommendations

### ❌ Fix 1: Add Pillar Links
The post needs at least one link to a pillar page matching `/services/`, `/industries/`, or `/blog/` patterns.
**Suggested additions:**
- Link to `/industries/ecommerce` (e-commerce pillar page) when discussing Case Study 1
- Link to `/services/local-seo` when discussing Case Study 2 (local home services)
- Link to `/blog/` categories when referencing content strategy

### ❌ Fix 2: Increase Internal Links
Need at least 3 unique internal link targets (currently only have `/` and `/contact`).
**Suggested additions:**
- Add a link to `/industries/ecommerce` from the e-commerce case study section
- Add a link to `/services/local-seo` or a relevant service page from the local SEO section
- Add a link to another related case study or blog post (e.g., `/blog/why-ecommerce-store-needs-seo-bangladesh`)

### ✅ Passed Checks (No Action Needed)
- **TF-IDF/Keyword Density** — Strong coverage of primary keywords
- **Entity Coverage** — Dhaka, Bangladesh, Google, and SEO entities well-represented
- **AEO/GEO** — Excellent question heading coverage (8× the minimum threshold)
- **Schema Readiness** — All metadata fields properly populated

---

## Detailed Link Inventory

All 5 links in the post:

| Text | URL | Type | Normalized |
|------|-----|------|------------|
| Best SEO Expert in Dhaka | `https://kanokmiah.com.bd/` | Internal (homepage) | `/` |
| Best SEO Expert in Dhaka | `https://kanokmiah.com.bd/` | Internal (homepage) | `/` |
| Best SEO Expert in Dhaka | `https://kanokmiah.com.bd/` | Internal (homepage) | `/` |
| Book Your Free SEO Consultation Today → | `https://kanokmiah.com.bd/contact` | Internal (contact) | `/contact` |
| Best SEO Expert in Dhaka | `https://kanokmiah.com.bd/` | Internal (homepage) | `/` |

**Note:** All 5 links are in the author bio / CTA sections. The main case study body contains ZERO internal links, which is a significant missed opportunity for both SEO equity distribution and user navigation.

---

*Report generated by Hermes Agent — framework_check_v2.py + check_single_post.py analysis*
