#!/usr/bin/env python3
"""
Batch 10 Content Framework Checks - FINAL
Refined keyword extraction with better handling of compound keywords.
"""
import re
import sys

FILEPATH = "/root/kanok-miahit/src/app/blog/data.js"

BATCH_10_SLUGS = [
    "local-seo-multiple-business-locations-bangladesh",
    "enterprise-seo-large-organizations-bangladesh",
    "seo-photographers-videographers-bangladesh",
    "seo-wedding-event-planners-bangladesh",
    "blogging-strategy-seo-frequency-topics-bangladesh",
    "backlink-outreach-templates-strategies-bangladesh",
    "seo-non-profit-organizations-bangladesh",
    "recovering-google-penalties-bangladesh-guide",
    "building-seo-roadmap-bangladesh-business",
    "voice-search-seo-bengali-bangladesh",
    "why-md-kanok-miah-is-the-best-seo-expert-in-dhaka-bangladesh",
    "locksmith-dundee-seo-case-study",
    "landlord-certificates-seo-case-study",
    "das-taxis-scotland-seo-case-study",
    "morethanpanel-seo-case-study",
    "smmgen-seo-case-study",
    "smmsun-seo-case-study",
    "mir-cement-seo-case-study",
    "dhaka-apparels-seo-case-study",
    "stealth-windshield-repairs-seo-case-study",
]

QUESTION_HEADING_PATTERN = re.compile(
    r'^(?:How|What|Why|When|Where|Can|Do|Is|Are|'
    r'কী|কেন|কীভাবে|কখন|কোথায়)'
    r'(?:\s|\?|:|：)',
    re.IGNORECASE
)

MD_LINK_PATTERN = re.compile(r'\[([^\]]*)\]\((/[^)]+)\)')
HTML_LINK_PATTERN = re.compile(r'href=(["\'])(/[^"\']+?)\1')


def extract_all_posts(filepath):
    """Parse data.js and extract post objects as dicts."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    slug_pattern = re.compile(r'\bslug:\s*"([^"]+)"')
    matches = list(slug_pattern.finditer(content))
    
    posts = []
    for i, m in enumerate(matches):
        slug = m.group(1)
        slug_pos = m.start()
        
        obj_start = slug_pos
        while obj_start > 0:
            obj_start -= 1
            if content[obj_start] == '{':
                break
            if slug_pos - obj_start > 200:
                obj_start = slug_pos
                break
        
        brace_count = 0
        obj_end = obj_start
        in_backtick = False
        in_double_quote = False
        in_single_quote = False
        escape_next = False
        
        while obj_end < len(content):
            ch = content[obj_end]
            
            if escape_next:
                escape_next = False
                obj_end += 1
                continue
            
            if ch == '\\':
                escape_next = True
                obj_end += 1
                continue
            
            if ch == '`' and not in_double_quote and not in_single_quote:
                in_backtick = not in_backtick
                obj_end += 1
                continue
            
            if ch == '"' and not in_backtick and not in_single_quote:
                in_double_quote = not in_double_quote
                obj_end += 1
                continue
            
            if ch == "'" and not in_backtick and not in_double_quote:
                in_single_quote = not in_single_quote
                obj_end += 1
                continue
            
            if not in_backtick and not in_double_quote and not in_single_quote:
                if ch == '{':
                    brace_count += 1
                elif ch == '}':
                    brace_count -= 1
                    if brace_count == 0 and obj_end > slug_pos:
                        break
            
            obj_end += 1
            if obj_end - obj_start > 200000:
                break
        
        post_text = content[obj_start:obj_end+1]
        
        post = {'slug': slug}
        
        t = re.search(r'title:\s*"([^"]*)"', post_text)
        if t:
            post['title'] = t.group(1)
        
        d = re.search(r'date:\s*"([^"]*)"', post_text)
        if d:
            post['date'] = d.group(1)
        
        e = re.search(r'excerpt:\s*"((?:[^"\\]|\\.)*)"', post_text)
        if e:
            post['excerpt'] = e.group(1)
        
        c_match = re.search(r'content:\s*`', post_text)
        if c_match:
            content_start = c_match.end()
            rest = post_text[content_start:]
            close_match = re.search(r'`\s*,?\s*\n?\s*\}', rest)
            if close_match:
                post['content'] = rest[:close_match.start()]
        
        posts.append(post)
    
    return posts


def get_primary_keyword(title):
    """
    Extract a meaningful primary keyword from the title for TF-IDF check.
    Returns a list of keyword candidates in priority order.
    """
    if not title:
        return [""]
    
    t = title.strip()
    candidates = []
    
    # CASE 1: Case study brand extraction
    # "X SEO Case Study: ..." → X
    cs1 = re.match(r'^(.+?)\s+SEO\s+Case\s+Study', t, re.IGNORECASE)
    if cs1:
        candidates.append(cs1.group(1).strip())
    
    # "X: From 0 to ..." or "X: 0 to ..." or "X: How ..."  (case study subtitles)
    cs2 = re.match(r'^([^:]+?)(?:\s+SEO)?:\s*(?:From|0\s+to|How\s+)', t, re.IGNORECASE)
    if cs2:
        brand = cs2.group(1).strip()
        if brand.lower() not in ('all',):
            candidates.append(brand)
    
    # "All X: 0 to ..." 
    cs3 = re.match(r'^All\s+(.+?):\s*0\s+to\s+', t, re.IGNORECASE)
    if cs3:
        candidates.append("All " + cs3.group(1).strip())
    
    # CASE 2: General post - clean the title
    # Remove site suffix, subtitle
    clean = re.sub(r'\s*[|–\-——].*$', '', t).strip()
    
    # Extract main topic - remove "in/for Bangladesh/Bengali/Dhaka" and marketing verbs
    main = re.sub(r'\s+(?:in|for)\s+(?:Bangladesh|Bengali|Dhaka).*$', '', clean, flags=re.IGNORECASE).strip()
    main = re.sub(r'^(?:Capture|Grow|Amplify|Scale|Get|Master|Attract|Dominate|Unlock|Build|Boost|Transform|Maximize|Learn|Discover|Find|Create|Drive|Achieve|Generate|Deliver)\s+(?:the\s+)?(?:Growing\s+)?(?:Your\s+)?', '', main, flags=re.IGNORECASE).strip()
    
    if main and len(main) > 5:
        candidates.append(main)
    
    # Also add the full clean title as fallback
    if clean != main:
        candidates.append(clean)
    
    # Add the whole title
    candidates.append(t)
    
    # Deduplicate while preserving order
    seen = set()
    unique = []
    for c in candidates:
        cl = c.lower()
        if cl not in seen:
            seen.add(cl)
            unique.append(c)
    
    return unique


def check_a_tfidf(title, content):
    """Check A: TF-IDF Coverage."""
    if not title or not content:
        return "NO TITLE/CONTENT", True
    
    content_lower = content.lower()
    candidates = get_primary_keyword(title)
    
    # Try each candidate, preferring longer/more specific matches
    best_kw = candidates[0] if candidates else title
    best_count = 0
    
    for kw in candidates:
        kw_lower = kw.lower()
        cnt = content_lower.count(kw_lower)
        # Score: count * 10 + specificity bonus (longer is better for same count)
        score = cnt * 10 + len(kw.split())
        if score > best_count * 10 + len(best_kw.split()):
            best_kw = kw
            best_count = cnt
    
    # If primary candidate fails, try multi-word breakdown
    if best_count < 5:
        words = best_kw.lower().split()
        # Remove stopwords
        stopwords = {'a', 'an', 'the', 'for', 'in', 'of', 'to', 'and', 'or', 'is', 'are',
                     'your', 'our', 'with', 'by', 'from', 'at', 'on', 'be', 'has', 'have',
                     'its', 'their', 'all', 'not', 'but', 'as', 'it', 'do', 'will', 'can',
                     'if', 'no', 'up', 'out', 'so', 'just', 'about', 'into', 'over', 'after'}
        sig_words = [w for w in words if w not in stopwords and len(w) > 2]
        
        # Try bigrams
        for i in range(len(sig_words) - 1):
            bigram = ' '.join(sig_words[i:i+2])
            cnt = content_lower.count(bigram)
            if cnt > best_count:
                best_kw = bigram
                best_count = cnt
        
        # Try individual significant words
        for w in sig_words:
            cnt = content_lower.count(w)
            if cnt > best_count:
                best_kw = w
                best_count = cnt
    
    flagged = best_count < 5
    return f"'{best_kw}': {best_count} occurrences", flagged


def check_b_semantic(content):
    if not content:
        return "NO CONTENT", True
    
    content_lower = content.lower()
    missing = []
    
    if 'dhaka' not in content_lower and 'bangladesh' not in content_lower:
        missing.append('Dhaka/Bangladesh')
    
    service_terms = ['seo', 'search engine optimization', 'optimization', 'ranking', 'organic']
    found_service = any(term in content_lower for term in service_terms)
    if not found_service:
        missing.append('Service type')
    
    industry_terms = [
        'business', 'industry', 'e-commerce', 'retail', 'healthcare', 
        'real estate', 'education', 'restaurant', 'service', 'digital',
        'local', 'enterprise', 'non-profit', 'photographer', 'videographer',
        'wedding', 'event', 'blog', 'backlink', 'outreach',
        'locksmith', 'landlord', 'taxis', 'panel', 'cement', 'apparel',
        'windshield', 'client', 'customer', 'market'
    ]
    found_industry = any(term in content_lower for term in industry_terms)
    if not found_industry:
        missing.append('Industry sector')
    
    if missing:
        return f"Missing: {', '.join(missing)}", True
    return "All entities present", False


def check_c_pillar_cluster(content):
    if not content:
        return "NO CONTENT", True
    
    md_links = MD_LINK_PATTERN.findall(content)
    html_links = HTML_LINK_PATTERN.findall(content)
    
    all_urls = [url for _, url in md_links] + [url for url, _ in html_links]
    
    services_links = [u for u in all_urls if u.startswith('/services/')]
    # Pillar = /about/, /contact/, /locations/, /industries/, /blog/ but note /blog/ links to OTHER blog posts, not pillar pages
    # Per spec: "Link to pillar page or /services/ page"
    pillar_links = [u for u in all_urls if u.startswith(('/services/', '/about', '/contact', '/locations/', '/industries/'))]
    
    if services_links:
        return f"/services/ links: {len(services_links)}", False
    elif pillar_links:
        return f"Pillar links: {len(pillar_links)}", False
    else:
        return "No pillar or services link", True


def check_d_aeo_geo(content):
    if not content:
        return "NO CONTENT", True
    
    heading_lines = re.findall(r'^#{2,3}\s+.*$', content, re.MULTILINE)
    question_headings = 0
    
    for heading in heading_lines:
        heading_text = heading.lstrip('#').strip()
        if not heading_text:
            continue
        if QUESTION_HEADING_PATTERN.match(heading_text):
            question_headings += 1
        elif heading_text.rstrip().endswith('?'):
            question_headings += 1
    
    flagged = question_headings < 2
    return f"{question_headings} question headings", flagged


def check_e_internal_linking(content):
    if not content:
        return "NO CONTENT", True
    
    md_links = MD_LINK_PATTERN.findall(content)
    html_links = HTML_LINK_PATTERN.findall(content)
    
    internal_paths = ['/blog/', '/services/', '/locations/', '/industries/']
    
    linked_urls = set()
    for _, url in md_links:
        for p in internal_paths:
            if url.startswith(p):
                linked_urls.add(url)
                break
    
    for url, _ in html_links:
        for p in internal_paths:
            if url.startswith(p):
                linked_urls.add(url)
                break
    
    count = len(linked_urls)
    flagged = count < 3
    return f"{count} internal links", flagged


def check_f_schema(post):
    missing = []
    for field in ['title', 'excerpt', 'date']:
        if field not in post or not post.get(field):
            missing.append(field)
    
    if missing:
        return f"Missing: {', '.join(missing)}", True
    return "All present", False


def main():
    print("=" * 150)
    print(f"{'Batch 10 Content Framework Checks':^150}")
    print(f"{'File: /root/kanok-miahit/src/app/blog/data.js':^150}")
    print(f"{'FINAL — All 6 checks per post':^150}")
    print("=" * 150)
    
    all_posts = extract_all_posts(FILEPATH)
    print(f"\nExtracted {len(all_posts)} total posts from data.js.")
    
    post_lookup = {p['slug']: p for p in all_posts}
    
    for slug in BATCH_10_SLUGS:
        if slug not in post_lookup:
            print(f"  WARNING: '{slug}' NOT FOUND in data.js!")
    
    results = []
    
    for slug in BATCH_10_SLUGS:
        post = post_lookup.get(slug)
        
        print(f"\n{'─'*150}")
        print(f"  SLUG: {slug}")
        
        if not post:
            print(f"{'─'*150}")
            print(f"  {'ERROR: Post not found':^146}")
            results.append([slug, 'NOT FOUND', True] * 6)
            continue
        
        title = post.get('title', '')
        content = post.get('content', '')
        
        print(f"  TITLE: {title}")
        print(f"  CONTENT LEN: {len(content) if content else 0} chars")
        print(f"{'─'*150}")
        
        a_result, a_flag = check_a_tfidf(title, content)
        a_status = "✅" if not a_flag else "❌ FLAG"
        print(f"  A. TF-IDF Coverage: {a_result}  {a_status}")
        
        b_result, b_flag = check_b_semantic(content)
        b_status = "✅" if not b_flag else "❌ FLAG"
        print(f"  B. Semantic Entity: {b_result}  {b_status}")
        
        c_result, c_flag = check_c_pillar_cluster(content)
        c_status = "✅" if not c_flag else "❌ FLAG"
        print(f"  C. Pillar-Cluster: {c_result}  {c_status}")
        
        d_result, d_flag = check_d_aeo_geo(content)
        d_status = "✅" if not d_flag else "❌ FLAG"
        print(f"  D. AEO/GEO (Q Headings): {d_result}  {d_status}")
        
        e_result, e_flag = check_e_internal_linking(content)
        e_status = "✅" if not e_flag else "❌ FLAG"
        print(f"  E. Internal Linking: {e_result}  {e_status}")
        
        f_result, f_flag = check_f_schema(post)
        f_status = "✅" if not f_flag else "❌ FLAG"
        print(f"  F. Schema (title/excerpt/date): {f_result}  {f_status}")
        
        results.append([slug, a_result, a_flag, b_result, b_flag, c_result, c_flag, d_result, d_flag, e_result, e_flag, f_result, f_flag])
    
    # ===== SUMMARY TABLE =====
    print(f"\n\n{'='*150}")
    print(f"{'SUMMARY TABLE':^150}")
    print(f"{'='*150}")
    
    headers = ['Slug', 'A: TF-IDF', 'F', 'B: Semantic', 'F', 'C: Pillar', 'F', 'D: AEO/GEO', 'F', 'E: Int Link', 'F', 'F: Schema', 'F']
    col_widths = [52, 14, 3, 16, 3, 14, 3, 14, 3, 12, 3, 12, 3]
    
    def fmt_row(items):
        parts = []
        for item, width in zip(items, col_widths):
            item_str = str(item)[:width]
            parts.append(f"{item_str:<{width}}")
        return "| " + " | ".join(parts) + " |"
    
    sep = "-" * 150
    print(fmt_row(headers))
    print(sep)
    
    passes = 0
    fails_list = []
    
    for row in results:
        slug = row[0]
        checks = []
        for i in range(6):
            result_text = row[1 + i*2]
            flag = row[2 + i*2]
            checks.append((result_text, flag))
        
        a_r, a_f = checks[0]
        b_r, b_f = checks[1]
        c_r, c_f = checks[2]
        d_r, d_f = checks[3]
        e_r, e_f = checks[4]
        f_r, f_f = checks[5]
        
        a_s = "❌" if a_f else "✅"
        b_s = "❌" if b_f else "✅"
        c_s = "❌" if c_f else "✅"
        d_s = "❌" if d_f else "✅"
        e_s = "❌" if e_f else "✅"
        f_s = "❌" if f_f else "✅"
        
        display_row = [slug, a_r, a_s, b_r, b_s, c_r, c_s, d_r, d_s, e_r, e_s, f_r, f_s]
        print(fmt_row(display_row))
        
        total_fails = sum([a_f, b_f, c_f, d_f, e_f, f_f])
        if total_fails == 0:
            passes += 1
        else:
            fails_list.append((slug, total_fails))
    
    print(sep)
    
    total_a = sum(1 for r in results if r[2])
    total_b = sum(1 for r in results if r[4])
    total_c = sum(1 for r in results if r[6])
    total_d = sum(1 for r in results if r[8])
    total_e = sum(1 for r in results if r[10])
    total_f = sum(1 for r in results if r[12])
    
    print(f"\n  Total posts in Batch 10: {len(results)}")
    print(f"  Posts with ALL 6 checks passed: {passes}")
    print(f"  Posts with at least one FLAG:  {len(fails_list)}")
    print(f"\n  Flag counts per check:")
    print(f"    A (TF-IDF Coverage < 5):        {total_a}/20")
    print(f"    B (Semantic Entity missing):     {total_b}/20")
    print(f"    C (Pillar/Cluster link missing): {total_c}/20")
    print(f"    D (AEO/GEO < 2 Q headings):      {total_d}/20")
    print(f"    E (Internal Links < 3):          {total_e}/20")
    print(f"    F (Schema fields missing):       {total_f}/20")
    print(f"  Total flags across all checks: {total_a + total_b + total_c + total_d + total_e + total_f}")
    
    if fails_list:
        print(f"\n  Posts needing attention (sorted by fail count):")
        for slug, cnt in sorted(fails_list, key=lambda x: -x[1]):
            print(f"    {cnt} flag(s): {slug}")
    
    print(f"\n{'='*150}")
    print(f"{'END OF BATCH 10 REPORT':^150}")
    print(f"{'='*150}")

if __name__ == '__main__':
    main()
