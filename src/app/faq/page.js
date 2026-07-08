import FaqClient from "./FaqClient";

export const metadata = {
  title: "Frequently Asked Questions",
  description: "Frequently asked questions about SEO services in Bangladesh. Learn about Local SEO, Technical SEO, Link Building, GEO/AI Search and more from Md Kanok Miah.",
  alternates: { canonical: "/faq" },
};

export default function FaqPage() {
  return <FaqClient />;
}
