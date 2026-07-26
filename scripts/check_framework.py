#!/usr/bin/env python3
"""
Content Framework Enforcer for kanokmiah.com.bd
Checks each blog post against the 6-point content framework.
"""

import re
import json
import sys

# Read the data.js file
with open('/root/kanok-miahit/src/app/blog/data.js', 'r') as f:
    content = f.read()

# Parse out each post using regex
# Posts are objects in the posts array
post_pattern = re.compile(
    r'\{[^}]*slug:\s*"([^"]+)"[^}]*title:\s*"([^"]*)"[^}]*date:\s*"([^"]*)"[^}]*excerpt:\s*"([^"]*)"[^}]*tags:\s*\[([^\]]*)\][^}]*content:\s*`([^`]*)`',
    re.DOTALL
)

# Alternative: split by slug and extract manually
# Let me use a simpler approach
posts_raw = re.findall(r'\{[^{}]*slug:\s*"([^"]+)"[^{}]*\}', content)
print(f"Found {len(posts_raw)} posts via regex", file=sys.stderr)

# Better approach: parse slug by slug
slug_positions = []
for m in re.finditer(r'slug:\s*"([^"]+)"', content):
    slug_positions.append((m.start(), m.group(1)))

print(f"Found {len(slug_positions)} slugs", file=sys.stderr)

# Get post boundaries: each post starts with `{` and ends with `},`
# Let's extract each post section
post_sections = []
for i, (pos, slug) in enumerate(slug_positions):
    # Find the start of this post object
    start = content.rfind('{', 0, pos)
    if start == -1:
        continue
    
    # Find the end of this post object (the matching `},` or `]` for the last one)
    if i < len(slug_positions) - 1:
        next_pos = slug_positions[i+1][0]
        # Find the `},` before the next slug
        end_match = content.rfind('},', pos, next_pos)
        if end_match == -1:
            end_match = content.rfind('`,\n  {', pos, next_pos)
        if end_match == -1:
            end = next_pos
        else:
            end = end_match + 2
    else:
        # Last post - find the closing
        end = content.find('\n];', pos)
        if end == -1:
            end = len(content)
    
    post_text = content[start:end]
    post_sections.append((slug, start, end, post_text))

# For each post, extract the full data including content inside backticks
# Let me use a more robust approach
posts = []
# Find all post objects
pattern = re.compile(
    r'\{[\s\S]*?slug:\s*"([^"]+)"[\s\S]*?title:\s*"([^"]*)"[\s\S]*?date:\s*"([^"]*)"[\s\S]*?excerpt:\s*"([^"]*)"[\s\S]*?tags:\s*\[([^\]]*)\][\s\S]*?content:\s*`\n?([\s\S]*?)`\s*,',
    re.DOTALL
)

matches = list(pattern.finditer(content))
print(f"Parsed {len(matches)} posts with full content", file=sys.stderr)

results = []

for m in matches[:]:  # Use all posts
    slug = m.group(1)
    title = m.group(2)
    date = m.group(3)
    excerpt = m.group(4)
    tags_str = m.group(5)
    post_content = m.group(6)
    
    tags = [t.strip().strip('"') for t in tags_str.split(',') if t.strip()]
    
    # ============ A. TF-IDF Coverage ============
    # Extract primary keyword from title (first meaningful noun phrase)
    title_lower = title.lower()
    # Remove "Complete", "Guide", "for", "in", "the", "a", "an" etc. at start to find the main topic
    stop_words = {'complete', 'guide', 'for', 'the', 'a', 'an', 'in', 'to', 'of', 'is', 'what', 'how', 'why', 'when', 'where', 'best', 'top', 'ultimate', 'essential', 'comprehensive', 'your', 'our'}
    
    # Extract meaningful words from title
    title_words = [w for w in title_lower.split() if w not in stop_words and len(w) > 2]
    
    # Pick primary keyword: first 2-3 meaningful words
    if len(title_words) >= 3:
        primary_kw = ' '.join(title_words[:3])
    elif len(title_words) >= 2:
        primary_kw = ' '.join(title_words[:2])
    elif len(title_words) >= 1:
        primary_kw = title_words[0]
    else:
        primary_kw = title_lower
    
    # Special case: if title starts with a question word, use the noun phrase after it
    question_starts = ['what is', 'what are', 'how to', 'how do', 'why is', 'why does']
    for qs in question_starts:
        if title_lower.startswith(qs):
            remainder = title_lower[len(qs):].strip()
            words = [w for w in remainder.split() if w not in stop_words and len(w) > 2]
            if words:
                primary_kw = ' '.join(words[:3]) if len(words) >= 3 else ' '.join(words[:2])
            break
    
    # Also check for SEO-related keywords - use the first prominent topic
    # Count occurrences
    kw_lower = primary_kw.lower()
    count = post_content.lower().count(kw_lower)
    
    tfidf_status = "✅" if count >= 5 else "❌"
    tfidf_detail = f"'{primary_kw}' → {count} occurrences"
    
    # ============ B. Semantic Entity Coverage ============
    required_entities = [
        ("location_dhaka", "Dhaka"),
        ("location_bangladesh", "Bangladesh"),
        ("service_seo", "SEO"),
    ]
    
    # Check tags for industry hints
    has_ecommerce = any('ecommerce' in t.lower() or 'shopify' in t.lower() or 'daraz' in t.lower() for t in tags)
    has_local = any('local' in t.lower() for t in tags)
    has_technical = any('technical' in t.lower() for t in tags)
    has_realestate = any('real estate' in t.lower() for t in tags)
    has_healthcare = any('healthcare' in t.lower() or 'medical' in t.lower() or 'clinic' in t.lower() for t in tags)
    has_education = any('education' in t.lower() for t in tags)
    has_hotel = any('hotel' in t.lower() or 'resort' in t.lower() or 'travel' in t.lower() or 'tourism' in t.lower() for t in tags)
    has_garment = any('garment' in t.lower() or 'textile' in t.lower() for t in tags)
    has_bangla = any('bangla' in t.lower() or 'বাংলা' in t.lower() for t in tags)
    has_linkbuilding = any('link building' in t.lower() or 'backlink' in t.lower() for t in tags)
    has_mobile = any('mobile' in t.lower() for t in tags)
    has_content = any('content' in t.lower() for t in tags)
    has_restaurant = any('restaurant' in t.lower() or 'cafe' in t.lower() or 'food' in t.lower() for t in tags)
    has_cleaning = any('cleaning' in t.lower() for t in tags)
    has_ngo = any('ngo' in t.lower() or 'non-profit' in t.lower() or 'nonprofit' in t.lower() for t in tags)
    has_law = any('law' in t.lower() or 'legal' in t.lower() or 'firm' in t.lower() for t in tags)
    has_fitness = any('fitness' in t.lower() or 'gym' in t.lower() for t in tags)
    has_startup = any('startup' in t.lower() for t in tags)
    has_photography = any('photographer' in t.lower() or 'videographer' in t.lower() for t in tags)
    has_wedding = any('wedding' in t.lower() or 'event' in t.lower() for t in tags)
    has_b2b = any('b2b' in t.lower() or 'lead generation' in t.lower() for t in tags)
    has_schema = any('schema' in t.lower() or 'structured data' in t.lower() for t in tags)
    has_voice = any('voice' in t.lower() for t in tags)
    has_case_study = 'case-study' in slug
    
    # Check entities present
    content_lower = post_content.lower()
    
    missing_entities = []
    
    if not has_bangla:
        if 'dhaka' not in content_lower:
            missing_entities.append("Dhaka")
        if 'bangladesh' not in content_lower:
            missing_entities.append("Bangladesh")
    
    if 'seo' not in content_lower:
        missing_entities.append("SEO (service)")
    
    # Industry-specific entities
    if has_ecommerce and 'e-commerce' not in content_lower and 'ecommerce' not in content_lower and 'online store' not in content_lower:
        missing_entities.append("e-commerce (industry)")
    if has_local and ('local seo' not in content_lower) and ('google maps' not in content_lower) and ('google business profile' not in content_lower):
        missing_entities.append("local SEO / GBP")
    if has_technical and ('technical seo' not in content_lower) and ('core web vitals' not in content_lower):
        missing_entities.append("technical SEO / Core Web Vitals")
    if has_garment and ('garment' not in content_lower and 'textile' not in content_lower):
        missing_entities.append("garment/textile (industry)")
    if has_restaurant and ('restaurant' not in content_lower and 'cafe' not in content_lower and 'food' not in content_lower):
        missing_entities.append("restaurant/food (industry)")
    if has_healthcare and ('healthcare' not in content_lower and 'medical' not in content_lower and 'clinic' not in content_lower and 'doctor' not in content_lower):
        missing_entities.append("healthcare/medical (industry)")
    if has_education and ('education' not in content_lower and 'school' not in content_lower and 'university' not in content_lower and 'student' not in content_lower and 'educational' not in content_lower):
        missing_entities.append("education (industry)")
    if has_realestate and ('real estate' not in content_lower and 'property' not in content_lower and 'developer' not in content_lower):
        missing_entities.append("real estate (industry)")
    if has_hotel and ('hotel' not in content_lower and 'resort' not in content_lower and 'travel' not in content_lower and 'tourism' not in content_lower):
        missing_entities.append("hotel/travel (industry)")
    if has_linkbuilding and ('link building' not in content_lower and 'backlink' not in content_lower):
        missing_entities.append("link building/backlinks")
    if has_mobile and ('mobile seo' not in content_lower and 'mobile optimization' not in content_lower):
        missing_entities.append("mobile SEO")
    if has_content and ('content marketing' not in content_lower and 'content strategy' not in content_lower):
        missing_entities.append("content marketing (method)")
    if has_cleaning and ('cleaning' not in content_lower):
        missing_entities.append("cleaning (industry)")
    if has_ngo and ('ngo' not in content_lower and 'non-profit' not in content_lower and 'nonprofit' not in content_lower and 'charity' not in content_lower and 'social' not in content_lower):
        missing_entities.append("NGO/non-profit (industry)")
    if has_law and ('law' not in content_lower and 'legal' not in content_lower and 'attorney' not in content_lower and 'lawyer' not in content_lower and 'firm' not in content_lower):
        missing_entities.append("legal/law (industry)")
    if has_fitness and ('fitness' not in content_lower and 'gym' not in content_lower and 'workout' not in content_lower):
        missing_entities.append("fitness/gym (industry)")
    if has_startup and ('startup' not in content_lower):
        missing_entities.append("startup (industry)")
    if has_photography and ('photographer' not in content_lower and 'photography' not in content_lower and 'videographer' not in content_lower):
        missing_entities.append("photography (industry)")
    if has_wedding and ('wedding' not in content_lower and 'event' not in content_lower and 'planner' not in content_lower):
        missing_entities.append("wedding/event (industry)")
    if has_b2b and ('b2b' not in content_lower and 'lead generation' not in content_lower):
        missing_entities.append("B2B/lead generation")
    if has_schema and ('schema' not in content_lower and 'structured data' not in content_lower and 'rich snippet' not in content_lower):
        missing_entities.append("schema/structured data")
    if has_voice and ('voice search' not in content_lower and 'voice' not in content_lower):
        missing_entities.append("voice search")
    
    entities_status = "✅" if len(missing_entities) == 0 else "❌"
    entities_detail = f"Missing: {', '.join(missing_entities)}" if missing_entities else "All key entities present"
    
    # ============ C. Pillar-Cluster Alignment ============
    pillar_pages = [
        "/blog/complete-seo-guide-bangladesh-businesses-2026",
        "/services/seo",
        "/services/local-seo",
        "/services/technical-seo",
        "/services/seo-consulting",
    ]
    
    has_pillar_link = any(f'({p}' in post_content or f'href="{p}' in post_content for p in pillar_pages)
    
    # Check if it links to its pillar based on tags
    pillar_link_status = "✅" if has_pillar_link else "❌"
    pillar_link_detail = "No pillar link found" if not has_pillar_link else "Links to pillar page"
    
    # ============ D. AEO/GEO Optimization ============
    question_heads = re.findall(r'^#{1,3}\s+(How\s|What\s|Why\s|When\s|Where\s|Can\s|Do\s|Is\s|Are\s|Does\s|Which\s|Who\s)', post_content, re.MULTILINE)
    num_question_heads = len(question_heads)
    
    aeo_status = "✅" if num_question_heads >= 2 else "❌"
    aeo_detail = f"{num_question_heads} question headings"
    
    # ============ E. Internal Linking ============
    # Count internal links (links starting with /)
    internal_links = re.findall(r'\(/(?:blog/|services/|locations/|industries/|about|contact|/)[^)]*\)', post_content)
    # Filter for actual links to other posts/pages (not self-references)
    self_link = f'/blog/{slug}'
    meaningful_links = [l for l in internal_links if self_link not in l]
    
    internal_links_status = "✅" if len(meaningful_links) >= 3 else "❌"
    internal_links_detail = f"{len(meaningful_links)} internal links"
    
    # ============ F. Schema Readiness ============
    schema_missing = []
    if not title:
        schema_missing.append("title")
    if not excerpt:
        schema_missing.append("excerpt")
    if not date:
        schema_missing.append("date")
    
    schema_status = "✅" if len(schema_missing) == 0 else "❌"
    schema_detail = f"Missing: {', '.join(schema_missing)}" if schema_missing else "All fields set"
    
    # ============ Assemble Result ============
    results.append({
        'slug': slug,
        'title': title,
        'checks': {
            'TF-IDF': {'status': tfidf_status, 'detail': tfidf_detail},
            'Entities': {'status': entities_status, 'detail': entities_detail},
            'Pillar Link': {'status': pillar_link_status, 'detail': pillar_link_detail},
            'AEO/GEO': {'status': aeo_status, 'detail': aeo_detail},
            'Internal Links': {'status': internal_links_status, 'detail': internal_links_detail},
            'Schema Ready': {'status': schema_status, 'detail': schema_detail},
        }
    })

# Output as JSON
print(json.dumps(results, indent=2))
