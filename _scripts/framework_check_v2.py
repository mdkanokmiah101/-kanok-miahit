#!/usr/bin/env python3
"""Framework Enforcement Checker for kanokmiah.com.bd blog posts - v2."""
import re

# ---- Helpers ----

def extract_post(content, slug):
    """Find blog post by slug in data.js content."""
    idx = content.find(f'slug: "{slug}"')
    if idx == -1:
        return None
    start = content.rfind('{', 0, idx)
    depth = 0
    in_template = False
    for i in range(start, len(content)):
        ch = content[i]
        if ch == '`':
            in_template = not in_template
        elif not in_template:
            if ch == '{':
                depth += 1
            elif ch == '}':
                depth -= 1
                if depth == 0:
                    return content[start:i+1]
    return None


def get_field(post, field):
    """Extract a named field from the post object."""
    m = re.search(rf'{field}:\s*"([^"]*)"', post)
    if m:
        return m.group(1)
    m = re.search(rf'{field}:\s*\n\s+"([^"]*)"', post)
    if m:
        return m.group(1)
    return ''


def get_tags(post):
    """Extract tags array from post."""
    m = re.search(r'tags:\s*\[([^\]]*)\]', post)
    if not m:
        return []
    tags_str = m.group(1)
    return [t.strip().strip('"') for t in tags_str.split(',') if t.strip()]


def get_content_body(post):
    """Get the template literal content body."""
    m = re.search(r'content:\s*`\n?(.*?)`,\s*\n?\}', post, re.DOTALL)
    if m:
        return m.group(1).strip()
    return ''


def count_keyword(text, keyword_parts):
    """Count occurrences of a set of keyword parts in text (case-insensitive)."""
    total = 0
    for kw in keyword_parts:
        pattern = re.escape(kw)
        matches = re.findall(pattern, text, re.IGNORECASE)
        total += len(matches)
    return total


def count_question_headings(text):
    """Count question-based headings."""
    q_words = ['How', 'What', 'Why', 'When', 'Where', 'Can', 'Do', 'Is', 'Are', 'Does', 'Will', 'Should']
    count = 0
    for line in text.split('\n'):
        line = line.strip()
        if line.startswith('#'):
            for qw in q_words:
                heading_text = line.lstrip('#').strip()
                if heading_text.startswith(qw + ' ') or heading_text.startswith(qw + '?') or heading_text.startswith(qw + ':'):
                    count += 1
                    break
    return count


def count_internal_links(text):
    """Count internal links."""
    links = set()
    # Markdown links
    for m in re.finditer(r'\[([^\]]*)\]\((/[^)]*)\)', text):
        link = m.group(2)
        if any(link.startswith(p) for p in ['/blog/', '/services/', '/locations/', '/industries/', '/about', '/contact', '/']):
            if link != '/':
                links.add(link)
    # HTML links
    for m in re.finditer(r'href="(/[^"]*)"', text):
        link = m.group(1)
        if any(link.startswith(p) for p in ['/blog/', '/services/', '/locations/', '/industries/', '/about', '/contact', '/']):
            if link != '/':
                links.add(link)
    return list(links)


def extract_primary_keyword(title):
    """Extract primary keyword/theme from title."""
    t = title.strip().lower()
    
    # Map known title patterns to primary keyword sets
    known = {
        'seo for fitness and gym businesses in bangladesh': ['fitness', 'gym'],
        'seo for law firms and legal services in bangladesh': ['law firm', 'legal services'],
        'b2b lead generation through seo in bangladesh': ['b2b lead generation', 'b2b seo'],
        'seo for startups in bangladesh': ['startup seo', 'startups'],
        'howto স্কিমা': ['howto schema', 'স্কিমা'],
    }
    
    for pattern, kws in known.items():
        if pattern in t:
            return kws
    
    # Generic fallback
    # Remove "SEO", "in Bangladesh", "Complete Guide" etc
    for stop in [' seo ', ' in bangladesh', ' complete guide', ' the ultimate guide', ' a complete ']:
        t = t.replace(stop, ' ')
    parts = [p.strip() for p in t.split() if p.strip() and len(p.strip()) > 2]
    if parts:
        return [parts[0]]
    return ['keyword']


# ---- Main ----

with open('src/app/blog/data.js', 'r') as f:
    content = f.read()

slugs_to_check = [
    'seo-for-fitness-gyms-bangladesh',
    'seo-for-law-firms-bangladesh',
    'b2b-lead-generation-seo-bangladesh',
    'seo-for-startups-bangladesh',
    'seo-howto-schema-bangladesh',
]

all_passed = True

for slug in slugs_to_check:
    post = extract_post(content, slug)
    if not post:
        print(f"⚠ Could not extract: {slug}")
        continue
    
    title = get_field(post, 'title')
    excerpt = get_field(post, 'excerpt')
    date = get_field(post, 'date')
    tags = get_tags(post)
    body = get_content_body(post)
    full_text = title + '\n' + excerpt + '\n' + body
    
    print(f"\n## Post: {slug}")
    print(f"**Title:** {title}")
    print(f"**Date:** {date}  |  **Tags:** {', '.join(tags)}")
    print()
    print("| Check | Status | Details |")
    print("|-------|--------|---------|")
    
    post_passed = True
    
    # A. TF-IDF Coverage
    primary_kws = extract_primary_keyword(title)
    kw_count = count_keyword(full_text, primary_kws)
    tfidf_status = '✅' if kw_count >= 5 else '❌'
    if tfidf_status == '❌': post_passed = False; all_passed = False
    kw_display = ' / '.join(primary_kws)
    print(f"| TF-IDF: `{kw_display}` | {tfidf_status} | {kw_count} occurrences{' (too thin!)' if kw_count < 5 else ''} |")
    
    # B. Semantic Entity Coverage
    entity_checks = {
        'Bangladesh/Bangladeshi': ['Bangladesh', 'Bangladeshi'],
        'Dhaka location': ['Dhaka'],
        'Location page links': ['/locations/'],
    }
    missing_entities = []
    for entity_name, variants in entity_checks.items():
        found = any(v in full_text for v in variants)
        if not found:
            missing_entities.append(entity_name)
    
    entities_status = '✅' if not missing_entities else '❌'
    if entities_status == '❌': post_passed = False; all_passed = False
    if missing_entities:
        details = f"Missing: {', '.join(missing_entities)}"
    else:
        details = 'All key entities present'
    print(f"| Entities | {entities_status} | {details} |")
    
    # C. Pillar-Cluster Alignment
    internal_links_all = count_internal_links(body)
    
    # Check for links to the main pillar guide or complementary guides
    pillar_guide_links = [l for l in internal_links_all if any(
        l.startswith(p) for p in ['/blog/complete-seo-guide-', '/blog/seo-guide-']
    )]
    
    # Also check for service page links (these act as pillar pages)
    service_links = [l for l in internal_links_all if l.startswith('/services/')]
    
    has_pillar_link = len(pillar_guide_links) > 0
    
    if has_pillar_link:
        pillar_detail = f"Links to pillar: {', '.join(pillar_guide_links[:3])}"
        pillar_status = '✅'
    elif len(internal_links_all) >= 3:
        pillar_detail = f"No explicit pillar guide link, but {len(internal_links_all)} internal links ({len(service_links)} to services)"
        pillar_status = '⚠'
    else:
        pillar_detail = 'No pillar page or sufficient internal links'
        pillar_status = '❌'
        post_passed = False; all_passed = False
    
    print(f"| Pillar Link | {pillar_status} | {pillar_detail} |")
    
    # D. AEO/GEO Optimization
    q_count = count_question_headings(body)
    has_faq = bool(re.search(r'##\s*FAQ|##\s*(Frequently Asked|প্রায়শই)', body))
    
    if q_count >= 2:
        aeo_status = '✅'
        aeo_detail = f'{q_count} question headings'
    elif q_count >= 1 and has_faq:
        aeo_status = '✅'
        aeo_detail = f'{q_count} question heading(s) + FAQ section'
    else:
        aeo_status = '❌'
        aeo_detail = f'{q_count} question headings (need ≥2 or add FAQ)'
        post_passed = False; all_passed = False
    
    print(f"| AEO/GEO | {aeo_status} | {aeo_detail} |")
    
    # E. Internal Linking
    link_count = len(internal_links_all)
    link_status = '✅' if link_count >= 3 else '❌'
    if link_status == '❌': post_passed = False; all_passed = False
    link_examples = ', '.join(internal_links_all[:5])
    if len(internal_links_all) > 5:
        link_examples += '...'
    print(f"| Internal Links | {link_status} | {link_count} total: {link_examples} |")
    
    # F. Schema Ready
    schema_missing = []
    if not title: schema_missing.append('title')
    if not excerpt: schema_missing.append('excerpt')
    if not date: schema_missing.append('date')
    schema_status = '✅' if not schema_missing else '❌'
    if schema_status == '❌': post_passed = False; all_passed = False
    schema_detail = 'All fields set' if not schema_missing else f"Missing: {', '.join(schema_missing)}"
    print(f"| Schema Ready | {schema_status} | {schema_detail} |")
    
    # Fix instructions
    print()
    print("### Fix instructions:")
    fixes = []
    
    if kw_count < 5:
        fixes.append(f"- **TF-IDF thin**: Add more instances of `{' / '.join(primary_kws)}` (currently {kw_count}). Target ≥5.")
    
    if missing_entities:
        for e in missing_entities:
            fixes.append(f"- **Missing entity: {e}** — Add mention to content body.")
    
    if not has_pillar_link and link_count >= 3:
        fixes.append(f"- **Pillar link recommended**: Link to `/blog/complete-seo-guide-bangladesh-businesses-2026` or relevant pillar page for stronger topical cluster signals.")
    elif not has_pillar_link and link_count < 3:
        fixes.append(f"- **Pillar link required**: Add link to the main pillar page AND at least {3 - link_count} more internal links.")
    
    if q_count < 2 and not has_faq:
        fixes.append(f"- **AEO/GEO**: Add ≥2 question-based headings (How, What, Why). Current: {q_count}. Also consider adding an FAQ section.")
    elif q_count < 2 and has_faq:
        pass  # FAQ compensates
    elif q_count < 2:
        fixes.append(f"- **AEO**: Add ≥2 question headings. Current: {q_count}.")
    
    if link_count < 3:
        fixes.append(f"- **Internal linking thin**: {link_count} internal links found, need ≥3. Link to services, locations, or related posts.")
    
    if schema_missing:
        fixes.append(f"- **Schema fields missing**: {', '.join(schema_missing)} must be set for ArticleSchema.")
    
    if not fixes:
        fixes.append("- ✅ All checks passed. No fixes needed.")
    
    for f_line in fixes:
        print(f_line)
    
    print()

# Summary
print("=" * 60)
print("OVERALL SUMMARY")
print("=" * 60)
if all_passed:
    print("✅ All framework checks passed across all reviewed posts.")
else:
    print("❌ Some posts need attention. See individual reports above.")
