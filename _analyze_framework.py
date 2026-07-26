#!/usr/bin/env python3
"""
Content Framework Analysis for kanokmiah.com.bd
Analyzes posts against the 6-pillar content framework.
"""
import json
import re
import sys
from pathlib import Path

# Load posts from JSON
with open('/tmp/posts.json', 'r') as f:
    ALL_POSTS = json.load(f)

POSTS_BY_SLUG = {p['slug']: p for p in ALL_POSTS}

# Modified slugs from git diff HEAD~4
MODIFIED_SLUGS = [
    "das-taxis-scotland-seo-case-study",
    "dhaka-apparels-seo-case-study",
    "hiring-seo-expert-dhaka-better-roi-than-paid-ads",
    "locksmith-dundee-seo-case-study",
    "mir-cement-seo-case-study",
    "morethanpanel-seo-case-study",
    "seo-case-study-dhaka-businesses-increased-organic-traffic",
    "seo-expert-vs-seo-agency-dhaka-which-is-right",
    "seo-featured-snippet-bangladesh",
    "seo-knowledge-panel-bangladesh",
    "smmgen-seo-case-study",
    "smmsun-seo-case-study",
    "stealth-windshield-repairs-seo-case-study",
    "top-10-seo-mistakes-dhaka-businesses-fix",
    "watchzonebd-seo-case-study",
]

def extract_primary_keyword(title):
    """Extract primary keyword from title."""
    title_lower = title.lower().strip()
    
    # Remove leading articles and common prefixes
    cleaned = re.sub(r'^(what is |what are |how to |why |the |a |an |complete |understanding )', '', title_lower)
    
    # For Bengali titles, take first meaningful phrase
    if re.search(r'[\u0980-\u09FF]', cleaned):
        # Bengali - take first meaningful keyword
        words = cleaned.split()
        stop_words = {'একটি', 'এবং', 'কীভাবে', 'জন্য', 'থেকে', 'করে', 'হবে', 'করা', 'কেন', 'বনাম', 'বাংলায়', 'নিয়ে'}
        keywords = [w for w in words if w not in stop_words and len(w) > 1][:2]
        return ' '.join(keywords) if keywords else words[0] if words else title
    
    # English - extract first meaningful noun phrase
    words = cleaned.split()
    stop_words = {'is', 'are', 'for', 'in', 'of', 'to', 'and', 'the', 'a', 'an', 'your', 'its', 'their', 'our', 'vs', 'or', 'that', 'with', 'from', 'by', 'on', 'at', 'be', 'it', 'as', 'but', 'not'}
    keywords = []
    for w in words[:6]:
        w_clean = w.strip('?:!.,;()[]{}""\'')
        if w_clean not in stop_words and len(w_clean) > 2:
            keywords.append(w_clean)
            if len(keywords) >= 3:
                break
    
    if not keywords:
        keywords = [w.strip('?:!.,;()[]{}""\'') for w in words[:2] if len(w.strip('?:!.,;()[]{}""\'')) > 0]
    
    return ' '.join(keywords) if keywords else title

def count_keyword(content, keyword):
    """Count case-insensitive occurrences."""
    if not keyword or not content:
        return 0
    return len(re.findall(re.escape(keyword), content, re.IGNORECASE))

def check_entities(post):
    """Check entity coverage."""
    content_lower = post['content'].lower()
    title_lower = post['title'].lower()
    tags_lower = [t.lower() for t in post.get('tags', [])]
    
    present = []
    missing = []
    
    # Location entities
    location_checks = {
        'bangladesh': 'Bangladesh',
        'dhaka': 'Dhaka',
    }
    
    for key, name in location_checks.items():
        if key in content_lower or key in title_lower:
            present.append(name)
        else:
            missing.append(name)
    
    # Service type based on tags and content
    service_map = {
        'seo': 'SEO',
        'local seo': 'Local SEO',
        'technical seo': 'Technical SEO',
        'ecommerce': 'E-commerce SEO',
        'link building': 'Link Building',
        'content marketing': 'Content Marketing',
        'mobile seo': 'Mobile SEO',
        'google business profile': 'Google Business Profile',
    }
    
    found_services = []
    for key, name in service_map.items():
        if key in content_lower or any(key in t for t in tags_lower):
            found_services.append(name)
    
    if found_services:
        present.extend(found_services[:2])
    else:
        missing.append('Service type')
    
    # Author entity
    author_terms = ['kanok', 'kanok miah', 'md kanok miah']
    has_author = any(t in content_lower for t in author_terms)
    if has_author:
        present.append('Kanok Miah')
    else:
        missing.append('Kanok Miah (author)')
    
    # Industry entity
    industry_map = {
        'real estate': 'Real Estate',
        'healthcare': 'Healthcare',
        'education': 'Education',
        'restaurant': 'Food/Restaurant',
        'ecommerce': 'E-commerce',
        'garment': 'Garments/Textile',
        'cleaning': 'Cleaning Services',
    }
    
    found_industries = []
    for key, name in industry_map.items():
        if key in content_lower:
            found_industries.append(name)
    
    if found_industries:
        present.extend(found_industries[:1])
    else:
        # Not required for every post
        pass
    
    return present, missing

def check_aeo(content):
    """Count question-based headings."""
    headings = re.findall(r'^#{2,4}\s+(How|What|Why|When|Where|Can|Do|Is|Are|Does|Will|Should|Would|Which|Who)\b', content, re.MULTILINE)
    return len(headings)

def count_internal_links(content):
    """Count internal links (pattern: [text](/path))."""
    links = re.findall(r'\[([^\]]+)\]\((\/[^)]+)\)', content)
    return len(links)

def check_schema(post):
    """Check schema readiness."""
    missing = []
    if not post.get('title'): missing.append('title')
    if not post.get('excerpt'): missing.append('excerpt')
    if not post.get('date'): missing.append('date')
    if not post.get('dateModified'): missing.append('dateModified')
    return missing

def check_pillar_link(post):
    """Check if post links to pillar pages."""
    content = post['content']
    
    pillar_pages = [
        ('Complete SEO Guide', '/blog/complete-seo-guide-bangladesh-businesses-2026'),
        ('Local SEO Guide', '/blog/local-seo-tips-dhaka-businesses-google-maps'),
        ('Technical SEO', '/blog/technical-seo-checklist-bangladeshi-websites'),
        ('E-commerce SEO', '/blog/why-ecommerce-store-needs-seo-bangladesh'),
        ('Link Building', '/blog/link-building-strategies-bangladesh-market'),
        ('Mobile SEO', '/blog/mobile-seo-optimization-bangladesh-mobile-first-era'),
        ('Content Marketing', '/blog/content-marketing-strategy-bangladeshi-brands-seo'),
        ('Real Estate SEO', '/blog/seo-real-estate-developers-dhaka'),
        ('International SEO', '/blog/international-seo-bangladesh-exporters-global-buyers'),
        ('Garments SEO', '/blog/seo-garments-textile-industry-b2b-lead-generation'),
        ('GBP Guide', '/blog/google-business-profile-optimization-guide-bangladesh'),
    ]
    
    # Find which pillars are linked
    linked_pillars = []
    for name, url in pillar_pages:
        slug = url.split('/')[-1]
        if slug in content or url in content:
            linked_pillars.append(name)
    
    return linked_pillars

def analyze_post(post):
    """Run all framework checks on one post."""
    content = post['content']
    title = post['title']
    tags = post.get('tags', [])
    
    if not content or len(content) < 50:
        return {
            'slug': post['slug'],
            'title': title,
            'error': 'Content too short or missing',
            'all_pass': False,
        }
    
    # A. TF-IDF Coverage
    keyword = extract_primary_keyword(title)
    kw_count = count_keyword(content, keyword)
    tfidf_pass = kw_count >= 5
    if not tfidf_pass:
        # Try with simplified keyword (first meaningful word)
        simpler = keyword.split()[0] if keyword.split() else keyword
        if simpler != keyword:
            kw_count2 = count_keyword(content, simpler)
            if kw_count2 >= 5:
                tfidf_pass = True
                kw_count = kw_count2
    
    # B. Entities
    present_entities, missing_entities = check_entities(post)
    entities_pass = len(missing_entities) == 0
    
    # C. Pillar links
    linked_pillars = check_pillar_link(post)
    pillar_pass = len(linked_pillars) > 0
    
    # D. AEO/GEO
    question_count = check_aeo(content)
    aeo_pass = question_count >= 2
    
    # E. Internal linking
    internal_links = count_internal_links(content)
    linking_pass = internal_links >= 3
    
    # F. Schema
    schema_missing = check_schema(post)
    schema_pass = len(schema_missing) == 0
    
    all_pass = all([tfidf_pass, entities_pass, pillar_pass, aeo_pass, linking_pass, schema_pass])
    
    return {
        'slug': post['slug'],
        'title': title,
        'all_pass': all_pass,
        'checks': [
            ('TF-IDF: ' + keyword[:40], '✅' if tfidf_pass else '❌', f'{kw_count} occurrences'),
            ('Entities', '✅' if entities_pass else '❌', f'Missing: {", ".join(missing_entities)}' if missing_entities else 'Complete'),
            ('Pillar Link', '✅' if pillar_pass else '❌', f'Links to: {", ".join(linked_pillars)}' if linked_pillars else 'None found'),
            ('AEO/GEO', '✅' if aeo_pass else '❌', f'{question_count} question headings'),
            ('Internal Links', '✅' if linking_pass else '❌', f'{internal_links} total'),
            ('Schema Ready', '✅' if schema_pass else '❌', f'Missing: {", ".join(schema_missing)}' if schema_missing else 'All fields set'),
        ],
        'tfidf_pass': tfidf_pass,
        'entities_pass': entities_pass,
        'pillar_pass': pillar_pass,
        'aeo_pass': aeo_pass,
        'linking_pass': linking_pass,
        'schema_pass': schema_pass,
        'keyword': keyword,
        'keyword_count': kw_count,
        'missing_entities': missing_entities,
        'linked_pillars': linked_pillars,
        'question_count': question_count,
        'internal_links': internal_links,
        'schema_missing': schema_missing,
    }

def print_fixes(r):
    """Print fix instructions for a failing post."""
    fixes = []
    if not r.get('tfidf_pass'):
        fixes.append(f"- ⚠ Keyword '{r['keyword']}' only appears {r['keyword_count']} times (need ≥5). Add more natural occurrences in content body.")
    if not r.get('entities_pass'):
        fixes.append(f"- ⚠ Missing entity references: {', '.join(r['missing_entities'])}. Mention these naturally in the content.")
    if not r.get('pillar_pass'):
        fixes.append("- ⚠ No pillar page link found. Add a contextual link to the relevant pillar guide (e.g., /blog/complete-seo-guide-bangladesh-businesses-2026).")
    if not r.get('aeo_pass'):
        fixes.append(f"- ⚠ Only {r['question_count']} question-based headings (need ≥2). Add FAQ sections or how-to headings starting with How, What, Why, etc.")
    if not r.get('linking_pass'):
        fixes.append(f"- ⚠ Only {r['internal_links']} internal links (need ≥3). Add more contextual links to other posts, services, or location pages.")
    if not r.get('schema_pass'):
        fixes.append(f"- ⚠ Missing schema fields: {', '.join(r['schema_missing'])}. Add these to the post metadata for ArticleSchema.")
    return fixes

def main():
    print("=" * 76)
    print("  CONTENT FRAMEWORK ENFORCER — kanokmiah.com.bd")
    print("  Framework check for posts modified in last 48 hours")
    print("=" * 76)
    
    modified = [s for s in MODIFIED_SLUGS if s in POSTS_BY_SLUG]
    not_found = [s for s in MODIFIED_SLUGS if s not in POSTS_BY_SLUG]
    
    if not_found:
        print(f"\n⚠  Posts not found in extract: {not_found}")
    
    print(f"\n📝 Analyzing {len(modified)} modified posts...\n")
    
    results = []
    for slug in modified:
        post = POSTS_BY_SLUG[slug]
        result = analyze_post(post)
        results.append(result)
        
        print(f"## Post: {result['slug']}")
        print(f"**Title:** {result['title']}")
        if result.get('error'):
            print(f"⚠  ERROR: {result['error']}")
            continue
        print(f"| Check | Status | Details |")
        print(f"|-------|--------|---------|")
        for check_name, status, details in result['checks']:
            print(f"| {check_name} | {status} | {details} |")
        
        if not result['all_pass']:
            fixes = print_fixes(result)
            print(f"\n### Fix instructions:")
            for f in fixes:
                print(f)
        print()
    
    # Summary
    passing = [r for r in results if r.get('all_pass')]
    failing = [r for r in results if r.get('all_pass') == False]
    
    print("=" * 76)
    print(f"📊 FRAMEWORK SUMMARY")
    print(f"   Total modified posts: {len(results)}")
    print(f"   ✅ Passing all checks: {len(passing)}")
    print(f"   ❌ Failing one or more: {len(failing)}")
    print()
    
    if failing:
        print("### ❌ Posts Requiring Fixes")
        for r in failing:
            failed_checks = []
            if not r.get('tfidf_pass'): failed_checks.append('TF-IDF')
            if not r.get('entities_pass'): failed_checks.append('Entities')
            if not r.get('pillar_pass'): failed_checks.append('Pillar')
            if not r.get('aeo_pass'): failed_checks.append('AEO/GEO')
            if not r.get('linking_pass'): failed_checks.append('Links')
            if not r.get('schema_pass'): failed_checks.append('Schema')
            print(f"  - [{', '.join(failed_checks)}] {r['slug']}")
    
    if passing:
        print("\n### ✅ Posts Passing All Checks")
        for r in passing:
            print(f"  - {r['slug']}")

if __name__ == '__main__':
    main()
