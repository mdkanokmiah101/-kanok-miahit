#!/usr/bin/env python3
"""
Content Framework Enforcer for kanokmiah.com.bd
Framework audit for recently modified blog posts.
"""
import re
import sys

# ===== PARSE POSTS =====
with open('/root/kanok-miahit/src/app/blog/data.js', 'r') as f:
    lines = f.readlines()

posts = []
current_post = None
in_content = False
content_lines = []

for raw in lines:
    stripped = raw.strip()
    
    if not in_content and stripped.startswith('slug:'):
        slug = stripped.split('"')[1] if '"' in stripped else ''
        current_post = {'slug': slug, 'title': '', 'date': '', 'excerpt': '', 'tags': [], 'content': ''}
    
    elif current_post and not in_content and stripped.startswith('title:'):
        m = re.match(r'title:\s*"(.+)"\s*,?\s*', stripped)
        if m:
            current_post['title'] = m.group(1)
    
    elif current_post and not in_content and stripped.startswith('date:'):
        m = re.match(r'date:\s*"(.+)"\s*,?\s*', stripped)
        if m:
            current_post['date'] = m.group(1)
    
    elif current_post and not in_content and stripped.startswith('excerpt:'):
        excerpt_part = stripped.replace('excerpt:', '').strip().strip(',').strip()
        if excerpt_part.startswith('"') and excerpt_part.endswith('"'):
            current_post['excerpt'] = excerpt_part.strip('"')
        else:
            # Multi-line excerpt
            parts = [excerpt_part]
            for j in range(lines.index(raw)+1, min(lines.index(raw)+10, len(lines))):
                l = lines[j].strip().rstrip(',')
                parts.append(l)
                if l.endswith('"'):
                    break
            current_post['excerpt'] = ' '.join(parts).strip().strip('"')
    
    elif current_post and not in_content and stripped.startswith('tags:'):
        tags_str = stripped.replace('tags:', '').strip().strip(',').strip()
        if tags_str.startswith('[') and tags_str.endswith(']'):
            current_post['tags'] = re.findall(r'"([^"]+)"', tags_str)
        else:
            parts = [tags_str]
            for j in range(lines.index(raw)+1, min(lines.index(raw)+10, len(lines))):
                l = lines[j].strip().rstrip(',')
                parts.append(l)
                if l.endswith(']'):
                    break
            current_post['tags'] = re.findall(r'"([^"]+)"', ' '.join(parts))
    
    elif current_post and not in_content and 'content:' in stripped and stripped.endswith('`') and not stripped.startswith('#'):
        in_content = True
        content_lines = []
    
    elif in_content:
        # Check for content end: backtick followed by comma (backtick is the content delimiter)
        end_match = re.match(r'^(.*?)`\s*,?\s*(//.*)?$', stripped)
        if end_match:
            before_bt = end_match.group(1)
            if before_bt or len(content_lines) > 0:
                if before_bt:
                    content_lines.append(before_bt)
                current_post['content'] = '\n'.join(content_lines)
                posts.append(current_post)
                in_content = False
                current_post = None
                content_lines = []
        else:
            content_lines.append(stripped)

# Build lookup
posts_by_slug = {p['slug']: p for p in posts}
print(f"Parsed {len(posts)} posts successfully", file=sys.stderr)

# ===== MODIFIED POSTS =====
modified_slugs = set()

# From commit 001ef98 (internal linking) - these had content changes
modified_slugs.update([
    "seo-people-also-ask-optimization", "seo-featured-snippet-bangladesh",
    "seo-knowledge-panel-bangladesh", "locksmith-dundee-seo-case-study",
    "das-taxis-scotland-seo-case-study", "morethanpanel-seo-case-study",
    "smmgen-seo-case-study", "smmsun-seo-case-study", "mir-cement-seo-case-study",
    "dhaka-apparels-seo-case-study", "stealth-windshield-repairs-seo-case-study",
    "seo-expert-vs-seo-agency-dhaka-which-is-right", "top-10-seo-mistakes-dhaka-businesses-fix",
    "seo-case-study-dhaka-businesses-increased-organic-traffic",
    "hiring-seo-expert-dhaka-better-roi-than-paid-ads", "watchzonebd-seo-case-study",
])

# From commit cad9c06 (blank line removal - affected many main posts)
modified_slugs.update([
    "complete-seo-guide-bangladesh-businesses-2026",
    "why-ecommerce-store-needs-seo-bangladesh", "technical-seo-checklist-bangladeshi-websites",
    "how-to-choose-right-seo-agency-bangladesh", "link-building-strategies-bangladesh-market",
    "geo-optimization-prepare-business-ai-search", "seo-garments-textile-industry-b2b-lead-generation",
    "google-business-profile-optimization-guide-bangladesh",
    "seo-vs-google-ads-whats-best-bangladesh-businesses", "seo-real-estate-developers-dhaka",
    "mobile-seo-optimization-bangladesh-mobile-first-era",
    "content-marketing-strategy-bangladeshi-brands-seo",
    "international-seo-bangladesh-exporters-global-buyers",
    "seo-bangla-beginners-guide-google-ranking", "local-seo-dhaka-google-maps-ranking",
])

# From commit 5cbb3f7 (HTML entity fix)
modified_slugs.update(["schema-markup-rich-snippets-techniques", "seo-canonical-url-guide-bd"])

# ===== FRAMEWORK CHECKS =====
def extract_primary_keyword(title):
    t = title.lower()
    # Bangla titles: use first meaningful phrase
    if any(ord(c) > 127 for c in t):
        # Bangla text - extract first content phrase
        t = re.sub(r'[ঃ].*$', '', t)  # Remove after colon or similar
        words = t.split()[:4]
        return ' '.join(words) if words else t
    
    # English titles
    for prefix in ['complete ', 'why your ', 'how to ', 'what is ', 'top ',
                   'best ', 'the ', 'a ', 'an ', 'ultimate ', 'seo ']:
        if t.startswith(prefix):
            t = t[len(prefix):]
            break
    t = re.sub(r'\s+(in|for|of|—|:).*$', '', t)
    words = [w for w in t.split() if len(w) > 2][:3]
    if not words:
        words = t.split()[:3]
    return ' '.join(words)

def count_occurrences(text, keyword):
    if not keyword or len(keyword) < 3:
        return 0
    return len(re.findall(re.escape(keyword), text, re.IGNORECASE))

def check_entities(content, title):
    """Check semantic entity coverage"""
    missing = []
    
    # Location checks
    if not re.search(r'\bDhaka\b', content) and 'dhaka' not in title.lower():
        missing.append('Dhaka')
    if not re.search(r'\bBangladesh\b', content) and 'bangladesh' not in title.lower():
        missing.append('Bangladesh')
    
    # Service type
    service_terms = ['SEO', 'search engine optimization', 'digital marketing',
                     'local SEO', 'technical SEO', 'link building', 'content marketing',
                     'on-page', 'off-page', 'Google Business', 'GBP']
    if not any(re.search(term, content, re.IGNORECASE) for term in service_terms):
        missing.append('service_type')
    
    return missing

def find_pillar_links(content, tags, slug):
    """Check pillar page links"""
    pillar_map = {
        'SEO Guide': 'complete-seo-guide-bangladesh-businesses-2026',
        'Local SEO': 'local-seo-tips-dhaka-businesses-google-maps',
        'Technical SEO': 'technical-seo-checklist-bangladeshi-websites',
        'E-commerce SEO': 'why-ecommerce-store-needs-seo-bangladesh',
        'Link Building': 'link-building-strategies-bangladesh-market',
        'GEO': 'geo-optimization-prepare-business-ai-search',
        'Mobile SEO': 'mobile-seo-optimization-bangladesh-mobile-first-era',
        'Content Marketing': 'content-marketing-strategy-bangladeshi-brands-seo',
        'International SEO': 'international-seo-bangladesh-exporters-global-buyers',
        'Google Ads': 'seo-vs-google-ads-whats-best-bangladesh-businesses',
        'Real Estate': 'seo-real-estate-developers-dhaka',
        'Google Business': 'google-business-profile-optimization-guide-bangladesh',
        'Garments SEO': 'seo-garments-textile-industry-b2b-lead-generation',
        'Bangladesh SEO': 'complete-seo-guide-bangladesh-businesses-2026',
        'Digital Marketing': 'complete-seo-guide-bangladesh-businesses-2026',
        '2026': 'seo-trends-2026-ai-geo-future',
        'Case Study': 'seo-case-study-dhaka-businesses-increased-organic-traffic',
        'Google Business Profile': 'google-business-profile-optimization-guide-bangladesh',
        'Google Maps': 'google-business-profile-optimization-guide-bangladesh',
    }
    
    linked = []
    for tag in tags:
        if tag in pillar_map:
            pillar_slug = pillar_map[tag]
            pillar_path = f'/blog/{pillar_slug}'
            if pillar_slug != slug and pillar_path in content:
                linked.append(pillar_path)
    
    # Check for homepage link
    if '(/)' in content:
        linked.append('/ (homepage)')
    
    return list(set(linked))

def count_question_headings(content):
    q_words = r'(?:How|What|Why|When|Where|Can|Do|Is|Are|Does|Which|Who|Should)'
    headings = re.findall(r'^#{1,6}\s+' + q_words + r'\b', content, re.MULTILINE)
    return len(headings)

def count_internal_links(content, slug):
    links = re.findall(r'\((/(?:blog|services|locations|industries|about|contact)/?[^)]*)\)', content)
    non_self = [l for l in links if f'/blog/{slug}' not in l]
    return len(set(non_self))

def check_schema_readiness(post):
    issues = []
    if not post.get('title', '').strip():
        issues.append('title')
    if not post.get('excerpt', '').strip():
        issues.append('excerpt')
    if not post.get('date', '').strip():
        issues.append('date')
    return issues

# ===== GENERATE REPORT =====
print("# Content Framework Audit Report")
print(f"**Generated:** {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')} (cron)")
print(f"**Trigger:** 3 commits in last 48 hours — internal linking, heading cleanup, HTML entity fixes")
print(f"**Posts analyzed:** {len(modified_slugs)}")
print()

# Only process slugs that are found in the parsed data
found_posts = [(slug, posts_by_slug.get(slug)) for slug in sorted(modified_slugs) if slug in posts_by_slug]
not_found = [slug for slug in sorted(modified_slugs) if slug not in posts_by_slug]

if not_found:
    print(f"ℹ️  Skipped {len(not_found)} slugs not found in data.js (may be in different section)")
    print()

all_pass = True

for slug, post in found_posts:
    content = post['content']
    title = post['title']
    tags = post['tags']
    
    print(f"## Post: {slug}")
    print(f"**Title:** {title}")
    print(f"**Tags:** {', '.join(tags)}")
    print()
    print("| Check | Status | Details |")
    print("|-------|--------|---------|")
    
    # A. TF-IDF Coverage
    keyword = extract_primary_keyword(title)
    kw_count = count_occurrences(content, keyword)
    kw_status = "✅" if kw_count >= 5 else "❌"
    if kw_status == "❌":
        all_pass = False
    print(f"| TF-IDF: \"{keyword}\" | {kw_status} | {kw_count} occurrences |")
    
    # B. Entities
    missing_entities = check_entities(content, title)
    entity_status = "✅" if len(missing_entities) == 0 else "❌"
    if entity_status == "❌":
        all_pass = False
    entity_detail = "All key entities present" if not missing_entities else f"Missing: {', '.join(missing_entities)}"
    print(f"| Entities | {entity_status} | {entity_detail} |")
    
    # C. Pillar Link
    pillar_links = find_pillar_links(content, tags, slug)
    pillar_status = "✅" if pillar_links else "❌"
    if pillar_status == "❌":
        all_pass = False
    pillar_detail = ', '.join(pillar_links) if pillar_links else "No pillar link found"
    print(f"| Pillar Link | {pillar_status} | {pillar_detail} |")
    
    # D. AEO/GEO
    q_count = count_question_headings(content)
    q_status = "✅" if q_count >= 2 else "❌"
    if q_status == "❌":
        all_pass = False
    print(f"| AEO/GEO | {q_status} | {q_count} question headings |")
    
    # E. Internal Links
    link_count = count_internal_links(content, slug)
    link_status = "✅" if link_count >= 3 else "❌"
    if link_status == "❌":
        all_pass = False
    print(f"| Internal Links | {link_status} | {link_count} unique internal links |")
    
    # F. Schema
    schema_issues = check_schema_readiness(post)
    schema_status = "✅" if len(schema_issues) == 0 else "❌"
    if schema_status == "❌":
        all_pass = False
    schema_detail = "All fields set" if not schema_issues else f"Missing: {', '.join(schema_issues)}"
    print(f"| Schema Ready | {schema_status} | {schema_detail} |")
    
    print()

# Summary
print("---")
if all_pass:
    print("## ✅ Overall: All framework checks pass for modified posts!")
else:
    print("## ⚠ Overall: Some posts need attention (flags above)")
print()
print("### Legend")
print("- **TF-IDF:** Primary keyword should appear ≥5 times for topical relevance")
print("- **Entities:** Location (Dhaka & Bangladesh), service type must be present")
print("- **Pillar Link:** Posts should link back to their topic cluster hub page")
print("- **AEO/GEO:** ≥2 question-based headings for AI/voice search optimization")
print("- **Internal Links:** ≥3 internal links to other posts, services, or locations")
print("- **Schema Ready:** title + excerpt + date needed for ArticleSchema markup")
