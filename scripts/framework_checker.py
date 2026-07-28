#!/usr/bin/env python3
"""
Content Framework Enforcer for kanokmiah.com.bd
Checks blog posts against defined content framework standards.
"""
import re
import sys

# Slugs modified in the last 48 hours (from git log)
MODIFIED_SLUGS = [
    "geo-optimization-prepare-business-ai-search",
    "seo-garments-textile-industry-b2b-lead-generation",
    "mobile-seo-optimization-bangladesh-mobile-first-era",
    "seo-healthcare-medical-clinics-bangladesh",
    "locksmith-dundee-seo-case-study",
    "das-taxis-scotland-seo-case-study",
    "morethanpanel-seo-case-study",
    "smmgen-seo-case-study",
    "smmsun-seo-case-study",
    "mir-cement-seo-case-study",
    "dhaka-apparels-seo-case-study",
    "stealth-windshield-repairs-seo-case-study",
    "how-to-choose-right-seo-agency-bangladesh",
    "seo-expert-vs-seo-agency-dhaka-which-is-right",
    "top-10-seo-mistakes-dhaka-businesses-fix",
    "seo-tips-for-business-owners-bd",
    "seo-case-study-dhaka-businesses-increased-organic-traffic",
    "hiring-seo-expert-dhaka-better-roi-than-paid-ads",
    "seo-trends-2026-ai-geo-future",
    "watchzonebd-seo-case-study",
]

def parse_posts(filepath):
    """Parse blog posts from data.js file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all post objects using regex
    # Each post starts with `{` (after comment/previous post) and has slug, title, date, etc.
    # We'll find them by splitting on slug patterns
    posts = []
    
    # Find each post block using slug as anchor
    pattern = r'{\s*\n\s+slug:\s*"([^"]+)"'
    matches = list(re.finditer(pattern, content))
    
    for i, match in enumerate(matches):
        slug = match.group(1)
        start = match.start()
        # End: either before the next slug, or end of file
        if i + 1 < len(matches):
            end = matches[i + 1].start()
        else:
            end = len(content)
        
        post_text = content[start:end]
        
        # Extract title
        title_match = re.search(r'title:\s*"([^"]+)"', post_text)
        title = title_match.group(1) if title_match else ""
        
        # Extract date
        date_match = re.search(r'date:\s*"([^"]+)"', post_text)
        date = date_match.group(1) if date_match else ""
        
        # Extract excerpt
        excerpt_match = re.search(r'excerpt:\s*"([^"]+)"', post_text)
        excerpt = excerpt_match.group(1) if excerpt_match else ""
        
        # Extract tags
        tags_match = re.search(r'tags:\s*\[([^\]]+)\]', post_text)
        tags = []
        if tags_match:
            tags_raw = tags_match.group(1)
            tags = re.findall(r'"([^"]+)"', tags_raw)
        
        # Extract content (the text inside backticks after "content: `")
        content_match = re.search(r'content:\s*`([\s\S]*?)`\s*,?\s*\}', post_text)
        post_content = content_match.group(1) if content_match else ""
        
        posts.append({
            'slug': slug,
            'title': title,
            'date': date,
            'excerpt': excerpt,
            'tags': tags,
            'content': post_content,
            'raw': post_text,
        })
    
    return posts


def check_tfidf(post):
    """Check TF-IDF keyword coverage."""
    title = post['title']
    content = post['content']
    
    # Strategy: generate candidate keywords from title and pick the best one
    clean_title = re.sub(r'\s*\|.*$', '', title).strip()
    # Remove "SEO Case Study:" / "How to" / "Why" type prefixes for cleaner extraction
    title_core = re.sub(r'^(SEO|How|What|Why|When|Where)\s+', '', clean_title)
    
    # Generate keyword candidates (ordered from most specific to most general)
    candidates = []
    
    words = clean_title.split()
    # Clean words (strip punctuation from individual words)
    clean_words = [w.strip(':;,."\'!?—–-') for w in words]
    
    # 1. Full title (first 4 words max, no trailing punctuation)
    if len(clean_words) >= 2:
        candidate = ' '.join(clean_words[:min(4, len(clean_words))]).strip()
        if candidate:
            candidates.append(candidate)
    
    # 2. After colon/slash — this is often the most descriptive part
    if ':' in clean_title:
        after_colon = clean_title.split(':')[-1].strip()
        if after_colon:
            words2 = after_colon.split()
            if len(words2) >= 2:
                candidates.append(' '.join(words2[:4]))
            candidates.append(after_colon)
    if '—' in clean_title:
        after_dash = clean_title.split('—')[-1].strip()
        if after_dash:
            candidates.append(after_dash)
    
    # 2b. First 2 cleaned words (best for titles like "GEO Optimization: ...")
    if len(clean_words) >= 2:
        two_word = ' '.join(clean_words[:2])
        if two_word not in candidates:
            candidates.append(two_word)
    if len(clean_words) >= 3:
        three_word = ' '.join(clean_words[:3])
        if three_word not in candidates:
            candidates.append(three_word)
    
    # 3. First 2 significant words (skip common stop words)
    stop_words = {'the', 'a', 'an', 'for', 'in', 'of', 'to', 'and', 'is', 'vs', 'or', 'your', 'our', 'their', 'how', 'what', 'why', 'when', 'where', 'top'}
    sig_words = [w for w in clean_words if w.lower() not in stop_words and w not in [':', '—', '-', '']]
    if len(sig_words) >= 2:
        candidates.append(' '.join(sig_words[:2]))
    if len(sig_words) >= 3:
        candidates.append(' '.join(sig_words[:3]))
    
    # 4. Remove common suffixes
    for suffix in [' SEO', ' SEO Case', ' Case Study', ' Guide', ' Tips', ' Strategy']:
        for c in candidates[:]:
            if c.endswith(suffix):
                candidates.append(c[:-len(suffix)])
    
    # 5. For case studies, try the company/brand name (first 1-2 words)
    if 'case study' in title.lower() or 'case-study' in post['slug']:
        # Company name is often the first 1-3 words
        company = ' '.join(words[:min(3, len(words))]).rstrip(':,').rstrip(' SEO').rstrip(' Case')
        candidates.append(company)
        # Also slug-derived name
        slug_parts = post['slug'].replace('-seo-case-study', '').replace('-case-study', '').split('-')
        slug_name = ' '.join([p.capitalize() for p in slug_parts if p not in ['seo', 'case', 'study']])
        if slug_name and slug_name not in candidates:
            candidates.append(slug_name)
    
    # 6. For "How to / What is / Why" titles, try the key noun phrase after the verb
    how_to_match = re.match(r'^(How\s+to|What\s+(Is|Are)|Why\s+(Do|Does|Is|Are|Should)|When\s+(Do|Does|Is)|Where\s+(Do|Is)|Can\s+|Does\s+|Is\s+|Are\s+|Top\s+\d+)', clean_title, re.IGNORECASE)
    if how_to_match:
        after_instruction = clean_title[how_to_match.end():].strip().lstrip(':').strip()
        if after_instruction:
            after_words = after_instruction.split()
            if len(after_words) >= 2:
                candidates.append(' '.join(after_words[:2]))
                candidates.append(' '.join(after_words[:3]))
            candidates.append(after_instruction)
    
    # Deduplicate while preserving order
    seen = set()
    unique_candidates = []
    for c in candidates:
        c = c.strip()
        if c and c not in seen and len(c) > 3:
            seen.add(c)
            unique_candidates.append(c)
    
    # Find the best keyword - one with highest count that hits the target
    best_keyword = unique_candidates[0] if unique_candidates else clean_title[:20]
    best_count = 0
    
    for kw in unique_candidates:
        try:
            count = len(re.findall(re.escape(kw), content, re.IGNORECASE))
        except:
            continue
        if count >= 5:
            best_keyword = kw
            best_count = count
            break
        if count > best_count:
            best_count = count
            best_keyword = kw
    
    # Final fallback: just use the core subject
    if best_count < 5 and sig_words:
        core = ' '.join(sig_words[:2])
        if core != best_keyword and len(core) > 3:
            try:
                count = len(re.findall(re.escape(core), content, re.IGNORECASE))
            except:
                count = 0
            if count > best_count:
                best_keyword = core
                best_count = count
    
    passed = best_count >= 5
    return {
        'keyword': best_keyword,
        'count': best_count,
        'passed': passed,
    }


def check_entities(post):
    """Check semantic entity coverage."""
    title = post['title']
    content = post['content']
    slug = post['slug']
    
    # Core entities that MUST be present (location-based)
    entities_to_check = {}
    
    # Check for location mentions (Bangladesh if relevant)
    title_lower = title.lower()
    slug_lower = slug.lower()
    has_bangladesh_context = any(term in title_lower or term in slug_lower 
                                  for term in ['bangladesh', 'dhaka', 'chittagong', 'sylhet', 'bd', 'bengali', 'বাংলাদেশ'])
    
    if has_bangladesh_context:
        entities_to_check['location_bangladesh'] = ('Bangladesh', ['Bangladesh'])
    
    # Dhaka entity if locally relevant
    if any(term in title_lower or term in slug_lower for term in ['dhaka', 'local']):
        entities_to_check['location_dhaka'] = ('Dhaka', ['Dhaka'])
    
    # Determine service type from title/slug/tags (word-boundary matching)
    service_types = [
        ('seo', 'SEO'),
        ('geo', 'GEO'),
        ('ai search', 'AI Search'),
        ('local seo', 'Local SEO'),
        ('healthcare', 'Healthcare'),
        ('medical', 'Medical'),
        ('mobile seo', 'Mobile SEO'),
        ('mobile optimization', 'Mobile Optimization'),
        ('content marketing', 'Content Marketing'),
        ('garments', 'Garments'),
        ('textile', 'Textile'),
        ('b2b seo', 'B2B SEO'),
        ('ecommerce seo', 'E-commerce SEO'),
        ('e-commerce seo', 'E-commerce SEO'),
        ('technical seo', 'Technical SEO'),
    ]
    
    for term, label in service_types:
        # Use word boundary matching to avoid false positives
        if re.search(r'\b' + re.escape(term) + r'\b', title_lower) or re.search(r'\b' + re.escape(term) + r'\b', slug_lower):
            entities_to_check[f'service_{term.replace(" ", "_")}'] = (label, [label])
    
    content_lower = content.lower()
    
    # Industry from tags (only show meaningful single-concept tags)
    meaningful_tags = [t for t in post['tags'] 
                       if t.lower() not in ['seo', 'bangladesh', 'digital marketing', 'case study', 
                                            'local seo', 'technical seo', 'b2b seo', 'mobile seo',
                                            'growth strategy', 'agency selection', 'hire seo',
                                            'seo roi', 'seo vs ads', 'organic traffic', 'seo case study']]
    
    for tag in meaningful_tags:
        # Only check short/medium-length tags (likely a single concept that should appear)
        # Skip long multi-word tags that are just category descriptors
        if len(tag) > 25:
            continue
        # Skip if this tag looks like a descriptive phrase
        if tag.lower() in [t.lower() for t in ['Dhaka SEO', 'SEO Tips Bangladesh', 'SEO Expert Dhaka', 
                                                'SEO Agency Dhaka', 'SEO Services Bangladesh',
                                                'SEO Results Bangladesh', 'Bangladesh RMG',
                                                'Garments SEO', 'Mobile-First Indexing',
                                                'Mobile Optimization', 'SEO Trends 2026',
                                                'SEO Mistakes']]:
            continue
        # Check if the tag isn't already covered by another entity
        tag_key = tag.lower().replace(' ', '_').replace('-', '_')
        if tag not in [v[0] for v in entities_to_check.values()]:
            # Use word-boundary matching for the tag
            tag_words = tag.split()
            if len(tag_words) <= 2:  # Only require single or two-word tags
                found = False
                for word in tag_words:
                    if re.search(r'\b' + re.escape(word) + r'\b', content_lower, re.IGNORECASE):
                        found = True
                        break
                if not found:
                    entities_to_check[f'tag_{tag_key}'] = (tag, tag_words)
    
    # For case studies, also check company name
    if 'case-study' in slug:
        slug_parts = slug.replace('-seo-case-study', '').replace('-case-study', '').split('-')
        # Only treat as company name if short (2-3 words max), not a descriptive sentence
        company_parts = [p.capitalize() for p in slug_parts if p not in ['seo', 'case', 'study']]
        if 1 <= len(company_parts) <= 3:
            company = ' '.join(company_parts)
            if company and len(company) > 3:
                entities_to_check['company'] = (company, [company])
    
    results = {}
    missing = []
    for key, (label, terms) in entities_to_check.items():
        found = False
        for term in terms:
            if term.lower() in content_lower:
                found = True
                break
        results[key] = {'label': label, 'found': found}
        if not found:
            missing.append(label)
    
    all_passed = len(missing) == 0
    return {
        'missing': missing,
        'passed': all_passed,
    }


def check_pillar_cluster(post):
    """Check pillar-cluster alignment."""
    tags = post['tags']
    content = post['content']
    slug = post['slug']
    title = post['title']
    
    # Pillar pages and their cluster topics
    pillar_map = {
        'complete-seo-guide-bangladesh-businesses-2026': ['SEO', 'SEO Guide', 'Complete SEO'],
        'geo-optimization-prepare-business-ai-search': ['GEO', 'AI Search', 'Generative Engine'],
        'local-seo-tips-dhaka-businesses-google-maps': ['Local SEO', 'Google Maps', 'Local Search'],
        'technical-seo-checklist-bangladeshi-websites': ['Technical SEO', 'Core Web Vitals', 'Site Speed'],
        'why-ecommerce-store-needs-seo-bangladesh': ['E-commerce SEO', 'Online Store'],
        'seo-trends-2026-ai-geo-future': ['SEO Trends', 'AI', 'GEO'],
        'seo-healthcare-medical-clinics-bangladesh': ['Healthcare SEO', 'Medical'],
        'mobile-seo-optimization-bangladesh-mobile-first-era': ['Mobile SEO'],
        'seo-garments-textile-industry-b2b-lead-generation': ['Garments', 'Textile', 'B2B SEO'],
        'content-marketing-strategy-bangladeshi-brands-seo': ['Content Marketing'],
    }
    
    # Determine which pillar this post belongs to
    matched_pillar = None
    for pillar_slug, pillar_tags in pillar_map.items():
        for pt in pillar_tags:
            pt_lower = pt.lower()
            for tag in tags:
                if pt_lower in tag.lower():
                    matched_pillar = (pillar_slug, pt)
                    break
            if matched_pillar:
                break
        if matched_pillar:
            break
    
    # If no match by tags, try title
    if not matched_pillar:
        for pillar_slug, pillar_tags in pillar_map.items():
            for pt in pillar_tags:
                if pt.lower() in title.lower():
                    matched_pillar = (pillar_slug, pt)
                    break
            if matched_pillar:
                break
    
    # Check if the post links to its pillar page
    links_to_pillar = False
    pillar_linked = ""
    if matched_pillar:
        pillar_slug, pillar_tag = matched_pillar
        # If this post IS the pillar page, no link needed
        if post['slug'] == pillar_slug:
            links_to_pillar = True
            pillar_linked = "(self - is pillar page)"
        else:
            pillar_path = f'/blog/{pillar_slug}'
            if pillar_path in content:
                links_to_pillar = True
                pillar_linked = f'/blog/{pillar_slug}'
    
    return {
        'matched_pillar': matched_pillar,
        'links_to_pillar': links_to_pillar,
        'pillar_linked': pillar_linked,
    }


def check_aeo_geo(post):
    """Check AEO/GEO optimization - question-based headings."""
    content = post['content']
    
    # Count question-based headings (## or ### starting with question words)
    question_heading_pattern = re.compile(
        r'^#{2,4}\s+(What|How|Why|When|Where|Can|Do|Is|Are|Does|Will|Should|Which|Who)\b',
        re.MULTILINE | re.IGNORECASE
    )
    matches = question_heading_pattern.findall(content)
    count = len(matches)
    
    # Also check for FAQ sections
    faq_section = re.search(r'##\s*Frequently Asked Questions', content, re.IGNORECASE)
    
    passed = count >= 2 or bool(faq_section)
    return {
        'question_heading_count': count,
        'has_faq': bool(faq_section),
        'passed': passed,
    }


def check_internal_links(post):
    """Count internal links in the post."""
    content = post['content']
    
    # Find all internal links (links starting with /)
    internal_link_pattern = re.compile(r'\[([^\]]+)\]\((/[^\)]+)\)')
    all_links = internal_link_pattern.findall(content)
    
    # Filter to relevant internal links (blog posts, services, locations)
    relevant_links = [(text, url) for text, url in all_links if url.startswith(('/blog/', '/services/', '/locations/', '/industries/', '/about', '/contact'))]
    
    count = len(relevant_links)
    passed = count >= 3
    return {
        'count': count,
        'passed': passed,
        'links': relevant_links,
    }


def check_schema(post):
    """Check if post has required fields for Article Schema."""
    has_title = bool(post['title'])
    has_excerpt = bool(post['excerpt'])
    has_date = bool(post['date'])
    
    missing = []
    if not has_title:
        missing.append('title')
    if not has_excerpt:
        missing.append('excerpt')
    if not has_date:
        missing.append('date')
    
    passed = len(missing) == 0
    return {
        'fields': {'title': has_title, 'excerpt': has_excerpt, 'date': has_date},
        'missing': missing,
        'passed': passed,
    }


def main():
    filepath = '/root/kanok-miahit/src/app/blog/data.js'
    print("=" * 72)
    print("📋 CONTENT FRAMEWORK ENFORCER REPORT")
    print(f"   Project: kanokmiah.com.bd")
    print(f"   Period: Last 48 hours")
    print(f"   Posts modified: {len(MODIFIED_SLUGS)}")
    print("=" * 72)
    
    posts = parse_posts(filepath)
    post_by_slug = {p['slug']: p for p in posts}
    
    overall_passed = True
    reports = []
    
    for slug in MODIFIED_SLUGS:
        post = post_by_slug.get(slug)
        if not post:
            reports.append(f"\n## Post: {slug}\n| Check | Status | Details |\n|-------|--------|---------|\n| **⚠️ NOT FOUND** | ❌ | Post not found in data.js |\n")
            continue
        
        print(f"\n🔍 Checking: {slug}")
        
        # A. TF-IDF
        tfidf = check_tfidf(post)
        
        # B. Entities
        entities = check_entities(post)
        
        # C. Pillar-cluster
        pillar = check_pillar_cluster(post)
        
        # D. AEO/GEO
        aeo = check_aeo_geo(post)
        
        # E. Internal links
        internal = check_internal_links(post)
        
        # F. Schema
        schema = check_schema(post)
        
        # Build report
        report_lines = [
            f"\n## Post: {slug}",
            f"**Title:** {post['title']}",
            f"**Tags:** {', '.join(post['tags'])}",
            f"",
            f"| Check | Status | Details |",
            f"|-------|--------|---------|",
        ]
        
        # TF-IDF line
        tfidf_status = "✅" if tfidf['passed'] else "❌"
        report_lines.append(f"| TF-IDF: `{tfidf['keyword']}` | {tfidf_status} | {tfidf['count']} occurrences {'✅ ≥ 5' if tfidf['passed'] else '❌ < 5'} |")
        if not tfidf['passed']:
            overall_passed = False
        
        # Entities line
        ent_status = "✅" if entities['passed'] else "❌"
        missing_str = ', '.join(entities['missing']) if entities['missing'] else 'None'
        report_lines.append(f"| Entities | {ent_status} | Missing: {missing_str} |")
        if not entities['passed']:
            overall_passed = False
        
        # Pillar line
        pillar_status = "✅" if pillar['links_to_pillar'] else "⚠️"
        if pillar['matched_pillar']:
            pillar_detail = f"Links to: {pillar['pillar_linked'] or 'NONE'}" if not pillar['links_to_pillar'] else f"✅ Links to: {pillar['pillar_linked']}"
            report_lines.append(f"| Pillar Link | {pillar_status} | {pillar_detail} |")
        else:
            report_lines.append(f"| Pillar Link | ⚠️ | No pillar match found for tags: {', '.join(post['tags'])} |")
        if not pillar['links_to_pillar']:
            overall_passed = False
        
        # AEO/GEO line
        aeo_status = "✅" if aeo['passed'] else "❌"
        report_lines.append(f"| AEO/GEO | {aeo_status} | {aeo['question_heading_count']} question headings{' + FAQ section' if aeo['has_faq'] else ''} |")
        if not aeo['passed']:
            overall_passed = False
        
        # Internal links line
        int_status = "✅" if internal['passed'] else "❌"
        report_lines.append(f"| Internal Links | {int_status} | {internal['count']} total relevant links |")
        if not internal['passed']:
            overall_passed = False
        
        # Schema line
        schema_status = "✅" if schema['passed'] else "❌"
        schema_detail = 'All fields set' if schema['passed'] else f"Missing: {', '.join(schema['missing'])}"
        report_lines.append(f"| Schema Ready | {schema_status} | {schema_detail} |")
        if not schema['passed']:
            overall_passed = False
        
        # Fix instructions
        fix_lines = ["", "### Fix instructions:"]
        any_fix = False
        
        if not tfidf['passed']:
            any_fix = True
            fix_lines.append(f"- **TF-IDF**: Add more occurrences of \"{tfidf['keyword']}\" in content (currently {tfidf['count']}, need ≥ 5)")
        
        if not entities['passed']:
            any_fix = True
            fix_lines.append(f"- **Entities**: Add missing entities: {', '.join(entities['missing'])}")
        
        if not pillar['links_to_pillar']:
            any_fix = True
            if pillar['matched_pillar']:
                fix_lines.append(f"- **Pillar Link**: Add a link to pillar page `/blog/{pillar['matched_pillar'][0]}` (related to: {pillar['matched_pillar'][1]})")
            else:
                fix_lines.append(f"- **Pillar Link**: Could not determine pillar topic. Add a link to the appropriate pillar page.")
        
        if not aeo['passed']:
            any_fix = True
            fix_lines.append(f"- **AEO/GEO**: Add more question-answering headings (currently {aeo['question_heading_count']}, need ≥ 2)")
        
        if not internal['passed']:
            any_fix = True
            fix_lines.append(f"- **Internal Links**: Add more internal links to blog posts, services, or locations (currently {internal['count']}, need ≥ 3)")
        
        if not schema['passed']:
            any_fix = True
            fix_lines.append(f"- **Schema**: Set missing fields: {', '.join(schema['missing'])}")
        
        if not any_fix:
            fix_lines.append("✅ All checks passed — no fixes needed.")
        
        report_lines.extend(fix_lines)
        reports.append('\n'.join(report_lines))
    
    # Print summary
    summary_lines = [
        "\n" + "=" * 72,
        "📊 SUMMARY",
        "=" * 72,
        f"Total modified posts: {len(MODIFIED_SLUGS)}",
    ]
    
    for slug in MODIFIED_SLUGS:
        post = post_by_slug.get(slug)
        if not post:
            continue
        tfidf = check_tfidf(post)
        entities = check_entities(post)
        pillar = check_pillar_cluster(post)
        aeo = check_aeo_geo(post)
        internal = check_internal_links(post)
        schema = check_schema(post)
        
        pillar_ok = pillar['links_to_pillar'] if pillar['links_to_pillar'] is not None else False
        checks = [tfidf['passed'], entities['passed'], pillar_ok, aeo['passed'], internal['passed'], schema['passed']]
        passed_count = sum(checks)
        status = "✅" if passed_count == 6 else "⚠️" if passed_count >= 4 else "❌"
        summary_lines.append(f"  {status} {slug}: {passed_count}/6 checks passed")
    
    if overall_passed:
        summary_lines.append(f"\n✅ All posts pass all framework checks!")
    else:
        summary_lines.append(f"\n⚠️ Some posts need attention — see detailed reports above.")
    
    print('\n'.join(summary_lines))
    
    # Output full report
    print("\n\n" + "=" * 72)
    print("FULL DETAILED REPORT")
    print("=" * 72)
    for report in reports:
        print(report)


if __name__ == '__main__':
    main()
