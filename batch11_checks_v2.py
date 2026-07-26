#!/usr/bin/env python3
"""Run all 6 content framework checks on Batch 11 posts - refined."""
import re
import json
import sys

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
    # Ensure we're at a real opening brace, not one inside a string
    # Let's find the last } before slug and find { after it
    before = content[:idx]
    last_brace = before.rfind('}')
    after_brace = before[last_brace+1:] if last_brace >= 0 else before
    # Find the first { after last }
    brace_pos = after_brace.find('{')
    if brace_pos >= 0:
        start = last_brace + 1 + brace_pos if last_brace >= 0 else brace_pos
    
    # Walk forward counting braces
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
    """Extract a field value."""
    if field_name == 'slug':
        m = re.search(r'slug:\s*"([^"]*)"', post_str)
        return m.group(1) if m else None
    
    if field_name == 'title':
        m = re.search(r'title:\s*"((?:[^"\\]|\\.)*)"', post_str)
        if m: return m.group(1)
        # Multi-line title
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
        if m:
            return re.findall(r'"([^"]*)"', m.group(1))
        return []
    
    if field_name == 'content':
        m = re.search(r'content:\s*`((?:[^`\\]|\\.)*)`', post_str, re.DOTALL)
        return m.group(1) if m else None
    
    return None

def get_primary_keyword(title):
    """Extract the primary keyword/phrase from a title."""
    if not title:
        return ""
    
    # Remove the trailing parenthetical and common suffixes
    title_clean = re.sub(r'\s*\([^)]*\)', '', title)
    title_clean = re.sub(r'\s*\|.*$', '', title_clean)
    title_clean = re.sub(r'\s*—.*$', '', title_clean)
    
    # Remove punctuation
    title_clean = re.sub(r'[^\w\s]', ' ', title_clean)
    words = title_clean.split()
    
    stop_words = {'the', 'a', 'an', 'in', 'of', 'to', 'for', 'and', 'or', 'is', 'are', 
                  'it', 'at', 'by', 'on', 'be', 'as', 'from', 'with', 'that', 'this',
                  'your', 'our', 'its', 'how', 'what', 'why', 'when', 'where', 'which',
                  'do', 'does', 'did', 'will', 'can', 'has', 'had', 'have', 'not', 'no',
                  'we', 'you', 'they', 'he', 'she', 'vs', 'amp', 'more', 'all'}
    
    meaningful = [w for w in words if w.lower() not in stop_words and len(w) > 2]
    
    # For case studies, use the brand/business name
    if 'case study' in title.lower():
        # Extract what's before "case study"
        cs_match = re.match(r'^(.+?)\s+SEO\s+Case\s+Study', title, re.IGNORECASE)
        if cs_match:
            brand = cs_match.group(1).strip()
            # Use 2-3 word brand name
            brand_words = [w for w in brand.split() if w.lower() not in stop_words and len(w) > 2]
            if len(brand_words) >= 2:
                return ' '.join(brand_words[:2])
            return brand_words[0] if brand_words else meaningful[0] if meaningful else words[0]
    
    # For comparison posts ("X vs Y"), use the main topic
    vs_match = re.search(r'(.+?)\s+vs\s+', title, re.IGNORECASE)
    if vs_match:
        topic = vs_match.group(1).strip()
        return topic
    
    # For listicle "Top 10 X" or "15 X"
    list_match = re.search(r'(?:Top\s+\d+\s+|^\d+\s+)(.+?)(?:\s+in|\s+for|\s+:|\s*$)', title, re.IGNORECASE)
    if list_match:
        return list_match.group(1).strip()
    
    # For "How/What/Why/When ..." titles, extract the subject
    q_match = re.search(r'(?:How|What|Why|When|Where|Can|Do|Is|Are)\s+(?:to\s+)?(.+?)(?:\s+in\s+\w+|\s*$)', title, re.IGNORECASE)
    if q_match:
        return q_match.group(1).strip()
    
    # Default: use first 2-3 meaningful words
    if len(meaningful) >= 3:
        return ' '.join(meaningful[:3])
    elif meaningful:
        return meaningful[0]
    return words[0] if words else ""

def count_in_content(content_text, keyword):
    if not content_text or not keyword:
        return 0
    return len(re.findall(re.escape(keyword), content_text, re.IGNORECASE))

def check_tfidf(title, content_text):
    """Check A: TF-IDF Coverage."""
    if not title or not content_text:
        return "N/A", "N/A"
    
    keyword = get_primary_keyword(title)
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
    
    # Check for both "Dhaka" and "Bangladesh" or at least one of "Bangladesh" context
    # The landlord certificates post is about UK, so check for UK too
    has_uk = bool(re.search(r'\bUK\b', content_text) or re.search(r'\bUnited Kingdom\b', content_text))
    has_bd_entity = has_dhaka or has_bangladesh or has_uk
    
    if not has_bd_entity:
        issues.append("geographic entity (Dhaka/Bangladesh/UK)")
    
    service_terms = ['seo', 'search engine optimization', 'search engine optimisation',
                     'local seo', 'organic traffic', 'keyword research', 'link building',
                     'on-page', 'off-page', 'technical seo', 'seo audit', 'content strategy',
                     'google business profile', 'google maps']
    has_service = any(re.search(r'\b' + re.escape(t) + r'\b', content_text, re.IGNORECASE) for t in service_terms)
    if not has_service:
        issues.append("service type (SEO)")
    
    industry_terms = ['ecommerce', 'e-commerce', 'real estate', 'healthcare', 'education',
                      'hospitality', 'restaurant', 'retail', 'technology', 'fashion',
                      'finance', 'legal', 'manufacturing', 'construction', 'logistics',
                      'travel', 'automotive', 'watch', 'electronics', 'agency',
                      'software', 'it services', 'certificates']
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
    
    # Check markdown links and HTML links to /services/
    md_pattern = r'\[([^\]]*)\]\((/services/[^)]*)\)'
    html_pattern = r'href="(/services/[^"]*)"'
    
    md_links = re.findall(md_pattern, content_text)
    html_links = re.findall(html_pattern, content_text)
    
    all_links = [link for _, link in md_links] + html_links
    
    if all_links:
        # Get unique paths
        unique = list(set(all_links))
        return f"✅ Found {len(unique)} link(s) to: {', '.join(u[:40] for u in unique[:3])}"
    else:
        return "⚠️ No pillar/services link found"

def check_aeo_geo(content_text):
    """Check D: Count question-based headings."""
    if not content_text:
        return 0, "N/A", []
    
    # Find markdown headings (##, ###, ####, #####)
    md_headings = re.findall(r'^#{2,5}\s+(.+)$', content_text, re.MULTILINE)
    # Find bold headings: **Text** or **Text**: or **Text**\n
    bold_headings = re.findall(r'^\*\*(.+?)\*\*\s*:?\s*$', content_text, re.MULTILINE)
    
    all_headings = md_headings + bold_headings
    
    # Question patterns
    en_q_words = r'^(How|What|Why|When|Where|Can|Do|Is|Are|Does|Did|Will|Should|Would|Could|Which)\b'
    bn_q_words = r'^(কী|কেন|কিভাবে|কীভাবে|কখন|কোথায়)'
    
    question_headings = []
    for h in all_headings:
        h_stripped = h.strip()
        # Check if it ends with ? (question mark)
        if h_stripped.endswith('?'):
            question_headings.append(h_stripped)
        # Check if it starts with a question word
        elif re.search(en_q_words, h_stripped, re.IGNORECASE):
            question_headings.append(h_stripped)
        elif re.search(bn_q_words, h_stripped):
            question_headings.append(h_stripped)
    
    # Also check for bolded question phrases that might be in **Q:** format
    q_format = re.findall(r'\*\*(?:Question|Q|প্রশ্ন)[:\s]*(.+?)\*\*', content_text)
    for q in q_format:
        q_s = q.strip()
        if q_s not in question_headings:
            question_headings.append(q_s)
    
    count = len(question_headings)
    flag = "⚠️ FLAG" if count < 2 else "✅ OK"
    return count, f"{count} ({flag})", question_headings[:5]

def check_internal_linking(content_text):
    """Check E: Count internal links (/blog/, /services/, /locations/, /industries/)."""
    if not content_text:
        return 0, "N/A", []
    
    # Match both markdown and HTML link formats
    md_pattern = r'\[([^\]]*)\]\((/[^)]*)\)'
    html_pattern = r'href="(/[^"]*)"'
    
    md_links = re.findall(md_pattern, content_text)
    html_links = re.findall(html_pattern, content_text)
    
    all_paths = [path for _, path in md_links] + html_links
    
    # Filter for internal paths
    internal_prefixes = ('/blog/', '/services/', '/locations/', '/industries/')
    internal_links = [p for p in all_paths if p.startswith(internal_prefixes)]
    
    count = len(internal_links)
    flag = "⚠️ FLAG" if count < 3 else "✅ OK"
    return count, f"{count} ({flag})", internal_links[:10]

def check_schema(post_str):
    """Check F: title, excerpt, date fields present."""
    missing = []
    
    has_title = bool(re.search(r'title:\s*["`]', post_str))
    has_excerpt = bool(re.search(r'excerpt:\s*["`]', post_str))
    has_date = bool(re.search(r'date:\s*"', post_str))
    
    if not has_title:
        missing.append("title")
    if not has_excerpt:
        missing.append("excerpt")
    if not has_date:
        missing.append("date")
    
    if missing:
        return f"⚠️ Missing: {', '.join(missing)}"
    else:
        return "✅ All present"

# Batch 11 slugs
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
    
    # A. TF-IDF Coverage
    keyword, tfidf_result = check_tfidf(title, content_text)
    print(f"\nA. TF-IDF Coverage:")
    print(f"   Primary keyword: '{keyword}'")
    print(f"   Occurrences in content: {tfidf_result}")
    
    # B. Semantic Entity Coverage
    semantic_result = check_semantic(content_text, tags)
    print(f"\nB. Semantic Entity Coverage:")
    print(f"   Result: {semantic_result}")
    
    # C. Pillar-Cluster Alignment
    pillar_result = check_pillar_cluster(content_text)
    print(f"\nC. Pillar-Cluster Alignment:")
    print(f"   Result: {pillar_result}")
    
    # D. AEO/GEO
    aeo_count, aeo_result, aeo_headings = check_aeo_geo(content_text)
    print(f"\nD. AEO/GEO Question Headings:")
    print(f"   Count: {aeo_result}")
    if aeo_headings:
        print(f"   Examples: {aeo_headings[:3]}")
    
    # E. Internal Linking
    il_count, il_result, il_links = check_internal_linking(content_text)
    print(f"\nE. Internal Linking:")
    print(f"   Count: {il_result}")
    if il_links:
        print(f"   Links found: {il_links[:5]}")
    else:
        print(f"   (none detected)")
    
    # F. Schema
    schema_result = check_schema(post_str)
    print(f"\nF. Schema Fields:")
    print(f"   Result: {schema_result}")
    
    results.append((slug, title, keyword, tfidf_result, semantic_result, pillar_result, aeo_result, il_result, schema_result))

# Summary Table
print(f"\n\n{'='*140}")
print("BATCH 11 — CONTENT FRAMEWORK CHECK REPORT")
print(f"{'='*140}")
print(f"{'Slug':<52} {'A:TF-IDF':<20} {'B:Semantic':<28} {'C:Pillar':<30} {'D:AEO/GEO':<18} {'E:IntLink':<18} {'F:Schema':<18}")
print(f"{'-'*52} {'-'*20} {'-'*28} {'-'*30} {'-'*18} {'-'*18} {'-'*18}")
for slug, title, keyword, tfidf, semantic, pillar, aeo, intlink, schema in results:
    short_slug = slug[:50]
    # Clean up display
    tdisp = tfidf[:18]
    sdisp = semantic[:26]
    pdisp = pillar[:28]
    adisp = aeo[:16]
    iddisp = intlink[:16]
    sdisp2 = schema[:16]
    print(f"{short_slug:<52} {tdisp:<20} {sdisp:<28} {pdisp:<30} {adisp:<18} {iddisp:<18} {sdisp2:<18}")
print(f"{'='*140}")

# Flag count summary
flags = {'A:TF-IDF': 0, 'B:Semantic': 0, 'C:Pillar': 0, 'D:AEO/GEO': 0, 'E:IntLink': 0, 'F:Schema': 0}
for _, _, _, tfidf, semantic, pillar, aeo, intlink, schema in results:
    if 'FLAG' in tfidf: flags['A:TF-IDF'] += 1
    if 'Missing' in semantic: flags['B:Semantic'] += 1
    if 'No pillar' in pillar: flags['C:Pillar'] += 1
    if 'FLAG' in aeo: flags['D:AEO/GEO'] += 1
    if 'FLAG' in intlink: flags['E:IntLink'] += 1
    if 'Missing' in schema: flags['F:Schema'] += 1

print(f"\n\nFLAG SUMMARY (out of {len(results)} posts):")
for check, count in flags.items():
    status = "⚠️" if count > 0 else "✅"
    print(f"  {status} {check}: {count} post(s) flagged")

total_flags = sum(flags.values())
print(f"\nTotal flags raised: {total_flags}")
print(f"Posts without any flags: {sum(1 for r in results if all('FLAG' not in r[i] and 'Missing' not in r[i] and 'No pillar' not in r[i] for i in range(3,9)))}")
print(f"Posts with at least one flag: {sum(1 for r in results if any('FLAG' in r[i] or 'Missing' in r[i] or 'No pillar' in r[i] for i in range(3,9)))}")

# Detailed per-post table
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
