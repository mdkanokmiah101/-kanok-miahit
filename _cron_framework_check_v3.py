#!/usr/bin/env python3
"""Content Framework Enforcer v3 - robust parser for data.js format."""

import re
import json

with open('src/app/blog/data.js', 'r') as f:
    raw = f.read()

MODIFIED_SLUGS = [
    "geo-optimization-prepare-business-ai-search",
    "seo-garments-textile-industry-b2b-lead-generation",
    "mobile-seo-optimization-bangladesh-mobile-first-era",
    "seo-healthcare-medical-clinics-bangladesh",
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

def extract_posts(text):
    """Extract posts using regex block splitting."""
    posts = {}
    blocks = re.split(r'(?={\s*\n\s*slug:\s*")', text)
    
    for block in blocks[1:]:  # Skip preamble
        # Slug
        slug_m = re.search(r'slug:\s*"([^"]+)"', block)
        if not slug_m:
            continue
        slug = slug_m.group(1)
        
        # Title
        title_m = re.search(r'title:\s*"([^"]*)"', block)
        title = title_m.group(1) if title_m else ''
        
        # Date
        date_m = re.search(r'date:\s*"([^"]*)"', block)
        date = date_m.group(1) if date_m else ''
        
        # Author
        author_m = re.search(r'author:\s*"([^"]*)"', block)
        author = author_m.group(1) if author_m else ''
        
        # Excerpt (can span lines, use DOTALL)
        excerpt_m = re.search(r'excerpt:\s*"([^"]*)"', block, re.DOTALL)
        excerpt = excerpt_m.group(1).replace('\n', ' ').strip() if excerpt_m else ''
        
        # Tags (array of strings)
        tags_m = re.search(r'tags:\s*\[([^\]]*)\]', block, re.DOTALL)
        tags = []
        if tags_m:
            tags = re.findall(r'"([^"]*)"', tags_m.group(1))
        
        # imagePlaceholder
        img_m = re.search(r'imagePlaceholder:\s*"([^"]*)"', block)
        img = img_m.group(1) if img_m else ''
        
        # Content (between backticks)
        content_m = re.search(r'content:\s*`([^`]*)`', block, re.DOTALL)
        content = content_m.group(1) if content_m else ''
        
        posts[slug] = {
            'slug': slug,
            'title': title,
            'date': date,
            'author': author,
            'excerpt': excerpt,
            'tags': tags,
            'imagePlaceholder': img,
            'content': content,
        }
    
    return posts

print("Parsing data.js...")
posts = extract_posts(raw)
print(f"Extracted {len(posts)} posts")

# Verify target posts
for s in MODIFIED_SLUGS:
    if s in posts:
        p = posts[s]
        print(f"  ✓ {s}: title='{p['title'][:60]}' content={len(p['content'])} chars tags={p['tags'][:3]}")
    else:
        print(f"  ✗ {s}: NOT FOUND")

# --- Framework check functions ---

def extract_primary_keyword(title, slug, tags):
    """Extract primary keyword from title."""
    tl = title.lower()
    if 'healthcare seo' in tl: return 'Healthcare SEO'
    if 'mobile seo' in tl and ('mobile-first' in tl or 'mobile first' in tl): return 'Mobile SEO'
    if 'geo' in tl or 'generative engine' in tl: return 'GEO'
    if 'garment' in tl or 'textile' in tl: return 'Garments Textile SEO'
    if 'seo for' in tl:
        m = re.search(r'SEO\s+for\s+(.+)', title, re.IGNORECASE)
        if m: return m.group(1).strip().rstrip('.').split(' in ')[0].strip()
    m = re.search(r'((?:Local|Technical|E-commerce|Mobile|Healthcare|International|Voice|Affiliate|Youtube|Video|Content)\s+SEO)', title, re.IGNORECASE)
    if m: return m.group(1)
    m = re.search(r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+SEO', title)
    if m: return m.group(1) + ' SEO'
    words = title.split()[:3]
    return ' '.join(words)

def count_occurrences(content, keyword):
    if not keyword: return 0
    return len(re.findall(re.escape(keyword), content, re.IGNORECASE))

def check_entities(content, slug):
    """Check for required entities."""
    cl = content.lower()
    missing = []
    
    # Always expected
    if 'bangladesh' not in cl and 'Bangladesh' not in content: missing.append('Bangladesh')
    if 'kanok miah' not in cl: missing.append('Kanok Miah')
    
    # Location-specific
    if 'dhaka' in slug.lower() and 'dhaka' not in cl: missing.append('Dhaka')
    
    # Industry entities
    industry_checks = [
        ('healthcare', ['Healthcare', 'Medical']),
        ('medical', ['Healthcare', 'Medical', 'Clinic']),
        ('garment', ['Garment', 'Textile']),
        ('textile', ['Garment', 'Textile']),
        ('ecommerce', ['E-commerce', 'Online Store']),
        ('real-estate', ['Real Estate']),
        ('law', ['Law Firm', 'Legal']),
        ('fitness', ['Fitness', 'Gym']),
        ('travel', ['Travel', 'Tourism']),
        ('tourism', ['Travel', 'Tourism']),
        ('education', ['Education', 'Educational']),
        ('startup', ['Startup']),
        ('hotel', ['Hotel', 'Resort']),
        ('restaurant', ['Restaurant', 'Cafe']),
        ('ngo', ['NGO']),
        ('photograph', ['Photography']),
        ('wedding', ['Wedding']),
        ('event', ['Event Management']),
        ('schema', ['Schema', 'Structured Data']),
        ('link-building', ['Link Building']),
        ('content-marketing', ['Content Marketing']),
        ('technical-seo', ['Technical SEO']),
        ('geo', ['GEO', 'Generative Engine']),
        ('case-study', ['Case Study']),
        ('mobile-seo', ['Mobile SEO']),
    ]
    for key, entities in industry_checks:
        if key in slug.lower():
            for ent in entities:
                if ent.lower() not in content.lower():
                    missing.append(ent)
            break
    
    # Service entities
    service_checks = [
        ('local-seo', 'Local SEO'),
        ('on-page-seo', 'On-Page SEO'),
        ('technical-seo', 'Technical SEO'),
        ('ecommerce', 'E-commerce SEO'),
        ('link-building', 'Link Building'),
    ]
    for key, ent in service_checks:
        if key in slug.lower() and ent.lower() not in content.lower():
            missing.append(ent)
            break
    
    return missing

def check_pillar_link(slug, content):
    """Check pillar-cluster alignment."""
    pillar_map = {
        'seo-guide': '/blog/complete-seo-guide-bangladesh-businesses-2026',
        'local-seo': '/blog/local-seo-tips-dhaka-businesses-google-maps',
        'technical-seo': '/blog/technical-seo-checklist-bangladeshi-websites',
        'ecommerce': '/blog/why-ecommerce-store-needs-seo-bangladesh',
        'content-marketing': '/blog/content-marketing-strategy-bangladeshi-brands-seo',
        'link-building': '/blog/link-building-strategies-bangladesh-market',
        'mobile-seo': '/blog/mobile-seo-optimization-bangladesh-mobile-first-era',
        'schema': '/blog/schema-markup-rich-snippets-techniques',
        'geo': '/blog/geo-optimization-prepare-business-ai-search',
        'healthcare': '/blog/seo-healthcare-medical-clinics-bangladesh',
        'garment': '/blog/seo-garments-textile-industry-b2b-lead-generation',
        'textile': '/blog/seo-garments-textile-industry-b2b-lead-generation',
    }
    for key, url in pillar_map.items():
        if key in slug.lower():
            has_link = url in content
            return key, has_link, url
    
    # Fallback: check if links to complete-seo-guide (universal pillar)
    universal = '/blog/complete-seo-guide-bangladesh-businesses-2026'
    if universal in content:
        return 'seo-guide (universal)', True, universal
    return 'unknown', False, None

def count_question_headings(content):
    pattern = re.compile(r'^#{2,4}\s+(How|What|Why|When|Where|Can|Do|Is|Are)\b', re.MULTILINE | re.IGNORECASE)
    return len(pattern.findall(content))

def count_internal_links(content):
    html = re.findall(r'href="(/(?:blog|services|locations|industries|about|contact)/[^"]*)"', content)
    md = [m[1] for m in re.findall(r'\[([^\]]+)\]\((/(?:blog|services|locations|industries|about|contact)[^)]*)\)', content)]
    all_links = list(set(html + md))
    return len(all_links), all_links

# --- Run checks ---
report_sections = []
pass_count = 0

for slug in MODIFIED_SLUGS:
    if slug not in posts:
        report_sections.append(f"## Post: {slug}\n**⚠️ Not found in data.js**\n")
        continue
    
    post = posts[slug]
    title = post['title']
    content = post['content']
    tags = post['tags']
    
    checks = {}
    fixes = []
    
    # A. TF-IDF Coverage
    keyword = extract_primary_keyword(title, slug, tags)
    kw_count = count_occurrences(content, keyword)
    kw_pass = kw_count >= 5
    checks['TF-IDF'] = ('✅' if kw_pass else '❌', f"Keyword: '{keyword}', {kw_count} occurrences")
    if not kw_pass:
        fixes.append(f"- **TF-IDF**: Increase '{keyword}' occurrences from {kw_count} to ≥5")
    
    # B. Semantic Entity Coverage
    missing_entities = check_entities(content, slug)
    ent_pass = len(missing_entities) == 0
    ent_detail = "All entities present ✓" if ent_pass else f"Missing: {', '.join(missing_entities)}"
    checks['Entities'] = ('✅' if ent_pass else '❌', ent_detail)
    if not ent_pass:
        fixes.append(f"- **Entities**: Missing: {', '.join(missing_entities)}")
    
    # C. Pillar-Cluster Alignment
    pillar_topic, pillar_pass, pillar_url = check_pillar_link(slug, content)
    if pillar_pass and pillar_url:
        pillar_detail = f"Pillar: {pillar_topic}, links to {pillar_url}"
    elif pillar_url:
        pillar_detail = f"Pillar: {pillar_topic}, missing link to {pillar_url}"
    else:
        pillar_detail = f"Pillar: {pillar_topic}, no pillar page identified"
    checks['Pillar Link'] = ('✅' if pillar_pass else '❌', pillar_detail)
    if not pillar_pass and pillar_url:
        fixes.append(f"- **Pillar Link**: Add link to pillar page {pillar_url}")
    
    # D. AEO/GEO Optimization
    q_count = count_question_headings(content)
    aeo_pass = q_count >= 2
    checks['AEO/GEO'] = ('✅' if aeo_pass else '❌', f"{q_count} question headings")
    if not aeo_pass:
        fixes.append(f"- **AEO/GEO**: Add ≥2 question headings (currently {q_count})")
    
    # E. Internal Linking
    link_count, link_list = count_internal_links(content)
    link_pass = link_count >= 3
    checks['Internal Links'] = ('✅' if link_pass else '❌', f"{link_count} unique internal links")
    if not link_pass:
        fixes.append(f"- **Internal Links**: Add ≥3 internal links (currently {link_count})")
    
    # F. Schema Ready
    schema_missing = []
    if not post['title']: schema_missing.append('title')
    if not post['excerpt']: schema_missing.append('excerpt')
    if not post['date']: schema_missing.append('date')
    schema_pass = len(schema_missing) == 0
    checks['Schema Ready'] = ('✅' if schema_pass else '❌', 
        "All fields set ✓" if schema_pass else f"Missing: {', '.join(schema_missing)}")
    if not schema_pass:
        fixes.append(f"- **Schema**: Missing: {', '.join(schema_missing)}")
    
    all_good = all([kw_pass, ent_pass, pillar_pass, aeo_pass, link_pass, schema_pass])
    if all_good: pass_count += 1
    
    # Build section
    section = f"## Post: {slug}\n**Title:** {title}\n\n"
    section += "| Check | Status | Details |\n|-------|--------|--------|\n"
    for cn, (st, dt) in checks.items():
        section += f"| {cn} | {st} | {dt} |\n"
    if fixes:
        section += "\n### Fix instructions:\n" + '\n'.join(fixes) + '\n'
    else:
        section += "\n### ✅ All checks passed!\n"
    report_sections.append(section)

# Build report
total = len([s for s in MODIFIED_SLUGS if s in posts])
report = f"""# 🏗️ Content Framework Enforcement Report
**Date:** 2026-07-26
**Project:** kanokmiah.com.bd
**Trigger:** Blog posts modified in last 48 hours

---

"""
report += '\n\n---\n\n'.join(report_sections)
report += f"""
---
## 📊 Executive Summary
- **Posts checked:** {total}
- **All checks passed:** {pass_count}/{total}
"""

with open('_cron_framework_report_2026-07-26.md', 'w') as f:
    f.write(report)

print(f"\nReport written ({total} posts, {pass_count} all-pass)")
print(report)
