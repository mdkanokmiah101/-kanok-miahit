"use client";
import { useEffect } from "react";
import { useParams } from "next/navigation";
import Navbar from "@/components/Navbar";
import Link from "next/link";
import industries from "../data";
import { BreadcrumbSchema } from "@/components/Schema";

export default function IndustryPage() {
  const { slug } = useParams();
  const ind = industries.find((i) => i.slug === slug);

  useEffect(() => {
    if (ind) {
      document.title = `${ind.title} SEO — Md Kanok Miah | Industry SEO Expert in Bangladesh`;
    }
  }, [ind]);

  if (!ind) {
    return (
      <div className="min-h-screen bg-white text-gray-900 flex items-center justify-center flex-col gap-4">
        <h1 className="text-3xl font-bold">Industry Not Found</h1>
        <p className="text-gray-600">The industry page you're looking for doesn't exist.</p>
        <Link href="/industries" className="text-primary hover:underline">← All Industries</Link>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-white text-gray-900">
      <head>
        <link rel="canonical" href={`https://kanokmiah.com.bd/industries/${ind.slug}`} />
        <meta name="robots" content="index, follow" />
        {BreadcrumbSchema([
          { name: "Home", url: "https://kanokmiah.com.bd" },
          { name: "Industries", url: "https://kanokmiah.com.bd/industries" },
          { name: ind.title, url: `https://kanokmiah.com.bd/industries/${ind.slug}` },
        ])}
      </head>
      {/* Navbar */}
      <Navbar />

      {/* Hero */}
      <section className="relative pt-32 pb-16 px-4 overflow-hidden">
        <div className="absolute top-1/3 -left-32 w-96 h-96 bg-primary/20 rounded-full blur-3xl animate-pulse" />
        <div className="absolute bottom-1/3 -right-32 w-96 h-96 bg-primary/20 rounded-full blur-3xl animate-pulse delay-1000" />
        <div className="relative max-w-4xl mx-auto">
          <div className="inline-flex items-center gap-2 bg-primary-light border border-primary/20 text-primary text-xs font-semibold px-5 py-2 rounded-full mb-6 backdrop-blur-sm">
            {ind.icon} Industry SEO
          </div>
          <h1 className="text-4xl md:text-6xl font-extrabold leading-tight mb-6">{ind.title}</h1>
          <p className="text-lg text-gray-600 max-w-3xl leading-relaxed">{ind.desc}</p>
        </div>
      </section>

      {/* Benefits */}
      <section className="py-16 px-4">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-2xl md:text-3xl font-extrabold mb-8">
            Why You Need <span className="text-primary">Industry-Specific SEO</span>
          </h2>
          <div className="grid md:grid-cols-2 gap-4">
            {ind.benefits.map((b, i) => (
              <div key={i} className="flex items-start gap-3 bg-gray-50 border border-gray-100 rounded-xl p-5">
                <span className="text-primary text-xl mt-0.5">✓</span>
                <span className="text-gray-600">{b}</span>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Our Services for This Industry */}
      <section className="py-16 px-4 bg-gray-50 border-y border-gray-100">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-2xl md:text-3xl font-extrabold mb-8">
            Our <span className="text-primary">{ind.shortTitle}</span> SEO Services
          </h2>
          <div className="grid md:grid-cols-2 gap-4">
            {ind.services.map((s, i) => (
              <div key={i} className="flex items-center gap-3 bg-gray-50 border border-gray-100 rounded-xl p-4">
                <span className="w-2 h-2 bg-primary-light0 rounded-full" />
                <span className="text-gray-600">{s}</span>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Process */}
      <section className="py-16 px-4">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-2xl md:text-3xl font-extrabold mb-3">
            My <span className="text-primary">SEO Process</span> for {ind.shortTitle}
          </h2>
          <p className="text-gray-500 mb-8">A proven methodology to drive results in the {ind.shortTitle.toLowerCase()} industry.</p>
          <div className="space-y-4">
            {[
              "Audit: Comprehensive analysis of your current website, competitors, and industry keywords",
              "Strategy: Custom SEO plan tailored to the {ind.shortTitle} industry landscape",
              "Execution: On-page optimization, content creation, technical fixes, and link building",
              "Monitoring: Weekly ranking and traffic tracking with detailed performance dashboards",
              "Optimization: Data-driven refinements to maximize ROI and long-term growth",
            ].map((step, i) => (
              <div key={i} className="flex items-start gap-4 bg-gray-50 border border-gray-100 rounded-xl p-5">
                <div className="w-10 h-10 rounded-xl bg-primary flex items-center justify-center font-extrabold text-sm text-white shrink-0">
                  {String(i + 1).padStart(2, "0")}
                </div>
                <div>
                  <p className="text-gray-600">{step}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* FAQ */}
      <section className="py-16 px-4 bg-gray-50/80 border-y border-gray-100">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-2xl md:text-3xl font-extrabold text-center mb-8">
            Frequently Asked <span className="text-primary">Questions</span> About {ind.shortTitle} SEO
          </h2>
          <div className="space-y-0 divide-y divide-gray-100 bg-white rounded-2xl p-6">
            {[
              { q: `How long does SEO take for ${ind.shortTitle.toLowerCase()} businesses?`, a: `SEO for the ${ind.shortTitle.toLowerCase()} industry typically shows initial results within 4-8 weeks, with significant ranking improvements in 3-6 months. Timeline depends on competition, current site health, and the scope of optimization needed.` },
              { q: `What makes ${ind.shortTitle.toLowerCase()} SEO different from general SEO?`, a: `${ind.shortTitle} businesses face unique search patterns, customer behavior, and competitive dynamics. My industry-specific approach addresses these nuances with tailored keyword research, content strategy, and technical optimization that general SEO cannot provide.` },
              { q: "Do you offer customized SEO packages?", a: "Yes, every SEO package is customized based on your specific business goals, target audience, industry competition, and budget. Contact me for a free consultation and personalized proposal." },
              { q: "How do you track and report results?", a: "I provide detailed monthly reports showing keyword rankings, organic traffic, conversion metrics, backlink growth, and actionable recommendations. You'll always know exactly how your SEO investment is performing." },
            ].map((faq, i) => (
              <details key={i} className="py-4 group">
                <summary className="font-semibold text-gray-900 cursor-pointer list-none flex justify-between items-center">
                  {faq.q}
                  <span className="text-primary transition-transform group-open:rotate-180">▼</span>
                </summary>
                <p className="text-gray-600 mt-3 pl-2">{faq.a}</p>
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
            Ready to <span className="text-amber-300">Dominate</span> Your Industry?
          </h2>
          <p className="text-primary/80 mb-8 text-lg">Get a free SEO audit tailored for your industry in Bangladesh.</p>
          <Link href="/#contact" className="group inline-flex items-center gap-2 bg-white text-primary-dark px-10 py-4 rounded-xl font-bold text-lg transition-all hover:shadow-xl hover:-translate-y-0.5">
            Get Your Free Audit
            <span className="group-hover:translate-x-1 transition-transform">→</span>
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
