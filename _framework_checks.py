#!/usr/bin/env python3
"""Run all framework checks on extracted posts."""
import json
import re

with open('/tmp/extracted_posts.json', 'r') as f:
    posts = json.load(f)

# From data.js, identify all known pillar pages and internal link targets
PILLAR_PAGES = {
    "complete-seo-guide-bangladesh-businesses-2026": {
        "pillar": "SEO Guide",
        "cluster_tags": ["SEO Guide", "Bangladesh SEO", "Digital Marketing", "2026"]
    },
    "local-seo-tips-dhaka-businesses-google-maps": {
        "pillar": "Local SEO",
        "cluster_tags": ["Local SEO", "Google Maps", "Dhaka"]
    },
    "why-ecommerce-store-needs-seo-bangladesh": {
        "pillar": "E-commerce SEO",
        "cluster_tags": ["E-commerce", "SEO"]
    },
    "technical-seo-checklist-bangladeshi-websites": {
        "pillar": "Technical SEO",
        "cluster_tags": ["Technical SEO", "Core Web Vitals"]
    },
}

# Known service pages
SERVICE_PAGES = [
    "/services/local-seo",
    "/services/on-page-seo",
    "/services/technical-seo",
    "/services/ecommerce-seo",
    "/services/seo-audit",
    "/services/content-marketing",
    "/services/link-building",
    "/services/ppc-management",
    "/services/social-media-marketing",
    "/services/web-design",
]

# Known location pages
LOCATION_PAGES = [
    "/locations/dhaka",
    "/locations/chittagong",
    "/locations/sylhet",
    "/locations/khulna",
    "/locations/rajshahi",
    "/locations/bogura",
]

# Known industry pages
INDUSTRY_PAGES = [
    "/industries/medical",
    "/industries/education",
    "/industries/ecommerce",
    "/industries/real-estate",
    "/industries/garments-textile",
    "/industries/hotel-resort",
    "/industries/restaurant-food",
    "/industries/legal",
    "/industries/fitness",
]

# Primary keywords derived from titles
def extract_primary_keyword(title):
    """Extract the most meaningful keyword phrase from title."""
    # Remove trailing year/date
    title_clean = re.sub(r'\s+(20\d{2}|202\d)\s*$', '', title)
    
    # For case studies, extract the brand/company name
    case_study_m = re.match(r'^(.+?)\s+(SEO\s+)?Case\s+Study', title, re.IGNORECASE)
    if case_study_m:
        brand = case_study_m.group(1).strip()
        words = brand.split()
        if len(words) <= 5:
            brand = re.sub(r'^SEO\s+for\s+', '', brand, flags=re.IGNORECASE)
            brand = re.sub(r'[&]', 'and', brand)
            return brand.strip()
    
    # For "SEO for X: Y" format - extract the key noun from the subject
    m = re.match(r'^(SEO\s+for\s+)(.+?)(?:\s*[:\-–—]\s*.*)?$', title, re.IGNORECASE)
    if m:
        subject = m.group(2).strip()
        # Clean special chars
        subject = re.sub(r'[&]', 'and', subject)
        # Take first 3 words max (the core industry/service)
        words = subject.split()
        if len(words) > 3:
            return ' '.join(words[:3])
        return subject
    
    # For "How to X", "Why X", "What X" - skip the question word
    m = re.match(r'^(How|Why|What|When|Where)\s+(.+?)(?:\s*[:\-–—].*)?$', title, re.IGNORECASE)
    if m:
        kw = m.group(2).strip()
        # Remove leading article
        kw = re.sub(r'^(A|An|The)\s+', '', kw, flags=re.IGNORECASE)
        kw = re.sub(r'[&]', 'and', kw)
        # Take first 4 words max
        words = kw.split()
        if len(words) > 4:
            return ' '.join(words[:4])
        return kw
    
    # For "Top 10 X" format
    m = re.match(r'^Top\s+\d+\s+(.+?)(?:\s*[:\-–—(].*)?$', title, re.IGNORECASE)
    if m:
        kw = m.group(1).strip()
        kw = re.sub(r'[&]', 'and', kw)
        words = kw.split()
        if len(words) > 4:
            return ' '.join(words[:4])
        return kw
    
    # For "X: Y" format, take the part before colon
    parts = re.split(r'\s*[:\-–—]\s*', title)
    main = parts[0].strip()
    
    # Remove trailing qualifiers
    main = re.sub(r'\s+(A\s+)?(Complete\s+)?(Guide|Checklist|Strategies|Tips)\s*$', '', main, flags=re.IGNORECASE)
    
    # Clean special chars
    main = re.sub(r'[&]', 'and', main)
    
    words = main.split()
    if len(words) > 6:
        return ' '.join(words[:4])
    return main

def count_keyword_occurrences(content, keyword):
    """Count occurrences of primary keyword in content."""
    if not keyword:
        return 0
    # Escape for regex
    kw = re.escape(keyword.lower())
    return len(re.findall(kw, content.lower()))

def count_question_headings(content):
    """Count question-based headings (## or ### starting with How, What, Why, etc.)"""
    q_words = r'(How|What|Why|When|Where|Can|Do|Is|Are|Which|Who|Whose|Should|Could|Would|Does|Did|Has|Have)'
    pattern = rf'^#{{2,3}}\s+{q_words}\b'
    matches = re.findall(pattern, content, re.MULTILINE)
    return len(matches)

def count_internal_links(content):
    """Count internal links to other posts, services, locations, industries."""
    # Match /blog/... , /services/... , /locations/... , /industries/... , /about
    internal_patterns = [
        r'/blog/[a-z0-9-]+',
        r'/services/[a-z0-9-]+',
        r'/locations/[a-z0-9-]+',
        r'/industries/[a-z0-9-]+',
        r'/about',
    ]
    total = 0
    links_found = []
    for pat in internal_patterns:
        matches = re.findall(pat, content)
        total += len(matches)
        links_found.extend(matches)
    return total, list(set(links_found))

def find_pillar_link(content, tags):
    """Check if post links to any known pillar page."""
    # Known pillar pages
    known_pillars = [
        'complete-seo-guide-bangladesh-businesses-2026',
        'local-seo-tips-dhaka-businesses-google-maps',
        'why-ecommerce-store-needs-seo-bangladesh',
        'technical-seo-checklist-bangladeshi-websites',
    ]
    
    # Find which pillar(s) are linked
    linked_pillars = []
    for p in known_pillars:
        if f'/blog/{p}' in content:
            linked_pillars.append(p)
    
    # Try to determine the best pillar match from tags
    tag_lower = [t.lower() for t in tags]
    tag_str = ' '.join(tag_lower)
    
    # Priority mapping: check specific first, then fallback
    if 'e-commerce' in tag_str or 'ecommerce' in tag_str:
        best_pillar = 'why-ecommerce-store-needs-seo-bangladesh'
    elif 'technical seo' in tag_str or 'core web vitals' in tag_str:
        best_pillar = 'technical-seo-checklist-bangladeshi-websites'
    elif ('local seo' in tag_str or 'google maps' in tag_str) and not any(x in tag_str for x in ['healthcare', 'medical', 'education', 'ecommerce', 'technical']):
        best_pillar = 'local-seo-tips-dhaka-businesses-google-maps'
    else:
        best_pillar = 'complete-seo-guide-bangladesh-businesses-2026'
    
    if linked_pillars:
        return True, best_pillar, linked_pillars
    return False, best_pillar, []

def check_schema_readiness(post):
    """Check if post has title, excerpt, date for ArticleSchema."""
    has_title = bool(post.get('title'))
    has_excerpt = bool(post.get('excerpt'))
    has_date = bool(post.get('date'))
    missing = []
    if not has_title: missing.append('title')
    if not has_excerpt: missing.append('excerpt')
    if not has_date: missing.append('date')
    return len(missing) == 0, missing

def check_entities(content, title):
    """Check for key entities."""
    entities = {
        'location_dhaka': r'\b[Dd]haka\b',
        'location_bangladesh': r'\b[Bb]angladesh\b',
    }
    
    # Determine expected entities based on title/content
    title_lower = title.lower()
    content_lower = content.lower()
    
    expected = ['location_dhaka', 'location_bangladesh']
    
    if 'seo' in title_lower:
        expected.append('service_seo')
    if 'local' in title_lower or 'maps' in title_lower:
        expected.append('service_local')
    if 'ecommerce' in title_lower or 'e-commerce' in title_lower or 'store' in title_lower:
        expected.append('industry_ecommerce')
    if 'healthcare' in title_lower or 'medical' in title_lower or 'clinic' in title_lower:
        expected.append('industry_healthcare')
    if 'garment' in title_lower or 'textile' in title_lower:
        expected.append('industry_garments')
    if 'case study' in title_lower:
        expected.append('case_study')
    
    entity_map = {
        'location_dhaka': r'\b[Dd]haka\b',
        'location_bangladesh': r'\b[Bb]angladesh\b',
        'service_seo': r'\b[Ss][Ee][Oo]\b',
        'service_local': r'\blocal\s+seo\b',
        'industry_ecommerce': r'\b(ecommerce|e-commerce)\b',
        'industry_healthcare': r'\b(healthcare|medical|clinic|hospital)\b',
        'industry_garments': r'\b(garment|textile)\b',
        'case_study': r'\bcase\s+study\b',
        'author_kanok': r'\bKanok\s+Miah\b',
    }
    
    found = []
    missing = []
    for entity in expected:
        pattern = entity_map.get(entity)
        if pattern:
            if re.search(pattern, content, re.IGNORECASE):
                found.append(entity)
            else:
                missing.append(entity)
    
    return found, missing

def run_checks(post):
    slug = post['slug']
    title = post['title']
    content = post['content']
    tags = post['tags']
    excerpt = post['excerpt']
    date = post['date']
    
    results = {}
    
    # A. TF-IDF Coverage
    keyword = extract_primary_keyword(title)
    kw_count = count_keyword_occurrences(content, keyword)
    results['tfidf'] = {
        'keyword': keyword[:50],
        'count': kw_count,
        'pass': kw_count >= 5
    }
    
    # B. Semantic Entity Coverage
    found_entities, missing_entities = check_entities(content, title)
    results['entities'] = {
        'found': found_entities,
        'missing': missing_entities,
        'pass': len(missing_entities) == 0
    }
    
    # C. Pillar-Cluster Alignment
    has_pillar, pillar_slug, linked_pillars = find_pillar_link(content, tags)
    results['pillar'] = {
        'has_link': has_pillar,
        'pillar_slug': pillar_slug,
        'linked_pillars': linked_pillars,
        'pass': has_pillar
    }
    
    # D. AEO/GEO Optimization
    q_count = count_question_headings(content)
    results['aeo_geo'] = {
        'question_headings': q_count,
        'pass': q_count >= 2
    }
    
    # E. Internal Linking
    link_count, links_found = count_internal_links(content)
    results['internal_links'] = {
        'count': link_count,
        'unique_links': links_found[:15],
        'pass': link_count >= 3
    }
    
    # F. Schema
    schema_ready, schema_missing = check_schema_readiness(post)
    results['schema'] = {
        'ready': schema_ready,
        'missing': schema_missing,
        'pass': schema_ready
    }
    
    return results

# Run checks on all posts
all_results = {}
for post in posts:
    slug = post['slug']
    all_results[slug] = run_checks(post)

# Generate report
for post in posts:
    slug = post['slug']
    title = post['title']
    r = all_results[slug]
    
    print(f"\n## Post: {slug}")
    print(f"**Title:** {title}")
    print(f"| Check | Status | Details |")
    print(f"|-------|--------|---------|")
    
    # TF-IDF
    tf = r['tfidf']
    tf_status = '✅' if tf['pass'] else '❌'
    print(f"| TF-IDF: \"{tf['keyword']}\" | {tf_status} | {tf['count']} occurrences |")
    
    # Entities
    en = r['entities']
    en_status = '✅' if en['pass'] else '❌'
    missing_str = ', '.join(en['missing']) if en['missing'] else 'None'
    print(f"| Entities | {en_status} | Missing: {missing_str} |")
    
    # Pillar
    pi = r['pillar']
    pi_status = '✅' if pi['pass'] else '❌'
    pi_detail = f"Links to pillar(s): {', '.join(pi['linked_pillars'])}" if pi['has_link'] else f"Expected: /blog/{pi['pillar_slug']} — not found"
    print(f"| Pillar Link | {pi_status} | {pi_detail} |")
    
    # AEO/GEO
    aeo = r['aeo_geo']
    aeo_status = '✅' if aeo['pass'] else '❌'
    print(f"| AEO/GEO | {aeo_status} | {aeo['question_headings']} question headings |")
    
    # Internal Links
    il = r['internal_links']
    il_status = '✅' if il['pass'] else '❌'
    print(f"| Internal Links | {il_status} | {il['count']} total |")
    
    # Schema
    sc = r['schema']
    sc_status = '✅' if sc['pass'] else '❌'
    sc_detail = 'All fields set' if sc['ready'] else f"Missing: {', '.join(sc['missing'])}"
    print(f"| Schema Ready | {sc_status} | {sc_detail} |")
    
    # Fix instructions
    print(f"\n### Fix instructions:")
    fixes = []
    if not tf['pass']:
        fixes.append(f"- **TF-IDF Thin**: Primary keyword \"{tf['keyword']}\" appears only {tf['count']} times. Add more occurrences (target ≥5) throughout the content.")
    if not en['pass']:
        fixes.append(f"- **Missing Entities**: Add these entities: {missing_str}")
    if not pi['pass']:
        fixes.append(f"- **Missing Pillar Link**: Add link to pillar page `/blog/{pi['pillar_slug']}`")
    if not aeo['pass']:
        fixes.append(f"- **Low Question Headings**: Only {aeo['question_headings']} found. Add at least 2 question-based headings (How, What, Why...)")
    if not il['pass']:
        fixes.append(f"- **Insufficient Internal Links**: Only {il['count']} found. Add more links to other posts, services, or locations (target ≥3)")
    if not sc['pass']:
        fixes.append(f"- **Schema Incomplete**: Missing fields: {', '.join(sc['missing'])}")
    
    if fixes:
        for fix in fixes:
            print(fix)
    else:
        print("✅ All checks passed — no changes needed.")

with open('/tmp/framework_report.md', 'w') as f:
    f.write("# Content Framework Enforcement Report\n")
    f.write(f"**Date:** 2026-07-27\n")
    f.write(f"**Posts checked:** {len(posts)}\n\n")
    
    for post in posts:
        slug = post['slug']
        title = post['title']
        r = all_results[slug]
        
        f.write(f"\n## Post: {slug}\n")
        f.write(f"**Title:** {title}\n\n")
        f.write("| Check | Status | Details |\n")
        f.write("|-------|--------|---------|\n")
        
        tf = r['tfidf']
        tf_status = '✅' if tf['pass'] else '❌'
        f.write(f"| TF-IDF: \"{tf['keyword']}\" | {tf_status} | {tf['count']} occurrences |\n")
        
        en = r['entities']
        en_status = '✅' if en['pass'] else '❌'
        missing_str = ', '.join(en['missing']) if en['missing'] else 'None'
        f.write(f"| Entities | {en_status} | Missing: {missing_str} |\n")
        
        pi = r['pillar']
        pi_status = '✅' if pi['pass'] else '❌'
        pi_detail = f"Links to pillar(s): {', '.join(pi['linked_pillars'])}" if pi['has_link'] else f"Expected: /blog/{pi['pillar_slug']} — not found"
        f.write(f"| Pillar Link | {pi_status} | {pi_detail} |\n")
        
        aeo = r['aeo_geo']
        aeo_status = '✅' if aeo['pass'] else '❌'
        f.write(f"| AEO/GEO | {aeo_status} | {aeo['question_headings']} question headings |\n")
        
        il = r['internal_links']
        il_status = '✅' if il['pass'] else '❌'
        f.write(f"| Internal Links | {il_status} | {il['count']} total |\n")
        
        sc = r['schema']
        sc_status = '✅' if sc['pass'] else '❌'
        sc_detail = 'All fields set' if sc['ready'] else f"Missing: {', '.join(sc['missing'])}"
        f.write(f"| Schema Ready | {sc_status} | {sc_detail} |\n")
        
        f.write("\n### Fix instructions:\n")
        fixes = []
        if not tf['pass']:
            fixes.append(f"- **TF-IDF Thin**: Primary keyword \"{tf['keyword']}\" appears only {tf['count']} times. Add more occurrences (target ≥5) throughout the content.")
        if not en['pass']:
            fixes.append(f"- **Missing Entities**: Add these entities: {missing_str}")
        if not pi['pass']:
            fixes.append(f"- **Missing Pillar Link**: Add link to known pillar page (e.g., `/blog/{pi['pillar_slug']}`). Current linked pillars: {', '.join(pi['linked_pillars']) if pi['linked_pillars'] else 'none'}")
        if not aeo['pass']:
            fixes.append(f"- **Low Question Headings**: Only {aeo['question_headings']} found. Add at least 2 question-based headings (How, What, Why...)")
        if not il['pass']:
            fixes.append(f"- **Insufficient Internal Links**: Only {il['count']} found. Add more links to other posts, services, or locations (target ≥3)")
        if not sc['pass']:
            fixes.append(f"- **Schema Incomplete**: Missing fields: {', '.join(sc['missing'])}")
        
        if fixes:
            for fix in fixes:
                f.write(fix + "\n")
        else:
            f.write("✅ All checks passed — no changes needed.\n")
        f.write("\n---\n")
    
    # Summary
    passed = sum(1 for r in all_results.values() if all([
        r['tfidf']['pass'],
        r['entities']['pass'],
        r['pillar']['pass'],
        r['aeo_geo']['pass'],
        r['internal_links']['pass'],
        r['schema']['pass'],
    ]))
    total = len(posts)
    f.write(f"\n## Summary\n")
    f.write(f"- **Total posts checked:** {total}\n")
    f.write(f"- **All checks passed:** {passed}/{total}\n")

print(f"\n\nReport saved to /tmp/framework_report.md")
