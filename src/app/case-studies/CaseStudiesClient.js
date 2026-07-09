"use client";

import Navbar from "@/components/Navbar";
import Link from "next/link";
import { BreadcrumbSchema, FAQSchema } from "@/components/Schema";

const caseStudies = [
  {
    industry: "Food & Restaurant",
    title: "Local Dhaka Restaurant — From Obscurity to Google Maps #1",
    icon: "🍽️",
    challenge:
      "A popular but digitally invisible Biriyani restaurant in Old Dhaka was losing customers to competitors who dominated Google Maps and local search. They had no Google Business Profile, zero online reviews, and inconsistent NAP citations across the few directories they appeared on.",
    solution:
      "Created and fully optimized a Google Business Profile with accurate NAP, 30+ high-quality photos of their dishes and interior, and the correct primary category ('Bengali Restaurant'). Built 40+ local citations on Bangladeshi directories (Yellow Pages BD, BDTradeInfo, Dhaka Directory). Launched a review-generation campaign that collected 25+ five-star Google reviews in 90 days.",
    results: [
      { metric: "Google Map Views", value: "+300%", unit: "increase" },
      { metric: "Google Reviews", value: "25+", unit: "5-star reviews" },
      { metric: "Direction Requests", value: "+200%", unit: "increase" },
      { metric: "Phone Calls", value: "+150%", unit: "increase" },
    ],
    bgColor: "bg-orange-50/80",
    borderColor: "border-orange-200",
    tagColor: "bg-orange-100 text-orange-800",
  },
  {
    industry: "E-commerce",
    title: "Daraz E-Commerce Store — 180% Organic Traffic Surge",
    icon: "🛒",
    challenge:
      "A Dhaka-based fashion accessories seller on Daraz was struggling to appear in the top 20 search results for high-volume keywords like 'fashion accessories in Bangladesh' and 'trendy bracelet Dhaka'. Their product titles were poorly optimized, images had no alt text, and they lacked any product schema markup.",
    solution:
      "Optimized 200+ product listings with bilingual (Bengali + English) keyword-rich titles and descriptions. Added descriptive alt text to all product images. Implemented product schema (structured data) for each listing. Built a blog section on their external Shopify store with category-level content targeting informational keywords. Fixed Core Web Vitals issues that were hurting mobile rankings.",
    results: [
      { metric: "Organic Traffic", value: "+180%", unit: "increase" },
      { metric: "Keyword Rankings (Top 10)", value: "47", unit: "keywords" },
      { metric: "Conversion Rate", value: "+35%", unit: "improvement" },
      { metric: "Revenue", value: "+120%", unit: "growth" },
    ],
    bgColor: "bg-blue-50/80",
    borderColor: "border-blue-200",
    tagColor: "bg-blue-100 text-blue-800",
  },
  {
    industry: "Real Estate",
    title: "Gulshan Real Estate Developer — #1 for 'Apartment in Dhaka'",
    icon: "🏢",
    challenge:
      "A mid-sized real estate developer in Gulshan, Dhaka, was invisible in organic search for the most competitive keyword in Bangladesh real estate: 'apartment in Dhaka'. Their website had severe technical issues — poor mobile performance, duplicate content across project pages, missing meta descriptions, and zero structured data. They were spending heavily on Google Ads with diminishing returns.",
    solution:
      "Conducted a full technical SEO audit resolving 30+ critical issues including Core Web Vitals optimization (LCP reduced from 4.2s to 1.8s), fixing 45 duplicate content pages, and implementing LocalBusiness and Product schema for each project. Built a content marketing engine producing weekly blog posts about Dhaka real estate trends, neighbourhood guides, and apartment buying checklists. Earned backlinks from 12 Bangladeshi real estate portals and news sites.",
    results: [
      { metric: "Ranking for 'apartment in Dhaka'", value: "#1", unit: "position" },
      { metric: "Organic Traffic", value: "+250%", unit: "increase" },
      { metric: "Qualified Leads", value: "+180%", unit: "increase" },
      { metric: "Google Ads Spend", value: "-60%", unit: "reduction" },
    ],
    bgColor: "bg-emerald-50/80",
    borderColor: "border-emerald-200",
    tagColor: "bg-emerald-100 text-emerald-800",
  },
  {
    industry: "Garments & Textile",
    title: "Garments Exporter — 25% More B2B Leads from International SEO",
    icon: "👕",
    challenge:
      "A garments manufacturer in Gazipur, Bangladesh, was heavily dependent on trade show networking and B2B platforms like TradeIndia for international leads. Their corporate website ranked poorly for English-language buyer keywords such as 'readymade garments supplier Bangladesh', 'woven shirt manufacturer Dhaka', and 'OEM apparel vendor Asia'. Technical SEO was non-existent and content was limited to a single static homepage.",
    solution:
      "Revamped the entire website architecture with a focus on international buyer intent. Created dedicated landing pages for each product category (woven shirts, denim, knitwear, sportswear) optimized for English-language long-tail keywords. Implemented hreflang tags for English and Arabic versions. Built a blog targeting buying-cycle keywords: 'how to source garments from Bangladesh', 'garments manufacturing timeline Dhaka'. Secured backlinks from international trade publications and Bangladesh export promotion sites.",
    results: [
      { metric: "B2B Inbound Leads", value: "+25%", unit: "increase" },
      { metric: "Organic Traffic (International)", value: "+180%", unit: "increase" },
      { metric: "Top 10 Keywords", value: "32", unit: "buyer keywords" },
      { metric: "Inquiry Conversion", value: "+40%", unit: "improvement" },
    ],
    bgColor: "bg-purple-50/80",
    borderColor: "border-purple-200",
    tagColor: "bg-purple-100 text-purple-800",
  },
];

export default function CaseStudiesClient() {
  const breadcrumbItems = [
    { name: "Home", url: "https://kanokmiah.com.bd" },
    { name: "Case Studies", url: "https://kanokmiah.com.bd/case-studies" },
  ];


  return (
    <div className="min-h-screen bg-white text-gray-900">
      <head>
        {BreadcrumbSchema(breadcrumbItems)}
      </head>
      {/* === NAVBAR === */}
      <Navbar />

      {/* === HERO === */}
      <section className="relative pt-32 pb-16 px-4 overflow-hidden">
        <div className="absolute top-1/3 -left-32 w-96 h-96 bg-primary/20 rounded-full blur-3xl animate-pulse" />
        <div className="absolute bottom-1/4 -right-32 w-80 h-80 bg-primary/20 rounded-full blur-3xl animate-pulse delay-1000" />
        <div className="relative max-w-4xl mx-auto text-center">
          <div className="inline-flex items-center gap-2 bg-primary-light border border-primary/20 text-primary text-xs font-semibold px-5 py-2 rounded-full mb-8 backdrop-blur-sm">
            <span className="w-2 h-2 bg-primary rounded-full animate-pulse" />
            Proven Results
          </div>
          <h1 className="text-4xl md:text-6xl lg:text-7xl font-extrabold tracking-tight leading-[1.05] mb-6">
            SEO Case <span className="text-primary">Studies</span>
          </h1>
          <p className="text-lg md:text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
            Real SEO campaigns for Bangladeshi businesses across industries — from local Dhaka restaurants to 
            international garments exporters. Each case study shows the exact strategy, execution, and measurable results.
          </p>
        </div>
      </section>

      {/* === CASE STUDIES GRID === */}
      <section className="relative py-16 px-4">
        <div className="absolute top-0 right-0 w-72 h-72 bg-primary/10 rounded-full blur-3xl" />
        <div className="relative max-w-6xl mx-auto grid md:grid-cols-2 gap-6">
          {caseStudies.map((cs, i) => (
            <div
              key={i}
              className={`group rounded-2xl border ${cs.borderColor} ${cs.bgColor} p-6 md:p-8 hover:shadow-lg hover:-translate-y-1 transition-all duration-300`}
            >
              {/* Industry Tag */}
              <div className="flex items-center justify-between mb-4">
                <span className={`inline-block text-xs font-bold px-3 py-1.5 rounded-full ${cs.tagColor}`}>
                  {cs.icon} {cs.industry}
                </span>
              </div>

              {/* Title */}
              <h3 className="text-xl md:text-2xl font-extrabold text-gray-900 mb-4 leading-tight">
                {cs.title}
              </h3>

              {/* Challenge */}
              <div className="mb-4">
                <h4 className="text-xs font-bold uppercase tracking-wider text-gray-500 mb-2">The Challenge</h4>
                <p className="text-gray-600 text-sm leading-relaxed">{cs.challenge}</p>
              </div>

              {/* Solution */}
              <div className="mb-5">
                <h4 className="text-xs font-bold uppercase tracking-wider text-gray-500 mb-2">The Solution</h4>
                <p className="text-gray-600 text-sm leading-relaxed">{cs.solution}</p>
              </div>

              {/* Results */}
              <div>
                <h4 className="text-xs font-bold uppercase tracking-wider text-gray-500 mb-3">Results</h4>
                <div className="grid grid-cols-2 gap-3">
                  {cs.results.map((r, j) => (
                    <div
                      key={j}
                      className="bg-white/70 border border-white rounded-xl p-3 text-center"
                    >
                      <div className="text-xl md:text-2xl font-extrabold text-primary">{r.value}</div>
                      <div className="text-xs text-gray-500 mt-0.5 leading-tight">{r.metric}</div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          ))}
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
          <h2 className="text-2xl md:text-3xl font-extrabold text-center mb-8">
            Frequently Asked <span className="text-primary">Questions</span>
          </h2>
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

      {/* === CTA === */}
      <section className="relative py-24 px-4 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-primary to-primary-dark" />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] bg-gradient-to-r from-primary/20 to-primary/20 rounded-full blur-3xl" />
        <div className="relative max-w-2xl mx-auto text-center">
          <h2 className="text-3xl md:text-5xl font-extrabold mb-4 text-white">
            Ready for Your <span className="text-amber-300">Success Story?</span>
          </h2>
          <p className="text-primary/80 mb-10 text-lg">
            Every campaign starts with a free, no-obligation SEO audit. Let&apos;s discuss how I can help your business rank higher.
          </p>
          <Link
            href="/contact"
            className="group inline-flex items-center gap-2 bg-white text-primary-dark px-10 py-4 rounded-xl font-bold text-lg transition-all hover:shadow-xl hover:-translate-y-0.5"
          >
            Get Free SEO Audit
            <span className="group-hover:translate-x-1 transition-transform">→</span>
          </Link>
        </div>
      </section>

      {/* === FOOTER COPYRIGHT === */}
      <footer className="py-8 border-t border-gray-100 text-center text-sm text-gray-500">
        <p>© 2026 <span className="text-primary font-bold">Md Kanok Miah</span> — SEO Expert in Bangladesh. All rights reserved.</p>
      </footer>
    </div>
  );
}
