#!/usr/bin/env python3
"""Framework enforcement check for modified blog posts."""
import json
import re
import sys
sys.path.insert(0, '/root/kanok-miahit')

# Load the extracted data
with open('/root/kanok-miahit/extracted-posts-analysis.json') as f:
    data = json.load(f)

def count_occurrences(text, term):
    """Count case-insensitive occurrences of term in text."""
    if not term:
        return 0
    return len(re.findall(re.escape(term), text, re.IGNORECASE))

def extract_primary_keyword(title):
    """Extract primary keyword from title (first meaningful noun phrase)."""
    # Remove common prefixes
    title_lower = title.lower()
    
    # Strategy: Try to get the main topic
    # Remove "Complete Guide to", "How to", "Ultimate Guide", etc.
    patterns = [
        r'^(complete|ultimate|comprehensive|expert)\s+(guide|checklist|tips?)\s+(?:for|to|on)\s+(.+?)(?:\s+in\s+\d{4}|$|\s*[|:])',
        r'^(how\s+to\s+.+?)(?:\s*[|:]|\s+in\s+\d{4}|$)',
        r'^(what\s+is\s+.+?)(?:\s*[|:]|$)',
        r'^(.+?)(?:\s*[|:]|\s+in\s+\d{4}|$)',
    ]
    
    for pat in patterns:
        m = re.search(pat, title_lower)
        if m:
            kw = m.group(1).strip()
            # Take first 3-4 words as the primary keyword phrase
            words = kw.split()
            if len(words) > 5:
                kw = ' '.join(words[:5])
            return kw
    
    # Fallback: first noun phrase (first 3 meaningful words)
    words = [w for w in title_lower.split() if len(w) > 2][:4]
    return ' '.join(words) if words else title_lower.split()[0]

def check_tfidf(title, content):
    """Check TF-IDF keyword coverage."""
    keyword = extract_primary_keyword(title)
    count = count_occurrences(content, keyword)
    status = "✅" if count >= 5 else "❌"
    return keyword, count, status

def check_entities(content, title_lower):
    """Check semantic entity coverage."""
    # Define entities that should be present based on content type
    all_entities = {
        'location_dhaka': {'terms': ['dhaka', 'dhaka\'s'], 'label': 'Dhaka (location)'},
        'location_bangladesh': {'terms': ['bangladesh', 'bangladeshi'], 'label': 'Bangladesh (location)'},
        'entity_seo_expert': {'terms': ['seo expert', 'seo specialist', 'seo consultant'], 'label': 'SEO Expert/Specialist'},
        'entity_google_business': {'terms': ['google business profile', 'gbp'], 'label': 'Google Business Profile'},
        'entity_local_seo': {'terms': ['local seo'], 'label': 'Local SEO'},
        'entity_technical_seo': {'terms': ['technical seo'], 'label': 'Technical SEO'},
        'entity_content_strategy': {'terms': ['content strategy', 'content marketing'], 'label': 'Content Strategy'},
    }
    
    # Additionally check for service-type entities
    if 'seo' in title_lower:
        all_entities['service_seo_services'] = {'terms': ['seo services', 'seo service'], 'label': 'SEO Services'}
    
    missing = []
    present = []
    
    for key, entity in all_entities.items():
        found = False
        for term in entity['terms']:
            if count_occurrences(content, term) > 0:
                found = True
                break
        if found:
            present.append(entity['label'])
        else:
            missing.append(entity['label'])
    
    # Determine if this is a service/location-specific page
    # All pages should have at minimum: Dhaka, Bangladesh, and SEO-related entities
    required = ['location_dhaka', 'location_bangladesh']
    if 'seo' in title_lower:
        required.extend(['entity_seo_expert', 'entity_local_seo', 'entity_technical_seo'])
    
    critical_missing = [all_entities[k]['label'] for k in required if k in all_entities and all_entities[k]['label'] in missing]
    
    status = "✅" if not critical_missing else "❌"
    return status, missing, present

def check_pillar_link(content, tags):
    """Check pillar-cluster alignment."""
    # Define pillar pages
    pillar_map = {
        'seo': {'slug': '/blog/complete-seo-guide-bangladesh-businesses-2026', 'label': 'SEO Guide Pillar'},
        'mobile': {'slug': '/blog/mobile-seo-optimization-bangladesh-mobile-first-era', 'label': 'Mobile SEO Pillar'},
        'local': {'slug': '/services/local-seo', 'label': 'Local SEO Service'},
        'technical': {'slug': '/services/technical-seo', 'label': 'Technical SEO Service'},
    }
    
    # Determine which pillar based on tags
    tag_text = ' '.join(tags).lower()
    linked_pillars = []
    
    # Check if any pillar links are in content
    for key, pillar in pillar_map.items():
        if count_occurrences(content, pillar['slug']) > 0:
            linked_pillars.append(pillar['label'])
    
    # Check for pillar based on tags
    if 'mobile' in tag_text or 'mobile-first' in tag_text:
        target_pillar = pillar_map['mobile']
    elif 'technical' in tag_text:
        target_pillar = pillar_map['technical']
    elif 'local' in tag_text or 'google business' in tag_text:
        target_pillar = pillar_map['local']
    elif 'seo' in tag_text:
        target_pillar = pillar_map['seo']
    else:
        target_pillar = None
    
    if not linked_pillars:
        status = "❌"
        details = "No pillar links found"
    elif target_pillar and target_pillar['label'] in linked_pillars:
        status = "✅"
        details = f"Links to pillar: {target_pillar['label']}"
    else:
        status = "⚠️"
        details = f"Links to: {', '.join(linked_pillars)} (expected: {target_pillar['label'] if target_pillar else 'N/A'})"
    
    return status, details, linked_pillars, target_pillar

def check_aeo_geo(content):
    """Check AEO/GEO optimization - question-based headings."""
    # Count headings starting with question words
    question_pattern = re.compile(
        r'^##\s+(What|How|Why|When|Where|Can|Do|Is|Are|Which|Who|Should|Does)\b',
        re.IGNORECASE | re.MULTILINE
    )
    question_headings = question_pattern.findall(content)
    count = len(question_headings)
    status = "✅" if count >= 2 else "❌"
    return status, count, question_headings

def check_internal_links(content):
    """Count internal links to other posts, services, locations."""
    # Internal links start with / and are not external URLs
    # Exclude the current page, anchors, and external URLs
    internal_link_pattern = re.compile(r'\(\s*(/[^\s)]+)\s*\)')
    all_internal = internal_link_pattern.findall(content)
    
    # Filter out image references, anchors, etc.
    valid_internal = [link for link in all_internal 
                      if not link.startswith('/_') 
                      and not link == '#'
                      and len(link) > 1]
    
    count = len(valid_internal)
    status = "✅" if count >= 3 else "❌"
    return status, count, valid_internal

def check_schema(post):
    """Check if post has fields needed for ArticleSchema."""
    missing_fields = []
    # Required for Article schema
    if not post.get('title'):
        missing_fields.append('title')
    if not post.get('excerpt'):
        missing_fields.append('excerpt')
    if not post.get('date'):
        missing_fields.append('date')
    if not post.get('author'):
        missing_fields.append('author')
    if not post.get('metaTitle'):
        missing_fields.append('metaTitle')
    if not post.get('metaDescription'):
        missing_fields.append('metaDescription')
    
    status = "✅" if len(missing_fields) == 0 else "❌"
    return status, missing_fields

def check_content_length(content):
    """Check content length adequacy."""
    word_count = len(content.split())
    status = "✅" if word_count >= 1500 else "❌"
    return status, word_count

def generate_fix_instructions(post, checks):
    """Generate specific fix instructions based on check results."""
    fixes = []
    slug = post['slug']
    
    # TF-IDF fixes
    if checks['tfidf_status'] == "❌":
        fixes.append(f"- **TF-IDF**: Increase occurrence of primary keyword \"{checks['tfidf_keyword']}\" to at least 5 times across the content (currently {checks['tfidf_count']}).")
    
    # Entity fixes
    if checks['entity_status'] == "❌" and checks['entity_missing']:
        fixes.append(f"- **Entities**: Add the following missing entities: {', '.join(checks['entity_missing'])}.")
    
    # Pillar link fixes
    if checks['pillar_status'] == "❌":
        if checks['pillar_target']:
            fixes.append(f"- **Pillar Link**: Add a link to the pillar page {checks['pillar_target']['slug']} (\"{checks['pillar_target']['label']}\").")
        else:
            fixes.append(f"- **Pillar Link**: Add links to relevant pillar/service pages (e.g., /services/local-seo, /services/technical-seo).")
    
    # AEO/GEO fixes
    if checks['aeo_status'] == "❌":
        fixes.append(f"- **AEO/GEO**: Add more question-based headings (H2s starting with What, How, Why, etc.). Currently has {checks['aeo_count']}, need at least 2.")
    
    # Internal link fixes
    if checks['links_status'] == "❌":
        fixes.append(f"- **Internal Links**: Add more internal links to reach at least 3 (currently has {checks['links_count']}). Link to related posts, services, or location pages.")
    
    # Schema fixes
    if checks['schema_status'] == "❌" and checks['schema_missing']:
        for field in checks['schema_missing']:
            if field in ['metaTitle', 'metaDescription']:
                fixes.append(f"- **Schema**: Add `{field}` field to the post entry for Article schema completeness.")
    
    return fixes


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
    entity_status, entity_missing, entity_present = check_entities(content, title.lower())
    print(f"\nB. Entity Coverage:")
    print(f"   Status: {entity_status}")
    if entity_present:
        print(f"   Present: {', '.join(entity_present)}")
    if entity_missing:
        print(f"   Missing: {', '.join(entity_missing)}")
    
    # C. Pillar-Cluster
    pillar_status, pillar_details, linked_pillars, pillar_target = check_pillar_link(content, tags)
    print(f"\nC. Pillar-Cluster Alignment:")
    print(f"   Status: {pillar_status} | {pillar_details}")
    if linked_pillars:
        print(f"   Pillar links found: {', '.join(linked_pillars)}")
    if pillar_target:
        print(f"   Target pillar: {pillar_target['label']} ({pillar_target['slug']})")
    
    # D. AEO/GEO
    aeo_status, aeo_count, aeo_headings = check_aeo_geo(content)
    print(f"\nD. AEO/GEO Optimization:")
    print(f"   Status: {aeo_status} | Question headings: {aeo_count}")
    if aeo_headings:
        print(f"   Found: {', '.join(h.title() for h in aeo_headings)}")
    
    # E. Internal Links
    links_status, links_count, link_targets = check_internal_links(content)
    print(f"\nE. Internal Linking:")
    print(f"   Status: {links_status} | Count: {links_count}")
    if link_targets:
        print(f"   Links to: {', '.join(link_targets[:10])}")
        if len(link_targets) > 10:
            print(f"   ... and {len(link_targets)-10} more")
    
    # F. Schema
    schema_status, schema_missing = check_schema(post)
    print(f"\nF. Schema Ready:")
    print(f"   Status: {schema_status}")
    if schema_missing:
        print(f"   Missing fields: {', '.join(schema_missing)}")
    
    # Content length bonus check
    len_status, word_count = check_content_length(content)
    print(f"\n   Content Length: {word_count} words ({len_status})")
    
    # Compile check results
    checks = {
        'tfidf_keyword': keyword,
        'tfidf_count': count,
        'tfidf_status': tfidf_status,
        'entity_status': entity_status,
        'entity_missing': entity_missing,
        'entity_present': entity_present,
        'pillar_status': pillar_status,
        'pillar_details': pillar_details,
        'pillar_linked': linked_pillars,
        'pillar_target': pillar_target,
        'aeo_status': aeo_status,
        'aeo_count': aeo_count,
        'aeo_headings': aeo_headings,
        'links_status': links_status,
        'links_count': links_count,
        'link_targets': link_targets,
        'schema_status': schema_status,
        'schema_missing': schema_missing,
        'word_count': word_count,
    }
    
    fixes = generate_fix_instructions(post, checks)
    
    results.append({
        'slug': slug,
        'title': title,
        'checks': checks,
        'fixes': fixes,
    })

# === GENERATE FINAL REPORT ===
print("\n\n" + "="*60)
print("FINAL FRAMEWORK ENFORCEMENT REPORT")
print("="*60)

for r in results:
    c = r['checks']
    print(f"\n## Post: {r['slug']}")
    print(f"**Title:** {r['title']}")
    print("")
    print("| Check | Status | Details |")
    print("|-------|--------|---------|")
    print(f"| TF-IDF: \"{c['tfidf_keyword']}\" | {c['tfidf_status']} | {c['tfidf_count']} occurrences |")
    
    entity_detail = "All key entities present" if not c['entity_missing'] else f"Missing: {', '.join(c['entity_missing'][:3])}"
    print(f"| Entities | {c['entity_status']} | {entity_detail} |")
    
    print(f"| Pillar Link | {c['pillar_status']} | {c['pillar_details']} |")
    print(f"| AEO/GEO | {c['aeo_status']} | {c['aeo_count']} question headings |")
    print(f"| Internal Links | {c['links_status']} | {c['links_count']} total |")
    print(f"| Schema Ready | {c['schema_status']} | Missing: {', '.join(c['schema_missing']) if c['schema_missing'] else 'All fields set'} |")
    print(f"| Content Length | {'✅' if c['word_count'] >= 1500 else '❌'} | {c['word_count']} words |")
    
    if c['fixes']:
        print("\n### Fix instructions:")
        for fix in c['fixes']:
            print(fix)
    else:
        print("\n### Fix instructions:")
        print("✅ All checks pass — no fixes needed.")
    print("")

# Summary
print("---")
print("### Summary")
print(f"Posts analyzed: {len(results)}")
all_pass = all(r['checks']['tfidf_status'] == '✅' and 
                r['checks']['entity_status'] == '✅' and
                '❌' not in r['checks']['pillar_status'] and
                r['checks']['aeo_status'] == '✅' and
                r['checks']['links_status'] == '✅' and
                r['checks']['schema_status'] == '✅'
                for r in results)
if all_pass:
    print("✅ All framework checks pass across all modified posts.")
else:
    total_issues = sum(len(r['fixes']) for r in results)
    print(f"⚠️  {total_issues} issue(s) requiring attention across {len(results)} post(s). See above for details.")
