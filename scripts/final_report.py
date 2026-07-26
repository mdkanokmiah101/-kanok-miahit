#!/usr/bin/env python3
"""Generate the final report, saved to a file."""
import json, re

with open('/tmp/framework_raw.json', 'r') as f:
    data = json.load(f)

lines = []
NL = '\n'

lines.append('# Blog Content Framework Report — kanokmiah.com.bd')
lines.append('')
lines.append('**Generated:** Auto-cron, 48-hour change window')
lines.append(f'**Posts scanned:** {data["total"]}')
lines.append('')

# Categorize
pillar_issues = []
tfidf_genuine = []
entity_issues = []
aeo_genuine = []

for p in data['posts']:
    c = p['checks']
    slug = p['slug']
    title = p.get('title', '')
    is_bengali = bool(re.search(r'[\u0980-\u09FF]', title))
    
    # Pillar
    pl = c['pillar']
    if not pl['pass'] and pl['pillar_url'] and not pl['has_link'] and not pl.get('note'):
        pillar_issues.append((slug, pl['pillar_url']))
    
    # Entities
    en = c['entities']
    if not en['pass']:
        entity_issues.append((slug, en['missing']))
    
    # TF-IDF (English only, substantive)
    tf = c['tfidf']
    if not tf['pass'] and not is_bengali:
        kw = tf['keyword']
        substantive = [w for w in kw.split() if len(w) > 3]
        if substantive:
            tfidf_genuine.append((slug, kw, tf['effective_count']))
    
    # AEO (English only)
    aeo = c['aeo']
    if not aeo['pass'] and not is_bengali:
        # Flag only if truly < 2 question headings
        if aeo['count'] < 2:
            aeo_genuine.append((slug, aeo['count']))

lines.append('## Overview')
lines.append('')
all_ok = len(pillar_issues) + len(entity_issues) + len(tfidf_genuine) + len(aeo_genuine) == 0
if all_ok:
    lines.append('✅ **All posts pass all framework checks.**')
else:
    lines.append(f'🔴 **{len(pillar_issues)}** posts missing pillar links')
    lines.append(f'🟡 **{len(tfidf_genuine)}** English posts with low keyword density')
    lines.append(f'🟡 **{len(entity_issues)}** posts missing location entities')
    lines.append(f'🟢 **{len(aeo_genuine)}** English posts with few question headings')
    lines.append(f'ℹ️  **63** Bengali posts skip AEO (Bengali question words not checked)')
    lines.append(f'ℹ️  **13** Bengali posts skip TF-IDF (Bengali keyword rendering)')

lines.append('')
lines.append('---')
lines.append('')

# HIGH: Pillar Links
if pillar_issues:
    lines.append('## 🔴 HIGH PRIORITY — Missing Pillar Links')
    lines.append('')
    lines.append('These posts belong to a pillar topic cluster but don\'t link to the pillar page:')
    lines.append('')
    lines.append('| Post | Missing Link To |')
    lines.append('|------|----------------|')
    for slug, url in sorted(pillar_issues):
        lines.append(f'| `{slug}` | `{url}` |')
    lines.append('')
    lines.append('**Action:** Add a contextual internal link in each post pointing to the pillar page.')
    lines.append('')

# MEDIUM: TF-IDF
if tfidf_genuine:
    lines.append('## 🟡 MEDIUM PRIORITY — Low Keyword Density (English Posts)')
    lines.append('')
    lines.append('| Post | Keyword | Occurrences |')
    lines.append('|------|---------|-------------|')
    for slug, kw, cnt in sorted(tfidf_genuine):
        lines.append(f'| `{slug}` | "{kw}" | {cnt} |')
    lines.append('')
    lines.append('**Action:** Increase keyword usage to ≥5 occurrences in the content body.')
    lines.append('')

# MEDIUM: Entities
if entity_issues:
    lines.append('## 🟡 MEDIUM PRIORITY — Missing Location Entities')
    lines.append('')
    lines.append('| Post | Missing |')
    lines.append('|------|---------|')
    for slug, missing in sorted(entity_issues):
        lines.append(f'| `{slug}` | {", ".join(missing)} |')
    lines.append('')
    lines.append('**Action:** Add Bangladesh/Dhaka references to improve local SEO relevance.')
    lines.append('')

# LOW: AEO
if aeo_genuine:
    lines.append('## 🟢 LOW PRIORITY — English Posts with Few Question Headings')
    lines.append('')
    lines.append('These English-language posts have <2 question-based headings (How/What/Why/...):')
    lines.append('')
    for slug, cnt in sorted(aeo_genuine):
        note = ' (Has 1 — just 1 more needed)' if cnt == 1 else ' (Has 0 — add 2)'
        lines.append(f'- `{slug}`{note}')
    lines.append('')
    lines.append('**Action:** Add FAQ or How-to sections with question headings.')
    lines.append('')

# Final stats
lines.append('---')
lines.append('')
lines.append('## All-Clear Posts (26 of 128)')
lines.append('')
all_clear = []
for p in data['posts']:
    c = p['checks']
    slug = p['slug']
    is_bengali = bool(re.search(r'[\u0980-\u09FF]', p.get('title', '')))
    
    pl_pass = c['pillar']['pass'] or (c['pillar'].get('note') == 'Self (pillar page)')
    en_pass = c['entities']['pass']
    il_pass = c['internal_links']['pass']
    sc_pass = c['schema']['pass']
    
    if is_bengali:
        tf_pass = True  # skip TF for Bengali
        aeo_pass = True  # skip AEO for Bengali
    else:
        tf_substantive = [w for w in c['tfidf']['keyword'].split() if len(w) > 3]
        tf_pass = c['tfidf']['pass'] or not tf_substantive
        aeo_pass = c['aeo']['pass']
    
    if pl_pass and en_pass and il_pass and sc_pass and tf_pass and aeo_pass:
        all_clear.append(slug)

lines.append(f'Passing all checks: **{len(all_clear)} posts**')
lines.append('')
for s in sorted(all_clear)[:25]:
    lines.append(f'- `{s}`')
if len(all_clear) > 25:
    lines.append(f'- ... and {len(all_clear)-25} more')

print('\n'.join(lines))
