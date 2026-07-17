import re
import sys

with open('src/app/blog/data.js', 'r') as f:
    content = f.read()

lines = content.split('\n')
in_code_block = False
issues = []

for i, line in enumerate(lines, 1):
    stripped = line.strip()

    # Toggle code block detection
    if stripped.startswith('```') or stripped.startswith('`' * 3):
        in_code_block = not in_code_block
        continue

    if in_code_block:
        continue

    # Check for HTML heading/formatting tags NOT in code blocks
    html_tags = re.findall(r'<(/?)(h[1-6]|p|strong|em|b|i|u|br|ul|ol|li|div|span|a)\b', stripped)
    for _, tag in html_tags:
        issues.append(('html', i, f'Found HTML tag <{tag}>: {stripped[:120]}'))

    # Check heading format
    m = re.match(r'^(#+)\s', stripped)
    if m:
        hashes = m.group(1)
        if hashes not in ('##', '###'):
            issues.append(('heading', i, f'Non-standard heading format "{hashes}": {stripped[:120]}'))

    # Check for # with no space
    m2 = re.match(r'^#{2,3}[^#\s]', stripped)
    if m2:
        issues.append(('heading', i, f'No space after hashes: {stripped[:120]}'))

    # Check for empty heading (## followed by nothing or just whitespace)
    if re.match(r'^#{2,3}\s*$', stripped):
        issues.append(('heading', i, f'Empty heading found'))

    # Check for bold/italic markdown issues inside template content
    # Look for single asterisk bold (should be **)
    # This is harder to detect without false positives

if issues:
    print(f"Found {len(issues)} issue(s):")
    for typ, line_num, msg in issues:
        print(f"  [{typ.upper()}] Line {line_num}: {msg}")
else:
    print("No issues found - all headings use proper format, no raw HTML tags in content.")

# Also let's check the overall heading structure per post
# Extract post slugs and check each post's heading hierarchy
print("\n--- Checking heading hierarchy per post ---")
posts = content.split("slug:")
for idx, post in enumerate(posts[1:], 1):
    slug_match = re.search(r'"([^"]+)"', post.split(',')[0])
    slug = slug_match.group(1) if slug_match else f'unknown_{idx}'
    
    # Find all headings in this post (lines starting with ## or ###)
    post_lines = post.split('\n')
    prev_level = 1  # Start at H1 level expectation
    had_issue = False
    for pl in post_lines:
        pl_stripped = pl.strip()
        hm = re.match(r'^(#{2,3})\s', pl_stripped)
        if hm:
            level = len(hm.group(1))
            if level > prev_level + 1:
                print(f"  Post '{slug}': Heading jump from H{prev_level} to H{level} at: {pl_stripped[:80]}")
                had_issue = True
            prev_level = level
    
    if not had_issue:
        heading_count = len([l for l in post_lines if re.match(r'^#{2,3}\s', l.strip())])
        print(f"  Post '{slug}': OK ({heading_count} headings)")
