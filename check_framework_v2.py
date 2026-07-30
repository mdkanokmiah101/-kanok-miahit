#!/usr/bin/env python3
"""Framework checker for blog posts in data.js - v2 with proper parsing"""

import re
import sys
import json

with open('src/app/blog/data.js', 'r') as f:
    content = f.read()

modified_slugs = [
    "link-building-strategies-bangladesh-market",
    "seo-garments-textile-industry-b2b-lead-generation",
    "google-business-profile-optimization-guide-bangladesh",
    "mobile-seo-optimization-bangladesh-mobile-first-era",
    "locksmith-dundee-seo-case-study",
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

# Parse by locating each post section
# Split on slug to get each post definition
sections = content.split("slug:")

posts = {}
for section in sections[1:]:  # Skip content before first slug
    slug_match = re.match(r'\s*"([^"]+)"', section)
    if not slug_match:
        continue
    slug = slug_match.group(1)
    
    # Extract fields
    title_match = re.search(r'title:\s*\n\s*"([^"]+)"', section)
    if not title_match:
        title_match = re.search(r'title:\s*"([^"]+)"', section)
    title = title_match.group(1) if title_match else ""
    
    date_match = re.search(r'date:\s*"([^"]+)"', section)
    date = date_match.group(1) if date_match else ""
    
    excerpt_match = re.search(r'excerpt:\s*\n\s*"([^"]+)"', section)
    if not excerpt_match:
        excerpt_match = re.search(r'excerpt:\s*"([^"]+)"', section)
    excerpt = excerpt_match.group(1) if excerpt_match else ""
    
    tags_match = re.search(r'tags:\s*\[([^\]]+)\]', section, re.DOTALL)
    tags = []
    if tags_match:
        tag_str = tags_match.group(1)
        tags = [t.strip().strip('"').strip("'") for t in tag_str.split(',') if t.strip()]
    
    # Content is everything between content: ` and ending `,
    content_match = re.search(r'content:\s*`\s*\n?(.*?)`\s*,', section, re.DOTALL)
    content_text = content_match.group(1) if content_match else ""
    
    if excerpt:
        posts[slug] = {
            'title': title,
            'date': date,
            'excerpt': excerpt,
            'tags': tags,
            'content': content_text,
        }

print(f"Parsed {len(posts)} posts total", file=sys.stderr)

# For each modified slug, run checks
results = {}

stopwords = {'a', 'an', 'the', 'for', 'of', 'in', 'to', 'is', 'are', 'was', 'were', 
             'your', 'our', 'my', 'its', 'his', 'her', 'their', 'at', 'on', 'by', 'with',
             'and', 'or', 'but', 'not', 'do', 'does', 'did', 'has', 'have', 'had', 'from',
             'why', 'how', 'what', 'when', 'where', 'which', 'who', 'whom', 'whose',
             'that', 'this', 'these', 'those', 'be', 'been', 'being', 'have', 'has',
             'had', 'having', 'will', 'would', 'could', 'should', 'may', 'might', 'shall',
             'can', 'need', 'dare', 'ought', 'used', 'about', 'into', 'through', 'during',
             'before', 'after', 'above', 'below', 'between', 'out', 'off', 'over', 'under',
             'again', 'further', 'then', 'once', 'here', 'there', 'all', 'each', 'every',
             'both', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'only',
             'own', 'same', 'so', 'than', 'too', 'very', 'just', 'because', 'as', 'until',
             'while', 'if', 'else', 'up', 'down', 'also'}

for slug in modified_slugs:
    if slug not in posts:
        print(f"⚠️  Post not found: {slug}", file=sys.stderr)
        continue
    
    post = posts[slug]
    title = post['title']
    content_text = post['content']
    content_lower = content_text.lower()
    
    checks = {}
    
    # A. TF-IDF Coverage
    # Extract primary keyword from title - first meaningful 1-2 word phrase
    words = title.split()
    keyword_parts = []
    for w in words:
        w_clean = w.strip('.,;:!?()[]{}""\'').strip()
        if w_clean.lower() not in stopwords and len(w_clean) > 2:
            keyword_parts.append(w_clean)
            if len(keyword_parts) >= 2:
                break
    
    primary_keyword = ' '.join(keyword_parts) if keyword_parts else words[0] if words else title
    kw_lower = primary_keyword.lower()
    
    # Count occurrences of the exact keyword
    exact_count = content_lower.count(kw_lower)
    
    # Also check individual words if multi-word keyword
    if len(kw_lower.split()) >= 2:
        # Try the first word of the keyword
        first_word = kw_lower.split()[0]
        approx_count = content_lower.count(first_word)
    else:
        approx_count = exact_count
    
    # For brand names, also try the brand+keyword variation
    checks['tfidf'] = {
        'keyword': primary_keyword,
        'exact_occurrences': exact_count,
        'approx_occurrences': approx_count,
        'pass': exact_count >= 5 or approx_count >= 10
    }
    
    # B. Semantic Entity Coverage
    required_entities = {
        'location_dhaka': ['dhaka', 'bangladesh'],
        'service_type': ['seo', 'local seo', 'technical seo'],
        'author': ['kanok miah'],
    }
    
    missing_entities = []
    for entity_group, keywords in required_entities.items():
        found = any(kw in content_lower for kw in keywords)
        if not found:
            entity_names = {
                'location_dhaka': 'Dhaka/Bangladesh (location)',
                'service_type': 'SEO services (service type)',
                'author': 'Kanok Miah (author)',
            }
            missing_entities.append(entity_names.get(entity_group, entity_group))
    
    checks['entities'] = {
        'pass': len(missing_entities) == 0,
        'missing': missing_entities if missing_entities else 'None',
    }
    
    # C. Pillar-Cluster Alignment
    pillar_links = [
        '/blog/complete-seo-guide-bangladesh-businesses-2026',
        '/blog/local-seo-tips-dhaka-businesses-google-maps',
        '/blog/technical-seo-checklist-bangladeshi-websites',
        '/blog/why-ecommerce-store-needs-seo-bangladesh',
        '/blog/link-building-strategies-bangladesh-market',
        '/blog/mobile-seo-optimization-bangladesh-mobile-first-era',
    ]
    
    pillar_names = {
        '/blog/complete-seo-guide-bangladesh-businesses-2026': 'Complete SEO Guide',
        '/blog/local-seo-tips-dhaka-businesses-google-maps': 'Local SEO Guide',
        '/blog/technical-seo-checklist-bangladeshi-websites': 'Technical SEO Guide',
        '/blog/why-ecommerce-store-needs-seo-bangladesh': 'E-commerce SEO Guide',
        '/blog/link-building-strategies-bangladesh-market': 'Link Building Guide',
        '/blog/mobile-seo-optimization-bangladesh-mobile-first-era': 'Mobile SEO Guide',
    }
    
    linked_pillar_found = None
    for link in pillar_links:
        if link in content_text:
            linked_pillar_found = pillar_names[link]
            break
    
    # Identify pillar from tags
    identified_pillar = 'Uncategorized'
    tag_to_pillar = {
        'link building': 'Link Building',
        'local seo': 'Local SEO',
        'technical seo': 'Technical SEO',
        'e-commerce seo': 'E-commerce SEO',
        'mobile seo': 'Mobile SEO',
        'seo guide': 'SEO Guide',
        'digital marketing': 'SEO Guide',
        'geo': 'GEO/AI Search',
        'ai search': 'GEO/AI Search',
        'google maps': 'Local SEO',
        'gbp': 'Local SEO',
        'daraz': 'E-commerce SEO',
        'shopify': 'E-commerce SEO',
        'core web vitals': 'Technical SEO',
    }
    
    for tag in tags:
        tag_lower = tag.lower()
        for key, pillar in tag_to_pillar.items():
            if key in tag_lower:
                identified_pillar = pillar
                break
        if identified_pillar != 'Uncategorized':
            break
    
    checks['pillar'] = {
        'pass': linked_pillar_found is not None,
        'identified_pillar': identified_pillar,
        'linked_pillar': linked_pillar_found if linked_pillar_found else 'None'
    }
    
    # D. AEO/GEO Optimization
    question_heading_pattern = re.compile(
        r'^###\s+(How|What|Why|When|Where|Can|Do|Is|Are|Does|Which|Who|Whose|Will|Would|Could|Should|Has|Have)\b',
        re.MULTILINE | re.IGNORECASE
    )
    question_heading_matches = question_heading_pattern.findall(content_text)
    unique_question_words = list(set(q.capitalize() for q in question_heading_matches))
    
    checks['aeo_geo'] = {
        'pass': len(question_heading_matches) >= 2,
        'question_heading_count': len(question_heading_matches),
        'unique_question_words': unique_question_words
    }
    
    # E. Internal Linking
    md_links = re.findall(r'\[([^\]]+)\]\(([^\)]+)\)', content_text)
    internal_md_links = []
    for text, link in md_links:
        if link.startswith('/') and not link.startswith('//'):
            internal_md_links.append(link)
    
    unique_internal = list(set(internal_md_links))
    
    checks['internal_links'] = {
        'pass': len(unique_internal) >= 3,
        'total_unique': len(unique_internal),
        'sample_links': unique_internal[:5]
    }
    
    # F. Schema - Check if post has title, excerpt, date
    schema_ready = True
    schema_missing = []
    
    if not post.get('title'):
        schema_missing.append('title')
        schema_ready = False
    if not post.get('excerpt'):
        schema_missing.append('excerpt')
        schema_ready = False
    if not post.get('date'):
        schema_missing.append('date')
        schema_ready = False
    
    checks['schema'] = {
        'pass': schema_ready,
        'missing_fields': schema_missing if schema_missing else 'None'
    }
    
    results[slug] = {
        'title': title,
        'tags': tags,
        'checks': checks
    }

# Output as formatted report
for slug, data in results.items():
    c = data['checks']
    t = c['tfidf']
    e = c['entities']
    p = c['pillar']
    a = c['aeo_geo']
    il = c['internal_links']
    s = c['schema']
    
    print(f"\n## Post: {slug}")
    print(f"**Title:** {data['title']}")
    print(f"| Check | Status | Details |")
    print(f"|-------|--------|---------|")
    
    kw_status = "✅" if t['pass'] else "❌"
    kw_detail = f"'{t['keyword']}' — {t['exact_occurrences']} exact, {t['approx_occurrences']} approx occurrences"
    print(f"| TF-IDF: {t['keyword']} | {kw_status} | {kw_detail} |")
    
    ent_status = "✅" if e['pass'] else "❌"
    ent_detail = f"Missing: {e['missing']}" if e['missing'] != 'None' else "All entities present (Dhaka/Bangladesh, SEO, Kanok Miah)"
    print(f"| Entities | {ent_status} | {ent_detail} |")
    
    pil_status = "✅" if p['pass'] else "❌"
    pil_detail = f"Links to: {p['linked_pillar']}" if p['linked_pillar'] != 'None' else f"No pillar link (belongs to: {p['identified_pillar']})"
    print(f"| Pillar Link | {pil_status} | {pil_detail} |")
    
    aeo_status = "✅" if a['pass'] else "❌"
    aeo_detail = f"{a['question_heading_count']} question headings"
    print(f"| AEO/GEO | {aeo_status} | {aeo_detail} |")
    
    il_status = "✅" if il['pass'] else "❌"
    il_detail = f"{il['total_unique']} unique internal links"
    print(f"| Internal Links | {il_status} | {il_detail} |")
    
    sch_status = "✅" if s['pass'] else "❌"
    sch_detail = f"Missing: {s['missing_fields']}" if s['missing_fields'] != 'None' else "All fields set (title, excerpt, date)"
    print(f"| Schema Ready | {sch_status} | {sch_detail} |")
    
    # Generate fix suggestions
    fixes = []
    if not t['pass']:
        fixes.append(f"- **TF-IDF too thin**: Use '{t['keyword']}' at least 5 times in content (currently {t['exact_occurrences']})")
    if not e['pass']:
        fixes.append(f"- **Missing entities**: Add mentions of: {', '.join(e['missing'])}")
    if not p['pass']:
        fixes.append(f"- **No pillar link**: Add a link to the relevant pillar page (e.g., /blog/{p['identified_pillar'].lower().replace(' ','-')}-...) in the content")
    if not a['pass']:
        fixes.append(f"- **Too few question headings**: Add 2+ question-based headings (How, What, Why, etc.) — currently {a['question_heading_count']}")
    if not il['pass']:
        fixes.append(f"- **Too few internal links**: Add more internal links to reach 3+ (currently {il['total_unique']})")
    if not s['pass']:
        fixes.append(f"- **Schema fields missing**: Set {', '.join(s['missing_fields'])} in the post object")
    
    if fixes:
        print(f"\n### Fix instructions:")
        for fix in fixes:
            print(fix)
    else:
        print("\n✅ All checks passed — no fixes needed.")
