#!/usr/bin/env python3
"""Extract and analyze all 9 blog posts from data.js - v2"""
import re
import json

with open('/root/kanok-miahit/src/app/blog/data.js', 'r', encoding='utf-8') as f:
    content = f.read()

slugs = [
    "how-to-choose-best-seo-expert-dhaka-15-things",
    "seo-expert-vs-seo-agency-dhaka-which-is-right",
    "top-10-seo-mistakes-dhaka-businesses-fix",
    "what-does-seo-expert-do-guide-business-owners",
    "seo-case-study-dhaka-businesses-increased-organic-traffic",
    "hiring-seo-expert-dhaka-better-roi-than-paid-ads",
    "ai-seo-2026-dhaka-experts-optimize-google-ai-chatgpt",
    "watchzonebd-seo-case-study",
    "seo-tips-for-business-owners-bd",
]

def extract_post(content, slug):
    """Extract a full post object from data.js using its slug"""
    # Find slug line
    pattern = rf'(\s+slug: "{re.escape(slug)}")'
    match = re.search(pattern, content)
    if not match:
        return None, "Slug not found"
    
    start_pos = match.start()
    
    # Find the opening brace of this post object.
    # The structure is: either "  },\n{\n    slug:" or "  },\n\n{\n    slug:"
    # Go backwards from slug to find the opening '{'
    # Look for "{\n    slug:" pattern
    opening = content.rfind('{', 0, start_pos)
    if opening == -1:
        return None, "Opening brace not found"
    
    # Find the closing of this post.
    # Look for the next "},\n{" or "},\n\n{" that starts the next post
    # Or the end of the array "];"
    
    # Find the content end by looking for the closing backtick of the content field
    # Then the next "}," 
    # Find the content field first
    content_match = re.search(r'content:\s*`', content[opening:])
    if content_match:
        content_start_in_post = opening + content_match.end()
        # Find closing backtick
        # Need to handle escaped backticks within content
        content_end = find_closing_backtick(content, content_start_in_post)
        if content_end:
            # After content field, find the closing of the object
            after_content = content[content_end:]
            # Look for "}," or "}" or "},"
            close_match = re.search(r'\}\s*,?\s*(?:\n|$)', after_content)
            if close_match:
                post_end = content_end + close_match.end()
                post_text = content[opening:post_end]
                return post_text, None
    
    # Simpler approach: find position of next slug or end of array
    next_slug_match = re.search(r'slug:\s*"', content[start_pos + 10:])
    if next_slug_match:
        post_end = start_pos + 10 + next_slug_match.start()
        # Go back to find the closing "}," before the next slug
        # Actually, find the "}," that closes this post
        close_pos = content.rfind('},', opening, post_end)
        if close_pos != -1:
            post_text = content[opening:close_pos+2]
            return post_text, None
    
    return None, "Could not find post boundaries"

def find_closing_backtick(content, start):
    """Find closing backtick, handling escaped backticks"""
    i = start
    while i < len(content):
        if content[i] == '\\' and i + 1 < len(content):
            i += 2  # skip escaped char
        elif content[i] == '`':
            return i + 1
        else:
            i += 1
    return None

# Simpler approach: split the file by post boundaries
# Each post starts with "{\n    slug:" and ends with "}," (or "}" for last)
# Let me just find each slug and its corresponding content

def extract_post_by_content_markers(content, slug):
    """More careful extraction using the content backtick field as anchor"""
    # Find the slug
    idx = content.find(f'slug: "{slug}"')
    if idx == -1:
        return None, "Slug not found"
    
    # Go backwards past "    slug: ..." line to find the opening {
    line_start = content.rfind('\n', 0, idx) + 1
    # Check the character before the line - should be \n followed by {
    before = content[:line_start]
    brace_pos = before.rstrip().rfind('{')
    if brace_pos == -1:
        return None, "Opening brace not found"
    
    # Content starts after "content: `"
    content_kw_idx = content.find('content: `', brace_pos)
    if content_kw_idx == -1:
        return None, "content: field not found"
    
    content_start = content_kw_idx + len('content: `')
    
    # Find closing backtick of content
    content_end = find_closing_backtick(content, content_start)
    if not content_end:
        return None, "Closing backtick not found"
    
    # After content backtick, find the closing }, or },
    after_content = content[content_end:]
    # Look for "}," or "}" at end
    close_match = re.search(r'\}\s*,?\s*(\n|$)', after_content)
    if not close_match:
        return None, "Closing brace not found"
    
    post_end = content_end + close_match.end()
    post_text = content[brace_pos:post_end]
    
    return post_text, None

# Even simpler approach: use approximate range-based extraction
def extract_by_line_range(content, slug, known_line):
    """Extract post text by line number with reasonable bounds"""
    lines = content.split('\n')
    # Find the slug line
    for i, line in enumerate(lines, 1):
        if f'slug: "{slug}"' in line:
            # Post starts at the { before this line
            # Find the { - it should be on a line by itself before the slug
            post_start = i - 2  # usually 1-2 lines before slug
            # Look backwards to find {
            for j in range(i-2, max(0, i-5), -1):
                if lines[j-1].strip() == '{' or lines[j-1].strip() == '{,':
                    post_start = j
                    break
            
            # Post ends at the }, before the next slug or end of array
            post_end = len(lines)
            for j in range(i, min(len(lines), i + 1000)):
                line_stripped = lines[j-1].strip()
                if line_stripped.startswith('slug:') and j != i:
                    post_end = j - 1
                    break
            
            return '\n'.join(lines[post_start-1:post_end])
    
    return None

# Let me try yet another approach - use the full file and regex
# to find each complete post object

def extract_all_posts_robust(content):
    """Extract all posts using the known pattern: each post starts with { on its own line then slug:"""
    # Split the content to find posts
    # Find all slug positions
    posts = {}
    
    # Strategy: find "slug: \"xxx\"" patterns. 
    # For each slug, find its post boundaries
    slug_pattern = re.compile(r'slug:\s*"([^"]+)"')
    
    # Find all matches with positions
    all_slugs = list(slug_pattern.finditer(content))
    
    for i, m in enumerate(all_slugs):
        slug = m.group(1)
        if slug not in slugs:
            continue
        
        slug_pos = m.start()
        
        # Find the opening { by looking backwards
        # The { should be on a line before the slug: line
        line_before = content.rfind('\n', 0, slug_pos)
        if line_before == -1:
            line_before = 0
        before_line_start = content.rfind('\n', 0, line_before - 1) + 1 if line_before > 0 else 0
        before_line = content[before_line_start:line_before].strip()
        
        # The { could be on the line immediately before slug, or there could be a blank line
        search_start = max(0, slug_pos - 20)
        brace_pos = content.rfind('{', search_start, slug_pos)
        if brace_pos == -1:
            brace_pos = content.rfind('{', max(0, slug_pos - 50), slug_pos)
        
        # Find the end: look at the next slug position
        if i + 1 < len(all_slugs):
            next_slug_pos = all_slugs[i + 1].start()
            
            # Go back from next slug to find this post's closing
            # Look for "}," pattern between our content end and next slug
            search_region = content[slug_pos:next_slug_pos]
            
            # Find the content field and its closing backtick
            content_field_match = re.search(r'content:\s*`', content[brace_pos:])
            if content_field_match:
                c_start = brace_pos + content_field_match.end()
                c_end = find_closing_backtick(content, c_start)
                if c_end:
                    # After this, find "}," or "}"
                    after = content[c_end:]
                    close_brace = re.search(r'\}\s*,?', after)
                    if close_brace:
                        post_end = c_end + close_brace.end()
                        post_text = content[brace_pos:post_end]
                        posts[slug] = post_text
                        continue
        
        # Fallback: use line-based approach
        lines = content.split('\n')
        slug_line_idx = None
        for li, l in enumerate(lines):
            if f'slug: "{slug}"' in l:
                slug_line_idx = li
                break
        
        if slug_line_idx is not None:
            # Find opening {
            post_start_line = slug_line_idx - 1
            for li in range(slug_line_idx - 1, max(0, slug_line_idx - 4), -1):
                if lines[li].strip() == '{':
                    post_start_line = li
                    break
            
            # Find closing }, or }
            post_end_line = len(lines) - 1
            for li in range(slug_line_idx + 1, min(len(lines), slug_line_idx + 500)):
                ls = lines[li].strip()
                if ls.startswith('slug:') and li != slug_line_idx:
                    # The previous line with "}," or "}" is the end
                    for pi in range(li - 1, slug_line_idx, -1):
                        if lines[pi].strip() in ['},', '}']:
                            post_end_line = pi
                            break
                    break
            
            posts[slug] = '\n'.join(lines[post_start_line:post_end_line+1])
    
    return posts

posts = extract_all_posts_robust(content)

for slug in slugs:
    print(f"\n{'='*70}")
    print(f"=== POST: {slug} ===")
    
    if slug not in posts:
        print(f"ERROR: Could not extract post")
        continue
    
    post_text = posts[slug]
    
    # Extract fields
    title_match = re.search(r'title:\s*"((?:[^"\\]|\\.)*)"', post_text)
    title = title_match.group(1) if title_match else "NOT FOUND"
    
    date_match = re.search(r'date:\s*"([^"]+)"', post_text)
    date = date_match.group(1) if date_match else "NOT FOUND"
    
    author_match = re.search(r'author:\s*"((?:[^"\\]|\\.)*)"', post_text)
    author = author_match.group(1) if author_match else "NOT FOUND"
    
    excerpt_match = re.search(r'excerpt:\s*"((?:[^"\\]|\\.)*)"', post_text)
    excerpt = excerpt_match.group(1) if excerpt_match else None
    
    metaTitle_match = re.search(r'metaTitle:\s*"((?:[^"\\]|\\.)*)"', post_text)
    metaTitle = metaTitle_match.group(1) if metaTitle_match else None
    
    metaDesc_match = re.search(r'metaDescription:\s*"((?:[^"\\]|\\.)*)"', post_text)
    metaDesc = metaDesc_match.group(1) if metaDesc_match else None
    
    imagePlaceholder_match = re.search(r'imagePlaceholder:\s*"([^"]*)"', post_text)
    imagePlaceholder = imagePlaceholder_match.group(1) if imagePlaceholder_match else None
    
    # Tags
    tags_match = re.search(r'tags:\s*\[([^\]]+)\]', post_text)
    tags = []
    if tags_match:
        tags_str = tags_match.group(1)
        tags = re.findall(r'"((?:[^"\\]|\\.)*)"', tags_str)
    
    # Content
    content_match = re.search(r'content:\s*`', post_text)
    post_content = ""
    if content_match:
        c_start = content_match.end()
        c_end = find_closing_backtick(post_text, c_start)
        if c_end:
            post_content = post_text[c_start:c_end-1]  # -1 to remove closing backtick
    
    is_bengali = slug == "seo-tips-for-business-owners-bd"
    
    print(f"Title: {title}")
    print(f"Date: {date}")
    print(f"Author: {author}")
    print(f"Tags: {tags}")
    print(f"Content length: {len(post_content)} chars")
    print(f"Excerpt: {excerpt[:60] if excerpt else 'MISSING'}...")
    print(f"metaTitle: {'SET' if metaTitle else 'MISSING'}")
    print(f"metaDesc: {'SET' if metaDesc else 'MISSING'}")
    
    # ---- A. TF-IDF Coverage ----
    if is_bengali:
        keyword = "SEO"
    else:
        # Extract primary keyword from title
        # Remove common prefixes
        title_clean = title
        for prefix in ['How to ', 'Top \\d+ ', 'What ', 'Why ', 'AI ', 'Complete ']:
            title_clean = re.sub(r'^' + prefix, '', title_clean, flags=re.IGNORECASE)
        
        # Get first meaningful noun phrase (up to colon, dash, or first few words)
        kw = title.split(':')[0].strip()
        # Remove leading question words etc
        kw = re.sub(r'^(How to |Top \d+ |What |Why |AI |Complete )', '', kw, flags=re.IGNORECASE).strip()
        
        # For SEO posts, just use "SEO Expert" or "SEO" as keyword depending on post
        if 'SEO Expert' in title or 'SEO expert' in title:
            keyword = 'SEO Expert'
        elif 'SEO Agency' in title:
            keyword = 'SEO Agency'
        elif 'SEO Mistakes' in title:
            keyword = 'SEO Mistakes'
        elif 'SEO Case Study' in title:
            keyword = 'SEO Case Study'
        elif 'SEO ROI' in title or 'ROI' in title:
            keyword = 'SEO ROI'
        elif 'AI SEO' in title:
            keyword = 'AI SEO'
        else:
            keyword = kw if kw else 'SEO'
    
    kw_count = len(re.findall(re.escape(keyword), post_content, re.IGNORECASE)) if keyword else 0
    
    # ---- B. Entities ----
    entities = {}
    if is_bengali:
        entities['Dhaka/Bangladesh'] = bool(re.search(r'ঢাকা|বাংলাদেশ|বাংলা', post_content))
        entities['Service Type'] = bool(re.search(r'SEO|সিওও', post_content, re.IGNORECASE))
        entities['Industry'] = bool(re.search(r'ব্যবসা|দোকান|অনলাইন', post_content))
    else:
        entities['Dhaka/Bangladesh'] = bool(re.search(r'Dhaka|Bangladesh|Bangladeshi', post_content))
        entities['Service Type'] = bool(re.search(r'SEO|search engine optimization|digital marketing', post_content, re.IGNORECASE))
        entities['Industry'] = bool(re.search(r'business|e-commerce|restaurant|garment|healthcare|real estate|agency|automotive', post_content, re.IGNORECASE))
    
    # ---- C. Pillar Link ----
    # Look for links to homepage (/) or service pages or blog index
    pillar_link_patterns = [
        (r'href="/"', 'Homepage'),
        (r'href="/services', 'Services page'),
        (r'href="/blog"', 'Blog index'),
        (r'href="https?://[^/]*kanokmiah[^"]*\.bd/?[\"#]', 'Homepage (absolute)'),
        (r'href="https?://[^/]*kanokmiah[^"]*\.com\.bd/?[\"#]', 'Homepage (absolute .com.bd)'),
    ]
    pillar_found = []
    for pattern, desc in pillar_link_patterns:
        if re.search(pattern, post_content, re.IGNORECASE):
            pillar_found.append(desc)
    
    # Check for ["Kanok Miah"](/)
    if re.search(r'\[Kanok Miah\]\(/\)', post_content):
        pillar_found.append('[Kanok Miah](/homepage)')
    
    # ---- D. AEO/GEO Question Headings ----
    if is_bengali:
        q_patterns = [
            r'##+\s*কীভাবে',
            r'##+\s*কী\b',
            r'##+\s*কেন\b',
            r'##+\s*কখন\b',
            r'##+\s*কোথায়',
            r'##+\s*কোথায়',
        ]
    else:
        q_patterns = [
            r'##+\s*How\s',
            r'##+\s*What\s',
            r'##+\s*Why\s',
            r'##+\s*When\s',
            r'##+\s*Where\s',
            r'##+\s*Can\s',
            r'##+\s*Do\s',
            r'##+\s*Does\s',
            r'##+\s*Is\s',
            r'##+\s*Are\s',
            r'##+\s*Should\s',
            r'##+\s*Which\s',
        ]
    q_count = 0
    q_headings_list = []
    for p in q_patterns:
        matches = re.findall(p, post_content, re.IGNORECASE)
        q_count += len(matches)
        for m in matches:
            q_headings_list.append(m.strip())
    
    # ---- E. Internal Links ----
    internal_patterns = [
        r'href="(/blog/[^"]+)"',
        r'href="(/services/[^"]+)"',
        r'href="(/locations/[^"]+)"',
        r'\]\((/blog/[^)]+)\)',
        r'\]\((/services/[^)]+)\)',
        r'\]\((/locations/[^)]+)\)',
    ]
    internal_links_set = set()
    for p in internal_patterns:
        for m in re.finditer(p, post_content):
            internal_links_set.add(m.group(1))
    
    # ---- F. Schema ----
    schema_all = {
        'title': title_match is not None and title != "NOT FOUND",
        'excerpt': excerpt is not None,
        'date': date_match is not None and date != "NOT FOUND",
        'author': author_match is not None and author != "NOT FOUND",
        'imagePlaceholder': imagePlaceholder is not None,
    }
    schema_optional = {
        'metaTitle': metaTitle is not None,
        'metaDescription': metaDesc is not None,
    }
    
    # ---- PRINT REPORT ----
    print(f"\n=== REPORT ===")
    print(f"A. TF-IDF: keyword='{keyword}', count={kw_count} {'✅' if kw_count >= 5 else '❌'}")
    
    missing_entities = [k for k, v in entities.items() if not v]
    print(f"B. Entities: {'✅' if all(entities.values()) else '❌'} Missing: {missing_entities if missing_entities else 'None'}")
    
    print(f"C. Pillar Link: {'✅' if pillar_found else '❌'} Links to: {pillar_found if pillar_found else 'None found'}")
    
    print(f"D. AEO/GEO: {'✅' if q_count >= 2 else '❌'} {q_count} question headings: {q_headings_list[:10]}")
    
    print(f"E. Internal Links: {'✅' if len(internal_links_set) >= 3 else '❌'} {len(internal_links_set)} total: {sorted(internal_links_set)}")
    
    all_schema = {**schema_all, **schema_optional}
    schema_ok = all(all_schema.values())
    print(f"F. Schema Ready: {'✅' if schema_ok else '❌'} Fields: {json.dumps(all_schema, indent=2)}")
    if not schema_ok:
        missing_schema = [k for k, v in all_schema.items() if not v]
        print(f"   Missing schema fields: {missing_schema}")
    
    # Content preview
    print(f"\nContent preview: {post_content[:80]}...")
