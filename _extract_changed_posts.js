const fs = require('fs');
const data = fs.readFileSync('src/app/blog/data.js', 'utf8');

const slugs = [
  "geo-optimization-prepare-business-ai-search",
  "seo-garments-textile-industry-b2b-lead-generation",
  "mobile-seo-optimization-bangladesh-mobile-first-era",
  "seo-healthcare-medical-clinics-bangladesh",
  "why-md-kanok-miah-is-the-best-seo-expert-in-dhaka-bangladesh",
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
  "ai-seo-2026-dhaka-experts-optimize-google-ai-chatgpt"
];

// First, get all slug line numbers
const lines = data.split('\n');
const slugLines = [];
for (let i = 0; i < lines.length; i++) {
  const match = lines[i].match(/^\s+slug:\s*"([^"]+)"/);
  if (match && slugs.includes(match[1])) {
    slugLines.push({ slug: match[1], lineNum: i + 1 });
  }
}

// Extract each post
for (const sl of slugLines) {
  // Find where this post object ends - next top-level }, or end of array
  let braceCount = 0;
  let started = false;
  let endLine = sl.lineNum;
  
  for (let i = sl.lineNum - 1; i < lines.length; i++) {
    const line = lines[i];
    if (!started) {
      if (line.includes('{')) { started = true; braceCount++; }
      continue;
    }
    for (const ch of line) {
      if (ch === '{') braceCount++;
      if (ch === '}') braceCount--;
    }
    if (braceCount === 0) {
      endLine = i + 1;
      break;
    }
    endLine = i + 1;
  }
  
  // Read the post content
  const postLines = lines.slice(sl.lineNum - 2, endLine);
  const postText = postLines.join('\n');
  
  // Extract fields
  const titleMatch = postText.match(/title:\s*"([^"]+)"/);
  const dateMatch = postText.match(/date:\s*"([^"]+)"/);
  const excerptMatch = postText.match(/excerpt:\s*([\s\S]*?)(?=\n\s+(tags|imagePlaceholder|metaTitle|content):)/);
  const tagsMatch = postText.match(/tags:\s*\[([^\]]+)\]/);
  const contentMatch = postText.match(/content:\s*`([\s\S]*)`\s*,?\s*$/);
  
  const title = titleMatch ? titleMatch[1] : 'N/A';
  const date = dateMatch ? dateMatch[1] : 'N/A';
  const excerpt = excerptMatch ? excerptMatch[1].trim().replace(/^"|"$/g, '') : 'N/A';
  const tags = tagsMatch ? tagsMatch[1].split(',').map(t => t.trim().replace(/"/g, '')) : [];
  const content = contentMatch ? contentMatch[1].trim() : 'N/A';
  
  console.log(`=== POST: ${sl.slug} ===`);
  console.log(`TITLE: ${title}`);
  console.log(`DATE: ${date}`);
  console.log(`TAGS: ${tags.join(', ')}`);
  console.log(`EXCERPT: ${excerpt}`);
  console.log(`CONTENT_LENGTH: ${content.length} chars`);
  
  // Extract primary keyword from title
  const words = title.replace(/[^\w\s]/g, '').split(' ');
  // Find first meaningful noun phrase (skip generic words)
  const stopwords = ['a', 'an', 'the', 'in', 'of', 'for', 'to', 'and', 'is', 'are', 'at', 'on', 'with', 'from', 'by', 'your', 'our', 'its', 'that', 'this', 'these', 'those', 'what', 'why', 'how', 'when', 'where', 'which', 'who', 'can', 'do', 'does', 'will', 'has', 'have', 'been', 'being'];
  let keyword = '';
  let found = false;
  for (let i = 0; i < words.length; i++) {
    if (!found && !stopwords.includes(words[i].toLowerCase()) && words[i].length > 2) {
      // Start collecting noun phrase
      let phrase = words[i];
      for (let j = i + 1; j < Math.min(i + 4, words.length); j++) {
        if (stopwords.includes(words[j].toLowerCase()) && words[j].toLowerCase() !== 'seo') break;
        phrase += ' ' + words[j];
      }
      keyword = phrase;
      found = true;
      break;
    }
  }
  
  // Count keyword occurrences in content (case insensitive)
  const contentLower = content.toLowerCase();
  const keywordLower = keyword.toLowerCase();
  let count = 0;
  let pos = 0;
  while ((pos = contentLower.indexOf(keywordLower, pos)) !== -1) {
    count++;
    pos += keywordLower.length;
  }
  
  console.log(`KEYWORD: "${keyword}" (${count} occurrences)`);
  
  // Count question headings (## or ### that start with question words)
  const qHeadings = content.match(/^#{2,3}\s+(How|What|Why|When|Where|Can|Do|Is|Are|Does|Which|Who)\b/gim);
  const qCount = qHeadings ? qHeadings.length : 0;
  console.log(`QUESTION HEADINGS: ${qCount}`);
  
  // Count internal links (links to /blog/, /services/, /locations/, /industries/)
  const internalLinks = content.match(/\/(?:blog|services|locations|industries|about)\/[^\s)]+/g);
  const internalCount = internalLinks ? internalLinks.length : 0;
  console.log(`INTERNAL LINKS: ${internalCount}`);
  if (internalLinks) {
    console.log(`INTERNAL LINK TARGETS: ${internalLinks.join(', ')}`);
  }
  
  // Check for pillar-related links
  const homeLinks = content.match(/\]\(\/\//g) || content.match(/\]\(\//g);
  const pillarLinks = [];
  // Find any links that might be pillar pages
  const allLinks = content.matchAll(/\[([^\]]+)\]\(([^)]+)\)/g);
  for (const link of allLinks) {
    const href = link[2];
    if (href.includes('/blog/complete-seo-guide-bangladesh-businesses-2026') || 
        href === '/' || 
        href.startsWith('/#')) {
      pillarLinks.push(href);
    }
  }
  console.log(`PILLAR LINKS: ${pillarLinks.join(', ') || 'none'}`);
  
  // Check entities needed
  const needsLocationDhaka = contentLower.includes('dhaka');
  const needsLocationBangladesh = contentLower.includes('bangladesh');
  const needsServiceSEO = contentLower.includes('seo') || keywordLower.includes('seo');
  console.log(`ENTITIES - Dhaka: ${needsLocationDhaka}, Bangladesh: ${needsLocationBangladesh}`);
  
  // Schema check
  console.log(`SCHEMA - Title: ${title !== 'N/A'}, Date: ${date !== 'N/A'}, Excerpt: ${excerpt !== 'N/A'}`);
  
  console.log(`\n---END ${sl.slug}---\n`);
}
