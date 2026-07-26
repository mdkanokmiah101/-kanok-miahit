#!/usr/bin/env python3
"""Map git diff hunks to post slugs in data.js."""
import re
import subprocess

# Get the diff with context
result = subprocess.run(
    ["git", "diff", "HEAD~3..HEAD", "--", "src/app/blog/data.js"],
    capture_output=True, text=True, cwd="/root/kanok-miahit"
)
diff = result.stdout

# Read current data.js
with open("/root/kanok-miahit/src/app/blog/data.js") as f:
    content = f.read()

# Find all slug positions (line numbers)
slug_positions = []
for m in re.finditer(r'slug: "([^"]+)"', content):
    line_num = content[:m.start()].count('\n') + 1
    slug_positions.append((line_num, m.group(1)))

# Parse diff hunks to find which lines were changed
# Each hunk looks like @@ -old_start,old_count +new_start,new_count @@
changed_lines_new = set()
for m in re.finditer(r'@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@', diff):
    new_start = int(m.group(1))
    new_count = int(m.group(2)) if m.group(2) else 1
    for i in range(new_start, new_start + new_count):
        changed_lines_new.add(i)

# Map changed lines to post slugs
affected_posts = set()
for i, (line_num, slug) in enumerate(slug_positions):
    # A post covers from its slug line to the next slug line (or end)
    next_slug_line = slug_positions[i+1][0] if i+1 < len(slug_positions) else len(content.split('\n')) + 1
    for changed_line in changed_lines_new:
        if line_num <= changed_line < next_slug_line:
            affected_posts.add(slug)
            break

print("Changed post slugs:")
for slug in sorted(affected_posts):
    print(slug)

print(f"\nTotal: {len(affected_posts)} posts changed")
