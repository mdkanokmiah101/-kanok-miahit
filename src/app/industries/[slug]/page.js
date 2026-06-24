"use client";
import { useParams } from "next/navigation";
import Link from "next/link";
import industries from "../data";

export default function IndustryPage() {
  const { slug } = useParams();
  const ind = industries.find((i) => i.slug === slug);

  if (!ind) {
    return (
      <div className="min-h-screen bg-[#0a0a0f] text-white flex items-center justify-center flex-col gap-4">
        <h1 className="text-3xl font-bold">Industry Not Found</h1>
        <p className="text-gray-400">The industry page you're looking for doesn't exist.</p>
        <Link href="/industries" className="text-cyan-400 hover:underline">← All Industries</Link>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#0a0a0f] text-white">
      {/* Navbar */}
      <nav className="fixed top-0 w-full bg-[#0a0a0f]/90 backdrop-blur-xl border-b border-white/5 z-50">
        <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
          <Link href="/" className="text-xl font-extrabold tracking-tight">
            <span className="bg-gradient-to-r from-cyan-400 to-emerald-400 bg-clip-text text-transparent">Kanok Miah</span>
            <span className="text-amber-400">IT</span>
          </Link>
          <div className="flex gap-4 text-sm">
            <Link href="/industries" className="text-gray-400 hover:text-cyan-400 transition-colors">← Industries</Link>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <section className="relative pt-32 pb-16 px-4 overflow-hidden">
        <div className="absolute top-1/3 -left-32 w-96 h-96 bg-cyan-500/20 rounded-full blur-3xl animate-pulse" />
        <div className="absolute bottom-1/3 -right-32 w-96 h-96 bg-emerald-500/20 rounded-full blur-3xl animate-pulse delay-1000" />
        <div className="relative max-w-4xl mx-auto">
          <div className="inline-flex items-center gap-2 bg-white/5 border border-white/10 text-cyan-300 text-xs font-semibold px-5 py-2 rounded-full mb-6 backdrop-blur-sm">
            {ind.icon} Industry SEO
          </div>
          <h1 className="text-4xl md:text-6xl font-extrabold leading-tight mb-6">{ind.title}</h1>
          <p className="text-lg text-gray-400 max-w-3xl leading-relaxed">{ind.desc}</p>
        </div>
      </section>

      {/* Benefits */}
      <section className="py-16 px-4">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-2xl md:text-3xl font-extrabold mb-8">
            Why You Need <span className="text-cyan-400">Industry-Specific SEO</span>
          </h2>
          <div className="grid md:grid-cols-2 gap-4">
            {ind.benefits.map((b, i) => (
              <div key={i} className="flex items-start gap-3 bg-white/[0.03] border border-white/10 rounded-xl p-5">
                <span className="text-emerald-400 text-xl mt-0.5">✓</span>
                <span className="text-gray-300">{b}</span>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Our Services for This Industry */}
      <section className="py-16 px-4 bg-white/[0.02] border-y border-white/5">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-2xl md:text-3xl font-extrabold mb-8">
            Our <span className="text-emerald-400">{ind.shortTitle}</span> SEO Services
          </h2>
          <div className="grid md:grid-cols-2 gap-4">
            {ind.services.map((s, i) => (
              <div key={i} className="flex items-center gap-3 bg-white/[0.03] border border-white/10 rounded-xl p-4">
                <span className="w-2 h-2 bg-cyan-400 rounded-full" />
                <span className="text-gray-300">{s}</span>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="relative py-24 px-4 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-cyan-600/20 via-emerald-600/20 to-amber-600/20" />
        <div className="relative max-w-2xl mx-auto text-center">
          <h2 className="text-3xl md:text-5xl font-extrabold mb-4">
            Ready to <span className="bg-gradient-to-r from-cyan-300 to-emerald-300 bg-clip-text text-transparent">Dominate</span> Your Industry?
          </h2>
          <p className="text-gray-400 mb-8 text-lg">Get a free SEO audit tailored for your industry in Bangladesh.</p>
          <Link href="/#contact" className="group inline-flex items-center gap-2 bg-gradient-to-r from-cyan-500 to-emerald-500 text-white px-10 py-4 rounded-xl font-bold text-lg transition-all hover:shadow-xl hover:shadow-cyan-500/30 hover:-translate-y-0.5">
            Get Your Free Audit
            <span className="group-hover:translate-x-1 transition-transform">→</span>
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-8 border-t border-white/5 text-center text-sm text-gray-600">
        <p>© 2026 <span className="bg-gradient-to-r from-cyan-400 to-emerald-400 bg-clip-text text-transparent font-bold">Kanok MiahIT</span> — SEO Agency in Bangladesh. All rights reserved.</p>
      </footer>
    </div>
  );
}
