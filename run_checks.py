#!/usr/bin/env python3
"""
Content Framework Checks for 40 modified blog posts.
Checks: TF-IDF keyword density, entity coverage, pillar-cluster alignment,
        AEO/GEO question headings, internal linking count, schema readiness.
"""
import re
import json
import math
from collections import Counter

# Load the data.js file
with open('/root/kanok-miahit/src/app/blog/data.js', 'r') as f:
    raw = f.read()

# The file is a JS module export. We'll parse it by extracting post objects.
# Each post is: { slug: "...", title: "...", date: "...", author: "...", excerpt: "...", tags: [...], content: `...` }
# We'll parse aggressively by splitting on "slug:"

# Strategy: use a state machine to extract each post
posts_raw = re.findall(r'\{(\s*slug\s*:\s*"[^"]*"(?:[^{}]|"(?:[^"\\]|\\.)*")*)\}', raw, re.DOTALL)
# Better: find each post object by capturing from '{' slug to the closing '}' that ends the post
# Let's use a different approach - find each post by starting at '{...slug:...}' pattern

# Extract all post objects using regex on slug boundaries
# Pattern: find positions of '  {' with 'slug:' following soon after
parts = raw.split('\n  {\n')
all_posts = []
for part in parts[1:]:  # skip the 'const posts = [' prefix
    # Find the matching closing brace for this post
    depth = 0
    post_chars = []
    i = 0
    brace_found = False
    while i < len(part):
        c = part[i]
        if c == '{':
            depth += 1
            brace_found = True
        elif c == '}':
            depth -= 1
            if depth == 0 and brace_found:
                post_chars.append(c)
                break
        post_chars.append(c)
        i += 1
    post_str = '{' + ''.join(post_chars)
    all_posts.append(post_str)

print(f"Parsed {len(all_posts)} posts from file")

def extract_field(post_str, field):
    """Extract a simple string field from a post string."""
    # Try double quotes first
    m = re.search(rf'{field}\s*:\s*"([^"]*)"', post_str)
    if m:
        return m.group(1)
    return None

def extract_tags(post_str):
    """Extract the tags array."""
    m = re.search(r'tags\s*:\s*\[([^\]]*)\]', post_str, re.DOTALL)
    if m:
        tags_str = m.group(1)
        tags = re.findall(r'"([^"]*)"', tags_str)
        return tags
    return []

def extract_content(post_str):
    """Extract the content (template literal) from a post string."""
    # Content is enclosed in backticks: content: ` ... `
    m = re.search(r'content\s*:\s*`([\\s\\S]*?)`\s*,?\s*\n?\s*\}', post_str, re.DOTALL)
    if m:
        return m.group(1)
    # Try alternative: content: `...` with no comma before }
    m = re.search(r'content\s*:\s*`([^`]*)`', post_str, re.DOTALL)
    if m:
        return m.group(1)
    return ""

def get_primary_keyword(title):
    """Extract primary keyword from title - first meaningful noun phrase."""
    if not title:
        return ""
    # Remove common stop words, SEO indicators, and find main topic
    title_lower = title.lower()
    # Try to find the main topic before the last few words
    # Common patterns: "X for Y", "X in Y", "Complete X Guide", etc.
    
    # List of stop words to filter
    stop_words = {'a', 'an', 'the', 'for', 'in', 'of', 'to', 'and', 'or', 'is', 'are',
                  'your', 'our', 'their', 'its', 'it', 'this', 'that', 'at', 'by',
                  'with', 'from', 'on', 'as', 'be', 'has', 'have', 'do', 'does',
                  'complete', 'ultimate', 'essential', 'guide', 'tips', 'strategies',
                  'checklist', 'how', 'what', 'why', 'when', 'where', 'which', 'who',
                  'best', 'top', 'vs', 'vs.', 'needs', 'matters', 'optimization'}
    
    # Split into words
    words = title_lower.split()
    
    # Remove leading SEO/guide words
    lead_words = {'complete', 'ultimate', 'essential', 'how', 'what', 'why', 'when',
                  'where', 'seo', 'geo', 'local', 'technical', 'mobile', 'enterprise',
                  'building', 'blogging', 'backlink'}
    
    # Find the main noun phrase - take significant words not in stop_words
    significant = [w for w in words if w not in stop_words and len(w) > 2]
    
    # Specialized extraction based on title content
    # For compound topic keywords, try to find the core topic
    if 'seo' in title_lower and 'guide' in title_lower:
        # Try to get the specific SEO type
        for prefix in ['technical', 'local', 'mobile', 'enterprise', 'complete']:
            if prefix in title_lower:
                rest = title_lower.split(prefix, 1)[1].strip()
                # Remove 'seo guide' from rest
                rest = re.sub(r'\bseo\s+guide\b', '', rest).strip()
                if rest:
                    # Get first meaningful word(s)
                    parts = rest.split()
                    result = []
                    for p in parts:
                        p = p.strip('-,')
                        if p not in stop_words and len(p) > 2:
                            result.append(p)
                        if len(result) >= 2:
                            break
                    if result:
                        return ' '.join(result)
    
    # For 'seo vs X' patterns
    if ' vs ' in title_lower or ' vs. ' in title_lower:
        parts = re.split(r'\s+vs\.?\s+', title_lower)
        # Take the part before 'vs'
        before = parts[0]
        sig = [w for w in before.split() if w not in stop_words and len(w) > 2]
        if sig:
            return ' '.join(sig[:2])
    
    # For 'why-X-is-best' type slugs
    if 'why' in significant:
        # Take the main subject after 'why'
        idx = words.index('why') if 'why' in words else -1
        if idx >= 0 and idx + 1 < len(words):
            after_why = words[idx+1:]
            sig = [w for w in after_why if w not in stop_words and len(w) > 2]
            if sig:
                return ' '.join(sig[:2])
    
    # Default: return top 2-3 significant words
    if len(significant) >= 2:
        return ' '.join(significant[:2])
    elif significant:
        return significant[0]
    return title_lower.strip()

def check_tfidf(content, keyword):
    """Check keyword density - count keyword occurrences."""
    if not keyword or not content:
        return 0
    content_lower = content.lower()
    keyword_lower = keyword.lower()
    # Count occurrences (case-insensitive, partial match for compound keywords)
    count = content_lower.count(keyword_lower)
    return count

def check_entities(content, slug, title):
    """Check entity coverage: location, service type, industry."""
    content_lower = content.lower()
    title_lower = title.lower()
    missing = []
    
    # 1. Location check - must have Dhaka AND/OR Bangladesh
    has_dhaka = 'dhaka' in content_lower
    has_bangladesh = 'bangladesh' in content_lower
    has_scotland = 'scotland' in content_lower
    has_dundee = 'dundee' in content_lower
    
    if 'case-study' in slug:
        has_dhaka = 'dhaka' in content_lower
        if 'scotland' in slug or 'dundee' in slug:
            if not has_scotland and not has_dundee:
                missing.append("Location (Scotland/Dundee)")
        elif 'dhaka' in slug:
            if not has_dhaka:
                missing.append("Location (Dhaka)")
        elif 'mir' in slug:
            if not has_bangladesh:
                missing.append("Location (Bangladesh)")
        elif 'morethanpanel' in slug or 'smmgen' in slug or 'smmsun' in slug:
            if not has_bangladesh:
                missing.append("Location (Bangladesh)")
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
        'google-business-profile': 'Google Business Profile',
        'seo-garments-textile': 'Garments/textile SEO',
        'seo-event-management': 'event SEO',
        'seo-non-profit': 'non-profit SEO',
        'seo-photographers': 'photographer SEO',
        'seo-wedding-event': 'wedding SEO',
        'seo-real-estate': 'real estate SEO',
        'seo-vs-google-ads': ['SEO', 'Google Ads'],
        'seo-vs-ppc': ['SEO', 'PPC'],
        'technical-seo': 'technical SEO',
        'mobile-seo': 'mobile SEO',
        'link-building': 'link building',
        'backlink-outreach': 'backlink outreach',
        'building-seo-roadmap': 'SEO roadmap',
        'blogging-strategy': 'blogging strategy',
        'complete-seo-guide': 'SEO guide',
        'enterprise-seo': 'enterprise SEO',
        'geo-optimization': 'GEO optimization',
        'how-to-choose-right-seo-agency': 'SEO agency',
        'why-ecommerce-store-needs-seo': 'e-commerce SEO',
        'why-md-kanok-miah-is-the-best': 'SEO expert',
        'seo-breadcrumb-schema': ['breadcrumb schema', 'structured data'],
        'seo-faq-schema': ['FAQ schema', 'FAQ'],
        'seo-howto-schema': ['HowTo schema', 'structured data'],
        'seo-hreflang-guide': ['hreflang', 'international SEO'],
        'seo-json-ld-schema': ['JSON-LD', 'structured data'],
        'seo-robots-txt-guide': ['robots.txt', 'technical SEO'],
        'seo-structured-data-guide': ['structured data', 'schema'],
        'seo-xml-sitemap-guide': ['XML sitemap', 'sitemap'],
        'landlord-certificates-seo': 'landlord certificates SEO',
        'das-taxis-scotland-seo': 'taxi SEO',
        'locksmith-dundee-seo': 'locksmith SEO',
        'morethanpanel-seo': 'panel beating SEO',
        'smmgen-seo': 'social media SEO',
        'smmsun-seo': 'social media SEO',
        'mir-cement-seo': 'cement SEO',
        'dhaka-apparels-seo': 'apparel SEO',
        'stealth-windshield-repairs-seo': 'windshield repair SEO',
        'seo-dashboard-tools': 'SEO dashboard',
    }
    
    # Find matching service topic
    matched_service = None
    for key, service in service_topics.items():
        if slug.startswith(key) or slug == key:
            matched_service = service
            break
    
    if matched_service:
        if isinstance(matched_service, list):
            found = False
            for s in matched_service:
                if s.lower() in content_lower:
                    found = True
                    break
            if not found:
                missing.append(f"Service topic ({', '.join(matched_service)})")
        else:
            if matched_service.lower() not in content_lower:
                missing.append(f"Service topic ({matched_service})")
    
    # 3. Industry check (if applicable)
    industry_checks = {
        'seo-garments-textile': ['garment', 'textile', 'apparel', 'rmg', 'readymade'],
        'seo-real-estate': ['real estate', 'property', 'developer', 'builder'],
        'seo-event-management': ['event', 'management', 'event planner'],
        'seo-wedding-event': ['wedding', 'event', 'planner'],
        'seo-non-profit': ['non-profit', 'ngo', 'charity', 'nonprofit'],
        'seo-photographers': ['photographer', 'photography', 'videographer', 'videography'],
        'why-ecommerce-store-needs-seo': ['e-commerce', 'ecommerce', 'online store', 'shop'],
        'seo-garments-textile': ['garment', 'textile', 'apparel'],
        'dhaka-apparels-seo': ['apparel', 'garment', 'clothing'],
        'mir-cement-seo': ['cement', 'construction', 'building material'],
        'locksmith-dundee-seo': ['locksmith'],
        'das-taxis-scotland-seo': ['taxi', 'cab'],
        'landlord-certificates-seo': ['landlord', 'gas safety', 'eicr', 'certificate'],
        'stealth-windshield-repairs-seo': ['windshield', 'auto glass', 'car glass'],
        'morethanpanel-seo': ['panel', 'panel beater', 'collision repair'],
        'smmgen-seo': ['social media', 'marketing'],
        'smmsun-seo': ['social media', 'marketing'],
    }
    
    for key, industry_terms in industry_checks.items():
        if slug.startswith(key) or slug == key:
            found = any(term.lower() in content_lower for term in industry_terms)
            if not found:
                missing.append(f"Industry terms ({', '.join(industry_terms[:3])})")
            break
    
    return missing

def check_pillar_link(content, tags, slug):
    """Check if the post links to its main pillar/thematic page."""
    content_lower = content.lower()
    links_in_content = re.findall(r'\[([^\]]*)\]\(([^)]*)\)', content)
    
    pillar_candidates = []
    
    # Based on tags and slug, determine what pillar links to look for
    slug_lower = slug.lower()
    
    # Mapping of topics to their expected pillar links
    pillar_mapping = {
        'seo-garments-textile': ['/industries/', '/blog/seo-garments-textile'],
        'seo-event-management': ['/industries/', '/blog/seo-event-management'],
        'seo-real-estate': ['/industries/', '/industries/real-estate'],
        'seo-photographers': ['/industries/', '/blog/seo-photographers'],
        'seo-wedding-event': ['/industries/', '/blog/seo-wedding-event'],
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
        'why-ecommerce-store-needs-seo': ['/industries/ecommerce'],
        'geo-optimization': ['/services/geo'],
        'how-to-choose-right-seo-agency': ['/services/'],
        'link-building': ['/services/link-building'],
        'backlink-outreach': ['/services/link-building'],
        'google-business-profile': ['/services/local-seo'],
        'seo-vs-google-ads': ['/services/'],
        'seo-vs-ppc': ['/services/'],
        'complete-seo-guide': ['/services/'],
        'enterprise-seo': ['/services/'],
        'blogging-strategy': ['/services/content-marketing'],
        'building-seo-roadmap': ['/services/'],
        'why-md-kanok-miah-is-the-best': ['/about', '/'],
        'mobile-seo': ['/services/technical-seo'],
        'landlord-certificates-seo': ['/case-studies/'],
        'das-taxis-scotland-seo': ['/case-studies/'],
        'locksmith-dundee-seo': ['/case-studies/'],
        'morethanpanel-seo': ['/case-studies/'],
        'smmgen-seo': ['/case-studies/'],
        'smmsun-seo': ['/case-studies/'],
        'mir-cement-seo': ['/case-studies/'],
        'dhaka-apparels-seo': ['/case-studies/'],
        'stealth-windshield-repairs-seo': ['/case-studies/'],
        'seo-dashboard-tools': ['/services/'],
    }
    
    # Find match
    expected_links = []
    for key, links in pillar_mapping.items():
        if slug_lower.startswith(key) or slug_lower == key:
            expected_links = links
            break
    
    # If no specific mapping, check tags for pillar hints
    if not expected_links and tags:
        for tag in tags:
            tag_lower = tag.lower()
            if any(t in tag_lower for t in ['seo', 'guide', 'service', 'industry']):
                continue
    
    found_links = []
    for _, href in links_in_content:
        for expected in expected_links:
            if href.startswith(expected):
                found_links.append(href)
    
    return found_links, expected_links

def check_aeo_geo(content):
    """Count question-based headings."""
    # Find all ## and ### headings that start with question words
    headings = re.findall(r'^#{2,3}\s+(.+)$', content, re.MULTILINE)
    question_words = ['how', 'what', 'why', 'when', 'where', 'can', 'do', 'is', 'are', 'does', 'will', 'should']
    question_headings = []
    for h in headings:
        h_stripped = h.strip().lower()
        # Check if starts with a question word
        for qw in question_words:
            if h_stripped.startswith(qw) or h_stripped.startswith('#' + qw) or h_stripped.startswith(qw.upper()):
                question_headings.append(h.strip())
                break
            # Also check "What is", "How to", etc.
            if h_stripped.startswith('#' + qw):
                question_headings.append(h.strip())
                break
    return question_headings

def check_internal_links(content):
    """Count internal links to other blog posts and site pages."""
    links = re.findall(r'\[([^\]]*)\]\(([^)]*)\)', content)
    internal_links = []
    internal_patterns = ['/blog/', '/services/', '/industries/', '/locations/', '/about', '/case-studies/', '/']
    for text, href in links:
        if href.startswith('/'):
            # Skip empty or self-referencing
            if len(href) > 1:
                internal_links.append((text, href))
        elif href.startswith('http') and 'kanokmiah.com.bd' in href.lower():
            internal_links.append((text, href))
    # Also count raw /blog/ links not in markdown format
    # Count unique internal destinations (don't double-count same link)
    unique_hrefs = set(h for _, h in internal_links)
    return len(unique_hrefs), internal_links[:20]  # Return count and up to 20 examples

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

# Parse posts properly
parsed_posts = {}
for post_str in all_posts:
    slug = extract_field(post_str, 'slug')
    if slug and slug in modified_slugs:
        title = extract_field(post_str, 'title')
        date = extract_field(post_str, 'date')
        author = extract_field(post_str, 'author')
        excerpt = extract_field(post_str, 'excerpt')
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
        'question_headings': question_headings,
        'aeo_pass': aeo_pass,
        'internal_count': internal_count,
        'internal_examples': internal_examples,
        'schema_missing': schema_missing,
        'schema_pass': schema_pass,
    }

# Output results
all_pass = 0
all_fail = 0
fail_details = []

for slug in modified_slugs:
    if slug not in results:
        print(f"❌ Post: {slug} — NOT FOUND in parsed data")
        all_fail += 1
        continue
    
    r = results[slug]
    checks_passed = r['tfidf_pass'] and r['entities_pass'] and r['pillar_pass'] and r['aeo_pass'] and r['il_pass'] and r['schema_pass']
    
    if checks_passed:
        print(f"✅ Post: {slug} — all checks passed")
        all_pass += 1
    else:
        print(f"\n## Post: {slug}")
        print(f"| Check | Status | Details |")
        print(f"|-------|--------|---------|")
        
        # TF-IDF
        tfidf_status = "✅" if r['tfidf_pass'] else "❌"
        print(f"| TF-IDF: '{r['keyword']}' | {tfidf_status} | {r['tfidf_count']} occurrences |")
        
        # Entities
        ent_status = "✅" if r['entities_pass'] else "❌"
        ent_detail = "All present" if r['entities_pass'] else f"Missing: {', '.join(r['missing_entities'])}"
        print(f"| Entities | {ent_status} | {ent_detail} |")
        
        # Pillar Link
        pill_status = "✅" if r['pillar_pass'] else "❌"
        pill_detail = "No relevant pillar link found"
        if r['found_pillar_links']:
            pill_detail = f"Links to: {', '.join(r['found_pillar_links'][:3])}"
        elif r['expected_pillar']:
            pill_detail = f"Expected pillar: {', '.join(r['expected_pillar'])}"
        print(f"| Pillar Link | {pill_status} | {pill_detail} |")
        
        # AEO/GEO
        aeo_status = "✅" if r['aeo_pass'] else "❌"
        print(f"| AEO/GEO | {aeo_status} | {len(r['question_headings'])} question headings |")
        
        # Internal Links
        il_status = "✅" if r['il_pass'] else "❌"
        print(f"| Internal Links | {il_status} | {r['internal_count']} unique internal links |")
        
        # Schema Ready
        sch_status = "✅" if r['schema_pass'] else "❌"
        sch_detail = "All fields set" if r['schema_pass'] else f"Missing: {', '.join(r['schema_missing'])}"
        print(f"| Schema Ready | {sch_status} | {sch_detail} |")
        
        # Fix instructions
        print(f"\n### Fix instructions:")
        fixes = []
        if not r['tfidf_pass']:
            fixes.append(f"- Increase usage of keyword '{r['keyword']}' in content (currently {r['tfidf_count']} occurrences, need ≥5)")
        if not r['entities_pass']:
            fixes.append(f"- Add missing entities: {', '.join(r['missing_entities'])}")
        if not r['pillar_pass']:
            if r['expected_pillar']:
                fixes.append(f"- Add internal link to pillar page ({', '.join(r['expected_pillar'])})")
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

print(f"\n\n## Summary")
print(f"Total posts checked: 40")
print(f"✅ All checks passed: {all_pass}")
print(f"❌ Some checks failed: {all_fail}")
print(f"Pass rate: {all_pass/40*100:.1f}% ({all_pass}/40)")

# For each failed post, provide summary of failures
print(f"\n### Breakdown of failures:")
failure_counts = {'TF-IDF': 0, 'Entities': 0, 'Pillar Link': 0, 'AEO/GEO': 0, 'Internal Links': 0, 'Schema Readiness': 0}
for slug in modified_slugs:
    if slug not in results:
        continue
    r = results[slug]
    if not r['tfidf_pass']: failure_counts['TF-IDF'] += 1
    if not r['entities_pass']: failure_counts['Entities'] += 1
    if not r['pillar_pass']: failure_counts['Pillar Link'] += 1
    if not r['aeo_pass']: failure_counts['AEO/GEO'] += 1
    if not r['il_pass']: failure_counts['Internal Links'] += 1
    if not r['schema_pass']: failure_counts['Schema Readiness'] += 1

for check, count in failure_counts.items():
    print(f"  {check}: {count} posts failing")
