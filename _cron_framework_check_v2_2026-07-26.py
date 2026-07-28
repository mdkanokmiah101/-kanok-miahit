#!/usr/bin/env python3
"""Content Framework Enforcer v2 - handles actual data.js format."""

import re
import json

with open('src/app/blog/data.js', 'r') as f:
    raw = f.read()

# Slugs we know were modified (from git log analysis)
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

def extract_posts_robust(text):
    """Extract all blog posts from data.js using a more robust approach."""
    posts = {}
    
    # Strategy: Find each post block by splitting on "{slug:"
    # Then extract fields with regex
    blocks = re.split(r'(?={slug:\s*")', text)
    
    for block in blocks:
        # Extract slug
        slug_m = re.search(r'slug:\s*"([^"]+)"', block)
        if not slug_m:
            continue
        slug = slug_m.group(1)
        
        # Extract title
        title_m = re.search(r'title:\s*"([^"]*)"', block)
        title = title_m.group(1) if title_m else ''
        
        # Extract date
        date_m = re.search(r'date:\s*"([^"]*)"', block)
        date = date_m.group(1) if date_m else ''
        
        # Extract author
        author_m = re.search(r'author:\s*"([^"]*)"', block)
        author = author_m.group(1) if author_m else ''
        
        # Extract excerpt (may span multiple lines)
        excerpt_m = re.search(r'excerpt:\s*"([^"]*)"', block, re.DOTALL)
        excerpt = excerpt_m.group(1).strip() if excerpt_m else ''
        
        # Extract tags
        tags_m = re.search(r'tags:\s*\[([^\]]*)\]', block)
        tags = []
        if tags_m:
            tags = re.findall(r'"([^"]+)"', tags_m.group(1))
        
        # Extract imagePlaceholder
        img_m = re.search(r'imagePlaceholder:\s*"([^"]*)"', block)
        img = img_m.group(1) if img_m else ''
        
        # Extract content (between backticks, may span many lines)
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
posts = extract_posts_robust(raw)
print(f"Extracted {len(posts)} posts")

# Verify our target posts exist
for s in MODIFIED_SLUGS:
    if s in posts:
        p = posts[s]
        print(f"  ✓ {s}: title='{p['title'][:60]}...' content={len(p['content'])} chars tags={p['tags']}")
    else:
        print(f"  ✗ {s}: NOT FOUND")

# --- Framework Check Functions ---

def extract_primary_keyword(title, slug, tags):
    """Extract primary keyword from title."""
    title_lower = title.lower()
    
    # Specialized patterns for this site's content
    if 'healthcare seo' in title_lower:
        return 'Healthcare SEO'
    if 'mobile seo' in title_lower and 'mobile-first' in title_lower:
        return 'Mobile SEO'
    if 'geo' in title_lower or 'generative engine' in title_lower:
        return 'GEO Optimization'
    if 'garment' in title_lower or 'textile' in title_lower:
        return 'Garments Textile SEO'
    if 'seo for' in title_lower:
        m = re.search(r'SEO\s+for\s+([A-Za-z].*)', title, re.IGNORECASE)
        if m:
            kw = m.group(1).strip().rstrip('.')
            return kw.split(' in ')[0].strip()
    if 'seo' in title_lower:
        # Get the main noun before/after SEO
        m = re.search(r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+SEO', title)
        if m:
            return m.group(1) + ' SEO'
    # Fall back to first 2 words
    words = title.split()[:3]
    return ' '.join(words)

def count_occurrences(content, keyword):
    """Count case-insensitive occurrences."""
    if not keyword:
        return 0
    return len(re.findall(re.escape(keyword), content, re.IGNORECASE))

def check_entities(content, slug, title):
    """Check semantic entities."""
    content_lower = content.lower()
    expected = []
    missing = []
    
    # Always expect Bangladesh
    if 'bangladesh' not in content_lower:
        missing.append('Bangladesh')
    expected.append('Bangladesh')
    
    # Dhaka for local posts
    if 'dhaka' in slug.lower():
        if 'dhaka' not in content_lower:
            missing.append('Dhaka')
        expected.append('Dhaka')
    
    # Check for Kanok Miah
    if 'kanok miah' not in content_lower:
        missing.append('Kanok Miah')
    expected.append('Kanok Miah')
    
    # Industry-specific entities
    industry_map = [
        ('healthcare', ['Healthcare', 'Medical', 'Patient']),
        ('medical', ['Healthcare', 'Medical', 'Clinic']),
        ('garment', ['Garment', 'Textile', 'Manufacturing']),
        ('textile', ['Garment', 'Textile', 'B2B']),
        ('mobile', ['Mobile', 'Smartphone']),
        ('ecommerce', ['E-commerce', 'Online Store']),
        ('real-estate', ['Real Estate', 'Property']),
        ('law', ['Law Firm', 'Legal']),
        ('fitness', ['Fitness', 'Gym']),
        ('travel', ['Travel', 'Tourism']),
        ('tourism', ['Travel', 'Tourism']),
        ('education', ['Education', 'Educational']),
        ('startup', ['Startup']),
        ('hotel', ['Hotel', 'Resort']),
        ('restaurant', ['Restaurant', 'Cafe']),
        ('ngo', ['NGO', 'Non-profit']),
        ('photograph', ['Photography']),
        ('wedding', ['Wedding']),
        ('event', ['Event']),
        ('schema', ['Schema', 'Structured Data']),
        ('link-building', ['Link Building', 'Backlink']),
        ('content-marketing', ['Content Marketing']),
        ('technical-seo', ['Technical SEO']),
        ('geo', ['GEO', 'Generative Engine']),
        ('case-study', ['Case Study']),
    ]
    
    for key, entities in industry_map:
        if key in slug.lower():
            for ent in entities:
                if ent.lower() not in content_lower:
                    missing.append(ent)
                expected.append(ent)
            break
    
    # Service entities
    service_map = [
        ('local-seo', 'Local SEO'),
        ('on-page-seo', 'On-Page SEO'),
        ('technical-seo', 'Technical SEO'),
        ('ecommerce', 'E-commerce SEO'),
        ('link-building', 'Link Building'),
    ]
    for key, ent in service_map:
        if key in slug.lower():
            if ent.lower() not in content_lower:
                missing.append(ent)
            expected.append(ent)
            break
    
    return expected, missing

def check_pillar_link(slug, content, tags):
    """Check pillar-cluster alignment."""
    pillar_map = {
        'seo-guide': ('/blog/complete-seo-guide-bangladesh-businesses-2026', 'Complete SEO Guide'),
        'local-seo': ('/blog/local-seo-tips-dhaka-businesses-google-maps', 'Local SEO Guide'),
        'technical-seo': ('/blog/technical-seo-checklist-bangladeshi-websites', 'Technical SEO Checklist'),
        'ecommerce': ('/blog/why-ecommerce-store-needs-seo-bangladesh', 'E-commerce SEO Guide'),
        'content-marketing': ('/blog/content-marketing-strategy-bangladeshi-brands-seo', 'Content Marketing Guide'),
        'link-building': ('/blog/link-building-strategies-bangladesh-market', 'Link Building Guide'),
        'mobile-seo': ('/blog/mobile-seo-optimization-bangladesh-mobile-first-era', 'Mobile SEO Guide'),
        'schema': ('/blog/schema-markup-rich-snippets-techniques', 'Schema Guide'),
        'geo': ('/blog/geo-optimization-prepare-business-ai-search', 'GEO Guide'),
        'healthcare': ('/blog/seo-healthcare-medical-clinics-bangladesh', 'Healthcare SEO Guide'),
        'garment': ('/blog/seo-garments-textile-industry-b2b-lead-generation', 'Garments SEO Guide'),
    }
    
    assigned = None
    pillar_url = None
    pillar_name = None
    
    for key, (url, name) in pillar_map.items():
        if key in slug.lower():
            assigned = key
            pillar_url = url
            pillar_name = name
            break
    
    if not assigned:
        # Check if the "complete-seo-guide" pillar link exists (universal pillar)
        if '/blog/complete-seo-guide-bangladesh-businesses-2026' in content:
            return 'seo-guide (Complete SEO Guide)', True, '/blog/complete-seo-guide-bangladesh-businesses-2026'
        return 'unknown', False, None
    
    has_link = pillar_url in content if pillar_url else False
    
    # If no direct pillar link, check if they link to the complete seo guide as fallback
    if not has_link and '/blog/complete-seo-guide-bangladesh-businesses-2026' in content:
        return f"{assigned} (links to Complete SEO Guide instead)", True, '/blog/complete-seo-guide-bangladesh-businesses-2026'
    
    return assigned, has_link, pillar_url

def count_question_headings(content):
    """Count question-based headings."""
    pattern = re.compile(r'^#{2,4}\s+(How|What|Why|When|Where|Can|Do|Is|Are)\b', re.MULTILINE | re.IGNORECASE)
    return len(pattern.findall(content))

def count_internal_links(content):
    """Count internal links."""
    # HTML-style href links to /blog/, /services/, /locations/, /industries/, /about/, /contact/
    html_pattern = re.compile(r'href="(/(?:blog|services|locations|industries|about|contact)/[^"]*)"')
    html_links = html_pattern.findall(content)
    
    # Markdown-style links
    md_pattern = re.compile(r'\[([^\]]+)\]\((/(?:blog|services|locations|industries|about|contact)[^)]*)\)')
    md_links = [m[1] for m in md_pattern.findall(content)]
    
    all_links = html_links + md_links
    # Deduplicate
    unique_links = list(set(all_links))
    return len(unique_links), unique_links

# --- Run checks ---
report_sections = []
all_pass_count = 0

for slug in MODIFIED_SLUGS:
    if slug not in posts:
        report_sections.append(f"## Post: {slug}\n**⚠️ Could not be extracted from data.js**\n")
        continue
    
    post = posts[slug]
    title = post['title']
    content = post['content']
    tags = post['tags']
    
    print(f"\n{'='*60}")
    print(f"Checking: {slug}")
    print(f"  Title: {title}")
    
    checks = {}
    fixes = []
    
    # A. TF-IDF Coverage
    keyword = extract_primary_keyword(title, slug, tags)
    kw_count = count_occurrences(content, keyword)
    kw_pass = kw_count >= 5
    checks['TF-IDF'] = ('✅' if kw_pass else '❌', f"Primary keyword: '{keyword}', {kw_count} occurrences in content")
    if not kw_pass:
        fixes.append(f"- **TF-IDF**: Increase '{keyword}' occurrences from {kw_count} to ≥5")
    print(f"  TF-IDF: keyword='{keyword}' count={kw_count} {'✅' if kw_pass else '❌'}")
    
    # B. Semantic Entity Coverage
    expected_entities, missing_entities = check_entities(content, slug, title)
    ent_pass = len(missing_entities) == 0
    if ent_pass:
        ent_detail = f"All expected entities present ✓"
    else:
        ent_detail = f"Missing: {', '.join(missing_entities)}"
    checks['Entities'] = ('✅' if ent_pass else '❌', ent_detail)
    if not ent_pass:
        fixes.append(f"- **Entities**: Missing: {', '.join(missing_entities)}")
    print(f"  Entities: {'✅' if ent_pass else '❌'} missing={missing_entities}")
    
    # C. Pillar-Cluster Alignment
    pillar_topic, pillar_pass, pillar_url = check_pillar_link(slug, content, tags)
    if pillar_pass:
        pillar_detail = f"Pillar: {pillar_topic}, links to: {pillar_url}"
    else:
        if pillar_url:
            pillar_detail = f"Pillar: {pillar_topic}, NO link to {pillar_url}"
        else:
            pillar_detail = f"Pillar: {pillar_topic}, no pillar page identified"
    checks['Pillar Link'] = ('✅' if pillar_pass else '❌', pillar_detail)
    if not pillar_pass and pillar_url:
        fixes.append(f"- **Pillar Link**: Add link to pillar page {pillar_url}")
    print(f"  Pillar: {'✅' if pillar_pass else '❌'} topic={pillar_topic} url={pillar_url}")
    
    # D. AEO/GEO Optimization
    q_count = count_question_headings(content)
    aeo_pass = q_count >= 2
    checks['AEO/GEO'] = ('✅' if aeo_pass else '❌', f"{q_count} question-based headings (H2-H4 starting with How/What/Why/When/Where/Can/Do/Is/Are)")
    if not aeo_pass:
        fixes.append(f"- **AEO/GEO**: Add ≥2 question-based headings (currently {q_count})")
    print(f"  AEO/GEO: {'✅' if aeo_pass else '❌'} {q_count} question headings")
    
    # E. Internal Linking
    link_count, link_list = count_internal_links(content)
    link_pass = link_count >= 3
    checks['Internal Links'] = ('✅' if link_pass else '❌', f"{link_count} unique internal links to /blog/, /services/, /locations/, /industries/, /about/, /contact/")
    if not link_pass:
        fixes.append(f"- **Internal Links**: Add ≥3 internal links (currently {link_count})")
    print(f"  Internal Links: {'✅' if link_pass else '❌'} {link_count} links")
    
    # F. Schema Ready
    schema_missing = []
    if not post['title']: schema_missing.append('title')
    if not post['excerpt']: schema_missing.append('excerpt')
    if not post['date']: schema_missing.append('date')
    if not post['imagePlaceholder']: schema_missing.append('imagePlaceholder')
    schema_pass = len(schema_missing) == 0
    if schema_pass:
        schema_detail = f"All ArticleSchema fields set ✓"
    else:
        schema_detail = f"Missing: {', '.join(schema_missing)}"
    checks['Schema Ready'] = ('✅' if schema_pass else '❌', schema_detail)
    if not schema_pass:
        fixes.append(f"- **Schema**: Missing required fields: {', '.join(schema_missing)}")
    print(f"  Schema: {'✅' if schema_pass else '❌'} missing={schema_missing}")
    
    # Determine overall pass
    all_pass = all([kw_pass, ent_pass, pillar_pass, aeo_pass, link_pass, schema_pass])
    if all_pass:
        all_pass_count += 1
    
    # Build section
    section = f"## Post: {slug}\n"
    section += f"**Title:** {title}\n\n"
    section += "| Check | Status | Details |\n"
    section += "|-------|--------|--------|\n"
    for check_name, (status, detail) in checks.items():
        section += f"| {check_name} | {status} | {detail} |\n"
    
    if fixes:
        section += "\n### Fix instructions:\n"
        for fix in fixes:
            section += fix + "\n"
    else:
        section += "\n### ✅ All checks passed!\n"
    
    report_sections.append(section)

# --- Generate report ---
total_checked = len([s for s in MODIFIED_SLUGS if s in posts])
report = """# 🏗️ Content Framework Enforcement Report
**Date:** 2026-07-26
**Project:** kanokmiah.com.bd
**Trigger:** Blog posts modified in last 48 hours

---

"""
report += '\n\n---\n\n'.join(report_sections)

report += f"""
---
## 📊 Executive Summary
- **Posts checked:** {total_checked}
- **All checks passed:** {all_pass_count}/{total_checked}
"""

# Write report
with open('_cron_framework_report_2026-07-26.md', 'w') as f:
    f.write(report)

print(f"\n{'='*60}")
print(f"Report saved to _cron_framework_report_2026-07-26.md")
print(f"Total checked: {total_checked}, All passed: {all_pass_count}/{total_checked}")
print(f"\n---REPORT START---")
print(report)
print(f"---REPORT END---")
