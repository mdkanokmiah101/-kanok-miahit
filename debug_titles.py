#!/usr/bin/env python3
"""Check various entities across posts."""
import re

with open('src/app/blog/data.js', 'r') as f:
    data = f.read()

slugs = [
    "complete-seo-guide-bangladesh-businesses-2026",
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
    obj_text = None
    lines = data.split('\n')
    slug_idx = None
    for i, line in enumerate(lines):
        if 'slug: "' + slug + '"' in line:
            slug_idx = i
            break
    
    if slug_idx is None:
        continue
    
    # Find title
    title = ""
    for i in range(slug_idx, slug_idx+10):
        if i < len(lines) and 'title:' in lines[i]:
            m = re.search(r'title:\s*"([^"]*)"', lines[i])
            if m:
                title = m.group(1)
            break
    
    print(f'\n=== {slug} ===')
    print(f'Title: {title}')
    
    # Check for digital marketing in various forms
    # Check tags
    tags_line = None
    for i in range(slug_idx, slug_idx+30):
        if i < len(lines) and 'tags:' in lines[i]:
            tags_line = i
            break
    
    tags = ""
    if tags_line:
        # Read tags until ]
        tag_text = ""
        for i in range(tags_line, tags_line+5):
            if i < len(lines):
                tag_text += lines[i]
                if ']' in lines[i]:
                    break
        tags = tag_text
    print(f'Tags: {tags[:120]}')
    
    # Check if title is Bangla
    has_bangla = bool(re.search(r'[\u0980-\u09FF]', title))
    print(f'Has Bangla text: {has_bangla}')
