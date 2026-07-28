const fs = require('fs');

const fileContent = fs.readFileSync('/root/kanok-miahit/src/app/blog/data.js', 'utf8');

// Define the posts we need to check with their slugs
const slugsToAnalyze = [
  'geo-optimization-prepare-business-ai-search',
  'seo-garments-textile-industry-b2b-lead-generation',
  'mobile-seo-optimization-bangladesh-mobile-first-era',
  'seo-healthcare-medical-clinics-bangladesh',
  'why-md-kanok-miah-is-the-best-seo-expert-in-dhaka-bangladesh',
  'how-to-choose-best-seo-expert-dhaka-15-things',
  'seo-expert-vs-seo-agency-dhaka-which-is-right',
  'top-10-seo-mistakes-dhaka-businesses-fix',
  'what-does-seo-expert-do-guide-business-owners',
  'ai-seo-2026-dhaka-experts-optimize-google-ai-chatgpt'
];

// Parse posts from the JS array
// Since it's a JS file with const posts = [...], let's extract each post object
// We'll use regex to find slug lines and extract the post objects

function extractPostContent(fullContent, slug) {
  // Find the post object starting with `{` before the slug
  const slugRegex = new RegExp(`slug:\\s*"${slug}"`);
  const slugMatch = fullContent.match(slugRegex);
  if (!slugMatch) return null;
  
  const slugIndex = slugMatch.index;
  
  // Find the start of the post object - go back from slugIndex to find `  {`
  const beforeSlug = fullContent.substring(0, slugIndex);
  const lastObjStart = beforeSlug.lastIndexOf('  {\n');
  const startIndex = lastObjStart !== -1 ? lastObjStart : slugIndex - 40;
  
  // Find the end of the post object - find `,\n  }` or `,\n}` after slug
  const afterSlug = fullContent.substring(slugIndex);
  // Find the closing pattern: backtick + `,\n  }` or `,\n}`
  const closeMatch = afterSlug.match(/`,?\s*\n\s*\}/);
  if (!closeMatch) return null;
  
  const endIndex = slugIndex + closeMatch.index + closeMatch[0].length;
  const postStr = fullContent.substring(startIndex, endIndex);
  
  return postStr;
}

function extractField(postStr, fieldName) {
  const regex = new RegExp(`\\s{4}${fieldName}:\\s*(.+)`, 's');
  const match = postStr.match(regex);
  if (!match) return null;
  let val = match[1].trim();
  // Remove trailing comma
  if (val.endsWith(',')) val = val.slice(0, -1);
  return val;
}

function extractContentField(postStr) {
  const match = postStr.match(/content:\s*`\n?([\s\S]*?)`\s*,?\s*\n\s*\}/);
  if (!match) return '';
  return match[1];
}

function countOccurrences(text, keyword) {
  const regex = new RegExp(keyword.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi');
  const matches = text.match(regex);
  return matches ? matches.length : 0;
}

function extractQuestionHeadings(content) {
  const regex = /^##+\s+(How\s|What\s|Why\s|When\s|Where\s|Can\s|Do\s|Is\s|Are\s)/gim;
  const matches = content.match(regex);
  return matches ? matches : [];
}

function extractInternalLinks(content) {
  const regex = /\(\/(blog|services|locations|industries)\/[^)]+\)/g;
  const matches = content.match(regex);
  return matches ? matches : [];
}

function extractEntities(content) {
  const entities = {
    dhaka: (content.match(/Dhaka/gi) || []).length,
    bangladesh: (content.match(/Bangladesh/gi) || []).length,
  };
  return entities;
}

// Main analysis
for (const slug of slugsToAnalyze) {
  console.log(`\n=== Analyzing: ${slug} ===`);
  const postStr = extractPostContent(fileContent, slug);
  if (!postStr) {
    console.log(`Could not find post: ${slug}`);
    continue;
  }
  
  // Extract fields
  const title = extractField(postStr, 'title');
  const date = extractField(postStr, 'date');
  const excerpt = extractField(postStr, 'excerpt');
  const tagsMatch = postStr.match(/tags:\s*\[([^\]]+)\]/);
  const tags = tagsMatch ? tagsMatch[1].split(',').map(t => t.trim().replace(/"/g, '')) : [];
  const dateModified = postStr.includes('dateModified');
  const faqs = postStr.includes('faqs:');
  const content = extractContentField(postStr);
  
  console.log(`Title: ${title}`);
  console.log(`Date: ${date}`);
  console.log(`Has excerpt: ${!!excerpt}`);
  console.log(`Tags: ${JSON.stringify(tags)}`);
  console.log(`Has dateModified: ${dateModified}`);
  console.log(`Has faqs: ${faqs}`);
  console.log(`Content length: ${content.length} chars`);
  
  // A. TF-IDF - extract primary keyword from title
  // First meaningful noun phrase
  const titleWords = title.split(/[:—–-]/)[0].trim(); // Get part before colon/dash
  let primaryKeyword = '';
  
  if (slug === 'geo-optimization-prepare-business-ai-search') primaryKeyword = 'GEO Optimization';
  else if (slug === 'seo-garments-textile-industry-b2b-lead-generation') primaryKeyword = 'SEO for Garments';
  else if (slug === 'mobile-seo-optimization-bangladesh-mobile-first-era') primaryKeyword = 'Mobile SEO';
  else if (slug === 'seo-healthcare-medical-clinics-bangladesh') primaryKeyword = 'Healthcare SEO';
  else if (slug === 'why-md-kanok-miah-is-the-best-seo-expert-in-dhaka-bangladesh') primaryKeyword = 'SEO Expert in Dhaka';
  else if (slug === 'how-to-choose-best-seo-expert-dhaka-15-things') primaryKeyword = 'SEO Expert in Dhaka';
  else if (slug === 'seo-expert-vs-seo-agency-dhaka-which-is-right') primaryKeyword = 'SEO Expert vs SEO Agency';
  else if (slug === 'top-10-seo-mistakes-dhaka-businesses-fix') primaryKeyword = 'SEO Mistakes';
  else if (slug === 'what-does-seo-expert-do-guide-business-owners') primaryKeyword = 'SEO Expert';
  else if (slug === 'ai-seo-2026-dhaka-experts-optimize-google-ai-chatgpt') primaryKeyword = 'AI SEO';
  
  const kwCount = countOccurrences(content, primaryKeyword);
  console.log(`\nA. TF-IDF: keyword="${primaryKeyword}", occurrences=${kwCount}`);
  
  // B. Entities
  const entityDhaka = countOccurrences(content, 'Dhaka');
  const entityBangladesh = countOccurrences(content, 'Bangladesh');
  console.log(`B. Entities: Dhaka=${entityDhaka}, Bangladesh=${entityBangladesh}`);
  
  // C. Pillar Link - look for links to pillar page
  const pillarLinks = content.match(/\/blog\/complete-seo-guide-bangladesh-businesses-2026/g);
  console.log(`C. Pillar links to complete-seo-guide: ${pillarLinks ? pillarLinks.length : 0}`);
  
  // D. AEO/GEO - question headings
  const questionHeadings = extractQuestionHeadings(content);
  console.log(`D. Question headings (${questionHeadings.length}): ${questionHeadings.slice(0,5).join(', ')}...`);
  
  // E. Internal links
  const internalLinks = extractInternalLinks(content);
  console.log(`E. Internal links: ${internalLinks.length}`);
  console.log(`   Links: ${internalLinks.slice(0,10).join(', ')}`);
  
  // F. Schema readiness
  console.log(`F. Schema Ready: title=${!!title}, excerpt=${!!excerpt}, date=${!!date}`);
}
