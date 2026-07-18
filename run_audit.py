#!/usr/bin/env python3
"""
Content Framework Enforcer for kanokmiah.com.bd - Optimized version.
"""
import re, subprocess, sys

# ── Step 1: Get modified slugs from git ──────────────────────────
result = subprocess.run(
    ['git', 'log', '--oneline', '--since=48 hours ago', '--format=%s', '--', 'src/app/blog/data.js'],
    capture_output=True, text=True, cwd='/root/kanok-miahit'
)
msgs = result.stdout.strip().split('\n')

modified_slugs = set()
for msg in msgs:
    for m in re.finditer(r'processed blog #\d+ - ([a-z0-9-]+)', msg):
        modified_slugs.add(m.group(1))
    for m in re.finditer(r'fix: deep audit fixes for ([a-z0-9-]+)', msg):
        modified_slugs.add(m.group(1))

# Also catch explicit slug patterns in commit messages
for msg in msgs:
    words = msg.split()
    for w in words:
        if re.match(r'^[a-z0-9-]+$', w) and len(w) > 10:
            if any(kw in w for kw in ['seo', 'blog', 'local', 'google', 'content', 'link', 'mobile', 'ecommerce', 'keyword', 'schema', 'technical']):
                modified_slugs.add(w)
            elif '-' in w and len(w.split('-')) >= 3:
                modified_slugs.add(w)

# ── Step 2: Parse data.js with line-by-line parser ───────────────
posts = []
with open('/root/kanok-miahit/src/app/blog/data.js', 'r') as f:
    lines = f.readlines()

print(f"Parsing {len(lines)} lines...", file=sys.stderr)

# Find post boundaries
brace_depth = 0
post_start = -1
current_post_lines = []
in_posts_array = False

for i, line in enumerate(lines):
    stripped = line.strip()
    
    if not in_posts_array:
        if 'const posts = [' in stripped or 'const posts=[' in stripped:
            in_posts_array = True
        continue
    
    if stripped.startswith('{') and not stripped.startswith('{{'):
        if post_start == -1:
            post_start = i
            current_post_lines = [line]
            brace_depth = stripped.count('{') - stripped.count('}')
        else:
            current_post_lines.append(line)
            brace_depth += stripped.count('{') - stripped.count('}')
    elif post_start >= 0:
        current_post_lines.append(line)
        brace_depth += stripped.count('{') - stripped.count('}')
        
        if brace_depth <= 0 and i > post_start:
            # End of post object
            post_text = ''.join(current_post_lines)
            
            # Extract fields
            slug_m = re.search(r'slug:\s*"([^"]+)"', post_text)
            title_m = re.search(r'title:\s*"([^"]*)"', post_text)
            date_m = re.search(r'date:\s*"([^"]*)"', post_text)
            excerpt_m = re.search(r'excerpt:\s*"([^"]*)"', post_text)
            tags_m = re.search(r'tags:\s*\[([^\]]+)\]', post_text)
            author_m = re.search(r'author:\s*"([^"]*)"', post_text)
            img_m = re.search(r'imagePlaceholder:\s*"([^"]*)"', post_text)
            metaT_m = re.search(r'metaTitle:\s*"([^"]*)"', post_text)
            metaD_m = re.search(r'metaDescription:\s*"([^"]*)"', post_text)
            dateMod_m = re.search(r'dateModified:\s*"([^"]*)"', post_text)
            
            # Content - find the template literal
            content_m = re.search(r'content:\s*`([^`]*)`', post_text)
            if not content_m:
                # Content might span multiple lines with backticks
                # Find from "content: `" to the next "`"
                cm = re.search(r'content:\s*`', post_text)
                if cm:
                    rest = post_text[cm.end():]
                    # Find the closing backtick followed by comma or newline
                    end_idx = -1
                    for j in range(len(rest)):
                        if rest[j] == '`' and (j+1 >= len(rest) or rest[j+1] in [',', '\n', ' ', '']):
                            end_idx = j
                            break
                    if end_idx >= 0:
                        content = rest[:end_idx]
                    else:
                        content = ''
                else:
                    content = ''
            else:
                content = content_m.group(1)
            
            if slug_m and title_m:
                tags = []
                if tags_m:
                    raw_tags = tags_m.group(1)
                    tags = [t.strip().strip('"').strip("'") for t in raw_tags.split(',')]
                
                posts.append({
                    'slug': slug_m.group(1),
                    'title': title_m.group(1) if title_m else '',
                    'date': date_m.group(1) if date_m else '',
                    'author': author_m.group(1) if author_m else '',
                    'excerpt': excerpt_m.group(1) if excerpt_m else '',
                    'tags': tags,
                    'imagePlaceholder': img_m.group(1) if img_m else '',
                    'metaTitle': metaT_m.group(1) if metaT_m else '',
                    'metaDescription': metaD_m.group(1) if metaD_m else '',
                    'dateModified': dateMod_m.group(1) if dateMod_m else '',
                    'content': content
                })
            
            post_start = -1
            current_post_lines = []
    elif stripped.startswith(']'):
        break  # End of posts array

print(f"Posts extracted: {len(posts)}", file=sys.stderr)

# Build slug dict
posts_dict = {p['slug']: p for p in posts if p['slug']}

# Filter to only modified slugs that exist in the dictionary
to_check = [s for s in modified_slugs if s in posts_dict]
# Also add slugs that are close matches
for s in list(modified_slugs):
    if s not in posts_dict:
        for pslug in posts_dict:
            if s in pslug or pslug in s:
                to_check.append(pslug)
                break

to_check = list(set(to_check))
print(f"Slugs to check: {len(to_check)}", file=sys.stderr)

# ── Step 3: Checks ───────────────────────────────────────────────

def check_tfidf(post):
    title = post['title']
    content = post['content']
    
    words = title.lower().split()
    stopwords = {'a','an','the','for','in','of','to','and','or','is','are','your','our','its',
                 'that','this','with','from','by','at','on','be','has','have','not','but','was',
                 'were','will','can','all','each','every','some','any','no','more','most','best',
                 'top','guide','tips','how','what','why','when','where','which','who'}
    
    keyword = ''
    for w in words:
        wc = w.strip('0123456789-')
        if len(wc) >= 4 and wc not in stopwords and wc not in ('seo','bangladesh','bangladeshi','bangla','bd','2026','2025','2024'):
            keyword = wc
            break
    
    if not keyword:
        for i, w in enumerate(words):
            if w in ('seo','complete','ultimate','essential') and i+1 < len(words):
                keyword = words[i+1].strip('0123456789-')
                if len(keyword) >= 4:
                    break
    
    if not keyword:
        keyword = words[-1] if words else title.lower()
    
    count = len(re.findall(re.escape(keyword), content, re.IGNORECASE))
    
    # Check bigrams
    bigrams = [' '.join(words[i:i+2]) for i in range(len(words)-1)]
    bigram_count = sum(len(re.findall(re.escape(bg), content, re.IGNORECASE)) for bg in bigrams if len(bg) > 8)
    
    passed = count >= 5 or bigram_count >= 3
    return {
        'keyword': keyword,
        'count': count,
        'bigram_count': bigram_count,
        'passed': passed,
        'detail': f"{count} occurrences of '{keyword}'" + (f", {bigram_count} bigram matches" if bigram_count > 0 else "")
    }


def check_entities(post):
    content_lower = post['content'].lower()
    title_lower = post['title'].lower()
    slug = post['slug'].lower()
    
    missing = []
    present = []
    
    # Dhaka
    if 'dhaka' in content_lower:
        present.append('Dhaka')
    else:
        missing.append('Location: Dhaka')
    
    # Bangladesh
    if 'bangladesh' in content_lower:
        present.append('Bangladesh')
    else:
        missing.append('Location: Bangladesh')
    
    # SEO
    if 'seo' in content_lower:
        present.append('SEO')
    else:
        missing.append('Service: SEO')
    
    # Industry-specific entities
    industry_map = {
        'ecommerce': ['ecommerce','e-commerce','online store','shop'],
        'real estate': ['real estate','property','developer'],
        'healthcare': ['healthcare','medical','clinic','doctor','hospital'],
        'education': ['education','school','university','college'],
        'travel': ['travel','tourism','tour','hotel'],
        'ngo': ['ngo','non-profit','nonprofit','charity'],
        'law': ['law firm','lawyer','attorney','legal'],
        'fitness': ['fitness','gym'],
        'startup': ['startup'],
        'garments': ['garment','textile','rmg'],
        'photography': ['photographer','videographer'],
        'event': ['event','wedding','planner'],
        'youtube': ['youtube'],
        'podcast': ['podcast'],
        'facebook': ['facebook','marketplace'],
        'restaurant': ['restaurant','food'],
        'mobile': ['mobile','smartphone'],
        'link building': ['link building','backlink'],
        'keyword': ['keyword research','long-tail keyword'],
        'schema': ['schema','structured data','rich snippet'],
    }
    
    for industry, terms in industry_map.items():
        if any(t in slug or t in title_lower for t in terms):
            if any(t in content_lower for t in terms):
                present.append(industry)
            else:
                missing.append(f'Industry: {industry}')
    
    return {
        'passed': len(missing) == 0,
        'present': present,
        'missing': missing
    }


def check_pillar_cluster(post):
    tags = [t.lower() for t in post['tags']]
    content_lower = post['content'].lower()
    slug = post['slug'].lower()
    
    pillar_pages = {
        'seo-guide': {'match': ['seo guide','complete seo'], 'url': '/blog/complete-seo-guide-bangladesh-businesses-2026'},
        'local-seo': {'match': ['local seo','local search','google maps','google business'], 'url': '/blog/local-seo-tips-dhaka-businesses-google-maps'},
        'technical-seo': {'match': ['technical seo','core web vitals','page speed'], 'url': '/blog/technical-seo-checklist-bangladeshi-websites'},
        'link-building': {'match': ['link building','backlink','off-page'], 'url': '/blog/link-building-strategies-bangladesh-market'},
        'content-marketing': {'match': ['content marketing','content strategy'], 'url': '/blog/content-marketing-seo-friendly-content-writing'},
        'keyword-research': {'match': ['keyword research','long-tail keyword','keyword clustering'], 'url': '/blog/keyword-research-bangladesh-market'},
        'ecommerce-seo': {'match': ['ecommerce','e-commerce','online store'], 'url': '/blog/ecommerce-seo-daraz-shopify-guide'},
        'mobile-seo': {'match': ['mobile seo','mobile-first','mobile optimization'], 'url': '/blog/mobile-seo-optimization-bangladesh-mobile-first-era'},
        'schema-markup': {'match': ['schema','structured data','rich snippet','json-ld'], 'url': '/blog/schema-markup-rich-snippets-techniques'},
        'seo-vs-ads': {'match': ['google ads','ppc','seo vs','vs google'], 'url': '/blog/seo-vs-google-ads-bangladesh-business'},
    }
    
    matched_pillar = None
    for pname, pinfo in pillar_pages.items():
        if any(m in slug or any(m in t for t in tags) for m in pinfo['match']):
            matched_pillar = pname
            break
    
    if not matched_pillar:
        best = None
        best_score = 0
        for pname, pinfo in pillar_pages.items():
            score = sum(1 for m in pinfo['match'] if m in content_lower)
            if score > best_score:
                best_score = score
                best = pname
        matched_pillar = best
    
    # Check for any pillar link
    linked_pillars = []
    for pname, pinfo in pillar_pages.items():
        if pinfo['url'] in content_lower:
            linked_pillars.append(pname)
    
    return {
        'matched_pillar': matched_pillar,
        'linked_pillars': linked_pillars,
        'any_pillar_link': len(linked_pillars) > 0
    }


def check_aeo_geo(post):
    content = post['content']
    headings = re.findall(r'^#{1,6}\s+(.+)$', content, re.MULTILINE)
    
    question_words = ['How','What','Why','When','Where','Can','Do','Is','Are','Does','Which','Who','Whose']
    qheadings = [h.strip() for h in headings if re.match(r'^(How|What|Why|When|Where|Can|Do|Is|Are|Does|Which|Who|Whose)\s', h.strip())]
    
    return {
        'total_headings': len(headings),
        'question_headings': qheadings,
        'count': len(qheadings),
        'passed': len(qheadings) >= 2
    }


def check_internal_links(post):
    content = post['content']
    
    patterns = [
        (r'\]\(/blog/[^)]+\)', 'blog'),
        (r'\]\(/locations/[^)]+\)', 'locations'),
        (r'\]\(/services/[^)]+\)', 'services'),
        (r'\]\(/industries/[^)]+\)', 'industries'),
        (r'\]\(/about[^)]*\)', 'about'),
        (r'\]\(/contact[^)]*\)', 'contact'),
    ]
    
    counts = {}
    total = 0
    for pat, cat in patterns:
        matches = re.findall(pat, content)
        counts[cat] = len(matches)
        total += len(matches)
    
    # Homepage link
    home_matches = re.findall(r'\]\(/\)', content)
    counts['homepage'] = len(home_matches)
    total += len(home_matches)
    
    return {
        'total': total,
        'blog': counts.get('blog', 0),
        'locations': counts.get('locations', 0),
        'services': counts.get('services', 0),
        'industries': counts.get('industries', 0),
        'other': counts.get('about', 0) + counts.get('contact', 0) + counts.get('homepage', 0),
        'passed': total >= 3
    }


def check_schema(post):
    issues = []
    
    if not post['title'] or len(post['title']) < 10:
        issues.append('Missing/short title')
    if not post['excerpt'] or len(post['excerpt']) < 50:
        issues.append(f'Missing/short excerpt ({len(post.get("excerpt",""))} chars)')
    if not post['date']:
        issues.append('Missing publish date')
    if not post.get('author'):
        issues.append('Missing author')
    if not post.get('dateModified'):
        issues.append('Missing dateModified')
    if not post.get('metaTitle'):
        issues.append('Missing metaTitle')
    if not post.get('metaDescription'):
        issues.append('Missing metaDescription')
    
    return {
        'passed': len(issues) == 0,
        'issues': issues
    }


# ── Step 4: Run and report ──────────────────────────────────────
report_parts = []
failing_posts = []

for slug in to_check:
    post = posts_dict[slug]
    
    tfidf = check_tfidf(post)
    entities = check_entities(post)
    pillar = check_pillar_cluster(post)
    aeo = check_aeo_geo(post)
    internal = check_internal_links(post)
    schema = check_schema(post)
    
    passed_all = all([tfidf['passed'], entities['passed'], pillar['any_pillar_link'], aeo['passed'], internal['passed'], schema['passed']])
    
    def s(p): return '✅' if p else '❌'
    
    missing_ent = ', '.join(entities['missing']) if not entities['passed'] else 'None'
    
    section = f"""## Post: {slug}
| Check | Status | Details |
|-------|--------|---------|
| TF-IDF: `{tfidf['keyword']}` | {s(tfidf['passed'])} | {tfidf['detail']} |
| Entities | {s(entities['passed'])} | Missing: {missing_ent} |
| Pillar: {pillar['matched_pillar'] or 'unknown'} | {s(pillar['any_pillar_link'])} | {'Links to: ' + ', '.join(pillar['linked_pillars']) if pillar['linked_pillars'] else 'No pillar link'} |
| AEO/GEO | {s(aeo['passed'])} | {aeo['count']} question headings (need ≥ 2) |
| Internal Links | {s(internal['passed'])} | {internal['total']} total ({internal['blog']} blog, {internal['locations']} loc, {internal['services']} svc, {internal['industries']} ind, {internal['other']} other) |
| Schema Ready | {s(schema['passed'])} | {'All set' if schema['passed'] else 'Issues: ' + ', '.join(schema['issues'])} |"""

    if not passed_all:
        fixes = []
        if not tfidf['passed']:
            fixes.append(f"• **TF-IDF**: '{tfidf['keyword']}' only appears {tfidf['count']}x (need ≥ 5). Add more natural occurrences.")
        if not entities['passed']:
            fixes.append(f"• **Entities**: Add missing: {', '.join(entities['missing'])}.")
        if not pillar['any_pillar_link'] and pillar['matched_pillar']:
            fixes.append(f"• **Pillar Link**: Add link to pillar page for '{pillar['matched_pillar']}'.")
        if not aeo['passed']:
            fixes.append(f"• **AEO/GEO**: Add {2 - aeo['count']} more question-based headings (How/What/Why/etc.).")
        if not internal['passed']:
            fixes.append(f"• **Internal Links**: Add {3 - internal['total']} more internal links (blog/services/locations).")
        if not schema['passed']:
            for iss in schema['issues']:
                fixes.append(f"• **Schema**: {iss}")
        
        section += "\n\n### ⚠️ Fix instructions:\n" + "\n".join(fixes)
        failing_posts.append(slug)
    else:
        section += "\n\n### ✅ All checks passed"
    
    report_parts.append(section)

# Summary
now = subprocess.run(['date', '-u'], capture_output=True, text=True).stdout.strip()
summary = f"""# 🏗️ Content Framework Enforcement Report
**Project:** kanokmiah.com.bd
**Run:** {now}
**Period:** Last 48 hours
**Posts modified (detected):** {len(modified_slugs)}
**Posts checked:** {len(to_check)}
**Status:** {'✅ All checks passed across all monitored posts' if not failing_posts else f'❌ {len(failing_posts)} posts need attention'}

"""

print(summary)
for s in report_parts:
    print(s)
    print("---")
