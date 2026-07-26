#!/usr/bin/env python3
import re, sys

with open('/root/kanok-miahit/src/app/blog/data.js', 'r', encoding='utf-8') as f:
    FC = f.read()

def get(slug):
    """Extract post content and metadata by slug"""
    idx = FC.find(f'slug: "{slug}"')
    if idx < 0: return None
    o = FC.rfind('{', 0, idx)
    c = FC.find('content: `', idx)
    b = FC.find('`,\n', c + 10)
    pe = FC.find('},', b + 2)
    pt = FC[o:pe + 2]
    cv = FC[c + 10:b]
    tm = re.search(r'title:\s*"([^"]*)"', pt)
    em = re.search(r'excerpt:\s*\n?\s*"([^"]*)"', pt, re.DOTALL)
    dm = re.search(r'date:\s*"([^"]*)"', pt)
    tg = re.search(r'tags:\s*\[([^\]]*)\]', pt, re.DOTALL)
    tr = tg.group(1) if tg else '[]'
    return {
        'title': tm.group(1) if tm else 'N/A',
        'excerpt': em.group(1).strip() if em else 'N/A',
        'date': dm.group(1) if dm else 'N/A',
        'tags': [t.strip().strip('"') for t in tr.split(',')],
        'content': cv,
        'cl': cv.lower()
    }

def analyze(slug, kw_label, kw_pat, inds):
    p = get(slug)
    if not p: return None
    
    kw_c = len(re.findall(kw_pat, p['cl']))
    ep, em = [], []
    
    if re.search(r'Dhaka|ঢাকা', p['content']): ep.append('Dhaka')
    else: em.append('Dhaka')
    if re.search(r'Bangladesh|বাংলাদেশ', p['content']): ep.append('Bangladesh')
    else: em.append('Bangladesh')
    
    svs = [s for s in ['seo services','on-page seo','technical seo','local seo','link building','content marketing','ecommerce seo'] if s in p['cl']]
    if svs: ep.append(f"Service({','.join([s.split()[0].title() for s in svs[:4]])})")
    else: em.append('Service type')
    
    fi = [i for i in inds if i.lower() in p['cl']]
    if fi: ep.append(f"Industry({','.join(fi)})")
    else: em.append('Industry')
    
    eq = re.findall(r'^##+\s+(How\s|What\s|Why\s|When\s|Where\s|Can\s|Do\s|Does\s|Is\s|Are\s)', p['content'], re.MULTILINE | re.IGNORECASE)
    bq = re.findall(r'^##+\s+(কী\s|কেন\s|কীভাবে\s|কিভাবে\s|কখন\s|কোথায়\s)', p['content'], re.MULTILINE)
    qc = len(eq) + len(bq)
    
    il = re.findall(r'\]\((/[^\)"\' ]+)', p['content'])
    ul = list(dict.fromkeys(il))
    ic = len(il)
    
    pl = [pp for pp in ['/blog/complete-seo-guide-bangladesh-businesses-2026','/services','/industries'] if pp in p['content']]
    hp = len(pl) > 0
    sr = p['title'] != 'N/A' and p['excerpt'] != 'N/A' and p['date'] != 'N/A'
    
    return {
        'slug': slug, 'title': p['title'], 'date': p['date'],
        'excerpt': p['excerpt'][:80], 'tags': p['tags'],
        'keyword': kw_label, 'kw_count': kw_c,
        'entities_present': ep, 'entities_missing': em,
        'q_count': qc, 'il_count': ic, 'has_pillar': hp,
        'schema_ready': sr, 'internal_links': ul
    }

print("Running analysis...\n")

results = []

# a) Travel
r = analyze('seo-travel-tourism-bangladesh', 'Travel & Tourism SEO', r'travel.*?seo|touris.*?seo', ['travel','tourism','hospitality'])
results.append(r)
print(f"  [a] Travel: kw={r['kw_count']}, q={r['q_count']}, il={r['il_count']}")

# b) Google Penalties
r = analyze('recovering-google-penalties-bangladesh-guide', 'Google Penalties', r'google penalt(y|ies)|manual action', [])
results.append(r)
print(f"  [b] Penalties: kw={r['kw_count']}, q={r['q_count']}, il={r['il_count']}")

# c) Mobile SEO
r = analyze('mobile-seo-optimization-bangladesh-mobile-first-era', 'Mobile SEO', r'mobile seo', [])
results.append(r)
print(f"  [c] Mobile: kw={r['kw_count']}, q={r['q_count']}, il={r['il_count']}")

# d) Local SEO Dhaka
r = analyze('local-seo-dhaka-google-maps-ranking', 'Local SEO', r'স্থানীয় seo|স্থানীয় এসইও|লোকাল seo', [])
# Add Bengali industry mentions
p = get('local-seo-dhaka-google-maps-ranking')
bn_inds = []
if any(t in p['content'] for t in ['রেস্টুরেন্ট','রেস্তোরাঁ']): bn_inds.append('Restaurant')
if any(t in p['content'] for t in ['স্যালন','বিউটি']): bn_inds.append('Salon/Beauty')
if 'ডেন্টিস্ট' in p['content']: bn_inds.append('Dental')
if bn_inds:
    r['entities_present'].append(f"Industry({','.join(bn_inds)})")
    r['entities_missing'] = [m for m in r['entities_missing'] if m != 'Industry']
results.append(r)
print(f"  [d] Local SEO: kw={r['kw_count']}, q={r['q_count']}, il={r['il_count']}")

# e) SEO Career
r = analyze('seo-career-guide-bangladesh-2026', 'SEO Career', r'seo ক্যারিয়ার|seo ক্যারিয়ার', [])
p = get('seo-career-guide-bangladesh-2026')
bn_inds = []
if 'ই-কমার্স' in p['content']: bn_inds.append('E-commerce')
if 'রিয়েল এস্টেট' in p['content']: bn_inds.append('Real Estate')
if 'স্বাস্থ্যসেবা' in p['content']: bn_inds.append('Healthcare')
if 'শিক্ষা' in p['content']: bn_inds.append('Education')
if bn_inds:
    r['entities_present'].append(f"Industry({','.join(bn_inds)})")
    r['entities_missing'] = [m for m in r['entities_missing'] if m != 'Industry']
results.append(r)
print(f"  [e] Career: kw={r['kw_count']}, q={r['q_count']}, il={r['il_count']}")

# f) Affiliate SEO
r = analyze('affiliate-seo-bangladesh', 'Affiliate SEO', r'affiliate seo', ['affiliate','e-commerce'])
results.append(r)
print(f"  [f] Affiliate: kw={r['kw_count']}, q={r['q_count']}, il={r['il_count']}")

print(f"\nTotal results: {len(results)}\n")

# Print final report
print("=" * 90)
print("FINAL REPORT - All 6 posts analyzed")
print("=" * 90)

for r in results:
    print(f"\n--- [{r['slug']}] ---")
    print(f"Title: {r['title']}")
    print(f"Date: {r['date']}")
    print(f"Tags: {r['tags']}")
    print(f"Keyword: '{r['keyword']}' | Occurrences: {r['kw_count']}")
    print(f"Entities Present: {'; '.join(r['entities_present'])}")
    print(f"Entities Missing: {'; '.join(r['entities_missing']) if r['entities_missing'] else 'None'}")
    print(f"Question Headings: {r['q_count']}")
    print(f"Internal Links: {r['il_count']}")
    print(f"Has Pillar Link: {r['has_pillar']}")
    print(f"Schema Ready: {r['schema_ready']}")
    print(f"Internal Links List: {r['internal_links']}")

print("\n\n=== MACHINE-PARSABLE (pipe-separated) ===")
print("slug|keyword|keyword_count|entities_present|entities_missing|question_headings|internal_links|has_pillar|schema_ready|list_of_internal_links")
for r in results:
    ep = ';'.join(r['entities_present'])
    em = ';'.join(r['entities_missing']) if r['entities_missing'] else '-'
    ils = ';'.join(r['internal_links'])
    print(f"{r['slug']}|{r['keyword']}|{r['kw_count']}|{ep}|{em}|{r['q_count']}|{r['il_count']}|{r['has_pillar']}|{r['schema_ready']}|{ils}")
