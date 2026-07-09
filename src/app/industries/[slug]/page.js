import industries from "../data";
import IndustryPageClient from "./IndustryPageClient";
import { BreadcrumbSchema, FAQSchema } from "@/components/Schema";
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

const industrySlugFaqs = [
  { question: "How does SEO work for this industry?", answer: "SEO for each industry requires a tailored approach. I analyze industry-specific search patterns, competitor strategies, and customer intent to create a customized optimization plan that targets the right keywords and delivers qualified traffic." },
  { question: "How long before I see results?", answer: "SEO results typically become visible within 3–6 months, depending on competition, current website state, and the aggressiveness of the strategy. Some improvements, like technical fixes, can show impact sooner — within 4–8 weeks." },
  { question: "What makes your approach different?", answer: "My approach combines deep local Bangladesh market knowledge with global SEO best practices. I focus on data-driven strategies, transparent reporting, and long-term sustainable growth rather than quick fixes that risk penalties." },
  { question: "Do you have case studies for this industry?", answer: "Yes, I have successfully worked with clients across various industries. Contact me to discuss case studies relevant to your specific industry. I'm happy to share examples of past results and client testimonials." },
];

export default async function IndustryPage({ params }) {
  const { slug } = await params;
  const ind = industries.find((i) => i.slug === slug);
  if (!ind) notFound();
  return (
    <>
      {BreadcrumbSchema([
        { name: "Home", url: "https://kanokmiah.com.bd" },
        { name: "Industries", url: "https://kanokmiah.com.bd/industries" },
        { name: ind?.title || slug, url: `https://kanokmiah.com.bd/industries/${slug}` },
      ])}
      {FAQSchema({ faqs: industrySlugFaqs })}
      <IndustryPageClient slug={slug} />
    </>
  );
}
