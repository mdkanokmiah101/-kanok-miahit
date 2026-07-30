#!/usr/bin/env python3
"""Extract changed post slugs from git diff."""
import subprocess
import re

# Read current data.js
with open("src/app/blog/data.js") as f:
    lines = f.readlines()

# Build slug -> line number mapping
slug_lines = {}
for i, line in enumerate(lines, 1):
    m = re.search(r'^\s*slug:\s*"([^"]+)"', line)
    if m:
        slug_lines[i] = m.group(1)

slug_positions = sorted(slug_lines.items())  # (line_num, slug)

def get_slug_for_line(target_line):
    """Find which slug is closest above a given line number."""
    best_slug = None
    for ln, slug in slug_positions:
        if ln <= target_line:
            best_slug = slug
        else:
            break
    return best_slug

def get_changed_slugs_from_diff(diff_text):
    changed = set()
    # Match @@ -old_start,old_count +new_start,new_count @@
    hunk_re = re.compile(r'@@\s+-(\d+)(?:,\d+)?\s+\+(\d+)(?:,\d+)?\s+@@')
    
    for line in diff_text.split('\n'):
        m = hunk_re.search(line)
        if m:
            start_line = int(m.group(2))  # Use new file start line
            slug = get_slug_for_line(start_line)
            if slug:
                changed.add(slug)
    return changed

# Get diff for c00ba6e
diff1 = subprocess.run(
    ["git", "diff", "--unified=0", "c00ba6e^", "c00ba6e", "--", "src/app/blog/data.js"],
    capture_output=True, text=True
).stdout

# Get diff for 089949f
diff2 = subprocess.run(
    ["git", "diff", "--unified=0", "089949f^", "089949f", "--", "src/app/blog/data.js"],
    capture_output=True, text=True
).stdout

changed1 = get_changed_slugs_from_diff(diff1)
changed2 = get_changed_slugs_from_diff(diff2)

all_changed = changed1 | changed2
print("Changed slugs from c00ba6e:", sorted(changed1))
print("Changed slugs from 089949f:", sorted(changed2))
print("All changed:", sorted(all_changed))
