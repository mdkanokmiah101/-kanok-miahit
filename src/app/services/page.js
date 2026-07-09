import ServicesClient from "./ServicesClient";
import { BreadcrumbSchema } from "@/components/Schema";

export const metadata = {
  title: "SEO Services",
  description: "Complete SEO solutions for Bangladeshi businesses — Local SEO, Technical SEO, Link Building, GEO/AI Search, E-commerce SEO, and more. Get a free SEO audit from Dhaka's trusted SEO expert.",
  alternates: { canonical: "/services" },
  openGraph: {
    title: "SEO Services",
    description: "Complete SEO solutions for Bangladeshi businesses — Local SEO, Technical SEO, Link Building, GEO/AI Search, E-commerce SEO.",
    url: "https://kanokmiah.com.bd/services",
    images: [{ url: "/kanok-miah-profile.webp", width: 400, height: 400, alt: "Md Kanok Miah — SEO Expert Dhaka" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "SEO Services — Md Kanok Miah",
    description: "Complete SEO solutions for Bangladeshi businesses — Local SEO, Technical SEO, Link Building, GEO/AI Search, E-commerce SEO.",
    images: ["/kanok-miah-profile.webp"],
  },
};

export default function ServicesPage() {
  return (
    <>
      {BreadcrumbSchema([
        { name: "Home", url: "https://kanokmiah.com.bd" },
        { name: "Services", url: "https://kanokmiah.com.bd/services" },
      ])}
      <ServicesClient />
    </>
  );
}
