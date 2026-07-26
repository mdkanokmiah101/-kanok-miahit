#!/usr/bin/env python3
"""Summarize the framework check report."""
import re

with open("/tmp/framework_report.txt") as f:
    data = f.read()

# Parse each post section
posts = []
current = None
for line in data.split('\n'):
    if line.startswith('## Post:'):
        if current:
            posts.append(current)
        current = {'slug': line.replace('## Post:', '').strip(), 'checks': [], 'fixes': []}
    elif current:
        if '|' in line and line.strip().startswith('|'):
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 4:
                check_name = parts[1]
                status = parts[2]
                detail = parts[3]
                current['checks'].append((check_name, status, detail))
        elif line.strip().startswith('- **'):
            current['fixes'].append(line.strip())

if current:
    posts.append(current)

# Aggregate
passed = [p for p in posts if not any('❌' in c[1] for c in p['checks'])]
failed = [p for p in posts if any('❌' in c[1] for c in p['checks'])]

print(f"REPORT: Content Framework Enforcement — {len(posts)} modified posts checked")
print(f"Generated: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')} BST")
print()
print("=" * 70)

# Summary table
print(f"\nOVERALL: {'✅ All checks passed' if len(failed)==0 else f'❌ {len(failed)} posts need attention'}")

print(f"\n{'='*70}")
print(f"SUMMARY BY CHECK TYPE:")
print(f"{'='*70}")

check_stats = {}
for p in posts:
    for name, status, detail in p['checks']:
        check_stats.setdefault(name, {'✅': 0, '❌': 0})
        if '✅' in status:
            check_stats[name]['✅'] += 1
        else:
            check_stats[name]['❌'] += 1

print(f"{'Check':<25} {'✅ Pass':>8} {'❌ Fail':>8} {'Status':>10}")
print(f"{'-'*25} {'-'*8} {'-'*8} {'-'*10}")
for cname, counts in sorted(check_stats.items()):
    total = counts['✅'] + counts['❌']
    status = '✅' if counts['❌'] == 0 else '❌'
    print(f"{cname:<25} {counts['✅']:>8} {counts['❌']:>8} {status:>10}")

print(f"\n{'='*70}")
print(f"POSTS THAT FAILED ({len(failed)}):")
print(f"{'='*70}")

for p in sorted(failed, key=lambda x: x['slug']):
    failing_checks = [c for c in p['checks'] if '❌' in c[1]]
    check_names = [c[0] for c in failing_checks]
    print(f"\n❌ {p['slug']}")
    for name, status, detail in failing_checks:
        print(f"   - {name}: {detail}")

print(f"\n{'='*70}")
print(f"ALL-PASS POSTS ({len(passed)}):")
for p in sorted(passed, key=lambda x: x['slug']):
    print(f"   ✅ {p['slug']}")

# Key action items
print(f"\n{'='*70}")
print("KEY ACTION ITEMS (most common failures):")
print(f"{'='*70}")

freq = {}
for p in failed:
    for name, _, _ in p['checks']:
        if '❌' in _:
            freq[name] = freq.get(name, 0) + 1

for name, count in sorted(freq.items(), key=lambda x: -x[1]):
    print(f"  - {name}: {count} posts affected")

print()
