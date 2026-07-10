import DhakaClient from "./DhakaClient";

export const metadata = {
  title: "Local SEO Services in Dhaka — Md Kanok Miah | SEO Expert",
  description: "Local SEO services in Dhaka, Bangladesh. Rank your business on Google Maps in Mirpur, Gulshan, Banani, Uttara & all Dhaka areas with expert SEO.",
  alternates: { canonical: "/locations/dhaka" },
  openGraph: {
    title: "Local SEO Dhaka — Md Kanok Miah | SEO Expert in Dhaka, Bangladesh",
    description: "Local SEO services in Dhaka, Bangladesh. Rank on Google Maps in Mirpur, Gulshan, Banani, Uttara & all Dhaka areas.",
    url: "https://kanokmiah.com.bd/locations/dhaka",
    images: [{ url: "https://kanokmiah.com.bd/kanok-miah-profile.webp", width: 400, height: 400, alt: "Md Kanok Miah — SEO Expert Dhaka" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "Local SEO Dhaka — Md Kanok Miah | SEO Expert in Dhaka, Bangladesh",
    description: "Local SEO services in Dhaka, Bangladesh.",
    images: ["https://kanokmiah.com.bd/kanok-miah-profile.webp"],
  },
};

export default function DhakaPage() {
  return <DhakaClient />;
}
