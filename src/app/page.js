import HomeClient from "./HomeClient";
import { LocalBusinessSchema, BreadcrumbSchema } from "@/components/Schema";

export const metadata = {
  title: "Best SEO Expert in Dhaka & Bangladesh | Kanok Miah",
  description:
    "Rank higher with Kanok Miah, the best SEO expert in Dhaka & Bangladesh. 6+ years, 210+ SEO wins. Free SEO audit — Call 01604-809110.",
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
      "Rank higher on Google & AI Search with Kanok Miah, a trusted SEO expert in Dhaka, Bangladesh. 6+ years, 210+ successful SEO campaigns. Free SEO audit—Call 01604-809110.",
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
      "Rank higher on Google & AI Search with Kanok Miah, a trusted SEO expert in Dhaka, Bangladesh. 6+ years, 210+ successful SEO campaigns. Free SEO audit—Call 01604-809110.",
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
  return (
    <>
      {LocalBusinessSchema()}
      {BreadcrumbSchema([
        { name: "Home", url: "https://kanokmiah.com.bd" },
        { name: "SEO Expert Dhaka", url: "https://kanokmiah.com.bd" },
      ])}
      <HomeClient />
    </>
  );
}
