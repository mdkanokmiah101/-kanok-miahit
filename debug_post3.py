#!/usr/bin/env python3
import re

with open('/root/kanok-miahit/src/app/blog/data.js', 'r', encoding='utf-8') as f:
    content = f.read()

slug = 'why-md-kanok-miah-is-the-best-seo-expert-in-dhaka-bangladesh'
slug_idx = content.find(f'slug: "{slug}"')
print(f"Slug at index: {slug_idx}")

# Show 500 chars after slug to see the structure
chunk = content[slug_idx:slug_idx+500]
print(f"\n--- 500 chars after slug ---")
print(chunk[:500])

# Find 'content:\n' specifically
idx = slug_idx
while idx < len(content):
    next_line_end = content.find('\n', idx)
    if next_line_end == -1:
        break
    line = content[idx:next_line_end]
    if 'content:' in line:
        print(f"\nFound 'content:' at {idx}: {line}")
        # Find backtick
        bt = content.find('`', idx)
        print(f"Backtick at {bt}: context = {repr(content[bt:bt+20])}")
        # Find closing backtick
        ct = content.find('`,', bt+1)
        if ct == -1:
            ct = content.find("`\n", bt+1)
        if ct == -1:
            # Search for the pattern more flexibly
            ct = content.find('`,', bt+1)
        print(f"Closing at {ct}: context = {repr(content[ct:ct+20])}")
        break
    idx = next_line_end + 1
