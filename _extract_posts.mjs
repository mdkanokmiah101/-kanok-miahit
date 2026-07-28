// Script to extract specific blog posts from data.js and output JSON
import posts from './src/app/blog/data.js';

const slugsOfInterest = [
  "geo-optimization-prepare-business-ai-search",
  "seo-garments-textile-industry-b2b-lead-generation",
  "seo-healthcare-medical-clinics-bangladesh",
  "why-md-kanok-miah-is-the-best-seo-expert-in-dhaka-bangladesh",
  "locksmith-dundee-seo-case-study",
  "landlord-certificates-seo-case-study",
  "das-taxis-scotland-seo-case-study",
  "morethanpanel-seo-case-study",
  "smmgen-seo-case-study",
  "smmsun-seo-case-study",
  "mir-cement-seo-case-study",
  "dhaka-apparels-seo-case-study",
  "stealth-windshield-repairs-seo-case-study",
  "how-to-choose-best-seo-expert-dhaka-15-things",
  "seo-expert-vs-seo-agency-dhaka-which-is-right",
  "top-10-seo-mistakes-dhaka-businesses-fix",
  "what-does-seo-expert-do-guide-business-owners",
  "seo-case-study-dhaka-businesses-increased-organic-traffic",
  "hiring-seo-expert-dhaka-better-roi-than-paid-ads",
  "ai-seo-2026-dhaka-experts-optimize-google-ai-chatgpt",
  "watchzonebd-seo-case-study"
];

const extracted = posts
  .filter(p => slugsOfInterest.includes(p.slug))
  .map(p => ({
    slug: p.slug,
    title: p.title,
    excerpt: p.excerpt,
    date: p.date,
    dateModified: p.dateModified,
    tags: p.tags,
    content: p.content
  }));

console.log(JSON.stringify(extracted, null, 2));
