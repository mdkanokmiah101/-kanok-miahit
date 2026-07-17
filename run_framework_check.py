#!/usr/bin/env python3
"""
Content Framework Enforcer for kanokmiah.com.bd - Full check
Runs all 6 framework checks on every blog post.
"""
import re, sys
from collections import Counter

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
    """Extract a simple quoted string field from a post"""
    m = re.search(rf'{field}:\s*"([^"]+)"', post)
    return m.group(1) if m else ''

def extract_content(post):
    """Extract the content (backtick string) from a post"""
    m = re.search(r'content:\s*`(.*)`', post, re.DOTALL)
    return m.group(1) if m else ''

def extract_all_fields(post):
    slug = extract_field(post, 'slug')
    title = extract_field(post, 'title')
    date = extract_field(post, 'date')
    author = extract_field(post, 'author')
    excerpt = extract_field(post, 'excerpt')
    content = extract_content(post)
    
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
        'content': content or '',
    }

def is_bengali(text):
    """Check if text contains Bengali characters"""
    bengali_count = len(re.findall(r'[\u0980-\u09FF]', text))
    return bengali_count > len(text) * 0.1

def count_keyword_occurrences(content, keyword):
    """Count occurrences of a keyword in content (case-insensitive)"""
    if not keyword:
        return 0
    return len(re.findall(re.escape(keyword), content, re.IGNORECASE))

def check_tfidf(title, content):
    """Check A: TF-IDF keyword coverage"""
    # Extract first meaningful noun phrase from title
    # For English: first meaningful word (skip stopwords like 'The', 'A', 'How', 'Why', 'What', 'Is', 'Are')
    # For Bengali: first meaningful noun phrase
    
    # Simple strategy: use the first 2-3 meaningful words from the title
    stopwords = {'a', 'an', 'the', 'how', 'why', 'what', 'when', 'where', 'which', 'who', 'do', 'does', 'did',
                 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'to', 'for', 'of', 'in',
                 'on', 'at', 'by', 'with', 'from', 'as', 'into', 'through', 'during', 'before', 'after', 'above',
                 'below', 'between', 'out', 'off', 'over', 'under', 'again', 'further', 'then', 'once',
                 'and', 'but', 'or', 'nor', 'not', 'so', 'yet', 'both', 'either', 'neither', 'each', 'every',
                 'your', 'their', 'its', 'our', 'my', 'his', 'her', 'some', 'any', 'no', 'all', 'most',
                 'best', 'top', 'ultimate', 'complete', 'guide', 'tips', 'for', 'in', 'of', 'the'}
    
    title_lower = title.lower()
    words = re.findall(r'[a-zA-Z\u0980-\u09FF]+', title_lower)
    
    # Filter stopwords and take first 2 meaningful words
    meaningful = [w for w in words if w not in stopwords and len(w) > 2]
    
    if is_bengali(title):
        # For Bengali, use the first noun phrase (first 2-3 significant words)
        keyword = ' '.join(meaningful[:3]) if meaningful else title_lower
    else:
        # For English, use primary keyword = first 2 meaningful words
        keyword = ' '.join(meaningful[:2]) if meaningful else title_lower
    
    count = count_keyword_occurrences(content, keyword)
    passed = count >= 5
    
    return {
        'keyword': keyword,
        'occurrences': count,
        'passed': passed,
        'detail': f'{count} occurrences'
    }

def check_entities(title, content, tags):
    """Check B: Semantic Entity Coverage"""
    # Entities to check
    entities = {
        'location_dhaka': r'dhaka|ঢাকা',
        'location_bangladesh': r'bangladesh|বাংলাদেশ',
        'service_seo': r'seo|এসইও',
    }
    
    # Add specific entities based on tags
    all_tags = ','.join(tags).lower()
    if any(t in all_tags for t in ['ecommerce', 'e-commerce', 'daraz', 'shopify', 'ই-কমার্স', 'দারাজ']):
        entities['entity_ecommerce'] = r'ecommerce|e-commerce|ই-কমার্স|দারাজ|shopify|শপিফাই'
    if any('real' in t and 'estate' in t for t in tags):
        entities['entity_realestate'] = r'real estate|রিয়েল এস্টেট|property|প্রপার্টি'
    if any(t in all_tags for t in ['local', 'google maps', 'gbp', 'লোকাল']):
        entities['entity_gbp'] = r'google business|gpb|গুগল বিজনেস|গুগল ম্যাপ'
    
    content_lower = content.lower()
    missing = []
    
    for name, pattern in entities.items():
        if not re.search(pattern, content_lower):
            missing.append(name)
    
    passed = len(missing) == 0
    return {
        'passed': passed,
        'missing': missing,
        'detail': f"Missing: {', '.join(missing) if missing else 'none'}"
    }

def check_pillar_link(title, content, tags, slug):
    """Check C: Pillar-Cluster Alignment"""
    # Based on tags, determine pillar topic
    all_tags = ','.join(tags).lower()
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
    
    # Find matching pillar
    linked_pillar = None
    for pillar_key, pillar_url in pillar_pages.items():
        if pillar_key in all_tags or pillar_key.replace(' ', '') in all_tags:
            if pillar_url in content:
                linked_pillar = pillar_url
                break
    
    # Also check if any pillar link exists at all
    if not linked_pillar:
        for pillar_url in pillar_pages.values():
            if pillar_url in content:
                linked_pillar = '(exists: ' + pillar_url + ')'
                break
    
    passed = linked_pillar is not None
    
    # Also check for the pillar page slug being referenced
    if is_bengali(title):
        # For Bengali posts, check if any internal links exist
        internal_links = re.findall(r'/blog/[a-z0-9-]+', content)
        passed = passed or len(internal_links) > 0
    
    return {
        'passed': passed,
        'pillar': linked_pillar or 'none found',
        'detail': f"Links to: {linked_pillar if linked_pillar else 'NO pillar link found'}"
    }

def check_aeo_geo(title, content):
    """Check D: AEO/GEO Optimization - count question headings"""
    content_clean = content  # Keep as-is
    
    # Count question-based headings (starting with How, What, Why, When, Where, Can, Do, Is, Are)
    # Also count Bengali question words
    question_patterns = [
        r'^##\s+(How\s|What\s|Why\s|When\s|Where\s|Can\s|Do\s|Is\s|Are\s|Does\s|Which\s|Who\s)',
        r'^###\s+(How\s|What\s|Why\s|When\s|Where\s|Can\s|Do\s|Is\s|Are\s|Does\s|Which\s|Who\s)',
        # Bengali question words
        r'^##\s+.*(?:কী|কেন|কিভাবে|কখন|কোথায়|কীভাবে|কোন|কার|কয়টি)',
        r'^###\s+.*(?:কী|কেন|কিভাবে|কখন|কোথায়|কীভাবে|কোন|কার|কয়টি)',
    ]
    
    # Also count FAQ sections and question marks in headings
    faq_section = len(re.findall(r'প্রায়শ[িই] জিজ্ঞাসিত|FAQ|প্রশ্ন', content, re.IGNORECASE))
    
    question_headings = 0
    for pattern in question_patterns:
        question_headings += len(re.findall(pattern, content, re.MULTILINE))
    
    # Also count any heading ending with ?
    question_headings += len(re.findall(r'^#{2,3}\s+.*\?', content, re.MULTILINE))
    
    # Count total AEO-friendly sections
    total_aeo = question_headings + faq_section
    
    passed = total_aeo >= 2
    return {
        'passed': passed,
        'question_headings': total_aeo,
        'faq_sections': faq_section,
        'detail': f'{total_aeo} AEO elements ({question_headings} question headings, {faq_section} FAQ sections)'
    }

def check_internal_links(content):
    """Check E: Internal Linking"""
    # Count internal links to other posts (/blog/...), services (/services/...), locations
    blog_links = re.findall(r'/blog/[a-z0-9-]+', content)
    service_links = re.findall(r'/services/[a-z0-9-]+', content)
    industry_links = re.findall(r'/industries/[a-z0-9-]+', content)
    other_links = re.findall(r'\b/about\b|\b/contact\b|\b/\b', content)
    
    # Deduplicate
    total_links = len(set(blog_links + service_links + industry_links))
    
    passed = total_links >= 3
    return {
        'passed': passed,
        'total': total_links,
        'blog_links': len(set(blog_links)),
        'service_links': len(set(service_links)),
        'detail': f'{total_links} internal links ({len(set(blog_links))} blog, {len(set(service_links))} service, {len(set(industry_links))} industry)'
    }

def check_schema(post_data):
    """Check F: Schema Readiness"""
    slug = post_data['slug']
    title = post_data['title']
    date = post_data['date']
    excerpt = post_data['excerpt']
    author = post_data['author']
    content = post_data['content']
    
    missing = []
    if not title or title == 'unknown':
        missing.append('title')
    if not excerpt:
        missing.append('excerpt')
    if not date:
        missing.append('date')
    if not author:
        missing.append('author')
    if not content or len(content) < 50:
        missing.append('content')
    
    passed = len(missing) == 0
    return {
        'passed': passed,
        'missing': missing,
        'detail': f"Missing: {', '.join(missing) if missing else 'all fields set'}"
    }

# Run checks on all posts
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
        'language': 'BN' if is_bengali(post['title']) else 'EN',
        'checks': {
            'tfidf': tfidf,
            'entities': entities,
            'pillar': pillar,
            'aeo': aeo,
            'links': links,
            'schema': schema,
        }
    })
    
    if (idx + 1) % 20 == 0:
        print(f"  Progress: {idx+1}/{len(posts)}", file=sys.stderr)

# Generate report
print("=" * 120)
print("CONTENT FRAMEWORK ENFORCEMENT REPORT - kanokmiah.com.bd")
print(f"Date: July 17, 2026 | Total posts checked: {len(results)}")
print("=" * 120)

# Summary stats
check_names = {'tfidf': 'TF-IDF', 'entities': 'Entities', 'pillar': 'Pillar Link', 
               'aeo': 'AEO/GEO', 'links': 'Internal Links', 'schema': 'Schema'}
summary = {k: {'passed': 0, 'failed': 0} for k in check_names}

all_passed = 0
for r in results:
    passed_all = all(v['passed'] for v in r['checks'].values())
    if passed_all:
        all_passed += 1
    for k, v in r['checks'].items():
        if v['passed']:
            summary[k]['passed'] += 1
        else:
            summary[k]['failed'] += 1

print(f"\n## GLOBAL SUMMARY: {all_passed}/{len(results)} posts passed all checks")
print(f"   Failed: {len(results) - all_passed}/{len(results)} posts have at least one issue")
print()
for k, v in summary.items():
    name = check_names[k]
    total = v['passed'] + v['failed']
    print(f"   {name:20s}: {v['passed']:3d}/{total:3d} passed ({v['failed']:3d} failed)")

print(f"\n{'='*120}")
print("## POST-BY-POST RESULTS")
print(f"{'='*120}\n")

# List failed posts first
failed_results = [r for r in results if not all(v['passed'] for v in r['checks'].values())]
passed_results = [r for r in results if all(v['passed'] for v in r['checks'].values())]

print(f"### FAILED POSTS ({len(failed_results)})")
print()

for r in failed_results:
    c = r['checks']
    print(f"## Post: {r['slug']}  [{r['language']}]")
    print(f"   Title: {r['title']}")
    print(f"| {'Check':15s} | {'Status':8s} | Details")
    print(f"|{'-'*15}|{'-'*9}|{'-'*50}")
    for k, v in c.items():
        name = check_names[k]
        status = '✅ PASS' if v['passed'] else '❌ FAIL'
        print(f"| {name:15s} | {status:8s} | {v['detail'][:70]}")
    
    # Fix instructions
    fix_lines = []
    if not c['tfidf']['passed']:
        fix_lines.append(f"- Increase '{c['tfidf']['keyword']}' occurrences to ≥5 (currently {c['tfidf']['occurrences']})")
    if not c['entities']['passed']:
        for m in c['entities']['missing']:
            fix_lines.append(f"- Add entity: {m} in content")
    if not c['pillar']['passed']:
        fix_lines.append(f"- Add link to pillar content page")
    if not c['aeo']['passed']:
        fix_lines.append(f"- Add more question-based headings (How/What/Why) — currently {c['aeo']['question_headings']}")
    if not c['links']['passed']:
        fix_lines.append(f"- Add more internal links — currently {c['links']['total']} (need ≥3)")
    if not c['schema']['passed']:
        for m in c['schema']['missing']:
            fix_lines.append(f"- Set missing schema field: {m}")
    
    print(f"\n### Fix instructions:")
    for fix in fix_lines:
        print(fix)
    print()

print(f"\n### PASSED POSTS ({len(passed_results)})")
print(f"All 6 checks passed for {len(passed_results)} posts")
for r in passed_results:
    print(f"  ✅ {r['slug']}  [{r['language']}]")

# Write full report to file
import datetime
report_text = f"""CONTENT FRAMEWORK ENFORCEMENT REPORT - kanokmiah.com.bd
=========================================================
Date: July 17, 2026 | Total posts checked: {len(results)} | All passed: {all_passed}/{len(results)}

GLOBAL SUMMARY:

  TF-IDF Coverage:     {summary['tfidf']['passed']}/{summary['tfidf']['passed'] + summary['tfidf']['failed']} passed
  Entity Coverage:     {summary['entities']['passed']}/{summary['entities']['passed'] + summary['entities']['failed']} passed
  Pillar Link:         {summary['pillar']['passed']}/{summary['pillar']['passed'] + summary['pillar']['failed']} passed
  AEO/GEO:             {summary['aeo']['passed']}/{summary['aeo']['passed'] + summary['aeo']['failed']} passed
  Internal Links:      {summary['links']['passed']}/{summary['links']['passed'] + summary['links']['failed']} passed
  Schema Ready:        {summary['schema']['passed']}/{summary['schema']['passed'] + summary['schema']['failed']} passed

FAILED POSTS ({len(failed_results)}):
"""
for r in failed_results:
    report_text += f"\n## {r['slug']} [{r['language']}]\n"
    for k, v in r['checks'].items():
        name = check_names[k]
        status = 'PASS' if v['passed'] else 'FAIL'
        report_text += f"  {name}: {status} | {v['detail']}\n"

with open('framework_report.txt', 'w') as f:
    f.write(report_text)

print(f"\nFull report written to framework_report.txt", file=sys.stderr)
