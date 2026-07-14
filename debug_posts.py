#!/usr/bin/env python3
"""Debug: Check what content is being extracted for specific posts."""
import re

FILEPATH = "/root/kanok-miahit/src/app/blog/data.js"

with open(FILEPATH, "r", encoding="utf-8") as f:
    text = f.read()

# Check the post near hreflang
slug = "seo-hreflang-guide-bangladesh"

# Find the post by slug
idx = text.find(f'slug: "{slug}"')
print(f"Found slug at index: {idx}")

# Get a window around it (5000 chars before and after)
start = max(0, idx - 100)
end = min(len(text), idx + 3000)
window = text[start:end]
print(f"Window length: {len(window)}")
print("---Window excerpt (last 500 chars):")
print(window[-500:])
print("---")

# Now find the end: look for the pattern `,\n  },\n  {
m = re.search(r'`,\s*\n\s*\},\s*\n\s*\{\s*\n\s+slug:', window)
if m:
    print(f"Found end pattern at pos {m.start()} in window")
    print(f"Last 100 chars before end pattern: ...{window[m.start()-100:m.start()]}")
else:
    print("End pattern NOT found!")
    # Try looking further
    end2 = min(len(text), idx + 5000)
    window2 = text[start:end2]
    m2 = re.search(r'`,\s*\n\s*\},\s*\n\s*\{\s*\n\s+slug:', window2)
    if m2:
        print(f"Found end pattern at pos {m2.start()} in extended window")
    else:
        print("Still not found in extended window")
        # Show what comes after
        print(f"Window from idx+2000: {text[idx+2000:idx+2100]}")

# Check what my regex finds
post_pattern = re.compile(
    r'\{\s*\n\s+slug:\s*"([^"]+)"(.*?)\n\s+\},?\s*\n\s*(?=\{\s*\n\s+slug:)',
    re.DOTALL
)
for m in post_pattern.finditer(text):
    if m.group(1) == slug:
        content = m.group(2)
        print(f"\n\nCaptured block length: {len(content)}")
        print(f"Last 200 chars: ...{content[-200:]}")
        # Check for internal links
        links = re.findall(r'href="(/[^"]*)"', content)
        print(f"Internal links found: {links}")
        break
