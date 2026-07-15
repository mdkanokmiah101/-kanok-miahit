import KhulnaClient from "./KhulnaClient";
import { BreadcrumbSchema } from "@/components/Schema";

export const metadata = {
  title: "Local SEO Khulna — Md Kanok Miah | SEO Expert in Khulna",
  description: "Professional local SEO services in Khulna, Bangladesh. Help shrimp exporters, industrial businesses, and local service providers rank on Google Maps. Expert Khulna SEO solutions.",
  alternates: { canonical: "https://kanokmiah.com.bd/locations/khulna" },
  openGraph: {
    title: "Local SEO Khulna — Md Kanok Miah | SEO Expert in Khulna",
    description: "Professional local SEO services in Khulna, Bangladesh. Get found on Google Maps for your Khulna business — from shrimp export to manufacturing.",
    url: "https://kanokmiah.com.bd/locations/khulna",
    images: [{ url: "https://kanokmiah.com.bd/kanok-miah-profile.webp", width: 1200, height: 630, alt: "Md Kanok Miah — SEO Expert Khulna" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "Local SEO Khulna — Md Kanok Miah | SEO Expert in Khulna",
    description: "Professional local SEO services in Khulna, Bangladesh.",
    images: ["https://kanokmiah.com.bd/kanok-miah-profile.webp"],
  },
};

const locationSchema = {
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  name: "Md Kanok Miah — SEO Expert Khulna",
  url: "https://kanokmiah.com.bd/locations/khulna",
  telephone: "+880-1604-809110",
  email: "mdkanokmiah232@gmail.com",
  description: "Local SEO services in Khulna, Bangladesh. Expert SEO solutions for Khulna businesses including shrimp export and industrial manufacturing.",
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
