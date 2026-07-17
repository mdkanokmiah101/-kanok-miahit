# Content Framework Compliance Audit
## Post: `seo-tips-for-business-owners-bd`

**File:** `/root/kanok-miahit/src/app/blog/data.js` (lines 5912–6179)
**Title:** ব্যবসায়ীদের জন্য SEO টিপস: নিজেই SEO করুন
**Date:** 2026-07-08
**Tags:** ব্যবসায়ীদের জন্য SEO, DIY SEO, বাংলাদেশ ব্যবসা, লোকাল SEO

---

## Audit Results

| # | Check | Result | Score | Details |
|---|-------|--------|-------|---------|
| A | **TF-IDF Coverage** | ❌ **FAIL** | 0/5 | Primary keyword "SEO টিপস" appears **0 times** in content body. "ব্যবসায়ীদের জন্য SEO" appears once. "DIY SEO" appears 3 times. All below threshold of 5. |
| B | **Semantic Entity Coverage** | ✅ **PASS** | 3/3 | **Location** (Bangladesh/Dhaka): 28 mentions ✓ · **Audience** (ব্যবসায়ী): 6 mentions ✓ · **Service type** (SEO/tips): extensively covered ✓ |
| C | **Pillar-Cluster Alignment** | ⚠️ **NEEDS WORK** | — | Tags are fragmented across 4 directions (SEO-for-business, DIY SEO, Bangladesh business, Local SEO). No single pillar topic. **One pillar link exists** (`/blog/complete-seo-guide-bangladesh-businesses-2026`) but it doesn't match the tags cohesively. |
| D | **AEO/GEO** | ✅ **PASS** | 9/2 | **9 question-based headings** found (threshold: ≥2). Strong coverage — many "কী", "কেন", "কীভাবে" headings throughout. |
| E | **Internal Linking** | ✅ **PASS** | 4/3 | **4 internal links to /blog/** · 0 to /industries/ · 0 to /locations/. Total qualifying: 4 (threshold: ≥3). |
| F | **Schema** | ✅ **PASS** | 5/5 | title ✓ · excerpt ✓ · date ✓ · author ✓ · tags ✓. All present. |

---

## Detailed Findings

### A. TF-IDF Coverage — DETAILED

| Keyword Variant | Occurrences in Content Body | Threshold | Status |
|---|---|---|---|
| `SEO টিপস` (exact from title) | **0** | ≥5 | ❌ |
| `ব্যবসায়ীদের জন্য SEO` | **1** | ≥5 | ❌ |
| `DIY SEO` | **3** | ≥5 | ❌ |
| `টিপস` (generic) | 3 | — | — |
| `SEO` (any context) | ~43 | — | Benchmark only |

**Root cause:** The title keyword "SEO টিপস" is never repeated in the content body. The post uses "DIY SEO গাইড", "SEO tips" (English word "tips" not in Bangla), and "প্র্যাকটিক্যাল টিপস" but never the exact Bangla phrase "SEO টিপস".

### B. Semantic Entity Coverage — DETAILED

| Entity | Examples Found | Count | Status |
|---|---|---|---|
| **Location** | বাংলাদেশ (Bangladesh), ঢাকা (Dhaka), গুলশান, চট্টগ্রাম, সিলেট | 28 | ✅ |
| **Audience** | ব্যবসায়ী (business people/owners), ব্যবসায়িক | 6 | ✅ |
| **Service type** | SEO, SEO টিপস concepts, SEO কৌশল, সার্চ ইঞ্জিন অপটিমাইজেশন | ~43 | ✅ |

### C. Pillar-Cluster Alignment — DETAILED

**Tags → Pillar mapping:**
- `ব্যবসায়ীদের জন্য SEO` → SEO-for-business pillar (no dedicated pillar page linked)
- `DIY SEO` → DIY/self-service SEO pillar (no dedicated pillar page linked)
- `বাংলাদেশ ব্যবসা` → Bangladesh business pillar (no dedicated pillar page linked)
- `লোকাল SEO` → Local SEO (linked via `/services/local-seo`, but that's a service page, not a blog pillar)

**Pillar link found:** `/blog/complete-seo-guide-bangladesh-businesses-2026` (line 6073) — this serves as a general SEO pillar but doesn't specifically match any single tag.

**Issue:** Tags should be consolidated to 1–2 pillar topics. Currently scattered across 4 different directions.

### D. AEO/GEO — DETAILED

**Question-based headings found (9 total):**
1. `## ব্যবসায়ীদের জন্য SEO: কেন এটি গুরুত্বপূর্ণ?`
2. `## SEO কী এবং কেন ব্যবসায়ীদের এটি জানা দরকার?`
3. `## কখন প্রফেশনাল সাহায্য নেওয়া উচিত?`
4. `### Bangladesh-এ GEO কেন গুরুত্বপূর্ণ?`
5. `### কীভাবে AEO আপনার ব্যবসার জন্য SEO কে সাহায্য করবে?`
6. `### ব্যবসার জন্য SEO এর জন্য সঠিক কৌশল কী?`
7. `### AI সার্চ ইঞ্জিনের জন্য কীভাবে কন্টেন্ট অপটিমাইজ করবেন?`
8. `## কেন বিশ্বাস করবেন মোঃ কনক মিঞাকে?`
9. `## আরও জানতে চান? বিশেষজ্ঞ পরামর্শ নিন`

### E. Internal Linking — DETAILED

| Pattern | Count | Links Found |
|---|---|---|
| `/blog/` | **4** | `/blog/seo-bangla-blog-content-writing`, `/blog/content-marketing-strategy-bangladeshi-brands-seo`, `/blog/content-marketing-seo-friendly-content-writing`, `/blog/complete-seo-guide-bangladesh-businesses-2026` |
| `/industries/` | **0** | — |
| `/locations/` | **0** | — |
| **Total** | **4** | ✅ ≥ 3 |

### F. Schema — DETAILED

| Field | Value | Status |
|---|---|---|
| `slug` | `seo-tips-for-business-owners-bd` | ✅ |
| `title` | ব্যবসায়ীদের জন্য SEO টিপস: নিজেই SEO করুন | ✅ |
| `date` | 2026-07-08 | ✅ |
| `author` | মোঃ কনক মিঞা | ✅ |
| `excerpt` | বাংলাদেশি ব্যবসায়ীদের জন্য সম্পূর্ণ DIY SEO গাইড … | ✅ |
| `tags` | ["ব্যবসায়ীদের জন্য SEO", "DIY SEO", "বাংলাদেশ ব্যবসা", "লোকাল SEO"] | ✅ |
| `imagePlaceholder` | 🏪 | ✅ |

---

## Fix Instructions

### 🔴 CRITICAL — A. TF-IDF Coverage

**Problem:** Primary keyword "SEO টিপস" has 0 occurrences in the content body.

**Fix:** Add the keyword "SEO টিপস" naturally at least 5 times throughout the content body. Suggested insertion points:

1. **Line 5924 (intro):** Change "প্র্যাকটিক্যাল টিপস শেয়ার করছি" → **"SEO টিপস শেয়ার করছি"** (1 occurrence)
2. **Line 5934 (heading):** Change "## ব্যবসায়ীদের জন্য DIY SEO গাইড" → **"## ব্যবসায়ীদের জন্য SEO টিপস: সম্পূর্ণ DIY গাইড"** (1 occurrence)
3. **Line 5951 (keyword research):** Add a sentence: "এই **SEO টিপস** গুলো ফলো করলে আপনি নিজেই আপনার সাইটের র‍্যাংকিং উন্নত করতে পারবেন।" (1 occurrence)
4. **Line 5980 (content creation):** Add: "কন্টেন্ট তৈরির সময় উপরের **SEO টিপস** মাথায় রাখুন।" (1 occurrence)
5. **Line 6077 (conclusion):** Add: "এই **SEO টিপস** গুলো নিয়মিত অনুশীলন করলে সাফল্য আসবেই।" (1 occurrence)

### 🟡 MODERATE — C. Pillar-Cluster Alignment

**Problem:** Tags are fragmented (4 different directions). No clear pillar-cluster mapping.

**Fix options:**
1. **Consolidate tags** to a single pillar focus (e.g., keep only "DIY SEO" and "ব্যবসায়ীদের জন্য SEO" and remove the other two), OR
2. **Add a dedicated pillar link** for each tag cluster. For example:
   - For "লোকাল SEO" tag → link to a Local SEO pillar page if one exists, or add `/blog/...` link
   - For "বাংলাদেশ ব্যবসা" tag → link to a Bangladesh business SEO pillar
3. Ensure the primary pillar link (`/blog/complete-seo-guide-bangladesh-businesses-2026`) is clearly related to the tags.

### 🟢 INFO — Other Checks

- **D. AEO/GEO:** ✅ Already strong with 9 question-based headings. No changes needed.
- **E. Internal Linking:** ✅ Above threshold (4 links). Consider adding `/industries/` and `/locations/` links for stronger internal mesh.
- **F. Schema:** ✅ All fields present. No changes needed.

---

## Overall Score

| Category | Result |
|---|---|
| Pass | B, D, E, F |
| Fail | **A — TF-IDF Coverage** |
| Needs Improvement | **C — Pillar-Cluster Alignment** |
| **Not Pass (overall)** | ❌ |

> **Action required:** Fix the TF-IDF keyword coverage (critical) and tighten pillar-cluster alignment (moderate) before this post is fully compliant.
