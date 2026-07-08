import services from "../data";
import ServicePageClient from "./ServicePageClient";

export function generateStaticParams() {
  return services.map((svc) => ({ slug: svc.slug }));
}

export function generateMetadata({ params }) {
  const svc = services.find((s) => s.slug === params.slug);
  if (!svc) return {};
  return {
    title: `${svc.title} — Md Kanok Miah | SEO Expert in Dhaka, Bangladesh`,
    description: svc.desc || svc.shortDesc,
    alternates: { canonical: `/services/${svc.slug}` },
    openGraph: {
      title: `${svc.title} — Md Kanok Miah | SEO Expert in Dhaka, Bangladesh`,
      description: svc.shortDesc,
      url: `https://kanokmiah.com.bd/services/${svc.slug}`,
    },
  };
}

export default function ServicePage({ params }) {
  return <ServicePageClient slug={params.slug} />;
}
