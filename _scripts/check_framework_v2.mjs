/**
 * Content Framework Enforcer v2 — improved keyword extraction + corrected slugs.
 */
import { readFileSync, writeFileSync, unlinkSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __dirname = dirname(fileURLToPath(import.meta.url));

// Load data.js via a small wrapper
const dataPath = join(__dirname, '..', 'src', 'app', 'blog', 'data.js');
const raw = readFileSync(dataPath, 'utf-8');

const wrapperPath = join(__dirname, '___data_wrapper.mjs');
writeFileSync(wrapperPath, raw + '\nexport { posts };\n');
let posts;
try {
  const mod = await import(`file://${wrapperPath}`);
  posts = mod.posts;
} catch (e) {
  console.error('Failed to parse data.js:', e.message);
  process.exit(1);
}
try { unlinkSync(wrapperPath); } catch {}

// ── Correct modified slugs (reconciled with actual slugs in data.js) ──────
const modifiedSlugs = [
  // From "silo: processed blog #NN - <slug>" commits (Bangla batch + English batch)
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
  // From "feat: new blog" commits (exact slugs found in data.js)
  "how-to-choose-best-seo-expert-dhaka-15-things",
  "seo-expert-vs-seo-agency-dhaka-which-is-right",
  "top-10-seo-mistakes-dhaka-businesses-fix",
  "what-does-seo-expert-do-guide-business-owners",
  "seo-case-study-dhaka-businesses-increased-organic-traffic",
  "ai-seo-2026-dhaka-experts-optimize-google-ai-chatgpt",
  "hiring-seo-expert-dhaka-better-roi-than-paid-ads",
  "how-to-track-measure-seo-roi-bangladesh",
];

// ── Helpers ─────────────────────────────────────────────────────────────────

function extractKeyword(title) {
  let t = title;
  // Remove common prefixes
  t = t.replace(/^(Complete |Ultimate |The |How to |Why |What |When |Where |Essential |Top \d+ )/i, '');
  // Remove trailing parenthetical like "(2026 Guide)"
  t = t.replace(/\s*\([^)]*\)\s*$/g, '');
  // Remove trailing tagline after colon or emdash
  t = t.replace(/\s*[—–:].*$/, '');
  // Split into words, keep meaningful ones (>= 2 chars)
  const words = t.split(/[\s]+/).filter(w => w.length >= 2);
  // Take first 2-3 words
  return words.slice(0, 3).join(' ');
}

function countPhraseInContent(content, phrase) {
  if (!phrase || phrase.length < 2) return 999;
  const escaped = phrase.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const regex = new RegExp(escaped, 'gi');
  const matches = content.match(regex);
  return matches ? matches.length : 0;
}

function countQuestionHeadings(content) {
  const qWords = ['How', 'What', 'Why', 'When', 'Where', 'Can', 'Do', 'Is', 'Are', 'Does', 'Which', 'Who',
                  // Bangla question words
                  'কিভাবে', 'কীভাবে', 'কেন', 'কী', 'কোন', 'কখন', 'কোথায়', 'কি', 'হবে', 'করবেন', 'হয়'];
  const headingLines = content.match(/^#{2,4}\s+.*$/gm) || [];
  return headingLines.filter(h => {
    const cleanH = h.replace(/^#+\s*/, '')          // strip markdown heading markers
                      .replace(/^\d+[\.\)]\s*/, '')  // strip numbering like "1." or "2)"
                      .replace(/^[A-Z][\.\)]\s*/, '') // strip single letter enumerators like "A."
                      .trim();
    return qWords.some(q => cleanH.startsWith(q) || cleanH.startsWith(q.toLowerCase()));
  }).length;
}

function countInternalLinks(content) {
  const links = content.match(/\[([^\]]*)\]\((\/[^)]*)\)/g) || [];
  return links.length;
}

function findPillarLink(content, tags, opts = {}) {
  const tagStr = (tags || []).join(' ').toLowerCase();
  const contentLower = content.toLowerCase();
  const currentSlug = opts.slug || '';

  const pillarMap = [
    { tags: ['seo', 'seo guide', 'bangladesh seo', 'seo strategy'], pillar: '/blog/complete-seo-guide-bangladesh-businesses-2026', name: 'Complete SEO Guide' },
    { tags: ['local seo', 'google maps', 'local'], pillar: '/blog/local-seo-tips-dhaka-businesses-google-maps', name: 'Local SEO Dhaka guide' },
    { tags: ['ecommerce', 'daraz', 'shopify'], pillar: '/industries/ecommerce', name: 'E-commerce industry page' },
    { tags: ['technical seo', 'core web vitals', 'page speed', 'technical'], pillar: '/blog/technical-seo-checklist-bangladeshi-websites', name: 'Technical SEO checklist' },
    { tags: ['link building', 'link building'], pillar: '/blog/link-building-bangladesh-strategies', name: 'Link building guide' },
    { tags: ['keyword research', 'keywords', 'keyword'], pillar: '/blog/keyword-research-bangladesh-market', name: 'Keyword research guide' },
    { tags: ['content marketing', 'content'], pillar: '/industries/digital-marketing', name: 'Digital Marketing page' },
    { tags: ['geo', 'ai search', 'generative ai', 'generative engine'], pillar: '/blog/geo-optimization-prepare-business-ai-search', name: 'GEO guide' },
    { tags: ['mobile seo', 'mobile', 'mobile-first'], pillar: '/blog/mobile-seo-optimization-bangladesh-mobile-first-era', name: 'Mobile SEO guide' },
    { tags: ['real estate', 'property', 'real estate'], pillar: '/industries/real-estate', name: 'Real estate industry page' },
    { tags: ['google ads', 'ppc', 'paid ads'], pillar: '/blog/seo-vs-google-ads-whats-best-bangladesh-businesses', name: 'SEO vs Google Ads guide' },
    { tags: ['google business profile', 'gbp'], pillar: '/blog/google-business-profile-optimization-guide-bangladesh', name: 'GBP guide' },
    { tags: ['garments', 'textile', 'b2b', 'manufacturing'], pillar: '/industries/manufacturing', name: 'Manufacturing page' },
    { tags: ['international seo', 'global', 'export'], pillar: '/blog/international-seo-bangladesh-exporters-global-buyers', name: 'International SEO guide' },
    { tags: ['beginner', 'beginners'], pillar: '/blog/seo-bangla-beginners-guide-google-ranking', name: 'SEO beginners guide' },
    { tags: ['schema', 'structured data', 'rich snippets'], pillar: '/blog/schema-markup-rich-snippets-techniques', name: 'Schema markup guide' },
    { tags: ['youtube', 'video seo'], pillar: '/blog/youtube-seo-bangladesh-ranking-tips', name: 'YouTube SEO guide' },
    { tags: ['google search console', 'gsc'], pillar: '/blog/google-search-console-performance-guide', name: 'Google Search Console guide' },
    { tags: ['seo agency', 'seo expert', 'agency', 'agency'], pillar: '/blog/how-to-choose-right-seo-agency-bangladesh', name: 'Choose SEO agency guide' },
    { tags: ['facebook', 'social media', 'marketplace'], pillar: '/industries/ecommerce', name: 'E-commerce page' },
    { tags: ['case study', 'case studies'], pillar: '/case-studies', name: 'Case studies page' },
  ];

  // Higher specificity first
  for (const mapping of pillarMap) {
    const hasTag = mapping.tags.some(t => tagStr.includes(t));
    if (hasTag) {
      // Don't flag if the supposed pillar IS this post
          const isSelfLink = mapping.pillar === '/blog/' + currentSlug;
          if (isSelfLink) continue;
          const linksToPillar = contentLower.includes(mapping.pillar.toLowerCase());
      return { pillarName: mapping.name, pillarUrl: mapping.pillar, found: linksToPillar };
    }
  }

  // Fallback: check if ANY pillar link exists in the blog/industries
  const anyPillarLink = contentLower.match(/\]\(\/(?:blog|industries|services|case-studies)\/[^)]+\)/g);
  return { pillarName: 'Unmapped', pillarUrl: '', found: anyPillarLink && anyPillarLink.length > 0, fallback: true };
}

function checkEntities(content, title, tags) {
  const contentLower = content.toLowerCase();
  const missing = [];

  if (!contentLower.includes('dhaka') && !contentLower.includes('bangladesh') && !contentLower.includes('বাংলাদেশ')) {
    missing.push('Dhaka/Bangladesh location');
  }

  const tagStr = (tags || []).join(' ').toLowerCase();
  if (tagStr.includes('seo') && !contentLower.includes('seo') && !contentLower.includes('এসইও')) {
    missing.push('SEO mention');
  }
  if (tagStr.includes('local') && !contentLower.includes('local') && !contentLower.includes('স্থানীয়')) {
    missing.push('local SEO mention');
  }
  if (tagStr.includes('ecommerce') && !contentLower.includes('ecommerce') && !contentLower.includes('e-commerce') && !contentLower.includes('ই-কমার্স')) {
    missing.push('e-commerce mention');
  }
  if (tagStr.includes('mobile') && !contentLower.includes('mobile') && !contentLower.includes('মোবাইল')) {
    missing.push('mobile mention');
  }
  if (tagStr.includes('technical') && !contentLower.includes('technical') && !contentLower.includes('টেকনিক্যাল')) {
    missing.push('technical SEO mention');
  }
  if (tagStr.includes('link building') && !contentLower.includes('link building') && !contentLower.includes('লিংক বিল্ডিং')) {
    missing.push('link building mention');
  }
  if (tagStr.includes('keyword') && !contentLower.includes('keyword') && !contentLower.includes('কীওয়ার্ড')) {
    missing.push('keyword mention');
  }

  return missing;
}

// ── Run checks ──────────────────────────────────────────────────────────────
const results = [];

for (const slug of modifiedSlugs) {
  const post = posts.find(p => p.slug === slug);
  if (!post) {
    results.push({ slug, error: 'NOT_FOUND' });
    continue;
  }

  const { title, date, excerpt, tags = [], content = '', metaTitle, metaDescription } = post;
  const keyword = extractKeyword(title);
  const kwCount = countPhraseInContent(content, keyword);
  const questionHeadings = countQuestionHeadings(content);
  const internalLinks = countInternalLinks(content);
  const missingEntities = checkEntities(content, title, tags);
  const pillarInfo = findPillarLink(content, tags, { slug });

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
    slug, title, keyword, kwCount, tfIdfOk,
    missingEntities, entitiesOk,
    pillarInfo, pillarOk,
    questionHeadings, aeoOk,
    internalLinks, linksOk,
    schemaMissing, schemaOk,
  });
}

// ── Output report ───────────────────────────────────────────────────────────
console.log('# Content Framework Enforcement Report');
console.log(`Run: ${new Date().toISOString()}`);
console.log(`Commit range: 2026-07-14 05:30 UTC → 2026-07-15 19:14 UTC`);
console.log(`Posts checked: ${results.length}\n`);

let allPassed = true;
let totalChecks = 0;
let passedChecks = 0;

for (const r of results) {
  if (r.error === 'NOT_FOUND') {
    console.log(`## ⚠️ Post: ${r.slug}`);
    console.log('**Not found in data.js** — may be a different slug or external file\n---\n');
    continue;
  }

  const checks = [
    { name: `TF-IDF: "${r.keyword}"`, ok: r.tfIdfOk, detail: r.tfIdfOk ? `${r.kwCount} occurrences ✅` : `Only ${r.kwCount} occurrences (need ≥5)` },
    { name: 'Entities', ok: r.entitiesOk, detail: r.entitiesOk ? 'All key entities present ✅' : `Missing: ${r.missingEntities.join(', ')}` },
    { name: 'Pillar Link', ok: r.pillarOk, detail: r.pillarOk ? `✅ Links to: ${r.pillarInfo.pillarName} (${r.pillarInfo.pillarUrl})` : `❌ No link to pillar: ${r.pillarInfo.pillarName}` },
    { name: 'AEO/GEO', ok: r.aeoOk, detail: r.aeoOk ? `${r.questionHeadings} question headings ✅` : `Only ${r.questionHeadings} question headings (need ≥2)` },
    { name: 'Internal Links', ok: r.linksOk, detail: r.linksOk ? `${r.internalLinks} internal links ✅` : `Only ${r.internalLinks} internal links (need ≥3)` },
    { name: 'Schema Ready', ok: r.schemaOk, detail: r.schemaOk ? 'All fields set ✅' : `Missing: ${r.schemaMissing.join(', ')}` },
  ];

  const hasFail = checks.some(c => !c.ok);
  if (hasFail) allPassed = false;
  for (const c of checks) { totalChecks++; if (c.ok) passedChecks++; }

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
    if (!r.tfIdfOk) console.log(`- **TF-IDF**: Increase "${r.keyword}" to ≥5 occurrences in body. Currently ${r.kwCount}.`);
    if (!r.entitiesOk) console.log(`- **Missing entities**: Add: ${r.missingEntities.join(', ')}`);
    if (!r.pillarOk) console.log(`- **Pillar link**: Add internal link to **${r.pillarInfo.pillarName}** (${r.pillarInfo.pillarUrl})`);
    if (!r.aeoOk) console.log(`- **AEO/GEO**: Add ${2 - r.questionHeadings} question-based ## headings (How, What, Why, কিভাবে, কী, কেন 등)`);
    if (!r.linksOk) console.log(`- **Internal links**: Add ${3 - r.internalLinks} more links to services, locations, or other posts`);
    if (!r.schemaOk) console.log(`- **Schema**: Set: ${r.schemaMissing.join(', ')} — needed for ArticleSchema`);
    console.log('');
  } else {
    console.log('\n✅ All checks passed.\n');
  }
  console.log('---\n');
}

// ── Summary ─────────────────────────────────────────────────────────────────
console.log('## Overall Summary');
console.log('| Metric | Value |');
console.log('|--------|-------|');
console.log(`| Posts checked | ${results.filter(r => !r.error).length} |`);
console.log(`| Not found | ${results.filter(r => r.error).length} |`);
const valid = results.filter(r => !r.error);
console.log(`| Checks passed | ${passedChecks}/${totalChecks} (${Math.round(passedChecks/totalChecks*100)}%) |`);
const fails = valid.filter(r => !r.tfIdfOk || !r.entitiesOk || !r.pillarOk || !r.aeoOk || !r.linksOk || !r.schemaOk);
console.log(`| Posts needing fixes | ${fails.length}/${valid.length} |`);
console.log(`| All checks passed | ${allPassed ? '✅ Yes' : '❌ No'} |`);
console.log('');

if (fails.length > 0) {
  console.log('### Posts needing fixes (by issue):');
  const tfidf = valid.filter(r => !r.tfIdfOk);
  const entities = valid.filter(r => !r.entitiesOk);
  const pillar = valid.filter(r => !r.pillarOk);
  const aeo = valid.filter(r => !r.aeoOk);
  const links = valid.filter(r => !r.linksOk);
  const schema = valid.filter(r => !r.schemaOk);

  if (tfidf.length) console.log(`\n**TF-IDF (${tfidf.length})**: ${tfidf.map(r => r.slug).join(', ')}`);
  if (entities.length) console.log(`\n**Entities (${entities.length})**: ${entities.map(r => r.slug).join(', ')}`);
  if (pillar.length) console.log(`\n**Pillar Link (${pillar.length})**: ${pillar.map(r => r.slug).join(', ')}`);
  if (aeo.length) console.log(`\n**AEO/GEO (${aeo.length})**: ${aeo.map(r => r.slug).join(', ')}`);
  if (links.length) console.log(`\n**Internal Links (${links.length})**: ${links.map(r => r.slug).join(', ')}`);
  if (schema.length) console.log(`\n**Schema (${schema.length})**: ${schema.map(r => r.slug).join(', ')}`);
}
