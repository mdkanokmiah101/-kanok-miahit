#!/usr/bin/env python3
"""Framework enforcement check for modified blog posts - v2."""
import json
import re

# Load the extracted data
with open('/root/kanok-miahit/extracted-posts-analysis.json') as f:
    data = json.load(f)

def count_occurrences(text, term):
    """Count case-insensitive occurrences of term in text."""
    if not term:
        return 0
    return len(re.findall(re.escape(term), text, re.IGNORECASE))

def extract_primary_keyword(title):
    """Extract primary keyword from title."""
    t = title.lower()
    # Remove trailing "| Kanok Miah" etc
    t = re.sub(r'\s*\|.*$', '', t)
    t = re.sub(r':\s+.*$', '', t)
    t = re.sub(r'\s+in\s+\d{4}$', '', t)
    # Take first 2-4 key words, skip stopwords at start
    stopwords = {'a', 'an', 'the', 'for', 'to', 'of', 'in', 'on', 'at', 'by', 'with', 'from', 'and', 'or', 'is', 'are'}
    words = t.split()
    # Skip leading "how", "what", "why" etc if title is a question
    skip = {'how', 'what', 'why', 'when', 'where', 'which', 'can', 'do', 'does', 'is', 'are'}
    if words and words[0] in skip:
        words = words[1:]
    # Remove trailing stopwords
    while words and words[-1] in stopwords:
        words = words[:-1]
    # Take 2-4 words
    kw = ' '.join(words[:4])
    if not kw:
        kw = title.split()[0].lower()
    return kw

def check_tfidf(title, content):
    """Check TF-IDF keyword coverage."""
    keyword = extract_primary_keyword(title)
    # Also try the first 2 words separately
    words = keyword.split()
    
    best_count = 0
    best_kw = keyword
    for n in range(len(words), 0, -1):
        sub_kw = ' '.join(words[:n])
        cnt = count_occurrences(content, sub_kw)
        if cnt > best_count:
            best_count = cnt
            best_kw = sub_kw
    
    # Also try title's key noun phrase
    # For "mobile seo for bangladesh" -> try "mobile seo"
    if ' ' in best_kw:
        first_two = ' '.join(best_kw.split()[:2])
        cnt2 = count_occurrences(content, first_two)
        if cnt2 > best_count:
            best_count = cnt2
            best_kw = first_two
    
    status = "✅" if best_count >= 5 else "❌"
    return best_kw, best_count, status

def check_entities(content, title_lower):
    """Check semantic entity coverage."""
    entities = {
        'location_dhaka': {'terms': ['dhaka'], 'label': 'Dhaka'},
        'location_bangladesh': {'terms': ['bangladesh', 'bangladeshi'], 'label': 'Bangladesh'},
        'entity_seo_expert': {'terms': ['seo expert', 'seo specialist', 'seo consultant'], 'label': 'SEO Expert/Specialist'},
        'entity_gbp': {'terms': ['google business profile', 'gbp'], 'label': 'Google Business Profile'},
        'entity_local_seo': {'terms': ['local seo'], 'label': 'Local SEO'},
        'entity_technical_seo': {'terms': ['technical seo'], 'label': 'Technical SEO'},
    }
    
    missing = []
    for key, entity in entities.items():
        found = any(count_occurrences(content, t) > 0 for t in entity['terms'])
        if not found:
            missing.append(entity['label'])
    
    # Required for all posts
    required = ['location_dhaka', 'location_bangladesh']
    if 'seo' in title_lower:
        required.append('entity_seo_expert')
    
    critical_missing = [entities[k]['label'] for k in required if k in entities and entities[k]['label'] in missing]
    status = "✅" if not critical_missing else "❌"
    return status, missing

def check_pillar_link(content, tags, slug):
    """Check pillar-cluster alignment."""
    pillar_map = {
        'seo': {'slug': '/blog/complete-seo-guide-bangladesh-businesses-2026', 'label': 'SEO Guide Pillar'},
        'local': {'slug': '/services/local-seo', 'label': 'Local SEO Service Pillar'},
        'technical': {'slug': '/services/technical-seo', 'label': 'Technical SEO Service Pillar'},
        'ecommerce': {'slug': '/services/ecommerce-seo', 'label': 'Ecommerce SEO Service Pillar'},
        'geo': {'slug': '/services/geo-ai-search', 'label': 'GEO/AI Search Service Pillar'},
    }
    
    tag_text = ' '.join(tags).lower()
    linked_pillars = []
    
    for key, pillar in pillar_map.items():
        if count_occurrences(content, pillar['slug']) > 0:
            linked_pillars.append(pillar['label'])
    
    # Determine which pillar based on tags
    if 'mobile' in tag_text:
        target_pillar = {'slug': '/blog/mobile-seo-optimization-bangladesh-mobile-first-era', 'label': 'Mobile SEO (self-pillar)'}
    elif 'technical' in tag_text:
        target_pillar = pillar_map['technical']
    elif 'local' in tag_text:
        target_pillar = pillar_map['local']
    elif 'ecommerce' in tag_text:
        target_pillar = pillar_map['ecommerce']
    elif 'geo' in tag_text or 'ai' in tag_text:
        target_pillar = pillar_map['geo']
    elif 'seo' in tag_text:
        target_pillar = pillar_map['seo']
    else:
        target_pillar = None
    
    if not linked_pillars:
        status = "❌"
        details = "No pillar/service links found"
    elif target_pillar and target_pillar['label'] in linked_pillars:
        status = "✅"
        details = f"Links to: {target_pillar['label']}"
    else:
        detail_str = ', '.join(linked_pillars)
        expected = target_pillar['label'] if target_pillar else 'N/A'
        status = "⚠️"
        details = f"Links to: {detail_str} (expected: {expected})"
    
    return status, details, target_pillar

def check_aeo_geo(content):
    """Check AEO/GEO optimization - question-based headings."""
    question_pattern = re.findall(
        r'^##\s+(What|How|Why|When|Where|Can|Do|Is|Are|Which|Who|Should|Does)\b',
        content, re.IGNORECASE | re.MULTILINE
    )
    count = len(question_pattern)
    status = "✅" if count >= 2 else "❌"
    return status, count

def check_internal_links(content):
    """Count internal links to other posts, services, locations."""
    links = re.findall(r'\(\s*(/[^\s)]+)\s*\)', content)
    valid = [l for l in links if not l.startswith('/_') and l != '#' and len(l) > 1]
    # Remove duplicates
    unique = list(set(valid))
    count = len(unique)
    status = "✅" if count >= 3 else "❌"
    return status, count

def check_schema(post):
    """Check if post has fields needed for ArticleSchema."""
    missing = []
    if not post.get('title'):
        missing.append('title')
    if not post.get('excerpt'):
        missing.append('excerpt')
    if not post.get('date'):
        missing.append('date')
    if not post.get('author'):
        missing.append('author')
    if not post.get('metaTitle'):
        missing.append('metaTitle')
    if not post.get('metaDescription'):
        missing.append('metaDescription')
    
    status = "✅" if len(missing) == 0 else "❌"
    return status, missing

# === Run checks ===
results = []

for post in data['posts']:
    slug = post['slug']
    title = post['title']
    content = post['content']
    tags = post.get('tags', [])
    
    print(f"\n{'='*60}")
    print(f"Analyzing: {slug}")
    print(f"Title: {title}")
    print(f"{'='*60}")
    
    # A. TF-IDF
    keyword, count, tfidf_status = check_tfidf(title, content)
    print(f"\nA. TF-IDF Coverage:")
    print(f"   Keyword: '{keyword}' | Occurrences: {count} | Status: {tfidf_status}")
    
    # B. Entities
    entity_status, entity_missing = check_entities(content, title.lower())
    print(f"\nB. Entity Coverage:")
    print(f"   Status: {entity_status}")
    if entity_missing:
        print(f"   Missing: {', '.join(entity_missing)}")
    else:
        print(f"   All key entities present")
    
    # C. Pillar-Cluster
    pillar_status, pillar_details, pillar_target = check_pillar_link(content, tags, slug)
    print(f"\nC. Pillar-Cluster Alignment:")
    print(f"   Status: {pillar_status} | {pillar_details}")
    
    # D. AEO/GEO
    aeo_status, aeo_count = check_aeo_geo(content)
    print(f"\nD. AEO/GEO Optimization:")
    print(f"   Status: {aeo_status} | Question headings: {aeo_count}")
    
    # E. Internal Links
    links_status, links_count = check_internal_links(content)
    print(f"\nE. Internal Linking:")
    print(f"   Status: {links_status} | Count: {links_count}")
    
    # F. Schema
    schema_status, schema_missing = check_schema(post)
    print(f"\nF. Schema Ready:")
    print(f"   Status: {schema_status}")
    if schema_missing:
        print(f"   Missing fields: {', '.join(schema_missing)}")
    else:
        print(f"   All fields set")
    
    # Word count
    word_count = len(content.split())
    wc_status = "✅" if word_count >= 1500 else "❌"
    print(f"\n   Content Length: {word_count} words ({wc_status})")
    
    # Generate fix instructions
    fixes = []
    
    if tfidf_status == "❌":
        fixes.append(f"- **TF-IDF**: Increase occurrence of \"{keyword}\" to at least 5 times (currently {count}).")
    
    if entity_status == "❌" and entity_missing:
        fixes.append(f"- **Entities**: Add missing entity mentions: {', '.join(entity_missing)}.")
    
    if pillar_status == "❌":
        if pillar_target:
            fixes.append(f"- **Pillar Link**: Add link to {pillar_target['slug']} ({pillar_target['label']}).")
        else:
            fixes.append(f"- **Pillar Link**: Add internal links to relevant SEO service pages.")
    
    if aeo_status == "❌":
        fixes.append(f"- **AEO/GEO**: Add more question-based H2s (currently {aeo_count}, need ≥2).")
    
    if links_status == "❌":
        fixes.append(f"- **Internal Links**: Add more internal links (currently {links_count}, need ≥3 unique).")
    
    if schema_status == "❌" and schema_missing:
        for fld in schema_missing:
            if fld in ['metaTitle', 'metaDescription']:
                fixes.append(f"- **Schema**: Add `{fld}` field for Article schema completeness.")
    
    results.append({
        'slug': slug,
        'title': title,
        'tfidf_keyword': keyword,
        'tfidf_count': count,
        'tfidf_status': tfidf_status,
        'entity_status': entity_status,
        'entity_missing': entity_missing,
        'pillar_status': pillar_status,
        'pillar_details': pillar_details,
        'aeo_status': aeo_status,
        'aeo_count': aeo_count,
        'links_status': links_status,
        'links_count': links_count,
        'schema_status': schema_status,
        'schema_missing': schema_missing,
        'word_count': word_count,
        'fixes': fixes,
    })

# === FINAL REPORT ===
print("\n\n" + "="*60)
print("FINAL FRAMEWORK ENFORCEMENT REPORT")
print("="*60)

for r in results:
    print(f"\n## Post: {r['slug']}")
    print(f"**Title:** {r['title']}")
    print("")
    print("| Check | Status | Details |")
    print("|-------|--------|---------|")
    entity_detail = "All key entities present" if not r['entity_missing'] else f"Missing: {', '.join(r['entity_missing'][:3])}"
    print(f"| TF-IDF: \"{r['tfidf_keyword']}\" | {r['tfidf_status']} | {r['tfidf_count']} occurrences |")
    print(f"| Entities | {r['entity_status']} | {entity_detail} |")
    print(f"| Pillar Link | {r['pillar_status']} | {r['pillar_details']} |")
    print(f"| AEO/GEO | {r['aeo_status']} | {r['aeo_count']} question headings |")
    print(f"| Internal Links | {r['links_status']} | {r['links_count']} total |")
    print(f"| Schema Ready | {r['schema_status']} | {'All fields set' if not r['schema_missing'] else 'Missing: ' + ', '.join(r['schema_missing'])} |")
    print(f"| Content Length | {'✅' if r['word_count'] >= 1500 else '❌'} | {r['word_count']} words |")
    
    if r['fixes']:
        print("\n### Fix instructions:")
        for fix in r['fixes']:
            print(fix)
    else:
        print("\n### Fix instructions:")
        print("✅ All checks pass — no fixes needed.")
    print("")

print("---")
print("### Summary")
print(f"Posts analyzed: {len(results)}")

flags = [r for r in results if any(status in r['tfidf_status'] + r['entity_status'] + r['aeo_status'] + r['links_status'] + r['schema_status'] for status in ['❌'])]
pillar_flags = [r for r in results if '⚠️' in r['pillar_status']]

if not flags and not pillar_flags:
    print("✅ All framework checks pass across all modified posts.")
else:
    print(f"⚠️  Issues found:")
    for r in results:
        issues = []
        if r['tfidf_status'] == '❌': issues.append('TF-IDF')
        if r['entity_status'] == '❌': issues.append('Entities')
        if '❌' in r['pillar_status']: issues.append('Pillar Link')
        if r['aeo_status'] == '❌': issues.append('AEO/GEO')
        if r['links_status'] == '❌': issues.append('Internal Links')
        if r['schema_status'] == '❌': issues.append('Schema')
        if issues:
            print(f"  ❌ {r['slug']}: {', '.join(issues)}")
        if '⚠️' in r['pillar_status']:
            print(f"  ⚠️ {r['slug']}: Pillar alignment suboptimal ({r['pillar_details']})")
