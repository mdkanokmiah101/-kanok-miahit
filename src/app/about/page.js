import AboutClient from "./AboutClient";
import { BreadcrumbSchema } from "@/components/Schema";

export const metadata = {
  title: "About Me",
  description: "Learn about Md Kanok Miah — Bangladesh's trusted SEO expert with 6+ years of experience. Helping businesses in Dhaka, Chittagong, and Sylhet rank higher on Google with proven SEO strategies.",
  alternates: { canonical: "/about" },
  openGraph: {
    title: "About Me",
    description: "Learn about Md Kanok Miah — Bangladesh's trusted SEO expert with 6+ years of experience.",
    url: "https://kanokmiah.com.bd/about",
    images: [{ url: "/kanok-miah-profile.webp", width: 400, height: 400, alt: "Md Kanok Miah — SEO Expert Dhaka" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "About Me — Md Kanok Miah",
    description: "Learn about Md Kanok Miah — Bangladesh's trusted SEO expert with 6+ years of experience.",
    images: ["/kanok-miah-profile.webp"],
  },
};

export default function AboutPage() {
  return (
    <>
      {BreadcrumbSchema([
        { name: "Home", url: "https://kanokmiah.com.bd" },
        { name: "About", url: "https://kanokmiah.com.bd/about" },
      ])}
      <AboutClient />
    </>
  );
}
