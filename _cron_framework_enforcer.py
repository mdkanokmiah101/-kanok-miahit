#!/usr/bin/env python3
"""Content Framework Enforcer for kanokmiah.com.bd — cron run."""

import re
import json
import math

MODIFIED_SLUGS = [
    "das-taxis-scotland-seo-case-study",
    "dhaka-apparels-seo-case-study",
    "hiring-seo-expert-dhaka-better-roi-than-paid-ads",
    "locksmith-dundee-seo-case-study",
    "mir-cement-seo-case-study",
    "morethanpanel-seo-case-study",
    "seo-case-study-dhaka-businesses-increased-organic-traffic",
    "seo-expert-vs-seo-agency-dhaka-which-is-right",
    "smmgen-seo-case-study",
    "smmsun-seo-case-study",
    "stealth-windshield-repairs-seo-case-study",
    "top-10-seo-mistakes-dhaka-businesses-fix",
    "watchzonebd-seo-case-study",
]

DATA_FILE = "/root/kanok-miahit/src/app/blog/data.js"

# ============================================================
# 1. PARSE posts from data.js
# ============================================================
def parse_posts(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    # Remove module.exports if present
    text = re.sub(r'module\.exports\s*=.*', '', text)

    # Find the posts array
    m = re.search(r'const\s+posts\s*=\s*\[(.*)\]', text, re.DOTALL)
    if not m:
        raise ValueError("Could not find posts array in data.js")
    array_body = m.group(1)

    # We'll extract objects by tracking brace depth
    posts_raw = []
    depth = 0
    start = None
    for i, ch in enumerate(array_body):
        if ch == '{':
            if depth == 0:
                start = i
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0 and start is not None:
                posts_raw.append(array_body[start:i+1])
                start = None

    posts = []
    for raw in posts_raw:
        post = {}
        # Extract slug
        slug_m = re.search(r'''slug:\s*["']([^"']+)["']''', raw)
        post['slug'] = slug_m.group(1) if slug_m else None
        # Extract title
        title_m = re.search(r'''title:\s*["']([^"']+)["']''', raw)
        post['title'] = title_m.group(1) if title_m else None
        # Extract date
        date_m = re.search(r'''date:\s*["']([^"']+)["']''', raw)
        post['date'] = date_m.group(1) if date_m else None
        # Extract excerpt
        excerpt_m = re.search(r'''excerpt:\s*["']([^"']+)["']''', raw)
        post['excerpt'] = excerpt_m.group(1) if excerpt_m else None
        # Extract tags
        tags_m = re.search(r'tags:\s*\[([^\]]+)\]', raw)
        if tags_m:
            tags_str = tags_m.group(1)
            post['tags'] = re.findall(r"""["']([^"']+)["']""", tags_str)
        else:
            post['tags'] = []
        # Extract content (backtick string)
        content_m = re.search(r'content:\s*`(.*)`', raw, re.DOTALL)
        if content_m:
            post['content'] = content_m.group(1)
        else:
            post['content'] = ''
        if post['slug']:
            posts.append(post)
    return posts

posts = parse_posts(DATA_FILE)
print(f"Parsed {len(posts)} posts total.")

# Build lookup
post_map = {p['slug']: p for p in posts}

# ============================================================
# 2. Framework checks
# ============================================================
def extract_primary_keyword(title):
    """Extract first meaningful noun phrase from title as primary keyword."""
    if not title:
        return "unknown"
    # Remove special chars for analysis
    t = title.lower().strip()
    # Common patterns: "X for Y", "X in Y", "X: Y", "X — Y"
    # Try to get the first noun-phrase
    # Simplistic: first 2-4 words that aren't stopwords
    stopwords = {'a', 'an', 'the', 'for', 'in', 'of', 'to', 'and', 'is', 'are', 'was', 'were', 'how', 'what', 'why', 'when', 'where', 'do', 'does', 'did'}
    words = t.split()
    # Skip leading stopwords
    kw_parts = []
    for w in words:
        if w in stopwords and not kw_parts:
            continue
        kw_parts.append(w)
        if len(kw_parts) >= 3:
            break
    if not kw_parts:
        kw_parts = words[:2]
    return ' '.join(kw_parts)

def check_tfidf(post):
    keyword = extract_primary_keyword(post.get('title', ''))
    content = post.get('content', '')
    # Count occurrences (case-insensitive)
    count = content.lower().count(keyword.lower())
    # Also try first 2 words as fallback
    if count < 5 and len(keyword.split()) > 2:
        bigram = ' '.join(keyword.split()[:2])
        count2 = content.lower().count(bigram.lower())
        if count2 > count:
            count = count2
    passed = count >= 5
    return keyword, passed, count

def check_entities(post):
    """Check key semantic entities."""
    content = post.get('content', '')
    title = post.get('title', '')
    slug = post.get('slug', '')
    content_lower = content.lower()
    
    entities_needed = []
    
    # Location entities
    locations_present = []
    for loc in ['dhaka', 'bangladesh']:
        if loc in content_lower:
            locations_present.append(loc)
    
    if 'dhaka' not in content_lower:
        entities_needed.append('Dhaka')
    if 'bangladesh' not in content_lower:
        entities_needed.append('Bangladesh')
    
    # Service type (SEO-related)
    seo_services = ['seo', 'search engine optimization', 'local seo', 'technical seo', 'on-page seo']
    service_found = any(s.lower() in content_lower for s in seo_services)
    if not service_found:
        entities_needed.append('SEO service')
    
    # Check for specific industry/location mentioned in slug
    slug_lower = slug.lower()
    # Extract potential industry from slug
    industry_terms = ['garments', 'textile', 'ecommerce', 'real estate', 'restaurant', 'locksmith', 'taxis', 'taxi', 
                      'cement', 'apparels', 'windshield', 'auto', 'watch', 'social media', 'panel']
    slug_industries = [t for t in industry_terms if t in slug_lower]
    for ind in slug_industries:
        if ind not in content_lower:
            entities_needed.append(f'{ind.title()} (from slug)')
    
    # Check for location in slug
    if 'scotland' in slug_lower and 'scotland' not in content_lower:
        entities_needed.append('Scotland')
    if 'dundee' in slug_lower and 'dundee' not in content_lower:
        entities_needed.append('Dundee')
    
    # Check for kanok miah (expert name)
    if 'kanok miah' not in content_lower and 'kanok' not in content_lower:
        entities_needed.append('Kanok Miah (author)')
    
    passed = len(entities_needed) == 0
    return passed, entities_needed, locations_present

def check_pillar_link(post):
    """Check if post links to pillar page based on tags."""
    tags = post.get('tags', [])
    content = post.get('content', '')
    slug = post.get('slug', '')
    
    pillar_pages = {
        'SEO Guide': '/blog/complete-seo-guide-bangladesh-businesses-2026',
        'Bangladesh SEO': '/blog/complete-seo-guide-bangladesh-businesses-2026',
        'Local SEO': '/blog/local-seo-tips-dhaka-businesses-google-maps',
        'Technical SEO': '/blog/technical-seo-checklist-bangladeshi-websites',
        'Keyword Research': '/blog/keyword-research-bangladesh-market',
        'Link Building': '/blog/link-building-bangladesh-strategies',
        'Content Marketing': '/blog/content-marketing-seo-friendly-content-writing',
        'Mobile SEO': '/blog/mobile-seo-bangladesh-ranking-strategy',
        'E-commerce SEO': '/blog/ecommerce-seo-daraz-shopify-guide',
        'YouTube SEO': '/blog/youtube-seo-bangladesh-ranking-tips',
    }
    
    # Find possible pillar pages
    linked_pillars = []
    for tag, pillar_url in pillar_pages.items():
        if tag in tags:
            # Check if the url or a /blog/ link to a similar topic is in content
            pillar_slug = pillar_url.split('/')[-1]
            if pillar_url.split('/')[-1] in content or pillar_url in content:
                linked_pillars.append(pillar_url)
    
    # Also check for generic pillar link to homepage
    if not linked_pillars:
        # Check for links to main SEO guide or other major pillars
        guide_patterns = [
            '/blog/complete-seo-guide-bangladesh-businesses-2026',
            '/blog/local-seo-tips-dhaka-businesses-google-maps',
            '/blog/technical-seo-checklist-bangladeshi-websites',
        ]
        for gp in guide_patterns:
            slug_part = gp.split('/')[-1]
            if slug_part in content or gp in content:
                linked_pillars.append(gp)
    
    passed = len(linked_pillars) > 0
    pillar_str = ', '.join(linked_pillars) if linked_pillars else 'None'
    # Determine which pillar based on tags
    pillar_topic = ' / '.join([t for t in tags if t in pillar_pages]) if any(t in pillar_pages for t in tags) else 'General'
    return passed, pillar_str, pillar_topic

def check_aeo_geo(post):
    """Count question-based headings."""
    content = post.get('content', '')
    # Count lines that are markdown headings starting with question words
    heading_lines = re.findall(r'^#{1,6}\s+(.+)$', content, re.MULTILINE)
    q_words = ['how', 'what', 'why', 'when', 'where', 'can', 'do', 'is', 'are', 'does', 'did', 'which', 'who']
    count = 0
    for h in heading_lines:
        first_word = h.strip().lower().split()[0] if h.strip().split() else ''
        # Remove punctuation from first word
        first_word = first_word.strip('?,.:;!-')
        if first_word in q_words:
            count += 1
    passed = count >= 2
    return passed, count

def check_internal_links(post):
    """Count internal links."""
    content = post.get('content', '')
    # Match markdown links starting with / (internal)
    internal_links = re.findall(r'\[([^\]]+)\]\((/[^)]+)\)', content)
    # Also match bare /blog/ or /services/ URLs
    bare_internal = re.findall(r'(?<=\s)(/blog/[^\s)\]]+|/services/[^\s)\]]+|/locations/[^\s)\]]+)', content)
    all_internal = set()
    for text, url in internal_links:
        all_internal.add(url)
    for url in bare_internal:
        url = url.rstrip('.,;:!?)')
        all_internal.add(url)
    count = len(all_internal)
    passed = count >= 3
    return passed, count, sorted(all_internal)

def check_schema(post):
    """Check schema readiness (title, excerpt, date)."""
    issues = []
    if not post.get('title'):
        issues.append('title missing')
    if not post.get('excerpt'):
        issues.append('excerpt missing')
    if not post.get('date'):
        issues.append('date missing')
    passed = len(issues) == 0
    return passed, issues

# ============================================================
# 3. Generate report
# ============================================================
report_parts = []
all_passed = True

for slug in MODIFIED_SLUGS:
    post = post_map.get(slug)
    if not post:
        report_parts.append(f"\n## Post: {slug}\n| Check | Status | Details |\n|-------|--------|---------|\n| **⚠️** | **NOT FOUND** | Post slug not in parsed data |\n")
        all_passed = False
        continue
    
    title = post.get('title', 'Untitled')
    
    # A. TF-IDF
    keyword, tfidf_pass, tfidf_count = check_tfidf(post)
    tfidf_status = '✅' if tfidf_pass else '❌'
    if not tfidf_pass:
        all_passed = False
    
    # B. Entities
    entities_pass, missing_entities, found_locs = check_entities(post)
    entities_status = '✅' if entities_pass else '❌'
    entities_detail = 'Missing: ' + ', '.join(missing_entities) if missing_entities else f'Locations: {", ".join(found_locs)}' if found_locs else 'All key entities found'
    if not entities_pass:
        all_passed = False
    
    # C. Pillar link
    pillar_pass, pillar_links, pillar_topic = check_pillar_link(post)
    pillar_status = '✅' if pillar_pass else '❌'
    pillar_detail = f'Links to: {pillar_links}' if pillar_links else f'Pillar: {pillar_topic} — no link found'
    if not pillar_pass:
        all_passed = False
    
    # D. AEO/GEO
    aeo_pass, q_count = check_aeo_geo(post)
    aeo_status = '✅' if aeo_pass else '❌'
    if not aeo_pass:
        all_passed = False
    
    # E. Internal links
    link_pass, link_count, link_urls = check_internal_links(post)
    link_status = '✅' if link_pass else '❌'
    if not link_pass:
        all_passed = False
    
    # F. Schema
    schema_pass, schema_issues = check_schema(post)
    schema_status = '✅' if schema_pass else '❌'
    schema_detail = 'All fields set' if schema_pass else 'Missing: ' + ', '.join(schema_issues)
    if not schema_pass:
        all_passed = False
    
    report_parts.append(f"""## Post: {slug}
**Title:** {title}

| Check | Status | Details |
|-------|--------|---------|
| **TF-IDF:** `{keyword}` | {tfidf_status} | {tfidf_count} occurrences |
| **Entities** | {entities_status} | {entities_detail} |
| **Pillar Link** | {pillar_status} | {pillar_detail} |
| **AEO/GEO** | {aeo_status} | {q_count} question headings |
| **Internal Links** | {link_status} | {link_count} total |
| **Schema Ready** | {schema_status} | {schema_detail} |

""")
    
    # Build fix instructions
    fix_parts = []
    if not tfidf_pass:
        fix_parts.append(f"- 🔤 **TF-IDF:** Use `{keyword}` at least 5 times in content (currently {tfidf_count}). Add naturally in headings, first paragraph, and key sections.")
    if not entities_pass:
        fix_parts.append(f"- 🏷️ **Entities:** Add missing entities: {', '.join(missing_entities)}. Include at minimum 'Dhaka'/'Bangladesh' location context and service type (SEO).")
    if not pillar_pass:
        fix_parts.append(f"- 🔗 **Pillar Link:** Link to pillar page for '{pillar_topic}'. Suggested: `/blog/complete-seo-guide-bangladesh-businesses-2026` or relevant pillar.")
    if not aeo_pass:
        fix_parts.append(f"- ❓ **AEO/GEO:** Add {2 - q_count} more question-based headings (starting with How/What/Why/Can/Do/Is/Are).")
    if not link_pass:
        missing_links = 3 - link_count
        fix_parts.append(f"- 🔗 **Internal Links:** Add at least {missing_links} more internal links to other posts, services, or location pages.")
    if not schema_pass:
        fix_parts.append(f"- 📋 **Schema:** Set missing fields: {', '.join(schema_issues)}. All of title, excerpt, and date are needed for ArticleSchema.")
    
    if fix_parts:
        report_parts.append("### Fix instructions:\n" + "\n".join(fix_parts) + "\n")

# Summary
total_posts = len([s for s in MODIFIED_SLUGS if s in post_map])
passed_posts = sum(1 for slug in MODIFIED_SLUGS if slug in post_map and 
                   check_tfidf(post_map[slug])[0] and 
                   check_entities(post_map[slug])[0] and 
                   check_pillar_link(post_map[slug])[0] and 
                   check_aeo_geo(post_map[slug])[0] and 
                   check_internal_links(post_map[slug])[0] and 
                   check_schema(post_map[slug])[0])

summary = f"""=====================================================
📊 CONTENT FRAMEWORK ENFORCEMENT REPORT
=====================================================
🕐 Generated: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
📝 Modified posts checked: {total_posts}
✅ All checks passed: {passed_posts}/{total_posts}
❌ Posts needing fixes: {total_posts - passed_posts}
=====================================================

"""
report_parts.insert(0, summary)
print("".join(report_parts))
