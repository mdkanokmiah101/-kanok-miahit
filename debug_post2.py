#!/usr/bin/env python3
"""
Debug: find content: field near slug
"""
import re

with open('/root/kanok-miahit/src/app/blog/data.js', 'r', encoding='utf-8') as f:
    content = f.read()

slug = 'why-md-kanok-miah-is-the-best-seo-expert-in-dhaka-bangladesh'
slug_idx = content.find(f'slug: "{slug}"')

print(f"Slug at index: {slug_idx}")

# Search for 'content:' between slug_idx and slug_idx + 2000
content_field = content.find('content:', slug_idx, slug_idx + 2000)
print(f"'content:' found at: {content_field}")
print(f"Distance from slug: {content_field - slug_idx}")
print(f"Context: {repr(content[content_field:content_field+30])}")

# Find the backtick
btick = content.find('`\n', content_field)
if btick == -1 or btick > content_field + 20:
    btick = content.find('`', content_field)
print(f"Backtick at: {btick}")
print(f"Context: {repr(content[btick:btick+20])}")

# Find closing backtick: `,\n or `\n,
# Look for ` near the end - after btick
# The closing should be ` followed by , (comma) or whitespace+comma
end_search = content.find('`,', btick + 100)  # start searching after some content
if end_search == -1:
    # Try `\n  ,
    end_search = content.find('`,\n  }', btick + 100)
if end_search == -1:
    # Try just the next `, 
    end_search = content.find('`,\n', btick + 100)
print(f"Closing backtick-comma at: {end_search}")

if end_search > 0:
    post_content = content[btick+1:end_search]
    print(f"\n=== POST CONTENT ===")
    print(f"Length: {len(post_content)}")
    print(f"Word count: {len(post_content.split())}")
    
    # Headings
    all_headings = re.findall(r'^(#{2,4})\s+(.+)$', post_content, re.MULTILINE)
    print(f"\nTotal headings: {len(all_headings)}")
    
    # Question headings
    qh = [h[1] for h in all_headings if h[1].strip().startswith(('How', 'What', 'Why', 'Where', 'When', 'Which', 'Who', 'Does', 'Can', 'Is', 'Are', 'Do'))]
    print(f"Question headings (AEO/GEO): {len(qh)}")
    for q in qh:
        print(f"  - {q}")
    
    # Keywords
    print(f"\n--- TF-IDF Keywords ---")
    kws = [
        ('seo expert in dhaka', 'SEO expert in Dhaka'),
        ('seo expert dhaka', 'SEO expert Dhaka'),
        ('best seo expert dhaka', 'best SEO expert Dhaka'),
        ('best seo expert', 'best SEO expert'),
        ('kanok miah', 'Kanok Miah'),
    ]
    for kw, label in kws:
        c = len(re.findall(re.escape(kw), post_content, re.IGNORECASE))
        print(f"  '{label}': {c}")
    
    # Internal links
    print(f"\n--- Internal Links ---")
    links = re.findall(r'\(/([^)]+)\)', post_content)
    full_links = ['/' + l for l in links]
    unique_links = sorted(set(full_links))
    print(f"Total link occurrences: {len(full_links)}")
    print(f"Unique links: {len(unique_links)}")
    for l in unique_links:
        print(f"  {l}")
    
    # Check pillar link
    has_geo = '/blog/geo-optimization-prepare-business-ai-search' in post_content
    print(f"\n  Pillar link (geo-optimization): {'✅ FOUND' if has_geo else '❌ MISSING'}")
    
    # External links
    externals = re.findall(r'\((https?://[^)]+)\)', post_content)
    if externals:
        print(f"\n--- External Links ---")
        for e in externals:
            print(f"  {e}")
    
    # Entities
    print(f"\n--- Key Entities ---")
    entities = ['Dhaka', 'Bangladesh', 'Google', 'Local SEO', 'Technical SEO', 
                'GEO', 'Google Business Profile', 'EEAT', 'E-E-A-T',
                'Khan IT', 'CloudMatrix Tech', 'Walton Plaza', 'LinkedIn',
                'Core Web Vitals', 'Schema', 'structured data']
    for e in entities:
        c = len(re.findall(re.escape(e), post_content, re.IGNORECASE))
        status = '✅' if c >= 3 else '⚠️' if c >= 1 else '❌'
        print(f"  {status} '{e}': {c}")
    
    # FAQ entries (in data, not just in content)
    print(f"\n--- FAQ (in post metadata) ---")
    # Count question: in post_text
    post_text = content[slug_idx-5:end_search+100]
    faq_q = post_text.count('question:')
    faq_a = post_text.count('answer:')
    print(f"  FAQ questions in metadata: {faq_q}")
    print(f"  FAQ answers in metadata: {faq_a}")
    
    # Word count per section
    print(f"\n--- Content Stats ---")
    print(f"  Total word count: {len(post_content.split())}")
    h2_headings = re.findall(r'^##\s+(.+)$', post_content, re.MULTILINE)
    print(f"  H2 sections: {len(h2_headings)}")
    
    # Check the Enforcement Report result (from July 27)
    print(f"\n--- Enforcement Report (2026-07-27) Status ---")
    print(f"  🏛️ Pillar Link: {'FIXED ✅' if has_geo else 'STILL MISSING ❌'}")
    print(f"  💬 AEO/GEO: ✅ (was already passing with {len(qh)} question headings)")
    print(f"  🔗 Internal Links: ✅ ({len(unique_links)} unique)")
    
    # Incoming links from other posts
    print(f"\n--- Incoming Links Analysis ---")
    blog_url = f'/blog/{slug}'
    total_refs = content.count(blog_url)
    own_refs = post_content.count(blog_url)
    print(f"  Total URL references in data.js: {total_refs}")
    print(f"  Self-references (within post): {own_refs}")
    print(f"  Incoming from other posts: {total_refs - own_refs}")
    
