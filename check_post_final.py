#!/usr/bin/env python3
"""
Comprehensive check for blog post: why-md-kanok-miah-is-the-best-seo-expert-in-dhaka-bangladesh
"""
import re, json, math
from collections import Counter

# Read the data file
with open('/root/kanok-miahit/src/app/blog/data.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the post - locate by slug
slug = 'why-md-kanok-miah-is-the-best-seo-expert-in-dhaka-bangladesh'
# Find the slug line
slug_idx = content.find(f'slug: "{slug}"')
if slug_idx == -1:
    print(f"ERROR: Could not find slug '{slug}'")
    exit(1)

# Find the opening brace for this post (go backwards)
start_idx = content.rfind('{', 0, slug_idx)
# Find the closing brace (go forwards) - need to count braces
brace_count = 0
end_idx = slug_idx
for i in range(slug_idx, len(content)):
    if content[i] == '{':
        brace_count += 1
    elif content[i] == '}':
        brace_count -= 1
        if brace_count == 0:
            end_idx = i + 1
            break

post_text = content[start_idx:end_idx]

print("=" * 70)
print("FULL COMPREHENSIVE AUDIT REPORT")
print(f"Post: {slug}")
print("=" * 70)

# 1. Extract metadata
print("\n## 1. METADATA")

# Title
m = re.search(r'title:\s*"([^"]+)"', post_text)
title = m.group(1) if m else "NOT FOUND"
print(f"   Title: {title}")

# Date
m = re.search(r'date:\s*"([^"]+)"', post_text)
date = m.group(1) if m else "NOT FOUND"
print(f"   Date: {date}")

# DateModified
m = re.search(r'dateModified:\s*"([^"]+)"', post_text)
date_mod = m.group(1) if m else "None"
print(f"   Last Modified: {date_mod}")

# Author
m = re.search(r'author:\s*"([^"]+)"', post_text)
author = m.group(1) if m else "NOT FOUND"
print(f"   Author: {author}")

# Excerpt
m = re.search(r'excerpt:\s*"([^"]+)"', post_text)
excerpt = m.group(1) if m else "NOT FOUND"
print(f"   Excerpt: {excerpt[:80]}...")

# Tags
tags = []
m = re.search(r'tags:\s*\[([^\]]+)\]', post_text)
if m:
    tags = [t.strip().strip('"') for t in m.group(1).split(',')]
    print(f"   Tags ({len(tags)}): {tags}")

# FAQs
faq_count = post_text.count('question:')
print(f"   FAQ entries: {faq_count}")

# Content - extract between the backticks
content_match = re.search(r'content:\s*`\n(.*?)`', post_text, re.DOTALL)
if content_match:
    blog_content = content_match.group(1)
else:
    # Try alternate pattern
    content_match = re.search(r'content:\s*`(.*?)`', post_text, re.DOTALL)
    blog_content = content_match.group(1) if content_match else ""

print(f"\n## 2. CONTENT ANALYSIS")

# Word count
words = blog_content.split()
word_count = len(words)
print(f"   Word count: {word_count}")

# Headings
h2 = re.findall(r'^##\s+(.+)$', blog_content, re.MULTILINE)
h3 = re.findall(r'^###\s+(.+)$', blog_content, re.MULTILINE)
h4 = re.findall(r'^####\s+(.+)$', blog_content, re.MULTILINE)
print(f"   H2 headings: {len(h2)}")
print(f"   H3 headings: {len(h3)}")
print(f"   H4 headings: {len(h4)}")

# Question headings (AEO/GEO)
q_headings = [h for h in h2 + h3 + h4 if h.strip().startswith(('How', 'What', 'Why', 'Where', 'When', 'Which', 'Who', 'Does', 'Can', 'Is', 'Are', 'Do'))]
print(f"   Question headings (AEO/GEO): {len(q_headings)}")
for qh in q_headings:
    print(f"     - {qh.strip()}")

# 3. TF-IDF / KEYWORD ANALYSIS
print(f"\n## 3. TF-IDF / KEYWORD ANALYSIS")

# Primary keyword: "SEO expert in Dhaka" or "best SEO expert in Dhaka"
primary_kw = "seo expert in dhaka"
primary_kw2 = "seo expert dhaka"
primary_kw3 = "best seo expert dhaka"

def count_kw(text, kw):
    return len(re.findall(re.escape(kw), text, re.IGNORECASE))

c1 = count_kw(blog_content, primary_kw)
c2 = count_kw(blog_content, primary_kw2)
c3 = count_kw(blog_content, primary_kw3)
print(f"   'SEO expert in Dhaka': {c1} occurrences")
print(f"   'SEO expert Dhaka': {c2} occurrences")
print(f"   'best SEO expert Dhaka': {c3} occurrences")

# Check tags used in content
print(f"\n   Tag usage in content:")
for tag in tags:
    cnt = count_kw(blog_content, tag.lower())
    status = "✅" if cnt >= 3 else "⚠️" if cnt >= 1 else "❌"
    print(f"   {status} '{tag}': {cnt} occurrences")

# 4. ENTITY ANALYSIS
print(f"\n## 4. ENTITY ANALYSIS")

key_entities = [
    "Dhaka", "Bangladesh", "Google", "SEO", "Local SEO", 
    "Technical SEO", "GEO", "Google Business Profile", 
    "E-commerce", "Link Building", "Canonical", "Schema",
    "Core Web Vitals", "EEAT", "Khan IT", "CloudMatrix Tech",
    "Walton Plaza", "LinkedIn", "250+ hours", "108 verified"
]

for entity in key_entities:
    cnt = count_kw(blog_content, entity.lower())
    if cnt > 0:
        print(f"   ✅ '{entity}': {cnt} occurrences")

# Check for missing important entities
missing = []
for entity in ["EEAT", "E-E-A-T"]:
    if count_kw(blog_content, entity.lower()) == 0:
        missing.append(entity)
if missing:
    for m in missing:
        print(f"   ❌ '{m}': NOT FOUND")

# 5. INTERNAL LINK ANALYSIS
print(f"\n## 5. INTERNAL LINK ANALYSIS")

# Find all internal links (/path/)
internal_links = re.findall(r'\((/[^)]+)\)', blog_content)
internal_links = [l for l in internal_links if l.startswith(('/blog/', '/services/', '/locations/', '/about', '/contact', '/industries/'))]
# Also find links without parentheses (markdown style may vary)
internal_links += re.findall(r'href="([^"]+)"', blog_content)

unique_links = list(set(internal_links))
print(f"   Total internal links: {len(internal_links)}")
print(f"   Unique internal links: {len(unique_links)}")

for link in sorted(unique_links):
    cnt = internal_links.count(link)
    print(f"     - {link} (x{cnt})")

# Check for pillar link requirement
required_pillar = '/blog/geo-optimization-prepare-business-ai-search'
pillar_found = required_pillar in internal_links
print(f"\n   🏛️ Pillar link to '{required_pillar}': {'✅ FOUND' if pillar_found else '❌ MISSING'}")

# Check for case study pillar (alternative)
required_pillar2 = '/blog/seo-case-study-dhaka-businesses-increased-organic-traffic'
pillar_found2 = required_pillar2 in internal_links
print(f"   🏛️ Pillar link to '{required_pillar2}': {'✅ FOUND' if pillar_found2 else 'NOT NEEDED (case study pillar)'}")

# 6. SCHEMA / STRUCTURED DATA READINESS
print(f"\n## 6. SCHEMA READINESS")

# Check metadata completeness
schema_checks = {
    "title": title != "NOT FOUND",
    "excerpt": excerpt != "NOT FOUND",
    "date": date != "NOT FOUND",
    "author": author != "NOT FOUND",
    "tags": len(tags) > 0,
    "faqs": faq_count >= 3,
    "dateModified": date_mod != "None"
}
for check, status in schema_checks.items():
    print(f"   {'✅' if status else '❌'} {check}")

print(f"\n   Schema types present in content:")
schema_types_found = []
if 'LocalBusiness' in blog_content or 'LocalBusiness' in post_text:
    schema_types_found.append('LocalBusiness')
if 'Organization' in blog_content or 'Organization' in post_text:
    schema_types_found.append('Organization')
if 'Article' in blog_content or 'Article' in post_text:
    schema_types_found.append('Article')
if 'FAQ' in blog_content or 'FAQ' in post_text:
    schema_types_found.append('FAQ')
if 'Product' in blog_content or 'Product' in post_text:
    schema_types_found.append('Product')
if 'BreadcrumbList' in blog_content or 'BreadcrumbList' in post_text:
    schema_types_found.append('BreadcrumbList')
for s in schema_types_found:
    print(f"   ✅ {s} mentioned")

# 7. AEO/GEO READINESS
print(f"\n## 7. AEO/GEO READINESS")

print(f"   Question headings: {len(q_headings)} (target: >= 2)")
print(f"   Status: ✅ PASS" if len(q_headings) >= 2 else f"   Status: ❌ FAIL")

# Check FAQ schema
print(f"   FAQ entries (in data): {faq_count} (target: >= 3)")

# Check entity density
total_entities = sum(1 for e in key_entities if count_kw(blog_content, e.lower()) > 0)
entity_density = round(total_entities / (word_count / 100), 2) if word_count > 0 else 0
print(f"   Entity count: {total_entities}")
print(f"   Entity density: {entity_density} per 100 words")

# Check if post is in geo_ready list
with open('/root/kanok-miahit/blog_aeo_geo_analysis_output.json') as f:
    geo_data = json.load(f)
is_geo_ready = slug in geo_data.get('geo_ready_posts', [])
print(f"   GEO Ready (from analysis): {'✅ YES' if is_geo_ready else '❌ NO'}")

# 8. PILLAR-CLUSTER ALIGNMENT
print(f"\n## 8. PILLAR-CLUSTER ALIGNMENT")

# Read cluster map
with open('/root/kanok-miahit/audit/cluster_map.md') as f:
    cluster_text = f.read()

# Find cluster for this post
pattern = rf'\|.*?{re.escape(slug)}.*?\|'
m = re.search(pattern, cluster_text)
if m:
    print(f"   Cluster assignment: {m.group(0).split('|')[-2].strip()}")
else:
    print(f"   Cluster assignment: NOT FOUND")

# 9. INCOMING LINKS FROM OTHER POSTS
print(f"\n## 9. INCOMING INTERNAL LINKS")

# Count references to this post URL in the data.js file
this_blog_path = f'/blog/{slug}'
incoming = content.count(this_blog_path)
# Subtract the post's own self-references (the slug in its metadata)
own_refs = post_text.count(this_blog_path)
incoming_from_others = incoming - own_refs
print(f"   Total references to this post URL: {incoming}")
print(f"   Self-references (from this post): {own_refs}")
print(f"   Incoming from other posts: {incoming_from_others}")

# Find which posts link to this one
for m in re.finditer(r'slug:\s*"([^"]+)"\s*,\s*\n\s*title:\s*"([^"]+)"', content):
    other_slug = m.group(1)
    other_title = m.group(2)
    if other_slug != slug:
        # Find this post content
        other_start = m.start()
        # Get enough content
        chunk = content[other_start:other_start+5000]
        if this_blog_path in chunk:
            print(f"   ⬅️  {other_slug} ('{other_title}')")

print(f"\n{'='*70}")
print("END OF REPORT")
print(f"{'='*70}")
