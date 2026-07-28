#!/usr/bin/env python3
"""Refined entity check - just checking if 'link building' or equivalent terms exist."""
import re

with open('/root/kanok-miahit/src/app/blog/data.js', 'r') as f:
    content = f.read()

SLUG = 'seo-case-study-dhaka-businesses-increased-organic-traffic'
idx = content.find(f'    slug: "{SLUG}",')
post_start = content.rfind('{', 0, idx)
content_field_start = content.find('    content: `', post_start)
content_start = content_field_start + len('    content: `')
rest = content[content_start:]
depth = 1
i = 0
while i < len(rest) and depth > 0:
    if rest[i] == '\\' and i + 1 < len(rest):
        i += 2
        continue
    if rest[i] == '`':
        depth -= 1
        if depth == 0:
            break
    i += 1
post_body = rest[:i]
body_lower = post_body.lower()

print("=== Link Building Equivalent Terms Check ===")
terms = {
    'link building': 0,
    'backlink': 0,
    'backlinks': 0,
    'guest post': 0,
    'authority building': 0,
    'referring domain': 0,
    'link profile': 0,
    'niche-relevant backlinks': 0,
    'link building strategies': 0,
}
for term in terms:
    count = body_lower.count(term.lower())
    terms[term] = count
    print(f"  {term:30s}: {count}")

# Also check if "Link Building" appears in tags
header = content[post_start:content_field_start]
tag_match = re.search(r'tags:\s*\[([^\]]+)\]', header)
if tag_match:
    tags_str = tag_match.group(1)
    tags = re.findall(r'"([^"]+)"', tags_str)
    print(f"\nTags: {tags}")
    print(f"'Link Building' in tags: {'Link Building' in tags}")
