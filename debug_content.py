#!/usr/bin/env python3
"""Debug content extraction."""

import re

DATA_FILE = "src/app/blog/data.js"

with open(DATA_FILE, 'r') as f:
    data = f.read()

lines = data.split('\n')
slug = 'complete-seo-guide-bangladesh-businesses-2026'

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
    if stripped == '{' or stripped == '{,':
        break
    start_idx -= 1

print('Start index: ' + str(start_idx+1))

# Go forward to find closing }
brace_depth = 0
in_content = False
end_idx = start_idx

for i in range(start_idx, len(lines)):
    stripped = lines[i].strip()
    
    if not in_content:
        if '{' in stripped:
            brace_depth += stripped.count('{') - stripped.count('}')
        if '}' in stripped:
            brace_depth += stripped.count('}') - stripped.count('{')
        
        if 'content: `' in lines[i]:
            in_content = True
            print('Content start at line ' + str(i+1))
        
        if brace_depth <= 0 and i > start_idx:
            end_idx = i
            break
    else:
        if stripped.startswith('`') and i > start_idx:
            in_content = False
            print('Content end at line ' + str(i+1) + ': ' + repr(stripped))
        if '{' in stripped:
            brace_depth += stripped.count('{')
        if '}' in stripped:
            brace_depth -= stripped.count('}')

obj_text = '\n'.join(lines[start_idx:end_idx+1])
print('Object text length: ' + str(len(obj_text)))

# Now try to get content
print('---')
print('Looking for content: ` in obj_text...')
idx = obj_text.find('content: `')
print('idx=' + str(idx))
if idx == -1:
    # Try other variations
    idx = obj_text.find('content: `')
    print('idx (alt)=' + str(idx))
    if idx == -1:
        # Look for content: followed by backtick
        idx = obj_text.find('content:')
        print('content: at idx=' + str(idx))
        if idx != -1:
            after = obj_text[idx:idx+50]
            print('After: ' + repr(after))

if idx != -1:
    bt_open = obj_text.index('`', idx)
    print('backtick at idx=' + str(bt_open))
    content_start = bt_open + 1
    rest = obj_text[content_start:]
    print('rest length: ' + str(len(rest)))
    print('rest first 50: ' + repr(rest[:50]))
    print('rest last 50: ' + repr(rest[-50:]))
    
    last_bt = rest.rfind('`')
    print('last backtick at offset: ' + str(last_bt))
    
    if last_bt != -1:
        content = rest[:last_bt]
        print('Content extracted! Length: ' + str(len(content)))
        print('First 100: ' + repr(content[:100]))
        print('Last 100: ' + repr(content[-100:]))
    else:
        print('NO LAST BACKTICK FOUND')
