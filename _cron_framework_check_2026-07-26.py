#!/usr/bin/env python3
"""Content Framework Enforcer - checks blog posts against framework rules."""

import re
import json
from collections import Counter

# Load data.js
with open('src/app/blog/data.js', 'r') as f:
    raw = f.read()

# Parse all blog posts (simple regex-based extraction)
# Match post objects: { slug: "...", title: "...", ... content: `...` }
# We'll use a more robust approach - find slug anchors then extract content

post_pattern = re.compile(
    r'{\s*\n\s*slug:\s*"([^"]+)"\s*,\s*\n\s*title:\s*"([^"]+)"\s*,\s*\n\s*excerpt:\s*"([^"]*)"\s*,\s*\n\s*date:\s*"([^"]*)"\s*,\s*\n\s*imagePlaceholder:\s*"([^"]*)"\s*,\s*\n\s*content:\s*`([^`]*)`',
    re.DOTALL
)

posts = {}
for m in post_pattern.finditer(raw):
    slug = m.group(1)
    posts[slug] = {
        'slug': slug,
        'title': m.group(2),
        'excerpt': m.group(3),
        'date': m.group(4),
        'imagePlaceholder': m.group(5),
        'content': m.group(6),
    }

print(f"Extracted {len(posts)} posts from data.js")

# Modified slugs (from git log in last 48 hours)
modified_slugs = [
    # From commit 540e798 (heading/tags cleanup + content tweaks)
    "geo-optimization-prepare-business-ai-search",
    "seo-garments-textile-industry-b2b-lead-generation",
    "mobile-seo-optimization-bangladesh-mobile-first-era",
    "seo-healthcare-medical-clinics-bangladesh",
    # From commit c822841 (remove duplicate homepage links + content tweaks)
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
]

def extract_primary_keyword(title):
    """Extract primary keyword from title (first meaningful noun phrase)."""
    # Clean title
    title = title.strip()
    # Remove leading "Complete", "Ultimate", "Best", "Top", "How to", "Why"
    # Try to get the SEO-related noun phrase
    # Patterns like "SEO for X", "X SEO", "X Guide"
    
    # Check for "SEO for X" pattern
    m = re.search(r'SEO\s+for\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', title)
    if m:
        return m.group(1)
    
    # Check for "X SEO" pattern (e.g., "Healthcare SEO", "Local SEO")
    m = re.search(r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+SEO', title)
    if m:
        return m.group(1) + " SEO"
    
    # Check for "Guide to X" or "X Guide"
    m = re.search(r'(?:Guide\s+to|Complete)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', title)
    if m:
        return m.group(1)
    
    # Check for "How to X" 
    m = re.search(r'How\s+to\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', title)
    if m:
        return m.group(1)
    
    # Fallback: first 2-3 words
    words = title.split()[:3]
    return ' '.join(words)

def count_keyword_occurrences(content, keyword):
    """Count occurrences of keyword in content (case-insensitive)."""
    if not keyword:
        return 0
    return len(re.findall(re.escape(keyword), content, re.IGNORECASE))

def check_entities(content, title, slug):
    """Check for required entities based on post topic."""
    entities = {
        'location_dhaka': 'Dhaka',
        'location_bangladesh': 'Bangladesh',
        'name_kanok': 'Kanok Miah',
    }
    
    # Determine expected entities based on slug/title
    expected = []
    
    # Location entities
    if 'bangladesh' in slug.lower() or 'dhaka' in slug.lower():
        expected.append('Bangladesh')
        if 'dhaka' in slug.lower():
            expected.append('Dhaka')
    
    # Service entities
    service_keywords = {
        'local-seo': 'Local SEO',
        'ecommerce': 'E-commerce SEO',
        'technical-seo': 'Technical SEO',
        'on-page-seo': 'On-Page SEO',
        'link-building': 'Link Building',
        'content-marketing': 'Content Marketing',
        'mobile-seo': 'Mobile SEO',
        'schema': 'Schema Markup',
        'google-business': 'Google Business Profile',
        'geo': 'GEO',
        'generative': 'Generative Engine Optimization',
    }
    for key, val in service_keywords.items():
        if key in slug.lower():
            expected.append(val)
            break
    
    # Industry entities
    industry_keywords = {
        'healthcare': 'Healthcare',
        'medical': 'Medical',
        'garment': 'Garment',
        'textile': 'Textile',
        'real-estate': 'Real Estate',
        'ecommerce': 'E-commerce',
        'education': 'Education',
        'travel': 'Travel',
        'tourism': 'Tourism',
        'fitness': 'Fitness',
        'gym': 'Gym',
        'law': 'Law',
        'legal': 'Legal',
        'startup': 'Startup',
        'hotel': 'Hotel',
        'resort': 'Resort',
        'restaurant': 'Restaurant',
        'ngo': 'NGO',
        'photograph': 'Photography',
        'wedding': 'Wedding',
        'event': 'Event',
    }
    for key, val in industry_keywords.items():
        if key in slug.lower():
            expected.append(val)
            break
    
    # Always expect Kanok Miah entity
    expected.append('Kanok Miah')
    
    # Check each entity
    results = {}
    for entity in expected:
        if entity.lower() in content.lower():
            results[entity] = True
        else:
            results[entity] = False
    
    return results

def detect_pillar_topic(tags_str, slug, content):
    """Determine pillar topic and check for pillar links."""
    # Common pillar topics
    pillar_pages = {
        'seo-guide': '/blog/complete-seo-guide-bangladesh-businesses-2026',
        'local-seo': '/blog/local-seo-tips-dhaka-businesses-google-maps',
        'technical-seo': '/blog/technical-seo-checklist-bangladeshi-websites',
        'ecommerce-seo': '/blog/why-ecommerce-store-needs-seo-bangladesh',
        'content-marketing': '/blog/content-marketing-strategy-bangladeshi-brands-seo',
        'link-building': '/blog/link-building-strategies-bangladesh-market',
        'mobile-seo': '/blog/mobile-seo-optimization-bangladesh-mobile-first-era',
        'schema': '/blog/schema-markup-rich-snippets-techniques',
        'geo': '/blog/geo-optimization-prepare-business-ai-search',
    }
    
    # Determine which pillar based on slug
    assigned_pillar = None
    pillar_link = None
    
    for key, url in pillar_pages.items():
        if key in slug.lower():
            assigned_pillar = key
            pillar_link = url
            break
    
    # Check if pillar link is in content
    if pillar_link and pillar_link.replace('/blog/', '').split('-')[0] in content.lower():
        has_pillar_link = pillar_link in content
    elif pillar_link:
        has_pillar_link = pillar_link in content
    else:
        has_pillar_link = False
        assigned_pillar = 'unknown'
    
    return assigned_pillar, has_pillar_link, pillar_link

def count_question_headings(content):
    """Count question-based headings (How, What, Why, When, Where, Can, Do, Is, Are)."""
    pattern = re.compile(r'^#{2,4}\s+(How|What|Why|When|Where|Can|Do|Is|Are)\b', re.MULTILINE | re.IGNORECASE)
    matches = pattern.findall(content)
    return len(matches)

def count_internal_links(content):
    """Count internal links to other posts, services, locations."""
    # Links starting with /blog/, /services/, /locations/, /industries/
    internal_pattern = re.compile(r'href="(/(?:blog|services|locations|industries|about|contact)/[^"]*)"')
    links = internal_pattern.findall(content)
    # Also count markdown-style links
    md_pattern = re.compile(r'\[([^\]]+)\]\((/(?:blog|services|locations|industries|about|contact)[^)]*)\)')
    md_links = md_pattern.findall(content)
    return len(links) + len(md_links), links + [l[1] for l in md_links]

# Run checks
report = []

for slug in modified_slugs:
    if slug not in posts:
        report.append(f"## Post: {slug}\n**⚠️ Not found in data.js**\n")
        continue
    
    post = posts[slug]
    title = post['title']
    content = post['content']
    excerpt = post['excerpt']
    date = post['date']
    img = post['imagePlaceholder']
    
    print(f"\n=== Checking: {slug} ===")
    print(f"  Title: {title[:80]}")
    print(f"  Content length: {len(content)} chars")
    
    results = {}
    fixes = []
    
    # A. TF-IDF Coverage
    keyword = extract_primary_keyword(title)
    keyword_count = count_keyword_occurrences(content, keyword)
    tfidf_pass = keyword_count >= 5
    results['TF-IDF'] = ('✅' if tfidf_pass else '❌', f"Keyword: '{keyword}', {keyword_count} occurrences")
    if not tfidf_pass:
        fixes.append(f"- **TF-IDF**: Add more occurrences of primary keyword '{keyword}' (currently {keyword_count}, need ≥5)")
    
    # B. Semantic Entity Coverage
    entity_results = check_entities(content, title, slug)
    missing_entities = [e for e, found in entity_results.items() if not found]
    entities_pass = len(missing_entities) == 0
    entities_detail = f"Missing: {', '.join(missing_entities)}" if missing_entities else "All key entities present"
    results['Entities'] = ('✅' if entities_pass else '❌', entities_detail)
    if not entities_pass:
        fixes.append(f"- **Entities**: Missing: {', '.join(missing_entities)}")
    
    # C. Pillar-Cluster Alignment
    pillar_topic, has_pillar_link, pillar_url = detect_pillar_topic('', slug, content)
    pillar_pass = has_pillar_link
    pillar_detail = f"Pillar: {pillar_topic}"
    if has_pillar_link:
        pillar_detail += f", links to: {pillar_url}"
    else:
        pillar_detail += f", no pillar link found"
    results['Pillar Link'] = ('✅' if pillar_pass else '❌', pillar_detail)
    if not pillar_pass and pillar_url:
        fixes.append(f"- **Pillar Link**: Add link to pillar page {pillar_url}")
    
    # D. AEO/GEO Optimization
    q_count = count_question_headings(content)
    aeo_pass = q_count >= 2
    results['AEO/GEO'] = ('✅' if aeo_pass else '❌', f"{q_count} question headings")
    if not aeo_pass:
        fixes.append(f"- **AEO/GEO**: Add more question-based headings (currently {q_count}, need ≥2)")
    
    # E. Internal Linking
    internal_count, internal_links = count_internal_links(content)
    internal_pass = internal_count >= 3
    results['Internal Links'] = ('✅' if internal_pass else '❌', f"{internal_count} total internal links")
    if not internal_pass:
        fixes.append(f"- **Internal Links**: Add more internal links (currently {internal_count}, need ≥3)")
    
    # F. Schema Ready
    schema_missing = []
    if not title: schema_missing.append('title')
    if not excerpt: schema_missing.append('excerpt')
    if not date: schema_missing.append('date')
    schema_pass = len(schema_missing) == 0
    schema_detail = f"All fields set" if schema_pass else f"Missing: {', '.join(schema_missing)}"
    results['Schema Ready'] = ('✅' if schema_pass else '❌', schema_detail)
    if not schema_pass:
        fixes.append(f"- **Schema**: Missing fields: {', '.join(schema_missing)}")
    
    # Build report section
    section = f"## Post: {slug}\n"
    section += f"**Title:** {title}\n\n"
    section += "| Check | Status | Details |\n"
    section += "|-------|--------|--------|\n"
    for check_name, (status, detail) in results.items():
        section += f"| {check_name} | {status} | {detail} |\n"
    
    if fixes:
        section += "\n### Fix instructions:\n"
        for fix in fixes:
            section += fix + "\n"
    else:
        section += "\n### ✅ All checks passed!\n"
    
    report.append(section)
    print(f"  Results: TF-IDF={'✅' if tfidf_pass else '❌'} Entities={'✅' if entities_pass else '❌'} Pillar={'✅' if pillar_pass else '❌'} AEO={'✅' if aeo_pass else '❌'} Internal={'✅' if internal_pass else '❌'} Schema={'✅' if schema_pass else '❌'}")

# Generate full report
full_report = """# Content Framework Enforcement Report
**Date:** 2026-07-26
**Project:** kanokmiah.com.bd
**Trigger:** Blog posts modified in last 48 hours

---

"""
full_report += '\n\n'.join(report)

# Summary
total_posts = len([s for s in modified_slugs if s in posts])
passed_all = sum(1 for s in modified_slugs if s in posts and all([
    count_keyword_occurrences(posts[s]['content'], extract_primary_keyword(posts[s]['title'])) >= 5,
    len([e for e, f in check_entities(posts[s]['content'], posts[s]['title'], s).items() if not f]) == 0,
    detect_pillar_topic('', s, posts[s]['content'])[1],
    count_question_headings(posts[s]['content']) >= 2,
    count_internal_links(posts[s]['content'])[0] >= 3,
    bool(posts[s]['title'] and posts[s]['excerpt'] and posts[s]['date'])
]))

summary_section = f"""
---
## Executive Summary
- **Posts checked:** {total_posts}
- **All checks passed:** {passed_all}/{total_posts}
"""
full_report += summary_section

with open('_cron_framework_report_2026-07-26.md', 'w') as f:
    f.write(full_report)

print(f"\n\nReport written to _cron_framework_report_2026-07-26.md")
print(summary_section)
