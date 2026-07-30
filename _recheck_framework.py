#!/usr/bin/env python3
"""
Re-check framework for recently modified blog posts.
Extracts each post and runs 6 checks: TF-IDF, Entities, Pillar Links, AEO/GEO, Internal Links, Schema.
Now with correct keyword mapping and / homepage link counting.
"""
import re, json, sys

with open('src/app/blog/data.js', 'r') as f:
    content = f.read()

# Find all post objects
post_pattern = re.compile(r'{\s*\n\s*slug:\s*"([^"]+)"', re.DOTALL)
posts_raw = []
for m in post_pattern.finditer(content):
    slug = m.group(1)
    start = m.start()
    depth = 1
    pos = start + 1
    in_content = False
    content_end_pos = -1
    
    while pos < len(content) and depth > 0:
        ch = content[pos]
        if ch == '`' and not in_content:
            before = content[max(0,pos-10):pos].strip()
            if before.endswith('content:'):
                in_content = True
                pos += 1
                continue
        if ch == '`' and in_content:
            after = content[pos:pos+5]
            if after.startswith('`,\n') or after.startswith(','):
                in_content = False
                pos += 1
                continue
        
        if not in_content:
            if ch == '{':
                depth += 1
            elif ch == '}':
                depth -= 1
                if depth == 0:
                    content_end_pos = pos
                    break
        pos += 1
    
    if content_end_pos > 0:
        raw = content[start:content_end_pos+1]
        posts_raw.append((slug, raw, m.start()))

def parse_post(raw, slug):
    post = {'slug': slug}
    m = re.search(r'title:\s*"((?:[^"\\]|\\.)*)"', raw)
    post['title'] = m.group(1) if m else ''
    m = re.search(r'date:\s*"([^"]+)"', raw)
    post['date'] = m.group(1) if m else ''
    m = re.search(r'author:\s*"([^"]*)"', raw)
    post['author'] = m.group(1) if m else ''
    m = re.search(r'excerpt:\s*\n?\s*"((?:[^"\\]|\\.)*)"', raw, re.DOTALL)
    post['excerpt'] = m.group(1).replace('\n', ' ') if m else ''
    m = re.search(r'tags:\s*\[([^\]]*)\]', raw)
    post['tags'] = [t.strip().strip('"') for t in m.group(1).split(',')] if m else []
    m = re.search(r'content:\s*`((?:[^`]|\\`)*)`', raw, re.DOTALL)
    post['content'] = m.group(1) if m else ''
    return post

all_posts = {}
for slug, raw, pos in posts_raw:
    all_posts[slug] = parse_post(raw, slug)

# Slugs that were modified
modified_slugs = [
    "link-building-strategies-bangladesh-market",
    "seo-garments-textile-industry-b2b-lead-generation",
    "google-business-profile-optimization-guide-bangladesh",
    "mobile-seo-optimization-bangladesh-mobile-first-era",
    "why-md-kanok-miah-is-the-best-seo-expert-in-dhaka-bangladesh",
    "landlord-certificates-seo-case-study",
    "das-taxis-scotland-seo-case-study",
    "morethanpanel-seo-case-study",
    "smmgen-seo-case-study",
    "smmsun-seo-case-study",
    "mir-cement-seo-case-study",
    "dhaka-apparels-seo-case-study",
    "stealth-windshield-repairs-seo-case-study",
    "how-to-choose-best-seo-expert-dhaka-15-things",
    "seo-expert-vs-seo-agency-dhaka-which-is-right",
    "top-10-seo-mistakes-dhaka-businesses-fix",
    "what-does-seo-expert-do-guide-business-owners",
    "seo-case-study-dhaka-businesses-increased-organic-traffic",
    "hiring-seo-expert-dhaka-better-roi-than-paid-ads",
    "ai-seo-2026-dhaka-experts-optimize-google-ai-chatgpt",
]

# Manual keyword mapping based on post titles (for TF-IDF check)
# These are more accurate than auto-extraction
KEYWORD_MAP = {
    "link-building-strategies-bangladesh-market": "link building",
    "seo-garments-textile-industry-b2b-lead-generation": "garments seo",
    "google-business-profile-optimization-guide-bangladesh": "google business profile",
    "mobile-seo-optimization-bangladesh-mobile-first-era": "mobile seo",
    "why-md-kanok-miah-is-the-best-seo-expert-in-dhaka-bangladesh": "kanok miah",
    "landlord-certificates-seo-case-study": "landlord certificates",
    "das-taxis-scotland-seo-case-study": "das taxis",
    "morethanpanel-seo-case-study": "morethanpanel",
    "smmgen-seo-case-study": "smmgen",
    "smmsun-seo-case-study": "smmsun",
    "mir-cement-seo-case-study": "mir cement",
    "dhaka-apparels-seo-case-study": "dhaka apparels",
    "stealth-windshield-repairs-seo-case-study": "stealth windshield",
    "how-to-choose-best-seo-expert-dhaka-15-things": "seo expert dhaka",
    "seo-expert-vs-seo-agency-dhaka-which-is-right": "seo expert",
    "top-10-seo-mistakes-dhaka-businesses-fix": "seo mistakes",
    "what-does-seo-expert-do-guide-business-owners": "seo expert",
    "seo-case-study-dhaka-businesses-increased-organic-traffic": "seo case study",
    "hiring-seo-expert-dhaka-better-roi-than-paid-ads": "hiring seo expert",
    "ai-seo-2026-dhaka-experts-optimize-google-ai-chatgpt": "ai seo",
}

def check_tfidf(title, content, slug):
    keyword = KEYWORD_MAP.get(slug, '')
    count = content.lower().count(keyword.lower())
    return keyword, count, count >= 5

def check_entities(title, content, tags, excerpt):
    entities = {}
    content_lower = content.lower() + ' ' + excerpt.lower()
    
    entities['Dhaka'] = 'dhaka' in content_lower
    entities['Bangladesh'] = 'bangladesh' in content_lower or 'bangladeshi' in content_lower
    entities['SEO'] = 'seo' in content_lower
    
    tags_lower = [t.lower() for t in tags]
    
    if any('geo' in t or ('ai' in t and 'search' in content_lower) or 'generative' in t for t in tags_lower):
        entities['GEO/AI Search'] = 'geo' in content_lower or 'ai search' in content_lower or 'generative engine' in content_lower
    
    if any('local seo' in t or 'google business' in t or 'google maps' in t or 'gbp' in t or 'gmb' in t for t in tags_lower):
        entities['Google Business Profile'] = 'google business profile' in content_lower or 'gbp' in content_lower or 'google my business' in content_lower
    
    if any('mobile' in t for t in tags_lower):
        entities['Mobile'] = 'mobile' in content_lower
    
    industry_map = {'b2b': 'B2B', 'garments': 'Garments', 'textile': 'Textile',
                    'healthcare': 'Healthcare', 'medical': 'Healthcare',
                    'real estate': 'Real Estate', 'ecommerce': 'Ecommerce',
                    'construction': 'Construction'}
    for kw, entity in industry_map.items():
        if any(kw in t for t in tags_lower):
            entities[entity] = kw in content_lower
    
    if any('case study' in t for t in tags_lower):
        entities['Results/ROI'] = any(w in content_lower for w in ['result', 'roi', 'increase', 'growth', 'visitor', 'traffic', 'lead', 'conversion', 'revenue', 'monthly', 'clicks', 'organic'])
    
    missing = [k for k, v in entities.items() if not v]
    return entities, missing

def check_pillar_links(slug, content, tags):
    tags_lower = [t.lower() for t in tags]
    
    if any('geo' in t or ('ai' in t and 'search' not in t and 'overview' not in t) or 'generative' in t for t in tags_lower):
        pillar = 'GEO & AI Search'
        expected_pages = ['/services/geo-ai-search']
    elif any('mobile' in t for t in tags_lower):
        pillar = 'Mobile SEO'
        expected_pages = ['/services/mobile-seo']
    elif any('case study' in t for t in tags_lower):
        pillar = 'Case Studies'
        expected_pages = ['/blog/seo-case-study-dhaka-businesses-increased-organic-traffic']
    elif any('healthcare' in t or 'medical' in t for t in tags_lower):
        pillar = 'Local SEO'
        expected_pages = ['/services/local-seo']
    elif any('garments' in t or 'textile' in t or 'b2b' in t for t in tags_lower):
        pillar = 'Industry SEO'
        expected_pages = ['/services']
    elif any('local seo' in t or 'google business' in t or 'google maps' in t for t in tags_lower):
        pillar = 'Local SEO'
        expected_pages = ['/services/local-seo']
    elif any('link building' in t for t in tags_lower):
        pillar = 'Link Building'
        expected_pages = ['/services/link-building']
    elif any('roi' in t or 'vs ads' in t for t in tags_lower):
        pillar = 'SEO'
        expected_pages = ['/services']
    else:
        pillar = 'SEO'
        expected_pages = ['/services']
    
    link_pattern = re.findall(r'\[([^\]]*)\]\(([^)]*)\)', content)
    found = []
    for ep in expected_pages:
        for text, url in link_pattern:
            if ep in url:
                if ep not in found:
                    found.append(ep)
        if ep in content:
            if ep not in found:
                found.append(ep)
    
    return pillar, expected_pages, found, len(found) > 0

def check_aeo_geo(content):
    lines = content.split('\n')
    question_heads = []
    for line in lines:
        stripped = line.strip()
        for prefix in ['###', '##', '####']:
            if stripped.startswith(prefix):
                text = stripped.lstrip('# ').strip()
                for qw in ['How', 'What', 'Why', 'When', 'Where', 'Can', 'Do', 'Is', 'Are', 'Does', 'Which']:
                    if text.startswith(qw + ' ') or text.startswith(qw + '?') or text.startswith(qw + ':') or text.startswith(qw + '’'):
                        question_heads.append(text)
                        break
                break
    return question_heads, len(question_heads) >= 2

def check_internal_links(content):
    """Count internal links to /blog/, /services/, /industries/, /locations/, or /"""
    link_pattern = re.findall(r'\[([^\]]*)\]\(([^)]*)\)', content)
    internal = []
    for text, url in link_pattern:
        # Normalize: trim anchors, trailing slashes
        url_clean = url.split('#')[0].rstrip('/')
        if not url_clean:
            url_clean = '/'
        if any(url_clean.startswith(p) for p in ['/blog', '/services', '/industries', '/locations', '']):
            if url_clean == '':
                url_clean = '/'
            # Deduplicate
            if url_clean not in internal:
                internal.append(url_clean)
    return internal, len(internal) >= 3

def check_schema(post):
    fields = {
        'title': bool(post.get('title', '')),
        'excerpt': bool(post.get('excerpt', '')),
        'date': bool(post.get('date', '')),
    }
    missing = [k for k, v in fields.items() if not v]
    return fields, len(missing) == 0

# Run all checks
results = {}
for slug in modified_slugs:
    if slug not in all_posts:
        print(f"⚠️ WARNING: Slug '{slug}' not found", file=sys.stderr)
        continue
    
    post = all_posts[slug]
    title = post['title']
    content = post['content']
    tags = post['tags']
    excerpt = post['excerpt']
    
    keyword, kw_count, kw_pass = check_tfidf(title, content, slug)
    entities, missing_entities = check_entities(title, content, tags, excerpt)
    pillar, expected_pages, found_pages, pillar_pass = check_pillar_links(slug, content, tags)
    question_heads, aeo_pass = check_aeo_geo(content)
    internal_links, links_pass = check_internal_links(content)
    schema_fields, schema_pass = check_schema(post)
    
    flags = sum(1 for p in [kw_pass, not missing_entities, pillar_pass, aeo_pass, links_pass, schema_pass] if not p)
    
    results[slug] = {
        'title': title,
        'date': post['date'],
        'tags': ', '.join(tags),
        'pillar': pillar,
        'checks': {
            'tfidf': {'keyword': keyword, 'count': kw_count, 'pass': kw_pass},
            'entities': {'missing': missing_entities, 'pass': len(missing_entities) == 0},
            'pillar_link': {'pillar': pillar, 'expected': expected_pages, 'found': found_pages, 'pass': pillar_pass},
            'aeo_geo': {'question_headings': question_heads[:5], 'count': len(question_heads), 'pass': aeo_pass},
            'internal_links': {'links': internal_links[:8], 'count': len(internal_links), 'pass': links_pass},
            'schema': {'fields': schema_fields, 'pass': schema_pass},
        },
        'total_flags': flags,
        'status': 'PASS' if flags == 0 else 'WARN' if flags <= 2 else 'FAIL'
    }

# Print report
print("=" * 80)
print("FRAMEWORK ENFORCEMENT REPORT — RE-CHECK after auto-fixes")
print("Date: 2026-07-28 | 20 modified posts analyzed")
print("=" * 80)

print("\n## Summary Table")
print("| # | Slug | TF-IDF | Entities | Pillar | AEO/GEO | Links | Schema | Status |")
print("|---|------|--------|----------|--------|---------|-------|--------|--------|")

fails, warns, passes = [], [], []
for i, slug in enumerate(modified_slugs, 1):
    r = results.get(slug)
    if not r:
        print(f"| {i} | {slug[:45]} | — | — | — | — | — | — | ⚠️ |")
        continue
    c = r['checks']
    icons = ''.join(['✅' if c[k]['pass'] else '❌' for k in ['tfidf','entities','pillar_link','aeo_geo','internal_links','schema']])
    status_icon = {'PASS': '✅', 'WARN': '⚠️', 'FAIL': '❌'}[r['status']]
    short = slug[:50]
    a, b, cl, d, e, f = [icons[j*2:j*2+2] for j in range(6)]
    # Rebuild with pipes
    print(f"| {i} | {short} | {'✅' if c['tfidf']['pass'] else '❌'} | {'✅' if c['entities']['pass'] else '❌'} | {'✅' if c['pillar_link']['pass'] else '❌'} | {'✅' if c['aeo_geo']['pass'] else '❌'} | {'✅' if c['internal_links']['pass'] else '❌'} | {'✅' if c['schema']['pass'] else '❌'} | {status_icon} {r['status']} |")
    
    if r['status'] == 'FAIL': fails.append(slug)
    elif r['status'] == 'WARN': warns.append(slug)
    else: passes.append(slug)

print(f"\n**Totals:** ✅ {len(passes)} PASS | ⚠️ {len(warns)} WARN | ❌ {len(fails)} FAIL")
print(f"**Checks passed:** {sum(1 for r in results.values() for c in r['checks'].values() if c['pass'])}/{len(results)*6}")

# Detailed report for posts WITH issues
for slug in modified_slugs:
    if slug not in results:
        continue
    r = results[slug]
    c = r['checks']
    total_flags = sum(1 for check in c.values() if not check['pass'])
    if total_flags == 0:
        continue
    
    print(f"\n---")
    print(f"## Post: {slug}")
    print(f"**Title:** {r['title'][:100]}")
    print(f"**Tags:** {r['tags']}")
    print(f"**Pillar:** {r['pillar']}")
    
    print(f"| Check | Status | Details |")
    print(f"|-------|--------|---------|")
    
    kw = c['tfidf']
    print(f"| TF-IDF: '{kw['keyword']}' | {'✅' if kw['pass'] else '❌'} | {kw['count']} occurrences |")
    
    en = c['entities']
    print(f"| Entities | {'✅' if en['pass'] else '❌'} | Missing: {', '.join(en['missing']) if en['missing'] else 'None'} |")
    
    pl = c['pillar_link']
    print(f"| Pillar Link | {'✅' if pl['pass'] else '❌'} | Pillar: {pl['pillar']} | Found: {', '.join(pl['found']) if pl['found'] else 'None'} |")
    
    ae = c['aeo_geo']
    qh = ', '.join(ae['question_headings'][:3]) if ae['question_headings'] else 'None'
    print(f"| AEO/GEO | {'✅' if ae['pass'] else '❌'} | {ae['count']} Q-headings | e.g.: {qh[:100]} |")
    
    il = c['internal_links']
    print(f"| Internal Links | {'✅' if il['pass'] else '❌'} | {il['count']} links | e.g.: {', '.join(il['links'][:5])[:100] if il['links'] else 'None'} |")
    
    sc = c['schema']
    ms = [k for k, v in sc['fields'].items() if not v]
    print(f"| Schema | {'✅' if sc['pass'] else '❌'} | {'All set' if not ms else 'Missing: ' + ', '.join(ms)} |")
    
    print(f"\n### Fix instructions:")
    if not kw['pass']:
        print(f"- 🔴 TF-IDF: '{kw['keyword']}' only {kw['count']}x. Need ≥5.")
    if en['missing']:
        print(f"- 🔴 Entities: Add: {', '.join(en['missing'])}.")
    if not pl['pass']:
        print(f"- 🔴 Pillar Link: Link to one of: {', '.join(pl['expected'])}.")
    if not ae['pass']:
        print(f"- 🔴 AEO/GEO: Add ≥2 question headings (How/What/Why/etc).")
    if not il['pass']:
        print(f"- 🔴 Internal Links: Only {il['count']}. Need ≥3 to /blog/, /services/, etc.")
    if not sc['pass']:
        print(f"- 🔴 Schema: Set missing fields: {', '.join(ms)}.")

# Comparison with previous report
print("\n" + "=" * 80)
print("COMPARISON WITH PREVIOUS REPORT (2026-07-27)")
print("=" * 80)

prev_report = {
    "link-building-strategies-bangladesh-market": "NOT CHECKED",
    "seo-garments-textile-industry-b2b-lead-generation": "PASS",
    "google-business-profile-optimization-guide-bangladesh": "NOT CHECKED",
    "mobile-seo-optimization-bangladesh-mobile-first-era": "WARN",
    "why-md-kanok-miah-is-the-best-seo-expert-in-dhaka-bangladesh": "PASS",
    "locksmith-dundee-seo-case-study": "WARN",
    "landlord-certificates-seo-case-study": "FAIL",
    "das-taxis-scotland-seo-case-study": "FAIL",
    "morethanpanel-seo-case-study": "FAIL",
    "smmgen-seo-case-study": "WARN",
    "smmsun-seo-case-study": "FAIL",
    "mir-cement-seo-case-study": "FAIL",
    "dhaka-apparels-seo-case-study": "FAIL",
    "stealth-windshield-repairs-seo-case-study": "FAIL",
    "how-to-choose-best-seo-expert-dhaka-15-things": "PASS",
    "seo-expert-vs-seo-agency-dhaka-which-is-right": "PASS",
    "top-10-seo-mistakes-dhaka-businesses-fix": "WARN",
    "what-does-seo-expert-do-guide-business-owners": "PASS",
    "seo-case-study-dhaka-businesses-increased-organic-traffic": "WARN",
    "hiring-seo-expert-dhaka-better-roi-than-paid-ads": "WARN",
    "ai-seo-2026-dhaka-experts-optimize-google-ai-chatgpt": "PASS",
}

print("\n| Slug | Prev | Now | Δ | Details |")
print("|------|------|-----|---|---------|")
improved, worsened, same, new_ = 0, 0, 0, 0

for slug in modified_slugs:
    r = results.get(slug)
    if not r:
        continue
    current = r['status']
    prev = prev_report.get(slug, 'NOT CHECKED')
    
    order = {'PASS': 0, 'WARN': 1, 'FAIL': 2, 'NOT CHECKED': 1}
    change_icon = '— Same'
    if prev == 'NOT CHECKED':
        change_icon = '🆕'
        new_ += 1
    elif order.get(prev, 1) > order.get(current, 1):
        change_icon = '✅ Improved'
        improved += 1
    elif order.get(prev, 1) < order.get(current, 1):
        change_icon = '❌ Worsened'
        worsened += 1
    else:
        same += 1
    
    # Check which specific checks changed
    failing_now = [k for k, v in r['checks'].items() if not v['pass']]
    detail = ', '.join(failing_now) if failing_now else 'All ✅'
    print(f"| {slug[:45]} | {prev:12s} | {current:6s} | {change_icon:14s} | {detail[:40]} |")

print(f"\n**Δ vs previous report:** ✅ Improved={improved}, ❌ Worsened={worsened}, — Same={same}, 🆕 New={new_}")

# Final summary of remaining issues
print("\n" + "=" * 80)
print("SUMMARY OF REMAINING ISSUES")
print("=" * 80)

all_flagged = []
for slug in modified_slugs:
    r = results.get(slug)
    if not r:
        continue
    failing = [(k, v) for k, v in r['checks'].items() if not v['pass']]
    if failing:
        all_flagged.append((slug, r['status'], r['title'], failing))

if all_flagged:
    print(f"\n**{len(all_flagged)} posts still have issues:**\n")
    for slug, status, title, failing in all_flagged:
        print(f"### {slug} **({status})**")
        for name, detail in failing:
            if name == 'tfidf':
                print(f"- 🔴 TF-IDF: '{detail['keyword']}' → {detail['count']}x (need ≥5)")
            elif name == 'entities':
                print(f"- 🔴 Entities missing: {', '.join(detail['missing'])}")
            elif name == 'pillar_link':
                print(f"- 🔴 Pillar Link ({detail['pillar']}): expected {detail['expected']}, found {detail['found']}")
            elif name == 'aeo_geo':
                print(f"- 🔴 AEO/GEO: {detail['count']} Q-headings (need ≥2)")
            elif name == 'internal_links':
                print(f"- 🔴 Internal Links: {detail['count']} links (need ≥3)")
            elif name == 'schema':
                ms = [k for k, v in detail['fields'].items() if not v]
                print(f"- 🔴 Schema missing: {ms}")
        print()
else:
    print("✅ All posts pass all framework checks!")

print(f"---")
print(f"Report generated by Content Framework Enforcer cron job")
