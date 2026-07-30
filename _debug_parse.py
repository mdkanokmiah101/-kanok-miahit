#!/usr/bin/env python3
"""Debug: check which posts are being parsed correctly."""
import re

with open("src/app/blog/data.js") as f:
    content = f.read()

# Try a different parsing approach - extract slugs one by one
# Find all slug occurrences
slugs = re.findall(r'slug:\s*"([^"]+)"', content)
print(f"Total slugs found in file: {len(slugs)}")

# Check for the specific missing slugs
missing = [
    'ai-seo-2026-dhaka-experts-optimize-google-ai-chatgpt',
    'how-to-choose-best-seo-expert-dhaka-15-things',
    'seo-expert-vs-seo-agency-dhaka-which-is-right',
    'what-does-seo-expert-do-guide-business-owners',
]

for s in missing:
    if s in slugs:
        print(f"✅ '{s}' found in slugs list")
    else:
        print(f"❌ '{s}' NOT found in slugs list")

# Now parse by splitting by slug: to get each post
parts = content.split('slug: "')
print(f"\nNumber of parts when split by slug: {len(parts)}")
found_slugs = [p.split('"')[0] for p in parts[1:]]
print(f"Found {len(found_slugs)} slugs")

for s in missing:
    if s in found_slugs:
        print(f"✅ '{s}' found in split-based parsing")
    else:
        print(f"❌ '{s}' NOT found in split-based parsing")

# Check what's at the line around the how-to-choose post
lines = content.split('\n')
print(f"\nLines around line 25420-25470:")
for i in range(25420, min(25470, len(lines))):
    line = lines[i]
    if len(line) > 100:
        line = line[:100] + "..."
    print(f"  {i+1}: {line}")
