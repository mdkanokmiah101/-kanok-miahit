import SylhetClient from "./SylhetClient";
import { BreadcrumbSchema } from "@/components/Schema";

export const metadata = {
  title: "Local SEO Sylhet — Md Kanok Miah | SEO Expert Dhaka",
  description: "Professional local SEO services in Sylhet, Bangladesh. Rank higher on Google Maps and attract more customers with expert local SEO.",
  alternates: { canonical: "https://kanokmiah.com.bd/locations/sylhet" },
  openGraph: {
    title: "Local SEO Sylhet — Md Kanok Miah | SEO Expert Dhaka",
    description: "Professional local SEO services in Sylhet, Bangladesh. Get found on Google Maps and attract more customers in Sylhet city.",
    url: "https://kanokmiah.com.bd/locations/sylhet",
    images: [{ url: "https://kanokmiah.com.bd/kanok-miah-profile.webp", width: 400, height: 400, alt: "Md Kanok Miah — SEO Expert Dhaka" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "Local SEO Sylhet — Md Kanok Miah | SEO Expert Dhaka",
    description: "Professional local SEO services in Sylhet, Bangladesh.",
    images: ["https://kanokmiah.com.bd/kanok-miah-profile.webp"],
  },
};

const locationSchema = {
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  name: "Md Kanok Miah — SEO Expert Sylhet",
  url: "https://kanokmiah.com.bd/locations/sylhet",
  telephone: "+880-1712-883101",
  email: "mdkanokmiah232@gmail.com",
  description: "Local SEO services in Sylhet, Bangladesh. Expert SEO solutions for Sylhet businesses.",
  image: "https://kanokmiah.com.bd/kanok-miah-profile.webp",
  address: { "@type": "PostalAddress", streetAddress: "Sylhet", addressLocality: "Sylhet", addressCountry: "BD" },
  geo: { "@type": "GeoCoordinates", latitude: "24.8949", longitude: "91.8687" },
  areaServed: ["Sylhet", "Bangladesh"],
  priceRange: "$$",
};

export default function SylhetPage() {
  return (
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(locationSchema) }} />
      {BreadcrumbSchema([
        { name: "Home", url: "https://kanokmiah.com.bd" },
        { name: "Locations", url: "https://kanokmiah.com.bd/locations/sylhet" },
        { name: "Sylhet", url: "https://kanokmiah.com.bd/locations/sylhet" },
      ])}
      <SylhetClient />
    </>
  );
}
