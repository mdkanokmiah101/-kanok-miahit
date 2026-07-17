#!/usr/bin/env python3
"""Run content framework checks on 10 blog posts from data.js (v3)."""
import re
import sys

DATA_FILE = "src/app/blog/data.js"

with open(DATA_FILE, "r", encoding="utf-8") as f:
    data = f.read()

SLUGS = [
    "content-marketing-seo-friendly-content-writing",
    "keyword-research-bangladesh-market",
    "link-building-bangladesh-strategies",
    "ecommerce-seo-daraz-shopify-guide",
    "technical-seo-core-web-vitals-optimization",
    "seo-trends-2026-ai-geo-future",
    "local-seo-dhaka-google-maps-ranking",
    "seo-bangla-beginners-guide-google-ranking",
    "international-seo-bangladesh-exporters-global-buyers",
    "content-marketing-strategy-bangladeshi-brands-seo",
]

def find_post(slug):
    idx = data.find(f'slug: "{slug}"')
    if idx == -1:
        return None
    before = data.rfind('{', 0, idx)
    if before == -1:
        return None
    depth = 0
    in_content = False
    end = before
    for i in range(before, len(data)):
        c = data[i]
        if c == '`' and (i == 0 or data[i-1] != '\\'):
            if not in_content:
                snippet = data[max(0,i-5):i+1]
                if 'content:' in snippet or 'content :' in snippet:
                    in_content = True
            else:
                in_content = False
        if not in_content:
            if c == '{':
                depth += 1
            elif c == '}':
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break
    return data[before:end]

def get_field(raw, field):
    m = re.search(r'\b' + re.escape(field) + r':\s*"([^"]*)"', raw)
    if m:
        return m.group(1)
    m = re.search(r'\b' + re.escape(field) + r':\s*\n\s*"([^"]*)"', raw)
    if m:
        return m.group(1)
    return ""

def get_tags(raw):
    m = re.search(r'\btags:\s*\[(.*?)\]', raw, re.DOTALL)
    if m:
        return re.findall(r'"([^"]*)"', m.group(1))
    return []

def get_content(raw):
    m = re.search(r'content:\s*`(.*)`', raw, re.DOTALL)
    if m:
        return m.group(1)
    return ""

def primary_keyword(title):
    if not title:
        return ""
    if re.match(r'^[a-zA-Z]', title):
        part = re.split(r'[:\u2014]', title)[0].strip()
        stops = {'a','an','the','for','in','of','to','and','or','is','are','was',
                 'were','how','what','why','when','where','which','who','at','by','with','from'}
        words = part.split()
        res = []
        for w in words:
            wc = w.strip('.,;:!?()[]{}""\'\'')
            if wc.lower() in stops and not res:
                continue
            res.append(wc)
            if len(res) >= 2 and len(' '.join(res)) > 5:
                break
            if len(res) >= 3:
                break
        return ' '.join(res) if res else (words[0] if words else title)
    else:
        # Bengali title: strip year prefix, take first content word
        part = re.split(r'[:\u2014]', title)[0].strip()
        # Remove leading year numbers (Bengali and English)
        part = re.sub(r'^[\d\u09E6-\u09EF]+\s*', '', part)
        # Skip known adverbial/prepositional words
        skips = [
            '\u09B8\u09B9\u099C', '\u09B8\u09B9\u099C\u09AD\u09BE\u09AC\u09C7',
            '\u0995\u09C0\u09AD\u09BE\u09AC\u09C7', '\u0995\u09C7\u09A8',
            '\u0995\u09C0', '\u0995\u09BF', '\u09AC\u09BE\u0982\u09B2\u09BE\u09A6\u09C7\u09B6\u09BF',
            '\u09AC\u09BE\u0982\u09B2\u09BE\u09A6\u09C7\u09B6\u09C7\u09B0',
            '\u098F\u0995\u099F\u09BF', '\u099C\u09A8\u09CD\u09AF', '\u098F\u09AC\u0982',
            '\u09AF\u09C1\u0997\u09C7', '\u0986\u09AA\u09A8\u09BE\u09B0', '\u098F\u0987',
            '\u0993', '\u09A4\u09BE', '\u09A5\u09C7\u0995\u09C7', '\u09A6\u09BF\u09AF\u09BC\u09C7',
            '\u0995\u09B0\u09C7', '\u09A8\u09BF\u09AF\u09BC\u09C7', '\u09AC\u09B2\u09C7',
            '\u09B9\u09AF\u09BC\u09C7', '\u09AA\u09B0\u09C7', '\u0986\u0997\u09C7',
            '\u09AE\u09A7\u09CD\u09AF\u09C7', '\u09AD\u09BF\u09A4\u09B0\u09C7',
            '\u09AC\u09BE\u0987\u09B0\u09C7', '\u09B8\u09BE\u09A5\u09C7',
            '\u09B8\u09BE\u09B2\u09C7\u09B0', '\u09AD\u09BE\u09B7\u09BE\u09AF\u09BC',
        ]
        words = part.split()
        # First try to find an English keyword (SEO, GEO, AI, etc.)
        for w in words:
            wc = w.strip('.,;:!?()[]{}""\'\'')
            if re.match(r'^[A-Za-z]', wc) and len(wc) > 1:
                return wc
        # Otherwise find first Bengali content word
        for w in words:
            wc = w.strip('.,;:!?()[]{}""\'\'')
            if len(wc) <= 1:
                continue
            if wc in skips:
                continue
            # Return this word
            return wc
        # Fallback
        return words[0] if words else title

def count_kw(content, kw):
    if not kw:
        return 0
    # Simple substring counting - works for both English and Bengali
    return content.lower().count(kw.lower())

def count_qheadings(content):
    en_pat = r'^#{2,4}\s+(How\s|What\s|Why\s|When\s|Where\s|Can\s|Do\s|Does\s|Is\s|Are\s|Which\s|Who\s)'
    bn_pat = r'^#{2,4}\s+(\u0995\u09C0\u09AD\u09BE\u09AC\u09C7|\u0995\u09C7\u09A8\s|\u0995\u09C0\s|\u0995\u09BF\s|\u0995\u0996\u09A8|\u0995\u09CB\u09A5\u09BE\u09AF\u09BC|\u0995\u09A4\s|\u0995\u09CB\u09A8\s|\u0995\u09C7\s|\u0995\u09BE\u09B0\s)'
    combined = re.compile(f'({en_pat}|{bn_pat})', re.MULTILINE | re.IGNORECASE)
    matches = combined.findall(content)
    faq = re.compile(r'^#{3,4}\s+.*\?\s*$', re.MULTILINE)
    faq_matches = faq.findall(content)
    all_m = set()
    for m in matches:
        if isinstance(m, tuple):
            all_m.add(m[0].strip())
        else:
            all_m.add(str(m).strip())
    for fm in faq_matches:
        all_m.add(fm.strip())
    return len(all_m), list(all_m)[:5]

def run(slug):
    print(f"\n## Post: {slug}")
    raw = find_post(slug)
    if not raw:
        print("| Check | Status | Details |")
        print("|-------|--------|---------|")
        print("| ALL | FAIL | Post not found |")
        print("### Fix instructions: Post slug not found in data.js")
        return

    title = get_field(raw, "title")
    date_val = get_field(raw, "date")
    excerpt = get_field(raw, "excerpt")
    tags = get_tags(raw)
    content = get_content(raw)

    results = {}
    fixes = []

    # A. TF-IDF
    kw = primary_keyword(title)
    cnt = count_kw(content, kw)
    if cnt < 5:
        s = "FLAG"
        fixes.append(f"**A. TF-IDF**: Keyword '{kw}' appears {cnt}x (need >= 5). Add more instances.")
    else:
        s = "PASS"
    results['A. TF-IDF'] = (s, f"Keyword '{kw}' found {cnt} times (need >= 5)")

    # B. Entities
    has_dhaka = bool(re.search(r'\u09A2\u09BE\u0995\u09BE|Dhaka', content))
    has_bd = bool(re.search(r'\u09AC\u09BE\u0982\u09B2\u09BE\u09A6\u09C7\u09B6|Bangladesh', content, re.IGNORECASE))
    has_svc = bool(re.search(r'\bSEO\b|\u09A1\u09BF\u099C\u09BF\u099F\u09BE\u09B2 \u09AE\u09BE\u09B0\u09CD\u0995\u09C7\u099F\u09BF\u0982|digital marketing|SEO Service', content, re.IGNORECASE))
    errors = []
    if not has_dhaka and not has_bd:
        errors.append("Location (Dhaka/Bangladesh)")
    if not has_svc:
        errors.append("Service (SEO/digital marketing)")
    if errors:
        s = "FLAG"
        fixes.append(f"**B. Entities**: Missing: {', '.join(errors)}.")
    else:
        s = "PASS"
    results['B. Entities'] = (s, f"Dhaka={'Y' if has_dhaka else 'N'} BD={'Y' if has_bd else 'N'} Svc={'Y' if has_svc else 'N'}")

    # C. Pillar Link
    expected = set()
    rule_map = {
        'content marketing': 'content-marketing-strategy-bangladeshi-brands-seo',
        'content writing': 'content-marketing-strategy-bangladeshi-brands-seo',
        'seo content': 'content-marketing-strategy-bangladeshi-brands-seo',
        'keyword research': 'complete-seo-guide-bangladesh-businesses-2026',
        'link building': 'complete-seo-guide-bangladesh-businesses-2026',
        'backlinks': 'complete-seo-guide-bangladesh-businesses-2026',
        'ecommerce': 'complete-seo-guide-bangladesh-businesses-2026',
        'technical seo': 'complete-seo-guide-bangladesh-businesses-2026',
        'core web vitals': 'complete-seo-guide-bangladesh-businesses-2026',
        'seo trends': 'complete-seo-guide-bangladesh-businesses-2026',
        'geo': 'complete-seo-guide-bangladesh-businesses-2026',
        'ai seo': 'complete-seo-guide-bangladesh-businesses-2026',
        'local seo': 'complete-seo-guide-bangladesh-businesses-2026',
        'google maps': 'complete-seo-guide-bangladesh-businesses-2026',
        'seo basics': 'complete-seo-guide-bangladesh-businesses-2026',
        'bangla seo': 'complete-seo-guide-bangladesh-businesses-2026',
        'international seo': 'complete-seo-guide-bangladesh-businesses-2026',
        'b2b seo': 'complete-seo-guide-bangladesh-businesses-2026',
        'seo strategy': 'complete-seo-guide-bangladesh-businesses-2026',
        'digital marketing': 'complete-seo-guide-bangladesh-businesses-2026',
        'bangladesh seo': 'complete-seo-guide-bangladesh-businesses-2026',
    }
    for tag in tags:
        tl = tag.lower().strip()
        for k, v in rule_map.items():
            if k in tl or tl in k:
                expected.add(v)
    if not expected:
        expected.add('complete-seo-guide-bangladesh-businesses-2026')

    blog_links = re.findall(r'/blog/([\w-]+)', content)
    matched = []
    for bl in blog_links:
        for ep in expected:
            if bl == ep or ep.startswith(bl) or bl.startswith(ep):
                matched.append(bl)

    if matched:
        s = "PASS"
    else:
        s = "FLAG"
        fixes.append(f"**C. Pillar Link**: No pillar link. Expected: {expected}. Blog links: {blog_links[:5]}. Add link to /blog/complete-seo-guide-bangladesh-businesses-2026")
    results['C. Pillar Link'] = (s, f"Expected: {expected}. Blog links: {blog_links[:5]}. Matched: {matched[:3] if matched else 'None'}")

    # D. AEO/GEO
    qc, qex = count_qheadings(content)
    if qc < 2:
        s = "FLAG"
        fixes.append(f"**D. AEO/GEO**: Only {qc} question-headings (need >= 2).")
    else:
        s = "PASS"
    results['D. AEO/GEO'] = (s, f"{qc} question-headings found (need >= 2). E.g.: {qex[:3]}")

    # E. Internal Links
    bc = len(re.findall(r'/blog/[\w-]+', content))
    sc = len(re.findall(r'/services/[\w]*[/]?', content))
    lc = len(re.findall(r'/locations/[\w]*[/]?', content))
    ic = len(re.findall(r'/industries/[\w]*[/]?', content))
    total = bc + sc + lc + ic
    if total < 3:
        s = "FLAG"
        fixes.append(f"**E. Internal Links**: Total {total} (blog:{bc} svc:{sc} loc:{lc} ind:{ic}) need >= 3.")
    else:
        s = "PASS"
    results['E. Internal Links'] = (s, f"Blog:{bc} Svc:{sc} Loc:{lc} Ind:{ic} Total:{total} (need >= 3)")

    # F. Schema
    ms = []
    if not title: ms.append("title")
    if not excerpt: ms.append("excerpt")
    if not date_val: ms.append("date")
    if ms:
        s = "FLAG"
        fixes.append(f"**F. Schema**: Missing: {', '.join(ms)}.")
    else:
        s = "PASS"
    tpre = title[:60] + '..' if len(title) > 60 else title
    epre = excerpt[:60] + '..' if len(excerpt) > 60 else excerpt
    results['F. Schema'] = (s, f"Title='{tpre}' Date='{date_val}' Excerpt='{epre}'")

    # Output
    print("| Check | Status | Details |")
    print("|-------|--------|---------|")
    for cn, (st, dt) in results.items():
        dt = dt.replace("|", "/").replace("\n", " ")
        print(f"| {cn} | {st} | {dt} |")
    print("### Fix instructions:")
    if fixes:
        for f in fixes:
            print(f"- {f}")
    else:
        print("- All checks passed!")
    print()

for s in SLUGS:
    run(s)
