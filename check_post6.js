const fs = require('fs');
const d = fs.readFileSync('src/app/blog/data.js', 'utf8');
const slug = 'hiring-seo-expert-dhaka-better-roi-than-paid-ads';
const idx = d.indexOf('slug: "' + slug + '"');
const contentStart = d.indexOf('content: `', idx);
const contentEnd = d.indexOf('`,', contentStart + 10);
const content = d.slice(contentStart + 10, contentEnd);

// Count keywords
for (const kw of ['SEO Expert', 'SEO Consultant', 'SEO ROI', 'SEO']) {
  const r = new RegExp(kw.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi');
  console.log(kw + ' count:', (content.match(r) || []).length);
}

// Title
const titleMatch = d.slice(idx, idx + 200).match(/title:\s*\n\s*"([^"]+)"/);
console.log('Title:', titleMatch ? titleMatch[1] : 'NOT FOUND');

// Question headings
const lines = content.split('\n');
let qCount = 0;
const qHeadings = [];
for (const line of lines) {
  if (!line.trim().startsWith('#')) continue;
  const t = line.replace(/^#+\s*/, '').trim();
  const clean = t.replace(/^\d+[\.\)]\s*/, '');
  if (/^(How|What|Why|When|Where|Can|Do|Is|Are)/i.test(clean)) {
    qCount++;
    qHeadings.push(t);
  }
}
console.log('Question headings:', qCount);
console.log('Sample headings:', qHeadings.slice(0, 5));
