import PortfolioClient from "./PortfolioClient";

export const metadata = {
  title: "Portfolio",
  description: "View the SEO portfolio of Md Kanok Miah \u2014 350+ projects completed, 50+ happy clients in Dhaka, Chittagong, Sylhet and across Bangladesh.",
  alternates: { canonical: "/portfolio" },
};

export default function PortfolioPage() {
  return <PortfolioClient />;
}
