# BLOG POST AUDIT REPORT
## what-does-seo-expert-do-guide-business-owners

---

## 1. POST METADATA

| Field | Value |
|-------|-------|
| **Title** | What Does an SEO Expert Actually Do? A Complete Guide for Business Owners |
| **Slug** | `what-does-seo-expert-do-guide-business-owners` |
| **Date** | 2026-07-14 |
| **Author** | Kanok Miah |
| **Tags** | SEO Expert Guide, SEO Services, Dhaka SEO, Digital Marketing Bangladesh |
| **Excerpt** | "What does an SEO expert do? Discover the complete guide — daily tasks, weekly activities, GEO/AEO optimization, E-E-A-T framework, and why Dhaka businesses need a professional SEO Specialist in Dhaka for long-term growth." |
| **Word Count** | 4,346 words |
| **Structure** | 10 H2 headings, 28 H3 headings, 38 total headings |
| **Reading Level** | Difficult (College) — Flesch ~39.4 |

---

## 2. TF-IDF ANALYSIS (Top 20 Keywords)

| Keyword | TF-IDF Score |
|---------|-------------|
| frequently | 1.221 |
| asked | 1.221 |
| questions | 0.949 |
| responsibilities | 0.916 |
| misconceptions | 0.916 |
| common | 0.678 |
| core | 0.634 |
| expert | 0.406 |
| bdt | 0.397 |
| keyword | 0.378 |
| content | 0.336 |
| page | 0.323 |
| business | 0.317 |
| geo | 0.314 |
| dhaka | 0.290 |
| search | 0.298 |
| optimization | 0.293 |
| strategy | 0.286 |
| technical | 0.275 |
| google | 0.270 |

**Analysis:** Keywords are well-distributed and relevant to the topic. High TF-IDF for "frequently asked questions" indicates strong FAQ section. "SEO expert", "Dhaka", "GEO", "technical" all align with the post's purpose.

---

## 3. ENTITY EXTRACTION

### Persons
- Kanok Miah ✓

### Organizations (13 unique)
- Google (43x), ChatGPT (2x), Gemini, Perplexity, BD Yellow Pages, BD Trade Info, Bangladesh Chamber of Commerce

### Locations (10+ unique)
- Dhaka (31x), Bangladesh (24x), Bangladeshi (12x), BD (10x), Gulshan (6x), Banani (5x), Dhanmondi (4x), Uttara (2x), Mirpur, Motijheel, Chittagong (mentioned), Sylhet (mentioned)

### Tools & Products (12+ unique)
- Google Search Console (6x), Ahrefs (4x), SEMrush (3x), Screaming Frog (2x), Sitebulb (2x), PageSpeed Insights (2x), Google Analytics (3x), Majestic, AccuRanker, BrightLocal, Whitespark, Google Keyword Planner

### Pricing References
- BDT 15,000 to BDT 2,00,000 ranges

**Analysis:** Very strong entity richness. Excellent coverage of local locations, tools, and pricing context. Demonstrates deep EEAT signals through tool expertise and local knowledge.

---

## 4. PILLAR-CLUSTER ANALYSIS

| Criterion | Result |
|-----------|--------|
| Word count ≥ 1,500 | ✅ 4,346 words |
| H2 sections ≥ 5 | ✅ 10 H2 headings |
| **Classification** | **✅ PILLAR POST** |
| Coverage | Complete guide covering 7 core responsibilities, day-in-life schedule, weekly schedule, GEO/AEO/EEAT, misconceptions, hiring guide, FAQs |

**Assessment:** This is a comprehensive pillar post that thoroughly covers the topic "what does an SEO expert do." It connects well to cluster content via the 3 internal links.

---

## 5. AEO/GEO OPTIMIZATION CHECK

| Check | Status |
|-------|--------|
| FAQ section present | ✅ |
| Question-answer format | ✅ (9 FAQ Q&A pairs in FAQ section) |
| Schema markup mentioned | ✅ |
| GEO mentioned | ✅ (dedicated section) |
| AEO mentioned | ✅ (dedicated section) |
| E-E-A-T mentioned | ✅ (dedicated section) |
| Voice search optimization | ✅ |
| Featured snippet optimization | ✅ |
| Entity-rich content | ✅ |
| Conversational tone | ✅ |
| Structured data mention | ✅ |
| HowTo/FAQ schema mention | ✅ |
| Question-based headings | ✅ |
| **AEO/GEO Score** | **13/13 (100%) — EXCELLENT** |

**Analysis:** The post is exceptionally well-optimized for AEO/GEO. It has a dedicated GEO section, AEO section, and EEAT section. Content is structured in question-answer formats throughout. Ideal for AI-powered search citation.

---

## 6. INTERNAL LINKS ANALYSIS

| Type | Count | Links |
|------|-------|-------|
| **Blog links** | 1 | `/blog/seo-tips-for-business-owners-bd` |
| **Location links** | 1 | `/locations/dhaka` |
| **Homepage link** | 1 | `/` (SEO expert in Dhaka) |
| **Service links** | 0 | — |
| **Industry links** | 0 | — |
| **About / Contact** | 0 | — |
| **Total Internal** | **3** | |
| **External links** | 2 | `kanokmiah.com.bd/contact`, `kanokmiah.com.bd/` |

### ⚠️ CRITICAL ISSUE: Insufficient internal linking
A 4,346-word pillar post should have **15-25+ internal links** to related cluster content. Currently only 3 internal links exist. This post should link to:
- Related service pages: `/services/local-seo`, `/services/technical-seo`, `/services/ecommerce-seo`
- Related blog posts: `/blog/complete-seo-guide-bangladesh-businesses-2026`, `/blog/how-to-choose-right-seo-agency-bangladesh`, `/blog/geo-optimization-prepare-business-ai-search`
- Industry pages: `/industries/food-restaurant`, `/industries/ecommerce`
- About page: `/about`
- Contact page: `/contact`

---

## 7. SCHEMA MARKUP ANALYSIS

**Schema types mentioned in content:**
- Review (6x), FAQ (4x), Organization (2x), LocalBusiness (2x), Article (2x), Product (1x), Service (1x), HowTo (1x)

**Actual schema rendering on the page (from `[slug]/page.js`):**

| Schema Type | Status | Details |
|-------------|--------|---------|
| **BreadcrumbSchema** | ✅ Auto-injected | Home → Blog → Post |
| **ArticleSchema** | ✅ Auto-injected | Uses title, excerpt, date, dateModified, author, publisher |
| **FAQSchema** | ❌ NOT rendered | Conditional on `post.faqs` array — post data does NOT include a `faqs` property |

### ⚠️ ISSUE: FAQSchema not rendering
The post has 9 FAQ questions in its content, but the post object in `data.js` does not include a `faqs` array. The FAQSchema component (`@type: FAQPage`) would add rich results for these FAQs. **Action:** Add a `faqs` property to the post object.

### Schema implementation mentions in content
The post has 5 explicit mentions of schema implementation actions ("implement", "add", "use" schema), correctly guiding readers on structured data.

---

## 8. OVERALL QUALITY SCORES

| Dimension | Score | Notes |
|-----------|-------|-------|
| 📏 Content Depth | **10.0/10** | 4,346 words, comprehensive topic coverage |
| 🏗️ Structure | **10.0/10** | Excellent H2/H3 hierarchy with clear sections |
| 🔗 Internal Links | **1.6/10** | Only 3 links — needs improvement |
| 🤖 AEO/GEO Optimization | **10.0/10** | Perfect score — all indicators present |
| 🏛️ Entity Richness | **10.0/10** | 35+ unique entities across 5 categories |
| **⭐ OVERALL** | **8.3/10** | **Grade: EXCELLENT** |

---

## 9. RECOMMENDATIONS

### High Priority
1. **Add `faqs` array to post data** to enable FAQSchema rich results — the content already has 9 FAQ items ready to extract
2. **Significantly increase internal linking** — add 15-25 internal links to service pages, related blog posts, industry pages, and the about/contact pages

### Medium Priority
3. **Add `dateModified` field** to the post object for better freshness signals
4. **Add a table of contents** at the beginning for improved navigation and featured snippet targeting

### Low Priority
5. The post could link out more specifically — e.g., when discussing "local citation building on Bangladeshi directories," link to the citation guide

---

## 10. GIT HISTORY (Last 48 Hours)

The file `src/app/blog/data.js` was last modified in commit `0cd493b` (2026-07-27) — within the last 48 hours. This commit's message was "fix: internal linking audit - remove duplicates, add homepage links" — it added homepage links across several posts but did not modify the `what-does-seo-expert-do` post specifically.

---

*Report generated by Hermes Agent audit script on 2026-07-28*
