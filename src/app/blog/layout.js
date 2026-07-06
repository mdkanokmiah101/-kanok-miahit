export const metadata = {
  title: "SEO Blog — Kanok MiahIT | Bangladesh Digital Marketing Tips",
  description:
    "Expert SEO tips, guides, and strategies for Bangladesh businesses. Learn local SEO, technical SEO, e-commerce SEO, GEO optimization, and more from Kanok MiahIT.",
  alternates: {
    canonical: "/blog",
  },
  openGraph: {
    type: "website",
    locale: "en_US",
    siteName: "Kanok MiahIT",
    title: "SEO Blog — Kanok MiahIT | Bangladesh Digital Marketing Tips",
    description:
      "Expert SEO tips, guides, and strategies for Bangladesh businesses. Learn local SEO, technical SEO, e-commerce SEO, GEO optimization, and more.",
    url: "https://kanokmiah.com.bd/blog",
  },
  twitter: {
    card: "summary_large_image",
    title: "SEO Blog — Kanok MiahIT | Bangladesh Digital Marketing Tips",
    description:
      "Expert SEO tips, guides, and strategies for Bangladesh businesses.",
  },
};

export default function BlogLayout({ children }) {
  return <>{children}</>;
}
