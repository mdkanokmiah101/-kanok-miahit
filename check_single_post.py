#!/usr/bin/env python3
"""Run all 6 framework checks on a single blog post."""
import re, sys
from datetime import datetime

DATA_PATH = 'src/app/blog/data.js'
SLUG = 'top-10-seo-mistakes-dhaka-businesses-fix'

with open(DATA_PATH, 'r') as f:
    text = f.read()
lines = text.split('\n')

# Build slug-to-line map
slug_positions = {}
for i, line in enumerate(lines):
    m = re.search(r'slug:\s+"([^"]+)"', line)
    if m:
        slug_positions[m.group(1)] = i

def extract_post_fields(slug):
    slug_line = slug_positions[slug]
    start = slug_line
    while start > 0 and not lines[start].strip().startswith('{'):
        start -= 1
    next_slug_line = None
    for s, ln in sorted(slug_positions.items(), key=lambda x: x[1]):
        if ln > slug_line:
            next_slug_line = ln
            break
    end = next_slug_line if next_slug_line else len(lines)
    post_lines = lines[start:end]
    post_text = '\n'.join(post_lines)

    title_m = re.search(r'title:\s+"([^"]*)"', post_text)
    date_m = re.search(r'date:\s+"([^"]*)"', post_text)
    excerpt_m = re.search(r'excerpt:\s*\n?\s+"([^"]*)"', post_text, re.DOTALL)
    tags_m = re.search(r'tags:\s*\[([^\]]*)\]', post_text, re.DOTALL)
    content_m = re.search(r'content:\s*`\n?([^`]*)`', post_text, re.DOTALL)

    title = title_m.group(1) if title_m else ''
    date = date_m.group(1) if date_m else ''
    excerpt = excerpt_m.group(1).replace('\n', ' ').strip() if excerpt_m else ''
    tags = re.findall(r'"([^"]*)"', tags_m.group(1)) if tags_m else []
    content = content_m.group(1) if content_m else ''

    return {'title': title, 'date': date, 'excerpt': excerpt, 'tags': tags,
            'content': content, 'slug': slug}

post = extract_post_fields(SLUG)
content = post['content']
title = post['title']

print("=" * 68)
print("  BLOG POST FRAMEWORK CHECK REPORT")
print("=" * 68)
print(f"\nSlug:           {post['slug']}")
print(f"Title:          {post['title']}")
print(f"Date:           {post['date']}")
print(f"Tags:           {', '.join(post['tags'])}")
print(f"Excerpt:        {post['excerpt'][:120]}...")
print(f"Content:        {len(content)} chars / ~{len(content.split())} words")
print()

# ============================================================
# CHECK 1: TF-IDF (Keyword Coverage)
# ============================================================
print("---")
print("A. TF-IDF COVERAGE")
print("---")

# Primary keyword extraction matching the framework logic
stop_words = {'the', 'a', 'an', 'in', 'of', 'for', 'to', 'and', 'or', 'is', 'are',
              'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do',
              'does', 'did', 'will', 'would', 'can', 'could', 'shall', 'should',
              'may', 'might', 'must', 'about', 'into', 'through', 'during',
              'before', 'after', 'above', 'below', 'between', 'out', 'off',
              'over', 'under', 'again', 'further', 'then', 'once', 'here',
              'there', 'when', 'where', 'why', 'how', 'all', 'each', 'every',
              'both', 'few', 'more', 'most', 'other', 'some', 'such', 'no',
              'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very',
              'just', 'because', 'as', 'until', 'while', 'with', 'without',
              'from', 'up', 'down', 'at', 'by', 'on', 'off', 'this', 'that',
              'these', 'those', 'it', 'its', 'your', 'our', 'their', 'what',
              'which', 'who', 'whom', 'your', '2026', 'guide', 'new'}

clean_title = title.replace(':', ' ').replace('?', ' ').replace('!', ' ')
words = clean_title.split()
meaningful = [w.strip() for w in words if w.lower() not in stop_words and len(w.strip()) > 2]

print(f"Title words: {words}")
print(f"Meaningful title words (no stop words): {meaningful}")

# Try 2-word phrase first: "SEO Mistakes"
kw_2 = 'SEO Mistakes'
count_2 = len(re.findall(re.escape(kw_2), content, re.IGNORECASE))

# Also count "SEO" separately
seo_count = len(re.findall(r'\bSEO\b', content))
mistakes_count = len(re.findall(r'\bmistakes?\b', content, re.IGNORECASE))
dhaka_count = len(re.findall(r'\bDhaka\b', content))

print(f'  Primary keyword "SEO Mistakes": {count_2} occurrences')
print(f'  "SEO" standalone:               {seo_count}')
print(f'  "mistakes" standalone:          {mistakes_count}')
print(f'  "Dhaka" standalone:             {dhaka_count}')

# Determine best keyword
best_count = max(count_2, seo_count)
if count_2 >= 5:
    best_kw = "SEO Mistakes"
elif seo_count >= 5:
    best_kw = "SEO"
else:
    best_kw = meaningful[0] if meaningful else words[0]
    best_count = len(re.findall(re.escape(best_kw), content, re.IGNORECASE))

status = 'PASS' if best_count >= 5 else ('WARN' if best_count >= 3 else 'FAIL')
print(f'  Best keyword: "{best_kw}" ({best_count} occurrences)')
print(f'  Threshold: >= 5')
print(f'  Result: [{status}]')
print()

# ============================================================
# CHECK 2: Semantic Entity Coverage
# ============================================================
print("---")
print("B. SEMANTIC ENTITY COVERAGE")
print("---")

# Per the framework, this post uses 'mistakes' entity set: ['mistakes', 'errors', 'avoid']
# Plus location entities
entity_sets = {
    'mistakes': ['mistakes', 'errors', 'avoid'],
}
to_check = entity_sets['mistakes'] + ['Dhaka', 'Bangladesh', 'Gulshan', 'Banani', 'Dhanmondi']

results = []
for entity in to_check:
    cnt = len(re.findall(re.escape(entity), content, re.IGNORECASE))
    passed = cnt > 0
    mark = 'PASS' if passed else 'MISS'
    results.append((entity, cnt, mark))
    print(f'  {mark}: "{entity}" — {cnt} occurrences')

passed_count = sum(1 for _, _, m in results if m == 'PASS')
total = len(results)
entity_status = 'PASS' if passed_count >= total else ('WARN' if passed_count >= total - 2 else 'FAIL')
print(f'  Result: {passed_count}/{total} entities found [{entity_status}]')
print()

# ============================================================
# CHECK 3: Pillar-Cluster Alignment
# ============================================================
print("---")
print("C. PILLAR-CLUSTER ALIGNMENT")
print("---")

# From cluster_map.md: cluster = "Content Marketing & SEO Strategy"
cluster_name = "Content Marketing & SEO Strategy"
pillar_urls = [
    '/blog/complete-seo-guide-bangladesh-businesses-2026',
    '/services/local-seo',
    '/services/technical-seo',
    '/services/ecommerce-seo',
    '/services/geo-ai-search',
    '/services/semantic-seo',
    '/services/link-building',
]

found_pillar = []
for url in pillar_urls:
    if url in content:
        found_pillar.append(url)

print(f'  Cluster: {cluster_name}')
for url in pillar_urls:
    mark = 'LINKED' if url in content else 'missing'
    print(f'  {mark}: {url}')

if found_pillar:
    print(f'  Result: PASS — linked to pillar(s): {", ".join(found_pillar)}')
else:
    print(f'  Result: FAIL — no link to any pillar page found')
print()

# ============================================================
# CHECK 4: AEO/GEO Optimization
# ============================================================
print("---")
print("D. AEO/GEO OPTIMIZATION")
print("---")

heading_pattern = re.findall(r'^#{2,6}\s+.*$', content, re.MULTILINE)
question_words = ['How', 'What', 'Why', 'When', 'Where', 'Can', 'Do', 'Is', 'Are', 'Does', 'Did']

q_headings = []
all_headings = []
for h in heading_pattern:
    text = h.lstrip('#').strip()
    all_headings.append(text)
    if text.split():
        first = text.split()[0]
        if first in question_words:
            q_headings.append(text)

print(f'  Total headings (H2+): {len(all_headings)}')
for h in all_headings:
    is_q = any(h.split() and h.split()[0] in question_words for _ in [1])
    # Check if it's a question heading
    first_word = h.split()[0] if h.split() else ''
    if first_word in question_words:
        print(f'    [QUESTION] {h[:90]}')
    else:
        print(f'              {h[:90]}')

print(f'\n  Question-format headings: {len(q_headings)}')
for q in q_headings:
    print(f'    "{q[:80]}"')

# Also check for GEO/AEO terms
geo_terms = ['Generative Engine Optimization', 'AI search', 'GEO', 'SGE', 'Perplexity', 'ChatGPT']
aeo_terms = ['Answer Engine Optimization', 'AEO']
geo_count = sum(1 for t in geo_terms if t.lower() in content.lower())
aeo_count = sum(1 for t in aeo_terms if t.lower() in content.lower())

print(f'\n  GEO terms found: {geo_count}/{len(geo_terms)}')
for t in geo_terms:
    cnt = content.lower().count(t.lower())
    if cnt > 0:
        print(f'    "{t}": x{cnt}')
print(f'  AEO terms found: {aeo_count}/{len(aeo_terms)}')
for t in aeo_terms:
    cnt = content.lower().count(t.lower())
    if cnt > 0:
        print(f'    "{t}": x{cnt}')

aeo_geo_status = 'PASS' if len(q_headings) >= 2 else 'FAIL'
print(f'\n  Result: {len(q_headings)} question headings (threshold: >= 2) [{aeo_geo_status}]')
print()

# ============================================================
# CHECK 5: Internal Linking
# ============================================================
print("---")
print("E. INTERNAL LINK ANALYSIS")
print("---")

# Collect all internal links from markdown () and href=""
md_links = set()
for m in re.finditer(r'\((/[^)\s#]+)\)', content):
    path = m.group(1).rstrip('/')
    if path and path != '/':
        md_links.add(path)

for m in re.finditer(r'href="(/[^"\s#]+)"', content):
    path = m.group(1).rstrip('/')
    if path and path != '/':
        md_links.add(path)

all_links = sorted(md_links)
print(f'  Total unique internal links: {len(all_links)}')
for link in all_links:
    cnt = content.count(link)
    print(f'    {link} (x{cnt})')

link_status = 'PASS' if len(all_links) >= 3 else 'FAIL'
print(f'  Result: {len(all_links)} internal links (threshold: >= 3) [{link_status}]')

# Also check external links
ext_links = re.findall(r'\(https?://[^)]+\)', content)
print(f'  External links: {len(ext_links)}')
for el in ext_links:
    print(f'    {el[:100]}')
print()

# ============================================================
# CHECK 6: Schema Readiness
# ============================================================
print("---")
print("F. SCHEMA READINESS")
print("---")

issues = []

# Title
if post.get('title'):
    print(f'  PASS: Title set ({len(post["title"])} chars)')
else:
    issues.append('Missing title')
    print(f'  FAIL: Title missing')

# Excerpt
excerpt = post.get('excerpt', '')
if excerpt and len(excerpt) >= 10:
    print(f'  PASS: Excerpt set ({len(excerpt)} chars)')
else:
    issues.append('Missing/short excerpt')
    print(f'  FAIL: Excerpt missing or too short')

# Date
date_str = post.get('date', '')
if date_str:
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        print(f'  PASS: Date valid ({date_str})')
    except ValueError:
        issues.append('Invalid date format')
        print(f'  FAIL: Invalid date format ({date_str})')
else:
    issues.append('Missing date')
    print(f'  FAIL: Date missing')

# Tags
tags = post.get('tags', [])
if tags and len(tags) > 0:
    print(f'  PASS: Tags present ({", ".join(tags)})')
else:
    issues.append('Missing tags')
    print(f'  FAIL: Tags missing')

# Content mentions of schema types
schema_types = ['Article', 'FAQ', 'LocalBusiness', 'Organization', 'Product', 'BreadcrumbList', 'Review', 'HowTo']
for st in schema_types:
    if st.lower() in content.lower():
        print(f'  NOTE: Content references "{st}" schema')

schema_status = 'PASS' if not issues else f'Issues: {", ".join(issues)}'
print(f'  Result: {schema_status}')
print()

# ============================================================
# SUMMARY SCOREBOARD
# ============================================================
print("=" * 68)
print("  FINAL SCOREBOARD")
print("=" * 68)

checks = [
    ('A. TF-IDF Coverage', status),
    ('B. Entity Coverage', entity_status),
    ('C. Pillar-Cluster', 'PASS' if found_pillar else 'FAIL'),
    ('D. AEO/GEO', aeo_geo_status),
    ('E. Internal Links', link_status),
    ('F. Schema', 'PASS' if not issues else 'FAIL'),
]

for name, st in checks:
    sym = 'PASS' if st.startswith('PASS') else 'FAIL' if st.startswith('FAIL') else st
    icon = 'PASS' if sym == 'PASS' else 'FAIL'
    print(f'  {name}: [{icon}]')

pass_count = sum(1 for _, s in checks if s.startswith('PASS'))
print(f'\n  {pass_count}/6 checks passed')
print(f'  {6 - pass_count}/6 checks need attention')
print()
print("=" * 68)
