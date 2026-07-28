#!/usr/bin/env python3
"""
Content Framework Enforcer v3 - Final
"""
import re, sys

with open('src/app/blog/data.js') as f:
    raw = f.read()

posts = []
for m in re.finditer(r'\{[^}]*slug:\s*"([^"]+)"', raw):
    start = m.start()
    while start > 0 and raw[start] != '{': start -= 1
    d, end = 0, -1
    for i in range(start, len(raw)):
        if raw[i] == '{': d += 1
        elif raw[i] == '}':
            d -= 1
            if d == 0: end = i + 1; break
    if end == -1: continue
    obj = raw[start:end]
    slugs = m.group(1)
    posts.append({
        'slug': slugs,
        'title': (re.search(r'title:\s*"([^"]*)"', obj[:2000]) or [None,''])[1],
        'date': (re.search(r'date:\s*"([^"]*)"', obj[:500]) or [None,''])[1],
        'excerpt': (re.search(r'excerpt:\s*"(.*?)"', obj[:3000], re.DOTALL) or [None,''])[1],
        'tags': [t.strip().strip('"') for t in (re.search(r'tags:\s*\[([^\]]*)\]', obj[:3000]) or [None,''])[1].split(',') if t.strip()],
        'content': (re.search(r'content:\s*`([\s\S]*)`\s*,\s*\}', obj) or [None,''])[1]
    })

MODIFIED = [
    "geo-optimization-prepare-business-ai-search",
    "seo-garments-textile-industry-b2b-lead-generation",
    "mobile-seo-optimization-bangladesh-mobile-first-era",
    "seo-healthcare-medical-clinics-bangladesh",
    "why-md-kanok-miah-is-the-best-seo-expert-in-dhaka-bangladesh",
    "locksmith-dundee-seo-case-study",
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

STOPS = {'a','an','the','for','in','of','to','and','or','is','are','was','were',
         'your','our','their','its','at','on','by','with','from','as','be','has',
         'have','had','do','does','did','but','not','up','down','out','off','over',
         'into','through','during','before','after','above','below','between','under',
         'bangladesh','bangladeshi','dhaka','how','what','why','when','where','can',
         'do','does','did','is','are','was','were','will','would','could','should',
         'may','might','which','who','whom','whose','this','that','these','those',
         'best','top','vs','guide','tips','optimize','optimization','all'}

def get_kw(title):
    t = re.sub(r'["\'][^"\']*["\']', '', title)
    parts = re.split(r'[:;\-\u2014|]', t)
    for part in parts:
        words = re.findall(r'[A-Za-z]+', part.strip())
        for w in words:
            if w.lower() not in STOPS and len(w) > 2:
                return w
    words = re.findall(r'[A-Za-z]+', title)
    for w in words:
        if len(w) > 2: return w
    return words[0] if words else 'seo'

PILLAR = {
    'local seo': '/blog/local-seo-tips-dhaka-businesses-google-maps',
    'technical seo': '/blog/technical-seo-checklist-bangladeshi-websites',
    'ecommerce': '/blog/why-ecommerce-store-needs-seo-bangladesh',
    'e-commerce': '/blog/why-ecommerce-store-needs-seo-bangladesh',
    'content marketing': '/blog/content-marketing-strategy-bangladeshi-brands-seo',
    'link building': '/blog/link-building-strategies-bangladesh-market',
    'keyword research': '/blog/keyword-research-bangladesh-market',
    'geo': '/blog/geo-optimization-prepare-business-ai-search',
    'generative engine optimization': '/blog/geo-optimization-prepare-business-ai-search',
    'ai search': '/blog/geo-optimization-prepare-business-ai-search',
    'ai seo': '/blog/geo-optimization-prepare-business-ai-search',
    'geo optimization': '/blog/geo-optimization-prepare-business-ai-search',
    'google ai overview bangladesh': '/blog/geo-optimization-prepare-business-ai-search',
    'mobile seo': '/blog/mobile-seo-optimization-bangladesh-mobile-first-era',
    'mobile': '/blog/mobile-seo-optimization-bangladesh-mobile-first-era',
    'mobile-first indexing': '/blog/mobile-seo-optimization-bangladesh-mobile-first-era',
    'mobile optimization': '/blog/mobile-seo-optimization-bangladesh-mobile-first-era',
    'schema': '/blog/schema-markup-rich-snippets-techniques',
    'structured data': '/blog/schema-markup-rich-snippets-techniques',
    'google business profile': '/blog/google-business-profile-optimization-guide-bangladesh',
    'google my business': '/blog/google-business-profile-optimization-guide-bangladesh',
    'garment': '/blog/seo-garments-textile-industry-b2b-lead-generation',
    'garments seo': '/blog/seo-garments-textile-industry-b2b-lead-generation',
    'textile': '/blog/seo-garments-textile-industry-b2b-lead-generation',
    'textile industry': '/blog/seo-garments-textile-industry-b2b-lead-generation',
    'bangladesh rmg': '/blog/seo-garments-textile-industry-b2b-lead-generation',
    'healthcare': '/blog/seo-healthcare-medical-clinics-bangladesh',
    'healthcare seo': '/blog/seo-healthcare-medical-clinics-bangladesh',
    'medical seo': '/blog/seo-healthcare-medical-clinics-bangladesh',
    'medical': '/blog/seo-healthcare-medical-clinics-bangladesh',
    'patient acquisition': '/blog/seo-healthcare-medical-clinics-bangladesh',
    'real estate': '/blog/seo-real-estate-developers-dhaka',
    'seo services': '/blog/seo-services-cost-bangladesh-pricing-guide',
    'seo services bangladesh': '/blog/seo-services-cost-bangladesh-pricing-guide',
    'seo expert': '/blog/how-to-choose-right-seo-agency-bangladesh',
    'seo agency': '/blog/how-to-choose-right-seo-agency-bangladesh',
    'seo consultant': '/blog/how-to-choose-right-seo-agency-bangladesh',
    'seo expert dhaka': '/blog/how-to-choose-best-seo-expert-dhaka-15-things',
    'seo agency dhaka': '/blog/how-to-choose-best-seo-expert-dhaka-15-things',
    'best seo expert': '/blog/how-to-choose-best-seo-expert-dhaka-15-things',
    'hire seo expert': '/blog/hiring-seo-expert-dhaka-better-roi-than-paid-ads',
    'seo mistakes': '/blog/seo-mistakes-to-avoid-bangladesh',
    'seo tips bangladesh': '/blog/seo-mistakes-to-avoid-bangladesh',
    'seo trends': '/blog/seo-trends-2026-ai-geo-future',
    'seo vs ads': '/blog/seo-vs-google-ads-whats-best-bangladesh-businesses',
    'seo roi': '/blog/seo-vs-google-ads-whats-best-bangladesh-businesses',
    'seo expert guide': None,
    'seo case study': None,
    'organic traffic': None,
    'seo results bangladesh': None,
    'dhaka seo': None,
    'dhaka seo expert': None,
    'digital marketing bangladesh': None,
    'case study': None,
    'smm panel': None,
    'growth strategy': None,
    'construction': None,
    'property safety': None,
    'locksmith': None,
    'transportation': None,
    'automotive': None,
    'seo dublin': None,
}

results = []
all_passed = 0
for slug in MODIFIED:
    p = next((x for x in posts if x['slug'] == slug), None)
    if not p:
        results.append(f"\n## Post: {slug}\n⚠️ **NOT FOUND**\n")
        continue

    c = p['content']
    cl = c.lower()
    tags_lower = [t.lower().strip() for t in p['tags'] if t.strip()]
    
    # A. TF-IDF
    kw = get_kw(p['title'])
    cnt = len(re.findall(r'\b' + re.escape(kw.lower()) + r'\b', cl))
    # For brand names with mixed case
    if cnt == 0 and kw.istitle():
        cnt = len(re.findall(re.escape(kw.lower()), cl))
    
    # B. Entities - simplified check based on tags
    entity_variations = {
        'Bangladesh': ['bangladesh', 'bangladeshi'],
        'Dhaka': ['dhaka'],
        'GEO': ['geo', 'generative engine'],
        'AI Search': ['ai search', 'ai-powered', 'ai-driven'],
        'Local SEO': ['local seo', 'local search', 'google maps'],
        'Technical SEO': ['technical seo', 'site speed'],
        'E-commerce': ['e-commerce', 'ecommerce', 'online store', 'daraz', 'shopify'],
        'B2B': ['b2b', 'business-to-business', 'lead generat'],
        'Link Building': ['link building', 'backlink'],
        'Content Marketing': ['content marketing', 'content strategy'],
        'Mobile SEO': ['mobile seo', 'mobile-first', 'mobile optimization'],
        'Schema': ['schema', 'structured data', 'json-ld'],
        'Google Business Profile': ['google business profile', 'google my business', 'gmb'],
        'SEO Expert/Consultant': ['seo expert', 'seo consultant', 'seo specialist'],
        'SEO Services': ['seo services', 'seo packages'],
        'Healthcare/Medical': ['healthcare', 'medical', 'clinic', 'hospital', 'patient'],
        'Garment/Textile': ['garment', 'textile', 'apparel', 'rmg', 'factory'],
        'Real Estate': ['real estate', 'property', 'apartment', 'developer'],
        'Case Study': ['case study', 'case studies'],
        'Keyword Research': ['keyword research'],
        'B2B SEO': ['b2b seo', 'b2b lead generation'],
        'Mobile-First': ['mobile-first', 'mobile first'],
        'Patient Acquisition': ['patient acquisition'],
        'Kanok Miah': ['kanok miah'],
        'SEO Tips': ['seo tips', 'seo mistakes'],
        'SEO vs Ads': ['seo vs ads', 'seo vs google ads'],
        'SEO ROI': ['seo roi', 'roi'],
        'Digital Marketing': ['digital marketing'],
        'Organic Traffic': ['organic traffic'],
        'SMM Panel': ['smm panel', 'smm panel'],
        'Construction': ['construction', 'cement'],
        'Transportation': ['transportation', 'taxis'],
        'Automotive': ['automotive', 'auto service', 'windshield'],
        'Locksmith': ['locksmith'],
    }
    
    # Determine which entities to check based on tags
    tag_to_entity = {
        'geo': 'GEO', 'ai search': 'AI Search', 'generative engine optimization': 'GEO',
        'local seo': 'Local SEO', 'technical seo': 'Technical SEO',
        'ecommerce': 'E-commerce', 'e-commerce': 'E-commerce',
        'content marketing': 'Content Marketing', 'link building': 'Link Building',
        'keyword research': 'Keyword Research', 'mobile seo': 'Mobile SEO',
        'mobile optimization': 'Mobile SEO', 'mobile-first indexing': 'Mobile-First',
        'schema': 'Schema', 'structured data': 'Schema',
        'google business profile': 'Google Business Profile',
        'google my business': 'Google Business Profile',
        'garment': 'Garment/Textile', 'garments seo': 'Garment/Textile',
        'textile': 'Garment/Textile', 'textile industry': 'Garment/Textile',
        'bangladesh rmg': 'Garment/Textile', 'b2b seo': 'B2B SEO',
        'healthcare seo': 'Healthcare/Medical', 'medical seo': 'Healthcare/Medical',
        'patient acquisition': 'Patient Acquisition',
        'real estate': 'Real Estate', 'seo services': 'SEO Services',
        'seo services bangladesh': 'SEO Services', 'seo expert': 'SEO Expert/Consultant',
        'seo agency': 'SEO Expert/Consultant', 'seo consultant': 'SEO Expert/Consultant',
        'seo expert dhaka': 'SEO Expert/Consultant', 'seo agency dhaka': 'SEO Expert/Consultant',
        'best seo expert': 'SEO Expert/Consultant', 'best seo expert dhaka': 'SEO Expert/Consultant',
        'hire seo expert': 'SEO Expert/Consultant',
        'seo mistakes': 'SEO Tips', 'seo tips bangladesh': 'SEO Tips',
        'seo trends': 'SEO Trends', 'seo vs ads': 'SEO vs Ads',
        'seo roi': 'SEO ROI', 'digital marketing bangladesh': 'Digital Marketing',
        'organic traffic': 'Organic Traffic', 'seo results bangladesh': 'Organic Traffic',
        'case study': 'Case Study', 'seo case study': 'Case Study',
        'smm panel': 'SMM Panel', 'growth strategy': None,
        'construction': 'Construction', 'property safety': None,
        'locksmith': 'Locksmith', 'transportation': 'Transportation',
        'automotive': 'Automotive',
        'ai seo': 'AI Search', 'geo optimization': 'GEO',
        'google ai overview bangladesh': 'AI Search',
        'seo expert guide': 'SEO Expert/Consultant',
        'dhaka seo': None, 'dhaka seo expert': 'SEO Expert/Consultant',
    }
    
    entities_needed = set()
    for tag in tags_lower:
        e = tag_to_entity.get(tag)
        if e:
            entities_needed.add(e)
    
    # Always check if 'Bangladesh' and 'Dhaka' make sense
    if any(v in cl for v in ['bangladesh', 'dhaka']):
        if 'Bangladesh' in str(p['tags']) or 'Bangladesh' in str(entities_needed):
            pass
        if any(v in p['title'].lower() for v in ['bangladesh', 'dhaka', 'local']):
            if 'Bangladesh' not in entities_needed:
                entities_needed.add('Bangladesh')
    
    missing_entities = []
    for entity in entities_needed:
        variations = entity_variations.get(entity, [entity.lower()])
        if not any(v in cl for v in variations):
            missing_entities.append(entity)
    
    # C. Pillar
    pillar_found = []
    for tag in tags_lower:
        pu = PILLAR.get(tag)
        if pu and f'({pu})' in c:
            pillar_found.append(pu)
    if '/blog/complete-seo-guide-bangladesh-businesses-2026' in c:
        pillar_found.append('/blog/complete-seo-guide-bangladesh-businesses-2026')
    pillar_found = list(set(pillar_found))
    
    # D. AEO/GEO
    qs = re.findall(r'^#{2,4}\s+(How|What|Why|When|Where|Can|Do|Is|Are|Does|Did|Will|Would|Should|Could|May|Might)\b', c, re.MULTILINE | re.IGNORECASE)
    qc = len(qs)
    
    # E. Internal Links (fixed regex to count /)
    links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', c)
    blog_l = [u for t,u in links if u.startswith('/blog/') and slug not in u]
    svc_l = [u for t,u in links if u.startswith('/services/')]
    loc_l = [u for t,u in links if u.startswith('/locations/')]
    other_l = [u for t,u in links if u in ['/about', '/contact', '/']]
    # Also check plain parenthesized paths (non-markdown)  
    plain = re.findall(r'\((/(?:[^)\s]+))\)', c)
    for l in plain:
        if l.startswith('/blog/') and slug not in l: blog_l.append(l)
        elif l.startswith('/services/'): svc_l.append(l)
        elif l.startswith('/locations/'): loc_l.append(l)
        elif l in ['/about', '/contact', '/']: other_l.append(l)
    # deduplicate
    blog_l = list(set(blog_l))
    svc_l = list(set(svc_l))
    loc_l = list(set(loc_l))
    other_l = list(set(other_l))
    total_il = len(blog_l) + len(svc_l) + len(loc_l) + len(other_l)
    
    # F. Schema
    schema_m = []
    if not p['title']: schema_m.append('title')
    if not p['excerpt']: schema_m.append('excerpt')
    if not p['date']: schema_m.append('date')
    
    # Build report
    lines = []
    lines.append(f"\n{'='*70}")
    lines.append(f"## Post: {slug}")
    lines.append(f"**Title:** {p['title']}")
    lines.append(f"**Tags:** {', '.join(p['tags'])}")
    lines.append(f"{'='*70}")
    lines.append(f"\n| Check | Status | Details |")
    lines.append(f"|-------|--------|---------|")
    
    tf = "✅" if cnt >= 5 else "❌"
    lines.append(f"| TF-IDF: **{kw}** | {tf} | {cnt} occurrences (need ≥ 5) |")
    
    es = "✅" if not missing_entities else "❌"
    miss_s = ", ".join(missing_entities) if missing_entities else "None"
    lines.append(f"| Entities | {es} | Missing: {miss_s} |")
    
    ps = "✅" if pillar_found else "❌"
    pd = "; ".join(x.replace('/blog/','').replace('-',' ').title()[:50] for x in pillar_found) if pillar_found else "No pillar link found"
    lines.append(f"| Pillar Link | {ps} | {pd} |")
    
    ae = "✅" if qc >= 2 else "❌"
    lines.append(f"| AEO/GEO | {ae} | {qc} question headings (need ≥ 2) |")
    
    ils = "✅" if total_il >= 3 else "❌"
    lines.append(f"| Internal Links | {ils} | {total_il} total (need ≥ 3): {len(blog_l)} blog, {len(svc_l)} svc, {len(loc_l)} loc, {len(other_l)} other |")
    
    scs = "✅" if not schema_m else "❌"
    scd = "All fields set" if not schema_m else f"Missing: {', '.join(schema_m)}"
    lines.append(f"| Schema Ready | {scs} | {scd} |")
    
    # Fixes
    lines.append(f"\n### Fix instructions:")
    fixes = []
    if cnt < 5:
        fixes.append(f"- 🔴 **TF-IDF**: Primary keyword '{kw}' only {cnt}x. Add more natural occurrences to reach ≥5.")
    if missing_entities:
        fixes.append(f"- 🔴 **Entities**: Missing: {miss_s}. Add these entities naturally in the content.")
    if not pillar_found:
        fixes.append(f"- 🔴 **Pillar Link**: No pillar page link. Add a contextual link based on your tags.")
    if qc < 2:
        fixes.append(f"- 🔴 **AEO/GEO**: Only {qc} question headings. Add ≥2 How/What/Why/... headings for AI answer optimization.")
    if total_il < 3:
        fixes.append(f"- 🔴 **Internal Links**: Only {total_il} links. Add more links to posts (/blog/), services (/services/), or locations (/locations/).")
    if schema_m:
        fixes.append(f"- 🔴 **Schema**: Missing: {', '.join(schema_m)}. Set these for ArticleSchema.")
    
    if not fixes:
        fixes.append("- ✅ All checks passed!")
        all_passed += 1
    
    for fix in fixes:
        lines.append(f"  {fix}")
    
    results.append('\n'.join(lines))

# Summary
print(f"\n{'='*60}")
print(f"CONTENT FRAMEWORK ENFORCEMENT REPORT")
print(f"{'='*60}")
print(f"Generated: Automated cron check - {len(MODIFIED)} posts modified in last 48h")
print(f"All checks passed: {all_passed}/{len(MODIFIED)}")
print(f"Needs attention: {len(MODIFIED)-all_passed}/{len(MODIFIED)}")
print(f"{'='*60}")

for r in results:
    print(r)
