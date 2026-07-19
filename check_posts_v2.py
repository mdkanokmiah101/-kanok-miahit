#!/usr/bin/env python3
"""Refined analysis of 4 blog posts for content framework checks."""

import re

with open('src/app/blog/data.js', 'r', encoding='utf-8') as f:
    content = f.read()

slugs = [
    'seo-for-law-firms-bangladesh',
    'b2b-lead-generation-seo-bangladesh',
    'seo-for-startups-bangladesh',
    'seo-howto-schema-bangladesh'
]

def get_post_by_slug(content, slug):
    """Extract post object by slug from JS array."""
    # Find the slug line
    pattern = rf'    slug: "{slug}"'
    idx = content.find(pattern)
    if idx == -1:
        return None
    
    # Go backwards to find opening {
    post_start = content.rfind('{', idx - 200, idx)
    if post_start == -1:
        post_start = idx - 50
    
    # Go forwards to find closing }, (end of this post object)
    search_start = idx + len(pattern)
    
    # The content field uses backticks. We need to find the closing `,
    # that matches the opening content: ` ... `,
    
    # Find the content: ` marker
    content_marker = 'content: `'
    cm_idx = content.find(content_marker, search_start)
    if cm_idx == -1:
        # Try with no space
        content_marker = 'content:`'
        cm_idx = content.find(content_marker, search_start)
    
    if cm_idx != -1:
        # Content starts after the marker
        content_start = cm_idx + len(content_marker)
        # Find the closing backtick followed by comma
        # The content ends with `,
        backtick_close = content.find('`,\n', content_start)
        if backtick_close != -1:
            post_end = backtick_close + 3  # Include `,\n
            # Then find the closing } of the post object
            close_brace = content.find('\n  }', post_end)
            if close_brace != -1:
                post_end = close_brace + 4  # Include \n  }
            return content[post_start:post_end]
    
    return None

def parse_field(post_text, field_name):
    patterns = [
        rf'{field_name}:\s*"([^"]*)"',
        rf"{field_name}:\s*'([^']*)'",
    ]
    for pattern in patterns:
        m = re.search(pattern, post_text, re.DOTALL)
        if m:
            return m.group(1)
    return None

def parse_tags(post_text):
    m = re.search(r'tags:\s*\[(.*?)\]', post_text, re.DOTALL)
    if m:
        tags_str = m.group(1)
        tags = re.findall(r'"([^"]*)"', tags_str)
        return tags
    return []

def extract_content(post_text):
    """Extract the content field between backticks."""
    m = re.search(r'content:\s*`\n(.*?)`,\n', post_text, re.DOTALL)
    if m:
        return m.group(1)
    return ''

def count_question_headings(text):
    """Count question-based headings (How/What/Why/When/Where/Can/Do/Is/Are)."""
    # Match headings that start with question words
    headings = re.findall(r'^(#{2,6})\s+(How|What|Why|When|Where|Can|Do|Is|Are)\b', text, re.MULTILINE)
    return len(headings), [h[1] + '...' for h in headings]

def check_pillar_link(text):
    return '/blog/complete-seo-guide-bangladesh-businesses-2026' in text

def keyword_occurrences(text, keyword):
    """Count how many times the core keyword appears."""
    return text.lower().count(keyword.lower())

def extract_primary_keyword_phrase(title):
    """Extract primary keyword phrases from title."""
    if not title:
        return "", ""
    # Remove common prefixes
    kw = title.replace("Complete ", "").replace("Why ", "").replace("How ", "")
    # Take first meaningful part
    return title, kw

def get_tfidf_keyword(tags, title):
    """Get the best keyword to check TF-IDF based on tags and title."""
    # Use the first tag as keyword, or the title's main subject
    return title

# Analyze each post
for slug in slugs:
    print(f"\n{'='*70}")
    print(f"## Post: {slug}")
    print(f"{'='*70}")
    
    post_text = get_post_by_slug(content, slug)
    if not post_text:
        print(f"ERROR: Could not extract post for {slug}")
        continue
    
    # Basic fields
    title = parse_field(post_text, 'title') or 'N/A'
    date = parse_field(post_text, 'date') or 'N/A'
    excerpt = parse_field(post_text, 'excerpt') or 'N/A'
    tags = parse_tags(post_text)
    content_text = extract_content(post_text)
    
    # Get content field directly from the raw post text
    # Clean up any HTML-like artifacts
    print(f"Title: {title}")
    print(f"Tags: {tags}")
    print(f"Content length: {len(content_text)} chars")
    
    # ---------- A. TF-IDF Coverage ----------
    print(f"\n### A. TF-IDF Coverage")
    # Use the first tag as primary keyword if available, or key part of title
    if tags:
        primary_kw = tags[0]
    else:
        primary_kw = title.split(':')[0].strip() if ':' in title else title
    
    kw_count = content_text.lower().count(primary_kw.lower())
    kw_flag = '✅' if kw_count >= 5 else '❌'
    print(f"TF-IDF: [{primary_kw}] | {kw_flag} | {kw_count} occurrences")
    
    # Also check other tag-based keywords
    for t in tags[1:]:
        c = content_text.lower().count(t.lower())
        print(f"  Tag '{t}': {c} occurrences")
    
    # ---------- B. Semantic Entity Coverage ----------
    print(f"\n### B. Semantic Entity Coverage")
    entity_checks = {
        'Dhaka': 'Dhaka' in content_text,
        'Bangladesh': 'Bangladesh' in content_text,
        'Chittagong': 'Chittagong' in content_text,
        'Sylhet': 'Sylhet' in content_text,
    }
    
    # Determine service type from tags
    service_found = []
    for tag in tags:
        if tag.lower() in content_text.lower():
            service_found.append(tag)
    
    missing_entities = [k for k, v in entity_checks.items() if not v]
    
    # Check for service type mentions
    service_check_passed = len(service_found) > 0
    
    print(f"  Dhaka/Bangladesh: {'✅' if entity_checks['Dhaka'] and entity_checks['Bangladesh'] else '❌'}")
    print(f"  Other cities (CTG/Sylhet): {'✅' if entity_checks['Chittagong'] or entity_checks['Sylhet'] else '❌'}")
    print(f"  Service type from tags in text: {'✅' if service_check_passed else '❌'}")
    if missing_entities:
        print(f"  Missing: {missing_entities}")
    
    # ---------- C. Pillar-Cluster Alignment ----------
    print(f"\n### C. Pillar-Cluster Alignment")
    has_pillar = check_pillar_link(content_text)
    print(f"  Links to pillar: {'✅' if has_pillar else '❌'}")
    if not has_pillar:
        print(f"  Missing: link to /blog/complete-seo-guide-bangladesh-businesses-2026")
    
    # ---------- D. AEO/GEO Optimization ----------
    print(f"\n### D. AEO/GEO Optimization")
    q_count, q_headings = count_question_headings(content_text)
    aeo_flag = '✅' if q_count >= 2 else '❌'
    print(f"  Question headings: {aeo_flag} | {q_count} found")
    for qh in q_headings:
        print(f"    - {qh}")
    
    # Also check for FAQ section
    has_faq = 'FAQ' in content_text or 'Frequently Asked' in content_text
    print(f"  FAQ section: {'✅' if has_faq else '❌'}")
    
    # ---------- E. Internal Linking ----------
    print(f"\n### E. Internal Linking")
    # Count all links starting with /
    all_internal = re.findall(r'(?<="|\(|\[)/[a-z][^)\s"\'<>]*', content_text)
    blog_links = re.findall(r'/blog/[^)\s"\'<>]+', content_text)
    services_links = re.findall(r'/services/[^)\s"\'<>]+', content_text)
    locations_links = re.findall(r'/locations/[^)\s"\'<>]+', content_text)
    other_links = re.findall(r'/industries/[^)\s"\'<>]+', content_text)
    
    total_internal = len(blog_links) + len(services_links) + len(locations_links) + len(other_links)
    
    flag_int = '✅' if total_internal >= 3 else '❌'
    print(f"  Internal links: {flag_int} | {total_internal} total")
    print(f"    /blog/: {len(blog_links)}")
    print(f"    /services/: {len(services_links)}")
    print(f"    /locations/: {len(locations_links)}")
    print(f"    /industries/: {len(other_links)}")
    
    # ---------- F. Schema Readiness ----------
    print(f"\n### F. Schema Readiness")
    title_ok = title != 'N/A' and len(title) > 0
    excerpt_ok = excerpt != 'N/A' and len(excerpt) > 0
    date_ok = date != 'N/A' and len(date) > 0
    
    # Check for author
    author = parse_field(post_text, 'author') or ''
    author_ok = len(author) > 0
    
    # Check for imagePlaceholder
    image = parse_field(post_text, 'imagePlaceholder') or ''
    image_ok = len(image) > 0
    
    all_schema_ok = title_ok and excerpt_ok and date_ok and author_ok and image_ok
    schema_flag = '✅' if all_schema_ok else '❌'
    
    print(f"  Schema Ready: {schema_flag}")
    print(f"    Title: {'✅' if title_ok else '❌'}")
    print(f"    Excerpt: {'✅' if excerpt_ok else '❌'}")
    print(f"    Date: {'✅' if date_ok else '❌'}")
    print(f"    Author: {'✅' if author_ok else '❌'}")
    print(f"    imagePlaceholder: {'✅' if image_ok else '❌'}")
    
    print()

print("=== DONE ===")
