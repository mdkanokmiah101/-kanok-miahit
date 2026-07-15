#!/bin/bash

for slug in complete-seo-guide-bangladesh-businesses-2026 why-ecommerce-store-needs-seo-bangladesh link-building-strategies-bangladesh-market seo-real-estate-developers-dhaka schema-markup-rich-snippets-techniques; do
  f="page_${slug}.html"
  
  # (1) raw **bold** markers
  bold=$(grep -o '\*\*' "$f" 2>/dev/null | wc -l)
  
  # (2) raw [text](url) markdown links
  mdlinks=$(grep -oP '\[.*?\]\(https?://[^)]*\)' "$f" 2>/dev/null | wc -l)
  
  # (3) raw --- (horizontal rule in markdown)
  dashes=$(grep -c '^---$' "$f" 2>/dev/null || echo 0)
  
  # (4) raw markdown headings (## or ### rendered as text)
  hashes=$(grep -oP '^#{1,6}\s+' "$f" 2>/dev/null | wc -l)
  
  # (5) raw schema.org or ld+json visible as text in HTML body
  schema_text=$(python3 -c "
import re
with open('$f','r') as f:
    html = f.read()
html_no_script = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL|re.IGNORECASE)
html_no_style = re.sub(r'<style[^>]*>.*?</style>', '', html_no_script, flags=re.DOTALL|re.IGNORECASE)
count = len(re.findall(r'schema\.org|ld\+json', html_no_style, re.IGNORECASE))
print(count)
" 2>/dev/null)
  
  echo "$slug|$bold|$mdlinks|$dashes|$hashes|$schema_text"
done
