#!/usr/bin/env python3
"""Final framework analysis for modified posts."""
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

def extract_post(slug):
    idx = content.find(f'slug: "{slug}"')
    if idx == -1:
        return None
    
    # Get title
    title_match = re.search(r'title:\s*"([^"]+)"', content[idx:idx+200])
    title = title_match.group(1) if title_match else "Unknown"
    
    # Get excerpt
    excerpt_match = re.search(r'excerpt:\s*\n\s*"([^"]+)"', content[idx:idx+300])
    excerpt = excerpt_match.group(1) if excerpt_match else ""
    if not excerpt:
        excerpt_match = re.search(r'excerpt:\s*"([^"]+)"', content[idx:idx+300])
        excerpt = excerpt_match.group(1) if excerpt_match else ""
    
    # Get date
    date_match = re.search(r'date:\s*"([^"]+)"', content[idx:idx+100])
    date = date_match.group(1) if date_match else ""
    
    # Get tags
    tag_match = re.search(r'tags:\s*\[(.*?)\]', content[idx:idx+300], re.DOTALL)
    tags = re.findall(r'"([^"]+)"', tag_match.group(1)) if tag_match else []
    
    # Get full content
    c_start = content.find('content: `', idx)
    if c_start == -1:
        return None
    c_start += len('content: `')
    c_end = content.find('`,\n  }', c_start)
    if c_end == -1:
        c_end = content.find('`,\n}', c_start)
    
    post_content = content[c_start:c_end]
    
    return {
        'slug': slug,
        'title': title,
        'excerpt': excerpt,
        'date': date,
        'tags': tags,
        'content': post_content
    }

# Manual TF-IDF keyword analysis
# For each post, determine the primary keyword from the title
# and count its occurrences in the content

keyword_mappings = {
    'geo-optimization-prepare-business-ai-search': {
        'keywords': ['geo optimization', 'generative engine optimization', 'geo']
    },
    'seo-garments-textile-industry-b2b-lead-generation': {
        'keywords': ['garments and textile seo', 'garments textile seo', 'seo for garments']
    },
    'seo-healthcare-medical-clinics-bangladesh': {
        'keywords': ['healthcare seo', 'medical seo', 'seo for healthcare']
    },
    'locksmith-dundee-seo-case-study': {
        'keywords': ['locksmith dundee', 'locksmith seo', 'dundee locksmith']
    },
    'landlord-certificates-seo-case-study': {
        'keywords': ['landlord certificates', 'landlord certification seo']
    },
    'das-taxis-scotland-seo-case-study': {
        'keywords': ['das taxis', 'taxis scotland seo']
    },
    'morethanpanel-seo-case-study': {
        'keywords': ['morethanpanel seo', 'morethanpanel case study']
    },
    'smmgen-seo-case-study': {
        'keywords': ['smmgen seo', 'smmgen case study']
    },
    'smmsun-seo-case-study': {
        'keywords': ['smmsun seo', 'smmsun case study']
    },
    'mir-cement-seo-case-study': {
        'keywords': ['mir cement', 'mir cement seo']
    },
    'dhaka-apparels-seo-case-study': {
        'keywords': ['dhaka apparels', 'dhaka apparels seo']
    },
    'stealth-windshield-repairs-seo-case-study': {
        'keywords': ['stealth windshield', 'stealth windshield repairs']
    },
    'seo-expert-vs-seo-agency-dhaka-which-is-right': {
        'keywords': ['seo expert vs seo agency', 'seo expert dhaka']
    },
    'top-10-seo-mistakes-dhaka-businesses-fix': {
        'keywords': ['seo mistakes', 'dhaka seo mistakes']
    },
    'seo-case-study-dhaka-businesses-increased-organic-traffic': {
        'keywords': ['seo case study', 'dhaka businesses organic traffic']
    },
    'hiring-seo-expert-dhaka-better-roi-than-paid-ads': {
        'keywords': ['hiring seo expert', 'seo roi', 'seo better roi']
    },
    'watchzonebd-seo-case-study': {
        'keywords': ['watchzonebd seo', 'watchzonebd case study']
    }
}

for slug in slugs:
    post = extract_post(slug)
    if not post:
        print(f"CANNOT EXTRACT: {slug}")
        continue
    
    content_lower = post['content'].lower()
    
    # TF-IDF: try each keyword
    best_kw = ''
    best_count = 0
    for kw in keyword_mappings[slug]['keywords']:
        count = content_lower.count(kw.lower())
        if count > best_count:
            best_count = count
            best_kw = kw
    
    # Entities
    has_dhaka = 'dhaka' in content_lower
    has_bangladesh = 'bangladesh' in content_lower
    has_service_keyword = any(s in content_lower for s in ['service', 'services'])
    
    # Pillar link
    has_pillar = '/blog/complete-seo-guide-bangladesh-businesses-2026' in post['content']
    
    # Q headings
    q_heads = re.findall(r'^##[^#].*\?', post['content'], re.MULTILINE)
    q_heads += re.findall(r'^###[^#].*\?', post['content'], re.MULTILINE)
    
    # Internal links
    all_links = re.findall(r'(/blog/[a-z0-9-]+|/services/[a-z0-9-]+|/industries/[a-z0-9-]+|/locations/[a-z0-9-]+)', post['content'])
    unique_links = set(all_links)
    
    # Schema
    has_excerpt = len(post['excerpt']) > 20
    has_date = bool(post['date'])
    
    print(f"=== {slug} ===")
    print(f"  Title: {post['title']}")
    print(f"  A. TF-IDF: best kw='{best_kw}' = {best_count} occ {'PASS' if best_count >= 5 else 'FLAG'}")
    print(f"  B. Entities: Dhaka={has_dhaka}, BD={has_bangladesh}, Services={has_service_keyword} {'PASS' if has_dhaka and has_bangladesh else 'FLAG'}")
    print(f"  C. Pillar link to complete-seo-guide: {'YES' if has_pillar else 'NO'} {'PASS' if has_pillar else 'FLAG'}")
    print(f"  D. AEO/GEO: {len(q_heads)} question headings {'PASS' if len(q_heads) >= 2 else 'FLAG'}")
    print(f"  E. Internal links: {len(unique_links)} unique {'PASS' if len(unique_links) >= 3 else 'FLAG'}")
    print(f"  F. Schema: excerpt={'YES' if has_excerpt else 'NO'}, date={'YES' if has_date else 'NO'} {'PASS' if has_excerpt and has_date else 'FLAG'}")
    print()
