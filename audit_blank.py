#!/usr/bin/env python3
"""Verify blank lines before all headings in the blog data."""
import re

with open("/root/kanok-miahit/src/app/blog/data.js", "r", encoding="utf-8") as f:
    lines = f.readlines()

issues = []
total_h2 = 0
total_h3 = 0
missing_blank = 0

for i, line in enumerate(lines):
    stripped = line.strip()
    if stripped.startswith('## ') or stripped.startswith('### '):
        total_h2 += stripped.startswith('## ')
        total_h3 += stripped.startswith('### ')
        # Check: the previous line should be blank
        # lines[i-1] if i > 0
        if i > 0:
            prev_line = lines[i-1].strip()
            if prev_line and not prev_line.startswith('`') and not prev_line.startswith('//'):
                # The line before heading has content (not blank, not code fence, not comment)
                # Check if we're inside a code block by counting ```
                code_block_depth = 0
                for j in range(max(0, i-30), i):
                    if lines[j].strip().startswith('```'):
                        code_block_depth += 1
                if code_block_depth % 2 == 0:
                    missing_blank += 1
                    if missing_blank <= 20:
                        # Show context
                        ctx_start = max(0, i-3)
                        ctx_end = min(len(lines), i+1)
                        context_lines = []
                        for k in range(ctx_start, ctx_end):
                            marker = ">>>" if k == i else "   "
                            context_lines.append(f"      {marker} L{k+1}: {lines[k].rstrip()}")
                        context_str = "\n".join(context_lines)
                        issues.append(f"LINE {i+1}: Heading not preceded by blank line. Context:\n{context_str}")

print(f"Total H2 headings: {total_h2}")
print(f"Total H3 headings: {total_h3}")
print(f"Missing blank line before heading: {missing_blank}")
print("\nSample issues (up to 20):")
for issue in issues[:20]:
    print(f"\n{issue}")
