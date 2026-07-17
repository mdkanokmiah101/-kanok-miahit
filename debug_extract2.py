#!/usr/bin/env python3
"""Debug extract_post function."""
import re

with open('src/app/blog/data.js', 'r') as f:
    data = f.read()

slug = 'complete-seo-guide-bangladesh-businesses-2026'
lines = data.split('\n')

# Find slug line
slug_line_idx = None
for i, line in enumerate(lines):
    if 'slug: "' + slug + '"' in line:
        slug_line_idx = i
        break

print('Slug at line ' + str(slug_line_idx+1))

# Go back to find opening {
start_idx = slug_line_idx
while start_idx >= 0:
    stripped = lines[start_idx].strip()
    print('  Looking back: line ' + str(start_idx+1) + ': ' + repr(stripped[:80]))
    if stripped == '{' or stripped == '{,':
        break
    start_idx -= 1

print('Found open brace at line ' + str(start_idx+1) + ': ' + repr(lines[start_idx]))

# Now find the closing
brace_depth = 0
in_content = False
end_idx = start_idx

for i in range(start_idx, len(lines)):
    line = lines[i]
    stripped = line.strip()
    
    if not in_content:
        if '{' in stripped:
            brace_depth += 1
        if '}' in stripped:
            brace_depth -= 1
        
        if 'content: `' in line:
            in_content = True
            print('  Found content start at line ' + str(i+1) + ', brace_depth=' + str(brace_depth))
        
        if brace_depth <= 0 and i > start_idx:
            end_idx = i
            print('  Brace depth zero at line ' + str(i+1) + ': ' + repr(stripped[:80]))
            break
    else:
        # In content
        if stripped.startswith('`') and i > start_idx:
            in_content = False
            print('  Found backtick close at line ' + str(i+1) + ': ' + repr(stripped[:80]))
        # Still count braces
        if '{' in stripped:
            brace_depth += stripped.count('{')
        if '}' in stripped:
            brace_depth -= stripped.count('}')

print('End idx: ' + str(end_idx+1))
print('Object lines: ' + str(end_idx - start_idx + 1))
obj_text = '\n'.join(lines[start_idx:end_idx+1])
print('Object text first 300: ' + repr(obj_text[:300]))
print('Object text last 300: ' + repr(obj_text[-300:]))
