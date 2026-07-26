#!/usr/bin/env python3
"""Generate clean, actionable framework report."""
import json, re

with open('/tmp/framework_raw.json', 'r') as f:
    data = json.load(f)

# Bengali question words to also check
BENGALI_QUESTION_WORDS = ['কীভাবে', 'কেন', 'কী', 'কখন', 'কোথায়', 'কোন', 'কে', 'কার', 'কিসের']

real_issues = []

for p in data['posts']:
    c = p['checks']
    slug = p['slug']
    title = p.get('title', '')
    flags = []

    # TF-IDF: skip if title has no meaningful keyword (stop-word only extraction)
    tf = c['tfidf']
    kw = tf['keyword']
    if not tf['pass']:
        # Only flag if the keyword has at least one substantive word
        substantive = [w for w in kw.split() if len(w) > 3]
        if substantive:
            flags.append(('**TF-IDF**', f'Keyword "{kw}" only {tf["effective_count"]} occurrences'))

    # Entities
    en = c['entities']
    if not en['pass']:
        flags.append(('**Entities**', f'Missing: {", ".join(en["missing"])}'))

    # Pillar
    pl = c['pillar']
    if not pl['pass'] and pl['pillar_url'] and not pl['has_link'] and not pl.get('note'):
        flags.append(('**Pillar Link**', f'Missing link to `{pl["pillar_url"]}`'))

    # AEO/GEO - check for Bengali question headings too
    aeo = c['aeo']
    aeo_pass = aeo['pass']
    if not aeo_pass:
        # Quick re-check for Bengali headings from raw content
        # We already have the fail from English-only check
        # If the post is Bengali, note that it may have Bengali question headings
        is_bengali = bool(re.search(r'[\u0980-\u09FF]', title))
        detail = f'Only {aeo["count"]} English question headings'
        if is_bengali:
            detail += ' — check for Bengali question headings (কীভাবে/কেন/কী)'
        flags.append(('**AEO/GEO**', detail))

    # Internal Links
    il = c['internal_links']
    if not il['pass']:
        flags.append(('**Internal Links**', f'Only {il["total"]} internal links'))

    # Schema
    sc = c['schema']
    if not sc['pass']:
        critical_missing = [m for m in sc['missing'] if m in ('title', 'excerpt', 'date', 'author')]
        if critical_missing:
            flags.append(('**Schema**', f'Missing critical fields: {", ".join(critical_missing)}'))

    if flags:
        real_issues.append((slug, title, flags))

print('# Blog Content Framework Report — kanokmiah.com.bd')
print(f'**Total posts scanned:** {data["total"]}')
print(f'**Posts with issues:** {len(real_issues)}')
print(f'**All-clear posts:** {data["total"] - len(real_issues)}')
print()

if not real_issues:
    print('✅ All posts pass all framework checks!')
else:
    # Summary table
    print('## Summary')
    print()
    print('| Issue Type | Count |')
    print('|------------|-------|')
    issue_counts = {}
    for _, _, flags in real_issues:
        for ftype, _ in flags:
            issue_counts[ftype] = issue_counts.get(ftype, 0) + 1
    for ftype, count in sorted(issue_counts.items(), key=lambda x: -x[1]):
        print(f'| {ftype} | {count} |')
    print()

    # Details
    print('## Details')
    print()
    for slug, title, flags in real_issues:
        print(f'### {slug}')
        print(f'_{title}_')
        print()
        for ftype, detail in flags:
            print(f'- {ftype}: {detail}')
        print()
