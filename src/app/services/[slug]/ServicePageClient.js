"use client";
import Link from "next/link";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import services from "../data";
import { FAQSchema } from "@/components/Schema";

export default function ServicePageClient({ slug }) {
  const svc = services.find((s) => s.slug === slug);

  if (!svc) {
    return (
      <div className="min-h-screen bg-white text-gray-900 flex items-center justify-center flex-col gap-4">
        <h1 className="text-3xl font-bold">Service Not Found</h1>
        <p className="text-gray-600">The service page you're looking for doesn't exist.</p>
        <Link href="/services" className="text-primary hover:underline">← All Services</Link>
      </div>
    );
  }

  const breadcrumbItems = [
    { name: "Home", url: "https://kanokmiah.com.bd" },
    { name: "Services", url: "https://kanokmiah.com.bd/services" },
    { name: svc.title, url: `https://kanokmiah.com.bd/services/${svc.slug}` },
  ];

  const faqs = (svc.faq && svc.faq.length > 0) ? svc.faq : [
    { question: `How long does ${svc.title} take to show results?`, answer: `Most ${svc.title.toLowerCase()} efforts show initial improvements within 4–8 weeks, with significant results building over 3–6 months of consistent optimization.` },
    { question: `Do you offer ${svc.title} for Chittagong?`, answer: `Yes, I provide ${svc.title.toLowerCase()} services for all of Bangladesh including Dhaka, Chittagong, Sylhet, and Khulna with strategies tailored to each market.` },
    { question: "Are your SEO methods white-hat and Google-compliant?", answer: "Absolutely. All my SEO strategies strictly follow Google's Webmaster Guidelines. I use only ethical, sustainable techniques that build long-term organic growth." },
    { question: "Do you provide monthly reports?", answer: "Yes, I provide detailed monthly reports showing keyword rankings, organic traffic, backlink growth, and key performance metrics." },
    { question: "How do I get started with SEO for my Bangladesh business?", answer: "Contact me for a free SEO audit where I analyze your current website, identify opportunities, and provide a customized strategy proposal with transparent pricing." },
  ];

  return (
    <div className="min-h-screen bg-white text-gray-900">
      <Navbar />

      <div className="pt-24 px-4 max-w-4xl mx-auto">
        <nav className="flex items-center gap-2 text-sm text-gray-500 py-3">
          <Link href="/" className="hover:text-primary transition-colors">Home</Link>
          <span className="text-gray-300">›</span>
          <Link href="/services" className="hover:text-primary transition-colors">Services</Link>
          <span className="text-gray-300">›</span>
          <span className="text-gray-800 font-medium">{svc.title}</span>
        </nav>
      </div>

      <section className="relative pt-8 pb-16 px-4 overflow-hidden">
        <div className="absolute top-1/3 -left-32 w-96 h-96 bg-primary/20 rounded-full blur-3xl animate-pulse" />
        <div className="absolute bottom-1/3 -right-32 w-96 h-96 bg-primary/10 rounded-full blur-3xl animate-pulse delay-1000" />
        <div className="relative max-w-4xl mx-auto">
          <div className="inline-flex items-center gap-2 bg-primary/10 border border-primary/20 text-primary text-xs font-semibold px-4 py-2 rounded-full mb-6">
            <span className="w-2 h-2 bg-primary rounded-full animate-pulse" />
            {svc.icon} {svc.title}
          </div>
          <h1 className="text-4xl md:text-6xl font-extrabold leading-tight mb-6">
            <span className="text-primary">{svc.title}</span><br/>
            <span className="text-gray-900">in Dhaka, Bangladesh</span>
          </h1>
          <p className="text-lg text-gray-600 max-w-3xl leading-relaxed">
            {svc.desc} As the{" "}
            <Link href="/" className="text-primary font-semibold hover:underline">
              best SEO expert in Dhaka
            </Link>
            , I deliver tailored strategies that drive real results for your business.
          </p>
          <div className="mt-4 flex flex-wrap items-center gap-3">
            <span className="inline-flex items-center gap-1.5 bg-blue-50 border border-blue-200 text-blue-700 text-xs font-medium px-4 py-2 rounded-full">✅ Expert Reviewed</span>
            <span className="text-xs text-gray-400">This guide was reviewed by Kanok Miah, SEO expert since 2019.</span>
          </div>
          <div className="mt-6 flex flex-wrap gap-4">
            <Link href="/contact" className="inline-flex items-center gap-2 bg-primary hover:bg-primary-dark text-white px-6 py-3 rounded-xl font-bold text-sm transition-all hover:shadow-lg hover:-translate-y-0.5">
              Get Free SEO Audit →
            </Link>
            <Link href="/services" className="inline-flex items-center gap-2 border border-gray-200 text-gray-600 px-6 py-3 rounded-xl font-semibold text-sm hover:border-primary hover:text-primary transition-all">
              ← All Services
            </Link>
          </div>
        </div>
      </section>

      {svc.qa && (
        <section className="px-4">
          <div className="max-w-4xl mx-auto">
            <div className="bg-primary-light border border-primary/20 rounded-xl p-5 mb-8">
              <p className="text-sm font-bold text-primary mb-1">⚡ Quick Answer</p>
              <p className="text-gray-700">{svc.qa}</p>
            </div>
          </div>
        </section>
      )}

      <section className="py-16 px-4">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-2xl md:text-3xl font-extrabold mb-3">
            Why You Need <span className="text-primary">{svc.title}</span> for Better Rankings
          </h2>
          <p className="text-gray-500 mb-8">The key benefits of professional SEO for your Bangladesh business.</p>
          <div className="grid md:grid-cols-2 gap-4">
            {svc.benefits.map((b, i) => (
              <div key={i} className="flex items-start gap-3 bg-gray-50 border border-gray-100 rounded-xl p-5">
                <span className="text-primary text-xl mt-0.5">✓</span>
                <span className="text-gray-600">{b}</span>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="py-16 px-4 bg-gray-50/80 border-y border-gray-100">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-2xl md:text-3xl font-extrabold mb-8">
            What&apos;s Included in <span className="text-primary">{svc.title}</span>
          </h2>
          <p className="text-gray-600 mb-8 leading-relaxed">{svc.desc}</p>
          <div className="grid md:grid-cols-2 gap-4">
            {svc.features.map((f, i) => (
              <div key={i} className="flex items-start gap-3 bg-white border border-gray-100 rounded-xl p-4">
                <span className="w-5 h-5 bg-primary rounded-full flex items-center justify-center text-white text-xs shrink-0 mt-0.5">✓</span>
                <span className="text-gray-600 text-sm">{f}</span>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="py-16 px-4">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-2xl md:text-3xl font-extrabold mb-3">
            My <span className="text-primary">SEO Process</span> for {svc.title}
          </h2>
          <p className="text-gray-500 mb-8">How I deliver results for {svc.title}.</p>
          <div className="space-y-4">
            {svc.process.map((step, i) => (
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

      <section className="py-16 px-4 bg-gray-50/80 border-y border-gray-100">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-2xl md:text-3xl font-extrabold text-center mb-10">
            Other <span className="text-primary">SEO Services</span>
          </h2>
          <div className="grid md:grid-cols-3 gap-4">
            {services.filter((s) => s.slug !== svc.slug).slice(0, 3).map((related, i) => (
              <Link key={i} href={`/services/${related.slug}`} className="group bg-white border border-gray-100 rounded-2xl p-6 hover:border-primary/20 hover:shadow-lg hover:-translate-y-1 transition-all">
                <div className="text-4xl mb-3">{related.icon}</div>
                <h3 className="font-bold text-gray-900 mb-2 group-hover:text-primary transition-colors">{related.title}</h3>
                <p className="text-gray-500 text-sm leading-relaxed">{related.shortDesc?.slice(0, 120)}...</p>
                <div className="mt-3 text-primary text-xs font-semibold">Learn More →</div>
              </Link>
            ))}
          </div>
        </div>
      </section>

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
          <div className="mt-10 text-center">
            <Link href="/industries" className="inline-flex items-center gap-2 text-primary font-semibold hover:text-primary-dark transition-colors text-sm">
              See which industries we serve →
            </Link>
          </div>
        </div>
      </section>

      <div className="bg-gray-50 border-y border-gray-100 py-12 px-4">
        <div className="max-w-4xl mx-auto flex items-start gap-6">
          <div className="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center text-2xl shrink-0">👤</div>
          <div>
            <p className="font-bold text-gray-900">Written by <span className="text-primary">Kanok Miah</span></p>
            <p className="text-sm text-gray-500">SEO Expert since 2019, helping Bangladeshi businesses rank higher on Google.</p>
            <p className="text-xs text-gray-400 mt-2">Last updated: July 2026</p>
          </div>
        </div>
      </div>

      <section className="relative py-24 px-4 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-primary to-primary-dark" />
        <div className="relative max-w-2xl mx-auto text-center">
          <h2 className="text-3xl md:text-5xl font-extrabold mb-4 text-white">
            Ready to <span className="text-amber-300">Rank Higher</span>?
          </h2>
          <p className="text-white/80 mb-8 text-lg">
            Get a free SEO audit and discover exactly what your website needs to grow in Bangladesh.
          </p>
          <Link href="/contact" className="group inline-flex items-center gap-2 bg-white text-primary-dark px-10 py-4 rounded-xl font-bold text-lg transition-all hover:shadow-xl hover:-translate-y-0.5">
            Start Your Free Audit
            <span className="group-hover:translate-x-1 transition-transform">→</span>
          </Link>
        </div>
      </section>

      <Footer />
    </div>
  );
}
