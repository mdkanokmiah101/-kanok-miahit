import MymensinghClient from "./MymensinghClient";

export const metadata = {
  title: "Local SEO Services in Mymensingh",
  description: "Professional local SEO services in Mymensingh, Bangladesh. Rank your business on Google Maps and attract more customers with proven local SEO.",
  alternates: { canonical: "/locations/mymensingh" },
  openGraph: {
    title: "Local SEO Services in Mymensingh — Md Kanok Miah | SEO Expert in Dhaka, Bangladesh",
    description: "Professional local SEO services in Mymensingh, Bangladesh. Rank on Google Maps and attract more customers in Mymensingh city.",
    url: "https://kanokmiah.com.bd/locations/mymensingh",
    images: [{ url: "https://kanokmiah.com.bd/kanok-miah-profile.webp", width: 400, height: 400, alt: "Md Kanok Miah — SEO Expert Dhaka" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "Local SEO Services in Mymensingh — Md Kanok Miah | SEO Expert in Dhaka, Bangladesh",
    description: "Professional local SEO services in Mymensingh, Bangladesh.",
    images: ["https://kanokmiah.com.bd/kanok-miah-profile.webp"],
  },
};

export default function MymensinghPage() {
  return <MymensinghClient />;
}
