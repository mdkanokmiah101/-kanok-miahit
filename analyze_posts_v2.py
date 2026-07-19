#!/usr/bin/env python3
"""Refined analysis for each post with more precise metrics."""
import re

with open('/root/kanok-miahit/src/app/blog/data.js', 'r') as f:
    content = f.read()

posts_to_check = [
    ("seo-for-fitness-gyms-bangladesh", "fitness and gym", ["fitness", "gym"], "Industry-Specific SEO", "/industries"),
    ("seo-for-law-firms-bangladesh", "law firm", ["law firm", "legal"], "Industry-Specific SEO", "/industries"),
    ("seo-https-ssl-impact-bangladesh", "HTTPS SSL", ["https", "ssl"], "Technical SEO", "/services/technical-seo"),
    ("b2b-lead-generation-seo-bangladesh", "B2B lead generation", ["b2b", "lead generation"], "B2B/Industrial SEO", "/industries"),
    ("seo-for-startups-bangladesh", "startup", ["startup"], "Growth SEO", "/services"),
]

def extract_post(full_text, slug):
    slug_pattern = rf'slug: "{re.escape(slug)}"'
    slug_match = re.search(slug_pattern, full_text)
    if not slug_match:
        return None
    
    pos = slug_match.start()
    while pos > 0 and full_text[pos] != '{':
        pos -= 1
    
    depth = 0
    end_pos = pos
    in_content = False
    i = pos
    while i < len(full_text):
        ch = full_text[i]
        if ch == '`':
            if not in_content:
                in_content = True
            elif i > 0 and full_text[i-1] != '\\':
                in_content = False
        if not in_content:
            if ch == '{':
                depth += 1
            elif ch == '}':
                depth -= 1
                if depth == 0:
                    end_pos = i + 1
                    break
        i += 1
    return pos, end_pos, full_text[pos:end_pos]

for slug, keyword_text, kw_parts, pillar_topic, pillar_page in posts_to_check:
    result = extract_post(content, slug)
    if not result:
        print(f"\n## Post: {slug}\n❌ NOT FOUND")
        continue
    
    _, _, post_text = result
    
    # Extract title
    title_m = re.search(r'title:\s*"([^"]+)"', post_text)
    title = title_m.group(1) if title_m else "Unknown"
    
    # Extract date
    date_m = re.search(r'date:\s*"([^"]+)"', post_text)
    date = date_m.group(1) if date_m else None
    
    # Extract excerpt
    excerpt_m = re.search(r'excerpt:\s*\n?\s*"([^"]+)"', post_text, re.DOTALL)
    excerpt = excerpt_m.group(1) if excerpt_m else None
    
    # Extract meta fields
    metaTitle_m = re.search(r'metaTitle:\s*"([^"]+)"', post_text)
    metaDesc_m = re.search(r'metaDescription:\s*"([^"]+)"', post_text)
    dateMod_m = re.search(r'dateModified:\s*"([^"]+)"', post_text)
    
    # Extract tags
    tags_m = re.search(r'tags:\s*\[(.*?)\]', post_text, re.DOTALL)
    tags = re.findall(r'"([^"]+)"', tags_m.group(1)) if tags_m else []
    
    # Extract content body
    # Need to find the backtick content - find the first backtick after "content:"
    content_start = post_text.find("content: `")
    if content_start >= 0:
        body_start = content_start + len("content: `")
        # Find the closing backtick before the closing brace of the post
        # Need to handle escaped backticks
        body = ""
        i = body_start
        while i < len(post_text):
            if post_text[i] == '`' and (i == 0 or post_text[i-1] != '\\'):
                break
            body += post_text[i]
            i += 1
    else:
        body = ""
    
    body_lower = body.lower() if body else ""
    
    # ===== A. TF-IDF =====
    kw_count = 0
    for part in kw_parts:
        kw_count += body_lower.count(part.lower())
    
    tfidf_pass = kw_count >= 5
    
    # ===== B. Entities =====
    entities_needed = {
        "Dhaka/Bangladesh (location)": "dhaka" in body_lower and "bangladesh" in body_lower,
    }
    if "b2b" in slug:
        entities_needed["Service type (B2B/Lead Gen)"] = any(x in body_lower for x in ["b2b", "lead generation", "লিড"])
    elif "law" in slug:
        entities_needed["Service type (Law/Legal)"] = any(x in body_lower for x in ["law", "legal", "আইন"])
    elif "fitness" in slug:
        entities_needed["Service type (Fitness/Gym)"] = any(x in body_lower for x in ["fitness", "gym", "ফিটনেস"])
    elif "startup" in slug:
        entities_needed["Service type (Startup)"] = any(x in body_lower for x in ["startup", "স্টার্টআপ"])
    elif "https" in slug:
        entities_needed["Service type (HTTPS/SSL)"] = any(x in body_lower for x in ["https", "ssl"])
    
    # Check for industry
    entities_needed["Industry context"] = bool(tags and len(tags) > 0)
    
    all_missing = [k for k, v in entities_needed.items() if not v]
    
    # ===== C. Pillar Link =====
    links_to_pillar = pillar_page in body
    
    # ===== D. AEO/GEO - Question headings =====
    # Count headings that start with question words (English and Bengali)
    heading_lines = re.findall(r'^#{1,3}\s+.*$', body, re.MULTILINE)
    question_headings = []
    q_words = ['how', 'what', 'why', 'when', 'where', 'can', 'do', 'is', 'are', 'will', 'does', 'কী', 'কেন', 'কখন', 'কোথায়', 'কিভাবে']
    
    for h in heading_lines:
        h_lower = h.lower()
        # Check if it starts with question word or ends with ?
        for qw in q_words:
            pattern = r'^#{1,3}\s+' + re.escape(qw) + r'\b'
            if re.search(pattern, h_lower):
                question_headings.append(h.strip())
                break
        else:
            if h.strip().endswith('?'):
                question_headings.append(h.strip())
    
    # Also count FAQ items
    faq_items = re.findall(r'###\s+[^`\n]+\?', body)
    for f in faq_items:
        if f.strip() not in question_headings:
            question_headings.append(f.strip())
    
    question_count = len(question_headings)
    aeo_pass = question_count >= 2
    
    # ===== E. Internal Links =====
    # Count internal links
    internal_links = re.findall(r'\[([^\]]+)\]\((/[^\)]+)\)', body)
    unique_destinations = set(l[1] for l in internal_links)
    
    service_links = [l for l in internal_links if l[1].startswith('/services') and not l[1].startswith('/services/') == False or ('/services' in l[1])]
    service_links = [l for l in internal_links if '/services' in l[1]]
    location_links = [l for l in internal_links if '/locations' in l[1]]
    blog_links = [l for l in internal_links if '/blog/' in l[1]]
    contact_about = [l for l in internal_links if l[1] in ['/contact', '/about']]
    
    total_internal = len(unique_destinations)
    internal_pass = total_internal >= 3
    
    # ===== F. Schema =====
    schema_items = {
        "title": bool(title and len(title) > 5),
        "excerpt": bool(excerpt and len(excerpt) > 15),
        "date": bool(date),
        "dateModified": bool(dateMod_m),
        "metaTitle": bool(metaTitle_m),
        "metaDescription": bool(metaDesc_m),
    }
    schema_missing = [k for k, v in schema_items.items() if not v]
    schema_pass = len(schema_missing) == 0
    
    # ===== Print Report =====
    status_icon = lambda p: "✅" if p else "❌"
    
    print(f"\n## Post: {slug}")
    print(f"Title: {title}")
    print(f"| Check | Status | Details |")
    print(f"|-------|--------|---------|")
    print(f"| TF-IDF: `{keyword_text}` | {status_icon(tfidf_pass)} | {kw_count} occurrences across top keyword parts |")
    
    if all_missing:
        print(f"| Entities | ❌ | Missing: {', '.join(all_missing)} |")
    else:
        print(f"| Entities | ✅ | All required entities present |")
    
    if links_to_pillar:
        print(f"| Pillar Link | ✅ | Links to pillar: {pillar_page} |")
    else:
        print(f"| Pillar Link | ❌ | No link to pillar page {pillar_page} found |")
    
    print(f"| AEO/GEO | {status_icon(aeo_pass)} | {question_count} question-based headings/FAQ items |")
    print(f"| Internal Links | {status_icon(internal_pass)} | {total_internal} unique internal link destinations |")
    print(f"| Schema Ready | {status_icon(schema_pass)} | Missing: {', '.join(schema_missing) if schema_missing else 'All fields set'} |")
    
    # Fix instructions
    fixes = []
    if not tfidf_pass:
        fixes.append(f"- 🔴 **TF-IDF**: Only {kw_count} occurrences of `{keyword_text}`. Add at least {5 - kw_count} more mentions spread across the content naturally.")
    if all_missing:
        fixes.append(f"- 🔴 **Entities**: Add missing entities: {', '.join(all_missing)}")
    if not links_to_pillar:
        fixes.append(f"- 🔴 **Pillar Link**: Add a contextual link to {pillar_page} to reinforce pillar-cluster structure.")
    if not aeo_pass:
        fixes.append(f"- 🔴 **AEO/GEO**: Only {question_count} question headings. Add at least {2 - question_count} more How/What/Why/Can/Is-style headings.")
    if not internal_pass:
        fixes.append(f"- 🔴 **Internal Links**: Only {total_internal} unique internal destinations. Need ≥ 3.")
    if schema_missing:
        for m in schema_missing:
            fixes.append(f"- 🔴 **Schema – {m}**: Missing `{m}` field. Add it to enable proper ArticleSchema generation.")
    
    if fixes:
        print(f"\n### Fix instructions:")
        for f in fixes:
            print(f)
        print()
    else:
        print(f"\n✅ All checks pass! No fixes needed.\n")
