#!/usr/bin/env python3
"""Identify posts with substantive content changes vs just formatting."""
import re
import subprocess

result = subprocess.run(
    ["git", "diff", "HEAD~3..HEAD", "--", "src/app/blog/data.js"],
    capture_output=True, text=True, cwd="/root/kanok-miahit"
)
diff = result.stdout

# Find content changes (non-whitespace, non-markdown-formatting changes)
content_changes = set()
formatting_changes = set()

lines = diff.split('\n')
current_hunk_new_start = 0

for i, line in enumerate(lines):
    hunk_match = re.match(r'@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@', line)
    if hunk_match:
        current_hunk_new_start = int(hunk_match.group(1))
        continue
    
    if line.startswith('+') and not line.startswith('+++'):
        content = line[1:]
        # Check if this is just a blank line addition
        if content.strip() == '' or content.strip() == '+':
            continue
        # Check if it's a formatting fix
        if re.match(r'^\+## .+', content) or re.match(r'^\+[-*] ', content):
            # This is a heading or list item
            formatting_changes.add(current_hunk_new_start)
            continue
        # Check if it's a markdown bold fix
        if re.match(r'^\+.*\*\*\S+', content) and re.match(r'^-.*\*\*\S+', lines[i-1][1:] if i > 0 and lines[i-1].startswith('-') else ''):
            continue
        # It's a real content change
        content_changes.add(current_hunk_new_start)

print(f"Formatting-only hunks: {len(formatting_changes)}")
print(f"Content-change hunks: {len(content_changes)}")

# Let me check what the actual content changes are
in_hunk = False
current_hunk_start = 0
for i, line in enumerate(lines):
    hunk_match = re.match(r'@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@', line)
    if hunk_match:
        current_hunk_start = int(hunk_match.group(1))
        in_hunk = True
        continue
    
    if line.startswith('+') and not line.startswith('+++') and len(line) > 1:
        content = line[1:]
        if content.strip() and not content.strip().startswith('##') and not content.strip().startswith('-') and not content.strip().startswith('*'):
            # Check if the corresponding old line is significantly different
            if i > 0 and lines[i-1].startswith('-'):
                old = lines[i-1][1:]
                if old.strip() != content.strip():
                    print(f"Content change near line {current_hunk_start}:")
                    print(f"  -: {old[:100]}")
                    print(f"  +: {content[:100]}")
                    print()
