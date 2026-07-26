#!/usr/bin/env python3
"""Process framework check results and generate report."""
import json

with open('/tmp/framework_raw.json', 'r') as f:
    data = json.load(f)

report_lines = []
report_lines.append('# Blog Content Framework Report — kanokmiah.com.bd')
report_lines.append(f'**Scanned:** {data["total"]} posts')
report_lines.append(f'**Posts with issues:** {data["failures"]}')
report_lines.append('')

# Find failed posts
failed = []
for p in data['posts']:
    c = p['checks']
    issues = {}
    for check_name in ['tfidf', 'entities', 'pillar', 'aeo', 'internal_links', 'schema']:
        if not c[check_name]['pass']:
            issues[check_name] = c[check_name]
    if issues:
        failed.append((p, issues))

if not failed:
    report_lines.append('✅ All posts pass all framework checks!')
else:
    for post, issues in failed:
        c = post['checks']
        slug = post['slug']
        title = post.get('title', '')
        report_lines.append(f'## Post: {slug}')
        report_lines.append(f'**Title:** {title}')
        report_lines.append('')
        report_lines.append('| Check | Status | Details |')
        report_lines.append('|-------|--------|---------|')

        tf = c['tfidf']
        tf_status = '✅' if tf['pass'] else '❌'
        report_lines.append(f'| TF-IDF | {tf_status} | Keyword: "{tf["keyword"]}" — {tf["effective_count"]} occurrences |')

        en = c['entities']
        en_status = '✅' if en['pass'] else '❌'
        missing_str = ', '.join(en['missing']) if en['missing'] else 'None'
        report_lines.append(f'| Entities | {en_status} | Service: {en["service_detected"]}, Industry: {en["industry_detected"]} | Missing: {missing_str} |')

        pl = c['pillar']
        pl_status = '✅' if pl['pass'] else '❌'
        pl_detail = f'Pillar: {pl["pillar_name"] or "None"}'
        if pl.get('note'):
            pl_detail += f' ({pl["note"]})'
        elif pl['pillar_url'] and not pl['has_link']:
            pl_detail += f' | Missing link: {pl["pillar_url"]}'
        elif not pl['pillar_url']:
            pl_detail += ' | No pillar mapping'
        report_lines.append(f'| Pillar Link | {pl_status} | {pl_detail} |')

        aeo = c['aeo']
        aeo_status = '✅' if aeo['pass'] else '❌'
        report_lines.append(f'| AEO/GEO | {aeo_status} | {aeo["count"]} question headings |')

        il = c['internal_links']
        il_status = '✅' if il['pass'] else '❌'
        report_lines.append(f'| Internal Links | {il_status} | {il["total"]} total ({il["blog_links"]} blog, {il["non_blog_links"]} other) |')

        sc = c['schema']
        sc_status = '✅' if sc['pass'] else '❌'
        sc_missing = ', '.join(sc['missing']) if sc['missing'] else 'All fields set'
        report_lines.append(f'| Schema Ready | {sc_status} | {sc_missing} |')

        # Fix instructions
        fix_lines = []
        if not tf['pass']:
            fix_lines.append(f'- **TF-IDF**: Increase usage of "{tf["keyword"]}" to ≥5 occurrences')
        if not en['pass']:
            fix_lines.append(f'- **Entities**: Add: {", ".join(en["missing"])}')
        if not pl['pass'] and pl.get('pillar_url') and not pl['has_link']:
            fix_lines.append(f'- **Pillar Link**: Link to `{pl["pillar_url"]}`')
        if not aeo['pass']:
            fix_lines.append('- **AEO/GEO**: Add ≥2 question headings (How/What/Why/...)')
        if not il['pass']:
            fix_lines.append(f'- **Internal Links**: Currently {il["total"]}, need ≥3')
        if not sc['pass']:
            fix_lines.append(f'- **Schema**: Set: {", ".join(sc["missing"])}')

        if fix_lines:
            report_lines.append('')
            report_lines.append('### Fix instructions:')
            report_lines.extend(fix_lines)

        report_lines.append('')

print('\n'.join(report_lines))
