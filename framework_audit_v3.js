#!/usr/bin/env node
/**
 * Content Framework Enforcer for kanokmiah.com.bd
 * Uses Node.js to parse the JS module directly
 */
const fs = require('fs');

// Read and eval the data file to get posts
const data = fs.readFileSync('/root/kanok-miahit/src/app/blog/data.js', 'utf8');

// The file has format: const posts = [ ... ]; export default posts;
// We need to capture the array
const arrayMatch = data.match(/const posts = (\[[\s\S]*?\]);\s*export/);
if (!arrayMatch) {
  console.error("Could not parse posts array");
  process.exit(1);
}

let posts;
try {
  // Replace template literals with regular strings for eval
  let jsCode = arrayMatch[1];
  
  // We need to handle template literals - convert to regular strings
  // This is tricky because content uses template literals with backticks
  
  // Alternative: write to temp file and require it
  const tmpFile = '/tmp/posts_data.cjs';
  fs.writeFileSync(tmpFile, 'module.exports = ' + arrayMatch[1] + ';');
  
  // But template literals inside template literals will break...
  // Let me try a different approach
  
  process.exit(0);
} catch(e) {
  console.error("Error:", e.message);
  process.exit(1);
}
