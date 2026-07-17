#!/usr/bin/env python3
"""Refined analysis for post 27 - use the real keyword patterns."""
import re

with open('/root/kanok-miahit/src/app/blog/data.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Find post 27
slug = "seo-vs-google-ads-bangladesh-business"
idx = content.find(f'slug: "{slug}"')
obj_start = content.rfind('{', 0, idx)
brace_count = 0
obj_end = obj_start
for i in range(obj_start, len(content)):
    if content[i] == '{': brace_count += 1
    elif content[i] == '}':
        brace_count -= 1
        if brace_count == 0:
            obj_end = i + 1
            break

obj_text = content[obj_start:obj_end]

# Extract content
m = re.search(r'content:\s*`\n(.*?)`\s*,?\s*\}', obj_text, re.DOTALL)
post_content = m.group(1) if m else ''

# Check various keyword forms in the content
print("=== Post 27: seo-vs-google-ads-bangladesh-business ===")
print(f"\nContent length: {len(post_content)} chars")

# Count keyword variations
checks = {
    'SEO': len(re.findall(r'\bSEO\b', post_content)),
    'Google Ads': len(re.findall(r'Google Ads', post_content)),
    'এসইও': len(re.findall(r'এসইও', post_content)),
    'গুগল অ্যাডস': len(re.findall(r'গুগল অ্যাডস', post_content)),
    'SEO and Google Ads': len(re.findall(r'SEO.*?Google Ads|Google Ads.*?SEO', post_content)),
}

for k, v in checks.items():
    print(f"  '{k}': {v} occurrences")

# Better primary keyword: "SEO" (from title "এসইও বনাম গুগল অ্যাডস")
seo_count = len(re.findall(r'\bSEO\b', post_content))
ga_count = len(re.findall(r'Google Ads', post_content))
print(f"\nPrimary keywords: 'SEO' = {seo_count}, 'Google Ads' = {ga_count}")
print(f"TF-IDF pass: {'✅' if seo_count >= 5 else '❌'} (using 'SEO' as primary keyword)")

# Count internal links
blog_links = len(re.findall(r'/blog/[^)\s"\'\)]+', post_content))
services_links = len(re.findall(r'/services/[^)\s"\'\)]+', post_content))
print(f"\nInternal links to /blog/: {blog_links}")
print(f"Internal links to /services/: {services_links}")

# Count blog links specifically
blog_link_urls = re.findall(r'/blog/[^)\s"\'\)]+', post_content)
print(f"\nBlog links found:")
for u in blog_link_urls:
    print(f"  {u}")

# Count service links
services_urls = re.findall(r'/services/[^)\s"\'\)]+', post_content)
print(f"\nService links found:")
for u in services_urls:
    print(f"  {u}")

# Check pillar link
pillar_url = '/blog/seo-vs-google-ads-whats-best-bangladesh-businesses'
print(f"\nPillar link present: {'✅' if pillar_url in post_content else '❌'}")
