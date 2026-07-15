import BarisalClient from "./BarisalClient";
import { BreadcrumbSchema } from "@/components/Schema";

export const metadata = {
  title: "Local SEO Barisal — Md Kanok Miah | SEO Expert in Barisal",
  description: "Professional local SEO services in Barisal, Bangladesh. Help agriculture, fisheries, and river-trade businesses rank on Google Maps. Expert Barisal SEO solutions.",
  alternates: { canonical: "https://kanokmiah.com.bd/locations/barisal" },
  openGraph: {
    title: "Local SEO Barisal — Md Kanok Miah | SEO Expert in Barisal",
    description: "Professional local SEO services in Barisal, Bangladesh. Get found on Google Maps for your Barisal business — from fisheries to tourism.",
    url: "https://kanokmiah.com.bd/locations/barisal",
    images: [{ url: "https://kanokmiah.com.bd/kanok-miah-profile.webp", width: 1200, height: 630, alt: "Md Kanok Miah — SEO Expert Barisal" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "Local SEO Barisal — Md Kanok Miah | SEO Expert in Barisal",
    description: "Professional local SEO services in Barisal, Bangladesh.",
    images: ["https://kanokmiah.com.bd/kanok-miah-profile.webp"],
  },
};

const locationSchema = {
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  name: "Md Kanok Miah — SEO Expert Barisal",
  url: "https://kanokmiah.com.bd/locations/barisal",
  telephone: "+880-1604-809110",
  email: "mdkanokmiah232@gmail.com",
  description: "Local SEO services in Barisal, Bangladesh. Expert SEO solutions for Barisal businesses including agriculture, fisheries, and river trade.",
  image: "https://kanokmiah.com.bd/kanok-miah-profile.webp",
  address: { "@type": "PostalAddress", streetAddress: "Barisal", addressLocality: "Barisal", addressCountry: "BD" },
  geo: { "@type": "GeoCoordinates", latitude: "22.7010", longitude: "90.3535" },
  areaServed: ["Barisal", "Bangladesh"],
  priceRange: "$$",
};

export default function BarisalPage() {
  return (
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(locationSchema) }} />
      {BreadcrumbSchema([
        { name: "Home", url: "https://kanokmiah.com.bd" },
        { name: "Locations", url: "https://kanokmiah.com.bd/locations/barisal" },
        { name: "Barisal", url: "https://kanokmiah.com.bd/locations/barisal" },
      ])}
      <BarisalClient />
    </>
  );
}
