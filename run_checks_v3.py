#!/usr/bin/env python3
"""
Comprehensive Content Framework Checks for 40 modified blog posts.
Checks: TF-IDF keyword density, entity coverage, pillar-cluster alignment,
        AEO/GEO question headings, internal linking count, schema readiness.
"""
import re, sys

# ============================================================
# PARSER
# ============================================================
def parse_posts(filepath):
    """Parse all post objects from JS data file, handling backtick template literals."""
    with open(filepath, 'r') as f:
        source = f.read()
    
    posts = []
    i = 0
    in_dq = False   # double-quoted string
    in_bt = False   # backtick template literal
    depth = 0
    start = 0
    
    while i < len(source):
        c = source[i]
        if c == '"' and not in_bt and (i == 0 or source[i-1] != '\\'):
            in_dq = not in_dq
        elif c == '`' and not in_dq and (i == 0 or source[i-1] != '\\'):
            in_bt = not in_bt
        elif not in_dq and not in_bt:
            if c == '{':
                if depth == 0:
                    start = i
                depth += 1
            elif c == '}':
                depth -= 1
                if depth == 0 and start > 0:
                    block = source[start:i+1]
                    if '"slug"' in block.replace("'", '"') or 'slug:' in block:
                        posts.append(block)
                    start = 0
        i += 1
    return posts

def get_str(post, field):
    """Extract a string field from a post block."""
    m = re.search(rf'{field}\s*:\s*"((?:[^"\\]|\\.)*)"', post)
    if m: return m.group(1)
    m = re.search(rf'{field}\s*:\s*\n\s*"((?:[^"\\]|\\.)*)"', post)
    if m: return m.group(1)
    return ""

def get_tags(post):
    m = re.search(r'tags\s*:\s*\[(.*?)\]', post, re.DOTALL)
    if m: return re.findall(r'"([^"]*)"', m.group(1))
    return []

def get_content(post):
    m = re.search(r'content\s*:\s*`', post)
    if not m: return ""
    start = m.end()
    end = post.find('`', start)
    if end == -1: return post[start:]
    return post[start:end]

# ============================================================
# CHECKS
# ============================================================

def get_keyword_and_alt(title, slug):
    """Intelligent primary keyword extraction. Returns (keyword, alt_keywords_to_check).
    alt_keywords is a list of alternative keywords to also check for TF-IDF.
    """
    if not title: return "", []
    t = title.lower()
    
    # For Bengali titles, use the slug or English portion
    bengali_posts = {
        'seo-breadcrumb-schema-bd': ('breadcrumb schema', ['breadcrumb', 'স্কিমা']),
        'seo-howto-schema-bangladesh': ('HowTo schema', ['howto', 'স্কিমা']),
        'seo-json-ld-schema-bangladesh': ('JSON-LD schema', ['json-ld', 'json ld', 'স্কিমা']),
        'seo-robots-txt-guide-bangladesh': ('robots.txt', ['robots.txt', 'robot']),
        'seo-structured-data-guide-bd': ('structured data', ['structured data', 'schema', 'schema markup']),
        'seo-xml-sitemap-guide-bd': ('XML sitemap', ['xml', 'sitemap']),
        'seo-faq-schema-bangladesh': ('faq schema', ['faq', 'স্কিমা']),
        'seo-hreflang-guide-bangladesh': ('hreflang', ['hreflang', 'hreflang ট্যাগ']),
    }
    if slug in bengali_posts:
        kw, alt_list = bengali_posts[slug]
        return kw, alt_list
    
    # Specific known patterns
    kw_map = {
        'best seo expert in dhaka': ('SEO expert', ['seo expert', 'md kanok miah']),
        'geo optimization': ('GEO optimization', ['geo', 'generative engine']),
        'google business profile': ('Google Business Profile', ['google business profile', 'gbp']),
        'faq schema': ('FAQ schema', ['faq']),
        'howto schema': ('HowTo schema', ['howto']),
        'breadcrumb schema': ('breadcrumb schema', ['breadcrumb']),
        'json-ld schema': ('JSON-LD schema', ['json-ld', 'json ld']),
        'structured data': ('structured data', ['structured data', 'schema markup', 'schema']),
        'hreflang': ('hreflang', ['hreflang']),
        'xml sitemap': ('XML sitemap', ['xml sitemap', 'sitemap']),
        'robots.txt': ('robots.txt', ['robots.txt', 'robot']),
        'link building': ('link building', ['link building', 'backlink']),
        'backlink outreach': ('backlink outreach', ['backlink outreach', 'backlink']),
        'technical seo': ('technical SEO', ['technical seo', 'technical']),
        'mobile seo': ('mobile SEO', ['mobile seo', 'mobile']),
        'enterprise seo': ('enterprise SEO', ['enterprise']),
        'blogging strategy': ('blogging strategy', ['blogging', 'blog']),
        'seo roadmap': ('SEO roadmap', ['seo roadmap', 'roadmap']),
        'complete seo guide': ('SEO guide', ['seo', 'optimization']),
        'ecommerce': ('e-commerce SEO', ['e-commerce', 'ecommerce', 'online store']),
        'e-commerce': ('e-commerce SEO', ['e-commerce', 'ecommerce', 'online store']),
        'seo vs google ads': ('SEO vs Google Ads', ['google ads', 'seo vs google']),
        'seo vs ppc': ('SEO vs PPC', ['ppc', 'seo vs ppc']),
        'choose right seo agency': ('SEO agency', ['seo agency', 'seo company']),
        'garments': ('garments', ['garments', 'textile', 'rmg']),
        'textile': ('textile', ['garments', 'textile', 'rmg']),
        'event management': ('event SEO', ['event management', 'event']),
        'non-profit': ('non-profit SEO', ['non-profit', 'nonprofit', 'ngo']),
        'photographers': ('photographer SEO', ['photographer', 'photography', 'videographer']),
        'videographers': ('photographer SEO', ['photographer', 'photography', 'videographer']),
        'wedding': ('wedding SEO', ['wedding', 'event planner']),
        'real estate': ('real estate SEO', ['real estate', 'property']),
        'multiple business locations': ('local SEO', ['local seo', 'multi-location', 'multiple location']),
        'why md kanok miah is the best': ('SEO expert Dhaka', ['md kanok miah', 'seo expert', 'kanok']),
    }
    for pattern, (kw, alts) in kw_map.items():
        if pattern in t:
            return kw, alts
    
    # Case studies - use business/service name as keyword
    if 'case study' in t or 'case-study' in slug:
        cs_kw_map = {
            'das taxis': ('Das Taxis', ['das', 'taxis', 'scotland']),
            'locksmith': ('locksmith', ['locksmith', 'dundee']),
            'landlord': ('landlord certificates', ['landlord', 'gas safety', 'eicr']),
            'morethanpanel': ('social media panel SEO', ['morethanpanel', 'smm', 'panel', 'social media']),
            'smmgen': ('SMMGen SEO', ['smmgen', 'social media', 'smm']),
            'smmsun': ('SMMSun SEO', ['smmsun', 'social media', 'smm']),
            'mir cement': ('Mir Cement SEO', ['mir cement', 'cement']),
            'dhaka apparels': ('Dhaka Apparels SEO', ['apparels', 'dhaka apparels']),
            'stealth windshield': ('windshield repair', ['windshield', 'auto glass']),
        }
        for pattern, (kw, alts) in cs_kw_map.items():
            if pattern in t or pattern in slug:
                return kw, alts
        return 'case study', ['seo', 'case study']
    
    # Generic: first 1-2 significant words (English only)
    import unicodedata
    def is_latin(ch):
        try:
            return unicodedata.category(ch).startswith('L') and ord(ch) < 0x4E00
        except:
            return False
    
    stop = {'a','an','the','for','in','of','to','and','or','is','are',
            'your','our','their','its','it','this','that','at','by',
            'with','from','on','as','be','has','have','do','does',
            'complete','ultimate','essential','guide','tips','strategies',
            'checklist','how','what','why','when','where','which','who',
            'best','top','vs','needs','businesses','business','should',
            'you','need','can','will','all','more','2026','2025','2024'}
    words = t.split()
    sig = [w.strip('(),-:;.') for w in words if w not in stop and len(w)>2 
           and all(is_latin(c) for c in w)]
    if sig:
        return ' '.join(sig[:2]), [w for w in sig[:3]]
    return t.strip(), [t.strip()]

def check_tfidf(content, kw):
    if not kw or not content: return 0
    c = content.lower()
    k = kw.lower()
    if ' ' in k:
        return c.count(k)
    else:
        return len(re.findall(r'\b' + re.escape(k) + r'\b', c))

def check_entities(content, slug):
    c = content.lower()
    missing = []
    
    # Location
    has_dhaka = 'dhaka' in c
    has_bd = 'bangladesh' in c
    has_scot = 'scotland' in c
    has_dundee = 'dundee' in c
    
    cs = 'case-study' in slug
    if cs:
        if 'scotland' in slug or 'dundee' in slug:
            if not has_scot and not has_dundee: missing.append("Location (Scotland/Dundee)")
        elif 'dhaka' in slug:
            if not has_dhaka: missing.append("Location (Dhaka)")
        else:
            if not has_dhaka and not has_bd: missing.append("Location (Dhaka/Bangladesh)")
    else:
        if not has_dhaka and not has_bd: missing.append("Location (Dhaka/Bangladesh)")
    
    # Service topic
    svc_map = {
        'local-seo-tips': 'local seo',
        'local-seo-multiple': 'local seo',
        'google-business-profile': 'google business profile',
        'seo-garments-textile': 'garments',
        'seo-event-management': 'event seo',
        'seo-non-profit': 'non-profit',
        'seo-photographers': 'photographer',
        'seo-wedding-event': 'wedding',
        'seo-real-estate': 'real estate',
        'seo-vs-google-ads': 'google ads',
        'seo-vs-ppc': 'ppc',
        'technical-seo': 'technical seo',
        'mobile-seo': 'mobile seo',
        'link-building': 'link building',
        'backlink-outreach': 'backlink',
        'building-seo-roadmap': 'seo roadmap',
        'blogging-strategy': 'blogging',
        'complete-seo-guide': 'seo',
        'enterprise-seo': 'enterprise seo',
        'geo-optimization': 'geo',
        'how-to-choose-right-seo-agency': 'seo agency',
        'why-ecommerce-store-needs-seo': 'e-commerce',
        'why-md-kanok-miah-is-the-best': 'seo expert',
        'seo-breadcrumb-schema': 'breadcrumb',
        'seo-faq-schema': 'faq schema',
        'seo-howto-schema': 'howto schema',
        'seo-hreflang-guide': 'hreflang',
        'seo-json-ld-schema': 'json-ld',
        'seo-robots-txt-guide': 'robots.txt',
        'seo-structured-data-guide': 'structured data',
        'seo-xml-sitemap-guide': 'xml sitemap',
        'locksmith-dundee-seo': 'locksmith',
        'das-taxis-scotland-seo': 'taxi',
        'landlord-certificates-seo': 'landlord',
        'morethanpanel-seo': 'panel beater',
        'smmgen-seo': 'social media',
        'smmsun-seo': 'social media',
        'mir-cement-seo': 'cement',
        'dhaka-apparels-seo': 'apparel',
        'stealth-windshield-repairs-seo': 'windshield',
        'morethanpanel-seo': 'morethanpanel',
        'smmgen-seo': 'smmgen',
        'smmsun-seo': 'smmsun',
    }
    for key, svc in svc_map.items():
        if slug.startswith(key) or slug == key:
            if svc not in c:
                missing.append(f"Service topic ({svc})")
            break
    
    # Industry
    ind_map = {
        'seo-garments-textile': ['garment','textile','apparel','rmg'],
        'seo-real-estate': ['real estate','property','developer','builder'],
        'seo-event-management': ['event'],
        'seo-wedding-event': ['wedding'],
        'seo-non-profit': ['non-profit','ngo','charity'],
        'seo-photographers': ['photographer','photography','videographer'],
        'dhaka-apparels-seo': ['apparels', 'garment', 'clothing'],
        'mir-cement-seo': ['cement'],
        'locksmith-dundee-seo': ['locksmith'],
        'das-taxis-scotland-seo': ['taxi', 'cab'],
        'landlord-certificates-seo': ['landlord', 'gas safety', 'eicr'],
        'stealth-windshield-repairs-seo': ['windshield', 'auto glass'],
        'morethanpanel-seo': ['morethanpanel', 'smm', 'social media'],
        'smmgen-seo': ['smmgen', 'social media'],
        'smmsun-seo': ['smmsun', 'social media'],
    }
    for key, terms in ind_map.items():
        if slug.startswith(key) or slug == key:
            if not any(t in c for t in terms):
                missing.append(f"Industry terms ({', '.join(terms[:3])})")
            break
    
    return missing

def check_pillar_link(content, slug):
    links = re.findall(r'\[([^\]]*)\]\(([^)]*)\)', content)
    
    pillar_map = {
        'seo-garments-textile': ['/industries/','/blog/seo-garments'],
        'seo-event-management': ['/industries/event','/blog/seo-event'],
        'seo-real-estate': ['/industries/real-estate'],
        'seo-photographers': ['/industries/'],
        'seo-wedding-event': ['/industries/'],
        'seo-non-profit': ['/industries/'],
        'seo-breadcrumb-schema': ['/blog/schema-markup','/blog/seo-structured-data'],
        'seo-howto-schema': ['/blog/schema-markup','/blog/seo-structured-data'],
        'seo-faq-schema': ['/blog/schema-markup','/blog/seo-structured-data'],
        'seo-json-ld-schema': ['/blog/schema-markup','/blog/seo-structured-data'],
        'seo-structured-data-guide': ['/blog/schema-markup','/blog/seo-json-ld'],
        'seo-hreflang-guide': ['/blog/international-seo'],
        'seo-robots-txt-guide': ['/services/technical-seo','/blog/technical-seo'],
        'seo-xml-sitemap-guide': ['/services/technical-seo','/blog/technical-seo'],
        'local-seo': ['/services/local-seo','/locations/'],
        'technical-seo': ['/services/technical-seo'],
        'mobile-seo': ['/services/technical-seo'],
        'why-ecommerce-store-needs-seo': ['/industries/ecommerce'],
        'geo-optimization': ['/services/'],
        'how-to-choose-right-seo-agency': ['/services/'],
        'link-building': ['/services/link-building'],
        'backlink-outreach': ['/services/link-building'],
        'google-business-profile': ['/services/local-seo'],
        'seo-vs-google-ads': ['/services/'],
        'seo-vs-ppc': ['/services/'],
        'complete-seo-guide': ['/services/','/industries/'],
        'enterprise-seo': ['/services/'],
        'blogging-strategy': ['/services/'],
        'building-seo-roadmap': ['/services/'],
        'why-md-kanok-miah-is-the-best': ['/about','/'],
        'landlord-certificates-seo': ['/case-studies/'],
        'das-taxis-scotland-seo': ['/case-studies/'],
        'locksmith-dundee-seo': ['/case-studies/'],
        'morethanpanel-seo': ['/case-studies/'],
        'smmgen-seo': ['/case-studies/'],
        'smmsun-seo': ['/case-studies/'],
        'mir-cement-seo': ['/case-studies/'],
        'dhaka-apparels-seo': ['/case-studies/'],
        'stealth-windshield-repairs-seo': ['/case-studies/'],
        'local-seo-multiple': ['/services/local-seo','/locations/'],
        'seo-dashboard-tools': ['/services/'],
    }
    
    expected = []
    for key, exp in pillar_map.items():
        if slug.startswith(key) or slug == key:
            expected = exp
            break
    
    found = []
    for _, href in links:
        for exp in expected:
            if href.startswith(exp) or href.startswith('https://kanokmiah.com.bd' + exp):
                found.append(href)
                break
    return found, expected

def check_aeo(content):
    headings = re.findall(r'^#{2,3}\s+(.+)$', content, re.MULTILINE)
    qw = ['how','what','why','when','where','can','do','is','are','does','will','should']
    qh = []
    for h in headings:
        s = h.strip().lower()
        for q in qw:
            if s.startswith(q):
                qh.append(h.strip())
                break
    return qh

def check_internal_links(content):
    links = re.findall(r'\[([^\]]*)\]\(([^)]*)\)', content)
    internals = set()
    for _, href in links:
        href = href.strip()
        if href.startswith('/') and len(href) > 1:
            internals.add(href)
        elif 'kanokmiah.com.bd' in href.lower():
            parts = href.split('/')
            if len(parts) >= 4:
                internals.add('/' + '/'.join(parts[3:]))
            else:
                internals.add('/')
    return len(internals), sorted(internals)[:15]

# ============================================================
# MAIN
# ============================================================
filepath = '/root/kanok-miahit/src/app/blog/data.js'
raw_posts = parse_posts(filepath)

modified = [
    "backlink-outreach-templates-strategies-bangladesh",
    "blogging-strategy-seo-frequency-topics-bangladesh",
    "building-seo-roadmap-bangladesh-business",
    "complete-seo-guide-bangladesh-businesses-2026",
    "das-taxis-scotland-seo-case-study",
    "dhaka-apparels-seo-case-study",
    "enterprise-seo-large-organizations-bangladesh",
    "geo-optimization-prepare-business-ai-search",
    "google-business-profile-optimization-guide-bangladesh",
    "how-to-choose-right-seo-agency-bangladesh",
    "landlord-certificates-seo-case-study",
    "link-building-strategies-bangladesh-market",
    "local-seo-multiple-business-locations-bangladesh",
    "local-seo-tips-dhaka-businesses-google-maps",
    "locksmith-dundee-seo-case-study",
    "mir-cement-seo-case-study",
    "mobile-seo-optimization-bangladesh-mobile-first-era",
    "morethanpanel-seo-case-study",
    "seo-breadcrumb-schema-bd",
    "seo-event-management-companies-bangladesh",
    "seo-faq-schema-bangladesh",
    "seo-garments-textile-industry-b2b-lead-generation",
    "seo-howto-schema-bangladesh",
    "seo-hreflang-guide-bangladesh",
    "seo-json-ld-schema-bangladesh",
    "seo-non-profit-organizations-bangladesh",
    "seo-photographers-videographers-bangladesh",
    "seo-real-estate-developers-dhaka",
    "seo-robots-txt-guide-bangladesh",
    "seo-structured-data-guide-bd",
    "seo-vs-google-ads-whats-best-bangladesh-businesses",
    "seo-vs-ppc-advertising-bangladesh",
    "seo-wedding-event-planners-bangladesh",
    "seo-xml-sitemap-guide-bd",
    "smmgen-seo-case-study",
    "smmsun-seo-case-study",
    "stealth-windshield-repairs-seo-case-study",
    "technical-seo-checklist-bangladeshi-websites",
    "why-ecommerce-store-needs-seo-bangladesh",
    "why-md-kanok-miah-is-the-best-seo-expert-in-dhaka-bangladesh"
]

# Build lookup
posts = {}
for rp in raw_posts:
    s = get_str(rp, 'slug')
    if s in modified:
        posts[s] = {
            'title': get_str(rp, 'title'),
            'date': get_str(rp, 'date'),
            'author': get_str(rp, 'author'),
            'excerpt': get_str(rp, 'excerpt'),
            'tags': get_tags(rp),
            'content': get_content(rp)
        }

print(f"Found {len(posts)} of 40 modified posts\n")

results = {}
for slug in modified:
    if slug not in posts:
        continue
    p = posts[slug]
    c = p['content']
    t = p['title']
    
    kw, alt_kw = get_keyword_and_alt(t, slug)
    # Check primary keyword first, then alternatives
    tfidf_n = check_tfidf(c, kw)
    best_kw = kw
    if tfidf_n < 5 and alt_kw:
        for ak in alt_kw:
            n = check_tfidf(c, ak)
            if n > tfidf_n:
                tfidf_n = n
                best_kw = ak
                if tfidf_n >= 5:
                    break
    kw = best_kw
    tf_pass = tfidf_n >= 5
    
    ent_missing = check_entities(c, slug)
    ent_pass = len(ent_missing) == 0
    
    pil_found, pil_exp = check_pillar_link(c, slug)
    pil_pass = len(pil_found) > 0
    
    qh = check_aeo(c)
    aeo_pass = len(qh) >= 2
    
    il_n, il_ex = check_internal_links(c)
    il_pass = il_n >= 3
    
    sch_missing = []
    if not p['title']: sch_missing.append('title')
    if not p['excerpt']: sch_missing.append('excerpt/description')
    if not p['date']: sch_missing.append('date')
    sch_pass = len(sch_missing) == 0
    
    results[slug] = dict(kw=kw, tfidf_n=tfidf_n, tf_pass=tf_pass,
                         ent_missing=ent_missing, ent_pass=ent_pass,
                         pil_found=pil_found, pil_exp=pil_exp, pil_pass=pil_pass,
                         qh=qh, aeo_pass=aeo_pass,
                         il_n=il_n, il_ex=il_ex, il_pass=il_pass,
                         sch_missing=sch_missing, sch_pass=sch_pass)

# Output
pass_all = 0
fail_all = 0
fc = {'TF-IDF':0,'Entities':0,'Pillar Link':0,'AEO/GEO':0,'Internal Links':0,'Schema Readiness':0}

for slug in modified:
    if slug not in results:
        print(f"❌ Post: {slug} — NOT FOUND\n")
        fail_all += 1
        continue
    
    r = results[slug]
    ok = all([r['tf_pass'], r['ent_pass'], r['pil_pass'], r['aeo_pass'], r['il_pass'], r['sch_pass']])
    
    if ok:
        print(f"✅ Post: {slug} — all checks passed")
        pass_all += 1
    else:
        print(f"\n## Post: {slug}")
        print(f"| Check | Status | Details |")
        print(f"|-------|--------|---------|")
        
        s = "✅" if r['tf_pass'] else "❌"
        print(f"| TF-IDF: '{r['kw']}' | {s} | {r['tfidf_n']} occurrences |")
        if not r['tf_pass']: fc['TF-IDF'] += 1
        
        s = "✅" if r['ent_pass'] else "❌"
        d = "All present" if r['ent_pass'] else f"Missing: {', '.join(r['ent_missing'])}"
        print(f"| Entities | {s} | {d} |")
        if not r['ent_pass']: fc['Entities'] += 1
        
        s = "✅" if r['pil_pass'] else "❌"
        if r['pil_found']:
            d = f"Links to: {', '.join(r['pil_found'][:3])}"
        elif r['pil_exp']:
            d = f"No link to {', '.join(r['pil_exp'])}"
        else:
            d = "No pillar mapped"
        print(f"| Pillar Link | {s} | {d} |")
        if not r['pil_pass']: fc['Pillar Link'] += 1
        
        s = "✅" if r['aeo_pass'] else "❌"
        preview = '; '.join(r['qh'][:3])
        print(f"| AEO/GEO | {s} | {len(r['qh'])} question headings{f' ({preview})' if preview else ''} |")
        if not r['aeo_pass']: fc['AEO/GEO'] += 1
        
        s = "✅" if r['il_pass'] else "❌"
        d = f"{r['il_n']} internal links"
        if r['il_ex']:
            d += f" (e.g. {', '.join(r['il_ex'][:5])})"
        print(f"| Internal Links | {s} | {d} |")
        if not r['il_pass']: fc['Internal Links'] += 1
        
        s = "✅" if r['sch_pass'] else "❌"
        d = "All set" if r['sch_pass'] else f"Missing: {', '.join(r['sch_missing'])}"
        print(f"| Schema Ready | {s} | {d} |")
        if not r['sch_pass']: fc['Schema Readiness'] += 1
        
        print(f"\n### Fix instructions:")
        if not r['tf_pass']:
            print(f"- Increase keyword '{r['kw']}' usage (currently {r['tfidf_n']}, need ≥5)")
        if not r['ent_pass']:
            print(f"- Add missing entities: {', '.join(r['ent_missing'])}")
        if not r['pil_pass']:
            if r['pil_exp']:
                print(f"- Link to pillar: {', '.join(r['pil_exp'])}")
            else:
                print(f"- Link to relevant pillar page")
        if not r['aeo_pass']:
            print(f"- Add ≥2 question headings (currently {len(r['qh'])})")
        if not r['il_pass']:
            print(f"- Add more internal links (currently {r['il_n']}, need ≥3)")
        if not r['sch_pass']:
            print(f"- Fix schema fields: {', '.join(r['sch_missing'])}")
        print()
        
        fail_all += 1

print(f"\n## SUMMARY")
print(f"Total: 40")
print(f"✅ All passed: {pass_all}")
print(f"❌ Some failed: {fail_all}")
print(f"Pass rate: {pass_all/40*100:.1f}%")
print(f"\n### Failures by check:")
for k, v in fc.items():
    print(f"  {k}: {v}")
