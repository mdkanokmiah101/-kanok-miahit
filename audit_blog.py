#!/usr/bin/env python3
"""Audit blog post data file for heading issues."""
import re

with open("/root/kanok-miahit/src/app/blog/data.js", "r", encoding="utf-8") as f:
    content = f.read()

issues = []

# 1. Check for raw HTML tags in template literal content areas
# First, extract all template literal content strings using backticks
# Find all content between backtick template literals
# We'll search for raw HTML tags outside code blocks

html_patterns = [
    (r'<h[1-6][>\s]', 'raw h1-h6 tag'),
    (r'</h[1-6]>', 'raw closing h tag'),
    (r'<p[>\s]', 'raw p tag'),
    (r'</p>', 'raw closing p tag'),
    (r'<strong[>\s]', 'raw strong tag'),
    (r'</strong>', 'raw closing strong tag'),
    (r'<b[>\s]', 'raw b tag'),
    (r'</b>', 'raw closing b tag'),
    (r'<em[>\s]', 'raw em tag'),
    (r'</em>', 'raw closing em tag'),
    (r'<i[>\s]', 'raw i tag'),
    (r'</i>', 'raw closing i tag'),
    (r'<span[>\s]', 'raw span tag'),
    (r'</span>', 'raw closing span tag'),
    (r'<div[>\s]', 'raw div tag'),
    (r'</div>', 'raw closing div tag'),
    (r'<br[>\s/]', 'raw br tag'),
    (r'<ul[>\s]', 'raw ul tag'),
    (r'<ol[>\s]', 'raw ol tag'),
    (r'<li[>\s]', 'raw li tag'),
    (r'<table[>\s]', 'raw table tag'),
    (r'<a\s', 'raw a tag'),
]

lines = content.split('\n')

for i, line in enumerate(lines, 1):
    # Only check template literal content (between backtick-delimited strings)
    for pattern, desc in html_patterns:
        if re.search(pattern, line):
            # Check if this is inside a code block (```html, ```xml, etc.)
            # Simple heuristic: if the line is preceded by ``` within 20 lines, it might be a code block
            # But let's check if it's on a line that also contains escaped or code markers
            if '```' not in line and not line.strip().startswith('\\`'):
                # Check surrounding context for code block markers
                start = max(0, i-20)
                context = lines[start:i]
                in_code_block = False
                code_block_count = 0
                for cl in context:
                    if cl.strip().startswith('```'):
                        code_block_count += 1
                if code_block_count % 2 == 0:  # Even number of ``` means we're NOT in a code block
                    issues.append(f"LINE {i}: {desc} found -> {line.strip()[:120]}")

# 2. Check heading format - headings must have space after ## or ###
for i, line in enumerate(lines, 1):
    stripped = line.strip()
    if stripped.startswith('##') or stripped.startswith('###'):
        # Must be exactly `## ` or `### `
        if stripped == '##' or stripped == '###':
            issues.append(f"LINE {i}: Empty heading -> '{stripped}'")
        elif not stripped.startswith('## ') and not stripped.startswith('### '):
            issues.append(f"LINE {i}: Malformed heading (no space after ##/###) -> '{stripped[:80]}'")
        # Check for extra space
        if '  ' in stripped[:5]:
            issues.append(f"LINE {i}: Double space after heading markers -> '{stripped[:80]}'")

# 3. Check for headings without blank line separation before them
# A heading should be preceded by a blank line (unless it's at the start of content)
for i, line in enumerate(lines, 1):
    stripped = line.strip()
    if (stripped.startswith('## ') or stripped.startswith('### ')) and i >= 2:
        prev_line = lines[i-2].strip()
        if prev_line and not prev_line.startswith('##') and not prev_line.startswith('```') and not prev_line.startswith('//'):
            # The line immediately before the heading (i-2, because lines are 0-indexed)
            # Actually let me check if i-1 (the line before) is empty
            line_before = lines[i-2].strip()
            if line_before and not line_before.startswith('##') and not line_before.startswith('###'):
                # Check if there's a blank line between them
                # lines[i-2] is the previous content line, lines[i-1] should be blank
                # But sometimes the previous line IS the blank line after content
                # Let me check more carefully
                prev_idx = i - 2
                while prev_idx >= 0 and not lines[prev_idx].strip():
                    prev_idx -= 1
                if prev_idx >= 0:
                    # prev_idx is the last non-empty line before the heading
                    # Check if there's exactly one blank line between them
                    blank_count = 0
                    for j in range(prev_idx + 1, i - 1):
                        if not lines[j].strip():
                            blank_count += 1
                    if blank_count == 0 and prev_idx != i - 2:
                        # No blank line between content and heading
                        issues.append(f"LINE {i}: Heading not preceded by blank line -> '{stripped[:80]}'")

print(f"Total lines: {len(lines)}")
print(f"Issues found: {len(issues)}")
for issue in issues:
    print(f"  {issue}")
