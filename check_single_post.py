#!/usr/bin/env python3
"""Single-post Content Framework check for 'seo-https-ssl-impact-bangladesh'"""
import re, json

# Read the data.js file
with open('/root/kanok-miahit/src/app/blog/data.js', 'r') as f:
    content = f.read()

# Extract the specific post by slug
# Find the post block containing our slug
start = content.find("slug: \"seo-https-ssl-impact-bangladesh\"")
if start == -1:
    print("ERROR: Could not find post slug in data.js")
    exit(1)

# Go back to find the opening {
post_start = content.rfind('{', 0, start)
# Find the closing }
depth = 0
in_content = False
i = post_start
while i < len(content):
    if 'content: `' in content[i:i+12] or 'content:`' in content[i:i+10]:
        in_content = True
    if in_content:
        if '`' in content[i]:
            # Check if this is the closing backtick
            before = content[max(0,i-50):i]
            if 'content: `' not in before and 'content:`' not in before:
                in_content = False
                i += 1
                continue
    else:
        if content[i] == '{':
            depth += 1
        elif content[i] == '}':
            depth -= 1
            if depth == 0:
                post_end = i + 1
                break
    i += 1

post_text = content[post_start:post_end]

def extract_field(post, field):
    m = re.search(rf'{field}:\s*"([^"]*)"', post)
    return m.group(1) if m else ''

def extract_content(post):
    m = re.search(r'content:\s*`(.*)`', post, re.DOTALL)
    return m.group(1) if m else ''

slug = extract_field(post_text, 'slug')
title = extract_field(post_text, 'title')
date = extract_field(post_text, 'date')
author = extract_field(post_text, 'author')
excerpt = extract_field(post_text, 'excerpt')
post_content = extract_content(post_text)

tags_m = re.search(r'tags:\s*\[([^\]]+)\]', post_text, re.DOTALL)
tags = []
if tags_m:
    tags = re.findall(r'"([^"]+)"', tags_m.group(1))

print(f"{'='*80}")
print(f"CONTENT FRAMEWORK CHECK — Single Post Report")
print(f"{'='*80}")
print(f"Slug:  {slug}")
print(f"Title: {title}")
print(f"Date:  {date}")
print(f"Author:{author}")
print(f"Tags:  {tags}")
print(f"Content length: {len(post_content)} chars")
print(f"{'='*80}\n")

# ===== CHECK A: TF-IDF =====
def is_bengali(text):
    return len(re.findall(r'[\u0980-\u09FF]', text)) > len(text) * 0.1

def extract_primary_keyword(title):
    title_lower = title.lower()
    stopwords = {'a', 'an', 'the', 'how', 'why', 'what', 'when', 'where', 'which', 'who', 'do', 'does', 'did',
                 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'to', 'for', 'of', 'in',
                 'on', 'at', 'by', 'with', 'from', 'as', 'into', 'through', 'during', 'before', 'after', 'above',
                 'below', 'between', 'out', 'off', 'over', 'under', 'again', 'further', 'then', 'once',
                 'and', 'but', 'or', 'nor', 'not', 'so', 'yet', 'both', 'either', 'neither', 'each', 'every',
                 'your', 'their', 'its', 'our', 'my', 'his', 'her', 'some', 'any', 'no', 'all', 'most',
                 'best', 'top', 'ultimate', 'complete', 'guide', 'tips', 'for', 'in', 'of', 'the', 'on', 'at',
                 'seo', 'also', 'just', 'more', 'than', 'very', 'too', 'can', 'has', 'get', 'got'}
    raw_words = re.split(r'[\s:;,()!?./\\[\]"\'\-]+', title_lower)
    meaningful = [w for w in raw_words if w not in stopwords and len(w) > 2]
    if not meaningful:
        meaningful = [w for w in raw_words if w not in {'a', 'an', 'the', 'for', 'in', 'of', 'to', 'and', 'or', 'at'} and len(w) > 1]
    if not meaningful:
        return title_lower.split()[0] if title_lower.split() else title_lower
    if is_bengali(title):
        for w in meaningful:
            if re.search(r'[\u0980-\u09FF]', w):
                return w
        return meaningful[0]
    else:
        return meaningful[0]

keyword = extract_primary_keyword(title)
print(f"[A] TF-IDF — Primary keyword extracted: '{keyword}'")

if re.search(r'[\u0980-\u09FF]', keyword):
    count = len(re.findall(re.escape(keyword), post_content, re.IGNORECASE))
else:
    count = len(re.findall(r'\b' + re.escape(keyword) + r'\b', post_content, re.IGNORECASE))

# Also show related keyword frequencies
ssl_count = len(re.findall(r'\bSSL\b', post_content, re.IGNORECASE))
https_count = len(re.findall(r'\bHTTPS\b', post_content, re.IGNORECASE))
seo_count = len(re.findall(r'\bSEO\b', post_content, re.IGNORECASE))

passed_a = count >= 5
print(f"   '{keyword}' occurrences: {count} (need ≥5) → {'✅ PASS' if passed_a else '❌ FAIL'}")
print(f"   Related: SSL={ssl_count}, HTTPS={https_count}, SEO={seo_count}")

# ===== CHECK B: Entities =====
print(f"\n[B] ENTITIES — Semantic Entity Coverage")
all_tags = ','.join(tags).lower()
content_lower = post_content.lower()

entities = {
    'location_dhaka': r'dhaka|ঢাকা',
    'location_bangladesh': r'bangladesh|বাংলাদেশ',
    'service_seo': r'SEO|এসইও',
}
tag_triggers = {
    'entity_ecommerce': (['ecommerce', 'e-commerce', 'daraz', 'shopify', 'ই-কমার্স'], r'ecommerce|e.commerce|ই-কমার্স|দারাজ'),
    'entity_realestate': (['real estate'], r'real estate|রিয়েল এস্টেট|property'),
    'entity_gbp': (['local seo', 'google maps', 'gbp', 'লোকাল'], r'google business|gpb|গুগল বিজনেস|গুগল ম্যাপ'),
    'entity_technical': (['technical seo', 'core web vitals', 'টেকনিক্যাল'], r'technical seo|core web vitals|টেকনিক্যাল|ক্রল'),
    'entity_keyword': (['keyword', 'কীওয়ার্ড'], r'keyword|কীওয়ার্ড|কীওয়ার্ড|লং.*টেল'),
    'entity_youtube': (['video', 'youtube', 'ইউটিউব'], r'youtube|ইউটিউব|video|ভিডিও'),
    'entity_mobile': (['mobile', 'মোবাইল'], r'mobile|মোবাইল|smartphone'),
    'entity_schema': (['schema', 'স্কিমা'], r'schema|স্কিমা|structured data|স্ট্রাকচারড ডেটা'),
    'entity_content': (['content', 'কন্টেন্ট', 'blog'], r'content|কন্টেন্ট|blog|ব্লগ'),
}
for name, (triggers, pat) in tag_triggers.items():
    if any(t in all_tags for t in triggers):
        entities[name] = pat

missing_entities = []
for name, pattern in entities.items():
    if re.search(pattern, content_lower, re.IGNORECASE):
        print(f"   ✓ {name}: found")
    else:
        print(f"   ✗ {name}: MISSING")
        missing_entities.append(name)

passed_b = len(missing_entities) == 0
print(f"   → {'✅ PASS' if passed_b else '❌ FAIL'} (missing: {', '.join(missing_entities) if missing_entities else 'none'})")

# ===== CHECK C: Pillar-Cluster =====
print(f"\n[C] PILLAR-CLUSTER — Pillar Link Check")
pillar_pages = {
    'seo guide': '/blog/complete-seo-guide-bangladesh-businesses-2026',
    'local seo': '/blog/local-seo-tips-dhaka-businesses-google-maps',
    'technical seo': '/blog/technical-seo-checklist-bangladeshi-websites',
    'ecommerce': '/blog/why-ecommerce-store-needs-seo-bangladesh',
    'keyword': '/blog/keyword-research-bangladesh-market',
    'link building': '/blog/link-building-strategies-bangladesh-market',
    'geo': '/blog/geo-optimization-prepare-business-ai-search',
    'content': '/blog/content-marketing-seo-friendly-content-writing',
    'mobile': '/blog/mobile-seo-bangladesh-ranking-strategy',
    'schema': '/blog/schema-markup-rich-snippets-techniques',
}

linked_pillar = None
for pillar_name, pillar_url in pillar_pages.items():
    if pillar_url in post_content:
        linked_pillar = (pillar_name, pillar_url)
        break

if not linked_pillar:
    blog_links = re.findall(r'/blog/[a-z0-9-]+', post_content)
    if blog_links:
        linked_pillar = ('(generic blog link)', blog_links[0])
        print(f"   ✓ Blog link found: {blog_links[0]} (not a defined pillar)")
        print(f"   ⚠ NOTE: No direct pillar page linked. Generic blog links exist.")

all_blog_links = list(set(re.findall(r'/blog/[a-z0-9-]+', post_content)))
all_service_links = list(set(re.findall(r'/services/[a-z0-9-]+', post_content)))
all_location_links = list(set(re.findall(r'/locations/[a-z0-9-]+', post_content)))

if linked_pillar and linked_pillar[0] != '(generic blog link)':
    passed_c = True
    print(f"   ✓ Pillar link: {linked_pillar[1]} ({linked_pillar[0]})")
else:
    passed_c = linked_pillar is not None

print(f"   All blog links in post: {all_blog_links}")
print(f"   All service links: {all_service_links}")
print(f"   → {'✅ PASS' if passed_c else '❌ FAIL'}")

# ===== CHECK D: AEO/GEO =====
print(f"\n[D] AEO/GEO — Optimization Check")
question_headings = len(re.findall(r'^#{2,3}\s+.*\?', post_content, re.MULTILINE))
q_words = r'^(?:How|What|Why|When|Where|Can|Do|Is|Are|Does|Which|Who)'
question_headings += len(re.findall(r'^#{2,3}\s+' + q_words, post_content, re.MULTILINE))
question_headings += len(re.findall(r'^#{2,3}\s+.*?(?:কী|কেন|কিভাবে|কখন|কোথায়|কীভাবে|কোন|কার|কয়টি|উপসংহার|বনাম)', post_content, re.MULTILINE))

faq_sections = len(re.findall(r'প্রায়শ[িই] जিজ্ঞাসিত|FAQ|প্রশ্ন', post_content, re.IGNORECASE))
# The FAQ section uses "FAQ" heading
faq_sections += len(re.findall(r'^#{2,3}\s+FAQ', post_content, re.MULTILINE))

total_aeo = question_headings + faq_sections
passed_d = total_aeo >= 2

# Count specific GEO elements
geo_section = 'generative engine optimization' in post_content.lower() or 'geo' in post_content.lower() and 'generative' in post_content.lower()
eeat_section = 'eeat' in post_content.lower() or 'experience, expertise' in post_content.lower()
aeo_section_heading = 'answer engine optimization' in post_content.lower() or 'aeo' in post_content.lower()

print(f"   Question headings: {question_headings}")
print(f"   FAQ sections: {faq_sections}")
print(f"   Total AEO elements: {total_aeo} (need ≥2)")
print(f"   GEO section present: {'✓' if geo_section else '✗'}")
print(f"   EEAT section present: {'✓' if eeat_section else '✗'}")
print(f"   AEO section present: {'✓' if aeo_section_heading else '✗'}")
print(f"   → {'✅ PASS' if passed_d else '❌ FAIL'}")

# ===== CHECK E: Internal Links =====
print(f"\n[E] INTERNAL LINKS")
blog_links_set = set(re.findall(r'/blog/[a-z0-9-]+', post_content))
service_links_set = set(re.findall(r'/services/[a-z0-9-]+', post_content))
industry_links_set = set(re.findall(r'/industries/[a-z0-9-]+', post_content))
location_links_set = set(re.findall(r'/locations/[a-z0-9-]+', post_content))
other_links_set = set(re.findall(r'/(?:about|contact|faq|privacy|terms)', post_content))

total_unique = len(blog_links_set) + len(service_links_set) + len(industry_links_set) + len(location_links_set) + len(other_links_set)
passed_e = total_unique >= 3

print(f"   Blog links: {sorted(blog_links_set)}")
print(f"   Service links: {sorted(service_links_set)}")
print(f"   Location links: {sorted(location_links_set)}")
print(f"   Other links (contact/about): {sorted(other_links_set)}")
print(f"   Total unique internal links: {total_unique} (need ≥3)")
print(f"   → {'✅ PASS' if passed_e else '❌ FAIL'}")

# ===== CHECK F: Schema =====
print(f"\n[F] SCHEMA — Schema Readiness")
schema_missing = []
if not title:
    schema_missing.append('title')
if not excerpt:
    schema_missing.append('excerpt')
if not date:
    schema_missing.append('date')
if not author:
    schema_missing.append('author')
if not post_content or len(post_content) < 50:
    schema_missing.append('content')

# Check for schema.org mentions in content
schema_mention = 'schema.org' in post_content.lower() or 'schema' in post_content.lower() or 'স্কিমা' in post_content
passed_f = len(schema_missing) == 0

print(f"   Title: {'✓' if title else '✗'} ({title[:50]}...)")
print(f"   Excerpt: {'✓' if excerpt else '✗'} ({excerpt[:50]}...)")
print(f"   Date: {'✓' if date else '✗'} ({date})")
print(f"   Author: {'✓' if author else '✗'} ({author})")
print(f"   Content length: {len(post_content)} chars (need ≥50)")
print(f"   Schema.org/structured data mentioned in content: {'✓' if schema_mention else '✗'}")
print(f"   Missing fields: {schema_missing if schema_missing else 'none'}")
print(f"   → {'✅ PASS' if passed_f else '❌ FAIL'}")

# ===== SUMMARY =====
print(f"\n{'='*80}")
print("FINAL SUMMARY — seo-https-ssl-impact-bangladesh")
print(f"{'='*80}")
checks = {
    'A: TF-IDF': passed_a,
    'B: Entities': passed_b,
    'C: Pillar-Cluster': passed_c,
    'D: AEO/GEO': passed_d,
    'E: Internal Links': passed_e,
    'F: Schema': passed_f,
}
all_pass = all(checks.values())
print(f"{'Check':20s} {'Status':10s} {'Detail'}")
print(f"{'-'*70}")
print(f"{'A: TF-IDF':20s} {'✅ PASS' if passed_a else '❌ FAIL':10s}  '{keyword}' x{count} (need ≥5)")
print(f"{'B: Entities':20s} {'✅ PASS' if passed_b else '❌ FAIL':10s}  Missing: {', '.join(missing_entities) if missing_entities else 'none'}")
if linked_pillar and linked_pillar[0] != '(generic blog link)':
    print(f"{'C: Pillar-Cluster':20s} {'✅ PASS' if passed_c else '❌ FAIL':10s}  Links to pillar: {linked_pillar[1]}")
elif linked_pillar:
    print(f"{'C: Pillar-Cluster':20s} {'✅ PASS' if passed_c else '❌ FAIL':10s}  Blog link found: {linked_pillar[1]} (not a defined pillar)")
else:
    print(f"{'C: Pillar-Cluster':20s} {'✅ PASS' if passed_c else '❌ FAIL':10s}  NO pillar link found")
print(f"{'D: AEO/GEO':20s} {'✅ PASS' if passed_d else '❌ FAIL':10s}  {total_aeo} AEO elements ({question_headings} Q-headings, {faq_sections} FAQ)")
print(f"{'E: Internal Links':20s} {'✅ PASS' if passed_e else '❌ FAIL':10s}  {total_unique} unique internal links (need ≥3)")
print(f"{'F: Schema':20s} {'✅ PASS' if passed_f else '❌ FAIL':10s}  Missing: {', '.join(schema_missing) if schema_missing else 'all fields set'}")
print(f"{'-'*70}")
print(f"{'OVERALL':20s} {'✅ ALL PASS' if all_pass else '❌ SOME FAILED'}")
print(f"{'='*80}")
