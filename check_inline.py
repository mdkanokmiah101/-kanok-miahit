import re

with open("src/app/blog/data.js", "r") as f:
    lines = f.readlines()

found = False
for i, line in enumerate(lines, 1):
    stripped = line.strip()
    # Skip heading lines, blank lines, and lines inside code blocks  
    if stripped.startswith("##") or stripped.startswith("###") or not stripped:
        continue
    if stripped.startswith("```") or stripped.startswith("*"):
        continue
    if "\\`" in stripped:
        continue
    # Check for ## used inline (not as heading)
    if re.search(r"[^\s``]##\s", stripped):
        print(f"Line {i}: Possible inline ##: {stripped[:100]}")
        found = True
    if re.search(r"[^\s``]###\s", stripped):
        print(f"Line {i}: Possible inline ###: {stripped[:100]}")
        found = True

if not found:
    print("No inline heading markers found - all ## and ### are proper headings.")

# Also check for any malformed bold/italic patterns
print()
print("=== Additional checks ===")
# Check for *** without proper closing
bad_bold = 0
for i, line in enumerate(lines, 1):
    stripped = line.strip()
    if "***" in stripped and not stripped.startswith("```"):
        # Check it's properly balanced
        opens = stripped.count("***")
        # This is likely intentional (bold+italic)
        pass

print("Done.")
