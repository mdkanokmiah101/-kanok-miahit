import ServicesClient from "./ServicesClient";

export const metadata = {
  title: "SEO Services",
  description: "Complete SEO solutions for Bangladeshi businesses — Local SEO, Technical SEO, Link Building, GEO/AI Search, E-commerce SEO, and more. Get a free SEO audit from Dhaka's trusted SEO expert.",
  alternates: { canonical: "/services" },
  openGraph: {
    title: "SEO Services",
    description: "Complete SEO solutions for Bangladeshi businesses — Local SEO, Technical SEO, Link Building, GEO/AI Search, E-commerce SEO.",
    url: "https://kanokmiah.com.bd/services",
  },
};

export default function ServicesPage() {
  return <ServicesClient />;
}
