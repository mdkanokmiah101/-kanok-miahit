#!/usr/bin/env python3
import subprocess, re

slugs = [
    "complete-seo-guide-bangladesh-businesses-2026",
    "local-seo-tips-dhaka-businesses-google-maps",
    "why-ecommerce-store-needs-seo-bangladesh",
    "technical-seo-checklist-bangladeshi-websites",
    "how-to-choose-right-seo-agency-bangladesh",
]

for slug in slugs:
    url = f"https://kanokmiah.com.bd/blog/{slug}"
    result = subprocess.run(["curl", "-sL", url, "--max-time", "15"], capture_output=True, text=True, timeout=20)
    html = result.stdout
    
    clean = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
    clean = re.sub(r'<style[^>]*>.*?</style>', '', clean, flags=re.DOTALL | re.IGNORECASE)
    
    print(f"\n========== {slug} ==========")
    
    # Check for raw markdown in visible text area
    # 1. Look for pipe tables
    pipes = re.findall(r'<p[^>]*>[^<]*\|[^<]*</p>', clean)
    print(f"  Pipe tables in <p> tags: {len(pipes)}")
    for p in pipes:
        # Strip HTML tags for clean view
        txt = re.sub(r'<[^>]+>', '', p)
        print(f"    -> '{txt[:120]}'")
    
    # 2. Check actual table elements
    tables = re.findall(r'<table', clean)
    print(f"  HTML <table> elements: {len(tables)}")
    
    # 3. Check for proper rendered bold (<strong> or <b>)
    strongs = re.findall(r'<(strong|b)>', clean)
    print(f"  <strong>/<b> elements: {len(strongs)}")
    
    # 4. Check if there are raw ** that are NOT in scripts (phone numbers etc)
    # First remove remaining HTML tags for visible text
    visible = re.sub(r'<[^>]+>', '\n', clean)
    bold_raw = re.findall(r'\*\*', visible)
    print(f"  Raw ** in visible text: {len(bold_raw)}")
    
    # 5. Check <h1-h6> tags for raw markdown characters
    headings = re.findall(r'<h[1-6][^>]*>(.*?)</h[1-6]>', clean, re.DOTALL | re.IGNORECASE)
    raw_heading_md = 0
    for h in headings:
        if re.search(r'##|###|####|#####|######', h):
            raw_heading_md += 1
            print(f"  RAW MD IN HEADING: {h[:100]}")
    print(f"  Raw ## in headings: {raw_heading_md}")
    
    # 6. Check FAQ section for schema visible as text
    faq_schema_text = re.findall(r'schema\.org|ld\+json|application/ld\+json', visible, re.IGNORECASE)
    print(f"  schema.org/ld+json visible as text: {len(faq_schema_text)}")
    
    # 7. Check if there's proper FAQ schema
    faq_schemas = re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>.*?"@type"\s*:\s*"FAQPage"', html, re.DOTALL | re.IGNORECASE)
    print(f"  FAQPage schema present: {len(faq_schemas)}")
    
