#!/usr/bin/env python3
"""Comprehensive audit of heading structure in blog data."""
import re

with open("/root/kanok-miahit/src/app/blog/data.js", "r", encoding="utf-8") as f:
    lines = f.readlines()

# 1. Collect all heading lines with line numbers
headings = []  # (line_number, level, text, is_in_code_block)
in_code_block = False
in_template_literal = False
template_literal_count = 0

for i, line in enumerate(lines):
    stripped = line.strip()
    
    # Track code blocks
    if stripped.startswith('```'):
        in_code_block = not in_code_block
    
    # Track template literal start/end
    if stripped == 'content: `':
        in_template_literal = True
        template_literal_count += 1
    elif in_template_literal and stripped == '`,' or stripped == '`':
        in_template_literal = False
    
    # Find headings
    m = re.match(r'^(#{2,3})\s+(.+)$', stripped)
    if m and not in_code_block:
        level = len(m.group(1))
        text = m.group(2)
        headings.append((i+1, level, text, stripped.startswith('## ')))

# Check heading structure issues
issues = []

# Issue 1: Check blank line before heading (only in template literal content areas, not at start of content)
for idx, (line_num, level, text, is_h2) in enumerate(headings):
    i = line_num - 1  # 0-indexed
    if i > 0 and i < len(lines):
        prev_line = lines[i-1].strip()
        # Skip if previous line is empty (blank line present)
        if not prev_line:
            continue
        # Skip if previous line is start of template literal `content: \``
        if prev_line == 'content: `':
            continue
        # Skip if previous line is a code fence
        if prev_line.startswith('```'):
            continue
        # Also check if we're 1 line after content: ` (which would mean there IS a blank line)
        if i >= 2 and lines[i-2].strip() == 'content: `':
            continue
        
        # This is a real issue - heading without preceding blank line
        ctx_start = max(0, i-3)
        ctx_end = min(len(lines), i+1)
        context_lines = []
        for k in range(ctx_start, ctx_end):
            marker = ">>>" if k == i else "   "
            context_lines.append(f"      {marker} L{k+1}: {lines[k].rstrip()[:100]}")
        context_str = "\n".join(context_lines)
        
        issues.append({
            'line': line_num,
            'type': 'missing_blank_line',
            'text': text,
            'context': context_str
        })

# Issue 2: Check for broken heading order
# H2 -> H3 -> H2 is fine (back to parent). H2 -> H2 is fine (new section).
# H3 -> H2 is fine (back to parent). H3 -> H3 with no H2 in between - fine for subsections.
# Actually the main concern is h2 -> h4 without h3 in between, but we only have h2/h3

# Issue 3: Check for any <!-- comment tags or other markdown issues near headings
for line_num, level, text, is_h2 in headings:
    if '<' in text and '>' in text:
        issues.append({
            'line': line_num,
            'type': 'html_in_heading',
            'text': text
        })
    # Check double spaces in heading text
    if '  ' in text:
        issues.append({
            'line': line_num,
            'type': 'double_spaces_in_heading',
            'text': text
        })
    # Check trailing spaces
    i = line_num - 1
    if i < len(lines) and lines[i].rstrip() != lines[i].strip():
        issues.append({
            'line': line_num,
            'type': 'trailing_whitespace',
            'text': text
        })

# Issue 4: Check for empty lines with just spaces (might cause issues)
for i, line in enumerate(lines):
    stripped = line.strip()
    if stripped == '' and line.strip('\n') != '' and line != '\n':
        issues.append({
            'line': i+1,
            'type': 'line_with_whitespace',
            'text': repr(line)
        })

print(f"Total headings: {len(headings)}")
print(f"Total issues: {len(issues)}")
print()

# Group by type
by_type = {}
for issue in issues:
    by_type.setdefault(issue['type'], []).append(issue)

for issue_type, items in sorted(by_type.items()):
    print(f"\n{'='*60}")
    print(f"Issue type: {issue_type} ({len(items)} occurrences)")
    print(f"{'='*60}")
    for item in items[:15]:
        print(f"\n  Line {item['line']}: {item.get('text','')}")
        if 'context' in item:
            print(item['context'])
    if len(items) > 15:
        print(f"  ... and {len(items)-15} more")
