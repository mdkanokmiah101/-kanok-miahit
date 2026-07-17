"use client";

import { useEffect, useRef } from "react";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import Link from "next/link";
import { BreadcrumbSchema, FAQSchema } from "@/components/Schema";

const neighborhoods = [
  { icon: "🏘️", name: "Mirpur", desc: "Mirpur is one of Dhaka's largest and most competitive local markets. I help businesses here dominate neighborhood search results by targeting local keywords and optimizing Google Business Profiles for maximum visibility. Whether you run a shop, restaurant, or service business in Mirpur, my SEO strategies drive real foot traffic and local leads." },
  { icon: "🏢", name: "Gulshan", desc: "Gulshan is Dhaka's premier corporate and diplomatic enclave, home to high-end restaurants, boutiques, and multinational offices. My hyperlocal SEO approach helps Gulshan businesses capture premium local search traffic, attract affluent customers, and outrank competitors in this upscale neighborhood." },
  { icon: "🏙️", name: "Banani", desc: "Banani's busy commercial zone is packed with businesses competing for the same customers. I use precision local SEO tactics — including neighborhood-specific keyword targeting and citation building — to help Banani businesses rise above the noise and get found by ready-to-buy local customers." },
  { icon: "🌆", name: "Uttara", desc: "Uttara is a rapidly growing suburb with a dense residential and commercial mix. My Google Maps optimization and local pack ranking strategies help Uttara businesses attract both walk-in customers and online leads from this expanding market. I focus on mobile-first SEO because most Uttara residents search on their phones." },
  { icon: "🏛️", name: "Dhanmondi", desc: "Dhanmondi is a bustling hub of restaurants, clinics, educational institutions, and retail shops. My local SEO services help Dhanmondi businesses rank higher in Google Maps and organic search, bringing in more customers from this high-traffic neighborhood. I understand the unique competitive dynamics of this area." },
  { icon: "🏗️", name: "Motijheel", desc: "Motijheel is Dhaka's primary financial district, where B2B service providers and financial institutions compete for visibility. My B2B local SEO strategies help Motijheel businesses rank for professional services keywords and generate qualified leads from decision-makers in this commercial hub." },
  { icon: "🏡", name: "Bashundhara R/A", desc: "Bashundhara Residential Area is one of Dhaka's most desirable neighborhoods with a growing mix of businesses and residents. I help Bashundhara R/A businesses establish strong local online presence through targeted Google Maps SEO and neighborhood-specific content strategies." },
  { icon: "🏪", name: "Mohammadpur", desc: "Mohammadpur is a densely populated residential and commercial area with fierce local competition. My SEO services help Mohammadpur businesses get discovered by local customers searching for products and services nearby. I optimize for 'near me' searches and local pack rankings to drive results." },
  { icon: "🏰", name: "Old Dhaka", desc: "Old Dhaka is the historic heart of the capital, rich with traditional markets, restaurants, and heritage businesses. I help Old Dhaka businesses preserve their loyal customer base while attracting new visitors through modern SEO techniques tailored to this unique, culturally rich neighborhood." },
];

const trustPoints = [
  { icon: "📍", title: "Google Maps Ranking", desc: "Proven strategies to get your business to the top of Google Maps in Dhaka." },
  { icon: "📋", title: "GBP Optimization", desc: "Expert Google Business Profile optimization for maximum local visibility." },
  { icon: "⏳", title: "Since 2019", desc: "Over half a decade of hands-on SEO experience in the Bangladesh market." },
  { icon: "🚀", title: "210+ Projects", desc: "Successfully delivered 210+ SEO projects for businesses across Bangladesh.", hasLink: true },
];

export default function DhakaClient() {

  // Scroll-triggered animation for process cards
  useEffect(() => {
    const cards = document.querySelectorAll(".process-card");
    if (!cards.length) return;
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("in-view");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.15, rootMargin: "0px 0px -50px 0px" }
    );
    cards.forEach((el) => observer.observe(el));
    return () => observer.disconnect();
  }, []);

  return (
    <div className="min-h-screen bg-white text-gray-900">
      <meta name="robots" content="index, follow" />
      {BreadcrumbSchema([
        { name: "Home", url: "https://kanokmiah.com.bd" },
        { name: "Locations", url: "https://kanokmiah.com.bd/locations" },
        { name: "Dhaka", url: "https://kanokmiah.com.bd/locations/dhaka" },
      ])}

      {/* === NAVBAR === */}
      <Navbar />

      {/* === HERO === */}
      <section className="relative pt-24 md:pt-32 pb-16 px-4 overflow-hidden">
        <div className="absolute top-1/3 -left-32 w-96 h-96 bg-primary/20 rounded-full blur-3xl animate-pulse hidden md:block" />
        <div className="absolute bottom-1/4 -right-32 w-80 h-80 bg-primary/20 rounded-full blur-3xl animate-pulse delay-1000 hidden md:block" />
        <div className="relative max-w-4xl mx-auto text-center">
          <div className="inline-flex items-center gap-2 bg-primary-light border border-primary/20 text-primary text-xs font-semibold px-5 py-2 rounded-full mb-8 backdrop-blur-sm">
            <span className="w-2 h-2 bg-primary rounded-full animate-pulse" />
            Dhaka SEO Services 2026
          </div>
          <h1 className="text-4xl md:text-6xl lg:text-7xl font-extrabold tracking-tight leading-[1.05] mb-6">
            <span className="text-primary">
              Best SEO Services in Dhaka
            </span>
            <br />Rank Higher in Your Neighborhood
          </h1>
          <p className="text-lg md:text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
            Your trusted local SEO expert in Dhaka. I help businesses across the capital city dominate Google search results, attract more local customers, and grow revenue with proven, data-driven SEO strategies. Looking for the <strong>best SEO services in Dhaka</strong>? You&apos;ve found the right expert.
          </p>
          <div className="mt-8 flex flex-wrap justify-center gap-4">
            <Link href="/contact" className="bg-primary text-white font-bold px-8 py-3.5 rounded-full hover:bg-primary-dark hover:shadow-lg hover:shadow-primary/25 transition-all">
              Get Free Dhaka SEO Audit
            </Link>
            <Link href="/portfolio" className="border-2 border-primary text-primary font-bold px-8 py-3.5 rounded-full hover:bg-primary hover:text-white transition-all">
              View My Work
            </Link>
          </div>
          <div className="mt-12 flex justify-center">
            <img 
              src="/kanok-miah-profile.webp" 
              alt="Kanok Miah — Best SEO Expert in Dhaka, Bangladesh" 
              width="120" 
              height="120" 
              className="rounded-full border-4 border-white shadow-xl"
              loading="lazy"
            />
          </div>
        </div>
      </section>

      {/* === DIRECT ANSWER BOX === */}
      <section className="relative py-12 px-4">
        <div className="max-w-4xl mx-auto">
          <div className="bg-gradient-to-br from-primary/5 to-primary/10 border border-primary/20 rounded-3xl p-6 md:p-10 text-center shadow-lg">
            <div className="text-5xl mb-4">🎯</div>
            <h2 className="text-2xl md:text-3xl font-extrabold text-gray-900 mb-4">
              The <span className="text-primary">Best SEO Services in Dhaka 2026</span> — Direct & Transparent
            </h2>
            <p className="text-gray-700 text-lg md:text-xl leading-relaxed max-w-3xl mx-auto">
              If you&apos;re looking for the best SEO services in Dhaka, you&apos;ve come to the right place. I specialize in helping Dhaka businesses rank higher on Google Maps, attract local customers through organic search, and grow revenue with data-driven SEO strategies tailored to Bangladesh&apos;s unique digital landscape.
            </p>
          </div>
        </div>
      </section>

      {/* === MY DHAKA SEO PROCESS — Apple/Stripe/Linear Level Premium Redesign === */}
      <section className="relative py-32 md:py-36 px-4 overflow-hidden">
        {/* Background — layered premium gradient with subtle geometric pattern */}
        <div className="absolute inset-0 bg-gradient-to-b from-gray-50/40 via-white to-gray-50/30" />
        <div className="absolute inset-0 opacity-[0.03]" style={{ backgroundImage: `radial-gradient(circle at 1px 1px, #124D1C 1px, transparent 0)`, backgroundSize: '32px 32px' }} aria-hidden="true" />
        <div className="absolute top-1/3 -left-40 w-[600px] h-[600px] bg-primary/[0.06] rounded-full blur-[140px] hidden md:block" />
        <div className="absolute bottom-1/3 -right-40 w-[550px] h-[550px] bg-primary/[0.04] rounded-full blur-[130px] hidden md:block" />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[700px] h-[700px] bg-amber-400/[0.02] rounded-full blur-[160px] hidden md:block" />
        {/* Subtle top border line */}
        <div className="absolute top-0 left-[10%] right-[10%] h-px bg-gradient-to-r from-transparent via-primary/10 to-transparent" />

        <div className="relative max-w-7xl mx-auto">
          {/* Section Label — premium pill badge */}
          <div className="text-center mb-16 md:mb-20">
            <span className="inline-flex items-center gap-2 text-[10px] md:text-[11px] font-bold tracking-[0.3em] uppercase px-6 py-2.5 rounded-full bg-primary/[0.05] border border-primary/[0.08] text-primary/80 backdrop-blur-sm">
              <span className="w-1.5 h-1.5 rounded-full bg-primary animate-pulse" />
              How I Work
            </span>
            <h2 className="text-[clamp(2rem,4.5vw,3.75rem)] font-extrabold mt-8 mb-6 text-gray-900 leading-[1.08] tracking-[-0.03em]">
              How Does My{' '}
              <span className="text-primary relative inline-block">
                Dhaka SEO Process
                <span className="absolute -bottom-1 left-0 right-0 h-[3px] bg-primary/20 rounded-full hidden md:block" />
              </span>{' '}
              Work?
            </h2>
            <p className="text-gray-400 text-base md:text-lg max-w-[600px] mx-auto leading-relaxed font-[450]">
              A proven, data-driven 5-step process that delivers real results for Dhaka businesses. No shortcuts, no guesswork — just consistent execution.
            </p>
          </div>

          {/* Connector + Cards Container */}
          <div className="relative">
            {/* Premium connector — solid green line with animated glowing dot */}
            <div className="hidden lg:block absolute top-[76px] left-[7%] right-[7%] z-0" aria-hidden="true">
              {/* Main line */}
              <div className="h-[2px] bg-gradient-to-r from-primary/10 via-primary/25 to-primary/10 rounded-full" />
              {/* Animated pulse dot */}
              <div className="absolute -top-[5px] left-0 w-3 h-3 animate-pulse">
                <div className="w-full h-full rounded-full bg-primary/30" />
                <div className="absolute inset-0 rounded-full bg-primary/10 animate-ping" />
              </div>
            </div>

            {/* Step indicators on the connector line */}
            <div className="hidden lg:flex absolute top-[70px] left-[7%] right-[7%] justify-between z-[1] pointer-events-none" aria-hidden="true">
              {[1,2,3,4,5].map((dot) => (
                <div key={dot} className="w-3 h-3 rounded-full bg-white border-2 border-primary/30 shadow-sm" />
              ))}
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-5 gap-5 lg:gap-6 items-stretch">
              {[
                {
                  step: "01",
                  title: "SEO Audit & Analysis",
                  desc: "Deep dive into your current rankings, competitor landscape, website health, and technical SEO issues to identify what's working and what needs fixing.",
                  icon: (
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
                      <circle cx="11" cy="11" r="8" />
                      <path d="M16.5 16.5L21 21" />
                      <path d="M11 8v6" />
                      <path d="M8 11h6" />
                    </svg>
                  ),
                },
                {
                  step: "02",
                  title: "Strategy & Keyword Research",
                  desc: "Identify high-value keyword opportunities specific to Dhaka — including Bengali-English bilingual queries, local intent keywords, and neighborhood-specific phrases.",
                  icon: (
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
                      <circle cx="12" cy="12" r="10" />
                      <circle cx="12" cy="12" r="4" />
                      <circle cx="12" cy="12" r="1" />
                      <path d="M12 2v4" />
                      <path d="M12 18v4" />
                      <path d="M2 12h4" />
                      <path d="M18 12h4" />
                    </svg>
                  ),
                },
                {
                  step: "03",
                  title: "On-Page & Technical Optimization",
                  desc: "Fix critical SEO issues, optimize page titles, meta descriptions, headers, content structure, and site speed — ensuring your website is fully search-engine friendly.",
                  icon: (
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
                      <rect x="4" y="4" width="16" height="16" rx="2" />
                      <path d="M4 9h16" />
                      <path d="M9 4v16" />
                      <circle cx="14" cy="14" r="2" />
                      <path d="M17 11l2 2-2 2" />
                    </svg>
                  ),
                },
                {
                  step: "04",
                  title: "Local SEO & Google Maps",
                  desc: "Optimize your Google Business Profile, build high-quality local citations, manage reviews, and implement hyperlocal strategies to dominate Google Maps results in Dhaka.",
                  icon: (
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
                      <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z" />
                      <circle cx="12" cy="10" r="3" />
                      <path d="M12 2v2" />
                      <path d="M12 16v2" />
                      <path d="M4.22 5.22l1.42 1.42" />
                      <path d="M18.36 6.64l1.42-1.42" />
                    </svg>
                  ),
                },
                {
                  step: "05",
                  title: "Monitoring & Reporting",
                  desc: "Track rankings, traffic, leads, and conversions with transparent reporting. I continuously refine your strategy based on real data to maximize ROI.",
                  icon: (
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
                      <rect x="3" y="3" width="18" height="18" rx="2" />
                      <path d="M7 16l3-4 3 4 4-6" />
                      <path d="M7 10h.01" />
                      <path d="M17 14h.01" />
                    </svg>
                  ),
                },
              ].map((s, i) => (
                <div
                  key={i}
                  className={`process-card group relative bg-white/95 backdrop-blur-sm border rounded-[24px] p-7 md:p-8 lg:p-9 flex flex-col transition-all duration-500 ease-out
                    ${i === 2
                      ? "border-primary/15 shadow-[0_0_0_1px_rgba(18,77,28,0.06),0_8px_30px_-6px_rgba(18,77,28,0.08)] hover:shadow-[0_0_0_1px_rgba(18,77,28,0.15),0_20px_60px_-12px_rgba(18,77,28,0.15)]"
                      : "border-gray-100/90 shadow-[0_0_0_1px_rgba(0,0,0,0.02),0_1px_3px_rgba(0,0,0,0.02)] hover:shadow-[0_0_0_1px_rgba(18,77,28,0.08),0_12px_40px_-8px_rgba(18,77,28,0.10)]"
                    }
                    hover:border-primary/20 hover:-translate-y-2`}
                  style={{
                    transitionDelay: `${i * 100}ms`,
                    background: `linear-gradient(135deg, rgba(255,255,255,1) 0%, rgba(249,250,251,0.5) 100%)`,
                  }}
                >
                  {/* Step Number Badge — Premium circular with inner gradient */}
                  <div className="relative mb-6 inline-flex">
                    <div className={`
                      relative z-10 w-[60px] h-[60px] rounded-full flex items-center justify-center font-bold text-lg
                      transition-all duration-500 ease-out group-hover:scale-110 group-hover:shadow-xl
                      ${i % 2 === 0
                        ? "bg-gradient-to-br from-primary via-[#0f6b20] to-[#0a3d13] text-white shadow-[0_4px_20px_-2px_rgba(18,77,28,0.3)] group-hover:shadow-[0_8px_30px_-4px_rgba(18,77,28,0.4)]"
                        : "bg-gradient-to-br from-amber-300 via-amber-400 to-amber-500 text-gray-900 shadow-[0_4px_20px_-2px_rgba(255,210,48,0.3)] group-hover:shadow-[0_8px_30px_-4px_rgba(255,210,48,0.4)]"
                      }
                    `}>
                      <span className="relative z-10">{s.step}</span>
                      {/* Inner shine */}
                      <div className="absolute inset-0 rounded-full bg-gradient-to-b from-white/15 to-transparent opacity-50" />
                    </div>
                    {/* Outer glow ring */}
                    <div className={`
                      absolute -inset-2 rounded-full opacity-0 group-hover:opacity-100 transition-all duration-500 blur-lg
                      ${i % 2 === 0 ? "bg-primary/15" : "bg-amber-400/15"}
                      group-hover:scale-110
                    `} />
                    {/* Subtle ring border */}
                    <div className={`
                      absolute -inset-[3px] rounded-full border opacity-0 group-hover:opacity-100 transition-all duration-500
                      ${i % 2 === 0 ? "border-primary/10" : "border-amber-400/10"}
                    `} />
                  </div>

                  {/* Icon — larger, with premium bg transition */}
                  <div className={`
                    w-[44px] h-[44px] rounded-2xl flex items-center justify-center mb-5
                    transition-all duration-300 ease-out
                    ${i % 2 === 0
                      ? "text-primary bg-primary/[0.06] group-hover:bg-primary group-hover:text-white group-hover:shadow-lg group-hover:shadow-primary/20"
                      : "text-amber-500 bg-amber-400/[0.08] group-hover:bg-amber-400 group-hover:text-white group-hover:shadow-lg group-hover:shadow-amber-400/20"
                    }
                  `}>
                    {s.icon}
                  </div>

                  {/* Content */}
                  <h3 className="font-bold text-[17px] lg:text-[18px] text-gray-900 mb-3 leading-snug tracking-[-0.01em]">
                    {s.title}
                  </h3>
                  <p className="text-gray-400 text-sm leading-relaxed flex-1 font-[450]">
                    {s.desc}
                  </p>

                  {/* Bottom accent line on hover */}
                  <div className={`
                    mt-6 h-[2px] rounded-full w-0 group-hover:w-full transition-all duration-500 ease-out
                    ${i % 2 === 0 ? "bg-gradient-to-r from-primary/30 to-primary/10" : "bg-gradient-to-r from-amber-400/30 to-amber-400/10"}
                  `} />
                </div>
              ))}
            </div>
          </div>

          {/* === Premium CTA === */}
          <div className="text-center mt-16 md:mt-20">
            <div className="relative inline-block max-w-lg mx-auto w-full">
              {/* Glow bg */}
              <div className="absolute inset-0 bg-gradient-to-b from-primary/[0.03] to-primary/[0.01] rounded-[24px] blur-xl" />
              <div className="relative bg-white/90 backdrop-blur-sm border border-primary/[0.06] rounded-[24px] p-8 md:p-10 shadow-[0_0_0_1px_rgba(18,77,28,0.03),0_4px_20px_-8px_rgba(18,77,28,0.06)] hover:shadow-[0_0_0_1px_rgba(18,77,28,0.06),0_8px_30px_-8px_rgba(18,77,28,0.10)] transition-all duration-300">
                <p className="text-gray-900 font-bold text-xl md:text-2xl mb-6 tracking-[-0.02em]">
                  Ready to Start Your SEO Growth?
                </p>
                <Link
                  href="/contact"
                  className="inline-flex items-center gap-2.5 bg-primary hover:bg-primary-dark text-white px-9 py-4 rounded-xl font-bold text-sm transition-all duration-300 hover:shadow-xl hover:shadow-primary/25 hover:-translate-y-0.5 focus:outline-none focus:ring-2 focus:ring-primary/40 focus:ring-offset-2 group/btn"
                  aria-label="Get your free SEO audit and start growing"
                >
                  <span>Get Free SEO Audit</span>
                  <span className="text-lg transition-transform duration-300 group-hover/btn:translate-x-1">→</span>
                </Link>
                <p className="text-gray-400 text-xs mt-4 font-medium">No commitment. Worth 5,000 BDT.</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Inline Scroll Animation — GPU accelerated, staggered, no layout shift */}
      <style jsx>{`
        .process-card {
          opacity: 0;
          transform: translateY(40px) scale(0.97);
          will-change: transform, opacity;
        }
        .process-card.in-view {
          animation: processCardIn 0.7s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }
        @keyframes processCardIn {
          0% { opacity: 0; transform: translateY(40px) scale(0.97); }
          100% { opacity: 1; transform: translateY(0) scale(1); }
        }
        .process-card.in-view .process-step-ring {
          animation: ringPulse 1.5s ease-out forwards;
        }
      `}</style>

      {/* === SEO INVESTMENT & PACKAGES === */}
      <section className="relative py-16 px-4">
        <div className="absolute top-0 right-0 w-72 h-72 bg-primary/10 rounded-full blur-3xl hidden md:block" />
        <div className="relative max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <span className="text-primary text-sm font-semibold tracking-widest uppercase">Investment</span>
            <h2 className="text-3xl md:text-5xl font-extrabold mt-3 mb-4">
              What Are My <span className="text-primary">SEO Packages</span> &amp; Pricing?
            </h2>
            <p className="text-gray-600 max-w-2xl mx-auto">
              Transparent pricing for Dhaka SEO services. Every package includes a free initial audit and strategy consultation.
            </p>
          </div>
          <div className="grid md:grid-cols-3 gap-6">
            {[
              {
                name: "Basic",
                price: "15,000 BDT",
                sub: "Perfect for small businesses starting with local SEO",
                features: [
                  "Google Business Profile optimization",
                  "Local keyword research (1-2 areas)",
                  "Basic on-page SEO fixes",
                  "Monthly ranking reports",
                  "Email support",
                ],
                popular: false,
              },
              {
                name: "Standard",
                price: "25,000 BDT",
                sub: "Ideal for businesses ready to scale their online presence",
                features: [
                  "Everything in Basic, plus:",
                  "Full local SEO + Google Maps dominance",
                  "On-page & technical SEO audit",
                  "Content optimization (up to 5 pages)",
                  "Local citation building",
                  "Monthly strategy calls",
                ],
                popular: true,
              },
              {
                name: "Premium",
                price: "40,000 BDT",
                sub: "For multi-location businesses & aggressive growth targets",
                features: [
                  "Everything in Standard, plus:",
                  "Multi-location SEO strategy",
                  "GEO (Generative Engine Optimization)",
                  "Advanced technical SEO",
                  "Link building & digital PR",
                  "Dedicated account manager",
                  "Weekly reporting & reviews",
                ],
                popular: false,
              },
            ].map((pkg, i) => (
              <div key={i} className={`relative bg-white border ${pkg.popular ? "border-primary shadow-xl shadow-primary/10 ring-2 ring-primary" : "border-gray-100"} rounded-2xl p-6 md:p-8 hover:shadow-lg transition-all`}>
                {pkg.popular && (
                  <div className="absolute -top-3 left-1/2 -translate-x-1/2 bg-primary text-white text-xs font-bold px-4 py-1 rounded-full">
                    Most Popular
                  </div>
                )}
                <h3 className="text-2xl font-extrabold text-gray-900 mb-1">{pkg.name}</h3>
                <p className="text-3xl font-black text-primary mb-2">{pkg.price}</p>
                <p className="text-gray-500 text-sm mb-6">{pkg.sub}</p>
                <ul className="space-y-3 mb-8">
                  {pkg.features.map((f, j) => (
                    <li key={j} className="flex items-start gap-2 text-sm text-gray-700">
                      <span className="text-primary mt-0.5 flex-shrink-0">✓</span>
                      {f}
                    </li>
                  ))}
                </ul>
                <Link
                  href="/contact"
                  className={`block text-center font-bold py-3 rounded-xl transition-all ${
                    pkg.popular
                      ? "bg-primary text-white hover:bg-primary-dark"
                      : "border-2 border-primary text-primary hover:bg-primary hover:text-white"
                  }`}
                >
                  Get Started
                </Link>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* === CLIENT SUCCESS STORIES === */}
      <section className="relative py-16 px-4 bg-gray-50/50">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <span className="text-primary text-sm font-semibold tracking-widest uppercase">Real Results</span>
            <h2 className="text-3xl md:text-5xl font-extrabold mt-3 mb-4">
              What Results Have Dhaka <span className="text-primary">Businesses</span> Achieved?
            </h2>
            <p className="text-gray-600 max-w-2xl mx-auto">
              Real Dhaka businesses that ranked higher, got more customers, and grew their revenue with my SEO services.
            </p>
          </div>
          <div className="grid md:grid-cols-3 gap-6">
            {[
              {
                emoji: "🍽️",
                title: "Restaurant in Gulshan",
                before: "Struggling to appear in Google Maps for 'best restaurants in Gulshan' despite excellent food and reviews.",
                after: "Ranked #1 in Google Maps 3-pack for 12+ high-value keywords within 4 months. Online orders increased by 185%.",
                result: "+185%",
                resultLabel: "Online Orders",
              },
              {
                emoji: "👕",
                title: "Garments Manufacturer in Mirpur",
                before: "Outranked by competitors for 'readymade garments Dhaka' and other B2B keywords. Website traffic was stagnant at under 200 monthly visits.",
                after: "Achieved top 3 organic rankings for 8 major industry keywords. Monthly traffic grew from 180 to 4,200+ visitors with 65% from Bangladesh.",
                result: "+2,233%",
                resultLabel: "Traffic Growth",
              },
              {
                emoji: "🏥",
                title: "Clinic in Dhanmondi",
                before: "New clinic with zero online presence competing against established hospitals with decade-old websites and hundreds of reviews.",
                after: "GBP ranked in top 3 for 'skin clinic Dhanmondi' and 'dermatologist in Dhaka' within 3 months. Appointment bookings grew by 310% through Google Maps alone.",
                result: "+310%",
                resultLabel: "Appointment Bookings",
              },
            ].map((story, i) => (
              <div key={i} className="bg-white border border-gray-100 rounded-2xl p-6 hover:shadow-lg hover:-translate-y-1 transition-all">
                <div className="text-4xl mb-4">{story.emoji}</div>
                <h3 className="font-bold text-xl mb-3 text-gray-900">{story.title}</h3>
                <div className="space-y-3 mb-5">
                  <div>
                    <span className="text-xs font-bold uppercase text-red-500 tracking-wider">Before</span>
                    <p className="text-gray-600 text-sm mt-1">{story.before}</p>
                  </div>
                  <div>
                    <span className="text-xs font-bold uppercase text-green-600 tracking-wider">After</span>
                    <p className="text-gray-600 text-sm mt-1">{story.after}</p>
                  </div>
                </div>
                <div className="bg-primary/5 rounded-xl p-4 text-center">
                  <div className="text-3xl font-black text-primary">{story.result}</div>
                  <div className="text-sm text-gray-500 font-medium">{story.resultLabel}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* === বাংলা সেকশন === */}
      <section className="relative py-16 px-4" lang="bn">
        <div className="absolute top-1/3 left-1/3 w-80 h-80 bg-primary/10 rounded-full blur-3xl hidden md:block" />
        <div className="relative max-w-4xl mx-auto">
          <div className="text-center mb-10">
            <span className="text-primary text-sm font-semibold tracking-widest uppercase">বাংলা</span>
            <h2 className="text-3xl md:text-5xl font-extrabold mt-3 mb-4 leading-relaxed">
              ঢাকায় সেরা এসইও <span className="text-primary">সার্ভিস</span>
            </h2>
          </div>

          <div className="bg-white border border-gray-100 rounded-3xl p-6 md:p-10 shadow-lg mb-8">
            <p className="text-gray-700 text-lg leading-relaxed mb-6 text-justify">
              ঢাকা বাংলাদেশের ব্যবসার প্রাণকেন্দ্র। গুলশান, বনানী, মিরপুর, উত্তরা, ধানমন্ডি সহ প্রতিটি এলাকায় অসংখ্য ব্যবসা প্রতিদিন তাদের অনলাইন উপস্থিতি বাড়ানোর জন্য প্রতিযোগিতা করছে। কিন্তু গুগলে ভালো র‌্যাংক করা সহজ নয় — এর জন্য দরকার সঠিক কৌশল, সঠিক পরিকল্পনা এবং স্থানীয় বাজার সম্পর্কে গভীর ধারণা। আমি ঢাকার প্রতিটি এলাকার জন্য আলাদাভাবে এসইও স্ট্র্যাটেজি তৈরি করি, যাতে আপনার ব্যবসা সঠিক গ্রাহকদের কাছে পৌঁছাতে পারে।
            </p>
            <p className="text-gray-700 text-lg leading-relaxed mb-6 text-justify">
              আমার ঢাকা এসইও সার্ভিসের মধ্যে রয়েছে গুগল ম্যাপস অপটিমাইজেশন, লোকাল কীবোর্ড রিসার্চ, অন-পেজ এসইও, টেকনিক্যাল এসইও, এবং বিস্তারিত রিপোর্টিং। আমি শুধু র‌্যাংকিং বাড়াই না — আমি আপনার ব্যবসায় আসল গ্রাহক এবং রাজস্ব আনতে কাজ করি। বাংলাদেশের ডিজিটাল বাজার সম্পর্কে আমার বাস্তব অভিজ্ঞতা এবং গভীর জ্ঞান আপনাকে প্রতিযোগীদের থেকে এগিয়ে রাখবে।
            </p>
            <p className="text-gray-700 text-lg leading-relaxed text-justify">
              আপনি যদি ঢাকায় একটি ছোট দোকান, রেস্টুরেন্ট, ক্লিনিক, বা বড় কোম্পানি চালান — আমার এসইও সার্ভিস আপনার জন্য উপযোগী। আমি প্রতিটি ব্যবসার চাহিদা বুঝে পার্সোনালাইজড স্ট্র্যাটেজি তৈরি করি। ফ্রি এসইও অডিটের জন্য আজই যোগাযোগ করুন এবং দেখুন কীভাবে আপনার ব্যবসা গুগলে শীর্ষ স্থান পেতে পারে।
            </p>
          </div>

          {/* Bengali FAQ */}
          <div className="max-w-3xl mx-auto">
            <h3 className="text-2xl font-extrabold text-center mb-8">
              সচরাচর <span className="text-primary">জিজ্ঞাসা</span>
            </h3>
            <div className="space-y-0 divide-y divide-gray-100">
              {[
                { question: "ঢাকায় এসইও ফলাফল দেখতে কত সময় লাগে?", answer: "সাধারণত ৩-৬ মাসের মধ্যে আপনি গুগল র‌্যাংকিং এবং ট্রাফিকে উল্লেখযোগ্য উন্নতি দেখতে পাবেন। তবে এটি আপনার ব্যবসার ধরণ, প্রতিযোগিতা এবং আপনার ওয়েবসাইটের বর্তমান অবস্থার উপর নির্ভর করে। আমি প্রথম মাসেই কিছু দ্রুত উন্নতি এনে দিতে পারি, কিন্তু স্থায়ী ফলাফলের জন্য ধৈর্যশীল এবং নিয়মিত প্রচেষ্টা প্রয়োজন।" },
                { question: "ঢাকায় এসইও সার্ভিসের খরচ কত?", answer: "আমার এসইও প্যাকেজগুলি আপনার ব্যবসার প্রয়োজন অনুযায়ী ডিজাইন করা হয়েছে। বেসিক প্যাকেজ ছোট ব্যবসার জন্য উপযোগী, স্ট্যান্ডার্ড প্যাকেজ মাঝারি ব্যবসার জন্য, এবং প্রিমিয়াম প্যাকেজ বড় প্রতিষ্ঠানের জন্য। সঠিক মূল্য জানতে একটি ফ্রি কনসালটেশন বুক করুন — আপনার প্রয়োজন বুঝে আমি সেরা সমাধান প্রস্তাব করব।" },
                { question: "আপনি কি প্রথম পেজে র‌্যাংকের গ্যারান্টি দেন?", answer: "গুগল কখনোই #1 র‌্যাংকের গ্যারান্টি দেয় না, এবং যে কেউ গ্যারান্টি দেয় তারা মিথ্যা বলছে। আমি যা গ্যারান্টি দিতে পারি তা হল — সঠিক এসইও কৌশল প্রয়োগ, স্বচ্ছ রিপোর্টিং, এবং আপনার ব্যবসার জন্য সর্বোচ্চ প্রচেষ্টা। আমার ট্র্যাক রেকর্ড এবং ক্লায়েন্ট সাফল্যের গল্পগুলি নিজেই কথা বলে।" },
              ].map((f, i) => (
                <details key={i} className="py-4 group">
                  <summary className="font-semibold text-gray-900 cursor-pointer list-none flex justify-between items-center text-base">
                    {f.question}
                    <span className="text-primary transition-transform group-open:rotate-180">▼</span>
                  </summary>
                  <p className="text-gray-600 mt-3 pl-2 leading-relaxed">{f.answer}</p>
                </details>
              ))}
            </div>
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
              Targeted SEO strategies for every key area in Dhaka — customized to your local market and competition. My <strong>best SEO services in Dhaka</strong> cover every neighborhood.
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
        <div className="absolute top-0 right-0 w-72 h-72 bg-primary/10 rounded-full blur-3xl hidden md:block" />
        <div className="relative max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <span className="text-primary text-sm font-semibold tracking-widest uppercase">Why Trust Me</span>
            <h2 className="text-3xl md:text-5xl font-extrabold mt-3 mb-4">
              Why Choose My <span className="text-primary">Best SEO Services in Dhaka</span>
            </h2>
            <p className="text-gray-600 max-w-2xl mx-auto">
              What sets my Dhaka SEO services apart from the competition. I deliver results that help your business grow. Looking for <Link href="/services" className="text-primary font-semibold hover:underline">all SEO services</Link>? Explore my complete range.
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

      {/* === WHAT DHAKA CLIENTS SAY === */}
      <section className="relative py-16 px-4 bg-gray-50/50">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <span className="text-primary text-sm font-semibold tracking-widest uppercase">Testimonials</span>
            <h2 className="text-3xl md:text-5xl font-extrabold mt-3 mb-4">
              What Dhaka Clients <span className="text-primary">Say</span>
            </h2>
            <p className="text-gray-600 max-w-2xl mx-auto">
              Hear from business owners across Dhaka who transformed their online presence with my SEO services.
            </p>
          </div>
          <div className="grid md:grid-cols-3 gap-6">
            {[
              {
                stars: 5,
                text: "Working with Kanok has been a game-changer for our restaurant in Banani. We went from page 3 to #1 on Google Maps in just 3 months. Our weekday lunch crowd has doubled and we're getting calls every day from new customers finding us online. Highly recommend his Dhaka SEO services!",
                name: "— Farid H.",
                business: "Restaurant Owner, Banani",
              },
              {
                stars: 5,
                text: "I was skeptical about SEO at first, but Kanok's data-driven approach convinced me. He took the time to understand our garment business in Mirpur and built a strategy that brought us qualified B2B leads from Google. Our export inquiries have increased significantly since we started working together.",
                name: "— Shamima K.",
                business: "Garments Exporter, Mirpur",
              },
              {
                stars: 5,
                text: "As a dental clinic in Dhanmondi, we needed local patients — not international traffic. Kanok's hyperlocal SEO strategy was perfect for us. Our Google Business Profile now ranks in the top 3 for multiple keywords and we've seen a steady stream of new patients booking appointments through Google. Truly the best SEO service in Dhaka!",
                name: "— Dr. Naveed R.",
                business: "Dental Clinic, Dhanmondi",
              },
            ].map((t, i) => (
              <div key={i} className="bg-white border border-gray-100 rounded-2xl p-6 hover:shadow-lg transition-all">
                <div className="flex items-center gap-1 mb-4">
                  {[...Array(5)].map((_, j) => (
                    <span key={j} className={`text-lg ${j < t.stars ? "text-[#FFD230]" : "text-gray-200"}`}>★</span>
                  ))}
                </div>
                <p className="text-gray-700 text-sm leading-relaxed mb-5 italic">&ldquo;{t.text}&rdquo;</p>
                <div className="border-t border-gray-100 pt-4">
                  <p className="font-bold text-gray-900 text-sm">{t.name}</p>
                  <p className="text-gray-500 text-xs">{t.business}</p>
                </div>
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
            { question: "How long does it take to see SEO results in Dhaka?", answer: "Most clients start seeing measurable improvements in rankings and traffic within 3-6 months of consistent SEO work. However, some quick wins — like fixing technical issues or optimizing your Google Business Profile — can show results within weeks. SEO is a long-term investment, and the best results compound over 6-12 months. I provide transparent monthly reports so you can track every improvement." },
            { question: "How much do SEO services cost in Dhaka?", answer: "My SEO packages are designed to fit different budgets and business needs. The Basic package starts at an affordable rate for small local businesses, while the Standard and Premium packages offer more comprehensive services for growing and enterprise businesses. Contact me for a free consultation and I'll recommend the best package for your specific goals and budget." },
            { question: "Can SEO help my small business in Bangladesh?", answer: "Absolutely! SEO is one of the most cost-effective ways for small businesses in Bangladesh to compete with larger companies. Unlike paid ads, SEO delivers long-term, sustainable traffic without ongoing ad spend. I've helped small shops, restaurants, clinics, and service providers in Dhaka outrank much bigger competitors through smart local SEO strategies." },
            { question: "Do you offer SEO services for e-commerce stores in Dhaka?", answer: "Yes, I offer specialized e-commerce SEO services for online stores in Dhaka. This includes product page optimization, category page structuring, technical SEO for e-commerce platforms, schema markup for products, and local e-commerce strategies to help Dhaka-based online stores attract more customers and increase sales." },
            { question: "What makes your SEO services different from agencies?", answer: "Unlike large agencies that treat you as just another client, I provide personalized, hands-on SEO services with direct access to me — the SEO expert working on your project. You get customized strategies based on deep knowledge of the Dhaka market, transparent reporting, and a dedicated partner who genuinely cares about your business growth. No account managers, no templates, no empty promises." },
            { question: "Do you guarantee #1 rankings on Google?", answer: "No ethical SEO professional can guarantee #1 rankings on Google — and anyone who does is misleading you. Google's algorithms are complex and constantly changing. What I can guarantee is my full commitment to implementing proven, white-hat SEO strategies that consistently deliver top-tier results for my clients. My track record speaks for itself: multiple clients ranking #1 for their target keywords in Dhaka's competitive market." },
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
              { question: "How long does it take to see SEO results in Dhaka?", answer: "Most clients start seeing measurable improvements in rankings and traffic within 3-6 months of consistent SEO work. However, some quick wins — like fixing technical issues or optimizing your Google Business Profile — can show results within weeks. SEO is a long-term investment, and the best results compound over 6-12 months. I provide transparent monthly reports so you can track every improvement." },
              { question: "How much do SEO services cost in Dhaka?", answer: "My SEO packages are designed to fit different budgets and business needs. The Basic package starts at an affordable rate for small local businesses, while the Standard and Premium packages offer more comprehensive services for growing and enterprise businesses. Contact me for a free consultation and I'll recommend the best package for your specific goals and budget." },
              { question: "Can SEO help my small business in Bangladesh?", answer: "Absolutely! SEO is one of the most cost-effective ways for small businesses in Bangladesh to compete with larger companies. Unlike paid ads, SEO delivers long-term, sustainable traffic without ongoing ad spend. I've helped small shops, restaurants, clinics, and service providers in Dhaka outrank much bigger competitors through smart local SEO strategies." },
              { question: "Do you offer SEO services for e-commerce stores in Dhaka?", answer: "Yes, I offer specialized e-commerce SEO services for online stores in Dhaka. This includes product page optimization, category page structuring, technical SEO for e-commerce platforms, schema markup for products, and local e-commerce strategies to help Dhaka-based online stores attract more customers and increase sales." },
              { question: "What makes your SEO services different from agencies?", answer: "Unlike large agencies that treat you as just another client, I provide personalized, hands-on SEO services with direct access to me — the SEO expert working on your project. You get customized strategies based on deep knowledge of the Dhaka market, transparent reporting, and a dedicated partner who genuinely cares about your business growth. No account managers, no templates, no empty promises." },
              { question: "Do you guarantee #1 rankings on Google?", answer: "No ethical SEO professional can guarantee #1 rankings on Google — and anyone who does is misleading you. Google's algorithms are complex and constantly changing. What I can guarantee is my full commitment to implementing proven, white-hat SEO strategies that consistently deliver top-tier results for my clients. My track record speaks for itself: multiple clients ranking #1 for their target keywords in Dhaka's competitive market." },
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
              Explore our comprehensive SEO services — including the <strong>best SEO services in Dhaka</strong> — designed to help your business rank higher and grow faster.
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
      <section className="relative py-16 md:py-24 px-4 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-primary to-primary-dark" />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] bg-gradient-to-r from-primary/20 to-primary/20 rounded-full blur-3xl hidden md:block" />
        <div className="relative max-w-2xl mx-auto text-center">
          <h2 className="text-3xl md:text-5xl font-extrabold mb-4 text-white">
            Get Free <span className="text-amber-300">Dhaka SEO Audit</span>
          </h2>
          <p className="text-white/80 mb-10 text-lg">
            Ready to dominate Dhaka&apos;s local search results? Let me analyze your current SEO and show you exactly how to rank higher in your neighborhood.
          </p>
          <Link href="/contact" className="group inline-flex items-center gap-2 bg-white text-primary-dark px-10 py-4 rounded-xl font-bold text-lg transition-all hover:shadow-xl hover:-translate-y-0.5">
            Claim Your Free Audit
            <span className="group-hover:translate-x-1 transition-transform">→</span>
          </Link>
        </div>
      </section>

      {/* === FOOTER === */}
      <Footer />
    </div>
  );
}
// force rebuild Thu Jul  9 07:58:51 UTC 2026
