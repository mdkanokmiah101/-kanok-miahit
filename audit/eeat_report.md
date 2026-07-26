# E-E-A-T Review Report — kanokmiah.com.bd Blog

**Generated:** 2026-07-20
**Total Posts Analyzed:** 128

---

## Scoring Methodology

Each post scored 0-10 across these criteria:

| Criterion | Max Points | How Assessed |
|-----------|-----------|--------------|
| Author Attribution | 2 | Author field set consistently to Kanok Miah / মোঃ কনক মিঞา? Post #64 has a BUG (markdown link in author field) |
| Credentials & Expertise | 2 | Content mentions experience years, certifications, project counts (7+ years, 210+ projects, Google Digital Garage, HubSpot, SEMrush) |
| Freshness | 2 | Post date within last 12 months |
| ArticleSchema | 2 | blog/[slug]/page.js includes <ArticleSchema> component |
| External Citations | 1 | Links to authoritative external sources (Google Search Central, DataReportal, official docs) |
| Author Bio/Photo | 1 | Visible author bio with photo on the blog post page |

---
## Site-Level Schema Audit

**Source:** /root/kanok-miahit/src/components/Schema.js and layout.js

| Schema Type | Present | Location |
|------------|---------|----------|
| **OrganizationSchema** | ✅ | layout.js (global) |
| **LocalBusinessSchema** | ✅ | layout.js (global) |
| **WebSiteSchema** | ✅ | layout.js (global) |
| **PersonSchema** | ✅ | layout.js (global) |
| **ArticleSchema** | ✅ | blog/[slug]/page.js (per post) |
| **BreadcrumbSchema** | ✅ | blog/page.js + blog/[slug]/page.js |
| **FAQSchema** | ✅ | blog/page.js + blog/[slug]/page.js (conditional) |
| **CollectionPageSchema** | ✅ | blog/page.js |
| **ServiceSchema** | ✅ | Service pages (per service) |
| **ContactPageSchema** | ✅ | contact/page.js |
| **AboutPageSchema** | ✅ | about/page.js |
| **AggregateRatingSchema** | ✅ | Schema.js (4.9/5, 108 reviews) |
| **ReviewSchema** | ✅ | Schema.js |
| **ProfessionalServiceSchema** | ✅ | Schema.js |
| **VideoObjectSchema** | ✅ | Schema.js |

**Verification Notes:**
- All 15 schema types are implemented and available
- 4 schemas (Organization, LocalBusiness, WebSite, Person) render globally on every page via layout.js
- ArticleSchema includes proper author (Person), publisher (Organization), datePublished, dateModified, and image
- BreadcrumbList is properly hierarchical on blog posts (Home > Blog > Post Title)
- FAQSchema is only rendered on blog posts that have a `faqs` array in the data — some posts include manual FAQ sections in markdown but may not have structured FAQ data

## Trust Elements Audit

| Element | Status | Details |
|---------|--------|---------|
| Google Search Console verification | ✅ | Meta tag present in layout.js |
| Google Analytics 4 | ✅ | Blog post on GA4 exists (seo-google-analytics-4-bangladesh) |
| Author consistency | ⚠️ | 127/128 posts use consistent name format. Post #64 has BUG: author contains markdown link `[মোঃ কনক মিঞা](/about)` |
| Author bio on blog posts | ❌ | No author bio section visible on blog post pages. Author name shown but no photo, credentials badge, or link to about page |
| Credentials on About page | ✅ | Google Digital Garage, HubSpot Academy, SEMrush Academy displayed as verified badges |
| Review count / Rating | ✅ | AggregateRating schema claims 4.9/5 with 108 reviews |
| Physical address | ✅ | Mirpur, Dhaka — in OrganizationSchema and LocalBusinessSchema |
| SameAs profiles | ✅ | Facebook, LinkedIn, YouTube, Pinterest, Instagram, TikTok, WhatsApp |
| SSL/HTTPS | ✅ | Site references https://kanokmiah.com.bd |
| Content in Bangla + English | ✅ | Bilingual content strategy (40 English + 73 Bangla posts) |
| Case studies with real data | ✅ | 11 case studies with measurable results |
| dateModified field | ⚠️ | Only present in SOME posts (e.g., complete-seo-guide has it, many do not) |

---
## Post-by-Post E-E-A-T Scores

| # | Slug | Score | Missing Elements | Notes |
|---|------|-------|-----------------|-------|
| 1 | complete-seo-guide-bangladesh-businesses-2026 | 9/10 | No author bio/photo on post page | Author name displayed but no photo or bio section |
| 2 | local-seo-tips-dhaka-businesses-google-maps | 9/10 | No author bio/photo on post page | Author name displayed but no photo or bio section |
| 3 | why-ecommerce-store-needs-seo-bangladesh | 9/10 | No author bio/photo on post page | Author name displayed but no photo or bio section |
| 4 | technical-seo-checklist-bangladeshi-websites | 9/10 | No author bio/photo on post page | Author name displayed but no photo or bio section |
| 5 | how-to-choose-right-seo-agency-bangladesh | 9/10 | No author bio/photo on post page | Author name displayed but no photo or bio section |
| 6 | link-building-strategies-bangladesh-market | 9/10 | No author bio/photo on post page | Author name displayed but no photo or bio section |
| 7 | geo-optimization-prepare-business-ai-search | 9/10 | No author bio/photo on post page | Author name displayed but no photo or bio section |
| 8 | seo-garments-textile-industry-b2b-lead-generation | 9/10 | No author bio/photo on post page | Author name displayed but no photo or bio section |
| 9 | google-business-profile-optimization-guide-bangladesh | 9/10 | No author bio/photo on post page | Author name displayed but no photo or bio section |
| 10 | seo-vs-google-ads-whats-best-bangladesh-businesses | 8/10 | No external authoritative citations; No author bio/photo on post page | Author name displayed but no photo or bio section |
| 11 | seo-real-estate-developers-dhaka | 8/10 | No external authoritative citations; No author bio/photo on post page | Author name displayed but no photo or bio section |
| 12 | mobile-seo-optimization-bangladesh-mobile-first-era | 8/10 | No external authoritative citations; No author bio/photo on post page | Author name displayed but no photo or bio section |
| 13 | content-marketing-strategy-bangladeshi-brands-seo | 8/10 | No external authoritative citations; No author bio/photo on post page | Author name displayed but no photo or bio section |
| 14 | international-seo-bangladesh-exporters-global-buyers | 8/10 | No external authoritative citations; No author bio/photo on post page | Author name displayed but no photo or bio section |
| 15 | seo-bangla-beginners-guide-google-ranking | 7/10 | Credentials/experience not mentioned in post content; No external authoritative citations; No author bio/photo on post page | No explicit credentials or experience years visible; Author name displayed but no photo or bio section |
| 16 | local-seo-dhaka-google-maps-ranking | 7/10 | Credentials/experience not mentioned in post content; No external authoritative citations; No author bio/photo on post page | No explicit credentials or experience years visible; Author name displayed but no photo or bio section |
| 17 | seo-trends-2026-ai-geo-future | 7/10 | Credentials/experience not mentioned in post content; No external authoritative citations; No author bio/photo on post page | No explicit credentials or experience years visible; Author name displayed but no photo or bio section |
| 18 | technical-seo-core-web-vitals-optimization | 7/10 | Credentials/experience not mentioned in post content; No external authoritative citations; No author bio/photo on post page | No explicit credentials or experience years visible; Author name displayed but no photo or bio section |
| 19 | ecommerce-seo-daraz-shopify-guide | 7/10 | Credentials/experience not mentioned in post content; No external authoritative citations; No author bio/photo on post page | No explicit credentials or experience years visible; Author name displayed but no photo or bio section |
| 20 | link-building-bangladesh-strategies | 7/10 | Credentials/experience not mentioned in post content; No external authoritative citations; No author bio/photo on post page | No explicit credentials or experience years visible; Author name displayed but no photo or bio section |
| 21 | keyword-research-bangladesh-market | 7/10 | Credentials/experience not mentioned in post content; No external authoritative citations; No author bio/photo on post page | No explicit credentials or experience years visible; Author name displayed but no photo or bio section |
| 22 | content-marketing-seo-friendly-content-writing | 7/10 | Credentials/experience not mentioned in post content; No external authoritative citations; No author bio/photo on post page | No explicit credentials or experience years visible; Author name displayed but no photo or bio section |
| 23 | google-search-console-performance-guide | 7/10 | Credentials/experience not mentioned in post content; No external authoritative citations; No author bio/photo on post page | No explicit credentials or experience years visible; Author name displayed but no photo or bio section |
| 24 | mobile-seo-bangladesh-ranking-strategy | 7/10 | Credentials/experience not mentioned in post content; No external authoritative citations; No author bio/photo on post page | No explicit credentials or experience years visible; Author name displayed but no photo or bio section |
| 25 | schema-markup-rich-snippets-techniques | 7/10 | Credentials/experience not mentioned in post content; No external authoritative citations; No author bio/photo on post page | No explicit credentials or experience years visible; Author name displayed but no photo or bio section |
| 26 | youtube-seo-bangladesh-ranking-tips | 7/10 | Credentials/experience not mentioned in post content; No external authoritative citations; No author bio/photo on post page | No explicit credentials or experience years visible; Author name displayed but no photo or bio section |
| 27 | seo-vs-google-ads-bangladesh-business | 7/10 | Credentials/experience not mentioned in post content; No external authoritative citations; No author bio/photo on post page | No explicit credentials or experience years visible; Author name displayed but no photo or bio section |
| 28 | seo-bangla-blog-content-writing | 8/10 | No external authoritative citations; No author bio/photo on post page | Author name displayed but no photo or bio section |
| 29 | seo-tips-for-business-owners-bd | 7/10 | Credentials/experience not mentioned in post content; No external authoritative citations; No author bio/photo on post page | No explicit credentials or experience years visible; Author name displayed but no photo or bio section |
| 30 | long-tail-keywords-bangladesh | 7/10 | Credentials/experience not mentioned in post content; No external authoritative citations; No author bio/photo on post page | No explicit credentials or experience years visible; Author name displayed but no photo or bio section |
| 31 | seo-for-facebook-marketplace | 7/10 | Credentials/experience not mentioned in post content; No external authoritative citations; No author bio/photo on post page | No explicit credentials or experience years visible; Author name displayed but no photo or bio section |
| 32 | seo-for-youtube-channel-bangla | 7/10 | Credentials/experience not mentioned in post content; No external authoritative citations; No author bio/photo on post page | No explicit credentials or experience years visible; Author name displayed but no photo or bio section |
| 33 | seo-google-updates-2026 | 7/10 | Credentials/experience not mentioned in post content; No external authoritative citations; No author bio/photo on post page | No explicit credentials or experience years visible; Author name displayed but no photo or bio section |
| 34 | seo-semantic-search-bangla | 7/10 | Credentials/experience not mentioned in post content; No external authoritative citations; No author bio/photo on post page | No explicit credentials or experience years visible; Author name displayed but no photo or bio section |
| 35 | seo-for-hotel-resort-bangladesh | 7/10 | Credentials/experience not mentioned in post content; No external authoritative citations; No author bio/photo on post page | No explicit credentials or experience years visible; Author name displayed but no photo or bio section |
| 36 | seo-google-business-profile-posts | 7/10 | Credentials/experience not mentioned in post content; No external authoritative citations; No author bio/photo on post page | No explicit credentials or experience years visible; Author name displayed but no photo or bio section |
| 37 | seo-local-citations-bangladesh | 7/10 | Credentials/experience not mentioned in post content; No external authoritative citations; No author bio/photo on post page | No explicit credentials or experience years visible; Author name displayed but no photo or bio section |
| 38 | seo-for-ngo-bangladesh | 7/10 | Credentials/experience not mentioned in post content; No external authoritative citations; No author bio/photo on post page | No explicit credentials or experience years visible; Author name displayed but no photo or bio section |
| 39 | seo-career-guide-bangladesh-2026 | 8/10 | No external authoritative citations; No author bio/photo on post page | Author name displayed but no photo or bio section |
| 40 | seo-consultant-dhaka-bangladesh | 7/10 | Credentials/experience not mentioned in post content; No external authoritative citations; No author bio/photo on post page | No explicit credentials or experience years visible; Author name displayed but no photo or bio section |
| 41 | google-my-business-optimization-bangladesh | 7/10 | Credentials/experience not mentioned in post content; No external authoritative citations; No author bio/photo on post page | No explicit credentials or experience years visible; Author name displayed but no photo or bio section |
| 42 | seo-for-new-website-bangladesh | 7/10 | Credentials/experience not mentioned in post content; No external authoritative citations; No author bio/photo on post page | No explicit credentials or experience years visible; Author name displayed but no photo or bio section |
| 43 | website-speed-optimization-bangladesh | 7/10 | Credentials/experience not mentioned in post content; No external authoritative citations; No author bio/photo on post page | No explicit credentials or experience years visible; Author name displayed but no photo or bio section |
| 44 | seo-audit-checklist-bangladesh | 7/10 | Credentials/experience not mentioned in post content; No external authoritative citations; No author bio/photo on post page | No explicit credentials or experience years visible; Author name displayed but no photo or bio section |
| 45 | affiliate-seo-bangladesh | 7/10 | Credentials/experience not mentioned in post content; No external authoritative citations; No author bio/photo on post page | No explicit credentials or experience years visible; Author name displayed but no photo or bio section |
| 46 | voice-search-seo-bangladesh | 8/10 | No external authoritative citations; No author bio/photo on post page | Author name displayed but no photo or bio section |
| 47 | seo-legal-compliance-bangladesh | 7/10 | Credentials/experience not mentioned in post content; No external authoritative citations; No author bio/photo on post page | No explicit credentials or experience years visible; Author name displayed but no photo or bio section |
| 48 | seo-for-restaurants-cafe-dhaka | 7/10 | Credentials/experience not mentioned in post content; No external authoritative citations; No author bio/photo on post page | No explicit credentials or experience years visible; Author name displayed but no photo or bio section |
| 49 | seo-for-cleaning-services-bangladesh | 7/10 | Credentials/experience not mentioned in post content; No external authoritative citations; No author bio/photo on post page | No explicit credentials or experience years visible; Author name displayed but no photo or bio section |
| 50 | seo-dashboard-tools-bangladesh | 7/10 | Credentials/experience not mentioned in post content; No external authoritative citations; No author bio/photo on post page | No explicit credentials or experience years visible; Author name displayed but no photo or bio section |
| 51 | seo-mistakes-to-avoid-bangladesh | 8/10 | No external authoritative citations; No author bio/photo on post page | Author name displayed but no photo or bio section |
| 52 | seo-website-migration-guide-bd | 7/10 | Credentials/experience not mentioned in post content; No external authoritative citations; No author bio/photo on post page | No explicit credentials or experience years visible; Author name displayed but no photo or bio section |
| 53 | google-tag-manager-seo-bd | 7/10 | Credentials/experience not mentioned in post content; No external authoritative citations; No author bio/photo on post page | No explicit credentials or experience years visible; Author name displayed but no photo or bio section |
| 54 | seo-google-analytics-4-bangladesh | 7/10 | Credentials/experience not mentioned in post content; No external authoritative citations; No author bio/photo on post page | No explicit credentials or experience years visible; Author name displayed but no photo or bio section |
| 55 | seo-keyword-clustering-bangladesh | 8/10 | No external authoritative citations; No author bio/photo on post page | Author name displayed but no photo or bio section |
| 56 | seo-competitor-analysis-bangladesh | 8/10 | No external authoritative citations; No author bio/photo on post page | Author name displayed but no photo or bio section |
| 57 | seo-landing-page-optimization-bd | 7/10 | Credentials/experience not mentioned in post content; No external authoritative citations; No author bio/photo on post page | No explicit credentials or experience years visible; Author name displayed but no photo or bio section |
| 58 | seo-for-mobile-apps-bangladesh | 7/10 | Credentials/experience not mentioned in post content; No external authoritative citations; No author bio/photo on post page | No explicit credentials or experience years visible; Author name displayed but no photo or bio section |
| 59 | google-discover-seo-bangladesh | 7/10 | Credentials/experience not mentioned in post content; No external authoritative citations; No author bio/photo on post page | No explicit credentials or experience years visible; Author name displayed but no photo or bio section |
| 60 | seo-for-podcast-bangladesh | 7/10 | Credentials/experience not mentioned in post content; No external authoritative citations; No author bio/photo on post page | No explicit credentials or experience years visible; Author name displayed but no photo or bio section |
| 61 | seo-pillar-content-strategy-bd | 8/10 | No external authoritative citations; No author bio/photo on post page | Author name displayed but no photo or bio section |
| 62 | seo-skyscraper-technique-bangladesh | 7/10 | Credentials/experience not mentioned in post content; No external authoritative citations; No author bio/photo on post page | No explicit credentials or experience years visible; Author name displayed but no photo or bio section |
| 63 | seo-content-repurposing-bangladesh | 7/10 | Credentials/experience not mentioned in post content; No external authoritative citations; No author bio/photo on post page | No explicit credentials or experience years visible; Author name displayed but no photo or bio section |
| 64 | seo-hubspot-vs-wordpress-bd | 6/10 | Author attribution (BUG: markdown link in author field); No external authoritative citations; No author bio/photo on post page | BUG: author='[মোঃ কনক মিঞা](/about)' contains markdown syntax; Author name displayed but no photo or bio section |
| 65 | seo-domain-authority-bangladesh | 7/10 | Credentials/experience not mentioned in post content; No external authoritative citations; No author bio/photo on post page | No explicit credentials or experience years visible; Author name displayed but no photo or bio section |
| 66 | seo-page-authority-bangladesh | 7/10 | Credentials/experience not mentioned in post content; No external authoritative citations; No author bio/photo on post page | No explicit credentials or experience years visible; Author name displayed but no photo or bio section |
| 67 | seo-referral-traffic-bangladesh | 7/10 | Credentials/experience not mentioned in post content; No external authoritative citations; No author bio/photo on post page | No explicit credentials or experience years visible; Author name displayed but no photo or bio section |
| 68 | seo-direct-traffic-bangladesh | 7/10 | Credentials/experience not mentioned in post content; No external authoritative citations; No author bio/photo on post page | No explicit credentials or experience years visible; Author name displayed but no photo or bio section |
| 69 | seo-branded-vs-non-branded-bd | 7/10 | Credentials/experience not mentioned in post content; No external authoritative citations; No author bio/photo on post page | No explicit credentials or experience years visible; Author name displayed but no photo or bio section |
| 70 | seo-search-intent-optimization | 7/10 | Credentials/experience not mentioned in post content; No external authoritative citations; No author bio/photo on post page | No explicit credentials or experience years visible; Author name displayed but no photo or bio section |
| 71 | seo-information-gain-optimization | 7/10 | Credentials/experience not mentioned in post content; No external authoritative citations; No author bio/photo on post page | No explicit credentials or experience years visible; Author name displayed but no photo or bio section |
| 72 | seo-passage-ranking-bangladesh | 7/10 | Credentials/experience not mentioned in post content; No external authoritative citations; No author bio/photo on post page | No explicit credentials or experience years visible; Author name displayed but no photo or bio section |
| 73 | seo-people-also-ask-optimization | 7/10 | Credentials/experience not mentioned in post content; No external authoritative citations; No author bio/photo on post page | No explicit credentials or experience years visible; Author name displayed but no photo or bio section |
| 74 | seo-featured-snippet-bangladesh | 7/10 | Credentials/experience not mentioned in post content; No external authoritative citations; No author bio/photo on post page | No explicit credentials or experience years visible; Author name displayed but no photo or bio section |
| 75 | seo-knowledge-panel-bangladesh | 7/10 | Credentials/experience not mentioned in post content; No external authoritative citations; No author bio/photo on post page | No explicit credentials or experience years visible; Author name displayed but no photo or bio section |
| 76 | seo-zero-click-search-bangladesh | 7/10 | Credentials/experience not mentioned in post content; No external authoritative citations; No author bio/photo on post page | No explicit credentials or experience years visible; Author name displayed but no photo or bio section |
| 77 | seo-google-penalty-recovery-bd | 7/10 | Credentials/experience not mentioned in post content; No external authoritative citations; No author bio/photo on post page | No explicit credentials or experience years visible; Author name displayed but no photo or bio section |
| 78 | seo-https-ssl-impact-bangladesh | 7/10 | Credentials/experience not mentioned in post content; No external authoritative citations; No author bio/photo on post page | No explicit credentials or experience years visible; Author name displayed but no photo or bio section |
| 79 | seo-redirects-guide-bangladesh | 7/10 | Credentials/experience not mentioned in post content; No external authoritative citations; No author bio/photo on post page | No explicit credentials or experience years visible; Author name displayed but no photo or bio section |
| 80 | seo-canonical-url-guide-bd | 7/10 | Credentials/experience not mentioned in post content; No external authoritative citations; No author bio/photo on post page | No explicit credentials or experience years visible; Author name displayed but no photo or bio section |
| 81 | seo-robots-txt-guide-bangladesh | 7/10 | Credentials/experience not mentioned in post content; No external authoritative citations; No author bio/photo on post page | No explicit credentials or experience years visible; Author name displayed but no photo or bio section |
| 82 | seo-xml-sitemap-guide-bd | 7/10 | Credentials/experience not mentioned in post content; No external authoritative citations; No author bio/photo on post page | No explicit credentials or experience years visible; Author name displayed but no photo or bio section |
| 83 | seo-hreflang-guide-bangladesh | 7/10 | Credentials/experience not mentioned in post content; No external authoritative citations; No author bio/photo on post page | No explicit credentials or experience years visible; Author name displayed but no photo or bio section |
| 84 | seo-structured-data-guide-bd | 7/10 | Credentials/experience not mentioned in post content; No external authoritative citations; No author bio/photo on post page | No explicit credentials or experience years visible; Author name displayed but no photo or bio section |
| 85 | seo-json-ld-schema-bangladesh | 7/10 | Credentials/experience not mentioned in post content; No external authoritative citations; No author bio/photo on post page | No explicit credentials or experience years visible; Author name displayed but no photo or bio section |
| 86 | seo-breadcrumb-schema-bd | 7/10 | Credentials/experience not mentioned in post content; No external authoritative citations; No author bio/photo on post page | No explicit credentials or experience years visible; Author name displayed but no photo or bio section |
| 87 | seo-faq-schema-bangladesh | 7/10 | Credentials/experience not mentioned in post content; No external authoritative citations; No author bio/photo on post page | No explicit credentials or experience years visible; Author name displayed but no photo or bio section |
| 88 | seo-howto-schema-bangladesh | 7/10 | Credentials/experience not mentioned in post content; No external authoritative citations; No author bio/photo on post page | No explicit credentials or experience years visible; Author name displayed but no photo or bio section |
| 89 | seo-for-startups-bangladesh | 8/10 | No external authoritative citations; No author bio/photo on post page | Author name displayed but no photo or bio section |
| 90 | b2b-lead-generation-seo-bangladesh | 8/10 | No external authoritative citations; No author bio/photo on post page | Author name displayed but no photo or bio section |
| 91 | seo-for-law-firms-bangladesh | 8/10 | No external authoritative citations; No author bio/photo on post page | Author name displayed but no photo or bio section |
| 92 | seo-for-fitness-gyms-bangladesh | 8/10 | No external authoritative citations; No author bio/photo on post page | Author name displayed but no photo or bio section |
| 93 | seo-services-cost-bangladesh-pricing-guide | 8/10 | No external authoritative citations; No author bio/photo on post page | Author name displayed but no photo or bio section |
| 94 | seo-vs-ppc-advertising-bangladesh | 8/10 | No external authoritative citations; No author bio/photo on post page | Author name displayed but no photo or bio section |
| 95 | how-to-track-measure-seo-roi-bangladesh | 8/10 | No external authoritative citations; No author bio/photo on post page | Author name displayed but no photo or bio section |
| 96 | seo-healthcare-medical-clinics-bangladesh | 8/10 | No external authoritative citations; No author bio/photo on post page | Author name displayed but no photo or bio section |
| 97 | seo-educational-institutions-bangladesh | 8/10 | No external authoritative citations; No author bio/photo on post page | Author name displayed but no photo or bio section |
| 98 | seo-travel-tourism-bangladesh | 8/10 | No external authoritative citations; No author bio/photo on post page | Author name displayed but no photo or bio section |
| 99 | seo-event-management-companies-bangladesh | 8/10 | No external authoritative citations; No author bio/photo on post page | Author name displayed but no photo or bio section |
| 100 | seo-real-estate-agents-property-developers-bangladesh | 8/10 | No external authoritative citations; No author bio/photo on post page | Author name displayed but no photo or bio section |
| 101 | local-seo-multiple-business-locations-bangladesh | 8/10 | No external authoritative citations; No author bio/photo on post page | Author name displayed but no photo or bio section |
| 102 | enterprise-seo-large-organizations-bangladesh | 8/10 | No external authoritative citations; No author bio/photo on post page | Author name displayed but no photo or bio section |
| 103 | seo-photographers-videographers-bangladesh | 8/10 | No external authoritative citations; No author bio/photo on post page | Author name displayed but no photo or bio section |
| 104 | seo-wedding-event-planners-bangladesh | 8/10 | No external authoritative citations; No author bio/photo on post page | Author name displayed but no photo or bio section |
| 105 | blogging-strategy-seo-frequency-topics-bangladesh | 8/10 | No external authoritative citations; No author bio/photo on post page | Author name displayed but no photo or bio section |
| 106 | backlink-outreach-templates-strategies-bangladesh | 8/10 | No external authoritative citations; No author bio/photo on post page | Author name displayed but no photo or bio section |
| 107 | seo-non-profit-organizations-bangladesh | 8/10 | No external authoritative citations; No author bio/photo on post page | Author name displayed but no photo or bio section |
| 108 | recovering-google-penalties-bangladesh-guide | 8/10 | No external authoritative citations; No author bio/photo on post page | Author name displayed but no photo or bio section |
| 109 | building-seo-roadmap-bangladesh-business | 8/10 | No external authoritative citations; No author bio/photo on post page | Author name displayed but no photo or bio section |
| 110 | voice-search-seo-bengali-bangladesh | 8/10 | No external authoritative citations; No author bio/photo on post page | Author name displayed but no photo or bio section |
| 111 | why-md-kanok-miah-is-the-best-seo-expert-in-dhaka-bangladesh | 8/10 | No external authoritative citations; No author bio/photo on post page | Author name displayed but no photo or bio section |
| 112 | locksmith-dundee-seo-case-study | 8/10 | No external authoritative citations; No author bio/photo on post page | Author name displayed but no photo or bio section |
| 113 | landlord-certificates-seo-case-study | 8/10 | No external authoritative citations; No author bio/photo on post page | Author name displayed but no photo or bio section |
| 114 | das-taxis-scotland-seo-case-study | 8/10 | No external authoritative citations; No author bio/photo on post page | Author name displayed but no photo or bio section |
| 115 | morethanpanel-seo-case-study | 8/10 | No external authoritative citations; No author bio/photo on post page | Author name displayed but no photo or bio section |
| 116 | smmgen-seo-case-study | 8/10 | No external authoritative citations; No author bio/photo on post page | Author name displayed but no photo or bio section |
| 117 | smmsun-seo-case-study | 8/10 | No external authoritative citations; No author bio/photo on post page | Author name displayed but no photo or bio section |
| 118 | mir-cement-seo-case-study | 8/10 | No external authoritative citations; No author bio/photo on post page | Author name displayed but no photo or bio section |
| 119 | dhaka-apparels-seo-case-study | 8/10 | No external authoritative citations; No author bio/photo on post page | Author name displayed but no photo or bio section |
| 120 | stealth-windshield-repairs-seo-case-study | 8/10 | No external authoritative citations; No author bio/photo on post page | Author name displayed but no photo or bio section |
| 121 | how-to-choose-best-seo-expert-dhaka-15-things | 8/10 | No external authoritative citations; No author bio/photo on post page | Author name displayed but no photo or bio section |
| 122 | seo-expert-vs-seo-agency-dhaka-which-is-right | 8/10 | No external authoritative citations; No author bio/photo on post page | Author name displayed but no photo or bio section |
| 123 | top-10-seo-mistakes-dhaka-businesses-fix | 8/10 | No external authoritative citations; No author bio/photo on post page | Author name displayed but no photo or bio section |
| 124 | what-does-seo-expert-do-guide-business-owners | 8/10 | No external authoritative citations; No author bio/photo on post page | Author name displayed but no photo or bio section |
| 125 | seo-case-study-dhaka-businesses-increased-organic-traffic | 8/10 | No external authoritative citations; No author bio/photo on post page | Author name displayed but no photo or bio section |
| 126 | hiring-seo-expert-dhaka-better-roi-than-paid-ads | 8/10 | No external authoritative citations; No author bio/photo on post page | Author name displayed but no photo or bio section |
| 127 | ai-seo-2026-dhaka-experts-optimize-google-ai-chatgpt | 8/10 | No external authoritative citations; No author bio/photo on post page | Author name displayed but no photo or bio section |
| 128 | watchzonebd-seo-case-study | 8/10 | No external authoritative citations; No author bio/photo on post page | Author name displayed but no photo or bio section |

---
## Score Distribution

| ≤3/10 | 0 posts |  |
| 9/10 | 9 posts | █████████ |
| 8/10 | 52 posts | ████████████████████████████████████████████████████ |
| 7/10 | 66 posts | ██████████████████████████████████████████████████████████████████ |
| 6/10 | 1 posts | █ |
| 5/10 | 0 posts |  |
| 4/10 | 0 posts |  |
| 10/10 | 0 posts |  |

**Average E-E-A-T Score:** 7.5/10
**Median E-E-A-T Score:** 7/10
**Posts scoring < 5:** 0
**Posts scoring 8+:** 61

---
## Critical Issues Found

### 1. Author Field Bug (Post #64)
- **Post:** seo-hubspot-vs-wordpress-bd
- **Current:** `author: "[মোঃ কনক মিঞা](/about)"`
- **Expected:** `author: "মোঃ কনক মিঞা"`
- **Impact:** High — author name renders with broken markdown syntax on the live page, undercuts E-E-A-T on author credibility

### 2. Missing Author Bio on Blog Posts
- **Issue:** Blog post pages display the author name but have NO author bio section, photo, credentials badge, or link to /about
- **Impact:** Medium — Google's E-E-A-T guidelines recommend showing author expertise and biography alongside content
- **Fix:** Add an author bio component below each post with photo, credentials (Google Digital Garage, HubSpot, SEMrush), and a link to /about

### 3. Inconsistent dateModified Field
- **Issue:** Only some posts have a `dateModified` field in data.js. Others only have `date`.
- **Impact:** Low-Medium — ArticleSchema uses dateModified || date as fallback, so schema is valid, but inconsistent data could cause update signals to be missed
- **Fix:** Add dateModified to all posts, ideally matching the last edit date

### 4. No Author Schema on Blog Posts
- **Issue:** ArticleSchema includes author as `Person` with name and url, but there is no separate Author schema markup or `sameAs` for the author entity
- **Impact:** Low — ArticleSchema author markup is adequate but adding a separate Author markup with social profiles would strengthen entity signals

