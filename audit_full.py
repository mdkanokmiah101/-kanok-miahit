#!/usr/bin/env python3
"""Full content framework audit on all 22 blog posts."""

import re
import json

# Load parsed posts
with open('/root/kanok-miahit/parsed_posts.json', 'r') as f:
    posts = json.load(f)

def get_primary_keyword(title):
    """Extract primary keyword from title intelligently."""
    # Clean the title
    t = title.replace(':', ' ').replace(',', ' ').replace('"', '')
    words = t.split()
    
    # Stopwords to skip at the beginning
    leading_stopwords = {'why', 'how', 'what', 'when', 'where', 'which', 'who', 'the', 'a', 'an', 'in', 'for', 'of', 'to', 'from', 'is', 'are', 'do', 'does', 'can', 'will', 'has', 'have', 'top', 'best', 'complete', 'ultimate', 'essential', 'guide', 'tips'}
    
    # Find first meaningful noun phrase
    # Strategy: start from beginning, skip leading stopwords, take up to 4 words
    meaningful = []
    started = False
    for w in words:
        wl = w.lower()
        if not started and wl in leading_stopwords:
            continue
        started = True
        if len(meaningful) < 4:
            meaningful.append(w)
        else:
            break
    
    if not meaningful:
        return words[0].lower() if words else ''
    
    kw = ' '.join(meaningful)
    # Remove trailing punctuation
    kw = kw.rstrip(':,.!?;')
    return kw

def analyze_post(post):
    slug = post['slug']
    title = post.get('title', '')
    content = post.get('content', '')
    tags = post.get('tags', [])
    excerpt = post.get('excerpt', '')
    date = post.get('date', '')
    
    content_lower = content.lower()
    
    results = {
        'slug': slug,
        'title': title,
    }
    
    # =========================================
    # A. TF-IDF Coverage
    # =========================================
    primary_kw = get_primary_keyword(title)
    if not primary_kw:
        primary_kw = title.split()[0].lower().rstrip(':,').rstrip('.')
    
    kw_lower = primary_kw.lower()
    count = content_lower.count(kw_lower)
    
    # Also try without the last word if it's common
    # For very short keywords, check if they exist
    results['tfidf_keyword'] = primary_kw
    results['tfidf_count'] = count
    results['tfidf_status'] = '✅' if count >= 5 else '❌'
    
    # =========================================
    # B. Semantic Entity Coverage
    # =========================================
    # Core entities every Dhaka-focused post should have
    core_entities = ['Dhaka', 'Bangladesh', 'Kanok Miah']
    
    # Service/industry-specific entity from tags
    tag_entities = []
    for tag in tags:
        tag_lower = tag.lower()
        # Skip generic tags
        if tag_lower in ['case study', 'seo', 'local seo', 'seo case study', 'seo strategy', 'growth strategy', 
                         'organic traffic', 'seo expert dhaka', 'seo services bangladesh', 'seo results bangladesh',
                         'digital marketing bangladesh', 'dhaka seo', 'seo expert bangladesh', 'seo results',
                         'seo mistakes', 'seo agency dhaka', 'seo services', 'dhaka seo expert', 'best seo expert',
                         'seo tips bangladesh', 'hire seo expert', 'hire seo', 'technical seo', 'content marketing',
                         'smm panel', 'b2b seo', 'property safety', 'transportation', 'automotive', 'construction']:
            continue
        tag_entities.append(tag)
    
    # Take up to 2 specific tag entities
    specific_entities = tag_entities[:2]
    
    all_entities = core_entities + specific_entities + ['SEO']
    
    # Special case: for UK-specific case studies, don't require Bangladesh/Dhaka
    is_uk_post = any(uk_term in slug.lower() for uk_term in ['dundee', 'scotland', 'uk', 'landlord'])
    is_smm_panel = any(sm in slug.lower() for sm in ['smmgen', 'smmsun', 'morethanpanel', 'panel'])
    
    if is_uk_post:
        # UK posts don't need Bangladesh/Dhaka
        all_entities = [e for e in all_entities if e not in ['Dhaka', 'Bangladesh']]
        if 'Kanok Miah' not in all_entities:
            all_entities.append('Kanok Miah')
    elif is_smm_panel:
        # SMM panel posts might not need Dhaka/Bangladesh unless they mention it
        pass
    
    missing_entities = []
    for entity in all_entities:
        if entity.lower() not in content_lower:
            missing_entities.append(entity)
    
    results['all_entities'] = all_entities
    results['missing_entities'] = missing_entities
    results['entities_status'] = '✅' if not missing_entities else '❌'
    
    # =========================================
    # C. Pillar-Cluster Alignment
    # =========================================
    # Check for pillar page links
    has_pillar_main = '/blog/complete-seo-guide-bangladesh-businesses-2026' in content
    
    # Check for services/industries links
    service_links = re.findall(r'/services/[a-z0-9-]*', content)
    industry_links = re.findall(r'/industries/[a-z0-9-]*', content)
    location_links = re.findall(r'/locations/[a-z0-9-]*', content)
    
    has_services = bool(service_links)
    has_industries = bool(industry_links)
    has_locations = bool(location_links)
    
    has_pillar_link = has_pillar_main or has_services or has_industries or has_locations
    
    results['pillar_link_status'] = '✅' if has_pillar_link else '❌'
    results['has_pillar_main'] = has_pillar_main
    results['has_services'] = has_services
    results['has_industries'] = has_industries
    results['has_locations'] = has_locations
    results['service_links'] = list(set(service_links))
    results['industry_links'] = list(set(industry_links))
    
    # =========================================
    # D. AEO/GEO Optimization
    # =========================================
    # Count question-based headings (## or ### starting with question words)
    question_pattern = re.compile(r'^#{2,3}\s+(How|What|Why|When|Where|Can|Do|Is|Are|Does|Which|Who)\b', re.MULTILINE)
    question_headings = question_pattern.findall(content)
    
    results['question_headings_list'] = question_headings
    results['question_count'] = len(question_headings)
    results['aeo_status'] = '✅' if len(question_headings) >= 2 else '❌'
    
    # =========================================
    # E. Internal Linking
    # =========================================
    # Find all internal links
    all_internal_links = re.findall(r'/(?:blog|services|locations|industries)/[a-z0-9-]+', content)
    # Remove self-references
    all_internal_links = [l for l in all_internal_links if l != f'/blog/{slug}']
    # Get unique
    unique_internal = list(set(all_internal_links))
    
    results['internal_links_list'] = unique_internal
    results['internal_link_count'] = len(unique_internal)
    results['internal_link_status'] = '✅' if len(unique_internal) >= 3 else '❌'
    
    # =========================================
    # F. Schema Readiness
    # =========================================
    has_date = bool(date)
    has_excerpt = bool(excerpt)
    has_title = bool(title)
    
    missing_schema = []
    if not has_title:
        missing_schema.append('title')
    if not has_excerpt:
        missing_schema.append('excerpt')
    if not has_date:
        missing_schema.append('date')
    
    results['schema_missing'] = missing_schema
    results['schema_status'] = '✅' if not missing_schema else '❌'
    
    return results


# Run the analysis
all_results = []
for post in posts:
    slug = post['slug']
    title = post.get('title', '')
    
    print(f"\n{'#'*80}")
    print(f"# Post: {slug}")
    print(f"# Title: {title}")
    print(f"{'#'*80}")
    
    results = analyze_post(post)
    all_results.append(results)
    
    # A. TF-IDF
    kw = results['tfidf_keyword']
    cnt = results['tfidf_count']
    status_a = results['tfidf_status']
    print(f"\n| Check | Status | Details |")
    print(f"|-------|--------|---------|")
    print(f"| TF-IDF: \"{kw}\" | {status_a} | {cnt} occurrences |")
    
    # B. Entities
    status_b = results['entities_status']
    missing = results['missing_entities']
    print(f"| Entities | {status_b} | Missing: {', '.join(missing) if missing else 'None'} |")
    
    # C. Pillar
    status_c = results['pillar_link_status']
    pillar_detail = []
    if results['has_pillar_main']:
        pillar_detail.append('/blog/complete-seo-guide...')
    if results['has_services']:
        pillar_detail.append(f"Services: {results['service_links'][:2]}")
    if results['has_industries']:
        pillar_detail.append(f"Industries: {results['industry_links'][:2]}")
    if results['has_locations']:
        pillar_detail.append('Has /locations/ links')
    pillar_str = '; '.join(pillar_detail) if pillar_detail else 'No pillar/services/industries links found'
    print(f"| Pillar Link | {status_c} | {pillar_str} |")
    
    # D. AEO/GEO
    status_d = results['aeo_status']
    qcount = results['question_count']
    qheads = results['question_headings_list']
    print(f"| AEO/GEO | {status_d} | {qcount} question headings: {qheads} |")
    
    # E. Internal Links
    status_e = results['internal_link_status']
    icount = results['internal_link_count']
    ilinks = results['internal_links_list']
    print(f"| Internal Links | {status_e} | {icount} total: {ilinks} |")
    
    # F. Schema
    status_f = results['schema_status']
    smissing = results['schema_missing']
    print(f"| Schema Ready | {status_f} | {'Missing: ' + ', '.join(smissing) if smissing else 'All fields set (title, excerpt, date)'} |")
    
    # Fix instructions
    fixes = []
    if cnt < 5:
        fixes.append(f"- Increase \"{kw}\" occurrences to at least 5 (currently {cnt})")
    if missing:
        fixes.append(f"- Add entities: {', '.join(missing)}")
    if results['pillar_link_status'] == '❌':
        fixes.append("- Add link to pillar page (/blog/complete-seo-guide...) or relevant /services/, /industries/ page")
    if results['aeo_status'] == '❌':
        fixes.append(f"- Add more question-based headings (## or ### starting with How/What/Why/etc) — currently {qcount}, need ≥2")
    if results['internal_link_status'] == '❌':
        fixes.append(f"- Add more internal links to /blog/*, /services/*, /locations/*, or /industries/* — currently {icount}, need ≥3")
    if results['schema_status'] == '❌':
        fixes.append(f"- Set missing schema fields: {', '.join(smissing)}")
    
    print(f"\n### Fix instructions:")
    if fixes:
        for f in fixes:
            print(f)
    else:
        print("None needed")
    print()

# =============================================
# SUMMARY SECTION
# =============================================
print(f"\n{'='*80}")
print("OVERALL SUMMARY")
print(f"{'='*80}")

pass_tfidf = sum(1 for r in all_results if r['tfidf_status'] == '✅')
pass_entities = sum(1 for r in all_results if r['entities_status'] == '✅')
pass_pillar = sum(1 for r in all_results if r['pillar_link_status'] == '✅')
pass_aeo = sum(1 for r in all_results if r['aeo_status'] == '✅')
pass_internal = sum(1 for r in all_results if r['internal_link_status'] == '✅')
pass_schema = sum(1 for r in all_results if r['schema_status'] == '✅')

pass_all = sum(1 for r in all_results if all([
    r['tfidf_status'] == '✅',
    r['entities_status'] == '✅',
    r['pillar_link_status'] == '✅',
    r['aeo_status'] == '✅',
    r['internal_link_status'] == '✅',
    r['schema_status'] == '✅'
]))

print(f"\n| Check | Passing | Rate |")
print(f"|-------|---------|------|")
print(f"| TF-IDF Coverage | {pass_tfidf}/22 | {pass_tfidf/22*100:.0f}% |")
print(f"| Entity Coverage | {pass_entities}/22 | {pass_entities/22*100:.0f}% |")
print(f"| Pillar Links | {pass_pillar}/22 | {pass_pillar/22*100:.0f}% |")
print(f"| AEO/GEO | {pass_aeo}/22 | {pass_aeo/22*100:.0f}% |")
print(f"| Internal Links | {pass_internal}/22 | {pass_internal/22*100:.0f}% |")
print(f"| Schema Ready | {pass_schema}/22 | {pass_schema/22*100:.0f}% |")
print(f"| **All Checks** | **{pass_all}/22** | **{pass_all/22*100:.0f}%** |")

# Per-post summary table
print(f"\n{'='*80}")
print("PER-POST SUMMARY TABLE")
print(f"{'='*80}")
print(f"{'Slug':<60} {'TF-IDF':<8} {'Ent':<5} {'Pillar':<8} {'AEO':<5} {'IntLnks':<9} {'Schema':<8} {'All':<5}")
print(f"{'-'*60} {'-'*8} {'-'*5} {'-'*8} {'-'*5} {'-'*9} {'-'*8} {'-'*5}")
for r in all_results:
    slug = r['slug'][:58]
    a = r['tfidf_status']
    b = r['entities_status']
    c = r['pillar_link_status']
    d = r['aeo_status']
    e = r['internal_link_status']
    f = r['schema_status']
    all_pass = '✅' if all([a=='✅',b=='✅',c=='✅',d=='✅',e=='✅',f=='✅']) else '❌'
    print(f"{slug:<60} {a:<8} {b:<5} {c:<8} {d:<5} {e:<9} {f:<8} {all_pass:<5}")

# Save full results
with open('/root/kanok-miahit/audit_full_results.json', 'w') as f:
    json.dump(all_results, f, indent=2, default=str)

print(f"\nFull results saved to audit_full_results.json")
