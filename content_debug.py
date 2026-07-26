#!/usr/bin/env python3
"""Debug the content extraction from a post object."""
import re

DATA_FILE = "/root/kanok-miahit/src/app/blog/data.js"

with open(DATA_FILE, "r", encoding="utf-8") as f:
    text = f.read()

# Find the geo-optimization post around line 1022
lines = text.split('\n')
print(f"Total lines: {len(lines)}")
print(f"Line 1020-1035:")
for i in range(1020, min(1036, len(lines))):
    print(f"  {i}: {repr(lines[i])}")

# Try to extract one post object
# Find "slug: \"geo-optimization" 
idx = text.find('slug: "geo-optimization-prepare-business-ai-search"')
if idx >= 0:
    # Find the opening { of this object - go back from slug
    before = text[:idx]
    brace_pos = before.rfind('{')
    print(f"\nFound slug at: {idx}")
    print(f"Opening brace at: {brace_pos}")
    print(f"Context around brace ({brace_pos-3}:{brace_pos+3}): {repr(text[brace_pos-3:brace_pos+3])}")
    
    # Now find the closing of this object
    # Track brace depth from opening
    depth = 0
    in_backtick = False
    i = brace_pos
    while i < len(text):
        ch = text[i]
        if in_backtick:
            if ch == '`':
                in_backtick = False
        else:
            if ch == '`':
                in_backtick = True
            elif ch == '{':
                depth += 1
            elif ch == '}':
                depth -= 1
                if depth == 0:
                    obj_end = i + 1
                    obj_text = text[brace_pos:obj_end]
                    print(f"\nExtracted object length: {len(obj_text)}")
                    print(f"Last 100 chars of obj: {repr(obj_text[-100:])}")
                    
                    # Try content regex
                    content_match = re.search(r'content:\s*`([\s\S]*?)`', obj_text)
                    if content_match:
                        print(f"Content found: {len(content_match.group(1))} chars")
                        print(f"First 100: {content_match.group(1)[:100]}")
                    else:
                        print("Content regex did NOT match")
                        # Check if 'content:' exists
                        if 'content:' in obj_text:
                            print("'content:' IS in the object text")
                            ci = obj_text.find('content:')
                            print(f"Context around 'content:': {repr(obj_text[ci:ci+50])}")
                        else:
                            print("'content:' NOT in object text")
                    break
        i += 1
    else:
        print("Could not find closing brace")
