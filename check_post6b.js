const fs = require('fs');
const d = fs.readFileSync('src/app/blog/data.js', 'utf8');
const slug = 'hiring-seo-expert-dhaka-better-roi-than-paid-ads';
const idx = d.indexOf('slug: "' + slug + '"');
const contentStart = d.indexOf('content: `', idx);
const contentEnd = d.indexOf('`,', contentStart + 10);
const content = d.slice(contentStart + 10, contentEnd);

// Check for all variants
for (const kw of ['SEO Expert', 'SEO expert', 'seo expert', 'SEO Consultant', 'SEO consultant', 'seo consultant']) {
  const r = new RegExp(kw.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g');
  console.log(kw + ':', (content.match(r) || []).length);
}

// Check if "SEO Expert" appears at all
console.log('---');
console.log('Has "SEO Expert"?', /SEO\s+Expert/i.test(content));
// Check the actual content for phrases around "SEO Expert"
const idx2 = content.toLowerCase().indexOf('seo expert');
if (idx2 >= 0) console.log('Found at position:', idx2, 'context:', content.substring(Math.max(0, idx2-20), idx2+30));
else console.log('No occurrence of "seo expert" (case insensitive) found');
