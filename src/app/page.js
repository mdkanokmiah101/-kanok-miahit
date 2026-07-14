import HomeClient from "./HomeClient";
import { LocalBusinessSchema } from "@/components/Schema";

export const metadata = {
  title: "Best SEO Expert in Dhaka & Bangladesh | Md Kanok Miah",
  description:
    "Rank higher with Md Kanok Miah, the best SEO expert in Dhaka & Bangladesh. 6+ years, 210+ SEO wins. Free SEO audit — Call 01604-809110.",
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
    "Md Kanok Miah",
  ],
  authors: [{ name: "Md Kanok Miah" }],
  creator: "Md Kanok Miah",
  publisher: "Md Kanok Miah",
  alternates: {
    canonical: "https://kanokmiah.com.bd/",
  },
  openGraph: {
    type: "website",
    locale: "en_US",
    siteName: "Md Kanok Miah",
    title: "Best SEO Expert in Dhaka | Md Kanok Miah | 210+ SEO Successes",
    description:
      "Rank higher on Google & AI Search with Md Kanok Miah, a trusted SEO expert in Dhaka. 6+ years, 210+ successful SEO campaigns. Free SEO audit—Call 01604-809110.",
    url: "https://kanokmiah.com.bd",
    images: [
      {
        url: "https://kanokmiah.com.bd/kanok-miah-profile.webp",
        width: 400,
        height: 400,
        alt: "Md Kanok Miah — Best SEO Expert in Dhaka, Bangladesh",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "Best SEO Expert in Dhaka | Md Kanok Miah | 210+ SEO Successes",
    description:
      "Rank higher on Google & AI Search with Md Kanok Miah, a trusted SEO expert in Dhaka. 6+ years, 210+ successful SEO campaigns. Free SEO audit—Call 01604-809110.",
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
      <HomeClient />
    </>
  );
}