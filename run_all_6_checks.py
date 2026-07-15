#!/usr/bin/env python3
"""
Run all 6 framework checks on a single post, handling edge cases:
- Multi-line excerpt values
- Absolute kanokmiah.com.bd URLs as internal links
- Proper content extraction
"""
import re
import sys

DATA_FILE = "/root/kanok-miahit/src/app/blog/data.js"
SLUG = "what-does-seo-expert-do-guide-business-owners"

with open(DATA_FILE, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# --- Find the post ---
slug_line_idx = None
for i, line in enumerate(lines):
    stripped = line.strip()
    if stripped.startswith('slug:') and f'"{SLUG}"' in stripped:
        slug_line_idx = i
        break

if slug_line_idx is None:
    print(f"ERROR: Post '{SLUG}' not found!")
    sys.exit(1)

# Find the opening brace of this post
post_start = None
for i in range(slug_line_idx, -1, -1):
    stripped = lines[i].strip()
    if stripped == '{':
        # Make sure we're past the const posts declaration
        if i > 0 and 'const posts' not in lines[i-1]:
            post_start = i
            break

if post_start is None:
    print("ERROR: Could not find post start")
    sys.exit(1)

# Extract the full post block by brace depth
depth = 0
in_content = False
content_parts = []
post_header_lines = []
post_end = None

for i in range(post_start, len(lines)):
    line = lines[i]
    stripped = line.strip()
    
    # Detect content field start
    if 'content:' in line and not in_content:
        in_content = True
        ci = line.find('`')
        if ci >= 0:
            before_content = line[:line.find('content:')]
            post_header_lines.append(before_content)
            rest = line[ci+1:]
            btc = rest.find('`')
            if btc >= 0:
                content_parts.append(rest[:btc])
                post_end = i
                in_content = False
                continue
            else:
                content_parts.append(rest)
                continue
        continue
    
    if in_content:
        btc = line.find('`')
        if btc >= 0:
            content_parts.append(line[:btc])
            post_end = i
            in_content = False
            continue
        else:
            content_parts.append(line)
            continue
    
    if not in_content:
        post_header_lines.append(line)
    
    # Track braces
    if not in_content:
        for ch in line:
            if ch == '{':
                depth += 1
            elif ch == '}':
                depth -= 1
        if depth == 0 and i > slug_line_idx and '}' in line:
            post_end = i
            break

content = '\n'.join(content_parts)
post_header = '\n'.join(post_header_lines)

# --- Extract fields properly ---
# Title
title_m = re.search(r'title:\s*"((?:[^"\\]|\\.)*)"', post_header)
title = title_m.group(1) if title_m else ""

# Date
date_m = re.search(r'date:\s*"((?:[^"\\]|\\.)*)"', post_header)
date_val = date_m.group(1) if date_m else ""

# Author
author_m = re.search(r'author:\s*"((?:[^"\\]|\\.)*)"', post_header)
author = author_m.group(1) if author_m else ""

# Excerpt (handle multi-line: field on one line, value on next)
excerpt = ""
excerpt_m = re.search(r'excerpt:\s*\n\s*"((?:[^"\\]|\\.)*)"', post_header)
if excerpt_m:
    excerpt = excerpt_m.group(1)
else:
    excerpt_m = re.search(r'excerpt:\s*"((?:[^"\\]|\\.)*)"', post_header)
    if excerpt_m:
        excerpt = excerpt_m.group(1)

# Tags
tags = []
tags_m = re.search(r'tags:\s*\[(.*?)\]', post_header, re.DOTALL)
if tags_m:
    tags = re.findall(r'"([^"]*)"', tags_m.group(1))

print("=" * 60)
print(f"POST: {SLUG}")
print(f"Title: {title}")
print(f"Date: {date_val}")
print(f"Author: {author}")
print(f"Tags: {tags}")
print(f"Content length: {len(content)} chars")
print(f"Excerpt: {excerpt[:80]}...")
print("=" * 60)

# ============================================================
# CRITERION 1: TF-IDF / Keyword Density
# ============================================================
c_lower = content.lower()
# Primary keyword: "seo expert"
kw_variants = ["seo expert", "seo specialist", "seo professional", "what does an seo expert do"]
best_kw = "seo expert"
best_count = c_lower.count(best_kw)
for v in kw_variants:
    n = c_lower.count(v)
    if n > best_count:
        best_count = n
        best_kw = v

tf_pass = best_count >= 5
print(f"\nCRITERION 1: TF-IDF / Keyword Density")
print(f"  Best keyword: '{best_kw}'")
print(f"  Occurrences: {best_count}")
print(f"  Threshold: ≥5")
print(f"  Result: {'✅ PASS' if tf_pass else '❌ FAIL'}")

# ============================================================
# CRITERION 2: Entities
# ============================================================
missing_ents = []
if 'dhaka' not in c_lower: missing_ents.append("Dhaka")
if 'bangladesh' not in c_lower: missing_ents.append("Bangladesh")
if 'google' not in c_lower: missing_ents.append("Google")
if 'seo' not in c_lower: missing_ents.append("SEO")
if 'expert' not in c_lower: missing_ents.append("Expert")
if 'business' not in c_lower: missing_ents.append("Business")
ent_pass = len(missing_ents) == 0
print(f"\nCRITERION 2: Entities")
print(f"  Missing: {missing_ents if missing_ents else 'None'}")
print(f"  Result: {'✅ PASS' if ent_pass else '❌ FAIL'}")

# ============================================================
# CRITERION 3: Pillar Link
# ============================================================
# Find all markdown links
all_links = re.findall(r'\[([^\]]*)\]\(([^)]*)\)', content)
# Normalize links: extract relative paths from absolute URLs
def normalize_url(url):
    url = url.strip()
    if url.startswith('/'):
        return url
    # Handle kanokmiah.com.bd absolute URLs
    m = re.search(r'https?://(?:www\.)?kanokmiah\.com\.bd(.*)', url)
    if m:
        path = m.group(1)
        return path if path else '/'
    return url

normalized_links = []
for text, url in all_links:
    norm = normalize_url(url)
    if norm.startswith('/') and len(norm) > 1 and not norm.startswith('//'):
        normalized_links.append((text.strip(), norm))

# Check for pillar links
pillar_keywords = ['/services/', '/industries/', '/blog/']
pil_found = []
for text, href in normalized_links:
    for pk in pillar_keywords:
        if href.startswith(pk) or href == pk.rstrip('/'):
            pil_found.append(href)
            break

pil_pass = len(pil_found) > 0
print(f"\nCRITERION 3: Pillar Link")
print(f"  All internal links: {[l for _, l in normalized_links]}")
print(f"  Pillar links found: {pil_found if pil_found else 'None'}")
print(f"  Result: {'✅ PASS' if pil_pass else '❌ FAIL'}")

# ============================================================
# CRITERION 4: AEO/GEO Question Headings
# ============================================================
headings = re.findall(r'^#{2,3}\s+(.+)$', content, re.MULTILINE)
qw = ['how', 'what', 'why', 'when', 'where', 'can', 'do', 'is', 'are', 'does', 'will', 'should', 'which', 'who']
qh = []
for h in headings:
    s = h.strip().lower()
    for q in qw:
        if s.startswith(q) or s.startswith(q.capitalize()):
            qh.append(h.strip())
            break
    # Also catch headings with '?' directly
    if '?' in h and h.strip() not in qh:
        qh.append(h.strip())

aeo_pass = len(qh) >= 2
print(f"\nCRITERION 4: AEO/GEO (Question Headings)")
print(f"  Total headings: {len(headings)}")
print(f"  Question headings ({len(qh)}):")
for q in qh:
    print(f"    - {q}")
print(f"  Threshold: ≥2")
print(f"  Result: {'✅ PASS' if aeo_pass else '❌ FAIL'}")

# ============================================================
# CRITERION 5: Internal Links
# ============================================================
# De-duplicate by path
unique_internals = set()
for text, href in normalized_links:
    h = href.strip()
    if h.startswith('/') and len(h) > 1:
        unique_internals.add(h)

il_pass = len(unique_internals) >= 3
print(f"\nCRITERION 5: Internal Links")
print(f"  Total unique internal links: {len(unique_internals)}")
for i, link in enumerate(sorted(unique_internals), 1):
    print(f"    {i}. {link}")
print(f"  Threshold: ≥3 unique")
print(f"  Result: {'✅ PASS' if il_pass else '❌ FAIL'}")

# ============================================================
# CRITERION 6: Schema Readiness
# ============================================================
sch_missing = []
if not title: sch_missing.append('title')
if not excerpt: sch_missing.append('excerpt/description')
if not date_val: sch_missing.append('date')
if not author: sch_missing.append('author')
if not tags: sch_missing.append('tags')
sch_pass = len(sch_missing) == 0

print(f"\nCRITERION 6: Schema Readiness")
print(f"  Title: {'✅' if title else '❌'} ({title[:60] if title else 'MISSING'})")
print(f"  Excerpt: {'✅' if excerpt else '❌'} ({excerpt[:60] if excerpt else 'MISSING'})")
print(f"  Date: {'✅' if date_val else '❌'} ({date_val if date_val else 'MISSING'})")
print(f"  Author: {'✅' if author else '❌'} ({author if author else 'MISSING'})")
print(f"  Tags: {'✅' if tags else '❌'} ({tags if tags else 'MISSING'})")
print(f"  Result: {'✅ PASS' if sch_pass else '❌ FAIL'}")

# ============================================================
# OVERALL
# ============================================================
all_pass = all([tf_pass, ent_pass, pil_pass, aeo_pass, il_pass, sch_pass])
print(f"\n{'='*60}")
print(f"OVERALL RESULT: {'✅ ALL 6 CHECKS PASS' if all_pass else '❌ SOME CHECKS FAIL'}")
print(f"  Passing: {sum([tf_pass, ent_pass, pil_pass, aeo_pass, il_pass, sch_pass])}/6")
if not all_pass:
    print(f"  Failing: ", end="")
    fails = []
    if not tf_pass: fails.append("TF-IDF")
    if not ent_pass: fails.append("Entities")
    if not pil_pass: fails.append("Pillar Link")
    if not aeo_pass: fails.append("AEO/GEO")
    if not il_pass: fails.append("Internal Links")
    if not sch_pass: fails.append("Schema Ready")
    print(", ".join(fails))
print(f"{'='*60}")
