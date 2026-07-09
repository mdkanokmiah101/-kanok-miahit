import CaseStudiesClient from "./CaseStudiesClient";

export const metadata = {
  title: "Case Studies",
  description: "Real SEO case studies from Bangladesh businesses. See how Md Kanok Miah helped Dhaka restaurants, e-commerce stores, and local businesses rank higher on Google.",
  alternates: { canonical: "/case-studies" },
};

export default function CaseStudiesPage() {
  return <CaseStudiesClient />;
}
