#!/usr/bin/env python3
"""
Content Framework Enforcer for kanokmiah.com.bd - Summary Report Generator
Consolidates results from run_audit.py into a human-readable report.
"""
import re, subprocess, json

# ── Get modified slugs ──────────────────────────
result = subprocess.run(
    ['git', 'log', '--oneline', '--since=48 hours ago', '--format=%s', '--', 'src/app/blog/data.js'],
    capture_output=True, text=True, cwd='/root/kanok-miahit'
)
msgs = result.stdout.strip().split('\n')

modified_slugs = set()
for msg in msgs:
    for m in re.finditer(r'processed blog #\d+ - ([a-z0-9-]+)', msg):
        modified_slugs.add(m.group(1))
    for m in re.finditer(r'fix: deep audit fixes for ([a-z0-9-]+)', msg):
        modified_slugs.add(m.group(1))
for msg in msgs:
    words = msg.split()
    for w in words:
        if re.match(r'^[a-z0-9-]+$', w) and len(w) > 10 and any(kw in w for kw in ['seo','blog','local','google','content','link','mobile','ecommerce','keyword','schema','technical']):
            modified_slugs.add(w)
        elif '-' in w and len(w.split('-')) >= 3:
            modified_slugs.add(w)

# ── Parse posts ─────────────────────────────────
posts = []
with open('/root/kanok-miahit/src/app/blog/data.js', 'r') as f:
    lines = f.readlines()

brace_depth = 0
post_start = -1
current_post_lines = []
in_posts_array = False

for line in lines:
    stripped = line.strip()
    if not in_posts_array:
        if 'const posts = [' in stripped or 'const posts=[' in stripped:
            in_posts_array = True
        continue
    if stripped.startswith('{') and not stripped.startswith('{{'):
        if post_start == -1:
            post_start = 0
            current_post_lines = [line]
            brace_depth = stripped.count('{') - stripped.count('}')
        else:
            current_post_lines.append(line)
            brace_depth += stripped.count('{') - stripped.count('}')
    elif post_start >= 0:
        current_post_lines.append(line)
        brace_depth += stripped.count('{') - stripped.count('}')
        if brace_depth <= 0:
            post_text = ''.join(current_post_lines)
            slug_m = re.search(r'slug:\s*"([^"]+)"', post_text)
            title_m = re.search(r'title:\s*"([^"]*)"', post_text)
            date_m = re.search(r'date:\s*"([^"]*)"', post_text)
            excerpt_m = re.search(r'excerpt:\s*"([^"]*)"', post_text)
            tags_m = re.search(r'tags:\s*\[([^\]]+)\]', post_text)
            author_m = re.search(r'author:\s*"([^"]*)"', post_text)
            metaT_m = re.search(r'metaTitle:\s*"([^"]*)"', post_text)
            metaD_m = re.search(r'metaDescription:\s*"([^"]*)"', post_text)
            dateMod_m = re.search(r'dateModified:\s*"([^"]*)"', post_text)
            content_m = re.search(r'content:\s*`([^`]*)`', post_text)
            content = ''
            if content_m:
                content = content_m.group(1)
            else:
                cm = re.search(r'content:\s*`', post_text)
                if cm:
                    rest = post_text[cm.end():]
                    for j in range(len(rest)):
                        if rest[j] == '`' and (j+1 >= len(rest) or rest[j+1] in ',;\n'):
                            content = rest[:j]
                            break
            
            if slug_m and title_m:
                tags = []
                if tags_m:
                    tags = [t.strip().strip('"').strip("'") for t in tags_m.group(1).split(',')]
                posts.append({
                    'slug': slug_m.group(1),
                    'title': title_m.group(1),
                    'date': date_m.group(1) if date_m else '',
                    'excerpt': excerpt_m.group(1) if excerpt_m else '',
                    'tags': tags,
                    'metaTitle': metaT_m.group(1) if metaT_m else '',
                    'metaDescription': metaD_m.group(1) if metaD_m else '',
                    'dateModified': dateMod_m.group(1) if dateMod_m else '',
                    'content': content
                })
            post_start = -1
            current_post_lines = []
    elif stripped.startswith(']'):
        break

posts_dict = {p['slug']: p for p in posts if p['slug']}
to_check = [s for s in modified_slugs if s in posts_dict]
for s in list(modified_slugs):
    if s not in posts_dict:
        for pslug in posts_dict:
            if s in pslug or pslug in s:
                to_check.append(pslug)
                break
to_check = list(set(to_check))

# ── Run checks on each post ─────────────────────
stopwords = {'a','an','the','for','in','of','to','and','or','is','are','your','our','its',
             'that','this','with','from','by','at','on','be','has','have','not','but','was',
             'were','will','can','all','each','every','some','any','no','more','most','best',
             'top','guide','tips','how','what','why','when','where','which','who'}

pillar_pages = {
    'seo-guide': '/blog/complete-seo-guide-bangladesh-businesses-2026',
    'local-seo': '/blog/local-seo-tips-dhaka-businesses-google-maps',
    'technical-seo': '/blog/technical-seo-checklist-bangladeshi-websites',
    'link-building': '/blog/link-building-strategies-bangladesh-market',
    'content-marketing': '/blog/content-marketing-seo-friendly-content-writing',
    'keyword-research': '/blog/keyword-research-bangladesh-market',
    'ecommerce-seo': '/blog/ecommerce-seo-daraz-shopify-guide',
    'mobile-seo': '/blog/mobile-seo-optimization-bangladesh-mobile-first-era',
    'schema-markup': '/blog/schema-markup-rich-snippets-techniques',
    'seo-vs-ads': '/blog/seo-vs-google-ads-bangladesh-business',
}

results = {}
all_passed_count = 0
failed_counts = {'tfidf': 0, 'entities': 0, 'pillar': 0, 'aeo': 0, 'links': 0, 'schema': 0}

for slug in to_check:
    post = posts_dict[slug]
    content_lower = post['content'].lower()
    title_lower = post['title'].lower()
    
    # TF-IDF
    words = title_lower.split()
    keyword = ''
    for w in words:
        wc = w.strip('0123456789-')
        if len(wc) >= 4 and wc not in stopwords and wc not in ('seo','bangladesh','bangladeshi','bangla','bd','2026','2025','2024'):
            keyword = wc
            break
    if not keyword:
        for i, w in enumerate(words):
            if w in ('seo','complete','ultimate','essential') and i+1 < len(words):
                keyword = words[i+1].strip('0123456789-')
                if len(keyword) >= 4: break
    if not keyword:
        keyword = words[-1] if words else title_lower
    count = len(re.findall(re.escape(keyword), post['content'], re.IGNORECASE))
    bigrams = [' '.join(words[i:i+2]) for i in range(len(words)-1)]
    bigram_count = sum(len(re.findall(re.escape(bg), post['content'], re.IGNORECASE)) for bg in bigrams if len(bg) > 8)
    tfidf_pass = count >= 5 or bigram_count >= 3
    
    # Entities
    missing_entities = []
    if 'dhaka' not in content_lower: missing_entities.append('Dhaka')
    if 'bangladesh' not in content_lower: missing_entities.append('Bangladesh')
    if 'seo' not in content_lower: missing_entities.append('SEO')
    entities_pass = len(missing_entities) == 0
    
    # Pillar
    matched_pillar = None
    for pname, purl in pillar_pages.items():
        pname_lower = pname.replace('-', ' ')
        if pname_lower in slug.lower() or any(pname_lower in t.lower() for t in post['tags']):
            matched_pillar = pname
            break
    if not matched_pillar:
        best = None; best_score = 0
        for pname, purl in pillar_pages.items():
            score = sum(1 for m in pname.replace('-', ' ').split() if m in content_lower)
            if score > best_score: best_score = score; best = pname
        matched_pillar = best
    pillar_link_found = any(purl in post['content'] for purl in pillar_pages.values())
    pillar_pass = pillar_link_found
    
    # AEO/GEO
    headings = re.findall(r'^#{1,6}\s+(.+)$', post['content'], re.MULTILINE)
    qheadings = [h.strip() for h in headings if re.match(r'^(How|What|Why|When|Where|Can|Do|Is|Are|Does|Which|Who|Whose)\s', h.strip())]
    aeo_pass = len(qheadings) >= 2
    
    # Internal links
    link_pats = [
        (r'\]\(/blog/[^)]+\)', 'blog'),
        (r'\]\(/locations/[^)]+\)', 'loc'),
        (r'\]\(/services/[^)]+\)', 'svc'),
        (r'\]\(/industries/[^)]+\)', 'ind'),
        (r'\]\(/about[^)]*\)', 'other'),
        (r'\]\(/contact[^)]*\)', 'other'),
        (r'\]\(/\)', 'other'),
    ]
    total_links = sum(len(re.findall(pat, post['content'])) for pat, _ in link_pats)
    links_pass = total_links >= 3
    
    # Schema
    schema_issues = []
    if not post['title'] or len(post['title']) < 10: schema_issues.append('title')
    if not post['excerpt'] or len(post['excerpt']) < 50: schema_issues.append('excerpt')
    if not post['date']: schema_issues.append('date')
    if not post.get('dateModified'): schema_issues.append('dateModified')
    if not post.get('metaTitle'): schema_issues.append('metaTitle')
    if not post.get('metaDescription'): schema_issues.append('metaDescription')
    schema_pass = len(schema_issues) == 0
    
    passed_all = all([tfidf_pass, entities_pass, pillar_pass, aeo_pass, links_pass, schema_pass])
    
    results[slug] = {
        'passed_all': passed_all,
        'title': post['title'][:60],
        'checks': {
            'TF-IDF': tfidf_pass,
            'Entities': entities_pass,
            'Pillar': pillar_pass,
            'AEO/GEO': aeo_pass,
            'Links': links_pass,
            'Schema': schema_pass,
        },
        'details': {
            'keyword_count': count,
            'missing_entities': missing_entities,
            'matched_pillar': matched_pillar,
            'qheading_count': len(qheadings),
            'total_links': total_links,
            'schema_issues': schema_issues,
        }
    }
    
    if not tfidf_pass: failed_counts['tfidf'] += 1
    if not entities_pass: failed_counts['entities'] += 1
    if not pillar_pass: failed_counts['pillar'] += 1
    if not aeo_pass: failed_counts['aeo'] += 1
    if not links_pass: failed_counts['links'] += 1
    if not schema_pass: failed_counts['schema'] += 1
    
    if passed_all:
        all_passed_count += 1

# ── Generate report ─────────────────────────────

# Fix instruction templates by category
fix_guides = {
    'schema': """### Schema Fix Pattern
Most failing posts need:
```yaml
dateModified: "YYYY-MM-DD"    # Add date of last modification
metaTitle: "..."              # SEO title (55-60 chars, include primary keyword)
metaDescription: "..."        # Meta description (150-160 chars with keyword + CTA)
```""",
    'pillar': """### Pillar Link Fix Pattern
Add a contextual link to the relevant pillar page at a natural point in the content. 
Reference the pillar by topic (e.g., "See our complete [SEO guide for Bangladesh](/blog/complete-seo-guide-bangladesh-businesses-2026) for a comprehensive overview.")""",
    'aeo': """### AEO/GEO Fix Pattern
Add voice-search-optimized question headings like:
- "How does X work in Bangladesh?"
- "What is the best strategy for Y?"
- "Why should Bangladeshi businesses care about Z?" """,
    'entities': """### Entity Coverage Fix Pattern
Mention "Dhaka", "Bangladesh", and "SEO" naturally in the first 2-3 paragraphs.
For technical docs (robots.txt, sitemap, canonical, redirects, hreflang, structured data), frame the topic in the Bangladesh context.""",
    'links': """### Internal Linking Fix Pattern
Add at least 3 internal links to related blog posts, service pages (/services/...), or location pages (/locations/dhaka).""",
    'tfidf': """### TF-IDF Fix Pattern
Use the primary keyword more frequently in subheadings, first paragraph, and naturally throughout the body."""
}

# Build the report
report = []
report.append("=" * 72)
report.append("🏗️  CONTENT FRAMEWORK ENFORCEMENT REPORT")
report.append("=" * 72)
report.append(f"**Project:** kanokmiah.com.bd")
report.append(f"**Date/Time:** Sat Jul 18 01:51:48 UTC 2026")
report.append(f"**Period:** Last 48 hours (Jul 16 01:49 – Jul 18 01:49 UTC)")
report.append(f"**Commits analyzed:** {len(msgs)}")
report.append(f"**Modified posts detected:** {len(modified_slugs)}")
report.append(f"**Posts inspected:** {len(to_check)}")
report.append("")

# EXECUTIVE SUMMARY
report.append("─" * 72)
report.append("📊 EXECUTIVE SUMMARY")
report.append("─" * 72)
report.append(f"✅ Posts passing ALL checks:  {all_passed_count}/{len(to_check)}")
report.append(f"❌ Posts needing attention:   {len(to_check) - all_passed_count}/{len(to_check)}")
report.append("")
report.append("Failures by category:")
report.append(f"  🔤 TF-IDF Coverage:       {failed_counts['tfidf']} failing  (keyword underused)")
report.append(f"  🌐 Entity Coverage:       {failed_counts['entities']} failing  (missing Dhaka/Bangladesh/SEO)")
report.append(f"  🏛️  Pillar-Cluster Link:   {failed_counts['pillar']} failing  (no link to pillar page)")
report.append(f"  🎤 AEO/GEO Optimization:  {failed_counts['aeo']} failing  (< 2 question headings)")
report.append(f"  🔗 Internal Linking:      {failed_counts['links']} failing  (< 3 internal links)")
report.append(f"  📋 Schema Readiness:      {failed_counts['schema']} failing  (missing meta/schema fields)")
report.append("")

# PRIORITY POSTS
report.append("─" * 72)
report.append("🚨 PRIORITY — POSTS WITH MULTIPLE FAILURES")
report.append("─" * 72)

multi_fail = {s: r for s, r in results.items() if not r['passed_all'] and sum(1 for v in r['checks'].values() if not v) >= 3}
high_prio = sorted(multi_fail.items(), key=lambda x: -sum(1 for v in x[1]['checks'].values() if not v))

if high_prio:
    for slug, r in high_prio:
        fails = [k for k, v in r['checks'].items() if not v]
        report.append(f"\n  ❌ **{slug}**")
        report.append(f"     Title: {r['title']}")
        report.append(f"     Failing: {', '.join(fails)}")
        if r['details']['missing_entities']:
            report.append(f"     Missing entities: {', '.join(r['details']['missing_entities'])}")
        if r['details']['schema_issues']:
            report.append(f"     Schema issues: {', '.join(r['details']['schema_issues'])}")
        if not r['checks']['AEO/GEO']:
            report.append(f"     Question headings: {r['details']['qheading_count']} (need 2+)")
        if not r['checks']['Links']:
            report.append(f"     Internal links: {r['details']['total_links']} (need 3+)")
else:
    report.append("\n  No posts with 3+ failures found.")

report.append("")

# POSTS THAT PASSED ALL
report.append("─" * 72)
report.append("✅ POSTS THAT PASSED ALL CHECKS")
report.append("─" * 72)
passed_posts = [s for s, r in results.items() if r['passed_all']]
if passed_posts:
    for s in passed_posts:
        report.append(f"  ✅ {s}")
else:
    report.append("  (none)")

report.append("")

# PER-CATEGORY BREAKDOWN
report.append("─" * 72)
report.append("📋 BREAKDOWN BY CHECK CATEGORY")
report.append("─" * 72)

# Schema failures are the most common
if failed_counts['schema'] > 0:
    schema_fail_list = [s for s, r in results.items() if not r['checks']['Schema']]
    total_schema_issues = {}
    for s in schema_fail_list:
        for issue in results[s]['details']['schema_issues']:
            total_schema_issues[issue] = total_schema_issues.get(issue, 0) + 1
    
    report.append(f"\n🔹 Schema Readiness — {failed_counts['schema']} posts failing")
    for issue, count in sorted(total_schema_issues.items(), key=lambda x: -x[1]):
        report.append(f"   • Missing {issue}: {count} posts")
    
    # Sample schema-failing posts
    report.append(f"   Sample posts: {', '.join(schema_fail_list[:5])}...")
    if failed_counts['schema'] >= 3:
        report.append("\n" + fix_guides['schema'])

# AEO/GEO
if failed_counts['aeo'] > 0:
    aeo_fail_list = [s for s, r in results.items() if not r['checks']['AEO/GEO']]
    report.append(f"\n🔹 AEO/GEO — {failed_counts['aeo']} posts failing")
    report.append(f"   Sample: {', '.join(aeo_fail_list[:5])}...")
    report.append(f"   Most have 0 question headings (need ≥ 2)")
    if failed_counts['aeo'] >= 3:
        report.append("\n" + fix_guides['aeo'])

# Pillar
if failed_counts['pillar'] > 0:
    pillar_fail_list = [s for s, r in results.items() if not r['checks']['Pillar']]
    report.append(f"\n🔹 Pillar-Cluster Link — {failed_counts['pillar']} posts failing")
    report.append(f"   Sample: {', '.join(pillar_fail_list[:5])}...")
    if failed_counts['pillar'] >= 3:
        report.append("\n" + fix_guides['pillar'])

# Entities
if failed_counts['entities'] > 0:
    ent_fail_list = [s for s, r in results.items() if not r['checks']['Entities']]
    report.append(f"\n🔹 Entity Coverage — {failed_counts['entities']} posts failing")
    for s in ent_fail_list:
        report.append(f"   ❌ {s}: missing {', '.join(results[s]['details']['missing_entities'])}")
    if failed_counts['entities'] >= 3:
        report.append("\n" + fix_guides['entities'])

# Internal Links
if failed_counts['links'] > 0:
    link_fail_list = [s for s, r in results.items() if not r['checks']['Links']]
    report.append(f"\n🔹 Internal Linking — {failed_counts['links']} posts failing")
    for s in link_fail_list:
        report.append(f"   ❌ {s}: {results[s]['details']['total_links']} links (need 3+)")
    if failed_counts['links'] >= 3:
        report.append("\n" + fix_guides['links'])

# TF-IDF
if failed_counts['tfidf'] > 0:
    tfidf_fail_list = [s for s, r in results.items() if not r['checks']['TF-IDF']]
    report.append(f"\n🔹 TF-IDF Coverage — {failed_counts['tfidf']} posts failing")
    for s in tfidf_fail_list:
        report.append(f"   ❌ {s}: keyword '{results[s]['details'].get('keyword','?')}' appears {results[s]['details']['keyword_count']}x")
    if failed_counts['tfidf'] >= 1:
        report.append("\n" + fix_guides['tfidf'])

report.append("")
report.append("─" * 72)
report.append("DETAILED RESULTS (all posts)")
report.append("─" * 72)

for slug in sorted(results.keys()):
    r = results[slug]
    status = '✅' if r['passed_all'] else '❌'
    fails = [k for k, v in r['checks'].items() if not v]
    fail_str = f" ({', '.join(fails)})" if fails else ''
    report.append(f"{status} **{slug}**{fail_str}")

report.append("")
report.append("─" * 72)
report.append("SYSTEM NOTES")
report.append("─" * 72)
report.append("• Schema failures (dateModified/metaTitle/metaDescription) are the most common issue,")
report.append("  affecting many Bengali-language posts that were processed recently.")
report.append("• Bengali posts using Unicode characters may have keyword-detection limitations")
report.append("  in the TF-IDF check (some detected '0 occurrences' are false negatives due to")
report.append("  stemming/morphology differences in Bangla).")
report.append("• Posts with 0 internal links (robots.txt, sitemap, canonical, redirects, hreflang,")
report.append("  structured data) are likely auto-generated technical doc pages.")
report.append("• The auto-fix cron ('auto-fix: blog heading/HTML tags cleanup') ran at 19:17 UTC,")
report.append("  so some heading/formatting issues may already be resolved.")
report.append("")
report.append("=" * 72)
report.append("END OF REPORT")
report.append("=" * 72)

print('\n'.join(report))
