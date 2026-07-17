#!/usr/bin/env python3
"""Content Framework Enforcer for kanokmiah.com.bd
Runs TF-IDF, Entity, Pillar, AEO/GEO, Internal Linking, and Schema checks
on specified blog posts from data.js.
"""

import re
import json
import sys
import math
from collections import Counter

# Load data.js
with open('src/app/blog/data.js', 'r') as f:
    content = f.read()

# Parse all posts using regex-based extraction
# Find each post object
post_pattern = re.compile(
    r'slug:\s*["\']([^"\']+)["\']\s*,\s*'
    r'title:\s*["\']([^"\']+)["\']',
    re.DOTALL
)

# More robust approach: split by "slug:" and reconstruct
parts = content.split("slug: ")[1:]  # Skip the array start

posts = []
for part in parts:
    post = {}
    # Extract slug
    slug_match = re.match(r'["\']([^"\']+)["\']', part)
    if not slug_match:
        continue
    post['slug'] = slug_match.group(1)

    # Extract other fields using patterns
    def extract_field(pattern, name):
        m = re.search(pattern, part, re.DOTALL)
        if m:
            post[name] = m.group(1).strip()

    extract_field(r'title:\s*["\']([^"\']+)["\']', 'title')
    extract_field(r'date:\s*["\']([^"\']+)["\']', 'date')
    extract_field(r'author:\s*["\']([^"\']+)["\']', 'author')
    extract_field(r'metaTitle:\s*["\']([^"\']+)["\']', 'metaTitle')
    extract_field(r'metaDescription:\s*["\']([^"\']+)["\']', 'metaDescription')
    extract_field(r'dateModified:\s*["\']([^"\']+)["\']', 'dateModified')

    # Tags
    tags_match = re.search(r'tags:\s*\[(.*?)\]', part, re.DOTALL)
    if tags_match:
        tags_str = tags_match.group(1)
        tags = re.findall(r'["\']([^"\']+)["\']', tags_str)
        post['tags'] = tags

    # Excerpt
    excerpt_match = re.search(r'excerpt:\s*["\']([^"\']+)["\']', part, re.DOTALL)
    if excerpt_match:
        post['excerpt'] = excerpt_match.group(1)

    # Content - everything between content: ` and the closing `
    content_match = re.search(r'content:\s*`([\s\S]*?)`\s*(?:,|\);|\n\s*[},])', part)
    if content_match:
        post['content'] = content_match.group(1)
    else:
        # Try a more lenient match
        content_match = re.search(r'content:\s*`([\s\S]*)`', part)
        if content_match:
            post['content'] = content_match.group(1)
        else:
            post['content'] = ''

    posts.append(post)

print(f"Total posts parsed: {len(posts)}", file=sys.stderr)

# Posts to check (from git diff analysis)
posts_to_check = [
    # 8 brand new posts
    "ai-seo-2026-dhaka-experts-optimize-google-ai-chatgpt",
    "hiring-seo-expert-dhaka-better-roi-than-paid-ads",
    "how-to-choose-best-seo-expert-dhaka-15-things",
    "seo-case-study-dhaka-businesses-increased-organic-traffic",
    "seo-expert-vs-seo-agency-dhaka-which-is-right",
    "top-10-seo-mistakes-dhaka-businesses-fix",
    "watchzonebd-seo-case-study",
    "what-does-seo-expert-do-guide-business-owners",
    # 21 existing posts with substantive changes
    "complete-seo-guide-bangladesh-businesses-2026",
    "content-marketing-strategy-bangladeshi-brands-seo",
    "das-taxis-scotland-seo-case-study",
    "geo-optimization-prepare-business-ai-search",
    "google-business-profile-optimization-guide-bangladesh",
    "how-to-choose-right-seo-agency-bangladesh",
    "international-seo-bangladesh-exporters-global-buyers",
    "link-building-strategies-bangladesh-market",
    "local-seo-tips-dhaka-businesses-google-maps",
    "locksmith-dundee-seo-case-study",
    "mobile-seo-optimization-bangladesh-mobile-first-era",
    "morethanpanel-seo-case-study",
    "seo-garments-textile-industry-b2b-lead-generation",
    "seo-real-estate-developers-dhaka",
    "seo-vs-google-ads-whats-best-bangladesh-businesses",
    "smmgen-seo-case-study",
    "smmsun-seo-case-study",
    "stealth-windshield-repairs-seo-case-study",
    "technical-seo-checklist-bangladeshi-websites",
    "why-ecommerce-store-needs-seo-bangladesh",
    "why-md-kanok-miah-is-the-best-seo-expert-in-dhaka-bangladesh",
]

def get_primary_keyword(title):
    """Extract primary keyword from title (first meaningful noun phrase)."""
    # Remove punctuation
    clean = re.sub(r'[^\w\s]', '', title)
    # Take first 2-4 words that form a meaningful noun phrase
    words = clean.split()
    if not words:
        return title.lower()
    # Skip articles/prepositions at start
    skip_words = {'a', 'an', 'the', 'how', 'what', 'why', 'when', 'where', 'is', 'are', 'do', 'does', 'to', 'for', 'in', 'of', 'on', 'at', 'by', 'with', 'from'}
    # Find first meaningful word
    start = 0
    for i, w in enumerate(words):
        if w.lower() not in skip_words:
            start = i
            break
    # Take 2-3 words as keyword phrase
    keyword = ' '.join(words[start:start+3])
    return keyword.lower()

def check_tfidf(content, title):
    """Check TF-IDF coverage - keyword occurrence count."""
    keyword = get_primary_keyword(title)
    if not keyword:
        return "N/A", "??", "Could not extract keyword"
    count = len(re.findall(re.escape(keyword), content.lower()))
    status = "✅" if count >= 5 else "❌"
    details = f"{count} occurrences of '{keyword}'"
    return status, keyword, details

def check_entities(content, slug, title, tags):
    """Check semantic entity coverage."""
    required_entities = {
        'location_dhaka': ['dhaka', 'dhaka'],
        'location_bangladesh': ['bangladesh', 'bangladesh', 'bangladeshi'],
        'kanok_miah': ['kanok miah', 'kanok'],
    }
    # Determine service type based on slug and tags
    service_types = []
    tag_text = ' '.join(tags).lower() if tags else ''
    slug_lower = slug.lower()
    title_lower = title.lower()
    
    # Service type mapping
    if any(x in slug_lower for x in ['seo', 'search-engine', 'ranking']):
        service_types.append('seo')
    if any(x in slug_lower for x in ['local-seo', 'google-maps', 'gbp', 'google-business']):
        service_types.append('local-seo')
    if any(x in slug_lower for x in ['technical-seo', 'core-web-vitals', 'page-speed']):
        service_types.append('technical-seo')
    if any(x in slug_lower for x in ['content', 'writing']):
        service_types.append('content-marketing')
    if any(x in slug_lower for x in ['link-building', 'backlink']):
        service_types.append('link-building')
    if any(x in slug_lower for x in ['geo', 'ai-search', 'generative']):
        service_types.append('geo')
    if any(x in slug_lower for x in ['ecommerce', 'e-commerce', 'daraz', 'shopify']):
        service_types.append('ecommerce')
    if any(x in slug_lower for x in ['real-estate', 'property']):
        service_types.append('real-estate')
    if any(x in slug_lower for x in ['garment', 'textile']):
        service_types.append('garments-textile')
    
    # Map service types to their keywords
    service_keywords = {
        'seo': ['seo', 'search engine optimization', 'organic search', 'ranking'],
        'local-seo': ['local seo', 'google business profile', 'google maps', 'gbp', 'local search'],
        'technical-seo': ['technical seo', 'core web vitals', 'page speed', 'crawlability'],
        'content-marketing': ['content marketing', 'content strategy', 'blog'],
        'link-building': ['link building', 'backlink', 'guest post'],
        'geo': ['geo', 'generative engine', 'ai search', 'sge'],
        'ecommerce': ['ecommerce', 'e-commerce', 'online store', 'product page'],
        'real-estate': ['real estate', 'property', 'developer'],
        'garments-textile': ['garment', 'textile', 'b2b'],
    }
    
    content_lower = content.lower()
    missing = []
    
    # Check location entities
    if not re.search(r'dhaka', content_lower):
        missing.append('Dhaka (location)')
    if not re.search(r'bangladesh|bangladeshi', content_lower):
        missing.append('Bangladesh (location)')
    if not re.search(r'kanok miah', content_lower):
        missing.append('Kanok Miah (author/brand)')
    
    # Check service-specific entities
    for st in service_types:
        if st in service_keywords:
            found_any = any(re.search(kw, content_lower) for kw in service_keywords[st])
            if not found_any:
                missing.append(f'{st.replace("-", " ").title()} keywords')
    
    # Also check tags for relevant industry entities
    if tags:
        industry_map = {
            'ecommerce': ['ecommerce', 'e-commerce', 'online store'],
            'real estate': ['real estate', 'property'],
            'healthcare': ['healthcare', 'medical', 'health', 'clinic'],
            'education': ['education', 'school', 'university', 'student'],
            'food': ['food', 'restaurant', 'cafe'],
        }
        for tag in tags:
            for industry, keywords in industry_map.items():
                if any(kw in tag.lower() for kw in keywords):
                    if not any(re.search(kw, content_lower) for kw in keywords):
                        missing.append(f'{industry.title()} (tagged but not covered)')
    
    status = "✅" if not missing else "❌"
    if not missing:
        details = "All required entities present"
    else:
        details = f"Missing: {', '.join(missing[:5])}"
        if len(missing) > 5:
            details += f" (+{len(missing)-5} more)"
    
    return status, details

def check_pillar_cluster(tags, content, slug):
    """Check pillar-cluster alignment."""
    if not tags:
        return "❌", "No tags defined"
    
    # Determine pillar topic from first tag or most relevant tag
    tag_text = ' '.join(tags).lower()
    content_lower = content.lower()
    
    # Define pillar pages and their cluster keywords
    pillar_pages = {
        'seo-guide': {
            'keyword': 'complete seo guide for bangladesh businesses',
            'slug': 'complete-seo-guide-bangladesh-businesses-2026',
            'cluster_tags': ['seo guide', 'seo', 'search engine optimization', '2026']
        },
        'local-seo': {
            'keyword': 'local seo tips for dhaka businesses',
            'slug': 'local-seo-tips-dhaka-businesses-google-maps',
            'cluster_tags': ['local seo', 'dhaka', 'google maps']
        },
        'technical-seo': {
            'keyword': 'technical seo checklist for bangladeshi websites',
            'slug': 'technical-seo-checklist-bangladeshi-websites',
            'cluster_tags': ['technical seo', 'core web vitals', 'website speed']
        },
    }
    
    # Check if post links to ANY pillar page
    pillar_links = []
    for pillar_slug, pillar in pillar_pages.items():
        if f'/blog/{pillar["slug"]}' in content:
            pillar_links.append(pillar['slug'])
    
    # Also check if post links to service pages or location pages
    service_link = bool(re.search(r'/services/', content))
    location_link = bool(re.search(r'/locations/', content))
    
    if pillar_links:
        return "✅", f"Links to pillar: {', '.join(pillar_links[:2])}"
    elif service_link or location_link:
        return "⚠️", f"No pillar page link. Has {'services' if service_link else ''} {'/ ' if service_link and location_link else ''} {'locations' if location_link else ''} link(s)."
    else:
        return "❌", "No pillar page link found"

def check_aeo_geo(content):
    """Check AEO/GEO optimization - count question-based headings."""
    # Find all headings (## or ###)
    headings = re.findall(r'^#{2,3}\s+.*$', content, re.MULTILINE)
    
    # Count question-based headings
    question_words = ['How', 'What', 'Why', 'When', 'Where', 'Can', 'Do', 'Is', 'Are', 'Does', 'Which', 'Who', 'Should', 'Will']
    question_headings = []
    for h in headings:
        h_text = h.lstrip('#').strip()
        first_word = h_text.split()[0] if h_text.split() else ''
        if first_word in question_words or first_word.rstrip('?:') in question_words:
            question_headings.append(h_text)
    
    count = len(question_headings)
    status = "✅" if count >= 2 else "❌"
    if question_headings:
        details = f"{count} question headings: {'; '.join(question_headings[:3])}"
        if len(question_headings) > 3:
            details += f" (+{len(question_headings)-3} more)"
    else:
        details = "0 question headings"
    
    return status, details

def check_internal_linking(content, slug):
    """Count internal links to other posts, services, locations."""
    # Internal links to blog posts
    blog_links = re.findall(r'/blog/([^"\')\]\s]+)', content)
    # Service links
    service_links = re.findall(r'/services/([^"\')\]\s]+)', content)
    # Location links
    location_links = re.findall(r'/locations/([^"\')\]\s]+)', content)
    # Industry links
    industry_links = re.findall(r'/industries/([^"\')\]\s]+)', content)
    
    # Exclude self-links
    blog_links = [l for l in blog_links if l != slug]
    
    total = len(blog_links) + len(service_links) + len(location_links) + len(industry_links)
    status = "✅" if total >= 3 else "❌"
    
    link_types = []
    if blog_links:
        link_types.append(f"{len(blog_links)} blog posts")
    if service_links:
        link_types.append(f"{len(service_links)} services")
    if location_links:
        link_types.append(f"{len(location_links)} locations")
    if industry_links:
        link_types.append(f"{len(industry_links)} industries")
    
    details = f"{total} total ({', '.join(link_types)})" if link_types else f"{total} total"
    
    return status, details

def check_schema(post):
    """Check if schema-required fields are present."""
    missing = []
    if not post.get('title'):
        missing.append('title')
    if not post.get('excerpt'):
        missing.append('excerpt')
    if not post.get('date'):
        missing.append('date')
    if not post.get('metaTitle'):
        missing.append('metaTitle')
    if not post.get('metaDescription'):
        missing.append('metaDescription')
    
    status = "✅" if not missing else "❌"
    if not missing:
        details = "All fields set (title, excerpt, date, metaTitle, metaDescription)"
    else:
        details = f"Missing: {', '.join(missing)}"
    
    return status, details

# Run checks for each post
print("=" * 80)
print("CONTENT FRAMEWORK ENFORCEMENT REPORT")
print(f"Generated: July 15, 2026")
print("=" * 80)

all_passed = True
for target_slug in posts_to_check:
    post = None
    for p in posts:
        if p['slug'] == target_slug:
            post = p
            break
    
    if not post:
        print(f"\n{'='*60}")
        print(f"## Post: {target_slug}")
        print(f"{'='*60}")
        print("⚠️  NOT FOUND in data.js")
        continue
    
    title = post.get('title', 'Untitled')
    content = post.get('content', '')
    tags = post.get('tags', [])
    
    print(f"\n{'='*60}")
    print(f"## Post: {target_slug}")
    print(f"Title: {title}")
    print(f"{'='*60}")
    print("| Check | Status | Details |")
    print("|-------|--------|---------|")
    
    # A. TF-IDF
    tfidf_status, keyword, tfidf_details = check_tfidf(content, title)
    print(f"| TF-IDF: {keyword} | {tfidf_status} | {tfidf_details} |")
    if tfidf_status == "❌":
        all_passed = False
    
    # B. Entities
    ent_status, ent_details = check_entities(content, target_slug, title, tags)
    print(f"| Entities | {ent_status} | {ent_details} |")
    if ent_status == "❌":
        all_passed = False
    
    # C. Pillar-Cluster
    pillar_status, pillar_details = check_pillar_cluster(tags, content, target_slug)
    print(f"| Pillar Link | {pillar_status} | {pillar_details} |")
    if pillar_status == "❌":
        all_passed = False
    
    # D. AEO/GEO
    aeo_status, aeo_details = check_aeo_geo(content)
    print(f"| AEO/GEO | {aeo_status} | {aeo_details} |")
    if aeo_status == "❌":
        all_passed = False
    
    # E. Internal Links
    il_status, il_details = check_internal_linking(content, target_slug)
    print(f"| Internal Links | {il_status} | {il_details} |")
    if il_status == "❌":
        all_passed = False
    
    # F. Schema
    schema_status, schema_details = check_schema(post)
    print(f"| Schema Ready | {schema_status} | {schema_details} |")
    if schema_status == "❌":
        all_passed = False
    
    # Fix instructions
    fixes = []
    if tfidf_status == "❌":
        fixes.append(f"- Increase usage of primary keyword '{keyword}' to >=5 occurrences (currently {tfidf_details.split()[0]})")
    if ent_status == "❌":
        fixes.append(f"- Add missing entities: {ent_details.replace('Missing: ', '')}")
    if pillar_status == "❌":
        fixes.append("- Add a link to the relevant pillar page (e.g., complete-seo-guide-bangladesh-businesses-2026, local-seo-tips-dhaka-businesses-google-maps, or technical-seo-checklist-bangladeshi-websites)")
    if aeo_status == "❌":
        fixes.append("- Add at least 2 question-based headings (How, What, Why, Can, Do, Is, Are...) for AEO/GEO optimization")
    if il_status == "❌":
        fixes.append("- Add more internal links to other blog posts, services, locations, or industries (need >=3)")
    if schema_status == "❌":
        missing_fields = schema_details.replace('Missing: ', '')
        fixes.append(f"- Set missing schema fields: {missing_fields}")
    
    if fixes:
        print("\n### Fix instructions:")
        for f in fixes:
            print(f)
    else:
        print("\n### ✅ All checks passed!")
    
    print()

print("=" * 80)
if all_passed:
    print("OVERALL: ✅ ALL POSTS PASS ALL CHECKS")
else:
    print("OVERALL: ❌ Some posts need fixes (see above)")
print("=" * 80)
