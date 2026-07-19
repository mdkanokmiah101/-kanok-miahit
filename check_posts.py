#!/usr/bin/env python3
"""Analyze 4 blog posts from data.js for content framework checks."""

import re
import json

with open('src/app/blog/data.js', 'r', encoding='utf-8') as f:
    content = f.read()

slugs = [
    'seo-for-law-firms-bangladesh',
    'b2b-lead-generation-seo-bangladesh',
    'seo-for-startups-bangladesh',
    'seo-howto-schema-bangladesh'
]

def extract_post(content, slug):
    """Extract a single post object from the JS data file."""
    start_marker = f'    slug: "{slug}"'
    idx = content.find(start_marker)
    if idx == -1:
        start_marker = f'    slug: \\"{slug}\\"'
        idx = content.find(start_marker)
    if idx == -1:
        print(f"ERROR: Could not find {slug}")
        return None
    
    # Find post start - go back to find the opening {
    post_start = content.rfind('{', idx - 100, idx)
    if post_start == -1:
        post_start = idx - 10
    
    # Find where this post ends - look for '},\n{' after the content
    search_from = idx + len(start_marker)
    
    # The post ends with the closing `, followed by a newline, then '},'
    # Try to find the closing backtick of the content field and then '},'
    
    # Find the end of the content field (the backtick followed by `,)
    # Last occurrence of `,\n  }, in the post
    # Let me find the last backtick followed by comma and newline
    end_marker = "`,\n  }"
    end_idx = content.find(end_marker, search_from)
    if end_idx == -1:
        end_marker = "`,\n}"
        end_idx = content.find(end_marker, search_from)
    if end_idx == -1:
        print(f"ERROR: Could not find end for {slug}")
        # Try to find by looking for next slug
        for s in slugs:
            if s == slug:
                continue
            mkr = f'    slug: "{s}"'
            ei = content.find(mkr, search_from)
            if ei != -1:
                end_idx = ei - 10
                break
    
    if end_idx == -1:
        print(f"ERROR: Cannot find end boundary for {slug}")
        return None
    
    # Include the closing
    post_text = content[post_start:end_idx + len(end_marker)]
    return post_text

def parse_field(post_text, field_name):
    """Extract a field value from a JS object string."""
    patterns = [
        rf'{field_name}:\s*"([^"]*)"',
        rf'{field_name}:\s*`([^`]*)`',
        rf"{field_name}:\s*'([^']*)'",
    ]
    for pattern in patterns:
        m = re.search(pattern, post_text, re.DOTALL)
        if m:
            return m.group(1)
    return None

def parse_tags(post_text):
    """Extract tags array."""
    m = re.search(r'tags:\s*\[(.*?)\]', post_text, re.DOTALL)
    if m:
        tags_str = m.group(1)
        tags = re.findall(r'"([^"]*)"', tags_str)
        return tags
    return []

def count_keyword(text, keyword):
    """Count occurrences of a keyword in text."""
    if not keyword:
        return 0
    return text.lower().count(keyword.lower())

def count_question_headings(text):
    """Count question-based headings (How/What/Why/When/Where/Can/Do/Is/Are)."""
    heading_pattern = re.findall(r'^#{2,6}\s+(How|What|Why|When|Where|Can|Do|Is|Are)\b', text, re.MULTILINE)
    return len(heading_pattern)

def count_internal_links(text):
    """Count internal links (/blog/, /services/, /locations/)."""
    blog_links = len(re.findall(r'/blog/[^)\"\']+', text))
    services_links = len(re.findall(r'/services/[^)\"\']+', text))
    locations_links = len(re.findall(r'/locations/[^)\"\']+', text))
    other_internal = len(re.findall(r'/(about|contact|industries)[^)\"\']*', text))
    return blog_links + services_links + locations_links + other_internal, blog_links, services_links, locations_links

def extract_primary_keyword(title):
    """Extract primary keyword from title."""
    # Simple extraction: take the first noun phrase or key term
    if not title:
        return ""
    # Remove prefix like "Why" or "Complete" or "How To"
    # For now just use the full title
    return title

def check_pillar_link(text):
    """Check if post links to /blog/complete-seo-guide-bangladesh-businesses-2026"""
    return '/blog/complete-seo-guide-bangladesh-businesses-2026' in text

def check_entities(text, service_type, industry):
    """Check for semantic entities."""
    entities = {
        'Dhaka': 'Dhaka' in text,
        'Bangladesh': 'Bangladesh' in text,
        'service_type': service_type.lower() in text.lower() if service_type else False,
        'industry': industry.lower() in text.lower() if industry else False,
    }
    return entities

# Main analysis
for slug in slugs:
    print(f"\n{'='*70}")
    print(f"## Post: {slug}")
    print(f"{'='*70}")
    
    post_text = extract_post(content, slug)
    if not post_text:
        print("ERROR: Could not extract post")
        continue
    
    # Parse fields
    title = parse_field(post_text, 'title')
    date = parse_field(post_text, 'date')
    excerpt = parse_field(post_text, 'excerpt')
    tags = parse_tags(post_text)
    content_text = parse_field(post_text, 'content') or ''
    
    print(f"Title: {title}")
    print(f"Date: {date}")
    print(f"Excerpt (first 80 chars): {excerpt[:80] if excerpt else 'N/A'}...")
    print(f"Tags: {tags}")
    print(f"Content length: {len(content_text)} chars")
    
    # A. TF-IDF Coverage
    primary_kw = title  # Use title as primary keyword approximation
    kw_count = count_keyword(content_text, primary_kw) if primary_kw else 0
    # Also try counting the main concept words
    print(f"\n--- A. TF-IDF Coverage ---")
    print(f"Primary keyword (title): {primary_kw}")
    print(f"Exact title occurrences in content: {kw_count}")
    
    # B. Semantic Entity Coverage
    print(f"\n--- B. Semantic Entity Coverage ---")
    entities = {}
    for entity in ['Dhaka', 'Bangladesh', 'Chittagong', 'Sylhet']:
        entities[entity] = entity.lower() in content_text.lower()
        print(f"  {entity}: {'✅' if entities[entity] else '❌'}")
    
    # Service type - try to infer from tags
    service_terms = ['SEO', 'legal', 'law', 'B2B', 'lead generation', 'startup', 'HowTo', 'schema']
    for term in service_terms:
        if term.lower() in content_text.lower():
            print(f"  Service term '{term}': ✅")
    
    # C. Pillar-Cluster Alignment
    print(f"\n--- C. Pillar-Cluster Alignment ---")
    has_pillar_link = check_pillar_link(content_text)
    print(f"Links to pillar page (/blog/complete-seo-guide-bangladesh-businesses-2026): {'✅' if has_pillar_link else '❌'}")
    
    # D. AEO/GEO Optimization
    print(f"\n--- D. AEO/GEO Optimization ---")
    q_headings = count_question_headings(content_text)
    print(f"Question-based headings count: {q_headings}")
    
    # E. Internal Linking
    print(f"\n--- E. Internal Linking ---")
    total_links, blog_links, services_links, locations_links = count_internal_links(content_text)
    print(f"Total internal links: {total_links}")
    print(f"  /blog/ links: {blog_links}")
    print(f"  /services/ links: {services_links}")
    print(f"  /locations/ links: {locations_links}")
    
    # F. Schema Readiness
    print(f"\n--- F. Schema Readiness ---")
    title_set = title is not None and len(title) > 0
    excerpt_set = excerpt is not None and len(excerpt) > 0
    date_set = date is not None and len(date) > 0
    author = parse_field(post_text, 'author')
    author_set = author is not None and len(author) > 0
    print(f"  Title: {'✅' if title_set else '❌'}")
    print(f"  Excerpt: {'✅' if excerpt_set else '❌'}")
    print(f"  Date: {'✅' if date_set else '❌'}")
    print(f"  Author: {'✅' if author_set else '❌'}")
    
    print()

print("=== ANALYSIS COMPLETE ===")
