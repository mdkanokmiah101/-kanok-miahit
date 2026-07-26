# Content Framework Enforcement Report
**Site:** kanokmiah.com.bd  
**Date:** July 21, 2026  
**Trigger:** Changes detected in `src/app/blog/data.js` (last 48 hours — 3 commits)

## Changes Detected
| Commit | Date | Changes |
|--------|------|---------|
| `8334a58` | Jul 19 | Heading/HTML tags cleanup (2 posts fixed) |
| `001ef98` | Jul 20 | Internal linking audit — removed 7 duplicate links, added 18 homepage links across 22 posts |
| `cad9c06` | Jul 20 | Bulk blank-line cleanup after headings (707 blank lines removed, all posts affected) |

**Scope:** All ~128 posts had formatting changes; ~44 posts had substantive content changes from the internal linking audit.

---

## Summary of Framework Checks Run Across All Posts

| Batch | # Posts | ✅ Full Pass | ❌ Flags | Key Issues |
|-------|---------|-------------|---------|------------|
| Batch 1 (Pillar posts) | 7 | 7 | 0 | — |
| Batch 2 (Industry posts) | 5 | 4 | 1 | Pillar link missing (garments post) |
| Batch 3 (Bengali posts) | 7 | 6 | 1 | TF-IDF thin (seo-trends-2026) |
| Batch 4 (Strategy posts) | 10 | 9 | 1 | TF-IDF thin (seo-tips-for-business-owners) |
| Batch 5 (Advanced Bengali) | 10 | 10 | 0 | — |
| Batch 6 (Service/business) | 11 | 10 | 1 | AEO/GEO fail (seo-consultant-dhaka) |
| Batch 7 (Technical SEO) | 20 | 9 | 11 | **11 posts lack question headings** |
| Batch 8 (Schema posts) | 13 | 3 | 10 | 5 TF-IDF thin + **9 lack question headings** |
| Batch 9 (Schema+Industry) | 17 | 16 | 1 | Missing Dhaka entity (breadcrumb post) |
| Batch 10 (Case studies) | 20 | 5 | 15 | **15 lack question headings** + 2 TF-IDF thin + 3 low internal links |
| Batch 11 (Service pages) | 9 | 2 | 7 | 2 TF-IDF thin + 4 missing pillar links + 4 low internal links |
| **TOTAL** | **129** | **81** | **48** | |

---

## Posts Requiring Fixes

### 🔴 CRITICAL: Missing Pillar Links (5 posts)
| Post | Issue | Fix |
|------|-------|-----|
| `seo-garments-textile-industry-b2b-lead-generation` | No link to main pillar page or /services/ | Add link to `/blog/complete-seo-guide-bangladesh-businesses-2026` in conclusion |
| `how-to-choose-best-seo-expert-dhaka-15-things` | No link to /services/ | Add service page link |
| `seo-expert-vs-seo-agency-dhaka-which-is-right` | No link to /services/ | Add service page link |
| `what-does-seo-expert-do-guide-business-owners` | No link to /services/ | Add service page link |
| `seo-case-study-dhaka-businesses-increased-organic-traffic` | No link to /services/ | Add service page link |

### 🔴 CRITICAL: AEO/GEO — Insufficient Question Headings (37 posts)
Most common issue across the site. Posts flagged have < 2 question-based headings (How/What/Why/When/Where/Can/Do/Is/Are or Bengali equivalents).

**Batch 7 (11 posts):**
- seo-website-migration-guide-bd, seo-google-analytics-4-bangladesh, seo-competitor-analysis-bangladesh, seo-landing-page-optimization-bd, seo-for-mobile-apps-bangladesh, google-discover-seo-bangladesh, seo-for-podcast-bangladesh, seo-skyscraper-technique-bangladesh, seo-hubspot-vs-wordpress-bd, seo-referral-traffic-bangladesh, seo-search-intent-optimization

**Batch 8 (9 posts):**
- seo-passage-ranking-bangladesh, seo-people-also-ask-optimization, seo-featured-snippet-bangladesh, seo-google-penalty-recovery-bd, seo-https-ssl-impact-bangladesh, seo-redirects-guide-bangladesh, seo-canonical-url-guide-bd, seo-robots-txt-guide-bangladesh, seo-hreflang-guide-bangladesh

**Batch 10 (15 posts):**
- local-seo-multiple-business-locations-bangladesh, seo-photographers-videographers-bangladesh, seo-wedding-event-planners-bangladesh, seo-non-profit-organizations-bangladesh, recovering-google-penalties-bangladesh-guide, building-seo-roadmap-bangladesh-business, why-md-kanok-miah-is-the-best-seo-expert-in-dhaka-bangladesh, locksmith-dundee-seo-case-study, landlord-certificates-seo-case-study, das-taxis-scotland-seo-case-study, morethanpanel-seo-case-study, smmgen-seo-case-study, smmsun-seo-case-study, mir-cement-seo-case-study, dhaka-apparels-seo-case-study, stealth-windshield-repairs-seo-case-study, watchzonebd-seo-case-study

**Other batches:**
- seo-consultant-dhaka-bangladesh (Batch 6)

### 🟡 MODERATE: TF-IDF Keyword Density Too Low (9 posts)
| Post | Keyword | Count | Fix |
|------|---------|-------|-----|
| `seo-trends-2026-ai-geo-future` | ২০২৬ সালের SEO ট্রেন্ডস | 1 | Add 4+ more mentions of the full title phrase |
| `seo-tips-for-business-owners-bd` | SEO টিপস | 2 | Add 3+ more mentions of "SEO টিপস" |
| `seo-people-also-ask-optimization` | পিপল অলসো আস্ক | 1 | Use full Bengali phrase more, not just "PAA" |
| `seo-https-ssl-impact-bangladesh` | HTTPS ও SSL | 2 | Use the combined phrase more |
| `seo-redirects-guide-bangladesh` | রিডাইরেক্ট গাইড | 1 | Use "রিডাইরেক্ট গাইড" more consistently |
| `seo-robots-txt-guide-bangladesh` | রোবটস.টেক্সট | 1 | Use Bengali form more |
| `seo-xml-sitemap-guide-bd` | XML সাইটম্যাপ গাইড | 1 | Use full phrase more consistently |
| `hiring-seo-expert-dhaka-better-roi-than-paid-ads` | SEO Expert | 0 | Content uses "SEO Consultant" — align with title keyword |
| `landlord-certificates-seo-case-study` | Landlord Certificates | 3 | Add 2+ more mentions |

### 🟡 MODERATE: Internal Linking Below Threshold (7 posts)
| Post | Links | Fix |
|------|-------|-----|
| `what-does-seo-expert-do-guide-business-owners` | 2 | Add 1+ more internal links |
| `seo-case-study-dhaka-businesses-increased-organic-traffic` | 2 | Add 1+ more internal links |
| `hiring-seo-expert-dhaka-better-roi-than-paid-ads` | 2 | Add 1+ more internal links |
| `how-to-choose-best-seo-expert-dhaka-15-things` | 2 | Add 1+ more internal links |
| `locksmith-dundee-seo-case-study` | 2 | Add 1+ more internal links |
| `das-taxis-scotland-seo-case-study` | 2 | Add 1+ more internal links |
| `stealth-windshield-repairs-seo-case-study` | 2 | Add 1+ more internal links |

### 🟢 MINOR: Missing Semantic Entities (1 post)
| Post | Missing Entity | Fix |
|------|----------------|-----|
| `seo-breadcrumb-schema-bd` | Dhaka/ঢাকা | Add mention of Dhaka in content or location links |

---

## Overall Statistics

| Check | Total Flags | Posts Checked | Pass Rate |
|-------|------------|---------------|-----------|
| A. TF-IDF Coverage | 9 | 129 | 93.0% |
| B. Semantic Entities | 1 | 129 | 99.2% |
| C. Pillar-Cluster Alignment | 5 | 129 | 96.1% |
| D. AEO/GEO Optimization | 37 | 129 | **71.3%** |
| E. Internal Linking | 7 | 129 | 94.6% |
| F. Schema Ready | 0 | 129 | 100% |
| **Overall (all 6 checks)** | **48** | **129** | **81/129 (62.8%)** |

## Priority Recommendations

1. **🏆 HIGH: Add question-based headings** to 37 posts lacking AEO/GEO optimization (How/What/Why/Where/Can/Do/Is/Are or Bengali equivalents). This is the single biggest gap and directly impacts AI search visibility (Google SGE, ChatGPT, Perplexity).

2. **🏆 HIGH: Fix pillar links** on 5 posts that don't link to /services/ or the main SEO pillar guide.

3. **🏆 MEDIUM: Boost TF-IDF keyword density** in 9 posts where the primary keyword phrase from the title appears fewer than 5 times in the content.

4. **🏆 MEDIUM: Increase internal linking** in 7 posts that have fewer than 3 internal links to related content.

5. **🏆 LOW: Add Dhaka entity** to the breadcrumb schema post.

---

*Report generated by Content Framework Enforcer — kanokmiah.com.bd*
