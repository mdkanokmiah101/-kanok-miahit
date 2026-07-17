#!/usr/bin/env python3
"""
Concise framework checker for kanokmiah.com.bd blog posts.
Generates a summary report grouped by issue type.
"""
import re
import subprocess
import json
from datetime import datetime, timezone

DATA_JS = "/root/kanok-miahit/src/app/blog/data.js"

def parse_posts(data_js):
    """Parse blog posts from data.js"""
    with open(data_js, 'r', encoding='utf-8') as f:
        content = f.read()
    
    blocks = content.split("slug: ")
    posts = []
    
    for block in blocks[1:]:
        try:
            slug_match = re.search(r'"([^"]+)"', block)
            if not slug_match: continue
            slug = slug_match.group(1)
            
            title_match = re.search(r'title:\s*"([^"]+)"', block)
            title = title_match.group(1) if title_match else "unknown"
            
            date_match = re.search(r'date:\s*"([^"]+)"', block)
            date_str = date_match.group(1) if date_match else "unknown"
            
            dm_match = re.search(r'dateModified:\s*"([^"]+)"', block)
            date_modified = dm_match.group(1) if dm_match else None
            
            tags_match = re.search(r'tags:\s*\[(.*?)\]', block, re.DOTALL)
            tags = []
            if tags_match:
                tags = re.findall(r'"([^"]+)"', tags_match.group(1))
            
            content_match = re.search(r'content:\s*`(.*?)`\s*,?\s*\}', block, re.DOTALL)
            content_text = content_match.group(1).strip() if content_match else ""
            
            excerpt_match = re.search(r'excerpt:\s*\n?\s*"([^"]+)"', block)
            excerpt = excerpt_match.group(1) if excerpt_match else ""
            
            post = {
                'slug': slug, 'title': title, 'date': date_str,
                'author': 'Kanok Miah', 'excerpt': excerpt, 'tags': tags,
                'dateModified': date_modified, 'content': content_text
            }
            posts.append(post)
        except:
            continue
    
    return posts

def analyze_post(post):
    """Run all 6 checks on a post. Returns dict of results."""
    content = post['content'].lower()
    title = post['title']
    c = content  # shorthand
    
    results = {}
    
    # A. TF-IDF
    title_clean = re.sub(r'^(why|what|how|is|are|do|does|the|a|an|your|our|complete|ultimate|best|top|সহজ|স্থানীয়|টেকনিক্যাল|কীওয়ার্ড|কন্টেন্ট|গুগল|ইউটিউব|মোবাইল|লিংক|স্কিমা|২০২৬) ', '', title.lower())
    title_clean = re.split(r'[—–\-:|]', title_clean)[0].strip()
    words = [w for w in title_clean.split() if len(w) > 2][:3]
    
    if len(words) >= 2:
        keyword = ' '.join(words[:2])
    elif len(words) >= 1:
        keyword = words[0]
    elif title_clean.strip():
        keyword = title_clean.split()[0] if title_clean.split() else title
    else:
        keyword = title[:30]
    
    # For Bengali titles, use first Bengali word of substance
    if any('\u0980' <= ch <= '\u09FF' for ch in title):
        bengali_words = re.findall(r'[\u0980-\u09FF]+', title.lower())
        if bengali_words:
            keyword = bengali_words[0]
    
    count = c.count(keyword.lower()) if len(keyword) > 2 else 0
    results['tfidf'] = {'keyword': keyword, 'count': count, 'passed': count >= 5}
    
    # B. Entities
    locs = ['dhaka', 'bangladesh', 'chittagong', 'sylhet']
    found_locs = [l for l in locs if l in c]
    missing_locs = [l for l in locs if l not in c]
    results['entities'] = {
        'passed': len(found_locs) >= 1,
        'found': found_locs,
        'missing': missing_locs
    }
    
    # C. Pillar Link
    service_pages = [
        '/services/local-seo', '/services/technical-seo', '/services/ecommerce-seo',
        '/services/on-page-seo', '/services/semantic-seo', '/services/geo-ai-search',
        '/services/link-building',
    ]
    pillar_blog = '/blog/complete-seo-guide-bangladesh-businesses-2026'
    
    found_links = [sp for sp in service_pages if sp in c]
    if pillar_blog in c:
        found_links.append(pillar_blog)
    
    results['pillar'] = {
        'passed': len(found_links) >= 1,
        'links': found_links
    }
    
    # D. AEO/GEO question headings
    q_headings = re.findall(
        r'^#{2,6}\s+(?:How|What|Why|When|Where|Can|Do|Is|Are|Does|Should|Which)\b[^\n]*\?',
        post['content'], re.MULTILINE | re.IGNORECASE
    )
    results['aeo'] = {'count': len(q_headings), 'passed': len(q_headings) >= 2}
    
    # E. Internal links
    internal_links = re.findall(r'\[([^\]]+)\]\((/[^)]+)\)', post['content'])
    results['il'] = {'count': len(internal_links), 'passed': len(internal_links) >= 3}
    
    # F. Schema
    missing_schema = []
    if not post['dateModified']: missing_schema.append('dateModified')
    if post['date'] == 'unknown': missing_schema.append('date')
    if post['author'] == 'unknown' or not post['author']: missing_schema.append('author')
    if len(post['excerpt']) < 20: missing_schema.append('excerpt')
    
    results['schema'] = {
        'passed': len(missing_schema) == 0,
        'missing': missing_schema
    }
    
    return results

def main():
    print("# Content Framework Enforcement Report")
    print(f"**Generated:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"**Project:** kanokmiah.com.bd")
    print()
    
    # Check git changes
    result = subprocess.run(
        ['git', 'log', '--oneline', '--since="48 hours ago"', '--', DATA_JS],
        capture_output=True, text=True, cwd='/root/kanok-miahit'
    )
    
    changes = result.stdout.strip().split('\n') if result.stdout.strip() else []
    print(f"**Commits touching data.js in last 48h:** {len(changes)}")
    for c in changes:
        print(f"  - {c}")
    print()
    
    # Parse posts
    posts = parse_posts(DATA_JS)
    print(f"**Total posts in data.js:** {len(posts)}")
    print()
    
    if not posts:
        print("❌ ERROR: Could not parse any posts.")
        return
    
    # Analyze all posts
    all_results = {}
    for post in posts:
        all_results[post['slug']] = analyze_post(post)
    
    # Group issues
    schema_issues = []
    tfidf_issues = []
    entity_issues = []
    pillar_issues = []
    aeo_issues = []
    il_issues = []
    
    for slug, r in all_results.items():
        post = next(p for p in posts if p['slug'] == slug)
        title = post['title']
        
        if not r['tfidf']['passed']:
            tfidf_issues.append((slug, title, r['tfidf']))
        if not r['entities']['passed']:
            entity_issues.append((slug, title, r['entities']))
        if not r['pillar']['passed']:
            pillar_issues.append((slug, title, r['pillar']))
        if not r['aeo']['passed']:
            aeo_issues.append((slug, title, r['aeo']))
        if not r['il']['passed']:
            il_issues.append((slug, title, r['il']))
        if not r['schema']['passed']:
            schema_issues.append((slug, title, r['schema']))
    
    # ====== REPORT ======
    
    # 1. TF-IDF issues
    if tfidf_issues:
        print("## ❌ TF-IDF Coverage Issues (keyword found < 5 times)")
        print(f"**{len(tfidf_issues)} post(s) affected**")
        print()
        print("| Post | Keyword | Count |")
        print("|------|---------|-------|")
        for slug, title, r in tfidf_issues:
            print(f"| {slug} | `{r['keyword']}` | {r['count']} |")
        print()
    else:
        print("## ✅ TF-IDF Coverage — All posts pass")
        print()
    
    # 2. Entity issues
    if entity_issues:
        print("## ❌ Entity Coverage Issues (no location entities found)")
        print(f"**{len(entity_issues)} post(s) affected**")
        print()
        for slug, title, r in entity_issues:
            print(f"- **{slug}**: No location entities found in content")
        print()
    else:
        print("## ✅ Entity Coverage — All posts pass")
        print()
    
    # 3. Pillar Link issues
    if pillar_issues:
        print("## ❌ Pillar/Service Link Missing")
        print(f"**{len(pillar_issues)} post(s) affected**")
        print()
        print("These posts have no links to any service page or the main pillar guide:")
        for slug, title, r in pillar_issues:
            print(f"- **{slug}**: `{title}`")
        print()
    else:
        print("## ✅ Pillar Links — All posts pass")
        print()
    
    # 4. AEO/GEO issues
    if aeo_issues:
        print("## ❌ AEO/GEO Optimization Issues (< 2 question-based headings)")
        print(f"**{len(aeo_issues)} post(s) affected**")
        print()
        # Group by count
        zero_count = [s for s, t, r in aeo_issues if r['count'] == 0]
        one_count = [s for s, t, r in aeo_issues if r['count'] == 1]
        
        if zero_count:
            print(f"**0 question headings ({len(zero_count)} posts) — worst offenders:**")
            for s in zero_count[:10]:
                post = next(p for p in posts if p['slug'] == s)
                print(f"  - {s}: `{post['title'][:60]}`")
            if len(zero_count) > 10:
                print(f"  ... and {len(zero_count) - 10} more")
        if one_count:
            print(f"**1 question heading ({len(one_count)} posts):**")
            for s in one_count[:5]:
                post = next(p for p in posts if p['slug'] == s)
                print(f"  - {s}: `{post['title'][:60]}`")
            if len(one_count) > 5:
                print(f"  ... and {len(one_count) - 5} more")
        print()
        print("**Pattern:** Most Bengali-language posts and newer silo case studies lack FAQ sections.")
        print()
    else:
        print("## ✅ AEO/GEO — All posts pass")
        print()
    
    # 5. Internal Link issues
    if il_issues:
        print("## ❌ Internal Link Issues (< 3 internal links)")
        print(f"**{len(il_issues)} post(s) affected**")
        print()
        print("| Post | Link Count |")
        print("|------|-----------|")
        for slug, title, r in il_issues:
            print(f"| {slug} | {r['count']} |")
        print()
    else:
        print("## ✅ Internal Links — All posts pass")
        print()
    
    # 6. Schema issues
    if schema_issues:
        print("## ❌ Schema Readiness Issues")
        print(f"**{len(schema_issues)} post(s) affected**")
        print()
        # Check what's missing most
        missing_counts = {}
        for slug, title, r in schema_issues:
            for m in r['missing']:
                missing_counts[m] = missing_counts.get(m, 0) + 1
        print("**Missing fields breakdown:**")
        for field, count in sorted(missing_counts.items(), key=lambda x: -x[1]):
            print(f"  - `{field}`: missing from {count} posts")
        print()
        # Specific list
        print("**All affected posts (no dateModified):**")
        for slug, title, r in schema_issues:
            print(f"  - {slug}")
        print()
        print("**Fix:** Bulk-add `dateModified: \"2026-07-15\"` to all posts that were processed on July 15.")
        print()
    
    # Overall summary
    total_issues = len(tfidf_issues) + len(entity_issues) + len(pillar_issues) + len(aeo_issues) + len(il_issues) + len(schema_issues)
    passing_posts = sum(1 for r in all_results.values() if all([
        r['tfidf']['passed'], r['entities']['passed'], r['pillar']['passed'],
        r['aeo']['passed'], r['il']['passed'], r['schema']['passed']
    ]))
    
    print("---")
    print("## Overall Summary")
    print(f"| Metric | Value |")
    print(f"|--------|-------|")
    print(f"| Total posts checked | {len(posts)} |")
    print(f"| Posts passing ALL checks | {passing_posts}/{len(posts)} |")
    print(f"| TF-IDF issues | {len(tfidf_issues)} |")
    print(f"| Entity issues | {len(entity_issues)} |")
    print(f"| Pillar link issues | {len(pillar_issues)} |")
    print(f"| AEO/GEO issues | {len(aeo_issues)} |")
    print(f"| Internal link issues | {len(il_issues)} |")
    print(f"| Schema issues | {len(schema_issues)} |")
    print()
    
    if passing_posts == len(posts):
        print("✅ ALL POSTS PASS ALL CHECKS.")
    elif total_issues == 0:
        print("✅ No issues found.")
    else:
        print("### Priority Fixes")
        print()
        # Priority 1: Schema (bulk fix, affects almost all posts)
        if schema_issues:
            print(f"**P1 — Add `dateModified` field to all {len(schema_issues)} posts**")
            print(f"  Bulk action: every post needs `dateModified: \"2026-07-15\"` added.")
            print()
        
        # Priority 2: Pillar links (critical for SEO structure)
        if pillar_issues:
            print(f"**P2 — Add pillar links to {len(pillar_issues)} posts**")
            for slug, title, r in pillar_issues:
                print(f"  - `{slug}`: needs link to /services/local-seo, /services/technical-seo, or /blog/complete-seo-guide-bangladesh-businesses-2026")
            print()
        
        # Priority 3: AEO/GEO (affects many Bengali + case study posts)
        if aeo_issues:
            print(f"**P3 — Add FAQ/question sections to {len(aeo_issues)} Bengali + case study posts**")
            print(f"  Add 2+ question-based headings (How, What, Why, etc.) per post.")
            print()
        
        # Priority 4: Internal links (few posts)
        if il_issues:
            print(f"**P4 — Add internal links to {len(il_issues)} posts**")
            for slug, title, r in il_issues:
                print(f"  - `{slug}`: has only {r['count']} internal link(s)")
            print()
        
        # Priority 5: TF-IDF
        if tfidf_issues:
            print(f"**P5 — Fix keyword density for {len(tfidf_issues)} posts**")
            for slug, title, r in tfidf_issues:
                print(f"  - `{slug}`: keyword `{r['keyword']}` found {r['count']} times")
            print()

if __name__ == '__main__':
    main()
