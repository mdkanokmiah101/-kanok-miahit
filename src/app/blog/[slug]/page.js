import posts from "../data";
import BlogPostClient from "./BlogPostClient";
import { BreadcrumbSchema, ArticleSchema } from "@/components/Schema";
import { notFound } from "next/navigation";

export async function generateMetadata({ params }) {
  const { slug } = await params;
  const post = posts.find((p) => p.slug === slug);
  if (!post) return { title: "Blog Post Not Found — Md Kanok Miah" };
  const fullTitle = `${post.title} — Md Kanok Miah | SEO Expert in Dhaka, Bangladesh`;
  return {
    title: fullTitle,
    description: post.excerpt || `${post.title} — SEO tips and guide by Md Kanok Miah.`,
    alternates: { canonical: `/blog/${post.slug}` },
    openGraph: {
      title: fullTitle,
      description: post.excerpt,
      url: `https://kanokmiah.com.bd/blog/${post.slug}`,
      images: [{ url: "/kanok-miah-profile.webp", width: 400, height: 400, alt: "Md Kanok Miah — SEO Expert Dhaka" }],
    },
  };
}

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
      <BlogPostClient />
    </>
  );
}
