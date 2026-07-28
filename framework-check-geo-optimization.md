# Framework Check Report: geo-optimization-prepare-business-ai-search

**Post slug:** `geo-optimization-prepare-business-ai-search`
**File:** `src/app/blog/data.js` (lines 1021–1201)
**Checked:** 2026-07-27

---

## Summary Table

| Check | Status | Details |
|-------|--------|---------|
| **A. TF-IDF Coverage** | ⚠️ PASS (marginal) | 5 occurrences of "GEO Optimization" in body (6 including title). Meets threshold but thin. |
| **B. Semantic Entity Coverage** | ✅ PASS | Dhaka, Bangladesh, GEO/AI Search, industries all present. |
| **C. Pillar-Cluster Alignment** | ✅ PASS | Links to pillar page `/blog/complete-seo-guide-bangladesh-businesses-2026` at line 1070. |
| **D. AEO/GEO Optimization** | ✅ PASS | 10 question-based headings found (threshold ≥ 2). |
| **E. Internal Linking** | ✅ PASS | 23 internal links across /blog/, /services/, /locations/, /industries/, /about, /contact (threshold ≥ 3). |
| **F. Schema Fields** | ✅ PASS | title, date, excerpt, author, tags all present. |

---

## A. TF-IDF Coverage — ⚠️ PASS (marginal)

**Primary keyword:** `GEO Optimization` (first meaningful noun phrase from title)

**Occurrences in content body:**
| # | Line | Context |
|---|------|---------|
| 1 | 1032 | "This comprehensive **GEO Optimization** guide will help..." |
| 2 | 1058 | "## **GEO Optimization** Strategies" (H2 heading) |
| 3 | 1074 | "A successful **GEO Optimization** strategy depends on..." |
| 4 | 1092 | "'## What is **GEO Optimization**?' rather than..." (in example text) |
| 5 | 1191 | "**GEO Optimization** is not optional — it is essential..." |

**Total: 5 in body (+1 in title at line 1023 = 6)**

**Verdict:** At threshold (5). Barely passes. Consider adding 2–3 more natural uses to strengthen TF-IDF signal.

---

## B. Semantic Entity Coverage — ✅ PASS

| Entity | Expected | Found | Lines |
|--------|----------|-------|-------|
| **Dhaka** (location) | ≥ 1 | ✓ Multiple | 1036, 1066, 1068, 1090, 1116, 1156, 1197 |
| **Bangladesh/Bangladeshi** (location) | ≥ 1 | ✓ Extensive | Throughout entire post |
| **GEO/Generative Engine Optimization** (service) | ≥ 1 | ✓ Extensive | Primary topic |
| **Industries** (medical, education, ecommerce, real estate, garments, restaurant) | ≥ 1 | ✓ Multiple | 1034, 1062 |

All key entities present with good coverage.

---

## C. Pillar-Cluster Alignment — ✅ PASS

**Tags:** `["GEO", "AI Search", "Generative Engine Optimization", "Future of SEO"]`
**Pillar topic:** GEO / AI Search (branches from the main SEO pillar page)

**Link to pillar page:** ✅ Found at line 1070:
> "My [comprehensive SEO guide for Bangladesh businesses](/blog/complete-seo-guide-bangladesh-businesses-2026) is structured as a topic cluster..."

**Recommendation:** The link is good. Consider also adding an explicit pillar mention in the conclusion section (line 1191 area) where "complete SEO guide for Bangladesh businesses" is mentioned in plain text but NOT hyperlinked.

---

## D. AEO/GEO Optimization — ✅ PASS

**Question-based headings found (10 total):**

| # | Line | Heading |
|---|------|---------|
| 1 | 1031 | `## What is Generative Engine Optimization?` |
| 2 | 1038 | `## How AI Search Engines Work` |
| 3 | 1050 | `## Why GEO Matters for Bangladesh Businesses` |
| 4 | 1134 | `### How to Be First in AI Search Results` |
| 5 | 1168 | `### What is the difference between SEO and GEO?` |
| 6 | 1171 | `### Is GEO more important than traditional SEO?` |
| 7 | 1174 | `### How do I know if my content is being cited by AI search engines?` |
| 8 | 1177 | `### Can Bengali content rank in AI search?` |
| 9 | 1180 | `### How is GEO different for B2B vs B2C businesses?` |
| 10 | 1183 | `### How long does GEO take to show results?` |

**Verdict:** 10 ≥ 2 — ✅ Passes easily. Strong question-heading coverage.

---

## E. Internal Linking — ✅ PASS

**Internal links found in post (23 total):**

| Type | Links | Lines |
|------|-------|-------|
| `/industries/` | `/industries/medical`, `/industries/education`, `/industries/ecommerce`, `/industries/real-estate`, `/industries/garments-textile`, `/industries/food-restaurant` | 1034, 1062 |
| `/blog/` | `/blog/complete-seo-guide-bangladesh-businesses-2026`, `/blog/technical-seo-checklist-bangladeshi-websites`, `/blog/local-seo-tips-dhaka-businesses-google-maps`, `/blog/why-ecommerce-store-needs-seo-bangladesh`, `/blog/seo-trends-2026-ai-geo-future` | 1070, 1136, 1191, 1197 |
| `/services/` | `/services/link-building`, `/services/geo-ai-search`, `/services/local-seo`, `/services/on-page-seo`, `/services/technical-seo`, `/services/ecommerce-seo` | 1136, 1197, 1199 |
| `/locations/` | `/locations/dhaka`, `/locations/chittagong`, `/locations/sylhet` | 1156 |
| Other | `/` (home), `/about`, `/contact` | 1036, 1197, 1199 |

**Verdict:** 23 ≥ 3 — ✅ Excellent internal linking coverage.

---

## F. Schema Fields — ✅ PASS

| Field | Value | Present |
|-------|-------|---------|
| `title` | "GEO Optimization: Prepare Your Business for AI Search" | ✅ |
| `date` | "2026-05-08" | ✅ |
| `excerpt` | "Generative Engine Optimization (GEO) is the next frontier in SEO..." | ✅ |
| `author` | "Kanok Miah" | ✅ |
| `tags` | ["GEO", "AI Search", "Generative Engine Optimization", "Future of SEO"] | ✅ |
| `imagePlaceholder` | "🤖" | ✅ |

All required fields for ArticleSchema markup are present.

---

## Overall Verdict

| Metric | Result |
|--------|--------|
| **Checks Passed** | 6/6 (5 ✅, 1 ⚠️) |
| **Overall** | **GOOD** — needs minor TF-IDF improvement |

**Primary fix needed:** Add 2–3 more occurrences of "GEO Optimization" in the body text to strengthen TF-IDF signal. Opportunities:
1. In the "Measuring GEO Success" section (line 1138), start with something like "Measuring **GEO Optimization** success requires different metrics..."
2. In "The Bangladesh Advantage" section (line 1126), add a sentence like "**GEO Optimization** for Bangladesh businesses represents a first-mover advantage..."
3. In the Conclusion (line 1191), reinforce: "**GEO Optimization** is essential for businesses..."

**Secondary fix:** Add a hyperlink to the pillar page at line 1197 where "complete SEO guide for Bangladesh businesses" appears as unlinked plain text.
