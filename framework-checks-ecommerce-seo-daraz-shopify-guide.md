# Blog Post Framework Check Report

**Post:** ই-কমার্স SEO: দারাজ ও শপিফাই স্টোরের জন্য সম্পূর্ণ গাইড
**Slug:** ecommerce-seo-daraz-shopify-guide
**Location:** `/root/kanok-miahit/src/app/blog/data.js`, lines 3753–3967

---

## A. TF-IDF Coverage

| Metric | Value |
|--------|-------|
| **Title** | ই-কমার্স SEO: দারাজ ও শপিফাই স্টোরের জন্য সম্পূর্ণ গাইড |
| **Primary keyword extracted** | ই-কমার্স SEO (first meaningful noun phrase) |
| **Occurrences in content** | **10** (lines: 3762 h2, 3826 body, 3832 h2, 3848 body, 3858 body, 3874 h3, 3903 h3, 3915 h3, 3949 body, 3963 list) |
| **Threshold** | ≥ 5 required |
| **Status** | ✅ **PASS** — Keyword appears 10 times, well above threshold |

---

## B. Semantic Entity Coverage

| Entity | Expected | Found? | Location(s) |
|--------|----------|--------|-------------|
| **Dhaka** (location) | Present | ✅ | Line 3766: "ঢাকায় অনলাইনে শাড়ি কিনবেন"; line 3858: "সেরা SEO সার্ভিস ঢাকা" |
| **Bangladesh** (location) | Present | ✅ | Line 3764: "বাংলাদেশের ই-কমার্স বাজার"; line 3766: "বাংলাদেশ"; throughout |
| **Service type (SEO)** | Present | ✅ | Ubiquitous across the entire post |
| **Industry (E-commerce)** | Present | ✅ | Line 3764: "ই-কমার্স বাজার"; heading at 3824; throughout |
| **Daraz** | Present | ✅ | Multiple — lines 3764, 3768, 3770, 3772, etc.; entire section "দারাজ সেলারদের জন্য SEO কৌশল" |
| **Shopify** | Present | ✅ | Multiple — entire section "শপিফাই স্টোরের জন্য SEO" starting line 3796 |

**Status:** ✅ **PASS** — All 5 required semantic entities present

---

## C. Pillar-Cluster Alignment

| Metric | Value |
|--------|-------|
| **Tags** | ই-কমার্স SEO, Daraz, Shopify, E-commerce Bangladesh, অনলাইন স্টোর |
| **Pillar topic inferred** | **E-commerce SEO** (based on primary tag and content focus) |
| **Relevant pillar/service page** | `/services/ecommerce-seo` (E-commerce SEO service page) |
| **Link to pillar/service page found?** | ✅ **YES** — Line 3852: `[e-commerce SEO services for Daraz and Shopify](/services/ecommerce-seo)` |
| **Additional pillar link** | ✅ Line 3963: `[ই-কমার্স SEO](/services/ecommerce-seo)` in service list |
| **Industry page link** | ✅ Line 3856: `[e-commerce retail SEO solutions](/industries/ecommerce)` |

**Status:** ✅ **PASS** — Post links directly to the pillar service page `/services/ecommerce-seo`

---

## D. AEO/GEO Optimization — Question-Based Headings

| Heading | Starts with English Q-word? | Match? |
|---------|----------------------------|--------|
| ## বাংলাদেশে ই-কমার্স SEO কেন গুরুত্বপূর্ণ | "বাংলাদেশে" (Bengali) | ❌ |
| ## দারাজ সেলারদের জন্য SEO কৌশল | "দারাজ" (Bengali) | ❌ |
| ## শপিফাই স্টোরের জন্য SEO | "শপিফাই" (Bengali) | ❌ |
| ## বাংলাদেশি ই-কমার্সের জন্য কন্টেন্ট মার্কেটিং | "বাংলাদেশি" (Bengali) | ❌ |
| ## ই-কমার্স SEO চেকলিস্ট | "ই-কমার্স" (Bengali) | ❌ |
| ## উপসংহার | "উপসংহার" (Bengali) | ❌ |
| ## প্রায়শই জিজ্ঞাসিত প্রশ্ন | "প্রায়শই" (Bengali) | ❌ |
| ## জেনারেটিভ ইঞ্জিন অপটিমাইজেশন (GEO) | "জেনারেটিভ" (Bengali) | ❌ |
| ## AI সার্চ ও অ্যানসার ইঞ্জিন অপটিমাইজেশন (AEO) | "AI" (not a Q-word) | ❌ |
| ## E-E-A-T: Google-এর গুণগত মানের মাপকাঠি | "E-E-A-T" (not a Q-word) | ❌ |
| ## কেন বিশ্বাস করবেন মোঃ কনক মিঞাকে? | "কেন" (Bengali for "Why") | ❌ |
| ## আরও জানতে চান? | "আরও" (Bengali) | ❌ |
| ### দারাজে SEO করতে কত সময় লাগে? | "দারাজে" (Bengali) | ❌ |
| ### শপিফাই এবং দারাজের জন্য SEO কি আলাদা? | "শপিফাই" (Bengali) | ❌ |
| ### প্রোডাক্ট পেজের জন্য কত শব্দের কন্টেন্ট দরকার? | "প্রোডাক্ট" (Bengali) | ❌ |
| ### ই-কমার্স সাইটের জন্য কোন স্কিমা সবচেয়ে গুরুত্বপূর্ণ? | "ই-কমার্স" (Bengali) | ❌ |
| ### ই-কমার্স SEO-তে সবচেয়ে বড় ভুল কী? | "ই-কমার্স" (Bengali) | ❌ |
| ### বাংলাদেশি ই-কমার্সের জন্য কোন প্ল্যাটফর্ম SEO-তে ভালো? | "বাংলাদেশি" (Bengali) | ❌ |
| ### Bangladesh-এ GEO কেন গুরুত্বপূর্ণ? | "Bangladesh-এ" (not a Q-word) | ❌ |
| ### কীভাবে AEO আপনার ই-কমার্স SEO কে সাহায্য করবে? | "কীভাবে" (Bengali for "How") | ❌ |
| ### ই-কমার্স SEO এর জন্য সঠিক কৌশল কী? | "ই-কমার্স" (Bengali) | ❌ |
| ### AI সার্চ ইঞ্জিনের জন্য কীভাবে কন্টেন্ট অপটিমাইজ করবেন? | "AI" (not a Q-word) | ❌ |

| Metric | Value |
|--------|-------|
| **Question headings starting with English Q-words** | **0** |
| **Threshold** | ≥ 2 |
| **Status** | ❌ **FLAG** — Strictly, 0 headings start with English question words (How, What, Why, When, Where, Can, Do, Is, Are) |
| **Note** | The post is entirely in Bengali. It contains **14 semantically question-based headings** (FAQ section + GEO/AEO sections with "কেন" / "কীভাবে" / "কী" question markers). These serve the AEO/GEO purpose but don't match the English-centric strict criteria. |

---

## E. Internal Linking

| Internal link | Type | Location |
|---------------|------|----------|
| `/blog/seo-for-facebook-marketplace` | /blog/ | Line 3830 |
| `/services/ecommerce-seo` | /services/ | Line 3852 |
| `/blog/why-ecommerce-store-needs-seo-bangladesh` | /blog/ | Line 3854 |
| `/industries/ecommerce` | /industries/ | Line 3856 |
| `/services` | /services/ | Line 3858 |
| `/services/technical-seo` | /services/ | Line 3949 |
| `/services/local-seo` | /services/ | Line 3949 |
| `/services/semantic-seo` | /services/ | Line 3949 |
| *(duplicate: /blog/why-ecommerce-store-needs-seo-bangladesh at 3960)* | /blog/ | Duplicate |
| *(duplicate: /services/technical-seo at 3961)* | /services/ | Duplicate |
| *(duplicate: /services/local-seo at 3962)* | /services/ | Duplicate |
| *(duplicate: /services/ecommerce-seo at 3963)* | /services/ | Duplicate |
| *(duplicate: /services/semantic-seo at 3964)* | /services/ | Duplicate |

| Metric | Value |
|--------|-------|
| **Unique internal links (/blog/, /services/, /industries/, /locations/)** | **8** (2 blog + 5 services + 1 industries + 0 locations) |
| **Threshold** | ≥ 3 |
| **Status** | ✅ **PASS** — 8 internal links found, well above threshold |

---

## F. Schema / Metadata Fields

| Field | Present? | Value |
|-------|----------|-------|
| **title** | ✅ | ই-কমার্স SEO: দারাজ ও শপিফাই স্টোরের জন্য সম্পূর্ণ গাইড |
| **excerpt** | ✅ | দারাজ এবং শপিফাই স্টোরের জন্য ই-কমার্স SEO-র সম্পূর্ণ গাইড... |
| **date** | ✅ | 2026-07-08 |
| **author** | ✅ | মোঃ কনক মিঞা |
| **tags** | ✅ | ["ই-কমার্স SEO", "Daraz", "Shopify", "E-commerce Bangladesh", "অনলাইন স্টোর"] |

**Status:** ✅ **PASS** — All 5 required metadata fields present

---

## Summary of Results

| Check | Result |
|-------|--------|
| **A. TF-IDF Coverage** | ✅ PASS (10 occurrences ≥ 5) |
| **B. Semantic Entity Coverage** | ✅ PASS (all 6 entities present) |
| **C. Pillar-Cluster Alignment** | ✅ PASS (links to `/services/ecommerce-seo`) |
| **D. AEO/GEO Optimization** | ❌ **FLAG** (0 English Q-word headings; post is Bengali — 14 Bengali question headings exist) |
| **E. Internal Linking** | ✅ PASS (8 internal links ≥ 3) |
| **F. Schema/Metadata** | ✅ PASS (all 5 fields present) |

**5/6 checks pass. 1 flag (D. AEO/GEO) — the post is entirely in Bengali and contains 14 semantically question-based headings in Bengali ("কেন" = Why, "কীভাবে" = How, "কী" = What) which serve the AEO/GEO purpose, but strictly no headings start with the English question words specified in the criteria.**
