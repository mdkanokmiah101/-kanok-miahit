import industries from "../data";
import IndustryPageClient from "./IndustryPageClient";
import { notFound } from "next/navigation";

export function generateStaticParams() {
  return industries.map((ind) => ({ slug: ind.slug }));
}

export async function generateMetadata({ params }) {
  const { slug } = await params;
  const ind = industries.find((i) => i.slug === slug);
  if (!ind) return { title: "Industry Not Found — Md Kanok Miah" };
  return {
    title: ind.title,
    description: ind.desc,
    alternates: { canonical: `/industries/${ind.slug}` },
    openGraph: {
      title: ind.title,
      description: ind.desc,
      url: `https://kanokmiah.com.bd/industries/${ind.slug}`,
      siteName: "Md Kanok Miah",
      images: [{ url: "/kanok-miah-profile.webp", width: 400, height: 400, alt: "Md Kanok Miah — SEO Expert Dhaka" }],
    },
    twitter: {
      card: "summary_large_image",
      title: ind.title,
      description: ind.desc,
      images: ["/kanok-miah-profile.webp"],
    },
  };
}

export default async function IndustryPage({ params }) {
  const { slug } = await params;
  const ind = industries.find((i) => i.slug === slug);
  if (!ind) notFound();
  return <IndustryPageClient slug={slug} />;
}
