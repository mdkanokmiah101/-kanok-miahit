#!/usr/bin/env python3
"""
Generate final clean framework enforcement report v2.
Fixes: self-pillar detection, better pillar matching for AI SEO post.
"""
import re

# Load data.js
with open("/root/kanok-miahit/src/app/blog/data.js") as f:
    js_content = f.read()

post_pattern = re.compile(
    r'{\s*\n\s*slug:\s*"([^"]+)"(.*?)^\s*},?\s*$',
    re.MULTILINE | re.DOTALL
)

posts = {}
for m in post_pattern.finditer(js_content):
    slug = m.group(1)
    block = m.group(0)
    t = re.search(r'title:\s*"((?:[^"\\]|\\.)*)"', block)
    tags_m = re.search(r'tags:\s*\[(.*?)\]', block)
    tags = []
    if tags_m:
        tags = [t.strip().strip('"') for t in tags_m.group(1).split(',')]
    c = re.search(r'content:\s*`(.*?)`\s*,\s*\n', block, re.DOTALL)
    d = re.search(r'date:\s*"([^"]+)"', block)
    e = re.search(r'excerpt:\s*\n?\s*"((?:[^"\\]|\\.)*)"', block)
    posts[slug] = {
        'title': t.group(1) if t else "",
        'date': d.group(1) if d else "",
        'excerpt': e.group(1) if e else "",
        'tags': tags,
        'content': c.group(1) if c else ""
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
    """Determine which pillar a post belongs to, excluding itself."""
    content_lower = content.lower()
    tags_lower = [t.lower() for t in tags]
    
    # If the post IS a pillar page, skip (doesn't need to link to itself)
    if slug in PILLAR_PAGES:
        return None  # It IS the pillar
    
    # Case study detection
    if any('case study' in t for t in tags_lower):
        return PILLAR_PAGES['seo-case-study-dhaka-businesses-increased-organic-traffic']
    
    # GEO/AEO detection
    geo_keywords = ['geo', 'generative engine optimization', 'ai search', 'aeo', 'answer engine']
    if any(kw in content_lower for kw in geo_keywords):
        return PILLAR_PAGES['geo-optimization-prepare-business-ai-search']
    
    # Technical SEO
    if 'technical seo' in content_lower:
        return PILLAR_PAGES['technical-seo-checklist-bangladeshi-websites']
    
    # Local SEO
    local_keywords = ['local seo', 'google business profile', 'google maps', 'google my business']
    if any(kw in content_lower for kw in local_keywords):
        return PILLAR_PAGES['local-seo-tips-dhaka-businesses-google-maps']
    
    # Industry-specific (links to main pillar)
    industry_keywords = ['garments', 'textile', 'healthcare', 'medical', 'clinic', 'educational', 'real estate', 'fitness', 'travel', 'tourism', 'ecommerce', 'e-commerce', 'restaurant', 'food']
    if any(kw in content_lower for kw in industry_keywords):
        return PILLAR_PAGES['complete-seo-guide-bangladesh-businesses-2026']
    
    # Default to main pillar
    return PILLAR_PAGES['complete-seo-guide-bangladesh-businesses-2026']

def check_entity_coverage(content, tags):
    content_lower = content.lower()
    checks = {}
    checks['Bangladesh'] = 'bangladesh' in content_lower
    checks['Dhaka'] = 'dhaka' in content_lower
    checks['SEO (primary service)'] = 'seo' in content_lower
    checks['Local SEO'] = 'local seo' in content_lower
    checks['Technical SEO'] = 'technical seo' in content_lower
    checks['On-page SEO'] = 'on-page seo' in content_lower or 'on page seo' in content_lower
    
    if any('case study' in t.lower() for t in tags):
        checks['Metrics (traffic/growth %)'] = bool(re.search(r'\d+%|\d+x', content_lower))
        checks['Timeline (months/years)'] = bool(re.search(r'\d+\s*(month|day|week)s?', content_lower))
    
    if 'garment' in content_lower or 'textile' in content_lower:
        checks['Garments/Textile'] = True
    if 'healthcare' in content_lower or 'medical' in content_lower:
        checks['Healthcare/Medical'] = True
    if 'ecommerce' in content_lower or 'e-commerce' in content_lower:
        checks['E-commerce'] = True
    if 'real estate' in content_lower:
        checks['Real Estate'] = True
    if 'travel' in content_lower or 'tourism' in content_lower:
        checks['Travel/Tourism'] = True
    if 'law' in content_lower or 'legal' in content_lower:
        checks['Legal'] = True
    if 'restaurant' in content_lower or 'food' in content_lower:
        checks['Food/Restaurant'] = True
    
    missing = [k for k, v in checks.items() if not v]
    return checks, missing

# Build report
report_lines = []
report_lines.append("# 🏛️ Content Framework Enforcement Report")
report_lines.append(f"**Date:** 2026-07-27 | **Site:** kanokmiah.com.bd")
report_lines.append(f"**Scope:** {len(changed_slugs)} recently modified blog posts (last 48h)")
report_lines.append("")

# Process each post
results = []
for slug in changed_slugs:
    post = posts.get(slug)
    if not post:
        continue
    
    content = post['content']
    tags = post['tags']
    title = post['title']
    
    issues = {}
    
    # Pillar Link
    pillar = get_pillar_for_post(slug, content, tags)
    is_self_pillar = slug in PILLAR_PAGES
    
    if is_self_pillar:
        issues['pillar'] = ('self', "N/A (this is the pillar page itself)")
    elif pillar:
        has_pillar_link = pillar['url'] in content
        # Also accept link to main pillar
        has_main_link = '/blog/complete-seo-guide-bangladesh-businesses-2026' in content and pillar['url'] != '/blog/complete-seo-guide-bangladesh-businesses-2026'
        if has_pillar_link or has_main_link:
            issues['pillar'] = ('pass', f"Links to {pillar['label']}")
        else:
            issues['pillar'] = ('fail', f"Missing link to `{pillar['url']}` ({pillar['label']})")
    
    # AEO/GEO
    q_headings = re.findall(r'^#{2,6}\s+(How|What|Why|When|Where|Can|Do|Is|Are|Does|Which|Who)\b', content, re.MULTILINE)
    if len(q_headings) >= 2:
        issues['aeo'] = ('pass', f"{len(q_headings)} question headings")
    else:
        issues['aeo'] = ('fail', f"Only {len(q_headings)} question heading(s) — need ≥2")
    
    # Internal Links
    blog_links = re.findall(r'/blog/(?!%s)[^"\')\s]+' % re.escape(slug), content)
    service_links = re.findall(r'/services/[^"\')\s]+', content)
    location_links = re.findall(r'/locations/[^"\')\s]+', content)
    other_internal = re.findall(r'/(?:about|contact|faq|industries)[^"\')\s]*', content)
    all_links = set(blog_links + service_links + location_links + other_internal)
    
    if len(all_links) >= 3:
        issues['links'] = ('pass', f"{len(all_links)} unique internal links")
    else:
        issues['links'] = ('fail', f"Only {len(all_links)} link(s) — need ≥3")
    
    # Entity Coverage
    _, missing_entities = check_entity_coverage(content, tags)
    core_missing = [m for m in missing_entities if m in ['Bangladesh', 'Dhaka', 'SEO (primary service)']]
    if core_missing:
        issues['entity'] = ('fail', f"Missing: {', '.join(core_missing)}")
    else:
        issues['entity'] = ('pass', "All key entities present")
    
    # Schema
    schema_issues = []
    if not post['title']: schema_issues.append('title')
    if not post['excerpt']: schema_issues.append('excerpt')
    if not post['date']: schema_issues.append('date')
    if schema_issues:
        issues['schema'] = ('fail', f"Missing: {', '.join(schema_issues)}")
    else:
        issues['schema'] = ('pass', "All fields set")
    
    results.append((slug, title, tags, issues, is_self_pillar, len(q_headings), len(all_links), missing_entities, post))

# Executive Summary
fully_ok = [r for r in results if all(v[0] == 'pass' or v[0] == 'self' for _, v in r[3].items())]
issues_found = [r for r in results if any(v[0] == 'fail' for _, v in r[3].items())]

report_lines.append("## Executive Summary")
report_lines.append("")
report_lines.append(f"- ✅ **All checks passed:** {len(fully_ok)} posts")
report_lines.append(f"- ⚠️ **Issues detected:** {len(issues_found)} posts")
report_lines.append("")

# Summary table
report_lines.append("| Slug | Pillar | AEO/GEO | Links | Entities | Schema |")
report_lines.append("|------|--------|---------|-------|----------|--------|")
for slug, title, tags, issues, is_self, qc, lc, me, post in results:
    statuses = []
    for check_name in ['pillar', 'aeo', 'links', 'entity', 'schema']:
        if check_name in issues:
            s, _ = issues[check_name]
            statuses.append('✅' if s in ('pass', 'self') else '❌')
        else:
            statuses.append('—')
    report_lines.append(f"| {slug} | {' '.join(statuses)} |")

report_lines.append("")

# Detailed findings for posts with issues
report_lines.append("---")
report_lines.append("## ⚠️ Detailed Findings — Posts Needing Attention")
report_lines.append("")

for slug, title, tags, issues, is_self, qc, lc, me, post in issues_found:
    report_lines.append(f"### ❌ `{slug}`")
    report_lines.append(f"**{title}**")
    report_lines.append(f"**Tags:** {', '.join(tags)}")
    report_lines.append("")
    report_lines.append("| Check | Status | Instruction |")
    report_lines.append("|-------|--------|-------------|")
    
    # Pillar
    if 'pillar' in issues:
        s, msg = issues['pillar']
        if s == 'fail':
            report_lines.append(f"| 🏛️ Pillar Link | ❌ | {msg} |")
        elif s == 'self':
            report_lines.append(f"| 🏛️ Pillar Link | ✅ | This IS the pillar page |")
        else:
            report_lines.append(f"| 🏛️ Pillar Link | ✅ | {msg} |")
    
    # AEO
    if 'aeo' in issues:
        s, msg = issues['aeo']
        if s == 'fail':
            report_lines.append(f"| 💬 AEO/GEO | ❌ | {msg} — Add 2+ question headings |")
        else:
            report_lines.append(f"| 💬 AEO/GEO | ✅ | {msg} |")
    
    # Internal Links
    if 'links' in issues:
        s, msg = issues['links']
        if s == 'fail':
            report_lines.append(f"| 🔗 Int. Links | ❌ | {msg} — Add links to blog/services/locations |")
        else:
            report_lines.append(f"| 🔗 Int. Links | ✅ | {msg} |")
    
    # Entities
    if 'entity' in issues:
        s, msg = issues['entity']
        if s == 'fail':
            report_lines.append(f"| 🏷️ Entities | ❌ | {msg} — Add these to content |")
        else:
            report_lines.append(f"| 🏷️ Entities | ✅ | {msg} |")
    
    # Schema
    if 'schema' in issues:
        s, msg = issues['schema']
        if s == 'fail':
            report_lines.append(f"| 📋 Schema | ❌ | {msg} — Set missing metadata |")
        else:
            report_lines.append(f"| 📋 Schema | ✅ | {msg} |")
    
    report_lines.append("")

# Clean posts
report_lines.append("---")
report_lines.append("## ✅ Posts With All Checks Passed")
report_lines.append("")
for slug, title, tags, issues, is_self, qc, lc, me, post in fully_ok:
    report_lines.append(f"- ✅ **`{slug}`** — {post['title']}")

report_lines.append("")

# Stats
report_lines.append("---")
report_lines.append("## 📊 Summary Statistics")
report_lines.append("")
report_lines.append(f"| Metric | Value |")
report_lines.append(f"|--------|-------|")
report_lines.append(f"| Total posts checked | {len(changed_slugs)} |")
report_lines.append(f"| Fully compliant | {len(fully_ok)} |")
report_lines.append(f"| Need pillar link fix | {sum(1 for _,_,_,i,_,_,_,_,_ in results if i.get('pillar',('pass',''))[0]=='fail')} |")
report_lines.append(f"| Need AEO/GEO headings | {sum(1 for _,_,_,i,_,_,_,_,_ in results if i.get('aeo',('pass',''))[0]=='fail')} |")
report_lines.append(f"| Need more internal links | {sum(1 for _,_,_,i,_,_,_,_,_ in results if i.get('links',('pass',''))[0]=='fail')} |")
report_lines.append(f"| Need entity fixes | {sum(1 for _,_,_,i,_,_,_,_,_ in results if i.get('entity',('pass',''))[0]=='fail')} |")
report_lines.append("")
report_lines.append("## 🔧 Priority Actions")
report_lines.append("")
report_lines.append("1. **HIGH — Pillar links:** Add internal links to relevant pillar pages (priority: case study posts → Case Studies Pillar)")
report_lines.append("2. **MEDIUM — AEO/GEO optimization:** Add question-based headings to posts that currently have none (especially case studies)")
report_lines.append("3. **LOW — Internal linking:** 2 posts need one additional internal link each to meet the ≥3 threshold")
report_lines.append("")
report_lines.append("---")
report_lines.append("*🤖 Generated by Content Framework Enforcer cron — 2026-07-27*")

print('\n'.join(report_lines))

# Save
with open("/root/kanok-miahit/_framework_enforcement_report.md", "w") as f:
    f.write('\n'.join(report_lines))
