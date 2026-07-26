
    import { createRequire } from 'module';
    const require = createRequire(import.meta.url);
    // Read the file and extract just the posts array
    const fs = require('fs');
    let code = fs.readFileSync('src/app/blog/data.js', 'utf-8');
    // Replace the module.exports line
    code = code.replace('module.exports = posts;', 'export default posts;');
    // Write and import
    const tmpFile = '/tmp/_posts_data.mjs';
    fs.writeFileSync(tmpFile, code);
    const mod = await import(tmpFile);
    export default mod.default;
  