#!/usr/bin/env python3
"""Extract slugs of posts changed in last 48 hours from git log."""
import subprocess
import re
import os

os.chdir("/root/kanok-miahit")

# Get the diff for data.js in the most recent commits (last 48h)
result = subprocess.run(
    ["git", "log", "--oneline", "--since=48 hours ago", "--", "src/app/blog/data.js"],
    capture_output=True, text=True
)
commits = result.stdout.strip().split("\n")
commits = [c.split()[0] for c in commits if c.strip()]

if not commits:
    print("NO_CHANGES")
    exit(0)

print(f"Found commits: {commits}")

# Get the full diff from all these commits combined
# Let's check each commit's diff
all_changed_slugs = set()

for commit in commits:
    # Get the parent
    parent = f"{commit}^"
    # Check if parent exists
    r = subprocess.run(["git", "rev-parse", "--verify", parent], capture_output=True, text=True)
    if r.returncode != 0:
        continue
    
    # Get the diff and find which posts were modified
    diff = subprocess.run(
        ["git", "diff", parent, commit, "--", "src/app/blog/data.js"],
        capture_output=True, text=True
    )
    
    if not diff.stdout.strip():
        continue
    
    # Find the post slugs that contain the changed lines
    # Read the current version of data.js
    with open("src/app/blog/data.js") as f:
        content = f.read()
    
    # Parse all post slugs and their line ranges
    posts = []
    # Match: slug: "something",
    pattern = re.compile(r'\bslug:\s*"([^"]+)"')
    
    # Also find all added/removed line numbers
    # Parse diff hunks to get line numbers
    hunk_re = re.compile(r'@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@')
    
    # Read the file with line numbers
    lines = content.split('\n')
    
    # Build a map of slug -> line number
    slug_lines = {}
    for i, line in enumerate(lines, 1):
        m = pattern.search(line)
        if m:
            slug_lines[i] = m.group(1)
    
    # For each chunk in the diff, determine which post it affects
    for hunk in diff.stdout.split('@@ '):
        if not hunk.strip():
            continue
        # Try to get the start line of the modified region
        lines_hunk = hunk.split('\n')
        if lines_hunk:
            first_line = lines_hunk[0]
            m = hunk_re.search('@@ ' + first_line if not first_line.startswith('@@') else first_line)
            if m:
                start_line = int(m.group(1))
                # Find which slug is closest above this line
                closest_slug = None
                closest_line = 0
                for ln, slug in sorted(slug_lines.items()):
                    if ln <= start_line and ln > closest_line:
                        closest_line = ln
                        closest_slug = slug
                if closest_slug:
                    all_changed_slugs.add(closest_slug)

changed = list(all_changed_slugs)
print(f"Changed slugs: {changed}")
