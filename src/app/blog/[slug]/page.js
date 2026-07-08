import posts from "../data";
import BlogPostClient from "./BlogPostClient";

export async function generateMetadata({ params }) {
  const { slug } = await params;
  const post = posts.find((p) => p.slug === slug);
  if (!post) return {};
  const fullTitle = `${post.title} — Md Kanok Miah | SEO Expert in Dhaka, Bangladesh`;
  return {
    title: fullTitle,
    description: post.excerpt || `${post.title} — SEO tips and guide by Md Kanok Miah.`,
    alternates: { canonical: `/blog/${post.slug}` },
    openGraph: {
      title: fullTitle,
      description: post.excerpt,
      url: `https://kanokmiah.com.bd/blog/${post.slug}`,
    },
  };
}

export default async function BlogPostPage({ params }) {
  await params;
  return <BlogPostClient />;
}
