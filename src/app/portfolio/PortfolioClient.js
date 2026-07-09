"use client";

import Navbar from "@/components/Navbar";
import Link from "next/link";
import { BreadcrumbSchema, FAQSchema } from "@/components/Schema";

const stats = [
  { number: "350+", label: "Projects Completed" },
  { number: "50+", label: "Happy Clients" },
  { number: "6+", label: "Years Experience" },
  { number: "4.9/5", label: "Client Rating" },
];

const portfolioItems = [
  {
    icon: "🍽️",
    industry: "Restaurant & Food",
    metric: "Local Map Rankings",
    before: "Not in top 20",
    after: "#1 for 'best biriyani Dhaka'",
    result: "Top 1",
    percentage: "+320%",
    desc: "Google Map views increased 320% after GBP optimization and local citation building.",
  },
  {
    icon: "🛒",
    industry: "E-commerce (Daraz)",
    metric: "Organic Traffic",
    before: "50 visitors/day",
    after: "1,200+ visitors/day",
    result: "1,200+/day",
    percentage: "+180%",
    desc: "Product page optimization and content marketing drove massive organic growth.",
  },
  {
    icon: "🏢",
    industry: "Real Estate",
    metric: "Keyword Position",
    before: "Page 5+",
    after: "#1 for 'apartment in Dhaka'",
    result: "#1 Position",
    percentage: "Top Rank",
    desc: "Technical SEO + content strategy secured first-page rankings for 30+ high-value keywords.",
  },
  {
    icon: "👕",
    industry: "Garments Export",
    metric: "B2B Lead Generation",
    before: "5 leads/month",
    after: "40+ leads/month",
    result: "40+/month",
    percentage: "+25%",
    desc: "International SEO strategy delivered 25% more qualified B2B leads from global buyers.",
  },
  {
    icon: "🏥",
    industry: "Healthcare",
    metric: "Website Traffic",
    before: "200 visitors/week",
    after: "3,500+ visitors/week",
    result: "3,500+/week",
    percentage: "+400%",
    desc: "Local SEO + content marketing for a Dhaka hospital quadrupled weekly site traffic.",
  },
  {
    icon: "🎓",
    industry: "Education",
    metric: "Enquiry Conversions",
    before: "10 enquiries/month",
    after: "85+ enquiries/month",
    result: "85+/month",
    percentage: "+280%",
    desc: "Ranked for 'best coaching center in Dhaka' and 20+ education-related keywords.",
  },
];

export default function PortfolioClient() {
  const breadcrumbItems = [
    { name: "Home", url: "https://kanokmiah.com.bd" },
    { name: "Portfolio", url: "https://kanokmiah.com.bd/portfolio" },
  ];


  return (
    <div className="min-h-screen bg-white text-gray-900">
      {BreadcrumbSchema(breadcrumbItems)}
      {/* === NAVBAR === */}
      <Navbar />

      {/* === HERO === */}
      <section className="relative pt-32 pb-16 px-4 overflow-hidden">
        <div className="absolute top-1/3 -left-32 w-96 h-96 bg-primary/20 rounded-full blur-3xl animate-pulse" />
        <div className="absolute bottom-1/4 -right-32 w-80 h-80 bg-primary/20 rounded-full blur-3xl animate-pulse delay-1000" />
        <div className="relative max-w-4xl mx-auto text-center">
          <div className="inline-flex items-center gap-2 bg-primary-light border border-primary/20 text-primary text-xs font-semibold px-5 py-2 rounded-full mb-8 backdrop-blur-sm">
            <span className="w-2 h-2 bg-primary rounded-full animate-pulse" />
            My Work
          </div>
          <h1 className="text-4xl md:text-6xl lg:text-7xl font-extrabold tracking-tight leading-[1.05] mb-6">
            My SEO <span className="text-primary">Portfolio</span>
          </h1>
          <p className="text-lg md:text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
            A track record of measurable SEO success for Bangladeshi businesses. Every number below 
            represents a real campaign with real results — not vanity metrics.
          </p>
        </div>
      </section>

      {/* === STATS BAND === */}
      <section className="relative py-16 border-y border-gray-100">
        <div className="absolute inset-0 bg-gradient-to-r from-primary/5 via-transparent to-primary/5" />
        <div className="relative max-w-5xl mx-auto px-4 grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
          {stats.map((stat, i) => (
            <div key={i}>
              <div className="text-4xl md:text-5xl font-extrabold bg-gradient-to-b from-primary to-primary-dark bg-clip-text text-transparent">
                {stat.number}
              </div>
              <div className="text-gray-500 text-sm mt-1">{stat.label}</div>
            </div>
          ))}
        </div>
      </section>

      {/* === PORTFOLIO GRID === */}
      <section className="relative py-16 px-4">
        <div className="absolute top-0 right-0 w-72 h-72 bg-primary/10 rounded-full blur-3xl" />
        <div className="relative max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <span className="text-primary text-sm font-semibold tracking-widest uppercase">Case Results</span>
            <h2 className="text-3xl md:text-5xl font-extrabold mt-3 mb-4">
              Before & After <span className="text-primary">Results</span>
            </h2>
            <p className="text-gray-500 max-w-xl mx-auto">
              Real data from real campaigns across diverse industries in Bangladesh.
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-5">
            {portfolioItems.map((item, i) => (
              <div
                key={i}
                className="group bg-gray-50/70 border border-gray-100 rounded-2xl p-6 hover:shadow-lg hover:-translate-y-1 transition-all duration-300"
              >
                {/* Icon + Industry */}
                <div className="flex items-center gap-3 mb-4">
                  <span className="text-3xl">{item.icon}</span>
                  <span className="text-xs font-bold uppercase tracking-wider text-gray-500">{item.industry}</span>
                </div>

                {/* Metric Label */}
                <h3 className="text-base font-bold text-gray-900 mb-3">{item.metric}</h3>

                {/* Before / After Display */}
                <div className="space-y-2 mb-4">
                  <div className="flex items-center justify-between bg-red-50 border border-red-100 rounded-lg px-3 py-2">
                    <span className="text-xs font-semibold text-red-600 uppercase">Before</span>
                    <span className="text-sm font-medium text-red-700">{item.before}</span>
                  </div>
                  <div className="flex items-center justify-between bg-green-50 border border-green-100 rounded-lg px-3 py-2">
                    <span className="text-xs font-semibold text-green-600 uppercase">After</span>
                    <span className="text-sm font-medium text-green-700">{item.after}</span>
                  </div>
                </div>

                {/* Result Badge */}
                <div className="flex items-center justify-between">
                  <span className="text-lg font-extrabold text-primary">{item.result}</span>
                  <span className="inline-block bg-primary-light text-primary text-xs font-bold px-3 py-1 rounded-full">
                    {item.percentage}
                  </span>
                </div>

                <p className="text-xs text-gray-500 mt-3 leading-relaxed">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* === FAQ === */}
      <section className="py-16 px-4 bg-white">
        <div className="max-w-4xl mx-auto">
          <FAQSchema faqs={[
            { question: "How many projects have you completed?", answer: "I have successfully delivered 350+ SEO projects for businesses across Bangladesh, spanning industries such as restaurants, e-commerce, real estate, garments & textiles, healthcare, education, and more. Each project is backed by measurable results and documented ROI." },
            { question: "What industries do you have experience in?", answer: "I have hands-on SEO experience across a diverse range of industries including food & restaurant, e-commerce (Daraz & Shopify), real estate, garments & textile export, healthcare, education, hospitality, and local services. My approach is tailored to each industry's unique competitive landscape and customer search behaviour." },
            { question: "How do I view more project details?", answer: "You can explore detailed case studies on my Case Studies page where I break down each project's challenge, the specific strategy applied, and the measurable results achieved. For a more in-depth discussion about how I can help your specific business, feel free to contact me directly for a free consultation." },
          ]} />
          <h2 className="text-2xl md:text-3xl font-extrabold text-center mb-8">
            Frequently Asked <span className="text-primary">Questions</span>
          </h2>
          <div className="space-y-0 divide-y divide-gray-100">
            {[
              { question: "How many projects have you completed?", answer: "I have successfully delivered 350+ SEO projects for businesses across Bangladesh, spanning industries such as restaurants, e-commerce, real estate, garments & textiles, healthcare, education, and more. Each project is backed by measurable results and documented ROI." },
              { question: "What industries do you have experience in?", answer: "I have hands-on SEO experience across a diverse range of industries including food & restaurant, e-commerce (Daraz & Shopify), real estate, garments & textile export, healthcare, education, hospitality, and local services. My approach is tailored to each industry's unique competitive landscape and customer search behaviour." },
              { question: "How do I view more project details?", answer: "You can explore detailed case studies on my Case Studies page where I break down each project's challenge, the specific strategy applied, and the measurable results achieved. For a more in-depth discussion about how I can help your specific business, feel free to contact me directly for a free consultation." },
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
            Let&apos;s Add Your <span className="text-amber-300">Success Story</span>
          </h2>
          <p className="text-primary/80 mb-10 text-lg">
            Your business could be the next case study. Start with a free SEO audit and discover your growth potential.
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
