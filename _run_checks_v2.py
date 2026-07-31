#!/usr/bin/env python3
"""
Framework check runner for the 4 changed posts in data.js - v2 with fixed logic
"""
import re

DATA_FILE = "/root/kanok-miahit/src/app/blog/data.js"

with open(DATA_FILE, "r") as f:
    content = f.read()

SLUGS_TO_CHECK = [
    "mobile-seo-optimization-bangladesh-mobile-first-era",
    "schema-markup-rich-snippets-techniques",
    "seo-canonical-url-guide-bd",
    "how-to-choose-best-seo-expert-dhaka-15-things",
]

def extract_post(content, slug):
    slug_pattern = rf'slug:\s*"{re.escape(slug)}"'
    match = re.search(slug_pattern, content)
    if not match:
        return None
    
    start = match.start()
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
    
    brace_depth = 0
    in_template_literal = False
    obj_end = None
    i = obj_start
    while i < len(content):
        ch = content[i]
        if in_template_literal:
            if ch == '`':
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
    pattern = rf'{field_name}:\s*"((?:[^"\\]|\\.)*)"'
    match = re.search(pattern, post_text, re.DOTALL)
    if match:
        return match.group(1)
    return None


def parse_tags(post_text):
    match = re.search(r'tags:\s*\[(.*?)\]', post_text, re.DOTALL)
    if match:
        tags_str = match.group(1)
        tags = re.findall(r'"([^"]*)"', tags_str)
        return tags
    return []


def extract_content(post_text):
    match = re.search(r'content:\s*`\n(.*?)`\s*,?\s*\}?\s*$', post_text, re.DOTALL)
    if not match:
        match = re.search(r'content:\s*`\n(.*?)`\s*,', post_text, re.DOTALL)
    if match:
        return match.group(1)
    return ""


def extract_primary_keyword(title):
    """Extract primary keyword: take first meaningful noun phrase before colon or pipe"""
    # Strip subtitle after colon or pipe
    for sep in [':', '|', '—', '–', '-']:
        if sep in title:
            title = title.split(sep)[0].strip()
    
    # Remove common leading phrases
    title_lower = title.lower()
    for prefix in ["how to ", "what is ", "what are ", "why ", "is ", "the ", "a ", "an "]:
        if title_lower.startswith(prefix):
            title_lower = title_lower[len(prefix):]
            title = title[len(prefix):]
            break
    
    # Get first 2-3 meaningful words
    words = title_lower.split()
    stop_words = {"for", "in", "of", "the", "a", "an", "your", "and", "to", "with", "from", "on", "at", "its", "our", "their"}
    meaningful = [w for w in words if w not in stop_words]
    
    if not meaningful:
        return words[0] if words else title
    
    # Take first 2-3 words for the keyword
    if len(meaningful) >= 3:
        return " ".join(meaningful[:3])
    return " ".join(meaningful)


def count_keyword_in_content(content, keyword):
    if not keyword:
        return 0
    return len(re.findall(re.escape(keyword), content, re.IGNORECASE))


def check_entity_appears(content, entity):
    """Check if entity text appears in content (flexible matching)"""
    # For multi-word tags, check if the main term appears
    # e.g. "SEO Expert Dhaka" -> check "seo expert" or "SEO" + "Dhaka"
    entity_lower = entity.lower()
    content_lower = content.lower()
    
    # Direct check first
    if entity_lower in content_lower:
        return True
    
    # For compound tags, split and check if key parts appear separately
    words = entity_lower.split()
    if len(words) >= 3:
        # Check if at least the first two words appear consecutively
        bigram = " ".join(words[:2])
        if bigram in content_lower:
            return True
        # Or check if the two main words appear separately
        key_words = [w for w in words if w not in {"seo", "seo", "bangladesh", "services", "expert"}]
        # Just check the whole phrase presence of partial
        if len(words) >= 2:
            if words[0] in content_lower and words[-1] in content_lower:
                return True
    
    return False


def check_entities(content, tags):
    """Check entity coverage. Tags are the key entities."""
    # Core entities that should always be present
    core_entities = ["Dhaka", "Bangladesh"]
    missing = []
    
    for entity in core_entities:
        if entity.lower() not in content.lower():
            missing.append(entity)
    
    # Check each tag entity (the tag itself)
    for tag in tags:
        if not check_entity_appears(content, tag):
            missing.append(tag)
    
    return missing


def count_question_headings(content):
    """Count question-based headings (## or ### starting with question words)"""
    headings = re.findall(r'^#{2,3}\s+(How|What|Why|When|Where|Can|Do|Is|Are|Does|Which|Who)\b', content, re.MULTILINE)
    return len(headings)


def count_internal_links(content):
    """Count internal links to other posts, services, locations"""
    links = re.findall(r'\[([^\]]*)\]\((/[^)]*)\)', content)
    internal = [(text, href) for text, href in links if href.startswith('/') and not href.startswith('//') and href not in ['/', '/#']]
    return len(internal), internal


def check_pillar_link(content, tags):
    """Check if post links to its pillar/service page"""
    tag_lower = [t.lower() for t in tags]
    
    pillar_mapping = {
        "mobile seo": "/services/local-seo",
        "mobile optimization": "/services/local-seo",
        "mobile-first indexing": "/services/local-seo",
        "mobile": "/services/local-seo",
        "schema": "/services/technical-seo",
        "structured data": "/services/technical-seo",
        "schema markup": "/services/technical-seo",
        "rich snippets": "/services/technical-seo",
        "canonical url": "/services/technical-seo",
        "technical seo": "/services/technical-seo",
        "canonical tag": "/services/technical-seo",
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
    
    if linked_pillars:
        for pillar_url in linked_pillars:
            if pillar_url in content:
                return True, pillar_url
    
    services_links = re.findall(r'\((/services/[^)]*)\)', content)
    if services_links:
        return True, services_links[0]
    
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
    
    title = parse_simple_field(post_text, 'title')
    date = parse_simple_field(post_text, 'date')
    post_content = extract_content(post_text)
    tags = parse_tags(post_text)
    
    if not title:
        print(f"## Post: {slug}")
        print("ERROR: Could not parse title")
        continue
    
    # A. TF-IDF Coverage
    keyword = extract_primary_keyword(title)
    kw_count = count_keyword_in_content(post_content, keyword)
    
    # B. Semantic Entity Coverage
    missing_entities = check_entities(post_content, tags)
    
    # C. Pillar-Cluster Alignment
    has_pillar, pillar_url = check_pillar_link(post_content, tags)
    
    # D. AEO/GEO Optimization
    q_headings = count_question_headings(post_content)
    
    # E. Internal Linking
    link_count, links = count_internal_links(post_content)
    
    # F. Schema
    schema_ok, schema_missing, schema_fields = check_schema_fields(post_text)
    
    results[slug] = {
        "title": title,
        "keyword": keyword,
        "kw_count": kw_count,
        "missing_entities": missing_entities,
        "has_pillar": has_pillar,
        "pillar_url": pillar_url,
        "q_headings": q_headings,
        "link_count": link_count,
        "tags": tags,
        "schema_ok": schema_ok,
        "schema_missing": schema_missing,
        "links_sample": links[:5],
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
    print(f"**Content:** {r['content_len']} chars")
    print()
    print(f"| Check | Status | Details |")
    print(f"|-------|--------|---------|")
    
    # A. TF-IDF
    tfidf_status = "✅" if r['kw_count'] >= 5 else ("⚠️" if r['kw_count'] >= 3 else "❌")
    print(f"| TF-IDF: \"{r['keyword']}\" | {tfidf_status} | {r['kw_count']} occurrences in content |")
    
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
    print(f"| AEO/GEO | {aeo_status} | {r['q_headings']} question-based headings |")
    
    # E. Internal Links
    il_status = "✅" if r['link_count'] >= 3 else "❌"
    print(f"| Internal Links | {il_status} | {r['link_count']} total internal links |")
    if r['link_count'] < 10:
        print(f"| Links sample | | {', '.join([f'[{t}]({h})' for t,h in r['links_sample']])} |")
    
    # F. Schema
    schema_status = "✅" if r['schema_ok'] else "❌"
    schema_detail = "All fields set" if r['schema_ok'] else f"Missing: {', '.join(r['schema_missing'])}"
    print(f"| Schema Ready | {schema_status} | {schema_detail} |")
    
    print()
    
    fix_items = []
    if r['kw_count'] < 5:
        if r['kw_count'] == 0:
            fix_items.append(f"- **TF-IDF thin**: Keyword \"{r['keyword']}\" not found in content. The keyword appears in the title but isn't repeated enough in the body. Add more natural mentions targeting ≥5.")
        else:
            fix_items.append(f"- **TF-IDF thin**: Keyword \"{r['keyword']}\" appears only {r['kw_count']}x. Add more natural mentions to reach ≥5.")
    if r['missing_entities']:
        fix_items.append(f"- **Missing entities**: Add mentions of: {missing_str}")
    if not r['has_pillar']:
        fix_items.append(f"- **Missing pillar link**: Add a link to the relevant pillar/service page based on tags")
    if r['q_headings'] < 2:
        fix_items.append(f"- **AEO/GEO low**: Add at least {2 - r['q_headings']} more question-based headings. Sprinkle How/What/Why/When sections.")
    if r['link_count'] < 3:
        fix_items.append(f"- **Internal linking low**: Add at least {3 - r['link_count']} more internal links to other posts, services, or locations.")
    if not r['schema_ok']:
        fix_items.append(f"- **Schema missing fields**: Add: {', '.join(r['schema_missing'])} to the post object.")
    
    if fix_items:
        print("### Fix instructions:")
        for item in fix_items:
            print(item)
    else:
        print("### All checks passed ✅")
    print()

# Summary
print("---")
print("## Overall Summary")
checks_total = 0
checks_pass = 0
for slug, r in results.items():
    post_pass = True
    for check_name, condition, label in [
        ("TF-IDF", r['kw_count'] >= 3, "keyword density"),
        ("Entities", not r['missing_entities'], "entity coverage"),
        ("Pillar", r['has_pillar'], "pillar link"),
        ("AEO/GEO", r['q_headings'] >= 2, "question headings"),
        ("Internal Links", r['link_count'] >= 3, "internal linking"),
        ("Schema", r['schema_ok'], "schema fields"),
    ]:
        checks_total += 1
        if condition:
            checks_pass += 1
        else:
            post_pass = False
    
    status_icon = "✅" if post_pass else "❌"
    print(f"{status_icon} {slug}: {'All pass' if post_pass else 'Has issues'}")

print(f"\n**{checks_pass}/{checks_total} checks passing ({checks_pass/checks_total*100:.0f}%)**")
