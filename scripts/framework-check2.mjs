// Refined checks with Bengali support
import posts from '../src/app/blog/data.js';

const targets = {
  'schema-markup-rich-snippets-techniques': { kw: ['স্কিমা মার্কআপ', 'schema markup'] },
  'seo-canonical-url-guide-bd': { kw: ['ক্যানোনিকাল ইউআরএল', 'canonical url'] },
  'how-to-choose-best-seo-expert-dhaka-15-things': { kw: ['seo expert', 'seo expert in dhaka'] },
};

const EN_Q = /^\s*(how|what|why|when|where|can|do|is|are)\b/i;
const BN_Q = /^(কী|কি|কেন|কীভাবে|কিভাবে|কোন|কোনটি|কত|কখন|কোথায়|কোথা)/;

for (const [slug, cfg] of Object.entries(targets)) {
  const post = posts.find(p => p.slug === slug);
  const content = post.content;
  console.log(`=== ${slug} ===`);
  for (const kw of cfg.kw) {
    const re = new RegExp(kw.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi');
    console.log(`KW "${kw}": ${(content.match(re) || []).length} occurrences`);
  }
  const headings = content.split('\n').map(l => l.trim())
    .filter(l => /^#{1,6}\s/.test(l)).map(l => l.replace(/^#{1,6}\s+/, ''));
  const enQ = headings.filter(h => EN_Q.test(h));
  const bnQ = headings.filter(h => BN_Q.test(h));
  console.log(`EN question headings (${enQ.length}): ${enQ.join(' | ')}`);
  console.log(`BN question headings (${bnQ.length}): ${bnQ.join(' | ')}`);
  console.log('');
}
