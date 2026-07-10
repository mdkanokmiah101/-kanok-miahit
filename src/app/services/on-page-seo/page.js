import services from "../data";
import ServicePageClient from "../[slug]/ServicePageClient";
import { BreadcrumbSchema, ServiceSchema } from "@/components/Schema";
import { notFound } from "next/navigation";

const SLUG = "on-page-seo";

function truncateMeta(str, maxLen = 155) {
  if (!str) return "";
  if (str.length <= maxLen) return str;
  const truncated = str.slice(0, maxLen);
  const lastSpace = truncated.lastIndexOf(" ");
  return (lastSpace > 0 ? truncated.slice(0, lastSpace) : truncated) + "…";
}

export function generateStaticParams() {
  return [{ slug: SLUG }];
}

export const dynamicParams = false;

export async function generateMetadata() {
  const svc = services.find((s) => s.slug === SLUG);
  if (!svc) return { title: "Service Not Found — Md Kanok Miah" };
  const metaDesc = truncateMeta(svc.shortDesc);
  return {
    title: svc.title,
    description: metaDesc,
    alternates: { canonical: `/services/${SLUG}` },
    openGraph: {
      title: `${svc.title} — Md Kanok Miah | SEO Expert in Dhaka, Bangladesh`,
      description: metaDesc,
      url: `https://kanokmiah.com.bd/services/${SLUG}`,
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

export default async function OnPageSeoPage() {
  const svc = services.find((s) => s.slug === SLUG);
  if (!svc) notFound();
  return (
    <>
      {BreadcrumbSchema([
        { name: "Home", url: "https://kanokmiah.com.bd" },
        { name: "Services", url: "https://kanokmiah.com.bd/services" },
        { name: svc.title, url: `https://kanokmiah.com.bd/services/${SLUG}` },
      ])}
      {svc && ServiceSchema(svc)}
      <ServicePageClient slug={SLUG} />
    </>
  );
}
