import LocationClient from "@/components/LocationClient";
import { BreadcrumbSchema } from "@/components/Schema";

export const metadata = {
  title: { absolute: "Best SEO Services in Khulna 2026 — Kanok Miah | SEO Expert, Khulna" },
  description: "Get the best SEO services in Khulna 2026 from Kanok Miah — 210+ projects. Rank on Google Maps across Sonadanga, Khalishpur, Gollamari & all Khulna with expert local SEO.",
  alternates: { canonical: "https://kanokmiah.com.bd/locations/khulna" },
  openGraph: {
    title: "Best SEO Services in Khulna 2026 — Kanok Miah",
    description: "Best SEO services in Khulna — rank on Google Maps with proven local SEO strategies.",
    url: "https://kanokmiah.com.bd/locations/khulna",
    images: [{ url: "https://kanokmiah.com.bd/kanok-miah-profile.webp", width: 1200, height: 630, alt: "Kanok Miah — SEO Expert Khulna" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "Best SEO Services in Khulna 2026 — Kanok Miah",
    description: "Best SEO services in Khulna — rank higher on Google Maps with proven local SEO strategies.",
    images: ["https://kanokmiah.com.bd/kanok-miah-profile.webp"],
  },
};

const locationSchema = {
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  name: "Kanok Miah — SEO Expert Khulna",
  url: "https://kanokmiah.com.bd/locations/khulna",
  telephone: "+880-1604-809110",
  email: "mdkanokmiah232@gmail.com",
  description: "Best SEO services in Khulna, Bangladesh. Expert local SEO solutions for Khulna businesses across all neighborhoods — Sonadanga, Khalishpur, Boyra & more.",
  image: "https://kanokmiah.com.bd/kanok-miah-profile.webp",
  address: { "@type": "PostalAddress", streetAddress: "Khulna", addressLocality: "Khulna", addressCountry: "BD" },
  geo: { "@type": "GeoCoordinates", latitude: "22.8456", longitude: "89.5403" },
  areaServed: ["Khulna", "Sonadanga", "Khalishpur", "Daulatpur"],
  priceRange: "$$",
  dateModified: "2026-07-20",
  sameAs: [
    "https://www.facebook.com/mdkanokmiahweb",
    "https://bd.linkedin.com/in/kanok-miah",
    "https://www.youtube.com/@kanokmiah"
  ],
  aggregateRating: {
    "@type": "AggregateRating",
    ratingValue: "4.9",
    bestRating: "5",
    ratingCount: "108"
  },
  openingHours: [
    { "@type": "OpeningHoursSpecification", dayOfWeek: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], opens: "09:00", closes: "18:00" },
    { "@type": "OpeningHoursSpecification", dayOfWeek: ["Saturday"], opens: "10:00", closes: "16:00" }
  ],
};

export default function KhulnaPage() {
  return (
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(locationSchema) }} />
      {BreadcrumbSchema([
        { name: "Home", url: "https://kanokmiah.com.bd" },
        { name: "Locations", url: "https://kanokmiah.com.bd/locations" },
        { name: "Khulna", url: "https://kanokmiah.com.bd/locations/khulna" },
      ])}
      <LocationClient city="khulna" />
    </>
  );
}
