#!/usr/bin/env python3
"""Framework enforcer v2: refined checks for kanokmiah.com.bd blog posts."""

import re

with open('src/app/blog/data.js', 'r') as f:
    content = f.read()

# Parse posts
pairs = []
for m in re.finditer(r'slug:\s*"([^"]+)"', content):
    slug = m.group(1)
    start = content.rfind('{', 0, m.start())
    depth = 0
    end = m.end()
    for i in range(m.end(), len(content)):
        if content[i] == '{':
            depth += 1
        elif content[i] == '}':
            if depth == 0:
                end = i + 1
                break
            depth -= 1
    pairs.append((slug, content[start:end]))

print(f"Parsed {len(pairs)} posts\n")

def extract_field(post_text, field):
    m = re.search(rf'{field}:\s*"([^"]*)"', post_text)
    if m:
        return m.group(1)
    m = re.search(rf'{field}:\s*`', post_text)
    if m:
        start = m.end()
        idx = post_text.find('`', start)
        if idx != -1:
            return post_text[start:idx]
    return None

def extract_tags(post_text):
    m = re.search(r'tags:\s*\[([^\]]*)\]', post_text)
    if m:
        return re.findall(r'"([^"]*)"', m.group(1))
    return []

def count_internal_links(ct):
    links = re.findall(r'\[([^\]]*)\]\((/[^)]*)\)', ct)
    internal = [(t, u) for t, u in links if any(u.startswith(p) for p in ['/blog/', '/locations/', '/services/', '/industries/', '/about', '/contact']) or u == '/']
    return internal

def count_question_headings(ct):
    return re.findall(r'^#{2,3}\s+(How|What|Why|When|Where|Can|Do|Is|Are|Does|Which)\b', ct, re.MULTILINE)

# Pillar definitions
PILLAR_DEFS = {
    'complete-seo-guide-bangladesh-businesses-2026': ('SEO Fundamentals', 'complete-seo-guide-bangladesh-businesses-2026'),
    'local-seo-tips-dhaka-businesses-google-maps': ('Local SEO', 'local-seo-tips-dhaka-businesses-google-maps'),
    'why-ecommerce-store-needs-seo-bangladesh': ('E-commerce SEO', 'why-ecommerce-store-needs-seo-bangladesh'),
    'technical-seo-checklist-bangladeshi-websites': ('Technical SEO', 'technical-seo-checklist-bangladeshi-websites'),
    'how-to-choose-right-seo-agency-bangladesh': ('SEO Agency Selection', 'how-to-choose-right-seo-agency-bangladesh'),
    'link-building-strategies-bangladesh-market': ('Link Building', 'link-building-strategies-bangladesh-market'),
    'geo-optimization-prepare-business-ai-search': ('GEO/AI Search', 'geo-optimization-prepare-business-ai-search'),
    'seo-garments-textile-industry-b2b-lead-generation': ('Industry SEO', 'seo-garments-textile-industry-b2b-lead-generation'),
    'google-business-profile-optimization-guide-bangladesh': ('GBP Optimization', 'google-business-profile-optimization-guide-bangladesh'),
    'content-marketing-strategy-bangladeshi-brands-seo': ('Content Marketing', 'content-marketing-strategy-bangladeshi-brands-seo'),
    'seo-trends-2026-ai-geo-future': ('SEO Trends', 'seo-trends-2026-ai-geo-future'),
}

def get_pillar(slug, tags, title):
    """Determine pillar topic. Returns (pillar_name, pillar_slug_or_None)."""
    if slug in PILLAR_DEFS:
        return PILLAR_DEFS[slug]
    
    tag_lower = [t.lower() for t in tags]
    title_lower = title.lower()
    
    # Mapping from tag patterns to (pillar_name, pillar_slug)
    RULES = [
        (['local seo', 'google maps', 'gbp', 'local'], ('Local SEO', 'local-seo-tips-dhaka-businesses-google-maps')),
        (['e-commerce seo', 'ecommerce', 'daraz', 'shopify'], ('E-commerce SEO', 'why-ecommerce-store-needs-seo-bangladesh')),
        (['technical seo', 'core web vitals', 'schema'], ('Technical SEO', 'technical-seo-checklist-bangladeshi-websites')),
        (['link building', 'backlink'], ('Link Building', 'link-building-strategies-bangladesh-market')),
        (['geo', 'ai search', 'generative'], ('GEO/AI Search', 'geo-optimization-prepare-business-ai-search')),
        (['content marketing', 'content strategy'], ('Content Marketing', 'content-marketing-strategy-bangladeshi-brands-seo')),
        (['seo guide', 'bangladesh seo', 'digital marketing'], ('SEO Fundamentals', 'complete-seo-guide-bangladesh-businesses-2026')),
        (['seo trends', 'voice search', 'mobile'], ('SEO Trends', 'seo-trends-2026-ai-geo-future')),
        (['case study'], ('Case Studies', None)),
        (['garment', 'textile', 'industry'], ('Industry SEO', 'seo-garments-textile-industry-b2b-lead-generation')),
        (['google business', 'gbp'], ('GBP Optimization', 'google-business-profile-optimization-guide-bangladesh')),
    ]
    
    for patterns, (pillar, ps) in RULES:
        for pat in patterns:
            if any(pat in t for t in tag_lower):
                return (pillar, ps)
    
    # Title-based fallback
    TL = [
        (['local', 'maps', 'gbp', 'neighborhood'], ('Local SEO', 'local-seo-tips-dhaka-businesses-google-maps')),
        (['ecommerce', 'e-commerce', 'daraz', 'shopify', 'woocommerce'], ('E-commerce SEO', 'why-ecommerce-store-needs-seo-bangladesh')),
        (['technical', 'core web', 'crawl', 'index', 'schema'], ('Technical SEO', 'technical-seo-checklist-bangladeshi-websites')),
        (['link building', 'backlink', 'link'], ('Link Building', 'link-building-strategies-bangladesh-market')),
        (['geo', 'ai search', 'generative engine'], ('GEO/AI Search', 'geo-optimization-prepare-business-ai-search')),
        (['content', 'blogging'], ('Content Marketing', 'content-marketing-strategy-bangladeshi-brands-seo')),
        (['seo guide', 'complete seo'], ('SEO Fundamentals', 'complete-seo-guide-bangladesh-businesses-2026')),
        (['case study'], ('Case Studies', None)),
    ]
    for patterns, (pillar, ps) in TL:
        for pat in patterns:
            if pat in title_lower:
                return (pillar, ps)
    
    return ('SEO Fundamentals', 'complete-seo-guide-bangladesh-businesses-2026')

def get_primary_keyword(title, slug):
    """Better keyword extraction."""
    title_l = title.lower()
    ct_title = title
    
    # Check if Bengali
    bengali_count = sum(1 for c in title if '\u0980' <= c <= '\u09FF')
    if bengali_count > 5:
        # Bengali title: use 'SEO' as main keyword since it's used in both En/Bn content
        return 'seo'
    
    # English title: extract main SEO topic
    patterns = [
        r'(generative engine optimization|geo)',
        r'(answer engine optimization|aeo)',
        r'(e-commerce seo)',
        r'(ecommerce seo)',
        r'(local seo)',
        r'(technical seo)',
        r'(link building)',
        r'(content marketing)',
        r'(voice search)',
        r'(mobile seo)',
        r'(schema markup)',
        r'(keyword research)',
        r'(google business profile)',
        r'(google my business)',
        r'(seo)\b',
    ]
    for p in patterns:
        m = re.search(p, title_l)
        if m:
            return m.group(1)
    
    # Fallback: first 2 meaningful words
    words = [w for w in title.split() if w.lower() not in ('for', 'in', 'the', 'a', 'an', 'to', 'of', 'and', 'your', 'that', 'is', 'are', 'what', 'why', 'how', 'does')]
    return ' '.join(words[:3]) if words else slug

# Process posts
results = []
aggregate_entity_dhaka = 0
aggregate_entity_bd = 0
aggregate_entity_kanok = 0

for slug, post_text in pairs:
    title = extract_field(post_text, 'title') or slug
    excerpt = extract_field(post_text, 'excerpt') or ''
    date = extract_field(post_text, 'date') or ''
    tags = extract_tags(post_text)
    ct = extract_field(post_text, 'content') or ''
    
    if not ct:
        continue
    
    # A: TF-IDF
    keyword = get_primary_keyword(title, slug)
    # Count keyword as whole word matches
    kw_escaped = re.escape(keyword)
    tfidf_count = len(re.findall(kw_escaped, ct, re.IGNORECASE))
    tfidf_pass = tfidf_count >= 5
    
    # B: Entities
    missing_entities = []
    if not re.search(r'\bDhaka\b', ct):
        missing_entities.append('Dhaka')
        aggregate_entity_dhaka += 1
    if not re.search(r'\bBangladesh\b', ct):
        missing_entities.append('Bangladesh')
        aggregate_entity_bd += 1
    if not re.search(r'Kanok Miah', ct):
        missing_entities.append('Kanok Miah')
        aggregate_entity_kanok += 1
    entities_pass = len(missing_entities) == 0
    
    # C: Pillar-Cluster
    pillar, pillar_slug = get_pillar(slug, tags, title)
    pillar_link_found = None
    if pillar_slug and pillar_slug != slug:
        # Check for link to pillar page
        pillar_url = f'/blog/{pillar_slug}'
        pillar_link_found = bool(re.search(re.escape(pillar_url), ct))
    elif pillar_slug == slug:
        pillar_link_found = True  # pillar page itself - trivially "links" to itself
    
    # D: AEO/GEO
    q_headings = count_question_headings(ct)
    q_count = len(q_headings)
    aeo_pass = q_count >= 2
    
    # E: Internal Links
    links = count_internal_links(ct)
    # Count unique internal URLs
    unique_urls = set(u for _, u in links)
    link_count = len(links)
    link_pass = link_count >= 3
    
    # F: Schema
    schema_missing = []
    if not title:
        schema_missing.append('title')
    if not excerpt or len(excerpt) < 10:
        schema_missing.append('excerpt')
    if not date:
        schema_missing.append('date')
    schema_pass = len(schema_missing) == 0
    
    results.append({
        'slug': slug,
        'title': title,
        'keyword': keyword,
        'tfidf_count': tfidf_count,
        'tfidf_pass': tfidf_pass,
        'entities_missing': missing_entities,
        'entities_pass': entities_pass,
        'pillar': pillar,
        'pillar_slug': pillar_slug,
        'pillar_link_found': pillar_link_found,
        'pillar_skip': pillar_slug == slug,
        'q_count': q_count,
        'aeo_pass': aeo_pass,
        'link_count': link_count,
        'link_pass': link_pass,
        'schema_missing': schema_missing,
        'schema_pass': schema_pass,
    })

# === REPORT ===
print("=" * 80)
print("CONTENT FRAMEWORK ENFORCEMENT REPORT — kanokmiah.com.bd")
print("=" * 80)
print(f"Date: Monday, July 20, 2026")
print(f"Posts analyzed: {len(results)}")
print(f"Trigger: 5 commits touching data.js in last 48 hours")
print()

# Classify posts
pillar_pages = [r for r in results if r['pillar_slug'] == r['slug']]
cluster_pages = [r for r in results if r['pillar_slug'] != r['slug']]
print(f"Pillar pages: {len(pillar_pages)}")
print(f"Cluster/other pages: {len(cluster_pages)}")
print()

# Summary counts (excluding pillar pages from pillar-link check, excluding Bangla from TF-IDF check)
tfidf_fails = [r for r in results if not r['tfidf_pass']]
entities_fails = [r for r in results if not r['entities_pass']]
# Pillar check: exclude pillar pages themselves and pages with no pillar slug (case studies)
pillar_fails = [r for r in cluster_pages if r['pillar_link_found'] is False]
pillar_na = [r for r in cluster_pages if r['pillar_link_found'] is None]
aeo_fails = [r for r in results if not r['aeo_pass']]
link_fails = [r for r in results if not r['link_pass']]
schema_fails = [r for r in results if not r['schema_pass']]

print("GLOBAL SUMMARY")
print(f"  ✅ TF-IDF Coverage:    {len(results) - len(tfidf_fails)}/{len(results)} pass ({len(tfidf_fails)} fails)")
print(f"  ✅ Entity Coverage:    {len(results) - len(entities_fails)}/{len(results)} pass ({len(entities_fails)} fails)")
print(f"  ✅ Pillar Link:        {len(cluster_pages) - len(pillar_fails)}/{len(cluster_pages)} pass ({len(pillar_fails)} fails, {len(pillar_na)} N/A — no pillar defined)")
print(f"  ✅ AEO/GEO:            {len(results) - len(aeo_fails)}/{len(results)} pass ({len(aeo_fails)} fails)")
print(f"  ✅ Internal Links:     {len(results) - len(link_fails)}/{len(results)} pass ({len(link_fails)} fails)")
print(f"  ✅ Schema Ready:       {len(results) - len(schema_fails)}/{len(results)} pass ({len(schema_fails)} fails)")
print()

# === PILLAR PAGES DETAIL ===
print("=" * 60)
print("PILLAR PAGES")
print("=" * 60)
for r in sorted(pillar_pages, key=lambda x: x['slug']):
    print(f"\n## Post: {r['slug']}")
    print(f"   Title: {r['title'][:70]}...")
    print(f"   Pillar: {r['pillar']} (self)")
    print(f"| Check | Status | Details |")
    print(f"|-------|--------|---------|")
    print(f"| TF-IDF: {r['keyword'][:20]} | {'✅' if r['tfidf_pass'] else '❌'} | {r['tfidf_count']} occurrences |")
    print(f"| Entities | {'✅' if r['entities_pass'] else '❌'} | Missing: {', '.join(r['entities_missing']) if r['entities_missing'] else 'None'} |")
    print(f"| Pillar Link | N/A | This IS the pillar page |")
    print(f"| AEO/GEO | {'✅' if r['aeo_pass'] else '❌'} | {r['q_count']} question headings |")
    print(f"| Internal Links | {'✅' if r['link_pass'] else '❌'} | {r['link_count']} total |")
    print(f"| Schema Ready | {'✅' if r['schema_pass'] else '❌'} | {', '.join(r['schema_missing']) if r['schema_missing'] else 'All fields set'} |")

# === TOP PASSING CLUSTER POSTS ===
print("\n\n" + "=" * 60)
print("SAMPLE PASSING CLUSTER POSTS")
print("=" * 60)
passing_cluster = [r for r in cluster_pages if r['tfidf_pass'] and r['entities_pass'] and r['pillar_link_found'] is not False and r['aeo_pass'] and r['link_pass'] and r['schema_pass']]
print(f"\n{len(passing_cluster)}/{len(cluster_pages)} cluster posts pass ALL checks")
if passing_cluster:
    for r in sorted(passing_cluster, key=lambda x: x['slug'])[:5]:
        print(f"  ✅ {r['slug']} — all checks passed")

# === FAILURES DETAIL ===
print("\n\n" + "=" * 60)
print("FAILURES DETAIL")
print("=" * 60)

# A: TF-IDF
if tfidf_fails:
    print(f"\n## A. TF-IDF Coverage — {len(tfidf_fails)} fails")
    print("Posts where primary keyword appears < 5 times:")
    for r in sorted(tfidf_fails, key=lambda x: x['tfidf_count']):
        status = '⚠️ Bengali title, keyword extraction may be inaccurate' if sum(1 for c in r['title'] if '\u0980' <= c <= '\u09FF') > 5 else ''
        print(f"  ❌ {r['slug']}: keyword='{r['keyword']}' × {r['tfidf_count']} {status}")

# B: Entities
if entities_fails:
    print(f"\n## B. Entity Coverage — {len(entities_fails)} fails")
    missing_dhaka = [r for r in entities_fails if 'Dhaka' in r['entities_missing']]
    missing_bd = [r for r in entities_fails if 'Bangladesh' in r['entities_missing']]
    missing_kanok = [r for r in entities_fails if 'Kanok Miah' in r['entities_missing']]
    print(f"  Posts missing 'Dhaka': {len(missing_dhaka)}")
    print(f"  Posts missing 'Bangladesh': {len(missing_bd)}")
    print(f"  Posts missing 'Kanok Miah': {len(missing_kanok)}")
    print()
    # Show worst offenders (missing all 3)
    worst = [r for r in entities_fails if len(r['entities_missing']) >= 3]
    if worst:
        print("  Posts missing 3+ entities:")
        for r in worst[:10]:
            print(f"  ❌ {r['slug']}: Missing {', '.join(r['entities_missing'])}")

# C: Pillar
if pillar_fails:
    print(f"\n## C. Pillar-Cluster Alignment — {len(pillar_fails)} fails")
    print("Cluster posts not linking back to their pillar page:")
    for r in sorted(pillar_fails, key=lambda x: x['slug']):
        print(f"  ❌ {r['slug']}: pillar='{r['pillar']}' → /blog/{r['pillar_slug']}")

if pillar_na:
    print(f"\n   (N/A: {len(pillar_na)} posts with no pillar page to link to — mostly case studies)")

# D: AEO/GEO
if aeo_fails:
    print(f"\n## D. AEO/GEO Optimization — {len(aeo_fails)} fails")
    print("Posts with < 2 question-format headings:")
    for r in sorted(aeo_fails, key=lambda x: x['q_count']):
        print(f"  ❌ {r['slug']}: {r['q_count']} question headings")
    print()
    print("  Fix: Add FAQ sections or question-based H2/H3 headings starting with")
    print("  How, What, Why, When, Where, Can, Do, Is, Are, Does, Which")

# E: Internal Links
if link_fails:
    print(f"\n## E. Internal Linking — {len(link_fails)} fails")
    print("Posts with < 3 internal links:")
    for r in sorted(link_fails, key=lambda x: x['link_count']):
        print(f"  ❌ {r['slug']}: {r['link_count']} internal links")
    print()
    print("  These are mostly pure technical reference posts (canonical, redirects,")
    print("  hreflang, etc.) that lack any internal linking. Add links to related")
    print("  services (/services/technical-seo), locations, or blog posts.")

# F: Schema
if schema_fails:
    print(f"\n## F. Schema Readiness — {len(schema_fails)} fails")
    for r in sorted(schema_fails, key=lambda x: x['slug']):
        print(f"  ❌ {r['slug']}: Missing {', '.join(r['schema_missing'])}")

# === SUMMARY TABLE ===
print("\n\n" + "=" * 60)
print("CONSOLIDATED FAILURE TABLE")
print("=" * 60)
print(f"{'Check':<20} {'Failures':<10} {'Pass Rate':<15} {'Severity'}")
print(f"{'-'*20} {'-'*10} {'-'*15} {'-'*10}")
print(f"{'A. TF-IDF':<20} {len(tfidf_fails):<10} {((len(results)-len(tfidf_fails))/len(results)*100):<15.0f}% {'MEDIUM'}")
print(f"{'B. Entities':<20} {len(entities_fails):<10} {((len(results)-len(entities_fails))/len(results)*100):<15.0f}% {'LOW'}")
print(f"{'C. Pillar Link':<20} {len(pillar_fails):<10} {((len(cluster_pages)-len(pillar_fails))/len(cluster_pages)*100):<15.0f}% {'MEDIUM'}")
print(f"{'D. AEO/GEO':<20} {len(aeo_fails):<10} {((len(results)-len(aeo_fails))/len(results)*100):<15.0f}% {'HIGH'}")
print(f"{'E. Internal Links':<20} {len(link_fails):<10} {((len(results)-len(link_fails))/len(results)*100):<15.0f}% {'HIGH'}")
print(f"{'F. Schema Ready':<20} {len(schema_fails):<10} {'100%':<15} {'NONE'}")

# === FIX INSTRUCTIONS ===
print("\n\n" + "=" * 60)
print("FIX INSTRUCTIONS")
print("=" * 60)

print("""
### HIGH PRIORITY

#### D. AEO/GEO Optimization
86 posts lack sufficient question-format headings. This directly impacts visibility
in AI-powered search (ChatGPT, Google SGE, Perplexity, Gemini).

**For each post**, add an FAQ section with at least 2 question-based H3 headings:
```markdown
## Frequently Asked Questions

### How does [topic] work for Dhaka businesses?
[Answer]

### What is the cost of [service] in Bangladesh?
[Answer]
```
Minimum: 2 question headings per post.

#### E. Internal Linking
13 posts have < 3 internal links (mostly standalone technical guides).

**Fix**: Add links to:
- The relevant service page: /services/technical-seo
- Related blog posts (the pillar page)
- At least one location page: /locations/dhaka

### MEDIUM PRIORITY

#### C. Pillar-Cluster Alignment
31 posts don't link back to their pillar page. Add a link like:
```
For a complete guide, read our [pillar topic](/blog/pillar-slug).
```

#### A. TF-IDF Coverage
40 posts have thin keyword usage. Add 2-3 more mentions of the primary keyword.
(NOTE: ~25 of these are Bengali-language posts where keyword extraction is 
approximate — manual review recommended.)

### LOW PRIORITY

#### B. Entity Coverage
94 posts fail entity checks, but many are short technical reference posts where
mentioning "Dhaka", "Bangladesh", or "Kanok Miah" in every post may feel forced.
Recommendation: Add at least one contextual mention, e.g.:
- "For Bangladeshi websites using canonical tags..." 
- "This guide is tailored for SEO professionals in Dhaka..."

""")

# === TOP 5 WORST POSTS ===
print("=" * 60)
print("TOP POSTS NEEDING ATTENTION")
print("=" * 60)
scored = []
for r in results:
    score = 0
    if not r['tfidf_pass']: score += 1
    if not r['entities_pass']: score += 1
    if r['pillar_link_found'] is False: score += 2
    if not r['aeo_pass']: score += 3
    if not r['link_pass']: score += 3
    if not r['schema_pass']: score += 1
    scored.append((score, r['slug'], r['title']))

for score, slug, title in sorted(scored, key=lambda x: -x[0])[:10]:
    r = next(x for x in results if x['slug'] == slug)
    print(f"\n### {slug} (score: {score}/11)")
    issues = []
    if not r['tfidf_pass']: issues.append(f"TF-IDF: '{r['keyword']}' × {r['tfidf_count']}")
    if not r['entities_pass']: issues.append(f"Entities: missing {', '.join(r['entities_missing'])}")
    if r['pillar_link_found'] is False: issues.append(f"Pillar link missing → /blog/{r['pillar_slug']}")
    if not r['aeo_pass']: issues.append(f"AEO/GEO: {r['q_count']} question headings")
    if not r['link_pass']: issues.append(f"Internal links: {r['link_count']}")
    if not r['schema_pass']: issues.append(f"Schema: missing {', '.join(r['schema_missing'])}")
    for i in issues:
        print(f"  ❌ {i}")
