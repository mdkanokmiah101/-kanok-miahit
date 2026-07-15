"use client";

import Navbar from "@/components/Navbar";
import Link from "next/link";
import { BreadcrumbSchema, FAQSchema } from "@/components/Schema";

const sylhetMarkets = [
  { icon: "🍽️", name: "Restaurants & Cafés", desc: "Dominate local restaurant searches in Sylhet — attract diners searching for the best food in town, from traditional pitha houses to modern cafes." },
  { icon: "🏨", name: "Hotels & Resorts", desc: "Get more direct bookings for Sylhet hotels and resorts with local SEO and Google Maps optimization targeting tourists and business travelers." },
  { icon: "✈️", name: "Overseas Businesses", desc: "SEO for Sylheti diaspora businesses — connect with customers in the UK, USA, and Middle East who are searching for services back home." },
  { icon: "🛒", name: "E-commerce Stores", desc: "Boost online sales for Sylhet-based e-commerce stores with targeted local and international SEO strategies." },
  { icon: "🏡", name: "Real Estate", desc: "Help Sylhet real estate agents and developers get found by property buyers searching online for homes in Sylhet city." },
  { icon: "🏥", name: "Healthcare & Clinics", desc: "Rank your Sylhet clinic or hospital higher for medical searches — attract more local patients looking for healthcare services." },
];

const trustPoints = [
  { icon: "📍", title: "Google Maps Ranking", desc: "Proven strategies to get your Sylhet business to the top of Google Maps and local search results." },
  { icon: "📋", title: "GBP Optimization", desc: "Expert Google Business Profile optimization for maximum visibility in Sylhet's local market." },
  { icon: "⏳", title: "Since 2019", desc: "Over half a decade of hands-on SEO experience specializing in the Bangladesh market." },
  { icon: "🚀", title: "210+ Projects", desc: "Successfully delivered 210+ SEO projects for businesses across Bangladesh including Sylhet.", hasLink: true },
];

export default function SylhetClient() {

  return (
    <div className="min-h-screen bg-white text-gray-900">
      <meta name="robots" content="index, follow" />
      {BreadcrumbSchema([
        { name: "Home", url: "https://kanokmiah.com.bd" },
        { name: "Locations", url: "https://kanokmiah.com.bd/locations" },
        { name: "Sylhet", url: "https://kanokmiah.com.bd/locations/sylhet" },
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
            Sylhet SEO Services
          </div>
          <h1 className="text-4xl md:text-6xl lg:text-7xl font-extrabold tracking-tight leading-[1.05] mb-6">
            <span className="block text-primary">Local SEO Expert in Sylhet</span>
            <span className="block">Dominate Google Maps</span>
          </h1>
          <p className="text-lg md:text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
            Your trusted local SEO partner in Sylhet. I help restaurants, hotels, overseas businesses, and local service providers dominate Google Maps and attract more customers — both locally and from the Sylheti diaspora worldwide.
          </p>
          <div className="mt-8 flex flex-wrap justify-center gap-4">
            <Link href="/contact" className="bg-primary text-white font-bold px-8 py-3.5 rounded-full hover:bg-primary-dark hover:shadow-lg hover:shadow-primary/25 transition-all">
              Get Free Sylhet SEO Audit
            </Link>
            <Link href="/portfolio" className="border-2 border-primary text-primary font-bold px-8 py-3.5 rounded-full hover:bg-primary hover:text-white transition-all">
              View My Work
            </Link>
          </div>
        </div>
      </section>

      {/* === SEO FOR SYLHET BUSINESSES === */}
      <section className="relative py-16 px-4 bg-gray-50/50">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <span className="text-primary text-sm font-semibold tracking-widest uppercase">Market Focus</span>
            <h2 className="text-3xl md:text-5xl font-extrabold mt-3 mb-4">
              SEO for Sylhet&apos;s <span className="text-primary">Unique Market</span>
            </h2>
            <p className="text-gray-600 max-w-2xl mx-auto">
              Tailored SEO strategies for Sylhet&apos;s distinctive business landscape — from local restaurants to overseas enterprises.
            </p>
          </div>
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
            {sylhetMarkets.map((biz, i) => (
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
              Why Choose Me for <span className="text-primary">Sylhet SEO</span>
            </h2>
            <p className="text-gray-600 max-w-2xl mx-auto">
              What sets my Sylhet SEO services apart from the competition.
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

      {/* === ABOUT SYLHET === */}
      <section className="relative py-16 px-4 bg-white">
        <div className="max-w-4xl mx-auto">
          <span className="text-primary text-sm font-semibold tracking-widest uppercase block text-center">About Sylhet</span>
          <h2 className="text-3xl md:text-5xl font-extrabold mt-3 mb-6 text-center">
            Why Sylhet <span className="text-primary">Needs SEO</span>
          </h2>
          <div className="space-y-4 text-gray-600 leading-relaxed">
            <p>Sylhet, known as the spiritual and cultural capital of eastern Bangladesh, is a city of immense natural beauty and economic significance. Famous for its rolling tea gardens — including the renowned Srimangal tea estates — lush hills, and the iconic Ratargul Swamp Forest, Sylhet attracts thousands of domestic and international tourists every year. Key landmarks like the Hazrat Shahjalal Mazar Sharif, Jaflong, Bichanakandi, and Lalakhal add to the city&apos;s cultural and religious importance.</p>
            <p>What truly sets Sylhet apart is its strong overseas diaspora connection. A significant portion of the Bangladeshi community in the United Kingdom, United States, and Middle East hails from the Sylhet region. This creates a unique dual-market dynamic where Sylheti businesses serve both local customers and the global Sylheti diaspora seeking services, products, and real estate investments back home. From restaurants serving authentic Sylheti cuisine to travel agencies organizing UK-Bangladesh flights, the local economy is deeply intertwined with international connections.</p>
            <p>The hospitality sector thrives in Sylhet, with hotels and resorts catering to religious tourists visiting the Hazrat Shahjalal shrine and nature lovers exploring the surrounding tea country. Real estate is another booming sector, driven by diaspora investments and a growing middle class. My Sylhet SEO services specifically target these unique market dynamics, helping local businesses capture search traffic from both Sylhet city residents and the vast overseas diaspora searching for services in their hometown.</p>
          </div>
        </div>
      </section>

      {/* === LOCAL SUCCESS STORIES === */}
      <section className="relative py-16 px-4 bg-gray-50/50">
        <div className="max-w-4xl mx-auto">
          <span className="text-primary text-sm font-semibold tracking-widest uppercase block text-center">Local Success</span>
          <h2 className="text-3xl md:text-5xl font-extrabold mt-3 mb-6 text-center">
            Sylhet <span className="text-primary">Case Studies</span>
          </h2>
          <div className="space-y-6">
            <div className="bg-white border border-gray-100 rounded-2xl p-6 md:p-8 hover:shadow-md transition-all">
              <div className="flex items-start gap-4">
                <div className="text-4xl shrink-0">🍽️</div>
                <div>
                  <h3 className="font-bold text-xl text-gray-900 mb-2">Sylhet Restaurant Found Online</h3>
                  <p className="text-gray-600 text-sm leading-relaxed">A popular Sylheti restaurant near the Hazrat Shahjalal shrine was struggling to appear on Google Maps despite having excellent food and service. After optimizing their Google Business Profile with updated menus, real photos of their signature dishes, and implementing a structured Google review campaign, the restaurant jumped from outside the top 20 to the #3 position for &quot;restaurants near Shahjalal Sylhet&quot; within 6 weeks. Their monthly Google Maps discovery searches increased by 340%, leading to a 40% rise in foot traffic from tourists visiting the shrine.</p>
                </div>
              </div>
            </div>
            <div className="bg-white border border-gray-100 rounded-2xl p-6 md:p-8 hover:shadow-md transition-all">
              <div className="flex items-start gap-4">
                <div className="text-4xl shrink-0">🏡</div>
                <div>
                  <h3 className="font-bold text-xl text-gray-900 mb-2">Sylhet Real Estate Agent Success</h3>
                  <p className="text-gray-600 text-sm leading-relaxed">A Sylhet-based real estate agency serving both local buyers and UK-based diaspora investors wanted to capture search traffic for property keywords. We implemented a dual-language SEO strategy targeting &quot;flats in Sylhet city&quot; and &quot;Sylhet property for UK buyers.&quot; With localized landing pages for popular neighborhoods and schema markup for property listings, organic traffic grew 220% in 3 months, with a significant portion coming from UK-based Sylheti diaspora searching for investment properties back home.</p>
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
            { question: "Do you serve Sylhet businesses?", answer: "Absolutely. I provide full-service SEO for businesses in Sylhet — from restaurants and hotels to real estate agencies and e-commerce stores. I understand Sylhet's unique business landscape, including the strong overseas diaspora connection, and tailor strategies that work for both local and international audiences." },
            { question: "How can Sylhet-based businesses rank nationally?", answer: "Sylhet businesses can rank nationally by targeting Bangladesh-wide keywords, creating high-quality content that appeals to a broader audience, building authoritative backlinks from national publications, and optimizing for both Bengali and English search queries. I help Sylhet businesses expand beyond local markets and compete on a national level." },
            { question: "Do you understand the Sylhet market?", answer: "Yes, I have deep knowledge of Sylhet's distinctive business environment — including the significant overseas diaspora influence, the city's growing hospitality sector, the unique buying patterns of Sylheti consumers, and the competitive dynamics across local industries. This local insight helps me create more effective SEO strategies for Sylhet businesses." },
            { question: "How does the Sylhet diaspora affect SEO strategy?", answer: "The Sylheti diaspora — particularly in the UK, USA, and Middle East — creates a unique SEO opportunity. Many overseas Sylhetis regularly search for services in Sylhet, including real estate for investment, restaurants for family visits, travel agencies for flights, and remittance services. My Sylhet SEO strategies specifically target these diaspora-driven search queries, helping local businesses capture this valuable international traffic." },
            { question: "How do I contact you from Sylhet?", answer: "You can contact me easily through the contact form on this page, send me an email, or give me a call. I typically respond within 24 hours. For Sylhet businesses, I offer both remote consultations and, where feasible, in-person meetings to discuss your SEO needs face-to-face." },
          ]} />
          <h2 className="text-2xl md:text-3xl font-extrabold text-center mb-8">
            Frequently Asked <span className="text-primary">Questions</span>
          </h2>
          <div className="space-y-0 divide-y divide-gray-100">
            {[
              { question: "Do you serve Sylhet businesses?", answer: "Absolutely. I provide full-service SEO for businesses in Sylhet — from restaurants and hotels to real estate agencies and e-commerce stores. I understand Sylhet's unique business landscape, including the strong overseas diaspora connection, and tailor strategies that work for both local and international audiences." },
              { question: "How can Sylhet-based businesses rank nationally?", answer: "Sylhet businesses can rank nationally by targeting Bangladesh-wide keywords, creating high-quality content that appeals to a broader audience, building authoritative backlinks from national publications, and optimizing for both Bengali and English search queries. I help Sylhet businesses expand beyond local markets and compete on a national level." },
              { question: "Do you understand the Sylhet market?", answer: "Yes, I have deep knowledge of Sylhet's distinctive business environment — including the significant overseas diaspora influence, the city's growing hospitality sector, the unique buying patterns of Sylheti consumers, and the competitive dynamics across local industries. This local insight helps me create more effective SEO strategies for Sylhet businesses." },
              { question: "How does the Sylhet diaspora affect SEO strategy?", answer: "The Sylheti diaspora — particularly in the UK, USA, and Middle East — creates a unique SEO opportunity. Many overseas Sylhetis regularly search for services in Sylhet, including real estate for investment, restaurants for family visits, travel agencies for flights, and remittance services. My Sylhet SEO strategies specifically target these diaspora-driven search queries, helping local businesses capture this valuable international traffic." },
              { question: "How do I contact you from Sylhet?", answer: "You can contact me easily through the contact form on this page, send me an email, or give me a call. I typically respond within 24 hours. For Sylhet businesses, I offer both remote consultations and, where feasible, in-person meetings to discuss your SEO needs face-to-face." },
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
            Get Free <span className="text-amber-300">Sylhet SEO Audit</span>
          </h2>
          <p className="text-white/80 mb-10 text-lg">
            Ready to dominate Google Maps in Sylhet? Let me analyze your current SEO and create a customized plan to help your business get found by more customers.
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
