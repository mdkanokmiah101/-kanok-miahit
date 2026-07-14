#!/usr/bin/env python3
import re
import sys

with open('src/app/blog/data.js','r') as f:
    c = f.read()

slug = sys.argv[1]

# Find the line number where this post's slug is defined (the actual post, not a reference)
lines = c.split('\n')
post_start = None
for i, line in enumerate(lines):
    stripped = line.strip()
    if stripped.startswith('slug:') and f'"{slug}"' in stripped:
        post_start = i
        break

if post_start is None:
    print(f"Post '{slug}' not found")
    sys.exit(1)

print(f'Post slug at line {post_start+1}')

# Work backwards to find the opening brace
for i in range(post_start, -1, -1):
    if '{' in lines[i]:
        # Skip if this is the const posts = [ line
        stripped = lines[i].strip()
        if stripped == 'const posts = [':
            continue
        post_start_line = i
        break

print(f'Post object starts at line {post_start_line+1}')
print(f'  Line: {lines[post_start_line][:100]}')

# Find matching closing brace by tracking depth
depth = 0
in_content = False
content_start = None
content_end = None

for i in range(post_start_line, len(lines)):
    line = lines[i]
    
    # Check if we're entering the content template literal
    if 'content:' in line and not in_content:
        # Find the backtick
        ci = line.find('`')
        if ci >= 0:
            in_content = True
            content_start = i
            # If content is inline (starts and ends on same line)
            line_after = line[ci+1:]
            btc = line_after.find('`')
            if btc >= 0:
                content = line_after[:btc]
                content_end = i
                break
            # Content continues on next lines
            continue
    
    if in_content:
        # Look for closing backtick
        btc = line.find('`')
        if btc >= 0:
            content_end = i
            break
    
    # Count braces for structure tracking (only when not in content)
    if not in_content:
        for ch in line:
            if ch == '{':
                depth += 1
            elif ch == '}':
                depth -= 1

if content_start and content_end:
    # Extract content
    content_lines = lines[content_start:content_end+1]
    # Remove the content: prefix from first line
    first_line = content_lines[0]
    ci = first_line.find('`')
    first_line_content = first_line[ci+1:]
    rest_lines = content_lines[1:-1] if len(content_lines) > 2 else []
    last_line = content_lines[-1]
    lci = last_line.find('`')
    last_line_content = last_line[:lci] if lci >= 0 else ''
    
    content = first_line_content + '\n'.join(rest_lines) + last_line_content
    
    print(f'Content length: {len(content)}')
    
    # Check for question headings
    heading_lines = re.findall(r'^#{1,3}\s+(.*)', content, re.MULTILINE)
    q_headings = [h for h in heading_lines if '?' in h or '\u0995\u09c0' in h]
    print(f'Total headings: {len(heading_lines)}')
    print(f'Question headings: {len(q_headings)}')
    if q_headings:
        for h in q_headings[:5]:
            print(f'  - {h[:60]}')
    
    # Internal links
    links = re.findall(r'\[([^\]]*)\]\(/(?!http|#|www)[^)]+\)', content)
    print(f'Internal links: {len(links)}')
    if links:
        for link in links[:5]:
            print(f'  [{link[0]}](/{link[1]})')
    
    # Entity check
    content_lower = content.lower()
    print(f'Has Bangladesh: {"বাংলাদেশ" in content or "bangladesh" in content_lower}')
    print(f'Has Dhaka: {"ঢাকা" in content or "dhaka" in content_lower}')
    
else:
    print(f'Content not found. in_content={in_content}')
    # Debug - show lines around where content should be
    for i in range(post_start_line, min(post_start_line+10, len(lines))):
        print(f'  Line {i+1}: {lines[i][:100]}')
