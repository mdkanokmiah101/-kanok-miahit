#!/usr/bin/env python3
"""Content framework checks for smmsun-seo-case-study."""
import re

with open('src/app/blog/data.js', 'r', encoding='utf-8') as f:
    raw = f.read()

# Find the specific post
start = raw.find('slug: "smmsun-seo-case-study"')
if start == -1:
    print('Post not found!')
    exit(1)

# Find the end - next slug
rest = raw[start:]
next_slug = re.search(r'^\s+slug: "(?!smmsun)', rest, re.MULTILINE)
if next_slug:
    end = start + next_slug.start()
else:
    end = len(raw)

post_raw = raw[start:end]

def extract_field(pattern, text, group=1):
    m = re.search(pattern, text)
    return m.group(group) if m else None

slug = extract_field(r'slug: "([^"]+)"', post_raw)
title = extract_field(r'title: "([^"]+)"', post_raw)
date = extract_field(r'date: "([^"]+)"', post_raw)
author = extract_field(r'author: "([^"]+)"', post_raw)
excerpt = extract_field(r'excerpt:\s*"([^"]+)"', post_raw)
tags_raw = extract_field(r'tags:\s*\[([^\]]+)\]', post_raw)
image_placeholder = extract_field(r'imagePlaceholder:\s*"([^"]+)"', post_raw)

# Extract content
content_m = re.search(r'content: `\n(.+?)`,\n', post_raw, re.DOTALL)
if content_m:
    content = content_m.group(1)
else:
    content = ''

print(f'=== POST METADATA ===')
print(f'slug: {slug}')
print(f'title: {title}')
print(f'date: {date}')
print(f'author: {author}')
print(f'excerpt excerpt: {excerpt[:80] if excerpt else "N/A"}...')
print(f'tags: {tags_raw}')
print(f'imagePlaceholder: {image_placeholder}')
print(f'content length: {len(content)} chars')
print()

# === CHECK 1: TF-IDF Keyword Counts ===
print('=== CHECK 1: TF-IDF KEYWORD COVERAGE ===')
content_lower = content.lower()
full_lower = post_raw.lower()

primary_kws = ['smmsun', 'smm panel', 'seo case study', 'traffic growth', 'organic clicks', 'seo', 'bangladesh', 'dhaka']
for kw in primary_kws:
    c = full_lower.count(kw.lower())
    print(f'  "{kw}": {c} occurrences')

# TF-IDF: primary keyword from title
# "smmsun" - brand keyword - should appear multiple times
# "seo" - topic keyword
print()

# === CHECK 2: ENTITIES ===
print('=== CHECK 2: SEMANTIC ENTITY COVERAGE ===')
entities = {
    'SMMSun': 'SMMSun' in content,
    'Kanok Miah': 'Kanok Miah' in content,
    'kanokmiah.com.bd': 'kanokmiah.com.bd' in content,
    'Bangladesh': 'Bangladesh' in content,
    'Dhaka': 'Dhaka' in content,
    'Instagram': 'Instagram' in content,
    'YouTube': 'YouTube' in content,
    'Facebook': 'Facebook' in content,
    'TikTok': 'TikTok' in content,
    'Google': 'Google' in content,
    'Core Web Vitals': 'Core Web Vitals' in content,
    'LCP': 'LCP' in content,
    'CTR': 'CTR' in content,
    'Schema Markup': 'schema markup' in content_lower,
    'FAQ': 'FAQ' in content or 'faq' in content_lower,
    'SERP': 'SERP' in content,
    'E-E-A-T': 'E-E-A-T' in content,
    'Internal Linking': 'internal linking' in content_lower or 'hub-and-spoke' in content_lower,
    'Meta Description': 'meta description' in content_lower,
    'Content Clusters': 'content clusters' in content_lower or 'content-cluster' in content_lower,
    'Pillar': 'pillar' in content_lower,
}
for entity, present in entities.items():
    print(f'  {"✅" if present else "❌"} {entity}: {"present" if present else "MISSING"}')
missing = [e for e, p in entities.items() if not p]
if missing:
    print(f'  ❌ Missing entities: {missing}')
else:
    print(f'  ✅ All key entities present')
print()

# === CHECK 3: PILLAR LINK ===
print('=== CHECK 3: PILLAR-CLUSTER ALIGNMENT ===')
internal_links = re.findall(r'\((/[^\s)]+)\)', content)
internal_links = [l for l in internal_links if not l.startswith('/`')]
print(f'Internal links found ({len(internal_links)}):')
for link in internal_links:
    print(f'  - {link}')
pillar_links = [l for l in internal_links if '/services/' in l or '/industries/' in l]
print(f'Pillar links: {pillar_links}')
print()

# === CHECK 4: AEO/GEO ===
print('=== CHECK 4: AEO/GEO OPTIMIZATION ===')
headings = re.findall(r'^#{2,3}\s+.*$', content, re.MULTILINE)
print(f'All headings ({len(headings)}):')
for h in headings:
    print(f'  - {h.strip()}')
question_headings = [h for h in headings if '?' in h]
print(f'Question headings: {len(question_headings)}')
# FAQ section check
has_faq_section = 'FAQ' in content or 'faq' in content_lower
print(f'FAQ section present: {has_faq_section}')
print()

# === CHECK 5: INTERNAL LINKS ===
print('=== CHECK 5: INTERNAL LINKING ===')
# Count all internal links (path-based)
all_internal = re.findall(r'\(/[^\s)]+\)', content)
all_internal = [l.strip('()') for l in all_internal if not l.strip('()').startswith('/`')]
unique_internal = set(all_internal)
print(f'Total internal links: {len(all_internal)}')
print(f'Unique internal paths: {len(unique_internal)}')
for l in sorted(unique_internal):
    print(f'  - {l}')
blog_links = [l for l in unique_internal if l.startswith('/blog/')]
service_links = [l for l in unique_internal if l.startswith('/services/')]
location_links = [l for l in unique_internal if l.startswith('/locations/')]
print(f'Blog-to-blog links: {len(blog_links)}')
print(f'Service page links: {len(service_links)}')
print(f'Location page links: {len(location_links)}')
print()

# === CHECK 6: SCHEMA READY ===
print('=== CHECK 6: SCHEMA/METADATA READY ===')
schema_fields = {
    'slug': slug is not None,
    'title': title is not None,
    'date': date is not None,
    'author': author is not None,
    'excerpt': excerpt is not None,
    'tags': tags_raw is not None,
    'imagePlaceholder': image_placeholder is not None,
    'content': len(content) > 0,
}
date_modified = 'dateModified' in post_raw
meta_title = 'metaTitle' in post_raw
meta_desc = 'metaDescription' in post_raw
image_field = 'image:' in post_raw

for field, present in schema_fields.items():
    print(f'  {"✅" if present else "❌"} {field}')
print(f'  {"✅" if date_modified else "❌"} dateModified')
print(f'  {"✅" if meta_title else "❌"} metaTitle')
print(f'  {"✅" if meta_desc else "❌"} metaDescription')
print(f'  {"✅" if image_field else "❌"} image')
print()
print(f'All required fields: {"✅ PASS" if all(schema_fields.values()) else "❌ FAIL"}')
print(f'Schema will render with fallbacks for missing optional fields')
