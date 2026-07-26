#!/usr/bin/env python3
"""
Framework checks on posts 5-9 (seo-for-startups-bangladesh, seo-howto-schema-bangladesh,
seo-faq-schema-bangladesh, seo-breadcrumb-schema-bd, seo-json-ld-schema-bangladesh)
"""
import json
import re
import os

POST_FILES = [
    "/tmp/blog_posts/seo-for-startups-bangladesh.json",
    "/tmp/blog_posts/seo-howto-schema-bangladesh.json",
    "/tmp/blog_posts/seo-faq-schema-bangladesh.json",
    "/tmp/blog_posts/seo-breadcrumb-schema-bd.json",
    "/tmp/blog_posts/seo-json-ld-schema-bangladesh.json",
]

# ─── Check: A. TF-IDF Coverage ───────────────────────────────────────────────
def check_tfidf(post):
    """Primary keyword density check."""
    title = post['title']
    content = post['content']
    slug = post['slug']

    # Determine primary keyword from title
    is_bengali = any(ord(c) > 127 for c in title)
    eng_kw = None
    eng_count = 0

    if is_bengali:
        # For Bengali titles, extract keyword before colon
        if ':' in title:
            keyword = title.split(':')[0].strip()
        else:
            keyword = title.strip()
        # Also try extracting the English acronym if present (e.g., JSON-LD, HowTo)
        eng_match = re.search(r'([A-Z][A-Z0-9\-]+)', title)
        eng_kw = eng_match.group(1) if eng_match else None
        if eng_kw:
            eng_count = content.count(eng_kw)
        else:
            eng_count = 0
        # Count Bengali title phrase
        count = content.count(keyword)
        # Use whichever is higher
        if eng_kw and eng_count > count:
            count = eng_count
            keyword_display = f"{keyword} (en:{eng_kw})"
        else:
            keyword_display = keyword
    else:
        # English: extract keyword before "in Bangladesh" or before colon
        kw_match = re.search(r'SEO for (.+?)(?: in Bangladesh|$)', title)
        if kw_match:
            keyword = kw_match.group(1).strip()
        elif ':' in title:
            keyword = title.split(':')[0].strip()
        else:
            keyword = title.strip()
        keyword_display = keyword
        count = content.count(keyword)

    # Case-insensitive count
    count_ci = len(re.findall(re.escape(keyword), content, re.IGNORECASE))
    if eng_kw and eng_count > 0:
        eng_count_ci = len(re.findall(re.escape(eng_kw), content, re.IGNORECASE))
        if eng_count_ci > count_ci:
            count_ci = eng_count_ci

    passed = count_ci >= 5
    return {
        'keyword': keyword_display[:60],
        'count': count_ci,
        'pass': passed,
        'is_bengali': is_bengali
    }


# ─── Check: B. Semantic Entity Coverage ───────────────────────────────────────
def check_entities(post):
    content = post['content'].lower()
    title = post['title']
    is_bengali = any(ord(c) > 127 for c in title)
    missing = []

    # 1. Bangladesh / বাংলাদেশ
    has_bd = bool(re.search(r'বাংলাদেশ|bangladesh|bangladeshi', content, re.IGNORECASE))
    if not has_bd:
        missing.append('Bangladesh/বাংলাদেশ')

    # 2. Local city (Dhaka/ঢাকা etc)
    cities = ['ঢাকা', 'dhaka', 'chittagong', 'চট্টগ্রাম', 'sylhet', 'সিলেট',
              'khulna', 'খুলনা', 'rajshahi', 'রাজশাহী']
    has_city = any(c in content for c in cities)
    if not has_city:
        missing.append('local city (ঢাকা/Dhaka etc.)')

    # 3. Google / গুগল
    has_google = bool(re.search(r'google|গুগল', content, re.IGNORECASE))
    if not has_google:
        missing.append('Google/গুগল')

    # 4. Schema / স্কিমা (for schema posts)
    has_schema = bool(re.search(r'schema|স্কিমা|schema\.org', content, re.IGNORECASE))
    if not has_schema:
        missing.append('Schema/স্কিমা')

    return {
        'missing': missing,
        'pass': len(missing) == 0
    }


# ─── Check: C. Pillar-Cluster Alignment ──────────────────────────────────────
def check_pillar(post):
    content = post['content']
    slug = post['slug']
    title = post['title']
    is_bengali = any(ord(c) > 127 for c in title)

    # For schema posts (HowTo, FAQ, Breadcrumb, JSON-LD), the structured data pillar
    # is /blog/seo-structured-data-guide-bd
    # Also check /services/technical-seo

    pillar_candidates = [
        '/blog/seo-structured-data-guide-bd',
        '/services/technical-seo',
        '/blog/complete-seo-guide-bangladesh-businesses-2026',
    ]

    found_pillars = []
    for p in pillar_candidates:
        if p in content or p.replace('/blog/', '/blog/') in content:
            found_pillars.append(p)

    # Also check for markdown-style links
    for p in pillar_candidates:
        slug_part = p.split('/')[-1]
        if slug_part in content:
            if slug_part not in [f.split('/')[-1] for f in found_pillars]:
                # Just the slug part appearing is weaker evidence, but note it
                if p not in found_pillars:
                    found_pillars.append(f"(slug:{slug_part})")

    return {
        'found_pillars': found_pillars if found_pillars else ['none'],
        'pass': len(found_pillars) > 0
    }


# ─── Check: D. AEO/GEO Optimization ──────────────────────────────────────────
def check_aeo_geo(post):
    content = post['content']
    title = post['title']
    is_bengali = any(ord(c) > 127 for c in title)

    # Extract all headings
    headings = re.findall(r'^#{2,4}\s+(.+?)$', content, re.MULTILINE)

    # English question words
    en_q = r'^(How|What|Why|When|Where|Can|Do|Is|Are|Does|Did|Will|Would|Should|Could|Which|Who)\s'

    # Bengali question words
    bn_q_words = [
        'কী', 'কীভাবে', 'কেন', 'কিভাবে', 'কি', 'কখন', 'কোথায়', 'কোথায়',
        'কেমন', 'কোন', 'কার', 'কত', 'কিসের', 'কেননা'
    ]
    bn_pattern = '|'.join(re.escape(w) for w in bn_q_words)
    bn_q = rf'^({bn_pattern})\s'

    question_headings = []
    for h in headings:
        h_stripped = h.strip()
        if re.match(en_q, h_stripped, re.IGNORECASE):
            question_headings.append(h_stripped)
        elif re.match(bn_q, h_stripped):
            question_headings.append(h_stripped)
        # Also treat headings ending with ? as questions
        if h_stripped.endswith('?'):
            if h_stripped not in question_headings:
                question_headings.append(h_stripped)

    return {
        'total_headings': len(headings),
        'question_headings': len(question_headings),
        'question_examples': question_headings[:5],
        'pass': len(question_headings) >= 2
    }


# ─── Check: E. Internal Linking ──────────────────────────────────────────────
def check_internal_links(post):
    content = post['content']
    slug = post['slug']

    # Find all internal links
    # HTML href links
    html_links = re.findall(r'href="(/[^"]+)"', content)
    # Markdown links
    md_links = re.findall(r'\[([^\]]+)\]\((/[^)]+)\)', content)
    md_link_urls = [m[1] for m in md_links]

    all_links = html_links + md_link_urls

    # Filter internal paths
    internal_paths = ['/blog/', '/services/', '/locations/', '/industries/', '/about', '/contact']
    internal = [l for l in all_links if any(l.startswith(p) for p in internal_paths)]

    # Remove self-references
    internal = [l for l in internal if slug not in l]

    unique = list(set(internal))

    # Count by category
    blog_links = [l for l in unique if l.startswith('/blog/')]
    svc_links = [l for l in unique if l.startswith('/services/')]
    loc_links = [l for l in unique if l.startswith('/locations/')]
    ind_links = [l for l in unique if l.startswith('/industries/')]

    return {
        'total_unique': len(unique),
        'blog': len(blog_links),
        'services': len(svc_links),
        'locations': len(loc_links),
        'industries': len(ind_links),
        'links_sample': unique[:5],
        'pass': len(unique) >= 3
    }


# ─── Check: F. Schema Readiness ──────────────────────────────────────────────
def check_schema(post):
    missing = []
    if not post.get('title'):
        missing.append('title')
    if not post.get('excerpt'):
        missing.append('excerpt')
    if not post.get('date'):
        missing.append('date')
    if not post.get('author'):
        missing.append('author')
    # Check dateModified (optional but recommended)
    has_date_mod = bool(post.get('dateModified'))
    return {
        'missing': missing,
        'dateModified': has_date_mod,
        'pass': len(missing) == 0
    }


# ─── Check: G. Bengali AEO Question Words ────────────────────────────────────
def check_bengali_aeo(post):
    """Specifically check Bengali question words for AEO."""
    content = post['content']
    title = post['title']
    is_bengali = any(ord(c) > 127 for c in title)

    if not is_bengali:
        return {'note': 'English post — Bengali AEO check N/A', 'pass': True}

    bn_question_words = {
        'কী': 'ki/what',
        'কেন': 'keno/why',
        'কিভাবে': 'kivabe/how',
        'কীভাবে': 'kivabe/how',
        'কি': 'ki/what',
        'কখন': 'kokhon/when',
        'কোথায়': 'kothay/where',
        'কোথায়': 'kothay/where',
        'কেমন': 'kemon/how',
        'কোন': 'kon/which',
    }

    found = {}
    for w, meaning in bn_question_words.items():
        c = content.count(w)
        if c > 0:
            found[w] = {'count': c, 'meaning': meaning}

    # Check in headings specifically — accept headings that:
    # 1. START with a Bengali question word, OR
    # 2. END with "?" AND contain a Bengali question word (Bengali often puts Q-word at end)
    # 3. END with "?" (generic question heading)
    headings = re.findall(r'^#{2,4}\s+(.+?)$', content, re.MULTILINE)
    q_in_headings = []
    for h in headings:
        h_stripped = h.strip()
        # Check heading starts with Bengali question word
        for w in bn_question_words:
            if h_stripped.startswith(w):
                if h_stripped not in q_in_headings:
                    q_in_headings.append(h_stripped)
                break
        else:
            # Check if heading contains Bengali question word AND ends with ?
            if h_stripped.endswith('?'):
                for w in bn_question_words:
                    if w in h_stripped:
                        if h_stripped not in q_in_headings:
                            q_in_headings.append(h_stripped)
                        break
                else:
                    # Ends with ? but no Bengali question word — still count as AEO
                    if h_stripped not in q_in_headings:
                        q_in_headings.append(h_stripped)

    return {
        'bengali_q_words_found': len(found),
        'words': found,
        'q_in_headings': q_in_headings[:5],
        'pass': len(q_in_headings) >= 2
    }


# ─── Run All Checks ──────────────────────────────────────────────────────────
def main():
    print("# Framework Check Report — Posts 5-9\n")

    all_results = []

    for filepath in POST_FILES:
        if not os.path.exists(filepath):
            print(f"## Post: {os.path.basename(filepath)}\n⚠️ **File not found**\n---\n")
            continue

        with open(filepath, 'r', encoding='utf-8') as f:
            post = json.load(f)

        slug = post['slug']
        title = post['title']
        tags = post.get('tags', [])
        is_bengali = any(ord(c) > 127 for c in title)
        content_len = len(post['content'])
        lang = "BENGALI" if is_bengali else "ENGLISH"

        print(f"## Post: {slug}")
        print(f"**Title:** {title}")
        print(f"**Language:** {lang}")
        print(f"**Tags:** {', '.join(tags)}")
        print(f"**Content Length:** {content_len:,} chars")
        print()

        # Run all checks
        tfidf = check_tfidf(post)
        entities = check_entities(post)
        pillar = check_pillar(post)
        aeo = check_aeo_geo(post)
        internal = check_internal_links(post)
        schema = check_schema(post)
        bn_aeo = check_bengali_aeo(post)

        results = {
            'slug': slug,
            'tfidf': tfidf,
            'entities': entities,
            'pillar': pillar,
            'aeo': aeo,
            'internal': internal,
            'schema': schema,
            'bn_aeo': bn_aeo,
        }
        all_results.append(results)

        # Print table
        print("| Check | Status | Details |")
        print("|-------|--------|---------|")

        # A. TF-IDF
        tfidf_icon = "✅" if tfidf['pass'] else "❌"
        print(f"| A. TF-IDF Coverage | {tfidf_icon} | Keyword `{tfidf['keyword']}` — {tfidf['count']} occurrences (need ≥5) |")

        # B. Entities
        ent_icon = "✅" if entities['pass'] else "❌"
        missing_str = ", ".join(entities['missing']) if entities['missing'] else "None"
        print(f"| B. Entity Coverage | {ent_icon} | Missing: {missing_str} |")

        # C. Pillar link
        pillar_icon = "✅" if pillar['pass'] else "❌"
        found_str = ", ".join(pillar['found_pillars'])
        print(f"| C. Pillar Link | {pillar_icon} | Found: {found_str} |")

        # D. AEO/GEO
        aeo_icon = "✅" if aeo['pass'] else "❌"
        examples = "; ".join(aeo['question_examples'][:3]) if aeo['question_examples'] else "none"
        print(f"| D. AEO/GEO | {aeo_icon} | {aeo['question_headings']}/{aeo['total_headings']} question headings. E.g.: {examples[:100]} |")

        # E. Internal Links
        il_icon = "✅" if internal['pass'] else "❌"
        print(f"| E. Internal Links | {il_icon} | {internal['total_unique']} unique (blog:{internal['blog']} svc:{internal['services']} loc:{internal['locations']} ind:{internal['industries']}) — need ≥3 |")

        # F. Schema
        schema_icon = "✅" if schema['pass'] else "❌"
        schema_detail = f"Missing: {', '.join(schema['missing'])}" if schema['missing'] else "All set"
        if not schema['dateModified']:
            schema_detail += " | dateModified: empty"
        print(f"| F. Schema Readiness | {schema_icon} | {schema_detail} |")

        # G. Bengali AEO
        if is_bengali:
            bn_icon = "✅" if bn_aeo['pass'] else "❌"
            qh_list = "; ".join(bn_aeo.get('q_in_headings', [])[:3]) if bn_aeo.get('q_in_headings') else "none"
            print(f"| G. Bengali Q-Words | {bn_icon} | {bn_aeo.get('bengali_q_words_found', 0)} unique Q-words, {len(bn_aeo.get('q_in_headings', []))} in headings. E.g.: {qh_list[:100]} |")

        print()

        # Fix instructions
        print("### Fix Instructions:")
        fixes = []

        if not tfidf['pass']:
            fixes.append(f"- **TF-IDF too thin**: Keyword `{tfidf['keyword']}` only appears {tfidf['count']} times (need 5+). Add more natural mentions.")
        if not entities['pass']:
            fixes.append(f"- **Missing entities**: Add references to: {', '.join(entities['missing'])}")
        if not pillar['pass']:
            fixes.append(f"- **No pillar link**: Add link to `/blog/seo-structured-data-guide-bd` or `/services/technical-seo`")
        if not aeo['pass']:
            fixes.append(f"- **Too few question headings**: Only {aeo['question_headings']} found (need ≥2). Add How/What/Why/Ken/Ki/Kivabe headings.")
        if not internal['pass']:
            fixes.append(f"- **Too few internal links**: Only {internal['total_unique']} unique (need ≥3). Link to related posts/services.")
        if not schema['pass']:
            fixes.append(f"- **Schema fields missing**: Set: {', '.join(schema['missing'])}")
        if is_bengali and not bn_aeo['pass']:
            fixes.append(f"- **Bengali AEO weak**: Use more Bengali question words (কী, কেন, কিভাবে, কখন, কোথায়) in headings.")

        if fixes:
            for f in fixes:
                print(f)
        else:
            print("✅ All checks passed — no fixes needed.")

        print()
        print("---")
        print()

    # ─── Executive Summary ────────────────────────────────────────────────
    print("# Executive Summary\n")

    total = len(all_results)
    tfidf_pass = sum(1 for r in all_results if r['tfidf']['pass'])
    ent_pass = sum(1 for r in all_results if r['entities']['pass'])
    pillar_pass = sum(1 for r in all_results if r['pillar']['pass'])
    aeo_pass = sum(1 for r in all_results if r['aeo']['pass'])
    il_pass = sum(1 for r in all_results if r['internal']['pass'])
    schema_pass = sum(1 for r in all_results if r['schema']['pass'])
    bn_pass = sum(1 for r in all_results if 'bn_aeo' in r and r['bn_aeo']['pass'])

    all_pass = sum(1 for r in all_results if all([
        r['tfidf']['pass'],
        r['entities']['pass'],
        r['pillar']['pass'],
        r['aeo']['pass'],
        r['internal']['pass'],
        r['schema']['pass'],
        ('bn_aeo' in r and r['bn_aeo']['pass']) or (r not in all_results or ('bn_aeo' in r and r['bn_aeo']['pass']) or ('bn_aeo' not in r))
    ]))

    # Simpler: count all_6_pass
    all_6_pass = sum(1 for r in all_results if all([
        r['tfidf']['pass'],
        r['entities']['pass'],
        r['pillar']['pass'],
        r['aeo']['pass'],
        r['internal']['pass'],
        r['schema']['pass'],
    ]))

    print(f"- **Posts checked:** {total}")
    print(f"- **All 6 checks passed:** {all_6_pass}/{total}")
    print()
    print("| Check | Pass Rate |")
    print("|-------|-----------|")
    print(f"| A. TF-IDF Coverage | {tfidf_pass}/{total} |")
    print(f"| B. Entity Coverage | {ent_pass}/{total} |")
    print(f"| C. Pillar Link | {pillar_pass}/{total} |")
    print(f"| D. AEO/GEO | {aeo_pass}/{total} |")
    print(f"| E. Internal Links | {il_pass}/{total} |")
    print(f"| F. Schema Readiness | {schema_pass}/{total} |")
    if bn_pass > 0:
        print(f"| G. Bengali Q-Words | {bn_pass}/{total} |")
    print()
    print("### Failing posts:")
    for r in all_results:
        passed_checks = [
            r['tfidf']['pass'],
            r['entities']['pass'],
            r['pillar']['pass'],
            r['aeo']['pass'],
            r['internal']['pass'],
            r['schema']['pass'],
        ]
        failed_checks = []
        if not r['tfidf']['pass']:
            failed_checks.append('TF-IDF')
        if not r['entities']['pass']:
            failed_checks.append('Entities')
        if not r['pillar']['pass']:
            failed_checks.append('Pillar')
        if not r['aeo']['pass']:
            failed_checks.append('AEO')
        if not r['internal']['pass']:
            failed_checks.append('InternalLinks')
        if not r['schema']['pass']:
            failed_checks.append('Schema')
        if failed_checks:
            print(f"- **{r['slug']}**: FAIL on {', '.join(failed_checks)}")

    print()
    print("---")
    print("*Report generated by Hermes Agent framework checker*")


if __name__ == '__main__':
    main()
