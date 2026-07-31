#!/usr/bin/env python3
"""
Framework check runner for the 4 changed posts in data.js
"""
import re
import json

DATA_FILE = "/root/kanok-miahit/src/app/blog/data.js"

with open(DATA_FILE, "r") as f:
    content = f.read()

# The data.js exports an array. Let's find the posts array
# Pattern: match each post object: { slug: "...", ... }
# We'll extract based on slug

SLUGS_TO_CHECK = [
    "mobile-seo-optimization-bangladesh-mobile-first-era",
    "schema-markup-rich-snippets-techniques",
    "seo-canonical-url-guide-bd",
    "how-to-choose-best-seo-expert-dhaka-15-things",
]

def extract_post(content, slug):
    """Extract a single post object as a text block starting from its slug line to the closing },"""
    # Find the slug line
    slug_pattern = rf"slug:\s*\"{re.escape(slug)}\""
    match = re.search(slug_pattern, content)
    if not match:
        return None
    
    # Find the start of this object - go back to find the opening { before slug
    start = match.start()
    # Go backwards to find the opening {
    brace_depth = 0
    obj_start = None
    for i in range(start, max(start - 500, -1), -1):
        if content[i] == '}':
            brace_depth += 1
        elif content[i] == '{':
            brace_depth -= 1
            if brace_depth < 0:
                obj_start = i
                break
    
    if obj_start is None:
        return None
    
    # Find the end of this object - need to find the matching }
    brace_depth = 0
    in_template_literal = False
    obj_end = None
    i = obj_start
    while i < len(content):
        ch = content[i]
        if in_template_literal:
            if ch == '`' and (i == 0 or content[i-1] != '\\'):
                in_template_literal = False
        else:
            if ch == '`':
                in_template_literal = True
            elif ch == '{':
                brace_depth += 1
            elif ch == '}':
                brace_depth -= 1
                if brace_depth == 0:
                    obj_end = i + 1
                    break
        i += 1
    
    if obj_end is None:
        return None
    
    return content[obj_start:obj_end]


def parse_simple_field(post_text, field_name):
    """Extract a simple string field value (not content/template literal)"""
    # Match field: "value" or field:\n      "multi-line value"
    pattern = rf'{field_name}:\s*"((?:[^"\\]|\\.)*)"'
    match = re.search(pattern, post_text, re.DOTALL)
    if match:
        return match.group(1)
    return None


def parse_tags(post_text):
    """Extract tags array"""
    match = re.search(r'tags:\s*\[(.*?)\]', post_text, re.DOTALL)
    if match:
        tags_str = match.group(1)
        tags = re.findall(r'"([^"]*)"', tags_str)
        return tags
    return []


def extract_content(post_text):
    """Extract content template literal"""
    match = re.search(r'content:\s*`\n(.*?)`\s*,?\s*\}?\s*$', post_text, re.DOTALL)
    if not match:
        match = re.search(r'content:\s*`\n(.*?)`\s*,', post_text, re.DOTALL)
    if match:
        return match.group(1)
    return ""


def count_keyword_in_content(content, keyword):
    """Count occurrences of primary keyword in content"""
    if not keyword:
        return 0
    return len(re.findall(re.escape(keyword), content, re.IGNORECASE))


def extract_primary_keyword(title):
    """Extract primary keyword from title"""
    # First meaningful noun phrase: skip "How to", "What", "Why", "The", "A", "An"
    # Return first few meaningful words or the whole title processed
    title_lower = title.lower()
    # Remove common prefixes
    for prefix in ["how to ", "what is ", "what are ", "why ", "the ", "a ", "an "]:
        if title_lower.startswith(prefix):
            title_lower = title_lower[len(prefix):]
            break
    
    # Take first 2-4 meaningful words
    words = title_lower.split()
    # Remove words like "for", "in", "of", "the", "a", "an", "your", "and", "to"
    stop_words = {"for", "in", "of", "the", "a", "an", "your", "and", "to", "with", "from", "on", "at", "is", "are", "that", "this", "our", "their", "its"}
    meaningful = [w for w in words if w not in stop_words]
    if not meaningful:
        return words[0] if words else title
    return " ".join(meaningful[:4])


def check_entities(content, entities):
    """Check which entities appear in content"""
    missing = []
    for entity in entities:
        if not re.search(re.escape(entity), content, re.IGNORECASE):
            missing.append(entity)
    return missing


def count_question_headings(content):
    """Count question-based headings (## or ### starting with question words)"""
    headings = re.findall(r'^#{2,3}\s+(How|What|Why|When|Where|Can|Do|Is|Are|Does|Which|Who)\b', content, re.MULTILINE)
    return len(headings)


def count_internal_links(content):
    """Count internal links to other posts, services, locations"""
    # Internal links: [text](/...) - relative paths
    links = re.findall(r'\[([^\]]*)\]\((/[^)]*)\)', content)
    # Filter to actual internal links (not anchors, not external)
    internal = [(text, href) for text, href in links if href.startswith('/') and not href.startswith('//')]
    return len(internal), internal


def check_pillar_link(content, tags):
    """Check if post links to its pillar topic page"""
    # Based on tags, determine pillar topic
    tag_lower = [t.lower() for t in tags]
    
    pillar_mapping = {
        "mobile seo": "/services/local-seo",
        "mobile optimization": "/services/local-seo",
        "mobile-first indexing": "/services/local-seo",
        "schema": "/services/technical-seo",
        "structured data": "/services/technical-seo",
        "rich snippets": "/services/technical-seo",
        "canonical url": "/services/technical-seo",
        "technical seo": "/services/technical-seo",
        "seo expert dhaka": "/services/local-seo",
        "hire seo expert": "/services/local-seo",
        "best seo expert": "/services/local-seo",
        "seo services bangladesh": "/services/local-seo",
        "local seo": "/services/local-seo",
        "content seo": "/services/on-page-seo",
        "on-page seo": "/services/on-page-seo",
        "seo consultant": "/services/local-seo",
        "ecommerce seo": "/services/ecommerce-seo",
    }
    
    linked_pillars = set()
    for tag in tag_lower:
        if tag in pillar_mapping:
            linked_pillars.add(pillar_mapping[tag])
    
    # Check if any of these pillar pages are linked
    if linked_pillars:
        for pillar_url in linked_pillars:
            if pillar_url in content:
                return True, pillar_url
    
    # If no pillar URL found, check for any /services/ link
    services_links = re.findall(r'\((/services/[^)]*)\)', content)
    if services_links:
        return True, services_links[0]  # Has some service link
    
    return False, ""

def check_schema_fields(post_text):
    """Check if post has all fields needed for ArticleSchema"""
    fields = {
        'title': parse_simple_field(post_text, 'title'),
        'excerpt': parse_simple_field(post_text, 'excerpt'),
        'date': parse_simple_field(post_text, 'date'),
        'metaTitle': parse_simple_field(post_text, 'metaTitle'),
        'metaDescription': parse_simple_field(post_text, 'metaDescription'),
        'dateModified': parse_simple_field(post_text, 'dateModified'),
    }
    missing = [k for k, v in fields.items() if not v]
    return len(missing) == 0, missing, fields


# Main
results = {}
for slug in SLUGS_TO_CHECK:
    post_text = extract_post(content, slug)
    if not post_text:
        print(f"## Post: {slug}")
        print("ERROR: Could not extract post")
        print()
        continue
    
    # Extract fields
    title = parse_simple_field(post_text, 'title')
    date = parse_simple_field(post_text, 'date')
    post_content = extract_content(post_text)
    tags = parse_tags(post_text)
    
    if not title:
        print(f"## Post: {slug}")
        print("ERROR: Could not parse title")
        print()
        continue
    
    # A. TF-IDF Coverage
    keyword = extract_primary_keyword(title)
    kw_count = count_keyword_in_content(post_content, keyword)
    
    # B. Semantic Entity Coverage
    entities = [
        "Dhaka", "Bangladesh", "SEO"
    ]
    
    # Add tag-based entities
    for tag in tags:
        if "seo" in tag.lower() and tag not in entities:
            entities.append(tag)
    
    missing_entities = check_entities(post_content, entities)
    
    # C. Pillar-Cluster Alignment
    has_pillar, pillar_url = check_pillar_link(post_content, tags)
    
    # D. AEO/GEO Optimization
    q_headings = count_question_headings(post_content)
    
    # E. Internal Linking
    link_count, links = count_internal_links(post_content)
    
    # F. Schema
    schema_ok, schema_missing, schema_fields = check_schema_fields(post_text)
    
    # Build result
    results[slug] = {
        "title": title,
        "keyword": keyword,
        "kw_count": kw_count,
        "missing_entities": missing_entities,
        "has_pillar": has_pillar,
        "pillar_url": pillar_url,
        "q_headings": q_headings,
        "link_count": link_count,
        "links": links,
        "schema_ok": schema_ok,
        "schema_missing": schema_missing,
        "tags": tags,
        "content_len": len(post_content),
    }

# Print report
for slug in SLUGS_TO_CHECK:
    if slug not in results:
        continue
    r = results[slug]
    
    print(f"## Post: {slug}")
    print(f"**Title:** {r['title']}")
    print(f"**Tags:** {', '.join(r['tags'])}")
    print(f"**Content length:** {r['content_len']} chars")
    print()
    print(f"| Check | Status | Details |")
    print(f"|-------|--------|---------|")
    
    # A. TF-IDF
    tfidf_status = "✅" if r['kw_count'] >= 5 else "❌"
    print(f"| TF-IDF: '{r['keyword']}' | {tfidf_status} | {r['kw_count']} occurrences |")
    
    # B. Entities
    ent_status = "✅" if not r['missing_entities'] else "❌"
    missing_str = ", ".join(r['missing_entities']) if r['missing_entities'] else "None"
    print(f"| Entities | {ent_status} | Missing: {missing_str} |")
    
    # C. Pillar
    pillar_status = "✅" if r['has_pillar'] else "❌"
    pillar_detail = r['pillar_url'] if r['has_pillar'] else "No pillar link found"
    print(f"| Pillar Link | {pillar_status} | Links to: {pillar_detail} |")
    
    # D. AEO/GEO
    aeo_status = "✅" if r['q_headings'] >= 2 else "❌"
    print(f"| AEO/GEO | {aeo_status} | {r['q_headings']} question headings |")
    
    # E. Internal Links
    il_status = "✅" if r['link_count'] >= 3 else "❌"
    print(f"| Internal Links | {il_status} | {r['link_count']} total |")
    if r['link_count'] < 10:
        print(f"| Internal Links (detail) | | {', '.join([f'[{t}]({h})' for t,h in r['links'][:10]])} |")
    
    # F. Schema
    schema_status = "✅" if r['schema_ok'] else "❌"
    schema_detail = "All fields set" if r['schema_ok'] else f"Missing: {', '.join(r['schema_missing'])}"
    print(f"| Schema Ready | {schema_status} | {schema_detail} |")
    
    print()
    
    # Fix instructions
    fix_items = []
    if r['kw_count'] < 5:
        fix_items.append(f"- **TF-IDF thin**: Increase usage of '{r['keyword']}' to at least 5 occurrences (currently {r['kw_count']})")
    if r['missing_entities']:
        fix_items.append(f"- **Missing entities**: Add mentions of: {missing_str}")
    if not r['has_pillar']:
        fix_items.append(f"- **Missing pillar link**: Add a link to the relevant pillar/service page based on tags")
    if r['q_headings'] < 2:
        fix_items.append(f"- **AEO/GEO low**: Add at least {2 - r['q_headings']} more question-based headings (How, What, Why, etc.)")
    if r['link_count'] < 3:
        fix_items.append(f"- **Internal linking low**: Add at least {3 - r['link_count']} more internal links to other posts, services, or locations")
    if not r['schema_ok']:
        fix_items.append(f"- **Schema missing fields**: Add: {', '.join(r['schema_missing'])}")
    
    if fix_items:
        print("### Fix instructions:")
        for item in fix_items:
            print(item)
    else:
        print("### All checks passed ✅")
    print()

# Summary
print("---")
print("## Summary")
all_pass = all(
    r['kw_count'] >= 5
    and not r['missing_entities']
    and r['has_pillar']
    and r['q_headings'] >= 2
    and r['link_count'] >= 3
    and r['schema_ok']
    for r in results.values()
)
if all_pass:
    print("✅ All framework checks pass for all changed posts.")
else:
    fails = sum(1 for r in results.values() if not (
        r['kw_count'] >= 5
        and not r['missing_entities']
        and r['has_pillar']
        and r['q_headings'] >= 2
        and r['link_count'] >= 3
        and r['schema_ok']
    ))
    print(f"⚠️ {fails}/{len(results)} posts have framework issues requiring attention.")
