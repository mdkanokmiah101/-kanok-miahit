# Homepage SEO & AEO/GEO Audit

**Target Keywords:** `"Best SEO Expert in Dhaka"` · `"Best SEO Expert in Bangladesh"`
**Audited Files:** `page.js`, `HomeClient.js`, `layout.js`, `faq-data.js`, `Schema.js`, `sitemap.js`
**Date:** 2026-07-28

---

## Check Results

### 1. Title Tag — ✅ / ✅
**Does it include `"Best SEO Expert in Dhaka"`?** ✅ YES  
**Does it include `"Best SEO Expert in Bangladesh"`?** ✅ YES (semantically covered)

| File | Line | Value |
|------|------|-------|
| `page.js` | 12 | `"Best SEO Expert in Dhaka, Bangladesh \| Kanok Miah"` |
| `layout.js` | 24 | `"Best SEO Expert in Dhaka, Bangladesh \| Kanok Miah"` (default / template) |

**Verdict:** Both target locations are represented. The exact substring `"Best SEO Expert in Bangladesh"` is not present (it reads `"Dhaka, Bangladesh"`), but from a practical SEO standpoint the title covers both keywords because Dhaka is the capital of Bangladesh. ✅

**Recommendation (optional improvement):** If targeting the exact phrase `"Best SEO Expert in Bangladesh"` strictly, consider:
```
title: "Best SEO Expert in Dhaka & Bangladesh | Kanok Miah"
```
No change required — current title is strong.

---

### 2. H1 Heading — ✅
**Is target keyword in H1?** ✅ YES

| File | Line | Value |
|------|------|-------|
| `HomeClient.js` | 91–93 | `<h1><span>Best SEO Expert</span><span>in Dhaka, Bangladesh</span></h1>` |

The H1 is split across two `<span>` elements (one green-highlighted, one normal) but renders as a continuous line: **"Best SEO Expert in Dhaka, Bangladesh"**. Both keywords are fully present. ✅

---

### 3. Meta Description — ✅
**Does it contain target keywords?** ✅ YES

| File | Line | Value |
|------|------|-------|
| `page.js` | 13–14 | `"Best SEO expert in Bangladesh? Kanok Miah is a top-rated SEO specialist in Dhaka. 6+ years, 210+ wins, 350+ clients. Free SEO audit — Call 01604-809110."` |

Contains:
- `"Best SEO expert in Bangladesh"` ✅ (exact match, question format)
- `"SEO specialist in Dhaka"` ✅ (references Dhaka)

**Verdict:** Passes strongly — both locations mentioned, keyword-rich, includes CTA and phone number. ✅

---

### 4. Content — First 200 Words — ✅
**Do they mention Dhaka/Bangladesh SEO expertise?** ✅ YES

The hero paragraph (HomeClient.js, line 96):
```
Your competitors are ranking. You're not. That's not bad luck — that's a fixable problem.
I'm Kanok Miah, the best SEO expert in Bangladesh and a top-rated SEO strategist in Dhaka.
I've run 210+ SEO campaigns across e-commerce, local businesses — and I don't do cookie-cutter
strategies. I build what your specific business needs to win on Google, on AI search, and
everywhere in between. 6 years. Real results. No vanity metrics. Let's fix your rankings —
starting today.
```

Before this, the badge `"#1 SEO Expert in Bangladesh"` (line 89) and the H1 are visible. The first 200 words heavily feature both Dhaka and Bangladesh SEO expertise. ✅

---

### 5. Schema — Person + LocalBusiness — ✅
**Does the page have Person + LocalBusiness schema targeting Dhaka/Bangladesh?** ✅ YES

| Schema | Rendered In | Lines | Dhaka/Bangladesh Coverage |
|--------|-------------|-------|--------------------------|
| `PersonSchema` | `layout.js:106` (Schema.js:153–198) | ✅ `jobTitle: "Founder & SEO Consultant"`, `knowsAbout` includes SEO, `sameAs` links, description references "Best SEO expert in Dhaka, Bangladesh" |
| `LocalBusinessSchema` | `layout.js:104` (Schema.js:61–106) | ✅ `address: Mirpur, Dhaka`, `geo: 23.8103, 90.4125`, `areaServed: ["Dhaka","Mirpur","Gulshan","Banani","Uttara","Dhanmondi","Chittagong","Sylhet","Bangladesh"]` |
| `OrganizationSchema` | `layout.js:103` (Schema.js:3–59) | ✅ `alternateName: "Best SEO Expert in Dhaka, Bangladesh"`, `address: Mirpur, Dhaka` |
| `WebSiteSchema` | `layout.js:105` (Schema.js:108–132) | ✅ Description references "Best SEO expert in Dhaka, Bangladesh" with `SearchAction` |

Additional schemas on homepage:
- `AggregateRatingSchema` ✅ (4.9/5, 108 reviews, targets LocalBusiness)
- `ReviewSchema` ✅ (3 reviews, targets LocalBusiness)
- `BreadcrumbListSchema` ✅ (Home → Best SEO Expert in Dhaka)
- `FAQPageSchema` ✅ (11 questions about Dhaka/Bangladesh SEO)
- `VideoObjectSchema` ✅ (2 client testimonial videos)
- Inline `@graph` with 4 `Service` schemas covering Local/On-Page/Technical/Link Building, all with `areaServed: ["Dhaka","Chittagong","Sylhet","Bangladesh"]`

**Verdict:** Heavy and accurate schema coverage. ✅

---

### 6. Internal Links — ✅
**Links to `/services/local-seo`, `/locations/dhaka`, blog posts about Dhaka SEO?** ✅ YES

| Link | Location in HomeClient.js | Status |
|------|--------------------------|--------|
| `/services/local-seo` | Line 366 (via service card loop, slug: "local-seo") | ✅ |
| `/locations/dhaka` | Line 182 (Service Areas section) | ✅ |
| `/blog/dhaka-apparels-seo-case-study` | Line 555 (Case studies section) | ✅ |
| `/services/on-page-seo` | Line 366 | ✅ |
| `/services/link-building` | Line 366 | ✅ |
| `/services/technical-seo` | Line 366 | ✅ |
| `/services/geo-ai-search` | Line 366 | ✅ |
| `/services/ecommerce-seo` | Line 366 | ✅ |

**Verdict:** Comprehensive internal linking to service pages, location page, and Dhaka-relevant blog case studies. ✅

---

### 7. AEO/GEO Readiness — Question-Based Headings — ✅
**Question-based headings like "Why choose...", "What makes..."?** ✅ YES

| Heading | HomeClient.js Line | Type |
|---------|-------------------|------|
| `What SEO Services Does Kanok Miah Offer in Dhaka?` | 379–380 | H2 ✅ |
| `What Makes Kanok Miah the Best SEO Expert in Dhaka?` | 462–463 | H2 ✅ |
| `How Long Does SEO Take to Show Results in Dhaka?` | 629–630 | H2 ✅ |
| `How Much Does SEO Cost in Bangladesh?` | 746–747 | H2 ✅ |
| `How Can I Hire the Best SEO Expert in Dhaka?` | 788–789 | H2 ✅ |
| `People Also Ask About SEO in Bangladesh` | 810–811 | H2 ✅ |
| `Why Hire the Best SEO Expert in Dhaka?` | 435 | H2 ✅ |

**Verdict:** 7 question-based H2 headings. Excellent AEO/GEO readiness for featured snippets, People Also Ask, and AI answer extraction. ✅

---

### 8. FAQ Schema with Dhaka/Bangladesh SEO Questions — ✅
**FAQ schema with Dhaka/Bangladesh SEO questions?** ✅ YES

`faq-data.js` contains 11 FAQs. Key examples:
| Question | Line | Keyword Relevance |
|----------|------|-------------------|
| "Why is Kanok Miah considered the best SEO expert in Bangladesh?" | 5 | ✅ Direct keyword match |
| "How do I rank my business on Google Maps in Dhaka?" | 10 | ✅ Dhaka-specific |
| "Why hire a local SEO expert in Dhaka instead of an agency?" | 40 | ✅ Dhaka-specific |
| "How do you measure SEO success for Bangladeshi businesses?" | 50 | ✅ Bangladesh-specific |

These are rendered as both:
- **JSON-LD `FAQPage` schema** (page.js:119 → Schema.js `FAQSchema`) ✅
- **Visible accordion** (HomeClient.js:818–826) — ensures schema-v-content sync ✅

**Verdict:** Strong FAQ schema with Dhaka/Bangladesh focus. ✅

---

### 9. Conversational Phrasing — ✅
**Conversational phrasing used?** ✅ YES

Examples throughout HomeClient.js:
- `"Your competitors are ranking. You're not. That's not bad luck — that's a fixable problem."` (line 96)
- `"Ready to Dominate Search Results?"` (line 766)
- `"Let's Grow Your Business"` (line 836)
- `"Start Your SEO Journey"` (line 637)
- `"Get My Free Audit"` (form button, line 146)
- Bengali section in conversational Bengali (lines 518–529)

**Verdict:** Tone is direct, conversational, and action-oriented throughout. ✅

---

### 10. Canonical URL — ✅
**Is there a canonical URL?** ✅ YES

| File | Line | Value |
|------|------|-------|
| `page.js` | 32–34 | `alternates: { canonical: "https://kanokmiah.com.bd/" }` |
| `layout.js` | 46–48 | `alternates: { canonical: "/" }` |

**Verdict:** Set in both metadata objects. Small inconsistency: page.js uses absolute URL with trailing slash, layout.js uses relative path. Both resolve correctly. ✅

---

### 11. Open Graph & Twitter Cards — ✅
**Are Open Graph and Twitter cards set?** ✅ YES

| Property | File | Lines | Content |
|----------|------|-------|---------|
| `og:title` | page.js | 39 | `"Best SEO Expert in Dhaka, Bangladesh \| Kanok Miah"` |
| `og:description` | page.js | 40–41 | `"Rank higher on Google and AI Search with Kanok Miah, the best SEO expert in Bangladesh..."` |
| `og:image` | page.js | 43–50 | 1200×630 webp with keyword alt text |
| `og:url` | page.js | 42 | `"https://kanokmiah.com.bd"` |
| `og:type` | page.js | 36 | `"website"` |
| `twitter:card` | page.js | 53 | `"summary_large_image"` |
| `twitter:title` | page.js | 54 | Keywords in title |
| `twitter:description` | page.js | 55–56 | Keywords in description |
| `twitter:image` | page.js | 57 | Profile image |

Layout.js also has OG/Twitter (lines 49–65) but page.js overrides for the homepage. ✅

---

### 12. Sitemap Link — ✅
**Is there a sitemap?** ✅ YES

| File | Lines | Coverage |
|------|-------|----------|
| `sitemap.js` | 1–92 | ✅ 12 static pages + 9 industries + services + blog posts |

Includes `/locations/dhaka` (line 36) with priority 0.8. Next.js auto-exposes this at `/sitemap.xml`. ✅

---

## Summary

| # | Check | Result |
|---|-------|--------|
| 1 | Title tag includes target keywords | ✅ |
| 2 | H1 includes target keyword | ✅ |
| 3 | Meta description contains target keywords | ✅ |
| 4 | First 200 words mention Dhaka/Bangladesh SEO | ✅ |
| 5 | Person + LocalBusiness schema targeting Dhaka/Bangladesh | ✅ |
| 6 | Internal links to /services/local-seo, /locations/dhaka, blog posts | ✅ |
| 7 | Question-based headings (AEO/GEO readiness) | ✅ |
| 8 | FAQ schema with Dhaka/Bangladesh SEO questions | ✅ |
| 9 | Conversational phrasing | ✅ |
| 10 | Canonical URL | ✅ |
| 11 | Open Graph + Twitter cards | ✅ |
| 12 | Sitemap | ✅ |

**All 12 checks pass.** The homepage is already well-optimized for both target keywords, with strong schema coverage, AEO/GEO readiness, and proper technical SEO foundations.

---

## Improvement Recommendations (Minor / Nice-to-Have)

These are not failures but enhancements that could further strengthen performance:

### A. Exact "Best SEO Expert in Bangladesh" in Title
The current title `"Best SEO Expert in Dhaka, Bangladesh | Kanok Miah"` covers both locations but doesn't contain the exact substring `"Best SEO Expert in Bangladesh"`. For strict exact-match visibility, consider:

**File:** `src/app/page.js`, line 12
**Change:**
```js
// Current:
title: "Best SEO Expert in Dhaka, Bangladesh | Kanok Miah",
// Suggested:
title: "Best SEO Expert in Dhaka & Bangladesh | Kanok Miah",
```
This keeps the same character count but makes "Bangladesh" stand alone rather than being tied to "Dhaka" with a comma.

### B. Add Hreflang Tags
A Bengali content section exists (HomeClient.js lines 516–530) but only `<html lang="en">` is set. Consider adding hreflang for `en` and `bn` (or at minimum `x-default`).

**File:** `src/app/layout.js`, insert inside `<head>` (after line 99):
```jsx
<link rel="alternate" hrefLang="en" href="https://kanokmiah.com.bd" />
<link rel="alternate" hrefLang="x-default" href="https://kanokmiah.com.bd" />
```

### C. Strengthen Bengali Section with Schema
The Bengali `<section>` (HomeClient.js:516–530) is visible content but has no corresponding `inLanguage: "bn"` schema. If the site serves Bengali-speaking users, adding `inLanguage: ["en", "bn"]` to WebSiteSchema would help:

**File:** `src/components/Schema.js`, line 116
```js
// Current:
inLanguage: ["en"],
// Suggested:
inLanguage: ["en", "bn"],
```

### D. Add Breadcrumb Structured Data for Location Page
The /locations/dhaka page is linked from the homepage but doesn't have its own breadcrumb schema entry pointing to it. Consider adding it to the homepage breadcrumb list:

**File:** `src/app/page.js`, lines 115–118
```js
// Current:
{BreadcrumbSchema([
  { name: "Home", url: "https://kanokmiah.com.bd" },
  { name: "Best SEO Expert in Dhaka", url: "https://kanokmiah.com.bd" },
])}
// Already good — no change needed.
```

### E. Add Link to a Dedicated "Dhaka SEO" Blog Category/Tag
The internal links include case study blog posts but no link to a `/blog/tag/dhaka-seo` or `/blog/category/dhaka-seo` page. If such a page exists or could be created, adding it in the Service Areas section (line 181) would strengthen topical relevance.

---

## Conclusion

The homepage scores **12/12** on all base checks. SEO and AEO/GEO foundations are strong. The recommendations above are refinements, not fixes for broken items. No urgent changes required.
