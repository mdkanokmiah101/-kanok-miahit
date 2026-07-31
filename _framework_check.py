#!/usr/bin/env python3
"""Framework compliance checker for modified blog posts."""
import re, json, sys

# Read data.js
with open("src/app/blog/data.js", "r", encoding="utf-8") as f:
    content = f.read()

# Extract all posts
posts_raw = re.findall(r'slug:\s*"([^"]+)"[\s\S]*?content:\s*`([\s\S]*?)`,?\n\s*[},]', content)

# Build dict
posts = {}
current_slug = None
current_start = 0

# Simpler approach: find posts by slug and content
lines = content.split('\n')
posts_dict = {}

i = 0
while i < len(lines):
    line = lines[i]
    slug_match = re.search(r'slug:\s*"([^"]+)"', line)
    if slug_match:
        slug = slug_match.group(1)
        # Collect post data
        post_data = {'slug': slug, 'lines_start': i}
        j = i
        while j < min(i + 100, len(lines)):
            sub = lines[j]
            if sub.startswith('    title:') or sub.startswith('    title:'):
                post_data['title'] = sub.split('title:')[1].strip().strip('",').strip('`')
            elif sub.startswith('    date:') and 'dateModified' not in sub:
                post_data['date'] = sub.split('date:')[1].strip().strip('",')
            elif sub.startswith('    excerpt:'):
                # Could be multi-line
                excerpt_lines = []
                k = j
                while k < min(j + 20, len(lines)):
                    el = lines[k]
                    if el.strip().startswith('tags:') or el.strip().startswith('imagePlaceholder'):
                        break
                    excerpt_lines.append(el)
                    k += 1
                post_data['excerpt'] = ' '.join(excerpt_lines)
            elif sub.startswith('    tags:'):
                tags_match = re.search(r'tags:\s*\[([^\]]+)\]', sub)
                if tags_match:
                    post_data['tags'] = [t.strip().strip('"') for t in tags_match.group(1).split(',')]
            elif sub.startswith('    metaTitle:'):
                post_data['metaTitle'] = True
            elif sub.startswith('    metaDescription:'):
                post_data['metaDescription'] = True
            elif sub.startswith('    dateModified:'):
                post_data['dateModified'] = True
            elif 'content: `' in sub or sub.strip().startswith('content:'):
                # Content starts
                content_lines = []
                k = j
                in_content = True
                # Find the backtick
                bt_match = re.search(r'content:\s*`', sub)
                if bt_match:
                    # Content may start on same line after backtick
                    after_bt = sub[bt_match.end():]
                    if after_bt.strip():
                        content_lines.append(after_bt)
                    k += 1
                    while k < len(lines):
                        if lines[k].strip().endswith('`,'):
                            content_lines.append(lines[k].strip()[:-2])
                            break
                        content_lines.append(lines[k])
                        k += 1
                    post_data['content'] = '\n'.join(content_lines)
                break
            j += 1
        posts_dict[slug] = post_data
    i += 1

# Check specific posts
target_slugs = [
    "mobile-seo-optimization-bangladesh-mobile-first-era",
    "how-to-choose-best-seo-expert-dhaka-15-things",
    "schema-markup-rich-snippets-techniques",
    "seo-canonical-url-guide-bd"
]

# Also extract using a different method - search for slug and grab surrounding lines
def extract_post_by_slug(slug):
    """Extract a post by slug from the data.js file."""
    # Find the slug line
    for i, line in enumerate(lines):
        if f'slug: "{slug}"' in line:
            start = i
            # Go back to find the opening {
            while start > 0 and not lines[start].strip() == '{':
                start -= 1
            # Find the closing },  (post end)
            brace_count = 0
            end = start
            for j in range(start, min(start + 1000, len(lines))):
                if '{' in lines[j]:
                    brace_count += lines[j].count('{')
                if '}' in lines[j]:
                    brace_count -= lines[j].count('}')
                if brace_count == 0 and j > start:
                    end = j
                    break
            
            block = '\n'.join(lines[start:end+1])
            
            # Extract fields
            result = {'slug': slug}
            
            title_m = re.search(r'title:\s*"([^"]*)"', block)
            if title_m: result['title'] = title_m.group(1)
            
            date_m = re.search(r'date:\s*"([^"]*)"', block)
            if date_m: result['date'] = date_m.group(1)
            
            excerpt_m = re.search(r'excerpt:\s*\n?\s*"([^"]*)"', block, re.DOTALL)
            if not excerpt_m:
                excerpt_m = re.search(r'excerpt:\s*"([^"]*)"', block)
            if excerpt_m: result['excerpt'] = excerpt_m.group(1).strip()
            
            tags_m = re.search(r'tags:\s*\[([^\]]+)\]', block)
            if tags_m: result['tags'] = [t.strip().strip('"') for t in tags_m.group(1).split(',')]
            
            result['has_metaTitle'] = bool(re.search(r'metaTitle:', block))
            result['has_metaDescription'] = bool(re.search(r'metaDescription:', block))
            result['has_dateModified'] = bool(re.search(r'dateModified:', block))
            
            # Extract content
            content_m = re.search(r'content:\s*`([\s\S]*?)`,?\n', block)
            if content_m:
                result['content'] = content_m.group(1)
            else:
                # Try multi-line content
                content_m2 = re.search(r'content:\s*`([\s\S]*?)\`,\s*\n', block)
                if content_m2:
                    result['content'] = content_m2.group(1)
            
            return result
    return None

for slug in target_slugs:
    post = extract_post_by_slug(slug)
    if not post:
        print(f"Could not find post: {slug}", file=sys.stderr)
        continue

    print(f"\n{'='*60}")
    print(f"## Post: {slug}")
    print(f"Title: {post.get('title', 'N/A')}")
    print(f"{'='*60}")
    
    content = post.get('content', '')
    title = post.get('title', '')
    tags = post.get('tags', [])
    excerpt = post.get('excerpt', '')
    
    # A. TF-IDF Coverage
    # Extract primary keyword from title (first meaningful noun phrase)
    # For English titles, take first significant word
    title_lower = title.lower()
    stop_words = {'the', 'a', 'an', 'for', 'in', 'of', 'to', 'and', 'or', 'is', 'are', 'how', 'what', 'why', 'when', 'where', 'your', 'our', 'their', 'its', 'that', 'this'}
    words = [w for w in re.findall(r'\b[a-zA-Z]+\b', title_lower) if w not in stop_words]
    
    # For Bengali titles, use first meaningful phrase
    if any(ord(c) > 0x0980 for c in title):
        # Bengali title
        keyword = title[:30]  # First ~30 chars
        keyword_count = content.count(keyword[:20]) if keyword else 0
    else:
        keyword = words[0] if words else title.split()[0] if title.split() else ''
        keyword_count = len(re.findall(r'\b' + re.escape(keyword) + r'\b', content.lower())) if keyword else 0
    
    # Also check bigram
    if len(words) >= 2:
        bigram = words[0] + ' ' + words[1]
        bigram_count = len(re.findall(re.escape(bigram), content.lower()))
        total_kw_count = keyword_count + bigram_count
    else:
        total_kw_count = keyword_count
    
    print(f"\n### A. TF-IDF Coverage")
    print(f"Primary keyword: '{keyword}'")
    print(f"Occurrences: {total_kw_count}")
    if total_kw_count < 5:
        print(f"Status: ❌ (too thin, {total_kw_count} < 5)")
    else:
        print(f"Status: ✅ ({total_kw_count} occurrences)")
    
    # B. Semantic Entity Coverage
    print(f"\n### B. Semantic Entity Coverage")
    entities_to_check = {
        'location_dhaka': ['dhaka', 'ঢাকা'],
        'location_bangladesh': ['bangladesh', 'বাংলাদেশ'],
        'location_chittagong': ['chittagong', 'চট্টগ্রাম'],
        'kanok_miah': ['kanok miah', 'কনক মিঞা', 'মোঃ কনক মিঞা'],
    }
    
    # Add service type based on tags
    service_keywords = {
        'seo': ['seo', 'এসইও'],
        'mobile': ['mobile', 'মোবাইল'],
        'local_seo': ['local seo', 'লোকাল এসইও'],
        'technical_seo': ['technical seo', 'টেকনিকেল এসইও'],
    }
    
    content_lower = content.lower()
    missing_entities = []
    
    for entity, variants in entities_to_check.items():
        found = False
        for v in variants:
            if v.lower() in content_lower:
                found = True
                break
        if not found:
            missing_entities.append(entity)
    
    for entity, variants in service_keywords.items():
        if entity in ' '.join(tags).lower():
            found = False
            for v in variants:
                if v.lower() in content_lower:
                    found = True
                    break
            if not found:
                missing_entities.append(f"service/{entity}")
    
    if missing_entities:
        print(f"Status: ❌ Missing: {', '.join(missing_entities)}")
    else:
        print(f"Status: ✅ All key entities present")
    
    # C. Pillar-Cluster Alignment
    print(f"\n### C. Pillar-Cluster Alignment")
    pillar_map = {
        'mobile seo': '/blog/mobile-seo-bangladesh-ranking-strategy',
        'seo expert': ['/', '/about'],
        'schema': '/blog/complete-seo-guide-bangladesh-businesses-2026',
        'canonical': '/blog/complete-seo-guide-bangladesh-businesses-2026',
        'technical seo': '/services/technical-seo',
        'seo bangladesh': '/blog/complete-seo-guide-bangladesh-businesses-2026',
    }
    
    # Determine pillar based on tags and title
    tags_lower = [t.lower() for t in tags]
    content_lower = content.lower()
    pillar_found = None
    
    # Check for links to pillar pages
    pillar_pages = [
        '/blog/complete-seo-guide-bangladesh-businesses-2026',
        '/blog/mobile-seo-bangladesh-ranking-strategy', 
        '/services/technical-seo',
        '/services/local-seo',
        '/services/on-page-seo',
        '/services/ecommerce-seo',
        '/',
        '/about',
    ]
    
    links_to_pillar = [p for p in pillar_pages if p.lower() in content_lower]
    
    if links_to_pillar:
        print(f"Status: ✅ Links to pillar: {links_to_pillar[0]}")
    else:
        print(f"Status: ❌ No pillar link found")
    
    # D. AEO/GEO Optimization
    print(f"\n### D. AEO/GEO Optimization")
    question_heading_pattern = re.compile(r'^#{2,3}\s+(How|What|Why|When|Where|Can|Do|Is|Are|Does|Which|Who)\b', re.MULTILINE | re.IGNORECASE)
    question_headings = question_heading_pattern.findall(content)
    heading_count = len(question_headings)
    
    print(f"Question-based headings: {heading_count}")
    if heading_count < 2:
        print(f"Status: ❌ (< 2 question headings)")
    else:
        print(f"Status: ✅ ({heading_count} question headings)")
    
    # E. Internal Linking
    print(f"\n### E. Internal Linking")
    internal_links = re.findall(r'\[([^\]]+)\]\((/[^)]+)\)', content)
    external_links = re.findall(r'\[([^\]]+)\]\((https?://[^)]+)\)', content)
    
    # Filter out anchor-only links
    internal_links = [l for l in internal_links if not l[1].startswith('#')]
    
    print(f"Internal links: {len(internal_links)}")
    for link_text, link_url in internal_links[:10]:
        print(f"  - [{link_text}]({link_url})")
    if len(internal_links) > 10:
        print(f"  ... and {len(internal_links) - 10} more")
    
    if len(internal_links) < 3:
        print(f"Status: ❌ (< 3 internal links)")
    else:
        print(f"Status: ✅ ({len(internal_links)} internal links)")
    
    # F. Schema Ready
    print(f"\n### F. Schema Ready")
    schema_fields = {
        'metaTitle': post.get('has_metaTitle', False),
        'metaDescription': post.get('has_metaDescription', False),
        'date': bool(post.get('date')),
        'excerpt': bool(post.get('excerpt')),
    }
    
    missing_schema = [k for k, v in schema_fields.items() if not v]
    if missing_schema:
        print(f"Status: ❌ Missing: {', '.join(missing_schema)}")
    else:
        print(f"Status: ✅ All fields set")

print("\n\n=== FRAMEWORK CHECKS COMPLETE ===")
