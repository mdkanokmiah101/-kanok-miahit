"use client";
import { useEffect } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import Navbar from "@/components/Navbar";
import services from "../data";

export default function ServicePage() {
  const { slug } = useParams();
  const svc = services.find((s) => s.slug === slug);

  useEffect(() => {
    if (svc) {
      document.title = `${svc.title} — Md Kanok Miah | SEO Expert in Dhaka, Bangladesh`;
    }
  }, [svc]);

  if (!svc) {
    return (
      <div className="min-h-screen bg-white text-gray-900 flex items-center justify-center flex-col gap-4">
        <h1 className="text-3xl font-bold">Service Not Found</h1>
        <p className="text-gray-600">The service page you're looking for doesn't exist.</p>
        <Link href="/services" className="text-primary hover:underline">← All Services</Link>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-white text-gray-900">
      <Navbar />

      {/* Hero */}
      <section className="relative pt-32 pb-16 px-4 overflow-hidden">
        <div className="absolute top-1/3 -left-32 w-96 h-96 bg-primary/20 rounded-full blur-3xl animate-pulse" />
        <div className="absolute bottom-1/3 -right-32 w-96 h-96 bg-primary/10 rounded-full blur-3xl animate-pulse delay-1000" />
        <div className="relative max-w-4xl mx-auto">
          <div className="inline-flex items-center gap-2 bg-primary-light border border-primary/20 text-primary text-xs font-semibold px-5 py-2 rounded-full mb-6 backdrop-blur-sm">
            {svc.icon} {svc.title}
          </div>
          <h1 className="text-4xl md:text-6xl font-extrabold leading-tight mb-6">{svc.title}</h1>
          <p className="text-lg text-gray-500 mb-3 font-medium">{svc.subtitle}</p>
          <p className="text-lg text-gray-600 max-w-3xl leading-relaxed">{svc.desc}</p>
          <div className="mt-8 flex flex-wrap gap-4">
            <Link href="/contact" className="inline-flex items-center gap-2 bg-primary hover:bg-primary-dark text-white px-6 py-3 rounded-xl font-bold text-sm transition-all hover:shadow-lg hover:-translate-y-0.5">
              Get Free SEO Audit →
            </Link>
            <Link href="/services" className="inline-flex items-center gap-2 border border-gray-200 text-gray-600 px-6 py-3 rounded-xl font-semibold text-sm hover:border-primary hover:text-primary transition-all">
              ← All Services
            </Link>
          </div>
        </div>
      </section>

      {/* Benefits */}
      <section className="py-16 px-4">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-2xl md:text-3xl font-extrabold mb-3">
            Why You Need <span className="text-primary">{svc.title}</span>
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

      {/* Full Service Description & Features */}
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

      {/* Process */}
      <section className="py-16 px-4">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-2xl md:text-3xl font-extrabold mb-3">
            My <span className="text-primary">Process</span>
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

      {/* Related Services */}
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
                <p className="text-gray-500 text-sm leading-relaxed">{related.shortDesc.slice(0, 120)}...</p>
                <div className="mt-3 text-primary text-xs font-semibold">Learn More →</div>
              </Link>
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
            Get a free SEO audit and discover exactly what your website needs to grow in Bangladesh.
          </p>
          <Link href="/contact" className="group inline-flex items-center gap-2 bg-white text-primary-dark px-10 py-4 rounded-xl font-bold text-lg transition-all hover:shadow-xl hover:-translate-y-0.5">
            Start Your Free Audit
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
