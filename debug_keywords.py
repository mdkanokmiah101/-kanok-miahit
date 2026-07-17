#!/usr/bin/env python3
"""Check actual content keywords for each Bangla post."""
import re

with open('src/app/blog/data.js', 'r') as f:
    data = f.read()

slugs = [
    ("seo-for-facebook-marketplace", "ফেসবুক মার্কেটপ্লেস", "SEO"),
    ("long-tail-keywords-bangladesh", "লং-টেল কীওয়ার্ড", "লং টেল"),
    ("seo-tips-for-business-owners-bd", "SEO টিপস", "ব্যবসা"),
    ("seo-bangla-blog-content-writing", "ব্লগ কন্টেন্ট", "SEO ফ্রেন্ডলি"),
    ("seo-vs-google-ads-bangladesh-business", "SEO", "Google Ads"),
    ("youtube-seo-bangladesh-ranking-tips", "ইউটিউব", "SEO"),
    ("schema-markup-rich-snippets-techniques", "স্কিমা মার্কআপ", "Schema"),
    ("mobile-seo-bangladesh-ranking-strategy", "মোবাইল", "SEO"),
    ("google-search-console-performance-guide", "গুগল সার্চ কনসোল", "Search Console"),
]

for slug, kw1, kw2 in slugs:
    lines = data.split('\n')
    slug_idx = None
    for i, line in enumerate(lines):
        if 'slug: "' + slug + '"' in line:
            slug_idx = i
            break
    
    # Extract content
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
    content_lower = content.lower()
    
    print(f'\n=== {slug} ===')
    for kw in [kw1, kw2, kw1.replace(' ', ''), kw2.replace(' ', '')]:
        if len(kw) > 1:
            c = content.count(kw)
            c_low = content_lower.count(kw.lower())
            print(f'  "{kw}" → {c} (case-insensitive: {c_low})')
