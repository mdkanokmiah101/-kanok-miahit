#!/usr/bin/env python3
"""Framework enforcer: run TF-IDF, Entity, Pillar, AEO/GEO, Internal Links, Schema checks on all blog posts."""

import re
import sys
import json

# Read the data.js file
with open('src/app/blog/data.js', 'r') as f:
    content = f.read()

# Parse posts from the JS array
# Each post starts with `  {` and the slug line, ends before the next `  {` or `];`
posts_raw = re.findall(r'\s*\{\n\s*slug: "([^"]+)",\n.*?\n\s*\},?\n(?=\s*\{|\s*\];)', content, re.DOTALL)

print(f"Found {len(posts_raw)} posts in data.js\n")

# Also try a simpler approach - find each post block
post_entries = re.finditer(
    r'\{[\s\n]*slug:\s*"([^"]+)"[\s\S]*?(?=\n\s*\},?\n\s*(?:\{|\[))',
    content
)

pairs = []
for m in re.finditer(r'slug:\s*"([^"]+)"', content):
    slug = m.group(1)
    # Find the start of this post object
    start = content.rfind('{', 0, m.start())
    # Find the end - the next `},` or `} ];`
    rest = content[m.end():]
    # Find the closing brace at the post level
    depth = 0
    end = m.end()
    for i in range(m.end(), len(content)):
        if content[i] == '{':
            depth += 1
        elif content[i] == '}':
            if depth == 0:
                end = i + 1
                break
            depth -= 1
    pairs.append((slug, content[start:end]))

print(f"Parsed {len(pairs)} post entries\n")

def extract_field(post_text, field):
    """Extract a field value from a post object."""
    # Match field: "value" or field: `value`
    m = re.search(rf'{field}:\s*"([^"]*)"', post_text)
    if m:
        return m.group(1)
    m = re.search(rf'{field}:\s*`', post_text)
    if m:
        # Content is in backticks, find the closing backtick
        start = m.end()
        # Find the matching closing backtick (not escaped)
        idx = post_text.find('`', start)
        if idx != -1:
            return post_text[start:idx]
    return None

def extract_tags(post_text):
    """Extract tags array."""
    m = re.search(r'tags:\s*\[([^\]]*)\]', post_text)
    if m:
        tags_str = m.group(1)
        tags = re.findall(r'"([^"]*)"', tags_str)
        return tags
    return []

def count_internal_links(content_text):
    """Count internal links - links to /blog/, /locations/, /services/, /industries/, /about, /contact."""
    links = re.findall(r'\[([^\]]*)\]\((/[^)]*)\)', content_text)
    internal = []
    for text, url in links:
        if any(url.startswith(p) for p in ['/blog/', '/locations/', '/services/', '/industries/', '/about', '/contact', '/']):
            if url != '/' or text:
                internal.append((text, url))
    return internal

def count_question_headings(content_text):
    """Count question-based headings (## or ### starting with question words)."""
    headings = re.findall(r'^#{2,3}\s+(How|What|Why|When|Where|Can|Do|Is|Are|Does|Which)\b', content_text, re.MULTILINE)
    return headings

def get_primary_keyword(title):
    """Extract primary keyword from title."""
    # Take first meaningful noun phrase - simple heuristic
    # Strip trailing year/location qualifiers
    # For SEO-related titles, extract the main topic
    title_lower = title.lower()
    
    # Common patterns
    patterns = [
        r'(seo)\b',
        r'(local seo)',
        r'(link building)',
        r'(technical seo)',
        r'(e-commerce seo)',
        r'(content marketing)',
        r'(keyword research)',
        r'(google business profile)',
        r'(voice search)',
        r'(mobile seo)',
        r'(schema markup)',
        r'(geo)\b',
        r'(aeo)\b',
        r'(generative engine optimization)',
    ]
    
    for p in patterns:
        m = re.search(p, title_lower)
        if m:
            return m.group(1)
    
    # Fallback: first 1-2 words
    words = title_lower.split()[:3]
    return ' '.join(words)

def check_tfidf(content_text, title, min_occurrences=5):
    """A: Check TF-IDF - primary keyword occurrence count."""
    keyword = get_primary_keyword(title)
    count = len(re.findall(re.escape(keyword), content_text, re.IGNORECASE))
    passed = count >= min_occurrences
    return keyword, count, passed

def check_entities(content_text):
    """B: Check entity coverage."""
    required_entities = {
        'Dhaka': r'\bDhaka\b',
        'Bangladesh': r'\bBangladesh\b',
        'Kanok Miah': r'Kanok Miah',
    }
    
    missing = []
    for entity, pattern in required_entities.items():
        if not re.search(pattern, content_text):
            missing.append(entity)
    
    # Check for service type
    service_indicators = ['SEO', 'optimization', 'ranking', 'search engine']
    has_service = any(s.lower() in content_text.lower() for s in service_indicators)
    if not has_service:
        missing.append('Service type (SEO/optimization)')
    
    # Check for industry
    industry_indicators = ['e-commerce', 'retail', 'restaurant', 'healthcare', 'real estate', 
                          'garment', 'education', 'cleaning', 'salon', 'travel', 'legal']
    has_industry = any(i.lower() in content_text.lower() for i in industry_indicators)
    if not has_industry:
        missing.append('Industry reference')
    
    passed = len(missing) == 0
    return missing, passed

def get_pillar_topic(tags, title):
    """C: Determine pillar topic from tags."""
    tag_lower = [t.lower() for t in tags]
    title_lower = title.lower()
    
    pillar_map = {
        'SEO Guide': ('SEO Fundamentals', '/blog/complete-seo-guide-bangladesh-businesses-2026'),
        'Bangladesh SEO': ('SEO Fundamentals', '/blog/complete-seo-guide-bangladesh-businesses-2026'),
        'Local SEO': ('Local SEO', '/blog/local-seo-tips-dhaka-businesses-google-maps'),
        'E-commerce SEO': ('E-commerce SEO', '/blog/why-ecommerce-store-needs-seo-bangladesh'),
        'Technical SEO': ('Technical SEO', '/blog/technical-seo-checklist-bangladeshi-websites'),
        'Link Building': ('Link Building', '/blog/link-building-strategies-bangladesh-market'),
        'GEO': ('GEO/AI Search', '/blog/geo-optimization-prepare-business-ai-search'),
        'AI Search': ('GEO/AI Search', '/blog/geo-optimization-prepare-business-ai-search'),
        'Content Marketing': ('Content Marketing', '/blog/content-marketing-strategy-bangladeshi-brands-seo'),
        'GBP': ('Local SEO', '/blog/local-seo-tips-dhaka-businesses-google-maps'),
        'Google Maps': ('Local SEO', '/blog/local-seo-tips-dhaka-businesses-google-maps'),
        'Schema': ('Technical SEO', '/blog/technical-seo-checklist-bangladeshi-websites'),
        'Core Web Vitals': ('Technical SEO', '/blog/technical-seo-checklist-bangladeshi-websites'),
        'Mobile': ('Technical SEO', '/blog/technical-seo-checklist-bangladeshi-websites'),
        'Voice Search': ('SEO Trends', '/blog/seo-trends-2026-ai-geo-future'),
        'SEO Trends': ('SEO Trends', '/blog/seo-trends-2026-ai-geo-future'),
        'Case Study': ('Case Studies', None),
        'E-commerce': ('E-commerce SEO', '/blog/why-ecommerce-store-needs-seo-bangladesh'),
        'Daraz': ('E-commerce SEO', '/blog/why-ecommerce-store-needs-seo-bangladesh'),
        'Shopify': ('E-commerce SEO', '/blog/why-ecommerce-store-needs-seo-bangladesh'),
    }
    
    for tag in tag_lower:
        for key, (pillar, url) in pillar_map.items():
            if key.lower() in tag:
                return pillar, url
    
    # Try to infer from title
    if 'local' in title_lower or 'maps' in title_lower or 'gbp' in title_lower:
        return ('Local SEO', '/blog/local-seo-tips-dhaka-businesses-google-maps')
    if 'ecommerce' in title_lower or 'e-commerce' in title_lower or 'shopify' in title_lower or 'daraz' in title_lower:
        return ('E-commerce SEO', '/blog/why-ecommerce-store-needs-seo-bangladesh')
    if 'technical' in title_lower or 'core web' in title_lower or 'schema' in title_lower:
        return ('Technical SEO', '/blog/technical-seo-checklist-bangladeshi-websites')
    if 'link building' in title_lower or 'backlink' in title_lower:
        return ('Link Building', '/blog/link-building-strategies-bangladesh-market')
    if 'geo' in title_lower or 'ai search' in title_lower or 'generative' in title_lower:
        return ('GEO/AI Search', '/blog/geo-optimization-prepare-business-ai-search')
    if 'content' in title_lower:
        return ('Content Marketing', '/blog/content-marketing-strategy-bangladeshi-brands-seo')
    if 'case study' in title_lower:
        return ('Case Studies', None)
    
    return ('Unknown', None)

def check_pillar_link(content_text, pillar_url):
    """C: Check if post links to the pillar page."""
    if pillar_url is None:
        return None, False  # No pillar URL defined
    
    # Check for the pillar URL in content
    in_text = pillar_url in content_text
    
    # Also check for relative paths
    pillar_slug = pillar_url.replace('/blog/', '')
    link_pattern = re.escape(pillar_url)
    found = bool(re.search(link_pattern, content_text))
    
    return pillar_url, found

def check_aeo_geo(content_text, min_questions=2):
    """D: Check AEO/GEO - count question-based headings."""
    q_headings = count_question_headings(content_text)
    count = len(q_headings)
    passed = count >= min_questions
    return count, passed, q_headings[:5]

def check_internal_links(content_text, min_links=3):
    """E: Check internal linking count."""
    links = count_internal_links(content_text)
    count = len(links)
    passed = count >= min_links
    return count, passed

def check_schema_readiness(post_text):
    """F: Check schema - post title, excerpt, date are set."""
    title = extract_field(post_text, 'title')
    excerpt = extract_field(post_text, 'excerpt')
    date = extract_field(post_text, 'date')
    
    missing = []
    if not title:
        missing.append('title')
    if not excerpt:
        missing.append('excerpt')
    if not date:
        missing.append('date')
    
    passed = len(missing) == 0
    return missing, passed

# Process each post
results = []
for slug, post_text in pairs:
    title = extract_field(post_text, 'title') or slug
    excerpt = extract_field(post_text, 'excerpt') or ''
    date = extract_field(post_text, 'date') or ''
    tags = extract_tags(post_text)
    
    # Get content from content field
    content_text = extract_field(post_text, 'content') or ''
    
    if not content_text:
        print(f"  ⚠️  {slug}: No content found, skipping framework checks")
        continue
    
    print(f"  Processing: {slug}")
    
    # A: TF-IDF
    keyword, tfidf_count, tfidf_pass = check_tfidf(content_text, title)
    
    # B: Entities
    entities_missing, entities_pass = check_entities(content_text)
    
    # C: Pillar-Cluster Alignment
    pillar, pillar_url = get_pillar_topic(tags, title)
    pillar_url_found, pillar_link_found = check_pillar_link(content_text, pillar_url)
    
    # D: AEO/GEO
    q_count, aeo_pass, sample_qs = check_aeo_geo(content_text)
    
    # E: Internal Links
    link_count, link_pass = check_internal_links(content_text)
    
    # F: Schema
    schema_missing, schema_pass = check_schema_readiness(post_text)
    
    results.append({
        'slug': slug,
        'title': title,
        'keyword': keyword,
        'tfidf_count': tfidf_count,
        'tfidf_pass': tfidf_pass,
        'entities_missing': entities_missing,
        'entities_pass': entities_pass,
        'pillar': pillar,
        'pillar_url': pillar_url,
        'pillar_link_found': pillar_link_found,
        'aeo_count': q_count,
        'aeo_pass': aeo_pass,
        'link_count': link_count,
        'link_pass': link_pass,
        'schema_missing': schema_missing,
        'schema_pass': schema_pass,
    })

# Generate summary report
print("\n" + "="*80)
print("CONTENT FRAMEWORK ENFORCEMENT REPORT")
print("="*80)
print(f"Date: Monday, July 20, 2026")
print(f"Posts analyzed: {len(results)}")
print()

# Count passes/fails
tfidf_fails = [r for r in results if not r['tfidf_pass']]
entities_fails = [r for r in results if not r['entities_pass']]
pillar_fails = [r for r in results if not r['pillar_link_found'] and r['pillar_url'] is not None]
aeo_fails = [r for r in results if not r['aeo_pass']]
link_fails = [r for r in results if not r['link_pass']]
schema_fails = [r for r in results if not r['schema_pass']]

print(f"SUMMARY")
print(f"  ✅ TF-IDF Coverage:    {len(results) - len(tfidf_fails)}/{len(results)} pass ({len(tfidf_fails)} fails)")
print(f"  ✅ Entity Coverage:    {len(results) - len(entities_fails)}/{len(results)} pass ({len(entities_fails)} fails)")
print(f"  ✅ Pillar Link:        {len(results) - len(pillar_fails)}/{len(results)} pass ({len(pillar_fails)} fails)")
print(f"  ✅ AEO/GEO:            {len(results) - len(aeo_fails)}/{len(results)} pass ({len(aeo_fails)} fails)")
print(f"  ✅ Internal Links:     {len(results) - len(link_fails)}/{len(results)} pass ({len(link_fails)} fails)")
print(f"  ✅ Schema Ready:       {len(results) - len(schema_fails)}/{len(results)} pass ({len(schema_fails)} fails)")

print()

# Detailed report for failed posts
if tfidf_fails:
    print(f"## TF-IDF Coverage Failures ({len(tfidf_fails)})")
    print(f"| Post | Keyword | Occurrences |")
    print(f"|------|---------|-------------|")
    for r in sorted(tfidf_fails, key=lambda x: x['tfidf_count'])[:20]:
        print(f"| {r['slug']} | {r['keyword']} | {r['tfidf_count']} |")
    print(f"... ({len(tfidf_fails)} total)")
    print()

if entities_fails:
    print(f"## Entity Coverage Failures ({len(entities_fails)})")
    for r in sorted(entities_fails, key=lambda x: len(x['entities_missing']), reverse=True)[:10]:
        print(f"- **{r['slug']}**: Missing: {', '.join(r['entities_missing'])}")
    if len(entities_fails) > 10:
        print(f"... and {len(entities_fails) - 10} more")
    print()

if pillar_fails:
    print(f"## Pillar Link Failures ({len(pillar_fails)})")
    for r in sorted(pillar_fails, key=lambda x: x['slug'])[:10]:
        print(f"- **{r['slug']}** (pillar: {r['pillar']} → {r['pillar_url']})")
    if len(pillar_fails) > 10:
        print(f"... and {len(pillar_fails) - 10} more")
    print()

if aeo_fails:
    print(f"## AEO/GEO Failures ({len(aeo_fails)})")
    for r in sorted(aeo_fails, key=lambda x: x['aeo_count'])[:10]:
        print(f"- **{r['slug']}**: {r['aeo_count']} question headings (< 2)")
    if len(aeo_fails) > 10:
        print(f"... and {len(aeo_fails) - 10} more")
    print()

if link_fails:
    print(f"## Internal Link Failures ({len(link_fails)})")
    for r in sorted(link_fails, key=lambda x: x['link_count'])[:10]:
        print(f"- **{r['slug']}**: {r['link_count']} internal links (< 3)")
    if len(link_fails) > 10:
        print(f"... and {len(link_fails) - 10} more")
    print()

if schema_fails:
    print(f"## Schema Readiness Failures ({len(schema_fails)})")
    for r in sorted(schema_fails, key=lambda x: x['slug'])[:10]:
        print(f"- **{r['slug']}**: Missing: {', '.join(r['schema_missing'])}")
    if len(schema_fails) > 10:
        print(f"... and {len(schema_fails) - 10} more")
    print()

# Sample detailed check for a few representative posts
print("\n## DETAILED SAMPLE CHECKS")
print()
sample_slugs = [
    'complete-seo-guide-bangladesh-businesses-2026',
    'local-seo-tips-dhaka-businesses-google-maps',
    'why-ecommerce-store-needs-seo-bangladesh',
    'technical-seo-checklist-bangladeshi-websites',
    'geo-optimization-prepare-business-ai-search',
    'seo-for-restaurants-cafe-dhaka',
    'seo-dashboard-tools-bangladesh',
]
for r in results:
    if r['slug'] in sample_slugs:
        print(f"### Post: {r['slug']}")
        print(f"| Check | Status | Details |")
        print(f"|-------|--------|---------|")
        print(f"| TF-IDF: {r['keyword']} | {'✅' if r['tfidf_pass'] else '❌'} | {r['tfidf_count']} occurrences |")
        print(f"| Entities | {'✅' if r['entities_pass'] else '❌'} | Missing: {', '.join(r['entities_missing']) if r['entities_missing'] else 'None'} |")
        print(f"| Pillar: {r['pillar']} | {'✅' if r['pillar_link_found'] else ('N/A' if r['pillar_url'] is None else '❌')} | Links to: {r['pillar_url'] if r['pillar_link_found'] else 'Not found'} |")
        print(f"| AEO/GEO | {'✅' if r['aeo_pass'] else '❌'} | {r['aeo_count']} question headings |")
        print(f"| Internal Links | {'✅' if r['link_pass'] else '❌'} | {r['link_count']} total |")
        print(f"| Schema Ready | {'✅' if r['schema_pass'] else '❌'} | Missing: {', '.join(r['schema_missing']) if r['schema_missing'] else 'All fields set'} |")
        print()

# Overall verdict
total_fails = len(tfidf_fails) + len(entities_fails) + len(pillar_fails) + len(aeo_fails) + len(link_fails) + len(schema_fails)
if total_fails == 0:
    print("## ✅ ALL FRAMEWORK CHECKS PASSED")
else:
    print(f"## ⚠️ {total_fails} TOTAL CHECK FAILURES ACROSS {len(results)} POSTS")
    print()
    print("### Priority Fix Recommendations")
    if len(aeo_fails) > 0:
        print(f"1. **High Priority - AEO/GEO ({len(aeo_fails)} posts)**: Add at least 2 question-format headings (How, What, Why, etc.) per post. This is critical for AI search visibility.")
    if len(link_fails) > 0:
        print(f"2. **High Priority - Internal Links ({len(link_fails)} posts)**: Ensure blog posts link to at least 3 internal pages (other posts, services, locations).")
    if len(pillar_fails) > 0:
        print(f"3. **Medium Priority - Pillar Links ({len(pillar_fails)} posts)**: Connect cluster posts back to their pillar topic page.")
    if len(tfidf_fails) > 0:
        print(f"4. **Medium Priority - TF-IDF ({len(tfidf_fails)} posts)**: Increase primary keyword density to at least 5 occurrences per post.")
    if len(entities_fails) > 0:
        print(f"5. **Low Priority - Entity Coverage ({len(entities_fails)} posts)**: Add missing entities to boost semantic relevance.")
    if len(schema_fails) > 0:
        print(f"6. **Low Priority - Schema Readiness ({len(schema_fails)} posts)**: Ensure all posts have title, excerpt, and date fields.")
