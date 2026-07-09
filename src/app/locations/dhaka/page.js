import DhakaClient from "./DhakaClient";

export const metadata = {
  title: "Local SEO Dhaka",
  description: "Local SEO services in Dhaka, Bangladesh. Rank your business on Google Maps in Mirpur, Gulshan, Banani, Uttara & all Dhaka areas with expert SEO.",
  alternates: { canonical: "/locations/dhaka" },
  openGraph: {
    title: "Local SEO Dhaka \u2014 Md Kanok Miah",
    description: "Local SEO services in Dhaka, Bangladesh. Rank on Google Maps in Mirpur, Gulshan, Banani, Uttara & all Dhaka areas.",
    url: "https://kanokmiah.com.bd/locations/dhaka",
    images: [{ url: "/kanok-miah-profile.webp", width: 400, height: 400, alt: "Md Kanok Miah \u2014 SEO Expert Dhaka" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "Local SEO Dhaka \u2014 Md Kanok Miah",
    description: "Local SEO services in Dhaka, Bangladesh.",
    images: ["/kanok-miah-profile.webp"],
  },
};

export default function DhakaPage() {
  return <DhakaClient />;
}
