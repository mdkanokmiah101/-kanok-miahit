"use client";

import Navbar from "@/components/Navbar";
import Link from "next/link";
import { BreadcrumbSchema, FAQSchema } from "@/components/Schema";

const rajshahiBusinesses = [
  { icon: "🥭", name: "Mango & Agri Export", desc: "Dominate agricultural search results for Rajshahi's famous mango and crop exporters targeting local and international buyers." },
  { icon: "🎓", name: "Education & Coaching", desc: "Rank your Rajshahi coaching center or educational institution higher for student searches across the division." },
  { icon: "🛍️", name: "Retail & Local Shops", desc: "Boost foot traffic and online visibility for Rajshahi retail businesses with targeted local Google Maps SEO." },
  { icon: "🏭", name: "Small Manufacturing", desc: "Help Rajshahi's small-scale manufacturers get found by B2B buyers searching for Bangladeshi products." },
  { icon: "🏨", name: "Hotels & Restaurants", desc: "Get more direct bookings for Rajshahi hotels, guest houses, and restaurants with local SEO." },
  { icon: "🏗️", name: "Real Estate & Construction", desc: "Help Rajshahi property developers and real estate agents dominate local property searches." },
];

const trustPoints = [
  { icon: "📍", title: "Google Maps Ranking", desc: "Proven strategies to get your Rajshahi business to the top of Google Maps and local search results." },
  { icon: "📋", title: "GBP Optimization", desc: "Expert Google Business Profile optimization for maximum visibility in Rajshahi's local market." },
  { icon: "⏳", title: "6+ Years Experience", desc: "Over half a decade of hands-on SEO experience specializing in the Bangladesh market including Rajshahi." },
  { icon: "🚀", title: "350+ Projects", desc: "Successfully delivered 350+ SEO projects for businesses across Bangladesh including Rajshahi." },
];

export default function RajshahiClient() {

  return (
    <div className="min-h-screen bg-white text-gray-900">
      <meta name="robots" content="index, follow" />
      {BreadcrumbSchema([
        { name: "Home", url: "https://kanokmiah.com.bd" },
        { name: "Locations", url: "https://kanokmiah.com.bd/locations" },
        { name: "Rajshahi", url: "https://kanokmiah.com.bd/locations/rajshahi" },
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
            Rajshahi SEO Services
          </div>
          <h1 className="text-4xl md:text-6xl lg:text-7xl font-extrabold tracking-tight leading-[1.05] mb-6">
            <span className="text-primary">
              Local SEO Expert in Rajshahi
            </span>
            <br />Dominate Google Maps
          </h1>
          <p className="text-lg md:text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
            Your trusted local SEO partner in Rajshahi. I help mango exporters, educational institutions, retail businesses, and local service providers dominate Google search and attract more customers online.
          </p>
          <div className="mt-8 flex flex-wrap justify-center gap-4">
            <Link href="/contact" className="bg-primary text-white font-bold px-8 py-3.5 rounded-full hover:bg-primary-dark hover:shadow-lg hover:shadow-primary/25 transition-all">
              Get Free Rajshahi SEO Audit
            </Link>
            <Link href="/portfolio" className="border-2 border-primary text-primary font-bold px-8 py-3.5 rounded-full hover:bg-primary hover:text-white transition-all">
              View My Work
            </Link>
          </div>
        </div>
      </section>

      {/* === SEO FOR RAJSHAHI BUSINESSES === */}
      <section className="relative py-16 px-4 bg-gray-50/50">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <span className="text-primary text-sm font-semibold tracking-widest uppercase">Market Focus</span>
            <h2 className="text-3xl md:text-5xl font-extrabold mt-3 mb-4">
              SEO for Rajshahi&apos;s <span className="text-primary">Economy</span>
            </h2>
            <p className="text-gray-600 max-w-2xl mx-auto">
              Tailored SEO strategies for Rajshahi&apos;s unique agricultural and educational economy — from mango export to coaching centers.
            </p>
          </div>
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
            {rajshahiBusinesses.map((biz, i) => (
              <div key={i} className="group bg-white border border-gray-100 rounded-2xl p-6 hover:shadow-lg hover:-translate-y-1 transition-all">
                <div className="text-4xl mb-4">{biz.icon}</div>
                <h3 className="font-bold text-xl mb-2 text-gray-900">{biz.name}</h3>
                <p className="text-gray-600 text-sm leading-relaxed">{biz.desc}</p>
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
              Why Choose Me for <span className="text-primary">Rajshahi SEO</span>
            </h2>
            <p className="text-gray-600 max-w-2xl mx-auto">
              What sets my Rajshahi SEO services apart from the competition.
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
            { question: "How is SEO different for Rajshahi businesses?", answer: "Rajshahi's economy is uniquely driven by agriculture — especially mango export — and education. My SEO strategies for Rajshahi businesses focus on bilingual Bengali + English optimization, Google Maps ranking for local service providers, and targeted keyword strategies for agricultural exporters and educational institutions looking to attract both local and national audiences." },
            { question: "Do you serve Rajshahi city and surrounding areas?", answer: "Yes, I provide SEO services for Rajshahi city and all surrounding areas including the Rajshahi University area, Kadirganj, Motihar, Shaheb Bazar, and all upazillas across the Rajshahi division. My hyperlocal approach helps businesses attract customers from all over the region." },
            { question: "What types of Rajshahi businesses benefit most from SEO?", answer: "Mango and crop exporters, coaching centers, local retailers, small manufacturers, hotels, restaurants, and real estate developers all benefit greatly from SEO. I help Rajshahi businesses build their online presence, attract more customers, and compete effectively beyond local boundaries." },
            { question: "How do I get started with SEO in Rajshahi?", answer: "Getting started is simple. Contact me through this page for a free SEO audit. I will analyze your current online presence, evaluate your competition in the Rajshahi market, and create a customized SEO strategy tailored to your business goals and target audience." },
          ]} />
          <h2 className="text-2xl md:text-3xl font-extrabold text-center mb-8">
            Frequently Asked <span className="text-primary">Questions</span>
          </h2>
          <div className="space-y-0 divide-y divide-gray-100">
            {[
              { question: "How is SEO different for Rajshahi businesses?", answer: "Rajshahi's economy is uniquely driven by agriculture — especially mango export — and education. My SEO strategies for Rajshahi businesses focus on bilingual Bengali + English optimization, Google Maps ranking for local service providers, and targeted keyword strategies for agricultural exporters and educational institutions looking to attract both local and national audiences." },
              { question: "Do you serve Rajshahi city and surrounding areas?", answer: "Yes, I provide SEO services for Rajshahi city and all surrounding areas including the Rajshahi University area, Kadirganj, Motihar, Shaheb Bazar, and all upazillas across the Rajshahi division. My hyperlocal approach helps businesses attract customers from all over the region." },
              { question: "What types of Rajshahi businesses benefit most from SEO?", answer: "Mango and crop exporters, coaching centers, local retailers, small manufacturers, hotels, restaurants, and real estate developers all benefit greatly from SEO. I help Rajshahi businesses build their online presence, attract more customers, and compete effectively beyond local boundaries." },
              { question: "How do I get started with SEO in Rajshahi?", answer: "Getting started is simple. Contact me through this page for a free SEO audit. I will analyze your current online presence, evaluate your competition in the Rajshahi market, and create a customized SEO strategy tailored to your business goals and target audience." },
            ].map((f, i) => (
              <details key={i} className="py-4 group">
                <summary className="font-semibold text-gray-900 cursor-pointer list-none flex justify-between items-center">
                  {f.question}
                  <span className="text-primary transition-transform group-open:rotate-180">&#9660;</span>
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
            <Link href="/blog" className="bg-primary text-white px-6 py-3 rounded-full font-semibold hover:bg-primary-dark transition-all text-sm">Read Our SEO Blog</Link>
            <Link href="/industries" className="border-2 border-primary text-primary px-6 py-3 rounded-full font-semibold hover:bg-primary hover:text-white transition-all text-sm">See All Industries</Link>
          </div>
        </div>
      </section>

      {/* === CTA === */}
      <section className="relative py-24 px-4 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-primary to-primary-dark" />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] bg-gradient-to-r from-primary/20 to-primary/20 rounded-full blur-3xl" />
        <div className="relative max-w-2xl mx-auto text-center">
          <h2 className="text-3xl md:text-5xl font-extrabold mb-4 text-white">
            Get Free <span className="text-amber-300">Rajshahi SEO Audit</span>
          </h2>
          <p className="text-primary/80 mb-10 text-lg">
            Ready to dominate Google Maps in Rajshahi? Let me analyze your current SEO and create a customized plan to help your business get found by more customers.
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
