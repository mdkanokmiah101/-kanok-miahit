#!/usr/bin/env python3
"""
Content Framework Enforcer for kanokmiah.com.bd
Checks blog posts against the content quality framework.
"""
import re
import json
import subprocess
import sys

# 1. Identify modified posts from git
result = subprocess.run(
    ['git', 'diff', 'HEAD~3..HEAD', '--', 'src/app/blog/data.js'],
    capture_output=True, text=True, cwd='/root/kanok-miahit'
)
diff_output = result.stdout

# Parse diff to get the line ranges and slugs
# We need to read data.js and find which posts correspond to changed lines
with open('/root/kanok-miahit/src/app/blog/data.js', 'r') as f:
    content = f.read()

# Extract all posts with their slug, title, tags, excerpt, date, content
posts_pattern = re.compile(
    r'{\s*slug:\s*"([^"]+)"\s*,\s*title:\s*"([^"]*?)"\s*,\s*date:\s*"([^"]*?)"\s*,\s*author:\s*"([^"]*?)"\s*,\s*excerpt:\s*"([^"]*?)"\s*,\s*tags:\s*\[(.*?)\]\s*,\s*imagePlaceholder:\s*"[^"]*?"\s*(?:,\s*metaTitle:\s*"[^"]*?"\s*)?(?:,\s*metaDescription:\s*"[^"]*?"\s*)?(?:,\s*dateModified:\s*"[^"]*?"\s*)?,\s*content:\s*`(.*?)`\s*}',
    re.DOTALL
)

all_posts = []
for m in posts_pattern.finditer(content):
    slug = m.group(1)
    title = m.group(2)
    date = m.group(3)
    excerpt = m.group(5)
    tags_raw = m.group(6)
    post_content = m.group(7)
    
    # Clean tags
    tags = [t.strip().strip('"') for t in tags_raw.split(',')]
    
    all_posts.append({
        'slug': slug,
        'title': title,
        'date': date,
        'excerpt': excerpt,
        'tags': tags,
        'content': post_content,
        'has_excerpt': bool(excerpt.strip()),
        'has_date': bool(date.strip()),
    })

print(f"Total posts found: {len(all_posts)}", file=sys.stderr)

# Check which line ranges were modified
# Parse diff hunks to get line numbers
line_pattern = re.compile(r'@@ -(\d+),(\d+) \+(\d+),(\d+) @@')
diff_lines = []
current_offset = 0
for line in diff_output.split('\n'):
    m = line_pattern.match(line)
    if m:
        old_start, old_count, new_start, new_count = int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))
        diff_lines.append((new_start, new_count))

# Now find which posts overlap with these changed line ranges
# We need to know the line number of each post's starting content
# Let's find slug positions
slug_positions = []
for m in re.finditer(r'slug:\s*"([^"]+)"', content):
    line_num = content[:m.start()].count('\n') + 1
    slug_positions.append((line_num, m.group(1)))

# For each post, determine its line range
modified_slugs = set()
# From diff context extraction (simpler approach - use the explicit list from diff)
# Let's just extract slugs from diff context
for slug_match in re.finditer(r'slug:\s*"([^"]+)"', diff_output):
    modified_slugs.add(slug_match.group(1))

# Also get from the "Looking for the" additions
for slug_match in re.finditer(r'(?:Looking for the|slug:)\s*"([^"]+)"', diff_output):
    modified_slugs.add(slug_match.group(1))

# Additional: check what's between diff hunks
# Get all hunks and their surrounding context
hunks = re.findall(r'@@ -\d+,\d+ +\d+,\d+ @@.*?(?=@@|$)', diff_output, re.DOTALL)

for hunk in hunks:
    # Extract slug references in context
    for slug_match in re.finditer(r'/blog/([a-z0-9-]+)', hunk):
        modified_slugs.add(slug_match.group(1))
    for slug_match in re.finditer(r'slug:\s*"([^"]+)"', hunk):
        modified_slugs.add(slug_match.group(1))

print(f"Modified slugs found: {len(modified_slugs)}", file=sys.stderr)
for s in sorted(modified_slugs):
    print(f"  {s}", file=sys.stderr)

# Also add slugs from the commit messages / explicit list
commit1_slugs = [
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
]
for s in commit1_slugs:
    modified_slugs.add(s)

# Build lookup
posts_by_slug = {p['slug']: p for p in all_posts}

# 2. Run framework checks on each modified post
def count_occurrences(text, keyword):
    """Count case-insensitive occurrences of keyword in text"""
    if not keyword:
        return 0
    return len(re.findall(re.escape(keyword), text, re.IGNORECASE))

def extract_primary_keyword(title):
    """Extract primary keyword from title (first meaningful noun phrase)"""
    # Remove SEO-specific suffixes
    t = title.lower()
    # For English titles, try to extract the main topic
    stop_prefixes = ['complete ', 'why your ', 'how to ', 'what is ', 'top ', 'best ', 'ultimate ']
    for prefix in stop_prefixes:
        if t.startswith(prefix):
            t = t[len(prefix):]
    
    # Remove trailing suffixes like "in bangladesh", "for x"
    t = re.sub(r'\s*(in|for|of|—).*$', '', t)
    
    # Take first 2-3 meaningful words
    words = t.split()[:3]
    return ' '.join(words) if words else title.split()[:3]

def check_entities(content):
    """Check semantic entity coverage"""
    entities = ['Dhaka', 'Bangladesh']
    
    # Check for location entities
    location_found = {
        'Dhaka': bool(re.search(r'\b[Dd]haka\b', content)),
        'Bangladesh': bool(re.search(r'\b[Bb]angladesh\b', content)),
    }
    
    # Check for service type entity
    service_terms = ['SEO', 'SE0', 'search engine optimization', 'digital marketing', 
                     'local SEO', 'technical SEO', 'link building', 'content marketing',
                     'on-page', 'off-page']
    service_found = any(term in content for term in service_terms)
    
    # Check for industry-specific entities
    industry_terms = ['e-commerce', 'ecommerce', 'real estate', 'healthcare', 'medical',
                      'garment', 'textile', 'education', 'restaurant', 'hotel', 'travel',
                      'B2B', 'startup', 'legal', 'fitness', 'photography', 'event',
                      'non-profit', 'NGO', 'export', 'cleaning', 'salon']
    industry_found = any(term in content for term in industry_terms)
    
    return {
        'Dhaka': location_found['Dhaka'],
        'Bangladesh': location_found['Bangladesh'],
        'service_type': service_found,
        'industry_specific': industry_found
    }

def find_pillar_link(content, tags, slug):
    """Check if post links to a pillar page based on tags"""
    pillar_pages = {
        'SEO Guide': '/blog/complete-seo-guide-bangladesh-businesses-2026',
        'Local SEO': '/blog/local-seo-tips-dhaka-businesses-google-maps',
        'Technical SEO': '/blog/technical-seo-checklist-bangladeshi-websites',
        'E-commerce SEO': '/blog/why-ecommerce-store-needs-seo-bangladesh',
        'Link Building': '/blog/link-building-strategies-bangladesh-market',
        'GEO': '/blog/geo-optimization-prepare-business-ai-search',
        'Bangladesh SEO': '/blog/complete-seo-guide-bangladesh-businesses-2026',
        'Digital Marketing': '/blog/complete-seo-guide-bangladesh-businesses-2026',
        '2026': '/blog/seo-trends-2026-ai-geo-future',
        'Mobile SEO': '/blog/mobile-seo-optimization-bangladesh-mobile-first-era',
        'Content Marketing': '/blog/content-marketing-strategy-bangladeshi-brands-seo',
        'International SEO': '/blog/international-seo-bangladesh-exporters-global-buyers',
        'Case Study': '/blog/seo-case-study-dhaka-businesses-increased-organic-traffic',
        'Google Business': '/blog/google-business-profile-optimization-guide-bangladesh',
        'Google Ads': '/blog/seo-vs-google-ads-whats-best-bangladesh-businesses',
        'Real Estate': '/blog/seo-real-estate-developers-dhaka',
        'Garments SEO': '/blog/seo-garments-textile-industry-b2b-lead-generation',
    }
    
    # Determine pillar from tags
    linked_pillars = []
    for tag in tags:
        if tag in pillar_pages:
            pillar_url = pillar_pages[tag]
            # Check if this pillar URL is referenced in content (excluding self-reference)
            if pillar_url.replace('/blog/', '') != slug and pillar_url in content:
                linked_pillars.append(pillar_url)
    
    return linked_pillars

def count_question_headings(content):
    """Count question-based headings"""
    q_headings = re.findall(r'^#{1,6}\s+(How|What|Why|When|Where|Can|Do|Is|Are|Does|Which|Who|Should)\b', content, re.MULTILINE)
    return len(q_headings)

def count_internal_links(content, slug):
    """Count internal links to other posts, services, locations"""
    # Links to /blog/, /services/, /locations/, /industries/, /about, /contact
    internal_links = re.findall(r'\(/(?:blog/[^)"\']+|services/[^)"\']+|locations/[^)"\']+|industries/[^)"\']+|about|contact|/?)\)', content)
    # Count unique links
    unique_links = set(internal_links)
    return len(unique_links)

def check_schema_readiness(post):
    """Check if post has title, excerpt, date for ArticleSchema"""
    issues = []
    if not post['title'].strip():
        issues.append('title')
    if not post.get('excerpt', '').strip():
        issues.append('excerpt')
    if not post.get('date', '').strip():
        issues.append('date')
    return issues

# Report header
print("# Content Framework Audit Report")
print(f"**Generated:** (automated cron check)")
print(f"**Trigger:** Content changes detected in last 48 hours")
print(f"**Commits:** 3 commits across {len(modified_slugs)} posts modified")
print()

# Check if we have posts to examine
target_posts = []
for slug in sorted(modified_slugs):
    if slug in posts_by_slug:
        target_posts.append(posts_by_slug[slug])
    else:
        print(f"⚠ WARNING: slug '{slug}' not found in data.js")

if not target_posts:
    print("✅ No modified posts found to analyze.")
    sys.exit(0)

# Run checks
all_pass = True
for post in target_posts:
    slug = post['slug']
    title = post['title']
    content = post['content']
    tags = post['tags']
    excerpt = post['excerpt']
    
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
    
    # B. Semantic Entity Coverage
    entities = check_entities(content)
    missing_entities = []
    if not entities['Dhaka']:
        missing_entities.append('Dhaka')
    if not entities['Bangladesh']:
        missing_entities.append('Bangladesh')
    if not entities['service_type']:
        missing_entities.append('service_type')
    
    entity_status = "✅" if len(missing_entities) == 0 else "❌"
    if entity_status == "❌":
        all_pass = False
    entity_detail = "All present" if len(missing_entities) == 0 else f"Missing: {', '.join(missing_entities)}"
    print(f"| Entities | {entity_status} | {entity_detail} |")
    
    # C. Pillar-Cluster Alignment
    pillar_links = find_pillar_link(content, tags, slug)
    pillar_status = "✅" if len(pillar_links) > 0 else "❌"
    if pillar_status == "❌":
        all_pass = False
    pillar_detail = f"Links to: {', '.join(pillar_links)}" if pillar_links else "No pillar link found"
    print(f"| Pillar Link | {pillar_status} | {pillar_detail} |")
    
    # D. AEO/GEO Optimization
    q_count = count_question_headings(content)
    q_status = "✅" if q_count >= 2 else "❌"
    if q_status == "❌":
        all_pass = False
    print(f"| AEO/GEO | {q_status} | {q_count} question headings |")
    
    # E. Internal Linking
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
    schema_detail = "All fields set" if len(schema_issues) == 0 else f"Missing: {', '.join(schema_issues)}"
    print(f"| Schema Ready | {schema_status} | {schema_detail} |")
    
    print()

# Summary
print("---")
if all_pass:
    print("## ✅ Summary: All checks pass for modified posts.")
else:
    print("## ⚠ Summary: Some posts need fixes (see flags above).")
print()
