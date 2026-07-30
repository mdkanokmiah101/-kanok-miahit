#!/usr/bin/env python3
"""Extract changed posts from data.js and run framework checks."""
import re, json, sys
from collections import Counter

with open('src/app/blog/data.js') as f:
    content = f.read()

# Slugs modified in the last 48 hours
changed_slugs = [
    "link-building-strategies-bangladesh-market",
    "seo-garments-textile-industry-b2b-lead-generation",
    "google-business-profile-optimization-guide-bangladesh",
    "mobile-seo-optimization-bangladesh-mobile-first-era",
    "why-md-kanok-miah-is-the-best-seo-expert-in-dhaka-bangladesh",
    "landlord-certificates-seo-case-study",
    "das-taxis-scotland-seo-case-study",
    "morethanpanel-seo-case-study",
    "smmgen-seo-case-study",
    "smmsun-seo-case-study",
    "mir-cement-seo-case-study",
    "dhaka-apparels-seo-case-study",
    "stealth-windshield-repairs-seo-case-study",
    "how-to-choose-best-seo-expert-dhaka-15-things",
    "seo-expert-vs-seo-agency-dhaka-which-is-right",
    "top-10-seo-mistakes-dhaka-businesses-fix",
    "what-does-seo-expert-do-guide-business-owners",
    "seo-case-study-dhaka-businesses-increased-organic-traffic",
    "hiring-seo-expert-dhaka-better-roi-than-paid-ads",
    "ai-seo-2026-dhaka-experts-optimize-google-ai-chatgpt",
]

# Parse all posts
pattern = re.compile(r'{\s*\n\s*slug:\s*"([^"]+)"')
matches = list(pattern.finditer(content))

all_posts = {}
for i, m in enumerate(matches):
    slug = m.group(1)
    start = m.start()
    if i + 1 < len(matches):
        end = matches[i+1].start() - 1
    else:
        end = content.rfind('];')
        if end == -1:
            end = len(content)
    
    post_text = content[start:end]
    
    title_m = re.search(r'title:\s*"([^"]+)"', post_text)
    title = title_m.group(1) if title_m else ''
    
    date_m = re.search(r'date:\s*"([^"]+)"', post_text)
    date = date_m.group(1) if date_m else ''
    
    excerpt_m = re.search(r'excerpt:\s*"([^"]+)"', post_text)
    excerpt = excerpt_m.group(1) if excerpt_m else ''
    
    tags_m = re.search(r'tags:\s*\[(.*?)\]', post_text, re.DOTALL)
    tags = re.findall(r'"([^"]+)"', tags_m.group(1)) if tags_m else []
    
    content_m = re.search(r'content:\s*`([^`]+)`', post_text)
    post_content = content_m.group(1) if content_m else ''
    
    all_posts[slug] = {
        'slug': slug,
        'title': title,
        'date': date,
        'excerpt': excerpt,
        'tags': tags,
        'content': post_content,
    }

print(f"Total posts in data.js: {len(all_posts)}")
print(f"Changed slugs to check: {len(changed_slugs)}")
print()

# Now run framework checks on each changed post
for slug in changed_slugs:
    if slug not in all_posts:
        print(f"WARNING: Slug '{slug}' not found!")
        continue
    
    post = all_posts[slug]
    title = post['title']
    content_text = post['content']
    tags = post['tags']
    excerpt = post['excerpt']
    date = post['date']
    
    print(f"{'='*70}")
    print(f"## Post: {slug}")
    print(f"Title: {title}")
    print(f"{'='*70}")
    
    # --- A. TF-IDF Coverage ---
    # Extract primary keyword from title (first meaningful noun phrase)
    # Simple: take the first 1-3 words that aren't stop words
    stop_words = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'how', 'what', 'why', 'when', 'where', 'to', 'for', 'of', 'in', 'on', 'at', 'by', 'with', 'from', 'and', 'or', 'but', 'your', 'our', 'its', 'their'}
    title_words = title.lower().split()
    keyword_parts = []
    for w in title_words:
        w_clean = w.strip('?:!,.;\'"()-')
        if w_clean and w_clean not in stop_words:
            keyword_parts.append(w_clean)
    
    # Try 2-word and 3-word phrases
    keyword = None
    keyword_count = 0
    for n in [3, 2, 1]:
        if len(keyword_parts) >= n:
            phrase = ' '.join(keyword_parts[:n])
            count = len(re.findall(re.escape(phrase), content_text.lower()))
            if count >= 3:
                keyword = phrase
                keyword_count = count
                break
    if not keyword and keyword_parts:
        keyword = keyword_parts[0]
        keyword_count = len(re.findall(re.escape(keyword), content_text.lower()))
    
    tfidf_status = "✅" if keyword_count >= 5 else "❌"
    print(f"\n### A. TF-IDF Coverage")
    print(f"Primary keyword: '{keyword}'")
    print(f"Occurrences in content: {keyword_count}")
    print(f"Status: {tfidf_status}")
    
    # --- B. Semantic Entity Coverage ---
    entities_to_check = []
    locations = ['dhaka', 'bangladesh', 'bangladeshi']
    # Check title for context
    title_lower = title.lower()
    if 'seo' in title_lower:
        entities_to_check.append('SEO')
    if 'local' in title_lower or 'maps' in title_lower:
        entities_to_check.append('local')
    if any(x in content_text.lower() for x in ['service', 'agency', 'consultant', 'expert']):
        entities_to_check.append('service type')
    if 'case study' in title_lower:
        entities_to_check.append('case study client/industry')
    
    # Check specific entities
    content_lower = content_text.lower()
    missing_entities = []
    
    # Location: Dhaka
    if 'dhaka' not in content_lower:
        missing_entities.append('Dhaka')
    # Location: Bangladesh
    if 'bangladesh' not in content_lower and 'bangladeshi' not in content_lower:
        missing_entities.append('Bangladesh')
    
    # Service type entities
    service_entities = {
        'local seo': 'local seo' in content_lower,
        'technical seo': 'technical seo' in content_lower,
        'on-page seo': 'on-page seo' in content_lower or 'on page seo' in content_lower,
        'off-page seo': 'off-page seo' in content_lower or 'off page seo' in content_lower,
        'ecommerce seo': 'ecommerce seo' in content_lower or 'e-commerce seo' in content_lower,
        'link building': 'link building' in content_lower,
        'content marketing': 'content marketing' in content_lower,
        'keyword research': 'keyword research' in content_lower,
        'google business profile': 'google business profile' in content_lower or 'gbp' in content_lower,
    }
    present_services = [k for k, v in service_entities.items() if v]
    
    entity_status = "✅"
    entity_details = []
    if missing_entities:
        entity_status = "❌"
        entity_details.append(f"Missing locations: {', '.join(missing_entities)}")
    if not present_services:
        entity_status = "❌"
        entity_details.append("No service entities found")
    else:
        entity_details.append(f"Services: {', '.join(present_services[:5])}")
    
    print(f"\n### B. Entity Coverage")
    print(f"Locations: {'✅ Dhaka' if 'dhaka' in content_lower else '❌ Dhaka'}, {'✅ Bangladesh' if 'bangladesh' in content_lower or 'bangladeshi' in content_lower else '❌ Bangladesh'}")
    print(f"Service entities found: {', '.join(present_services) if present_services else '❌ None'}")
    print(f"Status: {entity_status}")
    if missing_entities:
        print(f"Missing: {', '.join(missing_entities)}")
    
    # --- C. Pillar-Cluster Alignment ---
    pillar_pages = {
        'local-seo': ['local seo', 'google maps', 'local search', 'gbp', 'google business profile', 'near me'],
        'technical-seo': ['technical seo', 'core web vitals', 'page speed', 'crawl', 'index', 'schema', 'structured data'],
        'on-page-seo': ['on-page seo', 'meta', 'heading', 'content optimization', 'keyword research'],
        'ecommerce-seo': ['ecommerce', 'e-commerce', 'online store', 'shop', 'product'],
        'link-building': ['link building', 'backlink', 'guest post', 'outreach'],
        'seo-strategy': ['seo strategy', 'pillar', 'cluster', 'topical authority', 'content strategy'],
        'local-seo-guide': ['local seo', 'google maps', 'local business'],
        'seo-guide': ['complete seo', 'beginner', 'guide'],
    }
    
    # Determine pillar based on tags and content
    tag_lower = [t.lower() for t in tags]
    
    # Check if post links to any pillar page
    pillar_links = {
        '/services/local-seo': 'local seo' in content_lower,
        '/services/technical-seo': 'technical seo' in content_lower,
        '/services/on-page-seo': 'on page seo' in content_lower or 'on-page seo' in content_lower,
        '/services/ecommerce-seo': 'ecommerce seo' in content_lower or 'e-commerce seo' in content_lower,
        '/services/seo-audit': 'seo audit' in content_lower,
        '/services/seo-strategy': 'seo strategy' in content_lower or 'seo strateg' in content_lower,
    }
    actual_pillar_links = [k for k, v in pillar_links.items() if v]
    
    # Check if post explicitly links to /services/ pages
    explicit_pillar_link = re.search(r'/services/\w+', content_text)
    
    pillar_status = "✅" if explicit_pillar_link else "❌"
    
    print(f"\n### C. Pillar-Cluster Alignment")
    print(f"Tags: {tags}")
    print(f"Pillar link found: {'✅' if explicit_pillar_link else '❌'} - {'yes' if explicit_pillar_link else 'no explicit /services/ link'}")
    print(f"Status: {pillar_status}")
    if explicit_pillar_link:
        print(f"Links to: {explicit_pillar_link.group(0)}")
    
    # --- D. AEO/GEO Optimization ---
    q_headers = re.findall(r'^#{1,6}\s+(How|What|Why|When|Where|Can|Do|Is|Are|Which|Who|Whom|Whose)\b', content_text, re.MULTILINE)
    q_count = len(q_headers)
    aeo_status = "✅" if q_count >= 2 else "❌"
    
    print(f"\n### D. AEO/GEO (Question Headings)")
    print(f"Question-based headings: {q_count}")
    if q_headers:
        print(f"Questions: {', '.join(q_headers[:10])}")
    print(f"Status: {aeo_status}")
    
    # --- E. Internal Linking ---
    # Count internal links to other posts, services, locations
    internal_links = re.findall(r'\((/[^)]+)\)', content_text)
    # Filter for meaningful internal links (blog posts, services, locations)
    meaningful_links = [l for l in internal_links if any(l.startswith(p) for p in ['/blog/', '/services/', '/locations/', '/industries/', '/about', '/contact', '/'])]
    # Remove duplicates
    unique_links = list(set(meaningful_links))
    
    # Count explicit markdown links (not just bare paths)
    markdown_links = re.findall(r'\[([^\]]+)\]\((/[^)]+)\)', content_text)
    service_links = [l for l in markdown_links if l[1].startswith('/services/')]
    blog_links = [l for l in markdown_links if l[1].startswith('/blog/')]
    location_links = [l for l in markdown_links if l[1].startswith('/locations/')]
    
    total_internal = len(markdown_links)
    internal_status = "✅" if total_internal >= 3 else "❌"
    
    print(f"\n### E. Internal Linking")
    print(f"Total internal links (markdown): {total_internal}")
    print(f"  Service links: {len(service_links)}")
    print(f"  Blog links: {len(blog_links)}")
    print(f"  Location links: {len(location_links)}")
    print(f"Status: {internal_status}")
    
    # --- F. Schema Readiness ---
    schema_fields = {
        'title': bool(title and title != 'N/A'),
        'excerpt': bool(excerpt and excerpt != 'N/A'),
        'date': bool(date and date != 'N/A'),
    }
    all_fields_set = all(schema_fields.values())
    schema_status = "✅" if all_fields_set else "❌"
    
    print(f"\n### F. Schema Readiness")
    for field, present in schema_fields.items():
        print(f"  {field}: {'✅' if present else '❌'}")
    print(f"Status: {schema_status}")
    
    print()
    print("---")
    print()

# Print summary table at the end
print(f"\n\n{'='*80}")
print("SUMMARY TABLE")
print(f"{'='*80}")
print(f"{'Post':<55} {'TF-IDF':<8} {'Entity':<8} {'Pillar':<8} {'AEO/GEO':<8} {'IntLinks':<8} {'Schema':<8}")
print(f"{'-'*55} {'-'*8} {'-'*8} {'-'*8} {'-'*8} {'-'*8} {'-'*8}")
