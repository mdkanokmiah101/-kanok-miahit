#!/usr/bin/env python3
"""Final detailed analysis of all 9 blog posts"""
import re
import json

with open('/root/kanok-miahit/src/app/blog/data.js', 'r', encoding='utf-8') as f:
    content = f.read()

def find_closing_backtick(text, start):
    """Find closing backtick, handling escaped backticks"""
    i = start
    while i < len(text):
        if text[i] == '\\' and i + 1 < len(text):
            i += 2
        elif text[i] == '`':
            return i
        else:
            i += 1
    return None

def extract_post(content, slug):
    """Extract post by finding its slug and the post object boundaries"""
    idx = content.find(f'slug: "{slug}"')
    if idx == -1:
        return None, "Slug not found"
    
    # Find opening brace
    search_start = max(0, idx - 30)
    brace_pos = content.rfind('{', search_start, idx)
    if brace_pos == -1:
        return None, "Opening brace not found"
    
    # Find content field
    ckw = content.find('content: `', brace_pos)
    if ckw == -1:
        return None, "content: field not found"
    
    c_start = ckw + len('content: `')
    c_end = find_closing_backtick(content, c_start)
    if c_end is None:
        return None, "Closing backtick not found"
    
    # After content, find closing }
    after = content[c_end+1:]  # +1 to skip closing backtick
    close = re.search(r'\}\s*,?\s*(\n|$)', after)
    if not close:
        return None, "Closing brace not found"
    
    post_end = c_end + 1 + close.end()
    post_text = content[brace_pos:post_end]
    
    return post_text, None

def get_field(post_text, field):
    m = re.search(rf'{field}:\s*"((?:[^"\\]|\\.)*)"', post_text)
    return m.group(1) if m else None

def get_content(post_text):
    m = re.search(r'content:\s*`', post_text)
    if not m:
        return ""
    c_start = m.end()
    c_end = find_closing_backtick(post_text, c_start)
    if c_end:
        return post_text[c_start:c_end]
    return ""

def count_tfidf(content, keyword):
    if not keyword:
        return 0, "no keyword"
    return len(re.findall(re.escape(keyword), content, re.IGNORECASE)), keyword

def check_entities(content, is_bengali=False):
    entities = {}
    if is_bengali:
        entities['Dhaka/Bangladesh'] = bool(re.search(r'ঢাকা|বাংলাদেশ|বাংলা', content))
        entities['Service Type'] = bool(re.search(r'SEO|সিওও', content, re.IGNORECASE))
        entities['Industry'] = bool(re.search(r'ব্যবসা|দোকান|অনলাইন', content))
    else:
        entities['Dhaka/Bangladesh'] = bool(re.search(r'Dhaka|Bangladesh|Bangladeshi', content))
        entities['Service Type'] = bool(re.search(r'SEO|search engine optimization|digital marketing', content, re.IGNORECASE))
        entities['Industry'] = bool(re.search(r'business|e-commerce|restaurant|garment|healthcare|real estate|agency|automotive|watch|fashion', content, re.IGNORECASE))
    return entities

def check_pillar_link(content):
    """Look for links to homepage, services index, or blog index"""
    patterns = [
        (r'\(/\)', 'Homepage (/)'),
        (r'href="/"', 'Homepage href'),
        (r'href="/services"', 'Services page'),
        (r'href="/blog"', 'Blog index'),
    ]
    found = []
    for pat, desc in patterns:
        if re.search(pat, content):
            found.append(desc)
    return found

def count_question_headings(content, is_bengali=False):
    if is_bengali:
        patterns = [
            r'##+\s*(?:\d+[\.\)]\s*)?কীভাবে',
            r'##+\s*(?:\d+[\.\)]\s*)?কী\b',
            r'##+\s*(?:\d+[\.\)]\s*)?কেন\b',
            r'##+\s*(?:\d+[\.\)]\s*)?কখন\b',
            r'##+\s*(?:\d+[\.\)]\s*)?কোথায়',
            r'##+\s*(?:\d+[\.\)]\s*)?কোথায়',
        ]
    else:
        question_words = r'(How|What|Why|When|Where|Can|Do\b|Does\b|Is\b|Are\b|Should|Which)'
        patterns = [rf'##+\s*(?:\d+[\.\)]\s*)?{question_words}\s']
    
    matches = set()
    for p in patterns:
        for m in re.finditer(p, content, re.IGNORECASE):
            matches.add(m.group(0).strip())
    return len(matches), sorted(matches)

def count_internal_links(content):
    """Count internal links to /blog/, /services/, /locations/"""
    patterns = [
        r'href="/blog/([^"]+)"',
        r'href="/services/([^"]+)"',
        r'href="/locations/([^"]+)"',
        r'\]\(/blog/([^)]+)\)',
        r'\]\(/services/([^)]+)\)',
        r'\]\(/locations/([^)]+)\)',
    ]
    links = set()
    for p in patterns:
        for m in re.finditer(p, content):
            links.add(m.group(1))
    return len(links), sorted(links)

def check_schema(post_text):
    """Check if schema fields are set"""
    fields = {
        'title': bool(re.search(r'title:\s*"', post_text)),
        'excerpt': bool(re.search(r'excerpt:\s*"', post_text)),
        'date': bool(re.search(r'date:\s*"', post_text)),
        'author': bool(re.search(r'author:\s*"', post_text)),
        'imagePlaceholder': bool(re.search(r'imagePlaceholder:\s*"', post_text)),
        'metaTitle': bool(re.search(r'metaTitle:\s*"', post_text)),
        'metaDescription': bool(re.search(r'metaDescription:\s*"', post_text)),
    }
    return fields

# Define per-post keyword strategy for TF-IDF
post_keywords = {
    "how-to-choose-best-seo-expert-dhaka-15-things": "SEO Expert",
    "seo-expert-vs-seo-agency-dhaka-which-is-right": "SEO Expert",
    "top-10-seo-mistakes-dhaka-businesses-fix": "SEO Mistakes",
    "what-does-seo-expert-do-guide-business-owners": "SEO Expert",
    "seo-case-study-dhaka-businesses-increased-organic-traffic": "SEO Case Study",
    "hiring-seo-expert-dhaka-better-roi-than-paid-ads": "SEO ROI",
    "ai-seo-2026-dhaka-experts-optimize-google-ai-chatgpt": "AI SEO",
    "watchzonebd-seo-case-study": "SEO Case Study",
    "seo-tips-for-business-owners-bd": "SEO",
}

slugs = [
    "how-to-choose-best-seo-expert-dhaka-15-things",
    "seo-expert-vs-seo-agency-dhaka-which-is-right",
    "top-10-seo-mistakes-dhaka-businesses-fix",
    "what-does-seo-expert-do-guide-business-owners",
    "seo-case-study-dhaka-businesses-increased-organic-traffic",
    "hiring-seo-expert-dhaka-better-roi-than-paid-ads",
    "ai-seo-2026-dhaka-experts-optimize-google-ai-chatgpt",
    "watchzonebd-seo-case-study",
    "seo-tips-for-business-owners-bd",
]

results = {}

for slug in slugs:
    print(f"\n{'='*70}")
    print(f"## Post: {slug}")
    print(f"{'='*70}")
    
    post_text, err = extract_post(content, slug)
    if err:
        print(f"ERROR: {err}")
        continue
    
    title = get_field(post_text, 'title') or "UNKNOWN"
    excerpt = get_field(post_text, 'excerpt')
    date = get_field(post_text, 'date')
    author = get_field(post_text, 'author')
    metaTitle = get_field(post_text, 'metaTitle')
    metaDesc = get_field(post_text, 'metaDescription')
    
    tags_match = re.search(r'tags:\s*\[([^\]]+)\]', post_text)
    tags = re.findall(r'"((?:[^"\\]|\\.)*)"', tags_match.group(1)) if tags_match else []
    
    post_content = get_content(post_text)
    is_bengali = slug == "seo-tips-for-business-owners-bd"
    
    print(f"**Title:** {title}")
    print(f"**Date:** {date}")
    print(f"**Author:** {author}")
    print(f"**Tags:** {tags}")
    print(f"**Content length:** {len(post_content)} chars")
    
    # A. TF-IDF
    keyword = post_keywords[slug]
    kw_count, _ = count_tfidf(post_content, keyword)
    tfidf_pass = kw_count >= 5
    
    # B. Entities
    entities = check_entities(post_content, is_bengali)
    entities_pass = all(entities.values())
    
    # C. Pillar Link
    pillar_links = check_pillar_link(post_content)
    pillar_pass = len(pillar_links) > 0
    
    # D. AEO/GEO
    q_count, q_headings = count_question_headings(post_content, is_bengali)
    aeo_pass = q_count >= 2
    
    # E. Internal Links
    internal_count, internal_links = count_internal_links(post_content)
    internal_pass = internal_count >= 3
    
    # F. Schema
    schema = check_schema(post_text)
    schema_pass = all(schema.values())
    
    # Report table
    print(f"\n| Check | Status | Details |")
    print(f"|-------|--------|---------|")
    
    # TF-IDF
    status = "✅" if tfidf_pass else "❌"
    print(f"| TF-IDF: '{keyword}' | {status} | {kw_count} occurrences |")
    
    # Entities
    missing = [k for k, v in entities.items() if not v]
    status = "✅" if entities_pass else "❌"
    m_str = f"Missing: {', '.join(missing)}" if missing else "All present"
    print(f"| Entities | {status} | {m_str} |")
    
    # Pillar
    status = "✅" if pillar_pass else "❌"
    p_str = ', '.join(pillar_links) if pillar_links else "None found"
    print(f"| Pillar Link | {status} | {p_str} |")
    
    # AEO/GEO
    status = "✅" if aeo_pass else "❌"
    print(f"| AEO/GEO | {status} | {q_count} question headings |")
    
    # Internal Links
    status = "✅" if internal_pass else "❌"
    print(f"| Internal Links | {status} | {internal_count} total |")
    
    # Schema
    status = "✅" if schema_pass else "❌"
    missing_s = [k for k, v in schema.items() if not v]
    print(f"| Schema Ready | {status} | Missing: {', '.join(missing_s)} |")
    
    # Fix instructions
    print(f"\n### Fix instructions:")
    fixes = []
    if not tfidf_pass:
        fixes.append(f"- **TF-IDF**: Increase usage of '{keyword}' in content (currently {kw_count}, need ≥5)")
    if not entities_pass:
        fixes.append(f"- **Entities**: Add missing entities: {', '.join(missing)}")
    if not pillar_pass:
        fixes.append(f"- **Pillar Link**: Add a link to the homepage `/` or services page")
    if not aeo_pass:
        fixes.append(f"- **AEO/GEO**: Add more question-based headings (currently {q_count}, need ≥2)")
    if not internal_pass:
        fixes.append(f"- **Internal Links**: Add more internal links (currently {internal_count}, need ≥3)")
    if not schema_pass:
        fixes.append(f"- **Schema**: Add missing fields: {', '.join(missing_s)}")
    
    if fixes:
        for f in fixes:
            print(f)
    else:
        print("All checks pass! No fixes needed.")
    
    # Store results
    results[slug] = {
        'title': title,
        'keyword': keyword,
        'kw_count': kw_count,
        'tfidf_pass': tfidf_pass,
        'entities_pass': entities_pass,
        'entities_missing': missing,
        'pillar_pass': pillar_pass,
        'pillar_links': pillar_links,
        'aeo_pass': aeo_pass,
        'q_count': q_count,
        'q_headings': q_headings,
        'internal_pass': internal_pass,
        'internal_count': internal_count,
        'internal_links': internal_links,
        'schema_pass': schema_pass,
        'schema_missing': missing_s,
    }

# Summary
print(f"\n\n{'='*70}")
print("SUMMARY: ALL 9 POSTS")
print(f"{'='*70}")
print(f"\n| Post | TF-IDF | Entities | Pillar | AEO/GEO | Int.Links | Schema |")
print(f"|------|--------|----------|--------|---------|-----------|--------|")

for slug in slugs:
    if slug in results:
        r = results[slug]
        short_slug = slug[:45]
        print(f"| {short_slug} | {'✅' if r['tfidf_pass'] else '❌'} | {'✅' if r['entities_pass'] else '❌'} | {'✅' if r['pillar_pass'] else '❌'} | {'✅' if r['aeo_pass'] else '❌'} | {'✅' if r['internal_pass'] else '❌'} | {'✅' if r['schema_pass'] else '❌'} |")

print(f"\n{'='*70}")
print("OVERALL STATS")
print(f"{'='*70}")

total_checks = len(slugs) * 6
passed_checks = sum(
    1 for r in results.values() for c in ['tfidf_pass', 'entities_pass', 'pillar_pass', 'aeo_pass', 'internal_pass', 'schema_pass'] if r[c]
)
print(f"Passed: {passed_checks}/{total_checks} checks ({passed_checks/total_checks*100:.0f}%)")
print(f"Failed: {total_checks - passed_checks}/{total_checks} checks")

# Count passes per post
for slug in slugs:
    if slug in results:
        r = results[slug]
        p = sum([r['tfidf_pass'], r['entities_pass'], r['pillar_pass'], r['aeo_pass'], r['internal_pass'], r['schema_pass']])
        print(f"  {slug}: {p}/6 passed")
