#!/usr/bin/env python3
"""Run content framework checks on 10 blog posts from data.js (v2 - fixed)."""
import re
import json
import sys

DATA_FILE = "src/app/blog/data.js"

with open(DATA_FILE, "r", encoding="utf-8") as f:
    data = f.read()

SLUGS = [
    "content-marketing-seo-friendly-content-writing",
    "keyword-research-bangladesh-market",
    "link-building-bangladesh-strategies",
    "ecommerce-seo-daraz-shopify-guide",
    "technical-seo-core-web-vitals-optimization",
    "seo-trends-2026-ai-geo-future",
    "local-seo-dhaka-google-maps-ranking",
    "seo-bangla-beginners-guide-google-ranking",
    "international-seo-bangladesh-exporters-global-buyers",
    "content-marketing-strategy-bangladeshi-brands-seo",
]

def find_post(slug):
    # Use a more robust approach - find slug then find the enclosing { ... }
    idx = data.find(f'slug: "{slug}"')
    if idx == -1:
        return None
    # Find the opening { before this line
    before = data.rfind('{', 0, idx)
    if before == -1:
        return None
    # Now find the closing }, (end of post object)
    # Find the matching closing brace
    depth = 0
    in_content = False
    end = before
    for i in range(before, len(data)):
        c = data[i]
        if c == '`' and (i == 0 or data[i-1] != '\\'):
            # Check for template literal boundaries
            if not in_content:
                # Check if this starts content: \`
                if data[max(0,i-1):i+1] == ':\n`' or data[max(0,i-10):i+1].endswith(': `') or data[max(0,i-1):i+1] == ':`':
                    in_content = True
            else:
                # Check for closing backtick
                in_content = False
        if not in_content:
            if c == '{':
                depth += 1
            elif c == '}':
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break
    raw = data[before:end]
    return raw

def extract_field_simple(raw, field):
    """Extract simple string fields."""
    # Try patterns like:   field: "value",
    m = re.search(rf'\b{re.escape(field)}:\s*"([^"]*)"', raw)
    if m:
        return m.group(1)
    # Try multi-line:   field:\n"value",
    m = re.search(rf'\b{re.escape(field)}:\s*\n\s*"([^"]*)"', raw)
    if m:
        return m.group(1)
    return ""

def extract_tags(raw):
    m = re.search(r'\btags:\s*\[(.*?)\]', raw, re.DOTALL)
    if m:
        tags_str = m.group(1)
        tags = re.findall(r'"([^"]*)"', tags_str)
        return tags
    return []

def extract_content(raw):
    """Extract the template literal content."""
    m = re.search(r'content:\s*`(.*)`', raw, re.DOTALL)
    if m:
        return m.group(1)
    return ""

def extract_primary_keyword(title):
    """Extract first meaningful keyword from title."""
    if not title:
        return ""
    
    # For English titles, find key phrase
    if re.match(r'^[a-zA-Z]', title):
        # Take part before colon/dash/em-dash
        first_part = re.split(r'[:\-—]', title)[0].strip()
        # Return first 1-3 words that aren't stop words
        stop_words = {'a', 'an', 'the', 'for', 'in', 'of', 'to', 'and', 'or', 'is', 'are', 'was', 'were',
                      'how', 'what', 'why', 'when', 'where', 'which', 'who', 'at', 'by', 'with', 'from'}
        words = first_part.split()
        result = []
        for w in words:
            w_clean = w.strip('.,;:!?()[]{}""''')
            if w_clean.lower() in stop_words and not result:
                continue
            result.append(w_clean)
            if len(result) >= 2 and len(' '.join(result)) > 5:
                break
            if len(result) >= 3:
                break
        return ' '.join(result) if result else words[0] if words else title
    else:
        # Bengali title - extract first meaningful keyword phrase
        first_part = re.split(r'[:\-—]', title)[0].strip()
        # Remove leading year/numbers (both Bengali and English digits)
        first_part = re.sub(r'^[\d০১২৩৪৫৬৭৮৯]+\s*', '', first_part)
        # Skip introductory/adverbial words, keep content words
        skip_words = {'সহজ', 'সহজভাবে', 'সহজ ভাষায়', 'কীভাবে', 'কেন', 'কী', 'কি', 'বাংলাদেশি', 'বাংলাদেশের',
                      'একটি', 'জন্য', 'এবং', 'যুগে', 'আপনার', 'এই', 'ও', 'তা', 'থেকে', 'দিয়ে', 'করে',
                      'নিয়ে', 'বলে', 'হয়ে', 'পরে', 'আগে', 'মধ্যে', 'ভিতরে', 'বাইরে', 'সাথে'}
        words = first_part.split()
        result = []
        for w in words:
            w_clean = w.strip('.,;:!?()[]{}""''''")
            if w_clean in skip_words:
                continue
            # Skip single-character Bengali items (usually postpositions or particles)
            if len(w_clean) <= 1 and re.search(r'[\u0980-\u09FF]', w_clean):
                continue
            result.append(w_clean)
            # Take 1-2 content words for the keyword
            if len(result) >= 2 and len(' '.join(result)) >= 4:
                break
        # If no result after filtering, fall back to first word that's > 1 char
        if not result:
            for w in words:
                wc = w.strip('.,;:!?()[]{}""\'\'\'')
                if len(wc) > 1:
                    result.append(wc)
                    break
        return ' '.join(result) if result else words[0] if words else title

def count_keyword(content, keyword):
    """Count keyword occurrences in content with case-insensitive matching."""
    if not keyword:
        return 0
    # Escape for regex
    escaped = re.escape(keyword)
    # Try word boundary first for multi-word
    if len(keyword.split()) > 1:
        count = len(re.findall(r'\b' + escaped + r'\b', content, re.IGNORECASE))
        if count > 0:
            return count
    # Fall back to simple count
    return len(re.findall(escaped, content, re.IGNORECASE))

def count_question_headings(content):
    """Count question-based headings."""
    # English question words
    en_pattern = r'^#{2,4}\s+(How\s|What\s|Why\s|When\s|Where\s|Can\s|Do\s|Does\s|Is\s|Are\s|Which\s|Who\s)'
    # Bengali question words/phrases
    bn_pattern = r'^#{2,4}\s+(কীভাবে|কেন\s|কী\s|কি\s|কখন|কোথায়|কত\s|কোন\s|কে\s|কার\s)'
    
    combined = re.compile(f'({en_pattern}|{bn_pattern})', re.MULTILINE | re.IGNORECASE)
    matches = combined.findall(content)
    
    # Also catch FAQ patterns: ### question?
    faq_pattern = re.compile(r'^#{3,4}\s+.*\?\s*$', re.MULTILINE)
    faq_matches = faq_pattern.findall(content)
    
    all_matches = set()
    for m in matches:
        # m is a tuple from groups
        all_matches.add(m[0].strip() if isinstance(m, tuple) else str(m).strip())
    for fm in faq_matches:
        all_matches.add(fm.strip())
    
    return len(all_matches), list(all_matches)[:5]

def run_checks(slug):
    print(f"\n## Post: {slug}")
    
    raw = find_post(slug)
    if not raw:
        print("| Check | Status | Details |")
        print("|-------|--------|---------|")
        print(f"| ALL | ❌ FAIL | Post not found in data.js |")
        print("### Fix instructions: Post slug not found in data file.")
        return
    
    title = extract_field_simple(raw, "title")
    date_val = extract_field_simple(raw, "date")
    excerpt = extract_field_simple(raw, "excerpt")
    tags = extract_tags(raw)
    content = extract_content(raw)
    
    results = {}
    fix_items = []

    # ---- A. TF-IDF ----
    keyword = extract_primary_keyword(title)
    count = count_keyword(content, keyword)
    
    if count < 5:
        status = "❌ FLAG"
        fix_items.append(f"**A. TF-IDF**: Primary keyword '{keyword}' appears {count} time(s) (need ≥ 5). Add more natural occurrences in the content.")
    else:
        status = "✅ PASS"
    results['A. TF-IDF'] = (status, f"Keyword '{keyword}' found {count} times (need ≥ 5)")

    # ---- B. Entities ----
    has_dhaka = bool(re.search(r'ঢাকা|Dhaka', content))
    has_bangladesh = bool(re.search(r'বাংলাদেশ|Bangladesh', content, re.IGNORECASE))
    has_service = bool(re.search(r'\bSEO\b|ডিজিটাল মার্কেটিং|digital marketing|Content Marketing', content, re.IGNORECASE))
    
    missing = []
    if not has_dhaka and not has_bangladesh:
        missing.append("Location (Dhaka/Bangladesh)")
    if not has_service:
        missing.append("Service type (SEO/digital marketing)")
    
    if missing:
        status = "❌ FLAG"
        fix_items.append(f"**B. Entities**: Missing: {', '.join(missing)}.")
    else:
        status = "✅ PASS"
    
    loc_detail = f"Dhaka={'Y' if has_dhaka else 'N'}, Bangladesh={'Y' if has_bangladesh else 'N'}, SEO/DM={'Y' if has_service else 'N'}"
    results['B. Entities'] = (status, f"{loc_detail}")

    # ---- C. Pillar Link ----
    # Determine pillar slugs based on tags
    pillar_rules = {
        'content marketing': ['content-marketing-strategy-bangladeshi-brands-seo'],
        'content writing': ['content-marketing-strategy-bangladeshi-brands-seo'],
        'seo content': ['content-marketing-strategy-bangladeshi-brands-seo'],
        'keyword research': ['complete-seo-guide-bangladesh-businesses-2026'],
        'link building': ['complete-seo-guide-bangladesh-businesses-2026'],
        'backlinks': ['complete-seo-guide-bangladesh-businesses-2026'],
        'ecommerce': ['complete-seo-guide-bangladesh-businesses-2026'],
        'technical seo': ['complete-seo-guide-bangladesh-businesses-2026'],
        'core web vitals': ['complete-seo-guide-bangladesh-businesses-2026'],
        'seo trends': ['complete-seo-guide-bangladesh-businesses-2026'],
        'geo': ['complete-seo-guide-bangladesh-businesses-2026'],
        'ai seo': ['complete-seo-guide-bangladesh-businesses-2026'],
        'local seo': ['complete-seo-guide-bangladesh-businesses-2026'],
        'google maps': ['complete-seo-guide-bangladesh-businesses-2026'],
        'seo basics': ['complete-seo-guide-bangladesh-businesses-2026'],
        'bangla seo': ['complete-seo-guide-bangladesh-businesses-2026'],
        'international seo': ['complete-seo-guide-bangladesh-businesses-2026'],
        'b2b seo': ['complete-seo-guide-bangladesh-businesses-2026'],
        'seo strategy': ['complete-seo-guide-bangladesh-businesses-2026'],
        'digital marketing': ['complete-seo-guide-bangladesh-businesses-2026'],
        'bangladesh seo': ['complete-seo-guide-bangladesh-businesses-2026'],
    }
    
    expected_pillars = set()
    for tag in tags:
        tag_lower = tag.lower().strip()
        for key, pillars in pillar_rules.items():
            if key in tag_lower or tag_lower in key:
                for p in pillars:
                    expected_pillars.add(p)
    
    # If no specific pillar mapping, use default
    if not expected_pillars:
        expected_pillars.add('complete-seo-guide-bangladesh-businesses-2026')
    
    # Find all /blog/ links in content
    blog_links = re.findall(r'/blog/([\w-]+)', content)
    
    # Check if any blog link matches expected pillar slugs (substring match)
    linked_pillars = []
    for bl in blog_links:
        for ep in expected_pillars:
            if bl == ep or ep.startswith(bl) or bl.startswith(ep) or ep in bl or bl in ep:
                linked_pillars.append(bl)
    
    if linked_pillars:
        status = "✅ PASS"
    else:
        status = "❌ FLAG"
        fix_items.append(f"**C. Pillar Link**: No link to pillar page found. Based on tags, expected pillar(s): {expected_pillars}. Blog links found: {blog_links[:5]}. Add a link to the pillar page (e.g., /blog/complete-seo-guide-bangladesh-businesses-2026).")
    
    results['C. Pillar Link'] = (status, f"Expected pillars: {expected_pillars}. Blog links: {blog_links[:5]}. Matched: {linked_pillars[:3] if linked_pillars else 'None'}")

    # ---- D. AEO/GEO ----
    q_count, q_examples = count_question_headings(content)
    
    if q_count < 2:
        status = "❌ FLAG"
        fix_items.append(f"**D. AEO/GEO**: Only {q_count} question-based headings found (need ≥ 2). Add headings starting with How/What/Why or Bengali equivalents.")
    else:
        status = "✅ PASS"
    
    results['D. AEO/GEO'] = (status, f"{q_count} question-based heading(s) found (need ≥ 2). E.g.: {q_examples[:3]}")

    # ---- E. Internal Links ----
    blog_c = len(re.findall(r'/blog/[\w-]+', content))
    svc_c = len(re.findall(r'/services/[\w-]*', content))
    loc_c = len(re.findall(r'/locations/[\w-]*', content))
    ind_c = len(re.findall(r'/industries/[\w-]*', content))
    total = blog_c + svc_c + loc_c + ind_c
    
    if total < 3:
        status = "❌ FLAG"
        fix_items.append(f"**E. Internal Links**: Only {total} internal links (blog:{blog_c} svc:{svc_c} loc:{loc_c} ind:{ind_c}). Need ≥ 3.")
    else:
        status = "✅ PASS"
    
    results['E. Internal Links'] = (status, f"Blog:{blog_c} Svc:{svc_c} Loc:{loc_c} Ind:{ind_c} Total:{total} (need ≥ 3)")

    # ---- F. Schema ----
    missing_schema = []
    if not title: missing_schema.append("title")
    if not excerpt: missing_schema.append("excerpt")
    if not date_val: missing_schema.append("date")
    
    if missing_schema:
        status = "❌ FLAG"
        fix_items.append(f"**F. Schema**: Missing: {', '.join(missing_schema)}.")
    else:
        status = "✅ PASS"
    
    t_preview = (title[:60] + '..') if len(title) > 60 else title
    e_preview = (excerpt[:60] + '..') if len(excerpt) > 60 else excerpt
    results['F. Schema'] = (status, f"Title='{t_preview}' Date='{date_val}' Excerpt='{e_preview}'")

    # ---- Print ----
    print("| Check | Status | Details |")
    print("|-------|--------|---------|")
    for cname, (stat, detail) in results.items():
        det = detail.replace("|", "/").replace("\n", " ")
        print(f"| {cname} | {stat} | {det} |")
    
    print("### Fix instructions:")
    if fix_items:
        for fi in fix_items:
            print(f"- {fi}")
    else:
        print("- All checks passed! No fixes needed.")
    print()

for slug in SLUGS:
    run_checks(slug)
