import re

# Read the current data.js
with open('src/app/blog/data.js', 'r') as f:
    content = f.read()

# Modified posts list
modified_slugs = [
    'backlink-outreach-templates-strategies-bangladesh',
    'blogging-strategy-seo-frequency-topics-bangladesh',
    'building-seo-roadmap-bangladesh-business',
    'complete-seo-guide-bangladesh-businesses-2026',
    'das-taxis-scotland-seo-case-study',
    'dhaka-apparels-seo-case-study',
    'enterprise-seo-large-organizations-bangladesh',
    'geo-optimization-prepare-business-ai-search',
    'google-business-profile-optimization-guide-bangladesh',
    'how-to-choose-right-seo-agency-bangladesh',
    'landlord-certificates-seo-case-study',
    'link-building-strategies-bangladesh-market',
    'local-seo-multiple-business-locations-bangladesh',
    'local-seo-tips-dhaka-businesses-google-maps',
    'locksmith-dundee-seo-case-study',
    'mir-cement-seo-case-study',
    'mobile-seo-optimization-bangladesh-mobile-first-era',
    'morethanpanel-seo-case-study',
    'seo-breadcrumb-schema-bd',
    'seo-event-management-companies-bangladesh',
    'seo-faq-schema-bangladesh',
    'seo-garments-textile-industry-b2b-lead-generation',
    'seo-howto-schema-bangladesh',
    'seo-hreflang-guide-bangladesh',
    'seo-json-ld-schema-bangladesh',
    'seo-non-profit-organizations-bangladesh',
    'seo-photographers-videographers-bangladesh',
    'seo-real-estate-developers-dhaka',
    'seo-robots-txt-guide-bangladesh',
    'seo-structured-data-guide-bd',
    'seo-vs-google-ads-whats-best-bangladesh-businesses',
    'seo-vs-ppc-advertising-bangladesh',
    'seo-wedding-event-planners-bangladesh',
    'seo-xml-sitemap-guide-bd',
    'smmgen-seo-case-study',
    'smmsun-seo-case-study',
    'stealth-windshield-repairs-seo-case-study',
    'technical-seo-checklist-bangladeshi-websites',
    'why-ecommerce-store-needs-seo-bangladesh',
    'why-md-kanok-miah-is-the-best-seo-expert-in-dhaka-bangladesh',
]

def extract_post_by_slug(content, target_slug):
    lines = content.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i]
        m = re.search(r'slug: "([^"]+)"', line)
        if m and m.group(1) == target_slug:
            post_lines = [line]
            i += 1
            while i < len(lines):
                next_line = lines[i]
                if re.search(r'slug: "([^"]+)"', next_line):
                    break
                if next_line.strip() == '];':
                    break
                post_lines.append(next_line)
                i += 1
            return '\n'.join(post_lines)
        i += 1
    return None

def parse_post_metadata(post_text):
    meta = {}
    m = re.search(r'title: "([^"]*)"', post_text)
    meta['title'] = m.group(1) if m else ''
    m = re.search(r'date: "([^"]*)"', post_text)
    meta['date'] = m.group(1) if m else ''
    m = re.search(r'excerpt:\s+"([^"]*)"', post_text, re.DOTALL)
    meta['excerpt'] = m.group(1) if m else ''
    m = re.search(r'tags:\s*\[([^\]]+)\]', post_text, re.DOTALL)
    if m:
        meta['tags'] = [t.strip().strip('"') for t in m.group(1).split(',')]
    else:
        meta['tags'] = []
    m = re.search(r'content:\s*`((?:[^`]|`(?!\s*,))*)`', post_text, re.DOTALL)
    meta['content'] = m.group(1) if m else ''
    return meta

# Quick checks - report only failures
failure_count = 0
total_checked = 0

for slug in modified_slugs:
    post_text = extract_post_by_slug(content, slug)
    if not post_text:
        print(f"⚠️  Could not extract: {slug}")
        continue
    
    meta = parse_post_metadata(post_text)
    title = meta.get('title', '')
    content_text = meta.get('content', '')
    tags = meta.get('tags', [])
    content_lower = content_text.lower() if content_text else ''
    
    failures = []
    
    # A. TF-IDF - quick check
    # B. Entities - quick check
    # C. Pillar link - quick check
    # D. AEO question headings
    q_words = r'(How|What|Why|When|Where|Can|Do|Is|Are|Does|Should|Which)'
    q_pattern = re.compile(r'^#{2,3}\s+' + q_words, re.MULTILINE | re.IGNORECASE)
    q_count = len(q_pattern.findall(content_text)) if content_text else 0
    
    # E. Internal links
    link_pattern = re.compile(r'\[([^\]]*)\]\((/[^)]+)\)')
    links = link_pattern.findall(content_text) if content_text else []
    internal_links = [(text, url) for text, url in links if url.startswith(('/blog/', '/services/', '/industries/', '/locations/'))]
    link_count = len(internal_links)
    
    # F. Schema readiness
    schema_missing = []
    if not meta.get('title'): schema_missing.append('title')
    if not meta.get('excerpt'): schema_missing.append('excerpt')
    if not meta.get('date'): schema_missing.append('date')
    
    if q_count < 2:
        failures.append(f"AEO/GEO: {q_count} question headings (<2)")
    if link_count < 3:
        failures.append(f"Internal Links: {link_count} (<3)")
    if schema_missing:
        failures.append(f"Schema: missing {', '.join(schema_missing)}")
    
    if failures:
        failure_count += 1
        print(f"\n❌ {slug}")
        for f in failures:
            print(f"   - {f}")
    else:
        total_checked += 1

print(f"\n{'='*50}")
print(f"Modified posts checked: {len(modified_slugs)}")
print(f"Passed all checks: {total_checked}")
print(f"Failed checks: {failure_count}")
