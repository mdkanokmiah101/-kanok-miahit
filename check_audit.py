import re

with open("src/app/blog/data.js", "r") as f:
    content = f.read()

lines = content.split("\n")

issues_found = False

# 1. Check all headings
print("=== Checking heading format ===")
for i, line in enumerate(lines, 1):
    stripped = line.strip()
    if re.match(r"^##[^#\s]", stripped):
        print(f"Line {i}: ## without space: {stripped[:80]}")
        issues_found = True
    if re.match(r"^###[^#\s]", stripped):
        print(f"Line {i}: ### without space: {stripped[:80]}")
        issues_found = True
    if re.match(r"^#{4,}\s", stripped):
        print(f"Line {i}: Too many hashes: {stripped[:80]}")
        issues_found = True

# 2. Check HTML tags in non-code-block content
print()
print("=== Checking raw HTML tags outside code blocks ===")
in_code = False
for i, line in enumerate(lines, 1):
    stripped = line.strip()
    if "```" in stripped or "\\`\\`\\`" in stripped:
        in_code = not in_code
        continue
    if in_code:
        continue
    # Check for problematic HTML tags
    for tag in ["h1", "h2", "h3", "h4", "h5", "h6", "p", "strong", "em", "b", "i"]:
        pattern = r"<" + tag + r"[^>]*>"
        if re.search(pattern, stripped):
            print(f"Line {i}: Found <{tag}> outside code block: {stripped[:100]}")
            issues_found = True

# 3. Check for empty headings
print()
print("=== Checking empty headings ===")
for i, line in enumerate(lines, 1):
    stripped = line.strip()
    if re.match(r"^#{2,3}\s*$", stripped):
        print(f"Line {i}: Empty heading")
        issues_found = True

if not issues_found:
    print("No issues found!")
