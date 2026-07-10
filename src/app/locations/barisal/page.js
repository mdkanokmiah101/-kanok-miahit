import BarisalClient from "./BarisalClient";

export const metadata = {
  title: "Local SEO Services in Barisal — Md Kanok Miah | SEO Expert Dhaka, Bangladesh",
  description: "Professional local SEO services in Barisal, Bangladesh. Rank higher on Google Maps and attract more customers with proven local SEO.",
  alternates: { canonical: "/locations/barisal" },
  openGraph: {
    title: "Local SEO Services in Barisal — Md Kanok Miah | SEO Expert in Dhaka, Bangladesh",
    description: "Professional local SEO services in Barisal, Bangladesh. Rank higher on Google Maps and attract more customers in Barisal city.",
    url: "https://kanokmiah.com.bd/locations/barisal",
    images: [{ url: "https://kanokmiah.com.bd/kanok-miah-profile.webp", width: 400, height: 400, alt: "Md Kanok Miah — SEO Expert Dhaka" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "Local SEO Services in Barisal — Md Kanok Miah | SEO Expert in Dhaka, Bangladesh",
    description: "Professional local SEO services in Barisal, Bangladesh.",
    images: ["https://kanokmiah.com.bd/kanok-miah-profile.webp"],
  },
};

export default function BarisalPage() {
  return <BarisalClient />;
}
