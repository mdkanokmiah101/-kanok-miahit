import SylhetClient from "./SylhetClient";

export const metadata = {
  title: "Local SEO Services in Sylhet",
  description: "Professional local SEO services in Sylhet, Bangladesh. Rank higher on Google Maps and attract more customers with expert local SEO strategies.",
  alternates: { canonical: "/locations/sylhet" },
  openGraph: {
    title: "Local SEO Services in Sylhet — Md Kanok Miah | SEO Expert in Dhaka, Bangladesh",
    description: "Professional local SEO services in Sylhet, Bangladesh. Get found on Google Maps and attract more customers in Sylhet city.",
    url: "https://kanokmiah.com.bd/locations/sylhet",
    images: [{ url: "/kanok-miah-profile.webp", width: 400, height: 400, alt: "Md Kanok Miah — SEO Expert Dhaka" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "Local SEO Services in Sylhet — Md Kanok Miah | SEO Expert in Dhaka, Bangladesh",
    description: "Professional local SEO services in Sylhet, Bangladesh.",
    images: ["/kanok-miah-profile.webp"],
  },
};

export default function SylhetPage() {
  return <SylhetClient />;
}
