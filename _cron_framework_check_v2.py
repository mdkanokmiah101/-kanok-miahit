#!/usr/bin/env python3
"""
Refined framework enforcement checker for kanokmiah.com.bd blog posts.
"""
import re

DATA_PATH = 'src/app/blog/data.js'

with open(DATA_PATH, 'r') as f:
    text = f.read()
lines = text.split('\n')

# Build slug-to-line map
slug_positions = {}
for i, line in enumerate(lines):
    m = re.search(r'slug:\s*"([^"]+)"', line)
    if m:
        slug_positions[m.group(1)] = i

# Also build a map of slug to title
slug_title = {}
for i, line in enumerate(lines):
    m_slug = re.search(r'slug:\s*"([^"]+)"', line)
    if m_slug:
        slug = m_slug.group(1)
        # Look ahead for title within next few lines
        for j in range(i, min(i + 10, len(lines))):
            m_title = re.search(r'title:\s*"([^"]+)"', lines[j])
            if m_title:
                slug_title[slug] = m_title.group(1)
                break

def extract_post_fields(slug):
    """Extract title, date, excerpt, tags, content from a post."""
    slug_line = slug_positions[slug]
    
    # Find start of post (line with '{' before slug)
    start = slug_line
    while start > 0 and not lines[start].strip().startswith('{'):
        start -= 1
    
    # Find next slug or end
    next_slug_line = None
    for s, ln in sorted(slug_positions.items(), key=lambda x: x[1]):
        if ln > slug_line:
            next_slug_line = ln
            break
    
    end = next_slug_line if next_slug_line else len(lines)
    
    post_lines = lines[start:end]
    post_text = '\n'.join(post_lines)
    
    title_m = re.search(r'title:\s*"([^"]*)"', post_text)
    date_m = re.search(r'date:\s*"([^"]*)"', post_text)
    date_mod_m = re.search(r'dateModified:\s*"([^"]*)"', post_text)
    excerpt_m = re.search(r'excerpt:\s*\n?\s*"([^"]*)"', post_text, re.DOTALL)
    tags_m = re.search(r'tags:\s*\[([^\]]*)\]', post_text, re.DOTALL)
    content_m = re.search(r'content:\s*`\n?([^`]*)`', post_text, re.DOTALL)
    
    title = title_m.group(1) if title_m else ''
    date = date_m.group(1) if date_m else ''
    date_mod = date_mod_m.group(1) if date_mod_m else ''
    excerpt = excerpt_m.group(1).replace('\n', ' ').strip() if excerpt_m else ''
    tags = re.findall(r'"([^"]*)"', tags_m.group(1)) if tags_m else []
    content = content_m.group(1) if content_m else ''
    
    return {'title': title, 'date': date, 'dateModified': date_mod,
            'excerpt': excerpt, 'tags': tags, 'content': content, 'slug': slug}

def smart_keyword(title, content, is_case_study=False, slug=''):
    """Extract best primary keyword and count occurrences."""
    # For case studies, use the company/brand name from title
    if is_case_study or 'case study' in title.lower() or 'case-study' in slug:
        # Extract company name - words before "SEO" or "Case Study"
        parts = title.split(':')[0] if ':' in title else title
        parts = parts.replace('Case Study', '').replace('SEO', '').strip()
        # Clean up
        company_words = re.findall(r'[A-Za-z0-9]+', parts)
        if company_words:
            # Use the full company name
            kw = ' '.join(company_words)
            count = len(re.findall(re.escape(kw), content, re.IGNORECASE))
            if count >= 3:
                return kw, count
            # Try first word
            kw = company_words[0]
            count = len(re.findall(re.escape(kw), content, re.IGNORECASE))
            return kw, count
    
    # For Bengali titles, use English SEO as keyword
    if any('\u0980' <= c <= '\u09FF' for c in title):
        kw = 'SEO'
        count = len(re.findall(r'\bSEO\b', content))
        return kw, count
    
    # Try to extract meaningful 2-3 word phrase from title
    stop_words = {'the', 'a', 'an', 'in', 'of', 'for', 'to', 'and', 'or', 'is', 'are', 'was', 'were',
                  'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
                  'can', 'could', 'shall', 'should', 'may', 'might', 'must', 'about', 'into', 'through',
                  'during', 'before', 'after', 'above', 'below', 'between', 'out', 'off', 'over', 'under',
                  'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how',
                  'all', 'each', 'every', 'both', 'few', 'more', 'most', 'other', 'some', 'such',
                  'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 'just',
                  'because', 'as', 'until', 'while', 'with', 'without', 'from', 'up', 'down', 'at',
                  'by', 'on', 'off', 'this', 'that', 'these', 'those', 'it', 'its', 'your', 'our',
                  'their', 'what', 'which', 'who', 'whom', 'your', '2026', 'guide', 'new'}
    
    # Title clean
    clean_title = title.replace(':', ' ').replace('?', ' ').replace('!', ' ')
    words = clean_title.split()
    meaningful = [w.strip() for w in words if w.lower() not in stop_words and len(w.strip()) > 2]
    
    # For GEO Optimization title
    if 'GEO' in title or 'GEO Optimization' in title:
        kw = 'GEO'
        count = len(re.findall(r'\bGEO\b', content))
        return kw, count
    
    # Try primary/main keyword from title
    if meaningful:
        # Try 3-word phrase first
        if len(meaningful) >= 3:
            for phrase_len in [3, 2, 1]:
                phrase = ' '.join(meaningful[:phrase_len])
                count = len(re.findall(re.escape(phrase), content, re.IGNORECASE))
                if count >= 3:
                    return phrase, count
        
        # Try first meaningful word
        kw = meaningful[0]
        count = len(re.findall(re.escape(kw), content, re.IGNORECASE))
        if count >= 3:
            return kw, count
    
    # Fallback: first word from title
    kw = words[0].strip().rstrip(',').rstrip(':')
    count = len(re.findall(re.escape(kw), content, re.IGNORECASE))
    return kw, count

def check_tfidf(post):
    content = post['content']
    title = post['title']
    slug = post['slug']
    
    is_case = slug.endswith('case-study') or 'case-study' in slug
    keyword, count = smart_keyword(title, content, is_case, slug)
    
    status = '✅' if count >= 5 else ('⚠️' if count >= 3 else '❌')
    return f'TF-IDF: "{keyword}"', status, f'{count} occurrences'

def check_entities(post):
    content = post['content']
    title = post['title']
    slug = post['slug']
    
    expected = {
        'location': ['Dhaka', 'Bangladesh', 'Chittagong', 'Sylhet'],
        'geo': ['Generative Engine Optimization', 'AI search', 'ChatGPT', 'SGE', 'Perplexity'],
        'garments': ['garment', 'textile', 'B2B', 'manufacturer'],
        'healthcare': ['healthcare', 'hospital', 'clinic', 'patient'],
        'case_study': ['traffic', 'results', 'monthly'],
        'seo_expert': ['SEO', 'expert', 'Dhaka'],
        'agency': ['agency', 'SEO', 'choose'],
        'mistakes': ['mistakes', 'errors', 'avoid'],
        'hiring_roi': ['SEO', 'expert', 'ROI'],
        'trends': ['trends', 'AI', 'GEO', '2026'],
        'tips_bn': ['SEO', 'টিপস'],
    }
    
    # Determine what entities to check
    to_check = []
    loc_found = [l for l in expected['location'] if re.search(re.escape(l), content, re.IGNORECASE)]
    
    if slug == 'geo-optimization-prepare-business-ai-search':
        to_check = expected['geo']
    elif slug == 'seo-garments-textile-industry-b2b-lead-generation':
        to_check = expected['garments']
    elif slug == 'seo-healthcare-medical-clinics-bangladesh':
        to_check = expected['healthcare']
    elif slug in ['why-md-kanok-miah-is-the-best-seo-expert-in-dhaka-bangladesh']:
        to_check = ['SEO', 'expert', 'Dhaka', 'Bangladesh', 'certifications', 'experience']
    elif slug.endswith('case-study') or 'case-study' in slug:
        to_check = expected['case_study']
    elif slug in ['how-to-choose-right-seo-agency-bangladesh', 'seo-expert-vs-seo-agency-dhaka-which-is-right']:
        to_check = expected['agency']
    elif slug == 'top-10-seo-mistakes-dhaka-businesses-fix':
        to_check = expected['mistakes']
    elif slug == 'hiring-seo-expert-dhaka-better-roi-than-paid-ads':
        to_check = expected['hiring_roi']
    elif slug == 'seo-trends-2026-ai-geo-future':
        to_check = expected['trends']
    elif slug == 'seo-tips-for-business-owners-bd':
        to_check = expected['tips_bn']
    elif slug == 'seo-case-study-dhaka-businesses-increased-organic-traffic':
        to_check = expected['case_study'] + ['Dhaka']
    else:
        to_check = ['SEO', 'service', 'business']
    
    missing = []
    for entity in to_check:
        if not re.search(re.escape(entity), content, re.IGNORECASE):
            missing.append(entity)
    
    if not loc_found and slug not in ['locksmith-dundee-seo-case-study', 'das-taxis-scotland-seo-case-study',
                                       'stealth-windshield-repairs-seo-case-study',
                                       'morethanpanel-seo-case-study', 'smmgen-seo-case-study',
                                       'smmsun-seo-case-study', 'mir-cement-seo-case-study',
                                       'dhaka-apparels-seo-case-study']:
        missing.append('Dhaka/Bangladesh location')
    
    status = '✅' if not missing else '❌'
    detail = 'All key entities present' if not missing else f'Missing: {", ".join(missing[:5])}'
    return 'Entities', status, detail

def check_pillar_link(post):
    content = post['content']
    pillar_urls = [
        '/blog/complete-seo-guide-bangladesh-businesses-2026',
        '/services/local-seo', '/services/technical-seo', '/services/ecommerce-seo',
        '/services/geo-ai-search', '/services/semantic-seo', '/services/link-building',
    ]
    found = []
    for url in pillar_urls:
        c = content.count(url)
        if c > 0:
            found.append(f'{url}')
    status = '✅' if found else '❌'
    detail = f'Links to: {", ".join(found)}' if found else 'No pillar links found'
    return 'Pillar Link', status, detail

def check_aeo_geo(post):
    content = post['content']
    heading_pattern = re.findall(r'^#{2,6}\s+.*$', content, re.MULTILINE)
    question_words = ['How', 'What', 'Why', 'When', 'Where', 'Can', 'Do', 'Is', 'Are', 'Does', 'Did']
    
    q_headings = []
    for h in heading_pattern:
        text = h.lstrip('#').strip()
        if text.split():
            first = text.split()[0]
            if first in question_words:
                q_headings.append(text[:60])
    
    count = len(q_headings)
    status = '✅' if count >= 2 else '❌'
    detail = f'{count} question headings'
    if q_headings:
        detail += f' (first: "{q_headings[0]}")'
    return 'AEO/GEO', status, detail

def check_internal_links(post):
    content = post['content']
    # Count all unique internal link paths (not counting / and #)
    md_links = set()
    for m in re.finditer(r'\((/[^\)\s#]+)\)', content):
        path = m.group(1).rstrip('/')
        if path and path != '':
            md_links.add(path)
    
    for m in re.finditer(r'href="(/[^"\s#]+)"', content):
        path = m.group(1).rstrip('/')
        if path and path != '':
            md_links.add(path)
    
    # Filter out single-slash paths
    all_links = sorted([l for l in md_links if l != '/'])
    count = len(all_links)
    status = '✅' if count >= 3 else '❌'
    sample = ', '.join(all_links[:4]) if all_links else 'none'
    return 'Internal Links', status, f'{count} internal links (e.g., {sample})'

def check_schema(post):
    issues = []
    if not post.get('title'):
        issues.append('Missing title')
    if not post.get('excerpt') or len(post['excerpt']) < 10:
        issues.append('Missing/short excerpt')
    if not post.get('date'):
        issues.append('Missing date')
    status = '✅' if not issues else '❌'
    detail = 'All fields set' if not issues else ', '.join(issues)
    return 'Schema Ready', status, detail

def get_change_type(slug):
    substantive = [
        'geo-optimization-prepare-business-ai-search',
        'seo-garments-textile-industry-b2b-lead-generation',
        'seo-healthcare-medical-clinics-bangladesh',
    ]
    if slug in substantive:
        return 'Content modifications (additions/rewordings)'
    return 'Link cleanup only (removed duplicate /-linked homepage links)'

changed_slugs = [
    'geo-optimization-prepare-business-ai-search',
    'seo-garments-textile-industry-b2b-lead-generation',
    'seo-healthcare-medical-clinics-bangladesh',
    'why-md-kanok-miah-is-the-best-seo-expert-in-dhaka-bangladesh',
    'locksmith-dundee-seo-case-study',
    'das-taxis-scotland-seo-case-study',
    'morethanpanel-seo-case-study',
    'smmgen-seo-case-study',
    'smmsun-seo-case-study',
    'mir-cement-seo-case-study',
    'dhaka-apparels-seo-case-study',
    'stealth-windshield-repairs-seo-case-study',
    'how-to-choose-right-seo-agency-bangladesh',
    'seo-expert-vs-seo-agency-dhaka-which-is-right',
    'top-10-seo-mistakes-dhaka-businesses-fix',
    'seo-tips-for-business-owners-bd',
    'seo-case-study-dhaka-businesses-increased-organic-traffic',
    'hiring-seo-expert-dhaka-better-roi-than-paid-ads',
    'seo-trends-2026-ai-geo-future'
]

aggregate_stats = {'✅': 0, '❌': 0, '⚠️': 0}
check_names = ['TF-IDF', 'Entities', 'Pillar Link', 'AEO/GEO', 'Internal Links', 'Schema Ready']
check_fails = {c: [] for c in check_names}
check_passes = {c: [] for c in check_names}

print("=" * 82)
print("KANOKMIAH.COM.BD — CONTENT FRAMEWORK ENFORCEMENT REPORT")
print("Commit: c822841  |  Date: Sun Jul 26 06:06:18 2026 (last 48h)")
print("=" * 82)

all_posts_report = []

for slug in changed_slugs:
    if slug not in slug_positions:
        continue
    
    post = extract_post_fields(slug)
    
    print(f"\n{'─' * 82}")
    print(f"📄 {slug}")
    print(f"   Title: {post['title']}")
    print(f"   Change: {get_change_type(slug)}")
    print(f"{'─' * 82}")
    print(f"{'Check':<30} {'Status':<8} {'Details'}")
    print(f"{'─' * 30} {'─' * 8} {'─' * 42}")
    
    checks = {}
    for fn in [check_tfidf, check_entities, check_pillar_link, check_aeo_geo, check_internal_links, check_schema]:
        name, status, detail = fn(post)
        checks[name.split(':')[0].split('"')[0].strip()] = status
        icon = ' ' + status
        print(f"{name:<30} {icon:<8} {detail}")
        
        agg_key = status.strip()
        aggregate_stats[agg_key] = aggregate_stats.get(agg_key, 0) + 1
        
        # Track fails/passes per check category
        for cn in check_names:
            if name.startswith(cn) or cn in name:
                if '❌' in status or '⚠️' in status:
                    check_fails[cn].append(slug)
                else:
                    check_passes[cn].append(slug)
    
    print()

# Summary
print(f"\n{'=' * 82}")
print("SUMMARY")
print(f"{'=' * 82}")
total_checks = sum(aggregate_stats.values())
passed = aggregate_stats.get('✅', 0)
failed = aggregate_stats.get('❌', 0)
warned = aggregate_stats.get('⚠️', 0)
print(f"Total checks: {total_checks}  |  ✅ Passed: {passed}  |  ❌ Failed: {failed}  |  ⚠️ Warning: {warned}")
print(f"Overall pass rate: {passed/total_checks*100:.0f}%")
print()

print(f"{'Check':<30} {'Passed':<8} {'Failed':<8}")
print(f"{'─' * 30} {'─' * 8} {'─' * 8}")
for cn in check_names:
    p = len(check_passes.get(cn, []))
    f = len(check_fails.get(cn, []))
    print(f"{cn:<30} {p:<8} {f:<8}")

print()
print("KEY ISSUES TO ADDRESS:")
print()

# Section 1: Posts with missing dateModified
missing_dates = [s for s in changed_slugs if s in slug_positions]
missing_dates_actual = []
for s in missing_dates:
    post = extract_post_fields(s)
    if not post.get('dateModified'):
        missing_dates_actual.append(s)
print(f"1. Missing dateModified: {len(missing_dates_actual)} posts")
print(f"   All posts need dateModified set for ArticleSchema. The complete-seo-guide has it, use as template.")

# Section 2: AEO/GEO failures (low question headings)
aeo_fails = check_fails.get('AEO/GEO', [])
if aeo_fails:
    print(f"\n2. Low question-based headings (AEO/GEO): {len(aeo_fails)} posts")
    for s in aeo_fails:
        print(f"   • {s}")

# Section 3: Internal linking failures
il_fails = check_fails.get('Internal Links', [])
if il_fails:
    print(f"\n3. Insufficient internal links (< 3): {len(il_fails)} posts")
    for s in il_fails:
        print(f"   • {s}")

# Section 4: Entity coverage failures  
ent_fails = check_fails.get('Entities', [])
if ent_fails:
    print(f"\n4. Missing entities: {len(ent_fails)} posts")
    for s in ent_fails:
        print(f"   • {s}")

print()
print("CONSOLIDATED PRIORITY FIX LIST")
print(f"{'─' * 82}")
print("| Post | Issues |")
print(f"{'─' * 82}")
for slug in changed_slugs:
    if slug not in slug_positions:
        continue
    post = extract_post_fields(slug)
    issues = []
    
    # Check all six
    _, s1, _ = check_tfidf(post)
    _, s2, d2 = check_entities(post)
    _, s3, _ = check_pillar_link(post)
    _, s4, _ = check_aeo_geo(post)
    _, s5, _ = check_internal_links(post)
    _, s6, _ = check_schema(post)
    
    issue_list = []
    if '❌' in s1: issue_list.append('TF-IDF')
    if '❌' in s2: issue_list.append(f'Entities ({d2})')
    if '❌' in s3: issue_list.append('Pillar link')
    if '❌' in s4: issue_list.append('AEO/GEO')
    if '❌' in s5: issue_list.append('Internal links')
    if '❌' in s6: issue_list.append('Schema')
    
    if issue_list:
        print(f"| {slug:<50} | {', '.join(issue_list)} |")
    # else:
    #     print(f"| {slug:<50} | ✅ All checks passed |")

print(f"{'─' * 82}")
print("\nEnd of report.")
