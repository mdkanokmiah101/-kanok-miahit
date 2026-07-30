#!/usr/bin/env python3
"""
Framework enforcement checker for kanokmiah.com.bd blog posts.
Fixed parser for multi-line fields. Run framework checks on all modified posts.
"""
import re
import sys

DATA_FILE = "src/app/blog/data.js"

MODIFIED_SLUGS = [
    "link-building-strategies-bangladesh-market",
    "seo-garments-textile-industry-b2b-lead-generation",
    "google-business-profile-optimization-guide-bangladesh",
    "mobile-seo-optimization-bangladesh-mobile-first-era",
    "why-md-kanok-miah-is-the-best-seo-expert-in-dhaka-bangladesh",
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


def extract_string_value(lines, start_idx):
    """Extract a string value that may span multiple lines.
    Returns (value, end_idx)."""
    value_parts = []
    i = start_idx
    while i < len(lines):
        line = lines[i].strip()
        # Check if we have a complete "..." or `...` value
        if line.startswith('"'):
            # Find the closing quote
            rest = line[1:]
            if '"' in rest and not rest.startswith('"'):
                # Single line: "value",
                end = rest.index('"')
                value_parts.append(rest[:end])
                return ' '.join(value_parts), i + 1
            else:
                # Multi-line string
                value_parts.append(rest)
        elif line.startswith('`'):
            rest = line[1:]
            value_parts.append(rest)
        elif line.endswith('"') and not line.endswith(',"'):
            # End of a multi-line string value
            val = line[:-1] if line.endswith('"') else line
            value_parts.append(val)
            return ' '.join(value_parts), i + 1
        elif line.endswith('",') or line.endswith('`,'):
            # End of value with comma
            val = line[:-2] if line.endswith('",') else line[:-1]
            value_parts.append(val)
            return ' '.join(value_parts), i + 1
        elif line == ',' or line == '':
            # Skip separator lines
            i += 1
            continue
        elif line.startswith('}') or line.startswith('const') or line == '];':
            return ' '.join(value_parts), i
        else:
            # Content line
            value_parts.append(line)
        i += 1
    return ' '.join(value_parts), i


def parse_posts(filepath):
    """Parse data.js to extract all post objects."""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    posts = []
    i = 0
    n = len(lines)
    
    # Find start of posts array
    while i < n and 'const posts = [' not in lines[i]:
        i += 1
    i += 1  # skip past the opening line
    
    current_post = {}
    in_content = False
    content_lines = []
    content_start_line = 0
    
    while i < n:
        line = lines[i]
        stripped = line.strip()
        
        if stripped == '];':
            if current_post and 'slug' in current_post:
                current_post['content'] = '\n'.join(content_lines)
                posts.append(current_post)
            break
        
        if stripped == '{':
            if current_post and 'slug' in current_post:
                posts.append(current_post)
            current_post = {'content': ''}
            content_lines = []
            in_content = False
            i += 1
            continue
        
        # Parse slug field
        slug_match = re.match(r'\s*slug:\s*"([^"]+)"', stripped)
        if slug_match:
            current_post['slug'] = slug_match.group(1)
            i += 1
            continue
        
        # Parse title field (may span multiple lines)
        if stripped.startswith('title:'):
            title_val, new_i = extract_string_value(lines, i + 1)
            if title_val:
                current_post['title'] = title_val.strip()
            i = new_i
            continue
        
        # Parse date field
        date_match = re.match(r'\s*date:\s*"([^"]+)"', stripped)
        if date_match:
            current_post['date'] = date_match.group(1)
            i += 1
            continue
        
        # Parse excerpt field (may span multiple lines)
        if stripped.startswith('excerpt:'):
            excerpt_val, new_i = extract_string_value(lines, i + 1)
            if excerpt_val:
                current_post['excerpt'] = excerpt_val.strip()
            i = new_i
            continue
        
        # Parse tags field
        tags_match = re.match(r'\s*tags:\s*\[(.*)\]', stripped)
        if tags_match:
            tags_str = tags_match.group(1)
            tags = re.findall(r'"([^"]*?)"', tags_str)
            current_post['tags'] = tags
            i += 1
            continue
        
        # Parse imagePlaceholder field
        if stripped.startswith('imagePlaceholder:'):
            i += 1
            continue
        
        # Parse metaTitle and metaDescription
        if stripped.startswith('metaTitle:') or stripped.startswith('metaDescription:'):
            meta_val, new_i = extract_string_value(lines, i + 1)
            if meta_val:
                key = 'metaTitle' if stripped.startswith('metaTitle:') else 'metaDescription'
                current_post[key] = meta_val.strip()
            i = new_i
            continue
        
        if stripped.startswith('dateModified:'):
            i += 1
            continue
        
        # Parse content field
        if stripped.startswith('content:'):
            in_content = True
            content_start = line.index('`') + 1 if '`' in line else -1
            if content_start > 0:
                after_backtick = line[content_start:].strip()
                if after_backtick:
                    content_lines.append(after_backtick)
                # Check if content ends on same line
                if '`,' in after_backtick or after_backtick.strip() == '`':
                    in_content = False
                    content = '\n'.join(content_lines)
                    content = content.replace('`,' , '').replace('`', '')
                    current_post['content'] = content
                    content_lines = []
            i += 1
            continue
        
        if in_content:
            # Check for end of content backtick
            if '`,' in stripped or stripped == '`':
                content_lines.append(stripped.replace('`,', '').replace('`', ''))
                current_post['content'] = '\n'.join(content_lines)
                in_content = False
                content_lines = []
                i += 1
                continue
            
            content_lines.append(stripped)
            i += 1
            continue
        
        # End of post object
        if stripped == '},' or stripped == '}':
            if current_post and 'slug' in current_post:
                if not current_post.get('content'):
                    current_post['content'] = '\n'.join(content_lines)
                posts.append(current_post)
            current_post = {}
            content_lines = []
            in_content = False
            i += 1
            continue
        
        i += 1
    
    # Handle last post
    if current_post and 'slug' in current_post:
        current_post['content'] = '\n'.join(content_lines)
        posts.append(current_post)
    
    return posts


def get_primary_keyword(title):
    """Extract primary keyword from title."""
    if not title:
        return "seo"
    title_lower = title.lower()
    
    # Patterns for extracting the core topic
    patterns = [
        (r'(?:complete|comprehensive)\s+(.+?)(?:\s+for|\s+in|\s+—|$)', 1),
        (r'(.+?)\s+(?:guide|strategies|tips|checklist)(?:\s+for|\s+in|\s+—|$)', 1),
        (r'how to (.+?)(?:\s+in|\s+for|\s+—|:|\s+\d+|$)', 1),
        (r'what does (.+?) actually do', 1),
        (r'why (.+?) (?:is|delivers)', 1),
        (r'top \d+ (.+?) (?:dhaka|bangladesh)', 1),
        (r'^(.+?)(?:\s+in|\s+for|\s+—|\s*:|$)', 1),
    ]
    
    for pat, group in patterns:
        m = re.search(pat, title_lower)
        if m:
            kw = m.group(group).strip()
            words = kw.split()[:4]
            if len(words) >= 2 or (len(words) == 1 and len(words[0]) > 4):
                return ' '.join(words)
    
    # Fallback: first 3 meaningful words
    stopwords = {'the', 'a', 'an', 'for', 'in', 'to', 'of', 'and', 'is', 'vs', 'how', 'what', 'why', 'when', 'which'}
    words = [w for w in title_lower.split() if w not in stopwords and len(w) > 2]
    return ' '.join(words[:4]) if words else "seo optimization"


def check_tfidf(content, title):
    """Check TF-IDF: keyword occurrence count."""
    keyword = get_primary_keyword(title)
    if not keyword or keyword in ('s', ''):
        return "❌", f"Could not extract meaningful keyword from title: '{title[:50]}'"
    
    content_lower = content.lower()
    
    # Exact phrase match
    phrase_count = content_lower.count(keyword.lower())
    
    # If phrase count is low, check individual significant words
    words = keyword.split()
    if len(words) > 1:
        # Count individual significant words (length > 3)
        significant = [w for w in words if len(w) > 3]
        if significant:
            max_word_count = max(content_lower.count(w) for w in significant)
            count = max(phrase_count, max_word_count)
        else:
            count = phrase_count
    else:
        count = phrase_count
    
    status = "✅" if count >= 5 else "❌"
    return status, f"{count} occurrences of '{keyword}'"


def check_entities(content, title, tags):
    """Check semantic entity coverage."""
    content_lower = content.lower()
    missing = []
    
    # Location entities
    locations = ['dhaka', 'bangladesh']
    found_locs = [l for l in locations if l in content_lower]
    if not found_locs:
        missing.append('dhaka/bangladesh (no location entity)')
    
    # SEO service entity
    service_keywords = ['seo', 'search engine optimization']
    found_services = [s for s in service_keywords if s in content_lower]
    if not found_services:
        missing.append('seo (service entity)')
    
    # Industry-specific entities based on tags
    if tags:
        tag_str = ' '.join(t.lower() for t in tags)
        
        entity_checks = [
            ('garments', ['garment', 'textile', 'apparel', 'rmg']),
            ('ecommerce', ['ecommerce', 'e-commerce', 'online store', 'daraz']),
            ('local seo', ['google business profile', 'google maps', 'local search', 'gmb']),
            ('technical seo', ['technical seo', 'core web vitals', 'page speed', 'crawl']),
            ('link building', ['backlink', 'link building', 'guest post', 'anchor text']),
            ('construction', ['construction', 'cement', 'building material', 'real estate']),
            ('transportation', ['transportation', 'taxi', 'fleet', 'logistics']),
            ('automotive', ['automotive', 'windshield', 'auto repair', 'car']),
            ('locksmith', ['locksmith', 'lock', 'security', 'key']),
            ('smm panel', ['smm panel', 'social media marketing', 'panel']),
            ('case study', ['case study', 'traffic', 'rankings', 'organic', 'visitors']),
            ('b2b', ['b2b', 'manufacturing', 'industrial', 'wholesale']),
            ('ai seo', ['ai search', 'generative engine optimization', 'geo', 'aeo', 'chatgpt']),
            ('real estate', ['real estate', 'property', 'developer', 'housing']),
        ]
        
        for entity_name, keywords in entity_checks:
            # Check if any tag relates to this entity
            if any(kw in tag_str for kw in entity_name.split()):
                found_entity = any(k in content_lower for k in keywords)
                if not found_entity:
                    # Don't flag if the entity is too specific and content is a general guide
                    missing.append(f'{entity_name} (no entity mention)')
    
    status = "✅" if not missing else "❌"
    return status, missing


def check_pillar_cluster(tags, content, title):
    """Check pillar-cluster alignment."""
    if not tags:
        return "❌", "No tags defined"
    
    tag_str = ' '.join(t.lower() for t in tags)
    content_lower = content.lower()
    
    pillar_map = {
        'local-seo': ['local seo', 'google business profile', 'google maps', 'local search'],
        'technical-seo': ['technical seo', 'core web vitals', 'page speed', 'crawlability'],
        'on-page-seo': ['on-page seo', 'content optimization', 'meta tags'],
        'seo-guide': ['seo guide', 'seo strategy', 'complete seo'],
        'link-building': ['link building', 'backlink', 'guest post', 'link building strategy'],
        'ecommerce-seo': ['ecommerce', 'e-commerce', 'online store', 'daraz'],
        'geo-aeo': ['geo', 'aeo', 'ai search', 'generative engine', 'ai overview'],
        'case-study': ['case study', 'case studies', 'results'],
        'seo-services': ['seo service', 'seo expert', 'seo specialist', 'seo agency'],
    }
    
    matched_pillar = None
    for pillar, keywords in pillar_map.items():
        if any(kw in tag_str or kw in content_lower for kw in keywords):
            matched_pillar = pillar
            break
    
    if not matched_pillar:
        return "❌", "Could not determine pillar topic"
    
    pillar_urls = {
        'local-seo': ['/services/local-seo'],
        'technical-seo': ['/services/technical-seo'],
        'on-page-seo': ['/services/on-page-seo'],
        'seo-guide': ['/blog/complete-seo-guide-bangladesh-businesses-2026'],
        'link-building': ['/blog/link-building-strategies-bangladesh-market'],
        'ecommerce-seo': ['/services/ecommerce-seo'],
        'geo-aeo': ['/blog/geo-optimization-prepare-business-ai-search'],
        'case-study': ['/blog', '/services/'],
        'seo-services': ['/services/', '/'],
    }
    
    urls = pillar_urls.get(matched_pillar, ['/'])
    links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
    link_urls = [l[1] for l in links]
    
    found_urls = [u for u in urls if any(u in lu for lu in link_urls)]
    
    if found_urls:
        status = "✅"
        details = f"Pillar link found: {found_urls[0]}"
    else:
        status = "❌"
        details = f"No pillar link. Expected URL pattern: {urls[0]} for topic '{matched_pillar}'"
    
    return status, details


def check_aeo_geo(content):
    """Check AEO/GEO optimization: count question-based headings."""
    headings = re.findall(r'^#{1,4}\s+(.+)$', content, re.MULTILINE)
    
    question_words = ['How', 'What', 'Why', 'When', 'Where', 'Can', 'Do', 'Is', 'Are', 'Which', 'Who', 'Does']
    question_headings = []
    seen = set()
    
    for h in headings:
        h_stripped = h.strip()
        if h_stripped in seen:
            continue
        seen.add(h_stripped)
        for qw in question_words:
            if h_stripped.startswith(qw + ' ') or h_stripped.startswith(qw + ':'):
                question_headings.append(h_stripped)
                break
    
    count = len(question_headings)
    status = "✅" if count >= 2 else "❌"
    return status, f"{count} question headings"


def check_internal_links(content):
    """Count internal links."""
    links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
    
    seen_urls = set()
    for text, url in links:
        # Skip external and non-http links
        if url.startswith('http') and 'kanokmiah.com.bd' not in url and not url.startswith('/'):
            continue
        if url.startswith('#') or url.startswith('mailto:') or url.startswith('tel:'):
            continue
        
        # Normalize
        clean_url = url.split('?')[0].split('#')[0].rstrip('/')
        if clean_url.startswith('http'):
            # Extract path
            from urllib.parse import urlparse
            parsed = urlparse(url)
            clean_url = parsed.path.rstrip('/')
        
        if clean_url:
            seen_urls.add(clean_url)
    
    count = len(seen_urls)
    status = "✅" if count >= 3 else "❌"
    return status, f"{count} unique internal link URLs"


def check_schema(post):
    """Check if post has title, excerpt, date."""
    missing_fields = []
    if not post.get('title'):
        missing_fields.append('title')
    if not post.get('excerpt'):
        missing_fields.append('excerpt')
    if not post.get('date'):
        missing_fields.append('date')
    
    status = "✅" if not missing_fields else "❌"
    details = "title ✓, excerpt ✓, date ✓" if not missing_fields else f"Missing: {', '.join(missing_fields)}"
    return status, details


def main():
    posts = parse_posts(DATA_FILE)
    print(f"Parsed {len(posts)} total posts", file=sys.stderr)
    
    post_map = {p['slug']: p for p in posts if 'slug' in p}
    
    found_slugs = [s for s in MODIFIED_SLUGS if s in post_map]
    not_found = [s for s in MODIFIED_SLUGS if s not in post_map]
    if not_found:
        print(f"WARNING: Not found: {not_found}", file=sys.stderr)
    
    # Print report markdown
    total_checks = 0
    passed_checks = 0
    
    for slug in found_slugs:
        post = post_map[slug]
        title = post.get('title', 'Untitled')
        content = post.get('content', '')
        tags = post.get('tags', [])
        
        checks = {
            'TF-IDF': check_tfidf(content, title),
            'Entities': check_entities(content, title, tags),
            'Pillar Link': check_pillar_cluster(tags, content, title),
            'AEO/GEO': check_aeo_geo(content),
            'Internal Links': check_internal_links(content),
            'Schema Ready': check_schema(post),
        }
        
        has_failures = any(v[0] == '❌' for v in checks.values())
        status_icon = "⚠️" if has_failures else "✅"
        
        print(f"\n## {status_icon} Post: {slug}")
        print(f"**Title:** {title}")
        print(f"**Tags:** {', '.join(tags) if tags else '(none)'}")
        print(f"**Last Change:** Modified in last 48h (heading fix / internal link update)")
        print()
        print("| Check | Status | Details |")
        print("|-------|--------|---------|")
        
        for check_name, (status, details) in checks.items():
            total_checks += 1
            if status == '✅':
                passed_checks += 1
            
            if isinstance(details, list):
                d_str = ', '.join(details[:5]) if details else 'All entities present'
            else:
                d_str = str(details)
            
            print(f"| {check_name} | {status} | {d_str} |")
        
        if has_failures:
            print()
            print("### 🔧 Fix instructions:")
            for check_name, (status, details) in checks.items():
                if status == '❌':
                    if check_name == 'TF-IDF':
                        keyword = get_primary_keyword(title)
                        print(f"- **TF-IDF**: Increase keyword density. Add more natural mentions of '{keyword}' in headings and body text.")
                    elif check_name == 'Entities':
                        missing = details if isinstance(details, list) else [details]
                        print(f"- **Entity Coverage**: Add missing entities: {', '.join(missing[:5])}")
                    elif check_name == 'Pillar Link':
                        print(f"- **Pillar Link**: {details}")
                    elif check_name == 'AEO/GEO':
                        print(f"- **AEO/GEO**: Add more question-based headings (How, What, Why). {details}")
                    elif check_name == 'Internal Links':
                        print(f"- **Internal Links**: {details}")
                    elif check_name == 'Schema Ready':
                        print(f"- **Schema**: {details}")
    
    print(f"\n{'='*60}")
    print(f"## 📊 Framework Check Summary")
    print(f"- **Posts checked:** {len(found_slugs)}")
    print(f"- **Total checks:** {total_checks}")
    print(f"- **Passed:** {passed_checks}")
    print(f"- **Failed:** {total_checks - passed_checks}")
    
    if passed_checks == total_checks:
        print(f"\n✅ **All checks passed!** Content framework is properly enforced.")
    else:
        print(f"\n⚠️ **{total_checks - passed_checks} check(s) failed across {len(found_slugs)} posts.** See above for detailed fix instructions.")


if __name__ == '__main__':
    main()
