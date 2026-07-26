#!/usr/bin/env python3
import re

with open('src/app/blog/data.js', 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')

slugs = [
    ("seo-consultant-dhaka-bangladesh", 8928),
    ("google-my-business-optimization-bangladesh", 9125),
    ("seo-for-new-website-bangladesh", 9431),
    ("website-speed-optimization-bangladesh", 9726),
    ("seo-audit-checklist-bangladesh", 9944),
    ("affiliate-seo-bangladesh", 10222),
    ("voice-search-seo-bangladesh", 10469),
    ("seo-legal-compliance-bangladesh", 10615),
    ("seo-for-restaurants-cafe-dhaka", 10779),
    ("seo-for-cleaning-services-bangladesh", 10932),
    ("seo-dashboard-tools-bangladesh", 11101)
]

def count_keyword(content, keyword):
    if not content:
        return 0
    return len(re.findall(re.escape(keyword), content, re.IGNORECASE))

for target_slug, line_start in slugs:
    slug_line_idx = line_start - 1  # 0-indexed
    
    # Extract metadata
    post_data = {}
    for offset in range(-10, 10):
        idx = slug_line_idx + offset
        if idx < 0 or idx >= len(lines):
            continue
        line = lines[idx]
        if 'title:' in line:
            t = line.split('title:')[1].strip().strip(',').strip('"').strip("'")
            post_data['title'] = t
        if 'excerpt:' in line:
            e = line.split('excerpt:')[1].strip().strip(',').strip('"').strip("'")
            post_data['excerpt'] = e
        if 'date:' in line:
            d = line.split('date:')[1].strip().strip(',').strip('"').strip("'")
            post_data['date'] = d
    
    # Find content backtick block
    content_start = None
    content_end = None
    first_line_content = ""
    for offset in range(-5, 200):
        idx = slug_line_idx + offset
        if idx < 0 or idx >= len(lines):
            continue
        line = lines[idx]
        if 'content: `' in line or 'content:`' in line:
            bt_pos = line.find('`')
            if bt_pos >= 0:
                content_start = idx
                rest = line[bt_pos+1:]
                if rest.strip():
                    first_line_content = rest
                break
    
    if content_start is not None:
        for offset in range(0, 500):
            idx = content_start + offset
            if idx >= len(lines):
                break
            line = lines[idx]
            if idx == content_start:
                continue
            if line.strip().endswith('`,'):
                content_end = idx
                break
    
    content_text = ""
    if content_start is not None and content_end is not None:
        parts = []
        if first_line_content:
            parts.append(first_line_content)
        for i in range(content_start + 1, content_end):
            parts.append(lines[i])
        content_text = '\n'.join(parts)
    
    title = post_data.get('title', '')
    
    print(f"## Post: {target_slug}")
    print(f"**Title:** {title}")
    print(f"**Date:** {post_data.get('date', 'N/A')}")
    print()
    print("| Check | Status | Details |")
    print("|-------|--------|---------|")
    
    # A. TF-IDF Coverage - refined keyword extraction
    title_eng = re.findall(r'[A-Za-z][A-Za-z]+', title)  # words of 2+ letters
    
    if 'SEO' in title_eng:
        # For SEO-related posts, primary keyword is often just "SEO" or "SEO [concept]"
        keyword = 'SEO'
        # But also check if there's a more specific phrase
        if 'Voice' in title_eng and 'Search' in title_eng:
            keyword = 'Voice Search'
        elif 'My' in title_eng and 'Business' in title_eng:
            keyword = 'Google My Business'
        elif 'Website' in title_eng and 'Speed' in title_eng:
            keyword = 'Website Speed'
        elif 'Audit' in title_eng and 'Checklist' in title_eng:
            keyword = 'SEO Audit'
        elif 'Affiliate' in title_eng:
            keyword = 'Affiliate SEO'
        elif 'Legal' in title_eng:
            keyword = 'SEO Legal'
        elif 'Restaurant' in title_eng or 'Cafe' in title_eng:
            keyword = 'Restaurant SEO'
        elif 'Cleaning' in title_eng and 'Service' in title_eng:
            keyword = 'Cleaning Service'
        elif 'Dashboard' in title_eng:
            keyword = 'SEO Dashboard'
        elif 'New' in title_eng and 'Website' in title_eng:
            keyword = 'New Website SEO'
        elif 'Consultant' in title_eng:
            keyword = 'SEO Consultant'
        else:
            keyword = 'SEO'
    elif title_eng:
        keyword = ' '.join(title_eng[:3])
    else:
        # Bengali-only title - derive from slug
        keyword = target_slug.replace('-', ' ').replace('dhaka', 'Dhaka').replace('bangladesh', 'Bangladesh')
    
    count = count_keyword(content_text, keyword)
    if count >= 5:
        print(f"| A. TF-IDF Coverage | ✅ PASS | Keyword '{keyword}' found {count} times |")
    else:
        print(f"| A. TF-IDF Coverage | ❌ FAIL | Keyword '{keyword}' found only {count} times (< 5) |")
    
    # B. Semantic Entity Coverage
    entities = []
    if re.search(r'Dhaka|ঢাকা', content_text, re.IGNORECASE):
        entities.append("Dhaka")
    if re.search(r'Bangladesh|বাংলাদেশ', content_text, re.IGNORECASE):
        entities.append("Bangladesh")
    service_found = [t for t in ['service','services','SEO','optimization','marketing'] if re.search(r'\b' + re.escape(t) + r'\b', content_text, re.IGNORECASE)]
    if service_found:
        entities.append(f"Service({', '.join(service_found[:3])})")
    
    ind_map = {
        'seo-consultant':['consultant','business','e-commerce'],
        'google-my-business':['restaurant','dental','salon'],
        'seo-for-new-website':['website','business','cms'],
        'website-speed':['website','e-commerce','hosting'],
        'seo-audit':['website','business','e-commerce'],
        'affiliate-seo':['affiliate','e-commerce','fashion'],
        'voice-search-seo':['business','restaurant','smartphone'],
        'seo-legal-compliance':['business','garments','industry'],
        'seo-for-restaurants':['restaurant','cafe','food'],
        'seo-for-cleaning-services':['cleaning','service','office'],
        'seo-dashboard-tools':['marketer','dashboard','tool']
    }
    for key, terms in ind_map.items():
        if key in target_slug:
            found_ind = [t for t in terms if re.search(r'\b' + re.escape(t) + r'\b', content_text, re.IGNORECASE)]
            if found_ind:
                entities.append(f"Industry({', '.join(found_ind[:3])})")
            else:
                entities.append(f"Industry(⚠️ none of {', '.join(terms[:3])})")
            break
    
    missing_b = []
    if not re.search(r'Dhaka|ঢাকা', content_text, re.IGNORECASE):
        missing_b.append("Dhaka")
    if not re.search(r'Bangladesh|বাংলাদেশ', content_text, re.IGNORECASE):
        missing_b.append("Bangladesh")
    
    if missing_b:
        print(f"| B. Semantic Entity | ❌ FAIL | Missing: {', '.join(missing_b)}. Found: {'; '.join(entities)} |")
    else:
        print(f"| B. Semantic Entity | ✅ PASS | Found: {'; '.join(entities)} |")
    
    # C. Pillar-Cluster Alignment
    pillar_links = re.findall(r'\(/(?:blog|services|industries|locations)/[^)]+\)', content_text)
    if pillar_links:
        examples = [p.split('/')[-1].rstrip(')') for p in pillar_links[:3]]
        print(f"| C. Pillar-Cluster | ✅ PASS | {len(pillar_links)} links: {', '.join(examples)} |")
    else:
        print(f"| C. Pillar-Cluster | ❌ FAIL | No pillar/cluster links found |")
    
    # D. AEO/GEO Question Headings
    qh = re.findall(r'^#{2,3}\s+(How|What|Why|When|Where|Can|Do|Is|Are)\b', content_text, re.MULTILINE | re.IGNORECASE)
    if len(qh) >= 2:
        print(f"| D. AEO/GEO | ✅ PASS | {len(qh)} question headings: {', '.join(qh[:5])} |")
    else:
        print(f"| D. AEO/GEO | ❌ FAIL | Only {len(qh)} question headings (< 2): {', '.join(qh) if qh else 'none'} |")
    
    # E. Internal Linking
    internal_links = re.findall(r'\(/(?:blog|services|locations|industries)/[^)]+\)', content_text)
    if len(internal_links) >= 3:
        print(f"| E. Internal Linking | ✅ PASS | {len(internal_links)} internal links found |")
    else:
        print(f"| E. Internal Linking | ❌ FAIL | Only {len(internal_links)} internal links (< 3) |")
    
    # F. Schema Fields
    missing_f = []
    if not post_data.get('title'): missing_f.append('title')
    if not post_data.get('excerpt'): missing_f.append('excerpt')
    if not post_data.get('date'): missing_f.append('date')
    if missing_f:
        print(f"| F. Schema Fields | ❌ FAIL | Missing: {', '.join(missing_f)} |")
    else:
        print(f"| F. Schema Fields | ✅ PASS | All present (title, excerpt, date) |")
    
    print()
    print("### Fix instructions:")
    fixes = []
    
    if count < 5:
        fixes.append(f"- **A (TF-IDF):** Increase usage of keyword '{keyword}' to >=5 (currently {count}).")
    if missing_b:
        fixes.append(f"- **B (Semantic Entity):** Add missing: {', '.join(missing_b)}.")
    if not pillar_links:
        fixes.append("- **C (Pillar-Cluster):** Add link to /services/, /blog/, /industries/, or /locations/.")
    if len(qh) < 2:
        fixes.append(f"- **D (AEO/GEO):** Add question headings (How/What/Why/When/Where/Can/Do/Is/Are). Currently {len(qh)}.")
    if len(internal_links) < 3:
        fixes.append(f"- **E (Internal Linking):** Add more internal links. Currently {len(internal_links)}.")
    if missing_f:
        fixes.append(f"- **F (Schema):** Add missing: {', '.join(missing_f)}.")
    
    if fixes:
        for f in fixes:
            print(f)
    else:
        print("- All checks passed. No fixes needed.")
    
    print()
    print("---")
    print()
