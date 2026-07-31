#!/usr/bin/env python3
"""
Framework enforcer: reads blog data.js, extracts changed posts, runs all checks.
"""
import re, json, sys, math
from collections import Counter

DATA_FILE = "src/app/blog/data.js"

with open(DATA_FILE, "r") as f:
    raw = f.read()

# Parse posts — this is tricky because content uses backtick templates.
# We'll use a state-machine approach.

def parse_posts(text):
    """Parse JS array of post objects into list of dicts."""
    posts = []
    # Find slug first, then walk forward to extract fields
    pattern = r'slug:\s*"([^"]+)"'
    positions = [(m.start(), m.group(1)) for m in re.finditer(pattern, text)]
    
    for i, (pos, slug) in enumerate(positions):
        # Determine end: next slug or end of file
        end = positions[i+1][0] if i+1 < len(positions) else len(text)
        block = text[pos:end]
        
        post = {"slug": slug}
        
        # Extract title
        m = re.search(r'title:\s*`([^`]*)`\s*[,}]', block)
        if m: post["title"] = m.group(1)
        m = re.search(r'title:\s*"([^"]*)"\s*[,}]', block)
        if m: post["title"] = m.group(1)
        
        # Extract date
        m = re.search(r'date:\s*"([^"]*)"', block)
        if m: post["date"] = m.group(1)
        
        # Extract author
        m = re.search(r'author:\s*"([^"]*)"', block)
        if m: post["author"] = m.group(1)
        
        # Extract excerpt
        m = re.search(r'excerpt:\s*`([^`]*)`', block)
        if m: post["excerpt"] = m.group(1)
        m = re.search(r'excerpt:\s*"([^"]*)"', block)
        if m: post["excerpt"] = m.group(1)
        
        # Extract tags
        m = re.search(r'tags:\s*\[([^\]]*)\]', block)
        if m:
            tags_str = m.group(1)
            post["tags"] = [t.strip().strip('"').strip("'") for t in tags_str.split(",")]
        
        # Extract meta fields
        for field in ["metaTitle", "metaDescription", "dateModified"]:
            m = re.search(rf'{field}:\s*"([^"]*)"', block)
            if m: post[field] = m.group(1)
        
        # Extract content — find the content: `...` block
        # Content is the last big backtick block
        content_matches = list(re.finditer(r'content:\s*`((?:[^`\\]|\\.)*)`', block, re.DOTALL))
        if content_matches:
            # Use the last match (the actual content, not the placeholder image)
            post["content"] = content_matches[-1].group(1)
        
        posts.append(post)
    
    return posts

posts = parse_posts(raw)
print(f"Parsed {len(posts)} posts", file=sys.stderr)

changed_slugs = [
    "schema-markup-rich-snippets-techniques",
    "seo-canonical-url-guide-bd",
    "how-to-choose-best-seo-expert-dhaka-15-things"
]

target_posts = [p for p in posts if p["slug"] in changed_slugs]
print(f"Target posts: {[p['slug'] for p in target_posts]}", file=sys.stderr)

for p in target_posts:
    print(f"\n{'='*80}")
    print(f"## Post: {p['slug']}")
    print(f"{'='*80}")
    
    title = p.get("title", "NO TITLE")
    content = p.get("content", "")
    tags = p.get("tags", [])
    excerpt = p.get("excerpt", "")
    date = p.get("date", "")
    meta_title = p.get("metaTitle", "")
    meta_desc = p.get("metaDescription", "")
    date_mod = p.get("dateModified", "")
    
    print(f"Title: {title}")
    print(f"Tags: {tags}")
    print(f"Content length: {len(content)} chars")
    
    results = []
    
    # ==================== A. TF-IDF Coverage ====================
    # Extract primary keyword from title
    # Use the first meaningful noun phrase
    stop_words = {"how", "to", "the", "a", "an", "in", "of", "for", "on", "and", "is", "are", "your",
                  "what", "why", "when", "where", "which", "who", "whose", "that", "this", "these", "those",
                  "with", "without", "from", "by", "at", "as", "be", "been", "being", "have", "has", "had",
                  "do", "does", "did", "will", "would", "could", "should", "may", "might", "shall", "can",
                  "not", "no", "nor", "or", "but", "if", "so", "about", "up", "out", "than", "then", "also",
                  "just", "more", "most", "some", "any", "each", "every", "all", "both", "few", "own"}
    
    # Extract likely keyword: remove stopwords, take first multi-word phrase
    title_lower = title.lower().replace(":", "").replace("?", "").replace("!", "")
    words = [w for w in title_lower.split() if w not in stop_words and len(w) > 2]
    
    if words:
        # Primary keyword: first 2-3 meaningful words
        keyword = " ".join(words[:3])
        # But also try to match whole phrases
        # Count occurrences - try the full phrase, then individual words
        keyword_lower = keyword.lower()
        count = content.lower().count(keyword_lower)
        
        # If very low count, try shorter versions
        if count < 3 and len(words) >= 2:
            keyword = " ".join(words[:2])
            keyword_lower = keyword.lower()
            count = content.lower().count(keyword_lower)
        
        if count < 3 and len(words) >= 1:
            keyword = words[0]
            keyword_lower = keyword.lower()
            count = content.lower().count(keyword_lower)
    else:
        keyword = title_lower
        count = content.lower().count(keyword)
    
    tfidf_ok = count >= 5
    tfidf_emoji = "✅" if tfidf_ok else "❌"
    results.append(("TF-IDF", f"{tfidf_emoji}", f"Keyword: '{keyword}' — {count} occurrences"))
    
    # ==================== B. Semantic Entity Coverage ====================
    entities = {
        "location_dhaka": "Dhaka",
        "location_bangladesh": "Bangladesh",
        "service_seo": "SEO",
    }
    
    # Add specific entities based on content context
    content_lower = content.lower()
    
    missing_entities = []
    found_entities = []
    
    # Check Dhaka
    if "dhaka" in content_lower:
        found_entities.append("Dhaka")
    else:
        missing_entities.append("Dhaka")
    
    # Check Bangladesh
    if "bangladesh" in content_lower:
        found_entities.append("Bangladesh")
    else:
        missing_entities.append("Bangladesh")
    
    # Check SEO
    if "seo" in content_lower:
        found_entities.append("SEO")
    else:
        missing_entities.append("SEO")
    
    # Check for service-specific terms based on title/tags
    service_terms = ["expert", "consultant", "specialist", "services", "agency", "professional"]
    found_services = [t for t in service_terms if t in content_lower]
    if found_services:
        found_entities.extend(found_services[:2])
    else:
        missing_entities.append("service term (expert/consultant/specialist)")
    
    # Industry-specific
    if tags:
        for tag in tags:
            tag_lower = tag.lower()
            if tag_lower not in content_lower and len(tag_lower) > 4:
                # Tag should appear somewhere
                pass  # too strict
    
    entities_ok = len(missing_entities) < 2
    entities_emoji = "✅" if entities_ok else "❌"
    details = f"Found: {', '.join(found_entities[:5])}"
    if missing_entities:
        details += f" | Missing: {', '.join(missing_entities)}"
    results.append(("Entities", f"{entities_emoji}", details))
    
    # ==================== C. Pillar-Cluster Alignment ====================
    # Determine pillar topic based on tags
    pillar_pages = {
        "seo": "/services/seo",
        "local seo": "/services/local-seo",
        "technical seo": "/services/technical-seo",
        "geo": "/services/geo-ai-search",
        "ai seo": "/services/geo-ai-search",
        "content marketing": "/services/content-marketing",
        "ecommerce": "/services/ecommerce-seo",
        "garments": "/industries/garments-textile",
        "textile": "/industries/garments-textile",
        "real estate": "/industries/real-estate",
        "healthcare": "/industries/healthcare",
        "case study": "/case-studies",
    }
    
    tag_lower = [t.lower() for t in tags]
    matched_pillar = None
    for key, url in pillar_pages.items():
        if any(key in t for t in tag_lower):
            matched_pillar = url
            break
    
    # Check if post links to the pillar page
    pillar_link_found = False
    if matched_pillar:
        # Check for the pillar URL in content
        if matched_pillar in content:
            pillar_link_found = True
        # Also check for markdown links containing the pillar slug
        pillar_slug = matched_pillar.split("/")[-1]
        if pillar_slug in content:
            pillar_link_found = True
    
    # Also check for pillar-like structure
    if not matched_pillar:
        pillar_check = "No clear pillar topic identified"
    elif pillar_link_found:
        pillar_check = f"Links to pillar: {matched_pillar}"
    else:
        pillar_check = f"❌ No link to pillar page ({matched_pillar})"
    
    pillar_ok = matched_pillar is None or pillar_link_found
    pillar_emoji = "✅" if pillar_ok else "❌"
    results.append(("Pillar Link", f"{pillar_emoji}", pillar_check))
    
    # ==================== D. AEO/GEO Optimization ====================
    question_starts = ["How", "What", "Why", "When", "Where", "Can", "Do", "Is", "Are", "Does", "Should", "Which"]
    question_headings = []
    
    # Find headings (## heading, ### heading, etc.)
    heading_pattern = re.findall(r'#{2,4}\s+([^\n]+)', content)
    for h in heading_pattern:
        h_stripped = h.strip()
        for qs in question_starts:
            if h_stripped.startswith(qs) and h_stripped.endswith("?"):
                question_headings.append(h_stripped)
                break
    
    aeo_ok = len(question_headings) >= 2
    aeo_emoji = "✅" if aeo_ok else "❌"
    results.append(("AEO/GEO", f"{aeo_emoji}", f"{len(question_headings)} question-based headings"))
    if question_headings:
        results[-1] = ("AEO/GEO", f"{aeo_emoji}", f"{len(question_headings)} question-based headings: " + "; ".join(question_headings[:3]))
    
    # ==================== E. Internal Linking ====================
    # Count internal links: /blog/, /services/, /industries/, /locations/, /case-studies/, /about, /contact
    internal_link_patterns = [
        r'/blog/[a-z0-9-]+',
        r'/services/[a-z0-9-]+',
        r'/industries/[a-z0-9-]+',
        r'/locations/[a-z0-9-]+',
        r'/case-studies/[a-z0-9-]+',
        r'/about(?:[)"\s]|$)',
        r'/contact(?:[)"\s]|$)',
    ]
    internal_links = []
    for pat in internal_link_patterns:
        found = re.findall(pat, content)
        internal_links.extend(found)
    
    # Deduplicate
    internal_links = list(set(internal_links))
    
    links_ok = len(internal_links) >= 3
    links_emoji = "✅" if links_ok else "❌"
    results.append(("Internal Links", f"{links_emoji}", f"{len(internal_links)} internal links: {', '.join(internal_links[:5])}"))
    
    # ==================== F. Schema ====================
    schema_fields = {"title": bool(title), "excerpt": bool(excerpt), "date": bool(date)}
    missing_schema = [k for k, v in schema_fields.items() if not v]
    
    # Check for metaTitle, metaDescription, dateModified
    if meta_title:
        schema_fields["metaTitle"] = True
    else:
        missing_schema.append("metaTitle")
    
    if meta_desc:
        schema_fields["metaDescription"] = True
    else:
        missing_schema.append("metaDescription")
    
    if date_mod:
        schema_fields["dateModified"] = True
    else:
        missing_schema.append("dateModified")
    
    schema_ok = len(missing_schema) == 0
    schema_emoji = "✅" if schema_ok else "❌"
    details_schema = "All fields set" if schema_ok else f"Missing: {', '.join(missing_schema)}"
    results.append(("Schema Ready", f"{schema_emoji}", details_schema))
    
    # ==================== OUTPUT TABLE ====================
    print(f"\n{'| Check | Status | Details |':-^80}")
    print(f"{'|-------|--------|---------|':-^80}")
    for check, emoji, detail in results:
        print(f"| {check} | {emoji} | {detail} |")
    
    # ==================== FIX INSTRUCTIONS ====================
    print(f"\n### Fix instructions:")
    fixes = []
    if not tfidf_ok:
        fixes.append(f"- ✏️ **TF-IDF**: Increase usage of '{keyword}' to at least 5 times (currently {count}). Add more natural mentions in headings and body text.")
    if not entities_ok:
        fixes.append(f"- 🌐 **Entities**: Add missing entities: {', '.join(missing_entities)}. These should be naturally integrated into the content.")
    if not pillar_ok and matched_pillar:
        fixes.append(f"- 🔗 **Pillar Link**: Add a link to the pillar page ({matched_pillar}) in the content. Place it naturally in a relevant section.")
    if not aeo_ok:
        fixes.append(f"- ❓ **AEO/GEO**: Add at least 2 question-based headings (starting with How, What, Why, etc., ending with ?). Currently have {len(question_headings)}.")
    if not links_ok:
        fixes.append(f"- 🔗 **Internal Links**: Add internal links (to other blog posts, services, locations) — currently {len(internal_links)}, need at least 3.")
    if not schema_ok:
        if "metaTitle" in missing_schema:
            fixes.append(f"- 📋 **Schema**: Add `metaTitle` field based on the post title.")
        if "metaDescription" in missing_schema:
            fixes.append(f"- 📋 **Schema**: Add `metaDescription` field based on the post excerpt.")
        if "dateModified" in missing_schema:
            fixes.append(f"- 📋 **Schema**: Add `dateModified` field with current date.")
    
    if fixes:
        for f in fixes:
            print(f"  {f}")
    else:
        print("  ✅ All checks passed — no fixes needed.")
    
    print()

# Print summary
print(f"\n{'='*80}")
print("SUMMARY")
print(f"{'='*80}")
for p in target_posts:
    title = p.get("title", "NO TITLE")
    print(f"- {p['slug']}: {title[:60]}")
