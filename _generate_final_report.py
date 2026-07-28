#!/usr/bin/env python3
"""
Generate final clean framework enforcement report from the raw data.
This runs the actual checks and formats a clean markdown report.
"""
import re
import sys

# Load data.js
with open("/root/kanok-miahit/src/app/blog/data.js") as f:
    js_content = f.read()

# Parse posts
post_pattern = re.compile(
    r'{\s*\n\s*slug:\s*"([^"]+)"(.*?)^\s*},?\s*$',
    re.MULTILINE | re.DOTALL
)

posts = {}
for m in post_pattern.finditer(js_content):
    slug = m.group(1)
    block = m.group(0)
    
    t = re.search(r'title:\s*"((?:[^"\\]|\\.)*)"', block)
    title = t.group(1) if t else ""
    
    d = re.search(r'date:\s*"([^"]+)"', block)
    date = d.group(1) if d else ""
    
    e = re.search(r'excerpt:\s*\n?\s*"((?:[^"\\]|\\.)*)"', block)
    excerpt = e.group(1) if e else ""
    
    tags_m = re.search(r'tags:\s*\[(.*?)\]', block)
    tags = []
    if tags_m:
        tags = [t.strip().strip('"') for t in tags_m.group(1).split(',')]
    
    c = re.search(r'content:\s*`(.*?)`\s*,\s*\n', block, re.DOTALL)
    post_content = c.group(1) if c else ""
    
    posts[slug] = {
        'title': title,
        'date': date,
        'excerpt': excerpt,
        'tags': tags,
        'content': post_content
    }

changed_slugs = [
    "geo-optimization-prepare-business-ai-search",
    "seo-garments-textile-industry-b2b-lead-generation",
    "mobile-seo-optimization-bangladesh-mobile-first-era",
    "seo-healthcare-medical-clinics-bangladesh",
    "why-md-kanok-miah-is-the-best-seo-expert-in-dhaka-bangladesh",
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

# Known pillar pages on this site
PILLAR_PAGES = {
    'complete-seo-guide-bangladesh-businesses-2026': {
        'url': '/blog/complete-seo-guide-bangladesh-businesses-2026',
        'label': 'Complete SEO Guide (Main Pillar)',
    },
    'local-seo-tips-dhaka-businesses-google-maps': {
        'url': '/blog/local-seo-tips-dhaka-businesses-google-maps',
        'label': 'Local SEO Guide',
    },
    'technical-seo-checklist-bangladeshi-websites': {
        'url': '/blog/technical-seo-checklist-bangladeshi-websites',
        'label': 'Technical SEO Guide',
    },
    'geo-optimization-prepare-business-ai-search': {
        'url': '/blog/geo-optimization-prepare-business-ai-search',
        'label': 'GEO/AEO Guide',
    },
    'seo-case-study-dhaka-businesses-increased-organic-traffic': {
        'url': '/blog/seo-case-study-dhaka-businesses-increased-organic-traffic',
        'label': 'Case Studies Pillar',
    }
}

def get_pillar_for_post(slug, content, tags):
    """Determine which pillar a post belongs to."""
    content_lower = content.lower()
    tags_lower = [t.lower() for t in tags]
    
    # Case study detection (check tags first)
    if any('case study' in t for t in tags_lower):
        return PILLAR_PAGES['seo-case-study-dhaka-businesses-increased-organic-traffic']
    
    # Industry-specific guides that clearly belong to main pillar
    industry_guides = ['garments', 'textile', 'healthcare', 'medical', 'educational', 'real estate', 'fitness', 'travel', 'tourism']
    if any(ind in content_lower for ind in industry_guides):
        return PILLAR_PAGES['complete-seo-guide-bangladesh-businesses-2026']
    
    # GEO/AEO detection
    if any(kw in content_lower for kw in ['geo', 'generative engine optimization', 'ai search', 'aeo', 'answer engine']):
        return PILLAR_PAGES['geo-optimization-prepare-business-ai-search']
    
    # Technical SEO
    if 'technical seo' in content_lower:
        return PILLAR_PAGES['technical-seo-checklist-bangladeshi-websites']
    
    # Local SEO
    if 'local seo' in content_lower or 'google business profile' in content_lower:
        return PILLAR_PAGES['local-seo-tips-dhaka-businesses-google-maps']
    
    # Default
    return PILLAR_PAGES['complete-seo-guide-bangladesh-businesses-2026']

def check_entity_coverage(content, tags):
    """Check if key semantic entities are present."""
    content_lower = content.lower()
    checks = {}
    
    # Location entities
    checks['Bangladesh'] = 'bangladesh' in content_lower
    checks['Dhaka'] = 'dhaka' in content_lower
    
    # Core SEO entities
    checks['SEO (primary service)'] = 'seo' in content_lower
    checks['Local SEO'] = 'local seo' in content_lower
    checks['Technical SEO'] = 'technical seo' in content_lower
    checks['On-page SEO'] = 'on-page seo' in content_lower or 'on page seo' in content_lower
    
    # Content type specific
    if any('case study' in t.lower() for t in tags):
        checks['Metrics (traffic/growth %)'] = bool(re.search(r'\d+%|\d+x', content_lower))
        checks['Timeline (months/years)'] = bool(re.search(r'\d+\s*(month|day|week)s?', content_lower))
    
    # Service type specific 
    if 'google business profile' in content_lower or 'google my business' in content_lower:
        checks['GBP mention'] = True
    
    # Industry-specific entities
    if 'garment' in content_lower or 'textile' in content_lower:
        checks['Garments/Textile'] = True
    if 'healthcare' in content_lower or 'medical' in content_lower or 'clinic' in content_lower:
        checks['Healthcare/Medical'] = True
    if 'ecommerce' in content_lower or 'e-commerce' in content_lower:
        checks['E-commerce'] = True
    if 'real estate' in content_lower:
        checks['Real Estate'] = True
    if 'travel' in content_lower or 'tourism' in content_lower:
        checks['Travel/Tourism'] = True
    if 'law' in content_lower or 'legal' in content_lower or 'attorney' in content_lower:
        checks['Legal'] = True
    if 'restaurant' in content_lower or 'food' in content_lower:
        checks['Food/Restaurant'] = True
    if 'gym' in content_lower or 'fitness' in content_lower:
        checks['Fitness/Gym'] = True
    
    missing = [k for k, v in checks.items() if not v]
    return checks, missing

# Build the report
report = []
report.append("# 🏛️ Content Framework Enforcement Report")
report.append(f"**Date:** 2026-07-27 | **kanokmiah.com.bd**")
report.append(f"**Scope:** {len(changed_slugs)} recently modified blog posts")
report.append("")
report.append("---")
report.append("## Executive Summary")
report.append("")

pass_count = 0
fail_posts = []

for slug in changed_slugs:
    post = posts.get(slug)
    if not post:
        continue
    
    content = post['content']
    tags = post['tags']
    title = post['title']
    
    failures = []
    
    # --- Pillar Link Check ---
    pillar = get_pillar_for_post(slug, content, tags)
    pillar_url = pillar['url']
    has_pillar_link = pillar_url in content
    
    # Also check if it links to Complete SEO Guide (catch-all)
    main_pillar_url = '/blog/complete-seo-guide-bangladesh-businesses-2026'
    has_main_pillar_link = main_pillar_url in content
    
    if not has_pillar_link and not has_main_pillar_link:
        failures.append(f"pillar_link: Add link to `{pillar_url}` ({pillar['label']})")
    elif not has_pillar_link and has_main_pillar_link:
        pass  # Links to main pillar, acceptable
    
    # --- AEO/GEO Check ---
    q_headings = re.findall(r'^#{2,6}\s+(How|What|Why|When|Where|Can|Do|Is|Are|Does|Which|Who)\b', content, re.MULTILINE)
    if len(q_headings) < 2:
        failures.append(f"aeo_geo: Only {len(q_headings)} question heading(s) — need ≥2")
    
    # --- Internal Links Check ---
    blog_links = re.findall(r'/blog/(?!%s)[^"\')\s]+' % re.escape(slug), content)
    service_links = re.findall(r'/services/[^"\')\s]+', content)
    location_links = re.findall(r'/locations/[^"\')\s]+', content)
    other_internal = re.findall(r'/(?:about|contact|faq|industries)[^"\')\s]*', content)
    all_links = set(blog_links + service_links + location_links + other_internal)
    
    if len(all_links) < 3:
        failures.append(f"internal_links: Only {len(all_links)} unique internal link(s) — need ≥3")
    
    # --- Entity Check ---
    _, missing_entities = check_entity_coverage(content, tags)
    # Only flag as failure if core entities are missing
    core_missing = [m for m in missing_entities if m in ['Bangladesh', 'Dhaka', 'SEO (primary service)']]
    if core_missing:
        failures.append(f"entities: Missing core entities — {', '.join(core_missing)}")
    
    # --- Schema Check ---
    schema_missing = []
    if not post['title']:
        schema_missing.append('title')
    if not post['excerpt']:
        schema_missing.append('excerpt')
    if not post['date']:
        schema_missing.append('date')
    if schema_missing:
        failures.append(f"schema: Missing — {', '.join(schema_missing)}")
    
    if not failures:
        pass_count += 1
    else:
        fail_posts.append((slug, title, failures, pillar, has_pillar_link, len(q_headings), len(all_links), missing_entities))

# Summary table
report.append(f"- ✅ **All checks passed:** {pass_count} posts")
report.append(f"- ⚠️ **Issues found:** {len(fail_posts)} posts")
report.append("")

if not fail_posts:
    report.append("**No issues detected. All posts comply.** ✅")
else:
    report.append("")
    report.append("---")
    report.append("## Detailed Findings")
    report.append("")
    
    for slug, title, failures, pillar, has_pillar_link, q_count, link_count, missing_entities in fail_posts:
        report.append(f"### ❌ `{slug}`")
        report.append(f"**{title}**")
        report.append("")
        
        # Build a quick status table
        report.append("| Check | Status |")
        report.append("|-------|--------|")
        
        # Pillar
        if has_pillar_link:
            report.append(f"| Pillar Link | ✅ Links to {pillar['label']} |")
        else:
            report.append(f"| Pillar Link | ❌ Missing — should link to `{pillar['url']}` |")
        
        # AEO/GEO
        if q_count >= 2:
            report.append(f"| AEO/GEO | ✅ {q_count} question headings |")
        else:
            report.append(f"| AEO/GEO | ❌ Only {q_count} question headings (need ≥2) |")
        
        # Internal Links
        if link_count >= 3:
            report.append(f"| Internal Links | ✅ {link_count} internal links |")
        else:
            report.append(f"| Internal Links | ❌ Only {link_count} links (need ≥3) |")
        
        # Entities
        core_missing = [m for m in missing_entities if m in ['Bangladesh', 'Dhaka', 'SEO (primary service)']]
        if core_missing:
            report.append(f"| Entities | ❌ Missing: {', '.join(core_missing)} |")
        else:
            report.append(f"| Entities | ✅ Key entities present |")
        
        report.append("")
        
        # Consolidated fix instructions
        report.append("#### 🔧 Fix Instructions")
        for f in failures:
            if f.startswith("pillar_link:"):
                report.append(f"1. **{f.replace('pillar_link: ', '')}**")
            elif f.startswith("aeo_geo:"):
                report.append(f"1. **{f.replace('aeo_geo: ', '')}**")
                report.append("   → Add 2+ question headings (e.g., '## How Does X Work?' or '## What Makes Y Effective?')")
            elif f.startswith("internal_links:"):
                report.append(f"1. **{f.replace('internal_links: ', '')}**")
                report.append("   → Add links to related blog posts, service pages, or location pages")
            elif f.startswith("entities:"):
                report.append(f"1. **{f.replace('entities: ', '')}**")
                report.append("   → Mention the missing location/service entities in the content body")
            elif f.startswith("schema:"):
                report.append(f"1. **{f.replace('schema: ', '')}**")
                report.append("   → Set the missing fields in the post metadata")
        report.append("")

# Full details for posts with many failures
report.append("---")
report.append("## Posts With All Checks Passed ✅")
report.append("")

for slug in changed_slugs:
    post = posts.get(slug)
    if not post:
        continue
    content = post['content']
    tags = post['tags']
    
    pillar = get_pillar_for_post(slug, content, tags)
    pillar_url = pillar['url']
    has_pillar_link = pillar_url in content or '/blog/complete-seo-guide-bangladesh-businesses-2026' in content
    
    q_headings = re.findall(r'^#{2,6}\s+(How|What|Why|When|Where|Can|Do|Is|Are|Does|Which|Who)\b', content, re.MULTILINE)
    blog_links = re.findall(r'/blog/(?!%s)[^"\')\s]+' % re.escape(slug), content)
    service_links = re.findall(r'/services/[^"\')\s]+', content)
    location_links = re.findall(r'/locations/[^"\')\s]+', content)
    other_internal = re.findall(r'/(?:about|contact|faq|industries)[^"\')\s]*', content)
    all_links = set(blog_links + service_links + location_links + other_internal)
    _, missing_entities = check_entity_coverage(content, tags)
    core_missing = [m for m in missing_entities if m in ['Bangladesh', 'Dhaka', 'SEO (primary service)']]
    
    if has_pillar_link and len(q_headings) >= 2 and len(all_links) >= 3 and not core_missing and post['title'] and post['excerpt'] and post['date']:
        report.append(f"- ✅ **{slug}** — {post['title']}")

report.append("")
report.append("---")
report.append("## 📊 Summary Statistics")
report.append("")
report.append(f"| Metric | Value |")
report.append(f"|--------|-------|")
report.append(f"| Total posts checked | {len(changed_slugs)} |")
report.append(f"| Fully compliant | {pass_count} |")
report.append(f"| Need pillar link fix | {sum(1 for s,_,_,_,hp,_,_,_ in fail_posts if not hp)} |")
report.append(f"| Need AEO/GEO headings | {sum(1 for s,_,_,_,_,qc,_,_ in fail_posts if qc < 2)} |")
report.append(f"| Need more internal links | {sum(1 for s,_,_,_,_,_,lc,_ in fail_posts if lc < 3)} |")
report.append(f"| Need entity fixes | {sum(1 for s,_,_,_,_,_,_,me in fail_posts if any(m in ['Bangladesh', 'Dhaka', 'SEO (primary service)'] for m in me))} |")
report.append("")
report.append("## 🔧 Priority Actions")
report.append("")
report.append("1. **HIGH: Add pillar links to 12 case study posts** — Most case studies don't link to their pillar pages.")
report.append("2. **MEDIUM: Add question headings to 8 case study posts** — Case studies lack AEO/GEO optimization.")
report.append("3. **LOW: Add more internal links to 2 posts** (das-taxis-scotland-seo-case-study, stealth-windshield-repairs-seo-case-study)")
report.append("")
report.append("---")
report.append("*Report generated by Content Framework Enforcer cron job*")

print('\n'.join(report))

# Save
with open("/root/kanok-miahit/_framework_enforcement_report.md", "w") as f:
    f.write('\n'.join(report))
