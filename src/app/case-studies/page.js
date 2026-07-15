import CaseStudiesClient from "./CaseStudiesClient";
import { BreadcrumbSchema } from "@/components/Schema";

export const metadata = {
  title: "SEO Case Studies — Kanok Miah | Local SEO Expert Dhaka",
  description: "Real SEO case studies from Bangladesh. See how Kanok Miah helped Dhaka restaurants, e-commerce stores, and local businesses rank higher on Google.",
  alternates: { canonical: "https://kanokmiah.com.bd/case-studies" },
  openGraph: {
    title: "Case Studies — Kanok Miah | SEO Expert in Dhaka, Bangladesh",
    description: "Real SEO case studies from Bangladesh. See how local businesses rank higher on Google with proven strategies.",
    url: "https://kanokmiah.com.bd/case-studies",
    images: [{ url: "https://kanokmiah.com.bd/kanok-miah-profile.webp", width: 400, height: 400, alt: "Kanok Miah — SEO Expert Dhaka" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "Case Studies — Kanok Miah | SEO Expert in Dhaka, Bangladesh",
    description: "Real SEO case studies from Bangladesh businesses.",
    images: ["https://kanokmiah.com.bd/kanok-miah-profile.webp"],
  },
};

export default function CaseStudiesPage() {
  return (
    <>
      {BreadcrumbSchema([
        { name: "Home", url: "https://kanokmiah.com.bd" },
        { name: "Case Studies", url: "https://kanokmiah.com.bd/case-studies" },
      ])}
      <script type="application/ld+json" dangerouslySetInnerHTML={{__html: JSON.stringify({
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "SEO Case Studies | Kanok Miah",
        "description": "Real SEO case studies showing how Bangladeshi businesses achieved first-page rankings.",
        "url": "https://kanokmiah.com.bd/case-studies",
        "mainEntity": {
          "@type": "Blog",
          "name": "Kanok Miah SEO Blog",
          "description": "Real SEO case studies and results."
        }
      })}} />
      <CaseStudiesClient />
    </>
  );
}
