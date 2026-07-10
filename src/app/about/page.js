import AboutClient from "./AboutClient";
import { BreadcrumbSchema, FAQSchema, AboutPageSchema } from "@/components/Schema";

export const metadata = {
  title: "About Md Kanok Miah — SEO Expert in Dhaka, Bangladesh",
  description: "Learn about Md Kanok Miah \u2014 Bangladesh's trusted SEO expert with 6+ years of experience helping Dhaka businesses rank higher on Google.",
  alternates: { canonical: "https://kanokmiah.com.bd/about" },
  openGraph: {
    title: "About Md Kanok Miah — SEO Expert in Dhaka, Bangladesh",
    description: "Learn about Md Kanok Miah — Bangladesh's trusted SEO expert with 6+ years of experience.",
    url: "https://kanokmiah.com.bd/about",
    images: [{ url: "https://kanokmiah.com.bd/kanok-miah-profile.webp", width: 400, height: 400, alt: "Md Kanok Miah — SEO Expert Dhaka" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "About Me — Md Kanok Miah",
    description: "Learn about Md Kanok Miah — Bangladesh's trusted SEO expert with 6+ years of experience.",
    images: ["https://kanokmiah.com.bd/kanok-miah-profile.webp"],
  },
};

const aboutFaqs = [
  { question: "What experience does Md Kanok Miah have?", answer: "Md Kanok Miah has over 6 years of hands-on SEO experience, helping 50+ Bangladeshi businesses achieve first-page rankings on Google. His expertise spans local SEO, technical SEO, link building, semantic SEO, and GEO/AI search optimization." },
  { question: "What areas of Bangladesh do you serve?", answer: "I provide SEO services for businesses throughout Bangladesh including Dhaka, Chittagong, Sylhet, Khulna, Rajshahi, and all other major cities. My local SEO strategies are customized for each city's specific market." },
  { question: "What types of businesses do you work with?", answer: "I work with a diverse range of clients including local service businesses, e-commerce stores (Shopify, Daraz), real estate agencies, healthcare providers, educational institutions, and hospitality businesses across Bangladesh." },
  { question: "Do you offer a free consultation?", answer: "Yes! I offer a completely free initial consultation to discuss your business goals and SEO needs. During this call, I'll provide preliminary insights and recommendations with no obligation to proceed." },
  { question: "How do I get started with your services?", answer: "Getting started is simple: contact me through the website form, call +880 1712-883101, or send a WhatsApp message. I'll begin with a free SEO audit of your website and provide a customized strategy proposal." },
];

export default function AboutPage() {
  return (
    <>
      {AboutPageSchema()}
      {BreadcrumbSchema([
        { name: "Home", url: "https://kanokmiah.com.bd" },
        { name: "About", url: "https://kanokmiah.com.bd/about" },
      ])}
      {FAQSchema({ faqs: aboutFaqs })}
      <AboutClient />
    </>
  );
}
