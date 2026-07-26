#!/usr/bin/env python3
"""Run all 6 content framework checks on Batch 11 posts."""
import re
import json
import sys

# Read the data.js file
with open('/root/kanok-miahit/src/app/blog/data.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the posts array - get everything from "const posts = [...]"
# Use a simpler approach: extract each post object between { slug: ... } and the next { slug: or ];
# We'll search for each slug and extract the surrounding post object

def extract_post(content, slug):
    """Extract a full post object from the JS file using the slug."""
    # Find the slug
    idx = content.find(f'slug: "{slug}"')
    if idx == -1:
        return None
    
    # Find the opening { before slug
    # Go backwards to find the opening brace
    start = idx
    while start > 0 and content[start] != '{':
        start -= 1
    # But we need the opening brace of this post object
    # Look for the pattern: },\n  { or \n  { before slug
    before_slug = content[:idx]
    last_close = before_slug.rfind('}')
    after_last_close = before_slug[last_close+1:] if last_close >= 0 else before_slug
    # Find the '{' that starts this post
    pos = last_close
    while pos < idx:
        if content[pos] == '{':
            start = pos
            break
        pos += 1
    if start >= idx:
        # fallback: search backward from slug
        start = idx
        while start > 0 and content[start] != '{':
            start -= 1
    
    # Find the end - look for "},\n  {" or "},\n];" or ",\n  {" after content backtick
    # Better: find the closing } that matches the opening {
    depth = 0
    in_template = False
    template_char = None
    in_string = False
    string_char = None
    end = start
    
    while end < len(content):
        ch = content[end]
        
        if in_template:
            if ch == '\\':
                end += 2
                continue
            if ch == template_char:
                in_template = False
            end += 1
            continue
        
        if in_string:
            if ch == '\\':
                end += 2
                continue
            if ch == string_char:
                in_string = False
            end += 1
            continue
        
        if ch in ('"', "'", '`'):
            in_string = True
            string_char = ch
            end += 1
            continue
        
        if ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0:
                end += 1
                # This is the end of the post object
                post_str = content[start:end]
                return post_str
        
        end += 1
    
    return None

def extract_field(post_str, field_name):
    """Extract a field value from a post JS object string."""
    # Pattern: fieldName: value,
    # Handle multi-line values
    patterns = {
        'slug': r'slug:\s*"([^"]*)"',
        'title': r'title:\s*"((?:[^"\\]|\\.)*)"',
        'date': r'date:\s*"([^"]*)"',
        'author': r'author:\s*"([^"]*)"',
        'authorLink': r'authorLink:\s*"([^"]*)"',
        'imagePlaceholder': r'imagePlaceholder:\s*"([^"]*)"',
        'excerpt': r'excerpt:\s*(?:"([^"]*)"|`([^`]*)`)',
    }
    
    if field_name in patterns:
        m = re.search(patterns[field_name], post_str)
        if m:
            return m.group(1) or m.group(2) if m.lastindex and m.lastindex > 1 else m.group(1)
    
    # For tags array
    if field_name == 'tags':
        m = re.search(r'tags:\s*\[([^\]]*)\]', post_str, re.DOTALL)
        if m:
            tags_str = m.group(1)
            tags = re.findall(r'"([^"]*)"', tags_str)
            return tags
    
    # For content (template literal)
    if field_name == 'content':
        m = re.search(r'content:\s*`((?:[^`\\]|\\.)*)`', post_str, re.DOTALL)
        if m:
            return m.group(1)
    
    return None

def count_in_content(content_text, keyword):
    """Count case-insensitive occurrences of keyword in content."""
    if not content_text or not keyword:
        return 0
    return len(re.findall(re.escape(keyword), content_text, re.IGNORECASE))

def check_tfidf(title, content_text):
    """Check A: Extract primary keyword from title, count in content."""
    if not title or not content_text:
        return "N/A", "N/A"
    
    # Extract primary keyword from title
    # Remove common stop words and take meaningful words
    # Simplified: take the first 3-4 key terms from title
    title_lower = title.lower()
    # Remove punctuation
    title_clean = re.sub(r'[^\w\s]', ' ', title_lower)
    words = title_clean.split()
    
    # Common stop words to skip for keyword extraction
    stop_words = {'the', 'a', 'an', 'in', 'of', 'to', 'for', 'and', 'or', 'is', 'are', 
                  'it', 'at', 'by', 'on', 'be', 'as', 'from', 'with', 'that', 'this',
                  'your', 'our', 'its', 'how', 'what', 'why', 'when', 'where', 'which',
                  'do', 'does', 'did', 'will', 'can', 'has', 'had', 'have', 'not', 'no',
                  'we', 'you', 'they', 'he', 'she', 'vs'}
    
    # Find meaningful keywords
    meaningful = [w for w in words if w not in stop_words and len(w) > 2]
    
    # Try primary N-grams (2-3 word phrases from title)
    # First try the full title as a keyword phrase
    # Let's use a more sophisticated approach:
    # Check various n-grams from the title
    
    best_count = 0
    best_keyword = ""
    
    # Try 3-word phrases
    for i in range(len(meaningful) - 2):
        phrase = ' '.join(meaningful[i:i+3])
        c = count_in_content(content_text, phrase)
        if c > best_count:
            best_count = c
            best_keyword = phrase
    
    # Try 2-word phrases
    for i in range(len(meaningful) - 1):
        phrase = ' '.join(meaningful[i:i+2])
        c = count_in_content(content_text, phrase)
        if c > best_count:
            best_count = c
            best_keyword = phrase
    
    # Try single most relevant word
    for w in meaningful:
        c = count_in_content(content_text, w)
        if c > best_count:
            best_count = c
            best_keyword = w
    
    # Also try the full meaningful phrase (first 4 meaningful words)
    if len(meaningful) >= 4:
        phrase = ' '.join(meaningful[:4])
        c = count_in_content(content_text, phrase)
        if c > best_count:
            best_count = c
            best_keyword = phrase
    
    flag = "⚠️ FLAG" if best_count < 5 else "✅ OK"
    return best_keyword, f"{best_count} ({flag})"

def check_semantic(content_text, title, tags):
    """Check B: Semantic entity coverage."""
    issues = []
    
    # Check Dhaka/Bangladesh
    has_dhaka = bool(re.search(r'dhaka', content_text or '', re.IGNORECASE))
    has_bangladesh = bool(re.search(r'bangladesh', content_text or '', re.IGNORECASE))
    if not has_dhaka and not has_bangladesh:
        issues.append("Dhaka/Bangladesh")
    
    # Check service type - look for common SEO service terms
    service_terms = ['seo', 'search engine optimization', 'local seo', 'technical seo', 
                     'on-page seo', 'off-page seo', 'content marketing', 'link building',
                     'keyword research', 'seo audit', 'seo services', 'seo expert']
    has_service = any(re.search(r'\b' + re.escape(t) + r'\b', content_text or '', re.IGNORECASE) for t in service_terms)
    if not has_service:
        issues.append("service type")
    
    # Check industry sectors
    industry_terms = ['ecommerce', 'e-commerce', 'real estate', 'healthcare', 'education',
                      'hospitality', 'restaurant', 'retail', 'technology', 'it',
                      'fashion', 'finance', 'banking', 'legal', 'manufacturing',
                      'construction', 'logistics', 'travel', 'automotive', 'watch',
                      'electronics', 'digital marketing', 'agency']
    has_industry = any(re.search(r'\b' + re.escape(t) + r'\b', content_text or '', re.IGNORECASE) for t in industry_terms)
    if not has_industry and tags:
        # Check if tags mention industry
        has_industry = any(t.lower() in industry_terms for t in tags)
    
    if not has_industry:
        issues.append("industry sectors")
    
    if issues:
        return f"⚠️ Missing: {', '.join(issues)}"
    else:
        return "✅ All present"

def check_pillar_cluster(content_text):
    """Check C: Link to pillar page or /services/ page."""
    if not content_text:
        return "N/A"
    
    # Look for links to /services/ or pillar pages
    pillar_pattern = r'href="(/services/[^"]*)"'
    services_links = re.findall(pillar_pattern, content_text)
    
    if services_links:
        return f"✅ Found links to: {', '.join(set(sl.split('/')[2] if '/' in sl[10:] else sl for sl in services_links[:3]))}"
    else:
        return "⚠️ No pillar/services link found"

def check_aeo_geo(content_text):
    """Check D: Count question-based headings (How/What/Why etc. or Bengali)."""
    if not content_text:
        return 0, "N/A"
    
    # Count headings (## or ### or **heading** or markdown headings)
    # Look for question patterns in headings
    
    question_words = r'(How|What|Why|When|Where|Can|Do|Is|Are|Does|Did|Will|Should|Would|Could|Which)'
    bengali_question_words = r'(কী|কেন|কিভাবে|কীভাবে|কখন|কোথায়)'
    
    # Find all headings - look for ## Heading or **Heading** patterns that contain question words
    heading_lines = re.findall(r'^#{2,5}\s+(.+)$', content_text, re.MULTILINE)
    bold_headings = re.findall(r'^\*\*(.+?)\*\*$', content_text, re.MULTILINE)
    alt_headings = re.findall(r'^\*\*(.+?)\*\*:', content_text, re.MULTILINE)
    
    all_headings = heading_lines + bold_headings + alt_headings
    
    question_headings = []
    for h in all_headings:
        if re.search(question_words, h, re.IGNORECASE) or re.search(bengali_question_words, h):
            question_headings.append(h.strip())
    
    count = len(question_headings)
    flag = "⚠️ FLAG" if count < 2 else "✅ OK"
    return count, f"{count} ({flag})", question_headings[:5]

def check_internal_linking(content_text):
    """Check E: Count internal links (/blog/, /services/, /locations/, /industries/)."""
    if not content_text:
        return 0, "N/A"
    
    internal_pattern = r'href="(/(?:blog|services|locations|industries)/[^"]*)"'
    links = re.findall(internal_pattern, content_text)
    
    count = len(links)
    flag = "⚠️ FLAG" if count < 3 else "✅ OK"
    return count, f"{count} ({flag})", links[:10]

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
        print(f"ERROR: Could not extract post for slug: {slug}")
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
    print(f"   Result: {tfidf_result}")
    
    # B. Semantic Entity Coverage
    semantic_result = check_semantic(content_text, title, tags)
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
        print(f"   Links: {il_links[:5]}")
    
    # F. Schema
    schema_result = check_schema(post_str)
    print(f"\nF. Schema Fields:")
    print(f"   Result: {schema_result}")
    
    results.append((slug, title, keyword, tfidf_result, semantic_result, pillar_result, aeo_result, il_result, schema_result))

# Summary Table
print(f"\n\n{'='*120}")
print("BATCH 11 - SUMMARY TABLE")
print(f"{'='*120}")
print(f"{'Slug':<50} {'A:TF-IDF':<18} {'B:Semantic':<25} {'C:Pillar':<25} {'D:AEO/GEO':<18} {'E:IntLink':<18} {'F:Schema':<18}")
print(f"{'-'*50} {'-'*18} {'-'*25} {'-'*25} {'-'*18} {'-'*18} {'-'*18}")
for slug, title, keyword, tfidf, semantic, pillar, aeo, intlink, schema in results:
    short_slug = slug[:48]
    print(f"{short_slug:<50} {tfidf:<18} {semantic[:23]:<25} {pillar[:23]:<25} {aeo:<18} {intlink:<18} {schema:<18}")
print(f"{'='*120}")

# Detailed per-post table
print(f"\n\n{'='*120}")
print("BATCH 11 - DETAILED PER-POST REPORT")
print(f"{'='*120}")
for slug, title, keyword, tfidf, semantic, pillar, aeo, intlink, schema in results:
    print(f"\n{'─'*80}")
    print(f"Post: {slug}")
    print(f"Title: {title}")
    print(f"{'─'*80}")
    print(f"  A. TF-IDF Coverage    : {tfidf} (keyword: '{keyword}')")
    print(f"  B. Semantic Entities  : {semantic}")
    print(f"  C. Pillar-Cluster     : {pillar}")
    print(f"  D. AEO/GEO Questions  : {aeo}")
    print(f"  E. Internal Links     : {intlink}")
    print(f"  F. Schema Fields      : {schema}")
print(f"{'='*120}")
