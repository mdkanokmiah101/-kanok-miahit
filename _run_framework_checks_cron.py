#!/usr/bin/env python3
"""
Framework enforcement checker for kanokmiah.com.bd blog posts.
Reads data.js, extracts posts, runs 6 framework checks.
"""
import re
import json
import sys
from collections import Counter

DATA_FILE = "src/app/blog/data.js"

# Slug list from git diff HEAD~2 HEAD -- src/app/blog/data.js analysis
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

def parse_posts(filepath):
    """Parse data.js to extract all post objects."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    posts = []
    # Find each post object: { slug: "...", title: "...", ... content: `...` },
    # Use a more robust approach: split by slug: pattern
    lines = content.split('\n')
    
    current_post = None
    in_content = False
    content_lines = []
    brace_depth = 0
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        if stripped == 'const posts = [':
            continue
        
        if stripped == '];' and brace_depth == 0:
            if current_post:
                current_post['content'] = '\n'.join(content_lines)
                posts.append(current_post)
            break
        
        if current_post is None and stripped.startswith('{'):
            current_post = {}
            content_lines = []
            in_content = False
        
        if current_post is not None:
            slug_match = re.match(r'\s*slug:\s*"([^"]+)"', line)
            if slug_match:
                current_post['slug'] = slug_match.group(1)
                continue
            
            title_match = re.match(r'\s*title:\s*"([^"]+)"', line)
            if title_match:
                current_post['title'] = title_match.group(1)
                continue
            
            date_match = re.match(r'\s*date:\s*"([^"]+)"', line)
            if date_match:
                current_post['date'] = date_match.group(1)
                continue
            
            excerpt_match = re.match(r'\s*excerpt:\s*$', line)
            if excerpt_match:
                # excerpt is on next lines
                current_post['excerpt'] = ''
                continue
            
            if 'excerpt' in current_post and isinstance(current_post['excerpt'], str):
                excerpt_val = re.match(r'\s*"([^"]+)"', stripped)
                if excerpt_val and current_post['excerpt'] == '':
                    current_post['excerpt'] = excerpt_val.group(1)
                    continue
                elif excerpt_val and current_post['excerpt'] != '':
                    # Already got excerpt, move on
                    pass
            
            tags_match = re.match(r'\s*tags:\s*\[(.*?)\]', line)
            if tags_match:
                tags_str = tags_match.group(1)
                tags = re.findall(r'"([^"]+)"', tags_str)
                current_post['tags'] = tags
                continue
            
            content_start = re.match(r'\s*content:\s*`', line)
            if content_start:
                in_content = True
                content_part = line.split('`', 1)[1] if '`' in line else ''
                if content_part:
                    content_lines.append(content_part)
                continue
            
            if in_content:
                if '`,' in line and line.strip().endswith('`,'):
                    content_lines.append(line.replace('`,', '').strip())
                    current_post['content'] = '\n'.join(content_lines)
                    in_content = False
                    content_lines = []
                    continue
                elif stripped == '`,' or stripped == '`':
                    current_post['content'] = '\n'.join(content_lines)
                    in_content = False
                    content_lines = []
                    continue
                else:
                    # Remove trailing , after backtick if present
                    cl = line
                    if '`,' in line:
                        cl = line[:line.index('`,')]
                    content_lines.append(cl)
                    continue
            
            if stripped == '},' or stripped == '}':
                if current_post and 'slug' in current_post:
                    posts.append(current_post)
                current_post = None
                content_lines = []
                in_content = False
    
    return posts


def get_primary_keyword(title):
    """Extract primary keyword from title (first meaningful noun phrase)."""
    # Remove trailing location/qualifiers
    title_lower = title.lower()
    
    # Common patterns to find the core topic
    patterns = [
        r'complete (.+?) for',
        r'(.+?) guide for',
        r'(.+?) strategies for',
        r'(.+?) for bangladesh',
        r'(.+?) for bangladeshi',
        r'(.+?) in bangladesh',
        r'guide to (.+?) for',
        r'how to choose (.+?):',
        r'how to choose (.+?) in',
        r'what does (.+?) do',
        r'why (.+?) is the',
        r'top \d+ (.+?) for',
        r'(.+?) optimization for',
        r'(.+?) optimization guide',
        r'(.+?) for dhaka',
        r'(.+?) — ',
        r'(.+?):',
        r'^(.+?)(?: for| in| —)',
    ]
    
    for pat in patterns:
        m = re.search(pat, title_lower)
        if m:
            kw = m.group(1).strip()
            # Take first 3 words max
            words = kw.split()[:4]
            return ' '.join(words)
    
    # Fallback: take first 3-4 words
    words = title_lower.split()[:4]
    return ' '.join(words)


def check_tfidf(content, title):
    """Check TF-IDF: keyword occurrence count."""
    keyword = get_primary_keyword(title)
    if not keyword:
        return None, "could not extract keyword"
    
    content_lower = content.lower()
    count = content_lower.count(keyword.lower())
    
    # Also check individual word matches
    words = keyword.split()
    if len(words) > 1:
        # Count how many times the full phrase appears
        phrase_count = count
        # Also check individual significant words
        significant_words = [w for w in words if len(w) > 3]
        for w in significant_words:
            word_count = content_lower.count(w)
            if word_count >= 5:
                phrase_count = max(phrase_count, word_count)
        count = phrase_count
    
    status = "✅" if count >= 5 else "❌"
    return status, f"{count} occurrences of '{keyword}'"


def check_entities(content, title, tags):
    """Check semantic entity coverage."""
    content_lower = content.lower()
    missing = []
    
    # Location entities
    locations = ['dhaka', 'bangladesh']
    if any(loc in title.lower() or any(loc in t.lower() for t in tags) for loc in locations):
        for loc in locations:
            if loc not in content_lower:
                missing.append(loc)
    else:
        # Check if locations are in content at all
        found_locs = [l for l in locations if l in content_lower]
        if not found_locs:
            missing.append('dhaka/bangladesh (no location entity)')
    
    # Service type entities
    service_keywords = ['seo', 'search engine optimization', 'search engine']
    found_services = [s for s in service_keywords if s in content_lower]
    if not found_services:
        missing.append('seo (primary service)')
    
    # Industry entities based on tags
    industry_map = {
        'ecommerce': ['ecommerce', 'e-commerce', 'online store', 'daraz'],
        'local seo': ['local business', 'local search', 'google maps', 'gmb'],
        'technical seo': ['technical seo', 'core web vitals', 'page speed'],
        'link building': ['backlink', 'link building', 'guest post'],
        'garments': ['garment', 'textile', 'apparel', 'readymade'],
        'real estate': ['real estate', 'property', 'developer'],
        'healthcare': ['healthcare', 'medical', 'clinic', 'hospital', 'doctor'],
        'case study': ['case study', 'results', 'traffic', 'rankings'],
    }
    
    tag_lower = [t.lower() for t in (tags or [])]
    for industry, keywords in industry_map.items():
        if any(ind in ' '.join(tag_lower) for ind in industry.split()):
            found = [k for k in keywords if k in content_lower]
            if not found:
                missing.append(f'{industry} (no industry entity)')
    
    # Expert/authority entities
    if 'kanok' in content_lower or 'kanok miah' in content_lower:
        pass  # Authority entity present
    else:
        # Check if it's a case study about someone else
        if 'seo case study' in title.lower() or 'case study' in title.lower():
            pass  # Case studies may not mention the author
        else:
            missing.append('kanok miah (authority entity)')
    
    status = "✅" if not missing else "❌"
    return status, missing


def check_pillar_cluster(tags, content, title):
    """Check pillar-cluster alignment."""
    if not tags:
        return "❌", "No tags defined"
    
    tag_lower = [t.lower() for t in tags]
    tag_str = ' '.join(tag_lower)
    content_lower = content.lower()
    
    # Map tags to pillar topics
    pillar_map = {
        'local-seo': ['local seo', 'google business profile', 'google maps', 'local search'],
        'technical-seo': ['technical seo', 'core web vitals', 'page speed', 'crawl'],
        'on-page-seo': ['on-page seo', 'content optimization', 'meta'],
        'seo-guide': ['seo guide', 'seo strategy', 'complete seo'],
        'link-building': ['link building', 'backlink', 'guest post'],
        'ecommerce-seo': ['ecommerce', 'e-commerce', 'online store'],
        'geo-aeo': ['geo', 'aeo', 'ai search', 'generative engine'],
        'case-study': ['case study', 'case studies'],
        'seo-services': ['seo services', 'seo expert', 'seo agency'],
    }
    
    matched_pillar = None
    for pillar, keywords in pillar_map.items():
        if any(kw in tag_str for kw in keywords):
            matched_pillar = pillar
            break
    
    if not matched_pillar:
        # Try matching by content
        for pillar, keywords in pillar_map.items():
            if any(kw in content_lower for kw in keywords):
                matched_pillar = pillar
                break
    
    if not matched_pillar:
        return "❌", "Could not determine pillar topic from tags or content"
    
    # Check for pillar page links
    pillar_urls = {
        'local-seo': ['/services/local-seo', '/locations/'],
        'technical-seo': ['/services/technical-seo'],
        'on-page-seo': ['/services/on-page-seo'],
        'seo-guide': ['/blog/complete-seo-guide-bangladesh-businesses-2026'],
        'link-building': ['/blog/link-building-strategies-bangladesh-market'],
        'ecommerce-seo': ['/services/ecommerce-seo'],
        'geo-aeo': ['/blog/geo-optimization-prepare-business-ai-search'],
        'case-study': ['/blog', '/portfolio', '/case-studies'],
        'seo-services': ['/services/', '/'],
    }
    
    urls = pillar_urls.get(matched_pillar, ['/'])
    has_link = any(url in content for url in urls)
    
    # Also check markdown links
    links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
    link_urls = [l[1] for l in links]
    
    found_urls = [u for u in urls if any(u in lu for lu in link_urls)]
    
    if found_urls:
        status = "✅"
        details = f"Links to pillar page: {found_urls[0]}"
    else:
        status = "❌"
        details = f"No link to pillar topic '{matched_pillar}' pages: {urls}"
    
    return status, details


def check_aeo_geo(content):
    """Check AEO/GEO optimization: count question-based headings."""
    # Find all headings
    headings = re.findall(r'^#{1,4}\s+(.+)$', content, re.MULTILINE)
    
    question_words = ['How', 'What', 'Why', 'When', 'Where', 'Can', 'Do', 'Is', 'Are', 'Which', 'Who', 'Does']
    question_headings = []
    
    for h in headings:
        h_stripped = h.strip()
        for qw in question_words:
            if h_stripped.startswith(qw + ' ') or h_stripped.startswith(qw + ':'):
                question_headings.append(h_stripped)
                break
    
    count = len(question_headings)
    status = "✅" if count >= 2 else "❌"
    return status, f"{count} question headings: {question_headings[:5]}"


def check_internal_links(content):
    """Count internal links to other posts, services, locations."""
    links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
    
    internal_links = []
    for text, url in links:
        # Skip external links
        if url.startswith('http') and 'kanokmiah.com.bd' not in url:
            continue
        # Skip anchor-only links
        if url.startswith('#'):
            continue
        # Skip mailto
        if url.startswith('mailto:'):
            continue
        # Skip telephone
        if url.startswith('tel:'):
            continue
        
        # Count as internal if it starts with / or is a relative path
        if url.startswith('/') or 'kanokmiah.com.bd' in url:
            internal_links.append((text, url))
    
    # Deduplicate by URL
    seen_urls = set()
    unique_links = []
    for text, url in internal_links:
        if url not in seen_urls:
            seen_urls.add(url)
            unique_links.append((text, url))
    
    count = len(unique_links)
    status = "✅" if count >= 3 else "❌"
    return status, f"{count} internal links (unique URLs)"


def check_schema(post):
    """Check if post has title, excerpt, date (needed for ArticleSchema)."""
    missing_fields = []
    
    if not post.get('title'):
        missing_fields.append('title')
    if not post.get('excerpt'):
        missing_fields.append('excerpt')
    if not post.get('date'):
        missing_fields.append('date')
    
    # Check for metaTitle and metaDescription
    # These are outside the standard fields but nice to have
    # We can't easily extract them from our parsed post
    
    status = "✅" if not missing_fields else "❌"
    details = "All fields set (title ✓, excerpt ✓, date ✓)" if not missing_fields else f"Missing: {', '.join(missing_fields)}"
    return status, details


def main():
    posts = parse_posts(DATA_FILE)
    print(f"Parsed {len(posts)} total posts from data.js", file=sys.stderr)
    
    # Build slug->post map
    post_map = {p['slug']: p for p in posts if 'slug' in p}
    
    # Check which modified slugs exist
    found_slugs = [s for s in MODIFIED_SLUGS if s in post_map]
    not_found = [s for s in MODIFIED_SLUGS if s not in post_map]
    
    if not_found:
        print(f"WARNING: Could not find posts: {not_found}", file=sys.stderr)
    
    # Run checks on each modified post
    results = {}
    for slug in found_slugs:
        post = post_map[slug]
        title = post.get('title', 'Untitled')
        content = post.get('content', '')
        tags = post.get('tags', [])
        
        print(f"\n{'='*60}", file=sys.stderr)
        print(f"Checking: {slug} | {title}", file=sys.stderr)
        
        checks = {}
        
        # A. TF-IDF
        checks['TF-IDF'] = check_tfidf(content, title)
        
        # B. Entities
        checks['Entities'] = check_entities(content, title, tags)
        
        # C. Pillar-Cluster
        checks['Pillar Link'] = check_pillar_cluster(tags, content, title)
        
        # D. AEO/GEO
        checks['AEO/GEO'] = check_aeo_geo(content)
        
        # E. Internal Links
        checks['Internal Links'] = check_internal_links(content)
        
        # F. Schema
        checks['Schema Ready'] = check_schema(post)
        
        results[slug] = {
            'title': title,
            'checks': checks,
            'tags': tags,
        }
        
        print(f"  TF-IDF: {checks['TF-IDF'][0]} {checks['TF-IDF'][1]}", file=sys.stderr)
        print(f"  Entities: {checks['Entities'][0]} {checks['Entities'][1]}", file=sys.stderr)
        print(f"  Pillar: {checks['Pillar Link'][0]} {checks['Pillar Link'][1]}", file=sys.stderr)
        print(f"  AEO/GEO: {checks['AEO/GEO'][0]} {checks['AEO/GEO'][1]}", file=sys.stderr)
        print(f"  Internal Links: {checks['Internal Links'][0]} {checks['Internal Links'][1]}", file=sys.stderr)
        print(f"  Schema: {checks['Schema Ready'][0]} {checks['Schema Ready'][1]}", file=sys.stderr)
    
    # Print markdown report
    print_report(results)


def print_report(results):
    """Generate markdown report."""
    total_checks = 0
    passed_checks = 0
    
    for slug, data in results.items():
        title = data['title']
        checks = data['checks']
        
        has_failures = any(v[0] == '❌' for v in checks.values())
        status_icon = "⚠️" if has_failures else "✅"
        
        print(f"\n## {status_icon} Post: {slug}")
        print(f"**Title:** {title}")
        print(f"**Tags:** {', '.join(data.get('tags', []))}")
        print()
        print("| Check | Status | Details |")
        print("|-------|--------|---------|")
        
        for check_name, (status, details) in checks.items():
            total_checks += 1
            if status == '✅':
                passed_checks += 1
            
            if isinstance(details, list):
                if details:
                    details_str = ', '.join(details[:5])
                else:
                    details_str = 'All entities present'
            else:
                details_str = str(details)
            
            print(f"| {check_name} | {status} | {details_str} |")
        
        if has_failures:
            print()
            print("### 🔧 Fix instructions:")
            for check_name, (status, details) in checks.items():
                if status == '❌':
                    if check_name == 'TF-IDF':
                        print(f"- **TF-IDF**: Increase keyword density. Add more natural occurrences of the primary keyword throughout the post.")
                    elif check_name == 'Entities':
                        missing = details if isinstance(details, list) else [details]
                        print(f"- **Entity Coverage**: Add missing entities: {', '.join(missing[:5])}")
                    elif check_name == 'Pillar Link':
                        print(f"- **Pillar Link**: Add a link to the pillar page. {details}")
                    elif check_name == 'AEO/GEO':
                        print(f"- **AEO/GEO**: Add more question-based headings (How, What, Why, etc.). Currently {details}")
                    elif check_name == 'Internal Links':
                        print(f"- **Internal Links**: Add more internal links (at least 3). Currently {details}")
                    elif check_name == 'Schema Ready':
                        print(f"- **Schema**: {details}")
    
    # Summary
    all_pass = all(v[0] == '✅' for data in results.values() for v in data['checks'].values())
    
    print(f"\n{'='*60}")
    print(f"## 📊 Framework Check Summary")
    print(f"- **Posts checked:** {len(results)}")
    print(f"- **Total checks:** {total_checks}")
    print(f"- **Passed:** {passed_checks}")
    print(f"- **Failed:** {total_checks - passed_checks}")
    
    if all_pass:
        print(f"\n✅ **All checks passed!** Content framework is properly enforced.")
    else:
        print(f"\n⚠️ **Some checks failed.** See above for detailed fix instructions.")


if __name__ == '__main__':
    main()
