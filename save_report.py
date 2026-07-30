#!/usr/bin/env python3
"""Generate the structured JSON report file."""
import re
import json

with open('/root/kanok-miahit/src/app/blog/data.js', 'r', encoding='utf-8') as f:
    content = f.read()

# All 18 modified slugs
slugs = [
    "mobile-seo-optimization-bangladesh-mobile-first-era",
    "schema-markup-rich-snippets-techniques",
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

slug_to_change = {
    "mobile-seo-optimization-bangladesh-mobile-first-era": "Added metaTitle, metaDescription, dateModified",
    "schema-markup-rich-snippets-techniques": "Code block formatting fix (Bengali JSON-LD fencing)",
    "why-md-kanok-miah-is-the-best-seo-expert-in-dhaka-bangladesh": "URL conversion (external→internal)",
    "landlord-certificates-seo-case-study": "URL conversion (external→internal)",
    "das-taxis-scotland-seo-case-study": "URL conversion (external→internal)",
    "morethanpanel-seo-case-study": "URL conversion (external→internal)",
    "smmgen-seo-case-study": "URL conversion (external→internal)",
    "smmsun-seo-case-study": "URL conversion (external→internal)",
    "mir-cement-seo-case-study": "URL conversion (external→internal)",
    "dhaka-apparels-seo-case-study": "URL conversion (external→internal)",
    "stealth-windshield-repairs-seo-case-study": "URL conversion (external→internal)",
    "how-to-choose-best-seo-expert-dhaka-15-things": "Major: added metaTitle/metaDescription/dateModified + URL conversions + internal links",
    "seo-expert-vs-seo-agency-dhaka-which-is-right": "URL conversion (external→internal)",
    "top-10-seo-mistakes-dhaka-businesses-fix": "URL conversion (external→internal)",
    "what-does-seo-expert-do-guide-business-owners": "URL conversion (external→internal)",
    "seo-case-study-dhaka-businesses-increased-organic-traffic": "URL conversion (external→internal)",
    "hiring-seo-expert-dhaka-better-roi-than-paid-ads": "URL conversion (external→internal)",
    "ai-seo-2026-dhaka-experts-optimize-google-ai-chatgpt": "URL conversion (external→internal)",
}

def extract_post(text, slug):
    pattern = r'{\s*\n\s+slug:\s*"' + re.escape(slug) + r'"'
    match = re.search(pattern, text)
    if not match:
        return None
    start = match.start()
    content_marker = text.find('content: `', start)
    if content_marker == -1:
        return None
    meta_section = text[start:content_marker]
    
    result = {}
    m = re.search(r'slug:\s*"([^"]+)"', meta_section)
    if m: result['slug'] = m.group(1)
    m = re.search(r'title:\s*"([^"]+)"', meta_section)
    if m: result['title'] = m.group(1)
    m = re.search(r'date:\s*"([^"]+)"', meta_section)
    if m: result['date'] = m.group(1)
    m = re.search(r'author:\s*"([^"]+)"', meta_section)
    if m: result['author'] = m.group(1)
    m = re.search(r'excerpt:\s*\n?\s*"([^"]+)"', meta_section)
    if m: result['excerpt'] = m.group(1)
    m = re.search(r'tags:\s*\[([^\]]+)\]', meta_section)
    if m:
        tags = re.findall(r'"([^"]+)"', m.group(1))
        result['tags'] = tags
    m = re.search(r'metaTitle:\s*\n?\s*"([^"]+)"', meta_section)
    if m: result['metaTitle'] = m.group(1)
    m = re.search(r'metaDescription:\s*\n?\s*"([^"]+)"', meta_section)
    if m: result['metaDescription'] = m.group(1)
    m = re.search(r'dateModified:\s*"([^"]+)"', meta_section)
    if m: result['dateModified'] = m.group(1)
    
    cstart = content_marker + len('content: `')
    # Find closing backtick followed by comma or newline
    cend = text.find('`,\n', cstart)
    if cend == -1:
        cend = text.find('`\n', cstart)
    if cend == -1:
        cend = text.find('`,', cstart)
    if cend != -1:
        result['content'] = text[cstart:cend]
    
    return result

def get_keyword(title):
    if not title:
        return ""
    title = re.sub(r'\s*[|—–-]\s*Kanok Miah.*$', '', title).strip()
    title = re.sub(r'\s*[|—–-]\s*.*$', '', title).strip()
    words = title.split()
    skip = {'the', 'a', 'an', 'how', 'what', 'why', 'when', 'where', 'is', 'are', 'do', 'does', 'can'}
    for i, w in enumerate(words):
        if w.lower() not in skip and len(w) > 2:
            return ' '.join(words[i:i+3]).strip(',;:')
    return words[0] if words else ""

def count_keyword(content, kw):
    if not content or not kw:
        return 0
    return len(re.findall(re.escape(kw), content, re.IGNORECASE))

def count_question_headings(content):
    if not content:
        return 0, []
    headings = re.findall(r'^##[^#].*$', content, re.MULTILINE)
    qheads = []
    for h in headings:
        h2 = h.strip('# ')
        if re.match(r'^(How|What|Why|When|Where|Can|Do|Is|Are)\b', h2, re.IGNORECASE):
            qheads.append(h2)
    return len(qheads), qheads

def count_internal_links(content):
    if not content:
        return 0, []
    links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
    internal = [(t, u) for t, u in links if u.startswith('/')]
    return len(internal), internal

def check_entities(content):
    if not content:
        return {}
    cl = content.lower()
    return {
        'dhaka': 'Dhaka' in content,
        'bangladesh': 'Bangladesh' in content,
        'gulshan': 'Gulshan' in content,
        'banani': 'Banani' in content,
        'uttara': 'Uttara' in content,
        'dhanmondi': 'Dhanmondi' in content,
        'mirpur': 'Mirpur' in content,
    }

def check_pillar(content, tags):
    if not content or not tags:
        return False, []
    tl = [t.lower() for t in tags]
    mapping = {
        'seo': ['/services/', '/blog/complete-seo-guide-bangladesh-businesses-2026'],
        'local seo': ['/services/local-seo'],
        'technical seo': ['/services/technical-seo'],
        'ecommerce': ['/services/ecommerce-seo'],
        'b2b': ['/blog/b2b-lead-generation-seo-bangladesh'],
        'garments': ['/industries/garments-textile'],
        'smm': ['/services/ecommerce-seo'],
        'case study': ['/case-studies'],
    }
    targets = set()
    for t in tl:
        for kw, pages in mapping.items():
            if kw in t:
                targets.update(pages)
    found = [p for p in targets if p in content]
    return len(found) > 0, found

results = []
for slug in slugs:
    post = extract_post(content, slug)
    if not post:
        continue
    kw = get_keyword(post.get('title', ''))
    post_content = post.get('content', '')
    qc, qh = count_question_headings(post_content)
    ic, il = count_internal_links(post_content)
    hp, pf = check_pillar(post_content, post.get('tags', []))
    entities = check_entities(post_content)
    
    r = {
        'slug': post.get('slug', slug),
        'title': post.get('title', ''),
        'date': post.get('date', ''),
        'tags': post.get('tags', []),
        'keyword_analyzed': kw,
        'keyword_count_in_content': count_keyword(post_content, kw),
        'question_headings_count': qc,
        'question_headings': qh[:10],
        'internal_links_count': ic,
        'internal_links': [(t, u) for t, u in il[:10]],
        'has_metaTitle': 'metaTitle' in post,
        'has_metaDescription': 'metaDescription' in post,
        'has_dateModified': 'dateModified' in post,
        'dateModified': post.get('dateModified', None),
        'entities': entities,
        'has_pillar_link': hp,
        'pillar_links_found': pf,
        'content_length': len(post_content),
        'git_change_type': slug_to_change.get(slug, "Unknown"),
    }
    results.append(r)

with open('/root/kanok-miahit/post_analysis_report.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False, default=str)

print(f"Report written to /root/kanok-miahit/post_analysis_report.json")
print(f"Posts analyzed: {len(results)}")
print(f"Total file size: {len(json.dumps(results, indent=2, ensure_ascii=False, default=str)):,} chars")
