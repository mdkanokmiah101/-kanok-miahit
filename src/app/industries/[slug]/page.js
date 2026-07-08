import industries from "../data";
import IndustryPageClient from "./IndustryPageClient";

export function generateStaticParams() {
  return industries.map((ind) => ({ slug: ind.slug }));
}

export async function generateMetadata({ params }) {
  const { slug } = await params;
  const ind = industries.find((i) => i.slug === slug);
  if (!ind) return {};
  return {
    title: ind.title,
    description: ind.desc,
    alternates: { canonical: `/industries/${ind.slug}` },
    openGraph: {
      title: ind.title,
      description: ind.desc,
      url: `https://kanokmiah.com.bd/industries/${ind.slug}`,
    },
  };
}

export default async function IndustryPage({ params }) {
  const { slug } = await params;
  return <IndustryPageClient slug={slug} />;
}
