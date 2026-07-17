#!/usr/bin/env python3
"""
Content Framework Enforcer for kanokmiah.com.bd - v2
Fixed TF-IDF check - counts individual keyword word occurrences instead of exact phrase.
"""
import re, sys

with open('src/app/blog/data.js', 'r') as f:
    lines = f.readlines()

# Parse all posts
posts = []
i = 0
while i < len(lines):
    stripped = lines[i].strip()
    if stripped == '{':
        j = i + 1
        found_slug = False
        depth = 1
        in_content = False
        while j < len(lines) and depth > 0:
            l = lines[j]
            if 'slug:' in l and not in_content:
                found_slug = True
            if 'content: `' in l or 'content:`' in l or l.strip().startswith('content:'):
                in_content = True
            if in_content:
                if '`' in l and not l.strip().startswith('content:'):
                    backtick_count = l.count('`')
                    if backtick_count % 2 == 1:
                        in_content = False
            else:
                depth += l.count('{') - l.count('}')
            j += 1
        if found_slug:
            posts.append(''.join(lines[i:j]))
            i = j
            continue
    i += 1

print(f"Total posts: {len(posts)}", file=sys.stderr)

def extract_field(post, field):
    m = re.search(rf'{field}:\s*"([^"]+)"', post)
    return m.group(1) if m else ''

def extract_content(post):
    m = re.search(r'content:\s*`(.*)`', post, re.DOTALL)
    return m.group(1) if m else ''

def extract_all_fields(post):
    slug = extract_field(post, 'slug')
    title = extract_field(post, 'title')
    date = extract_field(post, 'date')
    author = extract_field(post, 'author')
    excerpt = extract_field(post, 'excerpt')
    content_content = extract_content(post)
    
    tags_m = re.search(r'tags:\s*\[([^\]]+)\]', post, re.DOTALL)
    tags = []
    if tags_m:
        tags = re.findall(r'"([^"]+)"', tags_m.group(1))
    
    return {
        'slug': slug or 'unknown',
        'title': title or 'unknown',
        'date': date or '',
        'author': author or '',
        'excerpt': excerpt or '',
        'tags': tags,
        'content': content_content or '',
    }

def is_bengali(text):
    return len(re.findall(r'[\u0980-\u09FF]', text)) > len(text) * 0.1

def extract_primary_keyword(title):
    """Extract a meaningful primary keyword from the title."""
    # Split title into words
    title_lower = title.lower()
    
    stopwords = {'a', 'an', 'the', 'how', 'why', 'what', 'when', 'where', 'which', 'who', 'do', 'does', 'did',
                 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'to', 'for', 'of', 'in',
                 'on', 'at', 'by', 'with', 'from', 'as', 'into', 'through', 'during', 'before', 'after', 'above',
                 'below', 'between', 'out', 'off', 'over', 'under', 'again', 'further', 'then', 'once',
                 'and', 'but', 'or', 'nor', 'not', 'so', 'yet', 'both', 'either', 'neither', 'each', 'every',
                 'your', 'their', 'its', 'our', 'my', 'his', 'her', 'some', 'any', 'no', 'all', 'most',
                 'best', 'top', 'ultimate', 'complete', 'guide', 'tips', 'for', 'in', 'of', 'the', 'on', 'at',
                 'seo', 'also', 'just', 'more', 'than', 'very', 'too', 'can', 'has', 'get', 'got'}
    
    # Extract meaningful words (non-stopword, length > 2)
    # Split on various separators
    raw_words = re.split(r'[\s:;,()!?./\\[\]"\'\-]+', title_lower)
    meaningful = [w for w in raw_words if w not in stopwords and len(w) > 2]
    
    if not meaningful:
        # Fallback: use first non-stopword
        raw_words = re.split(r'[\s:;,()!?./\\[\]"\'\-]+', title_lower)
        meaningful = [w for w in raw_words if w not in {'a', 'an', 'the', 'for', 'in', 'of', 'to', 'and', 'or', 'at'} and len(w) > 1]
    
    if not meaningful:
        return title_lower.split()[0] if title_lower.split() else title_lower
    
    # Use the first meaningful word as primary keyword (most specific to the topic)
    # For Bengali content, first meaningful Bengali word often signals the topic
    if is_bengali(title):
        # Find first Bengali meaningful word
        for w in meaningful:
            if re.search(r'[\u0980-\u09FF]', w):
                return w
        return meaningful[0]
    else:
        return meaningful[0]

def check_tfidf(title, content):
    """Check A: TF-IDF keyword coverage - count primary keyword occurrences."""
    keyword = extract_primary_keyword(title)
    
    if not keyword:
        return {'keyword': title[:30], 'occurrences': 0, 'passed': False, 'detail': 'Could not extract keyword'}
    
    # Count occurrences of the keyword as a whole word
    # Use word boundary for Latin text, no boundary for Bengali
    if re.search(r'[\u0980-\u09FF]', keyword):
        # Bengali: just count literal occurrences
        count = len(re.findall(re.escape(keyword), content, re.IGNORECASE))
    else:
        # English: count with word boundaries
        count = len(re.findall(r'\b' + re.escape(keyword) + r'\b', content, re.IGNORECASE))
    
    passed = count >= 5
    return {
        'keyword': keyword,
        'occurrences': count,
        'passed': passed,
        'detail': f'{count} occurrences of "{keyword}"'
    }

def check_entities(title, content, tags):
    """Check B: Semantic Entity Coverage"""
    entities = {
        'location_dhaka': r'dhaka|ঢাকা',
        'location_bangladesh': r'bangladesh|বাংলাদেশ',
        'service_seo': r'SEO|এসইও',
    }
    
    all_tags = ','.join(tags).lower()
    if any(t in all_tags for t in ['ecommerce', 'e-commerce', 'daraz', 'shopify', 'ই-কমার্স']):
        entities['entity_ecommerce'] = r'ecommerce|e.commerce|ই-কমার্স|দারাজ'
    if any(t in all_tags for t in ['real estate']):
        entities['entity_realestate'] = r'real estate|রিয়েল এস্টেট|property'
    if any(t in all_tags for t in ['local seo', 'google maps', 'gbp', 'লোকাল']):
        entities['entity_gbp'] = r'google business|gpb|গুগল বিজনেস|গুগল ম্যাপ'
    if any(t in all_tags for t in ['technical seo', 'core web vitals', 'টেকনিক্যাল']):
        entities['entity_technical'] = r'technical seo|core web vitals|টেকনিক্যাল|ক্রল'
    if any(t in all_tags for t in ['keyword', 'কীওয়ার্ড']):
        entities['entity_keyword'] = r'keyword|কীওয়ার্ড|কীওয়ার্ড|লং.*টেল'
    if any(t in all_tags for t in ['video', 'youtube', 'ইউটিউব']):
        entities['entity_youtube'] = r'youtube|ইউটিউব|video|ভিডিও'
    if any(t in all_tags for t in ['mobile', 'মোবাইল']):
        entities['entity_mobile'] = r'mobile|মোবাইল|smartphone'
    if any(t in all_tags for t in ['schema', 'স্কিমা']):
        entities['entity_schema'] = r'schema|স্কিমা|structured data|স্ট্রাকচারড ডেটা'
    if any(t in all_tags for t in ['content', 'কন্টেন্ট', 'blog']):
        entities['entity_content'] = r'content|কন্টেন্ট|blog|ব্লগ'
    
    content_lower = content.lower()
    missing = []
    
    for name, pattern in entities.items():
        if not re.search(pattern, content_lower, re.IGNORECASE):
            missing.append(name)
    
    passed = len(missing) == 0
    return {
        'passed': passed,
        'missing': missing,
        'detail': f"Missing: {', '.join(missing) if missing else 'none'}"
    }

def check_pillar_link(title, content, tags, slug):
    """Check C: Pillar-Cluster Alignment"""
    pillar_pages = {
        'seo guide': '/blog/complete-seo-guide-bangladesh-businesses-2026',
        'local seo': '/blog/local-seo-tips-dhaka-businesses-google-maps',
        'technical seo': '/blog/technical-seo-checklist-bangladeshi-websites',
        'ecommerce': '/blog/why-ecommerce-store-needs-seo-bangladesh',
        'keyword': '/blog/keyword-research-bangladesh-market',
        'link building': '/blog/link-building-strategies-bangladesh-market',
        'geo': '/blog/geo-optimization-prepare-business-ai-search',
        'content': '/blog/content-marketing-seo-friendly-content-writing',
        'mobile': '/blog/mobile-seo-bangladesh-ranking-strategy',
        'schema': '/blog/schema-markup-rich-snippets-techniques',
    }
    
    all_tags = ','.join(tags).lower()
    linked_pillar = None
    
    # Check if any pillar URL is linked in the content
    for pillar_url in pillar_pages.values():
        if pillar_url in content:
            linked_pillar = pillar_url
            break
    
    passed = linked_pillar is not None
    
    # For industry-specific posts, also check blog internal links
    if not passed:
        blog_links = re.findall(r'/blog/[a-z0-9-]+', content)
        if blog_links:
            linked_pillar = '(exists: ' + blog_links[0] + ')'
            passed = True
    
    return {
        'passed': passed,
        'pillar': linked_pillar or 'none found',
        'detail': f"Links to: {linked_pillar if linked_pillar else 'NO pillar link found'}"
    }

def check_aeo_geo(title, content):
    """Check D: AEO/GEO Optimization"""
    # Count question-based headings
    question_headings = len(re.findall(r'^#{2,3}\s+.*\?', content, re.MULTILINE))
    
    # Count headings starting with question words (English)
    q_words = r'^(?:How|What|Why|When|Where|Can|Do|Is|Are|Does|Which|Who)'
    question_headings += len(re.findall(r'^#{2,3}\s+' + q_words, content, re.MULTILINE))
    
    # Count headings with Bengali question words
    question_headings += len(re.findall(r'^#{2,3}\s+.*?(?:কী|কেন|কিভাবে|কখন|কোথায়|কীভাবে|কোন|কার|কয়টি|উপসংহার|বনাম)', 
                                        content, re.MULTILINE))
    
    # Count FAQ sections
    faq_sections = len(re.findall(r'প্রায়শ[িই] জিজ্ঞাসিত|FAQ|প্রশ্ন', content, re.IGNORECASE))
    
    total = question_headings + faq_sections
    passed = total >= 2
    
    return {
        'passed': passed,
        'question_headings': question_headings,
        'faq_sections': faq_sections,
        'detail': f'{total} AEO elements ({question_headings} question headings, {faq_sections} FAQ sections)'
    }

def check_internal_links(content):
    """Check E: Internal Linking"""
    blog_links = set(re.findall(r'/blog/[a-z0-9-]+', content))
    service_links = set(re.findall(r'/services/[a-z0-9-]+', content))
    industry_links = set(re.findall(r'/industries/[a-z0-9-]+', content))
    
    total_links = len(blog_links) + len(service_links) + len(industry_links)
    
    passed = total_links >= 3
    return {
        'passed': passed,
        'total': total_links,
        'blog_links': len(blog_links),
        'service_links': len(service_links),
        'detail': f'{total_links} internal links ({len(blog_links)} blog, {len(service_links)} service, {len(industry_links)} industry)'
    }

def check_schema(post_data):
    """Check F: Schema Readiness"""
    missing = []
    if not post_data['title'] or post_data['title'] == 'unknown':
        missing.append('title')
    if not post_data['excerpt']:
        missing.append('excerpt')
    if not post_data['date']:
        missing.append('date')
    if not post_data['author']:
        missing.append('author')
    if not post_data['content'] or len(post_data['content']) < 50:
        missing.append('content')
    
    passed = len(missing) == 0
    return {
        'passed': passed,
        'missing': missing,
        'detail': f"Missing: {', '.join(missing) if missing else 'all fields set'}"
    }

# Run checks
results = []
for idx, post_text in enumerate(posts):
    post = extract_all_fields(post_text)
    
    tfidf = check_tfidf(post['title'], post['content'])
    entities = check_entities(post['title'], post['content'], post['tags'])
    pillar = check_pillar_link(post['title'], post['content'], post['tags'], post['slug'])
    aeo = check_aeo_geo(post['title'], post['content'])
    links = check_internal_links(post['content'])
    schema = check_schema(post)
    
    results.append({
        'slug': post['slug'],
        'title': post['title'][:60],
        'lang': 'BN' if is_bengali(post['title']) else 'EN',
        'checks': {
            'TF-IDF': tfidf,
            'Entities': entities,
            'Pillar Link': pillar,
            'AEO/GEO': aeo,
            'Int. Links': links,
            'Schema': schema,
        }
    })
    
    if (idx + 1) % 20 == 0:
        print(f"  {idx+1}/{len(posts)}", file=sys.stderr)

# Print summary
all_passed = sum(1 for r in results if all(v['passed'] for v in r['checks'].values()))
check_stats = {}
for r in results:
    for k, v in r['checks'].items():
        if k not in check_stats:
            check_stats[k] = {'passed': 0, 'failed': 0}
        if v['passed']:
            check_stats[k]['passed'] += 1
        else:
            check_stats[k]['failed'] += 1

print("=" * 90)
print("CONTENT FRAMEWORK ENFORCEMENT REPORT - kanokmiah.com.bd")
print(f"Date: July 17, 2026 | Posts: {len(results)} | All passed: {all_passed}/{len(results)}")
print("=" * 90)

print("\n## GLOBAL SUMMARY")
for k, v in check_stats.items():
    pct = v['passed'] / (v['passed'] + v['failed']) * 100
    bar = '█' * int(pct / 5) + '░' * (20 - int(pct / 5))
    print(f"  {k:15s} {bar} {v['passed']:3d}/{v['passed']+v['failed']:3d} ({pct:.0f}%)")

# Failed posts
failed = [r for r in results if not all(v['passed'] for v in r['checks'].values())]
pass_ok = [r for r in results if all(v['passed'] for v in r['checks'].values())]

print(f"\n## ❌ FAILED POSTS ({len(failed)}):")
for r in failed:
    c = r['checks']
    fails = [k for k, v in c.items() if not v['passed']]
    print(f"\n### {r['slug']}  [{r['lang']}]")
    print(f"Title: {r['title']}")
    print(f"Fails on: {', '.join(fails)}")
    for k in fails:
        v = c[k]
        print(f"  - {k}: {v['detail']}")
    
    print("  Fixes:")
    for k in fails:
        v = c[k]
        if k == 'TF-IDF':
            print(f"    ✓ Add \"{v['keyword']}\" more times (currently {v['occurrence'] if 'occurrence' in v else v['occurrences']}, need ≥5)")
        elif k == 'Entities':
            for m in v['missing']:
                print(f"    ✓ Add entity: {m}")
        elif k == 'Pillar Link':
            print(f"    ✓ Add link to pillar content page")
        elif k == 'AEO/GEO':
            print(f"    ✓ Add question-based headings (currently {v.get('question_headings', 0)} total AEO elements)")
        elif k == 'Int. Links':
            print(f"    ✓ Add more internal links (currently {v.get('total', 0)}, need ≥3)")
        elif k == 'Schema':
            for m in v['missing']:
                print(f"    ✓ Set field: {m}")

print(f"\n## ✅ PASSED POSTS ({len(pass_ok)}):")
for r in pass_ok:
    print(f"  ✓ {r['slug']}  [{r['lang']}]")

# Write detailed report
with open('framework_report_v2.txt', 'w') as f:
    f.write("CONTENT FRAMEWORK ENFORCEMENT REPORT v2\n")
    f.write(f"Posts: {len(results)} | All passed: {all_passed}/{len(results)}\n\n")
    for r in results:
        f.write(f"{'✅' if all(v['passed'] for v in r['checks'].values()) else '❌'} {r['slug']} [{r['lang']}]\n")
        for k, v in r['checks'].items():
            f.write(f"  {k}: {'PASS' if v['passed'] else 'FAIL'} | {v['detail']}\n")

print(f"\nDetailed report: framework_report_v2.txt", file=sys.stderr)
