# Content Framework Check Report

**Post:** how-to-choose-best-seo-expert-dhaka-15-things
**Title:** How to Choose the Best SEO Expert in Dhaka: 15 Things to Check
**Date:** 2026-07-14
**Author:** Md Kanok Miah
**Tags:** SEO Expert Dhaka, Hire SEO Expert, SEO Services Bangladesh, Best SEO Expert
**Content Length:** ~12,089 characters (~2,000 words)
**Checker:** framework_check_v2.py + manual verification

---

## Framework Check Results

| # | Check | Status | Details |
|---|-------|--------|---------|
| 1 | **TF-IDF Keyword Density** | ✅ PASS | `"seo expert"` — 25 occurrences (≥5 threshold met) |
| 2 | **Entities (Dhaka/Bangladesh)** | ✅ PASS | Dhaka: 24 mentions, Bangladesh: 6 mentions — both present |
| 3 | **Pillar Cluster Link** | ❌ FAIL | **0 relative links detected** (see note below) |
| 4 | **AEO/GEO Question Headings** | ❌ FAIL | **0 markdown question headings** (see note below) |
| 5 | **Internal Links (≥3)** | ❌ FAIL | **0 relative internal links detected** (see note below) |
| 6 | **Schema Readiness** | ⚠️ TOOL BUG | Excerpt field present but not parsed correctly by checker |

---

## Detailed Analysis Per Criterion

### 1. ✅ TF-IDF Keyword Density — PASS

- **Keyword detected:** `"seo expert"` (bigram from title: "How to Choose the Best **SEO Expert** in Dhaka: 15 Things to Check")
- **Occurrences in content:** 25
- **Threshold:** ≥5
- **Verdict:** Well above threshold. The phrase "SEO expert" is naturally distributed throughout the post.

### 2. ✅ Entities — PASS

- **Dhaka:** 24 mentions — extensively covered (Gulshan, Banani, Dhanmondi, Uttara, Mirpur areas mentioned)
- **Bangladesh:** 6 mentions — present (Bangladeshi consumer behavior, Bangladesh market, etc.)
- **Verdict:** Both required location entities are present. Passes.

### 3. ❌ Pillar Cluster Link — FAIL (Tool Limitation)

**Tool result:** 0 pillar links found (0 service, 0 industry, 0 blog links)

**Actual content:** The post contains **20 internal links** using **absolute URLs** (`https://kanokmiah.com.bd/...`) instead of relative paths (`/...`). The checker's regex (`\(/services/[^)]+\)`) only matches relative paths.

**Absolute internal links present (all to same domain):**
| Target Page | Link Text |
|---|---|
| `/` (home) | "best SEO expert in Dhaka" (×4), "SEO specialist in Dhaka", "SEO consultant in Dhaka", "professional SEO expert in Dhaka", "5-step methodology", "kanokmiah.com.bd" |
| `/case-studies` | "SEO case studies" |
| `/industries/real-estate` | "real estate developer" (×2) |
| `/industries/garments-textile` | "garments factory" |
| `/services/geo-ai-search` | "AI SEO" |
| `/contact` | "free SEO audit", "contact me" |
| `/industries/ecommerce` | "e-commerce" |
| `/industries/smm-panel` | "SMM panels" |
| `/industries/medical` | "healthcare" |

**Pillar pages linked:** /case-studies, /industries/ (real-estate, garments-textile, ecommerce, smm-panel, medical), /services/geo-ai-search, /contact

**Verdict:** The post DOES link to pillar/industry/service pages (8 distinct internal destinations), but uses absolute URLs. **Fix: Convert `https://kanokmiah.com.bd/...` links to relative `/...` paths** so the checker (and Google's internal link analysis) can properly detect them.

### 4. ❌ AEO/GEO Question Headings — FAIL (Format Issue)

**Tool result:** 0 question headings detected

**Actual content:** The post has **21 markdown headings** (3× H2 + 17× H3 + 1× H2 for FAQ), all **declarative** — none contain a "?" character.

However, the **FAQ section** contains **5 questions formatted as bold text** (`**...?**`) rather than markdown headings:

1. `**What is the difference between an SEO expert and an SEO agency in Dhaka?**`
2. `**How long does it take to see results from a good SEO expert in Dhaka?**`
3. `**Can I do SEO myself instead of hiring an expert?**`
4. `**How much does a good SEO expert charge in Dhaka?**`
5. `**What guarantees should I expect from an SEO expert?**`

**Verdict:** The post has question content but not in the format the framework requires. AEO/GEO optimization for AI search engines works best with `##`-style question headings. **Fix: Convert 2+ of the FAQ bold questions to `##`-style headings** (e.g., `## What is the difference between an SEO expert and an SEO agency in Dhaka?`). This also improves AI search extractability.

### 5. ❌ Internal Links — FAIL (Tool Limitation)

**Tool result:** 0 internal links detected

**Actual content:** The post has **20 internal links** to pages on `kanokmiah.com.bd`, all using absolute URLs. Same root cause as criterion #3.

**Link distribution:**
| Category | Count |
|----------|-------|
| Home page (/) | 9 |
| Industries | 5 (real-estate ×2, garments-textile, ecommerce, smm-panel, medical) |
| Services | 1 (geo-ai-search) |
| Case Studies | 1 |
| Contact | 2 |
| **Total** | **20** |

**Verdict:** The post has abundant internal links (20 total, covering 8+ unique destinations) but all use absolute URLs. **Fix: Convert links to relative paths** (`/case-studies`, `/industries/real-estate`, etc.) so the framework checker and Google's internal link analysis can properly attribute them.

### 6. ⚠️ Schema Readiness — Tool Bug (Data Actually Present)

**Tool result:** FAIL — excerpt field "missing"

**Actual state in data.js:**
```javascript
excerpt:
  "Hiring the right SEO expert in Dhaka can transform your business, but choosing wrong wastes time and money. Here are 15 things to check before you hire the best SEO expert in Dhaka.",
```

**All schema fields present:**
| Field | Value | Status |
|-------|-------|--------|
| title | "How to Choose the Best SEO Expert in Dhaka: 15 Things to Check" | ✅ |
| excerpt | "Hiring the right SEO expert in Dhaka..." (128 chars) | ✅ (multi-line format not parsed by tool) |
| date | "2026-07-14" | ✅ |
| author | "Md Kanok Miah" | ✅ |
| tags | ["SEO Expert Dhaka", "Hire SEO Expert", "SEO Services Bangladesh", "Best SEO Expert"] | ✅ |

**Issue:** The `framework_check_v2.py` excerpt extraction code has a bug — it calls `stripped[8:]` on the `excerpt:` line (where `stripped` is just `"excerpt:"`) which returns an empty string, so it breaks out of the parsing loop without reading the value on the next line. **This is a script bug, not a content issue.**

**Verdict:** All ArticleSchema fields are present and populated. ✅ **PASS from content perspective.**

---

## Real Issues vs. Tool Artifacts

| Issue | Real Problem? | Priority |
|-------|---------------|----------|
| All internal links use absolute URLs | ✅ Yes — should use relative links for proper SEO value flow and framework compliance | **HIGH** |
| No `##`-style question headings | ✅ Yes — FAQ uses bold text format instead; AI search engines extract headings better | **MEDIUM** |
| Excerpt parsing fails | ❌ No — tool bug, data is correct | None |
| TF-IDF at 25 occurrences | ❌ No — well above threshold | None |
| Entities missing | ❌ No — both Dhaka and Bangladesh well covered | None |

---

## Recommended Fixes

1. **Convert absolute URLs to relative paths** — Replace `https://kanokmiah.com.bd/...` with `/...` throughout the post. This fixes both the Pillar Link check and Internal Links check, and follows SEO best practices (relative links preserve protocol and domain).

2. **Add 2+ `##`-style question headings** — Change the FAQ section from bold-text questions to proper `##` headings:
   ```markdown
   ## Frequently Asked Questions
   
   ## What is the difference between an SEO expert and an SEO agency in Dhaka?
   ...
   ## How long does it take to see results from a good SEO expert in Dhaka?
   ```

3. **No changes needed** for TF-IDF, entities, or schema — all correct.

---

## Summary

| Metric | Value |
|--------|-------|
| Checks Passed | **2/6** (TF-IDF, Entities) |
| Checks Failed (real content issues) | **3/6** (Pillar Link format, AEO/GEO format, Internal Links format) |
| Checks Failed (tool bug only) | **1/6** (Schema — excerpt parsing) |
| Real issues to fix | **2** (absolute URLs → relative; bold FAQ → heading FAQ) |
