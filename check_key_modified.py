import re

with open('src/app/blog/data.js', 'r') as f:
    content = f.read()

def extract_post_by_slug(content, target_slug):
    lines = content.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i]
        m = re.search(r'slug: "([^"]+)"', line)
        if m and m.group(1) == target_slug:
            post_lines = [line]
            i += 1
            while i < len(lines):
                next_line = lines[i]
                if re.search(r'slug: "([^"]+)"', next_line):
                    break
                if next_line.strip() == '];':
                    break
                post_lines.append(next_line)
                i += 1
            return '\n'.join(post_lines)
        i += 1
    return None

def parse_post_metadata(post_text):
    meta = {}
    m = re.search(r'title: "([^"]*)"', post_text)
    meta['title'] = m.group(1) if m else ''
    m = re.search(r'date: "([^"]*)"', post_text)
    meta['date'] = m.group(1) if m else ''
    m = re.search(r'excerpt:\s+"([^"]*)"', post_text, re.DOTALL)
    meta['excerpt'] = m.group(1) if m else ''
    m = re.search(r'tags:\s*\[([^\]]+)\]', post_text, re.DOTALL)
    if m:
        meta['tags'] = [t.strip().strip('"') for t in m.group(1).split(',')]
    else:
        meta['tags'] = []
    m = re.search(r'content:\s*`((?:[^`]|`(?!\s*,))*)`', post_text, re.DOTALL)
    meta['content'] = m.group(1) if m else ''
    return meta

# Check key heavily-modified posts
key_slugs = [
    'why-md-kanok-miah-is-the-best-seo-expert-in-dhaka-bangladesh',
    'complete-seo-guide-bangladesh-businesses-2026',
    'local-seo-tips-dhaka-businesses-google-maps',
    'technical-seo-checklist-bangladeshi-websites',
    'how-to-choose-right-seo-agency-bangladesh',
    'geo-optimization-prepare-business-ai-search',
]

for slug in key_slugs:
    print(f"\n{'='*70}")
    print(f"## Post: {slug}")
    
    post_text = extract_post_by_slug(content, slug)
    if not post_text:
        print("  Could not extract")
        continue
    
    meta = parse_post_metadata(post_text)
    title = meta.get('title', '')
    content_text = meta.get('content', '')
    tags = meta.get('tags', [])
    content_lower = content_text.lower() if content_text else ''
    
    print(f"  Title: {title}")
    print(f"  Tags: {tags}")
    print(f"  Content: {len(content_text)} chars")
    
    # TF-IDF - extract keyword from title
    title_lower = title.lower()
    # Remove prefixes
    for prefix in ['complete ', 'ultimate ', 'definitive ', 'essential ', 'top ', 'best ', 'how to ', 'why ', 'what ', 'when ', 'where ', 'the ', 'a ']:
        if title_lower.startswith(prefix):
            title_lower = title_lower[len(prefix):]
            break
    
    words = title_lower.split()
    # Take first 2 meaningful words
    stop_words = {'guide', 'for', 'in', 'the', 'of', 'to', 'and', 'a', 'an', 'is', 'are', 'your', 'from', 'with', 'that', 'this'}
    kw_terms = [w.strip('?:.,!;') for w in words if w not in stop_words and len(w) > 2][:2]
    if kw_terms:
        keyword = ' '.join(kw_terms)
        count = content_lower.count(keyword) if keyword else 0
        # Also count individual terms
        for term in kw_terms:
            count += content_lower.count(term)
        print(f"  TF-IDF: keyword='{keyword}' → {count} occurrences {'✅' if count >= 5 else '❌'}")
    else:
        print(f"  TF-IDF: ⚠️ Could not extract keyword")
    
    # Question headings
    q_words = r'(How|What|Why|When|Where|Can|Do|Is|Are|Does|Should|Which)'
    q_pattern = re.compile(r'^#{2,3}\s+' + q_words, re.MULTILINE | re.IGNORECASE)
    q_count = len(q_pattern.findall(content_text)) if content_text else 0
    print(f"  AEO/GEO: {q_count} question headings {'✅' if q_count >= 2 else '❌'}")
    
    # Internal links
    link_pattern = re.compile(r'\[([^\]]*)\]\((/[^)]+)\)')
    links = link_pattern.findall(content_text) if content_text else []
    internal_links = [url for _, url in links if url.startswith(('/blog/', '/services/', '/industries/', '/locations/'))]
    print(f"  Internal Links: {len(internal_links)} {'✅' if len(internal_links) >= 3 else '❌'}")
    if internal_links:
        print(f"    Sample: {internal_links[:5]}")
    
    # Schema
    schema_missing = []
    if not meta.get('title'): schema_missing.append('title')
    if not meta.get('excerpt'): schema_missing.append('excerpt')
    if not meta.get('date'): schema_missing.append('date')
    if schema_missing:
        print(f"  Schema: ❌ Missing: {', '.join(schema_missing)}")
    else:
        print(f"  Schema: ✅ All fields set")

print("\n\nDone.")
