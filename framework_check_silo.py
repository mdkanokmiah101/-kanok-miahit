#!/usr/bin/env python3
"""Framework enforcement check for recently modified blog posts."""

import re
import json
import sys

# Load data.js as text
with open('/root/kanok-miahit/src/app/blog/data.js', 'r') as f:
    js_text = f.read()

# Extract post slug we care about
TARGET_SLUGS = [
    "how-to-choose-best-seo-expert-dhaka-15-things",
    "mobile-seo-optimization-bangladesh-mobile-first-era"
]

def extract_post(slug):
    """Extract a single post object from data.js by slug."""
    # Find the slug definition
    slug_pattern = r"slug:\s*\"(" + re.escape(slug) + r")\""
    match = re.search(slug_pattern, js_text)
    if not match:
        return None
    
    # Find the enclosing object - go backwards to find the opening {, forward to find the closing },
    slug_pos = match.start()
    
    # Go backwards to find the opening brace of this object
    search_start = max(0, slug_pos - 2000)
    obj_start = js_text.rfind('{', search_start, slug_pos)
    # Make sure we found a proper opening
    if obj_start < 0:
        # Try a slightly different approach
        obj_start = js_text.rfind('{', 0, slug_pos - 10)
    
    if obj_start < 0:
        return None
    
    # Find the matching closing brace - count braces
    depth = 0
    in_content = False
    content_marker = None
    
    for i in range(obj_start, len(js_text)):
        ch = js_text[i]
        if ch == '`' and not in_content:
            # Could be start of template literal - check context
            if i > 0 and js_text[i-1] == ' ' and i+1 < len(js_text) and js_text[i+1] == '\n':
                in_content = True
                content_marker = i
            elif i > 0 and js_text[i-1:i+2] in ['  \n', '  `', '   ']:
                # Various edge cases
                pass
        elif ch == '`' and in_content:
            # Check if this ends the content (followed by `,` or `}`)
            in_content = False
        
        if not in_content:
            if ch == '{':
                depth += 1
            elif ch == '}':
                depth -= 1
                if depth == 0:
                    obj_end = i + 1
                    break
    else:
        return None
    
    obj_text = js_text[obj_start:obj_end]
    return obj_text

def extract_field(post_text, field_name):
    """Extract a field value from a post object."""
    # Match field: "value" or field:\n      "value" (multiline)
    patterns = [
        rf'{field_name}:\s*"([^"]*)"',
        rf'{field_name}:\s*\n\s*"([^"]*)"',
        rf"{field_name}:\s*'([^']*)'",
        rf'{field_name}:\s*\n\s*\[([^\]]+)\]',
    ]
    
    for p in patterns:
        m = re.search(p, post_text)
        if m:
            return m.group(1)
    return None

def extract_content(post_text):
    """Extract content from template literal."""
    m = re.search(r'content:\s*`\n(.*?)`\s*,', post_text, re.DOTALL)
    if m:
        return m.group(1)
    return ""

def count_keyword(content, keyword):
    """Count occurrences of a keyword in content (case-insensitive)."""
    return len(re.findall(re.escape(keyword), content, re.IGNORECASE))

def extract_primary_keyword(title):
    """Extract primary keyword from title (first meaningful noun phrase)."""
    # Remove common prefixes
    title_lower = title.lower()
    
    # Common patterns for blog titles
    # "How to Choose the Best SEO Expert in Dhaka: 15 Things to Check"
    # Try to extract the key noun phrase
    
    # Pattern 1: "X for Y" -> extract Y
    m = re.search(r'for\s+(.+?)(?:\s*[:–—]|$)', title_lower)
    if m:
        kw = m.group(1).strip()
        # Remove trailing punctuation
        kw = re.sub(r'[:;,.!?]$', '', kw)
        return kw
    
    # Pattern 2: Look for the main subject after "How to [verb]" 
    m = re.search(r'how to\s+\w+\s+(.+?)(?:\s*[:–—]|$)', title_lower)
    if m:
        return m.group(1).strip()
    
    # Pattern 3: First meaningful bigram/trigram
    words = title_lower.split()
    # Find first noun-looking sequence (skip articles, prepositions, etc)
    skip_words = {'how', 'to', 'the', 'a', 'an', 'for', 'in', 'of', 'on', 'at', 'is', 'are', 'your'}
    for i, w in enumerate(words):
        if w not in skip_words and len(w) > 2:
            # Take this word and up to 2 more
            kw = ' '.join(words[i:i+3])
            kw = re.sub(r'[:;,.!?]', '', kw)
            return kw
    
    return title_lower

def check_entities(content, title):
    """Check for required entities."""
    title_lower = title.lower()
    content_lower = content.lower()
    
    entities = {
        'location_dhaka': 'Dhaka',
        'location_bangladesh': 'Bangladesh',
    }
    
    # Determine service type from title/content
    if 'seo' in title_lower:
        entities['service_seo'] = 'SEO'
    if 'expert' in title_lower:
        entities['service_expert'] = 'SEO Expert'
    
    # Check if specific neighborhoods mentioned
    neighborhoods = ['Gulshan', 'Banani', 'Uttara', 'Dhanmondi', 'Mirpur', 'Motijheel', 'Badda', 'Bashundhara']
    found_neighborhoods = [n for n in neighborhoods if n.lower() in content_lower]
    
    missing = []
    present = []
    
    for key, entity_name in entities.items():
        if entity_name.lower() in content_lower:
            present.append(entity_name)
        else:
            missing.append(entity_name)
    
    return {
        'missing': missing,
        'present': present,
        'found_neighborhoods': found_neighborhoods
    }

def count_question_headings(content):
    """Count question-based headings (## or ### starting with How, What, Why, etc.)."""
    # Match headings that start with question words
    patterns = [
        r'^#{2,4}\s+(How\s.+)',
        r'^#{2,4}\s+(What\s.+)',
        r'^#{2,4}\s+(Why\s.+)',
        r'^#{2,4}\s+(When\s.+)',
        r'^#{2,4}\s+(Where\s.+)',
        r'^#{2,4}\s+(Can\s.+)',
        r'^#{2,4}\s+(Do\s.+)',
        r'^#{2,4}\s+(Is\s.+)',
        r'^#{2,4}\s+(Are\s.+)',
        r'^#{2,4}\s+(\w+\s+.+\?)',  # Any heading ending with ?
    ]
    
    headings = []
    for p in patterns:
        matches = re.findall(p, content, re.MULTILINE)
        headings.extend(matches)
    
    # Deduplicate
    return len(set(headings)), headings[:5]

def count_internal_links(content):
    """Count internal links (to /blog/, /services/, /locations/, /industries/, /about, /contact)."""
    # Internal links are relative paths
    patterns = [
        r'/blog/[^\s\)\"\']+',
        r'/services/[^\s\)\"\']+',
        r'/locations/[^\s\)\"\']+',
        r'/industries/[^\s\)\"\']+',
        r'/about\b',
        r'/contact\b',
        r'/case-studies\b',
        r'/\[/?\]',  # Link to homepage
    ]
    
    links = []
    for p in patterns:
        found = re.findall(p, content)
        links.extend(found)
    
    # Also find markdown links: [text](/path)
    md_links = re.findall(r'\]\(([^)]+)\)', content)
    internal_md = [l for l in md_links if l.startswith('/') and not l.startswith('//')]
    links.extend(internal_md)
    
    # Deduplicate
    unique_links = list(set(links))
    return len(unique_links), unique_links

def check_pillar_link(content, tags):
    """Check if post links to its pillar page based on tags."""
    pillar_map = {
        'SEO Expert': ['/about', '/services/local-seo', '/blog/seo-consultant-dhaka-bangladesh'],
        'SEO Agency': ['/services', '/blog/seo-expert-vs-seo-agency-dhaka-which-is-right'],
        'Mobile SEO': ['/services/technical-seo', '/blog/mobile-seo-optimization-bangladesh-mobile-first-era'],
        'Local SEO': ['/services/local-seo'],
        'Technical SEO': ['/services/technical-seo'],
        'Content': ['/services/on-page-seo'],
        'Case Study': ['/case-studies'],
    }
    
    content_lower = content.lower()
    found_pillar_links = []
    
    for tag in tags:
        for pillar, links in pillar_map.items():
            if pillar.lower() in tag.lower():
                for link in links:
                    if link in content:
                        found_pillar_links.append(link)
    
    # Also check for any /services/ or /about link broadly
    if not found_pillar_links:
        broad_links = ['/about', '/services', '/case-studies']
        for bl in broad_links:
            if bl in content:
                found_pillar_links.append(bl)
    
    return found_pillar_links

def check_schema_fields(post_text):
    """Check if post has fields needed for ArticleSchema."""
    fields = {
        'title': bool(re.search(r'title:\s', post_text)),
        'date': bool(re.search(r'date:\s', post_text)),
        'excerpt': bool(re.search(r'excerpt:\s', post_text)),
        'author': bool(re.search(r'author:\s', post_text)),
        'slug': bool(re.search(r'slug:\s', post_text)),
    }
    
    # Optional but recommended
    meta_extras = {
        'metaTitle': bool(re.search(r'metaTitle:\s', post_text)),
        'metaDescription': bool(re.search(r'metaDescription:\s', post_text)),
        'dateModified': bool(re.search(r'dateModified:\s', post_text)),
    }
    
    missing = [k for k, v in fields.items() if not v]
    missing_extras = [k for k, v in meta_extras.items() if not v]
    
    return {
        'required_missing': missing,
        'optional_missing': missing_extras,
        'all_required': len(missing) == 0
    }

# Process each target slug
for slug in TARGET_SLUGS:
    print(f"\n{'='*70}")
    print(f"## Post: {slug}")
    print(f"{'='*70}")
    
    post_text = extract_post(slug)
    if not post_text:
        # Try simpler approach - just find the section
        idx = js_text.find(f'slug: "{slug}"')
        if idx >= 0:
            # Find the enclosing block
            start = js_text.rfind('{\n', 0, idx)
            end = js_text.find('},\n', idx)
            if end < 0:
                end = js_text.find('},', idx)
            if end > 0:
                post_text = js_text[start:end+2]
    
    if not post_text:
        print(f"  ❌ Could not extract post data for {slug}")
        continue
    
    title = extract_field(post_text, 'title')
    if not title:
        # Try extracting from text directly
        m = re.search(r'title:\s*"([^"]+)"', post_text)
        title = m.group(1) if m else "Unknown"
    
    tags_raw = extract_field(post_text, 'tags')
    if tags_raw:
        tags = re.findall(r'"([^"]+)"', tags_raw)
    else:
        tags = []
    
    content = extract_content(post_text)
    
    if not content:
        print(f"  ⚠️ Could not extract content for {slug}")
        continue
    
    print(f"\n  Title: {title}")
    print(f"  Tags: {tags}")
    print(f"  Content length: {len(content)} chars")
    
    # A. TF-IDF Coverage
    primary_kw = extract_primary_keyword(title)
    kw_count = count_keyword(content, primary_kw)
    tfidf_status = "✅" if kw_count >= 5 else "❌"
    print(f"\n  ### A. TF-IDF Coverage")
    print(f"  Primary keyword: '{primary_kw}'")
    print(f"  | TF-IDF | {tfidf_status} | {kw_count} occurrences |")
    
    # B. Semantic Entity Coverage
    entity_result = check_entities(content, title)
    entity_status = "✅" if len(entity_result['missing']) == 0 else "❌"
    print(f"\n  ### B. Semantic Entity Coverage")
    print(f"  | Entities | {entity_status} | Missing: {entity_result['missing'] or 'None'} |")
    if entity_result['found_neighborhoods']:
        print(f"  Neighborhoods found: {entity_result['found_neighborhoods']}")
    
    # C. Pillar-Cluster Alignment
    pillar_links = check_pillar_link(content, tags)
    pillar_status = "✅" if pillar_links else "❌"
    print(f"\n  ### C. Pillar-Cluster Alignment")
    print(f"  | Pillar Link | {pillar_status} | Links to: {pillar_links or 'None'} |")
    
    # D. AEO/GEO Optimization
    q_count, q_examples = count_question_headings(content)
    aeo_status = "✅" if q_count >= 2 else "❌"
    print(f"\n  ### D. AEO/GEO Optimization")
    print(f"  | AEO/GEO | {aeo_status} | {q_count} question headings |")
    if q_examples:
        print(f"  Examples: {q_examples[:3]}")
    
    # E. Internal Linking
    link_count, links = count_internal_links(content)
    link_status = "✅" if link_count >= 3 else "❌"
    print(f"\n  ### E. Internal Linking")
    print(f"  | Internal Links | {link_status} | {link_count} total |")
    if links:
        print(f"  Links: {links[:10]}")
    
    # F. Schema
    schema_result = check_schema_fields(post_text)
    schema_status = "✅" if schema_result['all_required'] else "❌"
    print(f"\n  ### F. Schema Ready")
    print(f"  | Schema | {schema_status} | Required missing: {schema_result['required_missing'] or 'None'} |")
    if schema_result['optional_missing']:
        print(f"  Optional missing: {schema_result['optional_missing']}")
    
    # Summary
    print(f"\n  ---")
    all_pass = tfidf_status == "✅" and entity_status == "✅" and pillar_status == "✅" and aeo_status == "✅" and link_status == "✅" and schema_status == "✅"
    print(f"  Overall: {'✅ ALL CHECKS PASSED' if all_pass else '❌ SOME CHECKS FAILED - see fix instructions above'}")
