#!/usr/bin/env python3
"""Verify AEO/GEO for Bangla posts - look for Bangla question headings."""
import re

with open('src/app/blog/data.js', 'r') as f:
    data = f.read()

slugs = [
    "seo-for-facebook-marketplace",
    "long-tail-keywords-bangladesh",
    "seo-tips-for-business-owners-bd",
    "seo-bangla-blog-content-writing",
    "seo-vs-google-ads-bangladesh-business",
    "youtube-seo-bangladesh-ranking-tips",
    "schema-markup-rich-snippets-techniques",
    "mobile-seo-bangladesh-ranking-strategy",
    "google-search-console-performance-guide",
]

for slug in slugs:
    lines = data.split('\n')
    slug_idx = None
    for i, line in enumerate(lines):
        if 'slug: "' + slug + '"' in line:
            slug_idx = i
            break
    
    in_content = False
    content_lines = []
    for i in range(slug_idx, len(lines)):
        if 'content: `' in lines[i]:
            in_content = True
            continue
        if in_content:
            if lines[i].strip().startswith('`'):
                break
            content_lines.append(lines[i])
    
    content = '\n'.join(content_lines)
    
    # Find all headings
    headings = re.findall(r'^#{2,4}\s+(.+)', content, re.MULTILINE)
    
    # English question words
    en_q = [h for h in headings if re.match(r'(How|What|Why|When|Where|Can|Do|Is|Are)\b', h, re.IGNORECASE)]
    
    # Bangla question words
    bn_q = [h for h in headings if re.search(r'^(কি|কেন|কীভাবে|কোথায়|কখন|কত|কে|কার|কোন|কোনটি)', h)]
    
    # Also check headings with question marks
    q_mark = [h for h in headings if '?' in h]
    
    print(f'{slug}:')
    print(f'  Total headings: {len(headings)}')
    print(f'  English Q headings: {len(en_q)}')
    print(f'  Bangla Q headings: {len(bn_q)}')
    print(f'  Headings with ?: {len(q_mark)}')
    if headings:
        print(f'  Sample headings: {headings[:5]}')
    print()
