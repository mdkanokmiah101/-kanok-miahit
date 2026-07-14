#!/usr/bin/env python3
"""Framework checks on blog posts in data.js — v3 with improved keyword extraction"""

import re

DATA_FILE = "/root/kanok-miahit/src/app/blog/data.js"

with open(DATA_FILE, 'r', encoding='utf-8') as f:
    content = f.read()

target_slugs = [
    "mobile-seo-optimization-bangladesh-mobile-first-era",
    "content-marketing-strategy-bangladeshi-brands-seo",
    "international-seo-bangladesh-exporters-global-buyers",
    "seo-bangla-beginners-guide-google-ranking",
    "local-seo-dhaka-google-maps-ranking",
    "seo-trends-2026-ai-geo-future",
    "technical-seo-core-web-vitals-optimization",
    "ecommerce-seo-daraz-shopify-guide",
    "link-building-bangladesh-strategies",
    "keyword-research-bangladesh-market",
    "content-marketing-seo-friendly-content-writing",
]

EN_STOP = {
    'the','a','an','is','are','was','were','be','been','being','have','has','had',
    'do','does','did','will','would','can','could','shall','should','may','might',
    'must','on','in','at','by','for','of','to','with','from','into','through',
    'during','before','after','above','below','between','out','off','over','under',
    'again','further','then','once','here','there','when','where','why','how',
    'all','each','every','both','few','more','most','other','some','such','no',
    'nor','not','only','own','same','so','than','too','very','just','because',
    'as','until','while','about','and','but','or','if','what','which','who',
    'your','our','its','their','my','his','her','itself','himself','myself',
    'yourself','themselves','ultimate','complete','comprehensive','best','top',
    'guide','expert','professional','affordable','effective','proven','simple',
    'easy','essential','ultimate','definitive','beginner','advanced',
}

def extract_post(data, slug):
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

def get_field(post_text, name):
    if name == 'tags':
        m = re.search(r'tags:\s*\[([^\]]*)\]', post_text)
        return re.findall(r'"([^"]*)"', m.group(1)) if m else []
    if name == 'content':
        m = re.search(r'content:\s*`', post_text)
        if not m:
            return None
        start = m.end()
        rest = post_text[start:]
        i = 0
        while i < len(rest):
            if rest[i] == '`':
                after = rest[i+1:].lstrip()
                if after.startswith(',') or after.startswith('\n') or after.startswith('}'):
                    return rest[:i]
            i += 1
        return rest
    m = re.search(rf'{name}:\s*"', post_text)
    if not m:
        return None
    start = m.end()
    val = ""
    i = start
    while i < len(post_text):
        if post_text[i] == '\\' and i+1 < len(post_text):
            val += post_text[i] + post_text[i+1]
            i += 2
        elif post_text[i] == '"':
            break
        else:
            val += post_text[i]
            i += 1
    return val

def get_keyword(title):
    """Extract primary keyword from title: first 2 meaningful words (skip English stopwords)."""
    if not title:
        return None
    words = title.split()
    parts = []
    for w in words:
        wc = w.strip('":;,.-!?\'()[]').lower()
        # Skip English stopwords (articles, prepositions, common SEO filler)
        if wc in EN_STOP:
            continue
        parts.append(w.strip('":;,.-!?\''))
        if len(parts) >= 2:
            break
    # If nothing meaningful, take first word
    if not parts and words:
        return words[0].strip('":;,.-!?\'')
    return ' '.join(parts) if parts else None

def count_in_text(text, keyword):
    if not text or not keyword:
        return 0
    return len(re.findall(re.escape(keyword), text, re.IGNORECASE))

def extract_markdown_links(text):
    if not text:
        return []
    return re.findall(r'\[([^\]]*)\]\(([^)]*)\)', text)

def extract_href_links(text):
    if not text:
        return []
    return re.findall(r'href="([^"]*)"', text)

def get_all_links(text):
    links = set()
    for label, url in extract_markdown_links(text):
        if url.startswith('/') and not url.startswith('/#'):
            links.add(url)
    for url in extract_href_links(text):
        if url.startswith('/') and not url.startswith('/#'):
            links.add(url)
    return list(links)

# Results
results = []

for slug in target_slugs:
    post_text = extract_post(content, slug)
    if post_text is None:
        print(f"ERROR: could not find {slug}")
        continue

    title = get_field(post_text, 'title')
    date = get_field(post_text, 'date')
    excerpt = get_field(post_text, 'excerpt')
    tags = get_field(post_text, 'tags')
    content_body = get_field(post_text, 'content')

    # ---- CHECK A: TF-IDF ----
    keyword = get_keyword(title)
    kw_count = count_in_text(content_body, keyword) if keyword and content_body else 0
    flag_a = kw_count < 5

    # ---- CHECK B: Entities ----
    entities = ['Dhaka', 'Bangladesh', 'Google', 'SEO']
    ent_counts = {}
    ent_missing = []
    for e in entities:
        c = count_in_text(content_body, e) if content_body else 0
        ent_counts[e] = c
        if c == 0:
            ent_missing.append(e)
    flag_b = len(ent_missing) > 0

    # ---- CHECK C: Pillar links ----
    all_links = get_all_links(content_body) if content_body else []
    s_links = sum(1 for l in all_links if '/services/' in l)
    i_links = sum(1 for l in all_links if '/industries/' in l)
    b_links = sum(1 for l in all_links if '/blog/' in l)
    flag_c = (s_links + i_links + b_links) == 0

    # ---- CHECK D: AEO/GEO question headings ----
    q_words = ['How', 'What', 'Why', 'When', 'Where', 'Can', 'Do', 'Is', 'Are']
    qh_count = 0
    if content_body:
        headings = re.findall(r'^#{1,6}\s+(.+)', content_body, re.MULTILINE)
        for h in headings:
            h = h.strip()
            if not h:
                continue
            fw = h.split()[0].rstrip('?:;,!') if h.split() else ''
            for qw in q_words:
                if fw.lower() == qw.lower():
                    qh_count += 1
                    break
    flag_d = qh_count < 2

    # ---- CHECK E: Internal links ----
    il_count = len(all_links)
    flag_e = il_count < 3

    # ---- CHECK F: Schema ----
    schema_missing = []
    if not title: schema_missing.append('title')
    if not excerpt: schema_missing.append('excerpt')
    if not date: schema_missing.append('date')
    flag_f = len(schema_missing) > 0

    total_flags = sum([flag_a, flag_b, flag_c, flag_d, flag_e, flag_f])

    r = {
        'slug': slug, 'title': title, 'keyword': keyword, 'kw_count': kw_count,
        'flag_a': flag_a, 'ent_counts': ent_counts, 'ent_missing': ent_missing,
        'flag_b': flag_b, 's_links': s_links, 'i_links': i_links, 'b_links': b_links,
        'flag_c': flag_c, 'qh_count': qh_count, 'flag_d': flag_d,
        'il_count': il_count, 'flag_e': flag_e,
        'schema_missing': schema_missing, 'flag_f': flag_f, 'total_flags': total_flags,
    }
    results.append(r)

    # ---- PER-POST REPORT ----
    print(f"\n{'='*72}")
    print(f"📄 {slug}")
    print(f"{'='*72}")
    print(f"  Title:    {title}")
    print(f"  Date:     {date}")
    print(f"  Tags:     {tags}")
    print(f"  Content:  {len(content_body) if content_body else 0} chars")
    print()
    print(f"  A (TF-IDF):  '{keyword}' → {kw_count}x {'⚠️ <5' if flag_a else '✅ ≥5'}")
    ent_str = ' '.join(f"{e}={ent_counts[e]}" for e in entities)
    ent_str += f"  ⚠️ missing: {ent_missing}" if ent_missing else "  ✅ all present"
    print(f"  B (Entities):{ent_str}")
    print(f"  C (Pillar):  /services/:{s_links} /industries/:{i_links} /blog/:{b_links} {'⚠️ none' if flag_c else '✅ found'}")
    print(f"  D (AEO/GEO): {qh_count} question headings {'⚠️ <2' if flag_d else '✅ ≥2'}")
    print(f"  E (Int Lnk): {il_count} internal links {'⚠️ <3' if flag_e else '✅ ≥3'}")
    print(f"  F (Schema):  missing={schema_missing} {'⚠️' if flag_f else '✅ all set'}")
    print(f"  🚩 TOTAL: {total_flags}/6 flags")

# ====== SUMMARY TABLE ======
print(f"\n\n{'='*110}")
print("📊 SUMMARY TABLE — Batch 2 Framework Checks")
print(f"{'='*110}")
print(f"{'#':<3} {'Slug':<48} {'A':<5} {'B':<5} {'C':<5} {'D':<5} {'E':<5} {'F':<5} {'🚩':<4} {'Keyword (A)':<30}")
print("-"*110)
for i, r in enumerate(results, 1):
    s = r['slug'][:46] + '..' if len(r['slug']) > 47 else r['slug']
    kw = r['keyword']
    kw_short = (kw[:27] + '..') if kw and len(kw) > 28 else (kw or '')
    line = f"{i:<3} {s:<48} "
    line += f"{'⚠️' if r['flag_a'] else '✅':<5} "
    line += f"{'⚠️' if r['flag_b'] else '✅':<5} "
    line += f"{'⚠️' if r['flag_c'] else '✅':<5} "
    line += f"{'⚠️' if r['flag_d'] else '✅':<5} "
    line += f"{'⚠️' if r['flag_e'] else '✅':<5} "
    line += f"{'⚠️' if r['flag_f'] else '✅':<5} "
    line += f"{r['total_flags']:<4} {kw_short:<30}"
    print(line)

print("-"*110)
print(f"\nPassing ✅ = {sum(1 for r in results if r['total_flags']==0)}/{len(results)}")
for i, r in enumerate(results):
    if r['total_flags'] == 0:
        print(f"  ✅ #{i+1} {r['slug']} — all checks pass")

# ====== ISSUES ======
print(f"\n{'='*110}")
print("🔍 POSTS WITH ISSUES")
print(f"{'='*110}")
for i, r in enumerate(results, 1):
    issues = []
    if r['flag_a']:
        issues.append(f"A: primary keyword '{r['keyword']}' appears only {r['kw_count']}x in content (<5)")
    if r['flag_b']:
        issues.append(f"B: missing entity/entities: {r['ent_missing']}")
    if r['flag_c']:
        issues.append(f"C: no pillar links to /services/, /industries/, or /blog/")
    if r['flag_d']:
        issues.append(f"D: only {r['qh_count']} question-based heading(s) found (<2)")
    if r['flag_e']:
        issues.append(f"E: only {r['il_count']} internal link(s) found (<3)")
    if r['flag_f']:
        issues.append(f"F: schema field(s) missing: {r['schema_missing']}")
    if issues:
        print(f"\n  #{i} {r['slug']}")
        for iss in issues:
            print(f"    • {iss}")

# ====== ENTITY TABLE ======
print(f"\n\n{'='*110}")
print("📋 ENTITY COUNTS (per post)")
print(f"{'='*110}")
print(f"{'#':<3} {'Slug':<48} {'Dhaka':<8} {'Bangladesh':<12} {'Google':<8} {'SEO':<8}")
print("-"*110)
for i, r in enumerate(results, 1):
    s = r['slug'][:46] + '..' if len(r['slug']) > 47 else r['slug']
    print(f"{i:<3} {s:<48} {r['ent_counts'].get('Dhaka',0):<8} {r['ent_counts'].get('Bangladesh',0):<12} {r['ent_counts'].get('Google',0):<8} {r['ent_counts'].get('SEO',0):<8}")

# ====== INTERNAL LINKS TABLE ======
print(f"\n\n{'='*110}")
print("📋 INTERNAL / PILLAR LINKS (per post)")
print(f"{'='*110}")
print(f"{'#':<3} {'Slug':<48} {'Total Int':<10} {'/services/':<11} {'/industries/':<13} {'/blog/':<8}")
print("-"*110)
for i, r in enumerate(results, 1):
    s = r['slug'][:46] + '..' if len(r['slug']) > 47 else r['slug']
    print(f"{i:<3} {s:<48} {r['il_count']:<10} {r['s_links']:<11} {r['i_links']:<13} {r['b_links']:<8}")

print(f"\n{'='*110}")
print(f"✅ Batch 2 complete — {len(results)} posts checked")
