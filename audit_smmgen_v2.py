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

# Find the smmgen-seo-case-study post start and end
start_marker = 'slug: "smmgen-seo-case-study"'
start_idx = js_content.find(start_marker)
if start_idx == -1:
    raise ValueError("Could not find smmgen-seo-case-study in data.js")

# From start_idx, find the content field: "content: `"
content_start_marker = "content: `\n"
content_start = js_content.find(content_start_marker, start_idx)
if content_start == -1:
    content_start = js_content.find("content: `", start_idx)
    
content_start += len(content_start_marker) if js_content.find(content_start_marker, start_idx) != -1 else len("content: `")
# content_start now points to the first char after the opening backtick

# Find the closing backtick + comma pattern
content_end = js_content.find("`,\n", content_start)
if content_end == -1:
    # Try just backtick comma
    content_end = js_content.find("`,", content_start)
if content_end == -1:
    content_end = js_content.find("`\n", content_start)

content = js_content[content_start:content_end]

# Extract fields from before the content
pre_content = js_content[start_idx:content_start - len("content: `\n")]

def extract_field(name, text):
    m = re.search(rf'{name}:\s*"([^"]*)"', text)
    return m.group(1) if m else ""

def extract_tags(text):
    m = re.search(r'tags:\s*\[([^\]]+)\]', text)
    if m:
        tags_str = m.group(1)
        return [t.strip().strip('"').strip("'") for t in tags_str.split(",")]
    return []

slug = "smmgen-seo-case-study"
title = extract_field("title", pre_content)
date = extract_field("date", pre_content)
author = extract_field("author", pre_content)
excerpt = extract_field("excerpt", pre_content)
tags = extract_tags(pre_content)

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

# Calculate TF-IDF
default_idf_docs = 100
# Simulate corpus - common SEO/SMM terms get lower IDF
corpus_sim = {}
for w in words:
    if w in ['smm', 'seo', 'panel', 'organic', 'content', 'traffic', 'google', 'search', 'keywords', 'page', 'site', 'service', 'services', 'business', 'marketing', 'social', 'media', 'competitive', 'growth', 'result', 'results', 'monthly', 'clicks', 'ranking', 'competitors', 'technical', 'mobile', 'optimization']:
        corpus_sim[w] = 3  # very common in this domain
    elif w in ['strategy', 'market', 'experience', 'expert', 'buyer', 'industry', 'platform', 'online', 'website', 'build', 'increase', 'improved', 'implemented', 'created', 'optimized', 'phase']:
        corpus_sim[w] = 8  # moderately common
    else:
        corpus_sim[w] = default_idf_docs  # less common = higher IDF

print(f"\nTop 20 terms by TF-IDF score:")
tfidf_scores = {}
for word, count in word_freq.most_common(80):
    tf = count / total_words
    doc_freq = corpus_sim.get(word, default_idf_docs)
    idf = log((default_idf_docs + 1) / (doc_freq + 1)) + 1
    tfidf = tf * idf
    tfidf_scores[word] = tfidf

for word, score in sorted(tfidf_scores.items(), key=lambda x: -x[1])[:20]:
    print(f"  {word:<25s}  count={word_freq[word]:<5}  TF={word_freq[word]/total_words:.4f}  IDF={log((default_idf_docs+1)/(corpus_sim.get(word,default_idf_docs)+1))+1:.4f}  TF-IDF={score:.4f}")

# ============================================================
# CHECK 2: Entities (Named Entity Recognition simulation)
# ============================================================
print("\n" + "=" * 80)
print("CHECK 2: ENTITIES")
print("=" * 80)

# Extract entities via pattern matching
org_pattern = re.findall(r'\b(SMMGen|SMM|Instagram|YouTube|Facebook|TikTok|Redis|Google|MoreThanPanel)\b', content)
loc_pattern = re.findall(r'\b(Dhaka|Bangladesh)\b', content)
person_pattern = re.findall(r'\b(Kanok Miah)\b', content)
tech_terms_extracted = re.findall(r'\b(Core Web Vitals|FAQ|Product Schema|API|CDN|Cloudflare|LCP|schema markup|structured data|mobile-responsive|Redis caching|SERP|SEO|CTR|organic|hreflang)\b', content, re.IGNORECASE)
metric_pattern = re.findall(r'\b(\d[\d,]*)\s*(?:monthly|organic|clicks|impressions|keywords|pages|%|increase|growth|seconds?)\b', content, re.IGNORECASE)

print(f"\nOrganizations/Brands: {dict(Counter(org_pattern).most_common())}")
print(f"Locations: {dict(Counter(loc_pattern).most_common())}")
print(f"People: {dict(Counter(person_pattern).most_common())}")
print(f"Technical Terms (top): {dict(Counter([t.lower() for t in tech_terms_extracted]).most_common(15))}")

all_orgs = set(org_pattern)
all_locs = set(loc_pattern)
all_tech = set(t.lower() for t in tech_terms_extracted)
entity_density = len(all_orgs) + len(all_locs) + len(all_tech)

print(f"\nTotal unique named entities: {entity_density}")
print(f"  Organizations: {all_orgs}")
print(f"  Locations: {all_locs}")
print(f"  Tech/SEO terms: {all_tech}")

# ============================================================
# CHECK 3: Pillar-Cluster Structure
# ============================================================
print("\n" + "=" * 80)
print("CHECK 3: PILLAR-CLUSTER ANALYSIS")
print("=" * 80)

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
# Remove self-reference
other_links_to_this = [l for l in other_links_to_this if l != title.split(":")[0].strip()]
print(f"\nInternal links TO this post from OTHER posts: {len(other_links_to_this)}")
for text in other_links_to_this:
    print(f"  [{text}](/blog/{slug})")

service_links = [u for _, u in internal_links_out if '/services/' in u]
blog_links = [u for _, u in internal_links_out if '/blog/' in u]

pillar_assessment = {
    "post_type": "Case Study (cluster/supporting content)",
    "depth": "Medium-depth case study with specific metrics (27,900 clicks, 500+ keywords)",
    "pillar_candidate": False,
    "cluster_role": "Supporting authority content for SMM/SEO services topic cluster",
    "linking_to_services": len(service_links) > 0,
    "linking_to_other_blog_posts": len(blog_links) > 0,
    "incoming_crosslinks": len(other_links_to_this),
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
has_faq = bool(re.search(r'(FAQ|Frequently Asked)', content, re.IGNORECASE))
has_qa_format = bool(re.search(r'(###\s+(How|What|Why|Can|Do|Does|Is|Are|Should)\b.*\?)', content))

# Check for schema markup references
schema_refs = re.findall(r'(schema|structured data|markup|rich results)', content.lower())
has_schema_refs = len(schema_refs) > 0

# Check for conversational content
question_count = len(re.findall(r'[A-Z][^.]*\?', content))
direct_statements = len(re.findall(r'(?:^|\n)([A-Z][A-Za-z ,\d]{10,80}\.)', content))

# List/bullet point analysis
bullet_items = re.findall(r'^- \*\*([^*]+)\*\*', content, re.MULTILINE)
dash_items = re.findall(r'^- ([^-*\n]+)', content, re.MULTILINE)
total_structured_points = len(bullet_items) + len(dash_items)

# Entity richness for AI models
entity_richness = entity_density

print(f"Has FAQ section: {has_faq}")
print(f"Has Q&A format (questions as headings): {has_qa_format}")
print(f"Schema/structured data references: {has_schema_refs}")
print(f"Question-format queries addressed: {question_count}")
print(f"Bold list items (structured takeaways): {len(bullet_items)}")
print(f"Total bullet/dash list items: {total_structured_points}")
print(f"Unique entity types for AI extraction: {entity_richness}")
print(f"Direct declarative statements: {direct_statements}")

geo_score = 0
if has_faq: geo_score += 2
if has_qa_format: geo_score += 2
if has_schema_refs: geo_score += 2
if question_count >= 2: geo_score += 1
if total_structured_points >= 5: geo_score += 1
if entity_richness >= 8: geo_score += 2
elif entity_richness >= 5: geo_score += 1

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

all_internal_links = [url for text, url in internal_links_out]
outbound_external = re.findall(r'\(https?://[^)]+\)', content)
# Filter out the smmgen.com external link to the client
external_urls = [u for u in outbound_external if 'kanokmiah.com.bd' not in u]
own_site_urls = [u for u in outbound_external if 'kanokmiah.com.bd' in u]

print(f"Total internal links in post: {len(all_internal_links)}")
print(f"External outbound links: {len(external_urls)}")
print(f"Links to own site (kanokmiah.com.bd): {len(own_site_urls)}")

print(f"\nAll internal URLs:")
for url in all_internal_links:
    print(f"  {url}")

print(f"\nAll external URLs:")
for url in external_urls:
    print(f"  {url}")

# Check link diversity
service_links = [u for u in all_internal_links if '/services/' in u]
blog_links = [u for u in all_internal_links if '/blog/' in u]

print(f"\nLink Distribution:")
print(f"  Service pages: {len(service_links)}")
print(f"  Blog posts:    {len(blog_links)}")
print(f"  Other:         {len(all_internal_links) - len(service_links) - len(blog_links)}")

# Check anchor text quality
anchor_texts = [text for text, url in internal_links_out]
print(f"\nAnchor texts: {anchor_texts}")

# ============================================================
# CHECK 6: Schema / Structured Data Analysis
# ============================================================
print("\n" + "=" * 80)
print("CHECK 6: SCHEMA / STRUCTURED DATA ANALYSIS")
print("=" * 80)

# Look for schema markup mentions
schema_mentions = re.findall(r'(schema|structured data|markup|rich snippet|FAQ schema|Product schema|HowTo schema|Organization schema|Breadcrumb)', content.lower())
print(f"References to schema markup in content: {len(schema_mentions)}")
for ref in set(schema_mentions):
    print(f"  - {ref}")

# Check if the post itself mentions implementing schema
has_implemented_schema = any(phrase in content.lower() for phrase in [
    'faq schema', 'product schema', 'schema markup', 'structured data',
    'faq plus product schema markup'
])
print(f"\nPost mentions active schema implementation: {has_implemented_schema}")

# Check site-wide schema approach
schema_code = re.findall(r'structuredData|json-ld|application/ld\+json|"@type"|"@context"', js_content)
print(f"Schema/JSON-LD references in data.js (site-wide): {len(schema_code)}")

# Content-based schema assessment
has_faq_section = bool(re.search(r'FAQ', content))
has_howto = bool(re.search(r'(how it works|step[- ]by[- ]step|process|method)', content.lower()))
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
if has_schema_refs: schema_score += 1
if has_headline: schema_score += 1
print(f"\nSchema Optimization Score: {schema_score}/9")

# ============================================================
# OVERALL ASSESSMENT
# ============================================================
print("\n" + "=" * 80)
print("OVERALL SCORECARD")
print("=" * 80)

key_terms = ['smm', 'seo', 'organic', 'traffic', 'clicks', 'keywords', 'panel', 'growth', 'results']
key_terms_found = [t for t in key_terms if t in words]

checks = {
    "TF-IDF / Keyword Coverage": {
        "total_words": total_words,
        "unique_words": len(word_freq),
        "top_keywords": [w for w, _ in word_freq.most_common(10)],
        "key_terms_covered": len(key_terms_found),
        "verdict": "PASS" if total_words > 200 and len(key_terms_found) >= 5 else "NEEDS WORK"
    },
    "Entities": {
        "orgs_found": len(all_orgs),
        "locations_found": len(all_locs),
        "tech_terms_found": len(all_tech),
        "entity_richness_score": entity_density,
        "verdict": "PASS" if entity_density >= 5 else "NEEDS WORK"
    },
    "Pillar-Cluster": {
        "type": "Cluster / Case Study",
        "outgoing_internal_links": len(internal_links_out),
        "incoming_crosslinks": len(other_links_to_this),
        "links_to_services": service_links if service_links else "None",
        "links_to_other_posts": blog_links if blog_links else "None",
        "verdict": "PASS" if len(internal_links_out) >= 2 else "NEEDS WORK"
    },
    "AEO/GEO": {
        "score": geo_score,
        "max": 10,
        "has_faq": has_faq,
        "has_qa_format": has_qa_format,
        "structured_points": total_structured_points,
        "verdict": "PASS" if geo_score >= 5 else "NEEDS WORK"
    },
    "Internal Links": {
        "total_internal": len(all_internal_links),
        "total_external": len(external_urls),
        "links_to_own_site": len(own_site_urls),
        "distinct_pages_linked": len(set(all_internal_links)),
        "verdict": "PASS" if len(all_internal_links) >= 2 else "NEEDS WORK"
    },
    "Schema": {
        "score": schema_score,
        "max": 9,
        "schema_mentions": len(schema_mentions),
        "faq_section": has_faq_section,
        "article_schema_ready": has_author and has_date and has_headline,
        "verdict": "PASS" if schema_score >= 4 else "NEEDS WORK"
    }
}

for check_name, data in checks.items():
    verdict = data.get("verdict", "NEEDS WORK")
    print(f"\n{check_name}: [{verdict}]")
    for k, v in data.items():
        if k != "verdict":
            print(f"  {k}: {v}")

pass_count = sum(1 for c in checks.values() if c.get('verdict') == 'PASS')
total_checks_num = len(checks)
print(f"\n{'=' * 80}")
print(f"RESULT: {pass_count}/{total_checks_num} checks PASSED")
print(f"{'=' * 80}")

# Recommendations
print("\nRECOMMENDATIONS:")
recs = []
if total_words < 300:
    recs.append("Expand content (currently <300 meaningful words after stopword removal)")
if len(key_terms_found) < 5:
    recs.append(f"Add more primary keywords. Found {len(key_terms_found)}/{len(key_terms)} key SEO terms")
if entity_density < 5:
    recs.append("Add more named entities (brands, locations, technical terms) for AI search")
if len(internal_links_out) < 2:
    recs.append("Add more internal links to related services, blog posts, and industry pages")
if geo_score < 5:
    recs.append("Improve AEO/GEO: add FAQ section with natural language Q&A, more structured data, entity-rich content")
if schema_score < 4:
    recs.append("Implement Article schema, FAQ schema, and Product schema markup")
if len(other_links_to_this) < 2:
    recs.append("Add more cross-links from other relevant blog posts to this case study")
if not has_faq:
    recs.append("Add an FAQ section at the end to capture voice/answer engine queries")

for i, rec in enumerate(recs, 1):
    print(f"  {i}. {rec}")

if not recs:
    print("  No major issues found - post is well-optimized.")
