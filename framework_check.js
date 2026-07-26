// Extract and analyze blog posts from data.js
const fs = require('fs');
const data = fs.readFileSync('src/app/blog/data.js', 'utf8');

// Extract all post objects using a simple approach
// Find the array and eval it safely
const start = data.indexOf('const posts = [');
const end = data.lastIndexOf('];');
const arrayStr = data.slice(start + 'const posts = '.length, end + 1);

// We need a safer way - let's use regex to extract each post block
const postBlocks = data.match(/\{\s*\n\s*slug:\s*"([^"]+)",[\s\S]*?\n\s*\},/g);

const posts = [];
for (const block of postBlocks) {
  const slugMatch = block.match(/slug:\s*"([^"]+)"/);
  const titleMatch = block.match(/title:\s*"([^"]+)"/);
  const dateMatch = block.match(/date:\s*"([^"]+)"/);
  const excerptMatch = block.match(/excerpt:\s*\n\s*"([^"]+)"/);
  const tagsMatch = block.match(/tags:\s*\[([^\]]+)\]/);
  const dateModifiedMatch = block.match(/dateModified:\s*"([^"]+)"/);
  const metaTitleMatch = block.match(/metaTitle:\s*"([^"]+)"/);
  const metaDescMatch = block.match(/metaDescription:\s*"([^"]+)"/);
  const contentMatch = block.match(/content:\s*`([\s\S]*?)`\s*,?\s*\n\s*\}/);

  if (slugMatch) {
    const post = {
      slug: slugMatch[1],
      title: titleMatch ? titleMatch[1] : '',
      date: dateMatch ? dateMatch[1] : '',
      excerpt: excerptMatch ? excerptMatch[1] : '',
      tags: tagsMatch ? tagsMatch[1].split(',').map(t => t.trim().replace(/"/g, '')) : [],
      dateModified: dateModifiedMatch ? dateModifiedMatch[1] : '',
      metaTitle: metaTitleMatch ? metaTitleMatch[1] : '',
      metaDescription: metaDescMatch ? metaDescMatch[1] : '',
      content: contentMatch ? contentMatch[1] : ''
    };
    posts.push(post);
  }
}

// Output as JSON for Python processing
console.log(JSON.stringify(posts, null, 2));
