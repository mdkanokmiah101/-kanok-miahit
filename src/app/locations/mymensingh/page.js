import MymensinghClient from "./MymensinghClient";
import { BreadcrumbSchema } from "@/components/Schema";

export const metadata = {
  title: "Local SEO Mymensingh — Kanok Miah | SEO Expert in Mymensingh",
  description: "Professional local SEO services in Mymensingh, Bangladesh. Help agriculture, dairy, and educational institutions rank on Google Maps. Expert Mymensingh SEO solutions.",
  alternates: { canonical: "https://kanokmiah.com.bd/locations/mymensingh" },
  openGraph: {
    title: "Local SEO Mymensingh — Kanok Miah | SEO Expert in Mymensingh",
    description: "Professional local SEO services in Mymensingh, Bangladesh. Get found on Google Maps for your Mymensingh business — from dairy farming to education.",
    url: "https://kanokmiah.com.bd/locations/mymensingh",
    images: [{ url: "https://kanokmiah.com.bd/kanok-miah-profile.webp", width: 1200, height: 630, alt: "Kanok Miah — SEO Expert Mymensingh" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "Local SEO Mymensingh — Kanok Miah | SEO Expert in Mymensingh",
    description: "Professional local SEO services in Mymensingh, Bangladesh.",
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
  description: "Local SEO services in Mymensingh, Bangladesh. Expert SEO solutions for Mymensingh businesses including agriculture, dairy, and education.",
  image: "https://kanokmiah.com.bd/kanok-miah-profile.webp",
  address: { "@type": "PostalAddress", streetAddress: "Mymensingh", addressLocality: "Mymensingh", addressCountry: "BD" },
  geo: { "@type": "GeoCoordinates", latitude: "24.7471", longitude: "90.4203" },
  areaServed: ["Mymensingh", "Bangladesh"],
  priceRange: "$$",
};

export default function MymensinghPage() {
  return (
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(locationSchema) }} />
      {BreadcrumbSchema([
        { name: "Home", url: "https://kanokmiah.com.bd" },
        { name: "Locations", url: "https://kanokmiah.com.bd/locations/mymensingh" },
        { name: "Mymensingh", url: "https://kanokmiah.com.bd/locations/mymensingh" },
      ])}
      <MymensinghClient />
    </>
  );
}
