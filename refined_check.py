#!/usr/bin/env python3
"""Enhanced analysis with better pillar link detection and refined entity check."""
import re

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

# Known pillar page slugs on this site
pillar_slugs = [
    'complete-seo-guide-bangladesh-businesses-2026',
    'seo-bangla-beginners-guide-google-ranking',
    'content-marketing-strategy-bangladeshi-brands-seo',
]

# Refined entity categories
refined_entity_map = {
    'Bangladesh': ['বাংলাদেশ', 'Bangladesh', 'Bangladeshi'],
    'Dhaka': ['ঢাকা', 'Dhaka'],
    'SEO': ['SEO', 'seo', 'সার্চ ইঞ্জিন অপটিমাইজেশন'],
    'Marketing': ['মার্কেটিং', 'marketing', 'ডিজিটাল মার্কেটিং', 'digital marketing'],
}

def count_any(text, terms):
    return sum(text.count(t) for t in terms)

for slug in slugs:
    post = extract_post(content, slug)
    if not post:
        continue
    
    # Extract fields
    title = re.search(r'title:\s*"([^"]+)"', post)
    title = title.group(1) if title else '?'
    
    tags_m = re.search(r'tags:\s*\[([^\]]+)\]', post)
    tags_str = tags_m.group(1) if tags_m else ''
    tags = [t.strip().strip('"').strip("'") for t in tags_str.split(',')] if tags_str else []
    
    cm = re.search(r'content:\s*`\s*\n(.+?)(?=`\s*,?\s*\n\s*\}?)', post, re.DOTALL)
    content_text = cm.group(1) if cm else ''
    
    print(f'\n===== {slug} =====')
    print(f'Title: {title}')
    print(f'Tags: {tags}')
    
    # A. TF-IDF - primary keyword from title (before colon)
    if ':' in title:
        keyword = title.split(':')[0].strip()
    else:
        keyword = title.strip()
    kc = content_text.count(keyword)
    print(f'TF-IDF: keyword="{keyword}" count={kc} {"PASS" if kc >= 5 else "FAIL"}')
    
    # B. Entities
    print('Entities:')
    for cat, terms in refined_entity_map.items():
        c = count_any(content_text, terms)
        status = 'PASS' if c > 0 else 'FAIL'
        print(f'  {cat}: {c} ({status})')
    
    # C. Pillar links - check for links to known pillar pages OR cluster-to-pillar patterns
    pillar_links_found = []
    for ps in pillar_slugs:
        if ps in content_text:
            pillar_links_found.append(ps)
    # Also check for "/blog/complete-seo-guide" or similar
    if '/blog/complete-seo-guide' in content_text or 'complete-seo-guide' in content_text:
        if 'complete-seo-guide-bangladesh-businesses-2026' not in pillar_links_found:
            pillar_links_found.append('complete-seo-guide')
    print(f'Pillar link: {"PASS" if pillar_links_found else "FAIL"} (found: {pillar_links_found if pillar_links_found else "none"})')
    
    # D. AEO/GEO question headings
    qpattern = re.compile(r'^#{1,6}\s+(কী|কেন|কখন|কোথায়|কীভাবে|কিভাবে|কেমন|How|What|Why|When|Where|Can|Do|Is|Are|Does|Will|Should)', re.MULTILINE | re.IGNORECASE)
    qh = qpattern.findall(content_text)
    print(f'AEO/GEO: {len(qh)} question headings {"PASS" if len(qh) >= 2 else "FAIL"} - {qh[:5]}')
    
    # E. Internal links
    blog_links = re.findall(r'/blog/[a-zA-Z0-9-]+', content_text)
    service_links = re.findall(r'/services/[a-zA-Z0-9-]+', content_text)
    location_links = re.findall(r'/locations/[a-zA-Z0-9-]+', content_text)
    industry_links = re.findall(r'/industries/[a-zA-Z0-9-]+', content_text)
    
    all_links_set = set()
    for l in blog_links: all_links_set.add(l)
    for l in service_links: all_links_set.add(l)
    for l in location_links: all_links_set.add(l)
    for l in industry_links: all_links_set.add(l)
    
    print(f'Internal links: {len(all_links_set)} unique {"PASS" if len(all_links_set) >= 3 else "FAIL"}')
    print(f'  Blog links: {blog_links[:4]}')
    print(f'  Service links: {service_links[:3]}')
    print(f'  Location links: {location_links[:3]}')
    
    # F. Schema
    has_title = title != '?'
    has_excerpt = 'excerpt:' in post and len(re.search(r'excerpt:\s*"([^"]*)"', post).group(1)) > 5 if re.search(r'excerpt:\s*"([^"]*)"', post) else False
    has_date = 'date:' in post
    has_author = 'author:' in post
    print(f'Schema: title={has_title}, excerpt={has_excerpt}, date={has_date}, author={has_author} -> {"PASS" if all([has_title, has_excerpt, has_date, has_author]) else "FAIL"}')
