#!/usr/bin/env python3
"""Analyze blog posts for content framework compliance - simple approach."""
import re

with open('src/app/blog/data.js', 'r') as f:
    data = f.read()

# We know exactly where each post starts and ends from our read_file calls
# Let's extract each post's metadata and content using pattern matching

# First, let's just find all posts by their slug definition
slugs = [
    'how-to-choose-best-seo-expert-dhaka-15-things',
    'seo-expert-vs-seo-agency-dhaka-which-is-right',
    'top-10-seo-mistakes-dhaka-businesses-fix',
    'what-does-seo-expert-do-guide-business-owners',
    'seo-case-study-dhaka-businesses-increased-organic-traffic',
    'hiring-seo-expert-dhaka-better-roi-than-paid-ads',
    'ai-seo-2026-dhaka-experts-optimize-google-ai-chatgpt',
    'watchzonebd-seo-case-study',
]

def extract_post(data, slug):
    """Extract a single post object from data.js by its slug."""
    # Find the slug occurrence
    idx = data.index(f'slug: "{slug}"')
    # Find the opening { before it
    # Go backwards from idx to find {
    open_brace = data.rfind('{', 0, idx)
    
    # Find the closing } of this post object
    # After the content backtick, there's `,\n  },
    close = data.find('`,\n  },', open_brace)
    if close == -1:
        close = data.find('`,\n  }\n', open_brace)
    if close == -1:
        # For last post
        close = data.find('`,\n  }\n]', open_brace)
    
    if close == -1:
        return None
    
    # Include the closing brace
    close_brace = data.find('}', close + 3)
    if close_brace == -1:
        return None
    
    post_text = data[open_brace:close_brace + 1]
    return post_text

def get_field(post_text, field_name):
    """Extract a string field value from a post text."""
    # Match: field_name:\n    "value"  or field_name: "value"
    pattern = field_name + r':\s*\n?\s*"((?:[^"\\]|\\.)*)"'
    m = re.search(pattern, post_text)
    if m:
        return m.group(1)
    return None

def get_multiline_field(post_text, field_name):
    """Extract a multiline string field (like excerpt)."""
    pattern = field_name + r':\s*\n\s*"((?:[^"\\]|\\.)*)"'
    m = re.search(pattern, post_text)
    if m:
        return m.group(1)
    return None

def get_tags(post_text):
    """Extract tags array."""
    m = re.search(r'tags:\s*\[(.*?)\]', post_text, re.DOTALL)
    if m:
        tags_str = m.group(1)
        tags = re.findall(r'"([^"]+)"', tags_str)
        return tags
    return []

def get_content(post_text):
    """Extract content between backticks."""
    m = re.search(r'content:\s*`\n?(.*?)`', post_text, re.DOTALL)
    if m:
        return m.group(1)
    return ''

def count_keyword(content, keyword):
    """Count case-insensitive occurrences of a keyword in content."""
    return content.lower().count(keyword.lower())

def extract_primary_keyword(title):
    """Extract the primary keyword from a title."""
    # Remove common lead-in phrases
    kw = title
    for prefix in ['How to ', 'What Does ', 'What Is ', 'Why ', 'When ', 'Where ',
                   'Can ', 'Do ', 'Is ', 'Are ', 'Top ', 'The ']:
        if kw.startswith(prefix):
            kw = kw[len(prefix):]
            break
    
    # If contains colon, take everything before or after depending on context
    if ':' in kw:
        parts = kw.split(':')
        # If first part is very short, take second part
        if len(parts[0].split()) <= 3:
            kw = parts[1].strip()
        else:
            kw = parts[0].strip()
    
    # Remove trailing prepositions / location qualifiers for a cleaner keyword
    # But keep 'SEO Expert Dhaka' as a primary keyword
    return kw.strip()

def count_question_headings(content):
    """Count question-based headings in content."""
    pattern = r'^#{2,3}\s+(How\s|What\s|Why\s|When\s|Where\s|Can\s|Do\s|Is\s|Are\s)'
    matches = re.findall(pattern, content, re.MULTILINE)
    return matches

def count_internal_links(content):
    """Count internal markdown links (starting with /)."""
    links = re.findall(r'\[([^\]]+)\]\((/[^\)]+)\)', content)
    return links

def get_pillar_suggestion(tags):
    """Based on tags, suggest a pillar topic."""
    mapping = {
        'SEO Expert Dhaka': '/blog/complete-seo-guide-bangladesh-businesses-2026',
        'SEO Agency Dhaka': '/blog/complete-seo-guide-bangladesh-businesses-2026',
        'SEO Services Bangladesh': '/blog/complete-seo-guide-bangladesh-businesses-2026',
        'Hire SEO Expert': '/blog/complete-seo-guide-bangladesh-businesses-2026',
        'Hire SEO': '/blog/complete-seo-guide-bangladesh-businesses-2026',
        'SEO Mistakes': '/blog/complete-seo-guide-bangladesh-businesses-2026',
        'Dhaka SEO': '/blog/complete-seo-guide-bangladesh-businesses-2026',
        'SEO Tips Bangladesh': '/blog/complete-seo-guide-bangladesh-businesses-2026',
        'SEO Expert Guide': '/blog/complete-seo-guide-bangladesh-businesses-2026',
        'SEO Services': '/blog/complete-seo-guide-bangladesh-businesses-2026',
        'Digital Marketing Bangladesh': '/blog/complete-seo-guide-bangladesh-businesses-2026',
        'SEO Case Study': '/blog/complete-seo-guide-bangladesh-businesses-2026',
        'Organic Traffic': '/blog/complete-seo-guide-bangladesh-businesses-2026',
        'SEO Results Bangladesh': '/blog/complete-seo-guide-bangladesh-businesses-2026',
        'SEO ROI': '/blog/complete-seo-guide-bangladesh-businesses-2026',
        'SEO vs Ads': '/blog/complete-seo-guide-bangladesh-businesses-2026',
        'Dhaka SEO Expert': '/blog/complete-seo-guide-bangladesh-businesses-2026',
        'AI SEO': '/services/geo-ai-search',
        'GEO Optimization': '/services/geo-ai-search',
        'Google AI Overview Bangladesh': '/services/geo-ai-search',
        'Case Study': '/blog/complete-seo-guide-bangladesh-businesses-2026',
        'E-commerce SEO': '/blog/complete-seo-guide-bangladesh-businesses-2026',
        'Technical SEO': '/blog/complete-seo-guide-bangladesh-businesses-2026',
        'WatchZoneBD': '/blog/complete-seo-guide-bangladesh-businesses-2026',
        'Best SEO Expert': '/blog/complete-seo-guide-bangladesh-businesses-2026',
    }
    suggested = set()
    for tag in tags:
        if tag in mapping:
            suggested.add(mapping[tag])
    if not suggested:
        suggested.add('/blog/complete-seo-guide-bangladesh-businesses-2026')
    return suggested

def check_pillar_link(content, pillar_urls):
    """Check if content links to any pillar page."""
    for url in pillar_urls:
        if url in content:
            return True, url
    return False, None

print("=" * 100)
print("CONTENT FRAMEWORK ENFORCEMENT REPORT — 8 NEW BLOG POSTS")
print("=" * 100)

for slug in slugs:
    post_text = extract_post(data, slug)
    if post_text is None:
        print(f"\n{'='*80}")
        print(f"POST: {slug}")
        print("ERROR: Could not extract post")
        continue
    
    title = get_field(post_text, 'title')
    date_val = get_field(post_text, 'date')
    excerpt = get_multiline_field(post_text, 'excerpt')
    tags = get_tags(post_text)
    content = get_content(post_text)
    
    if not content:
        print(f"\n{'='*80}")
        print(f"POST: {slug} — {title}")
        print("ERROR: Could not extract content")
        continue
    
    print(f"\n{'='*80}")
    print(f"POST: {slug}")
    print(f"{'='*80}")
    print(f"**Title:** {title}")
    print(f"**Date:** {date_val}")
    print(f"**Tags:** {', '.join(tags)}")
    
    # ===== A) TF-IDF Coverage =====
    print(f"\n### A) TF-IDF Coverage")
    primary_kw = extract_primary_keyword(title)
    
    # Try the keyword itself
    kw_counts = {}
    for try_kw in [primary_kw, primary_kw.replace(' in Dhaka', ''), title]:
        cnt = count_keyword(content, try_kw)
        kw_counts[try_kw] = cnt
    
    best_kw = max(kw_counts, key=kw_counts.get)
    best_count = kw_counts[best_kw]
    
    print(f"Title-derived primary keyword: '{primary_kw}'")
    print(f"Best matching keyword in content: '{best_kw}' — {best_count} occurrences")
    print(f"**Status:** {'✅ PASS' if best_count >= 5 else '❌ FAIL'} (need ≥ 5)")
    
    # ===== B) Semantic Entity Coverage =====
    print(f"\n### B) Semantic Entity Coverage")
    has_dhaka = bool(re.search(r'Dhaka', content, re.IGNORECASE))
    has_bangladesh = bool(re.search(r'Bangladesh', content, re.IGNORECASE))
    
    # Check for service type
    has_seo = bool(re.search(r'SEO|search engine optimization', content, re.IGNORECASE))
    
    # Check for industry entities
    industry_patterns = [
        'e-commerce', 'ecommerce', 'restaurant', 'real estate', 'healthcare',
        'medical', 'education', 'fashion', 'garments', 'textile', 'B2B',
        'salon', 'cleaning', 'software', 'apparel', 'home service'
    ]
    found_industries = [ind for ind in industry_patterns if re.search(ind, content, re.IGNORECASE)]
    
    print(f"Dhaka/Bangladesh: {'✅' if has_dhaka else '❌'} Dhaka, {'✅' if has_bangladesh else '❌'} Bangladesh")
    print(f"Service type: {'✅ SEO' if has_seo else '❌ No SEO reference'}")
    print(f"Industry entities found: {', '.join(found_industries[:6]) if found_industries else 'None'}")
    
    # ===== C) Pillar-Cluster Alignment =====
    print(f"\n### C) Pillar-Cluster Alignment")
    suggested = get_pillar_suggestion(tags)
    pillar_urls_to_check = list(suggested) + [
        '/blog/complete-seo-guide-bangladesh-businesses-2026',
        '/services/geo-ai-search',
        'complete-seo-guide',
    ]
    found_pillar, pillar_link = check_pillar_link(content, pillar_urls_to_check)
    print(f"Tags: {', '.join(tags)}")
    print(f"Suggested pillar: {', '.join(suggested)}")
    print(f"Pillar link in content: {'✅ FOUND: ' + pillar_link if found_pillar else '❌ NOT FOUND'}")
    
    # ===== D) AEO/GEO Optimization =====
    print(f"\n### D) AEO/GEO Optimization")
    q_headings = count_question_headings(content)
    print(f"Question-based headings found: {len(q_headings)}")
    if q_headings:
        for h in q_headings:
            print(f"  - {h}...")
    print(f"**Status:** {'✅ PASS' if len(q_headings) >= 2 else '❌ FAIL'} (need ≥ 2)")
    
    # ===== E) Internal Linking =====
    print(f"\n### E) Internal Linking")
    internal_links = count_internal_links(content)
    # Also count kanokmiah.com.bd links as internal
    site_links = re.findall(r'\[([^\]]+)\]\((https?://kanokmiah\.com\.bd[^\)]+)\)', content)
    all_internal = internal_links + site_links
    print(f"Internal links (starting with /): {len(internal_links)}")
    for lt, lu in internal_links[:8]:
        print(f"  - [{lt}]({lu})")
    if site_links:
        print(f"Site-level links (kanokmiah.com.bd): {len(site_links)}")
        for lt, lu in site_links[:5]:
            print(f"  - [{lt}]({lu})")
    total_internal = len(internal_links)
    print(f"**Status:** {'✅ PASS' if total_internal >= 3 else '❌ FAIL'} (need ≥ 3 internal /-links, found {total_internal})")
    
    # ===== F) Schema Readiness =====
    print(f"\n### F) Schema Readiness")
    has_title_field = bool(title)
    has_excerpt_field = bool(excerpt)
    has_date_field = bool(date_val)
    
    print(f"title field: {'✅ SET' if has_title_field else '❌ MISSING'}")
    print(f"excerpt field: {'✅ SET' if has_excerpt_field else '❌ MISSING'}")
    print(f"date field: {'✅ SET' if has_date_field else '❌ MISSING'}")
    all_set = has_title_field and has_excerpt_field and has_date_field
    print(f"**Status:** {'✅ PASS' if all_set else '❌ FAIL'}")

print("\n" + "=" * 100)
print("END OF REPORT")
print("=" * 100)
