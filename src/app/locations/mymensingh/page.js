import LocationClient from "@/components/LocationClient";
import { BreadcrumbSchema } from "@/components/Schema";

export const metadata = {
  title: { absolute: "Best SEO Services in Mymensingh 2026 — Kanok Miah | SEO Expert, Mymensingh" },
  description: "Get the best SEO services in Mymensingh 2026 from Kanok Miah — 210+ projects. Rank on Google Maps across Mymensingh City, Kachijhuli, Bhaluka & all Mymensingh with expert local SEO.",
  alternates: { canonical: "https://kanokmiah.com.bd/locations/mymensingh" },
  openGraph: {
    title: "Best SEO Services in Mymensingh 2026 — Kanok Miah",
    description: "Best SEO services in Mymensingh — rank on Google Maps with proven local SEO strategies.",
    url: "https://kanokmiah.com.bd/locations/mymensingh",
    images: [{ url: "https://kanokmiah.com.bd/kanok-miah-profile.webp", width: 1200, height: 630, alt: "Kanok Miah — SEO Expert Mymensingh" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "Best SEO Services in Mymensingh 2026 — Kanok Miah",
    description: "Best SEO services in Mymensingh — rank higher on Google Maps with proven local SEO strategies.",
    images: ["https://kanokmiah.com.bd/kanok-miah-profile.webp"],
  },
};

const locationSchema = {
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  name: "Kanok Miah — SEO Expert Mymensingh",
  url: "https://kanokmiah.com.bd/locations/mymensingh",
  telephone: "+880-1604-809110",
  email: "mdkanokmiah232@gmail.com",
  description: "Best SEO services in Mymensingh, Bangladesh. Expert local SEO solutions for Mymensingh businesses across all neighborhoods — Kachijhuli, Birsressha, Bhaluka & more.",
  image: "https://kanokmiah.com.bd/kanok-miah-profile.webp",
  address: { "@type": "PostalAddress", streetAddress: "Mymensingh", addressLocality: "Mymensingh", addressCountry: "BD" },
  geo: { "@type": "GeoCoordinates", latitude: "24.7471", longitude: "90.4203" },
  areaServed: ["Mymensingh", "Kachijhuli", "Birsressha", "Bhaluka"],
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

export default function MymensinghPage() {
  return (
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(locationSchema) }} />
      {BreadcrumbSchema([
        { name: "Home", url: "https://kanokmiah.com.bd" },
        { name: "Locations", url: "https://kanokmiah.com.bd/locations" },
        { name: "Mymensingh", url: "https://kanokmiah.com.bd/locations/mymensingh" },
      ])}
      <LocationClient city="mymensingh" />
    </>
  );
}
