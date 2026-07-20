import LocationClient from "@/components/LocationClient";
import { BreadcrumbSchema } from "@/components/Schema";

export const metadata = {
  title: { absolute: "Best SEO Services in Rajshahi 2026 — Kanok Miah | SEO Expert, Rajshahi" },
  description: "Get the best SEO services in Rajshahi 2026 from Kanok Miah — 210+ projects. Rank on Google Maps across Boalia, Motihar, Kashiadanga & all Rajshahi with expert local SEO.",
  alternates: { canonical: "https://kanokmiah.com.bd/locations/rajshahi" },
  openGraph: {
    title: "Best SEO Services in Rajshahi 2026 — Kanok Miah",
    description: "Best SEO services in Rajshahi — rank on Google Maps with proven local SEO strategies.",
    url: "https://kanokmiah.com.bd/locations/rajshahi",
    images: [{ url: "https://kanokmiah.com.bd/kanok-miah-profile.webp", width: 1200, height: 630, alt: "Kanok Miah — SEO Expert Rajshahi" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "Best SEO Services in Rajshahi 2026 — Kanok Miah",
    description: "Best SEO services in Rajshahi — rank higher on Google Maps with proven local SEO strategies.",
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
  description: "Best SEO services in Rajshahi, Bangladesh. Expert local SEO solutions for Rajshahi businesses across all neighborhoods — Boalia, Motihar, Shah Makhdum & more.",
  image: "https://kanokmiah.com.bd/kanok-miah-profile.webp",
  address: { "@type": "PostalAddress", streetAddress: "Rajshahi", addressLocality: "Rajshahi", addressCountry: "BD" },
  geo: { "@type": "GeoCoordinates", latitude: "24.3745", longitude: "88.6042" },
  areaServed: ["Rajshahi", "Boalia", "Motihar", "Shah Makhdum"],
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

export default function RajshahiPage() {
  return (
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(locationSchema) }} />
      {BreadcrumbSchema([
        { name: "Home", url: "https://kanokmiah.com.bd" },
        { name: "Locations", url: "https://kanokmiah.com.bd/locations" },
        { name: "Rajshahi", url: "https://kanokmiah.com.bd/locations/rajshahi" },
      ])}
      <LocationClient city="rajshahi" />
    </>
  );
}
