import PortfolioClient from "./PortfolioClient";
import { BreadcrumbSchema } from "@/components/Schema";

export const metadata = {
  title: "SEO Portfolio — Md Kanok Miah | 210+ Projects in Bangladesh",
  description: "View the SEO portfolio of Md Kanok Miah — 210+ projects completed, 50+ happy clients in Dhaka, Chittagong, Sylhet and across Bangladesh.",
  alternates: { canonical: "https://kanokmiah.com.bd/portfolio" },
  openGraph: {
    title: "Portfolio — Md Kanok Miah | SEO Expert in Dhaka, Bangladesh",
    description: "View the SEO portfolio of Md Kanok Miah — 210+ projects completed, 50+ happy clients across Bangladesh.",
    url: "https://kanokmiah.com.bd/portfolio",
    images: [{ url: "https://kanokmiah.com.bd/kanok-miah-profile.webp", width: 400, height: 400, alt: "Md Kanok Miah — SEO Expert Dhaka" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "Portfolio — Md Kanok Miah | SEO Expert in Dhaka, Bangladesh",
    description: "View the SEO portfolio of Md Kanok Miah — 210+ projects, 50+ clients across Bangladesh.",
    images: ["https://kanokmiah.com.bd/kanok-miah-profile.webp"],
  },
};

export default function PortfolioPage() {
  return (
    <>
      {BreadcrumbSchema([
        { name: "Home", url: "https://kanokmiah.com.bd" },
        { name: "Portfolio", url: "https://kanokmiah.com.bd/portfolio" },
      ])}
      <script type="application/ld+json" dangerouslySetInnerHTML={{__html: JSON.stringify({
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "SEO Portfolio | Md Kanok Miah",
        "description": "SEO portfolio showcasing 210+ projects and 50+ clients across Bangladesh.",
        "url": "https://kanokmiah.com.bd/portfolio",
        "mainEntity": {
          "@type": "Blog",
          "name": "Md Kanok Miah SEO Portfolio",
          "description": "SEO portfolio and case results."
        }
      })}} />
      <PortfolioClient />
    </>
  );
}
