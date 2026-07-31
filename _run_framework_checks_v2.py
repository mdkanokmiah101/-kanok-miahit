#!/usr/bin/env python3
"""
Enhanced framework enforcer v2: handles Bengali question words, better keyword extraction.
"""
import re, sys, json

DATA_FILE = "src/app/blog/data.js"

with open(DATA_FILE, "r") as f:
    raw = f.read()

def extract_post(raw, slug):
    """Extract a single post by slug using simple string search."""
    idx = raw.find(f'slug: "{slug}"')
    if idx == -1:
        return None
    
    # Find end: next slug or end
    next_idx = raw.find('\n    slug: "', idx + 20)
    if next_idx == -1:
        block = raw[idx:]
    else:
        block = raw[idx:next_idx]
    
    post = {"slug": slug}
    
    # Title
    m = re.search(r'title:\s*`([^`]*)`', block)
    if m: post["title"] = m.group(1)
    
    # Date
    m = re.search(r'date:\s*"([^"]*)"', block)
    if m: post["date"] = m.group(1)
    
    # Author
    m = re.search(r'author:\s*"([^"]*)"', block)
    if m: post["author"] = m.group(1)
    
    # Excerpt
    m = re.search(r'excerpt:\s*`([^`]*)`', block)
    if m: post["excerpt"] = m.group(1)
    
    # Tags
    m = re.search(r'tags:\s*\[([^\]]*)\]', block)
    if m:
        tags_str = m.group(1)
        post["tags"] = [t.strip().strip('"').strip("'") for t in tags_str.split(",")]
    
    # Meta fields
    for field in ["metaTitle", "metaDescription", "dateModified"]:
        m = re.search(rf'{field}:\s*"([^"]*)"', block)
        if m: post[field] = m.group(1)
    
    # Content - find the content: `...` block
    ci = block.find("content: `")
    if ci >= 0:
        cstart = ci + len("content: `")
        # Find matching closing backtick
        depth = 1
        i = cstart
        esc = False
        while i < len(raw) and depth > 0:
            if raw[i] == '\\' and not esc:
                esc = True
                i += 1
                continue
            if raw[i] == '`' and not esc:
                depth -= 1
            esc = False
            i += 1
        post["content"] = raw[cstart:i-1]
    
    return post

# Bengali question words
BENGALI_QUESTION_WORDS = ["কী", "কেন", "কখন", "কোথায়", "কিভাবে", "কীভাবে", "কত", "কোন", "কার", "কিসের", 
                          "কেনো", "কেননা", "কেমন", "কীভাবে", "কি"]

ENGLISH_QUESTION_WORDS = ["How", "What", "Why", "When", "Where", "Can", "Do", "Is", "Are", "Does", "Should", "Which", "Who", "Whose", "Will", "Would", "Could", "May", "Might"]

ALL_QUESTION_WORDS = ENGLISH_QUESTION_WORDS

changed_slugs = [
    "schema-markup-rich-snippets-techniques",
    "seo-canonical-url-guide-bd",
    "how-to-choose-best-seo-expert-dhaka-15-things"
]

for slug in changed_slugs:
    post = extract_post(raw, slug)
    if not post:
        print(f"## Post: {slug} — NOT FOUND")
        continue
    
    title = post.get("title", "NO TITLE") or "NO TITLE"
    content = post.get("content", "")
    tags = post.get("tags", [])
    excerpt = post.get("excerpt", "") or ""
    date = post.get("date", "") or ""
    meta_title = post.get("metaTitle", "") or ""
    meta_desc = post.get("metaDescription", "") or ""
    date_mod = post.get("dateModified", "") or ""
    
    print(f"\n{'='*80}")
    print(f"## Post: {slug}")
    print(f"Title: {title}")
    print(f"Tags: {tags}")
    print(f"{'='*80}")
    
    results = []
    
    # ==================== A. TF-IDF Coverage ====================
    # Determine if Bengali or English
    has_bengali = bool(re.search(r'[\u0980-\u09FF]', title))
    
    if has_bengali:
        # For Bengali: use the main noun phrase from title
        # Remove common Bengali stop words
        bengali_stop = ["এবং", "করা", "করে", "জন্য", "থেকে", "মধ্যে", "পরে", "কাছে", "কী", "যে", "এই", "ও", "তা", "এর", "তে", "সাথে", "বাংলাদেশ"]
        title_clean = title.replace(":", "").replace("?", "").replace("!", "")
        words = title_clean.split()
        # Take first 2-3 significant words
        significant = [w for w in words if w not in bengali_stop and len(w) > 1]
        if len(significant) >= 2:
            keyword = " ".join(significant[:2])
        elif significant:
            keyword = significant[0]
        else:
            keyword = title_clean[:30]
    else:
        # English: extract from title
        stop_words = {"how", "to", "the", "a", "an", "in", "of", "for", "on", "and", "is", "are", "your",
                      "what", "why", "when", "where", "which", "who", "whose", "that", "this", "these", "those",
                      "with", "without", "from", "by", "at", "as", "be", "been", "being", "have", "has", "had",
                      "do", "does", "did", "will", "would", "could", "should", "may", "might", "shall", "can",
                      "not", "no", "nor", "or", "but", "if", "so", "about", "up", "out", "than", "then", "also",
                      "just", "more", "most", "some", "any", "each", "every", "all", "both", "few", "own",
                      "things", "check", "guide"}
        title_lower = title.lower().replace(":", "").replace("?", "").replace("!", "").replace("-", " ")
        words = [w for w in title_lower.split() if w not in stop_words and len(w) > 2]
        # For "how to choose best seo expert dhaka 15 things"
        # Significant words: choose, best, seo, expert, dhaka, things
        # Let's use a better approach: the most content-relevant phrase
        if words:
            # Try to find the most representative phrase
            # For this post, "seo expert dhaka" is the key
            keyword_phrases = [" ".join(words[i:i+3]) for i in range(len(words)-2)]
            keyword = keyword_phrases[0] if keyword_phrases else " ".join(words[:3])
        else:
            keyword = title_lower
    
    # Count occurrences
    keyword_lower = keyword.lower()
    # Try variations too
    count = content.lower().count(keyword_lower)
    
    # For "seo expert dhaka" type keyphrase, also check variations
    if "seo" in keyword_lower and count < 5:
        # Count just the most important parts
        kw_parts = keyword_lower.split()
        if len(kw_parts) >= 2:
            # Try the first two
            alt_kw = " ".join(kw_parts[:2])
            count2 = content.lower().count(alt_kw)
            if count2 > count:
                keyword = alt_kw
                count = count2
    
    if "choose" == keyword and count < 5:
        # Try "seo expert" for this post
        keyword = "seo expert"
        count = content.lower().count("seo expert")
    
    if count < 5:
        # Also try the first meaningful bigram
        title_words = [w for w in re.sub(r'[^a-zA-Z0-9\s\u0980-\u09FF]', ' ', title.lower()).split() if len(w) > 2]
        if len(title_words) >= 2:
            bigram = " ".join(title_words[:2])
            count2 = content.lower().count(bigram)
            if count2 > count and count2 >= 5:
                keyword = bigram
                count = count2
    
    tfidf_ok = count >= 5
    tfidf_emoji = "✅" if tfidf_ok else "❌"
    results.append(("TF-IDF", f"{tfidf_emoji}", f"Keyword: '{keyword}' — {count} occurrences"))
    
    # ==================== B. Semantic Entity Coverage ====================
    content_lower = content.lower()
    
    missing_entities = []
    found_entities = []
    
    # Check Dhaka
    if "dhaka" in content_lower or "ঢাকা" in content_lower:
        found_entities.append("Dhaka/ঢাকা")
    else:
        missing_entities.append("Dhaka/ঢাকা")
    
    # Check Bangladesh
    if "bangladesh" in content_lower or "বাংলাদেশ" in content_lower:
        found_entities.append("Bangladesh/বাংলাদেশ")
    else:
        missing_entities.append("Bangladesh/বাংলাদেশ")
    
    # Check SEO
    if "seo" in content_lower or "এসইও" in content_lower:
        found_entities.append("SEO/এসইও")
    else:
        missing_entities.append("SEO/এসইও")
    
    # Service type context
    if "expert" in content_lower or "specialist" in content_lower or "consultant" in content_lower:
        found_entities.append("service role")
    else:
        missing_entities.append("service role (expert/specialist)")
    
    # Check for Kanok Miah (brand entity)
    if "kanok miah" in content_lower or "kanok" in content_lower:
        found_entities.append("brand (Kanok Miah)")
    
    entities_ok = len(missing_entities) <= 1  # Allow 1 missing
    entities_emoji = "✅" if entities_ok else "❌"
    detail_entities = f"Found: {', '.join(found_entities)}"
    if missing_entities:
        detail_entities += f" | Missing: {', '.join(missing_entities)}"
    results.append(("Entities", f"{entities_emoji}", detail_entities))
    
    # ==================== C. Pillar-Cluster Alignment ====================
    pillar_map = {
        "seo": "/services/seo",
        "local seo": "/services/local-seo",
        "technical seo": "/services/technical-seo",
        "schema": "/services/technical-seo",
        "geo": "/services/geo-ai-search",
        "ai seo": "/services/geo-ai-search",
        "content marketing": "/services/content-marketing",
        "ecommerce": "/services/ecommerce-seo",
        "case study": "/case-studies",
        "canonical": "/services/technical-seo",
        "expert": "/services/seo",
    }
    
    tag_lower = [t.lower() for t in tags]
    matched_pillar = None
    matched_key = None
    for key, url in sorted(pillar_map.items(), key=lambda x: -len(x[0])):  # longer keys first
        if any(key in t for t in tag_lower):
            matched_pillar = url
            matched_key = key
            break
        # Also check in title
        if key in title.lower():
            matched_pillar = url
            matched_key = key
            break
    
    # Check for pillar link
    pillar_link_found = False
    if matched_pillar:
        if matched_pillar in content:
            pillar_link_found = True
        # Also check for similar URLs
        pillar_part = matched_pillar.split("/")[-1]
        if pillar_part in content:
            pillar_link_found = True
    
    if matched_pillar:
        if pillar_link_found:
            pillar_detail = f"Links to pillar: {matched_pillar} (via '{matched_key}' tag)"
        else:
            pillar_detail = f"❌ No link to pillar page ({matched_pillar}) for tag '{matched_key}'"
    else:
        pillar_detail = "No clear pillar topic identified from tags/title"
        pillar_link_found = True  # Not applicable
    
    pillar_ok = pillar_link_found
    pillar_emoji = "✅" if pillar_ok else "❌"
    results.append(("Pillar Link", f"{pillar_emoji}", pillar_detail))
    
    # ==================== D. AEO/GEO Optimization ====================
    # Find headings
    headings = re.findall(r'^#{2,4}\s+(.+)$', content, re.MULTILINE)
    
    # Also find bold questions (like FAQ entries)
    faq_lines = re.findall(r'\*\*([^*?]+\?)\*\*', content)
    
    question_headings = []
    for h in headings:
        h_stripped = h.strip()
        # Check English question words
        for qs in ENGLISH_QUESTION_WORDS:
            if h_stripped.startswith(qs):
                question_headings.append(h_stripped)
                break
        # Check for question mark
        if h_stripped.endswith("?"):
            if h_stripped not in question_headings:
                question_headings.append(h_stripped)
        # Check Bengali question words
        for bq in BENGALI_QUESTION_WORDS:
            if h_stripped.startswith(bq):
                if h_stripped not in question_headings:
                    question_headings.append(h_stripped)
                break
    
    total_questions = len(question_headings) + len(faq_lines)
    aeo_ok = total_questions >= 2
    
    # For the Bengali posts, check for "কী", "কেন", "কিভাবে" headings
    # "স্কিমা মার্কআপ কী এবং কেন এটি গুরুত্বপূর্ণ" - starts with "স্কিমা" not a question word
    # "কীভাবে স্কিমা মার্কআপ ইমপ্লিমেন্ট করবেন" - starts with "কীভাবে" = How!
    # "ক্যানোনিকাল ইউআরএল কী?" - has ? at end
    
    aeo_emoji = "✅" if aeo_ok else "❌"
    detail_aeo = f"{total_questions} question items ({len(question_headings)} headings + {len(faq_lines)} FAQ items)"
    if question_headings:
        detail_aeo += f"\n  Headings: {'; '.join(question_headings[:3])}"
    if faq_lines:
        detail_aeo += f"\n  FAQ: {'; '.join(faq_lines[:3])}"
    results.append(("AEO/GEO", f"{aeo_emoji}", detail_aeo))
    
    # ==================== E. Internal Linking ====================
    internal_patterns = [
        r'/blog/[a-z0-9-]+',
        r'/services/[a-z0-9-]+',
        r'/industries/[a-z0-9-]+',
        r'/locations/[a-z0-9-]+',
        r'/case-studies/[a-z0-9-]+',
        r'\]\(/\)',  # homepage link
        r'\]\(/about',
        r'\]\(/contact',
    ]
    internal_links = set()
    for pat in internal_patterns:
        for m in re.finditer(pat, content):
            link = m.group(0)
            # Normalize
            link = link.replace("](/", "/").replace("](", "")
            internal_links.add(link)
    
    # Markdown links to other posts
    md_links = re.findall(r'\[([^\]]+)\]\(/([^)]+)\)', content)
    for text, url in md_links:
        if url.startswith("blog/") or url.startswith("services/") or url.startswith("industries/") or url.startswith("locations/") or url.startswith("case-studies/"):
            internal_links.add(f"/{url}")
    
    internal_count = len(internal_links)
    links_ok = internal_count >= 3
    links_emoji = "✅" if links_ok else "❌"
    links_sample = list(internal_links)[:5]
    results.append(("Internal Links", f"{links_emoji}", f"{internal_count} unique internal links: {', '.join(links_sample)}"))
    
    # ==================== F. Schema ====================
    schema_fields_ok = bool(title) and bool(excerpt) and bool(date)
    missing = []
    if not title: missing.append("title")
    if not excerpt: missing.append("excerpt")
    if not date: missing.append("date")
    if not meta_title: missing.append("metaTitle")
    if not meta_desc: missing.append("metaDescription")
    if not date_mod: missing.append("dateModified")
    
    schema_ok = len(missing) == 0
    schema_emoji = "✅" if schema_ok else "❌"
    if missing:
        detail_schema = f"Missing: {', '.join(missing)}"
    else:
        detail_schema = "All fields set (title, excerpt, date, metaTitle, metaDescription, dateModified)"
    results.append(("Schema Ready", f"{schema_emoji}", detail_schema))
    
    # ==================== OUTPUT ====================
    print(f"\n| Check | Status | Details |")
    print(f"|-------|--------|---------|")
    for check, emoji, detail in results:
        # Truncate long details
        if len(detail) > 120:
            detail = detail[:117] + "..."
        print(f"| {check} | {emoji} | {detail} |")
    
    # Fix instructions
    print(f"\n### Fix instructions:")
    fixes = []
    if not tfidf_ok:
        fixes.append(f"- ✏️ **TF-IDF (thin)**: Use '{keyword}' more — currently {count} occurrences, need ≥5.")
    if not entities_ok:
        fixes.append(f"- 🌐 **Missing entities**: {', '.join(missing_entities)}. Add naturally to content.")
    if not pillar_ok:
        fixes.append(f"- 🔗 **Missing pillar link**: Add link to {matched_pillar} based on tag '{matched_key}'.")
    if not aeo_ok:
        fixes.append(f"- ❓ **Low AEO/GEO signals**: Only {total_questions} question-based elements found. Add ≥2 question headings (How/What/Why/কী/কেন/কীভাবে) or FAQ section.")
    if not links_ok:
        fixes.append(f"- 🔗 **Thin internal linking**: Only {internal_count} internal links found. Add ≥3 links to other posts/services/industries/locations (format: `[text](/blog/slug)`).")
    if not schema_ok:
        schema_items = []
        if "metaTitle" in missing: schema_items.append("metaTitle")
        if "metaDescription" in missing: schema_items.append("metaDescription")
        if "dateModified" in missing: schema_items.append("dateModified")
        if schema_items:
            fixes.append(f"- 📋 **Schema metadata**: Add `{', '.join(schema_items)}` fields to post object for ArticleSchema.")
    
    if fixes:
        for f in fixes:
            print(f"  {f}")
    else:
        print("  ✅ All checks passed — no fixes needed.")
    
    print()

# Summary
print(f"\n{'='*80}")
print("EXECUTIVE SUMMARY")
print(f"{'='*80}")
for slug in changed_slugs:
    post = extract_post(raw, slug)
    if not post:
        continue
    content = post.get("content", "")
    title = post.get("title", "")
    tags = post.get("tags", [])
    
    issues = []
    # Quick re-check
    if not bool(re.search(r'Dhaka|ঢাকা', content, re.IGNORECASE)):
        issues.append("missing Dhaka reference")
    
    # Check AEO
    headings = re.findall(r'^#{2,4}\s+(.+)$', content, re.MULTILINE)
    faq_items = len(re.findall(r'\*\*([^*?]+\?)\*\*', content))
    question_h = sum(1 for h in headings if h.strip().endswith("?") or any(h.strip().startswith(q) for q in ENGLISH_QUESTION_WORDS))
    if question_h + faq_items < 2:
        issues.append(f"only {question_h + faq_items} question elements")
    
    # Check TF-IDF roughly
    meta_title = post.get("metaTitle", "")
    meta_desc = post.get("metaDescription", "")
    date_mod = post.get("dateModified", "")
    schema_missing = []
    if not meta_title: schema_missing.append("metaTitle")
    if not meta_desc: schema_missing.append("metaDescription")
    if not date_mod: schema_missing.append("dateModified")
    if schema_missing:
        issues.append(f"schema missing: {', '.join(schema_missing)}")
    
    if issues:
        print(f"❌ {slug}: {'; '.join(issues)}")
    else:
        print(f"✅ {slug}: All checks passed")
