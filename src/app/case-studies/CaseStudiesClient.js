"use client";

import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import Link from "next/link";
import { FAQSchema } from "@/components/Schema";

const caseStudies = [
  {
    metric: "58,466",
    label: "Daily Visitors",
    name: "MoreThanPanel",
    industry: "SMM Panel",
    image: "/images/case-studies/SMMGen-2.webp",
    challenge: "Despite having 227,000 registered users, MoreThanPanel generated only 1,700 monthly organic visitors. The site had thin templated service pages, zero blog content, slow page speed (LCP 4.2s), duplicate meta data, weak internal linking, and no content topic architecture despite a domain authority of 31.",
    solution: "A sequenced 3-phase roadmap over 24 months: (1) Technical stability — page speed optimization (WebP, lazy loading), content differentiation, internal linking architecture, URL cleanup, meta tag standardization; (2) Structured content engine — launched blog with topic clusters (SMM comparisons, algorithm insights, growth strategies), expanded service pages with FAQs and semantic keywords; (3) Scaling and compounding — quarterly content refresh cycles, meta description optimization for CTR, voice search optimization, and conversational AI targeting.",
    results: [
      "58,466 daily organic visitors (from 1,700/mo)",
      "306,000 total clicks over 24 months",
      "6,450,000 total impressions",
      "6.2% CTR (last 3 months)",
      "60%+ reduction in indexing errors",
      "$0 ad spend (100% Organic SEO)",
    ],
    url: "/blog/morethanpanel-seo-case-study",
    website: "https://morethanpanel.com",
    emoji: "🚀",
  },
  {
    metric: "27,900",
    label: "Monthly Clicks",
    name: "SMMGen",
    industry: "SMM Panel",
    image: "/images/case-studies/SMMGen-2.webp",
    challenge: "SMMGen was generating only 32 monthly organic clicks with only 4 ranking keywords. The site suffered from poor mobile experience (70%+ buyers browse on phones), generic thin content (150–300 words per page), confusing service structure mixing platforms together, and zero trust signals in a fiercely competitive SMM panel industry.",
    solution: "Executed a 3-phase no-shortcuts strategy: (1) Complete technical audit (47 issues fixed), reverse-engineered top 20 competitors, intent-based keyword mapping (500+ terms), complete content overhaul with proven template (introduction, how it works, delivery details, pricing, FAQ, CTA); (2) Content expansion — published 28 in-depth buyer guides, moved from 1 broad service page to 12 individual optimized pages; (3) Authority building through ethical link acquisition.",
    results: [
      "27,900 monthly organic clicks (from 32)",
      "129,000 monthly impressions",
      "500+ ranking keywords (from 4)",
      "340% increase in indexed pages",
      "Core Web Vitals: Poor → Good",
      "$0 ad spend (100% Organic SEO)",
    ],
    url: "/blog/smmgen-seo-case-study",
    website: "https://smmgen.com",
    emoji: "📈",
  },
  {
    metric: "#1",
    label: "Rank in 90 Days",
    name: "Dhaka Apparels",
    industry: "B2B Garments Sourcing",
    image: "/images/case-studies/WatchZoneBD-.webp",
    challenge: "Brand new domain with zero authority, zero indexed pages, zero backlinks, no Google Business Profile — competing against established garments suppliers with 5+ years of SEO history, hundreds of pages, and strong backlink profiles in Bangladesh's $50B+ RMG sector.",
    solution: "5-phase structured plan: (1) Lead-generation website built with under 200ms server response, under 2s mobile load; (2) Content addressing real B2B buyer objections (MOQ, export docs, quality grading), dedicated pages per service category; (3) Full schema markup (Organization + Product), Core Web Vitals all Good; (4) Fully optimized GBP with real photos; (5) Selective contextual backlinks from trade directories only.",
    results: [
      "#1 for 'best stock garments supplier in bd'",
      "14,700 impressions in 90 days",
      "Featured in Google AI-generated search summaries",
      "$0 ad spend",
    ],
    url: "/blog/dhaka-apparels-seo-case-study",
    emoji: "🏆",
  },
  {
    metric: "15,440%",
    label: "Traffic Growth",
    name: "SMMSun",
    industry: "SMM Panel",
    image: "/images/case-studies/SMMSun-2.webp",
    challenge: "Only ~50 monthly organic clicks, just 2 low-value keywords ranking, thin generic content (150–200 words per page), and minimal trust signals in a crowded SMM panel market with hundreds of established competitors.",
    solution: "4-phase strategy: (1) Mapped 120+ search terms across 4 intent categories, rebuilt homepage around Best Affordable SMM Panel, created dedicated service pages per platform, FAQ section, schema markup; (2) On-page SEO — internal linking hub-and-spoke model, Core Web Vitals (LCP: 4.2s → 1.8s), mobile-first UX; (3) Content expansion with pillar pages and supporting articles; (4) E-E-A-T building through topical authority.",
    results: [
      "7,700+ monthly organic clicks (from ~50)",
      "15,440% traffic growth",
      "14.2% CTR (double industry average)",
      "LCP: 4.2s → 1.8s",
      "75%+ mobile traffic share",
      "$0 ad spend",
    ],
    url: "/blog/smmsun-seo-case-study",
    website: "https://smmsun.com",
    emoji: "🔥",
  },
  {
    metric: "5,853%",
    label: "Organic Growth",
    name: "Das Taxis Scotland",
    industry: "Transportation",
    image: "/images/case-studies/Das-Taxi.webp",
    challenge: "Das Taxis Scotland had a basic non-SEO website, no local SEO strategy, an unclaimed Google Business Profile, zero blog content, and only 2 referring domains. The business generated ~15 monthly organic visitors with only 3 keywords in the top 100.",
    solution: "4-phase organic strategy: (1) SEO-first website rebuild with 12 core service pages, schema markup, Search Console integration; (2) Comprehensive keyword research identifying 600+ local search terms with intent-based categorization; (3) 30+ pages of optimized content including local landing pages for Dunfermline, Rosyth, Kirkcaldy; (4) GBP optimization, 30+ local citations, review generation (25+ reviews, 4.7★).",
    results: [
      "893 monthly visitors (from ~15)",
      "636 keywords in top 100 (from 3)",
      "28 keywords in top 10",
      "5,247 total clicks (7 months)",
      "48,300 total impressions (7 months)",
      "Average position: 75+ → 18.3",
    ],
    url: "/blog/das-taxis-scotland-seo-case-study",
    website: "https://www.dastaxis.co.uk/",
    emoji: "💪",
  },
  {
    metric: "1,000+",
    label: "Monthly Visitors",
    name: "Locksmith Dundee",
    industry: "Locksmith Services",
    image: "/images/case-studies/Das-Taxi.webp",
    challenge: "Zero organic rankings, no claimed Google Business Profile, a single generic page with under 150 words of content, no citations/directory listings, and zero online reviews. Did not appear in the top 100 for any relevant keyword.",
    solution: "4-pillar local SEO: (1) GBP optimization with 30+ photos, service menu with pricing, weekly posts; (2) 6 dedicated service pages (1,000–1,500 words each) targeting specific high-intent keywords; (3) 40+ local citations across UK directories; (4) Review generation workflow to build local ranking signals.",
    results: [
      "1,000+ monthly organic visitors (6 months)",
      "40+ local citations built",
      "Top 3 rankings for key terms",
      "GBP fully optimized with 30+ photos",
      "$0 ad spend",
    ],
    url: "/blog/locksmith-dundee-seo-case-study",
    website: "https://locksmithdundee.scot/",
    emoji: "🎯",
  },
  {
    metric: "500+",
    label: "Monthly Visitors",
    name: "Mir Cement",
    industry: "B2B Construction Materials",
    image: "/images/case-studies/Master-racks.webp",
    challenge: "Zero organic rankings for competitive terms like 'cement price Bangladesh'. Thin product pages under 150 words, no local landing pages despite nationwide coverage, no B2B citation presence on any Bangladesh directory, no blog/content marketing.",
    solution: "5-pillar B2B SEO: (1) 3-tier keyword research (transactional, brand/category, informational); (2) Product pages rewritten to 1,200–1,500 words with technical specs, brand comparison guides, localized blog content; (3) Full on-page SEO; (4) Organization, Product, FAQ, Breadcrumb, LocalBusiness schema; (5) 40+ B2B citations on Bangladesh-specific directories with 100% NAP consistency.",
    results: [
      "500+ monthly organic visitors (from 0)",
      "12+ keywords in top 10",
      "80+ keywords in top 50",
      "8,000+ GBP views/month",
      "40+ GBP enquiries/month",
      "Page speed: 6.8s → 2.1s",
    ],
    url: "/blog/mir-cement-seo-case-study",
    emoji: "🏗️",
  },
  {
    metric: "400+",
    label: "Monthly Visitors",
    name: "Stealth Windshield Repairs",
    industry: "Auto Glass Repair",
    image: "/images/case-studies/Allseal-Waterproofing-.webp",
    challenge: "Zero organic visitors, unclaimed GBP, no citations on any directory, zero Google reviews, no location-specific pages, no content engine. Site loaded in 6.2 seconds with no SEO foundation.",
    solution: "4-phase local SEO: (1) Complete rebuild (6.2s → 1.4s), dedicated location pages for Edinburgh/Glasgow/Fife with LocalBusiness schema; (2) GBP optimization (35 photos, categories, service area); (3) 30+ local citations; (4) Review generation via SMS/email follow-up and QR codes in service van, achieving 38 reviews at 4.9★.",
    results: [
      "400+ monthly visitors (6 months)",
      "38 Google reviews (4.9★ average)",
      "2,800+ GBP impressions/month",
      "30+ local citations",
      "Page speed: 6.2s → 1.4s",
      "£0 ad spend (100% Organic SEO)",
    ],
    url: "/blog/stealth-windshield-repairs-seo-case-study",
    website: "https://stealthwindshieldrepairs.com/",
    emoji: "🚗",
  },
  {
    metric: "200+",
    label: "Monthly Leads",
    name: "All Landlord Certificates UK",
    industry: "Property Safety Certificates",
    image: "/images/case-studies/Allseal-Waterproofing-.webp",
    challenge: "Zero organic rankings, no local landing pages despite serving multiple UK cities, generic service descriptions under 200 words, no citation presence on UK property directories, significant technical SEO gaps.",
    solution: "Service pages rewritten to 1,200–1,800 words with FAQ sections, real cost breakdowns, legal requirement explanations; dedicated local landing pages for major UK cities (London, Manchester, Birmingham, etc.) with city-specific content; aggressive citation building on UK property directories and GBP optimization.",
    results: [
      "200+ monthly organic leads (5 months)",
      "Multi-city landing pages across UK",
      "Service pages: 1,200–1,800 words each",
      "Citation presence on UK directories",
      "100% Organic SEO",
    ],
    url: "/blog/landlord-certificates-seo-case-study",
    emoji: "📋",
  },
];

const results = [
  { name: "Das Taxis", img: "/images/case-studies/Das-Taxi.webp", industry: "Transportation", url: "https://www.dastaxis.co.uk/" },
  { name: "WatchZoneBD", img: "/images/case-studies/WatchZoneBD-.webp", industry: "E-commerce", url: "https://watchzonebd.com" },
  { name: "SMMGen", img: "/images/case-studies/SMMGen-2.webp", industry: "SMM Panel", url: "https://smmgen.com" },
  { name: "SMMSun", img: "/images/case-studies/SMMSun-2.webp", industry: "SMM Panel", url: "https://smmsun.com" },
  { name: "Allseal Waterproofing Pte Ltd.", img: "/images/case-studies/Allseal-Waterproofing-.webp", industry: "Construction", url: "https://allsealwaterproofing.com.sg/" },
  { name: "Stealth Windshield Repairs", img: "/images/case-studies/stealth-windshield.webp", industry: "Auto Glass", url: "https://stealthwindshieldrepairs.com/" },
  { name: "Locksmith Dundee", img: "/images/case-studies/Das-Taxi.webp", industry: "Locksmith", url: "https://locksmithdundee.scot/" },
  { name: "MoreThanPanel", img: "/images/case-studies/SMMGen-2.webp", industry: "SMM Panel", url: "https://morethanpanel.com" },
  { name: "Master Racks Limited", img: "/images/case-studies/Master-racks.webp", industry: "Industrial", url: "https://masterracksltd.com/" },
];

export default function CaseStudiesClient() {
  const featured = caseStudies[2]; // Dhaka Apparels — #1 in 90 days
  const remaining = caseStudies.filter((_, i) => i !== 2);

  return (
    <div className="min-h-screen bg-white text-gray-900">
      <Navbar />

      {/* === HERO === */}
      <section className="relative pt-32 pb-16 px-4 overflow-hidden">
        <div className="absolute top-1/3 -left-32 w-96 h-96 bg-primary/20 rounded-full blur-3xl animate-pulse" />
        <div className="absolute bottom-1/4 -right-32 w-80 h-80 bg-primary/20 rounded-full blur-3xl" />
        <div className="relative max-w-5xl mx-auto text-center">
          <div className="inline-flex items-center gap-2 bg-primary-light border border-primary/20 text-primary text-xs font-semibold px-5 py-2 rounded-full mb-6">
            <span className="w-2 h-2 bg-primary rounded-full animate-pulse" />
            Proven Results — 210+ SEO Campaigns
          </div>
          <h1 className="text-4xl md:text-6xl lg:text-7xl font-extrabold tracking-tight leading-[1.05] mb-6">
            SEO Case <span className="text-primary">Studies</span>
          </h1>
          <p className="text-lg md:text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed mb-10">
            Every number tells a story. Explore our real SEO campaigns — from local Dhaka businesses to international brands — with the exact strategies and measurable results by a proven <Link href="/" className="text-primary font-semibold hover:underline">SEO expert in Bangladesh</Link>.
          </p>
          <div className="flex flex-wrap justify-center gap-4 text-sm">
            <span className="bg-primary/10 text-primary font-bold px-5 py-2.5 rounded-full">210+ Projects</span>
            <span className="bg-primary/10 text-primary font-bold px-5 py-2.5 rounded-full">58K+ Daily Visitors</span>
            <span className="bg-primary/10 text-primary font-bold px-5 py-2.5 rounded-full">15,440% Max Growth</span>
            <span className="bg-primary/10 text-primary font-bold px-5 py-2.5 rounded-full">$0 Ad Spend</span>
          </div>
        </div>
      </section>

      {/* === RESULTS GALLERY === */}
      <section className="py-16 px-4">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <span className="text-primary text-sm font-semibold tracking-[0.2em] uppercase">Results Gallery</span>
            <h2 className="text-3xl md:text-5xl font-extrabold mt-4 mb-4 text-gray-900">SEO Results & <span className="text-primary">Success Stories</span></h2>
            <p className="text-gray-500 max-w-2xl mx-auto text-lg">Real screenshots from live campaigns — every number is a verified outcome, not a promise.</p>
          </div>
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
            {results.map((r, i) => (
              <a key={i} href={r.url} target="_blank" rel="noopener noreferrer" className="group bg-white rounded-2xl border border-gray-100 overflow-hidden hover:border-primary/20 hover:shadow-xl hover:-translate-y-1 transition-all duration-300">
                <div className="relative h-[180px] bg-gray-50 flex items-center justify-center overflow-hidden">
                  <img src={r.img} alt={`${r.name} Website`} className="w-full h-full object-contain p-3 group-hover:scale-105 transition-transform duration-500" loading="lazy" />
                  <span className="absolute top-3 right-3 bg-primary/85 text-white text-[10px] font-bold uppercase tracking-wider px-2.5 py-1 rounded-full">{r.industry}</span>
                </div>
                <div className="p-5">
                  <div className="font-bold text-primary mb-1 text-base">{r.name}</div>
                  <span className="text-xs text-gray-400">Visit Website →</span>
                </div>
              </a>
            ))}
          </div>
        </div>
      </section>

      {/* === FEATURED CASE STUDY === */}
      <section className="py-16 px-4 bg-gray-50/80">
        <div className="max-w-5xl mx-auto">
          <div className="text-center mb-12">
            <span className="text-primary text-sm font-semibold tracking-[0.2em] uppercase">Featured Case Study</span>
            <h2 className="text-3xl md:text-5xl font-extrabold mt-4 mb-4 text-gray-900">The <span className="text-primary">#1 Ranking</span> Story</h2>
          </div>
          <div className="bg-white rounded-2xl border border-primary/10 overflow-hidden hover:shadow-xl transition-all">
            <div className="bg-gradient-to-r from-primary to-primary-dark text-white text-xs font-bold uppercase tracking-wider px-6 py-2.5">🏆 Featured Case Study</div>
            <div className="p-6 md:p-8 grid md:grid-cols-2 gap-6 items-start">
              <div>
                <div className="text-4xl md:text-5xl font-extrabold text-primary">{featured.metric}</div>
                <div className="text-gray-500 text-sm font-medium mb-3">{featured.label} · {featured.name}</div>
                <h3 className="text-2xl font-extrabold mb-4">{featured.emoji} {featured.website ? <a href={featured.website} target="_blank" rel="noopener noreferrer" className="hover:underline text-primary">{featured.name}</a> : featured.name} — {featured.industry}</h3>
                <div className="mb-4">
                  <h4 className="text-xs font-bold uppercase tracking-wider text-primary mb-1">📋 The Challenge</h4>
                  <p className="text-gray-600 text-sm leading-relaxed break-words">{featured.challenge}</p>
                </div>
                <div className="mb-4">
                  <h4 className="text-xs font-bold uppercase tracking-wider text-primary mb-1">💡 The Strategy</h4>
                  <p className="text-gray-600 text-sm leading-relaxed break-words">{featured.solution}</p>
                </div>
                <div className="mb-5">
                  <h4 className="text-xs font-bold uppercase tracking-wider text-primary mb-2">📈 The Results</h4>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                    {featured.results.map((r, i) => (
                      <div key={i} className="bg-green-50 border border-green-100 rounded-xl px-3 py-2 text-sm text-gray-700 break-words">{r}</div>
                    ))}
                  </div>
                </div>
                <a href={featured.url} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-2 bg-primary hover:bg-primary-dark text-white px-6 py-3 rounded-xl font-bold text-sm transition-all hover:shadow-lg">
                  Read Full Case Study <span>→</span>
                </a>
              </div>
              <div className="hidden md:flex items-center justify-center">
                <div className="w-[160px] h-[160px] bg-primary/5 rounded-full flex items-center justify-center text-5xl relative">
                  {featured.emoji}
                  <div className="absolute inset-0 border-2 border-dashed border-primary/20 rounded-full animate-spin" style={{animationDuration:'20s'}} />
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* === ALL CASE STUDIES === */}
      <section className="py-16 px-4">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <span className="text-primary text-sm font-semibold tracking-[0.2em] uppercase">Case Studies</span>
            <h2 className="text-3xl md:text-5xl font-extrabold mt-4 mb-4 text-gray-900">The Full Story Behind <span className="text-primary">the Numbers</span></h2>
            <p className="text-gray-500 max-w-2xl mx-auto text-lg">Every campaign had a unique challenge — here's how we solved it and what the results looked like.</p>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-5">
            {remaining.map((cs, i) => (
              <a key={i} href={cs.url} target="_blank" rel="noopener noreferrer" className="group bg-white rounded-2xl border border-gray-100 p-6 hover:border-primary/20 hover:shadow-xl hover:-translate-y-1 transition-all duration-300 flex flex-col">
                <div className="flex items-baseline gap-3 mb-2">
                  <span className="text-2xl font-extrabold text-primary">{cs.metric}</span>
                  <span className="text-xs text-gray-500 uppercase tracking-wider">{cs.label}</span>
                </div>
                <h3 className="font-bold text-lg mb-1">{cs.emoji} {cs.website ? <a href={cs.website} target="_blank" rel="noopener noreferrer" className="hover:underline text-primary">{cs.name}</a> : cs.name}</h3>
                <span className="text-xs font-semibold bg-red-50 text-red-600 px-3 py-1 rounded-full inline-block mb-3 w-fit">{cs.industry}</span>
                <div className="mb-3">
                  <h4 className="text-[11px] font-bold uppercase tracking-wider text-primary mb-0.5">📋 Challenge</h4>
                  <p className="text-gray-600 text-sm leading-6 break-words overflow-hidden">{cs.challenge}</p>
                </div>
                <div className="mb-3">
                  <h4 className="text-[11px] font-bold uppercase tracking-wider text-primary mb-0.5">💡 Solution</h4>
                  <p className="text-gray-600 text-sm leading-6 break-words overflow-hidden">{cs.solution}</p>
                </div>
                <div className="mb-4">
                  <h4 className="text-[11px] font-bold uppercase tracking-wider text-primary mb-1">📈 Results</h4>
                  <ul className="space-y-1.5">
                    {cs.results.slice(0, 4).map((r, j) => (
                      <li key={j} className="text-xs text-gray-600 flex items-start gap-2 leading-5 break-words"><span className="shrink-0 text-[10px]">✅</span><span>{r}</span></li>
                    ))}
                  </ul>
                </div>
                <span className="inline-flex items-center gap-1.5 text-primary font-semibold text-sm mt-auto group-hover:gap-2 transition-all">Read Full Case Study →</span>
              </a>
            ))}
          </div>
        </div>
      </section>

      {/* === CTA === */}
      <section className="relative py-24 px-4 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-primary to-primary-dark" />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] bg-white/10 rounded-full blur-3xl" />
        <div className="relative max-w-2xl mx-auto text-center">
          <h2 className="text-3xl md:text-5xl font-extrabold mb-4 text-white">Ready for Your <span className="text-amber-300">Success Story?</span></h2>
          <p className="text-white/80 mb-10 text-lg">Every campaign starts with a free, no-obligation SEO audit. Let's discuss how I can help your business rank higher.</p>
          <Link href="/contact" className="group inline-flex items-center gap-2 bg-white text-primary-dark px-10 py-4 rounded-xl font-bold text-lg transition-all hover:shadow-xl hover:-translate-y-0.5">
            Get Free SEO Audit <span className="group-hover:translate-x-1 transition-transform">→</span>
          </Link>
        </div>
      </section>

      {/* === FAQ === */}
      <section className="py-16 px-4 bg-white">
        <div className="max-w-4xl mx-auto">
          <FAQSchema faqs={[
            { question: "What types of projects do you showcase?", answer: "I showcase real SEO campaigns I've executed for Bangladeshi businesses across various industries — including restaurant local SEO, e-commerce optimization, real estate keyword ranking, garments export B2B SEO, healthcare visibility, and education sector growth. Each case study includes the challenge, the exact strategy applied, and the measurable results achieved." },
            { question: "Can I see before-and-after results?", answer: "Absolutely. Every case study on this page includes clear before-and-after metrics — keyword position improvements, organic traffic growth, conversion rate changes, and revenue impact. I believe in transparent, data-backed proof of my SEO work rather than vague claims." },
            { question: "How do I get a case study for my business?", answer: "Getting your own case study is simple. Start with a free SEO audit where I analyze your current online presence. If we work together, I'll document the entire process — from baseline metrics to final results — and create a detailed case study showcasing your business's SEO transformation." },
          ]} />
          <h2 className="text-2xl md:text-3xl font-extrabold text-center mb-8">Frequently Asked <span className="text-primary">Questions</span></h2>
          <div className="space-y-0 divide-y divide-gray-100">
            {[
              { question: "What types of projects do you showcase?", answer: "I showcase real SEO campaigns I've executed for Bangladeshi businesses across various industries — including restaurant local SEO, e-commerce optimization, real estate keyword ranking, garments export B2B SEO, healthcare visibility, and education sector growth. Each case study includes the challenge, the exact strategy applied, and the measurable results achieved." },
              { question: "Can I see before-and-after results?", answer: "Absolutely. Every case study on this page includes clear before-and-after metrics — keyword position improvements, organic traffic growth, conversion rate changes, and revenue impact. I believe in transparent, data-backed proof of my SEO work rather than vague claims." },
              { question: "How do I get a case study for my business?", answer: "Getting your own case study is simple. Start with a free SEO audit where I analyze your current online presence. If we work together, I'll document the entire process — from baseline metrics to final results — and create a detailed case study showcasing your business's SEO transformation." },
            ].map((f, i) => (
              <details key={i} className="py-4 group">
                <summary className="font-semibold text-gray-900 cursor-pointer list-none flex justify-between items-center">
                  {f.question}
                  <span className="text-primary transition-transform group-open:rotate-180">▼</span>
                </summary>
                <p className="text-gray-600 mt-3 pl-2">{f.answer}</p>
              </details>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <Footer />
    </div>
  );
}
