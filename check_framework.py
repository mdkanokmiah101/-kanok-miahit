import re

with open('src/app/blog/data.js', 'r') as f:
    content = f.read()

# Find all post slug positions
slugs = list(re.finditer(r'slug:\s*"([^"]+)"', content))
slug_map = {m.group(1): m.start() for m in slugs}
slug_order = [m.group(1) for m in slugs]

def get_post_body(target_slug):
    idx = slug_order.index(target_slug)
    start = slug_map[target_slug]
    if idx + 1 < len(slug_order):
        end = slug_map[slug_order[idx + 1]]
    else:
        end = len(content)
    post_text = content[start:end]
    m = re.search(r'content:\s*`(.+)`\s*,?\s*\}', post_text, re.DOTALL)
    if m:
        return m.group(1)
    return post_text

# --- Post 1: GEO ---
body1 = get_post_body('geo-optimization-prepare-business-ai-search')
print("=== POST 1: GEO Optimization ===")
for kw in ['GEO Optimization', 'Generative Engine Optimization', 'GEO']:
    c = len(re.findall(re.escape(kw), body1, re.IGNORECASE))
    print(f"TF-IDF '{kw}': {c}")

q_pattern = r'^#{2,4}\s+(How|What|Why|When|Where|Can|Do|Is|Are)\b'
qhs1 = re.findall(q_pattern, body1, re.MULTILINE)
print(f"Question headings ({len(qhs1)}): {qhs1}")

links1 = re.findall(r'/blog/[\w-]+|/services/[\w-]+|/industries/[\w-]+|/locations/[\w-]+', body1)
print(f"Internal links: {len(set(links1))} unique ({len(links1)} total)")

for e in ['Bangladesh', 'Dhaka', 'ChatGPT', 'Gemini', 'Perplexity', 'Structured Data', 'FAQ Schema', 'E-E-A-T']:
    c = len(re.findall(re.escape(e), body1, re.IGNORECASE))
    print(f"Entity '{e}': {c}")
print()

# --- Post 2: Garments ---
body2 = get_post_body('seo-garments-textile-industry-b2b-lead-generation')
print("=== POST 2: Garments ===")
for kw in ['garment', 'textile', 'B2B SEO', 'garments and textile']:
    c = len(re.findall(re.escape(kw), body2, re.IGNORECASE))
    print(f"TF-IDF '{kw}': {c}")

qhs2 = re.findall(q_pattern, body2, re.MULTILINE)
print(f"Question headings ({len(qhs2)}): {qhs2}")

links2 = re.findall(r'/blog/[\w-]+|/services/[\w-]+|/industries/[\w-]+|/locations/[\w-]+', body2)
print(f"Internal links: {len(set(links2))} unique ({len(links2)} total)")

for e in ['Bangladesh', 'Dhaka', 'Chittagong', 'RMG', 'B2B', 'Oeko-Tex', 'GOTS', 'WRAP', 'Kanok Miah', 'international buyer']:
    c = len(re.findall(re.escape(e), body2, re.IGNORECASE))
    print(f"Entity '{e}': {c}")
print()

# --- Post 3: Mobile SEO ---
body3 = get_post_body('mobile-seo-optimization-bangladesh-mobile-first-era')
print("=== POST 3: Mobile SEO ===")
for kw in ['Mobile SEO', 'mobile optimization', 'mobile-first']:
    c = len(re.findall(re.escape(kw), body3, re.IGNORECASE))
    print(f"TF-IDF '{kw}': {c}")

qhs3 = re.findall(q_pattern, body3, re.MULTILINE)
print(f"Question headings ({len(qhs3)}): {qhs3}")

links3 = re.findall(r'/blog/[\w-]+|/services/[\w-]+|/industries/[\w-]+|/locations/[\w-]+', body3)
print(f"Internal links: {len(set(links3))} unique ({len(links3)} total)")

for e in ['Bangladesh', 'Dhaka', 'Core Web Vitals', 'voice search', 'AMP', 'Google Business Profile', 'Kanok Miah']:
    c = len(re.findall(re.escape(e), body3, re.IGNORECASE))
    print(f"Entity '{e}': {c}")
print()

# --- Post 4: Healthcare ---
body4 = get_post_body('seo-healthcare-medical-clinics-bangladesh')
print("=== POST 4: Healthcare ===")
for kw in ['Healthcare SEO', 'medical SEO', 'SEO for Healthcare']:
    c = len(re.findall(re.escape(kw), body4, re.IGNORECASE))
    print(f"TF-IDF '{kw}': {c}")

qhs4 = re.findall(q_pattern, body4, re.MULTILINE)
print(f"Question headings ({len(qhs4)}): {qhs4}")

links4 = re.findall(r'/blog/[\w-]+|/services/[\w-]+|/industries/[\w-]+|/locations/[\w-]+', body4)
print(f"Internal links: {len(set(links4))} unique ({len(links4)} total)")

for e in ['Bangladesh', 'Dhaka', 'Chittagong', 'Sylhet', 'patient', 'Google Business Profile', 'Kanok Miah', 'schema', 'EEAT', 'clinic', 'hospital']:
    c = len(re.findall(re.escape(e), body4, re.IGNORECASE))
    print(f"Entity '{e}': {c}")

# Also check pillar links
print()
print("=== PILLAR LINKS ===")
for name, body in [("GEO", body1), ("Garments", body2), ("Mobile SEO", body3), ("Healthcare", body4)]:
    has_pillar = '/blog/complete-seo-guide-bangladesh-businesses-2026' in body
    print(f"{name}: Links to pillar page = {has_pillar}")
    
# Check schema fields
print()
print("=== SCHEMA READINESS ===")
posts_info = [
    ('geo-optimization-prepare-business-ai-search', 'GEO Optimization'),
    ('seo-garments-textile-industry-b2b-lead-generation', 'Garments'),
    ('mobile-seo-optimization-bangladesh-mobile-first-era', 'Mobile SEO'),
    ('seo-healthcare-medical-clinics-bangladesh', 'Healthcare'),
]
for slug, name in posts_info:
    idx = slug_order.index(slug)
    start = slug_map[slug]
    if idx + 1 < len(slug_order):
        end = slug_map[slug_order[idx + 1]]
    else:
        end = len(content)
    post_text = content[start:end]
    has_title = "'title:" in post_text or '"title:' in post_text
    has_date = "'date:" in post_text or '"date:' in post_text
    has_excerpt = "'excerpt:" in post_text or '"excerpt:' in post_text
    has_dateModified = "'dateModified:" in post_text or '"dateModified:' in post_text
    print(f"{name}: title={'✅' if has_title else '❌'} date={'✅' if has_date else '❌'} excerpt={'✅' if has_excerpt else '❌'} dateModified={'✅' if has_dateModified else '❌'}")
