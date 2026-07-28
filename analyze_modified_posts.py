#!/usr/bin/env python3
"""
Analyze only the 17 modified blog posts for framework compliance.
"""
import re
import json
import sys

# Read data.js
with open('/root/kanok-miahit/src/app/blog/data.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

# Extract the posts array
# Find the start and end of the posts array
array_start = js_content.find('const posts = [')
if array_start == -1:
    print("ERROR: Could not find 'const posts = ['")
    sys.exit(1)

# Find the matching closing bracket - start from array_start and count brackets
depth = 0
array_end = array_start
for i in range(array_start, len(js_content)):
    if js_content[i] == '[':
        depth += 1
    elif js_content[i] == ']':
        depth -= 1
        if depth == 0:
            array_end = i + 1
            break

if depth != 0:
    print("ERROR: Unbalanced brackets")
    sys.exit(1)

array_text = js_content[array_start:array_end]

# Extract post objects by splitting on /\s*},\s*{\s*slug:/
# First, split into individual post strings
# Find all slug occurrences
slug_pattern = re.compile(r"slug:\s*\"([^\"]+)\"", re.IGNORECASE)
all_slugs = slug_pattern.findall(array_text)
print(f"Total posts found in array: {len(all_slugs)}")

# Target slugs (the 17 modified ones)
target_slugs = [
    "geo-optimization-prepare-business-ai-search",
    "seo-garments-textile-industry-b2b-lead-generation",
    "seo-healthcare-medical-clinics-bangladesh",
    "locksmith-dundee-seo-case-study",
    "landlord-certificates-seo-case-study",
    "das-taxis-scotland-seo-case-study",
    "morethanpanel-seo-case-study",
    "smmgen-seo-case-study",
    "smmsun-seo-case-study",
    "mir-cement-seo-case-study",
    "dhaka-apparels-seo-case-study",
    "stealth-windshield-repairs-seo-case-study",
    "seo-expert-vs-seo-agency-dhaka-which-is-right",
    "top-10-seo-mistakes-dhaka-businesses-fix",
    "seo-case-study-dhaka-businesses-increased-organic-traffic",
    "hiring-seo-expert-dhaka-better-roi-than-paid-ads",
    "watchzonebd-seo-case-study"
]

# Now extract each post object based on slug
# Split the array by post objects
# Posts start with { and end with }, followed by next post or array end
posts_text = array_text[len("const posts = "):]  # Remove the const declaration

# Parse posts by finding slug: "..." patterns and extracting their full objects
# Use simple approach: find each slug and extract the enclosing object
result_posts = []

for slug in target_slugs:
    # Find this slug in the array text
    idx = array_text.find(f'slug: "{slug}"')
    if idx == -1:
        print(f"WARNING: Could not find slug: {slug}")
        continue
    
    # Find the start of this post object (go back to find { before slug)
    post_start = idx
    while post_start > 0:
        post_start -= 1
        if array_text[post_start] == '{':
            # Check this is the start of a post (not a nested object)
            before = array_text[max(0,post_start-20):post_start].strip()
            if before == '' or before.endswith('[') or before.endswith(','):
                break
    
    # Find the end of this post object (balance braces from post_start)
    brace_depth = 0
    post_end = post_start
    found_start = False
    for i in range(post_start, len(array_text)):
        if array_text[i] == '{':
            brace_depth += 1
            found_start = True
        elif array_text[i] == '}':
            brace_depth -= 1
            if found_start and brace_depth == 0:
                post_end = i + 1
                break
    
    post_text = array_text[post_start:post_end]
    result_posts.append(post_text)

print(f"\nExtracted {len(result_posts)} post objects")

# Now analyze each post
def extract_field(post_text, field_name):
    """Extract a field value from a post's text representation."""
    # Match field_name: "value" or field_name: `value`
    patterns = [
        rf'{field_name}:\s*"((?:[^"\\]|\\.)*)"',
        rf'{field_name}:\s*`((?:[^`]|\\`)*)`',
    ]
    for pat in patterns:
        m = re.search(pat, post_text, re.DOTALL)
        if m:
            return m.group(1)
    return None

def extract_tags(post_text):
    """Extract tags array."""
    m = re.search(r'tags:\s*\[(.*?)\]', post_text, re.DOTALL)
    if m:
        tags_str = m.group(1)
        tags = re.findall(r'"([^"]+)"', tags_str)
        return tags
    return []

def extract_content(post_text):
    """Extract the content string."""
    m = re.search(r'content:\s*`((?:[^`]|\\`)*)`', post_text, re.DOTALL)
    if m:
        return m.group(1)
    return ""

def analyze_post(post_text, slug):
    """Run framework checks on a single post."""
    slug_from_text = extract_field(post_text, 'slug') or slug
    title = extract_field(post_text, 'title') or "Unknown"
    excerpt = extract_field(post_text, 'excerpt') or ""
    date = extract_field(post_text, 'date') or ""
    author = extract_field(post_text, 'author') or ""
    tags = extract_tags(post_text)
    content = extract_content(post_text)
    
    results = {
        'slug': slug_from_text,
        'title': title,
        'checks': {}
    }
    
    # A. TF-IDF Coverage
    # Extract primary keyword from title (first meaningful noun phrase)
    title_lower = title.lower()
    # Remove common prefixes
    for prefix in ['how to ', 'why ', 'what is ', 'top ', 'complete ']:
        if title_lower.startswith(prefix):
            title_lower = title_lower[len(prefix):]
            break
    
    # Extract first 2-3 meaningful words
    words = re.findall(r'[a-z]+', title_lower)
    # Skip very short words and common stop words
    stop_words = {'for', 'the', 'and', 'your', 'in', 'of', 'to', 'a', 'an', 'is', 'are', 'vs', 'or', 'from'}
    meaningful = [w for w in words if w not in stop_words and len(w) > 2]
    
    if len(meaningful) >= 2:
        # Primary keyword is first 2 meaningful words
        pk = f"{meaningful[0]} {meaningful[1]}"
    elif meaningful:
        pk = meaningful[0]
    else:
        pk = words[0] if words else ""
    
    # Also try with first 3 words
    if len(meaningful) >= 3:
        pk3 = f"{meaningful[0]} {meaningful[1]} {meaningful[2]}"
    else:
        pk3 = pk
    
    content_lower = content.lower()
    pk_count = content_lower.count(pk)
    pk3_count = content_lower.count(pk3) if pk3 != pk else pk_count
    
    # Use the better match
    best_pk = pk3 if pk3_count > pk_count else pk
    best_count = max(pk_count, pk3_count)
    
    results['checks']['tfidf'] = {
        'keyword': best_pk,
        'occurrences': best_count,
        'passed': best_count >= 5,
        'details': f"Primary keyword '{best_pk}' appears {best_count} times"
    }
    
    # B. Entity Coverage
    locations_found = []
    for loc in ['dhaka', 'bangladesh', 'chittagong', 'sylhet', 'gulshan', 'dhanmondi', 'banani']:
        if loc in content_lower:
            locations_found.append(loc)
    
    # Determine industry from tags and content
    industry_keywords = {
        'garment': ['garment', 'textile', 'rmg', 'apparel', 'factory'],
        'healthcare': ['healthcare', 'medical', 'clinic', 'hospital', 'patient'],
        'ecommerce': ['ecommerce', 'e-commerce', 'online store', 'retail', 'shop'],
        'real_estate': ['real estate', 'property', 'apartment', 'developer'],
        'education': ['education', 'school', 'university', 'college', 'student'],
        'seo': ['seo', 'search engine', 'optimization', 'ranking', 'google'],
        'local': ['local', 'maps', 'gbp', 'google business'],
    }
    
    industries_found = {}
    for ind, kws in industry_keywords.items():
        for kw in kws:
            if kw in content_lower:
                industries_found[ind] = True
                break
    
    # Service entities
    service_keywords = ['service', 'optimization', 'consulting', 'audit', 'marketing', 'strategy']
    service_count = sum(1 for sk in service_keywords if sk in content_lower)
    
    missing_entities = []
    if not any(loc in ['dhaka', 'bangladesh'] for loc in locations_found):
        missing_entities.append("Primary location (Dhaka/Bangladesh)")
    if not industries_found:
        missing_entities.append("Industry-specific entities")
    if service_count < 3:
        missing_entities.append(f"Service entities (found {service_count}, need >=3)")
    
    results['checks']['entities'] = {
        'locations': locations_found,
        'industries': list(industries_found.keys()),
        'service_count': service_count,
        'passed': len(missing_entities) == 0,
        'details': f"Locations: {locations_found}, Industries: {list(industries_found.keys())}, Services: {service_count}",
        'missing': missing_entities
    }
    
    # C. Pillar Link
    # Determine expected pillar based on tags
    tag_lower = [t.lower() for t in tags]
    pillar_slugs = {
        'complete-seo-guide-bangladesh-businesses-2026': ['seo guide', 'bangladesh seo', 'digital marketing', 'seo'],
        'seo-garments-textile-industry-b2b-lead-generation': ['garments seo', 'textile industry', 'b2b seo', 'bangladesh rmg'],
        'seo-healthcare-medical-clinics-bangladesh': ['healthcare seo', 'medical seo', 'patient acquisition'],
        'geo-optimization-prepare-business-ai-search': ['geo', 'ai search', 'generative engine optimization'],
    }
    
    expected_pillar = 'complete-seo-guide-bangladesh-businesses-2026'  # Default
    for pslug, ptags in pillar_slugs.items():
        for pt in ptags:
            if pt in tag_lower:
                expected_pillar = pslug
                break
    
    # Check if post links to expected pillar
    pillar_links = []
    for link_pattern in [f'/blog/{expected_pillar}', f'/blog/{slug}']:
        if link_pattern in content:
            pillar_links.append(link_pattern)
    
    results['checks']['pillar'] = {
        'expected_pillar': expected_pillar,
        'pillar_links_found': pillar_links,
        'passed': len(pillar_links) > 0,
        'details': f"Expected pillar: {expected_pillar}, Links found: {pillar_links}"
    }
    
    # D. AEO/GEO Question Headings
    # Count question-based headings (## ... ?)
    q_headings = re.findall(r'^##[^#].*\?', content, re.MULTILINE)
    # Also count ### headings with questions
    q_headings += re.findall(r'^###[^#].*\?', content, re.MULTILINE)
    
    # Count all question marks in content
    q_marks = content.count('?')
    
    # Count FAQ patterns
    faq_sections = [h for h in q_headings if any(h.lower().startswith(s) for s in ['## what', '## how', '## why', '## when', '## where', '## can', '## do', '## is', '## are', '### what', '### how', '### why', '### when', '### where', '### can', '### do', '### is', '### are'])]
    
    results['checks']['aeo_geo'] = {
        'question_headings': len(q_headings),
        'question_marks_in_content': q_marks,
        'passed': len(q_headings) >= 2,
        'details': f"{len(q_headings)} question-based headings, {q_marks} total question marks"
    }
    
    # E. Internal Links
    blog_links = re.findall(r'/blog/[a-z0-9-]+', content)
    services_links = re.findall(r'/services/[a-z0-9-]+', content)
    industries_links = re.findall(r'/industries/[a-z0-9-]+', content)
    locations_links = re.findall(r'/locations/[a-z0-9-]+', content)
    
    all_links = blog_links + services_links + industries_links + locations_links
    unique_links = list(set(all_links))
    
    results['checks']['internal_links'] = {
        'blog_links': len(blog_links),
        'services_links': len(services_links),
        'industries_links': len(industries_links),
        'locations_links': len(locations_links),
        'total_links': len(all_links),
        'unique_links': len(unique_links),
        'passed': len(unique_links) >= 3,
        'details': f"{len(unique_links)} unique internal links ({len(blog_links)} blog, {len(services_links)} services, {len(industries_links)} industries, {len(locations_links)} locations)"
    }
    
    # F. Schema Readiness
    schema_checks = {
        'title': bool(title and len(title) > 5),
        'excerpt': bool(excerpt and len(excerpt) > 20),
        'date': bool(date),
        'author': bool(author),
        'tags': len(tags) >= 2,
    }
    
    missing_fields = [k for k, v in schema_checks.items() if not v]
    
    results['checks']['schema'] = {
        'checks': schema_checks,
        'missing_fields': missing_fields,
        'passed': len(missing_fields) == 0,
        'details': f"All fields set" if not missing_fields else f"Missing: {missing_fields}"
    }
    
    # Overall
    total_flags = sum(1 for c in results['checks'].values() if not c['passed'])
    results['total_flags'] = total_flags
    
    return results

# Run analysis
all_results = []
for pt in result_posts:
    slug = extract_field(pt, 'slug') or "unknown"
    results = analyze_post(pt, slug)
    all_results.append(results)

# Print report
print("\n" + "="*80)
print("CONTENT FRAMEWORK ENFORCEMENT REPORT — Modified Posts Only")
print("="*80)
print(f"Posts Analyzed: {len(all_results)}")
print(f"Date: 2026-07-26")
print()

# Summary table
print(f"{'Slug':<55} {'T':<3} {'E':<3} {'P':<3} {'A':<3} {'I':<3} {'S':<3} {'Flags':<5}")
print("-"*80)
for r in all_results:
    c = r['checks']
    t = '✅' if c['tfidf']['passed'] else '❌'
    e = '✅' if c['entities']['passed'] else '❌'
    p = '✅' if c['pillar']['passed'] else '❌'
    a = '✅' if c['aeo_geo']['passed'] else '❌'
    i = '✅' if c['internal_links']['passed'] else '❌'
    s = '✅' if c['schema']['passed'] else '❌'
    name = r['slug'][:54]
    print(f"{name:<55} {t:<3} {e:<3} {p:<3} {a:<3} {i:<3} {s:<3} {r['total_flags']}")

print()
flagged = [r for r in all_results if r['total_flags'] > 0]
print(f"\nTotal flags across all modified posts: {sum(r['total_flags'] for r in all_results)}")
print(f"Posts with flags: {len(flagged)}")
print(f"Fully passing posts: {len(all_results) - len(flagged)}")

# Detailed per-post
for r in all_results:
    print("\n" + "="*80)
    print(f"  {r['title']}")
    print(f"  Slug: {r['slug']}")
    print("="*80)
    print(f"  OVERALL: {r['total_flags']}/6 checks flagged")
    
    c = r['checks']
    
    print(f"\n  A. TF-IDF COVERAGE: {'✅ PASS' if c['tfidf']['passed'] else '❌ FLAGGED'}")
    print(f"     Keyword: '{c['tfidf']['keyword']}' — {c['tfidf']['occurrences']} occurrences (threshold: 5)")
    
    print(f"\n  B. ENTITY COVERAGE: {'✅ PASS' if c['entities']['passed'] else '❌ FLAGGED'}")
    print(f"     Locations: {c['entities']['locations']}")
    print(f"     Industries: {c['entities']['industries']}")
    print(f"     Service count: {c['entities']['service_count']}")
    if not c['entities']['passed']:
        print(f"     Missing: {c['entities']['missing']}")
    
    print(f"\n  C. PILLAR LINK: {'✅ PASS' if c['pillar']['passed'] else '❌ FLAGGED'}")
    print(f"     Expected pillar: {c['pillar']['expected_pillar']}")
    print(f"     Links found: {c['pillar']['pillar_links_found']}")
    
    print(f"\n  D. AEO/GEO: {'✅ PASS' if c['aeo_geo']['passed'] else '❌ FLAGGED'}")
    print(f"     Question headings: {c['aeo_geo']['question_headings']} (threshold: 2)")
    print(f"     Question marks in content: {c['aeo_geo']['question_marks_in_content']}")
    
    print(f"\n  E. INTERNAL LINKS: {'✅ PASS' if c['internal_links']['passed'] else '❌ FLAGGED'}")
    print(f"     Blog links: {c['internal_links']['blog_links']}")
    print(f"     Service links: {c['internal_links']['services_links']}")
    print(f"     Industry links: {c['internal_links']['industries_links']}")
    print(f"     Location links: {c['internal_links']['locations_links']}")
    print(f"     Total unique: {c['internal_links']['unique_links']} (threshold: 3)")
    
    print(f"\n  F. SCHEMA READINESS: {'✅ PASS' if c['schema']['passed'] else '❌ FLAGGED'}")
    print(f"     Title: {c['schema']['checks']['title']}")
    print(f"     Excerpt: {c['schema']['checks']['excerpt']}")
    print(f"     Date: {c['schema']['checks']['date']}")
    print(f"     Author: {c['schema']['checks']['author']}")
    print(f"     Tags (>=2): {c['schema']['checks']['tags']}")
    if c['schema']['missing_fields']:
        print(f"     Missing fields: {c['schema']['missing_fields']}")

# If all pass, short summary
all_pass = all(r['total_flags'] == 0 for r in all_results)
if all_pass:
    print("\n" + "="*80)
    print("✅ ALL 17 MODIFIED POSTS PASS ALL 6 FRAMEWORK CHECKS")
    print("="*80)
else:
    print("\n" + "="*80)
    print("⚠️  FLAGGED POSTS SUMMARY")
    print("="*80)
    for r in flagged:
        print(f"\n  🟡 {r['slug']} — {r['total_flags']} flag(s)")
        c = r['checks']
        if not c['tfidf']['passed']:
            print(f"     ❌ TF-IDF: '{c['tfidf']['keyword']}' only {c['tfidf']['occurrences']} occurrences")
        if not c['pillar']['passed']:
            print(f"     ❌ Pillar: Missing link to {c['pillar']['expected_pillar']}")
        if not c['entities']['passed']:
            print(f"     ❌ Entities: {c['entities']['missing']}")
        if not c['aeo_geo']['passed']:
            print(f"     ❌ AEO/GEO: Only {c['aeo_geo']['question_headings']} question headings")
        if not c['internal_links']['passed']:
            print(f"     ❌ Internal Links: Only {c['internal_links']['unique_links']} unique links")
        if not c['schema']['passed']:
            print(f"     ❌ Schema: {c['schema']['details']}")

# Save results
output = {
    'posts_analyzed': len(all_results),
    'total_flags': sum(r['total_flags'] for r in all_results),
    'flagged_posts': [r['slug'] for r in flagged],
    'all_pass': all_pass,
    'posts': all_results
}

with open('/root/kanok-miahit/framework_analysis_modified.json', 'w') as f:
    json.dump(output, f, indent=2)

print(f"\n\nResults saved to framework_analysis_modified.json")
