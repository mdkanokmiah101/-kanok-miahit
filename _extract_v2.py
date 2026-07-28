#!/usr/bin/env python3
"""Extract changed posts from data.js - improved parser."""
import re
import json

with open('src/app/blog/data.js', 'r', encoding='utf-8') as f:
    content = f.read()

changed_slugs = [
    "geo-optimization-prepare-business-ai-search",
    "seo-garments-textile-industry-b2b-lead-generation",
    "seo-healthcare-medical-clinics-bangladesh",
    "why-md-kanok-miah-is-the-best-seo-expert-in-dhaka-bangladesh",
    "locksmith-dundee-seo-case-study",
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
    "watchzonebd-seo-case-study",
]

# Split into individual post objects by finding top-level { ... },
# but we need to track brace depth
posts_raw = []
depth = 0
start = None
for i, ch in enumerate(content):
    if ch == '{':
        if depth == 0:
            start = i
        depth += 1
    elif ch == '}':
        depth -= 1
        if depth == 0 and start is not None:
            block = content[start:i+1]
            if 'slug:' in block:
                posts_raw.append(block)
            start = None

print(f"Found {len(posts_raw)} post blocks total")

# Filter to changed slugs only
posts = []
for block in posts_raw:
    slug_m = re.search(r'slug:\s*"([^"]+)"', block)
    if slug_m and slug_m.group(1) in changed_slugs:
        slug = slug_m.group(1)
        
        title_m = re.search(r'title:\s*"([^"]+)"', block)
        date_m = re.search(r'date:\s*"([^"]+)"', block)
        excerpt_m = re.search(r'excerpt:\s*"([^"]+)"', block)
        if not excerpt_m:
            excerpt_m = re.search(r'excerpt:\n\s*"([^"]+)"', block)
        
        tags_match = re.search(r'tags:\s*\[([^\]]+)\]', block)
        tags = re.findall(r'"([^"]+)"', tags_match.group(1)) if tags_match else []
        
        # Extract content between backticks
        # Find content: ` ... `
        content_match = re.search(r'content:\s*`(.*?)`\s*,?\s*$', block, re.DOTALL | re.MULTILINE)
        if not content_match:
            # Try with the content spanning multiple lines
            idx = block.find('content: `')
            if idx >= 0:
                rest = block[idx+9:]
                end_idx = rest.rfind('`')
                if end_idx >= 0:
                    post_content = rest[:end_idx]
                else:
                    post_content = ''
            else:
                post_content = ''
        else:
            post_content = content_match.group(1)
        
        post = {
            'slug': slug,
            'title': title_m.group(1) if title_m else '',
            'date': date_m.group(1) if date_m else '',
            'excerpt': excerpt_m.group(1).strip() if excerpt_m else '',
            'tags': tags,
            'content': post_content,
        }
        posts.append(post)
        print(f"  {slug}: content_len={len(post_content)}, title={post['title'][:60]}")

with open('/tmp/extracted_posts.json', 'w') as f:
    json.dump(posts, f, indent=2, ensure_ascii=False)

print(f"\nTotal: {len(posts)} posts")
