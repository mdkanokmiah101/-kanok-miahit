#!/usr/bin/env python3
"""Content Framework Enforcer v2 - Improved TF-IDF with multi-phrase matching.
Run: python3 scripts/framework_check.py 2>&1
"""
import re, sys

with open('src/app/blog/data.js', 'r') as f:
    content = f.read()

parts = content.split("slug: ")[1:]
posts = []
for part in parts:
    post = {}
    m = re.match(r'["\']([^"\']+)["\']', part)
    if not m: continue
    post['slug'] = m.group(1)
    def extract(p, name):
        m2 = re.search(p, part, re.DOTALL)
        if m2: post[name] = m2.group(1).strip()
    extract(r'title:\s*["\']([^"\']+)["\']', 'title')
    extract(r'date:\s*["\']([^"\']+)["\']', 'date')
    extract(r'author:\s*["\']([^"\']+)["\']', 'author')
    extract(r'metaTitle:\s*["\']([^"\']+)["\']', 'metaTitle')
    extract(r'metaDescription:\s*["\']([^"\']+)["\']', 'metaDescription')
    tm = re.search(r'tags:\s*\[(.*?)\]', part, re.DOTALL)
    if tm: post['tags'] = re.findall(r'["\']([^"\']+)["\']', tm.group(1))
    cm = re.search(r'content:\s*`([\s\S]*?)`\s*(?:,|\);|\n\s*[},])', part)
    if cm: post['content'] = cm.group(1)
    else:
        cm2 = re.search(r'content:\s*`([\s\S]*)`', part)
        if cm2: post['content'] = cm2.group(1)
        else: post['content'] = ''
    posts.append(post)

print(f"Total posts parsed: {len(posts)}", file=sys.stderr)

posts_to_check = [
    "ai-seo-2026-dhaka-experts-optimize-google-ai-chatgpt",
    "hiring-seo-expert-dhaka-better-roi-than-paid-ads",
    "how-to-choose-best-seo-expert-dhaka-15-things",
    "seo-case-study-dhaka-businesses-increased-organic-traffic",
    "seo-expert-vs-seo-agency-dhaka-which-is-right",
    "top-10-seo-mistakes-dhaka-businesses-fix",
    "watchzonebd-seo-case-study",
    "what-does-seo-expert-do-guide-business-owners",
    "complete-seo-guide-bangladesh-businesses-2026",
    "content-marketing-strategy-bangladeshi-brands-seo",
    "das-taxis-scotland-seo-case-study",
    "geo-optimization-prepare-business-ai-search",
    "google-business-profile-optimization-guide-bangladesh",
    "how-to-choose-right-seo-agency-bangladesh",
    "international-seo-bangladesh-exporters-global-buyers",
    "link-building-strategies-bangladesh-market",
    "local-seo-tips-dhaka-businesses-google-maps",
    "locksmith-dundee-seo-case-study",
    "mobile-seo-optimization-bangladesh-mobile-first-era",
    "morethanpanel-seo-case-study",
    "seo-garments-textile-industry-b2b-lead-generation",
    "seo-real-estate-developers-dhaka",
    "seo-vs-google-ads-whats-best-bangladesh-businesses",
    "smmgen-seo-case-study",
    "smmsun-seo-case-study",
    "stealth-windshield-repairs-seo-case-study",
    "technical-seo-checklist-bangladeshi-websites",
    "why-ecommerce-store-needs-seo-bangladesh",
    "why-md-kanok-miah-is-the-best-seo-expert-in-dhaka-bangladesh",
]

STOP_WORDS = {'a','an','the','how','what','why','when','where','is','are','do','does',
              'to','for','in','of','on','at','by','with','from','and','or','but','not',
              'your','its','our','their','this','that','can','will','has','have','had',
              'be','been','being','was','were','it','as','no','yes','so','if','then',
              'which','who','whom','would','could','should','may','might','up','out',
              'about','into','over','after','before','between','through','during'}

def get_keyword_candidates(title):
    """Extract multiple keyword phrase candidates from title."""
    clean = re.sub(r'[^\w\s]', ' ', title)
    words = clean.split()
    
    # Skip leading stop words
    start = 0
    for i, w in enumerate(words):
        if w.lower() not in STOP_WORDS:
            start = i
            break
    
    candidates = []
    # Try different lengths of phrases
    for length in [4, 3, 2]:
        if start + length <= len(words):
            phrase = ' '.join(words[start:start+length])
            candidates.append(phrase.lower())
    
    # Also try the first content word + SEO-specific combinations
    if start < len(words):
        first_word = words[start].lower()
        for w in words[start+1:start+4]:
            candidates.append(f"{first_word} {w.lower()}")
    
    return list(set(candidates))

def check_tfidf(content, title):
    candidates = get_keyword_candidates(title)
    content_lower = content.lower()
    
    best_count = 0
    best_keyword = ""
    for kw in candidates:
        count = len(re.findall(re.escape(kw), content_lower))
        if count > best_count:
            best_count = count
            best_keyword = kw
    
    if best_count == 0 and candidates:
        best_keyword = candidates[0]
    
    status = "✅" if best_count >= 5 else "❌"
    return status, best_keyword, f"{best_count} occurrences"

def check_entities(content, slug, title, tags):
    content_lower = content.lower()
    missing = []
    if not re.search(r'dhaka', content_lower) and not any('international' in s or 'scotland' in s or 'dundee' in s or 'uk' in s or 'export' in s for s in [slug, title.lower()]):
        missing.append('Dhaka (location)')
    # Always require Bangladesh or Bangladesh context
    if not re.search(r'bangladesh|bangladeshi', content_lower):
        missing.append('Bangladesh (location)')
    if not re.search(r'kanok miah', content_lower):
        missing.append('Kanok Miah (author/brand)')
    status = "✅" if not missing else "❌"
    if not missing:
        details = "All required entities present"
    else:
        details = f"Missing: {', '.join(missing)}"
    return status, details

def check_pillar_cluster(tags, content, slug):
    pillar_slugs = [
        'complete-seo-guide-bangladesh-businesses-2026',
        'local-seo-tips-dhaka-businesses-google-maps',
        'technical-seo-checklist-bangladeshi-websites',
    ]
    found = [s for s in pillar_slugs if f'/blog/{s}' in content]
    has_services = bool(re.search(r'/services/', content))
    has_locations = bool(re.search(r'/locations/', content))
    
    if found:
        return "✅", f"Links to: {', '.join(found)}"
    elif has_services or has_locations:
        return "⚠️", f"No pillar page link (has {'services' if has_services else ''}{'/' if has_services and has_locations else ''}{'locations' if has_locations else ''})"
    else:
        return "❌", "No pillar page link found"

def check_aeo_geo(content):
    q_words = ['How','What','Why','When','Where','Can','Do','Is','Are','Does','Which','Who','Should','Will']
    headings = re.findall(r'^#{2,3}\s+.*$', content, re.MULTILINE)
    q_heads = []
    for h in headings:
        h_text = h.lstrip('#').strip()
        fw = h_text.split()[0] if h_text.split() else ''
        if fw in q_words or fw.rstrip('?:') in q_words:
            q_heads.append(h_text)
    count = len(q_heads)
    status = "✅" if count >= 2 else "❌"
    if q_heads:
        labels = q_heads[:3]
        if len(q_heads) > 3: labels.append(f"+{len(q_heads)-3} more")
        details = f"{count}: {'; '.join(labels)}"
    else:
        details = "0 question headings"
    return status, details

def check_internal_linking(content, slug):
    blog = [l for l in re.findall(r'/blog/([^"\')\]\s]+)', content) if l != slug]
    svc = re.findall(r'/services/([^"\')\]\s]+)', content)
    loc = re.findall(r'/locations/([^"\')\]\s]+)', content)
    ind = re.findall(r'/industries/([^"\')\]\s]+)', content)
    total = len(blog) + len(svc) + len(loc) + len(ind)
    status = "✅" if total >= 3 else "❌"
    types = []
    if blog: types.append(f"{len(blog)} posts")
    if svc: types.append(f"{len(svc)} services")
    if loc: types.append(f"{len(loc)} locations")
    if ind: types.append(f"{len(ind)} industries")
    return status, f"{total} total ({', '.join(types)})"

def check_schema(post):
    missing = []
    for field in ['title','excerpt','date','metaTitle','metaDescription']:
        if not post.get(field): missing.append(field)
    status = "✅" if not missing else "❌"
    if not missing:
        details = "All fields set"
    else:
        details = f"Missing: {', '.join(missing)}"
    return status, details

# Run
print("=" * 80)
print("CONTENT FRAMEWORK ENFORCEMENT REPORT — kanokmiah.com.bd")
print(f"Generated: July 15, 2026")
print("=" * 80)

all_passed = True
summary_rows = []

for target_slug in posts_to_check:
    post = next((p for p in posts if p['slug'] == target_slug), None)
    if not post:
        print(f"\n{'='*60}\n## Post: {target_slug}\n⚠️ NOT FOUND\n")
        continue
    
    title = post.get('title', '')
    content = post.get('content', '')
    tags = post.get('tags', [])
    
    print(f"\n{'='*60}")
    print(f"## Post: {target_slug}")
    print(f"Title: {title}")
    print(f"{'='*60}")
    print("| Check | Status | Details |")
    print("|-------|--------|---------|")
    
    results = {}
    
    st, kw, sd = check_tfidf(content, title)
    results['TF-IDF'] = (st, f"Keyword: '{kw}' — {sd}")
    print(f"| TF-IDF | {st} | {results['TF-IDF'][1]} |")
    
    st, sd = check_entities(content, target_slug, title, tags)
    results['Entities'] = (st, sd)
    print(f"| Entities | {st} | {sd} |")
    
    st, sd = check_pillar_cluster(tags, content, target_slug)
    results['Pillar Link'] = (st, sd)
    print(f"| Pillar | {st} | {sd} |")
    
    st, sd = check_aeo_geo(content)
    results['AEO/GEO'] = (st, sd)
    print(f"| AEO/GEO | {st} | {sd} |")
    
    st, sd = check_internal_linking(content, target_slug)
    results['Internal Links'] = (st, sd)
    print(f"| Internal Links | {st} | {sd} |")
    
    st, sd = check_schema(post)
    results['Schema'] = (st, sd)
    print(f"| Schema | {st} | {sd} |")
    
    # Fix instructions
    fixes = []
    if results['TF-IDF'][0] == '❌':
        fixes.append(f"- Boost primary keyword '{kw}' to >=5 occurrences")
    if results['Entities'][0] == '❌':
        fixes.append(f"- Add missing: {results['Entities'][1].replace('Missing: ', '')}")
    if results['Pillar Link'][0] == '❌':
        fixes.append("- Add link to pillar page (/blog/complete-seo-guide-bangladesh-businesses-2026)")
    if results['AEO/GEO'][0] == '❌':
        fixes.append("- Add >=2 question-based headings (How, What, Why...)")
    if results['Internal Links'][0] == '❌':
        fixes.append("- Add >=3 internal links (blog posts, services, locations, industries)")
    if results['Schema'][0] == '❌':
        fixes.append(f"- Set schema fields: {results['Schema'][1].replace('Missing: ', '')}")
    
    if fixes:
        print("\n### Fix instructions:")
        for f in fixes: print(f)
        all_passed = False
    else:
        print("\n### ✅ All checks passed!")
    
    # Store for summary
    checks_pass = all(r[0] == '✅' for r in results.values())
    summary_rows.append((target_slug, '✅ ALL PASS' if checks_pass else '❌ NEEDS FIXES'))
    print()

print("=" * 80)
print("SUMMARY")
print("=" * 80)
for slug, status in summary_rows:
    print(f"  {status} — {slug}")
print("=" * 80)
if all_passed:
    print("OVERALL: ✅ All 29 posts pass all framework checks")
else:
    # Count how many pass/fail
    pass_count = sum(1 for _, s in summary_rows if 'PASS' in s)
    fail_count = 29 - pass_count
    print(f"OVERALL: ❌ {fail_count} posts need fixes | {pass_count} posts pass all checks")
print("=" * 80)
