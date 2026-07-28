#!/usr/bin/env python3
"""Analyze internal links in modified blog posts."""
import re

with open('/root/kanok-miahit/src/app/blog/data.js', 'r') as f:
    content = f.read()

slugs = [
    'geo-optimization-prepare-business-ai-search',
    'seo-garments-textile-industry-b2b-lead-generation',
    'seo-healthcare-medical-clinics-bangladesh',
    'locksmith-dundee-seo-case-study',
    'landlord-certificates-seo-case-study',
    'das-taxis-scotland-seo-case-study',
    'morethanpanel-seo-case-study',
    'smmgen-seo-case-study',
    'smmsun-seo-case-study',
    'mir-cement-seo-case-study',
    'dhaka-apparels-seo-case-study',
    'stealth-windshield-repairs-seo-case-study',
    'seo-expert-vs-seo-agency-dhaka-which-is-right',
    'top-10-seo-mistakes-dhaka-businesses-fix',
    'seo-case-study-dhaka-businesses-increased-organic-traffic',
    'hiring-seo-expert-dhaka-better-roi-than-paid-ads',
    'watchzonebd-seo-case-study'
]

for slug in slugs:
    idx = content.find(f'slug: "{slug}"')
    if idx == -1:
        print(f'NOT FOUND: {slug}')
        continue
    
    # Find the content section of the post
    # Find the content:  marker after the slug
    content_start = content.find('content: `', idx)
    if content_start == -1:
        print(f'NO CONTENT: {slug}')
        continue
    
    content_start += len('content: `')
    # Find end of content
    content_end = content.find('`,\n  }', content_start)
    if content_end == -1:
        content_end = content.find('`,\n}', content_start)
    
    post_content = content[content_start:content_end]
    
    # Count internal links
    blog_links = re.findall(r'/blog/[a-z0-9-]+', post_content)
    serv_links = re.findall(r'/services/[a-z0-9-]+', post_content)
    ind_links = re.findall(r'/industries/[a-z0-9-]+', post_content)
    loc_links = re.findall(r'/locations/[a-z0-9-]+', post_content)
    all_links = blog_links + serv_links + ind_links + loc_links
    unique_links = set(all_links)
    
    has_pillar = any('/blog/complete-seo-guide' in l for l in unique_links)
    
    # Count question headings (## or ### level that end with ?)
    q_headings_h2 = re.findall(r'^## [A-Z].*\?', post_content, re.MULTILINE)
    q_headings_h3 = re.findall(r'^### [A-Z].*\?', post_content, re.MULTILINE)
    
    # Also count any line starting with ## that ends with ?
    q_headings_all = re.findall(r'^##[^#].*\?', post_content, re.MULTILINE)
    q_headings_all += re.findall(r'^###[^#].*\?', post_content, re.MULTILINE)
    
    total_q = len(q_headings_all)
    
    print(f'=== {slug} ===')
    print(f'  Internal links: blog={len(blog_links)}, serv={len(serv_links)}, ind={len(ind_links)}, loc={len(loc_links)}, unique={len(unique_links)}')
    print(f'  Pillar link to complete-seo-guide: {"YES" if has_pillar else "NO"}')
    if unique_links:
        print(f'  Unique URLs: {sorted(unique_links)}')
    print(f'  Q headings: {total_q}')
    if q_headings_all:
        for h in q_headings_all[:5]:
            print(f'    - {h.strip()}')
    print()
