#!/usr/bin/env python3
"""Analyze blog posts for content framework compliance."""
import re, json

# Read the data file
with open('/root/kanok-miahit/src/app/blog/data.js', 'r') as f:
    content = f.read()

# Extract posts array - find the const posts = [ ... ];
match = re.search(r'const posts = \[(.*?)\];', content, re.DOTALL)
if not match:
    # Try without const
    match = re.search(r'posts = \[(.*?)\];', content, re.DOTALL)
if not match:
    # Just find the array
    start = content.find('[')
    end = content.rfind('];') + 1
    match = content[start:end]

# Since the file is massive and the array is complex, let me extract individual posts by slug
posts_to_check = [
    "seo-for-fitness-gyms-bangladesh",
    "seo-for-law-firms-bangladesh", 
    "seo-https-ssl-impact-bangladesh",
    "b2b-lead-generation-seo-bangladesh",
    "seo-for-startups-bangladesh"
]

def extract_post_by_slug(full_text, slug):
    """Extract a single post object text from the JS array."""
    # Find the slug
    slug_pattern = rf'slug: "{re.escape(slug)}"'
    slug_match = re.search(slug_pattern, full_text)
    if not slug_match:
        return None
    
    # Find the start of this post object - go back to find the opening {
    pos = slug_match.start()
    # Go back to find the opening {
    while pos > 0 and full_text[pos] != '{':
        pos -= 1
        if pos < 0:
            return None
    
    # Now find the closing } that ends this post
    # Need to handle nested braces properly
    depth = 0
    end_pos = pos
    in_content = False
    content_delim = None
    
    i = pos
    while i < len(full_text):
        ch = full_text[i]
        
        # Handle template literals (backtick strings)
        if ch == '`':
            if not in_content:
                in_content = True
                content_delim = '`'
            elif content_delim == '`':
                # Check if it's escaped
                if i > 0 and full_text[i-1] != '\\':
                    in_content = False
                    content_delim = None
        
        if not in_content:
            if ch == '{':
                depth += 1
            elif ch == '}':
                depth -= 1
                if depth == 0:
                    end_pos = i + 1
                    break
        i += 1
    
    return pos, end_pos, full_text[pos:end_pos]

def analyze_post(slug, full_text):
    result = extract_post_by_slug(full_text, slug)
    if not result:
        return {"error": f"Post {slug} not found"}
    
    start, end, post_text = result
    
    # Extract metadata fields
    def extract_field(pattern, text=post_text):
        m = re.search(pattern, text, re.DOTALL)
        return m.group(1).strip() if m else None
    
    title = extract_field(r'title:\s*"([^"]+)"')
    date = extract_field(r'date:\s*"([^"]+)"')
    excerpt = extract_field(r'excerpt:\s*"([^"]+)"', post_text)
    if not excerpt:
        excerpt = extract_field(r'excerpt:\s*\n\s*"([^"]+)"', post_text)
    
    tags_match = re.search(r'tags:\s*\[(.*?)\]', post_text, re.DOTALL)
    tags = []
    if tags_match:
        tags = re.findall(r'"([^"]+)"', tags_match.group(1))
    
    metaTitle = extract_field(r'metaTitle:\s*"([^"]+)"')
    metaDescription = extract_field(r'metaDescription:\s*"([^"]+)"')
    dateModified = extract_field(r'dateModified:\s*"([^"]+)"')
    
    # Extract content (the big backtick string)
    content_match = re.search(r'content:\s*`\n?(.*?)`\s*,?\s*\}', post_text, re.DOTALL)
    body = content_match.group(1) if content_match else ""
    
    # A. TF-IDF: Extract primary keyword from title
    # First meaningful noun phrase
    title_lower = title.lower() if title else ""
    # Remove "seo for", "a", "the", etc.
    keyword = None
    if "seo for" in title_lower:
        keyword = title_lower.split("seo for")[1].split("in")[0].split(":")[0].strip()
    elif "through" in title_lower:
        parts = title_lower.split("through")
        keyword = parts[0].strip() if len(parts) > 1 else title_lower
    else:
        keyword = title_lower.replace("seo", "").strip()
        # Take first meaningful part
        parts = keyword.split()
        keyword = " ".join(parts[:3]) if len(parts) > 3 else keyword
    
    # Also try extracting the main subject
    # For "SEO for Fitness and Gym Businesses in Bangladesh" -> "fitness gym"
    # For "SEO for Law Firms and Legal Services in Bangladesh" -> "law firms"
    # For "B2B Lead Generation through SEO in Bangladesh" -> "b2b lead generation"
    
    primary_keyword_parts = []
    if "seo for" in title_lower:
        after_seo = title_lower.split("seo for")[1].strip()
        if " in " in after_seo:
            after_seo = after_seo.split(" in ")[0].strip()
        if ":" in after_seo:
            after_seo = after_seo.split(":")[0].strip()
        primary_keyword_parts = [w for w in after_seo.split() if w not in ["and", "a", "the", "an"]]
    
    primary_keyword = " ".join(primary_keyword_parts) if primary_keyword_parts else title_lower
    
    # Count occurrences of keyword parts in the body
    body_lower = body.lower()
    kw_count = 0
    for kw_part in primary_keyword_parts[:3]:  # Use top 3 meaningful words
        count = body_lower.count(kw_part)
        kw_count += count
    
    # B. Semantic Entity Coverage
    entities = {
        "Dhaka": "dhaka" in body_lower,
        "Bangladesh": "bangladesh" in body_lower,
        "Chittagong": "chittagong" in body_lower or "চট্টগ্রাম" in body,
    }
    
    missing_entities = [k for k, v in entities.items() if not v]
    
    # Check for main service-type entity
    if "fitness" in slug:
        entities["Gym/Fitness"] = "gym" in body_lower or "fitness" in body_lower
    elif "law" in slug:
        entities["Law/Legal"] = "law" in body_lower or "legal" in body_lower
    elif "b2b" in slug:
        entities["B2B/Lead Gen"] = "b2b" in body_lower or "lead generation" in body_lower or "লিড" in body
    elif "startup" in slug:
        entities["Startup"] = "startup" in body_lower or "startups" in body_lower or "স্টার্টআপ" in body
    elif "https" in slug:
        entities["HTTPS/SSL"] = "https" in body_lower or "ssl" in body_lower
    
    all_missing = [k for k, v in entities.items() if not v]
    
    # C. Pillar-Cluster Alignment - check for links to pillar pages
    pillar_links = []
    pillar_patterns = [
        r'/services\b', r'/industries\b', r'/locations\b',
        r'/about\b', r'/blog/\w+'
    ]
    for pattern in pillar_patterns:
        if re.search(pattern, body):
            pillar_links.append(pattern)
    
    has_pillar_link = len(pillar_links) > 0
    
    # Check if links to specific related blog posts
    blog_links = re.findall(r'/blog/([^"\'\)\s]+)', body)
    
    # D. AEO/GEO - count question headings
    question_heading_patterns = [
        r'#{1,3}\s+(How\s.+)',
        r'#{1,3}\s+(What\s.+)',
        r'#{1,3}\s+(Why\s.+)',
        r'#{1,3}\s+(When\s.+)',
        r'#{1,3}\s+(Where\s.+)',
        r'#{1,3}\s+(Can\s.+)',
        r'#{1,3}\s+(Do\s.+)',
        r'#{1,3}\s+(Is\s.+)',
        r'#{1,3}\s+(Are\s.+)',
        r'#{1,3}\s+(Will\s.+)',
        r'#{1,3}\s+(Does\s.+)',
    ]
    question_headings = []
    for pattern in question_heading_patterns:
        matches = re.findall(pattern, body, re.IGNORECASE | re.MULTILINE)
        question_headings.extend(matches)
    
    # Also count question marks in headings
    heading_questions = re.findall(r'#{1,3}\s+[^`\n]+\?', body)
    question_headings = list(set(question_headings + heading_questions))
    
    # Also check FAQ items
    faq_questions = re.findall(r'###\s+[^`\n]+\?', body)
    question_headings.extend(faq_questions)
    
    question_count = len(set(question_headings))
    
    # E. Internal Linking
    # Count internal links (markdown links starting with /)
    internal_links = re.findall(r'\[([^\]]+)\]\((/[^\)]+)\)', body)
    # Count by destination type
    service_links = [l for l in internal_links if '/services' in l[1]]
    location_links = [l for l in internal_links if '/locations' in l[1]]
    blog_links_count = [l for l in internal_links if '/blog/' in l[1]]
    other_links = [l for l in internal_links if not any(x in l[1] for x in ['/services', '/locations', '/blog/'])]
    
    total_internal = len(internal_links)
    
    # F. Schema readiness
    schema_checks = {
        "title": bool(title and len(title) > 10),
        "excerpt": bool(excerpt and len(excerpt) > 20),
        "date": bool(date),
        "dateModified": bool(dateModified),
        "metaTitle": bool(metaTitle),
        "metaDescription": bool(metaDescription),
    }
    schema_missing = [k for k, v in schema_checks.items() if not v]
    
    # Determine which pillar
    pillar_topic = "Uncategorized"
    if "fitness" in slug or "gym" in slug:
        pillar_topic = "Industry-Specific SEO"
    elif "law" in slug:
        pillar_topic = "Industry-Specific SEO"
    elif "b2b" in slug:
        pillar_topic = "B2B/Industrial SEO"
    elif "startup" in slug:
        pillar_topic = "Growth SEO"
    elif "https" in slug:
        pillar_topic = "Technical SEO"
    
    # Check if links to the pillar page
    pillar_page = ""
    if pillar_topic == "Industry-Specific SEO":
        pillar_page = "/industries"
    elif pillar_topic == "B2B/Industrial SEO":
        pillar_page = "/industries"
    elif pillar_topic == "Technical SEO":
        pillar_page = "/services/technical-seo"
    elif pillar_topic == "Growth SEO":
        pillar_page = "/services"
    
    links_to_pillar = any(pillar_page in l[1] for l in internal_links)
    
    return {
        "slug": slug,
        "title": title,
        "primary_keyword": primary_keyword,
        "keyword_count": kw_count,
        "entities": entities,
        "missing_entities": all_missing,
        "tags": tags,
        "pillar_topic": pillar_topic,
        "pillar_page": pillar_page,
        "links_to_pillar": links_to_pillar or has_pillar_link,
        "blog_links": blog_links,
        "question_headings": question_headings,
        "question_count": question_count,
        "internal_links": internal_links,
        "total_internal_links": total_internal,
        "service_links_count": len(service_links),
        "location_links_count": len(location_links),
        "blog_links_count": len(blog_links_count),
        "schema_checks": schema_checks,
        "schema_missing": schema_missing,
        "metaTitle": metaTitle,
        "metaDescription": metaDescription,
        "dateModified": dateModified,
        "excerpt": excerpt,
    }

for slug in posts_to_check:
    result = analyze_post(slug, content)
    print(f"\n{'='*80}")
    print(f"POST: {slug}")
    print(f"{'='*80}")
    if "error" in result:
        print(f"ERROR: {result['error']}")
        continue
    
    print(f"Title: {result['title']}")
    print(f"Primary Keyword: {result['primary_keyword']}")
    print(f"Keyword Count (top 3 parts): {result['keyword_count']}")
    print(f"Tags: {result['tags']}")
    print(f"Pillar Topic: {result['pillar_topic']}")
    print(f"Entities: {result['entities']}")
    print(f"Missing Entities: {result['missing_entities']}")
    print(f"Question Headings ({result['question_count']}): {result['question_headings']}")
    print(f"Total Internal Links: {result['total_internal_links']}")
    print(f"  Service links: {result['service_links_count']}")
    print(f"  Location links: {result['location_links_count']}")
    print(f"  Blog links: {result['blog_links_count']}")
    print(f"Links to Pillar: {result['links_to_pillar']}")
    print(f"Schema Checks: {result['schema_checks']}")
    print(f"Schema Missing: {result['schema_missing']}")
    print(f"metaTitle: {result['metaTitle']}")
    print(f"metaDescription: {result['metaDescription']}")
    print(f"dateModified: {result['dateModified']}")
    print(f"Blog Links: {result['blog_links']}")
    
    # Print detailed internal links for analysis
    print(f"\nInternal links:")
    for link_tuple in result['internal_links']:
        print(f"  - [{link_tuple[0]}]({link_tuple[1]})")
