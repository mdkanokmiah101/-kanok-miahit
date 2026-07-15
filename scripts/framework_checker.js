#!/usr/bin/env node
/**
 * Content Framework Enforcer — kanokmiah.com.bd
 * Checks all modified blog posts against the content framework.
 * Usage: node scripts/framework_checker.js
 */

const fs = require('fs');
const path = require('path');

// Read data.js
const dataPath = path.join(__dirname, '..', 'src/app/blog/data.js');
const raw = fs.readFileSync(dataPath, 'utf8');

// Extract each post object from the array
// We use a regex to match each post block
function extractPost(slug) {
  // Find the post object by slug
  const slugRegex = new RegExp(`slug:\\s*"${slug.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}"`);
  const slugMatch = raw.match(slugRegex);
  if (!slugMatch) return null;
  
  const slugIndex = slugMatch.index;
  
  // Find content field - look for `content: \` ... \``
  const afterSlug = raw.slice(slugIndex);
  
  // Extract title
  const titleMatch = afterSlug.match(/title:\s*"([^"]+)"/);
  const title = titleMatch ? titleMatch[1] : 'Unknown';
  
  // Extract excerpt
  const excerptMatch = afterSlug.match(/excerpt:\s*"([^"]+)"/);
  const excerpt = excerptMatch ? excerptMatch[1] : '';
  
  // Extract date
  const dateMatch = afterSlug.match(/date:\s*"([^"]+)"/);
  const date = dateMatch ? dateMatch[1] : '';
  
  // Extract tags
  const tagsMatch = afterSlug.match(/tags:\s*\[([^\]]+)\]/);
  const tags = tagsMatch 
    ? tagsMatch[1].split(',').map(t => t.trim().replace(/"/g, '').replace(/'/g, ''))
    : [];
  
  // Extract content (template literal)
  const contentMatch = afterSlug.match(/content:\s*`([\s\S]*?)`\s*(?=\n\s*(slug:|title:|date:|author:|excerpt:|tags:|imagePlaceholder:|metaTitle:|metaDescription:|dateModified:|content:|\[))/);
  
  let content = '';
  if (contentMatch) {
    content = contentMatch[1];
  } else {
    // Try alternative: find content between backticks
    const backtickMatch = afterSlug.match(/content:\s*`([\s\S]*?)`\s*(?:\n\s*[,\]])/);
    if (backtickMatch) {
      content = backtickMatch[1];
    }
  }
  
  return { slug, title, excerpt, date, tags, content };
}

// Modified slugs from last 48 hours
const modifiedSlugs = [
  'google-search-console-performance-guide',
  'content-marketing-seo-friendly-content-writing',
  'keyword-research-bangladesh-market',
  'link-building-bangladesh-strategies',
  'ecommerce-seo-daraz-shopify-guide',
  'technical-seo-core-web-vitals-optimization',
  'seo-trends-2026-ai-geo-future',
  'local-seo-dhaka-google-maps-ranking',
  'seo-bangla-beginners-guide-google-ranking',
  'international-seo-bangladesh-exporters-global-buyers',
  'content-marketing-strategy-bangladeshi-brands-seo',
  'mobile-seo-optimization-bangladesh-mobile-first-era',
  'seo-real-estate-developers-dhaka',
  'seo-vs-google-ads-whats-best-bangladesh-businesses',
  'google-business-profile-optimization-guide-bangladesh',
  'seo-garments-textile-industry-b2b-lead-generation',
  'geo-optimization-prepare-business-ai-search',
  'link-building-strategies-bangladesh-market',
  'how-to-choose-right-seo-agency-bangladesh',
  'technical-seo-checklist-bangladeshi-websites',
  'why-ecommerce-store-needs-seo-bangladesh',
  'local-seo-tips-dhaka-businesses-google-maps',
  'complete-seo-guide-bangladesh-businesses-2026'
];

// Also check if there are any new blog posts (from earlier commits)
// Those slugs aren't easily derivable, so let's check if data.js contains them
const newBlogTitles = [
  'AI SEO 2026 Dhaka Experts',
  'SEO Case Study Dhaka',
  'What Does an SEO Expert Do',
  'SEO ROI vs Paid Ads Dhaka',
  'Top 10 SEO Mistakes Dhaka Businesses Make',
  'SEO Expert vs SEO Agency in Dhaka',
  'How to Choose the Best SEO Expert in Dhaka: 15 Things to Check'
];

// Extract primary keyword from title
function extractPrimaryKeyword(title) {
  // Find first meaningful noun phrase
  const cleaned = title.replace(/^(Complete|Ultimate|Best|Top|Essential|Expert|How to|What|Why|When|Where) /i, '');
  const words = cleaned.split(/[\s,:-]+/).filter(w => w.length > 2);
  if (words.length === 0) return cleaned.toLowerCase();
  
  // Try to get a meaningful 2-3 word phrase from the beginning
  const phrase = words.slice(0, Math.min(3, words.length)).join(' ').toLowerCase();
  return phrase;
}

// Count keyword occurrences in content
function countKeyword(content, keyword) {
  if (!content || !keyword) return 0;
  const escaped = keyword.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const regex = new RegExp(escaped, 'gi');
  const matches = content.match(regex);
  return matches ? matches.length : 0;
}

// Count question-based headings
function countQuestionHeadings(content) {
  if (!content) return 0;
  const questionWords = ['How', 'What', 'Why', 'When', 'Where', 'Can', 'Do', 'Is', 'Are', 'Does', 'Which', 'Who'];
  const headingRegex = /^#{1,4}\s+(.*)$/gm;
  let count = 0;
  let match;
  while ((match = headingRegex.exec(content)) !== null) {
    const headingText = match[1].trim();
    if (questionWords.some(qw => headingText.startsWith(qw))) {
      count++;
    }
  }
  return count;
}

// Count internal links (links to /blog/, /services/, /industries/, /locations/, /about, /)
function countInternalLinks(content) {
  if (!content) return 0;
  const internalLinkRegex = /\[([^\]]*)\]\(\/([^)]*)\)/g;
  const links = [];
  let match;
  while ((match = internalLinkRegex.exec(content)) !== null) {
    links.push(match[0]);
  }
  return links.length;
}

// Check for missing entities
function checkMissingEntities(content, tags, title) {
  if (!content) return [];
  const missing = [];
  
  const contentLower = content.toLowerCase();
  
  // Location entities
  const locationEntities = ['dhaka', 'bangladesh', 'bangladeshi'];
  const hasLocation = locationEntities.some(e => contentLower.includes(e));
  if (!hasLocation) missing.push('Bangladesh/Dhaka location reference');
  
  // Check specific location mentions from tags
  if (tags.some(t => t.toLowerCase().includes('dhaka'))) {
    if (!contentLower.includes('dhaka')) missing.push('Dhaka (in tag but missing from content)');
  }
  
  // Service entities
  const serviceKeywords = ['seo', 'search engine optimization', 'search engine', 'ranking', 'organic', 'google'];
  const hasService = serviceKeywords.some(e => contentLower.includes(e));
  if (!hasService) missing.push('Service type (SEO)');
  
  // Industry entities  
  const industryEntities = ['business', 'website', 'online', 'digital'];
  const hasIndustry = industryEntities.some(e => contentLower.includes(e));
  if (!hasIndustry) missing.push('Industry/business context');
  
  // Check for specific entities mentioned in tags
  if (tags.some(t => t.toLowerCase().includes('local'))) {
    if (!contentLower.includes('local seo') && !contentLower.includes('local search')) {
      missing.push('Local SEO mention (tagged as local)');
    }
  }
  if (tags.some(t => t.toLowerCase().includes('ecommerce') || t.toLowerCase().includes('e-commerce'))) {
    if (!contentLower.includes('ecommerce') && !contentLower.includes('e-commerce')) {
      missing.push('E-commerce mention (tagged as ecommerce)');
    }
  }
  if (tags.some(t => t.toLowerCase().includes('technical'))) {
    if (!contentLower.includes('technical seo')) missing.push('Technical SEO mention (tagged as technical)');
  }
  
  return missing;
}

// Check pillar link (should link to a pillar page)
function findPillarLink(content, tags) {
  if (!content) return null;
  
  // The main pillar page is the complete SEO guide
  const pillarPatterns = [
    /\/blog\/complete-seo-guide-bangladesh-businesses-2026/,
    /\/services\//,
    /\/industries\//,
    /\/locations\//
  ];
  
  for (const pattern of pillarPatterns) {
    if (pattern.test(content)) {
      const match = content.match(pattern);
      return match ? match[0] : 'Found pillar/service/location link';
    }
  }
  return null;
}

// Determine pillar topic from tags
function determinePillar(tags) {
  if (!tags || tags.length === 0) return 'Uncategorized';
  
  const tagStr = tags.join(' ').toLowerCase();
  
  if (tagStr.includes('local seo') || tagStr.includes('local search') || tagStr.includes('google maps')) return 'Local SEO';
  if (tagStr.includes('technical') || tagStr.includes('core web vitals') || tagStr.includes('page speed')) return 'Technical SEO';
  if (tagStr.includes('ecommerce') || tagStr.includes('e-commerce') || tagStr.includes('shopify') || tagStr.includes('daraz')) return 'E-commerce SEO';
  if (tagStr.includes('link building') || tagStr.includes('backlink')) return 'Link Building';
  if (tagStr.includes('keyword') || tagStr.includes('keyword research')) return 'Keyword Research';
  if (tagStr.includes('content marketing') || tagStr.includes('content writing')) return 'Content Marketing';
  if (tagStr.includes('geo') || tagStr.includes('generative') || tagStr.includes('ai search')) return 'GEO/AI Search';
  if (tagStr.includes('international') || tagStr.includes('export')) return 'International SEO';
  if (tagStr.includes('mobile')) return 'Mobile SEO';
  if (tagStr.includes('google business') || tagStr.includes('gbp') || tagStr.includes('google my business')) return 'Google Business Profile';
  if (tagStr.includes('seo guide') || tagStr.includes('beginners') || tagStr.includes('bangla')) return 'SEO Basics';
  if (tagStr.includes('real estate')) return 'Real Estate SEO';
  if (tagStr.includes('garment') || tagStr.includes('textile') || tagStr.includes('b2b')) return 'B2B/Industry SEO';
  if (tagStr.includes('seo agency') || tagStr.includes('seo expert')) return 'SEO Agency/Expert';
  if (tagStr.includes('google ads') || tagStr.includes('ppc') || tagStr.includes('paid')) return 'SEO vs PPC';
  if (tagStr.includes('google search console') || tagStr.includes('search console') || tagStr.includes('performance')) return 'SEO Tools';
  
  return 'General SEO';
}

// Run all checks for a post
function runChecks(post) {
  if (!post) return null;
  
  const { slug, title, excerpt, date, tags, content } = post;
  
  if (!content) {
    return {
      slug, title,
      error: 'Could not extract content from data.js'
    };
  }
  
  // A. TF-IDF Coverage
  const keyword = extractPrimaryKeyword(title);
  const keywordCount = countKeyword(content, keyword);
  const tfidfPass = keywordCount >= 5;
  
  // B. Semantic Entity Coverage
  const missingEntities = checkMissingEntities(content, tags, title);
  const entitiesPass = missingEntities.length === 0;
  
  // C. Pillar-Cluster Alignment
  const pillar = determinePillar(tags);
  const pillarLink = findPillarLink(content, tags);
  const pillarPass = pillarLink !== null;
  
  // D. AEO/GEO Optimization
  const questionHeadings = countQuestionHeadings(content);
  const aeoPass = questionHeadings >= 2;
  
  // E. Internal Linking
  const internalLinks = countInternalLinks(content);
  const linkPass = internalLinks >= 3;
  
  // F. Schema Readiness
  const schemaTitle = title && title.length > 0;
  const schemaExcerpt = excerpt && excerpt.length > 0;
  const schemaDate = date && date.length > 0;
  const schemaPass = schemaTitle && schemaExcerpt && schemaDate;
  const schemaMissing = [];
  if (!schemaTitle) schemaMissing.push('title');
  if (!schemaExcerpt) schemaMissing.push('excerpt');
  if (!schemaDate) schemaMissing.push('date');
  
  return {
    slug,
    title,
    pillar,
    checks: {
      tfidf: { pass: tfidfPass, keyword, count: keywordCount },
      entities: { pass: entitiesPass, missing: missingEntities },
      pillarLink: { pass: pillarPass, link: pillarLink || 'None found' },
      aeo: { pass: aeoPass, count: questionHeadings },
      internalLinks: { pass: linkPass, count: internalLinks },
      schema: { pass: schemaPass, missing: schemaMissing }
    }
  };
}

// Generate report
function generateReport(results) {
  let report = '';
  
  for (const result of results) {
    if (!result) continue;
    if (result.error) {
      report += `## Post: ${result.slug}\n❌ ERROR: ${result.error}\n\n`;
      continue;
    }
    
    const c = result.checks;
    
    report += `## Post: ${result.slug}\n`;
    report += `**Title:** ${result.title}\n`;
    report += `**Pillar:** ${result.pillar}\n`;
    report += `\n`;
    report += `| Check | Status | Details |\n`;
    report += `|-------|--------|--------|\n`;
    report += `| TF-IDF: "${c.tfidf.keyword}" | ${c.tfidf.pass ? '✅' : '❌'} | ${c.tfidf.count} occurrences${!c.tfidf.pass ? ` (need ≥5)` : ''} |\n`;
    report += `| Entities | ${c.entities.pass ? '✅' : '❌'} | ${c.entities.pass ? 'All key entities present' : `Missing: ${c.entities.missing.join(', ')}`} |\n`;
    report += `| Pillar Link | ${c.pillarLink.pass ? '✅' : '❌'} | ${c.pillarLink.pass ? `Links to: ${c.pillarLink.link}` : 'No pillar/service/location link found'} |\n`;
    report += `| AEO/GEO | ${c.aeo.pass ? '✅' : '❌'} | ${c.aeo.count} question heading(s)${!c.aeo.pass ? ` (need ≥2)` : ''} |\n`;
    report += `| Internal Links | ${c.internalLinks.pass ? '✅' : '❌'} | ${c.internalLinks.count} total${!c.internalLinks.pass ? ` (need ≥3)` : ''} |\n`;
    report += `| Schema Ready | ${c.schema.pass ? '✅' : '❌'} | ${c.schema.pass ? 'All fields set (title, excerpt, date)' : `Missing: ${c.schema.missing.join(', ')}`} |\n`;
    
    // Fix instructions
    report += `\n### Fix instructions:\n`;
    let hasFixes = false;
    
    if (!c.tfidf.pass) {
      hasFixes = true;
      report += `- **TF-IDF too thin:** Increase "${c.tfidf.keyword}" occurrences to ≥5. Add the keyword naturally in headings, first paragraph, and conclusion.\n`;
    }
    if (!c.entities.pass) {
      hasFixes = true;
      report += `- **Missing entities:** Add references to: ${c.entities.missing.join(', ')}. Ensure location (Dhaka/Bangladesh), service type (SEO), and industry context are mentioned.\n`;
    }
    if (!c.pillarLink.pass) {
      hasFixes = true;
      report += `- **Missing pillar link:** Add a link to the pillar page (complete-seo-guide-bangladesh-businesses-2026, /services/, or /industries/). This ${result.pillar} post should reference its pillar topic.\n`;
    }
    if (!c.aeo.pass) {
      hasFixes = true;
      report += `- **AEO/GEO under-optimized:** Add ${2 - c.aeo.count} more question-based headings (starting with How, What, Why, When, Where, Can, Do, Is, Are) to capture voice/AI search queries.\n`;
    }
    if (!c.internalLinks.pass) {
      hasFixes = true;
      report += `- **Too few internal links:** Add ${3 - c.internalLinks.count} more internal links to related blog posts, services, or location pages.\n`;
    }
    if (!c.schema.pass) {
      hasFixes = true;
      report += `- **Schema fields missing:** Set ${c.schema.missing.join(', ')} in the post metadata for ArticleSchema compatibility.\n`;
    }
    
    if (!hasFixes) {
      report += `All checks passed. No fixes needed.\n`;
    }
    
    report += `\n---\n\n`;
  }
  
  return report;
}

// MAIN
console.log('# Content Framework Enforcement Report\n');
console.log(`Generated: ${new Date().toISOString()}\n`);
console.log(`Posts checked: ${modifiedSlugs.length}\n`);

const results = modifiedSlugs.map(slug => {
  const post = extractPost(slug);
  if (!post) {
    return { slug, title: 'Unknown', error: `Could not find post with slug "${slug}" in data.js` };
  }
  return runChecks(post);
});

const report = generateReport(results);

// Summary stats
const checked = results.filter(r => r && !r.error);
const passed = checked.filter(r => Object.values(r.checks).every(c => c.pass === true));
const failed = checked.filter(r => !Object.values(r.checks).every(c => c.pass === true));

console.log(`## Summary\n`);
console.log(`- ✅ All checks passed: ${passed.length}/${checked.length} posts`);
console.log(`- ❌ Needs fixes: ${failed.length}/${checked.length} posts`);
console.log(`- ❌ Extraction errors: ${results.filter(r => r && r.error).length} posts\n`);

if (failed.length > 0) {
  console.log(`### Posts requiring attention:\n`);
  for (const f of failed) {
    const failingChecks = Object.entries(f.checks)
      .filter(([_, c]) => c.pass === false)
      .map(([name]) => name);
    console.log(`- ${f.slug}: ${failingChecks.join(', ')}`);
  }
  console.log('');
}

console.log(`---\n\n${report}`);
