#!/usr/bin/env python3
"""Framework enforcement check - refined version."""
import re

with open('/root/kanok-miahit/src/app/blog/data.js', 'r') as f:
    js_text = f.read()

def extract_full_post(slug):
    """Extract a full post object by finding slug and parsing the object."""
    idx = js_text.find(f'slug: "{slug}"')
    if idx < 0:
        return None
    
    # Walk backwards to find opening brace
    brace_depth = 0
    obj_start = None
    for i in range(idx - 1, max(idx - 3000, 0), -1):
        if js_text[i] == '}':
            brace_depth += 1
        elif js_text[i] == '{':
            if brace_depth == 0:
                obj_start = i
                break
            brace_depth -= 1
    
    if obj_start is None:
        return None
    
    # Walk forward to find matching closing brace
    brace_depth = 0
    in_content = False
    content_end = None
    for i in range(obj_start, len(js_text)):
        c = js_text[i]
        if c == '`' and not in_content:
            # Check if this starts a template literal
            if i > 0 and (js_text[i-1] == '\n' or js_text[i-1] == ' '):
                in_content = True
        elif c == '`' and in_content:
            in_content = False
        elif not in_content:
            if c == '{':
                brace_depth += 1
            elif c == '}':
                brace_depth -= 1
                if brace_depth == 0:
                    content_end = i + 1
                    break
    
    if content_end:
        return js_text[obj_start:content_end]
    return None

def extract_field(post, field):
    """Extract a field value from post string."""
    # Try single-line: field: "value"
    m = re.search(rf'{re.escape(field)}:\s*"([^"]*)"', post)
    if m:
        return m.group(1)
    # Try multi-line: field:\n      "value"
    m = re.search(rf'{re.escape(field)}:\s*\n\s*"([^"]*)"', post)
    if m:
        return m.group(1)
    # Try date field: date: "value"
    m = re.search(rf'{re.escape(field)}:\s*"([^"]*)"', post)
    if m:
        return m.group(1)
    return None

def extract_tags(post):
    """Extract tags from post string."""
    m = re.search(r'tags:\s*\[([^\]]+)\]', post, re.DOTALL)
    if m:
        tag_str = m.group(1)
        return re.findall(r'"([^"]+)"', tag_str)
    return []

def extract_content(post):
    """Extract content from template literal."""
    m = re.search(r'content:\s*`\n(.*?)`\s*,', post, re.DOTALL)
    if m:
        return m.group(1)
    # Try without newline after backtick
    m = re.search(r'content:\s*`(.*?)`\s*,', post, re.DOTALL)
    if m:
        return m.group(1)
    return ""

# Posts to check
posts = [
    {
        'slug': 'how-to-choose-best-seo-expert-dhaka-15-things',
        'expected_keyword': 'seo expert in dhaka',
    },
    {
        'slug': 'mobile-seo-optimization-bangladesh-mobile-first-era',
        'expected_keyword': 'mobile SEO',
    },
]

for pdata in posts:
    slug = pdata['slug']
    expected_kw = pdata['expected_keyword']
    
    print(f"\n{'='*70}")
    print(f"## Post: {slug}")
    print(f"{'='*70}")
    
    post = extract_full_post(slug)
    if not post:
        print("  ❌ Could not extract post")
        continue
    
    title = extract_field(post, 'title') or "Unknown"
    excerpt = extract_field(post, 'excerpt')
    date = extract_field(post, 'date')
    author = extract_field(post, 'author')
    tags = extract_tags(post)
    content = extract_content(post)
    
    print(f"\n  Title: {title[:80]}...")
    print(f"  Tags: {tags}")
    print(f"  Content length: {len(content)} chars")
    
    # ===== A. TF-IDF Coverage =====
    # Use expected keyword
    kw_count = len(re.findall(re.escape(expected_kw), content, re.IGNORECASE))
    # Also try shorter variant
    words = expected_kw.split()
    if len(words) > 3:
        shorter_kw = ' '.join(words[-3:])  # Last 3 words
        kw_count_v2 = len(re.findall(re.escape(shorter_kw), content, re.IGNORECASE))
        kw_count = max(kw_count, kw_count_v2)
    if len(words) > 3:
        shorter_kw2 = ' '.join(words[-2:])  # Last 2 words
        kw_count_v3 = len(re.findall(re.escape(shorter_kw2), content, re.IGNORECASE))
        kw_count = max(kw_count, kw_count_v3)
    
    tfidf_ok = kw_count >= 5
    print(f"\n  ### A. TF-IDF Coverage")
    print(f"  Keyword: '{expected_kw}' → {kw_count} occurrences {'✅' if tfidf_ok else '❌'}")
    
    # ===== B. Semantic Entity Coverage =====
    content_lower = content.lower()
    
    required_entities = {
        'Location: Dhaka': 'dhaka',
        'Location: Bangladesh': 'bangladesh',
    }
    
    if 'seo' in slug.lower():
        required_entities['Service: SEO'] = 'seo'
    if 'expert' in slug.lower():
        required_entities['Service: SEO Expert'] = 'seo expert'
    if 'mobile' in slug.lower():
        required_entities['Topic: Mobile'] = 'mobile'
    
    missing_entities = []
    present_entities = []
    for label, term in required_entities.items():
        if term in content_lower:
            present_entities.append(label)
        else:
            missing_entities.append(label)
    
    # Check neighborhoods
    neighborhoods = ['Gulshan', 'Banani', 'Uttara', 'Dhanmondi', 'Mirpur', 'Motijheel', 'Badda', 'Bashundhara']
    found_nh = [n for n in neighborhoods if n.lower() in content_lower]
    
    entity_ok = len(missing_entities) == 0
    print(f"\n  ### B. Semantic Entity Coverage")
    print(f"  Entities: {'✅' if entity_ok else '❌'} | Missing: {missing_entities or 'None'}")
    if found_nh:
        print(f"  Dhaka neighborhoods: {found_nh}")
    
    # ===== C. Pillar-Cluster Alignment =====
    pillar_links_found = []
    pillar_patterns = ['/about', '/services', '/case-studies']
    # Check tags for pillar context
    tag_lower = [t.lower() for t in tags]
    
    for pp in pillar_patterns:
        if pp in content:
            pillar_links_found.append(pp)
    
    # Also check for other internal service links
    service_links = re.findall(r'/services/[^\s"\'\)]+', content)
    pillar_links_found.extend(service_links)
    
    pillar_links_found = list(set(pillar_links_found))
    pillar_ok = len(pillar_links_found) > 0
    print(f"\n  ### C. Pillar-Cluster Alignment")
    print(f"  Pillar Link: {'✅' if pillar_ok else '❌'} | Links to: {pillar_links_found or 'NONE'}")
    
    # ===== D. AEO/GEO Optimization =====
    question_heading_pattern = r'^##{1,4}\s+(How\s+|What\s+|Why\s+|When\s+|Where\s+|Can\s+|Do\s+|Is\s+|Are\s+|Does\s+|Which\s+)'
    q_headings = re.findall(question_heading_pattern, content, re.MULTILINE | re.IGNORECASE)
    q_count = len(q_headings)
    
    # Also count FAQ entries (bold text ending with ?)
    faq_questions = re.findall(r'\*\*([^*]+?\?)\*\*', content)
    total_q = q_count + len(faq_questions)
    
    aeo_ok = total_q >= 2
    print(f"\n  ### D. AEO/GEO Optimization")
    print(f"  AEO/GEO: {'✅' if aeo_ok else '❌'} | {q_count} question headings + {len(faq_questions)} FAQ = {total_q} total")
    
    # ===== E. Internal Linking =====
    # Count all relative-path links (markdown format and bare)
    md_links = re.findall(r'\]\((/[^\)]+)\)', content)
    bare_links = re.findall(r'(?<![\"\'])(/blog/|/services/|/locations/|/industries/|/about\b|/contact\b|/case-studies\b)', content)
    
    all_internal = list(set(md_links + list(bare_links)))
    # Filter for truly internal (not external with //)
    all_internal = [l for l in all_internal if not l.startswith('//')]
    
    internal_ok = len(all_internal) >= 3
    print(f"\n  ### E. Internal Linking")
    print(f"  Internal Links: {'✅' if internal_ok else '❌'} | {len(all_internal)} unique links")
    print(f"  Sample links: {all_internal[:8]}")
    
    # ===== F. Schema =====
    required_schema = {
        'title': bool(re.search(r'title:\s', post)),
        'date': bool(re.search(r'date:\s', post)),
        'excerpt': bool(re.search(r'excerpt:\s', post)),
        'author': bool(re.search(r'author:\s', post)),
        'slug': bool(re.search(r'slug:\s', post)),
    }
    optional_schema = {
        'metaTitle': bool(re.search(r'metaTitle:\s', post)),
        'metaDescription': bool(re.search(r'metaDescription:\s', post)),
        'dateModified': bool(re.search(r'dateModified:\s', post)),
    }
    
    req_missing = [k for k, v in required_schema.items() if not v]
    opt_missing = [k for k, v in optional_schema.items() if not v]
    schema_ok = len(req_missing) == 0
    print(f"\n  ### F. Schema Ready")
    print(f"  Schema: {'✅' if schema_ok else '❌'} | Required missing: {req_missing or 'None'}")
    if opt_missing:
        print(f"  ⚠️  Optional missing: {opt_missing} (recommended for ArticleSchema)")
    
    # ===== SUMMARY =====
    all_pass = tfidf_ok and entity_ok and pillar_ok and aeo_ok and internal_ok and schema_ok
    print(f"\n  {'='*40}")
    print(f"  OVERALL: {'✅ ALL CHECKS PASSED' if all_pass else '❌ CHECKS FAILED'}")
    
    if not all_pass:
        print(f"\n  ### Fix Instructions:")
        if not tfidf_ok:
            print(f"  🔧 TF-IDF: Use '{expected_kw}' at least 5 times in content (currently {kw_count}). Add more natural mentions.")
        if not entity_ok:
            print(f"  🔧 Entities: Add missing entities: {missing_entities}")
        if not pillar_ok:
            print(f"  🔧 Pillar: Add a link to pillar page (/about, /services, etc.)")
        if not aeo_ok:
            print(f"  🔧 AEO/GEO: Add at least 2 question-based headings (How, What, Why, etc.)")
        if not internal_ok:
            print(f"  🔧 Internal Links: Add at least 3 internal links to other posts/services")
        if not schema_ok:
            print(f"  🔧 Schema: Add required fields: {req_missing}")
    print()
