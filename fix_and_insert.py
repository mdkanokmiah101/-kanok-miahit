import re

with open('src/app/blog/data.js', 'r') as f:
    content = f.read()

# Find all positions of "`,\n  },"
positions = []
start = 0
pattern = "`,\n  },"
while True:
    idx = content.find(pattern, start)
    if idx == -1:
        break
    positions.append(idx)
    start = idx + 1

print("Found " + str(len(positions)) + " occurrences of pattern")
if positions:
    print("Last occurrence at position: " + str(positions[-1]))

# Check for proper ending
idx_end = content.find("`,\n  }\n];\n\nexport default posts;")
print("Proper ending found at: " + str(idx_end))

# Check what's after the last valid closing
if positions:
    last_idx = positions[-1]
    print("\nContent after last valid closing (first 500 chars):")
    print(repr(content[last_idx:last_idx+500]))
