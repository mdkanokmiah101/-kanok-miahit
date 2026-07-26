#!/usr/bin/env python3
"""Framework Enforcement Checker v3 - handles Bengali script entities."""
import re

def extract_post(content, slug):
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
    m = re.search(rf'{field}:\s*"([^"]*)"', post)
    if m:
        return m.group(1)
    m = re.search(rf'{field}:\s*\n\s+"([^"]*)"', post)
    if m:
        return m.group(1)
    return ''

def get_content_body(post):
    m = re.search(r'content:\s*`\n?(.*?)`,\s*\n?\}', post, re.DOTALL)
    if m:
        return m.group(1).strip()
    return ''

def count_keyword(text, keyword_parts):
    total = 0
    for kw in keyword_parts:
        total += len(re.findall(re.escape(kw), text, re.IGNORECASE))
    return total

def count_question_headings(text):
    q_words = ['How', 'What', 'Why', 'When', 'Where', 'Can', 'Do', 'Is', 'Are', 'Does', 'Will', 'Should', 'কী', 'কেন', 'কখন', 'কোথায়']
    count = 0
    for line in text.split('\n'):
        line = line.strip()
        if line.startswith('#'):
            heading_text = line.lstrip('#').strip()
            for qw in q_words:
                if heading_text.startswith(qw + ' ') or heading_text.startswith(qw + '?') or heading_text.startswith(qw + ':'):
                    count += 1
                    break
    return count

def count_internal_links(text):
    links = set()
    for m in re.finditer(r'\[([^\]]*)\]\((/[^)]*)\)', text):
        link = m.group(2)
        if any(link.startswith(p) for p in ['/blog/', '/services/', '/locations/', '/industries/', '/about', '/contact']):
            links.add(link)
    for m in re.finditer(r'href="(/[^"]*)"', text):
        link = m.group(1)
        if any(link.startswith(p) for p in ['/blog/', '/services/', '/locations/', '/industries/', '/about', '/contact']):
            links.add(link)
    return list(links)

def extract_primary_keyword(title):
    t = title.strip().lower()
    known = {
        'seo for fitness and gym businesses in bangladesh': ['fitness', 'gym'],
        'seo for law firms and legal services in bangladesh': ['law firm', 'legal services'],
        'b2b lead generation through seo in bangladesh': ['b2b lead generation', 'b2b seo'],
        'seo for startups in bangladesh': ['startup seo', 'startups'],
        'howto স্কিমা': ['howto schema', 'স্কিমা'],
        'faq স্কিমা': ['faq schema', 'স্কিমা'],
    }
    for pattern, kws in known.items():
        if pattern in t:
            return kws
    for stop in [' seo ', ' in bangladesh', ' complete guide', ' the ultimate guide', ' a complete ']:
        t = t.replace(stop, ' ')
    parts = [p.strip() for p in t.split() if p.strip() and len(p.strip()) > 2]
    if parts:
        return [parts[0]]
    return ['keyword']

# --- Run ---

with open('src/app/blog/data.js', 'r') as f:
    content = f.read()

# Add FAQ schema post
slugs_to_check = [
    'seo-for-fitness-gyms-bangladesh',
    'seo-for-law-firms-bangladesh',
    'b2b-lead-generation-seo-bangladesh',
    'seo-for-startups-bangladesh',
    'seo-howto-schema-bangladesh',
    'seo-faq-schema-bangladesh',
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
    body = get_content_body(post)
    full_text = title + '\n' + excerpt + '\n' + body
    
    print(f"\n## Post: {slug}")
    print(f"**Title:** {title}  |  **Date:** {date}")
    print()
    print("| Check | Status | Details |")
    print("|-------|--------|---------|")
    
    post_passed = True
    
    # A. TF-IDF
    primary_kws = extract_primary_keyword(title)
    kw_count = count_keyword(full_text, primary_kws)
    tfidf_status = '✅' if kw_count >= 5 else '❌'
    if tfidf_status == '❌': post_passed = False; all_passed = False
    kw_display = ' / '.join(primary_kws)
    print(f"| TF-IDF: `{kw_display}` | {tfidf_status} | {kw_count} occurrences{' (too thin!)' if kw_count < 5 else ''} |")
    
    # B. Entities (handles both Latin & Bengali script)
    entity_checks = {
        'Bangladesh (বাংলাদেশ)': ['Bangladesh', 'Bangladeshi', 'বাংলাদেশ', 'বাংলাদেশি'],
        'Dhaka (ঢাকা)': ['Dhaka', 'ঢাকা', 'ঢাকায়'],
        'Location pages': ['/locations/'],
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
    
    # C. Pillar link
    internal_links_all = count_internal_links(body)
    pillar_guide_links = [l for l in internal_links_all if any(
        l.startswith(p) for p in ['/blog/complete-seo-guide-', '/blog/seo-guide-']
    )]
    service_links = [l for l in internal_links_all if l.startswith('/services/')]
    has_pillar_link = len(pillar_guide_links) > 0
    
    if has_pillar_link:
        pillar_detail = f"Links to: {', '.join(pillar_guide_links[:3])}"
        pillar_status = '✅'
    elif len(internal_links_all) >= 3:
        pillar_detail = f"No direct pillar guide link; {len(internal_links_all)} internal links ({len(service_links)} to services)"
        pillar_status = '⚠'
    else:
        pillar_detail = 'No pillar page or sufficient internal links'
        pillar_status = '❌'; post_passed = False; all_passed = False
    print(f"| Pillar Link | {pillar_status} | {pillar_detail} |")
    
    # D. AEO
    q_count = count_question_headings(body)
    has_faq = bool(re.search(r'##\s*FAQ|##\s*(Frequently Asked|প্রায়শই|সাধারণ জিজ্ঞাসা|প্রশ্নোত্তর)', body))
    
    if q_count >= 2 or (q_count >= 1 and has_faq):
        aeo_status = '✅'
        aeo_detail = f'{q_count} question headings' + (' + FAQ' if has_faq else '')
    else:
        aeo_status = '❌'
        aeo_detail = f'{q_count} question headings (need ≥2 or add FAQ)'
        post_passed = False; all_passed = False
    print(f"| AEO/GEO | {aeo_status} | {aeo_detail} |")
    
    # E. Internal links
    link_count = len(internal_links_all)
    link_status = '✅' if link_count >= 3 else '❌'
    if link_status == '❌': post_passed = False; all_passed = False
    link_examples = ', '.join(internal_links_all[:5])
    if len(internal_links_all) > 5: link_examples += '...'
    print(f"| Internal Links | {link_status} | {link_count} total: {link_examples} |")
    
    # F. Schema
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
        fixes.append(f"- **TF-IDF thin**: Add more `{' / '.join(primary_kws)}` (currently {kw_count}, need ≥5).")
    if missing_entities:
        for e in missing_entities:
            fixes.append(f"- **Missing: {e}** — Add mention in content body.")
    if not has_pillar_link:
        fixes.append(f"- **Pillar link**: Add link to `/blog/complete-seo-guide-bangladesh-businesses-2026` for stronger cluster signal.")
    if q_count < 2 and not has_faq:
        fixes.append(f"- **AEO**: Add ≥2 question headings (How/What/Why or Bengali equivalents). Current: {q_count}.")
    if link_count < 3:
        fixes.append(f"- **Internal linking**: {link_count} links found, need ≥3. Link to services, locations, or related posts.")
    if schema_missing:
        fixes.append(f"- **Schema**: Set missing fields: {', '.join(schema_missing)}.")
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
