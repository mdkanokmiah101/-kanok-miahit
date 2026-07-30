#!/usr/bin/env python3
"""Generate the final formatted report with fix instructions."""
import json

with open('/root/kanok-miahit/content_framework_report.json') as f:
    results = json.load(f)

edge_case_notes = {
    'landlord-certificates-seo-case-study': (
        'Note: UK-based case study; Bangladesh entity requirement may not apply. '
        'Keyword extraction heuristic chose "All Landlord" from the title — manually verify appropriate keyword.'
    ),
    'morethanpanel-seo-case-study': (
        'Note: "MoreThanPanel SEO" is a composite of brand+service; the brand "MoreThanPanel" appears frequently '
        'in content but the exact joined phrase "MoreThanPanel SEO" does not. Use "MoreThanPanel" as keyword instead.'
    ),
    'smmgen-seo-case-study': (
        'Note: Same brand-phrase issue as above. "SMMGen" (brand) appears in content but "SMMGen SEO" as joined phrase does not.'
    ),
    'smmsun-seo-case-study': (
        'Note: Same brand-phrase issue as above. "SMMSun" (brand) appears in content but "SMMSun SEO" as joined phrase does not.'
    ),
    'watchzonebd-seo-case-study': (
        'Note: Same brand-phrase issue. "WatchZoneBD" (brand) appears 27x in content but "WatchZoneBD SEO" as joined phrase does not.'
    ),
    'top-10-seo-mistakes-dhaka-businesses-fix': (
        'Note: Keyword "Top" was extracted from "Top 10 SEO Mistakes...". Manually review: "SEO Mistakes" would be more semantically appropriate.'
    ),
    'hiring-seo-expert-dhaka-better-roi-than-paid-ads': (
        'Note: Keyword "Hiring" from title "Hiring an SEO Expert..." — consider using "SEO Expert" or "SEO ROI" as primary keyword instead.'
    ),
    'stealth-windshield-repairs-seo-case-study': (
        'Note: "Stealth Windshield" appears 2x in body but brand "Stealth Windshield Repairs" appears consistently. This is a UK/US case study so Dhaka/Bangladesh references are sparse.'
    ),
    'das-taxis-scotland-seo-case-study': (
        'Note: UK-based case study (Scotland). "Das Taxis" brand appears at beginning/end of content.'
    ),
    'dhaka-apparels-seo-case-study': (
        'Note: "Dhaka Apparels" appears 3x. Brand name naturally appears less in narrative case study format.'
    ),
    'mir-cement-seo-case-study': (
        'Note: "Mir Cement" appears 3x. Brand name appears naturally in case study context.'
    ),
}


report_sections = []
report_sections.append("""# KanokMiah.com.bd — Content Framework Enforcement Report

**Period:** Last 48 hours  
**Posts changed:** 22  
**Generated:** Automated cron check  
**Scope:** TF-IDF, Entity Coverage, Pillar Alignment, AEO/GEO, Internal Links, Schema Readiness
""")

for r in results:
    slug = r['slug']
    checks = r.get('checks', {})
    
    report_sections.append(f"## Post: `{slug}`")
    
    if 'error' in r:
        report_sections.append(f"**ERROR:** Could not extract post object for analysis.")
        continue
    
    report_sections.append("| Check | Status | Details |")
    report_sections.append("|-------|--------|---------|")
    
    tfidf = checks.get('tfidf', {})
    t_status = '✅' if tfidf.get('pass') else '❌'
    t_detail = f"Keyword '{tfidf.get('keyword', '')}' appears {tfidf.get('occurrences', 0)}x"
    if not tfidf.get('pass'):
        t_detail += ' (minimum 5 required)'
    report_sections.append(f"| TF-IDF Coverage | {t_status} | {t_detail} |")
    
    ent = checks.get('entities', {})
    e_status = '✅' if ent.get('pass') else '❌'
    if ent.get('pass'):
        e_detail = f"Found: {', '.join(ent.get('present', [])[:6])}"
    else:
        e_detail = f"Missing: {', '.join(ent.get('missing', []))}"
    report_sections.append(f"| Semantic Entities | {e_status} | {e_detail} |")
    
    pil = checks.get('pillar', {})
    p_status = '✅' if pil.get('pass') else '❌'
    if pil.get('pass'):
        p_detail = f"Links to pillar: {pil.get('pillar_url', '')}"
    else:
        p_detail = f"Missing (tags: {', '.join(pil.get('tags', [])[:4])})"
    report_sections.append(f"| Pillar Page Link | {p_status} | {p_detail} |")
    
    aeo = checks.get('aeo_geo', {})
    a_status = '✅' if aeo.get('pass') else '❌'
    a_detail = f"{aeo.get('question_headings', 0)} question heading(s)"
    if not aeo.get('pass'):
        a_detail += ' (minimum 2 required)'
    report_sections.append(f"| AEO/GEO (Q-Headings) | {a_status} | {a_detail} |")
    
    il = checks.get('internal_links', {})
    i_status = '✅' if il.get('pass') else '❌'
    i_detail = f"{il.get('count', 0)} internal link(s)"
    if not il.get('pass'):
        i_detail += ' (minimum 3 required)'
    report_sections.append(f"| Internal Links | {i_status} | {i_detail} |")
    
    sc = checks.get('schema', {})
    s_status = '✅' if sc.get('pass') else '❌'
    s_detail = 'All set (title, excerpt, date)' if sc.get('pass') else f"Missing: {', '.join(sc.get('missing_fields', []))}"
    report_sections.append(f"| Schema Ready | {s_status} | {s_detail} |")
    
    # Fix instructions
    fixes = []
    
    if not tfidf.get('pass'):
        kw = tfidf.get('keyword', '')
        occ = tfidf.get('occurrences', 0)
        fixes.append(f"- Increase keyword density for '{kw}': currently {occ} occurrences, target ≥5. Add in headings, introduction, and body.")
    
    if not ent.get('pass'):
        for missing in ent.get('missing', []):
            fixes.append(f"- Add entity: {missing}")
    
    if not pil.get('pass'):
        tags = pil.get('tags', [])
        tag_map = {
            'Link Building': '/blog/link-building-strategies-bangladesh-market',
            'Local SEO': '/blog/local-seo-tips-dhaka-businesses-google-maps',
            'Technical SEO': '/blog/technical-seo-checklist-bangladeshi-websites',
            'E-commerce SEO': '/blog/why-ecommerce-store-needs-seo-bangladesh',
            'Ecommerce SEO': '/blog/why-ecommerce-store-needs-seo-bangladesh',
            'SEO Guide': '/blog/complete-seo-guide-bangladesh-businesses-2026',
            'Google Business Profile': '/blog/google-business-profile-optimization-guide-bangladesh',
            'Mobile SEO': '/blog/mobile-seo-optimization-bangladesh-mobile-first-era',
            'Content Marketing': '/blog/seo-content-writing-strategy-guide-bangladesh',
            'GEO/AEO': '/blog/geo-aeo-optimization-bangladesh',
            'B2B SEO': '/blog/seo-garments-textile-industry-b2b-lead-generation',
        }
        suggested = ''
        for tag in tags:
            if tag in tag_map:
                suggested = tag_map[tag]
                break
        if suggested:
            fixes.append(f"- Add pillar link → {suggested}")
        else:
            fixes.append(f"- Add pillar link relevant to tags: {', '.join(tags[:3])}")
    
    if not aeo.get('pass'):
        qh = aeo.get('question_headings', 0)
        need = 2 - qh
        fixes.append(f"- Add {need} more question-based heading(s) (##/### starting with How/What/Why/Can/Do/Is/Are) for AEO/GEO optimization")
    
    if not il.get('pass'):
        cnt = il.get('count', 0)
        need = 3 - cnt
        fixes.append(f"- Add {need} more internal link(s) to related blog/service/location pages")
    
    if not sc.get('pass'):
        for field in sc.get('missing_fields', []):
            fixes.append(f"- Set '{field}' in post metadata")
    
    if fixes:
        report_sections.append("")
        report_sections.append("**Fix instructions:**")
        for fix in fixes:
            report_sections.append(fix)
    
    # Edge case notes
    if slug in edge_case_notes:
        report_sections.append(f"\n*{edge_case_notes[slug]}*")
    
    report_sections.append("")

# Summary
passed = sum(1 for r in results if 'error' not in r and all(c.get('pass', False) for c in r.get('checks', {}).values()))
total = len(results)

report_sections.append(f"---")
report_sections.append(f"## Summary")
report_sections.append(f"")
report_sections.append(f"**{passed}/{total} posts pass all 6 checks.** (2 posts: `google-business-profile-optimization-guide-bangladesh`, `mobile-seo-optimization-bangladesh-mobile-first-era`)")
report_sections.append(f"")

if passed < total:
    report_sections.append("### Posts needing action:")
    
    # Group by failure type
    by_type = {}
    for r in results:
        if 'error' in r:
            continue
        checks = r.get('checks', {})
        failing = [name for name, c in checks.items() if not c.get('pass', False)]
        for f in failing:
            by_type.setdefault(f, []).append(r['slug'])
    
    for check_name, slugs in sorted(by_type.items()):
        labels = {
            'tfidf': 'TF-IDF (thin keyword density)',
            'entities': 'Missing entities',
            'pillar': 'Missing pillar link',
            'aeo_geo': 'Too few question headings',
            'internal_links': 'Too few internal links',
            'schema': 'Schema fields missing',
        }
        label = labels.get(check_name, check_name)
        report_sections.append(f"- **{label}** ({len(slugs)} posts):")
        report_sections.append(f"  - {', '.join(f'`{s}`' for s in slugs)}")
    
    report_sections.append("")
    report_sections.append("### Key patterns:")
    report_sections.append("1. **Pillar links missing** (16 posts): Many case studies and service-guide posts lack links to their parent pillar page. This is the most common gap.")
    report_sections.append("2. **AEO/GEO question headings missing** (11 posts): Case studies (format: Project Snapshot → Challenge → Strategy → Results) don't use question headings. Add FAQ-style ## headings.")
    report_sections.append("3. **TF-IDF thin** (10 posts): Case studies with brand names as keywords show low occurrence counts. Consider using the brand name more consistently in headings.")
    report_sections.append("4. **Entity gaps** (1 post): `landlord-certificates` is a UK case study — Bangladesh entity gap may be acceptable.")

print('\n'.join(report_sections))
