import RangpurClient from "./RangpurClient";
import { BreadcrumbSchema } from "@/components/Schema";

export const metadata = {
  title: "Local SEO Rangpur — Md Kanok Miah | SEO Expert in Rangpur",
  description: "Professional local SEO services in Rangpur, Bangladesh. Help tobacco, potato, and agricultural businesses rank on Google Maps. Expert Rangpur SEO solutions.",
  alternates: { canonical: "https://kanokmiah.com.bd/locations/rangpur" },
  openGraph: {
    title: "Local SEO Rangpur — Md Kanok Miah | SEO Expert in Rangpur",
    description: "Professional local SEO services in Rangpur, Bangladesh. Get found on Google Maps for your Rangpur business — from agriculture to manufacturing.",
    url: "https://kanokmiah.com.bd/locations/rangpur",
    images: [{ url: "https://kanokmiah.com.bd/kanok-miah-profile.webp", width: 1200, height: 630, alt: "Md Kanok Miah — SEO Expert Rangpur" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "Local SEO Rangpur — Md Kanok Miah | SEO Expert in Rangpur",
    description: "Professional local SEO services in Rangpur, Bangladesh.",
    images: ["https://kanokmiah.com.bd/kanok-miah-profile.webp"],
  },
};

const locationSchema = {
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  name: "Md Kanok Miah — SEO Expert Rangpur",
  url: "https://kanokmiah.com.bd/locations/rangpur",
  telephone: "+880-1604-809110",
  email: "mdkanokmiah232@gmail.com",
  description: "Local SEO services in Rangpur, Bangladesh. Expert SEO solutions for Rangpur businesses including tobacco, potato, and agricultural industries.",
  image: "https://kanokmiah.com.bd/kanok-miah-profile.webp",
  address: { "@type": "PostalAddress", streetAddress: "Rangpur", addressLocality: "Rangpur", addressCountry: "BD" },
  geo: { "@type": "GeoCoordinates", latitude: "25.7468", longitude: "89.2508" },
  areaServed: ["Rangpur", "Bangladesh"],
  priceRange: "$$",
};

export default function RangpurPage() {
  return (
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(locationSchema) }} />
      {BreadcrumbSchema([
        { name: "Home", url: "https://kanokmiah.com.bd" },
        { name: "Locations", url: "https://kanokmiah.com.bd/locations/rangpur" },
        { name: "Rangpur", url: "https://kanokmiah.com.bd/locations/rangpur" },
      ])}
      <RangpurClient />
    </>
  );
}
