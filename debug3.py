#!/usr/bin/env python3
"""Debug content extraction regex."""
import re

FILEPATH = "/root/kanok-miahit/src/app/blog/data.js"

with open(FILEPATH, "r", encoding="utf-8") as f:
    text = f.read()

slug = "seo-hreflang-guide-bangladesh"

idx = text.find(f'slug: "{slug}"')
block_start = text.rfind('{', max(0, idx - 20), idx)
block = text[block_start:]

m = re.search(r"`,\s*\n\s*\},\s*\n\s*\{\s*\n\s+slug:", block)
if m:
    block = block[:m.start()]

print(f"Block length: {len(block)}")

# Test the content regex step by step
# Find content: \x60
content_start = block.find("content:")
print(f"content: at pos {content_start}")
print(f"chars after content:: {repr(block[content_start:content_start+20])}")

# Now test just the regex
content_match = re.search(r'content:\s*`', block)
if content_match:
    print(f"Opening backtick found at {content_match.start()}, group: {repr(content_match.group())}")
    start_pos = content_match.end()
    
    # Now try to find the closing backtick
    # The closing is \x60 (backtick) followed by , or whitespace
    # Test: find the first backtick after content start that's not escaped
    rest = block[start_pos:]
    print(f"\nFirst 100 chars of rest: {repr(rest[:100])}")
    
    # Search for unescaped backtick
    # Pattern: find backtick that's preceded by an even number of backslashes (or no backslash)
    # Actually, in JS template literals, backticks inside are escaped as \`
    # So unescaped backtick is one not preceded by backslash
    close_m = re.search(r'(?<!\\)`', rest)
    if close_m:
        print(f"\nFirst unescaped backtick at pos {close_m.start()}")
        print(f"Context: ...{repr(rest[max(0,close_m.start()-20):close_m.start()+20])}...")
    else:
        print("No unescaped backtick found!")
        # Check if there are any backticks at all
        all_backticks = [i for i, c in enumerate(rest) if c == '`']
        print(f"All backtick positions (first 10): {all_backticks[:10]}")
        if all_backticks:
            for pos in all_backticks[:5]:
                before = rest[max(0,pos-3):pos]
                print(f"  pos {pos}: before={repr(before)}, char={repr(rest[pos])}")

print("\n\n--- Now testing with full regex ---")
# Build regex manually to debug
# Pattern: content:\s*`((?:[^`\\]|\\.)*)`
# In Python raw string: r'content:\s*`((?:[^`\\]|\\.)*)`'
pattern = r'content:\s*`((?:[^`\\]|\\.)*)`'
print(f"Pattern: {pattern}")

# Test on a small string first
test = 'content: `hello world`'
print(f"Test on '{test}': {re.search(pattern, test)}")

# Test with escaped backtick
test2 = 'content: `hello \\`world`'
print(f"Test on '{test2}': {re.search(pattern, test2)}")

# Now test on the block
m = re.search(pattern, block, re.DOTALL)
if m:
    content = m.group(1)
    print(f"Content length: {len(content)}")
    print(f"Last 100 chars: ...{repr(content[-100:])}")
    links = re.findall(r'href="(/[^"]*)"', content)
    print(f"Links: {links}")
else:
    print("Full regex FAILED on block!")
    # Try without DOTALL
    m2 = re.search(pattern, block)
    if m2:
        print("Without DOTALL it works?")
    else:
        print("Still fails without DOTALL")
