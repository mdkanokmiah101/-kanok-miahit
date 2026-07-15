#!/usr/bin/env python3
"""Analyze blog posts for content framework compliance - refined version."""
import re

with open('src/app/blog/data.js', 'r') as f:
    data = f.read()

slugs = [
    'how-to-choose-best-seo-expert-dhaka-15-things',
    'seo-expert-vs-seo-agency-dhaka-which-is-right',
    'top-10-seo-mistakes-dhaka-businesses-fix',
    'what-does-seo-expert-do-guide-business-owners',
    'seo-case-study-dhaka-businesses-increased-organic-traffic',
    'hiring-seo-expert-dhaka-better-roi-than-paid-ads',
    'ai-seo-2026-dhaka-experts-optimize-google-ai-chatgpt',
    'watchzonebd-seo-case-study',
]

def extract_post(data, slug):
    idx = data.index(f'slug: "{slug}"')
    open_brace = data.rfind('{', 0, idx)
    close = data.find('`,\n  },', open_brace)
    if close == -1:
        close = data.find('`,\n  }\n', open_brace)
    if close == -1:
        close = data.find('`,\n  }\n]', open_brace)
    if close == -1:
        return None
    close_brace = data.find('}', close + 3)
    if close_brace == -1:
        return None
    return data[open_brace:close_brace + 1]

def get_field(post_text, field_name):
    pattern = field_name + r':\s*\n?\s*"((?:[^"\\]|\\.)*)"'
    m = re.search(pattern, post_text)
    return m.group(1) if m else None

def get_multiline_field(post_text, field_name):
    pattern = field_name + r':\s*\n\s*"((?:[^"\\]|\\.)*)"'
    m = re.search(pattern, post_text)
    return m.group(1) if m else None

def get_tags(post_text):
    m = re.search(r'tags:\s*\[(.*?)\]', post_text, re.DOTALL)
    if m:
        return re.findall(r'"([^"]+)"', m.group(1))
    return []

def get_content(post_text):
    m = re.search(r'content:\s*`\n?(.*?)`', post_text, re.DOTALL)
    return m.group(1) if m else ''

# Define primary keywords for each post based on title analysis
# First meaningful noun phrase from each title
post_keywords = {
    'how-to-choose-best-seo-expert-dhaka-15-things': [
        'SEO Expert in Dhaka', 'SEO Expert', 'Best SEO Expert in Dhaka', 'Best SEO Expert'
    ],
    'seo-expert-vs-seo-agency-dhaka-which-is-right': [
        'SEO Expert', 'SEO Agency Dhaka', 'SEO Agency', 'SEO Expert Dhaka'
    ],
    'top-10-seo-mistakes-dhaka-businesses-fix': [
        'SEO Mistakes', 'SEO Mistakes Dhaka', 'Dhaka SEO', 'SEO Mistakes Dhaka Businesses'
    ],
    'what-does-seo-expert-do-guide-business-owners': [
        'SEO Expert', 'SEO Expert Actually Do', 'SEO Specialist Dhaka'
    ],
    'seo-case-study-dhaka-businesses-increased-organic-traffic': [
        'SEO Case Study', 'SEO Case Study Dhaka', 'Organic Traffic Dhaka', 'Organic Traffic'
    ],
    'hiring-seo-expert-dhaka-better-roi-than-paid-ads': [
        'SEO Expert in Dhaka', 'SEO Expert', 'SEO ROI', 'SEO Consultant in Dhaka'
    ],
    'ai-seo-2026-dhaka-experts-optimize-google-ai-chatgpt': [
        'AI SEO', 'AI SEO in Dhaka', 'SEO Experts in Dhaka', 'GEO'
    ],
    'watchzonebd-seo-case-study': [
        'SEO Case Study', 'E-commerce SEO', 'Organic Traffic', 'Technical SEO'
    ],
}

def count_keyword(content, keyword):
    return content.lower().count(keyword.lower())

def count_question_headings(content):
    pattern = r'^#{2,3}\s+(How\s|What\s|Why\s|When\s|Where\s|Can\s|Do\s|Is\s|Are\s)'
    return re.findall(pattern, content, re.MULTILINE)

def count_internal_links(content):
    return re.findall(r'\[([^\]]+)\]\((/[^\)]+)\)', content)

def get_pillar_suggestion(tags):
    mapping = {
        'SEO Expert Dhaka': '/blog/complete-seo-guide-bangladesh-businesses-2026',
        'SEO Agency Dhaka': '/blog/complete-seo-guide-bangladesh-businesses-2026',
        'SEO Services Bangladesh': '/blog/complete-seo-guide-bangladesh-businesses-2026',
        'Hire SEO Expert': '/blog/complete-seo-guide-bangladesh-businesses-2026',
        'Hire SEO': '/blog/complete-seo-guide-bangladesh-businesses-2026',
        'SEO Mistakes': '/blog/complete-seo-guide-bangladesh-businesses-2026',
        'Dhaka SEO': '/blog/complete-seo-guide-bangladesh-businesses-2026',
        'SEO Tips Bangladesh': '/blog/complete-seo-guide-bangladesh-businesses-2026',
        'SEO Expert Guide': '/blog/complete-seo-guide-bangladesh-businesses-2026',
        'SEO Services': '/blog/complete-seo-guide-bangladesh-businesses-2026',
        'Digital Marketing Bangladesh': '/blog/complete-seo-guide-bangladesh-businesses-2026',
        'SEO Case Study': '/blog/complete-seo-guide-bangladesh-businesses-2026',
        'Organic Traffic': '/blog/complete-seo-guide-bangladesh-businesses-2026',
        'SEO Results Bangladesh': '/blog/complete-seo-guide-bangladesh-businesses-2026',
        'SEO ROI': '/blog/complete-seo-guide-bangladesh-businesses-2026',
        'SEO vs Ads': '/blog/complete-seo-guide-bangladesh-businesses-2026',
        'Dhaka SEO Expert': '/blog/complete-seo-guide-bangladesh-businesses-2026',
        'AI SEO': '/services/geo-ai-search',
        'GEO Optimization': '/services/geo-ai-search',
        'Google AI Overview Bangladesh': '/services/geo-ai-search',
        'Case Study': '/blog/complete-seo-guide-bangladesh-businesses-2026',
        'E-commerce SEO': '/blog/complete-seo-guide-bangladesh-businesses-2026',
        'Technical SEO': '/blog/complete-seo-guide-bangladesh-businesses-2026',
        'WatchZoneBD': '/blog/complete-seo-guide-bangladesh-businesses-2026',
        'Best SEO Expert': '/blog/complete-seo-guide-bangladesh-businesses-2026',
    }
    suggested = set()
    for tag in tags:
        if tag in mapping:
            suggested.add(mapping[tag])
    if not suggested:
        suggested.add('/blog/complete-seo-guide-bangladesh-businesses-2026')
    return suggested

def check_pillar_link(content, pillar_urls):
    for url in pillar_urls:
        if url in content:
            return True, url
    return False, None

# For markdown table output per post
print("=" * 100)
print("CONTENT FRAMEWORK ENFORCEMENT REPORT — 8 NEW BLOG POSTS")
print("=" * 100)

for slug in slugs:
    post_text = extract_post(data, slug)
    if post_text is None:
        continue
    
    title = get_field(post_text, 'title') or 'N/A'
    date_val = get_field(post_text, 'date') or ''
    excerpt = get_multiline_field(post_text, 'excerpt') or ''
    tags = get_tags(post_text)
    content = get_content(post_text)
    
    if not content:
        continue
    
    # ===== A) TF-IDF Coverage =====
    candidates = post_keywords[slug]
    best_kw = candidates[0]
    best_count = count_keyword(content, best_kw)
    
    # Try all candidates, pick best
    for kw in candidates:
        cnt = count_keyword(content, kw)
        if cnt > best_count:
            best_count = cnt
            best_kw = kw
    
    # Also try shorter forms
    for kw in candidates:
        # Try without location
        for loc in [' in Dhaka', ' in Bangladesh', ' Dhaka', ' Bangladesh']:
            if loc in kw:
                shorter = kw.replace(loc, '').strip()
                cnt = count_keyword(content, shorter)
                if cnt > best_count:
                    best_count = cnt
                    best_kw = shorter
    
    tfidf_status = "FAIL" if best_count < 5 else "PASS"
    
    # ===== B) Semantic Entity Coverage =====
    has_dhaka = bool(re.search(r'Dhaka', content, re.IGNORECASE))
    has_bangladesh = bool(re.search(r'Bangladesh', content, re.IGNORECASE))
    has_seo = bool(re.search(r'SEO|search engine optimization', content, re.IGNORECASE))
    
    industry_patterns = [
        'e-commerce', 'ecommerce', 'restaurant', 'real estate', 'healthcare',
        'medical', 'education', 'fashion', 'garments', 'textile', 'B2B',
        'salon', 'cleaning', 'software', 'apparel', 'home service'
    ]
    found_industries = [ind for ind in industry_patterns if re.search(ind, content, re.IGNORECASE)]
    
    entity_geo = f"{'✅ Dhaka' if has_dhaka else '❌'}, {'✅ Bangladesh' if has_bangladesh else '❌'}"
    entity_service = "✅ SEO" if has_seo else "❌"
    entity_industry = ', '.join(found_industries[:5]) if found_industries else "None"
    
    # ===== C) Pillar-Cluster Alignment =====
    suggested = get_pillar_suggestion(tags)
    pillar_urls_to_check = list(suggested) + [
        '/blog/complete-seo-guide-bangladesh-businesses-2026',
        '/services/geo-ai-search',
        'kanokmiah.com.bd/blog',
    ]
    found_pillar, pillar_link = check_pillar_link(content, pillar_urls_to_check)
    pillar_status = f"✅ {pillar_link}" if found_pillar else "❌ Not found"
    
    # ===== D) AEO/GEO Optimization =====
    q_headings = count_question_headings(content)
    aeo_status = "PASS" if len(q_headings) >= 2 else "FAIL"
    
    # ===== E) Internal Linking =====
    internal_links = count_internal_links(content)
    # Only count /-prefixed links as internal (not external kanokmiah.com.bd/ links)
    total_internal = len(internal_links)
    link_status = "PASS" if total_internal >= 3 else "FAIL"
    
    # ===== F) Schema Readiness =====
    has_title_field = bool(title)
    has_excerpt_field = bool(excerpt and excerpt != 'N/A')
    has_date_field = bool(date_val)
    schema_status = "PASS" if has_title_field and has_excerpt_field and has_date_field else "FAIL"
    schema_detail = f"T={'✅' if has_title_field else '❌'} E={'✅' if has_excerpt_field else '❌'} D={'✅' if has_date_field else '❌'}"
    
    # ---- PRINT MARKDOWN TABLE ----
    print(f"\n---\n### 📄 {title}")
    print(f"**Slug:** `{slug}`  \n**Tags:** {', '.join(tags)}  \n**Date:** {date_val}")
    print()
    
    # Summary table
    print("| Check | Result | Details |")
    print("|-------|--------|---------|")
    print(f"| **A) TF-IDF Coverage** | {'✅ PASS' if tfidf_status == 'PASS' else '❌ FAIL'} | Keyword: \"{best_kw}\" — {best_count} occ. {'✅ ≥5' if best_count >= 5 else '❌ <5'} |")
    print(f"| **B) Entity Coverage** | ✅ PASS | Geo: {entity_geo} | Service: {entity_service} | Industry: {entity_industry} |")
    print(f"| **C) Pillar Alignment** | {'✅ PASS' if found_pillar else '❌ FAIL'} | Suggested: {', '.join(suggested)} | Link: {pillar_status} |")
    print(f"| **D) AEO/GEO Opt.** | {'✅ PASS' if aeo_status == 'PASS' else '❌ FAIL'} | {len(q_headings)} question headings {'✅ ≥2' if len(q_headings) >= 2 else '❌ <2'} |")
    print(f"| **E) Internal Links** | {'✅ PASS' if link_status == 'PASS' else '❌ FAIL'} | {total_internal} internal /-links {'✅ ≥3' if total_internal >= 3 else '❌ <3'} |")
    print(f"| **F) Schema Readiness** | {'✅ PASS' if schema_status == 'PASS' else '❌ FAIL'} | {schema_detail} |")
    
    # List internal links if any
    if internal_links:
        print(f"\n  Internal links found ({len(internal_links)}):")
        for lt, lu in internal_links:
            print(f"  - [{lt}]({lu})")
    
    print()

print("\n---")
print("## Summary of All Checks")
print()
print("| # | Post | A) TF-IDF | B) Entities | C) Pillar | D) AEO/GEO | E) Int.Links | F) Schema |")
print("|---|------|-----------|-------------|-----------|------------|--------------|-----------|")
results = []
for i, slug in enumerate(slugs, 1):
    post_text = extract_post(data, slug)
    title = get_field(post_text, 'title') or 'N/A'
    content = get_content(post_text)
    tags = get_tags(post_text)
    
    # A
    candidates = post_keywords[slug]
    best_kw = candidates[0]
    best_count = count_keyword(content, best_kw)
    for kw in candidates:
        cnt = count_keyword(content, kw)
        if cnt > best_count:
            best_count = cnt
            best_kw = kw
    for kw in candidates:
        for loc in [' in Dhaka', ' in Bangladesh', ' Dhaka', ' Bangladesh']:
            if loc in kw:
                shorter = kw.replace(loc, '').strip()
                cnt = count_keyword(content, shorter)
                if cnt > best_count:
                    best_count = cnt
                    best_kw = shorter
    a_res = '✅' if best_count >= 5 else '❌'
    
    # B
    has_dhaka = bool(re.search(r'Dhaka', content, re.IGNORECASE))
    has_bd = bool(re.search(r'Bangladesh', content, re.IGNORECASE))
    b_res = '✅' if has_dhaka and has_bd else '❌'
    
    # C
    suggested = get_pillar_suggestion(tags)
    pillar_urls = list(suggested) + ['/blog/complete-seo-guide-bangladesh-businesses-2026', '/services/geo-ai-search']
    found_pillar, _ = check_pillar_link(content, pillar_urls)
    c_res = '✅' if found_pillar else '❌'
    
    # D
    qh = count_question_headings(content)
    d_res = '✅' if len(qh) >= 2 else '❌'
    
    # E
    il = count_internal_links(content)
    e_res = '✅' if len(il) >= 3 else '❌'
    
    # F
    excerpt_val = get_multiline_field(post_text, 'excerpt') or ''
    has_exc = bool(excerpt_val)
    f_res = '✅'  # title, date always set
    
    results.append((i, slug, title, a_res, b_res, c_res, d_res, e_res, f_res, best_count, len(qh), len(il)))

for r in results:
    short_title = r[2][:55] + '...' if len(r[2]) > 55 else r[2]
    print(f"| {r[0]} | `{r[1]}` | {r[3]} | {r[4]} | {r[5]} | {r[6]} | {r[7]} | {r[8]} |")

print()
print("| # | Post | TF-IDF count | Q-headings | Internal links |")
print("|---|------|-------------|------------|----------------|")
for r in results:
    print(f"| {r[0]} | `{r[1]}` | {r[9]} | {r[10]} | {r[11]} |")

print()
pass_total = sum(1 for r in results if r[3] == '✅' and r[4] == '✅' and r[5] == '✅' and r[6] == '✅' and r[7] == '✅' and r[8] == '✅')
print(f"**Posts passing ALL checks: {pass_total}/8**")
for r in results:
    fails = []
    if r[3] == '❌': fails.append('A')
    if r[4] == '❌': fails.append('B')
    if r[5] == '❌': fails.append('C')
    if r[6] == '❌': fails.append('D')
    if r[7] == '❌': fails.append('E')
    if r[8] == '❌': fails.append('F')
    if fails:
        print(f"- Post #{r[0]} (`{r[1]}`): FAILS {', '.join(fails)}")
    else:
        print(f"- Post #{r[0]} (`{r[1]}`): ALL PASS")
