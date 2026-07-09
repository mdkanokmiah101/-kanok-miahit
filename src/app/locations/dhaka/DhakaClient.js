"use client";

import Navbar from "@/components/Navbar";
import Link from "next/link";
import { BreadcrumbSchema, FAQSchema } from "@/components/Schema";

const neighborhoods = [
  { icon: "🏘️", name: "Mirpur", desc: "Rank your business in Mirpur's competitive local market with targeted neighborhood SEO." },
  { icon: "🏢", name: "Gulshan", desc: "Dominate Gulshan's corporate and high-end local search results." },
  { icon: "🏙️", name: "Banani", desc: "Capture Banani's commercial zone traffic with precision local SEO." },
  { icon: "🌆", name: "Uttara", desc: "Grow your Uttara business with Google Maps and local pack rankings." },
  { icon: "🏛️", name: "Dhanmondi", desc: "Attract more local customers in Dhanmondi with hyperlocal SEO strategies." },
  { icon: "🏗️", name: "Motijheel", desc: "Boost visibility for your Motijheel business in Dhaka's financial hub." },
];

const trustPoints = [
  { icon: "📍", title: "Google Maps Ranking", desc: "Proven strategies to get your business to the top of Google Maps in Dhaka." },
  { icon: "📋", title: "GBP Optimization", desc: "Expert Google Business Profile optimization for maximum local visibility." },
  { icon: "⏳", title: "6+ Years Experience", desc: "Over half a decade of hands-on SEO experience in the Bangladesh market." },
  { icon: "🚀", title: "350+ Projects", desc: "Successfully delivered 350+ SEO projects for businesses across Bangladesh." },
];

export default function DhakaClient() {

  return (
    <div className="min-h-screen bg-white text-gray-900">
      <link rel="canonical" href="https://kanokmiah.com.bd/locations/dhaka" />
      <meta name="robots" content="index, follow" />
      {BreadcrumbSchema([
        { name: "Home", url: "https://kanokmiah.com.bd" },
        { name: "Locations", url: "https://kanokmiah.com.bd/locations" },
        { name: "Dhaka", url: "https://kanokmiah.com.bd/locations/dhaka" },
      ])}

      {/* === NAVBAR === */}
      <Navbar />

      {/* === HERO === */}
      <section className="relative pt-32 pb-16 px-4 overflow-hidden">
        <div className="absolute top-1/3 -left-32 w-96 h-96 bg-primary/20 rounded-full blur-3xl animate-pulse" />
        <div className="absolute bottom-1/4 -right-32 w-80 h-80 bg-primary/20 rounded-full blur-3xl animate-pulse delay-1000" />
        <div className="relative max-w-4xl mx-auto text-center">
          <div className="inline-flex items-center gap-2 bg-primary-light border border-primary/20 text-primary text-xs font-semibold px-5 py-2 rounded-full mb-8 backdrop-blur-sm">
            <span className="w-2 h-2 bg-primary rounded-full animate-pulse" />
            Dhaka SEO Services
          </div>
          <h1 className="text-4xl md:text-6xl lg:text-7xl font-extrabold tracking-tight leading-[1.05] mb-6">
            <span className="text-primary">
              Best SEO Services in Dhaka
            </span>
            <br />Rank Higher in Your Neighborhood
          </h1>
          <p className="text-lg md:text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
            Your trusted local SEO expert in Dhaka. I help businesses across the capital city dominate Google search results, attract more local customers, and grow revenue with proven, data-driven SEO strategies.
          </p>
          <div className="mt-8 flex flex-wrap justify-center gap-4">
            <Link href="/contact" className="bg-primary text-white font-bold px-8 py-3.5 rounded-full hover:bg-primary-dark hover:shadow-lg hover:shadow-primary/25 transition-all">
              Get Free Dhaka SEO Audit
            </Link>
            <Link href="/portfolio" className="border-2 border-primary text-primary font-bold px-8 py-3.5 rounded-full hover:bg-primary hover:text-white transition-all">
              View My Work
            </Link>
          </div>
        </div>
      </section>

      {/* === SEO FOR DHAKA NEIGHBORHOODS === */}
      <section className="relative py-16 px-4 bg-gray-50/50">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <span className="text-primary text-sm font-semibold tracking-widest uppercase">Hyperlocal Coverage</span>
            <h2 className="text-3xl md:text-5xl font-extrabold mt-3 mb-4">
              SEO for Dhaka <span className="text-primary">Neighborhoods</span>
            </h2>
            <p className="text-gray-600 max-w-2xl mx-auto">
              Targeted SEO strategies for every key area in Dhaka — customized to your local market and competition.
            </p>
          </div>
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
            {neighborhoods.map((area, i) => (
              <div key={i} className="group bg-white border border-gray-100 rounded-2xl p-6 hover:shadow-lg hover:-translate-y-1 transition-all">
                <div className="text-4xl mb-4">{area.icon}</div>
                <h3 className="font-bold text-xl mb-2 text-gray-900">{area.name}</h3>
                <p className="text-gray-600 text-sm leading-relaxed">{area.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* === WHY CHOOSE ME === */}
      <section className="relative py-16 px-4">
        <div className="absolute top-0 right-0 w-72 h-72 bg-primary/10 rounded-full blur-3xl" />
        <div className="relative max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <span className="text-primary text-sm font-semibold tracking-widest uppercase">Why Trust Me</span>
            <h2 className="text-3xl md:text-5xl font-extrabold mt-3 mb-4">
              Why Choose Me for <span className="text-primary">Dhaka SEO</span>
            </h2>
            <p className="text-gray-600 max-w-2xl mx-auto">
              What sets my Dhaka SEO services apart from the competition.
            </p>
          </div>
          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-5">
            {trustPoints.map((point, i) => (
              <div key={i} className="bg-gray-50 border border-gray-100 rounded-2xl p-6 text-center hover:bg-gray-100 hover:border-gray-200 transition-all hover:-translate-y-1">
                <div className="text-4xl mb-4">{point.icon}</div>
                <h3 className="font-bold text-lg mb-2 text-gray-900">{point.title}</h3>
                <p className="text-gray-600 text-sm leading-relaxed">{point.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* === FAQ === */}
      <section className="py-16 px-4 bg-white">
        <div className="max-w-4xl mx-auto">
          <FAQSchema faqs={[
            { question: "What areas of Dhaka do you cover?", answer: "I provide SEO services across all major areas of Dhaka including Mirpur, Gulshan, Banani, Uttara, Dhanmondi, Motijheel, Old Dhaka, Mohammadpur, Bashundhara R/A, and all other neighborhoods in the capital. My hyperlocal SEO approach targets customers in your specific area to drive foot traffic and local leads." },
            { question: "How is SEO different for Dhaka businesses?", answer: "SEO for Dhaka businesses requires understanding the unique local search landscape — mobile-first user behaviour, bilingual search queries (Bengali + English), intense competition in key sectors like restaurants and real estate, and the dominance of Google Maps for local discovery. I tailor strategies to these specific Dhaka market dynamics." },
            { question: "Do you offer local Dhaka SEO services?", answer: "Yes, local SEO is my core specialty. I offer comprehensive local SEO services for Dhaka businesses including Google Business Profile optimization, local citation building, neighborhood-specific keyword targeting, review management, and local content creation — all designed to help you rank in Google Maps and local organic search." },
            { question: "How do I get a free SEO audit in Dhaka?", answer: "Getting a free SEO audit is simple. Just contact me through the form on this page or visit my contact page. I'll analyze your current online presence — including your website, Google Business Profile, and local competition — and provide a detailed report with actionable recommendations tailored to your Dhaka business." },
          ]} />
          <h2 className="text-2xl md:text-3xl font-extrabold text-center mb-8">
            Frequently Asked <span className="text-primary">Questions</span>
          </h2>
          <div className="space-y-0 divide-y divide-gray-100">
            {[
              { question: "What areas of Dhaka do you cover?", answer: "I provide SEO services across all major areas of Dhaka including Mirpur, Gulshan, Banani, Uttara, Dhanmondi, Motijheel, Old Dhaka, Mohammadpur, Bashundhara R/A, and all other neighborhoods in the capital. My hyperlocal SEO approach targets customers in your specific area to drive foot traffic and local leads." },
              { question: "How is SEO different for Dhaka businesses?", answer: "SEO for Dhaka businesses requires understanding the unique local search landscape — mobile-first user behaviour, bilingual search queries (Bengali + English), intense competition in key sectors like restaurants and real estate, and the dominance of Google Maps for local discovery. I tailor strategies to these specific Dhaka market dynamics." },
              { question: "Do you offer local Dhaka SEO services?", answer: "Yes, local SEO is my core specialty. I offer comprehensive local SEO services for Dhaka businesses including Google Business Profile optimization, local citation building, neighborhood-specific keyword targeting, review management, and local content creation — all designed to help you rank in Google Maps and local organic search." },
              { question: "How do I get a free SEO audit in Dhaka?", answer: "Getting a free SEO audit is simple. Just contact me through the form on this page or visit my contact page. I'll analyze your current online presence — including your website, Google Business Profile, and local competition — and provide a detailed report with actionable recommendations tailored to your Dhaka business." },
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

      {/* === DISCOVER OUR SERVICES === */}
      <section className="py-16 px-4 bg-gray-50/50">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-10">
            <h2 className="text-3xl md:text-5xl font-extrabold mb-4">
              Discover Our <span className="text-primary">Services</span>
            </h2>
            <p className="text-gray-600 max-w-2xl mx-auto">
              Explore our comprehensive SEO services designed to help your business rank higher and grow faster.
            </p>
          </div>
          <div className="flex flex-wrap justify-center gap-3">
            <Link href="/services/local-seo" className="bg-blue-50 text-primary px-4 py-2 rounded-full hover:bg-primary hover:text-white transition-all text-sm font-medium">Local SEO</Link>
            <Link href="/services/on-page-seo" className="bg-blue-50 text-primary px-4 py-2 rounded-full hover:bg-primary hover:text-white transition-all text-sm font-medium">On-Page SEO</Link>
            <Link href="/services/link-building" className="bg-blue-50 text-primary px-4 py-2 rounded-full hover:bg-primary hover:text-white transition-all text-sm font-medium">Link Building</Link>
            <Link href="/services/technical-seo" className="bg-blue-50 text-primary px-4 py-2 rounded-full hover:bg-primary hover:text-white transition-all text-sm font-medium">Technical SEO</Link>
            <Link href="/services/geo-ai-search" className="bg-blue-50 text-primary px-4 py-2 rounded-full hover:bg-primary hover:text-white transition-all text-sm font-medium">GEO/AI Search</Link>
            <Link href="/services/ecommerce-seo" className="bg-blue-50 text-primary px-4 py-2 rounded-full hover:bg-primary hover:text-white transition-all text-sm font-medium">E-commerce SEO</Link>
            <Link href="/services/semantic-seo" className="bg-blue-50 text-primary px-4 py-2 rounded-full hover:bg-primary hover:text-white transition-all text-sm font-medium">Semantic SEO</Link>
          </div>
          <div className="flex flex-wrap justify-center gap-4 mt-8">
            <Link href="/blog" className="bg-primary text-white px-6 py-3 rounded-full font-semibold hover:bg-primary-dark transition-all text-sm">📖 Read Our SEO Blog →</Link>
            <Link href="/industries" className="border-2 border-primary text-primary px-6 py-3 rounded-full font-semibold hover:bg-primary hover:text-white transition-all text-sm">🏭 See All Industries →</Link>
          </div>
        </div>
      </section>

      {/* === CTA === */}
      <section className="relative py-24 px-4 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-primary to-primary-dark" />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] bg-gradient-to-r from-primary/20 to-primary/20 rounded-full blur-3xl" />
        <div className="relative max-w-2xl mx-auto text-center">
          <h2 className="text-3xl md:text-5xl font-extrabold mb-4 text-white">
            Get Free <span className="text-amber-300">Dhaka SEO Audit</span>
          </h2>
          <p className="text-primary/80 mb-10 text-lg">
            Ready to dominate Dhaka&apos;s local search results? Let me analyze your current SEO and show you exactly how to rank higher in your neighborhood.
          </p>
          <Link href="/contact" className="group inline-flex items-center gap-2 bg-white text-primary-dark px-10 py-4 rounded-xl font-bold text-lg transition-all hover:shadow-xl hover:-translate-y-0.5">
            Claim Your Free Audit
            <span className="group-hover:translate-x-1 transition-transform">→</span>
          </Link>
        </div>
      </section>

      {/* === FOOTER === */}
      <footer className="py-8 border-t border-gray-100 text-center text-sm text-gray-500">
        <p>© 2026 <span className="text-primary font-bold">Md Kanok Miah</span> — SEO Expert in Bangladesh. All rights reserved.</p>
        <div className="mt-3 flex items-center justify-center gap-4 text-xs">
          <Link href="/about" className="hover:text-primary transition-colors">About</Link>
          <Link href="/privacy-policy" className="hover:text-primary transition-colors">Privacy Policy</Link>
          <Link href="/terms-of-service" className="hover:text-primary transition-colors">Terms of Service</Link>
        </div>
      </footer>
    </div>
  );
}
// force rebuild Thu Jul  9 07:58:51 UTC 2026
