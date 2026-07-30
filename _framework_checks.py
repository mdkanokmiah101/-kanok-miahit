#!/usr/bin/env python3
"""
Full framework check for changed blog posts - v2 with better parsing.
"""
import re
import json
import os
import sys

os.chdir("/root/kanok-miahit")

# ─── Parse data.js using slug-based splitting ───────────────
with open("src/app/blog/data.js") as f:
    content = f.read()

# Split by 'slug: "' to get post fragments
# Each fragment starts with the slug value and contains the rest of the post
parts = content.split('slug: "')
# parts[0] is "const posts = [\n  {"
# parts[1:] start with the slug value

posts = []
for i, part in enumerate(parts[1:], 1):
    slug = part.split('"')[0]  # Everything up to the closing '"'
    
    # Get the post data portion
    post_data = part[len(slug) + 1:]  # Skip slug value and closing '",'
    
    # Extract fields
    title_m = re.search(r'title:\s*"([^"]+)"', post_data[:2000])
    date_m = re.search(r'date:\s*"([^"]+)"', post_data[:1000])
    excerpt_m = re.search(r'excerpt:\s*\n?\s*"([^"]+)"', post_data[:3000])
    tags_m = re.search(r'tags:\s*\[([^\]]+)\]', post_data[:3000], re.DOTALL)
    metaTitle_m = re.search(r'metaTitle:\s*"([^"]+)"', post_data[:3000])
    metaDesc_m = re.search(r'metaDescription:\s*"([^"]+)"', post_data[:3000])
    dateMod_m = re.search(r'dateModified:\s*"([^"]+)"', post_data[:3000])
    
    # Extract content (between backtick quotes)
    content_m = re.search(r'content:\s*`\n(.*?)\n\s*`', post_data, re.DOTALL)
    if not content_m:
        content_m = re.search(r'content:\s*`(.*?)`', post_data, re.DOTALL)
    
    content_text = content_m.group(1) if content_m else ""
    
    # Parse tags
    tags = []
    if tags_m:
        tag_str = tags_m.group(1)
        tags = re.findall(r'"([^"]+)"', tag_str)
    
    post = {
        'slug': slug,
        'title': title_m.group(1) if title_m else '',
        'date': date_m.group(1) if date_m else '',
        'excerpt': excerpt_m.group(1) if excerpt_m else '',
        'tags': tags,
        'metaTitle': metaTitle_m.group(1) if metaTitle_m else '',
        'metaDescription': metaDesc_m.group(1) if metaDesc_m else '',
        'dateModified': dateMod_m.group(1) if dateMod_m else '',
        'content': content_text,
    }
    posts.append(post)

print(f"Parsed {len(posts)} posts total", file=sys.stderr)

# ─── Changed slugs ─────────────────────────────────────────
changed_slugs = [
    'ai-seo-2026-dhaka-experts-optimize-google-ai-chatgpt',
    'das-taxis-scotland-seo-case-study',
    'dhaka-apparels-seo-case-study',
    'google-business-profile-optimization-guide-bangladesh',
    'hiring-seo-expert-dhaka-better-roi-than-paid-ads',
    'how-to-choose-best-seo-expert-dhaka-15-things',
    'landlord-certificates-seo-case-study',
    'link-building-strategies-bangladesh-market',
    'mir-cement-seo-case-study',
    'mobile-seo-optimization-bangladesh-mobile-first-era',
    'morethanpanel-seo-case-study',
    'seo-case-study-dhaka-businesses-increased-organic-traffic',
    'seo-expert-vs-seo-agency-dhaka-which-is-right',
    'seo-garments-textile-industry-b2b-lead-generation',
    'smmgen-seo-case-study',
    'smmsun-seo-case-study',
    'stealth-windshield-repairs-seo-case-study',
    'top-10-seo-mistakes-dhaka-businesses-fix',
    'what-does-seo-expert-do-guide-business-owners',
    'why-md-kanok-miah-is-the-best-seo-expert-in-dhaka-bangladesh',
]

changed_posts = [p for p in posts if p['slug'] in changed_slugs]
print(f"Found {len(changed_posts)} changed posts", file=sys.stderr)
missing = [s for s in changed_slugs if s not in {p['slug'] for p in posts}]
if missing:
    print(f"MISSING: {missing}", file=sys.stderr)

# ─── Framework Checks ──────────────────────────────────────────

def check_tfidf(post):
    """Extract primary keyword from title, count occurrences in content."""
    title = post['title']
    clean_title = re.sub(r'\s*[|–-].*$', '', title).strip()
    
    stopwords = {'a', 'an', 'the', 'for', 'of', 'in', 'to', 'and', 'or', 'with', 'is', 'are', 'was', 'were', 'on', 'at', 'by', 'from', 'your', 'our', 'their', 'its', 'how', 'what', 'why', 'when', 'where', 'which', 'who', 'do', 'does', 'did', 'can', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'need', 'has', 'have', 'had', 'not', 'no', 'up', 'out', 'off', 'over', 'under', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'between', 'about', 'than', 'that', 'this', 'these', 'those'}
    
    words = clean_title.split()
    keyword_parts = [w for w in words if w.lower() not in stopwords]
    
    if not keyword_parts:
        keyword = clean_title
    else:
        keyword = ' '.join(keyword_parts[:3])
    
    keyword_lower = keyword.lower()
    
    # Count occurrences in content (case-insensitive)
    count = post['content'].lower().count(keyword_lower) if keyword_lower else 0
    
    # If count is too low, try with first 2 words
    if count < 3 and len(keyword_parts) > 1:
        keyword2 = ' '.join(keyword_parts[:2]).lower()
        count2 = post['content'].lower().count(keyword2)
        if count2 > count:
            keyword = keyword2
            count = count2
    
    # If still low, try with first word only
    if count < 3 and len(keyword_parts) >= 1:
        keyword3 = keyword_parts[0].lower()
        count3 = post['content'].lower().count(keyword3)
        if count3 > count:
            keyword = keyword3
            count = count3
    
    passed = count >= 5
    return {
        'keyword': keyword,
        'count': count,
        'passed': passed,
        'detail': f'{count} occurrences'
    }

def check_entities(post):
    """Check key entities that should be present."""
    content_lower = post['content'].lower()
    slug = post['slug']
    
    # Always required
    all_entities = ['Dhaka', 'Bangladesh']
    
    # Add service-type-specific entities
    if any(kw in slug for kw in ['seo', 'seo-expert']):
        all_entities.append('SEO')
    
    if 'local' in slug or 'google-business' in slug or 'gbp' in slug:
        all_entities.extend(['Google Business Profile', 'local SEO'])
    
    if 'technical' in slug:
        all_entities.extend(['Core Web Vitals', 'schema'])
    
    if 'link-building' in slug:
        all_entities.extend(['backlinks', 'link building'])
    
    if 'case-study' in slug or 'case study' in slug:
        all_entities.extend(['traffic', 'organic', 'rankings'])
    
    if 'garment' in slug or 'textile' in slug:
        all_entities.extend(['garments', 'textile'])
    
    if 'mobile' in slug:
        all_entities.extend(['mobile-first', 'smartphone'])
    
    if 'geo' in slug or 'ai' in slug:
        all_entities.extend(['AI', 'GEO', 'ChatGPT'])
    
    if 'healthcare' in slug or 'medical' in slug or 'clinic' in slug:
        all_entities.extend(['healthcare', 'medical'])
    
    if 'smmgen' in slug or 'smm' in slug or 'panel' in slug:
        all_entities.extend(['SMM panel', 'SMM'])
    
    # Add based on tags
    for tag in post['tags']:
        tag_lower = tag.lower()
        if 'seo' in tag_lower and 'seo' not in [e.lower() for e in all_entities]:
            all_entities.append('SEO')
        if 'E-commerce' in tag_lower or 'ecommerce' in tag_lower:
            all_entities.append('e-commerce')
        if 'garment' in tag_lower or 'textile' in tag_lower:
            all_entities.append('garments')
        if 'real estate' in tag_lower:
            all_entities.append('real estate')
        if 'healthcare' in tag_lower or 'medical' in tag_lower:
            all_entities.append('healthcare')
    
    # Deduplicate while preserving order
    seen = set()
    unique_entities = []
    for e in all_entities:
        e_lower = e.lower()
        if e_lower not in seen:
            seen.add(e_lower)
            unique_entities.append(e)
    
    missing = []
    for entity in unique_entities:
        if entity.lower() not in content_lower:
            missing.append(entity)
    
    passed = len(missing) == 0
    return {
        'expected': unique_entities,
        'missing': missing,
        'passed': passed,
        'detail': f"Missing: {', '.join(missing) if missing else 'None'}"
    }

def check_pillar_cluster(post):
    """Check pillar-cluster alignment based on tags."""
    tags = post['tags']
    slug = post['slug']
    content_lower = post['content'].lower()
    
    pillar_map = {
        'Local SEO': ['local', 'gbp', 'google business', 'google maps', 'near me'],
        'Technical SEO': ['technical', 'core web vitals', 'site speed', 'crawl', 'index', 'mobile'],
        'Content SEO': ['content', 'blog', 'writing', 'keyword research'],
        'Link Building': ['link building', 'backlinks', 'guest post'],
        'E-commerce SEO': ['ecommerce', 'e-commerce', 'online store', 'shop'],
        'SEO Strategy': ['seo strategy', 'seo guide', 'seo tips', 'seo checklist'],
        'GEO/AI SEO': ['geo', 'generative engine', 'ai seo', 'chatgpt', 'ai search'],
        'Case Study': ['case study', 'case-study'],
        'SEO Expert/Agency': ['seo expert', 'seo agency', 'seo consultant', 'seo specialist', 'hire seo', 'choose seo'],
    }
    
    detected_pillar = 'General SEO'
    for pillar, keywords in pillar_map.items():
        for kw in keywords:
            if kw in slug.lower() or any(kw in tag.lower() for tag in tags):
                detected_pillar = pillar
                break
        if detected_pillar != 'General SEO':
            break
    
    # Check for pillar links
    internal_links = re.findall(r'/blog/[a-z0-9-]+|/services/[a-z0-9-]+|/locations/[a-z0-9-]+|/industries/[a-z0-9-]+|/case-studies|/about|/contact', content_lower)
    
    pillar_link_patterns = {
        'Local SEO': ['/services/local', '/locations/', '/blog/local-seo'],
        'Technical SEO': ['/services/technical'],
        'Content SEO': ['/services/content', '/blog/content-'],
        'Link Building': ['/services/link-building', '/blog/link-building'],
        'E-commerce SEO': ['/services/ecommerce', '/industries/ecommerce'],
        'SEO Strategy': ['/blog/complete-seo-guide', '/blog/seo-'],
        'GEO/AI SEO': ['/services/geo', '/blog/geo-', '/blog/ai-seo'],
        'Case Study': ['/case-studies', '/blog/'],
        'SEO Expert/Agency': ['/about', '/blog/what-does-seo-expert', '/blog/hiring-seo', '/blog/how-to-choose', '/blog/seo-expert-vs'],
    }
    
    expected_links = pillar_link_patterns.get(detected_pillar, [])
    found_pillar_links = [l for l in internal_links if any(l.startswith(ep) for ep in expected_links)]
    has_pillar_link = len(found_pillar_links) > 0
    
    return {
        'pillar': detected_pillar,
        'has_pillar_link': has_pillar_link,
        'found_links': found_pillar_links[:5],
        'detail': f"Pillar: {detected_pillar} | Links to pillar: {'Yes' if has_pillar_link else 'No'}" + (f" ({', '.join(found_pillar_links[:3])})" if found_pillar_links else "")
    }

def check_aeo_geo(post):
    """Count question-based headings for AEO/GEO optimization."""
    content = post['content']
    
    # Find all headings (##, ###, #### lines)
    headings = re.findall(r'^#{2,4}\s+.*$', content, re.MULTILINE)
    
    question_starts = {'how', 'what', 'why', 'when', 'where', 'can', 'do', 'is', 'are', 'which', 'who', 'does', 'did', 'will', 'would', 'could', 'should', 'has', 'have', 'had', 'need', 'was', 'were'}
    
    question_headers = []
    for h in headings:
        h_clean = h.lstrip('#').strip()
        # Remove markdown formatting
        h_clean = re.sub(r'[*_`"]', '', h_clean)
        first_word = h_clean.split()[0].lower() if h_clean.split() else ''
        if first_word in question_starts:
            question_headers.append(h_clean)
    
    count = len(question_headers)
    passed = count >= 2
    
    return {
        'count': count,
        'questions': question_headers[:5],
        'passed': passed,
        'detail': f'{count} question headings' + (f': {"; ".join(question_headers[:3])}' if question_headers else '')
    }

def check_internal_links(post):
    """Count internal links to other posts, services, locations."""
    content = post['content']
    
    internal_links = re.findall(r'/blog/[a-z0-9-]+|/services/[a-z0-9-]+|/locations/[a-z0-9-]+|/industries/[a-z0-9-]+|/case-studies|/about|/contact', content)
    
    unique_links = list(set(internal_links))
    count = len(unique_links)
    passed = count >= 3
    
    return {
        'count': count,
        'unique_links': unique_links[:8],
        'passed': passed,
        'detail': f'{count} unique: {", ".join(unique_links[:5])}' if unique_links else '0 detected'
    }

def check_schema(post):
    """Check if post has schema-required fields."""
    fields = {
        'title': bool(post['title']),
        'excerpt': bool(post['excerpt']),
        'date': bool(post['date']),
        'metaTitle': bool(post['metaTitle']),
        'metaDescription': bool(post['metaDescription']),
        'dateModified': bool(post['dateModified']),
    }
    
    missing = [k for k, v in fields.items() if not v]
    passed = len(missing) == 0
    
    return {
        'fields': fields,
        'missing': missing,
        'passed': passed,
        'detail': f"Missing: {', '.join(missing) if missing else 'All ok'}"
    }

# ─── Run Checks and Generate Report ──────────────────────────

report_parts = []

for post in changed_posts:
    tfidf = check_tfidf(post)
    entities = check_entities(post)
    pillar = check_pillar_cluster(post)
    aeo = check_aeo_geo(post)
    links = check_internal_links(post)
    schema = check_schema(post)
    
    # Generate fix instructions
    fixes = []
    if not tfidf['passed']:
        fixes.append(f"- **TF-IDF**: Increase usage of \"{tfidf['keyword']}\" in content (currently {tfidf['count']}x, need ≥5). Add more natural keyword variations throughout the article.")
    if not entities['passed']:
        fixes.append(f"- **Entities**: Add missing entities: {', '.join(entities['missing'])}. Mention these explicitly in the content.")
    if not pillar['has_pillar_link']:
        fixes.append(f"- **Pillar Link**: Add a link to the {pillar['pillar']} pillar page. For {pillar['pillar']}, relevant service/pillar pages should be linked.")
    if not aeo['passed']:
        fixes.append(f"- **AEO/GEO**: Add 1-2 more question-based headings (starting with How, What, Why, etc.). Currently only {aeo['count']}.")
    if not links['passed']:
        fixes.append(f"- **Internal Links**: Add more internal links to other blog posts, services, or locations. Currently {links['count']}, need ≥3.")
    if not schema['passed']:
        fixes.append(f"- **Schema**: Add missing fields: {', '.join(schema['missing'])}.")
    
    failures = sum([not tfidf['passed'], not entities['passed'], not pillar['has_pillar_link'],
                    not aeo['passed'], not links['passed'], not schema['passed']])
    
    # Build table
    table = f"""## Post: {post['slug']}
| Check | Status | Details |
|-------|--------|---------|
| TF-IDF: `{tfidf['keyword']}` | {'✅' if tfidf['passed'] else '❌'} | {tfidf['detail']} |
| Entities | {'✅' if entities['passed'] else '❌'} | {entities['detail']} |
| Pillar Link | {'✅' if pillar['has_pillar_link'] else '❌'} | {pillar['detail']} |
| AEO/GEO | {'✅' if aeo['passed'] else '❌'} | {aeo['detail']} |
| Internal Links | {'✅' if links['passed'] else '❌'} | {links['detail']} |
| Schema Ready | {'✅' if schema['passed'] else '❌'} | {schema['detail']} |

Overall: {'✅ PASS' if failures == 0 else f'❌ FAIL ({failures}/6 checks)'}
"""
    
    if fixes:
        table += "\n### Fix instructions:\n" + "\n".join(fixes)
    
    report_parts.append(table)

report = "\n\n---\n\n".join(report_parts)

# Summary
total_posts = len(changed_posts)
pass_count = sum(1 for p in changed_posts if all([
    check_tfidf(p)['passed'],
    check_entities(p)['passed'],
    check_pillar_cluster(p)['has_pillar_link'],
    check_aeo_geo(p)['passed'],
    check_internal_links(p)['passed'],
    check_schema(p)['passed'],
]))

print(report)
print(f"\n\n## Executive Summary")
print(f"- Total changed posts checked: {total_posts}")
print(f"- Fully passing: {pass_count}")
print(f"- Need fixes: {total_posts - pass_count}")
