#!/usr/bin/env python3
"""Extract a single blog post from data.js by slug."""
import re, json, sys

slug_target = sys.argv[1]

with open('src/app/blog/data.js', 'r') as f:
    data = f.read()

# Find the post block - match from slug to next slug or end
pattern = r"slug:\s*\"(" + re.escape(slug_target) + r")\".*?(?=slug:\s*\"|\Z)"
match = re.search(pattern, data, re.DOTALL)
if not match:
    print(f"Post '{slug_target}' not found!")
    sys.exit(1)

block = match.group(0)

# Extract fields
fields = {}
fields['slug'] = slug_target

# title
m = re.search(r'title:\s*"((?:[^"\\]|\\.)*)"', block)
if m: fields['title'] = m.group(1)

# date
m = re.search(r'date:\s*"([^"]*)"', block)
if m: fields['date'] = m.group(1)

# excerpt
m = re.search(r'excerpt:\s*"((?:[^"\\]|\\.)*)"', block)
if m: fields['excerpt'] = m.group(1)

# tags
m = re.search(r'tags:\s*\[([^\]]*)\]', block)
if m: fields['tags'] = [t.strip().strip('"') for t in m.group(1).split(',')]

# metaTitle
m = re.search(r'metaTitle:\s*"((?:[^"\\]|\\.)*)"', block)
if m: fields['metaTitle'] = m.group(1)

# metaDescription
m = re.search(r'metaDescription:\s*"((?:[^"\\]|\\.)*)"', block)
if m: fields['metaDescription'] = m.group(1)

# dateModified
m = re.search(r'dateModified:\s*"([^"]*)"', block)
if m: fields['dateModified'] = m.group(1)

# content
m = re.search(r'content:\s*`((?:[^`\\]|\\.)*)`', block, re.DOTALL)
if m: fields['content'] = m.group(1)

print(json.dumps(fields, indent=2, ensure_ascii=False))
