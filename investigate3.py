#!/usr/bin/env python3
import subprocess, re

slug = "complete-seo-guide-bangladesh-businesses-2026"
url = f"https://kanokmiah.com.bd/blog/{slug}"

result = subprocess.run(["curl", "-sL", url, "--max-time", "15"], capture_output=True, text=True, timeout=20)
html = result.stdout

# Find actual <table> tags
tables = re.findall(r'<table.*?</table>', html, re.DOTALL | re.IGNORECASE)
print(f"Proper HTML <table> elements: {len(tables)}")
for i, t in enumerate(tables):
    print(f"  Table #{i+1}: {t[:200]}...")

# Find raw markdown table content in the HTML source (outside of scripts)
clean = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
clean = re.sub(r'<style[^>]*>.*?</style>', '', clean, flags=re.DOTALL | re.IGNORECASE)
# Look for pipe tables
pipe_tables = re.findall(r'\|[-]+\|[-]+\|', clean)
print(f"\nPipe table separator rows in non-script HTML: {len(pipe_tables)}")
for pt in pipe_tables:
    print(f"  -> '{pt}'")

# Also look for any raw markdown table rows
raw_rows = re.findall(r'<p>\|.*?\|</p>', clean)
print(f"\nRaw pipe tables inside <p> tags: {len(raw_rows)}")
for rr in raw_rows:
    print(f"  -> {rr}")

# Check if table is inside a <pre> or <code> block
pre_blocks = re.findall(r'<pre[^>]*>.*?</pre>', clean, re.DOTALL | re.IGNORECASE)
code_blocks = re.findall(r'<code[^>]*>.*?</code>', clean, re.DOTALL | re.IGNORECASE)
print(f"\n<pre> blocks: {len(pre_blocks)}")
print(f"<code> blocks: {len(code_blocks)}")
for pb in pre_blocks:
    if '---' in pb or '|' in pb:
        print(f"  PRE with table: {pb[:200]}")
for cb in code_blocks:
    if '---' in cb or '|' in cb:
        print(f"  CODE with table: {cb[:200]}")

# Search for the exact text around the table in the raw HTML
idx = clean.find('|----------|----------|-----------------|--------|----------|')
if idx >= 0:
    print(f"\nFound raw table at position {idx}")
    print(f"Context (200 chars before/after):")
    print(f"  BEFORE: {clean[max(0,idx-200):idx]}")
    print(f"  AFTER:  {clean[idx:idx+200]}")
