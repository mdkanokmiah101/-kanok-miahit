import HomeClient from "./HomeClient";

export const metadata = {
  title: "Top SEO Expert in Dhaka | Md Kanok Miah — #1 SEO Specialist",
  description:
    "Top SEO expert in Dhaka, Bangladesh with 6+ years of experience. Md Kanok Miah boosts rankings, traffic & leads — Local SEO, Technical SEO, GEO.",
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
    title: "Top SEO Expert in Dhaka | Md Kanok Miah — #1 SEO Specialist",
    description:
      "Looking for the best SEO expert in Dhaka, Bangladesh? Md Kanok Miah is a top-rated SEO specialist. Get higher rankings and more traffic with proven SEO strategies.",
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
    title: "Top SEO Expert in Dhaka | Md Kanok Miah — #1 SEO Specialist",
    description:
      "Looking for the best SEO expert in Dhaka, Bangladesh? Md Kanok Miah helps businesses rank higher, grow faster, dominate search.",
    images: ["https://kanokmiah.com.bd/kanok-miah-profile.webp"],
  },
  robots: {
    index: true,
    follow: true,
    "max-snippet": -1,
    "max-image-preview": "large",
  },
};

export default function HomePage() {
  return <HomeClient />;
}