#!/usr/bin/env python3
"""Generate clean final report from the framework check data."""
import subprocess, re, json, sys, os
os.chdir("/root/kanok-miahit")

# Reuse the post parsing and check functions from _framework_checks.py
# We need the posts variable and check functions
with open("src/app/blog/data.js") as f:
    content = f.read()

parts = content.split('slug: "')
posts = []
for i, part in enumerate(parts[1:], 1):
    slug = part.split('"')[0]
    post_data = part[len(slug) + 1:]
    
    title_m = re.search(r'title:\s*"([^"]+)"', post_data[:2000])
    date_m = re.search(r'date:\s*"([^"]+)"', post_data[:1000])
    excerpt_m = re.search(r'excerpt:\s*\n?\s*"([^"]+)"', post_data[:3000])
    tags_m = re.search(r'tags:\s*\[([^\]]+)\]', post_data[:3000], re.DOTALL)
    metaTitle_m = re.search(r'metaTitle:\s*"([^"]+)"', post_data[:3000])
    metaDesc_m = re.search(r'metaDescription:\s*"([^"]+)"', post_data[:3000])
    dateMod_m = re.search(r'dateModified:\s*"([^"]+)"', post_data[:3000])
    
    content_m = re.search(r'content:\s*`\n(.*?)\n\s*`', post_data, re.DOTALL)
    if not content_m:
        content_m = re.search(r'content:\s*`(.*?)`', post_data, re.DOTALL)
    
    content_text = content_m.group(1) if content_m else ""
    
    tags = []
    if tags_m:
        tag_str = tags_m.group(1)
        tags = re.findall(r'"([^"]+)"', tag_str)
    
    post = {
        'slug': slug,
        'title': title_m.group(1) if title_m else '',
        'date': date_m.group(1) if date_m else '',
        'excerpt': excerpt_m.group(1) if excerpt_m else '',
        'tags': tags,
        'metaTitle': metaTitle_m.group(1) if metaTitle_m else '',
        'metaDescription': metaDesc_m.group(1) if metaDesc_m else '',
        'dateModified': dateMod_m.group(1) if dateMod_m else '',
        'content': content_text,
    }
    posts.append(post)

changed_slugs = [
    'ai-seo-2026-dhaka-experts-optimize-google-ai-chatgpt',
    'das-taxis-scotland-seo-case-study',
    'dhaka-apparels-seo-case-study',
    'google-business-profile-optimization-guide-bangladesh',
    'hiring-seo-expert-dhaka-better-roi-than-paid-ads',
    'how-to-choose-best-seo-expert-dhaka-15-things',
    'landlord-certificates-seo-case-study',
    'link-building-strategies-bangladesh-market',
    'mir-cement-seo-case-study',
    'mobile-seo-optimization-bangladesh-mobile-first-era',
    'morethanpanel-seo-case-study',
    'seo-case-study-dhaka-businesses-increased-organic-traffic',
    'seo-expert-vs-seo-agency-dhaka-which-is-right',
    'seo-garments-textile-industry-b2b-lead-generation',
    'smmgen-seo-case-study',
    'smmsun-seo-case-study',
    'stealth-windshield-repairs-seo-case-study',
    'top-10-seo-mistakes-dhaka-businesses-fix',
    'what-does-seo-expert-do-guide-business-owners',
    'why-md-kanok-miah-is-the-best-seo-expert-in-dhaka-bangladesh',
]

def check_tfidf(post):
    title = post['title']
    clean_title = re.sub(r'\s*[|–-].*$', '', title).strip()
    
    stopwords = {'a', 'an', 'the', 'for', 'of', 'in', 'to', 'and', 'or', 'with', 'is', 'are', 'was', 'were', 'on', 'at', 'by', 'from', 'your', 'our', 'their', 'its', 'how', 'what', 'why', 'when', 'where', 'which', 'who', 'do', 'does', 'did', 'can', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'need', 'has', 'have', 'had', 'not', 'no', 'up', 'out', 'off', 'over', 'under', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'between', 'about', 'than', 'that', 'this', 'these', 'those'}
    
    words = clean_title.split()
    keyword_parts = [w for w in words if w.lower() not in stopwords]
    
    keyword = ''
    count = 0
    
    for n in range(3, 0, -1):
        if len(keyword_parts) >= n:
            kw = ' '.join(keyword_parts[:n])
            cnt = post['content'].lower().count(kw.lower())
            if cnt > count:
                keyword, count = kw, cnt
    
    # Also try slug-based phrases
    slug_parts = post['slug'].replace('-', ' ').split()
    for n in range(3, 0, -1):
        if len(slug_parts) >= n:
            kw = ' '.join(slug_parts[:n])
            if len(kw) > 3:
                cnt = post['content'].lower().count(kw)
                if cnt > count:
                    keyword, count = kw, cnt
    
    return {
        'keyword': keyword,
        'count': count,
        'passed': count >= 5,
        'detail': '%d occurrences' % count
    }

def check_entities(post):
    content_lower = post['content'].lower()
    slug = post['slug']
    
    all_entities = ['Dhaka', 'Bangladesh']
    
    if any(kw in slug for kw in ['seo', 'seo-expert']):
        all_entities.append('SEO')
    if 'local' in slug or 'google-business' in slug or 'gbp' in slug:
        all_entities.extend(['Google Business Profile', 'local SEO'])
    if 'technical' in slug:
        all_entities.extend(['Core Web Vitals', 'schema'])
    if 'link-building' in slug:
        all_entities.extend(['backlinks', 'link building'])
    if 'case-study' in slug or 'case study' in slug:
        all_entities.extend(['traffic', 'organic', 'rankings'])
    if 'garment' in slug or 'textile' in slug:
        all_entities.extend(['garments', 'textile'])
    if 'mobile' in slug:
        all_entities.extend(['mobile-first', 'smartphone'])
    if 'geo' in slug or 'ai' in slug:
        all_entities.extend(['AI', 'GEO', 'ChatGPT'])
    if 'smm' in slug or 'panel' in slug:
        all_entities.extend(['SMM panel'])
    
    for tag in post['tags']:
        tl = tag.lower()
        if 'seo' in tl and 'seo' not in [e.lower() for e in all_entities]:
            all_entities.append('SEO')
        if 'ecommerce' in tl or 'e-commerce' in tl:
            all_entities.append('e-commerce')
        if 'garment' in tl or 'textile' in tl:
            all_entities.append('garments')
        if 'real estate' in tl:
            all_entities.append('real estate')
        if 'healthcare' in tl or 'medical' in tl:
            all_entities.append('healthcare')
    
    seen = set()
    unique_entities = []
    for e in all_entities:
        el = e.lower()
        if el not in seen:
            seen.add(el)
            unique_entities.append(e)
    
    missing = [e for e in unique_entities if e.lower() not in content_lower]
    return {
        'missing': missing,
        'passed': len(missing) == 0,
        'detail': 'Missing: ' + (', '.join(missing) if missing else 'None')
    }

def check_pillar_cluster(post):
    tags = post['tags']
    slug = post['slug']
    content_lower = post['content'].lower()
    
    pillar_map = {
        'Local SEO': ['local', 'gbp', 'google business', 'google maps'],
        'Technical SEO': ['technical', 'core web vitals', 'mobile'],
        'Content SEO': ['content', 'blog', 'writing', 'keyword research'],
        'Link Building': ['link building', 'backlinks'],
        'E-commerce SEO': ['ecommerce', 'e-commerce'],
        'SEO Strategy': ['seo guide', 'seo tips', 'seo checklist'],
        'GEO/AI SEO': ['geo', 'generative engine', 'ai seo', 'chatgpt'],
        'SEO Expert/Agency': ['seo expert', 'seo agency', 'seo consultant', 'hire seo', 'choose seo'],
    }
    
    detected = 'General SEO'
    for pillar, kws in pillar_map.items():
        for kw in kws:
            if kw in slug.lower() or any(kw in tag.lower() for tag in tags):
                detected = pillar
                break
        if detected != 'General SEO':
            break
    
    internal = re.findall(r'/blog/[a-z0-9-]+|/services/[a-z0-9-]+|/locations/[a-z0-9-]+|/industries/[a-z0-9-]+', content_lower)
    
    if detected == 'General SEO' and internal:
        detected = 'SEO Strategy'
    
    # Check for pillar-specific links (not just any internal link)
    pillar_link_patterns = {
        'Local SEO': ['/services/local', '/locations/'],
        'Technical SEO': ['/services/technical'],
        'Content SEO': ['/services/content', '/blog/content-'],
        'Link Building': ['/services/link-building', '/blog/link-building'],
        'E-commerce SEO': ['/services/ecommerce', '/industries/ecommerce'],
        'SEO Strategy': ['/blog/complete-seo-guide', '/blog/seo-mistakes'],
        'GEO/AI SEO': ['/services/geo', '/blog/geo-', '/blog/ai-seo'],
        'SEO Expert/Agency': ['/about', '/blog/seo-expert', '/blog/hiring-seo', '/blog/how-to-choose', '/blog/seo-expert-vs'],
    }
    
    expected_patterns = pillar_link_patterns.get(detected, [])
    has_pillar_link = any(any(pat in link for pat in expected_patterns) for link in internal) if expected_patterns else len(internal) > 0
    
    return {
        'pillar': detected,
        'has_pillar_link': has_pillar_link,
        'passed': has_pillar_link,  # for unified check interface
        'detail': 'Pillar: %s | Links: %s' % (detected, 'Yes' if has_pillar_link else 'No')
    }

def check_aeo_geo(post):
    headings = re.findall(r'^#{2,4}\s+.*$', post['content'], re.MULTILINE)
    
    q_starts = {'how', 'what', 'why', 'when', 'where', 'can', 'do', 'is', 'are', 'which', 'who', 'does', 'did', 'will', 'would', 'could', 'should'}
    
    q_headers = []
    for h in headings:
        hc = re.sub(r'[*_`"]', '', h.lstrip('#').strip())
        fw = hc.split()[0].lower() if hc.split() else ''
        if fw in q_starts:
            q_headers.append(hc)
    
    return {
        'count': len(q_headers),
        'passed': len(q_headers) >= 2,
        'detail': '%d question headings' % len(q_headers)
    }

def check_links(post):
    links = re.findall(r'/blog/[a-z0-9-]+|/services/[a-z0-9-]+|/locations/[a-z0-9-]+|/industries/[a-z0-9-]+', post['content'])
    unique = list(set(links))
    return {
        'count': len(unique),
        'passed': len(unique) >= 3,
        'detail': '%d unique internal links' % len(unique)
    }

def check_schema(post):
    fields = {
        'title': bool(post['title']),
        'excerpt': bool(post['excerpt']),
        'date': bool(post['date']),
        'metaTitle': bool(post['metaTitle']),
        'metaDescription': bool(post['metaDescription']),
        'dateModified': bool(post['dateModified']),
    }
    missing = [k for k, v in fields.items() if not v]
    return {
        'missing': missing,
        'passed': len(missing) == 0,
        'detail': 'Missing: ' + (', '.join(missing) if missing else 'All ok')
    }

# Run checks
changed_posts = [p for p in posts if p['slug'] in changed_slugs]

all_results = []
for post in changed_posts:
    all_results.append({
        'slug': post['slug'],
        'title': post['title'],
        'checks': {
            'tfidf': check_tfidf(post),
            'entities': check_entities(post),
            'pillar': check_pillar_cluster(post),
            'aeo': check_aeo_geo(post),
            'links': check_links(post),
            'schema': check_schema(post),
        }
    })

# Summary
pass_counts = {'tfidf': 0, 'entities': 0, 'pillar': 0, 'aeo': 0, 'links': 0, 'schema': 0}
for r in all_results:
    for k in pass_counts:
        if r['checks'][k]['passed']:
            pass_counts[k] += 1

total = len(all_results)
fully_pass = sum(1 for r in all_results if all(r['checks'][k]['passed'] for k in pass_counts))

print("=" * 72)
print("  CONTENT FRAMEWORK ENFORCEMENT REPORT")
print("  Project: kanokmiah.com.bd")
print("  Period: Last 48 hours")
print("=" * 72)
print()
print("  EXECUTIVE SUMMARY")
print("  " + "-" * 56)
print("  Posts changed in last 48h: %d" % total)
print("  Fully passing all checks:   %d" % fully_pass)
print("  Need fixes:                 %d" % (total - fully_pass))
print()
print("  Check pass rates:")
labels = {'tfidf': 'TF-IDF Coverage', 'entities': 'Entity Coverage', 'pillar': 'Pillar Link',
          'aeo': 'AEO/GEO', 'links': 'Internal Links', 'schema': 'Schema Ready'}
for k in ['tfidf', 'entities', 'pillar', 'aeo', 'links', 'schema']:
    v = pass_counts[k]
    pct = v * 100 // total
    bar = '#' * (pct // 10) + '-' * (10 - pct // 10)
    print("    %-20s [%s] %d/%d (%d%%)" % (labels[k], bar, v, total, pct))

print()
print("=" * 72)
print("  DETAILED POST-BY-POST REPORT")
print("=" * 72)

check_order = [('TF-IDF', 'tfidf'), ('Entities', 'entities'), ('Pillar Link', 'pillar'),
               ('AEO/GEO', 'aeo'), ('Internal Links', 'links'), ('Schema Ready', 'schema')]

for r in all_results:
    c = r['checks']
    fails = sum(1 for _, k in check_order if not c[k]['passed'])
    
    icon = '+ OK' if fails == 0 else '! FIX'
    print()
    print("  [%s] %s" % (icon, r['slug']))
    print("  Title: %s" % r['title'][:90])
    
    for label, key in check_order:
        ck = c[key]
        st = 'PASS' if ck['passed'] else 'FAIL'
        dt = ck['detail']
        if len(dt) > 55:
            dt = dt[:52] + '...'
        print("    %-15s %-6s %s" % (label, st, dt))
    
    if fails > 0:
        print("    Fixes:")
        if not c['tfidf']['passed']:
            print("      - TF-IDF: Increase \"%s\" usage (%sx -> 5+)" % (c['tfidf']['keyword'], c['tfidf']['count']))
        if not c['entities']['passed']:
            print("      - Entities: Add: %s" % ', '.join(c['entities']['missing']))
        if not c['pillar']['has_pillar_link']:
            print("      - Pillar: Link to %s pillar page" % c['pillar']['pillar'])
        if not c['aeo']['passed']:
            print("      - AEO/GEO: Add question headings (now %d, need >=2)" % c['aeo']['count'])
        if not c['links']['passed']:
            print("      - Links: Add internal links (now %d, need >=3)" % c['links']['count'])
        if not c['schema']['passed']:
            print("      - Schema: Add %s" % ', '.join(c['schema']['missing']))

print()
print("=" * 72)
print("  PRIORITY FIX LIST (by issue type)")
print("=" * 72)

issue_labels = {
    'schema': 'Schema Missing Fields',
    'aeo': 'AEO/GEO Question Headings',
    'pillar': 'Pillar Link Missing',
    'tfidf': 'Keyword Density',
    'entities': 'Entity Coverage',
    'links': 'Internal Links',
}

issue_posts = {k: [] for k in issue_labels}
for r in all_results:
    for k in issue_labels:
        if not r['checks'][k]['passed']:
            issue_posts[k].append(r['slug'])

for k in sorted(issue_labels, key=lambda x: len(issue_posts[x]), reverse=True):
    posts_list = issue_posts[k]
    if posts_list:
        print("\n  %s (%d posts):" % (issue_labels[k], len(posts_list)))
        for s in posts_list:
            print("    - %s" % s)

print()
print("=" * 72)
print("  END OF REPORT")
print("=" * 72)
