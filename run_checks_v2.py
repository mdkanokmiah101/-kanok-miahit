#!/usr/bin/env python3
"""
Content Framework Checks for 40 modified blog posts.
Robust parser for JS data file with template literals.
"""
import re
import json

def parse_posts(filepath):
    """Parse blog posts from JS data file, handling template literals with backticks."""
    with open(filepath, 'r') as f:
        source = f.read()
    
    # Find all post objects. Each starts with `{` and ends with `},`
    # We need to parse with awareness of:
    #   - Double-quoted strings: "..."
    #   - Template literals: `...`
    #   - Nested braces inside template literals and strings
    
    posts = []
    i = 0
    in_post = False
    brace_depth = 0
    post_start = 0
    in_double_quote = False
    in_backtick = False
    
    while i < len(source):
        c = source[i]
        
        # Track string literals
        if c == '"' and not in_backtick:
            # Check if escaped
            if i == 0 or source[i-1] != '\\':
                in_double_quote = not in_double_quote
        elif c == '`' and not in_double_quote:
            # Check if escaped (unlikely in template literals but be safe)
            if i == 0 or source[i-1] != '\\':
                in_backtick = not in_backtick
        elif not in_double_quote and not in_backtick:
            if c == '{':
                if brace_depth == 0:
                    # This could be a post start - check if it has "slug:"
                    # We'll capture from here
                    post_start = i
                brace_depth += 1
            elif c == '}':
                brace_depth -= 1
                if brace_depth == 0 and post_start > 0:
                    # End of a post object
                    post_str = source[post_start:i+1]
                    if '"slug"' in post_str.replace("'", '"') or 'slug:' in post_str:
                        posts.append(post_str)
                    post_start = 0
        
        i += 1
    
    return posts

def extract_str_field(post_str, field_name):
    """Extract a simple string field value from a post string."""
    # Match field: "value" (double-quoted)
    m = re.search(rf'{field_name}\s*:\s*"((?:[^"\\]|\\.)*)"', post_str)
    if m:
        return m.group(1)
    # Match field: "value" that spans multiple lines (excerpt style)
    m = re.search(rf'{field_name}\s*:\s*\n\s*"((?:[^"\\]|\\.)*)"', post_str)
    if m:
        return m.group(1)
    return None

def extract_tags(post_str):
    """Extract tags array."""
    m = re.search(r'tags\s*:\s*\[((?:[^\[\]]*))\],', post_str, re.DOTALL)
    if m:
        tags_str = m.group(1)
        return re.findall(r'"([^"]*)"', tags_str)
    return []

def extract_content(post_str):
    """Extract content from template literal (backtick string)."""
    m = re.search(r'content\s*:\s*`((?:[^`]|`(?!,|\s*\}))*)`', post_str, re.DOTALL)
    if m:
        return m.group(1)
    # Alternative: content: `...` with potential trailing comma/brace
    m = re.search(r'content\s*:\s*`([^`]*)`', post_str, re.DOTALL)
    if m:
        return m.group(1)
    return ""

def get_primary_keyword(title):
    """Extract primary keyword from title - first meaningful noun phrase."""
    if not title:
        return ""
    title_lower = title.lower()
    
    # Special cases for known post types
    if 'best seo expert in dhaka' in title_lower:
        return 'SEO expert'
    if 'case study' in title_lower or 'seo case study' in title_lower:
        # Extract the main service type
        for svc in ['taxis', 'locksmith', 'landlord certificates', 'panel beating',
                     'windshield', 'cement', 'apparel', 'social media']:
            if svc in title_lower:
                return svc
        return 'case study'
    if 'geo optimization' in title_lower:
        return 'GEO optimization'
    if 'google business profile' in title_lower:
        return 'Google Business Profile'
    if 'faq schema' in title_lower:
        return 'FAQ schema'
    if 'howto schema' in title_lower:
        return 'HowTo schema'
    if 'breadcrumb schema' in title_lower:
        return 'breadcrumb schema'
    if 'json-ld schema' in title_lower:
        return 'JSON-LD schema'
    if 'structured data' in title_lower:
        return 'structured data'
    if 'hreflang' in title_lower:
        return 'hreflang'
    if 'xml sitemap' in title_lower:
        return 'XML sitemap'
    if 'robots.txt' in title_lower:
        return 'robots.txt'
    if 'link building' in title_lower:
        return 'link building'
    if 'backlink outreach' in title_lower:
        return 'backlink outreach'
    if 'technical seo' in title_lower:
        return 'technical SEO'
    if 'mobile seo' in title_lower:
        return 'mobile SEO'
    if 'local seo' in title_lower:
        return 'local SEO'
    if 'enterprise seo' in title_lower:
        return 'enterprise SEO'
    if 'blogging strategy' in title_lower:
        return 'blogging strategy'
    if 'seo roadmap' in title_lower:
        return 'SEO roadmap'
    if 'complete seo guide' in title_lower:
        return 'SEO guide'
    if 'ecommerce' in title_lower or 'e-commerce' in title_lower:
        return 'e-commerce SEO'
    if 'seo vs google ads' in title_lower:
        return 'SEO vs Google Ads'
    if 'seo vs ppc' in title_lower:
        return 'SEO vs PPC'
    if 'choose right seo agency' in title_lower:
        return 'SEO agency'
    if 'garments' in title_lower or 'textile' in title_lower:
        return 'Garments/textile SEO'
    if 'event management' in title_lower:
        return 'event SEO'
    if 'non-profit' in title_lower:
        return 'non-profit SEO'
    if 'photographers' in title_lower or 'videographers' in title_lower:
        return 'photographer SEO'
    if 'wedding' in title_lower and 'event' in title_lower:
        return 'wedding SEO'
    if 'real estate' in title_lower:
        return 'real estate SEO'
    if 'multiple business locations' in title_lower:
        return 'local SEO'
    
    # Generic fallback: take first 2-3 significant words
    stop_words = {'a', 'an', 'the', 'for', 'in', 'of', 'to', 'and', 'or', 'is', 'are',
                  'your', 'our', 'their', 'its', 'it', 'this', 'that', 'at', 'by',
                  'with', 'from', 'on', 'as', 'be', 'has', 'have', 'do', 'does',
                  'complete', 'ultimate', 'essential', 'guide', 'tips', 'strategies',
                  'checklist', 'how', 'what', 'why', 'when', 'where', 'which', 'who',
                  'best', 'top', 'vs', 'needs', 'businesses', 'business', 'should',
                  'you', 'need', 'can', 'will', 'all', 'more'}
    words = title_lower.split()
    significant = [w for w in words if w not in stop_words and len(w) > 2 and w.isalpha()]
    if len(significant) >= 1:
        return ' '.join(significant[:2])
    return title_lower.strip()

def check_tfidf(content, keyword):
    """Check keyword density - count keyword occurrences."""
    if not keyword or not content:
        return 0
    content_lower = content.lower()
    keyword_lower = keyword.lower()
    # Use word boundary for single words, partial for compound
    if ' ' in keyword_lower:
        count = content_lower.count(keyword_lower)
    else:
        # For single words, use word boundary to avoid partial matches
        count = len(re.findall(r'\b' + re.escape(keyword_lower) + r'\b', content_lower))
    return count

def check_entities(content, slug, title):
    """Check entity coverage: location, service type, industry."""
    content_lower = content.lower()
    missing = []
    
    # 1. Location check
    has_dhaka = 'dhaka' in content_lower
    has_bangladesh = 'bangladesh' in content_lower
    has_scotland = 'scotland' in content_lower
    has_dundee = 'dundee' in content_lower
    
    is_case_study = 'case-study' in slug
    
    if is_case_study:
        if 'scotland' in slug or 'dundee' in slug:
            if not has_scotland and not has_dundee:
                missing.append("Location (Scotland/Dundee)")
        elif 'dhaka' in slug:
            if not has_dhaka:
                missing.append("Location (Dhaka)")
        else:
            if not has_dhaka and not has_bangladesh:
                missing.append("Location (Dhaka/Bangladesh)")
    else:
        if not has_dhaka and not has_bangladesh:
            missing.append("Location (Dhaka/Bangladesh)")
    
    # 2. Service type check
    service_topics = {
        'local-seo-tips': 'local SEO',
        'local-seo-multiple': 'local SEO',
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
        'seo-dashboard-tools': 'seo',
    }
    
    for key, service in service_topics.items():
        if slug.startswith(key) or slug == key:
            if service not in content_lower:
                missing.append(f"Service topic ({service})")
            break
    
    # 3. Industry check
    industry_checks = {
        'seo-garments-textile': ['garment', 'textile', 'apparel', 'rmg'],
        'seo-real-estate': ['real estate', 'property', 'developer', 'builder'],
        'seo-event-management': ['event'],
        'seo-wedding-event': ['wedding'],
        'seo-non-profit': ['non-profit', 'ngo', 'charity'],
        'seo-photographers': ['photographer', 'photography', 'videographer'],
        'dhaka-apparels-seo': ['apparel', 'garment', 'clothing'],
        'mir-cement-seo': ['cement'],
        'locksmith-dundee-seo': ['locksmith'],
        'das-taxis-scotland-seo': ['taxi', 'cab'],
        'landlord-certificates-seo': ['landlord', 'gas safety', 'eicr'],
        'stealth-windshield-repairs-seo': ['windshield', 'auto glass'],
        'morethanpanel-seo': ['panel beater', 'collision'],
    }
    
    for key, industry_terms in industry_checks.items():
        if slug.startswith(key) or slug == key:
            found_industry = any(term.lower() in content_lower for term in industry_terms)
            if not found_industry:
                missing.append(f"Industry terms ({', '.join(industry_terms[:3])})")
            break
    
    return missing

def check_pillar_link(content, tags, slug):
    """Check if the post links to its main pillar/thematic page."""
    links = re.findall(r'\[([^\]]*)\]\(([^)]*)\)', content)
    
    pillar_mapping = {
        'seo-garments-textile': ['/industries/', '/blog/seo-garments'],
        'seo-event-management': ['/industries/event', '/blog/seo-event'],
        'seo-real-estate': ['/industries/real-estate'],
        'seo-photographers': ['/industries/', '/blog/seo-photographers'],
        'seo-wedding-event': ['/industries/', '/blog/seo-wedding'],
        'seo-non-profit': ['/industries/', '/blog/seo-non-profit'],
        'seo-breadcrumb-schema': ['/blog/seo-structured-data', '/blog/schema-markup'],
        'seo-howto-schema': ['/blog/seo-structured-data', '/blog/schema-markup'],
        'seo-faq-schema': ['/blog/seo-structured-data', '/blog/schema-markup'],
        'seo-json-ld-schema': ['/blog/seo-structured-data', '/blog/schema-markup'],
        'seo-structured-data-guide': ['/blog/schema-markup', '/blog/seo-json-ld'],
        'seo-hreflang-guide': ['/blog/international-seo'],
        'seo-robots-txt-guide': ['/blog/technical-seo'],
        'seo-xml-sitemap-guide': ['/blog/technical-seo'],
        'local-seo': ['/services/local-seo', '/locations/'],
        'technical-seo': ['/services/technical-seo'],
        'mobile-seo': ['/services/technical-seo'],
        'why-ecommerce-store-needs-seo': ['/industries/ecommerce'],
        'geo-optimization': ['/services/geo'],
        'how-to-choose-right-seo-agency': ['/services/'],
        'link-building': ['/services/link-building'],
        'backlink-outreach': ['/services/link-building'],
        'google-business-profile': ['/services/local-seo'],
        'seo-vs-google-ads': ['/services/'],
        'seo-vs-ppc': ['/services/'],
        'complete-seo-guide': ['/services/', '/industries/'],
        'enterprise-seo': ['/services/'],
        'blogging-strategy': ['/services/content-marketing'],
        'building-seo-roadmap': ['/services/'],
        'why-md-kanok-miah-is-the-best': ['/about', '/'],
        'landlord-certificates-seo': ['/case-studies/'],
        'das-taxis-scotland-seo': ['/case-studies/'],
        'locksmith-dundee-seo': ['/case-studies/'],
        'morethanpanel-seo': ['/case-studies/'],
        'smmgen-seo': ['/case-studies/'],
        'smmsun-seo': ['/case-studies/'],
        'mir-cement-seo': ['/case-studies/'],
        'dhaka-apparels-seo': ['/case-studies/'],
        'stealth-windshield-repairs-seo': ['/case-studies/'],
        'local-seo-multiple': ['/services/local-seo', '/locations/'],
        'seo-dashboard-tools': ['/services/'],
    }
    
    expected_pillar = []
    for key, links in pillar_mapping.items():
        if slug.startswith(key) or slug == key:
            expected_pillar = links
            break
    
    found_links = []
    for text, href in links:
        for expected in expected_pillar:
            if href.startswith(expected) or href.startswith('https://kanokmiah.com.bd' + expected):
                found_links.append(href)
                break
    
    return found_links, expected_pillar

def check_aeo_geo(content):
    """Count question-based headings."""
    headings = re.findall(r'^#{2,3}\s+(.+)$', content, re.MULTILINE)
    question_words = ['how', 'what', 'why', 'when', 'where', 'can', 'do', 'is', 'are', 'does', 'will', 'should']
    question_headings = []
    for h in headings:
        h_stripped = h.strip().lower()
        for qw in question_words:
            if h_stripped.startswith(qw):
                question_headings.append(h.strip())
                break
    return question_headings

def check_internal_links(content):
    """Count internal links to other pages/posts."""
    links = re.findall(r'\[([^\]]*)\]\(([^)]*)\)', content)
    internal_hrefs = set()
    
    # Skip self-referencing or empty links
    ignore = {'#', ''}
    
    for text, href in links:
        href = href.strip()
        # Skip anchors, empty, and non-standard links
        if href in ignore:
            continue
        # Internal: starts with /
        if href.startswith('/'):
            if len(href) > 1:  # ignore just '/'
                internal_hrefs.add(href)
        # Internal: contains our domain
        elif 'kanokmiah.com.bd' in href.lower():
            # Extract path
            path = '/' + '/'.join(href.split('/', 3)[3:]) if len(href.split('/')) > 3 else '/'
            internal_hrefs.add(path)
    
    return len(internal_hrefs), sorted(internal_hrefs)[:15]

def check_schema_readiness(post_data):
    """Check if post has all fields needed for ArticleSchema."""
    missing_fields = []
    if not post_data.get('title'):
        missing_fields.append('title')
    if not post_data.get('excerpt'):
        missing_fields.append('excerpt/description')
    if not post_data.get('date'):
        missing_fields.append('date')
    return missing_fields

# Main
filepath = '/root/kanok-miahit/src/app/blog/data.js'
all_posts = parse_posts(filepath)
print(f"Parsed {len(all_posts)} post objects")

# The 40 modified slugs
modified_slugs = [
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

# Parse all posts
parsed_posts = {}
for post_str in all_posts:
    slug = extract_str_field(post_str, 'slug')
    if slug:
        if slug in modified_slugs:
            title = extract_str_field(post_str, 'title')
            date = extract_str_field(post_str, 'date')
            author = extract_str_field(post_str, 'author')
            excerpt = extract_str_field(post_str, 'excerpt')
            tags = extract_tags(post_str)
            content = extract_content(post_str)
            parsed_posts[slug] = {
                'slug': slug,
                'title': title,
                'date': date,
                'author': author,
                'excerpt': excerpt,
                'tags': tags,
                'content': content
            }

print(f"Found {len(parsed_posts)} of 40 modified posts")
missing_slugs = [s for s in modified_slugs if s not in parsed_posts]
if missing_slugs:
    print(f"Missing: {missing_slugs}")

# Run checks
results = {}
for slug, post in parsed_posts.items():
    content = post.get('content', '')
    title = post.get('title', '')
    tags = post.get('tags', [])
    excerpt = post.get('excerpt', '')
    
    # A. TF-IDF
    keyword = get_primary_keyword(title)
    tfidf_count = check_tfidf(content, keyword)
    tfidf_pass = tfidf_count >= 5
    
    # B. Entities
    missing_entities = check_entities(content, slug, title)
    entities_pass = len(missing_entities) == 0
    
    # C. Pillar Link
    found_pillar_links, expected_pillar = check_pillar_link(content, tags, slug)
    pillar_pass = len(found_pillar_links) > 0
    
    # D. AEO/GEO
    question_headings = check_aeo_geo(content)
    aeo_pass = len(question_headings) >= 2
    
    # E. Internal Links
    internal_count, internal_examples = check_internal_links(content)
    il_pass = internal_count >= 3
    
    # F. Schema Readiness
    schema_missing = check_schema_readiness(post)
    schema_pass = len(schema_missing) == 0
    
    results[slug] = {
        'keyword': keyword,
        'tfidf_count': tfidf_count,
        'tfidf_pass': tfidf_pass,
        'missing_entities': missing_entities,
        'entities_pass': entities_pass,
        'found_pillar_links': found_pillar_links,
        'expected_pillar': expected_pillar,
        'pillar_pass': pillar_pass,
        'question_headings': [h[:60] for h in question_headings],
        'aeo_pass': aeo_pass,
        'internal_count': internal_count,
        'internal_examples': internal_examples,
        'schema_missing': schema_missing,
        'schema_pass': schema_pass,
    }

# Output
all_pass = 0
all_fail = 0
fail_counts = {'TF-IDF': 0, 'Entities': 0, 'Pillar Link': 0, 'AEO/GEO': 0, 'Internal Links': 0, 'Schema Readiness': 0}

for slug in modified_slugs:
    if slug not in results:
        print(f"❌ Post: {slug} — NOT FOUND in parsed data")
        all_fail += 1
        continue
    
    r = results[slug]
    checks = {
        'tfidf': r['tfidf_pass'],
        'entities': r['entities_pass'],
        'pillar': r['pillar_pass'],
        'aeo': r['aeo_pass'],
        'il': r['il_pass'],
        'schema': r['schema_pass'],
    }
    checks_passed = all(checks.values())
    
    if checks_passed:
        print(f"✅ Post: {slug} — all checks passed")
        all_pass += 1
    else:
        print(f"\n## Post: {slug}")
        print(f"title: {post['title'][:80]}...")
        print(f"| Check | Status | Details |")
        print(f"|-------|--------|---------|")
        
        tfidf_status = "✅" if r['tfidf_pass'] else "❌"
        print(f"| TF-IDF: '{r['keyword']}' | {tfidf_status} | {r['tfidf_count']} occurrences |")
        if not r['tfidf_pass']: fail_counts['TF-IDF'] += 1
        
        ent_status = "✅" if r['entities_pass'] else "❌"
        ent_detail = "All present" if r['entities_pass'] else f"Missing: {', '.join(r['missing_entities'])}"
        print(f"| Entities | {ent_status} | {ent_detail} |")
        if not r['entities_pass']: fail_counts['Entities'] += 1
        
        pill_status = "✅" if r['pillar_pass'] else "❌"
        if r['found_pillar_links']:
            pill_detail = f"Links to: {', '.join(r['found_pillar_links'][:3])}"
        elif r['expected_pillar']:
            pill_detail = f"No link found to {', '.join(r['expected_pillar'])}"
        else:
            pill_detail = "No pillar mapped for this post type"
        print(f"| Pillar Link | {pill_status} | {pill_detail} |")
        if not r['pillar_pass']: fail_counts['Pillar Link'] += 1
        
        aeo_status = "✅" if r['aeo_pass'] else "❌"
        qh_preview = '; '.join(r['question_headings'][:4])
        print(f"| AEO/GEO | {aeo_status} | {len(r['question_headings'])} question headings{f' ({qh_preview})' if qh_preview else ''} |")
        if not r['aeo_pass']: fail_counts['AEO/GEO'] += 1
        
        il_status = "✅" if r['il_pass'] else "❌"
        il_detail = f"{r['internal_count']} unique internal links"
        if r['internal_examples']:
            il_detail += f" (e.g. {', '.join(r['internal_examples'][:5])})"
        print(f"| Internal Links | {il_status} | {il_detail} |")
        if not r['il_pass']: fail_counts['Internal Links'] += 1
        
        sch_status = "✅" if r['schema_pass'] else "❌"
        sch_detail = "All fields set" if r['schema_pass'] else f"Missing: {', '.join(r['schema_missing'])}"
        print(f"| Schema Ready | {sch_status} | {sch_detail} |")
        if not r['schema_pass']: fail_counts['Schema Readiness'] += 1
        
        print(f"\n### Fix instructions:")
        fixes = []
        if not r['tfidf_pass']:
            fixes.append(f"- Increase usage of keyword '{r['keyword']}' in content (currently {r['tfidf_count']} occurrences, need ≥5)")
        if not r['entities_pass']:
            fixes.append(f"- Add missing entities: {', '.join(r['missing_entities'])}")
        if not r['pillar_pass']:
            if r['expected_pillar']:
                fixes.append(f"- Add internal link to pillar page: {', '.join(r['expected_pillar'])}")
            else:
                fixes.append(f"- Add internal link to relevant pillar/thematic page")
        if not r['aeo_pass']:
            fixes.append(f"- Add more question-based headings (## or ### starting with How/What/Why/etc.), currently {len(r['question_headings'])} (need ≥2)")
        if not r['il_pass']:
            fixes.append(f"- Add more internal links to other pages/posts (currently {r['internal_count']}, need ≥3)")
        if not r['schema_pass']:
            fixes.append(f"- Add missing schema fields: {', '.join(r['schema_missing'])}")
        for f in fixes:
            print(f)
        
        all_fail += 1

print(f"\n\n## SUMMARY")
print(f"Total posts checked: 40")
print(f"✅ All checks passed: {all_pass}")
print(f"❌ Some checks failed: {all_fail}")
print(f"Pass rate: {all_pass/40*100:.1f}% ({all_pass}/40)")

print(f"\n### Failure breakdown:")
for check, count in fail_counts.items():
    print(f"  {check}: {count} posts failing")
