#!/usr/bin/env python3
"""
Content Framework Enforcer v5 — Final
- TF-IDF uses core 2-3 word keyword (not full title phrase)
- Better flexible matching
"""
import re, json, sys, subprocess

DATA_FILE = "/root/kanok-miahit/src/app/blog/data.js"
PARSER_SCRIPT = "/root/kanok-miahit/_parse_posts.py"

ALL_CHANGED_SLUGS = sorted(set([
    "ai-seo-2026-dhaka-experts-optimize-google-ai-chatgpt",
    "content-marketing-strategy-bangladeshi-brands-seo",
    "das-taxis-scotland-seo-case-study",
    "dhaka-apparels-seo-case-study",
    "hiring-seo-expert-dhaka-better-roi-than-paid-ads",
    "how-to-choose-best-seo-expert-dhaka-15-things",
    "international-seo-bangladesh-exporters-global-buyers",
    "landlord-certificates-seo-case-study",
    "locksmith-dundee-seo-case-study",
    "mir-cement-seo-case-study",
    "mobile-seo-optimization-bangladesh-mobile-first-era",
    "morethanpanel-seo-case-study",
    "seo-case-study-dhaka-businesses-increased-organic-traffic",
    "seo-expert-vs-seo-agency-dhaka-which-is-right",
    "smmgen-seo-case-study",
    "smmsun-seo-case-study",
    "stealth-windshield-repairs-seo-case-study",
    "top-10-seo-mistakes-dhaka-businesses-fix",
    "watchzonebd-seo-case-study",
    "what-does-seo-expert-do-guide-business-owners",
    "geo-optimization-prepare-business-ai-search",
    "google-business-profile-optimization-guide-bangladesh",
    "how-to-choose-right-seo-agency-bangladesh",
    "link-building-strategies-bangladesh-market",
    "seo-garments-textile-industry-b2b-lead-generation",
    "seo-vs-google-ads-whats-best-bangladesh-businesses",
]))

LOCATIONS = ["dhaka","bangladesh","chittagong","sylhet","khulna","rajshahi","gulshan","banani","dhanmondi","uttara","motijheel","mirpur","farmgate","baridhara","bashundhara","bogura","comilla","dundee","scotland"]
SERVICES = ["local seo","technical seo","on-page seo","off-page seo","ecommerce seo","seo audit","link building","content marketing","keyword research","google maps","google business profile","seo consulting","seo services","seo expert","seo specialist","seo consultant","seo agency"]
INDUSTRIES = ["ecommerce","real estate","healthcare","medical","education","travel","tourism","restaurant","food","garment","textile","b2b","saas","startup","ngo","law firm","fitness","gym","photography","event","cleaning","automotive","transportation","locksmith","hospitality","hotel","watch","panel","taxis","windshield"]


def load_posts():
    result = subprocess.run(["python3", PARSER_SCRIPT], capture_output=True, text=True, cwd="/root/kanok-miahit")
    return json.loads(result.stdout)


def get_core_keyword(title, slug):
    """Extract the core 2-3 word keyword from title. Not the full phrase."""
    t = title.strip()
    t = re.sub(r'\s*\|.*$', '', t).strip()
    
    if "case-study" in slug:
        parts = slug.split('-')
        skip = {'seo','case','study','for','in','and','the','of','to'}
        name_parts = [p for p in parts if p not in skip and len(p) > 2]
        if name_parts:
            return ' '.join(name_parts[:3])
    
    t_lower = t.lower()
    
    # Remove leading question prefix
    t = re.sub(r'^(How to |What Is |What Does |What |Why |When |Where |Can |Do |Does |Is |Are |Should |Would |Top |The |A |An )\s*', '', t, flags=re.I)
    
    # Split on colon, pipe, em-dash — take main part
    main = re.split(r'\s*[:|]\s*', t)[0].strip()
    
    # For "X vs Y" titles — the topic is the comparison; use first meaningful entity
    vs_match = re.search(r'(.+?)\s+vs[.\s]+(.+)', main)
    if vs_match:
        first_side = vs_match.group(1).strip()
        # Take first 2 meaningful words from first side
        fw = [w for w in first_side.split() if w.lower() not in ('the','a','an','in','for','of','to','on','at','by','from','with','and','or')]
        if len(fw) >= 2:
            return ' '.join(fw[:2])
        return first_side[:20]
    
    # Get first 3-4 content words (preserving short words that are part of a phrase)
    words = main.split()
    
    # Strategy: take first 2-3 meaningful content words
    # Skip leading articles and very short words (prepositions)
    content_words = [w for w in words if w.lower() not in ('the','a','an','in','for','of','to','on','at','by','from','with','and','or','is','are','its','your')]
    
    if not content_words:
        content_words = words[:3]
    
    core = ' '.join(content_words[:3])
    
    # For "X vs Y" style titles, we already handled above
    # Ensure core is reasonable
    if len(core) > 45:
        core = ' '.join(core.split()[:2])
    
    return core


def count_tfidf(content, keyword):
    """Count keyword occurrences with flexible matching."""
    if not keyword:
        return 0
    c = content.lower()
    kw = keyword.lower().strip()
    
    # Exact phrase
    count = c.count(kw)
    if count >= 5:
        return count
    
    # Try all 2-word sliding windows from the keyword
    words = kw.split()
    if len(words) > 2:
        for i in range(len(words) - 1):
            pair = ' '.join(words[i:i+2])
            if len(pair) > 3:
                count = max(count, c.count(pair))
    
    return count


def check_tfidf(post):
    keyword = get_core_keyword(post.get('title',''), post.get('slug',''))
    count = count_tfidf(post.get('content',''), keyword)
    status = "✅" if count >= 5 else "❌"
    return {"check": "TF-IDF", "status": status, "keyword": keyword, "count": count}


def check_entities(post):
    content = post.get('content','').lower()
    title = post.get('title','').lower()
    slug = post.get('slug','')
    missing = []
    
    if not any(loc in content for loc in LOCATIONS):
        if not any(loc.replace(' ','-') in slug for loc in ['dhaka','bangladesh','chittagong','sylhet','dundee','scotland']):
            missing.append("location entities")
    if not any(svc in content for svc in SERVICES):
        missing.append("service type entities")
    if not any(ind in content for ind in INDUSTRIES):
        if not any(ind in title for ind in INDUSTRIES):
            missing.append("industry entities")
    if "case-study" in slug:
        if not re.search(r'\d+[%x×]|\d{3,}', post.get('content','')):
            missing.append("quantified results")
    
    status = "✅" if not missing else "❌"
    return {"check": "Entities", "status": status, "missing": missing or ["All present"]}


def check_pillar_link(post):
    content = post.get('content','')
    tags = [t.lower() for t in post.get('tags',[])]
    pillar_urls = ["/services/local-seo","/services/technical-seo","/services/ecommerce-seo","/services/seo-consulting-dhaka","/services/link-building","/services/content-seo","/services/seo-audit","/services/on-page-seo","/services"]
    tag_to_pillar = {
        "local seo":"/services/local-seo","technical seo":"/services/technical-seo",
        "ecommerce seo":"/services/ecommerce-seo","seo consulting":"/services/seo-consulting-dhaka",
        "seo consultant":"/services/seo-consulting-dhaka","link building":"/services/link-building",
        "content marketing":"/services/content-seo","content strategy":"/services/content-seo",
        "seo strategy":"/services/seo-audit","seo audit":"/services/seo-audit",
        "seo services":"/services","google maps":"/services/local-seo",
        "google business profile":"/services/local-seo","mobile seo":"/services/technical-seo",
        "international seo":"/services/technical-seo","b2b":"/services/technical-seo",
    }
    
    linked = [u for u in pillar_urls if u in content]
    if linked:
        status, detail = "✅", f"Links to: {', '.join(linked[:2])}"
    elif re.search(r'\(/services/[^)]*\)', content):
        status, detail = "❌", "Has service links but not pillar page"
    elif '(/)' in content:
        status, detail = "❌", "No pillar link (has homepage link)"
    else:
        status, detail = "❌", "No pillar link found"
    return {"check": "Pillar Link", "status": status, "detail": detail}


def check_aeo_geo(post):
    content = post.get('content','')
    q_starts = {'how','what','why','when','where','can','do','does','is','are','should','would','could','will','did','has','have','which','who'}
    headings = re.findall(r'^#{1,6}\s+(.+)$', content, re.MULTILINE)
    count = sum(1 for h in headings if h.strip().split()[0].lower().rstrip('?:;,') in q_starts)
    count += len(re.findall(r'\*\*([^:*]+?\?)\*\*', content))
    count += len(re.findall(r'(?:###\s+Q[.:]?\s*|(?:^|\n)\d+[.:]\s+)([^?\n]+\?)', content))
    status = "✅" if count >= 2 else "❌"
    return {"check": "AEO/GEO", "status": status, "count": count}


def check_internal_links(post):
    content = post.get('content','')
    slug = post.get('slug','')
    links = set()
    for text, path in re.findall(r'\[([^\]]+)\]\((/[^)]+)\)', content):
        if not path.startswith('http') and slug not in path:
            links.add(path)
    for link in re.findall(r'\((/(?:blog|services|locations|industries|about)[^)]*)\)', content):
        links.add(link)
    if '(/)' in content:
        links.add('/')
    count = len(links)
    status = "✅" if count >= 3 else "❌"
    return {"check": "Internal Links", "status": status, "count": count}


def check_schema(post):
    missing = []
    if not post.get('title'): missing.append("title")
    if not post.get('excerpt'): missing.append("excerpt")
    if not post.get('date'): missing.append("date")
    if not post.get('author'): missing.append("author")
    if not post.get('dateModified'): missing.append("dateModified (optional)")
    required = [m for m in missing if '(optional)' not in m]
    status = "❌" if required else "✅"
    return {"check": "Schema Ready", "status": status, "missing": missing or ["All fields set"]}


def generate_fix(results, post):
    fixes = []
    if results['tfidf']['status'] == '❌':
        fixes.append(f"- **TF-IDF**: Increase \"{results['tfidf']['keyword']}\" to ≥5 occurrences (currently {results['tfidf']['count']}). Add in headings and body.")
    if results['entities']['status'] == '❌':
        for m in results['entities']['missing']:
            if 'location' in m: fixes.append("- **Entities**: Add location references (Dhaka, Bangladesh).")
            elif 'service' in m: fixes.append("- **Entities**: Add SEO service type references.")
            elif 'industry' in m: fixes.append("- **Entities**: Add industry entities relevant to topic.")
            elif 'quantified' in m: fixes.append("- **Entities**: Add quantified results/metrics.")
            else: fixes.append(f"- **Entities**: {m}.")
    if results['pillar']['status'] == '❌':
        fixes.append("- **Pillar Link**: Add link to pillar/service page (e.g., /services/local-seo).")
    if results['aeo']['status'] == '❌':
        fixes.append(f"- **AEO/GEO**: Add ≥2 question headings (currently {results['aeo']['count']}). FAQ section recommended.")
    if results['internal']['status'] == '❌':
        fixes.append(f"- **Internal Links**: Need ≥3 links (currently {results['internal']['count']}).")
    if results['schema']['status'] == '❌':
        req = [m for m in results['schema']['missing'] if '(optional)' not in m]
        if req: fixes.append(f"- **Schema**: Set missing fields: {', '.join(req)}.")
    return fixes


def main():
    print("# Content Framework Enforcement Report")
    print("**Site:** kanokmiah.com.bd  |  **Date:** 2026-07-28\n")
    
    all_posts = load_posts()
    post_map = {p['slug']: p for p in all_posts}
    changed = [post_map[s] for s in ALL_CHANGED_SLUGS if s in post_map]
    not_found = [s for s in ALL_CHANGED_SLUGS if s not in post_map]
    if not_found: print(f"⚠️  Missing: {not_found}\n")
    
    print(f"**Posts analyzed:** {len(changed)}  |  **Scope:** 2 commits (heading cleanup + internal linking audit)\n")
    
    posts_with_issues = []
    
    for post in changed:
        slug = post['slug']
        title = post.get('title','')
        r = {}; r['tfidf']=check_tfidf(post); r['entities']=check_entities(post); r['pillar']=check_pillar_link(post); r['aeo']=check_aeo_geo(post); r['internal']=check_internal_links(post); r['schema']=check_schema(post)
        
        print(f"---\n## Post: {slug}")
        print(f"**{title[:90]}**\n")
        print("| Check | Status | Details |")
        print("|-------|--------|---------|")
        print(f"| TF-IDF ({r['tfidf']['keyword']}) | {r['tfidf']['status']} | {r['tfidf']['count']} occurrences |")
        print(f"| Entities | {r['entities']['status']} | {', '.join(r['entities']['missing'][:3])} |")
        print(f"| Pillar Link | {r['pillar']['status']} | {r['pillar']['detail']} |")
        print(f"| AEO/GEO | {r['aeo']['status']} | {r['aeo']['count']} question headings |")
        print(f"| Internal Links | {r['internal']['status']} | {r['internal']['count']} internal links |")
        print(f"| Schema | {r['schema']['status']} | {', '.join(r['schema']['missing'])} |")
        
        fixes = generate_fix(r, post)
        if fixes:
            posts_with_issues.append(slug)
            print(f"\n### Fix Instructions")
            for f in fixes: print(f)
        else:
            print(f"\n✅ Pass.")
        print()
    
    total = len(changed)
    passed = total - len(posts_with_issues)
    tfidf_f = sum(1 for p in changed if check_tfidf(p)['status']=='❌')
    ent_f = sum(1 for p in changed if check_entities(p)['status']=='❌')
    pil_f = sum(1 for p in changed if check_pillar_link(p)['status']=='❌')
    aeo_f = sum(1 for p in changed if check_aeo_geo(p)['status']=='❌')
    int_f = sum(1 for p in changed if check_internal_links(p)['status']=='❌')
    sch_f = sum(1 for p in changed if check_schema(p)['status']=='❌')
    
    print("---\n## Executive Summary")
    print(f"- **Analyzed:** {total} | **Pass all:** {passed} | **Need fixes:** {len(posts_with_issues)}")
    print(f"  - TF-IDF fails: {tfidf_f}")
    print(f"  - Entity fails: {ent_f}")
    print(f"  - Pillar fails: {pil_f}")
    print(f"  - AEO/GEO fails: {aeo_f}")
    print(f"  - Internal link fails: {int_f}")
    print(f"  - Schema fails: {sch_f}")
    if posts_with_issues:
        print(f"\n⚠️  **Fixes needed:** {', '.join(posts_with_issues)}")
    else:
        print(f"\n🎉 **All posts pass!**")


if __name__ == "__main__":
    main()
