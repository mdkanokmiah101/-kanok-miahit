import CaseStudiesClient from "./CaseStudiesClient";
import { BreadcrumbSchema, CollectionPageSchema } from "@/components/Schema";

export const metadata = {
  title: "Case Studies",
  description: "Real SEO case studies from Bangladesh. See how Md Kanok Miah helped Dhaka restaurants, e-commerce stores, and local businesses rank higher on Google.",
  alternates: { canonical: "/case-studies" },
  openGraph: {
    title: "Case Studies — Md Kanok Miah | SEO Expert Dhaka, Bangladesh",
    description: "Real SEO case studies from Bangladesh. See how local businesses rank higher on Google with proven strategies.",
    url: "https://kanokmiah.com.bd/case-studies",
    images: [{ url: "/kanok-miah-profile.webp", width: 400, height: 400, alt: "Md Kanok Miah — SEO Expert Dhaka" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "Case Studies — Md Kanok Miah",
    description: "Real SEO case studies from Bangladesh businesses.",
    images: ["/kanok-miah-profile.webp"],
  },
};

export default function CaseStudiesPage() {
  return (
    <>
      {BreadcrumbSchema([
        { name: "Home", url: "https://kanokmiah.com.bd" },
        { name: "Case Studies", url: "https://kanokmiah.com.bd/case-studies" },
      ])}
      {CollectionPageSchema({
        name: "SEO Case Studies | Md Kanok Miah",
        description: "Real SEO case studies showing how Bangladeshi businesses achieved first-page rankings.",
        url: "https://kanokmiah.com.bd/case-studies",
      })}
      <CaseStudiesClient />
    </>
  );
}
