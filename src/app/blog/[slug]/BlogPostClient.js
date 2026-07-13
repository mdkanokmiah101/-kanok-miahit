"use client";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import Link from "next/link";
import posts from "../data";
import services from "@/app/services/data";
import industries from "@/app/industries/data";

// Helper to render inline markdown links [text](url) as React elements
function renderInlineContent(text) {
  if (!text) return text;
  const linkRegex = /\[([^\]]+)\]\(([^)]+)\)/g;
  const parts = [];
  let lastIndex = 0;
  let match;
  let hasLinks = false;
  while ((match = linkRegex.exec(text)) !== null) {
    hasLinks = true;
    if (match.index > lastIndex) {
      parts.push(text.slice(lastIndex, match.index));
    }
    parts.push(
      <a key={match.index} href={match[2]} className="service-link" style={{ fontSize: 'inherit' }}>
        {match[1]}
      </a>
    );
    lastIndex = match.index + match[0].length;
  }
  if (hasLinks) {
    if (lastIndex < text.length) {
      parts.push(text.slice(lastIndex));
    }
    return parts;
  }
  return text;
}

export default function BlogPostClient() {
  const { slug } = useParams();
  const post = posts.find((p) => p.slug === slug);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    if (!post) return;
    window.scrollTo(0, 0);
  }, [post]);

  // Build contextual internal links based on post tags/content
  const contextualServices = [];
  const contextualIndustries = [];
  const tagKeywordMap = {
    "local": "local-seo",
    "gbp": "local-seo",
    "google maps": "local-seo",
    "near-me": "local-seo",
    "on-page": "on-page-seo",
    "onpage": "on-page-seo",
    "link building": "link-building",
    "backlink": "link-building",
    "technical": "technical-seo",
    "core web vitals": "technical-seo",
    "mobile": "technical-seo",
    "schema": "technical-seo",
    "semantic": "semantic-seo",
    "entity": "semantic-seo",
    "geo": "geo-ai-search",
    "generative engine": "geo-ai-search",
    "ai search": "geo-ai-search",
    "chatgpt": "geo-ai-search",
    "sge": "geo-ai-search",
    "ecommerce": "ecommerce-seo",
    "e-commerce": "ecommerce-seo",
    "daraz": "ecommerce-seo",
    "shopify": "ecommerce-seo",
    "woocommerce": "ecommerce-seo",
    "seo guide": null,
    "digital marketing": null,
    "garments": "garments-textile",
    "textile": "garments-textile",
    "rmg": "garments-textile",
    "real estate": "real-estate",
    "property": "real-estate",
    "cleaning": "cleaning",
    "spa": "spa-salon",
    "salon": "spa-salon",
    "beauty": "spa-salon",
    "medical": "medical",
    "healthcare": "medical",
    "education": "education",
    "training": "education",
    "restaurant": "food-restaurant",
    "food": "food-restaurant",
    "smm": "smm-panel",
    "social media": "smm-panel"
  };

  if (post) {
    // Check all tags
    post.tags.forEach(tag => {
      const lowerTag = tag.toLowerCase();
      // Check service slugs
      services.forEach(s => {
        if (lowerTag.includes(s.slug.replace("-seo", "").replace("-", " ")) ||
            lowerTag.includes(s.title.toLowerCase().split(" ").slice(0, 2).join(" ")) ||
            (tagKeywordMap[lowerTag] === s.slug)) {
          if (!contextualServices.find(x => x.slug === s.slug)) {
            contextualServices.push(s);
          }
        }
      });
      // Check industry slugs
      industries.forEach(ind => {
        const indKeywords = ind.shortTitle.toLowerCase().split(" & ")[0];
        if (lowerTag.includes(indKeywords) ||
            lowerTag.includes(ind.slug.replace("-", " "))) {
          if (!contextualIndustries.find(x => x.slug === ind.slug)) {
            contextualIndustries.push(ind);
          }
        }
      });
      // Check keyword map for industry
      Object.entries(tagKeywordMap).forEach(([keyword, slug]) => {
        if (lowerTag.includes(keyword) && slug) {
          const svc = services.find(s => s.slug === slug);
          if (svc && !contextualServices.find(x => x.slug === svc.slug)) {
            contextualServices.push(svc);
          }
          const indSlug = slug; // could be industry slug
          const ind = industries.find(i => i.slug === slug);
          if (ind && !contextualIndustries.find(x => x.slug === ind.slug)) {
            contextualIndustries.push(ind);
          }
        }
      });
    });

    // Also check content for keywords
    const contentLower = post.content.toLowerCase();
    services.forEach(s => {
      if (!contextualServices.find(x => x.slug === s.slug)) {
        const keyword = s.title.toLowerCase();
        if (contentLower.includes(keyword)) {
          contextualServices.push(s);
        }
      }
    });
    industries.forEach(ind => {
      if (!contextualIndustries.find(x => x.slug === ind.slug)) {
        const keyword = ind.shortTitle.toLowerCase();
        const keyword2 = ind.slug.replace("-", " ");
        if (contentLower.includes(keyword) || contentLower.includes(keyword2)) {
          contextualIndustries.push(ind);
        }
      }
    });
  }

  const hasContextualLinks = contextualServices.length > 0 || contextualIndustries.length > 0;

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
                <strong className="text-gray-900">{renderInlineContent(parts[1])}:</strong>
                {renderInlineContent(parts[2])}
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
            <span>{renderInlineContent(line.replace(/^- \*\*/, "").replace(/\*\*/, ""))}</span>
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
            <span>{renderInlineContent(line.replace("- ", ""))}</span>
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
          {renderInlineContent(line)}
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
            <span className="text-primary">{post.title}</span><br/>
            <span className="text-gray-900">SEO Blog — Dhaka, Bangladesh</span>
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

          {/* Contextual Internal Links */}
          {hasContextualLinks && (
            <div className="mt-12 pt-8 border-t border-gray-100">
              <h3 className="text-lg font-bold mb-4 text-gray-900">
                Read More About Our Services
              </h3>
              {contextualServices.length > 0 && (
                <div className="mb-5">
                  <p className="text-sm text-gray-500 mb-3 font-medium">Related SEO Services:</p>
                  <div className="flex flex-wrap gap-2">
                    {contextualServices.slice(0, 6).map((svc) => (
                      <Link
                        key={svc.slug}
                        href={`/services/${svc.slug}`}
                        className="inline-flex items-center gap-1.5 bg-gray-50 border border-gray-100 text-gray-700 px-3.5 py-2 rounded-lg text-xs font-medium hover:border-primary/30 hover:text-primary hover:bg-primary-light transition-all"
                      >
                        {svc.icon} {svc.title}
                      </Link>
                    ))}
                  </div>
                </div>
              )}
              {contextualIndustries.length > 0 && (
                <div>
                  <p className="text-sm text-gray-500 mb-3 font-medium">Industries We Serve:</p>
                  <div className="flex flex-wrap gap-2">
                    {contextualIndustries.slice(0, 6).map((ind) => (
                      <Link
                        key={ind.slug}
                        href={`/industries/${ind.slug}`}
                        className="inline-flex items-center gap-1.5 bg-gray-50 border border-gray-100 text-gray-700 px-3.5 py-2 rounded-lg text-xs font-medium hover:border-primary/30 hover:text-primary hover:bg-primary-light transition-all"
                      >
                        {ind.icon} {ind.shortTitle}
                      </Link>
                    ))}
                  </div>
                </div>
              )}
              <div className="mt-4 pt-3 border-t border-gray-50 flex flex-wrap gap-3 text-sm">
                <Link href="/services" className="text-primary font-semibold hover:text-primary-dark transition-colors">
                  View All SEO Services →
                </Link>
                <Link href="/industries" className="text-gray-500 font-medium hover:text-primary transition-colors">
                  Explore All Industries →
                </Link>
              </div>
            </div>
          )}

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
          
          <h2 className="text-2xl md:text-3xl font-extrabold text-center mb-8">
            Frequently Asked <span className="text-primary">Questions</span>
          </h2>
          <div className="space-y-0 divide-y divide-gray-100">
            {[
              { question: "How often should I publish blog posts for SEO?", answer: "For best SEO results, publish high-quality blog posts at least 2–4 times per month. Consistency matters more than frequency — Google rewards websites that regularly publish fresh, valuable content that addresses user search intent." },
              { question: "What topics should I write about?", answer: "Focus on topics your target audience is actively searching for. Conduct keyword research to identify questions and problems in your industry. Create content that provides comprehensive answers, guides, and insights that demonstrate expertise and authority." },
              { question: "How long should blog posts be?", answer: "There is no ideal word count, but comprehensive content tends to rank better. For most topics, aim for 1,500–2,500 words. However, quality and relevance are far more important than length — a well-written 800-word post can outrank a poorly written 3,000-word post." },
              { question: "How long does it take for posts to rank?", answer: "New blog posts typically take 3–6 months to start ranking on Google, depending on competition and domain authority. Older, established websites may see results faster. Consistent publishing and internal linking can accelerate this timeline." },
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
          <div className="w-16 h-16 rounded-full shrink-0 overflow-hidden border-2 border-primary/20">
            <img
              src="/kanok-miah-profile.webp"
              alt="Md Kanok Miah — SEO Expert in Dhaka, Bangladesh"
              className="w-full h-full object-cover"
            />
          </div>
          <div>
            <p className="font-bold text-gray-900">Written by <span className="text-primary">Md Kanok Miah</span></p>
            <p className="text-sm text-gray-600">A proven <Link href="/" className="text-primary font-semibold hover:underline">SEO expert in Dhaka</Link>, Bangladesh — <Link href="/about" className="text-primary font-semibold hover:underline">learn more about Md Kanok Miah →</Link></p>
            <p className="text-sm text-gray-600 mt-2">Since 2019, Md Kanok Miah has delivered 210+ <Link href="/services" className="text-primary font-semibold hover:underline">SEO</Link> projects for local businesses, e-commerce stores, and international brands. Currently SEO Project Manager at Khan IT and Head of Digital Marketing at CloudMatrix Tech. Certified: Google Digital Garage, HubSpot Academy, SEMrush Academy.</p>
            <p className="text-xs text-gray-500 mt-2">Last updated: July 2026</p>
          </div>
        </div>
      </div>

      {/* CTA */}
      <section className="relative py-24 px-4 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-primary to-primary-dark" />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] bg-gradient-to-r from-primary/20 to-primary/20 rounded-full blur-3xl" />
        <div className="relative max-w-2xl mx-auto text-center">
          <div className="inline-flex items-center gap-2 bg-white/10 text-white border border-white/20 text-xs font-semibold px-4 py-1.5 rounded-full mb-5 backdrop-blur-sm">
            <span className="w-2 h-2 bg-amber-300 rounded-full animate-pulse" />
            Available for New Projects
          </div>
          <h2 className="text-3xl md:text-5xl font-extrabold mb-4 text-white">
            Hire{' '}
            <span className="text-amber-300">
              Md Kanok Miah
            </span>
          </h2>
          <p className="text-white/80 mb-6 text-lg">
            Ready to rank #1 on Google? Get a <strong className="text-white">free SEO audit</strong> &amp; custom strategy from Dhaka's top SEO expert with <strong className="text-white">210+ successful projects</strong>.
          </p>
          <div className="flex flex-wrap items-center justify-center gap-4 mb-6">
            <Link
              href="/contact"
              className="group inline-flex items-center gap-2 bg-white text-primary-dark px-8 py-4 rounded-xl font-bold text-lg transition-all hover:shadow-xl hover:-translate-y-0.5"
            >
              📋 Get Free Audit
              <span className="group-hover:translate-x-1 transition-transform">
                →
              </span>
            </Link>
            <a
              href="https://wa.me/8801604809110?text=Hi%20Kanok%20Miah!%20I%20need%20SEO%20help."
              target="_blank"
              rel="noopener noreferrer"
              className="group inline-flex items-center gap-2 bg-amber-300 text-primary-dark px-8 py-4 rounded-xl font-bold text-lg transition-all hover:shadow-xl hover:-translate-y-0.5"
            >
              💬 WhatsApp Now
            </a>
          </div>
          <div className="flex flex-wrap items-center justify-center gap-6 text-sm text-white/70">
            <span className="flex items-center gap-1.5">📞 +880 1604-809110</span>
            <span className="flex items-center gap-1.5">⭐ 108+ Verified Reviews</span>
            <span className="flex items-center gap-1.5">🏆 210+ SEO Projects</span>
          </div>
        </div>
      </section>

      {/* Footer */}
      <Footer />
    </div>
  );
}
