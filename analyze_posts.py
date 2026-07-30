#!/usr/bin/env python3
"""Analyze modified blog posts for framework compliance."""

import re
import json
import sys

# Read the data.js file
with open('/root/kanok-miahit/src/app/blog/data.js', 'r', encoding='utf-8') as f:
    js_text = f.read()

# Modified post slugs to check
slugs = [
    "locksmith-dundee-seo-case-study",
    "landlord-certificates-seo-case-study",
    "das-taxis-scotland-seo-case-study",
    "morethanpanel-seo-case-study",
    "smmgen-seo-case-study",
    "smmsun-seo-case-study",
    "mir-cement-seo-case-study",
    "dhaka-apparels-seo-case-study",
    "stealth-windshield-repairs-seo-case-study",
    "how-to-choose-best-seo-expert-dhaka-15-things",
    "seo-expert-vs-seo-agency-dhaka-which-is-right",
    "top-10-seo-mistakes-dhaka-businesses-fix",
    "what-does-seo-expert-do-guide-business-owners",
    "seo-case-study-dhaka-businesses-increased-organic-traffic",
    "hiring-seo-expert-dhaka-better-roi-than-paid-ads",
    "ai-seo-2026-dhaka-experts-optimize-google-ai-chatgpt",
    "watchzonebd-seo-case-study",
]

# Extract all posts using regex - each post starts with { and ends with },
# We'll use a more robust approach: find the post objects

def extract_posts(text):
    """Extract individual post objects from the JS array."""
    # Find the start of posts array
    array_start = text.find("const posts = [\n")
    if array_start == -1:
        print("ERROR: Could not find posts array")
        return []
    
    # Now we need to parse the JS objects
    # Strategy: find each slug declaration and extract the full object
    
    posts = []
    # Find all slug declarations with their positions
    slug_pattern = re.compile(r"slug:\s*'([^']+)'")
    
    # Find all post objects by looking for { at slug positions
    # We'll iterate through the file finding each post
    
    lines = text.split('\n')
    
    current_post = None
    brace_depth = 0
    in_content = False
    content_delimiter = None
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        if current_post is None:
            # Look for start of a post object
            stripped = line.strip()
            if stripped == '{' or stripped.startswith('{') and not stripped.startswith('{,'):
                # Could be a post start - check if it has slug
                current_post = {'lines': [line]}
                brace_depth = line.count('{') - line.count('}')
                in_content = False
                content_delimiter = None
        else:
            current_post['lines'].append(line)
            brace_depth += line.count('{') - line.count('}')
            
            # Check if we're entering content
            if not in_content and 'content:' in line:
                in_content = True
                # Check if content starts on this line
                stripped_line = line.strip()
                if stripped_line.startswith('content:'):
                    rest = stripped_line[len('content:'):].strip()
                    if rest.startswith('`'):
                        content_delimiter = '`'
                    elif rest.startswith("'"):
                        content_delimiter = "'"
                    elif rest.startswith('"'):
                        content_delimiter = '"'
            
            # If brace depth is 0, we've closed the object
            if brace_depth <= 0 and not in_content:
                # But we might still be in content with backtick
                pass
            
            if brace_depth <= 0:
                # Check for closing brace
                if '}' in line and brace_depth <= 0:
                    # Post complete
                    post_text = '\n'.join(current_post['lines'])
                    posts.append(post_text)
                    current_post = None
                    brace_depth = 0
                    in_content = False
                    content_delimiter = None
        
        i += 1
    
    return posts

# Better approach: use regex to find content between top-level braces
# But content contains backticks/braces too...
# Let's try a different approach

def parse_js_objects(text):
    """Parse JavaScript objects with template literal content."""
    objects = []
    
    # Find the start of posts array
    match = re.search(r'const posts\s*=\s*\[', text)
    if not match:
        print("ERROR: Could not find posts array")
        return objects
    
    start_idx = match.end()
    
    # Now find each top-level object
    i = start_idx
    while i < len(text):
        # Skip whitespace
        while i < len(text) and text[i] in ' \n\r\t,':
            i += 1
        
        if i >= len(text) or text[i] == ']':
            break
        
        if text[i] == '{':
            # Parse one object
            obj_start = i
            brace_depth = 0
            in_backtick = False
            in_single_quote = False
            in_double_quote = False
            
            while i < len(text):
                ch = text[i]
                
                if ch == '\\' and i + 1 < len(text):
                    i += 2
                    continue
                
                if ch == '`' and not in_single_quote and not in_double_quote:
                    in_backtick = not in_backtick
                elif ch == "'" and not in_backtick and not in_double_quote:
                    in_single_quote = not in_single_quote
                elif ch == '"' and not in_backtick and not in_single_quote:
                    in_double_quote = not in_double_quote
                elif ch == '{' and not in_backtick and not in_single_quote and not in_double_quote:
                    brace_depth += 1
                elif ch == '}' and not in_backtick and not in_single_quote and not in_double_quote:
                    brace_depth -= 1
                    if brace_depth == 0:
                        obj_text = text[obj_start:i+1]
                        objects.append(obj_text)
                        i += 1
                        break
                
                i += 1
            else:
                break
        else:
            # Unexpected character, skip
            i += 1
    
    return objects

objects = parse_js_objects(js_text)
print(f"Found {len(objects)} total post objects")

# Build a dict by slug
def extract_slug(obj_text):
    m = re.search(r'slug:\s*"([^"]+)"', obj_text)
    return m.group(1) if m else None

def extract_field(obj_text, field_name):
    """Extract a simple string field value."""
    # Match field_name: "value" (double quotes)
    pattern = rf'{field_name}:\s*"([^"]*)"'
    m = re.search(pattern, obj_text)
    if m:
        return m.group(1)
    # Try single quotes
    pattern = rf"{field_name}:\s*'([^']*)'"
    m = re.search(pattern, obj_text)
    return m.group(1) if m else None

def extract_content(obj_text):
    """Extract the content template literal."""
    m = re.search(r'content:\s*`((?:[^`\\]|\\.)*)`', obj_text, re.DOTALL)
    if m:
        return m.group(1)
    return None

def extract_content_fallback(obj_text):
    """More robust content extraction."""
    m = re.search(r'content:\s*`', obj_text)
    if not m:
        return None
    start = m.end()
    depth = 0
    result_chars = []
    i = start
    while i < len(obj_text):
        ch = obj_text[i]
        if ch == '\\' and i + 1 < len(obj_text):
            result_chars.append(ch)
            result_chars.append(obj_text[i+1])
            i += 2
            continue
        if ch == '`':
            result_chars.append(ch)
            break
        result_chars.append(ch)
        i += 1
    return ''.join(result_chars[:-1])  # remove the closing backtick

# Map slugs to posts
posts_by_slug = {}
for obj in objects:
    slug = extract_slug(obj)
    if slug:
        posts_by_slug[slug] = obj

print(f"Found {len(posts_by_slug)} unique slugs")

# Now check each modified slug
for slug in slugs:
    print(f"\n{'='*80}")
    print(f"POST: {slug}")
    print(f"{'='*80}")
    
    obj = posts_by_slug.get(slug)
    if not obj:
        print(f"  ERROR: Post not found!")
        continue
    
    # Extract fields
    title = extract_field(obj, 'title')
    excerpt = extract_field(obj, 'excerpt')
    date = extract_field(obj, 'date')
    
    print(f"  Title: {title[:80] if title else 'MISSING'}...")
    print(f"  Excerpt: {excerpt[:80] if excerpt else 'MISSING'}...")
    print(f"  Date: {date if date else 'MISSING'}")
    
    content = extract_content_fallback(obj)
    if not content:
        print(f"  WARNING: Could not extract content")
        continue
    
    print(f"  Content length: {len(content)} chars")
    
    # --- CHECK 1: TF-IDF (keyword frequency >= 5) ---
    # Count occurrences of key terms
    keywords = {
        'seo': len(re.findall(r'\bSEO\b', content, re.IGNORECASE)),
        'bangladesh': len(re.findall(r'\bBangladesh\b', content, re.IGNORECASE)),
        'dhaka': len(re.findall(r'\bDhaka\b', content, re.IGNORECASE)),
        'organic': len(re.findall(r'\borganic\b', content, re.IGNORECASE)),
        'traffic': len(re.findall(r'\btraffic\b', content, re.IGNORECASE)),
        'google': len(re.findall(r'\bGoogle\b', content, re.IGNORECASE)),
        'local': len(re.findall(r'\blocal\b', content, re.IGNORECASE)),
        'services': len(re.findall(r'\bservices\b', content, re.IGNORECASE)),
    }
    has_tfidf = any(v >= 5 for v in keywords.values())
    print(f"  CHECK 1 - TF-IDF (keyword freq >=5): {'PASS' if has_tfidf else 'FAIL'}")
    for k, v in keywords.items():
        print(f"    '{k}': {v}")
    
    # --- CHECK 2: Entity coverage (Bangladesh/Dhaka + services) ---
    has_bangladesh = keywords['bangladesh'] >= 1 or keywords['dhaka'] >= 1
    has_services = keywords['services'] >= 1 or 'local seo' in content.lower() or 'seo services' in content.lower()
    has_entity = has_bangladesh and has_services
    print(f"  CHECK 2 - Entity coverage (Bangladesh/Dhaka + services): {'PASS' if has_entity else 'FAIL'}")
    print(f"    Bangladesh/Dhaka mention: {has_bangladesh}")
    print(f"    Services mention: {has_services}")
    
    # --- CHECK 3: Pillar-cluster alignment (links to services) ---
    # Find markdown links to /services/...
    service_links = re.findall(r'\[([^\]]*)\]\((/services/[^\)]+)\)', content)
    has_pillar = len(service_links) >= 1
    print(f"  CHECK 3 - Pillar-cluster alignment (links to services): {'PASS' if has_pillar else 'FAIL'}")
    for text, url in service_links:
        print(f"    [{text}]({url})")
    if not service_links:
        print(f"    No service links found")
    
    # --- CHECK 4: AEO/GEO (>= 2 question headings) ---
    # Find headings that are questions (contain ?)
    # Headings in markdown: ## ..., ### ..., etc.
    question_headings = []
    heading_pattern = re.compile(r'^#{2,6}\s+(.*)', re.MULTILINE)
    for match in heading_pattern.finditer(content):
        heading_text = match.group(1)
        if '?' in heading_text:
            question_headings.append(heading_text.strip())
    has_aeo_geo = len(question_headings) >= 2
    print(f"  CHECK 4 - AEO/GEO (>= 2 question headings): {'PASS' if has_aeo_geo else 'FAIL'}")
    for q in question_headings:
        print(f"    Q: {q}")
    if len(question_headings) < 2:
        print(f"    Only {len(question_headings)} question heading(s) found")
    
    # --- CHECK 5: Internal linking (>= 3 unique internal links) ---
    # Find all markdown links to internal pages (not external)
    # Internal links: (/path) or (/blog/path) or (/services/path) or (/locations/path)
    all_markdown_links = re.findall(r'\[([^\]]*)\]\(([^\)]+)\)', content)
    internal_links = []
    for text, url in all_markdown_links:
        # Exclude external URLs (http, https, mailto, tel)
        if url.startswith('/') and not url.startswith('//'):
            internal_links.append((text, url))
    
    # Get unique URLs
    unique_internal_urls = set(url for _, url in internal_links)
    has_internal_linking = len(unique_internal_urls) >= 3
    print(f"  CHECK 5 - Internal linking (>= 3 unique internal links): {'PASS' if has_internal_linking else 'FAIL'}")
    for text, url in internal_links:
        print(f"    [{text}]({url})")
    if len(unique_internal_urls) < 3:
        print(f"    Only {len(unique_internal_urls)} unique internal links found")
    
    # --- CHECK 6: Schema readiness (title, excerpt, date present) ---
    has_title = title is not None and len(title.strip()) > 0
    has_excerpt = excerpt is not None and len(excerpt.strip()) > 0
    has_date = date is not None and len(date.strip()) > 0
    has_schema = has_title and has_excerpt and has_date
    print(f"  CHECK 6 - Schema readiness (title, excerpt, date): {'PASS' if has_schema else 'FAIL'}")
    print(f"    Title present: {has_title}")
    print(f"    Excerpt present: {has_excerpt}")
    print(f"    Date present: {has_date}")
    
    # --- SUMMARY ---
    checks = [has_tfidf, has_entity, has_pillar, has_aeo_geo, has_internal_linking, has_schema]
    passed = sum(1 for c in checks if c)
    total = len(checks)
    print(f"  RESULT: {passed}/{total} checks passed")

print(f"\n{'='*80}")
print("SUMMARY TABLE")
print(f"{'='*80}")
print(f"{'Post':<50} {'TF-IDF':<8} {'Entity':<8} {'Pillar':<8} {'AEO/GEO':<8} {'IntLink':<8} {'Schema':<8} {'Score':<6}")
print(f"{'-'*50} {'-'*8} {'-'*8} {'-'*8} {'-'*8} {'-'*8} {'-'*8} {'-'*6}")

results = {}
for slug in slugs:
    obj = posts_by_slug.get(slug)
    if not obj:
        print(f"{slug:<50} {'N/A':<8} {'N/A':<8} {'N/A':<8} {'N/A':<8} {'N/A':<8} {'N/A':<8} {'N/A':<6}")
        continue
    
    title = extract_field(obj, 'title')
    excerpt = extract_field(obj, 'excerpt')
    date = extract_field(obj, 'date')
    content = extract_content_fallback(obj)
    
    if not content:
        print(f"{slug:<50} {'ERR':<8} {'ERR':<8} {'ERR':<8} {'ERR':<8} {'ERR':<8} {'ERR':<8} {'ERR':<6}")
        continue
    
    # TF-IDF
    seo_count = len(re.findall(r'\bSEO\b', content, re.IGNORECASE))
    dhaka_count = len(re.findall(r'\bDhaka\b', content, re.IGNORECASE))
    bangladesh_count = len(re.findall(r'\bBangladesh\b', content, re.IGNORECASE))
    services_count = len(re.findall(r'\bservices\b', content, re.IGNORECASE))
    organic_count = len(re.findall(r'\borganic\b', content, re.IGNORECASE))
    traffic_count = len(re.findall(r'\btraffic\b', content, re.IGNORECASE))
    keywords = {'seo': seo_count, 'dhaka': dhaka_count, 'bangladesh': bangladesh_count, 'services': services_count, 'organic': organic_count, 'traffic': traffic_count}
    c1 = any(v >= 5 for v in keywords.values())
    
    # Entity
    c2 = (bangladesh_count >= 1 or dhaka_count >= 1) and (services_count >= 1 or 'local seo' in content.lower() or 'seo services' in content.lower())
    
    # Pillar
    service_links = re.findall(r'\[([^\]]*)\]\((/services/[^\)]+)\)', content)
    c3 = len(service_links) >= 1
    
    # AEO/GEO
    question_headings = []
    heading_pattern = re.compile(r'^#{2,6}\s+(.*)', re.MULTILINE)
    for match in heading_pattern.finditer(content):
        ht = match.group(1)
        if '?' in ht:
            question_headings.append(ht.strip())
    c4 = len(question_headings) >= 2
    
    # Internal links
    all_links = re.findall(r'\[([^\]]*)\]\(([^\)]+)\)', content)
    internal_urls = set(url for _, url in all_links if url.startswith('/') and not url.startswith('//'))
    c5 = len(internal_urls) >= 3
    
    # Schema
    c6 = bool(title and title.strip() and excerpt and excerpt.strip() and date and date.strip())
    
    score = f"{sum([c1,c2,c3,c4,c5,c6])}/6"
    
    print(f"{slug[:48]:<50} {'PASS' if c1 else 'FAIL':<8} {'PASS' if c2 else 'FAIL':<8} {'PASS' if c3 else 'FAIL':<8} {'PASS' if c4 else 'FAIL':<8} {'PASS' if c5 else 'FAIL':<8} {'PASS' if c6 else 'FAIL':<8} {score:<6}")
    
    results[slug] = {
        'tfidf': c1, 'entity': c2, 'pillar': c3, 'aeo_geo': c4, 'internal_link': c5, 'schema': c6,
        'tfidf_counts': keywords,
        'service_links': [f"[{t}]({u})" for t,u in service_links],
        'question_headings': question_headings,
        'internal_link_count': len(internal_urls),
    }

print(f"\n{'='*80}")
print("DETAILED FAILURES")
print(f"{'='*80}")

for slug, r in results.items():
    failures = []
    if not r['tfidf']:
        failures.append(f"TF-IDF (max freq: {max(r['tfidf_counts'].values())})")
    if not r['entity']:
        failures.append("Entity coverage")
    if not r['pillar']:
        failures.append("Pillar-cluster (no service links)")
    if not r['aeo_geo']:
        failures.append(f"AEO/GEO ({len(r['question_headings'])} question headings, need >=2)")
    if not r['internal_link']:
        failures.append(f"Internal linking ({r['internal_link_count']} unique links, need >=3)")
    if not r['schema']:
        failures.append("Schema readiness")
    
    if failures:
        print(f"\n  FAILED: {slug}")
        for f in failures:
            print(f"    - {f}")
    else:
        print(f"\n  ALL PASS: {slug}")
