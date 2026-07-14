#!/usr/bin/env python3
"""Debug internal links extraction."""
import re

FILEPATH = "/root/kanok-miahit/src/app/blog/data.js"

with open(FILEPATH, "r", encoding="utf-8") as f:
    text = f.read()

slug = "seo-hreflang-guide-bangladesh"

# Find the block
idx = text.find(f'slug: "{slug}"')
# Go back to find the opening {
block_start = text.rfind('{', max(0, idx - 20), idx)
print(f"Block starts at: {block_start}")

# Now extract content from this block
block = text[block_start:]

# Find the end: `,\n  },\n  { or `,\n  }\n\n{
# Try different patterns
for pattern_name, pattern_str in [
    ("end1", r"`,\s*\n\s*\},\s*\n\s*\{\s*\n\s+slug:"),
    ("end2", r"`,\s*\n\s*\},\s*\n\s*\n\s*\{\s*\n\s+slug:"),
]:
    m = re.search(pattern_str, block)
    if m:
        print(f"Found end via {pattern_name} at pos {m.start()}")
        block = block[:m.start()]
        break
else:
    # Just find the first closing pattern
    m = re.search(r"`,\s*\n\s*\}", block)
    if m:
        block = block[:m.start() + 1]  # include closing backtick? No, include the backtick
        print(f"Found end via generic at pos {m.start()}")
    else:
        print("Cannot find end!")

print(f"\nBlock length: {len(block)}")

# Extract content
content_match = re.search(r'content:\s*`((?:[^`\\]|\\.)*)`', block, re.DOTALL)
if content_match:
    content = content_match.group(1)
    print(f"Content length: {len(content)}")
    print(f"\nLast 300 chars of content:\n{content[-300:]}")
    
    # Check for internal links
    links = re.findall(r'href="(/[^"]*)"', content)
    print(f"\nInternal links found: {links}")
    
    # Also check with simpler regex
    links2 = re.findall(r'/services/[^"]*', content)
    print(f"Services links: {links2}")
else:
    print("Content not found!")
    # Try to find content field
    content_field = re.search(r'content:\s*`', block)
    if content_field:
        print(f"Found content field at pos {content_field.start()}")
        # Show what follows
        rest = block[content_field.start():content_field.start()+200]
        print(f"Next 200 chars: {rest}")
