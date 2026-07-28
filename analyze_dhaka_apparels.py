#!/usr/bin/env python3
"""Comprehensive framework check for dhaka-apparels-seo-case-study"""

import re
import json
from collections import Counter

CONTENT = """## The Challenge: Starting from Absolute Zero
Dhaka Apparels started from absolute zero — a completely new domain with no authority, no indexed pages, no backlinks, no Google Business Profile, and no local search presence. They were competing against established garments suppliers with 5+ years of SEO history, hundreds of indexed pages, and strong backlink profiles.

In Bangladesh $50+ billion RMG (Ready-Made Garments) sector, Dhaka Apparels was entering a market where every competitor had years of head start in online visibility.

## The Solution: Five-Phase Structured Plan

### Phase 1: Foundation

A lead-generation website was built with under 200ms server response time and under 2 seconds mobile load speed. The design was mobile-first with click-to-call functionality, SEO-optimized URL structure, and logical internal linking architecture.

### Phase 2: Content That Converts

Instead of generic descriptions, we addressed real B2B buyer objections: MOQ (Minimum Order Quantity), export documentation, and quality grading. Dedicated pages were created for each service category with depth over volume — preferring comprehensive, authoritative content over thin, keyword-stuffed pages.

### Phase 3: Technical SEO and AI Readiness

Schema markup (Organization and Product) was implemented alongside Core Web Vitals optimization achieving all Good scores. Structured FAQ blocks were designed specifically for AI-generated search summaries — anticipating how Google Search Generative Experience would display content.

### Phase 4: Local SEO

The Google Business Profile was fully optimized with real photos of the facility and products. NAP consistency was ensured across all platforms. Location-targeted keywords were integrated throughout the content.

### Phase 5: Authority Building

Selective, contextual backlinks were earned from trade directories and B2B platforms only. Quality was prioritized over quantity, with every backlink adding genuine value to the site's authority profile.

## The Results

The impact was achieved in just 90 days:

- **Top Keyword Ranking**: #1 for "best stock garments supplier in bd"
- **Impressions (90 days)**: 14,700
- **AI Search Appearances**: Featured in Google AI-generated search summaries
- **Domain Authority**: 0 (started as brand new domain)
- **Timeline**: 90 days from zero to #1
- **Ad Spend**: $0

## Key Takeaways for New Domains

This case study proves that new domains can compete and win against established competitors. The key is a strategic, phased approach that prioritizes technical excellence, conversion-focused content, and AI-readiness from day one.

As the **best SEO expert in Dhaka**, I specialize in helping Bangladeshi garment manufacturers and B2B businesses achieve rapid SEO results on new domains. Visit [kanokmiah.com.bd](https://kanokmiah.com.bd/) to learn how we can take your business from zero to #1 in your market.

- [B2B SEO](/blog/b2b-lead-generation-seo-bangladesh) — B2B Lead Generation SEO
- Garments & Textile industry — Garments & Textile SEO
- [Mir Cement case study](/blog/mir-cement-seo-case-study) — Mir Cement Case Study

## Conclusion

Dhaka Apparels achievement of #1 ranking in 90 days on a brand new domain demonstrates that with the right strategy, new entrants can dominate even competitive B2B markets. Technical excellence, buyer-focused content, and AI readiness are the keys to rapid SEO success.
    
আপনার সাইটের জন্য [গার্মেন্টস ও টেক্সটাইল শিল্পের জন্য SEO পৃষ্ঠা](/industries/garments-textile)-এর মাধ্যমে আরও উন্নত SEO ফলাফল পেতে পারেন। গার্মেন্টস শিল্পের জন্য শিল্প-নির্দিষ্ট SEO কৌশল সম্পর্কে বিস্তারিত জানতে আমাদের ইন্ডাস্ট্রি পৃষ্ঠা দেখুন।

Looking for the professional SEO services.

**[SEO services in Dhaka neighborhoods](/locations/dhaka)**.
Looking for the best SEO expert in Bangladesh.

Looking for the [SEO expert in Dhaka](/)."""

POST_DATA = {
    "slug": "dhaka-apparels-seo-case-study",
    "title": "Dhaka Apparels SEO Case Study: Zero to #1 Ranking in 90 Days",
    "date": "2026-06-12",
    "author": "Kanok Miah",
    "excerpt": "How a brand new domain achieved #1 ranking for 'best stock garments supplier in bd' in just 90 days, generating 14,700 impressions and appearing in Google AI search summaries.",
    "tags": ["Case Study", "SEO", "B2B SEO", "Garments"],
    "imagePlaceholder": "📊",
    "tags_list": ["Case Study", "SEO", "B2B SEO", "Garments"]
}

print("=" * 70)
print("FRAMEWORK CHECK REPORT")
print("=" * 70)
print(f"Post: {POST_DATA['slug']}")
print(f"Title: {POST_DATA['title']}")
print(f"Date: {POST_DATA['date']}")
print(f"Author: {POST_DATA['author']}")
print(f"Tags: {', '.join(POST_DATA['tags'])}")
print(f"Content Length: {len(CONTENT)} chars, ~{len(CONTENT.split())} words")
print()

# ============================================================
# 1. TF-IDF / Keyword Density
# ============================================================
print("-" * 70)
print("1️⃣  TF-IDF / KEYWORD DENSITY")
print("-" * 70)

# Check for primary keyword patterns
keywords_to_check = {
    "seo case study": r"[Ss][Ee][Oo]\s+[Cc]ase\s+[Ss]tud(?:y|ies)",
    "garments": r"[Gg]arment",
    "b2b": r"[Bb]2[Bb]",
    "90 days": r"90\s+[Dd]ays",
    "ranking": r"[Rr]anking|[Rr]ank",
    "dhaka apparels": r"[Dd]haka\s+[Aa]pparels",
    "supplier": r"[Ss]upplier"
}

print(f"{'Keyword':<25} {'Occurrences':<15} {'Status':<10}")
print("-" * 50)
for kw, pattern in keywords_to_check.items():
    matches = re.findall(pattern, CONTENT)
    count = len(matches)
    threshold = 2
    status = "✅ PASS" if count >= threshold else "⚠️  LOW" if count >= 1 else "❌ MISS"
    print(f"{kw:<25} {count:<15} {status:<10}")

# Primary keyword focus check
primary_kw = "seo case study"
primary_count = len(re.findall(keywords_to_check[primary_kw], CONTENT))
tfidf_status = "✅ PASS" if primary_count >= 2 else "❌ FAIL"
print(f"\nPrimary keyword '{primary_kw}': {primary_count} occurrences → {tfidf_status}")

# Content-length appropriate density
word_count = len(CONTENT.split())
print(f"Word count: {word_count}")
if word_count >= 500:
    print("Content length: ✅ PASS (≥500 words)")
else:
    print("Content length: ❌ FAIL (<500 words)")

# ============================================================
# 2. Entity Coverage
# ============================================================
print()
print("-" * 70)
print("2️⃣  ENTITY COVERAGE")
print("-" * 70)

required_entities = {
    "Dhaka": r"[Dd]haka",
    "Bangladesh": r"[Bb]angladesh",
    "Google": r"[Gg]oogle",
    "SEO": r"[Ss][Ee][Oo]",
    "Garments/Apparel": r"[Gg]arment|[Aa]pparel",
    "B2B": r"[Bb]2[Bb]",
    "Domain": r"[Dd]omain",
    "90 Days": r"90\s+[Dd]ays",
}

print(f"{'Entity':<25} {'Present?':<15} {'Occurrences':<15}")
print("-" * 55)
for entity, pattern in required_entities.items():
    matches = re.findall(pattern, CONTENT)
    count = len(matches)
    present = "✅ Yes" if count > 0 else "❌ No"
    print(f"{entity:<25} {present:<15} {count:<15}")

# Additional named entity extraction
entities_found = Counter()
# Look for key named entities
named_patterns = {
    "Dhaka Apparels": r"Dhaka\s+Apparels",
    "Kanok Miah": r"Kanok\s+Miah",
    "Google Business Profile": r"Google\s+Business\s+Profile",
    "Core Web Vitals": r"Core\s+Web\s+Vitals",
    "Google SGE": r"Google\s+Search\s+Generative\s+Experience|SGE",
    "RMG": r"RMG|Ready[-\s]Made\s+Garments",
    "MOQ": r"MOQ|Minimum\s+Order\s+Quantity",
    "B2B": r"B2B",
}
for name, pat in named_patterns.items():
    c = len(re.findall(pat, CONTENT))
    if c > 0:
        entities_found[name] = c

print()
print("Additional Named Entities Detected:")
for name, count in entities_found.most_common(20):
    print(f"  • {name}: {count}")

# ============================================================
# 3. Pillar-Cluster Alignment
# ============================================================
print()
print("-" * 70)
print("3️⃣  PILLAR-CLUSTER ALIGNMENT")
print("-" * 70)

expected_pillar_patterns = ["/services/", "/industries/", "/blog/"]
found_pillar_links = []

# Extract all markdown links
link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
all_links = re.findall(link_pattern, CONTENT)

internal_links = []
external_links = []

for text, url in all_links:
    if url.startswith("/"):
        internal_links.append((text, url))
        # Check if it's a pillar link
        for pillar in expected_pillar_patterns:
            if url.startswith(pillar):
                found_pillar_links.append((text, url))
    elif url.startswith("http"):
        external_links.append((text, url))

print(f"\nInternal links found: {len(internal_links)}")
for text, url in internal_links:
    pillar = ""
    for p in expected_pillar_patterns:
        if url.startswith(p):
            pillar = f" ← PILLAR: {p}"
    print(f"  • [{text}]({url}){pillar}")

print(f"\nPillar links found: {len(found_pillar_links)}")
for text, url in found_pillar_links:
    print(f"  • [{text}]({url})")

# Identify which pillar pages are linked
pillar_categories = set()
for _, url in found_pillar_links:
    for p in expected_pillar_patterns:
        if url.startswith(p):
            pillar_categories.add(p)

print(f"\nPillar categories linked: {pillar_categories if pillar_categories else 'NONE'}")

# Check what pillars exist for this topic
# Post is about garments/B2B case study - should link to:
# /industries/garments-textile, /services/, /blog/
relevant_pillars = {
    "/industries/garments-textile": "Garments & Textile industry pillar",
    "/services/": "Services pillar",
    "/blog/": "Blog pillar"
}

print("\nRelevant pillar pages for this post:")
for pillar, desc in relevant_pillars.items():
    linked = any(pillar in url for _, url in found_pillar_links)
    status = "✅ LINKED" if linked else "❌ NOT LINKED"
    print(f"  {status}: {pillar} ({desc})")

pillar_status = "✅ PASS" if len(pillar_categories) >= 1 else "❌ FAIL"
print(f"\nPillar-Cluster check: {pillar_status} (need ≥1 pillar link, found {len(pillar_categories)})")

# ============================================================
# 4. AEO/GEO Question Headings
# ============================================================
print()
print("-" * 70)
print("4️⃣  AEO/GEO - QUESTION HEADINGS & AI READINESS")
print("-" * 70)

# Extract all headings
h2_pattern = r'^## (.+)$'
h3_pattern = r'^### (.+)$'
all_heading_lines = []

for line in CONTENT.split('\n'):
    if line.startswith('## '):
        all_heading_lines.append(('h2', line.lstrip('# ').strip()))
    elif line.startswith('### '):
        all_heading_lines.append(('h3', line.lstrip('# ').strip()))

question_headings = []
for htype, heading in all_heading_lines:
    if '?' in heading:
        question_headings.append(f"[{htype}] {heading}")

print(f"\nTotal headings (H2/H3): {len(all_heading_lines)}")
print(f"Question-based headings: {len(question_headings)}")
print(f"Threshold: ≥2")

if question_headings:
    print("\nQuestion headings found:")
    for qh in question_headings:
        print(f"  • {qh}")
else:
    print("\nNo question-based headings found.")

aeo_geo_status = "✅ PASS" if len(question_headings) >= 2 else "❌ FAIL"
print(f"\nAEO/GEO check: {aeo_geo_status}")

# Check AEO/GEO content indicators
geo_indicators = {
    "AI search": r"[Aa][Ii]\s+[Ss]earch|AI[-\s]generated|AI[-\s]readiness",
    "Generative Engine": r"[Gg]enerative\s+[Ee]ngine|GEO",
    "Schema markup": r"[Ss]chema\s+markup|[Ss]tructured\s+data",
    "FAQ blocks": r"[Ff]AQ|[Ff]requently\s+[Aa]sked",
    "Featured snippets": r"[Ff]eatured\s+[Ss]nippet|[Aa]I[-\s]generated\s+[Ss]ummar",
    "Entity": r"[Ee]ntit",
}

print("\nAEO/GEO Content Indicators:")
for indicator, pattern in geo_indicators.items():
    matches = re.findall(pattern, CONTENT)
    count = len(matches)
    present = "✅" if count > 0 else "❌"
    print(f"  {present} {indicator}: {count} occurrences")

# ============================================================
# 5. Internal Links Count
# ============================================================
print()
print("-" * 70)
print("5️⃣  INTERNAL LINKS")
print("-" * 70)

print(f"\nTotal internal links: {len(internal_links)}")
unique_internal_paths = set(url for _, url in internal_links)
print(f"Unique internal link destinations: {len(unique_internal_paths)}")
print(f"Threshold: ≥3 unique internal links")

print("\nLink Inventory:")
for text, url in all_links:
    link_type = "INTERNAL" if url.startswith("/") else "EXTERNAL" if url.startswith("http") else "OTHER"
    print(f"  [{text}]({url}) — {link_type}")

print(f"\nUnique internal paths: {unique_internal_paths if unique_internal_paths else 'NONE'}")

internal_links_status = "✅ PASS" if len(unique_internal_paths) >= 3 else "❌ FAIL" if len(unique_internal_paths) < 2 else "⚠️  BORDERLINE"
print(f"Internal Links check: {internal_links_status}")

# ============================================================
# 6. Schema Readiness
# ============================================================
print()
print("-" * 70)
print("6️⃣  SCHEMA READINESS")
print("-" * 70)

schema_checks = {
    "Title": POST_DATA["title"] != "",
    "Description/Excerpt": POST_DATA["excerpt"] != "",
    "Date (published)": POST_DATA["date"] != "",
    "Author": POST_DATA["author"] != "",
    "Tags": len(POST_DATA["tags"]) > 0,
}

print(f"\n{'Field':<25} {'Status':<15} {'Value':<30}")
print("-" * 70)
for field, present in schema_checks.items():
    val = POST_DATA.get(field.lower().split()[0], "")
    if field == "Title":
        val = POST_DATA["title"][:40]
    elif field == "Description/Excerpt":
        val = POST_DATA["excerpt"][:40]
    elif field == "Date (published)":
        val = POST_DATA["date"]
    elif field == "Author":
        val = POST_DATA["author"]
    elif field == "Tags":
        val = ", ".join(POST_DATA["tags"])
    status = "✅ SET" if present else "❌ MISSING"
    print(f"{field:<25} {status:<15} {val:<30}")

schema_status = "✅ PASS" if all(schema_checks.values()) else "❌ FAIL"
print(f"\nSchema Readiness check: {schema_status}")

# Article schema fields
print("\nArticle Schema fields available:")
article_schema = {
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": POST_DATA["title"],
    "description": POST_DATA["excerpt"],
    "datePublished": POST_DATA["date"],
    "author": {
        "@type": "Person",
        "name": POST_DATA["author"]
    }
}
print(json.dumps(article_schema, indent=2))

# ============================================================
# OVERALL SCORE
# ============================================================
print()
print("=" * 70)
print("OVERALL ASSESSMENT")
print("=" * 70)

results = []
# Check 1: TF-IDF
t1 = tfidf_status
results.append(("TF-IDF / Keyword Density", t1, f"Primary '{primary_kw}': {primary_count} occurrences"))

# Check 2: Entities
entity_pass = all(len(re.findall(pattern, CONTENT)) > 0 for pattern in required_entities.values())
t2 = "✅ PASS" if entity_pass else "❌ FAIL"
missing_entities = [e for e, p in required_entities.items() if len(re.findall(p, CONTENT)) == 0]
detail2 = f"All entities covered" if entity_pass else f"Missing: {', '.join(missing_entities)}"
results.append(("Entity Coverage", t2, detail2))

# Check 3: Pillar
t3 = pillar_status
detail3 = f"{len(pillar_categories)} pillar categories linked" if pillar_categories else "No pillar links found"
results.append(("Pillar-Cluster Alignment", t3, detail3))

# Check 4: AEO/GEO
t4 = aeo_geo_status
detail4 = f"{len(question_headings)} question headings found" if question_headings else "No question headings"
results.append(("AEO/GEO Question Headings", t4, detail4))

# Check 5: Internal Links
t5 = internal_links_status
detail5 = f"{len(unique_internal_paths)} unique internal link(s): {', '.join(unique_internal_paths) if unique_internal_paths else 'none'}"
results.append(("Internal Links", t5, detail5))

# Check 6: Schema
t6 = schema_status
detail6 = "All metadata fields populated" if all(schema_checks.values()) else "Missing fields"
results.append(("Schema Readiness", t6, detail6))

print(f"\n{'#':<3} {'Check':<30} {'Status':<15} Detail")
print("-" * 75)
pass_count = 0
fail_count = 0
for i, (name, status, detail) in enumerate(results, 1):
    print(f"{i:<3} {name:<30} {status:<15} {detail}")
    if "PASS" in status:
        pass_count += 1
    else:
        fail_count += 1

print()
print(f"OVERALL: {pass_count}/{len(results)} PASS — {fail_count} FAIL{'ING' if fail_count > 0 else ''}")
if fail_count > 0:
    print("\n❌ FAILING CHECKS:")
    for name, status, detail in results:
        if "FAIL" in status:
            print(f"  • {name}: {detail}")

print()
print("=" * 70)
print("RECOMMENDATIONS")
print("=" * 70)
recs = []
if pillar_status == "❌ FAIL":
    recs.append("Add at least one link to a pillar page (/industries/garments-textile, /services/, or /blog/)")
if internal_links_status in ("❌ FAIL", "⚠️  BORDERLINE"):
    recs.append(f"Add more internal links — currently have {len(unique_internal_paths)}, need ≥3 unique destinations")
if tfidf_status == "❌ FAIL":
    recs.append("Increase usage of primary keyword 'seo case study' in content")
if not entity_pass:
    recs.append(f"Add missing entities: {', '.join(missing_entities)}")
if aeo_geo_status == "❌ FAIL":
    recs.append("Add question-based headings (H2/H3 with '?') for AEO/GEO optimization")

if not recs:
    recs.append("All checks pass — no changes needed")
for r in recs:
    print(f"  • {r}")

print()
print("=" * 70)
print("DETAILED LINK INVENTORY")
print("=" * 70)
for i, (text, url) in enumerate(all_links, 1):
    link_type = "INTERNAL" if url.startswith("/") else "EXTERNAL"
    print(f"{i}. [{text}]({url}) — {link_type}")
