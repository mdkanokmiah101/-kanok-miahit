"use client";
import { useEffect } from "react";
import Link from "next/link";

export default function AboutPage() {
  useEffect(() => {
    document.title = "About Us — Md Kanok Miah | SEO Agency in Bangladesh";
  }, []);

  return (
    <div className="min-h-screen bg-white text-gray-900">

      {/* === NAVBAR === */}
      <nav className="fixed top-0 w-full bg-white/95 backdrop-blur-xl border-b border-gray-100 z-50">
        <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
          <Link href="/" className="text-xl font-extrabold tracking-tight">
            <span className="text-primary">Md Kanok Miah</span>
          </Link>
          <Link href="/" className="text-sm text-gray-600 hover:text-primary transition-colors">← Back to Home</Link>
        </div>
      </nav>

      {/* === HERO — COMPANY STORY === */}
      <section className="relative pt-32 pb-16 px-4 overflow-hidden">
        <div className="absolute top-1/3 -left-32 w-96 h-96 bg-primary/20 rounded-full blur-3xl animate-pulse" />
        <div className="absolute bottom-1/4 -right-32 w-80 h-80 bg-primary/20 rounded-full blur-3xl animate-pulse delay-1000" />
        <div className="relative max-w-4xl mx-auto text-center">
          <div className="inline-flex items-center gap-2 bg-primary-light border border-primary/20 text-primary text-xs font-semibold px-5 py-2 rounded-full mb-8 backdrop-blur-sm">
            <span className="w-2 h-2 bg-primary rounded-full animate-pulse" />
            Our Story
          </div>
          <h1 className="text-4xl md:text-6xl lg:text-7xl font-extrabold tracking-tight leading-[1.05] mb-6">
            <span className="text-primary">
              About Md Kanok Miah
            </span>
          </h1>
          <p className="text-lg md:text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
            Founded in Dhaka, Bangladesh, Md Kanok Miah is a results-driven SEO agency that helps local businesses 
            dominate search engine rankings. We combine deep local market knowledge with global SEO best practices 
            to deliver measurable growth for Bangladeshi enterprises.
          </p>
        </div>
      </section>

      {/* === STORY SECTION === */}
      <section className="relative py-16 px-4">
        <div className="max-w-4xl mx-auto">
          <div className="bg-gray-50 border border-gray-100 rounded-2xl p-7 md:p-10">
            <h2 className="text-2xl md:text-3xl font-extrabold mb-4">
              <span className="text-primary">Our Story</span>
            </h2>
            <div className="space-y-4 text-gray-600 leading-relaxed">
              <p>
                Md Kanok Miah started with a simple observation: Bangladeshi businesses were struggling to get found 
                online. Most SEO agencies either offered generic solutions that didn't account for local search behaviour 
                or were located overseas with no real understanding of the Bangladesh market.
              </p>
              <p>
                Founded by <strong className="text-gray-900">Md Kanok Miah</strong>, our agency set out to bridge that gap. 
                With over 6 years of hands-on experience optimising websites for Bangladeshi audiences, we've developed 
                a proprietary approach that blends technical SEO rigour with deep cultural and linguistic insights.
              </p>
              <p>
                From small local shops in Dhaka to growing e-commerce brands serving customers nationwide, we've helped 
                over 50 clients achieve first-page rankings on Google. Our strategies account for Bengali-language queries, 
                mobile-first usage patterns, and the unique competitive landscape of Bangladesh's digital economy.
              </p>
              <p>
                Today, Md Kanok Miah is recognised as one of Bangladesh's most trusted SEO agencies, delivering 
                transparent, data-driven SEO services that generate real business results — not just vanity metrics.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* === MISSION & VISION === */}
      <section className="relative py-16 px-4">
        <div className="absolute top-0 right-0 w-72 h-72 bg-primary/10 rounded-full blur-3xl" />
        <div className="relative max-w-4xl mx-auto grid md:grid-cols-2 gap-5">
          <div className="bg-gray-50 border border-gray-100 rounded-2xl p-7 hover:bg-gray-100 hover:border-gray-200 transition-all">
            <div className="text-3xl mb-4">🎯</div>
            <h3 className="font-bold text-xl mb-3 text-gray-900">Our Mission</h3>
            <p className="text-gray-600 text-sm leading-relaxed">
              To empower Bangladeshi businesses with world-class SEO strategies that drive real, 
              measurable growth. We are committed to making quality search engine optimisation 
              accessible, transparent, and results-focused for every client we serve.
            </p>
          </div>
          <div className="bg-gray-50 border border-gray-100 rounded-2xl p-7 hover:bg-gray-100 hover:border-gray-200 transition-all">
            <div className="text-3xl mb-4">🔭</div>
            <h3 className="font-bold text-xl mb-3 text-gray-900">Our Vision</h3>
            <p className="text-gray-600 text-sm leading-relaxed">
              To be Bangladesh's most trusted SEO agency — known for integrity, transparency, 
              and exceptional results. We envision a digital Bangladesh where local businesses 
              compete and win on the global stage through the power of search.
            </p>
          </div>
        </div>
      </section>

      {/* === TEAM VALUES === */}
      <section className="relative py-16 px-4">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-12">
            <span className="text-primary text-sm font-semibold tracking-widest uppercase">What We Stand For</span>
            <h2 className="text-3xl md:text-5xl font-extrabold mt-3 mb-4">
              <span className="text-primary">Core Values</span>
            </h2>
            <p className="text-gray-600 max-w-xl mx-auto">The principles that guide every project and partnership.</p>
          </div>
          <div className="grid md:grid-cols-2 gap-5">
            {[
              { icon: "🔍", title: "Transparency First", desc: "No hidden fees, no vanity metrics, no empty promises. Every report shows real KPIs: rankings, traffic, conversions, and ROI." },
              { icon: "🇧🇩", title: "Local Expertise", desc: "We understand Bangladeshi search behaviour, Bengali + English query patterns, and Dhaka-centric business dynamics inside out." },
              { icon: "📊", title: "Data-Driven Decisions", desc: "Every strategy starts with thorough keyword research, competitor analysis, and real ranking data — never guesswork." },
              { icon: "⚡", title: "Results-Oriented", desc: "We target quick wins while building long-term authority. Our processes are designed to compound results over time." },
              { icon: "🤝", title: "Client Partnership", desc: "We treat your business like ours. Regular communication, collaborative strategy, and shared goals define every engagement." },
              { icon: "🌱", title: "Continuous Learning", desc: "SEO evolves daily. We invest in ongoing education, testing, and adaptation to stay ahead of every algorithm update." },
            ].map((v, i) => (
              <div key={i} className="group bg-gray-50 border border-gray-100 rounded-2xl p-7 hover:bg-gray-100 hover:border-gray-200 transition-all hover:-translate-y-1">
                <div className="text-3xl mb-4">{v.icon}</div>
                <h3 className="font-bold text-lg mb-2 text-gray-900">{v.title}</h3>
                <p className="text-gray-600 text-sm leading-relaxed">{v.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* === STATS BAND === */}
      <section className="relative py-16 border-y border-gray-100">
        <div className="absolute inset-0 bg-gradient-to-r from-primary/5 via-transparent to-primary/5" />
        <div className="relative max-w-5xl mx-auto px-4 grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
          {[
            { num: "350+", label: "Projects Done", color: "from-primary to-primary-dark" },
            { num: "50+", label: "Happy Clients", color: "from-primary to-primary-dark" },
            { num: "95%", label: "Client Retention", color: "from-primary to-primary-dark" },
            { num: "6+", label: "Years Exp.", color: "from-primary to-primary-dark" },
          ].map((stat, i) => (
            <div key={i}>
              <div className={`text-4xl md:text-5xl font-extrabold bg-gradient-to-b ${stat.color} bg-clip-text text-transparent`}>{stat.num}</div>
              <div className="text-gray-500 text-sm mt-1">{stat.label}</div>
            </div>
          ))}
        </div>
      </section>

      {/* === CTA === */}
      <section className="relative py-24 px-4 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-primary to-primary-dark" />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] bg-gradient-to-r from-primary/20 to-primary/20 rounded-full blur-3xl" />
        <div className="relative max-w-2xl mx-auto text-center">
          <h2 className="text-3xl md:text-5xl font-extrabold mb-4 text-white">Let&apos;s Grow Your <span className="text-amber-300">Business</span> Together</h2>
          <p className="text-primary/80 mb-10 text-lg">Ready to see what a dedicated SEO partnership can do for your Bangladesh business? Get your free audit today.</p>
          <Link href="/#contact" className="group inline-flex items-center gap-2 bg-white text-primary-dark px-10 py-4 rounded-xl font-bold text-lg transition-all hover:shadow-xl hover:-translate-y-0.5">
            Get Your Free Audit
            <span className="group-hover:translate-x-1 transition-transform">→</span>
          </Link>
        </div>
      </section>

      {/* === FOOTER === */}
      <footer className="py-8 border-t border-gray-100 text-center text-sm text-gray-500">
        <p>© 2026 <span className="text-primary font-bold">Md Kanok Miah</span> — SEO Agency in Bangladesh. All rights reserved.</p>
        <div className="mt-3 flex items-center justify-center gap-4 text-xs">
          <Link href="/about" className="hover:text-primary transition-colors">About</Link>
          <Link href="/privacy-policy" className="hover:text-primary transition-colors">Privacy Policy</Link>
          <Link href="/terms-of-service" className="hover:text-primary transition-colors">Terms of Service</Link>
        </div>
      </footer>

    </div>
  );
}
