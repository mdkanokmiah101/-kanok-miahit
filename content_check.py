#!/usr/bin/env python3
"""Content Framework Checker for kanokmiah.com.bd blog posts."""
import re
import sys

# Read the data.js file
with open('/root/kanok-miahit/src/app/blog/data.js', 'r') as f:
    content = f.read()

def extract_field(block, pattern):
    m = re.search(pattern, block)
    return m.group(1) if m else ''

def get_post_block(content, slug):
    """Extract the full post object block from data.js."""
    post_idx = content.find(f'slug: "{slug}"')
    if post_idx == -1:
        return None, None
    open_brace = content.rfind('{', 0, post_idx)
    if open_brace == -1:
        return None, None
    
    # Find content: `...` end
    content_start = content.find(f'content: `', open_brace)
    if content_start == -1:
        return None, None
    content_text_start = content_start + len('content: `')
    # Find the closing backtick
    nested = 0
    close_content = -1
    for i in range(content_text_start, len(content)):
        if content[i] == '`':
            if nested == 0:
                close_content = i
                break
        elif content[i:i+2] == '\\`':
            i += 1
    if close_content == -1:
        return None, None
    
    # Now find the closing }, of the post object
    close_brace = content.find('},', close_content)
    if close_brace == -1:
        close_brace = content.find('}\n', close_content)
    if close_brace == -1:
        close_brace = content.find('}', close_content)
    
    post_block = content[open_brace:close_brace+1]
    return post_block, content[content_text_start:close_content]


def parse_all_posts(content):
    """Parse all posts from data.js."""
    posts = {}
    
    # Find all slugs and their content blocks
    slug_pattern = re.compile(r'slug:\s*"([^"]+)"')
    for m in slug_pattern.finditer(content):
        slug = m.group(1)
        post_block, content_text = get_post_block(content, slug)
        if post_block is None:
            continue
        
        title = extract_field(post_block, r'title:\s*"([^"]+)"')
        date = extract_field(post_block, r'date:\s*"([^"]+)"')
        date_modified = extract_field(post_block, r'dateModified:\s*"([^"]+)"')
        excerpt = extract_field(post_block, r'excerpt:\s*"([^"]*)"')
        tags_str = extract_field(post_block, r'tags:\s*\[(.*?)\]')
        meta_title = extract_field(post_block, r'metaTitle:\s*"([^"]*)"')
        meta_description = extract_field(post_block, r'metaDescription:\s*"([^"]*)"')
        
        tags = re.findall(r'"([^"]+)"', tags_str) if tags_str else []
        
        posts[slug] = {
            'title': title,
            'date': date or 'unknown',
            'dateModified': date_modified or '',
            'excerpt': excerpt or '',
            'tags': tags,
            'metaTitle': meta_title or '',
            'metaDescription': meta_description or '',
            'content': content_text
        }
    
    return posts


def check_tfidf(title, content):
    """Extract primary keyword from title and count occurrences."""
    stop_words = {'a', 'an', 'the', 'for', 'in', 'of', 'to', 'and', 'is', 'are', 'your', 'our', 'we', 'how', 'what', 'why', 'when', 'where', 'do', 'does', 'need', 'has', 'been', 'its', 'it', 'at', 'with', 'that', 'this', 'on', 'by', 'not', 'no', 'or', 'be'}
    
    words = re.findall(r'[A-Za-z]+', title)
    meaningful = [w for w in words if w.lower() not in stop_words and len(w) > 2]
    
    keyword = ''
    count = 0
    
    if meaningful:
        # Try the first meaningful word as base
        keyword = meaningful[0]
        count = len(re.findall(re.escape(keyword), content, re.IGNORECASE))
        
        # Try 2-3 word phrases
        for n in range(min(3, len(meaningful)), 1, -1):
            phrase = ' '.join(meaningful[:n])
            phrase_count = len(re.findall(re.escape(phrase), content, re.IGNORECASE))
            if phrase_count > 0:
                keyword = phrase
                count = phrase_count
                break
    
    return keyword, count


def check_entities(content, slug):
    """Check key entities for each post."""
    missing = []
    
    # Universal location entities
    if not re.search(r'Dhaka', content, re.IGNORECASE):
        missing.append('Dhaka (location)')
    if not re.search(r'Bangladesh', content, re.IGNORECASE):
        missing.append('Bangladesh (country)')
    
    # Service type entities based on slug
    slug_lower = slug.lower()
    if any(x in slug_lower for x in ['ecommerce', 'e-commerce', 'daraz', 'shopify', 'store']):
        if not re.search(r'e.?commerce|online store', content, re.IGNORECASE):
            missing.append('E-commerce (service type)')
    if any(x in slug_lower for x in ['garment', 'textile', 'b2b', 'lead.generation']):
        if not re.search(r'B2B|garment|RMG|manufacturer', content, re.IGNORECASE):
            missing.append('B2B/Garments (industry)')
    if any(x in slug_lower for x in ['local']):
        if not re.search(r'Google Business Profile|GBP|local search|Google Maps', content):
            missing.append('Local SEO (service type)')
    if any(x in slug_lower for x in ['mobile', 'amp']):
        if not re.search(r'mobile|smartphone', content, re.IGNORECASE):
            missing.append('Mobile (topic)')
    if 'link.building' in slug_lower:
        if not re.search(r'backlink|link building|guest post', content, re.IGNORECASE):
            missing.append('Link building (service type)')
    if 'technical' in slug_lower:
        if not re.search(r'technical|crawl|core web vitals|page speed', content, re.IGNORECASE):
            missing.append('Technical SEO (topic)')
    if 'case.study' in slug_lower:
        if not re.search(r'organic|traffic|growth|result|increase', content, re.IGNORECASE):
            missing.append('Results data (case study)')
    if 'real.estate' in slug_lower or 'property' in slug_lower:
        if not re.search(r'property|real estate', content, re.IGNORECASE):
            missing.append('Real estate (industry)')
    if 'google.business' in slug_lower or 'gbp' in slug_lower or 'google.my.business' in slug_lower:
        if not re.search(r'Google Business|GBP|Google My Business', content):
            missing.append('GBP (service type)')
    if 'geo' in slug_lower or 'ai' in slug_lower:
        if not re.search(r'GEO|AI|generative|ChatGPT', content):
            missing.append('GEO/AI (topic)')
    if 'consultant' in slug_lower or 'expert' in slug_lower or 'agency' in slug_lower:
        if not re.search(r'expert|consultant|agency|professional', content, re.IGNORECASE):
            missing.append('Service provider (entity)')
    if 'seo.optimization' in slug_lower or 'seo.guide' in slug_lower:
        pass  # broad SEO terms, skip specific checks
    
    return missing


def check_pillar_links(content):
    """Check links to pillar pages."""
    linked = []
    
    pillar_patterns = [
        ('/blog/complete-seo-guide-bangladesh-businesses-2026', 'Complete SEO Guide pillar'),
        ('/blog/local-seo-tips-dhaka-businesses-google-maps', 'Local SEO Guide pillar'),
        ('/blog/technical-seo-checklist-bangladeshi-websites', 'Technical SEO Guide pillar'),
        ('/services/', 'Services pages'),
        ('/services/local-seo', 'Local SEO services'),
        ('/services/technical-seo', 'Technical SEO services'),
        ('/services/ecommerce-seo', 'E-commerce SEO services'),
        ('/services/on-page-seo', 'On-page SEO services'),
        ('/services/geo-ai-search', 'GEO/AI search services'),
        ('/industries/', 'Industry pages'),
    ]
    
    for url, label in pillar_patterns:
        if url in content:
            linked.append(label)
    
    return linked


def check_aeo_geo(content):
    """Count question-based headings."""
    headings = re.findall(
        r'^#{2,6}\s+(How|What|Why|When|Where|Can|Do|Is|Are|Does|Which|Who)\b',
        content,
        re.MULTILINE | re.IGNORECASE
    )
    return headings


def check_internal_links(content):
    """Count and return internal links."""
    links = re.findall(r'\[([^\]]+)\]\(/([^)]+)\)', content)
    return links


def check_schema(post):
    """Check ArticleSchema readiness."""
    missing = []
    if not post.get('metaTitle'):
        missing.append('metaTitle')
    if not post.get('metaDescription'):
        missing.append('metaDescription')
    if not post.get('date'):
        missing.append('date')
    if not post.get('excerpt'):
        missing.append('excerpt')
    if not post.get('dateModified'):
        missing.append('dateModified (recommended)')
    return missing


# Parse all posts
posts = parse_all_posts(content)

# Changed posts from git diff analysis
changed_posts = [
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

# Summary stats
total_posts = len(posts)
pass_count = 0
fail_posts = []

print(f"📊 Content Framework Enforcement Report — kanokmiah.com.bd\n")
print(f"Total posts in database: {total_posts}")
print(f"Posts modified in last 48h: {len(changed_posts)}\n")

for slug in changed_posts:
    if slug not in posts:
        print(f"\n⚠️  Post '{slug}' not found in data.js")
        continue
    
    post = posts[slug]
    content = post['content']
    title = post['title']
    
    print(f"---")
    print(f"## Post: {slug}")
    print(f"**Title:** {title}")
    
    checks = []
    total_flags = 0
    
    # A. TF-IDF Coverage
    keyword, count = check_tfidf(title, content)
    if not keyword:
        keyword = title.split()[0] if title else 'N/A'
    tfidf_flag = count < 5
    total_flags += 1 if tfidf_flag else 0
    tfidf_status = '✅' if not tfidf_flag else '❌'
    
    # B. Entity Coverage
    missing_entities = check_entities(content, slug)
    entities_flag = len(missing_entities) > 0
    total_flags += 1 if entities_flag else 0
    entities_status = '✅' if not entities_flag else '❌'
    
    # C. Pillar-Cluster Alignment
    pillar_links = check_pillar_links(content)
    pillar_flag = len(pillar_links) == 0
    total_flags += 1 if pillar_flag else 0
    pillar_status = '✅' if not pillar_flag else '❌'
    
    # D. AEO/GEO Optimization
    question_headings = check_aeo_geo(content)
    aeo_flag = len(question_headings) < 2
    total_flags += 1 if aeo_flag else 0
    aeo_status = '✅' if not aeo_flag else '❌'
    
    # E. Internal Linking
    internal_links = check_internal_links(content)
    links_flag = len(internal_links) < 3
    total_flags += 1 if links_flag else 0
    links_status = '✅' if not links_flag else '❌'
    
    # F. Schema Readiness
    missing_fields = check_schema(post)
    schema_flag = len(missing_fields) > 0
    total_flags += 1 if schema_flag else 0
    schema_status = '✅' if not schema_flag else '❌'
    
    # Output table
    entity_detail = f"Missing: {', '.join(missing_entities)}" if missing_entities else "All key entities present"
    pillar_detail = f"Links to: {', '.join(pillar_links)}" if pillar_links else "No pillar link found"
    aeo_detail = f"{len(question_headings)} question headings: {', '.join(question_headings[:4])}" if question_headings else "None"
    link_detail = f"{len(internal_links)} total"
    schema_detail = f"Missing: {', '.join(missing_fields)}" if missing_fields else "All fields set"
    
    print(f"""
| Check | Status | Details |
|-------|--------|---------|
| TF-IDF: `{keyword}` | {tfidf_status} | {count} occurrences{' (thin — target ≥5)' if tfidf_flag else ''} |
| Entities | {entities_status} | {entity_detail} |
| Pillar Link | {pillar_status} | {pillar_detail} |
| AEO/GEO | {aeo_status} | {aeo_detail} |
| Internal Links | {links_status} | {link_detail} |
| Schema Ready | {schema_status} | {schema_detail} |
""")
    
    # Fix instructions
    if total_flags > 0:
        fail_posts.append(slug)
        print(f"### 🔧 Fix instructions for `{slug}`:")
        if tfidf_flag:
            print(f"- **TF-IDF too thin:** Increase `{keyword}` mentions to ≥5 across content")
        if entities_flag:
            print(f"- **Missing entities:** Add `{'`, `'.join(missing_entities)}` where relevant")
        if pillar_flag:
            print(f"- **No pillar link:** Link to the appropriate pillar page (e.g., `/blog/complete-seo-guide-bangladesh-businesses-2026`, `/services/`, or `/industries/`)")
        if aeo_flag:
            print(f"- **AEO/GEO weak:** Add ≥2 question-based headings (How, What, Why, etc.) for AI search optimization")
        if links_flag:
            print(f"- **Too few internal links ({len(internal_links)}):** Add more links to other blog posts, service pages, or location pages")
        if schema_flag:
            print(f"- **Schema fields missing:** Add `{'`, `'.join(missing_fields)}` to the post object")
        print()
    else:
        pass_count += 1

# Summary
print(f"\n{'='*60}")
print(f"📋 OVERALL SUMMARY")
print(f"{'='*60}")
print(f"✅ Posts passing all checks: {pass_count}/{len(changed_posts)}")
print(f"❌ Posts needing fixes: {len(fail_posts)}")
if fail_posts:
    print(f"   Affected: {', '.join(fail_posts)}")
print(f"\nNote: Most changes this cycle were automated (URL normalization, heading cleanup).")
print(f"The primary substantive change was silo optimization for `how-to-choose-best-seo-expert-dhaka-15-things`")
print(f"and meta field additions to `mobile-seo-optimization-bangladesh-mobile-first-era`.")
