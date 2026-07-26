#!/usr/bin/env python3
"""Spot-check a few posts to verify accuracy of link counting."""
import re

with open('/root/kanok-miahit/src/app/blog/data.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Manual verification: count links in first post
def parse_posts_robust(text):
    arr_start = text.find('const posts = [')
    bracket_start = text.find('[', arr_start)
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

# Check specific posts
check_slugs = [
    'complete-seo-guide-bangladesh-businesses-2026',
    'seo-structured-data-guide-bd',
    'locksmith-dundee-seo-case-study',
    'what-does-seo-expert-do-guide-business-owners',
]

for slug in check_slugs:
    post = next((p for p in posts if p['slug'] == slug), None)
    if not post:
        print(f"Post not found: {slug}")
        continue
    
    text = post['text']
    cs = text.find('content: `')
    cs += len('content: `')
    
    # Parse content properly
    content_parts = []
    i = cs
    while i < len(text):
        ch = text[i]
        if ch == '\\' and i + 1 < len(text) and text[i+1] == '`':
            content_parts.append('`')
            i += 2
            continue
        if ch == '`':
            if i + 1 < len(text) and text[i+1] == ',':
                break
            break  # end of content
        content_parts.append(ch)
        i += 1
    
    content_str = ''.join(content_parts)
    
    # Find all markdown links
    md_links = re.findall(r'\[([^\]]*)\]\(([^)]+)\)', content_str)
    
    internal = []
    external = []
    for text, url in md_links:
        url = url.strip()
        if url.startswith('/'):
            internal.append(url)
        elif url.startswith('http://') or url.startswith('https://'):
            domain_match = re.match(r'https?://([^/]+)', url)
            if domain_match:
                domain = domain_match.group(1).lower()
                if 'kanokmiah' in domain or 'kanok-miah' in domain:
                    path_match = re.match(r'https?://[^/]+(/.*)', url)
                    if path_match:
                        internal.append(path_match.group(1))
                    else:
                        internal.append('/')
                else:
                    external.append(url)
    
    words = re.sub(r'[#*_\[\]()>|`\-]', ' ', content_str).split()
    word_count = len(words)
    total = len(internal) + len(external)
    density = round(total / word_count * 100, 2) if word_count > 0 else 0
    
    print(f"\n{'='*60}")
    print(f"VERIFICATION: {slug}")
    print(f"{'='*60}")
    print(f"Internal links ({len(internal)}):")
    for l in internal:
        print(f"  {l}")
    print(f"External links ({len(external)}):")
    for l in external:
        print(f"  {l}")
    print(f"Word count: {word_count}")
    print(f"Link density: {density}")
