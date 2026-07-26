#!/usr/bin/env python3
"""Fetch kanokmiah.com.bd pages and validate schema markup."""
import json
import re
import urllib.request
import urllib.error
import sys
import time

def fetch_page(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read().decode('utf-8', errors='replace')
    except Exception as e:
        return None

def extract_jsonld(html):
    pattern = r'<script type="application/ld\+json">(.*?)</script>'
    blocks = re.findall(pattern, html, re.DOTALL)
    result = []
    for block in blocks:
        try:
            data = json.loads(block.strip())
            result.append(data)
        except json.JSONDecodeError:
            pass
    return result

def find_localbusiness(schemas):
    for s in schemas:
        if isinstance(s, dict):
            if s.get('@type') == 'LocalBusiness':
                return s
            if '@graph' in s:
                for item in s['@graph']:
                    if item.get('@type') == 'LocalBusiness':
                        return item
    return None

def find_faqpage(schemas):
    for s in schemas:
        if isinstance(s, dict):
            if s.get('@type') == 'FAQPage':
                return s
            if '@graph' in s:
                for item in s['@graph']:
                    if item.get('@type') == 'FAQPage':
                        return item
    return None

def has_aggregate_rating(schema):
    if isinstance(schema, dict):
        if 'aggregateRating' in schema:
            return True
        if '@graph' in schema:
            for item in schema['@graph']:
                if 'aggregateRating' in item:
                    return True
    return False

results = []

# Check 1: Homepage Schema
print("=== CHECK 1: Homepage Schema ===")
home_html = fetch_page("https://kanokmiah.com.bd/")
if home_html is None:
    print("FAIL: Could not fetch homepage")
    sys.exit(1)

home_schemas = extract_jsonld(home_html)
print(f"Found {len(home_schemas)} JSON-LD block(s)")

lb = find_localbusiness(home_schemas)
if lb:
    print("PASS: LocalBusiness schema found")
    results.append(("LocalBusiness on homepage", True))
else:
    print("FAIL: LocalBusiness schema NOT found")
    results.append(("LocalBusiness on homepage", False))

if has_aggregate_rating(lb if lb else {}):
    print("FAIL: aggregateRating IS present (should NOT be)")
    results.append(("aggregateRating absent on homepage", False))
else:
    print("PASS: aggregateRating NOT present")
    results.append(("aggregateRating absent on homepage", True))

fq_home = find_faqpage(home_schemas)
if fq_home:
    print("FAIL: FAQPage IS present on homepage (should NOT be)")
    results.append(("FAQPage absent on homepage", False))
else:
    print("PASS: FAQPage NOT present on homepage")
    results.append(("FAQPage absent on homepage", True))

# Check 2: FAQ Page Schema
print("\n=== CHECK 2: FAQ Page Schema ===")
faq_html = fetch_page("https://kanokmiah.com.bd/faq")
if faq_html is None:
    print("FAIL: Could not fetch /faq")
    sys.exit(1)

faq_schemas = extract_jsonld(faq_html)
print(f"Found {len(faq_schemas)} JSON-LD block(s)")

fq = find_faqpage(faq_schemas)
if fq:
    print("PASS: FAQPage schema found on /faq")
    results.append(("FAQPage on /faq", True))
    questions = fq.get('mainEntity', [])
    if isinstance(questions, list):
        print(f"  Contains {len(questions)} Q&A entries")
        for qa in questions[:3]:
            q_name = qa.get('name', 'N/A') if isinstance(qa, dict) else 'N/A'
            print(f"  - Q: {q_name}")
else:
    print("FAIL: FAQPage schema NOT found on /faq")
    results.append(("FAQPage on /faq", False))

# Check 3: TTFB
print("\n=== CHECK 3: TTFB ===")
start = time.time()
try:
    with urllib.request.urlopen('https://kanokmiah.com.bd/', timeout=15) as r:
        first_byte = time.time()
        r.read()
        end = time.time()
    ttfb = first_byte - start
    print(f"PASS: TTFB = {ttfb:.3f}s")
    if ttfb > 1.5:
        print("WARNING: Exceeds 1.5s threshold!")
        results.append(("TTFB under 1.5s", False))
    else:
        results.append(("TTFB under 1.5s", True))
except Exception as e:
    print(f"FAIL: Could not measure TTFB: {e}")
    results.append(("TTFB under 1.5s", False))

print("\n\n=== SUMMARY ===")
all_pass = True
for name, status in results:
    mark = "PASS" if status else "FAIL"
    print(f"  [{mark}] {name}")
    if not status:
        all_pass = False

print()
if all_pass:
    print("All checks passed. Site healthy.")
else:
    print("Some checks failed. See above for details.")
