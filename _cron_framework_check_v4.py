#!/usr/bin/env python3
"""Content Framework Enforcer v4 - refined heuristics."""

import re, json

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
    posts = {}
    blocks = re.split(r'(?={\s*\n\s*slug:\s*")', text)
    for block in blocks[1:]:
        slug_m = re.search(r'slug:\s*"([^"]+)"', block)
        if not slug_m: continue
        slug = slug_m.group(1)
        title_m = re.search(r'title:\s*"([^"]*)"', block)
        title = title_m.group(1) if title_m else ''
        date_m = re.search(r'date:\s*"([^"]*)"', block)
        date = date_m.group(1) if date_m else ''
        author_m = re.search(r'author:\s*"([^"]*)"', block)
        author = author_m.group(1) if author_m else ''
        excerpt_m = re.search(r'excerpt:\s*"([^"]*)"', block, re.DOTALL)
        excerpt = excerpt_m.group(1).replace('\n', ' ').strip() if excerpt_m else ''
        tags_m = re.search(r'tags:\s*\[([^\]]*)\]', block, re.DOTALL)
        tags = re.findall(r'"([^"]*)"', tags_m.group(1)) if tags_m else []
        img_m = re.search(r'imagePlaceholder:\s*"([^"]*)"', block)
        img = img_m.group(1) if img_m else ''
        content_m = re.search(r'content:\s*`([^`]*)`', block, re.DOTALL)
        content = content_m.group(1) if content_m else ''
        posts[slug] = {'slug': slug, 'title': title, 'date': date, 'author': author,
                       'excerpt': excerpt, 'tags': tags, 'imagePlaceholder': img, 'content': content}
    return posts

posts = extract_posts(raw)
print(f"Extracted {len(posts)} posts")

# ========== IMPROVED KEYWORD EXTRACTION ==========
def get_primary_keyword(slug, title, tags):
    """Extract a meaningful primary keyword for TF-IDF check."""
    tl = title.lower()
    
    # Manual overrides for known patterns
    keyword_map = {
        'geo-optimization': 'GEO',
        'seo-garments-textile': 'Garments SEO',
        'seo-healthcare': 'Healthcare SEO',
        'mobile-seo-optimization': 'Mobile SEO',
        'seo-expert-vs-seo-agency': 'SEO Expert vs SEO Agency',
        'top-10-seo-mistakes': 'SEO Mistakes',
        'hiring-seo-expert': 'SEO Expert Dhaka',
        'ai-seo-2026': 'AI SEO',
        'why-md-kanok-miah': 'Kanok Miah SEO',
        'how-to-choose-best-seo-expert': 'SEO Expert Dhaka',
        'what-does-seo-expert-do': 'SEO Expert',
        'seo-case-study-dhaka': 'SEO Case Study Dhaka',
        'locksmith-dundee': 'Locksmith SEO',
        'landlord-certificates': 'Landlord Certificates SEO',
        'das-taxis-scotland': 'Taxi SEO',
        'morethanpanel': 'SMM Panel SEO',
        'smmgen': 'SMM Panel SEO',
        'smmsun': 'SMM Panel SEO',
        'mir-cement': 'B2B SEO',
        'dhaka-apparels': 'Garments SEO',
        'stealth-windshield': 'Local SEO',
    }
    for key, kw in keyword_map.items():
        if key in slug: return kw
    
    # Generic extractors
    m = re.search(r'SEO\s+for\s+([A-Za-z].+)', title)
    if m: return m.group(1).strip().rstrip('.:;,').split(' in')[0].split(' –')[0].split(' —')[0]
    
    return title.split(':')[0].strip().rstrip('.:;,')

# ========== ENTITY CHECK ==========
def check_entities(content, slug, title):
    """Check entities, being aware of UK case studies."""
    cl = content.lower()
    is_uk_case = any(uk in slug for uk in ['dundee', 'scotland', 'uk', 'landlord', 'locksmith'])
    is_bd_focused = any(bd in slug for bd in ['bangladesh', 'dhaka', 'bd'])
    
    missing = []
    
    # Bangladesh entity (not expected for UK cases)
    if is_bd_focused and 'bangladesh' not in cl:
        missing.append('Bangladesh')
    elif is_bd_focused and 'dhaka' not in cl and 'dhaka' in slug:
        missing.append('Dhaka')
    
    # Kanok Miah (only for BD content or about pages)
    if not is_uk_case and 'kanok miah' not in cl:
        missing.append('Kanok Miah')
    
    # Industry-specific
    industry_checks = [
        ('healthcare', ['Healthcare', 'Medical', 'Patient']),
        ('medical', ['Healthcare', 'Medical', 'Clinic']),
        ('garment', ['Garment', 'Textile', 'Apparel']),
        ('textile', ['Garment', 'Textile', 'B2B']),
        ('ecommerce', ['E-commerce', 'Online Store']),
        ('real-estate', ['Real Estate']),
        ('fitness', ['Fitness', 'Gym']),
        ('travel', ['Travel', 'Tourism']),
        ('tourism', ['Travel', 'Tourism']),
        ('education', ['Education', 'Educational']),
        ('restaurant', ['Restaurant', 'Cafe']),
        ('schema', ['Schema', 'Structured Data']),
        ('link-building', ['Link Building']),
        ('content-marketing', ['Content Marketing']),
        ('technical-seo', ['Technical SEO']),
        ('geo', ['Generative Engine', 'GEO']),
    ]
    for key, entities in industry_checks:
        if key in slug:
            found = any(e.lower() in cl for e in entities)
            if not found:
                missing.extend(entities[:2])
            break
    
    return missing

# ========== PILLAR LINK CHECK ==========
def check_pillar(slug, content):
    """Check pillar alignment. If post IS the pillar, check it links to its cluster."""
    pillar_map = {
        'geo-optimization-prepare-business-ai-search': ('/blog/geo-optimization-prepare-business-ai-search', 'GEO'),
        'seo-garments-textile-industry-b2b-lead-generation': ('/blog/seo-garments-textile-industry-b2b-lead-generation', 'Garments SEO'),
        'mobile-seo-optimization-bangladesh-mobile-first-era': ('/blog/mobile-seo-optimization-bangladesh-mobile-first-era', 'Mobile SEO'),
        'seo-healthcare-medical-clinics-bangladesh': ('/blog/seo-healthcare-medical-clinics-bangladesh', 'Healthcare SEO'),
    }
    
    universal_pillar = '/blog/complete-seo-guide-bangladesh-businesses-2026'
    
    # If this post IS a pillar page itself, check it links to subordinate content
    if slug in pillar_map:
        _, name = pillar_map[slug]
        # Check it links to other blog posts (cluster content)
        links = re.findall(r'href="(/blog/[^"]*)"', content)
        links += [m[1] for m in re.findall(r'\[([^\]]+)\]\((/blog/[^)]*)\)', content)]
        other_blog_links = [l for l in links if l != pillar_map[slug][0]]
        has_cluster_links = len(other_blog_links) >= 2
        
        # Also check it links to relevant service pages
        service_links = len(re.findall(r'href="(/services/[^"]*)"', content))
        
        # A pillar page should also link to the universal pillar if different
        links_to_universal = universal_pillar in content
        
        if has_cluster_links:
            return name, True, f"cluster links: {len(other_blog_links)}"
        elif service_links >= 2:
            return name, True, f"service links: {service_links}"
        else:
            return name, False, f"only {len(other_blog_links)} cluster links"
    
    # For non-pillar posts, check if they link to any known pillar
    for ps, (pu, pn) in pillar_map.items():
        if pu in content:
            return pn, True, f"links to {pn} pillar"
    
    # Check universal pillar
    if universal_pillar in content:
        return 'Complete SEO Guide', True, 'links to universal pillar'
    
    return 'unknown', False, 'no pillar link found'

# ========== QUESTION HEADINGS ==========
def count_question_headings(content):
    return len(re.findall(r'^#{2,4}\s+(How|What|Why|When|Where|Can|Do|Is|Are)\b', content, re.MULTILINE | re.IGNORECASE))

# ========== INTERNAL LINKS ==========
def count_internal_links(content):
    html = re.findall(r'href="(/(?:blog|services|locations|industries|about|contact)/[^"]*)"', content)
    md = [m[1] for m in re.findall(r'\[([^\]]+)\]\((/(?:blog|services|locations|industries|about|contact)[^)]*)\)', content)]
    return len(set(html + md))

# ========== RUN CHECKS ==========
report_sections = []
pass_count = 0

for slug in MODIFIED_SLUGS:
    if slug not in posts:
        report_sections.append(f"## Post: {slug}\n**⚠️ Not found in data.js**\n")
        continue
    
    post = posts[slug]
    title = post['title']
    content = post['content']
    
    checks = {}
    fixes = []
    
    # A. TF-IDF
    keyword = get_primary_keyword(slug, title, post['tags'])
    kw_count = len(re.findall(re.escape(keyword), content, re.IGNORECASE))
    # Also check partial matches for multi-word keywords
    if kw_count < 5 and ' ' in keyword:
        words = keyword.split()
        kw_count = sum(1 for w in words if len(w) > 3 and len(re.findall(re.escape(w), content, re.IGNORECASE)) >= 3)
    else:
        pass
    
    kw_pass = kw_count >= 5
    checks['TF-IDF'] = ('✅' if kw_pass else '❌', f"Keyword: '{keyword}', ~{kw_count} occurrences")
    if not kw_pass:
        fixes.append(f"- **TF-IDF**: Increase '{keyword}' occurrences from ~{kw_count} to ≥5")
    
    # B. Entities
    missing_ents = check_entities(content, slug, title)
    ent_pass = len(missing_ents) == 0
    checks['Entities'] = ('✅' if ent_pass else '❌',
        "All present ✓" if ent_pass else f"Missing: {', '.join(missing_ents)}")
    if not ent_pass:
        fixes.append(f"- **Entities**: Add mentions of: {', '.join(missing_ents)}")
    
    # C. Pillar
    pillar_name, pillar_pass, pillar_detail = check_pillar(slug, content)
    checks['Pillar'] = ('✅' if pillar_pass else '❌', f"{pillar_name}: {pillar_detail}")
    if not pillar_pass:
        fixes.append(f"- **Pillar**: Link to a pillar page (e.g., Complete SEO Guide or industry-specific pillar)")
    
    # D. AEO/GEO
    q_count = count_question_headings(content)
    aeo_pass = q_count >= 2
    checks['AEO/GEO'] = ('✅' if aeo_pass else '❌', f"{q_count} question headings")
    if not aeo_pass:
        fixes.append(f"- **AEO/GEO**: Add ≥2 question-based headings (currently {q_count})")
    
    # E. Internal Links
    link_count = count_internal_links(content)
    link_pass = link_count >= 3
    checks['Internal Links'] = ('✅' if link_pass else '❌', f"{link_count} internal links")
    if not link_pass:
        fixes.append(f"- **Internal Links**: Add ≥3 internal links (currently {link_count})")
    
    # F. Schema
    schema_missing = []
    if not post['title']: schema_missing.append('title')
    if not post['excerpt']: schema_missing.append('excerpt')
    if not post['date']: schema_missing.append('date')
    schema_pass = len(schema_missing) == 0
    checks['Schema'] = ('✅' if schema_pass else '❌',
        "All fields set ✓" if schema_pass else f"Missing: {', '.join(schema_missing)}")
    if not schema_pass:
        fixes.append(f"- **Schema**: Missing fields: {', '.join(schema_missing)}")
    
    all_pass = all([kw_pass, ent_pass, pillar_pass, aeo_pass, link_pass, schema_pass])
    if all_pass: pass_count += 1
    
    section = f"## Post: {slug}\n**Title:** {title}\n\n"
    section += "| Check | Status | Details |\n|-------|--------|--------|\n"
    for cn, (st, dt) in checks.items():
        section += f"| {cn} | {st} | {dt} |\n"
    if not all_pass and fixes:
        section += "\n### Fix instructions:\n" + '\n'.join(fixes) + '\n'
    elif all_pass:
        section += "\n### ✅ All checks passed!\n"
    report_sections.append(section)

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

print(report)
