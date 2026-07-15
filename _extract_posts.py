#!/usr/bin/env python3
import re, sys, json

with open('src/app/blog/data.js') as f:
    content = f.read()

# Find all post objects by finding the slug line, then walking back for start and forward for end
# Better approach: split on complete post objects
lines = content.split('\n')
posts = []
i = 0
while i < len(lines):
    line = lines[i]
    # Find start of a post object: a line that's just "  {" or "{\n"
    stripped = line.strip()
    if stripped == '{':
        # Walk forward to find matching closing brace
        depth = 0
        j = i
        while j < len(lines):
            for ch in lines[j]:
                if ch == '{':
                    depth += 1
                elif ch == '}':
                    depth -= 1
            j += 1
            if depth <= 0:
                break
        post_text = '\n'.join(lines[i:j])
        posts.append(post_text)
        i = j
    else:
        i += 1

print(f"Found {len(posts)} posts")
for p in posts:
    slug_match = re.search(r'slug:\s*"([^"]+)"', p)
    date_match = re.search(r'date:\s*"([^"]+)"', p)
    title_match = re.search(r'title:\s*"([^"]+)"', p)
    tags_match = re.search(r'tags:\s*\[([^\]]+)\]', p)
    if slug_match:
        slug = slug_match.group(1)
        date = date_match.group(1) if date_match else ''
        title = title_match.group(1) if title_match else ''
        tags_str = tags_match.group(1) if tags_match else ''
        tags = [t.strip().strip('"') for t in tags_str.split(',')] if tags_str else []
        
        # Only posts from 2026-07-14 or later, OR locksmith-dundee
        if date >= '2026-07-14' or slug == 'locksmith-dundee-seo-case-study':
            print(f"\n=== POST: {slug} ===")
            print(f"TITLE: {title}")
            print(f"DATE: {date}")
            print(f"TAGS: {tags}")
            
            # Extract content field
            content_match = re.search(r'content:\s*`(.*?)`', p, re.DOTALL)
            if content_match:
                body = content_match.group(1)
                print(f"CONTENT LENGTH: {len(body)} chars")
                print(f"CONTENT (first 500): {body[:500]}")
            else:
                print("CONTENT: NOT FOUND")
                # Try alternate content format
                lines_p = p.split('\n')
                in_content = False
                content_lines = []
                for cl in lines_p:
                    if 'content:' in cl and '`' in cl:
                        in_content = True
                        idx = cl.find('`')
                        if idx >= 0:
                            content_lines.append(cl[idx+1:])
                    elif in_content:
                        if '`' in cl:
                            content_lines.append(cl[:cl.find('`')])
                            break
                        else:
                            content_lines.append(cl)
                if content_lines:
                    body = '\n'.join(content_lines)
                    print(f"CONTENT LENGTH (alt): {len(body)} chars")
