#!/usr/bin/env python3
"""
Analyze Internal Linking & Technical SEO for all blog posts in data.js
Version 3: Robust parsing using brace-depth tracking
"""
import re
import json

with open('/root/kanok-miahit/src/app/blog/data.js', 'r', encoding='utf-8') as f:
    content = f.read()

def parse_posts_robust(text):
    """Parse posts by tracking brace depth, handling template strings."""
    # Find the start of the array
    arr_start = text.find('const posts = [')
    if arr_start == -1:
        print("ERROR: Could not find 'const posts = ['")
        return []
    
    # Start after '['
    bracket_start = text.find('[', arr_start)
    if bracket_start == -1:
        return []
    
    posts = []
    i = bracket_start + 1
    
    array_depth = 0  # depth within the outer array
    brace_depth = 0  # depth within current post object
    
    current_post_start = -1
    current_post_slug = None
    
    in_template_string = False
    in_string = False
    string_char = None
    
    while i < len(text):
        ch = text[i]
        
        # Handle template strings (backticks)
        if ch == '`' and not in_string:
            if in_template_string:
                # Check if this backtick is escaped
                if i > 0 and text[i-1] == '\\':
                    # Escaped backtick, skip
                    i += 1
                    continue
                in_template_string = False
            else:
                in_template_string = True
            i += 1
            continue
        
        # Handle regular strings (inside template strings, these don't count)
        if in_template_string:
            # Inside template string, backslash escapes
            if ch == '\\' and i + 1 < len(text):
                i += 2
                continue
            i += 1
            continue
        
        # Handle regular strings (double/single quoted)
        if ch in ('"', "'") and not in_string:
            in_string = True
            string_char = ch
            i += 1
            continue
        
        if in_string:
            if ch == '\\' and i + 1 < len(text):
                i += 2  # skip escaped char
                continue
            if ch == string_char:
                in_string = False
            i += 1
            continue
        
        # Track braces for post objects
        if ch == '{':
            if brace_depth == 0:
                current_post_start = i
            brace_depth += 1
            i += 1
            continue
        
        if ch == '}':
            brace_depth -= 1
            if brace_depth == 0 and current_post_start is not None:
                # We've found the end of a post
                post_text = text[current_post_start:i+1]
                
                # Extract slug from this post text
                slug_match = re.search(r'slug:\s*"([^"]+)"', post_text)
                if slug_match:
                    slug = slug_match.group(1)
                    posts.append({
                        'slug': slug,
                        'text': post_text,
                    })
                current_post_start = None
            i += 1
            continue
        
        i += 1
    
    return posts


# Parse posts
posts = parse_posts_robust(content)
print(f"Parsed {len(posts)} posts")

# Get all unique slugs
all_slugs = [p['slug'] for p in posts]
unique_slugs = []
seen = set()
for s in all_slugs:
    if s not in seen:
        seen.add(s)
        unique_slugs.append(s)

print(f"Unique slugs: {len(unique_slugs)}")
valid_slug_set = set(unique_slugs)

# Display any duplicate slugs
slug_counts = {}
for s in all_slugs:
    slug_counts[s] = slug_counts.get(s, 0) + 1
for s, c in slug_counts.items():
    if c > 1:
        print(f"  DUPLICATE: {s} appears {c} times")


def extract_content_from_post_text(post_text):
    """Extract the content template string from a post object text."""
    # Find content: `
    content_start = post_text.find('content: `')
    if content_start == -1:
        return ""
    
    content_start += len('content: `')
    
    # Now parse the template string properly
    content_parts = []
    i = content_start
    while i < len(post_text):
        ch = post_text[i]
        
        # Check for escaped backtick
        if ch == '\\' and i + 1 < len(post_text) and post_text[i+1] == '`':
            content_parts.append('`')  # keep the backtick char
            i += 2
            continue
        
        # Check for closing backtick followed by comma (end of content)
        if ch == '`':
            if i + 1 < len(post_text) and post_text[i+1] == ',':
                # This is the closing `,
                return ''.join(content_parts)
            elif i + 1 < len(post_text) and post_text[i+1] == '\n':
                # Also possible: `\n  },
                if i + 2 < len(post_text) and post_text[i+2] == ' ':
                    return ''.join(content_parts)
            # Otherwise it might be another template string in the JS object?
            # Actually, content is the ONLY template string in these posts
            return ''.join(content_parts)
        
        content_parts.append(ch)
        i += 1
    
    return ''.join(content_parts)


def count_links(content, slug):
    """Count internal and external links in content."""
    
    internal_links = []
    external_links = []
    all_links = []
    
    # Find markdown links [text](url)
    md_links = re.findall(r'\[([^\]]*)\]\(([^)]+)\)', content)
    for text, url in md_links:
        url = url.strip()
        if url.startswith('/'):
            internal_links.append(url)
            all_links.append(url)
        elif url.startswith('http://') or url.startswith('https://'):
            domain_match = re.match(r'https?://([^/]+)', url)
            if domain_match:
                domain = domain_match.group(1).lower()
                if 'kanokmiah' in domain or 'kanok-miah' in domain:
                    path_match = re.match(r'https?://[^/]+(/.*)', url)
                    if path_match:
                        internal_links.append(path_match.group(1))
                    else:
                        internal_links.append('/')
                else:
                    external_links.append(url)
            all_links.append(url)
    
    # Also find bare http/https URLs outside markdown links
    bare_url_pattern = re.compile(r'(?<!\]\()(https?://[^\s\)\"\'<>\[\]]+)')
    bare_urls = bare_url_pattern.findall(content)
    for url in bare_urls:
        if url not in all_links:
            domain_match = re.match(r'https?://([^/]+)', url)
            if domain_match:
                domain = domain_match.group(1).lower()
                if 'kanokmiah' in domain or 'kanok-miah' in domain:
                    path_match = re.match(r'https?://[^/]+(/.*)', url)
                    if path_match:
                        internal_links.append(path_match.group(1))
                    else:
                        internal_links.append('/')
                else:
                    external_links.append(url)
            all_links.append(url)
    
    # Categorize internal links
    categorized = {
        '/blog/*': [],
        '/services/*': [],
        '/industries/*': [],
        '/locations/*': [],
        '/about': [],
        '/contact': [],
        '/': [],
        'other': [],
    }
    
    blog_internal_links = []
    for link in internal_links:
        if link.startswith('/blog/'):
            categorized['/blog/*'].append(link)
            blog_internal_links.append(link)
        elif link.startswith('/services/'):
            categorized['/services/*'].append(link)
        elif link.startswith('/industries/'):
            categorized['/industries/*'].append(link)
        elif link.startswith('/locations/'):
            categorized['/locations/*'].append(link)
        elif link == '/about':
            categorized['/about'].append(link)
        elif link == '/contact':
            categorized['/contact'].append(link)
        elif link == '/':
            categorized['/'].append(link)
        else:
            categorized['other'].append(link)
    
    # Count broken blog links
    broken_blog_links = []
    for link in blog_internal_links:
        path = link
        if path.startswith('/blog/'):
            link_slug = path[len('/blog/'):]
            link_slug = link_slug.rstrip('/')
            if link_slug not in valid_slug_set:
                broken_blog_links.append(link)
    
    # Count missing blog prefix links
    missing_blog_prefix = []
    for link in internal_links:
        link_path = link.rstrip('/')
        if link_path.startswith('/'):
            candidate = link_path[1:]
        else:
            candidate = link_path
        if candidate in valid_slug_set and not link.startswith('/blog/'):
            missing_blog_prefix.append(link)
    
    # Word count
    clean_text = re.sub(r'[#*_\[\]()>|`\-]', ' ', content)
    words = clean_text.split()
    word_count = len(words)
    
    total_links = len(internal_links) + len(external_links)
    link_density = round(total_links / word_count * 100, 2) if word_count > 0 else 0
    
    return {
        'internal_links': internal_links,
        'external_links': external_links,
        'internal_count': len(internal_links),
        'external_count': len(external_links),
        'categorized': categorized,
        'broken_blog_links': broken_blog_links,
        'broken_blog_count': len(broken_blog_links),
        'missing_blog_prefix': missing_blog_prefix,
        'missing_blog_prefix_count': len(missing_blog_prefix),
        'total_links': total_links,
        'word_count': word_count,
        'link_density': link_density,
    }


# Process each post
results = []
for post in posts:
    slug = post['slug']
    post_text = post['text']
    content_str = extract_content_from_post_text(post_text)
    
    if not content_str:
        print(f"WARNING: No content found for {slug}")
        continue
    
    analysis = count_links(content_str, slug)
    
    is_linking_gap = analysis['internal_count'] <= 1
    
    results.append({
        'slug': slug,
        'internal_count': analysis['internal_count'],
        'external_count': analysis['external_count'],
        'categorized': analysis['categorized'],
        'broken_blog_count': analysis['broken_blog_count'],
        'broken_blog_links': analysis['broken_blog_links'],
        'link_density': analysis['link_density'],
        'total_links': analysis['total_links'],
        'word_count': analysis['word_count'],
        'is_linking_gap': is_linking_gap,
        'missing_blog_prefix_count': analysis['missing_blog_prefix_count'],
        'missing_blog_prefix': analysis['missing_blog_prefix'],
        'internal_links': analysis['internal_links'],
        'external_links': analysis['external_links'],
    })

# De-duplicate by slug (keep first occurrence)
seen_slugs = set()
unique_results = []
for r in results:
    if r['slug'] not in seen_slugs:
        seen_slugs.add(r['slug'])
        unique_results.append(r)
results = unique_results

print(f"Unique posts analyzed: {len(results)}")

# Output pipe-delimited table
print("\n" + "="*130)
print("PIPE-DELIMITED TABLE: slug|internal_links|external_links|broken_links|link_density|posts_with_0_or_1_internal|missing_blog_prefix_count")
print("="*130)

posts_with_gaps = []
posts_with_missing_prefix = []
all_broken_links = []

for r in results:
    gap_flag = 'YES' if r['is_linking_gap'] else ''
    print(f"{r['slug']}|{r['internal_count']}|{r['external_count']}|{r['broken_blog_count']}|{r['link_density']}|{gap_flag}|{r['missing_blog_prefix_count']}")
    
    if r['is_linking_gap']:
        posts_with_gaps.append(r['slug'])
    if r['missing_blog_prefix_count'] > 0:
        posts_with_missing_prefix.append(r['slug'])
    for bl in r['broken_blog_links']:
        all_broken_links.append((r['slug'], bl))

print("\n" + "="*130)
print("ALL SLUGS IN DATA.JS (ACTUAL BLOG POSTS)")
print("="*130)
for s in unique_slugs:
    print(s)
print(f"Total: {len(unique_slugs)}")

print("\n" + "="*130)
print("POSTS WITH 0 OR 1 INTERNAL LINKS (LINKING GAPS)")
print("="*130)
if posts_with_gaps:
    for s in posts_with_gaps:
        r = next((r for r in results if r['slug'] == s), None)
        if r:
            print(f"  {s} (internal: {r['internal_count']})")
else:
    print("  None found")
print(f"Total: {len(posts_with_gaps)}")

print("\n" + "="*130)
print("POSTS WITH MISSING BLOG PREFIX LINKS")
print("="*130)
if posts_with_missing_prefix:
    for r in results:
        if r['missing_blog_prefix_count'] > 0:
            print(f"  {r['slug']}: {r['missing_blog_prefix']}")
else:
    print("  None found")
print(f"Total posts with missing prefix: {len(posts_with_missing_prefix)}")

print("\n" + "="*130)
print("BROKEN BLOG LINKS (links to /blog/slug where slug doesn't exist in posts array)")
print("="*130)
for source, link in all_broken_links:
    print(f"  {source} -> {link}")
if not all_broken_links:
    print("  None found!")
print(f"Total broken links: {len(all_broken_links)}")

print("\n" + "="*130)
print("SUMMARY STATISTICS")
print("="*130)
total_posts = len(results)
total_internal = sum(r['internal_count'] for r in results)
total_external = sum(r['external_count'] for r in results)
total_broken = sum(r['broken_blog_count'] for r in results)
total_missing_prefix = sum(r['missing_blog_prefix_count'] for r in results)
avg_link_density = round(sum(r['link_density'] for r in results) / total_posts, 2) if total_posts > 0 else 0

print(f"Total posts analyzed: {total_posts}")
print(f"Total internal links: {total_internal}")
print(f"Total external links: {total_external}")
print(f"Total broken blog links: {total_broken}")
print(f"Total missing blog prefix: {total_missing_prefix}")
print(f"Average link density: {avg_link_density} links per 100 words")
print(f"Posts with 0 or 1 internal links (gaps): {len(posts_with_gaps)}")
print(f"Posts with missing blog prefix: {len(posts_with_missing_prefix)}")

# Category breakdown
cat_totals = {}
for r in results:
    for cat, links in r['categorized'].items():
        cat_totals[cat] = cat_totals.get(cat, 0) + len(links)
print(f"\nInternal link category breakdown:")
for cat, count in sorted(cat_totals.items()):
    print(f"  {cat}: {count}")

# Save JSON
with open('/root/kanok-miahit/link_analysis_results_v3.json', 'w', encoding='utf-8') as f:
    json.dump({
        'posts': results,
        'summary': {
            'total_posts': total_posts,
            'total_internal': total_internal,
            'total_external': total_external,
            'total_broken': total_broken,
            'total_missing_prefix': total_missing_prefix,
            'avg_link_density': avg_link_density,
            'posts_with_gaps': posts_with_gaps,
            'posts_with_missing_prefix': posts_with_missing_prefix,
            'gap_count': len(posts_with_gaps),
            'missing_prefix_count': len(posts_with_missing_prefix),
        },
        'all_slugs': unique_slugs,
    }, f, indent=2, ensure_ascii=False)

print(f"\n\nDetailed results saved to link_analysis_results_v3.json")
