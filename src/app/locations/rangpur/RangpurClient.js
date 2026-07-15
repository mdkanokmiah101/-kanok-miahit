"use client";

import Navbar from "@/components/Navbar";
import Link from "next/link";
import { BreadcrumbSchema, FAQSchema } from "@/components/Schema";

const rangpurBusinesses = [
  { icon: "🌾", name: "Agriculture & Tobacco", desc: "Dominate local agricultural SEO for Rangpur's tobacco, rice, and potato farming businesses." },
  { icon: "🏭", name: "Manufacturing & Industry", desc: "Help Rangpur's industrial and manufacturing sector attract B2B buyers through search." },
  { icon: "🎓", name: "Education & Coaching", desc: "Rank Rangpur's educational institutions higher for student recruitment searches." },
  { icon: "🛍️", name: "Retail & E-commerce", desc: "Boost online visibility for Rangpur-based retailers and e-commerce stores." },
  { icon: "🏨", name: "Hotels & Hospitality", desc: "Get more bookings for Rangpur hotels, resorts, and restaurants with local SEO." },
  { icon: "🏗️", name: "Construction & Real Estate", desc: "Help Rangpur property developers dominate local real estate searches." },
];

const trustPoints = [
  { icon: "📍", title: "Google Maps Ranking", desc: "Proven strategies to get your Rangpur business to the top of Google Maps and local search results." },
  { icon: "📋", title: "GBP Optimization", desc: "Expert Google Business Profile optimization for maximum visibility in Rangpur's local market." },
  { icon: "⏳", title: "Since 2019", desc: "Over half a decade of hands-on SEO experience specializing in the Bangladesh market including Rangpur." },
  { icon: "🚀", title: "210+ Projects", desc: "Successfully delivered 210+ SEO projects for businesses across Bangladesh including Rangpur.", hasLink: true },
];

export default function RangpurClient() {

  return (
    <div className="min-h-screen bg-white text-gray-900">
      <meta name="robots" content="index, follow" />
      {BreadcrumbSchema([
        { name: "Home", url: "https://kanokmiah.com.bd" },
        { name: "Locations", url: "https://kanokmiah.com.bd/locations" },
        { name: "Rangpur", url: "https://kanokmiah.com.bd/locations/rangpur" },
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
            Rangpur SEO Services
          </div>
          <h1 className="text-4xl md:text-6xl lg:text-7xl font-extrabold tracking-tight leading-[1.05] mb-6">
            <span className="block text-primary">Local SEO Expert in Rangpur</span>
            <span className="block">Dominate Google Maps</span>
          </h1>
          <p className="text-lg md:text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
            Your trusted local SEO partner in Rangpur. I help tobacco and potato growers, agricultural businesses, and local service providers dominate Google search and attract more customers online.
          </p>
          <div className="mt-8 flex flex-wrap justify-center gap-4">
            <Link href="/contact" className="bg-primary text-white font-bold px-8 py-3.5 rounded-full hover:bg-primary-dark hover:shadow-lg hover:shadow-primary/25 transition-all">
              Get Free Rangpur SEO Audit
            </Link>
            <Link href="/portfolio" className="border-2 border-primary text-primary font-bold px-8 py-3.5 rounded-full hover:bg-primary hover:text-white transition-all">
              View My Work
            </Link>
          </div>
        </div>
      </section>

      {/* === SEO FOR RANGPUR BUSINESSES === */}
      <section className="relative py-16 px-4 bg-gray-50/50">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <span className="text-primary text-sm font-semibold tracking-widest uppercase">Industry Focus</span>
            <h2 className="text-3xl md:text-5xl font-extrabold mt-3 mb-4">
              SEO for Rangpur&apos;s <span className="text-primary">Industries</span>
            </h2>
            <p className="text-gray-600 max-w-2xl mx-auto">
              Tailored SEO strategies for Rangpur&apos;s distinctive agricultural economy — from tobacco and potato to education and retail.
            </p>
          </div>
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
            {rangpurBusinesses.map((biz, i) => (
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
              Why Choose Me for <span className="text-primary">Rangpur SEO</span>
            </h2>
            <p className="text-gray-600 max-w-2xl mx-auto">
              What sets my Rangpur SEO services apart from the competition.
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

      {/* === ABOUT RANGPUR === */}
      <section className="relative py-16 px-4 bg-white">
        <div className="max-w-4xl mx-auto">
          <span className="text-primary text-sm font-semibold tracking-widest uppercase block text-center">About Rangpur</span>
          <h2 className="text-3xl md:text-5xl font-extrabold mt-3 mb-6 text-center">
            Why Rangpur <span className="text-primary">Needs SEO</span>
          </h2>
          <div className="space-y-4 text-gray-600 leading-relaxed">
            <p>Rangpur, the divisional headquarters of northern Bangladesh, is a city of agricultural abundance and growing industrial significance. Known as the breadbasket of Bangladesh, the Rangpur region produces the majority of the country's tobacco, potatoes, and a significant portion of its rice and wheat. Key landmarks include the historic Carmichael College (established 1916), the magnificent Tajhat Palace and Zamindar Bari, the lush Rangpur Zoo, and the scenic Chiklee Lake that serves as the city's recreational heart.</p>
            <p>The city's economy is predominantly agricultural, with tobacco cultivation being the most prominent cash crop — Rangpur is the center of Bangladesh's tobacco industry, supplying major companies like British American Tobacco Bangladesh. Potato farming is another economic pillar, with Rangpur potatoes shipped to markets across the country. The region also produces significant quantities of wheat, maize, and vegetables. In addition to agriculture, Rangpur has a growing education sector with institutions like Rangpur Medical College, Begum Rokeya University, and the Bangladesh Army University of Engineering & Technology, creating a vibrant student community.</p>
            <p>For Rangpur businesses — from tobacco and potato suppliers to local retailers, coaching centers, and hotels — SEO is essential for capturing online visibility in an increasingly digital marketplace. My Rangpur SEO strategies focus on helping agricultural businesses reach B2B buyers, educational institutions attract student admissions, and local service providers dominate Google Maps rankings. With bilingual Bengali-English optimization tailored to Rangpur's unique agricultural economy, I help businesses across northern Bangladesh grow their online presence and attract more customers from both local and national markets.</p>
          </div>
        </div>
      </section>

      {/* === LOCAL SUCCESS STORIES === */}
      <section className="relative py-16 px-4 bg-gray-50/50">
        <div className="max-w-4xl mx-auto">
          <span className="text-primary text-sm font-semibold tracking-widest uppercase block text-center">Local Success</span>
          <h2 className="text-3xl md:text-5xl font-extrabold mt-3 mb-6 text-center">
            Rangpur <span className="text-primary">Case Studies</span>
          </h2>
          <div className="space-y-6">
            <div className="bg-white border border-gray-100 rounded-2xl p-6 md:p-8 hover:shadow-md transition-all">
              <div className="flex items-start gap-4">
                <div className="text-4xl shrink-0">🥔</div>
                <div>
                  <h3 className="font-bold text-xl text-gray-900 mb-2">Rangpur Potato Farmer B2B Growth</h3>
                  <p className="text-gray-600 text-sm leading-relaxed">A Rangpur-based potato wholesale business wanted to expand beyond local markets and supply major potato buyers in Dhaka, Chittagong, and export markets. We implemented a B2B SEO strategy targeting keywords like "best potato supplier Bangladesh," "Rangpur potato wholesale," and "Bangladesh potato export quality." By creating landing pages showcasing their storage facilities, transportation capabilities, and quality certifications, and building citations on agricultural trade directories, the business achieved a 230% increase in organic inquiries from Dhaka-based wholesale buyers within 5 months.</p>
                </div>
              </div>
            </div>
            <div className="bg-white border border-gray-100 rounded-2xl p-6 md:p-8 hover:shadow-md transition-all">
              <div className="flex items-start gap-4">
                <div className="text-4xl shrink-0">🎓</div>
                <div>
                  <h3 className="font-bold text-xl text-gray-900 mb-2">Rangpur Coaching Center Admissions</h3>
                  <p className="text-gray-600 text-sm leading-relaxed">A coaching center in Rangpur city preparing students for medical and engineering admission tests wanted to increase student enrollment. After optimizing their Google Business Profile, creating content about successful alumni and admission strategies, and targeting keywords like "medical coaching Rangpur" and "engineering admission preparation in Rangpur," the center's website traffic increased by 160% in 3 months. They received over 45 admission inquiries through their optimized contact forms, a 200% increase from their previous organic lead generation.</p>
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
            { question: "How is SEO different for Rangpur businesses?", answer: "Rangpur's economy is uniquely driven by tobacco, potato, and agricultural industries. My Rangpur SEO strategies focus on bilingual Bengali + English optimization, Google Maps ranking for local service providers, and targeted keyword strategies for agricultural and manufacturing businesses." },
            { question: "Do you serve Rangpur city and surrounding areas?", answer: "Yes, I provide SEO services for Rangpur city and all surrounding areas including Rangpur Sadar, Pirganj, Kaunia, and all upazillas across the Rangpur division. My hyperlocal approach helps businesses across the region attract more customers." },
            { question: "What types of Rangpur businesses benefit most from SEO?", answer: "Tobacco and potato traders, agricultural businesses, local retailers, educational institutions, hotels, restaurants, and real estate developers all benefit from SEO. I help Rangpur businesses build a strong online presence and compete beyond local boundaries." },
            { question: "How do I get started with SEO in Rangpur?", answer: "Getting started is simple. Contact me through this page for a free SEO audit. I will analyze your current online presence, evaluate your competition in the Rangpur market, and create a customized SEO strategy tailored to your business goals and target audience." },
            { question: "How can Rangpur agricultural businesses benefit from B2B SEO?", answer: "Rangpur's agricultural sector — particularly tobacco, potato, and crop trading — can benefit greatly from B2B SEO. I create targeted strategies that help agricultural businesses rank for keywords used by wholesale buyers, food processing companies, and export agents. This includes optimizing for terms like 'potato supplier Bangladesh,' 'tobacco leaf exporter,' and 'Rangpur crop wholesale,' helping local farmers and traders connect with buyers across Bangladesh and internationally." },
          ]} />
          <h2 className="text-2xl md:text-3xl font-extrabold text-center mb-8">
            Frequently Asked <span className="text-primary">Questions</span>
          </h2>
          <div className="space-y-0 divide-y divide-gray-100">
            {[
              { question: "How is SEO different for Rangpur businesses?", answer: "Rangpur's economy is uniquely driven by tobacco, potato, and agricultural industries. My Rangpur SEO strategies focus on bilingual Bengali + English optimization, Google Maps ranking for local service providers, and targeted keyword strategies for agricultural and manufacturing businesses." },
              { question: "Do you serve Rangpur city and surrounding areas?", answer: "Yes, I provide SEO services for Rangpur city and all surrounding areas including Rangpur Sadar, Pirganj, Kaunia, and all upazillas across the Rangpur division. My hyperlocal approach helps businesses across the region attract more customers." },
              { question: "What types of Rangpur businesses benefit most from SEO?", answer: "Tobacco and potato traders, agricultural businesses, local retailers, educational institutions, hotels, restaurants, and real estate developers all benefit from SEO. I help Rangpur businesses build a strong online presence and compete beyond local boundaries." },
              { question: "How do I get started with SEO in Rangpur?", answer: "Getting started is simple. Contact me through this page for a free SEO audit. I will analyze your current online presence, evaluate your competition in the Rangpur market, and create a customized SEO strategy tailored to your business goals and target audience." },
              { question: "How can Rangpur agricultural businesses benefit from B2B SEO?", answer: "Rangpur's agricultural sector — particularly tobacco, potato, and crop trading — can benefit greatly from B2B SEO. I create targeted strategies that help agricultural businesses rank for keywords used by wholesale buyers, food processing companies, and export agents. This includes optimizing for terms like 'potato supplier Bangladesh,' 'tobacco leaf exporter,' and 'Rangpur crop wholesale,' helping local farmers and traders connect with buyers across Bangladesh and internationally." },
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
            Get Free <span className="text-amber-300">Rangpur SEO Audit</span>
          </h2>
          <p className="text-white/80 mb-10 text-lg">
            Ready to dominate Google Maps in Rangpur? Let me analyze your current SEO and create a customized plan to help your business get found by more customers.
          </p>
          <Link href="/contact" className="group inline-flex items-center gap-2 bg-white text-primary-dark px-10 py-4 rounded-xl font-bold text-lg transition-all hover:shadow-xl hover:-translate-y-0.5">
            Claim Your Free Audit
            <span className="group-hover:translate-x-1 transition-transform">→</span>
          </Link>
        </div>
      </section>

      {/* === FOOTER === */}
      <footer className="py-8 border-t border-gray-100 text-center text-sm text-gray-500">
        <p>© 2026 <span className="text-primary font-bold">Kanok Miah</span> — SEO Expert in Bangladesh. All rights reserved.</p>
        <div className="mt-3 flex items-center justify-center gap-4 text-xs">
          <Link href="/about" className="hover:text-primary transition-colors">About</Link>
          <Link href="/privacy-policy" className="hover:text-primary transition-colors">Privacy Policy</Link>
          <Link href="/terms-of-service" className="hover:text-primary transition-colors">Terms of Service</Link>
        </div>
      </footer>
    </div>
  );
}
