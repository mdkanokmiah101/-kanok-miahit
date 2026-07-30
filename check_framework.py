#!/usr/bin/env python3
"""Content Framework Enforcer for kanokmiah.com.bd"""

import re
import json
import sys

# List of slugs to check (from git diff HEAD~2 HEAD)
AFFECTED_SLUGS = [
    "ai-seo-2026-dhaka-experts-optimize-google-ai-chatgpt",
    "das-taxis-scotland-seo-case-study",
    "dhaka-apparels-seo-case-study",
    "google-business-profile-optimization-guide-bangladesh",
    "hiring-seo-expert-dhaka-better-roi-than-paid-ads",
    "how-to-choose-best-seo-expert-dhaka-15-things",
    "landlord-certificates-seo-case-study",
    "link-building-strategies-bangladesh-market",
    "locksmith-dundee-seo-case-study",
    "mir-cement-seo-case-study",
    "mobile-seo-optimization-bangladesh-mobile-first-era",
    "morethanpanel-seo-case-study",
    "seo-case-study-dhaka-businesses-increased-organic-traffic",
    "seo-expert-vs-seo-agency-dhaka-which-is-right",
    "seo-garments-textile-industry-b2b-lead-generation",
    "smmgen-seo-case-study",
    "smmsun-seo-case-study",
    "stealth-windshield-repairs-seo-case-study",
    "top-10-seo-mistakes-dhaka-businesses-fix",
    "watchzonebd-seo-case-study",
    "what-does-seo-expert-do-guide-business-owners",
    "why-md-kanok-miah-is-the-best-seo-expert-in-dhaka-bangladesh",
]

def extract_posts(filepath):
    """Parse data.js and extract post objects as dicts."""
    with open(filepath, 'r') as f:
        content = f.read()
    
    posts = []
    # Find each post object
    # Pattern: { slug: "...", ... content: `...` }
    
    # We'll parse line by line
    lines = content.split('\n')
    in_post = False
    post_lines = []
    brace_depth = 0
    in_template_literal = False
    
    for line in lines:
        stripped = line.strip()
        
        # Track template literal boundaries (backtick content)
        backtick_count = stripped.count('`')
        if backtick_count % 2 == 1:
            in_template_literal = not in_template_literal
        
        if stripped.startswith('{') and not in_template_literal:
            in_post = True
            post_lines = [line]
            brace_depth = stripped.count('{') - stripped.count('}')
            continue
        
        if in_post:
            post_lines.append(line)
            brace_depth += stripped.count('{') - stripped.count('}')
            # Also track brace depth inside template literals? No - braces inside ` don't count
            if brace_depth <= 0 and not in_template_literal and stripped.rstrip(',').endswith('}'):
                # Check if this looks like a complete post
                post_text = '\n'.join(post_lines)
                posts.append(post_text)
                in_post = False
                post_lines = []
    
    # Parse each post text into a dict
    result = {}
    for post_text in posts:
        slug_m = re.search(r'slug:\s*"([^"]+)"', post_text)
        if slug_m:
            slug = slug_m.group(1)
            if slug in AFFECTED_SLUGS:
                title_m = re.search(r'title:\s*"([^"]+)"', post_text)
                date_m = re.search(r'date:\s*"([^"]+)"', post_text)
                excerpt_m = re.search(r'excerpt:\s*"([^"]+)"', post_text, re.DOTALL)
                tags_m = re.search(r'tags:\s*\[([^\]]+)\]', post_text)
                content_m = re.search(r'content:\s*`([\s\S]*?)`\s*,?\s*\}', post_text)
                date_mod_m = re.search(r'dateModified:\s*"([^"]+)"', post_text)
                
                # Extract tags
                tags = []
                if tags_m:
                    tag_str = tags_m.group(1)
                    tags = re.findall(r'"([^"]+)"', tag_str)
                
                # Extract content
                content = ""
                if content_m:
                    content = content_m.group(1)
                else:
                    # Try alternate pattern
                    idx = post_text.find('content: `')
                    if idx >= 0:
                        rest = post_text[idx + 9:]
                        # Find closing backtick followed by optional comma and }
                        # Need to track nested backticks (escaped \`)
                        depth = 0
                        parts = []
                        for c in rest:
                            if c == '`' and (not parts or parts[-1] != '\\'):
                                depth += 1
                                if depth == 2:
                                    break
                            parts.append(c)
                        content = ''.join(parts[:-1])  # remove the closing backtick
                
                result[slug] = {
                    'title': title_m.group(1) if title_m else '',
                    'date': date_m.group(1) if date_m else '',
                    'excerpt': excerpt_m.group(1) if excerpt_m else '',
                    'tags': tags,
                    'content': content,
                    'dateModified': date_mod_m.group(1) if date_mod_m else '',
                }
    
    return result


def check_tfidf(post):
    """Check primary keyword coverage."""
    title = post['title']
    content = post['content']
    
    # Extract first meaningful noun phrase from title
    # Remove common stop words and take first meaningful word(s)
    title_lower = title.lower()
    # Strip trailing/leading fluff
    # Common patterns in titles: "Complete X Guide", "X Tips", "How to X", "X for Y", "Why X", "X vs Y"
    # Take the first significant keyword
    stop_patterns = [
        r'^(complete|ultimate|essential|top|best|professional|expert)\s+(.+?)(\s+(guide|tips|strategies|checklist|techniques|mistakes|ways|things|benefits|steps).*)?$',
        r'^how to (.+?)(\s+.*)?$',
        r'^what does (a|an|the)?\s*(.+?)\s+(do|mean)(\s+.*)?$',
        r'^why (.+?)(\s+.*)?$',
        r'^(.+?)\s+vs\s+(.+?)(\s+.*)?$',
        r'^(.+?)(\s+guide|\s+checklist|\s+tips|\s+strategies|\s+optimization|\s+marketing|\s+seo)(\s+.*)?$',
    ]
    
    keyword = None
    for pattern in stop_patterns:
        m = re.match(pattern, title_lower)
        if m:
            groups = [g for g in m.groups() if g]
            if groups:
                keyword = groups[0].strip()
                break
    
    if not keyword:
        # Fall back to first 1-3 words
        words = title_lower.split()[:3]
        keyword = ' '.join(words)
    
    # Clean keyword
    keyword = keyword.strip(':,;.!?()-')
    
    # Count occurrences in content (case insensitive)
    count = len(re.findall(re.escape(keyword), content.lower()))
    
    # Also count if keyword is a multi-word phrase, check individual significant words
    keyword_words = keyword.split()
    if len(keyword_words) > 2:
        # Check the core 2-word phrase
        core = ' '.join(keyword_words[:2])
        core_count = len(re.findall(re.escape(core), content.lower()))
        count = max(count, core_count)
    
    return keyword, count


def check_entities(post):
    """Check semantic entity coverage."""
    content_lower = post['content'].lower()
    title = post['title']
    tags = post['tags']
    
    expected_entities = {
        'location_dhaka': ['dhaka'],
        'location_bangladesh': ['bangladesh', 'bangladeshi'],
        'service_seo': ['seo', 'search engine optimization'],
        'service_local_seo': ['local seo'],
    }
    
    # Add tag-specific entities
    tag_lower = [t.lower() for t in tags]
    if 'case study' in tag_lower or 'seo case study' in tag_lower:
        expected_entities['service_case_study'] = ['case study']
    
    if any('ai' in t for t in tag_lower):
        expected_entities['service_ai'] = ['ai', 'artificial intelligence', 'generative engine']
    
    if any('geo' in t for t in tag_lower) or 'geo' in tag_lower:
        expected_entities['service_geo'] = ['geo', 'generative engine optimization']
    
    if any('ecommerce' in t for t in tag_lower) or 'ecommerce' in tag_lower:
        expected_entities['service_ecommerce'] = ['ecommerce', 'e-commerce', 'online store']
    
    if any('technical' in t for t in tag_lower):
        expected_entities['service_technical'] = ['technical seo']
    
    # Check for location entities from title
    for loc in ['dhaka', 'chittagong', 'sylhet', 'gulshan', 'banani', 'dhanmondi', 'uttara', 'mirpur', 'motijheel', 'farmgate']:
        if loc in title.lower():
            expected_entities[f'location_{loc}'] = [loc]
    
    found = {}
    missing = {}
    
    for entity_name, keywords in expected_entities.items():
        entity_found = False
        for kw in keywords:
            if kw in content_lower:
                entity_found = True
                break
        if entity_found:
            found[entity_name] = True
        else:
            missing[entity_name] = keywords
    
    return found, missing


def check_pillar_link(post):
    """Check pillar-cluster alignment."""
    content = post['content']
    tags = post['tags']
    
    tag_lower = [t.lower() for t in tags]
    
    # Map tags to pillar pages
    pillar_map = {
        'local seo': '/services/local-seo',
        'technical seo': '/services/technical-seo',
        'on-page seo': '/services/on-page-seo',
        'seo guide': '/',
        'bangladesh seo': '/',
        'case study': '/case-studies',
        'seo case study': '/case-studies',
        'geo': '/services/geo-aeo-services',
        'aeo': '/services/geo-aeo-services',
        'ecommerce seo': '/services/ecommerce-seo',
        'content marketing': '/services/content-marketing',
        'seo audit': '/services/technical-seo',
        'link building': '/services/link-building',
        'seo consultant': '/',
        'seo expert': '/',
    }
    
    linked_pillars = set()
    for tag in tag_lower:
        if tag in pillar_map:
            pillar_url = pillar_map[tag]
            # Check if pillar URL is linked
            if pillar_url in content:
                linked_pillars.add(pillar_url)
    
    # Also check /services/ links in general as pillar links
    service_links = re.findall(r'/services/[a-z0-9-]+', content)
    for sl in service_links:
        linked_pillars.add(sl)
    
    # Check for homepage link as ultimate pillar
    has_homepage_link = bool(re.search(r'\]\(/\)', content) or re.search(r'\[.*\]\(https?://kanokmiah\.com\.bd/?\)', content))
    if has_homepage_link:
        linked_pillars.add('/')
    
    return list(linked_pillars), len(linked_pillars) == 0


def check_aeo_geo(post):
    """Check AEO/GEO optimization - question-based headings."""
    content = post['content']
    
    # Count headings that start with question words
    question_heading_pattern = r'^#{2,4}\s+(How|What|Why|When|Where|Can|Do|Is|Are|Does|Who|Which)\b'
    question_headings = re.findall(question_heading_pattern, content, re.MULTILINE)
    
    return len(question_headings), question_headings


def check_internal_links(post):
    """Check internal linking."""
    content = post['content']
    
    # Count markdown-style internal links
    # Internal = links to /, /blog/, /services/, /locations/, /case-studies/, /about/
    internal_link_pattern = r'\]\((/[a-z0-9-/]*)\)'
    all_links = re.findall(internal_link_pattern, content)
    
    # Filter for internal site links (not external, not anchors-only)
    internal_links = [l for l in all_links if l.startswith('/') and len(l) > 1]
    
    # Deduplicate
    unique_links = list(set(internal_links))
    
    return len(unique_links), unique_links


def check_schema(post):
    """Check schema readiness - title, excerpt, date."""
    missing_fields = []
    
    if not post['title']:
        missing_fields.append('title')
    if not post['excerpt']:
        missing_fields.append('excerpt')
    if not post['date']:
        missing_fields.append('date')
    if not post['dateModified']:
        missing_fields.append('dateModified')
    
    is_ready = len(missing_fields) == 0
    return is_ready, missing_fields


def run_checks(post):
    """Run all framework checks on a single post."""
    results = {}
    
    # A. TF-IDF
    keyword, count = check_tfidf(post)
    results['tfidf'] = {
        'keyword': keyword,
        'count': count,
        'passed': count >= 5,
    }
    
    # B. Entities
    found, missing = check_entities(post)
    results['entities'] = {
        'found': list(found.keys()),
        'missing': list(missing.keys()),
        'passed': len(missing) == 0,
    }
    
    # C. Pillar Link
    linked_pillars, no_link = check_pillar_link(post)
    results['pillar'] = {
        'linked_pillars': linked_pillars,
        'passed': not no_link,
    }
    
    # D. AEO/GEO
    q_count, q_headings = check_aeo_geo(post)
    results['aeo'] = {
        'count': q_count,
        'headings': q_headings,
        'passed': q_count >= 2,
    }
    
    # E. Internal Links
    link_count, links = check_internal_links(post)
    results['internal_links'] = {
        'count': link_count,
        'links': links,
        'passed': link_count >= 3,
    }
    
    # F. Schema
    is_ready, missing_schema = check_schema(post)
    results['schema'] = {
        'ready': is_ready,
        'missing': missing_schema,
    }
    
    return results, keyword


def generate_report(slug, post, results, keyword):
    """Generate formatted report."""
    r = results
    
    tfidf_status = "✅" if r['tfidf']['passed'] else "❌"
    entities_status = "✅" if r['entities']['passed'] else "❌"
    pillar_status = "✅" if r['pillar']['passed'] else "❌"
    aeo_status = "✅" if r['aeo']['passed'] else "❌"
    il_status = "✅" if r['internal_links']['passed'] else "❌"
    schema_status = "✅" if r['schema']['ready'] else "❌"
    
    lines = []
    lines.append(f"## Post: {slug}")
    lines.append(f"**Title:** {post['title']}")
    lines.append(f"**Date:** {post['date']} | **Tags:** {', '.join(post['tags'])}")
    lines.append("")
    lines.append("| Check | Status | Details |")
    lines.append("|-------|--------|---------|")
    lines.append(f"| TF-IDF: `{keyword}` | {tfidf_status} | {r['tfidf']['count']} occurrences {'✅' if r['tfidf']['passed'] else '❌ need ≥5'} |")
    
    if r['entities']['missing']:
        lines.append(f"| Entities | {entities_status} | Missing: {', '.join(r['entities']['missing'])} |")
    else:
        lines.append(f"| Entities | {entities_status} | All key entities present |")
    
    if r['pillar']['passed']:
        lines.append(f"| Pillar Link | {pillar_status} | Links to: {', '.join(r['pillar']['linked_pillars'])} |")
    else:
        lines.append(f"| Pillar Link | {pillar_status} | No pillar page link found |")
    
    lines.append(f"| AEO/GEO | {aeo_status} | {r['aeo']['count']} question headings {'✅' if r['aeo']['passed'] else '❌ need ≥2'} |")
    lines.append(f"| Internal Links | {il_status} | {r['internal_links']['count']} unique internal links {'✅' if r['internal_links']['passed'] else '❌ need ≥3'} |")
    
    if r['schema']['ready']:
        lines.append(f"| Schema Ready | {schema_status} | All fields set |")
    else:
        lines.append(f"| Schema Ready | {schema_status} | Missing: {', '.join(r['schema']['missing'])} |")
    
    # Fix instructions
    fixes = []
    if not r['tfidf']['passed']:
        fixes.append(f"- 🔴 **TF-IDF Thin:** Add more occurrences of `{keyword}` (currently {r['tfidf']['count']}, need ≥5). Mention the keyword naturally in additional sections.")
    if r['entities']['missing']:
        for ent in r['entities']['missing']:
            fixes.append(f"- 🔴 **Missing Entity:** Add `{ent}` reference(s) to the content.")
    if not r['pillar']['passed']:
        pillar_suggestion = '/services/local-seo'
        if any('technical' in t.lower() for t in post['tags']):
            pillar_suggestion = '/services/technical-seo'
        elif any('case study' in t.lower() for t in post['tags']):
            pillar_suggestion = '/case-studies'
        elif any('ecommerce' in t.lower() for t in post['tags']):
            pillar_suggestion = '/services/ecommerce-seo'
        fixes.append(f"- 🔴 **No Pillar Link:** Add a contextual link to the pillar page (`{pillar_suggestion}`) from within the content.")
    if not r['aeo']['passed']:
        fixes.append(f"- 🔴 **AEO/GEO Low:** Add more question-based headings (currently {r['aeo']['count']}, need ≥2). E.g., \"## What is X?\", \"## How does Y work in Bangladesh?\")")
    if not r['internal_links']['passed']:
        fixes.append(f"- 🔴 **Internal Links Sparse:** Add more internal links (currently {r['internal_links']['count']}, need ≥3). Link to services, other blog posts, or location pages.")
    if not r['schema']['ready']:
        fixes.append(f"- 🔴 **Schema Incomplete:** Missing fields: {', '.join(r['schema']['missing'])}. Add these to the post metadata.")
    
    if fixes:
        lines.append("")
        lines.append("### Fix Instructions:")
        for f in fixes:
            lines.append(f)
    
    lines.append("---")
    return '\n'.join(lines)


def main():
    posts = extract_posts('src/app/blog/data.js')
    
    print("# 📋 Content Framework Enforcer Report")
    print(f"**Date:** 2026-07-28 | **Scope:** 2 recent commits (heading cleanup + internal linking audit)")
    print(f"**Posts checked:** {len(posts)}/{len(AFFECTED_SLUGS)} found in data.js")
    print("")
    
    missing_slugs = [s for s in AFFECTED_SLUGS if s not in posts]
    if missing_slugs:
        print(f"⚠️ **Warning:** {len(missing_slugs)} slugs from diff not extractable (may be edge cases): {missing_slugs}")
        print("")
    
    all_passed = True
    total_checks = 0
    passed_checks = 0
    
    for slug, post in sorted(posts.items()):
        results, keyword = run_checks(post)
        report = generate_report(slug, post, results, keyword)
        print(report)
        
        # Count pass/fail
        checks = [results['tfidf']['passed'], results['entities']['passed'], 
                  results['pillar']['passed'], results['aeo']['passed'],
                  results['internal_links']['passed'], results['schema']['ready']]
        total_checks += len(checks)
        passed_checks += sum(checks)
        
        if not all(checks):
            all_passed = False
    
    # Summary
    print("")
    print("## 📊 Summary")
    print(f"| Metric | Value |")
    print(f"|--------|-------|")
    print(f"| Posts Checked | {len(posts)} |")
    print(f"| Checks Passed | {passed_checks}/{total_checks} ({passed_checks*100//total_checks if total_checks else 0}%) |")
    print(f"| Overall Status | {'✅ ALL PASSED' if all_passed else '❌ SOME CHECKS FAILED'} |")
    
    if not all_passed:
        print("")
        print("### 🔧 Recommended Next Actions")
        print("1. Run `silo:process` on failing posts to apply pillar links and heading fixes")
        print("2. For TF-IDF fails: add keyword-rich sections or FAQ content")
        print("3. For missing entities: ensure location (Dhaka/Bangladesh) and service names are present")
        print("4. For AEO/GEO: add question-based H2/H3s targeting voice/featured snippet queries")
    
    return 0 if all_passed else 1


if __name__ == '__main__':
    sys.exit(main())
