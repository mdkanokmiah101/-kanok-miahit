import RajshahiClient from "./RajshahiClient";

export const metadata = {
  title: "Local SEO Services in Rajshahi",
  description: "Professional local SEO services in Rajshahi, Bangladesh. Get found on Google Maps and attract more customers with expert local SEO.",
  alternates: { canonical: "/locations/rajshahi" },
  openGraph: {
    title: "Local SEO Services in Rajshahi — Md Kanok Miah",
    description: "Professional local SEO services in Rajshahi, Bangladesh. Get found on Google Maps and attract more customers in Rajshahi city.",
    url: "https://kanokmiah.com.bd/locations/rajshahi",
    images: [{ url: "/kanok-miah-profile.webp", width: 400, height: 400, alt: "Md Kanok Miah — SEO Expert Dhaka" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "Local SEO Services in Rajshahi — Md Kanok Miah",
    description: "Professional local SEO services in Rajshahi, Bangladesh.",
    images: ["/kanok-miah-profile.webp"],
  },
};

export default function RajshahiPage() {
  return <RajshahiClient />;
}
