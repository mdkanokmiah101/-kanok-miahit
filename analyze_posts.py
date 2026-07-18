#!/usr/bin/env python3
import re
import sys

with open('src/app/blog/data.js', 'r') as f:
    content = f.read()

def extract_post(content, slug):
    start_marker = f'slug: "{slug}"'
    start = content.find(start_marker)
    if start == -1:
        # try single quotes
        start_marker = f"slug: '{slug}'"
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

def analyze_post(post_text, slug):
    if not post_text:
        return None
    
    print(f'\n===== Analyzing: {slug} =====')
    
    title_match = re.search(r'title:\s*"([^"]+)"', post_text)
    title = title_match.group(1) if title_match else 'UNKNOWN'
    
    excerpt_match = re.search(r'excerpt:\s*"([^"]*)"', post_text)
    excerpt = excerpt_match.group(1) if excerpt_match else ''
    
    date_match = re.search(r'date:\s*"([^"]+)"', post_text)
    date = date_match.group(1) if date_match else 'UNKNOWN'
    
    tags_match = re.search(r'tags:\s*\[([^\]]+)\]', post_text)
    tags_str = tags_match.group(1) if tags_match else ''
    tags = [t.strip().strip('"').strip("'") for t in tags_str.split(',')] if tags_str else []
    
    # Extract content - find the content field value
    content_match = re.search(r'content:\s*`\s*\n(.+?)(?=`\s*,?\s*\n\s*\}?)', post_text, re.DOTALL)
    content_text = content_match.group(1) if content_match else ''
    
    print(f'Title: {title}')
    print(f'Date: {date}')
    print(f'Tags: {tags}')
    print(f'Content length: {len(content_text)} chars')
    
    # ----- A. TF-IDF Coverage -----
    if ':' in title:
        keyword = title.split(':')[0].strip()
    else:
        keyword = title.strip()
    
    # For Bengali: the part before colon is the main keyword concept
    keyword_count = content_text.count(keyword)
    # Also try counting without colon part if it appears
    if keyword_count < 2:
        # Maybe use first meaningful word group
        words = keyword.split()
        if len(words) > 1:
            # Try first 2 words
            alt_keyword = ' '.join(words[:2])
            keyword_count = max(keyword_count, content_text.count(alt_keyword))
    
    tfidf_pass = keyword_count >= 5
    print(f'Primary Keyword: "{keyword}"')
    print(f'TF-IDF: {"PASS" if tfidf_pass else "FAIL"} ({keyword_count} occurrences)')
    
    # ----- B. Semantic Entity Coverage -----
    entities = {}
    entities['Bangladesh'] = content_text.count('বাংলাদেশ') + content_text.count('Bangladesh') + content_text.count('Bangladeshi')
    entities['Dhaka'] = content_text.count('ঢাকা') + content_text.count('Dhaka')
    
    # Service-related entities
    entity_checks = [
        ('SEO', content_text.count('SEO') + content_text.count('seo')),
        ('digital marketing', content_text.count('ডিজিটাল মার্কেটিং') + content_text.count('digital marketing')),
        ('Google', content_text.count('Google') + content_text.count('গুগল')),
    ]
    
    print(f'Entities:')
    entity_pass = True
    missing_entities = []
    for name, count in entity_checks:
        status = "PASS" if count > 0 else "MISSING"
        if count == 0:
            missing_entities.append(name)
            entity_pass = False
        print(f'  {name}: {count} ({status})')
    print(f'  Bangladesh: {entities["Bangladesh"]}')
    print(f'  Dhaka: {entities["Dhaka"]}')
    if entities['Dhaka'] == 0:
        missing_entities.append('Dhaka/ঢাকা')
    if entities['Bangladesh'] == 0:
        missing_entities.append('Bangladesh/বাংলাদেশ')
    print(f'  Entity check: {"PASS" if entity_pass and entities["Dhaka"] > 0 and entities["Bangladesh"] > 0 else "FAIL"}')
    if missing_entities:
        print(f'  Missing entities: {missing_entities}')
    
    # ----- D. AEO/GEO: Question headings -----
    # Headings starting with question words (Bengali + English)
    q_pattern = re.compile(r'^#{1,6}\s+(কী|কেন|কখন|কোথায়|কীভাবে|কিভাবে|কেমন|How|What|Why|When|Where|Can|Do|Is|Are|Does|Will|Should)', re.MULTILINE | re.IGNORECASE)
    question_headings = q_pattern.findall(content_text)
    num_qh = len(question_headings)
    aeo_pass = num_qh >= 2
    print(f'AEO/GEO question headings: {num_qh} - {question_headings[:8]}')
    print(f'  AEO/GEO: {"PASS" if aeo_pass else "FAIL"} (need >=2, have {num_qh})')
    
    # ----- E. Internal Linking -----
    internal_links = re.findall(r'/blog/[a-zA-Z0-9-]+', content_text)
    service_links = re.findall(r'/services/[a-zA-Z0-9-]+', content_text)
    location_links = re.findall(r'/locations/[a-zA-Z0-9-]+', content_text)
    industry_links = re.findall(r'/industries/[a-zA-Z0-9-]+', content_text)
    about_links = re.findall(r'/about[^s]', content_text)
    home_links = re.findall(r'(?:"\(/\)"|"\(/"\))', content_text)  # links to /
    
    all_internal_links = internal_links + service_links + location_links + industry_links
    # Count unique internal links properly
    unique_biz_links = set()
    for l in internal_links:
        unique_biz_links.add(l)
    for l in service_links:
        unique_biz_links.add(l)
    for l in location_links:
        unique_biz_links.add(l)
    for l in industry_links:
        unique_biz_links.add(l)
    
    num_int_links = len(unique_biz_links)
    int_pass = num_int_links >= 3
    print(f'Internal links: {num_int_links} unique')
    print(f'  Blog links: {internal_links[:5]}')
    print(f'  Service links: {service_links[:5]}')
    print(f'  Location links: {location_links[:5]}')
    print(f'  Internal linking: {"PASS" if int_pass else "FAIL"} (need >=3, have {num_int_links})')
    
    # ----- C. Pillar-Cluster Alignment -----
    # Check if post links to any comprehensive/guide/pillar page
    pillar_keywords = ['complete-seo-guide', 'seo-guide', 'pillar', 'beginners-guide']
    pillar_link_found = False
    pillar_linked = []
    for pk in pillar_keywords:
        if pk in content_text:
            pillar_link_found = True
            pillar_linked.append(pk)
    print(f'Pillar link: {"PASS" if pillar_link_found else "FAIL"} - Links to: {pillar_linked if pillar_link_found else "None found"}')
    
    # ----- F. Schema Readiness -----
    has_title = title != 'UNKNOWN' and len(title) > 0
    has_excerpt = len(excerpt) > 5
    has_date = date != 'UNKNOWN'
    has_author = 'author' in post_text
    schema_pass = has_title and has_excerpt and has_date and has_author
    print(f'Schema Ready: {"PASS" if schema_pass else "FAIL"}')
    print(f'  Title: {"YES" if has_title else "NO"}')
    print(f'  Excerpt: {"YES" if has_excerpt else "NO"}')
    print(f'  Date: {"YES" if has_date else "NO"}')
    print(f'  Author: {"YES" if has_author else "NO"}')
    
    return {
        'slug': slug,
        'title': title,
        'keyword': keyword,
        'keyword_count': keyword_count,
        'tfidf_pass': tfidf_pass,
        'entity_pass': entity_pass and entities['Bangladesh'] > 0,
        'missing_entities': missing_entities,
        'question_headings': num_qh,
        'aeo_pass': aeo_pass,
        'num_internal_links': num_int_links,
        'int_pass': int_pass,
        'pillar_link_found': pillar_link_found,
        'pillar_linked': pillar_linked,
        'schema_pass': schema_pass,
        'tag_count': len(tags),
    }

# Analyze the 8 most recent posts
recent_slugs = [
    'seo-referral-traffic-bangladesh',
    'seo-page-authority-bangladesh',
    'seo-domain-authority-bangladesh',
    'seo-hubspot-vs-wordpress-bd',
    'seo-content-repurposing-bangladesh',
    'seo-skyscraper-technique-bangladesh',
    'seo-pillar-content-strategy-bd',
    'seo-for-podcast-bangladesh',
]

results = []
for slug in recent_slugs:
    post = extract_post(content, slug)
    result = analyze_post(post, slug)
    if result:
        results.append(result)

print("\n\n===== SUMMARY =====")
print(f"{'Slug':40s} {'TF-IDF':8s} {'Entities':10s} {'Pillar':8s} {'AEO':6s} {'IntLinks':9s} {'Schema':8s}")
print("-"*95)
for r in results:
    tfidf = 'PASS' if r['tfidf_pass'] else 'FAIL'
    ent = 'PASS' if r['entity_pass'] else 'FAIL'
    pillar = 'PASS' if r['pillar_link_found'] else 'FAIL'
    aeo = 'PASS' if r['aeo_pass'] else 'FAIL'
    intl = 'PASS' if r['int_pass'] else 'FAIL'
    schema = 'PASS' if r['schema_pass'] else 'FAIL'
    print(f"{r['slug']:40s} {tfidf:8s} {ent:10s} {pillar:8s} {aeo:6s} {intl:9s} {schema:8s}")
