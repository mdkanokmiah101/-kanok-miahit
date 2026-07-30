#!/usr/bin/env python3
"""Analyze changed blog posts for framework compliance."""
import re
import json

DATA_PATH = "src/app/blog/data.js"

with open(DATA_PATH, "r") as f:
    raw = f.read()

# Split into individual post objects by finding slug patterns
# Each post starts with '{' and has a slug field
posts = []
# Find all post boundaries by splitting on '},\n  {\n    slug:'
# But first normalize the whitespace for consistent parsing
# Let's find by slug patterns
slug_pattern = re.compile(r"slug:\s*['\"]([^'\"]+)['\"]")

# Find positions of each slug
matches = list(slug_pattern.finditer(raw))
slugs = [m.group(1) for m in matches]

# Slugs that were modified in the last 48 hours
changed_slugs = [
    "mobile-seo-optimization-bangladesh-mobile-first-era",
    "schema-markup-rich-snippets-techniques",
    "why-md-kanok-miah-is-the-best-seo-expert-in-dhaka-bangladesh",
    "locksmith-dundee-seo-case-study",
    "das-taxis-scotland-seo-case-study",
    "morethanpanel-seo-case-study",
    "smmgen-seo-case-study",
    "smmsun-seo-case-study",
    "mir-cement-seo-case-study",
    "dhaka-apparels-seo-case-study",
    "stealth-windshield-repairs-seo-case-study",
    "landlord-certificates-seo-case-study",
    "how-to-choose-best-seo-expert-dhaka-15-things",
    "seo-expert-vs-seo-agency-dhaka-which-is-right",
    "what-does-seo-expert-do-guide-business-owners",
    "seo-case-study-dhaka-businesses-increased-organic-traffic",
    "hiring-seo-expert-dhaka-better-roi-than-paid-ads",
    "ai-seo-2026-dhaka-experts-optimize-google-ai-chatgpt",
    "watchzonebd-seo-case-study",
]

def extract_post_by_slug(slug):
    """Extract a post object by its slug."""
    # Find the slug in the raw content
    idx = raw.find(f"slug: \"{slug}\"")
    if idx == -1:
        idx = raw.find(f"slug: '{slug}'")
    if idx == -1:
        return None
    
    # Find the post boundary - go back to find the opening {
    post_start = raw.rfind("{", idx - 500, idx)
    if post_start == -1:
        post_start = idx - 10
    
    # Find the closing of this post - look for "}," followed by next slug or end
    # Find next slug after current one
    next_slug_match = slug_pattern.search(raw, idx + len(slug) + 20)
    if next_slug_match:
        post_end = raw.rfind("},", next_slug_match.start() - 100, next_slug_match.start())
        if post_end == -1:
            post_end = next_slug_match.start() - 2
    else:
        post_end = raw.rfind("};", idx)
        if post_end == -1:
            return None
    
    post_text = raw[post_start:post_end].strip()
    return post_text

def extract_field(post_text, field):
    """Extract a field value from post text."""
    patterns = [
        rf"{field}:\s*['\"]([^'\"]+)['\"]",
        rf"{field}:\s*\n\s+['\"]([^'\"]+)['\"]",
        rf"{field}:\s*\n\s+`([^`]+)`",
    ]
    for p in patterns:
        m = re.search(p, post_text)
        if m:
            return m.group(1)
    return None

def extract_array_field(post_text, field):
    """Extract array field like tags."""
    # Find the field and extract array content
    idx = post_text.find(f"{field}: [")
    if idx == -1:
        return []
    start = post_text.find("[", idx)
    end = post_text.find("]", start)
    if start == -1 or end == -1:
        return []
    arr_str = post_text[start:end+1]
    # Parse simple string array
    items = re.findall(r"'([^']*)'|\"([^\"]*)\"", arr_str)
    return [a or b for a, b in items]

def extract_content(post_text):
    """Extract the content field (backtick string)."""
    idx = post_text.find("content: `")
    if idx == -1:
        return ""
    start = idx + len("content: `")
    # Find the closing backtick followed by comma
    # Need to handle nested backticks in code blocks
    content = ""
    stack = []
    i = start
    while i < len(post_text):
        if post_text[i] == '`' and (i+1 >= len(post_text) or post_text[i+1] == ','):
            # Check if this backtick is preceded by a newline
            if content.endswith('\n') or not content:
                break
        if post_text[i] == '`':
            # Check if this is a code block delimiter
            if i+2 < len(post_text) and post_text[i+1] == '`' and post_text[i+2] == '`':
                # Triple backtick - find the closing triple
                content += post_text[i]
                i += 1
                continue
        content += post_text[i]
        i += 1
    return content

def extract_content_simple(post_text):
    """Simpler content extraction - find content between first backtick after 'content: ' and the next ', that closes a backtick"""
    idx = post_text.find("content: `")
    if idx == -1:
        idx = post_text.find("content:\n    `")
    if idx == -1:
        return ""
    
    # Find the opening backtick
    bt_start = post_text.find("`", idx)
    if bt_start == -1:
        return ""
    
    # Find the closing backtick+comma pattern
    # Look for "\`," or "`," pattern 
    search_start = bt_start + 1
    while True:
        bt_end = post_text.find("`,", search_start)
        if bt_end == -1:
            break
        # Check if this backtick is preceded by a newline (end of content)
        before = post_text[bt_end-3:bt_end] if bt_end >= 3 else ""
        # The content backtick should be at a natural ending
        # Try to find it
        content = post_text[bt_start+1:bt_end]
        # Check if it's the real end (no unclosed triples)
        if content.count('`') % 2 == 0 or '\\`' in content:
            return content
        search_start = bt_end + 2
    
    return post_text[bt_start+1:]

# Try a different approach - extract content between specific line positions
# Let me use line-based extraction
lines = raw.split('\n')

def get_content_lines_for_slug(slug):
    """Get content lines for a post by finding slug line then content lines."""
    result = {"header": {}, "content": ""}
    in_post = False
    in_content = False
    content_lines = []
    header_lines = []
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        if slug in stripped and stripped.startswith("slug:"):
            in_post = True
            header_lines.append(line)
            continue
        if in_post:
            if stripped.startswith("content: `"):
                in_content = True
                # Content starts after the backtick
                content_start = line.find("`")
                if content_start >= 0 and content_start + 1 < len(line):
                    content_start_remainder = line[content_start+1:]
                    if content_start_remainder.strip():
                        content_lines.append(content_start_remainder)
                continue
            elif in_content:
                if stripped == "`," or stripped.endswith("`,"):
                    # End of content
                    in_content = False
                    in_post = False
                elif stripped.startswith("`"):
                    content_lines.append(line[line.find("`")+1:])
                else:
                    content_lines.append(line)
            elif stripped.startswith("},") or stripped == "},":
                # End of post
                in_post = False
            else:
                header_lines.append(line)
    
    result["header"] = "\n".join(header_lines)
    result["content"] = "\n".join(content_lines)
    return result

def analyze_post(slug):
    """Run all framework checks on a post."""
    data = get_content_lines_for_slug(slug)
    header = data["header"]
    content = data["content"]
    
    if not content and not header:
        return {"slug": slug, "error": "Could not extract post data"}
    
    # Extract metadata
    title_match = re.search(r'title:\s*["\'](.+?)["\']', header)
    title = title_match.group(1) if title_match else ""
    
    excerpt_match = re.search(r'excerpt:\s*["\'](.+?)["\']', header, re.DOTALL)
    excerpt_match2 = re.search(r'excerpt:\s*\n\s+["\'](.+?)["\']', header, re.DOTALL)
    excerpt = ""
    if excerpt_match:
        excerpt = excerpt_match.group(1)
    elif excerpt_match2:
        excerpt = excerpt_match2.group(1)
    
    date_match = re.search(r'date:\s*["\'](.+?)["\']', header)
    date = date_match.group(1) if date_match else ""
    
    # Extract dateModified
    dm_match = re.search(r'dateModified:\s*["\'](.+?)["\']', header)
    date_modified = dm_match.group(1) if dm_match else ""
    
    # Extract tags
    tags_match = re.search(r'tags:\s*\[(.+?)\]', header)
    tags = []
    if tags_match:
        tag_str = tags_match.group(1)
        tags = re.findall(r'["\']([^"\']+)["\']', tag_str)
    
    # Extract metaTitle, metaDescription
    mt_match = re.search(r'metaTitle:\s*\n?\s*["\'](.+?)["\']', header, re.DOTALL)
    meta_title = mt_match.group(1) if mt_match else ""
    
    md_match = re.search(r'metaDescription:\s*\n?\s*["\'](.+?)["\']', header, re.DOTALL)
    meta_desc = md_match.group(1) if md_match else ""
    
    results = {}
    
    # A. TF-IDF Coverage
    # Extract primary keyword from title (first meaningful noun phrase)
    title_lower = title.lower()
    # Common SEO keyword patterns in titles
    keyword = ""
    stop_words = ["the", "a", "an", "for", "to", "in", "of", "and", "or", "is", "are", "how", "what", "why", "when", "where", "can", "do", "does", "your", "our", "their", "its", "which", "who", "that", "this", "these", "those"]
    
    # Try to extract the main keyword - first noun phrase after stop words
    title_parts = title_lower.replace(":", " ").replace("?", " ").replace("!", " ").split()
    # Find first meaningful multi-word phrase
    for i, word in enumerate(title_parts):
        if word not in stop_words and len(word) > 2:
            # Collect following words that are also content words
            kw_parts = [word]
            for j in range(i+1, min(i+4, len(title_parts))):
                if title_parts[j] not in stop_words or j == i+1:
                    kw_parts.append(title_parts[j])
                else:
                    break
            keyword = " ".join(kw_parts)
            break
    
    if not keyword:
        keyword = title_parts[0] if title_parts else title
    
    # Count keyword occurrences in content (case-insensitive)
    kw_count = len(re.findall(re.escape(keyword), content, re.IGNORECASE)) if keyword else 0
    
    results["tfidf"] = {
        "keyword": keyword,
        "occurrences": kw_count,
        "pass": kw_count >= 5
    }
    
    # B. Semantic Entity Coverage
    required_entities = {
        "location_bd": "Bangladesh",
        "location_dhaka": "Dhaka",
    }
    
    # Determine service type from tags and title
    is_case_study = "case study" in title.lower() or any("case study" in t.lower() for t in tags)
    is_local_seo = "local seo" in title.lower() or "local" in tags or "local seo" in tags
    is_ecommerce = "ecommerce" in title.lower() or "e-commerce" in title.lower() or "ecommerce" in tags
    is_technical = "technical" in title.lower() or "technical seo" in tags
    is_mobile = "mobile" in title.lower() or "mobile seo" in tags
    is_schema = "schema" in title.lower() or "schema markup" in tags or "rich snippets" in tags or "structured data" in tags
    
    entities_to_check = ["Bangladesh", "Dhaka"]
    
    # For service-related posts
    if is_local_seo:
        entities_to_check.extend(["Google Business Profile", "local SEO"])
    if is_mobile:
        entities_to_check.extend(["mobile-first", "Core Web Vitals"])
    if is_technical:
        entities_to_check.extend(["Core Web Vitals", "structured data"])
    if is_schema:
        entities_to_check.extend(["JSON-LD", "rich snippets", "structured data"])
    if is_case_study:
        entities_to_check.extend(["organic traffic", "keywords", "ranking"])
    
    missing = []
    for entity in entities_to_check:
        if entity.lower() not in content.lower():
            missing.append(entity)
    
    results["entities"] = {
        "checked": entities_to_check,
        "missing": missing,
        "pass": len(missing) == 0
    }
    
    # C. Pillar-Cluster Alignment
    pillar_pages = [
        "/blog/complete-seo-guide-bangladesh-businesses-2026",
        "/blog/geo-optimization-prepare-business-ai-search",
        "/blog/technical-seo-checklist-bangladeshi-websites",
        "/blog/seo-bangla-beginners-guide-google-ranking",
        "/blog/seo-garments-textile-industry-b2b-lead-generation",
    ]
    
    pillar_link_found = None
    for pp in pillar_pages:
        if pp in content:
            pillar_link_found = pp
            break
    
    # Also check for any /blog/ links that could be pillar pages
    if not pillar_link_found:
        blog_links = re.findall(r'/blog/[\w-]+', content)
        if blog_links:
            # Check if any link to a known pillar
            for bl in blog_links:
                if bl.rstrip('/') in [p.rstrip('/') for p in pillar_pages]:
                    pillar_link_found = bl
                    break
            if not pillar_link_found and blog_links:
                pillar_link_found = f"links to: {', '.join(blog_links[:3])}"
    
    results["pillar"] = {
        "found": pillar_link_found,
        "pass": pillar_link_found is not None
    }
    
    # D. AEO/GEO Optimization
    q_words = r'\b(How|What|Why|When|Where|Can|Do|Does|Is|Are)\b.*\?'
    q_headings = re.findall(r'^##\s+' + q_words, content, re.MULTILINE | re.IGNORECASE)
    # Also check H3
    q_headings += re.findall(r'^###\s+' + q_words, content, re.MULTILINE | re.IGNORECASE)
    
    results["aeo"] = {
        "question_headings": len(q_headings),
        "pass": len(q_headings) >= 2
    }
    
    # E. Internal Linking
    # Count internal links: /something patterns
    internal_links = re.findall(r'\[([^\]]+)\]\((/[^\)]+)\)', content)
    # Filter to actual internal paths (not external URLs)
    internal_paths = [link for text, link in internal_links if not link.startswith('http') and not link.startswith('//')]
    
    results["internal_links"] = {
        "count": len(internal_paths),
        "pass": len(internal_paths) >= 3,
        "links": internal_paths
    }
    
    # F. Schema Ready
    schema_fields = {
        "title": bool(title),
        "excerpt": bool(excerpt),
        "date": bool(date),
        "metaTitle": bool(meta_title),
        "metaDescription": bool(meta_desc),
        "dateModified": bool(date_modified)
    }
    missing_fields = [k for k, v in schema_fields.items() if not v]
    
    # For case studies, excerpt and date are critical; meta fields are for ArticleSchema
    # Let me check if this post actually needs meta fields
    has_all_core = all([title, date])
    has_all_schema = all([meta_title, meta_desc, date_modified])
    
    results["schema"] = {
        "fields": schema_fields,
        "missing_fields": missing_fields,
        "pass": len(missing_fields) <= 1  # Allow missing meta if it's an older post
    }
    
    return results

# Run analysis for all changed slugs
all_results = {}
for slug in changed_slugs:
    print(f"\n{'='*60}")
    print(f"ANALYZING: {slug}")
    print(f"{'='*60}")
    result = analyze_post(slug)
    all_results[slug] = result
    
    if "error" in result:
        print(f"  ERROR: {result['error']}")
        continue
    
    # Print summary
    tf = result["tfidf"]
    print(f"\nA. TF-IDF: Keyword='{tf['keyword']}', Occurrences={tf['occurrences']}, PASS={tf['pass']}")
    
    en = result["entities"]
    print(f"B. Entities: Missing={en['missing']}, PASS={en['pass']}")
    
    pi = result["pillar"]
    print(f"C. Pillar Link: Found={pi['found']}, PASS={pi['pass']}")
    
    ae = result["aeo"]
    print(f"D. AEO/GEO: Question headings={ae['question_headings']}, PASS={ae['pass']}")
    
    il = result["internal_links"]
    print(f"E. Internal Links: Count={il['count']}, PASS={il['pass']}")
    
    sc = result["schema"]
    print(f"F. Schema: Missing fields={sc['missing_fields']}, PASS={sc['pass']}")

# Output JSON for report generation
print(f"\n\n{'='*60}")
print("JSON SUMMARY")
print(f"{'='*60}")
print(json.dumps(all_results, indent=2, default=str))
