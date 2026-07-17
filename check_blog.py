#!/usr/bin/env python3
"""Comprehensive audit of blog post headings in data.js"""
import re

with open('/root/kanok-miahit/src/app/blog/data.js', 'r') as f:
    content = f.read()
    lines = content.split('\n')

# Find all template literal content blocks (blog posts)
# Pattern: content: ` ... ` followed by , or // or end of line
# This is tricky with JS template literals because they can span many lines
# Let's find all opening backticks after 'content: ' and their matching close

posts = []
in_post = False
post_start = 0
depth = 0
for i, line in enumerate(lines):
    stripped = line.strip()
    if 'content:' in stripped and not in_post:
        # Find the backtick
        idx = stripped.find('`')
        if idx >= 0:
            in_post = True
            post_start = i
            # Check if there's more content on this line after the backtick
            after_tick = stripped[idx+1:]
            if '`' in after_tick:
                # The template literal could close on the same line for empty content
                # But for our case, content is multi-line
                pass
    elif in_post:
        if '`' in stripped:
            # Check if this backtick closes our template literal
            # It should be followed by , or ; or // or whitespace
            tick_idx = stripped.index('`')
            after = stripped[tick_idx+1:].strip()
            if after == '' or after.startswith(',') or after.startswith(';') or after.startswith('//'):
                posts.append((post_start, i, lines[post_start:i+1]))
                in_post = False

print(f"Found {len(posts)} blog posts with content template literals\n")

all_headings = []
current_post_idx = -1
post_headings = []

for post_num, (start, end, post_lines) in enumerate(posts, 1):
    print(f"=== Post {post_num} (lines {start+1}-{end+1}) ===")
    
    in_code = False
    post_issues = []
    post_h_tags = []
    
    for offset, line in enumerate(post_lines):
        lineno = start + offset + 1
        stripped = line.strip()
        
        # Track code blocks
        if stripped.startswith('```'):
            in_code = not in_code
            continue
        if in_code:
            continue
            
        # Check for markdown headings
        heading_match = re.match(r'^(#{1,6})\s+(.+)$', stripped)
        if heading_match:
            level = len(heading_match.group(1))
            text = heading_match.group(2)
            post_h_tags.append((lineno, level, text))
        
        # Check for raw HTML heading tags
        if re.search(r'<h[2-6][^>]*>', stripped, re.IGNORECASE):
            post_issues.append((lineno, f"Raw HTML h tag: {stripped[:80]}"))
        
        # Check for <p> tags
        if re.search(r'<p[^>]*>', stripped, re.IGNORECASE) and not re.match(r'^[\s]*\* ', stripped):
            # Only flag if it looks like HTML, not markdown
            if '<p ' in stripped or stripped.strip() == '<p>' or stripped.strip().startswith('<p>'):
                post_issues.append((lineno, f"Raw HTML p tag: {stripped[:80]}"))
        
        # Check for <strong> and <em> tags (should use ** and *)
        if re.search(r'<strong[^>]*>', stripped, re.IGNORECASE):
            post_issues.append((lineno, f"Raw HTML strong tag: {stripped[:80]}"))
        if re.search(r'<em[^>]*>', stripped, re.IGNORECASE):
            post_issues.append((lineno, f"Raw HTML em tag: {stripped[:80]}"))
        if re.search(r'<(b|i)>', stripped, re.IGNORECASE):
            post_issues.append((lineno, f"Raw HTML <{stripped.strip()[1:3]}> tag: {stripped[:80]}"))
    
    # Check heading structure
    prev_level = 0
    heading_structure_issues = []
    for lineno, level, text in post_h_tags:
        if prev_level and level > prev_level + 1:
            heading_structure_issues.append((lineno, f"Heading jump: {prev_level}→{level}: {'#'*level} {text[:50]}"))
        prev_level = level
    
    # Print results
    if post_issues:
        print(f"  ISSUES ({len(post_issues)}):")
        for lineno, msg in post_issues:
            print(f"    Line {lineno}: {msg}")
    else:
        print("  No raw HTML tag issues found")
    
    if heading_structure_issues:
        print(f"  STRUCTURE ISSUES ({len(heading_structure_issues)}):")
        for lineno, msg in heading_structure_issues:
            print(f"    Line {lineno}: {msg}")
    else:
        print("  No heading structure issues")
    
    print(f"  Headings: {len(post_h_tags)} found")
    for lineno, level, text in post_h_tags:
        print(f"    Line {lineno}: {'#'*level} {text[:60]}")
    print()

    all_headings.extend(post_h_tags)
