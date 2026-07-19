#!/usr/bin/env python3
"""
Content Framework Enforcer for kanokmiah.com.bd
Uses Node.js to reliably parse the ES module and export data as JSON.
"""
import json
import subprocess
import sys
import os
import re


def parse_with_node(filepath):
    """Use Node.js to dynamically import the JS module and extract post data."""
    script = r"""
const fs = require('fs');
const path = require('path');

// Read the file content
const code = fs.readFileSync(process.argv[1], 'utf-8');

// The file has `const posts = [...]` and `export default posts;`
// We need to evaluate it. Since it's ES module syntax but the project
// doesn't have "type": "module", we'll transform it for CommonJS eval.
// Strategy: find the post objects by parsing the JavaScript manually.
// Use regex to extract each post block between "  {" and "  },"/ "  }"

// Simpler: We'll parse the JS manually by tracking braces and backticks
const lines = code.split('\n');
const posts = [];

let i = 0;
while (i < lines.length) {
  const line = lines[i];
  // Look for post start: "  {" where next non-empty line has "slug:"
  if (line.trim() === '{') {
    let j = i + 1;
    while (j < lines.length && lines[j].trim() === '') j++;
    if (j < lines.length && lines[j].includes('slug:')) {
      // Extract post
      const post = {};
      let braceDepth = 1;
      let inBacktick = false;
      let k = i;
      let contentParts = [];
      
      while (k < lines.length && braceDepth > 0) {
        const l = lines[k];
        
        if (inBacktick) {
          // Inside backtick content
          const btIdx = l.indexOf('`');
          if (btIdx >= 0) {
            // Closing backtick
            const before = l.substring(0, btIdx);
            if (before.trim()) contentParts.push(before);
            inBacktick = false;
          } else {
            contentParts.push(l);
          }
          k++;
          continue;
        }
        
        // Check for backtick start
        if (l.includes('content:') && l.includes('`')) {
          const btIdx = l.indexOf('`');
          const afterBt = l.substring(btIdx + 1);
          if (afterBt.includes('`')) {
            // Same-line close
            const inner = afterBt.split('`')[0];
            if (inner.trim()) contentParts.push(inner);
          } else {
            inBacktick = true;
            if (afterBt.trim()) contentParts.push(afterBt);
          }
        }
        
        // Check for backtick start on its own line (content: \n`)
        if (l.trim() === 'content:') {
          if (k + 1 < lines.length && lines[k+1].trim() === '`') {
            inBacktick = true;
            k += 2;
            continue;
          }
        }
        
        if (!inBacktick) {
          braceDepth += (l.match(/\{/g) || []).length;
          braceDepth -= (l.match(/\}/g) || []).length;
        }
        
        // Extract fields (simple regex)
        const fieldMatch = l.match(/^\s*(\w+):\s*(.*)/);
        if (fieldMatch && !inBacktick) {
          const fieldName = fieldMatch[1];
          let fieldVal = fieldMatch[2].trim();
          
          if (fieldName === 'slug') {
            post.slug = fieldVal.replace(/['",]/g, '');
          } else if (fieldName === 'title') {
            post.title = fieldVal.replace(/^"|",?$/g, '');
          } else if (fieldName === 'date') {
            post.date = fieldVal.replace(/['",]/g, '');
          } else if (fieldName === 'author') {
            post.author = fieldVal.replace(/['",]/g, '');
          } else if (fieldName === 'excerpt') {
            // Might be multiline
            let excerpt = fieldVal;
            // Remove leading quote
            if (excerpt.startsWith('"')) excerpt = excerpt.substring(1);
            // Check if it ends on this line
            if (excerpt.endsWith('",') || excerpt.endsWith('"')) {
              excerpt = excerpt.replace(/",?$/, '');
            } else {
              // Multiline - skip ahead
              let m = k + 1;
              while (m < lines.length) {
                const ml = lines[m].trim();
                if (ml.endsWith('",') || ml.endsWith('"')) {
                  excerpt += ' ' + ml.replace(/",?$/, '');
                  k = m;
                  break;
                }
                excerpt += ' ' + ml;
                m++;
              }
            }
            post.excerpt = excerpt.replace(/\\s+/g, ' ').trim();
          } else if (fieldName === 'tags') {
            const tagsMatch = fieldVal.match(/\[(.*)\]/);
            if (tagsMatch) {
              post.tags = JSON.parse('[' + tagsMatch[1] + ']');
            }
          } else if (fieldName === 'metaTitle') {
            post.metaTitle = fieldVal.replace(/^"|",?$/g, '');
          } else if (fieldName === 'metaDescription') {
            let desc = fieldVal;
            if (desc.startsWith('"')) desc = desc.substring(1);
            if (desc.endsWith('",') || desc.endsWith('"')) {
              desc = desc.replace(/",?$/, '');
            } else {
              let m = k + 1;
              while (m < lines.length) {
                const ml = lines[m].trim();
                if (ml.endsWith('",') || ml.endsWith('"')) {
                  desc += ' ' + ml.replace(/",?$/, '');
                  k = m;
                  break;
                }
                desc += ' ' + ml;
                m++;
              }
            }
            post.metaDescription = desc.replace(/\s+/g, ' ').trim();
          } else if (fieldName === 'dateModified') {
            post.dateModified = fieldVal.replace(/['",]/g, '');
          } else if (fieldName === 'imagePlaceholder') {
            post.imagePlaceholder = fieldVal.replace(/['",]/g, '');
          } else if (fieldName === 'readTime') {
            post.readTime = fieldVal.replace(/['",]/g, '');
          }
        }
        
        k++;
      }
      
      // Save content (already collected)
      if (contentParts.length > 0) {
        post.content = contentParts.join('\n');
      }
      
      if (post.slug) {
        posts.push(post);
      }
      
      i = k;
      continue;
    }
  }
  i++;
}

// Output as JSON
console.log(JSON.stringify(posts, null, 2));
"""
    result = subprocess.run(
        ['node', '-e', script, filepath],
        capture_output=True, text=True, timeout=60
    )
    if result.returncode != 0:
        print("Node.js error:", result.stderr[:500], file=sys.stderr)
        return []
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as e:
        print("JSON parse error:", str(e), file=sys.stderr)
        print("stdout length:", len(result.stdout), file=sys.stderr)
        print("First 200:", result.stdout[:200], file=sys.stderr)
        return []


# Fallback: Pure Python regex-based parser if Node.js fails
def parse_with_python(filepath):
    """Python regex-based parser as fallback."""
    with open(filepath, 'r', encoding='utf-8') as f:
        raw = f.read()
    
    # Find all post blocks by slug: "..." pattern with context
    # Strategy: find all slug positions, then extract the block between
    # the opening { and the correct closing } that matches the nested structure
    
    slug_pattern = re.compile(r'^\s{4}slug:\s*"([^"]+)"', re.MULTILINE)
    posts = []
    
    for m in slug_pattern.finditer(raw):
        slug = m.group(1)
        start = raw.rfind('{', 0, m.start())
        if start < 0:
            continue
        
        # Now find the matching closing } 
        depth = 0
        in_backtick = False
        end = start
        while end < len(raw):
            c = raw[end]
            if in_backtick:
                if c == '`':
                    # Check it's not escaped
                    if end == 0 or raw[end-1] != '\\':
                        in_backtick = False
            else:
                if c == '`':
                    # Check if preceded by content: or similar
                    in_backtick = True
                if c == '{':
                    depth += 1
                elif c == '}':
                    depth -= 1
                    if depth == 0:
                        break
            end += 1
        
        post_text = raw[start:end+1]
        
        # Parse fields from post_text
        post = {'slug': slug}
        
        # Extract simple fields
        simple_fields = ['title', 'date', 'author', 'dateModified', 'readTime']
        for field in simple_fields:
            fm = re.search(rf'^\s*{field}:\s*"([^"]*)"', post_text, re.MULTILINE)
            if fm:
                post[field] = fm.group(1)
        
        # Excerpt (can be multiline)
        em = re.search(r'^\s*excerpt:\s*\n?\s*"((?:[^"\\]|\\.)*)"', post_text, re.MULTILINE | re.DOTALL)
        if em:
            post['excerpt'] = em.group(1).replace('\n', ' ').strip()
        
        # metaTitle
        mtm = re.search(r'^\s*metaTitle:\s*"([^"]*)"', post_text, re.MULTILINE)
        if mtm:
            post['metaTitle'] = mtm.group(1)
        
        # metaDescription (multiline)
        mdm = re.search(r'^\s*metaDescription:\s*\n?\s*"((?:[^"\\]|\\.)*)"', post_text, re.MULTILINE | re.DOTALL)
        if mdm:
            post['metaDescription'] = mdm.group(1).replace('\n', ' ').strip()
        
        # Tags
        tm = re.search(r'^\s*tags:\s*\[([^\]]*)\]', post_text, re.MULTILINE)
        if tm:
            tags_str = tm.group(1)
            tags = re.findall(r'"([^"]+)"', tags_str)
            post['tags'] = tags
        
        # Content (backtick template literal)
        # Find content: and extract between opening and closing backticks
        cm = re.search(r'^\s*content:\s*\n?`\n(.*?)\n\s*`,\s*$', post_text, re.DOTALL | re.MULTILINE)
        if not cm:
            cm = re.search(r'^\s*content:\s*\n?`\n(.*?)\n\s*`\s*$', post_text, re.DOTALL | re.MULTILINE)
        if not cm:
            cm = re.search(r'^\s*content:\s*\n?`\n(.*?)`,\s*$', post_text, re.DOTALL | re.MULTILINE)
        if not cm:
            cm = re.search(r'^\s*content:\s*\n?`\n(.*?)`\s*$', post_text, re.DOTALL | re.MULTILINE)
        # Broadest: just find content between backticks
        if not cm:
            cm = re.search(r'content:\s*`\n?(.*?)\n`[,\s]', post_text, re.DOTALL)
        if cm:
            post['content'] = cm.group(1)
        else:
            # Absolute fallback: find between first ` after content: and the next `
            start_idx = post_text.find('content:')
            if start_idx >= 0:
                bt_start = post_text.find('`', start_idx)
                if bt_start >= 0:
                    bt_end = post_text.find('`', bt_start + 1)
                    if bt_end > bt_start:
                        # Check if there are more backticks (take the last one)
                        last_bt = post_text.rfind('`', bt_start + 1, len(post_text) - 2)
                        if last_bt > bt_start:
                            bt_end = last_bt
                        post['content'] = post_text[bt_start+1:bt_end]
        
        posts.append(post)
    
    return posts


# Helper functions for checking
def extract_primary_keyword(title):
    if not title:
        return None
    title_lower = title.lower().strip()
    
    # For Bengali titles, extract the first meaningful segment
    bengali = bool(re.search(r'[\u0980-\u09FF]', title_lower))
    if bengali:
        # Extract text BEFORE "seo:" (this is the main topic)
        m = re.search(r'^([\u0980-\u09FF\s-]+?)\s+seo[ঃ:]', title_lower)
        if m:
            kw = m.group(1).strip()
            if kw and 2 <= len(kw) <= 60:
                return kw[:60]
        # Then try text after "SEO:"
        m = re.search(r'seo[ঃ:]\s*([\u0980-\u09FFa-zA-Z\s-]+)', title_lower)
        if m:
            kw = m.group(1).strip()
            kw = re.sub(r'\s+(গাইড|কৌশল|কীভাবে).*$', '', kw)
            if kw and 2 <= len(kw) <= 60:
                return kw[:60]
        # Just first Bengali word cluster
        m = re.search(r'^([\u0980-\u09FF\s-]+)', title_lower)
        if m:
            kw = m.group(1).strip()
            if kw and 2 <= len(kw) <= 60:
                return kw[:60]
        words = title_lower.split()
        if words:
            return words[0][:60]
    
    # English patterns
    patterns = [
        (r'SEO for ([a-zA-Z\s-]+)', 1),
        (r'Complete ([a-zA-Z\s-]+) Guide', 1),
        (r'([a-zA-Z\s-]+?)\s+(Tips|Strategies|Techniques|Checklist|Guide)', 1),
        (r'Why ([a-zA-Z\s-]+?) (Needs|Should|Is|Are)', 1),
        (r'^(Best|Top|Ultimate) ([a-zA-Z\s-]+)', 2),
        (r'How to ([a-zA-Z\s-]+)', 1),
        (r'What is ([a-zA-Z\s-]+)', 1),
        (r'([a-zA-Z\s-]+?)\s+in Bangladesh', 1),
        (r'([a-zA-Z\s-]+?)\s+for Bangladesh', 1),
    ]
    
    for pattern, group in patterns:
        m = re.search(pattern, title_lower)
        if m:
            kw = m.group(group).strip()
            kw = re.sub(r'\s+(in|for|of|at|the|on|through|with)\s+.*$', '', kw)
            if 3 <= len(kw) <= 50:
                return kw
    
    # Fallback: take first 3 meaningful words (English only)
    words = [w for w in title_lower.split() if len(w) > 2 and not w.startswith('&')]
    if words:
        return ' '.join(words[:3])
    return title_lower.split()[0] if title_lower.split() else title_lower[:60]


def count_keyword(content, keyword):
    if not content or not keyword:
        return 0
    return content.lower().count(keyword.lower().strip())


def check_internal_links(content):
    if not content:
        return 0, []
    # HTML-style links: href="/path"
    html_links = re.findall(r'href="(/[^"]+)"', content)
    # Markdown-style links: [text](/path)
    md_links = re.findall(r'\]\((/[^)]+)\)', content)
    all_links = html_links + md_links
    real = [l for l in all_links if l != '#' and not l.startswith('//')]
    # Remove duplicates while preserving order
    seen = set()
    unique = []
    for l in real:
        # Normalize by removing trailing slash
        normalized = l.rstrip('/')
        if normalized not in seen:
            seen.add(normalized)
            unique.append(l)
    return len(unique), unique


def count_question_headings(content):
    if not content:
        return 0, []
    headings = re.findall(
        r'^#{2,4}\s+(How|What|Why|When|Where|Can|Do|Is|Are|Does|Did|Will|Would|Should|Could|Has|Have)\b.*$',
        content, re.MULTILINE | re.IGNORECASE
    )
    full = []
    for m in re.finditer(
        r'^#{2,4}\s+((How|What|Why|When|Where|Can|Do|Is|Are|Does|Did|Will|Would|Should|Could|Has|Have)\b.*)$',
        content, re.MULTILINE | re.IGNORECASE
    ):
        full.append(m.group(1).strip())
    return len(headings), full


def check_entities(content, post):
    if not content:
        return [], []
    content_lower = content.lower()
    title_lower = (post.get('title', '') or '').lower()
    present = []
    missing = []
    if 'bangladesh' in content_lower or 'bangladeshi' in content_lower:
        present.append('🇧🇩 Bangladesh')
    else:
        missing.append('🇧🇩 Bangladesh')
    if 'dhaka' in content_lower:
        present.append('📍 Dhaka')
    service_checks = [
        ('seo', '🔧 SEO'),
        ('local seo', '📍 Local SEO'),
        ('technical seo', '⚙️ Technical SEO'),
        ('link building', '🔗 Link Building'),
        ('content market', '📝 Content Marketing'),
        ('google business', '🔍 Google Business'),
        ('mobile', '📱 Mobile'),
        ('keyword', '🔑 Keyword Research'),
        ('schema', '🏷️ Schema'),
        ('ecommerce', '🛒 E-commerce'),
    ]
    title_m = ' ' + title_lower + ' '
    for kw, entity in service_checks:
        if kw in title_m:
            kw_clean = kw.strip()
            if kw_clean in content_lower:
                if entity not in present:
                    present.append(entity)
            else:
                if entity not in missing:
                    missing.append(entity)
    return missing, present


def check_pillar_link(content, tags, slug):
    if not content:
        return False, None
    content_lower = content.lower()
    service_links = re.findall(r'/services/[a-z0-9-]+', content_lower)
    if service_links:
        return True, service_links[0]
    location_links = re.findall(r'/locations/[a-z0-9-]+', content_lower)
    if location_links:
        return True, location_links[0]
    return False, None


def check_schema_readiness(post):
    missing = []
    for field in ['title', 'excerpt', 'date', 'dateModified', 'author']:
        if not post.get(field):
            missing.append(field)
    return (len(missing) == 0), missing


def run_checks(post):
    slug = post.get('slug', 'unknown')
    title = post.get('title', '')
    content = post.get('content', '')
    tags = post.get('tags', [])
    results = {}
    keyword = extract_primary_keyword(title)
    keyword_occurrences = count_keyword(content, keyword) if keyword else 0
    results['tfidf'] = {'keyword': keyword, 'occurrences': keyword_occurrences, 'flag': keyword_occurrences < 5,
        'detail': "'" + str(keyword) + "' appears " + str(keyword_occurrences) + " time(s)"}
    missing_entities, present_entities = check_entities(content, post)
    results['entities'] = {'missing': missing_entities, 'flag': len(missing_entities) > 0,
        'detail': 'Missing: ' + (', '.join(missing_entities) if missing_entities else 'None')}
    has_pillar_link, pillar_url = check_pillar_link(content, tags, slug)
    results['pillar'] = {'has_link': has_pillar_link, 'pillar_url': pillar_url, 'flag': not has_pillar_link,
        'detail': 'Links to: ' + (pillar_url if pillar_url else 'No pillar link found')}
    q_count, q_headings = count_question_headings(content)
    results['aeo'] = {'count': q_count, 'flag': q_count < 2, 'detail': str(q_count) + ' question heading(s)'}
    link_count, links = check_internal_links(content)
    results['internal_links'] = {'count': link_count, 'flag': link_count < 3, 'detail': str(link_count) + ' internal link(s)'}
    schema_ready, schema_missing = check_schema_readiness(post)
    results['schema'] = {'ready': schema_ready, 'missing': schema_missing, 'flag': not schema_ready,
        'detail': 'All fields set' if schema_ready else 'Missing: ' + ', '.join(schema_missing)}
    return results


def generate_report(slug, title, results):
    lines = []
    lines.append("## Post: " + slug)
    lines.append("**Title:** " + (title or ''))
    lines.append("")
    lines.append("| Check | Status | Details |")
    lines.append("|-------|--------|---------|")
    r = results['tfidf']
    lines.append("| TF-IDF: `" + str(r['keyword']) + "` | " + ('✅' if not r['flag'] else '❌') + " | " + r['detail'] + " |")
    r = results['entities']
    lines.append("| Entities | " + ('✅' if not r['flag'] else '❌') + " | " + r['detail'] + " |")
    r = results['pillar']
    lines.append("| Pillar Link | " + ('✅' if not r['flag'] else '❌') + " | " + r['detail'] + " |")
    r = results['aeo']
    lines.append("| AEO/GEO | " + ('✅' if not r['flag'] else '❌') + " | " + r['detail'] + " |")
    r = results['internal_links']
    lines.append("| Internal Links | " + ('✅' if not r['flag'] else '❌') + " | " + r['detail'] + " |")
    r = results['schema']
    lines.append("| Schema Ready | " + ('✅' if not r['flag'] else '❌') + " | " + r['detail'] + " |")
    lines.append("")
    fixes = []
    if results['tfidf']['flag']:
        fixes.append("- **TF-IDF**: Increase usage of primary keyword '" + str(results['tfidf']['keyword']) + "' to at least 5 occurrences (currently " + str(results['tfidf']['occurrences']) + ")")
    if results['entities']['flag']:
        fixes.append("- **Entities**: Add missing entities: " + ', '.join(results['entities']['missing']))
    if results['pillar']['flag']:
        fixes.append("- **Pillar Link**: Add link to the relevant pillar/service page (e.g., /services/, /locations/)")
    if results['aeo']['flag']:
        fixes.append("- **AEO/GEO**: Add at least 2 question-based headings (How, What, Why, etc.) — currently " + str(results['aeo']['count']))
    if results['internal_links']['flag']:
        fixes.append("- **Internal Links**: Add more internal links (currently " + str(results['internal_links']['count']) + ", minimum 3)")
    if results['schema']['flag']:
        fixes.append("- **Schema**: Missing fields: " + ', '.join(results['schema']['missing']))
    if fixes:
        lines.append("### Fix instructions:")
        for fix in fixes:
            lines.append(fix)
    else:
        lines.append("### Fix instructions:")
        lines.append("✅ All checks pass — no fixes needed.")
    lines.append("")
    return '\n'.join(lines)


def main():
    with open('/tmp/changed_slugs.txt', 'r') as f:
        changed_slugs = set(line.strip() for line in f if line.strip())
    
    print("🔍 Found " + str(len(changed_slugs)) + " changed slugs in last 48 hours", flush=True)
    print("📂 Parsing data.js...", flush=True)
    
    # Try Node.js first
    posts = parse_with_node('/root/kanok-miahit/src/app/blog/data.js')
    
    if len(posts) < 50:
        print("⚠️  Node.js parser got " + str(len(posts)) + " posts, trying Python fallback...", flush=True)
        posts = parse_with_python('/root/kanok-miahit/src/app/blog/data.js')
    
    print("📊 Parsed " + str(len(posts)) + " total posts", flush=True)
    
    if len(posts) < 50:
        print("⚠️  Too few posts parsed! Debugging sample:", flush=True)
        for p in posts[:3]:
            slug = p.get('slug', 'N/A')
            content_len = len(p.get('content', ''))
            print(f"  Slug: '{slug}', Content: {content_len} chars", flush=True)
        sys.exit(1)
    
    posts_by_slug = {p.get('slug'): p for p in posts if p.get('slug')}
    
    found_slugs = set(posts_by_slug.keys())
    missing_slugs = changed_slugs - found_slugs
    if missing_slugs:
        print("⚠️  " + str(len(missing_slugs)) + " slugs not found: " + ', '.join(list(missing_slugs)[:10]), flush=True)
    
    slugs_to_check = changed_slugs & found_slugs
    print("🔎 Running framework checks on " + str(len(slugs_to_check)) + " posts...", flush=True)
    print("", flush=True)
    
    all_pass = True
    flag_counts = {'tfidf': 0, 'entities': 0, 'pillar': 0, 'aeo': 0, 'internal_links': 0, 'schema': 0}
    flagged_posts = 0
    reports = []
    
    for slug in sorted(slugs_to_check):
        post = posts_by_slug[slug]
        results = run_checks(post)
        report = generate_report(slug, post.get('title', ''), results)
        reports.append(report)
        has_flags = any(r['flag'] for r in results.values())
        if has_flags:
            all_pass = False
            flagged_posts += 1
            for check_name in flag_counts:
                if results[check_name]['flag']:
                    flag_counts[check_name] += 1
    
    for report in reports:
        print(report, flush=True)
        print("---", flush=True)
    
    print("", flush=True)
    print("=" * 60, flush=True)
    print("📍 FRAMEWORK ENFORCEMENT SUMMARY", flush=True)
    print("=" * 60, flush=True)
    print("Period: Last 48 hours", flush=True)
    print("Checked: " + str(len(slugs_to_check)) + " modified posts", flush=True)
    print("", flush=True)
    print("❌ Posts with flags: " + str(flagged_posts) + "/" + str(len(slugs_to_check)), flush=True)
    print("   - TF-IDF too thin (<5 occurrences): " + str(flag_counts['tfidf']), flush=True)
    print("   - Missing entities: " + str(flag_counts['entities']), flush=True)
    print("   - No pillar link: " + str(flag_counts['pillar']), flush=True)
    print("   - AEO/GEO low (<2 question headings): " + str(flag_counts['aeo']), flush=True)
    print("   - Too few internal links (<3): " + str(flag_counts['internal_links']), flush=True)
    print("   - Schema incomplete: " + str(flag_counts['schema']), flush=True)
    print("", flush=True)
    
    if all_pass:
        print("✅ ALL CHECKS PASSED — no fixes needed!", flush=True)
    else:
        print("⚠️  " + str(flagged_posts) + " posts need attention. See detailed results above.", flush=True)


if __name__ == '__main__':
    main()
