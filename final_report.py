#!/usr/bin/env python3
"""Final report generator - runs all checks and produces markdown output"""
import re, sys

with open('src/app/blog/data.js', 'r') as f:
    FILE_CONTENT = f.read()
LINES = FILE_CONTENT.split('\n')

def extract_post_by_slug(slug):
    """Extract post object from data.js"""
    start_line = None
    for i, line in enumerate(LINES):
        stripped = line.strip()
        if stripped.startswith('slug:') and f'"{slug}"' in stripped:
            start_line = i
            break
    if start_line is None:
        return None
    
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
    
    depth = 0
    in_content = False
    content_parts = []
    content_end_line = None
    post_lines = []
    
    for i in range(post_start, len(LINES)):
        line = LINES[i]
        if 'content:' in line and not in_content:
            in_content = True
            ci = line.find('`')
            if ci >= 0:
                before_content = line[:line.find('content:')]
                post_lines.append(before_content)
                rest = line[ci+1:]
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
        
        for ch in line:
            if ch == '{': depth += 1
            elif ch == '}': depth -= 1
        
        if not in_content:
            post_lines.append(line)
        
        if depth == 0 and i > start_line and '}' in line:
            break
    
    content = '\n'.join(content_parts)
    
    def extract_field(field):
        for line in post_lines:
            stripped = line.strip()
            if stripped.startswith(field + ':'):
                m = re.search(r':\s*"((?:[^"\\]|\\.)*)"', stripped)
                if m:
                    return m.group(1)
        return None
    
    tags = []
    for line in post_lines:
        stripped = line.strip()
        if stripped.startswith('tags:'):
            tags_str = stripped[5:].strip()
            tags = re.findall(r'"([^"]*)"', tags_str)
            break
    
    # Extract excerpt (might span multiple lines)
    excerpt = ''
    for i, line in enumerate(post_lines):
        stripped = line.strip()
        if stripped.startswith('excerpt:'):
            lines_after = post_lines[i:]
            combined = ' '.join(l.strip() for l in lines_after)
            # Extract value between first " and last ",
            m = re.search(r'excerpt:\s*"((?:[^"\\]|\\.)*)"', combined)
            if m:
                excerpt = m.group(1)
            break
    
    return {
        'slug': slug,
        'title': extract_field('title'),
        'date': extract_field('date'),
        'excerpt': excerpt,
        'author': extract_field('author'),
        'tags': tags,
        'content': content
    }

# === CHECKS ===
def check_tfidf(post):
    title = post.get('title', '')
    content = post.get('content', '')
    is_bengali = bool(re.search(r'[\u0980-\u09FF]', title))
    
    if is_bengali:
        parts = re.split(r'[:\u2014\u2013\u2015-]\s*', title)
        keyword = parts[0].strip() if parts else title
        count = content.count(keyword)
        english_words = re.findall(r'[a-zA-Z]{3,}', title)
        for word in english_words:
            wc = len(re.findall(r'\b' + re.escape(word.lower()) + r'\b', content.lower()))
            if wc > count:
                count = wc
                keyword = word
        passed = count >= 5
        return {'keyword': keyword[:30], 'count': count, 'passed': passed}
    else:
        stop_words = {'a','an','the','is','are','was','were','be','been','being','have','has','had',
                      'do','does','did','will','would','could','should','may','might','can','shall',
                      'to','of','in','for','on','with','at','by','from','as','into','through','during',
                      'before','after','above','below','between','out','off','over','under','again',
                      'further','then','once','here','there','when','where','why','how','all','each',
                      'every','both','few','more','most','other','some','such','no','nor','not','only',
                      'own','same','so','than','too','very','just','because','but','and','or','if',
                      'while','about','up','down','your','our','its','best','top','ultimate','complete',
                      'essential','guide','tips','checklist','strategies','strategy','optimization',
                      'whats','ways','benefits','need','needs','right','should','does','bangladesh',
                      'bangladeshi','bangla','bd'}
        title_lower = title.lower()
        words = re.findall(r'[a-zA-Z]+', title_lower)
        meaningful = [w for w in words if w not in stop_words and len(w) > 2]
        primary = meaningful[0] if meaningful else title_lower.split()[0] if title_lower.split() else ''
        content_lower = content.lower()
        single_count = len(re.findall(r'\b' + re.escape(primary.lower()) + r'\b', content_lower)) if primary else 0
        
        phrases = [' '.join(meaningful[i:i+2]) for i in range(len(meaningful)-1)]
        best_count, best_keyword = single_count, primary
        for phrase in phrases:
            c = content_lower.count(phrase.lower())
            if c > best_count:
                best_count, best_keyword = c, phrase
        passed = best_count >= 5
        return {'keyword': best_keyword or 'SEO', 'count': best_count, 'passed': passed}

def check_entities(post):
    content = post.get('content', '')
    cl = content.lower()
    missing = []
    if not ('বাংলাদেশ' in content or 'bangladesh' in cl):
        missing.append('Bangladesh')
    if not ('ঢাকা' in content or 'dhaka' in cl):
        missing.append('Dhaka')
    return {'missing': missing, 'passed': len(missing) == 0}

def check_pillar(post):
    content = post.get('content', '')
    svc = len(re.findall(r'\(/services/[^)]+\)', content))
    ind = len(re.findall(r'\(/industries/[^)]+\)', content))
    blog = len(re.findall(r'\(/blog/[^)]+\)', content))
    has = svc > 0 or ind > 0 or blog > 0
    return {'service_links': svc, 'industry_links': ind, 'blog_links': blog, 'passed': has}

def check_aeo(post):
    content = post.get('content', '')
    headings = re.findall(r'^#{1,3}\s+(.*)', content, re.MULTILINE)
    qh = [h for h in headings if '?' in h]
    # Bengali question markers
    bq_markers = ['কীভাবে', 'কেন', 'কি', 'কী', 'কোন', 'কখন', 'কোথায়']
    for h in headings:
        for marker in bq_markers:
            if marker in h and h not in qh:
                qh.append(h)
                break
    return {'question_headings': len(qh), 'passed': len(qh) >= 2}

def check_links(post):
    content = post.get('content', '')
    links = re.findall(r'\[([^\]]*)\]\(([^)]+)\)', content)
    internal = [(t, u) for t, u in links if u.startswith('/') and not u.startswith('//')]
    blog = sum(1 for _, u in internal if u.startswith('/blog/'))
    svc = sum(1 for _, u in internal if u.startswith('/services/'))
    ind = sum(1 for _, u in internal if u.startswith('/industries/'))
    return {'total': len(internal), 'blog_links': blog, 'service_links': svc, 'industry_links': ind, 'passed': len(internal) >= 3}

def check_schema(post):
    missing = []
    if not post.get('title'): missing.append('title')
    if not post.get('excerpt'): missing.append('excerpt')
    if not post.get('date'): missing.append('date')
    if not post.get('author'): missing.append('author')
    if not post.get('tags'): missing.append('tags')
    return {'missing': missing, 'passed': len(missing) == 0}

def analyze(slug):
    post = extract_post_by_slug(slug)
    if not post:
        return None, None
    tf = check_tfidf(post)
    en = check_entities(post)
    pi = check_pillar(post)
    ae = check_aeo(post)
    il = check_links(post)
    sc = check_schema(post)
    results = {'tfidf': tf, 'entities': en, 'pillar': pi, 'aeo': ae, 'links': il, 'schema': sc}
    return post, results

def format_result(slug, post, results):
    lines = [f"## Post: `{slug}`"]
    lines.append(f"**Title:** {post['title']}")
    lines.append("")
    lines.append("| Check | Status | Details |")
    lines.append("|-------|--------|---------|")
    
    tf = results['tfidf']
    lines.append(f"| TF-IDF: `{tf['keyword']}` | {'✅' if tf['passed'] else '❌'} | {tf['count']} occurrences |") 
    
    en = results['entities']
    ms = ', '.join(en['missing']) if en['missing'] else 'None'
    lines.append(f"| Entities | {'✅' if en['passed'] else '❌'} | Missing: {ms} |")
    
    pi = results['pillar']
    lines.append(f"| Pillar Link | {'✅' if pi['passed'] else '❌'} | Service: {pi['service_links']}, Industry: {pi['industry_links']}, Blog: {pi['blog_links']} |")
    
    ae = results['aeo']
    lines.append(f"| AEO/GEO | {'✅' if ae['passed'] else '❌'} | {ae['question_headings']} question headings |")
    
    il = results['links']
    lines.append(f"| Internal Links | {'✅' if il['passed'] else '❌'} | {il['total']} total (blog: {il['blog_links']}, svc: {il['service_links']}, ind: {il['industry_links']}) |")
    
    sc = results['schema']
    ms = 'All set' if sc['passed'] else ', '.join(sc['missing'])
    lines.append(f"| Schema Ready | {'✅' if sc['passed'] else '❌'} | {ms} |")
    
    lines.append("")
    lines.append("### Fix instructions:")
    fixes = []
    if not tf['passed']:
        fixes.append(f"- ❌ **TF-IDF thin**: `{tf['keyword']}` appears only {tf['count']}x (need ≥5)")
    if not en['passed']:
        fixes.append(f"- ❌ **Missing entities**: Add `{'`, `'.join(en['missing'])}` mentions")
    if not pi['passed']:
        fixes.append(f"- ❌ **No pillar link**: Add contextual links to services, industries, or blog posts")
    if not ae['passed']:
        fixes.append(f"- ❌ **AEO/GEO weak**: Only {ae['question_headings']} question heading(s) — add ≥2")
    if not il['passed']:
        fixes.append(f"- ❌ **Too few internal links**: Only {il['total']} — add ≥3 contextual links")
    if not sc['passed']:
        fixes.append(f"- ❌ **Schema incomplete**: Missing `{'`, `'.join(sc['missing'])}`")
    if not fixes:
        fixes.append("- ✅ **All checks passed**")
    lines.extend(fixes)
    lines.append("")
    return '\n'.join(lines)

# === MAIN ===
if __name__ == '__main__':
    slugs = sys.argv[1:] if len(sys.argv) > 1 else []
    if not slugs:
        print("Usage: python3 final_report.py <slug1> [slug2 ...]")
        sys.exit(1)
    
    for slug in slugs:
        post, results = analyze(slug)
        if post is None:
            print(f"## Post: {slug}")
            print("⚠️  Not found in data.js")
            print()
        else:
            print(format_result(slug, post, results))
    
    # Summary
    print("---")
    print(f"**Posts checked:** {len(slugs)}")
