# Content Framework Enforcement Report
**Site:** kanokmiah.com.bd | **Date:** 2026-07-22 | **Type:** Cron Audit

## Changes Detected
✅ 3 commits in last 48 hours touching `src/app/blog/data.js`:
1. **5cbb3f7** — auto-fix: blog heading/HTML tags cleanup (3 lines changed — `&lt;` → `<` in code blocks)
2. **cad9c069** — auto-fix: blog heading/HTML tags cleanup (707 blank-line deletions across entire file)
3. **001ef98** — fix: internal linking audit (61 insertions, 25 deletions across 22 posts — added homepage links, removed 7 duplicate links)

## Summary Dashboard

| Metric | Value |
|--------|-------|
| Total posts in data.js | 128 |
| Posts modified (substantive) | 22 |
| Posts examined in detail | 18 |
| Posts with all checks passing | **0** |
| Posts passing 5/6 checks | 2 |
| Posts passing 4/6 checks | 7 |
| Posts passing 3/6 checks | 6 |
| Posts passing 2/6 checks | 3 |

### Pass Rate by Check
| Check | ✅ Pass | ❌ Fail | Pass Rate |
|-------|--------|--------|-----------|
| A. TF-IDF Coverage | 14 | 4 | 78% |
| B. Entity Coverage | 15 | 3 | 83% |
| C. Pillar Link | 4 | 14 | 22% |
| D. AEO/GEO | 4 | 14 | 22% |
| E. Internal Links | 18 | 0 | 100% |
| F. Schema Ready | 18 | 0 | 100% |

## Per-Post Findings

### 1. `why-md-kanok-miah-is-the-best-seo-expert-in-dhaka-bangladesh`
| Check | Status | Detail |
|-------|--------|--------|
| TF-IDF: `Kanok Miah` | ✅ | 8 occurrences |
| Entities | ✅ | Dhaka, Bangladesh, SEO, Case Study |
| Pillar Link | ❌ | No link to `/blog/complete-seo-guide-bangladesh-businesses-2026` |
| AEO/GEO | ✅ | 4 question headings |
| Internal Links | ✅ | 15 total (4 blog, 7 services, 1 locations) |
| Schema Ready | ✅ | Title, excerpt, date, author all set |
> **Fix:** Add pillar link to complete SEO guide

### 2. `locksmith-dundee-seo-case-study`
| Check | Status | Detail |
|-------|--------|--------|
| TF-IDF: `Locksmith Dundee` | ✅ | 27 occurrences |
| Entities | ✅ | Dhaka, Bangladesh, SEO, Local SEO |
| Pillar Link | ❌ | No link to `/services/local-seo-dhaka` |
| AEO/GEO | ❌ | 0 question headings (uses "The Challenge:", "The Solution:" style) |
| Internal Links | ✅ | 3 total |
| Schema Ready | ✅ | All fields set |
> **Fix:** Add pillar link to local SEO services; add FAQ section with 2+ question headings

### 3. `landlord-certificates-seo-case-study`
| Check | Status | Detail |
|-------|--------|--------|
| TF-IDF: `All Landlord Certificates` | ❌ | ~2 occurrences |
| Entities | ✅ | Dhaka, Bangladesh, SEO, Local SEO |
| Pillar Link | ❌ | No link to local SEO service page |
| AEO/GEO | ❌ | 0 question headings |
| Internal Links | ✅ | 3 total |
| Schema Ready | ✅ | All fields set |
> **Fix:** Increase brand keyword usage; add pillar link; add 2+ question headings

### 4. `das-taxis-scotland-seo-case-study`
| Check | Status | Detail |
|-------|--------|--------|
| TF-IDF: `Das Taxis Scotland` | ❌ | 3 occurrences |
| Entities | ✅ | Dhaka, Bangladesh, SEO, Local SEO |
| Pillar Link | ❌ | No link to `/services/local-seo-dhaka` |
| AEO/GEO | ❌ | 0 question headings |
| Internal Links | ✅ | 3 total |
| Schema Ready | ✅ | All fields set |
> **Fix:** Increase brand keyword to ≥5; add pillar link; add 2+ question headings

### 5. `morethanpanel-seo-case-study`
| Check | Status | Detail |
|-------|--------|--------|
| TF-IDF: `MoreThanPanel` | ❌ | 4 occurrences |
| Entities | ✅ | Dhaka, Bangladesh, SEO, Content Marketing |
| Pillar Link | ❌ | No link to `/services/semantic-seo` |
| AEO/GEO | ❌ | 0 question headings |
| Internal Links | ✅ | 4 total |
| Schema Ready | ✅ | All fields set |
> **Fix:** Increase brand keyword to ≥5; add content marketing pillar link; add 2+ question headings

### 6. `smmgen-seo-case-study`
| Check | Status | Detail |
|-------|--------|--------|
| TF-IDF: `SMMGen` | ✅ | 5 occurrences |
| Entities | ✅ | Dhaka, Bangladesh, SEO, Technical SEO |
| Pillar Link | ✅ | Links to technical SEO |
| AEO/GEO | ❌ | 0 question headings |
| Internal Links | ✅ | 4 total |
| Schema Ready | ✅ | All fields set |
> **Fix:** Add 2+ question headings (FAQ-style section)

### 7. `smmsun-seo-case-study`
| Check | Status | Detail |
|-------|--------|--------|
| TF-IDF: `SMMSun` | ❌ | 4 occurrences |
| Entities | ✅ | Dhaka, Bangladesh, SEO, Case Study |
| Pillar Link | ❌ | No link to pillar |
| AEO/GEO | ❌ | 0 question headings |
| Internal Links | ✅ | 6 total |
| Schema Ready | ✅ | All fields set |
> **Fix:** Increase brand keyword; add pillar link; add 2+ question headings

### 8. `mir-cement-seo-case-study`
| Check | Status | Detail |
|-------|--------|--------|
| TF-IDF: `Mir Cement` | ❌ | 3 occurrences |
| Entities | ❌ | Missing: "Case Study" entity in content body |
| Pillar Link | ❌ | No link to pillar |
| AEO/GEO | ❌ | 0 question headings |
| Internal Links | ✅ | 5 total |
| Schema Ready | ✅ | All fields set |
> **Fix:** Increase brand keyword; add "case study" mention in content; add pillar link; add 2+ question headings

### 9. `dhaka-apparels-seo-case-study`
| Check | Status | Detail |
|-------|--------|--------|
| TF-IDF: `Dhaka Apparels` | ❌ | 3 occurrences |
| Entities | ✅ | Dhaka, Bangladesh, SEO, Garments/Textile |
| Pillar Link | ✅ | Links to garments pillar |
| AEO/GEO | ❌ | 0 question headings |
| Internal Links | ✅ | 5 total |
| Schema Ready | ✅ | All fields set |
> **Fix:** Increase brand keyword; add 2+ question headings

### 10. `stealth-windshield-repairs-seo-case-study`
| Check | Status | Detail |
|-------|--------|--------|
| TF-IDF: `Stealth` | ✅ | 5 occurrences |
| Entities | ✅ | Dhaka, Bangladesh, SEO, Local SEO |
| Pillar Link | ❌ | No link to `/services/local-seo-dhaka` |
| AEO/GEO | ❌ | 0 question headings |
| Internal Links | ✅ | 3 total |
| Schema Ready | ✅ | All fields set |
> **Fix:** Add local SEO pillar link; add 2+ question headings

### 11. `hiring-seo-expert-dhaka-better-roi-than-paid-ads`
| Check | Status | Detail |
|-------|--------|--------|
| TF-IDF: `Hiring` | ❌ | 3 occurrences |
| Entities | ✅ | Dhaka, Bangladesh, SEO |
| Pillar Link | ❌ | No pillar link |
| AEO/GEO | ✅ | 4 question headings |
| Internal Links | ✅ | 3 total |
| Schema Ready | ✅ | All fields set |
> **Fix:** Increase primary keyword density; add pillar link

### 12. `seo-expert-vs-seo-agency-dhaka-which-is-right`
| Check | Status | Detail |
|-------|--------|--------|
| TF-IDF: `SEO Expert` | ✅ | 23 occurrences |
| Entities | ✅ | Dhaka, Bangladesh, SEO |
| Pillar Link | ❌ | No pillar link |
| AEO/GEO | ✅ | 6 question headings |
| Internal Links | ✅ | 8 total |
| Schema Ready | ✅ | All fields set |
> **Fix:** Add pillar link to complete SEO guide

### 13. `top-10-seo-mistakes-dhaka-businesses-fix`
| Check | Status | Detail |
|-------|--------|--------|
| TF-IDF: `Top` | ✅ | 7 occurrences |
| Entities | ✅ | Dhaka, Bangladesh, SEO |
| Pillar Link | ❌ | No pillar link |
| AEO/GEO | ❌ | 0 question headings (uses list format, not H2/H3 questions) |
| Internal Links | ✅ | 7 total |
| Schema Ready | ✅ | All fields set |
> **Fix:** Add pillar link; add question-based subheadings

### 14. `seo-case-study-dhaka-businesses-increased-organic-traffic`
| Check | Status | Detail |
|-------|--------|--------|
| TF-IDF: `SEO Case Study` | ✅ | 7 occurrences |
| Entities | ✅ | Dhaka, Bangladesh, SEO, Case Study |
| Pillar Link | ❌ | No pillar link |
| AEO/GEO | ✅ | 4 question headings |
| Internal Links | ✅ | 3 total |
| Schema Ready | ✅ | All fields set |
> **Fix:** Add pillar link

### 15. `watchzonebd-seo-case-study`
| Check | Status | Detail |
|-------|--------|--------|
| TF-IDF: `WatchZoneBD` | ✅ | 14 occurrences |
| Entities | ❌ | Missing: "Case Study" in content body |
| Pillar Link | ✅ | Links to technical SEO pillar |
| AEO/GEO | ❌ | 0 question headings |
| Internal Links | ✅ | 5 total |
| Schema Ready | ✅ | All fields set |
> **Fix:** Add "case study" reference in content; add 2+ question headings

### 16. `seo-featured-snippet-bangladesh` (Bengali)
| Check | Status | Detail |
|-------|--------|--------|
| TF-IDF: `ফিচার্ড` | ✅ | 53 occurrences |
| Entities | ✅ | Dhaka, Bangladesh, SEO |
| Pillar Link | ❌ | No link to pillar |
| AEO/GEO | ❌ | 1 question heading (needs ≥2) |
| Internal Links | ✅ | 19 total |
| Schema Ready | ✅ | All fields set |
> **Fix:** Add pillar link; add 1 more Bengali question heading

### 17. `seo-knowledge-panel-bangladesh` (Bengali)
| Check | Status | Detail |
|-------|--------|--------|
| TF-IDF: `নলেজ` | ✅ | 64 occurrences |
| Entities | ✅ | Dhaka, Bangladesh, SEO |
| Pillar Link | ❌ | No link to pillar |
| AEO/GEO | ❌ | 1 question heading (needs ≥2) |
| Internal Links | ✅ | 18 total |
| Schema Ready | ✅ | All fields set |
> **Fix:** Add pillar link; add 1 more Bengali question heading

### 18. `seo-json-ld-schema-bangladesh` (Bengali)
| Check | Status | Detail |
|-------|--------|--------|
| TF-IDF: `JSON` | ✅ | 72 occurrences |
| Entities | ✅ | Dhaka, Bangladesh |
| Pillar Link | ⚠️ | Schema-specific post, no pillar match |
| AEO/GEO | ❌ | 1 question heading (needs ≥2) |
| Internal Links | ✅ | 19 total |
| Schema Ready | ✅ | All fields set |
> **Fix:** Add 1 more Bengali question heading

## Top Priority Issues

### 🚨 Critical (affects 10+ posts)
1. **Pillar-Cluster links missing** (14/18 posts) — Posts don't link back to their pillar topic page. Fix: add `[complete SEO guide](/blog/complete-seo-guide-bangladesh-businesses-2026)` or service/industry pillar link in content.
2. **AEO/GEO question headings insufficient** (14/18 posts) — Most posts lack ≥2 question-based H2/H3s. Fix: add FAQ sections and/or rewrite subheadings as questions (e.g. "What is X?" "How does Y work?").

### ⚠️ Moderate (affects 3-5 posts)
3. **TF-IDF keyword density low** (4/18 posts) — Brand names used only 2-4 times. Fix: naturally increase to ≥5 mentions.
4. **Entity coverage gaps** (3/18 posts) — "Case Study" entity missing in content body of some case study posts.

### ✅ Good (no action needed)
5. **Internal linking** — All 18 posts pass (≥3 internal links). The recent audit added 18 homepage references.
6. **Schema readiness** — All posts have title, excerpt, date, author — ArticleSchema requirements met.

## Internal Linking Audit Results
The commit 001ef98 was largely positive:
- ✅ Added 18 homepage/internal links across posts
- ✅ Removed 7 duplicate/broken links
- ✅ Added "Looking for the [SEO consultant](/)" CTA to 15+ posts
- ⚠️ Some links point to `/` (homepage) rather than specific content pages — partial improvement

## Action Items
1. **Pillar linking** — Create a cron job that adds pillar page links to posts based on their tags
2. **AEO/GEO pass** — Add a script to insert FAQ sections with question headings in posts that have <2
3. **TF-IDF review** — Fix 4 posts with thin keyword usage (Das Taxis, Mir Cement, Dhaka Apparels, MoreThanPanel)
4. **Bengali posts** — Add one more question heading each to `seo-featured-snippet`, `seo-knowledge-panel`, `seo-json-ld-schema`
