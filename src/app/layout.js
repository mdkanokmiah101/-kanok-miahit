import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { OrganizationSchema, LocalBusinessSchema, WebSiteSchema, PersonSchema } from "@/components/Schema";
import Link from "next/link";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata = {
  metadataBase: new URL("https://kanokmiah.com.bd"),
  title: {
    default: "Best SEO Expert in Dhaka, Bangladesh | Md Kanok Miah — #1 SEO Specialist",
    template: "%s — Md Kanok Miah | SEO Expert in Dhaka, Bangladesh",
  },
  description:
    "Looking for the best SEO expert in Dhaka, Bangladesh? Md Kanok Miah is a top-rated SEO specialist with 6+ years of experience. Get higher rankings, more traffic, and qualified leads with proven SEO strategies. Local SEO, Technical SEO, Link Building, GEO — Dhaka, Bangladesh.",
  keywords: [
    "best SEO expert in Dhaka",
    "SEO expert Dhaka",
    "SEO specialist Bangladesh",
    "local SEO Bangladesh",
    "Bangladesh SEO expert",
    "SEO consultant Dhaka",
    "on-page SEO",
    "technical SEO",
    "link building Bangladesh",
    "semantic SEO",
    "GEO optimization",
    "Md Kanok Miah",
  ],
  authors: [{ name: "Md Kanok Miah" }],
  creator: "Md Kanok Miah",
  publisher: "Md Kanok Miah",
  alternates: {
    canonical: "/",
  },
  openGraph: {
    type: "website",
    locale: "en_US",
    siteName: "Md Kanok Miah",
    title: "Best SEO Expert in Dhaka, Bangladesh | Md Kanok Miah — #1 SEO Specialist",
    description:
      "Looking for the best SEO expert in Dhaka, Bangladesh? Md Kanok Miah is a top-rated SEO specialist. Get higher rankings and more traffic with proven SEO strategies.",
    url: "https://kanokmiah.com.bd",
    images: [{ url: "/kanok-miah-profile.webp", width: 400, height: 400, alt: "Md Kanok Miah — SEO Expert Dhaka" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "Best SEO Expert in Dhaka, Bangladesh | Md Kanok Miah — #1 SEO Specialist",
    description:
      "Looking for the best SEO expert in Dhaka, Bangladesh? Md Kanok Miah helps businesses rank higher, grow faster, dominate search.",
    images: ["/kanok-miah-profile.webp"],
  },
  robots: {
    index: true,
    follow: true,
    "max-snippet": -1,
    "max-image-preview": "large",
  },
  icons: {
    icon: [{ url: "/favicon.ico", sizes: "32x32", type: "image/png" }],
    apple: "/icon-192.png",
  },
};

export default function RootLayout({ children }) {
  return (
    <html
      lang="en"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
    >
      <head>
        <OrganizationSchema />
        <LocalBusinessSchema />
        <WebSiteSchema />
        <PersonSchema />
        {/* Google Search Console verification */}
        <meta name="google-site-verification" content="etLH7vKLG9Iph0mFN1a8sOYhxFptpi_h_VYRk3mUFvM" />
        {/* Bing Webmaster Tools verification - set actual Bing code or leave empty */}
        <meta name="msvalidate.01" content="" />
      </head>
      <body className="min-h-full flex flex-col">{children}</body>
    </html>
  );
}