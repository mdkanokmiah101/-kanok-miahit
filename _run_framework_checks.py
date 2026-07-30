#!/usr/bin/env python3
"""Framework compliance checker - reads data.js directly."""
import re, json, sys

DATA_PATH = 'src/app/blog/data.js'

def get_post(slug):
    """Extract a single post from data.js by slug."""
    with open(DATA_PATH) as f:
        data = f.read()
    
    # Find post block - from this slug to next slug or end
    pattern = r'slug:\s*"' + re.escape(slug) + r'".*?(?=slug:\s*"|\Z)'
    m = re.search(pattern, data, re.DOTALL)
    if not m:
        return None
    block = m.group(0)
    
    post = {'slug': slug}
    
    # Simple key: "value" fields
    for key in ['title', 'date', 'author', 'excerpt', 'metaTitle', 'metaDescription', 'dateModified', 'readTime']:
        m2 = re.search(r'\b' + key + r'\s*:\s*"((?:[^"\\]|\\.)*)"', block)
        if m2:
            post[key] = m2.group(1)
    
    # Tags array
    m2 = re.search(r'tags:\s*\[([^\]]*)\]', block)
    if m2:
        tags_str = m2.group(1)
        post['tags'] = [t.strip().strip('"') for t in tags_str.split(',')]
    
    # Content template literal - find the backtick content
    # The content field ends before the next field or closing brace
    m2 = re.search(r'content:\s*`((?:[^`\\]|\\.)*)`', block, re.DOTALL)
    if m2:
        post['content'] = m2.group(1)
    
    return post


def check_tfidf(post):
    """Check TF-IDF keyword coverage."""
    title = post.get("title", "")
    content = post.get("content", "")
    if not content:
        return {"keyword": title, "count": 0, "passed": False, "detail": "No content found"}
    
    title_lower = title.lower()
    content_lower = content.lower()
    
    # Initialize
    keyword = ""
    count = 0

    # Extract primary keyword - for English titles
    if any('\u0980' <= c <= '\u09FF' for c in title):
        # Bengali - use excerpt first meaningful Bengali phrase
        excerpt = post.get("excerpt", "")
        words = excerpt.split()
        bengali_words = [w for w in words if any('\u0980' <= c <= '\u09FF' for c in w)]
        if bengali_words:
            keyword = bengali_words[0] if len(bengali_words) == 1 else ' '.join(bengali_words[:2])
        else:
            keyword = title[:30]
        # Count occurrences
        count = len(re.findall(re.escape(keyword), content))
    else:
        # English title - extract the core keyword
        # Remove site name suffix
        clean = re.sub(r'\s*\|\s*kanok\s+miah.*$', '', title_lower, flags=re.IGNORECASE).strip()
        
        # Strategy: find the most meaningful 2-3 word phrase from title
        # Remove "How to" prefix
        clean = re.sub(r'^how\s+to\s+', '', clean)
        # Remove parenthetical counts like "15 Things"
        clean = re.sub(r'\d+\s+things?\s+to\s+\w+', '', clean)
        # Remove subtitles after colon
        parts = clean.split(':')
        main_part = parts[0].strip()
        
        # Try different keyword candidates and pick the best one
        candidates = []
        
        # Candidate 1: Last 3 significant words of main part
        words = [w for w in main_part.split() if len(w) > 2]
        if len(words) >= 3:
            candidates.append(' '.join(words[-3:]))
        if len(words) >= 2:
            candidates.append(' '.join(words[-2:]))
        
        # Candidate 2: The whole main part (if not too long)
        if len(main_part.split()) <= 6:
            candidates.append(main_part)
        
        # Candidate 3: Title without "How to" and without colon part
        candidates.append(main_part)
        
        # Also try with "SEO" as it's likely the core topic
        seo_phrases = []
        for phrase in ['seo expert in dhaka', 'seo expert', 'mobile seo', 'seo in bangladesh',
                       'schema markup', 'rich snippets', 'structured data']:
            if phrase in content_lower:
                seo_phrases.append(phrase)
        
        candidates.extend(seo_phrases)
        
        # Try each candidate
        best_keyword = candidates[0] if candidates else clean
        best_count = 0
        
        for kw in candidates:
            count = len(re.findall(re.escape(kw), content_lower))
            if count > best_count:
                best_count = count
                best_keyword = kw
        
        keyword = best_keyword
        count = best_count
    
    # For "seo for bangladesh" type keywords, try partial matching
    if count < 3:
        words = keyword.split()
        for i in range(len(words), 0, -1):
            phrase = ' '.join(words[:i])
            if len(phrase) > 3:
                c = len(re.findall(re.escape(phrase), content_lower))
                if c > count:
                    count = c
                    keyword = phrase
    
    passed = count >= 5
    return {
        "keyword": keyword[:50],
        "count": count,
        "passed": passed,
        "detail": f"{count} occurrences of '{keyword[:40]}'"
    }


def check_entities(post):
    """Check required semantic entities."""
    content = post.get("content", "")
    content_lower = content.lower() if content else ""
    tags = [t.lower() for t in post.get("tags", [])]
    title = post.get("title", "").lower()
    
    # Always required entities
    required_entities = {
        "Dhaka": (r'\b[Dd]haka\b', "Location"),
        "Bangladesh": (r'\b[Bb]angladesh\b', "Location"),
    }
    
    missing = []
    found = {}
    
    for name, (pattern, _) in required_entities.items():
        found_flag = bool(re.search(pattern, content))
        found[name] = found_flag
        if not found_flag:
            missing.append(name)
    
    # Service type - check content for SEO-related service mentions
    service_patterns = [
        (r'\bseo\s+(?:expert|specialist|consultant|services?|agency|professional)\b', "SEO Service"),
        (r'\b(?:SEO|search engine optimization)\b', "SEO Topic"),
        (r'link building', "Link Building"),
        (r'content marketing', "Content Marketing"),
        (r'technical seo', "Technical SEO"),
        (r'local seo', "Local SEO"),
        (r'digital marketing', "Digital Marketing"),
        (r'on-page seo|on page seo', "On-Page SEO"),
        (r'geo|generative engine|ai search', "GEO/AI Search"),
        (r'aeo|answer engine', "AEO"),
    ]
    
    found_service = False
    for pattern, _ in service_patterns:
        if re.search(pattern, content_lower):
            found_service = True
            break
    
    found["Service Type Entity"] = found_service
    if not found_service:
        missing.append("Service type entity")
    
    return {
        "found": found,
        "missing": missing,
        "passed": len(missing) == 0
    }


def check_pillar_cluster(post):
    """Check pillar-cluster alignment."""
    content = post.get("content", "")
    content_lower = content.lower() if content else ""
    tags = [t.lower() for t in post.get("tags", [])]
    title = post.get("title", "").lower()
    
    pillars = {
        "SEO Services": {
            "patterns": [r'/services(?!\/\w)', r'/services\b'],
            "match_tags": ["seo service", "seo expert", "seo specialist", "seo consultant", "seo agency", "hire seo"],
        },
        "Local SEO": {
            "patterns": [r'/services/local-seo'],
            "match_tags": ["local seo", "google business profile", "gbp", "near me", "local search", "local business"],
        },
        "Technical SEO": {
            "patterns": [r'/services/technical-seo'],
            "match_tags": ["technical seo", "core web vitals", "page speed", "structured data", "schema", "mobile seo", "mobile-first", "mobile optimization"],
        },
        "GEO/AI Search": {
            "patterns": [r'/services/geo-ai-search', r'/services/geo'],
            "match_tags": ["geo", "ai seo", "generative engine", "ai search", "chatgpt", "generative engine optimization"],
        },
        "E-commerce SEO": {
            "patterns": [r'/services/ecommerce-seo'],
            "match_tags": ["ecommerce", "e-commerce", "online store", "shopify"],
        },
        "On-Page SEO": {
            "patterns": [r'/services/on-page-seo'],
            "match_tags": ["on-page", "on page seo", "content optimization", "seo content"],
        },
        "Link Building": {
            "patterns": [r'/services/link-building'],
            "match_tags": ["link building", "backlinks", "off-page"],
        },
    }
    
    # Determine pillar from tags
    matched_pillar = None
    for pname, pdata in pillars.items():
        for tag in tags:
            if any(pt in tag for pt in pdata["match_tags"]):
                matched_pillar = pname
                break
        if matched_pillar:
            break
    
    # If no pillar from tags, use title heuristics
    if not matched_pillar:
        if "schema" in title or "rich snippet" in title or "structured data" in title:
            matched_pillar = "Technical SEO"
        elif "mobile" in title:
            matched_pillar = "Technical SEO"
        elif "seo expert" in title or "choose" in title or "seo agency" in title:
            matched_pillar = "SEO Services"
        elif "link building" in title or "backlink" in title:
            matched_pillar = "Link Building"
        else:
            matched_pillar = "SEO Services"  # default
    
    # Check if any pillar page is linked
    linked_to = []
    for pname, pdata in pillars.items():
        for pattern in pdata["patterns"]:
            if re.search(pattern, content, re.IGNORECASE):
                linked_to.append(pname)
                break
    
    return {
        "matched_pillar": matched_pillar,
        "pillar_linked": len(linked_to) > 0,
        "links_to_pillar": linked_to,
        "passed": len(linked_to) > 0
    }


def check_aeo_geo(post):
    """Check AEO/GEO optimization - question-based headings."""
    content = post.get("content", "")
    if not content:
        return {"count": 0, "headings": [], "passed": False}
    
    # Count any heading (## or ###) that ends with ?
    question_headings = re.findall(
        r'^#{2,3}\s+.*?\?',
        content,
        re.MULTILINE
    )
    
    # Also count headings starting with question words (even without ?)
    q_starter_headings = re.findall(
        r'^#{2,3}\s+(?:How|What|Why|When|Where|Can|Do|Is|Are|Does|Should|Which|Who|Will)\b.*',
        content,
        re.MULTILINE | re.IGNORECASE
    )
    
    all_headings = list(set(question_headings + q_starter_headings))
    
    return {
        "count": len(all_headings),
        "headings": all_headings[:5],
        "passed": len(all_headings) >= 2
    }


def check_internal_links(post):
    """Count internal links."""
    content = post.get("content", "")
    if not content:
        return {"total": 0, "unique_targets": 0, "links": [], "passed": False}
    
    # Match markdown links with relative URLs
    internal_links = re.findall(r'\[([^\]]+)\]\((/[^\)]+)\)', content)
    
    # Filter meaningful internal links (not just /, /about, /contact, #)
    meaningful = [(text, url) for text, url in internal_links 
                  if url not in ('/', '/about', '/contact') 
                  and not url.startswith('/#')
                  and len(url) > 2]
    
    unique_targets = set(url for _, url in meaningful)
    
    return {
        "total": len(meaningful),
        "unique_targets": len(unique_targets),
        "links": meaningful[:10],
        "passed": len(meaningful) >= 3
    }


def check_schema_ready(post):
    """Check if schema metadata is set."""
    checks = {
        "title (headline)": bool(post.get("title")),
        "excerpt (description)": bool(post.get("excerpt")),
        "date (datePublished)": bool(post.get("date")),
        "metaTitle": bool(post.get("metaTitle")),
        "metaDescription": bool(post.get("metaDescription")),
        "dateModified": bool(post.get("dateModified")),
        "author": bool(post.get("author")),
    }
    
    missing_fields = [k if not v else None for k, v in checks.items()]
    missing = [k for k, v in checks.items() if not v]
    
    return {
        "checks": checks,
        "missing": missing,
        "passed": len(missing) == 0
    }


def generate_report(post):
    """Generate full framework report for a post."""
    slug = post.get("slug", "unknown")
    title = post.get("title", "Unknown")
    
    print(f"\n## Post: {slug}")
    print(f"**Title:** {title}")
    print()
    print("| Check | Status | Details |")
    print("|-------|--------|---------|")
    
    # A. TF-IDF
    tfidf = check_tfidf(post)
    tfidf_status = "✅" if tfidf["passed"] else "❌"
    print(f"| TF-IDF: `{tfidf['keyword']}` | {tfidf_status} | {tfidf['detail']} |")
    
    # B. Entities
    entities = check_entities(post)
    ent_status = "✅" if entities["passed"] else "❌"
    missing_ents = ", ".join(entities["missing"]) if entities["missing"] else "None"
    print(f"| Entities | {ent_status} | Missing: {missing_ents} |")
    
    # C. Pillar-Cluster
    pillar = check_pillar_cluster(post)
    pil_status = "✅" if pillar["passed"] else "❌"
    pil_detail = f"Pillar: {pillar['matched_pillar']}"
    if pillar["links_to_pillar"]:
        pil_detail += f" → links: {', '.join(pillar['links_to_pillar'])}"
    else:
        pil_detail += " → **NO pillar link found**"
    print(f"| Pillar Link | {pil_status} | {pil_detail} |")
    
    # D. AEO/GEO
    aeo = check_aeo_geo(post)
    aeo_status = "✅" if aeo["passed"] else "❌"
    print(f"| AEO/GEO | {aeo_status} | {aeo['count']} question headings |")
    if aeo["headings"]:
        print(f"| | | Sample: {aeo['headings'][:3]} |")
    
    # E. Internal Links
    links = check_internal_links(post)
    link_status = "✅" if links["passed"] else "❌"
    print(f"| Internal Links | {link_status} | {links['total']} total ({links['unique_targets']} unique) |")
    if not links["passed"]:
        print(f"| | | Samples: {links['links'][:5]} |")
    
    # F. Schema Ready
    schema = check_schema_ready(post)
    schema_status = "✅" if schema["passed"] else "❌"
    missing_schema = ", ".join(schema["missing"]) if schema["missing"] else "None"
    print(f"| Schema Ready | {schema_status} | Missing: {missing_schema} |")
    
    print()
    print("### Fix instructions:")
    fixes = []
    
    if not tfidf["passed"]:
        fixes.append(f"- **TF-IDF**: Keyword '{tfidf['keyword']}' appears only {tfidf['count']}x. Add more natural mentions throughout content (target ≥5).")
    
    if not entities["passed"]:
        for m in entities["missing"]:
            fixes.append(f"- **Entity**: Missing '{m}' reference in content.")
    
    if not pillar["passed"]:
        fixes.append(f"- **Pillar Link**: Add link to `{pillar['matched_pillar']}` pillar page (e.g., `/services/...`) with relevant anchor text.")
    
    if not aeo["passed"]:
        fixes.append(f"- **AEO/GEO**: Only {aeo['count']} question heading(s). Add ≥2 H2/H3 headings starting with How/What/Why/When/Where/Can/Do.")
    
    if not links["passed"]:
        fixes.append(f"- **Internal Links**: Only {links['total']} meaningful internal links. Add ≥3 (to blog posts, services, or locations).")
    
    if not schema["passed"]:
        for m in schema["missing"]:
            fixes.append(f"- **Schema**: Missing `{m}` field. Add it to post metadata (needed for Article Schema).")
    
    if not fixes:
        print("✅ All checks passed! No fixes needed.")
    else:
        for fix in fixes:
            print(fix)
    print()


def main():
    slugs = [
        "mobile-seo-optimization-bangladesh-mobile-first-era",
        "schema-markup-rich-snippets-techniques",
        "how-to-choose-best-seo-expert-dhaka-15-things"
    ]
    
    any_failures = False
    for slug in slugs:
        post = get_post(slug)
        if post:
            generate_report(post)
        else:
            print(f"\n## Post: {slug}")
            print("⚠️ Could not load post data.")
            any_failures = True
    
    # Summary
    print("\n---\n**Framework Enforcement Summary:**")
    all_passed = True
    for slug in slugs:
        post = get_post(slug)
        if not post:
            continue
        tfidf = check_tfidf(post)
        ents = check_entities(post)
        pillar = check_pillar_cluster(post)
        aeo = check_aeo_geo(post)
        links = check_internal_links(post)
        schema = check_schema_ready(post)
        
        checks = [tfidf["passed"], ents["passed"], pillar["passed"], aeo["passed"], links["passed"], schema["passed"]]
        all_ok = all(checks)
        icon = "✅" if all_ok else "❌"
        print(f"{icon} {slug}: {'All pass' if all_ok else f'{sum(checks)}/6 pass'}")
        if not all_ok:
            all_passed = False
    
    if all_passed:
        print("\n🎉 All posts pass framework compliance!")
    else:
        print("\n⚠️ Some posts need fixes as noted above.")


if __name__ == "__main__":
    main()
