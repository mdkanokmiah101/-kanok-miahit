#!/usr/bin/env python3
"""
Content Framework Enforcer for kanokmiah.com.bd
Checks: TF-IDF, Entities, Pillar-Cluster, AEO/GEO, Internal Links, Schema
"""
import re
import json
import sys

DATA_FILE = "src/app/blog/data.js"

with open(DATA_FILE, "r") as f:
    raw = f.read()

BENGALI_QWORDS = [
    "\u0995\u09c0",       # কী
    "\u0995\u09c7\u09a8", # কেন
    "\u0995\u09cb\u09a5\u09be\u09af\u09bc", # কোথায়
    "\u0995\u09bf\u09ad\u09be\u09ac\u09c7", # কিভাবে
    "\u0995\u09c0\u09ad\u09be\u09ac\u09c7", # কীভাবে
    "\u0995\u09a4",       # কত
    "\u0995\u09cb\u09a8", # কোন
    "\u0995\u09c7\u09ae\u09a8", # কেমন
]
ENGLISH_QWORDS = ["How", "What", "Why", "When", "Where", "Can", "Do", "Is", "Are", "Does", "Should", "Which", "Who", "Will", "Would", "Could"]
ALL_QWORDS = ENGLISH_QWORDS + BENGALI_QWORDS

def extract_post(raw, slug):
    idx = raw.find('slug: "' + slug + '"')
    if idx == -1:
        return None
    next_idx = raw.find('\n    slug: "', idx + 20)
    block = raw[idx:next_idx] if next_idx != -1 else raw[idx:]

    post = {"slug": slug}
    m = re.search(r'title:\s*`([^`]*)`', block)
    if m: post["title"] = m.group(1)
    if "title" not in post:
        m = re.search(r'title:\s*"([^"]*)"', block)
        if m: post["title"] = m.group(1)
    m = re.search(r'date:\s*"([^"]*)"', block)
    if m: post["date"] = m.group(1)
    m = re.search(r'excerpt:\s*`([^`]*)`', block)
    if m: post["excerpt"] = m.group(1)
    if "excerpt" not in post:
        m = re.search(r'excerpt:\s*"([^"]*)"', block)
        if m: post["excerpt"] = m.group(1)
    m = re.search(r'tags:\s*\[([^\]]*)\]', block)
    if m:
        post["tags"] = [t.strip().strip('"').strip("'") for t in m.group(1).split(",")]
    for field in ["metaTitle", "metaDescription", "dateModified"]:
        m = re.search(rf'{field}:\s*"([^"]*)"', block)
        if m: post[field] = m.group(1)
    ci = block.find("content: `")
    if ci >= 0:
        cstart = ci + len("content: `")
        # Find the closing backtick — it's the last backtick before end-of-object marker
        # Pattern: backtick, then comma/newline, then closing brace
        # Use the block (not raw) to avoid boundary issues
        rest = block[cstart:]
        # Strategy: find all backtick positions in rest
        bt_positions = [i for i, ch in enumerate(rest) if ch == "`"]
        if bt_positions:
            # The closing backtick is at one of these positions
            # Look for pattern: backtick, comma/whitespace/newline, closing brace
            for pos in reversed(bt_positions):
                after = rest[pos+1:pos+10]
                # Check if followed by ,\n  } or similar object-end pattern
                if re.match(r'^\s*,\s*\n\s*\}', after) or re.match(r'^\s*,\s*\n\s*\n', after) or re.match(r'^\s*\n\s*\}', after):
                    post["content"] = rest[:pos]
                    break
            else:
                # Fallback: use last backtick
                post["content"] = rest[:bt_positions[-1]]
    return post

def check_post(post):
    if not post:
        return None
    title = post.get("title", "") or ""
    content = post.get("content", "") or ""
    tags = post.get("tags", []) or []
    excerpt = post.get("excerpt", "") or ""
    date = post.get("date", "") or ""
    meta_title = post.get("metaTitle", "") or ""
    meta_desc = post.get("metaDescription", "") or ""
    date_mod = post.get("dateModified", "") or ""
    slug = post["slug"]

    cl = content.lower()
    has_bn = bool(re.search(r'[\u0980-\u09FF]', title))

    # === A. TF-IDF ===
    kw = title[:30]
    count = 0
    
    if has_bn:
        parts = re.sub(r'[:?!\u2013\u2014]', ' ', title).split()
        sig = [w for w in parts if len(w) > 1 and w not in ["\u098f\u09ac\u0982","\u0995\u09b0\u09be","\u0995\u09b0\u09c7","\u099c\u09a8\u09cd\u09af","\u09a5\u09c7\u0995\u09c7","\u09ae\u09a7\u09cd\u09af\u09c7","\u09aa\u09b0\u09c7","\u0995\u09be\u099b\u09c7","\u0995\u09c0","\u09af\u09c7","\u098f\u0987","\u0993","\u09a4\u09be","\u098f\u09b0"]]
        if len(sig) >= 2: kw = " ".join(sig[:2])
        elif sig: kw = sig[0]
        count = cl.count(kw)
    else:
        stopw = {"how","to","the","a","an","in","of","for","on","and","is","are","your","what","why","when","where","which","who","that","this","these","those","with","without","from","by","at","as","be","have","has","do","does","did","will","would","could","should","may","might","shall","can","not","no","nor","or","but","if","so","about","up","out","than","then","also","just","more","most","some","any","each","every","all","both","few","own","things","check","guide","choose"}
        tw = [w for w in re.sub(r'[:?!\-]', ' ', title.lower()).split() if w not in stopw and len(w) > 2]
        # Generate candidate keywords at various lengths and pick most frequent
        candidates = []
        if len(tw) >= 1: candidates.append(" ".join(tw[:1]))
        if len(tw) >= 2: candidates.append(" ".join(tw[:2]))
        if len(tw) >= 3: candidates.append(" ".join(tw[:3]))
        if len(tw) >= 4: candidates.append(" ".join(tw[:4]))
        # Also try phrase from title with SEO context
        tl = title.lower()
        if "seo" in tl and "expert" in tl:
            candidates.append("seo expert")
            if "dhaka" in tl:
                candidates.append("seo expert in dhaka")
        # Score candidate keywords
        best_kw, best_count = "", 0
        for cand in candidates:
            cc = cl.count(cand)
            if cc > best_count:
                best_count, best_kw = cc, cand
        kw, count = best_kw, best_count
    
    if count < 3:
        twords = [w for w in re.sub(r'[^a-zA-Z0-9\s\u0980-\u09FF]', ' ', title.lower()).split() if len(w) > 2]
        if len(twords) >= 2:
            bigram = " ".join(twords[:2])
            c2 = cl.count(bigram)
            if c2 > count:
                kw, count = bigram, c2

    tfidf_ok = count >= 5

    # === B. Entities ===
    missing_ent, found_ent = [], []
    if "dhaka" in cl or "\u09a2\u09be\u0995\u09be" in cl:
        found_ent.append("Dhaka")
    else:
        missing_ent.append("Dhaka")
    if "bangladesh" in cl or "\u09ac\u09be\u0982\u09b2\u09be\u09a6\u09c7\u09b6" in cl or "\u09ac\u09be\u0982\u09b2\u09be\u09a6\u09c7\u09b6" in cl:
        found_ent.append("Bangladesh")
    else:
        missing_ent.append("Bangladesh")
    if "seo" in cl:
        found_ent.append("SEO")
    else:
        missing_ent.append("SEO")
    if any(w in cl for w in ["expert", "specialist", "consultant", "services"]):
        found_ent.append("service_role")
    else:
        missing_ent.append("service_role")
    if "kanok" in cl:
        found_ent.append("brand_Kanok_Miah")
    ent_ok = len(missing_ent) <= 1

    # === C. Pillar ===
    pm = {
        "technical seo": "/services/technical-seo",
        "canonical": "/services/technical-seo",
        "schema": "/services/technical-seo",
        "local seo": "/services/local-seo",
        "seo expert": "/services/seo",
        "seo": "/services/seo",
        "geo": "/services/geo-ai-search",
        "ai seo": "/services/geo-ai-search",
        "case study": "/case-studies",
        "expert": "/services/seo",
        "structured data": "/services/technical-seo",
    }
    tag_str = " ".join(t.lower() for t in tags)
    mp, mk = None, None
    for key, url in sorted(pm.items(), key=lambda x: -len(x[0])):
        if key in tag_str or key in title.lower():
            mp, mk = url, key
            break
    plf = False
    if mp:
        if mp in content:
            plf = True
        else:
            sp = mp.split("/")[-1]
            if sp in content:
                plf = True

    # === D. AEO/GEO ===
    headings = re.findall(r'^#{2,4}\s+(.+)$', content, re.MULTILINE)
    faq_items = re.findall(r'\*\*([^*?]+\?)\*\*', content)
    qh = []
    for h in headings:
        hs = h.strip()
        if hs.endswith("?"):
            qh.append(hs)
            continue
        for q in ALL_QWORDS:
            if h.startswith(q):
                qh.append(hs)
                break
    total_q = len(qh) + len(faq_items)
    aeo_ok = total_q >= 2

    # === E. Internal Links ===
    il_pats = [r'/blog/[a-z0-9-]+', r'/services/[a-z0-9-]+', r'/industries/[a-z0-9-]+', r'/locations/[a-z0-9-]+', r'/case-studies/']
    ilinks = set()
    for pat in il_pats:
        for m in re.finditer(pat, content):
            ilinks.add(m.group(0))
    if "](/" in content:
        ilinks.add("/")
    il_count = len(ilinks)
    il_ok = il_count >= 3

    # === F. Schema ===
    schema_missing = []
    for fld, val in [("title", title), ("excerpt", excerpt), ("date", date), ("metaTitle", meta_title), ("metaDescription", meta_desc), ("dateModified", date_mod)]:
        if not val:
            schema_missing.append(fld)
    sc_ok = len(schema_missing) == 0

    return {
        "slug": slug,
        "title": title,
        "tfidf": {"ok": tfidf_ok, "keyword": kw, "count": count},
        "entities": {"ok": ent_ok, "found": found_ent, "missing": missing_ent},
        "pillar": {"ok": plf, "pillar_url": mp, "pillar_key": mk, "linked": plf},
        "aeo": {"ok": aeo_ok, "total_questions": total_q, "heading_qs": len(qh), "faq_items": len(faq_items)},
        "links": {"ok": il_ok, "count": il_count, "links": sorted(ilinks)},
        "schema": {"ok": sc_ok, "missing": schema_missing},
    }


# --- Main ---
changed_slugs = [
    "schema-markup-rich-snippets-techniques",
    "seo-canonical-url-guide-bd",
    "how-to-choose-best-seo-expert-dhaka-15-things",
]

results = []
for slug in changed_slugs:
    post = extract_post(raw, slug)
    result = check_post(post)
    results.append(result)

# Generate report
print("# Content Framework Enforcement Report — kanokmiah.com.bd\n")
print(f"Generated: automated cron run\n")

all_ok = True
for r in results:
    if r is None:
        print(f"## Post: UNKNOWN — Not found in data.js\n")
        all_ok = False
        continue

    print(f"## Post: `{r['slug']}`")
    print(f"**Title:** {r['title']}\n")

    print("| Check | Status | Details |")
    print("|-------|--------|---------|")

    # TF-IDF
    s = "✅" if r["tfidf"]["ok"] else "❌"
    print(f"| TF-IDF Coverage | {s} | Keyword: `{r['tfidf']['keyword']}` — {r['tfidf']['count']} occurrences {'(≥5 ✅)' if r['tfidf']['ok'] else '(<5 ❌)'} |")
    if not r["tfidf"]["ok"]:
        all_ok = False

    # Entities
    s = "✅" if r["entities"]["ok"] else "❌"
    detail = f"Found: {', '.join(r['entities']['found'])}"
    if r["entities"]["missing"]:
        detail += f" | Missing: {', '.join(r['entities']['missing'])}"
    print(f"| Semantic Entities | {s} | {detail} |")
    if not r["entities"]["ok"]:
        all_ok = False

    # Pillar
    s = "✅" if r["pillar"]["ok"] else "❌"
    if r["pillar"]["pillar_url"]:
        if r["pillar"]["linked"]:
            detail = f"Links to pillar: `{r['pillar']['pillar_url']}` (via tag: `{r['pillar']['pillar_key']}`)"
        else:
            detail = f"❌ No link to pillar page `{r['pillar']['pillar_url']}` (tag: `{r['pillar']['pillar_key']}`)"
    else:
        detail = "No specific pillar topic mapped from tags"
    print(f"| Pillar-Cluster | {s} | {detail} |")
    if not r["pillar"]["ok"]:
        all_ok = False

    # AEO/GEO
    s = "✅" if r["aeo"]["ok"] else "❌"
    detail = f"{r['aeo']['total_questions']} question-based elements ({r['aeo']['heading_qs']} headings + {r['aeo']['faq_items']} FAQ items)"
    if not r["aeo"]["ok"]:
        detail += " — need ≥2"
    print(f"| AEO/GEO | {s} | {detail} |")
    if not r["aeo"]["ok"]:
        all_ok = False

    # Internal Links
    s = "✅" if r["links"]["ok"] else "❌"
    link_sample = r["links"]["links"][:5]
    detail = f"{r['links']['count']} unique internal links"
    if not r["links"]["ok"]:
        detail += " — need ≥3"
    if link_sample:
        detail += f" (e.g., {', '.join(link_sample)})"
    print(f"| Internal Linking | {s} | {detail} |")
    if not r["links"]["ok"]:
        all_ok = False

    # Schema
    s = "✅" if r["schema"]["ok"] else "❌"
    if r["schema"]["ok"]:
        detail = "All 6 ArticleSchema fields set"
    else:
        detail = f"Missing: {', '.join(r['schema']['missing'])}"
    print(f"| Schema Ready | {s} | {detail} |")
    if not r["schema"]["ok"]:
        all_ok = False

    print()
    print("### Fix instructions:")
    fixes = []
    if not r["tfidf"]["ok"]:
        fixes.append(f"- ✏️ **TF-IDF thin**: Increase `{r['tfidf']['keyword']}` usage to ≥5 occurrences (currently {r['tfidf']['count']}). Add natural mentions in headings and body.")
    if not r["entities"]["ok"]:
        fixes.append(f"- 🌐 **Missing entities**: Add `{', '.join(r['entities']['missing'])}` naturally into the content (headings or body).")
    if not r["pillar"]["ok"]:
        fixes.append(f"- 🔗 **Missing pillar link**: Add a link to `{r['pillar']['pillar_url']}` — e.g., `[related service]({r['pillar']['pillar_url']})` — based on tag `{r['pillar']['pillar_key']}`.")
    if not r["aeo"]["ok"]:
        fixes.append(f"- ❓ **AEO/GEO** (Generative Engine Optimization): Add ≥2 question-format headings (starting with How/What/Why or Bengali কী/কেন/কীভাবে, ending with ?). Currently {r['aeo']['total_questions']}.")
    if not r["links"]["ok"]:
        fixes.append(f"- 🔗 **Internal linking thin**: Add ≥3 internal links to other posts (`/blog/...`), services (`/services/...`), industries (`/industries/...`), or locations (`/locations/...`). Currently {r['links']['count']}.")
    if not r["schema"]["ok"]:
        for m in r["schema"]["missing"]:
            fixes.append(f"- 📋 **Schema — {m}**: Add `{m}` field to the post object in data.js for proper ArticleSchema rendering.")
    if fixes:
        for f in fixes:
            print(f"  {f}")
    else:
        print("  ✅ No fixes needed for this post.")
    print("---\n")

# Executive summary
print("## Executive Summary\n")
passed = sum(1 for r in results if r and all(
    r[t]["ok"] for t in ["tfidf", "entities", "pillar", "aeo", "links", "schema"]
))
total = len(results)
print(f"**{passed}/{total} posts pass all checks**\n")

all_issues = []
for r in results:
    if r is None:
        continue
    issues = []
    if not r["tfidf"]["ok"]:
        issues.append(f"TF-IDF ({r['tfidf']['keyword']} x{r['tfidf']['count']})")
    if not r["entities"]["ok"]:
        issues.append(f"Entities missing: {', '.join(r['entities']['missing'])}")
    if not r["pillar"]["ok"]:
        issues.append(f"No pillar link to {r['pillar']['pillar_url']}")
    if not r["aeo"]["ok"]:
        issues.append(f"Only {r['aeo']['total_questions']} question elements")
    if not r["links"]["ok"]:
        issues.append(f"Only {r['links']['count']} internal links")
    if not r["schema"]["ok"]:
        issues.append(f"Schema missing: {', '.join(r['schema']['missing'])}")
    if issues:
        all_issues.append(f"- ❌ **{r['slug']}**: {'; '.join(issues)}")
    else:
        all_issues.append(f"- ✅ **{r['slug']}**: All checks passed")

for line in all_issues:
    print(line)

print()
if all_ok:
    print("**All checks pass — framework compliant.**")
else:
    print("**Some checks failed — fixes recommended above.**")
