#!/usr/bin/env python3
"""Extract full blog post content from data.js and run framework checks."""
import re
import json
import os
import sys

target_slugs = [
    "seo-featured-snippet-bangladesh",
    "seo-knowledge-panel-bangladesh",
    "locksmith-dundee-seo-case-study",
    "das-taxis-scotland-seo-case-study",
    "morethanpanel-seo-case-study",
    "smmgen-seo-case-study",
    "smmsun-seo-case-study",
    "mir-cement-seo-case-study",
    "dhaka-apparels-seo-case-study",
    "stealth-windshield-repairs-seo-case-study",
    "seo-expert-vs-seo-agency-dhaka-which-is-right",
    "top-10-seo-mistakes-dhaka-businesses-fix",
    "seo-case-study-dhaka-businesses-increased-organic-traffic",
    "hiring-seo-expert-dhaka-better-roi-than-paid-ads",
    "watchzonebd-seo-case-study",
]

with open("src/app/blog/data.js", "r") as f:
    content = f.read()

def extract_post(slug):
    """Extract full post object from data.js."""
    idx = content.find('slug: "' + slug + '"')
    if idx < 0:
        return None
    
    # Search backwards for the opening brace
    obj_start = content.rfind('{', idx - 500, idx)
    
    # Parse the forward to find matching closing brace
    depth = 0
    in_template = False
    in_string = False
    escape = False
    
    for i in range(obj_start, len(content)):
        ch = content[i]
        
        if escape:
            escape = False
            continue
        if ch == '\\':
            escape = True
            continue
        if ch == '`':
            in_template = not in_template
            continue
        if ch == '"' and not in_template:
            in_string = not in_string
            continue
        
        if not in_string and not in_template:
            if ch == '{':
                depth += 1
            elif ch == '}':
                depth -= 1
                if depth == 0:
                    obj_end = i + 1
                    post_text = content[obj_start:obj_end]
                    return post_text
    
    return None

def parse_post_fields(post_text):
    """Extract fields from post object text."""
    slug_m = re.search(r'slug:\s*"([^"]*)"', post_text)
    title_m = re.search(r'title:\s*"([^"]*)"', post_text)
    date_m = re.search(r'date:\s*"([^"]*)"', post_text)
    excerpt_m = re.search(r'excerpt:\s*"([^"]*)"', post_text, re.DOTALL)
    tags_m = re.search(r'tags:\s*\[([^\]]*)\]', post_text, re.DOTALL)
    content_m = re.search(r'content:\s*`(.*)`', post_text, re.DOTALL)
    
    slug = slug_m.group(1) if slug_m else ""
    title = title_m.group(1) if title_m else ""
    date = date_m.group(1) if date_m else ""
    excerpt = excerpt_m.group(1) if excerpt_m else ""
    
    tags_list = []
    if tags_m:
        tags_text = tags_m.group(1)
        tags_list = re.findall(r'"([^"]*)"', tags_text)
    
    post_content = content_m.group(1) if content_m else ""
    
    return {
        "slug": slug,
        "title": title,
        "date": date,
        "excerpt": excerpt,
        "tags": tags_list,
        "content": post_content,
    }

# Load all posts
posts = []
for slug in target_slugs:
    text = extract_post(slug)
    if text:
        post = parse_post_fields(text)
        if "featured-snippet" in slug or "knowledge-panel" in slug:
            post["lang"] = "bn"
        else:
            post["lang"] = "en"
        posts.append(post)
        print(f"Extracted: {slug} ({len(post['content'])} chars content)")
    else:
        print(f"NOT FOUND: {slug}")

# Save full data
with open("/tmp/all_posts_full.json", "w") as f:
    json.dump(posts, f, ensure_ascii=False, indent=2)
print(f"\nSaved {len(posts)} posts to /tmp/all_posts_full.json")
