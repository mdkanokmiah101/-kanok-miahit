import ContactClient from "./ContactClient";
import { BreadcrumbSchema, FAQSchema, ContactPageSchema } from "@/components/Schema";

export const metadata = {
  title: "Contact Me",
  description: "Contact Md Kanok Miah — the best SEO expert in Dhaka, Bangladesh. Get a free SEO audit for your business. Call +880 1712-883101 for a consultation.",
  alternates: { canonical: "/contact" },
  openGraph: {
    title: "Contact Md Kanok Miah — SEO Expert in Dhaka, Bangladesh",
    description: "Contact Md Kanok Miah — the best SEO expert in Dhaka, Bangladesh. Get a free SEO audit for your business. Call +880 1712-883101 for a consultation.",
    url: "https://kanokmiah.com.bd/contact",
    images: [{ url: "/kanok-miah-profile.webp", width: 400, height: 400, alt: "Md Kanok Miah — SEO Expert Dhaka" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "Contact Me — Md Kanok Miah",
    description: "Contact Md Kanok Miah for a free SEO audit. Get expert help for your Bangladesh business.",
    images: ["/kanok-miah-profile.webp"],
  },
};

const contactFaqs = [
  { question: "How quickly do you respond?", answer: "I typically respond to all inquiries within 24 hours. For urgent matters, WhatsApp messages are usually answered within a few hours. I value your time and make prompt communication a priority." },
  { question: "Do you offer free SEO audit?", answer: "Yes! I offer a completely free SEO audit worth BDT 5,000. I'll analyze your website's technical health, on-page optimization, current rankings, and provide a roadmap of opportunities — with no obligation to proceed." },
  { question: "What information do you need to start?", answer: "To get started, I need your website URL, a brief overview of your business goals, target keywords if you have them, and access to your Google Search Console and Analytics accounts if available. Everything else I can gather during the audit." },
  { question: "Can you work with my existing website?", answer: "Absolutely. I can optimize any existing website regardless of its current state — from sites with no SEO foundation to those already ranking but needing improvement. I work with all platforms including WordPress, Shopify, Wix, and custom-built sites." },
  { question: "What payment methods do you accept?", answer: "I accept multiple payment methods including bank transfer (within Bangladesh), bKash, Nagad, and international payments via PayPal. Payment terms are discussed and agreed upon before any work begins." },
];

export default function ContactPage() {
  return (
    <>
      {ContactPageSchema()}
      {BreadcrumbSchema([
        { name: "Home", url: "https://kanokmiah.com.bd" },
        { name: "Contact", url: "https://kanokmiah.com.bd/contact" },
      ])}
      {FAQSchema({ faqs: contactFaqs })}
      <ContactClient />
    </>
  );
}
