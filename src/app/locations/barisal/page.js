import BarisalClient from "./BarisalClient";
import { BreadcrumbSchema } from "@/components/Schema";

export const metadata = {
  title: "Local SEO Barisal — Md Kanok Miah | SEO Expert Dhaka",
  description: "Professional local SEO services in Barisal, Bangladesh. Rank higher on Google Maps and attract more customers with expert local SEO.",
  alternates: { canonical: "/locations/barisal" },
  openGraph: {
    title: "Local SEO Barisal — Md Kanok Miah | SEO Expert Dhaka",
    description: "Professional local SEO services in Barisal, Bangladesh. Get found on Google Maps and attract more customers in Barisal city.",
    url: "https://kanokmiah.com.bd/locations/barisal",
    images: [{ url: "https://kanokmiah.com.bd/kanok-miah-profile.webp", width: 400, height: 400, alt: "Md Kanok Miah — SEO Expert Dhaka" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "Local SEO Barisal — Md Kanok Miah | SEO Expert Dhaka",
    description: "Professional local SEO services in Barisal, Bangladesh.",
    images: ["https://kanokmiah.com.bd/kanok-miah-profile.webp"],
  },
};

const locationSchema = {
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  name: "Md Kanok Miah — SEO Expert Barisal",
  url: "https://kanokmiah.com.bd/locations/barisal",
  telephone: "+880-1712-883101",
  email: "mdkanokmiah232@gmail.com",
  description: "Local SEO services in Barisal, Bangladesh. Expert SEO solutions for Barisal businesses.",
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
