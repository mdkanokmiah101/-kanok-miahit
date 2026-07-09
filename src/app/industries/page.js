import IndustriesClient from "./IndustriesClient";
import { BreadcrumbSchema } from "@/components/Schema";

export const metadata = {
  title: "Industries We Serve",
  description: "Industry-specific SEO solutions for Bangladesh — Garments and Textile, E-commerce, Real Estate, Healthcare, Education, Food and Restaurant, and more. Tailored SEO strategies from Md Kanok Miah.",
  alternates: { canonical: "/industries" },
  openGraph: {
    title: "Industries We Serve",
    description: "Industry-specific SEO solutions for Bangladesh from Md Kanok Miah.",
    url: "https://kanokmiah.com.bd/industries",
    siteName: "Md Kanok Miah",
    images: [{ url: "/kanok-miah-profile.webp", width: 400, height: 400, alt: "Md Kanok Miah — SEO Expert Dhaka" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "Industries We Serve",
    description: "Industry-specific SEO solutions for Bangladesh from Md Kanok Miah.",
    images: ["/kanok-miah-profile.webp"],
  },
};

export default function IndustriesPage() {
  return (
    <>
      {BreadcrumbSchema([
        { name: "Home", url: "https://kanokmiah.com.bd" },
        { name: "Industries", url: "https://kanokmiah.com.bd/industries" },
      ])}
      <IndustriesClient />
    </>
  );
}
