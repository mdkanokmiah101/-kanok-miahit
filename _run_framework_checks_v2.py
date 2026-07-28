#!/usr/bin/env python3
"""
Content Framework Enforcer v2 - Fixed keyword extraction and pillar link detection.
"""
import re
import json

# Load data.js
with open("/root/kanok-miahit/src/app/blog/data.js") as f:
    content = f.read()

# Parse posts using a simpler approach - find slug and surrounding block
post_pattern = re.compile(
    r'{\s*\n\s*slug:\s*"([^"]+)"(.*?)^\s*},?\s*$',
    re.MULTILINE | re.DOTALL
)

posts = {}
for m in post_pattern.finditer(content):
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

def extract_primary_keyword(title, tags):
    """Extract primary keyword from title with improved logic."""
    title_lower = title.lower().strip()
    
    # For case studies, use the company name or "seo case study"
    if 'case study' in title_lower and ':' in title_lower:
        # Get the part before ":"
        prefix = title_lower.split(':')[0].strip()
        # Remove common prefixes
        for pfx in ['seo case study', 'case study']:
            prefix = prefix.replace(pfx, '').strip()
        # Take first 2-3 meaningful words
        words = [w for w in prefix.split() if len(w) > 2 and w not in {'the', 'for', 'and', 'seo'}]
        if words:
            return ' '.join(words[:3])
        return 'seo case study'
    
    # Remove trailing parenthetical content like "(And How to Fix Them)"
    title_clean = re.sub(r'\s*\([^)]*\)\s*$', '', title_lower)
    
    # Remove common prefixes
    for prefix_pattern in [
        r'^complete\s+', r'^ultimate\s+', r'^essential\s+', 
        r'^top\s+\d+\s+', r'^best\s+',
        r'^how\s+to\s+', r'^why\s+', r'^what\s+does\s+a\s+', r'^what\s+is\s+',
        r'^what\s+does\s+an?\s+',
        r'^seo\s+(?:for|in|of|and)\s+',
    ]:
        title_clean = re.sub(prefix_pattern, '', title_clean)
    
    # Remove trailing descriptors
    title_clean = re.sub(r':\s*.*$', '', title_clean)  # Remove after colon
    title_clean = re.sub(r'\s*(?:guide|checklist|tips|strateg(y|ies)|\d{4})\s*$', '', title_clean)
    
    # Also try tags as fallback
    if not title_clean or len(title_clean) < 5:
        for tag in tags:
            tag_lower = tag.lower()
            if 'seo' in tag_lower and len(tag_lower) > 5:
                return tag_lower
    
    # Take 2-4 meaningful words
    words = title_clean.split()
    meaningful = [w for w in words if len(w) > 2 or w in {'seo', 'geo', 'aeo'}]
    
    if not meaningful:
        meaningful = words
    
    return ' '.join(meaningful[:4])

def check_tfidf(title, content, tags):
    """A. TF-IDF Coverage."""
    keyword = extract_primary_keyword(title, tags)
    if not keyword:
        return "unknown", 0, False
    
    count = len(re.findall(re.escape(keyword), content, re.IGNORECASE))
    
    # If keyword match is too narrow (0-1), also try individual words
    if count <= 1:
        words = keyword.split()
        if len(words) > 1:
            # Try with just the main words
            for i in range(len(words), 0, -1):
                sub_kw = ' '.join(words[:i])
                if len(sub_kw) > 4:
                    count = len(re.findall(re.escape(sub_kw), content, re.IGNORECASE))
                    if count >= 3:
                        keyword = sub_kw
                        break
    
    passed = count >= 5
    return keyword, count, passed

def check_entities(title, content, tags):
    """B. Semantic Entity Coverage."""
    content_lower = content.lower()
    
    entity_checks = {}
    entity_checks['Bangladesh'] = 'bangladesh' in content_lower
    entity_checks['Dhaka'] = 'dhaka' in content_lower
    entity_checks['SEO'] = 'seo' in content_lower
    entity_checks['Local SEO'] = 'local seo' in content_lower
    entity_checks['Technical SEO'] = 'technical seo' in content_lower
    entity_checks['On-page SEO'] = 'on-page seo' in content_lower or 'on page seo' in content_lower
    
    # Detect service types from content
    if 'local seo' in tags or 'local seo' in content_lower:
        entity_checks['Google Business Profile'] = 'google business profile' in content_lower or 'google my business' in content_lower or 'gbp' in content_lower
    
    if 'geo' in content_lower.lower():
        entity_checks['GEO'] = 'geo' in content_lower.lower() and 'generative engine' in content_lower
    
    if 'healthcare' in content_lower or 'medical' in content_lower:
        entity_checks['Healthcare/Medical'] = True  # we already checked
    
    if 'garment' in content_lower or 'textile' in content_lower:
        entity_checks['Garments/Textile'] = True
    
    if 'ecommerce' in content_lower or 'e-commerce' in content_lower or 'retail' in content_lower:
        entity_checks['E-commerce'] = True
    
    if 'real estate' in content_lower:
        entity_checks['Real Estate'] = True
    
    if 'case study' in content_lower:
        # Check for key case study elements
        entity_checks['Traffic results'] = bool(re.search(r'\d+%|\d+x|increase|growth|traffic|visitors?', content_lower))
        entity_checks['Timeline'] = bool(re.search(r'\d+\s*(month|day|week)s?|january|february|march|april|may|june|july|august|september|october|november|december|202[4-6]', content_lower))
    
    missing = [k for k, v in entity_checks.items() if not v]
    passed = len(missing) <= 3
    return entity_checks, missing, passed

def check_pillar_link(title, content, tags, slug):
    """C. Pillar-Cluster Alignment."""
    content_lower = content.lower()
    tags_lower = [t.lower() for t in tags]
    
    # Known pillar pages on this site
    pillar_pages = {
        'complete-seo-guide-bangladesh-businesses-2026': {
            'keywords': ['seo guide', 'complete seo guide', 'seo for bangladesh'],
            'url': '/blog/complete-seo-guide-bangladesh-businesses-2026',
            'label': 'Complete SEO Guide (Main Pillar)'
        },
        'local-seo-tips-dhaka-businesses-google-maps': {
            'keywords': ['local seo', 'google maps seo', 'google business profile'],
            'url': '/blog/local-seo-tips-dhaka-businesses-google-maps',
            'label': 'Local SEO Guide'
        },
        'technical-seo-checklist-bangladeshi-websites': {
            'keywords': ['technical seo', 'seo checklist', 'website optimization'],
            'url': '/blog/technical-seo-checklist-bangladeshi-websites',
            'label': 'Technical SEO Guide'
        },
        'geo-optimization-prepare-business-ai-search': {
            'keywords': ['geo', 'generative engine', 'ai search', 'aeo'],
            'url': '/blog/geo-optimization-prepare-business-ai-search',
            'label': 'GEO/AEO Guide'
        },
        'seo-case-study-dhaka-businesses-increased-organic-traffic': {
            'keywords': ['case study', 'seo case study', 'seo results'],
            'url': '/blog/seo-case-study-dhaka-businesses-increased-organic-traffic',
            'label': 'Case Studies Pillar'
        }
    }
    
    # Determine which pillar this post belongs to
    matched_pillar = None
    for pillar_slug, pillar in pillar_pages.items():
        if pillar_slug == slug:
            continue  # Don't match self
        # Check tags
        for tag in tags_lower:
            for kw in pillar['keywords']:
                if kw in tag:
                    matched_pillar = pillar
                    break
        # Check content
        if not matched_pillar:
            for kw in pillar['keywords']:
                if kw in content_lower and len(kw) > 5:
                    matched_pillar = pillar
                    break
    
    # For case study posts, default to case_studies pillar
    if not matched_pillar and any('case study' in t.lower() for t in tags):
        matched_pillar = pillar_pages['seo-case-study-dhaka-businesses-increased-organic-traffic']
    
    # If still no match, check content-based classification
    if not matched_pillar:
        if 'local seo' in content_lower or 'google business profile' in content_lower:
            matched_pillar = pillar_pages['local-seo-tips-dhaka-businesses-google-maps']
        elif 'technical seo' in content_lower:
            matched_pillar = pillar_pages['technical-seo-checklist-bangladeshi-websites']
        elif 'geo' in content_lower.lower() or 'ai search' in content_lower:
            matched_pillar = pillar_pages['geo-optimization-prepare-business-ai-search']
        else:
            matched_pillar = pillar_pages['complete-seo-guide-bangladesh-businesses-2026']
    
    # Check if post links to any pillar page
    links = set()
    for ps, pp in pillar_pages.items():
        if pp['url'] in content:
            links.add(pp['url'])
    
    linked_to_pillar = matched_pillar['url'] in content if matched_pillar else False
    any_pillar_link = len(links) > 0
    
    passed = linked_to_pillar or any_pillar_link
    
    return matched_pillar['label'] if matched_pillar else "Unknown", list(links), passed

def check_aeo_geo(content):
    """D. AEO/GEO Optimization - count question-based headings."""
    question_headings = re.findall(
        r'^#{2,6}\s+(How|What|Why|When|Where|Can|Do|Is|Are|Does|Which|Who)\b',
        content,
        re.MULTILINE
    )
    count = len(question_headings)
    passed = count >= 2
    return count, passed

def check_internal_links(content, slug):
    """E. Internal Linking."""
    blog_links = re.findall(r'/blog/(?!%s)[^"\')\s]+' % re.escape(slug), content)
    service_links = re.findall(r'/services/[^"\')\s]+', content)
    location_links = re.findall(r'/locations/[^"\')\s]+', content)
    other_internal = re.findall(r'/(?:about|contact|faq|industries)[^"\')\s]*', content)
    
    all_links = set(blog_links + service_links + location_links + other_internal)
    total = len(all_links)
    passed = total >= 3
    return total, passed, sorted(all_links)

def check_schema(title, excerpt, date):
    """F. Schema Readiness."""
    issues = []
    if not title:
        issues.append("title missing")
    if not excerpt:
        issues.append("excerpt missing")
    if not date:
        issues.append("date missing")
    passed = len(issues) == 0
    return issues, passed

# Generate report
report_lines = []
report_lines.append("# Content Framework Enforcement Report")
report_lines.append(f"**Date:** 2026-07-27")
report_lines.append(f"**Scope:** {len(changed_slugs)} modified posts (last 48 hours)")
report_lines.append("")
report_lines.append("| Post | TF-IDF | Entities | Pillar | AEO/GEO | Int.Links | Schema |")
report_lines.append("|------|--------|----------|--------|---------|-----------|--------|")

summary_rows = []
all_passed = True
detailed_parts = []

for slug in changed_slugs:
    if slug not in posts:
        detailed_parts.append(f"\n## Post: {slug}\n❌ **Post not found in data.js!**\n")
        continue
    
    post = posts[slug]
    title = post['title']
    content = post['content']
    tags = post['tags']
    excerpt = post['excerpt']
    date = post['date']
    
    # A
    keyword, tfidf_count, tfidf_pass = check_tfidf(title, content, tags)
    
    # B
    entity_checks, missing, entity_pass = check_entities(title, content, tags)
    
    # C
    pillar_label, pillar_links, pillar_pass = check_pillar_link(title, content, tags, slug)
    
    # D
    aeo_count, aeo_pass = check_aeo_geo(content)
    
    # E
    link_count, link_pass, links = check_internal_links(content, slug)
    
    # F
    schema_issues, schema_pass = check_schema(title, excerpt, date)
    
    if not all([tfidf_pass, entity_pass, pillar_pass, aeo_pass, link_pass, schema_pass]):
        all_passed = False
    
    status_a = "✅" if tfidf_pass else "❌"
    status_b = "✅" if entity_pass else "❌"
    status_c = "✅" if pillar_pass else "❌"
    status_d = "✅" if aeo_pass else "❌"
    status_e = "✅" if link_pass else "❌"
    status_f = "✅" if schema_pass else "❌"
    
    # Summary row
    summary_rows.append(f"| {slug} | {status_a} | {status_b} | {status_c} | {status_d} | {status_e} | {status_f} |")
    
    # Detailed section
    detailed_parts.append(f"\n## Post: `{slug}`")
    detailed_parts.append(f"**Title:** {title}")
    detailed_parts.append(f"**Date:** {date}  **Tags:** {', '.join(tags)}")
    detailed_parts.append("")
    
    # A
    detailed_parts.append("### A. TF-IDF Coverage")
    detailed_parts.append(f"- **Keyword:** `{keyword}`")
    detailed_parts.append(f"- **Occurrences:** {tfidf_count}")
    detailed_parts.append(f"- **Result:** {status_a} {'PASS' if tfidf_pass else f'FAIL — only {tfidf_count} occurrences (need ≥5)'}")
    if not tfidf_pass:
        detailed_parts.append(f"  - **Fix:** Use primary keyword `{keyword}` more often in content body (≥5 times)")
    detailed_parts.append("")
    
    # B
    detailed_parts.append("### B. Semantic Entity Coverage")
    detailed_parts.append(f"- **Total checks:** {len(entity_checks)}")
    detailed_parts.append(f"- **Passed:** {len(entity_checks) - len(missing)}/{len(entity_checks)}")
    if missing:
        detailed_parts.append(f"- **Missing:** {', '.join(missing)}")
        if not entity_pass:
            detailed_parts.append(f"- **Result:** {status_b} FAIL — too many missing entities")
            detailed_parts.append(f"  - **Fix:** Add these missing entities to the content")
        else:
            detailed_parts.append(f"- **Result:** {status_b} OK — minor/expected misses")
    else:
        detailed_parts.append(f"- **Result:** {status_b} PASS — all entities present")
    detailed_parts.append("")
    
    # C
    detailed_parts.append("### C. Pillar-Cluster Alignment")
    detailed_parts.append(f"- **Pillar:** {pillar_label}")
    if pillar_links:
        detailed_parts.append(f"- **Links to pillar(s):** {', '.join(pillar_links)}")
    else:
        detailed_parts.append(f"- **Links to pillar(s):** none")
    detailed_parts.append(f"- **Result:** {status_c} {'PASS' if pillar_pass else 'FAIL — add link to pillar page'}")
    if not pillar_pass:
        detailed_parts.append(f"  - **Fix:** Add internal link to the {pillar_label} pillar page")
    detailed_parts.append("")
    
    # D
    detailed_parts.append("### D. AEO/GEO Optimization")
    detailed_parts.append(f"- **Question headings:** {aeo_count}")
    detailed_parts.append(f"- **Result:** {status_d} {'PASS' if aeo_pass else 'FAIL — need ≥2 question headings (How, What, Why, etc.)'}")
    if not aeo_pass:
        detailed_parts.append(f"  - **Fix:** Add at least 2 question-based headings (starting with How, What, Why, When, Where, Can, Do, Is, Are)")
    detailed_parts.append("")
    
    # E
    detailed_parts.append("### E. Internal Linking")
    detailed_parts.append(f"- **Total unique internal links:** {link_count}")
    if links:
        for link in links[:12]:
            detailed_parts.append(f"  - {link}")
        if len(links) > 12:
            detailed_parts.append(f"  - ... and {len(links)-12} more")
    detailed_parts.append(f"- **Result:** {status_e} {'PASS' if link_pass else f'FAIL — only {link_count} internal links (need ≥3)'}")
    if not link_pass:
        detailed_parts.append(f"  - **Fix:** Add more internal links to other blog posts, services, or location pages")
    detailed_parts.append("")
    
    # F
    detailed_parts.append("### F. Schema Readiness")
    detailed_parts.append(f"- Title: {'✅' if title else '❌'}")
    detailed_parts.append(f"- Excerpt: {'✅' if excerpt else '❌'} ({len(excerpt) if excerpt else 0} chars)")
    detailed_parts.append(f"- Date: {'✅' if date else '❌'}")
    detailed_parts.append(f"- **Result:** {status_f} {'PASS' if schema_pass else 'FAIL — missing: ' + ', '.join(schema_issues)}")
    detailed_parts.append("")

# Summary table
report_lines.extend(summary_rows)
report_lines.append("")
report_lines.append("---")
report_lines.append("")

# Detailed sections
report_lines.extend(detailed_parts)

# Final summary
fail_count = sum(1 for row in summary_rows if '❌' in row)
report_lines.append("\n# Final Summary")
report_lines.append(f"- **Posts checked:** {len(changed_slugs)}")
report_lines.append(f"- **Posts with all checks passed:** {len(changed_slugs) - fail_count}")
report_lines.append(f"- **Posts needing attention:** {fail_count}")
report_lines.append("")

if all_passed:
    report_lines.append("**Overall: ✅ ALL CHECKS PASSED** — All modified posts comply with the content framework.")
else:
    report_lines.append("**Overall: ⚠️  SOME POSTS NEED FIXES** — See detailed report above for fix instructions.")

report = '\n'.join(report_lines)
print(report)

# Save to file
with open("/root/kanok-miahit/_framework_enforcement_report.md", "w") as f:
    f.write(report)
