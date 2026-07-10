import DhakaClient from "./DhakaClient";
import { BreadcrumbSchema } from "@/components/Schema";

export const metadata = {
  title: "Local SEO Services in Dhaka — Md Kanok Miah | SEO Expert",
  description: "Local SEO services in Dhaka, Bangladesh. Rank your business on Google Maps in Mirpur, Gulshan, Banani, Uttara & all Dhaka areas with expert SEO.",
  alternates: { canonical: "/locations/dhaka" },
  openGraph: {
    title: "Local SEO Dhaka — Md Kanok Miah | SEO Expert in Dhaka, Bangladesh",
    description: "Local SEO services in Dhaka, Bangladesh. Rank on Google Maps in Mirpur, Gulshan, Banani, Uttara & all Dhaka areas.",
    url: "https://kanokmiah.com.bd/locations/dhaka",
    images: [{ url: "https://kanokmiah.com.bd/kanok-miah-profile.webp", width: 400, height: 400, alt: "Md Kanok Miah — SEO Expert Dhaka" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "Local SEO Dhaka — Md Kanok Miah | SEO Expert in Dhaka, Bangladesh",
    description: "Local SEO services in Dhaka, Bangladesh.",
    images: ["https://kanokmiah.com.bd/kanok-miah-profile.webp"],
  },
};

const locationSchema = {
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  name: "Md Kanok Miah — SEO Expert Dhaka",
  url: "https://kanokmiah.com.bd/locations/dhaka",
  telephone: "+880-1712-883101",
  email: "mdkanokmiah232@gmail.com",
  description: "Local SEO services in Dhaka, Bangladesh. Expert SEO solutions for Dhaka businesses.",
  image: "https://kanokmiah.com.bd/kanok-miah-profile.webp",
  address: { "@type": "PostalAddress", streetAddress: "Mirpur, Dhaka", addressLocality: "Dhaka", addressCountry: "BD" },
  geo: { "@type": "GeoCoordinates", latitude: "23.8103", longitude: "90.4125" },
  areaServed: ["Dhaka", "Mirpur", "Gulshan", "Banani", "Uttara", "Dhanmondi"],
  priceRange: "$$",
};

export default function DhakaPage() {
  return (
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(locationSchema) }} />
      {BreadcrumbSchema([
        { name: "Home", url: "https://kanokmiah.com.bd" },
        { name: "Locations", url: "https://kanokmiah.com.bd/locations/dhaka" },
        { name: "Dhaka", url: "https://kanokmiah.com.bd/locations/dhaka" },
      ])}
      <DhakaClient />
    </>
  );
}
