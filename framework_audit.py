#!/usr/bin/env python3
"""
Content Framework Audit for kanokmiah.com.bd blog posts.
Extracts post metadata/content from data.js and runs 6 framework checks.
"""
import re
import sys
from pathlib import Path

DATA_FILE = Path("/root/kanok-miahit/src/app/blog/data.js")

TARGET_SLUGS = [
    "watchzonebd-seo-case-study",
    "ai-seo-2026-dhaka-experts-optimize-google-ai-chatgpt",
    "hiring-seo-expert-dhaka-better-roi-than-paid-ads",
    "seo-case-study-dhaka-businesses-increased-organic-traffic",
    "what-does-seo-expert-do-guide-business-owners",
    "top-10-seo-mistakes-dhaka-businesses-fix",
    "seo-expert-vs-seo-agency-dhaka-which-is-right",
    "how-to-choose-best-seo-expert-dhaka-15-things",
    "locksmith-dundee-seo-case-study",
]


def read_file(path):
    """Read the full file content."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def find_post_boundaries(text, slug):
    """
    Find the start and end line of a post object with the given slug.
    Returns (start_line, end_line) 0-indexed, or None.
    """
    lines = text.split("\n")
    slug_pattern = f'slug: "{slug}"'

    for i, line in enumerate(lines):
        if slug_pattern in line:
            # Find the opening brace before this line
            # Walk backwards from the slug line to find the opening {
            start = i
            while start >= 0:
                stripped = lines[start].strip()
                if stripped == "{" or stripped == "{":
                    break
                start -= 1
            else:
                continue  # Should not happen, but just in case

            # Now find the matching closing brace
            depth = 0
            in_template = False
            end = start
            while end < len(lines):
                line_text = lines[end]
                for ch in line_text:
                    if ch == "`":
                        in_template = not in_template
                    if not in_template:
                        if ch == "{":
                            depth += 1
                        elif ch == "}":
                            depth -= 1
                            if depth == 0:
                                return (start, end)
                end += 1
            return (start, end)
    return None


def extract_post(text, slug):
    """
    Extract post data from the JS file content for the given slug.
    Returns a dict with slug, title, tags, date, excerpt, content.
    """
    boundaries = find_post_boundaries(text, slug)
    if not boundaries:
        return None

    start_line, end_line = boundaries
    lines = text.split("\n")
    obj_lines = lines[start_line : end_line + 1]

    # Join back into text
    obj_text = "\n".join(obj_lines)

    # Extract fields using regex
    post = {"slug": slug}

    # Title - can be on same line or next line
    title_match = re.search(
        r'title:\s*"((?:[^"\\]|\\.)*)"', obj_text, re.DOTALL
    )
    if title_match:
        post["title"] = title_match.group(1)
    else:
        # Title might be multiline with string concatenation
        # Actually in the data it's a single string
        post["title"] = "UNKNOWN"

    # Date
    date_match = re.search(r'date:\s*"([^"]+)"', obj_text)
    post["date"] = date_match.group(1) if date_match else "UNKNOWN"

    # Author
    author_match = re.search(r'author:\s*"([^"]+)"', obj_text)
    post["author"] = author_match.group(1) if author_match else "UNKNOWN"

    # Excerpt - can be multiline
    excerpt_match = re.search(
        r'excerpt:\s*\n?\s*"((?:[^"\\]|\\.)*)"', obj_text, re.DOTALL
    )
    if excerpt_match:
        post["excerpt"] = excerpt_match.group(1).replace("\n", " ").strip()
    else:
        post["excerpt"] = ""

    # Tags array
    tags_match = re.search(r'tags:\s*\[([^\]]+)\]', obj_text, re.DOTALL)
    if tags_match:
        tag_str = tags_match.group(1)
        tags = re.findall(r'"([^"]*)"', tag_str)
        post["tags"] = tags
    else:
        post["tags"] = []

    # Content template literal - find the backtick content
    # The content field is: content: `...`
    # We need to find the backtick after "content:"
    content_match = re.search(
        r'content:\s*`\n?(.*?)\n?`\s*,?\s*\n?\}', obj_text, re.DOTALL
    )
    if content_match:
        post["content"] = content_match.group(1)
    else:
        # Try alternative: content might be on the same line as opening backtick
        content_match2 = re.search(
            r'content:\s*`(.*?)`\s*,?\s*\n?\}', obj_text, re.DOTALL
        )
        if content_match2:
            post["content"] = content_match2.group(1)
        else:
            post["content"] = ""

    return post


def get_primary_keyword(title):
    """
    Extract primary keyword from title.
    Takes the first matching known keyword in the title (left-to-right),
    which represents the primary topic.
    """
    if not title:
        return ""

    # Known keyword phrases ranked by priority (primary topic first in scan order)
    known_keywords = [
        "SEO Case Study",
        "AI SEO",
        "SEO Mistakes",
        "SEO Expert",
        "SEO Agency",
        "SEO ROI",
        "SEO Services",
        "SEO Guide",
        "Local SEO",
        "Technical SEO",
        "E-commerce SEO",
        "GEO Optimization",
        "Organic Traffic",
    ]

    # Find the FIRST matching keyword in the title (left-to-right scan)
    # This ensures the primary topic (mentioned first) is chosen
    best_pos = len(title) + 1
    best_kw = None
    for kw in known_keywords:
        pos = title.lower().find(kw.lower())
        if pos >= 0 and pos < best_pos:
            best_pos = pos
            best_kw = kw

    if best_kw:
        return best_kw

    # Pattern-based extraction
    patterns = [
        # "SEO Case Study: ..." -> capture what comes before colon
        r'^([A-Z][A-Za-z\s]{3,60}?)(?:\s*:|\s*—|\s*–|\s*-\s)',
        # "Top 10 SEO Mistakes..." -> SEO Mistakes
        r'(?:Top\s+\d+\s+)?(SEO\s+\w+)',
        # "How to Choose the Best SEO Expert..." -> SEO Expert
        r'(SEO\s+(?:Expert|Agency|Audit|Guide|Strategy))',
    ]

    for p in patterns:
        m = re.search(p, title, re.IGNORECASE)
        if m:
            return m.group(1).strip()

    # Fallback: extract first meaningful bigram (two consecutive capitalized words)
    words = title.split()
    for i in range(len(words) - 1):
        if words[i][0].isupper() and words[i+1][0].isupper():
            return f"{words[i]} {words[i+1]}"

    # Last resort: first 3 words
    return " ".join(words[:3])


def check_tfidf(post):
    """Check A: TF-IDF Coverage - keyword frequency in content."""
    primary_kw = get_primary_keyword(post.get("title", ""))
    content = post.get("content", "")
    if not primary_kw:
        return {"status": "⚠️", "keyword": "N/A", "count": 0, "detail": "Could not extract keyword"}

    # Count occurrences (case-insensitive, whole or partial word)
    # Escape special regex chars in the keyword
    escaped = re.escape(primary_kw)
    count = len(re.findall(escaped, content, re.IGNORECASE))

    status = "✅" if count >= 5 else "❌"
    return {
        "status": status,
        "keyword": primary_kw,
        "count": count,
        "detail": f"'{primary_kw}' appears {count} times {'≥5 ✅' if count >= 5 else '<5 ❌'}",
    }


def check_entities(post):
    """Check B: Semantic Entity Coverage."""
    content = post.get("content", "")
    title = post.get("title", "")
    slug = post.get("slug", "")

    # Determine entity checks based on post context
    is_bd_focus = any(kw in slug + title for kw in ["dhaka", "bangladesh", "bd"])
    is_case_study = "case-study" in slug
    is_locksmith = "locksmith" in slug

    entities_to_check = []

    if is_bd_focus:
        entities_to_check.extend(["Dhaka", "Bangladesh", "SEO", "Google"])
    else:
        entities_to_check.extend(["SEO", "Google"])

    if is_case_study:
        if is_locksmith:
            entities_to_check.extend(["Locksmith", "Dundee", "local search"])
        elif "watchzone" in slug.lower():
            entities_to_check.extend(["WatchZoneBD", "e-commerce", "organic traffic"])
        else:
            entities_to_check.extend(["case study", "organic traffic"])

    # Ensure uniqueness while preserving order
    seen = set()
    unique_entities = []
    for e in entities_to_check:
        if e.lower() not in seen:
            seen.add(e.lower())
            unique_entities.append(e)

    results = []
    all_pass = True
    for entity in unique_entities:
        count = len(re.findall(re.escape(entity), content, re.IGNORECASE))
        found = count > 0
        if not found:
            all_pass = False
        results.append({"entity": entity, "count": count, "found": found})

    status = "✅" if all_pass else "❌"
    missing = [r["entity"] for r in results if not r["found"]]
    return {
        "status": status,
        "results": results,
        "detail": f"{len([r for r in results if r['found']])}/{len(results)} entities found" +
                  (f"; missing: {', '.join(missing)}" if missing else ""),
    }


def check_pillar_cluster(post):
    """Check C: Pillar-Cluster Alignment."""
    tags = post.get("tags", [])
    content = post.get("content", "")

    # Determine pillar topic from tags
    pillar_patterns = {
        "SEO": ["/services/", "/blog/complete-seo-guide-", "/industries/"],
        "Local SEO": ["/services/local-seo", "/industries/"],
        "E-commerce SEO": ["/industries/ecommerce", "/services/"],
        "Technical SEO": ["/services/technical-seo"],
        "AI SEO": ["/blog/ai-seo-"],
        "Case Study": ["/case-studies", "/blog/"],
    }

    # Find internal links to pillar pages
    internal_links = re.findall(r'href="(/(?:[^"]*))"', content)
    # Also find markdown links: [text](/path)
    internal_links += re.findall(r'\]\(((?:/[^\)]+))\)', content)

    # Filter to pillar-like links
    pillar_keywords = ["/industries/", "/services/", "/blog/", "/case-studies"]
    pillar_links = [
        l for l in internal_links
        if any(pk in l for pk in pillar_keywords) and len(l) > 10
    ]

    # Also check for the tag-based pillar guide
    # For SEO-tagged posts, check if /blog/complete-seo-guide-bangladesh-businesses-2026 linked
    tag_kw = " ".join(tags).lower()
    pillar_guide_links = [
        "/blog/complete-seo-guide-bangladesh-businesses-2026",
        "/industries/ecommerce",
        "/industries/real-estate",
        "/industries/medical",
        "/industries/education",
        "/industries/food-restaurant",
        "/industries/cleaning",
        "/industries/garments-textile",
        "/services/local-seo",
        "/services/technical-seo",
        "/services/on-page-seo",
    ]

    found_pillar = [l for l in pillar_links if any(pgl in l for pgl in pillar_guide_links)]
    # Also check if ANY /industries/, /services/, or /blog/pillar-guide link exists
    has_pillar_link = len(found_pillar) > 0

    # Also check for dedicated pillar guide link
    if not has_pillar_link:
        has_pillar_link = any(
            any(pg in l for pg in pillar_guide_links)
            for l in pillar_links
        )

    status = "✅" if has_pillar_link else "❌"
    return {
        "status": status,
        "pillar_links_found": found_pillar if found_pillar else pillar_links[:3],
        "total_internal_links_found": len(internal_links),
        "detail": f"{len(found_pillar)} pillar link(s) found" if has_pillar_link else "No pillar links found",
    }


def check_aeo_geo(post):
    """Check D: AEO/GEO Optimization - question-based headings."""
    content = post.get("content", "")
    
    # Count question-based headings
    # Patterns: ## Question? or ### Question?
    question_heading_pattern = re.compile(
        r'^#{2,3}\s+(How|What|Why|When|Where|Can|Do|Is|Are)\b',
        re.IGNORECASE | re.MULTILINE
    )
    
    matches = question_heading_pattern.findall(content)
    count = len(matches)
    
    status = "✅" if count >= 2 else "❌"
    return {
        "status": status,
        "count": count,
        "detail": f"{count} question-based heading(s) found {'≥2 ✅' if count >= 2 else '<2 ❌'}",
        "question_headings": matches,
    }


def check_internal_links(post):
    """Check E: Internal Linking - count internal links."""
    content = post.get("content", "")
    
    # Find all internal links: href="(/...) and markdown: ](/...)
    href_links = re.findall(r'href="(/(?:[^"]*))"', content)
    md_links = re.findall(r'\]\(((?:/[^\)]+))\)', content)
    
    all_internal = href_links + md_links
    
    # Filter out anchors-only, mailto, etc.
    valid_internal = [
        l for l in all_internal 
        if l.startswith("/") and not l.startswith("/#") and len(l) > 1
    ]
    
    # Remove duplicates
    unique_internal = list(set(valid_internal))
    
    count = len(unique_internal)
    status = "✅" if count >= 3 else "❌"
    
    return {
        "status": status,
        "count": count,
        "detail": f"{count} unique internal link(s) found {'≥3 ✅' if count >= 3 else '<3 ❌'}",
        "links": unique_internal[:10],  # Show first 10
    }


def check_schema(post):
    """Check F: Schema - required fields for ArticleSchema."""
    missing = []
    
    if not post.get("title") or post["title"] == "UNKNOWN":
        missing.append("title")
    if not post.get("excerpt"):
        missing.append("excerpt/description")
    if not post.get("date") or post["date"] == "UNKNOWN":
        missing.append("datePublished")
    if not post.get("author") or post["author"] == "UNKNOWN":
        missing.append("author")
    
    # Check content length as a proxy for schema readiness
    content_len = len(post.get("content", ""))
    
    status = "✅" if len(missing) == 0 else "❌"
    return {
        "status": status,
        "missing": missing,
        "content_length": content_len,
        "detail": "All required fields present ✅" if len(missing) == 0 else f"Missing: {', '.join(missing)}",
    }


def run_all_checks(post):
    """Run all 6 framework checks on a post."""
    return {
        "tfidf": check_tfidf(post),
        "entities": check_entities(post),
        "pillar_cluster": check_pillar_cluster(post),
        "aeo_geo": check_aeo_geo(post),
        "internal_links": check_internal_links(post),
        "schema": check_schema(post),
    }


def extract_content_range(text, slug):
    """Get the full content for a post by finding its boundaries and extracting just the content field."""
    boundaries = find_post_boundaries(text, slug)
    if not boundaries:
        return None
    
    start_line, end_line = boundaries
    lines = text.split("\n")
    obj_lines = lines[start_line : end_line + 1]
    obj_text = "\n".join(obj_lines)
    
    # Try to extract content between backticks after "content:"
    # Find the content: field
    idx = obj_text.find("content:")
    if idx == -1:
        return None
    
    # Find the opening backtick after content:
    rest = obj_text[idx:]
    bt_start = rest.find("`")
    if bt_start == -1:
        return None
    
    # Now find the closing backtick (the last one before `},`)
    content_start = idx + bt_start + 1
    # Search from the end backwards for the closing backtick
    # The content ends with `  }, or `,\n  } or similar
    obj_from_content = obj_text[idx + bt_start + 1:]
    
    # Find the matching closing backtick
    # Since template literals can have escaped backticks, we need to be careful
    # But in practice, the content ends with ` before }, or `,\n
    # Let's search for the pattern: `  }, or `,\n
    close_match = re.search(r'`\s*,?\s*\n?\s*\}', obj_from_content)
    if close_match:
        content = obj_from_content[:close_match.start()]
        return content
    
    return None


def extract_post_full(text, slug):
    """More robust extraction using boundary-based approach."""
    boundaries = find_post_boundaries(text, slug)
    if not boundaries:
        return None
    
    start_line, end_line = boundaries
    lines = text.split("\n")
    obj_lines = lines[start_line : end_line + 1]
    obj_text = "\n".join(obj_lines)
    
    post = {"slug": slug}
    
    # Title - handle both single-line and multi-line
    # pattern: title: "..." or title:\n  "..."
    title_match = re.search(r'title:\s*"([^"]*)"', obj_text)
    if title_match:
        post["title"] = title_match.group(1)
    else:
        # Try multi-line title (title: on one line, value on next)
        title_match2 = re.search(r'title:\s*\n\s*"([^"]*)"', obj_text)
        if title_match2:
            post["title"] = title_match2.group(1)
        else:
            post["title"] = "UNKNOWN"
    
    # Date
    date_match = re.search(r'date:\s*"([^"]+)"', obj_text)
    post["date"] = date_match.group(1) if date_match else "UNKNOWN"
    
    # Author
    author_match = re.search(r'author:\s*"([^"]+)"', obj_text)
    post["author"] = author_match.group(1) if author_match else "UNKNOWN"
    
    # Excerpt - can be multiline
    excerpt_match = re.search(
        r'excerpt:\s*\n?\s*"((?:[^"\\]|\\.)*)"', obj_text, re.DOTALL
    )
    if excerpt_match:
        post["excerpt"] = excerpt_match.group(1).replace("\n", " ").strip()
    else:
        post["excerpt"] = ""
    
    # Tags array
    tags_match = re.search(r'tags:\s*\[([^\]]+)\]', obj_text, re.DOTALL)
    if tags_match:
        tag_str = tags_match.group(1)
        tags = re.findall(r'"([^"]*)"', tag_str)
        post["tags"] = tags
    else:
        post["tags"] = []
    
    # Content - the tricky one
    content_text = extract_content_range(text, slug)
    if content_text:
        # Unescape any escaped backticks (though unlikely in this dataset)
        post["content"] = content_text
    else:
        # Fallback: try regex
        content_match = re.search(
            r'content:\s*`(.*)`\s*,?\s*\}', obj_text, re.DOTALL
        )
        if content_match:
            post["content"] = content_match.group(1)
        else:
            post["content"] = ""
    
    return post


def generate_report(results):
    """Generate a structured markdown report."""
    lines = []
    lines.append("# Content Framework Audit Report")
    lines.append(f"**Generated:** 2026-07-15")
    lines.append(f"**Source:** `/root/kanok-miahit/src/app/blog/data.js`")
    lines.append(f"**Posts Analyzed:** {len(results)}")
    lines.append("")
    
    for slug, data in results.items():
        post = data["post"]
        checks = data["checks"]
        
        lines.append("---")
        lines.append("")
        lines.append(f"## 📄 {post.get('title', 'Unknown')}")
        lines.append(f"**Slug:** `{slug}`")
        lines.append(f"**Date:** {post.get('date', 'N/A')}")
        lines.append(f"**Tags:** {', '.join(post.get('tags', []))}")
        lines.append("")
        
        # Summary badges
        tfidf_s = checks["tfidf"]["status"]
        entities_s = checks["entities"]["status"]
        pillar_s = checks["pillar_cluster"]["status"]
        aeo_s = checks["aeo_geo"]["status"]
        il_s = checks["internal_links"]["status"]
        schema_s = checks["schema"]["status"]
        
        total_pass = sum(1 for s in [tfidf_s, entities_s, pillar_s, aeo_s, il_s, schema_s] if s == "✅")
        
        lines.append(f"**Overall:** {total_pass}/6 checks passed")
        lines.append("")
        lines.append(f"| Check | Status | Detail |")
        lines.append(f"|-------|--------|--------|")
        lines.append(f"| **A) TF-IDF Coverage** | {tfidf_s} | {checks['tfidf']['detail']} |")
        lines.append(f"| **B) Semantic Entities** | {entities_s} | {checks['entities']['detail']} |")
        lines.append(f"| **C) Pillar-Cluster** | {pillar_s} | {checks['pillar_cluster']['detail']} |")
        lines.append(f"| **D) AEO/GEO** | {aeo_s} | {checks['aeo_geo']['detail']} |")
        lines.append(f"| **E) Internal Links** | {il_s} | {checks['internal_links']['detail']} |")
        lines.append(f"| **F) Schema Fields** | {schema_s} | {checks['schema']['detail']} |")
        lines.append("")
        
        # Detailed breakdowns
        lines.append("### A) TF-IDF Coverage")
        lines.append(f"- Primary keyword: `{checks['tfidf']['keyword']}`")
        lines.append(f"- Occurrences in content: **{checks['tfidf']['count']}**")
        lines.append(f"- Verdict: {checks['tfidf']['status']} {'≥5 occurrences' if checks['tfidf']['count'] >= 5 else '<5 occurrences — needs more keyword usage'}")
        lines.append("")
        
        lines.append("### B) Semantic Entity Coverage")
        for ent in checks["entities"]["results"]:
            found_mark = "✅" if ent["found"] else "❌"
            lines.append(f"- {found_mark} `{ent['entity']}`: {ent['count']} mention(s)")
        lines.append(f"- Verdict: {checks['entities']['status']}")
        lines.append("")
        
        lines.append("### C) Pillar-Cluster Alignment")
        pillar_links = checks["pillar_cluster"].get("pillar_links_found", [])
        if pillar_links:
            lines.append(f"- Pillar links found:")
            for pl in pillar_links[:5]:
                lines.append(f"  - `{pl}`")
        else:
            lines.append(f"- No pillar links found in content")
        lines.append(f"- Total internal links scanned: {checks['pillar_cluster'].get('total_internal_links_found', 0)}")
        lines.append(f"- Verdict: {checks['pillar_cluster']['status']}")
        lines.append("")
        
        lines.append("### D) AEO/GEO Optimization")
        lines.append(f"- Question-based headings: **{checks['aeo_geo']['count']}**")
        if checks["aeo_geo"].get("question_headings"):
            lines.append(f"- Starting with: {', '.join(set(checks['aeo_geo']['question_headings']))}")
        lines.append(f"- Verdict: {checks['aeo_geo']['status']} {'≥2 question headings ✅' if checks['aeo_geo']['count'] >= 2 else '<2 — needs more question-based H2/H3'}")
        lines.append("")
        
        lines.append("### E) Internal Linking")
        lines.append(f"- Unique internal links: **{checks['internal_links']['count']}**")
        if checks["internal_links"].get("links"):
            lines.append(f"- Links: {', '.join(checks['internal_links']['links'][:8])}")
            if len(checks["internal_links"]["links"]) > 8:
                lines.append(f"- ... and {len(checks['internal_links']['links']) - 8} more")
        lines.append(f"- Verdict: {checks['internal_links']['status']} {'≥3 internal links ✅' if checks['internal_links']['count'] >= 3 else '<3 — needs more internal links'}")
        lines.append("")
        
        lines.append("### F) Schema / Article Fields")
        lines.append(f"- Title present: {'✅' if post.get('title') and post['title'] != 'UNKNOWN' else '❌'}")
        lines.append(f"- Excerpt present: {'✅' if post.get('excerpt') else '❌'}")
        lines.append(f"- Date present: {'✅' if post.get('date') and post['date'] != 'UNKNOWN' else '❌'}")
        lines.append(f"- Author present: {'✅' if post.get('author') and post['author'] != 'UNKNOWN' else '❌'}")
        lines.append(f"- Content length: {checks['schema']['content_length']} chars")
        lines.append(f"- Verdict: {checks['schema']['status']}")
        lines.append("")
    
    # Summary table at end
    lines.append("---")
    lines.append("")
    lines.append("## 📊 Summary")
    lines.append("")
    lines.append("| # | Post | TF-IDF | Entities | Pillar | AEO/GEO | Int.Links | Schema | Score |")
    lines.append("|---|------|--------|----------|--------|---------|-----------|--------|-------|")
    
    for i, (slug, data) in enumerate(results.items(), 1):
        c = data["checks"]
        title_short = data["post"].get("title", slug)[:40]
        badges = "".join([
            c["tfidf"]["status"],
            c["entities"]["status"],
            c["pillar_cluster"]["status"],
            c["aeo_geo"]["status"],
            c["internal_links"]["status"],
            c["schema"]["status"],
        ])
        score = sum(1 for s in [
            c["tfidf"]["status"],
            c["entities"]["status"],
            c["pillar_cluster"]["status"],
            c["aeo_geo"]["status"],
            c["internal_links"]["status"],
            c["schema"]["status"],
        ] if s == "✅")
        lines.append(f"| {i} | {title_short}... | {c['tfidf']['status']} | {c['entities']['status']} | {c['pillar_cluster']['status']} | {c['aeo_geo']['status']} | {c['internal_links']['status']} | {c['schema']['status']} | **{score}/6** |")
    
    lines.append("")
    return "\n".join(lines)


def main():
    print("📖 Reading data.js...")
    text = read_file(DATA_FILE)
    print(f"   Read {len(text)} characters")
    
    results = {}
    
    for slug in TARGET_SLUGS:
        print(f"\n🔍 Extracting post: {slug}")
        post = extract_post_full(text, slug)
        
        if not post or not post.get("content"):
            print(f"   ⚠️  Could not extract post content for '{slug}'")
            continue
        
        content_len = len(post.get("content", ""))
        print(f"   Title: {post.get('title', 'N/A')[:60]}...")
        print(f"   Content length: {content_len} chars")
        print(f"   Tags: {', '.join(post.get('tags', []))}")
        
        print(f"   Running 6 checks...")
        checks = run_all_checks(post)
        
        results[slug] = {"post": post, "checks": checks}
        
        # Quick status
        print(f"   TF-IDF: {checks['tfidf']['status']} | Entities: {checks['entities']['status']} | Pillar: {checks['pillar_cluster']['status']} | AEO/GEO: {checks['aeo_geo']['status']} | IntLinks: {checks['internal_links']['status']} | Schema: {checks['schema']['status']}")
    
    print(f"\n✅ Extracted {len(results)} posts successfully")
    
    # Generate report
    print("\n📝 Generating report...")
    report = generate_report(results)
    
    # Write report
    report_path = Path("/root/kanok-miahit/framework-audit-report.md")
    report_path.write_text(report, encoding="utf-8")
    print(f"📄 Report written to: {report_path}")
    
    # Also print summary to stdout
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    for slug, data in results.items():
        c = data["checks"]
        score = sum(1 for s in [
            c["tfidf"]["status"],
            c["entities"]["status"],
            c["pillar_cluster"]["status"],
            c["aeo_geo"]["status"],
            c["internal_links"]["status"],
            c["schema"]["status"],
        ] if s == "✅")
        print(f"  {slug[:50]:50s} → {score}/6")
    
    print(f"\n✅ Total posts: {len(results)}")

if __name__ == "__main__":
    main()
