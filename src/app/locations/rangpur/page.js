import RangpurClient from "./RangpurClient";

export const metadata = {
  title: "Local SEO Services in Rangpur — Md Kanok Miah | SEO Expert Dhaka, Bangladesh",
  description: "Professional local SEO services in Rangpur, Bangladesh. Dominate Google Maps and attract more customers in Rangpur city with proven local SEO.",
  alternates: { canonical: "/locations/rangpur" },
  openGraph: {
    title: "Local SEO Services in Rangpur — Md Kanok Miah | SEO Expert in Dhaka, Bangladesh",
    description: "Professional local SEO services in Rangpur, Bangladesh. Dominate Google Maps and attract more customers in Rangpur city.",
    url: "https://kanokmiah.com.bd/locations/rangpur",
    images: [{ url: "https://kanokmiah.com.bd/kanok-miah-profile.webp", width: 400, height: 400, alt: "Md Kanok Miah — SEO Expert Dhaka" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "Local SEO Services in Rangpur — Md Kanok Miah | SEO Expert in Dhaka, Bangladesh",
    description: "Professional local SEO services in Rangpur, Bangladesh.",
    images: ["https://kanokmiah.com.bd/kanok-miah-profile.webp"],
  },
};

export default function RangpurPage() {
  return <RangpurClient />;
}
