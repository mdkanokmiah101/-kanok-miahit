#!/usr/bin/env python3
"""Debug script to extract post content properly"""
import re

with open('/root/kanok-miahit/src/app/blog/data.js', 'r', encoding='utf-8') as f:
    content = f.read()

slug = 'why-md-kanok-miah-is-the-best-seo-expert-in-dhaka-bangladesh'
slug_idx = content.find(f'slug: "{slug}"')

# Show context around slug
print(f"Slug found at index: {slug_idx}")
print(f"Context before: {content[slug_idx-50:slug_idx+50]}")

# Show the content: field
content_field = content.find('content:', slug_idx, slug_idx+30)
print(f"\n'content:' field at index: {content_field}")

# Show the characters around content:
print(f"Context: {repr(content[content_field:content_field+50])}")

# Find the backtick
btick = content.find('`', content_field)
print(f"\nFirst backtick at: {btick}")
print(f"Context: {repr(content[btick:btick+20])}")

# Now find the closing backtick - look for `, (backtick comma)
closing = content.find('`,', btick+1)
print(f"\nClosing backtick at: {closing}")
if closing > 0:
    post_content = content[btick+1:closing]
    print(f"\nContent length: {len(post_content)}")
    print(f"First 200 chars: {post_content[:200]}")
    print(f"Word count: {len(post_content.split())}")
    
    # Headings
    h2 = re.findall(r'^##\s+(.+)$', post_content, re.MULTILINE)
    print(f"\nH2 headings: {len(h2)}")
    for h in h2[:5]:
        print(f"  - {h}")
    
    # Question headings
    qh = [h for h in h2 if h.strip().startswith(('How', 'What', 'Why', 'Where', 'When', 'Which', 'Who', 'Does', 'Can', 'Is', 'Are', 'Do'))]
    print(f"\nQuestion headings: {len(qh)}")
    for q in qh:
        print(f"  - {q}")
    
    # Count keywords
    for kw in ['seo expert in dhaka', 'seo expert dhaka', 'best seo expert dhaka']:
        c = len(re.findall(re.escape(kw), post_content, re.IGNORECASE))
        print(f"  '{kw}': {c}")
    
    # Internal links
    links = re.findall(r'\((/[^)]+)\)', post_content)
    blog_links = [l for l in links if l.startswith('/')]
    print(f"\nInternal links: {len(links)}")
    print(f"Unique paths: {len(set(links))}")
    for l in sorted(set(links)):
        print(f"  {l}")
    
    # Check for pillar link
    has_pillar = '/blog/geo-optimization-prepare-business-ai-search' in post_content
    print(f"\nPillar link (geo-optimization): {'YES' if has_pillar else 'NO'}")
    
    # FAQ entries
    faq_count = post_content.count('### ')
    print(f"FAQ-like headings (###): {faq_count}")
    
    # Count actual FAQ
    faq_q = len(re.findall(r'###\s+(How|What|Why|Where|When|Which|Who|Does|Can|Is|Are|Do)', post_content))
    print(f"Question-format headings: {faq_q}")
