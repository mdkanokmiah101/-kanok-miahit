/**
 * Content Framework Enforcer — FINAL
 * kanokmiah.com.bd — 48-hour git change audit
 */
import { readFileSync } from 'fs';

const dataPath = '/root/kanok-miahit/src/app/blog/data.js';
const raw = readFileSync(dataPath, 'utf-8');
const code = raw.replace('export default posts', 'return posts');
const getPosts = new Function(code);
const allPosts = getPosts();

const changedSlugs = [
  "b2b-lead-generation-seo-bangladesh",
  "google-discover-seo-bangladesh",
  "google-tag-manager-seo-bd",
  "seo-branded-vs-non-branded-bd", "seo-breadcrumb-schema-bd",
  "seo-canonical-url-guide-bd", "seo-career-guide-bangladesh-2026",
  "seo-competitor-analysis-bangladesh", "seo-consultant-dhaka-bangladesh",
  "seo-content-repurposing-bangladesh", "seo-direct-traffic-bangladesh",
  "seo-domain-authority-bangladesh", "seo-faq-schema-bangladesh",
  "seo-featured-snippet-bangladesh", "seo-for-fitness-gyms-bangladesh",
  "seo-for-law-firms-bangladesh", "seo-for-mobile-apps-bangladesh",
  "seo-for-ngo-bangladesh", "seo-for-podcast-bangladesh",
  "seo-for-startups-bangladesh", "seo-google-business-profile-posts",
  "seo-google-penalty-recovery-bd", "seo-howto-schema-bangladesh",
  "seo-hreflang-guide-bangladesh", "seo-https-ssl-impact-bangladesh",
  "seo-hubspot-vs-wordpress-bd", "seo-information-gain-optimization",
  "seo-json-ld-schema-bangladesh", "seo-keyword-clustering-bangladesh",
  "seo-knowledge-panel-bangladesh", "seo-landing-page-optimization-bd",
  "seo-local-citations-bangladesh", "seo-page-authority-bangladesh",
  "seo-passage-ranking-bangladesh", "seo-people-also-ask-optimization",
  "seo-pillar-content-strategy-bd", "seo-redirects-guide-bangladesh",
  "seo-referral-traffic-bangladesh", "seo-robots-txt-guide-bangladesh",
  "seo-search-intent-optimization", "seo-skyscraper-technique-bangladesh",
  "seo-structured-data-guide-bd", "seo-xml-sitemap-guide-bd",
  "seo-zero-click-search-bangladesh",
  "why-md-kanok-miah-is-the-best-seo-expert-in-dhaka-bangladesh"
];

function extractKeyword(title) {
  if (!title) return '';
  let t = title.trim().replace(/^(Complete |The Ultimate |Ultimate |Essential |A |An |The |Your |Top |Best )/i, '');
  const hasBen = /[\u0980-\u09FF]/.test(t);
  if (hasBen) {
    const colIdx = t.indexOf(':');
    if (colIdx > 0) t = t.substring(0, colIdx).trim();
    const words = t.split(/\s+/).filter(w => w.length > 0);
    if (words.length > 3) t = words.slice(0, 3).join(' ');
    return t;
  }
  const stop = t.match(/\s(for|in|of|to|at|on|and|vs|or|the|a|an|–|—|-|:)\s/i);
  if (stop && stop.index > 0) t = t.substring(0, stop.index).trim();
  const words = t.split(/\s+/).filter(w => w.length > 0);
  if (words.length > 3) t = words.slice(0, 3).join(' ');
  return t;
}

function countOccurrences(text, kw) {
  if (!text || !kw) return 0;
  try {
    const m = text.match(new RegExp(kw.replace(/[.*+?^${}()|[\]\\–\-]/g, '\\$&'), 'gi'));
    return m ? m.length : 0;
  } catch { return text.toLowerCase().split(kw.toLowerCase()).length - 1; }
}

function countQuestionHeadings(c) {
  if (!c) return 0;
  const e = (c.match(/^#{2,3}\s+(How|What|Why|When|Where|Can|Do|Is|Are|Does|Will|Should|Which|Who)\b/gim) || []).length;
  const b = (c.match(/^#{2,3}\s+(কী|কেন|কখন|কোথায়|কিভাবে|কীভাবে|কি|কোন|কাদের|কাকে|কত|কে|কার|কোনটা|কোনটি)\s/gim) || []).length;
  return e + b;
}

function getExpectedEntities(tags, title) {
  const e = new Set();
  const lt = (tags||[]).map(t=>t.toLowerCase());
  const ltitle = (title||'').toLowerCase();
  const hasBen = /[\u0980-\u09FF]/.test(title);
  
  e.add('Bangladesh');
  if (hasBen || lt.some(t=>t.includes('dhaka')) || ltitle.includes('dhaka')) e.add('Dhaka');
  
  for (const t of [...lt, ltitle]) {
    if (t.includes('local seo')||t.includes('google maps')||t.includes('gbp')||t.includes('google business')) { e.add('Google Business Profile'); e.add('Google Maps'); }
    if (t.includes('technical seo')||t.includes('crawl')||t.includes('canonical')||t.includes('redirect')||t.includes('sitemap')||t.includes('hreflang')||t.includes('robots')||t.includes('tag manager')||t.includes('gtm')) e.add('Technical SEO');
    if (t.includes('schema')||t.includes('structured data')||t.includes('faq')||t.includes('howto')||t.includes('breadcrumb')||t.includes('json-ld')) { e.add('Structured Data'); e.add('Schema Markup'); }
    if (t.includes('ecommerce')||t.includes('e-commerce')||t.includes('daraz')||t.includes('shopify')) e.add('E-commerce');
    if (t.includes('link building')||t.includes('backlink')) e.add('Backlinks');
    if (t.includes('geo')||t.includes('ai search')||t.includes('generative engine')) { e.add('GEO'); e.add('AI Search'); }
    if (t.includes('fitness')||t.includes('gym')) e.add('Fitness/Gym Industry');
    if (t.includes('law')||t.includes('legal')||t.includes('law firm')) e.add('Legal Industry');
    if (t.includes('startup')) e.add('Startups');
    if (t.includes('b2b')||t.includes('lead generation')) { e.add('B2B'); e.add('Lead Generation'); }
    if (t.includes('mobile')||t.includes('app')) e.add('Mobile Optimization');
    if (t.includes('podcast')) e.add('Podcast SEO');
    if (t.includes('ngo')) e.add('NGO');
    if (t.includes('knowledge panel')) e.add('Knowledge Panel');
    if (t.includes('featured snippet')||t.includes('zero-click')) { e.add('Featured Snippet'); e.add('Zero-Click Search'); }
    if (t.includes('people also ask')||t.includes('paa')) e.add('People Also Ask');
    if (t.includes('passage ranking')||t.includes('information gain')) e.add('AI/ML Ranking Signals');
    if (t.includes('search intent')) e.add('Search Intent');
    if (t.includes('branded')||t.includes('non-branded')) e.add('Branded/Non-Branded Keywords');
    if (t.includes('direct traffic')||t.includes('referral traffic')) e.add('Traffic Analysis');
    if (t.includes('domain authority')||t.includes('page authority')) e.add('SEO Authority Metrics');
    if (t.includes('competitor analysis')||t.includes('keyword clustering')) { e.add('Competitor Analysis'); e.add('Keyword Clustering'); }
    if (t.includes('skyscraper')||t.includes('content repurposing')||t.includes('pillar')) e.add('Content Strategy');
    if (t.includes('hubspot')||t.includes('wordpress')) e.add('CMS Platform Comparison');
    if (t.includes('landing page')) e.add('Landing Page Optimization');
    if (t.includes('career')) e.add('SEO Career Guide');
    if (t.includes('citation')) { e.add('Local Citations'); e.add('Directory Listings'); }
  }
  
  if (!hasBen) e.add('Kanok Miah');
  
  return [...e];
}

function checkEntityPresence(content, entities) {
  const lower = (content||'').toLowerCase();
  const present = [], missing = [];
  for (const entity of entities) {
    const s = entity.toLowerCase();
    let found = lower.includes(s);
    if (entity === 'Kanok Miah' && !found) {
      found = lower.includes('kanok') || lower.includes('কনক') || lower.includes('মিঞা');
    }
    if (found) present.push(entity); else missing.push(entity);
  }
  return { present, missing };
}

function getPillarMapping(tags) {
  const lt = (tags||[]).map(t=>t.toLowerCase());
  if (lt.some(t=>t.includes('local seo')||t.includes('google maps')||t.includes('gbp')||t.includes('citation')||t.includes('google business')))
    return { pillar: 'Local SEO Services', pillarUrl: '/services/local-seo' };
  if (lt.some(t=>t.includes('technical seo')||t.includes('crawl')||t.includes('canonical')||t.includes('redirect')||t.includes('robots')||t.includes('sitemap')||t.includes('hreflang')||t.includes('schema')||t.includes('structured data')||t.includes('faq')||t.includes('howto')||t.includes('breadcrumb')||t.includes('json-ld')||t.includes('tag manager')||t.includes('gtm')||t.includes('mobile')||t.includes('app')))
    return { pillar: 'Technical SEO Services', pillarUrl: '/services/technical-seo' };
  if (lt.some(t=>t.includes('ecommerce')||t.includes('e-commerce')||t.includes('daraz')||t.includes('shopify')))
    return { pillar: 'E-commerce SEO Services', pillarUrl: '/services/ecommerce-seo' };
  if (lt.some(t=>t.includes('link building')||t.includes('backlink')))
    return { pillar: 'Link Building Services', pillarUrl: '/services/link-building' };
  if (lt.some(t=>t.includes('geo')||t.includes('ai search')||t.includes('generative')||t.includes('passage ranking')||t.includes('information gain')||t.includes('search intent')))
    return { pillar: 'GEO & AI Search', pillarUrl: '/services/geo-ai-search' };
  if (lt.some(t=>t.includes('seo guide')||t.includes('bangladesh seo')||t.includes('digital marketing')||t.includes('consultant')||t.includes('best seo expert')))
    return { pillar: 'Main SEO Guide', pillarUrl: '/blog/complete-seo-guide-bangladesh-businesses-2026' };
  if (lt.some(t=>t.includes('content')||t.includes('skyscraper')||t.includes('repurposing')||t.includes('pillar')||t.includes('podcast')))
    return { pillar: 'Content Marketing', pillarUrl: '/services' };
  if (lt.some(t=>t.includes('startup'))) return { pillar: 'Startup SEO', pillarUrl: '/services' };
  if (lt.some(t=>t.includes('b2b')||t.includes('lead'))) return { pillar: 'B2B SEO', pillarUrl: '/services' };
  if (lt.some(t=>t.includes('fitness')||t.includes('gym')||t.includes('law')||t.includes('ngo')||t.includes('garment')||t.includes('textile')||t.includes('real estate')||t.includes('food')||t.includes('restaurant')||t.includes('education')||t.includes('medical')||t.includes('spa')||t.includes('salon')))
    return { pillar: 'Industry SEO', pillarUrl: '/industries' };
  if (lt.some(t=>t.includes('knowledge panel')||t.includes('featured snippet')||t.includes('zero-click')||t.includes('people also ask')))
    return { pillar: 'SERP Features', pillarUrl: '/services' };
  if (lt.some(t=>t.includes('competitor')||t.includes('keyword clustering')||t.includes('branded')||t.includes('non-branded')||t.includes('direct')||t.includes('referral')||t.includes('domain authority')||t.includes('page authority')||t.includes('landing page')))
    return { pillar: 'SEO Strategy', pillarUrl: '/services' };
  if (lt.some(t=>t.includes('hubspot')||t.includes('wordpress'))) return { pillar: 'Platform SEO', pillarUrl: '/services' };
  if (lt.some(t=>t.includes('career'))) return { pillar: 'SEO Career Guide', pillarUrl: '/blog' };
  return { pillar: 'General SEO', pillarUrl: '/services' };
}

function getInternalLinks(content) {
  if (!content) return [];
  const m = [...content.matchAll(/\]\((\/[a-z0-9-/]+)\)/gi)];
  return m.map(x=>x[1]).filter(l=>l.startsWith('/blog/')||l.startsWith('/services/')||l.startsWith('/locations/')||l.startsWith('/industries/')||l==='/about'||l==='/contact');
}

function checkSchema(post) {
  const req = ['title','excerpt','date','slug','author'];
  const miss = req.filter(f=>!post[f]||(typeof post[f]==='string'&&!post[f].trim()));
  return { missing: miss, hasDateModified: !!post.dateModified };
}

// ---- MAIN ----
const changedPosts = allPosts.filter(p => changedSlugs.includes(p.slug));
const reports = [];

console.log('# 🔍 Content Framework Enforcement Report — kanokmiah.com.bd\n');
console.log(`**Date:** ${new Date().toISOString()} UTC`);
console.log(`**Scope:** 48-hour git changes to src/app/blog/data.js`);
console.log(`**Posts checked:** ${changedPosts.length}/${changedSlugs.length} changed slugs found\n`);

for (const post of changedPosts) {
  const title = post.title || '';
  const content = post.content || '';
  const tags = post.tags || [];
  
  const keyword = extractKeyword(title);
  const occurrences = countOccurrences(content, keyword);
  const expectedEntities = getExpectedEntities(tags, title);
  const { present: presentEntities, missing: missingEntities } = checkEntityPresence(content, expectedEntities);
  const { pillar, pillarUrl } = getPillarMapping(tags);
  const hasPillar = content ? content.includes(pillarUrl) : false;
  const questionHeadings = countQuestionHeadings(content);
  const meaningfulLinks = getInternalLinks(content);
  const { missing: schemaMissing, hasDateModified } = checkSchema(post);
  
  reports.push({
    slug: post.slug, title,
    keyword, occurrences, expectedEntities, missingEntities,
    pillar, pillarUrl, hasPillar,
    questionHeadings, meaningfulLinks,
    schemaMissing, hasDateModified, qhPass: questionHeadings >= 2,
    tfidfPass: occurrences >= 5,
    entityPass: missingEntities.length === 0,
    pillarPass: hasPillar,
    linkPass: meaningfulLinks.length >= 3,
    schemaPass: schemaMissing.length === 0,
    results: [
      { check: `TF-IDF`, status: occurrences >= 5 ? '✅' : '❌', details: `"${keyword}" → ${occurrences}× ${occurrences >= 5 ? '✅' : '(need ≥5)'}` },
      { check: `Entities (${expectedEntities.length} expected)`, status: missingEntities.length === 0 ? '✅' : '❌', details: missingEntities.length === 0 ? `All ${presentEntities.length} present ✅` : `Missing: ${missingEntities.join(', ')}` },
      { check: `Pillar: ${pillar}`, status: hasPillar ? '✅' : '❌', details: hasPillar ? `Links to ${pillarUrl} ✅` : `No link to ${pillarUrl}` },
      { check: `AEO/GEO (Q-headings)`, status: questionHeadings >= 2 ? '✅' : '❌', details: `${questionHeadings} Q-headings ${questionHeadings >= 2 ? '✅' : '(need ≥2)'}` },
      { check: `Internal Links`, status: meaningfulLinks.length >= 3 ? '✅' : '❌', details: `${meaningfulLinks.length} internal links ${meaningfulLinks.length >= 3 ? '✅' : '(need ≥3)'}` },
      { check: `Schema Ready`, status: schemaMissing.length === 0 ? '✅' : '❌', details: schemaMissing.length === 0 ? `All fields${hasDateModified ? ' + dateModified' : ''} ✅` : `Missing: ${schemaMissing.join(', ')}${hasDateModified ? '' : ', no dateModified'}` }
    ]
  });
}

// ---- Per-post output ----
for (const r of reports) {
  console.log(`## ${r.slug}`);
  console.log(`**Title:** ${r.title}`);
  console.log('| Check | Status | Details |');
  console.log('|-------|--------|---------|');
  for (const res of r.results) {
    console.log(`| ${res.check} | ${res.status} | ${res.details} |`);
  }
  console.log('');
}

// ---- Summary stats ----
console.log('---\n## 📊 Overall Summary\n');
console.log('| Metric | Count |');
console.log('|--------|-------|');
console.log(`| Total posts checked | ${reports.length} |`);
console.log(`| All 6 checks passed | ${reports.filter(r=>r.results.every(x=>x.status==='✅')).length} |`);
console.log(`| Has ≥1 failing check | ${reports.filter(r=>r.results.some(x=>x.status==='❌')).length} |`);
console.log(`|  |  |`);
console.log(`| ✅ TF-IDF ≥5 | ${reports.filter(r=>r.tfidfPass).length}/${reports.length} |`);
console.log(`| ✅ Entities covered | ${reports.filter(r=>r.entityPass).length}/${reports.length} |`);
console.log(`| ✅ Pillar link present | ${reports.filter(r=>r.pillarPass).length}/${reports.length} |`);
console.log(`| ✅ AEO/GEO ≥2 Q-headings | ${reports.filter(r=>r.qhPass).length}/${reports.length} |`);
console.log(`| ✅ Internal links ≥3 | ${reports.filter(r=>r.linkPass).length}/${reports.length} |`);
console.log(`| ✅ Schema ready | ${reports.filter(r=>r.schemaPass).length}/${reports.length} |`);

// Entity misses aggregated
const entityMissCount = {};
for (const r of reports) {
  for (const e of r.missingEntities) {
    entityMissCount[e] = (entityMissCount[e] || 0) + 1;
  }
}
console.log('\n## 🏆 Top Missing Entities\n');
for (const [e, c] of Object.entries(entityMissCount).sort((a,b)=>b[1]-a[1])) {
  console.log(`- **${e}**: ${c}/${reports.length} posts (${((c/reports.length)*100).toFixed(0)}%)`);
}

// ---- Priority Fix Instructions ----
console.log('\n## 🔧 Priority Fix Instructions\n');

// 1. Missing Pillar Links
const noPillarReports = reports.filter(r => !r.pillarPass);
if (noPillarReports.length > 0) {
  console.log(`### Missing Pillar Links (${noPillarReports.length} posts)\n`);
  for (const r of noPillarReports) {
    console.log(`- **${r.slug}**: Add link to **${r.pillar}** (${r.pillarUrl}) in the content body`);
  }
  console.log('');
}

// 2. Low AEO/GEO
const lowAeoReports = reports.filter(r => !r.qhPass);
if (lowAeoReports.length > 0) {
  console.log(`### Low AEO/GEO — <2 Question Headings (${lowAeoReports.length} posts)\n`);
  console.log('Add H2/H3 headings starting with question words (How/What/Why/কী/কেন/কিভাবে) to improve AI search visibility.\n');
  for (const r of lowAeoReports.slice(0, 20)) {
    console.log(`- **${r.slug}**: ${r.questionHeadings} Q-headings`);
  }
  if (lowAeoReports.length > 20) console.log(`- ... and ${lowAeoReports.length - 20} more`);
  console.log('');
}

// 3. Thin TF-IDF
const thinReports = reports.filter(r => !r.tfidfPass);
if (thinReports.length > 0) {
  console.log(`### Thin TF-IDF — <5 Keyword Occurrences (${thinReports.length} posts)\n`);
  for (const r of thinReports) {
    console.log(`- **${r.slug}**: "${r.keyword}" → ${r.occurrences}× — increase primary keyword usage in body text`);
  }
  console.log('');
}

// 4. Entity gaps
console.log(`### Entity Coverage Gaps (Top 5)\n`);
for (const [e, c] of Object.entries(entityMissCount).sort((a,b)=>b[1]-a[1]).slice(0, 5)) {
  console.log(`- **${e}**: missing from ${c} posts — ensure these entities appear in the content body`);
}
console.log('');

// 5. Clean posts
const clean = reports.filter(r => r.results.every(x => x.status === '✅'));
if (clean.length > 0) {
  console.log(`### ✅ Clean Posts — All Checks Passed\n`);
  for (const r of clean) {
    console.log(`- ✅ **${r.slug}** — ${r.title}`);
  }
  console.log('');
}

// Cleanup
console.log('---\n*Report generated by Content Framework Enforcer (cron job)*');
