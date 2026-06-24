"use client";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import posts from "../data";

export default function BlogPostPage() {
  const { slug } = useParams();
  const post = posts.find((p) => p.slug === slug);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    if (!post) return;
    document.title = `${post.title} — Kanok MiahIT Blog`;
    const metaDesc = document.querySelector('meta[name="description"]');
    if (metaDesc) {
      metaDesc.setAttribute("content", post.excerpt);
    }
    window.scrollTo(0, 0);
  }, [post]);

  if (!post) {
    return (
      <div className="min-h-screen bg-[#0a0a0f] text-white flex items-center justify-center flex-col gap-4 px-4">
        <div className="text-6xl mb-4">📝</div>
        <h1 className="text-3xl font-bold">Post Not Found</h1>
        <p className="text-gray-400 text-center max-w-md">
          The blog post you're looking for doesn't exist or may have been
          moved.
        </p>
        <Link
          href="/blog"
          className="text-cyan-400 hover:text-cyan-300 font-semibold transition-colors"
        >
          ← Back to Blog
        </Link>
      </div>
    );
  }

  // Related posts (same tags, exclude current)
  const related = posts
    .filter(
      (p) =>
        p.slug !== slug &&
        p.tags.some((t) => post.tags.includes(t))
    )
    .slice(0, 3);

  const shareUrl = typeof window !== "undefined"
    ? window.location.href
    : `https://kanok-miahit.vercel.app/blog/${post.slug}`;

  const handleCopyLink = () => {
    navigator.clipboard.writeText(shareUrl).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  };

  const formattedContent = post.content
    .split("\n")
    .filter((line) => line.trim())
    .map((line, i) => {
      if (line.startsWith("## ")) {
        return (
          <h2
            key={i}
            className="text-2xl md:text-3xl font-extrabold mt-12 mb-4 text-white"
          >
            {line.replace("## ", "")}
          </h2>
        );
      }
      if (line.startsWith("### ")) {
        return (
          <h3
            key={i}
            className="text-xl font-bold mt-8 mb-3 text-cyan-200"
          >
            {line.replace("### ", "")}
          </h3>
        );
      }
      if (line.startsWith("- **") && line.includes(":**")) {
        // Bullet with bold label
        const parts = line.match(/- \*\*(.+?):\*\*(.*)/);
        if (parts) {
          return (
            <li
              key={i}
              className="flex items-start gap-2 text-gray-300 mb-2"
            >
              <span className="text-emerald-400 mt-1.5 shrink-0">•</span>
              <span>
                <strong className="text-white">{parts[1]}:</strong>
                {parts[2]}
              </span>
            </li>
          );
        }
        return (
          <li
            key={i}
            className="flex items-start gap-2 text-gray-300 mb-2"
          >
            <span className="text-emerald-400 mt-1.5 shrink-0">•</span>
            <span>{line.replace(/^- \*\*/, "").replace(/\*\*/, "")}</span>
          </li>
        );
      }
      if (line.startsWith("- ")) {
        return (
          <li
            key={i}
            className="flex items-start gap-2 text-gray-300 mb-2"
          >
            <span className="text-emerald-400 mt-1.5 shrink-0">•</span>
            <span>{line.replace("- ", "")}</span>
          </li>
        );
      }
      if (line.startsWith("| ")) {
        // Table row — render as simple text
        return null;
      }
      // Regular paragraph
      return (
        <p key={i} className="text-gray-300 leading-relaxed mb-5 text-base">
          {line}
        </p>
      );
    });

  return (
    <div className="min-h-screen bg-[#0a0a0f] text-white">
      {/* Navbar */}
      <nav className="fixed top-0 w-full bg-[#0a0a0f]/90 backdrop-blur-xl border-b border-white/5 z-50">
        <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
          <Link href="/" className="text-xl font-extrabold tracking-tight">
            <span className="bg-gradient-to-r from-cyan-400 to-emerald-400 bg-clip-text text-transparent">
              Kanok Miah
            </span>
            <span className="text-amber-400">IT</span>
          </Link>
          <Link
            href="/blog"
            className="text-sm text-gray-400 hover:text-cyan-400 transition-colors"
          >
            ← Blog
          </Link>
        </div>
      </nav>

      {/* Article Hero */}
      <section className="relative pt-32 pb-12 px-4 overflow-hidden">
        <div className="absolute top-1/3 -left-32 w-96 h-96 bg-cyan-500/20 rounded-full blur-3xl animate-pulse" />
        <div className="absolute bottom-1/3 -right-32 w-96 h-96 bg-emerald-500/20 rounded-full blur-3xl animate-pulse delay-1000" />
        <div className="relative max-w-3xl mx-auto">
          <div className="inline-flex items-center gap-2 bg-white/5 border border-white/10 text-cyan-300 text-xs font-semibold px-5 py-2 rounded-full mb-6 backdrop-blur-sm">
            <span className="w-2 h-2 bg-emerald-400 rounded-full animate-pulse" />
            {post.tags[0]}
          </div>
          <h1 className="text-3xl md:text-5xl lg:text-6xl font-extrabold leading-tight mb-6">
            {post.title}
          </h1>
          <div className="flex flex-wrap items-center gap-4 text-sm text-gray-500 mb-8">
            <span className="flex items-center gap-2">
              <span className="w-7 h-7 rounded-full bg-gradient-to-br from-cyan-400 to-emerald-400 flex items-center justify-center text-xs font-bold text-[#0a0a0f]">
                KM
              </span>
              {post.author}
            </span>
            <span>•</span>
            <span>{post.date}</span>
            <span>•</span>
            <span className="text-2xl">{post.imagePlaceholder}</span>
          </div>
          <div className="flex flex-wrap gap-2">
            {post.tags.map((tag, ti) => (
              <span
                key={ti}
                className="text-xs font-medium text-cyan-400/80 bg-cyan-500/10 px-3 py-1.5 rounded-full"
              >
                #{tag}
              </span>
            ))}
          </div>
        </div>
      </section>

      {/* Article Content */}
      <article className="py-8 px-4">
        <div className="max-w-3xl mx-auto">
          {/* Excerpt / Lead */}
          <div className="text-lg md:text-xl text-gray-400 border-l-4 border-cyan-500/50 pl-5 mb-10 italic leading-relaxed">
            {post.excerpt}
          </div>

          {/* Content */}
          <div className="prose-custom">{formattedContent}</div>

          {/* Share Section */}
          <div className="mt-16 pt-8 border-t border-white/10">
            <h3 className="text-lg font-bold mb-4">
              Share this article
            </h3>
            <div className="flex flex-wrap gap-3">
              <a
                href={`https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(shareUrl)}`}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 bg-white/[0.05] border border-white/10 rounded-xl px-4 py-2.5 text-sm text-gray-300 hover:bg-white/[0.1] hover:border-cyan-500/30 transition-all"
              >
                <span>📘</span> Facebook
              </a>
              <a
                href={`https://twitter.com/intent/tweet?text=${encodeURIComponent(post.title)}&url=${encodeURIComponent(shareUrl)}`}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 bg-white/[0.05] border border-white/10 rounded-xl px-4 py-2.5 text-sm text-gray-300 hover:bg-white/[0.1] hover:border-cyan-500/30 transition-all"
              >
                <span>🐦</span> X / Twitter
              </a>
              <a
                href={`https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(shareUrl)}`}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 bg-white/[0.05] border border-white/10 rounded-xl px-4 py-2.5 text-sm text-gray-300 hover:bg-white/[0.1] hover:border-cyan-500/30 transition-all"
              >
                <span>💼</span> LinkedIn
              </a>
              <button
                onClick={handleCopyLink}
                className="inline-flex items-center gap-2 bg-white/[0.05] border border-white/10 rounded-xl px-4 py-2.5 text-sm text-gray-300 hover:bg-white/[0.1] hover:border-cyan-500/30 transition-all"
              >
                <span>{copied ? "✅" : "🔗"}</span>
                {copied ? "Copied!" : "Copy Link"}
              </button>
            </div>
          </div>
        </div>
      </article>

      {/* Related Posts */}
      {related.length > 0 && (
        <section className="py-16 px-4 bg-white/[0.02] border-y border-white/5">
          <div className="max-w-6xl mx-auto">
            <h2 className="text-2xl md:text-3xl font-extrabold mb-8 text-center">
              Related{" "}
              <span className="text-cyan-400">Articles</span>
            </h2>
            <div className="grid md:grid-cols-3 gap-5">
              {related.map((rp, i) => (
                <Link
                  key={i}
                  href={`/blog/${rp.slug}`}
                  className="group bg-white/[0.03] border border-white/10 rounded-2xl p-6 hover:bg-white/[0.06] hover:border-cyan-500/30 hover:-translate-y-1 transition-all"
                >
                  <div className="text-3xl mb-3">{rp.imagePlaceholder}</div>
                  <div className="flex flex-wrap gap-2 mb-2">
                    {rp.tags.slice(0, 2).map((tag, ti) => (
                      <span
                        key={ti}
                        className="text-xs font-medium text-cyan-400/80 bg-cyan-500/10 px-2 py-0.5 rounded-full"
                      >
                        {tag}
                      </span>
                    ))}
                  </div>
                  <h3 className="font-bold text-white mb-1.5 group-hover:text-cyan-300 transition-colors text-sm leading-snug">
                    {rp.title}
                  </h3>
                  <p className="text-gray-500 text-xs leading-relaxed">
                    {rp.date}
                  </p>
                </Link>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* CTA */}
      <section className="relative py-24 px-4 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-cyan-600/20 via-emerald-600/20 to-amber-600/20" />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] bg-gradient-to-r from-cyan-500/20 to-emerald-500/20 rounded-full blur-3xl" />
        <div className="relative max-w-2xl mx-auto text-center">
          <h2 className="text-3xl md:text-5xl font-extrabold mb-4">
            Let's Grow Your{" "}
            <span className="bg-gradient-to-r from-cyan-300 to-emerald-300 bg-clip-text text-transparent">
              Business
            </span>
          </h2>
          <p className="text-gray-400 mb-8 text-lg">
            Ready to rank higher in Bangladesh search results? Get a free SEO
            audit and discover how we can help.
          </p>
          <Link
            href="/#contact"
            className="group inline-flex items-center gap-2 bg-gradient-to-r from-cyan-500 to-emerald-500 text-white px-10 py-4 rounded-xl font-bold text-lg transition-all hover:shadow-xl hover:shadow-cyan-500/30 hover:-translate-y-0.5"
          >
            Get Your Free Audit
            <span className="group-hover:translate-x-1 transition-transform">
              →
            </span>
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-8 border-t border-white/5 text-center text-sm text-gray-600">
        <p>
          © 2026{" "}
          <span className="bg-gradient-to-r from-cyan-400 to-emerald-400 bg-clip-text text-transparent font-bold">
            Kanok MiahIT
          </span>{" "}
          — SEO Agency in Bangladesh. All rights reserved.
        </p>
      </footer>
    </div>
  );
}
