#!/usr/bin/env python3
"""Test parsing and link extraction."""
import re
import sys

def parse_posts(filepath):
    with open(filepath, 'r') as f:
        source = f.read()
    
    posts = []
    i = 0
    in_double_quote = False
    in_backtick = False
    brace_depth = 0
    post_start = 0
    
    while i < len(source):
        c = source[i]
        if c == '"' and not in_backtick:
            if i == 0 or source[i-1] != '\\':
                in_double_quote = not in_double_quote
        elif c == '`' and not in_double_quote:
            if i == 0 or source[i-1] != '\\':
                in_backtick = not in_backtick
        elif not in_double_quote and not in_backtick:
            if c == '{':
                if brace_depth == 0:
                    post_start = i
                brace_depth += 1
            elif c == '}':
                brace_depth -= 1
                if brace_depth == 0 and post_start > 0:
                    post_str = source[post_start:i+1]
                    if 'slug' in post_str:
                        posts.append(post_str)
                    post_start = 0
        i += 1
    return posts

def extract_str_field(post_str, field_name):
    m = re.search(rf'{field_name}\s*:\s*"((?:[^"\\]|\\.)*)"', post_str)
    if m:
        return m.group(1)
    m = re.search(rf'{field_name}\s*:\s*\n\s*"((?:[^"\\]|\\.)*)"', post_str)
    if m:
        return m.group(1)
    return None

def extract_content(post_str):
    # content: `...` - template literal
    m = re.search(r'content\s*:\s*`', post_str)
    if not m:
        return ""
    start = m.end()
    # Find matching closing backtick - need to handle escaped backticks
    # In JS template literals, backticks inside ${} can appear, but we don't have that here
    # Simple: find next backtick
    end = post_str.find('`', start)
    if end == -1:
        return post_str[start:]
    return post_str[start:end]

filepath = '/root/kanok-miahit/src/app/blog/data.js'
posts = parse_posts(filepath)
print(f"Found {len(posts)} posts")

modified_slugs = [
    "backlink-outreach-templates-strategies-bangladesh",
    "blogging-strategy-seo-frequency-topics-bangladesh",
    "building-seo-roadmap-bangladesh-business",
    "complete-seo-guide-bangladesh-businesses-2026",
    "das-taxis-scotland-seo-case-study",
    "dhaka-apparels-seo-case-study",
    "enterprise-seo-large-organizations-bangladesh",
    "geo-optimization-prepare-business-ai-search",
    "google-business-profile-optimization-guide-bangladesh",
    "how-to-choose-right-seo-agency-bangladesh",
    "landlord-certificates-seo-case-study",
    "link-building-strategies-bangladesh-market",
    "local-seo-multiple-business-locations-bangladesh",
    "local-seo-tips-dhaka-businesses-google-maps",
    "locksmith-dundee-seo-case-study",
    "mir-cement-seo-case-study",
    "mobile-seo-optimization-bangladesh-mobile-first-era",
    "morethanpanel-seo-case-study",
    "seo-breadcrumb-schema-bd",
    "seo-event-management-companies-bangladesh",
    "seo-faq-schema-bangladesh",
    "seo-garments-textile-industry-b2b-lead-generation",
    "seo-howto-schema-bangladesh",
    "seo-hreflang-guide-bangladesh",
    "seo-json-ld-schema-bangladesh",
    "seo-non-profit-organizations-bangladesh",
    "seo-photographers-videographers-bangladesh",
    "seo-real-estate-developers-dhaka",
    "seo-robots-txt-guide-bangladesh",
    "seo-structured-data-guide-bd",
    "seo-vs-google-ads-whats-best-bangladesh-businesses",
    "seo-vs-ppc-advertising-bangladesh",
    "seo-wedding-event-planners-bangladesh",
    "seo-xml-sitemap-guide-bd",
    "smmgen-seo-case-study",
    "smmsun-seo-case-study",
    "stealth-windshield-repairs-seo-case-study",
    "technical-seo-checklist-bangladeshi-websites",
    "why-ecommerce-store-needs-seo-bangladesh",
    "why-md-kanok-miah-is-the-best-seo-expert-in-dhaka-bangladesh"
]

found = 0
for p in posts:
    slug = extract_str_field(p, 'slug')
    if slug in modified_slugs:
        found += 1
        content = extract_content(p)
        links = re.findall(r'\[([^\]]*)\]\(([^)]*)\)', content)
        print(f"\nPost: {slug}")
        print(f"  Content length: {len(content)}")
        print(f"  Links found: {len(links)}")
        for l in links[:5]:
            print(f"    '{l[0]}' -> '{l[1]}'")
        
        # Now test with the full regex
        full_content = content
        all_links = re.findall(r'\[([^\]]*)\]\(([^)]*)\)', full_content)
        print(f"  Total links with full regex: {len(all_links)}")

print(f"\nFound {found} of 40 modified posts")
