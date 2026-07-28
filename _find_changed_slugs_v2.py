#!/usr/bin/env python3
import subprocess
import re

# Get the full diff
result = subprocess.run(
    ["git", "diff", "c822841^..0cd493b", "--", "src/app/blog/data.js"],
    capture_output=True, text=True, cwd="/root/kanok-miahit"
)
diff = result.stdout

# Read current data.js
with open("/root/kanok-miahit/src/app/blog/data.js") as f:
    content = f.read()

# Build line->slug mapping
lines = content.split('\n')
line_to_slug = {}
current_slug = None
for i, line in enumerate(lines):
    m = re.search(r'slug:\s*"([^"]+)"', line)
    if m:
        current_slug = m.group(1)
    if current_slug:
        line_to_slug[i + 1] = current_slug  # 1-indexed

# Better: for each line, find the slug that's closest before it
def get_slug_for_line(line_num, slug_map):
    """Find slug for line by checking the nearest slug defined before this line."""
    best_slug = None
    best_line = 0
    for l, s in sorted(slug_map.items()):
        if l <= line_num and l > best_line:
            best_line = l
            best_slug = s
    return best_slug

# Parse hunks
hunk_re = re.compile(r'@@ -(\d+),(\d+) \+(\d+),(\d+) @@')
changed_slugs = set()
for line in diff.split('\n'):
    m = hunk_re.match(line)
    if m:
        new_start = int(m.group(3))
        changed_slugs.add(get_slug_for_line(new_start, line_to_slug))

print("Changed slugs:")
for s in sorted(changed_slugs):
    print(s)
print(f"\nTotal: {len(changed_slugs)}")

with open("/root/kanok-miahit/_changed_slugs_v2.txt", "w") as f:
    for s in sorted(changed_slugs):
        f.write(s + "\n")

# Also let's identify the exact changes per post
print("\n\n=== Detailed change info ===")
current_changed_slug = None
for line in diff.split('\n'):
    m = hunk_re.match(line)
    if m:
        new_start = int(m.group(3))
        current_changed_slug = get_slug_for_line(new_start, line_to_slug)
        print(f"\n--- Post: {current_changed_slug} (starts at new line {new_start}) ---")
    elif current_changed_slug and (line.startswith('+') or line.startswith('-')):
        if len(line) > 1:
            print(line)
