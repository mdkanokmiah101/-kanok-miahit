"use client";
import { useState } from "react";

export default function Home() {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <div className="min-h-screen bg-[#0a0a0f] text-white">

      {/* === NAVBAR === */}
      <nav className="fixed top-0 w-full bg-[#0a0a0f]/90 backdrop-blur-xl border-b border-white/5 z-50">
        <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
          <a href="#" className="text-xl font-extrabold tracking-tight">
            <span className="bg-gradient-to-r from-cyan-400 to-emerald-400 bg-clip-text text-transparent">Kanok Miah</span>
            <span className="text-amber-400">IT</span>
          </a>
          <div className="hidden md:flex gap-8 text-sm font-medium text-gray-400">
            {["Services", "Industries", "Blog", "About", "Contact"].map(item => (
              <a key={item} href={`#${item.toLowerCase()}`} className="hover:text-cyan-400 transition-colors">{item}</a>
            ))}
          </div>
          <a href="#contact" className="hidden md:inline-block bg-gradient-to-r from-cyan-500 to-emerald-500 text-white text-sm font-bold px-5 py-2 rounded-full hover:shadow-lg hover:shadow-cyan-500/25 transition-all">Free Audit</a>
          <button onClick={() => setMenuOpen(!menuOpen)} className="md:hidden text-2xl text-gray-400">☰</button>
        </div>
        {menuOpen && (
          <div className="md:hidden bg-[#0a0a0f] border-b border-white/5 px-4 pb-4 flex flex-col gap-3 text-sm font-medium text-gray-400">
            <a href="#services" onClick={() => setMenuOpen(false)} className="hover:text-cyan-400">Services</a>
            <a href="/industries" onClick={() => setMenuOpen(false)} className="hover:text-cyan-400">Industries</a>
            <a href="/blog" onClick={() => setMenuOpen(false)} className="hover:text-cyan-400">Blog</a>
            <a href="/about" onClick={() => setMenuOpen(false)} className="hover:text-cyan-400">About</a>
            <a href="#contact" onClick={() => setMenuOpen(false)} className="hover:text-cyan-400">Contact</a>
          </div>
        )}
      </nav>

      {/* === FLOATING WHATSAPP BUTTON === */}
      <a
        href="https://wa.me/8801712883101?text=Hi%20Kanok%20MiahIT!%20I%20need%20SEO%20help%20for%20my%20business."
        target="_blank"
        rel="noopener noreferrer"
        className="fixed bottom-6 right-6 z-50 w-14 h-14 bg-emerald-500 rounded-full flex items-center justify-center text-2xl shadow-lg hover:bg-emerald-400 hover:scale-110 hover:shadow-emerald-500/40 transition-all animate-bounce"
        aria-label="Chat on WhatsApp"
      >
        💬
      </a>

      {/* === HERO — BIG & DRAMATIC === */}
      <section className="relative min-h-screen flex items-center justify-center px-4 overflow-hidden">
        {/* Animated gradient orbs */}
        <div className="absolute top-1/4 -left-32 w-96 h-96 bg-cyan-500/20 rounded-full blur-3xl animate-pulse" />
        <div className="absolute bottom-1/4 -right-32 w-96 h-96 bg-emerald-500/20 rounded-full blur-3xl animate-pulse delay-1000" />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-violet-500/10 rounded-full blur-3xl" />

        <div className="relative max-w-4xl mx-auto text-center">
          <div className="inline-flex items-center gap-2 bg-white/5 border border-white/10 text-cyan-300 text-xs font-semibold px-5 py-2 rounded-full mb-8 backdrop-blur-sm">
            <span className="w-2 h-2 bg-emerald-400 rounded-full animate-pulse" />
            #1 SEO Agency in Bangladesh
          </div>
          <h1 className="text-5xl md:text-7xl lg:text-8xl font-extrabold tracking-tight leading-[1.05] mb-6">
            <span className="bg-gradient-to-r from-cyan-300 via-emerald-300 to-amber-200 bg-clip-text text-transparent">
              Rank Higher.
            </span>
            <br />
            <span className="text-white">Grow Faster.</span>
            <br />
            <span className="text-white/70">Dominate Search.</span>
          </h1>
          <p className="text-lg md:text-xl text-gray-400 max-w-2xl mx-auto mb-10 leading-relaxed">
            Kanok MiahIT is a <span className="text-white font-semibold">Bangladesh-focused</span> SEO agency that gets local businesses 
            found on Google, generates qualified leads, and scales revenue — with proven strategies that work.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <a href="#contact" className="group relative inline-flex items-center gap-2 bg-gradient-to-r from-cyan-500 to-emerald-500 text-white px-8 py-4 rounded-xl font-bold text-lg transition-all hover:shadow-xl hover:shadow-cyan-500/30 hover:-translate-y-0.5">
              Get Free SEO Audit
              <span className="group-hover:translate-x-1 transition-transform">→</span>
            </a>
            <a href="#services" className="inline-flex items-center gap-2 border border-white/20 text-white/80 px-8 py-4 rounded-xl font-semibold text-lg hover:bg-white/5 hover:border-white/40 transition-all">
              View Services
            </a>
          </div>
          <div className="mt-16 flex flex-wrap items-center justify-center gap-6 md:gap-10 text-sm text-gray-500">
            <span className="flex items-center gap-2"><span className="w-5 h-5 rounded-full bg-cyan-500/20 flex items-center justify-center text-xs text-cyan-400">🏆</span> 6+ Years Experience</span>
            <span className="flex items-center gap-2"><span className="w-5 h-5 rounded-full bg-emerald-500/20 flex items-center justify-center text-xs text-emerald-400">📈</span> 350+ Projects</span>
            <span className="flex items-center gap-2"><span className="w-5 h-5 rounded-full bg-amber-500/20 flex items-center justify-center text-xs text-amber-400">🇧🇩</span> Bangladesh Focused</span>
          </div>
        </div>
      </section>

      {/* === STATS BAND === */}
      <section className="relative py-16 border-y border-white/5">
        <div className="absolute inset-0 bg-gradient-to-r from-cyan-500/5 via-transparent to-emerald-500/5" />
        <div className="relative max-w-5xl mx-auto px-4 grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
          {[
            { num: "350+", label: "Projects Done", color: "from-cyan-400 to-cyan-600" },
            { num: "50+", label: "Happy Clients", color: "from-emerald-400 to-emerald-600" },
            { num: "95%", label: "Client Retention", color: "from-amber-400 to-amber-600" },
            { num: "6+", label: "Years Exp.", color: "from-violet-400 to-violet-600" },
          ].map((stat, i) => (
            <div key={i}>
              <div className={`text-4xl md:text-5xl font-extrabold bg-gradient-to-b ${stat.color} bg-clip-text text-transparent`}>{stat.num}</div>
              <div className="text-gray-500 text-sm mt-1">{stat.label}</div>
            </div>
          ))}
        </div>
      </section>

      {/* === SERVICES === */}
      <section id="services" className="relative py-24 px-4">
        <div className="absolute top-0 right-0 w-72 h-72 bg-cyan-500/10 rounded-full blur-3xl" />
        <div className="relative max-w-5xl mx-auto">
          <div className="text-center mb-16">
            <span className="text-cyan-400 text-sm font-semibold tracking-widest uppercase">What We Do</span>
            <h2 className="text-3xl md:text-5xl font-extrabold mt-3 mb-4">SEO Services for Bangladesh</h2>
            <p className="text-gray-400 max-w-xl mx-auto">Complete SEO solutions tailored for Bangladesh — from local Dhaka SEO to international optimization.</p>
          </div>
          <div className="grid md:grid-cols-3 gap-5">
            {[
              { icon: "🔍", title: "Local SEO", desc: "Rank your business on Google Maps in Dhaka, Chittagong, Sylhet and beyond. GBP optimization, local citations, near-me SEO.", gradient: "from-cyan-500/20 to-cyan-600/5" },
              { icon: "📄", title: "On-Page SEO", desc: "Keyword-optimized content, meta tags, header structure, internal linking, and schema markup for Bangladesh audiences.", gradient: "from-emerald-500/20 to-emerald-600/5" },
              { icon: "🔗", title: "Link Building", desc: "Quality backlinks from Bangladeshi and international directories, guest posts, and niche-relevant websites that drive authority.", gradient: "from-amber-500/20 to-amber-600/5" },
              { icon: "📊", title: "Technical SEO", desc: "Site speed optimization, Core Web Vitals, mobile-first indexing, crawl budget fixes, and structured data for Google.", gradient: "from-violet-500/20 to-violet-600/5" },
              { icon: "🤖", title: "GEO / AI Search", desc: "Optimize for ChatGPT, Gemini, Perplexity, and Google AI Overviews. Entity-first SEO for the AI-powered search era.", gradient: "from-cyan-500/20 to-emerald-600/5" },
              { icon: "🛒", title: "E-commerce SEO", desc: "Shopify, Daraz, and WooCommerce SEO. Product page optimization, category structure, and conversion-focused SEO strategy.", gradient: "from-amber-500/20 to-violet-600/5" },
            ].map((s, i) => (
              <div key={i} className="group relative bg-white/[0.03] border border-white/10 rounded-2xl p-7 hover:bg-white/[0.06] hover:border-white/20 transition-all hover:-translate-y-1">
                <div className={`absolute inset-0 bg-gradient-to-br ${s.gradient} rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity`} />
                <div className="relative">
                  <div className="text-3xl mb-4">{s.icon}</div>
                  <h3 className="font-bold text-lg mb-2 text-white">{s.title}</h3>
                  <p className="text-gray-400 text-sm leading-relaxed">{s.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* === INDUSTRIES WE SERVE === */}
      <section id="industries" className="relative py-24 px-4">
        <div className="absolute top-0 right-0 w-72 h-72 bg-emerald-500/10 rounded-full blur-3xl" />
        <div className="relative max-w-5xl mx-auto">
          <div className="text-center mb-16">
            <span className="text-cyan-400 text-sm font-semibold tracking-widest uppercase">Industries We Serve</span>
            <h2 className="text-3xl md:text-5xl font-extrabold mt-3 mb-4">Industry-Specific SEO Solutions</h2>
            <p className="text-gray-400 max-w-xl mx-auto">Every industry has unique SEO challenges. We tailor strategies that work for your specific Bangladesh market sector.</p>
          </div>
          <div className="grid md:grid-cols-3 gap-4">
            {[
              { icon: "👕", title: "Garments & Textile", slug: "garments-textile", desc: "RMG exporters, textile mills, apparel manufacturers — B2B SEO for international buyers" },
              { icon: "🛒", title: "E-commerce", slug: "ecommerce", desc: "Daraz sellers, Shopify stores, WooCommerce — product & category SEO for higher sales" },
              { icon: "📱", title: "SMM Panel", slug: "smm-panel", desc: "Social media agencies & SMM panels — local SEO to attract Dhaka businesses" },
              { icon: "🏢", title: "Real Estate", slug: "real-estate", desc: "Developers, agents, housing — rank for location-based property keywords" },
              { icon: "🧹", title: "Cleaning Services", slug: "cleaning", desc: "Office & home cleaning companies — dominate Google Maps in your area" },
              { icon: "💆", title: "Spa & Salon", slug: "spa-salon", desc: "Beauty parlours, spas, salons — near-me SEO for more foot traffic" },
              { icon: "🏥", title: "Medical & Healthcare", slug: "medical", desc: "Hospitals, clinics, diagnostics — E-E-A-T optimized healthcare SEO" },
              { icon: "🎓", title: "Education", slug: "education", desc: "Universities, coaching, training institutes — student inquiry generation" },
              { icon: "🍽️", title: "Food & Restaurant", slug: "food-restaurant", desc: "Restaurants, cafes, food delivery — Google Maps dominance for dining" },
            ].map((ind, i) => (
              <a key={i} href={`/industries/${ind.slug}`} className="group bg-white/[0.03] border border-white/10 rounded-2xl p-6 hover:bg-white/[0.06] hover:border-cyan-500/30 hover:-translate-y-1 transition-all">
                <div className="text-3xl mb-3">{ind.icon}</div>
                <h3 className="font-bold text-white mb-1.5 group-hover:text-cyan-300 transition-colors">{ind.title}</h3>
                <p className="text-gray-500 text-sm leading-relaxed">{ind.desc}</p>
                <div className="mt-3 text-cyan-400 text-xs font-semibold opacity-0 group-hover:opacity-100 transition-opacity">Learn More →</div>
              </a>
            ))}
          </div>
          <div className="text-center mt-10">
            <a href="/industries" className="inline-flex items-center gap-2 text-cyan-400 font-semibold hover:text-cyan-300 transition-colors">
              View All Industries →
            </a>
          </div>
        </div>
      </section>

      {/* === ABOUT === */}
      <section id="about" className="relative py-24 px-4">
        <div className="absolute inset-0 bg-gradient-to-b from-white/[0.02] to-transparent" />
        <div className="relative max-w-4xl mx-auto">
          <div className="text-center mb-16">
            <span className="text-cyan-400 text-sm font-semibold tracking-widest uppercase">Why Choose Us</span>
            <h2 className="text-3xl md:text-5xl font-extrabold mt-3 mb-4">Why Kanok MiahIT?</h2>
            <p className="text-gray-400 max-w-xl mx-auto">6+ years mastering SEO for the Bangladesh market. We understand how local businesses rank and grow.</p>
          </div>
          <div className="grid md:grid-cols-2 gap-5">
            {[
              { title: "🇧🇩 Local Market Expertise", desc: "We know Bangladesh search behavior — Bengali + English queries, local intent, Dhaka-centric business patterns inside out.", accent: "cyan" },
              { title: "📈 Data-Driven Approach", desc: "Every strategy is built on keyword research, competitor analysis, and real ranking data — not guesswork or trends.", accent: "emerald" },
              { title: "⚡ Fast, Tangible Results", desc: "We target quick wins (GSC fixes, content gaps, technical issues) while building long-term authority that compounds.", accent: "amber" },
              { title: "🤝 Transparent Reporting", desc: "Monthly reports with real KPIs: rankings, traffic, conversions, ROI. No vanity metrics. No fluff. Just results.", accent: "violet" },
            ].map((a, i) => (
              <div key={i} className="group bg-white/[0.03] border border-white/10 rounded-2xl p-7 hover:bg-white/[0.06] hover:border-white/20 transition-all hover:-translate-y-1">
                <h3 className="font-bold text-lg mb-2 text-white">{a.title}</h3>
                <p className="text-gray-400 text-sm leading-relaxed">{a.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* === PROCESS === */}
      <section id="process" className="relative py-24 px-4">
        <div className="absolute bottom-0 left-0 w-72 h-72 bg-emerald-500/10 rounded-full blur-3xl" />
        <div className="relative max-w-5xl mx-auto">
          <div className="text-center mb-16">
            <span className="text-cyan-400 text-sm font-semibold tracking-widest uppercase">How We Work</span>
            <h2 className="text-3xl md:text-5xl font-extrabold mt-3 mb-4">Our 5-Step Process</h2>
            <p className="text-gray-400 max-w-xl mx-auto">A proven system that delivers measurable SEO results for Bangladeshi businesses.</p>
          </div>
          <div className="relative">
            {/* Connector line */}
            <div className="absolute top-12 left-[10%] right-[10%] h-px bg-gradient-to-r from-cyan-500/40 via-emerald-500/40 to-amber-500/40 hidden md:block" />
            <div className="grid md:grid-cols-5 gap-6">
              {[
                { step: "01", title: "Audit", desc: "Full site analysis — technical, content, backlinks, competitors", color: "from-cyan-400 to-cyan-600" },
                { step: "02", title: "Strategy", desc: "Custom SEO plan with Bangladesh keyword targeting", color: "from-emerald-400 to-emerald-600" },
                { step: "03", title: "Execute", desc: "On-page fixes, content, link building, technical SEO", color: "from-amber-400 to-amber-600" },
                { step: "04", title: "Monitor", desc: "Track rankings, traffic, and conversions weekly", color: "from-violet-400 to-violet-600" },
                { step: "05", title: "Optimize", desc: "Iterate and improve based on real performance data", color: "from-cyan-400 to-emerald-600" },
              ].map((p, i) => (
                <div key={i} className="relative text-center p-4">
                  <div className={`relative z-10 w-14 h-14 mx-auto mb-4 rounded-2xl bg-gradient-to-br ${p.color} flex items-center justify-center font-extrabold text-sm shadow-lg`}>
                    {p.step}
                  </div>
                  <h3 className="font-bold text-white mb-1">{p.title}</h3>
                  <p className="text-gray-500 text-xs leading-relaxed">{p.desc}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* === CTA === */}
      <section className="relative py-24 px-4 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-cyan-600/20 via-emerald-600/20 to-amber-600/20" />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] bg-gradient-to-r from-cyan-500/20 to-emerald-500/20 rounded-full blur-3xl" />
        <div className="relative max-w-2xl mx-auto text-center">
          <h2 className="text-3xl md:text-5xl font-extrabold mb-4">Ready to <span className="bg-gradient-to-r from-cyan-300 to-emerald-300 bg-clip-text text-transparent">Dominate</span> Search?</h2>
          <p className="text-gray-400 mb-10 text-lg">Get a free SEO audit for your Bangladesh business. No commitment, no hidden fees. Just real, actionable insights.</p>
          <a href="#contact" className="group inline-flex items-center gap-2 bg-gradient-to-r from-cyan-500 to-emerald-500 text-white px-10 py-4 rounded-xl font-bold text-lg transition-all hover:shadow-xl hover:shadow-cyan-500/30 hover:-translate-y-0.5">
            Get Your Free Audit
            <span className="group-hover:translate-x-1 transition-transform">→</span>
          </a>
        </div>
      </section>

      {/* === CONTACT — LEAD FORM === */}
      <section id="contact" className="py-24 px-4">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-16">
            <span className="text-cyan-400 text-sm font-semibold tracking-widest uppercase">Get In Touch</span>
            <h2 className="text-3xl md:text-4xl font-extrabold mt-3 mb-4">Contact Kanok MiahIT</h2>
            <p className="text-gray-400 mb-6">Ready to rank? Fill out the form and we'll get back to you within 24 hours.</p>
            <div className="flex flex-wrap items-center justify-center gap-4 text-sm">
              <a href="tel:+8801712883101" className="inline-flex items-center gap-2 bg-green-500/10 border border-green-500/30 text-green-400 px-5 py-2.5 rounded-full font-semibold hover:bg-green-500/20 transition-all">
                📞 <span className="font-bold">+880 1712-883101</span>
              </a>
              <a href="https://wa.me/8801712883101?text=Hi%20Kanok%20MiahIT!%20I%20need%20SEO%20help%20for%20my%20business." target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-2 bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 px-5 py-2.5 rounded-full font-semibold hover:bg-emerald-500/20 transition-all">
                💬 WhatsApp Us
              </a>
            </div>
          </div>
          <div className="grid md:grid-cols-2 gap-8 items-start">
            {/* Form */}
            <div className="bg-white/[0.03] border border-white/10 rounded-2xl p-8">
              <form
                action="https://formspree.io/f/xvgkrvrz"
                method="POST"
                className="space-y-5"
              >
                <div>
                  <label className="block text-sm text-gray-400 mb-1.5 font-medium">Your Name *</label>
                  <input
                    type="text"
                    name="name"
                    required
                    placeholder="e.g. Md. Rahim"
                    className="w-full bg-white/[0.05] border border-white/10 rounded-xl px-4 py-3 text-white placeholder-gray-600 focus:outline-none focus:border-cyan-500/50 focus:ring-1 focus:ring-cyan-500/20 transition-all"
                  />
                </div>
                <div>
                  <label className="block text-sm text-gray-400 mb-1.5 font-medium">Email Address *</label>
                  <input
                    type="email"
                    name="email"
                    required
                    placeholder="your@email.com"
                    className="w-full bg-white/[0.05] border border-white/10 rounded-xl px-4 py-3 text-white placeholder-gray-600 focus:outline-none focus:border-cyan-500/50 focus:ring-1 focus:ring-cyan-500/20 transition-all"
                  />
                </div>
                <div>
                  <label className="block text-sm text-gray-400 mb-1.5 font-medium">Phone Number</label>
                  <input
                    type="tel"
                    name="phone"
                    placeholder="01712-883101"
                    className="w-full bg-white/[0.05] border border-white/10 rounded-xl px-4 py-3 text-white placeholder-gray-600 focus:outline-none focus:border-cyan-500/50 focus:ring-1 focus:ring-cyan-500/20 transition-all"
                  />
                </div>
                <div>
                  <label className="block text-sm text-gray-400 mb-1.5 font-medium">Your Website</label>
                  <input
                    type="url"
                    name="website"
                    placeholder="https://yourwebsite.com"
                    className="w-full bg-white/[0.05] border border-white/10 rounded-xl px-4 py-3 text-white placeholder-gray-600 focus:outline-none focus:border-cyan-500/50 focus:ring-1 focus:ring-cyan-500/20 transition-all"
                  />
                </div>
                <div>
                  <label className="block text-sm text-gray-400 mb-1.5 font-medium">Tell Us About Your Project *</label>
                  <textarea
                    name="message"
                    required
                    rows="4"
                    placeholder="I need SEO for my e-commerce store in Dhaka..."
                    className="w-full bg-white/[0.05] border border-white/10 rounded-xl px-4 py-3 text-white placeholder-gray-600 focus:outline-none focus:border-cyan-500/50 focus:ring-1 focus:ring-cyan-500/20 transition-all resize-none"
                  ></textarea>
                </div>
                <input type="hidden" name="_subject" value="New SEO Lead from Kanok MiahIT Website!" />
                <input type="text" name="_gotcha" style={{display: "none"}} />
                <button
                  type="submit"
                  className="w-full bg-gradient-to-r from-cyan-500 to-emerald-500 text-white font-bold py-3.5 px-6 rounded-xl hover:shadow-lg hover:shadow-cyan-500/25 hover:-translate-y-0.5 transition-all"
                >
                  Get Free SEO Audit →
                </button>
                <p className="text-xs text-gray-600 text-center">We respect your privacy. No spam, ever.</p>
              </form>
            </div>

            {/* Contact Info */}
            <div className="space-y-6">
              <div className="bg-white/[0.03] border border-white/10 rounded-2xl p-7">
                <h3 className="font-bold text-lg mb-4 text-white">📞 Call Us Directly</h3>
                <p className="text-gray-400 text-sm mb-3">Speak directly with Kanok MiahIT's SEO team:</p>
                <a href="tel:+8801712883101" className="text-2xl font-extrabold bg-gradient-to-r from-cyan-300 to-emerald-300 bg-clip-text text-transparent hover:from-cyan-200 hover:to-emerald-200 transition-all">
                  +880 1712-883101
                </a>
              </div>

              <div className="bg-white/[0.03] border border-white/10 rounded-2xl p-7">
                <h3 className="font-bold text-lg mb-4 text-white">💬 WhatsApp</h3>
                <p className="text-gray-400 text-sm mb-3">Quick response on WhatsApp:</p>
                <a href="https://wa.me/8801712883101?text=Hi%20Kanok%20MiahIT!%20I%20need%20SEO%20help." target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-2 bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 px-5 py-3 rounded-xl font-semibold hover:bg-emerald-500/20 transition-all text-sm">
                  💬 Chat on WhatsApp → <span className="text-xs text-gray-500">(Fastest Response)</span>
                </a>
              </div>

              <div className="bg-white/[0.03] border border-white/10 rounded-2xl p-7">
                <h3 className="font-bold text-lg mb-4 text-white">📍 Other Ways to Reach</h3>
                <div className="space-y-3 text-sm">
                  <div className="flex items-center gap-3">
                    <span className="text-xl">📧</span>
                    <a href="mailto:mdkanokmiah232@gmail.com" className="text-gray-300 hover:text-cyan-400 transition-colors">mdkanokmiah232@gmail.com</a>
                  </div>
                  <div className="flex items-center gap-3">
                    <span className="text-xl">🌐</span>
                    <a href="https://kanokmiah.com" target="_blank" rel="noopener noreferrer" className="text-gray-300 hover:text-cyan-400 transition-colors">kanokmiah.com</a>
                  </div>
                  <div className="flex items-center gap-3">
                    <span className="text-xl">📍</span>
                    <span className="text-gray-300">Dhaka, Bangladesh</span>
                  </div>
                </div>
              </div>

              <div className="bg-gradient-to-r from-cyan-600/20 via-emerald-600/20 to-amber-600/20 border border-white/10 rounded-2xl p-6 text-center">
                <p className="text-gray-300 text-sm font-semibold">⭐ Free SEO Audit — Worth BDT 5,000</p>
                <p className="text-gray-500 text-xs mt-1">Get a complete analysis of your website. No commitment required.</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* === FOOTER === */}
      <footer className="py-10 border-t border-white/5 text-center text-sm text-gray-600">
        <div className="max-w-4xl mx-auto px-4">
          <div className="flex flex-wrap justify-center gap-6 mb-4">
            <a href="/" className="hover:text-cyan-400 transition-colors">Home</a>
            <a href="/industries" className="hover:text-cyan-400 transition-colors">Industries</a>
            <a href="/blog" className="hover:text-cyan-400 transition-colors">Blog</a>
            <a href="/about" className="hover:text-cyan-400 transition-colors">About</a>
            <a href="/privacy-policy" className="hover:text-cyan-400 transition-colors">Privacy</a>
            <a href="/terms-of-service" className="hover:text-cyan-400 transition-colors">Terms</a>
          </div>
          <p>© 2026 <span className="bg-gradient-to-r from-cyan-400 to-emerald-400 bg-clip-text text-transparent font-bold">Kanok MiahIT</span> — SEO Agency in Bangladesh. All rights reserved.</p>
          <p className="mt-2 text-xs text-gray-700">🇧🇩 Serving Dhaka, Chittagong, Sylhet & all of Bangladesh</p>
        </div>
      </footer>

    </div>
  );
}
