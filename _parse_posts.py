#!/usr/bin/env python3
"""Extract blog post data from data.js with slug, title, content, tags, etc."""
import re
import json

with open("/root/kanok-miahit/src/app/blog/data.js") as f:
    content = f.read()

# Parse the blogPosts array
# Find the blogPosts = [ ... ] pattern
match = re.search(r'const blogPosts\s*=\s*(\[.*?\]);', content, re.DOTALL)
if not match:
    # Try another pattern
    match = re.search(r'const\s+\w+\s*=\s*(\[.*?\]);', content, re.DOTALL)
    if not match:
        print("Could not find blogPosts array")
        exit(1)

posts_str = match.group(1)

# Parse each post object
# Find slug, title, excerpt, date, tags, content fields
posts = []
# Split by slug: to identify post boundaries
parts = posts_str.split('slug:')
for part in parts[1:]:
    post = {}
    slug_match = re.search(r'"([^"]+)"', part)
    if slug_match:
        post['slug'] = slug_match.group(1)
    
    # Get fields before next slug or end
    end_idx = re.search(r'\bslug:', part)
    
    for field in ['title', 'excerpt', 'date', 'content']:
        f_match = re.search(rf'{field}:\s*`((?:[^`]|\\`)*)`', part)
        if not f_match:
            f_match = re.search(rf'{field}:\s*"((?:[^"\\]|\\.)*)"', part)
        if f_match:
            post[field] = f_match.group(1)
    
    # Tags
    tags_match = re.search(r'tags:\s*\[(.*?)\]', part, re.DOTALL)
    if tags_match:
        tags_str = tags_match.group(1)
        tags = re.findall(r'"([^"]+)"', tags_str)
        post['tags'] = tags
    
    # Image placeholder
    img_match = re.search(r'imagePlaceholder:\s*"([^"]*)"', part)
    if img_match:
        post['imagePlaceholder'] = img_match.group(1)
    
    if post:
        posts.append(post)

# Output slugs with titles
print(f"Total posts found: {len(posts)}")
print("---")
for p in posts:
    slug = p.get('slug', 'unknown')
    title = p.get('title', 'no title')[:80]
    tags = p.get('tags', [])
    excerpt = (p.get('excerpt', '') or '')[:80]
    content_preview = (p.get('content', '') or '')[:100]
    print(f"Slug: {slug}")
    print(f"Title: {title}")
    print(f"Tags: {', '.join(tags[:5])}")
    print(f"Content length: {len(p.get('content', '') or '')}")
    print(f"Content preview: {content_preview}")
    print("---")
