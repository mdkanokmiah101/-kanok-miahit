import re

with open('/root/kanok-miahit/src/app/blog/data.js', 'r') as f:
    content = f.read()

# Find template literal content blocks (content: `...` )
# These are the blog post contents
# We need to find all the `content:` template literals

# Simple approach: split by content: and find the template literal
# Actually let me just look for HTML tags in the entire file, but skip lines inside ``` blocks

lines = content.split('\n')
in_code_block = False
in_template_literal = False  # We're inside a `template literal` (the blog content)
issues = []

for i, line in enumerate(lines, 1):
    stripped = line.strip()
    
    # Track code blocks
    if stripped.startswith('```'):
        in_code_block = not in_code_block
        continue
    
    # Skip lines that aren't inside a template literal (the blog content values)
    # Template literals start after content: `
    # We can detect them by looking for lines that are indented (part of an object)
    # Let's just search for actual heading-level HTML tags
    
    if in_code_block:
        continue
    
    # Look for specific problematic HTML tags
    # <h2>, <h3>, <p>, <strong>, <em>, <b>, <i> — these should not be in markdown content
    for pattern in [r'<(/?)(h[2-6])(\s[^>]*)?\s*/?>', 
                    r'<(/?)(p)(\s[^>]*)?>',
                    r'<(/?)(strong)(\s[^>]*)?>',
                    r'<(/?)(em)(\s[^>]*)?>',
                    r'<(/?)(b)(\s[^>]*)?>',
                    r'<(/?)(i)(\s[^>]*)?>',
                    r'<(/?)(span)(\s[^>]*)?>',
                    r'<(/?)(div)(\s[^>]*)?>',
                    r'<(/?)(section)(\s[^>]*)?>',
                    r'<(/?)(br)\s*/?>',
                    r'<(/?)(ul)(\s[^>]*)?>',
                    r'<(/?)(ol)(\s[^>]*)?>',
                    r'<(/?)(li)(\s[^>]*)?>']:
        matches = re.findall(pattern, stripped, re.IGNORECASE)
        if matches:
            issues.append((i, stripped[:150], matches))

if issues:
    print(f"Found {len(issues)} potential issues:")
    for line_no, content_line, tags in issues:
        print(f"  Line {line_no}: {content_line}")
        for t in tags:
            print(f"    -> <{t[0]}{t[1]}{t[2]}>")
else:
    print("No raw HTML tags found outside code blocks.")

# Now check all headings in template literals
print("\n\nChecking heading structures...")
# Find all ## and ### headings
heading_issues = []
for i, line in enumerate(lines, 1):
    stripped = line.strip()
    # Check for non-standard heading formats
    if re.match(r'^##[^# \t]', stripped):
        heading_issues.append((i, f"No space after ##: {stripped[:80]}"))
    if re.match(r'^###[^# \t]', stripped):
        heading_issues.append((i, f"No space after ###: {stripped[:80]}"))
    # Check for headings without blank line before them (broken structure)
    # This would require checking prev line

if heading_issues:
    print("Heading formatting issues:")
    for ln, msg in heading_issues:
        print(f"  Line {ln}: {msg}")
else:
    print("All headings have proper spacing after ##/### markers.")

# Also check for ###### headings (too deep)
for i, line in enumerate(lines, 1):
    stripped = line.strip()
    if re.match(r'^####\s', stripped):
        print(f"  Line {i}: Possible heading depth issue (####): {stripped[:80]}")

# Check for headings that look like heading tags <h2> etc
for i, line in enumerate(lines, 1):
    stripped = line.strip()
    if re.match(r'^\s*<h[2-6][^>]*>', stripped, re.IGNORECASE):
        print(f"  Line {i}: Raw HTML heading tag: {stripped[:80]}")
