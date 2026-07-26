#!/usr/bin/env python3
"""Final refined content framework check for Batch 9."""
import re

DATA_FILE = '/root/kanok-miahit/src/app/blog/data.js'

with open(DATA_FILE, 'r', encoding='utf-8') as f:
    content = f.read()

BATCH_9_SLUGS = [
    'seo-structured-data-guide-bd',
    'seo-json-ld-schema-bangladesh', 
    'seo-breadcrumb-schema-bd',
    'seo-faq-schema-bangladesh',
    'seo-howto-schema-bangladesh',
    'seo-for-startups-bangladesh',
    'b2b-lead-generation-seo-bangladesh',
    'seo-for-law-firms-bangladesh',
    'seo-for-fitness-gyms-bangladesh',
    'seo-services-cost-bangladesh-pricing-guide',
    'seo-vs-ppc-advertising-bangladesh',
    'how-to-track-measure-seo-roi-bangladesh',
    'seo-healthcare-medical-clinics-bangladesh',
    'seo-educational-institutions-bangladesh',
    'seo-travel-tourism-bangladesh',
    'seo-event-management-companies-bangladesh',
    'seo-real-estate-agents-property-developers-bangladesh'
]

def extract_post(slug):
    slug_pattern = f'    slug: "{slug}",'
    idx = content.find(slug_pattern)
    if idx == -1:
        return None
    post_start = content.rfind('{', 0, idx)
    if post_start == -1:
        post_start = idx
    content_field_start = content.find('    content: `', post_start)
    if content_field_start == -1:
        return None
    content_start = content_field_start + len('    content: `')
    rest = content[content_start:]
    depth = 1
    i = 0
    while i < len(rest) and depth > 0:
        if rest[i] == '\\' and i + 1 < len(rest):
            i += 2
            continue
        if rest[i] == '`':
            depth -= 1
            if depth == 0:
                break
        i += 1
    post_content = rest[:i]
    header = content[post_start:content_field_start]
    title_match = re.search(r'title:\s*"([^"]*)"', header)
    title = title_match.group(1) if title_match else 'Unknown'
    date_match = re.search(r'date:\s*"([^"]*)"', header)
    date = date_match.group(1) if date_match else 'Unknown'
    excerpt_match = re.search(r'excerpt:\s*\n\s+"([^"]*)"', header)
    if not excerpt_match:
        excerpt_match = re.search(r'excerpt:\s*"([^"]*)"', header)
    excerpt = excerpt_match.group(1) if excerpt_match else ''
    return {'slug': slug, 'title': title, 'date': date, 'content': post_content, 'excerpt': excerpt}

def get_keyword_candidates(title):
    """Generate reasonable primary keyword candidates from a title."""
    t = title.strip()
    t_lower = t.lower()
    candidates = []
    
    # For Bangla titles, use the main title (before colon) or whole title
    if any('\u0980' <= c <= '\u09FF' for c in t):
        main = t.split(':')[0].strip() if ':' in t else t.strip()
        candidates.append(main)
        # Also parts
        if ':' in t:
            after = t.split(':')[1].strip()
            candidates.append(after)
        return candidates
    
    # English titles
    
    # 1. Full title
    candidates.append(t)
    
    # 2. Before colon
    if ':' in t:
        main = t.split(':')[0].strip()
        candidates.append(main)
        after = t.split(':')[1].strip()
        candidates.append(after)
    
    # 3. For "SEO for X in Bangladesh" pattern
    if ' for ' in t_lower:
        parts = t_lower.split(' for ', 1)
        after_for = parts[1]
        # Remove trailing colon part
        after_for = after_for.split(':')[0].strip()
        candidates.append(after_for)
        # Remove ' in Bangladesh' if present
        short = after_for.replace(' in bangladesh', '').replace(' in Bangladesh', '').strip()
        if short != after_for:
            candidates.append(short)
        # Also "seo for X"
        candidates.append(f"seo for {after_for}")
    
    # 4. For "How to X" pattern
    if t_lower.startswith('how to'):
        candidates.append(t)
        rest = t[7:].split(':')[0].strip()
        candidates.append(rest)
    
    # 5. For "X vs Y" pattern
    if ' vs ' in t_lower:
        candidates.append(t)
    
    # 6. For specific known patterns that need custom handling
    # Law firms
    if 'law firm' in t_lower:
        candidates.append('law firms')
        candidates.append('legal services')
    # Fitness/gym
    if 'fitness' in t_lower or 'gym' in t_lower:
        candidates.append('fitness')
        candidates.append('gym')
    # Pricing/cost
    if 'pricing' in t_lower or 'cost' in t_lower:
        candidates.append('seo pricing')
        candidates.append('pricing')
    # Healthcare/medical
    if 'healthcare' in t_lower or 'medical' in t_lower or 'clinic' in t_lower:
        candidates.append('healthcare')
        candidates.append('medical')
        candidates.append('patient')
    # Education
    if 'education' in t_lower or 'student' in t_lower or 'enrollment' in t_lower:
        candidates.append('educational')
        candidates.append('student')
    # Travel/tourism
    if 'travel' in t_lower or 'tourism' in t_lower:
        candidates.append('travel')
        candidates.append('tourism')
    # Event
    if 'event' in t_lower:
        candidates.append('event')
    # Real estate
    if 'real estate' in t_lower or 'property' in t_lower:
        candidates.append('real estate')
        candidates.append('property')
    # B2B
    if 'b2b' in t_lower:
        candidates.append('b2b')
        candidates.append('lead generation')
    # PPC
    if 'ppc' in t_lower:
        candidates.append('ppc')
        candidates.append('seo vs ppc')
    # ROI
    if 'roi' in t_lower:
        candidates.append('seo roi')
        candidates.append('track and measure')
    # Startups/startup
    if 'startup' in t_lower:
        candidates.append('startup')
        candidates.append('startups')
    
    # Deduplicate preserving order
    seen = set()
    result = []
    for c in candidates:
        if c not in seen:
            seen.add(c)
            result.append(c)
    return result

def check_tfidf(post):
    title = post['title']
    body = post['content'].lower()
    candidates = get_keyword_candidates(title)
    
    best_count = 0
    best_kw = ''
    for kw in candidates:
        kw_lower = kw.lower()
        c = body.count(kw_lower)
        if c > best_count:
            best_count = c
            best_kw = kw
    
    # Also try the main SEO topic
    if best_count < 3:
        # Try extracting just the core noun phrase
        for kw in candidates:
            words = kw.split()
            if len(words) > 2:
                for i in range(len(words)):
                    sub = ' '.join(words[i:])
                    if len(sub) > 5:
                        c = body.count(sub.lower())
                        if c > best_count:
                            best_count = c
                            best_kw = sub
    
    return {
        'keyword': best_kw[:80] if best_kw else '(none)',
        'count': best_count,
        'pass': best_count >= 5,
        'flag': best_count < 5
    }

def check_semantic(post):
    body = post['content'].lower()
    found = []
    missing = []
    
    # Dhaka/ঢাকা
    if any(v in body for v in ['dhaka', 'ঢাকা']):
        found.append('Dhaka')
    else:
        missing.append('Dhaka/ঢাকা')
    
    # Bangladesh/বাংলাদেশ
    if any(v in body for v in ['bangladesh', 'বাংলাদেশ']):
        found.append('Bangladesh')
    else:
        missing.append('Bangladesh/বাংলাদেশ')
    
    # Service type
    if any(v in body for v in ['seo service', 'seo সেবা', 'অন-পেজ', 'off-page', 'টেকনিক্যাল', 'local seo', 'link building', 'সার্ভিস', 'service']):
        found.append('Service')
    else:
        missing.append('Service type')
    
    # Industry sector - any industry term
    sectors = ['schema', 'startup', 'b2b', 'manufactur', 'law', 'legal', 'fitness', 'gym', 
               'pricing', 'ppc', 'google ads', 'roi', 'analytics', 'healthcare', 'medical', 
               'clinic', 'education', 'school', 'university', 'travel', 'tourism', 'hotel',
               'event', 'wedding', 'real estate', 'property', 'developer']
    found_sectors = [s for s in sectors if s in body]
    if found_sectors:
        found.append(f'Sector:{found_sectors[0]}')
    else:
        missing.append('Industry sector')
    
    return {'pass': len(missing)==0, 'flag': len(missing)>0, 'found': found, 'missing': missing}

def check_pillar(post):
    body = post['content']
    has_pillar = '/blog/complete-seo-guide-bangladesh-businesses-2026' in body
    has_services = bool(re.search(r'/services/', body))
    details = []
    if has_pillar: details.append('Pillar')
    if has_services: details.append('/services/')
    return {'pass': has_pillar or has_services, 'flag': not (has_pillar or has_services), 'details': details or ['None']}

def check_aeo_geo(post):
    body = post['content']
    count = 0
    headings = []
    en_starters = ['how ', 'what ', 'why ', 'when ', 'where ', 'can ', 'do ', 'is ', 'are ']
    bn_starters = ['কী ', 'কেন ', 'কীভাবে ', 'কিভাবে ', 'কখন ', 'কোথায় ', 'কোন ']
    
    for line in body.split('\n'):
        stripped = line.strip()
        if not stripped.startswith('#'):
            continue
        h = stripped.lstrip('#').strip()
        hl = h.lower()
        
        matched = False
        for s in en_starters:
            if hl.startswith(s):
                count += 1
                headings.append(h[:70])
                matched = True
                break
        if matched:
            continue
        for s in bn_starters:
            if h.startswith(s):
                count += 1
                headings.append(h[:70])
                matched = True
                break
        if not matched:
            # Check if starts with Bengali question word followed by space/tab/:
            for qw in ['কী', 'কেন', 'কীভাবে', 'কিভাবে', 'কখন', 'কোথায়', 'কোন']:
                if h.startswith(qw) and len(h) > len(qw) and h[len(qw)] in ' \t:?':
                    count += 1
                    headings.append(h[:70])
                    break
    
    return {'count': count, 'headings': headings, 'pass': count >= 2, 'flag': count < 2}

def check_internal_links(post):
    body = post['content']
    links = re.findall(r'\[([^\]]*)\]\((/[^)]*)\)', body)
    internal = [(t, u) for t, u in links if any(u.startswith(p) for p in ['/blog/', '/services/', '/locations/', '/industries/'])]
    return {'count': len(internal), 'pass': len(internal) >= 3, 'flag': len(internal) < 3}

def check_schema(post):
    missing = []
    if not post.get('title') or post['title'] == 'Unknown':
        missing.append('title')
    if not post.get('excerpt') or post['excerpt'] == '':
        missing.append('excerpt')
    if not post.get('date') or post['date'] == 'Unknown':
        missing.append('date')
    return {'pass': len(missing)==0, 'flag': len(missing)>0, 'missing': missing}

# Run all
all_results = []
for slug in BATCH_9_SLUGS:
    post = extract_post(slug)
    if not post:
        print(f"ERROR: {slug} not found")
        continue
    
    a = check_tfidf(post)
    b = check_semantic(post)
    c = check_pillar(post)
    d = check_aeo_geo(post)
    e = check_internal_links(post)
    f = check_schema(post)
    
    all_results.append({'slug': slug, 'title': post['title'], 'A': a, 'B': b, 'C': c, 'D': d, 'E': e, 'F': f})
    
    flags = sum(1 for x in [a,b,c,d,e,f] if x['flag'])
    print(f"\n{'='*70}")
    print(f"📄 {slug}")
    print(f"   {post['title']}")
    print(f"   Flags: {flags}/6")
    print(f"  A TF-IDC: {'✅' if not a['flag'] else '❌'} '{a['keyword']}' x{a['count']}")
    print(f"  B Semant: {'✅' if not b['flag'] else '❌'} missing={b['missing']}")
    print(f"  C Pillar: {'✅' if not c['flag'] else '❌'} {c['details']}")
    print(f"  D AEO/GE: {'✅' if not d['flag'] else '❌'} {d['count']} Q-headings")
    print(f"  E IntLnk: {'✅' if not e['flag'] else '❌'} {e['count']} internal links")
    print(f"  F Schema: {'✅' if not f['flag'] else '❌'} missing={f['missing']}")
    if d['flag']:
        print(f"    Headings found: {d['headings']}")

# Summary table
print("\n\n" + "="*140)
print("BATCH 9 — FINAL SUMMARY")
print("="*140)
hdr = f"{'Slug':<52} {'TF-IDF':<8} {'Semantic':<10} {'Pillar':<8} {'AEO/GEO':<9} {'Links':<8} {'Schema':<8} {'Flags':<7}"
print(hdr)
print("-"*140)

total_flags = 0
for r in all_results:
    slug = r['slug'][:49]
    a = '✅' if not r['A']['flag'] else '❌'
    b = '✅' if not r['B']['flag'] else '❌'
    c = '✅' if not r['C']['flag'] else '❌'
    d = '✅' if not r['D']['flag'] else '❌'
    e = '✅' if not r['E']['flag'] else '❌'
    f = '✅' if not r['F']['flag'] else '❌'
    flags = sum(1 for x in ['A','B','C','D','E','F'] if r[x]['flag'])
    total_flags += flags
    print(f"{slug:<52} {a:<8} {b:<10} {c:<8} {d:<9} {e:<8} {f:<8} {flags}/6")

print("="*140)
print(f"\nTotal checks: {len(all_results)*6} | ✅ Passed: {len(all_results)*6 - total_flags} | ❌ Flagged: {total_flags} | Rate: {(len(all_results)*6 - total_flags)/(len(all_results)*6)*100:.1f}%")

print("\nPer-check pass rates:")
for label, key in [('TF-IDF Coverage', 'A'), ('Semantic Entities', 'B'), ('Pillar-Cluster', 'C'),
                    ('AEO/GEO', 'D'), ('Internal Links', 'E'), ('Schema Fields', 'F')]:
    flagged = sum(1 for r in all_results if r[key]['flag'])
    p = len(all_results) - flagged
    print(f"  {label:<20} {p:>2}/{len(all_results)} ({p/len(all_results)*100:>4.0f}%) {'✅' if not flagged else '❌ '+str(flagged)+' flagged'}")

print("\n\nFLAGGED ITEMS:")
for r in all_results:
    flags = [(k, r[k]) for k in ['A','B','C','D','E','F'] if r[k]['flag']]
    if flags:
        names = {'A':'TF-IDF','B':'Semantic','C':'Pillar','D':'AEO/GEO','E':'Links','F':'Schema'}
        print(f"  {r['slug']}: {', '.join(names[k] for k,_ in flags)}")
