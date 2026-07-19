#!/usr/bin/env python3
"""
Content Framework Enforcer for kanokmiah.com.bd
Checks each modified blog post against TF-IDF, Entities, Pillar, AEO/GEO,
Internal Linking, and Schema readiness rules.
"""

import re
import json
import os

# ── list of modified slugs (from git log --since="48 hours ago") ──
MODIFIED_SLUGS = [
    "affiliate-seo-bangladesh",
    "b2b-lead-generation-seo-bangladesh",
    "backlink-outreach-templates-strategies-bangladesh",
    "best-seo-expert-in-dhaka",
    "blogging-strategy-seo-frequency-topics-bangladesh",
    "building-seo-roadmap-bangladesh-business",
    "complete-seo-guide-bangladesh-businesses-2026",
    "content-marketing-seo-friendly-content-writing",
    "content-marketing-strategy-bangladeshi-brands-seo",
    "ecommerce-seo-daraz-shopify-guide",
    "enterprise-seo-large-organizations-bangladesh",
    "geo-optimization-prepare-business-ai-search",
    "google-business-profile-optimization-guide-bangladesh",
    "google-discover-seo-bangladesh",
    "google-my-business-optimization-bangladesh",
    "google-search-console-performance-guide",
    "google-tag-manager-seo-bd",
    "how-to-choose-right-seo-agency-bangladesh",
    "how-to-track-measure-seo-roi-bangladesh",
    "international-seo-bangladesh-exporters-global-buyers",
    "keyword-research-bangladesh-market",
    "link-building-bangladesh-strategies",
    "link-building-strategies-bangladesh-market",
    "local-seo-dhaka-google-maps-ranking",
    "local-seo-multiple-business-locations-bangladesh",
    "local-seo-tips-dhaka-businesses-google-maps",
    "long-tail-keywords-bangladesh",
    "mobile-seo-bangladesh-ranking-strategy",
    "mobile-seo-optimization-bangladesh-mobile-first-era",
    "recovering-google-penalties-bangladesh-guide",
    "schema-markup-rich-snippets-techniques",
    "seo-bangla-beginners-guide-google-ranking",
    "seo-bangla-blog-content-writing",
    "seo-branded-vs-non-branded-bd",
    "seo-breadcrumb-schema-bd",
    "seo-canonical-url-guide-bd",
    "seo-career-guide-bangladesh-2026",
    "seo-competitor-analysis-bangladesh",
    "seo-consultant-dhaka-bangladesh",
    "seo-content-repurposing-bangladesh",
    "seo-direct-traffic-bangladesh",
    "seo-domain-authority-bangladesh",
    "seo-educational-institutions-bangladesh",
    "seo-event-management-companies-bangladesh",
    "seo-faq-schema-bangladesh",
    "seo-featured-snippet-bangladesh",
    "seo-for-facebook-marketplace",
    "seo-for-fitness-gyms-bangladesh",
    "seo-for-hotel-resort-bangladesh",
    "seo-for-law-firms-bangladesh",
    "seo-for-mobile-apps-bangladesh",
    "seo-for-ngo-bangladesh",
    "seo-for-podcast-bangladesh",
    "seo-for-startups-bangladesh",
    "seo-for-youtube-channel-bangla",
    "seo-garments-textile-industry-b2b-lead-generation",
    "seo-google-business-profile-posts",
    "seo-google-penalty-recovery-bd",
    "seo-google-updates-2026",
    "seo-healthcare-medical-clinics-bangladesh",
    "seo-howto-schema-bangladesh",
    "seo-hreflang-guide-bangladesh",
    "seo-https-ssl-impact-bangladesh",
    "seo-hubspot-vs-wordpress-bd",
    "seo-information-gain-optimization",
    "seo-json-ld-schema-bangladesh",
    "seo-keyword-clustering-bangladesh",
    "seo-knowledge-panel-bangladesh",
    "seo-landing-page-optimization-bd",
    "seo-local-citations-bangladesh",
    "seo-non-profit-organizations-bangladesh",
    "seo-page-authority-bangladesh",
    "seo-passage-ranking-bangladesh",
    "seo-people-also-ask-optimization",
    "seo-photographers-videographers-bangladesh",
    "seo-pillar-content-strategy-bd",
    "seo-real-estate-agents-property-developers-bangladesh",
    "seo-real-estate-developers-dhaka",
    "seo-redirects-guide-bangladesh",
    "seo-referral-traffic-bangladesh",
    "seo-robots-txt-guide-bangladesh",
    "seo-search-intent-optimization",
    "seo-semantic-search-bangla",
    "seo-services-cost-bangladesh-pricing-guide",
    "seo-skyscraper-technique-bangladesh",
    "seo-structured-data-guide-bd",
    "seo-tips-for-business-owners-bd",
    "seo-travel-tourism-bangladesh",
    "seo-trends-2026-ai-geo-future",
    "seo-vs-google-ads-bangladesh-business",
    "seo-vs-google-ads-whats-best-bangladesh-businesses",
    "seo-vs-ppc-advertising-bangladesh",
    "seo-wedding-event-planners-bangladesh",
    "seo-xml-sitemap-guide-bd",
    "seo-zero-click-search-bangladesh",
    "technical-seo-checklist-bangladeshi-websites",
    "technical-seo-core-web-vitals-optimization",
    "why-ecommerce-store-needs-seo-bangladesh",
    "youtube-seo-bangladesh-ranking-tips"
]

DATAJS_PATH = "src/app/blog/data.js"


def parse_posts(filepath):
    """Parse data.js and return a dict of slug -> post data."""
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    # Split by slug lines to extract individual posts
    pattern = r'{\s*\n\s+slug:\s*"([^"]+)"'
    matches = list(re.finditer(pattern, text))
    
    posts = {}
    for i, m in enumerate(matches):
        slug = m.group(1)
        start = m.start()
        # End is start of next post or end of file/array
        if i + 1 < len(matches):
            end = matches[i+1].start()
        else:
            end = text.rfind("];") 
            if end == -1:
                end = len(text)
        
        post_text = text[start:end]
        
        # Extract fields
        post = {"slug": slug}
        
        # title
        t = re.search(r'title:\s*"([^"]*)"', post_text)
        post["title"] = t.group(1) if t else ""
        
        # date
        d = re.search(r'date:\s*"([^"]*)"', post_text)
        post["date"] = d.group(1) if d else ""
        
        # dateModified
        dm = re.search(r'dateModified:\s*"([^"]*)"', post_text)
        post["dateModified"] = dm.group(1) if dm else ""
        
        # author
        a = re.search(r'author:\s*"([^"]*)"', post_text)
        post["author"] = a.group(1) if a else ""
        
        # excerpt - can be multiline
        e = re.search(r'excerpt:\s*\n\s+"((?:[^"]|\\")*)"', post_text, re.DOTALL)
        if not e:
            e = re.search(r'excerpt:\s*"((?:[^"]|\\")*)"', post_text)
        post["excerpt"] = e.group(1).strip() if e else ""
        
        # metaTitle
        mt = re.search(r'metaTitle:\s*"([^"]*)"', post_text)
        post["metaTitle"] = mt.group(1) if mt else ""
        
        # metaDescription
        md = re.search(r'metaDescription:\s*"([^"]*)"', post_text)
        post["metaDescription"] = md.group(1) if md else ""
        
        # tags
        tags_match = re.search(r'tags:\s*\[(.*?)\]', post_text, re.DOTALL)
        if tags_match:
            tags_str = tags_match.group(1)
            post["tags"] = re.findall(r'"([^"]*)"', tags_str)
        else:
            post["tags"] = []
        
        # content - everything inside the backtick template literal
        content_match = re.search(r'content:\s*`\n(.*?)\n\s*`', post_text, re.DOTALL)
        if content_match:
            post["content"] = content_match.group(1)
        else:
            # Try without leading newline
            content_match = re.search(r'content:\s*`(.*?)`', post_text, re.DOTALL)
            post["content"] = content_match.group(1) if content_match else ""
        
        posts[slug] = post
    
    return posts


def extract_primary_keyword(title):
    """Extract the primary keyword from the title."""
    # Remove common prefixes like "Complete", "Ultimate", "The", "A"
    cleaned = re.sub(r'^(Complete |Ultimate |The |A |An )', '', title, flags=re.IGNORECASE)
    
    # Look for the main subject (first meaningful noun phrase)
    # Common patterns for SEO blog titles
    patterns = [
        r'SEO for ([A-Za-z\s-]+?)(?:\s*in\s|$|:)',
        r'([A-Za-z\s-]+?)(?:\s*SEO|\s*Optimization|\s*Guide|\s*Strategy|\s*Tips)',
    ]
    
    for p in patterns:
        m = re.search(p, cleaned, re.IGNORECASE)
        if m:
            return m.group(1).strip()
    
    # Fallback: first 3 meaningful words
    words = [w for w in cleaned.split() if len(w) > 3]
    if words:
        return ' '.join(words[:3])
    return cleaned.split()[0] if cleaned.split() else title


def count_keyword_in_content(content, keyword):
    """Count occurrences of keyword in content (case-insensitive)."""
    if not keyword or not content:
        return 0
    # Escape special regex chars
    escaped = re.escape(keyword)
    return len(re.findall(escaped, content, re.IGNORECASE))


def check_entities(content, title, tags, slug):
    """Check semantic entity coverage."""
    required_entities = {
        "location: Dhaka": r'\bDhaka\b',
        "location: Bangladesh": r'\bBangladesh\b',
    }
    
    # Industry-specific entities based on slug/tags/title
    text_lower = (title + " " + " ".join(tags) + " " + slug).lower()
    
    industry_entities = {}
    if any(w in text_lower for w in ["fitness", "gym", "gyms"]):
        industry_entities["industry: fitness/gym"] = r'\b(gym|fitness|workout|exercise)\b'
    if any(w in text_lower for w in ["law", "firm", "firms", "legal", "lawyer"]):
        industry_entities["industry: legal/law"] = r'\b(law|legal|lawyer|attorney|firm)\b'
    if any(w in text_lower for w in ["startup", "startups"]):
        industry_entities["industry: startup"] = r'\b(startup|start.?up|venture)\b'
    if any(w in text_lower for w in ["b2b", "lead", "lead generation"]):
        industry_entities["industry: B2B"] = r'\b(b2b|lead generation|business.?to.?business)\b'
    if any(w in text_lower for w in ["ecommerce", "e-commerce", "daraz", "shopify"]):
        industry_entities["industry: e-commerce"] = r'\b(ecommerce|e.?commerce|online.?store|retail)\b'
    if any(w in text_lower for w in ["healthcare", "medical", "clinic", "clinics", "health"]):
        industry_entities["industry: healthcare"] = r'\b(healthcare|medical|clinic|doctor|patient)\b'
    if any(w in text_lower for w in ["education", "educational", "school", "university", "institution"]):
        industry_entities["industry: education"] = r'\b(education|educational|school|university|college)\b'
    if any(w in text_lower for w in ["hotel", "resort", "travel", "tourism", "tourist"]):
        industry_entities["industry: hospitality/travel"] = r'\b(hotel|resort|travel|tourism|tourist)\b'
    if any(w in text_lower for w in ["real estate", "property", "developer", "agents"]):
        industry_entities["industry: real estate"] = r'\b(real estate|property|developer|apartment|land)\b'
    if any(w in text_lower for w in ["restaurant", "food"]):
        industry_entities["industry: restaurant/food"] = r'\b(restaurant|food|cafe|dining)\b'
    if any(w in text_lower for w in ["garment", "textile", "garments"]):
        industry_entities["industry: garment/textile"] = r'\b(garment|textile|apparel|readymade)\b'
    if any(w in text_lower for w in ["ngo", "non-profit", "nonprofit", "non profit"]):
        industry_entities["industry: NGO/non-profit"] = r'\b(ngo|non.?profit|nonprofit|charity)\b'
    if any(w in text_lower for w in ["youtube", "video"]):
        industry_entities["industry: YouTube"] = r'\b(youtube|video|channel|creator)\b'
    if any(w in text_lower for w in ["podcast"]):
        industry_entities["industry: podcast"] = r'\b(podcast|audio|episode)\b'
    if any(w in text_lower for w in ["mobile app", "mobile apps"]):
        industry_entities["industry: mobile app"] = r'\b(mobile app|app.?store|android|ios)\b'
    if any(w in text_lower for w in ["wedding", "event"]):
        industry_entities["industry: wedding/event"] = r'\b(wedding|event|planner|celebration)\b'
    if any(w in text_lower for w in ["photographer", "videographer", "photography"]):
        industry_entities["industry: photography"] = r'\b(photographer|videographer|photography|photo)\b'
    
    # Schema/technical posts
    if any(w in text_lower for w in ["schema", "structured data", "json-ld", "faq", "howto", "breadcrumb"]):
        industry_entities["technical: schema"] = r'\b(schema|structured data|json.?ld|markup|rich snippet)\b'
    if any(w in text_lower for w in ["canonical", "redirect", "robots.txt", "sitemap", "hreflang"]):
        industry_entities["technical: SEO"] = r'\b(canonical|redirect|robots|sitemap|hreflang)\b'
    
    all_entities = {**required_entities, **industry_entities}
    
    missing = []
    for name, pattern in all_entities.items():
        if not re.search(pattern, content, re.IGNORECASE):
            missing.append(name)
    
    return missing


def check_pillar_link(content, tags, slug, title):
    """Check if post links to its pillar page based on tags."""
    text_lower = (title + " " + slug + " " + " ".join(tags)).lower()
    
    # Map topic to expected pillar page URL
    pillar_pages = {
        "local-seo": ["/blog/local-seo-tips-dhaka-businesses-google-maps", "/local-seo-dhaka"],
        "on-page-seo": ["/blog/complete-seo-guide-bangladesh-businesses-2026"],
        "technical-seo": ["/blog/technical-seo-checklist-bangladeshi-websites"],
        "content": ["/blog/content-marketing-seo-friendly-content-writing"],
        "ecommerce": ["/blog/ecommerce-seo-daraz-shopify-guide"],
        "link-building": ["/blog/link-building-bangladesh-strategies"],
        "schema": ["/blog/seo-structured-data-guide-bd"],
        "geo": ["/blog/geo-optimization-prepare-business-ai-search"],
        "seo-guide": ["/blog/complete-seo-guide-bangladesh-businesses-2026"],
        "seo-tips": ["/blog/seo-tips-for-business-owners-bd"],
        "seo-agency": ["/blog/how-to-choose-right-seo-agency-bangladesh"],
        "seo-cost": ["/blog/seo-services-cost-bangladesh-pricing-guide"],
        "seo-vs-ppc": ["/blog/seo-vs-ppc-advertising-bangladesh"],
        "seo-vs-ads": ["/blog/seo-vs-google-ads-bangladesh-business"],
        "google-business": ["/blog/google-business-profile-optimization-guide-bangladesh"],
        "keyword": ["/blog/keyword-research-bangladesh-market"],
        "mobile": ["/blog/mobile-seo-optimization-bangladesh-mobile-first-era"],
        "international": ["/blog/international-seo-bangladesh-exporters-global-buyers"],
        "seo-trends": ["/blog/seo-trends-2026-ai-geo-future"],
        "core-web-vitals": ["/blog/technical-seo-core-web-vitals-optimization"],
        "career": ["/blog/seo-career-guide-bangladesh-2026"],
        "competitor": ["/blog/seo-competitor-analysis-bangladesh"],
    }
    
    # Determine which pillar(s) this post might belong to
    matched_pillars = []
    for pillar_key, _, in pillar_pages.items():
        if pillar_key in text_lower:
            matched_pillars.append(pillar_key)
    
    if not matched_pillars:
        return "unknown pillar", None
    
    # Check content for links to any pillar URL
    links_found = []
    for pillar in matched_pillars:
        expected_urls = pillar_pages[pillar]
        for url in expected_urls:
            # Check with and without /blog/ prefix
            if url in content or url.replace("/blog/", "/") in content:
                links_found.append(url)
    
    if links_found:
        return matched_pillars, links_found
    else:
        return matched_pillars, None


def check_aeo_geo_optimization(content):
    """Count question-based headings (AEO/GEO optimization)."""
    # Match markdown headings that start with question words
    question_pattern = r'^#{2,6}\s+(How|What|Why|When|Where|Can|Do|Is|Are|Which|Who|Whose)\b'
    matches = re.findall(question_pattern, content, re.MULTILINE | re.IGNORECASE)
    return len(matches), matches


def count_internal_links(content):
    """Count internal links to other posts, services, locations."""
    # Internal links are relative paths starting with /
    # /blog/... /services/... /locations/... /about /contact etc.
    internal_pattern = r'\[([^\]]*)\]\((/[^)]+)\)'
    all_links = re.findall(internal_pattern, content)
    
    # Filter to internal links only (not external http/https or anchors)
    internal = []
    external = []
    for text, url in all_links:
        if url.startswith('http') or url.startswith('#'):
            external.append(url)
        else:
            internal.append(url)
    
    return len(internal), internal


def check_schema_readiness(post):
    """Check if post has all fields needed for ArticleSchema."""
    missing = []
    
    if not post.get("title"):
        missing.append("title")
    if not post.get("excerpt"):
        missing.append("excerpt")
    if not post.get("date"):
        missing.append("date")
    if not post.get("author"):
        missing.append("author") 
    if not post.get("dateModified"):
        missing.append("dateModified")
    if not post.get("metaTitle"):
        missing.append("metaTitle")
    if not post.get("metaDescription"):
        missing.append("metaDescription")
    
    return missing


def check_post(post, slug):
    """Run all framework checks on a single post."""
    title = post.get("title", "")
    content = post.get("content", "")
    tags = post.get("tags", [])
    excerpt = post.get("excerpt", "")
    
    results = {}
    
    # A. TF-IDF Coverage
    keyword = extract_primary_keyword(title)
    occurrences = count_keyword_in_content(content, keyword)
    results["tf_idf"] = {
        "keyword": keyword,
        "occurrences": occurrences,
        "pass": occurrences >= 5
    }
    
    # B. Entities
    missing_entities = check_entities(content, title, tags, slug)
    results["entities"] = {
        "missing": missing_entities,
        "pass": len(missing_entities) == 0
    }
    
    # C. Pillar Link
    pillar_topics, pillar_links = check_pillar_link(content, tags, slug, title)
    results["pillar"] = {
        "topics": pillar_topics,
        "links": pillar_links,
        "pass": pillar_links is not None and len(pillar_links) > 0
    }
    
    # D. AEO/GEO
    q_count, q_headings = check_aeo_geo_optimization(content)
    results["aeo_geo"] = {
        "count": q_count,
        "headings": q_headings,
        "pass": q_count >= 2
    }
    
    # E. Internal Links
    link_count, links = count_internal_links(content)
    results["internal_links"] = {
        "count": link_count,
        "links": links,
        "pass": link_count >= 3
    }
    
    # F. Schema
    schema_missing = check_schema_readiness(post)
    results["schema"] = {
        "missing": schema_missing,
        "pass": len(schema_missing) == 0
    }
    
    return results


def generate_report(results, post, slug):
    """Generate a report line for a single post."""
    title = post.get("title", slug)
    
    lines = []
    lines.append(f"## Post: {slug}")
    lines.append(f'**Title:** {title}')
    lines.append("")
    lines.append("| Check | Status | Details |")
    lines.append("|-------|--------|---------|")
    
    # TF-IDF
    tf = results["tf_idf"]
    status = "✅" if tf["pass"] else "❌"
    lines.append(f"| TF-IDF: `{tf['keyword']}` | {status} | {tf['occurrences']} occurrences (min 5) |")
    
    # Entities
    en = results["entities"]
    status = "✅" if en["pass"] else "❌"
    details = "All entities covered" if en["pass"] else f"Missing: {', '.join(en['missing'])}"
    lines.append(f"| Entities | {status} | {details} |")
    
    # Pillar
    pi = results["pillar"]
    if pi["topics"] == "unknown pillar":
        status = "⚠️"
        details = "Could not determine pillar"
    else:
        status = "✅" if pi["pass"] else "❌"
        if pi["links"]:
            details = f"Links to: {', '.join(pi['links'])}"
        else:
            details = f"Pillar(s): {', '.join(pi['topics'])} — no pillar link found"
    lines.append(f"| Pillar Link | {status} | {details} |")
    
    # AEO/GEO
    aeo = results["aeo_geo"]
    status = "✅" if aeo["pass"] else "❌"
    details = f"{aeo['count']} question heading(s) found (min 2)"
    if aeo["count"] > 0:
        details += f": {', '.join(aeo['headings'][:5])}"
    lines.append(f"| AEO/GEO | {status} | {details} |")
    
    # Internal Links
    il = results["internal_links"]
    status = "✅" if il["pass"] else "❌"
    details = f"{il['count']} internal link(s) (min 3)"
    if il["links"]:
        details += f": {', '.join(il['links'][:5])}"
    lines.append(f"| Internal Links | {status} | {details} |")
    
    # Schema
    sc = results["schema"]
    status = "✅" if sc["pass"] else "❌"
    details = "All fields set" if sc["pass"] else f"Missing: {', '.join(sc['missing'])}"
    lines.append(f"| Schema Ready | {status} | {details} |")
    
    lines.append("")
    
    # Fix instructions
    fix_lines = []
    if not tf["pass"]:
        fix_lines.append(f"- **TF-IDF too thin**: Keyword `{tf['keyword']}` appears only {tf['occurrences']} times. Add {5 - tf['occurrences']}+ more mentions naturally throughout the content.")
    if not en["pass"]:
        fix_lines.append(f"- **Missing entities**: Add mentions of: {', '.join(en['missing'])}")
    if not pi["pass"] and pi["topics"] != "unknown pillar":
        fix_lines.append(f"- **No pillar link**: Add internal link to pillar page for {', '.join(pi['topics'])}")
    if not aeo["pass"]:
        fix_lines.append(f"- **Low AEO/GEO**: Add at least {2 - aeo['count']} more question-based headings (How, What, Why, etc.)")
    if not il["pass"]:
        fix_lines.append(f"- **Thin internal linking**: Add at least {3 - il['count']} more internal links to related posts, services, or locations")
    if not sc["pass"]:
        fix_lines.append(f"- **Schema incomplete**: Set missing fields: {', '.join(sc['missing'])}")
    
    if fix_lines:
        lines.append("### Fix instructions:")
        for l in fix_lines:
            lines.append(l)
        lines.append("")
    
    return "\n".join(lines)


def main():
    print("# Content Framework Enforcement Report — kanokmiah.com.bd")
    print(f"**Date:** (48-hour window from run time)")
    print(f"**Posts checked:** {len(MODIFIED_SLUGS)} modified posts")
    print("")
    
    if not os.path.exists(DATAJS_PATH):
        print(f"❌ ERROR: {DATAJS_PATH} not found!")
        return
    
    print("Parsing data.js... ", end="", flush=True)
    posts = parse_posts(DATAJS_PATH)
    print(f"done ({len(posts)} total posts found)")
    print("")
    
    passed_all = 0
    failed_any = 0
    not_found = 0
    
    for slug in MODIFIED_SLUGS:
        if slug not in posts:
            print(f"⚠️  Post '{slug}' not found in data.js (may have different slug format)")
            not_found += 1
            continue
        
        post = posts[slug]
        results = check_post(post, slug)
        
        all_pass = all(
            results[k]["pass"] for k in ["tf_idf", "entities", "pillar", "aeo_geo", "internal_links", "schema"]
        )
        
        if all_pass:
            passed_all += 1
        else:
            failed_any += 1
            report = generate_report(results, post, slug)
            print(report)
    
    # Summary
    print("---")
    print("## Summary")
    print(f"| Metric | Count |")
    print(f"|--------|-------|")
    print(f"| Total modified posts | {len(MODIFIED_SLUGS)} |")
    print(f"| Found in data.js | {len(MODIFIED_SLUGS) - not_found} |")
    print(f"| ✅ All checks passed | {passed_all} |")
    print(f"| ❌ At least one check failed | {failed_any} |")
    print(f"| ⚠️  Not found | {not_found} |")
    
    if failed_any == 0 and passed_all > 0:
        print("")
        print("🎉 **All posts pass all framework checks!**")
    
    print("")
    print("---")
    print("*Report generated by Content Framework Enforcer*")


if __name__ == "__main__":
    main()
