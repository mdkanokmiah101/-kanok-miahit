import RajshahiClient from "./RajshahiClient";
import { BreadcrumbSchema } from "@/components/Schema";

export const metadata = {
  title: "Local SEO Rajshahi — Kanok Miah | SEO Expert in Rajshahi",
  description: "Professional local SEO services in Rajshahi, Bangladesh. Help mango exporters, educational institutions, and local businesses rank on Google Maps. Expert Rajshahi SEO solutions.",
  alternates: { canonical: "https://kanokmiah.com.bd/locations/rajshahi" },
  openGraph: {
    title: "Local SEO Rajshahi — Kanok Miah | SEO Expert in Rajshahi",
    description: "Professional local SEO services in Rajshahi, Bangladesh. Get found on Google Maps for your Rajshahi business — from mango export to coaching centers.",
    url: "https://kanokmiah.com.bd/locations/rajshahi",
    images: [{ url: "https://kanokmiah.com.bd/kanok-miah-profile.webp", width: 1200, height: 630, alt: "Kanok Miah — SEO Expert Rajshahi" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "Local SEO Rajshahi — Kanok Miah | SEO Expert in Rajshahi",
    description: "Professional local SEO services in Rajshahi, Bangladesh.",
    images: ["https://kanokmiah.com.bd/kanok-miah-profile.webp"],
  },
};

const locationSchema = {
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  name: "Kanok Miah — SEO Expert Rajshahi",
  url: "https://kanokmiah.com.bd/locations/rajshahi",
  telephone: "+880-1604-809110",
  email: "mdkanokmiah232@gmail.com",
  description: "Local SEO services in Rajshahi, Bangladesh. Expert SEO solutions for Rajshahi businesses including mango export and educational institutions.",
  image: "https://kanokmiah.com.bd/kanok-miah-profile.webp",
  address: { "@type": "PostalAddress", streetAddress: "Rajshahi", addressLocality: "Rajshahi", addressCountry: "BD" },
  geo: { "@type": "GeoCoordinates", latitude: "24.3733", longitude: "88.6049" },
  areaServed: ["Rajshahi", "Bangladesh"],
  priceRange: "$$",
};

export default function RajshahiPage() {
  return (
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(locationSchema) }} />
      {BreadcrumbSchema([
        { name: "Home", url: "https://kanokmiah.com.bd" },
        { name: "Locations", url: "https://kanokmiah.com.bd/locations/rajshahi" },
        { name: "Rajshahi", url: "https://kanokmiah.com.bd/locations/rajshahi" },
      ])}
      <RajshahiClient />
    </>
  );
}
