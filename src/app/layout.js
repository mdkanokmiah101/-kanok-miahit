/**
 * Md Kanok Miah — SEO Expert in Dhaka, Bangladesh
 * Built with Next.js 16
 * Last deployed: 2026-07-09 (SEO title template fix + Turbopack compat)
 */
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import Link from "next/link";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const dynamic = 'force-dynamic';

export const metadata = {
  metadataBase: new URL("https://kanokmiah.com.bd"),
  title: {
    default: "SEO Expert in Dhaka, Bangladesh | Md Kanok Miah",
    template: "%s \u2014 Md Kanok Miah",
  },
  description:
    "Md Kanok Miah \u2014 top SEO expert in Dhaka, Bangladesh. 6+ years experience. Higher rankings, more traffic, qualified leads. Local SEO, Technical SEO, Link Building, GEO.",
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
  // Each page overrides alternates.canonical individually above the root level.
  // Setting a default canonical to "/" here would override those page-level values
  // in Next.js 16's metadata merging. We let pages declare their own canonical.
  openGraph: {
    type: "website",
    locale: "en_US",
    siteName: "Md Kanok Miah",
    title: "SEO Expert in Dhaka, Bangladesh | Md Kanok Miah",
    description:
      "Md Kanok Miah \u2014 top SEO expert in Dhaka, Bangladesh. Higher rankings, more traffic, qualified leads.",
    url: "https://kanokmiah.com.bd",
    images: [{ url: "/kanok-miah-profile.webp", width: 400, height: 400, alt: "Md Kanok Miah \u2014 SEO Expert Dhaka" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "SEO Expert in Dhaka, Bangladesh | Md Kanok Miah",
    description:
      "Looking for the best SEO expert in Dhaka? Md Kanok Miah helps businesses rank higher, grow faster, and dominate search.",
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
  // Pre-serialize JSON-LD schemas to avoid JSX brace-parsing issues with Turbopack
  const orgSchema = JSON.stringify({"@context":"https://schema.org","@type":"Organization","name":"Md Kanok Miah","url":"https://kanokmiah.com.bd","logo":"https://kanokmiah.com.bd/favicon.ico","description":"Bangladesh-focused SEO expert. Local SEO, technical SEO, link building, semantic SEO, and GEO optimization.","address":{"@type":"PostalAddress","addressLocality":"Dhaka","addressCountry":"BD"},"contactPoint":{"@type":"ContactPoint","telephone":"+880-1712-883101","contactType":"customer service","availableLanguage":["English","Bengali"]},"sameAs":["https://kanokmiah.com","https://www.facebook.com/mdkanokmiahweb","https://bd.linkedin.com/in/kanok-miah","https://www.youtube.com/@kanokmiah","https://www.pinterest.com/mdkanokmiah","https://www.instagram.com/kanokmiahbd","https://www.tiktok.com/@kanokmiahbd","https://wa.me/8801712883101"],"foundingDate":"2020","knowsAbout":["Search Engine Optimization","Local SEO","Technical SEO","Link Building","Semantic SEO","GEO / AI Search Optimization","E-commerce SEO","Content Marketing","Google Business Profile Optimization","Generative Engine Optimization"]});
  const lbSchema = JSON.stringify({"@context":"https://schema.org","@type":"LocalBusiness","name":"Md Kanok Miah \u2014 SEO Expert","url":"https://kanokmiah.com.bd","telephone":"+880-1712-883101","email":"mdkanokmiah232@gmail.com","description":"Best SEO expert in Dhaka, Bangladesh. Specializing in Local SEO, Technical SEO, Link Building, and GEO optimization.","image":"https://kanokmiah.com.bd/kanok-miah-profile.webp","address":{"@type":"PostalAddress","addressLocality":"Dhaka","addressCountry":"BD"},"geo":{"@type":"GeoCoordinates","latitude":"23.8103","longitude":"90.4125"},"priceRange":"$$","areaServed":["Dhaka","Mirpur","Gulshan","Banani","Uttara","Dhanmondi","Chittagong","Sylhet","Bangladesh"],"aggregateRating":{"@type":"AggregateRating","ratingValue":"4.9","bestRating":"5","ratingCount":"50"}});
  const wsSchema = JSON.stringify({"@context":"https://schema.org","@type":"WebSite","name":"Md Kanok Miah","url":"https://kanokmiah.com.bd","description":"Best SEO expert in Dhaka, Bangladesh. Get higher rankings, more traffic, and qualified leads with proven SEO strategies.","inLanguage":["en","bn"],"potentialAction":{"@type":"SearchAction","target":{"@type":"EntryPoint","urlTemplate":"https://kanokmiah.com.bd/blog?q={search_term_string}"},"query-input":"required name=search_term_string"}});
  const personSchema = JSON.stringify({"@context":"https://schema.org","@type":"Person","name":"Md Kanok Miah","alternateName":"Kanok Miah","givenName":"Kanok","familyName":"Miah","url":"https://kanokmiah.com.bd","sameAs":["https://kanokmiah.com","https://www.facebook.com/mdkanokmiahweb","https://bd.linkedin.com/in/kanok-miah","https://www.youtube.com/@kanokmiah","https://www.pinterest.com/mdkanokmiah","https://www.instagram.com/kanokmiahbd","https://www.tiktok.com/@kanokmiahbd"],"jobTitle":"SEO Expert & Digital Marketing Specialist","worksFor":{"@type":"Organization","name":"Md Kanok Miah"},"description":"Best SEO expert in Dhaka, Bangladesh with 6+ years of experience. Specializing in local SEO, technical SEO, link building, and GEO optimization."});
  const servicesSchema = JSON.stringify({"@context":"https://schema.org","@graph":[{"@type":"Service","name":"Local SEO","description":"Rank your business on Google Maps across Dhaka, Chittagong, Sylhet and beyond. GBP optimization, local citations, near-me SEO for Bangladeshi audiences.","provider":{"@type":"Person","name":"Md Kanok Miah"},"areaServed":["Dhaka","Chittagong","Sylhet","Bangladesh"],"serviceType":"Local SEO","offers":{"@type":"Offer","priceSpecification":{"@type":"PriceSpecification","priceCurrency":"BDT","description":"Custom pricing based on project scope"}}},{"@type":"Service","name":"On-Page SEO","description":"Keyword-optimized content, meta tags, header structure, internal linking, and schema markup crafted for Bangladesh search behavior.","provider":{"@type":"Person","name":"Md Kanok Miah"},"areaServed":["Dhaka","Chittagong","Sylhet","Bangladesh"],"serviceType":"On-Page SEO","offers":{"@type":"Offer","priceSpecification":{"@type":"PriceSpecification","priceCurrency":"BDT","description":"Custom pricing based on project scope"}}},{"@type":"Service","name":"Link Building","description":"Quality backlinks from Bangladeshi and international directories, guest posts, and niche-relevant websites that drive real authority gains.","provider":{"@type":"Person","name":"Md Kanok Miah"},"areaServed":["Dhaka","Chittagong","Sylhet","Bangladesh"],"serviceType":"Link Building","offers":{"@type":"Offer","priceSpecification":{"@type":"PriceSpecification","priceCurrency":"BDT","description":"Custom pricing based on project scope"}}},{"@type":"Service","name":"Technical SEO","description":"Site speed optimization, Core Web Vitals, mobile-first indexing, crawl budget fixes, and structured data implementation.","provider":{"@type":"Person","name":"Md Kanok Miah"},"areaServed":["Dhaka","Chittagong","Sylhet","Bangladesh"],"serviceType":"Technical SEO","offers":{"@type":"Offer","priceSpecification":{"@type":"PriceSpecification","priceCurrency":"BDT","description":"Custom pricing based on project scope"}}},{"@type":"Service","name":"GEO / AI Search","description":"Optimize for ChatGPT, Gemini, Perplexity, and Google AI Overviews. Entity-first SEO built for the AI-powered search era.","provider":{"@type":"Person","name":"Md Kanok Miah"},"areaServed":["Dhaka","Chittagong","Sylhet","Bangladesh"],"serviceType":"GEO / AI Search","offers":{"@type":"Offer","priceSpecification":{"@type":"PriceSpecification","priceCurrency":"BDT","description":"Custom pricing based on project scope"}}},{"@type":"Service","name":"E-commerce SEO","description":"Shopify, Daraz, WooCommerce SEO. Product page optimization, category restructuring, and conversion-focused search strategy.","provider":{"@type":"Person","name":"Md Kanok Miah"},"areaServed":["Dhaka","Chittagong","Sylhet","Bangladesh"],"serviceType":"E-commerce SEO","offers":{"@type":"Offer","priceSpecification":{"@type":"PriceSpecification","priceCurrency":"BDT","description":"Custom pricing based on project scope"}}},{"@type":"FAQPage","mainEntity":[{"@type":"Question","name":"How do I rank my business on Google Maps in Dhaka?","acceptedAnswer":{"@type":"Answer","text":"To rank your business on Google Maps in Dhaka, start by claiming and verifying your Google Business Profile with accurate NAP (Name, Address, Phone). Choose the most specific category for your business, add 20+ high-quality photos, collect genuine customer reviews, and post weekly updates. I also recommend building local citations on Bangladeshi directories like BD Yellow Pages and BdTradeInfo. Most Dhaka businesses see improved Google Maps visibility within 4-6 weeks of proper optimization."}},{"@type":"Question","name":"What is the best SEO strategy for a new website in Bangladesh?","acceptedAnswer":{"@type":"Answer","text":"For new websites in Bangladesh, the best strategy starts with technical SEO \u2014 ensure fast loading speeds, mobile responsiveness, and proper crawl setup. Then focus on keyword research targeting both Bengali and English search terms that your local customers use. Create high-quality content around these keywords, build a Google Business Profile, and start earning backlinks from Bangladeshi news sites and directories. Patience is key \u2014 most new sites take 3-6 months to see meaningful ranking improvements on Google Bangladesh."}},{"@type":"Question","name":"Can you help my Daraz store get more sales from Google?","acceptedAnswer":{"@type":"Answer","text":"Absolutely. I optimize Daraz seller pages for both Daraz internal search and Google organic search. This includes optimizing product titles with high-volume keywords in Bengali and English, writing detailed unique product descriptions, optimizing images with descriptive alt text, and encouraging product reviews. I also work on off-page signals like backlinks to your Daraz store. Most Daraz sellers see 50-100% organic traffic growth within 3 months of implementing these strategies."}},{"@type":"Question","name":"How much does SEO cost for small businesses in Bangladesh?","acceptedAnswer":{"@type":"Answer","text":"SEO pricing for small businesses in Bangladesh varies based on competition and scope. Monthly retainers typically range from BDT 15,000 to BDT 50,000. A BDT 15,000-20,000 plan usually includes local SEO (Google Business Profile optimization, citation building) and basic on-page SEO. More comprehensive packages (BDT 30,000-50,000) include technical SEO, link building, content creation, and detailed monthly reporting. I offer a free initial audit to recommend the right plan for your budget and goals."}},{"@type":"Question","name":"What is the difference between GEO and traditional SEO?","acceptedAnswer":{"@type":"Answer","text":"GEO (Generative Engine Optimization) optimizes your content for AI-powered search engines like ChatGPT, Google AI Overviews, Gemini, and Perplexity. Traditional SEO focuses on keyword rankings and backlinks for Google's blue-link search results. GEO uses entity-based content, authoritative citations, and structured data to help AI models accurately extract and cite your information. For Bangladeshi businesses, GEO is emerging as a crucial forward-looking strategy \u2014 those who optimize for AI search now will have a significant competitive advantage as growth accelerates."}}]}]});
  return (
    <html
      lang="en"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
    >
      <head>
        {/* Google Search Console verification */}
        <meta name="google-site-verification" content="etLH7vKLG9Iph0mFN1a8sOYhxFptpi_h_VYRk3mUFvM" />
        {/* Bing Webmaster Tools verification (placeholder) */}
        <meta name="msvalidate.01" content="" />
        {/* JSON-LD Structured Data */}
        <script type="application/ld+json" dangerouslySetInnerHTML={{__html: orgSchema}} />
        <script type="application/ld+json" dangerouslySetInnerHTML={{__html: lbSchema}} />
        <script type="application/ld+json" dangerouslySetInnerHTML={{__html: wsSchema}} />
        <script type="application/ld+json" dangerouslySetInnerHTML={{__html: personSchema}} />
      </head>
      <body className="min-h-full flex flex-col">
        {/* Service + FAQ schemas inline */}
        <script type="application/ld+json" dangerouslySetInnerHTML={{__html: servicesSchema}} />
        {children}
      </body>
    </html>
  );
}
