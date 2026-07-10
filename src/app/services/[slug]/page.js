import services from "../data";
import ServicePageClient from "./ServicePageClient";
import { BreadcrumbSchema, ServiceSchema } from "@/components/Schema";
import { notFound } from "next/navigation";

export function generateStaticParams() {
  return services.map((svc) => ({ slug: svc.slug }));
}

function truncateMeta(str, maxLen = 155) {
  if (!str) return "";
  if (str.length <= maxLen) return str;
  // Truncate at the last space before maxLen
  const truncated = str.slice(0, maxLen);
  const lastSpace = truncated.lastIndexOf(" ");
  return (lastSpace > 0 ? truncated.slice(0, lastSpace) : truncated) + "…";
}

export async function generateMetadata({ params }) {
  const { slug } = await params;
  const svc = services.find((s) => s.slug === slug);
  if (!svc) return { title: "Service Not Found — Md Kanok Miah" };
  const metaDesc = truncateMeta(svc.shortDesc);
  return {
    title: `${svc.title} Services in Bangladesh — Md Kanok Miah`,
    description: metaDesc,
    alternates: { canonical: `/services/${svc.slug}` },
    openGraph: {
      title: `${svc.title} — Md Kanok Miah | SEO Expert in Dhaka, Bangladesh`,
      description: metaDesc,
      url: `https://kanokmiah.com.bd/services/${svc.slug}`,
      images: [{ url: "https://kanokmiah.com.bd/kanok-miah-profile.webp", width: 400, height: 400, alt: "Md Kanok Miah — SEO Expert Dhaka" }],
    },
    twitter: {
      card: "summary_large_image",
      title: `${svc.title} — Md Kanok Miah | SEO Expert in Dhaka, Bangladesh`,
      description: metaDesc,
      images: ["https://kanokmiah.com.bd/kanok-miah-profile.webp"],
    },
  };
}

export default async function ServicePage({ params }) {
  const { slug } = await params;
  const svc = services.find((s) => s.slug === slug);
  if (!svc) notFound();
  return (
    <>
      {BreadcrumbSchema([
        { name: "Home", url: "https://kanokmiah.com.bd" },
        { name: "Services", url: "https://kanokmiah.com.bd/services" },
        { name: svc?.title || slug, url: `https://kanokmiah.com.bd/services/${slug}` },
      ])}
      {svc && ServiceSchema(svc)}
      <ServicePageClient slug={slug} />
    </>
  );
}
