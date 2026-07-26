#!/usr/bin/env python3
"""Full framework analysis on all extracted posts."""
import json
import re
import sys

with open("/tmp/all_posts_full.json") as f:
    posts = json.load(f)

def count_keyword(content, keyword):
    if not keyword:
        return 0
    return len(re.findall(re.escape(keyword), content, re.IGNORECASE))

def extract_keyword(title, lang="en"):
    if lang == "bn":
        # For Bengali, take first 3 words
        return ' '.join(title.split()[:3])
    # English: extract meaningful noun phrase
    t = re.sub(r'^(How|What|Why|The|Top|Best|Your|A|An|Complete)\s+', '', title)
    t = re.sub(r'[:\-–].*$', '', t)
    words = t.split()
    if not words:
        return title.split()[0] if title.split() else ""
    if len(words) >= 3:
        return ' '.join(words[:3])
    return ' '.join(words)

def check_entities(post):
    content = post["content"] + " " + post.get("excerpt", "")
    slug = post["slug"]
    
    entities = {}
    
    # Location: Dhaka or specific neighborhood
    if re.search(r'Dhaka|Gulshan|Banani|Dhanmondi|Uttara|Motijheel|Mirpur|Farmgate', content, re.IGNORECASE):
        entities["location"] = True
    else:
        entities["location"] = False
    
    # Bangladesh
    if re.search(r'Bangladesh|বাংলাদেশ', content):
        entities["bangladesh"] = True
    else:
        entities["bangladesh"] = False
    
    # Kanok Miah
    if re.search(r'Kanok Miah|কনক মিঞা|কানক মিয়া', content):
        entities["kanok_miah"] = True
    else:
        entities["kanok_miah"] = False
    
    # Service type
    if re.search(r'SEO|search engine|local SEO|technical SEO|link building|content marketing|GEO|Google Business|GBP|Google Maps', content, re.IGNORECASE):
        entities["service_type"] = True
    else:
        entities["service_type"] = False
    
    # Industry
    if re.search(r'garment|textile|restaurant|food|real estate|healthcare|medical|education|ecommerce|e-commerce|online store|retail|cleaning|salon|spa|case study|B2B', content, re.IGNORECASE):
        entities["industry"] = True
    else:
        entities["industry"] = False
    
    return entities

def count_question_headings(content):
    count = 0
    for line in content.split('\n'):
        line = line.strip()
        if re.match(r'^#{1,4}\s+(How|What|Why|When|Where|Can|Do|Is|Are)\b', line, re.IGNORECASE):
            count += 1
    return count

def count_internal_links(content):
    # Count all internal links
    blog = len(re.findall(r'/blog/[^)\s"\'\]>]+', content))
    services = len(re.findall(r'/services/[^)\s"\'\]>]+', content))
    locations = len(re.findall(r'/locations/[^)\s"\'\]>]+', content))
    industries = len(re.findall(r'/industries/[^)\s"\'\]>]+', content))
    homepage = len(re.findall(r'\(/\)|\(\/\)', content))
    about = len(re.findall(r'/about[^)\s"\'\]>]*', content))
    contact = len(re.findall(r'/contact[^)\s"\'\]>]*', content))
    
    total = blog + services + locations + industries + homepage + about + contact
    return total, {"blog": blog, "services": services, "locations": locations, "industries": industries, "homepage": homepage, "about": about, "contact": contact}

def pillar_check(tags, content):
    pillar_map = {
        "SEO Guide": "/blog/complete-seo-guide-bangladesh-businesses-2026",
        "Bangladesh SEO": "/blog/complete-seo-guide-bangladesh-businesses-2026",
        "Local SEO": "/blog/local-seo-tips-dhaka-businesses-google-maps",
        "E-commerce SEO": "/blog/why-ecommerce-store-needs-seo-bangladesh",
        "Technical SEO": "/blog/technical-seo-checklist-bangladeshi-websites",
        "Link Building": "/blog/link-building-strategies-bangladesh-market",
        "GEO": "/blog/geo-optimization-prepare-business-ai-search",
        "Google Maps": "/blog/local-seo-tips-dhaka-businesses-google-maps",
        "GBP": "/blog/google-business-profile-optimization-guide-bangladesh",
        "Case Study": None,
        "SEO": "/blog/complete-seo-guide-bangladesh-businesses-2026",
        "SMM Panel": None,
        "Growth Strategy": None,
        "B2B SEO": None,
        "Website Optimization": "/blog/technical-seo-checklist-bangladeshi-websites",
        "Core Web Vitals": "/blog/technical-seo-checklists-bangladeshi-websites",
        "Google Search": "/blog/complete-seo-guide-bangladesh-businesses-2026",
        "SMM Panel": None,
    }
    bengali_map = {
        "ফিচার্ড স্নিপেট": "/blog/schema-markup-rich-snippets-techniques",
        "পজিশন জিরো": "/blog/schema-markup-rich-snippets-techniques",
        "গুগল সার্চ": "/blog/complete-seo-guide-bangladesh-businesses-2026",
        "রিচ স্নিপেট": "/blog/schema-markup-rich-snippets-techniques",
        "নলেজ প্যানেল": "/blog/complete-seo-guide-bangladesh-businesses-2026",
        "নলেজ গ্রাফ": "/blog/complete-seo-guide-bangladesh-businesses-2026",
        "ব্র্যান্ডিং": "/blog/complete-seo-guide-bangladesh-businesses-2026",
        "বাংলাদেশ": "/blog/complete-seo-guide-bangladesh-businesses-2026",
        "SEO": "/blog/complete-seo-guide-bangladesh-businesses-2026",
    }
    
    pillar_url = None
    for tag in tags:
        if tag in pillar_map and pillar_map[tag]:
            pillar_url = pillar_map[tag]
            break
        if tag in bengali_map and bengali_map[tag]:
            pillar_url = bengali_map[tag]
            break
    
    # Also check if tags suggest a case study that should link to services
    if pillar_url is None and any("Case" in tag or "case" in content.lower()[:200] for tag in tags):
        pillar_url = "/services"  # Case studies should link to services page
    
    if pillar_url is None:
        return False, "No pillar mapping found for tags"
    
    linked = pillar_url in content
    if linked:
        return True, f"Links to: {pillar_url}"
    else:
        return False, f"Missing link to pillar: {pillar_url}"

def schema_check(post):
    issues = []
    if not post.get("title") or post["title"] == "":
        issues.append("title missing")
    if not post.get("excerpt") or post["excerpt"] == "":
        issues.append("excerpt missing")
    if not post.get("date") or post["date"] == "":
        issues.append("date missing")
    if not post.get("slug") or post["slug"] == "":
        issues.append("slug missing")
    
    if issues:
        return False, f"Missing: {', '.join(issues)}"
    return True, "All fields set"

# Run analysis
for post in posts:
    slug = post["slug"]
    title = post["title"]
    content = post["content"]
    tags = post["tags"]
    lang = post.get("lang", "en")
    
    # Also search in excerpt for entities
    excerpt = post.get("excerpt", "")
    
    print(f"\n## Post: {slug}")
    print(f"**Title:** {title}")
    print()
    print("| Check | Status | Details |")
    print("|-------|--------|---------|")
    
    # A. TF-IDF
    keyword = extract_keyword(title, lang)
    kw_count = count_keyword(content, keyword)
    # For case studies, also check the full title as a phrase
    if "case-study" in slug:
        # Use first meaningful part
        title_parts = title.split(":")
        if len(title_parts) > 1:
            main_kw = title_parts[0].strip()
            kw_count = count_keyword(content, main_kw)
            keyword = main_kw
        if kw_count < 3:
            # Try business name from slug
            biz_name = slug.replace("-seo-case-study", "").replace("-", " ").title()
            kw_count2 = count_keyword(content, biz_name)
            if kw_count2 > kw_count:
                keyword, kw_count = biz_name, kw_count2
    
    status = "✅" if kw_count >= 5 else "❌"
    print(f"| TF-IDF: {keyword[:35]} | {status} | {kw_count} occurrences |")
    
    # B. Entities
    ents = check_entities(post)
    missing = [k for k, v in ents.items() if not v]
    status = "✅" if not missing else "❌"
    if not missing:
        detail = "All key entities present"
    else:
        detail = f"Missing: {', '.join(missing)}"
    print(f"| Entities | {status} | {detail} |")
    
    # C. Pillar
    pil_pass, pil_detail = pillar_check(tags, content)
    status = "✅" if pil_pass else "❌"
    print(f"| Pillar Link | {status} | {pil_detail[:60]} |")
    
    # D. AEO/GEO
    q_count = count_question_headings(content)
    status = "✅" if q_count >= 2 else "❌"
    print(f"| AEO/GEO | {status} | {q_count} question headings |")
    
    # E. Internal Links
    link_count, link_detail = count_internal_links(content)
    status = "✅" if link_count >= 3 else "❌"
    print(f"| Internal Links | {status} | {link_count} total (blog:{link_detail['blog']}, svc:{link_detail['services']}, loc:{link_detail['locations']}, ind:{link_detail['industries']}, home:{link_detail['homepage']}, about:{link_detail['about']}, contact:{link_detail['contact']}) |")
    
    # F. Schema
    sc_pass, sc_detail = schema_check(post)
    status = "✅" if sc_pass else "❌"
    print(f"| Schema Ready | {status} | {sc_detail} |")

# Aggregate
print("\n\n---")
print("## Aggregate Summary")
print()
total = len(posts)
print(f"Total posts analyzed: {total}")
