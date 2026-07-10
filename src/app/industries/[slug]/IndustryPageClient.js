"use client";

import Navbar from "@/components/Navbar";
import Link from "next/link";
import industries from "../data";

export default function IndustryPageClient({ slug }) {
  const ind = industries.find((i) => i.slug === slug);

  if (!ind) {
    return (
      <div className="min-h-screen bg-white text-gray-900 flex flex-col items-center justify-center">
        <Navbar />
        <div className="text-center pt-32 pb-16 px-4">
          <div className="text-6xl mb-6">🔍</div>
          <h1 className="text-3xl md:text-5xl font-extrabold mb-4">Industry Not Found</h1>
          <p className="text-gray-500 text-lg max-w-md mx-auto mb-8">
            The industry page you're looking for doesn't exist.
          </p>
          <Link
            href="/industries"
            className="inline-flex items-center gap-2 text-primary font-semibold hover:text-primary-dark transition-colors"
          >
            ← All Industries
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-white text-gray-900">
      <Navbar />

      {/* Hero Section */}
      <section className="relative pt-32 pb-16 px-4 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-primary/[0.07] via-white to-primary/[0.04]" />
        <div className="absolute top-1/4 -left-32 w-[400px] h-[400px] bg-primary/20 rounded-full blur-[120px]" />
        <div className="relative max-w-4xl mx-auto text-center">
          <div className="text-6xl mb-6">{ind.icon}</div>
          <h1 className="text-3xl md:text-5xl lg:text-6xl font-extrabold tracking-tight mb-6">
            <span className="text-primary">{ind.title}</span><br/>
            <span className="text-gray-900">SEO Solutions in Dhaka, Bangladesh</span>
          </h1>
          <p className="text-lg text-gray-600 max-w-3xl mx-auto leading-relaxed">
            {ind.desc} As a <Link href="/" className="text-primary font-semibold hover:underline">best SEO expert in Dhaka</Link>, I deliver tailored results for this industry.
          </p>
          <div className="mt-8 flex flex-wrap justify-center gap-4">
            <a
              href="/#contact"
              className="inline-flex items-center gap-2 bg-primary hover:bg-primary-dark text-white px-8 py-3.5 rounded-xl font-bold text-base transition-all hover:shadow-xl hover:shadow-primary/30 hover:-translate-y-0.5"
            >
              Get SEO for Your Business →
            </a>
            <Link
              href="/services"
              className="inline-flex items-center gap-2 border-2 border-gray-200 text-gray-700 px-8 py-3.5 rounded-xl font-semibold text-base hover:border-primary/30 hover:text-primary transition-all"
            >
              View SEO Services
            </Link>
          </div>
        </div>
      </section>

      {/* Benefits Section */}
      <section className="py-20 px-4 bg-gray-50/80">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-12">
            <span className="text-primary text-sm font-semibold tracking-[0.2em] uppercase">
              Why You Need This
            </span>
            <h2 className="text-2xl md:text-4xl font-extrabold mt-3 mb-4 text-gray-900">
              Benefits of SEO for{" "}
              <span className="text-primary">{ind.shortTitle}</span>
            </h2>
          </div>
          <div className="grid md:grid-cols-2 gap-5">
            {ind.benefits.map((benefit, i) => (
              <div
                key={i}
                className="bg-white rounded-2xl p-6 border border-gray-100 hover:border-primary/20 hover:shadow-md transition-all flex items-start gap-4"
              >
                <div className="w-10 h-10 rounded-xl bg-primary/10 flex items-center justify-center text-lg shrink-0 mt-0.5">
                  ✅
                </div>
                <p className="text-gray-700 font-medium">{benefit}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Services Section */}
      <section className="py-20 px-4">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-12">
            <span className="text-primary text-sm font-semibold tracking-[0.2em] uppercase">
              What We Deliver
            </span>
            <h2 className="text-2xl md:text-4xl font-extrabold mt-3 mb-4 text-gray-900">
              SEO Services for{" "}
              <span className="text-primary">{ind.shortTitle}</span>
            </h2>
            <p className="text-gray-500 max-w-2xl mx-auto">
              Tailored SEO solutions designed specifically for the{" "}
              {ind.shortTitle.toLowerCase()} industry in Bangladesh.
            </p>
          </div>
          <div className="grid md:grid-cols-2 gap-4">
            {ind.services.map((service, i) => {
              const slugMap = {
                "Local SEO": "/services/local-seo",
                "On-Page SEO": "/services/on-page-seo",
                "Technical SEO": "/services/technical-seo",
                "Link Building": "/services/link-building",
                "GEO / AI Search": "/services/geo-ai-search",
                "E-commerce SEO": "/services/ecommerce-seo",
                "Semantic SEO": "/services/semantic-seo",
              };
              const match = Object.keys(slugMap).find((k) =>
                service.toLowerCase().includes(k.toLowerCase())
              );
              const href = match ? slugMap[match] : "/services";
              return (
                <Link
                  key={i}
                  href={href}
                  className="group bg-gray-50 border border-gray-100 rounded-xl px-6 py-5 hover:bg-white hover:border-primary/20 hover:shadow-md hover:-translate-y-0.5 transition-all flex items-center gap-3"
                >
                  <div className="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center text-base shrink-0 group-hover:bg-primary group-hover:text-white transition-all">
                    {i + 1}
                  </div>
                  <span className="text-gray-700 font-medium group-hover:text-gray-900 transition-colors">
                    {service}
                  </span>
                </Link>
              );
            })}
          </div>
        </div>
      </section>

      {/* FAQ */}
      <section className="py-16 px-4 bg-white">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-2xl md:text-3xl font-extrabold text-center mb-8">
            Frequently Asked <span className="text-primary">Questions</span>
          </h2>
          <div className="space-y-0 divide-y divide-gray-100">
            {[
              { question: "How does SEO work for this industry?", answer: "SEO for each industry requires a tailored approach. I analyze industry-specific search patterns, competitor strategies, and customer intent to create a customized optimization plan that targets the right keywords and delivers qualified traffic." },
              { question: "How long before I see results?", answer: "SEO results typically become visible within 3–6 months, depending on competition, current website state, and the aggressiveness of the strategy. Some improvements, like technical fixes, can show impact sooner — within 4–8 weeks." },
              { question: "What makes your approach different?", answer: "My approach combines deep local Bangladesh market knowledge with global SEO best practices. I focus on data-driven strategies, transparent reporting, and long-term sustainable growth rather than quick fixes that risk penalties." },
              { question: "Do you have case studies for this industry?", answer: "Yes, I have successfully worked with clients across various industries. Contact me to discuss case studies relevant to your specific industry. I'm happy to share examples of past results and client testimonials." },
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

      {/* CTA Section */}
      <section className="relative py-20 px-4 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-primary to-primary-dark" />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] bg-white/10 rounded-full blur-[100px]" />
        <div className="relative max-w-2xl mx-auto text-center">
          <h2 className="text-3xl md:text-4xl font-extrabold mb-4 text-white">
            Ready to Dominate Search Results in{" "}
            <span className="text-amber-300">{ind.shortTitle}</span>?
          </h2>
          <p className="text-primary/80 mb-8 text-lg max-w-xl mx-auto">
            Get a free SEO audit for your {ind.shortTitle.toLowerCase()} business. No commitment. Just real, actionable insights.
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <a
              href="/#contact"
              className="inline-flex items-center gap-2 bg-white text-primary-dark px-10 py-4 rounded-xl font-bold text-lg transition-all hover:shadow-xl hover:-translate-y-0.5"
            >
              Get Your Free Audit →
            </a>
            <Link
              href="/industries"
              className="inline-flex items-center gap-2 border-2 border-white/30 text-white px-10 py-4 rounded-xl font-bold text-lg hover:bg-white/10 transition-all"
            >
              ← All Industries
            </Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-8 border-t border-gray-100 text-center text-sm text-gray-500">
        <p>
          © 2026 <span className="text-primary font-bold">Md Kanok Miah</span> — SEO Expert in
          Bangladesh. All rights reserved.
        </p>
      </footer>
    </div>
  );
}
