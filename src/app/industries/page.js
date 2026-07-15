import IndustriesClient from "./IndustriesClient";
import { BreadcrumbSchema } from "@/components/Schema";

export const metadata = {
  title: "SEO by Industry — Bangladesh | Kanok Miah | SEO Expert",
  description: "Industry-specific SEO for Bangladesh — Garments, E-commerce, Real Estate, Healthcare, Education, Food and more. Expert strategies from Kanok Miah.",
  alternates: { canonical: "https://kanokmiah.com.bd/industries" },
  openGraph: {
    title: "Industries — Kanok Miah | SEO Expert in Dhaka, Bangladesh",
    description: "Industry-specific SEO for Bangladesh from Kanok Miah.",
    url: "https://kanokmiah.com.bd/industries",
    siteName: "Kanok Miah",
    images: [{ url: "https://kanokmiah.com.bd/kanok-miah-profile.webp", width: 400, height: 400, alt: "Kanok Miah \u2014 SEO Expert Dhaka" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "Industries — Kanok Miah | SEO Expert in Dhaka, Bangladesh",
    description: "Industry-specific SEO for Bangladesh from Kanok Miah.",
    images: ["https://kanokmiah.com.bd/kanok-miah-profile.webp"],
  },
};

const industriesFaqs = [
  { question: "Which industries do you specialize in?", answer: "I specialize in SEO for a wide range of industries including real estate, e-commerce, healthcare, education, hospitality, local services, and manufacturing. Each industry strategy is tailored to its unique competitive landscape and customer search behaviour." },
  { question: "How is SEO different for each industry?", answer: "Every industry has unique search patterns, customer journeys, and competitive dynamics. For example, e-commerce SEO focuses on product optimization and category structure, while local service SEO emphasizes Google Business Profile and local citations. I create customized strategies for each sector." },
  { question: "Do you work with B2B companies?", answer: "Absolutely. B2B SEO focuses on informational content, long-form guides, and lead generation through thought leadership. I tailor my approach based on your business model, whether B2B, B2C, or both." },
  { question: "Can you help my industry rank higher?", answer: "Yes, regardless of your industry, I can help you achieve higher rankings. I start with a thorough analysis of your industry's competitive landscape, identify untapped keyword opportunities, and implement proven SEO strategies that drive measurable results." },
];

export default function IndustriesPage() {
  return (
    <>
      {BreadcrumbSchema([
        { name: "Home", url: "https://kanokmiah.com.bd" },
        { name: "Industries", url: "https://kanokmiah.com.bd/industries" },
      ])}
      <script type="application/ld+json" dangerouslySetInnerHTML={{__html: JSON.stringify({
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "Industries We Serve | Kanok Miah",
        "description": "Industry-specific SEO for Bangladesh — Garments, E-commerce, Real Estate, Healthcare, Education, and more.",
        "url": "https://kanokmiah.com.bd/industries",
        "mainEntity": {
          "@type": "Blog",
          "name": "Kanok Miah Industries",
          "description": "Industry-specific SEO solutions for Bangladeshi businesses."
        }
      })}} />
      <IndustriesClient />
    </>
  );
}
