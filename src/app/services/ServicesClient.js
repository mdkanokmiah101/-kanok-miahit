"use client";

import Link from "next/link";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { FAQSchema } from "@/components/Schema";
import servicesList from "./data";

export default function ServicesClient() {

  const faqs = [
    { question: "How long does it take to see results from SEO?", answer: "Most clients see initial improvements within 4–8 weeks, with significant ranking gains in 3–6 months. Results depend on your industry competition, current site health, and the scope of work." },
    { question: "Do you offer SEO services for specific industries?", answer: "Yes, I specialize in SEO for multiple industries including real estate, e-commerce, healthcare, education, hospitality, and local service businesses across Bangladesh." },
    { question: "How is your SEO different from other agencies?", answer: "I combine deep local Bangladesh market knowledge with global SEO best practices. My strategies are data-driven, transparent, and focused on real business results — not vanity metrics." },
    { question: "Do you provide monthly SEO reports?", answer: "Absolutely. Every client receives detailed monthly reports showing keyword rankings, organic traffic, backlink growth, conversion data, and actionable recommendations for continued improvement." },
    { question: "Can I see examples of your past SEO work?", answer: "Yes, I have helped over 50 Bangladeshi businesses achieve first-page rankings. Contact me for a free consultation where I can share case studies relevant to your industry." },
  ];

  return (
    <div className="min-h-screen bg-white text-gray-900">
      <head>
      </head>
      <Navbar />

      {/* Hero */}
      <section className="relative pt-32 pb-16 px-4 text-center overflow-hidden bg-gradient-to-b from-gray-50 to-white">
        <div className="absolute top-1/4 left-1/4 w-72 h-72 bg-primary/[0.08] rounded-full blur-3xl" />
        <div className="absolute bottom-1/4 right-1/4 w-80 h-80 bg-primary/[0.05] rounded-full blur-3xl" />
        <div className="relative max-w-4xl mx-auto">
          <span className="text-primary text-sm font-semibold tracking-widest uppercase">What I Do</span>
          <h1 className="text-4xl md:text-6xl font-extrabold mt-4 mb-6">
            SEO Services for{" "}
            <span className="text-primary">Bangladesh</span>
          </h1>
          <p className="text-gray-500 text-lg max-w-2xl mx-auto leading-relaxed">
            Complete SEO solutions tailored for Bangladeshi businesses — from local Dhaka SEO 
            to international optimization. Every strategy is data-driven, transparent, and results-focused.
          </p>
          <div className="mt-8 flex flex-wrap justify-center gap-4">
            <Link href="/contact" className="inline-flex items-center gap-2 bg-primary hover:bg-primary-dark text-white px-6 py-3 rounded-xl font-bold text-sm transition-all hover:shadow-lg hover:-translate-y-0.5">
              Get Free SEO Audit →
            </Link>
            <Link href="/industries" className="inline-flex items-center gap-2 border border-gray-200 text-gray-600 px-6 py-3 rounded-xl font-semibold text-sm hover:border-primary hover:text-primary transition-all">
              View Industries
            </Link>
          </div>
        </div>
      </section>

      {/* Services */}
      <section className="py-16 px-4">
        <div className="max-w-6xl mx-auto space-y-10">
          {servicesList.map((svc, i) => (
            <div key={i} className="bg-gray-50 border border-gray-100 rounded-2xl p-8 md:p-10 hover:border-primary/20 transition-all">
              <div className="flex flex-col md:flex-row gap-8">
                <div className="md:w-1/3">
                  <div className="text-5xl mb-4">{svc.icon}</div>
                  <h2 className="text-2xl md:text-3xl font-extrabold text-gray-900 mb-2">{svc.title}</h2>
                  <p className="text-gray-500 text-sm leading-relaxed">{svc.subtitle}</p>
                  <Link href={`/services/${svc.slug}`} className="inline-flex items-center gap-1 mt-4 text-primary text-sm font-semibold hover:text-primary-dark transition-colors">
                    Learn More →
                  </Link>
                </div>
                <div className="md:w-2/3">
                  <p className="text-gray-600 leading-relaxed mb-5">{svc.desc}</p>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                    {svc.features.map((f, fi) => (
                      <div key={fi} className="flex items-start gap-2 text-sm text-gray-600">
                        <span className="text-primary shrink-0 mt-0.5">✓</span>
                        <span>{f}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Process */}
      <section className="py-16 px-4 bg-gray-50 border-y border-gray-100">
        <div className="max-w-5xl mx-auto text-center">
          <span className="text-primary text-sm font-semibold tracking-widest uppercase">How I Work</span>
          <h2 className="text-3xl md:text-4xl font-extrabold mt-3 mb-6 text-gray-900">My 5-Step Professional SEO Process for <span className="text-primary">Bangladesh Websites</span></h2>
          <p className="text-gray-500 max-w-xl mx-auto mb-12">A proven system that delivers measurable SEO results for Bangladeshi businesses.</p>
          <div className="grid md:grid-cols-5 gap-4">
            {[
              { step: "01", title: "Audit", desc: "Full site analysis — technical, content, backlinks, competitors" },
              { step: "02", title: "Strategy", desc: "Custom SEO plan with Bangladesh keyword targeting" },
              { step: "03", title: "Execute", desc: "On-page fixes, content, link building, technical SEO" },
              { step: "04", title: "Monitor", desc: "Track rankings, traffic, and conversions weekly" },
              { step: "05", title: "Optimize", desc: "Iterate and improve based on real performance data" },
            ].map((p, pi) => (
              <div key={pi} className="bg-white border border-gray-100 rounded-2xl p-5 hover:border-primary/20 hover:-translate-y-1 transition-all">
                <div className="w-12 h-12 mx-auto mb-3 rounded-xl bg-primary flex items-center justify-center font-extrabold text-sm text-white">{p.step}</div>
                <h3 className="font-bold text-gray-900 mb-1">{p.title}</h3>
                <p className="text-gray-500 text-xs leading-relaxed">{p.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Internal Links — Explore All Services */}
      <section className="py-16 px-4 bg-gray-50/80 border-y border-gray-100">
        <div className="max-w-4xl mx-auto text-center">
          <span className="text-primary text-sm font-semibold tracking-widest uppercase">Explore Our Services</span>
          <h2 className="text-2xl md:text-3xl font-extrabold mt-4 mb-4 text-gray-900">
            Complete <span className="text-primary">SEO Services</span> for Your Business
          </h2>
          <p className="text-gray-500 mb-8 max-w-2xl mx-auto">
            Explore our specialized SEO services designed to grow your business in Bangladesh:
          </p>
          <div className="flex flex-wrap justify-center gap-3">
            {servicesList.map((svc) => (
              <Link
                key={svc.slug}
                href={`/services/${svc.slug}`}
                className="inline-flex items-center gap-2 bg-white border border-gray-200 text-gray-700 px-5 py-2.5 rounded-xl text-sm font-semibold hover:border-primary hover:text-primary hover:bg-primary-light transition-all"
              >
                {svc.icon} {svc.title}
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* FAQ */}
      <section className="py-16 px-4 bg-white">
        <div className="max-w-4xl mx-auto">
          <FAQSchema faqs={faqs} />
          <h2 className="text-2xl md:text-3xl font-extrabold text-center mb-8">
            Frequently Asked <span className="text-primary">Questions</span>
          </h2>
          <div className="space-y-0 divide-y divide-gray-100">
            {faqs.map((f, i) => (
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

      {/* CTA */}
      <section className="relative py-24 px-4 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-primary to-primary-dark" />
        <div className="relative max-w-2xl mx-auto text-center">
          <h2 className="text-3xl md:text-5xl font-extrabold mb-4 text-white">
            Ready to <span className="text-amber-300">Rank Higher</span>?
          </h2>
          <p className="text-primary/80 mb-8 text-lg">
            Get a free SEO audit and discover exactly what your website needs to grow.
          </p>
          <Link href="/contact" className="group inline-flex items-center gap-2 bg-white text-primary-dark px-10 py-4 rounded-xl font-bold text-lg transition-all hover:shadow-xl hover:-translate-y-0.5">
            Start Your Free Audit
            <span className="group-hover:translate-x-1 transition-transform">→</span>
          </Link>
        </div>
      </section>

      {/* Footer */}
      <Footer />
    </div>
  );
}
