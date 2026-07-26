#!/usr/bin/env python3
"""Extract and audit blog posts from data.js - v3 with robust parsing."""
import re
import sys

with open('/root/kanok-miahit/src/app/blog/data.js', 'r') as f:
    content = f.read()

# Find the posts array
posts_match = re.search(r'const posts = \[(.*?)\];', content, re.DOTALL)
if not posts_match:
    print("ERROR: Could not find posts array")
    sys.exit(1)

posts_section = posts_match.group(1)

# Split by post objects - they start with { and have slug:
# Each post: optionally preceded by }, then { on its own line
posts_raw = re.split(r'\}\s*,\s*\{', posts_section)
# First element might start with [ and whitespace before first {
first_post = posts_raw[0]
if first_post.strip().startswith('{'):
    pass
else:
    # Remove leading non-{ content
    idx = first_post.find('{')
    if idx >= 0:
        posts_raw[0] = first_post[idx:]
    else:
        print("ERROR: Cannot find first post")
        sys.exit(1)

# Re-add the leading { that got split off for all except first
for i in range(1, len(posts_raw)):
    posts_raw[i] = '{' + posts_raw[i]
# Remove trailing } from last element if present
if posts_raw[-1].strip().endswith('}'):
    last = posts_raw[-1].strip()
    posts_raw[-1] = last[:-1].strip()  # Remove trailing }

target_slugs = [
    "das-taxis-scotland-seo-case-study",
    "dhaka-apparels-seo-case-study", 
    "hiring-seo-expert-dhaka-better-roi-than-paid-ads",
    "locksmith-dundee-seo-case-study",
    "mir-cement-seo-case-study",
    "morethanpanel-seo-case-study",
    "seo-case-study-dhaka-businesses-increased-organic-traffic",
    "seo-expert-vs-seo-agency-dhaka-which-is-right",
    "seo-featured-snippet-bangladesh",
    "seo-knowledge-panel-bangladesh",
    "smmgen-seo-case-study",
    "smmsun-seo-case-study",
    "stealth-windshield-repairs-seo-case-study",
    "top-10-seo-mistakes-dhaka-businesses-fix",
    "watchzonebd-seo-case-study",
    "seo-referral-traffic-bangladesh",
    "seo-photographers-videographers-bangladesh"
]

KEYWORD_OVERRIDES = {
    "das-taxis-scotland-seo-case-study": "Das Taxis Scotland",
    "dhaka-apparels-seo-case-study": "Dhaka Apparels",
    "hiring-seo-expert-dhaka-better-roi-than-paid-ads": "SEO Expert Dhaka",
    "locksmith-dundee-seo-case-study": "Locksmith Dundee",
    "mir-cement-seo-case-study": "Mir Cement",
    "morethanpanel-seo-case-study": "MoreThanPanel",
    "seo-case-study-dhaka-businesses-increased-organic-traffic": "Dhaka Businesses Organic Traffic",
    "seo-expert-vs-seo-agency-dhaka-which-is-right": "SEO Expert vs SEO Agency Dhaka",
    "seo-featured-snippet-bangladesh": "ফিচার্ড স্নিপেট",
    "seo-knowledge-panel-bangladesh": "নলেজ প্যানেল",
    "smmgen-seo-case-study": "SMMGen",
    "smmsun-seo-case-study": "SMMSun",
    "stealth-windshield-repairs-seo-case-study": "Stealth Windshield Repairs",
    "top-10-seo-mistakes-dhaka-businesses-fix": "SEO Mistakes Dhaka",
    "watchzonebd-seo-case-study": "WatchZoneBD",
    "seo-referral-traffic-bangladesh": "রেফারেল ট্রাফিক",
    "seo-photographers-videographers-bangladesh": "Photographers Videographers SEO",
}

def extract_field(text, field_name):
    """Extract a simple string field value."""
    # Multi-line: title:\n      "value"
    ml_pattern = re.compile(rf'\n\s+{field_name}:\s*\n\s+"([^"]*)"', re.DOTALL)
    m = ml_pattern.search(text)
    if m:
        return m.group(1)
    # Single line: title: "value"
    pattern = re.compile(rf'\n\s+{field_name}:\s+"([^"]*)"', re.DOTALL)
    m = pattern.search(text)
    if m:
        return m.group(1)
    return None

def extract_tags(text):
    pattern = re.compile(r'\n\s+tags:\s*\[(.*?)\]', re.DOTALL)
    m = pattern.search(text)
    if m:
        tags_str = m.group(1)
        tags = re.findall(r'"([^"]*)"', tags_str)
        return tags
    return []

def extract_content(text):
    """Extract the content field (backtick template)."""
    # Find content: followed by backtick template
    pattern = re.compile(r'\n\s+content:\s*`\n(.*?)`\s*,?\s*(?://.*)?\n', re.DOTALL)
    m = pattern.search(text)
    if m:
        return m.group(1)
    return ""

def count_keyword(content, keyword):
    if not keyword:
        return 0
    pattern = re.compile(re.escape(keyword), re.IGNORECASE)
    return len(pattern.findall(content))

def count_question_headings(content):
    q_words = r'(?:How|What|Why|When|Where|Can|Do|Is|Are|Should|Which|Does)'
    pattern = re.compile(r'^##\s+' + q_words, re.MULTILINE | re.IGNORECASE)
    return len(pattern.findall(content))

def count_internal_links(content):
    pattern = re.compile(r'\(/(?:blog|locations|services|industries|about|contact)/[^)]*\)')
    return len(pattern.findall(content))

def extract_pillar_topic(tags):
    tag_lower = [t.lower() for t in tags]
    pillar_map = {
        'seo guide': 'SEO Fundamentals',
        'bangladesh seo': 'SEO Fundamentals',
        'seo roi': 'SEO Fundamentals', 
        'seo vs ads': 'SEO Fundamentals',
        'digital marketing': 'SEO Fundamentals',
        'seo tips': 'SEO Fundamentals',
        'seo mistakes': 'SEO Fundamentals',
        'seo results': 'SEO Fundamentals',
        'referral traffic': 'SEO Fundamentals',
        'seo': 'SEO Fundamentals',
        'local seo': 'Local SEO', 
        'gbp': 'Local SEO',
        'google maps': 'Local SEO',
        'e-commerce seo': 'E-commerce SEO',
        'ecommerce': 'E-commerce SEO',
        'daraz': 'E-commerce SEO',
        'shopify': 'E-commerce SEO',
        'technical seo': 'Technical SEO',
        'core web vitals': 'Technical SEO',
        'link building': 'Link Building',
        'backlinks': 'Link Building',
        'geo': 'Generative Engine Optimization',
        'ai search': 'Generative Engine Optimization',
        'generative engine': 'Generative Engine Optimization',
        'case study': 'Case Studies',
        'featured snippet': 'Advanced SEO',
        'knowledge panel': 'Advanced SEO',
        'seo consultant': 'SEO Services',
        'seo agency': 'SEO Services',
        'seo expert': 'SEO Services',
        'dhaka seo': 'SEO Services',
        'garments': 'Industry SEO',
        'b2b seo': 'Industry SEO',
        'construction': 'Industry SEO',
        'transportation': 'Industry SEO',
        'locksmith': 'Industry SEO',
        'automotive': 'Industry SEO',
        'smm panel': 'Industry SEO',
        'content marketing': 'SEO Fundamentals',
        'growth strategy': 'SEO Fundamentals',
    }
    
    best_match = None
    best_len = 0
    for tag in tag_lower:
        for key, pillar in pillar_map.items():
            if key in tag and len(key) > best_len:
                best_match = pillar
                best_len = len(key)
    
    return best_match or 'General SEO'

def has_pillar_link(content, tags):
    pillar = extract_pillar_topic(tags)
    pillar_urls = {
        'SEO Fundamentals': ['/blog/complete-seo-guide-bangladesh-businesses-2026', '/blog/'],
        'Local SEO': ['/blog/local-seo-tips-dhaka-businesses-google-maps', '/services/local-seo', '/blog/google-my-business-optimization-bangladesh'],
        'E-commerce SEO': ['/blog/why-ecommerce-store-needs-seo-bangladesh', '/services/ecommerce-seo', '/blog/ecommerce-seo-daraz-shopify-guide'],
        'Technical SEO': ['/blog/technical-seo-checklist-bangladeshi-websites', '/services/technical-seo'],
        'Link Building': ['/blog/link-building-strategies-bangladesh-market', '/services/link-building'],
        'Generative Engine Optimization': ['/blog/geo-optimization-prepare-business-ai-search', '/services/geo-ai-search', '/blog/seo-trends-2026-ai-geo-future'],
        'Case Studies': ['/blog/'],
        'Advanced SEO': ['/blog/complete-seo-guide-bangladesh-businesses-2026'],
        'SEO Services': ['/blog/hiring-seo-expert-dhaka-better-roi-than-paid-ads', '/blog/seo-expert-vs-seo-agency-dhaka-which-is-right'],
        'Industry SEO': ['/blog/complete-seo-guide-bangladesh-businesses-2026', '/blog/'],
    }
    urls = pillar_urls.get(pillar, ['/blog/'])
    for url in urls:
        if url in content:
            return f"Links to {url}"
    return None

for slug in target_slugs:
    post_text = None
    for pt in posts_raw:
        if f'slug: "{slug}"' in pt:
            post_text = pt
            break
    
    if not post_text:
        print(f"## Post: {slug}")
        print(f"| Check | Status | Details |")
        print(f"|-------|--------|---------|")
        print(f"| **ERROR** | ❌ | Post not found in parsed array ({len(posts_raw)} posts total) |")
        print()
        continue
    
    title = extract_field(post_text, "title")
    excerpt = extract_field(post_text, "excerpt")
    date = extract_field(post_text, "date")
    tags = extract_tags(post_text)
    content = extract_content(post_text)
    
    if not title:
        print(f"## Post: {slug}")
        print(f"| **ERROR** | ❌ | Could not extract title. Post text length: {len(post_text)} chars |")
        print()
        continue
    
    # A. TF-IDF Coverage
    keyword = KEYWORD_OVERRIDES.get(slug, "")
    if not keyword:
        kw_count = 0
    else:
        kw_count = count_keyword(content, keyword)
    tfidf_status = "✅" if kw_count >= 5 else "❌"
    
    # B. Semantic Entity Coverage
    expected_entities = ['Dhaka', 'Bangladesh']
    tag_lower = [t.lower() for t in tags]
    
    if any(t in ['e-commerce seo', 'daraz', 'shopify', 'ecommerce'] for t in tag_lower):
        expected_entities.extend(['e-commerce'])
    if any('link building' in t for t in tag_lower):
        expected_entities.extend(['backlink'])
    if any(t in ['local seo', 'gbp', 'google maps'] for t in tag_lower):
        expected_entities.extend(['Google Business Profile'])
    if any(t in ['technical seo', 'core web vitals'] for t in tag_lower):
        expected_entities.extend(['Core Web Vitals'])
    if any('case study' in t for t in tag_lower):
        expected_entities.extend(['traffic', 'organic'])
    if any(t in ['seo', 'bangladesh seo'] for t in tag_lower):
        expected_entities.extend(['Google'])
    if any('featured snippet' in t for t in tag_lower):
        expected_entities.extend(['Google'])
    if any('knowledge panel' in t for t in tag_lower):
        expected_entities.extend(['Google'])
    if any('garments' in t for t in tag_lower):
        expected_entities.extend(['RMG'])
    if any('locksmith' in t for t in tag_lower):
        pass  # Locksmith - local entity fine
    if any('transportation' in t for t in tag_lower):
        pass
    if any('automotive' in t for t in tag_lower):
        pass
    if any('smm panel' in t for t in tag_lower):
        pass
    if any('photographers' in t for t in tag_lower):
        expected_entities.extend(['Google', 'local'])
    
    expected_entities = list(set(expected_entities))
    
    missing_entities = []
    for entity in expected_entities:
        if entity.lower() not in content.lower():
            missing_entities.append(entity)
    
    entities_status = "✅" if not missing_entities else "❌"
    
    # C. Pillar-Cluster Alignment
    pillar = extract_pillar_topic(tags)
    pillar_link = has_pillar_link(content, tags)
    pillar_status = "✅" if pillar_link else "❌"
    
    # D. AEO/GEO Optimization
    q_headings = count_question_headings(content)
    aeo_status = "✅" if q_headings >= 2 else "❌"
    
    # E. Internal Linking
    internal_links = count_internal_links(content)
    links_status = "✅" if internal_links >= 3 else "❌"
    
    # F. Schema Ready
    schema_missing = []
    if not title:
        schema_missing.append("title")
    if not excerpt:
        schema_missing.append("excerpt")
    if not date:
        schema_missing.append("date")
    schema_status = "✅" if not schema_missing else "❌"
    
    # Output report
    print(f"## Post: {slug}")
    short_title = (title[:65] + '...') if len(title) > 65 else title
    print(f"**Title:** {short_title}")
    print(f"**Tags:** {', '.join(tags)}")
    print()
    print(f"| Check | Status | Details |")
    print(f"|-------|--------|---------|")
    print(f"| TF-IDF: _{keyword}_ | {tfidf_status} | {kw_count} occurrences in content |")
    
    if not missing_entities:
        print(f"| Entity Coverage | ✅ | All expected entities present |")
    else:
        print(f"| Entity Coverage | {entities_status} | Missing: {', '.join(missing_entities)} |")
    
    if pillar_link:
        print(f"| Pillar Link ({pillar}) | ✅ | {pillar_link} |")
    else:
        print(f"| Pillar Link ({pillar}) | ❌ | No pillar link found |")
    
    print(f"| AEO/GEO Headings | {aeo_status} | {q_headings} question-based headings found |")
    print(f"| Internal Links | {links_status} | {internal_links} internal links |")
    
    if not schema_missing:
        print(f"| Schema Readyness | ✅ | title, excerpt, and date all present |")
    else:
        print(f"| Schema Readyness | ❌ | Missing: {', '.join(schema_missing)} |")
    
    # Fix instructions
    print(f"\n### Fix instructions:")
    fixes = []
    if kw_count < 5:
        fixes.append(f"- 🔴 **TF-IDF Thin**: Keyword \"{keyword}\" appears only {kw_count} times (need ≥5). Add more natural instances throughout the content.")
    if missing_entities:
        fixes.append(f"- 🔴 **Missing Entities**: Add: {', '.join(missing_entities)}. Include naturally in paragraphs or headings.")
    if not pillar_link:
        fixes.append(f"- 🔴 **Missing Pillar Link**: No link to the \"{pillar}\" pillar page found. Add a contextual link.")
    if q_headings < 2:
        fixes.append(f"- 🔴 **Low AEO/GEO**: Only {q_headings} question-based headings found (need ≥2). Add FAQ-style H2s starting with How/What/Why/When/Where/Can/Do/Is/Are.")
    if internal_links < 3:
        fixes.append(f"- 🔴 **Thin Internal Linking**: Only {internal_links} internal links (need ≥3). Link to related blog posts, services, or location pages.")
    if schema_missing:
        fixes.append(f"- 🔴 **Incomplete Schema**: Missing fields: {', '.join(schema_missing)}. Set these in the post metadata.")
    
    if not fixes:
        print(f"- ✅ All checks passed! No fixes needed.")
    else:
        for fix in fixes:
            print(f"  {fix}")
    
    print()
