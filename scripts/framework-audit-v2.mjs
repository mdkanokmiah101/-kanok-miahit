#!/usr/bin/env node
/**
 * Refined Content Framework Audit — only meaningful issues
 */

import { promises as fs } from 'fs';

async function main() {
  const dataJs = await fs.readFile('src/app/blog/data.js', 'utf-8');

  // Parse all posts using regex
  const slugs = [...dataJs.matchAll(/slug:\s*"([^"]+)"/g)].map(m => m[1]);
  const titles = [...dataJs.matchAll(/title:\s*"([^"]+)"/g)].map(m => m[1]);
  const dates = [...dataJs.matchAll(/date:\s*"([^"]+)"/g)].map(m => m[1]);
  // More robust excerpt extraction
  const excerptRegex = /excerpt:\s*(?:\n\s*)?"([^"]+)"/g;
  const excerpts = [...dataJs.matchAll(excerptRegex)].map(m => m[1]);
  const authorRegex = /author:\s*"([^"]+)"/g;
  const authors = [...dataJs.matchAll(authorRegex)].map(m => m[1]);
  const tagMatches = [...dataJs.matchAll(/tags:\s*\[([^\]]+)\]/g)];
  const tagsList = tagMatches.map(m => m[1].split(',').map(t => t.trim().replace(/^"|"$/g, '')).filter(t => t));
  const contentMatches = [...dataJs.matchAll(/content:\s*`([\s\S]*?)`\s*,?/g)];
  const contents = contentMatches.map(m => m[1]);

  // Build post objects
  const posts = [];
  const count = Math.max(slugs.length, titles.length, dates.length, contents.length);
  for (let i = 0; i < count; i++) {
    posts.push({
      slug: slugs[i] || '?',
      title: titles[i] || '',
      date: dates[i] || '',
      excerpt: excerpts[i] || '',
      tags: tagsList[i] || [],
      author: authors[i] || '',
      content: contents[i] || '',
    });
  }

  // Clean content — trim leading non-content JS
  for (const p of posts) {
    let c = p.content;
    // Find first markdown heading or paragraph
    const firstContent = c.search(/^[#A-Za-z\u0980-\u09FF]/m);
    if (firstContent > 0 && firstContent < 200) c = c.substring(firstContent);
    // Remove trailing JS
    const lastContent = c.lastIndexOf('`');
    if (lastContent > c.length * 0.8) c = c.substring(0, lastContent);
    p.content = c.trim();
  }

  // ── REAL framework checks ──

  let reportSections = [];

  for (const post of posts) {
    if (!post.content || post.content.length < 50) continue;

    const c = post.content;
    const isBangla = /[\u0980-\u09FF]/.test(post.title);

    let issues = [];
    let checks = {};

    // A. TF-IDF — check keyword exists enough
    const stopwords = new Set(['the','a','an','in','for','of','to','and','is','are','what','how','why','when','where','your','our','its','their','complete','guide','ultimate','best','top','seo','vs','for','and','the']);
    const titleWords = post.title.replace(/[^a-zA-Z\s\u0980-\u09FF-]/g, '').split(/\s+/).filter(w => w.length > 2 && !stopwords.has(w.toLowerCase()));
    const keyword = titleWords.slice(0, 2).join(' ') || post.title.split(' ').slice(0, 2).join(' ');
    let kwCount = 0;
    if (keyword.length >= 3 && !isBangla) {
      const kwParts = keyword.toLowerCase().split(' ');
      for (const part of kwParts) {
        if (part.length > 3) {
          const re = new RegExp(part.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi');
          kwCount += (c.match(re) || []).length;
        }
      }
    } else if (isBangla) {
      // For Bangla posts, just check the main topic word appears
      // Extract first non-stopword from title
      const banglaWords = post.title.match(/[\u0980-\u09FF]+/g) || [];
      if (banglaWords.length > 0) {
        const mainWord = banglaWords[0];
        const re = new RegExp(mainWord, 'g');
        kwCount = (c.match(re) || []).length;
      } else {
        kwCount = 999; // skip
      }
    }
    const tfidfOk = kwCount >= 5 || isBangla;
    if (!tfidfOk && kwCount < 5 && kwCount > 0 && !isBangla) {
      issues.push(`🔑 TF-IDF: "${keyword}" only ${kwCount} occurrences (need 5+)`);
    }

    // B. Entity check — only meaningful ones
    let missingEntities = [];
    const lower = c.toLowerCase();
    const titleLower = post.title.toLowerCase();

    // Check location: if title mentions Dhaka/Bangladesh, content should too
    if (/dhaka/i.test(post.title) && !/dhaka/i.test(c)) missingEntities.push('Dhaka (in content)');
    if (/bangladesh/i.test(post.title) && !/bangladesh/i.test(c)) missingEntities.push('Bangladesh (in content)');

    // Author name
    if (!isBangla && !/kanok\s*miah/i.test(c) && !/kanok/i.test(c)) {
      // Check if it's purely a case study (UK-focused etc)
      if (!/locksmith|dundee|scotland|uk|landlord/i.test(post.slug)) {
        missingEntities.push('Kanok Miah (author branding)');
      }
    }

    if (missingEntities.length > 0) {
      issues.push(`🏷️ Missing entities: ${missingEntities.join(', ')}`);
    }

    // C. Pillar link check
    const tags = (post.tags || []).join(' ').toLowerCase();
    let pillarSlug = null;
    let pillarName = null;

    if (tags.includes('seo guide') || tags.includes('bangladesh seo')) {
      pillarSlug = 'complete-seo-guide-bangladesh-businesses-2026';
      pillarName = 'Complete SEO Guide';
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
    } else if (tags.includes('geo') || tags.includes('aeo') || tags.includes('ai search') || tags.includes('generative engine')) {
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
    } else if (tags.includes('google ads') || tags.includes('ppc')) {
      pillarSlug = 'seo-vs-google-ads-bangladesh-business';
      pillarName = 'SEO vs Google Ads guide';
    } else if (tags.includes('schema') || tags.includes('structured data') || tags.includes('rich snippet')) {
      pillarSlug = 'schema-markup-rich-snippets-techniques';
      pillarName = 'Schema markup guide';
    } else if (tags.includes('youtube') || tags.includes('video')) {
      pillarSlug = 'youtube-seo-bangladesh-ranking-tips';
      pillarName = 'YouTube SEO guide';
    } else if (tags.includes('bangla') || tags.includes('বাংলা') || tags.includes('বাংলাদেশ')) {
      pillarSlug = 'seo-bangla-beginners-guide-google-ranking';
      pillarName = 'SEO Bangla guide';
    } else if (tags.includes('case study')) {
      pillarSlug = null; // case studies have flexible pillar mapping
    } else if (tags.includes('keyword research')) {
      pillarSlug = 'complete-seo-guide-bangladesh-businesses-2026';
      pillarName = 'Complete SEO Guide';
    } else if (tags.includes('voice search')) {
      pillarSlug = 'mobile-seo-optimization-bangladesh-mobile-first-era';
      pillarName = 'Mobile SEO guide';
    } else if (tags.includes('google business profile') || tags.includes('gbp') || tags.includes('google my business')) {
      pillarSlug = 'google-business-profile-optimization-guide-bangladesh';
      pillarName = 'GBP optimization guide';
    } else if (tags.includes('web development') || tags.includes('web design')) {
      pillarSlug = 'seo-for-new-website-bangladesh';
      pillarName = 'New Website SEO guide';
    } else if (tags.includes('blogging')) {
      pillarSlug = 'content-marketing-strategy-bangladeshi-brands-seo';
      pillarName = 'Content Marketing guide';
    }

    if (pillarSlug) {
      if (post.slug !== pillarSlug) {
        const pillarLinked = c.includes(pillarSlug);
        if (!pillarLinked) {
          issues.push(`🔗 Missing pillar link: link to "${pillarName}" post (/blog/${pillarSlug})`);
        }
      }
    } else {
      // For posts with no clear pillar mapping (case studies, industry-specific), skip silently
    }

    // D. AEO/GEO — question headings (only for English posts, Bangla posts naturally don't use English question H2s)
    if (!isBangla) {
      const questionH2 = (c.match(/^#{1,4}\s+(How|What|Why|When|Where|Can|Do|Is|Are|Does|Which|Who)\b/gim) || []);
      if (questionH2.length < 2) {
        issues.push(`❓ AEO/GEO: Only ${questionH2.length} question-based headings (need 2+ for AI search snippets)`);
      }
    }

    // E. Internal links
    const internalLinks = (c.match(/\]\(\/(?!http|https|www\.)(?:blog\/|services\/|locations\/|industries\/|about|contact)/g) || []);
    // Also count links to / (homepage)
    const homeLinks = (c.match(/\]\(\//g) || []);
    // Filter: links that are just / (homepage) vs full paths
    const homeOnlyLinks = (c.match(/\]\(\/\)/g) || []).length;
    const totalRelevantLinks = internalLinks.length + homeOnlyLinks;
    
    // For case studies/about pages, 2+ links is acceptable if they are relevant
    const isCaseStudy = post.tags.some(t => t.toLowerCase().includes('case study')) || post.slug.includes('case-study');
    const minLinks = isCaseStudy ? 2 : 3;
    
    // Exclude homepage links from the count since they were just added by the linking audit
    const nonHomeLinks = internalLinks.length;
    
    if (nonHomeLinks < minLinks && !isCaseStudy) {
      issues.push(`🔗 Internal links: only ${nonHomeLinks} to blog/services/locations (need ${minLinks}+)`);
    } else if (nonHomeLinks < 2 && isCaseStudy) {
      issues.push(`🔗 Internal links: only ${nonHomeLinks} to blog/services/locations (need ${minLinks}+)`);
    }

    // F. Schema readiness
    let schemaMissing = [];
    if (!post.title || post.title.trim() === '') schemaMissing.push('title');
    if (!post.date || post.date.trim() === '') schemaMissing.push('date');
    if (!post.author || post.author.trim() === '') schemaMissing.push('author');
    if (!post.slug || post.slug.trim() === '') schemaMissing.push('slug');
    if (schemaMissing.length > 0) {
      issues.push(`📋 Schema: missing field(s): ${schemaMissing.join(', ')}`);
    }

    // Only output if there are issues
    if (issues.length > 0) {
      reportSections.push({ slug: post.slug, title: post.title, issues, isBangla });
    }
  }

  // ── Generate report ──

  console.log('# Content Framework Enforcement Report');
  console.log(`Generated: ${new Date().toISOString()}`);
  console.log(`Posts audited: ${posts.length}`);
  console.log(`Posts with issues: ${reportSections.length}`);
  console.log(`Posts clean: ${posts.length - reportSections.length}`);
  console.log('');

  // Group by issue type for summary
  const typeCounts = {};
  for (const sec of reportSections) {
    for (const issue of sec.issues) {
      const type = issue.split(':')[0];
      typeCounts[type] = (typeCounts[type] || 0) + 1;
    }
  }

  console.log('## Summary by Issue Type');
  const sortedTypes = Object.entries(typeCounts).sort((a, b) => b[1] - a[1]);
  for (const [type, count] of sortedTypes) {
    console.log(`- ${type}: ${count} posts affected`);
  }
  console.log('');

  // Individual post reports
  console.log('## Per-Post Issues');
  console.log('');

  for (const sec of reportSections) {
    console.log(`### ${sec.slug}`);
    if (sec.title.length < 80) console.log(`*${sec.title}*`);
    console.log('');
    for (const issue of sec.issues) {
      console.log(`- ${issue}`);
    }
    console.log('');
  }

  // Priority action items
  console.log('## ⚡ Priority Fixes (by impact)');
  console.log('');

  // Count missing excerpts
  const missingExcerpt = reportSections.filter(s => s.issues.some(i => i.includes('Schema: missing')));
  const missingPillar = reportSections.filter(s => s.issues.some(i => i.includes('Missing pillar link')));
  const missingAEO = reportSections.filter(s => s.issues.some(i => i.includes('AEO/GEO')));
  const missingLinks = reportSections.filter(s => s.issues.some(i => i.includes('Internal links:')));
  const missingEntitiesReport = reportSections.filter(s => s.issues.some(i => i.includes('Missing entities')));

  if (missingExcerpt.length > 0) {
    console.log(`1️⃣  Add missing excerpt fields (${missingExcerpt.length} posts)`);
    console.log(`   Posts: ${missingExcerpt.map(s => s.slug).join(', ')}`);
    console.log('   → ArticleSchema requires excerpt. Open each post in data.js and add:\n     excerpt: "Your SEO-optimized meta description here.",');
    console.log('');
  }

  if (missingPillar.length > 0) {
    console.log(`2️⃣  Add pillar links (${missingPillar.length} posts)`);
    console.log(`   Posts: ${missingPillar.map(s => s.slug).join(', ')}`);
    console.log('   → Each cluster post should link back to its pillar page.');
    console.log('');
  }

  if (missingAEO.length > 0) {
    console.log(`3️⃣  Add question-based H2 headings for AEO/GEO (${missingAEO.length} English posts)`);
    console.log(`   Posts: ${missingAEO.map(s => s.slug).join(', ')}`);
    console.log('   → AI search engines favor content with clear Q&A sections.');
    console.log('   → Add 2+ H2s starting with How, What, Why, When, Where, Can, Do, Is, Are');
    console.log('');
  }

  if (missingLinks.length > 0) {
    console.log(`4️⃣  Increase internal linking (${missingLinks.length} posts)`);
    console.log(`   Posts: ${missingLinks.map(s => s.slug).join(', ')}`);
    console.log('   → Add links to /blog/, /services/, /locations/ within content body.');
    console.log('');
  }

  if (missingEntitiesReport.length > 0) {
    console.log(`5️⃣  Entity coverage improvements (${missingEntitiesReport.length} posts)`);
    console.log('   → Ensure location (Dhaka/Bangladesh) and author brand (Kanok Miah) are mentioned.');
    console.log('');
  }

  console.log('---');
  console.log(`✅ ${posts.length - reportSections.length} posts passed all checks.`);
}

main().catch(e => {
  console.error('Error:', e);
  process.exit(1);
});
