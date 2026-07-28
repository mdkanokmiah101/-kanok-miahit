const fs = require('fs');
const content = fs.readFileSync('/root/kanok-miahit/src/app/blog/data.js', 'utf8');
const lines = content.split('\n');

// Extract each post's content into separate files
const posts = [
  { slug: 'seo-expert-vs-seo-agency-dhaka-which-is-right', start: 25602, end: 25827 },
  { slug: 'smmgen-seo-case-study', start: 25065, end: 25122 },
  { slug: 'smmsun-seo-case-study', start: 25125, end: 25188 },
  { slug: 'stealth-windshield-repairs-seo-case-study', start: 25332, end: 25395 },
  { slug: 'top-10-seo-mistakes-dhaka-businesses-fix', start: 25830, end: 26022 },
  { slug: 'watchzonebd-seo-case-study', start: 27260, end: 27478 },
];

for (const post of posts) {
  const postLines = lines.slice(post.start - 1, post.end);
  const postContent = postLines.join('\n');
  fs.writeFileSync(`/root/kanok-miahit/tmp_${post.slug}.txt`, postContent);
  console.log(`Extracted ${post.slug}: ${postLines.length} lines`);
}
