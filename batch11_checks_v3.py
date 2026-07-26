#!/usr/bin/env python3
"""Run all 6 content framework checks on Batch 11 posts - v3 refined keyword extraction."""
import re
import json

with open('/root/kanok-miahit/src/app/blog/data.js', 'r', encoding='utf-8') as f:
    content = f.read()

def extract_post(content, slug):
    """Extract a full post object as a string."""
    idx = content.find(f'slug: "{slug}"')
    if idx == -1:
        return None
    
    # Walk backwards to find opening {
    start = idx
    while start > 0 and content[start] != '{':
        start -= 1
    before = content[:idx]
    last_brace = before.rfind('}')
    after_brace = before[last_brace+1:] if last_brace >= 0 else before
    brace_pos = after_brace.find('{')
    if brace_pos >= 0:
        start = last_brace + 1 + brace_pos if last_brace >= 0 else brace_pos
    
    depth = 0
    in_backtick = False
    in_string = False
    string_char = None
    
    for end in range(start, len(content)):
        ch = content[end]
        if in_backtick:
            if ch == '\\':
                end += 1
                continue
            if ch == '`':
                in_backtick = False
            continue
        if in_string:
            if ch == '\\':
                end += 1
                continue
            if ch == string_char:
                in_string = False
            continue
        if ch == '`':
            in_backtick = True
            continue
        if ch in ('"', "'"):
            in_string = True
            string_char = ch
            continue
        if ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0:
                return content[start:end+1]
    return None

def extract_field(post_str, field_name):
    if field_name == 'slug':
        m = re.search(r'slug:\s*"([^"]*)"', post_str)
        return m.group(1) if m else None
    if field_name == 'title':
        m = re.search(r'title:\s*"((?:[^"\\]|\\.)*)"', post_str)
        if m: return m.group(1)
        m = re.search(r'title:\s*\n\s+"((?:[^"\\]|\\.)*)"', post_str)
        return m.group(1) if m else None
    if field_name == 'date':
        m = re.search(r'date:\s*"([^"]*)"', post_str)
        return m.group(1) if m else None
    if field_name == 'excerpt':
        m = re.search(r'excerpt:\s*"((?:[^"\\]|\\.)*)"', post_str)
        if m: return m.group(1)
        m = re.search(r'excerpt:\s*`((?:[^`\\]|\\.)*)`', post_str)
        return m.group(1) if m else None
    if field_name == 'tags':
        m = re.search(r'tags:\s*\[([^\]]*)\]', post_str, re.DOTALL)
        if m: return re.findall(r'"([^"]*)"', m.group(1))
        return []
    if field_name == 'content':
        m = re.search(r'content:\s*`((?:[^`\\]|\\.)*)`', post_str, re.DOTALL)
        return m.group(1) if m else None
    return None

def extract_primary_keyword(slug):
    """Extract the primary target keyword from slug (predefined per post)."""
    keyword_map = {
        "how-to-choose-best-seo-expert-dhaka-15-things": "seo expert",
        "seo-expert-vs-seo-agency-dhaka-which-is-right": "seo agency",
        "top-10-seo-mistakes-dhaka-businesses-fix": "seo mistakes",
        "what-does-seo-expert-do-guide-business-owners": "seo expert",
        "seo-case-study-dhaka-businesses-increased-organic-traffic": "organic traffic",
        "hiring-seo-expert-dhaka-better-roi-than-paid-ads": "seo expert",
        "ai-seo-2026-dhaka-experts-optimize-google-ai-chatgpt": "ai seo",
        "watchzonebd-seo-case-study": "watchzonebd",
        "landlord-certificates-seo-case-study": "landlord certificates",
    }
    return keyword_map.get(slug, "")

def count_in_content(content_text, keyword):
    if not content_text or not keyword:
        return 0
    return len(re.findall(re.escape(keyword), content_text, re.IGNORECASE))

def check_tfidf(title, slug, content_text):
    """Check A: TF-IDF Coverage using primary keyword from title."""
    if not title or not content_text:
        return "N/A", "N/A"
    
    keyword = extract_primary_keyword(slug)
    if not keyword:
        # Fallback: use meaningful words from the slug
        slug_words = slug.replace('-', ' ').split()
        keyword = ' '.join(slug_words[:3])
    
    count = count_in_content(content_text, keyword)
    flag = "⚠️ FLAG" if count < 5 else "✅ OK"
    return keyword, f"{count} ({flag})"

def check_semantic(content_text, tags):
    """Check B: Semantic entity coverage."""
    issues = []
    if not content_text:
        return "N/A"
    
    has_dhaka = bool(re.search(r'\bdhaka\b', content_text, re.IGNORECASE))
    has_bangladesh = bool(re.search(r'\bbangladesh\b', content_text, re.IGNORECASE))
    has_uk = bool(re.search(r'\bUK\b', content_text) or re.search(r'\bUnited Kingdom\b', content_text))
    
    if not (has_dhaka or has_bangladesh or has_uk):
        issues.append("geographic entity (Dhaka/Bangladesh/UK)")
    
    service_terms = ['seo', 'search engine optimization', 'search engine optimisation',
                     'organic traffic', 'keyword research', 'link building',
                     'on-page', 'off-page', 'technical seo', 'seo audit',
                     'google business profile', 'google maps', 'local seo',
                     'content marketing', 'seo services', 'seo expert']
    has_service = any(re.search(r'\b' + re.escape(t) + r'\b', content_text, re.IGNORECASE) for t in service_terms)
    if not has_service:
        issues.append("service type (SEO)")
    
    industry_terms = ['ecommerce', 'e-commerce', 'real estate', 'healthcare', 'education',
                      'hospitality', 'restaurant', 'retail', 'technology', 'fashion',
                      'finance', 'legal', 'manufacturing', 'construction', 'logistics',
                      'travel', 'automotive', 'watch', 'electronics', 'agency',
                      'software', 'it services', 'certificates', 'food', 'medical']
    has_industry = any(re.search(r'\b' + re.escape(t) + r'\b', content_text, re.IGNORECASE) for t in industry_terms)
    if not has_industry:
        issues.append("industry sectors")
    
    if issues:
        return f"⚠️ Missing: {'; '.join(issues)}"
    else:
        return "✅ All present"

def check_pillar_cluster(content_text):
    """Check C: Link to pillar page or /services/ page."""
    if not content_text:
        return "N/A"
    
    md_pattern = r'\[([^\]]*)\]\((/services/[^)]*)\)'
    html_pattern = r'href="(/services/[^"]*)"'
    
    md_links = [link for _, link in re.findall(md_pattern, content_text)]
    html_links = re.findall(html_pattern, content_text)
    all_links = md_links + html_links
    
    if all_links:
        unique = list(set(all_links))
        return f"✅ Found {len(unique)} link(s) to: {', '.join(u[:40] for u in unique[:3])}"
    else:
        return "⚠️ No pillar/services link found"

def check_aeo_geo(content_text):
    """Check D: Count question-based headings."""
    if not content_text:
        return 0, "N/A", []
    
    # Find headings: ##, ###, ####, or **Heading** at start of line
    md_headings = re.findall(r'^#{2,5}\s+(.+)$', content_text, re.MULTILINE)
    bold_headings = re.findall(r'^\*\*(.+?)\*\*', content_text, re.MULTILINE)
    
    all_headings = md_headings + bold_headings
    
    en_q_words = r'^(How|What|Why|When|Where|Can|Do|Is|Are|Does|Did|Will|Should|Would|Could|Which)\b'
    bn_q_words = r'^(কী|কেন|কিভাবে|কীভাবে|কখন|কোথায়)'
    
    question_headings = []
    for h in all_headings:
        h_s = h.strip().rstrip(':').strip()
        if h_s.endswith('?'):
            question_headings.append(h_s)
        elif re.search(en_q_words, h_s, re.IGNORECASE):
            question_headings.append(h_s)
        elif re.search(bn_q_words, h_s):
            question_headings.append(h_s)
    
    count = len(question_headings)
    flag = "⚠️ FLAG" if count < 2 else "✅ OK"
    return count, f"{count} ({flag})", question_headings[:5]

def check_internal_linking(content_text):
    """Check E: Count internal links (/blog/, /services/, /locations/, /industries/)."""
    if not content_text:
        return 0, "N/A", []
    
    md_pattern = r'\[([^\]]*)\]\((/[^)]*)\)'
    html_pattern = r'href="(/[^"]*)"'
    
    md_links = [path for _, path in re.findall(md_pattern, content_text)]
    html_links = re.findall(html_pattern, content_text)
    all_paths = md_links + html_links
    
    internal_prefixes = ('/blog/', '/services/', '/locations/', '/industries/')
    internal_links = [p for p in all_paths if p.startswith(internal_prefixes)]
    
    count = len(internal_links)
    flag = "⚠️ FLAG" if count < 3 else "✅ OK"
    return count, f"{count} ({flag})", internal_links[:10]

def check_schema(post_str):
    """Check F: title, excerpt, date fields present."""
    missing = []
    if not re.search(r'title:\s*["`]', post_str):
        missing.append("title")
    if not re.search(r'excerpt:\s*["`]', post_str):
        missing.append("excerpt")
    if not re.search(r'date:\s*"', post_str):
        missing.append("date")
    if missing:
        return f"⚠️ Missing: {', '.join(missing)}"
    else:
        return "✅ All present"

slugs = [
    "how-to-choose-best-seo-expert-dhaka-15-things",
    "seo-expert-vs-seo-agency-dhaka-which-is-right",
    "top-10-seo-mistakes-dhaka-businesses-fix",
    "what-does-seo-expert-do-guide-business-owners",
    "seo-case-study-dhaka-businesses-increased-organic-traffic",
    "hiring-seo-expert-dhaka-better-roi-than-paid-ads",
    "ai-seo-2026-dhaka-experts-optimize-google-ai-chatgpt",
    "watchzonebd-seo-case-study",
    "landlord-certificates-seo-case-study",
]

results = []

for slug in slugs:
    post_str = extract_post(content, slug)
    if not post_str:
        print(f"\nERROR: Could not extract post for slug: {slug}\n")
        continue
    
    title = extract_field(post_str, 'title')
    excerpt = extract_field(post_str, 'excerpt')
    date = extract_field(post_str, 'date')
    tags = extract_field(post_str, 'tags') or []
    content_text = extract_field(post_str, 'content')
    
    print(f"\n{'='*80}")
    print(f"POST: {slug}")
    print(f"Title: {title}")
    print(f"{'='*80}")
    
    keyword, tfidf = check_tfidf(title, slug, content_text)
    print(f"A. TF-IDF: keyword='{keyword}' → {tfidf}")
    
    semantic = check_semantic(content_text, tags)
    print(f"B. Semantic: {semantic}")
    
    pillar = check_pillar_cluster(content_text)
    print(f"C. Pillar: {pillar}")
    
    aeo_count, aeo_res, aeo_ex = check_aeo_geo(content_text)
    print(f"D. AEO/GEO: {aeo_res} (e.g. {aeo_ex[:3]})")
    
    il_count, il_res, il_links = check_internal_linking(content_text)
    print(f"E. IntLinks: {il_res} (e.g. {il_links[:3] if il_links else 'none'})")
    
    schema = check_schema(post_str)
    print(f"F. Schema: {schema}")
    
    results.append((slug, title, keyword, tfidf, semantic, pillar, aeo_res, il_res, schema))

# ── SUMMARY TABLE ──
print(f"\n\n{'='*140}")
print("BATCH 11 — FINAL CHECK REPORT")
print(f"{'='*140}")
hdr = f"{'Slug':<52} {'A:TF-IDF':<20} {'B:Semantic':<28} {'C:Pillar':<30} {'D:AEO/GEO':<18} {'E:IntLink':<18} {'F:Schema':<18}"
print(hdr)
print('-' * 140)
for r in results:
    s = f"{r[0][:50]:<52} {r[3][:18]:<20} {r[4][:26]:<28} {r[5][:28]:<30} {r[6][:16]:<18} {r[7][:16]:<18} {r[8][:16]:<18}"
    print(s)
print('=' * 140)

# Flag counts
flags = {'A:TF-IDF': 0, 'B:Semantic': 0, 'C:Pillar': 0, 'D:AEO/GEO': 0, 'E:IntLink': 0, 'F:Schema': 0}
for r in results:
    if 'FLAG' in r[3]: flags['A:TF-IDF'] += 1
    if 'Missing' in r[4]: flags['B:Semantic'] += 1
    if 'No pillar' in r[5]: flags['C:Pillar'] += 1
    if 'FLAG' in r[6]: flags['D:AEO/GEO'] += 1
    if 'FLAG' in r[7]: flags['E:IntLink'] += 1
    if 'Missing' in r[8]: flags['F:Schema'] += 1

print(f"\nFLAG SUMMARY ({len(results)} posts):")
for k, v in flags.items():
    print(f"  {'⚠️' if v else '✅'} {k}: {v} flagged")
total = sum(flags.values())
print(f"  Total flags: {total}")
print(f"  Posts with 0 flags: {sum(1 for r in results if all(('FLAG' not in r[i] and 'Missing' not in r[i] and 'No pillar' not in r[i]) for i in range(3,9)))}")
print(f"  Posts with ≥1 flag: {sum(1 for r in results if any(('FLAG' in r[i] or 'Missing' in r[i] or 'No pillar' in r[i]) for i in range(3,9)))}")

# ── DETAILED TABLE ──
print(f"\n\n{'='*140}")
print("DETAILED PER-POST REPORT")
print(f"{'='*140}")
for slug, title, keyword, tfidf, semantic, pillar, aeo, intlink, schema in results:
    print(f"\n{'─'*90}")
    print(f"  {slug}")
    print(f"  Title: {title}")
    print(f"{'─'*90}")
    print(f"  A. TF-IDF Coverage    : {tfidf}  (keyword: '{keyword}')")
    print(f"  B. Semantic Entities  : {semantic}")
    print(f"  C. Pillar-Cluster     : {pillar}")
    print(f"  D. AEO/GEO Questions  : {aeo}")
    print(f"  E. Internal Links     : {intlink}")
    print(f"  F. Schema Fields      : {schema}")
print(f"{'='*140}")
