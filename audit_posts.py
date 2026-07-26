#!/usr/bin/env python3
"""Content Framework Audit for Kanok Miah Blog Posts — Fixed Version."""

import re
import json

# The 35 slugs to audit
AUDIT_SLUGS = [
    "affiliate-seo-bangladesh",
    "content-marketing-strategy-bangladeshi-brands-seo",
    "das-taxis-scotland-seo-case-study",
    "google-business-profile-optimization-guide-bangladesh",
    "google-discover-seo-bangladesh",
    "hiring-seo-expert-dhaka-better-roi-than-paid-ads",
    "local-seo-dhaka-google-maps-ranking",
    "seo-bangla-blog-content-writing",
    "seo-branded-vs-non-branded-bd",
    "seo-breadcrumb-schema-bd",
    "seo-career-guide-bangladesh-2026",
    "seo-direct-traffic-bangladesh",
    "seo-expert-vs-seo-agency-dhaka-which-is-right",
    "seo-faq-schema-bangladesh",
    "seo-for-hotel-resort-bangladesh",
    "seo-for-new-website-bangladesh",
    "seo-for-ngo-bangladesh",
    "seo-for-restaurants-cafe-dhaka",
    "seo-for-youtube-channel-bangla",
    "seo-google-analytics-4-bangladesh",
    "seo-google-business-profile-posts",
    "seo-hreflang-guide-bangladesh",
    "seo-https-ssl-impact-bangladesh",
    "seo-legal-compliance-bangladesh",
    "seo-local-citations-bangladesh",
    "seo-pillar-content-strategy-bd",
    "seo-real-estate-developers-dhaka",
    "seo-referral-traffic-bangladesh",
    "seo-skyscraper-technique-bangladesh",
    "seo-trends-2026-ai-geo-future",
    "seo-vs-google-ads-bangladesh-business",
    "seo-vs-google-ads-whats-best-bangladesh-businesses",
    "stealth-windshield-repairs-seo-case-study",
    "technical-seo-checklist-bangladeshi-websites",
    "website-speed-optimization-bangladesh",
]

PILLAR_SLUG = "complete-seo-guide-bangladesh-businesses-2026"
PILLAR_URL = f"/blog/{PILLAR_SLUG}"


def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def parse_posts(text):
    """Parse all blog posts from the JS file using regex-based post extraction.
    Returns a dict of slug -> {field: value}
    """
    posts = {}
    slug_set = set(AUDIT_SLUGS)
    
    # Strategy: Split by post boundaries. Each post starts with `{` on its own line
    # followed by `slug: "..."`. We find each target slug and extract its post.
    
    # First, find all slug positions
    lines = text.split('\n')
    total = len(lines)
    
    slug_positions = {}  # slug -> line_number
    for i, line in enumerate(lines):
        m = re.match(r'\s*slug:\s*"([^"]+)"', line)
        if m:
            slug = m.group(1)
            if slug in slug_set:
                slug_positions[slug] = i
    
    print(f"Found {len(slug_positions)}/{len(AUDIT_SLUGS)} target slugs in file.")
    missing = [s for s in AUDIT_SLUGS if s not in slug_positions]
    if missing:
        print(f"WARNING: Slugs not found by regex: {missing}")
    
    for slug, slug_line in slug_positions.items():
        # Find the start of this post object (the `{` before the slug)
        start = slug_line
        while start > 0:
            if lines[start].strip() == '{':
                break
            start -= 1
        
        # Now find the content field by searching forward from the slug line
        content_start_line = None
        for j in range(slug_line, min(slug_line + 100, total)):
            if re.match(r'\s*content:\s*`', lines[j]):
                content_start_line = j
                break
        
        if content_start_line is None:
            print(f"  ERROR: No content field found for {slug}")
            continue
        
        # The content starts after the ` on the content_start_line
        # But the ` might be at the end of the line like: content: `text here`
        # Or on its own line like: content: `
        content_line_text = lines[content_start_line]
        # Find the position of the first backtick
        bt_pos = content_line_text.find('`')
        
        if bt_pos >= 0:
            after_bt = content_line_text[bt_pos+1:]
            # If there's actual content after the backtick on the same line, include it
            if after_bt.strip():
                # The content starts right after the ` on this line
                content_start_actual = content_start_line
                content_first_line = after_bt
            else:
                content_start_actual = content_start_line + 1
                content_first_line = None
        else:
            content_start_actual = content_start_line + 1
            content_first_line = None
        
        # Now find the closing backtick
        # The closing backtick can be:
        # 1. On its own line: ``
        # 2. At the end of a content line: `text here`
        # 3. At the end followed by comma: `text here`,
        content_end_line = None
        for j in range(content_start_actual, total):
            line = lines[j]
            # Look for a backtick followed by optional comma/paren at end of line
            # The pattern is: anything then ` then optionally , or ) then end of string
            # But the backtick could be inside the content text (unlikely in practice)
            # Actually in JS template literals, backticks are escaped, so we can look for
            # a backtick that's at the end of the line (possibly with trailing comma)
            
            # Check if this line contains a closing backtick
            # We need to find a backtick that is NOT inside a string inside the template literal
            # Since we can't really parse JS template literals perfectly, we look for
            # lines that end with `, `, `), or backtick alone, or have backtick at end
            
            stripped = line.strip()
            # Check for patterns: content`, content`,), `, `)
            # A backtick at the end of the line (possibly with comma/paren)
            if '`' in stripped:
                # Find the last backtick
                last_bt = stripped.rfind('`')
                after_last_bt = stripped[last_bt+1:].strip()
                if after_last_bt in ('', ',', ')', '),'):
                    content_end_line = j
                    break
        
        if content_end_line is None:
            print(f"  ERROR: Could not find closing backtick for {slug}")
            continue
        
        # Extract content
        if content_start_actual == content_end_line:
            content_str = content_first_line or ''
        elif content_start_actual == content_start_line:
            # Content started on the same line as `content: \``
            content_str = content_first_line or ''
            for j in range(content_start_actual + 1, content_end_line):
                content_str += '\n' + lines[j]
        else:
            content_lines_list = []
            for j in range(content_start_actual, content_end_line):
                content_lines_list.append(lines[j])
            content_str = '\n'.join(content_lines_list)
        
        # Remove the closing backtick from the last line
        if content_str and content_str[-1] == '`':
            content_str = content_str[:-1]
        
        # Extract header fields
        header_text = '\n'.join(lines[start:content_start_line])
        
        post = {'slug': slug}
        
        # Title
        m = re.search(r'title:\s*"((?:[^"\\]|\\.)*)"', header_text)
        if m:
            post['title'] = m.group(1)
        
        # Date
        m = re.search(r'date:\s*"(\d{4}-\d{2}-\d{2})"', header_text)
        if m:
            post['date'] = m.group(1)
        
        # Excerpt (can be multi-line string)
        excerpt_match = re.search(r'excerpt:\s*"((?:[^"\\]|\\.)*)"\s*(?:,|$)', header_text, re.DOTALL)
        if excerpt_match:
            post['excerpt'] = excerpt_match.group(1)
        else:
            # Try parsing multi-line excerpt
            excerpt_lines = []
            in_excerpt = False
            for hl in lines[start:content_start_line]:
                if re.match(r'\s*excerpt:\s', hl):
                    in_excerpt = True
                    val = hl.split('excerpt:')[1].strip()
                    if val.startswith('"'):
                        val = val[1:]
                    excerpt_lines.append(val)
                elif in_excerpt:
                    stripped = hl.strip()
                    if stripped.endswith('",'):
                        excerpt_lines.append(stripped[:-2])
                        break
                    elif stripped.endswith('",'):
                        excerpt_lines.append(stripped[:-2])
                        break
                    elif stripped.endswith('"'):
                        excerpt_lines.append(stripped[:-1])
                        break
                    else:
                        excerpt_lines.append(stripped)
            if excerpt_lines:
                post['excerpt'] = ' '.join(excerpt_lines).strip()
        
        # Tags
        tags_match = re.search(r'tags:\s*\[([^\]]+)\]', header_text, re.DOTALL)
        if tags_match:
            tags_str = tags_match.group(1)
            tags = re.findall(r'"([^"]*)"', tags_str)
            post['tags'] = tags
        else:
            post['tags'] = []
        
        post['content'] = content_str
        posts[slug] = post
        print(f"  Parsed: {slug} (content: ~{len(content_str)} chars)")
    
    return posts


def extract_primary_keyword(title):
    """Extract primary keyword from title."""
    if not title:
        return ""
    title_lower = title.lower()
    
    # Patterns to extract meaningful keyword
    patterns = [
        r'^complete\s+(.+?)\s+(guide|strategy|checklist|overview)',
        r'^(ultimate|best|top|essential|comprehensive|expert|practical|proven)\s+(.+?)\s+(guide|strategy|tips|checklist|technique)',
        r'^(what|why|how)\s+(is|does|to|do)\s+(.+?)$',
        r'^(.+?)\s+(guide|strategy|checklist|tips|tutorial|overview|technique|পদ্ধতি|\u0997\u09be\u0987\u09a1|\u0995\u09cc\u09b6\u09b2)',
        r'^(.+?)\s+for\s+',
        r'^(.+?)\s+in\s+',
        r'^(.+?):\s+',
        r'^(.+?)\s+–\s+',
    ]
    
    for pattern in patterns:
        m = re.search(pattern, title_lower)
        if m:
            # Get the keyword group (the first meaningful capture)
            groups = m.groups()
            # Find the first non-empty, non-stopword group
            for g in groups:
                if g and len(g) > 3:
                    return g.strip()
    
    # Fallback: first 2-3 words skipping common words
    words = title_lower.split()
    skip_words = {'the', 'a', 'an', 'is', 'are', 'how', 'what', 'why', 'when', 'where', 'can', 'do', 'does', 'in', 'for', 'of', 'to', 'and', 'or', 'vs', 'your', 'our', 'its', 'vs.'}
    result = []
    for w in words:
        w_clean = re.sub(r'[^a-zA-Z0-9\u0980-\u09FF\s]', '', w)
        if w_clean and w_clean not in skip_words:
            result.append(w_clean)
        if len(result) >= 3:
            break
    if result:
        return ' '.join(result)
    return words[0] if words else ""


def check_tfidf(content, keyword):
    """Check keyword occurrence count."""
    if not keyword:
        return 0
    return len(re.findall(re.escape(keyword), content, re.IGNORECASE))


def check_entities(content, title, tags, excerpt):
    """Check required entities."""
    content_lower = content.lower()
    missing = []

    # Check for Bangladesh/Bangladeshi entities
    has_bangladesh = False
    for term in ['bangladesh', 'bangladeshi', 'বাংলাদেশ', 'বাংলাদেশী', 'বাংলাদেশি']:
        if term in content_lower:
            has_bangladesh = True
            break
    if not has_bangladesh:
        missing.append('"Bangladesh" / "বাংলাদেশ"')

    # Check for Dhaka
    has_dhaka = False
    for term in ['dhaka', 'ঢাকা']:
        if term in content_lower:
            has_dhaka = True
            break
    if not has_dhaka:
        missing.append('"Dhaka" / "ঢাকা"')

    # Check for service/industry entity based on tags and title
    tags_lower = [t.lower() for t in (tags or [])]
    title_lower = (title or '').lower()
    excerpt_lower = (excerpt or '').lower()
    combined = title_lower + ' ' + excerpt_lower + ' ' + content_lower
    
    service_entity_found = False
    
    # Service entity keywords organized by topic
    service_entities = {
        'seo': ['seo', 'search engine optimization'],
        'google ads / ppc': ['google ads', 'ppc', 'paid ads', 'adwords'],
        'content marketing': ['content marketing', 'content strategy'],
        'affiliate marketing': ['affiliate marketing', 'affiliate'],
        'local seo': ['local seo', 'local search', 'google maps', 'gmb', 'gbp', 'google business'],
        'technical seo': ['technical seo', 'core web vitals', 'page speed', 'crawlability'],
        'ecommerce': ['e-commerce', 'ecommerce', 'online store'],
        'youtube seo': ['youtube', 'video seo'],
        'google analytics': ['google analytics', 'ga4', 'analytics'],
        'schema / structured data': ['schema', 'structured data', 'breadcrumb', 'faq schema'],
        'link building': ['link building', 'backlink', 'linkbuilding'],
        'real estate': ['real estate', 'property'],
        'hotel / resort': ['hotel', 'resort', 'hospitality'],
        'restaurant / cafe': ['restaurant', 'cafe', 'food'],
        'ngo': ['ngo', 'nonprofit', 'non-profit', 'non profit'],
        'legal': ['legal', 'compliance', 'copyright'],
        'career': ['career', 'job', 'profession'],
        'hreflang': ['hreflang', 'international seo'],
        'https / ssl': ['https', 'ssl', 'security'],
        'mobile seo': ['mobile seo', 'mobile optimization'],
        'case study': ['case study'],
        'google discover': ['google discover', 'discover'],
        'skyscraper technique': ['skyscraper'],
        'pillar content': ['pillar', 'topic cluster'],
        'referral traffic': ['referral traffic', 'referral'],
        'direct traffic': ['direct traffic'],
        'branded vs non-branded': ['branded', 'non-branded'],
        'website speed': ['website speed', 'page speed', 'site speed', 'load time'],
        'bangla / bengali': ['bangla', 'bengali', 'বাংলা'],
        'citation': ['citation', 'nap', 'directory'],
    }

    # Collect all keywords from tags and title that are relevant
    relevant_kws = set()
    for tag in tags_lower:
        for entity, kws in service_entities.items():
            for kw in kws:
                if kw in tag:
                    relevant_kws.add(kw)
    
    # Also check title for service keywords
    for entity, kws in service_entities.items():
        for kw in kws:
            if kw in title_lower or kw in excerpt_lower:
                relevant_kws.add(kw)
    
    # Check if any service entity keyword is actually used in content
    if relevant_kws:
        for kw in relevant_kws:
            if len(kw) >= 4 and kw in content_lower:
                service_entity_found = True
                break
    
    # Broader check: look for any meaningful keyword from tags in content
    if not service_entity_found:
        for tag in tags_lower:
            # Skip very generic tags
            if tag in ['seo', 'digital marketing', '2026', 'bangladesh', 'dhaka', 'seo strategy']:
                continue
            words = tag.split()
            for w in words:
                if len(w) > 3 and w.lower() in content_lower:
                    service_entity_found = True
                    break
            if service_entity_found:
                break
    
    if not service_entity_found:
        missing.append('Service/Industry entity (from tags/content)')

    return missing


def check_pillar_link(content, slug):
    """Check if content links to the main pillar page."""
    if slug == PILLAR_SLUG:
        return True, 'N/A (this is the pillar page)'
    
    # The main pillar page URL
    for pattern in [PILLAR_URL, f'/blog/{PILLAR_SLUG}']:
        if pattern in content:
            return True, pattern
    return False, ''


def check_aeo_geo(content):
    """Count question-based headings."""
    questions = []
    for line in content.split('\n'):
        stripped = line.strip()
        if re.match(r'^#{2,3}\s+', stripped):
            heading_text = re.sub(r'^#+\s+', '', stripped)
            if re.match(r'^(How|What|Why|When|Where|Can|Do|Is|Are|Does|Which|Who)\b', heading_text, re.IGNORECASE):
                questions.append(heading_text)
    return questions


def check_internal_links(content):
    """Count internal links."""
    patterns = [
        r'/blog/[a-z0-9-]+',
        r'/services/[a-z0-9-]+',
        r'/locations/[a-z0-9-]+',
        r'/industries/[a-z0-9-]+',
    ]
    all_links = []
    for p in patterns:
        all_links.extend(re.findall(p, content))
    return list(set(all_links))


def check_schema_readiness(post):
    """Check if title, excerpt, date are all present."""
    missing = []
    if not post.get('title'):
        missing.append('title')
    if not post.get('excerpt'):
        missing.append('excerpt')
    if not post.get('date'):
        missing.append('date')
    return missing


def is_bengali(text):
    if not text:
        return False
    bengali_range = re.compile(r'[\u0980-\u09FF]')
    return bool(bengali_range.search(text))


def run_audit():
    print("=" * 70)
    print("CONTENT FRAMEWORK AUDIT REPORT")
    print(f"File: /root/kanok-miahit/src/app/blog/data.js")
    print(f"Posts to audit: {len(AUDIT_SLUGS)} (recently modified)")
    print("=" * 70)

    text = read_file('/root/kanok-miahit/src/app/blog/data.js')
    print("\nParsing blog posts...")
    posts = parse_posts(text)

    print(f"\nSuccessfully parsed: {len(posts)}/{len(AUDIT_SLUGS)} posts")
    missing_slugs = [s for s in AUDIT_SLUGS if s not in posts]
    if missing_slugs:
        print(f"Missing: {missing_slugs}")
    print()

    results = []
    for slug in AUDIT_SLUGS:
        if slug not in posts:
            print(f"\n{'='*60}")
            print(f"## Post: {slug}")
            print(f"{'='*60}")
            print("| Check | Status | Details |")
            print("|-------|--------|---------|")
            print("| PARSE | ❌ | Post not found in data.js |")
            print("\n### Fix instructions:")
            print(f"Post with slug '{slug}' was not found in the file. Check if slug exists or parse error occurred.")
            results.append({'slug': slug, 'pass': 0, 'total': 6, 'checks': {}})
            continue

        post = posts[slug]
        content = post.get('content', '')
        title = post.get('title', '')
        excerpt = post.get('excerpt', '')
        date = post.get('date', '')
        tags = post.get('tags', [])

        print(f"\n{'='*60}")
        print(f"## Post: {slug}")
        print(f"  Title: {title[:80] if title else 'N/A'}...")
        print(f"{'='*60}")

        # Extract primary keyword
        keyword = extract_primary_keyword(title)
        kw_count = check_tfidf(content, keyword) if keyword else 0
        tfidf_pass = kw_count >= 5
        tfidf_status = '✅' if tfidf_pass else '❌'

        # Entity check
        missing_entities = check_entities(content, title, tags, excerpt)
        entity_pass = len(missing_entities) == 0
        entity_status = '✅' if entity_pass else '❌'

        # Pillar link check
        pillar_found, pillar_url = check_pillar_link(content, slug)
        pillar_status = '✅' if pillar_found else '❌'

        # AEO/GEO check
        question_headings = check_aeo_geo(content)
        aeo_pass = len(question_headings) >= 2
        aeo_status = '✅' if aeo_pass else '❌'

        # Internal links check
        internal_links = check_internal_links(content)
        int_link_pass = len(internal_links) >= 3
        int_link_status = '✅' if int_link_pass else '❌'

        # Schema readiness check
        schema_missing = check_schema_readiness(post)
        schema_pass = len(schema_missing) == 0
        schema_status = '✅' if schema_pass else '❌'

        is_bn = is_bengali(title) or is_bengali(content[:200])

        tfidf_details = f'{kw_count} occurrences of "{keyword}"' if keyword else 'Could not extract keyword'
        entity_details = f'Missing: {", ".join(missing_entities)}' if missing_entities else 'All required entities found'
        pillar_details = f'Links to: {pillar_url}' if pillar_found else ('No pillar link found' if slug != PILLAR_SLUG else 'N/A')
        aeo_details = f'{len(question_headings)} question headings'
        if question_headings:
            aeo_details += f': {", ".join(q[:50] for q in question_headings[:3])}'
            if len(question_headings) > 3:
                aeo_details += f' (+{len(question_headings)-3} more)'
        int_link_details = f'{len(internal_links)} total: {", ".join(internal_links[:5])}' + ('...' if len(internal_links) > 5 else '')
        schema_details = f'Missing: {", ".join(schema_missing)}' if schema_missing else 'All fields set'

        print(f"| Check | Status | Details |")
        print(f"|-------|--------|---------|")
        print(f"| TF-IDF: {keyword[:50] if keyword else 'N/A'} | {tfidf_status} | {tfidf_details} |")
        print(f"| Entities | {entity_status} | {entity_details} |")
        print(f"| Pillar Link | {pillar_status} | {pillar_details} |")
        print(f"| AEO/GEO | {aeo_status} | {aeo_details} |")
        print(f"| Internal Links | {int_link_status} | {int_link_details} |")
        print(f"| Schema Ready | {schema_status} | {schema_details} |")

        print(f"\n### Fix instructions:")
        fixes = []
        if not tfidf_pass:
            fixes.append(f"- **TF-IDF**: Add the primary keyword \"{keyword}\" at least {5 - kw_count} more times in the content (currently {kw_count} occurrences). Ensure keyword appears naturally in headings, intro, and body.")
        if not entity_pass:
            if 'Bangladesh' in entity_details:
                fixes.append(f"- **Entities**: Add location entity \"Bangladesh\", \"Bangladeshi\", \"বাংলাদেশ\" or \"বাংলাদেশী\" at least once in the content.")
            if 'Dhaka' in entity_details:
                fixes.append(f"- **Entities**: Add location entity \"Dhaka\" or \"ঢাকা\" at least once in the content.")
            if 'Service/Industry' in entity_details:
                fixes.append(f"- **Entities**: Add relevant service/industry-specific terminology from the tags more prominently in the content. Tags: {tags}")
        if not pillar_found and slug != PILLAR_SLUG:
            fixes.append(f"- **Pillar Link**: Add an internal link to the main pillar page `{PILLAR_URL}` to strengthen pillar-cluster alignment.")
        if not aeo_pass:
            fixes.append(f"- **AEO/GEO**: Add at least {2 - len(question_headings)} more question-based headings (starting with How, What, Why, When, Where, Can, Do, Is, Are). Current: {len(question_headings)}")
        if not int_link_pass:
            fixes.append(f"- **Internal Links**: Add at least {3 - len(internal_links)} more internal links to /blog/..., /services/..., /locations/..., or /industries/... pages. Current: {len(internal_links)}")
        if not schema_pass:
            fixes.append(f"- **Schema Ready**: Add missing fields: {', '.join(schema_missing)}. These are needed for ArticleSchema markup.")
        if not fixes:
            fixes.append("- All checks passed. No fixes needed.")
        for f in fixes:
            print(f"{f}")

        checks_passed = sum([tfidf_pass, entity_pass, pillar_found, aeo_pass, int_link_pass, schema_pass])
        results.append({
            'slug': slug,
            'pass': checks_passed,
            'total': 6,
            'checks': {
                'TF-IDF': tfidf_pass,
                'Entities': entity_pass,
                'Pillar': pillar_found,
                'AEO/GEO': aeo_pass,
                'Internal Links': int_link_pass,
                'Schema': schema_pass,
            }
        })

    # Summary
    print("\n" + "=" * 70)
    print("OVERALL SUMMARY")
    print("=" * 70)
    total_passed = sum(r['pass'] for r in results)
    total_checks = sum(r['total'] for r in results)

    print(f"\nTotal posts: {len(results)}")
    print(f"Total checks: {total_checks}")
    print(f"Checks passed: {total_passed}")
    print(f"Checks failed: {total_checks - total_passed}")
    print(f"Overall pass rate: {total_passed}/{total_checks} ({total_passed * 100 // total_checks if total_checks else 0}%)")

    per_slug = [(r['slug'], r['pass'], r['total']) for r in results]
    print(f"\nPer-post results:")
    print(f"{'Slug':<55} {'Passed':<8} {'Total':<6} {'Status'}")
    print("-" * 75)
    for slug, p, t in per_slug:
        status = 'PASS ✅' if p == t else 'WARN ⚠️' if p >= t // 2 else 'FAIL ❌'
        print(f"{slug:<55} {p:<8} {t:<6} {status}")

    # Posts that need work
    failed_checks = sorted(
        [(r['slug'], r['pass'], r['total']) for r in results if r['pass'] < r['total']],
        key=lambda x: x[1]
    )
    if failed_checks:
        print(f"\nPosts needing attention ({len(failed_checks)} of {len(results)}):")
        for slug, p, t in failed_checks:
            if slug not in posts:
                print(f"  ❌ {slug} ({p}/{t} passed) - PARSE FAILED")
            else:
                r = next(rr for rr in results if rr['slug'] == slug)
                failed_checks_names = [c for c, v in r['checks'].items() if not v]
                print(f"  ❌ {slug} ({p}/{t} passed) - Failed: {', '.join(failed_checks_names)}")
    
    # Posts that fully pass
    passing = [(r['slug'], r['pass'], r['total']) for r in results if r['pass'] == r['total']]
    if passing:
        print(f"\nPosts passing all checks ({len(passing)} of {len(results)}):")
        for slug, p, t in passing:
            print(f"  ✅ {slug}")

    print(f"\n{'='*70}")
    print("END OF REPORT")
    print(f"{'='*70}")


if __name__ == '__main__':
    run_audit()
