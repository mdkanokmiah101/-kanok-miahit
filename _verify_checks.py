#!/usr/bin/env python3
"""Verify specific edge cases in the framework checks"""
import re

with open("/root/kanok-miahit/src/app/blog/data.js") as f:
    content = f.read()

def extract_post_text(content, slug):
    """Extract full post text more reliably"""
    idx = content.find(f'slug: "{slug}"')
    if idx == -1:
        print(f"  SLUG NOT FOUND: {slug}")
        return ""
    
    # Walk back to opening brace
    brace = 0
    for i in range(idx, max(idx-300, -1), -1):
        if content[i] == '}': brace += 1
        elif content[i] == '{': 
            brace -= 1
            if brace < 0:
                start = i
                break
    else:
        print(f"  Could not find opening brace")
        return ""
    
    # Walk forward to matching closing brace
    brace = 0
    in_bt = False
    for i in range(start, len(content)):
        ch = content[i]
        if in_bt:
            if ch == '`': in_bt = False
        else:
            if ch == '`': in_bt = True
            elif ch == '{': brace += 1
            elif ch == '}':
                brace -= 1
                if brace == 0:
                    return content[start:i+1]
    return ""

def extract_content(post_text):
    m = re.search(r'content:\s*`\n(.*?)`', post_text, re.DOTALL)
    if m: return m.group(1)
    return ""

def parse_field(post_text, field):
    m = re.search(rf'{field}:\s*"((?:[^"\\]|\\.)*)"', post_text, re.DOTALL)
    if m: return m.group(1)
    return None

# 1. Schema post
print("=== schema-markup-rich-snippets-techniques ===")
t = extract_post_text(content, "schema-markup-rich-snippets-techniques")
print(f"  Excerpt: {parse_field(t, 'excerpt')[:80]}")
c = extract_content(t)
print(f"  Content length: {len(c)}")
print(f"  'rich snippets' (EN): {c.lower().count('rich snippets')}")
print(f"  'রিচ স্নিপেট' (BN): {c.count('রিচ স্নিপেট')}")
print(f"  'bangladesh seo' (EN): {c.lower().count('bangladesh seo')}")
print(f"  'বাংলাদেশ' (BN): {c.count('বাংলাদেশ')}")
# Question headings
qhs = re.findall(r'^#{2,3}\s+(How|What|Why|When|Where|Can|Do|Is|Are|Does|Which|Who)\b', c, re.MULTILINE)
print(f"  Question headings (EN): {len(qhs)} - {qhs}")
# Bengali question word patterns
bn_qs = re.findall(r'^#{2,3}\s+(কীভাবে|কেন|কখন|কোথায়|কী|কি|কেন|কিভাবে|কোন)\b', c, re.MULTILINE)
print(f"  Question headings (BN): {len(bn_qs)} - {bn_qs}")
# Also check Bengali headings pattern
headings = re.findall(r'^##\s+.*$', c, re.MULTILINE)[:20]
print(f"  Sample headings: {headings[:10]}")

print()

# 2. Mobile SEO post
print("=== mobile-seo-optimization-bangladesh-mobile-first-era ===")
t2 = extract_post_text(content, "mobile-seo-optimization-bangladesh-mobile-first-era")
c2 = extract_content(t2)
# Check for 'mobile seo bangladesh' or 'seo in bangladesh' or similar
print(f"  'mobile seo bangladesh': {c2.lower().count('mobile seo bangladesh')}")
print(f"  'mobile seo' overall: {c2.lower().count('mobile seo')}")
print(f"  'seo for bangladesh': {c2.lower().count('seo for bangladesh')}")
print(f"  'mobile-first' in content: {c2.lower().count('mobile-first')}")
# Check title pattern usage
print(f"  Title contains 'Mobile SEO for Bangladesh' - checking body variation")
title_in_body = c2.lower().count('mobile seo for bangladesh')
print(f"  'mobile seo for bangladesh' in body: {title_in_body}")

# 3. How-to-choose post  
print()
print("=== how-to-choose-best-seo-expert-dhaka-15-things ===")
t3 = extract_post_text(content, "how-to-choose-best-seo-expert-dhaka-15-things")
c3 = extract_content(t3)
print(f"  'choose best seo': {c3.lower().count('choose best seo')}")
print(f"  'choose the best': {c3.lower().count('choose the best')}")
print(f"  'choosing seo': {c3.lower().count('choosing seo')}")
print(f"  'hire seo expert': {c3.lower().count('hire seo expert')}")
print(f"  'seo expert dhaka': {c3.lower().count('seo expert dhaka')}")
print(f"  'seo services bangladesh': {c3.lower().count('seo services bangladesh')}")
print(f"  'best seo expert': {c3.lower().count('best seo expert')}")
print(f"  Has question headings:")
qhs3 = re.findall(r'^#{2,3}\s+(How|What|Why|When|Where|Can|Do|Is|Are|Does|Which|Who)\b', c3, re.MULTILINE)
print(f"    EN: {len(qhs3)} - {qhs3}")
# Check AEO/GEO headings starting with question words
all_h3 = re.findall(r'^##\s+.*$', c3, re.MULTILINE)[:20]
print(f"  H2 headings: {all_h3}")
