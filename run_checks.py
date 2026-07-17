#!/usr/bin/env python3
"""Run content framework checks on 10 blog posts from data.js."""
import re
import json
import sys

DATA_FILE = "src/app/blog/data.js"

# Read the whole file
with open(DATA_FILE, "r", encoding="utf-8") as f:
    data = f.read()

# Slugs to check
SLUGS = [
    "content-marketing-seo-friendly-content-writing",
    "keyword-research-bangladesh-market",
    "link-building-bangladesh-strategies",
    "ecommerce-seo-daraz-shopify-guide",
    "technical-seo-core-web-vitals-optimization",
    "seo-trends-2026-ai-geo-future",
    "local-seo-dhaka-google-maps-ranking",
    "seo-bangla-beginners-guide-google-ranking",
    "international-seo-bangladesh-exporters-global-buyers",
    "content-marketing-strategy-bangladeshi-brands-seo",
]

def find_post(slug):
    """Extract a post object from data.js by slug."""
    pattern = r'{\s*\n\s*slug:\s*"' + re.escape(slug) + r'",\s*\n(.*?)\n\s*},'
    match = re.search(pattern, data, re.DOTALL)
    if not match:
        return None
    raw = match.group(0)
    return raw

def extract_field(raw, field):
    """Extract a field value from raw post string."""
    # Title
    m = re.search(rf'{field}:\s*"([^"]*)"', raw)
    if m:
        return m.group(1)
    # Excerpt (multi-line)
    m = re.search(rf'{field}:\s*\n\s*"([^"]*)"', raw)
    if m:
        return m.group(1)
    # Tags array
    m = re.search(rf'{field}:\s*\[(.*?)\]', raw, re.DOTALL)
    if m:
        return m.group(1)
    # Content (template literal)
    m = re.search(rf'{field}:\s*`(.*?)`', raw, re.DOTALL)
    if m:
        return m.group(1)
    return None

def run_checks(slug):
    print(f"\n## Post: {slug}")
    
    raw = find_post(slug)
    if not raw:
        print("| Check | Status | Details |")
        print("|-------|--------|---------|")
        print(f"| ALL | ❌ FAIL | Post not found in data.js |")
        print("### Fix instructions: Post slug not found in data file.")
        return
    
    title = extract_field(raw, "title") or ""
    date_val = extract_field(raw, "date") or ""
    excerpt = extract_field(raw, "excerpt") or ""
    tags_raw = extract_field(raw, "tags") or ""
    content_raw = extract_field(raw, "content") or ""
    
    tags = [t.strip().strip('"') for t in tags_raw.split(",")] if tags_raw else []
    
    results = {}
    fix_instructions = []

    # ---- A. TF-IDF ----
    # Extract primary keyword from title (first meaningful noun phrase)
    title_clean = title.strip()
    # Split on colon/dash and take first meaningful part
    parts = re.split(r'[:\-—]', title_clean)
    first_part = parts[0].strip()
    # Remove leading numbers, stop words etc. - take first meaningful noun phrase
    # For English titles, find first noun phrase
    # For Bengali titles, take the first substantive part
    
    # Simple heuristic: take first word that isn't a stop word
    bengali_stop = r'[সহজভাবে|কীভাবে|কেন|কী|একটি|জন্য|বাংলাদেশি]'
    words = re.findall(r'[\w]+', first_part)
    
    # For English titles, find key phrase
    if re.match(r'^[a-zA-Z]', first_part):
        # English title - extract first meaningful noun phrase
        # Common patterns: "Content Marketing Strategy for..." -> "Content Marketing"
        # "International SEO for..." -> "International SEO"
        stop_words_en = {'a', 'an', 'the', 'for', 'in', 'of', 'to', 'and', 'or', 'is', 'are', 'was', 'were'}
        key_phrase = []
        for w in words:
            if w.lower() in stop_words_en:
                if len(key_phrase) >= 1:
                    break
                continue
            key_phrase.append(w)
            if len(key_phrase) >= 2:
                break
        primary_kw = " ".join(key_phrase) if key_phrase else words[0] if words else title_clean
    else:
        # Bengali title - take first 1-2 significant words
        bengali_skip = {'সহজ', 'কীভাবে', 'কেন', 'কী', 'বাংলাদেশি', 'একটি', 'জন্য', 'এবং', 'বাংলাদেশের', '২০২৬', 'যুগে'}
        key_phrase = []
        for w in words:
            if w in bengali_skip:
                if len(key_phrase) >= 1:
                    break
                continue
            key_phrase.append(w)
            if len(key_phrase) >= 2:
                break
        primary_kw = " ".join(key_phrase) if key_phrase else words[0] if words else title_clean
    
    # Count occurrences in content
    content_lower = content_raw.lower()
    if primary_kw.lower() in content_lower:
        count = len(re.findall(re.escape(primary_kw), content_raw, re.IGNORECASE))
    else:
        # Try variations - if primary_kw is multi-word, try with word boundary
        count = len(re.findall(r'\b' + re.escape(primary_kw) + r'\b', content_raw, re.IGNORECASE))
        if count == 0 and len(primary_kw.split()) == 1:
            # Single word, use broader matching
            count = len(re.findall(re.escape(primary_kw), content_raw, re.IGNORECASE))
    
    status = "✅ PASS" if count >= 5 else "❌ FLAG"
    if count < 5:
        fix_instructions.append(f"**A. TF-IDF**: Primary keyword '{primary_kw}' appears {count} time(s), need ≥ 5. Add more instances of this keyword naturally in the content.")
    results['A. TF-IDF'] = (status, f"Keyword '{primary_kw}' found {count} times (need ≥ 5)")

    # ---- B. Entities ----
    content_check = content_raw
    
    # Check location entities
    has_dhaka = bool(re.search(r'ঢাকা|Dhaka', content_check))
    has_bangladesh = bool(re.search(r'বাংলাদেশ|Bangladesh', content_check))
    has_service = bool(re.search(r'SEO|ডিজিটাল মার্কেটিং|digital marketing|Content Marketing', content_check, re.IGNORECASE))
    
    missing_entities = []
    if not has_dhaka and not has_bangladesh:
        missing_entities.append("Location (Dhaka/Bangladesh)")
    if not has_service:
        missing_entities.append("Service type (SEO/digital marketing)")
    
    if missing_entities:
        status = "❌ FLAG"
        fix_instructions.append(f"**B. Entities**: Missing entity types: {', '.join(missing_entities)}. Add mentions of these in the content.")
    else:
        status = "✅ PASS"
    
    loc_detail = "Has Dhaka" if has_dhaka else "No Dhaka"
    loc_detail += ", Has Bangladesh" if has_bangladesh else ", No Bangladesh"
    loc_detail += ", Has SEO/digital marketing" if has_service else ", No SEO/digital marketing"
    results['B. Entities'] = (status, f"Location: {loc_detail}")

    # ---- C. Pillar Link ----
    # Based on tags, determine pillar topic
    pillar_map = {
        # Tags → pillar slug keywords
        "content marketing": ["content-marketing", "content-marketing-strategy"],
        "seo": ["complete-seo-guide", "seo-guide"],
        "link building": ["link-building"],
        "backlinks": ["link-building"],
        "keyword research": ["keyword-research"],
        "ecommerce": ["ecommerce-seo"],
        "e-commerce": ["ecommerce-seo"],
        "technical seo": ["technical-seo"],
        "core web vitals": ["technical-seo"],
        "seo trends": ["seo-trends"],
        "geo": ["geo-optimization", "seo-trends"],
        "ai seo": ["seo-trends"],
        "local seo": ["local-seo", "google-business-profile"],
        "dhaka": ["local-seo"],
        "google maps": ["local-seo"],
        "beginners": ["seo-bangla-beginners-guide"],
        "seo basics": ["seo-bangla-beginners-guide"],
        "international seo": ["international-seo"],
        "b2b seo": ["international-seo"],
        "digital marketing": ["content-marketing-strategy"],
    }
    
    pillar_slugs = set()
    for tag in tags:
        tag_lower = tag.lower().strip().strip('"')
        for key, slugs in pillar_map.items():
            if key in tag_lower or tag_lower in key:
                for s in slugs:
                    pillar_slugs.add(s)
    
    # Also check if the post links to /blog/... pillar pages
    blog_links = re.findall(r'/blog/([\w-]+)', content_check)
    
    linked_pillar = bool(set(blog_links) & pillar_slugs) if pillar_slugs else bool(blog_links)
    
    # If no pillar_slugs determined, check if any /blog/ links exist at all
    if not pillar_slugs:
        linked_pillar = len(blog_links) > 0
        pillar_detail = f"No specific pillar determined from tags; {len(blog_links)} blog link(s) found. Tags: {tags}"
    else:
        matching = set(blog_links) & pillar_slugs
        pillar_detail = f"Pillar candidates: {list(pillar_slugs)}. Links to pillars: {list(matching) if matching else 'None'}. Blog links: {blog_links[:5]}..."
    
    if not linked_pillar:
        status = "❌ FLAG"
        fix_instructions.append(f"**C. Pillar Link**: No link to pillar page found. Based on tags {tags}, expected pillar slugs: {list(pillar_slugs)}. Add a link to the relevant pillar page.")
    else:
        status = "✅ PASS"
    
    results['C. Pillar Link'] = (status, pillar_detail)

    # ---- D. AEO/GEO ----
    # Count question-based headings
    # Match headings starting with How, What, Why, When, Where, Can, Do, Is, Are
    # In both English and Bengali
    english_q_words = r'\b(How|What|Why|When|Where|Can|Do|Does|Is|Are|Which|Who)\b'
    bengali_q_words = r'(কীভাবে|কেন|কী|কি|কখন|কোথায়|কত|কোন|কে|কার|কাদের)'
    
    heading_pattern = re.compile(
        r'^#{2,4}\s+(?:' + english_q_words + r'|' + bengali_q_words + r')',
        re.MULTILINE | re.IGNORECASE
    )
    
    question_headings = heading_pattern.findall(content_check)
    # The findall will return tuples of matching groups
    actual_questions = []
    for match in heading_pattern.finditer(content_check):
        actual_questions.append(match.group(0).strip())
    
    q_count = len(actual_questions)
    
    # Also check FAQ-style questions (lines starting with ### ... ?)
    faq_pattern = re.compile(r'^#{3,4}\s+.*\?', re.MULTILINE)
    faq_questions = faq_pattern.findall(content_check)
    
    # Combine unique question-based headings
    all_q_headers = set(h.strip() for h in actual_questions + faq_questions)
    q_count = len(all_q_headers)
    
    status = "✅ PASS" if q_count >= 2 else "❌ FLAG"
    if q_count < 2:
        fix_instructions.append(f"**D. AEO/GEO**: Only {q_count} question-based heading(s) found, need ≥ 2. Add headings starting with How/What/Why or Bengali equivalents.")
    
    results['D. AEO/GEO'] = (status, f"{q_count} question-based heading(s) found (need ≥ 2). Examples: {list(all_q_headers)[:3]}")

    # ---- E. Internal Links ----
    blog_links_count = len(re.findall(r'/blog/[\w-]+', content_check))
    services_links_count = len(re.findall(r'/services/[\w-]*', content_check))
    locations_links_count = len(re.findall(r'/locations/[\w-]*', content_check))
    industries_links_count = len(re.findall(r'/industries/[\w-]*', content_check))
    
    total_internal = blog_links_count + services_links_count + locations_links_count + industries_links_count
    
    status = "✅ PASS" if total_internal >= 3 else "❌ FLAG"
    if total_internal < 3:
        fix_instructions.append(f"**E. Internal Links**: Only {total_internal} internal link(s) found (blog:{blog_links_count}, services:{services_links_count}, locations:{locations_links_count}, industries:{industries_links_count}). Need ≥ 3.")
    
    results['E. Internal Links'] = (status, f"Blog:{blog_links_count}, Services:{services_links_count}, Locations:{locations_links_count}, Industries:{industries_links_count}. Total:{total_internal} (need ≥ 3)")

    # ---- F. Schema ----
    schema_missing = []
    if not title:
        schema_missing.append("title")
    if not excerpt:
        schema_missing.append("excerpt")
    if not date_val:
        schema_missing.append("date")
    
    if schema_missing:
        status = "❌ FLAG"
        fix_instructions.append(f"**F. Schema**: Missing schema fields: {', '.join(schema_missing)}. Ensure title, excerpt, and date are set.")
    else:
        status = "✅ PASS"
    
    title_preview = title[:50] + "..." if len(title) > 50 else title
    excerpt_preview = excerpt[:50] + "..." if len(excerpt) > 50 else excerpt
    results['F. Schema'] = (status, f"Title='{title_preview}', Excerpt='{excerpt_preview}', Date='{date_val}'")

    # ---- Output ----
    print("| Check | Status | Details |")
    print("|-------|--------|---------|")
    for check_name, (stat, detail) in results.items():
        # Escape pipe characters in detail
        detail_escaped = detail.replace("|", "/")
        print(f"| {check_name} | {stat} | {detail_escaped} |")
    
    print("### Fix instructions:")
    if fix_instructions:
        for instr in fix_instructions:
            print(f"- {instr}")
    else:
        print("- All checks passed. No fixes needed.")
    print()

for slug in SLUGS:
    run_checks(slug)
