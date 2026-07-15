"use client";

import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import Link from "next/link";
// FAQSchema rendered server-side in page.js — not duplicated here

export default function AboutClient() {

  return (
    <div className="min-h-screen bg-white text-gray-900">

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
            <span className="text-primary">About</span><br/>
            <span className="text-gray-900">Kanok Miah</span>
          </h1>
          <p className="text-lg md:text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
            Founded in Dhaka, Bangladesh, Kanok Miah — <Link href="/" className="text-primary font-semibold hover:underline">best SEO expert in Dhaka</Link> — is a results-driven SEO professional who helps local businesses 
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
                Kanok Miah started with a simple observation: Bangladeshi businesses were struggling to get found 
                online. Most SEO agencies either offered generic solutions that didn't account for local search behaviour 
                or were located overseas with no real understanding of the Bangladesh market.
              </p>
              <p>
                Founded by <strong className="text-gray-900">Kanok Miah</strong>, my practice set out to bridge that gap. 
                Since 2019, I've been delivering hands-on SEO expertise optimising websites for Bangladeshi audiences, developing
                a proprietary approach that blends technical SEO rigour with deep cultural and linguistic insights.
              </p>
              <p>
                From small local shops in Dhaka to growing e-commerce brands serving customers nationwide, I've helped 
                over 50 clients achieve first-page rankings on Google. My strategies account for Bengali-language queries, 
                mobile-first usage patterns, and the unique competitive landscape of Bangladesh's digital economy.
              </p>
              <p>
                Today, Kanok Miah is recognised as one of Bangladesh's most trusted SEO experts, delivering
                transparent, data-driven SEO services that generate real business results — not just vanity metrics.
              </p>
              <p>
                As the <strong className="text-gray-900">Founder of kanokmiah.com</strong>, I bring a wealth of
                professional experience from leadership roles across Bangladesh's digital landscape. I currently serve as
                <strong className="text-gray-900"> SEO Project Manager at Khan IT</strong> and
                <strong className="text-gray-900"> Head of Digital Marketing at CloudMatrix Tech</strong>.
                Previously, I held key positions at <strong className="text-gray-900">Walton Plaza</strong> and
                <strong className="text-gray-900">Solus Corporation</strong>, where I honed my expertise in
                search engine optimisation and digital marketing strategy.
              </p>
              <p>
                Today, I manage <strong className="text-gray-900">8–12 SEO projects</strong> and
                <strong className="text-gray-900"> 2–5 ad campaigns</strong> each month, delivering measurable
                growth for businesses across Bangladesh. My hands-on approach combines technical SEO rigour with
                deep market understanding to consistently drive first-page rankings.
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
              <div className="text-2xl font-extrabold text-gray-900">Since 2019</div>
              <div className="text-sm text-gray-500">Experience</div>
            </div>
            <div className="bg-white border border-gray-100 rounded-2xl p-6 text-center hover:shadow-lg hover:-translate-y-1 transition-all">
              <div className="text-3xl mb-3">📈</div>
              <div className="text-2xl font-extrabold text-gray-900">210+</div>
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
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-3">
            <span className="inline-flex items-center gap-2 bg-green-50 border border-green-200 text-green-700 text-sm font-semibold px-4 py-3 rounded-xl">
              ✅ Google Digital Garage
            </span>
            <span className="inline-flex items-center gap-2 bg-blue-50 border border-blue-200 text-blue-700 text-sm font-semibold px-4 py-3 rounded-xl">
              ✅ HubSpot Academy
            </span>
            <span className="inline-flex items-center gap-2 bg-purple-50 border border-purple-200 text-purple-700 text-sm font-semibold px-4 py-3 rounded-xl">
              ✅ SEMrush Academy
            </span>
            <span className="inline-flex items-center gap-2 bg-amber-50 border border-amber-200 text-amber-700 text-sm font-semibold px-4 py-3 rounded-xl">
              ✅ LinkedIn Learning
            </span>
            <span className="inline-flex items-center gap-2 bg-rose-50 border border-rose-200 text-rose-700 text-sm font-semibold px-4 py-3 rounded-xl">
              ✅ Coursera
            </span>
            <span className="inline-flex items-center gap-2 bg-cyan-50 border border-cyan-200 text-cyan-700 text-sm font-semibold px-4 py-3 rounded-xl">
              ✅ Skillshare
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
            { num: "210+", label: "Projects Done", color: "from-primary to-primary-dark" },
            { num: "50+", label: "Happy Clients", color: "from-primary to-primary-dark" },
            { num: "95%", label: "Client Retention", color: "from-primary to-primary-dark" },
            { num: "Since 2019", label: "Years Exp.", color: "from-primary to-primary-dark" },
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

      {/* === MEET THE TEAM === */}
      <section className="relative py-24 px-4 bg-gray-50/50 overflow-hidden">
        <div className="relative max-w-5xl mx-auto">
          {/* HEADING */}
          <div className="text-center mb-14">
            <span className="inline-block text-primary text-sm font-semibold tracking-[0.2em] uppercase px-4 py-1.5 bg-primary-light/60 rounded-full border border-primary/10">Our Team</span>
            <h2 className="text-3xl md:text-5xl font-extrabold mt-5 mb-4 text-gray-900">
              Meet the <span className="text-primary">Experts</span>
            </h2>
            <p className="text-gray-500 max-w-2xl mx-auto text-lg">
              The talented people behind every successful SEO campaign — dedicated to growing your business.
            </p>
          </div>

          {/* LINE 1: Shazzat — Kanok Miah (center) — Sabbir */}
          <div className="grid grid-cols-3 gap-5 md:gap-8 items-center mb-6 md:mb-8">
            {/* Left: Shazzat */}
            <div className="group text-center">
              <div className="mx-auto w-24 h-24 md:w-28 md:h-28 mb-3 rounded-full overflow-hidden border-[3px] border-white shadow-md">
                <img src="/images/team/team-sazzat.webp" alt="Md Shazzat Hossain" width="150" height="150" loading="lazy"
                  className="w-full h-full object-cover object-center group-hover:scale-105 transition-transform duration-500" />
              </div>
              <h3 className="font-bold text-gray-900 text-xs md:text-sm leading-tight">Md Shazzat Hossain</h3>
              <p className="text-gray-500 text-[10px] md:text-xs mt-0.5">Head of Branding</p>
            </div>

            {/* Center: Kanok Miah — larger */}
            <div className="group text-center -mx-2 md:-mx-4">
              <div className="relative mx-auto w-28 h-28 md:w-36 md:h-36 mb-3">
                <div className="w-full h-full rounded-full overflow-hidden border-[4px] border-white shadow-lg">
                  <img src="/images/team/team-kanok-miah.webp" alt="Kanok Miah" width="200" height="200"
                    className="w-full h-full object-cover object-center group-hover:scale-105 transition-transform duration-500" />
                </div>
                <div className="absolute -bottom-1 left-1/2 -translate-x-1/2 bg-primary text-white text-[9px] md:text-[10px] font-bold px-2.5 py-0.5 rounded-full shadow-md whitespace-nowrap">
                  ⭐ Founder
                </div>
              </div>
              <h3 className="font-bold text-gray-900 text-sm md:text-base">Kanok Miah</h3>
              <p className="text-primary text-[11px] md:text-xs font-medium">Founder & Lead SEO Consultant</p>
              <div className="flex items-center justify-center gap-2 mt-2">
                <a href="https://www.facebook.com/mdkanokmiahweb" target="_blank" rel="noopener noreferrer"
                  className="w-6 h-6 rounded-full bg-gray-200 flex items-center justify-center text-gray-500 hover:bg-primary hover:text-white transition-all"
                  aria-label="Kanok Miah Facebook">
                  <svg className="w-2.5 h-2.5" fill="currentColor" viewBox="0 0 24 24"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
                </a>
                <a href="https://kanokmiah.com" target="_blank" rel="noopener noreferrer"
                  className="w-6 h-6 rounded-full bg-gray-200 flex items-center justify-center text-gray-500 hover:bg-primary hover:text-white transition-all"
                  aria-label="Kanok Miah Website">
                  <svg className="w-2.5 h-2.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" /></svg>
                </a>
              </div>
            </div>

            {/* Right: Sabbir */}
            <div className="group text-center">
              <div className="mx-auto w-24 h-24 md:w-28 md:h-28 mb-3 rounded-full overflow-hidden border-[3px] border-white shadow-md">
                <img src="/images/team/team-sabbir.webp" alt="Md Sabbir Hossain" width="150" height="150" loading="lazy"
                  className="w-full h-full object-cover object-center group-hover:scale-105 transition-transform duration-500" />
              </div>
              <h3 className="font-bold text-gray-900 text-xs md:text-sm leading-tight">Md Sabbir Hossain</h3>
              <p className="text-gray-500 text-[10px] md:text-xs mt-0.5">SEO Executive</p>
            </div>
          </div>

          {/* LINE 2: Papon — Sammam — Nusaiba */}
          <div className="grid grid-cols-3 gap-5 md:gap-8">
            {[
              { name: "Papon Hasan", role: "SEO Executive", img: "/images/team/team-papon.webp" },
              { name: "Sammam Iqbal", role: "SEO & Social Media Manager", img: "/images/team/team-sammam.webp" },
              { name: "Nusaiba Mim", role: "SEO Executive", img: "/images/team/team-female.webp" },
            ].map((member, i) => (
              <div key={i} className="group text-center">
                <div className="mx-auto w-24 h-24 md:w-28 md:h-28 mb-3 rounded-full overflow-hidden border-[3px] border-white shadow-md">
                  <img
                    src={member.img}
                    alt={member.name}
                    width="150"
                    height="150"
                    loading="lazy"
                    className="w-full h-full object-cover object-center group-hover:scale-105 transition-transform duration-500"
                  />
                </div>
                <h3 className="font-bold text-gray-900 text-xs md:text-sm leading-tight">{member.name}</h3>
                <p className="text-gray-500 text-[10px] md:text-xs mt-0.5">{member.role}</p>
              </div>
            ))}
          </div>

          {/* Bottom CTA */}
          <div className="text-center mt-12">
            <p className="text-gray-500 text-sm">
              Want to work with us? <a href="/contact" className="text-primary font-semibold hover:underline">Get in touch</a> — we'd love to hear from you.
            </p>
          </div>
        </div>
      </section>

      {/* === FAQ === */}
      <section className="py-16 px-4 bg-white">
        <div className="max-w-4xl mx-auto">
          {/* FAQ schema rendered server-side in page.js */}
          <h2 className="text-2xl md:text-3xl font-extrabold text-center mb-8">
            Frequently Asked <span className="text-primary">Questions</span>
          </h2>
          <div className="space-y-0 divide-y divide-gray-100">
            {[
              { question: "What experience does Kanok Miah have?", answer: "Kanok Miah has been delivering SEO results since 2019, helping 50+ Bangladeshi businesses achieve first-page rankings on Google. His expertise spans local SEO, technical SEO, link building, semantic SEO, and GEO/AI search optimization." },
              { question: "What areas of Bangladesh do you serve?", answer: "I provide SEO services for businesses throughout Bangladesh including Dhaka, Chittagong, Sylhet, Khulna, Rajshahi, and all other major cities. My local SEO strategies are customized for each city's specific market." },
              { question: "What types of businesses do you work with?", answer: "I work with a diverse range of clients including local service businesses, e-commerce stores (Shopify, Daraz), real estate agencies, healthcare providers, educational institutions, and hospitality businesses across Bangladesh." },
              { question: "Do you offer a free consultation?", answer: "Yes! I offer a completely free initial consultation to discuss your business goals and SEO needs. During this call, I'll provide preliminary insights and recommendations with no obligation to proceed." },
              { question: "How do I get started with your services?", answer: "Getting started is simple: contact me through the website form, call +880 1604-809110, or send a WhatsApp message. I'll begin with a free SEO audit of your website and provide a customized strategy proposal." },
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
          <p className="text-white/80 mb-10 text-lg">Ready to see what a dedicated SEO partnership can do for your Bangladesh business? Get your free audit today.</p>
          <Link href="/#contact" className="group inline-flex items-center gap-2 bg-white text-primary-dark px-10 py-4 rounded-xl font-bold text-lg transition-all hover:shadow-xl hover:-translate-y-0.5">
            Get Your Free Audit
            <span className="group-hover:translate-x-1 transition-transform">→</span>
          </Link>
        </div>
      </section>

      <Footer />
    </div>
  );
}
