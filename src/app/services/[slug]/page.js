import services from "../data";
import ServicePageClient from "./ServicePageClient";

export function generateStaticParams() {
  return services.map((svc) => ({ slug: svc.slug }));
}

export default function ServicePage({ params }) {
  return <ServicePageClient slug={params.slug} />;
}
