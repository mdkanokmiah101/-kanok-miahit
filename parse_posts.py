#!/usr/bin/env python3
"""
Parse blog posts from data.js and run framework checks.
"""
import re
import json
import sys

# Read the file
with open('src/app/blog/data.js', 'r') as f:
    raw = f.read()

# Parse posts by finding each post object
# Strategy: split by "slug:" and extract each post
posts = []
# Split on "  {\n    slug:" or variations
sections = re.split(r'\n\s*\{\s*\n\s*slug:\s*"', raw)

for i, section in enumerate(sections):
    if i == 0:
        continue  # Skip content before first post
    
    if not section.strip():
        continue
    
    slug = section.split('"')[0]
    
    # Find the closing brace of this post object
    # We need to find matching braces
    brace_depth = 0
    post_end = -1
    for j, ch in enumerate('{' + section):
        if ch == '{':
            brace_depth += 1
        elif ch == '}':
            brace_depth -= 1
            if brace_depth == 0:
                post_end = j
                break
    
    if post_end == -1:
        print(f"WARNING: Could not find end of post for slug={slug}")
        continue
    
    post_text = section[:post_end]
    
    # Extract title
    title_m = re.search(r'title:\s*"([^"]*)"', post_text)
    title = title_m.group(1) if title_m else slug
    
    # Extract tags
    tags_m = re.search(r'tags:\s*\[([^\]]+)\]', post_text)
    tags = []
    if tags_m:
        tags = re.findall(r'"([^"]*)"', tags_m.group(1))
    
    # Extract excerpt
    excerpt_m = re.search(r'excerpt:\s*"([^"]*)"', post_text)
    excerpt = excerpt_m.group(1) if excerpt_m else ""
    
    # Extract date
    date_m = re.search(r'date:\s*"([^"]*)"', post_text)
    date = date_m.group(1) if date_m else ""
    
    # Extract dateModified
    date_mod_m = re.search(r'dateModified:\s*"([^"]*)"', post_text)
    date_modified = date_mod_m.group(1) if date_mod_m else ""
    
    # Extract imagePlaceholder
    img_m = re.search(r'imagePlaceholder:\s*"([^"]*)"', post_text)
    image = img_m.group(1) if img_m else ""
    
    # Extract content (between backticks)
    # Find content: `
    content_start = post_text.find('content: `')
    if content_start >= 0:
        # Find the opening backtick
        bt_start = post_text.index('`', content_start)
        # Find the closing backtick (followed by , or )
        bt_end = post_text.rindex('`')
        if bt_end > bt_start:
            post_content = post_text[bt_start+1:bt_end]
        else:
            post_content = ""
    else:
        post_content = ""
    
    posts.append({
        'slug': slug,
        'title': title,
        'tags': tags,
        'excerpt': excerpt,
        'date': date,
        'dateModified': date_modified,
        'image': image,
        'content': post_content
    })

print(f"Parsed {len(posts)} posts")

# Save
with open('/tmp/posts_data.json', 'w') as f:
    json.dump(posts, f, indent=2, ensure_ascii=False)

# Print first few slugs
for p in posts[:5]:
    print(f"  {p['slug']}: {p['title'][:60]}... content_len={len(p['content'])}")
