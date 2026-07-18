#!/usr/bin/env python3
"""
Blog post content framework checker - refined version.
Reads posts from data.js and runs 6 framework checks.
Handles Bengali and English mixed content properly.
"""

import re
import json

# Read content for each post from the file
post_line_ranges = {
    "seo-referral-traffic-bangladesh": (13560, 13708),
    "seo-page-authority-bangladesh": (13423, 13550),
    "seo-domain-authority-bangladesh": (13281, 13413),
    "seo-hubspot-vs-wordpress-bd": (13142, 13271),
    "seo-content-repurposing-bangladesh": (13004, 13132),
    "seo-skyscraper-technique-bangladesh": (12895, 12994),
    "seo-pillar-content-strategy-bd": (12757, 12885),
    "seo-for-podcast-bangladesh": (12647, 12747),
    "google-discover-seo-bangladesh": (12559, 12637),
    "seo-for-mobile-apps-bangladesh": (12468, 12549),
}

def read_post_content(slug):
    if slug not in post_line_ranges:
        return ""
    start, end = post_line_ranges[slug]
    try:
        with open("/root/kanok-miahit/src/app/blog/data.js", "r", encoding="utf-8") as f:
            lines = f.readlines()
        content_lines = lines[start-1:end]
        content = "".join(content_lines)
        # Remove leading backtick and trailing `, or backtick
        if content.startswith('`'):
            content = content[1:]
        if content.endswith('`,\n'):
            content = content[:-3]
        elif content.endswith('`'):
            content = content[:-1]
        return content
    except Exception as e:
        print(f"Error reading {slug}: {e}")
        return ""

def extract_keyword(title):
    """Extract primary keyword from the title - first meaningful noun phrase."""
    # For Bengali titles like "রেফারেল ট্রাফিক: লিংক বিল্ডিং ছাড়া..."
    # The keyword is before the colon
    if ':' in title:
        keyword = title.split(':')[0].strip()
    elif '—' in title:
        keyword = title.split('—')[0].strip()
    else:
        # Take first 2-3 words
        words = title.strip().split()
        keyword = ' '.join(words[:3])
    return keyword

def count_occurrences(text, keywords):
    """Count occurrences of keyword (try multiple variants)."""
    text_lower = text.lower()
    total = 0
    for kw in keywords:
        count = len(re.findall(re.escape(kw), text_lower))
        total += count
    return total

def get_keyword_variants(keyword, slug, title):
    """Get keyword variants to search for in content."""
    variants = {keyword.lower()}
    
    # For English slug posts, also search the main topic words
    slug_to_keywords = {
        "seo-referral-traffic-bangladesh": ["referral traffic", "রেফারেল ট্রাফিক"],
        "seo-page-authority-bangladesh": ["page authority", "পেজ অথরিটি", "পিএ"],
        "seo-domain-authority-bangladesh": ["domain authority", "ডোমেইন অথরিটি", "ডিএ", "da"],
        "seo-hubspot-vs-wordpress-bd": ["hubspot", "wordpress", "shopify", "প্ল্যাটফর্ম তুলনা", "ওয়ার্ডপ্রেস", "শপিফাই", "হাবস্পট"],
        "seo-content-repurposing-bangladesh": ["content repurposing", "কন্টেন্ট রিপারপাজিং"],
        "seo-skyscraper-technique-bangladesh": ["skyscraper technique", "স্কাইস্ক্র্যাপার টেকনিক", "স্কাইস্ক্র্যাপার"],
        "seo-pillar-content-strategy-bd": ["pillar content strategy", "পিলার কন্টেন্ট স্ট্র্যাটেজি", "পিলার কন্টেন্ট"],
        "seo-for-podcast-bangladesh": ["podcast seo", "পডকাস্ট", "পডকাস্ট seo"],
        "google-discover-seo-bangladesh": ["google discover", "গুগল ডিসকভার", "ডিসকভার"],
        "seo-for-mobile-apps-bangladesh": ["app store optimization", "aso", "mobile app seo", "অ্যাপ স্টোর"],
    }
    
    if slug in slug_to_keywords:
        for kw in slug_to_keywords[slug]:
            variants.add(kw.lower())
    
    return variants

def check_entities(text, slug):
    """Check for required entities in content."""
    text_lower = text.lower()
    missing = []
    
    # Location-specific: Dhaka and Bangladesh MUST appear
    if 'dhaka' not in text_lower and 'ঢাকা' not in text:
        missing.append("Dhaka/ঢাকা")
    if 'bangladesh' not in text_lower and 'বাংলাদেশ' not in text:
        missing.append("Bangladesh/বাংলাদেশ")
    
    # Service-specific entities
    service_checks = {
        "seo-referral-traffic-bangladesh": {
            "terms": [("referral traffic", "রেফারেল ট্রাফিক"), ("link building", "লিংক বিল্ডিং")],
        },
        "seo-page-authority-bangladesh": {
            "terms": [("page authority", "পেজ অথরিটি"), ("pa", "পিএ")],
        },
        "seo-domain-authority-bangladesh": {
            "terms": [("domain authority", "ডোমেইন অথরিটি"), ("da", "ডিএ")],
        },
        "seo-hubspot-vs-wordpress-bd": {
            "terms": [("wordpress", "ওয়ার্ডপ্রেস"), ("shopify", "শপিফাই"), ("hubspot", "হাবস্পট")],
        },
        "seo-content-repurposing-bangladesh": {
            "terms": [("content repurposing", "কন্টেন্ট রিপারপাজিং")],
        },
        "seo-skyscraper-technique-bangladesh": {
            "terms": [("skyscraper", "স্কাইস্ক্র্যাপার"), ("backlink", "ব্যাকলিংক")],
        },
        "seo-pillar-content-strategy-bd": {
            "terms": [("pillar content", "পিলার কন্টেন্ট"), ("topic cluster", "টপিক ক্লাস্টার")],
        },
        "seo-for-podcast-bangladesh": {
            "terms": [("podcast", "পডকাস্ট"), ("audio", "অডিও")],
        },
        "google-discover-seo-bangladesh": {
            "terms": [("google discover", "গুগল ডিসকভার"), ("discover", "ডিসকভার")],
        },
        "seo-for-mobile-apps-bangladesh": {
            "terms": [("app store", "অ্যাপ স্টোর"), ("aso",), ("mobile app", "মোবাইল অ্যাপ")],
        },
    }
    
    if slug in service_checks:
        for term_group in service_checks[slug]["terms"]:
            found = False
            for term in term_group:
                if term.lower() in text_lower:
                    found = True
                    break
            if not found:
                missing.append(f"{term_group[0]}")
    
    # Industry terms
    industry_found = any(t in text_lower for t in ['seo', 'search engine', 'google', 'গুগল', 'সার্চ'])
    if not industry_found:
        missing.append("SEO/Search industry terms")
    
    return missing

def count_question_headings(text):
    """Count headings that start with question words."""
    heading_pattern = re.compile(r'^#{2,3}\s+(.+)$', re.MULTILINE)
    headings = heading_pattern.findall(text)
    question_words = [
        'কীভাবে', 'কী', 'কেন', 'কখন', 'কোথায়', 'How', 'What', 'Why', 'When', 'Where', 
        'Can', 'Do', 'Is', 'Are', 'Does', 'Will', 'Would', 'Should', 'Could', 'May'
    ]
    count = 0
    for h in headings:
        h_stripped = h.strip()
        for qw in question_words:
            if h_stripped.lower().startswith(qw.lower()):
                count += 1
                break
    return count

def count_internal_links(text):
    """Count internal links."""
    # Match href="/path" patterns
    href_links = re.findall(r'href="((?:/)(?:blog|services|locations|industries|about|contact)[^"]*)"', text)
    # Match markdown links [...](/path)
    md_links = re.findall(r'\]\(((?:/)(?:blog|services|locations|industries|about|contact)[^)]*)\)', text)
    # Also match root / links
    root_links = re.findall(r'href="(/)"', text)
    
    all_links = set(href_links + md_links)
    for link in root_links:
        all_links.add(link)
    
    # Count all internal links in the text (including duplicates for counting)
    all_link_matches = href_links + md_links + root_links
    
    return len(all_link_matches), sorted(all_links)

def check_pillar_link(text):
    """Check if post links to a pillar page (links to /blog/path or /services/path)."""
    pillar_pattern = re.findall(r'href="((?:/blog|/services)/[^"]+)"', text)
    md_pillar = re.findall(r'\]\(((?:/blog|/services)/[^)]+)\)', text)
    all_pillar = set(pillar_pattern + md_pillar)
    return all_pillar

# Post metadata
post_meta = {
    "seo-referral-traffic-bangladesh": {
        "title": "রেফারেল ট্রাফিক: লিংক বিল্ডিং ছাড়া ট্রাফিক বাড়ান",
        "date": "2026-07-08",
        "excerpt": "রেফারেল ট্রাফিক কীভাবে আপনার ওয়েবসাইটে আনা যায় — সোশ্যাল মিডিয়া, ফোরাম, অনলাইন কমিউনিটি এবং কন্টেন্ট সিন্ডিকেশনের মাধ্যমে ট্রাফিক বাড়ানোর কৌশল।",
    },
    "seo-page-authority-bangladesh": {
        "title": "পেজ অথরিটি: প্রতিটি পৃষ্ঠার শক্তি বাড়ান",
        "date": "2026-07-08",
        "excerpt": "পেজ অথরিটি (PA) কী, এটি কীভাবে কাজ করে এবং আপনার ওয়েবসাইটের প্রতিটি পৃষ্ঠার অথরিটি বাড়ানোর কৌশল — বিস্তারিত বাংলা গাইড।",
    },
    "seo-domain-authority-bangladesh": {
        "title": "ডোমেইন অথরিটি: বাংলাদেশি ওয়েবসাইটের DA বাড়ানোর উপায়",
        "date": "2026-07-08",
        "excerpt": "ডোমেইন অথরিটি (DA) কী, কেন এটি গুরুত্বপূর্ণ এবং কীভাবে বাংলাদেশি ওয়েবসাইটের DA বাড়ানো যায় — সম্পূর্ণ বাংলা গাইড।",
    },
    "seo-hubspot-vs-wordpress-bd": {
        "title": "SEO প্ল্যাটফর্ম তুলনা: হাবস্পট বনাম ওয়ার্ডপ্রেস বনাম শপিফাই",
        "date": "2026-07-08",
        "excerpt": "হাবস্পট, ওয়ার্ডপ্রেস এবং শপিফাই — তিনটি জনপ্রিয় প্ল্যাটফর্মের SEO ফিচার, সুবিধা এবং অসুবিধার বিস্তারিত তুলনা। বাংলাদেশি ব্যবসার জন্য কোনটি সেরা?",
    },
    "seo-content-repurposing-bangladesh": {
        "title": "কন্টেন্ট রিপারপাজিং: একটি কন্টেন্ট থেকে একাধিক আর্টিকেল",
        "date": "2026-07-08",
        "excerpt": "কন্টেন্ট রিপারপাজিং কৌশল — একটি কন্টেন্টকে বিভিন্ন ফরম্যাটে রূপান্তর করে আরও বেশি ট্রাফিক, ব্যাকলিংক এবং এনগেজমেন্ট পাওয়ার উপায়।",
    },
    "seo-skyscraper-technique-bangladesh": {
        "title": "স্কাইস্ক্র্যাপার টেকনিক: সেরা কন্টেন্ট তৈরি ও র‍্যাঙ্কিং",
        "date": "2026-07-08",
        "excerpt": "স্কাইস্ক্র্যাপার টেকনিক কীভাবে কাজ করে — প্রতিযোগীদের সেরা কন্টেন্ট খুঁজে তার চেয়ে ভালো কন্টেন্ট তৈরি করে ব্যাকলিংক এবং র‍্যাংকিংয়ে এগিয়ে যাওয়ার কৌশল।",
    },
    "seo-pillar-content-strategy-bd": {
        "title": "পিলার কন্টেন্ট স্ট্র্যাটেজি: টপিক্যাল অথরিটি বাড়ান",
        "date": "2026-07-08",
        "excerpt": "পিলার কন্টেন্ট স্ট্র্যাটেজি কীভাবে আপনার ওয়েবসাইটের টপিক্যাল অথরিটি বাড়ায় এবং সার্চ ইঞ্জিনে ভালো র‍্যাংক করতে সাহায্য করে — বিস্তারিত বাংলা গাইড।",
    },
    "seo-for-podcast-bangladesh": {
        "title": "পডকাস্টের জন্য SEO: অডিও কন্টেন্ট র‍্যাঙ্কিংয়ের কৌশল",
        "date": "2026-07-08",
        "excerpt": "পডকাস্টের জনপ্রিয়তা বাড়ছে। আপনার পডকাস্টকে সার্চ ইঞ্জিনে কীভাবে র‍্যাংক করাবেন, লিসেনার বাড়াবেন এবং অডিও কন্টেন্ট থেকে অর্গানিক ট্রাফিক পাবেন তার সম্পূর্ণ গাইড।",
    },
    "google-discover-seo-bangladesh": {
        "title": "গুগল ডিসকভার SEO: ট্রাফিক বাড়ান নতুন উপায়ে",
        "date": "2026-07-08",
        "excerpt": "গুগল ডিসকভার হল একটি পার্সোনালাইজড কন্টেন্ট ফিড যা ইউজারদের আগ্রহের ভিত্তিতে কন্টেন্ট দেখায়। কীভাবে আপনার কন্টেন্টকে গুগল ডিসকভারে র‍্যাংক করাবেন এবং বিপুল ট্রাফিক পাবেন তার সম্পূর্ণ গাইড।",
    },
    "seo-for-mobile-apps-bangladesh": {
        "title": "মোবাইল অ্যাপের জন্য SEO: অ্যাপ স্টোর অপটিমাইজেশন",
        "date": "2026-07-08",
        "excerpt": "অ্যাপ স্টোর অপটিমাইজেশন (ASO) হল মোবাইল অ্যাপের জন্য SEO। গুগল প্লে স্টোর এবং অ্যাপ স্টোরে আপনার অ্যাপকে কীভাবে র‍্যাংক করাবেন এবং আরও ডাউনলোড পাবেন তার সম্পূর্ণ গাইড।",
    },
}

print("=" * 100)
print("BLOG POST CONTENT FRAMEWORK ANALYSIS")
print("=" * 100)

results = []

for slug, meta in post_meta.items():
    content = read_post_content(slug)
    if not content:
        print(f"\n⚠️  Could not read content for {slug}")
        continue
    
    content_len = len(content)
    
    # A. TF-IDF Coverage
    keyword = extract_keyword(meta["title"])
    keyword_variants = get_keyword_variants(keyword, slug, meta["title"])
    occurrences = count_occurrences(content, keyword_variants)
    tfidf_status = "✅" if occurrences >= 5 else "❌"
    
    # B. Entities
    missing_entities = check_entities(content, slug)
    entities_status = "✅" if len(missing_entities) == 0 else "❌"
    
    # C. Pillar Link
    pillar_links = check_pillar_link(content)
    pillar_status = "✅" if len(pillar_links) > 0 else "❌"
    
    # D. AEO/GEO
    q_headings = count_question_headings(content)
    aeo_status = "✅" if q_headings >= 2 else "❌"
    
    # E. Internal Links
    internal_count, internal_link_set = count_internal_links(content)
    links_status = "✅" if internal_count >= 3 else "❌"
    
    # F. Schema Ready
    schema_missing = []
    for field in ["title", "excerpt", "date"]:
        if not meta.get(field):
            schema_missing.append(field)
    schema_status = "✅" if len(schema_missing) == 0 else "❌"
    
    results.append({
        "slug": slug,
        "title": meta["title"],
        "keyword": keyword,
        "variants": keyword_variants,
        "tfidf": (tfidf_status, occurrences),
        "entities": (entities_status, missing_entities),
        "pillar": (pillar_status, sorted(list(pillar_links))[:5]),
        "aeo": (aeo_status, q_headings),
        "links": (links_status, internal_count),
        "schema": (schema_status, schema_missing),
        "content_len": content_len,
    })

# Print results
for r in results:
    # Build fix instructions
    fixes = []
    if r['tfidf'][0] == '❌':
        fixes.append(f"Add keyword '{r['keyword']}' (or variants: {', '.join(r['variants'])}) at least 5 times in content (currently {r['tfidf'][1]})")
    if r['entities'][0] == '❌':
        fixes.append(f"Add missing entities: {', '.join(r['entities'][1])}")
    if r['pillar'][0] == '❌':
        fixes.append("Add at least one link to pillar page (/blog/... or /services/...)")
    if r['aeo'][0] == '❌':
        fixes.append(f"Add at least {2 - r['aeo'][1]} more question-based headings (How, What, Why, etc.)")
    if r['links'][0] == '❌':
        fixes.append(f"Add internal links to reach minimum 3 (currently {r['links'][1]})")
    if r['schema'][0] == '❌':
        fixes.append(f"Add missing schema fields: {', '.join(r['schema'][1])}")
    
    print(f"""
## Post: {r['slug']}
| Check | Status | Details |
|-------|--------|---------|
| TF-IDF: {r['keyword'][:40]} | {r['tfidf'][0]} | {r['tfidf'][1]} occurrences (variants: {', '.join(list(r['variants'])[:3])}) |
| Entities | {r['entities'][0]} | Missing: {', '.join(r['entities'][1]) if r['entities'][1] else 'None'} |
| Pillar Link | {r['pillar'][0]} | Links to: {', '.join(r['pillar'][1]) if r['pillar'][1] else 'None'} |
| AEO/GEO | {r['aeo'][0]} | {r['aeo'][1]} question headings |
| Internal Links | {r['links'][0]} | {r['links'][1]} total |
| Schema Ready | {r['schema'][0]} | All fields set (title, excerpt, date) |
### {"Fix instructions:" if fixes else "All checks passed ✅"}
{chr(10).join(fixes) if fixes else "No fixes needed."}
""")

# Executive Summary
print("\n\n" + "=" * 100)
print("EXECUTIVE SUMMARY")
print("=" * 100)

all_pass = sum(1 for r in results if all([
    r['tfidf'][0] == '✅',
    r['entities'][0] == '✅', 
    r['pillar'][0] == '✅',
    r['aeo'][0] == '✅',
    r['links'][0] == '✅',
    r['schema'][0] == '✅'
]))

print(f"""
Total posts analyzed: {len(results)}
Posts passing all 6 checks: {all_pass}
Posts with at least one issue: {len(results) - all_pass}
""")

# Summary by check
checks_summary = {
    "A. TF-IDF Coverage (≥5 occurrences)": sum(1 for r in results if r['tfidf'][0] == '✅'),
    "B. Entity Coverage": sum(1 for r in results if r['entities'][0] == '✅'),
    "C. Pillar Link": sum(1 for r in results if r['pillar'][0] == '✅'),
    "D. AEO/GEO (≥2 question headings)": sum(1 for r in results if r['aeo'][0] == '✅'),
    "E. Internal Linking (≥3)": sum(1 for r in results if r['links'][0] == '✅'),
    "F. Schema Ready": sum(1 for r in results if r['schema'][0] == '✅'),
}
print("| # | Check | Pass Rate |")
print("|---|-------|-----------|")
for i, (check, count) in enumerate(checks_summary.items(), 1):
    print(f"| {i} | {check} | {count}/{len(results)} ({count*100//len(results)}%) |")

# Detailed breakdown
print("\n\n### Posts Needing TF-IDF Fixes:")
for r in results:
    if r['tfidf'][0] == '❌':
        print(f"- {r['slug']}: '{r['keyword']}' only {r['tfidf'][1]} occurrences (need ≥5)")

print("\n### Posts Needing Entity Fixes:")
for r in results:
    if r['entities'][0] == '❌':
        print(f"- {r['slug']}: Missing {', '.join(r['entities'][1])}")

print("\n### Posts Needing AEO/GEO Improvements:")
for r in results:
    if r['aeo'][0] == '❌':
        print(f"- {r['slug']}: Only {r['aeo'][1]} question heading(s) (need ≥2)")

print("\n### Posts Passing All Checks:")
for r in results:
    if all([r['tfidf'][0] == '✅', r['entities'][0] == '✅', r['pillar'][0] == '✅', r['aeo'][0] == '✅', r['links'][0] == '✅', r['schema'][0] == '✅']):
        print(f"- {r['slug']}")
