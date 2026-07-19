#!/usr/bin/env node
/**
 * Content Framework Enforcer — automated checks for kanokmiah.com.bd blog posts.
 * Reads posts from data.js, checks against the content framework, outputs report.
 */
import { readFileSync, writeFileSync } from 'fs';

// ── Config ──────────────────────────────────────────────────────────────────
const DATA_JS = new URL('../src/app/blog/data.js', import.meta.url).pathname;
const SLUGS_FILE = '/tmp/modified_slugs.txt';

// Known pillar page slugs (blog pillar posts and service pages)
const PILLAR_SLUGS = new Set([
  'complete-seo-guide-bangladesh-businesses-2026',
  'local-seo-dhaka-google-maps-ranking',
  'seo-trends-2026-ai-geo-future',
  'technical-seo-core-web-vitals-optimization',
  'seo-bangla-beginners-guide-google-ranking',
  'seo-vs-google-ads-bangladesh-business',
  'seo-for-law-firms-bangladesh',
  'seo-for-startups-bangladesh',
  'seo-for-fitness-gyms-bangladesh',
]);

// Known pillar SERVICE pages
const PILLAR_SERVICES = [
  '/services/',
  '/services/seo',
  '/services/local-seo',
  '/services/ecommerce-seo',
  '/services/technical-seo',
  '/services/content-marketing',
];

// Location pages
const LOCATION_PAGES = [
  '/locations/dhaka',
  '/locations/chittagong',
  '/locations/sylhet',
  '/locations/khulna',
  '/locations/rajshahi',
  '/locations/barisal',
  '/locations/rangpur',
  '/locations/mymensingh',
  '/locations/',
];

// ── Helpers ─────────────────────────────────────────────────────────────────

/** Count occurrences of a substring (case-insensitive) in text */
function countOccurrences(text, keyword) {
  if (!keyword) return 0;
  const escaped = keyword.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const matches = text.match(new RegExp(escaped, 'gi'));
  return matches ? matches.length : 0;
}

/** Count question-based headings (## or ### starting with question words) */
function countQuestionHeadings(content) {
  const qWords = ['How', 'What', 'Why', 'When', 'Where', 'Can', 'Do', 'Is', 'Are', 'Does', 'Which'];
  const pattern = new RegExp(`^#{2,3}\\s+(${qWords.join('|')})\\b`, 'gim');
  const matches = content.match(pattern);
  return matches ? matches.length : 0;
}

/** Count internal links: /blog/, /services/, /locations/, /industries/, /about, /contact, /faq, / */
function countInternalLinks(content) {
  // Internal links are markdown links pointing to paths on the same domain
  const linkPattern = /\[([^\]]*)\]\((\/[^)]*)\)/g;
  const matches = content.matchAll(linkPattern);
  let count = 0;
  for (const m of matches) {
    const url = m[2];
    // Skip external-looking URLs (http://, https://, //)
    if (url.startsWith('//') || url.startsWith('http')) continue;
    // Skip anchor-only links
    if (url === '#' || url.startsWith('#') && !url.startsWith('#/')) continue;
    // Skip mailto:
    if (url.startsWith('mailto:')) continue;
    count++;
  }
  return count;
}

/** Extract primary keyword from title */
function extractPrimaryKeyword(title) {
  if (!title) return null;
  // Remove leading "Complete", "Ultimate", "Expert", "Best", "Top", "Affordable"
  let cleaned = title.replace(/^(Complete|Ultimate|Expert|Best|Top|Affordable|Professional|Comprehensive)\s+/i, '');
  // Take the first noun-phrase-like segment before common stop words
  const stopAt = / (Guide|Tips|Strategies|Checklist|Techniques|Optimization|Benefits|Mistakes|Services|Agency|Company|Expert|Specialist|Consultant|In|For|in Bangladesh|in Dhaka|in 2026|2026)/i;
  const match = cleaned.match(stopAt);
  if (match && match.index > 0) {
    return cleaned.slice(0, match.index).trim();
  }
  // Return first 3-4 words if no stop word found
  return cleaned.split(' ').slice(0, 4).join(' ');
}

/** Check if content links to a known pillar page */
function checkPillarLink(content, slug, tags) {
  // Check for links to pillar blog slugs
  for (const pslug of PILLAR_SLUGS) {
    if (slug === pslug) return { pass: true, detail: `Self (pillar page: ${pslug})` };
    if (content.includes(`/blog/${pslug}`)) {
      return { pass: true, detail: `Links to pillar: ${pslug}` };
    }
  }
  // Check for links to service pages
  for (const svc of PILLAR_SERVICES) {
    if (content.includes(svc)) {
      return { pass: true, detail: `Links to service: ${svc}*` };
    }
  }
  return { pass: false, detail: 'No pillar page or service link found' };
}

/** Determine the pillar topic from tags */
function determinePillarTopic(tags) {
  const tagStr = tags.join(' ').toLowerCase();
  if (tagStr.includes('local') || tagStr.includes('maps') || tagStr.includes('gbp') || tagStr.includes('google business')) return 'Local SEO';
  if (tagStr.includes('technical') || tagStr.includes('core web') || tagStr.includes('crawl') || tagStr.includes('schema') || tagStr.includes('structured data') || tagStr.includes('canonical') || tagStr.includes('robots') || tagStr.includes('sitemap') || tagStr.includes('redirect') || tagStr.includes('https') || tagStr.includes('hreflang')) return 'Technical SEO';
  if (tagStr.includes('trend') || tagStr.includes('2026') || tagStr.includes('future') || tagStr.includes('ai') || tagStr.includes('geo')) return 'SEO Trends & GEO';
  if (tagStr.includes('ecommerce') || tagStr.includes('shopify') || tagStr.includes('daraz')) return 'E-commerce SEO';
  if (tagStr.includes('link building') || tagStr.includes('backlink')) return 'Link Building';
  if (tagStr.includes('keyword') || tagStr.includes('search intent')) return 'Keyword Research';
  if (tagStr.includes('content') || tagStr.includes('blog') || tagStr.includes('writing')) return 'Content Marketing';
  if (tagStr.includes('beginner') || tagStr.includes('guide')) return 'SEO Guide';
  if (tagStr.includes('for ') || tagStr.includes('industry') || tagStr.includes('garment') || tagStr.includes('law') || tagStr.includes('fitness') || tagStr.includes('startup') || tagStr.includes('ngo') || tagStr.includes('real estate') || tagStr.includes('hotel') || tagStr.includes('restaurant') || tagStr.includes('education') || tagStr.includes('healthcare') || tagStr.includes('youtube') || tagStr.includes('podcast') || tagStr.includes('mobile app')) return 'Industry SEO';
  if (tagStr.includes('schema') || tagStr.includes('faq') || tagStr.includes('howto') || tagStr.includes('breadcrumb') || tagStr.includes('json-ld') || tagStr.includes('structured data')) return 'Structured Data';
  if (tagStr.includes('international') || tagStr.includes('hreflang') || tagStr.includes('global')) return 'International SEO';
  return 'General SEO';
}

/** Check entity coverage */
function checkEntityCoverage(content, title, slug, tags) {
  const tagStr = tags.join(' ').toLowerCase();
  const text = content.toLowerCase();
  const missing = [];

  // Location entities
  if (slug.includes('bangladesh') || slug.includes('bd') || tagStr.includes('bangladesh')) {
    if (!text.includes('dhaka')) missing.push('Dhaka');
    if (!text.includes('bangladesh')) missing.push('Bangladesh');
  }
  if (slug.includes('dhaka') || tagStr.includes('dhaka')) {
    if (!text.includes('dhaka')) missing.push('Dhaka');
  }

  // Industry entities
  if (tagStr.includes('garment') || tagStr.includes('textile') || slug.includes('garment')) {
    if (!text.includes('garment') && !text.includes('textile') && !text.includes('rmg')) missing.push('Garments/Textile');
  }
  if (tagStr.includes('law') || tagStr.includes('legal') || slug.includes('law')) {
    if (!text.includes('law') && !text.includes('legal') && !text.includes('attorney') && !text.includes('advocate')) missing.push('Law/Legal');
  }
  if (tagStr.includes('fitness') || tagStr.includes('gym') || slug.includes('fitness')) {
    if (!text.includes('fitness') && !text.includes('gym') && !text.includes('workout')) missing.push('Fitness/Gym');
  }
  if (tagStr.includes('startup') || slug.includes('startup')) {
    if (!text.includes('startup') && !text.includes('start-up')) missing.push('Startup');
  }
  if (tagStr.includes('ecommerce') || tagStr.includes('shopify') || tagStr.includes('daraz') || slug.includes('ecommerce')) {
    if (!text.includes('ecommerce') && !text.includes('e-commerce') && !text.includes('online store') && !text.includes('shop')) missing.push('E-commerce');
  }
  if (tagStr.includes('hotel') || tagStr.includes('resort') || slug.includes('hotel')) {
    if (!text.includes('hotel') && !text.includes('resort') && !text.includes('lodging')) missing.push('Hotel/Resort');
  }
  if (tagStr.includes('real estate') || slug.includes('real-estate')) {
    if (!text.includes('real estate') && !text.includes('property') && !text.includes('apartment')) missing.push('Real Estate');
  }
  if (tagStr.includes('ngo') || slug.includes('ngo')) {
    if (!text.includes('ngo') && !text.includes('non-profit') && !text.includes('nonprofit') && !text.includes('charity')) missing.push('NGO/Non-profit');
  }
  if (tagStr.includes('youtube') || slug.includes('youtube')) {
    if (!text.includes('youtube') && !text.includes('video')) missing.push('YouTube/Video');
  }
  if (tagStr.includes('podcast') || slug.includes('podcast')) {
    if (!text.includes('podcast') && !text.includes('audio')) missing.push('Podcast');
  }
  if (tagStr.includes('mobile app') || slug.includes('mobile-app')) {
    if (!text.includes('app') && !text.includes('mobile')) missing.push('Mobile App');
  }
  if (tagStr.includes('education') || tagStr.includes('educational')) {
    if (!text.includes('education') && !text.includes('student') && !text.includes('university') && !text.includes('college') && !text.includes('school')) missing.push('Education');
  }
  if (tagStr.includes('healthcare') || tagStr.includes('health') || tagStr.includes('medical')) {
    if (!text.includes('health') && !text.includes('medical') && !text.includes('doctor') && !text.includes('hospital') && !text.includes('clinic')) missing.push('Healthcare');
  }
  if (tagStr.includes('restaurant') || tagStr.includes('food')) {
    if (!text.includes('restaurant') && !text.includes('food') && !text.includes('cafe') && !text.includes('dining')) missing.push('Restaurant/Food');
  }

  // Service type entities
  if (tagStr.includes('seo') || slug.includes('seo')) {
    if (!text.includes('seo') && !text.includes('search engine optimization') && !text.includes('search engine optimisation')) missing.push('SEO');
  }
  if (tagStr.includes('local') || slug.includes('local')) {
    if (!text.includes('local seo') && !text.includes('local search')) missing.push('Local SEO');
  }
  if (tagStr.includes('content') || tagStr.includes('content marketing')) {
    if (!text.includes('content') && !text.includes('blog') && !text.includes('article')) missing.push('Content');
  }
  if (tagStr.includes('schema') || tagStr.includes('structured data')) {
    if (!text.includes('schema') && !text.includes('structured data') && !text.includes('rich snippet')) missing.push('Schema/Structured Data');
  }
  if (tagStr.includes('link building') || tagStr.includes('backlink')) {
    if (!text.includes('link') && !text.includes('backlink') && !text.includes('anchor text')) missing.push('Link Building');
  }
  if (tagStr.includes('technical') || slug.includes('technical') || slug.includes('core-web') || slug.includes('page-speed') || slug.includes('crawl')) {
    if (!text.includes('technical') && !text.includes('crawl') && !text.includes('index') && !text.includes('page speed') && !text.includes('core web')) missing.push('Technical SEO');
  }

  if (missing.length === 0) return { pass: true, detail: 'All expected entities found' };
  return { pass: false, detail: `Missing: ${missing.join(', ')}` };
}

// ── Main ────────────────────────────────────────────────────────────────────

async function main() {
  // Load posts
  const posts = (await import(DATA_JS)).default;

  // Load modified slugs
  const modifiedSlugs = readFileSync(SLUGS_FILE, 'utf-8')
    .split('\n')
    .map(s => s.trim())
    .filter(Boolean);

  console.log(`Loaded ${posts.length} total posts, ${modifiedSlugs.length} modified slugs\n`);

  const reportParts = [];
  let totalPass = 0;
  let totalFail = 0;
  let totalChecks = 0;
  let postsWithIssues = 0;
  let postsClean = 0;

  for (const slug of modifiedSlugs) {
    const post = posts.find(p => p.slug === slug);
    if (!post) {
      reportParts.push(`## Post: ${slug}\n⚠️ Post not found in data.js (slug mismatch)\n`);
      continue;
    }

    const { title, excerpt, date, tags = [], content = '' } = post;
    const keyword = extractPrimaryKeyword(title);
    const occurrences = countOccurrences(content, keyword);
    const questionHeadings = countQuestionHeadings(content);
    const internalLinks = countInternalLinks(content);

    // ── A. TF-IDF Coverage ──────────────────────────────────────────────
    const tfidfPass = occurrences >= 5;
    if (!tfidfPass) totalFail++; else totalPass++;
    totalChecks++;

    // ── B. Entity Coverage ──────────────────────────────────────────────
    const entityCheck = checkEntityCoverage(content, title, slug, tags);
    if (!entityCheck.pass) totalFail++; else totalPass++;
    totalChecks++;

    // ── C. Pillar-Cluster Alignment ─────────────────────────────────────
    const pillarCheck = checkPillarLink(content, slug, tags);
    const pillarTopic = determinePillarTopic(tags);
    if (!pillarCheck.pass) totalFail++; else totalPass++;
    totalChecks++;

    // ── D. AEO/GEO Optimization ─────────────────────────────────────────
    const aeoPass = questionHeadings >= 2;
    if (!aeoPass) totalFail++; else totalPass++;
    totalChecks++;

    // ── E. Internal Linking ─────────────────────────────────────────────
    const linkingPass = internalLinks >= 3;
    if (!linkingPass) totalFail++; else totalPass++;
    totalChecks++;

    // ── F. Schema Ready ─────────────────────────────────────────────────
    const schemaFields = { title: !!title, excerpt: !!excerpt, date: !!date };
    const missingFields = [];
    if (!schemaFields.title) missingFields.push('title');
    if (!schemaFields.excerpt) missingFields.push('excerpt');
    if (!schemaFields.date) missingFields.push('date');
    const schemaPass = missingFields.length === 0;
    if (!schemaPass) totalFail++; else totalPass++;
    totalChecks++;

    // ── Build report ────────────────────────────────────────────────────
    const hasIssues = !tfidfPass || !entityCheck.pass || !pillarCheck.pass || !aeoPass || !linkingPass || !schemaPass;
    if (hasIssues) postsWithIssues++; else postsClean++;

    const fixInstructions = [];

    if (!tfidfPass) {
      fixInstructions.push(`- **TF-IDF**: Add more "${keyword}" occurrences (currently ${occurrences}, need ≥5). Incorporate naturally in headings, body text, and examples.`);
    }

    if (!entityCheck.pass) {
      fixInstructions.push(`- **Entities**: Add missing entities: ${entityCheck.detail.replace('Missing: ', '')}. Mention each entity at least once in the content.`);
    }

    if (!pillarCheck.pass) {
      fixInstructions.push(`- **Pillar Link**: Add a link to the pillar page for "${pillarTopic}". Consider linking to the relevant `/services/` or `/blog/` pillar page.`);
    }

    if (!aeoPass) {
      fixInstructions.push(`- **AEO/GEO**: Add more question-based headings (currently ${questionHeadings}, need ≥2). Use "How", "What", "Why", etc.`);
    }

    if (!linkingPass) {
      fixInstructions.push(`- **Internal Links**: Add more internal links (currently ${internalLinks}, need ≥3). Link to other blog posts, service pages, or location pages.`);
    }

    if (!schemaPass) {
      fixInstructions.push(`- **Schema**: Missing fields: ${missingFields.join(', ')}. Ensure title, excerpt, and date are set for ArticleSchema.`);
    }

    reportParts.push(`## Post: ${slug}
| Check | Status | Details |
|-------|--------|---------|
| TF-IDF: \`${keyword}\` | ${tfidfPass ? '✅' : '❌'} | ${occurrences} occurrences |
| Entities | ${entityCheck.pass ? '✅' : '❌'} | ${entityCheck.detail} |
| Pillar Link | ${pillarCheck.pass ? '✅' : '❌'} | Pillar topic: ${pillarTopic}. ${pillarCheck.detail} |
| AEO/GEO | ${aeoPass ? '✅' : '❌'} | ${questionHeadings} question headings |
| Internal Links | ${linkingPass ? '✅' : '❌'} | ${internalLinks} total |
| Schema Ready | ${schemaPass ? '✅' : '❌'} | ${missingFields.length ? `Missing: ${missingFields.join(', ')}` : 'All fields set'} |

### ${hasIssues ? `⚠️ Fix instructions:` : '✅ All checks passed'}
${fixInstructions.length ? fixInstructions.join('\n') : 'No fixes needed — post meets all framework requirements.'}
`);
  }

  // ── Summary ───────────────────────────────────────────────────────────
  const summary = `# Content Framework Report — ${new Date().toISOString().slice(0, 10)}

**Period**: Last 48 hours
**Posts checked**: ${modifiedSlugs.length}
**Posts with issues**: ${postsWithIssues}
**Posts clean**: ${postsClean}
**Checks passed**: ${totalPass}/${totalChecks} (${Math.round(totalPass/totalChecks*100)}%)
**Failing checks**: ${totalFail}

---

${reportParts.join('\n\n')}
`;

  // Write report file
  const reportPath = '/tmp/framework-report.md';
  writeFileSync(reportPath, summary, 'utf-8');
  console.log(`Report written to ${reportPath}`);
  console.log(summary);
}

main().catch(err => {
  console.error('Fatal:', err);
  process.exit(1);
});
