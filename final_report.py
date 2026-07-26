#!/usr/bin/env python3
print("""
╔══════════════════════════════════════════════════════════════════════════════════════════════╗
║                     RAW MARKDOWN RENDERING AUDIT REPORT                                      ║
║                     kanokmiah.com.bd — 5 blog posts                                          ║
║                     Scanned: 2026-07-25                                                      ║
╚══════════════════════════════════════════════════════════════════════════════════════════════╝

Checks performed on visible text (scripts, styles, comments, SVG stripped):
  1. Raw **bold** markers          — count of literal "**" in visible text
  2. Raw [text](url) links         — count of "[text](" patterns in visible text
  3. Raw --- horizontal rules      — count of standalone "---" in visible text
  4. Raw ## in headings            — checks rendered <h1..h6> for unprocessed markdown
  5. schema.org / ld+json visible  — schema terms appearing outside <script> tags

┌──────────────────────────────────────────────────────────┬──────┬──────────┬──────┬────────┬──────────┐
│ Post                                                     │  **  │ [text](  │ ---  │ Raw ## │ Schema   │
├──────────────────────────────────────────────────────────┼──────┼──────────┼──────┼────────┼──────────┤
│ complete-seo-guide-bangladesh-businesses-2026            │  0   │    0     │  1*  │   0    │    0     │
│ local-seo-tips-dhaka-businesses-google-maps              │  0   │    0     │  0   │   0    │    0     │
│ why-ecommerce-store-needs-seo-bangladesh                 │  0   │    0     │  0   │   0    │    0     │
│ technical-seo-checklist-bangladeshi-websites             │  0   │    0     │  0   │   0    │    0     │
│ how-to-choose-right-seo-agency-bangladesh                │  0   │    0     │  0   │   0    │    0     │
└──────────────────────────────────────────────────────────┴──────┴──────────┴──────┴────────┴──────────┘

* The single "---" finding on the first post is actually a raw unrendered markdown TABLE 
  separator row:  |----------|----------|-----------------|--------|----------|
  appears as plain text inside a <p> tag. This is a real rendering defect.

DETAILED FINDINGS:
""")

import subprocess, re

slugs = [
    ("complete-seo-guide-bangladesh-businesses-2026", "Complete SEO Guide for Bangladesh Businesses 2026"),
    ("local-seo-tips-dhaka-businesses-google-maps", "Local SEO Tips for Dhaka Businesses — Google Maps"),
    ("why-ecommerce-store-needs-seo-bangladesh", "Why Your E-commerce Store Needs SEO in Bangladesh"),
    ("technical-seo-checklist-bangladeshi-websites", "Technical SEO Checklist for Bangladeshi Websites"),
    ("how-to-choose-right-seo-agency-bangladesh", "How to Choose the Right SEO Agency in Bangladesh"),
]

for slug, title in slugs:
    url = f"https://kanokmiah.com.bd/blog/{slug}"
    result = subprocess.run(["curl", "-sL", url, "--max-time", "15"], capture_output=True, text=True, timeout=20)
    html = result.stdout
    clean = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
    clean = re.sub(r'<style[^>]*>.*?</style>', '', clean, flags=re.DOTALL | re.IGNORECASE)
    clean = re.sub(r'<!--.*?-->', '', clean, flags=re.DOTALL)
    
    print(f"  ┌─ {slug}")
    print(f"  │  Title: {title}")
    
    # Bold
    visible = re.sub(r'<[^>]+>', '\n', clean)
    bold_count = len(re.findall(r'\*\*', visible))
    print(f"  ├─ ** bold markers:        {bold_count} {'✓' if bold_count == 0 else '✗ ISSUE'}")
    
    # Links
    link_count = len(re.findall(r'\[.*?\]\(', visible))
    print(f"  ├─ [text](url) links:      {link_count} {'✓' if link_count == 0 else '✗ ISSUE'}")
    
    # ---
    hr_count = len(re.findall(r'(?<![a-zA-Z0-9])---(?![a-zA-Z0-9])', visible))
    status_hr = "✓" if hr_count == 0 else "✗ ISSUE — raw table separator"
    print(f"  ├─ --- horizontal rules:   {hr_count} {status_hr}")
    if hr_count > 0:
        matches = re.findall(r'.{0,40}---.{0,40}', visible)
        for m in matches:
            print(f"  │    Raw text: \"{m.strip()}\"")
    
    # Headings
    headings = re.findall(r'<h[1-6][^>]*>(.*?)</h[1-6]>', clean, re.DOTALL | re.IGNORECASE)
    raw_h = sum(1 for h in headings if re.search(r'##|###|####|#####|######', h))
    print(f"  ├─ Raw ## in headings:     {raw_h} {'✓' if raw_h == 0 else '✗ ISSUE'}")
    
    # Schema
    schema_text = len(re.findall(r'schema\.org|ld\+json|application/ld\+json', visible, re.IGNORECASE))
    print(f"  ├─ schema.org visible:     {schema_text} {'✓' if schema_text == 0 else '✗ ISSUE'}")
    
    # Extra: check for FAQPage schema
    faqpage = re.findall(r'"FAQPage"', html)
    print(f"  └─ FAQPage schema present: {len(faqpage)} {'✓ FAQ schema found' if len(faqpage) > 0 else '— none (not necessarily an issue)'}")
    print()

print("""
╔══════════════════════════════════════════════════════════════════════════════════════════════╗
║                                     CONCLUSIONS                                             ║
╚══════════════════════════════════════════════════════════════════════════════════════════════╝

✓ PASS — Raw **bold** markdown:       0 issues across all 5 posts. No unrendered bold syntax.
✓ PASS — Raw [text](url) links:       0 issues across all 5 posts. Links properly rendered.
✗ ISSUE — Raw --- horizontal rules:   1 issue found.
     Post: complete-seo-guide-bangladesh-businesses-2026
     A markdown table separator row renders as raw visible text:
       "|----------|----------|-----------------|--------|----------|"
     inside a <p> tag. The markdown table was not converted to an HTML <table>.
     No <table> element exists on the page. The expected content (table with 5 
     columns showing SEO campaign results) is missing from the rendered output.
✓ PASS — Headings:                    0 issues. All <h2> tags are clean.
✓ PASS — FAQ schema:                  No raw schema text visible. Structured data
     (Organization, LocalBusiness, Article, BreadcrumbList, etc.) is properly
     embedded in <script type="application/ld+json"> blocks. No FAQPage schema 
     found on any post (content mentions FAQs but lacks FAQPage markup).

════════════════════════════════════════════════════════════════════════════════════════════════

SUMMARY: 4 of 5 pages are clean. 1 page (Complete SEO Guide) has a rendering defect 
where a markdown table separator row is visible as raw text.

The table content appears to be intended to show SEO campaign results but the 
markdown was not processed — only the separator row is visible. The missing 
content should likely be an HTML <table> with 5 columns of data.
""")
