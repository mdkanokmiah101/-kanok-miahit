#!/usr/bin/env python3
import subprocess, re

slug = "complete-seo-guide-bangladesh-businesses-2026"
url = f"https://kanokmiah.com.bd/blog/{slug}"

result = subprocess.run(["curl", "-sL", url, "--max-time", "15"], capture_output=True, text=True, timeout=20)
html = result.stdout

# Remove scripts, styles, comments
clean = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
clean = re.sub(r'<style[^>]*>.*?</style>', '', clean, flags=re.DOTALL | re.IGNORECASE)
clean = re.sub(r'<!--.*?-->', '', clean, flags=re.DOTALL)
clean = re.sub(r'<svg[^>]*>.*?</svg>', '', clean, flags=re.DOTALL | re.IGNORECASE)

# Show context around each --- occurrence (with HTML stripped for visible text)
visible = re.sub(r'<[^>]+>', '\n', clean)

# Find all --- with context
matches = list(re.finditer(r'(?<![a-zA-Z0-9])---(?![a-zA-Z0-9])', visible))
print(f"Total '---' matches: {len(matches)}")
print()

for i, m in enumerate(matches):
    start = max(0, m.start() - 60)
    end = min(len(visible), m.end() + 60)
    ctx = visible[start:end].replace('\n', ' ↵ ')
    print(f"#{i+1}: ...{ctx}...")
    print()

# Also check FAQ mentions
print("=" * 80)
print("FAQ mentions in visible text:")
faqs = re.findall(r'(?i)(faq|frequently asked questions)', visible)
print(f"Count: {len(faqs)}")
print()

# Check if FAQ section content has any raw schema
faq_section_match = re.search(r'(?i)faq.*?(?:\n\n|\Z)', visible[:5000])
if faq_section_match:
    print("FAQ section snippet (first 500 chars):")
    print(faq_section_match.group()[:500])
