#!/usr/bin/env python3
"""
Content Framework Enforcer for kanokmiah.com.bd
Runs 6 checks on modified blog posts: TF-IDF, Entities, Pillar Link, AEO/GEO, Internal Links, Schema
"""
import re
import json

with open('src/app/blog/data.js', 'r') as f:
    content = f.read()

target_slugs = [
    'seo-canonical-url-guide-bd',
    'mobile-seo-optimization-bangladesh-mobile-first-era',
    'local-seo-dhaka-google-maps-ranking',
    'seo-knowledge-panel-bangladesh',
    'seo-career-guide-bangladesh-2026',
    'affiliate-seo-bangladesh',
    'b2b-lead-generation-seo-bangladesh',
    'seo-for-fitness-gyms-bangladesh',
    'seo-healthcare-medical-clinics-bangladesh',
    'seo-educational-institutions-bangladesh',
    'seo-travel-tourism-bangladesh',
    'seo-google-penalty-recovery-bd',
    'technical-seo-core-web-vitals-optimization',
    'ecommerce-seo-daraz-shopify-guide',
    'link-building-bangladesh-strategies',
    'keyword-research-bangladesh-market',
    'content-marketing-seo-friendly-content-writing',
]

results = {}

for slug in target_slugs:
    idx = content.find(f'slug: "{slug}"')
    if idx < 0:
        results[slug] = {"error": "Post not found"}
        continue
    
    start = content.rfind('{', 0, idx)
    next_idx = content.find('slug:', idx + 10)
    if next_idx < 0:
        next_idx = content.rfind(']')
    post_block = content[start:next_idx]
    
    # Extract metadata
    title_match = re.search(r'title:\s*"([^"]*)"', post_block)
    title = title_match.group(1) if title_match else ''
    
    date_match = re.search(r'date:\s*"([^"]*)"', post_block)
    date = date_match.group(1) if date_match else ''
    
    date_modified_match = re.search(r'dateModified:\s*"([^"]*)"', post_block)
    date_modified = date_modified_match.group(1) if date_modified_match else ''
    
    excerpt_match = re.search(r'excerpt:\s*\n\s*"([^"]*)"', post_block)
    excerpt = excerpt_match.group(1) if excerpt_match else ''
    
    tags_match = re.search(r'tags:\s*\[([^\]]*)\]', post_block)
    tags_str = tags_match.group(1) if tags_match else ''
    tags = [t.strip().strip('"') for t in tags_str.split(',')] if tags_str else []
    
    # Extract content
    content_start = post_block.find('content: `')
    content_end = post_block.rfind('`,')
    content_text = ''
    if content_start >= 0 and content_end > content_start:
        content_text = post_block[content_start+10:content_end]
    
    lang = 'bn' if any('\u0980' <= c <= '\u09FF' for c in title[:5]) else 'en'
    
    checks = {}
    
    # --- A. TF-IDF Coverage ---
    if lang == 'bn':
        # Bengali: extract the first meaningful noun phrase from title
        # Remove "কীভাবে", "কেন", "কখন" etc prefixes, take the main topic
        bn_stop_prefixes = ['কীভাবে', 'কেন', 'কখন', 'কোথায়', 'কি']
        kw = title
        for pref in bn_stop_prefixes:
            if kw.startswith(pref):
                kw = kw[len(pref):].strip()
        # Take the first segment before : or — or ?
        kw = re.split(r'[:\-—?।]', kw)[0].strip()
        # If still too long, take first meaningful chunk
        if len(kw) > 20:
            parts = re.split(r'[,;]', kw)
            kw = parts[0].strip()
        keyword = kw
    else:
        # English: extract primary keyword from title
        # Remove question words, take first meaningful noun phrase
        kw = title
        kw = re.sub(r'^(How|What|Why|When|Where|Can|Do|Is|Are|Does|Which)\s+', '', kw)
        kw = re.split(r'[:\-—?]', kw)[0].strip()
        # Take first meaningful segment
        if len(kw.split()) > 8:
            kw = ' '.join(kw.split()[:6])
        keyword = kw

    # Count occurrences of keyword in content (case-insensitive)
    kw_count = content_text.lower().count(keyword.lower())
    keyword_ok = kw_count >= 5
    checks['tfidf'] = {
        'keyword': keyword,
        'count': kw_count,
        'passed': keyword_ok,
        'detail': f'"{keyword}" appears {kw_count} times'
    }
    
    # --- B. Semantic Entity Coverage ---
    entities = {
        'location': ['ঢাকা', 'Dhaka', 'বাংলাদেশ', 'Bangladesh'],
        'person': ['Kanok Miah', 'কনক মিঞা', 'Kanok'],
        'service': ['SEO']
    }
    
    missing_entities = []
    found_location = False
    found_person = False
    found_service_entity = False
    
    # Check location entities
    for loc in ['ঢাকা', 'Dhaka', 'বাংলাদেশ', 'Bangladesh', 'Chittagong', 'Sylhet', 'Khulna']:
        if loc.lower() in content_text.lower():
            found_location = True
            break
    if not found_location:
        missing_entities.append('location (Dhaka/Bangladesh)')
    
    # Check person entity
    for person in ['Kanok Miah', 'কনক মিঞা', 'Kanok']:
        if person.lower() in content_text.lower():
            found_person = True
            break
    if not found_person:
        missing_entities.append('author (Kanok Miah)')
    
    # If it's an English post, check for service type specific entities
    if lang == 'en':
        service_terms = ['SEO', 'search engine optimization', 'search engine']
        found_svc = any(t.lower() in content_text.lower() for t in service_terms)
        if not found_svc and 'SEO' not in title:
            missing_entities.append('service (SEO/optimization)')
    
    # Check industry-specific entities
    industry_terms = []
    if 'ecommerce' in slug or 'ecommerce' in slug or 'daraz' in slug or 'shopify' in slug:
        industry_terms = ['e-commerce', 'ecommerce', 'online store', 'দারাজ', 'Daraz', 'Shopify']
    elif 'fitness' in slug or 'gym' in slug:
        industry_terms = ['fitness', 'gym', 'ফিটনেস']
    elif 'healthcare' in slug or 'medical' in slug or 'clinic' in slug:
        industry_terms = ['healthcare', 'medical', 'clinic', 'patient', 'হেলথ']
    elif 'education' in slug or 'institution' in slug:
        industry_terms = ['education', 'student', 'school', 'college', 'university']
    elif 'travel' in slug or 'tourism' in slug:
        industry_terms = ['travel', 'tourism', 'tour', 'hotel']
    elif 'b2b' in slug or 'lead' in slug:
        industry_terms = ['B2B', 'lead', 'manufactur']
    elif 'canonical' in slug or 'technical' in slug:
        industry_terms = ['canonical', 'টেকনিক্যাল', 'টেকনিকেল', 'technical']
    elif 'mobile' in slug:
        industry_terms = ['mobile', 'মোবাইল']
    elif 'knowledge' in slug or 'knowledge panel' in slug:
        industry_terms = ['knowledge', 'নলেজ', 'knowledge panel']
    elif 'career' in slug:
        industry_terms = ['ক্যারিয়ার', 'career', 'পেশা']
    elif 'affiliate' in slug:
        industry_terms = ['affiliate', 'অ্যাফিলিয়েট']
    elif 'keyword' in slug:
        industry_terms = ['keyword', 'কীওয়ার্ড']
    elif 'content' in slug and 'writing' in slug:
        industry_terms = ['content', 'কন্টেন্ট']
    
    for term in industry_terms:
        if term.lower() in content_text.lower():
            break
    else:
        if industry_terms:
            missing_entities.append(f'industry term ({industry_terms[0]})')
    
    # Check link to /locations/ or /industries/ 
    has_location_link = '/locations/' in content_text
    has_industry_link = '/industries/' in content_text
    
    checks['entities'] = {
        'missing': missing_entities,
        'passed': len(missing_entities) == 0,
        'detail': ', '.join(missing_entities) if missing_entities else 'All key entities present',
        'has_location_link': has_location_link,
        'has_industry_link': has_industry_link
    }
    
    # --- C. Pillar-Cluster Alignment ---
    pillar_info = {'pillar_topic': '', 'has_pillar_link': False, 'pillar_link': ''}
    
    # Determine pillar based on tags
    tag_lower = [t.lower() for t in tags]
    pillar_map = {
        'seo-guide': ['seo guide', 'bangladesh seo', '2026'],
        'local-seo': ['local seo', 'google maps', 'gbp'],
        'ecommerce-seo': ['e-commerce seo', 'daraz', 'shopify', 'ecommerce'],
        'technical-seo': ['technical seo', 'core web vitals'],
        'link-building': ['link building', 'backlinks'],
        'geo-ai': ['geo', 'ai search', 'generative engine'],
        'content-marketing': ['content marketing', 'content writing'],
        'seo-career': ['ক্যারিয়ার', 'চাকরি', 'পেশা'],
    }
    
    assigned_pillar = ''
    for pillar, keywords in pillar_map.items():
        for kw in keywords:
            if any(kw in t for t in tag_lower):
                assigned_pillar = pillar
                break
        if assigned_pillar:
            break
    
    if not assigned_pillar:
        # Try based on slug
        for pillar, keywords in pillar_map.items():
            for kw in keywords:
                if kw.replace('-', '') in slug.lower().replace('-', ''):
                    assigned_pillar = pillar
                    break
            if assigned_pillar:
                break
    
    # Define pillar page URLs
    pillar_pages = {
        'seo-guide': '/blog/complete-seo-guide-bangladesh-businesses-2026',
        'local-seo': '/blog/local-seo-tips-dhaka-businesses-google-maps',
        'ecommerce-seo': '/blog/why-ecommerce-store-needs-seo-bangladesh',
        'technical-seo': '/blog/technical-seo-checklist-bangladeshi-websites',
        'link-building': '/blog/link-building-strategies-bangladesh-market',
        'geo-ai': '/blog/geo-optimization-prepare-business-ai-search',
        'content-marketing': '/blog/content-marketing-strategy-bangladeshi-brands-seo',
        'seo-career': '/blog/seo-career-guide-bangladesh-2026',
    }
    
    if assigned_pillar and assigned_pillar in pillar_pages:
        pillar_url = pillar_pages[assigned_pillar]
        has_link = pillar_url in content_text
        checks['pillar'] = {
            'pillar_topic': assigned_pillar,
            'pillar_url': pillar_url,
            'has_pillar_link': has_link,
            'passed': has_link,
            'detail': f'Links to pillar: {"Yes" if has_link else "No — add link to " + pillar_url}'
        }
    else:
        checks['pillar'] = {
            'pillar_topic': assigned_pillar or 'unclassified',
            'pillar_url': '',
            'has_pillar_link': False,
            'passed': False,
            'detail': f'Could not determine pillar topic (tags: {tags})'
        }
    
    # --- D. AEO/GEO Optimization ---
    # Count question-based headings
    question_heading_patterns = [
        r'^#{2,3}\s+(কীভাবে|কেন|কখন|কোথায়|কি|কী|How|What|Why|When|Where|Can|Do|Is|Are|Does|Which)',
    ]
    
    question_headings = []
    for line in content_text.split('\n'):
        stripped = line.strip()
        if stripped.startswith('##') or stripped.startswith('###'):
            # Check if it starts with a question word
            q_words_en = ['How ', 'What ', 'Why ', 'When ', 'Where ', 'Can ', 'Do ', 'Is ', 'Are ', 'Does ', 'Which ', 'Who ']
            q_words_bn = ['কীভাবে ', 'কেন ', 'কখন ', 'কোথায় ', 'কি ', 'কী ', 'কিভাবে ']
            heading_text = stripped.lstrip('#').strip()
            for qw in q_words_en + q_words_bn:
                if heading_text.startswith(qw):
                    question_headings.append(heading_text)
                    break
            else:
                # Also check if heading ends with ?
                if '?' in heading_text:
                    question_headings.append(heading_text)
    
    if not question_headings:
        # Also check FAQ section for question-based H3
        for line in content_text.split('\n'):
            stripped = line.strip()
            if stripped.startswith('###') and '?' in stripped:
                question_headings.append(stripped.lstrip('#').strip())
    
    aeo_passed = len(question_headings) >= 2
    checks['aeo'] = {
        'question_headings': question_headings,
        'count': len(question_headings),
        'passed': aeo_passed,
        'detail': f'{len(question_headings)} question headings found'
    }
    
    # --- E. Internal Linking ---
    # Count internal links (/blog/, /services/, /locations/, /industries/, /about/)
    internal_links = re.findall(r'\(/(?:blog/|services/|locations/|industries/|about/?|contact/?)[^)]*\)', content_text)
    internal_links_count = len(internal_links)
    
    # Also count markdown links to the homepage
    home_links = re.findall(r'\(/\)', content_text)
    internal_links_count += len(home_links)
    
    links_passed = internal_links_count >= 3
    checks['internal_links'] = {
        'count': internal_links_count,
        'links': internal_links[:10],  # show first 10
        'passed': links_passed,
        'detail': f'{internal_links_count} internal links found'
    }
    
    # --- F. Schema ---
    # Check if post has title, excerpt, date set
    schema_fields = {
        'title': bool(title),
        'excerpt': bool(excerpt),
        'date': bool(date),
    }
    missing_fields = [k for k, v in schema_fields.items() if not v]
    
    # Check for dateModified (important for Article schema freshness)
    if date_modified:
        schema_fields['dateModified'] = True
    else:
        missing_fields.append('dateModified')
    
    schema_passed = len(missing_fields) == 0
    checks['schema'] = {
        'missing_fields': missing_fields,
        'passed': schema_passed,
        'detail': f'Missing: {", ".join(missing_fields) if missing_fields else "All set"}'
    }
    
    results[slug] = {
        'title': title,
        'checks': checks,
        'lang': lang,
        'tags': tags,
    }

# Generate Report
print("=" * 80)
print("CONTENT FRAMEWORK ENFORCER REPORT")
print("=" * 80)
print(f"Date: 2026-07-24")
print(f"Posts checked: {len(target_slugs)}")
print()

all_passed = True
for slug, result in results.items():
    if 'error' in result:
        print(f"## ERROR: {slug} — {result['error']}")
        continue
    
    checks = result['checks']
    title = result['title']
    
    print(f"## Post: {slug}")
    print(f"**Title:** {title}")
    print()
    print("| Check | Status | Details |")
    print("|-------|--------|---------|")
    
    # A. TF-IDF
    tf = checks['tfidf']
    status = '✅' if tf['passed'] else '❌'
    print(f"| TF-IDF: {tf['keyword'][:40]} | {status} | {tf['detail']} |")
    if not tf['passed']:
        all_passed = False
    
    # B. Entities
    ent = checks['entities']
    status = '✅' if ent['passed'] else '❌'
    print(f"| Entities | {status} | {ent['detail']} |")
    if not ent['passed']:
        all_passed = False
    
    # C. Pillar
    pil = checks['pillar']
    status = '✅' if pil['passed'] else '❌'
    print(f"| Pillar Link | {status} | {pil['detail'][:80]} |")
    if not pil['passed']:
        all_passed = False
    
    # D. AEO/GEO
    aeo = checks['aeo']
    status = '✅' if aeo['passed'] else '❌'
    print(f"| AEO/GEO | {status} | {aeo['detail']} |")
    if not aeo['passed']:
        all_passed = False
    
    # E. Internal Links
    il = checks['internal_links']
    status = '✅' if il['passed'] else '❌'
    print(f"| Internal Links | {status} | {il['detail']} |")
    if not il['passed']:
        all_passed = False
    
    # F. Schema
    sch = checks['schema']
    status = '✅' if sch['passed'] else '❌'
    print(f"| Schema Ready | {status} | {sch['detail']} |")
    if not sch['passed']:
        all_passed = False
    
    print()

print("---")
print(f"**Overall: {'ALL CHECKS PASSED' if all_passed else 'SOME CHECKS NEED ATTENTION'}**")
