import industries from "../data";
import IndustryPageClient from "./IndustryPageClient";

export function generateStaticParams() {
  return industries.map((ind) => ({ slug: ind.slug }));
}

export function generateMetadata({ params }) {
  const ind = industries.find((i) => i.slug === params.slug);
  if (!ind) return {};
  return {
    title: `${ind.title} — Md Kanok Miah | Industry SEO Expert in Bangladesh`,
    description: ind.desc,
    alternates: { canonical: `/industries/${ind.slug}` },
    openGraph: {
      title: `${ind.title} — Md Kanok Miah | Industry SEO Expert in Bangladesh`,
      description: ind.desc,
      url: `https://kanokmiah.com.bd/industries/${ind.slug}`,
    },
  };
}

export default function IndustryPage({ params }) {
  return <IndustryPageClient slug={params.slug} />;
}
