#!/usr/bin/env python3
"""
Analyze blog posts from data.js for framework compliance.
Handles both English and Bangla content properly.
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
    
    # Go back to find opening {
    start_idx = slug_line_idx
    while start_idx >= 0:
        stripped = lines[start_idx].strip()
        if stripped == '{' or stripped == '{,':
            break
        start_idx -= 1
    
    # Go forward to find closing }
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
    
    obj_text = '\n'.join(lines[start_idx:end_idx+1])
    return obj_text


def get_field(obj_text, field_name):
    """Extract a simple quoted string field value."""
    m = re.search(rf'{re.escape(field_name)}:\s*"([^"]*)"', obj_text)
    if m:
        return m.group(1)
    return None


def get_content(obj_text):
    """Extract content from template literal."""
    idx = obj_text.find('content: `')
    if idx == -1:
        return ""
    
    bt_open = obj_text.index('`', idx)
    content_start = bt_open + 1
    rest = obj_text[content_start:]
    
    last_bt = rest.rfind('`')
    if last_bt == -1:
        return ""
    
    return rest[:last_bt]


def get_tags(obj_text):
    """Extract tags array."""
    m = re.search(r'tags:\s*\[(.*?)\]', obj_text, re.DOTALL)
    if m:
        return re.findall(r'"([^"]*)"', m.group(1))
    return []


# ----- KEYWORD EXTRACTION -----

def extract_keyword_from_title(title):
    """Extract the best SEO keyword from a title."""
    if not title:
        return "keyword"
    
    title_lower = title.lower().strip()
    
    # For English titles, extract meaningful keyword
    # Strategy: find the core topic/entity
    # Patterns:
    # "Complete SEO Guide for..." -> "SEO"
    # "SEO for Facebook Marketplace" -> "Facebook Marketplace" 
    # "Long Tail Keywords Bangladesh" -> "long tail keywords"
    
    # Check if title has Bangla characters
    has_bangla = bool(re.search(r'[\u0980-\u09FF]', title))
    
    if has_bangla:
        # For Bangla titles, extract the first meaningful keyword phrase
        # Remove common Bangla stop words
        bangla_stop = ['জন্য', 'এবং', 'কীভাবে', 'বনাম', 'থেকে', 'করা', 'হয়', 'এই', 'তা', 'একটি', 'বাংলাদেশি', 'বাংলাদেশের']
        title_clean = title
        for sw in bangla_stop:
            title_clean = title_clean.replace(' ' + sw + ' ', ' ')
        # Remove after colon or dash
        title_clean = re.split(r'[:\-–—]', title_clean)[0].strip()
        # Take first 2-3 words
        words = title_clean.split()
        # Try the full first phrase minus stop words
        keyword_parts = [w for w in words[:4] if w not in bangla_stop]
        if keyword_parts:
            return ' '.join(keyword_parts[:3])
        return ' '.join(words[:3])
    else:
        # English title
        # Remove trailing year patterns like "in 2026"
        title_clean = re.sub(r'\s+in\s+\d{4}$', '', title_lower)
        # Remove common prefixes/suffixes
        title_clean = re.sub(r'^(complete|ultimate|best|top|essential|beginner.s|advanced)\s+', '', title_clean)
        
        stop_words = {'a', 'an', 'the', 'for', 'in', 'of', 'to', 'and', 'or', 'vs', 'vs.', 'your', 'is', 'are', 'that', 'with', 'by', 'on', 'at', 'from'}
        words = title_clean.replace('-', ' ').split()
        
        # Strategy: find the core keyword
        # "SEO Guide for Bangladesh Businesses 2026" -> try "seo guide" then "seo"
        # "SEO for Facebook Marketplace" -> try "facebook marketplace" 
        # Remove leading 'seo' if followed by more specific terms
        # Actually, for SEO content, the primary keyword is usually the main subject
        
        # Try to extract the main subject phrase (before connecting words)
        keyword_parts = []
        for w in words:
            if w in stop_words:
                if len(keyword_parts) >= 2:
                    break
                continue
            keyword_parts.append(w)
        
        if not keyword_parts:
            return words[0] if words else "keyword"
        
        # Return the best keyword
        return ' '.join(keyword_parts[:3])


def count_keyword_in_content(keyword, content):
    """Count occurrences of a keyword in content, trying multiple forms."""
    content_lower = content.lower()
    
    # Try exact match first
    kw_lower = keyword.lower()
    count = content_lower.count(kw_lower)
    
    # If the keyword is English and content is Bangla-heavy, 
    # also check for the English version (e.g., "SEO" appearing in Bangla content)
    has_bangla = bool(re.search(r'[\u0980-\u09FF]', content))
    
    if count == 0 and not has_bangla:
        # Try just the first word
        first_word = kw_lower.split()[0] if ' ' in kw_lower else kw_lower
        count = content_lower.count(first_word)
        if count > 0:
            return count, first_word
    
    # For English keywords in predominantly English content
    if count < 3:
        # Try simpler forms
        words = kw_lower.split()
        for w in words:
            if len(w) > 2:  # Skip short words
                c = content_lower.count(w)
                if c > count:
                    count = c
                    break
    
    return count, keyword


# ----- CHECK FUNCTIONS -----

def check_tfidf(title, content):
    """Check A: TF-IDF Coverage."""
    if not title:
        return "❌", "No title found - cannot determine keyword"
    
    keyword = extract_keyword_from_title(title)
    count, used_kw = count_keyword_in_content(keyword, content)
    
    status = "✅" if count >= 5 else "❌"
    return status, str(count) + " occurrences of '" + used_kw + "'"


def check_entities(title, content, tags):
    """Check B: Semantic Entity Coverage."""
    content_lower = content.lower()
    title_lower = title.lower() if title else ""
    all_text = content_lower + " " + title_lower
    
    # Check locations - both English and Bangla
    locations = {
        "location (Bangladesh)": ["bangladesh", "bangladeshi", "বাংলাদেশ", "বাংলাদেশি"],
        "location (Dhaka)": ["dhaka", "ঢাকা"],
    }
    
    # Service types - both English and Bangla
    services = {
        "service (SEO)": ["seo", "search engine optimization", "এসইও"],
        "service (digital marketing)": ["digital marketing", "ডিজিটাল মার্কেটিং", "ডিজিটাল বিপণন"],
    }
    
    missing = []
    
    for name, keywords in locations.items():
        found = any(kw in all_text for kw in keywords)
        if not found:
            missing.append(name)
    
    for name, keywords in services.items():
        found = any(kw in all_text for kw in keywords)
        if not found:
            missing.append(name)
    
    # Check for other Bangladeshi cities
    bd_cities = [
        ("chittagong", "চট্টগ্রাম"), ("sylhet", "সিলেট"), ("khulna", "খুলনা"),
        ("rajshahi", "রাজশাহী"), ("comilla", "কুমিল্লা"), ("bogura", "বগুড়া"),
        ("barisal", "বরিশাল"), ("mymensingh", "ময়মনসিংহ"), ("rangpur", "রংপুর")
    ]
    found_cities = []
    for eng, ban in bd_cities:
        if eng in all_text or ban in all_text:
            found_cities.append(eng)
    
    # Only flag if no Bangladeshi location at all
    has_location = bool(found_cities) or "dhaka" in all_text.lower() or "ঢাকা" in all_text or "bangladesh" in all_text.lower()
    
    status = "✅" if len(missing) == 0 else "❌"
    details = "All entities present" if len(missing) == 0 else "Missing: " + ', '.join(missing)
    return status, details


def check_pillar_cluster(slug, tags, content):
    """Check C: Pillar-Cluster Alignment."""
    if not tags:
        return "❌", "No tags defined"
    
    # Map tags to pillar page URLs (both English and Bangla tags)
    pillar_map = {
        "seo guide": "/blog/complete-seo-guide-bangladesh-businesses-2026",
        "bangladesh seo": "/blog/complete-seo-guide-bangladesh-businesses-2026",
        "digital marketing": "/blog/complete-seo-guide-bangladesh-businesses-2026",
        "2026": "/blog/complete-seo-guide-bangladesh-businesses-2026",
        "seo": "/blog/complete-seo-guide-bangladesh-businesses-2026",
        "ফেসবুক মার্কেটপ্লেস": "/blog/seo-for-facebook-marketplace",
        "facebook marketplace": "/blog/seo-for-facebook-marketplace",
        "লং-টেল কীওয়ার্ড": "/blog/long-tail-keywords-bangladesh",
        "long tail keywords": "/blog/long-tail-keywords-bangladesh",
        "keyword research": "/blog/long-tail-keywords-bangladesh",
        "কীওয়ার্ড রিসার্চ": "/blog/long-tail-keywords-bangladesh",
        "ব্যবসায়ীদের জন্য seo": "/blog/seo-tips-for-business-owners-bd",
        "diy seo": "/blog/seo-tips-for-business-owners-bd",
        "seo tips": "/blog/seo-tips-for-business-owners-bd",
        "বাংলা ব্লগিং": "/blog/seo-bangla-blog-content-writing",
        "seo কন্টেন্ট রাইটিং": "/blog/seo-bangla-blog-content-writing",
        "content writing": "/blog/seo-bangla-blog-content-writing",
        "seo vs google ads": "/blog/seo-vs-google-ads-bangladesh-business",
        "ppc": "/blog/seo-vs-google-ads-bangladesh-business",
        "ইউটিউব seo": "/blog/youtube-seo-bangladesh-ranking-tips",
        "youtube seo": "/blog/youtube-seo-bangladesh-ranking-tips",
        "youtube ranking": "/blog/youtube-seo-bangladesh-ranking-tips",
        "স্কিমা মার্কআপ": "/blog/schema-markup-rich-snippets-techniques",
        "schema markup": "/blog/schema-markup-rich-snippets-techniques",
        "rich snippets": "/blog/schema-markup-rich-snippets-techniques",
        "structured data": "/blog/schema-markup-rich-snippets-techniques",
        "মোবাইল seo": "/blog/mobile-seo-bangladesh-ranking-strategy",
        "mobile seo": "/blog/mobile-seo-bangladesh-ranking-strategy",
        "mobile first": "/blog/mobile-seo-bangladesh-ranking-strategy",
        "voice search": "/blog/mobile-seo-bangladesh-ranking-strategy",
        "গুগল সার্চ কনসোল": "/blog/google-search-console-performance-guide",
        "google search console": "/blog/google-search-console-performance-guide",
        "seo টুল": "/blog/google-search-console-performance-guide",
    }
    
    pillar_link = None
    for tag in tags:
        tag_lower = tag.lower().strip()
        if tag_lower in pillar_map:
            pillar_link = pillar_map[tag_lower]
            break
    
    if not pillar_link:
        return "⚠️", "Cannot determine pillar from tags: " + ', '.join(tags[:3])
    
    # If this post IS the pillar page, no need to link to itself
    own_slug = "/blog/" + slug
    if pillar_link == own_slug:
        return "✅", "This post IS the pillar page (self-link not needed)"
    
    # Check if post links to the pillar page
    content_lower = content.lower()
    if pillar_link in content_lower:
        return "✅", "Links to pillar: " + pillar_link
    
    slug_name = pillar_link.split('/')[-1]
    if slug_name in content_lower:
        return "✅", "Links to pillar: " + pillar_link
    
    return "❌", "No link to pillar page (" + pillar_link + ")"


def check_aeo_geo(content):
    """Check D: AEO/GEO Optimization - question headings."""
    # Count question-based headings (## or ### lines starting with question words)
    heading_pattern = re.compile(r'^#{2,4}\s+(How|What|Why|When|Where|Can|Do|Is|Are)\b', re.MULTILINE | re.IGNORECASE)
    question_headings = heading_pattern.findall(content)
    
    count = len(question_headings)
    status = "✅" if count >= 2 else "❌"
    return status, str(count) + " question headings"


def check_internal_links(content):
    """Check E: Internal Linking."""
    blog_links = re.findall(r'/blog/[^"\')\s]+', content)
    services_links = re.findall(r'/services/[^"\')\s]+', content)
    locations_links = re.findall(r'/locations/[^"\')\s]+', content)
    industries_links = re.findall(r'/industries/[^"\')\s]+', content)
    
    total = len(blog_links) + len(services_links) + len(locations_links) + len(industries_links)
    
    status = "✅" if total >= 3 else "❌"
    details = str(total) + " total (" + str(len(blog_links)) + " blog, " + str(len(services_links)) + " services, " + str(len(locations_links)) + " locations, " + str(len(industries_links)) + " industries)"
    return status, details


def check_schema(obj_text):
    """Check F: Schema - title, excerpt, date."""
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
    """Run all 6 checks on a post."""
    obj_text = extract_post_obj(data, slug)
    if not obj_text:
        return "## Post: " + slug + "\nCould not extract post data for slug: " + slug
    
    title = get_field(obj_text, 'title') or ""
    content = get_content(obj_text)
    tags = get_tags(obj_text)
    
    if not content:
        return "## Post: " + slug + "\nCould not extract content for slug: " + slug
    
    # Run checks
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
        fix_instructions.append("- **TF-IDF**: Add more occurrences of '" + kw + "' - aim for at least 5 mentions in the content")
    
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
        fix_instructions.append("- **AEO/GEO**: Add more question-based headings (How, What, Why). Aim for at least 2.")
    
    if links_status and "❌" in links_status:
        fix_instructions.append("- **Internal Links**: Add more internal links to /blog/, /services/, or /locations/. Aim for at least 3 total.")
    
    if schema_status and "❌" in schema_status:
        m = re.search(r'Missing: (.+)', schema_details)
        if m:
            for field in m.group(1).split(', '):
                fix_instructions.append("- **Schema**: Add missing field '" + field + "' (title/excerpt/date)")
    
    fixes = "\n".join(fix_instructions) if fix_instructions else "No fixes needed - all checks pass."
    
    # Display keyword
    keyword = extract_keyword_from_title(title)
    
    output = """## Post: """ + slug + """
| Check | Status | Details |
|-------|--------|---------|
| TF-IDF: """ + keyword + """ | """ + tfidf_status + """ | """ + tfidf_details + """ |
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
    
    sys.stdout.write('\n'.join(results))


if __name__ == '__main__':
    main()
