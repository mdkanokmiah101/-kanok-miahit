import posts from "../data";
import BlogPostClient from "./BlogPostClient";
import { BreadcrumbSchema, ArticleSchema, FAQSchema } from "@/components/Schema";
import { notFound } from "next/navigation";

function truncateMeta(str, maxLen = 155) {
  if (!str) return "";
  if (str.length <= maxLen) return str;
  const truncated = str.slice(0, maxLen);
  const lastSpace = truncated.lastIndexOf(" ");
  return (lastSpace > 0 ? truncated.slice(0, lastSpace) : truncated) + "…";
}

export function generateStaticParams() {
  return posts.map((post) => ({ slug: post.slug }));
}

export async function generateMetadata({ params }) {
  const { slug } = await params;
  const post = posts.find((p) => p.slug === slug);
  if (!post) return { title: "Not Found" };
  const fullTitle = post.title;
  const metaDesc = truncateMeta(post.excerpt || `${post.title} — SEO tips and guide by Md Kanok Miah.`);
  return {
    title: `${fullTitle} — Md Kanok Miah`,
    description: metaDesc,
    alternates: { canonical: `https://kanokmiah.com.bd/blog/${post.slug}` },
    openGraph: {
      title: `${fullTitle} — Md Kanok Miah | SEO Expert in Dhaka, Bangladesh`,
      description: metaDesc,
      url: `https://kanokmiah.com.bd/blog/${post.slug}`,
      images: [{ url: "https://kanokmiah.com.bd/kanok-miah-profile.webp", width: 400, height: 400, alt: "Md Kanok Miah — SEO Expert Dhaka" }],
    },
    twitter: {
      card: "summary_large_image",
      title: `${fullTitle} — Md Kanok Miah | SEO Expert in Dhaka, Bangladesh`,
      description: metaDesc,
      images: ["https://kanokmiah.com.bd/kanok-miah-profile.webp"],
    },
  };
}

const blogPostFaqs = [
  { question: "How often should I publish blog posts for SEO?", answer: "For best SEO results, publish high-quality blog posts at least 2–4 times per month. Consistency matters more than frequency — Google rewards websites that regularly publish fresh, valuable content that addresses user search intent." },
  { question: "What topics should I write about?", answer: "Focus on topics your target audience is actively searching for. Conduct keyword research to identify questions and problems in your industry. Create content that provides comprehensive answers, guides, and insights that demonstrate expertise and authority." },
  { question: "How long should blog posts be?", answer: "There is no ideal word count, but comprehensive content tends to rank better. For most topics, aim for 1,500–2,500 words. However, quality and relevance are far more important than length — a well-written 800-word post can outrank a poorly written 3,000-word post." },
  { question: "How long does it take for posts to rank?", answer: "New blog posts typically take 3–6 months to start ranking on Google, depending on competition and domain authority. Older, established websites may see results faster. Consistent publishing and internal linking can accelerate this timeline." },
];

export default async function BlogPostPage({ params }) {
  const { slug } = await params;
  const post = posts.find((p) => p.slug === slug);
  if (!post) notFound();
  return (
    <>
      {BreadcrumbSchema([
        { name: "Home", url: "https://kanokmiah.com.bd" },
        { name: "Blog", url: "https://kanokmiah.com.bd/blog" },
        { name: post?.title || slug, url: `https://kanokmiah.com.bd/blog/${slug}` },
      ])}
      {post && ArticleSchema(post)}
      {FAQSchema({ faqs: blogPostFaqs })}
      <BlogPostClient />
    </>
  );
}
