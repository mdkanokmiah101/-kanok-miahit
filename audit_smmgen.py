#!/usr/bin/env python3
"""
Comprehensive SEO Content Audit for 'SMMGen SEO Case Study' blog post.
Checks: TF-IDF, Entities, Pillar-Cluster, AEO/GEO, Internal Links, Schema
"""
import re
import json
from collections import Counter
from math import log

# --- Load the post content ---
with open("/root/kanok-miahit/src/app/blog/data.js", "r") as f:
    js_content = f.read()

# Extract the smmgen-seo-case-study post
pattern = r"slug: \"smmgen-seo-case-study\",\s*\n(.*?)\n  \},"
match = re.search(pattern, js_content, re.DOTALL)
if not match:
    raise ValueError("Could not find smmgen-seo-case-study in data.js")

post_block = match.group(1)

# Extract fields
def extract_field(name, block):
    m = re.search(rf'{name}:\s*"([^"]*)"', block)
    return m.group(1) if m else ""

def extract_tags(block):
    m = re.search(r'tags:\s*\[([^\]]+)\]', block)
    if m:
        tags_str = m.group(1)
        return [t.strip().strip('"').strip("'") for t in tags_str.split(",")]
    return []

def extract_content(block):
    m = re.search(r'content: `\n(.*?)\n\s*`,', block, re.DOTALL)
    if m:
        return m.group(1)
    return ""

slug = "smmgen-seo-case-study"
title = extract_field("title", post_block)
date = extract_field("date", post_block)
author = extract_field("author", post_block)
excerpt = extract_field("excerpt", post_block)
tags = extract_tags(post_block)
content = extract_content(post_block)

print("=" * 80)
print("BLOG POST DATA")
print("=" * 80)
print(f"Slug:    {slug}")
print(f"Title:   {title}")
print(f"Date:    {date}")
print(f"Author:  {author}")
print(f"Tags:    {tags}")
print(f"Excerpt: {excerpt[:80]}...")
print(f"Content length: {len(content)} chars, ~{len(content.split())} words")
print()

# ============================================================
# CHECK 1: TF-IDF Analysis (keyword significance)
# ============================================================
print("=" * 80)
print("CHECK 1: TF-IDF / KEYWORD ANALYSIS")
print("=" * 80)

# Tokenize content
tokens = re.findall(r'\b[a-zA-Z][a-zA-Z-]+\b', content.lower())
stop_words = {
    'the','a','an','and','or','but','in','on','at','to','for','of','by','with',
    'from','as','is','was','are','were','be','been','being','have','has','had',
    'do','does','did','will','would','could','should','may','might','can',
    'it','its','this','that','these','those','we','he','she','they','you',
    'i','my','me','our','us','your','his','her','their','them','not','no',
    'nor','so','if','than','then','also','just','but','very','all','each',
    'every','both','few','more','most','some','any','such','only','own',
    'same','too','about','into','over','after','before','between','under',
    'above','below','up','down','out','off','through','during','without',
    'how','what','when','where','which','who','whom','why','because','while',
    'since','until','here','there','--','-','&'
}
words = [w for w in tokens if w not in stop_words and len(w) > 2]
word_freq = Counter(words)
total_words = len(words)

print(f"\nTotal words (after stopword removal): {total_words}")
print(f"Unique words: {len(word_freq)}")
print(f"\nTop 30 terms by frequency:")
for word, count in word_freq.most_common(30):
    tf = count / total_words
    print(f"  {word:<25s}  count={count:<5}  TF={tf:.4f}")

# TF-IDF against a simulated background corpus (SMM/SEO terms get higher IDF)
# Using a simple IDF corpus simulation
corpus_sim = {
    'smm': 3, 'seo': 3, 'organic': 5, 'panel': 3, 'social': 5,
    'media': 5, 'marketing': 5, 'traffic': 5, 'keywords': 5, 'ranking': 5,
    'clicks': 5, 'google': 5, 'content': 10, 'technical': 8, 'mobile': 8,
    'competitors': 8, 'growth': 5, 'case': 8, 'study': 8, 'dhaka': 10,
    'bangladesh': 10, 'service': 10, 'services': 10,
}
# Assign high IDF to common web words
default_idf_docs = 100
for w in words:
    if w not in corpus_sim:
        corpus_sim[w] = default_idf_docs // 2  # moderately common

print(f"\nTop 20 terms by TF-IDF score:")
tfidf_scores = {}
for word, count in word_freq.most_common(60):
    tf = count / total_words
    idf = log((default_idf_docs + 1) / (corpus_sim.get(word, default_idf_docs // 2) + 1)) + 1
    tfidf = tf * idf
    tfidf_scores[word] = tfidf

for word, score in sorted(tfidf_scores.items(), key=lambda x: -x[1])[:20]:
    print(f"  {word:<25s}  TF={word_freq[word]/total_words:.4f}  TF-IDF={score:.4f}")

# ============================================================
# CHECK 2: Entities (Named Entity Recognition simulation)
# ============================================================
print("\n" + "=" * 80)
print("CHECK 2: ENTITIES")
print("=" * 80)

# Extract entities via pattern matching
org_pattern = re.findall(r'\b(SMMGen|SMM|Instagram|YouTube|Facebook|TikTok|Redis|Google)\b', content)
loc_pattern = re.findall(r'\b(Dhaka|Bangladesh)\b', content)
person_pattern = re.findall(r'\b(Kanok Miah)\b', content)
metric_pattern = re.findall(r'(\d[\d,]*[\d]*)\s*(?:monthly|organic|clicks|impressions|keywords|pages|%|increase|growth)', content)
tech_terms = re.findall(r'\b(Core Web Vitals|FAQ|Product schema|API|CDN|Cloudflare|LCP|schema markup|structured data|mobile-responsive|Redis caching|SERP)\b', content)

print(f"\nOrganizations/Brands: {Counter(org_pattern).most_common()}")
print(f"Locations: {Counter(loc_pattern).most_common()}")
print(f"People: {Counter(person_pattern).most_common()}")
print(f"Technical Terms: {Counter(tech_terms).most_common()}")

# Extract all entities grouped
all_entities = {
    "ORGANIZATIONS": list(set(org_pattern)),
    "LOCATIONS": list(set(loc_pattern)),
    "PERSON": list(set(person_pattern)),
    "TECH_TERMS": list(set(tech_terms)),
    "METRICS": list(set(re.findall(r'(organic clicks|impressions|ranking keywords|indexed pages|domain authority|Core Web Vitals|CTR|monthly|ad spend)', content.lower())))
}

for cat, ents in all_entities.items():
    print(f"\n  {cat}: {ents}")

# ============================================================
# CHECK 3: Pillar-Cluster Structure
# ============================================================
print("\n" + "=" * 80)
print("CHECK 3: PILLAR-CLUSTER ANALYSIS")
print("=" * 80)

# Check if this is a pillar (comprehensive guide) or cluster (specific subtopic)
# This is a case study - narrow focus
headings = re.findall(r'^#{2,4}\s+(.+)$', content, re.MULTILINE)
print(f"\nHeadings found ({len(headings)}):")
for h in headings:
    print(f"  - {h}")

# Check for internal links to/from other content
internal_links_out = re.findall(r'\[([^\]]+)\]\((/[^)]+)\)', content)
print(f"\nInternal links OUT from this post: {len(internal_links_out)}")
for text, url in internal_links_out:
    print(f"  [{text}]({url})")

# Check if other posts link to this one
other_links_to_this = re.findall(r'\[([^\]]+)\]\(/blog/' + slug + r'\)', js_content)
print(f"\nInternal links TO this post from other posts: {len(other_links_to_this)}")
for text in other_links_to_this:
    print(f"  [{text}](/blog/{slug})")

pillar_assessment = {
    "post_type": "Case Study (cluster/supporting content)",
    "depth": "Medium-depth case study with specific metrics",
    "pillar_candidate": False,
    "cluster_role": "Supporting authority content for SMM/SEO services topic cluster",
    "linking_to_pillars": any('/services/' in url for _, url in internal_links_out),
    "linking_to_related_clusters": any('/blog/' in url for _, url in internal_links_out),
}
print(f"\nPillar-Cluster Assessment:")
for k, v in pillar_assessment.items():
    print(f"  {k}: {v}")

# ============================================================
# CHECK 4: AEO/GEO (Answer Engine Optimization / Generative Engine Optimization)
# ============================================================
print("\n" + "=" * 80)
print("CHECK 4: AEO/GEO ANALYSIS")
print("=" * 80)

# Check for FAQ/Q&A format
faq_pattern = re.findall(r'(?:FAQ|Frequently Asked|Question|Q:|\?\n)', content)
has_structured_faq = len(faq_pattern) > 0

# Check for schema markup references
schema_refs = re.findall(r'(schema|structured data|FAQ schema|Product schema|markup)', content.lower())
has_schema_refs = len(schema_refs) > 0

# Check for conversational/voice-friendly content
question_format = len(re.findall(r'\b(how|what|why|when|where|which|can|do|does|is|are)\b.*\?', content.lower()))
list_format = len(re.findall(r'^- \*\*', content, re.MULTILINE))  # bold list items
bullet_points = len(re.findall(r'^- ', content, re.MULTILINE))

# Entity richness for AI models
entity_density = len(set(org_pattern)) + len(set(loc_pattern)) + len(set(tech_terms))

# Check for direct answer format - concise answers followed by details
direct_answers = re.findall(r'(?:^|\n)([A-Z][^.]{10,80}\.)', content)

print(f"Has FAQ / Q&A format: {has_structured_faq}")
print(f"Schema/structured data references: {has_schema_refs}")
print(f"Question-format queries addressed: {question_format}")
print(f"Bold list items (structured takeaways): {list_format}")
print(f"Total bullet points: {bullet_points}")
print(f"Unique entity types for AI extraction: {entity_density}")
print(f"Direct declarative statements (candidate answers): {len(direct_answers)}")

geo_score = 0
if has_structured_faq: geo_score += 2
if has_schema_refs: geo_score += 3
if question_format > 3: geo_score += 2
if entity_density > 5: geo_score += 2
if list_format > 2: geo_score += 1
if bullet_points > 5: geo_score += 1

print(f"\nAEO/GEO Readiness Score: {geo_score}/10")
if geo_score >= 7:
    print("  Rating: GOOD - Strongly optimized for AI search engines")
elif geo_score >= 4:
    print("  Rating: MODERATE - Some optimization, room for improvement")
else:
    print("  Rating: NEEDS WORK - Consider adding FAQ section, more schema, entity-rich content")

# ============================================================
# CHECK 5: Internal Links Analysis
# ============================================================
print("\n" + "=" * 80)
print("CHECK 5: INTERNAL LINKS ANALYSIS")
print("=" * 80)

all_internal_links = re.findall(r'\((/[^)]+)\)', content)
outbound_external = re.findall(r'\(https?://[^)]+\)', content)
anchor_texts = re.findall(r'\[([^\]]+)\]', content)

print(f"Total internal links in post: {len(all_internal_links)}")
print(f"External outbound links: {len(outbound_external)}")
print(f"\nAll internal URLs:")
for url in all_internal_links:
    print(f"  {url}")

print(f"\nAll external URLs:")
for url in outbound_external:
    print(f"  {url}")

# Check link diversity
service_links = [u for u in all_internal_links if '/services/' in u]
blog_links = [u for u in all_internal_links if '/blog/' in u]
industry_links = [u for u in all_internal_links if '/industries/' in u]
root_links = [u for u in all_internal_links if u in ['/', '/about', '/contact']]

print(f"\nLink Distribution:")
print(f"  Service pages: {len(service_links)}")
print(f"  Blog posts:    {len(blog_links)}")
print(f"  Industry pages:{len(industry_links)}")
print(f"  Root/about:    {len(root_links)}")
print(f"  Other:         {len(all_internal_links) - len(service_links) - len(blog_links) - len(industry_links) - len(root_links)}")

# Check anchor text quality
anchor_texts_filtered = [a for a in anchor_texts if len(a) > 3 and a not in ['technical SEO', 'SMMGen case study']]
print(f"\nAnchor texts used: {anchor_texts_filtered}")

# ============================================================
# CHECK 6: Schema / Structured Data Analysis
# ============================================================
print("\n" + "=" * 80)
print("CHECK 6: SCHEMA / STRUCTURED DATA ANALYSIS")
print("=" * 80)

# Look for schema markup mentions and actual schema in the content
schema_mentions = re.findall(r'(?:schema|structured data|markup|rich snippet|FAQ schema|Product schema|HowTo schema|Organization schema|Breadcrumb)', content.lower())
print(f"References to schema markup in content: {len(schema_mentions)}")
for ref in set(schema_mentions):
    print(f"  - {ref}")

# Check if the post itself mentions implementing schema
has_implemented_schema = any(phrase in content.lower() for phrase in [
    'faq schema', 'product schema', 'schema markup', 'structured data',
    'faq plus product schema markup'
])
print(f"\nPost mentions active schema implementation: {has_implemented_schema}")

# Check site-wide schema approach (from data.js context)
# Search for schema-related code in the project
schema_code = re.findall(r'structuredData|json-ld|application/ld|"@type"', js_content)
print(f"Schema/JSON-LD references in data.js (site-wide): {len(schema_code)}")

# Content-based schema assessment
# Check for FAQ section
has_faq_section = 'FAQ' in content or 'Frequently Asked' in content
# Check for HowTo section
has_howto = 'how it works' in content.lower() or 'step' in content.lower()
# Check for Article/BlogPosting schema compatibility
has_author = author == "Kanok Miah"
has_date = bool(date)
has_headline = bool(title)

print(f"\nContent Schema Readiness:")
print(f"  FAQ section present: {has_faq_section}")
print(f"  HowTo structure: {has_howto}")
print(f"  Author available: {has_author}")
print(f"  Date available: {has_date}")
print(f"  Headline/title: {has_headline}")
print(f"  Article schema compatible: {has_author and has_date and has_headline}")

schema_score = 0
if has_faq_section: schema_score += 2
if has_howto: schema_score += 1
if has_implemented_schema: schema_score += 2
if has_author: schema_score += 1
if has_date: schema_score += 1
if has_schema_refs: schema_score += 2
print(f"\nSchema Optimization Score: {schema_score}/9")

# ============================================================
# OVERALL ASSESSMENT
# ============================================================
print("\n" + "=" * 80)
print("OVERALL SCORECARD")
print("=" * 80)

checks = {
    "TF-IDF / Keyword Coverage": {
        "total_words": total_words,
        "unique_words": len(word_freq),
        "key_terms_present": all(t.lower() in words for t in ['smm', 'seo', 'organic', 'traffic', 'clicks', 'keywords']),
        "verdict": "PASS" if total_words > 300 and len(word_freq) > 100 else "NEEDS WORK"
    },
    "Entities": {
        "orgs_found": len(set(org_pattern)),
        "locations_found": len(set(loc_pattern)),
        "tech_terms_found": len(set(tech_terms)),
        "entity_richness": entity_density,
        "verdict": "PASS" if entity_density >= 5 else "NEEDS WORK"
    },
    "Pillar-Cluster": {
        "type": "Cluster / Supporting Content",
        "internal_outgoing": len(internal_links_out),
        "incoming_links": len(other_links_to_this),
        "links_to_services": len(service_links),
        "verdict": "PASS" if len(internal_links_out) >= 3 else "NEEDS WORK"
    },
    "AEO/GEO": {
        "score": geo_score,
        "max_score": 10,
        "faq_present": has_structured_faq,
        "bullet_points": bullet_points,
        "verdict": "PASS" if geo_score >= 5 else "NEEDS WORK"
    },
    "Internal Links": {
        "total": len(all_internal_links),
        "external": len(outbound_external),
        "distinct_pages": len(set(all_internal_links)),
        "verdict": "PASS" if len(all_internal_links) >= 2 else "NEEDS WORK"
    },
    "Schema": {
        "score": schema_score,
        "max_score": 9,
        "schema_mentions": len(schema_mentions),
        "faq_section": has_faq_section,
        "verdict": "PASS" if schema_score >= 4 else "NEEDS WORK"
    }
}

for check_name, data in checks.items():
    verdict = data.pop("verdict")
    print(f"\n{check_name}: [{verdict}]")
    for k, v in data.items():
        print(f"  {k}: {v}")

pass_count = sum(1 for c in checks.values() if c.get('verdict', 'NEEDS WORK') == 'PASS')
total_checks = len(checks)
print(f"\n{'=' * 80}")
print(f"RESULT: {pass_count}/{total_checks} checks PASSED")
print(f"{'=' * 80}")

# Recommendations
print("\nRECOMMENDATIONS:")
recs = []
if total_words < 500:
    recs.append("Expand content to 500+ words for better topical coverage")
if entity_density < 5:
    recs.append("Add more named entities (brands, locations, technical terms) for AI search")
if len(internal_links_out) < 3:
    recs.append("Add more internal links to related services, blog posts, and industry pages")
if geo_score < 5:
    recs.append("Improve AEO/GEO: add FAQ section, more structured bullet points, entity-rich content")
if schema_score < 4:
    recs.append("Implement FAQ schema and Article schema markup")
if len(other_links_to_this) < 2:
    recs.append("Add more cross-links from other relevant blog posts to this case study")

for i, rec in enumerate(recs, 1):
    print(f"  {i}. {rec}")

if not recs:
    print("  No major issues found - post is well-optimized.")
