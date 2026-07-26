#!/usr/bin/env python3
"""Content framework checks for Batch 7 blog posts - v2 with Bangla support."""
import re

# ========== CONFIGURATION ==========
DATA_FILE = "/root/kanok-miahit/src/app/blog/data.js"

BATCH7_SLUGS = [
    "seo-mistakes-to-avoid-bangladesh",
    "seo-website-migration-guide-bd",
    "google-tag-manager-seo-bd",
    "seo-google-analytics-4-bangladesh",
    "seo-keyword-clustering-bangladesh",
    "seo-competitor-analysis-bangladesh",
    "seo-landing-page-optimization-bd",
    "seo-for-mobile-apps-bangladesh",
    "google-discover-seo-bangladesh",
    "seo-for-podcast-bangladesh",
    "seo-pillar-content-strategy-bd",
    "seo-skyscraper-technique-bangladesh",
    "seo-content-repurposing-bangladesh",
    "seo-hubspot-vs-wordpress-bd",
    "seo-domain-authority-bangladesh",
    "seo-page-authority-bangladesh",
    "seo-referral-traffic-bangladesh",
    "seo-direct-traffic-bangladesh",
    "seo-branded-vs-non-branded-bd",
    "seo-search-intent-optimization",
]


def read_file_to_string(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def extract_posts(content):
    """Parse all posts from data.js."""
    posts = []
    slug_pattern = re.compile(r'^\s+slug:\s*"([^"]+)",\s*$', re.MULTILINE)
    slug_matches = list(slug_pattern.finditer(content))
    
    for i, slug_match in enumerate(slug_matches):
        slug = slug_match.group(1)
        post_start = slug_match.start()
        
        if i + 1 < len(slug_matches):
            post_end = slug_matches[i + 1].start()
        else:
            post_end = len(content)
        
        post_text = content[post_start:post_end]
        
        title_m = re.search(r'title:\s*"([^"]*)"', post_text)
        date_m = re.search(r'date:\s*"([^"]*)"', post_text)
        author_m = re.search(r'author:\s*"([^"]*)"', post_text)
        excerpt_m = re.search(r'excerpt:\s*([^,]*),', post_text)
        tags_m = re.search(r'tags:\s*\[([^\]]*)\]', post_text)
        img_m = re.search(r'imagePlaceholder:\s*"([^"]*)"', post_text)
        
        # Extract content field (template literal)
        content_m = re.search(r'content:\s*`\n?(.*?)`,\s*\n?\s*\},?\s*', post_text, re.DOTALL)
        
        title = title_m.group(1) if title_m else ''
        date_val = date_m.group(1) if date_m else ''
        author = author_m.group(1) if author_m else ''
        excerpt = excerpt_m.group(1).strip().strip('"') if excerpt_m else ''
        tags_str = tags_m.group(1) if tags_m else ''
        tags = [t.strip().strip('"') for t in tags_str.split(',')] if tags_str.strip() else []
        img = img_m.group(1) if img_m else ''
        post_content = content_m.group(1) if content_m else ''
        
        posts.append({
            'slug': slug,
            'title': title,
            'date': date_val,
            'author': author,
            'excerpt': excerpt,
            'tags': tags,
            'imagePlaceholder': img,
            'content': post_content,
        })
    
    return posts


def has_bangla(text):
    """Check if text contains Bangla characters."""
    return bool(re.search(r'[\u0980-\u09FF]', text))


def check_tfidf(title, content, slug):
    """Check A: TF-IDF Coverage - count primary keyword in content."""
    title_lower = title.lower()
    content_lower = content.lower()
    
    # Strategy: extract the English topic from slug if title is Bangla
    # Slug format: "seo-X-bangladesh" where X is the topic
    slug_parts = slug.replace('seo-', '').replace('-bangladesh', '').replace('-bd', '').split('-')
    
    has_bangla_title = has_bangla(title)
    has_bangla_content = has_bangla(content)
    
    if has_bangla_title and not has_bangla_content:
        # Bangla title, English content - extract topic from slug
        primary_kw = ' '.join(slug_parts)
        count = content_lower.count(primary_kw)
        
        # Also try key terms from slug
        if count < 3:
            for term in ['seo mistakes', 'seo ' + slug_parts[0], slug_parts[0] + ' seo']:
                c = content_lower.count(term)
                if c > count:
                    primary_kw = term
                    count = c
        
        # Try the full slug
        if count < 3:
            primary_kw = slug.replace('-', ' ')
            count = content_lower.count(primary_kw)
    
    elif has_bangla_title:
        # Both title and content are Bangla
        # Extract the main Bangla topic words
        bangla_words = re.findall(r'[\u0980-\u09FF]+', title)
        
        # Try the first significant word (skip SEO, etc.)
        primary_kw = bangla_words[0] if bangla_words else title
        count = content.count(primary_kw)
        
        # Try 2-word combinations
        if count < 3 and len(bangla_words) >= 2:
            for start in range(len(bangla_words) - 1):
                kw = ''.join(bangla_words[start:start+2])
                c = content.count(kw)
                if c > count:
                    primary_kw = kw
                    count = c
        
        # Try the full title
        if count < 5:
            c = content.count(title)
            if c > count:
                primary_kw = title
                count = c
        
        # Try the excerpt keywords
        if count < 3:
            words = re.findall(r'[\u0980-\u09FF]+', content[:200])
            for w in words[:10]:
                c = content.count(w)
                if c > count:
                    primary_kw = w
                    count = c
    else:
        # English title, English content
        primary_kw = title_lower
        count = content_lower.count(primary_kw)
        
        if count < 3 and ':' in title:
            parts = title_lower.split(':')
            primary_kw = parts[-1].strip()
            count = content_lower.count(primary_kw)
        
        if count < 3:
            words = title_lower.split()[:4]
            primary_kw = ' '.join(words)
            count = content_lower.count(primary_kw)
    
    return {
        'keyword': primary_kw[:80],
        'count': count,
        'flag': count < 5
    }


def check_entities(title, content, tags):
    """Check B: Semantic Entity Coverage."""
    content_lower = content.lower()
    
    has_bangladesh = 'bangladesh' in content_lower or 'বাংলাদেশ' in content_lower
    has_dhaka = 'dhaka' in content_lower or 'ঢাকা' in content_lower
    
    service_terms = ['seo', 'digital marketing', 'web development', 'content marketing',
                     'social media', 'ppc', 'email marketing', 'consulting', 'audit',
                     'optimization', 'optimisation', 'web design']
    service_types_found = [t for t in service_terms if t in content_lower]
    
    industry_terms = ['e-commerce', 'ecommerce', 'retail', 'real estate', 'healthcare',
                      'education', 'travel', 'hospitality', 'manufacturing', 'garment',
                      'textile', 'it', 'technology', 'finance', 'banking', 'ngo',
                      'restaurant', 'food', 'fashion', 'startup', 'business',
                      'ই-কমার্স', 'ইকমার্স', 'শিক্ষা', 'স্বাস্থ্য', 'পর্যটন',
                      'ব্যবসা', 'প্রযুক্তি', 'আইটি']
    industries_found = [t for t in industry_terms if t in content_lower]
    
    missing = []
    if not has_bangladesh:
        missing.append('Bangladesh')
    if not has_dhaka:
        missing.append('Dhaka')
    if not service_types_found:
        missing.append('service_type')
    if not industries_found:
        missing.append('industry_sector')
    
    return {
        'bangladesh': has_bangladesh,
        'dhaka': has_dhaka,
        'service_types_found': list(set(service_types_found))[:5],
        'industries_found': list(set(industries_found))[:5],
        'missing': missing,
        'flag': len(missing) > 0
    }


def check_pillar_cluster(title, content, slug):
    """Check C: Pillar-Cluster Alignment."""
    services_links = len(re.findall(r'/services/', content))
    pillar_links = len(re.findall(r'/blog/complete-seo-guide-bangladesh-businesses-2026', content))
    internal_blog_links = len(re.findall(r'/blog/[a-z0-9\-]+', content))
    about_contact = len(re.findall(r'/(?:about|contact)', content))
    locations_links = len(re.findall(r'/locations/', content))
    
    total = services_links + pillar_links + internal_blog_links + about_contact + locations_links
    
    return {
        'services_links': services_links,
        'pillar_links': pillar_links,
        'internal_blog_links': internal_blog_links,
        'about_contact': about_contact,
        'locations_links': locations_links,
        'total_relevant_links': total,
        'flag': total == 0
    }


def check_aeo_geo(content):
    """Check D: AEO/GEO - question headings count.
    Supports both English and Bangla question words.
    """
    # English question words (at start of heading)
    en_qw = ['how', 'what', 'why', 'when', 'where', 'can', 'do', 'is', 'are',
             'which', 'who', 'should', 'would', 'could', 'will']
    
    # Bangla question words - use explicit boundary checks to avoid
    # false matches in compounds like 'কীওয়ার্ড' (keyword)
    bn_qw_patterns = [
        r'(?:^|\s)কী(?=\s|[।?!,;:\)"\']|$)',      # what
        r'(?:^|\s)কেন(?=\s|[।?!,;:\)"\']|$)',      # why
        r'(?:^|\s)কিভাবে(?=\s|[।?!,;:\)"\']|$)',   # how
        r'(?:^|\s)কীভাবে(?=\s|[।?!,;:\)"\']|$)',   # how
        r'(?:^|\s)কখন(?=\s|[।?!,;:\)"\']|$)',      # when
        r'(?:^|\s)কোথায়(?=\s|[।?!,;:\)"\']|$)',   # where
        r'(?:^|\s)কেনো(?=\s|[।?!,;:\)"\']|$)',     # why (alt)
        r'(?:^|\s)কোন(?=\s|[।?!,;:\)"\']|$)',      # which
        r'(?:^|\s)কারণ(?=\s|[।?!,;:\)"\']|$)',     # reason
        r'(?:^|\s)কি(?=\s|[।?!,;:\)"\']|$)',       # what (informal)
    ]
    
    heading_lines = re.findall(r'^#{2,3}\s+.*$', content, re.MULTILINE)
    
    question_headings = []
    for h in heading_lines:
        h_lower = h.lower()
        heading_text = re.sub(r'^#{2,3}\s+', '', h_lower)
        
        is_question = False
        
        # Check English question words at start of heading
        for qw in en_qw:
            if heading_text.startswith(qw + ' ') or heading_text.startswith(qw + '?') or heading_text.startswith(qw + ':'):
                is_question = True
                break
        
        # Check Bangla question words using word boundary regex
        if not is_question:
            for pattern in bn_qw_patterns:
                if re.search(pattern, heading_text):
                    is_question = True
                    break
        
        if is_question:
            question_headings.append(h.strip())
    
    return {
        'question_headings': question_headings,
        'count': len(question_headings),
        'flag': len(question_headings) < 2
    }


def check_internal_linking(content):
    """Check E: Internal Linking count."""
    blog_links = len(re.findall(r'/blog/', content))
    services_links = len(re.findall(r'/services/', content))
    locations_links = len(re.findall(r'/locations/', content))
    industries_links = len(re.findall(r'/industries/', content))
    about_links = len(re.findall(r'/about', content))
    contact_links = len(re.findall(r'/contact', content))
    
    total = blog_links + services_links + locations_links + industries_links + about_links + contact_links
    
    return {
        'blog_links': blog_links,
        'services_links': services_links,
        'locations_links': locations_links,
        'industries_links': industries_links,
        'about_contact_links': about_links + contact_links,
        'total': total,
        'flag': total < 3
    }


def check_schema(post):
    """Check F: Schema - title, excerpt, date fields present."""
    has_title = bool(post.get('title'))
    has_excerpt = bool(post.get('excerpt'))
    has_date = bool(post.get('date'))
    has_author = bool(post.get('author'))
    has_tags = bool(post.get('tags'))
    
    missing = []
    if not has_title:
        missing.append('title')
    if not has_excerpt:
        missing.append('excerpt')
    if not has_date:
        missing.append('date')
    
    return {
        'title': has_title,
        'excerpt': has_excerpt,
        'date': has_date,
        'author': has_author,
        'tags': has_tags,
        'missing': missing,
        'flag': len(missing) > 0
    }


def run_all_checks(post):
    title = post['title']
    content = post['content']
    tags = post['tags']
    slug = post['slug']
    
    a = check_tfidf(title, content, slug)
    b = check_entities(title, content, tags)
    c = check_pillar_cluster(title, content, slug)
    d = check_aeo_geo(content)
    e = check_internal_linking(content)
    f = check_schema(post)
    
    return {
        'slug': slug,
        'title': title,
        'A_TFIDF': a,
        'B_Entities': b,
        'C_PillarCluster': c,
        'D_AEO_GEO': d,
        'E_InternalLinks': e,
        'F_Schema': f,
    }


def print_results(results):
    for r in results:
        slug = r['slug']
        title = r['title']
        a = r['A_TFIDF']
        b = r['B_Entities']
        c = r['C_PillarCluster']
        d = r['D_AEO_GEO']
        e = r['E_InternalLinks']
        f = r['F_Schema']
        
        title_short = title[:60] if len(title) > 60 else title
        print(f"\n{'='*80}")
        print(f"📄 {slug}")
        print(f"   Title: {title_short}")
        print(f"{'='*80}")
        
        a_flag = "❌ FLAG" if a['flag'] else "✅ OK"
        print(f"\nA. TF-IDF Coverage: {a_flag}")
        print(f"   Primary keyword: \"{a['keyword']}\"")
        print(f"   Count in content: {a['count']} {'(< 5)' if a['flag'] else ''}")
        
        b_flag = "❌ FLAG" if b['flag'] else "✅ OK"
        print(f"\nB. Semantic Entities: {b_flag}")
        print(f"   Bangladesh: {'✅' if b['bangladesh'] else '❌'} | Dhaka: {'✅' if b['dhaka'] else '❌'}")
        print(f"   Service types: {b['service_types_found'][:3]}")
        print(f"   Industries: {b['industries_found'][:3]}")
        if b['missing']:
            print(f"   MISSING: {', '.join(b['missing'])}")
        
        c_flag = "❌ FLAG" if c['flag'] else "✅ OK"
        print(f"\nC. Pillar-Cluster: {c_flag}")
        print(f"   Services: {c['services_links']} | Pillar: {c['pillar_links']} | Blog: {c['internal_blog_links']} | About/Contact: {c['about_contact']}")
        print(f"   Total relevant links: {c['total_relevant_links']}")
        
        d_flag = "❌ FLAG" if d['flag'] else "✅ OK"
        print(f"\nD. AEO/GEO Questions: {d_flag}")
        print(f"   Question headings count: {d['count']} {'(< 2)' if d['flag'] else ''}")
        if d['question_headings']:
            for q in d['question_headings'][:5]:
                print(f"     - {q}")
        
        e_flag = "❌ FLAG" if e['flag'] else "✅ OK"
        print(f"\nE. Internal Links: {e_flag}")
        print(f"   /blog/: {e['blog_links']} | /services/: {e['services_links']} | /locations/: {e['locations_links']} | /industries/: {e['industries_links']} | /about+/contact: {e['about_contact_links']}")
        print(f"   Total: {e['total']} {'(< 3)' if e['flag'] else ''}")
        
        f_flag = "❌ FLAG" if f['flag'] else "✅ OK"
        print(f"\nF. Schema Fields: {f_flag}")
        print(f"   title: {'✅' if f['title'] else '❌'} | excerpt: {'✅' if f['excerpt'] else '❌'} | date: {'✅' if f['date'] else '❌'} | author: {'✅' if f['author'] else '❌'} | tags: {'✅' if f['tags'] else '❌'}")
        if f['missing']:
            print(f"   MISSING: {', '.join(f['missing'])}")
    
    # Summary table
    print(f"\n\n{'='*110}")
    print("SUMMARY TABLE - Batch 7 Content Framework Checks")
    print(f"{'='*110}")
    print(f"{'Post':<48} {'A':>4} {'B':>4} {'C':>4} {'D':>4} {'E':>4} {'F':>4} {'Flags':>8}")
    print("-" * 110)
    
    total_flags = 0
    post_flags = {}
    for r in results:
        slug = r['slug']
        flags = []
        if r['A_TFIDF']['flag']: flags.append('A')
        if r['B_Entities']['flag']: flags.append('B')
        if r['C_PillarCluster']['flag']: flags.append('C')
        if r['D_AEO_GEO']['flag']: flags.append('D')
        if r['E_InternalLinks']['flag']: flags.append('E')
        if r['F_Schema']['flag']: flags.append('F')
        
        flag_str = ','.join(flags) if flags else 'none'
        a_mark = '❌' if r['A_TFIDF']['flag'] else '✅'
        b_mark = '❌' if r['B_Entities']['flag'] else '✅'
        c_mark = '❌' if r['C_PillarCluster']['flag'] else '✅'
        d_mark = '❌' if r['D_AEO_GEO']['flag'] else '✅'
        e_mark = '❌' if r['E_InternalLinks']['flag'] else '✅'
        f_mark = '❌' if r['F_Schema']['flag'] else '✅'
        
        print(f"{slug:<48} {a_mark:>4} {b_mark:>4} {c_mark:>4} {d_mark:>4} {e_mark:>4} {f_mark:>4} {flag_str:>8}")
        total_flags += len(flags)
        post_flags[slug] = len(flags)
    
    print("-" * 110)
    print(f"\nTotal posts checked: {len(results)}")
    print(f"Total flags raised: {total_flags}")
    print(f"Average flags per post: {total_flags/len(results):.1f}")
    
    print(f"\nPosts with flags:")
    for slug, count in sorted(post_flags.items(), key=lambda x: -x[1]):
        if count > 0:
            print(f"  ⚠ {slug}: {count} flag(s)")
    
    print(f"\nFlags per check type:")
    a_count = sum(1 for r in results if r['A_TFIDF']['flag'])
    b_count = sum(1 for r in results if r['B_Entities']['flag'])
    c_count = sum(1 for r in results if r['C_PillarCluster']['flag'])
    d_count = sum(1 for r in results if r['D_AEO_GEO']['flag'])
    e_count = sum(1 for r in results if r['E_InternalLinks']['flag'])
    f_count = sum(1 for r in results if r['F_Schema']['flag'])
    print(f"  A (TF-IDF < 5):         {a_count:>2}/{len(results)}")
    print(f"  B (Missing entities):   {b_count:>2}/{len(results)}")
    print(f"  C (No pillar link):     {c_count:>2}/{len(results)}")
    print(f"  D (Questions < 2):      {d_count:>2}/{len(results)}")
    print(f"  E (Internal links < 3): {e_count:>2}/{len(results)}")
    print(f"  F (Missing schema):     {f_count:>2}/{len(results)}")


def main():
    print("Reading data.js...")
    content = read_file_to_string(DATA_FILE)
    print(f"Read {len(content)} characters ({len(content.splitlines())} lines)")
    
    print("\nExtracting posts...")
    all_posts = extract_posts(content)
    print(f"Found {len(all_posts)} total posts")
    
    batch7_posts = [p for p in all_posts if p['slug'] in BATCH7_SLUGS]
    print(f"Batch 7 posts found: {len(batch7_posts)}")
    
    if len(batch7_posts) != 20:
        found_slugs = [p['slug'] for p in batch7_posts]
        missing = [s for s in BATCH7_SLUGS if s not in found_slugs]
        print(f"WARNING: Missing {len(missing)} posts: {missing}")
    
    print("\nRunning checks...")
    results = []
    for post in batch7_posts:
        result = run_all_checks(post)
        results.append(result)
    
    print_results(results)


if __name__ == '__main__':
    main()
