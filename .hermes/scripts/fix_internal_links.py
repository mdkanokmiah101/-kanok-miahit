#!/usr/bin/env python3
"""
Internal Link Fixer for kanokmiah.com.bd Blog Posts
- Removes duplicate homepage links (keeps only 1 per post)
- Replaces extra homepage links with relevant blog-to-blog internal links
- Safe: processes replacements from end to start to preserve positions
"""

import re
import sys

DATA_FILE = "/root/kanok-miahit/src/app/blog/data.js"

STOP_WORDS = {
    'seo', 'for', 'in', 'bangladesh', 'bd', 'guide', 'tips', 'how', 'to',
    'and', 'the', 'a', 'is', 'of', 'your', 'with', 'from', 'dhaka', 'b2b',
    'getting', 'ready', 'its', 'need', 'needs', 'what', 'does', 'expert',
    'do', 'vs', 'right', 'top', 'fix', 'that', 'can', 'you', 'your', 'our',
    'are', 'not', 'but', 'has', 'have', 'been', 'all', 'more', 'best',
    'every', 'should', 'their', 'them', 'they', 'this', 'that', 'these',
    'those', 'who', 'which', 'when', 'where', 'why', 'any', 'some', 'each',
    'online', 'stores', 'store', 'business', 'businesses', 'brand', 'brands',
    'new', 'into', 'era', 'case', 'study', 'studies', 'up', 'out', 'over',
    'get', 'using', 'work', 'works', 'make', 'making', 'boost', 'increase',
    'grow', 'growth', 'build', 'building', 'create', 'creating'
}


def read_data():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return f.read()


def write_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        f.write(data)
    print(f"✅ Written {len(data)} bytes to data.js")


def extract_slugs_and_titles(data):
    """Extract slug -> title mapping"""
    pattern = r'slug: "([^"]+)",\s*\n\s*title: "([^"]+)",'
    matches = re.findall(pattern, data)
    return {slug: title for slug, title in matches}


def extract_keywords(slug):
    words = set(slug.replace('-', ' ').split())
    return words - STOP_WORDS


def build_slug_keywords(slug_title_map):
    return {slug: extract_keywords(slug) for slug in slug_title_map}


def find_related_posts(current_slug, slug_keywords, max_results=5):
    current_keywords = slug_keywords.get(current_slug, set())
    if not current_keywords:
        return []
    scores = []
    for slug, keywords in slug_keywords.items():
        if slug == current_slug:
            continue
        overlap = len(current_keywords & keywords)
        if overlap > 0:
            scores.append((overlap, slug))
    scores.sort(reverse=True)
    return [s[1] for s in scores[:max_results]]


def get_anchor_text(slug, slug_title_map):
    title = slug_title_map.get(slug, slug.replace('-', ' ').title())
    return title[:55] if len(title) > 55 else title


def fix_content(content, slug, slug_keywords, slug_title_map):
    """
    Fix internal links:
    1. Find ALL homepage links (both relative / and full URL https://kanokmiah.com.bd/)
    2. If > 1, keep only the first one
    3. Replace the rest with blog-to-blog internal links
    Process from END to START so positions stay valid.
    """
    # Patterns for homepage links
    # Relative: [text](/) or [text]( )
    rel_pattern = r'\[([^\]]*?)\]\(\s*/\s*\)'
    # Full URL: [text](https://kanokmiah.com.bd/) or [text](http://kanokmiah.com.bd/)
    full_pattern = r'\[([^\]]*?)\]\(https?://kanokmiah\.com\.bd/?\)'
    
    rel_matches = list(re.finditer(rel_pattern, content))
    full_matches = list(re.finditer(full_pattern, content))
    
    # Combine all matches with their positions
    all_matches = [(m.start(), m.end(), m.group(1), 'rel') for m in rel_matches]
    all_matches += [(m.start(), m.end(), m.group(1), 'full') for m in full_matches]
    all_matches.sort(key=lambda x: x[0])  # Sort by position
    
    total = len(all_matches)
    
    if total <= 1:
        return content, 0
    
    print(f"    Found {total} homepage links, keeping first, replacing {total-1}")
    
    # Keep first, replace rest (process from end to start)
    to_replace = all_matches[1:]  # Skip the first one
    to_replace.sort(key=lambda x: x[0], reverse=True)  # Process from end to start
    
    related = find_related_posts(slug, slug_keywords)
    
    replacements = 0
    for idx, (pos, end, anchor, link_type) in enumerate(to_replace):
        if idx < len(related):
            rel_slug = related[idx]
            rel_title = get_anchor_text(rel_slug, slug_title_map)
            replacement = f"[{rel_title}](/blog/{rel_slug})"
        else:
            # No more related posts - keep the anchor text but remove the link
            replacement = anchor
        
        content = content[:pos] + replacement + content[end:]
        replacements += 1
    
    return content, replacements


def process_file():
    data = read_data()
    slug_title_map = extract_slugs_and_titles(data)
    slug_keywords = build_slug_keywords(slug_title_map)
    
    print(f"📊 Found {len(slug_title_map)} blog posts")
    
    # Use a more precise pattern for each post
    post_pattern = r'(slug: "([^"]+)"[\s\S]*?content: `)([\s\S]*?)(`,\s*}\s*,?\s*)'
    
    total_replacements = 0
    fixed_posts = 0
    
    def process_post(match):
        nonlocal total_replacements, fixed_posts
        prefix = match.group(1)
        post_slug = match.group(2)
        content = match.group(3)
        suffix = match.group(4)
        
        new_content, count = fix_content(content, post_slug, slug_keywords, slug_title_map)
        
        if count > 0:
            fixed_posts += 1
            total_replacements += count
            return prefix + new_content + suffix
        return match.group(0)
    
    new_data = re.sub(post_pattern, process_post, data)
    
    if new_data == data:
        print("⚠️  No changes made.")
    else:
        write_data(new_data)
        print(f"\n📊 Summary:")
        print(f"   Fixed posts: {fixed_posts}")
        print(f"   Total replacements: {total_replacements}")
    
    return fixed_posts, total_replacements


if __name__ == "__main__":
    print("🔧 Internal Link Fixer for kanokmiah.com.bd")
    print("=" * 50)
    process_file()
