#!/usr/bin/env python3
"""
Content Framework Enforcer for kanokmiah.com.bd
Reads data.js, extracts all posts, runs framework checks on changed ones.
"""
import re
import sys
import json
import subprocess
from datetime import datetime, timedelta, timezone

DATAJS_PATH = "src/app/blog/data.js"

# ── 1. Get recently changed slugs ──────────────────────────────────────────
def get_changed_slugs(hours=48):
    """Return set of post slugs changed in the last N hours."""
    since = datetime.now(timezone.utc) - timedelta(hours=hours)
    since_str = since.strftime("%Y-%m-%d %H:%M:%S +0000")
    
    result = subprocess.run(
        ["git", "log", "--format=%s", "--since=" + since_str, "--", DATAJS_PATH],
        capture_output=True, text=True, cwd="/root/kanok-miahit"
    )
    
    slugs = set()
    for line in result.stdout.strip().split("\n"):
        line = line.strip()
        if not line:
            continue
        
        # Pattern: "silo: processed blog #NN - slug"
        m = re.search(r'- ([a-z0-9][a-z0-9-]+[a-z0-9])\s*(?:\(.*?\))?\s*$', line)
        if m:
            slugs.add(m.group(1))
            continue
        
        # Pattern: "silo: added ... to slug"
        m = re.search(r'to ([a-z0-9][a-z0-9-]+[a-z0-9])\s*$', line)
        if m:
            slugs.add(m.group(1))
            continue
        
        # Pattern: "fix: deep audit fixes for slug"
        m = re.search(r'fixes for ([a-z0-9][a-z0-9-]+[a-z0-9])\s', line)
        if m:
            slugs.add(m.group(1))
            continue
        
        # Pattern: "fix: internal linking audit — ..." — applies to all
        if "fix: internal linking audit" in line.lower():
            # This affected ALL 127 blogs — but we treat it as bulk, skip
            continue
    
    return slugs


# ── 2. Parse data.js ───────────────────────────────────────────────────────
def parse_posts(filepath):
    """Parse the data.js file and return a list of post dicts."""
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()
    
    # Find the posts array content
    array_match = re.search(r'const posts\s*=\s*\[(.*?)\];', text, re.DOTALL)
    if not array_match:
        print("ERROR: Could not find posts array", file=sys.stderr)
        sys.exit(1)
    
    array_body = array_match.group(1)
    
    # Split into individual post objects by tracking brace depth
    posts = []
    i = 0
    while i < len(array_body):
        # Skip whitespace/comments
        i = skip_ws(array_body, i)
        if i >= len(array_body) or array_body[i] != '{':
            break
        
        # Parse one post object
        post, i = parse_object(array_body, i)
        if post:
            posts.append(post)
    
    return posts


def skip_ws(text, i):
    """Skip whitespace and // comments."""
    while i < len(text):
        if text[i] in ' \t\n\r,':
            i += 1
        elif text[i:i+2] == '//':
            nl = text.find('\n', i)
            i = nl + 1 if nl != -1 else len(text)
        else:
            break
    return i


def parse_object(text, start):
    """Parse a JS object { ... } from position start. Returns (dict, end_pos)."""
    obj = {}
    i = start
    if text[i] != '{':
        return None, start + 1
    
    i += 1  # skip {
    depth = 1
    key = None
    
    while i < len(text) and depth > 0:
        i = skip_ws(text, i)
        if i >= len(text):
            break
        
        ch = text[i]
        
        # Handle closing
        if ch == '}':
            depth -= 1
            if depth == 0:
                i += 1
                break
            i += 1
            continue
        
        if ch == '{':
            # Nested object — skip it
            _, i = parse_object(text, i)
            continue
        
        if ch == '[':
            # Array — skip it
            _, i = parse_array(text, i)
            continue
        
        if ch == '`':
            # Template literal (backtick string) — read until closing backtick
            val, i = parse_backtick(text, i)
            if key is not None:
                obj[key] = val
                key = None
            continue
        
        if ch == "'":
            # Single-quoted string
            val, i = parse_sq_string(text, i)
            if key is not None:
                obj[key] = val
                key = None
            else:
                # It's the key name (property name can be unquoted)
                key = val
            continue
        
        if ch == '"':
            # Double-quoted string
            val, i = parse_dq_string(text, i)
            if key is not None:
                obj[key] = val
                key = None
            else:
                key = val
            continue
        
        if ch == ':':
            i += 1
            continue
        
        if ch.isalpha() or ch == '_':
            # Unquoted property name (e.g., slug, title, tags)
            ident_end = i
            while ident_end < len(text) and (text[ident_end].isalnum() or text[ident_end] in '_-'):
                ident_end += 1
            ident = text[i:ident_end]
            i = ident_end
            i = skip_ws(text, i)
            if i < len(text) and text[i] == ':':
                key = ident
                i += 1
            else:
                # It might be a value like true/false/null/numbers
                if ident in ('true', 'false'):
                    obj[key] = ident == 'true'
                elif ident == 'null':
                    obj[key] = None
                elif ident.isdigit():
                    obj[key] = int(ident)
                else:
                    obj[key] = ident
                key = None
            continue
        
        i += 1
    
    return obj, i


def parse_array(text, start):
    """Parse a JS array [...] from position start. Returns (list, end_pos)."""
    items = []
    i = start
    if text[i] != '[':
        return items, start + 1
    i += 1
    
    while i < len(text):
        i = skip_ws(text, i)
        if i >= len(text):
            break
        if text[i] == ']':
            i += 1
            break
        
        if text[i] == "'":
            val, i = parse_sq_string(text, i)
            items.append(val)
        elif text[i] == '"':
            val, i = parse_dq_string(text, i)
            items.append(val)
        elif text[i] == '`':
            val, i = parse_backtick(text, i)
            items.append(val)
        elif text[i].isalpha() or text[i] in '-0123456789':
            # unquoted value
            ident_end = i
            while ident_end < len(text) and (text[ident_end].isalnum() or text[ident_end] in '_-.'):
                ident_end += 1
            items.append(text[i:ident_end])
            i = ident_end
        else:
            i += 1
    
    return items, i


def parse_sq_string(text, start):
    """Parse a single-quoted string. Returns (str, end_pos)."""
    i = start + 1
    result = []
    while i < len(text):
        ch = text[i]
        if ch == '\\':
            if i + 1 < len(text):
                result.append(text[i+1])
                i += 2
            else:
                i += 1
        elif ch == "'":
            i += 1
            break
        else:
            result.append(ch)
            i += 1
    return ''.join(result), i


def parse_dq_string(text, start):
    """Parse a double-quoted string."""
    i = start + 1
    result = []
    while i < len(text):
        ch = text[i]
        if ch == '\\':
            if i + 1 < len(text):
                result.append(text[i+1])
                i += 2
            else:
                i += 1
        elif ch == '"':
            i += 1
            break
        else:
            result.append(ch)
            i += 1
    return ''.join(result), i


def parse_backtick(text, start):
    """Parse a backtick template literal. Returns (content_str, end_pos)."""
    i = start + 1
    result = []
    depth = 0  # track ${ } nesting
    while i < len(text):
        ch = text[i]
        if ch == '\\':
            if i + 1 < len(text):
                result.append(text[i+1])
                i += 2
            else:
                i += 1
        elif ch == '$' and i + 1 < len(text) and text[i+1] == '{':
            # Template expression — skip until matching }
            expr_depth = 1
            i += 2
            while i < len(text) and expr_depth > 0:
                if text[i] == '{':
                    expr_depth += 1
                elif text[i] == '}':
                    expr_depth -= 1
                i += 1
        elif ch == '`':
            i += 1
            break
        else:
            result.append(ch)
            i += 1
    return ''.join(result), i


# ── 3. Framework Checks ────────────────────────────────────────────────────
def check_tfidf(post):
    """A. TF-IDF Coverage: extract primary keyword from title, count occurrences."""
    title = post.get('title', '')
    content = post.get('content', '')
    
    # Extract first meaningful noun phrase from title
    # Remove common filler words and take first significant word(s)
    stopwords = {'the', 'a', 'an', 'in', 'of', 'for', 'to', 'and', 'or', 'is', 'are', 'was', 'were',
                 'at', 'on', 'by', 'with', 'from', 'as', 'be', 'has', 'have', 'do', 'does', 'did'}
    
    words = re.findall(r'[A-Za-z][a-z]*', title.lower())
    # Find the first non-stopword
    keyword = ''
    for w in words:
        if w not in stopwords and len(w) > 2:
            keyword = w
            break
    # Actually, let's try extracting the bigram that captures the topic
    # Better: take first 2-3 meaningful words as the primary keyword phrase
    meaningful = [w for w in words if w not in stopwords and len(w) > 2]
    if len(meaningful) >= 2:
        keyword = ' '.join(meaningful[:2])
    elif meaningful:
        keyword = meaningful[0]
    else:
        keyword = words[0] if words else title.split()[0] if title.split() else ''
    
    # Count occurrences of the keyword in the content
    content_lower = content.lower()
    count = content_lower.count(keyword.lower())
    
    passed = count >= 5
    return {
        'keyword': keyword,
        'count': count,
        'passed': passed,
        'detail': f"{count} occurrences of '{keyword}'"
    }


def check_entities(post):
    """B. Semantic Entity Coverage: key entities that should be present."""
    content = post.get('content', '')
    content_lower = content.lower()
    title = post.get('title', '').lower()
    tags = [t.lower() for t in post.get('tags', [])]
    
    expected_entities = {
        'location: Dhaka': ['dhaka'],
        'location: Bangladesh': ['bangladesh'],
        'brand: Kanok Miah': ['kanok miah'],
    }
    
    # Determine service type from title/tags
    service_keywords = {
        'seo': 'SEO',
        'local seo': 'Local SEO',
        'technical seo': 'Technical SEO',
        'ecommerce': 'E-commerce',
        'content': 'Content Marketing',
        'link building': 'Link Building',
        'google maps': 'Google Maps',
        'google business': 'Google Business Profile',
        'schema': 'Schema Markup',
        'keyword': 'Keyword Research',
        'mobile': 'Mobile SEO',
    }
    
    detected_service = None
    for sk, sv in service_keywords.items():
        if sk in title or sk in ' '.join(tags):
            detected_service = sv
            break
    
    if detected_service:
        expected_entities[f'service: {detected_service}'] = [detected_service.lower()]
    
    # Industry detection from title/tags
    industry_keywords = {
        'garment': 'Garments/Textile',
        'textile': 'Garments/Textile',
        'real estate': 'Real Estate',
        'ecommerce': 'E-commerce',
        'e-commerce': 'E-commerce',
        'restaurant': 'Food/Restaurant',
        'hotel': 'Hotel/Resort',
        'resort': 'Hotel/Resort',
        'fitness': 'Fitness/Gym',
        'gym': 'Fitness/Gym',
        'law': 'Law Firms',
        'legal': 'Law Firms',
        'ngo': 'NGO',
        'startup': 'Startup',
        'education': 'Education',
        'health': 'Healthcare',
        'healthcare': 'Healthcare',
        'travel': 'Travel/Tourism',
        'tourism': 'Travel/Tourism',
        'youtube': 'YouTube',
        'podcast': 'Podcast',
        'mobile app': 'Mobile Apps',
    }
    
    detected_industry = None
    for ik, iv in industry_keywords.items():
        if ik in title or ik in ' '.join(tags):
            detected_industry = iv
            break
    
    if detected_industry:
        expected_entities[f'industry: {detected_industry}'] = [detected_industry.lower()]
    
    missing = []
    for entity_name, terms in expected_entities.items():
        found = any(term in content_lower for term in terms)
        if not found:
            missing.append(entity_name)
    
    passed = len(missing) == 0
    return {
        'passed': passed,
        'missing': missing,
        'detail': f"Missing: {', '.join(missing) if missing else 'None'}"
    }


def check_pillar_link(post):
    """C. Pillar-Cluster Alignment: check for pillar page link based on tags."""
    content = post.get('content', '')
    tags = [t.lower() for t in post.get('tags', [])]
    
    # Map tags to pillar pages
    pillar_map = {
        'seo guide': '/blog/complete-seo-guide-bangladesh-businesses-2026',
        'bangladesh seo': '/blog/complete-seo-guide-bangladesh-businesses-2026',
        'local seo': '/blog/local-seo-dhaka-google-maps-ranking',
        'technical seo': '/blog/technical-seo-core-web-vitals-optimization',
        'ecommerce': '/blog/ecommerce-seo-daraz-shopify-guide',
        'content marketing': '/blog/content-marketing-strategy-bangladeshi-brands-seo',
        'link building': '/blog/link-building-bangladesh-strategies',
        'mobile seo': '/blog/mobile-seo-optimization-bangladesh-mobile-first-era',
        'schema': '/blog/schema-markup-rich-snippets-techniques',
        'keyword research': '/blog/keyword-research-bangladesh-market',
    }
    
    pillar_url = None
    pillar_reason = ""
    for tag_key, url in pillar_map.items():
        if any(tag_key in t for t in tags):
            pillar_url = url
            pillar_reason = f"Tag '{tag_key}' → {url}"
            break
    
    if not pillar_url:
        # Try to infer from title
        title = post.get('title', '').lower()
        for tag_key, url in pillar_map.items():
            if tag_key in title:
                pillar_url = url
                pillar_reason = f"Title matches '{tag_key}' → {url}"
                break
    
    if not pillar_url:
        return {
            'passed': False,
            'pillar_url': None,
            'detail': "No pillar page identified for this post's tags"
        }
    
    # Check if the pillar URL is linked in the content
    # Normalize URLs — remove /blog/ prefix for matching
    pillar_path = pillar_url.replace('/blog/', '')
    linked = pillar_path in content or pillar_url in content
    
    return {
        'passed': linked,
        'pillar_url': pillar_url,
        'detail': f"{'Links to' if linked else 'Missing link to'} pillar: {pillar_url}"
    }


def check_aeo_geo(post):
    """D. AEO/GEO Optimization: count question-based headings."""
    content = post.get('content', '')
    
    # Find markdown headings that start with question words
    q_headings = re.findall(
        r'^#{2,6}\s+(How|What|Why|When|Where|Can|Do|Is|Are|Does|Did|Has|Have|Should|Which|Who|Whose)(\s|\?|:)',
        content,
        re.MULTILINE | re.IGNORECASE
    )
    
    count = len(q_headings)
    passed = count >= 2
    return {
        'count': count,
        'passed': passed,
        'detail': f"{count} question-based heading(s)"
    }


def check_internal_links(post):
    """E. Internal Linking: count internal links to other posts, services, locations."""
    content = post.get('content', '')
    
    # Count links to /blog/, /locations/, /services/, /industries/, /about
    internal_links = re.findall(
        r'\b(?:/blog/|/locations/|/services/|/industries/|/about\b|/contact\b|/faq\b)',
        content
    )
    
    # Also count markdown links with internal paths
    md_links = re.findall(
        r'\[([^\]]+)\]\((/[^\)]+)\)',
        content
    )
    internal_md = [l for l in md_links if any(l[1].startswith(p) for p in ['/blog/', '/locations/', '/services/', '/industries/', '/about', '/contact', '/faq'])]
    
    # Also check for inline links without markdown syntax — /blog/slug patterns
    inline_links = re.findall(r'(?<!\()/blog/[a-z0-9-]+', content)  # avoid double-counting md links
    
    total = len(set(internal_links + [l[1] for l in internal_md] + inline_links))
    # Deduplicate
    all_links = set(internal_links + [l[1] for l in internal_md] + inline_links)
    total = len(all_links)
    
    passed = total >= 3
    return {
        'count': total,
        'passed': passed,
        'detail': f"{total} internal link(s) to posts/services/locations"
    }


def check_schema(post):
    """F. Schema: check if post has title, excerpt, date (needed for ArticleSchema)."""
    checks = {
        'title': bool(post.get('title')),
        'excerpt': bool(post.get('excerpt')),
        'date': bool(post.get('date')),
        'author': bool(post.get('author')),
    }
    
    # Check for metaTitle and metaDescription
    if 'metaTitle' in post:
        checks['metaTitle'] = bool(post.get('metaTitle'))
    if 'metaDescription' in post:
        checks['metaDescription'] = bool(post.get('metaDescription'))
    if 'dateModified' in post:
        checks['dateModified'] = bool(post.get('dateModified'))
    
    missing = [k for k, v in checks.items() if not v]
    passed = len(missing) == 0
    return {
        'passed': passed,
        'missing': missing,
        'detail': f"All set" if passed else f"Missing: {', '.join(missing)}"
    }


# ── 4. Generate Report ─────────────────────────────────────────────────────
def generate_report(slug, checks):
    """Generate a markdown table for a post."""
    tfidf = checks['tfidf']
    entities = checks['entities']
    pillar = checks['pillar']
    aeo = checks['aeo']
    links = checks['links']
    schema = checks['schema']
    
    lines = []
    lines.append(f"## Post: {slug}")
    lines.append(f"| Check | Status | Details |")
    lines.append(f"|-------|--------|---------|")
    lines.append(f"| TF-IDF: '{tfidf['keyword']}' | {'✅' if tfidf['passed'] else '❌'} | {tfidf['detail']} |")
    lines.append(f"| Entities | {'✅' if entities['passed'] else '❌'} | {entities['detail']} |")
    lines.append(f"| Pillar Link | {'✅' if pillar['passed'] else '❌'} | {pillar['detail']} |")
    lines.append(f"| AEO/GEO | {'✅' if aeo['passed'] else '❌'} | {aeo['detail']} |")
    lines.append(f"| Internal Links | {'✅' if links['passed'] else '❌'} | {links['detail']} |")
    lines.append(f"| Schema Ready | {'✅' if schema['passed'] else '❌'} | {schema['detail']} |")
    
    # Fix instructions
    fixes = []
    if not tfidf['passed']:
        fixes.append(f"- **TF-IDF**: Increase occurrences of '{tfidf['keyword']}' to ≥5 (currently {tfidf['count']})")
    if not entities['passed']:
        fixes.append(f"- **Entities**: Add content mentioning: {', '.join(entities['missing'])}")
    if not pillar['passed']:
        fixes.append(f"- **Pillar Link**: Add link to pillar page: {pillar['detail']}")
    if not aeo['passed']:
        fixes.append(f"- **AEO/GEO**: Add more question-based headings (currently {aeo['count']}, need ≥2)")
    if not links['passed']:
        fixes.append(f"- **Internal Links**: Add more internal links to posts/services/locations (currently {links['count']}, need ≥3)")
    if not schema['passed']:
        fixes.append(f"- **Schema**: Set missing fields: {', '.join(schema['missing'])}")
    
    if fixes:
        lines.append("")
        lines.append("### Fix instructions:")
        for f in fixes:
            lines.append(f)
    lines.append("")
    
    return '\n'.join(lines)


def main():
    hours = 48
    
    print(f"# Content Framework Report — kanokmiah.com.bd")
    print(f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"Period: Last {hours} hours")
    print()
    
    # Get changed slugs
    changed_slugs = get_changed_slugs(hours)
    print(f"Changed posts detected: {len(changed_slugs)}")
    print()
    
    if not changed_slugs:
        print("✅ No new/modified posts — framework check skipped.")
        return
    
    # Parse all posts
    posts = parse_posts(DATAJS_PATH)
    posts_by_slug = {p.get('slug', ''): p for p in posts if p.get('slug')}
    
    print(f"Total posts in data.js: {len(posts)}")
    print(f"Changed slugs found via git: {len(changed_slugs)}")
    print()
    
    # Run checks on changed posts
    failed_posts = 0
    all_passed = True
    
    # Sort slugs for consistent output
    sorted_slugs = sorted(changed_slugs)
    
    for slug in sorted_slugs:
        if slug not in posts_by_slug:
            print(f"⚠️  Slug '{slug}' not found in data.js — skipping")
            continue
        
        post = posts_by_slug[slug]
        
        checks = {
            'tfidf': check_tfidf(post),
            'entities': check_entities(post),
            'pillar': check_pillar_link(post),
            'aeo': check_aeo_geo(post),
            'links': check_internal_links(post),
            'schema': check_schema(post),
        }
        
        report = generate_report(slug, checks)
        print(report)
        
        post_failed = any(not c['passed'] for c in checks.values())
        if post_failed:
            failed_posts += 1
            all_passed = False
    
    # Summary
    print("---")
    print()
    if all_passed:
        print("## ✅ Summary: All checks passed for all changed posts!")
    else:
        print(f"## ⚠️  Summary: {failed_posts}/{len(sorted_slugs)} posts need attention")
        print()
        print("Priority issues by type:")
        issue_counts = {}
        for slug in sorted_slugs:
            if slug not in posts_by_slug:
                continue
            post = posts_by_slug[slug]
            for check_name, check_result in {
                'tfidf': check_tfidf(post),
                'entities': check_entities(post),
                'pillar': check_pillar_link(post),
                'aeo': check_aeo_geo(post),
                'links': check_internal_links(post),
                'schema': check_schema(post),
            }.items():
                if not check_result['passed']:
                    issue_counts[check_name] = issue_counts.get(check_name, 0) + 1
        for check_name, count in sorted(issue_counts.items(), key=lambda x: -x[1]):
            print(f"- {check_name}: {count} posts failing")


if __name__ == '__main__':
    main()
