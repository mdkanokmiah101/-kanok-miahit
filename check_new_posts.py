import re, json, sys

# Read the current data.js
with open('src/app/blog/data.js', 'r') as f:
    content = f.read()

def extract_post_by_slug(content, target_slug):
    """Extract a single post object by slug."""
    lines = content.split('\n')
    posts = {}
    i = 0
    current_slug = None
    post_start = None
    
    while i < len(lines):
        line = lines[i]
        m = re.search(r'slug: "([^"]+)"', line)
        if m:
            current_slug = m.group(1)
            post_start = i
            # If this is our target, collect the post
            if current_slug == target_slug:
                post_lines = [line]
                i += 1
                # Check if next line has content: (it might be on the next line or same line)
                while i < len(lines):
                    next_line = lines[i]
                    # Stop at next slug or end of array
                    if re.search(r'slug: "([^"]+)"', next_line) and i != post_start:
                        break
                    if next_line.strip() == '];':
                        break
                    post_lines.append(next_line)
                    i += 1
                return '\n'.join(post_lines)
        i += 1
    return None

def parse_post_metadata(post_text):
    """Extract title, date, excerpt, tags from post text."""
    meta = {}
    
    m = re.search(r'title: "([^"]*)"', post_text)
    if m:
        meta['title'] = m.group(1)
    
    m = re.search(r'date: "([^"]*)"', post_text)
    if m:
        meta['date'] = m.group(1)
    
    m = re.search(r'excerpt:\s+"([^"]*)"', post_text, re.DOTALL)
    if m:
        meta['excerpt'] = m.group(1)
    
    m = re.search(r'tags:\s*\[([^\]]+)\]', post_text, re.DOTALL)
    if m:
        tags_str = m.group(1)
        meta['tags'] = [t.strip().strip('"') for t in tags_str.split(',')]
    
    # Extract content - everything after content: `
    m = re.search(r'content:\s*`((?:[^`]|`(?!\s*,))*)`', post_text, re.DOTALL)
    if m:
        meta['content'] = m.group(1)
    
    return meta

def check_tfidf(title, content):
    """Check TF-IDF keyword coverage."""
    if not title:
        return None, "No title found"
    
    # Extract primary keyword from title
    # First meaningful noun phrase
    title_lower = title.lower()
    
    # Remove common prefixes
    prefix_patterns = [
        r'^(complete|ultimate|definitive|essential|top|best|how to|why|what|when|where)\s+',
        r'^(the|a|an)\s+',
    ]
    keyword = title_lower
    for pat in prefix_patterns:
        keyword = re.sub(pat, '', keyword)
    
    # Take first meaningful word pair
    words = keyword.split()
    if len(words) >= 3:
        keyword = ' '.join(words[:3])
    elif len(words) >= 2:
        keyword = ' '.join(words[:2])
    elif len(words) >= 1:
        keyword = words[0]
    else:
        keyword = title_lower
    
    # Find the most distinctive noun phrase (skip general words)
    stop_words = {'guide', 'for', 'in', 'the', 'of', 'to', 'and', 'a', 'an', 'is', 'are', 'your', 'from', 'with', 'that', 'this', 'businesses', 'dhaka', 'bangladesh', 'online'}
    
    # Also try to use tag-related terms
    # For now, just count occurrences of the keyword's key terms
    content_lower = content.lower() if content else ''
    
    keyword_terms = [w for w in keyword.split() if w not in stop_words and len(w) > 3]
    
    if not keyword_terms:
        # Fall back to most specific word
        keyword_terms = [w for w in keyword.split() if len(w) > 3][:1]
    
    if not keyword_terms:
        return "generic-title", "Could not extract meaningful keyword"
    
    # Count the main keyword phrase occurrences
    count = 0
    for term in keyword_terms:
        count += content_lower.count(term)
    
    primary_kw = ' '.join(keyword_terms)
    return primary_kw, count

def check_entities(content, tags, title):
    """Check semantic entity coverage."""
    content_lower = content.lower() if content else ''
    tags_lower = [t.lower() for t in (tags or [])]
    title_lower = title.lower() if title else ''
    
    # Key entities that should be present
    required_entities = {
        'location_dhaka': ['dhaka', 'dhaka\'s'],
        'location_bangladesh': ['bangladesh', 'bangladesh\'s', 'bangladeshi'],
        'entity_google': ['google', 'search engine'],
        'entity_seo': ['seo', 'search engine optimization'],
    }
    
    # Determine which additional entities based on tags/title
    if any('ecommerce' in t or 'e-commerce' in t for t in tags_lower):
        required_entities['service_ecommerce'] = ['ecommerce', 'e-commerce', 'online store']
    if any('local' in t for t in tags_lower):
        required_entities['service_local'] = ['local seo', 'google business profile', 'google maps']
    if any('technical' in t for t in tags_lower):
        required_entities['service_technical'] = ['technical', 'crawl', 'index', 'core web vitals', 'page speed']
    if any('ai' in t or 'geo' in t for t in tags_lower):
        required_entities['service_ai'] = ['ai', 'generative engine', 'geo', 'chatgpt', 'gemini']
    if any('content' in t or 'marketing' in t for t in tags_lower):
        required_entities['service_content'] = ['content', 'blog', 'article']
    if any('link' in t for t in tags_lower):
        required_entities['service_link'] = ['backlink', 'link building', 'internal link']
    if any('schema' in t or 'structured' in t for t in tags_lower):
        required_entities['service_schema'] = ['schema', 'structured data', 'rich snippet']
    if any('mobile' in t for t in tags_lower):
        required_entities['service_mobile'] = ['mobile', 'responsive']
    if any('voice' in t for t in tags_lower):
        required_entities['service_voice'] = ['voice search', 'voice']
    if any('case study' in t or 'case' in t for t in tags_lower) or 'case study' in title_lower:
        required_entities['service_case_study'] = ['case study', 'results', 'growth']
    if any('expert' in t or 'agency' in t for t in tags_lower):
        required_entities['service_expert'] = ['expert', 'agency', 'professional']
    
    # Add general business entity checks
    if any('restaurant' in t or 'food' in t or 'cafe' in t for t in tags_lower):
        required_entities['industry_restaurant'] = ['restaurant', 'cafe', 'food']
    if any('real estate' in t or 'property' in t for t in tags_lower):
        required_entities['industry_realestate'] = ['real estate', 'property', 'developer']
    if any('health' in t or 'medical' in t or 'clinic' in t for t in tags_lower):
        required_entities['industry_health'] = ['healthcare', 'medical', 'clinic', 'doctor']
    if any('education' in t for t in tags_lower):
        required_entities['industry_education'] = ['education', 'school', 'college', 'university']
    if any('salon' in t or 'spa' in t for t in tags_lower):
        required_entities['industry_salon'] = ['salon', 'spa', 'beauty']
    if any('cleaning' in t for t in tags_lower):
        required_entities['industry_cleaning'] = ['cleaning', 'clean']
    
    found = {}
    missing = {}
    
    for entity_name, keywords in required_entities.items():
        entity_found = False
        matched_kw = None
        for kw in keywords:
            if kw in content_lower:
                entity_found = True
                matched_kw = kw
                break
        if entity_found:
            found[entity_name] = matched_kw
        else:
            missing[entity_name] = keywords[0]
    
    return found, missing

def check_pillar_link(content, tags, title):
    """Check pillar-cluster alignment based on tags."""
    content_lower = content.lower() if content else ''
    tags_lower = [t.lower() for t in (tags or [])]
    
    # Map tags to pillar topics and their pillar page URLs
    pillar_map = {
        'seo guide': {'pillar': '/blog/complete-seo-guide-bangladesh-businesses-2026', 'aliases': ['complete seo guide']},
        'local seo': {'pillar': '/blog/local-seo-tips-dhaka-businesses-google-maps', 'aliases': ['local seo tips dhaka']},
        'ecommerce seo': {'pillar': '/blog/why-ecommerce-store-needs-seo-bangladesh', 'aliases': ['ecommerce store needs seo']},
        'technical seo': {'pillar': '/blog/technical-seo-checklist-bangladeshi-websites', 'aliases': ['technical seo checklist']},
        'case study': {'pillar': None, 'aliases': ['case study']},
        'ai seo': {'pillar': '/blog/geo-optimization-prepare-business-ai-search', 'aliases': ['geo optimization', 'ai search']},
        'link building': {'pillar': '/blog/link-building-strategies-bangladesh-market', 'aliases': ['link building strategies bangladesh']},
        'schema': {'pillar': '/blog/schema-markup-rich-snippets-techniques', 'aliases': ['schema markup rich snippets']},
    }
    
    # Try to determine pillar from tags or title
    primary_pillar = None
    pillar_url = None
    
    for tag in tags_lower:
        for pillar_name, pillar_info in pillar_map.items():
            if pillar_name in tag or any(alias in tag for alias in pillar_info['aliases']):
                primary_pillar = pillar_name
                pillar_url = pillar_info['pillar']
                break
        if primary_pillar:
            break
    
    if not primary_pillar:
        # Try from title
        title_lower = title.lower() if title else ''
        for pillar_name, pillar_info in pillar_map.items():
            if pillar_name in title_lower or any(alias in title_lower for alias in pillar_info['aliases']):
                primary_pillar = pillar_name
                pillar_url = pillar_info['pillar']
                break
    
    if not pillar_url:
        return None, "No pillar page mapped (tags don't match known pillars)"
    
    # Check if post links to pillar page
    if pillar_url in content_lower:
        return primary_pillar, f"Links to: {pillar_url}"
    else:
        global _pillar_url
        _pillar_url = pillar_url
        return primary_pillar, f"MISSING: No link to pillar page ({pillar_url})"

def check_aeo_geo(content):
    """Check AEO/GEO question-based headings."""
    if not content:
        return 0
    
    # Count question-based headings (## or ### starting with question words)
    q_words = r'(How|What|Why|When|Where|Can|Do|Is|Are|Does|Should|Which|Who|Whose|Whom)'
    pattern = re.compile(r'^#{2,3}\s+' + q_words, re.MULTILINE | re.IGNORECASE)
    
    matches = pattern.findall(content)
    return len(matches)

def check_internal_links(content):
    """Count internal links to other posts, services, locations."""
    if not content:
        return 0, []
    
    # Count links starting with /blog/, /services/, /industries/, /locations/
    link_pattern = re.compile(r'\[([^\]]*)\]\((/[^)]+)\)')
    links = link_pattern.findall(content)
    
    internal_links = [(text, url) for text, url in links if url.startswith(('/blog/', '/services/', '/industries/', '/locations/', '/'))]
    return len(internal_links), internal_links[:10]  # Return first 10 for sample

def check_schema_readiness(post_meta):
    """Check if post has title, excerpt, date (needed for ArticleSchema)."""
    missing_fields = []
    
    if not post_meta.get('title'):
        missing_fields.append('title')
    if not post_meta.get('excerpt'):
        missing_fields.append('excerpt')
    if not post_meta.get('date'):
        missing_fields.append('date')
    if not post_meta.get('tags'):
        missing_fields.append('tags')
    
    if missing_fields:
        return False, f"Missing: {', '.join(missing_fields)}"
    else:
        return True, "All fields set"

# Main: process new posts
new_slugs = [
    'ai-seo-2026-dhaka-experts-optimize-google-ai-chatgpt',
    'hiring-seo-expert-dhaka-better-roi-than-paid-ads',
    'how-to-choose-best-seo-expert-dhaka-15-things',
    'seo-case-study-dhaka-businesses-increased-organic-traffic',
    'seo-expert-vs-seo-agency-dhaka-which-is-right',
    'top-10-seo-mistakes-dhaka-businesses-fix',
    'watchzonebd-seo-case-study',
    'what-does-seo-expert-do-guide-business-owners',
]

for slug in new_slugs:
    print(f"\n{'='*70}")
    print(f"## Post: {slug}")
    print(f"{'='*70}")
    
    post_text = extract_post_by_slug(content, slug)
    if not post_text:
        print(f"ERROR: Could not extract post '{slug}'")
        continue
    
    meta = parse_post_metadata(post_text)
    title = meta.get('title', '')
    excerpt = meta.get('excerpt', '')
    date = meta.get('date', '')
    tags = meta.get('tags', [])
    content_text = meta.get('content', '')
    
    print(f"Title: {title}")
    print(f"Date: {date}")
    print(f"Tags: {tags}")
    print(f"Content length: {len(content_text)} chars")
    print()
    
    # A. TF-IDF Coverage
    keyword, count = check_tfidf(title, content_text)
    if isinstance(count, int):
        status = "✅" if count >= 5 else "❌"
        print(f"| TF-IDF: {keyword} | {status} | {count} occurrences |")
    else:
        print(f"| TF-IDF | ⚠️ | {count} |")
    
    # B. Semantic Entity Coverage
    found_entities, missing_entities = check_entities(content_text, tags, title)
    if missing_entities:
        print(f"| Entities | ❌ | Missing: {', '.join(missing_entities.keys())} |")
    else:
        print(f"| Entities | ✅ | All key entities present |")
    # Debug: show what was found
    if found_entities:
        print(f"  Found entities: {list(found_entities.keys())}")
    if missing_entities:
        print(f"  Missing entities: {missing_entities}")
    
    # C. Pillar-Cluster Alignment
    pillar, pillar_result = check_pillar_link(content_text, tags, title)
    if pillar:
        if 'MISSING' in pillar_result:
            print(f"| Pillar: {pillar} | ❌ | {pillar_result} |")
        else:
            print(f"| Pillar: {pillar} | ✅ | {pillar_result} |")
    else:
        print(f"| Pillar | ⚠️ | {pillar_result} |")
    
    # D. AEO/GEO Optimization
    q_count = check_aeo_geo(content_text)
    status = "✅" if q_count >= 2 else "❌"
    print(f"| AEO/GEO | {status} | {q_count} question headings |")
    if q_count < 2:
        print(f"  Need {2 - q_count} more question-based headings")
    
    # E. Internal Linking
    link_count, sample_links = check_internal_links(content_text)
    status = "✅" if link_count >= 3 else "❌"
    print(f"| Internal Links | {status} | {link_count} total |")
    if link_count < 3:
        print(f"  Need {3 - link_count} more internal links")
    if sample_links:
        print(f"  Sample links: {[u for _, u in sample_links[:5]]}")
    
    # F. Schema Readiness
    schema_ok, schema_msg = check_schema_readiness(meta)
    status = "✅" if schema_ok else "❌"
    print(f"| Schema Ready | {status} | {schema_msg} |")
    
    # Generate fix instructions
    print(f"\n### Fix instructions:")
    fixes = []
    
    if isinstance(count, int) and count < 5:
        fixes.append(f"- 🔍 TF-IDF: Increase use of '{keyword}' (currently {count} occurrences, need ≥5)")
    
    if missing_entities:
        for entity_name, example_kw in missing_entities.items():
            fixes.append(f"- 🏷️ Entity '{entity_name}': Add mention of '{example_kw}' to content")
    
    if pillar and 'MISSING' in pillar_result:
        fixes.append(f"- 🔗 Add link to pillar page: {pillar_result}")
    
    if q_count < 2:
        fixes.append(f"- ❓ Add {2 - q_count}+ question-based headings (How/What/Why/Can/Do/Is/Are...)")
    
    if link_count < 3:
        fixes.append(f"- 🔗 Add {3 - link_count}+ internal links to other blog posts, services, or industry pages")
    
    if not schema_ok:
        fixes.append(f"- 📋 Add missing schema fields: {schema_msg}")
    
    if not fixes:
        fixes.append("✅ All checks pass — no fixes needed")
    
    for f in fixes:
        print(f"  {f}")

print("\n\nDone processing new posts.")
