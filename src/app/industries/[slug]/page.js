"use client";
import { useParams } from "next/navigation";
import Link from "next/link";
import industries from "../data";

export default function IndustryPage() {
  const { slug } = useParams();
  const ind = industries.find((i) => i.slug === slug);

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
      {/* Navbar */}
      <nav className="fixed top-0 w-full bg-white/95 backdrop-blur-xl border-b border-gray-100 z-50">
        <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
          <Link href="/" className="text-xl font-extrabold tracking-tight">
            <span className="text-primary">Md Kanok Miah</span>
          </Link>
          <div className="flex gap-4 text-sm">
            <Link href="/industries" className="text-gray-600 hover:text-primary transition-colors">← Industries</Link>
          </div>
        </div>
      </nav>

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
