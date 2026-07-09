"use client";

import Navbar from "@/components/Navbar";
import Link from "next/link";
import { BreadcrumbSchema, FAQSchema } from "@/components/Schema";

export default function AboutClient() {

  return (
    <div className="min-h-screen bg-white text-gray-900">
      <head>
        <link rel="canonical" href="https://kanokmiah.com.bd/about" />
        <meta name="robots" content="index, follow" />
        {BreadcrumbSchema([
          { name: "Home", url: "https://kanokmiah.com.bd" },
          { name: "About", url: "https://kanokmiah.com.bd/about" },
        ])}
      </head>

      {/* === NAVBAR === */}
      <Navbar />

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
            Founded in Dhaka, Bangladesh, Md Kanok Miah is a results-driven SEO expert who helps local businesses 
            dominate search engine rankings. Combining deep local market knowledge with global SEO best practices 
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
                Founded by <strong className="text-gray-900">Md Kanok Miah</strong>, my practice set out to bridge that gap. 
                With over 6 years of hands-on experience optimising websites for Bangladeshi audiences, I've developed 
                a proprietary approach that blends technical SEO rigour with deep cultural and linguistic insights.
              </p>
              <p>
                From small local shops in Dhaka to growing e-commerce brands serving customers nationwide, I've helped 
                over 50 clients achieve first-page rankings on Google. My strategies account for Bengali-language queries, 
                mobile-first usage patterns, and the unique competitive landscape of Bangladesh's digital economy.
              </p>
              <p>
                Today, Md Kanok Miah is recognised as one of Bangladesh's most trusted SEO experts, delivering 
                transparent, data-driven SEO services that generate real business results — not just vanity metrics.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* === CREDENTIALS & CERTIFICATIONS === */}
      <section className="relative py-16 px-4 bg-gradient-to-b from-white to-gray-50/50">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-10">
            <span className="text-primary text-sm font-semibold tracking-widest uppercase">Credentials</span>
            <h2 className="text-3xl md:text-4xl font-extrabold mt-3 mb-4">
              Trusted <span className="text-primary">Expertise</span> & Certifications
            </h2>
            <p className="text-gray-600 max-w-2xl mx-auto">Verified credentials that back every SEO strategy I deliver.</p>
          </div>
          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
            <div className="bg-white border border-gray-100 rounded-2xl p-6 text-center hover:shadow-lg hover:-translate-y-1 transition-all">
              <div className="text-3xl mb-3">🏆</div>
              <div className="text-2xl font-extrabold text-gray-900">6+ Years</div>
              <div className="text-sm text-gray-500">Experience</div>
            </div>
            <div className="bg-white border border-gray-100 rounded-2xl p-6 text-center hover:shadow-lg hover:-translate-y-1 transition-all">
              <div className="text-3xl mb-3">📈</div>
              <div className="text-2xl font-extrabold text-gray-900">350+</div>
              <div className="text-sm text-gray-500">Projects Completed</div>
            </div>
            <div className="bg-white border border-gray-100 rounded-2xl p-6 text-center hover:shadow-lg hover:-translate-y-1 transition-all">
              <div className="text-3xl mb-3">🤝</div>
              <div className="text-2xl font-extrabold text-gray-900">50+</div>
              <div className="text-sm text-gray-500">Clients Served</div>
            </div>
            <div className="bg-white border border-gray-100 rounded-2xl p-6 text-center hover:shadow-lg hover:-translate-y-1 transition-all">
              <div className="text-3xl mb-3">⭐</div>
              <div className="text-2xl font-extrabold text-gray-900">4.9/5</div>
              <div className="text-sm text-gray-500">Client Rating</div>
            </div>
          </div>
          <div className="flex flex-wrap justify-center gap-4">
            <span className="inline-flex items-center gap-2 bg-green-50 border border-green-200 text-green-700 text-sm font-semibold px-5 py-3 rounded-xl">
              ✅ Google Business Profile Certified
            </span>
            <span className="inline-flex items-center gap-2 bg-blue-50 border border-blue-200 text-blue-700 text-sm font-semibold px-5 py-3 rounded-xl">
              ✅ Google Search Console Certified
            </span>
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
              To be Bangladesh's most trusted SEO expert — known for integrity, transparency, 
              and exceptional results. I envision a digital Bangladesh where local businesses 
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
              Core <span className="text-primary">Values</span> & SEO Philosophy
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

      {/* === PHOTO GALLERY === */}
      <section className="relative py-24 px-4 bg-gray-50/80">
        <div className="absolute inset-0 bg-gradient-to-b from-transparent via-primary/[0.02] to-transparent" />
        <div className="relative max-w-6xl mx-auto">
          <div className="text-center mb-14">
            <span className="text-primary text-sm font-semibold tracking-[0.2em] uppercase">Our Memories</span>
            <h2 className="text-3xl md:text-5xl font-extrabold mt-4 mb-4 text-gray-900">
              Office Tour & <span className="text-primary">Team Moments</span>
            </h2>
            <p className="text-gray-500 max-w-xl mx-auto text-lg">
              A glimpse into our journey — team outings, client meetings, and the people behind the results.
            </p>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
            {[
              { src: "/images/gallery/gallery-faruk-khan-office-tour.webp", alt: "Kanok Miah with Md Faruk Khan and team during office tour in Gazipur", span: "md:col-span-2 md:row-span-2" },
              { src: "/images/gallery/gallery-team-office-tour-3.webp", alt: "Kanok Miah with team members during office tour" },
              { src: "/images/gallery/gallery-pyramid-resort-main.webp", alt: "Kanok Miah office tour with KhanIT team at Pyramid Point Resort" },
              { src: "/images/gallery/gallery-pyramid-resort-team-1.webp", alt: "Kanok Miah with teammates at Pyramid Point Resort" },
              { src: "/images/gallery/gallery-pyramid-resort-team-2.webp", alt: "Team photo at Pyramid Point Resort outing" },
              { src: "/images/gallery/gallery-pyramid-resort-team-4.webp", alt: "Kanok Miah with KhanIT CEO and team at Pyramid Point Resort" },
              { src: "/images/gallery/gallery-team-office-tour-4.webp", alt: "Kanok Miah with team members during office visit", span: "md:col-span-2" },
              { src: "/images/gallery/gallery-pyramid-resort-team-5.webp", alt: "Team celebration at Pyramid Point Resort" },
              { src: "/images/gallery/gallery-pyramid-resort-team-6.webp", alt: "Team bonding at Pyramid Point Resort" },
            ].map((img, i) => (
              <a
                key={i}
                href={img.src}
                target="_blank"
                rel="noopener noreferrer"
                className={`group relative overflow-hidden rounded-2xl bg-gray-100 border border-gray-200 ${img.span || ""} transition-all duration-500 hover:shadow-xl hover:-translate-y-1`}
              >
                <img
                  src={img.src}
                  alt={img.alt}
                  width="400"
                  height="400"
                  loading="lazy"
                  className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700 ease-out"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/50 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                <div className="absolute bottom-0 left-0 right-0 p-4 translate-y-4 group-hover:translate-y-0 transition-all duration-300 opacity-0 group-hover:opacity-100">
                  <p className="text-white text-xs font-medium truncate">{img.alt}</p>
                </div>
              </a>
            ))}
          </div>
        </div>
      </section>

      {/* === FAQ === */}
      <section className="py-16 px-4 bg-white">
        <div className="max-w-4xl mx-auto">
          <FAQSchema faqs={[
            { question: "What experience does Md Kanok Miah have?", answer: "Md Kanok Miah has over 6 years of hands-on SEO experience, helping 50+ Bangladeshi businesses achieve first-page rankings on Google. His expertise spans local SEO, technical SEO, link building, semantic SEO, and GEO/AI search optimization." },
            { question: "What areas of Bangladesh do you serve?", answer: "I provide SEO services for businesses throughout Bangladesh including Dhaka, Chittagong, Sylhet, Khulna, Rajshahi, and all other major cities. My local SEO strategies are customized for each city's specific market." },
            { question: "What types of businesses do you work with?", answer: "I work with a diverse range of clients including local service businesses, e-commerce stores (Shopify, Daraz), real estate agencies, healthcare providers, educational institutions, and hospitality businesses across Bangladesh." },
            { question: "Do you offer a free consultation?", answer: "Yes! I offer a completely free initial consultation to discuss your business goals and SEO needs. During this call, I'll provide preliminary insights and recommendations with no obligation to proceed." },
            { question: "How do I get started with your services?", answer: "Getting started is simple: contact me through the website form, call +880 1712-883101, or send a WhatsApp message. I'll begin with a free SEO audit of your website and provide a customized strategy proposal." },
          ]} />
          <h2 className="text-2xl md:text-3xl font-extrabold text-center mb-8">
            Frequently Asked <span className="text-primary">Questions</span>
          </h2>
          <div className="space-y-0 divide-y divide-gray-100">
            {[
              { question: "What experience does Md Kanok Miah have?", answer: "Md Kanok Miah has over 6 years of hands-on SEO experience, helping 50+ Bangladeshi businesses achieve first-page rankings on Google. His expertise spans local SEO, technical SEO, link building, semantic SEO, and GEO/AI search optimization." },
              { question: "What areas of Bangladesh do you serve?", answer: "I provide SEO services for businesses throughout Bangladesh including Dhaka, Chittagong, Sylhet, Khulna, Rajshahi, and all other major cities. My local SEO strategies are customized for each city's specific market." },
              { question: "What types of businesses do you work with?", answer: "I work with a diverse range of clients including local service businesses, e-commerce stores (Shopify, Daraz), real estate agencies, healthcare providers, educational institutions, and hospitality businesses across Bangladesh." },
              { question: "Do you offer a free consultation?", answer: "Yes! I offer a completely free initial consultation to discuss your business goals and SEO needs. During this call, I'll provide preliminary insights and recommendations with no obligation to proceed." },
              { question: "How do I get started with your services?", answer: "Getting started is simple: contact me through the website form, call +880 1712-883101, or send a WhatsApp message. I'll begin with a free SEO audit of your website and provide a customized strategy proposal." },
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
