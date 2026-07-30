"""
Framework enforcement analysis for modified blog posts.
Performs A-F checks on each modified post.
"""
import re
import json

def parse_posts(filepath):
    """Parse all posts from data.js into a list of dicts."""
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Find each post block
    posts = []
    # Split by '{' that starts a new post (after comma)
    # Simpler: use regex to extract post blocks
    post_blocks = re.finditer(
        r'\{[^{}]*slug:\s*["\']([^"\']+)["\'][^{}]*\}',
        content,
        re.DOTALL
    )
    
    # Actually need a more robust parser. Let's do string-based parsing.
    # Find all slug lines first to locate posts
    slug_positions = []
    for m in re.finditer(r'\bslug:\s*["\']([^"\']+)["\']', content):
        slug_positions.append((m.start(), m.group(1)))
    
    # Now extract each post block from slug to the next slug
    posts = []
    for i, (pos, slug) in enumerate(slug_positions):
        # Find start of this post's object (backtrack to '{')
        start = content.rfind('{', 0, pos)
        
        # Find end: the '}' before the next slug or end of file
        if i + 1 < len(slug_positions):
            next_pos = slug_positions[i + 1][0]
            # Find the '}' that closes this post
            end = content.rfind('}', next_pos - 200, next_pos) + 1
        else:
            # Last post - find the last }
            end = content.rfind('}') + 1
        
        block = content[start:end]
        posts.append({
            'slug': slug,
            'block': block,
            'start_line': content[:start].count('\n') + 1,
            'end_line': content[:end].count('\n') + 1,
        })
    
    return posts, content


def extract_field(block, field_name):
    """Extract a field value from a post block."""
    # Match field_name: "value" or field_name: `value`
    patterns = [
        rf'{field_name}:\s*["\`]([^"\`]*)["\`]',
        rf'{field_name}:\s*`([^`]*)`',
    ]
    for p in patterns:
        m = re.search(p, block, re.DOTALL)
        if m:
            return m.group(1).strip()
    return None


def extract_content(block):
    """Extract the content field (multi-line template literal)."""
    m = re.search(r'content:\s*`\n(.*?)`\s*[,}}]', block, re.DOTALL)
    if m:
        return m.group(1)
    return ''


def check_tfidf(title, content):
    """Check keyword coverage - extract primary keyword from title."""
    # Extract first meaningful noun phrase from title
    # Remove common words and take first significant word(s)
    stop_words = {'a', 'an', 'the', 'for', 'in', 'of', 'to', 'and', 'is', 'are', 
                  'how', 'what', 'why', 'when', 'where', 'which', 'can', 'do',
                  'your', 'our', 'its', 'with', 'from', 'by', 'at', 'on', 'be',
                  'that', 'this', 'guide', 'tips', 'best', 'top', 'complete',
                  'ultimate', 'expert', 'vs', 'or'}
    
    # Remove common title suffixes
    title_clean = re.sub(r'\s*\|.*$', '', title)  # Remove | suffix
    words = title_clean.lower().split()
    
    # Try to find a meaningful phrase (2-3 words)
    # First, remove leading stop words
    meaningful = [w.strip('?:;,.!') for w in words if w.strip('?:;,.!') not in stop_words and len(w.strip('?:;,.!')) > 2]
    
    if not meaningful:
        # Fallback: use first non-stop word
        for w in words:
            wc = w.strip('?:;,.!')
            if wc and wc not in stop_words:
                meaningful.append(wc)
                break
    
    if not meaningful:
        return 'SEO', 0, 'Could not extract keyword from title'
    
    # Use the first 1-2 meaningful tokens as keyword
    keyword = ' '.join(meaningful[:2]).strip()
    
    # Count occurrences
    content_lower = content.lower()
    count = content_lower.count(keyword.lower())
    
    # Also check if keyword appears in tags
    status = '✅' if count >= 5 else '❌'
    detail = f'{count} occurrences'
    if count < 5:
        detail += ' — too thin'
    
    return keyword, count, detail


def check_entities(content):
    """Check semantic entity coverage."""
    # Key entities that should be present based on context
    entities = {
        'Location (Dhaka/Bangladesh)': [r'\bDhaka\b', r'\bBangladesh\b'],
        'Service type (SEO)': [r'\bSEO\b', r'\bsearch engine optimization\b'],
        'Kanok Miah (author/brand)': [r'Kanok Miah\b', r'Kanok'],
    }
    
    missing = []
    content_lower = content.lower()
    
    for entity_name, patterns in entities.items():
        found = any(re.search(p, content) for p in patterns)
        if not found:
            missing.append(entity_name)
    
    if missing:
        return '❌', f'Missing: {", ".join(missing)}'
    return '✅', 'All key entities present'


def check_pillar_link(post, all_posts_content):
    """Check if post links to its pillar page based on tags."""
    block = post['block']
    content = extract_content(block)
    tags_str = extract_field(block, 'tags')
    
    # Determine pillar topic from tags
    pillar_map = {
        'Local SEO': ('/services/local-seo', 'Local SEO'),
        'Technical SEO': ('/services/technical-seo', 'Technical SEO'),
        'E-commerce SEO': ('/services/ecommerce-seo', 'E-commerce SEO'),
        'Link Building': ('/services/link-building', 'Link Building'),
        'GEO': ('/services/geo-ai-search', 'GEO/AI Search'),
        'SEO Guide': ('/services/local-seo', 'SEO Services'),
        'Case Study': ('/services/local-seo', 'SEO Services'),
        'Content': ('/services/semantic-seo', 'Semantic SEO'),
        'Mobile': ('/services/technical-seo', 'Technical SEO'),
    }
    
    # Check tags
    if tags_str:
        tags = [t.strip().strip('"\'') for t in tags_str.split(',')]
    else:
        tags = []
    
    # Look for pillar references in content
    pillar_links_found = []
    pillar_pages = [
        '/services/', '/about', '/locations/dhaka',
        '/services/local-seo', '/services/technical-seo',
        '/services/ecommerce-seo', '/services/link-building',
        '/services/geo-ai-search', '/services/semantic-seo',
        '/blog/', '/'
    ]
    
    for page in pillar_pages:
        # Look for markdown links
        pattern = rf'\[([^\]]+)\]\({re.escape(page)}\)'
        if re.search(pattern, content):
            pillar_links_found.append(page)
    
    if pillar_links_found:
        return '✅', f'Links to: {", ".join(pillar_links_found[:3])}'
    else:
        return '❌', 'No pillar page link found'


def check_aeo_geo(content):
    """Check AEO/GEO optimization - question-based headings."""
    # Count headings that start with question words
    question_heading_pattern = r'#{2,4}\s+(How|What|Why|When|Where|Can|Do|Is|Are|Does|Will|Would|Should|Could)'
    headings = re.findall(question_heading_pattern, content, re.IGNORECASE)
    
    count = len(headings)
    if count >= 2:
        return '✅', f'{count} question headings'
    return '❌', f'{count} question headings (need ≥2)'


def check_internal_links(content, current_slug, all_posts_content):
    """Count internal links to other posts, services, locations."""
    # Skip the "Looking for the" section at the end (it's a footer)
    main_content = content
    
    # Count markdown links with internal paths
    internal_link_pattern = r'\[([^\]]+)\]\((/[^\)]+)\)'
    links = re.findall(internal_link_pattern, main_content)
    
    # Filter to meaningful internal links (not HTTP and not anchors only)
    meaningful_links = []
    for text, href in links:
        if href.startswith(('http://', 'https://')):
            continue
        if href == '#':
            continue
        meaningful_links.append((text, href))
    
    count = len(meaningful_links)
    if count >= 3:
        return '✅', f'{count} total ({", ".join(h for _, h in meaningful_links[:5])})'
    return '❌', f'{count} total (need ≥3)'


def check_schema(post):
    """Check if post has schema-essential fields."""
    block = post['block']
    
    title = extract_field(block, 'title')
    excerpt = extract_field(block, 'excerpt')
    date = extract_field(block, 'date')
    author = extract_field(block, 'author')
    metaTitle = extract_field(block, 'metaTitle')
    metaDescription = extract_field(block, 'metaDescription')
    
    required = {
        'title': title,
        'excerpt': excerpt,
        'date': date,
    }
    optional = {
        'author': author,
        'metaTitle': metaTitle,
        'metaDescription': metaDescription,
    }
    
    missing = [k for k, v in required.items() if not v]
    missing_opt = [k for k, v in optional.items() if not v]
    
    if not missing:
        detail = 'All required fields set'
        if missing_opt:
            detail += f' (missing optional: {", ".join(missing_opt)})'
        return '✅', detail
    else:
        return '❌', f'Missing: {", ".join(missing)}'


def analyze_post(post, all_posts_content):
    """Run all framework checks on a single post."""
    slug = post['slug']
    block = post['block']
    
    title = extract_field(block, 'title') or 'Untitled'
    content = extract_content(block)
    tags_str = extract_field(block, 'tags') or ''
    
    print(f'\n## Post: {slug}')
    print(f'**Title:** {title}')
    print()
    print('| Check | Status | Details |')
    print('|-------|--------|---------|')
    
    fixes = []
    
    # A. TF-IDF Coverage
    keyword, count, detail = check_tfidf(title, content)
    print(f'| TF-IDF: "{keyword}" | {"✅" if count >= 5 else "❌"} | {detail} |')
    if count < 5:
        fixes.append(f'- Boost TF-IDF: Use keyword "{keyword}" more in content (≥5 occurrences, currently {count})')
    
    # B. Semantic Entity Coverage
    entity_status, entity_detail = check_entities(content)
    print(f'| Entities | {entity_status} | {entity_detail} |')
    if entity_status == '❌':
        fixes.append(f'- Add missing entities: {entity_detail.replace("Missing: ", "")}')
    
    # C. Pillar-Cluster Alignment
    pillar_status, pillar_detail = check_pillar_link(post, all_posts_content)
    print(f'| Pillar Link | {pillar_status} | {pillar_detail} |')
    if pillar_status == '❌':
        fixes.append('- Add a link to the pillar service page (e.g., [/services/local-seo](/services/local-seo))')
    
    # D. AEO/GEO Optimization
    aeo_status, aeo_detail = check_aeo_geo(content)
    print(f'| AEO/GEO | {aeo_status} | {aeo_detail} |')
    if aeo_status == '❌':
        fixes.append(f'- Add more question-based headings (How/What/Why) — currently {aeo_detail.split()[0]}')
    
    # E. Internal Linking
    link_status, link_detail = check_internal_links(content, slug, all_posts_content)
    print(f'| Internal Links | {link_status} | {link_detail} |')
    count_links = int(link_detail.split()[0])
    if count_links < 3:
        fixes.append(f'- Add more internal links (≥3 needed, currently {count_links})')
    
    # F. Schema
    schema_status, schema_detail = check_schema(post)
    print(f'| Schema Ready | {schema_status} | {schema_detail} |')
    if schema_status == '❌':
        fixes.append(f'- Fix schema fields: {schema_detail}')
    
    if fixes:
        print()
        print('### Fix instructions:')
        for f in fixes:
            print(f)
    else:
        print()
        print('✅ All checks passed — no changes needed.')
    
    # Also print a quick summary of what was modified
    print()
    print(f'*Modified in this commit set*')

    return slug


# Main
filepath = '/root/kanok-miahit/src/app/blog/data.js'
posts, full_content = parse_posts(filepath)

# Slugs modified in the last 48 hours
modified_slugs = [
    'link-building-strategies-bangladesh-market',
    'seo-garments-textile-industry-b2b-lead-generation',
    'google-business-profile-optimization-guide-bangladesh',
    'mobile-seo-optimization-bangladesh-mobile-first-era',
    'why-md-kanok-miah-is-the-best-seo-expert-in-dhaka-bangladesh',
    'landlord-certificates-seo-case-study',
    'das-taxis-scotland-seo-case-study',
    'morethanpanel-seo-case-study',
    'smmgen-seo-case-study',
    'smmsun-seo-case-study',
    'mir-cement-seo-case-study',
    'dhaka-apparels-seo-case-study',
    'stealth-windshield-repairs-seo-case-study',
    'how-to-choose-best-seo-expert-dhaka-15-things',
    'seo-expert-vs-seo-agency-dhaka-which-is-right',
    'top-10-seo-mistakes-dhaka-businesses-fix',
    'what-does-seo-expert-do-guide-business-owners',
    'seo-case-study-dhaka-businesses-increased-organic-traffic',
    'hiring-seo-expert-dhaka-better-roi-than-paid-ads',
    'ai-seo-2026-dhaka-experts-optimize-google-ai-chatgpt',
]

all_posts_content = full_content  # Pass for pillar link detection

print(f'# Content Framework Enforcement Report')
print(f'**Date:** 2026-07-28')
print(f'**Source:** Git diff HEAD~2 HEAD on src/app/blog/data.js')
print(f'**Posts analyzed:** {len(modified_slugs)}')
print()

for slug in modified_slugs:
    post = next((p for p in posts if p['slug'] == slug), None)
    if post:
        analyze_post(post, all_posts_content)
    else:
        print(f'\n## Post: {slug}')
        print('⚠️ Could not find post in data.js')
