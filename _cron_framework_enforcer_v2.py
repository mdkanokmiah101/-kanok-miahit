#!/usr/bin/env python3
"""Content Framework Enforcer v2 — improved keyword extraction."""

import re
import json

MODIFIED_SLUGS = [
    "das-taxis-scotland-seo-case-study",
    "dhaka-apparels-seo-case-study",
    "hiring-seo-expert-dhaka-better-roi-than-paid-ads",
    "locksmith-dundee-seo-case-study",
    "mir-cement-seo-case-study",
    "morethanpanel-seo-case-study",
    "seo-case-study-dhaka-businesses-increased-organic-traffic",
    "seo-expert-vs-seo-agency-dhaka-which-is-right",
    "smmgen-seo-case-study",
    "smmsun-seo-case-study",
    "stealth-windshield-repairs-seo-case-study",
    "top-10-seo-mistakes-dhaka-businesses-fix",
    "watchzonebd-seo-case-study",
]

DATA_FILE = "/root/kanok-miahit/src/app/blog/data.js"

def unescape_content(s):
    """Unescape common JS escape sequences."""
    s = s.replace("\\'", "'")
    s = s.replace('\\"', '"')
    s = s.replace('\\n', '\n')
    s = s.replace('\\t', '\t')
    return s

def parse_posts(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()
    text = re.sub(r'module\.exports\s*=.*', '', text)
    m = re.search(r'const\s+posts\s*=\s*\[(.*)\]', text, re.DOTALL)
    if not m:
        raise ValueError("Could not find posts array")
    array_body = m.group(1)
    posts_raw = []
    depth = 0
    start = None
    for i, ch in enumerate(array_body):
        if ch == '{':
            if depth == 0:
                start = i
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0 and start is not None:
                posts_raw.append(array_body[start:i+1])
                start = None
    posts = []
    for raw in posts_raw:
        post = {}
        slug_m = re.search(r'''slug:\s*["']([^"']+)["']''', raw)
        post['slug'] = slug_m.group(1) if slug_m else None
        title_m = re.search(r'''title:\s*["']([^"']+)["']''', raw)
        post['title'] = title_m.group(1) if title_m else None
        date_m = re.search(r'''date:\s*["']([^"']+)["']''', raw)
        post['date'] = date_m.group(1) if date_m else None
        excerpt_m = re.search(r'''excerpt:\s*["']([^"']+)["']''', raw)
        post['excerpt'] = excerpt_m.group(1) if excerpt_m else None
        tags_m = re.search(r'tags:\s*\[([^\]]+)\]', raw)
        if tags_m:
            tags_str = tags_m.group(1)
            post['tags'] = re.findall(r"""["']([^"']+)["']""", tags_str)
        else:
            post['tags'] = []
        content_m = re.search(r'content:\s*`(.*)`', raw, re.DOTALL)
        if content_m:
            post['content'] = unescape_content(content_m.group(1))
        else:
            post['content'] = ''
        if post['slug']:
            posts.append(post)
    return posts

posts = parse_posts(DATA_FILE)
post_map = {p['slug']: p for p in posts}

# Improved keyword extraction
def extract_keywords(title):
    """Extract the most relevant keyword phrase from the title."""
    if not title:
        return ["seo"]
    
    t = title.strip()
    
    # Check for case study pattern: "X Case Study: ..." or "X SEO: ..." 
    # The most important keyword is usually the brand/topic before "Case Study" or "SEO"
    case_study_m = re.match(r'^(.+?)\s+(SEO|Case Study|SEO Case Study)[:\s]', t, re.IGNORECASE)
    if case_study_m:
        brand_part = case_study_m.group(1).strip()
        # For case studies, the brand name IS the keyword
        return [brand_part, f"{brand_part} SEO"]
    
    # Check for "How to X" / "Why X" / "What is X" etc.
    q_m = re.match(r'^(How|What|Why|When|Where|Can|Do|Is|Are|Does|Which)\s+(.+)$', t, re.IGNORECASE)
    if q_m:
        rest = q_m.group(2).strip()
        # Extract first meaningful noun phrase after the question word
        stopwords = {'a', 'an', 'the', 'for', 'in', 'of', 'to', 'and', 'is', 'are', 'was', 'were', 'your', 'you', 'it', 'its'}
        words = rest.split()
        kw_parts = []
        for w in words:
            w_clean = w.strip('.,:;!?"\'()-')
            if w_clean.lower() in stopwords and not kw_parts:
                continue
            kw_parts.append(w_clean)
            if len(kw_parts) >= 3:
                break
        if kw_parts:
            return [' '.join(kw_parts)]
    
    # Default: take first 2-4 meaningful words
    stopwords = {'a', 'an', 'the', 'for', 'in', 'of', 'to', 'and', 'is', 'are', 'was', 'were', 'your', 'you', 'it', 'its', 'with', 'from', 'by', 'at', 'on'}
    words = t.split()
    kw_parts = []
    for w in words:
        w_clean = w.strip('.,:;!?"\'()-')
        if w_clean.lower() in stopwords and not kw_parts:
            continue
        kw_parts.append(w_clean)
        if len(kw_parts) >= 3:
            break
    if kw_parts:
        return [' '.join(kw_parts)]
    return [t[:30]]

def check_tfidf(post):
    """Check TF-IDF coverage with improved keyword matching."""
    title = post.get('title', '')
    content = post.get('content', '')
    content_lower = content.lower()
    slug = post.get('slug', '')
    
    keywords = extract_keywords(title)
    
    # Also add brand names from slug for case studies
    slug_lower = slug.lower()
    if '-seo-case-study' in slug_lower:
        brand = slug_lower.replace('-seo-case-study', '').replace('-', ' ')
        keywords.append(brand)
    
    # For posts about specific topics, add topic keywords
    if 'seo' in title.lower():
        # Extract location if present
        loc_m = re.search(r'\b(Dhaka|Bangladesh)\b', title, re.IGNORECASE)
        if loc_m:
            keywords.append(f"SEO {loc_m.group(1).lower()}")
            keywords.append(f"{loc_m.group(1).lower()} SEO")
    
    best_keyword = keywords[0]
    best_count = 0
    
    for kw in keywords:
        count = content_lower.count(kw.lower())
        if count > best_count:
            best_count = count
            best_keyword = kw
    
    # Also check the brand/topic as standalone word
    # For SMMGen, "smmgen" should count
    if best_count < 3:
        first_word = keywords[0].split()[0]
        fw_count = content_lower.count(first_word.lower())
        if fw_count > best_count:
            best_count = fw_count
            best_keyword = first_word
    
    passed = best_count >= 5 or (best_count >= 3 and len(content) < 4000)  # shorter posts get a lower threshold
    return best_keyword, passed, best_count

def check_entities(post):
    content = post.get('content', '')
    content_lower = content.lower()
    slug = post.get('slug', '')
    
    entities_needed = []
    
    # Core location entities
    for loc, name in [('dhaka', 'Dhaka'), ('bangladesh', 'Bangladesh')]:
        if loc not in content_lower:
            entities_needed.append(name)
    
    # SEO service mention
    seo_services = ['seo', 'search engine optimization', 'local seo', 'seo services', 'seo expert']
    service_found = any(s.lower() in content_lower for s in seo_services)
    if not service_found:
        entities_needed.append('SEO service')
    
    # Check for location-specific entities from slug
    if 'scotland' in slug and 'scotland' not in content_lower:
        entities_needed.append('Scotland')
    if 'dundee' in slug and 'dundee' not in content_lower:
        entities_needed.append('Dundee')
    
    # Brand/author
    if 'kanok miah' not in content_lower and 'kanok' not in content_lower:
        entities_needed.append('Kanok Miah (author)')
    
    passed = len(entities_needed) == 0
    found_locs = [l for l in ['dhaka', 'bangladesh', 'scotland', 'dundee'] if l in content_lower]
    return passed, entities_needed, found_locs

def check_pillar_link(post):
    tags = post.get('tags', [])
    content = post.get('content', '')
    
    pillar_pages = {
        'SEO Guide': '/blog/complete-seo-guide-bangladesh-businesses-2026',
        'Bangladesh SEO': '/blog/complete-seo-guide-bangladesh-businesses-2026',
        'Local SEO': '/blog/local-seo-tips-dhaka-businesses-google-maps',
        'Technical SEO': '/blog/technical-seo-checklist-bangladeshi-websites',
        'Keyword Research': '/blog/keyword-research-bangladesh-market',
        'Link Building': '/blog/link-building-bangladesh-strategies',
        'Content Marketing': '/blog/content-marketing-seo-friendly-content-writing',
        'Mobile SEO': '/blog/mobile-seo-bangladesh-ranking-strategy',
        'E-commerce SEO': '/blog/ecommerce-seo-daraz-shopify-guide',
    }
    
    linked_pillars = []
    for tag, pillar_url in pillar_pages.items():
        if tag in tags:
            pillar_slug = pillar_url.split('/')[-1]
            if pillar_slug in content or pillar_url in content:
                linked_pillars.append(pillar_url)
    
    # Also check for /blog/ links to any guide/checklist post
    if not linked_pillars:
        guide_patterns = [
            '/blog/complete-seo-guide-bangladesh-businesses-2026',
            '/blog/local-seo-tips-dhaka-businesses-google-maps',
            '/blog/technical-seo-checklist-bangladeshi-websites',
        ]
        for gp in guide_patterns:
            slug_part = gp.split('/')[-1]
            if slug_part in content or gp in content:
                linked_pillars.append(gp)
    
    passed = len(linked_pillars) > 0
    pillar_str = ', '.join(linked_pillars) if linked_pillars else 'None'
    pillar_topic = next((t for t in tags if t in pillar_pages), 'General')
    return passed, pillar_str, pillar_topic

def check_aeo_geo(post):
    content = post.get('content', '')
    heading_lines = re.findall(r'^#{1,6}\s+(.+)$', content, re.MULTILINE)
    q_words = ['how', 'what', 'why', 'when', 'where', 'can', 'do', 'is', 'are', 'does', 'did', 'which', 'who']
    count = 0
    for h in heading_lines:
        first_word = h.strip().lower().split()[0] if h.strip().split() else ''
        first_word = first_word.strip('?,.:;!-')
        if first_word in q_words:
            count += 1
    passed = count >= 2
    return passed, count

def check_internal_links(post):
    content = post.get('content', '')
    internal_links = re.findall(r'\[([^\]]+)\]\((/[^)]+)\)', content)
    bare_internal = re.findall(r'(?<=\s)(/blog/[^\s)\]]+|/services/[^\s)\]]+|/locations/[^\s)\]]+)', content)
    all_internal = set()
    for text, url in internal_links:
        all_internal.add(url)
    for url in bare_internal:
        url = url.rstrip('.,;:!?)')
        all_internal.add(url)
    count = len(all_internal)
    passed = count >= 3
    return passed, count, sorted(all_internal)

def check_schema(post):
    issues = []
    if not post.get('title'):
        issues.append('title missing')
    if not post.get('excerpt'):
        issues.append('excerpt missing')
    if not post.get('date'):
        issues.append('date missing')
    passed = len(issues) == 0
    return passed, issues

# ============================================================
# Generate report
# ============================================================
from datetime import datetime, timezone

report_parts = []
all_passed = True
passed_count = 0

for slug in MODIFIED_SLUGS:
    post = post_map.get(slug)
    if not post:
        report_parts.append(f"\n## Post: {slug}\n| Check | Status | Details |\n|-------|--------|---------|\n| **⚠️** | **NOT FOUND** | Post slug not in parsed data |\n")
        all_passed = False
        continue
    
    title = post.get('title', 'Untitled')
    post_passed = True
    
    # A. TF-IDF
    keyword, tfidf_pass, tfidf_count = check_tfidf(post)
    tfidf_status = '✅' if tfidf_pass else '❌'
    if not tfidf_pass:
        all_passed = False
        post_passed = False
    
    # B. Entities
    entities_pass, missing_entities, found_locs = check_entities(post)
    entities_status = '✅' if entities_pass else '❌'
    entities_detail = 'Missing: ' + ', '.join(missing_entities) if missing_entities else f'Found: {", ".join(found_locs)}'
    if not entities_pass:
        all_passed = False
        post_passed = False
    
    # C. Pillar link
    pillar_pass, pillar_links, pillar_topic = check_pillar_link(post)
    pillar_status = '✅' if pillar_pass else '❌'
    pillar_detail = f'Links to: {pillar_links}' if pillar_links else f'Pillar: {pillar_topic} — no link found'
    if not pillar_pass:
        all_passed = False
        post_passed = False
    
    # D. AEO/GEO
    aeo_pass, q_count = check_aeo_geo(post)
    aeo_status = '✅' if aeo_pass else '❌'
    if not aeo_pass:
        all_passed = False
        post_passed = False
    
    # E. Internal links
    link_pass, link_count, link_urls = check_internal_links(post)
    link_status = '✅' if link_pass else '❌'
    if not link_pass:
        all_passed = False
        post_passed = False
    
    # F. Schema
    schema_pass, schema_issues = check_schema(post)
    schema_status = '✅' if schema_pass else '❌'
    schema_detail = 'All fields set' if schema_pass else 'Missing: ' + ', '.join(schema_issues)
    if not schema_pass:
        all_passed = False
        post_passed = False
    
    if post_passed:
        passed_count += 1
    
    report_parts.append(f"""## Post: {slug}
**Title:** {title}

| Check | Status | Details |
|-------|--------|---------|
| **TF-IDF:** `{keyword}` | {tfidf_status} | {tfidf_count} occurrences |
| **Entities** | {entities_status} | {entities_detail} |
| **Pillar Link** | {pillar_status} | {pillar_detail} |
| **AEO/GEO** | {aeo_status} | {q_count} question headings |
| **Internal Links** | {link_status} | {link_count} total |
| **Schema Ready** | {schema_status} | {schema_detail} |

""")
    
    # Build fix instructions
    fix_parts = []
    if not tfidf_pass:
        fix_parts.append(f"- 🔤 **TF-IDF:** Use `{keyword}` at least 5 times in content (currently {tfidf_count}). Add naturally in headings, first paragraph, and key sections as the primary keyword.")
    if not entities_pass:
        fix_parts.append(f"- 🏷️ **Entities:** Add missing entities: {', '.join(missing_entities)}. Include location context (Dhaka/Bangladesh), service type, and author/agency mentions for E-E-A-T.")
    if not pillar_pass:
        fix_parts.append(f"- 🔗 **Pillar Link:** Link to pillar page for '{pillar_topic}'. Suggested: `/blog/complete-seo-guide-bangladesh-businesses-2026` (main guide) or relevant pillar page based on tags: {', '.join(post.get('tags', []))}")
    if not aeo_pass:
        fix_parts.append(f"- ❓ **AEO/GEO:** Add {2 - q_count} more question-based H2/H3 headings (starting with How/What/Why/Can/Do/Is/Are) to capture AI Overview and voice search queries.")
    if not link_pass:
        missing_links = 3 - link_count
        fix_parts.append(f"- 🔗 **Internal Links:** Add at least {missing_links} more internal links to related blog posts, service pages (`/services/*`), or location pages (`/locations/*`).")
    if not schema_pass:
        fix_parts.append(f"- 📋 **Schema:** Set missing fields: {', '.join(schema_issues)}. All of `title`, `excerpt`, and `date` are required for ArticleSchema.")
    
    if fix_parts:
        report_parts.append("### Fix instructions:\n" + "\n".join(fix_parts) + "\n")

# Summary
now_utc = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
total = len(MODIFIED_SLUGS)
summary = f"""=====================================================
📊 CONTENT FRAMEWORK ENFORCEMENT REPORT
=====================================================
🕐 Generated: {now_utc}
📝 Modified posts (48h): {total}
✅ All checks passed: {passed_count}/{total}
❌ Posts needing fixes: {total - passed_count}
=====================================================

"""
report_parts.insert(0, summary)
print("".join(report_parts))
