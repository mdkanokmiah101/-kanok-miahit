#!/usr/bin/env python3
"""
Comprehensive Content Framework Check for 21 Modified Blog Posts.
Reads data.js, extracts each post, runs A-F checks, produces markdown report.
Version 2 - Fixed parsing.
"""

import re
from datetime import date

MODIFIED_SLUGS = [
    "geo-optimization-prepare-business-ai-search",
    "seo-garments-textile-industry-b2b-lead-generation",
    "mobile-seo-optimization-bangladesh-mobile-first-era",
    "seo-healthcare-medical-clinics-bangladesh",
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
    "how-to-choose-best-seo-expert-dhaka-15-things",
    "seo-expert-vs-seo-agency-dhaka-which-is-right",
    "top-10-seo-mistakes-dhaka-businesses-fix",
    "what-does-seo-expert-do-guide-business-owners",
    "seo-case-study-dhaka-businesses-increased-organic-traffic",
    "hiring-seo-expert-dhaka-better-roi-than-paid-ads",
    "ai-seo-2026-dhaka-experts-optimize-google-ai-chatgpt",
]

STOPWORDS = {
    'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
    'of', 'by', 'with', 'from', 'is', 'are', 'was', 'were', 'be', 'been',
    'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
    'could', 'should', 'may', 'might', 'shall', 'can', 'need', 'dare',
    'ought', 'used', 'this', 'that', 'these', 'those', 'i', 'you', 'he',
    'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them', 'my',
    'your', 'his', 'its', 'our', 'their', 'mine', 'yours', 'hers', 'ours',
    'theirs', 'what', 'which', 'who', 'whom', 'whose', 'when', 'where',
    'why', 'how', 'all', 'each', 'every', 'both', 'few', 'more', 'most',
    'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same',
    'so', 'than', 'too', 'very', 'just', 'because', 'as', 'until', 'while',
    'about', 'between', 'through', 'during', 'before', 'after', 'above',
    'below', 'up', 'down', 'out', 'off', 'over', 'under', 'again', 'further',
    'then', 'once', 'here', 'there'
}

QUESTION_WORDS = ['How', 'What', 'Why', 'When', 'Where', 'Can', 'Do', 'Is', 'Are']


def determine_pillar(tags):
    tag_lower = [t.lower() for t in tags]
    if any('geo' in t or 'ai search' in t or 'generative' in t for t in tag_lower):
        return "AI/GEO"
    if any('case study' in t.lower() for t in tags):
        return "Case Studies"
    if any(t.lower() in ('local seo', 'gbp', 'google maps') for t in tags):
        return "Local SEO"
    if any('e-commerce' in t.lower() or 'ecommerce' in t.lower() or 'daraz' in t.lower() or 'shopify' in t.lower() for t in tag_lower):
        return "E-commerce SEO"
    if any('healthcare' in t.lower() or 'medical' in t.lower() or 'clinic' in t.lower() for t in tag_lower):
        return "Industry SEO"
    if any('garment' in t.lower() or 'textile' in t.lower() for t in tag_lower):
        return "Industry SEO"
    if any('mobile' in t.lower() for t in tag_lower):
        return "Mobile SEO"
    if any('technical' in t.lower() or 'core web' in t.lower() for t in tag_lower):
        return "Technical SEO"
    if any('link building' in t.lower() for t in tag_lower):
        return "Link Building"
    if any('content' in t.lower() for t in tag_lower):
        return "Content Marketing"
    if any('seo' in t.lower() for t in tag_lower):
        return "SEO"
    return "General"


def extract_keyword(title):
    """
    Extract primary keyword from title.
    """
    # Try parenthesized term first (GEO, AEO, etc.) - but skip percentages, numbers, and conjunction phrases
    paren_match = re.search(r'\(([^)]+)\)', title)
    if paren_match:
        kw = paren_match.group(1).strip()
        # Skip if it starts with a conjunction/stopword, or is a number/percentage
        first_word = kw.split()[0].lower() if kw.split() else ''
        is_abbreviation = (len(kw) <= 8 and kw.isupper() and kw.isalpha())
        is_number = bool(re.match(r'^[\d,.%+]', kw))
        is_conjunction = first_word in ('and', 'or', 'but', 'how', 'what', 'why', 'the', 'a', 'an')
        if (is_abbreviation or len(kw) > 2) and not is_number and not is_conjunction:
            return kw

    # Remove trailing parenthetical and subtitle after colon/dash for core keyword
    core = title.split(':')[0].split('—')[0].split('–')[0].strip()
    core = re.sub(r'\([^)]*\)', '', core).strip()
    
    # Remove common prefixes like "Why", "How to", "Top 10", "What"
    core = re.sub(r'^(Why|How|What|When|Where|Top\s+\d+|The|A|An)\s+', '', core, flags=re.IGNORECASE).strip()
    
    words = re.findall(r"[A-Za-z0-9\x80-\xFF']+", core)
    meaningful = [w for w in words if w.lower() not in STOPWORDS and len(w) > 2]
    
    if not meaningful:
        meaningful = [w for w in words if w.lower() not in STOPWORDS and len(w) > 1]
    
    if meaningful:
        return ' '.join(meaningful[:2])
    
    # Fallback: use first 2 non-stopwords from original title
    all_words = re.findall(r"[A-Za-z0-9\x80-\xFF']+", title)
    meaningful = [w for w in all_words if w.lower() not in STOPWORDS and len(w) > 1]
    return ' '.join(meaningful[:2]) if meaningful else title


def count_keyword_occurrences(keyword, content):
    """Count case-insensitive occurrences of keyword as individual words or phrase."""
    if not keyword:
        return 0
    
    content_lower = content.lower()
    keyword_lower = keyword.lower()
    
    # Count as phrase first
    phrase_count = len(re.findall(re.escape(keyword_lower), content_lower))
    
    # Also count individual words
    words = keyword_lower.split()
    word_counts = []
    for w in words:
        word_counts.append(len(re.findall(r'\b' + re.escape(w) + r'\b', content_lower)))
    
    # If individual words appear more than the phrase, use the minimum individual count
    if word_counts:
        min_word_count = min(word_counts)
        return max(phrase_count, min_word_count)
    return phrase_count


def check_entities(content, tags, slug, title):
    entities_to_check = {
        'Dhaka': r'\b[Dd]haka\b',
        'Bangladesh': r'\b[Bb]angladesh\b',
        'SEO': r'\b[Ss][Ee][Oo]\b',
    }
    
    tag_lower = [t.lower() for t in tags]
    slug_lower = slug.lower()
    title_lower = title.lower()
    
    # Helper to check if any tag contains a substring
    def any_tag_contains(*substrings):
        return any(any(sub in t for sub in substrings) for t in tag_lower)
    
    if any_tag_contains('gbp', 'google maps', 'local seo'):
        entities_to_check['Google Business Profile'] = r'Google\s*(Business\s*Profile|My\s*Business|GBP|Maps)'
    
    if any_tag_contains('garment', 'textile', 'b2b', 'rmg'):
        entities_to_check['Garments/Textile'] = r'\b(garment|textile|rmg)\b'
    
    if any_tag_contains('healthcare', 'medical', 'clinic', 'patient'):
        entities_to_check['Medical/Healthcare'] = r'\b(healthcare|medical|clinic|doctor|patient|hospital)\b'
    
    if any_tag_contains('mobile') or 'mobile-seo' in slug_lower or 'mobile-first' in title_lower:
        entities_to_check['Mobile'] = r'\b(mobile|smartphone)\b'
    
    if any_tag_contains('geo', 'ai search', 'generative', 'ai') or 'geo' in slug_lower or 'ai' in slug_lower:
        entities_to_check['GEO/AI Search'] = r'\b(GEO|Generative Engine|AI\s*search|ChatGPT|Gemini|Perplexity)\b'
    
    if any_tag_contains('e-commerce', 'ecommerce', 'daraz', 'shopify'):
        entities_to_check['E-commerce'] = r'\b(e[\s-]?commerce|online\s*store|shop|product|daraz|shopify)\b'
    
    if any_tag_contains('mobile seo', 'mobile-first'):
        entities_to_check['Mobile-First'] = r'\b(mobile[\s-]?first|responsive|mobile[\s-]?friendly)\b'
    
    # Case studies
    case_study_keywords = ('case-study', 'locksmith', 'dundee', 'landlord', 'taxis', 
                           'morethanpanel', 'smmgen', 'smmsun', 'mir-cement', 
                           'dhaka-apparels', 'stealth', 'windshield')
    if any(kw in slug_lower for kw in case_study_keywords):
        entities_to_check['Results/ROI'] = r'\b(increase|growth|traffic|result|revenue|rank|organic|monthly)\b'
    
    results = {}
    for entity_name, pattern in entities_to_check.items():
        found = bool(re.search(pattern, content, re.IGNORECASE))
        results[entity_name] = found
    
    return results


def count_question_headings(content):
    q_pattern = '|'.join(re.escape(w) for w in QUESTION_WORDS)
    pattern = re.compile(
        r'^#{1,6}\s+(?:' + q_pattern + r')\b',
        re.MULTILINE | re.IGNORECASE
    )
    return len(pattern.findall(content))


def count_internal_links(content):
    md_links = re.findall(
        r'\[([^\]]*)\]\((/blog/[^)]*|/services/[^)]*|/industries/[^)]*|/locations/[^)]*)\)',
        content
    )
    # Also count bare mentions (like [/blog/something])
    bare_links = re.findall(
        r'(?<!\()(?:/blog/|/services/|/industries/|/locations/)[a-zA-Z0-9_-]+',
        content
    )
    all_links = set()
    for text, path in md_links:
        all_links.add(path)
    for link in bare_links:
        all_links.add(link)
    # Filter out matches that are substrings of markdown links already counted
    # Also filter out empty/too-short links
    valid_links = {l for l in all_links if len(l) > 10}
    return len(valid_links), valid_links


def check_pillar_links(content, pillar, tags):
    pillar_pages = {
        "AI/GEO": ["/services/geo-ai-search", "/blog/geo-optimization-prepare-business-ai-search"],
        "Case Studies": ["/blog/seo-case-study-dhaka-businesses-increased-organic-traffic", "/services/seo-case-studies"],
        "Local SEO": ["/services/local-seo", "/blog/local-seo-tips-dhaka-businesses-google-maps"],
        "E-commerce SEO": ["/services/ecommerce-seo", "/blog/why-ecommerce-store-needs-seo-bangladesh"],
        "Industry SEO": ["/services", "/industries/"],
        "Mobile SEO": ["/blog/mobile-seo-optimization-bangladesh-mobile-first-era", "/services/mobile-seo"],
        "Technical SEO": ["/blog/technical-seo-checklist-bangladeshi-websites"],
        "Link Building": ["/services/link-building", "/blog/link-building-strategies-bangladesh-market"],
        "Content Marketing": ["/blog/content-marketing-strategy-bangladeshi-brands-seo"],
        "SEO": ["/blog/complete-seo-guide-bangladesh-businesses-2026", "/services"],
        "General": ["/blog", "/"],
    }
    
    pages = pillar_pages.get(pillar, ["/blog/"])
    
    linked = []
    for page in pages:
        if page in content:
            linked.append(page)
    
    return linked, pages


def check_schema_fields(post):
    missing = []
    if not post.get('title'):
        missing.append('title')
    if not post.get('excerpt'):
        missing.append('excerpt')
    if not post.get('date'):
        missing.append('date')
    return missing


def extract_string_field(text, field_name):
    """Extract a simple string field: field_name: "value" or field_name:\n  "value" """
    # Try single-line first
    m = re.search(rf'{re.escape(field_name)}:\s*"((?:[^"\\]|\\.)*)"', text)
    if m:
        return m.group(1)
    return ''


def extract_tags(text):
    """Extract tags array."""
    m = re.search(r'tags:\s*\[([^\]]*)\]', text)
    if m:
        tag_str = m.group(1)
        return re.findall(r'"([^"]*)"', tag_str)
    return []


def parse_posts(filepath):
    """Parse data.js and extract posts as dicts."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Build a map of slug -> position in file
    posts = []
    
    # Strategy: find each post by locating its slug, then extract the post object
    # by finding the preceding '{' (start of object, after '},' separator)
    # and the following closing of object + content backtick
    
    for slug in MODIFIED_SLUGS:
        # Find the slug definition
        slug_pattern = r'slug:\s*"' + re.escape(slug) + r'"'
        slug_match = re.search(slug_pattern, content)
        if not slug_match:
            print(f"  WARNING: Slug not found: {slug}")
            continue
        
        slug_pos = slug_match.start()
        
        # Find post start: go backwards past the post header fields to the opening '{'
        # Look for the pattern '  },\n  {' or '\n  {' that's before the slug
        pre_content = content[:slug_pos]
        
        # Find the last occurrence of '  {\n' or '{\n' before slug
        # But we need to make sure it's not inside a template literal
        # Find all '{' positions before slug
        brace_positions = [m.start() for m in re.finditer(r'(?<!\w)\{', pre_content)]
        
        if not brace_positions:
            print(f"  WARNING: Could not find post start for: {slug}")
            continue
        
        # The post start is the last '{' before the slug that has a preceding newline
        # post start pattern: newline, spaces, {
        post_start_candidates = list(re.finditer(r'\n\s*\{', pre_content))
        if not post_start_candidates:
            print(f"  WARNING: Could not find post start pattern for: {slug}")
            continue
        
        post_start_match = post_start_candidates[-1]
        post_start = post_start_match.start() + 1  # +1 to skip the newline
        
        # Find post end: after the slug, we need to find the end of the post
        # The post ends at '`,\n  },' or '`\n  },' or '`\n  }];'
        # Need to handle the second-to-last and last posts differently
        post_text = content[post_start:]
        
        # Find the content's closing backtick
        # First find "content: `" opening
        content_open = re.search(r'content:\s*`', post_text)
        if not content_open:
            print(f"  WARNING: No content field for: {slug}")
            continue
        
        content_start = content_open.end()
        remaining = post_text[content_start:]
        
        # Find the closing backtick that's followed by comma or newline + }
        # The closing backtick could be just `, or ` // comment,
        end_match = re.search(r'`\s*(?://[^\n]*)?,?\s*\n\s*\}', remaining)
        if end_match:
            content_end = content_start + end_match.start()
        else:
            # Try just closing backtick
            end_match2 = re.search(r'`', remaining)
            if end_match2:
                content_end = content_start + end_match2.start()
            else:
                print(f"  WARNING: No closing backtick for: {slug}")
                continue
        
        # Extract the full post text from post_start to post_end
        post_full_text = post_text[:content_end + len('`')]
        
        # Extract the content
        raw_content = post_text[content_start:content_end]
        
        # Remove content prefix
        extracted = {
            'slug': slug,
            'title': extract_string_field(post_full_text, 'title'),
            'date': extract_string_field(post_full_text, 'date'),
            'excerpt': extract_string_field(post_full_text, 'excerpt'),
            'tags': extract_tags(post_full_text),
            'content': raw_content,
        }
        
        posts.append(extracted)
        print(f"  Parsed: {slug} - title: {extracted['title'][:50] if extracted['title'] else 'MISSING'}... | content length: {len(raw_content)}")
    
    return posts


def main():
    filepath = '/root/kanok-miahit/src/app/blog/data.js'
    
    print("=" * 60)
    print("PARSING DATA.JS (v2)")
    print("=" * 60)
    posts = parse_posts(filepath)
    
    print(f"\nParsed {len(posts)} posts from modified slugs list.")
    
    if len(posts) < 21:
        print(f"WARNING: Expected 21 posts, found {len(posts)}")
        found_slugs = {p['slug'] for p in posts}
        for s in MODIFIED_SLUGS:
            if s not in found_slugs:
                print(f"  MISSING: {s}")
    
    today = date.today().isoformat()
    report_path = f'/root/kanok-miahit/framework-enforcement-report-{today}.md'
    
    with open(report_path, 'w', encoding='utf-8') as report:
        report.write(f"# Content Framework Enforcement Report\n\n")
        report.write(f"**Date:** {today}\n")
        report.write(f"**Posts Analyzed:** {len(posts)} of {len(MODIFIED_SLUGS)} modified blog posts\n\n")
        
        # Summary table
        report.write("## Summary Table\n\n")
        report.write("| # | Slug | A: TF-IDF | B: Entities | C: Pillar Links | D: Q-Headings | E: Internal Links | F: Schema | Status |\n")
        report.write("|---|------|-----------|-------------|-----------------|---------------|-------------------|-----------|--------|\n")
        
        overall_passes = 0
        overall_fails = 0
        
        detail_items = []
        
        for idx, post in enumerate(posts):
            slug = post['slug']
            title = post['title']
            content = post['content']
            tags = post['tags']
            date_val = post.get('date', '')
            excerpt = post.get('excerpt', '')
            
            # A. TF-IDF Coverage
            keyword = extract_keyword(title)
            keyword_count = count_keyword_occurrences(keyword, content)
            a_flag = keyword_count < 5
            a_detail = f"Keyword: '{keyword}' → {keyword_count} occurrences {'❌' if a_flag else '✅'}"
            
            # B. Semantic Entity Coverage
            entity_results = check_entities(content, tags, slug, title)
            missing_entities = [name for name, found in entity_results.items() if not found]
            b_flag = len(missing_entities) > 0
            b_detail = f"Entities checked: {len(entity_results)} | Missing: {', '.join(missing_entities) if missing_entities else 'None'}{' ❌' if b_flag else ' ✅'}"
            
            # C. Pillar-Cluster Alignment
            pillar = determine_pillar(tags)
            linked_pages, expected_pages = check_pillar_links(content, pillar, tags)
            c_flag = len(linked_pages) == 0
            c_detail = f"Pillar: {pillar} | Expected: {expected_pages} | Found links: {linked_pages if linked_pages else 'None'} {'❌' if c_flag else '✅'}"
            
            # D. AEO/GEO Optimization
            q_count = count_question_headings(content)
            d_flag = q_count < 2
            d_detail = f"Question headings found: {q_count} {'❌' if d_flag else '✅'}"
            
            # E. Internal Linking
            link_count, links = count_internal_links(content)
            e_flag = link_count < 3
            e_detail = f"Internal links: {link_count} (to /blog/, /services/, /industries/, /locations/) {'❌' if e_flag else '✅'}"
            
            # F. Schema
            schema_missing = check_schema_fields(post)
            f_flag = len(schema_missing) > 0
            f_detail = f"Schema fields: title={'✅' if post['title'] else '❌'}, excerpt={'✅' if post['excerpt'] else '❌'}, date={'✅' if post['date'] else '❌'}"
            
            total_flags = sum([a_flag, b_flag, c_flag, d_flag, e_flag, f_flag])
            passes = 6 - total_flags
            overall_passes += passes
            overall_fails += total_flags
            
            if total_flags == 0:
                status = "✅ PASS"
            elif total_flags <= 2:
                status = "⚠️  WARN"
            else:
                status = "❌ FAIL"
            
            a_sym = '❌' if a_flag else '✅'
            b_sym = '❌' if b_flag else '✅'
            c_sym = '❌' if c_flag else '✅'
            d_sym = '❌' if d_flag else '✅'
            e_sym = '❌' if e_flag else '✅'
            f_sym = '❌' if f_flag else '✅'
            
            short_slug = slug[:45] + '...' if len(slug) > 45 else slug
            report.write(f"| {idx+1} | {short_slug} | {a_sym} | {b_sym} | {c_sym} | {d_sym} | {e_sym} | {f_sym} | {status} |\n")
            
            detail_items.append((slug, title, date_val, tags, excerpt, pillar, keyword, keyword_count, a_detail, a_flag, entity_results, missing_entities, b_flag, c_detail, linked_pages, expected_pages, c_flag, d_detail, q_count, d_flag, e_detail, link_count, links, e_flag, f_detail, schema_missing, f_flag, total_flags))
        
        report.write(f"\n**Totals:** {overall_passes}/{len(posts)*6} checks passed ({overall_fails} flags)\n\n")
        report.write("---\n\n")
        
        for (slug, title, date_val, tags, excerpt, pillar, keyword, keyword_count, a_detail, a_flag, entity_results, missing_entities, b_flag, c_detail, linked_pages, expected_pages, c_flag_val, d_detail, q_count, d_flag_val, e_detail, link_count, links, e_flag_val, f_detail, schema_missing, f_flag_val, total_flags) in detail_items:
            report.write(f"## {slug}\n\n")
            report.write(f"**Title:** {title}\n\n")
            report.write(f"**Date:** {date_val}\n\n")
            report.write(f"**Tags:** {', '.join(tags)}\n\n")
            report.write(f"**Pillar:** {pillar}\n\n")
            report.write(f"**Excerpt:** {excerpt[:120]}...\n\n")
            
            report.write("### A. TF-IDF Coverage\n\n")
            report.write(f"- {a_detail}\n")
            if a_flag:
                report.write(f"- ⚠️ **FLAG:** Under 5 occurrences — needs more keyword usage\n")
            else:
                report.write(f"- ✅ Adequate keyword coverage\n\n")
            
            report.write("### B. Semantic Entity Coverage\n\n")
            report.write(f"- {b_detail}\n")
            for entity_name, found in entity_results.items():
                report.write(f"  - {entity_name}: {'✅' if found else '❌ MISSING'}\n")
            if b_flag:
                report.write(f"- ⚠️ **FLAG:** Missing entities: {', '.join(missing_entities)}\n")
            else:
                report.write(f"- ✅ All key entities present\n")
            report.write("\n")
            
            report.write("### C. Pillar-Cluster Alignment\n\n")
            report.write(f"- Pillar topic: **{pillar}**\n")
            report.write(f"- Expected pillar pages: {expected_pages}\n")
            if linked_pages:
                report.write(f"- ✅ Linked to pillar: {linked_pages}\n")
            else:
                report.write(f"- ❌ **FLAG:** No links to pillar page found\n")
            report.write("\n")
            
            report.write("### D. AEO/GEO Optimization\n\n")
            report.write(f"- {d_detail}\n")
            if d_flag_val:
                report.write(f"- ⚠️ **FLAG:** Less than 2 question-based headings (need more How/What/Why style headings)\n")
            else:
                report.write(f"- ✅ Adequate question-based headings\n")
            report.write("\n")
            
            report.write("### E. Internal Linking\n\n")
            report.write(f"- {e_detail}\n")
            if link_count > 0:
                links_sorted = sorted(links)
                links_str = ', '.join(links_sorted[:15])
                if len(links_sorted) > 15:
                    links_str += f', ... (+{len(links_sorted)-15} more)'
                report.write(f"- Links found: {links_str}\n")
            if e_flag_val:
                report.write(f"- ⚠️ **FLAG:** Less than 3 internal links\n")
            else:
                report.write(f"- ✅ 3+ internal links found\n")
            report.write("\n")
            
            report.write("### F. Schema Readiness (ArticleSchema)\n\n")
            report.write(f"- {f_detail}\n")
            if f_flag_val:
                report.write(f"- ⚠️ **FLAG:** Missing fields: {', '.join(schema_missing)}\n")
            else:
                report.write(f"- ✅ All required schema fields present\n")
            report.write("\n")
            
            report.write(f"**Total Flags: {total_flags}/6** | ")
            if total_flags == 0:
                report.write("✅ PASS\n\n"
                )
            elif total_flags <= 2:
                report.write("⚠️  WARN\n\n")
            else:
                report.write("❌ FAIL\n\n")
            
            report.write("---\n\n")
        
        report.write("## Methodology\n\n")
        report.write("### A. TF-IDF Coverage\n")
        report.write("Keyword extracted from title. Counted case-insensitive occurrences (phrase + individual words) in content. Flagged if < 5.\n\n")
        report.write("### B. Semantic Entity Coverage\n")
        report.write("Key entities checked based on topic: Dhaka, Bangladesh, SEO, plus industry-specific terms. Flagged if any missing.\n\n")
        report.write("### C. Pillar-Cluster Alignment\n")
        report.write("Pillar topic determined from tags. Post checked for links to relevant pillar page.\n\n")
        report.write("### D. AEO/GEO Optimization\n")
        report.write("Headings starting with How, What, Why, When, Where, Can, Do, Is, Are counted. Flagged if < 2.\n\n")
        report.write("### E. Internal Linking\n")
        report.write("Markdown links to /blog/, /services/, /industries/, /locations/ counted (unique paths). Flagged if < 3.\n\n")
        report.write("### F. Schema Readiness\n")
        report.write("Post checked for title, excerpt, date fields needed for ArticleSchema. Flagged if any missing.\n\n")
    
    print(f"\nReport written to {report_path}")
    
    print(f"\n{'='*60}")
    print(f"SUMMARY")
    print(f"{'='*60}")
    print(f"Total posts: {len(posts)}")
    print(f"Total checks: {len(posts)*6}")
    print(f"Passed: {overall_passes}")
    print(f"Flagged: {overall_fails}")
    
    # Print individual results
    print(f"\n{'='*60}")
    print(f"DETAILED RESULTS")
    print(f"{'='*60}")
    for idx, post in enumerate(posts):
        slug = post['slug']
        keyword = extract_keyword(post['title'])
        kw_count = count_keyword_occurrences(keyword, post['content'])
        qc = count_question_headings(post['content'])
        lc, _ = count_internal_links(post['content'])
        pillar = determine_pillar(post['tags'])
        er = check_entities(post['content'], post['tags'], slug, post['title'])
        missing = [n for n, f in er.items() if not f]
        linked, _ = check_pillar_links(post['content'], pillar, post['tags'])
        schema_m = check_schema_fields(post)
        
        flags = sum([1 if kw_count < 5 else 0, 1 if missing else 0, 1 if not linked else 0, 1 if qc < 2 else 0, 1 if lc < 3 else 0, 1 if schema_m else 0])
        
        print(f"\n{idx+1}. {slug}")
        print(f"   Title: {post['title'][:60]}")
        print(f"   A: keyword='{keyword}' -> {kw_count} {'❌' if kw_count < 5 else '✅'}")
        print(f"   B: entities={len(er)}, missing={missing} {'❌' if missing else '✅'}")
        print(f"   C: pillar={pillar}, linked={linked} {'❌' if not linked else '✅'}")
        print(f"   D: q-headings={qc} {'❌' if qc < 2 else '✅'}")
        print(f"   E: internal-links={lc} {'❌' if lc < 3 else '✅'}")
        print(f"   F: schema={schema_m} {'❌' if schema_m else '✅'}")
        print(f"   Flags: {flags}/6")


if __name__ == '__main__':
    main()
