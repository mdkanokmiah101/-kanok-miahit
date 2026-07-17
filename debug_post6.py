#!/usr/bin/env python3
"""Debug post 6 content."""
import re

with open('src/app/blog/data.js', 'r') as f:
    data = f.read()

slug = 'seo-vs-google-ads-bangladesh-business'
lines = data.split('\n')

start = None
for i, line in enumerate(lines):
    if 'slug: "' + slug + '"' in line:
        start = i
        break

print('Start line: ' + str(start+1))

in_content = False
content_lines = []
for i, line in enumerate(lines):
    if i == start:
        # start processing from the slug line
        pass
    if 'content: `' in line and start <= i < start+20:
        in_content = True
        continue
    if in_content:
        if line.strip().startswith('`'):
            break
        content_lines.append(line)

content = '\n'.join(content_lines)
print('Content length: ' + str(len(content)))

# Check keywords
print('Contains "এসইও": ' + str('এসইও' in content))
print('Contains "বনাম": ' + str('বনাম' in content))
print('Contains "এসইও বনাম": ' + str('এসইও বনাম' in content))
print('Count এসইও: ' + str(content.count('এসইও')))
print('Count বনাম: ' + str(content.count('বনাম')))
print('Count গুগল: ' + str(content.count('গুগল')))
print('Count ডিজিটাল মার্কেটিং: ' + str(content.count('ডিজিটাল মার্কেটিং')))

# Check for digital marketing in English
content_lower = content.lower()
print('Count digital marketing: ' + str(content_lower.count('digital marketing')))
print('First 200 chars: ' + repr(content[:200]))
