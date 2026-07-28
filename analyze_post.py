#!/usr/bin/env python3
"""Analyze the mir-cement-seo-case-study blog post."""
import json, re, math, collections, sys
from collections import Counter
from pathlib import Path

# Load the post data
slug = "mir-cement-seo-case-study"
title = "Mir Cement SEO Case Study: 0 to 500+ Monthly Organic Visitors for a B2B Brand"
date = "2026-06-08"
tags = ["Case Study", "SEO", "B2B SEO", "Construction"]
excerpt = "How Mir Cement achieved 500+ monthly organic visitors, 12+ top-10 keyword rankings, and reduced bounce rate from 78% to 42% — driving B2B leads with zero ad spend."

content = """## The Challenge: Decades of Experience, Zero Online Visibility
Mir Cement had decades of industry experience as a trusted cement brand in Bangladesh, yet the company had zero organic rankings for competitive terms like "cement price Bangladesh" and "best cement in Bangladesh." The website had thin product pages under 150 words, no local landing pages despite nationwide coverage, no B2B citation presence on any Bangladesh directory, no blog or content marketing, and severe technical SEO gaps.

In a market with 30+ established cement brands competing for the same B2B buyers, Mir Cement was invisible during the crucial research phase of the purchasing journey.

## The Solution: Five-Pillar B2B SEO Strategy

### Pillar 1: Comprehensive Keyword Research

We mapped 3 tiers of keywords: transactional (buy cement, cement price), brand/category (best cement brand in Bangladesh, Portland cement), and informational long-tail (cement storage tips, concrete mix ratio guide). This created a complete picture of the B2B buyer journey.

### Pillar 2: Content Strategy

Product pages were rewritten to 1,200-1,500 words with technical specifications and current pricing. Brand comparison guides were created to help buyers evaluate options. Educational blog content was localized for Bangladesh, addressing construction professionals specific needs and questions.

### Pillar 3: On-Page SEO

Every page received comprehensive on-page optimization including title tags, meta descriptions, header structure, image optimization, and internal linking.

### Pillar 4: Technical SEO

Organization, Product, FAQ, Breadcrumb, and LocalBusiness schema markup was implemented. Page speed was reduced from 6.8 seconds to 2.1 seconds through image optimization, caching, and code minification.

### Pillar 5: B2B Citation Building

We built 40+ B2B citations on Bangladesh-specific directories, construction portals, and trade platforms with 100% NAP consistency. This established the brand's authority in the digital B2B ecosystem.

## The Results

The comprehensive strategy delivered impressive results:

- **Monthly Organic Visitors**: 0 to 500+
- **Keywords in Top 10**: 0 to 12+
- **Keywords in Top 50**: 0 to 80+
- **GBP Views**: N/A to 8,000+/month
- **GBP Enquiries**: 0 to 40+/month
- **B2B Citations**: 0 to 40+ consistent listings
- **Page Speed (Mobile)**: 6.8s to 2.1s
- **Bounce Rate**: 78% to 42%
- **Ad Spend**: $0

## Key Takeaways for B2B Brands

B2B SEO requires a different approach than B2C. Decision-makers in construction and manufacturing conduct extensive research before purchasing, and being visible at every stage of that research journey is critical.

As the **best SEO expert in Dhaka**, I specialize in B2B SEO strategies that help Bangladeshi manufacturers and suppliers dominate search results. Visit [kanokmiah.com.bd](https://kanokmiah.com.bd/) to learn how we can transform your B2B brand's online visibility.

- [B2B SEO](/blog/b2b-lead-generation-seo-bangladesh) — B2B Lead Generation SEO
- [technical SEO](/services/technical-seo) — Technical SEO Services
- Garments & Textile industry — Garments SEO

## Conclusion

Mir Cement journey from zero visibility to 500+ monthly organic visitors proves that B2B brands in Bangladesh can achieve remarkable SEO results. With comprehensive keyword research, in-depth content, technical optimization, and consistent citations, any B2B brand can dominate its market.
    
আপনার সাইটের জন্য [গার্মেন্টস ও টেক্সটাইল শিল্পের জন্য SEO পৃষ্ঠা](/industries/garments-textile)-এর মাধ্যমে আরও উন্নত SEO ফলাফল পেতে পারেন। শিল্প-নির্দিষ্ট SEO কৌশল সম্পর্কে আরও জানতে আমাদের ইন্ডাস্ট্রি পৃষ্ঠা দেখুন।

Looking for the SEO expert in Dhaka.

**[SEO services in Dhaka neighborhoods](/locations/dhaka)**.
Looking for the Kanok Miah.

Looking for the [SEO expert in Dhaka](/)."""


print("=" * 70)
print("BLOG POST ANALYSIS REPORT")
print(f"Post: {slug}")
print(f"Title: {title}")
print(f"Date: {date}")
print(f"Tags: {tags}")
print(f"Excerpt: {excerpt}")
print("=" * 70)

# ============================================================
# CHECK 1: TF-IDF Analysis
# ============================================================
print("\n\n## CHECK 1: TF-IDF ANALYSIS")
print("-" * 50)

# Tokenize: extract words from content (skip Bengali for TF-IDF)
words_en = re.findall(r'[a-zA-Z]+(?:-[a-zA-Z]+)?', content.lower())
# Filter out common stop words
stop_words = set("the a an in of to and is for on that with by are be has from as at was were it or not but have this all can will each its which would about their into than other these some after also been between over such through during before then after".split())
filtered_words = [w for w in words_en if w.lower() not in stop_words and len(w) > 2]

word_freq = Counter(filtered_words)
total_words = len(filtered_words)

print(f"Total English words (filtered): {total_words}")
print(f"Unique words: {len(word_freq)}")
print("\nTop 30 words by frequency (TF approximation):")
for i, (word, count) in enumerate(word_freq.most_common(30), 1):
    tf = count / total_words * 100
    print(f"  {i:2d}. {word:25s} count={count:3d}  TF={tf:.2f}%")

# Key domain terms check
domain_terms = ['cement', 'seo', 'b2b', 'bangladesh', 'organic', 'keywords', 
                'technical', 'content', 'citations', 'brand', 'page', 'search',
                'visibility', 'buyer', 'construction', 'price', 'ranking']
print("\nDomain term presence:")
for term in domain_terms:
    c = word_freq.get(term, 0)
    print(f"  {term:20s}: {c} occurrences")

# ============================================================
# CHECK 2: ENTITY ANALYSIS
# ============================================================
print("\n\n## CHECK 2: ENTITY ANALYSIS")
print("-" * 50)

# Named entities extraction (simple regex-based)
entities = {
    "BRANDS": list(set(re.findall(r'Mir Cement', content))),
    "LOCATIONS": list(set(re.findall(r'Bangladesh|Dhaka', content))),
    "PEOPLE": list(set(re.findall(r'Kanok Miah', content))),
}

# Extract capitalized phrases (potential entities)
capitalized_phrases = re.findall(r'[A-Z][a-z]+(?:\s[A-Z][a-z]+)*', content)
cap_counts = Counter(capitalized_phrases)
print("Top capitalized phrases (potential entities):")
for phrase, count in cap_counts.most_common(25):
    if len(phrase) > 2 and phrase not in ["The", "This", "We", "It", "Our", "Its", "Every", "Each", "These", "With", "Pillar"]:
        print(f"  {phrase:40s}: {count}")

print("\nEntity categories found:")
print(f"  - Brand: Mir Cement")
print(f"  - Location: Bangladesh, Dhaka")
print(f"  - Person: Kanok Miah")
print(f"  - Schema types: Organization, Product, FAQ, Breadcrumb, LocalBusiness")
print(f"  - Service: B2B SEO, Technical SEO, SEO services")

# ============================================================
# CHECK 3: PILLAR-CLUSTER ANALYSIS
# ============================================================
print("\n\n## CHECK 3: PILLAR-CLUSTER ANALYSIS")
print("-" * 50)

# Check for pillar topic and cluster structure
pillar_topics = re.findall(r'Pillar \d|^###.*?(?:Pillar|pillar)', content, re.MULTILINE)
print(f"Pillar references found: {len(pillar_topics)}")
for p in pillar_topics:
    print(f"  - {p.strip()}")

# Check internal links pointing to cluster content
internal_links = re.findall(r'\[([^\]]+)\]\((/[^\)]+)\)', content)
print(f"\nInternal links found: {len(internal_links)}")
for text, url in internal_links:
    print(f"  [{text}]({url})")

# Check for topic cluster structure
print("\nTopic cluster assessment:")
has_pillar_structure = len(re.findall(r'Pillar \d|pillar', content, re.IGNORECASE)) > 0
has_linked_content = len(internal_links) > 0
print(f"  Has pillar structure: {has_pillar_structure}")
print(f"  Has linked cluster content: {has_linked_content}")
print(f"  Cluster links point to:")
for text, url in internal_links:
    link_type = "same-topic" if "b2b" in url.lower() or "seo" in url.lower() else "other"
    print(f"    [{text}]({url}) -> {link_type}")

# ============================================================
# CHECK 4: AEO/GEO ANALYSIS
# ============================================================
print("\n\n## CHECK 4: AEO/GEO ANALYSIS")
print("-" * 50)

# Check for AEO/GEO features
aeo_geo_checks = {
    "Has FAQ section": bool(re.search(r'FAQ|Frequently Asked Questions', content, re.IGNORECASE)),
    "Has question headings": bool(re.search(r'^###\s+.+\?', content, re.MULTILINE)),
    "Has schema markup mentioned": bool(re.search(r'schema|Schema|structured data|Structured Data', content)),
    "Has AI search mention": bool(re.search(r'AI|artificial intelligence|generative|SGE', content, re.IGNORECASE)),
    "Has direct answers format": bool(re.search(r'^\*\*.*?\*\*:', content, re.MULTILINE)),
    "Has bullet points": bool(re.search(r'^- \*\*', content, re.MULTILINE)),
    "Bengali language present": bool(re.search(r'[\u0980-\u09FF]', content)),
}

print("AEO/GEO readiness check:")
for check, result in aeo_geo_checks.items():
    print(f"  {'✓' if result else '✗'} {check}")

# Count question-based content
questions = re.findall(r'^###\s+.*\?', content, re.MULTILINE)
print(f"\nQuestion-based headings: {len(questions)}")
for q in questions:
    print(f"  - {q.strip()}")

# Structured data readiness
print("\nStructured data (schema) readiness:")
schema_types = re.findall(r'(Organization|Product|FAQ|Breadcrumb|LocalBusiness|Review|Article|Service|BreadcrumbList|HowTo)', content)
schema_counts = Counter(schema_types)
for s_type, count in schema_counts.most_common():
    print(f"  - {s_type}: {count} mentions")

# ============================================================
# CHECK 5: INTERNAL LINKS ANALYSIS
# ============================================================
print("\n\n## CHECK 5: INTERNAL LINKS ANALYSIS")
print("-" * 50)

all_links = re.findall(r'\[([^\]]*)\]\(([^\)]*)\)', content)
print(f"Total links found: {len(all_links)}")
internal_count = 0
external_count = 0
for text, url in all_links:
    if url.startswith('/'):
        internal_count += 1
    elif url.startswith('http'):
        external_count += 1
    print(f"  [{text}]({url})")

print(f"\n  Internal links: {internal_count}")
print(f"  External links: {external_count}")

# Links analysis
print("\nInternal link breakdown by path:")
for text, url in all_links:
    if url.startswith('/'):
        parts = url.split('/')
        section = parts[1] if len(parts) > 1 else '/'
        print(f"  [{text}]({url}) -> section: /{section}")

# ============================================================
# CHECK 6: SCHEMA ANALYSIS
# ============================================================
print("\n\n## CHECK 6: SCHEMA ANALYSIS")
print("-" * 50)

schema_mentions = {
    "Organization": "Organization schema mentioned",
    "Product": "Product schema mentioned",
    "FAQ": "FAQ schema mentioned",
    "Breadcrumb": "Breadcrumb schema mentioned",
    "LocalBusiness": "LocalBusiness schema mentioned",
}

print("Schema types mentioned in content:")
for schema_type, desc in schema_mentions.items():
    found = schema_type.lower() in content.lower()
    print(f"  {'✓' if found else '✗'} {desc}")

# Check for schema implementation evidence
schema_implemented = re.findall(r'(?:schema|structured data).*?(?:implement|add|markup)', content, re.IGNORECASE)
print(f"\nSchema implementation references: {len(schema_implemented)}")
for ref in schema_implemented:
    print(f"  - {ref.strip()[:80]}...")

# Check for schema.org references
schema_org_refs = re.findall(r'schema\.org|Schema\.org', content)
print(f"Schema.org references: {len(schema_org_refs)}")

# ============================================================
# OVERALL ASSESSMENT
# ============================================================
print("\n\n" + "=" * 70)
print("OVERALL SEO AUDIT SUMMARY")
print("=" * 70)

checks_results = {
    "TF-IDF: Keyword density": "PASS - Good density of target terms (cement, B2B, SEO, Bangladesh)",
    "Entities: Brand & Location": "PASS - Mir Cement, Bangladesh, Dhaka, Kanok Miah all present",
    "Entities: Schema types": "PASS - 5 schema types mentioned (Organization, Product, FAQ, Breadcrumb, LocalBusiness)",
    "Pillar-Cluster: Structure": "PASS - Five-pillar B2B SEO strategy clearly defined",
    "Pillar-Cluster: Internal links": "PASS - 4+ internal links to related content",
    "AEO/GEO: Question format": "MODERATE - No FAQ section or question-answer format in this post",
    "AEO/GEO: Bengali content": "PASS - Bengali text present at end",
    "Internal Links: Quantity": "PASS - Multiple internal links to related services and blog posts",
    "Internal Links: Diversity": "PASS - Links to /blog/, /services/, /locations/, /industries/ paths",
    "Schema: Coverage": "PASS - Multiple schema types referenced in content strategy",
}

for check, result in checks_results.items():
    print(f"  {check:55s} | {result}")

print("\n" + "=" * 70)
print("RECOMMENDATIONS")
print("=" * 70)
print("""
1. ADD FAQ SECTION: The post lacks a FAQ section or question-answer format which is
   critical for AEO/GEO and featured snippet capture. Add 3-5 FAQs like:
   - "How long did Mir Cement's SEO take to show results?"
   - "What was the most effective SEO strategy for Mir Cement?"
   - "Can B2B brands in Bangladesh achieve SEO without ad spend?"

2. ADD SCHEMA MARKUP: The post mentions schema types but doesn't implement them.
   Add Article schema, FAQ schema (after adding FAQ), and HowTo schema for the
   five-pillar strategy section.

3. IMPROVE INTERNAL LINKING: Add links to related B2B SEO content like:
   - B2B Lead Generation SEO blog post
   - Construction industry SEO page
   - Technical SEO services page

4. ADD ENTITY-OPTIMIZED CONTENT: Include more entity-rich information about
   Mir Cement as a business, its locations, and specific product details.

5. ADD STATISTICAL SOURCES: Cite authoritative sources for cement industry data
   to boost EEAT signals.

6. ADD TABLE STRUCTURED DATA: The results section with metrics would benefit
   from structured data markup to enable rich results.
""")
