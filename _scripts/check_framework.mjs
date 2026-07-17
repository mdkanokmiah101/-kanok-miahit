/**
 * Content Framework Enforcer — runs all checks on modified blog posts.
 */
import { readFileSync, existsSync } from 'fs';

// ── Load data.js ────────────────────────────────────────────────────────────
const dataPath = new URL('../src/app/blog/data.js', import.meta.url).pathname;
const raw = readFileSync(dataPath, 'utf-8');

// Extract all post objects via a simple regex-based parse (the file is an array literal)
// We'll evaluate the JS directly using dynamic import of a temp file approach.
// Actually, let's use a safer eval approach.
import { writeFileSync, unlinkSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __dirname = dirname(fileURLToPath(import.meta.url));

// Write a small wrapper that exports the array
const wrapperPath = join(__dirname, '___data_wrapper.mjs');
const wrapperContent = raw.replace('const posts = [', 'const posts = [\n');
writeFileSync(wrapperPath, wrapperContent + '\nexport { posts };\n');

let posts;
try {
  const mod = await import(/* fileURL */ `file://${wrapperPath}`);
  posts = mod.posts;
} catch (e) {
  console.error('Failed to parse data.js:', e.message);
  process.exit(1);
}

// Cleanup
try { unlinkSync(wrapperPath); } catch {}

// ── Modified slugs (from git log) ───────────────────────────────────────────
const modifiedSlugs = new Set([
  "seo-for-facebook-marketplace",
  "long-tail-keywords-bangladesh",
  "seo-tips-for-business-owners-bd",
  "seo-bangla-blog-content-writing",
  "seo-vs-google-ads-bangladesh-business",
  "youtube-seo-bangladesh-ranking-tips",
  "schema-markup-rich-snippets-techniques",
  "mobile-seo-bangladesh-ranking-strategy",
  "google-search-console-performance-guide",
  "content-marketing-seo-friendly-content-writing",
  "keyword-research-bangladesh-market",
  "link-building-bangladesh-strategies",
  "ecommerce-seo-daraz-shopify-guide",
  "technical-seo-core-web-vitals-optimization",
  "seo-trends-2026-ai-geo-future",
  "local-seo-dhaka-google-maps-ranking",
  "seo-bangla-beginners-guide-google-ranking",
  "international-seo-bangladesh-exporters-global-buyers",
  "content-marketing-strategy-bangladeshi-brands-seo",
  "mobile-seo-optimization-bangladesh-mobile-first-era",
  "seo-real-estate-developers-dhaka",
  "seo-vs-google-ads-whats-best-bangladesh-businesses",
  "google-business-profile-optimization-guide-bangladesh",
  "seo-garments-textile-industry-b2b-lead-generation",
  "geo-optimization-prepare-business-ai-search",
  "link-building-strategies-bangladesh-market",
  "how-to-choose-right-seo-agency-bangladesh",
  "technical-seo-checklist-bangladeshi-websites",
  "why-ecommerce-store-needs-seo-bangladesh",
  "local-seo-tips-dhaka-businesses-google-maps",
  "complete-seo-guide-bangladesh-businesses-2026",
  "seo-expert-vs-seo-agency-dhaka",
  "top-10-seo-mistakes-dhaka-businesses-make",
  "what-does-an-seo-expert-do",
  "ai-seo-2026-dhaka-experts",
  "seo-case-study-dhaka",
  "seo-roi-vs-paid-ads-dhaka",
  "how-to-choose-best-seo-expert-dhaka"
]);

// ── Helper functions ────────────────────────────────────────────────────────

function extractKeyword(title) {
  // Extract first meaningful noun phrase from title
  // Strip common prefixes
  let t = title.replace(/^(Complete|Ultimate|The |How to|Why|What|When|Where|Essential|Top \d+ )/i, '');
  // Take first 2-3 words
  const words = t.split(/[\s,—–-]+/).filter(w => w.length > 2).slice(0, 4);
  return words.join(' ').toLowerCase();
}

function countOccurrences(text, keyword) {
  if (!keyword || keyword.length < 3) return 999; // skip if not meaningful
  const words = keyword.toLowerCase().split(/\s+/);
  let count = 0;
  const lowerText = text.toLowerCase();
  // Count the full phrase
  const regex = new RegExp(keyword.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi');
  const matches = lowerText.match(regex);
  return matches ? matches.length : 0;
}

function countQuestionHeadings(content) {
  // Count headings (## or ###) that start with question words
  const qWords = ['How', 'What', 'Why', 'When', 'Where', 'Can', 'Do', 'Is', 'Are', 'Does', 'Which', 'Who'];
  const headingLines = content.match(/^#{2,3}\s+.*$/gm) || [];
  return headingLines.filter(h => {
    const cleanH = h.replace(/^#+\s*/, '');
    return qWords.some(q => cleanH.startsWith(q));
  }).length;
}

function countInternalLinks(content) {
  // Count markdown links starting with /
  const links = content.match(/\[([^\]]*)\]\((\/[^)]*)\)/g) || [];
  return links.length;
}

function findPillarLink(content, tags) {
  // Check if post links to a pillar page based on tags
  const tagStr = (tags || []).join(' ').toLowerCase();
  const contentStr = content.toLowerCase();
  
  // Map of tag-based pillar pages
  const pillarMap = [
    { tags: ['seo', 'seo guide', 'bangladesh seo', 'seo strategy'], pillar: '/blog/complete-seo-guide-bangladesh-businesses-2026', name: 'Complete SEO Guide' },
    { tags: ['local seo', 'google maps'], pillar: '/blog/local-seo-tips-dhaka-businesses-google-maps', name: 'Local SEO Dhaka guide' },
    { tags: ['ecommerce', 'daraz', 'shopify'], pillar: '/industries/ecommerce', name: 'E-commerce industry page' },
    { tags: ['technical seo', 'core web vitals', 'page speed'], pillar: '/blog/technical-seo-checklist-bangladeshi-websites', name: 'Technical SEO checklist' },
    { tags: ['link building'], pillar: '/blog/link-building-bangladesh-strategies', name: 'Link building guide' },
    { tags: ['keyword research', 'keywords'], pillar: '/blog/keyword-research-bangladesh-market', name: 'Keyword research guide' },
    { tags: ['content marketing'], pillar: '/industries/digital-marketing', name: 'Digital Marketing page' },
    { tags: ['geo', 'ai search', 'generative ai'], pillar: '/blog/geo-optimization-prepare-business-ai-search', name: 'GEO guide' },
    { tags: ['mobile seo', 'mobile'], pillar: '/blog/mobile-seo-optimization-bangladesh-mobile-first-era', name: 'Mobile SEO guide' },
    { tags: ['real estate', 'property'], pillar: '/industries/real-estate', name: 'Real estate industry page' },
    { tags: ['google ads', 'ppc', 'paid ads'], pillar: '/blog/seo-vs-google-ads-whats-best-bangladesh-businesses', name: 'SEO vs Google Ads guide' },
    { tags: ['google business profile', 'gbp'], pillar: '/blog/google-business-profile-optimization-guide-bangladesh', name: 'GBP guide' },
    { tags: ['garments', 'textile', 'b2b', 'manufacturing'], pillar: '/industries/manufacturing', name: 'Manufacturing page' },
    { tags: ['international seo', 'global', 'export'], pillar: '/blog/international-seo-bangladesh-exporters-global-buyers', name: 'International SEO guide' },
    { tags: ['beginners', 'beginner guide'], pillar: '/blog/seo-bangla-beginners-guide-google-ranking', name: 'SEO beginners guide' },
    { tags: ['schema', 'structured data', 'rich snippets'], pillar: '/blog/schema-markup-rich-snippets-techniques', name: 'Schema markup guide' },
    { tags: ['youtube', 'video seo'], pillar: '/blog/youtube-seo-bangladesh-ranking-tips', name: 'YouTube SEO guide' },
    { tags: ['google search console', 'gsc'], pillar: '/blog/google-search-console-performance-guide', name: 'Google Search Console guide' },
    { tags: ['seo agency', 'seo expert', 'agency'], pillar: '/blog/how-to-choose-right-seo-agency-bangladesh', name: 'Choose SEO agency guide' },
    { tags: ['facebook', 'social media', 'marketplace'], pillar: '/industries/ecommerce', name: 'E-commerce page' },
  ];
  
  for (const mapping of pillarMap) {
    const hasTag = mapping.tags.some(t => tagStr.includes(t));
    if (hasTag) {
      const linksToPillar = contentStr.includes(mapping.pillar.toLowerCase());
      return { pillarName: mapping.name, pillarUrl: mapping.pillar, found: linksToPillar };
    }
  }
  
  return { pillarName: 'Unknown', pillarUrl: '', found: false };
}

function checkEntities(content, title, tags) {
  const contentLower = content.toLowerCase();
  const missing = [];
  
  // Location check
  if (!contentLower.includes('dhaka') && !contentLower.includes('bangladesh')) {
    missing.push('Dhaka/Bangladesh location mention');
  }
  
  // Service type check - extract from tags
  const tagStr = (tags || []).join(' ').toLowerCase();
  if (tagStr.includes('seo') && !contentLower.includes('seo')) {
    missing.push('SEO service mention');
  }
  if (tagStr.includes('local') && !contentLower.includes('local')) {
    missing.push('Local SEO mention');
  }
  if (tagStr.includes('ecommerce') && !contentLower.includes('ecommerce') && !contentLower.includes('e-commerce')) {
    missing.push('E-commerce mention');
  }
  if (tagStr.includes('mobile') && !contentLower.includes('mobile')) {
    missing.push('Mobile SEO mention');
  }
  if (tagStr.includes('technical') && !contentLower.includes('technical')) {
    missing.push('Technical SEO mention');
  }
  if (tagStr.includes('link building') && !contentLower.includes('link building') && !contentLower.includes('link-build')) {
    missing.push('Link building mention');
  }
  if (tagStr.includes('keyword') && !contentLower.includes('keyword')) {
    missing.push('Keyword research mention');
  }
  
  return missing;
}

// ── Run checks ──────────────────────────────────────────────────────────────
const results = [];

for (const slug of modifiedSlugs) {
  const post = posts.find(p => p.slug === slug);
  if (!post) {
    results.push({ slug, error: 'Not found in data.js' });
    continue;
  }
  
  const { title, date, excerpt, tags = [], content = '', metaTitle, metaDescription, dateModified, imagePlaceholder } = post;
  const keyword = extractKeyword(title);
  const kwCount = countOccurrences(content, keyword);
  const questionHeadings = countQuestionHeadings(content);
  const internalLinks = countInternalLinks(content);
  const missingEntities = checkEntities(content, title, tags);
  const pillarInfo = findPillarLink(content, tags);
  
  // Schema check
  const schemaMissing = [];
  if (!title) schemaMissing.push('title');
  if (!excerpt) schemaMissing.push('excerpt');
  if (!date) schemaMissing.push('date');
  if (!metaTitle) schemaMissing.push('metaTitle');
  if (!metaDescription) schemaMissing.push('metaDescription');
  
  const tfIdfOk = kwCount >= 5 || keyword.length < 3;
  const entitiesOk = missingEntities.length === 0;
  const pillarOk = pillarInfo.found;
  const aeoOk = questionHeadings >= 2;
  const linksOk = internalLinks >= 3;
  const schemaOk = schemaMissing.length === 0;
  
  results.push({
    slug,
    title,
    keyword,
    kwCount,
    tfIdfOk,
    missingEntities,
    entitiesOk,
    pillarInfo,
    pillarOk,
    questionHeadings,
    aeoOk,
    internalLinks,
    linksOk,
    schemaMissing,
    schemaOk,
    hasContent: content.length > 50
  });
}

// ── Output report ────────────────────────────────────────────────────────────
console.log('# Content Framework Enforcement Report');
console.log(`Run: ${new Date().toISOString()}`);
console.log(`Posts checked: ${results.length}\n`);
console.log('---\n');

let allPassed = true;
let totalChecks = 0;
let passedChecks = 0;

for (const r of results) {
  if (r.error) {
    console.log(`## Post: ${r.slug}`);
    console.log('⚠️ **Not found in data.js**\n');
    continue;
  }
  
  const checks = [
    { name: `TF-IDF: "${r.keyword}"`, ok: r.tfIdfOk, detail: r.tfIdfOk ? `${r.kwCount} occurrences` : `Only ${r.kwCount} occurrences (need ≥5)` },
    { name: 'Entities', ok: r.entitiesOk, detail: r.entitiesOk ? 'All key entities present' : `Missing: ${r.missingEntities.join(', ')}` },
    { name: 'Pillar Link', ok: r.pillarOk, detail: r.pillarOk ? `Links to: ${r.pillarInfo.pillarName} (${r.pillarInfo.pillarUrl})` : `No link to pillar: ${r.pillarInfo.pillarName}` },
    { name: 'AEO/GEO', ok: r.aeoOk, detail: r.aeoOk ? `${r.questionHeadings} question headings` : `Only ${r.questionHeadings} question headings (need ≥2)` },
    { name: 'Internal Links', ok: r.linksOk, detail: r.linksOk ? `${r.internalLinks} internal links` : `Only ${r.internalLinks} internal links (need ≥3)` },
    { name: 'Schema Ready', ok: r.schemaOk, detail: r.schemaOk ? 'All fields set' : `Missing: ${r.schemaMissing.join(', ')}` },
  ];
  
  const hasFail = checks.some(c => !c.ok);
  if (hasFail) allPassed = false;
  
  for (const c of checks) {
    totalChecks++;
    if (c.ok) passedChecks++;
  }
  
  const statusIcon = hasFail ? '⚠️' : '✅';
  console.log(`## ${statusIcon} Post: ${r.slug}`);
  console.log(`**Title:** ${r.title}`);
  console.log('| Check | Status | Details |');
  console.log('|-------|--------|---------|');
  for (const c of checks) {
    console.log(`| ${c.name} | ${c.ok ? '✅' : '❌'} | ${c.detail} |`);
  }
  
  if (hasFail) {
    console.log('\n### Fix instructions:');
    if (!r.tfIdfOk) console.log(`- **TF-IDF**: Increase "${r.keyword}" occurrences to ≥5. Add a few more uses in body paragraphs.`);
    if (!r.entitiesOk) console.log(`- **Missing entities**: Add mentions of: ${r.missingEntities.join(', ')}`);
    if (!r.pillarOk) console.log(`- **Pillar link**: Add an internal link to ${r.pillarInfo.pillarName} (${r.pillarInfo.pillarUrl})`);
    if (!r.aeoOk) console.log(`- **AEO/GEO**: Add ≥${2 - r.questionHeadings} more question-based headings (How, What, Why, etc.)`);
    if (!r.linksOk) console.log(`- **Internal links**: Add at least ${3 - r.internalLinks} more internal links (to services, locations, or other posts)`);
    if (!r.schemaOk) console.log(`- **Schema**: Set missing fields: ${r.schemaMissing.join(', ')}`);
    if (!r.hasContent) console.log(`- **Content**: Post body appears empty or missing`);
    console.log('');
  } else {
    console.log('\n✅ All checks passed.\n');
  }
  console.log('---\n');
}

// ── Summary ─────────────────────────────────────────────────────────────────
console.log('## Overall Summary');
console.log(`| Metric | Value |`);
console.log(`|--------|-------|`);
console.log(`| Posts checked | ${results.length} |`);
console.log(`| Checks passed | ${passedChecks}/${totalChecks} (${Math.round(passedChecks/totalChecks*100)}%) |`);
console.log(`| All checks passed | ${allPassed ? '✅ Yes' : '❌ No'} |`);
const fails = results.filter(r => !r.error && (
  !r.tfIdfOk || !r.entitiesOk || !r.pillarOk || !r.aeoOk || !r.linksOk || !r.schemaOk
));
console.log(`| Posts needing fixes | ${fails.length} |`);
console.log('');
if (fails.length > 0) {
  console.log('### Posts needing attention:');
  for (const f of fails) {
    const issues = [];
    if (!f.tfIdfOk) issues.push('TF-IDF');
    if (!f.entitiesOk) issues.push('Entities');
    if (!f.pillarOk) issues.push('Pillar');
    if (!f.aeoOk) issues.push('AEO/GEO');
    if (!f.linksOk) issues.push('Internal Links');
    if (!f.schemaOk) issues.push('Schema');
    console.log(`- **${f.slug}** — ${issues.join(', ')}`);
  }
}
