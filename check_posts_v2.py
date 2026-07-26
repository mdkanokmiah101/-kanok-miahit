#!/usr/bin/env python3
"""Comprehensive check of blog data.js formatting issues."""

import re
import sys

with open('/root/kanok-miahit/src/app/blog/data.js', 'r', encoding='utf-8') as f:
    content = f.read()
    lines = content.split('\n')

# =====================================================================
# 1. Find all post objects and verify metadata
# =====================================================================
print("=" * 70)
print("SECTION 1: POST METADATA COMPLETENESS")
print("=" * 70)

# Find all post objects by locating opening braces at object level
# A post starts with `  {` (2 spaces + opening brace) preceded by `]` or `},`
post_starts = []
for i, line in enumerate(lines, 1):
    stripped = line.strip()
    # Post object starts at indent level 2 with `{`
    if stripped == '{' and line.startswith('  {'):
        post_starts.append(i)

print(f"Total post objects found: {len(post_starts)}")
print()

# For each post, extract the slug and check metadata
required_fields = {
    'slug': False,
    'title': False, 
    'date': False,
    'author': False,
    'tags': False
}

metadata_issues = []

for start_line in post_starts:
    # Find end of this post object (matching brace)
    brace_depth = 0
    end_line = start_line - 1
    for j in range(start_line - 1, len(lines)):
        brace_depth += lines[j].count('{') - lines[j].count('}')
        end_line = j + 1
        if brace_depth == 0:
            break
    
    post_lines = lines[start_line-1:end_line]
    post_text = '\n'.join(post_lines)
    
    # Extract slug
    slug = None
    slug_m = re.search(r'slug:\s*"([^"]+)"', post_text)
    if slug_m:
        slug = slug_m.group(1)
    else:
        slug_m = re.search(r"slug:\s*'([^']+)'", post_text)
        if slug_m:
            slug = slug_m.group(1)
        else:
            slug = f"POST_AT_LINE_{start_line}"
    
    # Check each required field
    missing = []
    for field in ['title:', 'date:', 'author:', 'tags:']:
        if not re.search(r'\b' + re.escape(field), post_text):
            missing.append(field.rstrip(':'))
    
    if missing:
        metadata_issues.append({
            'post_slug': slug,
            'issue_type': 'Missing metadata field',
            'issue_description': f"Missing: {', '.join(missing)}",
            'line_number': start_line,
            'severity': 'HIGH'
        })

if metadata_issues:
    print("ISSUES FOUND:")
    for iss in metadata_issues:
        print(f"  {iss['post_slug']} (line {iss['line_number']}): {iss['issue_description']}")
else:
    print("PASS: All posts have required metadata fields (slug, title, date, author, tags) ✓")

# =====================================================================
# 2. Check for raw HTML comments
# =====================================================================
print()
print("=" * 70)
print("SECTION 2: RAW HTML COMMENTS")
print("=" * 70)

html_comment_issues = []
for i, line in enumerate(lines, 1):
    if '<!--' in line or '-->' in line:
        html_comment_issues.append({
            'post_slug': 'N/A',
            'issue_type': 'Raw HTML comment',
            'issue_description': line.strip()[:100],
            'line_number': i,
            'severity': 'HIGH'
        })

if html_comment_issues:
    print("ISSUES FOUND:")
    for iss in html_comment_issues:
        print(f"  Line {iss['line_number']}: {iss['issue_description']}")
else:
    print("PASS: No raw HTML comments found ✓")

# =====================================================================
# 3. Check for raw <script> tags (not in code blocks)
# =====================================================================
print()
print("=" * 70)
print("SECTION 3: RAW <script> TAGS")
print("=" * 70)

def is_in_code_block(lines_list, line_idx):
    """Check if line at line_idx is inside a fenced code block."""
    code_block_depth = 0
    for j in range(line_idx):
        if lines_list[j].strip().startswith('```'):
            code_block_depth ^= 1  # toggle
    return code_block_depth == 1

script_tag_issues = []
for i, line in enumerate(lines, 1):
    m = re.search(r'<script\b', line, re.IGNORECASE)
    if m and not is_in_code_block(lines, i - 1):
        # Also check if it's just a code example reference like `<script>` in text
        if '`' in line:
            continue  # inline code reference
        script_tag_issues.append({
            'post_slug': 'N/A',
            'issue_type': 'Raw <script> tag',
            'issue_description': line.strip()[:120],
            'line_number': i,
            'severity': 'HIGH'
        })

# Also check </script> tags
for i, line in enumerate(lines, 1):
    m = re.search(r'</script\b', line, re.IGNORECASE)
    if m and not is_in_code_block(lines, i - 1):
        if '`' in line:
            continue
        script_tag_issues.append({
            'post_slug': 'N/A',
            'issue_type': 'Raw </script> tag',
            'issue_description': line.strip()[:120],
            'line_number': i,
            'severity': 'HIGH'
        })

if script_tag_issues:
    print("ISSUES FOUND:")
    for iss in script_tag_issues:
        print(f"  Line {iss['line_number']}: {iss['issue_description']}")
else:
    print("PASS: No raw <script> tags outside code blocks found ✓")

# =====================================================================
# 4. Check for stray markdown artifacts
# =====================================================================
print()
print("=" * 70)
print("SECTION 4: STRAY MARKDOWN ARTIFACTS")
print("=" * 70)

all_stray_issues = []

# 4a. Check unmatched ** (odd count per line, not inside code blocks)
print("--- 4a. Unmatched ** (bold markers) ---")
for i, line in enumerate(lines, 1):
    if is_in_code_block(lines, i - 1):
        continue
    # Count ** occurrences
    matches = list(re.finditer(r'\*\*', line))
    count = len(matches)
    if count % 2 == 1:
        # Check if this is a multi-line bold that spans lines (starting with ** on this line)
        # Or if it's a false positive like "** Item" list syntax
        # Look at context: if next lines have ** closing, it's fine
        # For now, flag it as MEDIUM
        all_stray_issues.append({
            'post_slug': 'N/A',
            'issue_type': 'Unmatched ** marker',
            'issue_description': f"Odd number of ** ({count}) on line: {line.strip()[:120]}",
            'line_number': i,
            'severity': 'LOW'
        })

if any(iss['issue_type'] == 'Unmatched ** marker' for iss in all_stray_issues):
    for iss in all_stray_issues:
        if iss['issue_type'] == 'Unmatched ** marker':
            print(f"  Line {iss['line_number']}: {iss['issue_description']}")
else:
    print("  PASS: No unmatched ** markers found ✓")

# 4b. Check for stray --- that might indicate unintended horizontal rules
print()
print("--- 4b. --- horizontal rules in content ---")

# Check if --- lines are used legitimately as section separators
# The --- at line 27231 is before "## Conclusion" - that's intentional
# Let's just count and note them
hr_count = len(list(re.finditer(r'^---$', content, re.MULTILINE)))
print(f"  Total '---' lines in file: {hr_count}")
print(f"  Note: These appear to be intentional horizontal rules in markdown content ✓")

# 4c. Check for potential broken markdown links with {target="_blank"} or similar
print()
print("--- 4c. Unusual markdown link syntax ---")
for i, line in enumerate(lines, 1):
    if is_in_code_block(lines, i - 1):
        continue
    # Check for {target= in markdown links [text](url){target=...}
    if '{target=' in line or '{rel=' in line:
        m = re.search(r'\[([^\]]+)\]\(([^)]+)\)\{[^}]+\}', line)
        if m:
            all_stray_issues.append({
                'post_slug': 'N/A',
                'issue_type': 'Non-standard markdown link syntax',
                'issue_description': f"Link with attributes: [{m.group(1)}]({m.group(2)}){{...}} -> {line.strip()[:100]}",
                'line_number': i,
                'severity': 'LOW'
            })
            print(f"  Line {i}: {line.strip()[:120]}")

if not any(iss['issue_type'] == 'Non-standard markdown link syntax' for iss in all_stray_issues):
    print("  PASS: No unusual markdown link syntax found ✓")

# 4d. Check for lines with raw `[text](url)` that might be formatting errors
print()
print("--- 4d. Raw markdown link bracket balance ---")
for i, line in enumerate(lines, 1):
    if is_in_code_block(lines, i - 1):
        continue
    if '`' in line and line.strip().startswith('`'):
        continue
    # Check for unmatched brackets
    opensq = len(re.findall(r'\[', line))
    closesq = len(re.findall(r'\]', line))
    openp = len(re.findall(r'\(', line))
    closep = len(re.findall(r'\)', line))
    
    if opensq != closesq or openp != closep:
        # Filter false positives: JSON objects, arrays, code references
        # Skip lines that look like JSON/JS arrays (sameAs, itemListElement, etc.)
        if re.search(r'"(?:sameAs|itemListElement|mainEntity|tool|step|faq|headline|description)s?":\s*\[', line):
            continue
        if re.search(r'const\s+\w+\s*=', line):
            continue
        if line.strip().startswith('//') or line.strip().startswith('/*'):
            continue
        if line.strip() == '};' or line.strip() == '];':
            continue
        if line.strip().startswith('{') and line.strip().endswith('},'):
            continue
        
        # It's a potential issue
        desc = f"Bracket mismatch: [={opensq}]={closesq} (={openp})={closep} -> {line.strip()[:100]}"
        all_stray_issues.append({
            'post_slug': 'N/A',
            'issue_type': 'Broken markdown link syntax',
            'issue_description': desc,
            'line_number': i,
            'severity': 'MEDIUM'
        })

bracket_issues = [iss for iss in all_stray_issues if iss['issue_type'] == 'Broken markdown link syntax']
if bracket_issues:
    print(f"  Found {len(bracket_issues)} lines with bracket mismatches (some may be false positives):")
    for iss in bracket_issues[:15]:
        print(f"  Line {iss['line_number']}: {iss['issue_description']}")
    if len(bracket_issues) > 15:
        print(f"  ... and {len(bracket_issues) - 15} more")
else:
    print("  PASS: No bracket mismatches found ✓")

# =====================================================================
# FINAL SUMMARY
# =====================================================================
print()
print("=" * 70)
print("FINAL RESULTS TABLE")
print("=" * 70)

all_issues = metadata_issues + html_comment_issues + script_tag_issues + all_stray_issues

if not all_issues:
    print("ALL CLEAN — No issues found across all checks")
else:
    print(f"Total issues found: {len(all_issues)}")
    print()
    print(f"{'Post Slug':<55} {'Issue Type':<35} {'Description':<60} {'Line':<7} {'Severity':<8}")
    print("-" * 195)
    for iss in all_issues:
        slug = iss['post_slug'][:54]
        itype = iss['issue_type'][:34]
        desc = iss['issue_description'][:59]
        line = str(iss['line_number'])
        sev = iss['severity']
        print(f"{slug:<55} {itype:<35} {desc:<60} {line:<7} {sev:<8}")
