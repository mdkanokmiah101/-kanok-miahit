"use client";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Navbar from "@/components/Navbar";
import Link from "next/link";
import { FAQSchema } from "@/components/Schema";
import posts from "../data";

export default function BlogPostPage() {
  const { slug } = useParams();
  const post = posts.find((p) => p.slug === slug);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    if (!post) return;
    document.title = `${post.title} — Md Kanok Miah Blog`;
    const metaDesc = document.querySelector('meta[name="description"]');
    if (metaDesc) {
      metaDesc.setAttribute("content", post.excerpt);
    }
    window.scrollTo(0, 0);
  }, [post]);

  if (!post) {
    return (
      <div className="min-h-screen bg-white text-gray-900 flex items-center justify-center flex-col gap-4 px-4">
        <div className="text-6xl mb-4">📝</div>
        <h1 className="text-3xl font-bold">Post Not Found</h1>
        <p className="text-gray-600 text-center max-w-md">
          The blog post you're looking for doesn't exist or may have been
          moved.
        </p>
        <Link
          href="/blog"
          className="text-primary hover:text-primary-dark font-semibold transition-colors"
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
    : `https://kanokmiah.com.bd/blog/${post.slug}`;

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
            className="text-2xl md:text-3xl font-extrabold mt-12 mb-4 text-gray-900"
          >
            {line.replace("## ", "")}
          </h2>
        );
      }
      if (line.startsWith("### ")) {
        return (
          <h3
            key={i}
            className="text-xl font-bold mt-8 mb-3 text-primary"
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
              className="flex items-start gap-2 text-gray-600 mb-2"
            >
              <span className="text-primary mt-1.5 shrink-0">•</span>
              <span>
                <strong className="text-gray-900">{parts[1]}:</strong>
                {parts[2]}
              </span>
            </li>
          );
        }
        return (
          <li
            key={i}
            className="flex items-start gap-2 text-gray-600 mb-2"
          >
            <span className="text-primary mt-1.5 shrink-0">•</span>
            <span>{line.replace(/^- \*\*/, "").replace(/\*\*/, "")}</span>
          </li>
        );
      }
      if (line.startsWith("- ")) {
        return (
          <li
            key={i}
            className="flex items-start gap-2 text-gray-600 mb-2"
          >
            <span className="text-primary mt-1.5 shrink-0">•</span>
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
        <p key={i} className="text-gray-600 leading-relaxed mb-5 text-base">
          {line}
        </p>
      );
    });

  return (
    <div className="min-h-screen bg-white text-gray-900">
      {/* Navbar */}
      <Navbar />

      {/* Article Hero */}
      <section className="relative pt-32 pb-12 px-4 overflow-hidden">
        <div className="absolute top-1/3 -left-32 w-96 h-96 bg-primary/20 rounded-full blur-3xl animate-pulse" />
        <div className="absolute bottom-1/3 -right-32 w-96 h-96 bg-primary/20 rounded-full blur-3xl animate-pulse delay-1000" />
        <div className="relative max-w-3xl mx-auto">
          <div className="inline-flex items-center gap-2 bg-primary-light border border-primary/20 text-primary text-xs font-semibold px-5 py-2 rounded-full mb-6 backdrop-blur-sm">
            <span className="w-2 h-2 bg-primary rounded-full animate-pulse" />
            {post.tags[0]}
          </div>
          <h1 className="text-3xl md:text-5xl lg:text-6xl font-extrabold leading-tight mb-6">
            {post.title}
          </h1>
          <div className="flex flex-wrap items-center gap-4 text-sm text-gray-500 mb-8">
            <span className="flex items-center gap-2">
              <span className="w-7 h-7 rounded-full bg-primary flex items-center justify-center text-xs font-bold text-white">
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
                className="text-xs font-medium text-primary/80 bg-primary/10 px-3 py-1.5 rounded-full"
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
          <div className="text-lg md:text-xl text-gray-600 border-l-4 border-primary pl-5 mb-10 italic leading-relaxed">
            {post.excerpt}
          </div>

          {/* Content */}
          <div className="prose-custom">{formattedContent}</div>

          {/* Share Section */}
          <div className="mt-16 pt-8 border-t border-gray-100">
            <h3 className="text-lg font-bold mb-4">
              Share this article
            </h3>
            <div className="flex flex-wrap gap-3">
              <a
                href={`https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(shareUrl)}`}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 bg-gray-50 border border-gray-100 rounded-xl px-4 py-2.5 text-sm text-gray-600 hover:bg-gray-100 hover:border-primary/20 transition-all"
              >
                <span>📘</span> Facebook
              </a>
              <a
                href={`https://twitter.com/intent/tweet?text=${encodeURIComponent(post.title)}&url=${encodeURIComponent(shareUrl)}`}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 bg-gray-50 border border-gray-100 rounded-xl px-4 py-2.5 text-sm text-gray-600 hover:bg-gray-100 hover:border-primary/20 transition-all"
              >
                <span>🐦</span> X / Twitter
              </a>
              <a
                href={`https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(shareUrl)}`}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 bg-gray-50 border border-gray-100 rounded-xl px-4 py-2.5 text-sm text-gray-600 hover:bg-gray-100 hover:border-primary/20 transition-all"
              >
                <span>💼</span> LinkedIn
              </a>
              <button
                onClick={handleCopyLink}
                className="inline-flex items-center gap-2 bg-gray-50 border border-gray-100 rounded-xl px-4 py-2.5 text-sm text-gray-600 hover:bg-gray-100 hover:border-primary/20 transition-all"
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
        <section className="py-16 px-4 bg-gray-50 border-y border-gray-100">
          <div className="max-w-6xl mx-auto">
            <h2 className="text-2xl md:text-3xl font-extrabold mb-8 text-center">
              Related{" "}
              <span className="text-primary">Articles</span>
            </h2>
            <div className="grid md:grid-cols-3 gap-5">
              {related.map((rp, i) => (
                <Link
                  key={i}
                  href={`/blog/${rp.slug}`}
                  className="group bg-gray-50 border border-gray-100 rounded-2xl p-6 hover:bg-gray-100 hover:border-primary/20 hover:-translate-y-1 transition-all"
                >
                  <div className="text-3xl mb-3">{rp.imagePlaceholder}</div>
                  <div className="flex flex-wrap gap-2 mb-2">
                    {rp.tags.slice(0, 2).map((tag, ti) => (
                      <span
                        key={ti}
                        className="text-xs font-medium text-primary/80 bg-primary/10 px-2 py-0.5 rounded-full"
                      >
                        {tag}
                      </span>
                    ))}
                  </div>
                  <h3 className="font-bold text-gray-900 mb-1.5 group-hover:text-primary transition-colors text-sm leading-snug">
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

      {/* FAQ */}
      <section className="py-16 px-4 bg-white">
        <div className="max-w-4xl mx-auto">
          {FAQSchema([
            { question: "How often should I publish blog posts for SEO?", answer: "For best SEO results, publish high-quality blog posts at least 2–4 times per month. Consistency matters more than frequency — Google rewards websites that regularly publish fresh, valuable content that addresses user search intent." },
            { question: "What topics should I write about for SEO?", answer: "Focus on topics your target audience is actively searching for. Conduct keyword research to identify questions and problems in your industry. Create content that provides comprehensive answers, guides, and insights that demonstrate expertise and authority." },
            { question: "How long should my blog posts be for SEO?", answer: "There is no ideal word count, but comprehensive content tends to rank better. For most topics, aim for 1,500–2,500 words. However, quality and relevance are far more important than length — a well-written 800-word post can outrank a poorly written 3,000-word post." },
            { question: "How long does it take for blog posts to rank on Google?", answer: "New blog posts typically take 3–6 months to start ranking on Google, depending on competition and domain authority. Older, established websites may see results faster. Consistent publishing and internal linking can accelerate this timeline." },
            { question: "Can I repurpose existing content for new blog posts?", answer: "Yes, updating and republishing old content is an excellent SEO strategy. Refresh statistics, add new insights, improve formatting, and update the publication date. Google often gives a ranking boost to recently updated content." },
          ])}
          <h2 className="text-2xl md:text-3xl font-extrabold text-center mb-8">
            Frequently Asked <span className="text-primary">Questions</span>
          </h2>
          <div className="space-y-0 divide-y divide-gray-100">
            {[
              { question: "How often should I publish blog posts for SEO?", answer: "For best SEO results, publish high-quality blog posts at least 2–4 times per month. Consistency matters more than frequency — Google rewards websites that regularly publish fresh, valuable content that addresses user search intent." },
              { question: "What topics should I write about for SEO?", answer: "Focus on topics your target audience is actively searching for. Conduct keyword research to identify questions and problems in your industry. Create content that provides comprehensive answers, guides, and insights that demonstrate expertise and authority." },
              { question: "How long should my blog posts be for SEO?", answer: "There is no ideal word count, but comprehensive content tends to rank better. For most topics, aim for 1,500–2,500 words. However, quality and relevance are far more important than length — a well-written 800-word post can outrank a poorly written 3,000-word post." },
              { question: "How long does it take for blog posts to rank on Google?", answer: "New blog posts typically take 3–6 months to start ranking on Google, depending on competition and domain authority. Older, established websites may see results faster. Consistent publishing and internal linking can accelerate this timeline." },
              { question: "Can I repurpose existing content for new blog posts?", answer: "Yes, updating and republishing old content is an excellent SEO strategy. Refresh statistics, add new insights, improve formatting, and update the publication date. Google often gives a ranking boost to recently updated content." },
            ].map((f, i) => (
              <details key={i} className="py-4 group">
                <summary className="font-semibold text-gray-900 cursor-pointer list-none flex justify-between items-center">
                  {f.question}
                  <span className="text-primary transition-transform group-open:rotate-180">▼</span>
                </summary>
                <p className="text-gray-600 mt-3 pl-2">{f.answer}</p>
              </details>
            ))}
          </div>
        </div>
      </section>

      {/* Author Bio */}
      <div className="bg-gray-50 border-y border-gray-100 py-12 px-4">
        <div className="max-w-4xl mx-auto flex items-start gap-6">
          <div className="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center text-2xl shrink-0">👤</div>
          <div>
            <p className="font-bold text-gray-900">Written by <span className="text-primary">Md Kanok Miah</span></p>
            <p className="text-sm text-gray-500">SEO Expert with 6+ years of experience helping Bangladeshi businesses rank higher on Google. Google Business Profile certified.</p>
            <p className="text-xs text-gray-400 mt-2">Last updated: July 2026</p>
          </div>
        </div>
      </div>

      {/* CTA */}
      <section className="relative py-24 px-4 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-primary to-primary-dark" />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] bg-gradient-to-r from-primary/20 to-primary/20 rounded-full blur-3xl" />
        <div className="relative max-w-2xl mx-auto text-center">
          <h2 className="text-3xl md:text-5xl font-extrabold mb-4 text-white">
            Let's Grow Your{" "}
            <span className="text-amber-300">
              Business
            </span>
          </h2>
          <p className="text-primary/80 mb-8 text-lg">
            Ready to rank higher in Bangladesh search results? Get a free SEO
            audit and discover how we can help.
          </p>
          <Link
            href="/#contact"
            className="group inline-flex items-center gap-2 bg-white text-primary-dark px-10 py-4 rounded-xl font-bold text-lg transition-all hover:shadow-xl hover:-translate-y-0.5"
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
          <span className="text-primary font-bold">
            Md Kanok Miah
          </span>{" "}
          — SEO Expert in Bangladesh. All rights reserved.
        </p>
      </footer>
    </div>
  );
}
