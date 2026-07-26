#!/usr/bin/env python3
"""
Content Framework Enforcer — kanokmiah.com.bd (v2)
Reads data.js, runs all 6 framework checks on each post.
More robust TF-IDF using tags + title-based keyword extraction.
"""
import re, json, sys
from pathlib import Path
from collections import Counter

DATA_FILE = Path("src/app/blog/data.js")
posts_raw = DATA_FILE.read_text(encoding="utf-8")

# --- Parse posts ---
posts = []
current = None
for line in posts_raw.splitlines():
    sm = re.search(r'slug:\s*"([^"]+)"', line)
    if sm:
        if current:
            posts.append(current)
        current = {"slug": sm.group(1), "raw": ""}
    if current:
        current["raw"] += line + "\n"
if current:
    posts.append(current)

def get_field(post_raw, field):
    """Extract a single-line or multi-line string field value."""
    m = re.search(rf'{field}:\s*"([^"]*)"', post_raw)
    if m:
        return m.group(1)
    m = re.search(rf'{field}:\s*\n\s*"([^"]*)"', post_raw)
    if m:
        return m.group(1)
    return ""

def get_tags_linear(post_raw):
    """Extract tags from the tags: [...] line."""
    # Find the tags line
    for line in post_raw.splitlines():
        line_s = line.strip()
        if line_s.startswith("tags:") or line_s.startswith("tags :"):
            # Extract all quoted strings
            return re.findall(r'"([^"]+)"', line_s)
    return []

def get_content(post_raw):
    """Extract content (backtick block) from post raw text."""
    m = re.search(r'content:\s*`(.*?)`\s*,?\s*\n', post_raw, re.DOTALL)
    if m:
        return m.group(1)
    idx = post_raw.find("content:")
    if idx < 0:
        return ""
    rest = post_raw[idx:]
    bt_start = rest.find("`")
    if bt_start < 0:
        return ""
    bt_end = rest.find("`,\n", bt_start + 1)
    if bt_end < 0:
        bt_end = rest.rfind("`")
        if bt_end <= bt_start:
            return ""
    return rest[bt_start+1:bt_end]

def extract_keywords(title, tags):
    """Extract primary keyword from title and tags intelligently."""
    # Priority 1: Use tags as keyword source if they're descriptive
    # Priority 2: Extract meaningful phrase from title
    
    # Common stop words
    stop = {"a", "an", "the", "for", "in", "of", "to", "your", "is", "are", 
            "why", "what", "how", "that", "this", "with", "and", "or", "but",
            "not", "all", "be", "have", "has", "do", "does", "its", "it",
            "at", "on", "by", "from", "as", "no", "yes", "so", "if", "about",
            "into", "over", "after", "before", "between", "under", "above",
            "below", "out", "off", "up", "down", "just", "more", "most",
            "also", "very", "can", "will", "just", "should", "need", "needs",
            "which", "who", "whom", "when", "where", "their", "them", "they",
            "was", "were", "been", "being", "has", "had", "have", "does",
            "did", "done", "get", "got", "getting"}
    
    # Clean title
    title_lower = title.lower().replace(":", "").replace("—", " ").replace("-", " ").replace("'", "").replace('"', "").replace("?", "").replace("!", "")
    title_words = [w for w in title_lower.split() if w not in stop and len(w) > 1]
    
    # Try using tags first (they're usually better keywords)
    if tags:
        # Pick the most relevant tag (not just "Bangladesh", "2026" etc.)
        generic_tags = {"bangladesh", "2026", "digital marketing", "seo", "bd"}
        specific_tags = [t for t in tags if t.lower() not in generic_tags and len(t) > 3]
        if specific_tags:
            # Use the first specific tag
            candidate = specific_tags[0].lower()
            # Check if candidate appears in content with word boundaries
            return candidate
    
    # Fall back to title
    if len(title_words) >= 3:
        return " ".join(title_words[:3])
    elif len(title_words) >= 2:
        return " ".join(title_words[:2])
    elif title_words:
        return title_words[0]
    return title_lower.strip()

def count_phrase(content_lower, phrase):
    """Count occurrences of phrase with word boundaries, handling hyphenated forms."""
    count = 0
    # Exact phrase
    count += len(re.findall(r'\b' + re.escape(phrase) + r'\b', content_lower))
    # With hyphen variations (e.g., "e commerce" -> "e-commerce")
    if " " in phrase:
        hyphenated = phrase.replace(" ", "-")
        count += len(re.findall(r'\b' + re.escape(hyphenated) + r'\b', content_lower))
    return count

def check_tfidf(post_raw, content):
    title = get_field(post_raw, "title")
    tags = get_tags_linear(post_raw)
    
    keyword = extract_keywords(title, tags)
    content_lower = content.lower()
    
    exact_count = count_phrase(content_lower, keyword)
    
    # For shorter keywords, also check individual words all appearing
    words = keyword.split()
    if len(words) >= 2:
        # Check each word appears sufficiently
        min_word_count = min(content_lower.count(w) for w in words)
    else:
        min_word_count = exact_count
    
    return {
        "keyword": keyword,
        "occurrences": exact_count,
        "pass": exact_count >= 5 or min_word_count >= 10  # either phrase appears enough or all words appear enough
    }

def check_entities(post_raw, content):
    content_lower = content.lower()
    
    entities_to_check = {
        "Location: Dhaka": bool(re.search(r'\bdhaka\b', content_lower)),
        "Country: Bangladesh": bool(re.search(r'\bbangladesh\b', content_lower)),
    }
    
    service_types = {
        "local seo": ["local seo", "google business profile", "google maps", "gbp"],
        "technical seo": ["technical seo", "core web vital", "page speed"],
        "link building": ["link building", "backlink"],
        "content marketing": ["content marketing"],
        "geo": ["generative engine optimization", " geo ", "ai search"],
        "aeo": ["answer engine optimization", " aeo "],
    }
    
    detected_services = set()
    for svc, keywords in service_types.items():
        for kw in keywords:
            if kw in content_lower:
                detected_services.add(svc)
    
    missing_entities = [k for k, v in entities_to_check.items() if not v]
    
    return {
        "detected_services": sorted(detected_services),
        "missing_entities": missing_entities,
        "pass": len(missing_entities) == 0
    }

def check_pillar_link(post_raw, content):
    content_lower = content.lower()
    pillar_pages = [
        "/blog/complete-seo-guide-bangladesh-businesses-2026",
        "/services",
        "/about",
    ]
    
    found_pillar_links = [pp for pp in pillar_pages if pp.lower() in content_lower]
    
    tags = get_tags_linear(post_raw)
    
    return {
        "tags": tags,
        "pillar_links": found_pillar_links,
        "pass": len(found_pillar_links) > 0
    }

def check_aeo_geo(post_raw, content):
    faq_questions = re.findall(r'^#{1,3}\s+.*\?', content, re.MULTILINE)
    return {
        "question_heading_count": len(faq_questions),
        "pass": len(faq_questions) >= 2
    }

def check_internal_links(post_raw, content):
    internal_links = re.findall(r'\[([^\]]+)\]\((/[^)]+)\)', content)
    meaningful = [(text, url) for text, url in internal_links 
                  if url != "/" and "https://kanokmiah.com.bd" not in url and "http" not in url]
    return {
        "total_internal_links": len(meaningful),
        "pass": len(meaningful) >= 3
    }

def check_schema(post_raw, content):
    title = get_field(post_raw, "title")
    excerpt = get_field(post_raw, "excerpt")
    date = get_field(post_raw, "date")
    author = get_field(post_raw, "author")
    
    missing = []
    if not title:
        missing.append("title")
    if not excerpt:
        missing.append("excerpt")
    if not date:
        missing.append("date")
    if not author:
        missing.append("author")
    
    return {
        "fields": {"title": bool(title), "excerpt": bool(excerpt), "date": bool(date), "author": bool(author)},
        "missing": missing,
        "pass": len(missing) == 0
    }

# --- Run checks ---
results = []
for post in posts:
    slug = post["slug"]
    raw = post["raw"]
    content = get_content(raw)
    title = get_field(raw, "title")
    
    tfidf = check_tfidf(raw, content)
    entities = check_entities(raw, content)
    pillar = check_pillar_link(raw, content)
    aeo = check_aeo_geo(raw, content)
    internal = check_internal_links(raw, content)
    schema = check_schema(raw, content)
    
    result = {
        "slug": slug,
        "title": title,
        "checks": {
            "TF-IDF": tfidf,
            "Entities": entities,
            "Pillar Link": pillar,
            "AEO/GEO": aeo,
            "Internal Links": internal,
            "Schema Ready": schema,
        }
    }
    results.append(result)

# --- Print Markdown Report ---
pass_count = sum(1 for r in results if all(c["pass"] for c in r["checks"].values()))
fail_count = len(results) - pass_count

now = __import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')

print(f"# 📊 Content Framework Audit — kanokmiah.com.bd")
print(f"**Date:** {now} | **Posts checked:** {len(results)}")
print(f"**All checks passed:** {pass_count} ✅ | **Failures:** {fail_count} ❌")
print()

# --- Summary Table ---
print("## 📋 Summary Statistics")
print()
all_tfidf_pass = sum(1 for r in results if r["checks"]["TF-IDF"]["pass"])
all_entities_pass = sum(1 for r in results if r["checks"]["Entities"]["pass"])
all_pillar_pass = sum(1 for r in results if r["checks"]["Pillar Link"]["pass"])
all_aeo_pass = sum(1 for r in results if r["checks"]["AEO/GEO"]["pass"])
all_links_pass = sum(1 for r in results if r["checks"]["Internal Links"]["pass"])
all_schema_pass = sum(1 for r in results if r["checks"]["Schema Ready"]["pass"])

print(f"| Check | ✅ Pass | ❌ Fail | Pass Rate |")
print(f"|-------|--------|--------|-----------|")
total = len(results)
print(f"| TF-IDF Coverage | {all_tfidf_pass} | {total - all_tfidf_pass} | {all_tfidf_pass/total*100:.0f}% |")
print(f"| Entity Coverage | {all_entities_pass} | {total - all_entities_pass} | {all_entities_pass/total*100:.0f}% |")
print(f"| Pillar Link | {all_pillar_pass} | {total - all_pillar_pass} | {all_pillar_pass/total*100:.0f}% |")
print(f"| AEO/GEO Questions | {all_aeo_pass} | {total - all_aeo_pass} | {all_aeo_pass/total*100:.0f}% |")
print(f"| Internal Links | {all_links_pass} | {total - all_links_pass} | {all_links_pass/total*100:.0f}% |")
print(f"| Schema Readiness | {all_schema_pass} | {total - all_schema_pass} | {all_schema_pass/total*100:.0f}% |")
print()

# --- Detail: Failed posts ---
failed_posts = [r for r in results if not all(c["pass"] for c in r["checks"].values())]
if failed_posts:
    print(f"## ❌ Posts Requiring Attention ({len(failed_posts)})")
    print()
    for r in failed_posts:
        print(f"### {r['slug']}")
        print(f"**Title:** {r['title']}")
        print()
        print(f"| Check | Status | Details |")
        print(f"|-------|--------|---------|")
        for ck, cv in r["checks"].items():
            if ck == "TF-IDF":
                kw = cv.get("keyword", "")
                occ = cv.get("occurrences", 0)
                status = "✅" if cv["pass"] else "❌"
                detail = f"Keyword '{kw}' — {occ} occurrences{' (need ≥ 5)' if not cv['pass'] else ''}"
                print(f"| TF-IDF ({kw}) | {status} | {detail} |")
            elif ck == "Entities":
                missing = cv.get("missing_entities", [])
                status = "✅" if cv["pass"] else "❌"
                detail = f"Missing: {', '.join(missing) if missing else 'None'}"
                if cv.get("detected_services"):
                    detail += f" | Services: {', '.join(cv['detected_services'])}"
                print(f"| Entities | {status} | {detail} |")
            elif ck == "Pillar Link":
                status = "✅" if cv["pass"] else "❌"
                detail = f"Links to: {', '.join(cv['pillar_links']) if cv['pillar_links'] else 'None'}"
                print(f"| Pillar Link | {status} | {detail} |")
            elif ck == "AEO/GEO":
                status = "✅" if cv["pass"] else "❌"
                detail = f"{cv['question_heading_count']} question headings{' (need ≥ 2)' if not cv['pass'] else ''}"
                print(f"| AEO/GEO | {status} | {detail} |")
            elif ck == "Internal Links":
                status = "✅" if cv["pass"] else "❌"
                detail = f"{cv['total_internal_links']} total{' (need ≥ 3)' if not cv['pass'] else ''}"
                print(f"| Internal Links | {status} | {detail} |")
            elif ck == "Schema Ready":
                missing = cv.get("missing", [])
                status = "✅" if cv["pass"] else "❌"
                detail = f"Missing: {', '.join(missing) if missing else 'All fields set'}"
                print(f"| Schema Ready | {status} | {detail} |")
        
        print()
        print("**Fix instructions:**")
        for ck, cv in r["checks"].items():
            if not cv["pass"]:
                if ck == "TF-IDF":
                    print(f"- 🔑 **TF-IDF**: Increase usage of keyword '{cv['keyword']}' — currently {cv.get('occurrences', 0)} occurrences, target ≥ 5.")
                elif ck == "Entities":
                    print(f"- 🏷️ **Entities**: Add missing entities: {', '.join(cv.get('missing_entities', []))}")
                elif ck == "Pillar Link":
                    print(f"- 🔗 **Pillar Link**: Add link to /blog/complete-seo-guide-bangladesh-businesses-2026, /services, or /about")
                elif ck == "AEO/GEO":
                    print(f"- 💬 **AEO/GEO**: Add more question-based headings — currently {cv['question_heading_count']}, target ≥ 2")
                elif ck == "Internal Links":
                    print(f"- 🔗 **Internal Links**: Add more internal links — currently {cv['total_internal_links']}, target ≥ 3")
                elif ck == "Schema Ready":
                    print(f"- 📋 **Schema**: Set missing fields: {', '.join(cv.get('missing', []))}")
        print()

# --- Passing posts ---
passed_posts = [r for r in results if all(c["pass"] for c in r["checks"].values())]
if passed_posts:
    print(f"## ✅ Posts Passing All Checks ({len(passed_posts)})")
    for r in passed_posts:
        kw = r["checks"]["TF-IDF"]["keyword"]
        occ = r["checks"]["TF-IDF"]["occurrences"]
        aeo_cnt = r["checks"]["AEO/GEO"]["question_heading_count"]
        links = r["checks"]["Internal Links"]["total_internal_links"]
        print(f"- `{r['slug']}` — kw:'{kw}'({occ}) aeo:{aeo_cnt} links:{links}")

print()
print("---")
print(f"*Report generated by Content Framework Enforcer — {now}*")
