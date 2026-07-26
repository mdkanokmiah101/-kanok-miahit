#!/usr/bin/env python3
"""Quick heading depth check for all posts."""
import re, sys

filepath = '/root/kanok-miahit/src/app/blog/data.js'
with open(filepath, 'r') as f:
    text = f.read()

lines = text.split('\n')
n = len(lines)
i = 0
total = 0
issues = []

while i < n:
    line = lines[i]
    stripped = line.strip()
    if stripped == '{' and i + 1 < n and 'slug:' in lines[i + 1]:
        slug_m = re.search(r'slug:\s*"([^"]*)"', lines[i + 1])
        if not slug_m:
            i += 1
            continue
        slug = slug_m.group(1)
        total += 1
        
        content_start = None
        j = i + 2
        while j < min(i + 30, n):
            if 'content:' in lines[j] and '`' in lines[j]:
                content_start = j
                break
            j += 1
        
        if content_start is not None:
            parts = []
            start_line = lines[content_start]
            bt = start_line.find('`')
            after = start_line[bt + 1:]
            if after.strip():
                parts.append(after)
            k = content_start + 1
            while k < n:
                cl = lines[k]
                bt2 = cl.find('`')
                if bt2 >= 0:
                    after2 = cl[bt2 + 1:].strip()
                    if after2 == '' or after2.startswith(',') or after2.startswith('//'):
                        before = cl[:bt2]
                        if before.strip():
                            parts.append(before)
                        break
                parts.append(cl)
                k += 1
            content = '\n'.join(parts)
            
            h_levels = [len(m.group(1)) for m in re.finditer(r'^(#{1,6})\s+', content, re.MULTILINE)]
            relevant = [h for h in h_levels if h in (2,3,4)]
            for idx in range(1, len(relevant)):
                if relevant[idx] > relevant[idx-1] + 1:
                    issues.append(f"{slug}: H{relevant[idx-1]}->H{relevant[idx]} at level H{relevant[idx-1]}->H{relevant[idx]}")
                    break
            i = k
            continue
    i += 1

print(f"Total posts checked: {total}")
print(f"Issues found: {len(issues)}")
for iss in issues[:20]:
    print(f"  {iss}")
if not issues:
    print("  None - all posts have proper heading hierarchy!")
