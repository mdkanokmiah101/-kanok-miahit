// Read the data file and extract metrics for each blog post
const fs = require('fs');

const content = fs.readFileSync('/root/kanok-miahit/src/app/blog/data.js', 'utf-8');
const lines = content.split('\n');

// Define post ranges (0-indexed)
const posts = [
  { slug: 'how-to-choose-best-seo-expert-dhaka-15-things', start: 26518, end: 26716 },  // 0-indexed
  { slug: 'seo-expert-vs-seo-agency-dhaka-which-is-right', start: 26718, end: 26941 },
  { slug: 'top-10-seo-mistakes-dhaka-businesses-fix', start: 26943, end: 27133 },
  { slug: 'what-does-seo-expert-do-guide-business-owners', start: 27137, end: 27471 },
  { slug: 'seo-case-study-dhaka-businesses-increased-organic-traffic', start: 27473, end: 27795 },
  { slug: 'hiring-seo-expert-dhaka-better-roi-than-paid-ads', start: 27797, end: 28068 },
  { slug: 'ai-seo-2026-dhaka-experts-optimize-google-ai-chatgpt', start: 28071, end: 28355 },
  { slug: 'watchzonebd-seo-case-study', start: 28357, end: 28575 },
];

// Extract each post's data
for (const p of posts) {
  const postLines = lines.slice(p.start, p.end + 1);
  const postText = postLines.join('\n');
  
  console.log(`\n${'='.repeat(80)}`);
  console.log(`POST: ${p.slug}`);
  console.log(`${'='.repeat(80)}`);
  
  // Extract metadata fields
  const slugMatch = postText.match(/slug:\s*"([^"]+)"/);
  const titleMatch = postText.match(/title:\s*"([^"]+)"/);
  const dateMatch = postText.match(/date:\s*"([^"]+)"/);
  const authorMatch = postText.match(/author:\s*"([^"]+)"/);
  const excerptMatch = postText.match(/excerpt:\s*\n\s*"([^"]+)"/);
  const tagsMatch = postText.match(/tags:\s*\[([^\]]+)\]/);
  
  console.log(`\n--- METADATA ---`);
  console.log(`Title: ${titleMatch ? titleMatch[1] : 'NOT FOUND'}`);
  console.log(`Date: ${dateMatch ? dateMatch[1] : 'NOT FOUND'}`);
  console.log(`Author: ${authorMatch ? authorMatch[1] : 'NOT FOUND'}`);
  console.log(`Excerpt: ${excerptMatch ? excerptMatch[1] : 'NOT FOUND'}`);
  console.log(`Tags: ${tagsMatch ? tagsMatch[1] : 'NOT FOUND'}`);
  
  // Extract primary keyword from title
  const title = titleMatch ? titleMatch[1] : '';
  const titleWords = title.toLowerCase().split(/[\s,;:!?()]+/).filter(w => w.length > 2);
  // Primary keyword is typically the main topic phrase from title
  // Let's extract it intelligently
  let primaryKeyword = '';
  if (title.includes('SEO Expert')) {
    primaryKeyword = 'SEO Expert';
  } else if (title.includes('SEO Mistakes')) {
    primaryKeyword = 'SEO mistakes';
  } else if (title.includes('SEO Case Study')) {
    primaryKeyword = 'SEO case study';
  } else if (title.includes('AI SEO')) {
    primaryKeyword = 'AI SEO';
  } else if (title.includes('Hiring an SEO Expert')) {
    primaryKeyword = 'SEO Expert';
  } else if (title.includes('WatchZoneBD')) {
    primaryKeyword = 'WatchZoneBD';
  } else if (title.includes('SEO Specialist')) {
    primaryKeyword = 'SEO Specialist';
  } else {
    primaryKeyword = title.split(' ').slice(0, 3).join(' ');
  }
  
  // Extract content between backticks (the actual body)
  const contentMatch = postText.match(/content:\s*`\s*([\s\S]*?)`\s*,?\s*\n?\s*}/);
  let body = '';
  if (contentMatch) {
    body = contentMatch[1];
  } else {
    // Try alternative pattern
    const contentStart = postText.indexOf('content: `');
    if (contentStart >= 0) {
      const contentBodyStart = contentStart + 'content: `'.length;
      // Find the closing backtick - it should be followed by ,\n  }
      const closeIdx = postText.lastIndexOf('`');
      if (closeIdx > contentBodyStart) {
        body = postText.slice(contentBodyStart, closeIdx);
      }
    }
  }
  
  if (!body) {
    console.log(`\nERROR: Could not extract content body for ${p.slug}`);
    continue;
  }
  
  // a) First 100 words and last 100 words
  const words = body.trim().split(/\s+/);
  const first100 = words.slice(0, 100).join(' ');
  const last100 = words.slice(Math.max(0, words.length - 100)).join(' ');
  
  console.log(`\n--- a) FIRST 100 WORDS OF CONTENT ---`);
  console.log(first100);
  console.log(`\n--- a) LAST 100 WORDS OF CONTENT ---`);
  console.log(last100);
  console.log(`\nTotal word count of body: ${words.length}`);
  
  // b) Count primary keyword occurrences
  const bodyLower = body.toLowerCase();
  const kwVariants = [];
  
  // Determine keyword based on title
  if (title.includes('best SEO expert in Dhaka') || title.includes('SEO Expert in Dhaka') || title.includes('SEO expert in Dhaka')) {
    kwVariants.push('seo expert in dhaka');
    kwVariants.push('best seo expert in dhaka');
  } else if (title.includes('SEO Expert vs SEO Agency')) {
    kwVariants.push('seo expert vs seo agency');
    kwVariants.push('seo expert');
    kwVariants.push('seo agency');
  } else if (title.includes('SEO Mistakes')) {
    kwVariants.push('seo mistakes');
    kwVariants.push('seo mistakes dhaka');
  } else if (title.includes('What Does an SEO Expert')) {
    kwVariants.push('what does an seo expert do');
    kwVariants.push('seo specialist');
    kwVariants.push('seo expert do');
  } else if (title.includes('SEO Case Study')) {
    kwVariants.push('seo case study');
    kwVariants.push('seo case study dhaka');
  } else if (title.includes('Hiring an SEO Expert')) {
    kwVariants.push('seo roi');
    kwVariants.push('seo roi dhaka');
    kwVariants.push('seo expert');
    kwVariants.push('seo consultant');
  } else if (title.includes('AI SEO')) {
    kwVariants.push('ai seo');
    kwVariants.push('ai seo in dhaka');
    kwVariants.push('geo');
  } else if (title.includes('WatchZoneBD')) {
    kwVariants.push('watchzonebd');
    kwVariants.push('e-commerce seo');
  }
  
  console.log(`\n--- b) KEYWORD OCCURRENCES ---`);
  console.log(`Primary keyword variants from title: ${kwVariants.join(', ')}`);
  for (const kw of kwVariants) {
    const regex = new RegExp(kw.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi');
    const count = (bodyLower.match(regex) || []).length;
    console.log(`  "${kw}": ${count} occurrences`);
  }
  
  // Also count "best SEO expert in Dhaka" for posts that use it
  const bestExpertRegex = /best seo expert in dhaka/gi;
  const bestExpertCount = (bodyLower.match(bestExpertRegex) || []).length;
  if (bestExpertCount > 0) {
    console.log(`  "best seo expert in dhaka": ${bestExpertCount} occurrences`);
  }
  
  // c) Internal links
  console.log(`\n--- c) INTERNAL LINKS ---`);
  // Links starting with / (internal links)
  const internalLinkRegex = /\]\((\/[^)]+)\)/g;
  let linkMatch;
  const internalLinks = new Set();
  while ((linkMatch = internalLinkRegex.exec(body)) !== null) {
    internalLinks.add(linkMatch[1].split(/[\s#]/)[0]); // clean up
  }
  // Also find markdown links that are just paths
  const simplePathRegex = /\]\((\/[a-zA-Z0-9\/\-_]+)\)/g;
  while ((linkMatch = simplePathRegex.exec(body)) !== null) {
    internalLinks.add(linkMatch[1]);
  }
  
  if (internalLinks.size > 0) {
    for (const link of [...internalLinks].sort()) {
      console.log(`  ${link}`);
    }
  } else {
    console.log(`  No internal links found`);
  }
  
  // d) Question-based headings
  console.log(`\n--- d) QUESTION-BASED HEADINGS (H2/H3) ---`);
  const questionHeadings = [];
  const headingRegex = /^##+\s+(How|What|Why|When|Where|Can|Do|Is|Are)\b.*$/gmi;
  let hMatch;
  while ((hMatch = headingRegex.exec(body)) !== null) {
    questionHeadings.push(hMatch[0].trim());
  }
  // Also check for markdown headings that are questions
  const headingRegex2 = /^##+\s+.*\?$/gmi;
  let hMatch2;
  while ((hMatch2 = headingRegex2.exec(body)) !== null) {
    const q = hMatch2[0].trim();
    if (!questionHeadings.some(h => h === q)) {
      questionHeadings.push(q);
    }
  }
  
  console.log(`Count: ${questionHeadings.length}`);
  for (const h of questionHeadings) {
    console.log(`  ${h}`);
  }
  
  // e) Tags, title, date, excerpt - already printed above
  
  // f) Entity counts
  console.log(`\n--- f) ENTITY OCCURRENCES ---`);
  const entities = {};
  
  // "Dhaka"
  const dhakaCount = (bodyLower.match(/dhaka/g) || []).length;
  console.log(`  "Dhaka": ${dhakaCount} occurrences`);
  
  // "Bangladesh"
  const bangladeshCount = (bodyLower.match(/bangladesh/gi) || []).length;
  console.log(`  "Bangladesh": ${bangladeshCount} occurrences`);
  
  // Main service type
  const seoCount = (bodyLower.match(/\bseo\b/g) || []).length;
  console.log(`  "SEO": ${seoCount} occurrences`);
  
  // E-commerce
  const ecomCount = (bodyLower.match(/e-commerce|ecommerce/gi) || []).length;
  console.log(`  "E-commerce/Ecommerce": ${ecomCount} occurrences`);
  
  if (title.toLowerCase().includes('watchzonebd')) {
    const watchCount = (bodyLower.match(/watchzonebd/gi) || []).length;
    console.log(`  "WatchZoneBD": ${watchCount} occurrences`);
    const watchCount2 = (bodyLower.match(/watch/gi) || []).length;
    console.log(`  "Watch": ${watchCount2} occurrences`);
  }
  
  if (title.toLowerCase().includes('geo') || title.toLowerCase().includes('ai seo')) {
    const geoCount = (bodyLower.match(/\bgeo\b/g) || []).length;
    console.log(`  "GEO": ${geoCount} occurrences`);
    const aiCount = (bodyLower.match(/\bai\b/g) || []).length;
    console.log(`  "AI": ${aiCount} occurrences`);
  }
  
  // Count original links to kanokmiah.com.bd (external but internal to the brand)
  const externalLinks = body.match(/\]\(https?:\/\/kanokmiah\.com\.bd[^)]*\)/g) || [];
  console.log(`  External links to kanokmiah.com.bd: ${externalLinks.length}`);
}
