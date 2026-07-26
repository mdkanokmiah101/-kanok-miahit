#!/usr/bin/env python3
"""Run content framework checks on Batch 5 blog posts."""
import re, json

with open('/root/kanok-miahit/src/app/blog/data.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract each post's data by slug
posts_data = {}
# Find post objects by slug
post_pattern = re.compile(
    r"slug:\s*\"([^\"]+)\".*?title:\s*\"([^\"]+)\".*?date:\s*\"([^\"]+)\".*?excerpt:\s*\"([^\"]+)\".*?tags:\s*\[([^\]]+)\].*?imagePlaceholder:\s*\"([^\"]+)\".*?content:\s*`(.*?)`\s*,\s*\n\s*\}", 
    re.DOTALL
)

matches = post_pattern.findall(content)
for m in matches:
    slug = m[0]
    posts_data[slug] = {
        'slug': slug,
        'title': m[1],
        'date': m[2],
        'excerpt': m[3],
        'tags': m[4],
        'imagePlaceholder': m[5],
        'content': m[6]
    }

batch5_slugs = [
    'long-tail-keywords-bangladesh',
    'seo-for-facebook-marketplace',
    'seo-for-youtube-channel-bangla',
    'seo-google-updates-2026',
    'seo-semantic-search-bangla',
    'seo-for-hotel-resort-bangladesh',
    'seo-google-business-profile-posts',
    'seo-local-citations-bangladesh',
    'seo-for-ngo-bangladesh',
    'seo-career-guide-bangladesh-2026'
]

def count_occurrences(text, keyword):
    """Count occurrences of a keyword in text (case-insensitive)."""
    if not keyword:
        return 0
    return len(re.findall(re.escape(keyword), text, re.IGNORECASE))

def check_tfidf(post):
    """Check A: TF-IDF Coverage - primary keyword from title count."""
    title = post['title']
    content_text = post['content']
    
    # Extract primary keyword from title - take first meaningful word(s)
    # First clean title: remove prefixes like "SEO", "গাইড" etc if they appear
    # For Bengali titles, take the first noun phrase
    title_clean = title.replace(':', ' ').replace('—', ' ').replace('|', ' ').strip()
    
    # Strategy: Extract keywords from title - take key noun phrases
    # For Bengali, split on spaces and take first several words
    words = title_clean.split()
    
    # For English/Bengali mixed titles, extract the main topic
    # Try to find the core keyword
    primary_keyword = words[0] if words else ''
    
    # Better: take first 2-4 words that form a meaningful phrase
    # For English content in title
    eng_keywords = re.findall(r'[A-Za-z]+', title)
    
    # For Bengali, take first content word(s) from title
    bengali_pattern = re.findall(r'[\u0980-\u09FF]+', title)
    
    keyword_candidates = []
    if bengali_pattern:
        keyword_candidates = [bengali_pattern[0]]
    if eng_keywords:
        keyword_candidates = eng_keywords[:2]
    
    # Use first keyword phrase
    keyword_to_search = ''
    if bengali_pattern:
        keyword_to_search = bengali_pattern[0] if len(bengali_pattern) >= 1 else ''
    if eng_keywords and not bengali_pattern:
        keyword_to_search = eng_keywords[0] if eng_keywords else words[0]
    
    if not keyword_to_search and words:
        keyword_to_search = words[0]
    
    # For "লং-টেল কীওয়ার্ড" - use the full term
    if 'লং-টেল' in title:
        keyword_to_search = 'লং-টেল কীওয়ার্ড'
    elif 'ফেসবুক মার্কেটপ্লেস' in title:
        keyword_to_search = 'ফেসবুক মার্কেটপ্লেস'
    elif 'ইউটিউব চ্যানেল' in title or 'ইউটিউব SEO' in title or 'ইউটিউব' in title:
        keyword_to_search = 'ইউটিউব'
    elif 'গুগল আপডেট' in title:
        keyword_to_search = 'গুগল আপডেট'
    elif 'সেম্যান্টিক সার্চ' in title:
        keyword_to_search = 'সেম্যান্টিক সার্চ'
    elif 'হোটেল ও রিসোর্ট' in title:
        keyword_to_search = 'হোটেল'
    elif 'গুগল বিজনেস প্রোফাইল' in title:
        keyword_to_search = 'গুগল বিজনেস প্রোফাইল'
    elif 'লোকাল সাইটেশন' in title:
        keyword_to_search = 'লোকাল সাইটেশন'
    elif 'এনজিও' in title:
        keyword_to_search = 'এনজিও'
    elif 'SEO ক্যারিয়ার' in title or 'SEO কেরিয়ার' in title or 'SEO পেশা' in title:
        keyword_to_search = 'SEO'
    
    count = count_occurrences(content_text, keyword_to_search)
    passed = count >= 5
    return passed, f"Primary keyword '{keyword_to_search}' mentioned {count} times in content", keyword_to_search, count

def check_semantic_entities(post):
    """Check B: Semantic Entity Coverage - Dhaka/Bangladesh, service, industry entities."""
    content_text = post['content']
    title = post['title']
    
    entities_found = []
    entities_missing = []
    
    # Check for "Dhaka" or "ঢাকা"
    if re.search(r'ঢাকা|Dhaka', content_text):
        entities_found.append('Dhaka/ঢাকা')
    else:
        entities_missing.append('Dhaka/ঢাকা')
    
    # Check for "Bangladesh" or "বাংলাদেশ"
    if re.search(r'বাংলাদেশ|Bangladesh', content_text):
        entities_found.append('Bangladesh/বাংলাদেশ')
    else:
        entities_missing.append('Bangladesh/বাংলাদেশ')
    
    # Check for service-related entities
    service_entities = ['সার্ভিস', 'Service', 'SEO', 'ডিজিটাল মার্কেটিং', 'Digital Marketing']
    service_found = [s for s in service_entities if re.search(re.escape(s), content_text, re.IGNORECASE)]
    if service_found:
        entities_found.append(f"Service ({', '.join(set(s.lower() for s in service_found[:3]))})")
    else:
        entities_missing.append('Service entity')
    
    # Check for industry entities
    industry_entities = ['ব্যবসা', 'Business', 'ই-কমার্স', 'E-commerce', 'টেকনোলজি', 'Technology', 
                         'গার্মেন্টস', 'রিয়েল এস্টেট', 'হোটেল', 'শিক্ষা', 'স্বাস্থ্য']
    industry_found = [i for i in industry_entities if re.search(i, content_text)]
    if industry_found:
        entities_found.append(f"Industry ({', '.join(industry_found[:3])})")
    else:
        entities_missing.append('Industry entity')
    
    passed = len(entities_missing) == 0
    details = "Found: " + ", ".join(entities_found)
    if entities_missing:
        details += " | Missing: " + ", ".join(entities_missing)
    return passed, details

def check_pillar_cluster(post):
    """Check C: Pillar-Cluster Alignment - link to pillar or service page."""
    content_text = post['content']
    
    # Look for links to service pages or pillar blog posts
    pillar_links = re.findall(r'/services/[^\s\)\"\'<>]+', content_text)
    service_page_links = re.findall(r'/blog/[^\s\)\"\'<>]+', content_text)
    
    all_internal_links = pillar_links + service_page_links
    # Also check /industries/ and /locations/
    industry_links = re.findall(r'/industries[^\s\)\"\'<>]*', content_text)
    location_links = re.findall(r'/locations/[^\s\)\"\'<>]+', content_text)
    
    all_relevant = pillar_links + service_page_links + industry_links + location_links
    
    # Filter out self-references
    slug = post['slug']
    self_refs = [l for l in all_relevant if slug in l]
    other_links = [l for l in all_relevant if slug not in l]
    
    passed = len(other_links) >= 1
    if passed:
        details = f"Links to pillar/service pages found: {len(other_links)} (e.g., {', '.join(other_links[:3])})"
    else:
        details = "No links to pillar or service pages found"
    return passed, details, other_links

def check_aeo_geo(post):
    """Check D: AEO/GEO - question headings count."""
    content_text = post['content']
    
    # Find headings (## or ###) that start with question words
    heading_pattern = re.findall(r'^#{2,3}\s+(.+)$', content_text, re.MULTILINE)
    
    question_words = ['How', 'What', 'Why', 'When', 'Where', 'Can', 'Do', 'Is', 'Are',
                      'কী', 'কেন', 'কখন', 'কোথায়', 'কীভাবে', 'কিভাবে', 'কেমন', 'কোন',
                      'How', 'What', 'Why', 'When', 'Where']
    
    question_headings = []
    for h in heading_pattern:
        h_clean = h.strip()
        for qw in question_words:
            if h_clean.lower().startswith(qw.lower()):
                if h_clean not in question_headings:
                    question_headings.append(h_clean)
                break
    
    # Also check content for question-answer sections
    question_lines = re.findall(r'^###\s+[^:।\n]+\?', content_text, re.MULTILINE)
    
    all_questions = list(set(question_headings + [q.strip() for q in question_lines]))
    
    count = len(all_questions)
    passed = count >= 2
    
    if passed:
        details = f"{count} question headings found (e.g., {', '.join(all_questions[:3])})"
    else:
        details = f"Only {count} question headings found (need ≥2)"
    return passed, details, all_questions

def check_internal_linking(post):
    """Check E: Internal Linking - count internal links."""
    content_text = post['content']
    slug = post['slug']
    
    # Count internal links matching patterns
    blog_links = re.findall(r'/blog/[^\s\)\"\'<>]+', content_text)
    services_links = re.findall(r'/services/[^\s\)\"\'<>]+', content_text)
    locations_links = re.findall(r'/locations/[^\s\)\"\'<>]+', content_text)
    industries_links = re.findall(r'/industries[^\s\)\"\'<>]*', content_text)
    
    # Remove self-references
    all_links = blog_links + services_links + locations_links + industries_links
    other_links = [l for l in all_links if slug not in l]
    
    count = len(other_links)
    passed = count >= 3
    
    breakdown = f"blog:{len(blog_links)}, services:{len(services_links)}, locations:{len(locations_links)}, industries:{len(industries_links)}"
    if passed:
        details = f"{count} internal links found ({breakdown})"
    else:
        details = f"Only {count} internal links found, need ≥3 ({breakdown})"
    return passed, details, count

def check_schema(post):
    """Check F: Schema - title, excerpt, date fields present."""
    present = []
    missing = []
    
    # title field
    if post.get('title'):
        present.append('title')
    else:
        missing.append('title')
    
    # excerpt field  
    if post.get('excerpt'):
        present.append('excerpt')
    else:
        missing.append('excerpt')
    
    # date field
    if post.get('date'):
        present.append('date')
    else:
        missing.append('date')
    
    passed = len(missing) == 0
    if passed:
        details = f"All schema fields present: {', '.join(present)}"
    else:
        details = f"Missing: {', '.join(missing)}. Present: {', '.join(present)}"
    return passed, details

print("=" * 80)
print("BATCH 5 CONTENT FRAMEWORK CHECKS")
print("=" * 80)

for slug in batch5_slugs:
    if slug not in posts_data:
        print(f"\n## Post: {slug}")
        print("| Check | Status | Details |")
        print("|-------|--------|---------|")
        print(f"| A. TF-IDF | ⚠️ FAIL | Post data not found in data.js (regex may not match) |")
        continue
    
    post = posts_data[slug]
    print(f"\n## Post: {slug}")
    print(f"Title: {post['title'][:80]}...")
    print(f"| Check | Status | Details |")
    print(f"|-------|--------|---------|")
    
    # A. TF-IDF
    passed_a, detail_a, kw, cnt = check_tfidf(post)
    status_a = "✅ PASS" if passed_a else "⚠️ FAIL"
    print(f"| A. TF-IDF | {status_a} | {detail_a} |")
    
    # B. Semantic Entities
    passed_b, detail_b = check_semantic_entities(post)
    status_b = "✅ PASS" if passed_b else "⚠️ FAIL"
    print(f"| B. Semantic Entities | {status_b} | {detail_b} |")
    
    # C. Pillar-Cluster
    passed_c, detail_c, pillar_links = check_pillar_cluster(post)
    status_c = "✅ PASS" if passed_c else "⚠️ FAIL"
    print(f"| C. Pillar-Cluster | {status_c} | {detail_c} |")
    
    # D. AEO/GEO
    passed_d, detail_d, questions = check_aeo_geo(post)
    status_d = "✅ PASS" if passed_d else "⚠️ FAIL"
    print(f"| D. AEO/GEO | {status_d} | {detail_d} |")
    
    # E. Internal Linking
    passed_e, detail_e, link_count = check_internal_linking(post)
    status_e = "✅ PASS" if passed_e else "⚠️ FAIL"
    print(f"| E. Internal Linking | {status_e} | {detail_e} |")
    
    # F. Schema
    passed_f, detail_f = check_schema(post)
    status_f = "✅ PASS" if passed_f else "⚠️ FAIL"
    print(f"| F. Schema | {status_f} | {detail_f} |")
    
    # Fix instructions
    print("### Fix instructions:")
    fixes = []
    if not passed_a:
        fixes.append(f"- **TF-IDF**: Increase mentions of primary keyword '{kw}' (currently {cnt}) to ≥5 in content.")
    if not passed_b:
        fixes.append(f"- **Semantic Entities**: Add missing entities: check detail above.")
    if not passed_c:
        fixes.append("- **Pillar-Cluster**: Add at least 1 link to a pillar page (/blog/...) or service page (/services/...).")
    if not passed_d:
        fixes.append(f"- **AEO/GEO**: Add more question headings (How/What/Why/When/Where/Can/Do/Is/Are/কী/কেন/কিভাবে). Currently {len(questions)} found, need ≥2.")
    if not passed_e:
        fixes.append(f"- **Internal Linking**: Add more internal links to /blog/, /services/, /locations/, or /industries/. Currently {link_count}, need ≥3.")
    if not passed_f:
        fixes.append("- **Schema**: Ensure title, excerpt, and date fields are present in the post object.")
    
    if not fixes:
        print("All checks passed — no fixes needed.")
    else:
        for fix in fixes:
            print(fix)

print("\n" + "=" * 80)
print("SUMMARY TABLE")
print("=" * 80)
print(f"{'Post':<40} {'TF-IDF':<8} {'Entities':<10} {'Pillar':<8} {'AEO/GEO':<8} {'Int.Link':<8} {'Schema':<8}")
print("-" * 90)
for slug in batch5_slugs:
    if slug not in posts_data:
        print(f"{slug:<40} {'N/A':<8} {'N/A':<10} {'N/A':<8} {'N/A':<8} {'N/A':<8} {'N/A':<8}")
        continue
    post = posts_data[slug]
    a, _, _, _ = check_tfidf(post)
    b, _ = check_semantic_entities(post)
    c, _, _ = check_pillar_cluster(post)
    d, _, _ = check_aeo_geo(post)
    e, _, _ = check_internal_linking(post)
    f, _ = check_schema(post)
    status = lambda x: "✅" if x else "⚠️"
    name = slug[:39]
    print(f"{name:<40} {status(a):<8} {status(b):<10} {status(c):<8} {status(d):<8} {status(e):<8} {status(f):<8}")
