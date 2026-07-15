#!/usr/bin/env python3
"""
Content Framework Enforcer — kanokmiah.com.bd
Reads src/app/blog/data.js and runs framework checks on modified posts.
"""
import re
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Read data.js
data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src/app/blog/data.js')
with open(data_path, 'r', encoding='utf-8') as f:
    raw = f.read()

# Slugs modified in last 48 hours
modified_slugs = [
    'google-search-console-performance-guide',
    'content-marketing-seo-friendly-content-writing',
    'keyword-research-bangladesh-market',
    'link-building-bangladesh-strategies',
    'ecommerce-seo-daraz-shopify-guide',
    'technical-seo-core-web-vitals-optimization',
    'seo-trends-2026-ai-geo-future',
    'local-seo-dhaka-google-maps-ranking',
    'seo-bangla-beginners-guide-google-ranking',
    'international-seo-bangladesh-exporters-global-buyers',
    'content-marketing-strategy-bangladeshi-brands-seo',
    'mobile-seo-optimization-bangladesh-mobile-first-era',
    'seo-real-estate-developers-dhaka',
    'seo-vs-google-ads-whats-best-bangladesh-businesses',
    'google-business-profile-optimization-guide-bangladesh',
    'seo-garments-textile-industry-b2b-lead-generation',
    'geo-optimization-prepare-business-ai-search',
    'link-building-strategies-bangladesh-market',
    'how-to-choose-right-seo-agency-bangladesh',
    'technical-seo-checklist-bangladeshi-websites',
    'why-ecommerce-store-needs-seo-bangladesh',
    'local-seo-tips-dhaka-businesses-google-maps',
    'complete-seo-guide-bangladesh-businesses-2026'
]

def extract_post(raw, slug):
    """Extract a post object from data.js by slug."""
    # Find the slug position
    slug_pattern = re.compile(r'slug:\s*"{}"'.format(re.escape(slug)))
    m = slug_pattern.search(raw)
    if not m:
        return None
    
    start = m.start()
    
    # Find the post boundary: go back to find the opening { and forward to find the closing },
    # Posts are in format: { slug: "...", title: "...", ..., content: `...`, }
    
    # Find the opening brace before slug
    brace_start = raw.rfind('{', m.start() - 200, m.start())
    if brace_start == -1:
        return None
    
    # Find the content field - it uses template literals with backticks
    # content: `...`
    content_match = re.search(r'content:\s*`', raw[m.start():])
    if not content_match:
        return None
    
    content_start_in_post = m.start() + content_match.end()
    
    # Now find the closing backtick that ends the content
    # This is tricky because content may contain escaped backticks
    # We'll track nesting depth of backticks
    content_text = raw[content_start_in_post:]
    
    # Find the closing backtick — it's followed by `,` (possibly with whitespace and trailing comment)
    # Pattern: backtick, optional whitespace, comma, optional whitespace, optional comment (//...), newline, whitespace, }
    end_match = re.search(r'`\s*,\s*(?://[^\n]*)?\s*\n\s*\}', content_text)
    if end_match:
        content_end = content_start_in_post + end_match.start()
        raw_content = raw[content_start_in_post:content_end]
    else:
        return None
    
    # Now extract the post block from { to },
    post_end_in_raw = content_start_in_post + end_match.end() - 1  # past the closing }
    post_block = raw[brace_start:post_end_in_raw + 1]
    
    # Extract fields
    def extract_field(pattern):
        fm = re.search(pattern, post_block)
        return fm.group(1) if fm else ''
    
    title = extract_field(r'title:\s*"([^"]*)"')
    excerpt = extract_field(r'excerpt:\s*"([^"]*)"')
    date = extract_field(r'date:\s*"([^"]*)"')
    
    tags_match = re.search(r'tags:\s*\[([^\]]*)\]', post_block)
    tags = []
    if tags_match:
        tags_str = tags_match.group(1)
        tags = [t.strip().strip('"').strip("'") for t in tags_str.split(',')]
    
    return {
        'slug': slug,
        'title': title,
        'excerpt': excerpt,
        'date': date,
        'tags': tags,
        'content': raw_content
    }

def extract_keywords(title):
    """Extract meaningful keywords from title for TF-IDF-like check.
    Returns a list of keyword phrases (bigrams and trigrams) to search for."""
    # For Bengali titles, extract individual meaningful words
    # For English titles, extract bigrams/trigrams
    
    import unicodedata
    
    def is_bengali_char(c):
        """Check if a character is Bengali."""
        try:
            return '\u0980' <= c <= '\u09FF'
        except:
            return False
    
    def has_bengali(text):
        return any(is_bengali_char(c) for c in text)
    
    if has_bengali(title):
        # Bengali title: extract meaningful word pairs that appear in content
        # Remove emojis and special chars
        cleaned = re.sub(r'[^\u0980-\u09FF\w\s]', ' ', title)
        words = [w for w in cleaned.split() if len(w) > 2]
        keywords = []
        # Individual significant words
        for w in words:
            if w.lower() not in ['এবং', 'জন্য', 'কীভাবে', 'কি', 'যে', 'এই', 'তা', 'থেকে', 'করে', 'হবে', 'করে']:
                keywords.append(w)
        # Bigrams
        for i in range(len(words) - 1):
            keywords.append(words[i] + ' ' + words[i+1])
        # Also include 'seo' and 'bangladesh' if present as individual checks
        for w in ['seo', 'এসইও', 'bangladesh', 'বাংলাদেশ', 'dhaka', 'ঢাকা']:
            if w.lower() in title.lower() or w in title:
                keywords.append(w)
        return keywords
    
    # English title
    cleaned = re.sub(r'^(Complete |Ultimate |Best |Top |Essential |Expert |How to |What |Why |When |Where |) ', '', title, flags=re.IGNORECASE)
    words = [w for w in re.split(r'[\s,:-]+', cleaned) if len(w) > 2]
    if not words:
        return [cleaned.lower() if cleaned else title.lower()]
    
    keywords = []
    # Bigrams
    for i in range(len(words) - 1):
        keywords.append(words[i] + ' ' + words[i+1])
    # Trigram (first 3)
    if len(words) >= 3:
        keywords.append(' '.join(words[:3]))
    # Individual significant words (filter out stop words)
    stop_words = {'for', 'the', 'and', 'your', 'with', 'that', 'this', 'from', 'what', 'how', 'why', 'when', 'are', 'is', 'its'}
    for w in words[:4]:
        if w.lower() not in stop_words:
            keywords.append(w)
    
    return keywords

def count_keyword(content, keywords):
    """Count occurrences of any of the keywords in content.
    Returns (primary_phrase, count) where primary_phrase is the best match."""
    if not content or not keywords:
        return ('', 0)
    
    c = content.lower()
    best_count = 0
    best_phrase = keywords[0] if keywords else ''
    
    for kw in keywords:
        pattern = re.escape(kw.lower())
        matches = re.findall(pattern, c)
        count = len(matches)
        if count > best_count:
            best_count = count
            best_phrase = kw
    
    return (best_phrase, best_count)

def count_question_headings(content):
    """Count question-based headings (How, What, Why, When, Where, Can, Do, Is, Are)."""
    if not content:
        return 0
    question_words = ['How', 'What', 'Why', 'When', 'Where', 'Can', 'Do', 'Is', 'Are', 'Does', 'Which', 'Who']
    count = 0
    for line in content.split('\n'):
        line = line.strip()
        if re.match(r'^#{1,4}\s+', line):
            heading_text = re.sub(r'^#+\s*', '', line).strip()
            if any(heading_text.startswith(qw) for qw in question_words):
                count += 1
    return count

def count_internal_links(content):
    """Count internal links (links starting with /)."""
    if not content:
        return 0
    return len(re.findall(r'\[([^\]]*)\]\(/([^)]*)\)', content))

def check_missing_entities(content, tags):
    """Check for missing key entities."""
    if not content:
        return ['No content to analyze']
    missing = []
    c = content.lower()
    
    # Location entities
    if 'dhaka' not in c and 'bangladesh' not in c:
        missing.append('Location reference (Dhaka/Bangladesh)')
    
    # Service entity
    if 'seo' not in c and 'search engine optimization' not in c:
        missing.append('SEO/service type reference')
    
    # Tag-specific checks
    tag_str = ' '.join(tags).lower()
    
    checks = [
        ('local', ['local seo', 'local search']),
        ('ecommerce', ['ecommerce', 'e-commerce']),
        ('e-commerce', ['ecommerce', 'e-commerce']),
        ('technical', ['technical seo']),
        ('keyword', ['keyword']),
        ('link building', ['link building', 'backlink']),
        ('content marketing', ['content marketing', 'content writing']),
        ('content writing', ['content marketing', 'content writing']),
        ('geo', ['geo', 'generative engine']),
        ('generative', ['geo', 'generative engine']),
        ('mobile', ['mobile seo', 'mobile optimization']),
        ('google business', ['google business profile', 'gbp']),
        ('real estate', ['real estate']),
        ('garment', ['garment', 'textile']),
        ('seo agency', ['seo agency', 'seo expert']),
        ('google ads', ['google ads', 'ppc']),
        ('search console', ['search console', 'google search console']),
        ('beginners', ['beginners', 'guide', 'bangla']),
        ('bangla', ['bangla', 'bengali']),
    ]
    
    for tag_term, content_terms in checks:
        if tag_term in tag_str:
            if not any(t in c for t in content_terms):
                missing.append(f'"{tag_term}" mention (tagged but not in content)')
    
    return missing

def find_pillar_link(content):
    """Find pillar/service/location links in content."""
    if not content:
        return None
    patterns = [
        r'/blog/complete-seo-guide-bangladesh-businesses-2026',
        r'/services/',
        r'/industries/'
    ]
    for p in patterns:
        m = re.search(p, content)
        if m:
            return m.group(0)
    return None

def determine_pillar(tags):
    """Determine pillar topic from tags."""
    t = ' '.join(tags).lower()
    if 'local seo' in t or 'local search' in t or 'google maps' in t: return 'Local SEO'
    if 'technical' in t or 'core web vitals' in t or 'page speed' in t: return 'Technical SEO'
    if 'ecommerce' in t or 'e-commerce' in t or 'shopify' in t or 'daraz' in t: return 'E-commerce SEO'
    if 'link building' in t or 'backlink' in t: return 'Link Building'
    if 'keyword' in t: return 'Keyword Research'
    if 'content' in t and ('market' in t or 'writ' in t or 'strateg' in t): return 'Content Marketing'
    if 'geo' in t or 'generative' in t or 'ai' in t: return 'GEO/AI Search'
    if 'international' in t or 'export' in t: return 'International SEO'
    if 'mobile' in t: return 'Mobile SEO'
    if 'google business' in t or 'gbp' in t or 'google my business' in t: return 'Google Business Profile'
    if 'guide' in t or 'beginners' in t or 'bangla' in t: return 'SEO Basics'
    if 'real estate' in t: return 'Real Estate SEO'
    if 'garment' in t or 'textile' in t or 'b2b' in t: return 'B2B/Industry SEO'
    if 'agency' in t or 'expert' in t: return 'SEO Agency/Expert'
    if 'google ads' in t or 'ppc' in t or 'paid' in t: return 'SEO vs PPC'
    if 'search console' in t or 'performance' in t: return 'SEO Tools'
    return 'General SEO'

print("# Content Framework Enforcement Report")
print()
print(f"Generated: (cron check — kanokmiah.com.bd)")
print()
print(f"Posts modified in last 48 hours: {len(modified_slugs)}")
print()

results = []
errors = []

for slug in modified_slugs:
    post = extract_post(raw, slug)
    if not post:
        errors.append(slug)
        continue
    
    content = post['content']
    title = post['title']
    tags = post['tags']
    excerpt = post['excerpt']
    date = post['date']
    
    if not content or len(content.strip()) < 50:
        errors.append(slug + " (content too short or empty)")
        continue
    
    # A. TF-IDF Coverage
    keywords = extract_keywords(title)
    best_keyword, kw_count = count_keyword(content, keywords)
    
    # B. Entities
    missing = check_missing_entities(content, tags)
    
    # C. Pillar
    pillar = determine_pillar(tags)
    pillar_link = find_pillar_link(content)
    
    # D. AEO/GEO
    q_headings = count_question_headings(content)
    
    # E. Internal Links
    internal_links = count_internal_links(content)
    
    # F. Schema
    schema_ok = bool(title and excerpt and date)
    schema_missing = []
    if not title: schema_missing.append('title')
    if not excerpt: schema_missing.append('excerpt')
    if not date: schema_missing.append('date')
    
    results.append({
        'slug': slug,
        'title': title,
        'pillar': pillar,
        'checks': {
            'tfidf': {'pass': kw_count >= 5, 'keyword': best_keyword, 'count': kw_count},
            'entities': {'pass': len(missing) == 0, 'missing': missing},
            'pillar_link': {'pass': pillar_link is not None, 'link': pillar_link or 'None'},
            'aeo': {'pass': q_headings >= 2, 'count': q_headings},
            'internal_links': {'pass': internal_links >= 3, 'count': internal_links},
            'schema': {'pass': schema_ok, 'missing': schema_missing},
        }
    })

# Print results
all_passed = 0
all_failed = 0

for r in results:
    c = r['checks']
    checks_pass = all(v['pass'] for v in c.values())
    if checks_pass:
        all_passed += 1
    else:
        all_failed += 1
    
    print(f"## Post: {r['slug']}")
    print(f"**Title:** {r['title']}")
    print(f"**Pillar:** {r['pillar']}")
    print()
    print(f"| Check | Status | Details |")
    print(f"|-------|--------|--------|")
    print(f"| TF-IDF: \"{c['tfidf']['keyword']}\" | {'✅' if c['tfidf']['pass'] else '❌'} | {c['tfidf']['count']} occurrences{' (need ≥5)' if not c['tfidf']['pass'] else ''} |")
    print(f"| Entities | {'✅' if c['entities']['pass'] else '❌'} | {'All key entities present' if c['entities']['pass'] else 'Missing: ' + ', '.join(c['entities']['missing'])} |")
    print(f"| Pillar Link | {'✅' if c['pillar_link']['pass'] else '❌'} | {'Links to: ' + c['pillar_link']['link'] if c['pillar_link']['pass'] else 'No pillar/service/location link found'} |")
    print(f"| AEO/GEO | {'✅' if c['aeo']['pass'] else '❌'} | {c['aeo']['count']} question heading(s){' (need ≥2)' if not c['aeo']['pass'] else ''} |")
    print(f"| Internal Links | {'✅' if c['internal_links']['pass'] else '❌'} | {c['internal_links']['count']} total{' (need ≥3)' if not c['internal_links']['pass'] else ''} |")
    print(f"| Schema Ready | {'✅' if c['schema']['pass'] else '❌'} | {'All fields set (title, excerpt, date)' if c['schema']['pass'] else 'Missing: ' + ', '.join(c['schema']['missing'])} |")
    
    print()
    print("### Fix instructions:")
    has_fixes = False
    
    if not c['tfidf']['pass']:
        has_fixes = True
        print(f"- **TF-IDF too thin:** Increase \"{c['tfidf']['keyword']}\" occurrences to ≥5. Add the keyword naturally in headings, first paragraph, and conclusion.")
    if not c['entities']['pass']:
        has_fixes = True
        print(f"- **Missing entities:** Add references to: {', '.join(c['entities']['missing'])}.")
    if not c['pillar_link']['pass']:
        has_fixes = True
        print(f"- **Missing pillar link:** Add a link to the pillar page (complete-seo-guide, /services/, or /industries/). This \"{r['pillar']}\" post should reference its pillar topic.")
    if not c['aeo']['pass']:
        has_fixes = True
        print(f"- **AEO/GEO under-optimized:** Add {2 - c['aeo']['count']} more question-based headings (starting with How/What/Why/When/Where/Can/Do/Is/Are).")
    if not c['internal_links']['pass']:
        has_fixes = True
        print(f"- **Too few internal links:** Add {3 - c['internal_links']['count']} more internal links to related blog posts, services, or location pages.")
    if not c['schema']['pass']:
        has_fixes = True
        print(f"- **Schema fields missing:** Set {', '.join(c['schema']['missing'])} in the post metadata.")
    
    if not has_fixes:
        print("All checks passed. No fixes needed.")
    
    print()
    print("---")
    print()

# Summary
print("## Summary")
print(f"- ✅ All checks passed: **{all_passed}/{len(results)}** posts")
print(f"- ❌ Needs fixes: **{all_failed}/{len(results)}** posts")
if errors:
    print(f"- ❌ Extraction errors: {len(errors)} posts:")
    for e in errors:
        print(f"  - {e}")
print()

# If all pass, short summary
if all_failed == 0 and len(errors) == 0:
    print("🎉 All posts comply with the content framework. No action needed.")
