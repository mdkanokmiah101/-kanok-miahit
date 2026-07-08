import ContactClient from "./ContactClient";

export const metadata = {
  title: "Contact Me — Md Kanok Miah | SEO Expert in Dhaka, Bangladesh",
  description: "Contact Md Kanok Miah — the best SEO expert in Dhaka, Bangladesh. Get a free SEO audit for your business. Call +880 1712-883101 for a consultation.",
  alternates: { canonical: "/contact" },
  openGraph: {
    title: "Contact Me — Md Kanok Miah | SEO Expert in Dhaka, Bangladesh",
    description: "Contact Md Kanok Miah for a free SEO audit. Get expert help for your Bangladesh business.",
    url: "https://kanokmiah.com.bd/contact",
  },
};

export default function ContactPage() {
  return <ContactClient />;
}
