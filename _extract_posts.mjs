import { readFileSync, writeFileSync } from 'fs';

// Read the data.js file and evaluate it to get the posts array
const data = readFileSync('/root/kanok-miahit/src/app/blog/data.js', 'utf-8');

// We need to extract the posts array. Since it uses `const posts = [...]`, 
// we can evaluate it in a controlled way by extracting the array literal.
// But template literals make this complex. Let's use a different approach:
// Modify the file to export the data, then import it.

// Actually, let's just regex-extract each post block more carefully.
// Each post is of the form:
// {
//   slug: "...",
//   ...
//   content: `...`
// },

// Let's find the outer structure
const posts = [];

// Split by "  {" to find individual posts, but be careful with template literals
let depth = 0;
let currentPost = '';
let inTemplate = false;
let i = 0;

// Find the start of posts array
const arrayStart = data.indexOf('const posts = [');
if (arrayStart === -1) {
  console.error('Could not find posts array');
  process.exit(1);
}

// Parse from after the opening bracket
let j = arrayStart + 'const posts = ['.length;
let braceDepth = 0;
let inString = false;
let stringChar = '';

// Collect each post object
while (j < data.length) {
  const ch = data[j];
  
  // Handle strings
  if (!inTemplate) {
    if ((ch === '"' || ch === "'") && !inString) {
      inString = true;
      stringChar = ch;
    } else if (ch === stringChar && inString) {
      // Check if escaped
      if (j === 0 || data[j-1] !== '\\') {
        inString = false;
        stringChar = '';
      }
    }
  }
  
  // Handle template literals (backticks)
  if (ch === '`') {
    // Check if escaped
    if (j === 0 || data[j-1] !== '\\') {
      inTemplate = !inTemplate;
    }
  }
  
  if (!inString && !inTemplate) {
    if (ch === '{') braceDepth++;
    if (ch === '}') {
      braceDepth--;
      if (braceDepth === 0 && currentPost.includes('slug:')) {
        // End of a post object
        currentPost += '}';
        posts.push(currentPost);
        currentPost = '';
        j++;
        continue;
      }
    }
  }
  
  if (braceDepth > 0 || (braceDepth === 0 && ch === '{')) {
    currentPost += ch;
  }
  
  j++;
}

// Now parse each post
const extracted = posts.map(postText => {
  const extract = (key) => {
    // Handle both slug: "value" and key: value patterns
    const re = new RegExp(`${key}:\\s*"([^"]+)"`);
    const m = postText.match(re);
    return m ? m[1] : '';
  };
  
  const extractMulti = (key) => {
    const re = new RegExp(`${key}:\\s*"([^"]+)"`, 'g');
    const matches = [...postText.matchAll(re)];
    return matches.map(m => m[1]);
  };
  
  const slug = extract('slug');
  const title = extract('title');
  const date = extract('date');
  const excerpt = extract('excerpt');
  const dateModified = extract('dateModified');
  
  // Tags (array)
  const tagsMatch = postText.match(/tags:\s*\[([^\]]+)\]/);
  const tags = tagsMatch 
    ? tagsMatch[1].split(',').map(t => t.trim().replace(/^"/, '').replace(/"$/, '')).filter(Boolean)
    : [];
  
  // Content (template literal between backticks)
  // Find the content field value
  const contentMatch = postText.match(/content:\s*`\n?([\s\S]*?)\n?\s*`/);
  let content = contentMatch ? contentMatch[1] : '';
  
  // Remove the closing backtick artifacts
  if (content.endsWith('`')) {
    content = content.slice(0, -1);
  }
  
  return { slug, title, date, excerpt, dateModified, tags, content };
});

// Filter out empty entries
const valid = extracted.filter(p => p.slug);
console.log(JSON.stringify(valid, null, 2));
