#!/usr/bin/env python3
import re
import sys

with open('src/app/blog/data.js', 'r') as f:
    content = f.read()

slugs = [
    'seo-referral-traffic-bangladesh',
    'seo-page-authority-bangladesh',
    'seo-domain-authority-bangladesh',
    'seo-hubspot-vs-wordpress-bd',
    'seo-content-repurposing-bangladesh',
    'seo-skyscraper-technique-bangladesh',
    'seo-pillar-content-strategy-bd',
    'seo-for-podcast-bangladesh',
]

def extract_post(content, slug):
    start_marker = 'slug: "' + slug + '"'
    start = content.find(start_marker)
    if start == -1:
        return None
    post_start = content.rfind('{', 0, start)
    brace_count = 0
    post_end = post_start
    for i in range(post_start, len(content)):
        if content[i] == '{':
            brace_count += 1
        elif content[i] == '}':
            brace_count -= 1
            if brace_count == 0:
                post_end = i + 1
                break
    return content[post_start:post_end]

for slug in slugs:
    post = extract_post(content, slug)
    if not post:
        continue
    
    # Extract content field
    cm = re.search(r'content:\s*`\s*\n(.+?)(?=`\s*,?\s*\n\s*\}?)', post, re.DOTALL)
    content_text = cm.group(1) if cm else ''
    
    line_count = content_text.count('\n')
    word_count = len(content_text.split())
    
    # Market-related terms
    terms_dict = {
        'digital_marketing': ['ডিজিটাল মার্কেটিং', 'digital marketing'],
        'online_marketing': ['অনলাইন মার্কেটিং', 'online marketing'],
        'marketing_generic': ['মার্কেটিং', 'marketing'],
        'seo': ['SEO', 'seo'],
        'google': ['Google', 'গুগল'],
        'bangladesh': ['বাংলাদেশ', 'Bangladesh'],
        'dhaka': ['ঢাকা', 'Dhaka'],
        'chittagong': ['চট্টগ্রাম', 'Chittagong'],
        'sylhet': ['সিলেট', 'Sylhet'],
        'social_media': ['সোশ্যাল মিডিয়া', 'social media', 'ফেসবুক', 'Facebook', 'ইউটিউব', 'YouTube'],
        'content': ['কন্টেন্ট', 'content'],
        'link_building': ['লিংক বিল্ডিং', 'link building', 'ব্যাকলিংক', 'backlink'],
    }
    
    print(f'\n--- {slug} ---')
    print(f'Size: ~{line_count} lines, ~{word_count} words')
    for category, terms in terms_dict.items():
        count = sum(content_text.count(t) for t in terms)
        if count > 0:
            print(f'  {category}: {count}')
        else:
            print(f'  {category}: 0 [MISSING]')
