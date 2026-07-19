#!/usr/bin/env node
/**
 * Content Framework Enforcer v3 — refined keyword extraction for bilingual content.
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

/** Intelligent keyword extraction with bilingual fallback */
function extractPrimaryKeyword(title) {
  if (!title) return '';
  const colonIdx = title.indexOf(':');
  const beforeColon = colonIdx > -1 ? title.slice(0, colonIdx).trim() : title;
  let cleaned = beforeColon.replace(/^(Complete|Ultimate|Expert|Best|Top|Affordable|Professional|Comprehensive|সহজ|শ্রেষ্ঠ|সেরা|উত্তম|পূর্ণ|সম্পূর্ণ|সঠিক|নতুন|কার্যকরী)\s+/i, '');

  // Strategy 1: If the cleaned text contains Roman/English words, extract the longest English phrase
  const engWords = cleaned.match(/[A-Za-z][A-Za-z0-9+#.-]+/g);
  if (engWords && engWords.length > 0) {
    // For mixed Bengali+English, take the longest English segment
    // e.g. "সহজ ভাষায় SEO" → engWords = ["SEO"], return "SEO"
    // e.g. "B2B Lead Generation through SEO" → return first meaningful 2-4 words
    if (engWords.length === 1 && engWords[0].length <= 5) {
      // Single short English word like "SEO" — it's likely the primary keyword
      return engWords[0];
    }
    // Multiple English words — take first meaningful phrase (up to 4 words, stop at stop words)
    const engStop = /\s+(Guide|Tips|Strategies|Checklist|Techniques|Optimization|Benefits|Mistakes|Services|Agency|Company|Expert|Specialist|Consultant|Tools|Ideas|Examples|Case Study|Methods|Process|Steps|Framework|Roadmap|In|For|To|of|the|and|with|your|a|an|for|in|on|at|by|is|are|&|-|–|through|for|in Bangladesh|in Dhaka|in 2026|2026|Bangladesh|Dhaka)\s+/i;
    const fullEng = engWords.join(' ');
    const match = fullEng.match(engStop);
    if (match && match.index > 0) {
      return fullEng.slice(0, match.index).trim();
    }
    // No stop word found, return up to 3 words
    return engWords.slice(0, Math.min(3, engWords.length)).join(' ');
  }

  // Strategy 2: Pure Bengali — take the part before the colon (already cleaned)
  // Split by Bengali spaces/commas, take up to 3 meaningful tokens
  const bnParts = cleaned.split(/[\s,]+/).filter(Boolean);
  // Filter out very short tokens (likely particles)
  const meaningful = bnParts.filter(t => t.length >= 2);
  if (meaningful.length === 0) return bnParts.slice(0, 2).join(' ');

  // For Bengali, the primary keyword is usually the first 2-3 words
  // But avoid including "SEO" as a separate token - it should be the key term
  const seoIdx = meaningful.findIndex(t => /^SEO$/i.test(t) || t.includes('SEO'));
  if (seoIdx > 0) {
    // If SEO is not first, include everything up to and including SEO
    return meaningful.slice(0, seoIdx + 1).join(' ');
  }
  return meaningful.slice(0, Math.min(3, meaningful.length)).join(' ');
}

/** Multi-strategy TF-IDF check: try multiple keyword variants */
function checkTfidf(content, keyword, title) {
  if (!keyword || keyword.length < 2) return { pass: false, occurrences: 0, keyword };
  const text = content.toLowerCase();
  const kw = keyword.toLowerCase();

  // Direct count
  const escaped = kw.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const direct = (text.match(new RegExp(escaped, 'gi')) || []).length;
  if (direct >= 5) return { pass: true, occurrences: direct, keyword };

  // Strategy: Try just the English words if mixed
  const engWords = kw.match(/[a-z][a-z0-9+#.-]+/g);
  if (engWords && engWords.length >= 1) {
    // For "SEO" check separately — if it's >5 and the full keyword is some artifact
    for (const ew of engWords) {
      if (ew.length >= 2) {
        const ewEscaped = ew.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        const ewCount = (text.match(new RegExp(ewEscaped, 'gi')) || []).length;
        if (ewCount >= 5 && ew.length <= 8) {
          return { pass: true, occurrences: ewCount, keyword: ew };
        }
      }
    }
  }

  // Strategy: Try the first 2-3 Bengali tokens
  const bnTokens = kw.split(/[\s,]+/).filter(t => /[\u0980-\u09FF]/.test(t));
  if (bnTokens.length >= 2) {
    const bn2 = bnTokens.slice(0, 2).join(' ');
    const bn2Escaped = bn2.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const bn2Count = (text.match(new RegExp(bn2Escaped, 'gi')) || []).length;
    if (bn2Count >= 5) return { pass: true, occurrences: bn2Count, keyword: bn2 };
  }

  // Strategy: Try individual English words from the title
  const titleEng = title.match(/[A-Za-z][A-Za-z0-9+#.-]+/g);
  if (titleEng) {
    for (const te of titleEng) {
      if (te.length >= 3 && te.toLowerCase() !== 'the' && te.toLowerCase() !== 'and' && te.toLowerCase() !== 'for' && te.toLowerCase() !== 'with') {
        const teEscaped = te.toLowerCase().replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        const teCount = (text.match(new RegExp(teEscaped, 'gi')) || []).length;
        if (teCount >= 8) return { pass: true, occurrences: teCount, keyword: te };
      }
    }
  }

  // Strategy: Try just the English words from keyword as a phrase
  if (engWords && engWords.length >= 2) {
    const phrase = engWords.join(' ').toLowerCase();
    const phraseEscaped = phrase.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const phraseCount = (text.match(new RegExp(phraseEscaped, 'gi')) || []).length;
    if (phraseCount >= 5) return { pass: true, occurrences: phraseCount, keyword: phrase };
  }

  return { pass: direct >= 5, occurrences: direct, keyword };
}

/** Count question-based headings — supports Bangla + English */
function countQuestionHeadings(content) {
  const enWords = ['How', 'What', 'Why', 'When', 'Where', 'Can', 'Do', 'Is', 'Are', 'Does', 'Which', 'Who', 'Will', 'Has', 'Have', 'Should', 'Could', 'Would', 'May', 'Might'];
  const bnWords = ['কী', 'কেন', 'কখন', 'কোথায়', 'কীভাবে', 'কিভাবে', 'কোন', 'কোনটি', 'কি', 'হয়ে', 'হবে', 'হয়', 'কতো', 'কত', 'কার', 'কারা'];
  const allWords = [...enWords, ...bnWords];
  const pattern = new RegExp(`^#{2,3}\\s+(${allWords.join('|')})\\b`, 'gim');
  const matches = content.match(pattern);
  return matches ? matches.length : 0;
}

/** Count internal links */
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

/** Entity coverage check — bilingual */
function checkEntityCoverage(content, title, slug, tags) {
  const tagStr = tags.join(' ').toLowerCase();
  const text = content.toLowerCase();
  const missing = [];

  const needsBangladesh = slug.includes('bangladesh') || slug.includes('bd') || tagStr.includes('bangladesh');
  if (needsBangladesh) {
    if (!text.includes('bangladesh') && !text.includes('বাংলাদেশ') && !text.includes('বাংলাদেশী') && !text.includes('বাংলাদেশি')) missing.push('Bangladesh/বাংলাদেশ');
  }
  const needsDhaka = slug.includes('dhaka') || tagStr.includes('dhaka');
  if (needsDhaka) {
    if (!text.includes('dhaka') && !text.includes('ঢাকা') && !text.includes('ঢাকায়')) missing.push('Dhaka/ঢাকা');
  }

  const entityPairs = [
    { tag: ['garment','textile','rmg'], names: ['garment','textile','rmg','গার্মেন্টস','টেক্সটাইল'], label: 'Garments/Textile' },
    { tag: ['law','legal','attorney'], names: ['law','legal','attorney','advocate','আইন','আইনি','লিগাল'], label: 'Law/Legal' },
    { tag: ['fitness','gym','workout'], names: ['fitness','gym','workout','ফিটনেস','জিম'], label: 'Fitness/Gym' },
    { tag: ['startup','start-up'], names: ['startup','start-up','স্টার্টআপ'], label: 'Startup' },
    { tag: ['ecommerce','e-commerce','shopify','daraz'], names: ['ecommerce','e-commerce','online store','shop','ই-কমার্স','অনলাইন','দারাজ','shopify'], label: 'E-commerce' },
    { tag: ['hotel','resort'], names: ['hotel','resort','হোটেল','রিসোর্ট'], label: 'Hotel/Resort' },
    { tag: ['real estate','property'], names: ['real estate','property','রিয়েল এস্টেট'], label: 'Real Estate' },
    { tag: ['ngo','non-profit','nonprofit','charity'], names: ['ngo','non-profit','nonprofit','charity','এনজিও'], label: 'NGO/Non-profit' },
    { tag: ['youtube','video'], names: ['youtube','video','ইউটিউব','ভিডিও'], label: 'YouTube/Video' },
    { tag: ['podcast','audio'], names: ['podcast','audio','পডকাস্ট'], label: 'Podcast' },
    { tag: ['mobile app','mobile application'], names: ['app','mobile app','mobile application','মোবাইল অ্যাপ','অ্যাপ'], label: 'Mobile App' },
    { tag: ['education','educational','student','university','college','school'], names: ['education','student','university','college','school','শিক্ষা','বিশ্ববিদ্যালয়','কলেজ','স্কুল'], label: 'Education' },
    { tag: ['healthcare','health','medical','doctor','hospital','clinic'], names: ['health','medical','doctor','hospital','clinic','স্বাস্থ্য','চিকিৎসা','হাসপাতাল','ক্লিনিক'], label: 'Healthcare' },
    { tag: ['restaurant','food','cafe','dining'], names: ['restaurant','food','cafe','dining','রেস্টুরেন্ট','খাবার','ক্যাফে'], label: 'Restaurant/Food' },
    { tag: ['seo','search engine optimization'], names: ['seo','search engine optimization','এসইও','সার্চ ইঞ্জিন'], label: 'SEO' },
    { tag: ['local seo','local search','google maps'], names: ['local seo','local search','google maps','লোকাল','স্থানীয়'], label: 'Local SEO' },
    { tag: ['content marketing','content','blog','article'], names: ['content','blog','article','কন্টেন্ট','ব্লগ','আর্টিকেল'], label: 'Content' },
    { tag: ['schema','structured data','rich snippet','faq','howto','breadcrumb','json-ld'], names: ['schema','structured data','rich snippet','স্কিমা','স্ট্রাকচারড ডাটা','faq','howto'], label: 'Schema/Structured Data' },
    { tag: ['link building','backlink'], names: ['link building','backlink','লিংক','ব্যাকলিংক'], label: 'Link Building' },
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
    const { pass: tfidfPass, occurrences, keyword: usedKw } = checkTfidf(content, keyword, title);
    const questionHeadings = countQuestionHeadings(content);
    const internalLinks = countInternalLinks(content);

    if (tfidfPass) totalPass++; else totalFail++; totalChecks++;

    const entityCheck = checkEntityCoverage(content, title, slug, tags);
    if (entityCheck.pass) totalPass++; else totalFail++; totalChecks++;

    const pillarCheck = checkPillarLink(content, slug);
    const pillarTopic = determinePillarTopic(tags);
    if (pillarCheck.pass) totalPass++; else totalFail++; totalChecks++;

    const aeoPass = questionHeadings >= 2;
    if (aeoPass) totalPass++; else totalFail++; totalChecks++;

    const linkingPass = internalLinks >= 3;
    if (linkingPass) totalPass++; else totalFail++; totalChecks++;

    const missingSchema = [];
    if (!title) missingSchema.push('title');
    if (!excerpt) missingSchema.push('excerpt');
    if (!date) missingSchema.push('date');
    const schemaPass = missingSchema.length === 0;
    if (schemaPass) totalPass++; else totalFail++; totalChecks++;

    const hasIssues = !tfidfPass || !entityCheck.pass || !pillarCheck.pass || !aeoPass || !linkingPass || !schemaPass;
    if (hasIssues) postsWithIssues++; else postsClean++;

    const fixInstructions = [];
    if (!tfidfPass) fixInstructions.push(`- **TF-IDF**: \`${usedKw}\` appears only ${occurrences}× (need ≥5). Incorporate the topic term more prominently in headings and body paragraphs.`);
    if (!entityCheck.pass) fixInstructions.push(`- **Entities**: ${entityCheck.detail}. Add missing terms at least once.`);
    if (!pillarCheck.pass) fixInstructions.push(`- **Pillar Link**: Add a link to the "${pillarTopic}" pillar page (\`/blog/…\` or \`/services/…\`).`);
    if (!aeoPass) fixInstructions.push(`- **AEO/GEO**: Add ≥2 question-based headings. Use How/What/Why (English) or কী/কেন/কীভাবে (Bengali) — e.g. \`## কীভাবে …\`, \`## কেন … গুরুত্বপূর্ণ\`.`);
    if (!linkingPass) fixInstructions.push(`- **Internal Links**: Add more (${internalLinks} → ≥3). Link to other posts, services, or location pages.`);
    if (!schemaPass) fixInstructions.push(`- **Schema**: Missing: ${missingSchema.join(', ')}. Set these fields for ArticleSchema.`);

    reportParts.push(`## Post: ${slug}
| Check | Status | Details |
|-------|--------|---------|
| TF-IDF: \`${usedKw}\` | ${tfidfPass ? '✅' : '❌'} | ${occurrences} occurrences in content |
| Entities | ${entityCheck.pass ? '✅' : '❌'} | ${entityCheck.detail} |
| Pillar Link | ${pillarCheck.pass ? '✅' : '❌'} | ${pillarTopic}: ${pillarCheck.detail} |
| AEO/GEO | ${aeoPass ? '✅' : '❌'} | ${questionHeadings} question headings |
| Internal Links | ${linkingPass ? '✅' : '❌'} | ${internalLinks} internal links |
| Schema Ready | ${schemaPass ? '✅' : '❌'} | ${missingSchema.length ? `Missing: ${missingSchema.join(', ')}` : 'All fields set'}

### ${hasIssues ? '⚠️ Fix instructions:' : '✅ All checks passed'}
${fixInstructions.length ? fixInstructions.join('\n') : ''}`);
  }

  const pct = totalChecks ? Math.round(totalPass / totalChecks * 100) : 0;
  const summary = `# Content Framework Report — kanokmiah.com.bd
**Date**: ${new Date().toISOString().slice(0, 10)}
**Period**: Last 48 hours
**Posts checked**: ${modifiedSlugs.length}
**Posts with issues**: ${postsWithIssues}
**Posts fully clean**: ${postsClean}
**Checks passed**: ${totalPass}/${totalChecks} (${pct}%)
**Checks failed**: ${totalFail}
---

${reportParts.join('\n\n')}
`;

  const reportPath = '/tmp/framework-report-v3.md';
  writeFileSync(reportPath, summary, 'utf-8');
  console.log(summary);
}

main().catch(err => { console.error('Fatal:', err); process.exit(1); });
