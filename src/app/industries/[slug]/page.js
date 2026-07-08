import industries from "../data";
import IndustryPageClient from "./IndustryPageClient";

export function generateStaticParams() {
  return industries.map((ind) => ({ slug: ind.slug }));
}

export default function IndustryPage({ params }) {
  return <IndustryPageClient slug={params.slug} />;
}
