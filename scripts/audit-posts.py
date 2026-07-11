#!/usr/bin/env python3
"""Audit blog posts in data.js for word count and content quality."""
import re

with open('src/app/blog/data.js', 'r') as f:
    data = f.read()

# Find all post blocks by splitting on slug pattern
entries = data.split('    slug: "')
entries = entries[1:]  # Skip header

print(f"{'#':>3} | {'Slug':<60} | {'Words':>5} | {'Status':<12} | {'Headings':>8} | {'FAQ':>5} | {'AE':>5}")
print("-" * 110)

for i, entry in enumerate(entries):
    slug = entry.split('"')[0]
    
    content_match = re.search(r'content: `(.*?)`,', entry, re.DOTALL)
    if content_match:
        content = content_match.group(1)
        words = len(content.split())
    else:
        content = ""
        words = 0
    
    # Check headings
    h2 = len(re.findall(r'^##[^#]', content, re.MULTILINE))
    h3 = len(re.findall(r'^###[^#]', content, re.MULTILINE))
    
    # Check for FAQ
    has_faq = "Frequently Asked" in content or "FAQ" in content
    
    # Check for author expertise signals
    has_author_exp = "Md Kanok Miah" in content or "I have helped" in content or "my experience" in content.lower() or "I have been" in content
    
    # Check keywords
    has_best_seo = "best seo expert in dhaka" in content.lower()
    has_name = "Md Kanok Miah" in content
    has_bangladesh = "Bangladesh" in content
    has_seo = "SEO" in content
    
    # Check for internal links
    service_links = len(re.findall(r'/services/', content))
    industry_links = len(re.findall(r'/industries/', content))
    blog_links = len(re.findall(r'/blog/', content))
    
    status = "✅ OK" if words >= 2000 else "⚠️ SHORT"
    if i >= 15:
        break
    
    # More detailed checks for first 15
    aeo_signals = "✅" if (has_faq and "FAQ" in content.upper()) else "❌"
    geo_signals = "✅" if (has_name and has_bangladesh and "Dhaka" in content) else "❌"
    eeat_signals = "✅" if has_author_exp else "❌"
    
    print(f"{i+1:3d} | {slug:<60} | {words:5d} | {status:<12} | H2:{h2} H3:{h3} | {'Y' if has_faq else 'N'} | {'Y' if has_author_exp else 'N'}")
    print(f"     | {'':<60} | {'':5} | {'':12} | {'':8} | Link:/svc:{service_links} /ind:{industry_links} /blog:{blog_links}")
    print(f"     | {'':<60} | {'':5} | {'':12} | Keyw: best-seo={has_best_seo} name={has_name} BD={has_bangladesh} SEO={has_seo} {'| ⚠️ LOW' if words < 2000 else ''}")
    print(f"     | {'':<60} | {'':5} | {'':12} | AEO={aeo_signals} GEO={geo_signals} EEAT={eeat_signals}")
