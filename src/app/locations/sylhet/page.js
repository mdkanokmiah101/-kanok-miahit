import SylhetClient from "./SylhetClient";
import { BreadcrumbSchema } from "@/components/Schema";

export const metadata = {
  title: "Local SEO Sylhet — Kanok Miah | SEO Expert in Sylhet",
  description: "Professional local SEO services in Sylhet, Bangladesh. Help restaurants, hotels, and diaspora-connected businesses rank on Google Maps. Expert Sylhet SEO from a trusted SEO consultant.",
  alternates: { canonical: "https://kanokmiah.com.bd/locations/sylhet" },
  openGraph: {
    title: "Local SEO Sylhet — Kanok Miah | SEO Expert in Sylhet",
    description: "Professional local SEO services in Sylhet, Bangladesh. Get found on Google Maps for your Sylhet restaurant, hotel, or overseas business.",
    url: "https://kanokmiah.com.bd/locations/sylhet",
    images: [{ url: "https://kanokmiah.com.bd/kanok-miah-profile.webp", width: 1200, height: 630, alt: "Kanok Miah — SEO Expert Sylhet" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "Local SEO Sylhet — Kanok Miah | SEO Expert in Sylhet",
    description: "Professional local SEO services in Sylhet, Bangladesh.",
    images: ["https://kanokmiah.com.bd/kanok-miah-profile.webp"],
  },
};

const locationSchema = {
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  name: "Kanok Miah — SEO Expert Sylhet",
  url: "https://kanokmiah.com.bd/locations/sylhet",
  telephone: "+880-1604-809110",
  email: "mdkanokmiah232@gmail.com",
  description: "Local SEO services in Sylhet, Bangladesh. Expert SEO solutions for Sylhet businesses including restaurants, hotels, and overseas enterprises.",
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
