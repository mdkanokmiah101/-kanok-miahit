#!/usr/bin/env python3
"""Debug the content extraction."""
import re

with open('src/app/blog/data.js', 'r') as f:
    data = f.read()

slug = 'complete-seo-guide-bangladesh-businesses-2026'
pattern = re.compile(rf'slug:\s*"{re.escape(slug)}"')
m = pattern.search(data)

content_pos = data.find('content:', m.start())
print(f'content at index: {content_pos}')
print(f'Content start context: {repr(data[content_pos:content_pos+100])}')

# The backtick opens at content_pos + 9 for "content: `"
bt_open = content_pos + 9  # after 'content: '
print(f'Char at bt_open: {repr(data[bt_open])}')

# Rest is from after the opening backtick
rest = data[bt_open+1:]

# Find closing backtick - look for backtick followed by comma/newline
# Try backward from a likely area
for i, c in enumerate(rest):
    if c == '`':
        after = rest[i+1:i+5]
        if ',' in after or '\n' in after or '//' in after or rest[i-1] == '\n':
            print(f'Candidate closing backtick at offset {i}')
            print(f'Context: {repr(rest[max(0,i-50):i+50])}')
            break
else:
    # Try just the first backtick in rest that's at the end of a line
    m2 = re.search(r'\n`\s*,', rest)
    if m2:
        print(f'Found via regex at offset {m2.start()}')
        print(f'Context: {repr(rest[m2.start()-30:m2.start()+50])}')
    else:
        m3 = re.search(r'`\s*,\s*//', rest)
        if m3:
            print(f'Found via regex2 at offset {m3.start()}')
            print(f'Context: {repr(rest[m3.start()-30:m3.start()+50])}')
        else:
            print('No closing backtick found')
            # Look at what's around post end
            # Post 1 content should end around ~line 158
            lines = data.split('\n')
            for i in range(155, 165):
                print(f'Line {i+1}: {repr(lines[i][:200])}')
