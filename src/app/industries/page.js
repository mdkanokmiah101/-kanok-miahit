"use client";
import Link from "next/link";
import industries from "./data";

export default function IndustriesPage() {
  return (
    <div className="min-h-screen bg-[#0a0a0f] text-white">
      {/* Navbar */}
      <nav className="fixed top-0 w-full bg-[#0a0a0f]/90 backdrop-blur-xl border-b border-white/5 z-50">
        <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
          <Link href="/" className="text-xl font-extrabold tracking-tight">
            <span className="bg-gradient-to-r from-cyan-400 to-emerald-400 bg-clip-text text-transparent">Kanok Miah</span>
            <span className="text-amber-400">IT</span>
          </Link>
          <Link href="/" className="text-sm text-gray-400 hover:text-cyan-400 transition-colors">← Back to Home</Link>
        </div>
      </nav>

      {/* Header */}
      <section className="pt-32 pb-16 px-4 text-center">
        <div className="absolute top-1/4 left-1/4 w-72 h-72 bg-cyan-500/10 rounded-full blur-3xl" />
        <div className="relative max-w-4xl mx-auto">
          <span className="text-cyan-400 text-sm font-semibold tracking-widest uppercase">Industries We Serve</span>
          <h1 className="text-4xl md:text-6xl font-extrabold mt-4 mb-6">
            SEO Solutions for{" "}
            <span className="bg-gradient-to-r from-cyan-300 to-emerald-300 bg-clip-text text-transparent">Every Industry</span>
          </h1>
          <p className="text-gray-400 text-lg max-w-2xl mx-auto">
            Tailored SEO strategies for Bangladesh's top industries. Each sector has unique challenges — we solve them.
          </p>
        </div>
      </section>

      {/* Industry Grid */}
      <section className="pb-24 px-4">
        <div className="max-w-6xl mx-auto grid md:grid-cols-2 lg:grid-cols-3 gap-5">
          {industries.map((ind, i) => (
            <Link key={i} href={`/industries/${ind.slug}`} className="group bg-white/[0.03] border border-white/10 rounded-2xl p-7 hover:bg-white/[0.06] hover:border-cyan-500/30 hover:-translate-y-1 transition-all">
              <div className="text-4xl mb-4">{ind.icon}</div>
              <h3 className="font-bold text-lg text-white mb-2 group-hover:text-cyan-300 transition-colors">{ind.shortTitle}</h3>
              <p className="text-gray-400 text-sm leading-relaxed">{ind.desc.slice(0, 160)}...</p>
              <div className="mt-4 text-cyan-400 text-sm font-semibold group-hover:translate-x-1 transition-transform">
                Learn More →
              </div>
            </Link>
          ))}
        </div>
      </section>

      {/* Footer */}
      <footer className="py-8 border-t border-white/5 text-center text-sm text-gray-600">
        <p>© 2026 <span className="bg-gradient-to-r from-cyan-400 to-emerald-400 bg-clip-text text-transparent font-bold">Kanok MiahIT</span> — SEO Agency in Bangladesh. All rights reserved.</p>
      </footer>
    </div>
  );
}
