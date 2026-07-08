"use client";
import { useEffect } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { FAQSchema } from "@/components/Schema";
import services from "../data";
import { BreadcrumbSchema, ServiceSchema } from "@/components/Schema";

export default function ServicePage() {
  const { slug } = useParams();
  const svc = services.find((s) => s.slug === slug);

  useEffect(() => {
    if (svc) {
      document.title = `${svc.title} — Md Kanok Miah | SEO Expert in Dhaka, Bangladesh`;
    }
  }, [svc]);

  if (!svc) {
    return (
      <div className="min-h-screen bg-white text-gray-900 flex items-center justify-center flex-col gap-4">
        <h1 className="text-3xl font-bold">Service Not Found</h1>
        <p className="text-gray-600">The service page you're looking for doesn't exist.</p>
        <Link href="/services" className="text-primary hover:underline">← All Services</Link>
      </div>
    );
  }

  const breadcrumbItems = [
    { name: "Home", url: "https://kanokmiah.com.bd" },
    { name: "Services", url: "https://kanokmiah.com.bd/services" },
    { name: svc.title, url: `https://kanokmiah.com.bd/services/${svc.slug}` },
  ];

  const faqs = (() => {
    const slug = svc.slug;
    if (slug === "local-seo") return [
      { question: "How long does local SEO take to show results?", answer: "Most clients see initial improvements in 4–6 weeks, with significant ranking improvements in 3–6 months. Local SEO results depend on competition, your current online presence, and how quickly we can optimize your Google Business Profile and build local citations." },
      { question: "Do you offer local SEO for Chittagong?", answer: "Yes, I offer local SEO services for all major cities in Bangladesh including Chittagong, Sylhet, Dhaka, and Khulna. My strategies are tailored to each city's local search landscape." },
      { question: "What is Google Business Profile optimization?", answer: "GBP optimization involves verifying and fully optimizing your Google Business Profile with accurate NAP (Name, Address, Phone), selecting relevant categories, adding photos, collecting reviews, and posting regular updates to improve local pack rankings." },
      { question: "How do local citations help my business?", answer: "Local citations (mentions of your business name, address, and phone on other websites) help Google verify your business information and improve local search rankings. I build citations on top Bangladeshi directories like Bdshop and Yellow Pages BD." },
      { question: "Do you target both Bangla and English keywords?", answer: "Absolutely. I research and target both Bengali and English keywords that your local customers are actually searching for. This bilingual approach helps capture the widest possible local audience in Bangladesh." },
      { question: "Can you help with Google reviews management?", answer: "Yes, I help businesses develop a systematic approach to earn more positive Google reviews, respond to existing reviews professionally, and manage your online reputation effectively to boost local SEO performance." },
      { question: "How much does local SEO cost for a small business in Dhaka?", answer: "Local SEO packages for small businesses in Dhaka start from BDT 15,000 per month and vary based on competition, number of locations, and scope of citation building. I offer custom plans after a free audit of your current Google Business Profile and local search presence." },
    ];
    if (slug === "on-page-seo") return [
      { question: "What is included in on-page SEO?", answer: "My on-page SEO service includes title tag and meta description optimization, header structure improvements, keyword-optimized content, internal linking architecture, image alt text, and schema markup implementation." },
      { question: "How long does on-page SEO take?", answer: "Initial on-page optimizations can be implemented within 1–2 weeks, but seeing ranking improvements typically takes 4–8 weeks as search engines crawl and re-index your updated pages." },
      { question: "Do you follow Google's E-E-A-T guidelines?", answer: "Yes, all my on-page SEO work follows Google's Experience, Expertise, Authoritativeness, and Trustworthiness guidelines to ensure long-term ranking stability and protection from algorithm updates." },
      { question: "What is schema markup and why do I need it?", answer: "Schema markup is structured data added to your website that helps search engines understand your content better. It can enable rich snippets in search results, improving click-through rates and visibility." },
      { question: "Can you optimize existing content?", answer: "Yes, I audit your existing content and optimize it for both search engines and users. This includes keyword integration, readability improvements, internal linking, and ensuring proper heading hierarchy." },
      { question: "How do you choose which keywords to target?", answer: "I conduct comprehensive keyword research using tools like Google Keyword Planner, Ahrefs, and local Bangladesh search data to find high-intent, achievable keywords that balance search volume with competition." },
      { question: "How much does on-page SEO cost per page?", answer: "On-page SEO optimization starts from BDT 2,500 per page for basic optimization and goes up to BDT 8,000 per page for comprehensive optimization including schema markup, content rewriting, and internal linking restructuring. I offer discounted packages for 10+ pages." },
    ];
    if (slug === "link-building") return [
      { question: "What types of backlinks do you build?", answer: "I build high-quality backlinks through guest posting on authoritative Bangladeshi websites, local directory submissions, niche-relevant editorial links, broken link building, and digital PR campaigns." },
      { question: "Are your link building methods white-hat?", answer: "Absolutely. I only use ethical, white-hat link building techniques that comply with Google's Webmaster Guidelines. No PBNs, paid links, or spammy tactics that could get your site penalized." },
      { question: "How many backlinks do I need to rank?", answer: "Quality matters far more than quantity. A few high-authority, relevant backlinks from trusted Bangladeshi websites can have more impact than hundreds of low-quality links. I focus on building a natural, diverse backlink profile." },
      { question: "Do you build links from Bangladeshi websites?", answer: "Yes, I specialize in acquiring backlinks from high-authority Bangladeshi domains including news sites, business directories, educational institutions, and industry-specific platforms relevant to your niche." },
      { question: "How long does link building take to show results?", answer: "Link building is a long-term strategy. You can expect to see initial ranking improvements within 2–3 months, with significant authority gains accumulating over 6–12 months as Google recognizes your growing backlink profile." },
      { question: "Can you recover from Google penalties?", answer: "Yes, I offer link audit and recovery services. I identify toxic backlinks, create disavow files, and help you submit reconsideration requests to Google if your site has been manually penalized." },
      { question: "How much does link building cost per month?", answer: "Monthly link building packages start from BDT 25,000 and include 5-8 high-quality backlinks from authoritative Bangladeshi sources. Each link is earned through guest posting, digital PR, or broken link building — never purchased or PBN-based." },
    ];
    if (slug === "technical-seo") return [
      { question: "What is Core Web Vitals and why does it matter?", answer: "Core Web Vitals are Google's set of metrics measuring real-world user experience — loading speed (LCP), interactivity (FID/INP), and visual stability (CLS). They are ranking factors that directly impact your search positions." },
      { question: "How do you fix site speed issues?", answer: "I use tools like Google PageSpeed Insights and Lighthouse to diagnose speed bottlenecks, then implement fixes including image optimization, code minification, browser caching, CDN integration, and server response time improvements." },
      { question: "Do you work with WordPress websites?", answer: "Yes, I have extensive experience optimizing WordPress sites for technical SEO. I can fix plugin conflicts, optimize databases, implement caching solutions, and improve overall WordPress performance." },
      { question: "What is crawl budget optimization?", answer: "Crawl budget is the number of pages Googlebot crawls on your site within a given timeframe. I optimize it by fixing crawl errors, removing duplicate content, improving internal linking, and managing your sitemap and robots.txt properly." },
      { question: "How do you implement structured data?", answer: "I implement JSON-LD structured data markup for various schema types including LocalBusiness, Article, Product, FAQ, BreadcrumbList, and Review depending on your site's content and goals." },
      { question: "Can you fix mobile usability issues?", answer: "Yes, I identify and fix mobile usability issues such as tap targets too small, content wider than screen, viewport configuration problems, and font size issues to ensure your site passes Google's mobile-friendly test." },
      { question: "How much does technical SEO cost for a WordPress site?", answer: "Technical SEO audits start from BDT 10,000 and full optimization packages range from BDT 20,000 to BDT 50,000 depending on your site size and complexity. This includes Core Web Vitals fixes, schema markup, and crawl optimization." },
    ];
    if (slug === "geo-ai-search") return [
      { question: "What is GEO (Generative Engine Optimization)?", answer: "GEO is the practice of optimizing your content to be accurately cited and referenced by AI-powered search engines like Google AI Overviews, ChatGPT, Perplexity, and Gemini. It focuses on entity-based content and authoritative source building." },
      { question: "How do I get my business in ChatGPT responses?", answer: "To appear in ChatGPT responses, your website needs strong topical authority, clear entity signals, well-structured FAQ content, and citations from authoritative sources. I implement entity-first SEO strategies to achieve this." },
      { question: "How is GEO different from traditional SEO?", answer: "Traditional SEO focuses on keyword rankings and backlinks for Google's algorithm. GEO focuses on entity recognition, semantic relevance, and content structured for AI extraction — preparing your site for AI-powered search experiences." },
      { question: "Do you optimize for Google AI Overviews?", answer: "Yes, I optimize your content to be featured in Google AI Overviews (formerly SGE) by implementing clear entity definitions, authoritative citations, FAQ/QA structures, and comprehensive topical coverage." },
      { question: "What is entity-first content?", answer: "Entity-first content is structured around real-world entities (people, places, things, concepts) rather than just keywords. It helps AI systems understand your expertise and correctly attribute information to your business." },
      { question: "How long does GEO take to show results?", answer: "GEO is a forward-looking strategy. Some improvements in AI citation can appear within 2–3 months, but building the level of entity authority needed for consistent AI inclusion typically takes 6–12 months of sustained effort." },
      { question: "How much does GEO optimization cost for a Bangladeshi business?", answer: "GEO optimization packages start from BDT 20,000 per month for small businesses and range up to BDT 50,000 for comprehensive entity-first SEO strategies. Every package includes a full AI search readiness audit and entity content restructuring." },
    ];
    if (slug === "ecommerce-seo") return [
      { question: "Do you optimize Daraz seller pages?", answer: "Yes, I optimize Daraz seller pages for better visibility within Daraz's search and for Google. I focus on product titles, descriptions, images, category placement, and review signals to boost rankings." },
      { question: "How do you handle duplicate content in e-commerce?", answer: "I address duplicate content issues common in e-commerce sites — product variations, faceted navigation, and manufacturer descriptions — using canonical tags, parameter handling, and unique product descriptions." },
      { question: "Can you work with Shopify stores?", answer: "Yes, I specialize in Shopify SEO including collection page optimization, meta fields management, blog content strategy, URL structure fixes, and Shopify-specific technical SEO improvements." },
      { question: "How do you optimize product pages for conversions?", answer: "I optimize product pages for both search rankings and conversions by focusing on compelling product titles, detailed unique descriptions, customer review signals, high-quality images with alt text, and clear calls-to-action." },
      { question: "What is faceted navigation and why is it a problem?", answer: "Faceted navigation creates multiple URL variations for the same products based on filter selections, which can cause massive duplicate content issues. I implement proper canonical tags and noindex strategies to manage this." },
      { question: "How long does e-commerce SEO take to work?", answer: "E-commerce SEO typically shows initial results in 6–8 weeks for less competitive products. For highly competitive categories, expect 4–6 months to see meaningful ranking improvements and organic traffic growth." },
      { question: "How much does e-commerce SEO cost for a Daraz store?", answer: "E-commerce SEO for Daraz stores starts from BDT 15,000 per month and includes product title optimization, category restructuring, and review management. Full Shopify or WooCommerce SEO packages start from BDT 30,000 per month." },
    ];
    if (slug === "semantic-seo") return [
      { question: "What is semantic SEO and how is it different?", answer: "Semantic SEO goes beyond keywords to optimize for topics, entities, and user intent. It uses topic clusters, entity linking, and co-occurrence patterns to build topical authority that Google rewards with higher rankings." },
      { question: "What are topic clusters?", answer: "Topic clusters consist of a comprehensive pillar page covering a broad topic, linked to multiple cluster pages that dive deeper into specific subtopics. This structure signals expertise to Google and improves rankings for entire topic families." },
      { question: "How does entity SEO help my website?", answer: "Entity SEO helps Google understand the real-world entities your business is associated with (people, places, services). This improves your chances of appearing in Knowledge Graphs, rich snippets, and AI search results." },
      { question: "Do you implement schema markup for entities?", answer: "Yes, I implement Schema.org markup for Person, LocalBusiness, Service, and other entity types to help search engines build a comprehensive understanding of your business and its relationships." },
      { question: "How long does semantic SEO take to show results?", answer: "Semantic SEO is a medium to long-term strategy. Initial benefits from content restructuring can appear in 2–3 months, but building recognized topical authority typically takes 6–12 months." },
      { question: "Can semantic SEO help with AI search optimization?", answer: "Absolutely. Semantic SEO's focus on entities, relationships, and topical authority aligns perfectly with how AI search engines understand and cite content. It naturally prepares your site for GEO and AI search." },
      { question: "How much does semantic SEO cost per month?", answer: "Semantic SEO packages start from BDT 25,000 per month and include topical cluster strategy, entity schema implementation, and content restructuring. This advanced SEO approach delivers compounding authority gains over 6-12 months." },
    ];
    return [
      { question: `How long does ${svc.title} take to show results?`, answer: `Most ${svc.title.toLowerCase()} efforts show initial improvements within 4–8 weeks, with significant results building over 3–6 months of consistent optimization and strategy execution.` },
      { question: `Do you offer ${svc.title} for Chittagong?`, answer: `Yes, I provide ${svc.title.toLowerCase()} services for all of Bangladesh including Dhaka, Chittagong, Sylhet, and Khulna with strategies tailored to each market.` },
      { question: `What is included in your ${svc.title} package?`, answer: `Each ${svc.title.toLowerCase()} package includes a comprehensive audit, custom strategy development, implementation, monthly reporting, and ongoing optimization.` },
      { question: "Are your SEO methods white-hat and Google-compliant?", answer: "Absolutely. All my SEO strategies strictly follow Google's Webmaster Guidelines. I use only ethical, sustainable techniques that build long-term organic growth." },
      { question: "Do you provide monthly reports?", answer: "Yes, I provide detailed monthly reports showing keyword rankings, organic traffic, backlink growth, and key performance metrics so you can see exactly how your SEO investment is performing." },
      { question: "How do I get started with SEO for my Bangladesh business?", answer: "Getting started is simple. Contact me for a free SEO audit where I analyze your current website, identify opportunities, and provide a customized strategy proposal with transparent pricing." },
      { question: "What is the best way to improve my website rankings in Dhaka?", answer: "The best approach is a combination of local SEO (Google Business Profile optimization), on-page SEO (content and meta tags), and technical SEO (site speed and mobile optimization). I create a customized strategy after auditing your specific needs." },
    ];
  })();

  return (
    <div className="min-h-screen bg-white text-gray-900">
      <head>
        <link rel="canonical" href={`https://kanokmiah.com.bd/services/${svc.slug}`} />
        <meta name="robots" content="index, follow" />
        {BreadcrumbSchema(breadcrumbItems)}
        {ServiceSchema(svc)}
      </head>
      <Navbar />

      {/* Visible Breadcrumb Nav */}
      <div className="pt-24 px-4 max-w-4xl mx-auto">
        <nav className="flex items-center gap-2 text-sm text-gray-500 py-3">
          <Link href="/" className="hover:text-primary transition-colors">Home</Link>
          <span className="text-gray-300">›</span>
          <Link href="/services" className="hover:text-primary transition-colors">Services</Link>
          <span className="text-gray-300">›</span>
          <span className="text-gray-800 font-medium">{svc.title}</span>
        </nav>
      </div>

      {/* Hero */}
      <section className="relative pt-32 pb-16 px-4 overflow-hidden">
        <div className="absolute top-1/3 -left-32 w-96 h-96 bg-primary/20 rounded-full blur-3xl animate-pulse" />
        <div className="absolute bottom-1/3 -right-32 w-96 h-96 bg-primary/10 rounded-full blur-3xl animate-pulse delay-1000" />
        <div className="relative max-w-4xl mx-auto">
          <div className="flex flex-wrap items-center gap-3 mb-6">
            <div className="inline-flex items-center gap-2 bg-primary-light border border-primary/20 text-primary text-xs font-semibold px-5 py-2 rounded-full backdrop-blur-sm">
              {svc.icon} {svc.title}
            </div>
            <span className="inline-flex items-center gap-1 bg-amber-50 border border-amber-200 text-amber-700 text-xs font-semibold px-4 py-2 rounded-full">
              🕐 Last Updated: July 2026
            </span>
          </div>
          <h1 className="text-4xl md:text-6xl font-extrabold leading-tight mb-6">{svc.title}</h1>
          <p className="text-lg text-gray-500 mb-3 font-medium">{svc.subtitle}</p>
          <p className="text-lg text-gray-600 max-w-3xl leading-relaxed">{svc.desc}</p>
          <div className="mt-4 flex flex-wrap items-center gap-3">
            <span className="inline-flex items-center gap-1.5 bg-blue-50 border border-blue-200 text-blue-700 text-xs font-medium px-4 py-2 rounded-full">
              ✅ Expert Reviewed
            </span>
            <span className="text-xs text-gray-400">This guide was reviewed by Md Kanok Miah, SEO expert with 6+ years of experience serving Bangladesh businesses.</span>
          </div>
          <div className="mt-6 flex flex-wrap gap-4">
            <Link href="/contact" className="inline-flex items-center gap-2 bg-primary hover:bg-primary-dark text-white px-6 py-3 rounded-xl font-bold text-sm transition-all hover:shadow-lg hover:-translate-y-0.5">
              Get Free SEO Audit →
            </Link>
            <Link href="/services" className="inline-flex items-center gap-2 border border-gray-200 text-gray-600 px-6 py-3 rounded-xl font-semibold text-sm hover:border-primary hover:text-primary transition-all">
              ← All Services
            </Link>
          </div>
        </div>
      </section>

      {/* Quick Answer Box for AEO / GEO */}
      <section className="px-4">
        <div className="max-w-4xl mx-auto">
          <div className="bg-primary-light border border-primary/20 rounded-xl p-5 mb-8">
            <p className="text-sm font-bold text-primary mb-1">⚡ Quick Answer</p>
            <p className="text-gray-700">{svc.qa || 'Get expert SEO guidance tailored for your Bangladesh business. Contact Md Kanok Miah for a free consultation and audit.'}</p>
          </div>
        </div>
      </section>

      {/* Benefits */}
      <section className="py-16 px-4">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-2xl md:text-3xl font-extrabold mb-3">
            Why You Need <span className="text-primary">{svc.title}</span> for Better Rankings
          </h2>
          <p className="text-gray-500 mb-8">The key benefits of professional SEO for your Bangladesh business.</p>
          <div className="grid md:grid-cols-2 gap-4">
            {svc.benefits.map((b, i) => (
              <div key={i} className="flex items-start gap-3 bg-gray-50 border border-gray-100 rounded-xl p-5">
                <span className="text-primary text-xl mt-0.5">✓</span>
                <span className="text-gray-600">{b}</span>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Full Service Description & Features */}
      <section className="py-16 px-4 bg-gray-50/80 border-y border-gray-100">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-2xl md:text-3xl font-extrabold mb-8">
            What&apos;s Included in <span className="text-primary">{svc.title}</span> — Complete Features
          </h2>
          <p className="text-gray-600 mb-8 leading-relaxed">{svc.desc}</p>
          <div className="grid md:grid-cols-2 gap-4">
            {svc.features.map((f, i) => (
              <div key={i} className="flex items-start gap-3 bg-white border border-gray-100 rounded-xl p-4">
                <span className="w-5 h-5 bg-primary rounded-full flex items-center justify-center text-white text-xs shrink-0 mt-0.5">✓</span>
                <span className="text-gray-600 text-sm">{f}</span>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Process */}
      <section className="py-16 px-4">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-2xl md:text-3xl font-extrabold mb-3">
            My <span className="text-primary">SEO Process</span> for {svc.title}
          </h2>
          <p className="text-gray-500 mb-8">How I deliver results for {svc.title}.</p>
          <div className="space-y-4">
            {svc.process.map((step, i) => (
              <div key={i} className="flex items-start gap-4 bg-gray-50 border border-gray-100 rounded-xl p-5">
                <div className="w-10 h-10 rounded-xl bg-primary flex items-center justify-center font-extrabold text-sm text-white shrink-0">
                  {String(i + 1).padStart(2, "0")}
                </div>
                <div>
                  <p className="text-gray-600">{step}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Related Services */}
      <section className="py-16 px-4 bg-gray-50/80 border-y border-gray-100">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-2xl md:text-3xl font-extrabold text-center mb-10">
            Other <span className="text-primary">SEO Services</span>
          </h2>
          <div className="grid md:grid-cols-3 gap-4">
            {services.filter((s) => s.slug !== svc.slug).map((related, i) => (
              <Link key={i} href={`/services/${related.slug}`} className="group bg-white border border-gray-100 rounded-2xl p-6 hover:border-primary/20 hover:shadow-lg hover:-translate-y-1 transition-all">
                <div className="text-4xl mb-3">{related.icon}</div>
                <h3 className="font-bold text-gray-900 mb-2 group-hover:text-primary transition-colors">{related.title}</h3>
                <p className="text-gray-500 text-sm leading-relaxed">{related.shortDesc.slice(0, 120)}...</p>
                <div className="mt-3 text-primary text-xs font-semibold">Learn More →</div>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* FAQ */}
      <section className="py-16 px-4 bg-white">
        <div className="max-w-4xl mx-auto">
          {FAQSchema(faqs)}
          <h2 className="text-2xl md:text-3xl font-extrabold text-center mb-8">
            Frequently Asked <span className="text-primary">Questions</span>
          </h2>
          <div className="space-y-0 divide-y divide-gray-100">
            {faqs.map((f, i) => (
              <details key={i} className="py-4 group">
                <summary className="font-semibold text-gray-900 cursor-pointer list-none flex justify-between items-center">
                  {f.question}
                  <span className="text-primary transition-transform group-open:rotate-180">▼</span>
                </summary>
                <p className="text-gray-600 mt-3 pl-2">{f.answer}</p>
              </details>
            ))}
          </div>
          {/* Cross-link to Industries */}
          <div className="mt-10 text-center">
            <Link
              href="/industries"
              className="inline-flex items-center gap-2 text-primary font-semibold hover:text-primary-dark transition-colors text-sm"
            >
              See which industries we serve →
            </Link>
          </div>
        </div>
      </section>

      {/* Author Bio */}
      <div className="bg-gray-50 border-y border-gray-100 py-12 px-4">
        <div className="max-w-4xl mx-auto flex items-start gap-6">
          <div className="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center text-2xl shrink-0">👤</div>
          <div>
            <p className="font-bold text-gray-900">Written by <span className="text-primary">Md Kanok Miah</span></p>
            <p className="text-sm text-gray-500">SEO Expert with 6+ years of experience helping Bangladeshi businesses rank higher on Google. Google Business Profile certified.</p>
            <p className="text-xs text-gray-400 mt-2">Last updated: July 2026</p>
          </div>
        </div>
      </div>

      {/* CTA */}
      <section className="relative py-24 px-4 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-primary to-primary-dark" />
        <div className="relative max-w-2xl mx-auto text-center">
          <h2 className="text-3xl md:text-5xl font-extrabold mb-4 text-white">
            Ready to <span className="text-amber-300">Rank Higher</span>?
          </h2>
          <p className="text-primary/80 mb-8 text-lg">
            Get a free SEO audit and discover exactly what your website needs to grow in Bangladesh.
          </p>
          <Link href="/contact" className="group inline-flex items-center gap-2 bg-white text-primary-dark px-10 py-4 rounded-xl font-bold text-lg transition-all hover:shadow-xl hover:-translate-y-0.5">
            Start Your Free Audit
            <span className="group-hover:translate-x-1 transition-transform">→</span>
          </Link>
        </div>
      </section>

      {/* Footer */}
      <Footer />
    </div>
  );
}
