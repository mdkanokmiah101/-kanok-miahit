#!/usr/bin/env python3
"""
Analyze blog posts from data.js for framework compliance (v3).
Handles both English and Bangla content properly.
Improved keyword extraction with multi-granularity search.
"""

import re
import sys

DATA_FILE = "src/app/blog/data.js"


def extract_post_obj(data, slug):
    """Extract a single post object text by slug using line-based parsing."""
    lines = data.split('\n')
    
    slug_line_idx = None
    for i, line in enumerate(lines):
        if 'slug: "' + slug + '"' in line:
            slug_line_idx = i
            break
    
    if slug_line_idx is None:
        return None
    
    start_idx = slug_line_idx
    while start_idx >= 0:
        stripped = lines[start_idx].strip()
        if stripped == '{' or stripped == '{,':
            break
        start_idx -= 1
    
    brace_depth = 0
    in_content = False
    end_idx = start_idx
    
    for i in range(start_idx, len(lines)):
        stripped = lines[i].strip()
        
        if not in_content:
            brace_depth += stripped.count('{') - stripped.count('}')
            if 'content: `' in lines[i]:
                in_content = True
            if brace_depth <= 0 and i > start_idx:
                end_idx = i
                break
        else:
            if stripped.startswith('`') and i > start_idx:
                in_content = False
            brace_depth += stripped.count('{') - stripped.count('}')
    
    return '\n'.join(lines[start_idx:end_idx+1])


def get_field(obj_text, field_name):
    m = re.search(rf'{re.escape(field_name)}:\s*"([^"]*)"', obj_text)
    return m.group(1) if m else None


def get_content(obj_text):
    idx = obj_text.find('content: `')
    if idx == -1:
        return ""
    bt_open = obj_text.index('`', idx)
    rest = obj_text[bt_open + 1:]
    last_bt = rest.rfind('`')
    return rest[:last_bt] if last_bt != -1 else ""


def get_tags(obj_text):
    m = re.search(r'tags:\s*\[(.*?)\]', obj_text, re.DOTALL)
    return re.findall(r'"([^"]*)"', m.group(1)) if m else []


def best_keyword_match(title, content):
    """Find the best keyword from title and count in content.
    Tries multiple granularities to find the best match."""
    if not title:
        return "keyword", 0
    
    content_lower = content.lower()
    
    # Check if Bangla
    has_bangla = bool(re.search(r'[\u0980-\u09FF]', title))
    
    # Split on colon or dash to get main phrase
    main_part = re.split(r'[:\-–—]', title)[0].strip()
    
    if has_bangla:
        bangla_stop = {'জন্য', 'এবং', 'কীভাবে', 'বনাম', 'থেকে', 'করা', 'হয়', 'এই', 'তা', 'একটি', 'বাংলাদেশি', 'বাংলাদেশের', 'নিজেই'}
        words = main_part.split()
        # Try combinations: full phrase, without stop words, first 2, first word
        candidates = [main_part]
        
        # Remove trailing English words (like "SEO" at end of Bangla phrase)
        # e.g. "ফেসবুক মার্কেটপ্লেস SEO" -> "ফেসবুক মার্কেটপ্লেস"
        clean_words = []
        for w in words:
            is_bangla = bool(re.search(r'[\u0980-\u09FF]', w))
            if is_bangla or not clean_words:
                clean_words.append(w)
            else:
                break  # Stop at first English word after Bangla words
        if clean_words != words:
            candidates.append(' '.join(clean_words))
        
        # Remove stop words
        filtered = [w for w in words if w.lower() not in bangla_stop and w not in bangla_stop]
        if filtered and ' '.join(filtered) != main_part:
            candidates.append(' '.join(filtered))
        
        # First 2 words of filtered
        if len(filtered) >= 2:
            candidates.append(' '.join(filtered[:2]))
        
        # First word
        if filtered:
            candidates.append(filtered[0])
        elif words:
            candidates.append(words[0])
        
    else:
        # English title
        stop_words = {'a', 'an', 'the', 'for', 'in', 'of', 'to', 'and', 'or', 'vs', 'vs.', 'your', 'is', 'are', 'that', 'with', 'by', 'on', 'at', 'from'}
        words = main_part.lower().replace('-', ' ').split()
        
        candidates = [main_part.lower()]
        
        # Remove leading SEO/generic words to find core topic
        # e.g., "Complete SEO Guide for Bangladesh..." -> "seo guide"
        generic_prefixes = ['complete', 'ultimate', 'best', 'top', 'essential', 'beginner', 'advanced', 'expert']
        clean_words = [w for w in words if w not in generic_prefixes and w not in ['a', 'an', 'the']]
        if clean_words and ' '.join(clean_words) != main_part.lower():
            candidates.append(' '.join(clean_words))
        
        # Remove stop words
        filtered = [w for w in clean_words if w not in stop_words]
        if filtered and ' '.join(filtered) != ' '.join(clean_words):
            candidates.append(' '.join(filtered))
        
        # First 2 words of filtered
        if len(filtered) >= 2:
            candidates.append(' '.join(filtered[:2]))
        
        # First word
        if filtered:
            candidates.append(filtered[0])
    
    # Deduplicate candidates while preserving order
    seen = set()
    unique_candidates = []
    for c in candidates:
        if c not in seen:
            seen.add(c)
            unique_candidates.append(c)
    
    # Test each candidate and pick the one with highest count (preferring longer matches)
    best_count = 0
    best_kw = unique_candidates[0] if unique_candidates else "keyword"
    
    for kw in unique_candidates:
        c = content_lower.count(kw.lower())
        # Prefer longer keywords if they have reasonable count
        if c > best_count or (c == best_count and len(kw) > len(best_kw)):
            best_count = c
            best_kw = kw
    
    # Edge case: if "seo" is in the title but content uses it abundantly
    # Make sure we catch this
    if best_count < 5 and 'seo' in content_lower:
        seo_count = content_lower.count('seo')
        if seo_count > best_count:
            # Only use SEO as keyword if the title is SEO-themed
            if 'seo' in title.lower():
                best_count = seo_count
                best_kw = 'SEO'
    
    # Edge case for Bangla titles: if Bangla keyword doesn't match but English does
    # e.g. Title uses "এসইও" but content uses "SEO"
    if best_count < 5 and has_bangla:
        # Try English equivalents of common Bangla terms in title
        english_fallbacks = {
            'এসইও': 'seo',
            'গুগল': 'google',
            'অ্যাডস': 'ads',
            'ফেসবুক': 'facebook',
            'ইউটিউব': 'youtube',
            'বাংলাদেশ': 'bangladesh',
            'বাংলাদেশি': 'bangladeshi',
            'মোবাইল': 'mobile',
        }
        for bangla_term, english_term in english_fallbacks.items():
            if bangla_term in title and english_term in content_lower:
                c = content_lower.count(english_term)
                if c > best_count:
                    best_count = c
                    best_kw = english_term
    
    return best_kw, best_count


# ----- CHECK FUNCTIONS -----

def check_tfidf(title, content):
    if not title:
        return "❌", "No title found"
    keyword, count = best_keyword_match(title, content)
    status = "✅" if count >= 5 else "❌"
    return status, str(count) + " occurrences of '" + keyword + "'"


def check_entities(title, content, tags):
    content_lower = content.lower()
    title_lower = title.lower() if title else ""
    all_text = content_lower + " " + title_lower
    
    locations = {
        "location (Bangladesh)": ["bangladesh", "bangladeshi", "বাংলাদেশ", "বাংলাদেশি"],
        "location (Dhaka)": ["dhaka", "ঢাকা", "ঢাকায়", "dhaka"],
    }
    
    services = {
        "service (SEO)": ["seo", "search engine optimization", "এসইও"],
        "service (digital marketing)": ["digital marketing", "ডিজিটাল মার্কেটিং", "ডিজিটাল বিপণন"],
    }
    
    missing = []
    for name, keywords in locations.items():
        if not any(kw in all_text for kw in keywords):
            missing.append(name)
    
    for name, keywords in services.items():
        if not any(kw in all_text for kw in keywords):
            missing.append(name)
    
    status = "✅" if len(missing) == 0 else "❌"
    details = "All entities present" if len(missing) == 0 else "Missing: " + ', '.join(missing)
    return status, details


def check_pillar_cluster(slug, tags, content):
    if not tags:
        return "❌", "No tags defined"
    
    pillar_map = {
        "seo guide": "/blog/complete-seo-guide-bangladesh-businesses-2026",
        "bangladesh seo": "/blog/complete-seo-guide-bangladesh-businesses-2026",
        "digital marketing": "/blog/complete-seo-guide-bangladesh-businesses-2026",
        "2026": "/blog/complete-seo-guide-bangladesh-businesses-2026",
        "seo": "/blog/complete-seo-guide-bangladesh-businesses-2026",
        "ফেসবুক মার্কেটপ্লেস": "/blog/seo-for-facebook-marketplace",
        "facebook marketplace": "/blog/seo-for-facebook-marketplace",
        "প্রোডাক্ট seo": "/blog/seo-for-facebook-marketplace",
        "লং-টেল কীওয়ার্ড": "/blog/long-tail-keywords-bangladesh",
        "long tail keywords": "/blog/long-tail-keywords-bangladesh",
        "keyword research": "/blog/long-tail-keywords-bangladesh",
        "কীওয়ার্ড রিসার্চ": "/blog/long-tail-keywords-bangladesh",
        "seo কৌশল": "/blog/long-tail-keywords-bangladesh",
        "ব্যবসায়ীদের জন্য seo": "/blog/seo-tips-for-business-owners-bd",
        "diy seo": "/blog/seo-tips-for-business-owners-bd",
        "seo tips": "/blog/seo-tips-for-business-owners-bd",
        "লোকাল seo": "/blog/seo-tips-for-business-owners-bd",
        "বাংলা ব্লগিং": "/blog/seo-bangla-blog-content-writing",
        "seo কন্টেন্ট রাইটিং": "/blog/seo-bangla-blog-content-writing",
        "content writing": "/blog/seo-bangla-blog-content-writing",
        "কন্টেন্ট অপটিমাইজেশন": "/blog/seo-bangla-blog-content-writing",
        "seo vs google ads": "/blog/seo-vs-google-ads-bangladesh-business",
        "ppc": "/blog/seo-vs-google-ads-bangladesh-business",
        "online advertising": "/blog/seo-vs-google-ads-bangladesh-business",
        "ডিজিটাল মার্কেটিং": "/blog/seo-vs-google-ads-bangladesh-business",
        "ইউটিউব seo": "/blog/youtube-seo-bangladesh-ranking-tips",
        "youtube seo": "/blog/youtube-seo-bangladesh-ranking-tips",
        "youtube ranking": "/blog/youtube-seo-bangladesh-ranking-tips",
        "ভিডিও অপটিমাইজেশন": "/blog/youtube-seo-bangladesh-ranking-tips",
        "youtube algorithm": "/blog/youtube-seo-bangladesh-ranking-tips",
        "স্কিমা মার্কআপ": "/blog/schema-markup-rich-snippets-techniques",
        "schema markup": "/blog/schema-markup-rich-snippets-techniques",
        "rich snippets": "/blog/schema-markup-rich-snippets-techniques",
        "structured data": "/blog/schema-markup-rich-snippets-techniques",
        "মোবাইল seo": "/blog/mobile-seo-bangladesh-ranking-strategy",
        "mobile seo": "/blog/mobile-seo-bangladesh-ranking-strategy",
        "mobile first": "/blog/mobile-seo-bangladesh-ranking-strategy",
        "ভয়েস সার্চ": "/blog/mobile-seo-bangladesh-ranking-strategy",
        "voice search": "/blog/mobile-seo-bangladesh-ranking-strategy",
        "mobile optimization": "/blog/mobile-seo-bangladesh-ranking-strategy",
        "গুগল সার্চ কনসোল": "/blog/google-search-console-performance-guide",
        "google search console": "/blog/google-search-console-performance-guide",
        "seo টুল": "/blog/google-search-console-performance-guide",
        "ওয়েবসাইট পারফরমেন্স": "/blog/google-search-console-performance-guide",
    }
    
    pillar_link = None
    for tag in tags:
        tag_lower = tag.lower().strip()
        if tag_lower in pillar_map:
            pillar_link = pillar_map[tag_lower]
            break
    
    if not pillar_link:
        return "⚠️", "Cannot determine pillar from tags: " + ', '.join(tags[:3])
    
    own_slug = "/blog/" + slug
    if pillar_link == own_slug:
        return "✅", "This post IS the pillar page (self-link not needed)"
    
    content_lower = content.lower()
    if pillar_link in content_lower:
        return "✅", "Links to pillar: " + pillar_link
    
    slug_name = pillar_link.split('/')[-1]
    if slug_name in content_lower:
        return "✅", "Links to pillar: " + pillar_link
    
    return "❌", "No link to pillar page (" + pillar_link + ")"


def check_aeo_geo(content):
    """Check D: AEO/GEO Optimization - question headings (English + Bangla)."""
    # Find all headings
    all_headings = re.findall(r'^#{2,4}\s+(.+)', content, re.MULTILINE)
    
    # English question word starters
    en_q = [h for h in all_headings if re.match(r'(How|What|Why|When|Where|Can|Do|Is|Are)\b', h, re.IGNORECASE)]
    
    # Bangla question word starters
    bn_q = [h for h in all_headings if re.match(r'(কি|কেন|কীভাবে|কোথায়|কখন|কত|কে|কার|কোন|কোনটি)\b', h)]
    
    # Headings with question mark (includes those already counted above, but that's fine for threshold)
    q_mark = [h for h in all_headings if '?' in h]
    
    # Total unique question-based headings (union)
    all_question_set = set()
    for h in en_q:
        all_question_set.add(h.lower().strip())
    for h in bn_q:
        all_question_set.add(h.strip())
    for h in q_mark:
        all_question_set.add(h.strip().lower())
    
    total = len(all_question_set)
    status = "✅" if total >= 2 else "❌"
    details = str(len(en_q)) + " English Q, " + str(len(bn_q)) + " Bangla Q, " + str(len(q_mark)) + " with '?' (" + str(total) + " unique)"
    return status, details


def check_internal_links(content):
    blog_links = re.findall(r'/blog/[^"\')\s]+', content)
    services_links = re.findall(r'/services/[^"\')\s]+', content)
    locations_links = re.findall(r'/locations/[^"\')\s]+', content)
    industries_links = re.findall(r'/industries/[^"\')\s]+', content)
    
    total = len(blog_links) + len(services_links) + len(locations_links) + len(industries_links)
    
    status = "✅" if total >= 3 else "❌"
    details = str(total) + " total (" + str(len(blog_links)) + " blog, " + str(len(services_links)) + " services, " + str(len(locations_links)) + " locations, " + str(len(industries_links)) + " industries)"
    return status, details


def check_schema(obj_text):
    title = get_field(obj_text, 'title')
    excerpt = get_field(obj_text, 'excerpt')
    date = get_field(obj_text, 'date')
    
    missing = []
    if not title:
        missing.append('title')
    if not excerpt:
        missing.append('excerpt')
    if not date:
        missing.append('date')
    
    date_modified = get_field(obj_text, 'dateModified')
    
    status = "✅" if len(missing) == 0 else "❌"
    details = "All fields set" if len(missing) == 0 else "Missing: " + ', '.join(missing)
    if date_modified:
        details += " (has dateModified too)"
    return status, details


def analyze_post(slug, data):
    obj_text = extract_post_obj(data, slug)
    if not obj_text:
        return "## Post: " + slug + "\nCould not extract post data"
    
    title = get_field(obj_text, 'title') or ""
    content = get_content(obj_text)
    tags = get_tags(obj_text)
    
    if not content:
        return "## Post: " + slug + "\nCould not extract content"
    
    tfidf_status, tfidf_details = check_tfidf(title, content)
    entities_status, entities_details = check_entities(title, content, tags)
    pillar_status, pillar_details = check_pillar_cluster(slug, tags, content)
    aeo_status, aeo_details = check_aeo_geo(content)
    links_status, links_details = check_internal_links(content)
    schema_status, schema_details = check_schema(obj_text)
    
    # Build fix instructions
    fix_instructions = []
    
    if tfidf_status and "❌" in tfidf_status:
        m = re.search(r"'([^']*)'", tfidf_details)
        kw = m.group(1) if m else "primary keyword"
        fix_instructions.append("- **TF-IDF**: Only " + tfidf_details.split()[0] + " occurrences of '" + kw + "'. Add more mentions - aim for at least 5.")
    
    if entities_status and "❌" in entities_status:
        m = re.search(r'Missing: (.+)', entities_details)
        if m:
            for entity in m.group(1).split(', '):
                fix_instructions.append("- **Entities**: Add mention of " + entity)
    
    if pillar_status and ("❌" in pillar_status or "⚠️" in pillar_status):
        if "No link" in pillar_details:
            fix_instructions.append("- **Pillar Link**: " + pillar_details)
        elif "not clearly" in pillar_details:
            fix_instructions.append("- **Pillar Link**: " + pillar_details)
    
    if aeo_status and "❌" in aeo_status:
        fix_instructions.append("- **AEO/GEO**: Add more question-based headings (How, What, Why, etc.). Aim for at least 2.")
    
    if links_status and "❌" in links_status:
        fix_instructions.append("- **Internal Links**: Add more internal links to /blog/, /services/, or /locations/. Aim for at least 3 total.")
    
    if schema_status and "❌" in schema_status:
        m = re.search(r'Missing: (.+)', schema_details)
        if m:
            for field in m.group(1).split(', '):
                fix_instructions.append("- **Schema**: Add missing field '" + field + "' (title/excerpt/date)")
    
    fixes = "\n".join(fix_instructions) if fix_instructions else "No fixes needed - all checks pass."
    
    # Get keyword for display
    kw_display, _ = best_keyword_match(title, content)
    
    output = """## Post: """ + slug + """
| Check | Status | Details |
|-------|--------|---------|
| TF-IDF: """ + kw_display + """ | """ + tfidf_status + """ | """ + tfidf_details + """ |
| Entities | """ + entities_status + """ | """ + entities_details + """ |
| Pillar Link | """ + pillar_status + """ | """ + pillar_details + """ |
| AEO/GEO | """ + aeo_status + """ | """ + aeo_details + """ |
| Internal Links | """ + links_status + """ | """ + links_details + """ |
| Schema Ready | """ + schema_status + """ | """ + schema_details + """ |

### Fix instructions:
""" + fixes + "\n"
    return output


def main():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = f.read()
    
    slugs = [
        "complete-seo-guide-bangladesh-businesses-2026",
        "seo-for-facebook-marketplace",
        "long-tail-keywords-bangladesh",
        "seo-tips-for-business-owners-bd",
        "seo-bangla-blog-content-writing",
        "seo-vs-google-ads-bangladesh-business",
        "youtube-seo-bangladesh-ranking-tips",
        "schema-markup-rich-snippets-techniques",
        "mobile-seo-bangladesh-ranking-strategy",
        "google-search-console-performance-guide",
    ]
    
    results = []
    for slug in slugs:
        print("Analyzing: " + slug + "...", file=sys.stderr)
        result = analyze_post(slug, data)
        results.append(result)
    
    full_report = '\n---\n'.join(results)
    sys.stdout.write(full_report)


if __name__ == '__main__':
    main()
