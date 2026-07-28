#!/usr/bin/env python3
"""Extract changed posts from data.js for framework checking."""
import re
import json

with open('src/app/blog/data.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Slugs that were modified in the last commit
changed_slugs = [
    "geo-optimization-prepare-business-ai-search",
    "seo-garments-textile-industry-b2b-lead-generation",
    "seo-healthcare-medical-clinics-bangladesh",
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

# Check landlord-certificates too
for s in ["landlord-certificates-seo-case-study"]:
    if s in content:
        changed_slugs.append(s)

posts = []
# Simple parser - find each post block
pattern = r'(\s*\{\s*\n\s*slug:\s*"([^"]+)"[^}]+?\n\s*\})'
# Use a more robust approach: split by '{' and match slug
lines = content.split('\n')
i = 0
while i < len(lines):
    line = lines[i]
    # Find line with slug
    m = re.match(r'\s+slug:\s*"([^"]+)"', line)
    if m:
        slug = m.group(1)
        if slug in changed_slugs:
            # Collect the post block
            block_lines = []
            # Go back to find the opening {
            j = i
            while j >= 0:
                if '{' in lines[j]:
                    block_lines = lines[j-1:i-1]  # include lines before slug
                    break
                j -= 1
            
            # Now collect forward until we hit closing }, at proper nesting
            depth = 0
            started = False
            block = []
            for k in range(i, len(lines)):
                block.append(lines[k])
                depth += lines[k].count('{')
                depth -= lines[k].count('}')
                if depth <= 0 and started:
                    break
                if '{' in lines[k] and not started:
                    started = True
            
            post_text = '\n'.join(block)
            
            # Extract fields
            title_m = re.search(r'title:\s*"([^"]+)"', post_text)
            date_m = re.search(r'date:\s*"([^"]+)"', post_text)
            excerpt_m = re.search(r'excerpt:\n\s*"([^"]+)"', post_text)
            if not excerpt_m:
                excerpt_m = re.search(r'excerpt:\s*"([^"]+)"', post_text)
            tags_m = re.findall(r'"([^"]+)"', post_text.split('tags:')[1].split(']')[0]) if 'tags:' in post_text else []
            # Get content - between content: ` and closing `,
            content_m = re.search(r'content:\s*`(.*?)`\s*,?\s*\n', post_text, re.DOTALL)
            if not content_m:
                # Try alternate pattern
                idx = post_text.find('content: `')
                if idx >= 0:
                    # Find closing backtick
                    rest = post_text[idx+9:]
                    end_idx = rest.find('`\n')
                    if end_idx >= 0:
                        content_m = rest[:end_idx]
            
            post = {
                'slug': slug,
                'title': title_m.group(1) if title_m else '',
                'date': date_m.group(1) if date_m else '',
                'excerpt': excerpt_m.group(1) if excerpt_m else '',
                'tags': tags_m[:8] if tags_m else [],
                'content': content_m if isinstance(content_m, str) else (content_m.group(1) if content_m else ''),
            }
            posts.append(post)
            
            # Also get the full content properly
            idx = post_text.find('content: `')
            if idx >= 0:
                rest = post_text[idx+9:]
                end_idx = rest.rfind('`')
                if end_idx >= 0:
                    post['content'] = rest[:end_idx]
            
            print(f"Extracted: {slug} (title: {post['title'][:50]})")
    i += 1

with open('/tmp/extracted_posts.json', 'w') as f:
    json.dump(posts, f, indent=2, ensure_ascii=False)

print(f"\nTotal extracted: {len(posts)}")
for p in posts:
    print(f"  - {p['slug']}: content length={len(p.get('content', ''))}")
