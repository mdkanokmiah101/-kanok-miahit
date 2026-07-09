"use client";

import Navbar from "@/components/Navbar";
import Link from "next/link";
// Schema components rendered server-side in page.js — not duplicated here

const faqs = [
  {
    question: "How long does Local SEO take to show results in Bangladesh?",
    answer:
      "Local SEO in Bangladesh typically shows initial results within 3 to 6 months. The first 30 days are spent auditing your Google Business Profile, cleaning up local citations, and fixing NAP (Name, Address, Phone) inconsistencies across directories. By month 3, most clients see a noticeable increase in Google Map views and local pack appearances. Full dominance in Dhaka's competitive local search results usually takes 6 to 12 months of consistent citation building, review management, and localized content creation.",
  },
  {
    question: "How much does Technical SEO cost for a Bangladeshi website?",
    answer:
      "Technical SEO pricing in Bangladesh ranges from BDT 15,000 to BDT 50,000 depending on your site's size, platform, and complexity. A small WordPress site with basic issues (slow speed, missing meta tags, broken links) costs around BDT 15,000–25,000. An e-commerce store on Daraz or Shopify with hundreds of products and advanced issues (canonical errors, poor Core Web Vitals, structured data problems) ranges from BDT 30,000–50,000. Every engagement includes a full crawl audit, Core Web Vitals optimization, XML sitemap fixes, and schema markup implementation.",
  },
  {
    question: "What is your Link Building strategy for Bangladeshi businesses?",
    answer:
      "My link building strategy focuses entirely on quality over quantity. I secure backlinks from legitimate Bangladeshi sources: local news portals (Dhaka Tribune, The Business Standard), industry-specific Bangladeshi blogs, university and .edu.bd domains, chamber of commerce directories, and reputable local business associations. Each link is earned through guest posting, digital PR, broken link building, and resource page outreach. I strictly avoid PBNs, link farms, and any technique that could trigger a Google manual action. On average, clients gain 8–12 high-authority backlinks per month.",
  },
  {
    question: "What's the difference between GEO (Generative Engine Optimization) and Traditional SEO?",
    answer:
      "GEO (Generative Engine Optimization) is the practice of optimizing content for AI-driven search engines like Google's Search Generative Experience (SGE), ChatGPT, Perplexity, and Bing Copilot. Unlike traditional SEO which targets keyword rankings on a blue-link results page, GEO optimizes for how AI models extract, cite, and summarize information. Key tactics include: structuring content with clear entities, using authoritative citations, deploying FAQ schema with detailed answers, and ensuring your brand is referenced across authoritative sources. For Bangladeshi businesses, GEO is still early but critical for staying ahead as AI search adoption grows.",
  },
  {
    question: "How do I optimize my Google Business Profile for Dhaka local search?",
    answer:
      "Optimizing a Google Business Profile in Dhaka requires several specific steps: (1) Verify your exact business address and keep NAP consistent across all platforms, (2) Choose the most specific primary category (e.g., 'Bengali Restaurant' instead of just 'Restaurant'), (3) Add 20+ high-quality photos showing your premises, products, and team, (4) Collect and respond to every Google review — especially Bengali-language ones, (5) Post weekly Google Updates (offers, events, new products), (6) Use local Dhaka area keywords in your business description. I typically handle all of this within a 2-week onboarding period.",
  },
  {
    question: "Is SEO effective for e-commerce stores in Bangladesh (Daraz, Shopify)?",
    answer:
      "Absolutely. E-commerce SEO is one of the highest-ROI channels for Bangladeshi online stores. For Daraz sellers, optimizing product titles with Bengali + English keywords, improving image alt text, and collecting product reviews directly impacts search rank within Daraz's internal search and Google. For Shopify stores, technical SEO (page speed, mobile optimization, structured product schemas) combined with category-level content marketing routinely delivers 150–300% organic traffic growth within 6 months. E-commerce SEO in Bangladesh is particularly effective because most local competitors neglect it entirely.",
  },
  {
    question: "How does Content Marketing help SEO for Bangladeshi brands?",
    answer:
      "Content marketing powers SEO by building topical authority — Google ranks sites higher when it sees comprehensive, regularly updated content around a subject. For Bangladeshi brands, I create bilingual (Bengali + English) content targeting local search intent: 'best restaurant in Gulshan', 'how to start a business in Bangladesh', 'garments export documentation 2026'. Each blog post, guide, or landing page targets a specific keyword cluster and includes internal links to service pages. Over 6–12 months, this content compounds: older posts continue ranking and driving traffic without additional ad spend.",
  },
  {
    question: "Can you recover a website from a Google penalty in Bangladesh?",
    answer:
      "Yes, I have successfully recovered multiple Bangladeshi websites from Google manual actions and algorithmic penalties. The recovery process involves: (1) A full backlink audit using tools like Ahrefs to identify toxic links, (2) Creating and submitting a disavow file for spammy domains, (3) Fixing any on-page issues flagged in Google Search Console (cloaking, thin content, keyword stuffing), (4) Submitting a thorough reconsideration request in Search Console explaining every fix made. Recovery typically takes 4 to 12 weeks depending on penalty severity. I guarantee a structured roadmap before you pay anything.",
  },
  {
    question: "Should I invest in SEO or Google Ads for my Bangladesh business?",
    answer:
      "Both channels serve different goals. Google Ads delivers immediate traffic — ideal for promotions, short-term campaigns, and new businesses needing instant visibility. However, costs in Bangladesh are rising (CPCs for competitive keywords like 'home loan Dhaka' or 'best hotel in Cox's Bazar' can be BDT 50–150 per click). SEO is a long-term asset — rankings compound over time, traffic is free after the initial investment, and trust signals (organic ranking) convert better. My recommendation: start with a BDT 20,000–30,000 monthly SEO retainer for foundational rankings, then layer Google Ads on top for specific high-intent campaigns. 80% of my clients see better blended ROI with this hybrid approach.",
  },
  {
    question: "How do you choose the right keywords for a Bangladeshi business?",
    answer:
      "Keyword selection is a data-driven process. I begin by researching seed keywords in both English and Bengali using Ahrefs, Google Keyword Planner, and actual Search Console data. I analyse: search volume (local Bangladesh data), keyword difficulty (how many quality sites rank), commercial intent (transactional vs informational queries), and seasonality. For a Dhaka restaurant, I might target 'best kacchi in Dhaka' (high intent) and 'restaurant near Gulshan 2' (local long-tail). I also look for Bengali-alphabet queries that competitors ignore — these often have lower difficulty but strong conversion rates since they match how locals actually search on mobile.",
  },
];

export default function FAQPage() {
  return (
    <div className="min-h-screen bg-white text-gray-900">
      <Navbar />

      {/* === HERO === */}
      <section className="relative pt-32 pb-16 px-4 overflow-hidden">
        <div className="absolute top-1/3 -left-32 w-96 h-96 bg-primary/20 rounded-full blur-3xl animate-pulse" />
        <div className="absolute bottom-1/4 -right-32 w-80 h-80 bg-primary/20 rounded-full blur-3xl animate-pulse delay-1000" />
        <div className="relative max-w-4xl mx-auto text-center">
          <div className="inline-flex items-center gap-2 bg-primary-light border border-primary/20 text-primary text-xs font-semibold px-5 py-2 rounded-full mb-8 backdrop-blur-sm">
            <span className="w-2 h-2 bg-primary rounded-full animate-pulse" />
            FAQ
          </div>
          <h1 className="text-4xl md:text-6xl lg:text-7xl font-extrabold tracking-tight leading-[1.05] mb-6">
            Frequently Asked <span className="text-primary">Questions</span>
          </h1>
          <p className="text-lg md:text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
            Everything you need to know about SEO for your Bangladesh business — from local rankings to technical audits,
            link building to generative engine optimization. Can&apos;t find your question? Reach out for a free consultation.
          </p>
        </div>
      </section>

      {/* === FAQ ACCORDION === */}
      <section className="relative py-16 px-4">
        <div className="absolute top-0 right-0 w-72 h-72 bg-primary/10 rounded-full blur-3xl" />
        <div className="relative max-w-4xl mx-auto">
          <div className="space-y-0 divide-y divide-gray-100 bg-gray-50/50 border border-gray-100 rounded-2xl p-5 md:p-8">
            {faqs.map((faq, i) => (
              <details key={i} className="py-4 group">
                <summary className="font-semibold text-gray-900 cursor-pointer list-none flex justify-between items-center text-base md:text-lg">
                  <span>{faq.question}</span>
                  <span className="text-primary transition-transform group-open:rotate-180 shrink-0 ml-4">▼</span>
                </summary>
                <p className="text-gray-600 mt-3 pl-2 leading-relaxed text-sm md:text-base">{faq.answer}</p>
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
            Still Have <span className="text-amber-300">Questions?</span>
          </h2>
          <p className="text-primary/80 mb-10 text-lg">
            Get a personalised answer for your business. Claim your free SEO audit today — no strings attached.
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
