#!/usr/bin/env python3
"""FINAL Framework audit for 3 SEO guide posts."""

import re

with open('/root/kanok-miahit/src/app/blog/data.js') as f:
    raw = f.read()

def get_post(slug):
    """Extract a complete post by slug."""
    idx = raw.find('slug: "' + slug + '"')
    if idx < 0: return None
    brace = raw.rfind('{', 0, idx)
    
    # Find closing brace
    d = 0; i = brace
    while i < len(raw):
        if raw[i] == '{': d += 1
        elif raw[i] == '}': 
            d -= 1
            if d == 0: break
        i += 1
    block = raw[brace:i+1]
    
    # Parse fields
    m = re.search(r'title:\s*"([^"]+)"', block)
    title = m.group(1) if m else ''
    m = re.search(r'date:\s*"([^"]+)"', block)
    date_val = m.group(1) if m else ''
    m = re.search(r'excerpt:\s*\n?\s*"([^"]+)"', block)
    excerpt = m.group(1) if m else ''
    tags_m = re.search(r'tags:\s*\[(.*?)\]', block, re.DOTALL)
    tags = re.findall(r'"([^"]+)"', tags_m.group(1)) if tags_m else []
    
    # Content: extract between backticks
    cs = raw.find('content: `', brace)
    # Find the *real* closing backtick+comma
    pos = cs + 10
    while pos < len(raw):
        bt = raw.find('`', pos)
        if bt < 0: break
        if bt+1 < len(raw) and raw[bt+1] == ',':
            # Check it's followed by newline+spaces+} (closing the object)
            after = raw[bt+2:bt+10]
            if re.match(r'\s*\n\s*\}', after):
                content = raw[cs+10:bt]
                # Handle leading newline
                if content.startswith('\n'):
                    content = content[1:]
                return {'slug': slug, 'title': title, 'date': date_val, 
                        'excerpt': excerpt, 'tags': tags, 'content': content}
        pos = bt + 1
    return None


def audit(slug, tfidf_kw):
    p = get_post(slug)
    if not p:
        print(f"\n  ERROR: Could not parse post {slug}")
        return
    
    title = p['title']
    content = p['content']
    tags = p['tags']
    
    print(f"\n{'='*72}")
    print(f"  Post: {slug}")
    print(f"  Title: {title}")
    print(f"  Date: {p['date']}")
    print(f"  Tags: {tags}")
    print(f"  Content: {len(content)} chars")
    print(f"{'='*72}")
    
    flags = []
    
    # A: TF-IDF
    kw_count = len(re.findall(re.escape(tfidf_kw), content, re.IGNORECASE))
    if kw_count < 5:
        flags.append(f"A.TF-IDF ❌: '{tfidf_kw}' appears {kw_count}x (min 5)")
        print(f"  A. TF-IDF ❌: '{tfidf_kw}' appears {kw_count}x")
    else:
        print(f"  A. TF-IDF ✅: '{tfidf_kw}' appears {kw_count}x")
    
    # B: Entities
    entities_check = ['Dhaka', 'Bangladesh', 'SEO expert', 'SEO agency']
    missing_ent = []
    for e in entities_check:
        c = len(re.findall(re.escape(e), content, re.IGNORECASE))
        if c == 0:
            missing_ent.append(e)
    if missing_ent:
        flags.append(f"B.Entities ❌: Missing: {', '.join(missing_ent)}")
        print(f"  B. Entities ❌: Missing: {', '.join(missing_ent)}")
    else:
        print(f"  B. Entities ✅: All present")
    
    # C: Pillar-Cluster
    tag_lower = [t.lower() for t in tags]
    pillar_map = {
        'seo guide': '/services/seo', 'bangladesh seo': '/services/seo',
        'seo services': '/services/seo', 'seo expert': '/services/seo',
        'seo agency': '/services/seo', 'seo mistakes': '/services/seo',
        'seo roi': '/services/seo', 'seo vs ads': '/services/seo',
        'local seo': '/services/local-seo', 'technical seo': '/services/technical-seo',
        'ecommerce seo': '/services/ecommerce-seo', 'content market': '/services/content-marketing',
        'digital market': '/services/digital-marketing',
    }
    pillar = '/services/seo'
    for t in tag_lower:
        for key, val in pillar_map.items():
            if key in t:
                pillar = val
                break
    
    has_pillar = bool(re.search(r'\(' + re.escape(pillar) + r'\)', content))
    if not has_pillar:
        flags.append(f"C.Pillar ❌: No link to pillar page {pillar}")
        print(f"  C. Pillar Link ❌: No link to {pillar}")
    else:
        print(f"  C. Pillar Link ✅: Links to {pillar}")
    
    # D: AEO/GEO
    headings = re.findall(r'^#{2,3}\s+(.+)', content, re.MULTILINE)
    q_count = 0
    for h in headings:
        h_stripped = re.sub(r'^[\d.\)\s]+', '', h)  # strip leading "1. ", "2)" etc
        if re.match(r'(How|What|Why|When|Where|Can|Do|Is|Are)\b', h_stripped, re.IGNORECASE):
            q_count += 1
    if q_count < 2:
        flags.append(f"D.AEO/GEO ❌: {q_count} question headings (min 2)")
        print(f"  D. AEO/GEO ❌: {q_count} question headings")
    else:
        print(f"  D. AEO/GEO ✅: {q_count} question headings")
    
    # E: Internal Links
    blog_l = len(re.findall(r'\(/blog/', content))
    svc_l = len(re.findall(r'\(/services/', content))
    loc_l = len(re.findall(r'\(/locations/', content))
    ind_l = len(re.findall(r'\(/industries/', content))
    total_links = blog_l + svc_l + loc_l + ind_l
    if total_links < 3:
        flags.append(f"E.IntLinks ❌: {total_links} links (min 3)")
        print(f"  E. Internal Links ❌: {total_links} total ({blog_l} blog, {svc_l} services, {loc_l} locations, {ind_l} industries)")
    else:
        print(f"  E. Internal Links ✅: {total_links} total ({blog_l} blog, {svc_l} services, {loc_l} locations, {ind_l} industries)")
    
    # F: Schema
    schema_ok = bool(title) and bool(p['excerpt']) and bool(p['date'])
    if not schema_ok:
        missing_s = []
        if not title: missing_s.append('title')
        if not p['excerpt']: missing_s.append('excerpt')
        if not p['date']: missing_s.append('date')
        flags.append(f"F.Schema ❌: Missing: {', '.join(missing_s)}")
        print(f"  F. Schema ❌: Missing: {', '.join(missing_s)}")
    else:
        print(f"  F. Schema ✅: title ✓, excerpt ✓, date ✓")
    
    # Summary
    print(f"\n  FLAGS: {len(flags)}/6")
    for f in flags:
        print(f"    🔴 {f}")
    if not flags:
        print(f"  ✅ ALL CHECKS PASS")
    
    return {'slug': slug, 'flags': flags, 'total': len(flags)}


# Run audits
print("="*72)
print("  CONTENT FRAMEWORK AUDIT — 3 SEO Guide Posts")
print("="*72)

posts_config = [
    ('seo-expert-vs-seo-agency-dhaka-which-is-right', 'SEO Expert'),
    ('top-10-seo-mistakes-dhaka-businesses-fix', 'SEO Mistakes'),
    ('hiring-seo-expert-dhaka-better-roi-than-paid-ads', 'SEO Expert'),
]

results = []
for slug, kw in posts_config:
    r = audit(slug, kw)
    if r: results.append(r)

# EXECUTIVE SUMMARY
print(f"\n\n{'='*72}")
print("  EXECUTIVE SUMMARY")
print(f"{'='*72}")
print(f"  {'#':<3} {'Slug':<55} {'Flags':<8}  Status")
print(f"  {'─'*3} {'─'*55} {'─'*8}  {'─'*15}")
total = 0
for i, r in enumerate(results, 1):
    n = r['total']
    total += n
    status = "✅ PASS" if n == 0 else f"⚠️ {n}/6"
    print(f"  {i:<3} {r['slug']:<55} ({n})    {status}")
    for f in r['flags']:
        print(f"  {'':>3} {'':>55} {'':>8}  {f}")

print(f"\n  {'─'*72}")
print(f"  TOTAL: {total} flags across 3 posts (out of 18 checks)")
