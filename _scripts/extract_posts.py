#!/usr/bin/env python3
"""Extract specific blog posts from data.js for framework analysis."""
import re
import json

with open('src/app/blog/data.js', 'r') as f:
    content = f.read()

# Find blog post objects - they start with "slug:" and end with "},"
# But template literals make this complex. Let's find posts by slug.

target_slugs = [
    'seo-for-fitness-gyms-bangladesh',
    'seo-for-law-firms-bangladesh',
    'b2b-lead-generation-seo-bangladesh',
    'seo-for-startups-bangladesh',
    'seo-howto-schema-bangladesh',
]

for slug in target_slugs:
    # Find the slug in content
    idx = content.find(f'slug: "{slug}"')
    if idx == -1:
        print(f"Post not found: {slug}")
        continue
    
    # Find start of this blog post object - search backwards for "{"
    start = content.rfind('{', 0, idx)
    
    # Find end - count braces, careful with template literals
    depth = 0
    in_template = False
    end = start
    
    for i in range(start, len(content)):
        ch = content[i]
        if ch == '`':
            in_template = not in_template
        elif not in_template:
            if ch == '{':
                depth += 1
            elif ch == '}':
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break
    
    post_text = content[start:end]
    print(f"\n{'='*80}")
    print(f"POST: {slug}")
    print(f"{'='*80}")
    print(post_text[:100])
    print(f"... [total length: {len(post_text)} chars]")
    print(f"{'='*80}")
