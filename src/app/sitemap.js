import { readFileSync, existsSync } from "fs";

export default async function sitemap() {
  const baseUrl = "https://kanokmiah.com.bd";

  // Helper: parse real blog dates from data.js, fallback to staggered dates
  function getBlogDates() {
    const blogPath = "src/app/blog/data.js";
    const dates = {};
    if (existsSync(blogPath)) {
      const content = readFileSync(blogPath, "utf8");
      // Match slug + date pairs: slug: "xxx", ... date: "YYYY-MM-DD"
      const slugs = [...content.matchAll(/slug:\s*"([^"]+)"/g)];
      const dateMatches = [...content.matchAll(/date:\s*"([^"]+)"/g)];
      for (let i = 0; i < slugs.length && i < dateMatches.length; i++) {
        dates[slugs[i][1]] = dateMatches[i][1];
      }
    }
    return dates;
  }

  const blogDates = getBlogDates();

  const staticPages = [
    { url: baseUrl, lastModified: "2026-07-14", changeFrequency: "weekly", priority: 1.0 },
    { url: `${baseUrl}/services`, lastModified: "2026-07-14", changeFrequency: "weekly", priority: 0.9 },
    { url: `${baseUrl}/industries`, lastModified: "2026-07-14", changeFrequency: "weekly", priority: 0.9 },
    { url: `${baseUrl}/about`, lastModified: "2026-07-10", changeFrequency: "monthly", priority: 0.7 },
    { url: `${baseUrl}/contact`, lastModified: "2026-07-10", changeFrequency: "monthly", priority: 0.7 },
    { url: `${baseUrl}/privacy-policy`, lastModified: "2026-06-01", changeFrequency: "yearly", priority: 0.3 },
    { url: `${baseUrl}/terms-of-service`, lastModified: "2026-06-01", changeFrequency: "yearly", priority: 0.3 },
    { url: `${baseUrl}/blog`, lastModified: "2026-07-14", changeFrequency: "daily", priority: 0.8 },
    { url: `${baseUrl}/faq`, lastModified: "2026-07-10", changeFrequency: "monthly", priority: 0.7 },
    { url: `${baseUrl}/case-studies`, lastModified: "2026-07-14", changeFrequency: "weekly", priority: 0.8 },
    { url: `${baseUrl}/portfolio`, lastModified: "2026-07-10", changeFrequency: "weekly", priority: 0.8 },
    { url: `${baseUrl}/locations/dhaka`, lastModified: "2026-07-14", changeFrequency: "monthly", priority: 0.8 },
    { url: `${baseUrl}/locations/chittagong`, lastModified: "2026-07-14", changeFrequency: "monthly", priority: 0.7 },
    { url: `${baseUrl}/locations/sylhet`, lastModified: "2026-07-14", changeFrequency: "monthly", priority: 0.7 },
    { url: `${baseUrl}/locations/khulna`, lastModified: "2026-07-14", changeFrequency: "monthly", priority: 0.7 },
    { url: `${baseUrl}/locations/rajshahi`, lastModified: "2026-07-14", changeFrequency: "monthly", priority: 0.7 },
    { url: `${baseUrl}/locations/barisal`, lastModified: "2026-07-14", changeFrequency: "monthly", priority: 0.7 },
    { url: `${baseUrl}/locations/rangpur`, lastModified: "2026-07-14", changeFrequency: "monthly", priority: 0.7 },
    { url: `${baseUrl}/locations/mymensingh`, lastModified: "2026-07-14", changeFrequency: "monthly", priority: 0.7 },
  ];

  const industrySlugs = [
    "garments-textile", "ecommerce", "smm-panel", "real-estate",
    "cleaning", "spa-salon", "medical", "education", "food-restaurant",
  ];

  const industriesPages = industrySlugs.map((slug) => ({
    url: `${baseUrl}/industries/${slug}`,
    lastModified: "2026-07-14",
    changeFrequency: "monthly",
    priority: 0.8,
  }));

  // Read services from data file via filesystem
  let serviceSlugs = [];
  try {
    const svcPath = "src/app/services/data.js";
    if (existsSync(svcPath)) {
      const svcContent = readFileSync(svcPath, "utf8");
      const matches = svcContent.matchAll(/slug:\s*"([^"]+)"/g);
      for (const m of matches) serviceSlugs.push(m[1]);
    }
  } catch (e) {
    // silently fail
  }

  const servicePages = serviceSlugs.map((slug) => ({
    url: `${baseUrl}/services/${slug}`,
    lastModified: "2026-07-14",
    changeFrequency: "weekly",
    priority: 0.9,
  }));

  // Read blog posts using real dates from data file
  let blogSlugs = [];
  try {
    const blogPath = "src/app/blog/data.js";
    if (existsSync(blogPath)) {
      const blogContent = readFileSync(blogPath, "utf8");
      const matches = blogContent.matchAll(/slug:\s*"([^"]+)"/g);
      for (const m of matches) blogSlugs.push(m[1]);
    }
  } catch (e) {
    // silently fail
  }

  const blogPages = blogSlugs.map((slug) => ({
    url: `${baseUrl}/blog/${slug}`,
    lastModified: blogDates[slug] || "2026-07-14",
    changeFrequency: "monthly",
    priority: 0.7,
  }));

  return [...staticPages, ...industriesPages, ...servicePages, ...blogPages];
}
