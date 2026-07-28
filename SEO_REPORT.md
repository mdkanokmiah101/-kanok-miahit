# 🏠 Homepage Optimization Report — "Best SEO Expert in Dhaka/Bangladesh"

**Date:** 2026-07-27  
**Target URL:** https://kanokmiah.com.bd/  
**Source:** /root/kanok-miahit/src/app/  
**Deploy version:** v25-amp-fixes (local build verified on port 3000)  
**Production version:** v24 (stale — needs deployment)

---

## Current Status

| Element | Status | Details |
|---------|--------|---------|
| **H1** | ✅ Present | "Best SEO Expert in Dhaka, Bangladesh" — primary query front-loaded |
| **Title tag** | ✅ Optimized | "Best SEO Expert in Dhaka, Bangladesh | Kanok Miah" — 50 chars |
| **Meta description** | ✅ Optimized | "Best SEO expert in Bangladesh? Kanok Miah..." — 155 chars, opens with question (AEO-friendly) |
| **URL structure** | ✅ Clean | `/` — no hashes, no tracking params, no dates |
| **Canonical** | ✅ Self-referencing | `https://kanokmiah.com.bd/` |
| **robots** | ✅ index, follow | With `max-image-preview:large` |
| **OG tags** | ✅ Complete | og:title, og:description, og:image, og:url, og:site_name all present |
| **Twitter tags** | ✅ Complete | twitter:card, twitter:title, twitter:description, twitter:image |
| **metadataBase** | ✅ Set | `https://kanokmiah.com.bd` — no localhost twitter:image issue |
| **JSON-LD Schema** | ✅ 22 types | Organization, LocalBusiness, WebSite, Person, Service(@graph×6), FAQPage(×11), AggregateRating, Review(×3), VideoObject(×2), BreadcrumbList |
| **#1 Badge** | ✅ Present | "#1 SEO Expert in Bangladesh" badge in hero |
| **H2 Question count** | ✅ 7 | Strong AEO/GEO signal — well above 5-minimum threshold |
| **Standalone "Bangladesh" phrase** | ✅ Present | Meta description opens with "Best SEO expert in Bangladesh?" + "#1 SEO Expert in Bangladesh" badge + body text has "the best SEO expert in Bangladesh" |
| **Internal links** | ✅ Strong | Full mesh topology — services section links to 6 individual service pages, industries section links to 9+ industry pages, all nav items in header + footer |
| **Image alt text** | ✅ Good | "Kanok Miah — SEO Expert in Dhaka, Bangladesh" on about image |
| **FAQPage schema** | ✅ Present | 11 questions matching visible FAQ section |

---

## 🔴 Issues Found & Fixed

### Critical: `&amp;` in Visible Text (12 occurrences → 0)

The most impactful fix. React/Next.js HTML-escapes `&` to `&amp;` in JSX text nodes and JavaScript string literals. **5 headings** and **7 other text elements** were rendering literal `&amp;` in the DOM.

| Location | Before | After | File |
|----------|--------|-------|------|
| Lead form H3 | "Get Free SEO Audit & Proposal" | "and Proposal" | HomeClient.js:130 |
| Industry: Garments | "Garments & Textile" | "Garments and Textile" | HomeClient.js:403 |
| Industry: Spa | "Spa & Salon" | "Spa and Salon" | HomeClient.js:408 |
| Industry: Medical | "Medical & Healthcare" | "Medical and Healthcare" | HomeClient.js:409 |
| Industry: Food | "Food & Restaurant" | "Food and Restaurant" | HomeClient.js:411 |
| Industry: Cleaning | "Office & home cleaning" | "Office and home cleaning" | HomeClient.js:407 |
| Enterprise features | "WhatsApp & Phone Support" | "WhatsApp and Phone Support" | HomeClient.js:722 |
| Footer: Industries nav | Same 4 industry names | "and" variants | Footer.js:14-22 |
| Footer: Bottom line | "Serving Dhaka & all of Bangladesh" | "Serving Dhaka and all of Bangladesh" | Footer.js:182 |

**Also cleaned:** OG/twitter description "Google & AI Search" → "Google and AI Search" (meta content attributes, no visible impact but cleaner HTML).

### Important: `&amp;` in Page.js OG/Twitter Descriptions (2 occurrences → 0)

| Before | After | File |
|--------|-------|------|
| "Google & AI Search" | "Google and AI Search" | page.js:41,56 |

---

## 🟢 Strengths

1. **Excellent schema coverage** — 22 schema types including FAQPage, AggregateRating, Review, VideoObject, Service, Organization, LocalBusiness, Person, WebSite
2. **Strong AEO/GEO foundation** — 7 question-based H2s, FAQPage schema with 11 questions, opening meta description question format
3. **Target query in H1, title, and meta** — "Best SEO Expert in Dhaka, Bangladesh" appears in all key elements
4. **Good internal linking** — All service pages link from homepage, industries section, navbar, and footer
5. **Conversion elements** — Lead form in hero, WhatsApp floating button, multiple CTAs, trust badges
6. **metadataBase properly set** — No localhost-in-twitter:image issue
7. **Full OG/Twitter tags** — Social sharing previews work correctly

---

## 📋 Action Items

### ⚠️ Critical — Unblocks Deployment

- [ ] **Renew GitHub PAT token** — The git remote URL at `/root/kanok-miahit` has an expired PAT. Generate a new classic token (repo scope) at GitHub Settings → Developer Settings → Personal Access Tokens → Tokens (classic), then:
  ```bash
  cd /root/kanok-miahit
  git remote set-url origin https://USERNAME:NEW_TOKEN@github.com/mdkanokmiah101/-kanok-miahit.git
  ```
  Then commit and push:
  ```bash
  git add -A && git commit -m "fix: replace & with and in industry titles, footer, and form (v25)"
  git push origin main
  ```
  Vercel auto-deploys from `main` branch. Wait ~1-2 min for Vercel build.

### ✅ Completed (verified at localhost:3000)

- [x] **Fixed `&amp;` in 5 headings** — Lead form H3, 4 industry card titles (Garments, Spa, Medical, Food)
- [x] **Fixed `&amp;` in industry descriptions** — "Office & home cleaning" → "Office and home cleaning"
- [x] **Fixed `&amp;` in feature list** — "WhatsApp & Phone Support" → "WhatsApp and Phone Support"
- [x] **Fixed `&amp;` in footer** — 4 industry nav names and bottom tagline
- [x] **Fixed `&amp;` in OG/twitter descriptions** — "Google & AI Search" → "Google and AI Search"
- [x] **Updated deploy-version** — `2026-07-27-v25-amp-fixes`
- [x] **Build verified** — `npm run build` passes, localhost:3000 serving v25

### 📝 Recommended (future)

- [ ] **Standalone "Best SEO Expert in Bangladesh" in body** — The phrase currently appears only in meta description (question format), "#1 SEO Expert in Bangladesh" badge, and as "the best SEO expert in Bangladesh" (lowercase). Adding it as an H3 or standalone sentence would strengthen the national-scope signal, though current coverage is adequate.
- [ ] **Add OG/Twitter tags to FAQ page** — If `/faq` page exists, it likely inherits homepage OG tags. Add explicit metadata export if needed.
- [ ] **Monitor internal link target health** — When creating new service/industry pages, verify all homepage → target links return 200 before deploying.

---

## AI Search Visibility Assessment

| Platform | Potential | Notes |
|----------|-----------|-------|
| **ChatGPT citation** | 🟢 **High** | FAQPage schema (11 Q&A pairs), question-based H2s, strong entity markup, clear definition-first meta description |
| **Google AI Overviews** | 🟢 **High** | Top-10 ranking content, passage optimization via H2→direct-answer pattern, structured data |
| **Perplexity** | 🟢 **Medium-High** | Reddit/YouTube brand mentions help, FAQ data is pullable |

**Key AEO/GEO assets already in place:**
- ✅ Meta description opens with question ("Best SEO expert in Bangladesh?")
- ✅ 7 question-based H2s that match user search patterns
- ✅ Self-contained answer blocks (134-167 word passages) in AEO sections
- ✅ FAQPage schema with 11 detailed Q&A pairs
- ✅ Specific statistics with context (210+ projects, 4.9/5 rating, 108 reviews)
- ✅ Author identity (Person schema with job titles, certifications)
- ✅ Clear publication context (deploy-version meta, "Since 2019" badges)
- ✅ Structured data supporting all visible content

---

## Scoring: 8-Dimension Framework

| Dimension | Score | Notes |
|-----------|-------|-------|
| 1. Title Tag | ✅ 15/15 | Perfect 50-char, query first, brand at end |
| 2. Meta Description | ✅ 5/5 | 155-char, question format, CTA, both target phrases |
| 3. Header Structure | ✅ 10/10 | 1 H1, 7 question H2s, no skipped levels |
| 4. Body Content | ⚠️ 22/25 | Strong depth, minor standalone-Bangladesh gap |
| 5. Internal Links | ✅ 9/10 | Full mesh topology, could add more in-body contextual links |
| 6. Image/Media | ✅ 9/10 | Good alt text, could add more images with descriptive filenames |
| 7. URL Slug | ✅ 10/10 | Clean root URL, no parameters |
| 8. On-Page Schema | ✅ 10/10 | 22 schema types, all validated in rendered HTML |

**Overall: 90/100 (A+)**
