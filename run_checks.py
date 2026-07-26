#!/usr/bin/env python3
"""Run framework compliance checks on blog post: seo-vs-google-ads-whats-best-bangladesh-businesses"""

import re

# Read the file
with open('/root/kanok-miahit/src/app/blog/data.js', 'r') as f:
    lines = f.readlines()

# Post range: slug at line 1713 (0-indexed 1712), content at 1721 (0-indexed 1720), 
# content ends at line 1992 (0-indexed 1991)
slug_line = lines[1712]  # "    slug: ..."
meta_lines = lines[1712:1720]  # slug through imagePlaceholder
content_lines = lines[1720:]   # from content: ` line onward

# Extract the content body
content_body = ''
in_content = False
for line in lines[1712:]:
    if 'content: `' in line:
        in_content = True
        # Extract text after the backtick
        bt_idx = line.find('`')
        if bt_idx >= 0 and bt_idx < len(line) - 1:
            content_body += line[bt_idx+1:]
        continue
    if in_content:
        if line.strip().endswith('`,'):
            # End of content
            # Strip the trailing `, and any whitespace
            end_idx = line.rfind('`')
            if end_idx >= 0:
                content_body += line[:end_idx]
            break
        content_body += line

print("=" * 70)
print("FRAMEWORK COMPLIANCE CHECKS")
print("Post: seo-vs-google-ads-whats-best-bangladesh-businesses")
print("=" * 70)

# Extract metadata
meta_text = ''.join(meta_lines)
title = None
date = None
author = None
excerpt = None
tags = []

for line in meta_lines:
    l = line.strip()
    if l.startswith('title:'):
        title = l.split('title:')[1].strip().strip(',')
        title = title.strip('"')
    elif l.startswith('date:'):
        date = l.split('date:')[1].strip().strip(',')
        date = date.strip('"')
    elif l.startswith('author:'):
        author = l.split('author:')[1].strip().strip(',')
        author = author.strip('"')
    elif l.startswith('excerpt:'):
        # Could span multiple lines
        excerpt_parts = []
        for el in meta_lines[meta_lines.index(line):]:
            el_stripped = el.strip()
            if el_stripped.startswith('"') and el_stripped.endswith('",'):
                excerpt = el_stripped.strip('",')
                break
            elif el_stripped.startswith('"'):
                excerpt_parts.append(el_stripped.strip('"'))
            elif el_stripped.endswith('",'):
                excerpt_parts.append(el_stripped.rstrip(',').strip().rstrip('"'))
                excerpt = ' '.join(excerpt_parts)
                break
            else:
                excerpt_parts.append(el_stripped)
    elif l.startswith('tags:'):
        tags_str = l.split('tags:')[1].strip()
        # Extract quoted strings from array
        tags = re.findall(r'"([^"]+)"', tags_str)

print(f"  Title:   {title}")
print(f"  Date:    {date}")
print(f"  Author:  {author}")
print(f"  Tags:    {tags}")

# =========================================================
# A. TF-IDF Coverage
# =========================================================
print("\n" + "=" * 70)
print("A. TF-IDF COVERAGE")
print("=" * 70)

primary_keyword = "SEO"
count_keyword = content_body.count(primary_keyword)
print(f"  Primary keyword (first meaningful noun phrase): '{primary_keyword}'")
print(f"  Occurrences in content: {count_keyword}")
if count_keyword < 5:
    print("  ❌ FLAG: Keyword occurs < 5 times")
else:
    print("  ✅ PASS: Keyword occurs 5+ times")

# =========================================================
# B. Semantic Entity Coverage
# =========================================================
print("\n" + "=" * 70)
print("B. SEMANTIC ENTITY COVERAGE")
print("=" * 70)

entities = {
    "Dhaka": "Dhaka" in content_body,
    "Bangladesh/Bangladeshi": ("Bangladesh" in content_body or "Bangladeshi" in content_body),
    "Google Ads": "Google Ads" in content_body,
    "PPC": "PPC" in content_body,
    "SEO": "SEO" in content_body,
    "Digital Marketing": "digital marketing" in content_body.lower(),
}

for name, found in entities.items():
    print(f"  {name}: {'✅ FOUND' if found else '❌ MISSING'}")

missing = [k for k, v in entities.items() if not v]
if missing:
    print(f"  ❌ FLAG: Missing entities: {', '.join(missing)}")
else:
    print("  ✅ PASS: All key entities present")

# =========================================================
# C. Pillar-Cluster Alignment
# =========================================================
print("\n" + "=" * 70)
print("C. PILLAR-CLUSTER ALIGNMENT")
print("=" * 70)

print(f"  Tags: {tags}")
print("  Based on tags, this belongs to the 'SEO / Digital Marketing' pillar")

pillar_candidates = [
    "/blog/complete-seo-guide-bangladesh-businesses-2026",
    "/services",
]

found_pillar = None
for pc in pillar_candidates:
    if pc in content_body:
        found_pillar = pc
        break

if found_pillar:
    print(f"  ✅ PASS: Links to pillar page '{found_pillar}' found")
else:
    all_links = re.findall(r'\((/[^)]+)\)', content_body)
    print(f"  ❌ FLAG: No pillar page link detected. Links found: {all_links}")

# =========================================================
# D. AEO/GEO Optimization
# =========================================================
print("\n" + "=" * 70)
print("D. AEO/GEO OPTIMIZATION")
print("=" * 70)

question_words = ['How', 'What', 'Why', 'When', 'Where', 'Can', 'Do', 'Is', 'Are']
pattern = r'^#{2,4}\s+(' + '|'.join(question_words) + r')\b'
heading_matches = list(re.finditer(pattern, content_body, re.MULTILINE))

question_headings = []
for m in heading_matches:
    start = m.start()
    end_line = content_body.find('\n', start)
    if end_line == -1:
        end_line = len(content_body)
    heading_line = content_body[start:end_line].strip()
    question_headings.append(heading_line)

print(f"  Question-based headings found ({len(question_headings)}):")
for h in question_headings:
    print(f"    • {h}")

if len(question_headings) < 2:
    print("  ❌ FLAG: < 2 question headings found")
else:
    print(f"  ✅ PASS: {len(question_headings)} question headings found (>= 2)")

# =========================================================
# E. Internal Linking
# =========================================================
print("\n" + "=" * 70)
print("E. INTERNAL LINKING")
print("=" * 70)

link_pattern = re.compile(r'\[([^\]]+)\]\((/[^)]+)\)')
internal_links = link_pattern.findall(content_body)
seen_urls = set()
unique_links = []
for text, url in internal_links:
    if url not in seen_urls:
        seen_urls.add(url)
        unique_links.append((text, url))

print(f"  Unique internal links found: {len(unique_links)}")
for text, url in unique_links:
    print(f"    • [{text}]({url})")

blog_links = [(t, u) for t, u in unique_links if '/blog/' in u]
service_links = [(t, u) for t, u in unique_links if '/services' in u and '/blog/' not in u]
location_links = [(t, u) for t, u in unique_links if '/locations/' in u]
industry_links = [(t, u) for t, u in unique_links if '/industries/' in u]
other_links = [(t, u) for t, u in unique_links if not any(x in u for x in ['/blog/', '/services', '/locations/', '/industries/'])]

print(f"\n  Breakdown:")
print(f"    Blog links: {len(blog_links)}")
print(f"    Service links: {len(service_links)}")
print(f"    Location links: {len(location_links)}")
print(f"    Industry links: {len(industry_links)}")
if other_links:
    print(f"    Other: {len(other_links)} - {[(t, u) for t, u in other_links]}")

if len(unique_links) < 3:
    print("  ❌ FLAG: < 3 internal links")
else:
    print(f"  ✅ PASS: {len(unique_links)} internal links found (>= 3)")

# External links
ext_pattern = re.compile(r'\[([^\]]+)\]\((https?://[^)]+)\)')
external_links = ext_pattern.findall(content_body)
if external_links:
    print(f"\n  External links: {len(external_links)}")
    for t, u in external_links:
        print(f"    • [{t}]({u})")

# =========================================================
# F. Schema
# =========================================================
print("\n" + "=" * 70)
print("F. SCHEMA (ArticleSchema) FIELDS")
print("=" * 70)

checks = {
    "title": title is not None and len(title) > 5,
    "excerpt": excerpt is not None and len(str(excerpt)) > 20,
    "date": date is not None and len(date) > 5,
    "author": author is not None and len(author) > 2,
}

print(f"  title:   {'✅' if checks['title'] else '❌'} {title}")
print(f"  excerpt: {'✅' if checks['excerpt'] else '❌'} {str(excerpt)[:80]}...")
print(f"  date:    {'✅' if checks['date'] else '❌'} {date}")
print(f"  author:  {'✅' if checks['author'] else '❌'} {author}")

missing_fields = [k for k, v in checks.items() if not v]
if missing_fields:
    print(f"  ❌ FLAG: Missing fields for ArticleSchema: {', '.join(missing_fields)}")
else:
    print("  ✅ PASS: All ArticleSchema fields (title, excerpt, date, author) are set")

# =========================================================
# SUMMARY
# =========================================================
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

a_pass = count_keyword >= 5
b_pass = not missing
c_pass = found_pillar is not None
d_pass = len(question_headings) >= 2
e_pass = len(unique_links) >= 3
f_pass = not missing_fields

results = [
    ("A. TF-IDF Coverage", "✅ PASS" if a_pass else "❌ FLAG", f"Keyword '{primary_keyword}' appears {count_keyword} times in content"),
    ("B. Semantic Entity Coverage", "✅ PASS" if b_pass else "❌ FLAG", f"All key entities present ({', '.join(entities.keys())})"),
    ("C. Pillar-Cluster Alignment", "✅ PASS" if c_pass else "❌ FLAG", f"Links to pillar: {found_pillar}"),
    ("D. AEO/GEO Optimization", "✅ PASS" if d_pass else "❌ FLAG", f"{len(question_headings)} question-based headings found"),
    ("E. Internal Linking", "✅ PASS" if e_pass else "❌ FLAG", f"{len(unique_links)} unique internal links found"),
    ("F. Schema (ArticleSchema)", "✅ PASS" if f_pass else "❌ FLAG", f"Fields: title={bool(title)}, excerpt={bool(excerpt)}, date={bool(date)}, author={bool(author)}"),
]

for check, status, detail in results:
    print(f"  {check}: {status}")
    print(f"    {detail}")

print("=" * 70)
