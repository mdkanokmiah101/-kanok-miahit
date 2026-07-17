"use client";
import { useState } from "react";
import Link from "next/link";
import Footer from "@/components/Footer";

export default function HomeClient({ faqs = [] }) {
  const [menuOpen, setMenuOpen] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [activeTab, setActiveTab] = useState("reviews");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      const form = e.target;
      const data = new FormData(form);
      const res = await fetch("/api/contact", { method: "POST", body: data });
      const result = await res.json();
      if (result.success) {
        setSubmitted(true);
        form.reset();
      }
    } catch (err) {
      console.error("Form error:", err);
    }
    setSubmitting(false);
  };

  const navItem = [
    { name: "Services", path: "/services" },
    { name: "Case Studies", path: "/case-studies" },
    { name: "Industries", path: "/industries" },
    { name: "Blog", path: "/blog" },
    { name: "About", path: "/about" },
    { name: "Contact", path: "/contact" }
  ];

  // FAQ data is passed from page.js via props for schema-data sync

  return (
    <div className="min-h-screen bg-white">
      

      {/* ===== NAVBAR ===== */}
      <nav className="fixed top-0 w-full bg-white/90 backdrop-blur-xl border-b border-gray-100 z-50">
        <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
          <Link href="/" className="text-xl font-extrabold tracking-tight">
            <span className="text-primary">Kanok Miah</span>
          </Link>
          <div className="hidden md:flex items-center gap-8 text-sm font-medium text-gray-600">
            {navItem.map(item => (
              <Link key={item.name} href={item.path} className="hover:text-primary transition-colors">{item.name}</Link>
            ))}
            <Link href="/contact" className="bg-primary text-white text-sm font-bold px-5 py-2.5 rounded-full hover:bg-primary-dark hover:shadow-lg hover:shadow-primary/25 transition-all">Free Audit</Link>
          </div>
          <button onClick={() => setMenuOpen(!menuOpen)} className="md:hidden text-2xl text-gray-700" aria-label="Toggle menu">☰</button>
        </div>
        {menuOpen && (
          <div className="md:hidden bg-white border-b border-gray-100 px-4 pb-5 flex flex-col gap-3 text-sm font-medium text-gray-600">
            {navItem.map(item => (
              <Link key={item.name} href={item.path} onClick={() => setMenuOpen(false)} className="hover:text-primary transition-colors">{item.name}</Link>
            ))}
            <Link href="/contact" onClick={() => setMenuOpen(false)} className="bg-primary text-white text-center font-bold px-5 py-2.5 rounded-full">Free Audit</Link>
          </div>
        )}
      </nav>

      {/* ===== FLOATING WHATSAPP ===== */}
      <a href="https://wa.me/8801604809110?text=Hi%20Kanok%20Miah!%20I%20need%20SEO%20help%20for%20my%20business."
        target="_blank" rel="noopener noreferrer"
        className="fixed bottom-6 right-6 z-50 w-14 h-14 bg-emerald-500 rounded-full flex items-center justify-center text-2xl shadow-lg hover:bg-emerald-400 hover:scale-110 hover:shadow-emerald-500/40 transition-all animate-bounce"
        aria-label="Chat on WhatsApp">💬</a>

      {/* ===== HERO ===== */}
      <section className="relative min-h-[90vh] flex items-center pt-20 pb-16 px-4 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-primary/[0.07] via-white to-primary/[0.04]" />
        <div className="absolute top-1/4 -left-32 w-[500px] h-[500px] bg-primary/20 rounded-full blur-[120px]" />
        <div className="absolute bottom-1/4 -right-32 w-[400px] h-[400px] bg-primary/10 rounded-full blur-[100px]" />

        <div className="relative max-w-7xl mx-auto w-full grid lg:grid-cols-2 gap-8 lg:gap-16 items-center">
          <div className="lg:max-w-2xl">
            <div className="inline-flex items-center gap-2 bg-primary/10 border border-primary/20 text-primary text-xs font-semibold px-4 py-2 rounded-full mb-6">
              <span className="w-2 h-2 bg-primary rounded-full animate-pulse" />
              #1 SEO Expert in Bangladesh
            </div>
            <h1 className="text-4xl sm:text-5xl lg:text-5xl xl:text-6xl font-extrabold tracking-tight leading-[1.08] mb-4 lg:mb-6">
              <span className="text-primary">Best SEO Expert</span>{' '}
              <span className="block text-gray-900 whitespace-nowrap">in Dhaka, Bangladesh</span>
            </h1>
            <p className="text-gray-700 text-lg mb-8 leading-relaxed">
              Your competitors are ranking. You&apos;re not. That&apos;s not bad luck — that&apos;s a fixable problem. I&apos;m <strong className="text-gray-900">Kanok Miah</strong>, <strong className="text-gray-900">the best SEO expert in Dhaka, Bangladesh</strong> who has run <strong className="text-gray-900">210+ SEO campaigns</strong> across e-commerce, local businesses — and I don&apos;t do cookie-cutter strategies. I build what your specific business needs to win on Google, on AI search, and everywhere in between. <strong className="text-gray-900">6 years</strong>. Real results. No vanity metrics. Let&apos;s fix your rankings — starting today.
            </p>
            <div className="flex flex-wrap gap-3 mb-8">
              <a href="https://www.facebook.com/mdkanokmiahweb" target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1.5 bg-blue-50 border border-blue-200 text-blue-700 text-xs font-semibold px-4 py-2 rounded-full hover:bg-blue-100 hover:shadow-sm transition-all">👍 Follow on Facebook</a>
            </div>
            <div className="flex flex-col sm:flex-row gap-4">
              <Link href="/contact" className="inline-flex items-center justify-center gap-2 bg-primary hover:bg-primary-dark text-white px-8 py-4 rounded-xl font-bold text-lg transition-all hover:shadow-xl hover:shadow-primary/30 hover:-translate-y-0.5">
                Get Free SEO Audit
                <span className="text-lg">→</span>
              </Link>
              <Link href="/services" className="inline-flex items-center justify-center gap-2 border-2 border-gray-200 text-gray-700 px-8 py-4 rounded-xl font-semibold text-lg hover:border-primary/30 hover:text-primary transition-all">
                View Services
              </Link>
            </div>
            <div className="mt-10 flex flex-wrap gap-6">
              <div className="flex items-center gap-2 bg-gray-50 border border-gray-100 rounded-xl px-4 py-2.5">
                <span className="text-2xl">🏆</span>
                <div><div className="text-sm font-bold text-gray-900">Since 2019</div><div className="text-xs text-gray-600">Experience</div></div>
              </div>
              <div className="flex items-center gap-2 bg-gray-50 border border-gray-100 rounded-xl px-4 py-2.5">
                <span className="text-2xl">📈</span>
                <div><div className="text-sm font-bold text-gray-900">210+</div><div className="text-xs text-gray-600"><Link href="/services" className="text-primary hover:underline font-semibold">SEO</Link> Projects</div></div>
              </div>
              <div className="flex items-center gap-2 bg-gray-50 border border-gray-100 rounded-xl px-4 py-2.5">
                <span className="text-2xl">⭐</span>
                <div><div className="text-sm font-bold text-gray-900">4.9/5</div><div className="text-xs text-gray-600">Rating</div></div>
              </div>
            </div>
          </div>

          <div className="relative">
            {/* ===== LEAD FORM - Replaces Image ===== */}
            <div className="bg-white rounded-2xl shadow-2xl border border-gray-100 p-6 max-w-sm mx-auto">
              <h3 className="text-lg font-bold text-center text-gray-900 mb-3">
                🚀 Get <span className="text-primary">Free SEO Audit</span> & Proposal
              </h3>
              <form onSubmit={handleSubmit} className="space-y-3">
                <input type="text" name="name" placeholder="Your Name" required
                  className="w-full bg-gray-50 border border-gray-200 rounded-xl px-4 py-3 text-sm text-gray-900 placeholder-gray-400 focus:outline-none focus:border-primary focus:ring-2 focus:ring-primary/10 transition-all" />
                <div className="flex gap-2">
                  <span className="inline-flex items-center bg-gray-100 border border-gray-200 rounded-xl px-3 text-sm text-gray-500">+880</span>
                  <input type="tel" name="phone" placeholder="1XXXXXXXXX" required
                    className="flex-1 bg-gray-50 border border-gray-200 rounded-xl px-4 py-3 text-sm text-gray-900 placeholder-gray-400 focus:outline-none focus:border-primary focus:ring-2 focus:ring-primary/10 transition-all" />
                </div>
                <input type="text" name="website" placeholder="Your Website (optional)"
                  className="w-full bg-gray-50 border border-gray-200 rounded-xl px-4 py-3 text-sm text-gray-900 placeholder-gray-400 focus:outline-none focus:border-primary focus:ring-2 focus:ring-primary/10 transition-all" />
                <input type="hidden" name="source" value="homepage-hero-form" />
                <p className="text-gray-500 text-[11px] text-center">📧 We'll send your report to: <strong>mdkanokmiah101@gmail.com</strong></p>
                <button type="submit" disabled={submitting}
                  className="w-full bg-primary hover:bg-primary-dark text-white font-bold py-3.5 rounded-xl transition-all hover:shadow-lg hover:shadow-primary/25 disabled:opacity-50">
                  {submitting ? "Sending..." : submitted ? "✅ Sent! I'll WhatsApp you shortly" : "🔍 Get My Free Audit"}
                </button>
              </form>
              {/* WhatsApp Option Inside Form */}
              <div className="relative my-2">
                <div className="absolute inset-0 flex items-center"><div className="w-full border-t border-gray-200"></div></div>
                <div className="relative flex justify-center text-xs"><span className="bg-white px-2 text-gray-500">OR</span></div>
              </div>
              <a href="https://wa.me/8801604809110?text=Hi%20Kanok%20Miah!%20I%20need%20SEO%20help%20for%20my%20business." target="_blank"
                className="flex items-center justify-center gap-2 w-full bg-green-500 hover:bg-green-600 text-white font-semibold py-2.5 rounded-xl transition-all text-sm">
                💬 Chat on WhatsApp <span className="text-white">01604809110</span>
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* ===== STATS BAND ===== */}
      <section className="relative py-14 bg-gradient-to-r from-primary to-primary-dark overflow-hidden">
        <div className="relative max-w-6xl mx-auto px-4 grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
          {[
            { num: "210+", label: <><Link href="/services" className="text-white hover:text-amber-300 underline font-semibold">SEO</Link> Projects</> },
            { num: "50+", label: "Happy Clients" },
            { num: "95%", label: "Client Retention" },
            { num: "Since 2019", label: "Experience" },
          ].map((stat, i) => (
            <div key={i} className="py-2">
              <div className="text-3xl md:text-5xl font-extrabold text-white">{stat.num}</div>
              <div className="text-white/80 text-xs md:text-sm mt-1 font-medium uppercase tracking-wider">{stat.label}</div>
            </div>
          ))}
        </div>
        {/* Service Areas — internal links to location pages */}
        <div className="relative max-w-5xl mx-auto px-4 mt-10 pt-6 border-t border-white/20 text-center">
          <div className="text-white/60 text-xs font-semibold uppercase tracking-[0.15em] mb-3">📍 Service Areas</div>
          <div className="flex flex-wrap justify-center gap-2">
            <Link href="/locations/dhaka" className="text-xs bg-white/10 text-white px-3 py-1.5 rounded-full hover:bg-white/20 transition-colors">Dhaka</Link>
          </div>
        </div>
      </section>

      {/* ===== REVIEWS & TRAINING ===== */}
      <section className="relative py-24 px-4 bg-gray-50/50 overflow-hidden">
        <div className="absolute top-1/3 left-0 w-64 h-64 bg-primary/5 rounded-full blur-3xl" />
        <div className="absolute bottom-0 right-1/4 w-80 h-80 bg-primary-light/40 rounded-full blur-3xl" />
        <div className="relative max-w-5xl mx-auto">
          <div className="text-center mb-12">
            <span className="inline-block text-primary text-sm font-semibold tracking-[0.2em] uppercase px-4 py-1.5 bg-primary-light/60 rounded-full border border-primary/10">Social Proof</span>
            <h2 className="text-3xl md:text-5xl font-extrabold mt-5 mb-4 text-gray-900">
              Reviews & <span className="text-primary">Training</span>
            </h2>
            <p className="text-gray-500 max-w-2xl mx-auto text-lg">
              See what clients say about my work and explore free SEO training content.
            </p>
          </div>

          {/* Tabs */}
          <div className="flex justify-center mb-10">
            <div className="inline-flex bg-white rounded-full p-1 shadow-sm border border-gray-100">
              <button
                onClick={() => setActiveTab('reviews')}
                className={`px-6 md:px-8 py-2.5 rounded-full text-sm font-semibold transition-all duration-300 ${
                  activeTab === 'reviews'
                    ? 'bg-primary text-white shadow-md'
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                ⭐ Reviews
              </button>
              <button
                onClick={() => setActiveTab('training')}
                className={`px-6 md:px-8 py-2.5 rounded-full text-sm font-semibold transition-all duration-300 ${
                  activeTab === 'training'
                    ? 'bg-primary text-white shadow-md'
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                🎓 Training
              </button>
            </div>
          </div>

          {/* Reviews Tab Content */}
          {activeTab === 'reviews' && (
            <div className="grid md:grid-cols-2 gap-6">
              <div className="aspect-video rounded-2xl overflow-hidden shadow-lg bg-white">
                <iframe
                  src="https://www.youtube.com/embed/eIyD-ugY7_0"
                  title="Client Review 1"
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                  allowFullScreen
                  className="w-full h-full"
                />
              </div>
              <div className="aspect-video rounded-2xl overflow-hidden shadow-lg bg-white">
                <iframe
                  src="https://www.youtube.com/embed/hqtG7FM_ZAY"
                  title="Client Review 2"
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                  allowFullScreen
                  className="w-full h-full"
                />
              </div>
            </div>
          )}

          {/* Training Tab Content */}
          {activeTab === 'training' && (
            <div className="grid md:grid-cols-2 gap-6">
              <div className="aspect-video rounded-2xl overflow-hidden shadow-lg bg-white">
                <iframe
                  src="https://www.youtube.com/embed/yeF59fPBm_I"
                  title="SEO Training 1"
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                  allowFullScreen
                  className="w-full h-full"
                />
              </div>
              <div className="aspect-video rounded-2xl overflow-hidden shadow-lg bg-white">
                <iframe
                  src="https://www.youtube.com/embed/TxW-EGH7SAo"
                  title="SEO Training 2"
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                  allowFullScreen
                  className="w-full h-full"
                />
              </div>
            </div>
          )}
        </div>
      </section>

      {/* ===== ABOUT ME ===== */}
      <section className="relative py-24 px-4 overflow-hidden">
        <div className="absolute top-0 left-0 w-72 h-72 bg-primary/5 rounded-full blur-3xl" />
        <div className="absolute bottom-0 right-0 w-96 h-96 bg-primary-light/50 rounded-full blur-3xl" />
        <div className="relative max-w-6xl mx-auto">
          <div className="grid md:grid-cols-2 gap-10 md:gap-16 items-center">
            {/* Photo */}
            <div className="flex justify-center md:justify-end">
              <div className="relative">
                <div className="w-full h-full max-w-md mx-auto rounded-2xl overflow-hidden shadow-2xl border-[4px] border-white">
                  <img
                    src="/kanok-miah-about.webp"
                    alt="Kanok Miah — SEO Expert in Dhaka, Bangladesh"
                    width="1024"
                    height="682"
                    className="w-full h-full object-cover"
                  />
                </div>
                {/* Decorative elements */}
                <div className="absolute -top-4 -right-4 w-20 h-20 bg-primary/10 rounded-full blur-xl" />
                <div className="absolute -bottom-4 -left-4 w-16 h-16 border-2 border-primary/20 rounded-full" />
                {/* Experience badge */}
                <div className="absolute -bottom-3 -right-3 bg-primary text-white text-xs font-bold px-4 py-2 rounded-xl shadow-lg">
                  ⭐ 4.9/5 · 108+ Reviews
                </div>
              </div>
            </div>
            {/* Content */}
            <div className="max-w-xl">
              <span className="text-primary text-sm font-semibold tracking-[0.2em] uppercase">About Me</span>
              <h2 className="text-3xl md:text-5xl font-extrabold mt-3 mb-6 text-gray-900">
                <span className="text-primary">Kanok Miah</span><br />
                SEO Expert Since 2019
              </h2>
              <div className="space-y-4 text-gray-600 leading-relaxed">
                <p>
                  I'm <strong className="text-gray-900">Kanok Miah</strong> — a results-driven 
                  <strong className="text-gray-900"> SEO expert in Bangladesh</strong> who has been helping 
                  local businesses dominate <a href="https://developers.google.com/search" target="_blank" rel="noopener noreferrer" className="text-primary hover:underline">search rankings</a> <strong className="text-gray-900">since 2019</strong>. 
                  I've led <strong className="text-gray-900">210+ SEO projects</strong> for clients ranging 
                  from small local shops in Dhaka to international brands.
                </p>
                <p>
                  Currently serving as <strong className="text-gray-900">SEO Project Manager at <a href="https://www.khanit.com.bd/about/" target="_blank" rel="noopener noreferrer" className="text-primary hover:underline">Khan IT</a></strong> 
                  and <strong className="text-gray-900">Head of Digital Marketing at <a href="https://cloudmatrixtech.com/" target="_blank" rel="noopener noreferrer" className="text-primary hover:underline">CloudMatrix Tech</a></strong>. 
                  Every month I actively manage <strong className="text-gray-900">8–12 live SEO projects</strong> 
                  and <strong className="text-gray-900">2–5 paid ad campaigns</strong> — running real experiments 
                  on real websites to discover <a href="https://developers.google.com/search/docs/fundamentals/ranking-systems" target="_blank" rel="noopener noreferrer" className="text-primary hover:underline">what actually moves rankings</a>.
                </p>
                <p>
                  Certified by <strong className="text-gray-900">Google Digital Garage, HubSpot Academy, 
                  <a href="https://www.semrush.com/academy/" target="_blank" rel="noopener noreferrer" className="text-primary hover:underline">SEMrush Academy</a>, 
                  <a href="https://www.linkedin.com/learning/" target="_blank" rel="noopener noreferrer" className="text-primary hover:underline">LinkedIn Learning</a>, 
                  Coursera, Skillshare, and <a href="https://www.youtube.com/" target="_blank" rel="noopener noreferrer" className="text-primary hover:underline">YouTube</a></strong> 
                  — but the real learning came from doing. Every algorithm update, every ranking drop, every unexpected win taught me 
                  something no course ever could.
                </p>
              </div>
              <div className="flex flex-wrap gap-3 mt-8">
                <Link href="/about" className="inline-flex items-center gap-2 bg-primary hover:bg-primary-dark text-white px-6 py-3 rounded-xl font-semibold text-sm transition-all hover:shadow-lg">
                  Full Story <span>→</span>
                </Link>
                <Link href="/contact" className="inline-flex items-center gap-2 border-2 border-gray-200 text-gray-700 px-6 py-3 rounded-xl font-semibold text-sm hover:border-primary/30 hover:text-primary transition-all">
                  Let's Talk
                </Link>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ===== SERVICES ===== */}
      <section id="services" className="py-24 px-4 bg-gray-50/80">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <span className="text-primary text-sm font-semibold tracking-[0.2em] uppercase">What We Do</span>
            <h2 className="text-3xl md:text-5xl font-extrabold mt-4 mb-4 text-gray-900">Best SEO Services in <span className="text-primary">Dhaka, Bangladesh</span> — Local, Technical & GEO</h2>
            <p className="text-gray-500 max-w-2xl mx-auto text-lg">Complete SEO solutions tailored for the Bangladesh market — from local Dhaka SEO to international optimization.</p>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[
              { icon: "🔍", title: "Local SEO", desc: "Rank your business on Google Maps across Dhaka, Chittagong, Sylhet and beyond. GBP optimization, local citations, near-me SEO for Bangladeshi audiences.", slug: "local-seo" },
              { icon: "📄", title: "On-Page SEO", desc: "Keyword-optimized content, meta tags, header structure, internal linking, and schema markup crafted for Bangladesh search behavior.", slug: "on-page-seo" },
              { icon: "🔗", title: "Link Building", desc: "Quality backlinks from Bangladeshi and international directories, guest posts, and niche-relevant websites that drive real authority gains.", slug: "link-building" },
              { icon: "⚙️", title: "Technical SEO", desc: "Site speed optimization, Core Web Vitals, mobile-first indexing, crawl budget fixes, and structured data implementation.", slug: "technical-seo" },
              { icon: "🤖", title: "GEO / AI Search", desc: "Optimize for ChatGPT, Gemini, Perplexity, and Google AI Overviews. Entity-first SEO built for the AI-powered search era.", slug: "geo-ai-search" },
              { icon: "🛒", title: "E-commerce SEO", desc: "Shopify, Daraz, WooCommerce SEO. Product page optimization, category restructuring, and conversion-focused search strategy.", slug: "ecommerce-seo" },
            ].map((s, i) => (
              <Link key={i} href={`/services/${s.slug}`} className="group bg-white rounded-2xl p-7 border border-gray-100 hover:border-primary/20 hover:shadow-xl hover:-translate-y-1 transition-all duration-300">
                <div className="w-14 h-14 rounded-2xl bg-primary/10 flex items-center justify-center text-2xl mb-5 group-hover:bg-primary group-hover:text-white transition-all duration-300">{s.icon}</div>
                <h3 className="font-bold text-lg mb-2 text-gray-900">{s.title}</h3>
                <p className="text-gray-600 text-sm leading-relaxed">{s.desc}</p>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* ===== INDUSTRIES ===== */}
      <section id="industries" className="py-24 px-4">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <span className="text-primary text-sm font-semibold tracking-[0.2em] uppercase">Industries We Serve</span>
            <h2 className="text-3xl md:text-5xl font-extrabold mt-4 mb-4 text-gray-900">Industry-Specific <span className="text-primary">SEO Solutions</span> for Bangladesh</h2>
            <p className="text-gray-500 max-w-2xl mx-auto text-lg">Every industry has unique SEO challenges. We tailor strategies that work for your specific sector in Bangladesh.</p>
          </div>
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {[
              { icon: "👕", title: "Garments & Textile", desc: "RMG exporters, textile mills — B2B SEO for international buyers", slug: "garments-textile" },
              { icon: "🛒", title: "E-commerce", desc: "Daraz sellers, Shopify stores — product SEO for higher sales", slug: "ecommerce" },
              { icon: "📱", title: "SMM Panel", desc: "Social media agencies — local SEO to attract Dhaka businesses", slug: "smm-panel" },
              { icon: "🏢", title: "Real Estate", desc: "Developers, agents — rank for property keywords", slug: "real-estate" },
              { icon: "🧹", title: "Cleaning Services", desc: "Office & home cleaning — dominate Google Maps", slug: "cleaning" },
              { icon: "💆", title: "Spa & Salon", desc: "Beauty parlours — near-me SEO for foot traffic", slug: "spa-salon" },
              { icon: "🏥", title: "Medical & Healthcare", desc: "Hospitals, clinics — E-E-A-T healthcare SEO", slug: "medical" },
              { icon: "🎓", title: "Education", desc: "Universities, coaching — student inquiry generation", slug: "education" },
              { icon: "🍽️", title: "Food & Restaurant", desc: "Restaurants — Google Maps dominance for dining", slug: "food-restaurant" },
            ].map((ind, i) => (
              <Link key={i} href={`/industries/${ind.slug}`}
                className="group bg-gray-50 rounded-2xl p-6 border border-gray-100 hover:border-primary/20 hover:bg-primary-light hover:-translate-y-1 transition-all duration-300">
                <div className="text-3xl mb-3">{ind.icon}</div>
                <h3 className="font-bold text-gray-900 mb-1.5 group-hover:text-primary transition-colors">{ind.title}</h3>
                <p className="text-gray-600 text-sm leading-relaxed">{ind.desc}</p>
                <div className="mt-3 text-primary text-xs font-semibold opacity-0 group-hover:opacity-100 transition-all duration-300">Learn More →</div>
              </Link>
            ))}
          </div>
          <div className="text-center mt-10">
            <Link href="/industries" className="inline-flex items-center gap-2 text-primary font-semibold hover:text-primary-dark transition-colors">
              View All Industries <span>→</span>
            </Link>
          </div>
        </div>
      </section>

      {/* ===== WHY US ===== */}
      <section id="about" className="py-24 px-4 bg-gray-50/80">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <span className="text-primary text-sm font-semibold tracking-[0.2em] uppercase">Why Choose Me</span>
            <h2 className="text-3xl md:text-5xl font-extrabold mt-4 mb-4 text-gray-900">Why I'm the <span className="text-primary">Best SEO Expert in Dhaka</span></h2>
            <p className="text-gray-500 max-w-2xl mx-auto text-lg">Since 2019, mastering SEO for the Bangladesh market. Here&apos;s what sets me apart.</p>
          </div>
          <div className="grid md:grid-cols-2 gap-6">
            {[
              { icon: "🇧🇩", title: "Local Market Expertise", desc: "Deep understanding of Bangladeshi search behavior — Bengali + English queries, local intent, and Dhaka-centric business patterns." },
              { icon: "📊", title: "Data-Driven Approach", desc: "Every strategy starts with thorough keyword research, competitor analysis, and real ranking data — never guesswork." },
              { icon: "⚡", title: "Fast, Tangible Results", desc: "Quick wins through GSC fixes, content gaps, and technical improvements while building sustainable long-term authority." },
              { icon: "📋", title: "Transparent Reporting", desc: "Monthly reports with real KPIs: rankings, traffic, conversions, ROI. No vanity metrics. Just results you can see." },
            ].map((a, i) => (
              <div key={i} className="group bg-white rounded-2xl p-7 border border-gray-100 hover:border-primary/20 hover:shadow-lg hover:-translate-y-1 transition-all duration-300 flex gap-5">
                <div className="text-4xl shrink-0">{a.icon}</div>
                <div>
                  <h3 className="font-bold text-lg mb-2 text-gray-900">{a.title}</h3>
                  <p className="text-gray-600 text-sm leading-relaxed">{a.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ===== CASE STUDIES / SUCCESS STORIES (Brand Dark Green) ===== */}
      <section className="relative py-24 px-4 overflow-hidden" style={{ backgroundColor: '#0D3D14' }}>
        <div className="absolute top-0 right-0 w-96 h-96" style={{ backgroundColor: '#124D1C', opacity: '0.3', borderRadius: '50%', filter: 'blur(80px)' }} />
        <div className="absolute bottom-0 left-0 w-80 h-80" style={{ backgroundColor: '#124D1C', opacity: '0.4', borderRadius: '50%', filter: 'blur(100px)' }} />
        <div className="relative max-w-6xl mx-auto">
          <div className="text-center mb-14">
            <span className="inline-block text-[#E8F5E9] text-xs font-bold tracking-[0.2em] uppercase px-4 py-2 rounded-full border" style={{ borderColor: 'rgba(232,245,233,0.2)', backgroundColor: 'rgba(232,245,233,0.08)' }}>
              Proven Results
            </span>
            <h2 className="text-3xl md:text-5xl font-extrabold mt-5 mb-4" style={{ color: '#FFFFFF' }}>
              SEO <span style={{ color: '#E8F5E9' }}>Success Stories</span>
            </h2>
            <p className="max-w-2xl mx-auto text-lg" style={{ color: 'rgba(255,255,255,0.5)' }}>
              Real case studies with verified metrics — no fluff, no guesswork.
            </p>
          </div>

          {/* Case Study Cards Grid — No Images, Real Links */}
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {[
              { name: "Das Taxis", website: "https://www.dastaxis.co.uk/", metric: "893/mo", label: "Organic Visitors", growth: "+5,853%", tag: "Transportation", url: "/blog/das-taxis-scotland-seo-case-study" },
              { name: "Locksmith Dundee", website: "https://locksmithdundee.scot/", metric: "1.4K/mo", label: "Organic Traffic", growth: "+6,919%", tag: "Local Services", url: "/blog/locksmith-dundee-seo-case-study" },
              { name: "WatchZoneBD", website: "https://watchzonebd.com", metric: "46K+/mo", label: "Organic Traffic", growth: "3,883%", tag: "E-commerce", url: "/blog/watchzonebd-seo-case-study" },
              { name: "Dhaka Apparels", website: "https://dhaka-apparels.com/", metric: "8K/mo", label: "Organic Traffic", growth: "+3,000%", tag: "Garments", url: "/blog/dhaka-apparels-seo-case-study" },
              { name: "SMMGen", website: "https://smmgen.com", metric: "27.9K/mo", label: "Organic Clicks", growth: "+87,000%", tag: "SMM Panel", url: "/blog/smmgen-seo-case-study" },
              { name: "SMMSun", website: "https://smmsun.com", metric: "7.7K/mo", label: "Organic Clicks", growth: "+15,440%", tag: "SMM Panel", url: "/blog/smmsun-seo-case-study" },
            ].map((item, i) => (
              <a
                key={i}
                href={item.url}
                className="group rounded-xl border overflow-hidden transition-all duration-300 hover:-translate-y-1 hover:shadow-xl"
                style={{ backgroundColor: '#1B5E20', borderColor: 'rgba(255,255,255,0.08)' }}
                target="_blank"
                rel="noopener noreferrer"
              >
                <div className="p-6">
                  <div className="flex items-center justify-between mb-4">
                    <span className="text-xs font-bold uppercase tracking-wider px-3 py-1 rounded-full" style={{ color: '#E8F5E9', backgroundColor: 'rgba(232,245,233,0.1)' }}>{item.tag}</span>
                    <span className="text-xs font-extrabold px-2.5 py-1 rounded-full" style={{ color: '#FFD230', backgroundColor: 'rgba(255,210,48,0.15)' }}>{item.growth}</span>
                  </div>
                  {item.website ? <a href={item.website} target="_blank" className="font-bold text-lg" style={{color:'#FFFFFF'}}>{item.name}</a> : <h3 className="font-bold text-lg mb-1" style={{color:'#FFFFFF'}}>{item.name}</h3>}
                  <div className="mb-4">
                    <span className="text-2xl font-extrabold" style={{ color: '#81C784' }}>{item.metric}</span>
                    <span className="block text-xs mt-0.5" style={{ color: '#FFFFFF' }}>{item.label}</span>
                  </div>
                  <div className="flex items-center gap-1.5 text-sm font-semibold transition-all group-hover:gap-2.5" style={{ color: '#FFFFFF' }}>
                    View Case Study
                    <span className="text-base">→</span>
                  </div>
                </div>
                <div className="h-[3px] w-0 group-hover:w-full transition-all duration-500" style={{ backgroundColor: '#FFD230' }} />
              </a>
            ))}
          </div>

          <div className="text-center mt-10">
            <a href="/case-studies" className="inline-flex items-center gap-2 px-8 py-3.5 rounded-xl font-bold text-sm transition-all hover:shadow-lg" style={{ backgroundColor: '#E8F5E9', color: '#0D3D14' }}>
              View All Case Studies <span>→</span>
            </a>
          </div>
        </div>
      </section>

      {/* ===== PROCESS ===== */}
      <section className="py-24 px-4">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <span className="text-primary text-sm font-semibold tracking-[0.2em] uppercase">How We Work</span>
            <h2 className="text-3xl md:text-5xl font-extrabold mt-4 mb-4 text-gray-900">My <span className="text-primary">5-Step</span> Process</h2>
            <p className="text-gray-500 max-w-2xl mx-auto text-lg">A proven system that delivers measurable SEO results for Bangladeshi businesses.</p>
          </div>
          <div className="relative">
            <div className="hidden lg:block absolute top-16 left-[10%] right-[10%] h-0.5 bg-primary/20" />
            <div className="grid lg:grid-cols-5 gap-8">
              {[
                { step: "01", title: "Audit", desc: "Full site analysis — technical, content, backlinks, and competitors", color: "from-primary to-primary-dark" },
                { step: "02", title: "Strategy", desc: "Custom SEO plan with Bangladesh keyword targeting", color: "from-primary to-primary-dark" },
                { step: "03", title: "Execute", desc: "On-page fixes, content creation, link building, technical SEO", color: "from-primary to-primary-dark" },
                { step: "04", title: "Monitor", desc: "Track rankings, traffic, and conversions every week", color: "from-primary to-primary-dark" },
                { step: "05", title: "Optimize", desc: "Iterate and improve based on real performance data", color: "from-primary to-primary-dark" },
              ].map((p, i) => (
                <div key={i} className="relative text-center group">
                  <div className={`relative z-10 w-16 h-16 mx-auto mb-5 rounded-2xl bg-gradient-to-br ${p.color} text-white flex items-center justify-center font-extrabold text-sm shadow-lg group-hover:scale-110 group-hover:shadow-xl transition-all duration-300`}>
                    {p.step}
                  </div>
                  <h3 className="font-bold text-gray-900 mb-2 text-lg">{p.title}</h3>
                  <p className="text-gray-600 text-sm leading-relaxed">{p.desc}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* ===== CTA BANNER ===== */}
      <section className="relative py-24 px-4 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-primary to-primary-dark" />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-white/10 rounded-full blur-[100px]" />
        <div className="relative max-w-3xl mx-auto text-center">
          <span className="inline-block text-amber-300 text-sm font-semibold tracking-[0.2em] uppercase mb-4">Free Offer</span>
          <h2 className="text-3xl md:text-5xl font-extrabold mb-4 text-white">
            Ready to <span className="text-amber-300">Dominate</span> Search Results?
          </h2>
          <p className="text-white/80 mb-10 text-lg max-w-xl mx-auto">
            Get a free SEO audit for your Bangladesh business. No commitment. No hidden fees. Just real, actionable insights.
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link href="/contact" className="inline-flex items-center gap-2 bg-white text-primary-dark px-10 py-4 rounded-xl font-bold text-lg transition-all hover:shadow-xl hover:-translate-y-0.5">
              Get Your Free Audit <span>→</span>
            </Link>
            <a href="https://wa.me/8801604809110?text=Hi%20Kanok%20Miah!%20I%20want%20a%20free%20SEO%20audit."
              target="_blank" rel="noopener noreferrer"
              className="inline-flex items-center gap-2 border-2 border-white/30 text-white px-10 py-4 rounded-xl font-bold text-lg hover:bg-white/10 transition-all">
              💬 WhatsApp Me
            </a>
          </div>
        </div>
      </section>

      {/* ===== PEOPLE ALSO ASK ===== */}
      <section className="py-20 px-4 bg-gray-50/80">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-2xl md:text-4xl font-extrabold text-gray-900">
              People Also Ask About <span className="text-primary">SEO in Bangladesh</span>
            </h2>
            <p className="text-gray-600 mt-3 max-w-2xl mx-auto">
              Common questions business owners in Dhaka, Chittagong, and Sylhet ask about search engine optimization.
            </p>
          </div>
          <div className="divide-y divide-gray-100 bg-white border border-gray-100 rounded-2xl p-4 md:p-6 shadow-sm">
            {faqs.map((item, i) => (
              <details key={i} className="py-4 group">
                <summary className="flex justify-between items-center font-semibold text-gray-900 cursor-pointer list-none">
                  <span>{item.question}</span>
                  <span className="text-primary transition-transform group-open:rotate-180 shrink-0 ml-4">▼</span>
                </summary>
                <p className="text-gray-600 mt-3 pl-2 leading-relaxed">{item.answer}</p>
              </details>
            ))}
          </div>
        </div>
      </section>

      {/* ===== CONTACT ===== */}
      <section id="contact" className="py-24 px-4 bg-gray-50/80">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <span className="text-primary text-sm font-semibold tracking-[0.2em] uppercase">Get In Touch</span>
            <h2 className="text-3xl md:text-5xl font-extrabold mt-4 mb-4 text-gray-900">Let&apos;s Grow Your <span className="text-primary">Business</span></h2>
            <p className="text-gray-500 max-w-xl mx-auto text-lg">Fill out the form and I&apos;ll get back to you within 24 hours.</p>
          </div>
          <div className="grid lg:grid-cols-2 gap-10 items-start">
            {/* Form */}
            <div className="bg-white border border-gray-200 rounded-2xl p-8 shadow-sm hover:shadow-md transition-all">
              <form id="contactForm" onSubmit={handleSubmit} method="POST" className="space-y-5">
                <input type="hidden" name="_subject" value="New SEO Lead from Kanok Miah Website!" />
                <div className="grid sm:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm text-gray-700 mb-1.5 font-medium">Your Name *</label>
                    <input type="text" name="name" required placeholder="e.g. Md. Rahim"
                      className="w-full bg-gray-50 border border-gray-200 rounded-xl px-4 py-3 text-gray-900 placeholder-gray-400 focus:outline-none focus:border-primary focus:ring-2 focus:ring-primary/10 transition-all" />
                  </div>
                  <div>
                    <label className="block text-sm text-gray-700 mb-1.5 font-medium">Email *</label>
                    <input type="email" name="email" required placeholder="your@email.com"
                      className="w-full bg-gray-50 border border-gray-200 rounded-xl px-4 py-3 text-gray-900 placeholder-gray-400 focus:outline-none focus:border-primary focus:ring-2 focus:ring-primary/10 transition-all" />
                  </div>
                </div>
                <div className="grid sm:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm text-gray-700 mb-1.5 font-medium">Phone</label>
                    <input type="tel" name="phone" placeholder="01604-809110"
                      className="w-full bg-gray-50 border border-gray-200 rounded-xl px-4 py-3 text-gray-900 placeholder-gray-400 focus:outline-none focus:border-primary focus:ring-2 focus:ring-primary/10 transition-all" />
                  </div>
                  <div>
                    <label className="block text-sm text-gray-700 mb-1.5 font-medium">Website</label>
                    <input type="url" name="website" placeholder="https://yourwebsite.com"
                      className="w-full bg-gray-50 border border-gray-200 rounded-xl px-4 py-3 text-gray-900 placeholder-gray-400 focus:outline-none focus:border-primary focus:ring-2 focus:ring-primary/10 transition-all" />
                  </div>
                </div>
                <div>
                  <label className="block text-sm text-gray-700 mb-1.5 font-medium">Your Project *</label>
                  <textarea name="message" required rows="4" placeholder="Tell me about your business and SEO goals..."
                    className="w-full bg-gray-50 border border-gray-200 rounded-xl px-4 py-3 text-gray-900 placeholder-gray-400 focus:outline-none focus:border-primary focus:ring-2 focus:ring-primary/10 transition-all resize-none"></textarea>
                </div>
                {/* WhatsApp Option */}
                <div className="relative my-2">
                  <div className="absolute inset-0 flex items-center"><div className="w-full border-t border-gray-200"></div></div>
                  <div className="relative flex justify-center text-xs"><span className="bg-white px-2 text-gray-500">OR</span></div>
                </div>
                <a href="https://wa.me/8801604809110?text=Hi%20Kanok%20Miah!%20I%20need%20SEO%20help%20for%20my%20business." target="_blank"
                  className="flex items-center justify-center gap-2 w-full bg-green-500 hover:bg-green-600 text-white font-semibold py-3 rounded-xl transition-all">
                  💬 Chat on WhatsApp <span className="text-white">01604809110</span>
                </a>
                <p className="text-gray-500 text-xs text-center">📧 Results sent to <strong>mdkanokmiah101@gmail.com</strong></p>
                <button type="submit" disabled={submitting}
                  className="w-full bg-primary hover:bg-primary-dark disabled:bg-primary/50 text-white font-bold py-3.5 px-6 rounded-xl hover:shadow-lg hover:shadow-primary/25 transition-all text-lg">
                  {submitting ? "Sending..." : "Get Free SEO Audit →"}
                </button>
                {submitted && (
                  <div className="bg-green-50 border border-green-200 text-green-700 rounded-xl px-5 py-3 text-sm text-center font-medium">
                    ✅ Thank you! Your message has been sent. I'll get back to you within 24 hours.
                  </div>
                )}
                <p className="text-gray-500 text-xs text-center">🔒 Your information is safe. No spam, ever.</p>
              </form>
            </div>

            {/* Contact Info Cards */}
            <div className="space-y-5">
              <div className="bg-white border border-gray-200 rounded-2xl p-7 shadow-sm hover:shadow-md transition-all flex items-start gap-4">
                <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center text-xl shrink-0">📞</div>
                <div>
                  <h3 className="font-bold text-gray-900 mb-1">Call Me Directly</h3>
                  <p className="text-gray-500 text-sm mb-1">Speak with Kanok Miah personally:</p>
                  <a href="tel:+880****9110" className="text-xl font-extrabold text-primary hover:text-primary-dark">+880 1604-809110</a>
                </div>
              </div>
              <div className="bg-white border border-gray-200 rounded-2xl p-7 shadow-sm hover:shadow-md transition-all flex items-start gap-4">
                <div className="w-12 h-12 rounded-xl bg-emerald-50 flex items-center justify-center text-xl shrink-0">💬</div>
                <div>
                  <h3 className="font-bold text-gray-900 mb-1">WhatsApp</h3>
                  <p className="text-gray-500 text-sm mb-2">Quickest response on WhatsApp:</p>
                  <a href="https://wa.me/8801604809110?text=Hi%20Kanok%20Miah!%20I%20need%20SEO%20help."
                    target="_blank" rel="noopener noreferrer"
                    className="inline-flex items-center gap-2 bg-emerald-50 border border-emerald-200 text-emerald-700 px-5 py-2.5 rounded-xl font-semibold hover:bg-emerald-100 transition-all text-sm">
                    💬 Chat on WhatsApp <span className="text-xs text-gray-400">(Fastest Response)</span>
                  </a>
                </div>
              </div>
              <div className="bg-white border border-gray-200 rounded-2xl p-7 shadow-sm hover:shadow-md transition-all flex items-start gap-4">
                <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center text-xl shrink-0">📍</div>
                <div>
                  <h3 className="font-bold text-gray-900 mb-1">Other Ways to Reach</h3>
                  <div className="space-y-2 text-sm">
                    <div className="flex items-center gap-2">
                      <span>📧</span>
                      <a href="mailto:mdkanokmiah232@gmail.com" className="text-gray-600 hover:text-primary">mdkanokmiah232@gmail.com</a>
                    </div>
                    <div className="flex items-center gap-2">
                      <span>🌐</span>
                      <a href="https://kanokmiah.com" target="_blank" rel="noopener noreferrer" className="text-gray-600 hover:text-primary">kanokmiah.com</a>
                    </div>
                    <div className="flex items-center gap-2">
                      <span>📍</span>
                      <span className="text-gray-600">Dhaka, Bangladesh</span>
                    </div>
                  </div>
                </div>
              </div>
              <div className="bg-gradient-to-r from-primary to-primary-dark rounded-2xl p-6 text-center shadow-md">
                <div className="text-3xl mb-2">⭐</div>
                <p className="text-white text-lg font-bold">Free SEO Audit — Worth BDT 5,000</p>
                <p className="text-white/70 text-sm mt-1">Complete analysis of your website. No commitment required.</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ===== FOOTER ===== */}
      <Footer />

    </div>
  );
}