"use client";

import Navbar from "@/components/Navbar";
import Link from "next/link";
import { BreadcrumbSchema, FAQSchema } from "@/components/Schema";

const businessTypes = [
  { icon: "🚢", name: "Port & Shipping", desc: "SEO for Chittagong port businesses — attract global trade partners with optimized marine industry content focused on the Bay of Bengal shipping routes." },
  { icon: "📦", name: "Import / Export", desc: "Dominate import-export search results in Chittagong with targeted B2B SEO strategies that connect you with international buyers." },
  { icon: "🏭", name: "Logistics & Warehousing", desc: "Rank your logistics company higher for freight forwarding and warehouse services in Chittagong's growing industrial zones." },
  { icon: "🛍️", name: "Retail & E-commerce", desc: "Boost online sales for Chittagong-based retailers and e-commerce stores with local SEO targeting port city consumers." },
  { icon: "🏨", name: "Hospitality & Travel", desc: "Get more bookings for Chittagong hotels, resorts, and travel agencies with local search optimization and Google Maps visibility." },
  { icon: "🏗️", name: "Manufacturing", desc: "Help manufacturers in Chittagong get found by local and international buyers searching online for Bangladeshi industrial products." },
];

const trustPoints = [
  { icon: "📍", title: "Google Maps Ranking", desc: "Proven strategies to get your Chittagong business to the top of Google Maps and local search results." },
  { icon: "📋", title: "GBP Optimization", desc: "Expert Google Business Profile optimization for maximum local visibility in Chittagong." },
  { icon: "⏳", title: "Since 2019", desc: "Over half a decade of hands-on SEO experience specializing in the Bangladesh market." },
  { icon: "🚀", title: "210+ Projects", desc: "Successfully delivered 210+ SEO projects for businesses across Bangladesh including Chittagong.", hasLink: true },
];

export default function ChittagongClient() {

  return (
    <div className="min-h-screen bg-white text-gray-900">
      <meta name="robots" content="index, follow" />
      {BreadcrumbSchema([
        { name: "Home", url: "https://kanokmiah.com.bd" },
        { name: "Locations", url: "https://kanokmiah.com.bd/locations" },
        { name: "Chittagong", url: "https://kanokmiah.com.bd/locations/chittagong" },
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
            Chittagong SEO Services
          </div>
          <h1 className="text-4xl md:text-6xl lg:text-7xl font-extrabold tracking-tight leading-[1.05] mb-6">
            <span className="block text-primary">Top SEO Expert in Chittagong</span>
            <span className="block">Grow Your Business Online</span>
          </h1>
          <p className="text-lg md:text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
            As a dedicated SEO expert serving Chittagong, I specialize in helping port city businesses — from import/export companies to logistics providers — dominate Google search and attract more customers online.
          </p>
          <div className="mt-8 flex flex-wrap justify-center gap-4">
            <Link href="/contact" className="bg-primary text-white font-bold px-8 py-3.5 rounded-full hover:bg-primary-dark hover:shadow-lg hover:shadow-primary/25 transition-all">
              Get Free Chittagong SEO Audit
            </Link>
            <Link href="/portfolio" className="border-2 border-primary text-primary font-bold px-8 py-3.5 rounded-full hover:bg-primary hover:text-white transition-all">
              View My Work
            </Link>
          </div>
        </div>
      </section>

      {/* === SEO FOR CHITTAGONG BUSINESSES === */}
      <section className="relative py-16 px-4 bg-gray-50/50">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <span className="text-primary text-sm font-semibold tracking-widest uppercase">Industry Focus</span>
            <h2 className="text-3xl md:text-5xl font-extrabold mt-3 mb-4">
              SEO for Chittagong <span className="text-primary">Businesses</span>
            </h2>
            <p className="text-gray-600 max-w-2xl mx-auto">
              Tailored SEO strategies for Chittagong&apos;s unique port city economy — from shipping to retail.
            </p>
          </div>
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
            {businessTypes.map((biz, i) => (
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
              Why Choose Me for <span className="text-primary">Chittagong SEO</span>
            </h2>
            <p className="text-gray-600 max-w-2xl mx-auto">
              What sets my Chittagong SEO services apart from the competition.
            </p>
          </div>
          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-5">
            {trustPoints.map((point, i) => (
              <div key={i} className="bg-gray-50 border border-gray-100 rounded-2xl p-6 text-center hover:bg-gray-100 hover:border-gray-200 transition-all hover:-translate-y-1">
                <div className="text-4xl mb-4">{point.icon}</div>
                <h3 className="font-bold text-lg mb-2 text-gray-900">{point.title}</h3>
                <p className="text-gray-600 text-sm leading-relaxed">{point.hasLink ? <>Successfully delivered 210+ <Link href="/services" className="text-primary font-semibold hover:underline">SEO</Link> projects for businesses across Bangladesh{point.desc.includes("including") ? " including " + point.desc.split("including")[1] : "."}</> : point.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* === ABOUT CHITTAGONG === */}
      <section className="relative py-16 px-4 bg-white">
        <div className="max-w-4xl mx-auto">
          <span className="text-primary text-sm font-semibold tracking-widest uppercase block text-center">About Chittagong</span>
          <h2 className="text-3xl md:text-5xl font-extrabold mt-3 mb-6 text-center">
            Why Chittagong <span className="text-primary">Needs SEO</span>
          </h2>
          <div className="space-y-4 text-gray-600 leading-relaxed">
            <p>Chittagong, the commercial capital of Bangladesh and home to the country&apos;s largest seaport, is a powerhouse of trade and industry. The Port of Chittagong handles over 90% of Bangladesh&apos;s international maritime trade, making the city a vital hub for shipping, logistics, import/export, and manufacturing businesses. With landmarks like the Chittagong Hill Tracts, Patenga Beach, Foy&apos;s Lake, and the historic Naval Academy, the city attracts both business travelers and tourists.</p>
            <p>The city&apos;s economy is uniquely driven by port-related activities, heavy industry, and a growing service sector. Major industrial areas like the Chittagong Export Processing Zone (CEPZ), Karnaphuli EPZ, and Shitalpur EPZ house hundreds of factories producing garments, textiles, chemicals, and consumer goods. Additionally, Chittagong has a thriving retail scene in areas like Agrabad, GEC Circle, and Oxygen-Moor, with countless local businesses competing for customer attention.</p>
            <p>In this highly competitive environment, having a strong online presence is no longer optional. Chittagong businesses — from cargo shipping companies to local restaurants — need SEO to stand out, attract customers, and grow. My Chittagong SEO services are specifically designed to help local businesses capture search traffic from the thousands of daily Google searches originating in the port city. By optimizing for local keywords like &quot;shipping agent in Chittagong,&quot; &quot;logistics company Chittagong,&quot; and &quot;restaurants near Agrabad,&quot; I help businesses get found by the right customers at the right time.</p>
          </div>
        </div>
      </section>

      {/* === LOCAL SUCCESS STORIES === */}
      <section className="relative py-16 px-4 bg-gray-50/50">
        <div className="max-w-4xl mx-auto">
          <span className="text-primary text-sm font-semibold tracking-widest uppercase block text-center">Local Success</span>
          <h2 className="text-3xl md:text-5xl font-extrabold mt-3 mb-6 text-center">
            Chittagong <span className="text-primary">Case Studies</span>
          </h2>
          <div className="space-y-6">
            <div className="bg-white border border-gray-100 rounded-2xl p-6 md:p-8 hover:shadow-md transition-all">
              <div className="flex items-start gap-4">
                <div className="text-4xl shrink-0">📦</div>
                <div>
                  <h3 className="font-bold text-xl text-gray-900 mb-2">Chittagong Logistics Company</h3>
                  <p className="text-gray-600 text-sm leading-relaxed">A Chittagong-based freight forwarding and logistics company was struggling to rank for &quot;freight forwarder in Bangladesh&quot; and &quot;cargo service Chittagong.&quot; After implementing a comprehensive local SEO strategy including Google Business Profile optimization, local citation building on trade directories, and content targeting import/export keywords, the company saw a 180% increase in organic traffic within 4 months. Their Google Maps listing moved from page 3 to the top 3 local pack results for &quot;logistics company Chittagong,&quot; resulting in 25+ qualified B2B inquiries per month.</p>
                </div>
              </div>
            </div>
            <div className="bg-white border border-gray-100 rounded-2xl p-6 md:p-8 hover:shadow-md transition-all">
              <div className="flex items-start gap-4">
                <div className="text-4xl shrink-0">🏨</div>
                <div>
                  <h3 className="font-bold text-xl text-gray-900 mb-2">Chittagong Hotel Booking Growth</h3>
                  <p className="text-gray-600 text-sm leading-relaxed">A mid-sized hotel near Patenga Beach was losing bookings to competitors on Google Maps. We optimized their Google Business Profile with high-quality photos of rooms and amenities, added local landmarks (Patenga Beach, Naval Academy Road) to their service area, and generated 15+ positive Google reviews through a structured review campaign. Within 8 weeks, their direct booking inquiries increased by 65%, and they appeared in the top 3 Google Maps results for &quot;hotel near Patenga Beach Chittagong.&quot;</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* === FAQ === */}
      <section className="py-16 px-4 bg-white">
        <div className="max-w-4xl mx-auto">
          <FAQSchema faqs={[
            { question: "What areas of Chittagong do you cover?", answer: "I cover all areas of Chittagong including Agrabad, Halishahar, Nasirabad, Panchlaish, Chandgaon, Patenga, EPZ, Khulshi, Kotwali, and all other commercial and residential neighborhoods. My localized SEO approach targets customers in specific Chittagong areas to maximize local visibility." },
            { question: "How can Chittagong businesses benefit from SEO?", answer: "Chittagong businesses — especially in port, shipping, logistics, import/export, and manufacturing — can benefit tremendously from SEO by capturing high-intent B2B buyers searching for suppliers in Bangladesh. Local businesses like restaurants, hotels, and retailers also gain significant visibility through Google Maps optimization and local keyword targeting." },
            { question: "Do you offer on-site consultation in Chittagong?", answer: "Yes, I offer both remote and on-site consultation for Chittagong businesses. While most of my SEO work is delivered remotely with regular progress updates, I am available for in-person meetings in Chittagong to discuss strategy, conduct on-site audits, and provide personalized recommendations." },
            { question: "How is Chittagong's port economy different for SEO?", answer: "Chittagong's economy is uniquely tied to the Port of Chittagong, the largest seaport in Bangladesh handling over 90% of the country's international trade. This creates distinct SEO opportunities for B2B businesses targeting international buyers searching for Bangladeshi suppliers, freight forwarders, and shipping agents. My SEO strategies leverage these unique economic drivers to help Chittagong businesses dominate both local and global search results." },
            { question: "What is the first step for Chittagong businesses?", answer: "The first step is to get a free SEO audit. Contact me through this page, and I'll analyze your current online presence — website performance, Google Business Profile, competitor landscape, and keyword opportunities — then provide a clear roadmap tailored to your Chittagong business goals." },
          ]} />
          <h2 className="text-2xl md:text-3xl font-extrabold text-center mb-8">
            Frequently Asked <span className="text-primary">Questions</span>
          </h2>
          <div className="space-y-0 divide-y divide-gray-100">
            {[
              { question: "What areas of Chittagong do you cover?", answer: "I cover all areas of Chittagong including Agrabad, Halishahar, Nasirabad, Panchlaish, Chandgaon, Patenga, EPZ, Khulshi, Kotwali, and all other commercial and residential neighborhoods. My localized SEO approach targets customers in specific Chittagong areas to maximize local visibility." },
              { question: "How can Chittagong businesses benefit from SEO?", answer: "Chittagong businesses — especially in port, shipping, logistics, import/export, and manufacturing — can benefit tremendously from SEO by capturing high-intent B2B buyers searching for suppliers in Bangladesh. Local businesses like restaurants, hotels, and retailers also gain significant visibility through Google Maps optimization and local keyword targeting." },
              { question: "Do you offer on-site consultation in Chittagong?", answer: "Yes, I offer both remote and on-site consultation for Chittagong businesses. While most of my SEO work is delivered remotely with regular progress updates, I am available for in-person meetings in Chittagong to discuss strategy, conduct on-site audits, and provide personalized recommendations." },
              { question: "How is Chittagong's port economy different for SEO?", answer: "Chittagong's economy is uniquely tied to the Port of Chittagong, the largest seaport in Bangladesh handling over 90% of the country's international trade. This creates distinct SEO opportunities for B2B businesses targeting international buyers searching for Bangladeshi suppliers, freight forwarders, and shipping agents. My SEO strategies leverage these unique economic drivers to help Chittagong businesses dominate both global and local search results." },
              { question: "What is the first step for Chittagong businesses?", answer: "The first step is to get a free SEO audit. Contact me through this page, and I'll analyze your current online presence — website performance, Google Business Profile, competitor landscape, and keyword opportunities — then provide a clear roadmap tailored to your Chittagong business goals." },
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
            Get Free <span className="text-amber-300">Chittagong SEO Audit</span>
          </h2>
          <p className="text-white/80 mb-10 text-lg">
            Ready to grow your Chittagong business online? Let me analyze your current SEO and create a customized plan to dominate local search results.
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
