import PortfolioClient from "./PortfolioClient";
import { BreadcrumbSchema, CollectionPageSchema } from "@/components/Schema";

export const metadata = {
  title: "Portfolio",
  description: "View the SEO portfolio of Md Kanok Miah — 350+ projects completed, 50+ happy clients in Dhaka, Chittagong, Sylhet and across Bangladesh.",
  alternates: { canonical: "/portfolio" },
  openGraph: {
    title: "Portfolio — Md Kanok Miah | SEO Expert Dhaka, Bangladesh",
    description: "View the SEO portfolio of Md Kanok Miah — 350+ projects completed, 50+ happy clients across Bangladesh.",
    url: "https://kanokmiah.com.bd/portfolio",
    images: [{ url: "/kanok-miah-profile.webp", width: 400, height: 400, alt: "Md Kanok Miah — SEO Expert Dhaka" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "Portfolio — Md Kanok Miah",
    description: "View the SEO portfolio of Md Kanok Miah — 350+ projects, 50+ clients across Bangladesh.",
    images: ["/kanok-miah-profile.webp"],
  },
};

export default function PortfolioPage() {
  return (
    <>
      {BreadcrumbSchema([
        { name: "Home", url: "https://kanokmiah.com.bd" },
        { name: "Portfolio", url: "https://kanokmiah.com.bd/portfolio" },
      ])}
      {CollectionPageSchema({
        name: "SEO Portfolio | Md Kanok Miah",
        description: "SEO portfolio showcasing 350+ projects and 50+ clients across Bangladesh.",
        url: "https://kanokmiah.com.bd/portfolio",
      })}
      <PortfolioClient />
    </>
  );
}
