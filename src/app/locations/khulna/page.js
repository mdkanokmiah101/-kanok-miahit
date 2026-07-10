import KhulnaClient from "./KhulnaClient";
import { BreadcrumbSchema } from "@/components/Schema";

export const metadata = {
  title: "Local SEO Khulna — Md Kanok Miah | SEO Expert Dhaka",
  description: "Professional local SEO services in Khulna, Bangladesh. Rank higher on Google Maps and attract more customers with expert local SEO.",
  alternates: { canonical: "https://kanokmiah.com.bd/locations/khulna" },
  openGraph: {
    title: "Local SEO Khulna — Md Kanok Miah | SEO Expert Dhaka",
    description: "Professional local SEO services in Khulna, Bangladesh. Get found on Google Maps and attract more customers in Khulna city.",
    url: "https://kanokmiah.com.bd/locations/khulna",
    images: [{ url: "https://kanokmiah.com.bd/kanok-miah-profile.webp", width: 400, height: 400, alt: "Md Kanok Miah — SEO Expert Dhaka" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "Local SEO Khulna — Md Kanok Miah | SEO Expert Dhaka",
    description: "Professional local SEO services in Khulna, Bangladesh.",
    images: ["https://kanokmiah.com.bd/kanok-miah-profile.webp"],
  },
};

const locationSchema = {
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  name: "Md Kanok Miah — SEO Expert Khulna",
  url: "https://kanokmiah.com.bd/locations/khulna",
  telephone: "+880-1712-883101",
  email: "mdkanokmiah232@gmail.com",
  description: "Local SEO services in Khulna, Bangladesh. Expert SEO solutions for Khulna businesses.",
  image: "https://kanokmiah.com.bd/kanok-miah-profile.webp",
  address: { "@type": "PostalAddress", streetAddress: "Khulna", addressLocality: "Khulna", addressCountry: "BD" },
  geo: { "@type": "GeoCoordinates", latitude: "22.8456", longitude: "89.5403" },
  areaServed: ["Khulna", "Bangladesh"],
  priceRange: "$$",
};

export default function KhulnaPage() {
  return (
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(locationSchema) }} />
      {BreadcrumbSchema([
        { name: "Home", url: "https://kanokmiah.com.bd" },
        { name: "Locations", url: "https://kanokmiah.com.bd/locations/khulna" },
        { name: "Khulna", url: "https://kanokmiah.com.bd/locations/khulna" },
      ])}
      <KhulnaClient />
    </>
  );
}
