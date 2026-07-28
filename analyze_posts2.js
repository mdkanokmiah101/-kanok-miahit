const fs = require('fs');

const fileContent = fs.readFileSync('/root/kanok-miahit/src/app/blog/data.js', 'utf8');

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

function extractPostContent(fullContent, slug) {
  const slugRegex = new RegExp(`slug:\\s*"${slug}"`);
  const slugMatch = fullContent.match(slugRegex);
  if (!slugMatch) return null;
  
  const slugIndex = slugMatch.index;
  
  // Find the start of the post object
  const beforeSlug = fullContent.substring(0, slugIndex);
  const lastObjStart = beforeSlug.lastIndexOf('  {\n');
  let startIndex = lastObjStart !== -1 ? lastObjStart : slugIndex - 40;
  // If it starts with just `{\n` not `  {\n`
  const altObjStart = beforeSlug.lastIndexOf('{\n');
  if (altObjStart > startIndex) startIndex = altObjStart;
  
  const afterSlug = fullContent.substring(slugIndex);
  // Find the closing: backtick , maybe newline, then }
  const closeMatch = afterSlug.match(/`\s*,\s*\n\s*\}/);
  if (!closeMatch) return null;
  
  const endIndex = slugIndex + closeMatch.index + closeMatch[0].length;
  return fullContent.substring(startIndex, endIndex);
}

function extractField(postStr, fieldName) {
  const regex = new RegExp(`\\n\\s{4}${fieldName}:\\s*"((?:[^"\\\\]|\\\\.)*)"`);
  const match = postStr.match(regex);
  if (!match) {
    // Try multi-line excerpt
    const multiRegex = new RegExp(`\\n\\s{4}${fieldName}:\\n\\s{6}"((?:[^"\\\\]|\\\\.)*)"`, 's');
    const multiMatch = postStr.match(multiRegex);
    return multiMatch ? multiMatch[1] : null;
  }
  return match[1];
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
  const regex = /^#{2,4}\s+(How\s|What\s|Why\s|When\s|Where\s|Can\s|Do\s|Is\s|Are\s)/gim;
  const matches = content.match(regex);
  return matches ? matches : [];
}

function extractInternalLinks(content) {
  const regex = /\(\/(blog|services|locations|industries)\/[^)]+\)/g;
  const matches = content.match(regex);
  return matches ? matches : [];
}

function extractPillarLinks(content) {
  const regex = /\/blog\/complete-seo-guide-bangladesh-businesses-2026/g;
  const matches = content.match(regex);
  return matches ? matches : [];
}

function extractIndustryLinks(content) {
  const indRegex = /\/industries\/[^)]+/g;
  const matches = content.match(indRegex);
  return matches || [];
}

// Industry-specific pillar pages
const industryPillars = {
  'garments-textile': '/industries/garments-textile',
  'medical': '/industries/medical',
  'education': '/industries/education',
  'ecommerce': '/industries/ecommerce',
  'real-estate': '/industries/real-estate',
};

// Main analysis
for (const slug of slugsToAnalyze) {
  console.log(`\n=== POST: ${slug} ===`);
  const postStr = extractPostContent(fileContent, slug);
  if (!postStr) {
    console.log(`ERROR: Could not find`);
    continue;
  }
  
  const title = extractField(postStr, 'title');
  const date = extractField(postStr, 'date');
  const excerpt = extractField(postStr, 'excerpt');
  const dateModified = postStr.includes('dateModified');
  const hasFaqs = postStr.includes('faqs:');
  const content = extractContentField(postStr);
  
  // Tags
  const tagsMatch = postStr.match(/tags:\s*\[([^\]]+)\]/);
  const tags = tagsMatch ? tagsMatch[1].split(',').map(t => t.trim().replace(/"/g, '')) : [];
  
  console.log(`Title: ${title}`);
  console.log(`Date: ${date}`);
  console.log(`Excerpt: ${excerpt ? 'Present' : 'MISSING'}`);
  console.log(`Tags: [${tags.join(', ')}]`);
  console.log(`dateModified: ${dateModified ? 'Present' : 'Missing'}`);
  console.log(`faqs: ${hasFaqs ? 'Present' : 'Missing in metadata'}`);
  
  // A. TF-IDF
  let primaryKeyword = '';
  if (slug === 'geo-optimization-prepare-business-ai-search') primaryKeyword = 'GEO Optimization';
  else if (slug === 'seo-garments-textile-industry-b2b-lead-generation') primaryKeyword = 'Garments and Textile SEO';
  else if (slug === 'mobile-seo-optimization-bangladesh-mobile-first-era') primaryKeyword = 'Mobile SEO';
  else if (slug === 'seo-healthcare-medical-clinics-bangladesh') primaryKeyword = 'Healthcare SEO';
  else if (slug === 'why-md-kanok-miah-is-the-best-seo-expert-in-dhaka-bangladesh') primaryKeyword = 'SEO Expert in Dhaka';
  else if (slug === 'how-to-choose-best-seo-expert-dhaka-15-things') primaryKeyword = 'SEO Expert in Dhaka';
  else if (slug === 'seo-expert-vs-seo-agency-dhaka-which-is-right') primaryKeyword = 'SEO Expert';
  else if (slug === 'top-10-seo-mistakes-dhaka-businesses-fix') primaryKeyword = 'SEO Mistakes';
  else if (slug === 'what-does-seo-expert-do-guide-business-owners') primaryKeyword = 'SEO Expert';
  else if (slug === 'ai-seo-2026-dhaka-experts-optimize-google-ai-chatgpt') primaryKeyword = 'AI SEO';
  
  const kwCount = countOccurrences(content, primaryKeyword);
  const kwFlag = kwCount >= 5 ? 'PASS' : 'FAIL';
  console.log(`TF-IDF: keyword="${primaryKeyword}", count=${kwCount} [${kwFlag}]`);
  
  // B. Entities
  const entityDhaka = countOccurrences(content, 'Dhaka');
  const entityBangladesh = countOccurrences(content, 'Bangladesh');
  
  // Service type based on tags/content
  const serviceTypes = ['SEO', 'Digital Marketing', 'Local SEO', 'Technical SEO', 'On-Page SEO', 'Link Building', 'GEO', 'AI Search', 'Content Marketing'];
  let missingEntities = [];
  if (entityDhaka === 0) missingEntities.push('Dhaka');
  if (entityBangladesh === 0) missingEntities.push('Bangladesh');
  
  // Check if service type is mentioned
  let serviceFound = false;
  let industryFound = false;
  for (const st of serviceTypes) {
    if (content.toLowerCase().includes(st.toLowerCase())) { serviceFound = true; break; }
  }
  if (!serviceFound) missingEntities.push('Service Type');
  
  // Check industry mentions based on tags
  const tagsLower = tags.map(t => t.toLowerCase());
  if (tagsLower.some(t => t.includes('garment') || t.includes('textile'))) {
    if (!content.toLowerCase().includes('garment')) missingEntities.push('Garments/Textile');
  }
  if (tagsLower.some(t => t.includes('health') || t.includes('medical') || t.includes('clinic'))) {
    if (!content.toLowerCase().includes('patient') && !content.toLowerCase().includes('medical') && !content.toLowerCase().includes('clinic')) 
      missingEntities.push('Healthcare/Medical');
  }
  
  console.log(`Entities: Dhaka=${entityDhaka}, Bangladesh=${entityBangladesh}, Service=${serviceFound}`);
  console.log(`Missing: ${missingEntities.length > 0 ? missingEntities.join(', ') : 'None'}`);
  
  // C. Pillar Link
  const pillarLinks = extractPillarLinks(content);
  // Also check for industry pillar links
  const indLinks = extractIndustryLinks(content);
  console.log(`Pillar links: ${pillarLinks.length} (complete-seo-guide)`);
  console.log(`Industry links: ${indLinks.join(', ')}`);
  
  // Determine pillar topic from tags
  let pillarTopic = 'SEO Guide';
  if (tagsLower.some(t => t.includes('garment') || t.includes('textile'))) pillarTopic = 'Garments/Textile SEO';
  else if (tagsLower.some(t => t.includes('health') || t.includes('medical') || t.includes('clinic'))) pillarTopic = 'Healthcare SEO';
  else if (tagsLower.some(t => t.includes('mobile'))) pillarTopic = 'Mobile SEO';
  else if (tagsLower.some(t => t.includes('geo') || t.includes('ai'))) pillarTopic = 'GEO/AI Search';
  else if (tagsLower.some(t => t.includes('mistake'))) pillarTopic = 'SEO Best Practices';
  else if (tagsLower.some(t => t.includes('expert') || t.includes('agency'))) pillarTopic = 'SEO Services';
  console.log(`Pillar topic: ${pillarTopic}`);
  
  // D. AEO/GEO
  const questionHeadings = extractQuestionHeadings(content);
  const qhFlag = questionHeadings.length >= 2 ? 'PASS' : 'FAIL';
  console.log(`AEO/GEO: ${questionHeadings.length} question headings [${qhFlag}]`);
  console.log(`  Questions: ${questionHeadings.join(', ')}`);
  
  // E. Internal Links
  const internalLinks = extractInternalLinks(content);
  const blogLinks = internalLinks.filter(l => l.startsWith('/blog/'));
  const serviceLinks = internalLinks.filter(l => l.startsWith('/services/'));
  const locationLinks = internalLinks.filter(l => l.startsWith('/locations/'));
  const industryLinksIn = internalLinks.filter(l => l.startsWith('/industries/'));
  const ilFlag = internalLinks.length >= 3 ? 'PASS' : 'FAIL';
  console.log(`Internal links: ${internalLinks.length} total [${ilFlag}]`);
  console.log(`  /blog/: ${blogLinks.length}, /services/: ${serviceLinks.length}, /locations/: ${locationLinks.length}, /industries/: ${industryLinksIn.length}`);
  console.log(`  All: ${internalLinks.join(', ')}`);
  
  // F. Schema Ready
  const schemaIssues = [];
  if (!title) schemaIssues.push('title');
  if (!date) schemaIssues.push('date');
  if (!excerpt) schemaIssues.push('excerpt');
  const schemaFlag = schemaIssues.length === 0 ? 'PASS' : 'FAIL';
  console.log(`Schema: ${schemaIssues.length > 0 ? `Missing: ${schemaIssues.join(', ')}` : 'All fields set'} [${schemaFlag}]`);
}
