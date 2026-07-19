#!/usr/bin/env node
/**
 * Content Framework Enforcer v2 — handles Bengali/English bilingual content.
 */
import { readFileSync, writeFileSync } from 'fs';

const DATA_JS = new URL('../src/app/blog/data.js', import.meta.url).pathname;
const SLUGS_FILE = '/tmp/modified_slugs.txt';

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

const PILLAR_SERVICES = [
  '/services/', '/services/seo', '/services/local-seo',
  '/services/ecommerce-seo', '/services/technical-seo',
  '/services/content-marketing',
];

/** Extract primary keyword phrase from title (Bangla + English aware) */
function extractPrimaryKeyword(title) {
  if (!title) return '';

  // Split on colon — take the part BEFORE colon as the primary keyword zone
  const colonIdx = title.indexOf(':');
  const beforeColon = colonIdx > -1 ? title.slice(0, colonIdx).trim() : title;

  // Strip leading fluff
  const cleaned = beforeColon.replace(/^(Complete|Ultimate|Expert|Best|Top|Affordable|Professional|Comprehensive|সহজ|শ্রেষ্ঠ|সেরা|উত্তম|পূর্ণ|সম্পূর্ণ)\s+/i, '');

  // For English titles, grab the first meaningful 2-3 word phrase
  const engStop = / (Guide|Tips|Strategies|Checklist|Techniques|Optimization|Benefits|Mistakes|Services|Agency|Company|Expert|Specialist|Consultant|Tools|Ideas|Examples|Case Study|Checklist|মethods|Process|Steps|Framework|Roadmap|In |For |to |for |in |of |the |and |with |your |a |an |& |-|–)/i;
  const engMatch = cleaned.match(engStop);
  if (engMatch && engMatch.index > 0) {
    return cleaned.slice(0, engMatch.index).trim();
  }

  // For English, return first 3 words
  const engWords = cleaned.split(' ').filter(w => /[a-zA-Z]/.test(w));
  if (engWords.length >= 2) return engWords.slice(0, Math.min(3, engWords.length)).join(' ');

  // For Bangla/Bengali, return everything before colon (or first 5 words)
  const bengaliParts = cleaned.split(/[\s,]+/).filter(Boolean);
  return bengaliParts.slice(0, Math.min(5, bengaliParts.length)).join(' ');
}

/** Count occurrences of a keyword in text, with Bangla-aware fallback */
function countOccurrences(text, keyword) {
  if (!keyword || keyword.length < 2) return 0;
  const escaped = keyword.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const matches = text.match(new RegExp(escaped, 'gi'));
  return matches ? matches.length : 0;
}

/** Count question-based headings — supports Bangla + English */
function countQuestionHeadings(content) {
  // English question words
  const enWords = ['How', 'What', 'Why', 'When', 'Where', 'Can', 'Do', 'Is', 'Are', 'Does', 'Which', 'Who', 'Will', 'Has', 'Have', 'Should', 'Could', 'Would', 'May', 'Might'];
  // Bengali question words
  const bnWords = ['কী', 'কেন', 'কখন', 'কোথায়', 'কীভাবে', 'কিভাবে', 'কোন', 'কোনটি', 'কি', 'হয়ে', 'হবে', 'হয়', 'কতো', 'কত', 'কার', 'কারা'];

  const allWords = [...enWords, ...bnWords];
  const pattern = new RegExp(`^#{2,3}\\s+(${allWords.join('|')})\\b`, 'gim');
  const matches = content.match(pattern);
  return matches ? matches.length : 0;
}

/** Count internal links (same-domain markdown links) */
function countInternalLinks(content) {
  const linkPattern = /\[([^\]]*)\]\((\/[^)]*)\)/g;
  const matches = content.matchAll(linkPattern);
  let count = 0;
  for (const m of matches) {
    const url = m[2];
    if (url.startsWith('//') || url.startsWith('http') || url === '#' || url.startsWith('#') || url.startsWith('mailto:')) continue;
    count++;
  }
  return count;
}

/** Check pillar link */
function checkPillarLink(content, slug) {
  if (PILLAR_SLUGS.has(slug)) return { pass: true, detail: `Self: pillar page (${slug})` };
  for (const pslug of PILLAR_SLUGS) {
    if (content.includes(`/blog/${pslug}`)) return { pass: true, detail: `Links to pillar: ${pslug}` };
  }
  for (const svc of PILLAR_SERVICES) {
    if (content.includes(svc)) return { pass: true, detail: `Links to service: ${svc}*` };
  }
  return { pass: false, detail: 'No pillar page or service link found' };
}

/** Determine pillar topic from tags */
function determinePillarTopic(tags) {
  const tagStr = tags.join(' ').toLowerCase();
  if (tagStr.includes('local') || tagStr.includes('maps') || tagStr.includes('gbp') || tagStr.includes('google business')) return 'Local SEO';
  if (tagStr.includes('technical') || tagStr.includes('core web') || tagStr.includes('crawl') || tagStr.includes('schema') || tagStr.includes('structured data') || tagStr.includes('canonical') || tagStr.includes('robots') || tagStr.includes('sitemap') || tagStr.includes('redirect') || tagStr.includes('https') || tagStr.includes('hreflang')) return 'Technical SEO';
  if (tagStr.includes('trend') || tagStr.includes('2026') || tagStr.includes('future') || tagStr.includes('ai') || tagStr.includes('geo')) return 'SEO Trends & GEO';
  if (tagStr.includes('ecommerce') || tagStr.includes('shopify') || tagStr.includes('daraz')) return 'E-commerce SEO';
  if (tagStr.includes('link building') || tagStr.includes('backlink')) return 'Link Building';
  if (tagStr.includes('keyword') || tagStr.includes('search intent')) return 'Keyword Research';
  if (tagStr.includes('content') || tagStr.includes('blog') || tagStr.includes('writing')) return 'Content Marketing';
  if (tagStr.includes('for ') || tagStr.includes('industry') || tagStr.includes('garment') || tagStr.includes('law') || tagStr.includes('fitness') || tagStr.includes('startup') || tagStr.includes('ngo') || tagStr.includes('real estate') || tagStr.includes('hotel') || tagStr.includes('restaurant') || tagStr.includes('education') || tagStr.includes('healthcare') || tagStr.includes('youtube') || tagStr.includes('podcast') || tagStr.includes('mobile app')) return 'Industry SEO';
  if (tagStr.includes('schema') || tagStr.includes('faq') || tagStr.includes('howto') || tagStr.includes('breadcrumb') || tagStr.includes('json-ld') || tagStr.includes('rich snippet')) return 'Structured Data';
  if (tagStr.includes('international') || tagStr.includes('hreflang') || tagStr.includes('global')) return 'International SEO';
  return 'General SEO';
}

/** Entity coverage check — Bangla + English aware */
function checkEntityCoverage(content, title, slug, tags) {
  const tagStr = tags.join(' ').toLowerCase();
  const text = content.toLowerCase();
  const missing = [];

  // Location entities (check both English and Bengali forms)
  const needsBangladesh = slug.includes('bangladesh') || slug.includes('bd') || tagStr.includes('bangladesh');
  if (needsBangladesh) {
    if (!text.includes('bangladesh') && !text.includes('বাংলাদেশ') && !text.includes('বাংলাদেশী') && !text.includes('বাংলাদেশি')) {
      missing.push('Bangladesh/বাংলাদেশ');
    }
  }
  const needsDhaka = slug.includes('dhaka') || tagStr.includes('dhaka') || slug.includes('dhaka');
  if (needsDhaka) {
    if (!text.includes('dhaka') && !text.includes('ঢাকা') && !text.includes('ঢাকায়')) {
      missing.push('Dhaka/ঢাকা');
    }
  }

  // Industry/service entities (bilingual)
  const entityPairs = [
    { tag: ['garment','textile','rmg'], names: ['garment','textile','rmg','গার্মেন্টস','টেক্সটাইল'], label: 'Garments/Textile' },
    { tag: ['law','legal','attorney'], names: ['law','legal','attorney','advocate','আইন','আইনি','লিগাল'], label: 'Law/Legal' },
    { tag: ['fitness','gym','workout'], names: ['fitness','gym','workout','ফিটনেস','জিম'], label: 'Fitness/Gym' },
    { tag: ['startup','start-up'], names: ['startup','start-up','স্টার্টআপ','স্টার্ট-আপ'], label: 'Startup' },
    { tag: ['ecommerce','e-commerce','shopify','daraz','online store'], names: ['ecommerce','e-commerce','online store','shop','ই-কমার্স','অনলাইন','দারাজ','shopify'], label: 'E-commerce' },
    { tag: ['hotel','resort','lodging'], names: ['hotel','resort','lodging','হোটেল','রিসোর্ট'], label: 'Hotel/Resort' },
    { tag: ['real estate','property','apartment'], names: ['real estate','property','apartment','রিয়েল এস্টেট','প্রপার্টি'], label: 'Real Estate' },
    { tag: ['ngo','non-profit','nonprofit','charity'], names: ['ngo','non-profit','nonprofit','charity','এনজিও','দাতব্য'], label: 'NGO/Non-profit' },
    { tag: ['youtube','video'], names: ['youtube','video','ইউটিউব','ভিডিও'], label: 'YouTube/Video' },
    { tag: ['podcast','audio'], names: ['podcast','audio','পডকাস্ট'], label: 'Podcast' },
    { tag: ['mobile app','mobile application'], names: ['app','mobile application','মোবাইল অ্যাপ','অ্যাপ'], label: 'Mobile App' },
    { tag: ['education','educational','student','university','college','school'], names: ['education','student','university','college','school','শিক্ষা','বিশ্ববিদ্যালয়','কলেজ','স্কুল'], label: 'Education' },
    { tag: ['healthcare','health','medical','doctor','hospital','clinic'], names: ['health','medical','doctor','hospital','clinic','স্বাস্থ্য','চিকিৎসা','হাসপাতাল','ক্লিনিক'], label: 'Healthcare' },
    { tag: ['restaurant','food','cafe','dining'], names: ['restaurant','food','cafe','dining','রেস্টুরেন্ট','খাবার','ক্যাফে'], label: 'Restaurant/Food' },
    { tag: ['seo','search engine optimization'], names: ['seo','search engine optimization','search engine optimisation','এসইও','সার্চ ইঞ্জিন'], label: 'SEO' },
    { tag: ['local seo','local search','google maps'], names: ['local seo','local search','google maps','লোকাল','স্থানীয়'], label: 'Local SEO' },
    { tag: ['content marketing','content','blog','article'], names: ['content','blog','article','কন্টেন্ট','ব্লগ','আর্টিকেল'], label: 'Content' },
    { tag: ['schema','structured data','rich snippet','faq','howto','breadcrumb','json-ld'], names: ['schema','structured data','rich snippet','স্কিমা','স্ট্রাকচারড ডাটা','faq','howto'], label: 'Schema/Structured Data' },
    { tag: ['link building','backlink','anchor text'], names: ['link building','backlink','anchor text','লিংক','ব্যাকলিংক','লিংক বিল্ডিং'], label: 'Link Building' },
    { tag: ['technical','core web','page speed','crawl','index'], names: ['technical','crawl','index','page speed','core web','টেকনিক্যাল','ক্রল','ইনডেক্স'], label: 'Technical SEO' },
  ];

  for (const pair of entityPairs) {
    const tagMatch = pair.tag.some(t => tagStr.includes(t) || slug.includes(t));
    if (!tagMatch) continue;
    const found = pair.names.some(n => text.includes(n));
    if (!found) missing.push(pair.label);
  }

  if (missing.length === 0) return { pass: true, detail: 'All expected entities found' };
  return { pass: false, detail: `Missing: ${missing.join(', ')}` };
}

// ── Main ────────────────────────────────────────────────────────────────────

async function main() {
  const posts = (await import(DATA_JS)).default;
  const modifiedSlugs = readFileSync(SLUGS_FILE, 'utf-8')
    .split('\n').map(s => s.trim()).filter(Boolean);

  console.log(`Loaded ${posts.length} total posts, ${modifiedSlugs.length} modified slugs\n`);

  const reportParts = [];
  let totalPass = 0, totalFail = 0, totalChecks = 0;
  let postsWithIssues = 0, postsClean = 0;

  for (const slug of modifiedSlugs) {
    const post = posts.find(p => p.slug === slug);
    if (!post) {
      reportParts.push(`## Post: ${slug}\n⚠️ Not found in data.js\n`);
      continue;
    }

    const { title, excerpt, date, tags = [], content = '' } = post;
    const keyword = extractPrimaryKeyword(title);
    const occurrences = countOccurrences(content, keyword);
    const questionHeadings = countQuestionHeadings(content);
    const internalLinks = countInternalLinks(content);

    // A. TF-IDF
    const tfidfPass = occurrences >= 5;
    if (tfidfPass) totalPass++; else totalFail++; totalChecks++;

    // B. Entities
    const entityCheck = checkEntityCoverage(content, title, slug, tags);
    if (entityCheck.pass) totalPass++; else totalFail++; totalChecks++;

    // C. Pillar
    const pillarCheck = checkPillarLink(content, slug);
    const pillarTopic = determinePillarTopic(tags);
    if (pillarCheck.pass) totalPass++; else totalFail++; totalChecks++;

    // D. AEO/GEO
    const aeoPass = questionHeadings >= 2;
    if (aeoPass) totalPass++; else totalFail++; totalChecks++;

    // E. Internal Links
    const linkingPass = internalLinks >= 3;
    if (linkingPass) totalPass++; else totalFail++; totalChecks++;

    // F. Schema
    const missingSchema = [];
    if (!title) missingSchema.push('title');
    if (!excerpt) missingSchema.push('excerpt');
    if (!date) missingSchema.push('date');
    const schemaPass = missingSchema.length === 0;
    if (schemaPass) totalPass++; else totalFail++; totalChecks++;

    const hasIssues = !tfidfPass || !entityCheck.pass || !pillarCheck.pass || !aeoPass || !linkingPass || !schemaPass;
    if (hasIssues) postsWithIssues++; else postsClean++;

    const fixInstructions = [];
    if (!tfidfPass) fixInstructions.push(`- **TF-IDF**: Increase \`${keyword}\` occurrences (${occurrences} → ≥5). Use the term naturally in headings and body text.`);
    if (!entityCheck.pass) fixInstructions.push(`- **Entities**: ${entityCheck.detail}. Add missing terms at least once.`);
    if (!pillarCheck.pass) fixInstructions.push(`- **Pillar Link**: Add a link to the "${pillarTopic}" pillar page (\`/blog/…\` or \`/services/…\`).`);
    if (!aeoPass) fixInstructions.push(`- **AEO/GEO**: Add more question headings (${questionHeadings} → ≥2). Use How/What/Why or Bengali question words (কী/কেন/কীভাবে).`);
    if (!linkingPass) fixInstructions.push(`- **Internal Links**: Add more (${internalLinks} → ≥3). Link to other posts, services, or location pages.`);
    if (!schemaPass) fixInstructions.push(`- **Schema**: Missing: ${missingSchema.join(', ')}.`);

    reportParts.push(`## Post: ${slug}
| Check | Status | Details |
|-------|--------|---------|
| TF-IDF: \`${keyword}\` | ${tfidfPass ? '✅' : '❌'} | ${occurrences} occurrences |
| Entities | ${entityCheck.pass ? '✅' : '❌'} | ${entityCheck.detail} |
| Pillar Link | ${pillarCheck.pass ? '✅' : '❌'} | ${pillarTopic}: ${pillarCheck.detail} |
| AEO/GEO | ${aeoPass ? '✅' : '❌'} | ${questionHeadings} question headings |
| Internal Links | ${linkingPass ? '✅' : '❌'} | ${internalLinks} total |
| Schema Ready | ${schemaPass ? '✅' : '❌'} | ${missingSchema.length ? `Missing: ${missingSchema.join(', ')}` : 'All fields set'}

### ${hasIssues ? '⚠️ Fix instructions:' : '✅ All checks passed'}
${fixInstructions.length ? fixInstructions.join('\n') : 'No fixes needed.'}`);
  }

  const pct = totalChecks ? Math.round(totalPass / totalChecks * 100) : 0;
  const summary = `# Content Framework Report — kanokmiah.com.bd
**Date**: ${new Date().toISOString().slice(0, 10)}
**Period**: Last 48 hours
**Posts checked**: ${modifiedSlugs.length}
**Posts with issues**: ${postsWithIssues}
**Posts clean**: ${postsClean}
**Checks passed**: ${totalPass}/${totalChecks} (${pct}%)
**Checks failed**: ${totalFail}
---

${reportParts.join('\n\n')}
`;

  const reportPath = '/tmp/framework-report-v2.md';
  writeFileSync(reportPath, summary, 'utf-8');
  console.log(summary);
}

main().catch(err => { console.error('Fatal:', err); process.exit(1); });
