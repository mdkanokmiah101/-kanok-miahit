#!/usr/bin/env python3
"""Analyze blog posts for framework checks A, E, F and write results to a file."""

import re
import json

with open('/root/kanok-miahit/src/app/blog/data.js', 'r') as f:
    lines = f.readlines()

# Define line ranges for each target post (1-indexed)
posts = {
    "locksmith-dundee-seo-case-study": {
        "title": "Locksmith Dundee SEO Case Study: How We Generated 1,000+ Monthly Visitors from Local Search",
        "start": 24681, "end": 24879,
        "keyword": "locksmith dundee"
    },
    "how-to-choose-best-seo-expert-dhaka-15-things": {
        "title": "How to Choose the Best SEO Expert in Dhaka: 15 Things to Check",
        "start": 25417, "end": 25619,
        "keyword": "seo expert dhaka"
    },
    "seo-expert-vs-seo-agency-dhaka-which-is-right": {
        "title": "SEO Expert vs SEO Agency in Dhaka: Which One is Right for Your Business?",
        "start": 25622, "end": 25849,
        "keyword": "seo expert"
    },
    "top-10-seo-mistakes-dhaka-businesses-fix": {
        "title": "Top 10 SEO Mistakes Dhaka Businesses Make (And How to Fix Them)",
        "start": 25852, "end": 26046,
        "keyword": "seo mistakes"
    },
    "what-does-seo-expert-do-guide-business-owners": {
        "title": "What Does an SEO Expert Actually Do? A Complete Guide for Business Owners",
        "start": 26051, "end": 26389,
        "keyword": "seo expert"
    },
    "seo-case-study-dhaka-businesses-increased-organic-traffic": {
        "title": "SEO Case Study: How Businesses in Dhaka Increased Organic Traffic",
        "start": 26392, "end": 26718,
        "keyword": "seo case study"
    },
    "hiring-seo-expert-dhaka-better-roi-than-paid-ads": {
        "title": "Why Hiring an SEO Expert in Dhaka Delivers Better ROI Than Paid Ads",
        "start": 26721, "end": 26997,
        "keyword": "seo roi"
    },
    "ai-seo-2026-dhaka-experts-optimize-google-ai-chatgpt": {
        "title": "AI SEO in 2026: How SEO Experts in Dhaka Optimize for Google AI & ChatGPT",
        "start": 27001, "end": 27289,
        "keyword": "ai seo"
    },
    "watchzonebd-seo-case-study": {
        "title": "WatchZoneBD SEO Case Study: How We Scaled Organic Traffic from 1,004 to 40,000+ Monthly Visits",
        "start": 27292, "end": 27510,
        "keyword": "watchzonebd"
    },
}

def get_content_text(post_start, post_end):
    """Extract the content field (template literal) from the post."""
    post_text = ''.join(lines[post_start-1:post_end])
    # Find content: `...`
    m = re.search(r'content:\s*`((?:.|\n)*?)`,\s*\n', post_text, re.DOTALL)
    if m:
        return m.group(1)
    # Try alternate - find backtick after content:
    idx = post_text.find('content:')
    if idx == -1:
        return ""
    rest = post_text[idx:]
    start = rest.find('`')
    if start == -1:
        return ""
    rest = rest[start+1:]
    end = rest.rfind('`')
    if end == -1:
        return ""
    return rest[:end]

def count_keyword(text, keyword):
    """Count case-insensitive keyword occurrences."""
    if not text or not keyword:
        return 0
    return len(re.findall(re.escape(keyword), text, re.IGNORECASE))

def find_internal_links(text):
    """Find internal links: markdown links with / paths."""
    if not text:
        return []
    links = re.findall(r'\[([^\]]*)\]\(([^)]*)\)', text)
    internal = []
    for link_text, url in links:
        # Internal: starts with / (but not //)
        if url.startswith('/') and not url.startswith('//'):
            internal.append((link_text, url))
        # Also kanokmiah.com.bd with path
        elif 'kanokmiah.com.bd' in url:
            path = url.split('kanokmiah.com.bd')[1]
            internal.append((link_text, path if path else '/'))
    return internal

def find_schema_mentions(text):
    """Find schema/structured data mentions."""
    if not text:
        return []
    patterns = [
        r'\bschema\b', r'structured data', r'JSON-LD', r'Schema\.org',
        r'rich snippet', r'LocalBusiness', r'Organization',
        r'Product schema', r'Review schema', r'FAQ schema',
        r'Breadcrumb', r'HowTo', r'schema markup'
    ]
    found = set()
    for p in patterns:
        if re.search(p, text, re.IGNORECASE):
            found.add(p)
    return sorted(found)

results = []
for slug, info in posts.items():
    content = get_content_text(info["start"], info["end"])
    keyword = info["keyword"]
    
    # Check A: keyword count
    kw_count = count_keyword(content, keyword)
    
    # Check E: internal links
    internal_links = find_internal_links(content)
    int_count = len(internal_links)
    
    # Check F: schema
    schema_mentions = find_schema_mentions(content)
    
    results.append((slug, info["title"], keyword, kw_count, int_count, internal_links, schema_mentions))

# Print results
print("=" * 130)
print(f"{'SLUG':50s} {'KEYWORD COUNT (A)':25s} {'INT LINKS (E)':15s} {'SCHEMA (F)'}")
print("=" * 130)

for slug, title, kw, kw_count, int_count, int_links, schema in results:
    short_slug = slug[:48] if len(slug) > 48 else slug
    kw_str = f"{kw} = {kw_count}"
    int_str = f"{int_count} links"
    schema_str = ", ".join(schema[:5]) if schema else "NONE"
    if len(schema) > 5:
        schema_str += f" (+{len(schema)-5})"
    print(f"{short_slug:50s} {kw_str:25s} {int_str:15s} {schema_str}")

print()
print("=" * 130)
print("DETAILED RESULTS")
print("=" * 130)

for slug, title, kw, kw_count, int_count, int_links, schema in results:
    print(f"\n{'─'*100}")
    print(f"📄 {title}")
    print(f"   Slug: {slug}")
    print(f"   ├── [A] Keyword '{kw}': {kw_count} occurrences")
    print(f"   ├── [E] Internal links: {int_count}")
    if int_links:
        for t, u in int_links:
            print(f"   │     [{t}]({u})")
    print(f"   └── [F] Schema mentions ({len(schema)}):")
    if schema:
        for s in schema:
            print(f"        • {s}")
    else:
        print("        NONE")
