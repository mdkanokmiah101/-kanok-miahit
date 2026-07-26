#!/usr/bin/env python3
"""Check 'other' internal links to see if any match blog slugs without /blog/ prefix."""
import re
import json

with open('/root/kanok-miahit/src/app/blog/data.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Get all slugs
all_slugs = [m.group(1) for m in re.finditer(r'^\s{4}slug:\s*"([^"]+)"', content, re.MULTILINE)]
seen = set()
unique_slugs = []
for s in all_slugs:
    if s not in seen:
        seen.add(s)
        unique_slugs.append(s)
slug_set = set(unique_slugs)

print(f"Total unique slugs: {len(unique_slugs)}")

# Find all internal links that are in the 'other' category and check if they match slugs
slug_pattern = re.compile(r'^\s{4}slug:\s*"([^"]+)"', re.MULTILINE)
slug_matches = list(slug_pattern.finditer(content))

other_links_all = []

for i, match in enumerate(slug_matches):
    slug = match.group(1)
    start_pos = match.start()
    brace_start = content.rfind('{', 0, start_pos)
    
    if i + 1 < len(slug_matches):
        next_start = slug_matches[i + 1].start()
        end_pos = content.find('\n  },', brace_start, next_start)
        if end_pos == -1:
            end_pos = content.find('\n  }', brace_start, next_start)
        if end_pos != -1:
            end_pos += 5
        else:
            end_pos = content.rfind('}', brace_start, next_start)
            if end_pos != -1:
                end_pos += 1
    else:
        end_pos = content.find('\n];', start_pos)
        if end_pos != -1:
            end_pos += 3
    
    if brace_start >= 0 and end_pos > brace_start:
        post_text = content[brace_start:end_pos]
        
        # Extract content
        cs = post_text.find('content: `')
        if cs == -1:
            continue
        cs += len('content: `')
        ce = post_text.rfind('`,\n')
        if ce == -1:
            ce = post_text.rfind('`,')
        if ce == -1:
            ce = post_text.rfind('`')
        if ce <= cs:
            continue
        content_str = post_text[cs:ce]
        
        # Find all markdown links with internal paths
        md_links = re.findall(r'\[([^\]]*)\]\(([^)]+)\)', content_str)
        for text, url in md_links:
            url = url.strip()
            if url.startswith('/') and not url.startswith('/blog/') and not url.startswith('/services/') and not url.startswith('/industries/') and not url.startswith('/locations/') and url not in ['/about', '/contact', '/']:
                # Check if path matches a slug
                path = url.rstrip('/')
                if path.startswith('/'):
                    candidate = path[1:]
                else:
                    candidate = path
                if candidate in slug_set:
                    other_links_all.append((slug, url, candidate))

print(f"\nOther internal links that match blog slugs (no /blog/ prefix):")
for source, link, matched_slug in other_links_all:
    print(f"  [{source}] {link} -> matches slug '{matched_slug}'")
print(f"Total: {len(other_links_all)}")
