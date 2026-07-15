# Framework Check Report — what-does-seo-expert-do-guide-business-owners

**Date:** 2026-07-15  
**Title:** What Does an SEO Expert Actually Do? A Complete Guide for Business Owners  
**Author:** Md Kanok Miah  
**Tags:** SEO Expert Guide, SEO Services, Dhaka SEO, Digital Marketing Bangladesh  
**Content Length:** 31,235 chars  
**Slug:** what-does-seo-expert-do-guide-business-owners

---

## Results Summary

| # | Check | Status | Details |
|---|-------|--------|---------|
| 1 | **TF-IDF / Keyword Density** | ✅ PASS | 'seo expert' — 53 occurrences (threshold: ≥5) |
| 2 | **Entities** | ✅ PASS | Dhaka ✓, Bangladesh ✓, Google ✓, SEO ✓, Expert ✓, Business ✓ |
| 3 | **Pillar Link** | ❌ FAIL | No links to `/services/`, `/industries/`, or `/blog/` pillar pages |
| 4 | **AEO/GEO (Question Headings)** | ✅ PASS | 12 question headings found (threshold: ≥2) |
| 5 | **Internal Links** | ❌ FAIL | Only 1 unique internal link → /contact (threshold: ≥3) |
| 6 | **Schema Readiness** | ✅ PASS | Title ✓, Excerpt ✓, Date ✓, Author ✓, Tags ✓ |

**Overall: 4/6 checks pass — ❌ NOT framework compliant**

---

## Detailed Results

### Criterion 1: TF-IDF / Keyword Density ✅
- **Best keyword:** `seo expert`
- **Occurrences:** 53
- **Threshold:** ≥5
- **Verdict:** Pass — strong keyword presence throughout the 31K-char content.

### Criterion 2: Entities ✅
- **Required entities checked:** Dhaka, Bangladesh, Google, SEO, Expert, Business
- **All present.** The content naturally references Dhaka businesses, Bangladeshi context, Google/E-E-A-T framework, and SEO expert activities extensively.

### Criterion 3: Pillar Link ❌
- **Links found in content (normalized):** `/contact` (1 link)
- **Pillar pages checked:** `/services/`, `/industries/`, `/blog/`
- **Verdict:** The post has **no links** to any service, industry, or blog pillar pages. All 7 links point to `kanokmiah.com.bd/` (homepage) or `kanokmiah.com.bd/contact`. 
- **Fix needed:** Add internal links to relevant pillar pages, such as:
  - `/industries/food-restaurant`
  - `/industries/real-estate`
  - `/industries/ecommerce`
  - `/industries/medical`
  - `/services/geo-ai-search`
  - `/case-studies`
  - `/industries/cleaning`

### Criterion 4: AEO/GEO ✅
- **Total headings:** 38
- **Question headings found (12):**
  1. Introduction: What Does an SEO Expert Actually Do?
  2. The Short Answer: What Does an SEO Expert Do?
  3. When Should You Hire an SEO Expert?
  4. What does an SEO expert do on a daily basis?
  5. How is an SEO expert different from a digital marketing agency?
  6. How long does it take for an SEO expert to show results?
  7. What tools does an SEO expert use?
  8. Can an SEO expert help with Bengali-language SEO?
  9. How much do SEO expert services cost in Bangladesh?
  10. What is the difference between an SEO expert and an SEO consultant?
  11. Should I hire an in-house SEO expert or outsource?
  12. How do I choose the right SEO expert for my business?
- **Verdict:** Excellent AEO/GEO optimization — 12 question-based headings exceed the ≥2 threshold, making the content highly extractable by AI search engines.

### Criterion 5: Internal Links ❌
- **Unique internal links found:** 1
  - `/contact`
- **Threshold:** ≥3
- **Verdict:** Only 1 unique internal link. The post needs at least 3 internal links to different internal pages.
- **Note:** All links use absolute URLs (`https://kanokmiah.com.bd/...`). While functional, switching to relative paths (e.g., `/contact` instead of `https://kanokmiah.com.bd/contact`) is recommended for SEO value flow.
- **Fix needed:** Add ≥2 more internal links to industry/service/blog pages (see pillar link recommendations above).

### Criterion 6: Schema Readiness ✅
- **Title:** ✅ "What Does an SEO Expert Actually Do? A Complete Guide for Business Owners"
- **Excerpt:** ✅ Present (140 chars) — properly describes the post
- **Date:** ✅ 2026-07-14
- **Author:** ✅ Md Kanok Miah
- **Tags:** ✅ [SEO Expert Guide, SEO Services, Dhaka SEO, Digital Marketing Bangladesh]
- **Verdict:** All structural metadata present for Article schema implementation.
- *(Note: The framework_check_v2.py script incorrectly reports excerpt as missing due to a multiline parsing bug — the excerpt is actually present and correctly formatted.)*

---

## Fix Instructions

1. **❌ Add pillar links** — Insert links to `/services/`, `/industries/`, or `/blog/` pillar pages in relevant sections. Suggested placements:
   - In "Local SEO and Google Business Profile Management" section → link to `/industries/cleaning` or similar
   - In "Key Responsibilities" section → link to `/services/geo-ai-search` when discussing GEO/AEO
   - In content strategy section → link to `/case-studies`
   - In restaurant/local examples → link to `/industries/food-restaurant`

2. **❌ Add more internal links** — Currently only 1 unique internal path (`/contact`). Add ≥2 more links to distinct internal destinations. Use relative paths (`/industries/...`) instead of absolute URLs (`https://kanokmiah.com.bd/...`).

3. **ℹ️ Optional: Convert absolute URLs to relative** — All 7 links use `https://kanokmiah.com.bd/...` format. For proper SEO link equity flow and framework checker compatibility, use relative paths like `/contact`, `/industries/food-restaurant`, `/services/geo-ai-search`.

---

## Framework Checker Note

The existing `framework_check_v2.py` script reports **3 failures** (Pillar Link, Internal Links, Schema Ready) due to two bugs:
1. **Multi-line excerpt bug:** The parser breaks on multi-line `excerpt:` fields (value on next line), incorrectly reporting the excerpt as missing. The excerpt actually exists.
2. **Absolute URL handling:** The script only counts links starting with `/` as internal links. It does not normalize `https://kanokmiah.com.bd/...` URLs to their relative paths.

This corrected analysis handles both edge cases and reports the accurate status.

---

**Report generated by:** Hermes Agent (corrected analysis)  
**Raw output saved to:** /root/kanok-miahit/framework-report-what-does-seo-expert-do-guide-business-owners.md
