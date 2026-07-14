#!/usr/bin/env python3
import re, json

with open('src/app/blog/data.js', 'r') as f:
    content = f.read()

# Split by slug pattern to find posts
all_slugs = re.findall(r'slug:\s*"([^"]+)"', content)
print(f"Total posts in file: {len(all_slugs)}")

# The posts are separated by "},\n  {" patterns
# Let's find each post block
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
    # Extract primary keyword from title (first meaningful noun phrase)
    title_lower = title.lower() if title else ""
    # Remove common prefixes
    words = title_lower.replace('?', '').replace(',', '').split()
    # Look for meaningful keyword phrase - take the main topic
    # For "Why MD Kanok Miah is the best SEO expert in Dhaka, Bangladesh"
    # Keywords: SEO expert, best SEO expert, Dhaka SEO
    
    # Count various keyword patterns
    kw_pairs = [
        ("SEO expert", rf'SEO\s+expert', 5),
        ("best SEO expert", rf'best\s+SEO\s+expert', 3),
        ("SEO in Dhaka", rf'SEO[^.]*?Dhaka', 2),
        ("Dhaka SEO", rf'Dhaka[^.]*?SEO', 2),
        ("SEO", rf'\bSEO\b', 10),
    ]
    
    for kw_name, kw_pattern, threshold in kw_pairs:
        count = len(re.findall(kw_pattern, body, re.IGNORECASE | re.DOTALL))
        status = "✅" if count >= threshold else "❌"
        print(f"{status} {kw_name}: {count} occurrences (threshold: {threshold})")
    
    # B. Semantic Entity Coverage
    print(f"\n--- B. Entity Coverage ---")
    required_entities = {
        "Dhaka (city)": r'\bDhaka\b',
        "Bangladesh (country)": r'\bBangladesh\b',
        "Google (search engine)": r'\bGoogle\b',
        "Local SEO / GBP": r'(GBP|Google\s+Business\s+Profile|local\s+SEO)',
        "Organic search": r'organic\s+(search|traffic|visitors?)',
        "Client reviews/ratings": r'(review|rating|4\.9|5-star)',
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
    
    # Check pillar link - this post needs to link to the main pillar topic
    # Based on tags, determine pillar topic
    if any('SEO' in t for t in tags):
        pillar_marker = 'seo-guide-bangladesh'  # Main SEO guide pillar
        has_pillar_link = any(pillar_marker in link for link in blog_links)
        print(f"{'✅' if has_pillar_link else '❌'} Pillar link to 'complete-seo-guide-bangladesh-businesses-2026': {has_pillar_link}")
    
    # D. AEO/GEO Optimization
    print(f"\n--- D. AEO/GEO: Question-Based Headings ---")
    # Find markdown headings (## ...)
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
        print(f"✅ Title: '{title[:60]}...'")
    if not excerpt:
        print("❌ Excerpt missing")
        schema_ok = False
    else:
        print(f"✅ Excerpt: '{excerpt[:60]}...'")
    if not date_val:
        print("❌ Date missing")
        schema_ok = False
    else:
        print(f"✅ Date: {date_val}")
    if not author:
        print("❌ Author missing")
        schema_ok = False
    else:
        print(f"✅ Author: {author}")
    
    if schema_ok:
        print("   All ArticleSchema fields present!")
    
    return {
        'slug': slug,
        'title': title,
        'tags': tags,
        'tf_idf': kw_pairs,
        'entities': required_entities,
        'missing_entities': missing,
        'question_headings': len(q_headings),
        'q_heading_list': q_headings,
        'internal_links_count': len(all_internal_links),
        'internal_links': all_internal_links,
        'schema_ready': schema_ok,
    }

# Analyze the specific post
idx = 0
for pb in post_blocks:
    slug = get_field(pb, 'slug')
    if slug and slug == 'why-md-kanok-miah-is-the-best-seo-expert-in-dhaka-bangladesh':
        result = analyze_post(pb)
        break
