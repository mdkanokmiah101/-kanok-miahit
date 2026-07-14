#!/usr/bin/env python3
"""
Content Framework Enforcer v2 — handles Bengali content properly
"""
import re
import sys

with open('src/app/blog/data.js', 'r') as f:
    FILE_CONTENT = f.read()
LINES = FILE_CONTENT.split('\n')

def extract_post_by_slug(slug):
    """Extract post object using line-by-line brace tracking"""
    # Find the post slug definition
    start_line = None
    for i, line in enumerate(LINES):
        stripped = line.strip()
        if stripped.startswith('slug:') and f'"{slug}"' in stripped:
            start_line = i
            break
    
    if start_line is None:
        return None
    
    # Find the opening brace of this post object
    post_start = None
    for i in range(start_line, -1, -1):
        if '{' in LINES[i]:
            stripped = LINES[i].strip()
            if stripped == 'const posts = [':
                continue
            post_start = i
            break
    
    if post_start is None:
        return None
    
    # Extract the full post by tracking braces (skipping content field)
    depth = 0
    in_content = False
    content_parts = []
    content_end_line = None
    post_lines = []
    
    for i in range(post_start, len(LINES)):
        line = LINES[i]
        
        # Check for content field start
        if 'content:' in line and not in_content:
            in_content = True
            ci = line.find('`')
            if ci >= 0:
                before_content = line[:line.find('content:')]
                post_lines.append(before_content)
                rest = line[ci+1:]
                # Check if content ends on same line
                btc = rest.find('`')
                if btc >= 0:
                    content_parts.append(rest[:btc])
                    content_end_line = i
                    in_content = False
                    continue
                else:
                    content_parts.append(rest)
                    continue
            continue
        
        if in_content:
            btc = line.find('`')
            if btc >= 0:
                content_parts.append(line[:btc])
                content_end_line = i
                in_content = False
                continue
            else:
                content_parts.append(line)
                continue
        
        # Track braces for non-content lines
        for ch in line:
            if ch == '{':
                depth += 1
            elif ch == '}':
                depth -= 1
        
        if not in_content:
            post_lines.append(line)
        
        # Check if we've closed the post
        if depth == 0 and i > start_line and '}' in line:
            break
    
    content = '\n'.join(content_parts)
    
    # Extract fields from post_lines
    def extract_field(field):
        for line in post_lines:
            stripped = line.strip()
            if stripped.startswith(field + ':'):
                # Extract value between quotes
                m = re.search(r':\s*"((?:[^"\\]|\\.)*)"', stripped)
                if m:
                    return m.group(1)
        return None
    
    # Extract tags
    tags = []
    for line in post_lines:
        stripped = line.strip()
        if stripped.startswith('tags:'):
            tags_str = stripped[5:].strip()
            tags = re.findall(r'"([^"]*)"', tags_str)
            break
    
    title = extract_field('title')
    
    # Extract excerpt (might span multiple lines)
    excerpt_lines = []
    in_excerpt = False
    for line in post_lines:
        stripped = line.strip()
        if stripped.startswith('excerpt:'):
            in_excerpt = True
            val = stripped[8:].strip()
            if val.startswith('"') and val.endswith('",'):
                excerpt_lines.append(val[1:-2])
                break
            elif val.startswith('"'):
                excerpt_lines.append(val[1:])
                continue
            else:
                break
        if in_excerpt:
            if stripped.endswith('",'):
                excerpt_lines.append(stripped[:-2])
                break
            else:
                excerpt_lines.append(stripped)
    
    excerpt = ' '.join(excerpt_lines).strip()
    # Remove trailing comma if any
    if excerpt.endswith(','):
        excerpt = excerpt[:-1]
    
    return {
        'slug': slug,
        'title': title,
        'date': extract_field('date'),
        'excerpt': excerpt,
        'author': extract_field('author'),
        'tags': tags,
        'content': content
    }


def check_tfidf(post):
    title = post.get('title', '')
    content = post.get('content', '')
    
    # Extract meaningful terms from title
    # For Bengali titles, extract the first noun phrase
    title_lower = title.lower()
    
    # Check if title is Bengali
    is_bengali = bool(re.search(r'[\u0980-\u09FF]', title))
    
    if is_bengali:
        # Extract the main topic (usually before colon or em dash)
        parts = re.split(r'[:\u2014\u2013\u2015-]\s*', title)
        keyword = parts[0].strip() if parts else title
        # Remove common Bengali stop words
        bengali_stopwords = ['কীভাবে', 'কেন', 'কি', 'কোন', 'আপনার', 'বাংলায়', 'নিয়ম']
        for sw in bengali_stopwords:
            keyword = keyword.replace(sw, '').strip()
        
        # If not much left, use the full first part
        if len(keyword) < 3:
            keyword = parts[0].strip() if parts else title
        
        # Count occurrences (substring search since Bengali has no word boundaries like English)
        count = content.count(keyword)
        
        # Also try with the more specific term
        # Check for key Bengali terms
        bengali_terms = re.findall(r'[\u0980-\u09FF]{4,}', title)
        for term in bengali_terms[:3]:
            term_count = content.count(term)
            if term_count > count:
                count = term_count
                keyword = term
        
        # Check for English keywords mixed in Bengali title
        english_words = re.findall(r'[a-zA-Z]{3,}', title)
        for word in english_words:
            word_count = len(re.findall(r'\b' + re.escape(word.lower()) + r'\b', content.lower()))
            if word_count > count:
                count = word_count
                keyword = word
        
        passed = count >= 5
        return {'keyword': keyword, 'count': count, 'passed': passed}
    else:
        # English title - use existing logic
        stop_words = {'a', 'an', 'the', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
                      'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
                      'should', 'may', 'might', 'can', 'shall', 'to', 'of', 'in', 'for',
                      'on', 'with', 'at', 'by', 'from', 'as', 'into', 'through', 'during',
                      'before', 'after', 'above', 'below', 'between', 'out', 'off', 'over',
                      'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when',
                      'where', 'why', 'how', 'all', 'each', 'every', 'both', 'few', 'more',
                      'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own',
                      'same', 'so', 'than', 'too', 'very', 'just', 'because', 'but', 'and',
                      'or', 'if', 'while', 'about', 'up', 'down', 'your', 'our', 'its',
                      'best', 'top', 'ultimate', 'complete', 'essential', 'guide', 'tips',
                      'checklist', 'strategies', 'strategy', 'optimization', 'whats',
                      'ways', 'benefits', 'need', 'needs', 'right', 'should', 'does',
                      'bangladesh', 'bangladeshi', 'bangla', 'bd'}
        
        words = re.findall(r'[a-zA-Z]+', title_lower)
        meaningful = [w for w in words if w not in stop_words and len(w) > 2]
        
        primary_keyword = meaningful[0] if meaningful else title_lower.split()[0] if title_lower.split() else ''
        
        # Try bigrams/trigrams
        phrases = []
        for i in range(len(meaningful) - 1):
            phrases.append(meaningful[i] + ' ' + meaningful[i+1])
        
        content_lower = content.lower()
        single_count = len(re.findall(r'\b' + re.escape(primary_keyword.lower()) + r'\b', content_lower)) if primary_keyword else 0
        
        best_count = single_count
        best_keyword = primary_keyword
        for phrase in phrases:
            count = content_lower.count(phrase.lower())
            if count > best_count:
                best_count = count
                best_keyword = phrase
        
        passed = best_count >= 5
        return {'keyword': best_keyword or 'SEO', 'count': best_count, 'passed': passed}


def check_entities(post):
    content = post.get('content', '')
    content_lower = content.lower()
    
    # Check for location entities
    has_dhaka = 'ঢাকা' in content or 'dhaka' in content_lower
    has_bangladesh = 'বাংলাদেশ' in content or 'bangladesh' in content_lower
    
    missing = []
    if not has_bangladesh:
        missing.append('Bangladesh')
    if not has_dhaka:
        missing.append('Dhaka')
    
    # Check for service type entities
    service_keywords = ['seo', 'digital marketing', 'web design', 'content', 'link building', 'local seo']
    for kw in service_keywords:
        if kw in content_lower:
            break
    
    return {
        'required_entities': ['Dhaka', 'Bangladesh'],
        'missing': missing,
        'passed': len(missing) == 0
    }


def check_pillar_cluster(post):
    tags = post.get('tags', [])
    content = post.get('content', '')
    
    pillar_map = {
        'seo basics': ['SEO Guide', 'Bangladesh SEO', 'SEO', 'SEO Tips', 'SEO Fundamentals', 'Digital Marketing'],
        'local seo': ['Local SEO', 'Google Maps', 'GBP', 'Google Business Profile'],
        'technical seo': ['Technical SEO', 'Core Web Vitals', 'Site Speed', 'Crawlability'],
        'ecommerce seo': ['E-commerce', 'Ecommerce', 'Online Store'],
        'content marketing': ['Content Marketing', 'Content Strategy', 'Blogging'],
        'link building': ['Link Building', 'Backlinks', 'Off-Page SEO'],
        'geo/aeo': ['GEO', 'AEO', 'AI Search', 'Generative Engine'],
        'seo career': ['SEO Career', 'SEO Jobs', 'SEO Professional'],
        'case study': ['Case Study', 'Results', 'Local SEO'],
        'schema/semantic': ['Schema', 'Structured Data', 'Semantic', 'Rich Snippets', 'স্কিমা', 'স্ট্রাকচারড'],
        'bangla seo': ['বাংলা', 'বাংলাদেশ'],
    }
    
    pillar_topic = 'General SEO'
    for tag in tags:
        for pillar, keywords in pillar_map.items():
            for kw in keywords:
                if kw.lower() in tag.lower():
                    pillar_topic = pillar
                    break
    
    # Check for links to pillar pages (services, industries, blog)
    service_links = len(re.findall(r'\(/services/[^)]+\)', content))
    industry_links = len(re.findall(r'\(/industries/[^)]+\)', content))
    blog_links = len(re.findall(r'\(/blog/[^)]+\)', content))
    home_links = len(re.findall(r'\]\(/\)', content))
    
    has_pillar_link = service_links > 0 or industry_links > 0 or blog_links > 0
    
    return {
        'pillar_topic': pillar_topic,
        'has_pillar_link': has_pillar_link,
        'service_links': service_links,
        'industry_links': industry_links,
        'blog_links': blog_links,
        'home_links': home_links,
        'passed': has_pillar_link
    }


def check_aeo_geo(post):
    content = post.get('content', '')
    
    # Count question-based headings (any heading with ?)
    heading_lines = re.findall(r'^#{1,3}\s+(.*)', content, re.MULTILINE)
    question_headings = [h for h in heading_lines if '?' in h]
    
    # Also check for Bengali question markers
    bengali_q = ['কীভাবে', 'কেন', 'কি', 'কী', 'কোন', 'কখন', 'কোথায়', 'কেমন']
    for h in heading_lines:
        for marker in bengali_q:
            if h.startswith(marker) or (' ' + marker) in h:
                if h not in question_headings:
                    question_headings.append(h)
                break
    
    return {
        'question_headings': len(question_headings),
        'passed': len(question_headings) >= 2
    }


def check_internal_links(post):
    content = post.get('content', '')
    
    # Count all internal links - match markdown link syntax [text](url)
    all_links = re.findall(r'\[([^\]]*)\]\(([^)]+)\)', content)
    
    # Filter for internal links only
    internal = []
    for text, url in all_links:
        url = url.strip()
        if url.startswith('/') and not url.startswith('//') and not url.startswith('/#'):
            internal.append((text, url))
    
    # Categorize
    blog_links = [u for _, u in internal if u.startswith('/blog/')]
    service_links = [u for _, u in internal if u.startswith('/services/')]
    industry_links = [u for _, u in internal if u.startswith('/industries/')]
    home_links = [u for _, u in internal if u == '/']
    location_links = [u for _, u in internal if u.startswith('/locations/')]
    case_study_links = [u for _, u in internal if u.startswith('/case-studies/')]
    about_links = [u for _, u in internal if u.startswith('/about')]
    contact_links = [u for _, u in internal if u.startswith('/contact')]
    portfolio_links = [u for _, u in internal if u.startswith('/portfolio')]
    
    return {
        'total': len(internal),
        'blog_links': len(blog_links),
        'service_links': len(service_links),
        'industry_links': len(industry_links),
        'home_links': len(home_links),
        'other_links': len(internal) - len(blog_links) - len(service_links) - len(industry_links) - len(home_links),
        'passed': len(internal) >= 3
    }


def check_schema_readiness(post):
    title = post.get('title')
    excerpt = post.get('excerpt')
    date = post.get('date')
    author = post.get('author')
    tags = post.get('tags', [])
    
    missing = []
    if not title:
        missing.append('title')
    if not excerpt:
        missing.append('excerpt')
    if not date:
        missing.append('date')
    if not author:
        missing.append('author')
    if not tags:
        missing.append('tags (array)')
    
    return {
        'missing_fields': missing,
        'passed': len(missing) == 0
    }


def check_post(post):
    results = {}
    results['tfidf'] = check_tfidf(post)
    results['entities'] = check_entities(post)
    results['pillar'] = check_pillar_cluster(post)
    results['aeo_geo'] = check_aeo_geo(post)
    results['internal_links'] = check_internal_links(post)
    results['schema'] = check_schema_readiness(post)
    return results


def format_report(slug, results, title):
    lines = [f"## Post: {slug}"]
    lines.append(f"*{title}*")
    lines.append("| Check | Status | Details |")
    lines.append("|-------|--------|---------|")
    
    tf = results['tfidf']
    lines.append(f"| TF-IDF: `{tf['keyword'][:30]}` | {'✅' if tf['passed'] else '❌'} | {tf['count']} occurrences |")
    
    en = results['entities']
    missing_str = ', '.join(en['missing']) if en['missing'] else 'None'
    lines.append(f"| Entities | {'✅' if en['passed'] else '❌'} | Missing: {missing_str} |")
    
    pi = results['pillar']
    status = '✅' if pi['passed'] else '❌'
    lines.append(f"| Pillar Link | {status} | Pillar: {pi['pillar_topic']} | Service: {pi['service_links']}, Industry: {pi['industry_links']}, Blog: {pi['blog_links']} |")
    
    ae = results['aeo_geo']
    lines.append(f"| AEO/GEO | {'✅' if ae['passed'] else '❌'} | {ae['question_headings']} question headings |")
    
    il = results['internal_links']
    lines.append(f"| Internal Links | {'✅' if il['passed'] else '❌'} | {il['total']} total | Blog: {il['blog_links']}, Service: {il['service_links']}, Industry: {il['industry_links']} |")
    
    sc = results['schema']
    missing = 'All fields set' if sc['passed'] else ', '.join(sc['missing_fields'])
    lines.append(f"| Schema Ready | {'✅' if sc['passed'] else '❌'} | {missing} |")
    
    lines.append("")
    lines.append("### Fix instructions:")
    fixes = []
    
    if not tf['passed']:
        fixes.append(f"- ❌ **TF-IDF thin**: `{tf['keyword'][:40]}` appears only {tf['count']}x in content. Add ≥5 occurrences.")
    if not en['passed']:
        fixes.append(f"- ❌ **Missing entities**: {', '.join(en['missing'])} not mentioned in post content.")
    if not pi['passed']:
        fixes.append(f"- ❌ **No pillar link**: Post ({pi['pillar_topic']}) doesn't link to any related service, industry, or blog page.")
    if not ae['passed']:
        fixes.append(f"- ❌ **AEO/GEO weak**: Only {ae['question_headings']} question heading(s). Add ≥2 FAQ-style headings with '?' mark.")
    if not il['passed']:
        fixes.append(f"- ❌ **Too few internal links**: Only {il['total']} internal link(s). Add ≥3 links to posts, services, or industries.")
    if not sc['passed']:
        fixes.append(f"- ❌ **Schema fields missing**: {', '.join(sc['missing_fields'])}. Add these for ArticleSchema.")
    
    if all([tf['passed'], en['passed'], pi['passed'], ae['passed'], il['passed'], sc['passed']]):
        fixes.append("- ✅ **All checks passed** — no fixes needed.")
    
    lines.extend(fixes)
    lines.append("")
    
    return '\n'.join(lines)


def main():
    slugs = sys.argv[1:] if len(sys.argv) > 1 else []
    if not slugs:
        print("Usage: python3 framework_check_v2.py <slug1> [slug2 ...]")
        sys.exit(1)
    
    all_passed = True
    reports = []
    
    for slug in slugs:
        post = extract_post_by_slug(slug)
        if post is None:
            reports.append(f"## Post: {slug}\n⚠️  Could not find post in data.js\n")
            all_passed = False
            continue
        
        print(f"Checking: {post.get('title', slug)}", file=sys.stderr)
        checks = check_post(post)
        report = format_report(slug, checks, post.get('title', slug))
        reports.append(report)
        
        for check_name, check_result in checks.items():
            if not check_result['passed']:
                all_passed = False
    
    print('\n'.join(reports))
    
    if all_passed:
        print("\n✅ **ALL CHECKS PASSED** for all analyzed posts.")


if __name__ == '__main__':
    main()
