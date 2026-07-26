# Homepage SEO/AEO/GEO Audit — kanokmiah.com.bd

**Date:** 2026-07-21  
**Auditor:** Automated agent  
**Target Keywords:** "Best SEO Expert in Dhaka", "Best SEO Expert in Bangladesh"  
**Scanned Files:** `page.js`, `layout.js`, `HomeClient.js`, `faq-data.js`, `Schema.js`

---

## 1. Title Tag

**Source:** `page.js` line 12 exports a flat `title` string. In Next.js 14+, the layout (`layout.js` line 23-26) has `title: { default: "...", template: "%s — Kanok Miah | SEO Expert in Dhaka, Bangladesh" }`. The page title replaces the `default`, then the layout `template` is applied.

**Resulting title:**  
`Best SEO Expert in Dhaka, Bangladesh | Kanok Miah — Kanok Miah | SEO Expert in Dhaka, Bangladesh`

| Keyword | Present? | Detail |
|---------|----------|--------|
| "Best SEO Expert in Dhaka" | ✅ **Yes** | Exact substring found in page title |
| "Best SEO Expert in Bangladesh" | ❌ **No** | Title says "Best SEO Expert in **Dhaka, Bangladesh**" — not the isolated phrase "Bangladesh" without "Dhaka" |

**Recommendation:**
- Add a variant targeting "Best SEO Expert in Bangladesh" as a standalone phrase.  
  Suggested title templates:
  - `Best SEO Expert in Dhaka & Bangladesh | Kanok Miah — #1 SEO Specialist`
  - Or use the layout template more effectively. Since layout template appends `— Kanok Miah | SEO Expert in Dhaka, Bangladesh`, the current page title already ends with "Kanok Miah" and then the template repeats it. Consider removing the "| Kanok Miah" from the page title to reduce redundancy:
    - `page.js` title → `"Best SEO Expert in Dhaka, Bangladesh"`
    - Final would be `"Best SEO Expert in Dhaka, Bangladesh — Kanok Miah | SEO Expert in Dhaka, Bangladesh"`
- Better yet, craft a title alternating the keywords on different pages (homepage can target both).

---

## 2. H1 Heading

**Source:** `HomeClient.js` lines 91-94
```jsx
<h1>
  <span className="text-primary">Best SEO Expert</span>{' '}
  <span className="block text-gray-900 whitespace-nowrap">in Dhaka, Bangladesh</span>
</h1>
```
**Rendered text:** `Best SEO Expert in Dhaka, Bangladesh`

| Keyword | Present? | Detail |
|---------|----------|--------|
| "Best SEO Expert in Dhaka" | ✅ **Yes** | Substring found in continuous text |
| "Best SEO Expert in Bangladesh" | ❌ **No** | Text reads "Dhaka, Bangladesh" — the comma and "Dhaka" break the exact phrase |

**Recommendation:**
- The H1 is strong for Dhaka but misses the Bangladesh-only variant. Consider:
  - `Best SEO Expert in Dhaka & Bangladesh` (covers both in one H1)
  - Or keep as-is but ensure "Best SEO Expert in Bangladesh" appears in an H2 or strong paragraph on the page (it does — see below).

---

## 3. Meta Description

**Source:** `page.js` lines 13-14 (page-level overrides layout.js lines 27-28)
```
"Rank higher with Kanok Miah, the best SEO expert in Dhaka, Bangladesh. 6+ years, 210+ proven SEO wins. Free SEO audit for your business — Call 01604-809110."
```

| Keyword | Present? | Detail |
|---------|----------|--------|
| "Best SEO Expert in Dhaka" | ✅ **Yes** | "the best SEO expert in Dhaka, Bangladesh" contains the phrase (case-insensitive match) |
| "Best SEO Expert in Bangladesh" | ❌ **No** | Same issue — "Dhaka, Bangladesh" breaks the exact phrase |

**Recommendation:**
- Add a description variant that isolates "Best SEO Expert in Bangladesh":  
  `"Kanok Miah — the best SEO expert in Bangladesh and Dhaka. 6+ years, 210+ SEO wins. Free audit — Call 01604-809110."`
- The layout.js description is actually stronger semantically but is overridden by page.js. Consider merging the best of both.

---

## 4. First 200 Words of Visible Content

**Hero paragraph** (`HomeClient.js` lines 95-97):
> *"Your competitors are ranking. You're not. That's not bad luck — that's a fixable problem. I'm Kanok Miah, the best SEO expert in Bangladesh and a top-rated SEO strategist in Dhaka. I've run 210+ SEO campaigns across e-commerce, local businesses — and I don't do cookie-cutter strategies..."*

| Keyword | Present? | Detail |
|---------|----------|--------|
| "Best SEO Expert in Dhaka" | ✅ **Yes** | "a top-rated SEO strategist in Dhaka" — semantic match, not exact phrase |
| "Best SEO Expert in Bangladesh" | ✅ **Yes** | Exact phrase: "the **best SEO expert in Bangladesh**" (lowercase, but matches) |

**Also:** The hero badge (line 89) says `#1 SEO Expert in Bangladesh` — strong semantic signal.

**Recommendation:** ✅ No change needed here. The first 100 words nail both keywords.

---

## 5. Schema Markup

### Global schemas in `layout.js` (applied to every page):
| Schema | Target Keyword in name/description? |
|--------|-------------------------------------|
| OrganizationSchema | ❌ name: "Md Kanok Miah", description: "SEO expert since 2019..." |
| LocalBusinessSchema | ❌ name: "Md Kanok Miah — SEO Expert", description: "SEO expert since 2019..." |
| WebSiteSchema | ❌ name: "Md Kanok Miah" |
| PersonSchema | ❌ name: "Md Kanok Miah", description: "SEO expert since 2019..." |
| Inline Service `@graph` | ❌ Service.name: "Local SEO", "On-Page SEO", etc. |

### Page-specific schemas in `page.js`:
| Schema | Target Keyword in name/description? |
|--------|-------------------------------------|
| AggregateRatingSchema | ❌ itemReviewed.name: "Md Kanok Miah — SEO Expert" |
| ReviewSchema | ❌ itemReviewed.name: "Md Kanok Miah — SEO Expert" |
| VideoObjectSchema | ❌ name describes video content |
| BreadcrumbSchema | ⚠️ `{ name: "SEO Expert Dhaka", url: "..." }` — partial match only |
| FAQSchema | ⚠️ Questions target Dhaka/Bangladesh SEO but none use exact target keywords as question text |

| Keyword | Present in any schema? |
|---------|----------------------|
| "Best SEO Expert in Dhaka" | ❌ Not in any schema name or description field |
| "Best SEO Expert in Bangladesh" | ❌ Not in any schema name or description field |

**Recommendation:**
- **OrganizationSchema**: Add `alternateName: "Best SEO Expert in Dhaka, Bangladesh"` or include it in `description`.  
  E.g., `description: "Best SEO Expert in Dhaka, Bangladesh — SEO since 2019, 210+ projects."`
- **LocalBusinessSchema**: Change `name` to `"Kanok Miah — Best SEO Expert in Dhaka, Bangladesh"` or add `alternateName`.
- **WebSiteSchema**: Add `alternateName` or include the keyword in `description`.
- **BreadcrumbSchema**: Change second item name from `"SEO Expert Dhaka"` to `"Best SEO Expert in Dhaka, Bangladesh"`.
- **FAQSchema**: Add a FAQ question that uses the target keyword, e.g.,  
  Q: `"Why is Kanok Miah considered the best SEO expert in Bangladesh?"`
- **AggregateRatingSchema**: Change `itemName` prop default to `"Best SEO Expert in Dhaka, Bangladesh"`.

---

## 6. Internal Links

### Navbar links (`HomeClient.js` lines 55-59):
✅ `/services`, `/case-studies`, `/industries`, `/blog`, `/about`, `/contact`

### Services section (lines 358-371):
✅ Links to:
- `/services/local-seo`
- `/services/on-page-seo`
- `/services/link-building`
- `/services/technical-seo`
- `/services/geo-ai-search`
- `/services/ecommerce-seo`

### Location page link:
✅ Stats band (line 182): `<Link href="/locations/dhaka">Dhaka</Link>`

### Industries section (lines 402-420):
✅ Links to industry subpages (garments-textile, ecommerce, smm-panel, real-estate, etc.)

### Other internal links:
✅ Case study links to blog posts  
✅ "View All Services/Industries/Case Studies" links  
✅ Contact form → `/contact`  
✅ About → `/about`

| Criteria | Status |
|----------|--------|
| Links to `/services/*` | ✅ Present |
| Link to `/locations/dhaka` | ✅ Present |
| Links to blog/case studies | ✅ Present |

**Recommendation:** Consider adding an anchor link from the H1 or hero to the `/locations/dhaka` page for stronger topical relevance.

---

## 7. AEO/GEO Readiness

### Question-based H2 headings (excellent AEO practice):

| H2 Text | Location (line) | Quality |
|---------|-----------------|---------|
| "What SEO Services Does Kanok Miah Offer in Dhaka?" | 379-380 | ✅ Excellent — question format, location-specific |
| "What Makes Kanok Miah the Best SEO Expert in Dhaka?" | 462-463 | ✅ **Contains target keyword** in question |
| "How Long Does SEO Take to Show Results in Dhaka?" | 629-630 | ✅ Question format, location-specific, high search volume |
| "How Much Does SEO Cost in Bangladesh?" | 746-747 | ✅ Question format, country-specific |
| "How Can I Hire the Best SEO Expert in Dhaka?" | 788-789 | ✅ **Contains target keyword** in question |
| "People Also Ask About SEO in Bangladesh" | 810-811 | ✅ Mimics Google PAA feature |

### FAQ Schema:
✅ **Present** — `FAQSchema` on page.js line 119 with 10 questions from `faq-data.js`  
✅ Questions cover: Maps ranking (Dhaka), new website strategy (Bangladesh), timeline, pricing, Daraz, GEO vs SEO, why hire local, one-time vs monthly, measuring success, Bengali-language SEO  
✅ Single source of truth (`faq-data.js` used by both schema and accordion) — no schema/content drift

### Conversational phrasing:
✅ Hero paragraph uses direct, second-person conversational tone ("Your competitors are ranking. You're not.")  
✅ All AEO sections use natural language answers (100-200 words each)  
✅ FAQ answers are detailed, conversational, and include local specifics (BDT pricing, Dhaka neighborhoods)

### AEO/GEO Score: **85/100** — Strong but improvable

**Recommendations:**
- Add an H2: `"How Does Kanok Miah Rank as the Best SEO Expert in Bangladesh?"`
- Add a FAQ question that explicitly uses the target keyword in question text
- Include a "tl;dr" or "Quick Answer" summary box at the top of each AEO section (Google AI Overviews favor concise, structured answers)
- Add entity-rich lists (location names, service names, certifications) within AEO answer paragraphs

---

## 8. Content Gap Analysis

### AEO Section Review:

| Section | Target Keyword in Content? | Effectiveness for AEO |
|---------|---------------------------|----------------------|
| "What SEO Services Does Kanok Miah Offer in Dhaka?" | ✅ "best SEO expert in Dhaka" | ⭐⭐⭐⭐ — Lists all services, location-specific |
| "What Makes Kanok Miah the Best SEO Expert in Dhaka?" | ✅ "Best SEO Expert in Dhaka" in H2 | ⭐⭐⭐⭐⭐ — Perfect keyword placement, detailed bullet points |
| "How Long Does SEO Take to Show Results in Dhaka?" | ✅ "best SEO expert in Dhaka" | ⭐⭐⭐⭐ — Specific timeline, location |
| "How Much Does SEO Cost in Bangladesh?" | ⚠️ "SEO expert in Dhaka" (not Bangladesh) | ⭐⭐⭐ — Missing exact Bangladesh keyword in content |
| "How Can I Hire the Best SEO Expert in Dhaka?" | ✅ Both keywords in content | ⭐⭐⭐⭐⭐ — Both target keywords, clear 3-step process |

### Missing Content Opportunities:

| Gap | Severity | Suggestion |
|-----|----------|------------|
| No standalone "Best SEO Expert in Bangladesh" in title | 🔴 High | Add to title tag |
| No standalone "Best SEO Expert in Bangladesh" in H1 | 🔴 High | Add to H1 or use "Best SEO Expert in Dhaka & Bangladesh" |
| "Best SEO Expert in Bangladesh" not in meta description | 🟡 Medium | Add to meta description |
| Schema items lack target keywords as formal names | 🟡 Medium | Add `alternateName` or keyword-rich descriptions |
| No blog link from homepage to "best SEO expert" articles | 🟢 Low | Add a "Read my SEO insights" link in the about section |
| Bengali section (line 518) doesn't translate the target keywords | 🟢 Low | Add Bengali translation: "ঢাকা ও বাংলাদেশের সেরা SEO বিশেষজ্ঞ" |
| No testimonial quote containing target keyword | 🟢 Low | Ask clients to use "best SEO expert in Dhaka" in reviews |

---

## 9. Summary Scorecard

| # | Check | Status | Score |
|---|-------|--------|-------|
| 1 | Title contains "Best SEO Expert in Dhaka" | ✅ | 10/10 |
| 1b | Title contains "Best SEO Expert in Bangladesh" | ❌ | 0/10 |
| 2 | H1 contains "Best SEO Expert in Dhaka" | ✅ | 10/10 |
| 2b | H1 contains "Best SEO Expert in Bangladesh" | ❌ | 0/10 |
| 3 | Meta description contains target keywords | ⚠️ Partial | 5/10 |
| 4 | First 200 words mention Dhaka/Bangladesh SEO | ✅ | 10/10 |
| 5 | Schema includes target keywords | ❌ | 0/10 |
| 6 | Internal links to services + /locations/dhaka | ✅ | 10/10 |
| 7a | Question-based AEO headings (5 found) | ✅ | 10/10 |
| 7b | FAQ schema present with Dhaka/Bangladesh Qs | ✅ | 10/10 |
| 7c | Conversational phrasing used | ✅ | 10/10 |
| 8 | Content covers both keywords meaningfully | ✅ | 8/10 |

### Overall Score: **72/110** (~65%)

---

## 10. Priority Action Items

### 🔴 Critical (fix ASAP):
1. **Add "Best SEO Expert in Bangladesh" to the title tag** — modify `page.js` metadata.title or restructure layout/page title relationship
2. **Add "Best SEO Expert in Bangladesh" to the H1** — change from "Best SEO Expert in Dhaka, Bangladesh" to "Best SEO Expert in Dhaka & Bangladesh" or use a two-line H1
3. **Add both target keywords to schema descriptions** — especially `OrganizationSchema`, `LocalBusinessSchema`, `WebSiteSchema`, and `AggregateRatingSchema`

### 🟡 Important (fix this week):
4. **Update meta description** to include "Best SEO Expert in Bangladesh" as an exact phrase
5. **Add a FAQ question** that uses the target keyword: "Why choose Kanok Miah as the best SEO expert in Bangladesh?"
6. **Update BreadcrumbSchema** item name from "SEO Expert Dhaka" to "Best SEO Expert in Dhaka"

### 🟢 Nice to have:
7. Add Bengali translation of target keywords in the বাংলা section
8. Add a dedicated testiominal/expertise box highlighting "Best SEO Expert in Bangladesh" credential
9. Consider adding a `<link rel="alternate" hreflang="bn" />` for Bengali version

---

## 11. Files to Modify

| File | Line(s) | Change |
|------|---------|--------|
| `src/app/page.js` | 12 | `title: "Best SEO Expert in Dhaka & Bangladesh \| Kanok Miah"` |
| `src/app/page.js` | 13-14 | Update description to include "Best SEO Expert in Bangladesh" as exact phrase |
| `src/app/page.js` | 115-118 | `BreadcrumbSchema` item name → "Best SEO Expert in Dhaka" |
| `src/app/page.js` | 112 | `AggregateRatingSchema` itemName → "Kanok Miah — Best SEO Expert in Dhaka" |
| `src/components/Schema.js` | 7, 11 | `OrganizationSchema` description — add target keyword |
| `src/components/Schema.js` | 64, 69 | `LocalBusinessSchema` name/description — add target keyword |
| `src/components/Schema.js` | 110, 113 | `WebSiteSchema` description — add target keyword |
| `src/components/Schema.js` | 323, 328-329 | `AggregateRatingSchema` default itemName — add target keyword |
| `src/app/HomeClient.js` | 91-94 | H1: change to "Best SEO Expert in Dhaka & Bangladesh" or similar |
| `src/app/faq-data.js` | ~54 | Add a FAQ with explicit target keyword in question |

---

*Audit generated by Hermes Agent. All findings based on static analysis of source files at `/root/kanok-miahit/`.*
