import MymensinghClient from "./MymensinghClient";
import { BreadcrumbSchema } from "@/components/Schema";

export const metadata = {
  title: "Local SEO Services in Mymensingh — Md Kanok Miah | SEO Expert Dhaka, Bangladesh",
  description: "Professional local SEO services in Mymensingh, Bangladesh. Rank higher on Google Maps and attract more customers with expert local SEO.",
  alternates: { canonical: "/locations/mymensingh" },
  openGraph: {
    title: "Local SEO Services in Mymensingh — Md Kanok Miah | SEO Expert in Dhaka, Bangladesh",
    description: "Professional local SEO services in Mymensingh, Bangladesh. Get found on Google Maps and attract more customers in Mymensingh city.",
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

const locationSchema = {
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  name: "Md Kanok Miah — SEO Expert Mymensingh",
  url: "https://kanokmiah.com.bd/locations/mymensingh",
  telephone: "+880-1712-883101",
  email: "mdkanokmiah232@gmail.com",
  description: "Local SEO services in Mymensingh, Bangladesh. Expert SEO solutions for Mymensingh businesses.",
  image: "https://kanokmiah.com.bd/kanok-miah-profile.webp",
  address: { "@type": "PostalAddress", streetAddress: "Mymensingh", addressLocality: "Mymensingh", addressCountry: "BD" },
  geo: { "@type": "GeoCoordinates", latitude: "24.7471", longitude: "90.4203" },
  areaServed: ["Mymensingh", "Bangladesh"],
  priceRange: "$$",
};

export default function MymensinghPage() {
  return (
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={ __html: JSON.stringify(locationSchema) } />
      {BreadcrumbSchema([
        { name: "Home", url: "https://kanokmiah.com.bd" },
        { name: "Locations", url: "https://kanokmiah.com.bd/locations/mymensingh" },
        { name: "Mymensingh", url: "https://kanokmiah.com.bd/locations/mymensingh" },
      ])}
      <MymensinghClient />
    </>
  );
}
