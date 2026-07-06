"use client";
import Link from "next/link";
import industries from "./data";

export default function IndustriesPage() {
  return (
    <div className="min-h-screen bg-white text-gray-900">
      {/* Navbar */}
      <nav className="fixed top-0 w-full bg-white/95 backdrop-blur-xl border-b border-gray-100 z-50">
        <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
          <Link href="/" className="text-xl font-extrabold tracking-tight">
            <span className="text-blue-600">Md Kanok Miah</span>
            <span className="text-amber-500">IT</span>
          </Link>
          <Link href="/" className="text-sm text-gray-600 hover:text-blue-600 transition-colors">← Back to Home</Link>
        </div>
      </nav>

      {/* Header */}
      <section className="pt-32 pb-16 px-4 text-center relative overflow-hidden">
        <div className="absolute top-1/4 left-1/4 w-72 h-72 bg-blue-500/10 rounded-full blur-3xl" />
        <div className="relative max-w-4xl mx-auto">
          <span className="text-blue-600 text-sm font-semibold tracking-widest uppercase">Industries We Serve</span>
          <h1 className="text-4xl md:text-6xl font-extrabold mt-4 mb-6">
            SEO Solutions for{" "}
            <span className="text-blue-600">Every Industry</span>
          </h1>
          <p className="text-gray-600 text-lg max-w-2xl mx-auto">
            Tailored SEO strategies for Bangladesh's top industries. Each sector has unique challenges — we solve them.
          </p>
        </div>
      </section>

      {/* Industry Grid */}
      <section className="pb-24 px-4">
        <div className="max-w-6xl mx-auto grid md:grid-cols-2 lg:grid-cols-3 gap-5">
          {industries.map((ind, i) => (
            <Link key={i} href={`/industries/${ind.slug}`} className="group bg-gray-50 border border-gray-100 rounded-2xl p-7 hover:bg-gray-100 hover:border-blue-200 hover:-translate-y-1 transition-all">
              <div className="text-4xl mb-4">{ind.icon}</div>
              <h3 className="font-bold text-lg text-gray-900 mb-2 group-hover:text-blue-600 transition-colors">{ind.shortTitle}</h3>
              <p className="text-gray-600 text-sm leading-relaxed">{ind.desc.slice(0, 160)}...</p>
              <div className="mt-4 text-blue-600 text-sm font-semibold group-hover:translate-x-1 transition-transform">
                Learn More →
              </div>
            </Link>
          ))}
        </div>
      </section>

      {/* Footer */}
      <footer className="py-8 border-t border-gray-100 text-center text-sm text-gray-500">
        <p>© 2026 <span className="text-blue-600 font-bold">Kanok MiahIT</span> — SEO Agency in Bangladesh. All rights reserved.</p>
      </footer>
    </div>
  );
}
