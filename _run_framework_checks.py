#!/usr/bin/env python3
"""
Content Framework Enforcer for kanokmiah.com.bd
Performs full framework checks on specified blog posts.
"""
import re
import json
import sys

# Load data.js
with open("/root/kanok-miahit/src/app/blog/data.js") as f:
    content = f.read()

# Parse all posts
# Find each post object with slug, title, etc.
posts_raw = re.findall(
    r'{\s*\n\s*slug:\s*"([^"]+)"\s*,\s*\n\s*title:\s*"([^"]+)"\s*,\s*\n\s*date:\s*"([^"]+)"',
    content
)
# Build slug-to-post mapping with full text content
post_pattern = re.compile(
    r'{\s*\n\s*slug:\s*"([^"]+)"(.*?)^\s*},?\s*$',
    re.MULTILINE | re.DOTALL
)

posts = {}
for m in post_pattern.finditer(content):
    slug = m.group(1)
    block = m.group(0)
    
    # Extract title
    t = re.search(r'title:\s*"((?:[^"\\]|\\.)*)"', block)
    title = t.group(1) if t else ""
    
    # Extract date
    d = re.search(r'date:\s*"([^"]+)"', block)
    date = d.group(1) if d else ""
    
    # Extract excerpt
    e = re.search(r'excerpt:\s*\n?\s*"((?:[^"\\]|\\.)*)"', block)
    excerpt = e.group(1) if e else ""
    
    # Extract tags
    tags_m = re.search(r'tags:\s*\[(.*?)\]', block)
    tags = []
    if tags_m:
        tags = [t.strip().strip('"') for t in tags_m.group(1).split(',')]
    
    # Extract content (the content: `...` block)
    c = re.search(r'content:\s*`(.*?)`\s*,\s*\n', block, re.DOTALL)
    post_content = c.group(1) if c else ""
    
    posts[slug] = {
        'title': title,
        'date': date,
        'excerpt': excerpt,
        'tags': tags,
        'content': post_content
    }

# Changed slugs
changed_slugs = [
    "geo-optimization-prepare-business-ai-search",
    "seo-garments-textile-industry-b2b-lead-generation",
    "mobile-seo-optimization-bangladesh-mobile-first-era",
    "seo-healthcare-medical-clinics-bangladesh",
    "why-md-kanok-miah-is-the-best-seo-expert-in-dhaka-bangladesh",
    "landlord-certificates-seo-case-study",
    "das-taxis-scotland-seo-case-study",
    "morethanpanel-seo-case-study",
    "smmgen-seo-case-study",
    "smmsun-seo-case-study",
    "mir-cement-seo-case-study",
    "dhaka-apparels-seo-case-study",
    "stealth-windshield-repairs-seo-case-study",
    "how-to-choose-best-seo-expert-dhaka-15-things",
    "seo-expert-vs-seo-agency-dhaka-which-is-right",
    "top-10-seo-mistakes-dhaka-businesses-fix",
    "what-does-seo-expert-do-guide-business-owners",
    "seo-case-study-dhaka-businesses-increased-organic-traffic",
    "hiring-seo-expert-dhaka-better-roi-than-paid-ads",
    "ai-seo-2026-dhaka-experts-optimize-google-ai-chatgpt",
]

def extract_primary_keyword(title):
    """Extract primary keyword from title - first meaningful noun phrase."""
    # Remove common prefixes
    title_lower = title.lower()
    
    # Patterns for extracting the core topic
    # For SEO titles, the primary keyword is usually the main topic
    patterns = [
        r'(?:complete|ultimate|definitive|essential|expert)\s+(.+?)(?:\s+guide|\s+for|\s+in|\s+\d{4}|$)',
        r'(?:what|how|why|when|where)\s+(?:is|are|does|do|can|to)\s+(.+?)(?:\s+in|\s+for|\s+\?|$)',
        r'(.+?)(?:\s+guide|\s+strategy|\s+checklist|\s+tips|\s+optimization|\s+marketing|\s+services)',
    ]
    
    for p in patterns:
        m = re.search(p, title_lower)
        if m:
            kw = m.group(1).strip()
            # Break into words, take first 2-4 meaningful words
            words = kw.split()
            if len(words) > 4:
                kw = ' '.join(words[:4])
            return kw
    
    # Fallback: take first meaningful noun phrase (skip stopwords)
    stopwords = {'the', 'a', 'an', 'your', 'our', 'their', 'for', 'in', 'of', 'to', 'and', 'or', 'is', 'are', 'what', 'how', 'why'}
    words = title_lower.split()
    # Find first content word
    for i, w in enumerate(words):
        if w not in stopwords and len(w) > 2:
            # Take from here until we hit another stop word or preposition
            kw_words = [w]
            for j in range(i+1, min(i+4, len(words))):
                if words[j] in {'for', 'in', 'of', 'to', 'and', 'the', 'a', 'an'}:
                    break
                kw_words.append(words[j])
            return ' '.join(kw_words)
    return title_lower.split()[0] if title_lower else ""

def check_tfidf(title, content):
    """A. TF-IDF Coverage - check primary keyword frequency."""
    keyword = extract_primary_keyword(title)
    if not keyword:
        return "unknown", 0, False
    
    # Count occurrences of keyword in content (case insensitive)
    count = len(re.findall(re.escape(keyword), content, re.IGNORECASE))
    passed = count >= 5
    return keyword, count, passed

def check_entities(title, content, tags):
    """B. Semantic Entity Coverage."""
    title_lower = title.lower()
    content_lower = content.lower()
    tags_lower = [t.lower() for t in tags]
    
    # Define entities that should be present based on context
    expected_entities = {
        'location_dhaka': ['dhaka', 'dhaka'],
        'location_bangladesh': ['bangladesh', 'bangladesh'],
    }
    
    # Detect service type from content
    service_types = {
        'seo': ['seo', 'search engine optimization'],
        'local_seo': ['local seo', 'google business profile', 'google maps'],
        'technical_seo': ['technical seo', 'site speed', 'core web vitals'],
        'content_marketing': ['content marketing', 'content strategy'],
        'geo': ['geo', 'generative engine optimization', 'ai search'],
        'aeo': ['aeo', 'answer engine optimization'],
        'ecommerce_seo': ['e-commerce seo', 'ecommerce seo'],
        'healthcare_seo': ['healthcare seo', 'medical seo'],
    }
    
    detected_services = []
    for service, keywords in service_types.items():
        for kw in keywords:
            if kw in content_lower:
                detected_services.append(service)
                break
    
    # Industry detection
    industries = {
        'garments_textile': ['garment', 'textile', 'apparel', 'rmg'],
        'healthcare_medical': ['healthcare', 'medical', 'clinic', 'hospital', 'doctor', 'patient'],
        'ecommerce_retail': ['ecommerce', 'e-commerce', 'retail', 'online store', 'shop'],
        'real_estate': ['real estate', 'property', 'apartment', 'housing'],
        'education': ['education', 'educational institution', 'school', 'college', 'university'],
        'food_restaurant': ['restaurant', 'food', 'cafe', 'dining'],
        'travel_tourism': ['travel', 'tourism', 'tourist', 'hotel'],
        'fitness_gym': ['fitness', 'gym', 'fitness center'],
        'law_firm': ['law firm', 'legal', 'lawyer', 'attorney'],
        'automotive': ['auto', 'automotive', 'car', 'windshield', 'garage'],
        'b2b': ['b2b', 'lead generation', 'wholesale'],
        'seo_service': ['seo expert', 'seo consultant', 'seo services', 'seo agency'],
    }
    
    detected_industries = []
    for ind, keywords in industries.items():
        for kw in keywords:
            if kw in content_lower:
                detected_industries.append(ind)
                break
    
    # Build entity check list
    entity_checks = {}
    
    # Location entities
    entity_checks['bangladesh'] = 'bangladesh' in content_lower
    entity_checks['dhaka'] = 'dhaka' in content_lower
    
    # Service entities
    for service in ['seo', 'local seo', 'technical seo', 'on-page seo']:
        entity_checks[service] = service in content_lower
    
    # Industry-specific entities
    for ind in detected_industries[:3]:  # Check top 3 industries
        for kw in industries[ind]:
            if kw in content_lower:
                entity_checks[f'industry:{ind}'] = True
                break
    
    # Check for specific service mentions related to the business
    if 'case study' in title_lower or 'case study' in content_lower:
        entity_checks['case_study'] = True
    
    missing = [k for k, v in entity_checks.items() if not v]
    passed = len(missing) <= 3  # Allow some missing if not all relevant
    return entity_checks, missing, passed

def check_pillar_link(title, content, tags, slug):
    """C. Pillar-Cluster Alignment."""
    content_lower = content.lower()
    tags_lower = [t.lower() for t in tags]
    
    # Identify pillar topics and their pillar page URLs
    pillar_pages = {
        'seo_guide': {
            'url': '/blog/complete-seo-guide-bangladesh-businesses-2026',
            'keywords': ['seo guide', 'complete seo guide', 'seo for bangladesh'],
            'tags_match': ['seo guide', 'bangladesh seo', '2026']
        },
        'local_seo': {
            'url': '/blog/local-seo-tips-dhaka-businesses-google-maps',
            'keywords': ['local seo', 'google business profile', 'google maps'],
            'tags_match': ['local seo', 'google maps']
        },
        'technical_seo': {
            'url': '/blog/technical-seo-checklist-bangladeshi-websites',
            'keywords': ['technical seo', 'site speed', 'core web vitals'],
            'tags_match': ['technical seo']
        },
        'geo_aeo': {
            'url': '/blog/geo-optimization-prepare-business-ai-search',
            'keywords': ['geo', 'generative engine optimization', 'ai search', 'aeo'],
            'tags_match': ['geo', 'aeo']
        },
        'case_study': {
            'url': '/blog/seo-case-study-dhaka-businesses-increased-organic-traffic',
            'keywords': ['case study', 'seo results', 'traffic growth'],
            'tags_match': ['case study', 'seo case study']
        }
    }
    
    # Determine which pillar this post likely belongs to
    matched_pillar = None
    for pillar_name, pillar in pillar_pages.items():
        # Check tag overlap
        for tag in tags_lower:
            for match_tag in pillar['tags_match']:
                if match_tag in tag:
                    matched_pillar = pillar_name
                    break
        # Check keywords in content
        if not matched_pillar:
            for kw in pillar['keywords']:
                if kw in content_lower:
                    matched_pillar = pillar_name
                    break
    
    # Check if post links to its pillar page
    links_to_pillar = None
    if matched_pillar:
        pillar_url = pillar_pages[matched_pillar]['url']
        if pillar_url in content:
            links_to_pillar = pillar_pages[matched_pillar]['url']
    
    # Also check if post links to the complete SEO guide (the main pillar)
    main_pillar_url = '/blog/complete-seo-guide-bangladesh-businesses-2026'
    links_to_main = main_pillar_url in content
    
    passed = links_to_pillar is not None or links_to_main
    return matched_pillar, links_to_pillar or links_to_main, passed

def check_aeo_geo(content):
    """D. AEO/GEO Optimization - count question headings."""
    # Find markdown headings that are questions
    question_headings = re.findall(
        r'^#{2,6}\s+(How|What|Why|When|Where|Can|Do|Is|Are|Does|Which|Who)\b.*?\?',
        content,
        re.MULTILINE
    )
    count = len(question_headings)
    passed = count >= 2
    return count, passed, question_headings

def check_internal_links(content, slug):
    """E. Internal Linking - count internal links."""
    # Count internal links: /blog/, /services/, /locations/, /about
    blog_links = re.findall(r'/blog/(?!%s)[^"\')\s]+' % re.escape(slug), content)
    service_links = re.findall(r'/services/[^"\')\s]+', content)
    location_links = re.findall(r'/locations/[^"\')\s]+', content)
    other_internal = re.findall(r'/(?:about|contact|faq|industries)[^"\')\s]*', content)
    
    all_links = set(blog_links + service_links + location_links + other_internal)
    total = len(all_links)
    passed = total >= 3
    return total, passed, sorted(all_links)

def check_schema(title, excerpt, date):
    """F. Schema - check if post has necessary fields for ArticleSchema."""
    issues = []
    if not title:
        issues.append("title missing")
    if not excerpt:
        issues.append("excerpt missing")
    if not date:
        issues.append("date missing")
    passed = len(issues) == 0
    return issues, passed

# Run checks on all changed posts
print("# Content Framework Enforcement Report")
print(f"**Date:** 2026-07-27\n")
print(f"**Scope:** {len(changed_slugs)} modified posts (last 48 hours)\n")

all_passed = True

for slug in changed_slugs:
    if slug not in posts:
        print(f"\n## Post: {slug}")
        print("❌ **Post not found in data.js!**")
        continue
    
    post = posts[slug]
    title = post['title']
    content = post['content']
    tags = post['tags']
    excerpt = post['excerpt']
    date = post['date']
    
    print(f"\n## Post: {slug}")
    print(f"**Title:** {title}")
    print(f"**Date:** {date}")
    print(f"**Tags:** {', '.join(tags)}")
    print()
    
    # A. TF-IDF
    keyword, tfidf_count, tfidf_pass = check_tfidf(title, content)
    print(f"### A. TF-IDF Coverage")
    print(f"- **Keyword:** `{keyword}`")
    print(f"- **Occurrences:** {tfidf_count}")
    if tfidf_pass:
        print(f"- ✅ PASS ({tfidf_count} >= 5)")
    else:
        print(f"- ❌ FAIL ({tfidf_count} < 5 — too thin)")
        all_passed = False
    
    print()
    
    # B. Entities
    entity_checks, missing, entity_pass = check_entities(title, content, tags)
    print(f"### B. Semantic Entity Coverage")
    print(f"- **Total checks:** {len(entity_checks)}")
    print(f"- **Passed:** {len(entity_checks) - len(missing)}/{len(entity_checks)}")
    if missing:
        print(f"- **Missing entities:** {', '.join(missing)}")
        if not entity_pass:
            print(f"- ❌ FAIL — too many missing entities")
            all_passed = False
        else:
            print(f"- ⚠️  OK — minor misses")
    else:
        print(f"- ✅ All entities present")
    
    print()
    
    # C. Pillar Link
    pillar_name, pillar_link, pillar_pass = check_pillar_link(title, content, tags, slug)
    print(f"### C. Pillar-Cluster Alignment")
    if pillar_name:
        print(f"- **Matched pillar:** {pillar_name}")
    else:
        print(f"- **Matched pillar:** none detected")
    if pillar_link:
        print(f"- **Pillar link found:** {pillar_link}")
    else:
        print(f"- **Pillar link:** none found")
    if pillar_pass:
        print(f"- ✅ PASS")
    else:
        print(f"- ❌ FAIL — add link to pillar page")
        all_passed = False
    
    print()
    
    # D. AEO/GEO
    aeo_count, aeo_pass, question_headings = check_aeo_geo(content)
    print(f"### D. AEO/GEO Optimization")
    print(f"- **Question headings found:** {aeo_count}")
    if question_headings:
        for qh in question_headings:
            print(f"  - `{qh}?`")
    if aeo_pass:
        print(f"- ✅ PASS ({aeo_count} >= 2)")
    else:
        print(f"- ❌ FAIL ({aeo_count} < 2 — add more question headings)")
        all_passed = False
    
    print()
    
    # E. Internal Links
    link_count, link_pass, links = check_internal_links(content, slug)
    print(f"### E. Internal Linking")
    print(f"- **Total unique internal links:** {link_count}")
    if links:
        for link in links[:10]:
            print(f"  - {link}")
        if len(links) > 10:
            print(f"  - ... and {len(links) - 10} more")
    if link_pass:
        print(f"- ✅ PASS ({link_count} >= 3)")
    else:
        print(f"- ❌ FAIL ({link_count} < 3 — too few internal links)")
        all_passed = False
    
    print()
    
    # F. Schema
    schema_issues, schema_pass = check_schema(title, excerpt, date)
    print(f"### F. Schema Readiness")
    if not title:
        print(f"- ❌ Title missing")
    else:
        print(f"- ✅ Title: set")
    if not excerpt:
        print(f"- ❌ Excerpt missing")
    else:
        print(f"- ✅ Excerpt: set ({len(excerpt)} chars)")
    if not date:
        print(f"- ❌ Date missing")
    else:
        print(f"- ✅ Date: {date}")
    if schema_pass:
        print(f"- ✅ All schema fields present")
    else:
        print(f"- ❌ FAIL — missing: {', '.join(schema_issues)}")
        all_passed = False
    
    print("\n---\n")

# Summary
print("# Summary")
total_posts = len(changed_slugs)
print(f"**Posts checked:** {total_posts}")
if all_passed:
    print("**Overall:** ✅ ALL CHECKS PASSED — All posts comply with the content framework.")
else:
    print(f"**Overall:** ❌ Some posts need fixes (see details above).")
