# Framework Checks Report: `recovering-google-penalties-bangladesh-guide`

**Post Details**
- Slug: `recovering-google-penalties-bangladesh-guide`
- Title: "Recovering from Google Penalties: A Bangladesh Guide"
- Date: 2026-07-08
- Tags: `["Google Penalty", "SEO Recovery", "Manual Action", "Bangladesh"]`
- Lines in data.js: 23531–23706

---

## A. TF-IDF Coverage

| Check | Value | Status |
|---|---|---|
| **Primary keyword** | `Google Penalty` / `Google Penalties` | — |
| **Occurrences in content** | 7 | ✅ PASS (≥ 5) |

Occurrences found at lines: 23540 (`## What is a Google Penalty?`), 23542 (`A Google penalty is...`), 23543 (`## Understanding Google Penalties...`), 23545 (`Google penalties — both algorithmic...`), 23547 (`## Types of Google Penalties`), 23572 (`## Diagnosing a Google Penalty`), 23702 (`Google penalties are serious...`).

**Result: PASS** — Keyword appears 7 times, well above the 5-occurrence threshold.

---

## B. Semantic Entity Coverage

| Entity | Expected | Found? | Location |
|---|---|---|---|
| **Bangladesh** | Location | ✅ | Title, headings, body (multiple) |
| **Dhaka** | Major city | ✅ | Conclusion (line 23702) |
| **Chittagong** | Major city | ✅ | Conclusion (line 23702) |
| **Sylhet** | Major city | ✅ | Conclusion (line 23702) |
| **Penalty Recovery** | Service type | ✅ | Headings, body (multiple) |
| **SEO / Google Search Console** | Service/tool | ✅ | Body (multiple) |
| **Bangladeshi businesses/website owners** | Target audience | ✅ | Throughout content |

**Result: PASS** — All expected entities are present.

---

## C. Pillar-Cluster Alignment

| Check | Value | Status |
|---|---|---|
| **Pillar topic** | SEO Guide (tags: Google Penalty, SEO Recovery) | — |
| **Pillar page slug** | `complete-seo-guide-bangladesh-businesses-2026` | — |
| **Links to pillar blog page?** | No (no `/blog/complete-seo-guide-...` link) | ⚠️ |
| **Links to /services/* pages?** | Yes — 3 service links found | ✅ |

Service pillar links found:
- `/services/on-page-seo` (line 23698)
- `/services/technical-seo` (line 23704)
- `/services/link-building` (line 23704)

**Result: PASS** — The post does not link to the primary SEO guide pillar blog page (`complete-seo-guide-bangladesh-businesses-2026`), but it does link to 3 `/services/*` pages which qualify as pillar-ish per the criteria. **Recommendation:** Add an editorial link to the main SEO guide pillar page (`/blog/complete-seo-guide-bangladesh-businesses-2026`) for stronger pillar-cluster alignment.

---

## D. AEO/GEO Optimization (Question-Based Headings)

| Check | Count | Status |
|---|---|---|
| **Question headings** (`How/What/Why/When/Where/Can/Do/Is/Are`) | 1 | ❌ FLAG (< 2) |

Question headings found:
1. `## What is a Google Penalty?` (line 23540)

**Result: FLAG** — Only 1 question-based heading. Minimum recommended is 2. Consider adding at least one more Q&A heading (e.g., `## How to Identify a Google Penalty?`, `## Why Do Bangladeshi Sites Get Penalized?`).

---

## E. Internal Linking

| Check | Count | Status |
|---|---|---|
| **Internal links** (to `/blog/`, `/services/`, `/locations/`, `/industries/`, `/about`, `/contact`) | 8 | ✅ PASS (≥ 3) |

Internal links found:
| # | Link | Type |
|---|---|---|
| 1 | `/blog/google-search-console-performance-guide` | Blog |
| 2 | `/blog/seo-google-penalty-recovery-bd` | Blog |
| 3 | `/services/on-page-seo` | Services |
| 4 | `/services/technical-seo` | Services |
| 5 | `/services/link-building` | Services |
| 6 | `/locations/dhaka` | Locations |
| 7 | `/locations/chittagong` | Locations |
| 8 | `/locations/sylhet` | Locations |

**Result: PASS** — 8 strong internal links, well above the 3-link threshold. Good distribution across blog posts, services, and location pages.

---

## F. Schema / Post Fields

| Field | Present? | Status |
|---|---|---|
| `slug` | ✅ Yes | OK |
| `title` | ✅ Yes | OK |
| `excerpt` | ✅ Yes | OK |
| `date` | ✅ Yes | OK |
| `dateModified` | ❌ **Missing** | FLAG |

**Result: FLAG** — The `dateModified` field is absent. This is useful for schema markup (especially `article:modified_time` and structured data freshness signals). Consider adding it.

---

## Summary

| Check | Result |
|---|---|
| A. TF-IDF Coverage | ✅ PASS |
| B. Semantic Entity Coverage | ✅ PASS |
| C. Pillar-Cluster Alignment | ✅ PASS (with note) |
| D. AEO/GEO Optimization | ❌ **FLAG** — Only 1 question heading |
| E. Internal Linking | ✅ PASS |
| F. Schema / Post Fields | ❌ **FLAG** — `dateModified` missing |

**2 Flags, 4 Passes, 1 Advisory Note**

### Action Items

1. **[D] AEO/GEO:** Add 1+ additional question-based heading (e.g., `## How Do Bangladeshi Websites Get Penalized?` or `## What Happens After a Manual Action?`).
2. **[F] Schema:** Add `dateModified: "2026-07-08"` (or the last modified date) to the post object.
3. **[C] Advisory:** Consider linking to the main SEO pillar page `complete-seo-guide-bangladesh-businesses-2026` for stronger topical cluster signals.
