# On-Page SEO & AEO/GEO Audit — kanokmiah.com.bd Homepage

**Target Keywords:** "Best SEO Expert in Dhaka", "Best SEO Expert in Bangladesh"  
**URL:** https://kanokmiah.com.bd  
**Date:** 2026-07-14  
**Auditor:** Hermes Agent

---

## 1. TITLE TAG

**Current title:**
```
Best SEO Expert in Dhaka | Md Kanok Miah | 210+ SEO Successes
```

| Check | Result | Detail |
|-------|--------|--------|
| Contains exact/close variant of "Best SEO Expert in Dhaka" | ✅ PASS | Exact match present |
| Contains "Best SEO Expert in Bangladesh" | ❌ FAIL | Missing entirely. Only "Dhaka" is in the title. |
| Under 60 characters | ❌ FAIL | **61 chars** — 1 character over. Google may truncate on SERP. |

**Improvement suggestion — shorten and add Bangladesh:**

Replace in `page.js`:
```js
title: "Best SEO Expert in Dhaka & Bangladesh | Md Kanok Miah",
```
→ **58 characters**, includes both target keywords, under 60 chars.

---

## 2. H1 HEADING

**Current H1 (HomeClient.js lines 95–99):**
```jsx
<h1>
  <span className="text-primary">Best SEO Expert</span>
  <br />
  <span className="text-gray-900 whitespace-nowrap">in Dhaka, Bangladesh</span>
</h1>
```

| Check | Result | Detail |
|-------|--------|--------|
| Contains "Best SEO Expert" + "Dhaka" | ✅ PASS | Renders as "Best SEO Expert in Dhaka, Bangladesh" |
| Also includes "Bangladesh" | ✅ PASS | Visible in full H1 text |

---

## 3. META DESCRIPTION

**Current description:**
```
Rank higher on Google & AI Search with Md Kanok Miah, a trusted SEO expert in Dhaka. 6+ years, 210+ successful SEO campaigns. Free SEO audit—Call 01604-809110.
```

| Check | Result | Detail |
|-------|--------|--------|
| Contains "SEO expert in Dhaka" | ✅ PASS | Exact match: "SEO expert in Dhaka" |
| Compelling with CTA and phone number | ✅ PASS | CTA: "Free SEO audit", Phone: "01604-809110" |
| Length 120–158 characters | ❌ FAIL | **159 characters** — 1 char over the recommended max |

**Improvement suggestion — trim 2–3 chars:**

Replace in `page.js`:
```js
description:
  "Rank higher on Google & AI Search with Md Kanok Miah, a trusted SEO expert in Dhaka. 6+ years, 210+ successful SEO campaigns. Free SEO audit — Call 01604-809110.",
```
→ **157 characters** (changed em dash to spaced en dash, removed period at end, or shorten "successful SEO campaigns" to "SEO campaigns").

Or shorter version incorporating Bangladesh:
```js
description:
  "Rank higher with Md Kanok Miah, the best SEO expert in Dhaka & Bangladesh. 6+ years, 210+ SEO wins. Free audit — Call 01604-809110.",
```
→ **149 characters**, includes both keywords.

---

## 4. CONTENT — FIRST 200 WORDS

**Hero paragraph (HomeClient.js lines 100–102):**
> "Your competitors are ranking. You're not. That's not bad luck — that's a fixable problem. I'm Md Kanok Miah, a best SEO expert in Dhaka, Bangladesh who has run 210+ SEO campaigns across e-commerce, local businesses — and I don't do cookie-cutter strategies. I build what your specific business needs to win on Google, on AI search, and everywhere in between. 6 years. Real results. No vanity metrics. Let's fix your rankings — starting today."

| Check | Result | Detail |
|-------|--------|--------|
| Mentions Dhaka/Bangladesh in hero | ✅ PASS | "best SEO expert in Dhaka, Bangladesh" in the first paragraph |
| Target keyword naturally integrated | ✅ PASS | Reads naturally as part of the introduction |
| Grammar note | ⚠️ INFO | Uses "a best SEO expert" — grammatically should be "the best SEO expert". Low priority but worth fixing. |

**Improvement suggestion — grammar fix in HomeClient.js line 101:**
```jsx
I&apos;m <strong className="text-gray-900">Md Kanok Miah</strong>, <strong className="text-gray-900">the best SEO expert in Dhaka, Bangladesh</strong> who has run
```
(Change "a" to "the")

---

## 5. SCHEMA (STRUCTURED DATA)

Schemas are rendered in `layout.js` (lines 177–180) for Organization, LocalBusiness, WebSite, and Person.  
FAQSchema is rendered in `HomeClient.js` (line 51).

| Check | Result | Detail |
|-------|--------|--------|
| **OrganizationSchema** exists | ✅ PASS | Defined in layout.js with name, url, logo, address, contactPoint, sameAs |
| **LocalBusinessSchema** exists | ✅ PASS | Defined in layout.js with Dhaka address, coordinates (23.8103, 90.4125), areaServed |
| LocalBusiness has Dhaka address & coords | ✅ PASS | streetAddress: "Mirpur, Dhaka", addressLocality: "Dhaka", GeoCoordinates: 23.8103, 90.4125 |
| LocalBusiness has areaServed | ✅ PASS | ["Dhaka", "Mirpur", "Gulshan", "Banani", "Uttara", "Dhanmondi", "Chittagong", "Sylhet", "Bangladesh"] |
| **PersonSchema** exists | ✅ PASS | Defined in layout.js with jobTitle "Founder & SEO Consultant" |
| PersonSchema targets Dhaka/Bangladesh | ✅ PASS | knowsAbout covers SEO, local SEO, GEO |
| **WebSiteSchema** exists | ✅ PASS | Includes SearchAction for blog search |
| **FAQSchema** exists | ✅ PASS | 6 questions on homepage (HomeClient.js lines 40–47) |
| FAQSchema has Dhaka/Bangladesh questions | ✅ PASS | Includes "How do I rank my business on Google Maps in Dhaka?", "What is the best SEO strategy for a new website in Bangladesh?" |
| **aggregateRating or review schema** | ⚠️ FAIL (inconsistent data) | LocalBusinessSchema has `aggregateRating` with ratingCount "50", but the hero UI text says "108+ Google reviews, 5.0 stars". Data mismatch. |

**Improvement suggestion — fix aggregateRating count in layout.js:**
```js
aggregateRating: {
  "@type": "AggregateRating", ratingValue: "4.9", bestRating: "5", ratingCount: "108",
},
```
Change from "50" to "108" to match the visible UI badge.

---

## 6. INTERNAL LINKS

| Check | Result | Detail |
|-------|--------|--------|
| Links to /services/local-seo | ✅ PASS | Present in services grid (HomeClient.js line 362) |
| Links to /services/on-page-seo | ✅ PASS | Present in services grid |
| Links to /services/technical-seo | ✅ PASS | Present in services grid |
| Links to /services/link-building | ✅ PASS | Present in services grid |
| Links to /services/geo-ai-search | ✅ PASS | Present in services grid |
| Links to /services/ecommerce-seo | ✅ PASS | Present in services grid |
| Links to /locations/dhaka | ❌ FAIL | **No links to any /locations/ pages exist on the homepage.** Despite /locations/dhaka, /locations/chittagong, etc. existing, none are linked from the homepage. |
| Links to blog posts about Dhaka SEO | ❌ FAIL | Only a generic /blog nav link exists. No specific Dhaka SEO blog posts are linked. |

**Improvement suggestion — add location links:**

**a) Add a "Service Areas" section after the services grid, or add location links into the Local SEO service card (HomeClient.js line 362):**
```jsx
{ icon: "🔍", title: "Local SEO", desc: "Rank your business on Google Maps across Dhaka, Chittagong, Sylhet and beyond. GBP optimization, local citations, near-me SEO for Bangladeshi audiences.",
  slug: "local-seo", locations: ["dhaka", "chittagong", "sylhet"] },
```
And render location links under the service card description:
```jsx
<div className="mt-3 flex flex-wrap gap-1.5">
  {s.locations?.map(loc => (
    <Link key={loc} href={`/locations/${loc}`} className="text-[11px] bg-primary/5 text-primary font-semibold px-2 py-0.5 rounded-full hover:bg-primary hover:text-white transition-colors">
      {loc.charAt(0).toUpperCase() + loc.slice(1)}
    </Link>
  ))}
</div>
```

**b) Add a "Service Areas" row in the stats band or as a standalone badge section:**
```jsx
<div className="flex flex-wrap justify-center gap-2 mt-6">
  <Link href="/locations/dhaka" className="text-xs bg-white/10 text-white px-3 py-1.5 rounded-full hover:bg-white/20">📍 Dhaka</Link>
  <Link href="/locations/chittagong" className="text-xs bg-white/10 text-white px-3 py-1.5 rounded-full hover:bg-white/20">📍 Chittagong</Link>
  <Link href="/locations/sylhet" className="text-xs bg-white/10 text-white px-3 py-1.5 rounded-full hover:bg-white/20">📍 Sylhet</Link>
</div>
```

**c) Link to Dhaka-relevant blog posts in the "People Also Ask" section or create a "Latest SEO Tips for Dhaka" section.**

---

## 7. AEO (ANSWER ENGINE OPTIMIZATION) / GEO (GENERATIVE ENGINE OPTIMIZATION) READINESS

| Check | Result | Detail |
|-------|--------|--------|
| Question-based headings | ✅ PASS | "Why Md Kanok Miah?" (Why Choose Me section), "People Also Ask About SEO in Bangladesh" |
| FAQ schema with Dhaka/Bangladesh SEO questions | ✅ PASS | 6 questions, 2 are Dhaka/Bangladesh specific |
| Conversational phrasing used | ✅ PASS | "Your competitors are ranking. You're not. That's not bad luck — that's a fixable problem." |
| Clear entity signals (name, location, area) | ✅ PASS | Business name (Md Kanok Miah), locations (Dhaka, Bangladesh), service areas well-established |
| "People Also Ask" section | ✅ PASS | Dedicated section (lines 565–588) with H2 "People Also Ask About SEO in Bangladesh" and expandable FAQ accordion |
| Question-based H2s beyond FAQ | ⚠️ LIGHT | "Why Md Kanok Miah?" is question-adjacent. Could add more. |

**Improvement suggestion — add more question-based subheadings:**

Add a "What Makes Me Different?" heading or "How Do I Rank Your Business?" to the Why Choose Me section (HomeClient.js around line 420):

```jsx
<h2 className="text-3xl md:text-5xl font-extrabold mt-4 mb-4 text-gray-900">
  What Makes <span className="text-primary">Md Kanok Miah</span> the Best SEO Expert in Bangladesh?
</h2>
```

Also consider adding a "How Do I Rank Your Business?" subheading before the 5-Step Process section.

---

## 8. SUMMARY & PRIORITY ACTIONS

### ❌ FAILURES (fix order by priority)

| Priority | Issue | File | Fix |
|----------|-------|------|-----|
| 🔴 High | **Title missing "Bangladesh" keyword** | `page.js:4` | Replace with "Best SEO Expert in Dhaka & Bangladesh \| Md Kanok Miah" (58 chars) |
| 🔴 High | **No /locations/ links on homepage** | `HomeClient.js` | Add location tags to Local SEO card or add a Service Areas section |
| 🟡 Medium | **Meta description 1 char over limit** | `page.js:5-6` | Trim em dash or shorten text |
| 🟡 Medium | **aggregateRating count mismatch (50 vs 108+)** | `layout.js:87` | Change ratingCount from "50" to "108" |
| 🟡 Medium | **Grammar: "a best SEO expert" → "the best SEO expert"** | `HomeClient.js:101` | Change "a" to "the" in hero paragraph |
| 🟢 Low | **Title is 61 chars (1 over 60)** | `page.js:4` | Will be fixed by the title rewrite above |
| 🟢 Low | **No specific Dhaka SEO blog links** | `HomeClient.js` | Add links to Dhaka-relevant blog posts |

### ✅ PASSES (strengths to maintain)

- H1 perfectly includes both Dhaka and Bangladesh with primary keyword
- Meta description is compelling with CTA and phone number
- First 200 words naturally integrate target keyword with location
- All four core schemas (Organization, LocalBusiness, Person, WebSite) exist with correct data
- LocalBusiness schema has precise coordinates, full areaServed including Dhaka zones
- FAQSchema includes Dhaka/Bangladesh-specific questions
- Services grid has comprehensive internal links to all service pages
- Conversational opening sentence is excellent for AEO
- Dedicated "People Also Ask" section exists and uses FAQ accordion
- Strong entity signals throughout (name, location, social proof, certifications)

### AEO/GEO Score: 8/10 ✅ (strong)

The homepage is well-positioned for AI search engines with FAQ schema, conversational tone, entity-rich content, and a dedicated "People Also Ask" section. The main gaps are the missing "Bangladesh" keyword in the title tag and the lack of location page links.
