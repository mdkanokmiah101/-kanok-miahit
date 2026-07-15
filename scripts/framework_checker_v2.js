#!/usr/bin/env node
/**
 * Content Framework Enforcer — kanokmiah.com.bd
 * Uses module loading to get posts from data.js
 */

const path = require('path');

// Load posts from data.js
const dataPath = path.resolve(__dirname, '..', 'src/app/blog/data.js');
const { posts } = require(dataPath);

// Modified slugs from last 48 hours
const modifiedSlugs = new Set([
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
]);

// Get modified posts
const modifiedPosts = posts.filter(p => modifiedSlugs.has(p.slug));

console.log(`Found ${modifiedPosts.length} modified posts out of ${posts.length} total.\n`);

// Extract primary keyword from title
function extractPrimaryKeyword(title) {
  const cleaned = title.replace(/^(Complete |Ultimate |Best |Top |Essential |Expert |How to |What |Why |When |Where |) /i, '');
  const words = cleaned.split(/[\s,:-]+/).filter(w => w.length > 2);
  if (words.length === 0) return cleaned.toLowerCase();
  const phrase = words.slice(0, Math.min(3, words.length)).join(' ');
  return phrase;
}

// Count keyword occurrences in content
function countKeyword(content, keyword) {
  if (!content || !keyword) return 0;
  const escaped = keyword.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const regex = new RegExp('\\b' + escaped.replace(/\s+/g, '\\s+') + '\\b', 'gi');
  const matches = content.match(regex);
  return matches ? matches.length : 0;
}

// Count question-based headings
function countQuestionHeadings(content) {
  if (!content) return 0;
  const questionWords = ['How', 'What', 'Why', 'When', 'Where', 'Can', 'Do', 'Is', 'Are', 'Does', 'Which', 'Who'];
  const lines = content.split('\n');
  let count = 0;
  for (const line of lines) {
    if (line.match(/^#{1,4}\s+/)) {
      const headingText = line.replace(/^#+\s*/, '').trim();
      if (questionWords.some(qw => headingText.startsWith(qw))) {
        count++;
      }
    }
  }
  return count;
}

// Count internal links (links to /blog/, /services/, /industries/, /locations/, /about, /)
function countInternalLinks(content) {
  if (!content) return 0;
  const linkRegex = /\[([^\]]*)\]\(\/([^)]*)\)/g;
  let count = 0;
  let match;
  while ((match = linkRegex.exec(content)) !== null) {
    count++;
  }
  return count;
}

// Check for missing entities
function checkMissingEntities(content, tags) {
  if (!content) return [];
  const missing = [];
  const c = content.toLowerCase();
  
  // Location entities
  if (!c.includes('dhaka') && !c.includes('bangladesh')) {
    missing.push('Location reference (Dhaka/Bangladesh)');
  }
  
  // Service entity
  if (!c.includes('seo') && !c.includes('search engine optimization')) {
    missing.push('SEO/service type reference');
  }
  
  // Check tag-specific entities
  const tagStr = tags.join(' ').toLowerCase();
  
  if (tagStr.includes('local') && !c.includes('local seo') && !c.includes('local search')) {
    missing.push('Local SEO mention (tagged as local)');
  }
  if ((tagStr.includes('ecommerce') || tagStr.includes('e-commerce')) && !c.includes('ecommerce') && !c.includes('e-commerce')) {
    missing.push('E-commerce mention (tagged as e-commerce)');
  }
  if (tagStr.includes('technical') && !c.includes('technical seo')) {
    missing.push('Technical SEO mention (tagged as technical)');
  }
  if (tagStr.includes('keyword') && !c.includes('keyword')) {
    missing.push('Keyword research mention (tagged as keyword)');
  }
  if (tagStr.includes('link building') && !c.includes('link building') && !c.includes('backlink')) {
    missing.push('Link building mention (tagged as link building)');
  }
  if (tagStr.includes('content') && !c.includes('content marketing') && !c.includes('content writing')) {
    missing.push('Content marketing mention (tagged as content)');
  }
  if ((tagStr.includes('geo') || tagStr.includes('generative')) && !c.includes('geo') && !c.includes('generative engine')) {
    missing.push('GEO mention (tagged as GEO/AI)');
  }
  if (tagStr.includes('mobile') && !c.includes('mobile seo') && !c.includes('mobile optimization')) {
    missing.push('Mobile SEO mention (tagged as mobile)');
  }
  if ((tagStr.includes('google business') || tagStr.includes('gbp')) && !c.includes('google business profile') && !c.includes('gbp')) {
    missing.push('GBP mention (tagged as Google Business)');
  }
  
  return missing;
}

// Find pillar link
function findPillarLink(content) {
  if (!content) return null;
  
  const pillarPatterns = [
    /\/blog\/complete-seo-guide-bangladesh-businesses-2026/,
    /\/services\//,
    /\/industries\//
  ];
  
  for (const pattern of pillarPatterns) {
    const match = content.match(pattern);
    if (match) return match[0];
  }
  return null;
}

// Determine pillar from tags
function determinePillar(tags) {
  const t = tags.join(' ').toLowerCase();
  if (t.includes('local seo') || t.includes('local search') || t.includes('google maps')) return 'Local SEO';
  if (t.includes('technical') || t.includes('core web vitals') || t.includes('page speed')) return 'Technical SEO';
  if (t.includes('ecommerce') || t.includes('e-commerce') || t.includes('shopify') || t.includes('daraz')) return 'E-commerce SEO';
  if (t.includes('link building') || t.includes('backlink')) return 'Link Building';
  if (t.includes('keyword') || t.includes('keyword research')) return 'Keyword Research';
  if (t.includes('content marketing') || t.includes('content writing') || t.includes('content strategy')) return 'Content Marketing';
  if (t.includes('geo') || t.includes('generative') || t.includes('ai search')) return 'GEO/AI Search';
  if (t.includes('international') || t.includes('export')) return 'International SEO';
  if (t.includes('mobile')) return 'Mobile SEO';
  if (t.includes('google business') || t.includes('gbp') || t.includes('google my business')) return 'Google Business Profile';
  if (t.includes('seo guide') || t.includes('beginners') || t.includes('bangla')) return 'SEO Basics';
  if (t.includes('real estate')) return 'Real Estate SEO';
  if (t.includes('garment') || t.includes('textile') || t.includes('b2b')) return 'B2B/Industry SEO';
  if (t.includes('seo agency') || t.includes('seo expert')) return 'SEO Agency/Expert';
  if (t.includes('google ads') || t.includes('ppc') || t.includes('paid')) return 'SEO vs PPC';
  if (t.includes('google search console') || t.includes('search console') || t.includes('performance')) return 'SEO Tools';
  return 'General SEO';
}

// Run checks for a post
function runChecks(post) {
  const { slug, title, excerpt, date, tags, content } = post;
  
  // A. TF-IDF Coverage
  const keyword = extractPrimaryKeyword(title);
  const keywordCount = countKeyword(content, keyword);
  
  // B. Semantic Entity Coverage
  const missing = checkMissingEntities(content, tags);
  
  // C. Pillar-Cluster Alignment
  const pillar = determinePillar(tags);
  const pillarLink = findPillarLink(content);
  
  // D. AEO/GEO Optimization
  const questionHeadings = countQuestionHeadings(content);
  
  // E. Internal Linking
  const internalLinks = countInternalLinks(content);
  
  // F. Schema Readiness
  const schemaFields = { title: !!title, excerpt: !!excerpt, date: !!date };
  const schemaMissing = Object.entries(schemaFields).filter(([_, v]) => !v).map(([k]) => k);
  
  return {
    slug, title, pillar,
    checks: {
      tfidf: { pass: keywordCount >= 5, keyword, count: keywordCount },
      entities: { pass: missing.length === 0, missing },
      pillarLink: { pass: pillarLink !== null, link: pillarLink || 'None' },
      aeo: { pass: questionHeadings >= 2, count: questionHeadings },
      internalLinks: { pass: internalLinks >= 3, count: internalLinks },
      schema: { pass: schemaMissing.length === 0, missing: schemaMissing }
    }
  };
}

// Run all checks
const results = modifiedPosts.map(runChecks);

// Generate report
let allPassed = 0, allFailed = 0;

for (const r of results) {
  const c = r.checks;
  const checksAllPass = Object.values(c).every(ch => ch.pass === true);
  if (checksAllPass) allPassed++; else allFailed++;
  
  console.log(`## Post: ${r.slug}`);
  console.log(`**Title:** ${r.title}`);
  console.log(`**Pillar:** ${r.pillar}`);
  console.log('');
  console.log(`| Check | Status | Details |`);
  console.log(`|-------|--------|--------|`);
  console.log(`| TF-IDF: "${c.tfidf.keyword}" | ${c.tfidf.pass ? '✅' : '❌'} | ${c.tfidf.count} occurrences${!c.tfidf.pass ? ` (need ≥5)` : ''} |`);
  console.log(`| Entities | ${c.entities.pass ? '✅' : '❌'} | ${c.entities.pass ? 'All key entities present' : `Missing: ${c.entities.missing.join(', ')}`} |`);
  console.log(`| Pillar Link | ${c.pillarLink.pass ? '✅' : '❌'} | ${c.pillarLink.pass ? `Links to: ${c.pillarLink.link}` : 'No pillar/service/location link found'} |`);
  console.log(`| AEO/GEO | ${c.aeo.pass ? '✅' : '❌'} | ${c.aeo.count} question heading(s)${!c.aeo.pass ? ` (need ≥2)` : ''} |`);
  console.log(`| Internal Links | ${c.internalLinks.pass ? '✅' : '❌'} | ${c.internalLinks.count} total${!c.internalLinks.pass ? ` (need ≥3)` : ''} |`);
  console.log(`| Schema Ready | ${c.schema.pass ? '✅' : '❌'} | ${c.schema.pass ? 'All fields set (title, excerpt, date)' : `Missing: ${c.schema.missing.join(', ')}`} |`);
  
  console.log('');
  console.log('### Fix instructions:');
  let hasFixes = false;
  
  if (!c.tfidf.pass) {
    hasFixes = true;
    console.log(`- **TF-IDF too thin:** Increase "${c.tfidf.keyword}" occurrences to ≥5. Add the keyword naturally in headings, first paragraph, and conclusion.`);
  }
  if (!c.entities.pass) {
    hasFixes = true;
    console.log(`- **Missing entities:** Add references to: ${c.entities.missing.join(', ')}.`);
  }
  if (!c.pillarLink.pass) {
    hasFixes = true;
    console.log(`- **Missing pillar link:** Add a link to the pillar page (complete-seo-guide, /services/, or /industries/). This "${r.pillar}" post should reference its pillar topic.`);
  }
  if (!c.aeo.pass) {
    hasFixes = true;
    console.log(`- **AEO/GEO under-optimized:** Add ${2 - c.aeo.count} more question-based headings (starting with How/What/Why/When/Where/Can/Do/Is/Are).`);
  }
  if (!c.internalLinks.pass) {
    hasFixes = true;
    console.log(`- **Too few internal links:** Add ${3 - c.internalLinks.count} more internal links to related blog posts, services, or location pages.`);
  }
  if (!c.schema.pass) {
    hasFixes = true;
    console.log(`- **Schema fields missing:** Set ${c.schema.missing.join(', ')} in the post metadata.`);
  }
  
  if (!hasFixes) {
    console.log('All checks passed. No fixes needed.');
  }
  
  console.log('');
  console.log('---');
  console.log('');
}

console.log('## Summary');
console.log(`- ✅ All checks passed: **${allPassed}/${results.length}** posts`);
console.log(`- ❌ Needs fixes: **${allFailed}/${results.length}** posts`);
console.log(`- Total modified posts checked: ${results.length}`);
