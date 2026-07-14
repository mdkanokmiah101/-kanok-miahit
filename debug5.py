#!/usr/bin/env python3
"""Debug the original check logic - test regex patterns and content extraction."""
import re

FILEPATH = "/root/kanok-miahit/src/app/blog/data.js"

with open(FILEPATH, "r", encoding="utf-8") as f:
    text = f.read()

# Test 1: The post_pattern
post_pattern = re.compile(
    r'\{\s*\n\s+slug:\s*"([^"]+)"(.*?)\n\s+\},?\s*\n\s*(?=\{\s*\n\s+slug:)',
    re.DOTALL
)

slug = "seo-hreflang-guide-bangladesh"

# Find via finditer
for m in post_pattern.finditer(text):
    if m.group(1) == slug:
        block = m.group(0)
        print(f"finditer block length: {len(block)}")
        print(f"finditer block last 100 chars: {repr(block[-100:])}")
        
        # Extract content
        content_match = re.search(r'content:\s*`((?:[^`\\]|\\.)*)`', block, re.DOTALL)
        if content_match:
            content = content_match.group(1)
            print(f"Content length: {len(content)}")
            print(f"Content last 100 chars: {repr(content[-100:])}")
            links = re.findall(r'href="(/[^"]*)"', content)
            print(f"Internal links: {links}")
        else:
            print("Content regex FAILED on this block!")
            
            # Debug: find content field
            cf = re.search(r'content:\s*`', block)
            if cf:
                after = block[cf.end():]
                print(f"After content opening: first 100 chars: {repr(after[:100])}")
                # Check if there are unescaped backticks at all
                all_ticks = [i for i, c in enumerate(after) if c == '`']
                print(f"All backtick positions in after (first 20): {all_ticks[:20]}")
                print(f"All backtick positions in after (last 10): {all_ticks[-10:]}")
                for pos in all_ticks[-5:]:
                    before = after[max(0,pos-5):pos]
                    print(f"  Last ticks - pos {pos}: before={repr(before)}")
                for pos in all_ticks[:5]:
                    before = after[max(0,pos-5):pos]
                    print(f"  First ticks - pos {pos}: before={repr(before)}")
        break

print("\n\n--- Test 2: Simpler content extraction ---")
# Try a different approach: find content field and track backticks
idx = text.find(f'slug: "{slug}"')
block_start = text.rfind('{', max(0, idx - 20), idx)
block = text[block_start:]

# Cut the block at the end pattern
end_m = re.search(r"`,\s*\n\s*\},\s*\n\s*\{\s*\n\s+slug:", block)
if end_m:
    block = block[:end_m.start() + 1]  # include the closing backtick
    print(f"Block length after cutting: {len(block)}")
    print(f"Block last 50 chars: {repr(block[-50:])}")
else:
    print("End pattern not found!")
    # Try more flexible pattern
    end_m2 = re.search(r"`,\s*\n\s*\}", block)
    if end_m2:
        block = block[:end_m2.start() + 1]
        print(f"Block (flexible) last 50 chars: {repr(block[-50:])}")

# Now find content
content_field = re.search(r'content:\s*`', block)
if content_field:
    after = block[content_field.end():]
    print(f"\nAfter opening backtick - length: {len(after)}")
    # Find unescaped closing backtick manually
    i = 0
    while i < len(after):
        if after[i] == '\\' and i + 1 < len(after):
            i += 2  # skip escaped char
        elif after[i] == '`':
            print(f"Found unescaped closing backtick at pos {i}")
            content = after[:i]
            print(f"Content length: {len(content)}")
            print(f"Content last 100 chars: {repr(content[-100:])}")
            links = re.findall(r'href="(/[^"]*)"', content)
            print(f"Internal links: {links}")
            break
        else:
            i += 1
    else:
        print("No unescaped backtick found!")
