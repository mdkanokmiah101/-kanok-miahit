#!/usr/bin/env python3
"""Extract posts from data.js by finding line ranges."""
import re, sys

with open('src/app/blog/data.js') as f:
    lines = f.readlines()

# Find all post starts (lines with "  {" that are standalone)
post_starts = []
for i, line in enumerate(lines):
    stripped = line.strip()
    if stripped == '{':
        # Check if next few lines contain slug:
        context = ''.join(lines[i:i+10])
        if 'slug:' in context:
            post_starts.append(i)

# Find post ends by brace matching
posts = []
for start_idx in post_starts:
    depth = 0
    i = start_idx
    while i < len(lines):
        for ch in lines[i]:
            if ch == '{': depth += 1
            elif ch == '}': depth -= 1
        if depth <= 0:
            posts.append((start_idx, i))
            break
        i += 1

# Map slug -> line range
post_by_slug = {}
for start, end in posts:
    block_text = ''.join(lines[start:end+1])
    m = re.search(r'slug:\s*"([^"]+)"', block_text)
    if m:
        slug = m.group(1)
        post_by_slug[slug] = (start, end, block_text)

# Target slugs to check
targets = [
    'locksmith-dundee-seo-case-study',
    'how-to-choose-best-seo-expert-dhaka-15-things',
    'seo-expert-vs-seo-agency-dhaka-which-is-right',
    'top-10-seo-mistakes-dhaka-businesses-fix',
    'what-does-seo-expert-do-guide-business-owners',
    'seo-case-study-dhaka-businesses-increased-organic-traffic',
    'hiring-seo-expert-dhaka-better-roi-than-paid-ads',
    'ai-seo-2026-dhaka-experts-optimize-google-ai-chatgpt',
    'watchzonebd-seo-case-study',
]

def extract_field(block, field_name):
    """Extract a simple string/array field from the block."""
    # Try title: "value"
    m = re.search(rf'^\s+{field_name}:\s*"([^"]*)"', block, re.MULTILINE)
    if m: return m.group(1)
    # Try title:\n    "value"
    m = re.search(rf'{field_name}:\n\s+"([^"]*)"', block)
    if m: return m.group(1)
    return ''

def extract_content(block):
    """Extract content between backticks."""
    # Find content: then the first backtick
    idx = block.find('content:')
    if idx < 0: return ''
    rest = block[idx:]
    bt_start = rest.find('`')
    if bt_start < 0: return ''
    bt_end = rest.rfind('`')
    if bt_end <= bt_start: return ''
    return rest[bt_start+1:bt_end]

def extract_tags(block):
    """Extract tags from block."""
    m = re.search(r'tags:\s*\[([^\]]*)\]', block, re.DOTALL)
    if m:
        tag_str = m.group(1)
        tags = re.findall(r'"([^"]+)"', tag_str)
        return tags
    return []

for slug in targets:
    if slug not in post_by_slug:
        print(f"⚠️  {slug}: NOT FOUND in data.js")
        continue
    
    start, end, block = post_by_slug[slug]
    title = extract_field(block, 'title')
    date = extract_field(block, 'date')
    excerpt = extract_field(block, 'excerpt')
    author = extract_field(block, 'author')
    tags = extract_tags(block)
    content = extract_content(block)
    
    print(f"\n{'#'*70}")
    print(f"# Post: {slug}")
    print(f"# Title: {title[:100]}")
    print(f"# Date: {date}  |  Lines: {start+1}-{end+1}")
    print(f"{'#'*70}")
    print(f"Content length: {len(content)} chars")
    
    if not content:
        print("⚠️  Empty content!")
        continue
    
    # ===== A. TF-IDF Coverage =====
    # Get keyword from title (remove leading question/action words)
    title_lower = title.lower()
    # Remove prefix words
    for prefix in ['how to choose the best', 'what does an', 'top 10', 'how to', 'what is', 
                   'what does', 'why', 'is', 'are', 'can', 'do', 'does', 'the', 'a', 'an',
                   'seo case study', 'case study']:
        if title_lower.startswith(prefix + ' '):
            title_lower = title_lower[len(prefix)+1:]
            break
    
    # Get first meaningful 2-3 word phrase
    words = [w for w in title_lower.split() if w not in {'a','an','the','in','for','of','to','and','or',
             'is','are','was','were','be','have','has','do','does','did','with','from','by','at','on',
             'your','our','their','its','it','we','you','they','this','that','how','what','why','when',
             'where','which','who','can','will','would','should','may','might','must','not','no','but',
             'all','each','every','some','any','into','than','then','also','very','just'} and len(w) > 2]
    
    primary_kw = ' '.join(words[:3]) if words else title_lower.split()[0] if title_lower.split() else ''
    
    if primary_kw:
        kw_count = content.lower().count(primary_kw)
    else:
        kw_count = 0
    
    # Also check individual keyword words
    indiv_counts = {}
    for w in words[:3]:
        if len(w) > 2:
            indiv_counts[w] = content.lower().count(w)
    
    total_meaningful = sum(indiv_counts.values())
    tfidf_ok = total_meaningful >= 5 or kw_count >= 3
    
    # ===== B. Entity Coverage =====
    c_lower = content.lower()
    entity_checks = {
        'Dhaka': 'dhaka' in c_lower,
        'Bangladesh': 'bangladesh' in c_lower,
        'SEO': 'seo' in c_lower,
        'Google': 'google' in c_lower,
        'Author name': author.lower().split()[-1] in c_lower if author else False,
    }
    
    # Business-specific entities
    if 'case study' in title.lower() or 'case study' in [t.lower() for t in tags]:
        entity_checks['Results/data'] = any(w in c_lower for w in ['results', 'traffic', 'rankings', 'increased', 'growth'])
    
    missing_entities = [k for k, v in entity_checks.items() if not v]
    entity_ok = len(missing_entities) == 0
    
    # ===== C. Pillar-Cluster Alignment =====
    tag_lower = [t.lower() for t in tags]
    
    pillar_map = {
        'seo guide': '/',
        'local seo': '/services/local-seo',
        'technical seo': '/services/technical-seo',
        'case study': '/blog/seo-case-study-dhaka-businesses-increased-organic-traffic',
        'seo case study': '/blog/seo-case-study-dhaka-businesses-increased-organic-traffic',
        'ai seo': '/services/geo-ai-search',
        'geo': '/services/geo-ai-search',
        'geo optimization': '/services/geo-ai-search',
        'ecommerce': '/services/ecommerce-seo',
        'e-commerce': '/services/ecommerce-seo',
        'seo expert': '/',
        'seo agency': '/',
        'hire seo': '/',
        'seo mistakes': '/',
        'seo roi': '/',
        'seo services': '/',
        'seo services bangladesh': '/',
        'seo tips bangladesh': '/',
        'digital marketing bangladesh': '/',
        'organic traffic': '/',
        'seo results bangladesh': '/',
        'seo expert dhaka': '/',
        'seo expert guide': '/',
        'dhaka seo': '/',
        'dhaka seo expert': '/',
    }
    
    pillar_url = '/'
    for tag in tag_lower:
        for key, url in pillar_map.items():
            if key in tag:
                pillar_url = url
                break
        if pillar_url != '/':
            break
    
    pillar_link_count = content.count(pillar_url)
    pillar_ok = pillar_link_count >= 1
    
    # ===== D. AEO/GEO Optimization =====
    question_starts = {'How', 'What', 'Why', 'When', 'Where', 'Can', 'Do', 'Does', 'Is', 'Are', 'Which', 'Who'}
    question_heading_count = 0
    
    for line in content.split('\n'):
        stripped = line.strip()
        if stripped.startswith('##') or stripped.startswith('###'):
            heading_text = stripped.lstrip('#').strip()
            first_word = heading_text.split()[0] if heading_text.split() else ''
            if first_word in question_starts and '?' in heading_text:
                question_heading_count += 1
    
    aeo_ok = question_heading_count >= 2
    
    # ===== E. Internal Links =====
    internal_links = re.findall(r'\[([^\]]*)\]\((/[^\)\s]+)\)', content)
    # Filter out anchors, external URLs, email links
    valid_links = [(t, u) for t, u in internal_links 
                   if not u.startswith('//') and not u.startswith('/#') and not u.startswith('/cdn-cgi/')]
    links_ok = len(valid_links) >= 3
    
    # ===== F. Schema Ready =====
    schema_ok = bool(title) and bool(excerpt) and bool(date) and bool(author)
    
    # ===== SUMMARY TABLE =====
    print(f"\n## Framework Check Results")
    print(f"| Check | Status | Details |")
    print(f"|-------|--------|---------|")
    
    tfidf_detail = f"{kw_count} phrase occurrences, total {total_meaningful} key term occurrences"
    print(f"| TF-IDF: '{primary_kw[:40]}' | {'✅' if tfidf_ok else '❌'} | {tfidf_detail} |")
    
    entity_detail = f"All entities present" if entity_ok else f"Missing: {', '.join(missing_entities)}"
    print(f"| Entities | {'✅' if entity_ok else '❌'} | {entity_detail} |")
    
    pillar_detail = f"Links to {pillar_url}: {pillar_link_count}x" if pillar_ok else f"No link to pillar ({pillar_url})"
    print(f"| Pillar Link | {'✅' if pillar_ok else '❌'} | {pillar_detail} |")
    
    print(f"| AEO/GEO | {'✅' if aeo_ok else '❌'} | {question_heading_count} question-based headings |")
    
    # Count by type
    blog_l = sum(1 for _, u in valid_links if '/blog/' in u)
    serv_l = sum(1 for _, u in valid_links if '/services/' in u)
    ind_l = sum(1 for _, u in valid_links if '/industries/' in u)
    home_l = sum(1 for _, u in valid_links if u == '/')
    other_l = len(valid_links) - blog_l - serv_l - ind_l - home_l
    
    print(f"| Internal Links | {'✅' if links_ok else '❌'} | {len(valid_links)} total (blog:{blog_l}, services:{serv_l}, industries:{ind_l}, home:{home_l}, other:{other_l}) |")
    
    schema_detail_parts = []
    if title: schema_detail_parts.append(f"title: ✅ ({len(title)} chars)")
    else: schema_detail_parts.append("title: ❌")
    if excerpt: schema_detail_parts.append(f"excerpt: ✅ ({len(excerpt)} chars)")
    else: schema_detail_parts.append("excerpt: ❌")
    if date: schema_detail_parts.append(f"date: ✅ ({date})")
    else: schema_detail_parts.append("date: ❌")
    if author: schema_detail_parts.append(f"author: ✅ ({author})")
    else: schema_detail_parts.append("author: ❌")
    
    print(f"| Schema Ready | {'✅' if schema_ok else '❌'} | {', '.join(schema_detail_parts)} |")
    
    # ===== FIX INSTRUCTIONS =====
    fixes = []
    if not tfidf_ok:
        fixes.append(f"- Increase keyword '{primary_kw}' usage in content (currently {kw_count} phrase matches, need ≥5 key term occurrences)")
    if not entity_ok:
        fixes.append(f"- Add missing entities: {', '.join(missing_entities)}")
    if not pillar_ok:
        fixes.append(f"- Add internal link to pillar page: {pillar_url}")
    if not aeo_ok:
        fixes.append(f"- Add {2 - question_heading_count} more question-based headings (e.g., 'How does...?', 'What is...?', 'Why choose...?')")
    if not links_ok:
        fixes.append(f"- Add {3 - len(valid_links)} more internal links to other posts, services, or industry pages")
    if not schema_ok:
        schema_missing = []
        if not title: schema_missing.append('title')
        if not excerpt: schema_missing.append('excerpt')
        if not date: schema_missing.append('date')
        if not author: schema_missing.append('author')
        fixes.append(f"- Set missing schema fields: {', '.join(schema_missing)}")
    
    if fixes:
        print(f"\n### Fix instructions:")
        for f in fixes:
            print(f)
    else:
        print(f"\n✅ All checks pass — no fixes needed.")
