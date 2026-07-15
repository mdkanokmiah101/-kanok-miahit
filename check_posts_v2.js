const fs = require('fs');
const d = fs.readFileSync('src/app/blog/data.js', 'utf8');
const slugs = [
  'how-to-choose-best-seo-expert-dhaka-15-things',
  'seo-expert-vs-seo-agency-dhaka-which-is-right',
  'top-10-seo-mistakes-dhaka-businesses-fix',
  'what-does-seo-expert-do-guide-business-owners',
  'seo-case-study-dhaka-businesses-increased-organic-traffic',
  'hiring-seo-expert-dhaka-better-roi-than-paid-ads',
  'ai-seo-2026-dhaka-experts-optimize-google-ai-chatgpt',
  'watchzonebd-seo-case-study'
];

// Manually defined primary keywords per post
const keywords = {
  'how-to-choose-best-seo-expert-dhaka-15-things': 'SEO Expert',
  'seo-expert-vs-seo-agency-dhaka-which-is-right': 'SEO Expert',
  'top-10-seo-mistakes-dhaka-businesses-fix': 'SEO Mistakes',
  'what-does-seo-expert-do-guide-business-owners': 'SEO Expert',
  'seo-case-study-dhaka-businesses-increased-organic-traffic': 'SEO Case Study',
  'hiring-seo-expert-dhaka-better-roi-than-paid-ads': 'SEO Expert',
  'ai-seo-2026-dhaka-experts-optimize-google-ai-chatgpt': 'AI SEO',
  'watchzonebd-seo-case-study': 'E-commerce SEO'
};

for (const slug of slugs) {
  const idx = d.indexOf('slug: "' + slug + '"');
  const block = d.slice(idx, idx + 2000);
  
  const title = (block.match(/title: "([^"]+)"/) || [,''])[1];
  const tags = (block.match(/tags: \[([^\]]+)\]/) || [,''])[1];
  const excerpt = (block.match(/excerpt:\s*\n\s*"([^"]+)"/) || [,''])[1];
  const date = (block.match(/date: "([^"]+)"/) || [,''])[1];
  
  const contentStart = d.indexOf('content: `', idx);
  const contentEnd = d.indexOf('`,', contentStart + 10);
  const content = d.slice(contentStart + 10, contentEnd);
  
  // A) TF-IDF
  const primaryKw = keywords[slug];
  const kwRegex = new RegExp(primaryKw.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi');
  const kwCount = (content.match(kwRegex) || []).length;
  const tfidfPass = kwCount >= 5;
  
  // B) Entities
  const hasDhaka = /Dhaka/i.test(content);
  const hasBangladesh = /Bangladesh/i.test(content);
  const hasSeo = /SEO/i.test(content) || /search engine optimization/i.test(content);
  const entitiesPass = hasDhaka && hasBangladesh && hasSeo;
  const missingEntities = [];
  if (!hasDhaka) missingEntities.push('Dhaka');
  if (!hasBangladesh) missingEntities.push('Bangladesh');
  if (!hasSeo) missingEntities.push('SEO');
  
  // C) Pillar - check for main pillar or geo pillar
  const hasMainPillar = content.includes('/blog/complete-seo-guide-bangladesh-businesses-2026');
  const hasGeoPillar = content.includes('/services/geo-ai-search');
  const pillarPass = hasMainPillar || hasGeoPillar;
  
  // D) AEO/GEO - question headings
  const lines = content.split('\n');
  let qCount = 0;
  for (const line of lines) {
    if (!line.trim().startsWith('#')) continue;
    const t = line.replace(/^#+\s*/, '').trim();
    const clean = t.replace(/^\d+[\.\)]\s*/, '');
    if (/^(How|What|Why|When|Where|Can|Do|Is|Are)/i.test(clean)) {
      qCount++;
    }
  }
  const aeoPass = qCount >= 2;
  
  // E) Internal links
  const relLinks = (content.match(/\]\(\//g) || []).length;
  const fullLinks = (content.match(/\]\(https:\/\/kanokmiah\.com\.bd/g) || []).length;
  const totalLinks = relLinks + fullLinks;
  const linksPass = totalLinks >= 3;
  
  // F) Schema
  const schemaPass = title.length > 0 && excerpt.length > 0 && date.length > 0;
  
  // Collect question headings for detail
  const qHeadings = [];
  for (const line of lines) {
    if (!line.trim().startsWith('#')) continue;
    const t = line.replace(/^#+\s*/, '').trim();
    const clean = t.replace(/^\d+[\.\)]\s*/, '');
    if (/^(How|What|Why|When|Where|Can|Do|Is|Are)/i.test(clean)) {
      qHeadings.push(t);
    }
  }
  
  console.log('## Post: ' + slug);
  console.log('Title: ' + title);
  console.log('Tags: [' + tags + ']');
  console.log('');
  console.log('| Check | Status | Details |');
  console.log('|-------|--------|---------|');
  console.log('| TF-IDF: "' + primaryKw + '" | ' + (tfidfPass ? '✅' : '❌') + ' | ' + kwCount + ' occurrences (need ≥5) |');
  console.log('| Entities | ' + (entitiesPass ? '✅' : '❌') + ' | ' + (missingEntities.length ? 'Missing: ' + missingEntities.join(', ') : 'Dhaka ✅, Bangladesh ✅, SEO ✅') + ' |');
  const pillarDetail = hasMainPillar ? 'Links to pillar: /blog/complete-seo-guide...' : (hasGeoPillar ? 'Links to GEO pillar: /services/geo-ai-search' : '❌ No pillar link found');
  console.log('| Pillar Link | ' + (pillarPass ? '✅' : '❌') + ' | ' + pillarDetail + ' |');
  console.log('| AEO/GEO | ' + (aeoPass ? '✅' : '❌') + ' | ' + qCount + ' question headings (need ≥2): ' + qHeadings.slice(0,3).join('; ') + (qHeadings.length > 3 ? '...' : '') + ' |');
  console.log('| Internal Links | ' + (linksPass ? '✅' : '❌') + ' | ' + totalLinks + ' total (' + relLinks + ' relative + ' + fullLinks + ' full-domain) |');
  console.log('| Schema Ready | ' + (schemaPass ? '✅' : '❌') + ' | ' + (schemaPass ? 'Title ✅, Excerpt ✅, Date ✅' : 'Missing fields') + ' |');
  console.log('');
}
