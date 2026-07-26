#!/usr/bin/env python3
"""
Content Framework Enforcer for kanokmiah.com.bd
Line-based parser for large JS data file.
"""
import re
import sys

with open('/root/kanok-miahit/src/app/blog/data.js', 'r') as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}", file=sys.stderr)

# Parse posts using line-by-line state machine
posts = []
current_post = None
in_content = False
content_lines = []

for i, line in enumerate(lines):
    stripped = line.strip()
    
    # Detect slug line
    if not in_content and stripped.startswith('slug:'):
        slug = stripped.split('"')[1] if '"' in stripped else ''
        current_post = {'slug': slug, 'title': '', 'date': '', 'excerpt': '', 'tags': [], 'content': '', 'line_start': i + 1}
    
    # Detect title
    if current_post and not in_content and stripped.startswith('title:'):
        title_match = re.match(r'title:\s*"(.+)"\s*,?\s*', stripped)
        if title_match:
            current_post['title'] = title_match.group(1)
    
    # Detect date
    if current_post and not in_content and stripped.startswith('date:'):
        date_match = re.match(r'date:\s*"(.+)"\s*,?\s*', stripped)
        if date_match:
            current_post['date'] = date_match.group(1)
    
    # Detect excerpt
    if current_post and not in_content and stripped.startswith('excerpt:'):
        # May span multiple lines
        excerpt = stripped.replace('excerpt:', '').strip().strip(',').strip()
        if excerpt.startswith('"') and excerpt.endswith('"'):
            current_post['excerpt'] = excerpt.strip('"')
        else:
            # Multi-line excerpt - collect
            excerpt_lines = [excerpt]
            j = i + 1
            while j < len(lines):
                l = lines[j].strip().rstrip(',')
                excerpt_lines.append(l)
                if l.endswith('"'):
                    break
                j += 1
            full = ' '.join(excerpt_lines).strip().strip('"')
            current_post['excerpt'] = full
    
    # Detect tags
    if current_post and not in_content and stripped.startswith('tags:'):
        tags_str = stripped.replace('tags:', '').strip().strip(',').strip()
        if tags_str.startswith('[') and tags_str.endswith(']'):
            # Single line
            tags = re.findall(r'"([^"]+)"', tags_str)
            current_post['tags'] = tags
        else:
            # Multi-line
            tags_parts = [tags_str]
            j = i + 1
            while j < len(lines):
                l = lines[j].strip().rstrip(',')
                tags_parts.append(l)
                if l.endswith(']'):
                    break
                j += 1
            full = ' '.join(tags_parts)
            tags = re.findall(r'"([^"]+)"', full)
            current_post['tags'] = tags
    
    # Detect content start
    if current_post and not in_content and 'content:' in stripped and stripped.endswith('`') and not stripped.startswith('#'):
        in_content = True
        content_lines = []
        # Check if content is on same line as ` or on next line
        if stripped.strip() == 'content: `' or stripped.strip() == 'content:`':
            # Content starts on next line
            pass
        else:
            # Content starts inline after `content: ` - extract text after backtick
            content_start = stripped.find('`') + 1
            rest = stripped[content_start:]
            if rest:
                # Remove trailing comma and comment
                rest = re.sub(r'`.*$', '', rest)
                content_lines.append(rest)
    
    # Collect content lines
    if in_content:
        # Check if this line (or its stripped version) ends the content
        # Look for closing backtick followed by comma (possibly with comment)
        end_match = re.match(r'^(.*?)`\s*,?\s*(//.*)?$', stripped)
        if end_match and end_match.group(1) is not None:
            # Might be the end
            before_backtick = end_match.group(1)
            if before_backtick or len(content_lines) > 0:
                # End of content
                if before_backtick:
                    content_lines.append(before_backtick)
                current_post['content'] = '\n'.join(content_lines)
                current_post['line_end'] = i + 1
                posts.append(current_post)
                current_post = None
                in_content = False
                content_lines = []
                continue
        else:
            # Check if line is just closing backtick
            if stripped.startswith('`'):
                # This line starts with backtick - it's the closing delimiter
                # Content is everything collected so far
                content_after = stripped[1:].strip()
                if content_after and not content_after.startswith(','):
                    # There's text after the backtick - add it?
                    # Actually this shouldn't happen in template literals
                    pass
                current_post['content'] = '\n'.join(content_lines)
                current_post['line_end'] = i + 1
                posts.append(current_post)
                current_post = None
                in_content = False
                content_lines = []
                continue
            else:
                content_lines.append(stripped)

print(f"Parsed posts: {len(posts)}", file=sys.stderr)

# Verify
for p in posts[:3]:
    print(f"  {p['slug']}: {p['title'][:50]}... content length={len(p['content'])}", file=sys.stderr)

# Check for which slugs were modified
modified_slugs = {
    # From commit 001ef98 (internal linking)
    "seo-people-also-ask-optimization",
    "seo-featured-snippet-bangladesh", 
    "seo-knowledge-panel-bangladesh",
    "locksmith-dundee-seo-case-study",
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
    "watchzonebd-seo-case-study",
    # From commit cad9c06 (blank line removal) - extract from diff
    "complete-seo-guide-bangladesh-businesses-2026",
    "why-ecommerce-store-needs-seo-bangladesh",
    "technical-seo-checklist-bangladeshi-websites",
    "how-to-choose-right-seo-agency-bangladesh",
    "link-building-strategies-bangladesh-market",
    "geo-optimization-prepare-business-ai-search",
    "seo-garments-textile-industry-b2b-lead-generation",
    "google-business-profile-optimization-guide-bangladesh",
    "seo-vs-google-ads-whats-best-bangladesh-businesses",
    "seo-real-estate-developers-dhaka",
    "mobile-seo-optimization-bangladesh-mobile-first-era",
    "content-marketing-strategy-bangladeshi-brands-seo",
    "international-seo-bangladesh-exporters-global-buyers",
    "seo-bangla-beginners-guide-google-ranking",
    "local-seo-dhaka-google-maps-ranking",
    # From commit 5cbb3f7 (HTML entity fix)
    "schema-markup-rich-snippets-techniques",
    "seo-canonical-url-guide-bd",
}

# Build lookup
posts_by_slug = {p['slug']: p for p in posts}

# Check which modified slugs are found
found_slugs = []
not_found_slugs = []
for s in sorted(modified_slugs):
    if s in posts_by_slug:
        found_slugs.append(s)
    else:
        not_found_slugs.append(s)

if not_found_slugs:
    print(f"NOT FOUND in parsed data: {not_found_slugs}", file=sys.stderr)

print(f"Found slugs to check: {found_slugs}", file=sys.stderr)

# =============================================
# Framework Checks
# =============================================

def extract_primary_keyword(title):
    """Extract primary keyword from title"""
    t = title.lower()
    # Remove common prefixes
    for prefix in ['complete ', 'why your ', 'how to ', 'what is ', 'top ', 'best ', 
                   'the ', 'a ', 'an ', 'ultimate ', 'seo ']:
        if t.startswith(prefix):
            t = t[len(prefix):]
            break
    # Remove trailing location/context qualifiers
    t = re.sub(r'\s+(in|for|of|—|:).*$', '', t)
    # Take first 2-3 meaningful words
    words = [w for w in t.split() if len(w) > 2][:3]
    if not words:
        words = t.split()[:3]
    return ' '.join(words) if words else title.split()[:3]

def count_occurrences(text, keyword):
    if not keyword:
        return 0
    return len(re.findall(re.escape(keyword), text, re.IGNORECASE))

def check_entities(content):
    """Check semantic entity coverage"""
    location_found = {
        'Dhaka': bool(re.search(r'\bDhaka\b', content)),
        'Bangladesh': bool(re.search(r'\bBangladesh\b', content)),
    }
    service_terms = ['SEO', 'search engine optimization', 'digital marketing', 
                     'local SEO', 'technical SEO', 'link building', 'content marketing',
                     'on-page', 'off-page', 'Google Business']
    service_found = any(re.search(term, content, re.IGNORECASE) for term in service_terms)
    
    industry_terms = ['e-commerce', 'ecommerce', 'real estate', 'healthcare', 'medical',
                      'garment', 'textile', 'education', 'restaurant', 'hotel', 'travel',
                      'B2B', 'startup', 'legal', 'fitness', 'photography', 'event',
                      'non-profit', 'NGO', 'export', 'cleaning', 'salon']
    industry_found = any(re.search(term, content, re.IGNORECASE) for term in industry_terms)
    
    missing = []
    if not location_found['Dhaka']:
        missing.append('Dhaka')
    if not location_found['Bangladesh']:
        missing.append('Bangladesh')
    if not service_found:
        missing.append('service_type')
    
    return missing, {'Dhaka': location_found['Dhaka'], 'Bangladesh': location_found['Bangladesh'], 'service': service_found, 'industry': industry_found}

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
    }
    
    linked = []
    for tag in tags:
        if tag in pillar_map:
            pillar_slug = pillar_map[tag]
            pillar_path = f'/blog/{pillar_slug}'
            if pillar_slug != slug and pillar_path in content:
                linked.append(pillar_path)
    
    # Also check for homepage link (/)
    if '(/)' in content or '(/)' in content:
        linked.append('/ (homepage)')
    
    return linked

def count_question_headings(content):
    q_words = r'(?:How|What|Why|When|Where|Can|Do|Is|Are|Does|Which|Who|Should)'
    headings = re.findall(r'^#{1,6}\s+' + q_words + r'\b', content, re.MULTILINE)
    return len(headings)

def count_internal_links(content, slug):
    links = re.findall(r'\((/(?:blog|services|locations|industries|about|contact)/?[^)]*)\)', content)
    # Filter out self-references
    non_self = [l for l in links if f'/blog/{slug}' not in l]
    unique = set(non_self)
    return len(unique)

def check_schema_readiness(post):
    issues = []
    if not post.get('title', '').strip():
        issues.append('title')
    excerpt = post.get('excerpt', '').strip()
    if not excerpt:
        issues.append('excerpt')
    if not post.get('date', '').strip():
        issues.append('date')
    return issues

# Generate report
print("# Content Framework Audit Report")
print(f"**Generated:** Cron job — 2026-07-21")
print(f"**Trigger:** 3 commits in last 48 hours with changes to blog posts")
print(f"**Posts analyzed:** {len(found_slugs)}")
print()

all_pass = True

for slug in sorted(found_slugs):
    post = posts_by_slug[slug]
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
    missing_entities, entity_details = check_entities(content)
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

print("---")
if all_pass:
    print("## ✅ Overall: All framework checks pass!")
else:
    print("## ⚠ Overall: Some posts need attention (flagged above)")
print()
print("### Legend")
print("- **TF-IDF:** Primary keyword should appear ≥5 times for topical relevance")
print("- **Entities:** Location (Dhaka & Bangladesh), service type, industry context must be present")
print("- **Pillar Link:** Posts should link back to their pillar/topic cluster hub")
print("- **AEO/GEO:** ≥2 question-based headings for AI/voice search optimization")
print("- **Internal Links:** ≥3 internal links to other posts, services, or locations")
print("- **Schema Ready:** title + excerpt + date needed for ArticleSchema markup")
