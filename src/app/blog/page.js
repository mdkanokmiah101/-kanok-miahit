"use client";
import { useState, useEffect } from "react";
import Navbar from "@/components/Navbar";
import Link from "next/link";
import posts from "./data";

const categories = [
  { name: "SEO Guide", icon: "📘", count: 0 },
  { name: "Local SEO", icon: "📍", count: 0 },
  { name: "Technical SEO", icon: "🔧", count: 0 },
  { name: "E-commerce SEO", icon: "🛒", count: 0 },
  { name: "Link Building", icon: "🔗", count: 0 },
  { name: "GEO & AI Search", icon: "🤖", count: 0 },
  { name: "Digital Marketing", icon: "📈", count: 0 },
  { name: "Industry SEO", icon: "🏭", count: 0 },
];

// Count posts per category
categories.forEach(cat => {
  cat.count = posts.filter(p => p.tags.some(t => t.toLowerCase().includes(cat.name.toLowerCase().replace(/[&\s]/g, ' ').trim()))).length;
  if (cat.count === 0) {
    // broader match
    cat.count = posts.filter(p => p.tags.some(t => cat.tags ? t === cat.name : false)).length;
  }
});

export default function BlogPage() {
  const [activeCategory, setActiveCategory] = useState("All");


  const filteredPosts = activeCategory === "All"
    ? posts
    : posts.filter(p => p.tags.some(t => t.toLowerCase().includes(activeCategory.toLowerCase())));

  const recentPosts = posts.slice(0, 5);

  return (
    <div className="min-h-screen bg-white text-gray-900">
      <head>
        <link rel="canonical" href="https://kanokmiah.com.bd/blog" />
        <meta name="robots" content="index, follow" />
      </head>
      {/* Navbar */}
      <Navbar />

      {/* Header */}
      <section className="relative pt-32 pb-14 px-4 text-center overflow-hidden bg-gradient-to-b from-gray-50 to-white">
        <div className="absolute top-1/4 left-1/3 w-72 h-72 bg-primary/[0.07] rounded-full blur-3xl" />
        <div className="relative max-w-4xl mx-auto">
          <span className="text-primary text-sm font-semibold tracking-widest uppercase">Our Blog</span>
          <h1 className="text-4xl md:text-5xl font-extrabold mt-4 mb-4">
            SEO Insights for <span className="text-primary">Bangladesh</span>
          </h1>
          <p className="text-gray-500 text-lg max-w-2xl mx-auto">
            Expert SEO tips, guides, and strategies tailored for Bangladeshi businesses.
          </p>
        </div>
      </section>

      {/* Main Content */}
      <section className="py-12 px-4">
        <div className="max-w-6xl mx-auto flex flex-col lg:flex-row gap-10">
          
          {/* Sidebar */}
          <aside className="lg:w-80 shrink-0 order-first">
            <div className="sticky top-24 space-y-8">
              {/* Search */}
              <div>
                <h3 className="font-bold text-sm text-gray-900 uppercase tracking-wider mb-3">Search</h3>
                <input
                  type="text"
                  placeholder="Search articles..."
                  className="w-full bg-gray-50 border border-gray-200 rounded-xl px-4 py-2.5 text-sm text-gray-900 placeholder-gray-400 focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary/20 transition-all"
                />
              </div>

              {/* Categories */}
              <div>
                <h3 className="font-bold text-sm text-gray-900 uppercase tracking-wider mb-3">Categories</h3>
                <div className="space-y-1">
                  <button
                    onClick={() => setActiveCategory("All")}
                    className={`w-full text-left px-4 py-2.5 rounded-xl text-sm font-medium transition-all flex items-center justify-between ${
                      activeCategory === "All"
                        ? "bg-primary text-white"
                        : "text-gray-600 hover:bg-gray-50 hover:text-gray-900"
                    }`}
                  >
                    <span>📋 All Articles</span>
                    <span className={`text-xs font-bold px-2 py-0.5 rounded-full ${
                      activeCategory === "All" ? "bg-white/20 text-white" : "bg-gray-200 text-gray-500"
                    }`}>{posts.length}</span>
                  </button>
                  {categories.filter(c => c.count > 0).map((cat) => (
                    <button
                      key={cat.name}
                      onClick={() => setActiveCategory(cat.name)}
                      className={`w-full text-left px-4 py-2.5 rounded-xl text-sm font-medium transition-all flex items-center justify-between ${
                        activeCategory === cat.name
                          ? "bg-primary text-white"
                          : "text-gray-600 hover:bg-gray-50 hover:text-gray-900"
                      }`}
                    >
                      <span>{cat.icon} {cat.name}</span>
                      <span className={`text-xs font-bold px-2 py-0.5 rounded-full ${
                        activeCategory === cat.name ? "bg-white/20 text-white" : "bg-gray-200 text-gray-500"
                      }`}>{cat.count}</span>
                    </button>
                  ))}
                </div>
              </div>

              {/* Recent Posts */}
              <div className="bg-gray-50 border border-gray-100 rounded-2xl p-6">
                <h3 className="font-bold text-sm text-gray-900 uppercase tracking-wider mb-4">Recent Posts</h3>
                <div className="space-y-4">
                  {recentPosts.map((post, i) => (
                    <Link key={i} href={`/blog/${post.slug}`} className="group flex gap-3">
                      <span className="text-lg shrink-0 mt-0.5">{post.imagePlaceholder}</span>
                      <div className="min-w-0">
                        <h4 className="text-sm font-semibold text-gray-900 group-hover:text-primary transition-colors leading-snug line-clamp-2">
                          {post.title}
                        </h4>
                        <span className="text-xs text-gray-400">{post.date}</span>
                      </div>
                    </Link>
                  ))}
                </div>
              </div>
            </div>
          </aside>

          {/* Blog Posts */}
          <div className="flex-1 min-w-0">
            <h2 className="text-2xl md:text-3xl font-extrabold mb-6">
              Latest <span className="text-primary">Blog Posts</span> & SEO Tips
            </h2>
            {activeCategory !== "All" && (
              <div className="mb-6">
                <span className="text-sm text-gray-500">
                  Showing posts in <strong className="text-gray-900">{activeCategory}</strong>
                  <button
                    onClick={() => setActiveCategory("All")}
                    className="ml-2 text-primary hover:underline text-xs"
                  >
                    (Clear filter)
                  </button>
                </span>
              </div>
            )}

            {filteredPosts.length === 0 ? (
              <div className="text-center py-16">
                <div className="text-5xl mb-4">📭</div>
                <h3 className="text-xl font-bold text-gray-900 mb-2">No posts found</h3>
                <p className="text-gray-500">No posts in this category yet. Check back soon!</p>
                <button
                  onClick={() => setActiveCategory("All")}
                  className="mt-4 text-primary font-semibold hover:underline"
                >
                  ← View all posts
                </button>
              </div>
            ) : (
              <div className="grid md:grid-cols-2 gap-5">
                {filteredPosts.map((post, i) => (
                  <Link
                    key={i}
                    href={`/blog/${post.slug}`}
                    className="group bg-white border border-gray-100 rounded-2xl p-6 hover:border-primary/20 hover:-translate-y-1 transition-all flex flex-col shadow-sm hover:shadow-md"
                  >
                    <div className="flex items-start gap-3 mb-3">
                      <div className="text-3xl shrink-0">{post.imagePlaceholder}</div>
                      <div className="flex flex-wrap gap-1.5">
                        {post.tags.slice(0, 2).map((tag, ti) => (
                          <span
                            key={ti}
                            className="text-[11px] font-medium text-primary/70 bg-primary/[0.07] px-2.5 py-1 rounded-full"
                          >{tag}</span>
                        ))}
                      </div>
                    </div>
                    <h3 className="font-bold text-[15px] text-gray-900 mb-2 group-hover:text-primary transition-colors leading-snug">
                      {post.title}
                    </h3>
                    <p className="text-gray-500 text-sm leading-relaxed flex-1">
                      {post.excerpt.slice(0, 140)}...
                    </p>
                    <div className="mt-3 pt-3 border-t border-gray-100 flex items-center justify-between text-xs text-gray-400">
                      <span>{post.date}</span>
                      <span className="text-primary font-semibold group-hover:translate-x-1 transition-transform">
                        Read More →
                      </span>
                    </div>
                  </Link>
                ))}
              </div>
            )}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="relative py-20 px-4 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-primary to-primary-dark" />
        <div className="relative max-w-2xl mx-auto text-center">
          <h2 className="text-3xl md:text-4xl font-extrabold mb-3 text-white">
            Want to <span className="text-amber-300">Dominate</span> Search?
          </h2>
          <p className="text-primary/80 mb-7 text-base">
            Get a free SEO audit for your Bangladesh business.
          </p>
          <Link
            href="/#contact"
            className="group inline-flex items-center gap-2 bg-white text-primary-dark px-8 py-3.5 rounded-xl font-bold transition-all hover:shadow-xl hover:-translate-y-0.5"
          >
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
