#!/usr/bin/env python3
"""Check content around the link area."""
import re

FILEPATH = "/root/kanok-miahit/src/app/blog/data.js"

with open(FILEPATH, "r", encoding="utf-8") as f:
    text = f.read()

# Find content around the hreflang post where the link should be
idx = text.find('slug: "seo-hreflang-guide-bangladesh"')
block_start = text.rfind('{', max(0, idx - 20), idx)
block = text[block_start:]

# Cut at end
end_m = re.search(r"`,\s*\n\s*\},\s*\n\s*\{\s*\n\s+slug:", block)
if end_m:
    block = block[:end_m.start() + 1]
    
# Find content
cf = re.search(r'content:\s*`', block)
if cf:
    after = block[cf.end():]
    # Find unescaped closing backtick
    i = 0
    while i < len(after):
        if after[i] == '\\' and i + 1 < len(after):
            i += 2
        elif after[i] == '`':
            content = after[:i]
            break
        else:
            i += 1
    
    print(f"Content length: {len(content)}")
    
    # Search for the link
    idx_link = content.find('/services/on-page-seo')
    print(f"Link found at index: {idx_link}")
    if idx_link >= 0:
        print(f"Context: ...{content[max(0,idx_link-30):idx_link+50]}...")
    else:
        # Check the very end
        print(f"Last 200 chars of content: {repr(content[-200:])}")
        print(f"\nLast 300 chars of content: {repr(content[-300:])}")
        
        # Check if the link text is anywhere
        all_href = re.findall(r'href="[^"]*"', content)
        print(f"\nAll href attributes: {all_href}")
        
        # Check what's around the end of the content
        # Find the last occurrence of 'সেবা'
        last_s = content.rfind('সেবা')
        print(f"\nLast 'সেবা' at index: {last_s}")
        if last_s >= 0:
            print(f"After 'সেবা': {repr(content[last_s:last_s+100])}")
