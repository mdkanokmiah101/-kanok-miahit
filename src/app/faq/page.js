import FaqClient from "./FaqClient";

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
  return <FaqClient />;
}
