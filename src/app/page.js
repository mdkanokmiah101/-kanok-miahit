"use client";
import { useState } from "react";

export default function Home() {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <div className="min-h-screen bg-white">

      {/* === NAVBAR === */}
      <nav className="fixed top-0 w-full bg-white/95 backdrop-blur-xl border-b border-gray-100 z-50">
        <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
          <a href="#" className="text-xl font-extrabold tracking-tight">
            <span className="text-primary">Md Kanok Miah</span>
            <span className="text-amber-500">IT</span>
          </a>
          <div className="hidden md:flex gap-8 text-sm font-medium text-gray-600">
            {["Services", "Industries", "Blog", "About", "Contact"].map(item => (
              <a key={item} href={`#${item.toLowerCase()}`} className="hover:text-primary transition-colors">{item}</a>
            ))}
          </div>
          <a href="#contact" className="hidden md:inline-block bg-primary text-white text-sm font-bold px-5 py-2 rounded-full hover:bg-primary-dark hover:shadow-lg hover:shadow-primary/25 transition-all">Free Audit</a>
          <button onClick={() => setMenuOpen(!menuOpen)} className="md:hidden text-2xl text-gray-700">☰</button>
        </div>
        {menuOpen && (
          <div className="md:hidden bg-white border-b border-gray-100 px-4 pb-4 flex flex-col gap-3 text-sm font-medium text-gray-600">
            <a href="#services" onClick={() => setMenuOpen(false)} className="hover:text-primary">Services</a>
            <a href="/industries" onClick={() => setMenuOpen(false)} className="hover:text-primary">Industries</a>
            <a href="/blog" onClick={() => setMenuOpen(false)} className="hover:text-primary">Blog</a>
            <a href="/about" onClick={() => setMenuOpen(false)} className="hover:text-primary">About</a>
            <a href="#contact" onClick={() => setMenuOpen(false)} className="hover:text-primary">Contact</a>
          </div>
        )}
      </nav>

      {/* === FLOATING WHATSAPP === */}
      <a
        href="https://wa.me/8801712883101?text=Hi%20Kanok%20MiahIT!%20I%20need%20SEO%20help%20for%20my%20business."
        target="_blank"
        rel="noopener noreferrer"
        className="fixed bottom-6 right-6 z-50 w-14 h-14 bg-emerald-500 rounded-full flex items-center justify-center text-2xl shadow-lg hover:bg-emerald-400 hover:scale-110 hover:shadow-emerald-500/40 transition-all animate-bounce"
        aria-label="Chat on WhatsApp"
      >💬</a>

      {/* === HERO SECTION === */}
      <section className="relative pt-32 pb-24 px-4 overflow-hidden bg-gradient-to-br from-primary-light via-white to-sky-50">
        <div className="absolute top-20 left-1/4 w-72 h-72 bg-primary/30 rounded-full blur-3xl" />
        <div className="absolute bottom-20 right-1/4 w-96 h-96 bg-cyan-200/20 rounded-full blur-3xl" />
        <div className="relative max-w-6xl mx-auto grid md:grid-cols-2 gap-12 items-center">
          {/* Hero Text */}
          <div>
            <div className="inline-flex items-center gap-2 bg-primary-light border border-primary/20 text-primary-dark text-xs font-semibold px-5 py-2 rounded-full mb-6">
              <span className="w-2 h-2 bg-primary-light0 rounded-full animate-pulse" />
              #1 SEO Agency in Bangladesh
            </div>
            <h1 className="text-4xl md:text-6xl lg:text-7xl font-extrabold tracking-tight leading-[1.1] mb-6">
              <span className="text-primary">Best SEO Agency</span>
              <br />
              <span className="text-gray-900">in Dhaka, Bangladesh</span>
              <br />
              <span className="text-gray-400 text-3xl md:text-4xl font-semibold">Rank Higher. Grow Faster.</span>
            </h1>
            <p className="text-lg text-gray-600 mb-8 leading-relaxed max-w-xl">
              Kanok MiahIT is the <strong className="text-gray-900">best SEO agency in Dhaka, Bangladesh</strong>. 
              We help local businesses rank higher on Google, generate qualified leads, and scale revenue — 
              with proven strategies that work.
            </p>
            <div className="flex flex-col sm:flex-row gap-4">
              <a href="#contact" className="inline-flex items-center gap-2 bg-primary hover:bg-primary-dark text-white px-8 py-4 rounded-xl font-bold text-lg transition-all hover:shadow-xl hover:shadow-primary/30 hover:-translate-y-0.5">
                Get Free SEO Audit
                <span className="group-hover:translate-x-1 transition-transform">→</span>
              </a>
              <a href="#services" className="inline-flex items-center gap-2 border-2 border-gray-200 text-gray-700 px-8 py-4 rounded-xl font-semibold text-lg hover:border-primary/30 hover:text-primary transition-all">
                View Services
              </a>
            </div>
            {/* Trust badges */}
            <div className="mt-12 flex flex-wrap gap-6 text-sm text-gray-500">
              <span className="flex items-center gap-2"><span className="text-primary font-bold">🏆</span> 6+ Years Experience</span>
              <span className="flex items-center gap-2"><span className="text-green-600 font-bold">📈</span> 350+ Projects</span>
              <span className="flex items-center gap-2"><span className="text-amber-600 font-bold">🇧🇩</span> Bangladesh Focused</span>
            </div>
          </div>
          {/* Hero Image Placeholder */}
          <div className="relative hidden md:block">
            <div className="relative bg-gradient-to-br from-primary to-primary-dark rounded-3xl p-1 shadow-2xl">
              <div className="bg-white rounded-[22px] p-8">
                <div className="grid grid-cols-2 gap-4">
                  {["🔍", "📈", "🎯", "🚀"].map((emoji, i) => (
                    <div key={i} className="bg-primary-light rounded-2xl p-6 text-center">
                      <div className="text-4xl mb-2">{emoji}</div>
                      <div className="text-xs text-gray-500 font-medium">
                        {["SEO Audit", "Rankings", "Traffic", "Growth"][i]}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
            {/* Floating badge */}
            <div className="absolute -bottom-4 -left-4 bg-white rounded-2xl shadow-lg px-6 py-4 border border-gray-100">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center text-green-600 font-bold">⭐</div>
                <div>
                  <div className="text-sm font-bold text-gray-900">4.7/5 Rating</div>
                  <div className="text-xs text-gray-500">From 78K+ clients</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* === STATS BAND === */}
      <section className="py-16 bg-gradient-to-r from-primary to-primary-dark">
        <div className="max-w-5xl mx-auto px-4 grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
          {[
            { num: "350+", label: "Projects Done" },
            { num: "50+", label: "Happy Clients" },
            { num: "95%", label: "Client Retention" },
            { num: "6+", label: "Years Exp." },
          ].map((stat, i) => (
            <div key={i}>
              <div className="text-4xl md:text-5xl font-extrabold text-white">{stat.num}</div>
              <div className="text-primary/80 text-sm mt-1">{stat.label}</div>
            </div>
          ))}
        </div>
      </section>

      {/* === SERVICES === */}
      <section id="services" className="py-24 px-4 bg-gray-50">
        <div className="max-w-5xl mx-auto">
          <div className="text-center mb-16">
            <span className="text-primary text-sm font-semibold tracking-widest uppercase">What We Do</span>
            <h2 className="text-3xl md:text-5xl font-extrabold mt-3 mb-4 text-gray-900">SEO Services for Bangladesh</h2>
            <p className="text-gray-500 max-w-xl mx-auto">Complete SEO solutions tailored for Bangladesh — from local Dhaka SEO to international optimization.</p>
          </div>
          <div className="grid md:grid-cols-3 gap-6">
            {[
              { icon: "🔍", title: "Local SEO", desc: "Rank your business on Google Maps in Dhaka, Chittagong, Sylhet and beyond. GBP optimization, local citations, near-me SEO.", color: "blue" },
              { icon: "📄", title: "On-Page SEO", desc: "Keyword-optimized content, meta tags, header structure, internal linking, and schema markup for Bangladesh audiences.", color: "green" },
              { icon: "🔗", title: "Link Building", desc: "Quality backlinks from Bangladeshi and international directories, guest posts, and niche-relevant websites that drive authority.", color: "amber" },
              { icon: "📊", title: "Technical SEO", desc: "Site speed optimization, Core Web Vitals, mobile-first indexing, crawl budget fixes, and structured data for Google.", color: "purple" },
              { icon: "🤖", title: "GEO / AI Search", desc: "Optimize for ChatGPT, Gemini, Perplexity, and Google AI Overviews. Entity-first SEO for the AI-powered search era.", color: "teal" },
              { icon: "🛒", title: "E-commerce SEO", desc: "Shopify, Daraz, and WooCommerce SEO. Product page optimization, category structure, and conversion-focused SEO strategy.", color: "orange" },
            ].map((s, i) => (
              <div key={i} className="bg-white rounded-2xl p-7 border border-gray-100 hover:border-primary/20 hover:shadow-lg hover:-translate-y-1 transition-all">
                <div className={`w-14 h-14 rounded-xl bg-${s.color}-100 flex items-center justify-center text-2xl mb-5`}>{s.icon}</div>
                <h3 className="font-bold text-lg mb-2 text-gray-900">{s.title}</h3>
                <p className="text-gray-500 text-sm leading-relaxed">{s.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* === INDUSTRIES === */}
      <section id="industries" className="py-24 px-4">
        <div className="max-w-5xl mx-auto">
          <div className="text-center mb-16">
            <span className="text-primary text-sm font-semibold tracking-widest uppercase">Industries We Serve</span>
            <h2 className="text-3xl md:text-5xl font-extrabold mt-3 mb-4 text-gray-900">Industry-Specific SEO Solutions</h2>
            <p className="text-gray-500 max-w-xl mx-auto">Every industry has unique SEO challenges. We tailor strategies that work for your specific Bangladesh market sector.</p>
          </div>
          <div className="grid md:grid-cols-3 gap-4">
            {[
              { icon: "👕", title: "Garments & Textile", desc: "RMG exporters, textile mills — B2B SEO for international buyers", slug: "garments-textile" },
              { icon: "🛒", title: "E-commerce", desc: "Daraz sellers, Shopify stores — product SEO for higher sales", slug: "ecommerce" },
              { icon: "📱", title: "SMM Panel", desc: "Social media agencies — local SEO to attract Dhaka businesses", slug: "smm-panel" },
              { icon: "🏢", title: "Real Estate", desc: "Developers, agents — rank for property keywords", slug: "real-estate" },
              { icon: "🧹", title: "Cleaning Services", desc: "Office & home cleaning — dominate Google Maps", slug: "cleaning" },
              { icon: "💆", title: "Spa & Salon", desc: "Beauty parlours — near-me SEO for foot traffic", slug: "spa-salon" },
              { icon: "🏥", title: "Medical & Healthcare", desc: "Hospitals, clinics — E-E-A-T healthcare SEO", slug: "medical" },
              { icon: "🎓", title: "Education", desc: "Universities, coaching — student inquiry gen", slug: "education" },
              { icon: "🍽️", title: "Food & Restaurant", desc: "Restaurants — Maps dominance for dining", slug: "food-restaurant" },
            ].map((ind, i) => (
              <a key={i} href={`/industries/${ind.slug}`}
                className="bg-gray-50 rounded-2xl p-6 border border-gray-100 hover:border-primary/20 hover:bg-primary-light hover:-translate-y-1 transition-all group">
                <div className="text-3xl mb-3">{ind.icon}</div>
                <h3 className="font-bold text-gray-900 mb-1.5 group-hover:text-primary transition-colors">{ind.title}</h3>
                <p className="text-gray-500 text-sm leading-relaxed">{ind.desc}</p>
                <div className="mt-3 text-primary text-xs font-semibold opacity-0 group-hover:opacity-100 transition-opacity">Learn More →</div>
              </a>
            ))}
          </div>
          <div className="text-center mt-10">
            <a href="/industries" className="inline-flex items-center gap-2 text-primary font-semibold hover:text-primary-dark">View All Industries →</a>
          </div>
        </div>
      </section>

      {/* === WHY US === */}
      <section id="about" className="py-24 px-4 bg-gray-50">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-16">
            <span className="text-primary text-sm font-semibold tracking-widest uppercase">Why Choose Us</span>
            <h2 className="text-3xl md:text-5xl font-extrabold mt-3 mb-4 text-gray-900">Why Kanok MiahIT?</h2>
            <p className="text-gray-500 max-w-xl mx-auto">6+ years mastering SEO for the Bangladesh market. We understand how local businesses rank and grow.</p>
          </div>
          <div className="grid md:grid-cols-2 gap-5">
            {[
              { title: "🇧🇩 Local Market Expertise", desc: "We know Bangladesh search behavior — Bengali + English queries, local intent, Dhaka-centric business patterns." },
              { title: "📈 Data-Driven Approach", desc: "Every strategy is built on keyword research, competitor analysis, and real ranking data — not guesswork." },
              { title: "⚡ Fast, Tangible Results", desc: "We target quick wins (GSC fixes, content gaps, technical issues) while building long-term authority." },
              { title: "🤝 Transparent Reporting", desc: "Monthly reports with real KPIs: rankings, traffic, conversions, ROI. No vanity metrics. Just results." },
            ].map((a, i) => (
              <div key={i} className="bg-white rounded-2xl p-7 border border-gray-100 hover:border-primary/20 hover:shadow-md transition-all">
                <h3 className="font-bold text-lg mb-2 text-gray-900">{a.title}</h3>
                <p className="text-gray-500 text-sm leading-relaxed">{a.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* === PROCESS === */}
      <section id="process" className="py-24 px-4">
        <div className="max-w-5xl mx-auto">
          <div className="text-center mb-16">
            <span className="text-primary text-sm font-semibold tracking-widest uppercase">How We Work</span>
            <h2 className="text-3xl md:text-5xl font-extrabold mt-3 mb-4 text-gray-900">Our 5-Step Process</h2>
            <p className="text-gray-500 max-w-xl mx-auto">A proven system that delivers measurable SEO results for Bangladeshi businesses.</p>
          </div>
          <div className="grid md:grid-cols-5 gap-6">
            {[
              { step: "01", title: "Audit", desc: "Full site analysis — technical, content, backlinks, competitors" },
              { step: "02", title: "Strategy", desc: "Custom SEO plan with Bangladesh keyword targeting" },
              { step: "03", title: "Execute", desc: "On-page fixes, content, link building, technical SEO" },
              { step: "04", title: "Monitor", desc: "Track rankings, traffic, and conversions weekly" },
              { step: "05", title: "Optimize", desc: "Iterate and improve based on real performance data" },
            ].map((p, i) => (
              <div key={i} className="text-center p-4">
                <div className="w-14 h-14 mx-auto mb-4 rounded-2xl bg-primary text-white flex items-center justify-center font-extrabold text-sm shadow-lg">{p.step}</div>
                <h3 className="font-bold text-gray-900 mb-1">{p.title}</h3>
                <p className="text-gray-500 text-xs leading-relaxed">{p.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* === CTA BANNER === */}
      <section className="py-24 px-4 bg-gradient-to-r from-primary to-primary-dark">
        <div className="max-w-2xl mx-auto text-center">
          <h2 className="text-3xl md:text-5xl font-extrabold mb-4 text-white">Ready to <span className="text-amber-300">Dominate</span> Search?</h2>
          <p className="text-primary/80 mb-10 text-lg">Get a free SEO audit for your Bangladesh business. No commitment, no hidden fees.</p>
          <a href="#contact" className="inline-flex items-center gap-2 bg-white text-primary-dark px-10 py-4 rounded-xl font-bold text-lg transition-all hover:shadow-xl hover:-translate-y-0.5">
            Get Your Free Audit →
          </a>
        </div>
      </section>

      {/* === CONTACT === */}
      <section id="contact" className="py-24 px-4 bg-gray-50">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-16">
            <span className="text-primary text-sm font-semibold tracking-widest uppercase">Get In Touch</span>
            <h2 className="text-3xl md:text-4xl font-extrabold mt-3 mb-4 text-gray-900">Contact Kanok MiahIT</h2>
            <p className="text-gray-500 mb-6">Ready to rank? Fill out the form and we'll get back to you within 24 hours.</p>
            <div className="flex flex-wrap items-center justify-center gap-4 text-sm">
              <a href="tel:+880****3101" className="inline-flex items-center gap-2 bg-green-50 border border-green-200 text-green-700 px-5 py-2.5 rounded-full font-semibold hover:bg-green-100">
                📞 <span className="font-bold">+880 1712-883101</span>
              </a>
              <a href="https://wa.me/8801712883101?text=Hi%20Kanok%20MiahIT!%20I%20need%20SEO%20help%20for%20my%20business."
                 target="_blank" rel="noopener noreferrer"
                 className="inline-flex items-center gap-2 bg-emerald-50 border border-emerald-200 text-emerald-700 px-5 py-2.5 rounded-full font-semibold hover:bg-emerald-100">
                💬 WhatsApp Us
              </a>
            </div>
          </div>
          <div className="grid md:grid-cols-2 gap-8 items-start">
            {/* Form */}
            <div className="bg-white border border-gray-200 rounded-2xl p-8 shadow-sm">
              <form action="https://formspree.io/f/xvgkrvrz" method="POST" className="space-y-5">
                <div>
                  <label className="block text-sm text-gray-600 mb-1.5 font-medium">Your Name *</label>
                  <input type="text" name="name" required placeholder="e.g. Md. Rahim"
                    className="w-full bg-gray-50 border border-gray-200 rounded-xl px-4 py-3 text-gray-900 placeholder-gray-400 focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary/20 transition-all" />
                </div>
                <div>
                  <label className="block text-sm text-gray-600 mb-1.5 font-medium">Email Address *</label>
                  <input type="email" name="email" required placeholder="your@email.com"
                    className="w-full bg-gray-50 border border-gray-200 rounded-xl px-4 py-3 text-gray-900 placeholder-gray-400 focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary/20 transition-all" />
                </div>
                <div>
                  <label className="block text-sm text-gray-600 mb-1.5 font-medium">Phone Number</label>
                  <input type="tel" name="phone" placeholder="01712-883101"
                    className="w-full bg-gray-50 border border-gray-200 rounded-xl px-4 py-3 text-gray-900 placeholder-gray-400 focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary/20 transition-all" />
                </div>
                <div>
                  <label className="block text-sm text-gray-600 mb-1.5 font-medium">Your Website</label>
                  <input type="url" name="website" placeholder="https://yourwebsite.com"
                    className="w-full bg-gray-50 border border-gray-200 rounded-xl px-4 py-3 text-gray-900 placeholder-gray-400 focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary/20 transition-all" />
                </div>
                <div>
                  <label className="block text-sm text-gray-600 mb-1.5 font-medium">Tell Us About Your Project *</label>
                  <textarea name="message" required rows="4" placeholder="I need SEO for my e-commerce store in Dhaka..."
                    className="w-full bg-gray-50 border border-gray-200 rounded-xl px-4 py-3 text-gray-900 placeholder-gray-400 focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary/20 transition-all resize-none"></textarea>
                </div>
                <input type="hidden" name="_subject" value="New SEO Lead from Kanok MiahIT Website!" />
                <input type="text" name="_gotcha" style={{display: "none"}} />
                <button type="submit"
                  className="w-full bg-primary hover:bg-primary-dark text-white font-bold py-3.5 px-6 rounded-xl hover:shadow-lg transition-all">
                  Get Free SEO Audit →
                </button>
                <p className="text-xs text-gray-400 text-center">We respect your privacy. No spam, ever.</p>
              </form>
            </div>

            {/* Contact Info */}
            <div className="space-y-6">
              <div className="bg-white border border-gray-200 rounded-2xl p-7 shadow-sm">
                <h3 className="font-bold text-lg mb-4 text-gray-900">📞 Call Us Directly</h3>
                <p className="text-gray-500 text-sm mb-3">Speak directly with Kanok MiahIT's SEO team:</p>
                <a href="tel:+880****3101" className="text-2xl font-extrabold text-primary hover:text-primary-dark">+880 1712-883101</a>
              </div>
              <div className="bg-white border border-gray-200 rounded-2xl p-7 shadow-sm">
                <h3 className="font-bold text-lg mb-4 text-gray-900">💬 WhatsApp</h3>
                <p className="text-gray-500 text-sm mb-3">Quick response on WhatsApp:</p>
                <a href="https://wa.me/8801712883101?text=Hi%20Kanok%20MiahIT!%20I%20need%20SEO%20help."
                   target="_blank" rel="noopener noreferrer"
                   className="inline-flex items-center gap-2 bg-emerald-50 border border-emerald-200 text-emerald-700 px-5 py-3 rounded-xl font-semibold hover:bg-emerald-100 text-sm">
                  💬 Chat on WhatsApp → <span className="text-xs text-gray-400">(Fastest Response)</span>
                </a>
              </div>
              <div className="bg-white border border-gray-200 rounded-2xl p-7 shadow-sm">
                <h3 className="font-bold text-lg mb-4 text-gray-900">📍 Other Ways to Reach</h3>
                <div className="space-y-3 text-sm">
                  <div className="flex items-center gap-3">
                    <span className="text-xl">📧</span>
                    <a href="mailto:mdkanokmiah232@gmail.com" className="text-gray-600 hover:text-primary">mdkanokmiah232@gmail.com</a>
                  </div>
                  <div className="flex items-center gap-3">
                    <span className="text-xl">🌐</span>
                    <a href="https://kanokmiah.com" target="_blank" rel="noopener noreferrer" className="text-gray-600 hover:text-primary">kanokmiah.com</a>
                  </div>
                  <div className="flex items-center gap-3">
                    <span className="text-xl">📍</span>
                    <span className="text-gray-600">Dhaka, Bangladesh</span>
                  </div>
                </div>
              </div>
              <div className="bg-gradient-to-r from-primary to-primary-dark rounded-2xl p-6 text-center shadow-sm">
                <p className="text-white text-sm font-semibold">⭐ Free SEO Audit — Worth BDT 5,000</p>
                <p className="text-primary/80 text-xs mt-1">Get a complete analysis of your website. No commitment required.</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* === FOOTER === */}
      <footer className="py-10 border-t border-gray-100 text-center text-sm text-gray-500">
        <div className="max-w-4xl mx-auto px-4">
          <div className="flex flex-wrap justify-center gap-6 mb-4">
            <a href="/" className="hover:text-primary">Home</a>
            <a href="/industries" className="hover:text-primary">Industries</a>
            <a href="/blog" className="hover:text-primary">Blog</a>
            <a href="/about" className="hover:text-primary">About</a>
            <a href="/privacy-policy" className="hover:text-primary">Privacy</a>
            <a href="/terms-of-service" className="hover:text-primary">Terms</a>
          </div>
          <p>© 2026 <span className="text-primary font-bold">Kanok MiahIT</span> — SEO Agency in Bangladesh. All rights reserved.</p>
          <p className="mt-2 text-xs text-gray-400">🇧🇩 Serving Dhaka, Chittagong, Sylhet & all of Bangladesh</p>
        </div>
      </footer>

    </div>
  );
}
