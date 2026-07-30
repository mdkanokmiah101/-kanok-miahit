#!/usr/bin/env python3
"""
Framework enforcement checker for kanokmiah.com.bd blog posts.
v3 - Simple line-by-line parser that handles multi-line titles.
"""
import re
import sys

DATA_FILE = "src/app/blog/data.js"

MODIFIED_SLUGS = [
    "link-building-strategies-bangladesh-market",
    "seo-garments-textile-industry-b2b-lead-generation",
    "google-business-profile-optimization-guide-bangladesh",
    "mobile-seo-optimization-bangladesh-mobile-first-era",
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
    "watchzonebd-seo-case-study",
]


def parse_posts(filepath):
    """
    Parse data.js using section-based approach.
    Split by slug: declarations and extract post objects.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Find all post blocks by splitting on slug patterns
    # Each post starts with { and has slug: "...",
    posts_raw = re.findall(
        r'\{\s*\n\s*slug:\s*"([^"]+)"(.*?)\n\s*\},?\s*(?=\n\s*\{|\n\s*\];)',
        text,
        re.DOTALL
    )
    
    # Also try to find posts that follow a different pattern
    if not posts_raw:
        # Fallback: find all { ... }, blocks
        posts_raw = []
        
    posts = []
    for slug, body in posts_raw:
        post = {'slug': slug}
        
        # Extract title (single or multi-line)
        title_m = re.search(r'title:\s*\n?\s*"([^"]+)"', body)
        if title_m:
            post['title'] = title_m.group(1)
        
        # Extract date
        date_m = re.search(r'date:\s*"([^"]+)"', body)
        if date_m:
            post['date'] = date_m.group(1)
        
        # Extract excerpt
        excerpt_m = re.search(r'excerpt:\s*\n?\s*"([^"]+)"', body)
        if excerpt_m:
            post['excerpt'] = excerpt_m.group(1)
        
        # Extract tags
        tags_m = re.search(r'tags:\s*\[(.*?)\]', body, re.DOTALL)
        if tags_m:
            tags_str = tags_m.group(1)
            tags = re.findall(r'"([^"]*?)"', tags_str)
            post['tags'] = tags
        
        # Extract content (between content: \` and \`\)
        content_m = re.search(r'content:\s*`(.*?)`\s*,?\s*$', body, re.DOTALL)
        if content_m:
            post['content'] = content_m.group(1)
        
        posts.append(post)
    
    return posts


def get_primary_keyword(title):
    """Extract primary keyword from title."""
    if not title:
        return "seo optimization"
    title_lower = title.lower()
    
    # Remove trailing parenthetical/suffix
    title_clean = re.sub(r'\s*\([^)]*\)', '', title_lower)
    title_clean = re.sub(r'\s*:.*$', '', title_clean)
    title_clean = re.sub(r'\s*—.*$', '', title_clean)
    
    # Try to find the core noun phrase
    patterns = [
        r'(?:complete|comprehensive|ultimate)\s+(.+?)(?:\s+(?:for|in|to|—|:))',
        r'(.+?)\s+(?:guide|strategies|tips|checklist|optimization)(?:\s+(?:for|in|to|—|:))',
        r'how to (.+?)(?:\s+(?:in|for|—|:|\d+))',
        r'what does (.+?)(?:\s+actually|\s+do)',
        r'why (.+?)(?:\s+(?:is|delivers|should))',
        r'top \d+ (.+?)(?:\s+(?:dhaka|bangladesh|for))',
        r'(.+?)(?:\s+(?:in|for|—|:))',
    ]
    
    for pat in patterns:
        m = re.search(pat, title_clean)
        if m:
            kw = m.group(1).strip()
            words = kw.split()[:4]
            if len(words) >= 2 or (len(words) == 1 and len(words[0]) > 4):
                return ' '.join(words)
    
    # Fallback: first few words
    words = title_lower.split()[:4]
    return ' '.join(words)


def check_tfidf(content, title):
    keyword = get_primary_keyword(title)
    if not keyword:
        return "❌", "Could not extract keyword"
    
    content_lower = content.lower()
    phrase_count = content_lower.count(keyword.lower())
    
    words = keyword.split()
    if len(words) > 1:
        significant = [w for w in words if len(w) > 3]
        if significant:
            max_word_count = max(content_lower.count(w) for w in significant)
            count = max(phrase_count, max_word_count)
        else:
            count = phrase_count
    else:
        count = phrase_count
    
    status = "✅" if count >= 5 else "❌"
    return status, f"{count} occurrences of '{keyword}'"


def check_entities(content, title, tags):
    content_lower = content.lower()
    missing = []
    
    # Location entities
    if not any(loc in content_lower for loc in ['dhaka', 'bangladesh']):
        missing.append('dhaka/bangladesh')
    
    # SEO service
    if not any(s in content_lower for s in ['seo', 'search engine optimization']):
        missing.append('seo service')
    
    # Tag-based entity checks
    if tags:
        t = ' '.join(t.lower() for t in tags)
        checks = [
            ('garments', ['garment', 'textile', 'apparel']),
            ('ecommerce', ['ecommerce', 'e-commerce', 'online store']),
            ('local', ['google business profile', 'google maps', 'gmb']),
            ('technical', ['page speed', 'core web vitals', 'crawlability']),
            ('backlink', ['backlink', 'link building', 'guest post']),
            ('construction', ['construction', 'cement', 'property']),
            ('transport', ['transportation', 'taxi']),
            ('locksmith', ['locksmith', 'lock', 'security']),
            ('automotive', ['automotive', 'windshield', 'auto repair']),
            ('ai', ['ai search', 'generative engine', 'chatgpt', 'ai overview']),
            ('case', ['case study', 'organic traffic', 'rankings']),
            ('b2b', ['b2b', 'manufacturing', 'lead generation']),
        ]
        for name, kws in checks:
            if name in t:
                found = any(k in content_lower for k in kws)
                if not found:
                    missing.append(f'{name} entity')
    
    status = "✅" if not missing else "❌"
    return status, missing if missing else ["All entities present"]


def check_pillar_cluster(tags, content, title):
    if not tags:
        return "❌", "No tags defined"
    
    t = ' '.join(t.lower() for t in tags)
    content_lower = content.lower()
    
    pillar_map = {
        'local-seo': ['local seo', 'google business profile', 'google maps', 'local search'],
        'technical-seo': ['technical seo', 'core web vitals', 'page speed'],
        'on-page-seo': ['on-page seo', 'content optimization'],
        'link-building': ['link building', 'backlink'],
        'ecommerce-seo': ['ecommerce', 'e-commerce'],
        'geo-aeo': ['geo', 'aeo', 'ai search', 'generative engine', 'ai overview'],
        'case-study': ['case study', 'seo results', 'seo case study'],
        'seo-services': ['seo expert', 'seo agency', 'seo services'],
    }
    
    matched = None
    for pillar, kws in pillar_map.items():
        if any(kw in t or kw in content_lower for kw in kws):
            matched = pillar
            break
    
    if not matched:
        return "❌", "Could not determine pillar topic"
    
    pillar_urls = {
        'local-seo': ['/services/local-seo'],
        'technical-seo': ['/services/technical-seo'],
        'on-page-seo': ['/services/on-page-seo'],
        'link-building': ['/blog/link-building-strategies-bangladesh-market'],
        'ecommerce-seo': ['/services/ecommerce-seo'],
        'geo-aeo': ['/blog/geo-optimization-prepare-business-ai-search'],
        'case-study': ['/blog', '/services/'],
        'seo-services': ['/services/', '/'],
    }
    
    urls = pillar_urls.get(matched, ['/'])
    links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
    link_urls = [l[1] for l in links]
    
    found = [u for u in urls if any(u in lu for lu in link_urls)]
    
    if found:
        return "✅", f"Pillar link: {found[0]}"
    return "❌", f"No pillar link for '{matched}'. Add link to {urls[0]}"


def check_aeo_geo(content):
    headings = re.findall(r'^#{1,4}\s+(.+)$', content, re.MULTILINE)
    q_words = ['How ', 'What ', 'Why ', 'When ', 'Where ', 'Can ', 'Do ', 'Is ', 'Are ', 'Which ', 'Who ', 'Does ']
    
    count = 0
    for h in headings:
        h = h.strip()
        if any(h.startswith(q) for q in q_words):
            count += 1
    
    status = "✅" if count >= 2 else "❌"
    return status, f"{count} question headings"


def check_internal_links(content):
    links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
    seen = set()
    
    for text, url in links:
        if url.startswith('http') and 'kanokmiah.com.bd' not in url and not url.startswith('/'):
            continue
        if url.startswith('#') or url.startswith('mailto:') or url.startswith('tel:'):
            continue
        clean = url.split('?')[0].split('#')[0].rstrip('/')
        if clean.startswith('http'):
            import urllib.parse
            clean = urllib.parse.urlparse(url).path.rstrip('/')
        if clean:
            seen.add(clean)
    
    count = len(seen)
    status = "✅" if count >= 3 else "❌"
    return status, f"{count} internal links"


def check_schema(post):
    missing = []
    if not post.get('title'): missing.append('title')
    if not post.get('excerpt'): missing.append('excerpt')
    if not post.get('date'): missing.append('date')
    
    status = "✅" if not missing else "❌"
    return status, "All set" if not missing else f"Missing: {', '.join(missing)}"


def main():
    posts = parse_posts(DATA_FILE)
    print(f"Parsed {len(posts)} total posts", file=sys.stderr)
    
    post_map = {p['slug']: p for p in posts if 'slug' in p}
    
    found = [s for s in MODIFIED_SLUGS if s in post_map]
    missing = [s for s in MODIFIED_SLUGS if s not in post_map]
    
    if missing:
        print(f"WARNING: Posts not found: {missing}", file=sys.stderr)
    
    total_checks = 0
    passed_checks = 0
    
    for slug in found:
        post = post_map[slug]
        title = post.get('title', 'Untitled')
        content = post.get('content', '')
        tags = post.get('tags', [])
        
        checks = {
            'TF-IDF': check_tfidf(content, title),
            'Entities': check_entities(content, title, tags),
            'Pillar Link': check_pillar_cluster(tags, content, title),
            'AEO/GEO': check_aeo_geo(content),
            'Internal Links': check_internal_links(content),
            'Schema Ready': check_schema(post),
        }
        
        failures = any(v[0] == '❌' for v in checks.values())
        icon = "⚠️" if failures else "✅"
        
        print(f"\n## {icon} Post: {slug}")
        print(f"**Title:** {title}")
        print(f"**Tags:** {', '.join(tags) if tags else '(none)'}")
        print()
        print("| Check | Status | Details |")
        print("|-------|--------|---------|")
        
        for name, (status, details) in checks.items():
            total_checks += 1
            if status == '✅':
                passed_checks += 1
            d = ', '.join(details[:4]) if isinstance(details, list) else str(details)
            print(f"| {name} | {status} | {d} |")
        
        if failures:
            print()
            print("### 🔧 Fix instructions:")
            for name, (status, details) in checks.items():
                if status == '❌':
                    if name == 'TF-IDF':
                        kw = get_primary_keyword(title)
                        print(f"- **TF-IDF**: Add more occurrences of '{kw}' (currently {details})")
                    elif name == 'Entities':
                        missing_list = details if isinstance(details, list) else [str(details)]
                        for m in missing_list[:4]:
                            if m != "All entities present":
                                print(f"- **Entity**: Add missing entity: {m}")
                    elif name == 'Pillar Link':
                        print(f"- **Pillar Link**: {details}")
                    elif name == 'AEO/GEO':
                        print(f"- **AEO/GEO**: Add 2+ question headings (How/What/Why). Currently {details}")
                    elif name == 'Internal Links':
                        print(f"- **Internal Links**: {details}")
                    elif name == 'Schema Ready':
                        print(f"- **Schema**: {details}")
    
    print(f"\n{'='*60}")
    print(f"## 📊 Summary")
    print(f"Posts: {len(found)} | Checks: {total_checks} | ✅ {passed_checks} | ❌ {total_checks - passed_checks}")
    
    if passed_checks == total_checks:
        print(f"\n✅ All framework checks passed!")
    else:
        print(f"\n⚠️ {total_checks - passed_checks} failures need attention.")


if __name__ == '__main__':
    main()
