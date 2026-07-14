#!/usr/bin/env python3
import re

with open('src/app/blog/data.js', 'r') as f:
    content = f.read()

post_blocks = re.split(r'\},\s*\n\s*\{', content)

def get_field(post_block, field_name):
    patterns = [
        rf'{field_name}:\s*"((?:[^"\\]|\\.)*)"',
        rf'{field_name}:\s*`((?:[^`\\]|\\.)*)`',
    ]
    for pat in patterns:
        m = re.search(pat, post_block, re.DOTALL)
        if m:
            return m.group(1)
    return None

def get_content_body(post_block):
    m = re.search(r'content:\s*`((?:[^`]|\\.)*)`', post_block, re.DOTALL)
    if m:
        return m.group(1)
    return None

def get_tags(post_block):
    m = re.search(r'tags:\s*\[(.*?)\]', post_block, re.DOTALL)
    if m:
        return [t.strip().strip('"') for t in m.group(1).split(',')]
    return []

def analyze_post(post_block):
    slug = get_field(post_block, 'slug')
    title = get_field(post_block, 'title')
    excerpt = get_field(post_block, 'excerpt')
    date_val = get_field(post_block, 'date')
    author = get_field(post_block, 'author')
    tags = get_tags(post_block)
    body = get_content_body(post_block)
    
    if not slug or not body:
        return None
    
    print(f"\n{'='*70}")
    print(f"## Post: {slug}")
    print(f"{'='*70}")
    print(f"Title: {title}")
    print(f"Date: {date_val}")
    print(f"Tags: {tags}")
    print(f"Content length: {len(body)} chars")
    
    # A. TF-IDF Coverage
    print(f"\n--- A. TF-IDF Coverage ---")
    # Determine primary keyword from title
    title_lower = title.lower() if title else ""
    
    # For locksmith post, primary keyword is "locksmith SEO" or "locksmith Dundee"
    kw_pairs = [
        ("locksmith", r'\blocksmith\b', 5),
        ("local SEO", r'local\s+SEO', 3),
        ("Google Business Profile", r'Google\s+Business\s+Profile|GBP', 2),
        ("Dundee", r'\bDundee\b', 3),
    ]
    
    for kw_name, kw_pattern, threshold in kw_pairs:
        count = len(re.findall(kw_pattern, body, re.IGNORECASE | re.DOTALL))
        status = "✅" if count >= threshold else "❌"
        print(f"{status} {kw_name}: {count} occurrences (threshold: {threshold})")
    
    # B. Semantic Entity Coverage
    print(f"\n--- B. Entity Coverage ---")
    required_entities = {
        "Dundee (location)": r'\bDundee\b',
        "Scotland (region)": r'\bScotland\b',
        "Google (search engine)": r'\bGoogle\b',
        "GBP / Google Business Profile": r'(GBP|Google\s+Business\s+Profile)',
        "Local citations": r'(citation|directory|listings?)',
        "Client reviews": r'(review|rating|5-star)',
        "Organic traffic/visitors": r'organic\s+(traffic|visitors?)',
        "Locksmith services": r'(emergency\s+locksmith|car\s+locksmith|lock\s+installation)',
    }
    
    missing = []
    for ent_name, ent_pattern in required_entities.items():
        found = bool(re.search(ent_pattern, body, re.IGNORECASE))
        status = "✅" if found else "❌"
        print(f"{status} {ent_name}")
        if not found:
            missing.append(ent_name)
    
    if not missing:
        print("   All required entities present!")
    
    # C. Pillar-Cluster Alignment
    print(f"\n--- C. Pillar-Cluster Alignment ---")
    blog_links = re.findall(r'/blog/[^"\')\s]+', body)
    service_links = re.findall(r'/services/[^"\')\s]+', body)
    industry_links = re.findall(r'/industries/[^"\')\s]+', body)
    all_internal_links = blog_links + service_links + industry_links
    
    print(f"Blog links ({len(blog_links)}): {blog_links}")
    print(f"Service links ({len(service_links)}): {service_links}")
    print(f"Industry links ({len(industry_links)}): {industry_links}")
    
    # Check if post links back to main site or relevant pillar content
    abs_links = re.findall(r'\]\(https?://kanokmiah[^\)]+\)', body)
    if abs_links:
        print(f"Absolute links to kanokmiah.com.bd: {len(abs_links)}")
    
    # D. AEO/GEO Optimization
    print(f"\n--- D. AEO/GEO: Question-Based Headings ---")
    heading_pattern = re.compile(r'^##+\s+(.+)$', re.MULTILINE)
    all_headings = heading_pattern.findall(body)
    
    question_starters = r'^(How|What|Why|When|Where|Can|Do|Is|Are|Does|Will|Should|Which)\b'
    q_headings = [h for h in all_headings if re.match(question_starters, h.strip(), re.IGNORECASE)]
    
    print(f"{'✅' if len(q_headings) >= 2 else '❌'} Found {len(q_headings)} question-based headings (need >= 2)")
    for h in q_headings:
        print(f"   - {h.strip()}")
    
    # E. Internal Linking
    print(f"\n--- E. Internal Links ---")
    print(f"{'✅' if len(all_internal_links) >= 3 else '❌'} Total internal links: {len(all_internal_links)} (need >= 3)")
    
    # F. Schema
    print(f"\n--- F. Schema Readiness ---")
    schema_ok = True
    if not title:
        print("❌ Title missing")
        schema_ok = False
    else:
        print(f"✅ Title set")
    if not excerpt:
        print("❌ Excerpt missing")
        schema_ok = False
    else:
        print(f"✅ Excerpt set")
    if not date_val:
        print("❌ Date missing")
        schema_ok = False
    else:
        print(f"✅ Date: {date_val}")
    if not author:
        print("❌ Author missing")
        schema_ok = False
    else:
        print(f"✅ Author set")
    
    if schema_ok:
        print("   All ArticleSchema fields present!")
    
    return {
        'slug': slug,
        'title': title,
        'tf_idf_passed': True,  # simplified
        'q_headings': len(q_headings),
        'internal_links': len(all_internal_links),
        'schema_ready': schema_ok,
        'missing_entities': missing,
    }

# Find and analyze both posts
for pb in post_blocks:
    slug = get_field(pb, 'slug')
    if slug in ['why-md-kanok-miah-is-the-best-seo-expert-in-dhaka-bangladesh', 'locksmith-dundee-seo-case-study']:
        analyze_post(pb)
