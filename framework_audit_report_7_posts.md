# Framework Audit Report — 7 Posts

**Date:** 2026-07-20  
**Auditor:** Hermes Agent (cron job)  
**Method:** Read each post from `data.js` (restored from `.bak`), analyzed content, tags, schema, internal links  
**File:** `/root/kanok-miahit/src/app/blog/data.js` (28654 lines, from `.bak` backup — restored after accidental overwrite)

---

## Checks Overview

| # | Check | What we look for | Threshold |
|---|-------|-----------------|-----------|
| A | TF-IDF | Primary keyword from title → count in content | ❌ if < 5 |
| B | Entities | Bengali: 'বাংলাদেশ','গুগল','সার্চ'. Case studies: 'Dhaka','Bangladesh','SEO','organic traffic' | ❌ if any missing |
| C | Pillar-Cluster | Determine pillar from tags/cluster_map; check link to pillar page | ⚠️ if no explicit link |
| D | AEO/GEO | Question headings (EN: How/What/Why/Where/Can/Do/Is/Are; BN: কী/কেন/কখন/কোথায়) | ❌ if < 2 |
| E | Internal Links | Count of /blog/, /services/, /locations/, /industries/ | ❌ if < 3 |
| F | Schema | title, excerpt, date all set? | ❌ if any missing |

---

## Bengali SEO Posts

### 1. seo-referral-traffic-bangladesh (line 13270)

| Check | Status | Details |
|-------|--------|---------|
| **A. TF-IDF** | ✅ **Pass** | "রেফারেল ট্রাফিক" appears **16×** in content body |
| **B. Entities** | ✅ **Pass** | 'বাংলাদেশ' (8×), 'গুগল' (3×), 'সার্চ' (3×) — all present |
| **C. Pillar-Cluster** | ⚠️ **Partial** | Tags: [`রেফারেল ট্রাফিক`,`ট্রাফিক জেনারেশন`,`সোশ্যাল মিডিয়া`,`অনলাইন মার্কেটিং`,`বাংলাদেশ`]. Cluster map assigns to **Content Marketing & SEO Strategy** (Pillar 4). Post links to /blog/content-marketing-strategy-bangladeshi-brands-seo, /blog/link-building-strategies-bangladesh-market, /blog/google-search-console-performance-guide — these are cluster siblings, but no explicit link to the pillar page (e.g. `complete-seo-guide-bangladesh-businesses-2026`). |
| **D. AEO/GEO** | ❌ **FAIL** | Only **1** Bengali question-word heading found: "কেন রেফারেল ট্রাফিক গুরুত্বপূর্ণ" (কেন). No কী/কখন/কোথায় question headings. Threshold is < 2. |
| **E. Internal Links** | ✅ **Pass** | **14 links**: /blog/ (4×), /services/ (2×: on-page-seo, technical-seo), /locations/ (8× city pages) |
| **F. Schema** | ✅ **Pass** | title ✅, excerpt ✅, date (2026-07-08) ✅ |

---

### 2. seo-people-also-ask-optimization (line 14504)

| Check | Status | Details |
|-------|--------|---------|
| **A. TF-IDF** | ✅ **Pass** | "PAA" appears **60+×** in content body. "পিপল অলসো আস্ক" appears in title + 1 heading but "PAA" (also in title) is pervasive enough. |
| **B. Entities** | ✅ **Pass** | 'বাংলাদেশ' (12+×), 'গুগল' (15+×), 'সার্চ' (15+×) |
| **C. Pillar-Cluster** | ⚠️ **Partial** | Tags: [`পিপল অলসো আস্ক`,`PAA`,`গুগল সার্চ`,`FAQ স্কিমা`,`রিচ স্নিপেট`,`বাংলাদেশ`]. Cluster map assigns to **GEO & AI Search** (Pillar 5). Links to /blog/seo-featured-snippet-bangladesh, /blog/keyword-research-bangladesh-market, /blog/long-tail-keywords-bangladesh — cluster siblings but no explicit link to the GEO pillar page (`/blog/geo-optimization-prepare-business-ai-search`). |
| **D. AEO/GEO** | ✅ **Pass** | **7+** Bengali question headings: "PAA বক্স কী এবং কেন গুরুত্বপূর্ণ" (কী,কেন), "PAA বক্সে কীভাবে কন্টেন্ট দেখাবেন" (কীভাবে), "কীভাবে PAA প্রশ্ন খুঁজবেন" (কীভাবে), plus FAQ section with "কী" headings (PAA বক্স কী?, উপায় কী?, সম্পর্ক কী?) |
| **E. Internal Links** | ✅ **Pass** | **15+ links**: /blog/ (6×), /services/ (2×: on-page-seo, technical-seo), /locations/ (8× city pages) |
| **F. Schema** | ✅ **Pass** | title ✅, excerpt ✅, date (2026-07-08) ✅ |

---

### 3. seo-featured-snippet-bangladesh (line 14818)

| Check | Status | Details |
|-------|--------|---------|
| **A. TF-IDF** | ✅ **Pass** | "ফিচার্ড স্নিপেট" appears **50+×** in content body |
| **B. Entities** | ✅ **Pass** | 'বাংলাদেশ' (8+×), 'গুগল' (10+×), 'সার্চ' (10+×) |
| **C. Pillar-Cluster** | ⚠️ **Partial** | Tags: [`ফিচার্ড স্নিপেট`,`পজিশন জিরো`,`গুগল সার্চ`,`রিচ স্নিপেট`,`SEO`,`বাংলাদেশ`]. Cluster map: **GEO & AI Search** (Pillar 5). Links to cluster siblings (/blog/seo-people-also-ask-optimization, /blog/seo-passage-ranking-bangladesh, /blog/seo-semantic-search-bangla) but no explicit link to the GEO pillar page. |
| **D. AEO/GEO** | ✅ **Pass** | **3** Bengali question headings: "ফিচার্ড স্নিপেট কী?" (কী), "কেন ফিচার্ড স্নিপেট গুরুত্বপূর্ণ" (কেন), plus FAQ section with "ফিচার্ড স্নিপেট কী?" |
| **E. Internal Links** | ✅ **Pass** | **16+ links**: /blog/ (6×), /services/ (2×: semantic-seo, on-page-seo), /locations/ (8× city pages) |
| **F. Schema** | ✅ **Pass** | title ✅, excerpt ✅, date (2026-07-08) ✅ |

---

### 4. seo-knowledge-panel-bangladesh (line 15151)

| Check | Status | Details |
|-------|--------|---------|
| **A. TF-IDF** | ✅ **Pass** | "নলেজ প্যানেল" appears **50+×** in content body |
| **B. Entities** | ✅ **Pass** | 'বাংলাদেশ' (8+×), 'গুগল' (12+×), 'সার্চ' (8+×) |
| **C. Pillar-Cluster** | ⚠️ **Partial** | Tags: [`নলেজ প্যানেল`,`নলেজ গ্রাফ`,`গুগল সার্চ`,`ব্র্যান্ডিং`,`SEO`,`বাংলাদেশ`]. Cluster map: **GEO & AI Search** (Pillar 5). Links to /blog/schema-markup-rich-snippets-techniques, /blog/seo-json-ld-schema-bangladesh, /blog/seo-breadcrumb-schema-bd, /blog/seo-zero-click-search-bangladesh — cluster siblings but no explicit link to GEO pillar page. |
| **D. AEO/GEO** | ✅ **Pass** | **6** Bengali question headings: "নলেজ প্যানেল কী?" (কী), "কেন নলেজ প্যানেল গুরুত্বপূর্ণ" (কেন), "কীভাবে নলেজ প্যানেল তৈরি করবেন" (কীভাবে), plus FAQ section with "নলেজ প্যানেল কী?", "নলেজ প্যানেল কীভাবে তৈরি করবেন?" (কীভাবে), "নলেজ প্যানেল কেন গুরুত্বপূর্ণ?" (কেন) |
| **E. Internal Links** | ✅ **Pass** | **12+ links**: /blog/ (5×), /services/ (3×: technical-seo, on-page-seo, geo-ai-search), /locations/ (8× city pages) |
| **F. Schema** | ✅ **Pass** | title ✅, excerpt ✅, date (2026-07-08) ✅ |

---

## Dhaka Case Studies

### 5. mir-cement-seo-case-study (line 26382)

| Check | Status | Details |
|-------|--------|---------|
| **A. TF-IDF** | ❌ **FAIL** | Primary keyword "Mir Cement" appears only **3×** in content body (lines 26393, 26395, 26446). Title (line 26383) and excerpt (line 26387) don't count toward content body. |
| **B. Entities** | ❌ **FAIL** | 'Dhaka' ✅ (1×: "best SEO expert in Dhaka"), 'Bangladesh' ✅ (2×), 'SEO' ✅ (8+×), **'organic traffic' ❌** — exact phrase not found anywhere in content body. "organic visitors" and "Organic Visitors" appear but not "organic traffic". |
| **C. Pillar-Cluster** | ✅ **Pass** | Tags: [`Case Study`,`SEO`,`B2B SEO`,`Construction`]. Cluster map assigns to **Case Studies & Portfolio** (Pillar 8). Internal links to `/blog/b2b-lead-generation-seo-bangladesh` (B2B SEO pillar sibling), `/services/technical-seo`, `/industries/garments-textile`, `/locations/dhaka`. Cross-links within case study cluster via `/blog/mir-cement-seo-case-study` reflinks in other posts. |
| **D. AEO/GEO** | ❌ **FAIL** | **0** question-format headings. All H2s are declarative: "The Challenge", "The Solution", "The Results", "Key Takeaways", "Conclusion". No How/What/Why/Where/Can/Do/Is/Are. |
| **E. Internal Links** | ✅ **Pass** | **4 links**: /blog/ (1×: b2b-lead-generation-seo-bangladesh), /services/ (1×: technical-seo), /industries/ (1×: garments-textile), /locations/ (1×: dhaka) |
| **F. Schema** | ✅ **Pass** | title ✅, excerpt ✅, date (2026-06-08) ✅ |

---

### 6. dhaka-apparels-seo-case-study (line 26452)

| Check | Status | Details |
|-------|--------|---------|
| **A. TF-IDF** | ❌ **FAIL** | Primary keyword "Dhaka Apparels" appears only **3×** in content body (lines 26463, 26465, 26513). |
| **B. Entities** | ❌ **FAIL** | 'Dhaka' ✅ (1× in content + title), 'Bangladesh' ✅ (1×: "Bangladesh $50+ billion RMG sector"), 'SEO' ✅ (5+×), **'organic traffic' ❌** — exact phrase not found in content body. |
| **C. Pillar-Cluster** | ✅ **Pass** | Tags: [`Case Study`,`SEO`,`B2B SEO`,`Garments`]. Cluster map: **Case Studies & Portfolio** (Pillar 8). Links to `/blog/b2b-lead-generation-seo-bangladesh` (B2B SEO sibling) and `/blog/mir-cement-seo-case-study` (cross-cluster ref). |
| **D. AEO/GEO** | ❌ **FAIL** | **0** question-format headings. All declarative: "The Challenge", "The Solution", "Phase 1-5", "The Results", "Key Takeaways", "Conclusion". |
| **E. Internal Links** | ✅ **Pass** | **3 links**: /blog/ (1×: b2b-lead-generation-seo-bangladesh), /industries/ (1×: garments-textile), /locations/ (1×: dhaka) |
| **F. Schema** | ✅ **Pass** | title ✅, excerpt ✅, date (2026-06-12) ✅ |

---

### 7. seo-case-study-dhaka-businesses-increased-organic-traffic (line 27548)

| Check | Status | Details |
|-------|--------|---------|
| **A. TF-IDF** | ✅ **Pass** | Keywords from title: "SEO case study" (~5×), "Dhaka" (15+×), "organic traffic" (~7× in content body: lines 27837-27839 "organic traffic" in conclusion, 27949 "organic traffic has already matched", 27955 "organic traffic grew from", 28121 "organic traffic growth", 28406 "organic traffic from AI-related keywords") |
| **B. Entities** | ✅ **Pass** | 'Dhaka' ✅ (15+× throughout), 'Bangladesh' ✅ (10+×), 'SEO' ✅ (20+×), 'organic traffic' ✅ (~7× in content) |
| **C. Pillar-Cluster** | ✅ **Pass** | Tags: [`SEO Case Study`,`Dhaka SEO`,`Organic Traffic`,`SEO Results Bangladesh`]. Cluster map: **Case Studies & Portfolio** (Pillar 8). Post is a multi-case-study compilation linking to its source businesses. Contains cross-references to other posts. |
| **D. AEO/GEO** | ✅ **Pass** | **6+** question headings: "How long does SEO take to show results for Dhaka businesses?" (How), "What is the typical SEO investment for a Dhaka-based business?" (What), "Which Dhaka neighborhoods benefit most from local SEO?" (Which ~ What), "Can I do SEO myself or should I hire a professional?" (Can, How), "How does GEO help Dhaka businesses?" (How), "What is AEO and why does it matter?" (What), "How does E-E-A-T affect SEO for Bangladeshi businesses?" (How), "What is the single most important SEO action for a new Dhaka business?" (What), "How does this SEO case study differ from international case studies?" (How) |
| **E. Internal Links** | ✅ **Pass** | **5+ links**: /blog/ references (seo-referral-traffic-bangladesh), /services/ (in body text), /locations/dhaka |
| **F. Schema** | ✅ **Pass** | title ✅, excerpt ✅, date (2026-07-14) ✅ |

---

## Summary

| # | Post | A: TF-IDF | B: Entities | C: Pillar | D: AEO/GEO | E: Int. Links | F: Schema | Flags |
|---|------|-----------|-------------|-----------|-------------|---------------|-----------|-------|
| 1 | seo-referral-traffic-bangladesh | ✅ | ✅ | ⚠️ | ❌ | ✅ | ✅ | **1 Fail, 1 Partial** |
| 2 | seo-people-also-ask-optimization | ✅ | ✅ | ⚠️ | ✅ | ✅ | ✅ | **1 Partial** |
| 3 | seo-featured-snippet-bangladesh | ✅ | ✅ | ⚠️ | ✅ | ✅ | ✅ | **1 Partial** |
| 4 | seo-knowledge-panel-bangladesh | ✅ | ✅ | ⚠️ | ✅ | ✅ | ✅ | **1 Partial** |
| 5 | mir-cement-seo-case-study | ❌ | ❌ | ✅ | ❌ | ✅ | ✅ | **3 Fails** |
| 6 | dhaka-apparels-seo-case-study | ❌ | ❌ | ✅ | ❌ | ✅ | ✅ | **3 Fails** |
| 7 | seo-case-study-dhaka-businesses-increased-organic-traffic | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | **0 Fails** |

## Critical Issues

### Immediate Failures (❌)
1. **TF-IDF < 5**: Posts 5 (Mir Cement) and 6 (Dhaka Apparels) use their primary brand keyword only 3× each in content body.
2. **Missing entity 'organic traffic'**: Posts 5 and 6 lack the exact phrase "organic traffic" entirely in content body — despite being SEO case studies.
3. **AEO/GEO = 0 question headings**: Posts 5 and 6 have zero question-format headings in English. H2s are all declarative titles.

### Recommendations
1. **Post 5 and 6**: Add "Mir Cement" / "Dhaka Apparels" at least 5× in body content and include "organic traffic" phrase naturally. Convert at least 2-3 H2s to question format (e.g., "What was the challenge?", "How did we solve it?").
2. **Post 1**: Add at least one more Bengali question heading (e.g., "কীভাবে রেফারেল ট্রাফিক বাড়াবেন?") to pass AEO/GEO check.
3. **All Bengali posts (1-4)**: Consider adding explicit links to the main pillar page for **GEO & AI Search** or **Content Marketing & SEO Strategy** to strengthen pillar-cluster topology.
4. **All posts**: Schema (title, excerpt, date) is correctly set across all 7 posts — good.

## Files Created/Modified

- **Created:** `/root/kanok-miahit/framework_audit_report_7_posts.md` (this report)
- **Restored:** `/root/kanok-miahit/src/app/blog/data.js` — was accidentally overwritten during initial analysis, restored from `/root/kanok-miahit/src/app/blog/data.js.bak`
