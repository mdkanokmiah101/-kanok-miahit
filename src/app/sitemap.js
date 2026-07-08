import { readFileSync, readdirSync, existsSync } from "fs";

export default async function sitemap() {
  const baseUrl = "https://kanokmiah.com.bd";

  const staticPages = [
    { url: baseUrl, lastModified: new Date(), changeFrequency: "weekly", priority: 1.0 },
    { url: `${baseUrl}/services`, lastModified: new Date(), changeFrequency: "weekly", priority: 0.9 },
    { url: `${baseUrl}/industries`, lastModified: new Date(), changeFrequency: "weekly", priority: 0.9 },
    { url: `${baseUrl}/about`, lastModified: new Date(), changeFrequency: "monthly", priority: 0.7 },
    { url: `${baseUrl}/contact`, lastModified: new Date(), changeFrequency: "monthly", priority: 0.7 },
    { url: `${baseUrl}/privacy-policy`, lastModified: new Date(), changeFrequency: "yearly", priority: 0.3 },
    { url: `${baseUrl}/terms-of-service`, lastModified: new Date(), changeFrequency: "yearly", priority: 0.3 },
    { url: `${baseUrl}/blog`, lastModified: new Date(), changeFrequency: "daily", priority: 0.8 },
    { url: `${baseUrl}/faq`, lastModified: new Date(), changeFrequency: "monthly", priority: 0.7 },
    { url: `${baseUrl}/case-studies`, lastModified: new Date(), changeFrequency: "weekly", priority: 0.8 },
    { url: `${baseUrl}/portfolio`, lastModified: new Date(), changeFrequency: "weekly", priority: 0.8 },
  ];

  const industrySlugs = [
    "garments-textile", "ecommerce", "smm-panel", "real-estate",
    "cleaning", "spa-salon", "medical", "education", "food-restaurant",
  ];

  const industriesPages = industrySlugs.map((slug) => ({
    url: `${baseUrl}/industries/${slug}`,
    lastModified: new Date(),
    changeFrequency: "monthly",
    priority: 0.8,
  }));

  const locationSlugs = ["dhaka", "chittagong", "sylhet", "khulna", "rajshahi", "barisal", "rangpur", "mymensingh"];
  const locationPages = locationSlugs.map((slug) => ({
    url: `${baseUrl}/locations/${slug}`,
    lastModified: new Date(),
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
    lastModified: new Date(),
    changeFrequency: "weekly",
    priority: 0.9,
  }));

  // Read blog posts from data file via filesystem
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
    lastModified: new Date(),
    changeFrequency: "monthly",
    priority: 0.7,
  }));

  return [...staticPages, ...industriesPages, ...locationPages, ...servicePages, ...blogPages];
}
