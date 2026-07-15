import HomeClient from "./HomeClient";
import { LocalBusinessSchema, FAQSchema } from "@/components/Schema";

export const metadata = {
  title: "Best SEO Expert in Dhaka & Bangladesh | Md Kanok Miah",
  description:
    "Rank higher with Md Kanok Miah, the best SEO expert in Dhaka & Bangladesh. 6+ years, 210+ SEO wins. Free SEO audit — Call 01604-809110.",
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
    canonical: "https://kanokmiah.com.bd/",
  },
  openGraph: {
    type: "website",
    locale: "en_US",
    siteName: "Md Kanok Miah",
    title: "Best SEO Expert in Dhaka, Bangladesh | Md Kanok Miah",
    description:
      "Rank higher on Google & AI Search with Md Kanok Miah, a trusted SEO expert in Dhaka, Bangladesh. 6+ years, 210+ successful SEO campaigns. Free SEO audit—Call 01604-809110.",
    url: "https://kanokmiah.com.bd",
    images: [
      {
        url: "https://kanokmiah.com.bd/kanok-miah-profile.webp",
        width: 400,
        height: 400,
        alt: "Md Kanok Miah — Best SEO Expert in Dhaka, Bangladesh",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "Best SEO Expert in Dhaka, Bangladesh | Md Kanok Miah",
    description:
      "Rank higher on Google & AI Search with Md Kanok Miah, a trusted SEO expert in Dhaka, Bangladesh. 6+ years, 210+ successful SEO campaigns. Free SEO audit—Call 01604-809110.",
    images: ["https://kanokmiah.com.bd/kanok-miah-profile.webp"],
  },
  robots: {
    index: true,
    follow: true,
    "max-snippet": -1,
    "max-image-preview": "large",
  },
  verification: {
    google: "etLH7vKLG9Iph0mFN1a8sOYhxFptpi_h_VYRk3mUFvM",
    other: {
      "msvalidate.01": "A10B9573E2B9D84E27B9BCE37CCB8B28",
    },
  },
};

const homePageFaqs = [
  { question: "How do I rank my business on Google Maps in Dhaka?", answer: "To rank your business on Google Maps in Dhaka, start by claiming and verifying your Google Business Profile with accurate NAP (Name, Address, Phone). Choose the most specific category for your business, add 20+ high-quality photos, collect genuine customer reviews, and post weekly updates. I also recommend building local citations on Bangladeshi directories like BD Yellow Pages and BdTradeInfo. Most Dhaka businesses see improved Google Maps visibility within 4-6 weeks of proper optimization." },
  { question: "What is the best SEO strategy for a new website in Bangladesh?", answer: "For new websites in Bangladesh, the best strategy starts with technical SEO — ensure fast loading speeds, mobile responsiveness, and proper crawl setup. Then focus on keyword research targeting both Bengali and English search terms that your local customers use. Create high-quality content around these keywords, build a Google Business Profile, and start earning backlinks from Bangladeshi news sites and directories. Patience is key — most new sites take 3-6 months to see meaningful ranking improvements on Google Bangladesh." },
  { question: "How long does SEO take to show results?", answer: "SEO typically takes 3-6 months to show meaningful results for most businesses in Bangladesh. However, you may start seeing initial improvements in rankings and traffic within 4-6 weeks for low-competition keywords. Factors that influence the timeline include your website's current state, competition level in your industry, keyword difficulty, content quality, and the aggressiveness of link building efforts. I set realistic expectations and provide monthly progress reports so you can see incremental improvements every step of the way." },
  { question: "How much does SEO cost for small businesses?", answer: "SEO pricing for small businesses in Bangladesh varies based on competition and scope. Monthly retainers typically range from BDT 15,000 to BDT 50,000. A BDT 15,000-20,000 plan usually includes local SEO (Google Business Profile optimization, citation building) and basic on-page SEO. More comprehensive packages (BDT 30,000-50,000) include technical SEO, link building, content creation, and detailed monthly reporting. I offer a free initial audit to recommend the right plan for your budget and goals." },
  { question: "What is the difference between GEO and traditional SEO?", answer: "GEO (Generative Engine Optimization) optimizes your content for AI-powered search engines like ChatGPT, Google AI Overviews, Gemini, and Perplexity. Traditional SEO focuses on keyword rankings and backlinks for Google's blue-link search results. GEO uses entity-based content, authoritative citations, and structured data to help AI models accurately extract and cite your information. For Bangladeshi businesses, GEO is emerging as a crucial forward-looking strategy — those who optimize for AI search now will have a significant competitive advantage as AI adoption accelerates." },
  { question: "Can you help my Daraz store rank higher?", answer: "Absolutely. I optimize Daraz seller pages for both Daraz internal search and Google organic search. This includes optimizing product titles with high-volume keywords in Bengali and English, writing detailed unique product descriptions, optimizing images with descriptive alt text, and encouraging product reviews. I also work on off-page signals like backlinks to your Daraz store. Most Daraz sellers see significant ranking improvements and 50-100% organic traffic growth within 3 months of implementing these strategies." },
];

export default function HomePage() {
  return (
    <>
      {LocalBusinessSchema()}
      <FAQSchema faqs={homePageFaqs} />
      <HomeClient />
    </>
  );
}