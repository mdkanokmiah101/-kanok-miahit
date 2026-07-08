import posts from "../data";
import BlogPostClient from "./BlogPostClient";

export function generateMetadata({ params }) {
  const post = posts.find((p) => p.slug === params.slug);
  if (!post) return {};
  return {
    title: `${post.title} — Md Kanok Miah Blog`,
    description: post.excerpt || `${post.title} — SEO tips and guide by Md Kanok Miah.`,
    alternates: { canonical: `/blog/${post.slug}` },
    openGraph: {
      title: `${post.title} — Md Kanok Miah Blog`,
      description: post.excerpt,
      url: `https://kanokmiah.com.bd/blog/${post.slug}`,
    },
  };
}

export default function BlogPostPage({ params }) {
  return <BlogPostClient />;
}
