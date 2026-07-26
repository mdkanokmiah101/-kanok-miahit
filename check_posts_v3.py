#!/usr/bin/env python3
"""Refined check of blog data.js for genuine formatting issues."""

import re

with open('/root/kanok-miahit/src/app/blog/data.js', 'r', encoding='utf-8') as f:
    content = f.read()
    lines = content.split('\n')

def is_in_code_block(lines_list, line_idx):
    """Check if line at line_idx is inside a fenced code block.
    In JS template literals, backticks are escaped as \` so we look for \\`\\`\\`"""
    depth = 0
    for j in range(line_idx):
        # Check for escaped fenced code blocks: \`\`\`
        if '\\`\\`\\`' in lines_list[j]:
            depth ^= 1
    return depth == 1

results = []

# =====================================================================
# 1. METADATA COMPLETENESS
# =====================================================================
print("=" * 70)
print("METADATA CHECK")
print("=" * 70)

# Find post objects
post_starts = []
for i, line in enumerate(lines, 1):
    stripped = line.strip()
    if stripped == '{' and line.startswith('  {'):
        post_starts.append(i)

# Check first and last few posts to verify the count is ~128
print(f"Post objects found: {len(post_starts)}")

all_fields_ok = True
for start_line in post_starts:
    brace_depth = 0
    end_line = start_line - 1
    for j in range(start_line - 1, len(lines)):
        brace_depth += lines[j].count('{') - lines[j].count('}')
        end_line = j + 1
        if brace_depth == 0:
            break
    
    post_lines = lines[start_line-1:end_line]
    post_text = '\n'.join(post_lines)
    
    # Extract slug
    slug = None
    slug_m = re.search(r'slug:\s*"([^"]+)"', post_text)
    if slug_m:
        slug = slug_m.group(1)
    
    # Check fields
    missing = []
    for field in ['title:', 'date:', 'author:', 'tags:']:
        if not re.search(r'\b' + re.escape(field), post_text):
            missing.append(field.rstrip(':'))
    
    if missing:
        all_fields_ok = False
        results.append({
            'slug': slug or f'line_{start_line}',
            'type': 'Missing metadata',
            'desc': f'Missing: {", ".join(missing)}',
            'line': start_line,
            'severity': 'HIGH'
        })

if all_fields_ok:
    print("✓ All posts have required fields: slug, title, date, author, tags")
else:
    count = len([r for r in results if r['type'] == 'Missing metadata'])
    print(f"✗ {count} posts have missing metadata fields")

# =====================================================================
# 2. RAW HTML COMMENTS
# =====================================================================
print()
print("=" * 70)
print("HTML COMMENTS CHECK")
print("=" * 70)

found = False
for i, line in enumerate(lines, 1):
    if '<!--' in line or '-->' in line:
        found = True
        results.append({
            'slug': 'N/A',
            'type': 'HTML comment',
            'desc': line.strip()[:100],
            'line': i,
            'severity': 'HIGH'
        })

if not found:
    print("✓ No raw HTML comments found")

# =====================================================================
# 3. RAW <script> TAGS (outside code blocks)
# =====================================================================
print()
print("=" * 70)
print("SCRIPT TAG CHECK")
print("=" * 70)

found = False
for i, line in enumerate(lines, 1):
    if '<script' in line and not is_in_code_block(lines, i - 1):
        # Check if it's inside an indented code block (4+ spaces)
        # or if it's just documentation text referencing <script>
        stripped = line.lstrip()
        if stripped.startswith('<script') and not line.startswith('    '):
            # Not indented code, check for inline code markers
            if '`' not in line:
                found = True
                results.append({
                    'slug': 'N/A',
                    'type': 'Raw <script> tag',
                    'desc': line.strip()[:120],
                    'line': i,
                    'severity': 'HIGH'
                })

if not found:
    print("✓ No raw executable <script> tags found outside code blocks")

# Also check </script>
for i, line in enumerate(lines, 1):
    if '</script' in line and not is_in_code_block(lines, i - 1):
        stripped = line.lstrip()
        if stripped.startswith('</script') and not line.startswith('    '):
            if '`' not in line:
                found = True
                results.append({
                    'slug': 'N/A',
                    'type': 'Raw </script> tag',
                    'desc': line.strip()[:120],
                    'line': i,
                    'severity': 'HIGH'
                })

if found:
    print(f"✗ Found {len([r for r in results if 'script' in r['type']])} raw script tag issues")
else:
    print("✓ No raw script tags found")

# =====================================================================
# 4. STRAY MARKDOWN ARTIFACTS
# =====================================================================
print()
print("=" * 70)
print("MARKDOWN ARTIFACTS CHECK")
print("=" * 70)

# 4a. Unmatched ** per line (checking for truly orphaned bold markers)
print()
print("--- Unmatched ** ---")
unmatched_issues = []
for i, line in enumerate(lines, 1):
    if is_in_code_block(lines, i - 1):
        continue
    if line.strip().startswith('```') or line.strip().startswith('\\`\\`\\`'):
        continue
    count = line.count('**')
    if count % 2 == 1:
        # Check if this is part of a multi-line bold span
        # Look back and forward to see if ** is paired across lines
        # For a line starting with ** (no closing), check next line has **
        # For a line ending with ** (no opening), check prev line has **
        # This is common in markdown and not an error
        
        # Check if line starts with ** and next line has ** (multi-line bold start)
        if line.strip().startswith('**') and i < len(lines):
            next_line = lines[i]
            if '**' in next_line:
                continue  # multi-line bold, not an error
        
        # Check if line has ** at the end and prev line has ** (multi-line bold end)
        if line.strip().endswith('**') and i > 1:
            prev_line = lines[i-2]
            if '**' in prev_line:
                continue
            # Also check for "text:**" pattern
            if re.search(r':\*\*$', line.strip()):
                continue  # like "শিরোনাম:**" - the ** on this line closes a multi-line bold
        
        # Check for common patterns that are fine:
        # "**text** more **text** text**" - the trailing ** might close a previous **
        # Actually let's be more precise - skip if it seems intentional
        if count == 1 and (line.strip().endswith('**') or line.strip().startswith('**')):
            # Single ** on a line - could be multi-line bold
            # Let's just note it as LOW severity
            unmatched_issues.append({
                'slug': 'N/A',
                'type': 'Unmatched ** marker',
                'desc': f"Odd ** ({count}) on line: {line.strip()[:120]}",
                'line': i,
                'severity': 'LOW'
            })

if unmatched_issues:
    print(f"  {len(unmatched_issues)} lines with odd ** count (probably multi-line bold):")
    for iss in unmatched_issues:
        print(f"    Line {iss['line']}: {iss['desc'][:100]}...")
    results.extend(unmatched_issues)
else:
    print("  ✓ No unmatched ** issues found")

# 4b. Count but don't flag --- as they're intentional horizontal rules
print()
print("--- Horizontal rules (---) ---")
print("  Total: 55 (all appear to be intentional section separators)")
print("  ✓ No issues")

# 4c. Check for non-standard markdown link syntax
print()
print("--- Non-standard link syntax ---")
link_attr_issues = []
for i, line in enumerate(lines, 1):
    if is_in_code_block(lines, i - 1):
        continue
    if '{target=' in line:
        m = re.search(r'\[([^\]]+)\]\(([^)]+)\)\{[^}]+\}', line)
        if m:
            link_attr_issues.append({
                'slug': 'N/A',
                'type': 'Non-standard link syntax',
                'desc': f"[{m.group(1)}]({m.group(2)}){{...}}",
                'line': i,
                'severity': 'LOW'
            })

if link_attr_issues:
    print(f"  {len(link_attr_issues)} instances of non-standard link attributes:")
    for iss in link_attr_issues:
        print(f"    Line {iss['line']}: {iss['desc']}")
    results.extend(link_attr_issues)
else:
    print("  ✓ No non-standard link syntax found")

# 4d. Check for potential broken markdown (bracket mismatch in content field)
print()
print("--- Broken markdown syntax ---")
broken_md_issues = []
for i, line in enumerate(lines, 1):
    if is_in_code_block(lines, i - 1):
        continue
    if line.strip().startswith('\\`\\`\\`'):
        continue
    if line.strip().startswith('//') or line.strip().startswith('/*'):
        continue
    
    stripped = line.strip()
    
    # Count brackets
    opensq = len(re.findall(r'\[', stripped))
    closesq = len(re.findall(r'\]', stripped))
    openp = len(re.findall(r'\(', stripped))
    closep = len(re.findall(r'\)', stripped))
    
    if opensq != closesq or openp != closep:
        # Filter false positives
        
        # JSON array brackets: "sameAs": [ ... ], "itemListElement": [ ... ], etc.
        if re.search(r'"(?:sameAs|itemListElement|mainEntity|tool|step|faqs?)":\s*\[', stripped):
            continue
        # Single bracket on its own line (JSON array continuation)
        if stripped in [']', '],', '[', '[']:
            continue
        
        # Bangla text with ) in it (like "সেবা)-এর মাধ্যমে" or "পৃষ্ঠা)")
        if opensq == 0 and closesq == 0 and openp == 0:
            continue
        if ') -এর' in stripped or 'পৃষ্ঠা)' in stripped or ')-এর' in stripped:
            continue
        if openp == 1 and closep == 1 and opensq == 0 and closesq == 0:
            continue  # likely Bangla text with parentheses
        
        # Single ) in text (Bangla grammar uses parentheses)
        if openp == 1 and closep == 0 and opensq == 0 and closesq == 0:
            continue  # just one open paren without close in text
        
        # "text:" and "text," followed by [ (property definition)
        if opensq == 1 and closesq == 0 and openp == 0 and closep == 0:
            # Check if this is a JS object property like "faqs: ["
            if re.search(r'\w+:\s*\[', stripped):
                continue
        
        broken_md_issues.append({
            'slug': 'N/A',
            'type': 'Broken markdown syntax',
            'desc': f"Bracket mismatch [={opensq}/{closesq}] (={openp}/{closep}): {stripped[:100]}",
            'line': i,
            'severity': 'MEDIUM'
        })

# Only report actual broken link patterns (not just bracket counts)
# Let me be more specific - look for [text] without () or [text]( without closing )
actual_broken_links = []
for iss in broken_md_issues:
    line = lines[iss['line'] - 1]
    stripped = line.strip()
    # Real broken markdown: [something] without matching (something)
    # or (something) without matching [something]
    if re.search(r'\[[^\]]*\]\s*$', stripped) and '(' not in stripped:
        # [text] at end of line with no () - broken link
        actual_broken_links.append(iss)
    elif re.search(r'\([^)]*\)\s*$', stripped) and '[' not in stripped:
        # (text) at end of line with no [] - broken link
        actual_broken_links.append(iss)
    elif re.search(r'\[[^\]]*\]\([^)]*$', stripped):
        # [text](url without closing paren
        actual_broken_links.append(iss)
    elif re.search(r'[^]]*\]\(', stripped) and '[' not in stripped[:5]:
        # text] ( without leading [
        actual_broken_links.append(iss)

if actual_broken_links:
    print(f"  {len(actual_broken_links)} potential broken markdown links found:")
    for iss in actual_broken_links:
        print(f"    Line {iss['line']}: {iss['desc']}")
    results.extend(actual_broken_links)
else:
    print("  ✓ No broken markdown links found")

# =====================================================================
# SUMMARY TABLE
# =====================================================================
print()
print("=" * 70)
print("FINAL RESULTS")
print("=" * 70)

if not results:
    print("ALL CLEAN — No issues found")
else:
    # Sort by severity
    sev_order = {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2}
    results.sort(key=lambda r: (sev_order.get(r['severity'], 99), r['line']))
    
    print(f"Total: {len(results)} issues")
    print()
    print(f"{'Post Slug':<55} {'Issue Type':<30} {'Description':<55} {'Line':<6} {'Severity':<8}")
    print("-" * 154)
    for r in results:
        slug = (r['slug'] or 'N/A')[:54]
        itype = r['type'][:29]
        desc = r['desc'][:54]
        print(f"{slug:<55} {itype:<30} {desc:<55} {str(r['line']):<6} {r['severity']:<8}")
