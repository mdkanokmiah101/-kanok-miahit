#!/usr/bin/env python3
"""
Final analysis: Generate clean pipe-delimited table and summary.
Uses v3 robust parsing.
"""
import re
import json

with open('/root/kanok-miahit/src/app/blog/data.js', 'r', encoding='utf-8') as f:
    content = f.read()

# --- Robust parsing ---
def parse_posts_robust(text):
    arr_start = text.find('const posts = [')
    bracket_start = text.find('[', arr_start)
    if bracket_start == -1:
        return []
    posts = []
    i = bracket_start + 1
    brace_depth = 0
    current_post_start = -1
    in_template_string = False
    in_string = False
    string_char = None
    
    while i < len(text):
        ch = text[i]
        if ch == '`' and not in_string:
            if in_template_string:
                if i > 0 and text[i-1] == '\\':
                    i += 1
                    continue
                in_template_string = False
            else:
                in_template_string = True
            i += 1
            continue
        if in_template_string:
            if ch == '\\' and i + 1 < len(text):
                i += 2
                continue
            i += 1
            continue
        if ch in ('"', "'") and not in_string:
            in_string = True
            string_char = ch
            i += 1
            continue
        if in_string:
            if ch == '\\' and i + 1 < len(text):
                i += 2
                continue
            if ch == string_char:
                in_string = False
            i += 1
            continue
        if ch == '{':
            if brace_depth == 0:
                current_post_start = i
            brace_depth += 1
            i += 1
            continue
        if ch == '}':
            brace_depth -= 1
            if brace_depth == 0 and current_post_start is not None:
                post_text = text[current_post_start:i+1]
                slug_match = re.search(r'slug:\s*"([^"]+)"', post_text)
                if slug_match:
                    posts.append({'slug': slug_match.group(1), 'text': post_text})
                current_post_start = None
            i += 1
            continue
        i += 1
    return posts

posts = parse_posts_robust(content)

# Extract unique slugs
all_slugs = [p['slug'] for p in posts]
unique_slugs = []
seen = set()
for s in all_slugs:
    if s not in seen:
        seen.add(s)
        unique_slugs.append(s)
valid_slug_set = set(unique_slugs)

# --- Extract content from template string ---
def extract_content(post_text):
    cs = post_text.find('content: `')
    if cs == -1:
        return ""
    cs += len('content: `')
    parts = []
    i = cs
    while i < len(post_text):
        ch = post_text[i]
        if ch == '\\' and i + 1 < len(post_text) and post_text[i+1] == '`':
            parts.append('`')
            i += 2
            continue
        if ch == '`':
            if i + 1 < len(post_text) and post_text[i+1] == ',':
                break
            break
        parts.append(ch)
        i += 1
    return ''.join(parts)

# --- Link analysis ---
def analyze(content_str, slug, valid_set):
    # Find markdown links
    internal = []
    external = []
    all_links = set()
    
    md_links = re.findall(r'\[([^\]]*)\]\(([^)]+)\)', content_str)
    for txt, url in md_links:
        url = url.strip()
        all_links.add(url)
        if url.startswith('/'):
            internal.append(url)
        elif url.startswith('http://') or url.startswith('https://'):
            m = re.match(r'https?://([^/]+)', url)
            if m:
                domain = m.group(1).lower()
                if 'kanokmiah' in domain or 'kanok-miah' in domain:
                    p = re.match(r'https?://[^/]+(/.*)', url)
                    internal.append(p.group(1) if p else '/')
                else:
                    external.append(url)
    
    # Bare URLs outside markdown
    bare = re.findall(r'(?<!\]\()(https?://[^\s\)\"\'<>\[\]]+)', content_str)
    for url in bare:
        if url not in all_links:
            all_links.add(url)
            m = re.match(r'https?://([^/]+)', url)
            if m:
                domain = m.group(1).lower()
                if 'kanokmiah' in domain or 'kanok-miah' in domain:
                    p = re.match(r'https?://[^/]+(/.*)', url)
                    internal.append(p.group(1) if p else '/')
                else:
                    external.append(url)
    
    # Categorize
    cat = {'/blog/*': [], '/services/*': [], '/industries/*': [], '/locations/*': [], '/about': [], '/contact': [], '/': [], 'other': []}
    blog_links = []
    for l in internal:
        if l.startswith('/blog/'):
            cat['/blog/*'].append(l); blog_links.append(l)
        elif l.startswith('/services/'): cat['/services/*'].append(l)
        elif l.startswith('/industries/'): cat['/industries/*'].append(l)
        elif l.startswith('/locations/'): cat['/locations/*'].append(l)
        elif l == '/about': cat['/about'].append(l)
        elif l == '/contact': cat['/contact'].append(l)
        elif l == '/': cat['/'].append(l)
        else: cat['other'].append(l)
    
    # Broken blog links
    broken = []
    for l in blog_links:
        s = l[len('/blog/'):].rstrip('/')
        if s not in valid_set:
            broken.append(l)
    
    # Missing blog prefix
    missing = []
    for l in internal:
        cand = l.rstrip('/')
        if cand.startswith('/'): cand = cand[1:]
        if cand in valid_set and not l.startswith('/blog/'):
            missing.append(l)
    
    # Word count
    words = re.sub(r'[#*_\[\]()>|`\-]', ' ', content_str).split()
    wc = len(words)
    total = len(internal) + len(external)
    density = round(total / wc * 100, 2) if wc > 0 else 0
    
    return {
        'internal_count': len(internal), 'external_count': len(external),
        'broken_blog_count': len(broken), 'broken_blog_links': broken,
        'link_density': density, 'total_links': total, 'word_count': wc,
        'missing_blog_prefix_count': len(missing), 'missing_blog_prefix': missing,
        'internal_links': internal, 'external_links': external, 'categorized': cat,
    }

# Process all posts
results = []
for post in posts:
    slug = post['slug']
    c = extract_content(post['text'])
    if not c:
        continue
    a = analyze(c, slug, valid_slug_set)
    results.append({
        'slug': slug, 'internal_count': a['internal_count'],
        'external_count': a['external_count'],
        'broken_blog_count': a['broken_blog_count'],
        'broken_blog_links': a['broken_blog_links'],
        'link_density': a['link_density'],
        'missing_blog_prefix_count': a['missing_blog_prefix_count'],
        'missing_blog_prefix': a['missing_blog_prefix'],
        'is_linking_gap': a['internal_count'] <= 1,
        'categorized': a['categorized'],
    })

# De-duplicate by slug
seen = set()
unique = []
for r in results:
    if r['slug'] not in seen:
        seen.add(r['slug'])
        unique.append(r)
results = unique

# Output
print("=" * 140)
print("INTERNAL LINKING & TECHNICAL SEO ANALYSIS — ALL BLOG POSTS")
print("=" * 140)

# Pipe-delimited table header
print("slug|internal_links|external_links|broken_blog_links|link_density|link_gap_0or1|missing_blog_prefix")
print("-" * 140)

for r in results:
    gap = 'YES' if r['is_linking_gap'] else ''
    print(f"{r['slug']}|{r['internal_count']}|{r['external_count']}|{r['broken_blog_count']}|{r['link_density']}|{gap}|{r['missing_blog_prefix_count']}")

# Summary sections
posts_with_gaps = [r['slug'] for r in results if r['is_linking_gap']]
posts_with_prefix = [r for r in results if r['missing_blog_prefix_count'] > 0]
all_broken = [(r['slug'], bl) for r in results for bl in r['broken_blog_links']]

print("\n" + "=" * 140)
print("ALL 128 BLOG SLUGS IN data.js")
print("=" * 140)
for s in unique_slugs:
    print(s)

print("\n" + "=" * 140)
print("SECTION 1 — LINKING GAPS (Posts with 0 or 1 internal links)")
print("=" * 140)
if posts_with_gaps:
    for s in posts_with_gaps:
        r = next(x for x in results if x['slug'] == s)
        print(f"  {s}  (internal: {r['internal_count']})")
else:
    print("  None found — all 128 posts have ≥2 internal links")
print(f"Total: {len(posts_with_gaps)}")

print("\n" + "=" * 140)
print("SECTION 2 — POSTS WITH MISSING BLOG PREFIX")
print("=" * 140)
if posts_with_prefix:
    for r in posts_with_prefix:
        print(f"  {r['slug']}: {r['missing_blog_prefix']}")
else:
    print("  None found")
print(f"Total: {len(posts_with_prefix)}")

print("\n" + "=" * 140)
print("SECTION 3 — BROKEN BLOG LINKS (/blog/slug that doesn't exist)")
print("=" * 140)
if all_broken:
    for src, link in all_broken:
        slug_name = link[len('/blog/'):].rstrip('/')
        print(f"  [{src}]  {link}  (slug '{slug_name}' not found in posts array)")
else:
    print("  None found")
print(f"Total broken links: {len(all_broken)}")

print("\n" + "=" * 140)
print("SECTION 4 — INTERNAL LINK CATEGORY BREAKDOWN (all posts combined)")
print("=" * 140)
cat_totals = {}
for r in results:
    for cat, links in r['categorized'].items():
        cat_totals[cat] = cat_totals.get(cat, 0) + len(links)
for cat, count in sorted(cat_totals.items()):
    print(f"  {cat:<15}: {count:>4}")
print(f"  {'TOTAL':<15}: {sum(cat_totals.values()):>4}")

print("\n" + "=" * 140)
print("OVERALL SUMMARY")
print("=" * 140)
total_posts = len(results)
total_int = sum(r['internal_count'] for r in results)
total_ext = sum(r['external_count'] for r in results)
total_broken = sum(r['broken_blog_count'] for r in results)
total_missing = sum(r['missing_blog_prefix_count'] for r in results)
avg_density = round(sum(r['link_density'] for r in results) / total_posts, 2) if total_posts > 0 else 0

print(f"  Posts analyzed:                      {total_posts}")
print(f"  Total internal links:                {total_int}")
print(f"  Total external links:                {total_ext}")
print(f"  Total broken blog links:             {total_broken}")
print(f"  Total missing blog prefix:           {total_missing}")
print(f"  Average link density:                {avg_density} links/100 words")
print(f"  Posts with 0 or 1 internal (gaps):   {len(posts_with_gaps)}")
print(f"  Posts with missing blog prefix:      {len(posts_with_prefix)}")

# Save final JSON
with open('/root/kanok-miahit/link_analysis_final.json', 'w', encoding='utf-8') as f:
    json.dump({
        'posts': results,
        'all_slugs': unique_slugs,
        'summary': {
            'total_posts': total_posts,
            'total_internal': total_int,
            'total_external': total_ext,
            'total_broken': total_broken,
            'total_missing_prefix': total_missing,
            'avg_link_density': avg_density,
            'gap_count': len(posts_with_gaps),
            'missing_prefix_count': len(posts_with_prefix),
            'post_with_gaps': posts_with_gaps,
            'posts_with_missing_prefix': [r['slug'] for r in posts_with_prefix],
            'broken_links': [{'source': s, 'link': l, 'missing_slug': l[len('/blog/'):].rstrip('/')} for s, l in all_broken],
        }
    }, f, indent=2, ensure_ascii=False)

print("\nDetailed JSON saved to link_analysis_final.json")
