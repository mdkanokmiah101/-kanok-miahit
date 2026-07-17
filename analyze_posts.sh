#!/usr/bin/env python3
import re
import sys
import json

# Read data.js
with open('src/app/blog/data.js', 'r') as f:
    content = f.read()

# Extract all posts using regex
# Find each post object between { ... }
posts_raw = re.findall(r'\{[^{}]*slug:\s*"([^"]*)"[^{}]*\}', content, re.DOTALL)

# Actually, let's be smarter. Extract post by post using a more robust approach
# Each post is an object inside the posts array
# Let's extract each slug and its position
slugs = re.findall(r'slug:\s*"([^"]*)"', content)

# The posts we know were recently modified (from git log)
recent_slugs = [
    "seo-for-facebook-marketplace",
    "long-tail-keywords-bangladesh",
    "seo-tips-for-business-owners-bd",
    "seo-bangla-blog-content-writing",
    "seo-vs-google-ads-bangladesh-business",
    "youtube-seo-bangladesh-ranking-tips",
    "schema-markup-rich-snippets-techniques",
    "mobile-seo-bangladesh-ranking-strategy",
    "google-search-console-performance-guide",
    "content-marketing-seo-friendly-content-writing",
    "keyword-research-bangladesh-market",
    "link-building-bangladesh-strategies",
    "ecommerce-seo-daraz-shopify-guide",
    "technical-seo-core-web-vitals-optimization",
    "seo-trends-2026-ai-geo-future",
    "local-seo-dhaka-google-maps-ranking",
    "seo-bangla-beginners-guide-google-ranking",
    "international-seo-bangladesh-exporters-global-buyers",
    "content-marketing-strategy-bangladeshi-brands-seo",
    "mobile-seo-optimization-bangladesh-mobile-first-era",
    "seo-real-estate-developers-dhaka",
    "seo-vs-google-ads-whats-best-bangladesh-businesses",
    "google-business-profile-optimization-guide-bangladesh",
    "seo-garments-textile-industry-b2b-lead-generation",
    "geo-optimization-prepare-business-ai-search",
    "link-building-strategies-bangladesh-market",
    "how-to-choose-right-seo-agency-bangladesh",
    "technical-seo-checklist-bangladeshi-websites",
    "why-ecommerce-store-needs-seo-bangladesh",
    "local-seo-tips-dhaka-businesses-google-maps",
]

# For each slug, find the line number with the slug
lines = content.split('\n')

# Find line numbers for each slug
slug_lines = {}
for i, line in enumerate(lines, 1):
    m = re.search(r'slug:\s*"([^"]*)"', line)
    if m:
        slug_lines[m.group(1)] = i

for slug in recent_slugs:
    if slug in slug_lines:
        print(f"Post: {slug} (line {slug_lines[slug]})")
    else:
        print(f"Post: {slug} (NOT FOUND in data.js!)")
