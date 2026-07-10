import RajshahiClient from "./RajshahiClient";
import { BreadcrumbSchema } from "@/components/Schema";

export const metadata = {
  title: "Local SEO Rajshahi — Md Kanok Miah | SEO Expert Dhaka",
  description: "Professional local SEO services in Rajshahi, Bangladesh. Rank higher on Google Maps and attract more customers with expert local SEO.",
  alternates: { canonical: "/locations/rajshahi" },
  openGraph: {
    title: "Local SEO Rajshahi — Md Kanok Miah | SEO Expert Dhaka",
    description: "Professional local SEO services in Rajshahi, Bangladesh. Get found on Google Maps and attract more customers in Rajshahi city.",
    url: "https://kanokmiah.com.bd/locations/rajshahi",
    images: [{ url: "https://kanokmiah.com.bd/kanok-miah-profile.webp", width: 400, height: 400, alt: "Md Kanok Miah — SEO Expert Dhaka" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "Local SEO Rajshahi — Md Kanok Miah | SEO Expert Dhaka",
    description: "Professional local SEO services in Rajshahi, Bangladesh.",
    images: ["https://kanokmiah.com.bd/kanok-miah-profile.webp"],
  },
};

const locationSchema = {
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  name: "Md Kanok Miah — SEO Expert Rajshahi",
  url: "https://kanokmiah.com.bd/locations/rajshahi",
  telephone: "+880-1712-883101",
  email: "mdkanokmiah232@gmail.com",
  description: "Local SEO services in Rajshahi, Bangladesh. Expert SEO solutions for Rajshahi businesses.",
  image: "https://kanokmiah.com.bd/kanok-miah-profile.webp",
  address: { "@type": "PostalAddress", streetAddress: "Rajshahi", addressLocality: "Rajshahi", addressCountry: "BD" },
  geo: { "@type": "GeoCoordinates", latitude: "24.3745", longitude: "88.6042" },
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
