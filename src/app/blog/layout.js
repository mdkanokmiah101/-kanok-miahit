import { BreadcrumbSchema, CollectionPageSchema } from "@/components/Schema";

export const metadata = {
  title: "SEO Blog | Bangladesh Digital Marketing Tips",
  description:
    "Expert SEO tips, guides, and strategies for Bangladesh businesses. Learn local SEO, technical SEO, e-commerce SEO, GEO optimization, & more from Md Kanok Miah.",
  alternates: {
    canonical: "/blog",
  },
  openGraph: {
    type: "website",
    locale: "en_US",
    siteName: "Md Kanok Miah",
    title: "SEO Blog | Bangladesh Digital Marketing Tips",
    description:
      "Expert SEO tips, guides, and strategies for Bangladesh businesses. Learn local SEO, technical SEO, e-commerce SEO, GEO optimization, and more.",
    url: "https://kanokmiah.com.bd/blog",
    images: [{ url: "/kanok-miah-profile.webp", width: 400, height: 400, alt: "Md Kanok Miah — SEO Expert Dhaka" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "SEO Blog | Bangladesh Digital Marketing Tips",
    description:
      "Expert SEO tips, guides, and strategies for Bangladesh businesses.",
    images: ["/kanok-miah-profile.webp"],
  },
};

export default function BlogLayout({ children }) {
  return (
    <>
      {children}
    </>
  );
}
