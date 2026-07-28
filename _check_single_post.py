#!/usr/bin/env python3
"""Comprehensive single-post checker for kanokmiah.com.bd blog."""

import json, re, sys, os
from collections import Counter, defaultdict
from urllib.parse import urlparse

# ---------------------------------------------------------------------------
# 1. EXTRACT THE POST
# ---------------------------------------------------------------------------
with open('src/app/blog/data.js', 'r') as f:
    content = f.read()

slug = 'seo-expert-vs-seo-agency-dhaka-which-is-right'
idx = content.find(slug)
start = content.rfind('{', idx-200, idx)
depth = 0
end = start
for i in range(start, len(content)):
    if content[i] == '{': depth += 1
    elif content[i] == '}': depth -= 1
    if depth == 0:
        end = i+1
        break

post_str = content[start:end]

def extract_field(obj_str, field):
    pat = re.compile(rf'\b{field}:\s*`((?:[^`]|\\`)*)`', re.DOTALL)
    m = pat.search(obj_str)
    if m: return m.group(1).strip()
    pat2 = re.compile(rf'\b{field}:\s*"([^"]*)"', re.DOTALL)
    m2 = pat2.search(obj_str)
    if m2: return m2.group(1).strip()
    return None

def extract_array(obj_str, field):
    pat = re.compile(rf'\b{field}:\s*\[([^\]]+)\]', re.DOTALL)
    m = pat.search(obj_str)
    if m:
        raw = m.group(1)
        items = re.findall(r'"([^"]*)"', raw)
        return items
    return []

title = extract_field(post_str, 'title')
date = extract_field(post_str, 'date')
author = extract_field(post_str, 'author')
excerpt = extract_field(post_str, 'excerpt')
dateModified = extract_field(post_str, 'dateModified')
metaTitle = extract_field(post_str, 'metaTitle')
metaDescription = extract_field(post_str, 'metaDescription')
tags_list = extract_array(post_str, 'tags')
content_text = extract_field(post_str, 'content')

print("=" * 72)
print("BLOG POST CHECK REPORT")
print("=" * 72)
print(f"Slug:           {slug}")
print(f"Title:          {title}")
print(f"Date:           {date}")
print(f"Author:         {author}")
print(f"Date Modified:  {dateModified or 'NOT SET'}")
print(f"Meta Title:     {metaTitle or 'NOT SET'}")
print(f"Meta Desc:      {metaDescription or 'NOT SET'}")
print(f"Tags:           {tags_list}")
print(f"Content chars:  {len(content_text)}")
wc = len(content_text.split())
print(f"Word count:     {wc}")

# ===========================================================================
# 2. TF-IDF ANALYSIS (with sklearn)
# ===========================================================================
print("\n" + "-" * 72)
print("CHECK 1: TF-IDF / KEYWORD ANALYSIS")
print("-" * 72)

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    import numpy as np
    
    all_posts_slugs = re.findall(r'slug:\s*"([^"]+)"', content)
    post_contents = []
    target_idx = -1
    for i, p_slug in enumerate(all_posts_slugs):
        p_idx = content.find(f'slug: "{p_slug}"')
        if p_idx == -1: continue
        p_start = content.rfind('{', p_idx-150, p_idx)
        search_window = content[p_start:p_start+30000]
        c_match = re.search(r'content:\s*`((?:[^`]|\\`)*)`', search_window, re.DOTALL)
        if c_match:
            post_contents.append(c_match.group(1))
        else:
            post_contents.append('')
        if slug in p_slug:
            target_idx = i

    if target_idx >= 0 and len(post_contents) > 1:
        vectorizer = TfidfVectorizer(max_features=500, stop_words='english',
                                      ngram_range=(1,3), min_df=1, max_df=0.85)
        tfidf_matrix = vectorizer.fit_transform(post_contents)
        feature_names = vectorizer.get_feature_names_out()
        scores = tfidf_matrix[target_idx].toarray().flatten()
        top_indices = scores.argsort()[-40:][::-1]
        
        print(f"\nTop 25 TF-IDF terms (ngram range 1-3):")
        for rank, ti in enumerate(top_indices[:25], 1):
            if scores[ti] > 0:
                print(f"  {rank:2d}. {feature_names[ti]:45s} score={scores[ti]:.4f}")
    else:
        print("  Could not compute TF-IDF (not enough posts)")
except ImportError:
    print("  sklearn not available, using frequency analysis")

# Frequency analysis
words = re.findall(r'\b[a-zA-Z]{3,}\b', content_text.lower())
cust_stop = {'the','and','for','are','that','this','with','your','from','have','has','been',
             'what','which','will','their','they','when','more','about','than','also','each',
             'does','were','over','some','after','into','other','then','them','made','its',
             'just','can','very','year','new','how','you','all','not','one','but',
             'out','who','may','most','would','should','because','could','these','those',
             'while','where','there','here','both','between','under','before','after','only',
             'every','such','much','many','own','same','way','back','well','down','up',
             'any','off','too','still','being','doing','get','got','go','going','make',
             'take','come','like','know','see','think','want','need','said','say','use',
             'than','also','per','now','even','then','already','without','within',
             'across','another','around','because','behind','besides','beyond','might',
             'must','shall','let','thing','things','much','mostly','near','next',
             'often','once','quite','rather','really','since','still','sure','though',
             'thus','together','whether','while','yet','via','else','ever','everyone',
             'everything','indeed','least','less','likely','merely','otherwise','perhaps',
             'quite','rather','regarding','several','various','whereas'}
words = [w for w in words if w not in cust_stop and len(w) > 2]
c = Counter(words)
print(f"\nTop 20 content keywords (frequency):")
for i, (word, count) in enumerate(c.most_common(20)):
    print(f"  {i+1:2d}. {word:35s} occurs {count}x")

# ===========================================================================
# 3. ENTITY EXTRACTION
# ===========================================================================
print("\n" + "-" * 72)
print("CHECK 2: ENTITIES ANALYSIS")
print("-" * 72)

locations_list = ['Dhaka', 'Gulshan', 'Banani', 'Dhanmondi', 'Uttara', 'Motijheel',
             'Mirpur', 'Farmgate', 'Chittagong', 'Sylhet', 'Bangladesh', 'Bogura',
             'Khulna', 'Rajshahi', 'Comilla']
services_list = ['SEO', 'content marketing', 'link building', 'technical SEO', 'local SEO',
            'on-page SEO', 'off-page SEO', 'GEO', 'AEO', 'SEO audit', 'SEO services',
            'digital marketing', 'social media', 'PPC', 'Google Ads']
platforms_list = ['Google', 'Facebook', 'LinkedIn', 'YouTube', 'WhatsApp', 'Instagram',
             'ChatGPT', 'Perplexity', 'Gemini', 'Google Maps', 'GBP', 'Google Business Profile',
             'Ahrefs', 'SEMrush', 'Moz', 'BrightLocal', 'Local Falcon']
people_list = ['Kanok Miah']
entities_found = defaultdict(list)

for loc in locations_list:
    count = content_text.count(loc)
    if count > 0:
        entities_found['Locations'].append((loc, count))

for svc in services_list:
    count = content_text.lower().count(svc.lower())
    if count > 0:
        entities_found['Services/Topics'].append((svc, count))

for plat in platforms_list:
    count = content_text.count(plat)
    if count > 0:
        entities_found['Platforms/Tools'].append((plat, count))

for person in people_list:
    count = content_text.count(person)
    if count > 0:
        entities_found['People'].append((person, count))

# Currency
currency_matches = re.findall(r'BDT\s+[\d,]+', content_text)
if currency_matches:
    entities_found['Pricing'].append((f"BDT amounts ({len(currency_matches)} mentions)", len(currency_matches)))

# Percentages
pct_matches = re.findall(r'\d+%', content_text)
if pct_matches:
    entities_found['Statistics'].append((f"Percentage mentions ({len(pct_matches)} total)", len(pct_matches)))

for cat, items in entities_found.items():
    sorted_items = sorted(items, key=lambda x: x[1], reverse=True)
    print(f"\n  {cat}:")
    for item, count in sorted_items[:15]:
        print(f"    - {item}: {count}x")

# ===========================================================================
# 4. PILLAR-CLUSTER ANALYSIS
# ===========================================================================
print("\n" + "-" * 72)
print("CHECK 3: PILLAR-CLUSTER ANALYSIS")
print("-" * 72)

internal_links = re.findall(r'\[([^\]]+)\]\((/[^)]+)\)', content_text)
external_links = re.findall(r'\[([^\]]+)\]\((https?://[^)]+)\)', content_text)

pillar_pages = set()
cluster_pages = set()
related_posts = set()

for link_text, link_url in internal_links:
    if '/blog/' in link_url:
        related_posts.add(link_url)
    elif '/services/' in link_url:
        pillar_pages.add(link_url)
    elif '/locations/' in link_url:
        cluster_pages.add(link_url)
    elif '/industries/' in link_url:
        cluster_pages.add(link_url)

print(f"\n  Internal links found: {len(internal_links)}")
print(f"  External links found: {len(external_links)}")
print(f"\n  Pillar page links (/services/):")
for p in sorted(pillar_pages):
    print(f"    -> {p}")
print(f"\n  Location/Industry pages (/locations/, /industries/):")
for p in sorted(cluster_pages):
    print(f"    -> {p}")
print(f"\n  Related blog posts (/blog/):")
for p in sorted(related_posts):
    print(f"    -> {p}")
print(f"\n  External links:")
for link_text, link_url in external_links:
    print(f"    -> {link_url}")

links_to_services = [l for l in internal_links if '/services/' in l[1]]
links_to_industries = [l for l in internal_links if '/industries/' in l[1]]
links_to_locations = [l for l in internal_links if '/locations/' in l[1]]

print(f"\n  Cluster-to-Pillar connections:")
print(f"    Links to service pages: {len(links_to_services)}")
print(f"    Links to industry pages: {len(links_to_industries)}")
print(f"    Links to location pages: {len(links_to_locations)}")

# ===========================================================================
# 5. AEO/GEO ANALYSIS
# ===========================================================================
print("\n" + "-" * 72)
print("CHECK 4: AEO / GEO ANALYSIS")
print("-" * 72)

has_faq = 'frequently asked questions' in content_text.lower() or 'faq' in content_text.lower()
qa_count = len(re.findall(r'\*\*[^?]+\?\*\*', content_text))
qa_count2 = len(re.findall(r'### [^?]+\?', content_text))

print(f"\n  FAQ section present: {has_faq}")
print(f"  Q&A pairs (bold marker): {qa_count}")
print(f"  Q&A pairs (heading marker): {qa_count2}")

voice_phrases = ['near me', 'where is', 'how to', 'what is', 'best * in', 'find me', 'recommend']
for phrase in voice_phrases:
    count = content_text.lower().count(phrase)
    if count > 0:
        print(f"  Voice search phrase '{phrase}': {count}x")

geo_signals = []
if any(loc in content_text for loc in ['Dhaka', 'Bangladesh', 'Gulshan', 'Banani', 'Dhanmondi']):
    geo_signals.append("Location entities present (key for GEO)")
if has_faq:
    geo_signals.append("FAQ section present (helps AI extraction)")
if qa_count + qa_count2 > 0:
    geo_signals.append(f"Q&A format ({qa_count + qa_count2} pairs) — strong AEO signal")
if 'structured data' in content_text.lower() or 'schema' in content_text.lower():
    geo_signals.append("Schema/structured data mentioned in content")
if 'chatgpt' in content_text.lower() or 'perplexity' in content_text.lower() or 'gemini' in content_text.lower():
    geo_signals.append("AI engine mentions (ChatGPT, Perplexity, Gemini)")

print(f"\n  GEO/AEO signals:")
for s in geo_signals:
    print(f"    ✓ {s}")

# ===========================================================================
# 6. INTERNAL LINKS ANALYSIS
# ===========================================================================
print("\n" + "-" * 72)
print("CHECK 5: INTERNAL LINKING ANALYSIS")
print("-" * 72)

all_internal = re.findall(r'\[([^\]]+)\]\((/[^)]+)\)', content_text)
print(f"\n  Total internal links: {len(all_internal)}")

link_cats = defaultdict(list)
for text, url in all_internal:
    parsed = urlparse(url)
    path = parsed.path
    if path.startswith('/blog/'):
        link_cats['Blog posts'].append((text, path))
    elif path.startswith('/services/'):
        link_cats['Services'].append((text, path))
    elif path.startswith('/locations/'):
        link_cats['Locations'].append((text, path))
    elif path.startswith('/industries/'):
        link_cats['Industries'].append((text, path))
    elif path in ['/', '/about', '/contact']:
        link_cats['Core pages'].append((text, path))
    else:
        link_cats['Other'].append((text, path))

for cat, links in link_cats.items():
    print(f"\n  {cat} ({len(links)}):")
    for text, path in links[:8]:
        print(f"    [{text}]({path})")

link_density = len(all_internal) / wc * 100
print(f"\n  Word count: {wc}")
print(f"  Internal link density: {link_density:.2f}% ({len(all_internal)} links / {wc} words)")

# ===========================================================================
# 7. SCHEMA ANALYSIS
# ===========================================================================
print("\n" + "-" * 72)
print("CHECK 6: SCHEMA / STRUCTURED DATA ANALYSIS")
print("-" * 72)

schema_types_list = ['FAQ', 'Product', 'Review', 'BreadcrumbList', 'Organization',
                'LocalBusiness', 'Article', 'BlogPosting', 'HowTo', 'Person']
print(f"\n  Schema types mentioned in content:")
for st in schema_types_list:
    count = content_text.count(st) + content_text.count(st.lower())
    if count > 0:
        print(f"    - {st}: {count}x")

schema_ld = re.findall(r'application/ld\+json', content_text)
schema_micro = re.findall(r'itemscope|itemprop|itemtype', content_text, re.IGNORECASE)
print(f"\n  Actual structured data markup in content:")
print(f"    JSON-LD blocks: {len(schema_ld)}")
print(f"    Microdata attributes: {len(schema_micro)}")

# Check for schema in the full post object
has_schema_ref = 'schema' in content_text.lower()
print(f"    Schema keyword mentioned: {has_schema_ref}")

# ===========================================================================
# 8. SUMMARY & ISSUES
# ===========================================================================
print("\n" + "=" * 72)
print("SUMMARY & ISSUES FOUND")
print("=" * 72)

issues = []
warnings = []

# Missing fields
if not dateModified:
    issues.append("MISSING: dateModified field (present in other posts like 'complete-seo-guide')")
if not metaTitle:
    warnings.append("WARNING: metaTitle field not set (may affect SERP display)")
if not metaDescription:
    warnings.append("WARNING: metaDescription field not set (may affect CTR from search)")

# Content quality
if wc < 1500:
    issues.append(f"SHORT: Content is only {wc} words (recommended min 2000 for competitive topic)")
elif wc < 3000:
    warnings.append(f"LENGTH: Content is {wc} words (good, but 3000+ strengthens topical authority)")

# Link density
if link_density < 1.0:
    warnings.append(f"LINKS: Low internal link density ({link_density:.1f}%). Aim for 1-3%")
elif link_density > 5.0:
    warnings.append(f"LINKS: High link density ({link_density:.1f}%). Could appear spammy")

# FAQ present?
if not has_faq:
    warnings.append("AEO: No FAQ section found. FAQ markup is a strong AEO signal for voice/AI search")

# Pillar connections
if len(links_to_services) == 0:
    warnings.append("PILLAR: No links to service pages found (missed monetization funnel connection)")
if len(related_posts) == 0:
    warnings.append("CLUSTER: No internal links to other blog posts (missed cluster-building opportunity)")

# Schema
if not has_schema_ref:
    warnings.append("SCHEMA: No schema/structured data references in content")

# External links
if len(external_links) > 3:
    warnings.append(f"EXTERNAL: {len(external_links)} external links (consider nofollow/check relevance)")

# Print issues
if issues:
    print("\n  ISSUES (should fix):")
    for i, iss in enumerate(issues, 1):
        print(f"  [{i}] {iss}")
else:
    print("\n  ✓ No critical issues found")

if warnings:
    print("\n  WARNINGS (consider fixing):")
    for i, warn in enumerate(warnings, 1):
        print(f"  [{i}] {warn}")
else:
    print("\n  ✓ No warnings found")

# Overall score
score = 100
score -= len(issues) * 10
score -= len(warnings) * 5
score = max(0, min(100, score))
grade = 'A' if score >= 90 else 'B' if score >= 80 else 'C' if score >= 70 else 'D' if score >= 60 else 'F'
print(f"\n  OVERALL POST QUALITY SCORE: {score}/100 (Grade: {grade})")
print(f"  Issues: {len(issues)}, Warnings: {len(warnings)}")

# Save report
report = f"""# Blog Post Check Report
## Post: {title}
**Slug:** {slug}  
**Date:** {date} | **Author:** {author}  
**Tags:** {', '.join(tags_list)}  
**Word Count:** {wc}  
**Score:** {score}/100 (Grade: {grade})

### Issues Found
{chr(10).join(f'- {i}' for i in issues) if issues else '- None'}

### Warnings
{chr(10).join(f'- {w}' for w in warnings) if warnings else '- None'}
"""
with open(f'{slug}-framework-check.md', 'w') as f:
    f.write(report)
print(f"\n  Report saved to: {slug}-framework-check.md")
