"use client";

import Navbar from "@/components/Navbar";
import Link from "next/link";
import { FAQSchema } from "@/components/Schema";
import industries from "./data";

export default function IndustriesClient() {

  return (
    <div className="min-h-screen bg-white text-gray-900">
      <head>
        <link rel="canonical" href="https://kanokmiah.com.bd/industries" />
        <meta name="robots" content="index, follow" />
      </head>
      {/* Navbar */}
      <Navbar />

      {/* Header */}
      <section className="pt-32 pb-16 px-4 text-center relative overflow-hidden">
        <div className="absolute top-1/4 left-1/4 w-72 h-72 bg-primary/10 rounded-full blur-3xl" />
        <div className="relative max-w-4xl mx-auto">
          <span className="text-primary text-sm font-semibold tracking-widest uppercase">Industries We Serve</span>
          <h1 className="text-4xl md:text-6xl font-extrabold mt-4 mb-6">
            Industry-Specific <span className="text-primary">SEO Solutions</span> for Bangladesh
          </h1>
          <p className="text-gray-600 text-lg max-w-2xl mx-auto">
            Tailored SEO strategies for Bangladesh's top industries. Each sector has unique challenges — we solve them.
          </p>
        </div>
      </section>

      {/* Industry Grid */}
      <section className="pb-24 px-4">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-2xl md:text-3xl font-extrabold text-center mb-10">
            Industries We Serve with <span className="text-primary">Custom SEO Strategies</span>
          </h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-5">
          {industries.map((ind, i) => (
            <Link key={i} href={`/industries/${ind.slug}`} className="group bg-gray-50 border border-gray-100 rounded-2xl p-7 hover:bg-gray-100 hover:border-primary/20 hover:-translate-y-1 transition-all">
              <div className="text-4xl mb-4">{ind.icon}</div>
              <h3 className="font-bold text-lg text-gray-900 mb-2 group-hover:text-primary transition-colors">{ind.shortTitle}</h3>
              <p className="text-gray-600 text-sm leading-relaxed">{ind.desc.slice(0, 160)}...</p>
              <div className="mt-4 text-primary text-sm font-semibold group-hover:translate-x-1 transition-transform">
                Learn More →
              </div>
            </Link>
          ))}
        </div>
        </div>
      </section>

      {/* FAQ */}
      <section className="py-16 px-4 bg-white">
        <div className="max-w-4xl mx-auto">
          {FAQSchema([
            { question: "Which industries do you specialize in for SEO?", answer: "I specialize in SEO for a wide range of industries including real estate, e-commerce, healthcare, education, hospitality, local services, and manufacturing. Each industry strategy is tailored to its unique competitive landscape and customer search behaviour." },
            { question: "Do you offer industry-specific SEO strategies?", answer: "Yes, every industry has unique search patterns, customer journeys, and competitive dynamics. I create customized SEO strategies that address the specific challenges and opportunities of each industry sector." },
            { question: "How is SEO different for e-commerce vs local service businesses?", answer: "E-commerce SEO focuses on product page optimization, category structure, faceted navigation, and review signals. Local service SEO emphasizes Google Business Profile optimization, local citations, and near-me keyword targeting. Both require different technical and content approaches." },
            { question: "Can you optimize for both B2B and B2C companies?", answer: "Absolutely. B2B SEO focuses on informational content, long-form guides, and lead generation through thought leadership. B2C SEO targets transactional keywords, local intent, and conversion optimization. I tailor my approach based on your business model." },
            { question: "Do you understand the Bangladesh-specific challenges for each industry?", answer: "Yes, I deeply understand Bangladesh's unique digital landscape — mobile-first usage patterns, bilingual search behaviour (Bengali + English), local competition dynamics, and industry-specific regulations that affect SEO strategies in each sector." },
          ])}
          <h2 className="text-2xl md:text-3xl font-extrabold text-center mb-8">
            Frequently Asked <span className="text-primary">Questions</span>
          </h2>
          <div className="space-y-0 divide-y divide-gray-100">
            {[
              { question: "Which industries do you specialize in for SEO?", answer: "I specialize in SEO for a wide range of industries including real estate, e-commerce, healthcare, education, hospitality, local services, and manufacturing. Each industry strategy is tailored to its unique competitive landscape and customer search behaviour." },
              { question: "Do you offer industry-specific SEO strategies?", answer: "Yes, every industry has unique search patterns, customer journeys, and competitive dynamics. I create customized SEO strategies that address the specific challenges and opportunities of each industry sector." },
              { question: "How is SEO different for e-commerce vs local service businesses?", answer: "E-commerce SEO focuses on product page optimization, category structure, faceted navigation, and review signals. Local service SEO emphasizes Google Business Profile optimization, local citations, and near-me keyword targeting. Both require different technical and content approaches." },
              { question: "Can you optimize for both B2B and B2C companies?", answer: "Absolutely. B2B SEO focuses on informational content, long-form guides, and lead generation through thought leadership. B2C SEO targets transactional keywords, local intent, and conversion optimization. I tailor my approach based on your business model." },
              { question: "Do you understand the Bangladesh-specific challenges for each industry?", answer: "Yes, I deeply understand Bangladesh's unique digital landscape — mobile-first usage patterns, bilingual search behaviour (Bengali + English), local competition dynamics, and industry-specific regulations that affect SEO strategies in each sector." },
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

      {/* Cross-Link to Services */}
      <section className="py-16 px-4 bg-gradient-to-r from-primary to-primary-dark">
        <div className="max-w-2xl mx-auto text-center">
          <h2 className="text-2xl md:text-4xl font-extrabold mb-4 text-white">
            Need SEO Tailored for Your Industry?
          </h2>
          <p className="text-primary/80 mb-6 max-w-xl mx-auto">
            Explore all our SEO services — from local SEO to technical optimization — and find the perfect strategy for your business.
          </p>
          <Link
            href="/services"
            className="inline-flex items-center gap-2 bg-white text-primary-dark px-8 py-3.5 rounded-xl font-bold text-base hover:shadow-xl hover:-translate-y-0.5 transition-all"
          >
            View All SEO Services →
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-8 border-t border-gray-100 text-center text-sm text-gray-500">
        <p>© 2026 <span className="text-primary font-bold">Md Kanok Miah</span> — SEO Expert in Bangladesh. All rights reserved.</p>
      </footer>
    </div>
  );
}
