#!/usr/bin/env python3
"""Debug content extraction for hiring-seo-expert-dhaka-better-roi-than-paid-ads."""
import re

with open('/root/kanok-miahit/src/app/blog/data.js', 'r', encoding='utf-8') as f:
    content = f.read()

slug = "hiring-seo-expert-dhaka-better-roi-than-paid-ads"
idx = content.find(f'slug: "{slug}"')
print(f"Found slug at index {idx}")

# Extract post
start = idx
while start > 0 and content[start] != '{':
    start -= 1
before = content[:idx]
last_brace = before.rfind('}')
after_brace = before[last_brace+1:] if last_brace >= 0 else before
brace_pos = after_brace.find('{')
if brace_pos >= 0:
    start = last_brace + 1 + brace_pos if last_brace >= 0 else brace_pos

print(f"Post starts at index {start}")

# Just extract and print the content field roughly
content_field = content[start:]
# Find content: ` ... `
cm = re.search(r'content:\s*`', content_field)
if cm:
    cstart = cm.start()
    # Walk forward to find closing backtick
    cpos = cm.end()
    while cpos < len(content_field):
        if content_field[cpos] == '\\':
            cpos += 2
            continue
        if content_field[cpos] == '`':
            break
        cpos += 1
    extracted = content_field[cm.end():cpos]
    print(f"\nContent extracted: {len(extracted)} chars")
    print(f"First 200 chars: {extracted[:200]}")
    print(f"\nLast 200 chars: {extracted[-200:]}")
    
    # Count 'seo expert' case insensitive
    count = len(re.findall(r'seo expert', extracted, re.IGNORECASE))
    print(f"\n'seo expert' count case-insensitive: {count}")
    
    # Also check 'seo consultant' 
    count2 = len(re.findall(r'seo consultant', extracted, re.IGNORECASE))
    print(f"'seo consultant' count case-insensitive: {count2}")
    
    # Check 'seo'
    count3 = len(re.findall(r'\bseo\b', extracted, re.IGNORECASE))
    print(f"'seo' word count: {count3}")
else:
    print("Could not find content field!")
