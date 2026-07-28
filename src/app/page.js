import HomeClient from "./HomeClient";
import {
  BreadcrumbSchema,
  FAQSchema,
  AggregateRatingSchema,
  ReviewSchema,
  VideoObjectSchema,
} from "@/components/Schema";
import { homepageFaqs } from "./faq-data";

export const metadata = {
  title: "Best SEO Expert in Dhaka, Bangladesh | Kanok Miah",
  description:
    "Best SEO expert in Bangladesh? Kanok Miah is a top-rated SEO specialist in Dhaka. 6+ years, 210+ wins, 350+ clients. Free SEO audit — Call 01604-809110.",
  keywords: [
    "best SEO expert in Dhaka",
    "SEO expert Dhaka",
    "SEO specialist Bangladesh",
    "local SEO Bangladesh",
    "Bangladesh SEO expert",
    "SEO consultant Dhaka",
    "on-page SEO",
    "technical SEO",
    "link building Bangladesh",
    "semantic SEO",
    "GEO optimization",
    "Kanok Miah",
  ],
  authors: [{ name: "Kanok Miah" }],
  creator: "Kanok Miah",
  publisher: "Kanok Miah",
  alternates: {
    canonical: "https://kanokmiah.com.bd/",
  },
  openGraph: {
    type: "website",
    locale: "en_US",
    siteName: "Kanok Miah",
    title: "Best SEO Expert in Dhaka, Bangladesh | Kanok Miah",
    description:
      "Rank higher on Google and AI Search with Kanok Miah, the best SEO expert in Bangladesh and a trusted SEO specialist in Dhaka. 6+ years, 210+ successful SEO campaigns. Free SEO audit—Call 01604-809110.",
    url: "https://kanokmiah.com.bd",
    images: [
      {
        url: "https://kanokmiah.com.bd/kanok-miah-profile.webp",
        width: 1200,
        height: 630,
        alt: "Kanok Miah — Best SEO Expert in Dhaka, Bangladesh",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "Best SEO Expert in Dhaka, Bangladesh | Kanok Miah",
    description:
      "Rank higher on Google and AI Search with Kanok Miah, the best SEO expert in Bangladesh and a trusted SEO specialist in Dhaka. 6+ years, 210+ successful SEO campaigns. Free SEO audit—Call 01604-809110.",
    images: ["https://kanokmiah.com.bd/kanok-miah-profile.webp"],
  },
  robots: {
    index: true,
    follow: true,
    "max-snippet": -1,
    "max-image-preview": "large",
  },
  verification: {
    google: "etLH7vKLG9Iph0mFN1a8sOYhxFptpi_h_VYRk3mUFvM",
    other: {
      "msvalidate.01": "A10B9573E2B9D84E27B9BCE37CCB8B28",
    },
  },
};

export default function HomePage() {
  const homepageReviews = [
    {
      author: "Client (Google Review)",
      rating: "5",
      body: "Excellent SEO services! Highly recommended for local SEO in Dhaka.",
      datePublished: "2025-06-15",
    },
    {
      author: "Client (Google Review)",
      rating: "5",
      body: "Kanok helped my business rank on Google Maps. Great results and professional service.",
      datePublished: "2025-05-20",
    },
    {
      author: "Client (Google Review)",
      rating: "5",
      body: "Professional SEO expert with deep knowledge of technical SEO and link building.",
      datePublished: "2025-04-10",
    },
  ];

  const homepageVideos = [
    {
      name: "Client Review 1 - Kanok Miah SEO Services",
      description: "Client testimonial about SEO services provided by Kanok Miah",
      embedUrl: "https://www.youtube.com/embed/eIyD-ugY7_0",
      uploadDate: "2024-06-01",
    },
    {
      name: "Client Review 2 - Kanok Miah SEO Services",
      description: "Client testimonial about SEO services provided by Kanok Miah",
      embedUrl: "https://www.youtube.com/embed/hqtG7FM_ZAY",
      uploadDate: "2024-06-01",
    },
  ];

  return (
    <>
      {AggregateRatingSchema({ ratingValue: "4.9", bestRating: "5", ratingCount: "108" })}
      <ReviewSchema reviews={homepageReviews} />
      <VideoObjectSchema videos={homepageVideos} />
      {BreadcrumbSchema([
        { name: "Home", url: "https://kanokmiah.com.bd" },
        { name: "Best SEO Expert in Dhaka", url: "https://kanokmiah.com.bd" },
      ])}
      <FAQSchema faqs={homepageFaqs} />
      <HomeClient faqs={homepageFaqs} />
    </>
  );
}
