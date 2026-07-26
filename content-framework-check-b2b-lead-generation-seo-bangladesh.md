# Content Framework Check Report

**Post:** B2B Lead Generation through SEO in Bangladesh  
**Slug:** b2b-lead-generation-seo-bangladesh  
**File:** `/root/kanok-miahit/src/app/blog/data.js` (lines 19520–19729)  
**Date:** 2026-07-08  

---

## A. TF-IDF — Keyword Frequency

| Item | Value |
|------|-------|
| Title | "B2B Lead Generation through SEO in Bangladesh" |
| Primary keyword extracted | **B2B Lead Generation** |
| Occurrences in English | 5 (title + 1 heading + 3 body mentions) |
| Occurrences in Bengali (লিড জেনারেশন) | 12 |
| **Total occurrences** | **17** |
| Threshold | ≥ 5 |
| **Result** | ✅ **PASS** (17 ≥ 5) |

---

## B. Entity Presence Check

| Entity | Present? | Evidence |
|--------|----------|----------|
| **Bangladesh** | ✅ YES | In title, excerpt, headings, body throughout |
| **B2B** | ✅ YES | In title, excerpt, tags, body extensively |
| **lead generation** | ✅ YES | In title, excerpt, headings, body |
| **SEO** | ✅ YES | In title, excerpt, tags, body extensively |
| **manufacturing** | ✅ YES | Line 19587: "topics like **manufacturing** and exports" |

**Result:** ✅ **PASS** — All 5 entities present.

---

## C. Pillar Link Check

| Criteria | Value |
|----------|-------|
| Expected pillar URL | `/blog/complete-seo-guide-bangladesh-businesses-2026` |
| Found? | ✅ YES (line 19726) |
| Anchor text | "Complete SEO Guide for Bangladesh Businesses 2026" |

**Result:** ✅ **PASS** — Pillar link found.

---

## D. AEO/GEO — Question-Based Headings

Question-based headings found (4 total):

1. `## What is B2B Lead Generation SEO?`
2. `### B2B SEO কী?`
3. `### B2B SEO-র মূল পার্থক্য কী?`
4. `### B2B লিড জেনারেশনের জন্য কোন ধরনের কন্টেন্ট ভালো?`

| Threshold | Count | Result |
|-----------|-------|--------|
| ≥ 2 | 4 | ✅ **PASS** |

---

## E. Internal Links Count

| Category | Unique Paths | Total Occurrences |
|----------|-------------|-------------------|
| `/blog/` | 6 unique internal + 1 external (Ahrefs) | 6 internal |
| `/services/` | 4 sub-pages + `/services` root | 5 |
| `/locations/` | 8 city pages | 8 |
| **Total** | — | **19** |

**/blog/ internal links:**
- `/blog/seo-for-startups-bangladesh`
- `/blog/seo-travel-tourism-bangladesh`
- `/blog/seo-garments-textile-industry-b2b-lead-generation`
- `/blog/seo-for-ngo-bangladesh`
- `/blog/seo-for-hotel-resort-bangladesh`
- `/blog/complete-seo-guide-bangladesh-businesses-2026`

**/services/ links:**
- `/services` (root)
- `/services/link-building`
- `/services/on-page-seo`
- `/services/technical-seo`
- `/services/ecommerce-seo`

**/locations/ links:**
- `/locations/dhaka`, `/locations/chittagong`, `/locations/sylhet`, `/locations/khulna`
- `/locations/rajshahi`, `/locations/barisal`, `/locations/rangpur`, `/locations/mymensingh`

**Additional internal links (bonus):**
- `/industries/` (line 19574)
- `/industries/garments-textile` (line 19617)
- `/about` (line 19728)
- `/contact` (line 19728)

| Threshold | Count | Result |
|-----------|-------|--------|
| ≥ 3 | 19 | ✅ **PASS** |

---

## F. Schema / Metadata Check

| Field | Value | Set? |
|-------|-------|------|
| **title** | "B2B Lead Generation through SEO in Bangladesh" | ✅ YES (line 19521) |
| **excerpt** | "A complete guide to generating high-quality B2B leads in Bangladesh using SEO — targeting manufacturers, importers, exporters, and service buyers through strategic organic search content." | ✅ YES (line 19524–19525) |
| **date** | "2026-07-08" | ✅ YES (line 19522) |
| **author** | "Kanok Miah" | ✅ YES (line 19523) |
| **tags** | ["B2B SEO", "Lead Generation", "Bangladesh Business", "Industrial SEO"] | ✅ YES (line 19526) |
| **imagePlaceholder** | "🏭" | ✅ YES (line 19527) |

**Result:** ✅ **PASS** — All schema/metadata fields properly set.

---

## Summary

| Check | Status | Detail |
|-------|--------|--------|
| A. TF-IDF Keyword Frequency | ✅ PASS | 17 occurrences of "B2B lead generation" (≥ 5) |
| B. Entity Presence (5 entities) | ✅ PASS | All 5 present |
| C. Pillar Link | ✅ PASS | Links to `/blog/complete-seo-guide-bangladesh-businesses-2026` |
| D. AEO/GEO Question Headings | ✅ PASS | 4 question-based headings (≥ 2) |
| E. Internal Links (/blog/, /services/, /locations/) | ✅ PASS | 19 total (≥ 3) |
| F. Schema/Metadata | ✅ PASS | title, excerpt, date, author, tags all set |

**Overall: ✅ ALL CHECKS PASSED**
