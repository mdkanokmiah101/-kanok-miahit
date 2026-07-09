import FaqClient from "./FaqClient";
import { BreadcrumbSchema, FAQSchema } from "@/components/Schema";

const faqData = [
  {
    question: "What is Local SEO and why is it important for Bangladeshi businesses?",
    answer: "Local SEO optimizes your online presence to attract more customers from relevant local searches. For Bangladeshi businesses, it's crucial because most customers search for services \"near me\" or \"in Dhaka.\" Local SEO helps you appear in Google Maps, local pack results, and organic search for location-specific queries — driving foot traffic and phone calls from nearby customers actively looking for your services.",
  },
  {
    question: "How long does SEO take to show results in Bangladesh?",
    answer: "SEO typically takes 3–6 months to show meaningful results for most businesses in Bangladesh. However, initial improvements in rankings and traffic can appear within 4–6 weeks for low-competition keywords. Factors like website condition, industry competition, content quality, and link-building speed all influence the timeline.",
  },
  {
    question: "What is the difference between GEO and traditional SEO?",
    answer: "GEO (Generative Engine Optimization) optimizes content for AI-powered search engines like ChatGPT, Google AI Overviews, Gemini, and Perplexity. Traditional SEO focuses on keyword rankings and backlinks for Google's blue-link results. GEO uses entity-based content, authoritative citations, and structured data to help AI models accurately cite your information.",
  },
  {
    question: "How much does SEO cost for small businesses in Bangladesh?",
    answer: "SEO pricing for small businesses varies based on competition and scope. Monthly retainers typically range from BDT 15,000 to BDT 50,000. A basic plan includes local SEO and on-page optimization, while comprehensive packages include technical SEO, link building, content creation, and monthly reporting.",
  },
  {
    question: "Do I need both a website and Google Business Profile?",
    answer: "Yes! A Google Business Profile helps you appear in Google Maps and local pack results, while a website gives you a hub for content, detailed service pages, and blog posts. Both are essential for a complete local SEO strategy in Bangladesh.",
  },
  {
    question: "Can SEO work for e-commerce stores in Bangladesh?",
    answer: "Absolutely. E-commerce SEO optimizes product pages, category pages, and site structure to rank for product-related searches. For Daraz sellers, I optimize both Daraz internal search rankings and Google organic search visibility.",
  },
];

export const metadata = {
  title: "FAQ \u2014 SEO Questions Answered",
  description: "FAQ about SEO services in Bangladesh. Learn about Local SEO, Technical SEO, Link Building, GEO/AI Search and more from Md Kanok Miah.",
  alternates: { canonical: "/faq" },
  openGraph: {
    title: "FAQ \u2014 SEO Questions Answered",
    description: "Get answers to common SEO questions for Bangladeshi businesses. Local SEO, Technical SEO, Link Building, GEO/AI Search explained by Md Kanok Miah.",
    url: "https://kanokmiah.com.bd/faq",
    images: [{ url: "/kanok-miah-profile.webp", width: 400, height: 400, alt: "Md Kanok Miah \u2014 SEO Expert Dhaka" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "FAQ \u2014 SEO Questions Answered",
    description: "Get answers to common SEO questions for Bangladeshi businesses.",
    images: ["/kanok-miah-profile.webp"],
  },
};

export default function FaqPage() {
  return (
    <>
      {BreadcrumbSchema([
        { name: "Home", url: "https://kanokmiah.com.bd" },
        { name: "FAQ", url: "https://kanokmiah.com.bd/faq" },
      ])}
      {FAQSchema({ faqs: faqData })}
      <FaqClient />
    </>
  );
}
