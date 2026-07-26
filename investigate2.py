#!/usr/bin/env python3
import subprocess, re

# Check the complete-seo-guide page for the table rendering issue
slug = "complete-seo-guide-bangladesh-businesses-2026"
url = f"https://kanokmiah.com.bd/blog/{slug}"

result = subprocess.run(["curl", "-sL", url, "--max-time", "15"], capture_output=True, text=True, timeout=20)
html = result.stdout

# Remove scripts, styles, comments
clean = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
clean = re.sub(r'<style[^>]*>.*?</style>', '', clean, flags=re.DOTALL | re.IGNORECASE)
clean = re.sub(r'<!--.*?-->', '', clean, flags=re.DOTALL)
clean = re.sub(r'<svg[^>]*>.*?</svg>', '', clean, flags=re.DOTALL | re.IGNORECASE)

visible = re.sub(r'<[^>]+>', '\n', clean)

# Find the table section
print("=== Looking for raw pipe tables in visible text ===")
table_lines = re.findall(r'.{0,40}\|.*?\|.{0,40}', visible)
for line in table_lines[:20]:
    print(f"  {line.strip()}")
print()

# Check all pages for pipe tables
print("=== Checking ALL pages for pipe tables ===")
for slug in [
    "complete-seo-guide-bangladesh-businesses-2026",
    "local-seo-tips-dhaka-businesses-google-maps",
    "why-ecommerce-store-needs-seo-bangladesh",
    "technical-seo-checklist-bangladeshi-websites",
    "how-to-choose-right-seo-agency-bangladesh",
]:
    url = f"https://kanokmiah.com.bd/blog/{slug}"
    r = subprocess.run(["curl", "-sL", url, "--max-time", "15"], capture_output=True, text=True, timeout=20)
    h = r.stdout
    c = re.sub(r'<script[^>]*>.*?</script>', '', h, flags=re.DOTALL | re.IGNORECASE)
    c = re.sub(r'<style[^>]*>.*?</style>', '', c, flags=re.DOTALL | re.IGNORECASE)
    c = re.sub(r'<!--.*?-->', '', c, flags=re.DOTALL)
    v = re.sub(r'<[^>]+>', '\n', c)
    pipes = re.findall(r'\|.*?\|', v)
    md_tables = [p for p in pipes if '---' in p or '|' in p]
    print(f"  {slug}: {len(md_tables)} raw pipe table fragments")
    
    # Also check for raw markdown table rows (lines starting with |)
    raw_table_rows = re.findall(r'^\|.*\|$', v, re.MULTILINE)
    if raw_table_rows:
        print(f"    Raw table rows found: {len(raw_table_rows)}")
        for tr in raw_table_rows[:5]:
            print(f"      -> {tr.strip()[:100]}")
    print()

print("=== Checking FAQ context ===")
for slug in [
    "complete-seo-guide-bangladesh-businesses-2026",
    "local-seo-tips-dhaka-businesses-google-maps",
    "why-ecommerce-store-needs-seo-bangladesh",
]:
    url = f"https://kanokmiah.com.bd/blog/{slug}"
    r = subprocess.run(["curl", "-sL", url, "--max-time", "15"], capture_output=True, text=True, timeout=20)
    v = re.sub(r'<script[^>]*>.*?</script>', '', r.stdout, flags=re.DOTALL | re.IGNORECASE)
    v = re.sub(r'<style[^>]*>.*?</style>', '', v, flags=re.DOTALL | re.IGNORECASE)
    v = re.sub(r'<!--.*?-->', '', v, flags=re.DOTALL)
    v = re.sub(r'<[^>]+>', '\n', v)
    
    # Find FAQ context
    faq_idx = v.lower().find('faq')
    if faq_idx >= 0:
        start = max(0, faq_idx - 100)
        end = min(len(v), faq_idx + 500)
        print(f"  {slug}:")
        print(f"    FAQ context: {v[start:end][:500]}")
        print()
