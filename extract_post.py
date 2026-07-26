#!/usr/bin/env python3
"""Extract a blog post from data.js by slug line number."""
import re, sys

with open('src/app/blog/data.js', 'r') as f:
    lines = f.readlines()

target_slugs = [
    'mobile-seo-optimization-bangladesh-mobile-first-era',
    'local-seo-dhaka-google-maps-ranking',
    'seo-knowledge-panel-bangladesh',
    'seo-canonical-url-guide-bd'
]

# Find line numbers for each slug
slug_lines = {}
for i, line in enumerate(lines, 1):
    m = re.search(r"slug:\s*\"([^\"]+)\"", line)
    if m and m.group(1) in target_slugs:
        slug_lines[m.group(1)] = i

print("Found slugs at lines:", slug_lines)

# For each slug, extract the full post object
for slug, start_line in slug_lines.items():
    # Find the object boundaries - find matching braces
    brace_count = 0
    started = False
    end_line = start_line
    
    for i in range(start_line - 1, len(lines)):
        line = lines[i]
        for ch in line:
            if ch == '{':
                brace_count += 1
                started = True
            elif ch == '}':
                brace_count -= 1
        if started and brace_count == 0:
            end_line = i + 1
            break
    
    print(f"\n{'='*80}")
    print(f"POST: {slug} (lines {start_line}-{end_line})")
    print(f"{'='*80}")
    
    # Extract fields
    post_text = ''.join(lines[start_line-1:end_line])
    
    # Get title
    t_match = re.search(r'title:\s*"([^"]+)"', post_text)
    title = t_match.group(1) if t_match else "NO TITLE"
    
    # Get tags
    tags_match = re.search(r'tags:\s*\[(.*?)\]', post_text, re.DOTALL)
    tags = []
    if tags_match:
        tags = re.findall(r'"([^"]+)"', tags_match.group(1))
    
    # Get excerpt
    e_match = re.search(r'excerpt:\s*"([^"]+)"', post_text)
    excerpt = e_match.group(1) if e_match else "NO EXCERPT"
    
    # Get content (the template literal)
    c_match = re.search(r'content:\s*`(.*)`', post_text, re.DOTALL)
    content = c_match.group(1) if c_match else ""
    
    # Get date
    d_match = re.search(r'date:\s*"([^"]+)"', post_text)
    date = d_match.group(1) if d_match else "NO DATE"
    
    print(f"Title: {title}")
    print(f"Date: {date}")
    print(f"Tags: {tags}")
    print(f"Excerpt len: {len(excerpt)}")
    print(f"Content len: {len(content)}")
    
    # --- Framework Checks ---
    
    # A. TF-IDF Coverage (primary keyword from title)
    print(f"\n--- CHECK A: TF-IDF Coverage ---")
    words = title.lower().split()
    # Find first meaningful noun phrase (skip stop words)
    stop_words = {'the', 'a', 'an', 'for', 'of', 'in', 'to', 'and', 'is', 'are', 'your', 'our', 'its', 'how', 'what', 'why', 'when', 'where'}
    keyword = ''
    for w in words:
        if w not in stop_words and len(w) > 2:
            keyword = w
            break
    if not keyword:
        keyword = words[0] if words else ''
    
    content_lower = content.lower()
    keyword_count = content_lower.count(keyword)
    print(f"Primary keyword (from title): '{keyword}'")
    print(f"Occurrences in content: {keyword_count}")
    print(f"Status: {'✅' if keyword_count >= 5 else '❌'}")
    
    # B. Semantic Entity Coverage
    print(f"\n--- CHECK B: Semantic Entity Coverage ---")
    entities = {
        'location_dhaka': 'dhaka',
        'location_bangladesh': 'bangladesh',
        'service_seo': 'seo',
    }
    # Add more specific entities based on title
    missing = []
    for e_name, e_value in entities.items():
        if content_lower.count(e_value) < 1:
            missing.append(e_value)
    
    # Check for other key entities
    if 'google' in content_lower.lower() or 'service' in content_lower.lower():
        pass  # common enough
    else:
        pass
    
    print(f"Missing entities: {missing if missing else 'None'}")
    print(f"Status: {'✅' if not missing else '❌'}")
    
    # C. Pillar-Cluster Alignment
    print(f"\n--- CHECK C: Pillar-Cluster Alignment ---")
    pillar_links = re.findall(r'/blog/[^\s"\')\]]+', content)
    service_links = re.findall(r'/services/[^\s"\')\]]+', content)
    location_links = re.findall(r'/locations/[^\s"\')\]]+', content)
    
    # Check if links to pillar page exist
    all_internal_links = pillar_links + service_links + location_links
    print(f"Internal links found: {len(all_internal_links)}")
    print(f"  Blog links: {len(pillar_links)}")
    print(f"  Service links: {len(service_links)}")
    print(f"  Location links: {len(location_links)}")
    
    # D. AEO/GEO Optimization
    print(f"\n--- CHECK D: AEO/GEO Optimization ---")
    question_headings = re.findall(r'^#{2,4}\s+(What|How|Why|When|Where|Can|Do|Is|Are|Does|Which|Who)\b', content, re.MULTILINE)
    print(f"Question-based headings ({len(question_headings)}): {question_headings}")
    print(f"Status: {'✅' if len(question_headings) >= 2 else '❌'}")
    
    # E. Internal Linking
    print(f"\n--- CHECK E: Internal Linking (detailed) ---")
    # All internal links: /something paths
    internal_links = re.findall(r'(/\w[\w/-]*)', content)
    # Filter meaningful internal links
    meaningful = [l for l in internal_links if l.startswith(('/blog/', '/services/', '/locations/', '/industries/', '/about', '/contact'))]
    print(f"Meaningful internal links: {len(meaningful)}")
    for l in meaningful:
        print(f"  - {l}")
    print(f"Status: {'✅' if len(meaningful) >= 3 else '❌'}")
    
    # F. Schema Ready
    print(f"\n--- CHECK F: Schema Ready ---")
    schema_fields = {'title': bool(title and title != "NO TITLE"), 
                     'excerpt': bool(excerpt and excerpt != "NO EXCERPT"),
                     'date': bool(date and date != "NO DATE")}
    print(f"Title set: {schema_fields['title']}")
    print(f"Excerpt set: {schema_fields['excerpt']}")
    print(f"Date set: {schema_fields['date']}")
    print(f"Status: {'✅' if all(schema_fields.values()) else '❌'}")
    
    print(f"\n{'='*80}\n")
