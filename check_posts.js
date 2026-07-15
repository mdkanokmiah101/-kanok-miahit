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
for (const slug of slugs) {
  const idx = d.indexOf('slug: "' + slug + '"');
  // get title
  const titleMatch = d.slice(idx, idx + 500).match(/title: "([^"]+)"/);
  const title = titleMatch ? titleMatch[1] : 'UNKNOWN';
  // get tags
  const tagsMatch = d.slice(idx, idx + 600).match(/tags: \[([^\]]+)\]/);
  const tags = tagsMatch ? tagsMatch[1] : '';
  // get excerpt
  const excerptMatch = d.slice(idx, idx + 800).match(/excerpt:\s*\n\s*"([^"]+)"/);
  const excerpt = excerptMatch ? excerptMatch[1] : '';
  // get date
  const dateMatch = d.slice(idx, idx + 400).match(/date: "([^"]+)"/);
  const date = dateMatch ? dateMatch[1] : '';
  // content
  const contentStart = d.indexOf('content: `', idx);
  const contentEnd = d.indexOf('`,', contentStart + 10);
  const content = d.slice(contentStart + 10, contentEnd);
  
  // A) TF-IDF: keyword from title
  let keyword = title;
  // Remove leading question words
  keyword = keyword.replace(/^(How|What|Why|When|Where|Can|Do|Is|Are)\s+/i, '');
  // Take first 2 meaningful words (3+ chars)
  const words = keyword.split(/[\s,:;—–\-()]+/).filter(w => w.length > 2);
  const primaryKw = words.slice(0, 2).join(' ');
  const kwRegex = new RegExp(primaryKw.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi');
  const kwCount = (content.match(kwRegex) || []).length;
  const tfidfPass = kwCount >= 5;
  
  // B) Entity check
  const hasDhaka = /Dhaka/i.test(content);
  const hasBangladesh = /Bangladesh/i.test(content);
  const hasSeo = /SEO/i.test(content);
  const entitiesPass = hasDhaka && hasBangladesh && hasSeo;
  const missingEntities = [];
  if (!hasDhaka) missingEntities.push('Dhaka');
  if (!hasBangladesh) missingEntities.push('Bangladesh');
  if (!hasSeo) missingEntities.push('SEO');
  
  // C) Pillar link
  const pillarUrl = '/blog/complete-seo-guide-bangladesh-businesses-2026';
  // Also check for GEO pillar if relevant
  const hasPillarLink = content.includes(pillarUrl);
  const hasGeoPillar = content.includes('/services/geo-ai-search');
  const pillarPass = hasPillarLink || hasGeoPillar;
  
  // D) AEO/GEO question headings
  const lines = content.split('\n');
  let qCount = 0;
  for (const line of lines) {
    const t = line.replace(/^#+\s*/, '').trim();
    // Remove leading numbers like "1. ", "2. " etc
    const clean = t.replace(/^\d+[\.\)]\s*/, '');
    if (/^(How|What|Why|When|Where|Can|Do|Is|Are)/i.test(clean)) {
      qCount++;
    }
  }
  const aeoPass = qCount >= 2;
  
  // E) Internal links (both relative and full-domain)
  const relLinks = (content.match(/\]\(\//g) || []).length;
  const fullLinks = (content.match(/\]\(https:\/\/kanokmiah\.com\.bd/g) || []).length;
  const totalLinks = relLinks + fullLinks;
  const linksPass = totalLinks >= 3;
  
  // F) Schema check
  const schemaPass = title.length > 0 && excerpt.length > 0 && date.length > 0;
  
  // Output
  console.log('## Post: ' + slug);
  console.log('Title: ' + title);
  console.log('| Check | Status | Details |');
  console.log('|-------|--------|---------|');
  console.log('| TF-IDF: "' + primaryKw + '" | ' + (tfidfPass ? '✅' : '❌') + ' | ' + kwCount + ' occurrences |');
  console.log('| Entities | ' + (entitiesPass ? '✅' : '❌') + ' | ' + (missingEntities.length ? 'Missing: ' + missingEntities.join(', ') : 'All present (Dhaka, Bangladesh, SEO)') + ' |');
  const pillarDetail = hasPillarLink ? 'Found: ' + pillarUrl : (hasGeoPillar ? 'Found: /services/geo-ai-search' : 'None found');
  console.log('| Pillar Link | ' + (pillarPass ? '✅' : '❌') + ' | ' + pillarDetail + ' |');
  console.log('| AEO/GEO | ' + (aeoPass ? '✅' : '❌') + ' | ' + qCount + ' question headings |');
  console.log('| Internal Links | ' + (linksPass ? '✅' : '❌') + ' | ' + totalLinks + ' total (' + relLinks + ' relative + ' + fullLinks + ' full-domain) |');
  console.log('| Schema Ready | ' + (schemaPass ? '✅' : '❌') + ' | ' + (schemaPass ? 'All fields set' : 'Missing fields') + ' |');
  console.log('');
}
