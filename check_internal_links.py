#!/usr/bin/env python3
"""Count internal links (to /blog/, /services/, /locations/, /industries/) in each blog post's content field,
and verify title, excerpt, date fields exist for schema readiness."""

import re
import json

# Read the file
with open('/root/kanok-miahit/src/app/blog/data.js', 'r') as f:
    content = f.read()

# Extract each post object - simplify by regex splitting on slug patterns
# First, find all slug lines and their positions
slug_pattern = re.compile(r"slug:\s*['\"]([^'\"]+)['\"]")

# Find all posts by splitting on '{' and looking for slug
# Better approach: find line ranges for each post
lines = content.split('\n')

posts_to_check = [
    "why-md-kanok-miah-is-the-best-seo-expert-in-dhaka-bangladesh",
    "locksmith-dundee-seo-case-study",
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
    "watchzonebd-seo-case-study",
]

# Find line number for each slug
slug_lines = {}
for i, line in enumerate(lines, 1):
    m = slug_pattern.search(line)
    if m and m.group(1) in posts_to_check:
        slug_lines[m.group(1)] = i

print(f"Found {len(slug_lines)} posts to check")
for s, ln in slug_lines.items():
    print(f"  {s}: line {ln}")

# Now extract content for each post by finding its boundaries
# A post starts with a line that has "slug:" and ends at the next "  }," or "},"
# Actually, the pattern is: each post is an object like:
#   {
#     slug: "...",
#     ...
#     content: `...`,
#   },
# We need to find each slug and then extract the content between content: \` and \`,

# Let me extract the content field using regex
results = []

for slug in posts_to_check:
    # Find the post object containing this slug
    # First find the slug line position
    slug_pos = content.find(f"slug: \"{slug}\"")
    if slug_pos == -1:
        slug_pos = content.find(f"slug: '{slug}'")
    
    if slug_pos == -1:
        results.append((slug, "NOT FOUND", False, False))
        continue
    
    # Find the content field - look for "content: `" or "content:`"
    content_start = content.find("content: `", slug_pos)
    if content_start == -1:
        content_start = content.find("content:`", slug_pos)
    
    if content_start == -1:
        results.append((slug, "NO CONTENT FIELD", False, False))
        continue
    
    # content starts after the backtick
    content_start_actual = content.index('`', content_start) + 1
    
    # Find closing backtick followed by ,
    # Look for the closing backtick that's followed by `,`
    content_end = content.find("`,", content_start_actual)
    if content_end == -1:
        # Try just backtick at end
        content_end = content.find("`", content_start_actual)
    
    post_content = content[content_start_actual:content_end]
    
    # Count internal links
    # Links starting with /blog/, /services/, /locations/, /industries/ in markdown [text](url) format
    # Also check for plain text URL patterns
    link_pattern = re.compile(r'\[([^\]]*)\]\((/[^)]*)\)')
    links = link_pattern.findall(post_content)
    
    internal_links = []
    for text, url in links:
        if any(url.startswith(p) for p in ['/blog/', '/services/', '/locations/', '/industries/']):
            internal_links.append((text, url))
    
    # Also check for non-markdown internal links (e.g., just /blog/... in text)
    # But for now we only count markdown links as per the threshold definition
    
    # Check for title, excerpt, date in the post object (before the content field)
    post_before_content = content[slug_pos:content_start]
    has_title = 'title:' in post_before_content
    has_excerpt = 'excerpt:' in post_before_content
    has_date = 'date:' in post_before_content
    
    results.append((slug, len(internal_links), has_title and has_excerpt and has_date, internal_links))

# Print results
print("\n\n")
print("=" * 100)
print(f"{'Slug':<65} {'Internal Links':<18} {'Schema Ready':<15}")
print("=" * 100)
all_pass = True
for slug, link_count, schema_ready, links in results:
    status = "✅ PASS" if link_count >= 3 and schema_ready else "❌ FAIL"
    if link_count < 3:
        all_pass = False
    if not schema_ready:
        all_pass = False
    print(f"{slug:<65} {str(link_count):<18} {'✅' if schema_ready else '❌':<15} {status}")
    if link_count < 3:
        print(f"  ⚠️  Only {link_count} internal links (need 3+)")
        for t, u in links:
            print(f"     [{t}]({u})")
    if not schema_ready:
        print(f"  ⚠️  Missing title/excerpt/date")

print("=" * 100)
if all_pass:
    print("\n✅ ALL POSTS PASS: Each has ≥3 internal links and is schema-ready")
else:
    print("\n❌ SOME POSTS FAIL: See details above")

# Print detailed link info for all posts
print("\n\nDETAILED INTERNAL LINKS PER POST:")
print("=" * 100)
for slug, link_count, schema_ready, links in results:
    print(f"\n--- {slug} ---")
    print(f"  Internal links: {link_count}")
    for t, u in links:
        print(f"    [{t}]({u})")
