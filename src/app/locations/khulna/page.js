import KhulnaClient from "./KhulnaClient";

export const metadata = {
  title: "Local SEO Services in Khulna",
  description: "Professional local SEO services in Khulna, Bangladesh. Rank your business on Google Maps and attract more customers with expert local SEO.",
  alternates: { canonical: "/locations/khulna" },
  openGraph: {
    title: "Local SEO Services in Khulna — Md Kanok Miah | SEO Expert in Dhaka, Bangladesh",
    description: "Professional local SEO services in Khulna, Bangladesh. Rank on Google Maps and attract more customers in Khulna city.",
    url: "https://kanokmiah.com.bd/locations/khulna",
    images: [{ url: "https://kanokmiah.com.bd/kanok-miah-profile.webp", width: 400, height: 400, alt: "Md Kanok Miah — SEO Expert Dhaka" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "Local SEO Services in Khulna — Md Kanok Miah | SEO Expert in Dhaka, Bangladesh",
    description: "Professional local SEO services in Khulna, Bangladesh.",
    images: ["https://kanokmiah.com.bd/kanok-miah-profile.webp"],
  },
};

export default function KhulnaPage() {
  return <KhulnaClient />;
}
