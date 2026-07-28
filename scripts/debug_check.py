#!/usr/bin/env python3
"""
Quick debug script to find which check returns None.
"""
import re

filepath = '/root/kanok-miahit/src/app/blog/data.js'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Check if "watchzonebd-seo-case-study" exists
if 'watchzonebd-seo-case-study' in content:
    print("Found watchzonebd-seo-case-study")
    
# Check the slug regex
pattern = r'{\s*\n\s+slug:\s*"([^"]+)"'
matches = list(re.finditer(pattern, content))
print(f"Total posts found: {len(matches)}")
for m in matches[:5]:
    print(f"  slug: {m.group(1)}")
    
# Check if watchzonebd's slug is in the matches
watchzone = [m for m in matches if m.group(1) == 'watchzonebd-seo-case-study']
print(f"watchzonebd matches: {len(watchzone)}")

# Show last 5 slugs
for m in matches[-5:]:
    print(f"  slug: {m.group(1)}")
