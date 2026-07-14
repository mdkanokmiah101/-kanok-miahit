#!/usr/bin/env python3
"""Full check of the original script's regex patterns."""
import re

FILEPATH = "/root/kanok-miahit/src/app/blog/data.js"

with open(FILEPATH, "r", encoding="utf-8") as f:
    text = f.read()

# Replicate the original script exactly
post_pattern = re.compile(
    r'\{\s*\n\s+slug:\s*"([^"]+)"(.*?)\n\s+\},?\s*\n\s*(?=\{\s*\n\s+slug:)',
    re.DOTALL
)

def get_content_block(block):
    m = re.search(r'content:\s*`((?:[^`\\]|\\.)*)`', block, re.DOTALL)
    if m:
        return m.group(1)
    return ""

slug = "seo-hreflang-guide-bangladesh"

for m in post_pattern.finditer(text):
    if m.group(1) == slug:
        block = m.group(0)
        print(f"Block length: {len(block)}")
        
        content = get_content_block(block)
        print(f"Content length: {len(content)}")
        
        # Test the regex
        internal_links = re.findall(r'href="(/[^"]*)"', content)
        print(f"All internal links: {internal_links}")
        
        # Also test /services regex
        services_links = re.findall(r'/services/[^"]*', content)
        print(f"Services links: {services_links}")
        
        # Check if "on-page-seo" is in content
        print(f"'on-page-seo' in content: {'on-page-seo' in content}")
        print(f"'technical-seo' in content: {'technical-seo' in content}")
        
        # Find all href in content
        all_href = [m for m in re.finditer(r'href="([^"]*)"', content)]
        print(f"All href matches: {[(m.start(), m.group(1)) for m in all_href]}")
        
        break
