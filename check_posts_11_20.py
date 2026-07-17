#!/usr/bin/env python3
"""
Content Framework Checks for Posts 11-20 (batch 2) — Bengali content adapted.
Checks: TF-IDF keyword density, entity coverage, pillar-cluster alignment,
        AEO/GEO question headings, internal linking count, schema readiness.
"""
import re

DATA_FILE = "/root/kanok-miahit/src/app/blog/data.js"

with open(DATA_FILE, 'r', encoding='utf-8') as f:
    source = f.read()

TARGET_SLUGS = [
    "ecommerce-seo-daraz-shopify-guide",
    "link-building-bangladesh-strategies",
    "keyword-research-bangladesh-market",
    "content-marketing-seo-friendly-content-writing",
    "google-search-console-performance-guide",
    "mobile-seo-bangladesh-ranking-strategy",
    "schema-markup-rich-snippets-techniques",
    "youtube-seo-bangladesh-ranking-tips",
    "seo-bangla-blog-content-writing",
    "seo-tips-for-business-owners-bd",
]

# Parse helpers
def parse_post(data, slug):
    slug_line = 'slug: "' + slug + '"'
    idx = data.find(slug_line)
    if idx == -1:
        return None
    pre = data[:idx]
    block_start = pre.rfind('{\n')
    search_from = idx + len(slug_line)
    candidates = [len(data)]
    m = data.find('},\n  {\n    slug:', search_from)
    if m != -1: candidates.append(m + 1)
    m = data.find('};\n', search_from)
    if m != -1: candidates.append(m)
    m = data.find('];', search_from)
    if m != -1: candidates.append(m)
    end_idx = min(candidates)
    return data[block_start:end_idx]

def get_str(post, name):
    m = re.search(name + ':\\s*"((?:[^"\\\\]|\\.)*)"', post)
    if m: return m.group(1)
    m = re.search(name + ':\\s*\n\\s*"((?:[^"\\\\]|\\.)*)"', post)
    if m: return m.group(1)
    return ""

def get_tags(post):
    m = re.search(r'tags:\s*\[(.*?)\]', post, re.DOTALL)
    if m: return re.findall(r'"([^"]*)"', m.group(1))
    return []

def get_content(post):
    m = re.search(r'content:\s*`', post)
    if not m: return ""
    start = m.end()
    end = post.find('`', start)
    if end == -1: return post[start:]
    return post[start:end]

# Content analysis
def count_keyword(content, keyword):
    """Count case-insensitive occurrences of a keyword string."""
    if not keyword or not content:
        return 0
    return content.lower().count(keyword.lower())

def get_keyword_checks(slug):
    """Return (primary keyword, list of alt keywords) for a slug."""
    mapping = {
        'ecommerce-seo-daraz-shopify-guide': (
            'ই-কমার্স',
            ['দারাজ', 'শপিফাই', 'ecommerce', 'daraz', 'shopify', 'ইকমার্স']
        ),
        'link-building-bangladesh-strategies': (
            'লিংক বিল্ডিং',
            ['ব্যাকলিংক', 'link building', 'backlink', 'লিংক বিল্ডিং']
        ),
        'keyword-research-bangladesh-market': (
            'কীওয়ার্ড',
            ['কীওয়ার্ড রিসার্চ', 'keyword research', 'কীওয়ার্ড']
        ),
        'content-marketing-seo-friendly-content-writing': (
            'কন্টেন্ট মার্কেটিং',
            ['content marketing', 'কন্টেন্ট', 'কন্টেন্ট মার্কেটিং']
        ),
        'google-search-console-performance-guide': (
            'গুগল সার্চ কনসোল',
            ['search console', 'গুগল সার্চ কনসোল', 'gsc', 'পারফরমেন্স']
        ),
        'mobile-seo-bangladesh-ranking-strategy': (
            'মোবাইল',
            ['mobile seo', 'মোবাইল', 'মোবাইল SEO']
        ),
        'schema-markup-rich-snippets-techniques': (
            'স্কিমা মার্কআপ',
            ['schema', 'স্কিমা', 'schema markup', 'স্কিমা মার্কআপ']
        ),
        'youtube-seo-bangladesh-ranking-tips': (
            'ইউটিউব',
            ['youtube', 'ইউটিউব', 'youtube seo']
        ),
        'seo-bangla-blog-content-writing': (
            'বাংলা ব্লগ',
            ['বাংলা', 'bangla', 'ব্লগ', 'কন্টেন্ট']
        ),
        'seo-tips-for-business-owners-bd': (
            'SEO টিপস',
            ['seo tips', 'SEO', 'ব্যবসায়ী', 'এসইও']
        ),
    }
    return mapping.get(slug, (slug.replace('-', ' '), []))

def check_pillar_link(content, slug):
    links = re.findall(r'\[([^\]]*)\]\(([^)]*)\)', content)
    found_pillar = set()
    pillar_patterns = ['/services/', '/industries/', '/blog/', '/locations/', '/about', '/case-studies/']

    for text, href in links:
        h = href.strip()
        if h.startswith('/') and len(h) > 1:
            for pp in pillar_patterns:
                if h.startswith(pp):
                    found_pillar.add(h)
                    break
        elif 'kanokmiah.com.bd' in h.lower():
            parts = h.split('/')
            if len(parts) >= 4:
                normalized = '/' + '/'.join(parts[3:])
                for pp in pillar_patterns:
                    if normalized.startswith(pp):
                        found_pillar.add(normalized)
                        break
    return sorted(found_pillar)

def check_aeo_geo_bn(content):
    """Count question-based headings — supports Bengali question words."""
    headings = re.findall(r'^#{2,3}\s+(.+)$', content, re.MULTILINE)
    # English and Bengali question starters
    question_words = [
        'how', 'what', 'why', 'when', 'where', 'can', 'do', 'is', 'are',
        'does', 'will', 'should', 'which', 'who',
        # Bengali
        'কেন', 'কী', 'কি', 'কিভাবে', 'কখন', 'কোথায়', 'কত', 'কে',
        'কার', 'কোন', 'কোনটি', 'কেমন', 'হয়', 'আছে', 'পারে', 'যায়',
        'বাংলাদেশ',  # 'Bangladesh-এ GEO কেন গুরুত্বপূর্ণ?' starts with Bangladesh
    ]
    question_headings = []
    for h in headings:
        s = h.strip().lower()
        for qw in question_words:
            if s.startswith(qw.lower()):
                question_headings.append(h.strip())
                break
    return question_headings

def check_internal_links(content):
    links = re.findall(r'\[([^\]]*)\]\(([^)]*)\)', content)
    internals = set()
    for text, href in links:
        h = href.strip()
        if h.startswith('/') and len(h) > 1:
            internals.add(h)
        elif 'kanokmiah.com.bd' in h.lower():
            parts = h.split('/')
            if len(parts) >= 4:
                internals.add('/' + '/'.join(parts[3:]))
            else:
                internals.add('/')
    return sorted(internals)

def check_schema_readiness(post_data):
    missing = []
    if not post_data.get('title'): missing.append('title')
    if not post_data.get('excerpt'): missing.append('excerpt/description')
    if not post_data.get('date'): missing.append('date')
    if not post_data.get('author'): missing.append('author')
    if not post_data.get('tags'): missing.append('tags')
    return missing

# Main pipeline
results = {}
for slug in TARGET_SLUGS:
    post_raw = parse_post(source, slug)
    if not post_raw:
        results[slug] = {'error': 'NOT FOUND'}
        continue

    title = get_str(post_raw, 'title') or ''
    excerpt = get_str(post_raw, 'excerpt') or ''
    date = get_str(post_raw, 'date') or ''
    author = get_str(post_raw, 'author') or ''
    tags = get_tags(post_raw) or []
    content = get_content(post_raw) or ''

    # Find best keyword
    primary, alternates = get_keyword_checks(slug)
    c_lower = content.lower()

    best_kw = primary
    best_count = c_lower.count(best_kw.lower())

    for alt in alternates:
        c = c_lower.count(alt.lower())
        if c > best_count:
            best_count = c
            best_kw = alt

    tfidf_pass = best_count >= 5

    # Entities — check essential topic presence
    has_dhaka = 'ঢাকা' in content or 'dhaka' in c_lower
    has_bangladesh = 'বাংলাদেশ' in content or 'bangladesh' in c_lower

    missing_entities = []
    if not has_dhaka and not has_bangladesh:
        missing_entities.append("Location (Dhaka/Bangladesh)")

    # Check slug-specific Bengali entities
    entity_map = {
        'ecommerce-seo-daraz-shopify-guide': [('ই-কমার্স', 'ই-কমার্স'), ('দারাজ', 'দারাজ'), ('শপিফাই', 'শপিফাই')],
        'link-building-bangladesh-strategies': [('লিংক বিল্ডিং', 'লিংক বিল্ডিং'), ('ব্যাকলিংক', 'ব্যাকলিংক')],
        'keyword-research-bangladesh-market': [('কীওয়ার্ড', 'কীওয়ার্ড/Keyword')],
        'content-marketing-seo-friendly-content-writing': [('কন্টেন্ট মার্কেটিং', 'কন্টেন্ট মার্কেটিং'), ('কন্টেন্ট', 'কন্টেন্ট')],
        'google-search-console-performance-guide': [('গুগল সার্চ কনসোল', 'গুগল সার্চ কনসোল'), ('পারফরমেন্স', 'পারফরমেন্স')],
        'mobile-seo-bangladesh-ranking-strategy': [('মোবাইল', 'মোবাইল'), ('মোবাইল SEO', 'মোবাইল SEO')],
        'schema-markup-rich-snippets-techniques': [('স্কিমা', 'স্কিমা'), ('স্কিমা মার্কআপ', 'স্কিমা মার্কআপ')],
        'youtube-seo-bangladesh-ranking-tips': [('ইউটিউব', 'ইউটিউব'), ('ইউটিউব SEO', 'ইউটিউব SEO')],
        'seo-bangla-blog-content-writing': [('বাংলা', 'বাংলা'), ('ব্লগ', 'ব্লগ')],
        'seo-tips-for-business-owners-bd': [('ব্যবসায়ী', 'ব্যবসায়ী'), ('SEO টিপস', 'SEO টিপস')],
    }

    if slug in entity_map:
        for term, label in entity_map[slug]:
            if term.lower() not in content.lower():
                missing_entities.append("Entity (" + label + ")")

    entities_pass = len(missing_entities) == 0

    # AEO/GEO
    question_headings = check_aeo_geo_bn(content)
    aeo_pass = len(question_headings) >= 2

    # Pillar Link
    found_pillar = check_pillar_link(content, slug)
    pillar_pass = len(found_pillar) > 0

    # Internal Links
    internals = check_internal_links(content)
    il_pass = len(internals) >= 3

    # Schema
    schema_missing = check_schema_readiness({
        'title': title, 'excerpt': excerpt, 'date': date,
        'author': author, 'tags': tags
    })
    schema_pass = len(schema_missing) == 0

    results[slug] = {
        'title': title,
        'keyword': best_kw,
        'tfidf_count': best_count,
        'tfidf_pass': tfidf_pass,
        'missing_entities': missing_entities,
        'entities_pass': entities_pass,
        'found_pillar': found_pillar,
        'pillar_pass': pillar_pass,
        'question_headings': question_headings,
        'aeo_pass': aeo_pass,
        'internals': internals,
        'il_pass': il_pass,
        'schema_missing': schema_missing,
        'schema_pass': schema_pass,
        'content_len': len(content),
    }

# Output
all_pass_count = 0
fail_count = 0

for slug in TARGET_SLUGS:
    r = results[slug]
    if 'error' in r:
        sep = '=' * 70
        print()
        print(sep)
        print("Post: " + slug + " -- NOT FOUND in data.js")
        print(sep)
        fail_count += 1
        continue

    checks_passed = (r['tfidf_pass'] and r['entities_pass'] and r['pillar_pass']
                     and r['aeo_pass'] and r['il_pass'] and r['schema_pass'])
    total_passing = sum([r['tfidf_pass'], r['entities_pass'], r['pillar_pass'],
                         r['aeo_pass'], r['il_pass'], r['schema_pass']])

    sep = '=' * 70
    post_num = TARGET_SLUGS.index(slug) + 11
    print()
    print(sep)
    print("Post " + str(post_num) + ": " + slug)
    print(sep)
    print("Title: " + r['title'])
    print("Content length: " + str(r['content_len']) + " chars")
    print()

    print("{:<28} {:<7} {:<50}".format('Check', 'Status', 'Details'))
    print("{:-<28} {:-<7} {:-<50}".format('', '', ''))

    tfidf_detail = "keyword='" + r['keyword'] + "', found=" + str(r['tfidf_count']) + "x (need >=5)"
    print("{:<28} {:<7} {:<50}".format(
        'TF-IDF Keyword Density',
        'PASS' if r['tfidf_pass'] else 'FAIL',
        tfidf_detail[:48]))

    ent_detail = "All present" if r['entities_pass'] else "Missing: " + ', '.join(r['missing_entities'])
    print("{:<28} {:<7} {:<50}".format(
        'Entities',
        'PASS' if r['entities_pass'] else 'FAIL',
        ent_detail[:48]))

    pil_detail = "No relevant pillar link" if not r['found_pillar'] else "Links: " + ', '.join(r['found_pillar'][:5])
    print("{:<28} {:<7} {:<50}".format(
        'Pillar Link',
        'PASS' if r['pillar_pass'] else 'FAIL',
        pil_detail[:48]))

    aeo_detail = str(len(r['question_headings'])) + " question headings (need >=2)"
    print("{:<28} {:<7} {:<50}".format(
        'AEO/GEO Questions',
        'PASS' if r['aeo_pass'] else 'FAIL',
        aeo_detail[:48]))

    il_detail = str(len(r['internals'])) + " unique internal links (need >=3)"
    print("{:<28} {:<7} {:<50}".format(
        'Internal Links',
        'PASS' if r['il_pass'] else 'FAIL',
        il_detail[:48]))

    sch_detail = "All fields set" if r['schema_pass'] else "Missing: " + ', '.join(r['schema_missing'])
    print("{:<28} {:<7} {:<50}".format(
        'Schema Readiness',
        'PASS' if r['schema_pass'] else 'FAIL',
        sch_detail[:48]))

    total_str = "  Result: " + ('ALL PASS' if checks_passed else 'SOME FAILED') + " (" + str(total_passing) + "/6 checks passing)"
    print()
    print(total_str)

    if not checks_passed:
        print("  Fixes needed:")
        if not r['tfidf_pass']:
            print("    TF-IDF: Keyword '" + r['keyword'] + "' appears only " + str(r['tfidf_count']) + "x. Add >=5 occurrences.")
        if not r['entities_pass']:
            print("    Entities: Missing " + ', '.join(r['missing_entities']) + ".")
        if not r['pillar_pass']:
            print("    Pillar Link: Add internal link to /services/, /industries/, or /blog/ page.")
        if not r['aeo_pass']:
            print("    AEO/GEO: Only " + str(len(r['question_headings'])) + " question heading(s). Add >=2 FAQ-style headings.")
            print("    Question words checked: how, what, why, কেন, কী, কিভাবে, কত, etc.")
        if not r['il_pass']:
            print("    Internal Links: Only " + str(len(r['internals'])) + " link(s). Add >=3 internal links.")
        if not r['schema_pass']:
            print("    Schema: Missing fields: " + ', '.join(r['schema_missing']) + ".")
        fail_count += 1
    else:
        all_pass_count += 1

# Summary
print()
sep = '=' * 70
print(sep)
print("SUMMARY")
print(sep)
print("Posts checked: " + str(len(TARGET_SLUGS)))
print("All checks passed: " + str(all_pass_count))
print("Some checks failed: " + str(fail_count))
pass_rate = all_pass_count / len(TARGET_SLUGS) * 100
print("Pass rate: " + str(all_pass_count) + "/" + str(len(TARGET_SLUGS)) + " (" + str(round(pass_rate, 1)) + "%)")
print()

failure_counts = {'TF-IDF': 0, 'Entities': 0, 'Pillar Link': 0, 'AEO/GEO': 0, 'Internal Links': 0, 'Schema Readiness': 0}
for slug in TARGET_SLUGS:
    r = results.get(slug, {})
    if not r.get('tfidf_pass'): failure_counts['TF-IDF'] += 1
    if not r.get('entities_pass'): failure_counts['Entities'] += 1
    if not r.get('pillar_pass'): failure_counts['Pillar Link'] += 1
    if not r.get('aeo_pass'): failure_counts['AEO/GEO'] += 1
    if not r.get('il_pass'): failure_counts['Internal Links'] += 1
    if not r.get('schema_pass'): failure_counts['Schema Readiness'] += 1

print("Failure breakdown across all checks:")
for check, count in failure_counts.items():
    print("  " + check + ": " + str(count) + "/" + str(len(TARGET_SLUGS)) + " posts failing")
