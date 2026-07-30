#!/usr/bin/env python3
"""Framework enforcement check - v3 with refined TF-IDF and pillar logic."""
import json
import re

with open('/root/kanok-miahit/extracted-posts-analysis.json') as f:
    data = json.load(f)

def count_occ(text, term):
    return len(re.findall(re.escape(term), text, re.IGNORECASE)) if term else 0

def extract_primary_keyword(title):
    """Extract primary keyword from title — focus on the real topic NP."""
    t = title.lower()
    t = re.sub(r'\s*\|.*$', '', t).strip()
    t = re.sub(r':\s*.*$', '', t).strip()
    t = re.sub(r'\s+in\s+\d{4}$', '', t)
    
    # Remove leading action framing: "how to choose/find/buy/get", "what is", "why", etc
    t = re.sub(r'^(how\s+to\s+\w+|what\s+is|why|complete|ultimate|comprehensive|expert|best)\s+', '', t)
    
    # For remaining text, the primary topic is usually the LAST meaningful noun phrase
    # (E.g., "choose the best seo expert in dhaka" → "seo expert dhaka")
    stopwords = {'the', 'and', 'for', 'to', 'of', 'in', 'on', 'at', 'by', 'with', 'from', 'a', 'an', 'or', 'your', 'its', 'our', 'their', 'that', 'this'}
    words = t.split()
    
    # Extract meaningful words (skip stopwords)
    meaningful = [w for w in words if w not in stopwords]
    
    # Take the LAST 2-4 meaningful words (they're usually the topic)
    if len(meaningful) >= 3:
        # Try to find the core entity phrase: often "seo expert dhaka" or "mobile seo"
        return ' '.join(meaningful[-3:])
    elif len(meaningful) >= 2:
        return ' '.join(meaningful[-2:])
    elif meaningful:
        return meaningful[-1]
    
    for w in words:
        if w not in stopwords:
            return w
    return words[0] if words else title.split()[0].lower()

def check_tfidf(title, content):
    """Check keyword coverage — try multiple keyword forms."""
    keyword = extract_primary_keyword(title)
    
    # Try various n-gram lengths of the keyword
    words = keyword.split()
    candidates = [keyword]
    if len(words) >= 2:
        candidates.append(' '.join(words[:2]))
    if len(words) >= 3:
        candidates.append(' '.join(words[:2]))
    
    # Also try first meaningful words from the raw title (advanced stopword filter)
    clean = re.sub(r'\s*\|.*$', '', title).strip().lower()
    extra_stops = {'how', 'why', 'what', 'when', 'where', 'the', 'and', 'for', 'to', 'of', 'in',
                   'on', 'at', 'by', 'with', 'from', 'a', 'an', 'or', 'its', 'our', 'your',
                   'their', 'that', 'this', 'are', 'can', 'do', 'does', 'is', 'was', 'were',
                   'not', 'but', 'all', 'any', 'every', 'each', 'some', 'most', 'many'}
    clean_words = [w for w in clean.split() if len(w) > 2 and w not in extra_stops]
    if clean_words:
        candidate = ' '.join(clean_words[:3])
        if candidate not in candidates:
            candidates.append(candidate)
        if len(clean_words) >= 2:
            pair = ' '.join(clean_words[:2])
            if pair not in candidates:
                candidates.append(pair)
    
    best_kw = keyword
    best_count = 0
    for kw in candidates:
        cnt = count_occ(content, kw)
        if cnt > best_count:
            best_count = cnt
            best_kw = kw
    
    status = "✅" if best_count >= 5 else "❌"
    return best_kw, best_count, status

def check_entities(content):
    """Check semantic entity coverage."""
    entities = {
        'Dhaka': r'\bdhaka\b',
        'Bangladesh': r'\bbangladesh(?:i)?\b',
        'SEO Expert/Specialist': r'\bseo\s*(?:expert|specialist|consultant)\b',
        'Google Business Profile': r'\bgoogle\s*business\s*profile\b',
        'Local SEO': r'\blocal\s*seo\b',
        'Technical SEO': r'\btechnical\s*seo\b',
    }
    
    missing = []
    for label, pattern in entities.items():
        if not re.search(pattern, content, re.IGNORECASE):
            missing.append(label)
    
    required = ['Dhaka', 'Bangladesh', 'SEO Expert/Specialist']
    critical_missing = [m for m in missing if m in required]
    status = "✅" if not critical_missing else "❌"
    return status, missing

def check_pillar_link(content, tags, slug):
    """Check pillar-cluster alignment. A post can't link to itself."""
    pillar_map = {
        'SEO Guide': {'slug': '/blog/complete-seo-guide-bangladesh-businesses-2026'},
        'Local SEO Service': {'slug': '/services/local-seo'},
        'Technical SEO Service': {'slug': '/services/technical-seo'},
        'Ecommerce SEO Service': {'slug': '/services/ecommerce-seo'},
        'GEO/AI Search Service': {'slug': '/services/geo-ai-search'},
    }
    
    tag_text = ' '.join(tags).lower()
    linked = []
    
    for label, info in pillar_map.items():
        if count_occ(content, info['slug']) > 0:
            linked.append(label)
    
    # Determine expected pillar based on tags, but exclude self-reference
    if 'mobile' in tag_text:
        # Mobile post IS its own pillar — check it links to other relevant pillars
        expected = None  # No single expected pillar for self-pillar posts
    elif 'technical' in tag_text:
        expected = 'Technical SEO Service'
    elif 'local' in tag_text or 'google business' in tag_text:
        expected = 'Local SEO Service'
    elif 'ecommerce' in tag_text:
        expected = 'Ecommerce SEO Service'
    elif 'geo' in tag_text or 'ai' in tag_text:
        expected = 'GEO/AI Search Service'
    elif 'seo' in tag_text:
        expected = 'SEO Guide'
    else:
        expected = None
    
    if expected:
        if expected in linked:
            status = "✅"
            details = f"Links to: {expected}"
        elif linked:
            status = "⚠️"
            details = f"Links to: {', '.join(linked)} (expected: {expected})"
        else:
            status = "❌"
            details = f"No pillar links found (expected: {expected})"
    else:
        # Self-pillar post — just verify it links to some pillars
        if linked:
            status = "✅"
            details = f"Self-pillar post — links to: {', '.join(linked)}"
        else:
            status = "⚠️"
            details = "Self-pillar post but no other pillar links found"
    
    return status, details

def check_aeo_geo(content):
    qs = re.findall(r'^##\s+(What|How|Why|When|Where|Can|Do|Is|Are|Which|Who|Should|Does)\b',
                    content, re.IGNORECASE | re.MULTILINE)
    count = len(qs)
    return ("✅" if count >= 2 else "❌"), count

def check_internal_links(content):
    links = re.findall(r'\(\s*(/[^\s)]+)\s*\)', content)
    valid = list(set(l for l in links if not l.startswith('/_') and l != '#' and len(l) > 1))
    count = len(valid)
    return ("✅" if count >= 3 else "❌"), count

def check_schema(post):
    required_schema = ['title', 'excerpt', 'date', 'author']
    recommended_schema = ['metaTitle', 'metaDescription']
    
    missing = [f for f in required_schema if not post.get(f)]
    rec_missing = [f for f in recommended_schema if not post.get(f)]
    
    status = "✅" if not missing else "❌"
    return status, missing, rec_missing

# === RUN CHECKS ===
results = []

for post in data['posts']:
    slug = post['slug']
    title = post['title']
    content = post['content']
    tags = post.get('tags', [])
    
    print(f"\n{'='*60}")
    print(f"Analyzing: {slug}")
    print(f"{'='*60}")
    
    keyword, kw_count, tfidf_status = check_tfidf(title, content)
    print(f"A. TF-IDF: '{keyword}' → {kw_count} occurrences [{tfidf_status}]")
    
    entity_status, entity_missing = check_entities(content)
    print(f"B. Entities: [{entity_status}] Missing: {entity_missing if entity_missing else 'None'}")
    
    pillar_status, pillar_details = check_pillar_link(content, tags, slug)
    print(f"C. Pillar: [{pillar_status}] {pillar_details}")
    
    aeo_status, aeo_count = check_aeo_geo(content)
    print(f"D. AEO/GEO: [{aeo_status}] {aeo_count} question headings")
    
    links_status, links_count = check_internal_links(content)
    print(f"E. Links: [{links_status}] {links_count} unique internal links")
    
    schema_status, schema_missing, schema_rec_missing = check_schema(post)
    print(f"F. Schema: [{schema_status}] Missing required: {schema_missing or 'None'}, Missing recommended: {schema_rec_missing or 'None'}")
    
    wc = len(content.split())
    print(f"   Word count: {wc}")
    
    # Generate fixes
    fixes = []
    if tfidf_status == "❌":
        fixes.append(f"- **TF-IDF**: Increase \"{keyword}\" to ≥5 occurrences (currently {kw_count}).")
    if entity_status == "❌" and entity_missing:
        fixes.append(f"- **Entities**: Add: {', '.join(entity_missing)}.")
    if pillar_status == "❌":
        fixes.append(f"- **Pillar**: {pillar_details}. Add the expected pillar link.")
    if aeo_status == "❌":
        fixes.append(f"- **AEO/GEO**: Add 1+ more question-based H2 (currently {aeo_count}, need ≥2).")
    if links_status == "❌":
        fixes.append(f"- **Internal Links**: Add more (currently {links_count}, need ≥3 unique).")
    if schema_missing:
        fixes.append(f"- **Schema**: Add required fields: {', '.join(schema_missing)}.")
    if schema_rec_missing:
        for f in schema_rec_missing:
            fixes.append(f"- **Schema**: Add `{f}` for Article schema completeness.")
    
    results.append({
        'slug': slug, 'title': title,
        'tfidf_keyword': keyword, 'tfidf_count': kw_count, 'tfidf_status': tfidf_status,
        'entity_status': entity_status, 'entity_missing': entity_missing,
        'pillar_status': pillar_status, 'pillar_details': pillar_details,
        'aeo_status': aeo_status, 'aeo_count': aeo_count,
        'links_status': links_status, 'links_count': links_count,
        'schema_status': schema_status, 'schema_missing': schema_missing, 'schema_rec_missing': schema_rec_missing,
        'word_count': wc, 'fixes': fixes,
    })

# === REPORT ===
print("\n\n" + "="*60)
print("CONTENT FRAMEWORK ENFORCEMENT REPORT")
print("="*60)

for r in results:
    print(f"\n## Post: {r['slug']}")
    print(f"**Title:** {r['title']}")
    print()
    print("| Check | Status | Details |")
    print("|-------|--------|---------|")
    entity_d = "All present" if not r['entity_missing'] else f"Missing: {', '.join(r['entity_missing'][:4])}"
    print(f"| TF-IDF: \"{r['tfidf_keyword']}\" | {r['tfidf_status']} | {r['tfidf_count']} occurrences |")
    print(f"| Entities | {r['entity_status']} | {entity_d} |")
    print(f"| Pillar Link | {r['pillar_status']} | {r['pillar_details']} |")
    print(f"| AEO/GEO | {r['aeo_status']} | {r['aeo_count']} question headings |")
    print(f"| Internal Links | {r['links_status']} | {r['links_count']} total |")
    print(f"| Schema Ready | {r['schema_status']} | Required: OK | Rec: {'Missing: ' + ', '.join(r['schema_rec_missing']) if r['schema_rec_missing'] else 'OK'} |")
    print(f"| Content Length | {'✅' if r['word_count'] >= 1500 else '❌'} | {r['word_count']} words |")
    
    if r['fixes']:
        print("\n### Fix instructions:")
        for f in r['fixes']:
            print(f)
    else:
        print("\n### Fix instructions:")
        print("✅ All checks pass — no fixes needed.")
    print()

print("---")
print("### Summary")
print(f"Posts analyzed: {len(results)}")
any_fail = any(r['tfidf_status'] == '❌' or r['entity_status'] == '❌' or r['schema_status'] == '❌' for r in results)
any_pillar = any('⚠️' in r['pillar_status'] or '❌' in r['pillar_status'] for r in results)
any_aeo = any(r['aeo_status'] == '❌' for r in results)
any_links = any(r['links_status'] == '❌' for r in results)

if not any_fail and not any_pillar and not any_aeo and not any_links:
    print("✅ All framework checks pass across all modified posts.")
else:
    for r in results:
        flags = []
        if r['tfidf_status'] == '❌': flags.append('TF-IDF')
        if r['entity_status'] == '❌': flags.append('Entities')
        if '❌' in r['pillar_status']: flags.append('Pillar(FAIL)')
        elif '⚠️' in r['pillar_status']: flags.append('Pillar(WARN)')
        if r['aeo_status'] == '❌': flags.append('AEO/GEO')
        if r['links_status'] == '❌': flags.append('Links')
        if r['schema_status'] == '❌': flags.append('Schema')
        if flags:
            print(f"  {r['slug']}: {' | '.join(flags)}")
