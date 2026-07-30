#!/usr/bin/env python3
"""
Content Framework Enforcer for kanokmiah.com.bd — v2
Reads blog/data.js, runs 6 checks on specified post slugs.
"""

import re
import sys

DATA_FILE = '/root/kanok-miahit/src/app/blog/data.js'

MODIFIED_SLUGS = [
    "mobile-seo-optimization-bangladesh-mobile-first-era",
    "why-md-kanok-miah-is-the-best-seo-expert-in-dhaka-bangladesh",
    "landlord-certificates-seo-case-study",
    "das-taxis-scotland-seo-case-study",
    "morethanpanel-seo-case-study",
    "smmgen-seo-case-study",
    "smmsun-seo-case-study",
    "mir-cement-seo-case-study",
    "dhaka-apparels-seo-case-study",
    "stealth-windshield-repairs-seo-case-study",
    "how-to-choose-best-seo-expert-dhaka-15-things",
    "seo-expert-vs-seo-agency-dhaka-which-is-right",
    "top-10-seo-mistakes-dhaka-businesses-fix",
    "what-does-seo-expert-do-guide-business-owners",
    "seo-case-study-dhaka-businesses-increased-organic-traffic",
    "hiring-seo-expert-dhaka-better-roi-than-paid-ads",
    "ai-seo-2026-dhaka-experts-optimize-google-ai-chatgpt",
    "link-building-strategies-bangladesh-market",
    "seo-garments-textile-industry-b2b-lead-generation",
    "google-business-profile-optimization-guide-bangladesh",
]

# ── Post parsing ──────────────────────────────────────────────────────────

def parse_posts(filepath):
    """Parse the JS array of post objects from data.js"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    start = content.find('[')
    end = content.rfind(']')
    if start == -1 or end == -1:
        print("ERROR: Could not find posts array"); sys.exit(1)
    
    array_content = content[start:end+1]
    
    # Split top-level objects by tracking brace depth
    posts_raw = []
    depth = 0
    current = []
    in_str = False
    str_char = None
    escape = False
    
    for ch in array_content:
        if escape:
            current.append(ch); escape = False; continue
        if ch == '\\' and in_str:
            current.append(ch); escape = True; continue
        if ch in ('"', "'", '`') and in_str and ch == str_char:
            in_str = False; current.append(ch); continue
        if ch in ('"', "'", '`') and not in_str:
            in_str = True; str_char = ch; current.append(ch); continue
        if not in_str:
            if ch == '{': depth += 1
            elif ch == '}': depth -= 1
            elif ch == ',' and depth == 0:
                posts_raw.append(''.join(current)); current = []; continue
        current.append(ch)
    if current:
        remaining = ''.join(current).strip().rstrip(',').strip()
        if remaining and remaining not in ('[', ']', ''):
            posts_raw.append(remaining)
    
    posts = []
    for raw in posts_raw:
        raw = raw.strip().strip(',').strip()
        if not raw or raw in ('[', ']', ''):
            continue
        
        post = {}
        m = re.search(r'slug:\s*"([^"]+)"', raw)
        if not m: continue
        post['slug'] = m.group(1)
        
        m = re.search(r'title:\s*"([^"]+)"', raw)
        post['title'] = m.group(1) if m else ''
        
        m = re.search(r'date:\s*"([^"]+)"', raw)
        post['date'] = m.group(1) if m else ''
        
        m = re.search(r'excerpt:\s*(`|")(.*?)\1', raw, re.DOTALL)
        if m:
            post['excerpt'] = m.group(2).replace('\\n', '\n').replace('\\"', '"')
        else:
            post['excerpt'] = ''
        
        m = re.search(r'tags:\s*\[(.*?)\]', raw, re.DOTALL)
        if m:
            tags_str = m.group(1)
            post['tags'] = re.findall(r'"([^"]+)"', tags_str)
        else:
            post['tags'] = []
        
        # Content: everything from `content:` until the closing backtick
        m = re.search(r'content:\s*(`)(.*?)\1\s*,?\s*(\n|$)', raw, re.DOTALL)
        if m:
            post['content'] = m.group(2).replace('\\`', '`')
        else:
            # Try double-quoted content
            m = re.search(r'content:\s*(")(.*?)\1\s*,?\s*(\n|$)', raw, re.DOTALL)
            if m:
                post['content'] = m.group(2).replace('\\n', '\n').replace('\\"', '"')
            else:
                post['content'] = ''
        
        posts.append(post)
    
    return posts


# ── Keyword extraction ────────────────────────────────────────────────────

def extract_primary_keyword(title, slug, tags):
    """Extract a meaningful primary keyword from the post."""
    title_lower = title.lower().strip()
    
    # For case studies: use the brand/client name
    if 'case study' in slug.lower():
        # Remove "SEO Case Study/Case Study" suffix
        m = re.match(r'^(.+?)\s+(SEO Case Study|Case Study|SEO)', title, re.IGNORECASE)
        if m:
            brand = m.group(1).strip()
            # Take first 2-3 meaningful words
            words = brand.split()
            # Remove leading small words
            while words and words[0].lower() in ('the', 'a', 'an', 'how', 'why'):
                words.pop(0)
            return ' '.join(words[:2]).lower()
        # Fallback: take meaningful parts
        words = title_lower.split()
        # Filter out very common words
        stop = {'the', 'a', 'an', 'from', 'to', 'in', 'of', 'for', 'and', 'how', 'why', 'what', 'seo'}
        meaningful = [w for w in words if w not in stop][:2]
        return ' '.join(meaningful) if meaningful else slug.split('-')[0]
    
    # For guide/tutorial posts: use the main topic
    # Strip prefixes like "Complete", "Ultimate", "Top", "How to", "What is", "Why"
    cleaned = title_lower
    prefixes = [
        r'^complete\s+', r'^ultimate\s+', r'^top\s+\d+\s+', r'^how\s+to\s+',
        r'^what\s+(does|is)\s+', r'^why\s+', r'^best\s+', r'^guide\s+to\s+',
        r'^tips\s+for\s+',
    ]
    for p in prefixes:
        cleaned = re.sub(p, '', cleaned)
    
    # Remove everything after: for, in, of, vs, —, :
    for sep in [' vs ', ' — ', ' : ', ' - ', ' for ', ' in ', ' of ', ': ']:
        idx = cleaned.find(sep)
        if idx > 0:
            cleaned = cleaned[:idx]
    
    # Take first 2-3 meaningful words
    words = cleaned.split()
    stop = {'the', 'a', 'an', 'and', 'or', 'to', 'for', 'in', 'of', 'your', 'that', 'this',
            'from', 'with', 'our', 'its', 'their', 'all', 'is', 'are', 'be', 'has', 'have'}
    meaningful = [w for w in words if w not in stop and len(w) > 1]
    
    if meaningful:
        # Also try the whole slug for better keyword
        # For specific searches, tags often have the real keyword
        tag_keywords = [t.lower() for t in tags if len(t) > 3]
        for tk in tag_keywords:
            # Check if tag appears in content as a primary topic
            if tk not in ('case study', 'seo', 'digital marketing', 'bangladesh'):
                pass  # Prefer tag-derived keywords
        
        return ' '.join(meaningful[:3])
    
    # Last resort: use first meaningful slug part
    return slug.split('-')[0]


# ── Check functions ───────────────────────────────────────────────────────

def check_tfidf(content, keyword):
    """Check keyword frequency (≥5 occurrences)."""
    if not keyword:
        return False, 0
    keyword_lower = keyword.lower().strip()
    content_lower = content.lower()
    count = content_lower.count(keyword_lower)
    return count >= 5, count


def check_entities(content, slug):
    """Check required entities are present."""
    content_lower = content.lower()
    missing = []
    
    # Location entities
    if 'dhaka' not in content_lower:
        missing.append('Dhaka')
    if 'bangladesh' not in content_lower:
        missing.append('Bangladesh')
    
    # Service type — most posts should mention 'seo' generically
    if 'seo' not in content_lower:
        missing.append('SEO service term')
    
    # For case studies about foreign clients (UK, Scotland), Dhaka/Bangladesh may not be relevant
    foreign_clients = ['locksmith dundee', 'das taxis scotland', 'landlord certificates uk',
                      'stealth windshield repairs']
    is_foreign = any(term in slug.lower() for term in foreign_clients)
    
    if is_foreign:
        # Remove location requirements for foreign case studies
        missing = [m for m in missing if m not in ('Dhaka', 'Bangladesh')]
    
    return missing


def check_pillar_link(content, slug, tags):
    """Check for pillar page links."""
    content_lower = content.lower()
    
    # Known pillar/authority pages
    pillar_pages = [
        '/blog/complete-seo-guide-bangladesh-businesses-2026',
        '/services/local-seo',
        '/services/technical-seo',
        '/services/on-page-seo',
        '/services/ecommerce-seo',
        '/services/geo-ai-search',
        '/blog/seo-case-study-dhaka-businesses-increased-organic-traffic',
    ]
    
    linked = [p for p in pillar_pages if p in content_lower]
    
    # Also check for tag-relevant pillar
    tag_lower = [t.lower() for t in tags]
    relevant_pillars = []
    for t in tag_lower:
        if 'local seo' in t or 'local' in t:
            relevant_pillars.append('/services/local-seo')
        if 'technical seo' in t:
            relevant_pillars.append('/services/technical-seo')
        if 'ecommerce' in t or 'e-commerce' in t:
            relevant_pillars.append('/services/ecommerce-seo')
        if 'case study' in t:
            relevant_pillars.append('/blog/seo-case-study-dhaka-businesses-increased-organic-traffic')
    
    if linked:
        return linked
    return None


def count_question_headings(content):
    """Count question-based headings and question sentences."""
    count = 0
    for line in content.split('\n'):
        line = line.strip()
        # Markdown headings with question words
        if line.startswith('##') or line.startswith('###'):
            if re.match(r'^#{2,3}\s+(How|What|Why|When|Where|Can|Do|Is|Are|Should|Which)\b', line, re.IGNORECASE):
                count += 1
        # Standalone question sentences
        elif line.endswith('?') and len(line) > 15 and len(line) < 250:
            if re.match(r'^(How|What|Why|When|Where|Can|Do|Is|Are|Should|Which)\b', line, re.IGNORECASE):
                count += 1
    return count


def count_internal_links(content):
    """Count unique internal links."""
    links = re.findall(r'\((/[^)]+)\)', content)
    # Filter to internal site links
    internal = []
    for link in links:
        if link in ('#', ''):
            continue
        if link.startswith(('/blog/', '/services/', '/locations/', '/industries/', '/')):
            if link not in internal:
                internal.append(link)
    # Filter out external-looking links (with protocol)
    internal = [l for l in internal if not l.startswith(('http://', 'https://', '//'))]
    # Count only unique
    unique = list(set(internal))
    return len(unique) >= 3, len(unique), unique


def check_schema_ready(post):
    """Check if post has title, excerpt, date."""
    missing = []
    if not post.get('title'):
        missing.append('title')
    if not post.get('excerpt'):
        missing.append('excerpt')
    if not post.get('date'):
        missing.append('date')
    return (not missing), missing


# ── Report generation ────────────────────────────────────────────────────

def generate_report(results):
    lines = []
    
    for slug, checks in results.items():
        title = checks.get('title', '')
        tags_str = ', '.join(checks.get('tags', []))
        
        lines.append(f"## Post: {slug}")
        lines.append(f"**Title:** {title}")
        lines.append(f"**Tags:** {tags_str}")
        lines.append("")
        lines.append("| Check | Status | Details |")
        lines.append("|-------|--------|---------|")
        
        # --- TF-IDF ---
        t = checks.get('tfidf', {})
        kw = t.get('keyword', 'N/A')
        tfidf_passed = t.get('passed', False)
        tfidf_count = t.get('count', 0)
        tfidf_status = '✅' if tfidf_passed else '❌'
        tfidf_detail = f"Keyword: '{kw}' — {tfidf_count} occurrences" if kw else "Could not extract keyword"
        lines.append(f"| TF-IDF: {kw} | {tfidf_status} | {tfidf_detail} |")
        
        # --- Entities ---
        e = checks.get('entities', {})
        e_missing = e.get('missing', [])
        e_status = '✅' if not e_missing else '❌'
        e_detail = f"Missing: {', '.join(e_missing)}" if e_missing else "All key entities present"
        lines.append(f"| Entities | {e_status} | {e_detail} |")
        
        # --- Pillar ---
        p = checks.get('pillar', {})
        p_linked = p.get('linked_pillars', [])
        p_status = '✅' if p_linked else '❌'
        p_detail = f"Links to: {', '.join(p_linked[:3])}" if p_linked else "No pillar link found"
        lines.append(f"| Pillar Link | {p_status} | {p_detail} |")
        
        # --- AEO/GEO ---
        a = checks.get('aeo_geo', {})
        a_passed = a.get('passed', False)
        a_count = a.get('count', 0)
        a_status = '✅' if a_passed else '❌'
        lines.append(f"| AEO/GEO | {a_status} | {a_count} question headings/Qs |")
        
        # --- Internal Links ---
        i = checks.get('internal_links', {})
        i_passed = i.get('passed', False)
        i_count = i.get('count', 0)
        i_status = '✅' if i_passed else '❌'
        i_links = i.get('links', [])
        i_detail = f"{i_count} total: {', '.join(i_links[:5])}" if i_links else "None"
        if len(i_links) > 5:
            i_detail += f" (+{len(i_links)-5} more)"
        lines.append(f"| Internal Links | {i_status} | {i_detail} |")
        
        # --- Schema ---
        s = checks.get('schema', {})
        s_passed = s.get('passed', False)
        s_missing = s.get('missing', [])
        s_status = '✅' if s_passed else '❌'
        s_detail = "All fields set" if s_passed else f"Missing: {', '.join(s_missing)}"
        lines.append(f"| Schema Ready | {s_status} | {s_detail} |")
        
        # --- Fix instructions ---
        lines.append("")
        lines.append("### Fix instructions:")
        fixes = []
        
        if not tfidf_passed and kw:
            fixes.append(f"- **TF-IDF:** Add more occurrences of '{kw}' (currently {tfidf_count}, need ≥5)")
        if e_missing:
            fixes.append(f"- **Entities:** Add mentions of: {', '.join(e_missing)}")
        if not p_linked:
            fixes.append("- **Pillar Link:** Add a link to the relevant pillar page (e.g., /blog/complete-seo-guide-bangladesh-businesses-2026 or /services/local-seo)")
        if not a_passed:
            fixes.append(f"- **AEO/GEO:** Add more question-based headings/Qs (currently {a_count}, need ≥2)")
        if not i_passed:
            fixes.append(f"- **Internal Links:** Add more internal links (currently {i_count}, need ≥3)")
        if not s_passed:
            fixes.append(f"- **Schema:** Set missing fields: {', '.join(s_missing)}")
        
        if fixes:
            lines.extend(fixes)
        else:
            lines.append("All checks pass — no fixes needed.")
        lines.append("")
    
    return '\n'.join(lines)


# ── Main ──────────────────────────────────────────────────────────────────

def main():
    print("Parsing posts from data.js...", file=sys.stderr)
    posts = parse_posts(DATA_FILE)
    slug_map = {p['slug']: p for p in posts}
    
    results = {}
    
    for slug in MODIFIED_SLUGS:
        if slug not in slug_map:
            print(f"WARNING: Slug '{slug}' not found", file=sys.stderr)
            continue
        
        post = slug_map[slug]
        title = post.get('title', '')
        content = post.get('content', '')
        tags = post.get('tags', [])
        
        print(f"Checking: {slug}...", file=sys.stderr)
        
        checks = {'title': title, 'tags': tags}
        
        # A. TF-IDF
        keyword = extract_primary_keyword(title, slug, tags)
        tfidf_passed, tfidf_count = check_tfidf(content, keyword)
        checks['tfidf'] = {'keyword': keyword, 'passed': tfidf_passed, 'count': tfidf_count}
        
        # B. Entities
        missing = check_entities(content, slug)
        checks['entities'] = {'missing': missing}
        
        # C. Pillar
        linked = check_pillar_link(content, slug, tags)
        checks['pillar'] = {'linked_pillars': linked if linked else []}
        
        # D. AEO/GEO
        aeo_count = count_question_headings(content)
        checks['aeo_geo'] = {'passed': aeo_count >= 2, 'count': aeo_count}
        
        # E. Internal Links
        il_passed, il_count, il_links = count_internal_links(content)
        checks['internal_links'] = {'passed': il_passed, 'count': il_count, 'links': il_links}
        
        # F. Schema
        s_passed, s_missing = check_schema_ready(post)
        checks['schema'] = {'passed': s_passed, 'missing': s_missing}
        
        results[slug] = checks
    
    print(generate_report(results))


if __name__ == '__main__':
    main()
