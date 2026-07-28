#!/usr/bin/env python3
"""
Cron framework enforcement checker for kanokmiah.com.bd blog posts.
"""
import re, os, sys
from collections import Counter

DATA_PATH = 'src/app/blog/data.js'

# Read the file
with open(DATA_PATH, 'r') as f:
    text = f.read()

# Extract all posts by finding slug markers and their surrounding blocks
# A post starts with '{' followed by slug: "..." and ends with '},'
# We'll use a pragmatic approach: split by slug: and parse each chunk

# First, get line numbers for each slug
lines = text.split('\n')

slug_positions = {}
for i, line in enumerate(lines):
    m = re.search(r'slug:\s*"([^"]+)"', line)
    if m:
        slug_positions[m.group(1)] = i

changed_slugs = [
    'geo-optimization-prepare-business-ai-search',
    'seo-garments-textile-industry-b2b-lead-generation',
    'seo-healthcare-medical-clinics-bangladesh',
    'why-md-kanok-miah-is-the-best-seo-expert-in-dhaka-bangladesh',
    'locksmith-dundee-seo-case-study',
    'das-taxis-scotland-seo-case-study',
    'morethanpanel-seo-case-study',
    'smmgen-seo-case-study',
    'smmsun-seo-case-study',
    'mir-cement-seo-case-study',
    'dhaka-apparels-seo-case-study',
    'stealth-windshield-repairs-seo-case-study',
    'how-to-choose-right-seo-agency-bangladesh',
    'seo-expert-vs-seo-agency-dhaka-which-is-right',
    'top-10-seo-mistakes-dhaka-businesses-fix',
    'seo-tips-for-business-owners-bd',
    'seo-case-study-dhaka-businesses-increased-organic-traffic',
    'hiring-seo-expert-dhaka-better-roi-than-paid-ads',
    'seo-trends-2026-ai-geo-future'
]

def extract_post_fields(lines, slug_line, all_slug_positions):
    """Extract title, date, excerpt, tags, content from a post given its starting line."""
    slug_line_idx = all_slug_positions[slug_line]
    
    # Find the start of this post object (look for '{' before slug, going up)
    start = slug_line_idx
    while start > 0 and not lines[start].strip().startswith('{'):
        start -= 1
    # The post starts at 'start' line which has '{'
    
    # Find where this post ends - find the next slug or the end of array
    # Look for the next slug that is AFTER this one
    next_slug_line = None
    all_slug_names = sorted(all_slug_positions.keys(), 
                           key=lambda s: all_slug_positions[s])
    found_current = False
    for s in all_slug_names:
        if all_slug_positions[s] == slug_line_idx:
            found_current = True
            continue
        if found_current and all_slug_positions[s] > slug_line_idx:
            next_slug_line = all_slug_positions[s]
            break
    
    if next_slug_line:
        end = next_slug_line
    else:
        # Last post - find '];'
        end = len(lines)
    
    post_lines = lines[start:end]
    post_text = '\n'.join(post_lines)
    
    # Extract fields
    title_m = re.search(r'title:\s*"([^"]*)"', post_text)
    date_m = re.search(r'date:\s*"([^"]*)"', post_text)
    date_mod_m = re.search(r'dateModified:\s*"([^"]*)"', post_text)
    excerpt_m = re.search(r'excerpt:\s*\n?\s*"([^"]*)"', post_text, re.DOTALL)
    tags_m = re.search(r'tags:\s*\[([^\]]*)\]', post_text, re.DOTALL)
    content_m = re.search(r'content:\s*`\n?([^`]*)`', post_text, re.DOTALL)
    
    title = title_m.group(1) if title_m else ''
    date = date_m.group(1) if date_m else ''
    date_mod = date_mod_m.group(1) if date_mod_m else ''
    excerpt = excerpt_m.group(1).replace('\n', ' ').strip() if excerpt_m else ''
    tags = []
    if tags_m:
        raw_tags = tags_m.group(1)
        tags = re.findall(r'"([^"]*)"', raw_tags)
    
    content = content_m.group(1) if content_m else ''
    
    return {
        'title': title,
        'date': date,
        'dateModified': date_mod,
        'excerpt': excerpt,
        'tags': tags,
        'content': content,
        'slug': slug_line
    }

def check_tfidf(post):
    """A. TF-IDF Coverage - extract primary keyword from title, count occurrences."""
    title = post['title']
    content = post['content']
    
    # Extract first meaningful noun phrase from title
    # Simple heuristic: first 2-4 words that aren't stop words
    stop_words = {'the', 'a', 'an', 'in', 'of', 'for', 'to', 'and', 'or', 'is', 'are', 'was', 'were',
                   'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
                   'can', 'could', 'shall', 'should', 'may', 'might', 'must', 'about', 'into', 'through',
                   'during', 'before', 'after', 'above', 'below', 'between', 'out', 'off', 'over', 'under',
                   'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how',
                   'all', 'each', 'every', 'both', 'few', 'more', 'most', 'other', 'some', 'such',
                   'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 'just',
                   'because', 'as', 'until', 'while', 'with', 'without', 'from', 'up', 'down', 'at',
                   'by', 'on', 'off', 'this', 'that', 'these', 'those', 'it', 'its', 'your', 'our', 'their'
                   'what', 'which', 'who', 'whom'}
    
    # Extract primary keyword - take first 2-3 meaningful words from title
    words = re.findall(r'[A-Za-z]+', title)
    meaningful = [w.lower() for w in words if w.lower() not in stop_words and len(w) > 2]
    
    # For case studies, use the main category keyword
    if 'case study' in title.lower() or 'case' in title.lower():
        keyword = meaningful[0] if meaningful else title.split()[0].lower()
    else:
        # Get 2-3 word phrase from meaningful words
        if len(meaningful) >= 3:
            keyword = ' '.join(meaningful[:3])
        elif len(meaningful) >= 2:
            keyword = ' '.join(meaningful[:2])
        elif meaningful:
            keyword = meaningful[0]
        else:
            keyword = words[0].lower() if words else ''
    
    # Count occurrences in content (case-insensitive)
    count = len(re.findall(re.escape(keyword), content, re.IGNORECASE))
    
    # For very long keywords, also check if individual parts appear
    if count < 5 and ' ' in keyword:
        parts = keyword.split()
        min_part_count = min(len(re.findall(re.escape(p), content, re.IGNORECASE)) for p in parts)
        if min_part_count >= 5:
            # Use the first part as a simpler keyword
            keyword = parts[0]
            count = len(re.findall(re.escape(keyword), content, re.IGNORECASE))
    
    status = '✅' if count >= 5 else '❌'
    return {
        'check': f'TF-IDF: "{keyword}"',
        'status': status,
        'details': f'{count} occurrences'
    }

def check_entities(post):
    """B. Semantic Entity Coverage."""
    content = post['content']
    title = post['title']
    slug = post['slug']
    
    # Determine expected entities based on slug/title
    entities_to_check = []
    
    # Location entities
    locations = ['Dhaka', 'Bangladesh', 'Chittagong', 'Sylhet']
    found_locations = [loc for loc in locations if re.search(re.escape(loc), content, re.IGNORECASE)]
    
    # Service type entities
    if 'geo' in slug.lower() or 'ai' in slug.lower() or 'generative' in title.lower():
        entities_to_check.extend(['Generative Engine', 'AI search', 'ChatGPT', 'SGE', 'Perplexity'])
    elif 'garment' in slug.lower() or 'textile' in slug.lower():
        entities_to_check.extend(['garment', 'textile', 'B2B', 'manufacturer', 'factory'])
    elif 'healthcare' in slug.lower() or 'medical' in slug.lower() or 'clinic' in slug.lower():
        entities_to_check.extend(['healthcare', 'hospital', 'clinic', 'patient'])
    elif 'case-study' in slug.lower() or 'case study' in title.lower():
        entities_to_check.extend(['case study', 'traffic', 'results', 'SEO'])
    elif 'seo expert' in slug.lower() or 'seo consultant' in slug.lower():
        entities_to_check.extend(['SEO', 'expert', 'Dhaka', 'Bangladesh'])
    elif 'agency' in slug.lower():
        entities_to_check.extend(['SEO agency', 'choose', 'right'])
    elif 'mistakes' in slug.lower():
        entities_to_check.extend(['mistakes', 'errors', 'fix'])
    elif 'hiring' in slug.lower() or 'roi' in slug.lower():
        entities_to_check.extend(['hire', 'SEO expert', 'ROI', 'paid ads'])
    elif 'tips' in slug.lower():
        entities_to_check.extend(['tips', 'SEO', 'business owners'])
    elif 'trends' in slug.lower():
        entities_to_check.extend(['trends', '2026', 'AI', 'GEO'])
    
    if 'bangladesh' in slug.lower() or 'dhaka' in slug.lower():
        entities_to_check.append('Bangladesh')
        entities_to_check.append('Dhaka')
    
    missing = []
    for entity in entities_to_check:
        if not re.search(re.escape(entity), content, re.IGNORECASE):
            missing.append(entity)
    
    # Check location coverage
    if not found_locations:
        missing.append('Any location (Dhaka/Bangladesh)')
    
    status = '✅' if not missing else '❌'
    return {
        'check': 'Entities',
        'status': status,
        'details': f'Missing: {", ".join(missing)}' if missing else 'All key entities present'
    }

def check_pillar_link(post):
    """C. Pillar-Cluster Alignment."""
    tags = post['tags']
    content = post['content']
    slug = post['slug']
    
    # Determine pillar topic from tags
    pillar_pages = {
        'SEO Guide': ['/blog/complete-seo-guide-bangladesh-businesses-2026'],
        'Bangladesh SEO': ['/blog/complete-seo-guide-bangladesh-businesses-2026'],
        'Local SEO': ['/services/local-seo', '/blog/local-seo-tips-dhaka-businesses-google-maps'],
        'Technical SEO': ['/services/technical-seo'],
        'GEO': ['/services/geo-ai-search', '/blog/geo-optimization-prepare-business-ai-search'],
        'E-commerce': ['/services/ecommerce-seo'],
        'Case Study': None,
    }
    
    # Default pillar based on slug
    pillar_links_found = []
    
    # Check for links to main pillar pages
    pillar_urls = [
        '/blog/complete-seo-guide-bangladesh-businesses-2026',
        '/services/local-seo',
        '/services/technical-seo',
        '/services/ecommerce-seo',
        '/services/on-page-seo',
        '/services/geo-ai-search',
        '/services/semantic-seo',
        '/services/link-building',
        '/services/',
        '/industries/',
        '/locations/',
        '/about',
    ]
    
    for url in pillar_urls:
        count = content.count(url)
        if count > 0:
            pillar_links_found.append(f'{url} (x{count})')
    
    status = '✅' if pillar_links_found else '❌'
    details = 'Links to: ' + ', '.join(pillar_links_found) if pillar_links_found else 'No pillar links found'
    return {
        'check': 'Pillar Link',
        'status': status,
        'details': details
    }

def check_aeo_geo(post):
    """D. AEO/GEO Optimization - count question-based headings."""
    content = post['content']
    
    # Find all markdown headings (## or ### etc)
    heading_pattern = re.findall(r'^#{2,6}\s+.*$', content, re.MULTILINE)
    
    # Count question-based headings
    question_words = ['How', 'What', 'Why', 'When', 'Where', 'Can', 'Do', 'Is', 'Are', 'Does', 'Did', 'Will', 'Would', 'Could', 'Should', 'Which', 'Who']
    
    question_headings = []
    for h in heading_pattern:
        heading_text = h.lstrip('#').strip()
        first_word = heading_text.split()[0] if heading_text.split() else ''
        if first_word in question_words:
            question_headings.append(heading_text)
    
    count = len(question_headings)
    status = '✅' if count >= 2 else '❌'
    return {
        'check': 'AEO/GEO',
        'status': status,
        'details': f'{count} question headings' + (f' ({", ".join(question_headings[:5])})' if question_headings else '')
    }

def check_internal_links(post):
    """E. Internal Linking."""
    content = post['content']
    
    # Find internal links (relative URLs)
    internal_links = re.findall(r'href="(/[^"]*)"', content)
    
    # Filter to meaningful internal links (not just /)
    meaningful = [l for l in internal_links if l != '/' and l != '']
    
    # Also find markdown links
    md_links = re.findall(r'\[([^\]]*)\]\((/[^\)]*)\)', content)
    md_paths = [path for _, path in md_links if path != '/' and path != '']
    
    all_links = list(set(meaningful + md_paths))
    
    count = len(all_links)
    status = '✅' if count >= 3 else '❌'
    return {
        'check': 'Internal Links',
        'status': status,
        'details': f'{count} internal links' + (f' (e.g., {", ".join(all_links[:5])})' if all_links else '')
    }

def check_schema(post):
    """F. Schema - check title, excerpt, date are set."""
    issues = []
    if not post.get('title'):
        issues.append('Missing title')
    if not post.get('excerpt') or len(post['excerpt']) < 10:
        issues.append('Missing/short excerpt')
    if not post.get('date'):
        issues.append('Missing date')
    if not post.get('dateModified'):
        issues.append('Missing dateModified')
    
    status = '✅' if not issues else '❌'
    return {
        'check': 'Schema Ready',
        'status': status,
        'details': 'All fields set' if not issues else ', '.join(issues)
    }

def get_change_type(slug):
    """Determine what changed in this post."""
    # These had substantive content additions
    substantive = [
        'geo-optimization-prepare-business-ai-search',
        'seo-garments-textile-industry-b2b-lead-generation',
        'seo-healthcare-medical-clinics-bangladesh',
    ]
    if slug in substantive:
        return 'Content modifications'
    return 'Link cleanup (removed duplicate homepage links)'

# Run checks for all changed posts
print("=" * 80)
print("KANOKMIAH.COM.BD — CONTENT FRAMEWORK ENFORCEMENT REPORT")
print("=" * 80)
print()

print(f"Checking {len(changed_slugs)} modified posts from commit c822841")
print()

print("Legend:")
print("  ✅ = Pass,  ❌ = Fail (needs attention)")
print()

# For each changed slug, extract and check
for slug in changed_slugs:
    if slug not in slug_positions:
        print(f"\n## Post: {slug}")
        print("| ERROR | Could not find this slug in data.js |")
        continue
    
    post = extract_post_fields(lines, slug, slug_positions)
    change_type = get_change_type(slug)
    
    print(f"## Post: {slug}")
    print(f"**Title:** {post['title']}")
    print(f"**Change type:** {change_type}")
    print()
    print("| Check | Status | Details |")
    print("|-------|--------|---------|")
    
    result_a = check_tfidf(post)
    print(f"| {result_a['check']} | {result_a['status']} | {result_a['details']} |")
    
    result_b = check_entities(post)
    print(f"| {result_b['check']} | {result_b['status']} | {result_b['details']} |")
    
    result_c = check_pillar_link(post)
    print(f"| {result_c['check']} | {result_c['status']} | {result_c['details']} |")
    
    result_d = check_aeo_geo(post)
    print(f"| {result_d['check']} | {result_d['status']} | {result_d['details']} |")
    
    result_e = check_internal_links(post)
    print(f"| {result_e['check']} | {result_e['status']} | {result_e['details']} |")
    
    result_f = check_schema(post)
    print(f"| {result_f['check']} | {result_f['status']} | {result_f['details']} |")
    
    print()
    print("---")
    print()

print()
print("=" * 80)
print("END OF REPORT")
print("=" * 80)
