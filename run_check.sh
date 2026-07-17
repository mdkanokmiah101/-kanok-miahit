python3 << 'PYEOF'
import re
with open('/root/kanok-miahit/src/app/blog/data.js') as f:
    d = f.read()
si = d.index('slug: "technical-seo-core-web-vitals-optimization"')
cs = d.index('content: `', si)
ct = d.index('\n', cs) + 1
ci = d.index('`,\n  },\n  {', ct)
pc = d[ct:ci]
ms = d[si:cs]

print("="*70)
print("FRAMEWORK CHECKS: technical-seo-core-web-vitals-optimization")
print("="*70)

# A
pk = "টেকনিক্যাল SEO"
cnt = pc.count(pk)
print(f"\nA. TF-IDF COVERAGE")
print(f"   Primary keyword: '{pk}'")
print(f"   Occurrences: {cnt}")
print(f"   Verdict: {'PASS' if cnt>=5 else 'FAIL'} (threshold ≥5)")

# B
print(f"\nB. SEMANTIC ENTITY COVERAGE")
ents = [("Dhaka",["ঢাকা","Dhaka"]),("Bangladesh",["বাংলাদেশ","Bangladesh"]),("Technical SEO",["টেকনিক্যাল SEO"]),("Core Web Vitals",["কোর ওয়েব ভাইটালস","Core Web Vitals"]),("Page Speed",["পেজ স্পিড","Page Speed","সাইট স্পিড"]),("Web/Search Industry",["ওয়েবসাইট","সার্চ ইঞ্জিন"])]
all_e = True
for n,p in ents:
    f = any(x in pc for x in p)
    print(f"   {'PASS' if f else 'FAIL'} {n}")
    if not f: all_e = False

# C
print(f"\nC. PILLAR-CLUSTER ALIGNMENT")
tm = re.search(r'tags:\s*\[([^\]]+)\]', ms)
tags = [t.strip().strip('"') for t in tm.group(1).split(',')]
print(f"   Tags: {tags}")
print(f"   Pillar: টেকনিক্যাল SEO")
pillar = "/services/technical-seo" in pc
print(f"   Link to pillar: {'PASS' if pillar else 'FAIL'}")

# D
print(f"\nD. AEO/GEO OPTIMIZATION")
qh = []
for raw in pc.split('\n'):
    l = raw.strip()
    if not l.startswith('##'): continue
    is_q = any(qw in l for qw in ['কীভাবে','কী ','কোন ','কেন','কখন','কোথায়','কি '])
    is_q = is_q or bool(re.match(r'^##+\s+(How|What|Why|When|Where|Can|Do|Is|Are)\b', l, re.I))
    is_q = is_q or l.rstrip().endswith('?')
    if is_q: qh.append(l)
print(f"   Question headings: {len(qh)}")
for h in qh[:10]: print(f"     → {h}")
print(f"   Verdict: {'PASS' if len(qh)>=2 else 'FAIL'} (threshold ≥2)")

# E
print(f"\nE. INTERNAL LINKING")
u = set()
for pfx in ['/blog/','/services/','/industries/','/locations/']:
    for m in re.findall(r'\('+pfx+r'[^)]+\)', pc):
        u.add(m[1:-1])
print(f"   Unique internal links: {len(u)}")
for x in sorted(u): print(f"     - {x}")
print(f"   Verdict: {'PASS' if len(u)>=3 else 'FAIL'} (threshold ≥3)")

# F
print(f"\nF. SCHEMA (FIELD PRESENCE)")
flds = {'title':r'title:\s*"[^"]+"','excerpt':r'excerpt:\s*"[^"]+"','date':r'date:\s*"[^"]+"','author':r'author:\s*"[^"]+"','tags':r'tags:\s*\['}
all_f = True
for fn,pat in flds.items():
    p = bool(re.search(pat, ms))
    print(f"   {fn}: {'PASS' if p else 'FAIL'}")
    if not p: all_f = False

print("\n" + "="*70)
print("SUMMARY")
print("="*70)
print(f"A. TF-IDF Coverage:    {'PASS' if cnt>=5 else 'FAIL'} ({cnt} occurrences)")
print(f"B. Semantic Entities:  {'PASS' if all_e else 'FAIL'}")
print(f"C. Pillar-Cluster:     {'PASS' if pillar else 'FAIL'}")
print(f"D. AEO/GEO:            {'PASS' if len(qh)>=2 else 'FAIL'} ({len(qh)} question headings)")
print(f"E. Internal Linking:   {'PASS' if len(u)>=3 else 'FAIL'} ({len(u)} links)")
print(f"F. Schema Fields:      {'PASS' if all_f else 'FAIL'}")
print()
all_pass = all([cnt>=5, all_e, pillar, len(qh)>=2, len(u)>=3, all_f])
print(f"OVERALL: {'✅ ALL CHECKS PASSED' if all_pass else '❌ SOME CHECKS FAILED'}")
PYEOF