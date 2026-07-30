#!/usr/bin/env python3
"""Extract changed post slugs by parsing git diff hunks and mapping to slug line numbers."""
import subprocess
import re

# Run: git diff --unified=0 c00ba6e^..c00ba6e -- src/app/blog/data.js
diff = subprocess.run(
    ["git", "diff", "--unified=0", "c00ba6e^", "c00ba6e", "--", "src/app/blog/data.js"],
    capture_output=True, text=True
).stdout

# Also check the earlier commit
diff2 = subprocess.run(
    ["git", "diff", "--unified=0", "089949f^", "089949f", "--", "src/app/blog/data.js"],
    capture_output=True, text=True
).stdout

# Read current data.js
with open("src/app/blog/data.js") as f:
    lines = f.readlines()

# Build slug -> line number mapping
slug_lines = {}
for i, line in enumerate(lines, 1):
    m = re.search(r'slug:\s*"([^"]+)"', line)
    if m:
        slug_lines[i] = m.group(1)

# Also build reverse mapping: slug -> start/end lines
slug_positions = []
for ln in sorted(slug_lines.keys()):
    slug_positions.append((ln, slug_lines[ln]))

def get_slug_for_line(target_line, slug_positions):
    """Find which slug is closest above a given line number."""
    best_slug = None
    best_line = 0
    for ln, slug in slug_positions:
        if ln <= target_line and ln > best_line:
            best_line = ln
            best_slug = slug
    return best_slug

def get_changed_slugs_from_diff(diff_text):
    """Parse diff hunks and return set of changed slugs."""
    changed = set()
    hunk_re = re.compile(r'@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@')
    
    for hunk in diff_text.split('@@ '):
        if not hunk.strip():
            continue
        lines_hunk = hunk.split('\n')
        first_line_text = lines_hunk[0] if lines_hunk else ""
        m = hunk_re.search(first_line_text)
        if m:
            start_line = int(m.group(1))
            slug = get_slug_for_line(start_line, slug_positions)
            if slug:
                changed.add(slug)
    return changed

changed1 = get_changed_slugs_from_diff(diff)
changed2 = get_changed_slugs_from_diff(diff2)

all_changed = changed1 | changed2
print("Changed slugs from c00ba6e:", sorted(changed1))
print("Changed slugs from 089949f:", sorted(changed2))
print("All changed:", sorted(all_changed))
