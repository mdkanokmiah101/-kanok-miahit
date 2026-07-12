"use client";

import Navbar from "@/components/Navbar";
import Link from "next/link";
import { BreadcrumbSchema, FAQSchema } from "@/components/Schema";

const khulnaBusinesses = [
  { icon: "🦐", name: "Shrimp & Seafood Export", desc: "Dominate global seafood search results for Khulna-based shrimp and fish exporters targeting international buyers." },
  { icon: "🏭", name: "Industrial & Manufacturing", desc: "Rank your Khulna factory higher for B2B searches — attract industrial buyers searching for Bangladeshi manufacturers." },
  { icon: "🌾", name: "Agriculture & Jute", desc: "Help Khulna agri-businesses and jute exporters get found online with targeted local SEO strategies." },
  { icon: "🛍️", name: "Retail & E-commerce", desc: "Boost online sales for Khulna-based retailers and e-commerce stores reaching customers across Bangladesh." },
  { icon: "🏨", name: "Hotels & Hospitality", desc: "Get more bookings for Khulna hotels, resorts, and restaurants with Google Maps optimization." },
  { icon: "🏗️", name: "Construction & Real Estate", desc: "Help Khulna property developers and construction firms dominate local real estate searches." },
];

const trustPoints = [
  { icon: "📍", title: "Google Maps Ranking", desc: "Proven strategies to get your Khulna business to the top of Google Maps and local search results." },
  { icon: "📋", title: "GBP Optimization", desc: "Expert Google Business Profile optimization for maximum visibility in Khulna's local market." },
  { icon: "⏳", title: "Since 2019", desc: "Over half a decade of hands-on SEO experience specializing in the Bangladesh market including Khulna." },
  { icon: "🚀", title: "210+ Projects", desc: "Successfully delivered 210+ SEO projects for businesses across Bangladesh including Khulna." },
];

export default function KhulnaClient() {

  return (
    <div className="min-h-screen bg-white text-gray-900">
      <meta name="robots" content="index, follow" />
      {BreadcrumbSchema([
        { name: "Home", url: "https://kanokmiah.com.bd" },
        { name: "Locations", url: "https://kanokmiah.com.bd/locations" },
        { name: "Khulna", url: "https://kanokmiah.com.bd/locations/khulna" },
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
            Khulna SEO Services
          </div>
          <h1 className="text-4xl md:text-6xl lg:text-7xl font-extrabold tracking-tight leading-[1.05] mb-6">
            <span className="text-primary">
              Local SEO Expert in Khulna
            </span>
            <br />Dominate Google Maps
          </h1>
          <p className="text-lg md:text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
            Your trusted local SEO partner in Khulna. I help shrimp exporters, industrial businesses, agri-companies, and local service providers dominate Google search and attract more customers online.
          </p>
          <div className="mt-8 flex flex-wrap justify-center gap-4">
            <Link href="/contact" className="bg-primary text-white font-bold px-8 py-3.5 rounded-full hover:bg-primary-dark hover:shadow-lg hover:shadow-primary/25 transition-all">
              Get Free Khulna SEO Audit
            </Link>
            <Link href="/portfolio" className="border-2 border-primary text-primary font-bold px-8 py-3.5 rounded-full hover:bg-primary hover:text-white transition-all">
              View My Work
            </Link>
          </div>
        </div>
      </section>

      {/* === SEO FOR KHULNA BUSINESSES === */}
      <section className="relative py-16 px-4 bg-gray-50/50">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <span className="text-primary text-sm font-semibold tracking-widest uppercase">Industry Focus</span>
            <h2 className="text-3xl md:text-5xl font-extrabold mt-3 mb-4">
              SEO for Khulna&apos;s <span className="text-primary">Industries</span>
            </h2>
            <p className="text-gray-600 max-w-2xl mx-auto">
              Tailored SEO strategies for Khulna&apos;s distinctive industrial economy — from shrimp export to manufacturing.
            </p>
          </div>
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
            {khulnaBusinesses.map((biz, i) => (
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
              Why Choose Me for <span className="text-primary">Khulna SEO</span>
            </h2>
            <p className="text-gray-600 max-w-2xl mx-auto">
              What sets my Khulna SEO services apart from the competition.
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
            { question: "How is SEO different for Khulna businesses?", answer: "Khulna businesses — especially in shrimp export, industrial manufacturing, and agriculture — need a specialized approach that targets both local B2B buyers and international markets. My Khulna SEO strategies focus on bilingual English + Bengali optimization, Google Maps ranking for local service providers, and industry-specific keyword targeting for export-oriented businesses." },
            { question: "Do you serve Khulna city and surrounding areas?", answer: "Yes, I provide SEO services for Khulna city and all surrounding areas including the Khulna Industrial Zone, Rupsha, Daulatpur, and Sonadanga. My hyperlocal SEO approach helps businesses across the Khulna division attract more customers both locally and nationally." },
            { question: "What types of Khulna businesses benefit most from SEO?", answer: "All types of Khulna businesses benefit from SEO — shrimp exporters looking for international buyers, local manufacturers, retail shops, hotels, restaurants, and real estate developers. SEO helps Khulna businesses build credibility, attract more customers, and compete effectively in both local and national markets." },
            { question: "How do I get started with SEO in Khulna?", answer: "Getting started is simple. Contact me through this page for a free SEO audit. I will analyze your current online presence, evaluate your competition in the Khulna market, and create a customized SEO strategy tailored to your business goals and target audience." },
          ]} />
          <h2 className="text-2xl md:text-3xl font-extrabold text-center mb-8">
            Frequently Asked <span className="text-primary">Questions</span>
          </h2>
          <div className="space-y-0 divide-y divide-gray-100">
            {[
              { question: "How is SEO different for Khulna businesses?", answer: "Khulna businesses — especially in shrimp export, industrial manufacturing, and agriculture — need a specialized approach that targets both local B2B buyers and international markets. My Khulna SEO strategies focus on bilingual English + Bengali optimization, Google Maps ranking for local service providers, and industry-specific keyword targeting for export-oriented businesses." },
              { question: "Do you serve Khulna city and surrounding areas?", answer: "Yes, I provide SEO services for Khulna city and all surrounding areas including the Khulna Industrial Zone, Rupsha, Daulatpur, and Sonadanga. My hyperlocal SEO approach helps businesses across the Khulna division attract more customers both locally and nationally." },
              { question: "What types of Khulna businesses benefit most from SEO?", answer: "All types of Khulna businesses benefit from SEO — shrimp exporters looking for international buyers, local manufacturers, retail shops, hotels, restaurants, and real estate developers. SEO helps Khulna businesses build credibility, attract more customers, and compete effectively in both local and national markets." },
              { question: "How do I get started with SEO in Khulna?", answer: "Getting started is simple. Contact me through this page for a free SEO audit. I will analyze your current online presence, evaluate your competition in the Khulna market, and create a customized SEO strategy tailored to your business goals and target audience." },
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
            Get Free <span className="text-amber-300">Khulna SEO Audit</span>
          </h2>
          <p className="text-primary/80 mb-10 text-lg">
            Ready to dominate Google Maps in Khulna? Let me analyze your current SEO and create a customized plan to help your business get found by more customers.
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
