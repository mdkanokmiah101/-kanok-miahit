import DhakaClient from "./DhakaClient";
import { BreadcrumbSchema } from "@/components/Schema";

export const metadata = {
  title: "Best SEO Services in Dhaka",
  description: "Get the best SEO services in Dhaka from Kanok Miah — 210+ projects delivered. Rank on Google Maps across Mirpur, Gulshan, Banani, Uttara & all Dhaka with expert local SEO.",
  alternates: { canonical: "https://kanokmiah.com.bd/locations/dhaka" },
  openGraph: {
    title: "Best SEO Services in Dhaka — Kanok Miah",
    description: "Best SEO services in Dhaka — rank on Google Maps across Mirpur, Gulshan, Banani, Uttara & all Dhaka neighborhoods with proven local SEO.",
    url: "https://kanokmiah.com.bd/locations/dhaka",
    images: [{ url: "https://kanokmiah.com.bd/kanok-miah-profile.webp", width: 1200, height: 630, alt: "Kanok Miah — SEO Expert Dhaka" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "Best SEO Services in Dhaka — Kanok Miah",
    description: "Best SEO services in Dhaka — rank higher on Google Maps with proven local SEO strategies.",
    images: ["https://kanokmiah.com.bd/kanok-miah-profile.webp"],
  },
};

const locationSchema = {
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  name: "Kanok Miah — SEO Expert Dhaka",
  url: "https://kanokmiah.com.bd/locations/dhaka",
  telephone: "+880-1604-809110",
  email: "mdkanokmiah232@gmail.com",
  description: "Best SEO services in Dhaka, Bangladesh. Expert SEO solutions for Dhaka businesses across all neighborhoods — Mirpur, Gulshan, Banani, Uttara & more.",
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
