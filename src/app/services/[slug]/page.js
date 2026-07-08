import services from "../data";
import ServicePageClient from "./ServicePageClient";

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
    },
  };
}

export default async function ServicePage({ params }) {
  const { slug } = await params;
  return <ServicePageClient slug={slug} />;
}
