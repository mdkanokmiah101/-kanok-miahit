#!/usr/bin/env python3
"""
Analyze 18 blog posts modified in the last 48 hours in data.js
Extract metadata, count keywords, question headings, internal links, etc.
"""
import re
import json

# Read the file
with open('/root/kanok-miahit/src/app/blog/data.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Define all 18 modified slugs based on git diff analysis
slugs = [
    "mobile-seo-optimization-bangladesh-mobile-first-era",
    "schema-markup-rich-snippets-techniques",
    "why-md-kanok-miah-is-the-best-seo-expert-in-dhaka-bangladesh",
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
]

def extract_post_object(text, slug):
    """Extract the full post object for a given slug."""
    # Find the slug in the text
    pattern = r'{\s*\n\s+slug:\s*"' + re.escape(slug) + r'"'
    match = re.search(pattern, text)
    if not match:
        return None
    
    start = match.start()
    
    # Find the content field opening
    content_marker = text.find('content: `', start)
    if content_marker == -1:
        return None
    
    # Find the metadata section (everything before content)
    meta_section = text[start:content_marker]
    
    # Extract metadata fields
    result = {}
    
    # slug
    m = re.search(r'slug:\s*"([^"]+)"', meta_section)
    if m: result['slug'] = m.group(1)
    
    # title
    m = re.search(r'title:\s*"([^"]+)"', meta_section)
    if m: result['title'] = m.group(1)
    
    # date
    m = re.search(r'date:\s*"([^"]+)"', meta_section)
    if m: result['date'] = m.group(1)
    
    # author
    m = re.search(r'author:\s*"([^"]+)"', meta_section)
    if m: result['author'] = m.group(1)
    
    # excerpt
    m = re.search(r'excerpt:\s*\n?\s*"([^"]+)"', meta_section)
    if m: result['excerpt'] = m.group(1)
    
    # tags
    m = re.search(r'tags:\s*\[([^\]]+)\]', meta_section)
    if m:
        tags_str = m.group(1)
        tags = re.findall(r'"([^"]+)"', tags_str)
        result['tags'] = tags
    
    # metaTitle
    m = re.search(r'metaTitle:\s*\n?\s*"([^"]+)"', meta_section)
    if m: result['metaTitle'] = m.group(1)
    
    # metaDescription
    m = re.search(r'metaDescription:\s*\n?\s*"([^"]+)"', meta_section)
    if m: result['metaDescription'] = m.group(1)
    
    # dateModified
    m = re.search(r'dateModified:\s*"([^"]+)"', meta_section)
    if m: result['dateModified'] = m.group(1)
    
    # Extract content - find the backtick string
    content_start = content_marker + len('content: `')
    # Find closing backtick
    content_end = text.find('`,\n', content_start)
    if content_end == -1:
        content_end = text.find('`\n', content_start)
    if content_end == -1:
        content_end = text.find('`,', content_start)
    if content_end != -1:
        result['content'] = text[content_start:content_end]
    
    return result

def get_first_keyword_noun_phrase(title):
    """Extract first meaningful keyword from title."""
    if not title:
        return ""
    # Remove trailing site name
    title = re.sub(r'\s*[|—–-]\s*Kanok Miah.*$', '', title).strip()
    title = re.sub(r'\s*[|—–-]\s*.*$', '', title).strip()
    # Take first meaningful looking phrase
    words = title.split()
    # Skip articles/prepositions at start
    skip = {'the', 'a', 'an', 'how', 'what', 'why', 'when', 'where', 'is', 'are', 'do', 'does', 'can'}
    for i, w in enumerate(words):
        if w.lower() not in skip and len(w) > 2:
            # Take up to 4 words as keyword phrase
            return ' '.join(words[i:i+3]).strip(',;:')
    return words[0] if words else ""

def count_keyword(content, keyword):
    """Count occurrences of keyword in content (case-insensitive)."""
    if not content or not keyword:
        return 0
    pattern = re.escape(keyword)
    return len(re.findall(pattern, content, re.IGNORECASE))

def count_question_headings(content):
    """Count headings starting with How/What/Why/When/Where/Can/Do/Is/Are."""
    if not content:
        return 0, []
    # Match ## headings
    headings = re.findall(r'^##[^#].*$', content, re.MULTILINE)
    question_heads = []
    for h in headings:
        h_stripped = h.strip('# ')
        if re.match(r'^(How|What|Why|When|Where|Can|Do|Is|Are)\b', h_stripped, re.IGNORECASE):
            question_heads.append(h_stripped)
    return len(question_heads), question_heads

def count_internal_links(content):
    """Count links starting with / (internal links)."""
    if not content:
        return 0, []
    links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
    internal = [(text, url) for text, url in links if url.startswith('/')]
    return len(internal), internal

def check_pillar_link(content, tags):
    """Check if post links to a relevant pillar page."""
    if not content or not tags:
        return False, []
    tags_lower = [t.lower() for t in tags]
    
    # Pillar pages mapping
    pillar_pages = {
        'seo': ['/services/', '/blog/complete-seo-guide-bangladesh-businesses-2026'],
        'local seo': ['/services/local-seo'],
        'technical seo': ['/services/technical-seo'],
        'ecommerce': ['/services/ecommerce-seo'],
        'seo expert': ['/'],
        'case study': ['/case-studies'],
        'b2b': ['/blog/b2b-lead-generation-seo-bangladesh'],
        'smm': ['/services/ecommerce-seo'],
        'garments': ['/industries/garments-textile'],
    }
    
    relevant_pillars = []
    for tag in tags_lower:
        for keyword, pages in pillar_pages.items():
            if keyword in tag:
                relevant_pillars.extend(pages)
    
    # Check if content links to these pages
    found = []
    for p in set(relevant_pillars):
        if p in content:
            found.append(p)
    
    return len(found) > 0, found

def check_entities(content):
    """Check for location, service type, industry mentions."""
    if not content:
        return {}
    content_lower = content.lower()
    return {
        'dhaka': 'Dhaka' in content or 'dhaka' in content_lower,
        'bangladesh': 'Bangladesh' in content or 'bangladesh' in content_lower,
        'gulshan': 'Gulshan' in content or 'gulshan' in content_lower,
        'banani': 'Banani' in content or 'banani' in content_lower,
        'uttara': 'Uttara' in content or 'uttara' in content_lower,
        'dhanmondi': 'Dhanmondi' in content or 'dhanmondi' in content_lower,
        'mirpur': 'Mirpur' in content or 'mirpur' in content_lower,
    }

# Process each post
results = []
for slug in slugs:
    post = extract_post_object(content, slug)
    if not post:
        print(f"WARNING: Could not extract post for slug: {slug}")
        continue
    
    title = post.get('title', '')
    tags = post.get('tags', [])
    post_content = post.get('content', '')
    
    keyword = get_first_keyword_noun_phrase(title)
    keyword_count = count_keyword(post_content, keyword)
    q_count, q_heads = count_question_headings(post_content)
    il_count, il_links = count_internal_links(post_content)
    has_pillar, pillar_found = check_pillar_link(post_content, tags)
    entities = check_entities(post_content)
    
    report = {
        'slug': post.get('slug', slug),
        'title': title,
        'date': post.get('date', ''),
        'tags': tags,
        'keyword_analyzed': keyword,
        'keyword_count_in_content': keyword_count,
        'question_headings_count': q_count,
        'question_headings': q_heads[:10],  # top 10
        'internal_links_count': il_count,
        'internal_links': il_links[:10],  # top 10
        'has_metaTitle': 'metaTitle' in post,
        'metaTitle': post.get('metaTitle', None),
        'has_metaDescription': 'metaDescription' in post,
        'metaDescription': post.get('metaDescription', None),
        'has_dateModified': 'dateModified' in post,
        'dateModified': post.get('dateModified', None),
        'entities': entities,
        'has_pillar_link': has_pillar,
        'pillar_links_found': pillar_found,
        'content_length': len(post_content) if post_content else 0,
        'git_change_type': None,  # will fill in
    }
    
    # Classify git change type
    slug_to_change = {
        "mobile-seo-optimization-bangladesh-mobile-first-era": "Added metaTitle, metaDescription, dateModified",
        "schema-markup-rich-snippets-techniques": "Code block formatting fix (Bengali JSON-LD fencing)",
        "why-md-kanok-miah-is-the-best-seo-expert-in-dhaka-bangladesh": "URL conversion (external→internal)",
        "landlord-certificates-seo-case-study": "URL conversion (external→internal)",
        "das-taxis-scotland-seo-case-study": "URL conversion (external→internal)",
        "morethanpanel-seo-case-study": "URL conversion (external→internal)",
        "smmgen-seo-case-study": "URL conversion (external→internal)",
        "smmsun-seo-case-study": "URL conversion (external→internal)",
        "mir-cement-seo-case-study": "URL conversion (external→internal)",
        "dhaka-apparels-seo-case-study": "URL conversion (external→internal)",
        "stealth-windshield-repairs-seo-case-study": "URL conversion (external→internal)",
        "how-to-choose-best-seo-expert-dhaka-15-things": "Major: added metaTitle/metaDescription/dateModified + URL conversions + internal links",
        "seo-expert-vs-seo-agency-dhaka-which-is-right": "URL conversion (external→internal)",
        "top-10-seo-mistakes-dhaka-businesses-fix": "URL conversion (external→internal)",
        "what-does-seo-expert-do-guide-business-owners": "URL conversion (external→internal)",
        "seo-case-study-dhaka-businesses-increased-organic-traffic": "URL conversion (external→internal)",
        "hiring-seo-expert-dhaka-better-roi-than-paid-ads": "URL conversion (external→internal)",
        "ai-seo-2026-dhaka-experts-optimize-google-ai-chatgpt": "URL conversion (external→internal)",
    }
    report['git_change_type'] = slug_to_change.get(slug, "Unknown")
    
    results.append(report)
    print(f"✓ Analyzed: {post.get('slug', '?')}")

# Summary stats
print(f"\n{'='*80}")
print(f"COMPLETE: Analyzed {len(results)} posts")
print(f"{'='*80}")

# Output as JSON
print("\n--- STRUCTURED JSON REPORT ---")
print(json.dumps(results, indent=2, ensure_ascii=False, default=str))

# Summary table
print(f"\n{'='*80}")
print("SUMMARY TABLE")
print(f"{'='*80}")
print(f"{'#':<3} {'Slug':<55} {'KW Count':<8} {'Q Hdgs':<7} {'Int Links':<9} {'MetaT':<6} {'MetaD':<6} {'DateM':<6} {'Pillar':<6}")
print(f"{'─'*3} {'─'*55} {'─'*8} {'─'*7} {'─'*9} {'─'*6} {'─'*6} {'─'*6} {'─'*6}")
for i, r in enumerate(results, 1):
    kw = r['keyword_count_in_content']
    qh = r['question_headings_count']
    il = r['internal_links_count']
    mt = '✓' if r['has_metaTitle'] else '✗'
    md = '✓' if r['has_metaDescription'] else '✗'
    dm = '✓' if r['has_dateModified'] else '✗'
    pl = '✓' if r['has_pillar_link'] else '✗'
    short_slug = r['slug'][:54]
    print(f"{i:<3} {short_slug:<55} {kw:<8} {qh:<7} {il:<9} {mt:<6} {md:<6} {dm:<6} {pl:<6}")

print(f"\n{'='*80}")
print("DETAILED PER-POST REPORT")
print(f"{'='*80}")

for r in results:
    print(f"\n{'─'*80}")
    print(f"Post: {r['slug']}")
    print(f"Title: {r['title']}")
    print(f"Date: {r['date']}")
    print(f"Tags: {', '.join(r['tags'])}")
    print(f"Git Change: {r['git_change_type']}")
    print(f"Content Length: {r['content_length']:,} chars")
    print(f"")
    print(f"  Keyword Analyzed: '{r['keyword_analyzed']}' — Count in content: {r['keyword_count_in_content']}")
    print(f"  Question Headings: {r['question_headings_count']}")
    for h in r['question_headings'][:5]:
        print(f"    - {h}")
    print(f"  Internal Links: {r['internal_links_count']}")
    for t, u in r['internal_links'][:5]:
        print(f"    - [{t}]({u})")
    print(f"  Metadata:")
    print(f"    metaTitle: {'✓ PRESENT' if r['has_metaTitle'] else '✗ MISSING'} = {r.get('metaTitle','N/A')[:60] if r.get('metaTitle') else 'N/A'}...")
    print(f"    metaDescription: {'✓ PRESENT' if r['has_metaDescription'] else '✗ MISSING'} = {r.get('metaDescription','N/A')[:60] if r.get('metaDescription') else 'N/A'}...")
    print(f"    dateModified: {'✓ PRESENT' if r['has_dateModified'] else '✗ MISSING'} = {r.get('dateModified','N/A')}")
    print(f"  Entities:")
    for k, v in r['entities'].items():
        print(f"    {k}: {'✓' if v else '✗'}")
    print(f"  Pillar Link: {'✓ YES' if r['has_pillar_link'] else '✗ NO'}")
    if r['pillar_links_found']:
        for p in r['pillar_links_found']:
            print(f"    - {p}")
