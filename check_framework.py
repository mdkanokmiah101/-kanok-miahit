#!/usr/bin/env python3
"""
Content Framework Enforcer for kanokmiah.com.bd
Checks blog posts against 6 framework dimensions.
"""
import re, sys, json

# The modified slugs from git diff
MODIFIED_SLUGS = [
    "geo-optimization-prepare-business-ai-search",
    "seo-garments-textile-industry-b2b-lead-generation",
    "mobile-seo-optimization-bangladesh-mobile-first-era",
    "seo-healthcare-medical-clinics-bangladesh",
    "locksmith-dundee-seo-case-study",
    "das-taxis-scotland-seo-case-study",
    "smmgen-seo-case-study",
    "smmsun-seo-case-study",
    "mir-cement-seo-case-study",
    "dhaka-apparels-seo-case-study",
    "stealth-windshield-repairs-seo-case-study",
    "seo-expert-vs-seo-agency-dhaka-which-is-right",
    "hiring-seo-expert-dhaka-better-roi-than-paid-ads",
    "seo-case-study-dhaka-businesses-increased-organic-traffic",
    "watchzonebd-seo-case-study",
    "how-to-choose-best-seo-expert-dhaka-15-things",
    "top-10-seo-mistakes-dhaka-businesses-fix",
    "what-does-seo-expert-do-guide-business-owners",
    "ai-seo-2026-dhaka-experts-optimize-google-ai-chatgpt",
]

def parse_posts(filepath):
    """Parse blog posts from data.js using regex-based extraction."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    posts = []
    # Find each post object starting with `{` and ending with `},`
    # Use regex to extract slug:title blocks
    # Each post is: {\n    slug: "...",\n    title: "...",\n    ...
    # We'll split by looking for patterns like `  {` after `const posts = [`
    
    # Find the array start
    array_start = content.find('const posts = [')
    if array_start == -1:
        print("ERROR: Could not find 'const posts = ['")
        sys.exit(1)
    
    # Extract the array content
    array_content = content[array_start + len('const posts = ['):]
    
    # Find matching closing bracket - track nesting
    depth = 1
    i = 0
    while depth > 0 and i < len(array_content):
        if array_content[i] == '[':
            depth += 1
        elif array_content[i] == ']':
            depth -= 1
        i += 1
    
    if depth != 0:
        print("ERROR: Unbalanced brackets")
        sys.exit(1)
    
    array_body = array_content[:i-1]  # exclude trailing ']'
    
    # Split into individual post objects at the top level
    # Each post starts with `  {` (or `{`) at the top level and ends with `  },`
    posts_raw = []
    depth = 0
    current = []
    in_post = False
    
    for line in array_body.split('\n'):
        # Check if this line starts a new post
        stripped = line.strip()
        if stripped == '{' and not in_post:
            in_post = True
            current = [line]
            depth = 1
        elif in_post:
            current.append(line)
            depth += stripped.count('{') - stripped.count('}')
            if depth <= 0:
                posts_raw.append('\n'.join(current))
                in_post = False
                current = []
    
    # Parse each post into a dict
    for pr in posts_raw:
        post = {}
        
        # Extract slug
        m = re.search(r'slug:\s*"([^"]+)"', pr)
        if m:
            post['slug'] = m.group(1)
        
        # Extract title
        m = re.search(r'title:\s*"([^"]+)"', pr)
        if m:
            post['title'] = m.group(1)
        
        # Extract date
        m = re.search(r'date:\s*"([^"]+)"', pr)
        if m:
            post['date'] = m.group(1)
        
        # Extract excerpt
        m = re.search(r'excerpt:\s*"([^"]+)"', pr)
        if m:
            post['excerpt'] = m.group(1)
        # Also try multi-line excerpt
        if 'excerpt:' in pr:
            m = re.search(r'excerpt:\s*\n\s+"([^"]+)"', pr)
            if m:
                post['excerpt'] = m.group(1)
        
        # Extract tags
        m = re.search(r'tags:\s*\[([^\]]+)\]', pr)
        if m:
            tags_str = m.group(1)
            post['tags'] = re.findall(r'"([^"]+)"', tags_str)
        
        # Extract content (everything between content: \` and the closing \`)
        # Use non-greedy match for the template literal
        m = re.search(r'content:\s*`((?:[^`]|\\`)*)`', pr, re.DOTALL)
        if m:
            post['content'] = m.group(1)
        
        # Extract dateModified if present
        m = re.search(r'dateModified:\s*"([^"]+)"', pr)
        if m:
            post['dateModified'] = m.group(1)
        
        posts.append(post)
    
    return posts

def check_tfidf(title, content):
    """Extract primary keyword from title and count occurrences in content."""
    # Extract first meaningful noun phrase from title
    # Remove stop words and take first substantive word(s)
    title_lower = title.lower()
    
    # Common SEO patterns in titles
    patterns = [
        (r'(SEO|seo|Seo)\s+(for|in|of|guide|tips|strategy|checklist|mistakes|expert|agency|services|case\s+study|optimization|basics|audit|tools)\s', None),
        (r'(search\s+engine\s+optimization)', None),
        (r'(local\s+seo|technical\s+seo|on-page\s+seo|ecommerce\s+seo|e-commerce\s+seo)', None),
        (r'(generative\s+engine\s+optimization|geo\s+optimization|ai\s+search)', None),
        (r'(mobile\s+seo|mobile\s+optimization|mobile-first)', None),
        (r'(garments?\s+(?:and\s+)?textile)', None),
        (r'(healthcare|medical|clinic|doctor)', None),
        (r'(link\s+building|backlinks|off-page)', None),
        (r'(keyword\s+research|keyword\s+analysis)', None),
        (r'(content\s+marketing|content\s+strategy)', None),
        (r'(google\s+business\s+profile|gbp|google\s+maps)', None),
        (r'(core\s+web\s+vitals|page\s+speed|page\s+experience)', None),
        (r'(international\s+seo|multilingual|hreflang)', None),
        (r'(ecommerce|e-commerce|online\s+store|shopify)', None),
        (r'(real\s+estate|property|housing)', None),
        (r'(education|university|college|school)', None),
        (r'(restaurant|food|dining|cafe)', None),
        (r'(beauty|salon|spa|barber)', None),
        (r'(lawyer|attorney|legal|law\s+firm)', None),
    ]
    
    keyword = None
    for pat, _ in patterns:
        m = re.search(pat, title_lower)
        if m:
            keyword = m.group(0).strip()
            break
    
    if not keyword:
        # Fallback: take first 2-3 meaningful words
        words = [w for w in title_lower.split() if w not in ('a','an','the','in','for','of','to','and','or','is','are','your','our','their','its','with','on','at','by','from','as','be','has','have','do','does','did','will','would','could','should','may','might','must','need','can','all','every','each','some','any','no','not','only','just','also','very','more','most','much','many','such','than','that','this','these','those','what','which','who','whom','when','where','why','how')]
        if words:
            keyword = ' '.join(words[:3])
        else:
            keyword = title_lower.split()[0] if title_lower.split() else title
    
    # Count occurrences of the keyword in content (case-insensitive)
    content_lower = content.lower()
    count = len(re.findall(re.escape(keyword.lower()), content_lower))
    
    return keyword, count

def check_entities(title, content, tags):
    """Check for key semantic entities."""
    title_lower = title.lower()
    content_lower = content.lower()
    
    # Determine expected entities based on title/tags
    expected_entities = []
    
    # Location entities (always should have Dhaka or Bangladesh)
    locations = ['dhaka', 'bangladesh', 'chittagong', 'sylhet', 'gulshan', 'banani', 'dhanmondi', 'uttara', 'motijheel', 'mirpur', 'farmgate']
    has_location = False
    found_locations = []
    for loc in locations:
        if loc in title_lower or loc in content_lower:
            has_location = True
            found_locations.append(loc)
    if not has_location:
        expected_entities.append('location (Dhaka/Bangladesh)')
    
    # Determine service/industry type from title and tags
    tag_lower = [t.lower() for t in tags] if tags else []
    combined = title_lower + ' ' + ' '.join(tag_lower)
    
    service_patterns = [
        ('local seo', ['local', 'maps', 'gbp', 'citation']),
        ('technical seo', ['technical', 'crawl', 'core web vitals', 'schema', 'structured data']),
        ('content strategy', ['content', 'blog', 'article', 'writing']),
        ('link building', ['link', 'backlink', 'authority']),
        ('geo/aeo', ['geo', 'generative engine', 'aeo', 'answer engine', 'ai search']),
        ('ecommerce seo', ['ecommerce', 'e-commerce', 'shop', 'product', 'online store']),
        ('web design/development', ['web design', 'web dev', 'website', 'responsive']),
        ('social media marketing', ['social media', 'facebook', 'instagram', 'linkedin']),
    ]
    
    found_services = []
    for svc_name, svc_keywords in service_patterns:
        if any(kw in combined for kw in svc_keywords):
            found_services.append(svc_name)
    
    # Check industry entities
    industry_patterns = [
        'garment', 'textile', 'apparel', 'rmg',
        'healthcare', 'medical', 'clinic', 'hospital', 'doctor',
        'real estate', 'property', 'housing',
        'education', 'university', 'college', 'school',
        'ecommerce', 'e-commerce', 'retail', 'shop',
        'restaurant', 'food', 'dining', 'cafe',
        'beauty', 'salon', 'spa',
        'locksmith',
        'taxi', 'transportation',
        'cement', 'construction', 'manufacturing',
        'windshield', 'auto', 'automotive',
    ]
    
    found_industries = []
    for ind in industry_patterns:
        if ind in combined or ind in content_lower:
            found_industries.append(ind)
    
    # Brand entity
    brand_entity = False
    if 'kanok miah' in content_lower or '/about' in content_lower:
        brand_entity = True
    
    # Check for competitor/named entities
    competitors = ['google', 'chatgpt', 'perplexity', 'gemini', 'claude', 'sge']
    found_competitors = [c for c in competitors if c in content_lower]
    
    missing = []
    if not has_location:
        missing.append('location entity (Dhaka/Bangladesh)')
    if not brand_entity:
        missing.append('brand entity (Kanok Miah)')
    if not found_services:
        missing.append('service type entity')
    
    return {
        'locations_found': found_locations,
        'services_found': found_services,
        'industries_found': found_industries,
        'brand_entity': brand_entity,
        'competitors_found': found_competitors,
        'missing': missing,
    }

def check_pillar_cluster(title, content, tags):
    """Check alignment with pillar topics and links to pillar page."""
    tag_lower = [t.lower() for t in tags] if tags else []
    title_lower = title.lower()
    content_lower = content.lower()
    
    # Pillar pages mapping
    pillars = {
        'SEO Guide': {
            'pillar_slug': 'complete-seo-guide-bangladesh-businesses-2026',
            'pillar_title': 'Complete SEO Guide for Bangladesh Businesses in 2026',
            'keywords': ['seo guide', 'seo basics', 'seo tips', 'seo strategy'],
        },
        'Local SEO': {
            'pillar_slug': 'local-seo-tips-dhaka-businesses-google-maps',
            'pillar_title': 'Local SEO Tips for Dhaka Businesses',
            'keywords': ['local seo', 'google business profile', 'google maps', 'gbp', 'local search', 'near me'],
        },
        'Technical SEO': {
            'pillar_slug': 'technical-seo-checklist-bangladeshi-websites',
            'pillar_title': 'Technical SEO Checklist',
            'keywords': ['technical seo', 'core web vitals', 'page speed', 'schema markup', 'crawlability', 'structured data'],
        },
        'GEO/AEO': {
            'pillar_slug': 'geo-optimization-prepare-business-ai-search',
            'pillar_title': 'GEO Optimization Guide for Bangladesh',
            'keywords': ['geo', 'generative engine optimization', 'aeo', 'answer engine optimization', 'ai search', 'ai-powered search'],
        },
        'Content Marketing': {
            'pillar_slug': 'content-marketing-strategy-bangladesh-seo',
            'pillar_title': 'Content Marketing Strategy',
            'keywords': ['content marketing', 'content strategy', 'blogging', 'content writing'],
        },
        'E-commerce SEO': {
            'pillar_slug': 'why-ecommerce-store-needs-seo-bangladesh',
            'pillar_title': 'E-commerce SEO for Bangladesh',
            'keywords': ['ecommerce', 'e-commerce', 'online store', 'shopify', 'product page'],
        },
        'Case Studies': {
            'pillar_slug': None,  # No single pillar page
            'keywords': ['case study', 'seo result', 'traffic increase', 'ranking improvement'],
        },
    }
    
    # Determine which pillar(s) this post belongs to
    matched_pillars = []
    for pillar_name, pillar_info in pillars.items():
        if any(kw in title_lower or kw in ' '.join(tag_lower) for kw in pillar_info['keywords']):
            matched_pillars.append(pillar_name)
        elif any(kw in content_lower for kw in pillar_info['keywords']):
            matched_pillars.append(pillar_name)
    
    # Check if post already links to the pillar page
    pillar_links = []
    for pillar_name, pillar_info in pillars.items():
        if pillar_info['pillar_slug']:
            # Check for link to this pillar
            link_patterns = [
                f'/blog/{pillar_info["pillar_slug"]}',
                f'blog/{pillar_info["pillar_slug"]}',
                pillar_info['pillar_title'].lower(),
            ]
            for lp in link_patterns:
                if lp.lower() in content_lower:
                    pillar_links.append(pillar_name)
                    break
    
    return {
        'matched_pillars': matched_pillars,
        'pillar_links': pillar_links,
        'missing_pillar_links': [p for p in matched_pillars if p not in pillar_links and p != 'Case Studies'],
    }

def check_aeo_geo(content):
    """Check for question-based headings (AEO/GEO optimization)."""
    # Look for headings (##, ###, ####) that start with question words
    question_heading_pattern = re.compile(
        r'#{2,4}\s+(How|What|Why|When|Where|Can|Do|Does|Is|Are|Will|Would|Could|Should|Has|Have|Which|Who|Whom)\b',
        re.IGNORECASE
    )
    headings = question_heading_pattern.findall(content)
    return len(headings), headings

def check_internal_links(content, slug):
    """Count internal links to other posts, services, locations."""
    # Count links to /blog/, /services/, /locations/, /industries/, /about, # (hash links excluded)
    # Exclude self-references and external links
    internal_link_pattern = re.compile(
        r'\[([^\]]*)\]\(((?:/blog/|/services/|/locations/|/industries/|/about|/contact|/faq|/#)[^)]*)\)',
        re.IGNORECASE
    )
    all_links = internal_link_pattern.findall(content)
    
    # Exclude links to self
    self_slug = f'/blog/{slug}'
    other_links = [(text, url) for text, url in all_links if self_slug not in url]
    
    # Also count bare internal links (without markdown)
    bare_links = re.findall(r'(?:/blog/[^"\'\s\)]+|/services/[^"\'\s\)]+|/locations/[^"\'\s\)]+|/industries/[^"\'\s\)]+)', content)
    
    # Count unique link destinations
    link_urls = set(url for _, url in other_links)
    link_urls.update(bare_links)
    
    return len(link_urls), other_links

def check_schema(title, excerpt, date, dateModified):
    """Check if fields needed for ArticleSchema are present."""
    missing_fields = []
    if not title:
        missing_fields.append('title')
    if not excerpt:
        missing_fields.append('excerpt')
    if not date:
        missing_fields.append('date')
    
    return {
        'all_present': len(missing_fields) == 0,
        'missing_fields': missing_fields,
        'fields': {
            'title': bool(title),
            'excerpt': bool(excerpt),
            'date': bool(date),
            'dateModified': bool(dateModified),
        }
    }

def main():
    filepath = '/root/kanok-miahit/src/app/blog/data.js'
    posts = parse_posts(filepath)
    
    # Index by slug
    post_map = {p.get('slug'): p for p in posts}
    
    results = []
    
    for slug in MODIFIED_SLUGS:
        if slug not in post_map:
            results.append(f"## Post: {slug}\n⚠️ **Post not found in data.js**\n")
            continue
        
        post = post_map[slug]
        title = post.get('title', '')
        excerpt = post.get('excerpt', '')
        date = post.get('date', '')
        tags = post.get('tags', [])
        content = post.get('content', '')
        dateModified = post.get('dateModified', '')
        
        # A. TF-IDF Coverage
        keyword, tfidf_count = check_tfidf(title, content)
        tfidf_pass = tfidf_count >= 5
        
        # B. Entity Coverage
        entity_result = check_entities(title, content, tags)
        entity_pass = len(entity_result['missing']) == 0
        
        # C. Pillar-Cluster Alignment
        pillar_result = check_pillar_cluster(title, content, tags)
        pillar_pass = len(pillar_result['missing_pillar_links']) == 0
        
        # D. AEO/GEO Optimization
        aeo_count, aeo_headings = check_aeo_geo(content)
        aeo_pass = aeo_count >= 2
        
        # E. Internal Linking
        link_count, _ = check_internal_links(content, slug)
        link_pass = link_count >= 3
        
        # F. Schema
        schema_result = check_schema(title, excerpt, date, dateModified)
        schema_pass = schema_result['all_present']
        
        results.append({
            'slug': slug,
            'title': title,
            'checks': {
                'tfidf': {
                    'pass': tfidf_pass,
                    'keyword': keyword,
                    'count': tfidf_count,
                },
                'entities': {
                    'pass': entity_pass,
                    'missing': entity_result['missing'],
                    'locations': entity_result['locations_found'],
                    'services': entity_result['services_found'],
                    'industries': entity_result['industries_found'],
                    'brand': entity_result['brand_entity'],
                },
                'pillar': {
                    'pass': pillar_pass,
                    'matched_pillars': pillar_result['matched_pillars'],
                    'pillar_links': pillar_result['pillar_links'],
                    'missing_links': pillar_result['missing_pillar_links'],
                },
                'aeo': {
                    'pass': aeo_pass,
                    'count': aeo_count,
                    'headings': aeo_headings,
                },
                'links': {
                    'pass': link_pass,
                    'count': link_count,
                },
                'schema': {
                    'pass': schema_pass,
                    'missing_fields': schema_result['missing_fields'],
                    'fields': schema_result['fields'],
                }
            }
        })
    
    # Generate report
    all_pass = True
    for r in results:
        if isinstance(r, str):
            print(r)
            all_pass = False
            continue
        
        checks = r['checks']
        row_all_pass = all(c['pass'] for c in checks.values())
        if not row_all_pass:
            all_pass = False
        
        slug = r['slug']
        title = r['title']
        c = checks
        
        print(f"## Post: {slug}")
        print(f"**Title:** {title}")
        print("| Check | Status | Details |")
        print("|-------|--------|---------|")
        print(f"| TF-IDF: `{c['tfidf']['keyword']}` | {'✅' if c['tfidf']['pass'] else '❌'} | {c['tfidf']['count']} occurrences |")
        print(f"| Entities | {'✅' if c['entities']['pass'] else '❌'} | Missing: {', '.join(c['entities']['missing']) if c['entities']['missing'] else 'None'} (Locs: {', '.join(c['entities']['locations'][:5]) if c['entities']['locations'] else 'None'}, Svcs: {', '.join(c['entities']['services'][:3]) if c['entities']['services'] else 'None'}) |")
        print(f"| Pillar Link | {'✅' if c['pillar']['pass'] else '❌'} | Pillars: {', '.join(c['pillar']['matched_pillars'][:3]) if c['pillar']['matched_pillars'] else 'None'} → Links to: {', '.join(c['pillar']['pillar_links'][:3]) if c['pillar']['pillar_links'] else 'None'} |")
        print(f"| AEO/GEO | {'✅' if c['aeo']['pass'] else '❌'} | {c['aeo']['count']} question headings ({', '.join(c['aeo']['headings'][:5]) if c['aeo']['headings'] else 'None'}) |")
        print(f"| Internal Links | {'✅' if c['links']['pass'] else '❌'} | {c['links']['count']} internal links |")
        print(f"| Schema Ready | {'✅' if c['schema']['pass'] else '❌'} | Missing: {', '.join(c['schema']['missing_fields']) if c['schema']['missing_fields'] else 'All fields set'} |")
        
        # Fix instructions
        fixes = []
        if not c['tfidf']['pass']:
            fixes.append(f"- 🔴 **TF-IDF Thin**: Keyword `{c['tfidf']['keyword']}` appears only {c['tfidf']['count']} times. Add more natural mentions throughout (target ≥5).")
        if not c['entities']['pass']:
            for m in c['entities']['missing']:
                fixes.append(f"- 🔴 **Missing Entity**: {m}. Add natural references to this entity in the content.")
        if not c['pillar']['pass']:
            for mp in c['pillar']['missing_links']:
                pillar_info = {
                    'SEO Guide': ('complete-seo-guide-bangladesh-businesses-2026', 'Complete SEO Guide'),
                    'Local SEO': ('local-seo-tips-dhaka-businesses-google-maps', 'Local SEO Tips'),
                    'Technical SEO': ('technical-seo-checklist-bangladeshi-websites', 'Technical SEO Checklist'),
                    'GEO/AEO': ('geo-optimization-prepare-business-ai-search', 'GEO Optimization Guide'),
                    'Content Marketing': ('content-marketing-strategy-bangladesh-seo', 'Content Marketing Strategy'),
                    'E-commerce SEO': ('why-ecommerce-store-needs-seo-bangladesh', 'E-commerce SEO Guide'),
                }
                if mp in pillar_info:
                    fixes.append(f"- 🔴 **Missing Pillar Link**: No link to `{mp}` pillar page (/{pillar_info[mp][0]}). Add: `[{pillar_info[mp][1]}](/blog/{pillar_info[mp][0]})`.")
                else:
                    fixes.append(f"- 🔴 **Missing Pillar Link**: No link to `{mp}` pillar page.")
        if not c['aeo']['pass']:
            fixes.append(f"- 🟡 **Low AEO/GEO**: Only {c['aeo']['count']} question headings found (need ≥2). Add a FAQ section with question-based headings (How, What, Why, etc.).")
        if not c['links']['pass']:
            fixes.append(f"- 🟡 **Thin Internal Linking**: Only {c['links']['count']} internal links (need ≥3). Add links to related blog posts, service pages, or location pages.")
        if not c['schema']['pass']:
            for f in c['schema']['missing_fields']:
                fixes.append(f"- 🟡 **Missing Schema Field**: `{f}` is not set. Add it for proper ArticleSchema markup.")
        
        if fixes:
            print("\n### Fix instructions:")
            for f in fixes:
                print(f)
        else:
            print("\n### ✅ All checks pass — no fixes needed.")
        
        print()
    
    # Summary
    total = len([r for r in results if isinstance(r, dict)])
    passed = sum(1 for r in results if isinstance(r, dict) and all(c['pass'] for c in r['checks'].values()))
    failed = total - passed
    
    print("---")
    print(f"## Summary: {passed}/{total} posts pass all checks ({failed} need attention)")

if __name__ == '__main__':
    main()
