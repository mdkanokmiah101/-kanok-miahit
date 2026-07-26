#!/usr/bin/env python3
"""Extract full blog post data from data.js for analysis."""
import re
import json

target_slugs = {
    "seo-featured-snippet-bangladesh": {"lang": "bn"},
    "seo-knowledge-panel-bangladesh": {"lang": "bn"},
    "locksmith-dundee-seo-case-study": {"lang": "en"},
    "das-taxis-scotland-seo-case-study": {"lang": "en"},
    "morethanpanel-seo-case-study": {"lang": "en"},
    "smmgen-seo-case-study": {"lang": "en"},
    "smmsun-seo-case-study": {"lang": "en"},
    "mir-cement-seo-case-study": {"lang": "en"},
    "dhaka-apparels-seo-case-study": {"lang": "en"},
    "stealth-windshield-repairs-seo-case-study": {"lang": "en"},
    "seo-expert-vs-seo-agency-dhaka-which-is-right": {"lang": "en"},
    "top-10-seo-mistakes-dhaka-businesses-fix": {"lang": "en"},
    "seo-case-study-dhaka-businesses-increased-organic-traffic": {"lang": "en"},
    "hiring-seo-expert-dhaka-better-roi-than-paid-ads": {"lang": "en"},
    "watchzonebd-seo-case-study": {"lang": "en"},
}

with open("src/app/blog/data.js", "r") as f:
    content = f.read()

# Find each post by slug and extract the full object
for slug, info in target_slugs.items():
    idx = content.find('slug: "' + slug + '"')
    if idx < 0:
        print(f"NOT FOUND: {slug}")
        continue
    
    # Find the opening brace of the object - search backwards
    obj_start = content.rfind('{', idx - 500, idx)
    
    # Find the closing brace - need to count braces
    # Strategy: find "}," or "}\n" after the slug position
    depth = 0
    obj_end = obj_start
    in_template = False
    in_string = False
    escape = False
    template_depth = 0
    
    for i in range(obj_start, len(content)):
        ch = content[i]
        
        if escape:
            escape = False
            continue
        if ch == '\\':
            escape = True
            continue
        if ch == '`' and not in_string:
            in_template = not in_template
            if not in_template:
                template_depth = 0
            continue
        if ch == '"' and not in_template:
            in_string = not in_string
            continue
        if in_template and ch == '$' and i+1 < len(content) and content[i+1] == '{':
            template_depth += 1
            continue
        
        if not in_string and not in_template:
            if ch == '{':
                depth += 1
            elif ch == '}':
                depth -= 1
                if depth == 0:
                    obj_end = i + 1
                    break
    
    post_text = content[obj_start:obj_end]
    
    # Extract basic fields
    title_match = re.search(r'title:\s*"([^"]*)"', post_text)
    title = title_match.group(1) if title_match else "N/A"
    
    date_match = re.search(r'date:\s*"([^"]*)"', post_text)
    date = date_match.group(1) if date_match else "N/A"
    
    excerpt_match = re.search(r'excerpt:\s*"([^"]*)"', post_text, re.DOTALL)
    excerpt = excerpt_match.group(1) if excerpt_match else "N/A"
    
    tags_match = re.search(r'tags:\s*\[([^\]]*)\]', post_text, re.DOTALL)
    tags_list = []
    if tags_match:
        tags_text = tags_match.group(1)
        tags_list = re.findall(r'"([^"]*)"', tags_text)
    
    # Extract content (the template literal)
    content_match = re.search(r'content:\s*`(.*)`', post_text, re.DOTALL)
    post_content = content_match.group(1) if content_match else ""
    
    # Save extracted data as JSON for analysis
    data = {
        "slug": slug,
        "title": title,
        "date": date,
        "excerpt": excerpt,
        "tags": tags_list,
        "content": post_content[:10000],  # Keep first 10000 chars of content
        "content_length": len(post_content),
    }
    
    with open(f"/tmp/post_{slug}.json", "w") as out:
        json.dump(data, out, ensure_ascii=False, indent=2)
    
    print(f"✓ Extracted: {slug} - {title[:50]}... ({len(post_content)} chars)")

print("\nDone!")
