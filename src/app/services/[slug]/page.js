import services from "../data";
import ServicePageClient from "./ServicePageClient";
import { BreadcrumbSchema } from "@/components/Schema";

export function generateStaticParams() {
  return services.map((svc) => ({ slug: svc.slug }));
}

export async function generateMetadata({ params }) {
  const { slug } = await params;
  const svc = services.find((s) => s.slug === slug);
  if (!svc) return {};
  return {
    title: svc.title,
    description: svc.desc || svc.shortDesc,
    alternates: { canonical: `/services/${svc.slug}` },
    openGraph: {
      title: svc.title,
      description: svc.shortDesc,
      url: `https://kanokmiah.com.bd/services/${svc.slug}`,
      images: [{ url: "/kanok-miah-profile.webp", width: 400, height: 400, alt: "Md Kanok Miah — SEO Expert Dhaka" }],
    },
    twitter: {
      card: "summary_large_image",
      title: `${svc.title} — Md Kanok Miah`,
      description: svc.shortDesc,
      images: ["/kanok-miah-profile.webp"],
    },
  };
}

export default async function ServicePage({ params }) {
  const { slug } = await params;
  const svc = services.find((s) => s.slug === slug);
  return (
    <>
      {BreadcrumbSchema([
        { name: "Home", url: "https://kanokmiah.com.bd" },
        { name: "Services", url: "https://kanokmiah.com.bd/services" },
        { name: svc?.title || slug, url: `https://kanokmiah.com.bd/services/${slug}` },
      ])}
      <ServicePageClient slug={slug} />
    </>
  );
}
