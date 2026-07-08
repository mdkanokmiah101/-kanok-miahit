import IndustriesClient from "./IndustriesClient";

export const metadata = {
  title: "Industries We Serve — Md Kanok Miah | SEO Expert in Bangladesh",
  description: "Industry-specific SEO solutions for Bangladesh — Garments and Textile, E-commerce, Real Estate, Healthcare, Education, Food and Restaurant, and more. Tailored SEO strategies from Md Kanok Miah.",
  alternates: { canonical: "/industries" },
  openGraph: {
    title: "Industries We Serve — Md Kanok Miah | SEO Expert in Bangladesh",
    description: "Industry-specific SEO solutions for Bangladesh from Md Kanok Miah.",
    url: "https://kanokmiah.com.bd/industries",
  },
};

export default function IndustriesPage() {
  return <IndustriesClient />;
}
