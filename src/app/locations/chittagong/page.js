import ChittagongClient from "./ChittagongClient";

export const metadata = {
  title: "Local SEO Services in Chittagong",
  description: "Professional local SEO services in Chittagong, Bangladesh. Rank higher on Google Maps and attract more customers with expert local SEO.",
  alternates: { canonical: "/locations/chittagong" },
  openGraph: {
    title: "Local SEO Services in Chittagong — Md Kanok Miah | SEO Expert in Dhaka, Bangladesh",
    description: "Professional local SEO services in Chittagong, Bangladesh. Rank higher on Google Maps and attract more customers in Chittagong port city.",
    url: "https://kanokmiah.com.bd/locations/chittagong",
    images: [{ url: "/kanok-miah-profile.webp", width: 400, height: 400, alt: "Md Kanok Miah — SEO Expert Dhaka" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "Local SEO Services in Chittagong — Md Kanok Miah | SEO Expert in Dhaka, Bangladesh",
    description: "Professional local SEO services in Chittagong, Bangladesh.",
    images: ["/kanok-miah-profile.webp"],
  },
};

export default function ChittagongPage() {
  return <ChittagongClient />;
}
