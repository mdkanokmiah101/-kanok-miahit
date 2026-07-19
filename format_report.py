#!/usr/bin/env python3
"""Generate consolidated summary from framework check report."""
import re

with open('/tmp/framework_report.txt', 'r') as f:
    content = f.read()

# Parse posts
posts = content.split('============================================================\n')
print("""# 📋 Content Framework Enforcement Report — kanokmiah.com.bd
**Date:** Scheduled cron run
**Scope:** 55 modified posts in last 48 hours (71 commits)
**Status:** Framework checks completed

---

""")

all_pass = []
needs_fix = []

for post in posts:
    if '📝 Post:' not in post:
        continue
    
    slug_match = re.search(r'📝 Post: (.+)', post)
    slug = slug_match.group(1).strip() if slug_match else 'unknown'
    
    title_match = re.search(r'Title: (.+?)\.\.\.', post)
    title = title_match.group(1).strip() if title_match else slug
    
    # Check if all pass
    if "✅ All checks passed! No fixes needed." in post:
        all_pass.append(slug)
        continue
    
    # Extract fail details
    fails = []
    
    # TF-IDF
    tfidf_match = re.search(r'TF-IDF:.*?([❌])', post, re.DOTALL)
    tfidf_detail = re.search(r'TF-IDF:.*?\| (❌) \| (.+?) \|', post)
    if tfidf_detail:
        fails.append(('TF-IDF', tfidf_detail.group(2)))
    
    # Entities
    entity_match = re.search(r'Entities.*?\| (❌) \| (.+?) \|', post)
    if entity_match:
        fails.append(('Entities', entity_match.group(2)))
    
    # Pillar
    pillar_match = re.search(r'Pillar Link.*?\| (❌)', post)
    if pillar_match:
        fails.append(('Pillar Link', 'Missing link to pillar page'))
    
    # AEO/GEO
    aeo_match = re.search(r'AEO/GEO.*?\| (❌) \| (.+?) \|', post)
    if aeo_match:
        fails.append(('AEO/GEO', aeo_match.group(2)))
    
    # Internal Links
    il_match = re.search(r'Internal Links.*?\| (❌)', post)
    if il_match:
        fails.append(('Internal Links', 'Too few internal links'))
    
    needs_fix.append((slug, title[:60], fails))

# Summary
print(f"## Summary\n")
print(f"- **Total posts checked:** {len(all_pass) + len(needs_fix)}")
print(f"- **✅ Fully compliant:** {len(all_pass)}")
print(f"- **❌ Needs fixes:** {len(needs_fix)}")
print()

# Issue breakdown
pillar_count = sum(1 for _, _, fails in needs_fix if any(f[0] == 'Pillar Link' for f in fails))
aeo_count = sum(1 for _, _, fails in needs_fix if any(f[0] == 'AEO/GEO' for f in fails))
entity_count = sum(1 for _, _, fails in needs_fix if any(f[0] == 'Entities' for f in fails))
tfidf_count = sum(1 for _, _, fails in needs_fix if any(f[0] == 'TF-IDF' for f in fails))
il_count = sum(1 for _, _, fails in needs_fix if any(f[0] == 'Internal Links' for f in fails))

print("### Issue Frequency\n")
print(f"| Issue | Count | Severity |")
print(f"|-------|-------|----------|")
print(f"| 🔗 Missing pillar link | {pillar_count} | HIGH |")
print(f"| ❓ AEO/GEO (< 2 question headings) | {aeo_count} | MEDIUM |")
print(f"| 🏷️ Missing entities | {entity_count} | MEDIUM |")
print(f"| 🔍 TF-IDF too thin (<5 keyword occurrences) | {tfidf_count} | HIGH |")
print(f"| 🔗 Insufficient internal links | {il_count} | LOW |")
print()

# Fully compliant posts
print("### ✅ Fully Compliant Posts (all checks pass)\n")
for slug in all_pass:
    print(f"- {slug}")
print()

# Priority fix list
print("### 🚨 Priority Fix List\n")
print("Posts sorted by fix urgency (most issues first):\n")

needs_fix.sort(key=lambda x: -len(x[2]))

for slug, title, fails in needs_fix:
    icons = {
        'TF-IDF': '🔍',
        'Entities': '🏷️',
        'Pillar Link': '🔗',
        'AEO/GEO': '❓',
        'Internal Links': '🔗',
    }
    fail_icons = ' '.join(icons.get(f[0], '⚠️') for f in fails)
    print(f"**{slug}** — {fail_icons} ({len(fails)} issues)")
    for fname, fdetail in fails:
        print(f"  - {icons.get(fname, '⚠️')} **{fname}**: {fdetail}")
    print()

# Detailed report reference
print("---")
print("### 📑 Detailed Per-Post Report\n")
print("Below is the full per-post breakdown:\n")

# Print full report but in a more readable format
for post in posts:
    if '📝 Post:' not in post:
        continue
    # Print just the table and fix instructions
    lines = post.split('\n')
    in_table = False
    in_fix = False
    for line in lines:
        if line.startswith('## Post:'):
            print(line)
        elif line.startswith('| Check'):
            print(line)
            in_table = True
        elif line.startswith('|--'):
            if in_table:
                print(line)
        elif line.startswith('| TF-IDF') or line.startswith('| Entities') or line.startswith('| Pillar') or line.startswith('| AEO/GEO') or line.startswith('| Internal') or line.startswith('| Schema'):
            print(line)
        elif line.startswith('|   └'):
            print(line)
        elif line.startswith('### Fix'):
            print(line)
            in_fix = True
            in_table = False
        elif in_fix and line.strip() and not line.startswith('|'):
            print(line)
        elif not line.strip() and in_fix:
            print()
            in_fix = False
    print()
