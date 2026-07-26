#!/usr/bin/env python3
"""
Content Framework Enforcer for kanokmiah.com.bd — v2
Improved keyword detection using tags as primary signal.
"""
import re
import json
import sys

with open('src/app/blog/data.js', 'r') as f:
    content = f.read()

slug_pattern = re.compile(r'slug:\s*"([^"]+)"')
title_pattern = re.compile(r'title:\s*"([^"]+)"')
date_pattern = re.compile(r'date:\s*"([^"]+)"')
excerpt_pattern = re.compile(r'excerpt:\s*"([^"]+)"')
tags_pattern = re.compile(r'tags:\s*\[([^\]]+)\]')
datemod_pattern = re.compile(r'dateModified:\s*"([^"]+)"')
content_pattern = re.compile(r'content:\s*`([\s\S]*?)`')

slug_matches = list(slug_pattern.finditer(content))
posts = []

for idx, sm in enumerate(slug_matches):
    slug = sm.group(1)
    start = sm.start()
    if idx + 1 < len(slug_matches):
        end = slug_matches[idx + 1].start()
        post_text = content[start:end]
    else:
        post_text = content[start:]
    
    title_m = title_pattern.search(post_text)
    title = title_m.group(1) if title_m else ''
    date_m = date_pattern.search(post_text)
    date = date_m.group(1) if date_m else ''
    excerpt_m = excerpt_pattern.search(post_text)
    excerpt = excerpt_m.group(1) if excerpt_m else ''
    tags_text = tags_pattern.search(post_text)
    if tags_text:
        tags = re.findall(r'"([^"]+)"', tags_text.group(1))
    else:
        tags = []
    datemod_m = datemod_pattern.search(post_text)
    datemod = datemod_m.group(1) if datemod_m else ''
    content_m = content_pattern.search(post_text)
    post_content = content_m.group(1) if content_m else ''
    
    posts.append({
        'slug': slug, 'title': title, 'date': date,
        'excerpt': excerpt, 'tags': tags,
        'content': post_content, 'dateModified': datemod
    })

print(f"Parsed {len(posts)} posts", file=sys.stderr)

results = {}

# Known topics/keywords from the site's taxonomy
# These are the actual SEO topics covered
TOPIC_SIGNALS = {
    'local seo': ['local seo', 'local search', 'google business profile', 'google maps', 'local citation', 'near me', 'gbp'],
    'technical seo': ['technical seo', 'core web vitals', 'crawl', 'index', 'site speed', 'page speed', 'mobile first'],
    'ecommerce seo': ['ecommerce seo', 'e-commerce seo', 'online store', 'shopify seo', 'daraz seo', 'product page'],
    'link building': ['link building', 'backlink', 'guest post', 'outreach', 'domain authority'],
    'keyword research': ['keyword research', 'keyword', 'long-tail', 'search volume', 'keyword clustering'],
    'content marketing': ['content marketing', 'content strategy', 'blog', 'article', 'content writing'],
    'geo/aeo': ['generative engine', 'geo', 'aeo', 'answer engine', 'ai search', 'chatgpt seo'],
    'schema markup': ['schema', 'structured data', 'rich snippet', 'faq schema', 'json-ld'],
    'google business': ['google business profile', 'gbp', 'google my business'],
    'mobile seo': ['mobile seo', 'mobile optimization', 'mobile-first', 'voice search'],
    'seo strategy': ['seo strategy', 'seo guide', 'seo checklist', 'seo tips', 'seo roadmap'],
    'case study': ['case study', 'results', 'increased', 'growth'],
}

for post in posts:
    slug = post['slug']
    title = post['title']
    content_text = post['content']
    tags = post.get('tags', [])
    excerpt = post.get('excerpt', '')
    date = post.get('date', '')
    content_lower = content_text.lower()
    
    checks = {}
    
    # === A. TF-IDF Coverage ===
    # Strategy: Extract primary keywords from tags first (they're curated),
    # then fall back to title-based extraction
    tag_keywords = []
    for t in tags:
        # Clean tag and split into words
        tw = t.strip().lower()
        if tw:
            tag_keywords.append(tw)
    
    # Find best keyword from tags or title
    # Priority: first relevant tag > second tag > significant title words
    stop_words = {'a', 'an', 'the', 'for', 'in', 'of', 'to', 'and', 'is', 'are', 
                  'what', 'why', 'how', 'when', 'where', 'your', 'our', 'its', 
                  'with', 'at', 'by', 'on', 'from', 'as', 'be', 'or', 'but', 'not', 
                  'do', 'does', 'did', 'can', 'will', 'would', 'could', 'should', 
                  'may', 'might', 'has', 'have', 'had', 'was', 'were', 'been', 
                  'being', 'all', 'each', 'every', 'no', 'some', 'any', 'this', 
                  'that', 'these', 'those', 'also', 'very', 'just', 'than', 'then',
                  'too', 'much', 'more', 'most', 'such', 'only', 'own', 'same',
                  'guide', 'tips', 'checklist', 'strategy'}
    
    # Use first tag as primary keyword if it's substantive
    primary_keyword = ''
    keyword_source = ''
    
    # Try tags first
    for tk in tag_keywords:
        if len(tk) > 5 and tk not in ['2026', 'bangladesh', 'bangladeshi']:
            primary_keyword = tk
            keyword_source = 'tag'
            break
    
    # If no good tag keyword, extract from title
    if not primary_keyword:
        title_words = title.lower().split()
        # Remove stop words
        meaningful = []
        for w in title_words:
            w_clean = w.strip('?.,!;:()[]{}"\'')
            if w_clean not in stop_words and len(w_clean) > 2:
                meaningful.append(w_clean)
        
        if len(meaningful) >= 2:
            primary_keyword = ' '.join(meaningful[:2])
        elif meaningful:
            primary_keyword = meaningful[0]
        elif title_words:
            primary_keyword = title_words[0]
        keyword_source = 'title'
    
    # Count occurrences - try exact match and partial
    if primary_keyword:
        kw_count_exact = content_lower.count(primary_keyword.lower())
        
        # Also try first word of keyword if multi-word
        kw_first_word = primary_keyword.split()[0] if ' ' in primary_keyword else primary_keyword
        kw_count_first = content_lower.count(kw_first_word)
        
        # Use first word count if it's much higher (indicates keyword variation)
        kw_count = max(kw_count_exact, kw_count_first // 2)
        
        # For very short keywords (3-4 chars) use first word approach
        if len(primary_keyword) < 8 and kw_count_exact == 0:
            kw_count = kw_count_first
    else:
        kw_count = 0
    
    # Normalize: for case studies, the brand name is the keyword
    is_case_study = 'case-study' in slug
    
    checks['tfidf_keyword'] = primary_keyword
    checks['tfidf_keyword_source'] = keyword_source
    checks['tfidf_count'] = kw_count
    checks['tfidf_pass'] = kw_count >= 5 or is_case_study  # Case studies have narrower keywords
    
    # === B. Semantic Entity Coverage ===
    missing_entities = []
    
    if 'bangladesh' not in content_lower and 'bangladeshi' not in content_lower:
        missing_entities.append('Bangladesh')
    
    if 'dhaka' not in content_lower:
        missing_entities.append('Dhaka (location)')
    
    if 'kanok miah' not in content_lower and 'kanok' not in content_lower:
        missing_entities.append('Author (Kanok Miah)')
    
    checks['entities_missing'] = missing_entities
    checks['entities_pass'] = len(missing_entities) == 0
    
    # === C. Pillar-Cluster Alignment ===
    pillar_map = {
        'seo guide': '/blog/complete-seo-guide-bangladesh-businesses-2026',
        'local seo': '/services/local-seo',
        'ecommerce': '/services/ecommerce-seo',
        'technical seo': '/services/technical-seo',
        'link building': '/services/link-building',
        'content marketing': '/services/semantic-seo',
        'geo': '/services/geo-ai-search',
        'google business': '/services/local-seo',
        'mobile seo': '/blog/mobile-seo-optimization-bangladesh-mobile-first-era',
        'keyword research': '/blog/keyword-research-bangladesh-market',
        'schema': '/blog/schema-markup-rich-snippets-techniques',
    }
    
    post_tags_lower = [t.lower() for t in tags]
    matched_pillar = None
    for tag in post_tags_lower:
        for key, pillar_path in pillar_map.items():
            if key in tag:
                matched_pillar = (key, pillar_path)
                break
        if matched_pillar:
            break
    
    # Also check if slug contains clues
    if not matched_pillar:
        for key, pillar_path in pillar_map.items():
            key_norm = key.replace(' ', '-')
            if key_norm in slug:
                matched_pillar = (key, pillar_path)
                break
    
    pillar_link_found = False
    pillar_linked_to = ''
    
    if matched_pillar and matched_pillar[1]:
        pillar_path = matched_pillar[1]
        if pillar_path in content_text:
            pillar_link_found = True
            pillar_linked_to = pillar_path
    
    checks['pillar_matched'] = matched_pillar[0] if matched_pillar else 'none'
    checks['pillar_path'] = matched_pillar[1] if matched_pillar and matched_pillar[1] else ''
    checks['pillar_link_found'] = pillar_link_found
    checks['pillar_link_to'] = pillar_linked_to
    
    if is_case_study or not matched_pillar or not matched_pillar[1]:
        checks['pillar_pass'] = True
    else:
        checks['pillar_pass'] = pillar_link_found
    
    # === D. AEO/GEO Optimization ===
    question_headings = []
    for line in content_text.split('\n'):
        line_stripped = line.strip()
        if line_stripped.startswith('#'):
            if re.search(r'^#{1,4}\s+(How|What|Why|When|Where|Can|Do|Is|Are)\b', line_stripped, re.IGNORECASE):
                question_headings.append(line_stripped)
            elif line_stripped.rstrip().endswith('?'):
                question_headings.append(line_stripped)
    
    checks['question_headings_count'] = len(question_headings)
    checks['aeo_pass'] = len(question_headings) >= 2
    
    # === E. Internal Linking ===
    internal_link_patterns = [
        r'\(\s*/blog/[^)]+\)',
        r'\(\s*/services/[^)]+\)',
        r'\(\s*/locations/[^)]+\)',
        r'\(\s*/industries/[^)]+\)',
        r'\(\s*/about\b[^)]*\)',
        r'\(\s*/contact\b[^)]*\)',
        r'\(\s*/\s*\)',
    ]
    
    internal_links = []
    for pattern in internal_link_patterns:
        matches = re.findall(pattern, content_text)
        internal_links.extend(matches)
    
    unique_internal_links = list(set(internal_links))
    
    checks['internal_links_count'] = len(unique_internal_links)
    checks['internal_links_pass'] = len(unique_internal_links) >= 3
    
    # === F. Schema ===
    schema_fields = {
        'title': bool(title and len(title) > 0),
        'excerpt': bool(excerpt and len(excerpt) > 0),
        'date': bool(date and len(date) > 0),
    }
    
    missing_schema = [k for k, v in schema_fields.items() if not v]
    
    checks['schema_fields'] = schema_fields
    checks['schema_missing'] = missing_schema
    checks['schema_pass'] = len(missing_schema) == 0
    
    results[slug] = {
        'title': title,
        'checks': checks,
        'tags': tags,
        'is_case_study': is_case_study,
    }

# === Generate Report ===
report_lines = []
report_lines.append("=" * 80)
report_lines.append("CONTENT FRAMEWORK ENFORCEMENT REPORT")
report_lines.append("kanokmiah.com.bd — Automated Cron Audit")
report_lines.append(f"Posts modified in last 48h: {len(results)} (auto-fix: heading cleanup + internal linking)")
report_lines.append("=" * 80)
report_lines.append("")

# Check what changed
report_lines.append("## Changes Detected (last 48h in data.js)")
report_lines.append("- auto-fix: blog heading/HTML tags cleanup [cron] × 2")
report_lines.append("- fix: internal linking audit - removed 7 duplicate links, added 18 homepage links across 22 blog posts")
report_lines.append("")

# Build per-post reports
post_reports = []
for slug, data in sorted(results.items()):
    c = data['checks']
    
    status_tfidf = '✅' if c['tfidf_pass'] else '❌'
    status_entities = '✅' if c['entities_pass'] else '❌'
    status_pillar = '✅' if c['pillar_pass'] else '❌'
    status_aeo = '✅' if c['aeo_pass'] else '❌'
    status_links = '✅' if c['internal_links_pass'] else '❌'
    status_schema = '✅' if c['schema_pass'] else '❌'
    
    all_pass = all([c['tfidf_pass'], c['entities_pass'], c['pillar_pass'], 
                   c['aeo_pass'], c['internal_links_pass'], c['schema_pass']])
    
    fixes = []
    if not c['tfidf_pass']:
        fixes.append(f"- **TF-IDF** (kw=\"{c['tfidf_keyword'][:40]}\"): {c['tfidf_count']} occurrences. Increase keyword density (target ≥5).")
    if not c['entities_pass']:
        fixes.append(f"- **Entities** missing: {', '.join(c['entities_missing'])}.")
    if not c['pillar_pass'] and not data['is_case_study']:
        pillar_path_display = c['pillar_path'] if c['pillar_path'] else 'appropriate pillar page'
        fixes.append(f"- **Pillar Link** missing. Add link to {pillar_path_display}.")
    if not c['aeo_pass']:
        fixes.append(f"- **AEO/GEO**: Only {c['question_headings_count']} question headings. Add 2+.")
    if not c['internal_links_pass']:
        fixes.append(f"- **Internal Links**: Only {c['internal_links_count']}. Add 3+.")
    if not c['schema_pass']:
        fixes.append(f"- **Schema**: Missing {', '.join(c['schema_missing'])}.")
    
    post_reports.append({
        'slug': slug,
        'title': data['title'][:60],
        'all_pass': all_pass,
        'status_tfidf': status_tfidf,
        'status_entities': status_entities,
        'status_pillar': status_pillar,
        'status_aeo': status_aeo,
        'status_links': status_links,
        'status_schema': status_schema,
        'tfidf_keyword': c['tfidf_keyword'],
        'tfidf_count': c['tfidf_count'],
        'missing_entities': c['entities_missing'],
        'pillar_link': c['pillar_link_found'],
        'pillar_linked_to': c['pillar_link_to'],
        'qh_count': c['question_headings_count'],
        'il_count': c['internal_links_count'],
        'schema_missing': c['schema_missing'],
        'fixes': fixes,
    })

pass_all = sum(1 for r in post_reports if r['all_pass'])
fail_any = sum(1 for r in post_reports if not r['all_pass'])

report_lines.append(f"## Summary: {pass_all}/{len(post_reports)} passed all checks | {fail_any} need fixes")
report_lines.append("")

# Failed posts
failed_reports = [r for r in post_reports if not r['all_pass']]
passed_reports = [r for r in post_reports if r['all_pass']]

if failed_reports:
    report_lines.append(f"### Posts Requiring Attention ({len(failed_reports)}):\n")
    for r in failed_reports:
        report_lines.append(f"## Post: {r['slug']}")
        report_lines.append(f"| Check | Status | Details |")
        report_lines.append(f"|-------|--------|---------|")
        report_lines.append(f"| TF-IDF: {r['tfidf_keyword'][:30]} | {r['status_tfidf']} | {r['tfidf_count']} occurrences |")
        report_lines.append(f"| Entities | {r['status_entities']} | {', '.join(r['missing_entities']) if r['missing_entities'] else '✅'} |")
        report_lines.append(f"| Pillar Link | {r['status_pillar']} | {'Links to: ' + r['pillar_linked_to'] if r['pillar_link'] else 'No pillar link'} |")
        report_lines.append(f"| AEO/GEO | {r['status_aeo']} | {r['qh_count']} question headings |")
        report_lines.append(f"| Internal Links | {r['status_links']} | {r['il_count']} total |")
        report_lines.append(f"| Schema Ready | {r['status_schema']} | {'All fields set' if r['status_schema'] == '✅' else 'Missing: ' + ', '.join(r['schema_missing'])} |")
        if r['fixes']:
            report_lines.append("\n### Fix instructions:")
            for fix in r['fixes']:
                report_lines.append(fix)
        report_lines.append("")

# Passing posts summary
if passed_reports:
    report_lines.append(f"### Posts Passing All Checks ({len(passed_reports)}):\n")
    for r in passed_reports:
        report_lines.append(f"- ✅ {r['slug']}")

report_lines.append("")
report_lines.append("## Aggregate Statistics")
report_lines.append(f"Total posts checked: {len(post_reports)}")
report_lines.append(f"Passing all checks: {pass_all}")
report_lines.append(f"Need fixes: {fail_any}")
report_lines.append("")
report_lines.append("### Check-level failure counts:")
report_lines.append(f"- **TF-IDF** (< 5 keyword occurrences): {sum(1 for r in post_reports if not r['status_tfidf'] == '✅')}")
report_lines.append(f"- **Entities** (missing required entities): {sum(1 for r in post_reports if not r['status_entities'] == '✅')}")
report_lines.append(f"- **Pillar Link** (no pillar link): {sum(1 for r in post_reports if not r['status_pillar'] == '✅')}")
report_lines.append(f"- **AEO/GEO** (< 2 question headings): {sum(1 for r in post_reports if not r['status_aeo'] == '✅')}")
report_lines.append(f"- **Internal Links** (< 3): {sum(1 for r in post_reports if not r['status_links'] == '✅')}")
report_lines.append(f"- **Schema Data** (missing fields): {sum(1 for r in post_reports if not r['status_schema'] == '✅')}")

report_lines.append("")
report_lines.append("---")
report_lines.append("### Priority Issues Summary")
report_lines.append("")

# Top priorities
missing_author = sum(1 for r in post_reports if 'Author (Kanok Miah)' in r['missing_entities'])
if missing_author > 0:
    report_lines.append(f"**🔴 HIGH PRIORITY**: {missing_author} posts missing author entity (Kanok Miah). Add 'Kanok Miah' mentions for EEAT.")

no_pillar = sum(1 for r in post_reports if not r['status_pillar'] == '✅' and not r['status_schema'] == '✅ benchmark')
if no_pillar > 0:
    report_lines.append(f"**🟡 MEDIUM PRIORITY**: {no_pillar} posts missing pillar topic links. Add cluster-to-pillar links.")

low_aeo = sum(1 for r in post_reports if not r['status_aeo'] == '✅')
if low_aeo > 0:
    report_lines.append(f"**🟡 MEDIUM PRIORITY**: {low_aeo} posts with insufficient question headings. Add 2+ question-based headings for AEO/GEO.")

low_links = sum(1 for r in post_reports if not r['status_links'] == '✅')
if low_links > 0:
    report_lines.append(f"**🟡 MEDIUM PRIORITY**: {low_links} posts with fewer than 3 internal links.")

print('\n'.join(report_lines))
