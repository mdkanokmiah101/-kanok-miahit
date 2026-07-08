import AboutClient from "./AboutClient";

export const metadata = {
  title: "About Me",
  description: "Learn about Md Kanok Miah — Bangladesh's trusted SEO expert with 6+ years of experience. Helping businesses in Dhaka, Chittagong, and Sylhet rank higher on Google with proven SEO strategies.",
  alternates: { canonical: "/about" },
  openGraph: {
    title: "About Me",
    description: "Learn about Md Kanok Miah — Bangladesh's trusted SEO expert with 6+ years of experience.",
    url: "https://kanokmiah.com.bd/about",
  },
};

export default function AboutPage() {
  return <AboutClient />;
}
