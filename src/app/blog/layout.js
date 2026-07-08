export const metadata = {
  title: "SEO Blog | Bangladesh Digital Marketing Tips",
  description:
    "Expert SEO tips, guides, and strategies for Bangladesh businesses. Learn local SEO, technical SEO, e-commerce SEO, GEO optimization, and more from Md Kanok Miah.",
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
  },
  twitter: {
    card: "summary_large_image",
    title: "SEO Blog | Bangladesh Digital Marketing Tips",
    description:
      "Expert SEO tips, guides, and strategies for Bangladesh businesses.",
  },
};

export default function BlogLayout({ children }) {
  return <>{children}</>;
}
