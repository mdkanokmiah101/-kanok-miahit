#!/usr/bin/env python3
"""Framework Enforcement Checker for kanokmiah.com.bd blog posts."""
import re
import json
import os

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
    """Extract a named field from the post object (simple regex-based)."""
    m = re.search(rf'{field}:\s*"([^"]*)"', post)
    if m:
        return m.group(1)
    # Handle multiline excerpt
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
        return m.group(1)
    return ''


def count_keyword(text, keyword):
    """Count occurrences of a keyword in text (case-insensitive)."""
    if not keyword:
        return 0
    pattern = re.escape(keyword)
    matches = re.findall(pattern, text, re.IGNORECASE)
    return len(matches)


def get_key_entities(content_body, title):
    """Identify entities that should be present."""
    entities = {
        'Bangladesh': ['Bangladesh', 'Bangladeshi'],
        'Dhaka': ['Dhaka'],
        'location link': ['/locations/'],
    }
    return entities


def count_question_headings(text):
    """Count question-based headings."""
    q_words = ['How', 'What', 'Why', 'When', 'Where', 'Can', 'Do', 'Is', 'Are', 'Does', 'Will', 'Should']
    count = 0
    for line in text.split('\n'):
        line = line.strip()
        if line.startswith('#'):
            for qw in q_words:
                # Check if heading starts with ## followed by question word
                heading_text = line.lstrip('#').strip()
                if heading_text.startswith(qw + ' ') or heading_text.startswith(qw + '?'):
                    count += 1
                    break
    return count


def count_internal_links(text):
    """Count internal links (to /blog/, /services/, /locations/, /about/, /contact/, /industries/)."""
    patterns = [r'href="/[^"]*"', r'\[([^\]]*)\]\((/[^)]*)\)']
    links = set()
    # Find markdown links with internal paths
    for m in re.finditer(r'\[([^\]]*)\]\((/[^)]*)\)', text):
        link = m.group(2)
        if any(link.startswith(p) for p in ['/blog/', '/services/', '/locations/', '/industries/', '/about', '/contact']):
            links.add(link)
    # Find HTML links
    for m in re.finditer(r'href="(/[^"]*)"', text):
        link = m.group(1)
        if any(link.startswith(p) for p in ['/blog/', '/services/', '/locations/', '/industries/', '/about', '/contact']):
            links.add(link)
    return list(links)


def extract_primary_keyword(title):
    """Extract primary keyword from title (first meaningful noun phrase)."""
    # Try to get the main topic from the title
    # Strip common prefixes
    title_lower = title.lower()
    prefixes = ['seo for ', 'complete ', 'the ultimate ', 'a complete ']
    for p in prefixes:
        if title_lower.startswith(p):
            remainder = title[len(p):]
            # Take the first noun phrase before ' in', ' for', ' at', ' -'
            m = re.match(r'([^(in|for|at|–|—)]+)', remainder)
            if m:
                kw = m.group(1).strip().strip(':').strip(',')
                if kw:
                    return kw
            return remainder.split(' in ')[0].split(' for ')[0].strip() if ' in ' in remainder else remainder.split('for ')[0].strip()
    
    # For titles starting with B2B etc.
    if title_lower.startswith('b2b'):
        return 'B2B lead generation'
    
    # Default: take the main part
    return title.split(':')[0].split('—')[0].strip()


# ---- Main Check Logic ----

with open('src/app/blog/data.js', 'r') as f:
    content = f.read()

slugs_to_check = [
    'seo-for-fitness-gyms-bangladesh',
    'seo-for-law-firms-bangladesh',
    'b2b-lead-generation-seo-bangladesh',
    'seo-for-startups-bangladesh',
    'seo-howto-schema-bangladesh',
]

all_checks_passed = True

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
    
    print(f"\n## Post: {slug}")
    print(f"**Title:** {title}")
    print()
    print(f"| Check | Status | Details |")
    print(f"|-------|--------|---------|")
    
    post_passed = True
    
    # A. TF-IDF Coverage
    primary_kw = extract_primary_keyword(title)
    kw_count = count_keyword(body + title, primary_kw)
    tfidf_status = '✅' if kw_count >= 5 else '❌'
    if tfidf_status == '❌': post_passed = False; all_checks_passed = False
    print(f"| TF-IDF: `{primary_kw}` | {tfidf_status} | {kw_count} occurrences{' (too thin!)' if kw_count < 5 else ''} |")
    
    # B. Semantic Entity Coverage
    text_to_check = body + title + excerpt
    entities_found = {}
    entity_checks = {
        'Bangladesh/Bangladeshi': ['Bangladesh', 'Bangladeshi'],
        'Dhaka location': ['Dhaka'],
        'Location page links': ['/locations/'],
    }
    missing_entities = []
    for entity_name, variants in entity_checks.items():
        found = any(v in text_to_check for v in variants)
        entities_found[entity_name] = found
        if not found:
            missing_entities.append(entity_name)
    entities_status = '✅' if not missing_entities else '❌'
    if entities_status == '❌': post_passed = False; all_checks_passed = False
    details = ''
    if missing_entities:
        missing_str = ', '.join(missing_entities)
        details = f"Missing: {missing_str}"
    else:
        details = 'All key entities present'
    print(f"| Entities | {entities_status} | {details} |")
    
    # Also check service-type specific entities
    industry_entities = {
        'seo-for-fitness-gyms-bangladesh': ['fitness', 'gym', 'gyms', 'personal trainer', 'workout'],
        'seo-for-law-firms-bangladesh': ['law', 'legal', 'attorney', 'lawyer', 'firm'],
        'b2b-lead-generation-seo-bangladesh': ['B2B', 'lead', 'manufacturer', 'supplier', 'procurement'],
        'seo-for-startups-bangladesh': ['startup', 'startups', 'funding', 'seed', 'early-stage'],
        'seo-howto-schema-bangladesh': ['HowTo', 'schema', 'structured data', 'markup', 'JSON-LD'],
    }
    if slug in industry_entities:
        missing_ind = []
        for ind_entity in industry_entities[slug]:
            if not any(v in text_to_check.lower() for v in [ind_entity]):
                if ind_entity not in [m.split(':')[0] for m in missing_entities]:
                    pass  # These are supplementary, not critical
        
    # C. Pillar-Cluster Alignment
    pillar_links = []
    for m in re.finditer(r'\[([^\]]*)\]\((/[^)]*)\)', body):
        link = m.group(2)
        if link.startswith('/blog/') and link != f'/blog/{slug}':
            pillar_links.append(link)
    
    # Look for pillar page links (main service pages)
    pillar_page_links = [l for l in pillar_links if any(l.startswith(p) for p in ['/blog/seo-guide-', '/blog/complete-seo-guide'])]
    has_pillar_link = len(pillar_page_links) > 0
    
    pillar_status = '✅' if has_pillar_link else '⚠'
    if not has_pillar_link:
        # Check if there's any clear pillar/cluster page link
        cluster_links = [l for l in pillar_links if l != f'/blog/{slug}']
        if cluster_links:
            pillar_status = '⚠'
            details = f"No explicit pillar link, but {len(cluster_links)} sibling post links found"
        else:
            pillar_status = '❌'
            post_passed = False; all_checks_passed = False
            details = 'No pillar or cluster links found'
    else:
        details = f"Links to: {', '.join(pillar_page_links[:3])}"
    
    if pillar_status == '⚠':
        if not cluster_links:
            pillar_status = '❌'
            post_passed = False; all_checks_passed = False
            details = 'No pillar page link found'
    
    if details is None:
        details = f"Links to: {', '.join(pillar_page_links[:3])}" if has_pillar_link else 'No pillar link found'
    print(f"| Pillar Link | {pillar_status} | {details} |")
    
    # D. AEO/GEO Optimization
    q_count = count_question_headings(body)
    aeo_status = '✅' if q_count >= 2 else '❌'
    if aeo_status == '❌': post_passed = False; all_checks_passed = False
    print(f"| AEO/GEO | {aeo_status} | {q_count} question headings{' (need ≥2!)' if q_count < 2 else ''} |")
    
    # Also check for FAQ section
    has_faq = 'FAQ' in body or 'faq' in body
    if not has_faq and q_count < 2:
        aeo_status = '❌'
    
    # E. Internal Linking
    internal_links = count_internal_links(body)
    # Also add links from the "content" area
    link_count = len(internal_links)
    link_status = '✅' if link_count >= 3 else '❌'
    if link_status == '❌': post_passed = False; all_checks_passed = False
    print(f"| Internal Links | {link_status} | {link_count} total (unique paths: {', '.join(internal_links[:5])}{'...' if len(internal_links) > 5 else ''}) |")
    
    # F. Schema Ready
    schema_missing = []
    if not title: schema_missing.append('title')
    if not excerpt: schema_missing.append('excerpt')
    if not date: schema_missing.append('date')
    schema_status = '✅' if not schema_missing else '❌'
    if schema_status == '❌': post_passed = False; all_checks_passed = False
    schema_detail = 'All fields set' if not schema_missing else f"Missing: {', '.join(schema_missing)}"
    print(f"| Schema Ready | {schema_status} | {schema_detail} |")
    
    # Fix instructions
    print()
    print("### Fix instructions:")
    fixes = []
    
    if kw_count < 5:
        fixes.append(f"- **TF-IDF**: Add more instances of the primary keyword `{primary_kw}` (currently {kw_count}). Target ≥5 occurrences in the body.")
    
    if missing_entities:
        for e in missing_entities:
            fixes.append(f"- **Entity: {e}** — Ensure this entity is mentioned in the content body.")
    
    if not has_pillar_link:
        fixes.append(f"- **Pillar Link**: Add a link to the main pillar/topic cluster page (e.g., `/blog/complete-seo-guide-bangladesh-businesses-2026` or a relevant guide).")
    
    if q_count < 2:
        fixes.append(f"- **AEO**: Add more question-based headings (How, What, Why, etc.). Current: {q_count}, need ≥2. Consider adding a FAQ section.")
    
    if link_count < 3:
        fixes.append(f"- **Internal Links**: Add more internal links to services, locations, or other blog posts. Currently {link_count}, need ≥3.")
    
    if schema_missing:
        fixes.append(f"- **Schema**: Set the missing fields: {', '.join(schema_missing)}.")
    
    if not fixes:
        fixes.append("- ✅ All checks passed. No fixes needed.")
    
    for f in fixes:
        print(f)
    
    print()

# Summary
print(f"\n{'='*60}")
print("OVERALL SUMMARY")
print(f"{'='*60}")
if all_checks_passed:
    print("✅ All framework checks passed across all reviewed posts.")
else:
    print("❌ Some posts need attention. See individual reports above.")
