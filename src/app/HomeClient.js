"use client";
import { useState } from "react";
import Link from "next/link";
import Footer from "@/components/Footer";
import { FAQSchema } from "@/components/Schema";

export default function HomeClient() {
  const [menuOpen, setMenuOpen] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [submitted, setSubmitted] = useState(false);

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
    { name: "Industries", path: "/industries" },
    { name: "Blog", path: "/blog" },
    { name: "About", path: "/about" },
    { name: "Contact", path: "/contact" }
  ];

  const faqs = [
    { question: "How do I rank my business on Google Maps in Dhaka?", answer: "To rank your business on Google Maps in Dhaka, start by claiming and verifying your Google Business Profile with accurate NAP (Name, Address, Phone). Choose the most specific category for your business, add 20+ high-quality photos, collect genuine customer reviews, and post weekly updates. I also recommend building local citations on Bangladeshi directories like BD Yellow Pages and BdTradeInfo. Most Dhaka businesses see improved Google Maps visibility within 4-6 weeks of proper optimization." },
    { question: "What is the best SEO strategy for a new website in Bangladesh?", answer: "For new websites in Bangladesh, the best strategy starts with technical SEO — ensure fast loading speeds, mobile responsiveness, and proper crawl setup. Then focus on keyword research targeting both Bengali and English search terms that your local customers use. Create high-quality content around these keywords, build a Google Business Profile, and start earning backlinks from Bangladeshi news sites and directories. Patience is key — most new sites take 3-6 months to see meaningful ranking improvements on Google Bangladesh." },
    { question: "How long does SEO take to show results?", answer: "SEO typically takes 3-6 months to show meaningful results for most businesses in Bangladesh. However, you may start seeing initial improvements in rankings and traffic within 4-6 weeks for low-competition keywords. Factors that influence the timeline include your website's current state, competition level in your industry, keyword difficulty, content quality, and the aggressiveness of link building efforts. I set realistic expectations and provide monthly progress reports so you can see incremental improvements every step of the way." },
    { question: "How much does SEO cost for small businesses?", answer: "SEO pricing for small businesses in Bangladesh varies based on competition and scope. Monthly retainers typically range from BDT 15,000 to BDT 50,000. A BDT 15,000-20,000 plan usually includes local SEO (Google Business Profile optimization, citation building) and basic on-page SEO. More comprehensive packages (BDT 30,000-50,000) include technical SEO, link building, content creation, and detailed monthly reporting. I offer a free initial audit to recommend the right plan for your budget and goals." },
    { question: "What is the difference between GEO and traditional SEO?", answer: "GEO (Generative Engine Optimization) optimizes your content for AI-powered search engines like ChatGPT, Google AI Overviews, Gemini, and Perplexity. Traditional SEO focuses on keyword rankings and backlinks for Google's blue-link search results. GEO uses entity-based content, authoritative citations, and structured data to help AI models accurately extract and cite your information. For Bangladeshi businesses, GEO is emerging as a crucial forward-looking strategy — those who optimize for AI search now will have a significant competitive advantage as AI adoption accelerates." },
    { question: "Can you help my Daraz store rank higher?", answer: "Absolutely. I optimize Daraz seller pages for both Daraz internal search and Google organic search. This includes optimizing product titles with high-volume keywords in Bengali and English, writing detailed unique product descriptions, optimizing images with descriptive alt text, and encouraging product reviews. I also work on off-page signals like backlinks to your Daraz store. Most Daraz sellers see significant ranking improvements and 50-100% organic traffic growth within 3 months of implementing these strategies." },
  ];

  return (
    <div className="min-h-screen bg-white">
      {FAQSchema({ faqs })}

      {/* ===== NAVBAR ===== */}
      <nav className="fixed top-0 w-full bg-white/90 backdrop-blur-xl border-b border-gray-100 z-50">
        <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
          <Link href="/" className="text-xl font-extrabold tracking-tight">
            <span className="text-primary">Md Kanok Miah</span>
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
              <span className="text-primary">Best SEO Expert</span>
              <br />
              <span className="text-gray-900 whitespace-nowrap">in Dhaka, Bangladesh</span>
            </h1>
            <p className="text-lg text-gray-600 mb-8 leading-relaxed">
              Md Kanok Miah is the <strong className="text-gray-900">best SEO expert in Dhaka, Bangladesh</strong> — serving <strong className="text-gray-900">Mirpur, Gulshan, Banani, Uttara, Dhanmondi</strong> and all across the country.
              With <strong className="text-gray-900">6+ years</strong> of experience, I help local businesses rank higher on Google,
              generate qualified leads, and scale revenue — with proven strategies that work.
            </p>
            <div className="flex flex-wrap gap-3 mb-8">
              <span className="inline-flex items-center gap-1.5 bg-green-50 border border-green-200 text-green-700 text-xs font-semibold px-4 py-2 rounded-full">
                ✅ Google Business Profile verified
              </span>
              <span className="inline-flex items-center gap-1.5 bg-amber-50 border border-amber-200 text-amber-700 text-xs font-semibold px-4 py-2 rounded-full">
                ⭐ 108+ Google reviews, 5.0 stars
              </span>
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
                <div><div className="text-sm font-bold text-gray-900">6+ Years</div><div className="text-xs text-gray-500">Experience</div></div>
              </div>
              <div className="flex items-center gap-2 bg-gray-50 border border-gray-100 rounded-xl px-4 py-2.5">
                <span className="text-2xl">📈</span>
                <div><div className="text-sm font-bold text-gray-900">350+</div><div className="text-xs text-gray-500">Projects</div></div>
              </div>
              <div className="flex items-center gap-2 bg-gray-50 border border-gray-100 rounded-xl px-4 py-2.5">
                <span className="text-2xl">⭐</span>
                <div><div className="text-sm font-bold text-gray-900">4.9/5</div><div className="text-xs text-gray-500">Rating</div></div>
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
                <p className="text-[11px] text-gray-400 text-center">📧 We'll send your report to: <strong>mdkanokmiah101@gmail.com</strong></p>
                <button type="submit" disabled={submitting}
                  className="w-full bg-primary hover:bg-primary-dark text-white font-bold py-3.5 rounded-xl transition-all hover:shadow-lg hover:shadow-primary/25 disabled:opacity-50">
                  {submitting ? "Sending..." : submitted ? "✅ Sent! I'll WhatsApp you shortly" : "🔍 Get My Free Audit"}
                </button>
              </form>
              {/* WhatsApp Option Inside Form */}
              <div className="relative my-2">
                <div className="absolute inset-0 flex items-center"><div className="w-full border-t border-gray-200"></div></div>
                <div className="relative flex justify-center text-xs"><span className="bg-white px-2 text-gray-400">OR</span></div>
              </div>
              <a href="https://wa.me/8801604809110?text=Hi%20Kanok%20Miah!%20I%20need%20SEO%20help%20for%20my%20business." target="_blank"
                className="flex items-center justify-center gap-2 w-full bg-green-500 hover:bg-green-600 text-white font-semibold py-2.5 rounded-xl transition-all text-sm">
                💬 Chat on WhatsApp <span className="text-green-100">01604809110</span>
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* ===== STATS BAND ===== */}
      <section className="relative py-14 bg-gradient-to-r from-primary to-primary-dark overflow-hidden">
        <div className="relative max-w-6xl mx-auto px-4 grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
          {[
            { num: "350+", label: "Projects Done" },
            { num: "50+", label: "Happy Clients" },
            { num: "95%", label: "Client Retention" },
            { num: "6+", label: "Years Experience" },
          ].map((stat, i) => (
            <div key={i} className="py-2">
              <div className="text-3xl md:text-5xl font-extrabold text-white">{stat.num}</div>
              <div className="text-primary/70 text-xs md:text-sm mt-1 font-medium uppercase tracking-wider">{stat.label}</div>
            </div>
          ))}
        </div>
      </section>

      {/* ===== SERVICES ===== */}
      <section id="services" className="py-24 px-4 bg-gray-50/80">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <span className="text-primary text-sm font-semibold tracking-[0.2em] uppercase">What We Do</span>
            <h2 className="text-3xl md:text-5xl font-extrabold mt-4 mb-4 text-gray-900">SEO Services for <span className="text-primary">Bangladesh</span> — Local & Technical SEO</h2>
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
                <p className="text-gray-500 text-sm leading-relaxed">{s.desc}</p>
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
                <p className="text-gray-500 text-sm leading-relaxed">{ind.desc}</p>
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
            <h2 className="text-3xl md:text-5xl font-extrabold mt-4 mb-4 text-gray-900">Why <span className="text-primary">Md Kanok Miah</span>?</h2>
            <p className="text-gray-500 max-w-2xl mx-auto text-lg">6+ years mastering SEO for the Bangladesh market. Here&apos;s what sets me apart.</p>
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
                  <p className="text-gray-500 text-sm leading-relaxed">{a.desc}</p>
                </div>
              </div>
            ))}
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
                  <p className="text-gray-500 text-sm leading-relaxed">{p.desc}</p>
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
          <p className="text-primary/80 mb-10 text-lg max-w-xl mx-auto">
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
                <input type="hidden" name="_subject" value="New SEO Lead from Md Kanok Miah Website!" />
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
                  <div className="relative flex justify-center text-xs"><span className="bg-white px-2 text-gray-400">OR</span></div>
                </div>
                <a href="https://wa.me/8801604809110?text=Hi%20Kanok%20Miah!%20I%20need%20SEO%20help%20for%20my%20business." target="_blank"
                  className="flex items-center justify-center gap-2 w-full bg-green-500 hover:bg-green-600 text-white font-semibold py-3 rounded-xl transition-all">
                  💬 Chat on WhatsApp <span className="text-green-100">01604809110</span>
                </a>
                <p className="text-xs text-gray-400 text-center">📧 Results sent to <strong>mdkanokmiah101@gmail.com</strong></p>
                <button type="submit" disabled={submitting}
                  className="w-full bg-primary hover:bg-primary-dark disabled:bg-primary/50 text-white font-bold py-3.5 px-6 rounded-xl hover:shadow-lg hover:shadow-primary/25 transition-all text-lg">
                  {submitting ? "Sending..." : "Get Free SEO Audit →"}
                </button>
                {submitted && (
                  <div className="bg-green-50 border border-green-200 text-green-700 rounded-xl px-5 py-3 text-sm text-center font-medium">
                    ✅ Thank you! Your message has been sent. I'll get back to you within 24 hours.
                  </div>
                )}
                <p className="text-xs text-gray-400 text-center">🔒 Your information is safe. No spam, ever.</p>
              </form>
            </div>

            {/* Contact Info Cards */}
            <div className="space-y-5">
              <div className="bg-white border border-gray-200 rounded-2xl p-7 shadow-sm hover:shadow-md transition-all flex items-start gap-4">
                <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center text-xl shrink-0">📞</div>
                <div>
                  <h3 className="font-bold text-gray-900 mb-1">Call Me Directly</h3>
                  <p className="text-gray-500 text-sm mb-1">Speak with Md Kanok Miah personally:</p>
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
                <p className="text-primary/70 text-sm mt-1">Complete analysis of your website. No commitment required.</p>
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