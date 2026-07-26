#!/usr/bin/env node
/**
 * Content Framework Enforcer — Blog Post Audit
 * Checks: TF-IDF coverage, Semantic entities, Pillar-cluster alignment,
 *         AEO/GEO optimization, Internal linking, Schema readiness
 */

import { promises as fs } from 'fs';

// ── Helpers ──────────────────────────────────────────────────────────

function extractKeyword(title) {
  // Extract first meaningful noun phrase from title
  const stopwords = new Set(['the', 'a', 'an', 'in', 'for', 'of', 'to', 'and', 'is', 'are', 'what', 'how', 'why', 'when', 'where', 'your', 'our', 'its', 'their', 'complete', 'guide', 'ultimate', 'best', 'top']);
  const words = title.replace(/[^a-zA-Z\s-]/g, '').split(/\s+/).filter(w => w.length > 2 && !stopwords.has(w.toLowerCase()));
  // Also return the full first "key phrase" — first 2-3 meaningful words
  const meaningful = words.filter(w => w.length > 3);
  return meaningful.slice(0, 3).join(' ') || words.slice(0, 3).join(' ') || title.split(' ').slice(0, 3).join(' ');
}

function countOccurrences(content, keyword) {
  if (!keyword || keyword.length < 3) return 999; // skip if keyword too short
  const parts = keyword.toLowerCase().split(' ');
  let count = 0;
  // Check whole keyword phrase
  const phraseRegex = new RegExp(keyword.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi');
  count = (content.match(phraseRegex) || []).length;
  // Also check key terms individually  
  for (const part of parts) {
    if (part.length > 3) {
      const termRegex = new RegExp(part.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi');
      count += (content.match(termRegex) || []).length;
    }
  }
  return count;
}

function checkEntities(content, title, slug) {
  const requiredEntities = [];
  const lower = content.toLowerCase();
  const titleLower = title.toLowerCase();

  // Location entities
  if (!lower.includes('dhaka') && !slug.includes('dhaka')) {
    requiredEntities.push('Dhaka');
  }
  if (!lower.includes('bangladesh')) {
    requiredEntities.push('Bangladesh');
  }

  // Service type - try to determine from content
  if (lower.includes('seo') || lower.includes('search engine optimization')) {
    if (!lower.includes('seo')) requiredEntities.push('SEO');
  }

  // Author entity
  if (!lower.includes('kanok miah') && !lower.includes('kanok')) {
    // Check if it's a Bangla post
    if (!/[ঀ-৿]/.test(content)) {
      requiredEntities.push('Kanok Miah');
    }
  }

  // Industry/theme specific entities
  if (lower.includes('ecommerce') || lower.includes('e-commerce') || lower.includes('shopify') || lower.includes('daraz')) {
    if (!lower.includes('ecommerce') && !lower.includes('e-commerce')) requiredEntities.push('E-commerce');
  }
  if (lower.includes('garment') || lower.includes('textile') || lower.includes('rmg')) {
    if (!lower.includes('garment')) requiredEntities.push('Garment/Textile');
  }
  if (lower.includes('real estate') || lower.includes('property') || lower.includes('apartment')) {
    if (!lower.includes('real estate')) requiredEntities.push('Real Estate');
  }
  if (lower.includes('mobile') || lower.includes('smartphone') || lower.includes('voice search')) {
    // Common enough, don't flag
  }
  if (lower.includes('google business profile') || lower.includes('gbp') || lower.includes('google maps')) {
    if (!lower.includes('google business profile')) requiredEntities.push('Google Business Profile');
  }
  if (lower.includes('international') || lower.includes('export') || lower.includes('global buyer')) {
    if (!lower.includes('export')) requiredEntities.push('Export');
  }
  if (lower.includes('content market') || lower.includes('content writing')) {
    // common
  }
  if (lower.includes('link building') || lower.includes('backlink')) {
    if (!lower.includes('link building')) requiredEntities.push('Link Building');
  }
  if (lower.includes('keyword research') || lower.includes('keyword')) {
    // common
  }

  return requiredEntities;
}

function countQuestionHeadings(content) {
  const questionStarters = /^#{1,6}\s+(How|What|Why|When|Where|Can|Do|Is|Are|Does|Which|Who)\b/gim;
  const matches = content.match(questionStarters) || [];
  return matches.length;
}

function countInternalLinks(content) {
  // Count links to /blog/, /services/, /locations/, /industries/, /about, /contact, /
  const internalLinkPattern = /\]\(\/(?!http|https|www\.)(?:blog\/|services\/|locations\/|industries\/|about|contact|#)/g;
  const matches = content.match(internalLinkPattern) || [];
  return matches.length;
}

function checkPillarLink(post, allPosts) {
  // Determine pillar topic from tags
  const tags = (post.tags || []).join(' ').toLowerCase();
  let pillarSlug = null;
  let pillarName = null;

  if (tags.includes('seo guide') || tags.includes('bangladesh seo')) {
    pillarSlug = 'complete-seo-guide-bangladesh-businesses-2026';
    pillarName = 'Complete SEO Guide for Bangladesh Businesses 2026';
  } else if (tags.includes('ecommerce') || tags.includes('e-commerce')) {
    pillarSlug = 'why-ecommerce-store-needs-seo-bangladesh';
    pillarName = 'E-commerce SEO guide';
  } else if (tags.includes('technical')) {
    pillarSlug = 'technical-seo-checklist-bangladeshi-websites';
    pillarName = 'Technical SEO guide';
  } else if (tags.includes('local')) {
    pillarSlug = 'google-business-profile-optimization-guide-bangladesh';
    pillarName = 'GBP optimization guide';
  } else if (tags.includes('link building')) {
    pillarSlug = 'link-building-strategies-bangladesh-market';
    pillarName = 'Link Building guide';
  } else if (tags.includes('mobile')) {
    pillarSlug = 'mobile-seo-optimization-bangladesh-mobile-first-era';
    pillarName = 'Mobile SEO guide';
  } else if (tags.includes('content')) {
    pillarSlug = 'content-marketing-strategy-bangladeshi-brands-seo';
    pillarName = 'Content Marketing guide';
  } else if (tags.includes('geo') || tags.includes('aeo') || tags.includes('ai search')) {
    pillarSlug = 'geo-optimization-prepare-business-ai-search';
    pillarName = 'GEO/AEO guide';
  } else if (tags.includes('garment') || tags.includes('textile')) {
    pillarSlug = 'seo-garments-textile-industry-b2b-lead-generation';
    pillarName = 'Garments/Textile SEO guide';
  } else if (tags.includes('real estate')) {
    pillarSlug = 'seo-real-estate-developers-dhaka';
    pillarName = 'Real Estate SEO guide';
  } else if (tags.includes('international') || tags.includes('export')) {
    pillarSlug = 'international-seo-bangladesh-exporters-global-buyers';
    pillarName = 'International SEO guide';
  } else if (tags.includes('semantic') || tags.includes('schema')) {
    pillarSlug = 'schema-markup-rich-snippets-techniques';
    pillarName = 'Schema markup guide';
  } else if (tags.includes('bangla') || tags.includes('বাংলা')) {
    pillarSlug = 'seo-bangla-beginners-guide-google-ranking';
    pillarName = 'SEO Bangla guide';
  } else if (tags.includes('google ads') || tags.includes('ppc')) {
    pillarSlug = 'seo-vs-google-ads-bangladesh-business';
    pillarName = 'SEO vs Google Ads guide';
  }

  if (!pillarSlug) return { ok: null, detail: 'No pillar mapping found for tags: ' + (post.tags || []).join(', ') };

  // Check if pillar is this post itself
  if (post.slug === pillarSlug) return { ok: true, detail: `Self (pillar page: ${pillarName})` };

  // Check content links to pillar
  const contentLower = post.content.toLowerCase();
  const pillarLink = contentLower.includes(pillarSlug) || contentLower.includes(pillarName.toLowerCase().slice(0, 20));
  if (pillarLink) {
    return { ok: true, detail: `Links to pillar: ${pillarName}` };
  }

  return { ok: false, detail: `Missing link to pillar: ${pillarName} (${pillarSlug})` };
}

function checkSchemaReadiness(post) {
  const missing = [];
  if (!post.title || post.title.trim() === '') missing.push('title');
  if (!post.excerpt || post.excerpt.trim() === '') missing.push('excerpt');
  if (!post.date || post.date.trim() === '') missing.push('date');
  if (!post.slug || post.slug.trim() === '') missing.push('slug');
  if (!post.author || post.author.trim() === '') missing.push('author');
  if (missing.length > 0) {
    return { ok: false, detail: `Missing: ${missing.join(', ')}` };
  }
  return { ok: true, detail: 'All basic fields set (title, excerpt, date, slug, author)' };
}

// ── Main ─────────────────────────────────────────────────────────────

async function main() {
  // Read data.js
  const dataJs = await fs.readFile('src/app/blog/data.js', 'utf-8');

  // Extract posts array using eval-safe method
  // Find the posts array definition and reconstruct
  const postsStart = dataJs.indexOf('const posts = [');
  if (postsStart === -1) {
    console.error('Could not find posts array in data.js');
    process.exit(1);
  }

  // We need to evaluate the JS to get the posts. Since it's CommonJS-like, let's
  // write it as a module and import it.
  await fs.writeFile('scripts/_temp_load_posts.mjs', `
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
  `);

  // Actually, let's just use a simpler approach: regex to find each post object
  const posts = [];
  // Find all post objects by splitting on '},' and reconstructing
  // Simpler: just match slug, title, date, excerpt, tags, content fields
  const slugRegex = /slug:\s*"([^"]+)"/g;
  const titleRegex = /title:\s*"([^"]+)"/g;
  const dateRegex = /date:\s*"([^"]+)"/g;
  const excerptRegex = /excerpt:\s*\n\s*"([^"]+)"/g;
  const tagsRegex = /tags:\s*\[([^\]]+)\]/g;
  const contentRegex = /content:\s*`([\s\S]*?)`\s*,/g;

  const slugs = [...dataJs.matchAll(slugRegex)].map(m => m[1]);
  const titles = [...dataJs.matchAll(titleRegex)].map(m => m[1]);
  const dates = [...dataJs.matchAll(dateRegex)].map(m => m[1]);
  const excerpts = [...dataJs.matchAll(excerptRegex)].map(m => m[1]);

  // Parse tags
  const tagMatches = [...dataJs.matchAll(tagsRegex)];
  const tagsList = tagMatches.map(m => {
    const inner = m[1];
    return inner.split(',').map(t => t.trim().replace(/^"|"$/g, '')).filter(t => t);
  });

  // Parse content - this is tricky with backticks
  const contentMatches = [...dataJs.matchAll(/content:\s*`([\s\S]*?)`\s*,?/g)];
  const contents = contentMatches.map(m => m[1]);

  // Parse authors
  const authorRegex = /author:\s*"([^"]+)"/g;
  const authors = [...dataJs.matchAll(authorRegex)].map(m => m[1]);

  // Build posts array
  const maxLen = Math.max(slugs.length, titles.length, dates.length, contents.length);
  for (let i = 0; i < maxLen; i++) {
    posts.push({
      slug: slugs[i] || 'unknown',
      title: titles[i] || '',
      date: dates[i] || '',
      excerpt: excerpts[i] || '',
      tags: tagsList[i] || [],
      author: authors[i] || '',
      content: contents[i] || '',
    });
  }

  // Clean up extracted content - remove any JS code that got mixed in
  for (const post of posts) {
    if (post.content) {
      // Check if the content starts right after backtick, may contain preceding JS
      const contentStart = post.content.search(/^##/m);
      if (contentStart > 0 && contentStart < 100) {
        post.content = post.content.substring(contentStart);
      }
    }
  }

  if (posts.length === 0) {
    console.error('No posts found');
    process.exit(1);
  }

  console.log(`Found ${posts.length} posts total\n`);

  // Track all results
  let allPassed = true;
  let resultsByPost = {};

  for (const post of posts) {
    if (!post.content || post.content.trim() === '') {
      console.log(`## Post: ${post.slug} (${post.title})`);
      console.log('⚠️  Skipped — no content extracted\n');
      continue;
    }

    const keyword = extractKeyword(post.title);
    let keywordDisplay = keyword;

    // Special cases for Bangla posts
    const isBangla = /[\u0980-\u09FF]/.test(post.title);

    // A. TF-IDF Coverage
    const kwCount = countOccurrences(post.content, keyword);
    let tfidfOk = kwCount >= 5 || isBangla; // Bangla posts get pass since keyword extraction is English-focused
    let tfidfDetail = `${kwCount} occurrences`;
    if (!tfidfOk) {
      if (isBangla) {
        tfidfOk = null; // uncertain
        tfidfDetail = `${kwCount} occurrences (Bangla — keyword extraction may be inaccurate)`;
      } else {
        tfidfDetail = `${kwCount} occurrences (needs 5+)`;
      }
    }

    // B. Semantic Entity Coverage
    const missingEntities = checkEntities(post.content, post.title, post.slug);
    let entitiesOk = missingEntities.length === 0;
    let entitiesDetail = entitiesOk ? 'All key entities present' : `Missing: ${missingEntities.join(', ')}`;

    // C. Pillar-Cluster Alignment
    const pillarResult = checkPillarLink(post, posts);
    let pillarOk = pillarResult.ok;
    let pillarDetail = pillarResult.detail;

    // D. AEO/GEO Optimization
    const qHeadings = countQuestionHeadings(post.content);
    let aeoOk = qHeadings >= 2;
    let aeoDetail = `${qHeadings} question headings`;
    if (!aeoOk) aeoDetail += ' (needs 2+)';

    // E. Internal Linking
    const internalLinks = countInternalLinks(post.content);
    let linksOk = internalLinks >= 3;
    let linksDetail = `${internalLinks} total`;
    if (!linksOk) linksDetail += ' (needs 3+)';

    // F. Schema
    const schemaResult = checkSchemaReadiness(post);
    let schemaOk = schemaResult.ok;
    let schemaDetail = schemaResult.detail;

    // ── Report ──
    const checks = {
      'TF-IDF': { ok: tfidfOk, detail: tfidfDetail, key: keywordDisplay },
      'Entities': { ok: entitiesOk, detail: entitiesDetail },
      'Pillar Link': { ok: pillarOk, detail: pillarDetail },
      'AEO/GEO': { ok: aeoOk, detail: aeoDetail },
      'Internal Links': { ok: linksOk, detail: linksDetail },
      'Schema Ready': { ok: schemaOk, detail: schemaDetail },
    };

    resultsByPost[post.slug] = { title: post.title, checks };

    // Determine if post passes overall
    const failures = Object.entries(checks).filter(([_, v]) => v.ok === false);
    const warnings = Object.entries(checks).filter(([_, v]) => v.ok === null);
    const passed = failures.length === 0;

    if (!passed) allPassed = false;
  }

  // ── Generate Report ──
  // Show only posts that have failures (or all if all pass)
  const postsWithIssues = Object.entries(resultsByPost).filter(([_, p]) =>
    Object.values(p.checks).some(c => c.ok === false)
  );
  const postsClean = Object.entries(resultsByPost).filter(([_, p]) =>
    Object.values(p.checks).every(c => c.ok !== false)
  );

  if (postsWithIssues.length === 0) {
    console.log('✅ ALL POSTS PASS — no framework issues found.');
    return;
  }

  for (const [slug, data] of postsWithIssues) {
    console.log(`## Post: ${slug}`);
    console.log(`Title: ${data.title}`);
    console.log('| Check | Status | Details |');
    console.log('|-------|--------|---------|');
    for (const [checkName, checkData] of Object.entries(data.checks)) {
      let status;
      if (checkData.ok === true) status = '✅';
      else if (checkData.ok === null) status = '⚠️';
      else status = '❌';
      const detailKey = checkData.key ? `"${checkData.key}" — ` : '';
      console.log(`| ${checkName} | ${status} | ${detailKey}${checkData.detail} |`);
    }
    console.log('');

    // Fix instructions
    console.log('### Fix instructions:');
    for (const [checkName, checkData] of Object.entries(data.checks)) {
      if (checkData.ok === false) {
        switch (checkName) {
          case 'TF-IDF':
            console.log(`- 🔑 TF-IDF: Increase usage of keyword "${checkData.key}" to at least 5 occurrences across the content.`);
            break;
          case 'Entities':
            console.log(`- 🏷️ Entities: Add mentions of: ${checkData.detail.replace('Missing: ', '')}`);
            break;
          case 'Pillar Link':
            console.log(`- 🔗 Pillar Link: ${checkData.detail}`);
            break;
          case 'AEO/GEO':
            console.log(`- ❓ AEO/GEO: Add question-based H2 headings (How, What, Why, etc.) — need 2+ total.`);
            break;
          case 'Internal Links':
            console.log(`- 🔗 Internal Links: Add more internal links to /blog/, /services/, /locations/, /industries/ — need 3+ total.`);
            break;
          case 'Schema Ready':
            console.log(`- 📋 Schema: ${checkData.detail}`);
            break;
        }
      }
    }
    console.log('');
  }

  // Summary of clean posts
  if (postsClean.length > 0) {
    console.log(`\n✅ ${postsClean.length} posts passed all checks (no issues found).`);
  }
  console.log(`\n📊 Total: ${postsWithIssues.length} posts with issues, ${postsClean.length} clean.`);
}

main().catch(e => {
  console.error('Error:', e);
  process.exit(1);
});
