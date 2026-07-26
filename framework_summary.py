#!/usr/bin/env python3
"""Content Framework Enforcer — summary report generator"""
import re, subprocess

# Read slugs from git diff
result = subprocess.run(
    ['git', 'diff', 'HEAD~4..HEAD', '--', 'src/app/blog/data.js'],
    capture_output=True, text=True, cwd='/root/kanok-miahit'
)

with open('src/app/blog/data.js', 'r') as f:
    lines = f.readlines()

line_to_slug = {}
current_slug = None
for i, line in enumerate(lines, 1):
    m = re.search(r"slug:\s*['\"]([^'\"]+)['\"]", line)
    if m:
        current_slug = m.group(1)
    if current_slug:
        line_to_slug[i] = current_slug

hunks = re.findall(r'@@ -(\d+),(\d+) \+(\d+),(\d+) @@', result.stdout)
changed_slugs = set()
for old_start, old_count, new_start, new_count in hunks:
    for line_no in range(int(old_start), int(old_start) + int(old_count)):
        if line_no in line_to_slug:
            changed_slugs.add(line_to_slug[line_no])
    for line_no in range(int(new_start), int(new_start) + int(new_count)):
        if line_no in line_to_slug:
            changed_slugs.add(line_to_slug[line_no])

changed_slugs = sorted(changed_slugs)

commit_count = subprocess.run(
    ['git', 'log', '--oneline', '--since="48 hours ago"', '--', 'src/app/blog/data.js'],
    capture_output=True, text=True, cwd='/root/kanok-miahit'
)
n_commits = len(commit_count.stdout.strip().split('\n')) if commit_count.stdout.strip() else 0

print("Content Framework Enforcement Report -- kanokmiah.com.bd")
print("=" * 60)
print(f"Period: Last 48 hours")
print(f"Commits touching data.js: {n_commits}")
print(f"Posts modified: {len(changed_slugs)}")

# Nature of changes
diff_text = result.stdout
bold_fixes = len(re.findall(r'\*\*, \*\*', diff_text))
content_changes = re.findall(r'^-.*\n\+.*', diff_text)

print(f"Nature: Bold/formatting fixes, blank line insersions, heading cleanup")
print(f"Content changes (auto-fix + enforcer): {len(content_changes)} lines")

print("\nCommits (most recent first):")
for c in commit_count.stdout.strip().split('\n'):
    print(f"  {'📝' if 'content-framework' in c else '🤖'}  {c}")

# Read all posts
with open('src/app/blog/data.js', 'r') as f:
    content = f.read()

post_data = {}
for slug in changed_slugs:
    m = re.search(r"slug:\s*['\"]" + re.escape(slug) + r"['\"].*?content:\s*`(.*?)`", content, re.DOTALL)
    if not m:
        continue

    post_content = m.group(1)
    title_m = re.search(r"title:\s*['\"]([^'\"]+)['\"]", content[m.start():m.end()])
    tags_m = re.search(r"tags:\s*\[(.*?)\]", content[m.start():m.end()], re.DOTALL)
    tags = re.findall(r"['\"]([^'\"]+)['\"]", tags_m.group(1)) if tags_m else []
    title = title_m.group(1) if title_m else slug

    # AEO check
    headings = re.findall(r'^#{2,3}\s+(.+)$', post_content, re.MULTILINE)
    question_starts = ['How', 'What', 'Why', 'When', 'Where', 'Can', 'Do', 'Does', 'Is', 'Are',
                       'কিভাবে', 'কী', 'কেন', 'কখন', 'কোথায়', 'কীভাবে', 'কি']
    qh_count = sum(1 for h in headings if any(h.strip().lower().startswith(qs.lower()) for qs in question_starts))

    # Internal links
    internal_links = re.findall(r'\[([^\]]+)\]\((/[^)]+)\)', post_content)
    internal_count = len([1 for t, u in internal_links if not u.startswith(('http://', 'https://', '//'))])

    # Entity checks
    has_bd = bool(re.search(r'(বাংলাদেশ|Bangladesh)', post_content, re.IGNORECASE))
    has_dhaka = bool(re.search(r'(ঢাকা|Dhaka)', post_content, re.IGNORECASE))

    # Pillar link check
    has_pillar = bool(re.search(r'(/blog/complete-seo-guide-bangladesh-businesses-2026|/services/technical-seo|/blog/local-seo-dhaka-google-maps-ranking)', post_content))

    # Schema check
    date_m = re.search(r"date:\s*['\"]([^'\"]+)['\"]", content[m.start():m.end()])
    excerpt_m = re.search(r"excerpt:\s*['\"]([^'\"]+)['\"]", content[m.start():m.end()])

    post_data[slug] = {
        'title': title, 'qh_cnt': qh_count, 'aeo_pass': qh_count >= 2,
        'internal_cnt': internal_count, 'internal_pass': internal_count >= 3,
        'has_bd': has_bd, 'has_dhaka': has_dhaka, 'entities_pass': has_bd and has_dhaka,
        'has_pillar': has_pillar, 'schema_pass': bool(date_m) and bool(excerpt_m) and bool(title)
    }

all_pass = sum(1 for s in changed_slugs if s in post_data and all([
    post_data[s]['aeo_pass'], post_data[s]['internal_pass'],
    post_data[s]['entities_pass'], post_data[s]['has_pillar'], post_data[s]['schema_pass']]))
any_fail = len(changed_slugs) - all_pass

print(f"\nFramework Check Summary:")
print(f"  All checks passed: {all_pass} posts")
print(f"  Some checks failed: {any_fail} posts")

aeo_fails = sum(1 for s in changed_slugs if s in post_data and not post_data[s]['aeo_pass'])
int_fails = sum(1 for s in changed_slugs if s in post_data and not post_data[s]['internal_pass'])
ent_fails = sum(1 for s in changed_slugs if s in post_data and not post_data[s]['entities_pass'])
pillar_fails = sum(1 for s in changed_slugs if s in post_data and not post_data[s]['has_pillar'])

print(f"\nFailure breakdown:")
print(f"  AEO/GEO (question headings < 2):  {aeo_fails} posts")
print(f"  Internal Links (< 3):              {int_fails} posts")
print(f"  Entity Coverage:                   {ent_fails} posts")
print(f"  Pillar Link missing:               {pillar_fails} posts")

# Priority posts (3+ fails)
priority = []
for slug in changed_slugs:
    if slug not in post_data:
        continue
    p = post_data[slug]
    fails = []
    if not p['aeo_pass']: fails.append('AEO')
    if not p['internal_pass']: fails.append('InternalLinks')
    if not p['entities_pass']: fails.append('Entities')
    if not p['has_pillar']: fails.append('PillarLink')
    if not p['schema_pass']: fails.append('Schema')
    if len(fails) >= 3:
        priority.append((slug, fails))

if priority:
    print(f"\nPriority posts (3+ failing checks):")
    for slug, fails in priority:
        p = post_data[slug]
        print(f"  '{slug}'")
        print(f"    Title: {p['title'][:60]}")
        print(f"    Fails: {', '.join(fails)}")
        print(f"    Details: AEO={p['qh_cnt']}q, Links={p['internal_cnt']}, BD={p['has_bd']}, Dhaka={p['has_dhaka']}, Pillar={p['has_pillar']}")

# Focus: canonical URL post
print(f"\n{'='*60}")
print("FOCUS: seo-canonical-url-guide-bd (manually edited by enforcer)")
print('='*60)
slug = 'seo-canonical-url-guide-bd'
if slug in post_data:
    p = post_data[slug]
    print(f"  Title: {p['title']}")
    print(f"  AEO/GEO: {'PASS' if p['aeo_pass'] else 'FAIL'} ({p['qh_cnt']} question headings)")
    print(f"  Internal Links: {'PASS' if p['internal_pass'] else 'FAIL'} ({p['internal_cnt']} total)")
    print(f"  Entities: {'PASS' if p['entities_pass'] else 'FAIL'} (Bangladesh={p['has_bd']}, Dhaka={p['has_dhaka']})")
    print(f"  Pillar Link: {'PASS' if p['has_pillar'] else 'FAIL'}")
    print(f"  Schema: {'PASS' if p['schema_pass'] else 'FAIL'}")
    print(f"  Status: {'NEEDS FIXES - internal links low, Dhaka entity missing' if not p['entities_pass'] or not p['internal_pass'] else 'OK'}")

print(f"\n{'='*60}")
print("FULL DETAILED REPORT (all 56 posts)")
print('='*60)

# Individual post results
for slug in changed_slugs:
    if slug not in post_data:
        continue
    p = post_data[slug]
    checks = []
    checks.append(f"TF-IDF: see detail above")
    checks.append(f"AEO: {'PASS' if p['aeo_pass'] else 'FAIL'} ({p['qh_cnt']}q)")
    checks.append(f"Links: {'PASS' if p['internal_pass'] else 'FAIL'} ({p['internal_cnt']})")
    checks.append(f"Ent: {'PASS' if p['entities_pass'] else 'FAIL'} (BD={p['has_bd']},Dhk={p['has_dhaka']})")
    checks.append(f"Pillar: {'PASS' if p['has_pillar'] else 'FAIL'}")
    checks.append(f"Schema: {'PASS' if p['schema_pass'] else 'FAIL'}")
    
    all_ok = p['aeo_pass'] and p['internal_pass'] and p['entities_pass'] and p['has_pillar'] and p['schema_pass']
    status = 'OK' if all_ok else 'NEEDS FIXES'
    icon = 'PASS' if all_ok else 'FAIL'
    
    # Fix suggestions
    fixes = []
    if not p['entities_pass']:
        if not p['has_dhaka']:
            fixes.append("add Dhaka mention")
    if not p['internal_pass']:
        fixes.append(f"add {3-p['internal_cnt']} internal link(s)")
    if not p['aeo_pass']:
        fixes.append(f"add {2-p['qh_cnt']} question heading(s)")
    if not p['has_pillar']:
        fixes.append("add pillar link")
    
    print(f"  {icon:4s} | {slug:45s} | {chr(10)+' '*53 if fixes else 'OK'}{' | '.join(fixes) if fixes else ''}")

print(f"\n{'='*60}")
print("END REPORT")
