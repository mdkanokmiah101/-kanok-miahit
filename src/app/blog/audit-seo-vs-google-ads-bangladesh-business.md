# Content Framework Audit Report

**Post:** SEO vs Google Ads — বাংলাদেশি ব্যবসার জন্য কোনটি সঠিক
**Slug:** `seo-vs-google-ads-bangladesh-business`
**Audit Date:** 2026-07-16
**File:** `/root/kanok-miahit/src/app/blog/data.js` (lines ~5441-5639)

---

## Audit Results Summary

| Check | Status | Details |
|-------|--------|---------|
| **A. TF-IDF Coverage** | ✅ PASS | Primary keyword concept ("SEO vs Google Ads") appears 8+ times; well above threshold of 5 |
| **B. Semantic Entity Coverage** | ✅ PASS | All key entities (Bangladesh/Dhaka locations, comparison terms, business types) present |
| **C. Pillar-Cluster Alignment** | ⚠️ PARTIAL | Links to `/services/` pillar pages but no dedicated Digital Marketing pillar page exists in site |
| **D. AEO/GEO** | ✅ PASS | 9 question-based headings found (threshold: 2) |
| **E. Internal Linking** | 🚩 **FLAG** | Only 2 links to `/blog/`, 0 to `/industries/`, 0 to `/locations/` (threshold: 3) |
| **F. Schema/Metadata** | ✅ PASS | All fields set: title, excerpt, date, author, readTime, tags (5) |

---

## A. TF-IDF Coverage — ✅ PASS

**Primary keyword extracted from title:** "SEO vs Google Ads" / "এসইও বনাম গুগল অ্যাডস"

| Term | Occurrences in body |
|------|:---:|
| `SEO` | 75 |
| `Google Ads` | 51 |
| `SEO এবং Google Ads` (combined form) | 7 |
| `SEO vs Google Ads` | 1 |
| `বনাম` | 2 |

**Verdict:** PASS — keyword is heavily repeated throughout, far exceeding the minimum threshold of 5. No action needed.

---

## B. Semantic Entity Coverage — ✅ PASS

| Entity Category | Keywords Checked | Found? |
|----------------|-----------------|--------|
| Location — Bangladesh | বাংলাদেশ, Bangladesh, বাংলাদেশি | ✅ Yes (multiple) |
| Location — Dhaka | ঢাকা, Dhaka | ✅ Yes (explicit) |
| Comparison terms | বনাম, vs, তুলনামূলক, পার্থক্য, তুলনা | ✅ Yes |
| Business types | ই-কমার্স, ecommerce, রেস্টুরেন্ট, বিটুবি, রিয়েল এস্টেট, হেলথকেয়ার, এডুকেশন, শপিফাই, ম্যানুফ্যাকচারিং, স্যালন, ক্লিনিক | ✅ Yes (11 types) |

**Verdict:** PASS — strong semantic coverage. Business types include ecommerce (5 mentions), restaurant (3), B2B, real estate, healthcare, education, manufacturing, salon, clinic.

---

## C. Pillar-Cluster Alignment — ⚠️ PARTIAL

**Post tags:** `["SEO vs Google Ads", "PPC", "Bangladesh Business", "ডিজিটাল মার্কেটিং", "Online Advertising"]`

**Inferred pillar topic:** ডিজিটাল মার্কেটিং (Digital Marketing) / SEO Services

**Pillar page links found:**
| Link Target | Anchor Text | Type |
|-------------|-------------|------|
| `/services` | SEO সার্ভিস | ✅ Pillar link (appears twice) |
| `/services/local-seo` | local SEO services for Bangladeshi businesses | ✅ Cluster link |
| `/services/technical-seo` | টেকনিক্যাল SEO | ✅ Cluster link |
| `/services/ecommerce-seo` | ই-কমার্স SEO | ✅ Cluster link |
| `/services/semantic-seo` | কন্টেন্ট মার্কেটিং | ✅ Cluster link |
| `/services/local-seo` | লোকাল SEO | ✅ Cluster link |

**Verdict:** PARTIAL — The post successfully links to the main `/services/` pillar page and multiple service cluster pages. However, there is **no dedicated Digital Marketing pillar page** in the site structure (`/services/[slug]` directory exists but no specific "digital-marketing" route). The tag "ডিজিটাল মার্কেটিং" (Digital Marketing) would benefit from a dedicated pillar page that links to all posts in this cluster.

---

## D. AEO/GEO — ✅ PASS

**Question-based headings found (9 total, threshold: 2):**

| # | Heading | Type |
|:-:|---------|------|
| 1 | কখন SEO বেছে নেবেন | 🇧🇩 Question word (কখন) |
| 2 | কখন Google Ads বেছে নেবেন | 🇧🇩 Question word (কখন) |
| 3 | Bangladesh-এ GEO কেন গুরুত্বপূর্ণ? | 🇧🇩 Question word (কেন) + ❓ |
| 4 | কীভাবে AEO আপনার SEO বনাম গুগল এডস কে সাহায্য করবে? | 🇧🇩 Question word (কীভাবে) + ❓ |
| 5 | SEO বনাম গুগল এডস এর জন্য সঠিক কৌশল কী? | ❓ |
| 6 | AI সার্চ ইঞ্জিনের জন্য কীভাবে কন্টেন্ট অপটিমাইজ করবেন? | ❓ |
| 7 | কেন বিশ্বাস করবেন মোঃ কনক মিঞাকে? | 🇧🇩 Question word (কেন) + ❓ |
| 8 | আরও জানতে চান? বিশেষজ্ঞ পরামর্শ নিন | ❓ |
| 9 | কখন SEO এবং কখন Google Ads ব্যবহার করবেন? | 🇧🇩 Question word (কখন) + ❓ |

**Also contains dedicated AEO/GEO sections:**
- Section: "জেনারেটিভ ইঞ্জিন অপটিমাইজেশন (GEO) — AI সার্চের জন্য প্রস্তুতি" (line 5565)
- Section: "AI সার্চ ও অ্যানসার ইঞ্জিন অপটিমাইজেশন (AEO)" (line 5583)
- FAQ-style Q&A blocks (lines 5599-5604)

**Verdict:** PASS — Excellent AEO/GEO compliance. The post has dedicated GEO and AEO sections, multiple question-answer pairs, and a FAQ-style format well-suited for AI search engines.

---

## E. Internal Linking — 🚩 FLAG

| Target pattern | Count | URLs found |
|---------------|:-----:|------------|
| `/blog/` | 2 | `/blog/seo-vs-google-ads-whats-best-bangladesh-businesses`, `/blog/keyword-research-bangladesh-market` |
| `/industries/` | 0 | — |
| `/locations/` | 0 | — |
| **Total** | **2** | — |
| `/services/` | 9 | (5 unique destinations x ~2 appearances each) |
| `/contact` | 1 | `/contact` |

**Verdict: FLAG** — Only 2 internal links to `/blog/`, `/industries/`, or `/locations/` combined (threshold: 3).

---

## F. Schema/Metadata — ✅ PASS

| Field | Status | Value |
|-------|--------|-------|
| `title` | ✅ SET | এসইও বনাম গুগল অ্যাডস: বাংলাদেশি ব্যবসার জন্য কোনটি সঠিক |
| `slug` | ✅ SET | seo-vs-google-ads-bangladesh-business |
| `date` | ✅ SET | 2026-07-08 |
| `author` | ✅ SET | মোঃ কনক মিঞা |
| `excerpt` | ✅ SET | বাংলাদেশি ব্যবসার জন্য SEO এবং Google Ads — কোনটি বেশি কার্যকরী?... |
| `readTime` | ✅ SET | 10 min |
| `tags` | ✅ SET | 5 tags (SEO vs Google Ads, PPC, Bangladesh Business, ডিজিটাল মার্কেটিং, Online Advertising) |
| `imagePlaceholder` | ✅ SET | 🏗️ |

**Verdict:** PASS — All required metadata fields are present.

---

## Fix Instructions

### 🚩 HIGH PRIORITY — Fix Internal Linking (Check E)

**Problem:** Only 2 links to `/blog/`, `/industries/`, `/locations/` — below the minimum of 3.

**Recommended fixes (add at least 2 additional links):**

1. **Add a link to a relevant `/industries/` page.** The post already discusses multiple industries (e-commerce, restaurant, B2B, real estate, healthcare, education). Add a relevant markdown link, e.g.:
   ```
   - [ই-কমার্স ব্যবসার জন্য SEO টিপস](/industries/ecommerce-seo) — আরও জানুন
   ```
   Add this near the "বাংলাদেশি ইন্ডাস্ট্রির জন্য সুপারিশ" section (~line 5522).

2. **Add a link to a relevant `/locations/` page.** The post discusses Dhaka and Bangladesh. Add:
   ```
   - [ঢাকার জন্য লোকাল SEO সার্ভিস](/locations/dhaka) — বিস্তারিত
   ```
   Add this near the "ঢাকায় একটি নতুন রেস্টুরেন্ট" example (~line 5534).

3. **Alternatively, add a third `/blog/` link** if no relevant industries/locations pages exist. The post could link to another related blog post like a technical SEO guide.

### ⚠️ MEDIUM PRIORITY — Pillar-Cluster Enhancement (Check C)

**Problem:** No dedicated "Digital Marketing" pillar page exists.

**Recommendations:**
1. Create a `/services/digital-marketing` pillar page that serves as the hub for all blog posts tagged with "ডিজিটাল মার্কেটিং" and related tags.
2. Ensure this post links to `/services/digital-marketing` once it exists.
3. If a pillar page won't be created, add the tag "SEO সার্ভিস" which better matches the existing `/services/` pillar page.

### ✅ LOW PRIORITY — Already Meeting Standards

- **TF-IDF:** No changes needed
- **Semantic entities:** Already strong; consider adding a mention of "চট্টগ্রাম" for broader location coverage
- **AEO/GEO:** Already excellent; no changes needed
- **Schema:** Already complete; no changes needed

---

## Final Verdict

| Component | Score |
|-----------|:-----:|
| A. TF-IDF Coverage | ✅ 100% |
| B. Semantic Entity Coverage | ✅ 100% |
| C. Pillar-Cluster Alignment | ⚠️ 70% |
| D. AEO/GEO | ✅ 100% |
| E. Internal Linking | 🚩 40% |
| F. Schema/Metadata | ✅ 100% |
| **Overall** | **85% — Good, with 1 fix needed** |
