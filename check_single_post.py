#!/usr/bin/env python3
"""Run framework checks on a single blog post."""
import re

DATA_FILE = "/root/kanok-miahit/src/app/blog/data.js"
TARGET_SLUG = "seo-expert-vs-seo-agency-dhaka-which-is-right"

with open(DATA_FILE, 'r', encoding='utf-8') as f:
    source = f.read()

# --- Parse the post ---
def parse_post(data, slug):
    slug_line = f'slug: "{slug}"'
    idx = data.find(slug_line)
    if idx == -1:
        return None
    pre = data[:idx]
    block_start = pre.rfind('{\n')
    search_from = idx + len(slug_line)
    candidates = [len(data)]
    m = data.find('},\n  {\n    slug:', search_from)
    if m != -1:
        candidates.append(m + 1)
    m = data.find('};\n', search_from)
    if m != -1:
        candidates.append(m)
    m = data.find('];', search_from)
    if m != -1:
        candidates.append(m)
    end_idx = min(candidates)
    return data[block_start:end_idx]

def get_str(post, name):
    m = re.search(rf'{name}:\s*"((?:[^"\\]|\\.)*)"', post)
    if m: return m.group(1)
    m = re.search(rf'{name}:\s*\n\s*"((?:[^"\\]|\\.)*)"', post)
    if m: return m.group(1)
    return ""

def get_tags(post):
    m = re.search(r'tags:\s*\[(.*?)\]', post, re.DOTALL)
    if m: return re.findall(r'"([^"]*)"', m.group(1))
    return []

def get_content(post):
    m = re.search(r'content:\s*`', post)
    if not m: return ""
    start = m.end()
    end = post.find('`', start)
    if end == -1: return post[start:]
    return post[start:end]

post = parse_post(source, TARGET_SLUG)
if not post:
    print(f"ERROR: Post '{TARGET_SLUG}' not found!")
    exit(1)

title = get_str(post, 'title')
excerpt = get_str(post, 'excerpt')
date = get_str(post, 'date')
author = get_str(post, 'author')
tags = get_tags(post)
content = get_content(post)

print(f"=== Post: {TARGET_SLUG} ===")
print(f"Title: {title}")
print(f"Date: {date}")
print(f"Author: {author}")
print(f"Tags: {tags}")
print(f"Content length: {len(content)} chars")
print(f"Excerpt: {excerpt[:80]}...")
print()

# --- CRITERION 1: TF-IDF / Keyword density ---
# Primary keyword for this post: "seo expert vs seo agency"
kw = "seo expert"
alt_kw = ["seo agency", "seo expert dhaka", "seo agency dhaka"]
c_lower = content.lower()
tfidf_n = c_lower.count(kw)
best_kw = kw
for ak in alt_kw:
    n = c_lower.count(ak)
    if n > tfidf_n:
        tfidf_n = n
        best_kw = ak
tf_pass = tfidf_n >= 5
print(f"CRITERION 1: TF-IDF (keyword: '{best_kw}')")
print(f"  Occurrences: {tfidf_n}")
print(f"  Result: {'✅ PASS' if tf_pass else '❌ FAIL'} (need ≥5)")

# --- CRITERION 2: Entities ---
missing_ents = []
if 'dhaka' not in c_lower: missing_ents.append("Dhaka")
if 'bangladesh' not in c_lower: missing_ents.append("Bangladesh")
if 'google' not in c_lower: missing_ents.append("Google")
if 'seo' not in c_lower: missing_ents.append("SEO")
if 'expert' not in c_lower: missing_ents.append("Expert")
if 'agency' not in c_lower: missing_ents.append("Agency")
ent_pass = len(missing_ents) == 0
print(f"CRITERION 2: Entities")
print(f"  Missing: {missing_ents if missing_ents else 'None'}")
print(f"  Result: {'✅ PASS' if ent_pass else '❌ FAIL'}")

# --- CRITERION 3: Pillar Link ---
# This post is a comparison. Expected pillar: /services/ or similar
links = re.findall(r'\[([^\]]*)\]\(([^)]*)\)', content)
pillar_keywords = ['/services/', '/industries/', '/blog/']
pil_found = []
for _, href in links:
    h = href.strip()
    if h.startswith('/') or 'kanokmiah.com.bd' in h.lower():
        normalized = h
        if 'kanokmiah.com.bd' in h.lower():
            parts = h.split('/')
            if len(parts) >= 4:
                normalized = '/' + '/'.join(parts[3:])
        for pk in pillar_keywords:
            if normalized.startswith(pk) or normalized == pk.rstrip('/'):
                pil_found.append(normalized)

pil_pass = len(pil_found) > 0
print(f"CRITERION 3: Pillar Link")
print(f"  Found pillar links: {pil_found if pil_found else 'None'}")
print(f"  Result: {'✅ PASS' if pil_pass else '❌ FAIL'}")

# --- CRITERION 4: AEO/GEO (question headings) ---
headings = re.findall(r'^#{2,3}\s+(.+)$', content, re.MULTILINE)
qw = ['how','what','why','when','where','can','do','is','are','does','will','should']
qh = []
for h in headings:
    s = h.strip().lower()
    for q in qw:
        if s.startswith(q):
            qh.append(h.strip())
            break
aeo_pass = len(qh) >= 2
print(f"CRITERION 4: AEO/GEO Question Headings")
print(f"  Total headings: {len(headings)}")
print(f"  Question headings: {qh if qh else 'None'}")
print(f"  Result: {'✅ PASS' if aeo_pass else '❌ FAIL'} (need ≥2)")

# --- CRITERION 5: Internal Links ---
internals = set()
for _, href in links:
    h = href.strip()
    if h.startswith('/') and len(h) > 1:
        internals.add(h)
    elif 'kanokmiah.com.bd' in h.lower():
        parts = h.split('/')
        if len(parts) >= 4:
            internals.add('/' + '/'.join(parts[3:]))
        else:
            internals.add('/')

il_pass = len(internals) >= 3
print(f"CRITERION 5: Internal Links")
print(f"  Total unique internal links: {len(internals)}")
for i, link in enumerate(sorted(internals), 1):
    print(f"    {i}. {link}")
print(f"  Result: {'✅ PASS' if il_pass else '❌ FAIL'} (need ≥3)")

# --- CRITERION 6: Schema Readiness ---
sch_missing = []
if not title: sch_missing.append('title')
if not excerpt: sch_missing.append('excerpt/description')
if not date: sch_missing.append('date')
if not tags: sch_missing.append('tags')
sch_pass = len(sch_missing) == 0
print(f"CRITERION 6: Schema Readiness")
print(f"  Title: {'✅' if title else '❌'} ({title[:60] if title else 'MISSING'})")
print(f"  Excerpt: {'✅' if excerpt else '❌'} ({excerpt[:60] if excerpt else 'MISSING'})")
print(f"  Date: {'✅' if date else '❌'} ({date if date else 'MISSING'})")
print(f"  Tags: {'✅' if tags else '❌'} ({tags if tags else 'MISSING'})")
print(f"  Result: {'✅ PASS' if sch_pass else '❌ FAIL'}")

# --- OVERALL ---
all_pass = all([tf_pass, ent_pass, pil_pass, aeo_pass, il_pass, sch_pass])
print(f"\n{'='*50}")
print(f"OVERALL RESULT: {'✅ ALL CHECKS PASS' if all_pass else '❌ SOME CHECKS FAIL'}")
print(f"  Criteria passing: {sum([tf_pass, ent_pass, pil_pass, aeo_pass, il_pass, sch_pass])}/6")
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
