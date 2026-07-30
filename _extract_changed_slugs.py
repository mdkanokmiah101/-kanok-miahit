#!/usr/bin/env python3
"""Extract slugs of all blog posts modified in the last 48 hours."""
import re
import subprocess
import json

# Get the diff
result = subprocess.run(
    ["git", "diff", "HEAD~2", "HEAD", "--", "src/app/blog/data.js"],
    capture_output=True, text=True, cwd="/root/kanok-miahit"
)
diff = result.stdout

# Read the full data.js file
with open("/root/kanok-miahit/src/app/blog/data.js", "r") as f:
    content = f.read()

# Find all blog post entries and their start lines
# Pattern: slug: "something" preceded by {
posts = []
for m in re.finditer(r'\bslug:\s*"([^"]+)"', content):
    slug = m.group(1)
    pos = m.start()
    # Get the line number
    line_num = content[:pos].count('\n') + 1
    posts.append((slug, line_num, pos))

# Parse the diff to find which lines changed
# For each hunk, find the line numbers
changed_slugs = set()
for hunk in re.finditer(r'@@ -\d+,\d+ \+(\d+),\d+ @@', diff):
    start_line = int(hunk.group(1))
    # The hunk shows lines starting from this line number
    # Find which post(s) this range falls into
    for slug, line_num, pos in posts:
        # Check if this slug's position is near the changed lines
        # The slug line itself might be before the change
        # Let's find the end of this post entry
        slug_end = None
        after_slug = content[pos:]
        # Find the next "}," or "};" after this slug (within reasonable bounds)
        next_close = re.search(r'^\s*\},?\s*$', after_slug, re.MULTILINE)
        if next_close:
            slug_end = pos + next_close.end()
        
        # If the hunk start line is between the slug's line and the end of the post
        hunk_start_pos = None
        for i, ch in enumerate(content):
            if content[:i].count('\n') + 1 == start_line:
                hunk_start_pos = i
                break
        
        if hunk_start_pos and pos <= hunk_start_pos:
            if slug_end is None or hunk_start_pos <= slug_end:
                changed_slugs.add(slug)

# Also try alternative: get line numbers of changed lines
changed_lines = set()
for hunk in re.finditer(r'@@ -\d+,\d+ \+(\d+),\d+ @@', diff):
    hunk_start = int(hunk.group(1))
    # Parse the lines in the hunk to find which specific line numbers changed
    hunk_body_start = hunk.end()
    body = diff[hunk_body_start:].split('\n')
    line_no = hunk_start
    for line in body:
        if line.startswith('+') and not line.startswith('+++'):
            changed_lines.add(line_no)
        if line.startswith(' '):
            line_no += 1
        elif line.startswith('+'):
            line_no += 1
        # '-' lines don't advance line count

print(f"Changed lines: {sorted(changed_lines)}")

# Now map each changed line to the post slug
# For each changed line, find the nearest preceding slug
for line in sorted(changed_lines):
    # Find all slugs whose line number <= this line
    candidates = [(s, l) for s, l, p in posts if l <= line]
    if candidates:
        # Find the closest slug before this line
        candidates.sort(key=lambda x: x[1], reverse=True)
        changed_slugs.add(candidates[0][0])

print(f"\nChanged slugs ({len(changed_slugs)}):")
for s in sorted(changed_slugs):
    print(s)

with open("/root/kanok-miahit/_changed_slugs_v2.json", "w") as f:
    json.dump(sorted(changed_slugs), f, indent=2)
