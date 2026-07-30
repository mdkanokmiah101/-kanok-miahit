#!/usr/bin/env python3
"""Improved analysis of changed blog posts for framework compliance."""
import re
import json

DATA_PATH = "src/app/blog/data.js"

with open(DATA_PATH, "r") as f:
    raw = f.read()

lines = raw.split('\n')

# Slugs that were modified in the last 48 hours
changed_slugs = [
    "mobile-seo-optimization-bangladesh-mobile-first-era",
    "schema-markup-rich-snippets-techniques",
    "why-md-kanok-miah-is-the-best-seo-expert-in-dhaka-bangladesh",
    "locksmith-dundee-seo-case-study",
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
    "what-does-seo-expert-do-guide-business-owners",
    "seo-case-study-dhaka-businesses-increased-organic-traffic",
    "hiring-seo-expert-dhaka-better-roi-than-paid-ads",
    "ai-seo-2026-dhaka-experts-optimize-google-ai-chatgpt",
    "watchzonebd-seo-case-study",
]

def get_post_data(slug):
    """Extract post data from lines."""
    found_idx = -1
    for i, line in enumerate(lines):
        if f'slug: "{slug}"' in line or f"slug: '{slug}'" in line:
            found_idx = i
            break
    
    if found_idx == -1:
        return None
    
    # Collect header lines until content:
    header_lines = []
    content_lines = []
    in_content = False
    brace_depth = 0
    started = False
    
    for i in range(found_idx, len(lines)):
        line = lines[i]
        stripped = line.strip()
        
        if not started:
            started = True
        
        if in_content:
            if stripped == "`,":
                in_content = False
                continue
            # Remove leading ` if content starts on same line
            line_content = line
            if '`' in line and not stripped.startswith('```'):
                bt_idx = line.find('`')
                if line[bt_idx:bt_idx+3] != '```' and i == found_idx:
                    # Content on same line as opening backtick
                    line_content = line[bt_idx+1:]
            content_lines.append(line_content)
        elif 'content: `' in stripped:
            in_content = True
            bt_idx = line.find('`')
            if bt_idx >= 0 and bt_idx + 1 < len(line):
                remainder = line[bt_idx+1:]
                if remainder.strip():
                    content_lines.append(remainder)
        elif not in_content:
            header_lines.append(line)
    
    content = "\n".join(content_lines)
    header = "\n".join(header_lines)
    
    # Extract fields
    def extract(field):
        m = re.search(rf'{field}:\s*"([^"]*)"', header)
        if not m:
            m = re.search(rf"{field}:\s*'([^']*)'", header)
        if not m:
            m = re.search(rf'{field}:\s*\n\s+"([^"]*)"', header)
        return m.group(1) if m else ""
    
    def extract_multiline(field):
        """For multiline field values like excerpt."""
        idx = header.find(f"{field}:")
        if idx == -1:
            return ""
        rest = header[idx+len(field)+1:]
        # Find first quote
        q_idx = rest.find('"')
        if q_idx == -1:
            q_idx = rest.find("'")
        if q_idx == -1:
            return ""
        quote_char = rest[q_idx]
        # Find closing quote
        end_idx = rest.find(quote_char, q_idx+1)
        if end_idx == -1:
            return ""
        return rest[q_idx+1:end_idx]
    
    title = extract("title")
    slug_val = extract("slug")
    date = extract("date")
    author = extract("author")
    excerpt = extract_multiline("excerpt")
    
    # Tags
    tags = []
    t_idx = header.find("tags: [")
    if t_idx >= 0:
        br_start = header.find("[", t_idx)
        br_end = header.find("]", br_start)
        if br_start >= 0 and br_end >= 0:
            tag_str = header[br_start+1:br_end]
            tags = re.findall(r'"([^"]*)"', tag_str)
    
    # Meta fields
    meta_title = extract_multiline("metaTitle")
    meta_desc = extract_multiline("metaDescription")
    date_mod = extract("dateModified")
    
    return {
        "slug": slug_val,
        "title": title,
        "date": date,
        "author": author,
        "excerpt": excerpt,
        "tags": tags,
        "metaTitle": meta_title,
        "metaDescription": meta_desc,
        "dateModified": date_mod,
        "content": content
    }

def analyze_post(slug):
    pd = get_post_data(slug)
    if not pd or not pd["content"]:
        return {"slug": slug, "error": "Could not extract post"}
    
    title = pd["title"]
    content = pd["content"]
    tags = pd["tags"]
    excerpt = pd["excerpt"]
    meta_title = pd["metaTitle"]
    meta_desc = pd["metaDescription"]
    date_mod = pd["dateModified"]
    date = pd["date"]
    
    results = {"title": title, "slug": slug}
    
    # ========== A. TF-IDF Coverage ==========
    # Determine keyword from title context
    title_lower = title.lower()
    
    # Map common patterns to their keywords
    keyword_overrides = {
        "seo expert": "SEO expert",
        "seo agency": "SEO agency",
        "seo consultant": "SEO consultant",
        "mobile seo": "Mobile SEO",
        "schema markup": "Schema Markup",
        "local seo": "Local SEO",
        "technical seo": "Technical SEO",
        "link building": "Link Building",
        "digital marketing": "Digital Marketing",
        "seo case study": "Case Study",
        "google business profile": "Google Business Profile",
        "ai seo": "AI SEO",
        "geo": "GEO",
        "seo mistakes": "SEO mistakes",
        "seo roi": "SEO ROI",
        "ecommerce seo": "Ecommerce SEO",
    }
    
    keyword = None
    for pattern, kw in keyword_overrides.items():
        if pattern in title_lower:
            keyword = kw
            break
    
    if not keyword:
        # Try to find first meaningful keyword
        words = title_lower.replace(":", " ").replace("?", " ").split()
        # Try multi-word first
        for i in range(len(words)):
            phrase = " ".join(words[i:i+3])
            if len(phrase.split()) >= 2 and phrase not in ["how to", "what is", "why do", "is the"]:
                # Check if it appears in content
                if len(re.findall(re.escape(phrase), content, re.IGNORECASE)) > 0:
                    keyword = phrase
                    break
        
        if not keyword:
            for i in range(len(words)):
                if len(words[i]) > 2 and words[i] not in ["the", "for", "and", "your", "our", "its", "from", "with"]:
                    keyword = words[i]
                    break
    
    if not keyword:
        keyword = title_lower.split()[0] if title_lower else slug
    
    kw_count = len(re.findall(re.escape(keyword), content, re.IGNORECASE)) if keyword else 0
    results["tfidf"] = {
        "keyword": keyword,
        "occurrences": kw_count,
        "pass": kw_count >= 3  # More lenient: 3+ for niche case studies
    }
    
    # ========== B. Entity Coverage ==========
    is_case = slug.endswith("seo-case-study") or "case study" in title_lower
    is_seo = "seo" in title_lower
    is_schema = "schema" in title_lower or "structured data" in slug
    is_mobile = "mobile" in title_lower or slug.startswith("mobile")
    is_local = "local" in title_lower or "local" in tags
    is_technical = "technical" in title_lower
    is_ai_geo = "ai" in title_lower or "geo" in title_lower or "ai search" in title_lower or "chatgpt" in title_lower
    is_hiring = "hire" in title_lower or "choose" in title_lower or "expert" in title_lower
    
    entities_to_check = ["Bangladesh", "Dhaka"]
    
    if is_case:
        entities_to_check.extend(["organic traffic", "ranking", "keywords"])
    if is_schema:
        entities_to_check.extend(["JSON-LD", "structured data", "rich snippets", "CTR"])
    if is_mobile:
        entities_to_check.extend(["mobile-first", "Core Web Vitals", "voice search"])
    if is_local:
        entities_to_check.extend(["Google Business Profile", "Google Maps"])
    if is_technical:
        entities_to_check.extend(["Core Web Vitals", "structured data"])
    if is_ai_geo:
        entities_to_check.extend(["Generative Engine", "Google AI Overviews", "entity", "FAQ schema"])
    if is_hiring:
        entities_to_check.extend(["Google Business Profile", "case studies", "industry"])
    
    # Check for specific entities in content
    missing = []
    for entity in entities_to_check:
        if entity.lower() not in content.lower():
            missing.append(entity)
    
    results["entities"] = {
        "checked": entities_to_check,
        "missing": missing,
        "pass": len(missing) <= 1  # Allow 1 missing entity
    }
    
    # ========== C. Pillar Link ==========
    pillar_pages = [
        "/blog/complete-seo-guide-bangladesh-businesses-2026",
        "/blog/geo-optimization-prepare-business-ai-search",
        "/blog/technical-seo-checklist-bangladeshi-websites",
        "/blog/seo-bangla-beginners-guide-google-ranking",
        "/blog/seo-garments-textile-industry-b2b-lead-generation",
        "/blog/seo-trends-2026-ai-geo-future",
    ]
    
    pillar_link = None
    for pp in pillar_pages:
        if f"({pp})" in content or f"href=\"{pp}\"" in content or f"]({pp}" in content:
            pillar_link = pp
            break
    
    if not pillar_link:
        blog_links = re.findall(r'\[([^\]]+)\]\((/blog/[\w-]+)\)', content)
        pillar_link = f"links to: {blog_links[0][1]}" if blog_links else None
    
    results["pillar"] = {
        "found": pillar_link,
        "pass": pillar_link is not None
    }
    
    # ========== D. AEO/GEO ==========
    # Find question-based headings
    q_pattern = re.compile(r'^#{2,4}\s+(How|What|Why|When|Where|Can|Do|Does|Is|Are)[^?]*\?', re.MULTILINE | re.IGNORECASE)
    q_headings = q_pattern.findall(content)
    
    # Also count FAQ-style questions in headings
    faq_qs = re.findall(r'^#{2,4}\s+.+\?$', content, re.MULTILINE)
    
    results["aeo"] = {
        "question_headings": len(faq_qs),
        "pass": len(faq_qs) >= 2
    }
    
    # ========== E. Internal Linking ==========
    # Count markdown links to internal paths
    internal_links = re.findall(r'\[([^\]]+)\]\((/[^\)]+)\)', content)
    # Filter to actual internal paths
    internal_paths = []
    for text, link in internal_links:
        if not link.startswith('http') and not link.startswith('//') and not link.startswith('#'):
            internal_paths.append(link)
    
    results["internal_links"] = {
        "count": len(internal_paths),
        "pass": len(internal_paths) >= 3,
        "paths": internal_paths[:5]  # Show first 5
    }
    
    # ========== F. Schema ==========
    missing_schema = []
    if not meta_title:
        missing_schema.append("metaTitle")
    if not meta_desc:
        missing_schema.append("metaDescription")
    if not date_mod:
        missing_schema.append("dateModified")
    
    # For ArticleSchema we need title, excerpt, date, metaTitle, metaDescription, dateModified
    # Some posts were created before meta fields were required - we flag them but don't fail
    has_core = bool(date) and bool(excerpt)
    
    results["schema"] = {
        "has_metaTitle": bool(meta_title),
        "has_metaDescription": bool(meta_desc),
        "has_dateModified": bool(date_mod),
        "has_date": bool(date),
        "has_excerpt": bool(excerpt),
        "missing_fields": missing_schema,
        "pass": len(missing_schema) == 0  # Strict: all meta fields needed for ArticleSchema
    }
    
    return results

# Run and output formatted
all_results = {}
for slug in changed_slugs:
    result = analyze_post(slug)
    all_results[slug] = result
    
    if "error" in result:
        print(f"\n## Post: {slug}")
        print(f"ERROR: {result['error']}")
        continue
    
    print(f"\n## Post: {slug}")
    print(f"**Title:** {result['title']}")
    print(f"| Check | Status | Details |")
    print(f"|-------|--------|---------|")
    
    tf = result["tfidf"]
    status_tf = "✅" if tf["pass"] else "❌"
    print(f"| TF-IDF: `{tf['keyword']}` | {status_tf} | {tf['occurrences']} occurrences |")
    
    en = result["entities"]
    status_en = "✅" if en["pass"] else "❌"
    missing_str = ", ".join(en["missing"]) if en["missing"] else "None"
    print(f"| Entities | {status_en} | Missing: {missing_str} |")
    
    pi = result["pillar"]
    status_pi = "✅" if pi["pass"] else "❌"
    pillar_str = str(pi["found"]) if pi["found"] else "None"
    print(f"| Pillar Link | {status_pi} | {pillar_str} |")
    
    ae = result["aeo"]
    status_ae = "✅" if ae["pass"] else "❌"
    print(f"| AEO/GEO | {status_ae} | {ae['question_headings']} question headings |")
    
    il = result["internal_links"]
    status_il = "✅" if il["pass"] else "❌"
    print(f"| Internal Links | {status_il} | {il['count']} total |")
    
    sc = result["schema"]
    status_sc = "✅" if sc["pass"] else "❌"
    missing_sc = ", ".join(sc["missing_fields"]) if sc["missing_fields"] else "All set"
    print(f"| Schema Ready | {status_sc} | Missing: {missing_sc} |")

print("\n\n---")
print("## Overall Summary")
pass_count = 0
total = 0
for r in all_results.values():
    if "error" not in r:
        total += 1
        if (r.get("tfidf", {}).get("pass", False) and
            r.get("entities", {}).get("pass", True) and
            r.get("pillar", {}).get("pass", True) and
            r.get("aeo", {}).get("pass", True) and
            r.get("internal_links", {}).get("pass", True) and
            r.get("schema", {}).get("pass", True)):
            pass_count += 1
print(f"\nPosts passing ALL checks: {pass_count}/{total}")
print(f"Posts with issues: {total - pass_count}/{total}")
print(f"\nTotal posts modified in 48h: {len(changed_slugs)}")
