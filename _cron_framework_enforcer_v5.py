#!/usr/bin/env python3
"""Content Framework Enforcer v5 — final clean version."""

import re

MODIFIED_SLUGS = [
    "das-taxis-scotland-seo-case-study",
    "dhaka-apparels-seo-case-study",
    "hiring-seo-expert-dhaka-better-roi-than-paid-ads",
    "locksmith-dundee-seo-case-study",
    "mir-cement-seo-case-study",
    "morethanpanel-seo-case-study",
    "seo-case-study-dhaka-businesses-increased-organic-traffic",
    "seo-expert-vs-seo-agency-dhaka-which-is-right",
    "smmgen-seo-case-study",
    "smmsun-seo-case-study",
    "stealth-windshield-repairs-seo-case-study",
    "top-10-seo-mistakes-dhaka-businesses-fix",
    "watchzonebd-seo-case-study",
]

DATA_FILE = "/root/kanok-miahit/src/app/blog/data.js"

def unescape_content(s):
    return s.replace("\\'", "'").replace('\\"', '"').replace('\\n', '\n').replace('\\t', '\t')

def parse_posts(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()
    text = re.sub(r'module\.exports\s*=.*', '', text)
    m = re.search(r'const\s+posts\s*=\s*\[(.*)\]', text, re.DOTALL)
    if not m:
        raise ValueError("Could not find posts array")
    array_body = m.group(1)
    posts_raw = []
    depth = 0; start = None
    for i, ch in enumerate(array_body):
        if ch == '{':
            if depth == 0: start = i
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0 and start is not None:
                posts_raw.append(array_body[start:i+1]); start = None
    posts = []
    for raw in posts_raw:
        post = {}
        slug_m = re.search(r'''slug:\s*["']([^"']+)["']''', raw)
        post['slug'] = slug_m.group(1) if slug_m else None
        title_m = re.search(r'''title:\s*["']([^"']+)["']''', raw)
        post['title'] = title_m.group(1) if title_m else None
        date_m = re.search(r'''date:\s*["']([^"']+)["']''', raw)
        post['date'] = date_m.group(1) if date_m else None
        excerpt_m = re.search(r'''excerpt:\s*["']([^"']+)["']''', raw)
        post['excerpt'] = excerpt_m.group(1) if excerpt_m else None
        tags_m = re.search(r'tags:\s*\[([^\]]+)\]', raw)
        post['tags'] = re.findall(r"""["']([^"']+)["']""", tags_m.group(1)) if tags_m else []
        content_m = re.search(r'content:\s*`(.*)`', raw, re.DOTALL)
        post['content'] = unescape_content(content_m.group(1)) if content_m else ''
        if post['slug']: posts.append(post)
    return posts

posts = parse_posts(DATA_FILE)
post_map = {p['slug']: p for p in posts}

def get_primary_keywords(title, slug):
    """Return a list of keyword candidates ordered by relevance."""
    cand = []
    t = title.strip() if title else ""
    sl = slug.lower() if slug else ""
    
    # 1. Brand name from case study slugs
    if '-seo-case-study' in sl:
        brand = sl.replace('-seo-case-study', '').replace('-', ' ')
        cand.append(brand)
        cand.append(brand.split()[0])  # first word of brand
    
    # 2. Title pattern: "X SEO Case Study: ..." or "X SEO: ..." -> brand X
    m = re.match(r'^(.+?)\s+(SEO|Case Study)\s*[:\-–—]', t, re.IGNORECASE)
    if m:
        cand.append(m.group(1).strip())
    
    # 3. Title pattern: "SEO Case Study: How Businesses in X..." -> focus on X
    m = re.match(r'^SEO\s+Case\s+Study\s*:\s+(.+)$', t, re.IGNORECASE)
    if m:
        rest = m.group(1).strip()
        words = re.sub(r'^(how|what|why|when|where)\s+', '', rest, flags=re.IGNORECASE).split()
        np = ' '.join(w for w in words if w.lower() not in {'a','an','the','in','of','to','for','and','or','from','by','with','at'})
        if np: cand.append(np[:50])
        cand.append('SEO')
    
    # 4. "X vs Y" title -> both X and Y
    m = re.match(r'^(.+?)\s+vs\.?\s+(.+)$', t, re.IGNORECASE)
    if m:
        cand.append(m.group(1).strip())
        cand.append(m.group(2).split(' in')[0].split(' for')[0].strip())
    
    # 5. "Top N X" -> X
    m = re.match(r'^(Top\s+\d+\s+)(.+?)(?:\s*\(.*)?$', t, re.IGNORECASE)
    if m:
        cand.append(m.group(2).strip())
    
    # 6. "Why/How/What X..." -> skip question word, take main NP
    m = re.match(r'^(How|What|Why|When|Where|Can|Do|Is|Are|Does|Which)\s+(.+)$', t, re.IGNORECASE)
    if m:
        rest = m.group(2).strip()
        stopwords = {'a','an','the','for','in','of','to','and','is','are','was','were','your','you','it','its','with','from','by','at','on'}
        words = rest.split()
        kw = [w.strip('.,:;!?"\'()-') for w in words if w.lower() not in stopwords or len(w) > 3]
        if kw: cand.append(' '.join(kw[:4]))
    
    # 7. Location + "SEO" combo
    loc_m = re.search(r'\b(Dhaka|Bangladesh)\b', t, re.IGNORECASE)
    if loc_m:
        cand.append(f"SEO {loc_m.group(1).lower()}")
        cand.append(f"SEO in {loc_m.group(1).lower()}")
    
    # 8. Generic fallback: "SEO"
    cand.append("SEO")
    
    return list(dict.fromkeys(cand))  # deduplicate preserving order

def check_tfidf(post):
    content = post.get('content', '')
    content_lower = content.lower()
    candidates = get_primary_keywords(post.get('title', ''), post.get('slug', ''))
    
    best_kw = candidates[0]
    best_count = 0
    
    for kw in candidates:
        kwl = kw.lower()
        count = content_lower.count(kwl)
        if count > best_count:
            best_count = count
            best_kw = kw
    
    # Content-length-adjusted threshold: longer posts should have more
    clen = len(content)
    threshold = 5 if clen > 5000 else 3 if clen > 2000 else 2
    passed = best_count >= threshold
    return best_kw, passed, best_count

def check_entities(post):
    content = post.get('content', '').lower()
    slug = post.get('slug', '').lower()
    missing = []
    for loc, name in [('dhaka', 'Dhaka'), ('bangladesh', 'Bangladesh')]:
        if loc not in content: missing.append(name)
    if not any(s in content for s in ['seo', 'search engine optimization']):
        missing.append('SEO service')
    if 'scotland' in slug and 'scotland' not in content:
        missing.append('Scotland')
    if 'dundee' in slug and 'dundee' not in content:
        missing.append('Dundee')
    passed = len(missing) == 0
    found = [l for l in ['dhaka','bangladesh','scotland','dundee'] if l in content]
    return passed, missing, found

def check_pillar_link(post):
    tags = post.get('tags', [])
    content = post.get('content', '')
    pillars = {
        'SEO Guide': '/blog/complete-seo-guide-bangladesh-businesses-2026',
        'Bangladesh SEO': '/blog/complete-seo-guide-bangladesh-businesses-2026',
        'Local SEO': '/blog/local-seo-tips-dhaka-businesses-google-maps',
        'Technical SEO': '/blog/technical-seo-checklist-bangladeshi-websites',
        'Keyword Research': '/blog/keyword-research-bangladesh-market',
        'Link Building': '/blog/link-building-bangladesh-strategies',
        'Content Marketing': '/blog/content-marketing-seo-friendly-content-writing',
        'Mobile SEO': '/blog/mobile-seo-bangladesh-ranking-strategy',
        'E-commerce SEO': '/blog/ecommerce-seo-daraz-shopify-guide',
    }
    linked = []
    for tag, url in pillars.items():
        if tag in tags:
            if url.split('/')[-1] in content or url in content:
                linked.append(url)
    if not linked:
        for tag, url in pillars.items():
            if url.split('/')[-1] in content or url in content:
                linked.append(url)
    passed = len(linked) > 0
    topic = next((t for t in tags if t in pillars), 'General')
    return passed, ', '.join(linked) if linked else 'None', topic

def check_aeo_geo(post):
    content = post.get('content', '')
    headings = re.findall(r'^#{1,6}\s+(.+)$', content, re.MULTILINE)
    qw = ['how','what','why','when','where','can','do','is','are','does','did','which','who']
    count = 0
    for h in headings:
        cleaned = re.sub(r'^[\d\s\.\)\]\(\[\-]+', '', h.strip()).strip()
        first = cleaned.lower().split()[0] if cleaned.split() else ''
        if first.strip('?,.:;!-') in qw:
            count += 1
    return count >= 2, count

def check_internal_links(post):
    content = post.get('content', '')
    links = re.findall(r'\[([^\]]+)\]\((/[^)]+)\)', content)
    bare = re.findall(r'(?<=\s)(/blog/[^\s)\]]+|/services/[^\s)\]]+|/locations/[^\s)\]]+)', content)
    all_links = set()
    for text, url in links: all_links.add(url)
    for url in bare: all_links.add(url.rstrip('.,;:!?)'))
    return len(all_links) >= 3, len(all_links), sorted(all_links)

def check_schema(post):
    issues = []
    if not post.get('title'): issues.append('title')
    if not post.get('excerpt'): issues.append('excerpt')
    if not post.get('date'): issues.append('date')
    return len(issues) == 0, issues

# ============================================================
from datetime import datetime, timezone

report = []
passed_total = 0

for slug in MODIFIED_SLUGS:
    post = post_map.get(slug)
    if not post:
        report.append(f"\n## Post: {slug}\n| Check | Status | Details |\n|-------|--------|---------|\n| **⚠️** | **NOT FOUND** | Post slug not in parsed data |\n")
        continue
    
    title = post.get('title', 'Untitled')
    post_ok = True
    
    kw, kw_pass, kw_count = check_tfidf(post)
    kw_st = '✅' if kw_pass else '❌'
    if not kw_pass: post_ok = False
    
    ent_pass, ent_miss, ent_found = check_entities(post)
    ent_st = '✅' if ent_pass else '❌'
    ent_det = 'Missing: ' + ', '.join(ent_miss) if ent_miss else f'Found: {", ".join(ent_found)}'
    if not ent_pass: post_ok = False
    
    pil_pass, pil_links, pil_topic = check_pillar_link(post)
    pil_st = '✅' if pil_pass else '❌'
    pil_det = f'Links to: {pil_links}' if pil_links != 'None' else f'Pillar: {pil_topic} — no link found'
    if not pil_pass: post_ok = False
    
    aeo_pass, aeo_count = check_aeo_geo(post)
    aeo_st = '✅' if aeo_pass else '❌'
    if not aeo_pass: post_ok = False
    
    link_pass, link_count, link_urls = check_internal_links(post)
    link_st = '✅' if link_pass else '❌'
    if not link_pass: post_ok = False
    
    sch_pass, sch_issues = check_schema(post)
    sch_st = '✅' if sch_pass else '❌'
    sch_det = 'All fields set' if sch_pass else 'Missing: ' + ', '.join(sch_issues)
    if not sch_pass: post_ok = False
    
    if post_ok: passed_total += 1
    
    report.append(f"""## Post: {slug}
**Title:** {title}

| Check | Status | Details |
|-------|--------|---------|
| **TF-IDF:** `{kw}` | {kw_st} | {kw_count} occurrences |
| **Entities** | {ent_st} | {ent_det} |
| **Pillar Link** | {pil_st} | {pil_det} |
| **AEO/GEO** | {aeo_st} | {aeo_count} question headings |
| **Internal Links** | {link_st} | {link_count} total |
| **Schema Ready** | {sch_st} | {sch_det} |

""")
    
    fixes = []
    if not kw_pass:
        fixes.append(f"- 🔤 **TF-IDF:** Key phrase `{kw}` appears only {kw_count}x. Add naturally in headings, first paragraph, and key sections to reach 5+ occurrences.")
    if not ent_pass:
        fixes.append(f"- 🏷️ **Entities:** Add missing: {', '.join(ent_miss)}. Include location (Dhaka/Bangladesh), service type, and author mentions for E-E-A-T.")
    if not pil_pass:
        fixes.append(f"- 🔗 **Pillar Link:** No link to pillar page for '{pil_topic}'. Add internal link to `/blog/complete-seo-guide-bangladesh-businesses-2026` (main guide) or appropriate pillar based on tags: {', '.join(post.get('tags', []))}")
    if not aeo_pass:
        fixes.append(f"- ❓ **AEO/GEO:** Only {aeo_count} question heading{'s' if aeo_count !=1 else ''}. Add {2-aeo_count} more H2/H3 headings starting with How/What/Why/Can/Do/Is/Are to capture AI Overview & voice search.")
    if not link_pass:
        fixes.append(f"- 🔗 **Internal Links:** Only {link_count} internal link{'s' if link_count !=1 else ''}. Add {3-link_count} more links to posts, services (`/services/*`), or locations (`/locations/*`).")
    if not sch_pass:
        fixes.append(f"- 📋 **Schema:** Missing: {', '.join(sch_issues)}. All of `title`, `excerpt`, and `date` are required for ArticleSchema.")
    
    if fixes:
        report.append("### Fix instructions:\n" + "\n".join(fixes) + "\n")

now = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
t = len(MODIFIED_SLUGS)
header = f"""=====================================================
📊 CONTENT FRAMEWORK ENFORCEMENT REPORT
=====================================================
🕐  Generated: {now}
📝  Modified posts (48h): {t}
✅  All checks passed: {passed_total}/{t}
❌  Posts needing fixes: {t - passed_total}
=====================================================

"""
report.insert(0, header)
print("".join(report))
