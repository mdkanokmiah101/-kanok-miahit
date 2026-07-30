#!/usr/bin/env python3
"""Framework enforcement checks for kanokmiah.com.bd blog posts — v2."""
import re, sys

with open('src/app/blog/data.js', 'r') as f:
    raw = f.read()

def extract_post(raw, slug):
    """Extract a post object by slug, handling template literal content."""
    idx = raw.find(f"slug: \"{slug}\"")
    if idx == -1:
        idx = raw.find(f"slug: '{slug}'")
    if idx == -1:
        print(f"ERROR: slug '{slug}' not found")
        return None
    
    obj_start = raw.rfind('{\n', 0, idx)
    if obj_start == -1:
        obj_start = raw.rfind('{', 0, idx)
    
    content_marker = raw.find('content: `', obj_start)
    if content_marker == -1:
        content_marker = raw.find('content: \x60', obj_start)
    
    content_start = content_marker + len('content: `')
    content_end = raw.find('`,\n', content_start)
    if content_end == -1:
        content_end = raw.find('`,\n  ', content_start)
    
    post_content = raw[content_start:content_end]
    
    def get_field(field_name):
        m = re.search(rf'{field_name}:\s*"([^"]*)"', raw[obj_start:content_marker])
        if m:
            return m.group(1)
        m = re.search(rf"{field_name}:\s*'([^']*)'", raw[obj_start:content_marker])
        if m:
            return m.group(1)
        return None
    
    title = get_field('title')
    excerpt = get_field('excerpt')
    date_val = get_field('date')
    meta_title = get_field('metaTitle')
    meta_desc = get_field('metaDescription')
    date_mod = get_field('dateModified')
    
    tags_match = re.search(r'tags:\s*\[(.*?)\]', raw[obj_start:content_marker], re.DOTALL)
    tags = []
    if tags_match:
        tags = re.findall(r'"([^"]*)"', tags_match.group(1))
    
    return {
        'slug': slug,
        'title': title,
        'excerpt': excerpt,
        'date': date_val,
        'metaTitle': meta_title,
        'metaDescription': meta_desc,
        'dateModified': date_mod,
        'tags': tags,
        'content': post_content
    }

def check_tfidf(post):
    """Check TF-IDF keyword coverage."""
    title = post.get('title', '') or ''
    content = post.get('content', '') or ''
    
    # Manual keyword mapping for known posts
    slug = post.get('slug', '')
    keyword_map = {
        'mobile-seo-optimization-bangladesh-mobile-first-era': 'Mobile SEO',
        'how-to-choose-best-seo-expert-dhaka-15-things': 'SEO Expert in Dhaka',
    }
    
    if slug in keyword_map:
        keyword = keyword_map[slug]
    else:
        # Generic fallback: extract from title
        title_clean = re.sub(r'\s*[|–—-].*$', '', title).strip()
        if ':' in title_clean:
            keyword = title_clean.split(':')[0].strip()
        else:
            keyword = title_clean
    
    count = len(re.findall(re.escape(keyword), content, re.IGNORECASE))
    
    return {
        'keyword': keyword,
        'occurrences': count,
        'pass': count >= 5
    }

def check_entities(post):
    """Check semantic entity coverage."""
    content = post.get('content', '') or ''
    
    missing = []
    
    dhaka_count = len(re.findall(r'Dhaka', content, re.IGNORECASE))
    bd_count = len(re.findall(r'Bangladesh', content, re.IGNORECASE))
    
    if dhaka_count == 0:
        missing.append('Dhaka')
    if bd_count == 0:
        missing.append('Bangladesh')
    
    return {
        'missing': missing,
        'pass': len(missing) == 0,
        'dhaka_count': dhaka_count,
        'bd_count': bd_count
    }

def check_pillar(post):
    """Check pillar-cluster alignment."""
    content = post.get('content', '') or ''
    tags = post.get('tags', [])
    
    # Standard pillar pages on this site
    pillar_pages = [
        '/blog/complete-seo-guide-bangladesh-businesses-2026',
        '/blog/local-seo-tips-dhaka-businesses-google-maps',
        '/blog/technical-seo-checklist-bangladeshi-websites',
        '/blog/why-ecommerce-store-needs-seo-bangladesh',
        '/blog/how-to-choose-right-seo-agency-bangladesh',
    ]
    
    linked_pillars = [p for p in pillar_pages if p in content]
    
    return {
        'linked_pillars': linked_pillars,
        'pass': len(linked_pillars) > 0
    }

def check_aeo_geo(post):
    """Check AEO/GEO question-based headings."""
    content = post.get('content', '') or ''
    
    # Count all question-based headings (##+ at start of line)
    heading_qs = re.findall(r'^#{2,6}\s+(How|What|Why|When|Where|Can|Do|Is|Are)\b',
                            content, re.IGNORECASE | re.MULTILINE)
    
    # Also count bold/FAQ questions like **What is...?**
    # These are typically in FAQ sections without heading markup
    lines = content.split('\n')
    faq_count = 0
    for line in lines:
        line = line.strip()
        if line.startswith('**') and re.match(r'\*\*(How|What|Why|When|Where|Can|Do|Is|Are)\b', line):
            faq_count += 1
    
    total = len(heading_qs) + faq_count
    
    return {
        'question_headings': heading_qs,
        'faq_questions': faq_count,
        'count': total,
        'pass': total >= 2
    }

def check_internal_links(post):
    """Check internal linking."""
    content = post.get('content', '') or ''
    
    # Find all markdown links with relative paths
    # Pattern: [text](/path)  or  (/)  or  (/(/more))
    all_links = re.findall(r'\(/([a-z0-9_-]+(?:/[a-z0-9_-]+)*|)\)', content)
    # Filter empty and clean up
    links = [l if l else '/' for l in all_links]
    
    # Also find bare paths that might be in angle brackets or other formats
    # Count unique links
    unique_links = list(set(links))
    
    return {
        'links': unique_links,
        'count': len(links),
        'pass': len(links) >= 3
    }

def check_schema(post):
    """Check ArticleSchema readiness."""
    missing = []
    
    if not post.get('title'):
        missing.append('title')
    if not post.get('excerpt'):
        missing.append('excerpt')
    if not post.get('date'):
        missing.append('date')
    if not post.get('metaTitle'):
        missing.append('metaTitle')
    if not post.get('metaDescription'):
        missing.append('metaDescription')
    
    return {
        'missing': missing,
        'pass': len(missing) == 0
    }

# Main
slugs = [
    'mobile-seo-optimization-bangladesh-mobile-first-era',
    'how-to-choose-best-seo-expert-dhaka-15-things'
]

for slug in slugs:
    post = extract_post(raw, slug)
    if not post:
        continue
    
    print(f"\n## Post: {slug}")
    print(f"| Check | Status | Details |")
    print(f"|-------|--------|---------|")
    
    # A. TF-IDF
    tfidf = check_tfidf(post)
    status = "✅" if tfidf['pass'] else "❌"
    print(f"| TF-IDF: \"{tfidf['keyword']}\" | {status} | {tfidf['occurrences']} occurrences |")
    
    # B. Entities
    ent = check_entities(post)
    status = "✅" if ent['pass'] else "❌"
    detail = f"Dhaka: {ent['dhaka_count']}, Bangladesh: {ent['bd_count']}" if ent['pass'] else f"Missing: {', '.join(ent['missing'])}"
    print(f"| Entities | {status} | {detail} |")
    
    # C. Pillar
    pillar = check_pillar(post)
    status = "✅" if pillar['pass'] else "❌"
    detail = f"Links to: {', '.join(pillar['linked_pillars'])}" if pillar['pass'] else "No pillar page link found"
    print(f"| Pillar Link | {status} | {detail} |")
    
    # D. AEO/GEO
    aeo = check_aeo_geo(post)
    status = "✅" if aeo['pass'] else "❌"
    q_h = aeo['question_headings']
    q_str = ', '.join(q_h) if q_h else 'none'
    print(f"| AEO/GEO | {status} | {aeo['count']} total ({len(q_h)} heading + {aeo['faq_questions']} FAQ) |")
    
    # E. Internal Links
    il = check_internal_links(post)
    status = "✅" if il['pass'] else "❌"
    print(f"| Internal Links | {status} | {il['count']} total |")
    
    # F. Schema
    schema = check_schema(post)
    status = "✅" if schema['pass'] else "❌"
    detail = "All fields set" if schema['pass'] else f"Missing: {', '.join(schema['missing'])}"
    print(f"| Schema Ready | {status} | {detail} |")
    
    # Fix instructions
    print(f"\n### Fix instructions:")
    fixes = []
    if not tfidf['pass']:
        fixes.append(f"- **TF-IDF**: Increase \"{tfidf['keyword']}\" occurrences from {tfidf['occurrences']} to ≥5")
    if not ent['pass']:
        fixes.append(f"- **Entities**: Add missing entities: {', '.join(ent['missing'])}")
    if not pillar['pass']:
        fixes.append("- **Pillar**: Add internal link to the pillar page (e.g., /blog/complete-seo-guide-bangladesh-businesses-2026)")
    if not aeo['pass']:
        fixes.append(f"- **AEO/GEO**: Add more question-based headings (How, What, Why, etc.) — currently {aeo['count']}, need ≥2")
    if not il['pass']:
        fixes.append(f"- **Internal Links**: Add more internal links — currently {il['count']}, need ≥3")
    if not schema['pass']:
        fixes.append(f"- **Schema**: Add missing schema fields: {', '.join(schema['missing'])}")
    
    if fixes:
        for f in fixes:
            print(f)
    else:
        print("All checks passed — no fixes needed.")
