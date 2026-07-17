#!/usr/bin/env python3
"""
Framework checker for kanokmiah.com.bd blog posts.
Reads data.js, extracts all posts, and runs 6 checks on each.
"""
import re
import json
import subprocess
import sys
from datetime import datetime, timezone, timedelta

# File paths
DATA_JS = "/root/kanok-miahit/src/app/blog/data.js"

def parse_posts(data_js):
    """Parse blog posts from data.js - extracts slug, title, date, tags, content, excerpt."""
    with open(data_js, 'r', encoding='utf-8') as f:
        content = f.read()
    
    posts = []
    
    # Find all post objects using regex
    # Each post starts with { slug: "...", and ends with }, or }, (except last)
    # We'll use a simpler approach by finding slug/title/date/excerpt/tags/content blocks
    
    # Split by "slug:" to find individual posts
    blocks = content.split("slug: ")
    
    for i, block in enumerate(blocks[1:], 1):  # skip first split part
        try:
            # Extract slug
            slug_match = re.search(r'"([^"]+)"', block)
            if not slug_match:
                continue
            slug = slug_match.group(1)
            
            # Extract date
            date_match = re.search(r'date:\s*"([^"]+)"', block)
            date_str = date_match.group(1) if date_match else "unknown"
            
            # Extract title
            title_match = re.search(r'title:\s*"([^"]+)"', block)
            title = title_match.group(1) if title_match else "unknown"
            
            # Extract author
            author_match = re.search(r'author:\s*"([^"]+)"', block)
            author = author_match.group(1) if author_match else "unknown"
            
            # Extract excerpt
            excerpt_match = re.search(r'excerpt:\s*\n?\s*"([^"]+)"', block)
            excerpt = excerpt_match.group(1) if excerpt_match else ""
            
            # Extract tags array
            tags_match = re.search(r'tags:\s*\[(.*?)\]', block, re.DOTALL)
            tags = []
            if tags_match:
                tags_str = tags_match.group(1)
                tags = re.findall(r'"([^"]+)"', tags_str)
            
            # Extract dateModified
            dm_match = re.search(r'dateModified:\s*"([^"]+)"', block)
            date_modified = dm_match.group(1) if dm_match else None
            
            # Extract content
            content_match = re.search(r'content:\s*`(.*?)`\s*,?\s*\}', block, re.DOTALL)
            content_text = content_match.group(1).strip() if content_match else ""
            
            posts.append({
                'slug': slug,
                'title': title,
                'date': date_str,
                'author': author,
                'excerpt': excerpt,
                'tags': tags,
                'dateModified': date_modified,
                'content': content_text
            })
        except Exception as e:
            print(f"Warning: Error parsing post block {i}: {e}", file=sys.stderr)
            continue
    
    return posts


def extract_keyword(title):
    """Extract primary keyword from title (first meaningful noun phrase)."""
    # Clean title
    title_clean = title.lower()
    
    # Remove common prefixes
    title_clean = re.sub(r'^(why|what|how|is|are|do|does|the|a|an|your|our|complete|ultimate|best|top) ', '', title_clean)
    
    # Get first meaningful chunk
    # Remove trailing description after - or : or —
    title_clean = re.split(r'[—–\-:|]', title_clean)[0].strip()
    
    # Remove blog-related words at end
    title_clean = re.sub(r'\s+(in|for|of|to|at|on|with)\s+\d{4}.*$', '', title_clean)
    
    # Get the main noun phrase by taking first 2-4 meaningful words
    words = [w for w in title_clean.split() if len(w) > 2]
    
    if not words:
        words = title_clean.split()[:4]
    
    if len(words) >= 3:
        keyword = ' '.join(words[:3])
    elif len(words) >= 2:
        keyword = ' '.join(words[:2])
    else:
        keyword = words[0] if words else title_clean
    
    return keyword


def check_tfidf(post):
    """Check TF-IDF coverage - primary keyword occurrence count."""
    keyword = extract_keyword(post['title'])
    content_lower = post['content'].lower()
    keyword_lower = keyword.lower()
    
    # Count occurrences of the keyword in content
    count = content_lower.count(keyword_lower)
    
    # Also check for base form
    # e.g., "SEO Guide" → also count "SEO guides"
    base_words = keyword_lower.split()
    if len(base_words) > 1:
        for i, w in enumerate(base_words):
            alt_count = content_lower.count(w)
            if alt_count > count:
                count = alt_count  # use the most common word form
    
    passed = count >= 5
    return {
        'keyword': keyword,
        'count': count,
        'passed': passed,
        'details': f"'{keyword}' found {count} times"
    }


# Key entities that should be present
REQUIRED_ENTITIES_MAP = {
    'location': ['dhaka', 'bangladesh', 'chittagong', 'sylhet'],
    'service': ['seo', 'digital marketing', 'search engine optimization', 'content marketing', 'local seo', 'technical seo'],
    'industry': ['ecommerce', 'real estate', 'healthcare', 'restaurant', 'garment', 'education'],
}

def check_entities(post):
    """Check semantic entity coverage."""
    content_lower = post['content'].lower()
    
    found_locations = []
    missing_locations = []
    
    for loc in ['dhaka', 'bangladesh', 'chittagong', 'sylhet']:
        if loc in content_lower:
            found_locations.append(loc.title())
        else:
            missing_locations.append(loc.title())
    
    found_services = []
    missing_services = []
    
    for svc in ['seo', 'digital marketing', 'content marketing', 'local seo', 'technical seo']:
        if svc.lower() in content_lower:
            found_services.append(svc.title() if ' ' not in svc else svc.title())
    
    # Check for at least some location and at least some service mention
    location_ok = len(found_locations) >= 1
    
    return {
        'found_locations': found_locations,
        'missing_locations': [l for l in ['Dhaka', 'Bangladesh', 'Chittagong', 'Sylhet'] if l.lower() not in content_lower],
        'location_ok': location_ok,
        'passed': location_ok,
        'details': f"Locations found: {', '.join(found_locations) if found_locations else 'none'} | Missing: {', '.join(missing_locations) if missing_locations else 'none'}"
    }


def check_pillar_link(post):
    """Check if post links to a pillar page based on its tags."""
    content_lower = post['content'].lower()
    tags = [t.lower() for t in post['tags']]
    
    # Define pillar pages per tag
    pillar_map = {
        'local seo': '/services/local-seo',
        'technical seo': '/services/technical-seo',
        'e-commerce seo': '/services/ecommerce-seo',
        'ecommerce seo': '/services/ecommerce-seo',
        'on-page seo': '/services/on-page-seo',
        'semantic seo': '/services/semantic-seo',
        'geo': '/services/geo-ai-search',
        'generative engine optimization': '/services/geo-ai-search',
        'link building': '/services/link-building',
        'seo guide': '/blog/complete-seo-guide-bangladesh-businesses-2026',
        'bangladesh seo': '/blog/complete-seo-guide-bangladesh-businesses-2026',
    }
    
    # Also check content for service page links and pillar blog links
    service_pages = [
        '/services/local-seo',
        '/services/technical-seo', 
        '/services/ecommerce-seo',
        '/services/on-page-seo',
        '/services/semantic-seo',
        '/services/geo-ai-search',
        '/services/link-building',
    ]
    
    pillar_blog = '/blog/complete-seo-guide-bangladesh-businesses-2026'
    
    found_links = []
    for sp in service_pages:
        if sp in content_lower:
            found_links.append(sp)
    
    if pillar_blog in content_lower:
        found_links.append(pillar_blog)
    
    passed = len(found_links) >= 1
    
    return {
        'passed': passed,
        'found_links': found_links,
        'details': f"Links to: {', '.join(found_links) if found_links else 'NO pillar/service links found'}"
    }


def check_aeo_geo(post):
    """Count question-based headings for AEO/GEO optimization."""
    content = post['content']
    
    question_heading_pattern = re.compile(
        r'^#{2,6}\s+(How|What|Why|When|Where|Can|Do|Is|Are|Does|Should|Which)\b.*\?',
        re.MULTILINE | re.IGNORECASE
    )
    
    matches = question_heading_pattern.findall(content)
    
    # Also count question headings
    all_q_headings = re.findall(
        r'^#{2,6}\s+(?:How|What|Why|When|Where|Can|Do|Is|Are|Does|Should|Which)\b[^\n]*\?',
        content, re.MULTILINE | re.IGNORECASE
    )
    
    count = len(all_q_headings)
    passed = count >= 2
    
    return {
        'count': count,
        'passed': passed,
        'details': f"{count} question-based heading(s) found"
    }


def check_internal_linking(post):
    """Count internal links in the post."""
    content = post['content']
    
    # Match markdown links starting with /
    internal_links = re.findall(r'\[([^\]]+)\]\((/[^)]+)\)', content)
    
    count = len(internal_links)
    passed = count >= 3
    
    links_list = []
    for text, url in internal_links:
        links_list.append(f"[{text}]({url})")
    
    return {
        'count': count,
        'passed': passed,
        'details': f"{count} internal link(s) found",
        'links': links_list[:10]  # first 10 links
    }


def check_schema(post):
    """Check if post has all fields needed for ArticleSchema."""
    # Check title, excerpt, date, author
    has_title = post['title'] and post['title'] != 'unknown'
    has_excerpt = len(post['excerpt']) > 20
    has_date = post['date'] != 'unknown'
    has_author = post['author'] != 'unknown'
    has_date_modified = post['dateModified'] is not None
    
    missing = []
    if not has_title:
        missing.append('title')
    if not has_excerpt:
        missing.append('excerpt')
    if not has_date:
        missing.append('date')
    if not has_author:
        missing.append('author')
    if not has_date_modified:
        missing.append('dateModified')
    
    passed = len(missing) == 0
    return {
        'passed': passed,
        'missing': missing,
        'details': f"All fields set" if passed else f"Missing: {', '.join(missing)}"
    }


def get_modified_slugs_since(hours=48):
    """Get list of post slugs modified in the last N hours using git log."""
    result = subprocess.run(
        ['git', 'log', '--oneline', f'--since="{hours} hours ago"', '--', DATA_JS],
        capture_output=True, text=True, cwd='/root/kanok-miahit'
    )
    
    if not result.stdout.strip():
        return []
    
    # Read current data.js to get all slugs
    with open(DATA_JS, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract all slugs
    slugs = re.findall(r'slug:\s*"([^"]+)"', content)
    return slugs


def main():
    print("# Content Framework Enforcement Report")
    print(f"**Generated:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"**Project:** kanokmiah.com.bd")
    print()
    
    # Step 1: Check git for changes
    result = subprocess.run(
        ['git', 'log', '--oneline', '--since="48 hours ago"', '--', DATA_JS],
        capture_output=True, text=True, cwd='/root/kanok-miahit'
    )
    
    if not result.stdout.strip():
        print("✅ No new/modified posts — framework check skipped.")
        return
    
    changes = result.stdout.strip().split('\n')
    print(f"**Commits touching data.js in last 48h:** {len(changes)}")
    print()
    
    # Parse all posts
    posts = parse_posts(DATA_JS)
    print(f"**Total posts parsed:** {len(posts)}")
    print()
    
    if not posts:
        print("❌ ERROR: Could not parse any posts from data.js")
        return
    
    # Run checks on all posts (they were all modified)
    all_passed = True
    
    for post in posts:
        slug = post['slug']
        print(f"## Post: {slug}")
        print(f"### Title: {post['title']}")
        print()
        print(f"| Check | Status | Details |")
        print(f"|-------|--------|---------|")
        
        # A. TF-IDF
        tfidf = check_tfidf(post)
        status = "✅" if tfidf['passed'] else "❌"
        if not tfidf['passed']:
            all_passed = False
        print(f"| TF-IDF: `{tfidf['keyword']}` | {status} | {tfidf['count']} occurrence(s) |")
        
        # B. Entities
        entities = check_entities(post)
        status = "✅" if entities['passed'] else "❌"
        if not entities['passed']:
            all_passed = False
        print(f"| Entities | {status} | {entities['details']} |")
        
        # C. Pillar Link
        pillar = check_pillar_link(post)
        status = "✅" if pillar['passed'] else "❌"
        if not pillar['passed']:
            all_passed = False
        print(f"| Pillar Link | {status} | {pillar['details']} |")
        
        # D. AEO/GEO
        aeo = check_aeo_geo(post)
        status = "✅" if aeo['passed'] else "❌"
        if not aeo['passed']:
            all_passed = False
        print(f"| AEO/GEO | {status} | {aeo['details']} |")
        
        # E. Internal Links
        il = check_internal_linking(post)
        status = "✅" if il['passed'] else "❌"
        if not il['passed']:
            all_passed = False
        print(f"| Internal Links | {status} | {il['details']} |")
        
        # F. Schema
        schema = check_schema(post)
        status = "✅" if schema['passed'] else "❌"
        if not schema['passed']:
            all_passed = False
        print(f"| Schema Ready | {status} | {schema['details']} |")
        
        # Fix instructions
        fixes = []
        if not tfidf['passed']:
            fixes.append(f"- **TF-IDF too thin:** Add more occurrences of `{tfidf['keyword']}` — aim for at least 5 in the content body.")
        if not entities['passed']:
            missing_ents = entities.get('missing_locations', [])
            if missing_ents:
                fixes.append(f"- **Missing entities:** Add mentions of: {', '.join(missing_ents[:3])}")
        if not pillar['passed']:
            fixes.append("- **Pillar link missing:** Add link to relevant service page (e.g., /services/local-seo, /services/technical-seo) or the pillar guide.")
        if not aeo['passed']:
            fixes.append(f"- **Too few question headings:** Add 1-2 more FAQ or how-to sections starting with How/What/Why/Can/Do/Is/Are.")
        if not il['passed']:
            fixes.append(f"- **Not enough internal links:** Add 2-3 more cross-links to other blog posts, service pages, or location pages.")
        if not schema['passed']:
            fixes.append(f"- **Schema data incomplete:** Add missing fields: {', '.join(schema['missing'])}")
        
        if fixes:
            print(f"\n### ⚠️ Fix instructions:")
            for f in fixes:
                print(f)
        else:
            print(f"\n### ✅ All checks passed — no fixes needed.")
        
        print()
    
    # Summary
    print("---")
    print(f"## Summary")
    if all_passed:
        print("✅ All posts pass all framework checks.")
    else:
        print("❌ Some posts need attention. See individual post sections above for details.")


if __name__ == '__main__':
    main()
