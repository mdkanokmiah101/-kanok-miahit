# Framework Checks Report — Batch 3 (Posts 21-28)

## Legend
| Check | Description | Pass threshold |
|-------|-------------|----------------|
| **A** (TF-IDF) | Primary keyword from title → occurrences in content | ≥ 5 |
| **B** (Entities) | Dhaka, Bangladesh, Google, SEO all appear | all 4 present |
| **C** (Pillar) | Links to /services/, /industries/, or /blog/ exist | ≥ 1 |
| **D** (AEO/GEO) | Question-based headings (How/What/Why/When/Where/Can/Do/Is/Are) | ≥ 2 |
| **E** (Internal Links) | Internal links to other posts/services/locations | ≥ 3 |
| **F** (Schema) | title, excerpt, date fields set | all 3 present |

## Summary Table

```
 #  Slug (truncated if >47 chars)                       A    B    C    D    E    F    🚩   Keyword (A)
--------------------------------------------------------------------------------------------------------------
21  long-tail-keywords-bangladesh                    ✅   ✅   ✅   ⚠️   ✅   ✅   1    লং-টেল কীওয়ার্ড
22  how-to-choose-best-seo-expert-dhaka-15-things    ✅   ✅   ✅   ✅   ✅   ✅   0    SEO Expert
23  seo-expert-vs-seo-agency-dhaka-which-is-right    ✅   ✅   ✅   ✅   ✅   ✅   0    SEO Expert
24  top-10-seo-mistakes-dhaka-businesses-fix         ✅   ✅   ✅   ✅   ✅   ✅   0    SEO Mistakes
25  what-does-seo-expert-do-guide-business-owners    ✅   ✅   ✅   ✅   ⚠️   ✅   1    SEO Expert
26  seo-case-study-dhaka-businesses-increased-orga.. ✅   ✅   ✅   ✅   ⚠️   ✅   1    SEO Case Study
27  hiring-seo-expert-dhaka-better-roi-than-paid-a.. ⚠️   ✅   ✅   ✅   ⚠️   ✅   2    SEO Expert
28  ai-seo-2026-dhaka-experts-optimize-google-ai-c.. ✅   ✅   ✅   ✅   ✅   ✅   0    AI SEO
--------------------------------------------------------------------------------------------------------------
```

**4 posts pass all 6 checks** ✅
**4 posts have issues** — Check D (Bangla post lacks question headings) and Check E (insufficient internal links)

---

## Per-Post Details

### ✅ #21 long-tail-keywords-bangladesh — **1/6 flags**
- Title: লং-টেল কীওয়ার্ড: বাংলাদেশি মার্কেটে কম প্রতিযোগিতার কীওয়ার্ড
- A: "লং-টেল কীওয়ার্ড" → 45x ✅
- B: Dhaka=5 Bangladesh=6 Google=10 SEO=57 ✅
- C: /services/=10 /industries/=0 /blog/=4 ✅
- D: 0 question headings ⚠️ (<2) — Bangla post uses declarative headings, similar to batch 2 Bangla posts
- E: 15 internal links ✅
- F: all fields set ✅

### ✅ #22 how-to-choose-best-seo-expert-dhaka-15-things — **0/6 flags** ALL PASS
- Title: How to Choose the Best SEO Expert in Dhaka: 15 Things to Check
- A: "SEO Expert" → 26x ✅
- B: Dhaka=28 Bangladesh=18 Google=18 SEO=69 ✅
- C: /services/=0 /industries/=1 /blog/=8 ✅
- D: 2 question headings ✅
- E: 9 internal links ✅
- F: all fields set ✅

### ✅ #23 seo-expert-vs-seo-agency-dhaka-which-is-right — **0/6 flags** ALL PASS
- Title: SEO Expert vs SEO Agency in Dhaka: Which One is Right for Your Business?
- A: "SEO Expert" → 22x ✅
- B: Dhaka=17 Bangladesh=13 Google=5 SEO=65 ✅
- C: /services/=0 /industries/=3 /blog/=2 ✅
- D: 4 question headings ✅
- E: 7 internal links ✅
- F: all fields set ✅

### ✅ #24 top-10-seo-mistakes-dhaka-businesses-fix — **0/6 flags** ALL PASS
- Title: Top 10 SEO Mistakes Dhaka Businesses Make (And How to Fix Them)
- A: "SEO Mistakes" → 8x ✅
- B: Dhaka=47 Bangladesh=25 Google=54 SEO=63 ✅
- C: /services/=6 /industries/=0 /blog/=1 ✅
- D: 4 question headings ✅
- E: 7 internal links ✅
- F: all fields set ✅

### ⚠️ #25 what-does-seo-expert-do-guide-business-owners — **1/6 flags**
- Title: What Does an SEO Expert Actually Do? A Complete Guide for Business Owners
- A: "SEO Expert" → 53x ✅
- B: Dhaka=29 Bangladesh=24 Google=43 SEO=130 ✅
- C: /services/=0 /industries/=0 /blog/=1 ✅
- D: 9 question headings ✅
- E: 1 internal link ⚠️ (<3) — only has `[ব্যবসায়ীদের জন্য SEO টিপস: নিজেই SEO করুন](/blog/seo-tips-for-business-owners-bd)`
- F: all fields set ✅

### ⚠️ #26 seo-case-study-dhaka-businesses-increased-organic-traffic — **1/6 flags**
- Title: SEO Case Study: How Businesses in Dhaka Increased Organic Traffic
- A: "SEO Case Study" → 7x ✅
- B: Dhaka=51 Bangladesh=28 Google=34 SEO=62 ✅
- C: /services/=0 /industries/=0 /blog/=2 ✅
- D: 9 question headings ✅
- E: 2 internal links ⚠️ (<3) — only has 2 links to Bangla blog posts
- F: all fields set ✅

### ⚠️ #27 hiring-seo-expert-dhaka-better-roi-than-paid-ads — **2/6 flags**
- Title: Why Hiring an SEO Expert in Dhaka Delivers Better ROI Than Paid Ads
- A: "SEO Expert" → 0x ⚠️ (<5) — body uses "SEO Consultant" (6x) instead of "SEO Expert" (0x); title keyword not reflected in content
- B: Dhaka=37 Bangladesh=28 Google=30 SEO=98 ✅
- C: /services/=1 /industries/=0 /blog/=0 ✅ (has /services/local-seo)
- D: 13 question headings ✅
- E: 1 internal link ⚠️ (<3) — only `[local SEO services](/services/local-seo)`
- F: all fields set ✅

### ✅ #28 ai-seo-2026-dhaka-experts-optimize-google-ai-chatgpt — **0/6 flags** ALL PASS
- Title: AI SEO in 2026: How SEO Experts in Dhaka Optimize for Google AI & ChatGPT
- A: "AI SEO" → 27x ✅
- B: Dhaka=27 Bangladesh=37 Google=51 SEO=70 ✅
- C: /services/=1 /industries/=0 /blog/=3 ✅
- D: 12 question headings ✅
- E: 4 internal links ✅
- F: all fields set ✅

---

## Entity Counts Matrix

```
 #  Slug                                     Dhaka    Bangladesh   Google   SEO
------------------------------------------------------------------------------
21  long-tail-keywords-bangladesh               5        6           10       57
22  how-to-choose-best-seo-expert-dhaka         28       18          18       69
23  seo-expert-vs-seo-agency-dhaka              17       13           5       65
24  top-10-seo-mistakes-dhaka-businesses        47       25          54       63
25  what-does-seo-expert-do                     29       24          43      130
26  seo-case-study-dhaka                        51       28          34       62
27  hiring-seo-expert-dhaka                     37       28          30       98
28  ai-seo-2026-dhaka-experts                   27       37          51       70
```

**All 8 posts pass Check B** — all 4 entities (Dhaka, Bangladesh, Google, SEO) appear in every post.

---

## Internal & Pillar Link Counts

```
 #  Slug                                    Total      /services/   /industries/   /blog/
--------------------------------------------------------------------------------------------
21  long-tail-keywords-bangladesh              15         10            0              4
22  how-to-choose-best-seo-expert-dhaka         9          0            1              8
23  seo-expert-vs-seo-agency-dhaka              7          0            3              2
24  top-10-seo-mistakes-dhaka-businesses        7          6            0              1
25  what-does-seo-expert-do                     1          0            0              1
26  seo-case-study-dhaka                        2          0            0              2
27  hiring-seo-expert-dhaka                     1          1            0              0
28  ai-seo-2026-dhaka-experts                   4          1            0              3
```

**All 8 posts pass Check C** (each has at least one pillar link).
**3 posts fail Check E** (#25, #26, #27) — insufficient internal links.

---

## Key Findings

1. **All 8 posts have excellent entity coverage** (Check B) — Dhaka, Bangladesh, Google, and SEO all appear in every post with strong counts.

2. **All 8 posts have complete schema fields** (Check F) — title, excerpt, and date are all present.

3. **All 8 posts have at least one pillar link** (Check C) — every post links to /services/, /industries/, or /blog/.

4. **4 posts pass all 6 checks** with zero flags:
   - #22 — how-to-choose-best-seo-expert-dhaka-15-things
   - #23 — seo-expert-vs-seo-agency-dhaka-which-is-right
   - #24 — top-10-seo-mistakes-dhaka-businesses-fix
   - #28 — ai-seo-2026-dhaka-experts-optimize-google-ai-chatgpt

5. **Check D failure on Bangla post (#21):** Same systemic pattern as batch 2 — the Bangla post uses declarative headings instead of question-form headings. Zero question-based headings found.

6. **Check E failures on 3 posts (#25, #26, #27):** These posts have insufficient internal linking (1-2 links vs. ≥3 required).
   - #25 has only `[ব্যবসায়ীদের জন্য SEO টিপস](/blog/seo-tips-for-business-owners-bd)`
   - #26 has only 2 links (both to Bangla blog posts)
   - #27 has only `[local SEO services](/services/local-seo)`

7. **Check A failure on post #27:** "SEO Expert" appears 0x in the body content. The post consistently uses "SEO Consultant" (6 occurrences) instead of the title's "SEO Expert" keyword. This is a genuine keyword mismatch between title and content.

---

**Files created:**
- `/root/kanok-miahit/check_batch3_posts.py` — Python script for running framework checks
- `/root/kanok-miahit/batch3_report.md` — This report
