#!/usr/bin/env python3
"""Run all 6 framework checks on a single blog post specified by slug."""
import re, sys

DATA_FILE = "/root/kanok-miahit/src/app/blog/data.js"
SLUG = sys.argv[1] if len(sys.argv) > 1 else "hiring-seo-expert-dhaka-better-roi-than-paid-ads"

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

post = parse_post(source, SLUG)
if not post:
    print(f"ERROR: Post '{SLUG}' not found!")
    exit(1)

title = get_str(post, 'title')
excerpt = get_str(post, 'excerpt')
date = get_str(post, 'date')
author = get_str(post, 'author')
tags = get_tags(post)
content = get_content(post)

print(f"=== Post: {SLUG} ===")
print(f"Title: {title}")
print(f"Date: {date}")
print(f"Author: {author}")
print(f"Tags: {tags}")
print(f"Content length: {len(content)} chars")
print(f"Excerpt: {excerpt[:100]}...")
print()

# ============================================================
# CRITERION 1: TF-IDF / Keyword density
# ============================================================
# Primary keyword for this post: "seo roi", "seo vs ads", "seo Dhaka"
kw = "seo roi"
alt_kw = ["seo vs ads", "seo dhaka", "seo expert dhaka", "better roi", "organic search", "paid ads", "google ads"]
c_lower = content.lower()
tfidf_n = c_lower.count(kw)
best_kw = kw
for ak in alt_kw:
    n = c_lower.count(ak)
    if n > tfidf_n:
        tfidf_n = n
        best_kw = ak
tf_pass = tfidf_n >= 5
print(f"CRITERION 1: TF-IDF (keyword density)")
print(f"  Best keyword found: '{best_kw}'")
print(f"  Occurrences: {tfidf_n}")
print(f"  Threshold: ≥5")
print(f"  Result: {'✅ PASS' if tf_pass else '❌ FAIL'}")

# ============================================================
# CRITERION 2: Entities
# ============================================================
missing_ents = []
if 'dhaka' not in c_lower: missing_ents.append("Dhaka")
if 'bangladesh' not in c_lower: missing_ents.append("Bangladesh")
if 'seo' not in c_lower: missing_ents.append("SEO")
if 'roi' not in c_lower: missing_ents.append("ROI")
if 'paid' not in c_lower: missing_ents.append("Paid Ads")
ent_pass = len(missing_ents) == 0
print(f"\nCRITERION 2: Entities")
print(f"  Required: Dhaka, Bangladesh, SEO, ROI, Paid Ads")
print(f"  Missing: {missing_ents if missing_ents else 'None'}")
print(f"  Result: {'✅ PASS' if ent_pass else '❌ FAIL'}")

# ============================================================
# CRITERION 3: Pillar Link
# ============================================================
# Expected: link to /services/ or /services/local-seo
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
print(f"\nCRITERION 3: Pillar Link")
print(f"  Expected: link to /services/ or /industries/ or /blog/")
print(f"  Found pillar links: {pil_found if pil_found else 'None'}")
print(f"  Result: {'✅ PASS' if pil_pass else '❌ FAIL'}")

# ============================================================
# CRITERION 4: AEO/GEO (question headings)
# ============================================================
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
print(f"\nCRITERION 4: AEO/GEO Question Headings")
print(f"  Total headings: {len(headings)}")
print(f"  Question headings ({len(qh)}): {qh if qh else 'None'}")
print(f"  Threshold: ≥2")
print(f"  Result: {'✅ PASS' if aeo_pass else '❌ FAIL'}")

# ============================================================
# CRITERION 5: Internal Links
# ============================================================
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
print(f"\nCRITERION 5: Internal Links")
print(f"  Total unique internal links: {len(internals)}")
for i, link in enumerate(sorted(internals), 1):
    print(f"    {i}. {link}")
print(f"  Threshold: ≥3")
print(f"  Result: {'✅ PASS' if il_pass else '❌ FAIL'}")

# ============================================================
# CRITERION 6: Schema Readiness
# ============================================================
sch_missing = []
if not title: sch_missing.append('title')
if not excerpt: sch_missing.append('excerpt/description')
if not date: sch_missing.append('date')
if not author: sch_missing.append('author')
if not tags: sch_missing.append('tags')
sch_pass = len(sch_missing) == 0
print(f"\nCRITERION 6: Schema Readiness")
print(f"  Title: {'✅' if title else '❌'} ({title[:80] if title else 'MISSING'})")
print(f"  Excerpt: {'✅' if excerpt else '❌'} ({excerpt[:80] if excerpt else 'MISSING'})")
print(f"  Date: {'✅' if date else '❌'} ({date if date else 'MISSING'})")
print(f"  Author: {'✅' if author else '❌'} ({author if author else 'MISSING'})")
print(f"  Tags: {'✅' if tags else '❌'} ({tags if tags else 'MISSING'})")
print(f"  Result: {'✅ PASS' if sch_pass else '❌ FAIL'}")

# ============================================================
# OVERALL
# ============================================================
all_pass = all([tf_pass, ent_pass, pil_pass, aeo_pass, il_pass, sch_pass])
print(f"\n{'='*60}")
print(f"OVERALL RESULT: {'✅ ALL 6 CHECKS PASSED' if all_pass else '❌ SOME CHECKS FAILED'}")
print(f"  Passing: {sum([tf_pass, ent_pass, pil_pass, aeo_pass, il_pass, sch_pass])}/6")
fails = []
if not tf_pass: fails.append("TF-IDF")
if not ent_pass: fails.append("Entities")
if not pil_pass: fails.append("Pillar Link")
if not aeo_pass: fails.append("AEO/GEO")
if not il_pass: fails.append("Internal Links")
if not sch_pass: fails.append("Schema Readiness")
if fails:
    print(f"  Failing checks: {', '.join(fails)}")

# ============================================================
# DETAILED REPORT
# ============================================================
print(f"\n{'='*60}")
print("FRAMEWORK CHECK REPORT")
print(f"{'='*60}")
print(f"Post: {SLUG}")
print(f"Title: {title}")
print(f"Date: {date}")
print(f"Author: {author}")
print(f"Tags: {tags}")
print(f"Content Length: {len(content)} characters")
# Format strings without backslash in f-strings
tfidf_status = 'PASS' if tf_pass else 'FAIL'
ent_status = 'PASS' if ent_pass else 'FAIL'
pil_status = 'PASS' if pil_pass else 'FAIL'
aeo_status = 'PASS' if aeo_pass else 'FAIL'
il_status = 'PASS' if il_pass else 'FAIL'
sch_status = 'PASS' if sch_pass else 'FAIL'
tfidf_detail = 'keyword="' + best_kw + '"'
tfidf_count = 'occurrences=' + str(tfidf_n) + ' (need >=5)'
ent_detail = 'Missing: ' + str(missing_ents) if missing_ents else 'All present'
pil_detail = 'Found: ' + str(pil_found) if pil_found else 'None'
aeo_detail = str(len(qh)) + ' question headings (need >=2)'
il_detail = str(len(internals)) + ' unique internal links (need >=3)'
sch_detail = 'All fields set' if sch_pass else 'Missing: ' + str(sch_missing)

print('=' * 60)
print('| {:<22} | {:<8} | {:<40} |'.format('Check', 'Status', 'Details'))
print('|{:-<22}-+-{:-<8}-+-{:-<40}-|'.format('', '', ''))
print('| {:<22} | {:<8} | {:<40} |'.format('TF-IDF Keyword Density', tfidf_status, tfidf_detail))
print('| {:<22} | {:<8} | {:<40} |'.format('', '', tfidf_count))
print('| {:<22} | {:<8} | {:<40} |'.format('Entities', ent_status, ent_detail))
print('| {:<22} | {:<8} | {:<40} |'.format('Pillar Link', pil_status, pil_detail))
print('| {:<22} | {:<8} | {:<40} |'.format('AEO/GEO Questions', aeo_status, aeo_detail))
print('| {:<22} | {:<8} | {:<40} |'.format('Internal Links', il_status, il_detail))
print('| {:<22} | {:<8} | {:<40} |'.format('Schema Readiness', sch_status, sch_detail))
print('=' * 60)

# Fix instructions
print(f"\n### Fix Instructions:")
fixes = []
if not tf_pass:
    fixes.append(f"- ❌ **TF-IDF thin**: '{best_kw}' appears only {tfidf_n}x in content. Add ≥5 occurrences.")
if not ent_pass:
    fixes.append(f"- ❌ **Missing entities**: {', '.join(missing_ents)} not mentioned in post content.")
if not pil_pass:
    fixes.append(f"- ❌ **No pillar link**: Post doesn't link to any related service, industry, or blog page.")
if not aeo_pass:
    fixes.append(f"- ❌ **AEO/GEO weak**: Only {len(qh)} question heading(s). Add ≥2 FAQ-style headings with '?' mark.")
if not il_pass:
    fixes.append(f"- ❌ **Too few internal links**: Only {len(internals)} internal link(s). Add ≥3 links to posts, services, or industries.")
if not sch_pass:
    fixes.append(f"- ❌ **Schema fields missing**: {', '.join(sch_missing)}. Add these for ArticleSchema.")
if all_pass:
    fixes.append("- ✅ **All checks passed** — no fixes needed.")
for f in fixes:
    print(f)
print()
