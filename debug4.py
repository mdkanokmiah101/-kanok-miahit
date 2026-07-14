#!/usr/bin/env python3
"""Debug content extraction - find closing backtick."""
import re

FILEPATH = "/root/kanok-miahit/src/app/blog/data.js"

with open(FILEPATH, "r", encoding="utf-8") as f:
    text = f.read()

slug = "seo-hreflang-guide-bangladesh"

# Find block
idx = text.find(f'slug: "{slug}"')
block_start = text.rfind('{', max(0, idx - 20), idx)
block = text[block_start:]

# Find content start
content_start = block.find("content:")
rest = block[content_start:]
print(f"rest length: {len(rest)}")

# Find opening and closing backticks
# Opening: first backtick after content:
open_m = re.search(r'content:\s*`', rest)
if open_m:
    after_open = rest[open_m.end():]
    print(f"after_open length: {len(after_open)}")
    print(f"after_open last 100 chars: {repr(after_open[-100:])}")
    
    # Find ALL backticks in after_open
    all_ticks = [i for i, c in enumerate(after_open) if c == '`']
    print(f"Total backticks in after_open: {len(all_ticks)}")
    
    # Show last 10 backtick positions
    if all_ticks:
        print(f"Last 10 backtick positions in after_open: {all_ticks[-10:]}")
        for pos in all_ticks[-5:]:
            before = after_open[max(0,pos-5):pos]
            after = after_open[pos:pos+5]
            print(f"  pos {pos}: before={repr(before)}, after={repr(after)}")
    
    # Now, all backticks in after_open should be escaped EXCEPT the closing one
    # Check if the last character of after_open is a backtick
    print(f"\nLast char of after_open: {repr(after_open[-1])}")
    print(f"Last 3 chars: {repr(after_open[-3:])}")
    
    # The closing backtick pattern is: ...`,\n  } or ...`,\n  }\n\n{
    # Let me check what's at the very end of after_open (or rest)
    print(f"\nrest last 200 chars: {repr(rest[-200:])}")
