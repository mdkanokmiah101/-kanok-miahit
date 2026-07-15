import ChittagongClient from "./ChittagongClient";
import { BreadcrumbSchema } from "@/components/Schema";

export const metadata = {
  title: "Local SEO Chittagong — Kanok Miah | SEO Expert in Chittagong",
  description: "Professional local SEO services in Chittagong, Bangladesh's port city. Rank higher on Google Maps, attract more customers from Agrabad, Halishahar, EPZ & all Chittagong areas with expert local SEO.",
  alternates: { canonical: "https://kanokmiah.com.bd/locations/chittagong" },
  openGraph: {
    title: "Local SEO Chittagong — Kanok Miah | SEO Expert in Chittagong",
    description: "Professional local SEO services in Chittagong, Bangladesh. Get found on Google Maps and attract more customers in Chittagong port city with proven SEO strategies.",
    url: "https://kanokmiah.com.bd/locations/chittagong",
    images: [{ url: "https://kanokmiah.com.bd/kanok-miah-profile.webp", width: 1200, height: 630, alt: "Kanok Miah — SEO Expert Chittagong" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "Local SEO Chittagong — Kanok Miah | SEO Expert in Chittagong",
    description: "Professional local SEO services in Chittagong, Bangladesh.",
    images: ["https://kanokmiah.com.bd/kanok-miah-profile.webp"],
  },
};

const locationSchema = {
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  name: "Kanok Miah — SEO Expert Chittagong",
  url: "https://kanokmiah.com.bd/locations/chittagong",
  telephone: "+880-1604-809110",
  email: "mdkanokmiah232@gmail.com",
  description: "Local SEO services in Chittagong, Bangladesh. Expert SEO solutions for Chittagong businesses including port, shipping, and import/export companies.",
  image: "https://kanokmiah.com.bd/kanok-miah-profile.webp",
  address: { "@type": "PostalAddress", streetAddress: "Chittagong", addressLocality: "Chittagong", addressCountry: "BD" },
  geo: { "@type": "GeoCoordinates", latitude: "22.3569", longitude: "91.7832" },
  areaServed: ["Chittagong", "Bangladesh"],
  priceRange: "$$",
};

export default function ChittagongPage() {
  return (
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(locationSchema) }} />
      {BreadcrumbSchema([
        { name: "Home", url: "https://kanokmiah.com.bd" },
        { name: "Locations", url: "https://kanokmiah.com.bd/locations/chittagong" },
        { name: "Chittagong", url: "https://kanokmiah.com.bd/locations/chittagong" },
      ])}
      <ChittagongClient />
    </>
  );
}
