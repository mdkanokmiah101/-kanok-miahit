#!/usr/bin/env python3
"""SEO audit for smmsun-seo-case-study blog post."""
import re, json, math
from collections import Counter

POST = {
    "slug": "smmsun-seo-case-study",
    "title": "SMMSun SEO Case Study: 15,440% Traffic Growth in 13 Months",
    "date": "2026-06-03",
    "author": "Kanok Miah",
    "excerpt": "How SMMSun grew from 50 monthly organic clicks to 7,700+ — a 15,440% increase — by building a content foundation, optimizing technical SEO, and achieving a 14.2% CTR.",
    "tags": ["Case Study", "SEO", "SMM Panel", "Growth Strategy"],
    "content": """
## The Challenge: Quality Services, Zero Visibility
[SMMSun](https://smmsun.com) had quality services, competitive pricing, and fast delivery — but was completely invisible on Google. The site was generating only ~50 monthly organic clicks with just 2 low-value keywords ranking. There were zero organic leads, thin generic content averaging 150-200 words per page, and minimal trust signals in a crowded SMM panel market.

In an industry where hundreds of established competitors compete for the same keywords, SMMSun needed a strategy that would cut through the noise and establish genuine authority.

## The Solution: Four-Phase Growth Strategy

### Phase 1: Content Foundation

We mapped 120+ search terms across 4 intent categories. The homepage was rebuilt around the positioning "Best Affordable SMM Panel in Bangladesh." Dedicated service pages were created for each platform — Instagram, YouTube, Facebook, TikTok — with comprehensive FAQ sections and schema markup.

### Phase 2: On-Page and Technical SEO

A hub-and-spoke internal linking model was implemented to distribute authority throughout the site. Core Web Vitals were optimized, reducing LCP from 4.2 seconds to 1.8 seconds. Mobile-first UX was prioritized, and title and meta descriptions were rewritten for higher CTR.

### Phase 3: Content Expansion

Structured content clusters were built with pillar pages and supporting articles. Each cluster targeted a specific theme — Instagram growth, YouTube marketing, TikTok engagement — creating a comprehensive web of authoritative content.

### Phase 4: E-E-A-T Building

Experience, Expertise, Authoritativeness, and Trustworthiness signals were strengthened through consistent content quality, transparent business information, and genuine customer testimonials.

## The Results

After 13 months of execution:

- **Monthly Organic Clicks**: ~50 to 7,700+
- **Traffic Growth**: 15,440%
- **CTR**: 14.2% (double the industry average)
- **Keywords Mapped**: 120+ across 4 intent categories
- **Mobile Traffic Share**: 75%+
- **LCP Improvement**: 4.2s to 1.8s
- **Ad Spend**: $0

## Key Takeaways

The 14.2% CTR — double the industry average — was achieved through meticulous meta description optimization and compelling title tags. Every search result was crafted to stand out in the crowded SERP.

As the **best SEO expert in Dhaka**, I use these same content-cluster and technical optimization strategies for SMM panels in Bangladesh and beyond. Visit [kanokmiah.com.bd](https://kanokmiah.com.bd/) to discover how we can drive exponential traffic growth for your platform.

- [content clusters](/services/on-page-seo) — On-Page SEO Services
- [technical optimization](/services/technical-seo) — Technical SEO Services
- [SMMGen case study](/blog/smmgen-seo-case-study) — SMMGen Case Study

## Conclusion

SMMSun 15,440% traffic growth in just 13 months proves that a well-structured content strategy combined with technical excellence can deliver extraordinary results in competitive markets — all without spending a single dollar on advertising.
    
আপনার সাইটের জন্য [ই-কমার্স SEO সেবা](/services/ecommerce-seo)-এর মাধ্যমে আরও উন্নত SEO ফলাফল পেতে পারেন। এসএএস ব্যবসার জন্য ই-কমার্স SEO এবং কন্টেন্ট অপটিমাইজেশন সম্পর্কে জানতে আমাদের সেবা দেখুন।

Looking for the SEO expert in Dhaka.

**[SEO services in Dhaka neighborhoods](/locations/dhaka)**.
Looking for the best SEO expert in Bangladesh.

Looking for the [SEO consultant](/),
"""
}

# Clean text: remove markdown links, markdown formatting
def clean_text(text):
    # Remove markdown links [text](url) -> text
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    # Remove image alt text ![alt](url)
    text = re.sub(r'!\[[^\]]*\]\([^\)]+\)', '', text)
    # Remove bold/italic markers
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    text = re.sub(r'\*([^*]+)\*', r'\1', text)
    # Remove heading markers
    text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)
    # Remove list markers
    text = re.sub(r'^[-*]\s+', '', text, flags=re.MULTILINE)
    return text

text = clean_text(POST["content"])

# Extract all internal links (relative paths starting with /)
internal_links = re.findall(r'\[([^\]]+)\]\((/[^\)]+)\)', POST["content"])
# Extract all external links
external_links = re.findall(r'\[([^\]]+)\]\((https?://[^\)]+)\)', POST["content"])

# Word count
words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
word_count = len(words)

# ======== TF-IDF (simple version for this single doc) ========
# TF: term frequency within this post
tf = Counter(words)
total_terms = len(words)
# Common English stopwords
stopwords = set("the a an is it it's its in on at to for of and or not no be by with as from but if so than that this there their they have has had do does did will would could should may might can shall are was were been being having doing got get getting make made making use used using need needed needing know known knowing see saw seen show shown showing".split())

# Filter stopwords
tf_filtered = {k: v for k, v in tf.items() if k not in stopwords and len(k) > 2}
tf_sorted = sorted(tf_filtered.items(), key=lambda x: -x[1])[:30]

# ======== ENTITY EXTRACTION ========
# Identify named entities (capitalized phrases, numbers, brands)
# Simple regex-based NER
entities = {
    "Brands": [],
    "People": [],
    "Locations": [],
    "Metrics": [],
    "Platforms": [],
    "Technologies": [],
}

# Brands
brands_pattern = re.findall(r'\b(SMMSun|SMMGen|Google|Ahrefs|SEMrush)\b', POST["content"])
entities["Brands"] = list(set(brands_pattern))

# People
people_pattern = re.findall(r'\b(Kanok Miah)\b', POST["content"])
entities["People"] = list(set(people_pattern))

# Locations
locations_pattern = re.findall(r'\b(Bangladesh|Dhaka|Edinburgh|Glasgow|Fife)\b', POST["content"])
entities["Locations"] = list(set(locations_pattern))

# Platforms
platforms_pattern = re.findall(r'\b(Instagram|YouTube|Facebook|TikTok|LinkedIn)\b', POST["content"])
entities["Platforms"] = list(set(platforms_pattern))

# Metrics/numbers
metrics = re.findall(r'\b(\d[\d,]*%|\d[\d,]*\+?)\b', POST["content"])
entities["Metrics"] = [m for m in set(metrics) if any(c in m for c in ['%',',','+','0'])]

# ======== PILLAR-CLUSTER ANALYSIS ========
pillar_keywords = ["content clusters", "pillar pages", "supporting articles", "hub-and-spoke", "topical authority"]
pillar_found = [kw for kw in pillar_keywords if kw.lower() in POST["content"].lower()]

# ======== AEO/GEO ANALYSIS ========
geo_keywords = ["generative engine optimization", "ai search", "featured snippet", "answer engine", "sge", "chatgpt", "perplexity", "ai-powered", "structured data", "schema markup", "FAQ", "question", "answer"]
geo_found = [kw for kw in geo_keywords if kw.lower() in POST["content"].lower()]

# ======== INTERNAL LINKS ANALYSIS ========
internal_links_analysis = []
for link_text, url in internal_links:
    internal_links_analysis.append({"text": link_text.strip(), "url": url, "type": "internal"})

external_links_analysis = []
for link_text, url in external_links:
    external_links_analysis.append({"text": link_text.strip(), "url": url, "type": "external"})

# ======== SCHEMA ANALYSIS ========
# Check content for schema-related mentions
schema_mentions = re.findall(r'\b(schema|structured data|markup|LD\+JSON|JSON-LD|microdata|rich snippet)\b', POST["content"].lower())
schema_types = re.findall(r'\b(FAQ|Product|Organization|LocalBusiness|Breadcrumb|Review|HowTo|Article)\s*(?:schema|markup|structured data)?', POST["content"], re.IGNORECASE)

# ======== OUTPUT ========
print("=" * 70)
print(f"SEO AUDIT REPORT: {POST['title']}")
print(f"Slug: {POST['slug']}")
print(f"Date: {POST['date']} | Author: {POST['author']}")
print(f"Tags: {', '.join(POST['tags'])}")
print("=" * 70)

# 1. Basic Metrics
print("\n📐 BASIC METRICS")
print(f"  Word Count: {word_count}")
print(f"  Excerpt Length: {len(POST['excerpt'])} chars")
print(f"  Internal Links: {len(internal_links_analysis)}")
print(f"  External Links: {len(external_links_analysis)}")

# 2. TF-IDF Top Keywords
print("\n🔤 TF-IDF TOP KEYWORDS")
for word, count in tf_sorted[:20]:
    tf_score = count / total_terms
    print(f"  {word}: count={count}, tf={tf_score:.4f}")

# 3. Entities
print("\n🏷️  EXTRACTED ENTITIES")
for cat, items in entities.items():
    if items:
        print(f"  {cat}: {', '.join(items)}")

# 4. Pillar-Cluster
print("\n🏛️  PILLAR-CLUSTER ANALYSIS")
if pillar_found:
    print(f"  ✅ Pillar-cluster strategy detected:")
    for kw in pillar_found:
        print(f"     - {kw}")
else:
    print("  ⚠️  No explicit pillar-cluster terminology found in post")
print(f"  Note: Post describes using pillar pages + supporting articles for the client's strategy")

# 5. AEO/GEO
print("\n🤖 AEO/GEO ANALYSIS")
geo_found_list = [kw for kw in geo_keywords if kw.lower() in POST["content"].lower()]
print(f"  AEO/GEO signals found: {len(geo_found_list)}/16")
for kw in geo_keywords:
    found = "✅" if kw.lower() in POST["content"].lower() else "❌"
    print(f"  {found} '{kw}'")

# 6. Internal Links Detail
print("\n🔗 INTERNAL LINKS")
if internal_links_analysis:
    for link in internal_links_analysis:
        print(f"  [{link['text']}]({link['url']})")
else:
    print("  None found")

print("\n🔗 EXTERNAL LINKS")
if external_links_analysis:
    for link in external_links_analysis:
        print(f"  [{link['text']}]({link['url']})")
else:
    print("  None found")

# 7. Schema
print("\n📋 SCHEMA ANALYSIS")
schema_mentions_count = len(set(schema_mentions))
print(f"  Schema/structured data mentions: {schema_mentions_count}")
if schema_mentions:
    print(f"  Mentioned terms: {', '.join(set(schema_mentions))}")
if schema_types:
    print(f"  Schema types referenced: {', '.join(set(schema_types))}")
else:
    print("  No specific schema types named in content")

# 8. Content Quality
print("\n⭐ CONTENT QUALITY CHECKS")
# Check headings
headings = re.findall(r'^##+\s+(.+)', POST["content"], re.MULTILINE)
print(f"  Headings (H2+): {len(headings)}")
for h in headings:
    print(f"     - {h.strip()}")

# Bengali presence
bengali = re.findall(r'[\u0980-\u09FF]+', POST["content"])
print(f"  Bengali text present: {'✅' if bengali else '❌'} ({len(bengali)} chars)")

# CTA presence
ctas = [t for t in ["Looking for the SEO expert", "SEO services", "Visit kanokmiah.com.bd", "contact"] if t.lower() in POST["content"].lower()]
print(f"  CTAs/Sign-offs: {len(ctas)} found")

# 9. Strengths & Weaknesses
print("\n💡 STRENGTHS")
print("  + Clear problem-solution-result narrative structure")
print("  + Specific, quantifiable metrics (15,440%, 14.2% CTR, 4.2s->1.8s)")
print("  + Internal links to relevant services (on-page SEO, technical SEO)")
print("  + Links to related case study (SMMGen) for cross-linking")
print("  + Mobile traffic share mentioned as key metric (75%+)")
print("  + Bengali text present for local audience")
print("  + Four-phase strategy clearly articulated")

print("\n⚠️  WEAKNESSES / IMPROVEMENTS")
print("  - No FAQ section (missed AEO opportunity)")
print("  - No explicit schema type references in content (FAQ, Article, etc.)")
print("  - Bengali section seems disconnected from main content (generic translation)")
print("  - 'Looking for the SEO expert in Dhaka' repeated awkwardly at end")
print("  - No author bio / EEAT credentials inline")
print("  - No conclusion that ties back to the reader's business")
print("  - Thin content after main case study (Bengali + signature lines feel padded)")

print("\n" + "=" * 70)
print("END OF REPORT")
