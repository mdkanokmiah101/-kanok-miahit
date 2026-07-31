// Content Framework Enforcer — checks for kanokmiah.com.bd blog posts
import posts from '../src/app/blog/data.js';

const TARGET_SLUGS = [
  'schema-markup-rich-snippets-techniques',
  'seo-canonical-url-guide-bd',
  'how-to-choose-best-seo-expert-dhaka-15-things',
];

const QUESTION_WORDS = /^\s*(how|what|why|when|where|can|do|is|are)\b/i;

function countOccurrences(haystack, needle) {
  if (!needle) return 0;
  const n = needle.toLowerCase().trim();
  const h = haystack.toLowerCase();
  let count = 0;
  let idx = 0;
  while ((idx = h.indexOf(n, idx)) !== -1) {
    count++;
    idx += n.length;
  }
  return count;
}

// Extract primary keyword: first meaningful noun phrase from title.
// Heuristic: strip leading stop/question words + generic words, take first 2-4 significant words.
const TITLE_STOP = new Set([
  'a','an','the','of','for','in','on','at','to','from','by','with','and','or','your','you',
  'our','we','i','is','are','was','were','be','been','how','what','why','when','where','can',
  'do','does','did','complete','ultimate','best','guide','bangladesh','bangladeshi','dhaka',
  '2026','2025','2024','top','things','thing','know','before','after','vs','&','and',
]);

function primaryKeyword(title) {
  const words = title.replace(/[^a-zA-Z0-9\s-]/g, ' ').split(/\s+/).filter(Boolean);
  // Find first significant word (not in stop set)
  let start = -1;
  for (let i = 0; i < words.length; i++) {
    if (!TITLE_STOP.has(words[i].toLowerCase())) { start = i; break; }
  }
  if (start === -1) return null;
  const phrase = [];
  for (let i = start; i < words.length && phrase.length < 3; i++) {
    const w = words[i].toLowerCase();
    if (TITLE_STOP.has(w) && phrase.length > 0) break;
    if (w.length < 3 && phrase.length === 0) continue;
    phrase.push(w);
  }
  return phrase.join(' ');
}

function extractHeadings(content) {
  return content
    .split('\n')
    .map(l => l.trim())
    .filter(l => /^#{1,6}\s/.test(l))
    .map(l => l.replace(/^#{1,6}\s+/, ''));
}

function internalLinks(content) {
  const links = [...content.matchAll(/\[([^\]]+)\]\((\/[^)]*)\)/g)].map(m => ({ text: m[1], href: m[2] }));
  return links;
}

function analyze(post) {
  const slug = post.slug;
  const title = post.title || '';
  const excerpt = post.excerpt || '';
  const content = post.content || '';
  const tags = Array.isArray(post.tags) ? post.tags : [];
  const kw = primaryKeyword(title);

  const kwCount = kw ? countOccurrences(content, kw) : 0;

  // B. Semantic entities — location, service type, industry
  const entityChecks = {
    'Location: Dhaka/Bangladesh': /dhaka|bangladesh/i.test(content),
    'Service type (SEO/service)': /seo|সেবা|service|agency|মার্কেটিং|optimization|অপটিমাইজেশন/i.test(content),
  };
  const missingEntities = Object.entries(entityChecks)
    .filter(([, ok]) => !ok)
    .map(([k]) => k);

  // C. Pillar link — check for links to pillar pages (/blog/complete-seo-guide..., /services/..., /locations/...)
  const pillarPatterns = [
    /\(\/blog\/complete-seo-guide-bangladesh-businesses-2026\)/,
    /\(\/blog\/seo-bangla-beginners-guide-google-ranking\)/,
    /\(\/blog\/local-seo-tips-dhaka-businesses-google-maps\)/,
    /\(\/blog\/technical-seo-checklist-bangladeshi-websites\)/,
  ];
  const pillarHits = pillarPatterns.map(p => (p.test(content) ? p.source : null)).filter(Boolean);

  // D. AEO/GEO question headings
  const headings = extractHeadings(content);
  const questionHeadings = headings.filter(h => QUESTION_WORDS.test(h));

  // E. Internal links
  const links = internalLinks(content);
  const internalCount = links.length;
  const linkTargets = links.map(l => l.href);

  // F. Schema readiness
  const schemaFields = {
    title: !!title,
    excerpt: !!excerpt,
    date: !!post.date,
    metaTitle: !!post.metaTitle,
    metaDescription: !!post.metaDescription,
    dateModified: !!post.dateModified,
  };
  const missingSchema = Object.entries(schemaFields).filter(([, ok]) => !ok).map(([k]) => k);

  return {
    slug, title, kw, kwCount, missingEntities, pillarHits, questionHeadings,
    internalCount, linkTargets, missingSchema, headings, tags,
  };
}

for (const slug of TARGET_SLUGS) {
  const post = posts.find(p => p.slug === slug);
  if (!post) { console.log(`NOT FOUND: ${slug}`); continue; }
  const r = analyze(post);
  console.log(JSON.stringify(r, null, 2));
  console.log('---END---');
}
