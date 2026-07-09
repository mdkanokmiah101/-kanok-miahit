import DhakaClient from "./DhakaClient";

export const metadata = {
  title: "Local SEO Services in Dhaka",
  description: "Professional local SEO services in Dhaka, Bangladesh. Rank your business on Google Maps in Mirpur, Gulshan, Banani, Uttara, Dhanmondi and all Dhaka areas with expert SEO.",
  alternates: { canonical: "/locations/dhaka" },
  openGraph: {
    title: "Local SEO Services in Dhaka — Md Kanok Miah",
    description: "Professional local SEO services in Dhaka, Bangladesh. Rank on Google Maps in Mirpur, Gulshan, Banani, Uttara, Dhanmondi and all Dhaka areas.",
    url: "https://kanokmiah.com.bd/locations/dhaka",
    images: [{ url: "/kanok-miah-profile.webp", width: 400, height: 400, alt: "Md Kanok Miah — SEO Expert Dhaka" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "Local SEO Services in Dhaka — Md Kanok Miah",
    description: "Professional local SEO services in Dhaka, Bangladesh.",
    images: ["/kanok-miah-profile.webp"],
  },
};

export default function DhakaPage() {
  return <DhakaClient />;
}
