"use client";
import { useState, useEffect } from "react";
import Link from "next/link";
import posts from "./data";

const POSTS_PER_PAGE = 6;

export default function BlogPage() {
  const [currentPage, setCurrentPage] = useState(1);
  const totalPages = Math.ceil(posts.length / POSTS_PER_PAGE);
  const startIndex = (currentPage - 1) * POSTS_PER_PAGE;
  const currentPosts = posts.slice(startIndex, startIndex + POSTS_PER_PAGE);

  useEffect(() => {
    document.title =
      "SEO Blog — Kanok MiahIT | Bangladesh Digital Marketing Tips";
    const metaDesc = document.querySelector('meta[name="description"]');
    if (metaDesc) {
      metaDesc.setAttribute(
        "content",
        "Expert SEO tips, guides, and strategies for Bangladesh businesses. Learn local SEO, technical SEO, e-commerce SEO, GEO optimization, and more from Kanok MiahIT."
      );
    }
  }, []);

  return (
    <div className="min-h-screen bg-white text-gray-900">
      {/* Navbar */}
      <nav className="fixed top-0 w-full bg-white/95 backdrop-blur-xl border-b border-gray-100 z-50">
        <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
          <Link href="/" className="text-xl font-extrabold tracking-tight">
            <span className="text-blue-600">
              Kanok Miah
            </span>
            <span className="text-amber-500">IT</span>
          </Link>
          <Link
            href="/"
            className="text-sm text-gray-600 hover:text-blue-600 transition-colors"
          >
            ← Back to Home
          </Link>
        </div>
      </nav>

      {/* Header */}
      <section className="relative pt-32 pb-16 px-4 text-center overflow-hidden">
        <div className="absolute top-1/4 left-1/4 w-72 h-72 bg-blue-500/10 rounded-full blur-3xl" />
        <div className="absolute bottom-1/4 right-1/4 w-72 h-72 bg-blue-500/10 rounded-full blur-3xl" />
        <div className="relative max-w-4xl mx-auto">
          <span className="text-blue-600 text-sm font-semibold tracking-widest uppercase">
            Our Blog
          </span>
          <h1 className="text-4xl md:text-6xl font-extrabold mt-4 mb-6">
            SEO Insights for{" "}
            <span className="text-blue-600">
              Bangladesh
            </span>
          </h1>
          <p className="text-gray-600 text-lg max-w-2xl mx-auto">
            Expert SEO tips, guides, and strategies tailored for Bangladeshi
            businesses. Learn how to rank higher, attract more customers, and
            grow your online presence.
          </p>
        </div>
      </section>

      {/* Blog Grid */}
      <section className="pb-16 px-4">
        <div className="max-w-6xl mx-auto grid md:grid-cols-2 lg:grid-cols-3 gap-5">
          {currentPosts.map((post, i) => (
            <Link
              key={i}
              href={`/blog/${post.slug}`}
              className="group bg-gray-50 border border-gray-100 rounded-2xl p-7 hover:bg-gray-100 hover:border-blue-200 hover:-translate-y-1 transition-all flex flex-col"
            >
              <div className="text-4xl mb-4">{post.imagePlaceholder}</div>
              <div className="flex flex-wrap gap-2 mb-3">
                {post.tags.slice(0, 2).map((tag, ti) => (
                  <span
                    key={ti}
                    className="text-xs font-medium text-blue-600/80 bg-blue-500/10 px-2.5 py-1 rounded-full"
                  >
                    {tag}
                  </span>
                ))}
              </div>
              <h3 className="font-bold text-lg text-gray-900 mb-2 group-hover:text-blue-600 transition-colors leading-tight">
                {post.title}
              </h3>
              <p className="text-gray-600 text-sm leading-relaxed flex-1">
                {post.excerpt.slice(0, 150)}...
              </p>
              <div className="mt-4 flex items-center justify-between text-xs text-gray-500">
                <span>{post.date}</span>
                <span className="text-blue-600 font-semibold group-hover:translate-x-1 transition-transform">
                  Read More →
                </span>
              </div>
            </Link>
          ))}
        </div>
      </section>

      {/* Pagination */}
      {totalPages > 1 && (
        <section className="pb-24 px-4">
          <div className="max-w-6xl mx-auto flex items-center justify-center gap-3">
            <button
              onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
              disabled={currentPage === 1}
              className="px-4 py-2 rounded-xl border border-gray-100 text-sm text-gray-600 hover:bg-gray-100 hover:text-gray-900 transition-all disabled:opacity-30 disabled:cursor-not-allowed"
            >
              ← Previous
            </button>
            {Array.from({ length: totalPages }, (_, i) => i + 1).map(
              (page) => (
                <button
                  key={page}
                  onClick={() => setCurrentPage(page)}
                  className={`w-10 h-10 rounded-xl text-sm font-semibold transition-all ${
                    page === currentPage
                      ? "bg-blue-600 text-white"
                      : "border border-gray-100 text-gray-600 hover:bg-gray-100 hover:text-gray-900"
                  }`}
                >
                  {page}
                </button>
              )
            )}
            <button
              onClick={() =>
                setCurrentPage((p) => Math.min(totalPages, p + 1))
              }
              disabled={currentPage === totalPages}
              className="px-4 py-2 rounded-xl border border-gray-100 text-sm text-gray-600 hover:bg-gray-100 hover:text-gray-900 transition-all disabled:opacity-30 disabled:cursor-not-allowed"
            >
              Next →
            </button>
          </div>
        </section>
      )}

      {/* CTA */}
      <section className="relative py-24 px-4 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-blue-600 to-blue-800" />
        <div className="relative max-w-2xl mx-auto text-center">
          <h2 className="text-3xl md:text-5xl font-extrabold mb-4 text-white">
            Want to{" "}
            <span className="text-amber-300">
              Dominate
            </span>{" "}
            Search?
          </h2>
          <p className="text-blue-200 mb-8 text-lg">
            Get a free SEO audit for your Bangladesh business. Let us help you
            rank higher and grow faster.
          </p>
          <Link
            href="/#contact"
            className="group inline-flex items-center gap-2 bg-white text-blue-700 px-10 py-4 rounded-xl font-bold text-lg transition-all hover:shadow-xl hover:-translate-y-0.5"
          >
            Get Your Free Audit
            <span className="group-hover:translate-x-1 transition-transform">
              →
            </span>
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-8 border-t border-gray-100 text-center text-sm text-gray-500">
        <p>
          © 2026{" "}
          <span className="text-blue-600 font-bold">
            Kanok MiahIT
          </span>{" "}
          — SEO Agency in Bangladesh. All rights reserved.
        </p>
      </footer>
    </div>
  );
}
