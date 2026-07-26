#!/usr/bin/env python3
"""Audit kanokmiah blog posts - corrected version."""
import re
import json

with open('/root/kanok-miahit/src/app/blog/data.js', 'r') as f:
    raw = f.read()

# Split file into individual post blocks
# Posts are separated by: },\n  {\n    slug:
# First post starts after "const posts = [\n  {\n"

# Find all post boundaries
posts_raw = re.split(r'\},\s*\n\s*\{', raw)

# Handle the first and last
# First element: "const posts = [\n  {\n    slug: ..."
# Other elements: "    slug: ..."
# Last element ends with "  },\n];\nexport default ..."

# Clean up first element
first = posts_raw[0]
if first.startswith('const posts = ['):
    first = first[len('const posts = ['):].strip()
    if first.startswith('{\n'):
        first = first[2:]  # remove opening brace and newline
    elif first.startswith('\n  {\n'):
        first = first[5:]

posts_raw[0] = first

# Clean up last element
last = posts_raw[-1]
# Remove trailing ], export default etc.
last = re.sub(r'\],?\s*\n?export default.*', '', last, flags=re.DOTALL)
posts_raw[-1] = last

print(f"Found {len(posts_raw)} post blocks")

# Parse each post block
post_data = []
for block in posts_raw:
    post = {}
    
    # Slug
    m = re.search(r'slug:\s*"([^"]+)"', block)
    if m:
        post['slug'] = m.group(1)
    
    # Title
    m = re.search(r'title:\s*"([^"]+)"', block)
    if m:
        post['title'] = m.group(1)
    
    # Date
    m = re.search(r'date:\s*"([^"]+)"', block)
    if m:
        post['date'] = m.group(1)
    
    # Excerpt (may span multiple lines)
    m = re.search(r'excerpt:\s*\n?\s*"([^"]+)"', block)
    if m:
        post['excerpt'] = m.group(1)
    else:
        # Try multi-line excerpt
        m2 = re.search(r'excerpt:\s*\n((?:\s*"[^"]*?"?\s*\n?)+)', block)
        if m2:
            # Clean up
            excerpt_raw = m2.group(1)
            excerpt_parts = re.findall(r'"([^"]*)"', excerpt_raw)
            post['excerpt'] = ' '.join(excerpt_parts)
        else:
            post['excerpt'] = ''
    
    # Tags
    m = re.search(r'tags:\s*\[(.*?)\]', block, re.DOTALL)
    if m:
        post['tags'] = re.findall(r'"([^"]+)"', m.group(1))
    else:
        post['tags'] = []
    
    # dateModified
    m = re.search(r'dateModified:\s*"([^"]+)"', block)
    post['dateModified'] = m.group(1) if m else ''
    
    # Content - find content between backticks after "content: `"
    content_match = re.search(r'content:\s*`(.*)`', block, re.DOTALL)
    if content_match:
        post['content'] = content_match.group(1)
    else:
        post['content'] = ''
    
    # Clean trailing backtick from content
    if post.get('content', '').endswith('`'):
        post['content'] = post['content'][:-1]
    
    post_data.append(post)

print(f"Parsed {len(post_data)} posts")
for p in post_data[:3]:
    print(f"  {p.get('slug','?')}: content_len={len(p.get('content',''))}")

# ===== ANALYSIS =====

def extract_keyword(title):
    """Extract primary keyword from title."""
    if not title:
        return ""
    t = re.sub(r'\b\d{4}\b', '', title)
    t = re.sub(r'in 2026', '', t, flags=re.IGNORECASE)
    t = t.strip()
    
    # Pattern: Complete/Ultimate/Essential X for/in/of
    m = re.search(r'(?:Complete|Ultimate|Essential|The)\s+(.*?)(?:\s+(?:for|in|to|of|that|:))', t, re.IGNORECASE)
    if m: return m.group(1).strip()
    
    # Pattern: Why X Needs/Is
    m = re.search(r'Why\s+(.*?)\s+(?:Needs|Is|Should|Must)', t, re.IGNORECASE)
    if m: return m.group(1).strip()
    
    # Pattern: How to X
    m = re.search(r'How to\s+(.*?)(?:\s+(?:for|in|to|of|the))', t, re.IGNORECASE)
    if m: return m.group(1).strip()
    
    # Pattern: X Tips/Strategies
    m = re.search(r'(.*?)\s+(?:Tips|Strategies|Checklist)\s+', t, re.IGNORECASE)
    if m: return m.group(1).strip()
    
    # Pattern: X: subtitle
    m = re.search(r'^(.*?)\s*:', t)
    if m: return m.group(1).strip()
    
    # Pattern: X for Y (SEO for Garments...)
    m = re.search(r'^(.*?)\s+for\s+', t, re.IGNORECASE)
    if m: return m.group(1).strip()
    
    # Fallback: first 2-3 words
    words = t.split()
    if len(words) >= 3:
        return ' '.join(words[:3])
    return t.strip()

def check_pillar_link(content, slug, tags, title):
    """Determine pillar link status."""
    # Mapping from tag to pillar page URL
    tag_to_pillar = {
        'SEO Guide': '/blog/complete-seo-guide-bangladesh-businesses-2026',
        'Bangladesh SEO': '/blog/complete-seo-guide-bangladesh-businesses-2026',
        'Local SEO': '/blog/local-seo-tips-dhaka-businesses-google-maps',
        'Dhaka': '/blog/local-seo-tips-dhaka-businesses-google-maps',
        'Google Maps': '/blog/local-seo-tips-dhaka-businesses-google-maps',
        'GBP': '/blog/google-business-profile-optimization-guide-bangladesh',
        'E-commerce SEO': '/blog/why-ecommerce-store-needs-seo-bangladesh',
        'E-commerce': '/blog/why-ecommerce-store-needs-seo-bangladesh',
        'Daraz': '/blog/why-ecommerce-store-needs-seo-bangladesh',
        'Shopify': '/blog/why-ecommerce-store-needs-seo-bangladesh',
        'Technical SEO': '/blog/technical-seo-checklist-bangladeshi-websites',
        'Core Web Vitals': '/blog/technical-seo-checklist-bangladeshi-websites',
        'Website Optimization': '/blog/technical-seo-checklist-bangladeshi-websites',
        'SEO Agency': '/blog/how-to-choose-right-seo-agency-bangladesh',
        'Agency Selection': '/blog/how-to-choose-right-seo-agency-bangladesh',
        'Link Building': '/blog/link-building-strategies-bangladesh-market',
        'Backlinks': '/blog/link-building-strategies-bangladesh-market',
        'GEO': '/blog/geo-optimization-prepare-business-ai-search',
        'AI Search': '/blog/geo-optimization-prepare-business-ai-search',
        'Generative Engine Optimization': '/blog/geo-optimization-prepare-business-ai-search',
        'Future of SEO': '/blog/geo-optimization-prepare-business-ai-search',
        'Garments SEO': '/blog/seo-garments-textile-industry-b2b-lead-generation',
        'Textile Industry': '/blog/seo-garments-textile-industry-b2b-lead-generation',
        'B2B SEO': '/blog/seo-garments-textile-industry-b2b-lead-generation',
        'Bangladesh RMG': '/blog/seo-garments-textile-industry-b2b-lead-generation',
        'Google Business Profile': '/blog/google-business-profile-optimization-guide-bangladesh',
        'Bangladesh Business': '/blog/google-business-profile-optimization-guide-bangladesh',
        'SEO vs Ads': '/blog/seo-vs-google-ads-whats-best-bangladesh-businesses',
        'Google Ads': '/blog/seo-vs-google-ads-whats-best-bangladesh-businesses',
        'PPC': '/blog/seo-vs-google-ads-whats-best-bangladesh-businesses',
        'Bangladesh Digital Marketing': '/blog/seo-vs-google-ads-whats-best-bangladesh-businesses',
        'Digital Marketing': '/blog/complete-seo-guide-bangladesh-businesses-2026',
    }
    
    pillar_url = None
    for tag in tags:
        if tag in tag_to_pillar:
            pillar_url = tag_to_pillar[tag]
            break
    
    if not pillar_url:
        return None, "No pillar URL determined from tags"
    
    # If this post IS the pillar, check if it links to OTHER pillar pages
    post_pillar_url = '/blog/' + slug
    if post_pillar_url == pillar_url:
        # This post is the pillar itself - check if it links to related cluster pages
        return None, f"Self (is pillar page itself)"
    
    if re.search(re.escape(pillar_url), content):
        return True, f"Links to cluster pillar: {pillar_url}"
    else:
        return False, f"Missing link to pillar page: {pillar_url}"

# ===== ANALYZE 10 ENGLISH PILLAR POSTS =====
pillar_slugs = [
    "complete-seo-guide-bangladesh-businesses-2026",
    "local-seo-tips-dhaka-businesses-google-maps",
    "why-ecommerce-store-needs-seo-bangladesh",
    "technical-seo-checklist-bangladeshi-websites",
    "how-to-choose-right-seo-agency-bangladesh",
    "link-building-strategies-bangladesh-market",
    "geo-optimization-prepare-business-ai-search",
    "seo-garments-textile-industry-b2b-lead-generation",
    "google-business-profile-optimization-guide-bangladesh",
    "seo-vs-google-ads-whats-best-bangladesh-businesses"
]

print("\n" + "="*100)
print("ENGLISH PILLAR POSTS - CONTENT FRAMEWORK AUDIT")
print("="*100)

for slug in pillar_slugs:
    post = None
    for p in post_data:
        if p.get('slug') == slug:
            post = p
            break
    
    if not post:
        print(f"\n## Post: {slug}")
        print("| Check | Status | Details |")
        print("|-------|--------|---------|")
        print("| ERROR | ❌ | Post not found in data.js |")
        continue
    
    title = post.get('title', '')
    content_text = post.get('content', '')
    tags = post.get('tags', [])
    
    # A. TF-IDF Coverage
    keyword = extract_keyword(title)
    keyword_count = len(re.findall(re.escape(keyword), content_text, re.IGNORECASE))
    if keyword_count < 3:
        # Try first word only as keyword
        first_word = keyword.split()[0] if keyword.split() else keyword
        keyword_count = max(keyword_count, len(re.findall(re.escape(first_word), content_text, re.IGNORECASE)))
        # For very generic single words, try bigram
        if len(keyword.split()) == 1 and keyword_count > 20:
            pass  # It's OK, the single word appears enough
    
    # B. Entities
    entities_missing = []
    if not re.search(r'\bDhaka\b', content_text, re.IGNORECASE):
        entities_missing.append('Dhaka')
    if not re.search(r'\bBangladesh\b', content_text, re.IGNORECASE):
        entities_missing.append('Bangladesh')
    if not re.search(r'SEO|GEO|AEO|search engine optimization', content_text, re.IGNORECASE):
        entities_missing.append('SEO service type')
    
    # Check industry mentions based on post topic
    mentions_ecomm = bool(re.search(r'e-commerce|ecommerce|online\s+store|Daraz|Shopify', content_text, re.IGNORECASE))
    mentions_garment = bool(re.search(r'garment|textile|apparel|RMG', content_text, re.IGNORECASE))
    mentions_restaurant = bool(re.search(r'restaurant|cafe|food', content_text, re.IGNORECASE))
    mentions_realestate = bool(re.search(r'real\s+estate|property', content_text, re.IGNORECASE))
    
    # C. Pillar Link
    pillar_result = check_pillar_link(content_text, slug, tags, title)
    pillar_status, pillar_details = pillar_result
    
    # D. AEO/GEO
    question_starts = ['How', 'What', 'Why', 'When', 'Where', 'Can', 'Do', 'Is', 'Are', 'Does', 'Should', 'Which']
    heading_pattern = re.compile(r'#{2,3}\s+(.*?)$', re.MULTILINE)
    headings = heading_pattern.findall(content_text)
    question_headings = [h.strip() for h in headings if any(h.strip().startswith(qs + ' ') or h.strip().startswith(qs + '?') or h.strip() == qs for qs in question_starts)]
    
    # E. Internal Links
    blog_links = set(re.findall(r'/blog/[^"\')\s>]+', content_text))
    services_links = set(re.findall(r'/services/[^"\')\s>]+', content_text))
    locations_links = set(re.findall(r'/locations/[^"\')\s>]+', content_text))
    all_internal = blog_links | services_links | locations_links
    
    # F. Schema
    schema_missing = []
    if not post.get('title'): schema_missing.append('title')
    if not post.get('excerpt'): schema_missing.append('excerpt')
    if not post.get('date'): schema_missing.append('date')
    if not post.get('dateModified'): schema_missing.append('dateModified')
    
    # Print report
    print(f"\n## Post: {slug}")
    print(f"**Title:** {title}")
    print(f"**Tags:** {tags}")
    print("| Check | Status | Details |")
    print("|-------|--------|---------|")
    
    tfidf_pass = keyword_count >= 5
    tfidf_status = "✅" if tfidf_pass else "❌"
    print(f"| TF-IDF: `{keyword}` | {tfidf_status} | {keyword_count} occurrences in content |")
    
    ent_pass = len(entities_missing) == 0
    ent_status = "✅" if ent_pass else "❌"
    missing_str = ", ".join(entities_missing) if entities_missing else "All required entities present (Dhaka, Bangladesh, SEO)"
    print(f"| Entities | {ent_status} | {missing_str} |")
    
    if pillar_status is None:
        print(f"| Pillar Link | ➖ | {pillar_details} |")
    elif pillar_status:
        print(f"| Pillar Link | ✅ | {pillar_details} |")
    else:
        print(f"| Pillar Link | ❌ | {pillar_details} |")
    
    aeo_pass = len(question_headings) >= 2
    aeo_status = "✅" if aeo_pass else "❌"
    qh_sample = question_headings[:5]
    print(f"| AEO/GEO | {aeo_status} | {len(question_headings)} question headings |")
    
    link_pass = len(all_internal) >= 3
    link_status = "✅" if link_pass else "❌"
    print(f"| Internal Links | {link_status} | {len(all_internal)} total ({len(blog_links)} blog, {len(services_links)} services, {len(locations_links)} locations) |")
    
    schema_pass = len(schema_missing) == 0
    schema_status = "✅" if schema_pass else "❌"
    schema_details = "All fields set" if schema_pass else f"Missing: {', '.join(schema_missing)}"
    print(f"| Schema Ready | {schema_status} | {schema_details} |")
    
    # Fix instructions
    print("\n### Fix instructions:")
    fixes = []
    if not tfidf_pass:
        fixes.append(f"- **TF-IDF**: Increase keyword \"{keyword}\" usage from {keyword_count} to ≥5")
    if not ent_pass:
        fixes.append(f"- **Entities**: Add missing: {', '.join(entities_missing)}")
    if pillar_status is not None and not pillar_status:
        fixes.append(f"- **Pillar Link**: Add link to {pillar_details.split(':')[-1].strip()}")
    if not aeo_pass:
        fixes.append(f"- **AEO/GEO**: Add ≥2 question headings (currently {len(question_headings)})")
    if not link_pass:
        fixes.append(f"- **Internal Links**: Add ≥3 internal links (currently {len(all_internal)})")
    if not schema_pass:
        fixes.append(f"- **Schema**: Add {', '.join(schema_missing)} fields")
    
    if not fixes:
        print("✅ **All checks passed**")
    else:
        for f in fixes:
            print(f)

print("\n\n" + "="*100)
print("BENGALI POSTS - INTERNAL LINK REMOVAL VERIFICATION")
print("="*100)

# Check which posts had the removed links STILL present
removed_links = [
    '/blog/seo-canonical-url-guide-bd',
    '/blog/google-search-console-performance-guide',
    '/blog/seo-structured-data-guide-bd',
    '/blog/schema-markup-rich-snippets-techniques',
    '/blog/seo-json-ld-schema-bangladesh',
    '/blog/seo-howto-schema-bangladesh'
]

for link in removed_links:
    link_short = link.split('/')[-1]
    found_in = []
    for p in post_data:
        if link in p.get('content', ''):
            found_in.append(p.get('slug', '?'))
    if found_in:
        print(f"\n🔴 **{link}** - STILL PRESENT in {len(found_in)} posts: {', '.join(found_in[:10])}")
    else:
        print(f"\n✅ **{link}** - Successfully removed from all posts")

print("\n\n" + "="*100)
print("GIT DIFF ANALYSIS - CATEGORIZING CHANGES")
print("="*100)

# Run git diff to see what changed
import subprocess
result = subprocess.run(
    ['git', 'diff', 'HEAD~3..HEAD', '--', 'src/app/blog/data.js'],
    capture_output=True, text=True, cwd='/root/kanok-miahit'
)
diff_text = result.stdout

# Categorize changes
blank_line_removals = len(re.findall(r'^-$', diff_text, re.MULTILINE))
blank_line_additions = len(re.findall(r'^\+$', diff_text, re.MULTILINE))

# Content changes (non-blank-line)
content_changes = 0
for line in diff_text.split('\n'):
    if line.startswith('-') and len(line.strip()) > 0 and line.strip() != '-':
        content_changes += 1
    elif line.startswith('+') and len(line.strip()) > 0 and line.strip() != '+':
        content_changes += 1

print(f"\nTotal diff size: {len(diff_text)} chars, {len(diff_text.split(chr(10)))} lines")
print(f"Blank line removals: ~{blank_line_removals}")
print(f"Content changes (non-blank): ~{content_changes}")

# Specific change types
homepage_link_adds = len(re.findall(r'^\+.*\[([^\]]+)\]\(/\)', diff_text))
link_removals = len(re.findall(r'^\-.*/blog/[a-z]', diff_text))
link_additions = len(re.findall(r'^\+.*/blog/[a-z]', diff_text))
entity_fixes = len(re.findall(r'&lt;|&gt;', diff_text))

print(f"Homepage link additions: ~{homepage_link_adds}")
print(f"Blog link removals: ~{link_removals}")
print(f"Blog link additions: ~{link_additions}")
print(f"HTML entity fixes: ~{entity_fixes}")
